#!/usr/bin/env python3
"""
Batch analysis of sound_tuning two-photon sessions from one auditory cortical area.

This script is the batch/area-level version of:
    twophoton_sound_tuning_EV_20260812.ipynb

Version 8 scope
---------------
* sound_tuning sessions only.
* Canonical brain areas:
      A1  <- any info2p brainArea containing "A1"
      AAF <- any info2p brainArea containing "AAF"
      A2  <- any info2p brainArea containing "A2" or "AuV"
* The lowFreq/highFreq suffix and depth are retained as metadata but are NOT
  used to filter or stratify yet.
* GREEN  = functional GCaMP ROI without sufficient anatomical tdTomato overlap.
* YELLOW = functional GCaMP ROI with sufficient anatomical tdTomato overlap.
* RED anatomical ROIs are Cellpose objects segmented from meanImg_chan2.
* Cellpose/overlap settings match the finalized notebook:
      IoU cutoff            = 0.15
      Cellpose cellprob     = -0.5
      Cellpose flow         = 0.5
      diameter              = median equivalent diameter of functional ROIs
* No functional ROI is excluded based on the legacy Suite2p channel-2 score.
  Every analyzed functional ROI is classified GREEN or YELLOW solely from the
  finalized Cellpose anatomical-overlap rule.
* Summary plots use conservative robust y-axis limits when one or two extreme
  values would otherwise compress the mean +/- SEM differences. Those points
  remain in all calculations/statistics and are only clipped visually.
* Imaging/behavior event alignment assumes acquisition starts before sound presentation,
  so any small excess of imaging-detected sound triggers is treated as trailing events.
  The first N imaging events are aligned to the N behavioral trials and timing is validated.
* Outputs are always saved under jaratoolbox.settings.TEMP_OUTPUT_PATH.
* Figure-output expansion in v8:
      - restores the notebook reliable sound-responsive/non-responsive figure,
        per session and pooled across the selected area;
      - writes FDR sound-responsive-only versions of the main response figures;
      - writes session-aware summary figures: individual-session mean +/- SD
        in light/thin form plus overall mean +/- SEM across sessions in
        dark/thick form;
      - replaces FI/FO response ratios with signed selectivity indices and adds
        AM-rate lifetime-sparseness selectivity summaries;
      - adds per-session top-10 GREEN/YELLOW selective-cell example figures and
        combined top-50 FI/FO-selectivity rasters.

Example
-------
python sound_tuning_area_analysis_v8.py imag039 \
    --area A1 \
    --dates 20260729 20260730

A discovery-only run can be made with:
python sound_tuning_area_analysis_v8.py imag039 \
    --area A1 \
    --dates 20260729 20260730 \
    --dry-run

Output root
-----------
<TEMP_OUTPUT_PATH>/evan/sound_tuning_area_analysis/<subject>/<area>/<date_tag>/
    session_selection.csv
    run_manifest.json
    session_outputs/<date>_<session>/...
    combined/...

Statistics
----------
The notebook's pooled-cell tests are retained as descriptive/exploratory
comparisons. Across-session inference is additionally reported using one value
per session/population (paired GREEN vs YELLOW summaries), so pooled cells are
not silently treated as independent biological replicates.
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

from jaratoolbox import settings
from jaratoolbox import twophotonanalysis
from suite2p.detection.chan2detect import cellpose_overlap


# =============================================================================
# FINAL NOTEBOOK PARAMETERS
# =============================================================================

PARADIGM = "sound_tuning"

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
SELECTIVITY_DENOMINATOR_ABS_THRESHOLD = 1e-6
SELECTIVITY_DENOMINATOR_RELATIVE_THRESHOLD = 0.05
N_EXAMPLE_CELLS_PER_CLASS = 10
N_COMBINED_RASTER_CELLS_PER_CLASS = 50
N_AM_EXAMPLE_CELLS_PER_SESSION_CLASS = 5

FDR_ALPHA = 0.05
N_PERMUTATIONS_DEFAULT = 20000
RANDOM_SEED_DEFAULT = 20260812

GREEN_COLOR = "forestgreen"
YELLOW_COLOR = "goldenrod"
DISPLAY_GREEN_COLOR = "lime"
DISPLAY_YELLOW_COLOR = "yellow"
ANATOMICAL_RED_COLOR = "red"
FADE_IN_COLOR = "tab:blue"
FADE_OUT_COLOR = "tab:orange"
BEST_AM_COLOR = "tab:purple"

FUNCTIONAL_OUTLINE_LW = 0.25
RED_OUTLINE_LW = 0.45


# =============================================================================
# COMMAND LINE
# =============================================================================

def normalize_area_argument(value: str) -> str:
    value_upper = str(value).strip().upper()
    if value_upper == "AUV":
        return "A2"
    if value_upper in {"A1", "AAF", "A2"}:
        return value_upper
    raise argparse.ArgumentTypeError("Area must be A1, AAF, A2, or AuV.")


def normalize_dates(values: list[str]) -> list[str]:
    dates: list[str] = []
    for value in values:
        for piece in str(value).replace(",", " ").split():
            piece = piece.strip()
            if not piece:
                continue
            if len(piece) != 8 or not piece.isdigit():
                raise argparse.ArgumentTypeError(
                    f"Invalid date '{piece}'. Dates must be YYYYMMDD."
                )
            dates.append(piece)
    if not dates:
        raise argparse.ArgumentTypeError("At least one date is required.")
    return sorted(set(dates))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("subject", help="Subject ID, e.g. imag039.")
    parser.add_argument(
        "--area",
        required=True,
        type=normalize_area_argument,
        help="Canonical area: A1, AAF, A2 (AuV is accepted as A2).",
    )
    parser.add_argument(
        "--dates",
        required=True,
        nargs="+",
        help="Dates to include (YYYYMMDD), separated by spaces or commas.",
    )
    parser.add_argument(
        "--plane",
        type=int,
        default=PLANE_DEFAULT,
        help=f"Suite2p plane number. Default: {PLANE_DEFAULT}.",
    )
    parser.add_argument(
        "--n-permutations",
        type=int,
        default=N_PERMUTATIONS_DEFAULT,
        help=(
            "Monte-Carlo sign-flip permutations per response test. "
            f"Default: {N_PERMUTATIONS_DEFAULT}."
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=RANDOM_SEED_DEFAULT,
        help=f"Random seed. Default: {RANDOM_SEED_DEFAULT}.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Find and print matching info2p sessions without loading imaging data.",
    )
    return parser.parse_args()


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
        v = float(value)
        return None if not np.isfinite(v) else v
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, float):
        return None if not np.isfinite(value) else value
    return value


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(obj), indent=2))


def safe_divide(num: float, den: float) -> float:
    return float(num / den) if den else np.nan


def finite_values(values: np.ndarray | pd.Series) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    return values[np.isfinite(values)]


def mean_sem(values: np.ndarray | pd.Series) -> tuple[float, float]:
    values = finite_values(values)
    if len(values) == 0:
        return np.nan, np.nan
    mean_value = float(np.mean(values))
    sem_value = (
        float(np.std(values, ddof=1) / np.sqrt(len(values)))
        if len(values) > 1
        else np.nan
    )
    return mean_value, sem_value


def mean_sd_sem(values: np.ndarray | pd.Series) -> tuple[float, float, float, int]:
    """Return mean, SD, SEM, and finite n."""
    vals = finite_values(values)
    n = len(vals)
    if n == 0:
        return np.nan, np.nan, np.nan, 0
    mean_value = float(np.mean(vals))
    if n > 1:
        sd_value = float(np.std(vals, ddof=1))
        sem_value = float(sd_value / np.sqrt(n))
    else:
        sd_value = np.nan
        sem_value = np.nan
    return mean_value, sd_value, sem_value, n


def format_mean_sem(mean_value: float, sem_value: float, n: int, digits: int = 4) -> str:
    if not np.isfinite(mean_value):
        return "n/a"
    if np.isfinite(sem_value):
        return f"{mean_value:.{digits}f} ± {sem_value:.{digits}f} SEM\nn={n}"
    return f"{mean_value:.{digits}f}\nSEM n/a, n={n}"


def apply_mean_error_y_limits(
    ax,
    means,
    errors=None,
    reference_values=None,
    pad_fraction: float = 0.22,
) -> None:
    """Optimize a mean-only panel from means +/- plotted errors only.

    Raw-cell outliers are intentionally irrelevant here because they are not
    displayed.  This makes differences between summary estimates visually
    readable while still showing every plotted mean and error bar.
    """
    means_arr = np.asarray(means, dtype=float).ravel()
    if errors is None:
        errors_arr = np.zeros_like(means_arr)
    else:
        errors_arr = np.asarray(errors, dtype=float).ravel()
        if errors_arr.size != means_arr.size:
            errors_arr = np.resize(errors_arr, means_arr.shape)

    finite_mean = np.isfinite(means_arr)
    if not np.any(finite_mean):
        return

    lows = means_arr[finite_mean].copy()
    highs = means_arr[finite_mean].copy()
    finite_err = np.isfinite(errors_arr[finite_mean])
    errs = np.where(finite_err, np.abs(errors_arr[finite_mean]), 0.0)
    lows -= errs
    highs += errs

    vals = np.concatenate([lows, highs])
    if reference_values is not None:
        refs = finite_values(reference_values)
        if len(refs):
            vals = np.concatenate([vals, refs])

    ymin = float(np.min(vals))
    ymax = float(np.max(vals))
    span = ymax - ymin
    if span <= 0:
        pad = max(abs(ymin) * 0.15, 1e-4)
    else:
        pad = max(pad_fraction * span, 1e-5)
    ax.set_ylim(ymin - pad, ymax + pad)


def annotate_mean_sem_point(
    ax,
    x: float,
    mean_value: float,
    sem_value: float,
    n: int,
    *,
    color: str = "black",
    digits: int = 4,
    x_offset_points: float = 0.0,
    y_offset_points: float = 7.0,
    fontsize: float = 7.0,
) -> None:
    if not np.isfinite(mean_value):
        return
    anchor_y = mean_value + (sem_value if np.isfinite(sem_value) else 0.0)
    ax.annotate(
        format_mean_sem(mean_value, sem_value, n, digits=digits),
        xy=(x, anchor_y),
        xytext=(x_offset_points, y_offset_points),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=fontsize,
        color=color,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.78, pad=1.2),
        zorder=10,
    )


def fdr_sound_responsive_subset(cell_df: pd.DataFrame) -> pd.DataFrame:
    if "sound_responsive_fdr" not in cell_df.columns:
        return cell_df.iloc[0:0].copy()
    return cell_df[
        cell_df["cell_class"].isin(["green", "yellow"])
        & cell_df["sound_responsive_fdr"].astype(bool)
    ].copy()


def subset_session_class_summary(cell_df: pd.DataFrame) -> pd.DataFrame:
    """Build session x class summaries for subset statistics/plots."""
    rows = []
    classified = cell_df[cell_df["cell_class"].isin(["green", "yellow"])].copy()
    for (session_key, class_name), df in classified.groupby(["session_key", "cell_class"], sort=False):
        n = len(df)
        fi = finite_values(df["fade_in_response"]) if "fade_in_response" in df else np.array([])
        fi_fo = finite_values(df["fade_in_vs_fade_out_selectivity"]) if "fade_in_vs_fade_out_selectivity" in df else np.array([])
        fi_am = finite_values(df["fade_in_vs_best_am_selectivity"]) if "fade_in_vs_best_am_selectivity" in df else np.array([])
        am_sp = finite_values(df["am_rate_lifetime_sparseness"]) if "am_rate_lifetime_sparseness" in df else np.array([])
        row = {
            "session_key": session_key,
            "cell_class": class_name,
            "n_cells": n,
            "n_sound_responsive_fdr": int(np.sum(df["sound_responsive_fdr"].astype(bool))) if n else 0,
            "pct_sound_responsive_fdr": 100.0 * float(np.mean(df["sound_responsive_fdr"].astype(bool))) if n else np.nan,
            "n_sound_excited_fdr": int(np.sum(df["sound_excited_fdr"].astype(bool))) if n else 0,
            "pct_sound_excited_fdr": 100.0 * float(np.mean(df["sound_excited_fdr"].astype(bool))) if n else np.nan,
            "n_sound_suppressed_fdr": int(np.sum(df["sound_suppressed_fdr"].astype(bool))) if n else 0,
            "pct_sound_suppressed_fdr": 100.0 * float(np.mean(df["sound_suppressed_fdr"].astype(bool))) if n else np.nan,
            "mean_fade_in_response": float(np.mean(fi)) if len(fi) else np.nan,
            "std_fade_in_response": float(np.std(fi, ddof=1)) if len(fi) > 1 else np.nan,
            "mean_fade_in_vs_fade_out_selectivity": float(np.mean(fi_fo)) if len(fi_fo) else np.nan,
            "std_fade_in_vs_fade_out_selectivity": float(np.std(fi_fo, ddof=1)) if len(fi_fo) > 1 else np.nan,
            "mean_fade_in_vs_best_am_selectivity": float(np.mean(fi_am)) if len(fi_am) else np.nan,
            "std_fade_in_vs_best_am_selectivity": float(np.std(fi_am, ddof=1)) if len(fi_am) > 1 else np.nan,
            "mean_am_rate_lifetime_sparseness": float(np.mean(am_sp)) if len(am_sp) else np.nan,
            "std_am_rate_lifetime_sparseness": float(np.std(am_sp, ddof=1)) if len(am_sp) > 1 else np.nan,
        }
        for col in ["subject", "date", "session", "brainArea", "canonicalArea", "depth"]:
            if col in df.columns and len(df):
                row[col] = df.iloc[0][col]
        rows.append(row)
    return pd.DataFrame(rows)


def apply_robust_y_limits(
    ax,
    datasets,
    important_values=None,
    reference_values=None,
    max_clip_per_tail: int = 2,
    fence_scale: float = 3.0,
    annotate: bool = True,
) -> None:
    """Set a display-only y-range that can ignore a few extreme points.

    The underlying data are never modified.  A tail is clipped only when values
    lie beyond a conservative Tukey-style fence (Q1/Q3 +/- fence_scale*IQR).
    At most ``max_clip_per_tail`` extreme points are allowed to determine the
    clipped portion on either side.  Mean +/- SEM values and requested
    reference lines are always kept visible.

    This is intended for summary plots where one or two extreme cells can make
    the central green/yellow mean +/- SEM comparison unreadable.
    """
    arrays = []
    for values in datasets:
        vals = finite_values(values)
        if len(vals):
            arrays.append(vals)
    if not arrays:
        return

    values = np.sort(np.concatenate(arrays))
    if len(values) < 4:
        return

    q1, q3 = np.percentile(values, [25, 75])
    iqr = float(q3 - q1)

    if np.isfinite(iqr) and iqr > 0:
        lower_fence = q1 - fence_scale * iqr
        upper_fence = q3 + fence_scale * iqr
    else:
        median = float(np.median(values))
        mad = float(np.median(np.abs(values - median)))
        if not np.isfinite(mad) or mad <= 0:
            return
        # 1.4826*MAD approximates sigma for a Gaussian; 4 sigma is conservative.
        spread = 4.0 * 1.4826 * mad
        lower_fence = median - spread
        upper_fence = median + spread

    n_low_extreme = int(np.sum(values < lower_fence))
    n_high_extreme = int(np.sum(values > upper_fence))

    n_clip_low = min(max_clip_per_tail, n_low_extreme)
    n_clip_high = min(max_clip_per_tail, n_high_extreme)

    display_low = float(values[n_clip_low]) if n_clip_low else float(values[0])
    display_high = (
        float(values[-1 - n_clip_high]) if n_clip_high else float(values[-1])
    )

    keep_values = []
    if important_values is not None:
        keep_values.extend(finite_values(important_values).tolist())
    if reference_values is not None:
        keep_values.extend(finite_values(reference_values).tolist())

    if keep_values:
        display_low = min(display_low, min(keep_values))
        display_high = max(display_high, max(keep_values))

    if not np.isfinite(display_low) or not np.isfinite(display_high):
        return

    span = display_high - display_low
    if span <= 0:
        pad = max(abs(display_low) * 0.08, 1e-6)
    else:
        pad = 0.08 * span

    ymin = display_low - pad
    ymax = display_high + pad

    # Count points that will actually fall outside the final visible range.
    n_below = int(np.sum(values < ymin))
    n_above = int(np.sum(values > ymax))
    if n_below == 0 and n_above == 0:
        return

    ax.set_ylim(ymin, ymax)

    if annotate:
        clipped_parts = []
        if n_below:
            clipped_parts.append(f"{n_below} below")
        if n_above:
            clipped_parts.append(f"{n_above} above")
        ax.text(
            0.98,
            0.02,
            "display y-limit clips " + ", ".join(clipped_parts),
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=7,
            color="0.35",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=1.5),
        )


def holm_correct(p_values: list[float]) -> np.ndarray:
    p_values_array = np.asarray(p_values, dtype=float)
    corrected = np.full_like(p_values_array, np.nan)
    valid_indices = np.flatnonzero(np.isfinite(p_values_array))
    if len(valid_indices) == 0:
        return corrected
    valid_p = p_values_array[valid_indices]
    order = np.argsort(valid_p)
    sorted_p = valid_p[order]
    m = len(sorted_p)
    adjusted_sorted = np.empty(m, dtype=float)
    running_max = 0.0
    for rank in range(m):
        adjusted_value = (m - rank) * sorted_p[rank]
        running_max = max(running_max, adjusted_value)
        adjusted_sorted[rank] = min(running_max, 1.0)
    restored = np.empty(m, dtype=float)
    restored[order] = adjusted_sorted
    corrected[valid_indices] = restored
    return corrected


def bh_fdr(p_values: np.ndarray, valid_mask: np.ndarray) -> np.ndarray:
    p_values = np.asarray(p_values, dtype=float)
    valid_mask = np.asarray(valid_mask, dtype=bool)
    q_values = np.full_like(p_values, np.nan, dtype=float)
    finite_indices = np.flatnonzero(np.isfinite(p_values) & valid_mask)
    if len(finite_indices) == 0:
        return q_values
    finite_p = p_values[finite_indices]
    order = np.argsort(finite_p)
    ranked_p = finite_p[order]
    n_tests = len(ranked_p)
    adjusted = ranked_p * n_tests / np.arange(1, n_tests + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    adjusted = np.clip(adjusted, 0, 1)
    restored = np.empty(n_tests, dtype=float)
    restored[order] = adjusted
    q_values[finite_indices] = restored
    return q_values




def response_selectivity_index(response_a: np.ndarray, response_b: np.ndarray) -> np.ndarray:
    """Signed (A-B)/(A+B) selectivity with a conservative cancellation guard.

    The guard rejects cases where A+B is both very small in absolute terms and
    small relative to |A|+|B|. This prevents nearly cancelling signed dF/F
    responses from generating numerically enormous selectivity values.
    """
    a = np.asarray(response_a, dtype=float)
    b = np.asarray(response_b, dtype=float)
    a, b = np.broadcast_arrays(a, b)
    out = np.full(a.shape, np.nan, dtype=float)
    denom = a + b
    scale = np.abs(a) + np.abs(b)
    threshold = np.maximum(
        SELECTIVITY_DENOMINATOR_ABS_THRESHOLD,
        SELECTIVITY_DENOMINATOR_RELATIVE_THRESHOLD * scale,
    )
    valid = np.isfinite(a) & np.isfinite(b) & np.isfinite(denom) & (np.abs(denom) > threshold)
    out[valid] = (a[valid] - b[valid]) / denom[valid]
    return out


def lifetime_sparseness(response_matrix: np.ndarray) -> np.ndarray:
    """Lifetime sparseness across conditions/rates for each row.

    Uses the standard Treves-Rolls style expression on the signed,
    baseline-subtracted dF/F response profile supplied by the analysis. At
    least two finite AM-rate responses are required.
    """
    matrix = np.asarray(response_matrix, dtype=float)
    if matrix.ndim == 1:
        matrix = matrix[None, :]
    out = np.full(matrix.shape[0], np.nan, dtype=float)
    for row_idx, row in enumerate(matrix):
        vals = row[np.isfinite(row)]
        n = len(vals)
        if n < 2:
            continue
        mean_sq = float(np.mean(vals ** 2))
        if not np.isfinite(mean_sq) or mean_sq <= 1e-15:
            continue
        mean_response = float(np.mean(vals))
        out[row_idx] = (1.0 - (mean_response ** 2) / mean_sq) / (1.0 - 1.0 / n)
    return out


def _mean_sd(values: np.ndarray) -> tuple[float, float, int]:
    vals = finite_values(values)
    if len(vals) == 0:
        return np.nan, np.nan, 0
    mean = float(np.mean(vals))
    sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else np.nan
    return mean, sd, len(vals)


def _equation_footer() -> str:
    return (
        r"$SI_{FI/FO}=(R_{FI}-R_{FO})/(R_{FI}+R_{FO})$"
        "     "
        r"$S_{AM}=\frac{1-(\bar{R}^{2}/\overline{R^{2}})}{1-1/N}$"
    )


def _plot_trace_condition_axis(ax, traces: np.ndarray, tvec: np.ndarray, color: str, title: str) -> None:
    traces = np.asarray(traces, dtype=float)
    if traces.ndim != 2 or traces.shape[0] == 0:
        ax.text(0.5, 0.5, "No valid trials", transform=ax.transAxes, ha="center", va="center")
        ax.set_title(title)
        return
    for row in traces:
        ax.plot(tvec, row, color=color, alpha=0.18, ls="--", lw=0.75)
    mean_trace = np.nanmean(traces, axis=0)
    sd_trace = np.nanstd(traces, axis=0, ddof=1) if traces.shape[0] > 1 else np.full(traces.shape[1], np.nan)
    valid_sd = np.isfinite(mean_trace) & np.isfinite(sd_trace)
    if np.any(valid_sd):
        ax.fill_between(
            tvec,
            mean_trace - sd_trace,
            mean_trace + sd_trace,
            color=color,
            alpha=0.18,
            linewidth=0,
            label="mean ± SD",
        )
        ax.plot(tvec, mean_trace - sd_trace, color=color, alpha=0.55, lw=1.0)
        ax.plot(tvec, mean_trace + sd_trace, color=color, alpha=0.55, lw=1.0)
    ax.plot(tvec, mean_trace, color=color, lw=2.5, label="mean")
    ax.axvline(0, color="black", ls=":", lw=1)
    ax.axhline(0, color="black", ls=":", lw=0.8)
    ax.set_title(f"{title}\nn={traces.shape[0]} trials")
    ax.set_xlabel("Time from onset (s)")
    ax.grid(axis="y", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)


def _plot_response_condition_points(ax, values_by_condition, labels, colors, ylabel: str) -> None:
    rng = np.random.default_rng(91827)
    all_means, all_sds = [], []
    for pos, (values, label, color) in enumerate(zip(values_by_condition, labels, colors)):
        vals = finite_values(values)
        if len(vals):
            jitter = rng.uniform(-0.09, 0.09, len(vals))
            ax.scatter(
                np.full(len(vals), pos, dtype=float) + jitter,
                vals,
                color=color,
                alpha=0.24,
                s=18,
                edgecolors="none",
                zorder=2,
            )
        mean, sd, _ = _mean_sd(vals)
        all_means.append(mean); all_sds.append(sd)
        if np.isfinite(mean):
            ax.errorbar(
                pos,
                mean,
                yerr=sd if np.isfinite(sd) else None,
                marker="o",
                color=color,
                markersize=8,
                lw=2.2,
                elinewidth=2.0,
                capsize=5,
                zorder=4,
            )
    ax.axhline(0, color="black", ls=":", lw=0.8)
    ax.set_xticks(np.arange(len(labels)), labels, rotation=0)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.18)
    ax.spines[["top", "right"]].set_visible(False)
    apply_mean_error_y_limits(ax, all_means, all_sds, reference_values=[0.0])


def _save_session_ranked_example_figures(
    cell_df: pd.DataFrame,
    eventlocked_baseline_corrected: np.ndarray,
    trial_response: np.ndarray,
    tvec: np.ndarray,
    fade_in_mask: np.ndarray,
    fade_out_mask: np.ndarray,
    am_masks: list[np.ndarray],
    am_rates: np.ndarray,
    session_output_dir: Path,
    title_suffix: str,
    folder_name: str,
    ranking_column: str,
    ranking_display_name: str,
    require_fdr_sound_responsive: bool = False,
) -> None:
    """Save ranked GREEN/YELLOW example cells for one session."""
    root = session_output_dir / folder_name
    root.mkdir(parents=True, exist_ok=True)
    am_colors = [plt.cm.viridis(v) for v in np.linspace(0.15, 0.85, max(len(am_rates), 1))]

    for class_name, class_color in [("green", GREEN_COLOR), ("yellow", YELLOW_COLOR)]:
        cdf = cell_df[cell_df["cell_class"] == class_name].copy()
        if require_fdr_sound_responsive and "sound_responsive_fdr" in cdf.columns:
            cdf = cdf[cdf["sound_responsive_fdr"].astype(bool)].copy()
        cdf = cdf[np.isfinite(cdf[ranking_column])].copy()
        if len(cdf) == 0:
            continue
        cdf["_abs_rank_metric"] = np.abs(cdf[ranking_column].to_numpy(dtype=float))
        cdf = cdf.sort_values("_abs_rank_metric", ascending=False).head(N_EXAMPLE_CELLS_PER_CLASS)
        class_dir = root / class_name
        class_dir.mkdir(parents=True, exist_ok=True)

        for rank, (_, row) in enumerate(cdf.iterrows(), start=1):
            i = int(row["analysis_index"])
            roi = int(row["suite2p_roi"])
            fi_fo_si = float(row["fade_in_vs_fade_out_selectivity"])
            am_sparse = float(row["am_rate_lifetime_sparseness"])
            rank_metric_value = float(row[ranking_column])

            n_am = max(len(am_rates), 1)
            fig = plt.figure(figsize=(max(18, 4.0 * (2 + n_am)), 6.2))
            outer = fig.add_gridspec(1, 2, width_ratios=[2, n_am], wspace=0.25)
            left = outer[0, 0].subgridspec(1, 2, wspace=0.28)
            right = outer[0, 1].subgridspec(1, n_am, wspace=0.28)
            left_axes = [fig.add_subplot(left[0, j]) for j in range(2)]
            right_axes = [fig.add_subplot(right[0, j]) for j in range(n_am)]

            _plot_trace_condition_axis(
                left_axes[0], eventlocked_baseline_corrected[i, fade_in_mask, :], tvec,
                FADE_IN_COLOR, "Fade-in"
            )
            _plot_trace_condition_axis(
                left_axes[1], eventlocked_baseline_corrected[i, fade_out_mask, :], tvec,
                FADE_OUT_COLOR, "Fade-out"
            )
            left_axes[0].set_ylabel("Baseline-subtracted dF/F")
            for j, ax in enumerate(right_axes):
                if j < len(am_rates):
                    _plot_trace_condition_axis(
                        ax,
                        eventlocked_baseline_corrected[i, am_masks[j], :],
                        tvec,
                        am_colors[j],
                        f"AM {am_rates[j]:g} Hz",
                    )
                else:
                    ax.axis("off")
            right_axes[0].set_ylabel("Baseline-subtracted dF/F")
            fig.text(0.20, 0.835, "Fade-in vs fade-out", ha="center", va="center", fontsize=12, fontweight="bold")
            fig.text(0.68, 0.835, "AM-rate responses", ha="center", va="center", fontsize=12, fontweight="bold")
            fig.suptitle(
                f"{title_suffix} | {class_name.upper()} rank {rank} | ROI {roi}\n"
                f"{ranking_display_name}={rank_metric_value:.3f} | "
                f"FI/FO selectivity={fi_fo_si:.3f} | AM lifetime sparseness={am_sparse:.3f}",
                fontsize=13,
                y=0.98,
            )
            fig.text(0.5, 0.015, _equation_footer(), ha="center", va="bottom", fontsize=10)
            fig.subplots_adjust(top=0.76, bottom=0.14)
            fig.savefig(class_dir / f"rank_{rank:02d}_roi_{roi:04d}_full_traces.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

            fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.8))
            _plot_response_condition_points(
                axes[0],
                [trial_response[i, fade_in_mask], trial_response[i, fade_out_mask]],
                ["Fade-in", "Fade-out"],
                [FADE_IN_COLOR, FADE_OUT_COLOR],
                "Mean baseline-corrected dF/F (0–1 s)",
            )
            axes[0].set_title("Fade-in vs fade-out trial responses\nlight points = trials; dark = mean ± SD")
            _plot_response_condition_points(
                axes[1],
                [trial_response[i, mask] for mask in am_masks],
                [f"{rate:g} Hz" for rate in am_rates],
                am_colors[:len(am_rates)],
                "Mean baseline-corrected dF/F (0–1 s)",
            )
            axes[1].set_title("AM-rate trial responses\nlight points = trials; dark = mean ± SD")
            fig.suptitle(
                f"{title_suffix} | {class_name.upper()} rank {rank} | ROI {roi}\n"
                f"{ranking_display_name}={rank_metric_value:.3f} | "
                f"FI/FO selectivity={fi_fo_si:.3f} | AM lifetime sparseness={am_sparse:.3f}",
                fontsize=13,
                y=0.98,
            )
            fig.text(0.5, 0.015, _equation_footer(), ha="center", va="bottom", fontsize=10)
            fig.subplots_adjust(top=0.79, bottom=0.18, wspace=0.28)
            fig.savefig(class_dir / f"rank_{rank:02d}_roi_{roi:04d}_response_scalars.png", dpi=300, bbox_inches="tight")
            plt.close(fig)


def save_session_selective_example_figures(
    cell_df: pd.DataFrame,
    eventlocked_baseline_corrected: np.ndarray,
    trial_response: np.ndarray,
    tvec: np.ndarray,
    fade_in_mask: np.ndarray,
    fade_out_mask: np.ndarray,
    am_masks: list[np.ndarray],
    am_rates: np.ndarray,
    session_output_dir: Path,
    title_suffix: str,
) -> None:
    _save_session_ranked_example_figures(
        cell_df=cell_df,
        eventlocked_baseline_corrected=eventlocked_baseline_corrected,
        trial_response=trial_response,
        tvec=tvec,
        fade_in_mask=fade_in_mask,
        fade_out_mask=fade_out_mask,
        am_masks=am_masks,
        am_rates=am_rates,
        session_output_dir=session_output_dir,
        title_suffix=title_suffix,
        folder_name="example_selective_cells",
        ranking_column="fade_in_vs_fade_out_selectivity",
        ranking_display_name="|FI/FO selectivity| rank metric",
        require_fdr_sound_responsive=False,
    )


def save_session_sound_responsive_example_figures(
    cell_df: pd.DataFrame,
    eventlocked_baseline_corrected: np.ndarray,
    trial_response: np.ndarray,
    tvec: np.ndarray,
    fade_in_mask: np.ndarray,
    fade_out_mask: np.ndarray,
    am_masks: list[np.ndarray],
    am_rates: np.ndarray,
    session_output_dir: Path,
    title_suffix: str,
) -> None:
    _save_session_ranked_example_figures(
        cell_df=cell_df,
        eventlocked_baseline_corrected=eventlocked_baseline_corrected,
        trial_response=trial_response,
        tvec=tvec,
        fade_in_mask=fade_in_mask,
        fade_out_mask=fade_out_mask,
        am_masks=am_masks,
        am_rates=am_rates,
        session_output_dir=session_output_dir,
        title_suffix=title_suffix,
        folder_name="example_sound_responsive_cells",
        ranking_column="mean_sound_response",
        ranking_display_name="|mean sound response| rank metric",
        require_fdr_sound_responsive=True,
    )

def safe_mannwhitney(a: np.ndarray, b: np.ndarray) -> dict[str, float | None]:
    a = finite_values(a)
    b = finite_values(b)
    if len(a) == 0 or len(b) == 0:
        return {"statistic": None, "p": None, "n_a": len(a), "n_b": len(b)}
    result = stats.mannwhitneyu(a, b, alternative="two-sided", method="auto")
    return {
        "statistic": float(result.statistic),
        "p": float(result.pvalue),
        "n_a": len(a),
        "n_b": len(b),
    }


def safe_wilcoxon(
    values: np.ndarray,
    alternative: str = "two-sided",
) -> dict[str, float | None]:
    values = finite_values(values)
    if len(values) == 0 or not np.any(values != 0):
        return {"statistic": None, "p": None, "n": len(values)}
    try:
        result = stats.wilcoxon(
            values,
            alternative=alternative,
            zero_method="wilcox",
        )
    except ValueError:
        return {"statistic": None, "p": None, "n": len(values)}
    return {
        "statistic": float(result.statistic),
        "p": float(result.pvalue),
        "n": len(values),
    }


def safe_paired_wilcoxon(
    a: np.ndarray,
    b: np.ndarray,
    alternative: str = "two-sided",
) -> dict[str, float | None]:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    valid = np.isfinite(a) & np.isfinite(b)
    a = a[valid]
    b = b[valid]
    if len(a) == 0:
        return {"statistic": None, "p": None, "n_pairs": 0}
    diff = a - b
    out = safe_wilcoxon(diff, alternative=alternative)
    return {"statistic": out["statistic"], "p": out["p"], "n_pairs": len(a)}


# =============================================================================
# INFO2P SESSION DISCOVERY
# =============================================================================

def canonical_brain_area(brain_area: Any) -> str | None:
    """Collapse info2p brainArea strings to A1 / AAF / A2."""
    text = str(brain_area)
    upper = text.upper()
    # Explicit order keeps matching predictable.
    if "AAF" in upper:
        return "AAF"
    if "A1" in upper:
        return "A1"
    if "A2" in upper or "AUV" in upper:
        return "A2"
    return None


def load_info2p_sessions(subject: str) -> tuple[Path, list[dict[str, Any]]]:
    info2p_dir = Path(settings.INFO2P_PATH)
    info_file = info2p_dir / f"{subject}_info2p.py"
    if not info_file.exists():
        raise FileNotFoundError(f"Subject info2p file not found:\n{info_file}")

    module_name = f"_batch_{subject}_info2p"
    spec = importlib.util.spec_from_file_location(module_name, info_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load info2p file:\n{info_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sessions = getattr(module, "sessions", None)
    if sessions is None:
        raise AttributeError(f"No 'sessions' list found in:\n{info_file}")
    return info_file, list(sessions)


def select_sessions(
    sessions: list[dict[str, Any]],
    requested_dates: list[str],
    requested_area: str,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    requested_dates_set = set(requested_dates)
    for session in sessions:
        date = str(session.get("date", ""))
        paradigm = str(session.get("paradigm", ""))
        raw_area = session.get("brainArea", "")
        area = canonical_brain_area(raw_area)
        if (
            date in requested_dates_set
            and paradigm == PARADIGM
            and area == requested_area
        ):
            item = dict(session)
            item["canonicalArea"] = area
            selected.append(item)
    selected.sort(key=lambda s: (str(s.get("date", "")), str(s.get("session", ""))))
    return selected


def session_selection_dataframe(selected: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for s in selected:
        rows.append(
            {
                "subject": s.get("subject"),
                "date": str(s.get("date")),
                "session": str(s.get("session")),
                "brainArea": s.get("brainArea"),
                "canonicalArea": s.get("canonicalArea"),
                "depth": s.get("depth"),
                "sessionLabel": s.get("sessionLabel"),
                "paradigm": s.get("paradigm"),
                "fps": s.get("fps"),
                "magnification": s.get("magnification"),
            }
        )
    return pd.DataFrame(rows)


# =============================================================================
# OUTPUT TREE
# =============================================================================

def build_output_dirs(
    subject: str,
    area: str,
    dates: list[str],
) -> dict[str, Path]:
    date_tag = "_".join(dates)
    root = (
        Path(settings.TEMP_OUTPUT_PATH)
        / "evan"
        / "sound_tuning_area_analysis"
        / subject
        / area
        / date_tag
    )
    session_root = root / "session_outputs"
    combined = root / "combined"
    session_root.mkdir(parents=True, exist_ok=True)
    combined.mkdir(parents=True, exist_ok=True)
    return {"root": root, "session_root": session_root, "combined": combined}


# =============================================================================
# ROI / IMAGE HELPERS
# =============================================================================

def robust_image_limits(image: np.ndarray) -> tuple[float, float]:
    finite = image[np.isfinite(image)]
    if len(finite) == 0:
        raise ValueError("Image contains no finite pixels.")
    return float(np.percentile(finite, 1)), float(np.percentile(finite, 99.5))


def draw_binary_mask_contour(ax, binary_mask, color, linewidth):
    if np.any(binary_mask):
        ax.contour(
            binary_mask.astype(float),
            levels=[0.5],
            colors=[color],
            linewidths=linewidth,
        )


def draw_functional_roi_contour(ax, roi_stat, color, linewidth, Ly, Lx):
    ypix = np.asarray(roi_stat["ypix"], dtype=int)
    xpix = np.asarray(roi_stat["xpix"], dtype=int)
    valid = (ypix >= 0) & (ypix < Ly) & (xpix >= 0) & (xpix < Lx)
    ypix = ypix[valid]
    xpix = xpix[valid]
    if len(xpix) == 0:
        return
    padding = 2
    xmin = max(0, int(np.min(xpix)) - padding)
    xmax = min(Lx - 1, int(np.max(xpix)) + padding)
    ymin = max(0, int(np.min(ypix)) - padding)
    ymax = min(Ly - 1, int(np.max(ypix)) + padding)
    local_mask = np.zeros((ymax - ymin + 1, xmax - xmin + 1), dtype=float)
    local_mask[ypix - ymin, xpix - xmin] = 1.0
    ax.contour(
        local_mask,
        levels=[0.5],
        colors=[color],
        linewidths=linewidth,
        origin="upper",
        extent=[xmin - 0.5, xmax + 0.5, ymax + 0.5, ymin - 0.5],
    )


def red_labels_overlapping_yellow(
    functional_stats: np.ndarray,
    yellow_mask: np.ndarray,
    red_masks: np.ndarray,
) -> set[int]:
    Ly, Lx = red_masks.shape
    labels_to_hide: set[int] = set()
    for analysis_index, roi_stat in enumerate(functional_stats):
        if not yellow_mask[analysis_index]:
            continue
        ypix = np.asarray(roi_stat["ypix"], dtype=int)
        xpix = np.asarray(roi_stat["xpix"], dtype=int)
        valid = (ypix >= 0) & (ypix < Ly) & (xpix >= 0) & (xpix < Lx)
        ypix = ypix[valid]
        xpix = xpix[valid]
        if len(xpix) == 0:
            continue
        labels = np.unique(red_masks[ypix, xpix])
        for label in labels[labels > 0]:
            labels_to_hide.add(int(label))
    return labels_to_hide


def save_classification_overlay(
    background: np.ndarray,
    background_name: str,
    functional_stats: np.ndarray,
    red_masks: np.ndarray,
    green_mask: np.ndarray,
    yellow_mask: np.ndarray,
    output_path: Path,
    title_suffix: str,
) -> None:
    Ly, Lx = background.shape
    vmin, vmax = robust_image_limits(background)
    labels = np.unique(red_masks)
    labels = labels[labels > 0]
    labels_to_hide = red_labels_overlapping_yellow(
        functional_stats, yellow_mask, red_masks
    )
    visible_labels = [int(x) for x in labels if int(x) not in labels_to_hide]

    fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)
    ax.imshow(
        background,
        cmap="gray",
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest",
    )

    for i, roi_stat in enumerate(functional_stats):
        if green_mask[i]:
            draw_functional_roi_contour(
                ax,
                roi_stat,
                DISPLAY_GREEN_COLOR,
                FUNCTIONAL_OUTLINE_LW,
                Ly,
                Lx,
            )

    for label in visible_labels:
        draw_binary_mask_contour(
            ax,
            red_masks == label,
            ANATOMICAL_RED_COLOR,
            RED_OUTLINE_LW,
        )

    for i, roi_stat in enumerate(functional_stats):
        if yellow_mask[i]:
            draw_functional_roi_contour(
                ax,
                roi_stat,
                DISPLAY_YELLOW_COLOR,
                FUNCTIONAL_OUTLINE_LW,
                Ly,
                Lx,
            )

    legend_handles = [
        Line2D([0], [0], color=DISPLAY_GREEN_COLOR, lw=1.5,
               label=f"Green functional ROIs (n={int(np.sum(green_mask))})"),
        Line2D([0], [0], color=DISPLAY_YELLOW_COLOR, lw=1.5,
               label=f"Yellow functional ROIs (n={int(np.sum(yellow_mask))})"),
        Line2D([0], [0], color=ANATOMICAL_RED_COLOR, lw=1.5,
               label=f"Visible red anatomical ROIs (n={len(visible_labels)})"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", frameon=True, fontsize=8)
    ax.set_title(
        f"{background_name}: green, red, and yellow outlines\n"
        f"yellow overrides overlapping red outlines\n{title_suffix}"
    )
    ax.set_xlabel("X pixel")
    ax.set_ylabel("Y pixel")
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# SIGN-FLIP RESPONSE TEST
# =============================================================================

def signflip_pvalues_grouped(
    response_matrix: np.ndarray,
    tested_mask: np.ndarray,
    n_permutations: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Two-sided Monte-Carlo sign-flip p-values.

    This is the same null hypothesis as the notebook, but cells sharing the same
    finite-trial pattern reuse one random sign matrix for speed. P-values remain
    valid Monte-Carlo sign-flip tests; they will not reproduce the notebook's
    exact random numbers cell-by-cell.
    """
    response_matrix = np.asarray(response_matrix, dtype=float)
    tested_mask = np.asarray(tested_mask, dtype=bool)
    n_cells = response_matrix.shape[0]
    p_values = np.full(n_cells, np.nan, dtype=float)
    tested_indices = np.flatnonzero(tested_mask)
    if len(tested_indices) == 0:
        return p_values

    groups: dict[bytes, list[int]] = {}
    finite_masks: dict[bytes, np.ndarray] = {}
    for cell_index in tested_indices:
        finite = np.isfinite(response_matrix[cell_index])
        key = np.packbits(finite).tobytes()
        groups.setdefault(key, []).append(int(cell_index))
        finite_masks[key] = finite

    for key, cell_indices_list in groups.items():
        finite = finite_masks[key]
        n_trials = int(np.sum(finite))
        if n_trials < 3:
            continue
        cell_indices = np.asarray(cell_indices_list, dtype=int)
        values = response_matrix[cell_indices][:, finite]
        observed = np.mean(values, axis=1)

        # float32 substantially lowers memory while preserving the Monte-Carlo
        # comparison at the precision relevant here.
        signs = rng.choice(
            np.array([-1.0, 1.0], dtype=np.float32),
            size=(n_permutations, n_trials),
            replace=True,
        )
        null_means = (signs @ values.T) / float(n_trials)
        extreme = np.sum(np.abs(null_means) >= np.abs(observed)[None, :], axis=0)
        p_values[cell_indices] = (1.0 + extreme) / (n_permutations + 1.0)

    return p_values


