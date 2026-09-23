#!/usr/bin/env python3
"""
FOV-aware analysis of the new sound_tuning blocks:
    pure_tones, chord_tones, and fm_tones/fm_sounds.

The key design assumption is that all sound blocks assigned the same ``FOV#``
were acquired without moving the two-photon field of view and were processed
from one concatenated Suite2p binary. After the concatenated Suite2p result is
split back into per-session folders, ROI index i must therefore refer to the
same cell in every block belonging to that FOV.

``FOV#`` is the authoritative grouping field and starts at 0. It is expected to
be stored in each info2p session dictionary as, e.g. ``'FOV#': 0``. The same
FOV number may be reused on a different recording date; the unique key used by
this script is subject + date + FOV#.

For older info2p files without ``FOV#`` the script can infer provisional groups
from consecutive acquisition order, exact brainArea, depth, and duplicate block
labels. Inferred grouping is always marked as such in fov_manifest.csv. For an
ambiguous legacy day, use --fov-groups to override it explicitly rather than
silently accepting a questionable grouping.

Example
-------
python sound_tuning_multistim_fov_analysis_v3.py imag039 \
    --area A1 --dates 20260910

Legacy explicit grouping example (only needed before FOV# is added to info2p):
python sound_tuning_multistim_fov_analysis_v3.py imag039 \
    --area A1 --dates 20260910 \
    --fov-groups 20260910:000-001-002 20260910:006-007 20260910:008 20260910:009

Output
------
<TEMP_OUTPUT_PATH>/evan/sound_tuning_multistim_fov_analysis/<subject>/<area>/<date_tag>/
    fov_manifest.csv
    run_manifest.json
    fov_outputs/<date>_FOV###/...
    combined/
        combined_cell_results.csv
        combined_fov_summary.csv
        ... figures/statistics ...

Primary inference in combined summaries uses FOVs as the replicate. Pooled-cell
statistics, when written, are explicitly labeled exploratory.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import traceback
from pathlib import Path
from typing import Any, Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from jaratoolbox import settings
from jaratoolbox import twophotonanalysis

try:
    import torch
    from suite2p.detection.chan2detect import cellpose_overlap
except Exception as exc:  # pragma: no cover - resolved on analysis workstation
    torch = None
    cellpose_overlap = None
    _CELLPOSE_IMPORT_ERROR = exc
else:
    _CELLPOSE_IMPORT_ERROR = None


# =============================================================================
# PARAMETERS
# =============================================================================

PARADIGM = "sound_tuning"
BLOCK_ALIASES = {
    "pure_tones": "pure_tones",
    "pure_tone": "pure_tones",
    "chord_tones": "chord_tones",
    "chord_3t": "chord_tones",
    "fm_tones": "fm_tones",
    "fm_sounds": "fm_tones",
    "fm": "fm_tones",
}
BLOCK_ORDER = ("pure_tones", "chord_tones", "fm_tones")
BLOCK_SHORT = {"pure_tones": "pure", "chord_tones": "chord", "fm_tones": "fm"}
BLOCK_LABEL = {"pure_tones": "Pure tones", "chord_tones": "3-tone chords", "fm_tones": "FM sweeps"}

TIME_RANGE = (-1.0, 1.5)
BASELINE_RANGE = (-1.0, 0.0)
RESPONSE_RANGE = (0.0, 1.0)
MIN_FINITE_TRIALS = 3
DEFAULT_PERMUTATIONS = 4096
DEFAULT_SEED = 20260910

CELL_PROB_THRESHOLD = 0.0
IOU_THRESHOLD = 0.15
CELLPOSE_CELLPROB_THRESHOLD = -0.5
CELLPOSE_FLOW_THRESHOLD = 0.5
CELLPOSE_DIAMETER = None

GREEN = "green"
YELLOW = "yellow"
CELL_CLASSES = (GREEN, YELLOW)
CLASS_COLORS = {GREEN: "tab:green", YELLOW: "goldenrod"}
AREA_COLORS = {"A1": "tab:blue", "AAF": "tab:orange", "A2": "tab:purple"}

SELECTIVITY_SPEC = {
    "pure_tones": {
        "metric": "pure_lifetime_sparseness",
        "label": "Pure-tone selectivity (lifetime sparseness)",
        "equation": r"$S_{life}=\frac{1-(\overline{|R|})^2/\overline{|R|^2}}{1-1/n}$",
        "ylim": (-0.05, 1.05),
        "folder": "pure_tones",
    },
    "chord_tones": {
        "metric": "chord_harmonic_selectivity",
        "label": "Chord harmonic selectivity",
        "equation": r"$SI_{harm}=\frac{R_{harm}-\overline{R}_{nonharm}}{|R_{harm}|+|\overline{R}_{nonharm}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "chord_tones",
    },
    "fm_tones": {
        "metric": "fm_direction_selectivity",
        "label": "FM direction selectivity",
        "equation": r"$SI_{dir}=\frac{\overline{R}_{up}-\overline{R}_{down}}{|\overline{R}_{up}|+|\overline{R}_{down}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "fm_sounds",
    },
}


# =============================================================================
# CLI / I/O
# =============================================================================

def canonical_area(value: Any) -> str | None:
    u = str(value).upper()
    if "AAF" in u:
        return "AAF"
    if "A1" in u:
        return "A1"
    if "A2" in u or "AUV" in u:
        return "A2"
    return None


def canonical_block(value: Any) -> str | None:
    key = str(value).strip().lower()
    return BLOCK_ALIASES.get(key)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject")
    p.add_argument("--area", required=True, choices=["A1", "AAF", "A2"])
    p.add_argument("--dates", nargs="+", required=True)
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--n-permutations", type=int, default=DEFAULT_PERMUTATIONS)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument(
        "--fov-groups", nargs="*", default=None,
        help=("Legacy override groups, e.g. 20260910:000-001-002 20260910:006-007. "
              "Only needed when info2p lacks FOV# or needs an explicit legacy correction."),
    )
    p.add_argument("--dry-run", action="store_true", help="Discover/group FOVs and write no imaging outputs.")
    return p.parse_args()


def jsonable(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, Path):
        return str(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(jsonable(obj), indent=2), encoding="utf-8")


def output_dirs(subject: str, area: str, dates: list[str]) -> dict[str, Path]:
    tag = "_".join(dates)
    root = Path(settings.TEMP_OUTPUT_PATH) / "evan" / "sound_tuning_multistim_fov_analysis" / subject / area / tag
    fov = root / "fov_outputs"
    combined = root / "combined"
    fov.mkdir(parents=True, exist_ok=True)
    combined.mkdir(parents=True, exist_ok=True)
    return {"root": root, "fov": fov, "combined": combined}


# =============================================================================
# INFO2P / FOV GROUPING
# =============================================================================

def load_info2p(subject: str) -> tuple[Path, list[dict[str, Any]]]:
    path = Path(settings.INFO2P_PATH) / f"{subject}_info2p.py"
    if not path.exists():
        raise FileNotFoundError(f"info2p file not found: {path}")
    spec = importlib.util.spec_from_file_location(f"_multistim_{subject}_info2p", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sessions = getattr(mod, "sessions", None)
    if sessions is None:
        raise AttributeError(f"No sessions list found in {path}")
    return path, [dict(s) for s in sessions]


def select_new_sound_sessions(sessions: list[dict[str, Any]], dates: list[str], area: str) -> list[dict[str, Any]]:
    dset = set(map(str, dates))
    out = []
    for s in sessions:
        block = canonical_block(s.get("sessionLabel", ""))
        if (
            str(s.get("date", "")) in dset
            and str(s.get("paradigm", "")) == PARADIGM
            and canonical_area(s.get("brainArea", "")) == area
            and block in BLOCK_ORDER
        ):
            q = dict(s)
            q["canonicalArea"] = area
            q["block_type"] = block
            q["date"] = str(q.get("date", ""))
            q["session"] = str(q.get("session", "")).zfill(3)
            out.append(q)
    out.sort(key=lambda x: (x["date"], x["session"]))
    return out


def parse_fov_override(tokens: list[str] | None) -> dict[tuple[str, str], int]:
    """Return {(date, session): local_fov_number} from CLI groups."""
    mapping: dict[tuple[str, str], int] = {}
    if not tokens:
        return mapping
    by_date_counter: dict[str, int] = {}
    for token in tokens:
        if ":" not in token:
            raise ValueError(f"--fov-groups entry must have DATE:sessions form: {token}")
        date, sess_text = token.split(":", 1)
        fov_num = by_date_counter.get(date, 0)
        by_date_counter[date] = fov_num + 1
        for sess in sess_text.split("-"):
            key = (date, str(sess).zfill(3))
            if key in mapping:
                raise ValueError(f"Session repeated in --fov-groups: {key}")
            mapping[key] = fov_num
    return mapping


def _same_depth(a: Any, b: Any, tol: float = 1e-6) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return str(a) == str(b)


def assign_fovs(selected: list[dict[str, Any]], override_tokens: list[str] | None) -> list[dict[str, Any]]:
    """Assign FOVs, preferring CLI override, then FOV#, then legacy inference."""
    override = parse_fov_override(override_tokens)
    out = [dict(s) for s in selected]

    # Determine whether every selected session has an explicit FOV#.
    explicit_all = all(("FOV#" in s and s.get("FOV#") is not None) for s in out) if out else False

    if override:
        for s in out:
            k = (s["date"], s["session"])
            if k in override:
                s["fov_number"] = int(override[k])
                s["fov_grouping_source"] = "cli_override"
            elif "FOV#" in s and s.get("FOV#") is not None:
                s["fov_number"] = int(s["FOV#"])
                s["fov_grouping_source"] = "info2p_FOV#"
            else:
                s["fov_number"] = None
                s["fov_grouping_source"] = "unassigned"
        if any(s["fov_number"] is None for s in out):
            missing = [(s["date"], s["session"]) for s in out if s["fov_number"] is None]
            raise ValueError(f"CLI override did not cover all legacy sessions and no FOV# was present: {missing}")
    elif explicit_all:
        for s in out:
            s["fov_number"] = int(s["FOV#"])
            s["fov_grouping_source"] = "info2p_FOV#"
    else:
        # Conservative legacy inference: adjacency + exact raw brainArea + depth,
        # at most one block of each type in a provisional FOV. This cannot detect
        # within-session motion; inferred manifests must be reviewed.
        by_date: dict[str, list[dict[str, Any]]] = {}
        for s in out:
            by_date.setdefault(s["date"], []).append(s)
        for date, seq in by_date.items():
            fov_num = 0
            current: list[dict[str, Any]] = []
            for s in seq:
                if "FOV#" in s and s.get("FOV#") is not None:
                    # If a legacy day mixes explicit and absent values, preserve
                    # explicit values but start fresh around absent records.
                    s["fov_number"] = int(s["FOV#"])
                    s["fov_grouping_source"] = "info2p_FOV#"
                    current = []
                    fov_num = max(fov_num, int(s["FOV#"]) + 1)
                    continue
                start_new = not current
                if current:
                    prev0 = current[0]
                    blocks = {x["block_type"] for x in current}
                    start_new = (
                        str(s.get("brainArea")) != str(prev0.get("brainArea"))
                        or not _same_depth(s.get("depth"), prev0.get("depth"))
                        or s["block_type"] in blocks
                        or len(current) >= 3
                    )
                if start_new:
                    if current:
                        fov_num += 1
                    current = [s]
                else:
                    current.append(s)
                s["fov_number"] = fov_num
                s["fov_grouping_source"] = "legacy_inferred_REVIEW"

    for s in out:
        s["fov_uid"] = f"{s['date']}_FOV{int(s['fov_number']):03d}"
    return out


