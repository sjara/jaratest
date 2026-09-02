#!/usr/bin/env python3
"""
Batch/area-level analysis of two-photon am_tuning sessions.

This is the batch counterpart of:
    twophoton_am_tuning_EV_20260813_cellpose_updated.ipynb

It discovers all matching info2p sessions for one subject, auditory cortical area,
and date set, runs the finalized Cellpose-based GREEN/YELLOW classification and
AM-tuning analysis session-by-session, then combines sessions within the same
area and tuning mode.

Supported tuning modes
----------------------
* tuningFreq : pure-tone frequency tuning (stimType == Sine)
* tuningAM   : amplitude-modulation-rate tuning (stimType == AM)

The two modes are NEVER pooled together.  By default both are processed, but
combined outputs are written separately for tuningFreq and tuningAM.

Final GREEN/YELLOW classification
---------------------------------
GREEN  = functional GCaMP ROI without sufficient channel-2 anatomical overlap.
YELLOW = functional GCaMP ROI with sufficient channel-2 anatomical overlap.
RED    = Cellpose anatomical tdTomato object segmented from channel 2.

Cellpose settings match the finalized notebook:
    IoU cutoff        = 0.15
    cellprob threshold= -0.5
    flow threshold    = 0.5
    diameter          = median equivalent diameter of functional Suite2p ROIs

No functional ROI is excluded on the basis of legacy redcell.npy.

Session discovery
-----------------
* paradigm must be 'am_tuning'
* brainArea is canonicalized by substring:
      A1  <- contains 'A1'
      AAF <- contains 'AAF'
      A2  <- contains 'A2' or 'AuV'
* lowFreq/highFreq suffixes and depth are retained as metadata but do not
  filter the area-level analysis.

Imaging/behavior alignment
--------------------------
The acquisition-order rule from the finalized notebook is used:
* if imaging events == behavior trials, use them directly;
* if imaging has <= 5 extra sound events, keep the FIRST N behavior-matched
  events and treat the extras as trailing events;
* timing is validated using stimDur + isi;
* fewer imaging events than behavioral trials, too many extras, or failed
  timing QC causes that session to be skipped with ERROR.json.

Figures
-------
The expanded figure philosophy from the finalized sound_tuning v5 workflow is
used here as well:
* reliable stimulus-responsive/non-responsive GREEN/YELLOW figure;
* all-cell and FDR-responsive-only tuning curves;
* clean mean +/- SEM-only companions with optimized y axes and numeric values;
* amplitude-threshold and FDR-responsive selectivity rasters;
* GREEN/YELLOW summary metrics;
* intensity-resolved tuning profiles;
* condition-selectivity contrast (condition minus all other conditions),
  replacing the old d-prime analysis;
* session-level GREEN/YELLOW comparisons.

Statistics
----------
Pooled-cell tests are retained as exploratory/descriptive.  Primary combined
GREEN/YELLOW inference is additionally reported at the session level, using
paired GREEN and YELLOW summaries from the same imaging sessions.

Example
-------
python am_tuning_area_analysis.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730

Only frequency tuning:
python am_tuning_area_analysis.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730 \
    --mode tuningFreq

Dry run:
python am_tuning_area_analysis.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730 \
    --dry-run

Output root
-----------
<TEMP_OUTPUT_PATH>/evan/am_tuning_area_analysis/<subject>/<area>/<date_tag>/
    session_selection.csv
    run_manifest.json
    tuningFreq/
        session_outputs/<date>_<session>/...
        combined/...
    tuningAM/
        session_outputs/<date>_<session>/...
        combined/...
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import traceback
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from scipy import stats
import torch

from jaratoolbox import loadbehavior, settings, twophotonanalysis
from suite2p.detection.chan2detect import cellpose_overlap


# =============================================================================
# FINAL NOTEBOOK PARAMETERS
# =============================================================================

PARADIGM_PRIMARY = "am_tuning"
PARADIGM_FALLBACK = "am_tuning_curve"
PLANE_DEFAULT = 0
CELL_PROB_THRESHOLD = 0.001
TIME_RANGE = (-1.0, 3.0)
BASELINE_WINDOW = (-1.0, 0.0)
RESPONSE_WINDOW = (0.0, 1.0)

IOU_THRESHOLD = 0.15
OLD_IOU_THRESHOLD = 0.25
CELLPOSE_CELLPROB_THRESHOLD = -0.5
CELLPOSE_FLOW_THRESHOLD = 0.5
CELLPOSE_DIAMETER = None

RASTER_MIN_ABS_RESPONSE = 0.02
FDR_ALPHA = 0.05
N_PERMUTATIONS_DEFAULT = 20000
RANDOM_SEED_DEFAULT = 20260813

MAX_EXTRA_EVENTS = 5
MAX_MEAN_ABS_ERROR_S = 0.25
MAX_ABS_ERROR_S = 0.75

GREEN_COLOR = "forestgreen"
YELLOW_COLOR = "goldenrod"
DISPLAY_GREEN_COLOR = "lime"
DISPLAY_YELLOW_COLOR = "yellow"
ANATOMICAL_RED_COLOR = "red"
FUNCTIONAL_OUTLINE_LW = 0.25
RED_OUTLINE_LW = 0.45


# =============================================================================
# COMMAND LINE
# =============================================================================

def normalize_area_argument(value: str) -> str:
    upper = str(value).strip().upper()
    if upper == "AUV":
        return "A2"
    if upper in {"A1", "AAF", "A2"}:
        return upper
    raise argparse.ArgumentTypeError("Area must be A1, AAF, A2, or AuV.")


def normalize_dates(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        for piece in str(value).replace(",", " ").split():
            if len(piece) != 8 or not piece.isdigit():
                raise argparse.ArgumentTypeError(
                    f"Invalid date '{piece}'. Dates must be YYYYMMDD."
                )
            out.append(piece)
    if not out:
        raise argparse.ArgumentTypeError("At least one date is required.")
    return sorted(set(out))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("subject", help="Subject ID, e.g. imag039.")
    parser.add_argument(
        "--area", required=True, type=normalize_area_argument,
        help="Canonical area: A1, AAF, or A2 (AuV accepted as A2).",
    )
    parser.add_argument(
        "--dates", required=True, nargs="+",
        help="Dates to include, YYYYMMDD, separated by spaces or commas.",
    )
    parser.add_argument(
        "--mode", choices=["both", "tuningFreq", "tuningAM"], default="both",
        help="Tuning mode to analyze. Default: both, combined separately.",
    )
    parser.add_argument(
        "--plane", type=int, default=PLANE_DEFAULT,
        help=f"Suite2p plane number. Default: {PLANE_DEFAULT}.",
    )
    parser.add_argument(
        "--n-permutations", type=int, default=N_PERMUTATIONS_DEFAULT,
        help=f"Sign-flip permutations per cell. Default: {N_PERMUTATIONS_DEFAULT}.",
    )
    parser.add_argument(
        "--seed", type=int, default=RANDOM_SEED_DEFAULT,
        help=f"Random seed. Default: {RANDOM_SEED_DEFAULT}.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print matching info2p sessions without loading imaging data.",
    )
    args = parser.parse_args()
    args.dates = normalize_dates(args.dates)
    return args


# =============================================================================
# GENERAL HELPERS
# =============================================================================

def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        x = float(value)
        return x if np.isfinite(x) else None
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(jsonable(obj), f, indent=2)


def finite_values(values: Any) -> np.ndarray:
    arr = np.asarray(values, dtype=float).ravel()
    return arr[np.isfinite(arr)]


def mean_sem(values: Any) -> tuple[float, float, int]:
    vals = finite_values(values)
    n = len(vals)
    if n == 0:
        return np.nan, np.nan, 0
    mean = float(np.mean(vals))
    sem = float(stats.sem(vals)) if n > 1 else np.nan
    return mean, sem, n


def safe_divide(a: float, b: float) -> float:
    return float(a / b) if b else np.nan


def bh_fdr(p_values: np.ndarray) -> np.ndarray:
    p = np.asarray(p_values, dtype=float)
    q = np.full(p.shape, np.nan)
    valid = np.isfinite(p)
    pv = p[valid]
    if len(pv) == 0:
        return q
    order = np.argsort(pv)
    ranked = pv[order]
    m = len(ranked)
    adjusted = ranked * m / np.arange(1, m + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    adjusted = np.minimum(adjusted, 1.0)
    qv = np.empty_like(adjusted)
    qv[order] = adjusted
    q[valid] = qv
    return q


def holm_correct(p_values: list[float]) -> np.ndarray:
    p = np.asarray(p_values, dtype=float)
    out = np.full_like(p, np.nan)
    valid_idx = np.flatnonzero(np.isfinite(p))
    if len(valid_idx) == 0:
        return out
    vals = p[valid_idx]
    order = np.argsort(vals)
    sorted_vals = vals[order]
    m = len(sorted_vals)
    adj = np.maximum.accumulate(
        np.asarray([(m - i) * x for i, x in enumerate(sorted_vals)], dtype=float)
    )
    adj = np.minimum(adj, 1.0)
    unsorted = np.empty_like(adj)
    unsorted[order] = adj
    out[valid_idx] = unsorted
    return out


def safe_mannwhitney(a: Any, b: Any) -> dict[str, Any]:
    a = finite_values(a); b = finite_values(b)
    if len(a) == 0 or len(b) == 0:
        return {"n_a": len(a), "n_b": len(b), "U": None, "p": None}
    res = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {"n_a": len(a), "n_b": len(b), "U": float(res.statistic), "p": float(res.pvalue)}


def safe_paired_wilcoxon(a: Any, b: Any) -> dict[str, Any]:
    a = np.asarray(a, dtype=float).ravel(); b = np.asarray(b, dtype=float).ravel()
    valid = np.isfinite(a) & np.isfinite(b)
    a = a[valid]; b = b[valid]
    if len(a) == 0:
        return {"n_pairs": 0, "W": None, "p": None}
    d = b - a
    if np.allclose(d, 0, equal_nan=False):
        return {"n_pairs": len(a), "W": 0.0, "p": 1.0}
    try:
        res = stats.wilcoxon(b, a, alternative="two-sided", zero_method="wilcox")
        return {"n_pairs": len(a), "W": float(res.statistic), "p": float(res.pvalue)}
    except ValueError:
        return {"n_pairs": len(a), "W": None, "p": None}


def optimized_summary_ylim(
    ax, means: Any, errors: Any | None = None, reference_values: tuple[float, ...] = (),
    pad_fraction: float = 0.18,
) -> None:
    means = np.asarray(means, dtype=float).ravel()
    if errors is None:
        errors = np.zeros_like(means)
    else:
        errors = np.asarray(errors, dtype=float).ravel()
        if len(errors) != len(means):
            errors = np.resize(errors, means.shape)
    finite = np.isfinite(means)
    vals: list[float] = []
    if np.any(finite):
        err = np.where(np.isfinite(errors), errors, 0.0)
        vals.extend((means[finite] - err[finite]).tolist())
        vals.extend((means[finite] + err[finite]).tolist())
    vals.extend([float(x) for x in reference_values if np.isfinite(x)])
    vals = [x for x in vals if np.isfinite(x)]
    if not vals:
        return
    lo, hi = min(vals), max(vals)
    span = hi - lo
    if span <= 0:
        span = max(abs(lo), 0.05)
    pad = max(span * pad_fraction, 0.02 * max(abs(lo), abs(hi), 0.05))
    ax.set_ylim(lo - pad, hi + pad)


def apply_robust_y_limits(ax, values: Any, reference_values: tuple[float, ...] = ()) -> None:
    vals = finite_values(values)
    if len(vals) == 0:
        return
    if len(vals) >= 4:
        q1, q3 = np.percentile(vals, [25, 75])
        iqr = q3 - q1
        if iqr > 0:
            lo_fence, hi_fence = q1 - 3 * iqr, q3 + 3 * iqr
            shown = vals[(vals >= lo_fence) & (vals <= hi_fence)]
            if len(shown) == 0:
                shown = vals
        else:
            shown = vals
    else:
        shown = vals
    lo, hi = float(np.min(shown)), float(np.max(shown))
    refs = [x for x in reference_values if np.isfinite(x)]
    if refs:
        lo = min(lo, *refs); hi = max(hi, *refs)
    span = hi - lo
    if span <= 0:
        span = max(abs(lo), 0.05)
    pad = 0.12 * span
    ax.set_ylim(lo - pad, hi + pad)


def signflip_pvalues_grouped(matrix: np.ndarray, n_permutations: int, rng: np.random.Generator) -> np.ndarray:
    """Two-sided sign-flip p-values for rows of cells x trials, grouped by finite count."""
    x = np.asarray(matrix, dtype=float)
    n_cells = x.shape[0]
    p = np.full(n_cells, np.nan)
    nfinite = np.sum(np.isfinite(x), axis=1)
    for n in np.unique(nfinite):
        if n < 2:
            continue
        inds = np.flatnonzero(nfinite == n)
        # Ragged finite values are compressed per cell because all have equal n here.
        vals = np.vstack([x[i, np.isfinite(x[i])] for i in inds])
        obs = np.abs(np.mean(vals, axis=1))
        exceed = np.zeros(len(inds), dtype=np.int64)
        batch = 1000
        remaining = int(n_permutations)
        while remaining > 0:
            b = min(batch, remaining)
            signs = rng.choice(np.array([-1.0, 1.0]), size=(b, n))
            perm_means = np.abs((vals @ signs.T) / n)
            exceed += np.sum(perm_means >= obs[:, None], axis=1)
            remaining -= b
        p[inds] = (exceed + 1) / (n_permutations + 1)
    return p


# =============================================================================
# SESSION DISCOVERY
# =============================================================================

def canonical_brain_area(brain_area: Any) -> str | None:
    upper = str(brain_area).upper()
    if "AAF" in upper:
        return "AAF"
    if "A1" in upper:
        return "A1"
    if "A2" in upper or "AUV" in upper:
        return "A2"
    return None


def canonical_tuning_mode_from_label(label: Any) -> str | None:
    text = str(label).strip().lower()
    if text == "tuningfreq" or "tuningfreq" in text:
        return "tuningFreq"
    if text == "tuningam" or "tuningam" in text:
        return "tuningAM"
    return None


def load_info2p_sessions(subject: str) -> tuple[Path, list[dict[str, Any]]]:
    info_file = Path(settings.INFO2P_PATH) / f"{subject}_info2p.py"
    if not info_file.exists():
        raise FileNotFoundError(f"Subject info2p file not found:\n{info_file}")
    spec = importlib.util.spec_from_file_location(f"_am_batch_{subject}", info_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not import info2p file:\n{info_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sessions = getattr(module, "sessions", None)
    if sessions is None:
        raise AttributeError(f"No sessions list in:\n{info_file}")
    return info_file, list(sessions)


def select_sessions(
    sessions: list[dict[str, Any]], dates: list[str], area: str, mode: str
) -> list[dict[str, Any]]:
    date_set = set(dates)
    selected: list[dict[str, Any]] = []
    for sess in sessions:
        if str(sess.get("date", "")) not in date_set:
            continue
        if str(sess.get("paradigm", "")) != PARADIGM_PRIMARY:
            continue
        canon_area = canonical_brain_area(sess.get("brainArea", ""))
        if canon_area != area:
            continue
        label_mode = canonical_tuning_mode_from_label(sess.get("sessionLabel", ""))
        if mode != "both" and label_mode is not None and label_mode != mode:
            continue
        item = dict(sess)
        item["canonicalArea"] = canon_area
        item["info2p_tuningMode"] = label_mode
        selected.append(item)
    selected.sort(key=lambda s: (str(s.get("date", "")), str(s.get("session", ""))))
    return selected


def selection_dataframe(selected: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for s in selected:
        rows.append({
            "subject": s.get("subject"), "date": str(s.get("date")),
            "session": str(s.get("session")), "brainArea": s.get("brainArea"),
            "canonicalArea": s.get("canonicalArea"), "depth": s.get("depth"),
            "sessionLabel": s.get("sessionLabel"), "paradigm": s.get("paradigm"),
            "info2p_tuningMode": s.get("info2p_tuningMode"),
        })
    return pd.DataFrame(rows)


# =============================================================================
# IMAGE / CELLPOSE HELPERS
# =============================================================================

def robust_image_limits(image: np.ndarray) -> tuple[float, float]:
    vals = np.asarray(image, dtype=float)
    finite = vals[np.isfinite(vals)]
    if len(finite) == 0:
        return 0.0, 1.0
    lo, hi = np.percentile(finite, [1, 99.7])
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        lo, hi = float(np.min(finite)), float(np.max(finite))
    return float(lo), float(hi)


def draw_binary_mask_contour(ax, binary_mask, color, linewidth):
    if np.any(binary_mask):
        ax.contour(binary_mask.astype(float), levels=[0.5], colors=[color], linewidths=linewidth)


def draw_functional_roi_contour(ax, roi_stat, color, linewidth, Ly, Lx):
    ypix = np.asarray(roi_stat["ypix"], dtype=int)
    xpix = np.asarray(roi_stat["xpix"], dtype=int)
    valid = (ypix >= 0) & (ypix < Ly) & (xpix >= 0) & (xpix < Lx)
    ypix = ypix[valid]; xpix = xpix[valid]
    if len(xpix) == 0:
        return
    pad = 2
    xmin = max(0, int(np.min(xpix)) - pad); xmax = min(Lx - 1, int(np.max(xpix)) + pad)
    ymin = max(0, int(np.min(ypix)) - pad); ymax = min(Ly - 1, int(np.max(ypix)) + pad)
    local = np.zeros((ymax-ymin+1, xmax-xmin+1), dtype=float)
    local[ypix-ymin, xpix-xmin] = 1.0
    ax.contour(
        local, levels=[0.5], colors=[color], linewidths=linewidth, origin="upper",
        extent=[xmin-0.5, xmax+0.5, ymax+0.5, ymin-0.5],
    )


def red_labels_overlapping_yellow(
    red_masks: np.ndarray, functional_stats: np.ndarray, yellow_mask: np.ndarray
) -> set[int]:
    Ly, Lx = red_masks.shape
    labels: set[int] = set()
    for i in np.flatnonzero(yellow_mask):
        stat_i = functional_stats[i]
        y = np.asarray(stat_i["ypix"], dtype=int); x = np.asarray(stat_i["xpix"], dtype=int)
        valid = (y >= 0) & (y < Ly) & (x >= 0) & (x < Lx)
        vals = np.unique(red_masks[y[valid], x[valid]])
        labels.update(int(v) for v in vals if int(v) > 0)
    return labels


def save_classification_overlay(
    image: np.ndarray, image_name: str, functional_stats: np.ndarray,
    red_masks: np.ndarray, green_mask: np.ndarray, yellow_mask: np.ndarray,
    output_path: Path, title: str,
) -> None:
    Ly, Lx = image.shape
    vmin, vmax = robust_image_limits(image)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image, cmap="gray", vmin=vmin, vmax=vmax)
    hidden = red_labels_overlapping_yellow(red_masks, functional_stats, yellow_mask)
    for i in np.flatnonzero(green_mask):
        draw_functional_roi_contour(ax, functional_stats[i], DISPLAY_GREEN_COLOR, FUNCTIONAL_OUTLINE_LW, Ly, Lx)
    for lab in range(1, int(np.max(red_masks)) + 1):
        if lab in hidden:
            continue
        draw_binary_mask_contour(ax, red_masks == lab, ANATOMICAL_RED_COLOR, RED_OUTLINE_LW)
    for i in np.flatnonzero(yellow_mask):
        draw_functional_roi_contour(ax, functional_stats[i], DISPLAY_YELLOW_COLOR, FUNCTIONAL_OUTLINE_LW, Ly, Lx)
    handles = [
        Line2D([0],[0], color=DISPLAY_GREEN_COLOR, lw=1.5, label=f"Green functional (n={np.sum(green_mask)})"),
        Line2D([0],[0], color=DISPLAY_YELLOW_COLOR, lw=1.5, label=f"Yellow functional (n={np.sum(yellow_mask)})"),
        Line2D([0],[0], color=ANATOMICAL_RED_COLOR, lw=1.5, label=f"Red anatomical visible (n={int(np.max(red_masks))-len(hidden)})"),
    ]
    ax.legend(handles=handles, loc="upper right", fontsize=8, frameon=True)
    ax.set_title(f"{title}\nBackground: {image_name}; yellow priority over red")
    ax.set_axis_off()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# LOADING / ALIGNMENT / MODE DETECTION
# =============================================================================

def load_am_twophoton(subject: str, date: str, session: str, plane: int):
    candidates = [PARADIGM_PRIMARY, PARADIGM_FALLBACK]
    errors = []
    for paradigm in candidates:
        try:
            behavior_path = Path(loadbehavior.path_to_behavior_data(subject, paradigm, f"{date}_{session}"))
            if not behavior_path.exists():
                continue
            obj = twophotonanalysis.TwoPhoton(subject, date, session, plane, paradigm=paradigm)
            return obj, paradigm, behavior_path
        except Exception as exc:
            errors.append(f"{paradigm}: {exc}")
    raise FileNotFoundError(
        "Could not load am_tuning behavior/two-photon data. Attempts:\n" + "\n".join(errors)
    )


def detect_tuning_mode(data2p) -> tuple[str, str, str]:
    stim_type_raw = np.asarray(data2p.bdata["stimType"]).ravel()
    unique = np.unique(stim_type_raw)
    if len(unique) != 1:
        raise ValueError(f"Expected one stimType for session, found {unique}.")
    value = unique[0]
    if isinstance(value, (str, np.str_)):
        name = str(value)
    else:
        menu = ["Sine", "Chord", "Noise", "AM", "ToneTrain", "Laser", "LaserTrain", "Light"]
        idx = int(value)
        if idx < 0 or idx >= len(menu):
            raise ValueError(f"Unknown stimType value: {value}")
        name = menu[idx]
    if name == "Sine":
        return "tuningFreq", "Tone frequency (kHz)", "Pure-tone frequency tuning"
    if name == "AM":
        return "tuningAM", "AM rate (Hz)", "AM-rate tuning"
    raise ValueError(f"Only Sine and AM sessions are supported; stimType={name!r}.")


def align_events(data2p, eventlocked: np.ndarray, valid_events: np.ndarray, n_behavior_trials: int,
                 stim_duration: np.ndarray, isi: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    n_imaging = int(eventlocked.shape[1])
    if n_imaging < n_behavior_trials:
        raise ValueError(
            f"Fewer imaging events than behavioral trials: {n_imaging} vs {n_behavior_trials}."
        )
    extra = n_imaging - n_behavior_trials
    if extra > MAX_EXTRA_EVENTS:
        raise ValueError(
            f"Unexpected mismatch: {n_imaging} imaging events vs {n_behavior_trials} behavioral trials "
            f"({extra} extra); automatic trimming limited to <= {MAX_EXTRA_EVENTS}."
        )
    aligned = eventlocked[:, :n_behavior_trials, :]
    valid_aligned = np.asarray(valid_events[:n_behavior_trials], dtype=bool)
    onset = np.asarray(data2p.event_onset[:n_behavior_trials], dtype=float)
    expected = stim_duration[:n_behavior_trials-1] + isi[:n_behavior_trials-1]
    observed = np.diff(onset) / float(data2p.srate)
    finite = np.isfinite(expected) & np.isfinite(observed)
    if not np.any(finite):
        raise ValueError("No finite intervals available for alignment QC.")
    err = observed[finite] - expected[finite]
    mae = float(np.mean(np.abs(err))); maxerr = float(np.max(np.abs(err)))
    if mae > MAX_MEAN_ABS_ERROR_S or maxerr > MAX_ABS_ERROR_S:
        raise ValueError(
            f"First-event alignment failed timing QC. MAE={mae:.4f}s, max error={maxerr:.4f}s."
        )
    diag = {
        "n_imaging_events": n_imaging, "n_behavior_trials": n_behavior_trials,
        "n_extra_imaging_events": extra, "n_extra_before": 0, "n_extra_after": extra,
        "timing_mae_s": mae, "timing_max_abs_error_s": maxerr,
        "alignment_note": f"Used first {n_behavior_trials} imaging events; ignored {extra} trailing extras.",
    }
    return aligned, valid_aligned, diag


# =============================================================================
# PER-SESSION ANALYSIS
# =============================================================================

def analyze_session(meta: dict[str, Any], plane: int, n_permutations: int, seed: int,
                    session_output_dir: Path) -> dict[str, Any]:
    subject = str(meta["subject"]); date = str(meta["date"]); session = str(meta["session"])
    session_output_dir.mkdir(parents=True, exist_ok=True)
    print("\n" + "="*78)
    print(f"SESSION {subject} {date} {session} | {meta.get('brainArea')} | depth={meta.get('depth')}")
    print("="*78)

    data2p, behavior_paradigm, behavior_path = load_am_twophoton(subject, date, session, plane)
    tuning_mode, tuning_axis_label, tuning_title = detect_tuning_mode(data2p)
    expected_mode = meta.get("info2p_tuningMode")
    if expected_mode is not None and expected_mode != tuning_mode:
        raise ValueError(
            f"info2p sessionLabel implies {expected_mode}, but behavior stimType implies {tuning_mode}."
        )
    print(f"Detected tuning mode: {tuning_mode}")
    print(f"Behavior file: {behavior_path}")

    suite2p_dir = Path(data2p.data_path).expanduser().resolve()
    required = [suite2p_dir / x for x in ("ops.npy", "iscell.npy", "stat.npy")]
    missing = [str(x) for x in required if not x.exists()]
    if missing:
        raise FileNotFoundError("Missing Suite2p files:\n" + "\n".join(missing))

    # Define cell set once.
    iscell = np.asarray(data2p.iscell)
    cell_mask = (iscell[:, 0] == 1) & (iscell[:, 1] > CELL_PROB_THRESHOLD)
    cell_roi_indices = np.flatnonzero(cell_mask)
    eventlocked_all, tvec, valid_events = data2p.event_locked_average(time_range=list(TIME_RANGE), dff=True)
    valid_events = np.asarray(valid_events, dtype=bool).ravel()
    eventlocked = np.asarray(eventlocked_all[cell_mask], dtype=float)
    n_cells = eventlocked.shape[0]
    print(f"Analysis cells: {n_cells} / {eventlocked_all.shape[0]} Suite2p ROIs")

    # Cellpose classification.
    ops = np.load(suite2p_dir / "ops.npy", allow_pickle=True).item()
    stat_all = np.load(suite2p_dir / "stat.npy", allow_pickle=True)
    functional_stats = stat_all[np.asarray(cell_roi_indices, dtype=int)]
    if "meanImg_chan2" in ops and ops["meanImg_chan2"] is not None:
        red_image = np.asarray(ops["meanImg_chan2"], dtype=float); red_image_name = "meanImg_chan2"
    elif "meanImg_chan2_corrected" in ops and ops["meanImg_chan2_corrected"] is not None:
        red_image = np.asarray(ops["meanImg_chan2_corrected"], dtype=float); red_image_name = "meanImg_chan2_corrected"
    else:
        raise KeyError("No channel-2 mean image found in ops.npy.")
    equiv = np.asarray([2*np.sqrt(len(s["ypix"])/np.pi) for s in functional_stats if len(s["ypix"]) > 0], dtype=float)
    if len(equiv) == 0:
        raise ValueError("Could not estimate Cellpose diameter.")
    diameter = float(np.nanmedian(equiv)) if CELLPOSE_DIAMETER is None else float(CELLPOSE_DIAMETER)
    cp_settings = {"cellprob_threshold": CELLPOSE_CELLPROB_THRESHOLD, "flow_threshold": CELLPOSE_FLOW_THRESHOLD}
    print(f"Running Cellpose: diameter={diameter:.2f}, cellprob={CELLPOSE_CELLPROB_THRESHOLD}, flow={CELLPOSE_FLOW_THRESHOLD}, IoU={IOU_THRESHOLD}")
    redstats, red_masks = cellpose_overlap(
        functional_stats, red_image, diameter=diameter, chan2_threshold=IOU_THRESHOLD,
        device=torch.device("cpu"), settings=cp_settings,
    )
    red_iou = np.asarray(redstats[:, 1], dtype=float)
    yellow_mask = red_iou > IOU_THRESHOLD
    green_mask = ~yellow_mask
    n_green = int(np.sum(green_mask)); n_yellow = int(np.sum(yellow_mask))
    print(f"Cellpose anatomical tdTomato ROIs: {int(np.max(red_masks))}")
    print(f"Green functional: {n_green}; Yellow functional: {n_yellow}")

    # Legacy red score optional metadata only.
    legacy_scores = np.full(n_cells, np.nan)
    redcell_path = suite2p_dir / "redcell.npy"
    if redcell_path.exists():
        legacy = np.asarray(np.load(redcell_path, allow_pickle=True))
        if legacy.ndim == 2 and legacy.shape[1] >= 2 and np.max(cell_roi_indices, initial=-1) < legacy.shape[0]:
            legacy_scores = legacy[cell_roi_indices, 1].astype(float)

    # Save overlays.
    title = f"{subject} {date} {session} p{plane} | {tuning_mode}"
    save_classification_overlay(
        red_image, red_image_name, functional_stats, np.asarray(red_masks), green_mask, yellow_mask,
        session_output_dir / "classification_overlay_chan2.png", title,
    )
    if "meanImg" in ops and ops["meanImg"] is not None:
        mean1 = np.asarray(ops["meanImg"], dtype=float)
        if mean1.shape == red_image.shape:
            save_classification_overlay(
                mean1, "meanImg (chan1)", functional_stats, np.asarray(red_masks), green_mask, yellow_mask,
                session_output_dir / "classification_overlay_chan1.png", title,
            )
    np.savez(
        session_output_dir / "green_yellow_classification.npz",
        cell_roi_indices=np.asarray(cell_roi_indices, dtype=int), green_only_mask=green_mask,
        yellow_cell_mask=yellow_mask, cellpose_red_iou=red_iou,
        iou_threshold=IOU_THRESHOLD, cellpose_cellprob_threshold=CELLPOSE_CELLPROB_THRESHOLD,
        cellpose_flow_threshold=CELLPOSE_FLOW_THRESHOLD, cellpose_diameter=diameter,
    )

    # Behavior arrays.
    current_value = np.asarray(data2p.bdata["currentFreq"], dtype=float).ravel()
    current_intensity = np.asarray(data2p.bdata["currentIntensity"], dtype=float).ravel()
    stim_duration = np.asarray(data2p.bdata["stimDur"], dtype=float).ravel()
    isi = np.asarray(data2p.bdata["isi"], dtype=float).ravel()
    try:
        laser_trial = np.asarray(data2p.bdata["laserTrial"]).astype(bool).ravel()
    except (KeyError, TypeError):
        laser_trial = np.zeros(len(current_value), dtype=bool)
    lengths = {"currentFreq":len(current_value), "currentIntensity":len(current_intensity),
               "stimDur":len(stim_duration), "isi":len(isi), "laserTrial":len(laser_trial)}
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Behavioral arrays have different lengths: {lengths}")
    n_beh = len(current_value)
    eventlocked_aligned, valid_aligned, align_diag = align_events(
        data2p, eventlocked, valid_events, n_beh, stim_duration, isi
    )
    print("Trial alignment:")
    print(f"  imaging events: {align_diag['n_imaging_events']}; behavior trials: {n_beh}; trailing ignored: {align_diag['n_extra_after']}")
    print(f"  timing MAE={align_diag['timing_mae_s']:.4f}s; max={align_diag['timing_max_abs_error_s']:.4f}s")

    analysis_trials = valid_aligned & ~laser_trial
    possible_values = np.sort(np.unique(current_value[analysis_trials]))
    possible_intensities = np.sort(np.unique(current_intensity[analysis_trials]))
    if len(possible_values) == 0:
        raise ValueError("No valid non-laser tuning trials.")
    plot_values = possible_values / 1000.0 if tuning_mode == "tuningFreq" else possible_values.copy()

    baseline_mask = (tvec >= BASELINE_WINDOW[0]) & (tvec < BASELINE_WINDOW[1])
    response_mask = (tvec >= RESPONSE_WINDOW[0]) & (tvec <= RESPONSE_WINDOW[1])
    if not np.any(baseline_mask) or not np.any(response_mask):
        raise ValueError("Event-locked time vector does not cover baseline/response windows.")
    trial_baseline = np.nanmean(eventlocked_aligned[:, :, baseline_mask], axis=2, keepdims=True)
    eventlocked_bc = eventlocked_aligned - trial_baseline
    trial_response = np.nanmean(eventlocked_bc[:, :, response_mask], axis=2)

    n_int = len(possible_intensities); n_val = len(possible_values)
    condition_responses = np.full((n_cells, n_int, n_val), np.nan)
    condition_counts = np.zeros((n_int, n_val), dtype=int)
    condition_masks: list[np.ndarray] = []
    condition_names: list[str] = []
    condition_pairs: list[tuple[float,float]] = []
    for ii, intensity in enumerate(possible_intensities):
        for vi, value in enumerate(possible_values):
            mask = analysis_trials & np.isclose(current_intensity, intensity) & np.isclose(current_value, value)
            condition_counts[ii, vi] = int(np.sum(mask))
            if np.any(mask):
                condition_responses[:, ii, vi] = np.nanmean(trial_response[:, mask], axis=1)
            condition_masks.append(mask.copy())
            condition_pairs.append((float(value), float(intensity)))
            if tuning_mode == "tuningFreq":
                condition_names.append(f"{value/1000:g} kHz, {intensity:g} dB")
            else:
                condition_names.append(f"{value:g} Hz AM, {intensity:g} dB")
    condition_responses_flat = condition_responses.reshape(n_cells, n_int*n_val)

    tuning_curves = np.full((n_cells, n_val), np.nan)
    tuning_counts = np.zeros(n_val, dtype=int)
    for vi, value in enumerate(possible_values):
        mask = analysis_trials & np.isclose(current_value, value)
        tuning_counts[vi] = int(np.sum(mask))
        if np.any(mask):
            tuning_curves[:, vi] = np.nanmean(trial_response[:, mask], axis=1)

    # Reliable stimulus response using all analysis trials.
    stim_evoked = np.where(analysis_trials[None, :], trial_response, np.nan)
    mean_stim = np.nanmean(stim_evoked, axis=1)
    median_stim = np.nanmedian(stim_evoked, axis=1)
    sd_stim = np.nanstd(stim_evoked, axis=1, ddof=1)
    nfinite = np.sum(np.isfinite(stim_evoked), axis=1)
    sem_stim = np.full(n_cells, np.nan); ok = nfinite > 1
    sem_stim[ok] = sd_stim[ok] / np.sqrt(nfinite[ok])
    dz = np.full(n_cells, np.nan); okdz = ok & np.isfinite(sd_stim) & (sd_stim > 0)
    dz[okdz] = mean_stim[okdz] / sd_stim[okdz]
    rng = np.random.default_rng(seed + int(date[-4:]) + int(session))
    pvals = signflip_pvalues_grouped(stim_evoked, n_permutations, rng)
    qvals = bh_fdr(pvals)
    responsive_fdr = np.isfinite(qvals) & (qvals < FDR_ALPHA)
    excited_fdr = responsive_fdr & (mean_stim > 0)
    suppressed_fdr = responsive_fdr & (mean_stim < 0)

    # Amplitude-threshold raster criterion.
    peak_abs_condition = np.full(n_cells, np.nan)
    finite_rows = np.any(np.isfinite(condition_responses_flat), axis=1)
    peak_abs_condition[finite_rows] = np.nanmax(np.abs(condition_responses_flat[finite_rows]), axis=1)
    amplitude_responsive = np.isfinite(peak_abs_condition) & (peak_abs_condition > RASTER_MIN_ABS_RESPONSE)

    # Tuning metrics.
    preferred_index = np.full(n_cells, -1, dtype=int)
    preferred_value = np.full(n_cells, np.nan)
    best_response = np.full(n_cells, np.nan)
    peak_abs_response = np.full(n_cells, np.nan)
    modulation_depth = np.full(n_cells, np.nan)
    selectivity_contrast = np.full(n_cells, np.nan)
    selectivity_index = np.full(n_cells, np.nan)
    for ci in np.flatnonzero(np.any(np.isfinite(tuning_curves), axis=1)):
        curve = tuning_curves[ci]; finite = np.isfinite(curve); inds = np.flatnonzero(finite)
        best_idx = int(inds[int(np.nanargmax(curve[finite]))])
        best = float(curve[best_idx])
        preferred_index[ci] = best_idx; preferred_value[ci] = possible_values[best_idx]
        best_response[ci] = best
        peak_abs_response[ci] = float(np.nanmax(np.abs(curve)))
        modulation_depth[ci] = float(np.nanmax(curve) - np.nanmin(curve))
        other = finite.copy(); other[best_idx] = False
        if np.any(other):
            mean_other = float(np.nanmean(curve[other])); contrast = best - mean_other
            denom = abs(best) + abs(mean_other)
            selectivity_contrast[ci] = contrast
            if denom > 1e-12:
                selectivity_index[ci] = contrast / denom

    # Condition selectivity contrast = this condition - all other tuning conditions.
    mask_matrix = np.vstack(condition_masks)
    all_tuning_trials = np.any(mask_matrix, axis=0)
    cond_selectivity = np.full((n_cells, len(condition_masks)), np.nan)
    for k, this_mask in enumerate(mask_matrix):
        this_trials = this_mask & all_tuning_trials
        other_trials = all_tuning_trials & ~this_trials
        if np.any(this_trials) and np.any(other_trials):
            cond_selectivity[:, k] = (
                np.nanmean(trial_response[:, this_trials], axis=1)
                - np.nanmean(trial_response[:, other_trials], axis=1)
            )

    cell_class = np.where(yellow_mask, "yellow", "green")
    rows: list[dict[str, Any]] = []
    for ci in range(n_cells):
        row: dict[str, Any] = {
            "subject": subject, "date": date, "session": session,
            "session_key": f"{date}_{session}", "brainArea": meta.get("brainArea"),
            "canonicalArea": meta.get("canonicalArea"), "depth": meta.get("depth"),
            "sessionLabel": meta.get("sessionLabel"), "plane": plane,
            "tuning_mode": tuning_mode, "analysis_cell_index": ci,
            "suite2p_roi_index": int(cell_roi_indices[ci]), "cell_class": cell_class[ci],
            "cellpose_red_iou": float(red_iou[ci]), "suite2p_chan2_score": float(legacy_scores[ci]),
            "stim_response_mean": float(mean_stim[ci]), "stim_response_median": float(median_stim[ci]),
            "stim_response_sem": float(sem_stim[ci]), "stim_response_dz": float(dz[ci]),
            "stim_response_p": float(pvals[ci]), "stim_response_q": float(qvals[ci]),
            "stim_responsive_fdr": bool(responsive_fdr[ci]), "stim_excited_fdr": bool(excited_fdr[ci]),
            "stim_suppressed_fdr": bool(suppressed_fdr[ci]),
            "best_tuning_response": float(best_response[ci]), "peak_absolute_response": float(peak_abs_response[ci]),
            "tuning_modulation_depth": float(modulation_depth[ci]),
            "tuning_selectivity_contrast": float(selectivity_contrast[ci]),
            "tuning_selectivity_index": float(selectivity_index[ci]),
            "preferred_tuning_value_Hz": float(preferred_value[ci]),
            "amplitude_responsive_0p02": bool(amplitude_responsive[ci]),
        }
        for vi, value in enumerate(possible_values):
            prefix = "response_freq" if tuning_mode == "tuningFreq" else "response_AM"
            row[f"{prefix}_{value:g}_Hz"] = float(tuning_curves[ci, vi])
        rows.append(row)
    cell_df = pd.DataFrame(rows)
    cell_df.to_csv(session_output_dir / "cell_results.csv", index=False)

    # Long condition table retains intensity information for combined plots.
    condition_rows = []
    for ci in range(n_cells):
        for k, ((value, intensity), cname) in enumerate(zip(condition_pairs, condition_names)):
            ii = int(np.flatnonzero(np.isclose(possible_intensities, intensity))[0])
            vi = int(np.flatnonzero(np.isclose(possible_values, value))[0])
            condition_rows.append({
                "subject":subject, "date":date, "session":session, "session_key":f"{date}_{session}",
                "brainArea":meta.get("brainArea"), "canonicalArea":meta.get("canonicalArea"), "depth":meta.get("depth"),
                "tuning_mode":tuning_mode, "analysis_cell_index":ci, "suite2p_roi_index":int(cell_roi_indices[ci]),
                "cell_class":cell_class[ci], "stim_responsive_fdr":bool(responsive_fdr[ci]),
                "amplitude_responsive_0p02":bool(amplitude_responsive[ci]),
                "tuning_value_Hz":value, "intensity_dB":intensity, "condition_name":cname,
                "condition_response":float(condition_responses[ci, ii, vi]),
                "condition_selectivity_contrast":float(cond_selectivity[ci, k]),
                "n_trials_condition":int(condition_counts[ii, vi]),
            })
    condition_df = pd.DataFrame(condition_rows)
    condition_df.to_csv(session_output_dir / "condition_results.csv", index=False)

    # One row per session x class for primary combined inference.
    class_rows = []
    metrics = [
        "stim_response_mean", "best_tuning_response", "peak_absolute_response",
        "tuning_modulation_depth", "tuning_selectivity_contrast", "tuning_selectivity_index",
    ]
    for cls in ("green", "yellow"):
        sub = cell_df[cell_df.cell_class == cls]
        r: dict[str, Any] = {
            "subject":subject, "date":date, "session":session, "session_key":f"{date}_{session}",
            "brainArea":meta.get("brainArea"), "canonicalArea":meta.get("canonicalArea"), "depth":meta.get("depth"),
            "tuning_mode":tuning_mode, "cell_class":cls, "n_cells":len(sub),
            "n_stim_responsive_fdr":int(sub.stim_responsive_fdr.sum()),
            "pct_stim_responsive_fdr":100*safe_divide(int(sub.stim_responsive_fdr.sum()), len(sub)),
            "n_stim_excited_fdr":int(sub.stim_excited_fdr.sum()),
            "pct_stim_excited_fdr":100*safe_divide(int(sub.stim_excited_fdr.sum()), len(sub)),
            "n_stim_suppressed_fdr":int(sub.stim_suppressed_fdr.sum()),
            "pct_stim_suppressed_fdr":100*safe_divide(int(sub.stim_suppressed_fdr.sum()), len(sub)),
            "n_amplitude_responsive_0p02":int(sub.amplitude_responsive_0p02.sum()),
            "pct_amplitude_responsive_0p02":100*safe_divide(int(sub.amplitude_responsive_0p02.sum()), len(sub)),
        }
        for metric in metrics:
            r[f"mean_{metric}"] = float(np.nanmean(sub[metric])) if np.any(np.isfinite(sub[metric])) else np.nan
            r[f"median_{metric}"] = float(np.nanmedian(sub[metric])) if np.any(np.isfinite(sub[metric])) else np.nan
        class_rows.append(r)
    class_summary_df = pd.DataFrame(class_rows)
    class_summary_df.to_csv(session_output_dir / "session_class_summary.csv", index=False)

    save_json(session_output_dir / "session_summary.json", {
        "metadata": meta, "behavior_paradigm": behavior_paradigm, "behavior_path": behavior_path,
        "suite2p_dir": suite2p_dir, "tuning_mode": tuning_mode,
        "n_total_suite2p_rois": int(data2p.roiF.shape[0]), "n_analysis_cells": n_cells,
        "n_green":n_green, "n_yellow":n_yellow, "n_red_anatomical":int(np.max(red_masks)),
        "legacy_chan2_score_used_for_exclusion":False, "cellpose_diameter":diameter,
        "possible_tuning_values_Hz":possible_values, "possible_intensities_dB":possible_intensities,
        "condition_counts":condition_counts, **align_diag,
    })

    # Per-session responsive figure + tuning figures.
    sound_responsiveness_figure(cell_df, session_output_dir / "stim_responsive_cells_green_yellow.png", title)
    tuning_curve_figures(cell_df, tuning_mode, possible_values, session_output_dir, title)
    tuning_raster_figures(cell_df, tuning_mode, possible_values, session_output_dir, title)
    green_yellow_metric_figures(cell_df, session_output_dir, title)
    condition_profile_figures(condition_df, tuning_mode, session_output_dir, title)

    return {
        "meta":meta, "tuning_mode":tuning_mode, "cell_df":cell_df,
        "condition_df":condition_df, "class_summary_df":class_summary_df,
        "possible_values":possible_values, "possible_intensities":possible_intensities,
    }


# =============================================================================
# FIGURE HELPERS
# =============================================================================

def sound_responsiveness_figure(cell_df: pd.DataFrame, output_path: Path, title: str) -> None:
    df = cell_df.reset_index(drop=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
    ax = axes[0]
    for cls, color in (("green", GREEN_COLOR), ("yellow", YELLOW_COLOR)):
        sub = df[df.cell_class == cls]
        for responsive, marker in ((False,"o"),(True,"o")):
            ss = sub[sub.stim_responsive_fdr == responsive]
            if len(ss):
                ax.scatter(ss.index, ss.stim_response_mean, s=22 if responsive else 12,
                           facecolors=color if responsive else "none", edgecolors=color,
                           alpha=0.85, linewidths=0.7, marker=marker)
        exc = sub[sub.stim_excited_fdr]
        sup = sub[sub.stim_suppressed_fdr]
        if len(exc): ax.scatter(exc.index, exc.stim_response_mean, marker="^", s=42, color=color)
        if len(sup): ax.scatter(sup.index, sup.stim_response_mean, marker="v", s=42, color=color)
    ax.axhline(0, color="black", ls=":", lw=1)
    ax.set_xlabel("Cell index in combined/session table")
    ax.set_ylabel("Mean stimulus response (baseline-subtracted dF/F)")
    ax.set_title("Reliable stimulus responses\nopen=not FDR responsive; filled/triangle=FDR responsive")
    apply_robust_y_limits(ax, df.stim_response_mean, reference_values=(0,))

    ax = axes[1]
    cats = ["Responsive", "Excited", "Suppressed"]
    x = np.arange(3); width=.36
    vals = {}
    for cls in ("green","yellow"):
        sub = df[df.cell_class==cls]; n=len(sub)
        vals[cls] = [100*safe_divide(int(sub.stim_responsive_fdr.sum()),n),
                     100*safe_divide(int(sub.stim_excited_fdr.sum()),n),
                     100*safe_divide(int(sub.stim_suppressed_fdr.sum()),n)]
    ax.bar(x-width/2, vals["green"], width, color=GREEN_COLOR, label=f"Green n={sum(df.cell_class=='green')}")
    ax.bar(x+width/2, vals["yellow"], width, color=YELLOW_COLOR, label=f"Yellow n={sum(df.cell_class=='yellow')}")
    ax.set_xticks(x, cats); ax.set_ylabel("Cells (%)"); ax.set_ylim(0, max(5, 1.18*np.nanmax(vals["green"]+vals["yellow"])))
    ax.legend(frameon=False); ax.set_title("FDR response classifications")
    fig.suptitle(title)
    fig.savefig(output_path, dpi=300, bbox_inches="tight"); plt.close(fig)


def _response_columns(cell_df: pd.DataFrame, tuning_mode: str) -> tuple[list[str], np.ndarray]:
    prefix = "response_freq_" if tuning_mode == "tuningFreq" else "response_AM_"
    cols=[]; vals=[]
    for c in cell_df.columns:
        if c.startswith(prefix) and c.endswith("_Hz"):
            try:
                v=float(c[len(prefix):-3])
            except ValueError:
                continue
            cols.append(c); vals.append(v)
    order=np.argsort(vals)
    return [cols[i] for i in order], np.asarray([vals[i] for i in order], dtype=float)


def _xplot(values: np.ndarray, mode: str) -> np.ndarray:
    return values/1000.0 if mode=="tuningFreq" else values


def _xlabel(mode: str) -> str:
    return "Tone frequency (kHz)" if mode=="tuningFreq" else "AM rate (Hz)"


def tuning_curve_figures(cell_df: pd.DataFrame, mode: str, possible_values: np.ndarray,
                         outdir: Path, title: str, prefix: str="") -> None:
    cols, values = _response_columns(cell_df, mode)
    if not cols: return
    x = _xplot(values, mode)
    for responsive_only, tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df = cell_df[cell_df.stim_responsive_fdr] if responsive_only else cell_df
        if len(df)==0: continue
        # Individuals + means.
        fig, ax = plt.subplots(figsize=(9,6), constrained_layout=True)
        allvals=[]
        for cls,color in (("green",GREEN_COLOR),("yellow",YELLOW_COLOR)):
            sub=df[df.cell_class==cls]; mat=sub[cols].to_numpy(float)
            for row in mat:
                ax.plot(x,row,color=color,alpha=.07,lw=.7)
            means=np.nanmean(mat,axis=0) if len(mat) else np.full(len(cols),np.nan)
            sems=np.asarray([mean_sem(mat[:,i])[1] if len(mat) else np.nan for i in range(len(cols))])
            ax.errorbar(x,means,yerr=sems,fmt="o-",capsize=3,lw=2,color=color,label=f"{cls.title()} n={len(sub)}")
            allvals.extend(mat[np.isfinite(mat)].tolist())
        ax.axhline(0,color="black",ls=":",lw=1); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Response (baseline-subtracted dF/F)")
        if mode=="tuningFreq": ax.set_xscale("log")
        ax.legend(frameon=False); ax.grid(alpha=.2); ax.set_title(f"{title}\n{tag.replace('_',' ')}")
        apply_robust_y_limits(ax, allvals, reference_values=(0,))
        fig.savefig(outdir/f"{prefix}tuning_curves_{tag}.png",dpi=300,bbox_inches="tight"); plt.close(fig)
        # Mean SEM only.
        fig,ax=plt.subplots(figsize=(9,6),constrained_layout=True); mcat=[]; ecat=[]
        for cls,color,offset in (("green",GREEN_COLOR,8),("yellow",YELLOW_COLOR,-11)):
            sub=df[df.cell_class==cls]; mat=sub[cols].to_numpy(float)
            means=np.asarray([mean_sem(mat[:,i])[0] if len(mat) else np.nan for i in range(len(cols))])
            sems=np.asarray([mean_sem(mat[:,i])[1] if len(mat) else np.nan for i in range(len(cols))])
            ax.errorbar(x,means,yerr=sems,fmt="o-",capsize=4,lw=2,color=color,label=f"{cls.title()} n={len(sub)}")
            if len(values)<=18:
                for xx,mm,ss in zip(x,means,sems):
                    if np.isfinite(mm): ax.annotate(f"{mm:.3f}±{ss:.3f}" if np.isfinite(ss) else f"{mm:.3f}",(xx,mm),xytext=(0,offset),textcoords="offset points",ha="center",fontsize=6,color=color,rotation=40)
            mcat.extend(means); ecat.extend(sems)
        ax.axhline(0,color="black",ls=":",lw=1); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Mean response (dF/F)")
        if mode=="tuningFreq": ax.set_xscale("log")
        ax.legend(frameon=False); ax.grid(alpha=.2); ax.set_title(f"{title}\n{tag.replace('_',' ')} — mean ± SEM only")
        optimized_summary_ylim(ax,mcat,ecat,reference_values=(0,))
        fig.savefig(outdir/f"{prefix}tuning_curves_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def tuning_raster_figures(cell_df: pd.DataFrame, mode: str, possible_values: np.ndarray,
                          outdir: Path, title: str, prefix: str="") -> None:
    cols, values = _response_columns(cell_df, mode)
    if not cols: return
    for fdr,tag in ((False,"amplitude_responsive"),(True,"FDR_responsive_only")):
        base=cell_df[cell_df.amplitude_responsive_0p02]
        if fdr: base=base[base.stim_responsive_fdr]
        fig,axes=plt.subplots(1,2,figsize=(13,7),constrained_layout=True)
        for ax,(cls,cmap) in zip(axes,(("green","Greens"),("yellow","YlOrBr"))):
            sub=base[base.cell_class==cls]; mat=sub[cols].to_numpy(float)
            if len(mat)==0:
                ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center"); ax.set_title(cls.title()); continue
            norm=np.nanmax(np.abs(mat),axis=1); norm[norm<=0]=np.nan
            matn=mat/norm[:,None]
            pref=np.nanargmax(np.where(np.isfinite(matn),matn,-np.inf),axis=1)
            order=np.argsort(pref); im=ax.imshow(matn[order],aspect="auto",interpolation="nearest",cmap="coolwarm",vmin=-1,vmax=1)
            ax.set_title(f"{cls.title()} n={len(sub)}"); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Cells sorted by preferred value")
            ticks=np.arange(len(values)); labels=[f"{v/1000:g}" if mode=="tuningFreq" else f"{v:g}" for v in values]
            ax.set_xticks(ticks,labels,rotation=45,ha="right"); fig.colorbar(im,ax=ax,label="Normalized response")
        fig.suptitle(f"{title}\nSelectivity rasters — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}selectivity_rasters_{tag}.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def green_yellow_metric_figures(cell_df: pd.DataFrame, outdir: Path, title: str, prefix: str="") -> None:
    metrics=[
        ("best_tuning_response","Best tuning response"),("peak_absolute_response","Peak absolute response"),
        ("tuning_modulation_depth","Tuning modulation depth"),("tuning_selectivity_contrast","Tuning selectivity contrast"),
        ("tuning_selectivity_index","Tuning selectivity index"),
    ]
    for fdr,tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df=cell_df[cell_df.stim_responsive_fdr] if fdr else cell_df
        fig,axes=plt.subplots(2,3,figsize=(15,9),constrained_layout=True); axes=axes.ravel()
        rng=np.random.default_rng(20260813)
        for ax,(metric,label) in zip(axes,metrics):
            allvals=[]
            for xpos,(cls,color) in enumerate((("green",GREEN_COLOR),("yellow",YELLOW_COLOR))):
                vals=finite_values(df.loc[df.cell_class==cls,metric]); allvals.extend(vals.tolist())
                if len(vals):
                    xj=xpos+rng.uniform(-.09,.09,size=len(vals)); ax.scatter(xj,vals,s=14,alpha=.28,color=color)
                    m,se,n=mean_sem(vals); ax.errorbar(xpos,m,yerr=se,fmt="o",capsize=5,color="black",mfc=color,ms=7)
            g=finite_values(df.loc[df.cell_class=="green",metric]); y=finite_values(df.loc[df.cell_class=="yellow",metric])
            p=safe_mannwhitney(g,y)["p"]
            ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(f"{label}\npooled MW p={p:.3g}" if p is not None else label)
            apply_robust_y_limits(ax,allvals,reference_values=(0,) if metric!="tuning_selectivity_index" else ())
        axes[-1].axis("off"); fig.suptitle(f"{title}\nGREEN vs YELLOW — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}green_yellow_tuning_summary_{tag}.png",dpi=300,bbox_inches="tight"); plt.close(fig)

        fig,axes=plt.subplots(2,3,figsize=(15,9),constrained_layout=True); axes=axes.ravel()
        for ax,(metric,label) in zip(axes,metrics):
            means=[]; sems=[]
            for xpos,(cls,color) in enumerate((("green",GREEN_COLOR),("yellow",YELLOW_COLOR))):
                vals=df.loc[df.cell_class==cls,metric]; m,se,n=mean_sem(vals); means.append(m); sems.append(se)
                ax.errorbar(xpos,m,yerr=se,fmt="o",capsize=5,color=color,ms=8)
                if np.isfinite(m): ax.annotate(f"{m:.4f} ± {se:.4f}\nn={n}" if np.isfinite(se) else f"{m:.4f}\nn={n}",(xpos,m),xytext=(0,12 if xpos==0 else -30),textcoords="offset points",ha="center",fontsize=8,color=color)
            ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(label); optimized_summary_ylim(ax,means,sems,reference_values=(0,) if metric!="tuning_selectivity_index" else ())
        axes[-1].axis("off"); fig.suptitle(f"{title}\nGREEN vs YELLOW — {tag.replace('_',' ')} — mean ± SEM only")
        fig.savefig(outdir/f"{prefix}green_yellow_tuning_summary_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def condition_profile_figures(condition_df: pd.DataFrame, mode: str, outdir: Path, title: str, prefix: str="") -> None:
    for fdr,tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df=condition_df[condition_df.stim_responsive_fdr] if fdr else condition_df
        if len(df)==0: continue
        values=np.sort(df.tuning_value_Hz.unique()); intensities=np.sort(df.intensity_dB.unique())
        x=_xplot(values,mode)
        fig,axes=plt.subplots(1,max(1,len(intensities)),figsize=(6*max(1,len(intensities)),5),squeeze=False,constrained_layout=True)
        for ax,intensity in zip(axes.ravel(),intensities):
            means_all=[]; sems_all=[]
            for cls,color,offset in (("green",GREEN_COLOR,8),("yellow",YELLOW_COLOR,-10)):
                means=[]; sems=[]
                for value in values:
                    vals=df[(df.cell_class==cls)&np.isclose(df.intensity_dB,intensity)&np.isclose(df.tuning_value_Hz,value)].condition_response
                    m,se,n=mean_sem(vals); means.append(m); sems.append(se)
                ax.errorbar(x,means,yerr=sems,fmt="o-",capsize=3,color=color,label=cls.title())
                means_all.extend(means); sems_all.extend(sems)
            ax.axhline(0,color="black",ls=":",lw=1); ax.set_title(f"{intensity:g} dB SPL"); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Mean response (dF/F)")
            if mode=="tuningFreq": ax.set_xscale("log")
            ax.legend(frameon=False); ax.grid(alpha=.2); optimized_summary_ylim(ax,means_all,sems_all,reference_values=(0,))
        fig.suptitle(f"{title}\nIntensity-resolved tuning — {tag.replace('_',' ')} — mean ± SEM")
        fig.savefig(outdir/f"{prefix}intensity_resolved_tuning_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)

        # Condition selectivity contrast summary.
        ordered=(df[["condition_name","tuning_value_Hz","intensity_dB"]].drop_duplicates().sort_values(["intensity_dB","tuning_value_Hz"]))
        names=ordered.condition_name.tolist(); xpos=np.arange(len(names))
        fig,axes=plt.subplots(2,1,figsize=(max(12,.75*len(names)),9),constrained_layout=True)
        means_by={}; sems_by={}
        for cls,color,shift in (("green",GREEN_COLOR,-.08),("yellow",YELLOW_COLOR,.08)):
            means=[]; sems=[]
            for name in names:
                vals=df[(df.cell_class==cls)&(df.condition_name==name)].condition_selectivity_contrast
                m,se,n=mean_sem(vals); means.append(m); sems.append(se)
            means_by[cls]=np.asarray(means); sems_by[cls]=np.asarray(sems)
            axes[0].errorbar(xpos+shift,means,yerr=sems,fmt="o",capsize=3,color=color,label=cls.title())
        axes[0].axhline(0,color="black",ls=":",lw=1); axes[0].set_xticks(xpos,names,rotation=45,ha="right"); axes[0].set_ylabel("Condition selectivity contrast (dF/F)"); axes[0].legend(frameon=False)
        optimized_summary_ylim(axes[0],np.r_[means_by["green"],means_by["yellow"]],np.r_[sems_by["green"],sems_by["yellow"]],reference_values=(0,))
        diff=means_by["yellow"]-means_by["green"]; axes[1].plot(xpos,diff,"o-",color="black"); axes[1].axhline(0,color="black",ls="--",lw=1)
        axes[1].set_xticks(xpos,names,rotation=45,ha="right"); axes[1].set_ylabel("Yellow - green mean contrast"); optimized_summary_ylim(axes[1],diff,np.zeros_like(diff),reference_values=(0,))
        fig.suptitle(f"{title}\nCondition selectivity (condition - all others) — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}condition_selectivity_contrast_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


# =============================================================================
# COMBINED AREA-LEVEL STATISTICS / FIGURES
# =============================================================================

def combined_statistics(cell_df: pd.DataFrame, class_summary_df: pd.DataFrame) -> dict[str, Any]:
    metrics=["stim_response_mean","best_tuning_response","peak_absolute_response","tuning_modulation_depth","tuning_selectivity_contrast","tuning_selectivity_index"]
    out: dict[str, Any] = {"pooled_cell_exploratory":{}, "paired_session_primary":{}}
    for metric in metrics:
        out["pooled_cell_exploratory"][metric]=safe_mannwhitney(
            cell_df.loc[cell_df.cell_class=="green",metric], cell_df.loc[cell_df.cell_class=="yellow",metric]
        )
        col=f"median_{metric}"
        wide=class_summary_df.pivot_table(index="session_key",columns="cell_class",values=col,aggfunc="first")
        if "green" in wide and "yellow" in wide:
            out["paired_session_primary"][metric]=safe_paired_wilcoxon(wide["green"],wide["yellow"])
        else:
            out["paired_session_primary"][metric]={"n_pairs":0,"W":None,"p":None}
    for metric in ("pct_stim_responsive_fdr","pct_stim_excited_fdr","pct_stim_suppressed_fdr"):
        wide=class_summary_df.pivot_table(index="session_key",columns="cell_class",values=metric,aggfunc="first")
        if "green" in wide and "yellow" in wide:
            out["paired_session_primary"][metric]=safe_paired_wilcoxon(wide["green"],wide["yellow"])
    return out


def session_level_figures(class_summary_df: pd.DataFrame, output_dir: Path, title: str) -> None:
    metrics=[
        ("median_best_tuning_response","Median best tuning response"),
        ("median_peak_absolute_response","Median peak absolute response"),
        ("median_tuning_modulation_depth","Median tuning modulation depth"),
        ("median_tuning_selectivity_contrast","Median selectivity contrast"),
        ("median_tuning_selectivity_index","Median selectivity index"),
        ("pct_stim_responsive_fdr","FDR responsive cells (%)"),
    ]
    fig,axes=plt.subplots(2,3,figsize=(15,9),constrained_layout=True); axes=axes.ravel()
    for ax,(metric,label) in zip(axes,metrics):
        wide=class_summary_df.pivot_table(index="session_key",columns="cell_class",values=metric,aggfunc="first")
        if "green" not in wide or "yellow" not in wide:
            ax.text(.5,.5,"Insufficient paired sessions",transform=ax.transAxes,ha="center"); continue
        valid=wide[["green","yellow"]].dropna()
        for _,r in valid.iterrows(): ax.plot([0,1],[r.green,r.yellow],color="0.7",lw=1,zorder=1)
        ax.scatter(np.zeros(len(valid)),valid.green,color=GREEN_COLOR,zorder=2); ax.scatter(np.ones(len(valid)),valid.yellow,color=YELLOW_COLOR,zorder=2)
        res=safe_paired_wilcoxon(valid.green,valid.yellow)
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(f"{label}\npaired Wilcoxon p={res['p']:.3g}" if res['p'] is not None else label)
        apply_robust_y_limits(ax,np.r_[valid.green,valid.yellow],reference_values=(0,) if "response" in metric or "contrast" in metric else ())
    fig.suptitle(f"{title}\nSession-level GREEN/YELLOW comparisons")
    fig.savefig(output_dir/"combined_session_level_green_yellow_comparisons.png",dpi=300,bbox_inches="tight"); plt.close(fig)

    fig,axes=plt.subplots(2,3,figsize=(15,9),constrained_layout=True); axes=axes.ravel()
    for ax,(metric,label) in zip(axes,metrics):
        means=[]; sems=[]
        for xpos,(cls,color) in enumerate((("green",GREEN_COLOR),("yellow",YELLOW_COLOR))):
            vals=class_summary_df.loc[class_summary_df.cell_class==cls,metric]; m,se,n=mean_sem(vals); means.append(m); sems.append(se)
            ax.errorbar(xpos,m,yerr=se,fmt="o",capsize=5,color=color,ms=8)
            if np.isfinite(m): ax.annotate(f"{m:.4f} ± {se:.4f}\nn sessions={n}" if np.isfinite(se) else f"{m:.4f}\nn={n}",(xpos,m),xytext=(0,12 if xpos==0 else -30),textcoords="offset points",ha="center",fontsize=8,color=color)
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(label); optimized_summary_ylim(ax,means,sems,reference_values=(0,) if "response" in metric or "contrast" in metric else ())
    fig.suptitle(f"{title}\nSession summaries — mean ± SEM only")
    fig.savefig(output_dir/"combined_session_level_green_yellow_comparisons_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def write_combined_report(path: Path, mode: str, cell_df: pd.DataFrame, class_summary_df: pd.DataFrame, stats_dict: dict[str, Any]) -> None:
    lines=[]
    lines.append(f"AM_TUNING AREA ANALYSIS — {mode}\n")
    lines.append(f"Cells: {len(cell_df)} | sessions: {cell_df.session_key.nunique()}\n")
    lines.append(f"Green cells: {sum(cell_df.cell_class=='green')} | Yellow cells: {sum(cell_df.cell_class=='yellow')}\n")
    lines.append("\nPRIMARY: PAIRED SESSION-LEVEL GREEN VS YELLOW\n")
    lines.append("Each session contributes one GREEN and one YELLOW summary when both are available.\n")
    for metric,res in stats_dict.get("paired_session_primary",{}).items():
        lines.append(f"  {metric}: n_pairs={res.get('n_pairs')} W={res.get('W')} p={res.get('p')}\n")
    lines.append("\nEXPLORATORY: POOLED CELLS\n")
    lines.append("These tests pool cells across sessions and therefore do not treat session/animal structure as the primary replicate.\n")
    for metric,res in stats_dict.get("pooled_cell_exploratory",{}).items():
        lines.append(f"  {metric}: n_green={res.get('n_a')} n_yellow={res.get('n_b')} U={res.get('U')} p={res.get('p')}\n")
    path.write_text("".join(lines))


def combine_mode_results(results: list[dict[str, Any]], mode_dir: Path, subject: str, area: str, dates: list[str], mode: str) -> None:
    if not results:
        return
    combined_dir=mode_dir/"combined"; combined_dir.mkdir(parents=True,exist_ok=True)
    cell_df=pd.concat([r["cell_df"] for r in results],ignore_index=True,sort=False)
    cond_df=pd.concat([r["condition_df"] for r in results],ignore_index=True,sort=False)
    class_df=pd.concat([r["class_summary_df"] for r in results],ignore_index=True,sort=False)
    cell_df.to_csv(combined_dir/"combined_cell_results.csv",index=False)
    cond_df.to_csv(combined_dir/"combined_condition_results.csv",index=False)
    class_df.to_csv(combined_dir/"combined_session_class_summary.csv",index=False)
    title=f"{subject} | {area} | {mode} | {', '.join(dates)} | {cell_df.session_key.nunique()} sessions"
    sound_responsiveness_figure(cell_df,combined_dir/"combined_stim_responsive_cells_green_yellow.png",title)
    cols,values=_response_columns(cell_df,mode)
    tuning_curve_figures(cell_df,mode,values,combined_dir,title,prefix="combined_")
    tuning_raster_figures(cell_df,mode,values,combined_dir,title,prefix="combined_")
    green_yellow_metric_figures(cell_df,combined_dir,title,prefix="combined_")
    condition_profile_figures(cond_df,mode,combined_dir,title,prefix="combined_")
    session_level_figures(class_df,combined_dir,title)
    stats_dict=combined_statistics(cell_df,class_df)
    save_json(combined_dir/"combined_statistics.json",stats_dict)
    write_combined_report(combined_dir/"combined_report.txt",mode,cell_df,class_df,stats_dict)
    figure_names=sorted(p.name for p in combined_dir.glob("*.png"))
    (combined_dir/"FIGURE_INDEX.txt").write_text("\n".join(figure_names)+"\n")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args=parse_args()
    info_file,sessions=load_info2p_sessions(args.subject)
    selected=select_sessions(sessions,args.dates,args.area,args.mode)
    date_tag="_".join(args.dates)
    root=Path(settings.TEMP_OUTPUT_PATH)/"evan"/"am_tuning_area_analysis"/args.subject/args.area/date_tag
    root.mkdir(parents=True,exist_ok=True)
    selection_df=selection_dataframe(selected)
    selection_df.to_csv(root/"session_selection.csv",index=False)

    print("="*78)
    print("AM_TUNING AREA ANALYSIS")
    print("="*78)
    print(f"Subject:        {args.subject}")
    print(f"Requested area: {args.area}")
    print(f"Dates:          {', '.join(args.dates)}")
    print(f"Mode:           {args.mode} (tuningFreq and tuningAM are always combined separately)")
    print(f"Paradigm:       {PARADIGM_PRIMARY}")
    print(f"Info2p:         {info_file}")
    print(f"Data root:      {settings.TWOPHOTON_PATH}")
    print(f"Behavior root:  {settings.BEHAVIOR_PATH}")
    print(f"Output root:    {root}")
    print(f"Sessions:       {len(selected)}")
    print("\nSelected sessions:")
    for s in selected:
        print(f"  {s.get('date')}  {s.get('session')}  brainArea={s.get('brainArea')}  depth={s.get('depth')}  label={s.get('sessionLabel')}  mode={s.get('info2p_tuningMode')}")
    if args.dry_run:
        print("\nDry run complete; no imaging data were loaded.")
        return
    if not selected:
        raise RuntimeError("No matching am_tuning sessions found.")

    by_mode: dict[str,list[dict[str,Any]]] = {"tuningFreq":[],"tuningAM":[]}
    failures=[]
    for meta in selected:
        hinted=meta.get("info2p_tuningMode") or "unknown"
        provisional_mode_dir=root/(hinted if hinted in by_mode else "unclassified")
        session_dir=provisional_mode_dir/"session_outputs"/f"{meta['date']}_{meta['session']}"
        try:
            result=analyze_session(meta,args.plane,args.n_permutations,args.seed,session_dir)
            actual=result["tuning_mode"]
            if args.mode != "both" and actual != args.mode:
                print(f"Skipping {meta['date']} {meta['session']} after behavior detection: actual mode {actual} != requested {args.mode}")
                continue
            # If info2p hint was absent/wrong directory, move is not attempted; actual mode still drives combined output.
            by_mode[actual].append(result)
        except Exception as exc:
            session_dir.mkdir(parents=True,exist_ok=True)
            err={"date":str(meta.get("date")),"session":str(meta.get("session")),"brainArea":meta.get("brainArea"),
                 "sessionLabel":meta.get("sessionLabel"),"error_type":type(exc).__name__,"error":str(exc),"traceback":traceback.format_exc()}
            save_json(session_dir/"ERROR.json",err); failures.append(err)
            print(f"ERROR {meta.get('date')} {meta.get('session')}: {type(exc).__name__}: {exc}")

    modes_to_combine=[args.mode] if args.mode in {"tuningFreq","tuningAM"} else ["tuningFreq","tuningAM"]
    for mode in modes_to_combine:
        if by_mode[mode]:
            mode_dir=root/mode; mode_dir.mkdir(parents=True,exist_ok=True)
            combine_mode_results(by_mode[mode],mode_dir,args.subject,args.area,args.dates,mode)

    manifest={
        "subject":args.subject,"area":args.area,"dates":args.dates,"requested_mode":args.mode,
        "info2p_file":info_file,"output_root":root,"n_selected":len(selected),
        "n_success_tuningFreq":len(by_mode["tuningFreq"]),"n_success_tuningAM":len(by_mode["tuningAM"]),
        "n_failed":len(failures),"failures":failures,
        "parameters":{
            "cell_prob_threshold":CELL_PROB_THRESHOLD,"iou_threshold":IOU_THRESHOLD,
            "cellpose_cellprob_threshold":CELLPOSE_CELLPROB_THRESHOLD,"cellpose_flow_threshold":CELLPOSE_FLOW_THRESHOLD,
            "raster_min_abs_response":RASTER_MIN_ABS_RESPONSE,"fdr_alpha":FDR_ALPHA,
            "n_permutations":args.n_permutations,"seed":args.seed,
        },
    }
    save_json(root/"run_manifest.json",manifest)
    print("\n"+"="*78)
    print("ANALYSIS COMPLETE")
    print("="*78)
    print(f"tuningFreq successful sessions: {len(by_mode['tuningFreq'])}")
    print(f"tuningAM successful sessions:   {len(by_mode['tuningAM'])}")
    print(f"Failed sessions:                {len(failures)}")
    print(f"Outputs: {root}")


if __name__ == "__main__":
    main()