def align_imaging_events_to_behavior(
    eventlocked: np.ndarray,
    valid_events: np.ndarray,
    event_onset: np.ndarray,
    srate: float,
    stim_duration: np.ndarray,
    isi: np.ndarray,
    n_behavior_trials: int,
    max_extra_events: int = 5,
    max_mean_abs_error_s: float = 0.25,
    max_abs_error_s: float = 0.75,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    """Align imaging sound events to behavior using acquisition-order knowledge.

    Experimental acquisition always starts 2P imaging before the sound
    presentation is manually started. Therefore, when the imaging event stream
    contains a small number of extra sound triggers, those extras are assumed to
    be trailing events from sound presentation continuing beyond the behavioral
    file's intended trial count. The first ``n_behavior_trials`` imaging events
    are retained.

    The chosen alignment is still validated against the expected behavioral
    onset-to-onset intervals (stim_duration + ISI). If timing agreement is poor,
    the session fails rather than silently accepting a questionable alignment.
    """
    valid_events = np.asarray(valid_events, dtype=bool)
    event_onset = np.asarray(event_onset, dtype=float)
    n_imaging_events = int(eventlocked.shape[1])

    if len(valid_events) != n_imaging_events:
        raise ValueError(
            f"valid_events has length {len(valid_events)} but eventlocked has "
            f"{n_imaging_events} imaging events."
        )
    if len(event_onset) != n_imaging_events:
        raise ValueError(
            f"event_onset has length {len(event_onset)} but eventlocked has "
            f"{n_imaging_events} imaging events."
        )

    if n_imaging_events < n_behavior_trials:
        raise ValueError(
            f"Fewer imaging events than behavioral trials: {n_imaging_events} vs "
            f"{n_behavior_trials}. Automatic alignment is not safe."
        )

    extra = n_imaging_events - n_behavior_trials
    if extra > max_extra_events:
        raise ValueError(
            f"Unexpected trial mismatch: {n_imaging_events} imaging events vs "
            f"{n_behavior_trials} behavioral trials ({extra} extra imaging events). "
            f"Automatic trailing-event trimming is limited to <= {max_extra_events} extras."
        )

    # Acquisition order tells us which side to trim: keep the first N imaging
    # sound events and ignore only trailing extras.
    start = 0
    stop = n_behavior_trials
    aligned_eventlocked = eventlocked[:, start:stop, :]
    aligned_valid_events = valid_events[start:stop]
    aligned_event_onset = event_onset[start:stop]

    stim_duration = np.asarray(stim_duration, dtype=float).reshape(-1)
    isi = np.asarray(isi, dtype=float).reshape(-1)
    if len(stim_duration) < n_behavior_trials or len(isi) < n_behavior_trials:
        raise ValueError(
            "Cannot validate imaging/behavior alignment because stim_duration or "
            "ISI is shorter than the behavioral trial count."
        )

    # For behavioral trials 0..N-2, expected onset(k+1)-onset(k) is the current
    # stimulus duration plus its following ISI.
    expected_intervals = stim_duration[: n_behavior_trials - 1] + isi[: n_behavior_trials - 1]
    observed_intervals = np.diff(aligned_event_onset) / float(srate)
    finite = np.isfinite(observed_intervals) & np.isfinite(expected_intervals)
    if not np.any(finite):
        raise ValueError(
            "Could not evaluate any finite imaging/behavior timing intervals for alignment QC."
        )

    errors = observed_intervals[finite] - expected_intervals[finite]
    timing_mae = float(np.mean(np.abs(errors)))
    timing_maxerr = float(np.max(np.abs(errors)))

    if timing_mae > max_mean_abs_error_s or timing_maxerr > max_abs_error_s:
        raise ValueError(
            f"First-event alignment failed timing QC for {n_imaging_events} imaging "
            f"events vs {n_behavior_trials} behavioral trials. MAE={timing_mae:.4f}s, "
            f"max error={timing_maxerr:.4f}s. Acceptance limits are "
            f"MAE<={max_mean_abs_error_s:.3f}s and max<={max_abs_error_s:.3f}s."
        )

    if extra == 0:
        alignment_note = "imaging and behavioral trial counts matched; first-event alignment used"
    else:
        alignment_note = (
            f"first-event alignment used imaging events 0:{stop}; "
            f"ignored {extra} trailing imaging event{'s' if extra != 1 else ''}"
        )

    diagnostics = {
        "alignment_note": alignment_note,
        "alignment_offset": 0,
        "n_extra_imaging_events": int(extra),
        "n_extra_before": 0,
        "n_extra_after": int(extra),
        "timing_mae_s": timing_mae,
        "timing_max_abs_error_s": timing_maxerr,
    }

    print("Trial alignment:")
    print(f"  imaging sound events: {n_imaging_events}")
    print(f"  behavioral trials:    {n_behavior_trials}")
    print(f"  using imaging events: 0:{stop}")
    print(f"  ignored trailing imaging events: {extra}")
    print("Timing validation:")
    print(f"  mean abs interval error: {timing_mae:.4f}s")
    print(f"  max abs interval error:  {timing_maxerr:.4f}s")
    print("  alignment PASSED")

    return aligned_eventlocked, aligned_valid_events, aligned_event_onset, diagnostics


# =============================================================================
# PER-SESSION ANALYSIS
# =============================================================================

def analyze_session(
    meta: dict[str, Any],
    plane: int,
    session_output_dir: Path,
    n_permutations: int,
    seed: int,
) -> dict[str, Any]:
    subject = str(meta["subject"])
    date = str(meta["date"])
    session = str(meta["session"])
    title_suffix = f"{subject} {date} {session} p{plane}"
    session_output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 78)
    print(f"ANALYZING {title_suffix} | {meta.get('brainArea')} | depth={meta.get('depth')}")
    print("=" * 78)

    data2p = twophotonanalysis.TwoPhoton(
        subject,
        date,
        session,
        plane,
        paradigm=PARADIGM,
    )
    suite2p_dir = Path(data2p.data_path)
    print(f"Suite2p directory: {suite2p_dir}")

    ops_path = suite2p_dir / "ops.npy"
    stat_path = suite2p_dir / "stat.npy"
    redcell_path = suite2p_dir / "redcell.npy"
    for required in (ops_path, stat_path):
        if not required.exists():
            raise FileNotFoundError(f"Missing required Suite2p file:\n{required}")

    ops = np.load(ops_path, allow_pickle=True).item()
    stat_array = np.load(stat_path, allow_pickle=True)
    redcell_data = np.load(redcell_path) if redcell_path.exists() else None

    # -------------------------------------------------------------------------
    # Define analyzed cells once, retaining original Suite2p ROI indices.
    # -------------------------------------------------------------------------
    cell_mask = (
        (data2p.iscell[:, 0] == 1)
        & (data2p.iscell[:, 1] > CELL_PROB_THRESHOLD)
    )
    cell_roi_indices = np.flatnonzero(cell_mask)
    functional_stats = stat_array[cell_roi_indices]

    eventlocked_all, tvec, valid_events = data2p.event_locked_average(
        time_range=list(TIME_RANGE),
        dff=True,
    )
    eventlocked = eventlocked_all[cell_mask, :, :]
    valid_events = np.asarray(valid_events, dtype=bool)
    n_analysis_cells = eventlocked.shape[0]
    if n_analysis_cells != len(cell_roi_indices):
        raise ValueError("eventlocked rows do not match retained cell indices.")

    # -------------------------------------------------------------------------
    # Behavioral fields + imaging/behavior event alignment.
    # Do this BEFORE any trial-based QC/statistics so unmatched imaging triggers
    # can never enter the analysis.
    # -------------------------------------------------------------------------
    bdata = data2p.bdata
    required_bdata = [
        "current_stim_type",
        "current_AM_rate",
        "fade_direction",
        "current_intensity",
        "stim_duration",
        "ISI",
    ]
    missing_bdata = [key for key in required_bdata if key not in bdata]
    if missing_bdata:
        raise KeyError("Missing sound_tuning behavioral fields: " + ", ".join(missing_bdata))

    stim_type = np.asarray(bdata["current_stim_type"])
    current_am = np.asarray(bdata["current_AM_rate"], dtype=float)
    fade_direction = np.asarray(bdata["fade_direction"])
    stim_duration = np.asarray(bdata["stim_duration"], dtype=float)
    isi = np.asarray(bdata["ISI"], dtype=float)
    n_behavior_trials = len(stim_type)
    n_imaging_events = eventlocked.shape[1]

    (
        eventlocked_aligned,
        valid_events_aligned,
        event_onset_aligned,
        alignment_diagnostics,
    ) = align_imaging_events_to_behavior(
        eventlocked=eventlocked,
        valid_events=valid_events,
        event_onset=np.asarray(data2p.event_onset),
        srate=float(data2p.srate),
        stim_duration=stim_duration,
        isi=isi,
        n_behavior_trials=n_behavior_trials,
    )
    alignment_note = alignment_diagnostics["alignment_note"]

    assert eventlocked_aligned.shape[1] == n_behavior_trials
    assert len(valid_events_aligned) == n_behavior_trials
    assert len(event_onset_aligned) == n_behavior_trials

    print(
        f"Aligned event-locked data: {eventlocked_aligned.shape}; "
        f"valid trials={int(np.sum(valid_events_aligned))}/{n_behavior_trials}"
    )

    # -------------------------------------------------------------------------
    # Cellpose anatomical tdTomato segmentation + functional overlap.
    # -------------------------------------------------------------------------
    if ops.get("meanImg_chan2") is not None:
        red_image = np.asarray(ops["meanImg_chan2"], dtype=float)
        red_image_name = "meanImg_chan2"
    elif ops.get("meanImg_chan2_corrected") is not None:
        red_image = np.asarray(ops["meanImg_chan2_corrected"], dtype=float)
        red_image_name = "meanImg_chan2_corrected"
    else:
        raise KeyError("No channel-2 mean image found in ops.npy.")

    if ops.get("meanImg") is None:
        raise KeyError("No channel-1 mean image (meanImg) found in ops.npy.")
    chan1_image = np.asarray(ops["meanImg"], dtype=float)

    # Retain the legacy Suite2p channel-2 score as optional metadata only.
    # It is NOT used to classify or exclude any cell.
    if redcell_data is not None and redcell_data.ndim == 2 and redcell_data.shape[1] > 1:
        suite2p_chan2_scores = np.asarray(
            redcell_data[cell_roi_indices, 1], dtype=float
        )
    else:
        suite2p_chan2_scores = np.full(n_analysis_cells, np.nan, dtype=float)

    equivalent_diameters = []
    for roi_stat in functional_stats:
        n_pixels = len(roi_stat["ypix"])
        if n_pixels > 0:
            equivalent_diameters.append(2 * np.sqrt(n_pixels / np.pi))
    if not equivalent_diameters:
        raise ValueError("Could not estimate functional ROI diameter.")
    estimated_diameter = float(np.median(equivalent_diameters))
    cellpose_diameter = (
        estimated_diameter if CELLPOSE_DIAMETER is None else float(CELLPOSE_DIAMETER)
    )
    cellpose_settings = {
        "params": None,
        "chan2_params": None,
        "cellprob_threshold": CELLPOSE_CELLPROB_THRESHOLD,
        "flow_threshold": CELLPOSE_FLOW_THRESHOLD,
    }
    print(
        "Cellpose: "
        f"diameter={cellpose_diameter:.2f}, "
        f"cellprob={CELLPOSE_CELLPROB_THRESHOLD:.2f}, "
        f"flow={CELLPOSE_FLOW_THRESHOLD:.2f}, IoU>{IOU_THRESHOLD:.2f}"
    )
    cellpose_redstats, cellpose_red_masks = cellpose_overlap(
        functional_stats,
        red_image,
        diameter=cellpose_diameter,
        chan2_threshold=IOU_THRESHOLD,
        device=torch.device("cpu"),
        settings=cellpose_settings,
    )
    cellpose_red_iou = np.asarray(cellpose_redstats[:, 1], dtype=float)

    # Final classification: every analyzed functional ROI is assigned GREEN or
    # YELLOW solely from Cellpose anatomical overlap.  No legacy-score outlier
    # exclusion is applied.
    yellow_cell_mask = cellpose_red_iou > IOU_THRESHOLD
    green_only_mask = ~yellow_cell_mask
    excluded_mask = np.zeros(n_analysis_cells, dtype=bool)  # compatibility only
    classified_mask = green_only_mask | yellow_cell_mask

    if not np.all(classified_mask):
        raise RuntimeError("Every analyzed ROI should be classified GREEN or YELLOW.")

    n_green = int(np.sum(green_only_mask))
    n_yellow = int(np.sum(yellow_cell_mask))
    n_excluded = 0
    n_red_anatomical = int(len(np.unique(cellpose_red_masks)[np.unique(cellpose_red_masks) > 0]))
    print(
        f"Classification: green={n_green}, yellow={n_yellow}, "
        f"excluded=0, red anatomical={n_red_anatomical}"
    )
    print("Legacy Suite2p channel-2 scores retained as metadata only; no cell excluded.")

    # Save final classification, matching notebook variables plus useful IoU.
    np.savez(
        session_output_dir / f"{subject}_{date}_{session}_p{plane}_green_yellow_classification.npz",
        cell_roi_indices=np.asarray(cell_roi_indices, dtype=int),
        green_only_mask=np.asarray(green_only_mask, dtype=bool),
        yellow_cell_mask=np.asarray(yellow_cell_mask, dtype=bool),
        excluded_mask=np.asarray(excluded_mask, dtype=bool),
        green_cell_roi_indices=np.asarray(cell_roi_indices[green_only_mask], dtype=int),
        yellow_cell_roi_indices=np.asarray(cell_roi_indices[yellow_cell_mask], dtype=int),
        excluded_roi_indices=np.asarray(cell_roi_indices[excluded_mask], dtype=int),
        cellpose_red_iou=cellpose_red_iou,
        legacy_chan2_score=suite2p_chan2_scores,
        iou_threshold=float(IOU_THRESHOLD),
        cellpose_cellprob_threshold=float(CELLPOSE_CELLPROB_THRESHOLD),
        cellpose_flow_threshold=float(CELLPOSE_FLOW_THRESHOLD),
        cellpose_diameter=float(cellpose_diameter),
    )

    # Per-session spatial QC on both channels.
    save_classification_overlay(
        red_image,
        red_image_name,
        functional_stats,
        cellpose_red_masks,
        green_only_mask,
        yellow_cell_mask,
        session_output_dir / f"{subject}_{date}_{session}_p{plane}_chan2_classification_overlay.png",
        title_suffix,
    )
    save_classification_overlay(
        chan1_image,
        "meanImg (chan1)",
        functional_stats,
        cellpose_red_masks,
        green_only_mask,
        yellow_cell_mask,
        session_output_dir / f"{subject}_{date}_{session}_p{plane}_chan1_classification_overlay.png",
        title_suffix,
    )

    # -------------------------------------------------------------------------
    # All-sounds eventlocked QC (same analyzed cell set).
    # -------------------------------------------------------------------------
    trialavg = np.nanmean(eventlocked_aligned[:, valid_events_aligned, :], axis=1)
    fig = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs = fig.add_gridspec(4, 1)
    ax0 = fig.add_subplot(gs[:3, 0])
    im = ax0.imshow(
        trialavg,
        interpolation="nearest",
        extent=[tvec[0], tvec[-1], n_analysis_cells, 0],
        aspect="auto",
        cmap="viridis",
    )
    fig.colorbar(im, ax=ax0, label="dF/F")
    ax0.axvline(0, color="darkred")
    ax0.set_title(f"Event-locked average across all sound conditions\n{title_suffix}")
    ax0.set_ylabel("Cell")
    ax0.tick_params(labelbottom=False)
    ax1 = fig.add_subplot(gs[3, 0], sharex=ax0)
    ax1.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    ax1.axvline(0, color="darkred")
    ax1.set_xlabel("Time from sound onset (s)")
    ax1.set_ylabel("Mean dF/F")
    fig.savefig(
        session_output_dir / f"{subject}_{date}_{session}_p{plane}_all_sounds_eventlocked_avg.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    # -------------------------------------------------------------------------
    # Reliable sound response: notebook sign-flip test + BH-FDR, per session.
    # -------------------------------------------------------------------------
    baseline_mask_t = (tvec >= BASELINE_WINDOW[0]) & (tvec < BASELINE_WINDOW[1])
    response_mask_t = (tvec >= RESPONSE_WINDOW[0]) & (tvec <= RESPONSE_WINDOW[1])
    if not np.any(baseline_mask_t) or not np.any(response_mask_t):
        raise ValueError("Baseline/response windows do not overlap eventlocked tvec.")
    eventlocked_valid = eventlocked_aligned[:, valid_events_aligned, :]
    baseline_each_trial = np.nanmean(eventlocked_valid[:, :, baseline_mask_t], axis=2)
    response_each_trial = np.nanmean(eventlocked_valid[:, :, response_mask_t], axis=2)
    sound_evoked_response = response_each_trial - baseline_each_trial
    mean_sound_response = np.nanmean(sound_evoked_response, axis=1)
    median_sound_response = np.nanmedian(sound_evoked_response, axis=1)
    response_sd = np.nanstd(sound_evoked_response, axis=1, ddof=1)
    n_finite_trials = np.sum(np.isfinite(sound_evoked_response), axis=1)
    sem_sound_response = response_sd / np.sqrt(np.maximum(n_finite_trials, 1))
    sound_response_dz = np.full(n_analysis_cells, np.nan)
    valid_sd = classified_mask & np.isfinite(response_sd) & (response_sd > 1e-12)
    sound_response_dz[valid_sd] = mean_sound_response[valid_sd] / response_sd[valid_sd]

    session_rng = np.random.default_rng(seed)
    p_values = signflip_pvalues_grouped(
        sound_evoked_response,
        classified_mask,
        n_permutations,
        session_rng,
    )
    q_values = bh_fdr(p_values, classified_mask)
    sound_responsive_cells = classified_mask & np.isfinite(q_values) & (q_values < FDR_ALPHA)
    sound_excited_cells = sound_responsive_cells & (mean_sound_response > 0)
    sound_suppressed_cells = sound_responsive_cells & (mean_sound_response < 0)

    # -------------------------------------------------------------------------
    # Behavioral condition masks (event alignment was completed above).
    # -------------------------------------------------------------------------
    am_trials = stim_type == 0
    fading_trials = stim_type == 1
    fade_in_trials = fading_trials & (fade_direction == 0)
    fade_out_trials = fading_trials & (fade_direction == 1)
    possible_am_rates = np.sort(np.unique(current_am[am_trials & np.isfinite(current_am)]))

    # Trial-specific baseline correction and one response value per trial.
    trial_baseline = np.nanmean(
        eventlocked_aligned[:, :, baseline_mask_t], axis=2, keepdims=True
    )
    eventlocked_baseline_corrected = eventlocked_aligned - trial_baseline
    trial_response = np.nanmean(
        eventlocked_baseline_corrected[:, :, response_mask_t], axis=2
    )
    condition_names = ["Fade-in", "Fade-out"] + [
        f"AM {rate:g} Hz" for rate in possible_am_rates
    ]
    condition_masks = [
        fade_in_trials & valid_events_aligned,
        fade_out_trials & valid_events_aligned,
    ]
    for rate in possible_am_rates:
        condition_masks.append(
            am_trials & np.isclose(current_am, rate) & valid_events_aligned
        )

    condition_responses = np.full(
        (n_analysis_cells, len(condition_names)), np.nan, dtype=float
    )
    n_trials_each_condition = []
    for condition_index, condition_mask in enumerate(condition_masks):
        n_trials_condition = int(np.sum(condition_mask))
        n_trials_each_condition.append(n_trials_condition)
        if n_trials_condition > 0:
            condition_responses[:, condition_index] = np.nanmean(
                trial_response[:, condition_mask], axis=1
            )

    fade_in_response = condition_responses[:, 0]
    fade_out_response = condition_responses[:, 1]
    valid_am_trials = am_trials & valid_events_aligned
    mean_am_response_trial_weighted = (
        np.nanmean(trial_response[:, valid_am_trials], axis=1)
        if np.any(valid_am_trials)
        else np.full(n_analysis_cells, np.nan)
    )
    am_condition_responses = condition_responses[:, 2:]
    mean_am_across_rates = (
        np.nanmean(am_condition_responses, axis=1)
        if am_condition_responses.shape[1] > 0
        else np.full(n_analysis_cells, np.nan)
    )

    best_am_idx = np.full(n_analysis_cells, -1, dtype=int)
    best_am_response = np.full(n_analysis_cells, np.nan)
    best_am_rate = np.full(n_analysis_cells, np.nan)
    if am_condition_responses.shape[1] > 0:
        finite_am_row = np.any(np.isfinite(am_condition_responses), axis=1)
        rows = np.flatnonzero(finite_am_row)
        best = np.nanargmax(am_condition_responses[rows], axis=1)
        best_am_idx[rows] = best
        best_am_response[rows] = am_condition_responses[rows, best]
        best_am_rate[rows] = possible_am_rates[best]

    fade_selectivity = response_selectivity_index(fade_in_response, fade_out_response)
    fadein_bestam_selectivity = response_selectivity_index(fade_in_response, best_am_response)
    am_rate_lifetime_sparseness = lifetime_sparseness(am_condition_responses)
    looming_score = fade_in_response - 0.5 * (fade_out_response + mean_am_across_rates)
    peak_abs_condition_response = np.full(n_analysis_cells, np.nan)
    finite_condition_row = np.any(np.isfinite(condition_responses), axis=1)
    peak_abs_condition_response[finite_condition_row] = np.nanmax(
        np.abs(condition_responses[finite_condition_row]), axis=1
    )
    raster_responsive = (
        classified_mask
        & np.isfinite(peak_abs_condition_response)
        & (peak_abs_condition_response > RASTER_MIN_ABS_RESPONSE)
    )
    preferred_condition_idx = np.full(n_analysis_cells, -1, dtype=int)
    rows = np.flatnonzero(finite_condition_row)
    if len(rows):
        preferred_condition_idx[rows] = np.nanargmax(condition_responses[rows], axis=1)

    # Mean FI/FO traces for the combined top-example panel.
    fade_in_valid = fade_in_trials & valid_events_aligned
    fade_out_valid = fade_out_trials & valid_events_aligned
    mean_fade_in_trace = (
        np.nanmean(eventlocked_baseline_corrected[:, fade_in_valid, :], axis=1)
        if np.any(fade_in_valid)
        else np.full((n_analysis_cells, len(tvec)), np.nan)
    )
    mean_fade_out_trace = (
        np.nanmean(eventlocked_baseline_corrected[:, fade_out_valid, :], axis=1)
        if np.any(fade_out_valid)
        else np.full((n_analysis_cells, len(tvec)), np.nan)
    )

    # -------------------------------------------------------------------------
    # Per-cell table.
    # -------------------------------------------------------------------------
    cell_class = np.full(n_analysis_cells, "unclassified", dtype=object)
    cell_class[green_only_mask] = "green"
    cell_class[yellow_cell_mask] = "yellow"

    cell_rows: list[dict[str, Any]] = []
    for i in range(n_analysis_cells):
        row: dict[str, Any] = {
            "subject": subject,
            "date": date,
            "session": session,
            "session_key": f"{date}_{session}",
            "brainArea": meta.get("brainArea"),
            "canonicalArea": meta.get("canonicalArea"),
            "depth": meta.get("depth"),
            "sessionLabel": meta.get("sessionLabel"),
            "plane": plane,
            "analysis_index": i,
            "suite2p_roi": int(cell_roi_indices[i]),
            "cell_class": cell_class[i],
            "excluded": bool(excluded_mask[i]),
            "cellpose_iou": float(cellpose_red_iou[i]),
            "legacy_chan2_score": float(suite2p_chan2_scores[i]),
            "mean_sound_response": float(mean_sound_response[i]),
            "median_sound_response": float(median_sound_response[i]),
            "sound_response_sem": float(sem_sound_response[i]),
            "sound_response_dz": float(sound_response_dz[i]),
            "sound_response_p": float(p_values[i]),
            "sound_response_q": float(q_values[i]),
            "sound_responsive_fdr": bool(sound_responsive_cells[i]),
            "sound_excited_fdr": bool(sound_excited_cells[i]),
            "sound_suppressed_fdr": bool(sound_suppressed_cells[i]),
            "fade_in_response": float(fade_in_response[i]),
            "fade_out_response": float(fade_out_response[i]),
            "mean_am_response_trial_weighted": float(mean_am_response_trial_weighted[i]),
            "mean_am_response_across_rates": float(mean_am_across_rates[i]),
            "best_am_response": float(best_am_response[i]),
            "best_am_rate": float(best_am_rate[i]),
            "fade_in_vs_fade_out_selectivity": float(fade_selectivity[i]),
            "fade_in_vs_best_am_selectivity": float(fadein_bestam_selectivity[i]),
            "am_rate_lifetime_sparseness": float(am_rate_lifetime_sparseness[i]),
            "looming_score": float(looming_score[i]),
            "peak_abs_condition_response": float(peak_abs_condition_response[i]),
            "raster_responsive": bool(raster_responsive[i]),
            "preferred_condition_index": int(preferred_condition_idx[i]),
            "preferred_condition": (
                condition_names[preferred_condition_idx[i]]
                if preferred_condition_idx[i] >= 0
                else None
            ),
        }
        for rate_index, rate in enumerate(possible_am_rates):
            row[f"am_response_{rate:g}Hz"] = float(am_condition_responses[i, rate_index])
        cell_rows.append(row)
    cell_df = pd.DataFrame(cell_rows)
    cell_df.to_csv(session_output_dir / "cell_results.csv", index=False)

    # Requested per-session examples:
    #   (1) top 10 GREEN and top 10 YELLOW cells by absolute FI/FO selectivity;
    #   (2) top 10 GREEN and top 10 YELLOW cells by absolute mean sound response
    #       among the statistically sound-responsive (BH-FDR) cells.
    example_tvec = np.asarray(tvec, dtype=float)
    example_fi_mask = np.asarray(condition_masks[0], dtype=bool)
    example_fo_mask = np.asarray(condition_masks[1], dtype=bool)
    example_am_masks = [np.asarray(mask, dtype=bool) for mask in condition_masks[2:]]
    example_am_rates = np.asarray(possible_am_rates, dtype=float)
    save_session_selective_example_figures(
        cell_df=cell_df,
        eventlocked_baseline_corrected=eventlocked_baseline_corrected,
        trial_response=trial_response,
        tvec=example_tvec,
        fade_in_mask=example_fi_mask,
        fade_out_mask=example_fo_mask,
        am_masks=example_am_masks,
        am_rates=example_am_rates,
        session_output_dir=session_output_dir,
        title_suffix=title_suffix,
    )
    save_session_sound_responsive_example_figures(
        cell_df=cell_df,
        eventlocked_baseline_corrected=eventlocked_baseline_corrected,
        trial_response=trial_response,
        tvec=example_tvec,
        fade_in_mask=example_fi_mask,
        fade_out_mask=example_fo_mask,
        am_masks=example_am_masks,
        am_rates=example_am_rates,
        session_output_dir=session_output_dir,
        title_suffix=title_suffix,
    )

    # Restore the notebook's reliable sound-responsive/non-responsive figure.
    sound_responsiveness_figure(
        cell_df,
        session_output_dir / f"{subject}_{date}_{session}_p{plane}_sound_responsive_cells_green_yellow.png",
        title_suffix,
    )

    # -------------------------------------------------------------------------
    # Per-class session summary (one row per session x GREEN/YELLOW).
    # -------------------------------------------------------------------------
    class_summary_rows: list[dict[str, Any]] = []
    for class_name, class_mask in (("green", green_only_mask), ("yellow", yellow_cell_mask)):
        n_class = int(np.sum(class_mask))
        n_sound_resp = int(np.sum(sound_responsive_cells & class_mask))
        n_excited = int(np.sum(sound_excited_cells & class_mask))
        n_suppressed = int(np.sum(sound_suppressed_cells & class_mask))
        n_raster_resp = int(np.sum(raster_responsive & class_mask))
        class_fade = fade_in_response[class_mask]
        class_fade_selectivity = fade_selectivity[class_mask]
        class_fade_bestam_selectivity = fadein_bestam_selectivity[class_mask]
        class_am_sparseness = am_rate_lifetime_sparseness[class_mask]
        class_summary: dict[str, Any] = {
            "subject": subject,
            "date": date,
            "session": session,
            "session_key": f"{date}_{session}",
            "brainArea": meta.get("brainArea"),
            "canonicalArea": meta.get("canonicalArea"),
            "depth": meta.get("depth"),
            "cell_class": class_name,
            "n_cells": n_class,
            "n_sound_responsive_fdr": n_sound_resp,
            "pct_sound_responsive_fdr": 100 * safe_divide(n_sound_resp, n_class),
            "n_sound_excited_fdr": n_excited,
            "pct_sound_excited_fdr": 100 * safe_divide(n_excited, n_class),
            "n_sound_suppressed_fdr": n_suppressed,
            "pct_sound_suppressed_fdr": 100 * safe_divide(n_suppressed, n_class),
            "n_raster_responsive": n_raster_resp,
            "pct_raster_responsive": 100 * safe_divide(n_raster_resp, n_class),
            "mean_fade_in_response": float(np.nanmean(class_fade)) if n_class else np.nan,
            "median_fade_in_response": float(np.nanmedian(class_fade)) if n_class else np.nan,
            "pct_negative_fade_in": (
                100 * float(np.mean(class_fade[np.isfinite(class_fade)] < 0))
                if np.any(np.isfinite(class_fade)) else np.nan
            ),
            "std_fade_in_response": (
                float(np.nanstd(class_fade, ddof=1)) if np.sum(np.isfinite(class_fade)) > 1 else np.nan
            ),
            "mean_fade_in_vs_fade_out_selectivity": (
                float(np.nanmean(class_fade_selectivity)) if np.any(np.isfinite(class_fade_selectivity)) else np.nan
            ),
            "std_fade_in_vs_fade_out_selectivity": (
                float(np.nanstd(class_fade_selectivity, ddof=1)) if np.sum(np.isfinite(class_fade_selectivity)) > 1 else np.nan
            ),
            "mean_fade_in_vs_best_am_selectivity": (
                float(np.nanmean(class_fade_bestam_selectivity)) if np.any(np.isfinite(class_fade_bestam_selectivity)) else np.nan
            ),
            "std_fade_in_vs_best_am_selectivity": (
                float(np.nanstd(class_fade_bestam_selectivity, ddof=1)) if np.sum(np.isfinite(class_fade_bestam_selectivity)) > 1 else np.nan
            ),
            "mean_am_rate_lifetime_sparseness": (
                float(np.nanmean(class_am_sparseness)) if np.any(np.isfinite(class_am_sparseness)) else np.nan
            ),
            "std_am_rate_lifetime_sparseness": (
                float(np.nanstd(class_am_sparseness, ddof=1)) if np.sum(np.isfinite(class_am_sparseness)) > 1 else np.nan
            ),
            "mean_looming_score_raster_responsive": (
                float(np.nanmean(looming_score[class_mask & raster_responsive]))
                if np.any(class_mask & raster_responsive) else np.nan
            ),
        }
        for rate_index, rate in enumerate(possible_am_rates):
            vals = am_condition_responses[class_mask, rate_index]
            class_summary[f"mean_am_{rate:g}Hz"] = (
                float(np.nanmean(vals)) if np.any(np.isfinite(vals)) else np.nan
            )
        class_summary_rows.append(class_summary)
    class_summary_df = pd.DataFrame(class_summary_rows)
    class_summary_df.to_csv(session_output_dir / "session_class_summary.csv", index=False)

    # Save a small session metadata/results JSON.
    session_summary_json = {
        "metadata": meta,
        "suite2p_dir": str(suite2p_dir),
        "n_total_suite2p_rois": int(data2p.roiF.shape[0]),
        "n_analysis_cells": n_analysis_cells,
        "n_green": n_green,
        "n_yellow": n_yellow,
        "n_excluded": n_excluded,
        "n_red_anatomical": n_red_anatomical,
        "legacy_chan2_score_used_for_exclusion": False,
        "cellpose_diameter": cellpose_diameter,
        "possible_am_rates": possible_am_rates,
        "condition_names": condition_names,
        "n_trials_each_condition": n_trials_each_condition,
        "alignment_note": alignment_note,
        "alignment_offset": alignment_diagnostics["alignment_offset"],
        "n_extra_imaging_events": alignment_diagnostics["n_extra_imaging_events"],
        "n_extra_before": alignment_diagnostics["n_extra_before"],
        "n_extra_after": alignment_diagnostics["n_extra_after"],
        "alignment_timing_mae_s": alignment_diagnostics["timing_mae_s"],
        "alignment_timing_max_abs_error_s": alignment_diagnostics["timing_max_abs_error_s"],
        "n_imaging_events": n_imaging_events,
        "n_behavior_trials": n_behavior_trials,
        "n_valid_imaging_events": int(np.sum(valid_events)),
    }
    save_json(session_output_dir / "session_summary.json", session_summary_json)

    trace_records: list[dict[str, Any]] = []
    for i in np.flatnonzero(classified_mask):
        trace_records.append(
            {
                "subject": subject,
                "date": date,
                "session": session,
                "session_key": f"{date}_{session}",
                "analysis_index": int(i),
                "suite2p_roi": int(cell_roi_indices[i]),
                "cell_class": str(cell_class[i]),
                "fade_selectivity": float(fade_selectivity[i]),
                "am_rate_lifetime_sparseness": float(am_rate_lifetime_sparseness[i]),
                "raster_responsive": bool(raster_responsive[i]),
                "sound_responsive_fdr": bool(sound_responsive_cells[i]),
                "tvec": np.asarray(tvec, dtype=float),
                "fade_in_trace": np.asarray(mean_fade_in_trace[i], dtype=float),
                "fade_out_trace": np.asarray(mean_fade_out_trace[i], dtype=float),
            }
        )

    return {
        "meta": meta,
        "cell_df": cell_df,
        "class_summary_df": class_summary_df,
        "trace_records": trace_records,
        "possible_am_rates": np.asarray(possible_am_rates, dtype=float),
        "condition_names": condition_names,
        "condition_responses": condition_responses,
        "cell_class": cell_class,
        "classified_mask": classified_mask,
        "raster_responsive": raster_responsive,
    }



# =============================================================================
# SOUND-RESPONSIVENESS FIGURES
# =============================================================================

def sound_responsiveness_figure(
    cell_df: pd.DataFrame,
    output_path: Path,
    title: str,
) -> None:
    """Notebook-equivalent responsive/non-responsive figure.

    Panel A: each classified cell's mean all-sound response. Phenotype is color;
    non-significant cells are circles, significant increases are triangles up,
    and significant decreases are triangles down.
    Panel B: GREEN/YELLOW percentages responsive, excited, and suppressed.
    """
    df = cell_df[cell_df["cell_class"].isin(["green", "yellow"])].copy().reset_index(drop=True)
    if len(df) == 0:
        return

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8), constrained_layout=True)
    ax = axes[0]
    x = np.arange(len(df), dtype=float)
    response = df["mean_sound_response"].to_numpy(dtype=float)
    cls = df["cell_class"].to_numpy(dtype=object)
    responsive = df["sound_responsive_fdr"].astype(bool).to_numpy()
    excited = df["sound_excited_fdr"].astype(bool).to_numpy()
    suppressed = df["sound_suppressed_fdr"].astype(bool).to_numpy()

    for class_name, color, edge in [
        ("green", GREEN_COLOR, "none"),
        ("yellow", YELLOW_COLOR, "black"),
    ]:
        cmask = cls == class_name
        masks = [
            (cmask & ~responsive, "o", 25, 0.30),
            (cmask & excited, "^", 48, 0.92),
            (cmask & suppressed, "v", 48, 0.92),
        ]
        for mask, marker_style, size, alpha in masks:
            valid = mask & np.isfinite(response)
            ax.scatter(
                x[valid], response[valid], s=size, marker=marker_style,
                color=color, alpha=alpha, edgecolors=edge,
                linewidth=0.35 if class_name == "yellow" else 0.0,
            )
    ax.axhline(0, color="black", ls=":", lw=1)
    ax.set_xlabel("Cell index in plotted dataset")
    ax.set_ylabel("Mean sound-evoked\nbaseline-subtracted dF/F")
    pct = 100.0 * np.mean(responsive) if len(responsive) else np.nan
    ax.set_title(f"Reliable sound responses\n{pct:.1f}% responsive overall")
    handles = [
        Line2D([0], [0], marker="o", linestyle="None", markerfacecolor=GREEN_COLOR,
               markeredgecolor=GREEN_COLOR, markersize=7, label="Green"),
        Line2D([0], [0], marker="o", linestyle="None", markerfacecolor=YELLOW_COLOR,
               markeredgecolor="black", markersize=7, label="Yellow"),
        Line2D([0], [0], marker="o", linestyle="None", color="black", markersize=6,
               label="Not significant"),
        Line2D([0], [0], marker="^", linestyle="None", color="black", markersize=7,
               label="Significant increase"),
        Line2D([0], [0], marker="v", linestyle="None", color="black", markersize=7,
               label="Significant decrease"),
    ]
    ax.legend(handles=handles, frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    m_all, se_all = mean_sem(response)
    important = [0.0, m_all]
    if np.isfinite(se_all):
        important += [m_all - se_all, m_all + se_all]
    apply_robust_y_limits(ax, [response], important_values=important, reference_values=[0.0])

    ax = axes[1]
    categories = ["Responsive", "Excited", "Suppressed"]
    xcat = np.arange(3)
    width = 0.36
    percentages = {}
    counts = {}
    totals = {}
    for class_name in ["green", "yellow"]:
        cdf = df[df["cell_class"] == class_name]
        total = len(cdf)
        vals = np.array([
            np.sum(cdf["sound_responsive_fdr"].astype(bool)),
            np.sum(cdf["sound_excited_fdr"].astype(bool)),
            np.sum(cdf["sound_suppressed_fdr"].astype(bool)),
        ], dtype=int)
        counts[class_name] = vals
        totals[class_name] = total
        percentages[class_name] = 100.0 * vals / total if total else np.full(3, np.nan)

    bars_g = ax.bar(xcat - width/2, percentages["green"], width=width,
                    color=GREEN_COLOR, alpha=0.82, label=f"Green (n={totals['green']})")
    bars_y = ax.bar(xcat + width/2, percentages["yellow"], width=width,
                    color=YELLOW_COLOR, edgecolor="black", linewidth=0.5,
                    alpha=0.87, label=f"Yellow (n={totals['yellow']})")
    for bars, class_name in [(bars_g, "green"), (bars_y, "yellow")]:
        for bar, count in zip(bars, counts[class_name]):
            h = bar.get_height()
            if np.isfinite(h):
                ax.text(bar.get_x()+bar.get_width()/2, h+1, str(int(count)),
                        ha="center", va="bottom", fontsize=8)

    g_resp = int(counts["green"][0])
    y_resp = int(counts["yellow"][0])
    contingency = [
        [g_resp, totals["green"] - g_resp],
        [y_resp, totals["yellow"] - y_resp],
    ]
    try:
        fisher = stats.fisher_exact(contingency)
        fisher_p = float(fisher.pvalue)
    except Exception:
        fisher_p = np.nan
    ptxt = "n/a" if not np.isfinite(fisher_p) else f"{fisher_p:.3g}"
    ax.set_xticks(xcat, categories)
    ax.set_ylabel("Cells (%)")
    ax.set_title(f"Sound responsiveness by cell class\nFisher responsive fraction p={ptxt}")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    ymax = np.nanmax(np.concatenate([percentages["green"], percentages["yellow"]]))
    ax.set_ylim(0, max(10, float(ymax) + 10))

    axes[0].text(-0.10, 1.03, "A", transform=axes[0].transAxes, fontsize=16, fontweight="bold")
    axes[1].text(-0.10, 1.03, "B", transform=axes[1].transAxes, fontsize=16, fontweight="bold")
    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def sound_responsiveness_session_mean_only(
    cell_df: pd.DataFrame,
    output_path: Path,
    title: str,
) -> None:
    """Session mean +/- SD plus overall mean +/- SEM for response fractions."""
    metrics = [
        ("sound_responsive_fdr", "Responsive"),
        ("sound_excited_fdr", "Excited"),
        ("sound_suppressed_fdr", "Suppressed"),
    ]
    classified = cell_df[cell_df["cell_class"].isin(["green", "yellow"])].copy()
    fig, ax = plt.subplots(figsize=(11.5, 7.0))
    x = np.arange(len(metrics), dtype=float)
    offsets = {"green": -0.12, "yellow": 0.12}
    colors = {"green": GREEN_COLOR, "yellow": YELLOW_COLOR}
    session_offsets = np.linspace(-0.045, 0.045, max(classified["session_key"].nunique(), 1))
    all_bounds = []

    for class_name in ["green", "yellow"]:
        cdf = classified[classified["cell_class"] == class_name]
        session_keys = list(dict.fromkeys(cdf["session_key"].tolist()))
        session_means_by_metric = [[] for _ in metrics]
        for s_idx, session_key in enumerate(session_keys):
            sdf = cdf[cdf["session_key"] == session_key]
            for m_idx, (metric, _) in enumerate(metrics):
                vals = 100.0 * sdf[metric].astype(float).to_numpy()
                mean, sd, _ = _mean_sd(vals)
                session_means_by_metric[m_idx].append(mean)
                xx = x[m_idx] + offsets[class_name] + session_offsets[min(s_idx, len(session_offsets)-1)]
                ax.errorbar(
                    xx, mean, yerr=sd if np.isfinite(sd) else None,
                    marker="o", markersize=3.6, lw=0, elinewidth=0.8, capsize=2.5,
                    color=colors[class_name], alpha=0.28, zorder=2,
                )
                if np.isfinite(mean):
                    all_bounds.append(mean)
                    if np.isfinite(sd):
                        all_bounds.extend([mean-sd, mean+sd])
        overall_means, overall_sems, overall_ns = [], [], []
        for vals in session_means_by_metric:
            m, _, se, n = mean_sd_sem(vals)
            overall_means.append(m); overall_sems.append(se); overall_ns.append(n)
        xpos = x + offsets[class_name]
        ax.errorbar(
            xpos, overall_means, yerr=overall_sems, marker="o", markersize=8,
            lw=2.8, elinewidth=2.4, capsize=5.5,
            color=colors[class_name], alpha=1.0, label=f"{class_name.capitalize()} overall",
            zorder=5,
        )
        for xx, m, se, n in zip(xpos, overall_means, overall_sems, overall_ns):
            annotate_mean_sem_point(ax, xx, m, se, n, color=colors[class_name], digits=2, fontsize=7)
            if np.isfinite(m):
                all_bounds.append(m)
                if np.isfinite(se):
                    all_bounds.extend([m-se, m+se])

    ax.set_xticks(x, [name for _, name in metrics])
    ax.set_ylabel("Cells (%)")
    ax.set_title("Thin/light: individual session mean ± SD; thick/dark: overall mean ± SEM")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    apply_robust_y_limits(ax, [all_bounds], important_values=all_bounds)
    fig.suptitle(title, fontsize=14)
    fig.subplots_adjust(top=0.84, bottom=0.12)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# COMBINED PLOTS
# =============================================================================

def plot_paired_cell_population(ax, a, b, label_a, label_b, title, line_color):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    valid = np.isfinite(a) & np.isfinite(b)
    a = a[valid]
    b = b[valid]
    rng = np.random.default_rng(1234)
    ja = rng.uniform(-0.05, 0.05, len(a))
    jb = rng.uniform(-0.05, 0.05, len(b))
    for va, vb, xa, xb in zip(a, b, ja, jb):
        ax.plot([0 + xa, 1 + xb], [va, vb], color=line_color, alpha=0.10, lw=0.6)
    ax.scatter(np.zeros(len(a)) + ja, a, s=12, alpha=0.35, color=FADE_IN_COLOR, edgecolors="none")
    comparison_color = FADE_OUT_COLOR if label_b == "Fade-out" else BEST_AM_COLOR
    ax.scatter(np.ones(len(b)) + jb, b, s=12, alpha=0.35, color=comparison_color, edgecolors="none")
    ma, sea = mean_sem(a)
    mb, seb = mean_sem(b)
    ax.errorbar([0, 1], [ma, mb], yerr=[sea, seb], fmt="o-", color="black", lw=2, capsize=4)
    ax.axhline(0, color="black", ls=":", lw=1)
    ax.set_xticks([0, 1], [label_a, label_b])
    ax.set_title(title)
    ax.set_ylabel("Mean baseline-subtracted dF/F")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)

    important = [ma, mb, 0.0]
    if np.isfinite(sea):
        important.extend([ma - sea, ma + sea])
    if np.isfinite(seb):
        important.extend([mb - seb, mb + seb])
    apply_robust_y_limits(
        ax,
        [a, b],
        important_values=important,
        reference_values=[0.0],
    )





