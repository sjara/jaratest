#!/usr/bin/env python3
"""
PURE-TONE LEVEL SERIES -- FOV-aware best-frequency analysis across sound levels (v2).

v2 = v1 plus session selection, for days that mix level-series FOVs with other blocks
(e.g. imag041 20261015):
    * --sessions limits the analysis to the listed sessions (001 or 20261015_001, or a
      range 001-004); --exclude-sessions drops sessions.
    * A pure-tone session whose behavior file does not exist (e.g. a failed recording
      that is still in info2p) is skipped with a warning and listed in run_manifest.json,
      instead of stopping the whole run.
The analysis, output columns, and trial archives (schema pure_tone_levels_v1) are the
same as v1, so the posthoc figure scripts read v2 outputs unchanged.

Alternate branch built from sound_tuning_multistim_dualF0_fov_analysis_v1.py (pure-tone
parts only; same helpers, alignment QC, Cellpose GREEN/YELLOW classification, response
scalar, sign-flip tests, and per-condition BH-FDR). Use it for days where each FOV has
several pure_tones sessions recorded at different sound levels, e.g. info2p
sessionLabel 'pure_tones_45dB', 'pure_tones_55dB', ... with the same FOV#.

Each session's level comes from its sessionLabel (pure_tones_<N>dB) and is checked
against the behavior file (tone_intensity / current_intensity) when the session is
analyzed. A plain 'pure_tones' label falls back to the behavior file. An FOV may have
any subset of levels (an FOV with a single level is used in the per-level analyses
and skipped by the paired cross-level comparisons).

Per level (same definitions as the multistim pipeline):
    responsiveness (union of per-frequency FDR tests), BF = argmax of the mean tuning
    curve, FWHM, lifetime sparseness, and last time's BF outputs (per-FOV histograms,
    FOV x BF heatmaps, FOV median BF GREEN/YELLOW, BF across FOVs with KW / pairwise MW /
    subfield tests) in combined/per_level/<N>dB/.

Across levels (combined/best_frequency_across_levels/):
    * BF-eligible cell at level L: FDR-responsive at L, response at its BF > 0, and
      q < 0.05 at the BF itself. Cross-level BF comparisons use BF-eligible cells only.
    * Half-max centroid BF: mean log2 frequency weighted by (response - peak/2), over
      the frequencies at or above half the peak. Less granular than the argmax BF and
      unchanged by a pure gain change.
    * Paired BF shifts for every level pair, log2(BF_high / BF_low) in octaves, for the
      same cell. Per-cell permutation test: within each frequency, trials of the two
      levels are pooled and the level labels shuffled; statistic |delta BF|. BH-FDR
      across cells per pair within each FOV. The centroid version is the per-cell test
      to use: on synthetic data it recovered a 0.9-octave shift in >99% of cells with no
      false positives for unshifted cells tuned away from the range edges. The argmax
      version is very conservative (the shuffled null jitters between the two peaks) and
      is kept for reference. Caveat: when tuning broadens with level, a cell whose BF is
      within ~1.5 octaves of the lowest/highest tested frequency is truncated by the
      range edge, which genuinely moves its centroid; check edge cells before calling
      their shift a BF change.
    * Per-cell BF-vs-level slope (octaves per 10 dB; cells BF-eligible at >= 3 levels).
    * Response threshold (lowest level with a significant excitatory condition) and
      CF (largest significant excitatory frequency at threshold), level-pooled BF.
    * FOV is the replicate for population claims (per-FOV medians; Wilcoxon / Friedman
      across FOVs). With few FOVs the smallest attainable p is large (4 FOVs: two-sided
      Wilcoxon p >= 0.125), so the within-FOV cell-level tests are reported as well,
      labeled as describing that FOV; pooled-cell tests are labeled exploratory.

Example
-------
python sound_tuning_pure_tone_levels_fov_analysis_v2.py imag041 --area A1 --dates 20261008
python sound_tuning_pure_tone_levels_fov_analysis_v2.py imag041 --area A1 --dates 20261015 \
    --sessions 001-004 012-015

Output
------
<TEMP_OUTPUT_PATH>/evan/sound_tuning_pure_tone_levels_fov_analysis/<subject>/<area>/<date_tag>/
    fov_manifest.csv, run_manifest.json, failures.json
    fov_outputs/<date>_FOV###/
        *_pure_tones_<N>dB_trial_response_archive_levels_v1.npz
        <N>dB/  (profile, raster, BF histogram for that level)
        level_tuning_pages/, cell_reports/<class>/, fov_cell_results.csv
    combined/
        combined_cell_results.csv          (wide: pure_<N>dB_* columns + cross-level columns)
        combined_cell_level_results.csv    (long: one row per cell x level)
        per_level/<N>dB/...                (last time's BF outputs, per level)
        best_frequency_across_levels/...   (cross-level BF comparison)
        REPORT.txt
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
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

from jaratoolbox import loadbehavior
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
SCRIPT_VERSION = "levels_v2"
ARCHIVE_SCHEMA = "pure_tone_levels_v1"
OUTPUT_FAMILY = "sound_tuning_pure_tone_levels_fov_analysis"
LABEL_RE = re.compile(r"^pure_tones?(?:_(\d+(?:\.\d+)?)\s*db(?:_?spl)?)?$", re.IGNORECASE)
BEHAVIOR_LEVEL_FIELDS = ("tone_intensity", "current_intensity")

TIME_RANGE = (-1.0, 1.5)
BASELINE_RANGE = (-1.0, 0.0)
RESPONSE_RANGE = (0.0, 1.0)
MIN_FINITE_TRIALS = 3
DEFAULT_PERMUTATIONS = 4096
DEFAULT_SHIFT_PERMUTATIONS = 2000
DEFAULT_SEED = 20261008
BF_Q_ALPHA = 0.05
MIN_LEVELS_FOR_SLOPE = 3
SHIFT_CELL_CHUNK = 256

CELL_PROB_THRESHOLD = 0.0
IOU_THRESHOLD = 0.15
CELLPOSE_CELLPROB_THRESHOLD = -0.5
CELLPOSE_FLOW_THRESHOLD = 0.5
CELLPOSE_DIAMETER = None

GREEN = "green"
YELLOW = "yellow"
CELL_CLASSES = (GREEN, YELLOW)
CELL_GROUPS = ("all", GREEN, YELLOW)   # reduced to ("all",) in main() when no FOV recorded a red channel
CLASS_COLORS = {GREEN: "tab:green", YELLOW: "goldenrod", "all": "0.35"}

# Per-level columns (prefix pure_<N>dB_) shared by the wide and long tables.
LEVEL_MEASURES = (
    "responsive_fdr", "excited_fdr", "suppressed_fdr", "any_excitatory_condition_fdr", "bf_eligible",
    "best_frequency_hz", "bf_centroid_hz", "preferred_response", "q_at_bf", "fwhm_octaves",
    "lifetime_sparseness", "gini_coefficient", "fano_factor", "n_significant_conditions", "trial_archive_path",
)
ID_COLUMNS = ("subject", "date", "FOV#", "fov_uid", "brainArea", "canonicalArea", "depth", "plane",
              "analysis_cell_index", "suite2p_roi_index", "cell_class", "cellpose_red_iou", "suite2p_red_score",
              "red_channel_recorded")


def level_tag(level: float) -> str:
    return f"{float(level):g}dB"


def lp(level: float) -> str:
    """Column prefix for one level, e.g. pure_45dB."""
    return f"pure_{level_tag(level)}"


def cond_col(level: float, freq: float) -> str:
    return f"{lp(level)}_response_{freq:.6g}_Hz"


def cond_q_col(level: float, freq: float) -> str:
    return f"{lp(level)}_response_q_{freq:.6g}_Hz"


def pair_tag(a: float, b: float) -> str:
    """Pair label, higher level first: shifts are log2(BF_b / BF_a) with b > a."""
    return f"{float(b):g}_vs_{float(a):g}dB"


def level_colors(levels: Iterable[float]) -> dict[float, Any]:
    levels = sorted(levels)
    cols = plt.cm.magma(np.linspace(0.18, 0.72, max(len(levels), 2)))
    return {lv: cols[i] for i, lv in enumerate(levels)}


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


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject")
    p.add_argument("--area", required=True, choices=["A1", "AAF", "A2"])
    p.add_argument("--dates", nargs="+", required=True)
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--n-permutations", type=int, default=DEFAULT_PERMUTATIONS,
                   help="sign-flip permutations for responsiveness (per frequency and level)")
    p.add_argument("--n-shift-permutations", type=int, default=DEFAULT_SHIFT_PERMUTATIONS,
                   help="level-label permutations for the per-cell BF-shift test")
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--reference-level", type=float, default=None,
                   help="level that BF shifts are expressed relative to (default: highest level)")
    p.add_argument("--skip-cell-reports", action="store_true", help="skip per-cell report PNGs (slow)")
    p.add_argument("--sessions", nargs="+", default=None, metavar="SESSION",
                   help="analyze only these sessions: 001, 20261015_001, or a range 001-004")
    p.add_argument("--exclude-sessions", nargs="+", default=None, metavar="SESSION",
                   help="drop these sessions (same forms as --sessions)")
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
        return jsonable(x.tolist())
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(jsonable(obj), indent=2), encoding="utf-8")


def output_dirs(subject: str, area: str, dates: list[str]) -> dict[str, Path]:
    tag = "_".join(dates)
    root = Path(settings.TEMP_OUTPUT_PATH) / "evan" / OUTPUT_FAMILY / subject / area / tag
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
    spec = importlib.util.spec_from_file_location(f"_levels_{subject}_info2p", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sessions = getattr(mod, "sessions", None)
    if sessions is None:
        raise AttributeError(f"No sessions list found in {path}")
    return path, [dict(s) for s in sessions]


def parse_label_level(label: Any) -> tuple[bool, float | None]:
    """(is a pure-tone session, level in dB from the label or None)."""
    m = LABEL_RE.match(str(label).strip())
    if not m:
        return False, None
    return True, (float(m.group(1)) if m.group(1) else None)


def read_behavior_level(bdata: Any) -> tuple[float | None, str | None]:
    """Single tone level stored in a behavior file, or (None, None) if no level field exists."""
    for key in BEHAVIOR_LEVEL_FIELDS:
        if key in bdata:
            v = np.asarray(bdata[key], float).ravel()
            v = v[np.isfinite(v)]
            if not len(v):
                continue
            if not np.allclose(v, v[0]):
                raise ValueError(f"Behavior field {key} varies within the session: {np.unique(v)}")
            return float(v[0]), key
    return None, None


def parse_session_filter(tokens: list[str] | None) -> set[tuple[str | None, str]] | None:
    """{(date or None, 3-digit session)} from 001, 20261015_001, or ranges like 001-004."""
    if not tokens:
        return None
    out: set[tuple[str | None, str]] = set()
    for tok in tokens:
        date, _, sess = str(tok).rpartition("_")
        date = date or None
        if "-" in sess:
            a, b = sess.split("-", 1)
            out.update((date, f"{k:03d}") for k in range(int(a), int(b) + 1))
        else:
            out.add((date, f"{int(sess):03d}"))
    return out


def _in_filter(filt: set[tuple[str | None, str]], date: str, session: str) -> bool:
    return (date, session) in filt or (None, session) in filt


def select_level_sessions(sessions: list[dict[str, Any]], dates: list[str], area: str,
                          subject: str, include: set | None = None, exclude: set | None = None,
                          skipped: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    dset = set(map(str, dates))
    out = []
    for s in sessions:
        is_pure, level = parse_label_level(s.get("sessionLabel", ""))
        if not (is_pure and str(s.get("date", "")) in dset and str(s.get("paradigm", "")) == PARADIGM
                and canonical_area(s.get("brainArea", "")) == area):
            continue
        q = dict(s)
        q["canonicalArea"] = area
        q["date"] = str(q.get("date", ""))
        q["session"] = str(q.get("session", "")).zfill(3)
        if include is not None and not _in_filter(include, q["date"], q["session"]):
            continue
        if exclude is not None and _in_filter(exclude, q["date"], q["session"]):
            continue
        bpath = loadbehavior.path_to_behavior_data(subject, PARADIGM, f"{q['date']}_{q['session']}")
        if not Path(bpath).exists():
            print(f"WARNING: skipping {q['date']}_{q['session']} ({s.get('sessionLabel')}): no behavior file {bpath}")
            if skipped is not None:
                skipped.append({"date": q["date"], "session": q["session"], "sessionLabel": s.get("sessionLabel"),
                                "reason": f"behavior file not found: {bpath}"})
            continue
        if level is None:
            path = loadbehavior.path_to_behavior_data(subject, PARADIGM, f"{q['date']}_{q['session']}")
            level, _ = read_behavior_level(loadbehavior.BehaviorData(path))
            if level is None:
                raise ValueError(f"Session {q['date']}_{q['session']}: no level in sessionLabel "
                                 f"{s.get('sessionLabel')!r} or behavior file")
            q["level_source"] = "behavior"
        else:
            q["level_source"] = "sessionLabel"
        q["level_db"] = float(level)
        out.append(q)
    out.sort(key=lambda x: (x["date"], x["session"]))
    return out


def assign_fovs(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [(s["date"], s["session"]) for s in selected if s.get("FOV#") is None]
    if missing:
        raise ValueError(f"These sessions have no FOV# in info2p (required for level series): {missing}")
    out = [dict(s) for s in selected]
    for s in out:
        s["fov_number"] = int(s["FOV#"])
        s["fov_uid"] = f"{s['date']}_FOV{s['fov_number']:03d}"
    return out


def validate_fov_groups(assigned: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for s in assigned:
        groups.setdefault(s["fov_uid"], []).append(s)
    rows = []
    for uid, seq in groups.items():
        seq.sort(key=lambda x: x["session"])
        areas = {str(s.get("brainArea")) for s in seq}
        if len(areas) > 1:
            raise ValueError(f"FOV {uid} contains multiple brainArea values: {areas}")
        levels = [s["level_db"] for s in seq]
        if len(levels) != len(set(levels)):
            raise ValueError(f"FOV {uid} has two sessions at the same level: "
                             f"{[(s['session'], s['level_db']) for s in seq]}")
        depth_warning = len({str(s.get("depth")) for s in seq}) > 1
        for s in seq:
            rows.append({
                "subject": s.get("subject"), "date": s["date"], "FOV#": int(s["fov_number"]),
                "fov_uid": uid, "session": s["session"], "level_db": s["level_db"],
                "level_source": s["level_source"], "sessionLabel": s.get("sessionLabel"),
                "brainArea": s.get("brainArea"), "canonicalArea": s.get("canonicalArea"),
                "depth": s.get("depth"), "fps": s.get("fps"), "nFrames": s.get("nFrames"),
                "n_levels_in_FOV": len(seq), "depth_mismatch_within_FOV": depth_warning,
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


def argmax_log2(curves: np.ndarray, x: np.ndarray) -> np.ndarray:
    """log2 frequency of the peak along the last axis; NaN where the curve is all NaN."""
    c = np.where(np.isfinite(curves), curves, -np.inf)
    out = np.asarray(x, float)[np.argmax(c, axis=-1)]
    return np.where(np.isfinite(c).any(axis=-1), out, np.nan)


def halfmax_centroid_log2(curves: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Centroid of log2 frequency weighted by (response - peak/2) over above-half-max points.

    Works along the last axis. NaN when the peak is <= 0 or the curve is all NaN.
    Scale invariant, so a pure gain change between levels leaves it unchanged.
    """
    c = np.asarray(curves, float)
    peak = np.max(np.where(np.isfinite(c), c, -np.inf), axis=-1, keepdims=True)
    w = np.clip(np.nan_to_num(c - peak / 2.0, nan=0.0, neginf=0.0, posinf=0.0), 0.0, None)
    s = w.sum(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = (w * np.asarray(x, float)).sum(axis=-1) / s
    return np.where((peak[..., 0] > 0) & (s > 0), out, np.nan)


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


def wilcoxon_vs_zero(d: Iterable[Any]) -> dict[str, Any]:
    d = finite(d)
    rec = {"n": int(len(d)), "median": float(np.median(d)) if len(d) else np.nan, "W": np.nan, "p": np.nan}
    if len(d) < 2:
        return rec
    if np.allclose(d, 0):
        rec.update(W=0.0, p=1.0); return rec
    try:
        r = stats.wilcoxon(d, alternative="two-sided", zero_method="wilcox")
        rec.update(W=float(r.statistic), p=float(r.pvalue))
    except ValueError:
        pass
    return rec


def friedman_across_levels(piv: pd.DataFrame) -> dict[str, Any]:
    """Friedman test over the columns (levels) of a replicate x level table; complete rows only."""
    sub = piv.dropna()
    rec = {"n_replicates": int(len(sub)), "n_levels": int(sub.shape[1]), "chi2": np.nan, "p": np.nan}
    if sub.shape[1] < 3 or len(sub) < 2:
        return rec
    try:
        r = stats.friedmanchisquare(*[sub[c].to_numpy(float) for c in sub.columns])
        rec.update(chi2=float(r.statistic), p=float(r.pvalue))
    except ValueError:
        pass
    return rec


def _mw_simple(x, y) -> dict[str, Any]:
    x = finite(x); y = finite(y)
    if not len(x) or not len(y):
        return {"U": np.nan, "p": np.nan, "n1": len(x), "n2": len(y)}
    r = stats.mannwhitneyu(x, y, alternative="two-sided")
    return {"U": float(r.statistic), "p": float(r.pvalue), "n1": len(x), "n2": len(y)}


def _fmt(v: Any, spec: str = ".3g") -> str:
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "NA"
    return format(v, spec) if np.isfinite(v) else "NA"


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
    if ops.get("meanImg_chan2") is None and ops.get("meanImg_chan2_corrected") is None and int(ops.get("nchannels", 1)) == 1:
        # Single-channel recording (no PMT1/tdTomato): no overlap classification is possible.
        # Every functional ROI is labeled GREEN and red_channel_recorded is False.
        print(f"  No red channel in {sdir} (nchannels=1): all {len(roi_idx)} cells labeled GREEN, Cellpose skipped")
        return {"roi_indices": roi_idx, "cell_mask": cell_mask, "cell_class": np.full(len(roi_idx), GREEN),
                "red_iou": np.full(len(roi_idx), np.nan), "legacy_red_score": np.full(len(roi_idx), np.nan),
                "stat_signature": roi_signature(stat_array, roi_idx), "suite2p_dir": str(sdir),
                "cellpose_diameter": np.nan, "red_channel_recorded": False}
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
            "suite2p_dir": str(sdir), "cellpose_diameter": diameter, "red_channel_recorded": True}


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