def validate_fov_groups(assigned: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for s in assigned:
        groups.setdefault(s["fov_uid"], []).append(s)
    rows = []
    for uid, seq in groups.items():
        seq.sort(key=lambda x: x["session"])
        areas = {str(s.get("brainArea")) for s in seq}
        depths = {str(s.get("depth")) for s in seq}
        blocks = [s["block_type"] for s in seq]
        if len(areas) > 1:
            raise ValueError(f"FOV {uid} contains multiple brainArea values: {areas}")
        if len(depths) > 1:
            # Exact FOV# is authoritative, but retain a warning in manifest.
            depth_warning = True
        else:
            depth_warning = False
        if len(blocks) != len(set(blocks)):
            raise ValueError(f"FOV {uid} contains duplicate block types: {blocks}")
        for s in seq:
            rows.append({
                "subject": s.get("subject"), "date": s["date"], "FOV#": int(s["fov_number"]),
                "fov_uid": uid, "session": s["session"], "block_type": s["block_type"],
                "sessionLabel": s.get("sessionLabel"), "brainArea": s.get("brainArea"),
                "canonicalArea": s.get("canonicalArea"), "depth": s.get("depth"),
                "fps": s.get("fps"), "nFrames": s.get("nFrames"),
                "grouping_source": s.get("fov_grouping_source"),
                "depth_mismatch_within_FOV": depth_warning,
            })
    return rows


# =============================================================================
# STATISTICS / METRICS
# =============================================================================

def finite(x: Iterable[Any]) -> np.ndarray:
    a = np.asarray(list(x) if not isinstance(x, np.ndarray) else x, dtype=float).ravel()
    return a[np.isfinite(a)]


def mean_sem(x: Iterable[Any]) -> tuple[float, float, int]:
    a = finite(x)
    if len(a) == 0:
        return np.nan, np.nan, 0
    return float(np.mean(a)), float(stats.sem(a)) if len(a) > 1 else np.nan, int(len(a))


def holm_adjust(pvals: Iterable[Any]) -> np.ndarray:
    p = np.asarray(list(pvals), dtype=float)
    out = np.full_like(p, np.nan)
    idx = np.flatnonzero(np.isfinite(p))
    if not len(idx):
        return out
    vals = p[idx]
    order = np.argsort(vals)
    ranked = vals[order]
    adj = np.maximum.accumulate((len(ranked) - np.arange(len(ranked))) * ranked)
    adj = np.minimum(adj, 1.0)
    out[idx[order]] = adj
    return out


def bh_fdr(p_values: np.ndarray, valid_mask: np.ndarray | None = None) -> np.ndarray:
    p = np.asarray(p_values, dtype=float)
    if valid_mask is None:
        valid_mask = np.isfinite(p)
    else:
        valid_mask = np.asarray(valid_mask, dtype=bool) & np.isfinite(p)
    q = np.full_like(p, np.nan)
    inds = np.flatnonzero(valid_mask)
    if len(inds) == 0:
        return q
    vals = p[inds]
    order = np.argsort(vals)
    ranked = vals[order]
    m = len(ranked)
    adj = ranked * m / np.arange(1, m + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.minimum(adj, 1.0)
    q[inds[order]] = adj
    return q


def signflip_pvalues_grouped(response_matrix: np.ndarray, tested_mask: np.ndarray,
                              n_permutations: int, rng: np.random.Generator) -> np.ndarray:
    response_matrix = np.asarray(response_matrix, dtype=float)
    tested_mask = np.asarray(tested_mask, dtype=bool)
    p_values = np.full(response_matrix.shape[0], np.nan)
    groups: dict[bytes, list[int]] = {}
    masks: dict[bytes, np.ndarray] = {}
    for ci in np.flatnonzero(tested_mask):
        fm = np.isfinite(response_matrix[ci])
        key = np.packbits(fm).tobytes()
        groups.setdefault(key, []).append(int(ci)); masks[key] = fm
    for key, cis in groups.items():
        fm = masks[key]; n = int(fm.sum())
        if n < MIN_FINITE_TRIALS:
            continue
        vals = response_matrix[np.asarray(cis)][:, fm]
        obs = vals.mean(axis=1)
        signs = rng.choice(np.array([-1., 1.], dtype=np.float32), size=(n_permutations, n))
        null = (signs @ vals.T) / n
        extreme = np.sum(np.abs(null) >= np.abs(obs)[None, :], axis=0)
        p_values[np.asarray(cis)] = (1 + extreme) / (n_permutations + 1)
    return p_values


def bounded_selectivity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a, float); b = np.asarray(b, float)
    den = np.abs(a) + np.abs(b)
    out = np.full(np.broadcast(a, b).shape, np.nan)
    ok = np.isfinite(a) & np.isfinite(b) & (den > 0)
    out[ok] = (a[ok] - b[ok]) / den[ok]
    return out


def lifetime_sparseness_rows(mat: np.ndarray) -> np.ndarray:
    x = np.abs(np.asarray(mat, float))
    n = x.shape[1]
    out = np.full(x.shape[0], np.nan)
    if n <= 1:
        return out
    for i, row in enumerate(x):
        v = row[np.isfinite(row)]
        if len(v) <= 1:
            continue
        m1 = np.mean(v); m2 = np.mean(v ** 2)
        if m2 <= 0:
            continue
        out[i] = (1 - (m1 ** 2 / m2)) / (1 - 1 / len(v))
    return out


def gini_rows(mat: np.ndarray) -> np.ndarray:
    x = np.abs(np.asarray(mat, float)); out = np.full(x.shape[0], np.nan)
    for i, row in enumerate(x):
        v = row[np.isfinite(row)]
        if not len(v) or np.sum(v) <= 0:
            continue
        v = np.sort(v); n = len(v)
        out[i] = np.sum((2 * np.arange(1, n + 1) - n - 1) * v) / (n * np.sum(v))
    return out


def fano_rows(mat: np.ndarray) -> np.ndarray:
    x = np.abs(np.asarray(mat, float)); out = np.full(x.shape[0], np.nan)
    for i, row in enumerate(x):
        v = row[np.isfinite(row)]
        if len(v) < 2 or np.mean(v) <= 0:
            continue
        out[i] = np.var(v, ddof=1) / np.mean(v)
    return out


def fwhm_log2_rows(mat: np.ndarray, values: np.ndarray) -> np.ndarray:
    """FWHM using linear interpolation in log2(value); boundary/unbracketed -> NaN."""
    mat = np.asarray(mat, float); values = np.asarray(values, float)
    out = np.full(mat.shape[0], np.nan)
    if len(values) < 3 or np.any(values <= 0):
        return out
    order = np.argsort(values); x = np.log2(values[order]); ymat = mat[:, order]
    for i, y0 in enumerate(ymat):
        y = np.asarray(y0, float)
        if not np.all(np.isfinite(y)):
            continue
        pk = int(np.argmax(y)); peak = y[pk]
        if pk == 0 or pk == len(y)-1 or peak <= 0:
            continue
        half = peak / 2.0
        li = np.flatnonzero(y[:pk] <= half)
        ri = np.flatnonzero(y[pk+1:] <= half)
        if not len(li) or not len(ri):
            continue
        l0 = li[-1]; l1 = l0 + 1
        r1 = pk + 1 + ri[0]; r0 = r1 - 1
        def interp(xa, ya, xb, yb):
            if yb == ya: return np.nan
            return xa + (half - ya) * (xb - xa) / (yb - ya)
        xl = interp(x[l0], y[l0], x[l1], y[l1])
        xr = interp(x[r0], y[r0], x[r1], y[r1])
        if np.isfinite(xl) and np.isfinite(xr) and xr >= xl:
            out[i] = xr - xl
    return out


def safe_wilcoxon_pairs(tab: pd.DataFrame, a_col: str, b_col: str) -> dict[str, Any]:
    sub = tab[[a_col, b_col]].dropna()
    if len(sub) < 2:
        return {"n_pairs": len(sub), "W": np.nan, "p": np.nan}
    d = sub[a_col].to_numpy(float) - sub[b_col].to_numpy(float)
    if np.allclose(d, 0):
        return {"n_pairs": len(sub), "W": 0.0, "p": 1.0}
    try:
        r = stats.wilcoxon(sub[a_col], sub[b_col], alternative="two-sided", zero_method="wilcox")
        return {"n_pairs": len(sub), "W": float(r.statistic), "p": float(r.pvalue)}
    except Exception:
        return {"n_pairs": len(sub), "W": np.nan, "p": np.nan}


# =============================================================================
# EVENT ALIGNMENT / CELL CLASSIFICATION
# =============================================================================

def align_imaging_events_to_behavior(eventlocked: np.ndarray, valid_events: np.ndarray,
                                     event_onset: np.ndarray, srate: float,
                                     stim_duration: np.ndarray, isi: np.ndarray,
                                     n_behavior_trials: int,
                                     max_extra_events: int = 5,
                                     max_mean_abs_error_s: float = 0.25,
                                     max_abs_error_s: float = 0.75):
    valid_events = np.asarray(valid_events, bool); event_onset = np.asarray(event_onset, float)
    n_im = int(eventlocked.shape[1])
    if len(valid_events) != n_im or len(event_onset) != n_im:
        raise ValueError("Event arrays have inconsistent lengths")
    if n_im < n_behavior_trials:
        raise ValueError(f"Fewer imaging events ({n_im}) than behavioral trials ({n_behavior_trials})")
    extra = n_im - n_behavior_trials
    if extra > max_extra_events:
        raise ValueError(f"Too many extra imaging events ({extra}); automatic trim limited to {max_extra_events}")
    ev = eventlocked[:, :n_behavior_trials, :]
    va = valid_events[:n_behavior_trials]
    eo = event_onset[:n_behavior_trials]
    sd = np.asarray(stim_duration, float).reshape(-1); ii = np.asarray(isi, float).reshape(-1)
    exp = sd[:n_behavior_trials-1] + ii[:n_behavior_trials-1]
    obs = np.diff(eo) / float(srate)
    ok = np.isfinite(exp) & np.isfinite(obs)
    if not np.any(ok):
        raise ValueError("No finite onset intervals for alignment QC")
    err = obs[ok] - exp[ok]
    mae = float(np.mean(np.abs(err))); mx = float(np.max(np.abs(err)))
    if mae > max_mean_abs_error_s or mx > max_abs_error_s:
        raise ValueError(f"Alignment timing QC failed: MAE={mae:.3f}s max={mx:.3f}s")
    diag = {"n_imaging_events": n_im, "n_behavior_trials": n_behavior_trials,
            "n_extra_trailing": extra, "timing_mae_s": mae, "timing_max_abs_error_s": mx}
    return ev, va, eo, diag


def roi_signature(stat_array: np.ndarray, roi_indices: np.ndarray) -> np.ndarray:
    rows = []
    for idx in roi_indices:
        st = stat_array[int(idx)]
        yp = np.asarray(st["ypix"], float); xp = np.asarray(st["xpix"], float)
        rows.append([len(yp), np.mean(yp) if len(yp) else np.nan, np.mean(xp) if len(xp) else np.nan])
    return np.asarray(rows, float)


def classify_fov_cells(reference_data2p, plane: int, out_dir: Path) -> dict[str, Any]:
    if cellpose_overlap is None or torch is None:
        raise ImportError(f"Suite2p Cellpose overlap import failed: {_CELLPOSE_IMPORT_ERROR}")
    sdir = Path(reference_data2p.data_path)
    ops = np.load(sdir / "ops.npy", allow_pickle=True).item()
    stat_array = np.load(sdir / "stat.npy", allow_pickle=True)
    redcell_path = sdir / "redcell.npy"
    redcell = np.load(redcell_path) if redcell_path.exists() else None
    cell_mask = (reference_data2p.iscell[:, 0] == 1) & (reference_data2p.iscell[:, 1] > CELL_PROB_THRESHOLD)
    roi_idx = np.flatnonzero(cell_mask)
    fstats = stat_array[roi_idx]
    if ops.get("meanImg_chan2") is not None:
        red_img = np.asarray(ops["meanImg_chan2"], float)
    elif ops.get("meanImg_chan2_corrected") is not None:
        red_img = np.asarray(ops["meanImg_chan2_corrected"], float)
    else:
        raise KeyError("No meanImg_chan2 in ops.npy; cannot classify GREEN/YELLOW")
    if ops.get("meanImg") is None:
        raise KeyError("No meanImg in ops.npy")
    green_img = np.asarray(ops["meanImg"], float)
    diameters = [2*np.sqrt(len(st["ypix"])/np.pi) for st in fstats if len(st["ypix"]) > 0]
    diameter = float(np.median(diameters)) if CELLPOSE_DIAMETER is None else float(CELLPOSE_DIAMETER)
    cp_settings = {"params": None, "chan2_params": None,
                   "cellprob_threshold": CELLPOSE_CELLPROB_THRESHOLD,
                   "flow_threshold": CELLPOSE_FLOW_THRESHOLD}
    redstats, redmasks = cellpose_overlap(
        fstats, red_img, diameter=diameter, chan2_threshold=IOU_THRESHOLD,
        device=torch.device("cpu"), settings=cp_settings)
    iou = np.asarray(redstats[:, 1], float)
    yellow = iou > IOU_THRESHOLD
    classes = np.where(yellow, YELLOW, GREEN)
    legacy = np.full(len(roi_idx), np.nan)
    if redcell is not None and redcell.ndim == 2 and redcell.shape[1] > 1:
        legacy = np.asarray(redcell[roi_idx, 1], float)

    # Compact classification overlay.
    fig, ax = plt.subplots(figsize=(8, 8))
    lo, hi = np.nanpercentile(green_img[np.isfinite(green_img)], [1, 99.5])
    ax.imshow(green_img, cmap="gray", vmin=lo, vmax=hi)
    for j, st in enumerate(fstats):
        y = np.asarray(st["ypix"], int); x = np.asarray(st["xpix"], int)
        ax.scatter(x, y, s=1.2, alpha=0.35, c=CLASS_COLORS[classes[j]])
    ax.set_title(f"Shared FOV cell classification: GREEN={np.sum(classes==GREEN)}, YELLOW={np.sum(classes==YELLOW)}")
    ax.set_axis_off(); fig.tight_layout()
    fig.savefig(out_dir / "shared_FOV_green_yellow_classification.png", dpi=250, bbox_inches="tight")
    plt.close(fig)

    return {"roi_indices": roi_idx, "cell_mask": cell_mask, "cell_class": classes,
            "red_iou": iou, "legacy_red_score": legacy,
            "stat_signature": roi_signature(stat_array, roi_idx),
            "suite2p_dir": str(sdir), "cellpose_diameter": diameter}


def verify_shared_rois(data2p, reference: dict[str, Any]) -> None:
    sdir = Path(data2p.data_path)
    stat_array = np.load(sdir / "stat.npy", allow_pickle=True)
    roi_idx = np.asarray(reference["roi_indices"], int)
    if np.max(roi_idx, initial=-1) >= len(stat_array):
        raise ValueError(f"Suite2p ROI count differs across sessions in an FOV: {sdir}")
    sig = roi_signature(stat_array, roi_idx)
    refsig = np.asarray(reference["stat_signature"], float)
    if sig.shape != refsig.shape or not np.allclose(sig, refsig, atol=1e-6, equal_nan=True):
        raise ValueError(
            "ROI geometry/indexing differs across sessions assigned to the same FOV. "
            "These sessions do not appear to be split products of one concatenated Suite2p analysis."
        )





def _fm_log_positions(values):
    """Signed log2-magnitude coordinates with uniform spacing of tested FM levels.

    The FM stimulus generator uses log-spaced nonzero slope magnitudes. This
    transform preserves that log spacing on both sides of zero. If a 0-slope
    condition is present it occupies the center; if it is absent, the two
    smallest-magnitude slopes straddle the center with the same spacing as all
    other adjacent tested levels.
    """
    values = np.asarray(values, float)
    out = np.full(values.shape, np.nan, float)
    finite = np.isfinite(values)
    mags = np.sort(np.unique(np.abs(values[finite & (values != 0)])))
    if not len(mags):
        out[finite] = 0.0
        return out
    lm = np.log2(mags)
    step = float(np.median(np.diff(lm))) if len(lm) > 1 else 1.0
    if not np.isfinite(step) or step <= 0:
        step = 1.0
    base = step if np.any(finite & np.isclose(values, 0.0)) else 0.5 * step
    logdist = np.log2(np.abs(values[finite & (values != 0)]) / mags[0])
    out[finite & (values != 0)] = np.sign(values[finite & (values != 0)]) * (base + logdist)
    out[finite & np.isclose(values, 0.0)] = 0.0
    return out

def _selectivity_equation_box(ax, block):
    spec = SELECTIVITY_SPEC[block]
    ax.text(
        0.02, 0.03, spec["equation"], transform=ax.transAxes, ha="left", va="bottom",
        fontsize=9.5, bbox=dict(boxstyle="round,pad=0.32", facecolor="white", edgecolor="0.75", alpha=0.95),
    )

def _readable_condition_ticks(ax, x, labels, dense_threshold=10):
    """Readable condition labels: dense axes label every other tick, rotated ~60 deg."""
    x=np.asarray(x,float); labels=list(labels)
    ax.set_xticks(x)
    if len(labels)>=dense_threshold:
        shown=[lab if (i%2==0) else "" for i,lab in enumerate(labels)]
        ax.set_xticklabels(shown, rotation=60, ha="right", rotation_mode="anchor")
    else:
        ax.set_xticklabels(labels, rotation=45 if len(labels)>6 else 0, ha="right" if len(labels)>6 else "center")


def _condition_axis(block, values):
    values=np.asarray(values,float)
    if block=="pure_tones":
        x=np.log2(values/1000.0); labels=[f"{v/1000:g}" for v in values]; xlabel="Frequency (kHz; log2 spacing)"
    elif block=="chord_tones":
        x=values; labels=[f"{v:.3g}" for v in values]; xlabel="Middle tone position (octaves above F0)"
    else:
        x=_fm_log_positions(values); labels=[f"{v:g}" for v in values]; xlabel="FM slope (octaves/s; signed log2-magnitude spacing)"
    return x,labels,xlabel


def _cell_scalar_sem(trial_response, cond_trial, valid, cell_index, values):
    out=[]
    for v in values:
        m=np.asarray(valid,bool)&np.isclose(cond_trial,v,rtol=1e-8,atol=1e-10)
        z=np.asarray(trial_response[cell_index,m],float); z=z[np.isfinite(z)]
        out.append(float(stats.sem(z)) if len(z)>1 else np.nan)
    return np.asarray(out,float)


def _save_tuning_pages(block, values, curve, pref_val, pref_resp, responsive, roi_idx, classes, out_dir):
    """Paginated 3x2 tuning-curve pages for all FDR-responsive cells."""
    root=out_dir/'individual_tuning_pages'/block
    root.mkdir(parents=True,exist_ok=True)
    idx=np.flatnonzero(np.asarray(responsive,bool))
    if not len(idx): return
    # Sort by preferred condition, then strongest preferred response within that condition.
    idx=sorted(idx,key=lambda i:(np.inf if not np.isfinite(pref_val[i]) else pref_val[i],
                                 -(abs(pref_resp[i]) if np.isfinite(pref_resp[i]) else -np.inf), int(roi_idx[i])))
    x,labels,xlabel=_condition_axis(block,values)
    for pg,start in enumerate(range(0,len(idx),6),start=1):
        subset=idx[start:start+6]
        fig,axes=plt.subplots(3,2,figsize=(12,13),squeeze=False)
        for ax in axes.ravel(): ax.axis('off')
        for ax,i in zip(axes.ravel(),subset):
            ax.axis('on')
            ax.plot(x,curve[i],marker='o',lw=1.8,color=CLASS_COLORS.get(str(classes[i]),'0.25'))
            ax.axhline(0,color='0.55',ls='--',lw=.8)
            _readable_condition_ticks(ax,x,labels)
            ax.set_xlabel(xlabel); ax.set_ylabel('Mean response (dF/F)')
            ax.set_title(f"ROI {int(roi_idx[i])} | {str(classes[i]).upper()} | preferred={pref_val[i]:.4g}")
            ax.grid(axis='y',alpha=.15)
            ax.spines[['top','right']].set_visible(False)
        fig.suptitle(f"{BLOCK_LABEL[block]} tuning — FDR-responsive cells — page {pg}",fontsize=15)
        fig.tight_layout(rect=[0,0,1,.97]); fig.savefig(root/f"page_{pg:03d}.png",dpi=250); plt.close(fig)


def _save_pure_bf_histograms(df, values, out_dir):
    if 'pure_best_frequency_hz' not in df or 'pure_responsive_fdr' not in df: return
    use=df[df['pure_responsive_fdr'].fillna(False).astype(bool)&pd.to_numeric(df['pure_best_frequency_hz'],errors='coerce').notna()].copy()
    if use.empty: return
    root=out_dir/'best_frequency'; root.mkdir(parents=True,exist_ok=True)
    vals=np.asarray(values,float); x=np.log2(vals/1000.0); width=np.min(np.diff(x))*.8 if len(x)>1 else .7
    fig,axes=plt.subplots(2,1,figsize=(11,9),sharex=True)
    for cls in CELL_CLASSES:
        arr=pd.to_numeric(use.loc[use.cell_class==cls,'pure_best_frequency_hz'],errors='coerce').to_numpy(float)
        counts=np.array([np.sum(np.isclose(arr,v)) for v in vals],float)
        frac=counts/counts.sum() if counts.sum()>0 else np.full_like(counts,np.nan)
        offset=-.2*width if cls==GREEN else .2*width
        axes[0].bar(x+offset,counts,width=.38*width,label=f"{cls.upper()} n={len(arr)}",alpha=.75)
        axes[1].plot(x,frac,marker='o',lw=2,label=f"{cls.upper()} n={len(arr)}",color=CLASS_COLORS[cls])
    axes[0].set_ylabel('Responsive cells (count)'); axes[1].set_ylabel('Fraction of responsive cells'); axes[1].set_xlabel('Best frequency (kHz; log2 spacing)')
    _readable_condition_ticks(axes[1],x,[f"{v/1000:g}" for v in vals]); axes[0].legend(frameon=False); axes[1].legend(frameon=False)
    fig.suptitle('Best-frequency distribution — pure-tone FDR-responsive cells'); fig.tight_layout(rect=[0,0,1,.96]); fig.savefig(root/'best_frequency_histogram_counts_and_fraction.png',dpi=250); plt.close(fig)


def _archive_cell_report_data(archive_path):
    with np.load(str(archive_path),allow_pickle=False) as z:
        return {k:z[k] for k in z.files}


def _save_cell_reports(base, block_meta, fov_dir):
    """One PNG per cell responsive to >=1 available sound block."""
    resp_cols=[f"{BLOCK_SHORT[b]}_responsive_fdr" for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_responsive_fdr" in base]
    if not resp_cols: return
    anyresp=np.zeros(len(base),bool)
    for c in resp_cols: anyresp|=base[c].fillna(False).astype(bool).to_numpy()
    if not anyresp.any(): return
    archives={b:_archive_cell_report_data(meta['trial_archive']) for b,meta in block_meta.items()}
    root=fov_dir/'cell_reports'
    for cls in CELL_CLASSES: (root/cls).mkdir(parents=True,exist_ok=True)
    for ridx,row in base.loc[anyresp].iterrows():
        cls=str(row['cell_class']); roi=int(row['suite2p_roi_index']); acell=int(row['analysis_cell_index'])
        fig,axes=plt.subplots(3,2,figsize=(14,15),squeeze=False)
        for rr,b in enumerate(BLOCK_ORDER):
            axtr,axtu=axes[rr]
            if b not in archives:
                axtr.axis('off'); axtu.axis('off'); axtr.text(.5,.5,f"{BLOCK_LABEL[b]}\nnot acquired in this FOV",ha='center',va='center',transform=axtr.transAxes); continue
            arc=archives[b]; rois=np.asarray(arc['suite2p_roi_index'],int); hits=np.flatnonzero(rois==roi)
            if not len(hits): axtr.axis('off'); axtu.axis('off'); continue
            i=int(hits[0]); vals=np.asarray(arc['condition_values'],float); t=np.asarray(arc['tvec'],float)
            tm=np.asarray(arc['condition_trace_mean'],float)[i]; ts=np.asarray(arc['condition_trace_sem'],float)[i]
            cmap=plt.cm.viridis(np.linspace(.08,.92,len(vals)))
            for j,v in enumerate(vals):
                axtr.plot(t,tm[j],lw=1.4,color=cmap[j],label=f"{v:g}")
                if np.any(np.isfinite(ts[j])): axtr.fill_between(t,tm[j]-ts[j],tm[j]+ts[j],color=cmap[j],alpha=.08,lw=0)
            axtr.axvline(0,color='k',ls=':',lw=.9); axtr.axhline(0,color='.55',ls='--',lw=.7); axtr.set_xlabel('Time from sound onset (s)'); axtr.set_ylabel('Baseline-subtracted dF/F'); axtr.set_title(f"{BLOCK_LABEL[b]}: mean ± SEM traces")
            tr=np.asarray(arc['trial_response'],float); cond=np.asarray(arc['trial_condition_value'],float); valid=np.asarray(arc['valid_trial_mask'],bool)
            means=np.array([np.nanmean(tr[i,valid&np.isclose(cond,v)]) for v in vals]); sems=_cell_scalar_sem(tr,cond,valid,i,vals)
            x,labels,xlabel=_condition_axis(b,vals); axtu.errorbar(x,means,yerr=sems,marker='o',lw=1.8,capsize=3,color=CLASS_COLORS.get(cls,'0.25'))
            axtu.axhline(0,color='.55',ls='--',lw=.8); _readable_condition_ticks(axtu,x,labels); axtu.set_xlabel(xlabel); axtu.set_ylabel('Mean response (dF/F)'); axtu.set_title(f"{BLOCK_LABEL[b]} tuning")
            axtu.spines[['top','right']].set_visible(False); axtr.spines[['top','right']].set_visible(False)
        bits=[]
        if np.isfinite(pd.to_numeric(pd.Series([row.get('pure_best_frequency_hz',np.nan)]),errors='coerce').iloc[0]): bits.append(f"BF={float(row['pure_best_frequency_hz'])/1000:.3g} kHz")
        bits.append('responsive: '+', '.join([BLOCK_LABEL[b] for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_responsive_fdr" in row and bool(row.get(f"{BLOCK_SHORT[b]}_responsive_fdr",False))]))
        fig.suptitle(f"Cell report | {row['subject']} {row['date']} FOV#{int(row['FOV#'])} | {row['canonicalArea']} depth={row['depth']:.1f} um\nROI {roi} | analysis cell {acell} | {cls.upper()} | "+' | '.join(bits),fontsize=14)
        fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(root/cls/f"ROI_{roi:05d}_cell_report.png",dpi=250); plt.close(fig)


def _save_combined_bf_outputs(cells,out_dir):
    if 'pure_best_frequency_hz' not in cells or 'pure_responsive_fdr' not in cells: return
    use=cells[cells['pure_responsive_fdr'].fillna(False).astype(bool)&pd.to_numeric(cells['pure_best_frequency_hz'],errors='coerce').notna()].copy()
    if use.empty:return
    root=out_dir/'best_frequency'; root.mkdir(parents=True,exist_ok=True)
    vals=np.sort(pd.to_numeric(use['pure_best_frequency_hz'],errors='coerce').dropna().unique()); x=np.log2(vals/1000)
    # FOV x BF fraction heatmaps separately by class.
    for cls in CELL_CLASSES:
        rows=[]; labels=[]
        for uid,g in use[use.cell_class==cls].groupby('fov_uid'):
            arr=pd.to_numeric(g['pure_best_frequency_hz'],errors='coerce').to_numpy(float); arr=arr[np.isfinite(arr)]
            if not len(arr):continue
            rows.append([np.mean(np.isclose(arr,v)) for v in vals]); labels.append(str(uid))
        if rows:
            M=np.asarray(rows,float); fig,ax=plt.subplots(figsize=(11,max(4,0.42*len(rows)+2.5))); im=ax.imshow(M,aspect='auto',vmin=0,vmax=np.nanmax(M) if np.nanmax(M)>0 else 1,cmap='viridis')
            ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels); ax.set_xticks(range(len(vals))); labs=[f"{v/1000:g}" if i%2==0 else '' for i,v in enumerate(vals)]; ax.set_xticklabels(labs,rotation=60,ha='right'); ax.set_xlabel('Best frequency (kHz)'); ax.set_ylabel('FOV'); ax.set_title(f"{cls.upper()} — fraction of responsive cells by BF within each FOV"); fig.colorbar(im,ax=ax,label='Fraction of cells'); fig.tight_layout(); fig.savefig(root/f"FOV_by_best_frequency_fraction_{cls}.png",dpi=250); plt.close(fig)
    # Per-FOV median BF summary by class.
    fig,ax=plt.subplots(figsize=(7,5.5)); rng=np.random.default_rng(117)
    for pos,cls in enumerate(CELL_CLASSES):
        meds=[]; ns=[]
        for uid,g in use[use.cell_class==cls].groupby('fov_uid'):
            arr=np.log2(pd.to_numeric(g['pure_best_frequency_hz'],errors='coerce').to_numpy(float)); arr=arr[np.isfinite(arr)]
            if len(arr): meds.append(np.median(arr)); ns.append(len(arr))
        if meds:
            sizes=35+6*np.sqrt(np.asarray(ns)); ax.scatter(np.full(len(meds),pos)+rng.uniform(-.06,.06,len(meds)),np.asarray(meds),s=sizes,facecolors=CLASS_COLORS[cls],edgecolors='none',alpha=.8,label=cls.upper())
            mu,se,n=mean_sem(meds); ax.errorbar(pos,mu,yerr=se,fmt='o',color='black',capsize=4,zorder=4)
    ax.set_xticks([0,1]); ax.set_xticklabels(['GREEN','YELLOW']); ax.set_ylabel('FOV median log2(BF [Hz])'); ax.set_title('Pure-tone BF center across FOVs\nmarker size reflects responsive-cell count; no class-colored outlines'); fig.tight_layout(); fig.savefig(root/'FOV_median_best_frequency_GREEN_YELLOW.png',dpi=250); plt.close(fig)

# =============================================================================
# BLOCK ANALYSIS
# =============================================================================

def condition_column_name(block: str, value: float) -> str:
    if block == "pure_tones":
        return f"pure_response_{value:.6g}_Hz"
    if block == "chord_tones":
        return f"chord_response_middle_oct_{value:.6g}"
    return f"fm_response_slope_{value:+.6g}_oct_per_s".replace("+", "pos").replace("-", "neg")


def condition_q_column_name(block: str, value: float) -> str:
    return condition_column_name(block, value).replace("_response_", "_response_q_")


def _trial_response(eventlocked: np.ndarray, tvec: np.ndarray) -> np.ndarray:
    b = (tvec >= BASELINE_RANGE[0]) & (tvec < BASELINE_RANGE[1])
    r = (tvec >= RESPONSE_RANGE[0]) & (tvec < RESPONSE_RANGE[1])
    return np.nanmean(eventlocked[:, :, r], axis=2) - np.nanmean(eventlocked[:, :, b], axis=2)


def _block_condition_values(block: str, bdata: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    if block == "pure_tones":
        vals = np.asarray(bdata["current_tone_freq"], float)
        return vals, {"condition_unit": "Hz"}
    if block == "chord_tones":
        vals = np.asarray(bdata["current_chord3t_middle_octave"], float)
        f0arr = np.asarray(bdata["chord3t_F0"], float)
        f0 = float(np.nanmedian(f0arr))
        return vals, {"condition_unit": "octaves above F0", "F0_hz": f0}
    vals = np.asarray(bdata["current_FM_slope"], float)
    c = np.asarray(bdata["FM_center_freq"], float)
    center = float(np.nanmedian(c))
    return vals, {"condition_unit": "octaves/s", "center_frequency_hz": center}


def analyze_block(meta: dict[str, Any], plane: int, fov_reference: dict[str, Any],
                  out_dir: Path, n_permutations: int, seed: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    subject, date, session = str(meta["subject"]), str(meta["date"]), str(meta["session"])
    block = str(meta["block_type"]); prefix = BLOCK_SHORT[block]
    data2p = twophotonanalysis.TwoPhoton(subject, date, session, plane, paradigm=PARADIGM)
    verify_shared_rois(data2p, fov_reference)
    roi_idx = np.asarray(fov_reference["roi_indices"], int)

    ev_all, tvec, valid = data2p.event_locked_average(time_range=list(TIME_RANGE), dff=True)
    ev = np.asarray(ev_all[roi_idx], float)
    bdata = data2p.bdata
    required = ["stim_duration", "ISI"]
    if block == "pure_tones": required += ["current_tone_freq"]
    if block == "chord_tones": required += ["current_chord3t_middle_octave", "chord3t_F0"]
    if block == "fm_tones": required += ["current_FM_slope", "FM_center_freq"]
    missing = [k for k in required if k not in bdata]
    if missing:
        raise KeyError(f"Missing behavior fields for {block}: {missing}")
    cond_trial, extras = _block_condition_values(block, bdata)
    ntr = len(cond_trial)
    ev, valid, event_onset, align_diag = align_imaging_events_to_behavior(
        ev, valid, np.asarray(data2p.event_onset), float(data2p.srate),
        np.asarray(bdata["stim_duration"], float), np.asarray(bdata["ISI"], float), ntr)
    tvec_arr=np.asarray(tvec,float)
    bmask=(tvec_arr>=BASELINE_RANGE[0])&(tvec_arr<BASELINE_RANGE[1])
    ev_bc=ev-np.nanmean(ev[:,:,bmask],axis=2)[:,:,None]
    tr = _trial_response(ev, tvec_arr)
    tr[:, ~np.asarray(valid, bool)] = np.nan

    values = np.sort(np.unique(cond_trial[np.isfinite(cond_trial)]))
    curve = np.full((len(roi_idx), len(values)), np.nan)
    pmat = np.full_like(curve, np.nan); qmat = np.full_like(curve, np.nan); sigmat = np.zeros_like(curve, bool)
    trace_mean=np.full((len(roi_idx),len(values),ev_bc.shape[2]),np.nan,dtype=float)
    trace_sem=np.full_like(trace_mean,np.nan)
    rng = np.random.default_rng(seed)
    counts = []
    for j, val in enumerate(values):
        tm = np.asarray(valid, bool) & np.isclose(cond_trial, val, rtol=1e-8, atol=1e-10)
        counts.append(int(tm.sum()))
        curve[:, j] = np.nanmean(tr[:, tm], axis=1)
        if np.any(tm):
            trace_mean[:,j,:]=np.nanmean(ev_bc[:,tm,:],axis=1)
            trace_sem[:,j,:]=stats.sem(ev_bc[:,tm,:],axis=1,nan_policy="omit") if int(tm.sum())>1 else np.nan
        tested = np.sum(np.isfinite(tr[:, tm]), axis=1) >= MIN_FINITE_TRIALS
        p = signflip_pvalues_grouped(tr[:, tm], tested, n_permutations, rng)
        q = bh_fdr(p, tested)
        pmat[:, j] = p; qmat[:, j] = q; sigmat[:, j] = np.isfinite(q) & (q < 0.05)

    resp_any = np.any(sigmat, axis=1)
    # Sign based on the largest-absolute significant condition response.
    excited = np.zeros(len(roi_idx), bool); suppressed = np.zeros(len(roi_idx), bool)
    for i in range(len(roi_idx)):
        jj = np.flatnonzero(sigmat[i])
        if not len(jj): continue
        bestj = jj[np.nanargmax(np.abs(curve[i, jj]))]
        excited[i] = curve[i, bestj] > 0; suppressed[i] = curve[i, bestj] < 0

    # Standard tuning metrics.
    pref_idx = np.full(len(roi_idx), -1, int)
    for i, row in enumerate(curve):
        if np.any(np.isfinite(row)):
            pref_idx[i] = int(np.nanargmax(row))
    pref_val = np.array([values[j] if j >= 0 else np.nan for j in pref_idx], float)
    pref_resp = np.array([curve[i, j] if j >= 0 else np.nan for i, j in enumerate(pref_idx)], float)
    sparse = lifetime_sparseness_rows(curve); gini = gini_rows(curve); fano = fano_rows(curve)

    df = pd.DataFrame({
        "analysis_cell_index": np.arange(len(roi_idx)),
        "suite2p_roi_index": roi_idx,
        "cell_class": np.asarray(fov_reference["cell_class"]),
        "cellpose_red_iou": np.asarray(fov_reference["red_iou"], float),
        "suite2p_red_score": np.asarray(fov_reference["legacy_red_score"], float),
        f"{prefix}_responsive_fdr": resp_any,
        f"{prefix}_excited_fdr": excited,
        f"{prefix}_suppressed_fdr": suppressed,
        f"{prefix}_preferred_condition": pref_val,
        f"{prefix}_preferred_response": pref_resp,
        f"{prefix}_lifetime_sparseness": sparse,
        f"{prefix}_gini_coefficient": gini,
        f"{prefix}_fano_factor": fano,
    })
    for j, val in enumerate(values):
        df[condition_column_name(block, val)] = curve[:, j]
        df[condition_q_column_name(block, val)] = qmat[:, j]

    if block == "pure_tones":
        df["pure_best_frequency_hz"] = pref_val
        df["pure_fwhm_octaves"] = fwhm_log2_rows(curve, values)
    elif block == "chord_tones":
        f0 = float(extras["F0_hz"])
        df["chord_best_middle_octave"] = pref_val
        df["chord_best_middle_frequency_hz"] = f0 * np.power(2.0, pref_val)
        df["chord_best_middle_distance_from_harmonic_octave"] = np.abs(pref_val - 1.0)
        if np.any(np.isclose(values, 1.0)):
            hj = int(np.argmin(np.abs(values - 1.0)))
            rh = curve[:, hj]
            other = np.nanmean(np.delete(curve, hj, axis=1), axis=1) if len(values) > 1 else np.full(len(df), np.nan)
            df["chord_harmonic_response"] = rh
            df["chord_nonharmonic_mean_response"] = other
            df["chord_harmonic_selectivity"] = bounded_selectivity(rh, other)
        else:
            df["chord_harmonic_response"] = np.nan
            df["chord_nonharmonic_mean_response"] = np.nan
            df["chord_harmonic_selectivity"] = np.nan
    else:
        df["fm_best_slope_oct_per_s"] = pref_val
        df["fm_best_abs_slope_oct_per_s"] = np.abs(pref_val)
        pos = values > 0; neg = values < 0
        rup = np.nanmean(curve[:, pos], axis=1) if np.any(pos) else np.full(len(df), np.nan)
        rdn = np.nanmean(curve[:, neg], axis=1) if np.any(neg) else np.full(len(df), np.nan)
        df["fm_upward_mean_response"] = rup
        df["fm_downward_mean_response"] = rdn
        df["fm_direction_selectivity"] = bounded_selectivity(rup, rdn)
        mags = np.sort(np.unique(np.abs(values[np.abs(values) > 0])))
        speedmat = np.full((len(df), len(mags)), np.nan)
        for j, mag in enumerate(mags):
            use = np.isclose(np.abs(values), mag)
            speedmat[:, j] = np.nanmean(curve[:, use], axis=1)
        df["fm_speed_lifetime_sparseness"] = lifetime_sparseness_rows(speedmat)

    # Save compact trial archive for downstream trial-reduction robustness.
    archive = out_dir / f"{subject}_{date}_{session}_p{plane}_{block}_trial_response_archive_v2.npz"
    np.savez_compressed(
        archive,
        schema_version=np.asarray("multistim_v2"), subject=np.asarray(subject), date=np.asarray(date), session=np.asarray(session),
        block_type=np.asarray(block), fov_number=np.asarray(int(meta["fov_number"])),
        suite2p_roi_index=roi_idx.astype(int), cell_class=np.asarray(fov_reference["cell_class"]).astype("U8"),
        trial_condition_value=np.asarray(cond_trial, float), valid_trial_mask=np.asarray(valid, bool),
        trial_response=np.asarray(tr, np.float32), condition_values=np.asarray(values, float),
        tvec=np.asarray(tvec_arr,np.float32), condition_trace_mean=np.asarray(trace_mean,np.float32), condition_trace_sem=np.asarray(trace_sem,np.float32),
        condition_mean_response=np.asarray(curve, np.float32), condition_p_values=np.asarray(pmat, np.float32),
        condition_q_values=np.asarray(qmat, np.float32), condition_responsive_fdr=np.asarray(sigmat, bool),
        any_condition_responsive_fdr=np.asarray(resp_any, bool),
    )
    df[f"{prefix}_trial_archive_path"] = str(archive)

    # Per-FOV block figures: class profiles + raster.
    if block == "pure_tones":
        xplot = np.log2(values / 1000.0); xlabel = "Frequency (kHz; log2 spacing)"
    elif block == "fm_tones":
        xplot = _fm_log_positions(values); xlabel = "FM slope (octaves/s; signed log2-magnitude spacing)"
    else:
        xplot = values; xlabel = "Middle tone position (octaves above F0)"
    xticklabels = [f"{v/1000:g}" for v in values] if block == "pure_tones" else [f"{v:g}" for v in values]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for cls in CELL_CLASSES:
        m = np.asarray(fov_reference["cell_class"]) == cls
        if not np.any(m): continue
        mu = np.nanmean(curve[m], axis=0)
        se = stats.sem(curve[m], axis=0, nan_policy="omit")
        ax.plot(xplot, mu, marker="o", label=f"{cls.upper()} (n={m.sum()})", color=CLASS_COLORS[cls])
        ax.fill_between(xplot, mu-se, mu+se, alpha=.18, color=CLASS_COLORS[cls])
    ax.axhline(0, color="0.5", ls="--", lw=1); ax.set_xlabel(xlabel); ax.set_ylabel("Evoked response (dF/F, 0-1 s minus baseline)")
    _readable_condition_ticks(ax,xplot,xticklabels)
    ax.set_title(f"{BLOCK_LABEL[block]} — shared FOV responses"); ax.legend(frameon=False); fig.tight_layout()
    fig.savefig(out_dir / f"{block}_GREEN_YELLOW_tuning_profile.png", dpi=250); plt.close(fig)

    order = np.argsort(np.nan_to_num(pref_val, nan=np.inf))
    im = curve[order]
    fig, ax = plt.subplots(figsize=(9, max(4.5, min(12, len(df)/70))))
    vmax = np.nanpercentile(np.abs(im), 98) if np.any(np.isfinite(im)) else 1
    ax.imshow(im, aspect="auto", interpolation="nearest", cmap="coolwarm", vmin=-vmax, vmax=vmax)
    _readable_condition_ticks(ax,np.arange(len(values)),xticklabels)
    ax.set_xlabel(xlabel); ax.set_ylabel("Cells sorted by preferred condition"); ax.set_title(f"{BLOCK_LABEL[block]} response raster")
    fig.tight_layout(); fig.savefig(out_dir / f"{block}_response_raster.png", dpi=250); plt.close(fig)

    _save_tuning_pages(block,values,curve,pref_val,pref_resp,resp_any,roi_idx,np.asarray(fov_reference["cell_class"]),out_dir)
    if block=="pure_tones": _save_pure_bf_histograms(df,values,out_dir)

    meta_out = {"block_type": block, "condition_values": values, "trial_counts": counts,
                "alignment": align_diag, **extras, "trial_archive": str(archive)}
    return df, meta_out


# =============================================================================
# FOV MERGE / CROSS-SOUND METRICS
# =============================================================================

def merge_fov_blocks(meta_seq: list[dict[str, Any]], plane: int, fov_dir: Path,
                     n_permutations: int, seed: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    meta_seq = sorted(meta_seq, key=lambda x: x["session"])
    ref_meta = meta_seq[0]
    ref_data = twophotonanalysis.TwoPhoton(str(ref_meta["subject"]), str(ref_meta["date"]), str(ref_meta["session"]), plane, paradigm=PARADIGM)
    reference = classify_fov_cells(ref_data, plane, fov_dir)
    base = pd.DataFrame({
        "subject": str(ref_meta["subject"]), "date": str(ref_meta["date"]),
        "FOV#": int(ref_meta["fov_number"]), "fov_uid": ref_meta["fov_uid"],
        "brainArea": str(ref_meta.get("brainArea")), "canonicalArea": str(ref_meta.get("canonicalArea")),
        "depth": float(ref_meta.get("depth", np.nan)), "plane": int(plane),
        "analysis_cell_index": np.arange(len(reference["roi_indices"])),
        "suite2p_roi_index": np.asarray(reference["roi_indices"], int),
        "cell_class": np.asarray(reference["cell_class"]),
        "cellpose_red_iou": np.asarray(reference["red_iou"], float),
        "suite2p_red_score": np.asarray(reference["legacy_red_score"], float),
    })
    block_meta = {}
    sessions_by_block = {}
    for k, meta in enumerate(meta_seq):
        block = meta["block_type"]; sessions_by_block[block] = meta["session"]
        bdf, bout = analyze_block(meta, plane, reference, fov_dir, n_permutations, seed + 1009*k)
        keep = [c for c in bdf.columns if c not in {"analysis_cell_index","suite2p_roi_index","cell_class","cellpose_red_iou","suite2p_red_score"}]
        base = base.merge(bdf[["suite2p_roi_index"] + keep], on="suite2p_roi_index", how="left", validate="one_to_one")
        block_meta[block] = bout

    # Cross-sound cell-level metrics are only defined where both blocks exist.
    if "pure_tones" in block_meta and "chord_tones" in block_meta:
        if "pure_best_frequency_hz" in base and "chord_best_middle_frequency_hz" in base:
            base["pure_vs_chord_best_frequency_log2_difference"] = np.log2(base["chord_best_middle_frequency_hz"] / base["pure_best_frequency_hz"])
    if "pure_tones" in block_meta and "fm_tones" in block_meta:
        if "pure_lifetime_sparseness" in base and "fm_direction_selectivity" in base:
            base["pure_sparseness_x_fm_direction_selectivity"] = base["pure_lifetime_sparseness"] * base["fm_direction_selectivity"]

    resp_cols = [f"{BLOCK_SHORT[b]}_responsive_fdr" for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_responsive_fdr" in base]
    if resp_cols:
        base["n_sound_blocks_responsive"] = base[resp_cols].fillna(False).astype(bool).sum(axis=1)
        base["responsive_to_all_available_blocks"] = base[resp_cols].fillna(False).astype(bool).all(axis=1)

    base["available_blocks"] = "+".join([b for b in BLOCK_ORDER if b in block_meta])
    base["grouping_source"] = ";".join(sorted({str(m.get("fov_grouping_source")) for m in meta_seq}))
    base.to_csv(fov_dir / "fov_cell_results.csv", index=False)

    # Responsiveness overlap and cross-sound scatter figures.
    if resp_cols:
        labels = [c.replace("_responsive_fdr", "") for c in resp_cols]
        mat = np.zeros((len(resp_cols), len(resp_cols)))
        for i, a in enumerate(resp_cols):
            for j, b in enumerate(resp_cols):
                den = np.sum(base[a].fillna(False).astype(bool))
                mat[i,j] = np.sum(base[a].fillna(False).astype(bool) & base[b].fillna(False).astype(bool)) / den if den else np.nan
        fig, ax = plt.subplots(figsize=(5.5, 4.8)); im=ax.imshow(mat, vmin=0, vmax=1, cmap="viridis")
        ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=30); ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
        for i in range(len(labels)):
            for j in range(len(labels)):
                ax.text(j,i,f"{mat[i,j]:.2f}" if np.isfinite(mat[i,j]) else "NA",ha="center",va="center",color="white" if np.isfinite(mat[i,j]) and mat[i,j]>.45 else "black")
        ax.set_title("P(responsive to column block | responsive to row block)"); fig.colorbar(im, ax=ax, label="Conditional fraction"); fig.tight_layout()
        fig.savefig(fov_dir / "cross_sound_responsiveness_overlap.png", dpi=250); plt.close(fig)

    def scatter_pair(xcol, ycol, xlabel, ylabel, fname, mask_extra=None):
        if xcol not in base or ycol not in base: return
        fig, ax = plt.subplots(figsize=(6.5,5.5))
        for cls in CELL_CLASSES:
            m = (base.cell_class==cls) & np.isfinite(base[xcol]) & np.isfinite(base[ycol])
            if mask_extra is not None: m &= mask_extra(base)
            ax.scatter(base.loc[m,xcol], base.loc[m,ycol], s=18, alpha=.6, label=f"{cls.upper()} n={m.sum()}", color=CLASS_COLORS[cls])
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.legend(frameon=False); ax.set_title("Same cells across sound blocks"); fig.tight_layout()
        fig.savefig(fov_dir/fname,dpi=250); plt.close(fig)
    scatter_pair("pure_best_frequency_hz","chord_best_middle_frequency_hz","Pure-tone BF (Hz)","Preferred chord middle frequency (Hz)","same_cell_pure_BF_vs_chord_middle_frequency.png")
    scatter_pair("pure_best_frequency_hz","fm_direction_selectivity","Pure-tone BF (Hz)","FM direction selectivity (up - down)","same_cell_pure_BF_vs_FM_direction_selectivity.png")
    scatter_pair("chord_harmonic_selectivity","fm_direction_selectivity","Chord harmonic selectivity","FM direction selectivity","same_cell_chord_vs_FM_selectivity.png")
    _save_cell_reports(base,block_meta,fov_dir)

    summary = {"fov_uid": ref_meta["fov_uid"], "FOV#": int(ref_meta["fov_number"]),
               "date": ref_meta["date"], "sessions_by_block": sessions_by_block,
               "available_blocks": list(block_meta), "n_cells": len(base),
               "n_green": int(np.sum(base.cell_class==GREEN)), "n_yellow": int(np.sum(base.cell_class==YELLOW)),
               "suite2p_reference_dir": reference["suite2p_dir"], "block_metadata": block_meta}
    save_json(fov_dir / "fov_manifest.json", summary)
    return base, summary


# =============================================================================
# COMBINED AREA SUMMARIES
# =============================================================================

def fov_class_summary(cells: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_cols = ["subject","date","FOV#","fov_uid","brainArea","canonicalArea","depth","cell_class"]
    for keys, g in cells.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys)); row["n_cells"] = len(g)
        for b in BLOCK_ORDER:
            p = BLOCK_SHORT[b]; rc=f"{p}_responsive_fdr"
            if rc in g:
                valid = g[rc].notna(); row[f"{p}_n_measured"] = int(valid.sum())
                row[f"{p}_percent_responsive"] = 100*np.nanmean(g.loc[valid,rc].astype(float)) if valid.any() else np.nan
            for metric in [f"{p}_lifetime_sparseness",f"{p}_gini_coefficient",f"{p}_fano_factor"]:
                if metric in g: row[f"mean_{metric}"] = float(np.nanmean(g[metric])) if np.any(np.isfinite(g[metric])) else np.nan
        for metric in ["pure_best_frequency_hz","pure_fwhm_octaves","chord_best_middle_octave","chord_harmonic_selectivity",
                       "fm_best_slope_oct_per_s","fm_best_abs_slope_oct_per_s","fm_direction_selectivity","fm_speed_lifetime_sparseness"]:
            if metric in g: row[f"mean_{metric}"] = float(np.nanmean(g[metric])) if np.any(np.isfinite(g[metric])) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def plot_combined_responsiveness(summary: pd.DataFrame, out_dir: Path) -> dict[str, Any]:
    stats_out = {}; metrics = [(b, f"{BLOCK_SHORT[b]}_percent_responsive") for b in BLOCK_ORDER]
    fig, axes = plt.subplots(1,3,figsize=(15,5),squeeze=False)
    pvals=[]; recs=[]
    for ax,(b,col) in zip(axes[0],metrics):
        if col not in summary or not np.any(np.isfinite(summary[col])):
            ax.axis("off"); continue
        piv = summary.pivot_table(index="fov_uid",columns="cell_class",values=col,aggfunc="mean")
        for _,r in piv.iterrows():
            if GREEN in r and YELLOW in r and np.isfinite(r[GREEN]) and np.isfinite(r[YELLOW]):
                ax.plot([0,1],[r[GREEN],r[YELLOW]],color="0.75",lw=1,zorder=1)
        for x,cls in enumerate(CELL_CLASSES):
            vals = piv[cls].dropna().to_numpy(float) if cls in piv else np.array([])
            ax.scatter(np.full(len(vals),x),vals,s=32,color=CLASS_COLORS[cls],zorder=2)
            mu,se,n=mean_sem(vals); ax.errorbar(x,mu,yerr=se,fmt="o",color="black",capsize=4,zorder=3)
        rec=safe_wilcoxon_pairs(piv.reset_index(),GREEN,YELLOW) if GREEN in piv and YELLOW in piv else {"n_pairs":0,"W":np.nan,"p":np.nan}
        pvals.append(rec["p"]); recs.append((ax,b,rec)); ax.set_xticks([0,1]); ax.set_xticklabels(["GREEN","YELLOW"]); ax.set_ylim(0,100)
        ax.set_ylabel("Responsive cells (%)"); ax.set_title(BLOCK_LABEL[b])
    adj=holm_adjust(pvals)
    for (ax,b,rec),ph in zip(recs,adj):
        rec["p_holm_3_blocks"] = float(ph) if np.isfinite(ph) else np.nan; stats_out[b]=rec
        ax.text(.02,.98,f"paired FOV Wilcoxon\nW={rec['W']:.3g}, p={rec['p']:.3g}\nHolm(3) p={ph:.3g}\nn={rec['n_pairs']} FOV pairs",transform=ax.transAxes,ha="left",va="top",fontsize=8)
    fig.suptitle("Sound responsiveness: GREEN vs YELLOW; FOV is replicate"); fig.tight_layout(rect=[0,0,1,.94])
    fig.savefig(out_dir/"responsive_fraction_GREEN_vs_YELLOW_FOV_POINTS.png",dpi=250); plt.close(fig)
    return stats_out


def _profile_columns(cells: pd.DataFrame, block: str) -> list[tuple[float,str]]:
    pat = {
        "pure_tones": re.compile(r"^pure_response_([0-9.eE+-]+)_Hz$"),
        "chord_tones": re.compile(r"^chord_response_middle_oct_([0-9.eE+-]+)$"),
        "fm_tones": re.compile(r"^fm_response_slope_(pos|neg)?([0-9.eE+]+)_oct_per_s$"),
    }[block]
    out=[]
    for c in cells.columns:
        m=pat.match(c)
        if not m: continue
        if block=="fm_tones":
            sign=-1 if m.group(1)=="neg" else 1; val=sign*float(m.group(2))
        else: val=float(m.group(1))
        out.append((val,c))
    return sorted(out)


def plot_combined_profiles(cells: pd.DataFrame, out_dir: Path) -> None:
    for block in BLOCK_ORDER:
        cols=_profile_columns(cells,block)
        if not cols: continue
        vals=np.array([v for v,_ in cols])
        if block=="pure_tones": x=np.log2(vals/1000)
        elif block=="fm_tones": x=_fm_log_positions(vals)
        else: x=vals
        fig,axes=plt.subplots(1,2,figsize=(13,5),sharey=True)
        for ax,cls in zip(axes,CELL_CLASSES):
            sub=cells[cells.cell_class==cls]
            # each FOV contributes its mean tuning curve
            curves=[]
            for uid,g in sub.groupby("fov_uid"):
                arr=g[[c for _,c in cols]].to_numpy(float)
                if np.any(np.isfinite(arr)): curves.append(np.nanmean(arr,axis=0))
            if curves:
                M=np.vstack(curves)
                for row in M: ax.plot(x,row,color="0.78",lw=.8,alpha=.8)
                mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy="omit")
                ax.plot(x,mu,marker="o",lw=2.2,color=CLASS_COLORS[cls]); ax.fill_between(x,mu-se,mu+se,color=CLASS_COLORS[cls],alpha=.2)
            ax.axhline(0,color="0.5",ls="--",lw=1); ax.set_title(f"{cls.upper()} — FOV means")
            if block=="pure_tones": _readable_condition_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel("Frequency (kHz; log2 spacing)")
            elif block=="chord_tones": _readable_condition_ticks(ax,x,[f"{v:.3g}" for v in vals]); ax.set_xlabel("Middle tone octave above F0")
            else: _readable_condition_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel("FM slope (octaves/s; signed log2-magnitude spacing)")
        axes[0].set_ylabel("Evoked response (dF/F)"); fig.suptitle(f"{BLOCK_LABEL[block]} — across-FOV profiles"); fig.tight_layout(rect=[0,0,1,.94])
        fig.savefig(out_dir/f"{block}_across_FOV_GREEN_YELLOW_profiles.png",dpi=250); plt.close(fig)


def plot_primary_selectivity_green_yellow(cells: pd.DataFrame, out_dir: Path) -> dict[str, Any]:
    """Dedicated primary selectivity plots: GREEN vs YELLOW with FOV as replicate."""
    root = out_dir / "selectivity_plots"
    root.mkdir(parents=True, exist_ok=True)
    stats_out = {}
    for branch in ("all_cells", "responsive_only"):
        tmp = []
        for block in BLOCK_ORDER:
            spec = SELECTIVITY_SPEC[block]; metric = spec["metric"]
            use = cells
            if branch == "responsive_only":
                rc = f"{BLOCK_SHORT[block]}_responsive_fdr"
                use = cells[cells[rc].fillna(False).astype(bool)].copy() if rc in cells else cells.iloc[0:0].copy()
            if metric not in use:
                continue
            x = use[["fov_uid", "cell_class", metric]].copy()
            x[metric] = pd.to_numeric(x[metric], errors="coerce")
            t = x.groupby(["fov_uid", "cell_class"], as_index=False)[metric].mean().rename(columns={metric:"value"})
            piv = t.pivot(index="fov_uid", columns="cell_class", values="value").reset_index() if len(t) else pd.DataFrame()
            rec = safe_wilcoxon_pairs(piv, GREEN, YELLOW) if len(piv) and GREEN in piv and YELLOW in piv else {"n_pairs":0,"W":np.nan,"p":np.nan}
            tmp.append((block, piv, rec))
        adj = holm_adjust([rec["p"] for _,_,rec in tmp])
        for (block,piv,rec),ph in zip(tmp,adj):
            spec=SELECTIVITY_SPEC[block]; rec["p_holm_3_selectivity_indices"] = float(ph) if np.isfinite(ph) else np.nan
            stats_out.setdefault(branch,{})[block]=rec
            d = root/spec["folder"]; d.mkdir(parents=True,exist_ok=True)
            fig,ax=plt.subplots(figsize=(6.6,5.8))
            if len(piv):
                for _,r in piv.iterrows():
                    if np.isfinite(r.get(GREEN,np.nan)) and np.isfinite(r.get(YELLOW,np.nan)):
                        ax.plot([0,1],[r[GREEN],r[YELLOW]],color="0.78",lw=.9,zorder=1)
                for pos,cls in enumerate(CELL_CLASSES):
                    v=finite(piv[cls]) if cls in piv else np.array([])
                    ax.scatter(np.full(len(v),pos),v,s=34,color=CLASS_COLORS[cls],zorder=2)
                    mu,se,n=mean_sem(v); ax.errorbar(pos,mu,yerr=se,fmt="o",color="black",capsize=4,zorder=3)
            ax.set_xticks([0,1]); ax.set_xticklabels(["GREEN","YELLOW"]); ax.set_ylabel(spec["label"]); ax.set_ylim(*spec["ylim"]); ax.axhline(0,color="0.6",ls="--",lw=.8) if spec["ylim"][0] < 0 else None
            ax.set_title(f"{BLOCK_LABEL[block]} — {branch.replace('_',' ')}\nGREEN vs YELLOW; FOV is replicate")
            ax.text(.98,.98,f"paired FOV Wilcoxon\nW={rec['W']:.3g}, p={rec['p']:.3g}\nHolm(3 indices) p={ph:.3g}\nn={rec['n_pairs']} pairs",transform=ax.transAxes,ha="right",va="top",fontsize=8.5)
            _selectivity_equation_box(ax,block); fig.tight_layout(); fig.savefig(d/f"{branch}_GREEN_vs_YELLOW_FOV_primary_selectivity.png",dpi=250); plt.close(fig)
    save_json(root/"primary_selectivity_statistics.json",stats_out)
    return stats_out


def write_report(path: Path, cells: pd.DataFrame, summary: pd.DataFrame, response_stats: dict[str,Any]) -> None:
    lines=["SOUND_TUNING MULTISTIM FOV ANALYSIS v3","="*72,"",
           "Primary replicate: FOV (same ROI population across sound blocks).",
           "Responsiveness: condition-specific sign-flip tests, BH-FDR across cells separately at each condition; union across conditions.",""]
    lines.append(f"FOVs: {cells['fov_uid'].nunique()} | cells/FOV rows: {len(cells)}")
    for b in BLOCK_ORDER:
        rc=f"{BLOCK_SHORT[b]}_responsive_fdr"
        if rc in cells:
            lines.append(f"{BLOCK_LABEL[b]} measured in {cells.loc[cells[rc].notna(),'fov_uid'].nunique()} FOVs")
    lines += ["","GREEN vs YELLOW responsiveness (paired Wilcoxon across FOVs; Holm across 3 blocks):"]
    for b,r in response_stats.items():
        lines.append(f"  {b}: W={r.get('W',np.nan):.4g}, p={r.get('p',np.nan):.4g}, Holm p={r.get('p_holm_3_blocks',np.nan):.4g}, n={r.get('n_pairs',0)}")
    path.write_text("\n".join(lines)+"\n",encoding="utf-8")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args=parse_args(); subject=str(args.subject); dates=[str(x) for x in args.dates]; area=str(args.area)
    info_path,sessions=load_info2p(subject)
    selected=select_new_sound_sessions(sessions,dates,area)
    if not selected:
        raise RuntimeError(f"No new sound_tuning sessions found for {subject}, area={area}, dates={dates}")
    assigned=assign_fovs(selected,args.fov_groups)
    manifest_rows=validate_fov_groups(assigned)
    od=output_dirs(subject,area,dates)
    manifest=pd.DataFrame(manifest_rows)
    manifest.to_csv(od["root"]/"fov_manifest.csv",index=False)
    print("="*86); print("SOUND_TUNING MULTISTIM FOV ANALYSIS v3"); print("="*86)
    print(f"Subject: {subject} | area: {area} | dates: {dates}")
    print(f"info2p: {info_path}"); print(f"Output: {od['root']}")
    print(manifest[["date","FOV#","session","block_type","brainArea","depth","grouping_source"]].to_string(index=False))
    if any(manifest.grouping_source.str.contains("legacy_inferred",na=False)):
        print("\nWARNING: legacy inferred FOV grouping is provisional. Add FOV# to info2p or use --fov-groups for ambiguous days.")
    save_json(od["root"]/"run_manifest.json",{
        "script_version":"v3","subject":subject,"dates":dates,"area":area,"plane":args.plane,
        "info2p_file":str(info_path),"TEMP_OUTPUT_PATH":str(settings.TEMP_OUTPUT_PATH),
        "FOV_field":"FOV#","FOV_numbering":"starts at 0; unique key = date + FOV#",
        "blocks":list(BLOCK_ORDER),"fm_aliases":["fm_tones","fm_sounds"],
        "primary_replicate":"FOV","responsiveness":"condition-specific sign-flip + per-condition BH-FDR across cells; union",
        "n_permutations":args.n_permutations,"seed":args.seed,
    })
    if args.dry_run:
        print("Dry run complete."); return

    groups: dict[str,list[dict[str,Any]]]={}
    for s in assigned: groups.setdefault(s["fov_uid"],[]).append(s)
    cell_tables=[]; fov_summaries=[]; failures=[]
    for gi,(uid,seq) in enumerate(sorted(groups.items())):
        fd=od["fov"]/uid; fd.mkdir(parents=True,exist_ok=True)
        print("\n"+"-"*86); print(f"FOV {uid}: {[x['session']+':'+x['block_type'] for x in seq]}")
        try:
            df,summ=merge_fov_blocks(seq,args.plane,fd,max(64,int(args.n_permutations)),int(args.seed)+10000*gi)
            cell_tables.append(df); fov_summaries.append(summ)
        except Exception as exc:
            failures.append({"fov_uid":uid,"error":repr(exc),"traceback":traceback.format_exc()})
            print(f"FAILED {uid}: {exc}")
    save_json(od["root"]/"failures.json",failures)
    if not cell_tables:
        raise RuntimeError("No FOV completed successfully; see failures.json")
    cells=pd.concat(cell_tables,ignore_index=True,sort=False)
    cells.to_csv(od["combined"]/"combined_cell_results.csv",index=False)
    fs=fov_class_summary(cells); fs.to_csv(od["combined"]/"combined_fov_summary.csv",index=False)
    response_stats=plot_combined_responsiveness(fs,od["combined"])
    save_json(od["combined"]/"responsiveness_statistics.json",response_stats)
    plot_primary_selectivity_green_yellow(cells,od["combined"])
    plot_combined_profiles(cells,od["combined"])
    _save_combined_bf_outputs(cells,od["combined"])
    write_report(od["combined"]/"REPORT.txt",cells,fs,response_stats)
    print("\n"+"="*86); print("DONE"); print(f"Successful FOVs: {len(cell_tables)}; failed: {len(failures)}"); print(f"Outputs: {od['root']}")


if __name__ == "__main__":
    main()