def _session_mean_sd_matrix(df: pd.DataFrame, columns: list[str]):
    records = []
    for session_key, sdf in df.groupby("session_key", sort=True):
        means, sds = [], []
        for col in columns:
            vals = sdf[col].to_numpy(dtype=float) if col in sdf else np.array([])
            m, sd, _ = _mean_sd(vals)
            means.append(m); sds.append(sd)
        records.append((str(session_key), np.asarray(means, float), np.asarray(sds, float)))
    return records


def _plot_session_profile_mean_sd(
    ax,
    df: pd.DataFrame,
    columns: list[str],
    labels: list[str],
    color,
    title: str,
    *,
    reference_zero: bool = True,
    x_values: np.ndarray | None = None,
) -> None:
    """Thin/light session mean +/- SD; thick/dark overall session-mean +/- SEM."""
    x = np.arange(len(columns), dtype=float) if x_values is None else np.asarray(x_values, dtype=float)
    records = _session_mean_sd_matrix(df, columns)
    session_mean_rows = []
    display = []
    for _, means, sds in records:
        session_mean_rows.append(means)
        ax.errorbar(
            x, means, yerr=sds, marker="o", markersize=3.2,
            lw=0.9, elinewidth=0.7, capsize=2.0,
            color=color, alpha=0.22, zorder=2,
        )
        display.extend(finite_values(means).tolist())
        valid = np.isfinite(means) & np.isfinite(sds)
        display.extend((means[valid]-sds[valid]).tolist())
        display.extend((means[valid]+sds[valid]).tolist())
    matrix = np.vstack(session_mean_rows) if session_mean_rows else np.empty((0, len(columns)))
    overall_mean = np.full(len(columns), np.nan)
    overall_sem = np.full(len(columns), np.nan)
    overall_n = np.zeros(len(columns), dtype=int)
    for j in range(len(columns)):
        m, _, se, n = mean_sd_sem(matrix[:, j] if len(matrix) else np.array([]))
        overall_mean[j] = m; overall_sem[j] = se; overall_n[j] = n
    ax.errorbar(
        x, overall_mean, yerr=overall_sem, marker="o", markersize=8,
        lw=3.0, elinewidth=2.4, capsize=5,
        color=color, alpha=1.0, zorder=5,
    )
    for xx, m, se, n in zip(x, overall_mean, overall_sem, overall_n):
        annotate_mean_sem_point(ax, xx, m, se, int(n), color=color, digits=4, fontsize=6.3)
    if reference_zero:
        ax.axhline(0, color="black", ls=":", lw=0.9)
    ax.set_xticks(x, labels, rotation=45 if len(labels) > 4 else 0, ha="right" if len(labels) > 4 else "center")
    ax.set_title(title + "\nlight: session mean ± SD; dark: overall mean ± SEM")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    refs = [0.0] if reference_zero else None
    apply_robust_y_limits(ax, [display, overall_mean], important_values=np.r_[overall_mean, overall_mean-overall_sem, overall_mean+overall_sem], reference_values=refs)