# =============================================================================
# PLOT HELPERS
# =============================================================================

def _readable_condition_ticks(ax, x, labels, dense_threshold=10):
    """Readable condition labels: dense axes label every other tick, rotated ~60 deg."""
    x = np.asarray(x, float); labels = list(labels)
    ax.set_xticks(x)
    if len(labels) >= dense_threshold:
        shown = [lab if (i % 2 == 0) else "" for i, lab in enumerate(labels)]
        ax.set_xticklabels(shown, rotation=60, ha="right", rotation_mode="anchor")
    else:
        ax.set_xticklabels(labels, rotation=45 if len(labels) > 6 else 0, ha="right" if len(labels) > 6 else "center")


def _khz_axis(ax, freqs_hz, axis="x"):
    x = np.log2(np.asarray(freqs_hz, float) / 1000.0)
    labels = [f"{v/1000:.3g}" for v in freqs_hz]
    if axis == "x":
        _readable_condition_ticks(ax, x, labels)
    else:
        ax.set_yticks(x[::2]); ax.set_yticklabels(labels[::2])


def _bf_text(row: pd.Series, levels: list[float]) -> str:
    bits = []
    for lv in levels:
        bf = pd.to_numeric(pd.Series([row.get(f"{lp(lv)}_best_frequency_hz", np.nan)]), errors="coerce").iloc[0]
        ok = bool(row.get(f"{lp(lv)}_bf_eligible", False)) if pd.notna(row.get(f"{lp(lv)}_bf_eligible", np.nan)) else False
        bits.append(f"{lv:g}:{bf/1000:.3g}" if ok and np.isfinite(bf) else f"{lv:g}:-")
    return "BF kHz " + " ".join(bits)


# =============================================================================
# PER-LEVEL ANALYSIS
# =============================================================================

def _trial_response(eventlocked: np.ndarray, tvec: np.ndarray) -> np.ndarray:
    b = (tvec >= BASELINE_RANGE[0]) & (tvec < BASELINE_RANGE[1])
    r = (tvec >= RESPONSE_RANGE[0]) & (tvec < RESPONSE_RANGE[1])
    return np.nanmean(eventlocked[:, :, r], axis=2) - np.nanmean(eventlocked[:, :, b], axis=2)


def _check_behavior_is_pure_tone_at_level(bdata: Any, level: float, tag: str) -> dict[str, Any]:
    info: dict[str, Any] = {}
    if "current_stim_type" in bdata:
        code = getattr(bdata, "labels", {}).get("current_stim_type", {}).get("Pure_tone")
        if code is not None:
            st = np.asarray(bdata["current_stim_type"]).ravel()
            n_other = int(np.sum(st != code))
            if n_other:
                raise ValueError(f"{tag}: {n_other} trials are not pure tones; this script expects pure-tone-only sessions")
            info["stim_type_checked"] = True
    blevel, field = read_behavior_level(bdata)
    if blevel is not None and not np.isclose(blevel, level):
        raise ValueError(f"{tag}: behavior {field} = {blevel:g} dB but the session is assigned {level:g} dB")
    info["behavior_level_db"] = blevel; info["behavior_level_field"] = field
    return info


def _save_level_bf_histogram(df: pd.DataFrame, level: float, values: np.ndarray, out_dir: Path) -> None:
    """Per-FOV BF histogram at one level (pure-tone FDR-responsive cells), as in the multistim pipeline."""
    p = lp(level)
    use = df[df[f"{p}_responsive_fdr"].astype(bool) & np.isfinite(df[f"{p}_best_frequency_hz"])]
    if use.empty:
        return
    vals = np.asarray(values, float); x = np.log2(vals / 1000.0); width = np.min(np.diff(x)) * .8 if len(x) > 1 else .7
    fig, axes = plt.subplots(2, 1, figsize=(11, 9), sharex=True)
    for cls in CELL_CLASSES:
        arr = use.loc[use.cell_class == cls, f"{p}_best_frequency_hz"].to_numpy(float)
        counts = np.array([np.sum(np.isclose(arr, v)) for v in vals], float)
        frac = counts / counts.sum() if counts.sum() > 0 else np.full_like(counts, np.nan)
        offset = -.2 * width if cls == GREEN else .2 * width
        axes[0].bar(x + offset, counts, width=.38 * width, label=f"{cls.upper()} n={len(arr)}", alpha=.75, color=CLASS_COLORS[cls])
        axes[1].plot(x, frac, marker="o", lw=2, label=f"{cls.upper()} n={len(arr)}", color=CLASS_COLORS[cls])
    axes[0].set_ylabel("Responsive cells (count)"); axes[1].set_ylabel("Fraction of responsive cells")
    axes[1].set_xlabel("Best frequency (kHz; log2 spacing)")
    _readable_condition_ticks(axes[1], x, [f"{v/1000:.3g}" for v in vals]); axes[0].legend(frameon=False); axes[1].legend(frameon=False)
    fig.suptitle(f"Best-frequency distribution at {level:g} dB — pure-tone FDR-responsive cells")
    fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(out_dir / "best_frequency_histogram_counts_and_fraction.png", dpi=250); plt.close(fig)


