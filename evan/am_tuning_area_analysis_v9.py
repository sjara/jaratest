#!/usr/bin/env python3
"""
Batch/area-level analysis of two-photon am_tuning sessions (v9; condition-specific FDR + alternate dF/F + trial archives).

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
The acquisition-order rule from the finalized notebook is used, with robust
recovery for occasional missed/extra triggers:
* zero-offset alignment (first imaging sound event -> first behavioral trial)
  is always tried first;
* only if zero-offset fails immediately, a conservative fallback may ignore up
  to 3 leading imaging events OR behavioral trials; the shifted start must pass
  several consecutive early timing intervals before it is accepted;
* trailing extra imaging events are ignored;
* trailing behavioral trials that continued after imaging stopped are ignored;
* isolated internal missed/extra triggers can be skipped monotonically when
  doing so restores the expected stimDur + isi timing;
* all downstream behavior arrays are subset with the SAME matched indices as
  the event-locked imaging data;
* strict post-alignment timing QC is retained. Sessions that cannot be aligned
  cleanly are skipped with ERROR.json rather than guessed.

Figures
-------
The expanded figure philosophy from the finalized sound_tuning v13 workflow is
used here as well:
* reliable stimulus-responsive/non-responsive GREEN/YELLOW figure;
* all-cell and FDR-responsive-only tuning curves;
* clean mean +/- SEM-only companions with optimized y axes and numeric values;
* amplitude-threshold and FDR-responsive selectivity rasters;
* GREEN/YELLOW summary metrics;
* intensity-resolved tuning profiles;
* condition-selectivity contrast (condition minus all other conditions),
  replacing the old d-prime analysis;
* session-level GREEN/YELLOW comparisons;
* primary lifetime-sparseness tuning selectivity plus separate Gini, Fano, and FWHM figures;
* per-session top-10 selective and top-10 FDR-responsive GREEN/YELLOW examples;
* combined session-mean profiles with top-5 high-sparseness cells per session;
* combined top-50 lifetime-sparseness rasters;
* condition-specific FDR responsiveness at each frequency/AM rate, with
  stim_responsive_fdr defined as the union across tuning values;
* two alternate dF/F sensitivity definitions (whole-session median F0 and
  60-s local prestimulus-only median F0), exported without redefining the
  primary responsiveness labels;
* compact per-session trial-response NPZ archives for downstream Monte-Carlo
  trial-repetition subsampling analyses.

Statistics
----------
Pooled-cell tests are retained as exploratory/descriptive.  Primary combined
GREEN/YELLOW inference is additionally reported at the session level, using
paired GREEN and YELLOW summaries from the same imaging sessions.

Tuning-axis geometry
--------------------
Every graph whose x-axis is frequency or AM rate uses explicit base-2
coordinates x=log2(value). Therefore every doubling occupies the same physical
distance (for example 2, 4, 8, 16, 32 kHz are equally spaced). Tick labels
remain in kHz for tuningFreq and Hz for tuningAM.

Example
-------
python am_tuning_area_analysis_v9.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730

Only frequency tuning:
python am_tuning_area_analysis_v9.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730 \
    --mode tuningFreq

Dry run:
python am_tuning_area_analysis_v9.py imag039 \
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
N_EXAMPLE_CELLS_PER_CLASS = 10
N_COMBINED_RASTER_CELLS_PER_CLASS = 50
N_TOP_PROFILE_CELLS_PER_SESSION_CLASS = 5
FDR_ALPHA = 0.05
N_PERMUTATIONS_DEFAULT = 20000
RANDOM_SEED_DEFAULT = 20260813

# Alignment QC / recovery settings.
# Normal consecutive event intervals must agree within MAX_ABS_ERROR_S.
# If they do not, the aligner may skip a small number of INTERNAL imaging or
# behavioral events to recover a monotonic match. Large trailing mismatches are
# allowed only when the retained matched sequence still covers most of both
# streams.
MAX_INTERNAL_SKIP_PER_STEP = 3
MAX_TOTAL_INTERNAL_SKIPS = 8
MAX_LEADING_SKIP = 3
LEADING_VALIDATION_INTERVALS = 4
ALIGN_SKIP_PENALTY_S = 0.25
MIN_ALIGNMENT_COVERAGE = 0.80
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


def mean_sd_sem(values: Any) -> tuple[float, float, float, int]:
    vals = finite_values(values)
    n = len(vals)
    if n == 0:
        return np.nan, np.nan, np.nan, 0
    mean = float(np.mean(vals))
    sd = float(np.std(vals, ddof=1)) if n > 1 else np.nan
    sem = float(sd / np.sqrt(n)) if n > 1 else np.nan
    return mean, sd, sem, n


def lifetime_sparseness_nonnegative(values: Any) -> float:
    """Treves-Rolls lifetime sparseness on a nonnegative response-magnitude profile."""
    r = finite_values(values)
    if len(r) < 2:
        return np.nan
    r = np.maximum(r, 0.0)
    mean_sq = float(np.mean(r)) ** 2
    mean_of_sq = float(np.mean(r ** 2))
    if not np.isfinite(mean_of_sq) or mean_of_sq <= 1e-15:
        return np.nan
    n = len(r)
    return float((1.0 - mean_sq / mean_of_sq) / (1.0 - 1.0 / n))


def gini_coefficient_nonnegative(values: Any) -> float:
    """Gini coefficient of a nonnegative tuning-profile magnitude vector."""
    x = finite_values(values)
    if len(x) < 2:
        return np.nan
    x = np.maximum(x, 0.0)
    total = float(np.sum(x))
    if total <= 1e-15:
        return np.nan
    x = np.sort(x)
    n = len(x)
    ranks = np.arange(1, n + 1, dtype=float)
    return float((2.0 * np.sum(ranks * x) / (n * total)) - (n + 1.0) / n)


def fano_factor_nonnegative(values: Any) -> float:
    """Variance/mean across nonnegative tuning-profile magnitudes (scale-dependent)."""
    x = finite_values(values)
    if len(x) < 2:
        return np.nan
    x = np.maximum(x, 0.0)
    mean = float(np.mean(x))
    if mean <= 1e-15:
        return np.nan
    return float(np.var(x, ddof=1) / mean)


def tuning_fwhm(values: Any, tuning_values_hz: Any, mode: str) -> float:
    """FWHM of |response| around its largest peak. Frequency width is in octaves; AM width in Hz.

    A width is returned only when the half-maximum crossing is bracketed on both
    sides by sampled tuning values. Boundary-peaked or otherwise unbracketed
    curves return NaN rather than a censored/invented bandwidth.
    """
    y = np.asarray(values, dtype=float).ravel()
    x_hz = np.asarray(tuning_values_hz, dtype=float).ravel()
    valid = np.isfinite(y) & np.isfinite(x_hz) & (x_hz > 0)
    if np.sum(valid) < 3:
        return np.nan
    y = np.abs(y[valid])
    x_hz = x_hz[valid]
    order = np.argsort(x_hz)
    y = y[order]; x_hz = x_hz[order]
    if not np.any(np.isfinite(y)):
        return np.nan
    peak_i = int(np.nanargmax(y))
    peak = float(y[peak_i])
    if not np.isfinite(peak) or peak <= 1e-15 or peak_i == 0 or peak_i == len(y)-1:
        return np.nan
    half = 0.5 * peak
    x = np.log2(x_hz) if mode == "tuningFreq" else x_hz.astype(float)

    left = np.nan
    for i in range(peak_i - 1, -1, -1):
        if y[i] <= half <= y[i+1] or y[i] >= half >= y[i+1]:
            y0, y1 = float(y[i]), float(y[i+1])
            if y1 == y0:
                left = float(x[i])
            else:
                left = float(x[i] + (half - y0) * (x[i+1] - x[i]) / (y1 - y0))
            break
    right = np.nan
    for i in range(peak_i, len(y)-1):
        if y[i] >= half >= y[i+1] or y[i] <= half <= y[i+1]:
            y0, y1 = float(y[i]), float(y[i+1])
            if y1 == y0:
                right = float(x[i+1])
            else:
                right = float(x[i] + (half - y0) * (x[i+1] - x[i]) / (y1 - y0))
            break
    if not (np.isfinite(left) and np.isfinite(right) and right >= left):
        return np.nan
    return float(right - left)


def selectivity_metric_label(metric: str, mode: str) -> str:
    if metric == "tuning_lifetime_sparseness":
        return "Lifetime sparseness"
    if metric == "tuning_gini_coefficient":
        return "Gini coefficient"
    if metric == "tuning_fano_factor":
        return "Fano factor across |response| profile"
    if metric == "tuning_fwhm":
        return "FWHM (octaves)" if mode == "tuningFreq" else "FWHM (Hz)"
    return metric


def selectivity_equation_footer(mode: str) -> str:
    fwhm_unit = "octaves (log2 frequency)" if mode == "tuningFreq" else "Hz"
    return (
        r"Lifetime sparseness = [1 - (mean(r))$^2$/mean(r$^2$)]/[1 - 1/N];  "
        r"Gini = inequality of r;  Fano = var(r)/mean(r);  "
        f"FWHM = width of |response| at 1/2 max ({fwhm_unit});  r = |mean baseline-corrected dF/F|"
    )


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


def _save_eventlocked_average_figure(eventlocked_data, valid_events, tvec, output_path, title, cbar_label="dF/F"):
    """QC figure for one dF/F definition, using the same aligned valid trials."""
    valid_events = np.asarray(valid_events, dtype=bool)
    if not np.any(valid_events):
        return
    trialavg = np.nanmean(np.asarray(eventlocked_data, dtype=float)[:, valid_events, :], axis=1)
    fig = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs = fig.add_gridspec(4, 1)
    ax0 = fig.add_subplot(gs[:3, 0])
    im = ax0.imshow(
        trialavg, interpolation="nearest",
        extent=[tvec[0], tvec[-1], trialavg.shape[0], 0],
        aspect="auto", cmap="viridis",
    )
    fig.colorbar(im, ax=ax0, label=cbar_label)
    ax0.axvline(0, color="darkred")
    ax0.set_title(title)
    ax0.set_ylabel("Cell")
    ax0.tick_params(labelbottom=False)
    ax1 = fig.add_subplot(gs[3, 0], sharex=ax0)
    ax1.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    ax1.axvline(0, color="darkred")
    ax1.set_xlabel("Time from stimulus onset (s)")
    ax1.set_ylabel(f"Mean {cbar_label}")
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _session_median_dff(eventlocked_raw: np.ndarray, full_session_raw: np.ndarray) -> np.ndarray:
    """dF/F with one whole-session median F0 per cell."""
    eventlocked_raw = np.asarray(eventlocked_raw, dtype=float)
    full_session_raw = np.asarray(full_session_raw, dtype=float)
    f0 = np.nanmedian(full_session_raw, axis=1)
    good = np.isfinite(f0) & (np.abs(f0) > 1e-12)
    out = np.full_like(eventlocked_raw, np.nan, dtype=float)
    out[good] = (
        eventlocked_raw[good] - f0[good, None, None]
    ) / f0[good, None, None]
    return out


def _local_prestim_median_dff(
    eventlocked_raw: np.ndarray,
    event_onset_samples: np.ndarray,
    srate: float,
    valid_events: np.ndarray,
    tvec: np.ndarray,
    local_window_s: float = 60.0,
    prestim_window_s: tuple[float, float] = (-0.300, 0.0),
) -> np.ndarray:
    """dF/F using prestimulus samples from stimuli within +/- local_window/2."""
    raw = np.asarray(eventlocked_raw, dtype=float)
    onset_s = np.asarray(event_onset_samples, dtype=float) / float(srate)
    valid_events = np.asarray(valid_events, dtype=bool)
    pre = (np.asarray(tvec) >= prestim_window_s[0]) & (np.asarray(tvec) < prestim_window_s[1])
    out = np.full_like(raw, np.nan, dtype=float)
    if not np.any(pre):
        return out
    half_window = float(local_window_s) / 2.0
    for ei in range(raw.shape[1]):
        neighbors = (
            valid_events
            & np.isfinite(onset_s)
            & (np.abs(onset_s - onset_s[ei]) <= half_window)
        )
        if not np.any(neighbors):
            continue
        baseline_samples = raw[:, neighbors, :][:, :, pre]
        f0 = np.nanmedian(baseline_samples, axis=(1, 2))
        good = np.isfinite(f0) & (np.abs(f0) > 1e-12)
        out[good, ei, :] = (raw[good, ei, :] - f0[good, None]) / f0[good, None]
    return out


def _trial_response_from_dff(
    eventlocked_dff: np.ndarray,
    baseline_mask_t: np.ndarray,
    response_mask_t: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return trial-baseline-corrected traces and one response scalar per trial."""
    data = np.asarray(eventlocked_dff, dtype=float)
    baseline = np.nanmean(data[:, :, baseline_mask_t], axis=2, keepdims=True)
    bc = data - baseline
    response = np.nanmean(bc[:, :, response_mask_t], axis=2)
    return bc, response