def _plot_session_class_metric_mean_sd(
    ax,
    df: pd.DataFrame,
    metric: str,
    ylabel: str,
    title: str,
    p_value: float | None = None,
    reference: float | None = None,
    transform=None,
) -> None:
    """GREEN/YELLOW metric with each session mean +/- SD and overall +/- SEM."""
    colors = {"green": GREEN_COLOR, "yellow": YELLOW_COLOR}
    class_x = {"green": 0.0, "yellow": 1.0}
    session_keys = sorted(df["session_key"].dropna().astype(str).unique())
    jitter = np.linspace(-0.055, 0.055, max(len(session_keys), 1))
    session_means = {"green": [], "yellow": []}
    display = []
    paired_means = {}
    for s_idx, session_key in enumerate(session_keys):
        paired_means[session_key] = {}
        for class_name in ["green", "yellow"]:
            sdf = df[(df["session_key"].astype(str) == session_key) & (df["cell_class"] == class_name)]
            if metric not in sdf:
                continue
            vals = sdf[metric].to_numpy(dtype=float)
            if transform is not None:
                vals = transform(vals)
            mean, sd, _ = _mean_sd(vals)
            session_means[class_name].append(mean)
            paired_means[session_key][class_name] = mean
            xx = class_x[class_name] + jitter[min(s_idx, len(jitter)-1)]
            ax.errorbar(
                xx, mean, yerr=sd if np.isfinite(sd) else None,
                marker="o", markersize=3.5, lw=0, elinewidth=0.75, capsize=2,
                color=colors[class_name], alpha=0.25, zorder=2,
            )
            if np.isfinite(mean):
                display.append(mean)
                if np.isfinite(sd): display.extend([mean-sd, mean+sd])
    for session_key, pair in paired_means.items():
        if np.isfinite(pair.get("green", np.nan)) and np.isfinite(pair.get("yellow", np.nan)):
            ax.plot([0, 1], [pair["green"], pair["yellow"]], color="0.65", alpha=0.18, lw=0.7, zorder=1)

    overall = {}
    for class_name in ["green", "yellow"]:
        m, _, se, n = mean_sd_sem(session_means[class_name])
        overall[class_name] = (m, se, n)
        x = class_x[class_name]
        ax.errorbar(
            x, m, yerr=se if np.isfinite(se) else None,
            marker="o", markersize=9, lw=0, elinewidth=2.6, capsize=6,
            color=colors[class_name], alpha=1.0, zorder=6,
        )
        annotate_mean_sem_point(ax, x, m, se, n, color=colors[class_name], digits=4, fontsize=7)
    if np.isfinite(overall["green"][0]) and np.isfinite(overall["yellow"][0]):
        ax.plot([0, 1], [overall["green"][0], overall["yellow"][0]], color="black", lw=2.2, alpha=0.75, zorder=4)
    if reference is not None:
        ax.axhline(reference, color="black", ls=":", lw=1)
    ptxt = "n/a" if p_value is None else f"{p_value:.3g}"
    ax.set_title(title + f"\npaired-session p={ptxt}\nlight: session mean ± SD; dark: overall mean ± SEM")
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    imp = []
    for m,se,_ in overall.values():
        if np.isfinite(m):
            imp.append(m)
            if np.isfinite(se): imp.extend([m-se,m+se])
    apply_robust_y_limits(ax, [display], important_values=imp, reference_values=None if reference is None else [reference])


