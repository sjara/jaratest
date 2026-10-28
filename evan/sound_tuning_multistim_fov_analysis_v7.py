#!/usr/bin/env python3
"""
v7 = v6 plus per-cell BF / selectivity notes on every single-cell panel (statistics,
response definitions and trial archives are unchanged from v6):
    * Pure-tone sessions at other levels in the same FOV are no longer dropped. The level
      chosen as the pure_tones block is unchanged (--pure-tone-level / v6 default); each
      other level is analyzed the same way into fov_outputs/<FOV>/pure_tones_other_levels/
      <N>dB/ (own archive, raster, tuning pages) and merged as pure_<N>dB_* columns.
    * BF eligibility as in the level-series branch and quick_bf_check_v1.py:
      pure_bf_eligible = responsive (FDR) & response at BF > 0 & q at BF < 0.05, plus
      pure_q_at_bf (and pure_<N>dB_bf_eligible / pure_<N>dB_q_at_bf for other levels).
    * Every individual_tuning_pages panel and every cell_reports tuning panel gets a note:
      the cell's BF at each pure-tone level ("n.s." = not BF-eligible at that level), the
      BF offset in octaves from that sound's center frequency / chord F0 (primary level),
      and its selectivity index (noise pairs also the per-cell novelty-test q). Tuning
      pages are therefore drawn after all blocks of the FOV are merged.

v6 = v5 plus three new sound blocks and automatic block detection (pure_tones, chord_tones
and fm_tones are analyzed exactly as in v5):
    * fm_range (column prefix fmr_): FM sweeps over a fixed frequency range
      (behavior stim type FM_fixed_range; condition = signed slope, oct/s). The sound
      lasts as long as the sweep (octave_range / |slope|), so the slowest sweeps outlast
      the usual 0-1 s window. Metrics as for fm_tones (direction selectivity, best slope,
      speed sparseness).
    * band_noise (bn_): AM band noise at a fixed center frequency (Band_noise; condition
      = bandwidth in octaves). Bandwidth selectivity
      SI_bw = (R_widest - R_narrowest) / (|R_widest| + |R_narrowest|), +1 = prefers broadband.
    * noise_pair (np_): two 0.1-s sounds, A = narrow band noise, B = white noise, in the
      orders AB, BA, AA, BB at several gaps (Noise_pair; condition code =
      10 x order index + gap in s, see NOISEPAIR_ORDERS). Novelty selectivity
      SI_nov = (R_diff - R_same) / (|R_diff| + |R_same|), R_diff = mean(AB, BA),
      R_same = mean(AA, BB). Both sides contain one A and one B as the first sound, so
      under linear summation the first-sound responses cancel and SI_nov measures how
      much more the cell responds to a second sound that differs from the first
      (stimulus-specific adaptation). Also per gap, and the first-sound preference
      SI_first = (mean(AA, AB) - mean(BA, BB)) / (...), +1 = prefers band noise A.
    * The block type comes from the behavior file's current_stim_type (the sessionLabel
      is only a cross-check), so labels like fm_sounds_frange_60dB / band_noise_60dB /
      noise_pair_60dB / pure_tones_65dB need no alias. Sessions without a behavior file
      are skipped and listed in run_manifest.json.
    * When an FOV has pure-tone sessions at several levels (a level series), one level is
      used as this FOV's pure_tones block: --pure-tone-level, or by default the level
      recorded in the most FOVs (ties: closest to the median level of the other blocks).
      The level series itself is analyzed by sound_tuning_pure_tone_levels_fov_analysis_v2.py.
    * Event alignment uses each trial's real sound duration (fm_range: sweep duration;
      noise_pair: 2 x sound duration + gap). The behavior file's stim_duration is the GUI
      value and is wrong for these blocks.
    * Response window is per block (BLOCK_RESPONSE_RANGE): 0-1.4 s for fm_range and
      noise_pair, whose sounds last up to 1.2 s / 1.0 s; 0-1 s for every other block.
      The fm_range / noise_pair selectivity indices are also saved for the standard 0-1 s
      window (*_win0to1) as a sensitivity check. Baseline stays -1-0 s.
    * Recordings without a red channel (nchannels = 1) are handled as in the level-series
      branch: every cell is GREEN (= unclassified), red_channel_recorded = False, and the
      combined GREEN-vs-YELLOW figures are replaced by all-cell figures with per-FOV
      tests of each selectivity index against 0.
    * --sessions / --exclude-sessions, --skip-cell-reports. Cell reports show only the
      blocks recorded in that FOV (one row each).
    * Fixed-duration FM files written after the FMfixeddur_ rename are read as fm_tones.
Stages 2/3 (v6) do not know the new blocks yet; their pure/chord/FM results are unchanged.

FOV-aware analysis of the new sound_tuning blocks:
    pure_tones, chord_tones, fm_tones/fm_sounds, fm_range, band_noise, and noise_pair.

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
python sound_tuning_multistim_fov_analysis_v7.py imag039 \
    --area A1 --dates 20260910

python sound_tuning_multistim_fov_analysis_v7.py imag041 \
    --area A1 --dates 20261015 --sessions 003 005-011 014 016-018

Legacy explicit grouping example (only needed before FOV# is added to info2p):
python sound_tuning_multistim_fov_analysis_v7.py imag039 \
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

SCRIPT_VERSION = "v7"
PARADIGM = "sound_tuning"
BLOCK_ALIASES = {
    "pure_tones": "pure_tones",
    "pure_tone": "pure_tones",
    "chord_tones": "chord_tones",
    "chord_3t": "chord_tones",
    "fm_tones": "fm_tones",
    "fm_sounds": "fm_tones",
    "fm_sounds_fdur": "fm_tones",
    "fm": "fm_tones",
    "fm_sounds_frange": "fm_range",
    "fm_range": "fm_range",
    "fm_fixed_range": "fm_range",
    "band_noise": "band_noise",
    "bandnoise": "band_noise",
    "noise_pair": "noise_pair",
    "noisepair": "noise_pair",
}
# Behavior-file stim types (current_stim_type menu) -> block. AM_noise / Fading_noise belong
# to sound_tuning_area_analysis_v13.py and are not analyzed here.
STIM_TYPE_BLOCK = {
    "Pure_tone": "pure_tones", "Chord_3t": "chord_tones", "FM": "fm_tones", "FM_fixed_dur": "fm_tones",
    "FM_fixed_range": "fm_range", "Band_noise": "band_noise", "Noise_pair": "noise_pair",
}
BLOCK_ORDER = ("pure_tones", "chord_tones", "fm_tones", "fm_range", "band_noise", "noise_pair")
BLOCK_SHORT = {"pure_tones": "pure", "chord_tones": "chord", "fm_tones": "fm",
               "fm_range": "fmr", "band_noise": "bn", "noise_pair": "np"}
BLOCK_LABEL = {"pure_tones": "Pure tones", "chord_tones": "3-tone chords", "fm_tones": "FM sweeps",
               "fm_range": "FM sweeps (fixed range)", "band_noise": "Band noise", "noise_pair": "Noise pairs"}
FM_BLOCKS = ("fm_tones", "fm_range")
# Behavior field holding the block's center frequency (band noise / noise pair: center of band A).
CENTER_FREQ_FIELD = {"fm_range": "FMfixedrange_center_freq", "band_noise": "bandnoise_center_freq",
                     "noise_pair": "noisepair_center_freq"}
LEVEL_SUFFIX_RE = re.compile(r"_\d+(?:\.\d+)?\s*db(?:_?spl)?$", re.IGNORECASE)

# Noise-pair condition code = 10 * order index + gap (s); gaps must be < 10 s.
NOISEPAIR_ORDERS = ("A_then_B", "B_then_A", "A_then_A", "B_then_B")
NOISEPAIR_SHORT = {"A_then_B": "AB", "B_then_A": "BA", "A_then_A": "AA", "B_then_B": "BB"}

TIME_RANGE = (-1.0, 1.5)
BASELINE_RANGE = (-1.0, 0.0)
RESPONSE_RANGE = (0.0, 1.0)
# fm_range sounds last up to octave_range/|slope_min| (1.2 s for 6 octaves at 5 oct/s) and
# noise pairs up to 2 x 0.1 + 0.8 = 1.0 s. With ISI >= 1.4 s, 1.4 s after onset is the latest
# end that never reaches the next trial's sound.
BLOCK_RESPONSE_RANGE = {"fm_range": (0.0, 1.4), "noise_pair": (0.0, 1.4)}
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
CLASS_COLORS = {GREEN: "tab:green", YELLOW: "goldenrod", "all": "0.35"}
AREA_COLORS = {"A1": "tab:blue", "AAF": "tab:orange", "A2": "tab:purple"}
# Set in main(): False when no FOV in the run recorded a red channel (every cell GREEN = unclassified).
RED_RECORDED = True

SELECTIVITY_SPEC = {
    "pure_tones": {
        "metric": "pure_lifetime_sparseness",
        "label": "Pure-tone selectivity (lifetime sparseness)",
        "symbol": r"$S_{life}$",
        "equation": r"$S_{life}=\frac{1-(\overline{|R|})^2/\overline{|R|^2}}{1-1/n}$",
        "ylim": (-0.05, 1.05),
        "folder": "pure_tones",
    },
    "chord_tones": {
        "metric": "chord_harmonic_selectivity",
        "label": "Chord harmonic selectivity",
        "symbol": r"$SI_{harm}$",
        "equation": r"$SI_{harm}=\frac{R_{harm}-\overline{R}_{nonharm}}{|R_{harm}|+|\overline{R}_{nonharm}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "chord_tones",
    },
    "fm_tones": {
        "metric": "fm_direction_selectivity",
        "label": "FM direction selectivity",
        "symbol": r"$SI_{dir}$",
        "equation": r"$SI_{dir}=\frac{\overline{R}_{up}-\overline{R}_{down}}{|\overline{R}_{up}|+|\overline{R}_{down}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "fm_sounds",
    },
    "fm_range": {
        "metric": "fmr_direction_selectivity",
        "label": "FM fixed-range direction selectivity",
        "symbol": r"$SI_{dir}$",
        "equation": r"$SI_{dir}=\frac{\overline{R}_{up}-\overline{R}_{down}}{|\overline{R}_{up}|+|\overline{R}_{down}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "fm_range",
    },
    "band_noise": {
        "metric": "bn_bandwidth_selectivity",
        "label": "Band-noise bandwidth selectivity",
        "symbol": r"$SI_{bw}$",
        "equation": r"$SI_{bw}=\frac{R_{widest}-R_{narrowest}}{|R_{widest}|+|R_{narrowest}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "band_noise",
    },
    "noise_pair": {
        "metric": "np_novelty_selectivity",
        "label": "Noise-pair novelty selectivity",
        "symbol": r"$SI_{nov}$",
        "equation": r"$SI_{nov}=\frac{\overline{R}_{AB,BA}-\overline{R}_{AA,BB}}{|\overline{R}_{AB,BA}|+|\overline{R}_{AA,BB}|}$",
        "ylim": (-1.05, 1.05),
        "folder": "noise_pair",
    },
}


def response_range(block: str) -> tuple[float, float]:
    return BLOCK_RESPONSE_RANGE.get(block, RESPONSE_RANGE)


def plot_groups() -> tuple[str, ...]:
    """Cell groups for combined figures: GREEN/YELLOW, or all cells when no red channel was recorded."""
    return CELL_CLASSES if RED_RECORDED else ("all",)


def group_mask(cell_class: Any, group: str) -> np.ndarray:
    cc = np.asarray(cell_class)
    return np.ones(len(cc), bool) if group == "all" else (cc == group)


def group_label(group: str) -> str:
    if group == "all":
        return "ALL CELLS (no red channel)"
    return group.upper() if RED_RECORDED else f"{group.upper()} (unclassified)"


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
    key = LEVEL_SUFFIX_RE.sub("", str(value).strip().lower())
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
    p.add_argument("--sessions", nargs="+", default=None, metavar="SESSION",
                   help="analyze only these sessions: 001, 20261015_001, or a range 001-004")
    p.add_argument("--exclude-sessions", nargs="+", default=None, metavar="SESSION",
                   help="drop these sessions (same forms as --sessions)")
    p.add_argument("--pure-tone-level", type=float, default=None,
                   help=("dB SPL of the pure-tone session used in FOVs with several pure-tone levels "
                         "(default: the level recorded in the most FOVs)"))
    p.add_argument("--skip-cell-reports", action="store_true", help="skip the per-cell report PNGs (slow)")
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


def inspect_behavior_session(subject: str, date: str, session: str) -> dict[str, Any]:
    """Sound type(s), block, and level stored in one sound_tuning behavior file.

    status: 'ok', 'no_behavior' (file missing), 'mixed' (several stim types in one session),
    'unsupported' (stim type not analyzed here), or 'no_stim_type' (no current_stim_type field).
    """
    path = Path(loadbehavior.path_to_behavior_data(subject, PARADIGM, f"{date}_{session}"))
    rec: dict[str, Any] = {"behavior_path": str(path), "stim_types": [], "detected_block": None,
                           "level_db": np.nan, "n_trials": 0}
    if not path.exists():
        return {**rec, "status": "no_behavior"}
    bdata = loadbehavior.BehaviorData(str(path))
    if "current_stim_type" not in bdata:
        return {**rec, "status": "no_stim_type"}
    codes = np.asarray(bdata["current_stim_type"]).ravel()
    labels = bdata.labels.get("current_stim_type", {}) if hasattr(bdata, "labels") else {}
    names = sorted({str(labels.get(int(c), int(c))) for c in np.unique(codes)})
    rec["stim_types"] = names; rec["n_trials"] = int(len(codes))
    if "current_intensity" in bdata:
        lv = finite(bdata["current_intensity"])
        if len(lv):
            rec["level_db"] = float(np.median(lv))
    if len(names) != 1:
        return {**rec, "status": "mixed"}
    block = STIM_TYPE_BLOCK.get(names[0])
    if block is None:
        return {**rec, "status": "unsupported"}
    rec["detected_block"] = block
    if block == "chord_tones" and "chord3t_F0" in bdata:
        rec["chord_F0_hz"] = float(np.nanmedian(np.asarray(bdata["chord3t_F0"], float)))
    center_field = CENTER_FREQ_FIELD.get(block)
    if center_field and center_field in bdata:
        rec["center_frequency_hz"] = float(np.nanmedian(np.asarray(bdata[center_field], float)))
    return {**rec, "status": "ok"}


def select_new_sound_sessions(sessions: list[dict[str, Any]], dates: list[str], area: str, subject: str,
                              include: set | None = None, exclude: set | None = None,
                              skipped: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Sessions of this paradigm/area/date whose behavior file holds one analyzable sound block.

    The block comes from the behavior file; the sessionLabel is used only when the file has no
    current_stim_type field (older paradigm versions), and a disagreement is printed.
    """
    dset = set(map(str, dates))
    out = []
    for s in sessions:
        if not (str(s.get("date", "")) in dset and str(s.get("paradigm", "")) == PARADIGM
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
        label_block = canonical_block(s.get("sessionLabel", ""))
        info = inspect_behavior_session(subject, q["date"], q["session"])
        block = info["detected_block"] if info["status"] == "ok" else (label_block if info["status"] == "no_stim_type" else None)
        if block is None:
            if skipped is not None and (label_block is not None or info["status"] != "unsupported"):
                skipped.append({"date": q["date"], "session": q["session"], "sessionLabel": s.get("sessionLabel"),
                                "status": info["status"], "stim_types": info["stim_types"]})
            if label_block is not None or info["status"] in ("mixed", "no_behavior"):
                print(f"WARNING: skipping {q['date']}_{q['session']} ({s.get('sessionLabel')}): {info['status']} {info['stim_types']}")
            continue
        if label_block is not None and label_block != block:
            print(f"WARNING: {q['date']}_{q['session']}: sessionLabel {s.get('sessionLabel')!r} suggests {label_block}, "
                  f"behavior file says {block}; using {block}")
        q["block_type"] = block
        q["label_block"] = label_block
        q["block_source"] = "behavior" if info["status"] == "ok" else "sessionLabel"
        q["level_db"] = info["level_db"]
        q["behavior_info"] = info
        out.append(q)
    out.sort(key=lambda x: (x["date"], x["session"]))
    return out


def choose_pure_tone_level(selected: list[dict[str, Any]], requested: float | None) -> float | None:
    """Level used as the pure_tones block in FOVs with pure tones at several levels."""
    pure = [s for s in selected if s["block_type"] == "pure_tones" and np.isfinite(s.get("level_db", np.nan))]
    if requested is not None:
        return float(requested)
    fov_levels: dict[tuple, set] = {}
    for s in pure:
        fov_levels.setdefault(s["fov_uid"], set()).add(float(s["level_db"]))
    if not any(len(v) > 1 for v in fov_levels.values()):
        return None
    counts: dict[float, int] = {}
    for v in fov_levels.values():
        for lv in v:
            counts[lv] = counts.get(lv, 0) + 1
    other = finite([s.get("level_db", np.nan) for s in selected if s["block_type"] != "pure_tones"])
    target = float(np.median(other)) if len(other) else max(counts)
    return sorted(counts, key=lambda lv: (-counts[lv], abs(lv - target), -lv))[0]


def split_pure_tone_levels(assigned: list[dict[str, Any]], level: float | None
                           ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """In each FOV with several pure-tone sessions the one closest to `level` is the pure_tones block.

    Returns (sessions analyzed as blocks, other-level pure-tone sessions). The other levels are
    analyzed for per-cell BF only (pure_<N>dB_* columns), see merge_fov_blocks().
    """
    if level is None:
        return assigned, []
    by_fov: dict[str, list[dict[str, Any]]] = {}
    for s in assigned:
        if s["block_type"] == "pure_tones":
            by_fov.setdefault(s["fov_uid"], []).append(s)
    drop = set()
    for uid, seq in by_fov.items():
        if len(seq) < 2:
            continue
        keep = min(seq, key=lambda s: (abs(float(s.get("level_db", np.inf)) - level), s["session"]))
        for s in seq:
            if s is not keep:
                drop.add((s["date"], s["session"]))
    return ([s for s in assigned if (s["date"], s["session"]) not in drop],
            [s for s in assigned if (s["date"], s["session"]) in drop])


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
            raise ValueError(f"FOV {uid} contains duplicate block types: {list(zip([s['session'] for s in seq], blocks))}. "
                             "Two chord F0s per FOV: use sound_tuning_multistim_dualF0_fov_analysis_v1.py; "
                             "otherwise select sessions with --sessions / --exclude-sessions.")
        for s in seq:
            rows.append({
                "subject": s.get("subject"), "date": s["date"], "FOV#": int(s["fov_number"]),
                "fov_uid": uid, "session": s["session"], "block_type": s["block_type"],
                "block_source": s.get("block_source"), "label_block": s.get("label_block"),
                "level_db": s.get("level_db"),
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

def _selectivity_equation_box(ax, block, fontsize=15.0):
    """Draw the selectivity equation in a blank side panel, directly under any statistics text already there."""
    spec = SELECTIVITY_SPEC[block]
    ax.axis("off")
    box = dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="0.75", alpha=0.98)
    if ax.texts:
        ax.annotate(spec["equation"], xy=(0.5, 0.0), xycoords=ax.texts[-1], xytext=(0, -18), textcoords="offset points",
                    ha="center", va="top", fontsize=fontsize, bbox=box)
    else:
        ax.text(0.5, 0.5, spec["equation"], transform=ax.transAxes, ha="center", va="center", fontsize=fontsize, bbox=box)


def _format_cell_selectivity(block, value):
    """Compact per-cell selectivity label for tuning panels."""
    symbol = SELECTIVITY_SPEC[block].get("symbol", "SI")
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = np.nan
    if not np.isfinite(value):
        return f"{symbol} = NA"
    if block == "pure_tones":
        return f"{symbol} = {value:.3f}"
    return f"{symbol} = {value:+.3f}"

def _bf_level_prefixes(base):
    """[(level dB, column prefix)] for the pure-tone levels present: the pure_tones block first, then other levels."""
    out = []
    if "pure_best_frequency_hz" in base:
        lv = pd.to_numeric(base.get("pure_tones_level_db", pd.Series([np.nan])), errors="coerce").iloc[0]
        out.append((lv, "pure_"))
    lvs = sorted({float(m.group(1)) for c in base.columns for m in [re.match(r"pure_(\d+(?:\.\d+)?)dB_best_frequency_hz$", c)] if m})
    return out + [(lv, f"pure_{lv:g}dB_") for lv in lvs]


def _block_center(block, block_meta):
    """(name, Hz) of the frequency a block was centered on, or None."""
    m = block_meta.get(block, {})
    key = {"chord_tones": ("F0", "F0_hz"), "fm_range": ("FM center", "center_frequency_hz"),
           "band_noise": ("band center", "center_frequency_hz"), "noise_pair": ("A center", "A_center_frequency_hz")}.get(block)
    if key is None or not np.isfinite(float(m.get(key[1], np.nan))):
        return None
    return key[0], float(m[key[1]])


def _cell_bf_note(row, block, levels, block_meta):
    """One-line BF note for a single-cell panel: BF per level, and BF offset from the block's center (primary level)."""
    def bf_at(pre):
        bf = pd.to_numeric(pd.Series([row.get(f"{pre}best_frequency_hz", np.nan)]), errors="coerce").iloc[0]
        ok = row.get(f"{pre}bf_eligible", False)
        return float(bf) if (pd.notna(ok) and bool(ok) and np.isfinite(bf)) else np.nan
    if not levels:
        return ""
    parts = []
    for lv, pre in levels:
        bf = bf_at(pre); lab = f"{lv:g} dB " if np.isfinite(lv) else ""
        parts.append(f"{lab}{bf/1000:.3g} kHz" if np.isfinite(bf) else f"{lab}n.s.")
    note = "BF: " + " · ".join(parts)
    center = _block_center(block, block_meta); bf0 = bf_at(levels[0][1])
    if center is not None and np.isfinite(bf0):
        note += f"\nBF re {center[0]} ({center[1]/1000:.3g} kHz): {np.log2(bf0/center[1]):+.2f} oct"
    return note


def _cell_selectivity_note(row, block, metric_col=None):
    txt = _format_cell_selectivity(block, row.get(metric_col or SELECTIVITY_SPEC[block]["metric"], np.nan))
    if block == "noise_pair":
        q = pd.to_numeric(pd.Series([row.get("np_novelty_q", np.nan)]), errors="coerce").iloc[0]
        if np.isfinite(q): txt += f" (novelty test q={q:.2g})"
    return txt


def _readable_condition_ticks(ax, x, labels, dense_threshold=10):
    """Readable condition labels: dense axes label every other tick, rotated ~60 deg."""
    x=np.asarray(x,float); labels=list(labels)
    ax.set_xticks(x)
    if len(labels)>=dense_threshold:
        shown=[lab if (i%2==0) else "" for i,lab in enumerate(labels)]
        ax.set_xticklabels(shown, rotation=60, ha="right", rotation_mode="anchor")
    else:
        ax.set_xticklabels(labels, rotation=45 if len(labels)>6 else 0, ha="right" if len(labels)>6 else "center")


def noisepair_code(order_name: str, gap: float) -> float:
    return 10.0 * NOISEPAIR_ORDERS.index(order_name) + round(float(gap), 6)


def noisepair_decode(code: Any) -> tuple[np.ndarray, np.ndarray]:
    """(order index, gap in s) from noise-pair condition codes."""
    c = np.asarray(code, float)
    oi = np.floor(np.round(c, 6) / 10.0).astype(int)
    return oi, np.round(c - 10.0 * oi, 6)


def _condition_axis(block, values):
    values=np.asarray(values,float)
    if block=="pure_tones":
        x=np.log2(values/1000.0); labels=[f"{v/1000:.3g}" for v in values]; xlabel="Frequency (kHz; log2 spacing)"
    elif block=="chord_tones":
        x=values; labels=[f"{v:.3g}" for v in values]; xlabel="Middle tone position (octaves above F0)"
    elif block=="band_noise":
        x=np.log2(values); labels=[f"{v:.3g}" for v in values]; xlabel="Bandwidth (octaves; log2 spacing)"
    elif block=="noise_pair":
        oi,gap=noisepair_decode(values); gaps=np.sort(np.unique(gap))
        x=oi*(len(gaps)+1)+np.searchsorted(gaps,gap).astype(float)
        labels=[f"{NOISEPAIR_SHORT[NOISEPAIR_ORDERS[o]]} {g:g}" for o,g in zip(oi,gap)]; xlabel="Order and gap (s)"
    else:
        x=_fm_log_positions(values); labels=[f"{v:g}" for v in values]; xlabel="FM slope (octaves/s; signed log2-magnitude spacing)"
    return x,labels,xlabel


def _condition_tick_labels(block, values):
    return _condition_axis(block, values)[1]


def _plot_condition_curve(ax, block, x, y, yerr=None, label=None, **kw):
    """Tuning curve; noise pairs are drawn as one line per order (orders are not a continuum)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if block != "noise_pair":
        if yerr is None:
            ax.plot(x, y, marker="o", lw=1.8, label=label, **kw)
        else:
            ax.errorbar(x, y, yerr=yerr, marker="o", lw=1.8, capsize=3, label=label, **kw)
        return
    # Orders occupy blocks of n_gaps + 1 positions; a jump > 1 starts a new order.
    breaks = np.r_[0, np.flatnonzero(np.diff(x) > 1.5) + 1, len(x)]
    for k, (a, b) in enumerate(zip(breaks[:-1], breaks[1:])):
        if yerr is None:
            ax.plot(x[a:b], y[a:b], marker="o", lw=1.8, label=label if k == 0 else None, **kw)
        else:
            ax.errorbar(x[a:b], y[a:b], yerr=np.asarray(yerr, float)[a:b], marker="o", lw=1.8, capsize=3,
                        label=label if k == 0 else None, **kw)


def _cell_scalar_sem(trial_response, cond_trial, valid, cell_index, values):
    out=[]
    for v in values:
        m=np.asarray(valid,bool)&np.isclose(cond_trial,v,rtol=1e-8,atol=1e-10)
        z=np.asarray(trial_response[cell_index,m],float); z=z[np.isfinite(z)]
        out.append(float(stats.sem(z)) if len(z)>1 else np.nan)
    return np.asarray(out,float)


def _save_tuning_pages(block, values, curve, pref_val, pref_resp, selectivity_notes, responsive, roi_idx, classes, out_dir,
                       bf_notes=None):
    """Paginated 3x2 tuning-curve pages for all FDR-responsive cells (titles: SI and BF notes per cell)."""
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
            _plot_condition_curve(ax,block,x,curve[i],color=CLASS_COLORS.get(str(classes[i]),'0.25'))
            ax.axhline(0,color='0.55',ls='--',lw=.8)
            _readable_condition_ticks(ax,x,labels)
            ax.set_xlabel(xlabel); ax.set_ylabel('Mean response (dF/F)')
            pref_txt=(_condition_tick_labels(block,[pref_val[i]])[0] if block=="noise_pair" else f"{pref_val[i]:.4g}") if np.isfinite(pref_val[i]) else "NA"
            note=f"\n{bf_notes[i]}" if bf_notes is not None and bf_notes[i] else ""
            ax.set_title(f"ROI {int(roi_idx[i])} | {group_label(str(classes[i]))} | preferred={pref_txt}\n{selectivity_notes[i]}{note}",fontsize=11)
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
    for cls in plot_groups():
        arr=pd.to_numeric(use.loc[group_mask(use.cell_class,cls),'pure_best_frequency_hz'],errors='coerce').to_numpy(float)
        counts=np.array([np.sum(np.isclose(arr,v)) for v in vals],float)
        frac=counts/counts.sum() if counts.sum()>0 else np.full_like(counts,np.nan)
        offset=0.0 if cls=="all" else (-.2*width if cls==GREEN else .2*width)
        axes[0].bar(x+offset,counts,width=(.8 if cls=="all" else .38)*width,label=f"{group_label(cls)} n={len(arr)}",alpha=.75)
        axes[1].plot(x,frac,marker='o',lw=2,label=f"{group_label(cls)} n={len(arr)}",color=CLASS_COLORS[cls])
    axes[0].set_ylabel('Responsive cells (count)'); axes[1].set_ylabel('Fraction of responsive cells'); axes[1].set_xlabel('Best frequency (kHz; log2 spacing)')
    _readable_condition_ticks(axes[1],x,[f"{v/1000:.3g}" for v in vals]); axes[0].legend(frameon=False); axes[1].legend(frameon=False)
    fig.suptitle('Best-frequency distribution — pure-tone FDR-responsive cells'); fig.tight_layout(rect=[0,0,1,.96]); fig.savefig(root/'best_frequency_histogram_counts_and_fraction.png',dpi=250); plt.close(fig)


def _archive_cell_report_data(archive_path):
    with np.load(str(archive_path),allow_pickle=False) as z:
        return {k:z[k] for k in z.files}


def _save_cell_reports(base, block_meta, fov_dir, levels=()):
    """One PNG per cell responsive to >=1 available sound block."""
    resp_cols=[f"{BLOCK_SHORT[b]}_responsive_fdr" for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_responsive_fdr" in base]
    if not resp_cols: return
    anyresp=np.zeros(len(base),bool)
    for c in resp_cols: anyresp|=base[c].fillna(False).astype(bool).to_numpy()
    if not anyresp.any(): return
    archives={b:_archive_cell_report_data(meta['trial_archive']) for b,meta in block_meta.items()}
    blocks=[b for b in BLOCK_ORDER if b in archives]
    root=fov_dir/'cell_reports'
    for cls in CELL_CLASSES: (root/cls).mkdir(parents=True,exist_ok=True)
    for ridx,row in base.loc[anyresp].iterrows():
        cls=str(row['cell_class']); roi=int(row['suite2p_roi_index']); acell=int(row['analysis_cell_index'])
        fig,axes=plt.subplots(len(blocks),2,figsize=(14,5*len(blocks)),squeeze=False)
        for rr,b in enumerate(blocks):
            axtr,axtu=axes[rr]
            arc=archives[b]; rois=np.asarray(arc['suite2p_roi_index'],int); hits=np.flatnonzero(rois==roi)
            if not len(hits): axtr.axis('off'); axtu.axis('off'); continue
            i=int(hits[0]); vals=np.asarray(arc['condition_values'],float); t=np.asarray(arc['tvec'],float)
            tm=np.asarray(arc['condition_trace_mean'],float)[i]; ts=np.asarray(arc['condition_trace_sem'],float)[i]
            cmap=plt.cm.viridis(np.linspace(.08,.92,len(vals)))
            for j,lab in enumerate(_condition_tick_labels(b,vals)):
                axtr.plot(t,tm[j],lw=1.4,color=cmap[j],label=lab)
                if np.any(np.isfinite(ts[j])): axtr.fill_between(t,tm[j]-ts[j],tm[j]+ts[j],color=cmap[j],alpha=.08,lw=0)
            axtr.axvline(0,color='k',ls=':',lw=.9); axtr.axhline(0,color='.55',ls='--',lw=.7); axtr.set_xlabel('Time from sound onset (s)'); axtr.set_ylabel('Baseline-subtracted dF/F'); axtr.set_title(f"{BLOCK_LABEL[b]}: mean ± SEM traces")
            rwin=response_range(b)
            if rwin!=RESPONSE_RANGE: axtr.axvspan(*rwin,color='0.85',alpha=.35,lw=0,zorder=0)
            if b=='noise_pair': axtr.legend(fontsize=6,ncol=4,frameon=False,loc='upper right')
            tr=np.asarray(arc['trial_response'],float); cond=np.asarray(arc['trial_condition_value'],float); valid=np.asarray(arc['valid_trial_mask'],bool)
            means=np.array([np.nanmean(tr[i,valid&np.isclose(cond,v)]) for v in vals]); sems=_cell_scalar_sem(tr,cond,valid,i,vals)
            x,labels,xlabel=_condition_axis(b,vals); _plot_condition_curve(axtu,b,x,means,yerr=sems,color=CLASS_COLORS.get(cls,'0.25'))
            axtu.axhline(0,color='.55',ls='--',lw=.8); _readable_condition_ticks(axtu,x,labels); axtu.set_xlabel(xlabel); axtu.set_ylabel('Mean response (dF/F)'); bfn=_cell_bf_note(row,b,levels,block_meta); axtu.set_title(f"{BLOCK_LABEL[b]} tuning (response {rwin[0]:g}-{rwin[1]:g} s)\n{_cell_selectivity_note(row,b)}"+(f"\n{bfn}" if bfn else ""),fontsize=11)
            axtu.spines[['top','right']].set_visible(False); axtr.spines[['top','right']].set_visible(False)
        bits=[f"ROI {roi} | analysis cell {acell} | {group_label(cls)}"]
        if levels: bits.append(_cell_bf_note(row,"pure_tones",levels,block_meta))
        resp='responsive: '+', '.join([BLOCK_LABEL[b] for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_responsive_fdr" in row and bool(row.get(f"{BLOCK_SHORT[b]}_responsive_fdr",False))])
        # Three title lines so the BF note and a long responsive-block list are not cut off.
        fig.suptitle(f"Cell report | {row['subject']} {row['date']} FOV#{int(row['FOV#'])} | {row['canonicalArea']} depth={row['depth']:.1f} um\n"+' | '.join(bits)+f"\n{resp}",fontsize=14)
        fig.tight_layout(rect=[0,0,1,1-.065*3/len(blocks)]); fig.savefig(root/cls/f"ROI_{roi:05d}_cell_report.png",dpi=250); plt.close(fig)


def _save_combined_bf_outputs(cells,out_dir):
    if 'pure_best_frequency_hz' not in cells or 'pure_responsive_fdr' not in cells: return
    use=cells[cells['pure_responsive_fdr'].fillna(False).astype(bool)&pd.to_numeric(cells['pure_best_frequency_hz'],errors='coerce').notna()].copy()
    if use.empty:return
    root=out_dir/'best_frequency'; root.mkdir(parents=True,exist_ok=True)
    vals=np.sort(pd.to_numeric(use['pure_best_frequency_hz'],errors='coerce').dropna().unique()); x=np.log2(vals/1000)
    # FOV x BF fraction heatmaps separately by class.
    for cls in plot_groups():
        rows=[]; labels=[]
        for uid,g in use[group_mask(use.cell_class,cls)].groupby('fov_uid'):
            arr=pd.to_numeric(g['pure_best_frequency_hz'],errors='coerce').to_numpy(float); arr=arr[np.isfinite(arr)]
            if not len(arr):continue
            rows.append([np.mean(np.isclose(arr,v)) for v in vals]); labels.append(str(uid))
        if rows:
            M=np.asarray(rows,float); fig,ax=plt.subplots(figsize=(11,max(4,0.42*len(rows)+2.5))); im=ax.imshow(M,aspect='auto',vmin=0,vmax=np.nanmax(M) if np.nanmax(M)>0 else 1,cmap='viridis')
            ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels); ax.set_xticks(range(len(vals))); labs=[f"{v/1000:.3g}" if i%2==0 else '' for i,v in enumerate(vals)]; ax.set_xticklabels(labs,rotation=60,ha='right'); ax.set_xlabel('Best frequency (kHz)'); ax.set_ylabel('FOV'); ax.set_title(f"{group_label(cls)} — fraction of responsive cells by BF within each FOV"); fig.colorbar(im,ax=ax,label='Fraction of cells'); fig.tight_layout(); fig.savefig(root/f"FOV_by_best_frequency_fraction_{cls}.png",dpi=250); plt.close(fig)
    # Per-FOV median BF summary by class.
    fig,ax=plt.subplots(figsize=(7,5.5)); rng=np.random.default_rng(117)
    for pos,cls in enumerate(plot_groups()):
        meds=[]; ns=[]
        for uid,g in use[group_mask(use.cell_class,cls)].groupby('fov_uid'):
            arr=np.log2(pd.to_numeric(g['pure_best_frequency_hz'],errors='coerce').to_numpy(float)); arr=arr[np.isfinite(arr)]
            if len(arr): meds.append(np.median(arr)); ns.append(len(arr))
        if meds:
            sizes=35+6*np.sqrt(np.asarray(ns)); ax.scatter(np.full(len(meds),pos)+rng.uniform(-.06,.06,len(meds)),np.asarray(meds),s=sizes,facecolors=CLASS_COLORS[cls],edgecolors='none',alpha=.8,label=group_label(cls))
            mu,se,n=mean_sem(meds); ax.errorbar(pos,mu,yerr=se,fmt='o',color='black',capsize=4,zorder=4)
    ax.set_xticks(range(len(plot_groups()))); ax.set_xticklabels([group_label(g) for g in plot_groups()]); ax.set_ylabel('FOV median log2(BF [Hz])'); ax.set_title('Pure-tone BF center across FOVs\nmarker size reflects responsive-cell count; no class-colored outlines'); fig.tight_layout(); fig.savefig(root/'FOV_median_best_frequency_GREEN_YELLOW.png',dpi=250); plt.close(fig)

# =============================================================================
# BLOCK ANALYSIS
# =============================================================================

def condition_column_name(block: str, value: float) -> str:
    if block == "pure_tones":
        return f"pure_response_{value:.6g}_Hz"
    if block == "chord_tones":
        return f"chord_response_middle_oct_{value:.6g}"
    if block == "band_noise":
        return f"bn_response_bw_{value:.6g}_oct"
    if block == "noise_pair":
        oi, gap = noisepair_decode([value])
        return f"np_response_{NOISEPAIR_ORDERS[int(oi[0])]}_gap_{float(gap[0]):.6g}_s"
    return f"{BLOCK_SHORT[block]}_response_slope_{value:+.6g}_oct_per_s".replace("+", "pos").replace("-", "neg")


def condition_q_column_name(block: str, value: float) -> str:
    return condition_column_name(block, value).replace("_response_", "_response_q_")


def _trial_response(eventlocked: np.ndarray, tvec: np.ndarray, window: tuple[float, float] = RESPONSE_RANGE) -> np.ndarray:
    b = (tvec >= BASELINE_RANGE[0]) & (tvec < BASELINE_RANGE[1])
    r = (tvec >= window[0]) & (tvec < window[1])
    return np.nanmean(eventlocked[:, :, r], axis=2) - np.nanmean(eventlocked[:, :, b], axis=2)


def _fm_fields(bdata: dict[str, Any], block: str) -> tuple[str, str]:
    """(per-trial slope field, center-frequency field) for the FM blocks, across paradigm versions."""
    if block == "fm_range":
        return "current_FMfixedrange_slope", "FMfixedrange_center_freq"
    if "current_FM_slope" in bdata:
        return "current_FM_slope", "FM_center_freq"
    return "current_FMfixeddur_slope", "FMfixeddur_center_freq"


def _block_required_fields(block: str, bdata: dict[str, Any]) -> list[str]:
    req = ["stim_duration", "ISI"]
    if block == "pure_tones": req += ["current_tone_freq"]
    if block == "chord_tones": req += ["current_chord3t_middle_octave", "chord3t_F0"]
    if block in FM_BLOCKS: req += list(_fm_fields(bdata, block))
    if block == "fm_range": req += ["current_FMfixedrange_sweep_duration", "FMfixedrange_octave_range"]
    if block == "band_noise": req += ["current_bandnoise_bandwidth", "bandnoise_center_freq", "bandnoise_mod_rate"]
    if block == "noise_pair": req += ["current_noisepair_order", "current_noisepair_gap", "noisepair_sound_duration",
                                      "noisepair_center_freq", "noisepair_bandwidth"]
    return req


def _block_condition_values(block: str, bdata: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    if block == "pure_tones":
        vals = np.asarray(bdata["current_tone_freq"], float)
        return vals, {"condition_unit": "Hz"}
    if block == "chord_tones":
        vals = np.asarray(bdata["current_chord3t_middle_octave"], float)
        f0arr = np.asarray(bdata["chord3t_F0"], float)
        f0 = float(np.nanmedian(f0arr))
        return vals, {"condition_unit": "octaves above F0", "F0_hz": f0}
    if block == "band_noise":
        vals = np.round(np.asarray(bdata["current_bandnoise_bandwidth"], float), 6)
        return vals, {"condition_unit": "bandwidth (octaves)",
                      "center_frequency_hz": float(np.nanmedian(np.asarray(bdata["bandnoise_center_freq"], float))),
                      "AM_rate_hz": float(np.nanmedian(np.asarray(bdata["bandnoise_mod_rate"], float)))}
    if block == "noise_pair":
        codes = np.asarray(bdata["current_noisepair_order"]).astype(int)
        labels = bdata.labels.get("current_noisepair_order", {}) if hasattr(bdata, "labels") else {}
        names = [str(labels.get(int(c), NOISEPAIR_ORDERS[int(c)])) for c in codes]
        gaps = np.asarray(bdata["current_noisepair_gap"], float)
        vals = np.array([noisepair_code(n, g) for n, g in zip(names, gaps)], float)
        return vals, {"condition_unit": "10 x order index + gap (s)", "orders": list(NOISEPAIR_ORDERS),
                      "A_center_frequency_hz": float(np.nanmedian(np.asarray(bdata["noisepair_center_freq"], float))),
                      "A_bandwidth_octaves": float(np.nanmedian(np.asarray(bdata["noisepair_bandwidth"], float))),
                      "sound_duration_s": float(np.nanmedian(np.asarray(bdata["noisepair_sound_duration"], float)))}
    slope_field, center_field = _fm_fields(bdata, block)
    vals = np.asarray(bdata[slope_field], float)
    c = np.asarray(bdata[center_field], float)
    center = float(np.nanmedian(c))
    extras = {"condition_unit": "octaves/s", "center_frequency_hz": center}
    if block == "fm_range":
        extras["octave_range"] = float(np.nanmedian(np.asarray(bdata["FMfixedrange_octave_range"], float)))
    return vals, extras


def _trial_sound_duration(block: str, bdata: dict[str, Any]) -> np.ndarray:
    """Real sound duration of each trial (the behavior file's stim_duration is the GUI value)."""
    if block == "fm_range" and "current_FMfixedrange_sweep_onset" not in bdata:
        # Since tkparadigms 91a5c1b the sound lasts as long as the sweep; earlier versions
        # (which saved a sweep onset) centered the sweep inside stim_duration.
        return np.asarray(bdata["current_FMfixedrange_sweep_duration"], float)
    if block == "noise_pair":
        return 2 * np.asarray(bdata["noisepair_sound_duration"], float) + np.asarray(bdata["current_noisepair_gap"], float)
    return np.asarray(bdata["stim_duration"], float)


def _block_specific_metrics(block: str, df: pd.DataFrame, curve: np.ndarray, values: np.ndarray,
                            pref_val: np.ndarray, extras: dict[str, Any]) -> None:
    """Add block-specific columns to df in place, from a cells x conditions mean-response matrix."""
    n = len(df); nanv = np.full(n, np.nan)
    p = BLOCK_SHORT[block]
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
            other = np.nanmean(np.delete(curve, hj, axis=1), axis=1) if len(values) > 1 else nanv
            df["chord_harmonic_response"] = rh
            df["chord_nonharmonic_mean_response"] = other
            df["chord_harmonic_selectivity"] = bounded_selectivity(rh, other)
        else:
            df["chord_harmonic_response"] = np.nan
            df["chord_nonharmonic_mean_response"] = np.nan
            df["chord_harmonic_selectivity"] = np.nan
    elif block in FM_BLOCKS:
        df[f"{p}_best_slope_oct_per_s"] = pref_val
        df[f"{p}_best_abs_slope_oct_per_s"] = np.abs(pref_val)
        pos = values > 0; neg = values < 0
        rup = np.nanmean(curve[:, pos], axis=1) if np.any(pos) else nanv
        rdn = np.nanmean(curve[:, neg], axis=1) if np.any(neg) else nanv
        df[f"{p}_upward_mean_response"] = rup
        df[f"{p}_downward_mean_response"] = rdn
        df[f"{p}_direction_selectivity"] = bounded_selectivity(rup, rdn)
        mags = np.sort(np.unique(np.abs(values[np.abs(values) > 0])))
        speedmat = np.full((n, len(mags)), np.nan)
        for j, mag in enumerate(mags):
            use = np.isclose(np.abs(values), mag)
            speedmat[:, j] = np.nanmean(curve[:, use], axis=1)
        df[f"{p}_speed_lifetime_sparseness"] = lifetime_sparseness_rows(speedmat)
        if block == "fm_range":
            df["fmr_center_frequency_hz"] = float(extras["center_frequency_hz"])
            df["fmr_best_sweep_duration_s"] = float(extras.get("octave_range", np.nan)) / np.abs(pref_val)
    elif block == "band_noise":
        jn = int(np.argmin(values)); jw = int(np.argmax(values))
        df["bn_best_bandwidth_oct"] = pref_val
        df["bn_narrowest_response"] = curve[:, jn]
        df["bn_widest_response"] = curve[:, jw]
        df["bn_bandwidth_selectivity"] = bounded_selectivity(curve[:, jw], curve[:, jn])
        df["bn_center_frequency_hz"] = float(extras["center_frequency_hz"])
    elif block == "noise_pair":
        oi, gap = noisepair_decode(values)
        def omean(names, gmask=None):
            m = np.isin(oi, [NOISEPAIR_ORDERS.index(x) for x in names])
            if gmask is not None: m &= gmask
            return np.nanmean(curve[:, m], axis=1) if np.any(m) else nanv
        for name in NOISEPAIR_ORDERS:
            df[f"np_mean_response_{NOISEPAIR_SHORT[name]}"] = omean([name])
        diff = omean(["A_then_B", "B_then_A"]); same = omean(["A_then_A", "B_then_B"])
        df["np_different_pair_mean_response"] = diff
        df["np_same_pair_mean_response"] = same
        df["np_novelty_selectivity"] = bounded_selectivity(diff, same)
        df["np_first_sound_selectivity"] = bounded_selectivity(omean(["A_then_A", "A_then_B"]), omean(["B_then_A", "B_then_B"]))
        for g in np.unique(gap):
            gm = np.isclose(gap, g)
            df[f"np_novelty_selectivity_gap_{g:g}_s"] = bounded_selectivity(omean(["A_then_B", "B_then_A"], gm),
                                                                           omean(["A_then_A", "B_then_B"], gm))
        po, pg = noisepair_decode(np.nan_to_num(pref_val, nan=0.0))
        df["np_best_order"] = np.where(np.isfinite(pref_val), [NOISEPAIR_SHORT[NOISEPAIR_ORDERS[int(o)]] for o in po], None)
        df["np_best_gap_s"] = np.where(np.isfinite(pref_val), pg, np.nan)
        df["np_A_center_frequency_hz"] = float(extras["A_center_frequency_hz"])


def noisepair_novelty_test(tr: np.ndarray, cond_trial: np.ndarray, valid: np.ndarray,
                           values: np.ndarray) -> dict[str, np.ndarray]:
    """Per-cell test of R_diff - R_same (the numerator of SI_nov).

    The contrast is mean over different-pair conditions (AB, BA at every gap) minus mean over
    same-pair conditions (AA, BB), each condition weighted equally. Its variance is the sum of
    the per-condition variances of the mean (Welch-style, trials independent), giving a z
    statistic, a two-sided normal p, and BH-FDR across cells. The ratio SI_nov is noisy when
    responses are small; this tests the difference itself.
    """
    oi, _ = noisepair_decode(values)
    sign = np.where(np.isin(oi, [0, 1]), 1.0, -1.0)
    n_side = {1.0: max(1, int(np.sum(sign > 0))), -1.0: max(1, int(np.sum(sign < 0)))}
    ncell = tr.shape[0]; contrast = np.zeros(ncell); var = np.zeros(ncell); ok = np.ones(ncell, bool)
    for j, val in enumerate(values):
        tm = valid & np.isclose(cond_trial, val, rtol=1e-8, atol=1e-10)
        x = tr[:, tm]; n = np.sum(np.isfinite(x), axis=1)
        ok &= n >= MIN_FINITE_TRIALS
        w = sign[j] / n_side[sign[j]]
        with np.errstate(invalid="ignore", divide="ignore"):
            contrast += w * np.nanmean(x, axis=1)
            var += w ** 2 * np.nanvar(x, axis=1, ddof=1) / n
    with np.errstate(invalid="ignore", divide="ignore"):
        z = np.where(ok & (var > 0), contrast / np.sqrt(var), np.nan)
    p = np.where(np.isfinite(z), 2 * stats.norm.sf(np.abs(z)), np.nan)
    q = bh_fdr(p)
    return {"np_novelty_contrast": np.where(ok, contrast, np.nan), "np_novelty_z": z, "np_novelty_p": p,
            "np_novelty_q": q, "np_novelty_sig_fdr": np.isfinite(q) & (q < 0.05)}


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
    missing = [k for k in _block_required_fields(block, bdata) if k not in bdata]
    if missing:
        raise KeyError(f"Missing behavior fields for {block}: {missing}")
    cond_trial, extras = _block_condition_values(block, bdata)
    ntr = len(cond_trial)
    sound_dur = _trial_sound_duration(block, bdata)
    ev, valid, event_onset, align_diag = align_imaging_events_to_behavior(
        ev, valid, np.asarray(data2p.event_onset), float(data2p.srate),
        sound_dur, np.asarray(bdata["ISI"], float), ntr)
    rwin = response_range(block)
    isi = finite(bdata["ISI"])
    if len(isi) and rwin[1] > float(np.min(isi)) + float(np.nanmin(sound_dur)):
        print(f"  WARNING {block} {session}: response window ends at {rwin[1]:g} s but the next sound can start "
              f"{float(np.min(isi)) + float(np.nanmin(sound_dur)):.3g} s after onset")
    tvec_arr=np.asarray(tvec,float)
    bmask=(tvec_arr>=BASELINE_RANGE[0])&(tvec_arr<BASELINE_RANGE[1])
    ev_bc=ev-np.nanmean(ev[:,:,bmask],axis=2)[:,:,None]
    tr = _trial_response(ev, tvec_arr, rwin)
    tr[:, ~np.asarray(valid, bool)] = np.nan
    tr_std = None
    if rwin != RESPONSE_RANGE:
        tr_std = _trial_response(ev, tvec_arr, RESPONSE_RANGE)
        tr_std[:, ~np.asarray(valid, bool)] = np.nan

    values = np.sort(np.unique(cond_trial[np.isfinite(cond_trial)]))
    curve = np.full((len(roi_idx), len(values)), np.nan)
    curve_std = np.full_like(curve, np.nan)
    pmat = np.full_like(curve, np.nan); qmat = np.full_like(curve, np.nan); sigmat = np.zeros_like(curve, bool)
    trace_mean=np.full((len(roi_idx),len(values),ev_bc.shape[2]),np.nan,dtype=float)
    trace_sem=np.full_like(trace_mean,np.nan)
    rng = np.random.default_rng(seed)
    counts = []
    for j, val in enumerate(values):
        tm = np.asarray(valid, bool) & np.isclose(cond_trial, val, rtol=1e-8, atol=1e-10)
        counts.append(int(tm.sum()))
        curve[:, j] = np.nanmean(tr[:, tm], axis=1)
        if tr_std is not None:
            curve_std[:, j] = np.nanmean(tr_std[:, tm], axis=1)
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
    _block_specific_metrics(block, df, curve, values, pref_val, extras)
    if block == "pure_tones":
        # BF eligibility as in the level-series branch / quick_bf_check_v1.py.
        q_at = np.array([qmat[i, j] if j >= 0 else np.nan for i, j in enumerate(pref_idx)], float)
        df["pure_q_at_bf"] = q_at
        df["pure_bf_eligible"] = resp_any & (pref_resp > 0) & np.isfinite(q_at) & (q_at < 0.05)
    if block == "noise_pair":
        for k, v in noisepair_novelty_test(tr, cond_trial, np.asarray(valid, bool), values).items():
            df[k] = v
    if tr_std is not None:
        # Sensitivity: the primary selectivity index from the standard 0-1 s window.
        tmp = pd.DataFrame(index=df.index)
        std_pref = np.array([values[int(np.nanargmax(r))] if np.any(np.isfinite(r)) else np.nan for r in curve_std], float)
        _block_specific_metrics(block, tmp, curve_std, values, std_pref, extras)
        metric = SELECTIVITY_SPEC[block]["metric"]
        df[f"{metric}_win0to1"] = tmp[metric].to_numpy()
    df[f"{prefix}_response_window_s"] = f"{rwin[0]:g}-{rwin[1]:g}"

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
        response_window_s=np.asarray(rwin, float), trial_sound_duration_s=np.asarray(sound_dur, np.float32),
        level_db=np.asarray(float(meta.get("level_db", np.nan))),
    )
    df[f"{prefix}_trial_archive_path"] = str(archive)

    # Per-FOV block figures: class profiles + raster.
    xplot, xticklabels, xlabel = _condition_axis(block, values)
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for cls in CELL_CLASSES:
        m = np.asarray(fov_reference["cell_class"]) == cls
        if not np.any(m): continue
        mu = np.nanmean(curve[m], axis=0)
        se = stats.sem(curve[m], axis=0, nan_policy="omit")
        _plot_condition_curve(ax, block, xplot, mu, label=f"{group_label(cls)} (n={m.sum()})", color=CLASS_COLORS[cls])
        if block != "noise_pair":
            ax.fill_between(xplot, mu-se, mu+se, alpha=.18, color=CLASS_COLORS[cls])
    ax.axhline(0, color="0.5", ls="--", lw=1); ax.set_xlabel(xlabel)
    ax.set_ylabel(f"Evoked response (dF/F, {rwin[0]:g}-{rwin[1]:g} s minus baseline)")
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

    if block=="pure_tones": _save_pure_bf_histograms(df,values,out_dir)

    meta_out = {"block_type": block, "session": session, "level_db": meta.get("level_db"),
                "condition_values": values, "trial_counts": counts, "response_window_s": list(rwin),
                "alignment": align_diag, **extras, "trial_archive": str(archive),
                # Drawn in merge_fov_blocks() once the cell's BF is known; removed before saving the manifest.
                "_tuning_pages": dict(values=values, curve=curve, pref_val=pref_val, pref_resp=pref_resp,
                                      responsive=resp_any, roi_idx=roi_idx, classes=np.asarray(fov_reference["cell_class"]),
                                      out_dir=out_dir)}
    print(f"  {session} {block}: responsive={int(resp_any.sum())} of {len(df)} | trials/condition "
          f"{min(counts)}-{max(counts)} | alignment MAE={align_diag['timing_mae_s']*1000:.0f} ms")
    return df, meta_out


# =============================================================================
# FOV MERGE / CROSS-SOUND METRICS
# =============================================================================

def merge_fov_blocks(meta_seq: list[dict[str, Any]], plane: int, fov_dir: Path,
                     n_permutations: int, seed: int, cell_reports: bool = True,
                     other_pure_levels: list[dict[str, Any]] = ()) -> tuple[pd.DataFrame, dict[str, Any]]:
    global RED_RECORDED
    meta_seq = sorted(meta_seq, key=lambda x: x["session"])
    ref_meta = meta_seq[0]
    ref_data = twophotonanalysis.TwoPhoton(str(ref_meta["subject"]), str(ref_meta["date"]), str(ref_meta["session"]), plane, paradigm=PARADIGM)
    reference = classify_fov_cells(ref_data, plane, fov_dir)
    RED_RECORDED = bool(reference["red_channel_recorded"])  # per-FOV figure labels; reset for the run in main()
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
    block_meta = {}
    sessions_by_block = {}
    for k, meta in enumerate(meta_seq):
        block = meta["block_type"]; sessions_by_block[block] = meta["session"]
        bdf, bout = analyze_block(meta, plane, reference, fov_dir, n_permutations, seed + 1009*k)
        keep = [c for c in bdf.columns if c not in {"analysis_cell_index","suite2p_roi_index","cell_class","cellpose_red_iou","suite2p_red_score"}]
        base = base.merge(bdf[["suite2p_roi_index"] + keep], on="suite2p_roi_index", how="left", validate="one_to_one")
        block_meta[block] = bout
    if "pure_tones" in block_meta:
        base["pure_tones_level_db"] = float(block_meta["pure_tones"].get("level_db") or np.nan)
    # Other pure-tone levels in this FOV: same analysis, own folder, columns pure_<N>dB_*.
    level_meta = {}
    for k, meta in enumerate(sorted(other_pure_levels, key=lambda m: float(m.get("level_db", np.nan)))):
        lv = float(meta["level_db"]); pre = f"pure_{lv:g}dB_"
        sub = fov_dir / "pure_tones_other_levels" / f"{lv:g}dB"; sub.mkdir(parents=True, exist_ok=True)
        bdf, bout = analyze_block(meta, plane, reference, sub, n_permutations, seed + 7919*(k+1))
        keep = [c for c in bdf.columns if c.startswith("pure_")]
        bdf = bdf[["suite2p_roi_index"] + keep].rename(columns={c: pre + c[len("pure_"):] for c in keep})
        base = base.merge(bdf, on="suite2p_roi_index", how="left", validate="one_to_one")
        level_meta[lv] = bout
    base = base.copy()  # de-fragment after the per-block merges

    # Cross-sound cell-level metrics are only defined where both blocks exist.
    if "pure_tones" in block_meta and "chord_tones" in block_meta:
        if "pure_best_frequency_hz" in base and "chord_best_middle_frequency_hz" in base:
            base["pure_vs_chord_best_frequency_log2_difference"] = np.log2(base["chord_best_middle_frequency_hz"] / base["pure_best_frequency_hz"])
    if "pure_tones" in block_meta and "fm_tones" in block_meta:
        if "pure_lifetime_sparseness" in base and "fm_direction_selectivity" in base:
            base["pure_sparseness_x_fm_direction_selectivity"] = base["pure_lifetime_sparseness"] * base["fm_direction_selectivity"]
    # Where the cell's BF sits relative to the sound's center frequency (octaves; + = BF above center).
    # Band noise / noise-pair A cover the center, and a fixed-range sweep crosses the BF earlier
    # for one direction than the other, so these are the main covariates of the new indices.
    for b, ccol in (("fm_range", "fmr_center_frequency_hz"), ("band_noise", "bn_center_frequency_hz"),
                    ("noise_pair", "np_A_center_frequency_hz")):
        if "pure_tones" in block_meta and b in block_meta and ccol in base:
            base[f"pure_bf_octaves_from_{BLOCK_SHORT[b]}_center"] = np.log2(
                pd.to_numeric(base["pure_best_frequency_hz"], errors="coerce") / pd.to_numeric(base[ccol], errors="coerce"))

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

    def scatter_pair(xcol, ycol, xlabel, ylabel, fname, mask_extra=None, title="Same cells across sound blocks"):
        if xcol not in base or ycol not in base: return
        fig, ax = plt.subplots(figsize=(6.5,5.5))
        for cls in CELL_CLASSES:
            m = (base.cell_class==cls) & np.isfinite(base[xcol]) & np.isfinite(base[ycol])
            if mask_extra is not None: m &= mask_extra(base)
            if not m.any(): continue
            ax.scatter(base.loc[m,xcol], base.loc[m,ycol], s=18, alpha=.6, label=f"{group_label(cls)} n={m.sum()}", color=CLASS_COLORS[cls])
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.legend(frameon=False); ax.set_title(title); fig.tight_layout()
        fig.savefig(fov_dir/fname,dpi=250); plt.close(fig)
    def both_responsive(b):
        cols = ["pure_responsive_fdr", f"{BLOCK_SHORT[b]}_responsive_fdr"]
        return lambda d: d[cols].fillna(False).astype(bool).all(axis=1) if all(c in d for c in cols) else False
    for b in ("fm_range", "band_noise", "noise_pair"):
        xcol = f"pure_bf_octaves_from_{BLOCK_SHORT[b]}_center"
        metrics = [SELECTIVITY_SPEC[b]["metric"]] + (["np_first_sound_selectivity"] if b == "noise_pair" else [])
        for ycol in metrics:
            if xcol not in base or ycol not in base: continue
            m = both_responsive(b)(base) & np.isfinite(base[xcol]) & np.isfinite(base[ycol])
            rho = stats.spearmanr(base.loc[m, xcol], base.loc[m, ycol]) if m.sum() >= 5 else None
            rtxt = f"Spearman rho={rho.statistic:.2f}, p={rho.pvalue:.2g} (cells)" if rho is not None else "n < 5"
            scatter_pair(xcol, ycol, f"Pure-tone BF re {BLOCK_LABEL[b].lower()} center (octaves)", ycol,
                         f"same_cell_BF_offset_vs_{ycol}.png", both_responsive(b),
                         f"Cells responsive to pure tones and {BLOCK_LABEL[b].lower()}\n{rtxt}")
    scatter_pair("pure_best_frequency_hz","chord_best_middle_frequency_hz","Pure-tone BF (Hz)","Preferred chord middle frequency (Hz)","same_cell_pure_BF_vs_chord_middle_frequency.png")
    scatter_pair("pure_best_frequency_hz","fm_direction_selectivity","Pure-tone BF (Hz)","FM direction selectivity (up - down)","same_cell_pure_BF_vs_FM_direction_selectivity.png")
    scatter_pair("chord_harmonic_selectivity","fm_direction_selectivity","Chord harmonic selectivity","FM direction selectivity","same_cell_chord_vs_FM_selectivity.png")
    # Single-cell tuning pages, now that each cell's BF at every level is known.
    levels = _bf_level_prefixes(base)
    for b, meta in list(block_meta.items()) + [("pure_tones", m) for m in level_meta.values()]:
        pg = meta.pop("_tuning_pages")
        assert np.array_equal(np.asarray(pg["roi_idx"], int), base["suite2p_roi_index"].to_numpy(int))
        if meta is block_meta.get(b):
            sel = [_cell_selectivity_note(r, b) for _, r in base.iterrows()]
        else:  # other pure-tone level: its own sparseness column
            pre = f"pure_{float(meta['level_db']):g}dB_"
            sel = [_cell_selectivity_note(r, b, pre + "lifetime_sparseness") for _, r in base.iterrows()]
        bfn = [_cell_bf_note(r, b, levels, block_meta) for _, r in base.iterrows()]
        _save_tuning_pages(b, pg["values"], pg["curve"], pg["pref_val"], pg["pref_resp"], sel, pg["responsive"],
                           pg["roi_idx"], pg["classes"], pg["out_dir"], bfn)
    if cell_reports:
        _save_cell_reports(base,block_meta,fov_dir,levels)

    summary = {"fov_uid": ref_meta["fov_uid"], "FOV#": int(ref_meta["fov_number"]),
               "date": ref_meta["date"], "sessions_by_block": sessions_by_block,
               "available_blocks": list(block_meta), "n_cells": len(base),
               "n_green": int(np.sum(base.cell_class==GREEN)), "n_yellow": int(np.sum(base.cell_class==YELLOW)),
               "red_channel_recorded": bool(reference["red_channel_recorded"]),
               "suite2p_reference_dir": reference["suite2p_dir"], "block_metadata": block_meta,
               "other_pure_tone_levels": {f"{lv:g}dB": m for lv, m in level_meta.items()}}
    save_json(fov_dir / "fov_manifest.json", summary)
    return base, summary


# =============================================================================
# COMBINED AREA SUMMARIES
# =============================================================================

def _blocks_present(cells: pd.DataFrame) -> list[str]:
    return [b for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_responsive_fdr" in cells
            and cells[f"{BLOCK_SHORT[b]}_responsive_fdr"].notna().any()]


SUMMARY_METRICS = ["pure_best_frequency_hz","pure_fwhm_octaves","chord_best_middle_octave","chord_harmonic_selectivity",
                   "fm_best_slope_oct_per_s","fm_best_abs_slope_oct_per_s","fm_direction_selectivity","fm_speed_lifetime_sparseness",
                   "fmr_best_abs_slope_oct_per_s","fmr_direction_selectivity","fmr_direction_selectivity_win0to1","fmr_speed_lifetime_sparseness",
                   "bn_best_bandwidth_oct","bn_bandwidth_selectivity",
                   "np_novelty_selectivity","np_novelty_selectivity_win0to1","np_first_sound_selectivity"]


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
        for metric in SUMMARY_METRICS:
            if metric in g: row[f"mean_{metric}"] = float(np.nanmean(g[metric])) if np.any(np.isfinite(g[metric])) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def plot_combined_responsiveness(summary: pd.DataFrame, out_dir: Path) -> dict[str, Any]:
    blocks = [b for b in BLOCK_ORDER if f"{BLOCK_SHORT[b]}_percent_responsive" in summary
              and np.any(np.isfinite(summary[f"{BLOCK_SHORT[b]}_percent_responsive"]))]
    if not blocks:
        return {}
    stats_out = {}
    fig, axes = plt.subplots(1,len(blocks),figsize=(5*len(blocks),5),squeeze=False)
    if not RED_RECORDED:
        # No GREEN/YELLOW split: % responsive per FOV for each block, no test.
        for ax,b in zip(axes[0],blocks):
            col=f"{BLOCK_SHORT[b]}_percent_responsive"; t=summary.dropna(subset=[col]).sort_values(["date","FOV#"])
            ax.bar(range(len(t)),t[col],color=CLASS_COLORS["all"],alpha=.8)
            ax.set_xticks(range(len(t))); ax.set_xticklabels([f"FOV{int(f)}\n{str(a).split('_')[-1]}" for f,a in zip(t["FOV#"],t.brainArea)])
            ax.set_ylim(0,100); ax.set_ylabel("Responsive cells (%)"); ax.set_title(BLOCK_LABEL[b])
            stats_out[b]={"percent_responsive_by_FOV":dict(zip(t.fov_uid,t[col]))}
        fig.suptitle("Sound responsiveness by FOV (all cells; no red channel)"); fig.tight_layout(rect=[0,0,1,.93])
        fig.savefig(out_dir/"responsive_fraction_by_FOV.png",dpi=250); plt.close(fig)
        return stats_out
    pvals=[]; recs=[]
    for ax,b in zip(axes[0],blocks):
        col=f"{BLOCK_SHORT[b]}_percent_responsive"
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
    adj=holm_adjust(pvals); nb=len(blocks)
    for (ax,b,rec),ph in zip(recs,adj):
        rec["p_holm_blocks"] = float(ph) if np.isfinite(ph) else np.nan; rec["n_blocks_in_holm_family"]=nb; stats_out[b]=rec
        ax.text(.02,.98,f"paired FOV Wilcoxon\nW={rec['W']:.3g}, p={rec['p']:.3g}\nHolm({nb}) p={ph:.3g}\nn={rec['n_pairs']} FOV pairs",transform=ax.transAxes,ha="left",va="top",fontsize=8)
    fig.suptitle("Sound responsiveness: GREEN vs YELLOW; FOV is replicate"); fig.tight_layout(rect=[0,0,1,.94])
    fig.savefig(out_dir/"responsive_fraction_GREEN_vs_YELLOW_FOV_POINTS.png",dpi=250); plt.close(fig)
    return stats_out


def _profile_columns(cells: pd.DataFrame, block: str) -> list[tuple[float,str]]:
    pat = {
        "pure_tones": re.compile(r"^pure_response_([0-9.eE+-]+)_Hz$"),
        "chord_tones": re.compile(r"^chord_response_middle_oct_([0-9.eE+-]+)$"),
        "fm_tones": re.compile(r"^fm_response_slope_(pos|neg)?([0-9.eE+]+)_oct_per_s$"),
        "fm_range": re.compile(r"^fmr_response_slope_(pos|neg)?([0-9.eE+]+)_oct_per_s$"),
        "band_noise": re.compile(r"^bn_response_bw_([0-9.eE+-]+)_oct$"),
        "noise_pair": re.compile(r"^np_response_(A_then_B|B_then_A|A_then_A|B_then_B)_gap_([0-9.eE+-]+)_s$"),
    }[block]
    out=[]
    for c in cells.columns:
        m=pat.match(c)
        if not m: continue
        if block in FM_BLOCKS:
            sign=-1 if m.group(1)=="neg" else 1; val=sign*float(m.group(2))
        elif block=="noise_pair":
            val=noisepair_code(m.group(1),float(m.group(2)))
        else: val=float(m.group(1))
        out.append((val,c))
    return sorted(out)


def plot_combined_profiles(cells: pd.DataFrame, out_dir: Path) -> None:
    for block in BLOCK_ORDER:
        cols=_profile_columns(cells,block)
        if not cols: continue
        vals=np.array([v for v,_ in cols])
        x,labels,xlabel=_condition_axis(block,vals)
        groups=plot_groups()
        fig,axes=plt.subplots(1,len(groups),figsize=(6.5*len(groups)+.5,5),sharey=True,squeeze=False)
        for ax,cls in zip(axes[0],groups):
            sub=cells[group_mask(cells.cell_class,cls)]
            # each FOV contributes its mean tuning curve
            curves=[]
            for uid,g in sub.groupby("fov_uid"):
                arr=g[[c for _,c in cols]].to_numpy(float)
                if np.any(np.isfinite(arr)): curves.append(np.nanmean(arr,axis=0))
            if curves:
                M=np.vstack(curves)
                for row in M: _plot_condition_curve(ax,block,x,row,color="0.78",alpha=.8)
                mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy="omit") if len(M)>1 else np.full_like(mu,np.nan)
                _plot_condition_curve(ax,block,x,mu,color=CLASS_COLORS[cls])
                if block!="noise_pair": ax.fill_between(x,mu-se,mu+se,color=CLASS_COLORS[cls],alpha=.2)
            ax.axhline(0,color="0.5",ls="--",lw=1); ax.set_title(f"{group_label(cls)} — FOV means (n={len(curves)} FOVs)")
            _readable_condition_ticks(ax,x,labels); ax.set_xlabel(xlabel)
        rw=response_range(block)
        axes[0][0].set_ylabel(f"Evoked response (dF/F, {rw[0]:g}-{rw[1]:g} s)"); fig.suptitle(f"{BLOCK_LABEL[block]} — across-FOV profiles"); fig.tight_layout(rect=[0,0,1,.94])
        fig.savefig(out_dir/f"{block}_across_FOV_GREEN_YELLOW_profiles.png",dpi=250); plt.close(fig)


def _selectivity_use(cells: pd.DataFrame, block: str, branch: str) -> pd.DataFrame:
    if branch == "responsive_only":
        rc = f"{BLOCK_SHORT[block]}_responsive_fdr"
        return cells[cells[rc].fillna(False).astype(bool)].copy() if rc in cells else cells.iloc[0:0].copy()
    rc = f"{BLOCK_SHORT[block]}_responsive_fdr"
    return cells[cells[rc].notna()].copy() if rc in cells else cells.iloc[0:0].copy()


def plot_primary_selectivity_green_yellow(cells: pd.DataFrame, out_dir: Path) -> dict[str, Any]:
    """Dedicated primary selectivity plots: GREEN vs YELLOW with FOV as replicate."""
    root = out_dir / "selectivity_plots"
    root.mkdir(parents=True, exist_ok=True)
    stats_out = {}
    blocks = [b for b in _blocks_present(cells) if SELECTIVITY_SPEC[b]["metric"] in cells]
    for branch in ("all_cells", "responsive_only"):
        tmp = []
        for block in blocks:
            spec = SELECTIVITY_SPEC[block]; metric = spec["metric"]
            use = _selectivity_use(cells, block, branch)
            x = use[["fov_uid", "cell_class", metric]].copy()
            x[metric] = pd.to_numeric(x[metric], errors="coerce")
            t = x.groupby(["fov_uid", "cell_class"], as_index=False)[metric].mean().rename(columns={metric:"value"})
            piv = t.pivot(index="fov_uid", columns="cell_class", values="value").reset_index() if len(t) else pd.DataFrame()
            rec = safe_wilcoxon_pairs(piv, GREEN, YELLOW) if len(piv) and GREEN in piv and YELLOW in piv else {"n_pairs":0,"W":np.nan,"p":np.nan}
            tmp.append((block, piv, rec))
        adj = holm_adjust([rec["p"] for _,_,rec in tmp]); nb = len(tmp)
        for (block,piv,rec),ph in zip(tmp,adj):
            spec=SELECTIVITY_SPEC[block]; rec["p_holm_selectivity_indices"] = float(ph) if np.isfinite(ph) else np.nan
            rec["n_indices_in_holm_family"] = nb
            stats_out.setdefault(branch,{})[block]=rec
            d = root/spec["folder"]; d.mkdir(parents=True,exist_ok=True)
            fig,(ax,axeq)=plt.subplots(1,2,figsize=(9.6,5.8),gridspec_kw={"width_ratios":[2.35,1.0]})
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
            axeq.text(.5,.97,f"paired FOV Wilcoxon\nW={rec['W']:.3g}, p={rec['p']:.3g}\nHolm({nb} indices) p={ph:.3g}\nn={rec['n_pairs']} pairs",transform=axeq.transAxes,ha="center",va="top",fontsize=9)
            _selectivity_equation_box(axeq,block,fontsize=15.5); fig.tight_layout(); fig.savefig(d/f"{branch}_GREEN_vs_YELLOW_FOV_primary_selectivity.png",dpi=250); plt.close(fig)
    save_json(root/"primary_selectivity_statistics.json",stats_out)
    return stats_out


def _wilcoxon_vs_zero(v: Iterable[Any]) -> dict[str, Any]:
    a = finite(v)
    if len(a) < 2 or np.allclose(a, 0):
        return {"n": int(len(a)), "median": float(np.median(a)) if len(a) else np.nan, "W": np.nan, "p": np.nan}
    r = stats.wilcoxon(a, alternative="two-sided", zero_method="wilcox")
    return {"n": int(len(a)), "median": float(np.median(a)), "W": float(r.statistic), "p": float(r.pvalue)}


def plot_selectivity_by_fov(cells: pd.DataFrame, out_dir: Path) -> dict[str, Any]:
    """Each selectivity index per FOV (all cells pooled over classes) and its test against 0.

    Used when there is no GREEN/YELLOW split. FOV is the replicate across FOVs (Wilcoxon on
    FOV medians, which has little power with few FOVs); the within-FOV cell-level Wilcoxon
    describes that FOV only.
    """
    root = out_dir / "selectivity_plots"; root.mkdir(parents=True, exist_ok=True)
    stats_out: dict[str, Any] = {}
    metrics = []
    for b in _blocks_present(cells):
        m = SELECTIVITY_SPEC[b]["metric"]
        if m in cells: metrics.append((b, m, SELECTIVITY_SPEC[b]["label"]))
        if f"{m}_win0to1" in cells: metrics.append((b, f"{m}_win0to1", SELECTIVITY_SPEC[b]["label"] + " (0-1 s window)"))
        if b == "noise_pair" and "np_first_sound_selectivity" in cells:
            metrics.append((b, "np_first_sound_selectivity", "Noise-pair first-sound selectivity (A vs B first)"))
    fovs = cells[["fov_uid","FOV#","date","brainArea"]].drop_duplicates("fov_uid").sort_values(["date","FOV#"])
    rng = np.random.default_rng(11)
    for branch in ("all_cells", "responsive_only"):
        for block, metric, label in metrics:
            use = _selectivity_use(cells, block, branch)
            spec = SELECTIVITY_SPEC[block]; d = root/spec["folder"]; d.mkdir(parents=True, exist_ok=True)
            fig,(ax,axeq)=plt.subplots(1,2,figsize=(3.2+1.6*len(fovs),5.8),gridspec_kw={"width_ratios":[2.35,1.0]})
            rec: dict[str, Any] = {"by_FOV": {}}; meds = []
            for k,(_,fr) in enumerate(fovs.iterrows()):
                v = finite(pd.to_numeric(use.loc[use.fov_uid==fr.fov_uid, metric], errors="coerce"))
                rec["by_FOV"][fr.fov_uid] = _wilcoxon_vs_zero(v)
                if len(v):
                    ax.scatter(k+rng.uniform(-.18,.18,len(v)), v, s=7, alpha=.35, color=CLASS_COLORS["all"], edgecolors="none")
                    ax.plot([k-.28,k+.28],[np.median(v)]*2, color="black", lw=2.2); meds.append(np.median(v))
            rec["across_FOV_medians"] = _wilcoxon_vs_zero(meds)
            pooled = finite(pd.to_numeric(use[metric], errors="coerce")); rec["pooled_cells_exploratory"] = _wilcoxon_vs_zero(pooled)
            stats_out.setdefault(branch, {})[metric] = rec
            ax.axhline(0,color="0.6",ls="--",lw=.8); ax.set_ylim(*spec["ylim"])
            ax.set_xticks(range(len(fovs))); ax.set_xticklabels([f"FOV{int(f)}\n{str(a).split('_')[-1]}" for f,a in zip(fovs["FOV#"],fovs.brainArea)])
            ax.set_ylabel(label); ax.set_title(f"{BLOCK_LABEL[block]} — {branch.replace('_',' ')}\ncells per FOV; bar = median")
            lines=["Wilcoxon vs 0 (cells within FOV)"]
            for _,fr in fovs.iterrows():
                r=rec["by_FOV"][fr.fov_uid]; fn=int(fr["FOV#"])
                lines.append(f"FOV{fn}: med={r['median']:+.2f} p={r['p']:.2g} n={r['n']}" if r["n"] else f"FOV{fn}: n=0")
            ra=rec["across_FOV_medians"]; lines.append(f"\nFOV medians vs 0: p={ra['p']:.2g} (n={ra['n']} FOVs)")
            axeq.text(.5,.97,"\n".join(lines),transform=axeq.transAxes,ha="center",va="top",fontsize=8.5)
            _selectivity_equation_box(axeq,block,fontsize=13)
            fig.tight_layout(); fig.savefig(d/f"{branch}_{metric}_by_FOV.png",dpi=250); plt.close(fig)
    save_json(root/"selectivity_by_FOV_statistics.json", stats_out)
    return stats_out


def plot_noise_pair_gap_dependence(cells: pd.DataFrame, out_dir: Path) -> None:
    """Novelty selectivity and per-order responses as a function of gap (noise-pair responsive cells)."""
    pat = re.compile(r"^np_novelty_selectivity_gap_([0-9.]+)_s$")
    gcols = sorted(((float(m.group(1)), c) for c in cells.columns if (m := pat.match(c))))
    if not gcols or "np_responsive_fdr" not in cells: return
    use = cells[cells["np_responsive_fdr"].fillna(False).astype(bool)]
    if use.empty: return
    gaps = np.array([g for g,_ in gcols]); x = np.log2(gaps)
    prof = dict(_profile_columns(cells, "noise_pair"))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    for uid, g in use.groupby("fov_uid"):
        fovn = int(g["FOV#"].iloc[0])
        ax1.plot(x, [np.nanmedian(pd.to_numeric(g[c], errors="coerce")) for _,c in gcols], marker="o", label=f"FOV{fovn} (n={len(g)})")
    ax1.axhline(0, color="0.6", ls="--", lw=.8); ax1.set_xticks(x); ax1.set_xticklabels([f"{v:g}" for v in gaps])
    ax1.set_xlabel("Gap between sounds (s; log2 spacing)"); ax1.set_ylabel("Median SI_nov (different - same pair)")
    ax1.set_title("Novelty selectivity vs gap — noise-pair responsive cells"); ax1.legend(frameon=False)
    for oname in NOISEPAIR_ORDERS:
        cols = [prof.get(noisepair_code(oname, gp)) for gp in gaps]
        if any(c is None for c in cols): continue
        fov_curves = [np.nanmean(g[cols].to_numpy(float), axis=0) for _, g in use.groupby("fov_uid")]
        M = np.vstack(fov_curves); mu = np.nanmean(M, axis=0)
        ax2.plot(x, mu, marker="o", lw=2, label=NOISEPAIR_SHORT[oname], ls="-" if oname[0] != oname[-1] else "--")
    ax2.set_xticks(x); ax2.set_xticklabels([f"{v:g}" for v in gaps]); ax2.axhline(0, color="0.6", ls="--", lw=.8)
    ax2.set_xlabel("Gap between sounds (s; log2 spacing)"); ax2.set_ylabel(f"Mean response (dF/F, {response_range('noise_pair')[0]:g}-{response_range('noise_pair')[1]:g} s)")
    ax2.set_title("Response by order (mean of FOV means)\nsolid = different pair, dashed = same pair"); ax2.legend(frameon=False)
    fig.tight_layout(); d = out_dir / "selectivity_plots" / "noise_pair"; d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / "noise_pair_gap_dependence.png", dpi=250); plt.close(fig)


def write_report(path: Path, cells: pd.DataFrame, summary: pd.DataFrame, response_stats: dict[str,Any],
                 fov_sel_stats: dict[str, Any] | None = None, run_info: dict[str, Any] | None = None) -> None:
    blocks = _blocks_present(cells)
    lines=[f"SOUND_TUNING MULTISTIM FOV ANALYSIS {SCRIPT_VERSION}","="*72,"",
           "Primary replicate: FOV (same ROI population across sound blocks).",
           "Responsiveness: condition-specific sign-flip tests, BH-FDR across cells separately at each condition; union across conditions.",
           "Response windows: " + ", ".join(f"{b} {response_range(b)[0]:g}-{response_range(b)[1]:g} s" for b in blocks) + "; baseline -1-0 s.",""]
    if run_info:
        if run_info.get("pure_tone_level_db") is not None:
            lines.append(f"Pure-tone block level in FOVs with several levels: {run_info['pure_tone_level_db']:g} dB SPL")
        for sk in run_info.get("skipped_sessions", []):
            lines.append(f"  skipped {sk['date']}_{sk['session']} ({sk.get('sessionLabel')}): {sk['status']}")
        lines.append("")
    lines.append(f"FOVs: {cells['fov_uid'].nunique()} | cells/FOV rows: {len(cells)}")
    if not RED_RECORDED:
        lines.append("No red channel recorded (nchannels = 1): every cell is labeled GREEN (= unclassified); GREEN/YELLOW tests skipped.")
    for uid, g in cells.groupby("fov_uid"):
        bits = []
        for b in blocks:
            rc = f"{BLOCK_SHORT[b]}_responsive_fdr"
            if g[rc].notna().any(): bits.append(f"{BLOCK_SHORT[b]} {int(g[rc].fillna(False).astype(bool).sum())}")
        lines.append(f"  {uid} ({g.brainArea.iloc[0]}): n={len(g)} | responsive: " + ", ".join(bits))
        if "np_novelty_sig_fdr" in g and g["np_novelty_sig_fdr"].notna().any():
            sig = g["np_novelty_sig_fdr"].fillna(False).astype(bool); con = pd.to_numeric(g["np_novelty_contrast"], errors="coerce")
            lines.append(f"      noise-pair novelty contrast FDR-significant: {int((sig & (con > 0)).sum())} different > same, "
                         f"{int((sig & (con < 0)).sum())} same > different")
    if RED_RECORDED:
        lines += ["",f"GREEN vs YELLOW responsiveness (paired Wilcoxon across FOVs; Holm across {len(response_stats)} blocks):"]
        for b,r in response_stats.items():
            lines.append(f"  {b}: W={r.get('W',np.nan):.4g}, p={r.get('p',np.nan):.4g}, Holm p={r.get('p_holm_blocks',np.nan):.4g}, n={r.get('n_pairs',0)}")
    if fov_sel_stats:
        lines += ["", "Selectivity indices, responsive cells: median per FOV, Wilcoxon vs 0 within FOV (describes that FOV);",
                  "FOV medians vs 0 across FOVs (little power with few FOVs)."]
        for metric, rec in fov_sel_stats.get("responsive_only", {}).items():
            parts = [f"{uid.split('_')[-1]} {r['median']:+.2f} (p={r['p']:.2g}, n={r['n']})" for uid, r in rec["by_FOV"].items() if r["n"]]
            lines.append(f"  {metric}: " + "; ".join(parts) + f" | FOV medians p={rec['across_FOV_medians']['p']:.2g}")
    path.write_text("\n".join(lines)+"\n",encoding="utf-8")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    global RED_RECORDED
    args=parse_args(); subject=str(args.subject); dates=[str(x) for x in args.dates]; area=str(args.area)
    info_path,sessions=load_info2p(subject)
    skipped: list[dict[str,Any]]=[]
    selected=select_new_sound_sessions(sessions,dates,area,subject,parse_session_filter(args.sessions),
                                       parse_session_filter(args.exclude_sessions),skipped)
    if not selected:
        raise RuntimeError(f"No new sound_tuning sessions found for {subject}, area={area}, dates={dates}")
    assigned=assign_fovs(selected,args.fov_groups)
    pure_level=choose_pure_tone_level(assigned,args.pure_tone_level)
    assigned,other_levels=split_pure_tone_levels(assigned,pure_level)
    manifest_rows=validate_fov_groups(assigned)
    od=output_dirs(subject,area,dates)
    manifest=pd.DataFrame(manifest_rows)
    manifest.to_csv(od["root"]/"fov_manifest.csv",index=False)
    print("="*86); print(f"SOUND_TUNING MULTISTIM FOV ANALYSIS {SCRIPT_VERSION}"); print("="*86)
    print(f"Subject: {subject} | area: {area} | dates: {dates}")
    print(f"info2p: {info_path}"); print(f"Output: {od['root']}")
    print(manifest[["date","FOV#","session","block_type","level_db","sessionLabel","brainArea","depth","grouping_source"]].to_string(index=False))
    if pure_level is not None:
        print(f"\nFOVs with several pure-tone levels use the {pure_level:g} dB session as their pure_tones block; "
              f"other levels give per-cell BF only: {[s['date']+'_'+s['session']+' '+format(float(s['level_db']),'g')+' dB' for s in other_levels]}")
    for sk in skipped:
        print(f"Skipped {sk['date']}_{sk['session']} ({sk.get('sessionLabel')}): {sk['status']}")
    if any(manifest.grouping_source.str.contains("legacy_inferred",na=False)):
        print("\nWARNING: legacy inferred FOV grouping is provisional. Add FOV# to info2p or use --fov-groups for ambiguous days.")
    run_info={
        "script_version":SCRIPT_VERSION,"subject":subject,"dates":dates,"area":area,"plane":args.plane,
        "info2p_file":str(info_path),"TEMP_OUTPUT_PATH":str(settings.TEMP_OUTPUT_PATH),
        "FOV_field":"FOV#","FOV_numbering":"starts at 0; unique key = date + FOV#",
        "blocks":list(BLOCK_ORDER),"block_source":"behavior current_stim_type (sessionLabel only as fallback)",
        "response_window_s":{b:list(response_range(b)) for b in BLOCK_ORDER},"baseline_window_s":list(BASELINE_RANGE),
        "noise_pair_condition_code":"10 x index in "+str(list(NOISEPAIR_ORDERS))+" + gap (s)",
        "pure_tone_level_db":pure_level,
        "other_pure_tone_level_sessions":[{"date":s["date"],"session":s["session"],"FOV#":s.get("fov_number"),"level_db":s.get("level_db")} for s in other_levels],
        "bf_eligible":"pure tones: responsive (FDR) & response at BF > 0 & q at BF < 0.05","sessions_filter":args.sessions,"exclude_sessions":args.exclude_sessions,
        "skipped_sessions":skipped,
        "primary_replicate":"FOV","responsiveness":"condition-specific sign-flip + per-condition BH-FDR across cells; union",
        "n_permutations":args.n_permutations,"seed":args.seed,
    }
    save_json(od["root"]/"run_manifest.json",run_info)
    if args.dry_run:
        print("Dry run complete."); return

    groups: dict[str,list[dict[str,Any]]]={}
    for s in assigned: groups.setdefault(s["fov_uid"],[]).append(s)
    cell_tables=[]; fov_summaries=[]; failures=[]
    for gi,(uid,seq) in enumerate(sorted(groups.items())):
        fd=od["fov"]/uid; fd.mkdir(parents=True,exist_ok=True)
        print("\n"+"-"*86); print(f"FOV {uid}: {[x['session']+':'+x['block_type'] for x in seq]}")
        try:
            df,summ=merge_fov_blocks(seq,args.plane,fd,max(64,int(args.n_permutations)),int(args.seed)+10000*gi,
                                     not args.skip_cell_reports,[s for s in other_levels if s["fov_uid"]==uid])
            cell_tables.append(df); fov_summaries.append(summ)
        except Exception as exc:
            failures.append({"fov_uid":uid,"error":repr(exc),"traceback":traceback.format_exc()})
            print(f"FAILED {uid}: {exc}")
    save_json(od["root"]/"failures.json",failures)
    if not cell_tables:
        raise RuntimeError("No FOV completed successfully; see failures.json")
    cells=pd.concat(cell_tables,ignore_index=True,sort=False)
    red_fovs=cells.groupby("fov_uid")["red_channel_recorded"].first()
    RED_RECORDED=bool(red_fovs.any())
    if not RED_RECORDED:
        print("No FOV recorded a red channel: GREEN/YELLOW comparisons skipped; summaries use all cells.")
    elif not red_fovs.all():
        print(f"WARNING: FOVs without a red channel ({list(red_fovs[~red_fovs].index)}) have every cell labeled GREEN; "
              "their GREEN cells are unclassified, not tdTomato-negative.")
    cells.to_csv(od["combined"]/"combined_cell_results.csv",index=False)
    fs=fov_class_summary(cells); fs.to_csv(od["combined"]/"combined_fov_summary.csv",index=False)
    response_stats=plot_combined_responsiveness(fs,od["combined"])
    save_json(od["combined"]/"responsiveness_statistics.json",response_stats)
    fov_sel_stats=None
    if RED_RECORDED:
        plot_primary_selectivity_green_yellow(cells,od["combined"])
    else:
        fov_sel_stats=plot_selectivity_by_fov(cells,od["combined"])
    plot_combined_profiles(cells,od["combined"])
    plot_noise_pair_gap_dependence(cells,od["combined"])
    _save_combined_bf_outputs(cells,od["combined"])
    write_report(od["combined"]/"REPORT.txt",cells,fs,response_stats,fov_sel_stats,run_info)
    print("\n"+"="*86); print("DONE"); print(f"Successful FOVs: {len(cell_tables)}; failed: {len(failures)}"); print(f"Outputs: {od['root']}")


if __name__ == "__main__":
    main()