def analyze_level(meta: dict[str, Any], plane: int, fov_reference: dict[str, Any], fov_dir: Path,
                  n_permutations: int, seed: int) -> tuple[pd.DataFrame, dict[str, Any], dict[str, np.ndarray]]:
    subject, date, session = str(meta["subject"]), str(meta["date"]), str(meta["session"])
    level = float(meta["level_db"]); p = lp(level); tag = f"{date}_{session} ({level:g} dB)"
    out_dir = fov_dir / level_tag(level); out_dir.mkdir(parents=True, exist_ok=True)
    data2p = twophotonanalysis.TwoPhoton(subject, date, session, plane, paradigm=PARADIGM)
    verify_shared_rois(data2p, fov_reference)
    roi_idx = np.asarray(fov_reference["roi_indices"], int)
    classes = np.asarray(fov_reference["cell_class"])

    ev_all, tvec, valid = data2p.event_locked_average(time_range=list(TIME_RANGE), dff=True)
    ev = np.asarray(ev_all[roi_idx], float)
    bdata = data2p.bdata
    missing = [k for k in ("stim_duration", "ISI", "current_tone_freq") if k not in bdata]
    if missing:
        raise KeyError(f"{tag}: missing behavior fields {missing}")
    beh_info = _check_behavior_is_pure_tone_at_level(bdata, level, tag)
    cond_trial = np.asarray(bdata["current_tone_freq"], float)
    ntr = len(cond_trial)
    ev, valid, event_onset, align_diag = align_imaging_events_to_behavior(
        ev, valid, np.asarray(data2p.event_onset), float(data2p.srate),
        np.asarray(bdata["stim_duration"], float), np.asarray(bdata["ISI"], float), ntr)
    tvec_arr = np.asarray(tvec, float)
    bmask = (tvec_arr >= BASELINE_RANGE[0]) & (tvec_arr < BASELINE_RANGE[1])
    ev_bc = ev - np.nanmean(ev[:, :, bmask], axis=2)[:, :, None]
    tr = _trial_response(ev, tvec_arr)
    tr[:, ~np.asarray(valid, bool)] = np.nan

    values = np.sort(np.unique(cond_trial[np.isfinite(cond_trial)]))
    ncell, nval = len(roi_idx), len(values)
    curve = np.full((ncell, nval), np.nan)
    pmat = np.full_like(curve, np.nan); qmat = np.full_like(curve, np.nan); sigmat = np.zeros_like(curve, bool)
    trace_mean = np.full((ncell, nval, ev_bc.shape[2]), np.nan, dtype=float)
    trace_sem = np.full_like(trace_mean, np.nan)
    rng = np.random.default_rng(seed)
    counts = []
    for j, val in enumerate(values):
        tm = np.asarray(valid, bool) & np.isclose(cond_trial, val, rtol=1e-8, atol=1e-10)
        counts.append(int(tm.sum()))
        curve[:, j] = np.nanmean(tr[:, tm], axis=1)
        if np.any(tm):
            trace_mean[:, j, :] = np.nanmean(ev_bc[:, tm, :], axis=1)
            trace_sem[:, j, :] = stats.sem(ev_bc[:, tm, :], axis=1, nan_policy="omit") if int(tm.sum()) > 1 else np.nan
        tested = np.sum(np.isfinite(tr[:, tm]), axis=1) >= MIN_FINITE_TRIALS
        pv = signflip_pvalues_grouped(tr[:, tm], tested, n_permutations, rng)
        q = bh_fdr(pv, tested)
        pmat[:, j] = pv; qmat[:, j] = q; sigmat[:, j] = np.isfinite(q) & (q < 0.05)

    resp_any = np.any(sigmat, axis=1)
    excitatory_any = np.any(sigmat & (curve > 0), axis=1)
    # Sign based on the largest-absolute significant condition response.
    excited = np.zeros(ncell, bool); suppressed = np.zeros(ncell, bool)
    for i in range(ncell):
        jj = np.flatnonzero(sigmat[i])
        if not len(jj): continue
        bestj = jj[np.nanargmax(np.abs(curve[i, jj]))]
        excited[i] = curve[i, bestj] > 0; suppressed[i] = curve[i, bestj] < 0

    pref_idx = np.full(ncell, -1, int)
    for i, row in enumerate(curve):
        if np.any(np.isfinite(row)):
            pref_idx[i] = int(np.nanargmax(row))
    has = pref_idx >= 0
    bf = np.where(has, values[np.clip(pref_idx, 0, None)], np.nan)
    pref_resp = np.where(has, curve[np.arange(ncell), np.clip(pref_idx, 0, None)], np.nan)
    q_at_bf = np.where(has, qmat[np.arange(ncell), np.clip(pref_idx, 0, None)], np.nan)
    bf_eligible = resp_any & (pref_resp > 0) & (q_at_bf < BF_Q_ALPHA)
    centroid = 2.0 ** halfmax_centroid_log2(curve, np.log2(values))

    df = pd.DataFrame({
        "suite2p_roi_index": roi_idx,
        f"{p}_session": session,
        f"{p}_responsive_fdr": resp_any,
        f"{p}_excited_fdr": excited,
        f"{p}_suppressed_fdr": suppressed,
        f"{p}_any_excitatory_condition_fdr": excitatory_any,
        f"{p}_bf_eligible": bf_eligible,
        f"{p}_best_frequency_hz": bf,
        f"{p}_bf_centroid_hz": centroid,
        f"{p}_preferred_response": pref_resp,
        f"{p}_q_at_bf": q_at_bf,
        f"{p}_fwhm_octaves": fwhm_log2_rows(curve, values),
        f"{p}_lifetime_sparseness": lifetime_sparseness_rows(curve),
        f"{p}_gini_coefficient": gini_rows(curve),
        f"{p}_fano_factor": fano_rows(curve),
        f"{p}_n_significant_conditions": sigmat.sum(axis=1),
    })
    for j, val in enumerate(values):
        df[cond_col(level, val)] = curve[:, j]
        df[cond_q_col(level, val)] = qmat[:, j]

    archive = fov_dir / f"{subject}_{date}_{session}_p{plane}_pure_tones_{level_tag(level)}_trial_response_archive_levels_v1.npz"
    arc = dict(
        schema_version=np.asarray(ARCHIVE_SCHEMA), subject=np.asarray(subject), date=np.asarray(date),
        session=np.asarray(session), block_type=np.asarray("pure_tones"), level_db=np.asarray(level),
        fov_number=np.asarray(int(meta["fov_number"])),
        suite2p_roi_index=roi_idx.astype(int), cell_class=classes.astype("U8"),
        trial_condition_value=np.asarray(cond_trial, float), valid_trial_mask=np.asarray(valid, bool),
        trial_response=np.asarray(tr, np.float32), condition_values=np.asarray(values, float),
        tvec=np.asarray(tvec_arr, np.float32), condition_trace_mean=np.asarray(trace_mean, np.float32),
        condition_trace_sem=np.asarray(trace_sem, np.float32),
        condition_mean_response=np.asarray(curve, np.float32), condition_p_values=np.asarray(pmat, np.float32),
        condition_q_values=np.asarray(qmat, np.float32), condition_responsive_fdr=np.asarray(sigmat, bool),
        any_condition_responsive_fdr=np.asarray(resp_any, bool),
    )
    np.savez_compressed(archive, **arc)
    df[f"{p}_trial_archive_path"] = str(archive)

    # Per-level FOV figures: class profiles, raster, BF histogram.
    xplot = np.log2(values / 1000.0); xticklabels = [f"{v/1000:.3g}" for v in values]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for cls in CELL_CLASSES:
        m = classes == cls
        if not np.any(m): continue
        mu = np.nanmean(curve[m], axis=0); se = stats.sem(curve[m], axis=0, nan_policy="omit")
        ax.plot(xplot, mu, marker="o", label=f"{cls.upper()} (n={m.sum()})", color=CLASS_COLORS[cls])
        ax.fill_between(xplot, mu-se, mu+se, alpha=.18, color=CLASS_COLORS[cls])
    ax.axhline(0, color="0.5", ls="--", lw=1); ax.set_xlabel("Frequency (kHz; log2 spacing)")
    ax.set_ylabel("Evoked response (dF/F, 0-1 s minus baseline)"); _readable_condition_ticks(ax, xplot, xticklabels)
    ax.set_title(f"Pure tones {level:g} dB — shared FOV responses"); ax.legend(frameon=False); fig.tight_layout()
    fig.savefig(out_dir / "pure_tones_GREEN_YELLOW_tuning_profile.png", dpi=250); plt.close(fig)

    order = np.argsort(np.nan_to_num(bf, nan=np.inf), kind="stable")
    im = curve[order]
    fig, ax = plt.subplots(figsize=(9, max(4.5, min(12, ncell/70))))
    vmax = np.nanpercentile(np.abs(im), 98) if np.any(np.isfinite(im)) else 1
    ax.imshow(im, aspect="auto", interpolation="nearest", cmap="coolwarm", vmin=-vmax, vmax=vmax)
    _readable_condition_ticks(ax, np.arange(nval), xticklabels)
    ax.set_xlabel("Frequency (kHz)"); ax.set_ylabel("Cells sorted by BF"); ax.set_title(f"Pure tones {level:g} dB response raster")
    fig.tight_layout(); fig.savefig(out_dir / "pure_tones_response_raster.png", dpi=250); plt.close(fig)
    df_cls = df.assign(cell_class=classes)
    _save_level_bf_histogram(df_cls, level, values, out_dir)

    meta_out = {"level_db": level, "session": session, "condition_values": values, "trial_counts": counts,
                "alignment": align_diag, **beh_info, "trial_archive": str(archive)}
    return df, meta_out, arc


# =============================================================================
# CROSS-LEVEL (WITHIN FOV)
# =============================================================================

def _common_frequencies(arcs: dict[float, dict[str, np.ndarray]]) -> np.ndarray:
    levels = sorted(arcs)
    common = np.asarray(arcs[levels[0]]["condition_values"], float)
    for lv in levels[1:]:
        other = np.asarray(arcs[lv]["condition_values"], float)
        common = np.array([f for f in common if np.any(np.isclose(other, f, rtol=1e-6))])
    return common


def _level_curves(arc: dict[str, np.ndarray], freqs: np.ndarray) -> np.ndarray:
    vals = np.asarray(arc["condition_values"], float)
    cols = [int(np.flatnonzero(np.isclose(vals, f, rtol=1e-6))[0]) for f in freqs]
    return np.asarray(arc["condition_mean_response"], float)[:, cols]


