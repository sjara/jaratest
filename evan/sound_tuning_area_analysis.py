#!/usr/bin/env python3
"""
Batch analysis of sound_tuning two-photon sessions from one auditory cortical area.

This script is the batch/area-level version of:
    twophoton_sound_tuning_EV_20260812.ipynb

Version 1 scope
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
* The notebook's legacy-score outlier rule is preserved independently for each
  session: the analyzed ROI with the minimum finite Suite2p chan2 score is
  excluded from both GREEN and YELLOW.
* Outputs are always saved under jaratoolbox.settings.TEMP_OUTPUT_PATH.

Example
-------
python sound_tuning_area_analysis.py imag039 \
    --area A1 \
    --dates 20260729 20260730

A discovery-only run can be made with:
python sound_tuning_area_analysis.py imag039 \
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
RATIO_DENOMINATOR_THRESHOLD = 1e-12

FDR_ALPHA = 0.05
N_PERMUTATIONS_DEFAULT = 20000
RANDOM_SEED_DEFAULT = 20260812

GREEN_COLOR = "forestgreen"
YELLOW_COLOR = "goldenrod"
DISPLAY_GREEN_COLOR = "lime"
DISPLAY_YELLOW_COLOR = "yellow"
ANATOMICAL_RED_COLOR = "red"
EXCLUDED_COLOR = "magenta"
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


def amplitude_ratio(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    ratio = np.full(len(numerator), np.nan, dtype=float)
    valid = (
        np.isfinite(numerator)
        & np.isfinite(denominator)
        & (np.abs(denominator) > RATIO_DENOMINATOR_THRESHOLD)
    )
    ratio[valid] = np.abs(numerator[valid]) / np.abs(denominator[valid])
    return ratio


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
    outlier_analysis_index: int,
    red_masks: np.ndarray,
) -> set[int]:
    Ly, Lx = red_masks.shape
    labels_to_hide: set[int] = set()
    for analysis_index, roi_stat in enumerate(functional_stats):
        if analysis_index == outlier_analysis_index or not yellow_mask[analysis_index]:
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
    outlier_analysis_index: int,
    output_path: Path,
    title_suffix: str,
) -> None:
    Ly, Lx = background.shape
    vmin, vmax = robust_image_limits(background)
    labels = np.unique(red_masks)
    labels = labels[labels > 0]
    labels_to_hide = red_labels_overlapping_yellow(
        functional_stats, yellow_mask, outlier_analysis_index, red_masks
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
        if i == outlier_analysis_index:
            continue
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
        if i == outlier_analysis_index:
            continue
        if yellow_mask[i]:
            draw_functional_roi_contour(
                ax,
                roi_stat,
                DISPLAY_YELLOW_COLOR,
                FUNCTIONAL_OUTLINE_LW,
                Ly,
                Lx,
            )

    draw_functional_roi_contour(
        ax,
        functional_stats[outlier_analysis_index],
        EXCLUDED_COLOR,
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
        Line2D([0], [0], color=EXCLUDED_COLOR, lw=1.5,
               label="Excluded outlier ROI"),
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
    for required in (ops_path, stat_path, redcell_path):
        if not required.exists():
            raise FileNotFoundError(f"Missing required Suite2p file:\n{required}")

    ops = np.load(ops_path, allow_pickle=True).item()
    stat_array = np.load(stat_path, allow_pickle=True)
    redcell_data = np.load(redcell_path)

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

    suite2p_chan2_scores = np.asarray(
        redcell_data[cell_roi_indices, 1], dtype=float
    )
    finite_score_mask = np.isfinite(suite2p_chan2_scores)
    finite_analysis_indices = np.flatnonzero(finite_score_mask)
    if len(finite_analysis_indices) == 0:
        raise ValueError("No finite legacy Suite2p chan2 scores.")
    outlier_analysis_index = int(
        finite_analysis_indices[
            np.argmin(suite2p_chan2_scores[finite_score_mask])
        ]
    )
    outlier_roi_index = int(cell_roi_indices[outlier_analysis_index])
    outlier_score = float(suite2p_chan2_scores[outlier_analysis_index])

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
    # Match the finalized notebook exactly: every non-yellow ROI is green
    # (including any NaN IoU), before the one excluded outlier is removed.
    yellow_cell_mask = cellpose_red_iou > IOU_THRESHOLD
    green_only_mask = ~yellow_cell_mask
    excluded_mask = np.zeros(n_analysis_cells, dtype=bool)
    excluded_mask[outlier_analysis_index] = True
    green_only_mask[excluded_mask] = False
    yellow_cell_mask[excluded_mask] = False
    classified_mask = green_only_mask | yellow_cell_mask

    n_green = int(np.sum(green_only_mask))
    n_yellow = int(np.sum(yellow_cell_mask))
    n_excluded = int(np.sum(excluded_mask))
    n_red_anatomical = int(len(np.unique(cellpose_red_masks)[np.unique(cellpose_red_masks) > 0]))
    print(
        f"Classification: green={n_green}, yellow={n_yellow}, "
        f"excluded={n_excluded}, red anatomical={n_red_anatomical}"
    )
    print(
        f"Excluded analysis index={outlier_analysis_index}, "
        f"Suite2p ROI={outlier_roi_index}, legacy score={outlier_score:.5f}"
    )

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
        outlier_analysis_index,
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
        outlier_analysis_index,
        session_output_dir / f"{subject}_{date}_{session}_p{plane}_chan1_classification_overlay.png",
        title_suffix,
    )

    # -------------------------------------------------------------------------
    # All-sounds eventlocked QC (same analyzed cell set).
    # -------------------------------------------------------------------------
    trialavg = np.nanmean(eventlocked[:, valid_events, :], axis=1)
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
    eventlocked_valid = eventlocked[:, valid_events, :]
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
    # Behavioral conditions and imaging/behavior alignment.
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
    n_behavior_trials = len(stim_type)
    n_imaging_events = eventlocked.shape[1]
    if n_imaging_events == n_behavior_trials + 1:
        eventlocked_aligned = eventlocked[:, :n_behavior_trials, :]
        valid_events_aligned = valid_events[:n_behavior_trials]
        alignment_note = "one extra imaging event at end; final event removed"
    elif n_imaging_events == n_behavior_trials:
        eventlocked_aligned = eventlocked
        valid_events_aligned = valid_events
        alignment_note = "imaging and behavioral trial counts matched"
    else:
        raise ValueError(
            f"Unexpected trial mismatch: {n_imaging_events} imaging events vs "
            f"{n_behavior_trials} behavioral trials."
        )

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

    fade_ratio = amplitude_ratio(fade_in_response, fade_out_response)
    fadein_bestam_ratio = amplitude_ratio(fade_in_response, best_am_response)
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
    cell_class = np.full(n_analysis_cells, "excluded", dtype=object)
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
            "fade_in_over_fade_out_abs_ratio": float(fade_ratio[i]),
            "fade_in_over_best_am_abs_ratio": float(fadein_bestam_ratio[i]),
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
        class_ratio_a = fade_ratio[class_mask]
        class_ratio_b = fadein_bestam_ratio[class_mask]
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
            "median_fade_in_over_fade_out_abs_ratio": (
                float(np.nanmedian(class_ratio_a)) if np.any(np.isfinite(class_ratio_a)) else np.nan
            ),
            "median_fade_in_over_best_am_abs_ratio": (
                float(np.nanmedian(class_ratio_b)) if np.any(np.isfinite(class_ratio_b)) else np.nan
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
        "outlier_analysis_index": outlier_analysis_index,
        "outlier_suite2p_roi": outlier_roi_index,
        "outlier_legacy_score": outlier_score,
        "cellpose_diameter": cellpose_diameter,
        "possible_am_rates": possible_am_rates,
        "condition_names": condition_names,
        "n_trials_each_condition": n_trials_each_condition,
        "alignment_note": alignment_note,
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
                "fade_ratio": float(fade_ratio[i]),
                "raster_responsive": bool(raster_responsive[i]),
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


def plot_ratio_violin(ax, green_values, yellow_values, title, p_value):
    datasets = [finite_values(green_values), finite_values(yellow_values)]
    positions = [0, 1]
    colors = [GREEN_COLOR, YELLOW_COLOR]
    rng = np.random.default_rng(5678)
    for pos, vals, color in zip(positions, datasets, colors):
        if len(vals) >= 2 and np.std(vals) > 0:
            vp = ax.violinplot([vals], positions=[pos], widths=0.75,
                               showmeans=False, showmedians=True, showextrema=False)
            for body in vp["bodies"]:
                body.set_facecolor(color)
                body.set_edgecolor(color)
                body.set_alpha(0.25)
            vp["cmedians"].set_color("black")
        if len(vals):
            jitter = rng.uniform(-0.08, 0.08, len(vals))
            ax.scatter(np.full(len(vals), pos) + jitter, vals, s=12, alpha=0.35,
                       color=color, edgecolors="none")
            m, se = mean_sem(vals)
            ax.errorbar(pos, m, yerr=se, fmt="o", color="black", capsize=4, zorder=4)
    ax.axhline(1, color="black", ls=":", lw=1)
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    p_text = "n/a" if p_value is None else f"{p_value:.3g}"
    ax.set_title(f"{title}\npooled-cell p={p_text}")
    ax.set_ylabel("Response-amplitude ratio")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)


def combined_sound_response_summary(
    cell_df: pd.DataFrame,
    trace_records: list[dict[str, Any]],
    am_rates: list[float],
    pooled_stats: dict[str, Any],
    output_path: Path,
    title: str,
) -> None:
    classified = cell_df[cell_df["cell_class"].isin(["green", "yellow"])].copy()
    green = classified[classified["cell_class"] == "green"]
    yellow = classified[classified["cell_class"] == "yellow"]

    fig = plt.figure(figsize=(24, 14), constrained_layout=True)
    outer = fig.add_gridspec(2, 2)
    gs_a = outer[0, 0].subgridspec(1, 3)
    gs_b = outer[0, 1].subgridspec(1, 3)
    gs_c = outer[1, 0].subgridspec(2, 3)
    ax_a1, ax_a2, ax_a3 = [fig.add_subplot(gs_a[0, i]) for i in range(3)]
    ax_b1, ax_b2, ax_b3 = [fig.add_subplot(gs_b[0, i]) for i in range(3)]
    example_axes = [fig.add_subplot(gs_c[r, c]) for r in range(2) for c in range(3)]
    ax_d = fig.add_subplot(outer[1, 1])

    plot_paired_cell_population(
        ax_a1, green["fade_in_response"], green["fade_out_response"],
        "Fade-in", "Fade-out", f"Green pooled cells\nn={len(green)}", GREEN_COLOR
    )
    plot_paired_cell_population(
        ax_a2, yellow["fade_in_response"], yellow["fade_out_response"],
        "Fade-in", "Fade-out", f"Yellow pooled cells\nn={len(yellow)}", YELLOW_COLOR
    )
    plot_ratio_violin(
        ax_a3,
        green["fade_in_over_fade_out_abs_ratio"],
        yellow["fade_in_over_fade_out_abs_ratio"],
        "|Fade-in| / |Fade-out|",
        pooled_stats["fade_ratio_green_vs_yellow"]["holm_p"],
    )

    plot_paired_cell_population(
        ax_b1, green["fade_in_response"], green["best_am_response"],
        "Fade-in", "Best AM", f"Green pooled cells\nn={len(green)}", GREEN_COLOR
    )
    plot_paired_cell_population(
        ax_b2, yellow["fade_in_response"], yellow["best_am_response"],
        "Fade-in", "Best AM", f"Yellow pooled cells\nn={len(yellow)}", YELLOW_COLOR
    )
    plot_ratio_violin(
        ax_b3,
        green["fade_in_over_best_am_abs_ratio"],
        yellow["fade_in_over_best_am_abs_ratio"],
        "|Fade-in| / |Best AM|",
        pooled_stats["fade_bestam_ratio_green_vs_yellow"]["holm_p"],
    )

    # Top pooled examples by FI/FO ratio, restricted to the notebook raster-response threshold.
    for row_idx, class_name in enumerate(["green", "yellow"]):
        candidates = [
            r for r in trace_records
            if r["cell_class"] == class_name
            and r["raster_responsive"]
            and np.isfinite(r["fade_ratio"])
        ]
        candidates.sort(key=lambda r: r["fade_ratio"], reverse=True)
        for col_idx in range(3):
            ax = example_axes[row_idx * 3 + col_idx]
            if col_idx >= len(candidates):
                ax.axis("off")
                continue
            r = candidates[col_idx]
            ax.plot(r["tvec"], r["fade_in_trace"], color=FADE_IN_COLOR, lw=2, label="Fade-in")
            ax.plot(r["tvec"], r["fade_out_trace"], color=FADE_OUT_COLOR, lw=2, label="Fade-out")
            ax.axvline(0, color="black", ls="--", lw=1)
            ax.axhline(0, color="black", ls=":", lw=1)
            ax.set_title(
                f"{class_name.capitalize()} | {r['date']} {r['session']}\n"
                f"ROI {r['suite2p_roi']} | |FI|/|FO|={r['fade_ratio']:.2f}"
            )
            ax.set_xlabel("Time from sound onset (s)")
            ax.set_ylabel("Baseline-subtracted dF/F")
            ax.grid(axis="y", alpha=0.2)
            ax.spines[["top", "right"]].set_visible(False)
        if row_idx == 0 and candidates:
            example_axes[0].legend(frameon=False, fontsize=8)

    # AM response profiles, pooled cells. Individual lines remain descriptive.
    x = np.arange(len(am_rates))
    for class_name, class_df, color, offset in [
        ("green", green, GREEN_COLOR, -0.04),
        ("yellow", yellow, YELLOW_COLOR, 0.04),
    ]:
        matrix = []
        for rate in am_rates:
            col = f"am_response_{rate:g}Hz"
            matrix.append(class_df[col].to_numpy(dtype=float) if col in class_df else np.full(len(class_df), np.nan))
        matrix = np.column_stack(matrix) if matrix else np.empty((len(class_df), 0))
        for row in matrix:
            ax_d.plot(x, row, color=color, alpha=0.06 if class_name == "green" else 0.12, lw=0.6)
        mean = np.nanmean(matrix, axis=0) if len(matrix) else np.full(len(am_rates), np.nan)
        n = np.sum(np.isfinite(matrix), axis=0)
        sem = np.full(len(am_rates), np.nan)
        valid = n > 1
        if np.any(valid):
            sem[valid] = np.nanstd(matrix[:, valid], axis=0, ddof=1) / np.sqrt(n[valid])
        ax_d.errorbar(x + offset, mean, yerr=sem, marker="o", capsize=4, lw=2.5,
                      color=color, label=f"{class_name.capitalize()} (n={len(class_df)})")
    ax_d.axhline(0, color="black", ls=":", lw=1)
    ax_d.set_xticks(x, [f"{r:g}" for r in am_rates])
    ax_d.set_xlabel("AM rate (Hz)")
    ax_d.set_ylabel("Mean baseline-subtracted dF/F")
    ax_d.set_title("AM-rate response profiles (pooled cells)")
    ax_d.legend(frameon=False)
    ax_d.grid(axis="y", alpha=0.2)
    ax_d.spines[["top", "right"]].set_visible(False)

    ax_a1.text(-0.32, 1.10, "A", transform=ax_a1.transAxes, fontsize=18, fontweight="bold")
    ax_b1.text(-0.32, 1.10, "B", transform=ax_b1.transAxes, fontsize=18, fontweight="bold")
    example_axes[0].text(-0.32, 1.15, "C", transform=example_axes[0].transAxes, fontsize=18, fontweight="bold")
    ax_d.text(-0.10, 1.05, "D", transform=ax_d.transAxes, fontsize=18, fontweight="bold")
    fig.suptitle(title + "\nPooled-cell panels are descriptive/exploratory", fontsize=15)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def combined_condition_response_plot(cell_df: pd.DataFrame, am_rates: list[float], output_path: Path, title: str) -> None:
    condition_cols = ["fade_in_response", "fade_out_response"] + [f"am_response_{r:g}Hz" for r in am_rates]
    labels = ["Fade-in", "Fade-out"] + [f"AM {r:g}" for r in am_rates]
    x = np.arange(len(condition_cols), dtype=float)
    if len(am_rates):
        x[2:] += 0.7

    fig, axes = plt.subplots(1, 4, figsize=(22, 6), constrained_layout=True)
    groups = [
        ("All classified", cell_df[cell_df["cell_class"].isin(["green", "yellow"])], "black"),
        ("Green", cell_df[cell_df["cell_class"] == "green"], GREEN_COLOR),
        ("Yellow", cell_df[cell_df["cell_class"] == "yellow"], YELLOW_COLOR),
    ]
    rng = np.random.default_rng(31415)
    for ax, (group_name, df, color) in zip(axes[:3], groups):
        for ci, col in enumerate(condition_cols):
            if col not in df:
                continue
            vals = finite_values(df[col])
            if not len(vals):
                continue
            jitter = rng.uniform(-0.08, 0.08, len(vals))
            ax.scatter(np.full(len(vals), x[ci]) + jitter, vals, s=10, alpha=0.25,
                       color=color, edgecolors="none")
            m, se = mean_sem(vals)
            ax.errorbar(x[ci], m, yerr=se, fmt="o", color="black", capsize=3)
        ax.axhline(0, color="black", ls=":", lw=1)
        ax.set_xticks(x, labels, rotation=45, ha="right")
        ax.set_title(f"{group_name}\nn={len(df)} cells")
        ax.set_ylabel("Mean baseline-subtracted dF/F")
        ax.grid(axis="y", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)

    ax = axes[3]
    for class_name, color, offset in [("green", GREEN_COLOR, -0.05), ("yellow", YELLOW_COLOR, 0.05)]:
        df = cell_df[cell_df["cell_class"] == class_name]
        means, sems = [], []
        for col in condition_cols:
            vals = df[col] if col in df else np.array([])
            m, se = mean_sem(vals)
            means.append(m)
            sems.append(se)
        ax.errorbar(x + offset, means, yerr=sems, marker="o", capsize=4, lw=2,
                    color=color, label=f"{class_name.capitalize()} (n={len(df)})")
    ax.axhline(0, color="black", ls=":", lw=1)
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_title("Green vs yellow mean ± SEM")
    ax.set_ylabel("Mean baseline-subtracted dF/F")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def combined_selectivity_raster_preference_and_ratio(
    cell_df: pd.DataFrame,
    am_rates: list[float],
    output_path: Path,
    title: str,
) -> None:
    """Combined version of the notebook's 3 x 2 selectivity raster figure.

    Rows: all / green / yellow amplitude-responsive cells.
    Columns: preferred-condition sort / |FI|:|FO| ratio sort.
    """
    condition_cols = ["fade_in_response", "fade_out_response"] + [
        f"am_response_{r:g}Hz" for r in am_rates
    ]
    labels = ["FI", "FO"] + [f"AM {r:g}" for r in am_rates]
    responsive = cell_df[
        cell_df["cell_class"].isin(["green", "yellow"])
        & (cell_df["raster_responsive"] == True)  # noqa: E712
    ].copy()

    fig, axes = plt.subplots(3, 2, figsize=(15, 18), constrained_layout=True)
    im = None
    groups = [
        ("All responsive", responsive),
        ("Green responsive", responsive[responsive["cell_class"] == "green"]),
        ("Yellow responsive", responsive[responsive["cell_class"] == "yellow"]),
    ]

    for row_idx, (group_name, df) in enumerate(groups):
        if len(df) == 0:
            for col_idx in range(2):
                axes[row_idx, col_idx].text(
                    0.5, 0.5, "No responsive cells",
                    transform=axes[row_idx, col_idx].transAxes,
                    ha="center", va="center"
                )
                axes[row_idx, col_idx].set_title(group_name)
            continue

        matrix = np.column_stack([
            df[col].to_numpy(dtype=float)
            if col in df else np.full(len(df), np.nan)
            for col in condition_cols
        ])
        norm = np.nanmax(np.abs(matrix), axis=1, keepdims=True)
        norm[(~np.isfinite(norm)) | (norm <= 0)] = np.nan
        normalized = matrix / norm

        # Preferred condition = largest signed response. Sort by condition then
        # strongest preferred response within condition, matching the notebook.
        pref_idx = np.nanargmax(matrix, axis=1)
        pref_response = np.nanmax(matrix, axis=1)
        pref_order = np.lexsort((-pref_response, pref_idx))
        pref_sorted = normalized[pref_order]

        # |FI| / |FO|, descending; invalid ratios go to the bottom.
        ratio = amplitude_ratio(matrix[:, 0], matrix[:, 1])
        ratio_sort_values = np.where(np.isfinite(ratio), ratio, -np.inf)
        ratio_order = np.argsort(ratio_sort_values)[::-1]
        ratio_sorted = normalized[ratio_order]

        for col_idx, (plot_matrix, subtitle) in enumerate([
            (pref_sorted, "sorted by preferred condition"),
            (ratio_sorted, "sorted by |FI| / |FO|"),
        ]):
            ax = axes[row_idx, col_idx]
            im = ax.imshow(
                plot_matrix,
                aspect="auto",
                interpolation="nearest",
                cmap="coolwarm",
                vmin=-1,
                vmax=1,
            )
            ax.set_title(f"{group_name} — {subtitle}\nn={len(df)}")
            ax.set_xticks(np.arange(len(labels)), labels, rotation=45, ha="right")
            ax.set_ylabel("Cells")
            ax.set_xlabel("Sound condition")

        # Preferred-condition boundaries on the left panel.
        counts = np.bincount(pref_idx, minlength=len(condition_cols))
        cumulative = np.cumsum(counts)
        for boundary in cumulative[:-1]:
            if boundary > 0:
                axes[row_idx, 0].axhline(boundary - 0.5, color="white", lw=0.7, alpha=0.8)

    if im is not None:
        cbar = fig.colorbar(im, ax=axes, shrink=0.65)
        cbar.set_label("Response / max absolute response per cell")
    fig.suptitle(
        title + f"\nRaster criterion: max |condition response| > {RASTER_MIN_ABS_RESPONSE:.3f}",
        fontsize=14,
    )
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


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
    pivot = class_summary_df.pivot(index="session_key", columns="cell_class")
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)
    panels = [
        ("pct_sound_responsive_fdr", "Sound-responsive cells (%)",
         session_stats["responsive_fraction_green_vs_yellow"]),
        ("median_fade_in_over_fade_out_abs_ratio", "Median |FI| / |FO|",
         session_stats["fade_ratio_green_vs_yellow"]),
        ("median_fade_in_over_best_am_abs_ratio", "Median |FI| / |best AM|",
         session_stats["fade_bestam_ratio_green_vs_yellow"]),
        ("mean_fade_in_response", "Mean fade-in response",
         session_stats["fade_in_green_vs_yellow"]),
    ]
    rng = np.random.default_rng(2718)
    for ax, (metric, ylabel, stat_result) in zip(axes.flat, panels):
        if metric not in pivot:
            ax.axis("off")
            continue
        green = pivot[metric].get("green", pd.Series(dtype=float))
        yellow = pivot[metric].get("yellow", pd.Series(dtype=float))
        common = green.index.intersection(yellow.index)
        gv = green.loc[common].to_numpy(dtype=float)
        yv = yellow.loc[common].to_numpy(dtype=float)
        valid = np.isfinite(gv) & np.isfinite(yv)
        gv, yv = gv[valid], yv[valid]
        for g, y in zip(gv, yv):
            ax.plot([0, 1], [g, y], color="0.6", alpha=0.6, lw=1)
        ax.scatter(np.zeros(len(gv)) + rng.uniform(-0.03, 0.03, len(gv)), gv,
                   color=GREEN_COLOR, s=35, zorder=3)
        ax.scatter(np.ones(len(yv)) + rng.uniform(-0.03, 0.03, len(yv)), yv,
                   color=YELLOW_COLOR, edgecolor="black", linewidth=0.3, s=40, zorder=3)
        p = stat_result.get("p")
        p_text = "n/a" if p is None else f"{p:.3g}"
        ax.set_title(f"paired sessions n={len(gv)} | Wilcoxon p={p_text}")
        ax.set_xticks([0, 1], ["Green", "Yellow"])
        ax.set_ylabel(ylabel)
        ax.grid(axis="y", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(title + "\nSession-level paired summaries", fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


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
    fig.suptitle(title, fontsize=14)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# COMBINED STATISTICS
# =============================================================================

def compute_combined_statistics(
    cell_df: pd.DataFrame,
    class_summary_df: pd.DataFrame,
) -> tuple[dict[str, Any], dict[str, Any]]:
    classified = cell_df[cell_df["cell_class"].isin(["green", "yellow"])]
    green = classified[classified["cell_class"] == "green"]
    yellow = classified[classified["cell_class"] == "yellow"]

    # Notebook-equivalent pooled-cell comparisons (exploratory).
    ratio_a = safe_mannwhitney(
        green["fade_in_over_fade_out_abs_ratio"],
        yellow["fade_in_over_fade_out_abs_ratio"],
    )
    ratio_b = safe_mannwhitney(
        green["fade_in_over_best_am_abs_ratio"],
        yellow["fade_in_over_best_am_abs_ratio"],
    )
    corrected = holm_correct([
        np.nan if ratio_a["p"] is None else float(ratio_a["p"]),
        np.nan if ratio_b["p"] is None else float(ratio_b["p"]),
    ])
    ratio_a["holm_p"] = None if not np.isfinite(corrected[0]) else float(corrected[0])
    ratio_b["holm_p"] = None if not np.isfinite(corrected[1]) else float(corrected[1])

    yellow_fade = finite_values(yellow["fade_in_response"])
    green_fade = finite_values(green["fade_in_response"])
    pooled = {
        "note": "Pooled-cell tests are descriptive/exploratory; cells from the same session are not independent biological replicates.",
        "fade_ratio_green_vs_yellow": ratio_a,
        "fade_bestam_ratio_green_vs_yellow": ratio_b,
        "fade_in_yellow_vs_zero_two_sided": safe_wilcoxon(yellow_fade, "two-sided"),
        "fade_in_yellow_less_than_zero": safe_wilcoxon(yellow_fade, "less"),
        "fade_in_yellow_vs_green": safe_mannwhitney(yellow_fade, green_fade),
    }
    try:
        g_resp = int(np.sum(green["sound_responsive_fdr"].astype(bool)))
        y_resp = int(np.sum(yellow["sound_responsive_fdr"].astype(bool)))
        contingency = [[g_resp, len(green) - g_resp], [y_resp, len(yellow) - y_resp]]
        fisher = stats.fisher_exact(contingency)
        pooled["responsive_fraction_fisher_green_vs_yellow"] = {
            "odds_ratio": float(fisher.statistic),
            "p": float(fisher.pvalue),
            "table": contingency,
        }
    except Exception:
        pooled["responsive_fraction_fisher_green_vs_yellow"] = {
            "odds_ratio": None, "p": None, "table": None
        }

    # Session-level paired inference.
    pivot = class_summary_df.pivot(index="session_key", columns="cell_class")

    def paired_metric(metric: str, alternative: str = "two-sided") -> dict[str, Any]:
        if metric not in pivot or "green" not in pivot[metric] or "yellow" not in pivot[metric]:
            return {"statistic": None, "p": None, "n_pairs": 0}
        return safe_paired_wilcoxon(
            pivot[metric]["green"].to_numpy(dtype=float),
            pivot[metric]["yellow"].to_numpy(dtype=float),
            alternative=alternative,
        )

    session_level = {
        "note": "Primary across-session comparisons use one GREEN and one YELLOW summary per session when both are available.",
        "responsive_fraction_green_vs_yellow": paired_metric("pct_sound_responsive_fdr"),
        "fade_ratio_green_vs_yellow": paired_metric("median_fade_in_over_fade_out_abs_ratio"),
        "fade_bestam_ratio_green_vs_yellow": paired_metric("median_fade_in_over_best_am_abs_ratio"),
        "fade_in_green_vs_yellow": paired_metric("mean_fade_in_response"),
    }
    # Yellow session mean fade-in response < 0.
    if "mean_fade_in_response" in pivot and "yellow" in pivot["mean_fade_in_response"]:
        session_level["yellow_mean_fade_in_less_than_zero"] = safe_wilcoxon(
            pivot["mean_fade_in_response"]["yellow"].to_numpy(dtype=float),
            alternative="less",
        )
    else:
        session_level["yellow_mean_fade_in_less_than_zero"] = {
            "statistic": None, "p": None, "n": 0
        }

    # Holm correction across the same two planned ratio comparisons.
    ratio_session_ps = [
        session_level["fade_ratio_green_vs_yellow"]["p"],
        session_level["fade_bestam_ratio_green_vs_yellow"]["p"],
    ]
    corrected_session = holm_correct([
        np.nan if p is None else float(p) for p in ratio_session_ps
    ])
    session_level["fade_ratio_green_vs_yellow"]["holm_p"] = (
        None if not np.isfinite(corrected_session[0]) else float(corrected_session[0])
    )
    session_level["fade_bestam_ratio_green_vs_yellow"]["holm_p"] = (
        None if not np.isfinite(corrected_session[1]) else float(corrected_session[1])
    )
    return pooled, session_level


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
    stats_payload = {
        "pooled_cell_exploratory": pooled_stats,
        "session_level_primary": session_stats,
        "n_successful_sessions": len(session_results),
        "n_failed_sessions": len(failures),
        "n_cells_total_rows": len(cell_df),
        "n_green_pooled": int(np.sum(cell_df["cell_class"] == "green")),
        "n_yellow_pooled": int(np.sum(cell_df["cell_class"] == "yellow")),
        "am_rates": all_am_rates,
    }
    save_json(combined_dir / "combined_statistics.json", stats_payload)

    title = (
        f"{subject} | {area} | {', '.join(dates)} | "
        f"{len(session_results)} successful sound_tuning sessions"
    )

    combined_condition_response_plot(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_condition_responses_green_yellow.png",
        title,
    )
    combined_selectivity_raster_preference_and_ratio(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_selectivity_rasters_preference_and_ratio.png",
        title,
    )
    combined_selectivity_raster(
        cell_df,
        all_am_rates,
        combined_dir / "combined_sound_selectivity_raster_looming_score.png",
        title,
    )
    combined_sound_response_summary(
        cell_df,
        trace_records,
        all_am_rates,
        pooled_stats,
        combined_dir / "combined_green_yellow_sound_response_summary.png",
        title,
    )
    session_level_figure(
        class_summary_df,
        combined_dir / "combined_session_level_green_yellow_comparisons.png",
        title,
        session_stats,
    )
    combined_fade_in_suppression_plot(
        cell_df,
        class_summary_df,
        combined_dir / "combined_fade_in_suppression_green_yellow.png",
        title,
        pooled_stats,
        session_stats,
    )

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