def _plot_session_paired_condition_points(ax, df, col_a, col_b, label_a, label_b, color, title):
    n_sessions = 0
    display = []
    for session_key, sdf in df.groupby("session_key", sort=True):
        a = finite_values(sdf[col_a]) if col_a in sdf else np.array([])
        b = finite_values(sdf[col_b]) if col_b in sdf else np.array([])
        ma, sda, _ = _mean_sd(a)
        mb, sdb, _ = _mean_sd(b)
        if not (np.isfinite(ma) and np.isfinite(mb)):
            continue
        n_sessions += 1
        ax.plot([0,1], [ma,mb], color=color, alpha=0.26, lw=0.9, zorder=1)
        ax.errorbar([0,1], [ma,mb], yerr=[sda if np.isfinite(sda) else np.nan, sdb if np.isfinite(sdb) else np.nan],
                    fmt='o', markersize=4.0, lw=0, elinewidth=0.8, capsize=2.2,
                    color=color, alpha=0.38, zorder=2,
                    markeredgecolor='black' if color == YELLOW_COLOR else 'none', markeredgewidth=0.25)
        display.extend([ma, mb])
        if np.isfinite(sda): display.extend([ma-sda, ma+sda])
        if np.isfinite(sdb): display.extend([mb-sdb, mb+sdb])
    ax.axhline(0, color='black', ls=':', lw=0.8)
    ax.set_xticks([0,1], [label_a,label_b])
    ax.set_ylabel('Session mean baseline-subtracted dF/F')
    ax.set_title(f"{title}\npoints = session means ± SD; n={n_sessions}")
    ax.grid(axis='y', alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    apply_robust_y_limits(ax, [display], reference_values=[0.0])


def _plot_session_class_metric_points(ax, df, metric, ylabel, title, p_value=None, reference=None):
    colors={"green":GREEN_COLOR,"yellow":YELLOW_COLOR}
    display=[]
    for session_key in sorted(df["session_key"].dropna().astype(str).unique()):
        pair={}
        pair_sd={}
        for class_name in ["green","yellow"]:
            sdf=df[(df["session_key"].astype(str)==session_key)&(df["cell_class"]==class_name)]
            vals=finite_values(sdf[metric]) if metric in sdf else np.array([])
            m,sd,_=_mean_sd(vals)
            pair[class_name]=m; pair_sd[class_name]=sd
            if np.isfinite(m):
                xx=0 if class_name=='green' else 1
                ax.errorbar(xx,m,yerr=sd if np.isfinite(sd) else None,fmt='o',markersize=4.0,
                            lw=0,elinewidth=0.8,capsize=2.2,color=colors[class_name],alpha=0.38,zorder=2,
                            markeredgecolor='black' if class_name=='yellow' else 'none', markeredgewidth=0.25)
                display.append(m)
                if np.isfinite(sd): display.extend([m-sd,m+sd])
        g=pair.get('green',np.nan); y=pair.get('yellow',np.nan)
        if np.isfinite(g) and np.isfinite(y):
            ax.plot([0,1],[g,y],color='0.65',alpha=0.28,lw=0.9,zorder=1)
    if reference is not None:
        ax.axhline(reference,color='black',ls=':',lw=1)
    ptxt='n/a' if p_value is None else f"{p_value:.3g}"
    ax.set_xticks([0,1],["Green","Yellow"])
    ax.set_ylabel(ylabel)
    ax.set_title(title+f"\npoints = session means ± SD | paired p={ptxt}")
    ax.grid(axis='y',alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    apply_robust_y_limits(ax,[display],reference_values=None if reference is None else [reference])


def _plot_cell_paired_condition_points(ax, df, col_a, col_b, label_a, label_b, color, title):
    a = finite_values(df[col_a]) if col_a in df else np.array([])
    b = finite_values(df[col_b]) if col_b in df else np.array([])
    display=[]
    rng=np.random.default_rng(1001)
    if len(a):
        x0=np.full(len(a),0.0)+rng.uniform(-0.10,0.10,len(a))
        ax.scatter(x0,a,color=color,alpha=0.16,s=14,edgecolors='none',zorder=1)
        m,se,_=mean_sd_sem(a)
        ax.errorbar(0,m,yerr=se if np.isfinite(se) else None,fmt='o',markersize=7.5,elinewidth=2.0,capsize=5,
                    color=color,lw=0,zorder=3)
        annotate_mean_sem_point(ax,0,m,se,len(a),color=color,digits=4,fontsize=6.2)
        display.extend(a.tolist())
        if np.isfinite(m):
            display.extend([m])
            if np.isfinite(se): display.extend([m-se,m+se])
    if len(b):
        x1=np.full(len(b),1.0)+rng.uniform(-0.10,0.10,len(b))
        ax.scatter(x1,b,color=color,alpha=0.16,s=14,edgecolors='none',zorder=1)
        m,se,_=mean_sd_sem(b)
        ax.errorbar(1,m,yerr=se if np.isfinite(se) else None,fmt='o',markersize=7.5,elinewidth=2.0,capsize=5,
                    color=color,lw=0,zorder=3)
        annotate_mean_sem_point(ax,1,m,se,len(b),color=color,digits=4,fontsize=6.2)
        display.extend(b.tolist())
        if np.isfinite(m):
            display.extend([m])
            if np.isfinite(se): display.extend([m-se,m+se])
    ax.axhline(0, color='black', ls=':', lw=0.8)
    ax.set_xticks([0,1], [label_a,label_b])
    ax.set_ylabel('Cell baseline-subtracted dF/F')
    ax.set_title(f"{title}\npoints = cells; dark = pooled mean ± SEM")
    ax.grid(axis='y', alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    apply_robust_y_limits(ax, [display], reference_values=[0.0])


def _plot_cell_class_metric_points(ax, df, metric, ylabel, title, p_value=None, reference=None):
    colors={"green":GREEN_COLOR,"yellow":YELLOW_COLOR}
    rng=np.random.default_rng(1002)
    display=[]
    for pos,class_name in enumerate(['green','yellow']):
        sdf=df[df['cell_class']==class_name]
        vals=finite_values(sdf[metric]) if metric in sdf else np.array([])
        if len(vals):
            x=np.full(len(vals),float(pos))+rng.uniform(-0.10,0.10,len(vals))
            ax.scatter(x,vals,color=colors[class_name],alpha=0.16,s=14,edgecolors='none',zorder=1)
            m,se,_=mean_sd_sem(vals)
            ax.errorbar(pos,m,yerr=se if np.isfinite(se) else None,fmt='o',markersize=7.5,elinewidth=2.0,capsize=5,
                        color=colors[class_name],lw=0,zorder=3,
                        markeredgecolor='black' if class_name=='yellow' else 'none',markeredgewidth=0.25)
            annotate_mean_sem_point(ax,pos,m,se,len(vals),color=colors[class_name],digits=4,fontsize=6.2)
            display.extend(vals.tolist())
            if np.isfinite(m):
                display.extend([m])
                if np.isfinite(se): display.extend([m-se,m+se])
    if reference is not None:
        ax.axhline(reference,color='black',ls=':',lw=1)
    ptxt='n/a' if p_value is None else f"{p_value:.3g}"
    ax.set_xticks([0,1],["Green","Yellow"])
    ax.set_ylabel(ylabel)
    ax.set_title(title+f"\npoints = cells | pooled-cell p={ptxt}")
    ax.grid(axis='y',alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    apply_robust_y_limits(ax,[display],reference_values=None if reference is None else [reference])

def _interp_trace_to_common(tvec, trace, common_t):
    tvec=np.asarray(tvec,float); trace=np.asarray(trace,float)
    valid=np.isfinite(tvec)&np.isfinite(trace)
    if np.sum(valid)<2:
        return np.full(len(common_t),np.nan)
    order=np.argsort(tvec[valid])
    return np.interp(common_t,tvec[valid][order],trace[valid][order],left=np.nan,right=np.nan)


def _plot_top_selectivity_raster(ax, trace_records, class_name: str, title: str):
    candidates=[r for r in trace_records if r.get("cell_class")==class_name and np.isfinite(r.get("fade_selectivity",np.nan))]
    candidates.sort(key=lambda r: abs(float(r["fade_selectivity"])), reverse=True)
    candidates=candidates[:N_COMBINED_RASTER_CELLS_PER_CLASS]
    if not candidates:
        ax.text(0.5,0.5,f"No {class_name} cells",transform=ax.transAxes,ha="center",va="center")
        ax.set_title(title); return None
    common_t=np.linspace(TIME_RANGE[0],TIME_RANGE[1],180)
    rows=[]
    for r in candidates:
        fi=_interp_trace_to_common(r["tvec"],r["fade_in_trace"],common_t)
        fo=_interp_trace_to_common(r["tvec"],r["fade_out_trace"],common_t)
        row=np.r_[fi,fo]
        scale=np.nanmax(np.abs(row)) if np.any(np.isfinite(row)) else np.nan
        if np.isfinite(scale) and scale>0: row=row/scale
        rows.append(row)
    mat=np.vstack(rows)
    im=ax.imshow(mat,aspect="auto",interpolation="nearest",cmap="coolwarm",vmin=-1,vmax=1)
    n=len(common_t); onset=int(np.argmin(np.abs(common_t)))
    ax.axvline(n-0.5,color="black",lw=1.3)
    ax.axvline(onset-0.5,color="black",ls=":",lw=0.8)
    ax.axvline(n+onset-0.5,color="black",ls=":",lw=0.8)
    ax.set_xticks([n/2,1.5*n],["Fade-in","Fade-out"])
    ax.set_ylabel("Cells ranked by |FI/FO SI|")
    ax.set_title(f"{title}\ntop {len(candidates)} across sessions")
    return im


def _plot_am_profiles_sessions_and_top_cells(ax, df: pd.DataFrame, am_rates: list[float]) -> None:
    x=np.arange(len(am_rates),dtype=float)
    display=[]
    for class_name,color in [("green",GREEN_COLOR),("yellow",YELLOW_COLOR)]:
        cdf=df[df["cell_class"]==class_name]
        for session_key,sdf in cdf.groupby("session_key",sort=True):
            cols=[f"am_response_{r:g}Hz" for r in am_rates]
            matrix=np.column_stack([sdf[col].to_numpy(float) if col in sdf else np.full(len(sdf),np.nan) for col in cols]) if cols else np.empty((len(sdf),0))
            if matrix.size==0: continue
            # Top five cells in this session/class by AM lifetime sparseness.
            ranks=sdf["am_rate_lifetime_sparseness"].to_numpy(float)
            valid_rank=np.flatnonzero(np.isfinite(ranks))
            valid_rank=valid_rank[np.argsort(ranks[valid_rank])[::-1]][:N_AM_EXAMPLE_CELLS_PER_SESSION_CLASS]
            for ridx in valid_rank:
                ax.plot(x,matrix[ridx],color=color,alpha=0.18,lw=0.9,ls="--",zorder=1)
                display.extend(finite_values(matrix[ridx]).tolist())
            mean=np.nanmean(matrix,axis=0)
            ax.plot(x,mean,color=color,alpha=0.72,lw=2.0,ls="-",marker="o",markersize=3.5,zorder=3)
            display.extend(finite_values(mean).tolist())
    ax.axhline(0,color="black",ls=":",lw=0.9)
    ax.set_xticks(x,[f"{r:g}" for r in am_rates])
    ax.set_xlabel("AM rate (Hz)")
    ax.set_ylabel("Baseline-subtracted dF/F")
    ax.set_title("AM-rate response profiles\nsolid/darker = session means; dashed/dim = top 5 cells/session by lifetime sparseness")
    handles=[
        Line2D([0],[0],color=GREEN_COLOR,lw=2,label="Green session mean"),
        Line2D([0],[0],color=YELLOW_COLOR,lw=2,label="Yellow session mean"),
        Line2D([0],[0],color="0.35",lw=1,ls="--",alpha=0.5,label="Individual high-sparseness cell"),
    ]
    ax.legend(handles=handles,frameon=False,fontsize=8)
    ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    apply_robust_y_limits(ax,[display],reference_values=[0.0])

def combined_sound_response_summary(
    cell_df: pd.DataFrame,
    trace_records: list[dict[str, Any]],
    am_rates: list[float],
    session_stats: dict[str, Any],
    output_path: Path,
    title: str,
) -> None:
    """Combined summary using session means as the displayed replicate."""
    classified=cell_df[cell_df["cell_class"].isin(["green","yellow"])].copy()
    green=classified[classified["cell_class"]=="green"]
    yellow=classified[classified["cell_class"]=="yellow"]

    fig=plt.figure(figsize=(25,22))
    gs=fig.add_gridspec(4,3,height_ratios=[1,1,1.2,1.25],hspace=0.42,wspace=0.30)
    axes=[[fig.add_subplot(gs[r,c]) for c in range(3)] for r in range(3)]
    ax_am=fig.add_subplot(gs[3,:])

    _plot_session_paired_condition_points(axes[0][0],green,"fade_in_response","fade_out_response","Fade-in","Fade-out",GREEN_COLOR,"Green")
    _plot_session_paired_condition_points(axes[0][1],yellow,"fade_in_response","fade_out_response","Fade-in","Fade-out",YELLOW_COLOR,"Yellow")
    _plot_session_class_metric_points(
        axes[0][2],classified,"fade_in_vs_fade_out_selectivity","FI/FO selectivity index",
        r"$SI_{FI/FO}=(R_{FI}-R_{FO})/(R_{FI}+R_{FO})$",
        session_stats.get("fade_selectivity_green_vs_yellow",{}).get("p"),reference=0.0)

    _plot_session_paired_condition_points(axes[1][0],green,"fade_in_response","best_am_response","Fade-in","Best AM",GREEN_COLOR,"Green")
    _plot_session_paired_condition_points(axes[1][1],yellow,"fade_in_response","best_am_response","Fade-in","Best AM",YELLOW_COLOR,"Yellow")
    _plot_session_class_metric_points(
        axes[1][2],classified,"fade_in_vs_best_am_selectivity","FI/best-AM selectivity index",
        r"$SI_{FI/AM}=(R_{FI}-R_{bestAM})/(R_{FI}+R_{bestAM})$",
        session_stats.get("fade_bestam_selectivity_green_vs_yellow",{}).get("p"),reference=0.0)

    im_g=_plot_top_selectivity_raster(axes[2][0],trace_records,"green","GREEN FI/FO raster")
    im_y=_plot_top_selectivity_raster(axes[2][1],trace_records,"yellow","YELLOW FI/FO raster")
    im=im_g if im_g is not None else im_y
    if im is not None:
        cbar=fig.colorbar(im,ax=[axes[2][0],axes[2][1]],fraction=0.035,pad=0.02)
        cbar.set_label("Response / max absolute response per cell")
    _plot_session_class_metric_points(
        axes[2][2],classified,"am_rate_lifetime_sparseness","AM lifetime sparseness",
        "AM-rate selectivity (lifetime sparseness)",
        session_stats.get("am_rate_lifetime_sparseness_green_vs_yellow",{}).get("p"),reference=None)

    _plot_am_profiles_sessions_and_top_cells(ax_am,classified,am_rates)
    fig.text(0.5,0.012,_equation_footer(),ha="center",va="bottom",fontsize=11)
    fig.suptitle(title+"\nAll comparison points are session means",fontsize=15,y=0.995)
    fig.subplots_adjust(top=0.95,bottom=0.06)
    fig.savefig(output_path,dpi=300,bbox_inches="tight")
    plt.close(fig)


def combined_sound_response_summary_cell_points(
    cell_df: pd.DataFrame,
    trace_records: list[dict[str, Any]],
    am_rates: list[float],
    pooled_stats: dict[str, Any],
    output_path: Path,
    title: str,
) -> None:
    """Combined summary variant using individual cells as the displayed points."""
    classified=cell_df[cell_df["cell_class"].isin(["green","yellow"])].copy()
    green=classified[classified["cell_class"]=="green"]
    yellow=classified[classified["cell_class"]=="yellow"]

    fig=plt.figure(figsize=(25,22))
    gs=fig.add_gridspec(4,3,height_ratios=[1,1,1.2,1.25],hspace=0.42,wspace=0.30)
    axes=[[fig.add_subplot(gs[r,c]) for c in range(3)] for r in range(3)]
    ax_am=fig.add_subplot(gs[3,:])

    _plot_cell_paired_condition_points(axes[0][0],green,"fade_in_response","fade_out_response","Fade-in","Fade-out",GREEN_COLOR,"Green")
    _plot_cell_paired_condition_points(axes[0][1],yellow,"fade_in_response","fade_out_response","Fade-in","Fade-out",YELLOW_COLOR,"Yellow")
    _plot_cell_class_metric_points(
        axes[0][2],classified,"fade_in_vs_fade_out_selectivity","FI/FO selectivity index",
        r"$SI_{FI/FO}=(R_{FI}-R_{FO})/(R_{FI}+R_{FO})$",
        pooled_stats.get("fade_selectivity_green_vs_yellow",{}).get("p"),reference=0.0)

    _plot_cell_paired_condition_points(axes[1][0],green,"fade_in_response","best_am_response","Fade-in","Best AM",GREEN_COLOR,"Green")
    _plot_cell_paired_condition_points(axes[1][1],yellow,"fade_in_response","best_am_response","Fade-in","Best AM",YELLOW_COLOR,"Yellow")
    _plot_cell_class_metric_points(
        axes[1][2],classified,"fade_in_vs_best_am_selectivity","FI/best-AM selectivity index",
        r"$SI_{FI/AM}=(R_{FI}-R_{bestAM})/(R_{FI}+R_{bestAM})$",
        pooled_stats.get("fade_bestam_selectivity_green_vs_yellow",{}).get("p"),reference=0.0)

    im_g=_plot_top_selectivity_raster(axes[2][0],trace_records,"green","GREEN FI/FO raster")
    im_y=_plot_top_selectivity_raster(axes[2][1],trace_records,"yellow","YELLOW FI/FO raster")
    im=im_g if im_g is not None else im_y
    if im is not None:
        cbar=fig.colorbar(im,ax=[axes[2][0],axes[2][1]],fraction=0.035,pad=0.02)
        cbar.set_label("Response / max absolute response per cell")
    _plot_cell_class_metric_points(
        axes[2][2],classified,"am_rate_lifetime_sparseness","AM lifetime sparseness",
        "AM-rate selectivity (lifetime sparseness)",
        pooled_stats.get("am_rate_lifetime_sparseness_green_vs_yellow",{}).get("p"),reference=None)

    _plot_am_profiles_sessions_and_top_cells(ax_am,classified,am_rates)
    fig.text(0.5,0.012,_equation_footer(),ha="center",va="bottom",fontsize=11)
    fig.suptitle(title+"\nAll comparison points are individual cells",fontsize=15,y=0.995)
    fig.subplots_adjust(top=0.95,bottom=0.06)
    fig.savefig(output_path,dpi=300,bbox_inches="tight")
    plt.close(fig)


def combined_condition_response_plot(cell_df: pd.DataFrame, am_rates: list[float], output_path: Path, title: str) -> None:
    condition_cols = ["fade_in_response", "fade_out_response"] + [f"am_response_{r:g}Hz" for r in am_rates]
    labels = ["Fade-in", "Fade-out"] + [f"AM {r:g}" for r in am_rates]
    x = np.arange(len(condition_cols), dtype=float)
    if len(am_rates):
        x[2:] += 0.7

    fig, axes = plt.subplots(1, 4, figsize=(22, 6), constrained_layout=True)
    groups = [
        ("All plotted cells", cell_df[cell_df["cell_class"].isin(["green", "yellow"])], "black"),
        ("Green", cell_df[cell_df["cell_class"] == "green"], GREEN_COLOR),
        ("Yellow", cell_df[cell_df["cell_class"] == "yellow"], YELLOW_COLOR),
    ]
    rng = np.random.default_rng(31415)
    for ax, (group_name, df, color) in zip(axes[:3], groups):
        display_values = []
        important_values = [0.0]
        for ci, col in enumerate(condition_cols):
            if col not in df:
                continue
            vals = finite_values(df[col])
            if not len(vals):
                continue
            display_values.append(vals)
            jitter = rng.uniform(-0.08, 0.08, len(vals))
            ax.scatter(np.full(len(vals), x[ci]) + jitter, vals, s=10, alpha=0.25,
                       color=color, edgecolors="none")
            m, se = mean_sem(vals)
            ax.errorbar(x[ci], m, yerr=se, fmt="o", color="black", capsize=3)
            important_values.append(m)
            if np.isfinite(se):
                important_values.extend([m - se, m + se])
        ax.axhline(0, color="black", ls=":", lw=1)
        ax.set_xticks(x, labels, rotation=45, ha="right")
        ax.set_title(f"{group_name}\nn={len(df)} cells")
        ax.set_ylabel("Mean baseline-subtracted dF/F")
        ax.grid(axis="y", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
        apply_robust_y_limits(
            ax,
            display_values,
            important_values=important_values,
            reference_values=[0.0],
        )

    ax = axes[3]
    comparison_display_values = []
    comparison_important_values = [0.0]
    for class_name, color, offset in [("green", GREEN_COLOR, -0.05), ("yellow", YELLOW_COLOR, 0.05)]:
        df = cell_df[cell_df["cell_class"] == class_name]
        means, sems = [], []
        for col in condition_cols:
            vals = df[col] if col in df else np.array([])
            finite = finite_values(vals)
            if len(finite):
                comparison_display_values.append(finite)
            m, se = mean_sem(vals)
            means.append(m)
            sems.append(se)
            if np.isfinite(m):
                comparison_important_values.append(m)
                if np.isfinite(se):
                    comparison_important_values.extend([m - se, m + se])
        ax.errorbar(x + offset, means, yerr=sems, marker="o", capsize=4, lw=2,
                    color=color, label=f"{class_name.capitalize()} (n={len(df)})")
    ax.axhline(0, color="black", ls=":", lw=1)
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_title("Green vs yellow mean ± SEM")
    ax.set_ylabel("Mean baseline-subtracted dF/F")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    apply_robust_y_limits(
        ax,
        comparison_display_values,
        important_values=comparison_important_values,
        reference_values=[0.0],
    )
    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)



def combined_condition_response_mean_only(
    cell_df: pd.DataFrame,
    am_rates: list[float],
    output_path: Path,
    title: str,
) -> None:
    """Session mean +/- SD and overall session-mean +/- SEM for sound conditions."""
    df_all=cell_df[cell_df["cell_class"].isin(["green","yellow"])].copy()
    cols=["fade_in_response","fade_out_response"]+[f"am_response_{r:g}Hz" for r in am_rates]
    labels=["Fade-in","Fade-out"]+[f"AM {r:g}" for r in am_rates]
    x=np.arange(len(cols),dtype=float)
    if len(am_rates): x[2:]+=0.7
    fig,axes=plt.subplots(1,4,figsize=(25,7.5))
    _plot_session_profile_mean_sd(axes[0],df_all,cols,labels,"black","All classified cells",x_values=x)
    _plot_session_profile_mean_sd(axes[1],df_all[df_all["cell_class"]=="green"],cols,labels,GREEN_COLOR,"Green",x_values=x)
    _plot_session_profile_mean_sd(axes[2],df_all[df_all["cell_class"]=="yellow"],cols,labels,YELLOW_COLOR,"Yellow",x_values=x)

    ax=axes[3]
    display=[]
    for class_name,color,offset in [("green",GREEN_COLOR,-0.045),("yellow",YELLOW_COLOR,0.045)]:
        cdf=df_all[df_all["cell_class"]==class_name]
        records=_session_mean_sd_matrix(cdf,cols)
        rows=[]
        for _,means,sds in records:
            rows.append(means)
            ax.errorbar(x+offset,means,yerr=sds,marker="o",markersize=2.8,lw=0.7,elinewidth=0.6,capsize=1.8,color=color,alpha=0.18)
            display.extend(finite_values(means).tolist())
        mat=np.vstack(rows) if rows else np.empty((0,len(cols)))
        om=[]; ose=[]
        for j in range(len(cols)):
            m,_,se,_=mean_sd_sem(mat[:,j] if len(mat) else np.array([])); om.append(m); ose.append(se)
        ax.errorbar(x+offset,om,yerr=ose,marker="o",markersize=7,lw=2.8,elinewidth=2.2,capsize=4.5,color=color,alpha=1,label=class_name.capitalize(),zorder=5)
    ax.axhline(0,color="black",ls=":",lw=0.9)
    ax.set_xticks(x,labels,rotation=45,ha="right")
    ax.set_ylabel("Baseline-subtracted dF/F")
    ax.set_title("Green vs yellow\nlight: session mean ± SD; dark: overall mean ± SEM")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    apply_robust_y_limits(ax,[display],reference_values=[0.0])
    fig.suptitle(title,fontsize=14)
    fig.subplots_adjust(top=0.82,bottom=0.22,wspace=0.32)
    fig.savefig(output_path,dpi=300,bbox_inches="tight"); plt.close(fig)


def _plot_two_condition_mean_only(ax, df, col_a, col_b, label_a, label_b, color, panel_title):
    _plot_session_profile_mean_sd(ax,df,[col_a,col_b],[label_a,label_b],color,panel_title)
    ax.set_ylabel("Baseline-subtracted dF/F")




def combined_sound_response_summary_mean_only(
    cell_df: pd.DataFrame,
    am_rates: list[float],
    session_stats: dict[str, Any],
    output_path: Path,
    title: str,
) -> None:
    """Session mean +/- SD plus overall mean +/- SEM companion summary."""
    classified=cell_df[cell_df["cell_class"].isin(["green","yellow"])].copy()
    green=classified[classified["cell_class"]=="green"]
    yellow=classified[classified["cell_class"]=="yellow"]
    fig,axes=plt.subplots(3,3,figsize=(20,17))

    _plot_session_profile_mean_sd(axes[0,0],green,["fade_in_response","fade_out_response"],["Fade-in","Fade-out"],GREEN_COLOR,"Green FI vs FO")
    axes[0,0].set_ylabel("Baseline-subtracted dF/F")
    _plot_session_profile_mean_sd(axes[0,1],yellow,["fade_in_response","fade_out_response"],["Fade-in","Fade-out"],YELLOW_COLOR,"Yellow FI vs FO")
    axes[0,1].set_ylabel("Baseline-subtracted dF/F")
    _plot_session_class_metric_mean_sd(
        axes[0,2],classified,"fade_in_vs_fade_out_selectivity","FI/FO selectivity index","FI vs FO selectivity",
        session_stats.get("fade_selectivity_green_vs_yellow",{}).get("p"),reference=0.0)

    _plot_session_profile_mean_sd(axes[1,0],green,["fade_in_response","best_am_response"],["Fade-in","Best AM"],GREEN_COLOR,"Green FI vs best AM")
    axes[1,0].set_ylabel("Baseline-subtracted dF/F")
    _plot_session_profile_mean_sd(axes[1,1],yellow,["fade_in_response","best_am_response"],["Fade-in","Best AM"],YELLOW_COLOR,"Yellow FI vs best AM")
    axes[1,1].set_ylabel("Baseline-subtracted dF/F")
    _plot_session_class_metric_mean_sd(
        axes[1,2],classified,"fade_in_vs_best_am_selectivity","FI/best-AM selectivity index","FI vs best AM selectivity",
        session_stats.get("fade_bestam_selectivity_green_vs_yellow",{}).get("p"),reference=0.0)

    am_cols=[f"am_response_{r:g}Hz" for r in am_rates]; am_labels=[f"{r:g}" for r in am_rates]
    _plot_session_profile_mean_sd(axes[2,0],green,am_cols,am_labels,GREEN_COLOR,"Green AM-rate profile")
    axes[2,0].set_xlabel("AM rate (Hz)"); axes[2,0].set_ylabel("Baseline-subtracted dF/F")
    _plot_session_profile_mean_sd(axes[2,1],yellow,am_cols,am_labels,YELLOW_COLOR,"Yellow AM-rate profile")
    axes[2,1].set_xlabel("AM rate (Hz)"); axes[2,1].set_ylabel("Baseline-subtracted dF/F")
    _plot_session_class_metric_mean_sd(
        axes[2,2],classified,"am_rate_lifetime_sparseness","AM lifetime sparseness","AM-rate selectivity",
        session_stats.get("am_rate_lifetime_sparseness_green_vs_yellow",{}).get("p"),reference=None)

    fig.text(0.5,0.012,_equation_footer(),ha="center",va="bottom",fontsize=10)
    fig.suptitle(title+"\nLight/thin = individual session mean ± SD; dark/thick = overall mean ± SEM across sessions",fontsize=14,y=0.995)
    fig.subplots_adjust(top=0.93,bottom=0.07,hspace=0.46,wspace=0.34)
    fig.savefig(output_path,dpi=300,bbox_inches="tight"); plt.close(fig)


def combined_selectivity_raster_preference_and_selectivity(
    cell_df: pd.DataFrame,
    am_rates: list[float],
    output_path: Path,
    title: str,
) -> None:
    condition_cols=["fade_in_response","fade_out_response"]+[f"am_response_{r:g}Hz" for r in am_rates]
    labels=["FI","FO"]+[f"AM {r:g}" for r in am_rates]
    fig,axes=plt.subplots(2,3,figsize=(19,11),constrained_layout=True)
    im=None
    for row_idx,(class_name,color_name) in enumerate([("green","GREEN"),("yellow","YELLOW")]):
        df=cell_df[(cell_df["cell_class"]==class_name)&(cell_df["raster_responsive"]==True)].copy()  # noqa: E712
        if len(df)==0:
            for ax in axes[row_idx]: ax.axis("off")
            continue
        matrix=np.column_stack([df[col].to_numpy(float) if col in df else np.full(len(df),np.nan) for col in condition_cols])
        norm=np.nanmax(np.abs(matrix),axis=1,keepdims=True); norm[(~np.isfinite(norm))|(norm<=0)]=np.nan
        normalized=matrix/norm
        pref=np.nanargmax(np.where(np.isfinite(matrix),matrix,-np.inf),axis=1)
        pref_order=np.argsort(pref)
        fi_fo=np.abs(df["fade_in_vs_fade_out_selectivity"].to_numpy(float))
        fi_order=np.argsort(np.where(np.isfinite(fi_fo),fi_fo,-np.inf))[::-1]
        am_sp=df["am_rate_lifetime_sparseness"].to_numpy(float)
        am_order=np.argsort(np.where(np.isfinite(am_sp),am_sp,-np.inf))[::-1]
        for ax,(order,sort_title) in zip(axes[row_idx],[
            (pref_order,"sorted by preferred condition"),
            (fi_order,"sorted by |FI/FO selectivity|"),
            (am_order,"sorted by AM lifetime sparseness"),
        ]):
            im=ax.imshow(normalized[order],aspect="auto",interpolation="nearest",cmap="coolwarm",vmin=-1,vmax=1)
            ax.set_xticks(np.arange(len(labels)),labels,rotation=45,ha="right")
            ax.set_ylabel("Cells")
            ax.set_title(f"{color_name} | {sort_title}\nn={len(df)}")
    if im is not None:
        cbar=fig.colorbar(im,ax=axes,shrink=0.86); cbar.set_label("Response / max absolute response per cell")
    fig.suptitle(title,fontsize=14)
    fig.savefig(output_path,dpi=300,bbox_inches="tight"); plt.close(fig)


def combined_selectivity_raster(cell_df: pd.DataFrame, am_rates: list[float], output_path: Path, title: str) -> None:
    condition_cols = ["fade_in_response", "fade_out_response"] + [f"am_response_{r:g}Hz" for r in am_rates]
    labels = ["FI", "FO"] + [f"AM {r:g}" for r in am_rates]
    fig, axes = plt.subplots(1, 2, figsize=(13, 9), constrained_layout=True)
    im = None
    for ax, class_name, color_name in zip(axes, ["green", "yellow"], ["GREEN", "YELLOW"]):
        df = cell_df[(cell_df["cell_class"] == class_name) & (cell_df["raster_responsive"] == True)].copy()  # noqa: E712
        if len(df) == 0:
            ax.text(0.5, 0.5, f"No responsive {class_name} cells", transform=ax.transAxes,
                    ha="center", va="center")
            ax.set_title(color_name)
            continue
        matrix = np.column_stack([
            df[col].to_numpy(dtype=float) if col in df else np.full(len(df), np.nan)
            for col in condition_cols
        ])
        norm = np.nanmax(np.abs(matrix), axis=1, keepdims=True)
        norm[(~np.isfinite(norm)) | (norm <= 0)] = np.nan
        normalized = matrix / norm
        order = np.argsort(df["looming_score"].to_numpy(dtype=float))[::-1]
        normalized = normalized[order]
        im = ax.imshow(normalized, aspect="auto", interpolation="nearest", cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_title(f"{color_name} responsive cells\nn={len(df)} | sorted by looming score")
        ax.set_xticks(np.arange(len(labels)), labels, rotation=45, ha="right")
        ax.set_ylabel("Cells")
        ax.set_xlabel("Sound condition")
    if im is not None:
        cbar = fig.colorbar(im, ax=axes, shrink=0.85)
        cbar.set_label("Response / max absolute response per cell")
    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def session_level_figure(
    class_summary_df: pd.DataFrame,
    output_path: Path,
    title: str,
    session_stats: dict[str, Any],
) -> None:
    """Primary session-level GREEN/YELLOW comparisons using session means."""
    fig,axes=plt.subplots(2,3,figsize=(18,10))
    panels=[
        ("pct_sound_responsive_fdr","Sound-responsive cells (%)","responsive_fraction_green_vs_yellow",None),
        ("mean_fade_in_vs_fade_out_selectivity","Mean FI/FO selectivity","fade_selectivity_green_vs_yellow",0.0),
        ("mean_fade_in_vs_best_am_selectivity","Mean FI/best-AM selectivity","fade_bestam_selectivity_green_vs_yellow",0.0),
        ("mean_am_rate_lifetime_sparseness","Mean AM lifetime sparseness","am_rate_lifetime_sparseness_green_vs_yellow",None),
        ("mean_fade_in_response","Mean fade-in response","fade_in_green_vs_yellow",0.0),
    ]
    pivot=class_summary_df.pivot(index="session_key",columns="cell_class") if len(class_summary_df) else pd.DataFrame()
    for ax,(metric,ylabel,stat_key,ref) in zip(axes.flat,panels):
        if metric not in pivot or "green" not in pivot[metric] or "yellow" not in pivot[metric]:
            ax.axis("off"); continue
        g=pivot[metric]["green"]; y=pivot[metric]["yellow"]; common=g.index.intersection(y.index)
        gv=g.loc[common].to_numpy(float); yv=y.loc[common].to_numpy(float)
        valid=np.isfinite(gv)&np.isfinite(yv); gv=gv[valid]; yv=yv[valid]
        for gg,yy in zip(gv,yv): ax.plot([0,1],[gg,yy],color="0.6",alpha=0.55,lw=1)
        ax.scatter(np.zeros(len(gv)),gv,color=GREEN_COLOR,s=35,zorder=3)
        ax.scatter(np.ones(len(yv)),yv,color=YELLOW_COLOR,edgecolor="black",linewidth=0.3,s=40,zorder=3)
        if ref is not None: ax.axhline(ref,color="black",ls=":",lw=1)
        pval=session_stats.get(stat_key,{}).get("p"); ptxt="n/a" if pval is None else f"{pval:.3g}"
        ax.set_title(f"paired sessions n={len(gv)} | Wilcoxon p={ptxt}")
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(ylabel); ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
        apply_robust_y_limits(ax,[gv,yv],reference_values=None if ref is None else [ref])
    axes.flat[-1].axis("off")
    fig.suptitle(title+"\nSession-level paired summaries",fontsize=14)
    fig.subplots_adjust(top=0.90,hspace=0.35,wspace=0.30)
    fig.savefig(output_path,dpi=300,bbox_inches="tight"); plt.close(fig)


def combined_fade_in_suppression_plot(
    cell_df: pd.DataFrame,
    class_summary_df: pd.DataFrame,
    output_path: Path,
    title: str,
    pooled_stats: dict[str, Any],
    session_stats: dict[str, Any],
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)
    rng = np.random.default_rng(42)
    ax = axes[0]
    for pos, class_name, color in [(0, "green", GREEN_COLOR), (1, "yellow", YELLOW_COLOR)]:
        vals = finite_values(cell_df.loc[cell_df["cell_class"] == class_name, "fade_in_response"])
        jitter = rng.uniform(-0.12, 0.12, len(vals))
        ax.scatter(np.full(len(vals), pos) + jitter, vals, color=color,
                   alpha=0.4 if class_name == "green" else 0.65, s=18,
                   edgecolor="black" if class_name == "yellow" else "none", linewidth=0.2)
        if len(vals):
            med = np.median(vals)
            ax.plot([pos - 0.2, pos + 0.2], [med, med], color="black", lw=3)
    ax.axhline(0, color="black", ls="--", lw=1)
    pooled_p = pooled_stats["fade_in_yellow_vs_green"]["p"]
    suppress_p = pooled_stats["fade_in_yellow_less_than_zero"]["p"]
    ax.set_title(
        "Pooled cells (exploratory)\n"
        f"yellow<0 p={('n/a' if suppress_p is None else f'{suppress_p:.3g}')}; "
        f"yellow vs green p={('n/a' if pooled_p is None else f'{pooled_p:.3g}')}"
    )
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel("Mean fade-in response (baseline-subtracted dF/F)")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    green_fade_display = finite_values(
        cell_df.loc[cell_df["cell_class"] == "green", "fade_in_response"]
    )
    yellow_fade_display = finite_values(
        cell_df.loc[cell_df["cell_class"] == "yellow", "fade_in_response"]
    )
    mg, seg = mean_sem(green_fade_display)
    my, sey = mean_sem(yellow_fade_display)
    important = [mg, my, 0.0]
    if np.isfinite(seg):
        important.extend([mg - seg, mg + seg])
    if np.isfinite(sey):
        important.extend([my - sey, my + sey])
    apply_robust_y_limits(
        ax,
        [green_fade_display, yellow_fade_display],
        important_values=important,
        reference_values=[0.0],
    )

    ax = axes[1]
    pivot = class_summary_df.pivot(index="session_key", columns="cell_class", values="mean_fade_in_response")
    if "green" in pivot and "yellow" in pivot:
        valid = np.isfinite(pivot["green"]) & np.isfinite(pivot["yellow"])
        gv = pivot.loc[valid, "green"].to_numpy(dtype=float)
        yv = pivot.loc[valid, "yellow"].to_numpy(dtype=float)
        for g, y in zip(gv, yv):
            ax.plot([0, 1], [g, y], color="0.6", alpha=0.7)
        ax.scatter(np.zeros(len(gv)), gv, color=GREEN_COLOR, s=40)
        ax.scatter(np.ones(len(yv)), yv, color=YELLOW_COLOR, edgecolor="black", linewidth=0.3, s=45)
    else:
        gv = yv = np.array([])
    ax.axhline(0, color="black", ls="--", lw=1)
    p_pair = session_stats["fade_in_green_vs_yellow"]["p"]
    p_y0 = session_stats["yellow_mean_fade_in_less_than_zero"]["p"]
    ax.set_title(
        "Session means (primary across-session view)\n"
        f"yellow<0 p={('n/a' if p_y0 is None else f'{p_y0:.3g}')}; "
        f"green vs yellow p={('n/a' if p_pair is None else f'{p_pair:.3g}')}"
    )
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel("Session mean fade-in response")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    mg, seg = mean_sem(gv)
    my, sey = mean_sem(yv)
    important = [mg, my, 0.0]
    if np.isfinite(seg):
        important.extend([mg - seg, mg + seg])
    if np.isfinite(sey):
        important.extend([my - sey, my + sey])
    apply_robust_y_limits(
        ax,
        [gv, yv],
        important_values=important,
        reference_values=[0.0],
    )
    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)



def fade_in_suppression_mean_only(
    cell_df: pd.DataFrame,
    class_summary_df: pd.DataFrame,
    output_path: Path,
    title: str,
    pooled_stats: dict[str, Any],
    session_stats: dict[str, Any],
) -> None:
    """Fade-in session means +/- SD plus overall mean +/- SEM."""
    df=cell_df[cell_df["cell_class"].isin(["green","yellow"])].copy()
    fig,axes=plt.subplots(1,2,figsize=(15,6.5))

    ax=axes[0]
    session_keys=sorted(df["session_key"].dropna().astype(str).unique()); x=np.arange(len(session_keys),dtype=float)
    for class_name,color,offset in [("green",GREEN_COLOR,-0.06),("yellow",YELLOW_COLOR,0.06)]:
        means=[]; sds=[]
        for key in session_keys:
            sdf=df[(df["session_key"].astype(str)==key)&(df["cell_class"]==class_name)]
            m,sd,_=_mean_sd(sdf["fade_in_response"].to_numpy(float)); means.append(m); sds.append(sd)
        ax.errorbar(x+offset,means,yerr=sds,marker="o",markersize=4,lw=0.9,elinewidth=0.8,capsize=2.5,color=color,alpha=0.30,label=f"{class_name.capitalize()} sessions")
        om,_,ose,n=mean_sd_sem(means)
        ax.axhline(om,color=color,lw=3.0,alpha=1.0)
        if np.isfinite(ose): ax.fill_between([-0.5,len(session_keys)-0.5],[om-ose]*2,[om+ose]*2,color=color,alpha=0.10)
    ax.axhline(0,color="black",ls=":",lw=1)
    ax.set_xticks(x,[k.replace("_","\n") for k in session_keys],rotation=45,ha="right")
    ax.set_ylabel("Fade-in response")
    ax.set_title("By session\npoints/error = session mean ± SD; thick horizontal = overall mean ± SEM")
    ax.legend(frameon=False,fontsize=8); ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)

    _plot_session_class_metric_mean_sd(
        axes[1],df,"fade_in_response","Fade-in response","Collapsed GREEN vs YELLOW",
        session_stats.get("fade_in_green_vs_yellow",{}).get("p"),reference=0.0)
    p_y0=session_stats.get("yellow_mean_fade_in_less_than_zero",{}).get("p")
    axes[1].text(0.5,0.02,f"Yellow session means < 0: p={'n/a' if p_y0 is None else f'{p_y0:.3g}'}",transform=axes[1].transAxes,ha="center",va="bottom",fontsize=8)
    fig.suptitle(title,fontsize=14)
    fig.subplots_adjust(top=0.84,bottom=0.20,wspace=0.32)
    fig.savefig(output_path,dpi=300,bbox_inches="tight"); plt.close(fig)


def session_level_mean_only_figure(
    cell_df: pd.DataFrame,
    output_path: Path,
    title: str,
    session_stats: dict[str, Any],
) -> None:
    """Session mean +/- SD and overall mean +/- SEM for primary metrics."""
    df=cell_df[cell_df["cell_class"].isin(["green","yellow"])].copy()
    df["sound_responsive_pct_cell"]=100.0*df["sound_responsive_fdr"].astype(float)
    fig,axes=plt.subplots(2,3,figsize=(18,11))
    panels=[
        ("sound_responsive_pct_cell","Sound-responsive cells (%)","Responsive fraction","responsive_fraction_green_vs_yellow",None),
        ("fade_in_vs_fade_out_selectivity","FI/FO selectivity index","FI vs FO selectivity","fade_selectivity_green_vs_yellow",0.0),
        ("fade_in_vs_best_am_selectivity","FI/best-AM selectivity index","FI vs best AM selectivity","fade_bestam_selectivity_green_vs_yellow",0.0),
        ("am_rate_lifetime_sparseness","AM lifetime sparseness","AM-rate selectivity","am_rate_lifetime_sparseness_green_vs_yellow",None),
        ("fade_in_response","Fade-in response","Fade-in response","fade_in_green_vs_yellow",0.0),
    ]
    for ax,(metric,ylabel,panel_title,stat_key,ref) in zip(axes.flat,panels):
        _plot_session_class_metric_mean_sd(ax,df,metric,ylabel,panel_title,session_stats.get(stat_key,{}).get("p"),reference=ref)
    axes.flat[-1].axis("off")
    fig.suptitle(title+"\nLight/thin = individual session mean ± SD; dark/thick = overall mean ± SEM",fontsize=14)
    fig.subplots_adjust(top=0.90,hspace=0.48,wspace=0.32)
    fig.savefig(output_path,dpi=300,bbox_inches="tight"); plt.close(fig)


# =============================================================================
# COMBINED STATISTICS
# =============================================================================

def compute_combined_statistics(
    cell_df: pd.DataFrame,
    class_summary_df: pd.DataFrame,
) -> tuple[dict[str, Any], dict[str, Any]]:
    classified=cell_df[cell_df["cell_class"].isin(["green","yellow"])]
    green=classified[classified["cell_class"]=="green"]
    yellow=classified[classified["cell_class"]=="yellow"]

    selectivity_metrics=[
        ("fade_selectivity_green_vs_yellow","fade_in_vs_fade_out_selectivity"),
        ("fade_bestam_selectivity_green_vs_yellow","fade_in_vs_best_am_selectivity"),
        ("am_rate_lifetime_sparseness_green_vs_yellow","am_rate_lifetime_sparseness"),
    ]
    pooled_tests={}
    raw_p=[]
    for key,col in selectivity_metrics:
        res=safe_mannwhitney(green[col],yellow[col]); pooled_tests[key]=res
        raw_p.append(np.nan if res["p"] is None else float(res["p"]))
    corrected=holm_correct(raw_p)
    for (key,_),pcorr in zip(selectivity_metrics,corrected):
        pooled_tests[key]["holm_p"]=None if not np.isfinite(pcorr) else float(pcorr)

    yellow_fade=finite_values(yellow["fade_in_response"]); green_fade=finite_values(green["fade_in_response"])
    pooled={
        "note":"Pooled-cell tests are descriptive/exploratory; cells from the same session are not independent biological replicates.",
        **pooled_tests,
        "fade_in_yellow_vs_zero_two_sided":safe_wilcoxon(yellow_fade,"two-sided"),
        "fade_in_yellow_less_than_zero":safe_wilcoxon(yellow_fade,"less"),
        "fade_in_yellow_vs_green":safe_mannwhitney(yellow_fade,green_fade),
    }
    try:
        g_resp=int(np.sum(green["sound_responsive_fdr"].astype(bool))); y_resp=int(np.sum(yellow["sound_responsive_fdr"].astype(bool)))
        contingency=[[g_resp,len(green)-g_resp],[y_resp,len(yellow)-y_resp]]; fisher=stats.fisher_exact(contingency)
        pooled["responsive_fraction_fisher_green_vs_yellow"]={"odds_ratio":float(fisher.statistic),"p":float(fisher.pvalue),"table":contingency}
    except Exception:
        pooled["responsive_fraction_fisher_green_vs_yellow"]={"odds_ratio":None,"p":None,"table":None}

    pivot=class_summary_df.pivot(index="session_key",columns="cell_class") if len(class_summary_df) else pd.DataFrame()
    def paired_metric(metric,alternative="two-sided"):
        if metric not in pivot or "green" not in pivot[metric] or "yellow" not in pivot[metric]:
            return {"statistic":None,"p":None,"n_pairs":0}
        return safe_paired_wilcoxon(pivot[metric]["green"].to_numpy(float),pivot[metric]["yellow"].to_numpy(float),alternative=alternative)
    session_level={
        "note":"Primary across-session comparisons use one GREEN and one YELLOW mean per session when both are available.",
        "responsive_fraction_green_vs_yellow":paired_metric("pct_sound_responsive_fdr"),
        "fade_selectivity_green_vs_yellow":paired_metric("mean_fade_in_vs_fade_out_selectivity"),
        "fade_bestam_selectivity_green_vs_yellow":paired_metric("mean_fade_in_vs_best_am_selectivity"),
        "am_rate_lifetime_sparseness_green_vs_yellow":paired_metric("mean_am_rate_lifetime_sparseness"),
        "fade_in_green_vs_yellow":paired_metric("mean_fade_in_response"),
    }
    if "mean_fade_in_response" in pivot and "yellow" in pivot["mean_fade_in_response"]:
        session_level["yellow_mean_fade_in_less_than_zero"]=safe_wilcoxon(pivot["mean_fade_in_response"]["yellow"].to_numpy(float),alternative="less")
    else:
        session_level["yellow_mean_fade_in_less_than_zero"]={"statistic":None,"p":None,"n":0}
    keys=["fade_selectivity_green_vs_yellow","fade_bestam_selectivity_green_vs_yellow","am_rate_lifetime_sparseness_green_vs_yellow"]
    corr=holm_correct([np.nan if session_level[k]["p"] is None else float(session_level[k]["p"]) for k in keys])
    for k,pcorr in zip(keys,corr): session_level[k]["holm_p"]=None if not np.isfinite(pcorr) else float(pcorr)
    return pooled,session_level


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args = parse_args()
    dates = normalize_dates(args.dates)
    subject = args.subject
    area = args.area

    info_file, all_sessions = load_info2p_sessions(subject)
    selected = select_sessions(all_sessions, dates, area)
    output_dirs = build_output_dirs(subject, area, dates)
    selection_df = session_selection_dataframe(selected)
    selection_df.to_csv(output_dirs["root"] / "session_selection.csv", index=False)

    print("\n" + "=" * 78)
    print("SOUND_TUNING AREA ANALYSIS")
    print("=" * 78)
    print(f"Subject:       {subject}")
    print(f"Requested area:{' ' if area else ''}{area}")
    print(f"Dates:         {', '.join(dates)}")
    print(f"Paradigm:      {PARADIGM}")
    print(f"Info2p:        {info_file}")
    print(f"Data root:     {settings.TWOPHOTON_PATH}")
    print(f"Behavior root: {settings.BEHAVIOR_PATH}")
    print(f"Output root:   {output_dirs['root']}")
    print(f"Sessions:      {len(selected)}")

    if len(selected):
        print("\nSelected sessions:")
        for s in selected:
            print(
                f"  {s['date']}  {s['session']}  "
                f"brainArea={s.get('brainArea')}  depth={s.get('depth')}  "
                f"label={s.get('sessionLabel')}"
            )
    else:
        raise ValueError(
            f"No {PARADIGM} sessions found for subject={subject}, "
            f"area={area}, dates={dates}."
        )

    manifest: dict[str, Any] = {
        "subject": subject,
        "area": area,
        "dates": dates,
        "plane": args.plane,
        "paradigm": PARADIGM,
        "info2p_file": str(info_file),
        "settings": {
            "TWOPHOTON_PATH": getattr(settings, "TWOPHOTON_PATH", None),
            "BEHAVIOR_PATH": getattr(settings, "BEHAVIOR_PATH", None),
            "INFO2P_PATH": getattr(settings, "INFO2P_PATH", None),
            "TEMP_OUTPUT_PATH": getattr(settings, "TEMP_OUTPUT_PATH", None),
        },
        "analysis_parameters": {
            "cell_prob_threshold": CELL_PROB_THRESHOLD,
            "time_range": TIME_RANGE,
            "baseline_window": BASELINE_WINDOW,
            "response_window": RESPONSE_WINDOW,
            "iou_threshold": IOU_THRESHOLD,
            "cellpose_cellprob_threshold": CELLPOSE_CELLPROB_THRESHOLD,
            "cellpose_flow_threshold": CELLPOSE_FLOW_THRESHOLD,
            "raster_min_abs_response": RASTER_MIN_ABS_RESPONSE,
            "fdr_alpha": FDR_ALPHA,
            "n_permutations": args.n_permutations,
            "seed": args.seed,
        },
        "selected_sessions": selected,
        "successful_sessions": [],
        "failed_sessions": [],
        "output_root": str(output_dirs["root"]),
    }
    save_json(output_dirs["root"] / "run_manifest.json", manifest)

    if args.dry_run:
        print("\nDry run complete; no imaging data were loaded.")
        return

    session_results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for session_index, meta in enumerate(selected):
        date = str(meta["date"])
        session = str(meta["session"])
        session_dir = output_dirs["session_root"] / f"{date}_{session}"
        try:
            result = analyze_session(
                meta,
                plane=args.plane,
                session_output_dir=session_dir,
                n_permutations=args.n_permutations,
                seed=args.seed + session_index,
            )
            session_results.append(result)
            manifest["successful_sessions"].append(
                {"date": date, "session": session, "output_dir": str(session_dir)}
            )
        except Exception as exc:
            error_record = {
                "date": date,
                "session": session,
                "brainArea": meta.get("brainArea"),
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
            failures.append(error_record)
            manifest["failed_sessions"].append(error_record)
            session_dir.mkdir(parents=True, exist_ok=True)
            save_json(session_dir / "ERROR.json", error_record)
            print("\nERROR in session " + f"{date} {session}: {type(exc).__name__}: {exc}")
            print("Continuing with remaining selected sessions.")
        finally:
            save_json(output_dirs["root"] / "run_manifest.json", manifest)

    if failures:
        pd.DataFrame(failures).drop(columns=["traceback"], errors="ignore").to_csv(
            output_dirs["root"] / "session_failures.csv", index=False
        )

    if not session_results:
        raise RuntimeError(
            "All selected sessions failed. See run_manifest.json and session_outputs/*/ERROR.json."
        )

    # -------------------------------------------------------------------------
    # Combined tables.
    # -------------------------------------------------------------------------
    cell_df = pd.concat([r["cell_df"] for r in session_results], ignore_index=True, sort=False)
    class_summary_df = pd.concat(
        [r["class_summary_df"] for r in session_results], ignore_index=True, sort=False
    )
    trace_records = [tr for r in session_results for tr in r["trace_records"]]
    combined_dir = output_dirs["combined"]
    cell_df.to_csv(combined_dir / "combined_cell_results.csv", index=False)
    class_summary_df.to_csv(combined_dir / "combined_session_class_summary.csv", index=False)

    all_am_rates = sorted({
        float(rate)
        for result in session_results
        for rate in result["possible_am_rates"]
    })

    pooled_stats, session_stats = compute_combined_statistics(cell_df, class_summary_df)

    # Statistically reliable sound-responsive subset (BH-FDR q < 0.05 within session).
    responsive_cell_df = fdr_sound_responsive_subset(cell_df)
    responsive_class_summary_df = subset_session_class_summary(responsive_cell_df)
    responsive_trace_records = [
        r for r in trace_records if bool(r.get("sound_responsive_fdr", False))
    ]
    if len(responsive_cell_df) and len(responsive_class_summary_df):
        responsive_pooled_stats, responsive_session_stats = compute_combined_statistics(
            responsive_cell_df, responsive_class_summary_df
        )
    else:
        responsive_pooled_stats = {
            "fade_selectivity_green_vs_yellow": {"p": None, "holm_p": None},
            "fade_bestam_selectivity_green_vs_yellow": {"p": None, "holm_p": None},
            "am_rate_lifetime_sparseness_green_vs_yellow": {"p": None, "holm_p": None},
            "fade_in_yellow_vs_zero_two_sided": {"p": None},
            "fade_in_yellow_less_than_zero": {"p": None},
            "fade_in_yellow_vs_green": {"p": None},
        }
        responsive_session_stats = {
            "responsive_fraction_green_vs_yellow": {"p": None},
            "fade_selectivity_green_vs_yellow": {"p": None, "holm_p": None},
            "fade_bestam_selectivity_green_vs_yellow": {"p": None, "holm_p": None},
            "am_rate_lifetime_sparseness_green_vs_yellow": {"p": None, "holm_p": None},
            "fade_in_green_vs_yellow": {"p": None},
            "yellow_mean_fade_in_less_than_zero": {"p": None},
        }

    stats_payload = {
        "pooled_cell_exploratory": pooled_stats,
        "session_level_primary": session_stats,
        "fdr_sound_responsive_cells_only": {"pooled_cell_exploratory": responsive_pooled_stats, "session_level": responsive_session_stats},
        "n_successful_sessions": len(session_results),
        "n_failed_sessions": len(failures),
        "n_cells_total_rows": len(cell_df),
        "n_green_pooled": int(np.sum(cell_df["cell_class"] == "green")),
        "n_yellow_pooled": int(np.sum(cell_df["cell_class"] == "yellow")),
        "n_fdr_sound_responsive_pooled": int(len(responsive_cell_df)),
        "n_green_fdr_sound_responsive": int(np.sum(responsive_cell_df["cell_class"] == "green")),
        "n_yellow_fdr_sound_responsive": int(np.sum(responsive_cell_df["cell_class"] == "yellow")),
        "am_rates": all_am_rates,
    }
    save_json(combined_dir / "combined_statistics.json", stats_payload)

    title = (
        f"{subject} | {area} | {', '.join(dates)} | "
        f"{len(session_results)} successful sound_tuning sessions"
    )

    # -------------------------------------------------------------------------
    # Restored notebook responsiveness figure + clean session-mean companion.
    # -------------------------------------------------------------------------
    sound_responsiveness_figure(
        cell_df,
        combined_dir / "combined_sound_responsive_cells_green_yellow.png",
        title + " | pooled cells",
    )
    sound_responsiveness_session_mean_only(
        cell_df,
        combined_dir / "combined_sound_responsiveness_session_mean_sem_only.png",
        title,
    )

    # -------------------------------------------------------------------------
    # Sound-condition response curves: detailed, FDR-responsive-only, and
    # session mean±SD + overall mean±SEM companions for both subsets.
    # -------------------------------------------------------------------------
    combined_condition_response_plot(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_condition_responses_green_yellow.png",
        title + " | all classified cells",
    )
    combined_condition_response_plot(
        responsive_cell_df,
        all_am_rates,
        combined_dir / "combined_sound_condition_responses_green_yellow_FDR_responsive_only.png",
        title + " | FDR sound-responsive cells only",
    )
    combined_condition_response_mean_only(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_condition_responses_green_yellow_MEAN_SEM_ONLY.png",
        title + " | all classified cells",
    )
    combined_condition_response_mean_only(
        responsive_cell_df,
        all_am_rates,
        combined_dir / "combined_sound_condition_responses_green_yellow_FDR_responsive_only_MEAN_SEM_ONLY.png",
        title + " | FDR sound-responsive cells only",
    )

    # -------------------------------------------------------------------------
    # Selectivity rasters. Existing versions use the notebook amplitude display
    # threshold; additional versions require statistical FDR responsiveness too.
    # -------------------------------------------------------------------------
    combined_selectivity_raster_preference_and_selectivity(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_selectivity_rasters_preference_and_selectivity.png",
        title,
    )
    combined_selectivity_raster_preference_and_selectivity(
        responsive_cell_df,
        all_am_rates,
        combined_dir / "combined_sound_selectivity_rasters_preference_and_selectivity_FDR_responsive_only.png",
        title + " | FDR sound-responsive cells only",
    )
    combined_selectivity_raster(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_selectivity_raster_looming_score.png",
        title,
    )
    combined_selectivity_raster(
        responsive_cell_df,
        all_am_rates,
        combined_dir / "combined_sound_selectivity_raster_looming_score_FDR_responsive_only.png",
        title + " | FDR sound-responsive cells only",
    )

    # -------------------------------------------------------------------------
    # Main green/yellow sound-response summary: detailed + responsive-only +
    # session mean±SD + overall mean±SEM companions.
    # -------------------------------------------------------------------------
    combined_sound_response_summary(
        cell_df,
        trace_records,
        all_am_rates,
        session_stats,
        combined_dir / "combined_green_yellow_sound_response_summary.png",
        title + " | all classified cells",
    )
    combined_sound_response_summary_cell_points(
        cell_df,
        trace_records,
        all_am_rates,
        pooled_stats,
        combined_dir / "combined_green_yellow_sound_response_summary_INDIVIDUAL_CELLS.png",
        title + " | all classified cells",
    )
    combined_sound_response_summary(
        responsive_cell_df,
        responsive_trace_records,
        all_am_rates,
        responsive_session_stats,
        combined_dir / "combined_green_yellow_sound_response_summary_FDR_responsive_only.png",
        title + " | FDR sound-responsive cells only",
    )
    combined_sound_response_summary_cell_points(
        responsive_cell_df,
        responsive_trace_records,
        all_am_rates,
        responsive_pooled_stats,
        combined_dir / "combined_green_yellow_sound_response_summary_FDR_responsive_only_INDIVIDUAL_CELLS.png",
        title + " | FDR sound-responsive cells only",
    )
    combined_sound_response_summary_mean_only(
        cell_df,
        all_am_rates,
        session_stats,
        combined_dir / "combined_green_yellow_sound_response_summary_MEAN_SEM_ONLY.png",
        title + " | all classified cells",
    )
    combined_sound_response_summary_mean_only(
        responsive_cell_df,
        all_am_rates,
        responsive_session_stats,
        combined_dir / "combined_green_yellow_sound_response_summary_FDR_responsive_only_MEAN_SEM_ONLY.png",
        title + " | FDR sound-responsive cells only",
    )

    # -------------------------------------------------------------------------
    # Session-level comparisons and mean-only companion.
    # -------------------------------------------------------------------------
    session_level_figure(
        class_summary_df,
        combined_dir / "combined_session_level_green_yellow_comparisons.png",
        title,
        session_stats,
    )
    session_level_mean_only_figure(
        cell_df,
        combined_dir / "combined_session_level_green_yellow_comparisons_MEAN_SEM_ONLY.png",
        title,
        session_stats,
    )

    # -------------------------------------------------------------------------
    # Fade-in suppression: detailed, FDR-responsive-only, and mean-only.
    # -------------------------------------------------------------------------
    combined_fade_in_suppression_plot(
        cell_df,
        class_summary_df,
        combined_dir / "combined_fade_in_suppression_green_yellow.png",
        title + " | all classified cells",
        pooled_stats,
        session_stats,
    )
    if len(responsive_class_summary_df):
        combined_fade_in_suppression_plot(
            responsive_cell_df,
            responsive_class_summary_df,
            combined_dir / "combined_fade_in_suppression_green_yellow_FDR_responsive_only.png",
            title + " | FDR sound-responsive cells only",
            responsive_pooled_stats,
            responsive_session_stats,
        )
    fade_in_suppression_mean_only(
        cell_df,
        class_summary_df,
        combined_dir / "combined_fade_in_suppression_green_yellow_MEAN_SEM_ONLY.png",
        title + " | all classified cells",
        pooled_stats,
        session_stats,
    )
    if len(responsive_class_summary_df):
        fade_in_suppression_mean_only(
            responsive_cell_df,
            responsive_class_summary_df,
            combined_dir / "combined_fade_in_suppression_green_yellow_FDR_responsive_only_MEAN_SEM_ONLY.png",
            title + " | FDR sound-responsive cells only",
            responsive_pooled_stats,
            responsive_session_stats,
        )

    # Figure index for quick navigation.
    figure_index = [
        "FIGURE VARIANTS",
        "=" * 70,
        "FDR responsive means sound_responsive_fdr == True (per-session BH-FDR q<0.05).",
        "MEAN_SEM_ONLY files show individual-session mean ± SD (light/thin) and overall mean ± SEM across sessions (dark/thick).",
        "Selectivity rasters use FI/FO selectivity and AM lifetime sparseness; FDR versions additionally require statistical responsiveness.",
        "",
    ]
    for p in sorted(combined_dir.glob("*.png")):
        figure_index.append(p.name)
    (combined_dir / "FIGURE_INDEX.txt").write_text("\n".join(figure_index))

    # Short human-readable report.
    report_lines = [
        "SOUND_TUNING AREA ANALYSIS COMPLETE",
        "=" * 50,
        f"Subject: {subject}",
        f"Area: {area}",
        f"Dates: {', '.join(dates)}",
        f"Successful sessions: {len(session_results)}/{len(selected)}",
        f"Pooled green cells: {int(np.sum(cell_df['cell_class'] == 'green'))}",
        f"Pooled yellow cells: {int(np.sum(cell_df['cell_class'] == 'yellow'))}",
        f"FDR sound-responsive pooled cells: {len(responsive_cell_df)}",
        f"  Green responsive: {int(np.sum(responsive_cell_df['cell_class'] == 'green'))}",
        f"  Yellow responsive: {int(np.sum(responsive_cell_df['cell_class'] == 'yellow'))}",
        "",
        "Primary across-session statistics:",
        json.dumps(jsonable(session_stats), indent=2),
        "",
        "Exploratory pooled-cell statistics:",
        json.dumps(jsonable(pooled_stats), indent=2),
        "",
        f"Output directory: {output_dirs['root']}",
    ]
    (combined_dir / "combined_report.txt").write_text("\n".join(report_lines))

    manifest["combined_outputs"] = {
        "combined_dir": str(combined_dir),
        "combined_cell_results": str(combined_dir / "combined_cell_results.csv"),
        "combined_session_class_summary": str(combined_dir / "combined_session_class_summary.csv"),
        "combined_statistics": str(combined_dir / "combined_statistics.json"),
    }
    save_json(output_dirs["root"] / "run_manifest.json", manifest)

    print("\n" + "=" * 78)
    print("ANALYSIS COMPLETE")
    print("=" * 78)
    print(f"Successful sessions: {len(session_results)}/{len(selected)}")
    if failures:
        print(f"Failed sessions:     {len(failures)}")
    print(f"Pooled green cells:  {int(np.sum(cell_df['cell_class'] == 'green'))}")
    print(f"Pooled yellow cells: {int(np.sum(cell_df['cell_class'] == 'yellow'))}")
    print(f"All outputs saved under:\n{output_dirs['root']}")


if __name__ == "__main__":
    main()