def bf_shift_permutation(arc_a: dict[str, np.ndarray], arc_b: dict[str, np.ndarray], freqs: np.ndarray,
                         cells: np.ndarray, n_perm: int, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Per-cell permutation test of a BF difference between two levels of the same cells.

    Within each frequency, the trials of both levels are pooled and the level labels are
    shuffled (keeping each level's trial count). The null distribution of |delta BF| is
    built for the argmax BF and the half-max centroid BF. Returns observed signed shifts
    (log2 BF_b - log2 BF_a, octaves) and permutation p-values, for the requested cells.
    """
    x = np.log2(np.asarray(freqs, float))
    nf = len(freqs); cells = np.asarray(cells, int)
    out = {k: np.full(len(cells), np.nan) for k in ("d_argmax", "d_centroid", "p_argmax", "p_centroid")}
    if not len(cells):
        return out
    per_freq = []
    for f in freqs:
        ma = np.asarray(arc_a["valid_trial_mask"], bool) & np.isclose(np.asarray(arc_a["trial_condition_value"], float), f, rtol=1e-6)
        mb = np.asarray(arc_b["valid_trial_mask"], bool) & np.isclose(np.asarray(arc_b["trial_condition_value"], float), f, rtol=1e-6)
        na, nb = int(ma.sum()), int(mb.sum())
        keys = rng.random((n_perm, na + nb))
        assign_a = (np.argsort(np.argsort(keys, axis=1), axis=1) < na).astype(np.float32)
        per_freq.append((ma, mb, na, assign_a))
    tra = np.asarray(arc_a["trial_response"], np.float32); trb = np.asarray(arc_b["trial_response"], np.float32)
    for start in range(0, len(cells), SHIFT_CELL_CHUNK):
        sl = slice(start, start + SHIFT_CELL_CHUNK); ci = cells[sl]
        null_a = np.full((len(ci), n_perm, nf), np.nan, np.float32); null_b = np.full_like(null_a, np.nan)
        obs_a = np.full((len(ci), nf), np.nan); obs_b = np.full_like(obs_a, np.nan)
        for j, (ma, mb, na, assign_a) in enumerate(per_freq):
            X = np.concatenate([tra[ci][:, ma], trb[ci][:, mb]], axis=1)
            fin = np.isfinite(X).astype(np.float32); X0 = np.nan_to_num(X, nan=0.0)
            with np.errstate(invalid="ignore", divide="ignore"):
                obs_a[:, j] = X0[:, :na].sum(1) / fin[:, :na].sum(1)
                obs_b[:, j] = X0[:, na:].sum(1) / fin[:, na:].sum(1)
                null_a[:, :, j] = (X0 @ assign_a.T) / (fin @ assign_a.T)
                null_b[:, :, j] = (X0 @ (1 - assign_a).T) / (fin @ (1 - assign_a).T)
        d_arg = argmax_log2(obs_b, x) - argmax_log2(obs_a, x)
        d_cen = halfmax_centroid_log2(obs_b, x) - halfmax_centroid_log2(obs_a, x)
        n_arg = np.abs(argmax_log2(null_b, x) - argmax_log2(null_a, x))
        n_cen = np.abs(halfmax_centroid_log2(null_b, x) - halfmax_centroid_log2(null_a, x))
        for key, d, null in (("argmax", d_arg, n_arg), ("centroid", d_cen, n_cen)):
            ok_null = np.isfinite(null)
            ext = np.sum(ok_null & (null >= np.abs(d)[:, None] - 1e-9), axis=1)
            nvalid = ok_null.sum(axis=1)
            with np.errstate(invalid="ignore", divide="ignore"):
                pv = (1 + ext) / (1 + nvalid)
            out[f"d_{key}"][sl] = d
            out[f"p_{key}"][sl] = np.where(np.isfinite(d) & (nvalid > 0), pv, np.nan)
    return out


def cross_level_metrics(base: pd.DataFrame, arcs: dict[float, dict[str, np.ndarray]],
                        n_shift_perm: int, seed: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Cell-level comparisons across the levels recorded in one FOV (same ROIs in every level)."""
    levels = sorted(arcs); n = len(base)
    out = pd.DataFrame(index=base.index)
    elig = {lv: base[f"{lp(lv)}_bf_eligible"].fillna(False).astype(bool).to_numpy() for lv in levels}
    excit = {lv: base[f"{lp(lv)}_any_excitatory_condition_fdr"].fillna(False).astype(bool).to_numpy() for lv in levels}
    resp = {lv: base[f"{lp(lv)}_responsive_fdr"].fillna(False).astype(bool).to_numpy() for lv in levels}
    lbf = {lv: np.log2(base[f"{lp(lv)}_best_frequency_hz"].to_numpy(float)) for lv in levels}
    lcen = {lv: np.log2(base[f"{lp(lv)}_bf_centroid_hz"].to_numpy(float)) for lv in levels}
    out["levels_recorded_db"] = "+".join(f"{lv:g}" for lv in levels)
    out["n_levels_recorded"] = len(levels)
    out["n_levels_responsive"] = np.sum([resp[lv] for lv in levels], axis=0)
    out["n_levels_bf_eligible"] = np.sum([elig[lv] for lv in levels], axis=0)
    out["responsive_any_level"] = out["n_levels_responsive"] > 0
    info: dict[str, Any] = {"levels_db": levels}
    if len(levels) < 2:
        return out, info

    # Threshold and CF: lowest level with a significant excitatory condition.
    freqs = _common_frequencies(arcs)
    info["common_frequencies_hz"] = freqs
    thr = np.full(n, np.nan); cf = np.full(n, np.nan)
    for i in range(n):
        for lv in levels:
            if excit[lv][i]:
                thr[i] = lv
                c = np.asarray(arcs[lv]["condition_mean_response"], float)[i]
                s = np.asarray(arcs[lv]["condition_responsive_fdr"], bool)[i] & (c > 0)
                vals = np.asarray(arcs[lv]["condition_values"], float)
                cf[i] = vals[np.flatnonzero(s)[np.argmax(c[s])]]
                break
    out["threshold_level_db"] = thr
    out["threshold_at_lowest_recorded_level"] = np.isclose(thr, levels[0])
    out["cf_hz"] = cf
    if len(freqs):
        pooled = np.nanmean(np.stack([_level_curves(arcs[lv], freqs) for lv in levels]), axis=0)
        out["pooled_bf_hz"] = 2.0 ** argmax_log2(pooled, np.log2(freqs))

    # BF vs level slope (octaves per 10 dB) for cells BF-eligible at >= MIN_LEVELS_FOR_SLOPE levels.
    lv_arr = np.asarray(levels, float)
    for name, src in (("bf", lbf), ("centroid", lcen)):
        slope = np.full(n, np.nan)
        Y = np.stack([src[lv] for lv in levels], axis=1)
        E = np.stack([elig[lv] for lv in levels], axis=1) & np.isfinite(Y)
        for i in np.flatnonzero(E.sum(1) >= MIN_LEVELS_FOR_SLOPE):
            slope[i] = 10.0 * np.polyfit(lv_arr[E[i]], Y[i, E[i]], 1)[0]
        out[f"{name}_level_slope_oct_per_10dB"] = slope

    # Paired level comparisons with per-cell permutation tests.
    rng = np.random.default_rng(seed)
    info["pairs"] = {}
    for a, b in itertools.combinations(levels, 2):
        t = pair_tag(a, b)
        both = elig[a] & elig[b]
        out[f"bfshift_{t}_oct"] = np.where(both, lbf[b] - lbf[a], np.nan)
        out[f"centroidshift_{t}_oct"] = np.where(both, lcen[b] - lcen[a], np.nan)
        res = bf_shift_permutation(arcs[a], arcs[b], freqs, np.flatnonzero(both), n_shift_perm, rng)
        for key, col in (("argmax", "bfshift"), ("centroid", "centroidshift")):
            pfull = np.full(n, np.nan); pfull[both] = res[f"p_{key}"]
            out[f"{col}_{t}_perm_p"] = pfull
            out[f"{col}_{t}_perm_q"] = bh_fdr(pfull)
        info["pairs"][t] = {"n_cells_bf_eligible_both": int(both.sum())}
    return out, info


# =============================================================================
# PER-FOV FIGURES ACROSS LEVELS
# =============================================================================

def _cell_level_curve(arc, i, freqs):
    vals = np.asarray(arc["condition_values"], float)
    tr = np.asarray(arc["trial_response"], float)[i]
    cond = np.asarray(arc["trial_condition_value"], float); valid = np.asarray(arc["valid_trial_mask"], bool)
    mu, se = [], []
    for f in freqs:
        z = tr[valid & np.isclose(cond, f, rtol=1e-6)]; z = z[np.isfinite(z)]
        mu.append(np.mean(z) if len(z) else np.nan); se.append(stats.sem(z) if len(z) > 1 else np.nan)
    return np.asarray(mu), np.asarray(se)


def save_level_tuning_pages(base: pd.DataFrame, arcs: dict[float, dict[str, np.ndarray]], fov_dir: Path) -> None:
    """3x2 pages of cells responsive at any level; each panel overlays the tuning curve at every level."""
    levels = sorted(arcs); cols = level_colors(levels)
    resp = base["responsive_any_level"].fillna(False).astype(bool) if "responsive_any_level" in base else pd.Series(False, index=base.index)
    sub = base[resp].copy()
    if sub.empty:
        return
    root = fov_dir / "level_tuning_pages"; root.mkdir(parents=True, exist_ok=True)
    sortcol = "pooled_bf_hz" if "pooled_bf_hz" in sub else f"{lp(levels[-1])}_best_frequency_hz"
    sub = sub.sort_values([sortcol, "suite2p_roi_index"], na_position="last")
    for pg, start in enumerate(range(0, len(sub), 6), start=1):
        fig, axes = plt.subplots(3, 2, figsize=(12, 13), squeeze=False)
        for ax in axes.ravel(): ax.axis("off")
        for ax, (_, row) in zip(axes.ravel(), sub.iloc[start:start+6].iterrows()):
            ax.axis("on"); i = int(row["analysis_cell_index"])
            for lv in levels:
                vals = np.asarray(arcs[lv]["condition_values"], float)
                mu = np.asarray(arcs[lv]["condition_mean_response"], float)[i]
                ax.plot(np.log2(vals/1000), mu, marker="o", ms=3.5, lw=1.6, color=cols[lv], label=f"{lv:g} dB")
                if bool(row.get(f"{lp(lv)}_bf_eligible", False)):
                    ax.axvline(np.log2(row[f"{lp(lv)}_best_frequency_hz"]/1000), color=cols[lv], ls=":", lw=1.2)
            ax.axhline(0, color="0.55", ls="--", lw=.8)
            _khz_axis(ax, np.asarray(arcs[levels[-1]]["condition_values"], float))
            ax.set_xlabel("Frequency (kHz; log2 spacing)"); ax.set_ylabel("Mean response (dF/F)")
            ax.set_title(f"ROI {int(row['suite2p_roi_index'])} | {str(row['cell_class']).upper()}\n{_bf_text(row, levels)}", fontsize=10)
            ax.spines[["top", "right"]].set_visible(False)
        axes[0, 0].legend(frameon=False, fontsize=8)
        fig.suptitle(f"Pure-tone tuning across levels — cells responsive at any level — page {pg}\n"
                     "dotted lines = BF at each level where BF-eligible", fontsize=14)
        fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(root / f"page_{pg:03d}.png", dpi=200); plt.close(fig)


def save_level_cell_reports(base: pd.DataFrame, arcs: dict[float, dict[str, np.ndarray]], fov_dir: Path) -> None:
    """One PNG per cell responsive at any level: frequency-level response map, tuning curves, traces at BF."""
    levels = sorted(arcs); cols = level_colors(levels)
    resp = base["responsive_any_level"].fillna(False).astype(bool) if "responsive_any_level" in base else pd.Series(False, index=base.index)
    if not resp.any():
        return
    freqs = _common_frequencies(arcs)
    root = fov_dir / "cell_reports"
    for cls in CELL_CLASSES: (root / cls).mkdir(parents=True, exist_ok=True)
    for _, row in base[resp].iterrows():
        i = int(row["analysis_cell_index"]); roi = int(row["suite2p_roi_index"]); cls = str(row["cell_class"])
        fig, (axm, axc, axt) = plt.subplots(1, 3, figsize=(19, 5.6), gridspec_kw={"width_ratios": [1.1, 1.2, 1.0]})
        if len(freqs):
            M = np.stack([_level_curves(arcs[lv], freqs)[i] for lv in levels])
            vmax = np.nanmax(np.abs(M)) if np.any(np.isfinite(M)) else 1.0
            im = axm.imshow(M, aspect="auto", origin="lower", cmap="coolwarm", vmin=-vmax, vmax=vmax, interpolation="nearest")
            for li, lv in enumerate(levels):
                sig = np.asarray(arcs[lv]["condition_responsive_fdr"], bool)[i]
                vals = np.asarray(arcs[lv]["condition_values"], float)
                for f in vals[sig]:
                    k = np.flatnonzero(np.isclose(freqs, f, rtol=1e-6))
                    if len(k): axm.text(k[0], li, "*", ha="center", va="center", fontsize=10)
            _readable_condition_ticks(axm, np.arange(len(freqs)), [f"{v/1000:.3g}" for v in freqs])
            axm.set_yticks(range(len(levels))); axm.set_yticklabels([f"{lv:g}" for lv in levels])
            axm.set_xlabel("Frequency (kHz)"); axm.set_ylabel("Level (dB SPL)")
            axm.set_title("Mean response (dF/F); * FDR q<0.05"); fig.colorbar(im, ax=axm, fraction=.046, pad=.03)
        for lv in levels:
            vals = np.asarray(arcs[lv]["condition_values"], float)
            mu, se = _cell_level_curve(arcs[lv], i, vals)
            axc.errorbar(np.log2(vals/1000), mu, yerr=se, marker="o", ms=4, lw=1.7, capsize=2, color=cols[lv], label=f"{lv:g} dB")
            if bool(row.get(f"{lp(lv)}_bf_eligible", False)):
                bfv = float(row[f"{lp(lv)}_best_frequency_hz"])
                axc.axvline(np.log2(bfv/1000), color=cols[lv], ls=":", lw=1.2)
                j = int(np.flatnonzero(np.isclose(vals, bfv, rtol=1e-6))[0])
                t = np.asarray(arcs[lv]["tvec"], float)
                tm = np.asarray(arcs[lv]["condition_trace_mean"], float)[i, j]; ts = np.asarray(arcs[lv]["condition_trace_sem"], float)[i, j]
                axt.plot(t, tm, color=cols[lv], lw=1.5, label=f"{lv:g} dB @ {bfv/1000:.3g} kHz")
                axt.fill_between(t, tm-ts, tm+ts, color=cols[lv], alpha=.12, lw=0)
        axc.axhline(0, color=".55", ls="--", lw=.8); _khz_axis(axc, np.asarray(arcs[levels[-1]]["condition_values"], float))
        axc.set_xlabel("Frequency (kHz; log2 spacing)"); axc.set_ylabel("Mean response (dF/F) ± SEM")
        axc.set_title("Tuning at each level (dotted = BF where eligible)"); axc.legend(frameon=False, fontsize=8)
        axt.axvline(0, color="k", ls=":", lw=.9); axt.axhline(0, color=".55", ls="--", lw=.7)
        axt.set_xlabel("Time from sound onset (s)"); axt.set_ylabel("Baseline-subtracted dF/F")
        axt.set_title("Mean ± SEM trace at each level's own BF"); axt.legend(frameon=False, fontsize=8)
        for ax in (axc, axt): ax.spines[["top", "right"]].set_visible(False)
        slope = row.get("bf_level_slope_oct_per_10dB", np.nan)
        fig.suptitle(f"Cell report | {row['subject']} {row['date']} FOV#{int(row['FOV#'])} | {row['canonicalArea']} "
                     f"depth={float(row['depth']):.1f} um | ROI {roi} | {cls.upper()}\n{_bf_text(row, levels)} | "
                     f"threshold={_fmt(row.get('threshold_level_db'), 'g')} dB, CF={_fmt(row.get('cf_hz', np.nan)/1000)} kHz, "
                     f"BF slope={_fmt(slope, '+.3f')} oct/10 dB", fontsize=12)
        fig.tight_layout(rect=[0, 0, 1, .9]); fig.savefig(root / cls / f"ROI_{roi:05d}_cell_report.png", dpi=200); plt.close(fig)


# =============================================================================
# FOV ANALYSIS
# =============================================================================

def analyze_fov(meta_seq: list[dict[str, Any]], plane: int, fov_dir: Path, n_permutations: int,
                n_shift_perm: int, seed: int, cell_reports: bool) -> tuple[pd.DataFrame, dict[str, Any]]:
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
        "red_channel_recorded": bool(reference["red_channel_recorded"]),
    })
    level_meta: dict[float, Any] = {}; arcs: dict[float, dict[str, np.ndarray]] = {}
    for k, meta in enumerate(meta_seq):
        ldf, lout, arc = analyze_level(meta, plane, reference, fov_dir, n_permutations, seed + 1009 * k)
        base = base.merge(ldf, on="suite2p_roi_index", how="left", validate="one_to_one")
        lv = float(meta["level_db"]); level_meta[lv] = lout; arcs[lv] = arc
        n_resp = int(ldf[f"{lp(lv)}_responsive_fdr"].sum()); n_elig = int(ldf[f"{lp(lv)}_bf_eligible"].sum())
        print(f"  {meta['session']} {lv:g} dB: responsive={n_resp}, BF-eligible={n_elig} of {len(ldf)}")
    cross, cross_info = cross_level_metrics(base, arcs, n_shift_perm, seed + 7)
    base = pd.concat([base, cross], axis=1)
    base.to_csv(fov_dir / "fov_cell_results.csv", index=False)
    save_level_tuning_pages(base, arcs, fov_dir)
    if cell_reports:
        save_level_cell_reports(base, arcs, fov_dir)
    summary = {"fov_uid": ref_meta["fov_uid"], "FOV#": int(ref_meta["fov_number"]), "date": ref_meta["date"],
               "levels_db": sorted(level_meta), "sessions_by_level": {f"{lv:g}": m["session"] for lv, m in level_meta.items()},
               "n_cells": len(base), "n_green": int(np.sum(base.cell_class == GREEN)), "n_yellow": int(np.sum(base.cell_class == YELLOW)),
               "suite2p_reference_dir": reference["suite2p_dir"], "level_metadata": level_meta, "cross_level": cross_info}
    save_json(fov_dir / "fov_manifest.json", summary)
    return base, summary


# =============================================================================
# COMBINED: PER-LEVEL VIEWS (last time's BF outputs, one folder per level)
# =============================================================================

def level_view(cells: pd.DataFrame, level: float) -> pd.DataFrame:
    """Cells measured at one level, with pure_<N>dB_* columns renamed to pure_* (multistim naming)."""
    p = lp(level) + "_"
    rc = p + "responsive_fdr"
    if rc not in cells:
        return cells.iloc[0:0].copy()
    sub = cells[cells[rc].notna()]
    ren = {c: "pure_" + c[len(p):] for c in cells.columns if c.startswith(p)}
    keep = [c for c in ID_COLUMNS if c in cells]
    v = sub[keep + list(ren)].rename(columns=ren).copy()
    for c in ("pure_responsive_fdr", "pure_excited_fdr", "pure_bf_eligible", "pure_any_excitatory_condition_fdr"):
        if c in v: v[c] = v[c].fillna(False).astype(bool)
    v["level_db"] = float(level)
    return v


def long_level_table(cells: pd.DataFrame, levels: list[float]) -> pd.DataFrame:
    rows = []
    for lv in levels:
        v = level_view(cells, lv)
        if v.empty: continue
        keep = [c for c in ID_COLUMNS if c in v] + ["level_db"] + [f"pure_{m}" for m in LEVEL_MEASURES if f"pure_{m}" in v]
        rows.append(v[keep])
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def _subfield_label(brain_area: Any) -> str:
    s = str(brain_area)
    return s.split("_", 1)[1] if "_" in s else "unlabeled"