def _tuning_outputs_from_trials(
    trial_response: np.ndarray,
    analysis_trials: np.ndarray,
    current_value: np.ndarray,
    possible_values: np.ndarray,
    mode: str,
) -> dict[str, np.ndarray]:
    """Recompute tuning curves and scalar metrics from an arbitrary trial-response matrix."""
    tr = np.asarray(trial_response, dtype=float)
    analysis_trials = np.asarray(analysis_trials, dtype=bool)
    current_value = np.asarray(current_value, dtype=float)
    possible_values = np.asarray(possible_values, dtype=float)
    n_cells = tr.shape[0]
    n_val = len(possible_values)

    curves = np.full((n_cells, n_val), np.nan, dtype=float)
    counts = np.zeros(n_val, dtype=int)
    for vi, value in enumerate(possible_values):
        mask = analysis_trials & np.isclose(current_value, value)
        counts[vi] = int(np.sum(mask))
        if np.any(mask):
            curves[:, vi] = np.nanmean(tr[:, mask], axis=1)

    stim_mean = (
        np.nanmean(tr[:, analysis_trials], axis=1)
        if np.any(analysis_trials)
        else np.full(n_cells, np.nan)
    )
    preferred_index = np.full(n_cells, -1, dtype=int)
    preferred_value = np.full(n_cells, np.nan)
    best_response = np.full(n_cells, np.nan)
    peak_abs_response = np.full(n_cells, np.nan)
    modulation_depth = np.full(n_cells, np.nan)
    selectivity_contrast = np.full(n_cells, np.nan)
    selectivity_index = np.full(n_cells, np.nan)
    lifetime = np.full(n_cells, np.nan)
    gini = np.full(n_cells, np.nan)
    fano = np.full(n_cells, np.nan)
    fwhm = np.full(n_cells, np.nan)

    for ci in np.flatnonzero(np.any(np.isfinite(curves), axis=1)):
        curve = curves[ci]
        finite = np.isfinite(curve)
        inds = np.flatnonzero(finite)
        if not len(inds):
            continue
        best_idx = int(inds[int(np.nanargmax(curve[finite]))])
        best = float(curve[best_idx])
        preferred_index[ci] = best_idx
        preferred_value[ci] = possible_values[best_idx]
        best_response[ci] = best
        peak_abs_response[ci] = float(np.nanmax(np.abs(curve)))
        modulation_depth[ci] = float(np.nanmax(curve) - np.nanmin(curve))
        other = finite.copy()
        other[best_idx] = False
        if np.any(other):
            mean_other = float(np.nanmean(curve[other]))
            contrast = best - mean_other
            denom = abs(best) + abs(mean_other)
            selectivity_contrast[ci] = contrast
            if denom > 1e-12:
                selectivity_index[ci] = contrast / denom
        mag = np.abs(curve[finite])
        lifetime[ci] = lifetime_sparseness_nonnegative(mag)
        gini[ci] = gini_coefficient_nonnegative(mag)
        fano[ci] = fano_factor_nonnegative(mag)
        fwhm[ci] = tuning_fwhm(curve, possible_values, mode)

    return {
        "tuning_curves": curves,
        "tuning_counts": counts,
        "stim_response_mean": stim_mean,
        "preferred_index": preferred_index,
        "preferred_value_Hz": preferred_value,
        "best_tuning_response": best_response,
        "peak_absolute_response": peak_abs_response,
        "tuning_modulation_depth": modulation_depth,
        "tuning_selectivity_contrast": selectivity_contrast,
        "tuning_selectivity_index": selectivity_index,
        "tuning_lifetime_sparseness": lifetime,
        "tuning_gini_coefficient": gini,
        "tuning_fano_factor": fano,
        "tuning_fwhm": fwhm,
    }


def _condition_responses_from_trials(
    trial_response: np.ndarray,
    condition_masks: list[np.ndarray],
    n_int: int,
    n_val: int,
) -> np.ndarray:
    out = np.full((trial_response.shape[0], n_int, n_val), np.nan, dtype=float)
    for k, mask in enumerate(condition_masks):
        ii = k // n_val
        vi = k % n_val
        mask = np.asarray(mask, dtype=bool)
        if np.any(mask):
            out[:, ii, vi] = np.nanmean(trial_response[:, mask], axis=1)
    return out