def save_combined_bf_outputs(cells: pd.DataFrame, out_dir: Path, title_suffix: str = "") -> None:
    if "pure_best_frequency_hz" not in cells or "pure_responsive_fdr" not in cells: return
    use = cells[cells["pure_responsive_fdr"].fillna(False).astype(bool) & pd.to_numeric(cells["pure_best_frequency_hz"], errors="coerce").notna()].copy()
    if use.empty: return
    root = out_dir / "best_frequency"; root.mkdir(parents=True, exist_ok=True)
    vals = np.sort(pd.to_numeric(use["pure_best_frequency_hz"], errors="coerce").dropna().unique())
    # FOV x BF fraction heatmaps separately by class.
    for cls in CELL_CLASSES:
        rows = []; labels = []
        for uid, g in use[use.cell_class == cls].groupby("fov_uid"):
            arr = pd.to_numeric(g["pure_best_frequency_hz"], errors="coerce").to_numpy(float); arr = arr[np.isfinite(arr)]
            if not len(arr): continue
            rows.append([np.mean(np.isclose(arr, v)) for v in vals]); labels.append(str(uid))
        if rows:
            M = np.asarray(rows, float); fig, ax = plt.subplots(figsize=(11, max(4, 0.42*len(rows)+2.5)))
            im = ax.imshow(M, aspect="auto", vmin=0, vmax=np.nanmax(M) if np.nanmax(M) > 0 else 1, cmap="viridis")
            ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels); ax.set_xticks(range(len(vals)))
            ax.set_xticklabels([f"{v/1000:.3g}" if i % 2 == 0 else "" for i, v in enumerate(vals)], rotation=60, ha="right")
            ax.set_xlabel("Best frequency (kHz)"); ax.set_ylabel("FOV")
            ax.set_title(f"{cls.upper()} — fraction of responsive cells by BF within each FOV{title_suffix}")
            fig.colorbar(im, ax=ax, label="Fraction of cells"); fig.tight_layout(); fig.savefig(root/f"FOV_by_best_frequency_fraction_{cls}.png", dpi=250); plt.close(fig)
    # Per-FOV median BF summary by class.
    fig, ax = plt.subplots(figsize=(7, 5.5)); rng = np.random.default_rng(117)
    for pos, cls in enumerate(CELL_CLASSES):
        meds = []; ns = []
        for uid, g in use[use.cell_class == cls].groupby("fov_uid"):
            arr = np.log2(pd.to_numeric(g["pure_best_frequency_hz"], errors="coerce").to_numpy(float)); arr = arr[np.isfinite(arr)]
            if len(arr): meds.append(np.median(arr)); ns.append(len(arr))
        if meds:
            sizes = 35 + 6*np.sqrt(np.asarray(ns))
            ax.scatter(np.full(len(meds), pos)+rng.uniform(-.06, .06, len(meds)), np.asarray(meds), s=sizes, facecolors=CLASS_COLORS[cls], edgecolors="none", alpha=.8, label=cls.upper())
            mu, se, n = mean_sem(meds); ax.errorbar(pos, mu, yerr=se, fmt="o", color="black", capsize=4, zorder=4)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["GREEN", "YELLOW"]); ax.set_ylabel("FOV median log2(BF [Hz])")
    ax.set_title(f"Pure-tone BF center across FOVs{title_suffix}\nmarker size reflects responsive-cell count")
    fig.tight_layout(); fig.savefig(root/"FOV_median_best_frequency_GREEN_YELLOW.png", dpi=250); plt.close(fig)


def plot_bf_across_fovs(cells: pd.DataFrame, area: str, out_dir: Path, title_suffix: str = "") -> dict[str, Any]:
    """Best-frequency comparison across every FOV of this area (same as the multistim dual-F0 branch).

    Cell-level tests (Kruskal-Wallis across FOVs, pairwise Mann-Whitney with Holm) describe
    whether BF distributions differ between FOVs, i.e. tonotopic position; cells are the unit
    because each FOV is its own group here. The subfield comparison (for example lowFreq vs
    highFreq labels from brainArea) uses one median per FOV, so FOV is the replicate.
    """
    if "pure_best_frequency_hz" not in cells or "pure_responsive_fdr" not in cells:
        return {}
    bf = pd.to_numeric(cells["pure_best_frequency_hz"], errors="coerce")
    use = cells[cells["pure_responsive_fdr"].fillna(False).astype(bool) & (bf > 0)].copy()
    if use.empty:
        return {}
    use["log2_bf_khz"] = np.log2(pd.to_numeric(use["pure_best_frequency_hz"], errors="coerce") / 1000.0)
    root = out_dir / "best_frequency_across_FOVs"; root.mkdir(parents=True, exist_ok=True)
    fovs = (use[["fov_uid", "date", "FOV#", "brainArea", "depth"]].drop_duplicates("fov_uid")
            .sort_values(["date", "FOV#"]).reset_index(drop=True))
    fovs["subfield"] = fovs["brainArea"].map(_subfield_label)
    uids = list(fovs["fov_uid"])
    ticklabels = [f"FOV{int(r['FOV#'])}\n{r['subfield']}\n{float(r['depth']):.0f} um" for _, r in fovs.iterrows()]
    groups = {g: (use if g == "all" else use[use.cell_class == g]) for g in CELL_GROUPS}

    rows = []
    for gname, g in groups.items():
        for _, fr in fovs.iterrows():
            v = finite(g.loc[g.fov_uid == fr.fov_uid, "log2_bf_khz"])
            rows.append({"cells": gname, "fov_uid": fr.fov_uid, "FOV#": int(fr["FOV#"]), "brainArea": fr.brainArea,
                         "subfield": fr.subfield, "depth": fr.depth, "n_cells": len(v),
                         "median_bf_khz": float(2 ** np.median(v)) if len(v) else np.nan,
                         "q25_bf_khz": float(2 ** np.percentile(v, 25)) if len(v) else np.nan,
                         "q75_bf_khz": float(2 ** np.percentile(v, 75)) if len(v) else np.nan})
    summ = pd.DataFrame(rows); summ.to_csv(root / "BF_per_FOV_summary.csv", index=False)

    stats_out: dict[str, Any] = {"note": "cell-level tests across FOVs describe BF differences between FOVs (tonotopic position)"}
    pair_rows = []
    for gname, g in groups.items():
        per = [finite(g.loc[g.fov_uid == u, "log2_bf_khz"]) for u in uids]
        good = [v for v in per if len(v)]
        kwr = {"H": np.nan, "p": np.nan}
        if len(good) >= 2:
            try:
                r = stats.kruskal(*good); kwr = {"H": float(r.statistic), "p": float(r.pvalue)}
            except ValueError:
                kwr = {"H": 0.0, "p": 1.0}
        kwr["n_fovs_with_cells"] = len(good); kwr["n_cells"] = int(sum(len(v) for v in good))
        prs = []
        for i in range(len(uids)):
            for j in range(i + 1, len(uids)):
                r = _mw_simple(per[i], per[j])
                r.update({"cells": gname, "fov_a": uids[i], "fov_b": uids[j],
                          "median_diff_oct_a_minus_b": float(np.median(per[i]) - np.median(per[j])) if len(per[i]) and len(per[j]) else np.nan})
                prs.append(r)
        adj = holm_adjust([r["p"] for r in prs])
        for r, ph in zip(prs, adj):
            r["p_holm_pairs"] = float(ph) if np.isfinite(ph) else np.nan
        pair_rows += prs; stats_out[gname] = {"kruskal_wallis_across_FOVs": kwr, "n_pairs": len(prs)}
    pd.DataFrame(pair_rows).to_csv(root / "BF_pairwise_FOV_tests.csv", index=False)

    ytick_hz = np.sort(pd.to_numeric(use["pure_best_frequency_hz"], errors="coerce").dropna().unique())
    fig, (ax, axs) = plt.subplots(1, 2, figsize=(max(12, 1.5 * len(uids) + 6), 6.5), gridspec_kw={"width_ratios": [max(2.0, .35 * len(uids)), 1.0]})
    rng = np.random.default_rng(4049)
    for i, u in enumerate(uids):
        allv = finite(use.loc[use.fov_uid == u, "log2_bf_khz"])
        if len(allv):
            ax.boxplot([allv], positions=[i], widths=.62, showfliers=False, patch_artist=True,
                       boxprops=dict(facecolor="0.93", edgecolor="0.55"), medianprops=dict(color="black", lw=1.6),
                       whiskerprops=dict(color="0.55"), capprops=dict(color="0.55"))
        for off, cls in ((-.14, GREEN), (.14, YELLOW)):
            v = finite(use.loc[(use.fov_uid == u) & (use.cell_class == cls), "log2_bf_khz"])
            if len(v):
                ax.scatter(i + off + rng.uniform(-.07, .07, len(v)), v + rng.uniform(-.04, .04, len(v)), s=12, alpha=.55,
                           color=CLASS_COLORS[cls], edgecolors="none", label=cls.upper() if i == 0 else None, zorder=3)
    ax.set_xticks(range(len(uids))); ax.set_xticklabels(ticklabels, fontsize=8.5)
    yt = np.log2(ytick_hz / 1000.0); ax.set_yticks(yt[::2]); ax.set_yticklabels([f"{v/1000:.3g}" for v in ytick_hz[::2]])
    ax.set_ylabel("Best frequency (kHz; log2 spacing)"); ax.set_xlim(-.6, len(uids) - .4)
    ax.set_title(f"{area}: pure-tone BF of FDR-responsive cells in every FOV{title_suffix}\nbox = all cells; points jittered (GREEN left, YELLOW right)")
    ax.legend(frameon=False, loc="upper left")
    lines = ["Kruskal-Wallis across FOVs (cells = units;", "  describes BF differences between FOVs)"]
    for gname in CELL_GROUPS:
        r = stats_out[gname]["kruskal_wallis_across_FOVs"]
        lines.append(f"{gname.upper():6s}: H={r['H']:.3g}, p={r['p']:.3g}, nFOV={r['n_fovs_with_cells']}, n={r['n_cells']}")
    lines += ["", "Per-FOV n (" + " / ".join(g.upper() for g in CELL_GROUPS) + "):"]
    for u, lab in zip(uids, ticklabels):
        ns = [int(summ.loc[(summ.cells == g) & (summ.fov_uid == u), "n_cells"].iloc[0]) for g in CELL_GROUPS]
        lines.append(f"{lab.splitlines()[0]:6s} {lab.splitlines()[1]:10s} " + " / ".join(f"{n:4d}" for n in ns))
    lines += ["", "Pairwise FOV tests (MW U, Holm across pairs):", "BF_pairwise_FOV_heatmaps.png, BF_pairwise_FOV_tests.csv"]
    axs.axis("off"); axs.text(.01, .99, "\n".join(lines), va="top", ha="left", fontsize=8.2, family="monospace", transform=axs.transAxes)
    fig.tight_layout(); fig.savefig(root / "BF_by_FOV_cells.png", dpi=250); plt.close(fig)

    pr = pd.DataFrame(pair_rows)
    if len(uids) >= 2 and len(pr):
        ng = len(CELL_GROUPS)
        fig, axes = plt.subplots(1, ng, figsize=(max(5.5 * ng, 1.35 * ng * len(uids)), max(5.2, .55 * len(uids) + 2.8)), squeeze=False)
        short = [lab.splitlines()[0] + " " + lab.splitlines()[1] for lab in ticklabels]
        lim = np.nanmax(np.abs(pr["median_diff_oct_a_minus_b"])) if np.any(np.isfinite(pr["median_diff_oct_a_minus_b"])) else 1.0
        for ax, gname in zip(axes[0], CELL_GROUPS):
            M = np.full((len(uids), len(uids)), np.nan); S = np.zeros_like(M, bool)
            for _, r in pr[pr.cells == gname].iterrows():
                i, j = uids.index(r.fov_a), uids.index(r.fov_b)
                M[i, j] = r.median_diff_oct_a_minus_b; M[j, i] = -r.median_diff_oct_a_minus_b
                S[i, j] = S[j, i] = bool(np.isfinite(r.p_holm_pairs) and r.p_holm_pairs < .05)
            im = ax.imshow(M, cmap="coolwarm", vmin=-lim, vmax=lim)
            for i in range(len(uids)):
                for j in range(len(uids)):
                    if S[i, j]: ax.text(j, i, "*", ha="center", va="center", fontsize=14, color="black")
            ax.set_xticks(range(len(uids))); ax.set_xticklabels(short, rotation=60, ha="right", fontsize=8)
            ax.set_yticks(range(len(uids))); ax.set_yticklabels(short, fontsize=8)
            ax.set_title(f"{gname.upper()}: median BF(row) - BF(col), octaves\n* Holm-corrected MW p<0.05 ({stats_out[gname]['n_pairs']} pairs)", fontsize=9.5)
            fig.colorbar(im, ax=ax, fraction=.046, pad=.04, label="octaves")
        fig.suptitle(f"{area}: pairwise BF comparisons between FOVs (cells = units){title_suffix}"); fig.tight_layout(rect=[0, 0, 1, .94])
        fig.savefig(root / "BF_pairwise_FOV_heatmaps.png", dpi=250); plt.close(fig)

    subs = list(dict.fromkeys(fovs["subfield"]))
    stats_out["subfield"] = {"groups": subs}
    fig, axes = plt.subplots(1, len(CELL_GROUPS), figsize=(5 * len(CELL_GROUPS), 5.4), sharey=True, squeeze=False)
    for ax, gname in zip(axes[0], CELL_GROUPS):
        s = summ[(summ.cells == gname) & (summ.n_cells > 0)]
        med = {sf: np.log2(s.loc[s.subfield == sf, "median_bf_khz"].to_numpy(float)) for sf in subs}
        for i, sf in enumerate(subs):
            z = finite(med[sf]); ns = s.loc[s.subfield == sf, "n_cells"].to_numpy(float)
            ax.scatter(np.full(len(z), i), z, s=35 + 6 * np.sqrt(ns[:len(z)]), color=CLASS_COLORS.get(gname, "0.35"), edgecolors="none", alpha=.85)
            mu, se, n = mean_sem(z); ax.errorbar(i, mu, yerr=se, fmt="o", color="black", capsize=4)
        if len(subs) == 2:
            r = _mw_simple(med[subs[0]], med[subs[1]]); r["test"] = "Mann-Whitney U on FOV medians"
            txt = f"{subs[0]} vs {subs[1]}: MW U={r['U']:.3g}, p={r['p']:.3g}\nnFOV={r['n1']}/{r['n2']} (FOV = replicate)"
        elif len(subs) > 2:
            good = [finite(v) for v in med.values() if len(finite(v))]
            try:
                kk = stats.kruskal(*good); r = {"test": "Kruskal-Wallis on FOV medians", "H": float(kk.statistic), "p": float(kk.pvalue)}
            except ValueError:
                r = {"test": "Kruskal-Wallis on FOV medians", "H": np.nan, "p": np.nan}
            txt = f"Kruskal-Wallis H={r['H']:.3g}, p={r['p']:.3g} (FOV = replicate)"
        else:
            r = {"test": "none (one subfield label)"}; txt = "only one subfield label"
        stats_out["subfield"][gname] = r
        ax.text(.02, .98, txt, transform=ax.transAxes, va="top", fontsize=8.3)
        ax.set_xticks(range(len(subs))); ax.set_xticklabels(subs); ax.set_xlim(-.6, len(subs) - .4); ax.set_title(f"{gname.upper()} cells")
    axes[0, 0].set_yticks(yt[::2]); axes[0, 0].set_yticklabels([f"{v/1000:.3g}" for v in ytick_hz[::2]]); axes[0, 0].set_ylabel("FOV median BF (kHz; log2 spacing)")
    fig.suptitle(f"{area}: FOV median BF by brainArea subfield label (marker size = responsive-cell count){title_suffix}"); fig.tight_layout(rect=[0, 0, 1, .93])
    fig.savefig(root / "BF_FOV_median_by_subfield.png", dpi=250); plt.close(fig)
    save_json(root / "BF_across_FOVs_statistics.json", stats_out)
    return stats_out


def plot_responsiveness_by_level(fsum: pd.DataFrame, levels: list[float], out_dir: Path) -> dict[str, Any]:
    """GREEN vs YELLOW % responsive at each level; paired across FOVs, Holm across levels."""
    fig, axes = plt.subplots(1, len(levels), figsize=(4.6 * len(levels), 5), squeeze=False, sharey=True)
    recs = []
    for ax, lv in zip(axes[0], levels):
        s = fsum[(fsum.level_db == lv) & fsum.cell_class.isin(CELL_CLASSES)]
        piv = s.pivot_table(index="fov_uid", columns="cell_class", values="pct_responsive", aggfunc="mean")
        for _, r in piv.iterrows():
            if GREEN in r and YELLOW in r and np.isfinite(r[GREEN]) and np.isfinite(r[YELLOW]):
                ax.plot([0, 1], [r[GREEN], r[YELLOW]], color="0.75", lw=1, zorder=1)
        for x, cls in enumerate(CELL_CLASSES):
            v = piv[cls].dropna().to_numpy(float) if cls in piv else np.array([])
            ax.scatter(np.full(len(v), x), v, s=32, color=CLASS_COLORS[cls], zorder=2)
            mu, se, n = mean_sem(v); ax.errorbar(x, mu, yerr=se, fmt="o", color="black", capsize=4, zorder=3)
        rec = safe_wilcoxon_pairs(piv.reset_index(), GREEN, YELLOW) if GREEN in piv and YELLOW in piv else {"n_pairs": 0, "W": np.nan, "p": np.nan}
        recs.append((ax, lv, rec)); ax.set_xticks([0, 1]); ax.set_xticklabels(["GREEN", "YELLOW"]); ax.set_ylim(0, 100)
        ax.set_title(f"{lv:g} dB")
    axes[0, 0].set_ylabel("Responsive cells (%)")
    adj = holm_adjust([r["p"] for _, _, r in recs]); out = {}
    for (ax, lv, rec), ph in zip(recs, adj):
        rec[f"p_holm_{len(recs)}_levels"] = float(ph) if np.isfinite(ph) else np.nan; out[f"{lv:g}dB"] = rec
        ax.text(.02, .98, f"paired FOV Wilcoxon\nW={_fmt(rec['W'])}, p={_fmt(rec['p'])}\nHolm({len(recs)}) p={_fmt(ph)}\nn={rec['n_pairs']} FOVs",
                transform=ax.transAxes, ha="left", va="top", fontsize=8)
    fig.suptitle("Pure-tone responsiveness: GREEN vs YELLOW at each level; FOV is replicate"); fig.tight_layout(rect=[0, 0, 1, .93])
    fig.savefig(out_dir / "responsive_fraction_GREEN_vs_YELLOW_by_level.png", dpi=250); plt.close(fig)
    return out


# =============================================================================
# COMBINED: BF ACROSS LEVELS
# =============================================================================