def _condition_selectivity_from_trials(
    trial_response: np.ndarray,
    condition_masks: list[np.ndarray],
) -> np.ndarray:
    if not condition_masks:
        return np.empty((trial_response.shape[0], 0), dtype=float)
    mask_matrix = np.vstack(condition_masks)
    all_trials = np.any(mask_matrix, axis=0)
    out = np.full((trial_response.shape[0], len(condition_masks)), np.nan, dtype=float)
    for k, this_mask in enumerate(mask_matrix):
        this_trials = this_mask & all_trials
        other_trials = all_trials & ~this_trials
        if np.any(this_trials) and np.any(other_trials):
            out[:, k] = (
                np.nanmean(trial_response[:, this_trials], axis=1)
                - np.nanmean(trial_response[:, other_trials], axis=1)
            )
    return out


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
                 stim_duration: np.ndarray, isi: np.ndarray
                 ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    """Monotonically align imaging sound events to behavioral trials.

    Experimental acquisition order is used as a strong prior: normally the first
    imaging sound event corresponds to the first behavioral sound trial.  That
    zero-offset start is ALWAYS tried first.  Only if it fails immediately does
    the function test a small one-sided leading skip (up to MAX_LEADING_SKIP)
    and require several consecutive early intervals to pass timing QC before
    accepting the shifted start.  From the accepted start we walk forward
    monotonically through the two event sequences.

    Normal case
    -----------
    Consecutive imaging and behavioral intervals are paired directly.

    Internal mismatch recovery
    --------------------------
    When a consecutive interval fails timing QC, the function tests whether
    skipping up to ``MAX_INTERNAL_SKIP_PER_STEP`` events on ONE side restores a
    valid timing interval.  This catches isolated missed imaging triggers or
    isolated extra imaging triggers without allowing arbitrary re-ordering.

    Trailing mismatch recovery
    --------------------------
    Once either sequence ends, remaining events on the other side are treated
    as trailing unmatched events.  This supports both common acquisition cases:
    imaging continuing after sound presentation, and sound presentation
    continuing after imaging stopped.

    Returns
    -------
    eventlocked_aligned
        Imaging data containing only matched imaging events.
    valid_aligned
        Valid-event mask for the matched imaging events.
    imaging_indices
        Original imaging-event indices retained.
    behavior_indices
        Original behavioral-trial indices retained.  Every downstream behavior
        array MUST be subset with these indices.
    diag
        Alignment diagnostics saved into the per-session output.
    """
    n_imaging = int(eventlocked.shape[1])
    n_behavior_trials = int(n_behavior_trials)

    if n_imaging < 1 or n_behavior_trials < 1:
        raise ValueError(
            f"Cannot align empty event streams: {n_imaging} imaging events, "
            f"{n_behavior_trials} behavioral trials."
        )

    valid_events = np.asarray(valid_events, dtype=bool).ravel()
    if len(valid_events) < n_imaging:
        raise ValueError(
            f"valid_events has length {len(valid_events)} but eventlocked contains "
            f"{n_imaging} imaging events."
        )

    onset_samples = np.asarray(data2p.event_onset, dtype=float).ravel()
    if len(onset_samples) < n_imaging:
        raise ValueError(
            f"event_onset has length {len(onset_samples)} but eventlocked contains "
            f"{n_imaging} imaging events."
        )
    onset_samples = onset_samples[:n_imaging]
    imaging_time = (onset_samples - onset_samples[0]) / float(data2p.srate)

    stim_duration = np.asarray(stim_duration, dtype=float).ravel()
    isi = np.asarray(isi, dtype=float).ravel()
    if len(stim_duration) < n_behavior_trials or len(isi) < n_behavior_trials:
        raise ValueError(
            "stim_duration/isi are shorter than the behavioral trial count: "
            f"stimDur={len(stim_duration)}, isi={len(isi)}, behavior={n_behavior_trials}."
        )

    behavior_time = np.zeros(n_behavior_trials, dtype=float)
    if n_behavior_trials > 1:
        behavior_intervals = (
            stim_duration[:n_behavior_trials-1] + isi[:n_behavior_trials-1]
        )
        if not np.all(np.isfinite(behavior_intervals)):
            bad = np.flatnonzero(~np.isfinite(behavior_intervals))
            raise ValueError(
                "Non-finite expected behavioral inter-trial intervals at indices "
                f"{bad[:10].tolist()}."
            )
        behavior_time[1:] = np.cumsum(behavior_intervals)

    # -------------------------------------------------------------------------
    # START ALIGNMENT
    # -------------------------------------------------------------------------
    # Zero-offset is the default and is never replaced if its first interval
    # already passes QC.  A leading-offset search is activated ONLY when the
    # very first zero-offset interval fails.  This protects normally aligned
    # sessions from accidental one-trial shifts.
    start_i = 0
    start_j = 0
    leading_imaging = np.array([], dtype=int)
    leading_behavior = np.array([], dtype=int)
    start_alignment_mode = "zero_offset"
    start_candidate_records: list[dict[str, Any]] = []

    if n_imaging > 1 and n_behavior_trials > 1:
        first_obs = imaging_time[1] - imaging_time[0]
        first_exp = behavior_time[1] - behavior_time[0]
        first_err = abs(first_obs - first_exp) if np.isfinite(first_obs) and np.isfinite(first_exp) else np.inf

        if first_err > MAX_ABS_ERROR_S:
            candidates: list[tuple[float, float, int, int, int]] = []

            def evaluate_leading_candidate(ii: int, jj: int, nskip: int):
                n_available = min(
                    LEADING_VALIDATION_INTERVALS,
                    n_imaging - ii - 1,
                    n_behavior_trials - jj - 1,
                )
                if n_available < 2:
                    return
                obs = np.diff(imaging_time[ii:ii+n_available+1])
                exp = np.diff(behavior_time[jj:jj+n_available+1])
                finite = np.isfinite(obs) & np.isfinite(exp)
                if np.count_nonzero(finite) < 2:
                    return
                errs = np.abs(obs[finite] - exp[finite])
                mae0 = float(np.mean(errs))
                max0 = float(np.max(errs))
                rec = {
                    "start_imaging_index": int(ii),
                    "start_behavior_index": int(jj),
                    "n_leading_skipped": int(nskip),
                    "n_validation_intervals": int(np.count_nonzero(finite)),
                    "validation_mae_s": mae0,
                    "validation_max_abs_error_s": max0,
                    "passed": bool(max0 <= MAX_ABS_ERROR_S and mae0 <= MAX_MEAN_ABS_ERROR_S),
                }
                start_candidate_records.append(rec)
                if rec["passed"]:
                    score = mae0 + ALIGN_SKIP_PENALTY_S * nskip
                    candidates.append((score, mae0, ii, jj, nskip))

            # One-sided leading skips only.  Do not allow simultaneous shifts
            # on both streams.
            for k in range(1, MAX_LEADING_SKIP + 1):
                if k < n_imaging:
                    evaluate_leading_candidate(k, 0, k)
                if k < n_behavior_trials:
                    evaluate_leading_candidate(0, k, k)

            if not candidates:
                summary = "; ".join(
                    f"img={r['start_imaging_index']},beh={r['start_behavior_index']}: "
                    f"MAE={r['validation_mae_s']:.3f}s,max={r['validation_max_abs_error_s']:.3f}s"
                    for r in start_candidate_records
                )
                raise ValueError(
                    "Initial zero-offset alignment failed and no conservative leading "
                    f"skip of <= {MAX_LEADING_SKIP} event(s) produced "
                    f"{LEADING_VALIDATION_INTERVALS} early intervals within timing QC. "
                    f"Zero-offset first interval error={first_err:.4f}s. "
                    f"Candidates: {summary}"
                )

            candidates.sort(key=lambda x: (x[0], x[1], x[4]))
            _, _, start_i, start_j, _ = candidates[0]
            start_alignment_mode = "leading_fallback"
            leading_imaging = np.arange(0, start_i, dtype=int)
            leading_behavior = np.arange(0, start_j, dtype=int)

            print(
                "Start alignment fallback: zero-offset failed; "
                f"starting at imaging event {start_i}, behavior trial {start_j}. "
                f"Leading ignored: imaging={len(leading_imaging)}, "
                f"behavior={len(leading_behavior)}."
            )

    # All subsequent matching is monotonic.
    matched_imaging = [int(start_i)]
    matched_behavior = [int(start_j)]
    skipped_imaging_internal: list[int] = []
    skipped_behavior_internal: list[int] = []
    step_records: list[dict[str, Any]] = []

    i = int(start_i)
    j = int(start_j)
    while (i + 1 < n_imaging) and (j + 1 < n_behavior_trials):
        obs_dt = imaging_time[i + 1] - imaging_time[i]
        exp_dt = behavior_time[j + 1] - behavior_time[j]
        normal_err = abs(obs_dt - exp_dt) if np.isfinite(obs_dt) and np.isfinite(exp_dt) else np.inf

        if normal_err <= MAX_ABS_ERROR_S:
            ni, nj = i + 1, j + 1
            chosen_err = float(normal_err)
            skip_img = 0
            skip_beh = 0
        else:
            # Search only local, one-sided skips.  We do NOT allow arbitrary
            # offsets or simultaneous skipping on both sides.
            candidates: list[tuple[float, float, int, int, int, int]] = []

            for k in range(1, MAX_INTERNAL_SKIP_PER_STEP + 1):
                # Extra/misdetected imaging event(s): skip imaging event(s).
                ni = i + 1 + k
                nj = j + 1
                if ni < n_imaging:
                    obs = imaging_time[ni] - imaging_time[i]
                    exp = behavior_time[nj] - behavior_time[j]
                    raw_err = abs(obs - exp) if np.isfinite(obs) and np.isfinite(exp) else np.inf
                    if raw_err <= MAX_ABS_ERROR_S:
                        score = raw_err + ALIGN_SKIP_PENALTY_S * k
                        candidates.append((score, raw_err, ni, nj, k, 0))

                # Missed imaging trigger / unmatched behavioral trial(s): skip
                # behavioral trial(s).
                ni = i + 1
                nj = j + 1 + k
                if nj < n_behavior_trials:
                    obs = imaging_time[ni] - imaging_time[i]
                    exp = behavior_time[nj] - behavior_time[j]
                    raw_err = abs(obs - exp) if np.isfinite(obs) and np.isfinite(exp) else np.inf
                    if raw_err <= MAX_ABS_ERROR_S:
                        score = raw_err + ALIGN_SKIP_PENALTY_S * k
                        candidates.append((score, raw_err, ni, nj, 0, k))

            if not candidates:
                raise ValueError(
                    "Internal event alignment failed. "
                    f"At matched imaging event {i} / behavior trial {j}, the next "
                    f"interval error was {normal_err:.4f}s and no one-sided skip of "
                    f"<= {MAX_INTERNAL_SKIP_PER_STEP} event(s) restored timing within "
                    f"{MAX_ABS_ERROR_S:.2f}s."
                )

            candidates.sort(key=lambda x: (x[0], x[1], x[4] + x[5]))
            score, raw_err, ni, nj, skip_img, skip_beh = candidates[0]

            # A skip must genuinely improve the failed direct match after its
            # explicit complexity penalty; otherwise do not silently rescue an
            # ambiguous alignment.
            if not (score < normal_err):
                raise ValueError(
                    "Internal event alignment was ambiguous. "
                    f"Direct interval error={normal_err:.4f}s; best skip candidate "
                    f"raw error={raw_err:.4f}s, penalized score={score:.4f}s."
                )
            chosen_err = float(raw_err)

            if skip_img:
                skipped_imaging_internal.extend(range(i + 1, ni))
            if skip_beh:
                skipped_behavior_internal.extend(range(j + 1, nj))

        matched_imaging.append(int(ni))
        matched_behavior.append(int(nj))
        step_records.append({
            "from_imaging": int(i), "to_imaging": int(ni),
            "from_behavior": int(j), "to_behavior": int(nj),
            "skipped_imaging": int(skip_img),
            "skipped_behavior": int(skip_beh),
            "timing_error_s": float(chosen_err),
        })
        i, j = int(ni), int(nj)

        if (len(skipped_imaging_internal) + len(skipped_behavior_internal)) > MAX_TOTAL_INTERNAL_SKIPS:
            raise ValueError(
                "Alignment required too many internal skips: "
                f"{len(skipped_imaging_internal)} imaging + "
                f"{len(skipped_behavior_internal)} behavioral > "
                f"MAX_TOTAL_INTERNAL_SKIPS={MAX_TOTAL_INTERNAL_SKIPS}."
            )

    matched_imaging = np.asarray(matched_imaging, dtype=int)
    matched_behavior = np.asarray(matched_behavior, dtype=int)

    trailing_imaging = np.arange(i + 1, n_imaging, dtype=int)
    trailing_behavior = np.arange(j + 1, n_behavior_trials, dtype=int)

    # Require that the matched sequence still represents most of BOTH streams.
    n_matched = len(matched_imaging)
    coverage = n_matched / float(max(n_imaging, n_behavior_trials))
    if coverage < MIN_ALIGNMENT_COVERAGE:
        raise ValueError(
            f"Alignment retained only {n_matched}/{max(n_imaging, n_behavior_trials)} "
            f"events ({100*coverage:.1f}% coverage), below the required "
            f"{100*MIN_ALIGNMENT_COVERAGE:.0f}%."
        )

    # Strict post-alignment timing QC.  Consecutive matched pairs can span
    # skipped internal events; comparing their cumulative elapsed times is the
    # correct check after a skip.
    if n_matched > 1:
        observed = np.diff(imaging_time[matched_imaging])
        expected = np.diff(behavior_time[matched_behavior])
        finite = np.isfinite(observed) & np.isfinite(expected)
        if not np.any(finite):
            raise ValueError("No finite intervals available for post-alignment QC.")
        err = observed[finite] - expected[finite]
        mae = float(np.mean(np.abs(err)))
        maxerr = float(np.max(np.abs(err)))
    else:
        mae = 0.0
        maxerr = 0.0

    if mae > MAX_MEAN_ABS_ERROR_S or maxerr > MAX_ABS_ERROR_S:
        raise ValueError(
            "Recovered alignment failed final timing QC. "
            f"MAE={mae:.4f}s, max error={maxerr:.4f}s."
        )

    eventlocked_aligned = eventlocked[:, matched_imaging, :]
    valid_aligned = valid_events[matched_imaging]

    note_parts = [f"matched {n_matched} imaging/behavior events"]
    if len(leading_imaging):
        note_parts.append(f"ignored {len(leading_imaging)} leading imaging event(s)")
    if len(leading_behavior):
        note_parts.append(f"ignored {len(leading_behavior)} leading behavior trial(s)")
    if len(skipped_imaging_internal):
        note_parts.append(f"skipped {len(skipped_imaging_internal)} internal imaging event(s)")
    if len(skipped_behavior_internal):
        note_parts.append(f"skipped {len(skipped_behavior_internal)} internal behavior trial(s)")
    if len(trailing_imaging):
        note_parts.append(f"ignored {len(trailing_imaging)} trailing imaging event(s)")
    if len(trailing_behavior):
        note_parts.append(f"ignored {len(trailing_behavior)} trailing behavior trial(s)")

    diag = {
        "n_imaging_events": int(n_imaging),
        "n_behavior_trials": int(n_behavior_trials),
        "n_matched_trials": int(n_matched),
        "alignment_coverage": float(coverage),
        "matched_imaging_indices": [int(x) for x in matched_imaging],
        "matched_behavior_indices": [int(x) for x in matched_behavior],
        "start_alignment_mode": start_alignment_mode,
        "start_imaging_index": int(start_i),
        "start_behavior_index": int(start_j),
        "n_leading_imaging_ignored": int(len(leading_imaging)),
        "n_leading_behavior_ignored": int(len(leading_behavior)),
        "leading_imaging_indices": [int(x) for x in leading_imaging],
        "leading_behavior_indices": [int(x) for x in leading_behavior],
        "start_alignment_candidates": start_candidate_records,
        "n_internal_imaging_skipped": int(len(skipped_imaging_internal)),
        "n_internal_behavior_skipped": int(len(skipped_behavior_internal)),
        "internal_imaging_skipped_indices": [int(x) for x in skipped_imaging_internal],
        "internal_behavior_skipped_indices": [int(x) for x in skipped_behavior_internal],
        "n_trailing_imaging_ignored": int(len(trailing_imaging)),
        "n_trailing_behavior_ignored": int(len(trailing_behavior)),
        "trailing_imaging_indices": [int(x) for x in trailing_imaging],
        "trailing_behavior_indices": [int(x) for x in trailing_behavior],
        # Backward-compatible fields used by earlier reports.
        "n_extra_imaging_events": int(max(0, n_imaging - n_behavior_trials)),
        "n_extra_before": int(len(leading_imaging)),
        "n_extra_after": int(len(trailing_imaging)),
        "timing_mae_s": float(mae),
        "timing_max_abs_error_s": float(maxerr),
        "alignment_note": "; ".join(note_parts) + ".",
        "alignment_steps_with_skips": [
            rec for rec in step_records
            if rec["skipped_imaging"] or rec["skipped_behavior"]
        ],
    }

    return (
        eventlocked_aligned,
        np.asarray(valid_aligned, dtype=bool),
        matched_imaging,
        matched_behavior,
        diag,
    )


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
    eventlocked_all, tvec, valid_events = data2p.event_locked_average(
        time_range=list(TIME_RANGE), dff=True
    )
    eventlocked_raw_all, tvec_raw, valid_events_raw = data2p.event_locked_average(
        time_range=list(TIME_RANGE), dff=False
    )
    if len(tvec_raw) != len(tvec) or not np.allclose(tvec_raw, tvec, equal_nan=True):
        raise ValueError("dff=True and dff=False eventlocked time vectors do not match.")
    valid_events = np.asarray(valid_events, dtype=bool).ravel()
    valid_events_raw = np.asarray(valid_events_raw, dtype=bool).ravel()
    eventlocked = np.asarray(eventlocked_all[cell_mask], dtype=float)
    eventlocked_raw = np.asarray(eventlocked_raw_all[cell_mask], dtype=float)
    if eventlocked_raw.shape != eventlocked.shape:
        raise ValueError("dff=True and dff=False eventlocked arrays do not match in shape.")
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
    cp_settings = {
        "params": None,
        "chan2_params": None,
        "cellprob_threshold": CELLPOSE_CELLPROB_THRESHOLD,
        "flow_threshold": CELLPOSE_FLOW_THRESHOLD,
    }
    print(
        f"Running Cellpose: diameter={diameter:.2f}, "
        f"cellprob={CELLPOSE_CELLPROB_THRESHOLD}, "
        f"flow={CELLPOSE_FLOW_THRESHOLD}, IoU={IOU_THRESHOLD}"
    )
    print(
        "Cellpose execution device: Suite2p auto-detection "
        "(GPU if available, otherwise CPU)"
    )
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
    n_beh_original = len(current_value)
    (
        eventlocked_aligned, valid_aligned, imaging_trial_indices,
        behavior_trial_indices, align_diag
    ) = align_events(
        data2p, eventlocked, valid_events, n_beh_original, stim_duration, isi
    )

    # CRITICAL: subset every behavior array with the exact behavioral indices
    # matched to the retained imaging events.  This keeps all labels synchronized
    # after internal skips or trailing behavior trimming.
    current_value = current_value[behavior_trial_indices]
    current_intensity = current_intensity[behavior_trial_indices]
    stim_duration = stim_duration[behavior_trial_indices]
    isi = isi[behavior_trial_indices]
    laser_trial = laser_trial[behavior_trial_indices]

    # Apply the exact same retained imaging-event indices to raw fluorescence.
    eventlocked_raw_aligned = np.asarray(eventlocked_raw[:, imaging_trial_indices, :], dtype=float)
    event_onset_all = np.asarray(data2p.event_onset, dtype=float).ravel()
    event_onset_aligned = event_onset_all[np.asarray(imaging_trial_indices, dtype=int)]
    if eventlocked_raw_aligned.shape != eventlocked_aligned.shape:
        raise ValueError("Aligned raw and primary eventlocked arrays differ in shape.")

    print("Trial alignment:")
    print(
        f"  imaging events: {align_diag['n_imaging_events']}; "
        f"behavior trials: {align_diag['n_behavior_trials']}; "
        f"matched: {align_diag['n_matched_trials']}"
    )
    print(
        f"  start: mode={align_diag['start_alignment_mode']}; "
        f"imaging_index={align_diag['start_imaging_index']}; "
        f"behavior_index={align_diag['start_behavior_index']}; "
        f"leading ignored: imaging={align_diag['n_leading_imaging_ignored']}, "
        f"behavior={align_diag['n_leading_behavior_ignored']}"
    )
    print(
        f"  internal skips: imaging={align_diag['n_internal_imaging_skipped']}, "
        f"behavior={align_diag['n_internal_behavior_skipped']}"
    )
    print(
        f"  trailing ignored: imaging={align_diag['n_trailing_imaging_ignored']}, "
        f"behavior={align_diag['n_trailing_behavior_ignored']}"
    )
    print(
        f"  timing MAE={align_diag['timing_mae_s']:.4f}s; "
        f"max={align_diag['timing_max_abs_error_s']:.4f}s"
    )
    print(f"  {align_diag['alignment_note']}")

    analysis_trials = np.asarray(valid_aligned & ~laser_trial, dtype=bool)
    possible_values = np.sort(np.unique(current_value[analysis_trials]))
    possible_intensities = np.sort(np.unique(current_intensity[analysis_trials]))
    if len(possible_values) == 0:
        raise ValueError("No valid non-laser tuning trials.")

    baseline_mask = (tvec >= BASELINE_WINDOW[0]) & (tvec < BASELINE_WINDOW[1])
    response_mask = (tvec >= RESPONSE_WINDOW[0]) & (tvec <= RESPONSE_WINDOW[1])
    if not np.any(baseline_mask) or not np.any(response_mask):
        raise ValueError("Event-locked time vector does not cover baseline/response windows.")

    # Primary jaratoolbox dff=True trial responses.
    eventlocked_bc, trial_response = _trial_response_from_dff(
        eventlocked_aligned, baseline_mask, response_mask
    )

    # Alternate dF/F definitions. These are sensitivity outputs only; primary
    # condition-specific responsiveness labels are NOT redefined from them.
    full_session_raw = np.asarray(data2p.roiF[cell_mask, :], dtype=float)
    session_median_dff = _session_median_dff(eventlocked_raw_aligned, full_session_raw)
    local_prestim_dff = _local_prestim_median_dff(
        eventlocked_raw_aligned,
        event_onset_aligned,
        float(data2p.srate),
        np.asarray(valid_aligned, dtype=bool),
        np.asarray(tvec, dtype=float),
        local_window_s=60.0,
        prestim_window_s=(-0.300, 0.0),
    )
    _, trial_response_session_median_dff = _trial_response_from_dff(
        session_median_dff, baseline_mask, response_mask
    )
    _, trial_response_60s_prestim_median_dff = _trial_response_from_dff(
        local_prestim_dff, baseline_mask, response_mask
    )

    # QC: same aligned trials, three F0 definitions.
    _save_eventlocked_average_figure(
        eventlocked_aligned, np.asarray(valid_aligned, dtype=bool), np.asarray(tvec, dtype=float),
        session_output_dir / "all_stimuli_eventlocked_avg_CURRENT_DFF.png",
        f"Current jaratoolbox dff=True\n{title}",
    )
    _save_eventlocked_average_figure(
        session_median_dff, np.asarray(valid_aligned, dtype=bool), np.asarray(tvec, dtype=float),
        session_output_dir / "all_stimuli_eventlocked_avg_SESSION_MEDIAN_DFF.png",
        f"Whole-session median F0 dF/F\n{title}",
    )
    _save_eventlocked_average_figure(
        local_prestim_dff, np.asarray(valid_aligned, dtype=bool), np.asarray(tvec, dtype=float),
        session_output_dir / "all_stimuli_eventlocked_avg_60s_PRESTIM_MEDIAN_DFF.png",
        f"60-s local prestimulus-only median F0 dF/F\n{title}",
    )

    n_int = len(possible_intensities)
    n_val = len(possible_values)
    condition_counts = np.zeros((n_int, n_val), dtype=int)
    condition_masks: list[np.ndarray] = []
    condition_names: list[str] = []
    condition_pairs: list[tuple[float, float]] = []
    for ii, intensity in enumerate(possible_intensities):
        for vi, value in enumerate(possible_values):
            mask = (
                analysis_trials
                & np.isclose(current_intensity, intensity)
                & np.isclose(current_value, value)
            )
            condition_counts[ii, vi] = int(np.sum(mask))
            condition_masks.append(mask.copy())
            condition_pairs.append((float(value), float(intensity)))
            if tuning_mode == "tuningFreq":
                condition_names.append(f"{value/1000:g} kHz, {intensity:g} dB")
            else:
                condition_names.append(f"{value:g} Hz AM, {intensity:g} dB")

    condition_responses = _condition_responses_from_trials(
        trial_response, condition_masks, n_int, n_val
    )
    condition_responses_session_median_dff = _condition_responses_from_trials(
        trial_response_session_median_dff, condition_masks, n_int, n_val
    )
    condition_responses_60s_prestim_median_dff = _condition_responses_from_trials(
        trial_response_60s_prestim_median_dff, condition_masks, n_int, n_val
    )
    condition_responses_flat = condition_responses.reshape(n_cells, n_int * n_val)

    # Primary and alternate tuning metrics, pooled across intensity at each tuning value.
    primary_tuning = _tuning_outputs_from_trials(
        trial_response, analysis_trials, current_value, possible_values, tuning_mode
    )
    alt_session_median = _tuning_outputs_from_trials(
        trial_response_session_median_dff, analysis_trials, current_value, possible_values, tuning_mode
    )
    alt_60s_prestim = _tuning_outputs_from_trials(
        trial_response_60s_prestim_median_dff, analysis_trials, current_value, possible_values, tuning_mode
    )
    tuning_curves = primary_tuning["tuning_curves"]
    tuning_counts = primary_tuning["tuning_counts"]

    # Global all-trials response test retained as metadata/backward-compatible p/q.
    stim_evoked = np.where(analysis_trials[None, :], trial_response, np.nan)
    mean_stim = np.nanmean(stim_evoked, axis=1)
    median_stim = np.nanmedian(stim_evoked, axis=1)
    sd_stim = np.nanstd(stim_evoked, axis=1, ddof=1)
    nfinite = np.sum(np.isfinite(stim_evoked), axis=1)
    sem_stim = np.full(n_cells, np.nan)
    ok = nfinite > 1
    sem_stim[ok] = sd_stim[ok] / np.sqrt(nfinite[ok])
    dz = np.full(n_cells, np.nan)
    okdz = ok & np.isfinite(sd_stim) & (sd_stim > 0)
    dz[okdz] = mean_stim[okdz] / sd_stim[okdz]
    rng_global = np.random.default_rng(seed + int(date[-4:]) + int(session))
    global_pvals = signflip_pvalues_grouped(stim_evoked, n_permutations, rng_global)
    global_qvals = bh_fdr(global_pvals)
    global_responsive_fdr = np.isfinite(global_qvals) & (global_qvals < FDR_ALPHA)

    # v9 PRIMARY responsiveness: test each tuning value separately, pooling
    # across intensity. BH-FDR is applied separately across cells within each
    # tuning value; the generic stim_responsive_fdr is their union.
    tuning_value_p = np.full((n_cells, n_val), np.nan, dtype=float)
    tuning_value_q = np.full((n_cells, n_val), np.nan, dtype=float)
    tuning_value_responsive = np.zeros((n_cells, n_val), dtype=bool)
    for vi, value in enumerate(possible_values):
        mask = analysis_trials & np.isclose(current_value, value)
        if np.sum(mask) < 2:
            continue
        matrix = np.where(mask[None, :], trial_response, np.nan)
        rng_value = np.random.default_rng(
            int(seed) + int(date[-4:]) * 1009 + int(session) * 9176 + vi * 104729
        )
        p_here = signflip_pvalues_grouped(matrix, n_permutations, rng_value)
        q_here = bh_fdr(p_here)
        tuning_value_p[:, vi] = p_here
        tuning_value_q[:, vi] = q_here
        tuning_value_responsive[:, vi] = np.isfinite(q_here) & (q_here < FDR_ALPHA)

    responsive_fdr = np.any(tuning_value_responsive, axis=1)
    excited_fdr = np.zeros(n_cells, dtype=bool)
    suppressed_fdr = np.zeros(n_cells, dtype=bool)
    for ci in np.flatnonzero(responsive_fdr):
        inds = np.flatnonzero(tuning_value_responsive[ci] & np.isfinite(tuning_curves[ci]))
        if not len(inds):
            continue
        strongest = int(inds[np.argmax(np.abs(tuning_curves[ci, inds]))])
        val = float(tuning_curves[ci, strongest])
        excited_fdr[ci] = val > 0
        suppressed_fdr[ci] = val < 0

    # Amplitude-threshold raster criterion.
    peak_abs_condition = np.full(n_cells, np.nan)
    finite_rows = np.any(np.isfinite(condition_responses_flat), axis=1)
    peak_abs_condition[finite_rows] = np.nanmax(
        np.abs(condition_responses_flat[finite_rows]), axis=1
    )
    amplitude_responsive = np.isfinite(peak_abs_condition) & (
        peak_abs_condition > RASTER_MIN_ABS_RESPONSE
    )

    # Primary scalar metrics.
    preferred_index = primary_tuning["preferred_index"]
    preferred_value = primary_tuning["preferred_value_Hz"]
    best_response = primary_tuning["best_tuning_response"]
    peak_abs_response = primary_tuning["peak_absolute_response"]
    modulation_depth = primary_tuning["tuning_modulation_depth"]
    selectivity_contrast = primary_tuning["tuning_selectivity_contrast"]
    selectivity_index = primary_tuning["tuning_selectivity_index"]
    tuning_lifetime_sparseness = primary_tuning["tuning_lifetime_sparseness"]
    tuning_gini_coefficient = primary_tuning["tuning_gini_coefficient"]
    tuning_fano_factor = primary_tuning["tuning_fano_factor"]
    tuning_fwhm_values = primary_tuning["tuning_fwhm"]

    # Condition-selectivity contrast = this intensity x tuning condition - all others.
    cond_selectivity = _condition_selectivity_from_trials(trial_response, condition_masks)
    cond_selectivity_session_median_dff = _condition_selectivity_from_trials(
        trial_response_session_median_dff, condition_masks
    )
    cond_selectivity_60s_prestim_median_dff = _condition_selectivity_from_trials(
        trial_response_60s_prestim_median_dff, condition_masks
    )

    cell_class = np.where(yellow_mask, "yellow", "green")

    # ---------------------------------------------------------------------
    # v9 compact per-trial archive for downstream trial-repetition analysis.
    # ---------------------------------------------------------------------
    n_aligned_trials = len(current_value)
    trial_condition_index = np.full(n_aligned_trials, -1, dtype=np.int16)
    for k, mask in enumerate(condition_masks):
        trial_condition_index[np.asarray(mask, dtype=bool)] = int(k)
    trial_tuning_value_index = np.full(n_aligned_trials, -1, dtype=np.int16)
    for vi, value in enumerate(possible_values):
        trial_tuning_value_index[
            analysis_trials & np.isclose(current_value, value)
        ] = int(vi)

    trial_archive_path = (
        session_output_dir
        / f"{subject}_{date}_{session}_p{plane}_trial_response_archive_v9.npz"
    )
    np.savez_compressed(
        trial_archive_path,
        archive_schema_version=np.asarray(1, dtype=np.int16),
        source_script_version=np.asarray("v9"),
        subject=np.asarray(subject),
        date=np.asarray(date),
        session=np.asarray(session),
        session_key=np.asarray(f"{date}_{session}"),
        canonical_area=np.asarray(str(meta.get("canonicalArea"))),
        brain_area=np.asarray(str(meta.get("brainArea"))),
        depth_um=np.asarray(float(meta.get("depth")) if meta.get("depth") is not None else np.nan),
        plane=np.asarray(int(plane), dtype=np.int16),
        tuning_mode=np.asarray(tuning_mode),
        sampling_rate_hz=np.asarray(float(data2p.srate)),
        baseline_window_s=np.asarray(BASELINE_WINDOW, dtype=float),
        response_window_s=np.asarray(RESPONSE_WINDOW, dtype=float),
        fdr_alpha=np.asarray(float(FDR_ALPHA)),
        n_permutations_full_analysis=np.asarray(int(n_permutations), dtype=np.int32),
        full_analysis_seed=np.asarray(int(seed), dtype=np.int64),
        trial_index=np.arange(n_aligned_trials, dtype=np.int32),
        valid_trial_mask=np.asarray(valid_aligned, dtype=bool),
        analysis_trial_mask=np.asarray(analysis_trials, dtype=bool),
        laser_trial=np.asarray(laser_trial, dtype=bool),
        trial_condition_index=trial_condition_index,
        trial_tuning_value_index=trial_tuning_value_index,
        condition_names=np.asarray(condition_names, dtype=str),
        condition_trial_counts=np.asarray(condition_counts.reshape(-1), dtype=np.int32),
        condition_tuning_value_hz=np.asarray([x[0] for x in condition_pairs], dtype=float),
        condition_intensity_db=np.asarray([x[1] for x in condition_pairs], dtype=float),
        possible_tuning_values_hz=np.asarray(possible_values, dtype=float),
        possible_intensities_db=np.asarray(possible_intensities, dtype=float),
        tuning_value_trial_counts=np.asarray(tuning_counts, dtype=np.int32),
        current_tuning_value_hz=np.asarray(current_value, dtype=float),
        current_intensity_db=np.asarray(current_intensity, dtype=float),
        stim_duration_s=np.asarray(stim_duration, dtype=float),
        isi_s=np.asarray(isi, dtype=float),
        event_onset_samples=np.asarray(event_onset_aligned, dtype=float),
        event_onset_seconds=np.asarray(event_onset_aligned, dtype=float) / float(data2p.srate),
        analysis_cell_index=np.arange(n_cells, dtype=np.int32),
        suite2p_roi_index=np.asarray(cell_roi_indices, dtype=np.int32),
        cell_class=np.asarray(cell_class, dtype=str),
        green_only_mask=np.asarray(green_mask, dtype=bool),
        yellow_cell_mask=np.asarray(yellow_mask, dtype=bool),
        cellpose_red_iou=np.asarray(red_iou, dtype=float),
        trial_response_primary=np.asarray(trial_response, dtype=float),
        trial_response_session_median_dff=np.asarray(
            trial_response_session_median_dff, dtype=float
        ),
        trial_response_60s_prestim_median_dff=np.asarray(
            trial_response_60s_prestim_median_dff, dtype=float
        ),
        primary_tuning_curves=np.asarray(tuning_curves, dtype=float),
        primary_tuning_value_p_values=np.asarray(tuning_value_p, dtype=float),
        primary_tuning_value_q_values=np.asarray(tuning_value_q, dtype=float),
        primary_tuning_value_responsive_fdr=np.asarray(
            tuning_value_responsive, dtype=bool
        ),
        primary_any_tuning_value_responsive_fdr=np.asarray(
            responsive_fdr, dtype=bool
        ),
        primary_stim_excited_fdr=np.asarray(excited_fdr, dtype=bool),
        primary_stim_suppressed_fdr=np.asarray(suppressed_fdr, dtype=bool),
        primary_global_stim_response_p=np.asarray(global_pvals, dtype=float),
        primary_global_stim_response_q=np.asarray(global_qvals, dtype=float),
        primary_global_stim_responsive_fdr=np.asarray(
            global_responsive_fdr, dtype=bool
        ),
        primary_condition_responses=np.asarray(condition_responses, dtype=float),
        session_median_tuning_curves=np.asarray(
            alt_session_median["tuning_curves"], dtype=float
        ),
        prestim_60s_tuning_curves=np.asarray(
            alt_60s_prestim["tuning_curves"], dtype=float
        ),
        session_median_condition_responses=np.asarray(
            condition_responses_session_median_dff, dtype=float
        ),
        prestim_60s_condition_responses=np.asarray(
            condition_responses_60s_prestim_median_dff, dtype=float
        ),
    )
    with np.load(trial_archive_path, allow_pickle=False) as chk:
        expected = (n_cells, n_aligned_trials)
        for key in (
            "trial_response_primary",
            "trial_response_session_median_dff",
            "trial_response_60s_prestim_median_dff",
        ):
            if tuple(chk[key].shape) != expected:
                raise RuntimeError(
                    f"v9 trial archive {key} has shape {chk[key].shape}, expected {expected}."
                )
        if tuple(chk["primary_tuning_value_responsive_fdr"].shape) != (n_cells, n_val):
            raise RuntimeError("v9 trial archive tuning-value FDR matrix shape mismatch.")
    print(
        f"Saved v9 trial-response archive: {trial_archive_path} "
        f"({trial_archive_path.stat().st_size / (1024**2):.2f} MiB)"
    )

    rows: list[dict[str, Any]] = []
    for ci in range(n_cells):
        row: dict[str, Any] = {
            "subject": subject, "date": date, "session": session,
            "session_key": f"{date}_{session}", "brainArea": meta.get("brainArea"),
            "canonicalArea": meta.get("canonicalArea"), "depth": meta.get("depth"),
            "sessionLabel": meta.get("sessionLabel"), "plane": plane,
            "tuning_mode": tuning_mode, "analysis_cell_index": ci,
            "suite2p_roi_index": int(cell_roi_indices[ci]), "cell_class": cell_class[ci],
            "trial_response_archive_path": str(trial_archive_path),
            "trial_response_archive_schema_version": 1,
            "cellpose_red_iou": float(red_iou[ci]), "suite2p_chan2_score": float(legacy_scores[ci]),
            "stim_response_mean": float(mean_stim[ci]), "stim_response_median": float(median_stim[ci]),
            "stim_response_sem": float(sem_stim[ci]), "stim_response_dz": float(dz[ci]),
            # Backward-compatible global all-trials p/q:
            "stim_response_p": float(global_pvals[ci]), "stim_response_q": float(global_qvals[ci]),
            "global_stim_responsive_fdr": bool(global_responsive_fdr[ci]),
            # PRIMARY v9 condition-specific union:
            "stim_responsive_fdr": bool(responsive_fdr[ci]),
            "any_tuning_value_responsive_fdr": bool(responsive_fdr[ci]),
            "stim_excited_fdr": bool(excited_fdr[ci]),
            "stim_suppressed_fdr": bool(suppressed_fdr[ci]),
            "best_tuning_response": float(best_response[ci]),
            "peak_absolute_response": float(peak_abs_response[ci]),
            "tuning_modulation_depth": float(modulation_depth[ci]),
            "tuning_selectivity_contrast": float(selectivity_contrast[ci]),
            "tuning_selectivity_index": float(selectivity_index[ci]),
            "tuning_lifetime_sparseness": float(tuning_lifetime_sparseness[ci]),
            "tuning_gini_coefficient": float(tuning_gini_coefficient[ci]),
            "tuning_fano_factor": float(tuning_fano_factor[ci]),
            "tuning_fwhm": float(tuning_fwhm_values[ci]),
            "tuning_fwhm_units": "octaves" if tuning_mode == "tuningFreq" else "Hz",
            "preferred_tuning_value_Hz": float(preferred_value[ci]),
            "amplitude_responsive_0p02": bool(amplitude_responsive[ci]),

            # Alternate dF/F sensitivity metrics. Responsiveness is intentionally
            # inherited from the primary jaratoolbox dff=True analysis.
            "stim_response_mean_session_median_dff": float(
                alt_session_median["stim_response_mean"][ci]
            ),
            "best_tuning_response_session_median_dff": float(
                alt_session_median["best_tuning_response"][ci]
            ),
            "peak_absolute_response_session_median_dff": float(
                alt_session_median["peak_absolute_response"][ci]
            ),
            "tuning_modulation_depth_session_median_dff": float(
                alt_session_median["tuning_modulation_depth"][ci]
            ),
            "tuning_selectivity_contrast_session_median_dff": float(
                alt_session_median["tuning_selectivity_contrast"][ci]
            ),
            "tuning_selectivity_index_session_median_dff": float(
                alt_session_median["tuning_selectivity_index"][ci]
            ),
            "tuning_lifetime_sparseness_session_median_dff": float(
                alt_session_median["tuning_lifetime_sparseness"][ci]
            ),
            "tuning_gini_coefficient_session_median_dff": float(
                alt_session_median["tuning_gini_coefficient"][ci]
            ),
            "tuning_fano_factor_session_median_dff": float(
                alt_session_median["tuning_fano_factor"][ci]
            ),
            "tuning_fwhm_session_median_dff": float(
                alt_session_median["tuning_fwhm"][ci]
            ),
            "preferred_tuning_value_Hz_session_median_dff": float(
                alt_session_median["preferred_value_Hz"][ci]
            ),
            "stim_response_mean_60s_prestim_median_dff": float(
                alt_60s_prestim["stim_response_mean"][ci]
            ),
            "best_tuning_response_60s_prestim_median_dff": float(
                alt_60s_prestim["best_tuning_response"][ci]
            ),
            "peak_absolute_response_60s_prestim_median_dff": float(
                alt_60s_prestim["peak_absolute_response"][ci]
            ),
            "tuning_modulation_depth_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_modulation_depth"][ci]
            ),
            "tuning_selectivity_contrast_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_selectivity_contrast"][ci]
            ),
            "tuning_selectivity_index_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_selectivity_index"][ci]
            ),
            "tuning_lifetime_sparseness_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_lifetime_sparseness"][ci]
            ),
            "tuning_gini_coefficient_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_gini_coefficient"][ci]
            ),
            "tuning_fano_factor_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_fano_factor"][ci]
            ),
            "tuning_fwhm_60s_prestim_median_dff": float(
                alt_60s_prestim["tuning_fwhm"][ci]
            ),
            "preferred_tuning_value_Hz_60s_prestim_median_dff": float(
                alt_60s_prestim["preferred_value_Hz"][ci]
            ),
        }
        for vi, value in enumerate(possible_values):
            base_prefix = "response_freq" if tuning_mode == "tuningFreq" else "response_AM"
            vtag = f"{value:g}"
            row[f"{base_prefix}_{vtag}_Hz"] = float(tuning_curves[ci, vi])
            row[f"{base_prefix}_{vtag}_Hz_session_median_dff"] = float(
                alt_session_median["tuning_curves"][ci, vi]
            )
            row[f"{base_prefix}_{vtag}_Hz_60s_prestim_median_dff"] = float(
                alt_60s_prestim["tuning_curves"][ci, vi]
            )
            row[f"tuning_value_response_p_{vtag}_Hz"] = float(tuning_value_p[ci, vi])
            row[f"tuning_value_response_q_{vtag}_Hz"] = float(tuning_value_q[ci, vi])
            row[f"tuning_value_responsive_fdr_{vtag}_Hz"] = bool(
                tuning_value_responsive[ci, vi]
            )
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
                "condition_response_session_median_dff":float(
                    condition_responses_session_median_dff[ci, ii, vi]
                ),
                "condition_response_60s_prestim_median_dff":float(
                    condition_responses_60s_prestim_median_dff[ci, ii, vi]
                ),
                "condition_selectivity_contrast":float(cond_selectivity[ci, k]),
                "condition_selectivity_contrast_session_median_dff":float(
                    cond_selectivity_session_median_dff[ci, k]
                ),
                "condition_selectivity_contrast_60s_prestim_median_dff":float(
                    cond_selectivity_60s_prestim_median_dff[ci, k]
                ),
                "n_trials_condition":int(condition_counts[ii, vi]),
            })
    condition_df = pd.DataFrame(condition_rows)
    condition_df.to_csv(session_output_dir / "condition_results.csv", index=False)

    # One row per session x class for primary combined inference.
    class_rows = []
    metrics = [
        "stim_response_mean", "best_tuning_response", "peak_absolute_response",
        "tuning_modulation_depth", "tuning_selectivity_contrast", "tuning_selectivity_index",
        "tuning_lifetime_sparseness", "tuning_gini_coefficient",
        "tuning_fano_factor", "tuning_fwhm",
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
            vals = finite_values(sub[metric])
            r[f"mean_{metric}"] = float(np.mean(vals)) if len(vals) else np.nan
            r[f"std_{metric}"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else np.nan
            r[f"median_{metric}"] = float(np.median(vals)) if len(vals) else np.nan
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
        "condition_counts":condition_counts,
        "trial_response_archive_path": str(trial_archive_path),
        "trial_response_archive_schema_version": 1,
        "responsiveness_definition": (
            "BH-FDR separately across cells within each tuning value (frequency or AM rate), "
            "pooling intensities; stim_responsive_fdr is the union across tuning values"
        ),
        "global_all_trials_response_test_retained_as_metadata": True,
        "alternate_dff_sensitivity_outputs": {
            "session_median_dff": "F0 = whole-session median fluorescence per cell",
            "60s_prestim_median_dff": (
                "F0 = median of -300 to 0 ms prestimulus samples from valid stimuli "
                "within +/-30 s of each event"
            ),
            "responsiveness_recomputed": False,
            "responsiveness_note": (
                "Primary jaratoolbox dff=True tuning-value-specific FDR labels are reused "
                "for alternate-dF/F sensitivity analyses"
            ),
        },
        "selectivity_metric_definitions": {
            "profile": "absolute magnitude of the mean baseline-corrected tuning response at each tuning value",
            "lifetime_sparseness": "Treves-Rolls lifetime sparseness across |response| profile",
            "gini_coefficient": "Gini coefficient across |response| profile",
            "fano_factor": "sample variance / mean across |response| profile; scale-dependent",
            "fwhm": "half-maximum width of |response| around the largest peak; octaves for tuningFreq, Hz for tuningAM; NaN when crossings are not bracketed",
        },
        **align_diag,
    })

    # Per-session responsive figure + tuning figures.
    sound_responsiveness_figure(cell_df, session_output_dir / "stim_responsive_cells_green_yellow.png", title)
    tuning_curve_figures(cell_df, tuning_mode, possible_values, session_output_dir, title)
    tuning_raster_figures(cell_df, tuning_mode, possible_values, session_output_dir, title)
    green_yellow_metric_figures(cell_df, session_output_dir, title)
    condition_profile_figures(condition_df, tuning_mode, session_output_dir, title)
    standalone_selectivity_figures(cell_df, tuning_mode, session_output_dir, title, combined=False)
    save_session_tuning_example_figures(
        cell_df=cell_df, eventlocked_bc=eventlocked_bc, trial_response=trial_response,
        tvec=np.asarray(tvec, dtype=float), analysis_trials=np.asarray(analysis_trials, dtype=bool),
        current_value=np.asarray(current_value, dtype=float), possible_values=np.asarray(possible_values, dtype=float),
        mode=tuning_mode, outdir=session_output_dir, title=title,
    )

    return {
        "meta":meta, "tuning_mode":tuning_mode, "cell_df":cell_df,
        "condition_df":condition_df, "class_summary_df":class_summary_df,
        "possible_values":possible_values, "possible_intensities":possible_intensities,
        "trial_response_archive_path": trial_archive_path,
        "n_aligned_trials": int(n_aligned_trials),
        "n_analysis_trials": int(np.sum(analysis_trials)),
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


def _display_tuning_values(values_hz: np.ndarray, mode: str) -> np.ndarray:
    """Return tuning values in the units shown to the user (kHz or Hz)."""
    values_hz = np.asarray(values_hz, dtype=float)
    return values_hz / 1000.0 if mode == "tuningFreq" else values_hz


def _xplot(values_hz: np.ndarray, mode: str) -> np.ndarray:
    """Return explicit octave coordinates for plotting.

    We plot on a LINEAR Matplotlib axis using x = log2(displayed tuning value).
    This guarantees that equal ratios occupy equal physical distances: for example,
    2->4 kHz and 20->40 kHz are both exactly one x-axis unit apart.
    """
    display_values = _display_tuning_values(values_hz, mode)
    out = np.full(display_values.shape, np.nan, dtype=float)
    good = np.isfinite(display_values) & (display_values > 0)
    out[good] = np.log2(display_values[good])
    return out


def _xlabel(mode: str) -> str:
    return "Tone frequency (kHz)" if mode=="tuningFreq" else "AM rate (Hz)"


def _log2_tick_labels(values: np.ndarray, mode: str) -> list[str]:
    values = np.asarray(values, dtype=float)
    if mode == "tuningFreq":
        return [f"{v/1000:g}" for v in values]
    return [f"{v:g}" for v in values]


def _apply_log2_tuning_axis(ax, values_hz: np.ndarray, mode: str) -> None:
    """Format a true octave-spaced tuning axis using explicit log2 coordinates.

    The plotted x coordinate is log2(frequency/rate in displayed units), while the
    tick labels show the original tuning values.  Thus every doubling has the same
    physical length on the axis regardless of absolute frequency/rate.
    """
    values_hz = np.asarray(values_hz, dtype=float).ravel()
    display_values = _display_tuning_values(values_hz, mode)
    finite = np.isfinite(display_values) & (display_values > 0)
    if not np.any(finite):
        return
    coords = np.log2(display_values[finite])
    ax.set_xscale("linear")
    ax.set_xticks(coords)
    ax.set_xticklabels(_log2_tick_labels(values_hz[finite], mode))
    lo = float(np.min(coords)); hi = float(np.max(coords))
    margin_oct = 0.12
    if hi > lo:
        ax.set_xlim(lo - margin_oct, hi + margin_oct)
    else:
        ax.set_xlim(lo - 0.5, hi + 0.5)


def _log2_bin_edges(values_hz: np.ndarray, mode: str) -> np.ndarray | None:
    """Bin edges in explicit octave coordinates for tuning rasters."""
    values_hz = np.asarray(values_hz, dtype=float).ravel()
    display_values = _display_tuning_values(values_hz, mode)
    if len(display_values) == 0 or np.any(~np.isfinite(display_values)) or np.any(display_values <= 0):
        return None
    centers = np.log2(display_values)
    if len(centers) == 1:
        return np.asarray([centers[0] - 0.5, centers[0] + 0.5], dtype=float)
    mids = 0.5 * (centers[:-1] + centers[1:])
    edges = np.empty(len(centers) + 1, dtype=float)
    edges[1:-1] = mids
    edges[0] = centers[0] - (mids[0] - centers[0])
    edges[-1] = centers[-1] + (centers[-1] - mids[-1])
    return edges


def tuning_curve_figures(cell_df: pd.DataFrame, mode: str, possible_values: np.ndarray,
                         outdir: Path, title: str, prefix: str="") -> None:
    cols, values = _response_columns(cell_df, mode)
    if not cols: return
    x = _xplot(values, mode)
    for responsive_only, tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df = cell_df[cell_df.stim_responsive_fdr] if responsive_only else cell_df
        if len(df)==0: continue
        # Existing detailed version: individual cells + pooled-cell mean/SEM.
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
        _apply_log2_tuning_axis(ax, values, mode)
        ax.legend(frameon=False); ax.grid(alpha=.2); ax.set_title(f"{title}\n{tag.replace('_',' ')}")
        apply_robust_y_limits(ax, allvals, reference_values=(0,))
        fig.savefig(outdir/f"{prefix}tuning_curves_{tag}.png",dpi=300,bbox_inches="tight"); plt.close(fig)

        # MEAN_SEM_ONLY convention from sound v10: light session mean +/- SD
        # across cells, dark overall mean +/- SEM across session means.
        fig,ax=plt.subplots(figsize=(9.5,6.3),constrained_layout=True)
        display=[]
        for cls,color in (("green",GREEN_COLOR),("yellow",YELLOW_COLOR)):
            cdf=df[df.cell_class==cls]
            session_profiles=[]
            for session_key,sdf in cdf.groupby("session_key",sort=True):
                mat=sdf[cols].to_numpy(float)
                if len(mat)==0: continue
                sm=np.nanmean(mat,axis=0)
                ssd=np.nanstd(mat,axis=0,ddof=1) if len(mat)>1 else np.full(len(cols),np.nan)
                session_profiles.append(sm)
                ax.plot(x,sm,color=color,alpha=.24,lw=1.0,marker="o",ms=2.5,zorder=2)
                if np.any(np.isfinite(ssd)):
                    ax.fill_between(x,sm-ssd,sm+ssd,color=color,alpha=.035,zorder=1)
                display.extend(finite_values(sm).tolist())
                display.extend(finite_values(sm-ssd).tolist()); display.extend(finite_values(sm+ssd).tolist())
            if session_profiles:
                smat=np.vstack(session_profiles)
                overall=np.nanmean(smat,axis=0)
                sem=np.asarray([stats.sem(smat[:,i],nan_policy="omit") if np.sum(np.isfinite(smat[:,i]))>1 else np.nan for i in range(len(cols))])
                ax.errorbar(x,overall,yerr=sem,fmt="o-",capsize=4,lw=2.8,elinewidth=2.0,ms=5.5,
                            color=color,label=f"{cls.title()} overall; {len(session_profiles)} sessions",zorder=5)
        ax.axhline(0,color="black",ls=":",lw=1); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Mean response (dF/F)")
        _apply_log2_tuning_axis(ax, values, mode)
        ax.legend(frameon=False); ax.grid(alpha=.2)
        ax.set_title(f"{title}\n{tag.replace('_',' ')} — light=session mean ± SD; dark=overall mean ± SEM")
        apply_robust_y_limits(ax,display,reference_values=(0,))
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
            order=np.argsort(pref)
            edges = _log2_bin_edges(values, mode)
            if edges is not None:
                yedges = np.arange(len(order)+1, dtype=float)
                im = ax.pcolormesh(edges, yedges, matn[order], cmap="coolwarm", vmin=-1, vmax=1, shading="flat")
                ax.set_ylim(len(order), 0)
                _apply_log2_tuning_axis(ax, values, mode)
            else:
                im=ax.imshow(matn[order],aspect="auto",interpolation="nearest",cmap="coolwarm",vmin=-1,vmax=1)
                ticks=np.arange(len(values)); labels=_log2_tick_labels(values, mode)
                ax.set_xticks(ticks,labels,rotation=45,ha="right")
            ax.set_title(f"{cls.title()} n={len(sub)}"); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Cells sorted by preferred value")
            ax.tick_params(axis="x", labelrotation=45)
            for tick in ax.get_xticklabels(): tick.set_ha("right")
            fig.colorbar(im,ax=ax,label="Normalized response")
        fig.suptitle(f"{title}\nSelectivity rasters — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}selectivity_rasters_{tag}.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def green_yellow_metric_figures(cell_df: pd.DataFrame, outdir: Path, title: str, prefix: str="") -> None:
    metrics=[
        ("best_tuning_response","Best tuning response"),("peak_absolute_response","Peak absolute response"),
        ("tuning_modulation_depth","Tuning modulation depth"),("tuning_selectivity_contrast","Legacy best-vs-rest selectivity contrast"),
        ("tuning_selectivity_index","Legacy best-vs-rest selectivity index"),
    ]
    for fdr,tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df=cell_df[cell_df.stim_responsive_fdr] if fdr else cell_df
        if len(df)==0: continue
        # Existing detailed pooled-cell view.
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

        # Session-hierarchy mean-only companion.
        fig,axes=plt.subplots(2,3,figsize=(15,9),constrained_layout=True); axes=axes.ravel()
        colors={"green":GREEN_COLOR,"yellow":YELLOW_COLOR}
        for ax,(metric,label) in zip(axes,metrics):
            display=[]
            sessions=sorted(df.session_key.dropna().astype(str).unique())
            jitter=np.linspace(-.05,.05,max(1,len(sessions)))
            session_means={"green":[],"yellow":[]}
            for si,session_key in enumerate(sessions):
                for xpos,cls in enumerate(("green","yellow")):
                    vals=finite_values(df[(df.session_key.astype(str)==session_key)&(df.cell_class==cls)][metric])
                    m,sd,_,_=mean_sd_sem(vals)
                    if not np.isfinite(m): continue
                    session_means[cls].append(m)
                    xx=xpos+jitter[min(si,len(jitter)-1)]
                    ax.errorbar(xx,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=3.5,elinewidth=.7,capsize=2,
                                color=colors[cls],alpha=.27,zorder=2)
                    display.append(m)
                    if np.isfinite(sd): display.extend([m-sd,m+sd])
            for xpos,cls in enumerate(("green","yellow")):
                m,_,se,n=mean_sd_sem(session_means[cls])
                if np.isfinite(m):
                    ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,elinewidth=2.5,capsize=6,
                                color=colors[cls],zorder=5)
                    txt=f"{m:.3f}±{se:.3f}\nn sess={n}" if np.isfinite(se) else f"{m:.3f}\nn sess={n}"
                    ax.annotate(txt,(xpos,m),xytext=(0,12 if xpos==0 else -32),textcoords="offset points",ha="center",fontsize=7,color=colors[cls])
            ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(label+"\nlight=session mean ± SD; dark=overall mean ± SEM")
            ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
            apply_robust_y_limits(ax,display,reference_values=(0,) if metric!="tuning_selectivity_index" else ())
        axes[-1].axis("off"); fig.suptitle(f"{title}\nGREEN vs YELLOW — {tag.replace('_',' ')} — session hierarchy")
        fig.savefig(outdir/f"{prefix}green_yellow_tuning_summary_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def _plot_green_yellow_cell_metric(ax, df: pd.DataFrame, metric: str, mode: str, title: str) -> None:
    rng = np.random.default_rng(20260819)
    colors = {"green": GREEN_COLOR, "yellow": YELLOW_COLOR}
    allvals = []
    for xpos, cls in enumerate(("green", "yellow")):
        vals = finite_values(df.loc[df.cell_class == cls, metric])
        if len(vals):
            xj = xpos + rng.uniform(-0.10, 0.10, len(vals))
            ax.scatter(xj, vals, s=18, alpha=0.25, color=colors[cls], edgecolors="none", zorder=1)
            m, _, se, n = mean_sd_sem(vals)
            ax.errorbar(xpos, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=9,
                        elinewidth=2.1, capsize=5, color=colors[cls], zorder=4)
            if np.isfinite(m):
                label = f"{m:.3f} ± {se:.3f}\nn={n}" if np.isfinite(se) else f"{m:.3f}\nn={n}"
                ax.annotate(label, (xpos, m), xytext=(0, 12 if xpos == 0 else -32),
                            textcoords="offset points", ha="center", fontsize=8, color=colors[cls])
            allvals.extend(vals.tolist())
    g = finite_values(df.loc[df.cell_class == "green", metric])
    y = finite_values(df.loc[df.cell_class == "yellow", metric])
    p = safe_mannwhitney(g, y).get("p")
    ptxt = "n/a" if p is None else f"{p:.3g}"
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel(selectivity_metric_label(metric, mode))
    ax.set_title(f"{title}\nindividual cells; exploratory pooled MW p={ptxt}")
    ax.grid(axis="y", alpha=.2); ax.spines[["top", "right"]].set_visible(False)
    ref = () if metric != "tuning_fwhm" else ()
    apply_robust_y_limits(ax, allvals, reference_values=ref)


def _plot_green_yellow_session_metric(ax, df: pd.DataFrame, metric: str, mode: str, title: str) -> None:
    colors = {"green": GREEN_COLOR, "yellow": YELLOW_COLOR}
    session_means = {"green": [], "yellow": []}
    display = []
    pairs = {}
    sessions = sorted(df.session_key.dropna().astype(str).unique())
    jitter = np.linspace(-0.055, 0.055, max(len(sessions), 1))
    for si, session_key in enumerate(sessions):
        pairs[session_key] = {}
        for cls in ("green", "yellow"):
            vals = finite_values(df[(df.session_key.astype(str) == session_key) & (df.cell_class == cls)][metric])
            m, sd, _, _ = mean_sd_sem(vals)
            pairs[session_key][cls] = m
            if np.isfinite(m):
                session_means[cls].append(m)
                xpos = (0 if cls == "green" else 1) + jitter[min(si, len(jitter)-1)]
                ax.errorbar(xpos, m, yerr=sd if np.isfinite(sd) else None, fmt="o", ms=4,
                            elinewidth=.8, capsize=2.3, color=colors[cls], alpha=.30, zorder=2)
                display.append(m)
                if np.isfinite(sd): display.extend([m-sd, m+sd])
    for pair in pairs.values():
        g, y = pair.get("green", np.nan), pair.get("yellow", np.nan)
        if np.isfinite(g) and np.isfinite(y):
            ax.plot([0, 1], [g, y], color="0.65", alpha=.24, lw=.8, zorder=1)
    overall = {}
    for xpos, cls in enumerate(("green", "yellow")):
        m, _, se, n = mean_sd_sem(session_means[cls])
        overall[cls] = m
        if np.isfinite(m):
            ax.errorbar(xpos, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=10,
                        elinewidth=2.6, capsize=6, color=colors[cls], alpha=1, zorder=5)
            label = f"{m:.3f} ± {se:.3f}\nn sess={n}" if np.isfinite(se) else f"{m:.3f}\nn sess={n}"
            ax.annotate(label, (xpos, m), xytext=(0, 13 if xpos == 0 else -34),
                        textcoords="offset points", ha="center", fontsize=8, color=colors[cls])
    wide = df.groupby(["session_key", "cell_class"])[metric].mean().unstack("cell_class")
    if "green" in wide and "yellow" in wide:
        res = safe_paired_wilcoxon(wide["green"], wide["yellow"])
        p = res.get("p")
    else:
        p = None
    ptxt = "n/a" if p is None else f"{p:.3g}"
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel(selectivity_metric_label(metric, mode))
    ax.set_title(f"{title}\nlight=session mean ± SD; dark=overall mean ± SEM; paired p={ptxt}")
    ax.grid(axis="y", alpha=.2); ax.spines[["top", "right"]].set_visible(False)
    apply_robust_y_limits(ax, display)


def standalone_selectivity_figures(cell_df: pd.DataFrame, mode: str, outdir: Path, title: str,
                                   combined: bool = False, prefix: str = "") -> None:
    metrics = [
        ("tuning_lifetime_sparseness", "lifetime_sparseness"),
        ("tuning_gini_coefficient", "gini_coefficient"),
        ("tuning_fano_factor", "fano_factor"),
        ("tuning_fwhm", "fwhm_bandwidth"),
    ]
    for responsive_only, tag in ((False, "all_cells"), (True, "FDR_responsive_only")):
        df = cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
        if len(df) == 0:
            continue
        for metric, slug in metrics:
            fig, ax = plt.subplots(figsize=(7.2, 6.2))
            _plot_green_yellow_cell_metric(ax, df, metric, mode,
                                           f"{title}\n{selectivity_metric_label(metric, mode)} — {tag.replace('_',' ')}")
            fig.text(.5, .005, selectivity_equation_footer(mode), ha="center", va="bottom", fontsize=7.5)
            fig.subplots_adjust(bottom=.14)
            fig.savefig(outdir / f"{prefix}{slug}_green_yellow_{tag}_CELL_POINTS.png", dpi=300, bbox_inches="tight")
            plt.close(fig)
            if combined:
                fig, ax = plt.subplots(figsize=(7.2, 6.2))
                _plot_green_yellow_session_metric(ax, df, metric, mode,
                                                  f"{title}\n{selectivity_metric_label(metric, mode)} — {tag.replace('_',' ')}")
                fig.text(.5, .005, selectivity_equation_footer(mode), ha="center", va="bottom", fontsize=7.5)
                fig.subplots_adjust(bottom=.14)
                fig.savefig(outdir / f"{prefix}{slug}_green_yellow_{tag}_SESSION_POINTS.png", dpi=300, bbox_inches="tight")
                plt.close(fig)


def _plot_example_trace_axis(ax, traces: np.ndarray, tvec: np.ndarray, color: str, label: str) -> None:
    traces = np.asarray(traces, dtype=float)
    if traces.ndim == 1:
        traces = traces[None, :]
    if traces.size == 0 or traces.shape[0] == 0:
        ax.text(.5, .5, "No trials", transform=ax.transAxes, ha="center", va="center")
        ax.set_title(label); return
    for tr in traces:
        ax.plot(tvec, tr, color=color, alpha=.15, lw=.75, ls="--")
    mean = np.nanmean(traces, axis=0)
    sd = np.nanstd(traces, axis=0, ddof=1) if traces.shape[0] > 1 else np.full_like(mean, np.nan)
    ax.plot(tvec, mean, color=color, lw=2.4)
    if np.any(np.isfinite(sd)):
        ax.fill_between(tvec, mean-sd, mean+sd, color=color, alpha=.15)
    ax.axvline(0, color="black", ls=":", lw=.8); ax.axhline(0, color="black", ls=":", lw=.7)
    ax.set_title(f"{label}\nn={traces.shape[0]} trials")
    ax.set_xlabel("Time from onset (s)"); ax.grid(axis="y", alpha=.18)
    ax.spines[["top", "right"]].set_visible(False)


def _plot_example_scalar_points(
    ax,
    values_by_tuning: list[np.ndarray],
    tuning_values_hz: np.ndarray,
    labels: list[str],
    colors: list[Any],
    ylabel: str,
    mode: str,
) -> None:
    rng = np.random.default_rng(20260820)
    xvals = _xplot(np.asarray(tuning_values_hz, dtype=float), mode)
    means, sds = [], []
    for xpos, vals0, label, color in zip(xvals, values_by_tuning, labels, colors):
        vals = finite_values(vals0)
        if len(vals):
            if np.isfinite(xpos) and xpos > 0:
                # Jitter symmetrically in explicit octave coordinates so the visual
                # spread is constant across low and high frequencies/rates.
                xj = xpos + rng.uniform(-0.045, 0.045, len(vals))
            else:
                xj = np.full(len(vals), xpos, dtype=float)
            ax.scatter(xj, vals, s=17, color=color, alpha=.24, edgecolors="none")
        m, sd, _, _ = mean_sd_sem(vals); means.append(m); sds.append(sd)
        if np.isfinite(m):
            ax.errorbar(xpos, m, yerr=sd if np.isfinite(sd) else None, fmt="o", ms=7.5,
                        elinewidth=2, capsize=4.5, color=color, zorder=4)
    ax.axhline(0, color="black", ls=":", lw=.8)
    _apply_log2_tuning_axis(ax, np.asarray(tuning_values_hz, dtype=float), mode)
    ax.set_xlabel(_xlabel(mode))
    ax.tick_params(axis="x", labelrotation=45)
    for tick in ax.get_xticklabels():
        tick.set_ha("right")
    ax.set_ylabel(ylabel); ax.grid(axis="y", alpha=.18); ax.spines[["top", "right"]].set_visible(False)
    optimized_summary_ylim(ax, means, sds, reference_values=(0,))


def _save_ranked_tuning_examples(cell_df: pd.DataFrame, eventlocked_bc: np.ndarray, trial_response: np.ndarray,
                                 tvec: np.ndarray, analysis_trials: np.ndarray, current_value: np.ndarray,
                                 possible_values: np.ndarray, mode: str, outdir: Path, title: str,
                                 folder: str, rank_metric: str, rank_label: str, require_fdr: bool) -> None:
    root = outdir / folder; root.mkdir(parents=True, exist_ok=True)
    cmap = plt.cm.viridis(np.linspace(.12, .88, max(1, len(possible_values))))
    labels = [f"{v/1000:g} kHz" if mode == "tuningFreq" else f"{v:g} Hz" for v in possible_values]
    masks = [analysis_trials & np.isclose(current_value, v) for v in possible_values]
    for cls in ("green", "yellow"):
        cdf = cell_df[cell_df.cell_class == cls].copy()
        if require_fdr:
            cdf = cdf[cdf.stim_responsive_fdr.astype(bool)].copy()
        cdf = cdf[np.isfinite(cdf[rank_metric])].copy()
        if len(cdf) == 0: continue
        cdf["_rank_abs"] = np.abs(cdf[rank_metric].to_numpy(float))
        cdf = cdf.sort_values("_rank_abs", ascending=False).head(N_EXAMPLE_CELLS_PER_CLASS)
        class_dir = root / cls; class_dir.mkdir(parents=True, exist_ok=True)
        for rank, (_, row) in enumerate(cdf.iterrows(), start=1):
            ci = int(row.analysis_cell_index); roi = int(row.suite2p_roi_index)
            # Full event-locked traces: one column per tuning value, pooled across intensity.
            fig, axes = plt.subplots(1, max(1, len(possible_values)),
                                     figsize=(max(14, 3.3*len(possible_values)), 5.8), squeeze=False)
            for vi, ax in enumerate(axes.ravel()):
                if vi < len(possible_values):
                    _plot_example_trace_axis(ax, eventlocked_bc[ci, masks[vi], :], tvec, cmap[vi], labels[vi])
                    if vi == 0: ax.set_ylabel("Baseline-subtracted dF/F")
                else: ax.axis("off")
            rank_display = abs(float(row[rank_metric])) if rank_metric == "stim_response_mean" else float(row[rank_metric])
            fig.suptitle(f"{title} | {cls.upper()} rank {rank} | ROI {roi}\n"
                         f"{rank_label}={rank_display:.3f} | "
                         f"lifetime sparseness={float(row.tuning_lifetime_sparseness):.3f}", y=.98)
            fig.text(.5, .01, selectivity_equation_footer(mode), ha="center", va="bottom", fontsize=7.5)
            fig.subplots_adjust(top=.78, bottom=.18, wspace=.28)
            fig.savefig(class_dir / f"rank_{rank:02d}_roi_{roi:04d}_full_traces.png", dpi=300, bbox_inches="tight")
            plt.close(fig)
            # Scalar per-trial response amplitude, same metric used by analysis.
            fig, ax = plt.subplots(figsize=(max(8, 1.25*len(possible_values)), 6), constrained_layout=True)
            _plot_example_scalar_points(
                ax,
                [trial_response[ci, m] for m in masks],
                possible_values,
                labels,
                list(cmap),
                "Mean baseline-corrected dF/F (0–1 s)",
                mode,
            )
            ax.set_title("Trial response amplitudes\nlight=trials; dark=mean ± SD")
            fig.suptitle(f"{title} | {cls.upper()} rank {rank} | ROI {roi}\n"
                         f"{rank_label}={rank_display:.3f} | "
                         f"lifetime sparseness={float(row.tuning_lifetime_sparseness):.3f}", y=1.02)
            fig.text(.5, -.015, selectivity_equation_footer(mode), ha="center", va="top", fontsize=7.5)
            fig.savefig(class_dir / f"rank_{rank:02d}_roi_{roi:04d}_response_scalars.png", dpi=300, bbox_inches="tight")
            plt.close(fig)


def save_session_tuning_example_figures(cell_df: pd.DataFrame, eventlocked_bc: np.ndarray, trial_response: np.ndarray,
                                        tvec: np.ndarray, analysis_trials: np.ndarray, current_value: np.ndarray,
                                        possible_values: np.ndarray, mode: str, outdir: Path, title: str) -> None:
    _save_ranked_tuning_examples(cell_df, eventlocked_bc, trial_response, tvec, analysis_trials, current_value,
                                 possible_values, mode, outdir, title, "example_selective_cells",
                                 "tuning_lifetime_sparseness", "lifetime sparseness", False)
    _save_ranked_tuning_examples(cell_df, eventlocked_bc, trial_response, tvec, analysis_trials, current_value,
                                 possible_values, mode, outdir, title, "example_stim_responsive_cells",
                                 "stim_response_mean", "|mean stimulus response| rank metric", True)


def tuning_profile_session_hierarchy_figure(cell_df: pd.DataFrame, mode: str, outdir: Path, title: str,
                                            prefix: str = "") -> None:
    cols, values = _response_columns(cell_df, mode)
    if not cols: return
    x = _xplot(values, mode)
    for responsive_only, tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df = cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
        if len(df) == 0: continue
        fig, ax = plt.subplots(figsize=(10, 6.4), constrained_layout=True)
        for cls, color in (("green", GREEN_COLOR), ("yellow", YELLOW_COLOR)):
            class_df = df[df.cell_class == cls]
            session_profiles = []
            for session_key, sdf in class_df.groupby("session_key", sort=True):
                mat = sdf[cols].to_numpy(float)
                if len(mat) == 0: continue
                mean = np.nanmean(mat, axis=0)
                sd = np.nanstd(mat, axis=0, ddof=1) if len(mat) > 1 else np.full(len(cols), np.nan)
                session_profiles.append(mean)
                ax.plot(x, mean, color=color, alpha=.25, lw=1.0, marker="o", ms=2.5)
                if np.any(np.isfinite(sd)):
                    ax.fill_between(x, mean-sd, mean+sd, color=color, alpha=.035)
            if session_profiles:
                smat = np.vstack(session_profiles)
                overall = np.nanmean(smat, axis=0)
                sem = np.asarray([stats.sem(smat[:,i], nan_policy="omit") if np.sum(np.isfinite(smat[:,i])) > 1 else np.nan for i in range(len(cols))])
                ax.errorbar(x, overall, yerr=sem, fmt="o-", color=color, lw=2.8, ms=5.5,
                            elinewidth=2.0, capsize=4, label=f"{cls.title()} overall (sessions={len(session_profiles)})", zorder=5)
        ax.axhline(0,color="black",ls=":",lw=.9); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Baseline-subtracted dF/F")
        _apply_log2_tuning_axis(ax, values, mode)
        ax.set_title(f"{title}\nlight=session mean ± SD; dark=overall mean ± SEM — {tag.replace('_',' ')}")
        ax.legend(frameon=False); ax.grid(alpha=.2); ax.spines[["top","right"]].set_visible(False)
        fig.savefig(outdir / f"{prefix}tuning_curves_{tag}_SESSION_HIERARCHY.png", dpi=300, bbox_inches="tight")
        plt.close(fig)


def tuning_profiles_sessions_top_cells(cell_df: pd.DataFrame, mode: str, outdir: Path, title: str,
                                       prefix: str = "") -> None:
    cols, values = _response_columns(cell_df, mode)
    if not cols: return
    x = _xplot(values, mode)
    for responsive_only, tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df = cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
        if len(df) == 0: continue
        fig, ax = plt.subplots(figsize=(10,6.3), constrained_layout=True)
        for cls,color in (("green",GREEN_COLOR),("yellow",YELLOW_COLOR)):
            cdf=df[df.cell_class==cls]
            for session_key,sdf in cdf.groupby("session_key",sort=True):
                mat=sdf[cols].to_numpy(float)
                if len(mat)==0: continue
                ranks=sdf.tuning_lifetime_sparseness.to_numpy(float)
                valid=np.flatnonzero(np.isfinite(ranks))
                valid=valid[np.argsort(ranks[valid])[::-1]][:N_TOP_PROFILE_CELLS_PER_SESSION_CLASS]
                for ridx in valid:
                    ax.plot(x,mat[ridx],color=color,alpha=.15,lw=.8,ls="--",zorder=1)
                ax.plot(x,np.nanmean(mat,axis=0),color=color,alpha=.65,lw=1.8,ls="-",marker="o",ms=3,zorder=3)
        ax.axhline(0,color="black",ls=":",lw=.9); ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Baseline-subtracted dF/F")
        _apply_log2_tuning_axis(ax, values, mode)
        ax.set_title(f"{title}\nsolid=session means; dashed=top 5 cells/session by lifetime sparseness — {tag.replace('_',' ')}")
        handles=[Line2D([0],[0],color=GREEN_COLOR,lw=2,label="Green session mean"),
                 Line2D([0],[0],color=YELLOW_COLOR,lw=2,label="Yellow session mean"),
                 Line2D([0],[0],color="0.35",lw=1,ls="--",alpha=.5,label="High-sparseness cell")]
        ax.legend(handles=handles,frameon=False); ax.grid(alpha=.2); ax.spines[["top","right"]].set_visible(False)
        fig.savefig(outdir/f"{prefix}tuning_profiles_{tag}_SESSION_MEANS_TOP5_CELLS.png",dpi=300,bbox_inches="tight")
        plt.close(fig)


def combined_top50_lifetime_sparseness_raster(cell_df: pd.DataFrame, mode: str, outdir: Path, title: str,
                                              prefix: str = "") -> None:
    cols, values = _response_columns(cell_df, mode)
    if not cols: return
    for responsive_only, tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df=cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
        fig,axes=plt.subplots(1,2,figsize=(14,7),constrained_layout=True)
        im=None
        for ax,cls in zip(axes,("green","yellow")):
            sub=df[(df.cell_class==cls)&np.isfinite(df.tuning_lifetime_sparseness)].copy()
            sub=sub.sort_values("tuning_lifetime_sparseness",ascending=False).head(N_COMBINED_RASTER_CELLS_PER_CLASS)
            mat=sub[cols].to_numpy(float)
            if len(mat)==0:
                ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center"); ax.set_title(cls.title()); continue
            norm=np.nanmax(np.abs(mat),axis=1); norm[norm<=0]=np.nan
            matn=mat/norm[:,None]
            edges = _log2_bin_edges(values, mode)
            if edges is not None:
                yedges = np.arange(len(matn)+1, dtype=float)
                im = ax.pcolormesh(edges, yedges, matn, cmap="coolwarm", vmin=-1, vmax=1, shading="flat")
                ax.set_ylim(len(matn), 0)
                _apply_log2_tuning_axis(ax, values, mode)
            else:
                im=ax.imshow(matn,aspect="auto",interpolation="nearest",cmap="coolwarm",vmin=-1,vmax=1)
                labels=_log2_tick_labels(values, mode)
                ax.set_xticks(np.arange(len(values)),labels,rotation=45,ha="right")
            ax.set_title(f"{cls.title()} top {len(sub)} by lifetime sparseness")
            ax.set_ylabel("Cells ranked by sparseness")
            ax.set_xlabel(_xlabel(mode))
            ax.tick_params(axis="x", labelrotation=45)
            for tick in ax.get_xticklabels(): tick.set_ha("right")
        if im is not None: fig.colorbar(im,ax=axes,label="Response / max |response| per cell")
        fig.suptitle(f"{title}\nTop-selectivity tuning rasters — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}top50_lifetime_sparseness_rasters_{tag}.png",dpi=300,bbox_inches="tight")
        plt.close(fig)


def condition_profile_figures(condition_df: pd.DataFrame, mode: str, outdir: Path, title: str, prefix: str="") -> None:
    for fdr,tag in ((False,"all_cells"),(True,"FDR_responsive_only")):
        df=condition_df[condition_df.stim_responsive_fdr] if fdr else condition_df
        if len(df)==0: continue
        values=np.sort(df.tuning_value_Hz.unique()); intensities=np.sort(df.intensity_dB.unique())
        x=_xplot(values,mode)
        fig,axes=plt.subplots(1,max(1,len(intensities)),figsize=(6*max(1,len(intensities)),5.6),squeeze=False,constrained_layout=True)
        for ax,intensity in zip(axes.ravel(),intensities):
            display=[]
            for cls,color in (("green",GREEN_COLOR),("yellow",YELLOW_COLOR)):
                session_profiles=[]
                for session_key,sdf in df[(df.cell_class==cls)&np.isclose(df.intensity_dB,intensity)].groupby("session_key",sort=True):
                    means=[]; sds=[]
                    for value in values:
                        vals=finite_values(sdf[np.isclose(sdf.tuning_value_Hz,value)].condition_response)
                        m,sd,_,_=mean_sd_sem(vals); means.append(m); sds.append(sd)
                    means=np.asarray(means,float); sds=np.asarray(sds,float)
                    if not np.any(np.isfinite(means)): continue
                    session_profiles.append(means)
                    ax.plot(x,means,color=color,alpha=.24,lw=1.0,marker="o",ms=2.5,zorder=2)
                    if np.any(np.isfinite(sds)):
                        ax.fill_between(x,means-sds,means+sds,color=color,alpha=.035,zorder=1)
                    display.extend(finite_values(means).tolist())
                    display.extend(finite_values(means-sds).tolist()); display.extend(finite_values(means+sds).tolist())
                if session_profiles:
                    smat=np.vstack(session_profiles)
                    overall=np.nanmean(smat,axis=0)
                    sem=np.asarray([stats.sem(smat[:,i],nan_policy="omit") if np.sum(np.isfinite(smat[:,i]))>1 else np.nan for i in range(len(values))])
                    ax.errorbar(x,overall,yerr=sem,fmt="o-",capsize=4,color=color,lw=2.7,elinewidth=1.9,ms=5,
                                label=f"{cls.title()} overall; {len(session_profiles)} sessions",zorder=5)
            ax.axhline(0,color="black",ls=":",lw=1); ax.set_title(f"{intensity:g} dB SPL\nlight=session mean ± SD; dark=overall mean ± SEM")
            ax.set_xlabel(_xlabel(mode)); ax.set_ylabel("Mean response (dF/F)")
            _apply_log2_tuning_axis(ax, values, mode)
            ax.legend(frameon=False,fontsize=8); ax.grid(alpha=.2); ax.spines[["top","right"]].set_visible(False)
            apply_robust_y_limits(ax,display,reference_values=(0,))
        fig.suptitle(f"{title}\nIntensity-resolved tuning — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}intensity_resolved_tuning_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)

        # Condition-selectivity contrast: session means +/- within-session SD
        # are shown lightly; overall mean +/- SEM across session means is dark.
        ordered=(df[["condition_name","tuning_value_Hz","intensity_dB"]].drop_duplicates().sort_values(["intensity_dB","tuning_value_Hz"]))
        names=ordered.condition_name.tolist(); xpos=np.arange(len(names),dtype=float)
        fig,axes=plt.subplots(2,1,figsize=(max(12,.80*len(names)),10),constrained_layout=True)
        overall_by={}; sem_by={}; session_maps={}
        for cls,color,shift in (("green",GREEN_COLOR,-.10),("yellow",YELLOW_COLOR,.10)):
            session_map={}
            for session_key,sdf in df[df.cell_class==cls].groupby("session_key",sort=True):
                means=[]; sds=[]
                for name in names:
                    vals=finite_values(sdf[sdf.condition_name==name].condition_selectivity_contrast)
                    m,sd,_,_=mean_sd_sem(vals); means.append(m); sds.append(sd)
                means=np.asarray(means,float); sds=np.asarray(sds,float)
                session_map[str(session_key)]=means
                axes[0].errorbar(xpos+shift,means,yerr=sds,fmt="o",ms=2.8,elinewidth=.55,capsize=1.5,
                                 color=color,alpha=.18,zorder=1)
            session_maps[cls]=session_map
            if session_map:
                smat=np.vstack(list(session_map.values()))
                overall=np.nanmean(smat,axis=0)
                sem=np.asarray([stats.sem(smat[:,i],nan_policy="omit") if np.sum(np.isfinite(smat[:,i]))>1 else np.nan for i in range(len(names))])
            else:
                overall=np.full(len(names),np.nan); sem=np.full(len(names),np.nan)
            overall_by[cls]=overall; sem_by[cls]=sem
            axes[0].errorbar(xpos+shift,overall,yerr=sem,fmt="o",ms=6.5,elinewidth=2.0,capsize=4,
                             color=color,label=cls.title(),zorder=5)
        axes[0].axhline(0,color="black",ls=":",lw=1); axes[0].set_xticks(xpos,names,rotation=45,ha="right")
        axes[0].set_ylabel("Condition selectivity contrast (dF/F)"); axes[0].legend(frameon=False)
        axes[0].set_title("light=session mean ± SD; dark=overall mean ± SEM")
        # Paired session yellow-green differences where both classes exist.
        pair_keys=sorted(set(session_maps.get("green",{})) & set(session_maps.get("yellow",{})))
        pair_diffs=[]
        for key in pair_keys:
            d=session_maps["yellow"][key]-session_maps["green"][key]
            pair_diffs.append(d); axes[1].plot(xpos,d,color="0.55",alpha=.23,lw=.8,marker="o",ms=2)
        if pair_diffs:
            dmat=np.vstack(pair_diffs); dm=np.nanmean(dmat,axis=0)
            dse=np.asarray([stats.sem(dmat[:,i],nan_policy="omit") if np.sum(np.isfinite(dmat[:,i]))>1 else np.nan for i in range(len(names))])
            axes[1].errorbar(xpos,dm,yerr=dse,fmt="o-",color="black",lw=2.2,elinewidth=1.8,capsize=4,label="Overall paired difference")
        axes[1].axhline(0,color="black",ls="--",lw=1); axes[1].set_xticks(xpos,names,rotation=45,ha="right")
        axes[1].set_ylabel("Yellow - green session mean contrast"); axes[1].legend(frameon=False)
        fig.suptitle(f"{title}\nCondition selectivity (condition - all others) — {tag.replace('_',' ')}")
        fig.savefig(outdir/f"{prefix}condition_selectivity_contrast_{tag}_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


# =============================================================================
# COMBINED AREA-LEVEL STATISTICS / FIGURES
# =============================================================================

def combined_statistics(cell_df: pd.DataFrame, class_summary_df: pd.DataFrame) -> dict[str, Any]:
    metrics=["stim_response_mean","best_tuning_response","peak_absolute_response","tuning_modulation_depth",
             "tuning_selectivity_contrast","tuning_selectivity_index","tuning_lifetime_sparseness",
             "tuning_gini_coefficient","tuning_fano_factor","tuning_fwhm"]
    out: dict[str, Any] = {
        "primary_tuning_selectivity_metric": "tuning_lifetime_sparseness",
        "selectivity_metric_note": "Gini, Fano, and FWHM are reported as complementary measures; Fano is scale-dependent.",
        "pooled_cell_exploratory":{}, "paired_session_primary":{}
    }
    for metric in metrics:
        out["pooled_cell_exploratory"][metric]=safe_mannwhitney(
            cell_df.loc[cell_df.cell_class=="green",metric], cell_df.loc[cell_df.cell_class=="yellow",metric]
        )
        col=f"mean_{metric}"
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
        ("mean_best_tuning_response","Mean best tuning response"),
        ("mean_peak_absolute_response","Mean peak absolute response"),
        ("mean_tuning_modulation_depth","Mean tuning modulation depth"),
        ("mean_tuning_lifetime_sparseness","Mean lifetime sparseness"),
        ("mean_tuning_gini_coefficient","Mean Gini coefficient"),
        ("mean_tuning_fano_factor","Mean tuning-profile Fano factor"),
        ("mean_tuning_fwhm","Mean FWHM bandwidth"),
        ("pct_stim_responsive_fdr","FDR responsive cells (%)"),
    ]
    fig,axes=plt.subplots(2,4,figsize=(20,10),constrained_layout=True); axes=axes.ravel()
    for ax,(metric,label) in zip(axes,metrics):
        wide=class_summary_df.pivot_table(index="session_key",columns="cell_class",values=metric,aggfunc="first")
        if "green" not in wide or "yellow" not in wide:
            ax.text(.5,.5,"Insufficient paired sessions",transform=ax.transAxes,ha="center"); continue
        valid=wide[["green","yellow"]].dropna()
        for _,r in valid.iterrows(): ax.plot([0,1],[r.green,r.yellow],color="0.7",lw=1,zorder=1)
        ax.scatter(np.zeros(len(valid)),valid.green,color=GREEN_COLOR,zorder=2)
        ax.scatter(np.ones(len(valid)),valid.yellow,color=YELLOW_COLOR,zorder=2)
        res=safe_paired_wilcoxon(valid.green,valid.yellow)
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label)
        ax.set_title(f"{label}\npaired Wilcoxon p={res['p']:.3g}" if res['p'] is not None else label)
        apply_robust_y_limits(ax,np.r_[valid.green,valid.yellow])
    fig.suptitle(f"{title}\nSession-level GREEN/YELLOW comparisons")
    fig.savefig(output_dir/"combined_session_level_green_yellow_comparisons.png",dpi=300,bbox_inches="tight"); plt.close(fig)

    # New convention: show each session mean +/- within-session SD lightly, plus
    # overall mean +/- SEM across session means in dark/thick form.
    fig,axes=plt.subplots(2,4,figsize=(20,10),constrained_layout=True); axes=axes.ravel()
    colors={"green":GREEN_COLOR,"yellow":YELLOW_COLOR}
    for ax,(metric,label) in zip(axes,metrics):
        base_metric = metric[len("mean_"):] if metric.startswith("mean_") else None
        for xpos,cls in enumerate(("green","yellow")):
            sdf=class_summary_df[class_summary_df.cell_class==cls].copy()
            session_means=finite_values(sdf[metric])
            if base_metric is not None and f"std_{base_metric}" in sdf:
                session_sds=pd.to_numeric(sdf[f"std_{base_metric}"],errors="coerce").to_numpy(float)
                mvals=pd.to_numeric(sdf[metric],errors="coerce").to_numpy(float)
                valid=np.isfinite(mvals)
                offsets=np.linspace(-.05,.05,max(1,np.sum(valid)))
                kk=0
                for m,sd in zip(mvals,session_sds):
                    if not np.isfinite(m): continue
                    ax.errorbar(xpos+offsets[min(kk,len(offsets)-1)],m,yerr=sd if np.isfinite(sd) else None,
                                fmt="o",ms=3.5,elinewidth=.75,capsize=2,color=colors[cls],alpha=.28,zorder=2)
                    kk+=1
            else:
                offsets=np.linspace(-.05,.05,max(1,len(session_means)))
                ax.scatter(xpos+offsets[:len(session_means)],session_means,s=17,color=colors[cls],alpha=.28,zorder=2)
            m,_,se,n=mean_sd_sem(session_means)
            if np.isfinite(m):
                ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,elinewidth=2.5,capsize=6,
                            color=colors[cls],zorder=5)
                txt=f"{m:.3f}±{se:.3f}\nn sess={n}" if np.isfinite(se) else f"{m:.3f}\nn sess={n}"
                ax.annotate(txt,(xpos,m),xytext=(0,12 if xpos==0 else -32),textcoords="offset points",ha="center",fontsize=7,color=colors[cls])
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(label)
        ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
    fig.suptitle(f"{title}\nSession hierarchy: light=session mean ± SD; dark=overall mean ± SEM")
    fig.savefig(output_dir/"combined_session_level_green_yellow_comparisons_MEAN_SEM_ONLY.png",dpi=300,bbox_inches="tight"); plt.close(fig)


def write_combined_report(path: Path, mode: str, cell_df: pd.DataFrame, class_summary_df: pd.DataFrame, stats_dict: dict[str, Any]) -> None:
    lines=[]
    lines.append(f"AM_TUNING AREA ANALYSIS — {mode}\n")
    lines.append(f"Cells: {len(cell_df)} | sessions: {cell_df.session_key.nunique()}\n")
    lines.append(f"Green cells: {sum(cell_df.cell_class=='green')} | Yellow cells: {sum(cell_df.cell_class=='yellow')}\n")
    lines.append("\nSELECTIVITY METRICS\n")
    lines.append("Primary selectivity: lifetime sparseness across |mean baseline-corrected tuning response|.\n")
    lines.append("Comparison measures: Gini coefficient, Fano factor=variance/mean across |response| (scale-dependent), and FWHM.\n")
    lines.append("FWHM is reported in octaves for tuningFreq and Hz for tuningAM; unbracketed half-max crossings are NaN.\n")
    lines.append("All numeric frequency- and AM-rate x-axes use explicit base-2 coordinates x=log2(value); every doubling is equally spaced.\n")
    lines.append("PRIMARY responsiveness is BH-FDR separately across cells at each tuning value; stim_responsive_fdr is the union across values.\n")
    lines.append("Whole-session-median and 60-s prestimulus-median dF/F metrics are exported as sensitivity analyses without redefining responsiveness.\n")
    lines.append("Per-session trial_response_archive_v9.npz files support downstream trial-repetition subsampling.\n")
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

    archive_index_rows = []
    for r in results:
        rmeta = r["meta"]
        archive_index_rows.append({
            "subject": str(rmeta.get("subject", subject)),
            "date": str(rmeta.get("date")),
            "session": str(rmeta.get("session")),
            "session_key": f"{rmeta.get('date')}_{rmeta.get('session')}",
            "brainArea": rmeta.get("brainArea"),
            "canonicalArea": rmeta.get("canonicalArea"),
            "depth": rmeta.get("depth"),
            "tuning_mode": mode,
            "n_cells": int(len(r["cell_df"])),
            "n_aligned_trials": int(r.get("n_aligned_trials", 0)),
            "n_analysis_trials": int(r.get("n_analysis_trials", 0)),
            "trial_response_archive_path": str(r["trial_response_archive_path"]),
            "trial_response_archive_schema_version": 1,
        })
    pd.DataFrame(archive_index_rows).to_csv(
        combined_dir/"combined_trial_response_archive_index.csv", index=False
    )

    title=f"{subject} | {area} | {mode} | {', '.join(dates)} | {cell_df.session_key.nunique()} sessions"
    sound_responsiveness_figure(cell_df,combined_dir/"combined_stim_responsive_cells_green_yellow.png",title)
    cols,values=_response_columns(cell_df,mode)
    tuning_curve_figures(cell_df,mode,values,combined_dir,title,prefix="combined_")
    tuning_raster_figures(cell_df,mode,values,combined_dir,title,prefix="combined_")
    green_yellow_metric_figures(cell_df,combined_dir,title,prefix="combined_")
    condition_profile_figures(cond_df,mode,combined_dir,title,prefix="combined_")
    standalone_selectivity_figures(cell_df,mode,combined_dir,title,combined=True,prefix="combined_")
    tuning_profile_session_hierarchy_figure(cell_df,mode,combined_dir,title,prefix="combined_")
    tuning_profiles_sessions_top_cells(cell_df,mode,combined_dir,title,prefix="combined_")
    combined_top50_lifetime_sparseness_raster(cell_df,mode,combined_dir,title,prefix="combined_")
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
    print("AM_TUNING AREA ANALYSIS v9")
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
        session_dir.mkdir(parents=True, exist_ok=True)
        stale_error = session_dir / "ERROR.json"
        if stale_error.exists():
            stale_error.unlink()
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
            "raster_min_abs_response":RASTER_MIN_ABS_RESPONSE,
            "selectivity_profile":"absolute magnitude of mean baseline-corrected tuning response",
            "frequency_fwhm_units":"octaves","am_fwhm_units":"Hz",
            "fano_definition":"sample variance / mean across absolute tuning-response magnitudes",
            "fdr_alpha":FDR_ALPHA,
            "n_permutations":args.n_permutations,"seed":args.seed,
            "source_script_version":"v9",
            "primary_responsiveness":"BH-FDR separately across cells within each tuning value; union across values",
            "alternate_dff_session_median":"whole-session median F0 per cell",
            "alternate_dff_60s_prestim":"prestimulus-only median F0 from stimuli within +/-30 s",
            "alternate_dff_recomputes_responsiveness":False,
            "trial_response_archive":"session_outputs/<date>_<session>/<subject>_<date>_<session>_p<plane>_trial_response_archive_v9.npz",
            "tuning_axis_geometry":"explicit x=log2(displayed frequency or AM rate); equal doublings have equal spacing",
            "alignment_max_internal_skip_per_step":MAX_INTERNAL_SKIP_PER_STEP,
            "alignment_max_total_internal_skips":MAX_TOTAL_INTERNAL_SKIPS,
            "alignment_max_leading_skip":MAX_LEADING_SKIP,
            "alignment_leading_validation_intervals":LEADING_VALIDATION_INTERVALS,
            "alignment_skip_penalty_s":ALIGN_SKIP_PENALTY_S,
            "alignment_min_coverage":MIN_ALIGNMENT_COVERAGE,
            "alignment_max_mean_abs_error_s":MAX_MEAN_ABS_ERROR_S,
            "alignment_max_abs_error_s":MAX_ABS_ERROR_S,
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