def fov_level_summary(long: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gname in CELL_GROUPS:
        g0 = long if gname == "all" else long[long.cell_class == gname]
        for (uid, lv), g in g0.groupby(["fov_uid", "level_db"]):
            el = g[g.pure_bf_eligible]
            rows.append({"cell_class": gname, "fov_uid": uid, "FOV#": int(g["FOV#"].iloc[0]), "brainArea": g.brainArea.iloc[0],
                         "level_db": lv, "n_cells": len(g),
                         "pct_responsive": 100 * g.pure_responsive_fdr.mean(), "pct_bf_eligible": 100 * g.pure_bf_eligible.mean(),
                         "n_bf_eligible": len(el),
                         "median_bf_khz": float(2 ** np.median(np.log2(el.pure_best_frequency_hz))) / 1000 if len(el) else np.nan,
                         "median_centroid_bf_khz": float(2 ** np.nanmedian(np.log2(el.pure_bf_centroid_hz))) / 1000 if len(el) and el.pure_bf_centroid_hz.notna().any() else np.nan,
                         "median_response_at_bf": float(np.median(el.pure_preferred_response)) if len(el) else np.nan,
                         "median_fwhm_octaves": float(np.nanmedian(el.pure_fwhm_octaves)) if len(el) and el.pure_fwhm_octaves.notna().any() else np.nan,
                         "median_lifetime_sparseness": float(np.nanmedian(el.pure_lifetime_sparseness)) if len(el) and el.pure_lifetime_sparseness.notna().any() else np.nan})
    return pd.DataFrame(rows)


def _pair_columns(cells: pd.DataFrame) -> list[tuple[float, float, str]]:
    pat = re.compile(r"^bfshift_([0-9.]+)_vs_([0-9.]+)dB_oct$")
    out = []
    for c in cells.columns:
        m = pat.match(c)
        if m: out.append((float(m.group(2)), float(m.group(1)), pair_tag(float(m.group(2)), float(m.group(1)))))
    return sorted(set(out))


def bf_shift_tables(cells: pd.DataFrame, pairs: list[tuple[float, float, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Long cell x pair shift table and FOV x class x pair summary."""
    rows = []
    for a, b, t in pairs:
        c = f"bfshift_{t}_oct"
        sub = cells[cells[c].notna()]
        for _, r in sub.iterrows():
            rows.append({"fov_uid": r.fov_uid, "FOV#": int(r["FOV#"]), "suite2p_roi_index": int(r.suite2p_roi_index),
                         "cell_class": r.cell_class, "level_a_db": a, "level_b_db": b, "pair": t,
                         "bf_a_hz": r[f"{lp(a)}_best_frequency_hz"], "bf_b_hz": r[f"{lp(b)}_best_frequency_hz"],
                         "bfshift_oct": r[c], "bfshift_perm_p": r[f"bfshift_{t}_perm_p"], "bfshift_perm_q": r[f"bfshift_{t}_perm_q"],
                         "centroidshift_oct": r[f"centroidshift_{t}_oct"], "centroidshift_perm_p": r[f"centroidshift_{t}_perm_p"],
                         "centroidshift_perm_q": r[f"centroidshift_{t}_perm_q"]})
    long = pd.DataFrame(rows)
    srows = []
    if len(long):
        for gname in CELL_GROUPS:
            g0 = long if gname == "all" else long[long.cell_class == gname]
            for (uid, t), g in g0.groupby(["fov_uid", "pair"]):
                srows.append({"cell_class": gname, "fov_uid": uid, "FOV#": int(g["FOV#"].iloc[0]), "pair": t,
                              "level_a_db": g.level_a_db.iloc[0], "level_b_db": g.level_b_db.iloc[0], "n_cells": len(g),
                              "median_bfshift_oct": float(g.bfshift_oct.median()),
                              "median_abs_bfshift_oct": float(g.bfshift_oct.abs().median()),
                              "pct_bf_unchanged": 100 * float(np.mean(np.isclose(g.bfshift_oct, 0))),
                              "median_centroidshift_oct": float(g.centroidshift_oct.median()) if g.centroidshift_oct.notna().any() else np.nan,
                              "pct_sig_bfshift_q05": 100 * float(np.mean(g.bfshift_perm_q < .05)),
                              "pct_sig_centroidshift_q05": 100 * float(np.mean(g.centroidshift_perm_q < .05)),
                              "within_FOV_wilcoxon_bfshift": wilcoxon_vs_zero(g.bfshift_oct)["p"],
                              "within_FOV_wilcoxon_centroidshift": wilcoxon_vs_zero(g.centroidshift_oct)["p"]})
    return long, pd.DataFrame(srows)


def analyze_bf_across_levels(cells: pd.DataFrame, long: pd.DataFrame, levels: list[float], ref: float,
                             area: str, out_dir: Path) -> dict[str, Any]:
    root = out_dir / "best_frequency_across_levels"; root.mkdir(parents=True, exist_ok=True)
    cols = level_colors(levels)
    st: dict[str, Any] = {"reference_level_db": ref, "levels_db": levels,
                          "bf_eligible_definition": "FDR-responsive at the level, response at BF > 0, q < 0.05 at BF",
                          "replicate": "FOV for across-FOV tests; within-FOV tests use cells and describe that FOV; pooled-cell tests exploratory"}
    fsum = fov_level_summary(long); fsum.to_csv(root / "BF_level_FOV_summary.csv", index=False)
    pairs = _pair_columns(cells)
    shift_long, shift_summ = bf_shift_tables(cells, pairs)
    shift_long.to_csv(root / "BF_level_pair_shifts_cells.csv", index=False)
    shift_summ.to_csv(root / "BF_level_pair_shifts_FOV_summary.csv", index=False)
    all_freqs = np.sort(long.loc[long.pure_bf_eligible, "pure_best_frequency_hz"].dropna().unique())
    multi_fovs = sorted(cells.loc[cells["n_levels_recorded"] >= 2, "fov_uid"].unique()) if "n_levels_recorded" in cells else []
    st["fovs_with_multiple_levels"] = multi_fovs

    # 1. Tuning metrics by level (FOV lines), Friedman across levels on FOVs with every level.
    metrics = [("pct_responsive", "Responsive cells (%)"), ("pct_bf_eligible", "BF-eligible cells (%)"),
               ("median_bf_khz", "Median BF (kHz)"), ("median_response_at_bf", "Median response at BF (dF/F)"),
               ("median_fwhm_octaves", "Median FWHM (octaves)"), ("median_lifetime_sparseness", "Median lifetime sparseness")]
    fig, axes = plt.subplots(len(metrics), len(CELL_GROUPS), figsize=(max(11, 4.7 * len(CELL_GROUPS) + .5), 3.1 * len(metrics)), squeeze=False, sharex=True)
    st["metrics_by_level_friedman"] = {}
    for r_, (m, lab) in enumerate(metrics):
        for c_, gname in enumerate(CELL_GROUPS):
            ax = axes[r_, c_]; s = fsum[fsum.cell_class == gname]
            piv = s.pivot_table(index="fov_uid", columns="level_db", values=m)
            yv = (lambda v: np.log2(v)) if m == "median_bf_khz" else (lambda v: v)
            for uid, row in piv.iterrows():
                ax.plot(row.index, yv(row.to_numpy(float)), marker="o", ms=3.5, lw=1, color="0.7")
            mu = [mean_sem(yv(piv[lv].to_numpy(float)))[:2] if lv in piv else (np.nan, np.nan) for lv in levels]
            ax.errorbar(levels, [x[0] for x in mu], yerr=[x[1] for x in mu], marker="o", lw=2, capsize=3, color=CLASS_COLORS[gname])
            fr = friedman_across_levels(piv.reindex(columns=levels)) if len(piv) else {"chi2": np.nan, "p": np.nan, "n_replicates": 0}
            st["metrics_by_level_friedman"].setdefault(m, {})[gname] = fr
            ax.text(.02, .97, f"Friedman p={_fmt(fr['p'])} (nFOV={fr['n_replicates']})", transform=ax.transAxes, va="top", fontsize=8)
            if m == "median_bf_khz" and len(all_freqs):
                ax.set_yticks(np.log2(all_freqs[::2]/1000)); ax.set_yticklabels([f"{v/1000:.3g}" for v in all_freqs[::2]])
            if r_ == 0: ax.set_title(f"{gname.upper()} cells")
            if c_ == 0: ax.set_ylabel(lab, fontsize=9)
            ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[-1]: ax.set_xticks(levels); ax.set_xlabel("Level (dB SPL)")
    fig.suptitle(f"{area}: pure-tone tuning metrics by level (gray = one FOV; BF/response/FWHM/sparseness over BF-eligible cells)\n"
                 "Friedman test across levels uses FOVs recorded at every level", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(root / "tuning_metrics_by_level.png", dpi=220); plt.close(fig)

    # 2. BF distribution per level (fraction of BF-eligible cells), all FOVs pooled and per FOV.
    if len(all_freqs):
        x = np.log2(all_freqs / 1000)
        fovs = sorted(long.fov_uid.unique())
        fig, axes = plt.subplots(len(fovs) + 1, len(CELL_GROUPS), figsize=(max(11, 5 * len(CELL_GROUPS) + .5), 2.6 * (len(fovs) + 1) + 1), squeeze=False, sharex=True)
        for c_, gname in enumerate(CELL_GROUPS):
            g0 = long[long.pure_bf_eligible] if gname == "all" else long[long.pure_bf_eligible & (long.cell_class == gname)]
            for r_, uid in enumerate(["pooled"] + fovs):
                ax = axes[r_, c_]; g = g0 if uid == "pooled" else g0[g0.fov_uid == uid]
                for lv in levels:
                    arr = g.loc[g.level_db == lv, "pure_best_frequency_hz"].to_numpy(float)
                    if not len(arr): continue
                    frac = np.array([np.mean(np.isclose(arr, f)) for f in all_freqs])
                    ax.plot(x, frac, marker="o", ms=3, lw=1.6, color=cols[lv], label=f"{lv:g} dB (n={len(arr)})")
                ax.legend(frameon=False, fontsize=7, loc="upper right")
                if c_ == 0: ax.set_ylabel(("all FOVs\n(pooled cells)" if uid == "pooled" else uid) + "\nfraction", fontsize=8.5)
                if r_ == 0: ax.set_title(f"{gname.upper()} BF-eligible cells")
                ax.spines[["top", "right"]].set_visible(False)
        for ax in axes[-1]: _khz_axis(ax, all_freqs); ax.set_xlabel("Best frequency (kHz)")
        fig.suptitle(f"{area}: BF distribution at each level", fontsize=13); fig.tight_layout(rect=[0, 0, 1, .97])
        fig.savefig(root / "BF_distribution_by_level.png", dpi=220); plt.close(fig)

    # 3. Paired BF scatter for every level pair (same cells), pooled cells with FOV-level summary text.
    if pairs and len(all_freqs):
        rng = np.random.default_rng(31)
        fig, axes = plt.subplots(1, len(pairs), figsize=(4.6 * len(pairs), 5.2), squeeze=False)
        lo, hi = np.log2(all_freqs[0]/1000) - .3, np.log2(all_freqs[-1]/1000) + .3
        for ax, (a, b, t) in zip(axes[0], pairs):
            g = shift_long[shift_long.pair == t] if len(shift_long) else pd.DataFrame()
            ax.plot([lo, hi], [lo, hi], color="0.6", lw=1, ls="--")
            for cls in CELL_CLASSES:
                s = g[g.cell_class == cls] if len(g) else g
                if not len(s): continue
                ax.scatter(np.log2(s.bf_a_hz/1000) + rng.uniform(-.07, .07, len(s)), np.log2(s.bf_b_hz/1000) + rng.uniform(-.07, .07, len(s)),
                           s=10, alpha=.5, color=CLASS_COLORS[cls], edgecolors="none", label=f"{cls.upper()} n={len(s)}")
            ss = shift_summ[(shift_summ.cell_class == "all") & (shift_summ.pair == t)] if len(shift_summ) else pd.DataFrame()
            fovr = wilcoxon_vs_zero(ss.median_bfshift_oct) if len(ss) else {"n": 0, "p": np.nan, "median": np.nan}
            txt = (f"median shift {_fmt(g.bfshift_oct.median() if len(g) else np.nan, '+.2f')} oct (cells)\n"
                   f"BF unchanged: {_fmt(100*np.mean(np.isclose(g.bfshift_oct, 0)) if len(g) else np.nan, '.0f')}%\n"
                   f"centroid perm q<.05: {_fmt(100*np.mean(g.centroidshift_perm_q < .05) if len(g) else np.nan, '.0f')}% of cells\n"
                   f"FOV medians vs 0: p={_fmt(fovr['p'])} (nFOV={fovr['n']})")
            ax.text(.03, .97, txt, transform=ax.transAxes, va="top", fontsize=8)
            ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
            ticks = all_freqs[::3]; ax.set_xticks(np.log2(ticks/1000)); ax.set_xticklabels([f"{v/1000:.3g}" for v in ticks])
            ax.set_yticks(np.log2(ticks/1000)); ax.set_yticklabels([f"{v/1000:.3g}" for v in ticks])
            ax.set_xlabel(f"BF at {a:g} dB (kHz)"); ax.set_ylabel(f"BF at {b:g} dB (kHz)"); ax.set_title(f"{b:g} vs {a:g} dB")
            ax.legend(frameon=False, fontsize=7, loc="lower right")
        fig.suptitle(f"{area}: BF of the same cells at two levels (BF-eligible at both; jittered)", fontsize=12)
        fig.tight_layout(rect=[0, 0, 1, .94]); fig.savefig(root / "BF_pairwise_level_scatter.png", dpi=220); plt.close(fig)

    # 4. BF shift relative to the reference level, FOV medians (FOV = replicate).
    st["shift_vs_reference"] = {}
    others = [lv for lv in levels if lv != ref]
    if others and len(shift_long):
        fig, axes = plt.subplots(2, len(CELL_GROUPS), figsize=(max(11, 5 * len(CELL_GROUPS) + .5), 9), squeeze=False, sharex=True)
        for r_, (col, lab) in enumerate((("bfshift_oct", "argmax BF"), ("centroidshift_oct", "half-max centroid BF"))):
            for c_, gname in enumerate(CELL_GROUPS):
                ax = axes[r_, c_]; recs = []
                g0 = shift_long if gname == "all" else shift_long[shift_long.cell_class == gname]
                meds = {}
                for lv in others:
                    a, b = min(lv, ref), max(lv, ref); sign = 1.0 if lv > ref else -1.0   # shift = BF(lv) - BF(ref)
                    g = g0[g0.pair == pair_tag(a, b)]
                    meds[lv] = g.groupby("fov_uid")[col].median() * sign
                    rec = wilcoxon_vs_zero(meds[lv]); rec["pooled_cells_exploratory"] = wilcoxon_vs_zero(g[col] * sign)
                    recs.append((lv, rec))
                tab = pd.DataFrame(meds)
                for uid, row in tab.iterrows():
                    ax.plot(list(row.index) + [ref], list(row.to_numpy(float)) + [0.0], marker="o", ms=3.5, lw=1, color="0.7")
                mu = [mean_sem(tab[lv])[:2] if lv in tab else (np.nan, np.nan) for lv in others]
                ax.errorbar(others + [ref], [m[0] for m in mu] + [0.0], yerr=[m[1] for m in mu] + [0.0], marker="o", lw=2, capsize=3, color=CLASS_COLORS[gname])
                ax.axhline(0, color="0.5", ls="--", lw=.8)
                adj = holm_adjust([rec["p"] for _, rec in recs])
                lines = []
                for (lv, rec), ph in zip(recs, adj):
                    rec[f"p_holm_{len(recs)}_levels"] = float(ph) if np.isfinite(ph) else np.nan
                    st["shift_vs_reference"].setdefault(lab, {}).setdefault(gname, {})[f"{lv:g}dB"] = rec
                    lines.append(f"{lv:g} dB: FOV p={_fmt(rec['p'])} (Holm {_fmt(ph)}, n={rec['n']}); cells p={_fmt(rec['pooled_cells_exploratory']['p'])}")
                ax.text(.02, .02, "\n".join(lines), transform=ax.transAxes, fontsize=7.2, va="bottom")
                if r_ == 0: ax.set_title(f"{gname.upper()} cells")
                if c_ == 0: ax.set_ylabel(f"{lab} shift re {ref:g} dB (octaves)\nFOV medians")
                ax.spines[["top", "right"]].set_visible(False)
        for ax in axes[-1]: ax.set_xticks(levels); ax.set_xlabel("Level (dB SPL)")
        fig.suptitle(f"{area}: BF shift relative to {ref:g} dB, same cells (BF-eligible at both levels)\n"
                     "gray = one FOV median; colored = mean ± SEM across FOVs; FOV Wilcoxon vs 0 (Holm across levels); "
                     "'cells' = pooled-cell Wilcoxon (exploratory)", fontsize=11)
        fig.tight_layout(rect=[0, 0, 1, .93]); fig.savefig(root / "BF_shift_vs_reference_level.png", dpi=220); plt.close(fig)

    # 5. Per-cell BF-vs-level slope by FOV and class.
    st["slope"] = {}
    for col, lab in (("bf_level_slope_oct_per_10dB", "argmax BF"), ("centroid_level_slope_oct_per_10dB", "centroid BF")):
        if col not in cells: continue
        s = cells[cells[col].notna()]
        if s.empty: continue
        fovs = sorted(s.fov_uid.unique()); rng = np.random.default_rng(5)
        fig, (ax, axs) = plt.subplots(1, 2, figsize=(max(10, 2.2 * len(fovs) + 6), 5.8), gridspec_kw={"width_ratios": [max(1.5, .5 * len(fovs)), 1]})
        rec_fov = {}
        for i, uid in enumerate(fovs):
            for off, cls in ((-.15, GREEN), (.15, YELLOW)):
                v = finite(s.loc[(s.fov_uid == uid) & (s.cell_class == cls), col])
                if len(v):
                    ax.scatter(i + off + rng.uniform(-.06, .06, len(v)), v, s=11, alpha=.5, color=CLASS_COLORS[cls], edgecolors="none",
                               label=cls.upper() if i == 0 else None)
                    ax.plot([i + off - .12, i + off + .12], [np.median(v)] * 2, color="black", lw=2)
            rec_fov[uid] = {g: wilcoxon_vs_zero(s.loc[(s.fov_uid == uid) & ((s.cell_class == g) if g != "all" else True), col]) for g in CELL_GROUPS}
        ax.axhline(0, color="0.5", ls="--", lw=.8); ax.set_xticks(range(len(fovs))); ax.set_xticklabels(fovs, rotation=20, fontsize=8)
        ax.set_ylabel(f"{lab} slope (octaves per 10 dB)"); ax.legend(frameon=False)
        ax.set_title(f"Per-cell {lab} vs level slope (cells BF-eligible at >= {MIN_LEVELS_FOR_SLOPE} levels); bar = median")
        meds = s.groupby(["fov_uid", "cell_class"])[col].median().unstack()
        allmed = s.groupby("fov_uid")[col].median()
        across = {"all": wilcoxon_vs_zero(allmed)}
        for cls in CELL_CLASSES:
            across[cls] = wilcoxon_vs_zero(meds[cls]) if cls in meds else wilcoxon_vs_zero([])
        gy = safe_wilcoxon_pairs(meds.reset_index(), GREEN, YELLOW) if GREEN in meds and YELLOW in meds else {"n_pairs": 0, "W": np.nan, "p": np.nan}
        pooled = {g: wilcoxon_vs_zero(s[col] if g == "all" else s.loc[s.cell_class == g, col]) for g in CELL_GROUPS}
        pooled["GREEN_vs_YELLOW_MW"] = _mw_simple(s.loc[s.cell_class == GREEN, col], s.loc[s.cell_class == YELLOW, col])
        st["slope"][lab] = {"across_FOV_medians_vs_0": across, "GREEN_vs_YELLOW_paired_FOV": gy,
                            "within_FOV_cells_vs_0": rec_fov, "pooled_cells_exploratory": pooled}
        lines = ["Across FOVs (FOV medians vs 0, Wilcoxon):"]
        lines += [f"  {g.upper():6s} median={_fmt(across[g]['median'], '+.3f')} p={_fmt(across[g]['p'])} nFOV={across[g]['n']}" for g in CELL_GROUPS]
        lines += [f"GREEN vs YELLOW (paired FOVs): p={_fmt(gy['p'])} n={gy['n_pairs']}", "", "Within each FOV (cells vs 0):"]
        lines += [f"  {uid}: all p={_fmt(rec_fov[uid]['all']['p'])} n={rec_fov[uid]['all']['n']}" for uid in fovs]
        lines += ["", "Pooled cells (exploratory):"]
        lines += [f"  {g.upper():6s} median={_fmt(pooled[g]['median'], '+.3f')} p={_fmt(pooled[g]['p'])} n={pooled[g]['n']}" for g in CELL_GROUPS]
        lines += [f"  GREEN vs YELLOW MW p={_fmt(pooled['GREEN_vs_YELLOW_MW']['p'])}"]
        axs.axis("off"); axs.text(0, 1, "\n".join(lines), va="top", fontsize=8.2, family="monospace", transform=axs.transAxes)
        fig.tight_layout(); fig.savefig(root / f"{col.replace('_oct_per_10dB', '')}_by_FOV.png", dpi=220); plt.close(fig)

    # 6. Per-FOV BF matrix: cells x levels, sorted by BF at the reference level.
    if multi_fovs and len(all_freqs):
        fig, axes = plt.subplots(1, len(multi_fovs), figsize=(3.2 * len(multi_fovs) + 1.5, 9), squeeze=False)
        vmin, vmax = np.log2(all_freqs[0]/1000), np.log2(all_freqs[-1]/1000)
        for ax, uid in zip(axes[0], multi_fovs):
            g = cells[(cells.fov_uid == uid) & (cells.n_levels_bf_eligible >= 2)].copy()
            lv_here = [lv for lv in levels if f"{lp(lv)}_bf_eligible" in g and g[f"{lp(lv)}_bf_eligible"].notna().any()]
            M = np.stack([np.where(g[f"{lp(lv)}_bf_eligible"].fillna(False).astype(bool), np.log2(g[f"{lp(lv)}_best_frequency_hz"].astype(float)/1000), np.nan)
                          for lv in lv_here], axis=1) if len(g) else np.zeros((0, len(lv_here)))
            sortkey = M[:, lv_here.index(ref)] if ref in lv_here else np.nanmedian(M, axis=1)
            order = np.lexsort((np.nanmedian(M, axis=1) if len(M) else [], np.nan_to_num(sortkey, nan=np.inf)))
            im = ax.imshow(M[order] if len(M) else np.zeros((1, len(lv_here))) * np.nan, aspect="auto", cmap="viridis", vmin=vmin, vmax=vmax, interpolation="nearest")
            ax.set_facecolor("0.88"); ax.set_xticks(range(len(lv_here))); ax.set_xticklabels([f"{lv:g}" for lv in lv_here])
            ax.set_xlabel("Level (dB)"); ax.set_title(f"{uid}\nn={len(g)} cells", fontsize=9); ax.set_yticks([])
        axes[0, 0].set_ylabel(f"Cells BF-eligible at >= 2 levels, sorted by BF at {ref:g} dB")
        cb = fig.colorbar(im, ax=axes[0].tolist(), fraction=.03, pad=.02); cb.set_label("BF (kHz)")
        tk = all_freqs[::2]; cb.set_ticks(np.log2(tk/1000)); cb.set_ticklabels([f"{v/1000:.3g}" for v in tk])
        fig.suptitle(f"{area}: BF of each cell at each level (gray = not BF-eligible at that level)", fontsize=12)
        fig.savefig(root / "BF_across_levels_cell_matrix.png", dpi=220, bbox_inches="tight"); plt.close(fig)

    # 7. Percent of cells with a significant BF shift (permutation, BH within FOV) per pair.
    if len(shift_summ):
        fig, axes = plt.subplots(2, len(CELL_GROUPS), figsize=(max(11, 5 * len(CELL_GROUPS) + .5), 8.5), squeeze=False, sharey=True)
        tags = [t for _, _, t in pairs]
        for r_, (col, lab) in enumerate((("pct_sig_centroidshift_q05", "centroid BF (primary test)"),
                                         ("pct_sig_bfshift_q05", "argmax BF (conservative)"))):
            for c_, gname in enumerate(CELL_GROUPS):
                ax = axes[r_, c_]; s = shift_summ[shift_summ.cell_class == gname]
                piv = s.pivot_table(index="fov_uid", columns="pair", values=col).reindex(columns=tags)
                for uid, row in piv.iterrows():
                    ax.plot(range(len(tags)), row.to_numpy(float), marker="o", ms=3.5, lw=1, color="0.7")
                mu = [mean_sem(piv[t])[:2] for t in tags]
                ax.errorbar(range(len(tags)), [m[0] for m in mu], yerr=[m[1] for m in mu], marker="o", lw=2, capsize=3, color=CLASS_COLORS[gname])
                ax.axhline(5, color="0.5", ls=":", lw=.8)
                ax.set_xticks(range(len(tags))); ax.set_xticklabels([t.replace("_vs_", " vs ") for t in tags], rotation=35, ha="right", fontsize=8)
                if r_ == 0: ax.set_title(f"{gname.upper()} cells")
                if c_ == 0: ax.set_ylabel(f"% cells with significant\n{lab} shift (q<0.05)")
                ax.spines[["top", "right"]].set_visible(False)
        fig.suptitle(f"{area}: per-cell BF-shift permutation test (level labels shuffled within frequency; BH within FOV and pair)\n"
                     "gray = one FOV; denominator = cells BF-eligible at both levels", fontsize=11)
        fig.tight_layout(rect=[0, 0, 1, .93]); fig.savefig(root / "BF_shift_permutation_significance.png", dpi=220); plt.close(fig)

    # 8. Threshold and CF vs BF at the reference level.
    if "threshold_level_db" in cells and "cf_hz" in cells:
        s = cells[cells.threshold_level_db.notna()]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
        for k, cls in enumerate(CELL_CLASSES):
            v = s.loc[s.cell_class == cls, "threshold_level_db"].to_numpy(float)
            if len(v):
                frac = [np.mean(np.isclose(v, lv)) for lv in levels]
                ax1.bar(np.arange(len(levels)) + (k - .5) * .38, frac, width=.38, color=CLASS_COLORS[cls], label=f"{cls.upper()} n={len(v)}")
        ax1.set_xticks(range(len(levels))); ax1.set_xticklabels([f"{lv:g}" for lv in levels]); ax1.set_xlabel("Response threshold (dB SPL)")
        ax1.set_ylabel("Fraction of cells with an excitatory response"); ax1.legend(frameon=False)
        ax1.set_title(f"Lowest level with a significant excitatory response\n(threshold at {levels[0]:g} dB means <= {levels[0]:g} dB)")
        rcol = f"{lp(ref)}_best_frequency_hz"; ecol = f"{lp(ref)}_bf_eligible"
        if rcol in s and len(all_freqs):
            s2 = s[s[ecol].fillna(False).astype(bool) & s.cf_hz.notna()]; rng = np.random.default_rng(9)
            for cls in CELL_CLASSES:
                q = s2[s2.cell_class == cls]
                ax2.scatter(np.log2(q[rcol]/1000) + rng.uniform(-.07, .07, len(q)), np.log2(q.cf_hz/1000) + rng.uniform(-.07, .07, len(q)),
                            s=10, alpha=.5, color=CLASS_COLORS[cls], edgecolors="none", label=f"{cls.upper()} n={len(q)}")
            lo, hi = np.log2(all_freqs[0]/1000) - .3, np.log2(all_freqs[-1]/1000) + .3
            ax2.plot([lo, hi], [lo, hi], color="0.6", ls="--", lw=1); ax2.set_xlim(lo, hi); ax2.set_ylim(lo, hi)
            tk = all_freqs[::3]; ax2.set_xticks(np.log2(tk/1000)); ax2.set_xticklabels([f"{v/1000:.3g}" for v in tk])
            ax2.set_yticks(np.log2(tk/1000)); ax2.set_yticklabels([f"{v/1000:.3g}" for v in tk])
            d = np.log2(s2.cf_hz / s2[rcol]); r = wilcoxon_vs_zero(d)
            ax2.text(.03, .97, f"CF - BF({ref:g} dB): median {_fmt(r['median'], '+.2f')} oct\npooled-cell Wilcoxon p={_fmt(r['p'])} (exploratory)",
                     transform=ax2.transAxes, va="top", fontsize=8.5)
            ax2.set_xlabel(f"BF at {ref:g} dB (kHz)"); ax2.set_ylabel("CF (kHz; best significant frequency at threshold)"); ax2.legend(frameon=False, loc="lower right")
            st["cf_minus_reference_bf_oct_pooled_cells"] = r
        fig.suptitle(f"{area}: response threshold and characteristic frequency", fontsize=12); fig.tight_layout(rect=[0, 0, 1, .94])
        fig.savefig(root / "threshold_and_CF.png", dpi=220); plt.close(fig)

    save_json(root / "BF_across_levels_statistics.json", st)
    return st


def write_report(path: Path, cells: pd.DataFrame, levels: list[float], ref: float, resp_stats: dict[str, Any],
                 per_level_bf: dict[str, Any], lvl_stats: dict[str, Any], n_shift_perm: int) -> None:
    lines = [f"PURE-TONE LEVEL SERIES — FOV ANALYSIS {SCRIPT_VERSION}", "=" * 72, "",
             f"Levels: {', '.join(f'{lv:g}' for lv in levels)} dB SPL | reference level for shifts: {ref:g} dB",
             f"FOVs: {cells['fov_uid'].nunique()} | cell rows: {len(cells)}",
             "Responsiveness: per-frequency sign-flip tests, BH-FDR across cells at each frequency; union across frequencies.",
             f"BF-eligible: {lvl_stats.get('bf_eligible_definition', '')}.",
             f"BF-shift permutation test: {n_shift_perm} level-label shuffles within frequency; BH across cells per FOV and pair.", ""]
    for uid, g in cells.groupby("fov_uid"):
        lines.append(f"  {uid} ({g.brainArea.iloc[0]}, depth {g.depth.iloc[0]:.0f} um): levels {g.levels_recorded_db.iloc[0]} dB, "
                     f"n={len(g)} (GREEN {int((g.cell_class == GREEN).sum())}, YELLOW {int((g.cell_class == YELLOW).sum())})")
    if not cells["red_channel_recorded"].any():
        lines += ["", "No red channel recorded (nchannels = 1): every cell is labeled GREEN, GREEN/YELLOW comparisons skipped."]
    else:
        lines += ["", "GREEN vs YELLOW % responsive per level (paired Wilcoxon across FOVs; Holm across levels):"]
    for lv, r in resp_stats.items():
        lines.append(f"  {lv}: W={_fmt(r.get('W'))}, p={_fmt(r.get('p'))}, Holm p={_fmt(r.get(f'p_holm_{len(resp_stats)}_levels'))}, n={r.get('n_pairs', 0)}")
    lines += ["", "BF across FOVs at each level (Kruskal-Wallis, cells = units; see per_level/<N>dB/best_frequency_across_FOVs/):"]
    for lv, bs in per_level_bf.items():
        r = bs.get("all", {}).get("kruskal_wallis_across_FOVs", {})
        lines.append(f"  {lv}: H={_fmt(r.get('H'))}, p={_fmt(r.get('p'))}, nFOV={r.get('n_fovs_with_cells', 0)}, n={r.get('n_cells', 0)}")
    lines += ["", f"BF shift re {ref:g} dB (FOV medians vs 0, Wilcoxon; Holm across levels):"]
    for lab, byg in lvl_stats.get("shift_vs_reference", {}).items():
        for g, bylv in byg.items():
            for lv, r in bylv.items():
                lines.append(f"  [{lab}] {g} {lv}: median of FOV medians={_fmt(r.get('median'), '+.3f')} oct, p={_fmt(r.get('p'))}, "
                             f"n={r.get('n')}; pooled cells p={_fmt(r.get('pooled_cells_exploratory', {}).get('p'))} (exploratory)")
    lines += ["", "BF-vs-level slope (octaves per 10 dB):"]
    for lab, r in lvl_stats.get("slope", {}).items():
        for g in CELL_GROUPS:
            rr = r["across_FOV_medians_vs_0"][g]
            lines.append(f"  [{lab}] {g}: median of FOV medians={_fmt(rr.get('median'), '+.3f')}, p={_fmt(rr.get('p'))}, nFOV={rr.get('n')}")
        if YELLOW in CELL_GROUPS:
            gy = r["GREEN_vs_YELLOW_paired_FOV"]
            lines.append(f"  [{lab}] GREEN vs YELLOW paired FOVs: p={_fmt(gy.get('p'))}, n={gy.get('n_pairs')}")
    lines += ["", "Note: with few FOVs the across-FOV tests have little power (4 FOVs: two-sided Wilcoxon p >= 0.125).",
              "Within-FOV and pooled-cell results are in best_frequency_across_levels/*.csv and *_statistics.json."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args = parse_args(); subject = str(args.subject); dates = [str(x) for x in args.dates]; area = str(args.area)
    info_path, sessions = load_info2p(subject)
    skipped: list[dict[str, Any]] = []
    selected = select_level_sessions(sessions, dates, area, subject, parse_session_filter(args.sessions),
                                     parse_session_filter(args.exclude_sessions), skipped)
    if not selected:
        raise RuntimeError(f"No pure-tone sound_tuning sessions found for {subject}, area={area}, dates={dates}")
    assigned = assign_fovs(selected)
    manifest = pd.DataFrame(validate_fov_groups(assigned))
    levels = sorted(manifest.level_db.unique().tolist())
    ref = float(args.reference_level) if args.reference_level is not None else float(levels[-1])
    if ref not in levels:
        raise ValueError(f"--reference-level {ref:g} is not one of the recorded levels {levels}")
    od = output_dirs(subject, area, dates)
    manifest.to_csv(od["root"] / "fov_manifest.csv", index=False)
    print("=" * 86); print(f"PURE-TONE LEVEL SERIES — FOV ANALYSIS {SCRIPT_VERSION}"); print("=" * 86)
    print(f"Subject: {subject} | area: {area} | dates: {dates}")
    print(f"info2p: {info_path}"); print(f"Output: {od['root']}")
    print(f"Levels: {levels} dB | reference level: {ref:g} dB")
    print(manifest[["date", "FOV#", "session", "level_db", "level_source", "sessionLabel", "brainArea", "depth", "n_levels_in_FOV"]].to_string(index=False))
    save_json(od["root"] / "run_manifest.json", {
        "script_version": SCRIPT_VERSION, "analysis_branch": "pure-tone level series",
        "based_on": "sound_tuning_multistim_dualF0_fov_analysis_v1.py (pure-tone parts)",
        "subject": subject, "dates": dates, "area": area, "plane": args.plane, "levels_db": levels, "reference_level_db": ref,
        "info2p_file": str(info_path), "TEMP_OUTPUT_PATH": str(settings.TEMP_OUTPUT_PATH),
        "FOV_field": "FOV#", "primary_replicate": "FOV",
        "responsiveness": "per-frequency sign-flip + per-frequency BH-FDR across cells; union",
        "bf_eligible": "responsive, response at BF > 0, q at BF < 0.05",
        "n_permutations": args.n_permutations, "n_shift_permutations": args.n_shift_permutations, "seed": args.seed,
        "sessions_filter": args.sessions, "exclude_sessions": args.exclude_sessions, "skipped_sessions": skipped,
    })
    if args.dry_run:
        print("Dry run complete."); return

    groups: dict[str, list[dict[str, Any]]] = {}
    for s in assigned: groups.setdefault(s["fov_uid"], []).append(s)
    cell_tables = []; failures = []
    for gi, (uid, seq) in enumerate(sorted(groups.items())):
        fd = od["fov"] / uid; fd.mkdir(parents=True, exist_ok=True)
        print("\n" + "-" * 86); print(f"FOV {uid}: {[x['session'] + ':' + level_tag(x['level_db']) for x in seq]}")
        try:
            df, _ = analyze_fov(seq, args.plane, fd, max(64, int(args.n_permutations)), max(100, int(args.n_shift_permutations)),
                                int(args.seed) + 10000 * gi, not args.skip_cell_reports)
            cell_tables.append(df)
        except Exception as exc:
            failures.append({"fov_uid": uid, "error": repr(exc), "traceback": traceback.format_exc()})
            print(f"FAILED {uid}: {exc}")
    save_json(od["root"] / "failures.json", failures)
    if not cell_tables:
        raise RuntimeError("No FOV completed successfully; see failures.json")
    cells = pd.concat(cell_tables, ignore_index=True, sort=False)
    global CELL_GROUPS
    red_fovs = cells.groupby("fov_uid")["red_channel_recorded"].first()
    if not red_fovs.any():
        CELL_GROUPS = ("all",)
        print("No FOV recorded a red channel: GREEN/YELLOW comparisons skipped; summaries use all cells.")
    elif not red_fovs.all():
        print(f"WARNING: FOVs without a red channel ({list(red_fovs[~red_fovs].index)}) have every cell labeled GREEN; "
              "their GREEN cells are unclassified, not tdTomato-negative.")
    cells.to_csv(od["combined"] / "combined_cell_results.csv", index=False)
    long = long_level_table(cells, levels)
    long.to_csv(od["combined"] / "combined_cell_level_results.csv", index=False)

    per_level_bf = {}
    for lv in levels:
        view = level_view(cells, lv)
        if view.empty: continue
        d = od["combined"] / "per_level" / level_tag(lv); d.mkdir(parents=True, exist_ok=True)
        save_combined_bf_outputs(view, d, f" — {lv:g} dB")
        per_level_bf[level_tag(lv)] = plot_bf_across_fovs(view, area, d, f" — {lv:g} dB")
    fsum = fov_level_summary(long)
    resp_stats = {}
    if red_fovs.any():
        resp_stats = plot_responsiveness_by_level(fsum, levels, od["combined"])
        save_json(od["combined"] / "responsiveness_statistics.json", resp_stats)
    lvl_stats = analyze_bf_across_levels(cells, long, levels, ref, area, od["combined"])
    write_report(od["combined"] / "REPORT.txt", cells, levels, ref, resp_stats, per_level_bf, lvl_stats, args.n_shift_permutations)
    print("\n" + "=" * 86); print("DONE"); print(f"Successful FOVs: {len(cell_tables)}; failed: {len(failures)}"); print(f"Outputs: {od['root']}")


if __name__ == "__main__":
    main()
