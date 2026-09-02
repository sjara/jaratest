#!/usr/bin/env python3
"""
Compare YELLOW versus GREEN AM-tuning responses within each AREA x LAYER stratum.

This is the layer follow-up analysis for am_tuning_area_analysis_v9.py.
It does NOT rerun Suite2p, Cellpose, or event alignment. Instead it loads the
already-saved combined outputs for each area and asks questions such as:

    Within A2 L2/3, do YELLOW cells show stronger tuning selectivity than GREEN cells?
    Within A1 L4/5, do YELLOW and GREEN cells differ at specific frequencies / AM rates?

Analyses are run independently for:
    tuningFreq
    tuningAM

and independently for six AREA x LAYER combinations:
    A1  x L2/3   100 <= depth < 300 um
    A1  x L4/5   300 <= depth <= 600 um
    AAF x L2/3   100 <= depth < 300 um
    AAF x L4/5   300 <= depth <= 600 um
    A2  x L2/3   100 <= depth < 300 um
    A2  x L4/5   300 <= depth <= 600 um

The 300-um boundary is assigned to L4/5 so no session is counted twice.

PRIMARY INFERENCE
-----------------
GREEN and YELLOW cells are recorded in the same imaging sessions. Therefore the
primary inference is SESSION-LEVEL and PAIRED. Each session contributes one
GREEN summary and one YELLOW summary when both classes have usable values, and
paired Wilcoxon signed-rank tests compare YELLOW versus GREEN.

Pooled-cell Mann-Whitney / Fisher tests are also saved, but are explicitly
labeled exploratory because cells within the same session are not independent
biological replicates.

For tuning curves and intensity-resolved condition responses, the script also
computes paired GREEN-vs-YELLOW session-level tests separately at every tuning
value or tuning-value x intensity condition, with Holm correction across all
conditions in the corresponding output table.

CURRENT TUNING-SELECTIVITY CONVENTION
-------------------------------------
The primary tuning-selectivity metric is lifetime sparseness across the absolute
magnitude tuning profile r_i = |R_i|, where R_i is the mean baseline-corrected
0-1 s dF/F response at frequency or AM-rate i.  Separate GREEN-vs-YELLOW
comparisons are also generated for the Gini coefficient, tuning-profile Fano
factor, and FWHM bandwidth. Frequency FWHM is in octaves; AM-rate FWHM is in Hz.
Legacy best-vs-rest contrast/index outputs remain available upstream but are not part of the retained primary layer-level figure/statistics family.

V9 RESPONSIVENESS / SENSITIVITY CONVENTION
------------------------------------------
Primary responsiveness is BH-FDR separately across cells at each tuning value,
with stim_responsive_fdr defined as the union across tuning values. Layer plots
show both overall responsiveness and tuning-value-specific responsiveness.
Whole-session-median and 60-s local prestimulus-median dF/F are retained as
sensitivity analyses for the primary lifetime-sparseness metric; they do not
redefine the primary v9 responsive-cell set.

All real frequency / AM-rate axes use explicit octave coordinates x = log2(value)
for plotting, while tick labels show the original kHz / Hz values. This guarantees
that equal ratios (for example 2->4 kHz and 20->40 kHz) occupy exactly the same
physical width. Categorical GREEN/YELLOW axes remain linear.

PREREQUISITE OUTPUTS
--------------------
For each requested area and tuning mode, this script expects:

<TEMP_OUTPUT_PATH>/evan/am_tuning_area_analysis/<subject>/<area>/<date_tag>/
    <tuning_mode>/combined/combined_cell_results.csv
    <tuning_mode>/combined/combined_condition_results.csv

These are produced by am_tuning_area_analysis_v9.py. The v9 primary responsiveness flag is the union of tuning-value-specific BH-FDR discoveries.

Examples
--------
Run both tuning modes:

python am_tuning_area_layer_green_yellow_analysis.py imag039 \
    --dates 20260717 20260729 20260730

Only frequency tuning:

python am_tuning_area_layer_green_yellow_analysis.py imag039 \
    --dates 20260717 20260729 20260730 --mode tuningFreq

Dry run:

python am_tuning_area_layer_green_yellow_analysis.py imag039 \
    --dates 20260717 20260729 20260730 --dry-run
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats

from jaratoolbox import settings


# =============================================================================
# CONSTANTS
# =============================================================================

AREAS = ("A1", "AAF", "A2")
CELL_CLASSES = ("green", "yellow")
TUNING_MODES = ("tuningFreq", "tuningAM")
CELL_CLASS_COLORS = {"green": "limegreen", "yellow": "goldenrod"}

LAYERS = {
    "L23_100to300um": (100.0, 300.0, "L2/3 (100-<300 um)"),
    "L45_300to600um": (300.0, 600.0, "L4/5 (300-600 um)"),
}

DPI = 180

CONTINUOUS_METRICS = {
    "stim_response_mean": {
        "label": "Mean stimulus response (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "best_tuning_response": {
        "label": "Best tuning response (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "peak_absolute_response": {
        "label": "Peak absolute response (|dF/F|)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "tuning_modulation_depth": {
        "label": "Tuning modulation depth (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    # Primary and comparison tuning-selectivity metrics from am_tuning_area_analysis_v9.py.
    "tuning_lifetime_sparseness": {
        "label": "Lifetime sparseness",
        "session_agg": "mean",
        "reference": None,
    },
    "tuning_gini_coefficient": {
        "label": "Gini coefficient",
        "session_agg": "mean",
        "reference": None,
    },
    "tuning_fano_factor": {
        "label": "Tuning-profile Fano factor",
        "session_agg": "mean",
        "reference": None,
    },
    "tuning_fwhm": {
        "label": "FWHM tuning bandwidth",
        "session_agg": "mean",
        "reference": None,
    },
    # Legacy best-vs-rest metrics retained for backward-compatible descriptive output.
    "tuning_selectivity_contrast": {
        "label": "Legacy best-vs-rest selectivity contrast (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "tuning_selectivity_index": {
        "label": "Legacy best-vs-rest selectivity index",
        "session_agg": "mean",
        "reference": 0.0,
    },
}

SELECTIVITY_METRICS = (
    "tuning_lifetime_sparseness",
    "tuning_gini_coefficient",
    "tuning_fano_factor",
    "tuning_fwhm",
)


BINARY_METRICS = {
    "stim_responsive_fdr": ("pct_stim_responsive_fdr", "FDR stimulus-responsive cells (%)"),
    "stim_excited_fdr": ("pct_stim_excited_fdr", "FDR excited cells (%)"),
    "stim_suppressed_fdr": ("pct_stim_suppressed_fdr", "FDR suppressed cells (%)"),
}


# =============================================================================
# ARGUMENTS / PATHS
# =============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("subject", help="Subject ID, e.g. imag039.")
    parser.add_argument("--dates", nargs="+", required=True, help="Dates used for the prerequisite AM area analyses.")
    parser.add_argument("--areas", nargs="+", default=list(AREAS), choices=list(AREAS), help="Areas to analyze. Default: A1 AAF A2.")
    parser.add_argument("--mode", choices=["both", *TUNING_MODES], default="both", help="Analyze tuningFreq, tuningAM, or both (default).")
    parser.add_argument("--dry-run", action="store_true", help="Print expected inputs and outputs and stop.")
    return parser.parse_args()


def date_tag(dates: Iterable[str]) -> str:
    return "_".join(str(d) for d in dates)


def area_mode_dir(subject: str, area: str, dates: list[str], mode: str) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH) / "evan" / "am_tuning_area_analysis"
        / subject / area / date_tag(dates) / mode / "combined"
    )


def expected_area_cell_csv(subject: str, area: str, dates: list[str], mode: str) -> Path:
    return area_mode_dir(subject, area, dates, mode) / "combined_cell_results.csv"


def expected_area_condition_csv(subject: str, area: str, dates: list[str], mode: str) -> Path:
    return area_mode_dir(subject, area, dates, mode) / "combined_condition_results.csv"


def output_root(subject: str, dates: list[str]) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH) / "evan" / "am_tuning_area_layer_green_yellow_analysis"
        / subject / date_tag(dates)
    )


# =============================================================================
# GENERAL UTILITIES
# =============================================================================

def json_default(obj: Any) -> Any:
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(obj, f, indent=2, default=json_default)


def _coerce_bool(df: pd.DataFrame, col: str) -> None:
    if col not in df.columns:
        return
    if df[col].dtype != bool:
        df[col] = df[col].astype(str).str.lower().isin(["true", "1", "yes"])


def finite_values(values: Iterable[Any]) -> np.ndarray:
    arr = pd.to_numeric(pd.Series(values), errors="coerce").to_numpy(dtype=float)
    return arr[np.isfinite(arr)]


def mean_sem(values: Iterable[Any]) -> tuple[float, float, int]:
    vals = finite_values(values)
    n = len(vals)
    if n == 0:
        return np.nan, np.nan, 0
    mean = float(np.mean(vals))
    sem = float(stats.sem(vals, nan_policy="omit")) if n > 1 else np.nan
    return mean, sem, n


def mean_sd_sem(values: Iterable[Any]) -> tuple[float, float, float, int]:
    vals = finite_values(values)
    n = len(vals)
    if n == 0:
        return np.nan, np.nan, np.nan, 0
    mean = float(np.mean(vals))
    sd = float(np.std(vals, ddof=1)) if n > 1 else np.nan
    sem = float(sd / np.sqrt(n)) if n > 1 else np.nan
    return mean, sd, sem, n


def median_iqr(values: Iterable[Any]) -> tuple[float, float, float, int]:
    vals = finite_values(values)
    if len(vals) == 0:
        return np.nan, np.nan, np.nan, 0
    return (
        float(np.median(vals)), float(np.percentile(vals, 25)),
        float(np.percentile(vals, 75)), len(vals),
    )


def holm_adjust(p_values: list[float]) -> list[float]:
    p = np.asarray(p_values, dtype=float)
    out = np.full_like(p, np.nan)
    idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0:
        return out.tolist()
    order = idx[np.argsort(p[idx])]
    running = 0.0
    m = len(order)
    for rank, ii in enumerate(order):
        adj = min(1.0, (m-rank) * p[ii])
        running = max(running, adj)
        out[ii] = running
    return out.tolist()


def cliffs_delta(yellow: Iterable[Any], green: Iterable[Any]) -> float:
    y = finite_values(yellow)
    g = finite_values(green)
    if len(y) == 0 or len(g) == 0:
        return np.nan
    ranks = stats.rankdata(np.concatenate([y, g]))
    ry = np.sum(ranks[:len(y)])
    u = ry - len(y)*(len(y)+1)/2
    return float((2*u)/(len(y)*len(g)) - 1)


def safe_mannwhitney(yellow: Iterable[Any], green: Iterable[Any]) -> dict[str, Any]:
    y = finite_values(yellow)
    g = finite_values(green)
    if len(y) == 0 or len(g) == 0:
        return {"n_yellow":len(y), "n_green":len(g), "U":np.nan, "p":np.nan, "cliffs_delta_yellow_minus_green":np.nan}
    try:
        res = stats.mannwhitneyu(y, g, alternative="two-sided")
        return {
            "n_yellow":len(y), "n_green":len(g), "U":float(res.statistic),
            "p":float(res.pvalue), "cliffs_delta_yellow_minus_green":cliffs_delta(y, g),
        }
    except Exception:
        return {"n_yellow":len(y), "n_green":len(g), "U":np.nan, "p":np.nan, "cliffs_delta_yellow_minus_green":np.nan}


def safe_wilcoxon_pairs(yellow: Iterable[Any], green: Iterable[Any]) -> dict[str, Any]:
    y = pd.to_numeric(pd.Series(yellow), errors="coerce").to_numpy(float)
    g = pd.to_numeric(pd.Series(green), errors="coerce").to_numpy(float)
    valid = np.isfinite(y) & np.isfinite(g)
    y = y[valid]; g = g[valid]
    diff = y - g
    n = len(diff)
    if n == 0:
        return {
            "n_paired_sessions":0, "W":np.nan, "p":np.nan,
            "mean_difference_yellow_minus_green":np.nan,
            "sem_difference":np.nan,
            "median_difference_yellow_minus_green":np.nan,
            "q1_difference":np.nan, "q3_difference":np.nan,
        }
    q1, q3 = np.percentile(diff, [25, 75])
    if n < 2:
        W, p = np.nan, np.nan
    elif np.allclose(diff, 0, equal_nan=False):
        W, p = 0.0, 1.0
    else:
        try:
            res = stats.wilcoxon(y, g, alternative="two-sided", zero_method="wilcox")
            W, p = float(res.statistic), float(res.pvalue)
        except Exception:
            W, p = np.nan, np.nan
    return {
        "n_paired_sessions":n, "W":W, "p":p,
        "mean_difference_yellow_minus_green":float(np.mean(diff)),
        "sem_difference":float(stats.sem(diff)) if n > 1 else np.nan,
        "median_difference_yellow_minus_green":float(np.median(diff)),
        "q1_difference":float(q1), "q3_difference":float(q3),
    }


def fisher_green_yellow(df: pd.DataFrame, binary_col: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    counts = {}
    for cls in CELL_CLASSES:
        cdf = df[df.cell_class == cls]
        n = len(cdf)
        pos = int(cdf[binary_col].astype(bool).sum()) if n else 0
        counts[cls] = (pos, n)
        out[cls] = {"n_cells":n, "positive":pos, "percent":100*pos/n if n else np.nan}
    gp, gn = counts["green"]
    yp, yn = counts["yellow"]
    if gn == 0 or yn == 0:
        odds, p = np.nan, np.nan
    else:
        odds, p = stats.fisher_exact([[yp, yn-yp], [gp, gn-gp]])
    out["yellow_vs_green_fisher"] = {
        "odds_ratio":float(odds) if np.isfinite(odds) else np.nan,
        "p":float(p) if np.isfinite(p) else np.nan,
    }
    return out


def p_text(p: float) -> str:
    if not np.isfinite(p):
        return "p=n/a"
    if p < 1e-4:
        return "p<1e-4"
    return f"p={p:.4f}"


# =============================================================================
# LOAD / FILTER DATA
# =============================================================================

def load_mode_tables(
    subject: str, dates: list[str], areas: list[str], mode: str,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, dict[str, str]]]:
    cell_frames = []
    cond_frames = []
    missing = []
    provenance: dict[str, dict[str, str]] = {}

    for area in areas:
        cp = expected_area_cell_csv(subject, area, dates, mode)
        qp = expected_area_condition_csv(subject, area, dates, mode)
        provenance[area] = {"cell":str(cp), "condition":str(qp)}
        if not cp.exists(): missing.append(cp)
        if not qp.exists(): missing.append(qp)
        if not cp.exists() or not qp.exists():
            continue
        cdf = pd.read_csv(cp)
        qdf = pd.read_csv(qp)
        for df, path in ((cdf, cp), (qdf, qp)):
            if "canonicalArea" not in df.columns:
                raise ValueError(f"{path} has no canonicalArea column; expected am_tuning_area_analysis_v9.py output.")
            bad = set(df.canonicalArea.dropna().astype(str).unique()) - {area}
            if bad:
                raise ValueError(f"{path} contains unexpected canonicalArea values: {sorted(bad)}")
            if "tuning_mode" not in df.columns:
                raise ValueError(f"{path} has no tuning_mode column.")
            badmode = set(df.tuning_mode.dropna().astype(str).unique()) - {mode}
            if badmode:
                raise ValueError(f"{path} contains unexpected tuning_mode values: {sorted(badmode)}")
        cell_frames.append(cdf)
        cond_frames.append(qdf)

    if missing:
        msg = "Missing prerequisite AM area-analysis output(s):\n" + "\n".join(f"  {p}" for p in missing)
        msg += "\nRun am_tuning_area_analysis_v9.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)
    if not cell_frames:
        raise RuntimeError(f"No {mode} area tables were loaded.")

    cells = pd.concat(cell_frames, ignore_index=True, sort=False)
    conds = pd.concat(cond_frames, ignore_index=True, sort=False)

    req_cells = {
        "subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode",
        "stim_responsive_fdr","any_tuning_value_responsive_fdr","stim_excited_fdr","stim_suppressed_fdr","stim_response_mean",
        "best_tuning_response","peak_absolute_response","tuning_modulation_depth",
        "tuning_selectivity_contrast","tuning_selectivity_index","preferred_tuning_value_Hz",
        "tuning_lifetime_sparseness","tuning_gini_coefficient",
        "tuning_fano_factor","tuning_fwhm",
        "tuning_lifetime_sparseness_session_median_dff", "tuning_lifetime_sparseness_60s_prestim_median_dff",
    }
    miss = sorted(req_cells - set(cells.columns))
    if miss:
        raise ValueError("Combined AM cell table(s) are missing required columns: " + ", ".join(miss))

    req_cond = {
        "subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode",
        "stim_responsive_fdr","tuning_value_Hz","intensity_dB","condition_response","condition_selectivity_contrast",
    }
    miss = sorted(req_cond - set(conds.columns))
    if miss:
        raise ValueError("Combined AM condition table(s) are missing required columns: " + ", ".join(miss))

    cells["depth"] = pd.to_numeric(cells.depth, errors="coerce")
    conds["depth"] = pd.to_numeric(conds.depth, errors="coerce")
    for col in BINARY_METRICS:
        _coerce_bool(cells, col)
    for col in [c for c in cells.columns if c.startswith("tuning_value_responsive_fdr_")]:
        _coerce_bool(cells, col)
    _coerce_bool(conds, "stim_responsive_fdr")
    cells = cells[cells.cell_class.isin(CELL_CLASSES)].copy()
    conds = conds[conds.cell_class.isin(CELL_CLASSES)].copy()
    return cells, conds, provenance

def subset_layer(df: pd.DataFrame, layer_key: str) -> pd.DataFrame:
    low, high, _ = LAYERS[layer_key]
    depth = pd.to_numeric(df.depth, errors="coerce")
    if layer_key.startswith("L23"):
        mask = (depth >= low) & (depth < high)
    else:
        mask = (depth >= low) & (depth <= high)
    return df.loc[mask].copy()


# =============================================================================
# TUNING HELPERS / SESSION AGGREGATION
# =============================================================================

def response_columns(df: pd.DataFrame, mode: str, suffix: str = "") -> tuple[list[str], np.ndarray, list[str]]:
    base_prefix = "response_freq_" if mode == "tuningFreq" else "response_AM_"
    parsed = []
    for c in df.columns:
        if not c.startswith(base_prefix):
            continue
        core = c
        if suffix:
            if not c.endswith(suffix):
                continue
            core = c[:-len(suffix)]
        elif not c.endswith("_Hz"):
            continue
        if not core.endswith("_Hz"):
            continue
        text = core[len(base_prefix):-3]
        try:
            parsed.append((float(text), c))
        except Exception:
            pass
    parsed.sort(key=lambda x: x[0])
    values = np.asarray([p[0] for p in parsed], dtype=float)
    cols = [p[1] for p in parsed]
    labels = [f"{v/1000:g}" for v in values] if mode == "tuningFreq" else [f"{v:g}" for v in values]
    return cols, values, labels

def mode_axis_label(mode: str) -> str:
    return "Tone frequency (kHz)" if mode == "tuningFreq" else "AM rate (Hz)"


def mode_title(mode: str) -> str:
    return "Frequency tuning" if mode == "tuningFreq" else "AM-rate tuning"


def tuning_display_values(values_hz: Iterable[Any], mode: str) -> np.ndarray:
    """Return tuning values in the units shown to the user (kHz or Hz)."""
    values = np.asarray(values_hz, dtype=float)
    return values / 1000.0 if mode == "tuningFreq" else values


def xplot(values_hz: Iterable[Any], mode: str) -> np.ndarray:
    """Explicit octave coordinate used for every numeric tuning x-axis.

    Plotting at x = log2(value) guarantees that any two equal frequency/rate
    ratios occupy equal physical distance on the axis. For example, 2->4 kHz
    and 20->40 kHz both span exactly one x unit.
    """
    display = tuning_display_values(values_hz, mode)
    out = np.full(display.shape, np.nan, dtype=float)
    valid = np.isfinite(display) & (display > 0)
    out[valid] = np.log2(display[valid])
    return out


def log2_tick_labels(values_hz: Iterable[Any], mode: str) -> list[str]:
    values = np.asarray(values_hz, dtype=float)
    return [f"{v/1000:g}" for v in values] if mode == "tuningFreq" else [f"{v:g}" for v in values]


def apply_log2_tuning_axis(ax, values_hz: Iterable[Any], mode: str) -> None:
    """Label an axis whose plotted coordinates are already explicit log2 values."""
    values_hz = np.asarray(values_hz, dtype=float).ravel()
    coords = xplot(values_hz, mode)
    valid = np.isfinite(coords)
    if not np.any(valid):
        return
    xv = coords[valid]
    labels = np.asarray(log2_tick_labels(values_hz[valid], mode), dtype=object)
    ax.set_xscale("linear")
    ax.set_xticks(xv)
    ax.set_xticklabels(labels)
    lo, hi = float(np.min(xv)), float(np.max(xv))
    if hi > lo:
        margin_oct = 0.12
        ax.set_xlim(lo - margin_oct, hi + margin_oct)
    else:
        ax.set_xlim(lo - 0.5, hi + 0.5)


def log2_bin_edges(values_hz: Iterable[Any], mode: str) -> np.ndarray | None:
    """Bin edges in explicit octave coordinates for tuning rasters."""
    x = xplot(values_hz, mode)
    if len(x) == 0 or np.any(~np.isfinite(x)):
        return None
    if len(x) == 1:
        return np.asarray([x[0] - 0.5, x[0] + 0.5], dtype=float)
    mids = 0.5 * (x[:-1] + x[1:])
    edges = np.empty(len(x) + 1, dtype=float)
    edges[1:-1] = mids
    edges[0] = x[0] - (mids[0] - x[0])
    edges[-1] = x[-1] + (x[-1] - mids[-1])
    return edges


def metric_label(metric: str, mode: str) -> str:
    if metric == "tuning_fwhm":
        return "FWHM bandwidth (octaves)" if mode == "tuningFreq" else "FWHM bandwidth (Hz)"
    return CONTINUOUS_METRICS.get(metric, {}).get("label", metric)


def selectivity_equation_footer(mode: str) -> str:
    fwhm_unit = "octaves (log2 frequency)" if mode == "tuningFreq" else "Hz"
    return (
        r"Lifetime sparseness = [1 - (mean(r))$^2$/mean(r$^2$)]/[1 - 1/N];  "
        r"Gini = inequality of r;  Fano = var(r)/mean(r);  "
        f"FWHM = width of |response| at 1/2 max ({fwhm_unit});  r = |mean baseline-corrected dF/F|"
    )


def aggregate_sessions(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    """One row per session x cell class; sessions are the biological replicate."""
    rows=[]
    group_cols=["subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode"]
    response_cols, values, _ = response_columns(df, mode)
    value_flag_cols=[]
    for v in values:
        tag=f"{float(v):g}".replace(".","p")
        col=f"tuning_value_responsive_fdr_{tag}_Hz"
        if col in df.columns: value_flag_cols.append((float(v),col))
    alt_metrics=[
        "tuning_lifetime_sparseness_session_median_dff",
        "tuning_lifetime_sparseness_60s_prestim_median_dff",
        "tuning_gini_coefficient_session_median_dff",
        "tuning_gini_coefficient_60s_prestim_median_dff",
        "tuning_fano_factor_session_median_dff",
        "tuning_fano_factor_60s_prestim_median_dff",
        "tuning_fwhm_session_median_dff",
        "tuning_fwhm_60s_prestim_median_dff",
    ]
    for keys,sdf in df.groupby(group_cols,dropna=False):
        row=dict(zip(group_cols,keys)); n=len(sdf); row["n_cells"]=int(n)
        for col,pct in [("stim_responsive_fdr","pct_stim_responsive_fdr"),("stim_excited_fdr","pct_stim_excited_fdr"),("stim_suppressed_fdr","pct_stim_suppressed_fdr")]:
            vals=sdf[col].astype(bool).to_numpy(float) if col in sdf else np.array([])
            row[pct]=100*float(np.mean(vals)) if len(vals) else np.nan
        for v,col in value_flag_cols:
            row[f"pct_{col}"]=100*float(sdf[col].astype(bool).mean()) if len(sdf) else np.nan
        for metric in SELECTIVITY_METRICS:
            vals=finite_values(sdf[metric]) if metric in sdf else np.array([])
            row[metric]=float(np.mean(vals)) if len(vals) else np.nan
        for metric in alt_metrics:
            vals=finite_values(sdf[metric]) if metric in sdf else np.array([])
            row[metric]=float(np.mean(vals)) if len(vals) else np.nan
        for col in response_cols:
            vals=finite_values(sdf[col]); row[col]=float(np.mean(vals)) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)

def paired_session_vectors(session_df: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    if len(session_df) == 0 or metric not in session_df.columns:
        return pd.DataFrame(columns=["yellow","green"]), np.array([]), np.array([])
    piv = session_df.pivot_table(index="session_key", columns="cell_class", values=metric, aggfunc="first")
    for cls in ("yellow", "green"):
        if cls not in piv.columns:
            piv[cls] = np.nan
    piv = piv[["yellow", "green"]].copy()
    y = pd.to_numeric(piv.yellow, errors="coerce")
    g = pd.to_numeric(piv.green, errors="coerce")
    valid = np.isfinite(y) & np.isfinite(g)
    piv = piv.loc[valid].copy()
    return piv, piv.yellow.to_numpy(float), piv.green.to_numpy(float)


# =============================================================================
# STATISTICS
# =============================================================================

def analyze_continuous_metric(cell_df: pd.DataFrame, session_df: pd.DataFrame, metric: str) -> dict[str, Any]:
    pooled_summary = {}
    session_summary = {}
    for cls in CELL_CLASSES:
        m, se, n = mean_sem(cell_df.loc[cell_df.cell_class == cls, metric])
        med, q1, q3, _ = median_iqr(cell_df.loc[cell_df.cell_class == cls, metric])
        pooled_summary[cls] = {"n_cells":n, "mean":m, "sem":se, "median":med, "q1":q1, "q3":q3}
        m, se, n = mean_sem(session_df.loc[session_df.cell_class == cls, metric])
        med, q1, q3, _ = median_iqr(session_df.loc[session_df.cell_class == cls, metric])
        session_summary[cls] = {"n_sessions":n, "mean":m, "sem":se, "median":med, "q1":q1, "q3":q3}
    piv, y, g = paired_session_vectors(session_df, metric)
    return {
        "label":metric_label(metric, str(cell_df["tuning_mode"].dropna().iloc[0]) if "tuning_mode" in cell_df and cell_df["tuning_mode"].notna().any() else "tuningAM"),
        "session_aggregation":CONTINUOUS_METRICS[metric]["session_agg"],
        "session_level_primary_paired":{
            "summary":session_summary,
            "yellow_vs_green_wilcoxon":safe_wilcoxon_pairs(y, g),
            "paired_session_keys":piv.index.astype(str).tolist(),
        },
        "pooled_cell_exploratory":{
            "summary":pooled_summary,
            "yellow_vs_green_mannwhitney":safe_mannwhitney(
                cell_df.loc[cell_df.cell_class == "yellow", metric],
                cell_df.loc[cell_df.cell_class == "green", metric],
            ),
        },
    }


def analyze_binary_metric(cell_df: pd.DataFrame, session_df: pd.DataFrame, metric: str) -> dict[str, Any]:
    pct_col, label = BINARY_METRICS[metric]
    session_summary = {}
    for cls in CELL_CLASSES:
        m, se, n = mean_sem(session_df.loc[session_df.cell_class == cls, pct_col])
        session_summary[cls] = {"n_sessions":n, "mean_percent":m, "sem_percent":se}
    piv, y, g = paired_session_vectors(session_df, pct_col)
    return {
        "label":label,
        "session_level_primary_paired":{
            "summary":session_summary,
            "yellow_vs_green_wilcoxon":safe_wilcoxon_pairs(y, g),
            "paired_session_keys":piv.index.astype(str).tolist(),
        },
        "pooled_cell_exploratory":fisher_green_yellow(cell_df, metric),
    }


def run_statistics(cell_df: pd.DataFrame, session_df: pd.DataFrame, include_binary: bool = True) -> dict[str, Any]:
    out: dict[str, Any] = {"continuous":{}, "binary":{}}
    for metric in SELECTIVITY_METRICS:
        if metric in cell_df.columns:
            out["continuous"][metric]=analyze_continuous_metric(cell_df,session_df,metric)
    # Holm across the four retained session-level selectivity comparisons.
    names=list(out["continuous"])
    pvals=[out["continuous"][m]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"].get("p",np.nan) for m in names]
    adj=holm_adjust(pvals)
    for m,padj in zip(names,adj):
        out["continuous"][m]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]["p_holm_selectivity_family"]=padj
    if include_binary:
        for metric in BINARY_METRICS:
            if metric in cell_df.columns:
                out["binary"][metric]=analyze_binary_metric(cell_df,session_df,metric)
        bnames=list(out["binary"])
        bp=[out["binary"][m]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"].get("p",np.nan) for m in bnames]
        badj=holm_adjust(bp)
        for m,padj in zip(bnames,badj):
            out["binary"][m]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]["p_holm_responsiveness_family"]=padj
    return out

def tuning_value_statistics(cell_df: pd.DataFrame, mode: str, responsive_only: bool) -> pd.DataFrame:
    df = cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
    sdf = aggregate_sessions(df, mode) if len(df) else pd.DataFrame()
    cols, values, _ = response_columns(df, mode)
    rows = []
    for col, value in zip(cols, values):
        piv, y, g = paired_session_vectors(sdf, col)
        test = safe_wilcoxon_pairs(y, g)
        rows.append({
            "subset":"FDR_responsive_only" if responsive_only else "all_cells",
            "tuning_mode":mode, "tuning_value_Hz":value, "response_column":col,
            "n_paired_sessions":test["n_paired_sessions"], "W":test["W"], "p":test["p"],
            "mean_difference_yellow_minus_green":test["mean_difference_yellow_minus_green"],
            "sem_difference":test["sem_difference"],
            "median_difference_yellow_minus_green":test["median_difference_yellow_minus_green"],
        })
    out = pd.DataFrame(rows)
    if len(out):
        out["p_holm_global"] = holm_adjust(out.p.tolist())
    return out


def condition_statistics(cond_df: pd.DataFrame, metric: str, responsive_only: bool) -> pd.DataFrame:
    df = cond_df[cond_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cond_df.copy()
    group_cols = ["session_key","cell_class","tuning_value_Hz","intensity_dB"]
    sess = df.groupby(group_cols, dropna=False)[metric].mean().reset_index() if len(df) else pd.DataFrame(columns=group_cols+[metric])
    rows = []
    for (value, intensity), sdf in sess.groupby(["tuning_value_Hz","intensity_dB"], dropna=False):
        piv = sdf.pivot_table(index="session_key", columns="cell_class", values=metric, aggfunc="first")
        for cls in ("yellow", "green"):
            if cls not in piv.columns:
                piv[cls] = np.nan
        piv = piv[["yellow","green"]].dropna()
        test = safe_wilcoxon_pairs(piv.yellow, piv.green)
        rows.append({
            "subset":"FDR_responsive_only" if responsive_only else "all_cells",
            "metric":metric, "tuning_value_Hz":value, "intensity_dB":intensity,
            "n_paired_sessions":test["n_paired_sessions"], "W":test["W"], "p":test["p"],
            "mean_difference_yellow_minus_green":test["mean_difference_yellow_minus_green"],
            "sem_difference":test["sem_difference"],
            "median_difference_yellow_minus_green":test["median_difference_yellow_minus_green"],
        })
    out = pd.DataFrame(rows)
    if len(out):
        out["p_holm_global"] = holm_adjust(out.p.tolist())
    return out


# =============================================================================
# PLOT UTILITIES
# =============================================================================

def optimized_ylim_from_summary(
    means: np.ndarray, errors: np.ndarray | None = None,
    reference_values: list[float] | tuple[float, ...] | None = None,
    pad_fraction: float = 0.18,
) -> tuple[float, float] | None:
    means = np.asarray(means, dtype=float)
    if errors is None:
        errors = np.zeros_like(means)
    errors = np.asarray(errors, dtype=float)
    low = means - np.nan_to_num(errors, nan=0.0)
    high = means + np.nan_to_num(errors, nan=0.0)
    vals = np.r_[low[np.isfinite(low)], high[np.isfinite(high)]]
    if reference_values:
        vals = np.r_[vals, np.asarray(reference_values, dtype=float)]
    vals = vals[np.isfinite(vals)]
    if len(vals) == 0:
        return None
    lo, hi = float(np.min(vals)), float(np.max(vals))
    span = hi-lo
    if span <= 0:
        span = max(abs(lo), 1.0)*0.25
    pad = pad_fraction*span
    return lo-pad, hi+pad


def robust_cell_ylim(values: Iterable[Any], reference: float | None = None) -> tuple[float, float, int] | None:
    vals = finite_values(values)
    if len(vals) == 0:
        return None
    q1, q3 = np.percentile(vals, [25,75])
    iqr = q3-q1
    if iqr > 0:
        lo_f, hi_f = q1-3*iqr, q3+3*iqr
        keep = vals[(vals>=lo_f)&(vals<=hi_f)]
    else:
        keep = vals
    if len(keep) == 0:
        keep = vals
    lo, hi = float(np.min(keep)), float(np.max(keep))
    if reference is not None and np.isfinite(reference):
        lo = min(lo, reference); hi = max(hi, reference)
    span = hi-lo
    if span <= 0:
        span = max(abs(lo),1.0)*0.25
    pad = 0.12*span
    clipped = int(np.sum((vals < lo) | (vals > hi)))
    return lo-pad, hi+pad, clipped


def annotate_mean_sem(ax, x: float, mean: float, sem: float, n: int, color: str, y_offset_frac: float = 0.02) -> None:
    if not np.isfinite(mean):
        return
    y0, y1 = ax.get_ylim()
    offset = y_offset_frac*(y1-y0)
    se_txt = f"{sem:.3g}" if np.isfinite(sem) else "n/a"
    ax.text(x, mean+offset, f"{mean:.3g}±{se_txt}\nn={n}", ha="center", va="bottom", fontsize=7, color=color)


# =============================================================================
# FIGURES
# =============================================================================

def _plot_session_metric_panel(ax, session_df: pd.DataFrame, metric: str, mode: str, connect_pairs: bool = True) -> None:
    x=np.asarray([0.0,1.0]); display=[]
    piv=session_df.pivot_table(index="session_key",columns="cell_class",values=metric,aggfunc="first") if len(session_df) else pd.DataFrame()
    if {"green","yellow"}.issubset(piv.columns):
        paired=piv[["green","yellow"]].apply(pd.to_numeric,errors="coerce").dropna()
        if connect_pairs:
            for _,r in paired.iterrows():
                ax.plot(x,[r.green,r.yellow],color="0.55",alpha=.45,lw=.9,zorder=1)
                ax.scatter(x,[r.green,r.yellow],s=24,color=[CELL_CLASS_COLORS["green"],CELL_CLASS_COLORS["yellow"]],zorder=3)
                display.extend([r.green,r.yellow])
    for xpos,cls in enumerate(CELL_CLASSES):
        vals=finite_values(session_df.loc[session_df.cell_class==cls,metric]) if metric in session_df else np.array([])
        m,se,n=mean_sem(vals)
        if np.isfinite(m):
            ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,elinewidth=2.4,color=CELL_CLASS_COLORS[cls],zorder=5)
            display.extend(vals.tolist())
    ref=CONTINUOUS_METRICS.get(metric,{}).get("reference",None)
    if ref is not None: ax.axhline(ref,color="0.45",ls="--",lw=1)
    ax.set_xticks(x,["Green","Yellow"]); ax.set_ylabel(metric_label(metric,mode)); ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False)
    ylim=robust_cell_ylim(display,ref)
    if ylim: ax.set_ylim(ylim[0],ylim[1])

def plot_metric_grid(
    cell_df: pd.DataFrame, session_df: pd.DataFrame,
    area: str, layer_label: str, mode: str,
    output_path: Path, display_mode: str, subset_label: str,
) -> None:
    metrics=[m for m in CONTINUOUS_METRICS if m in cell_df.columns]
    if not metrics: return
    ncols=3; nrows=math.ceil(len(metrics)/ncols)
    fig,axes=plt.subplots(nrows,ncols,figsize=(16,4.8*nrows),squeeze=False); axes=axes.ravel()
    rng=np.random.default_rng(20260819)
    for ax,metric in zip(axes,metrics):
        cfg=CONTINUOUS_METRICS[metric]; ref=cfg["reference"]
        if display_mode in ("mean","session_paired","session_mean"):
            _plot_session_metric_panel(ax,session_df,metric,mode,connect_pairs=display_mode!="mean")
            continue
        display=[]
        for xpos,cls in enumerate(CELL_CLASSES):
            vals=finite_values(cell_df.loc[cell_df.cell_class==cls,metric])
            if len(vals):
                ax.scatter(np.full(len(vals),xpos)+rng.uniform(-.085,.085,len(vals)),vals,s=16,alpha=.24,
                           color=CELL_CLASS_COLORS[cls],edgecolors="none")
                m,_,se,n=mean_sd_sem(vals)
                ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=5,
                            elinewidth=2.2,lw=0,color=CELL_CLASS_COLORS[cls],zorder=5)
                display.extend(vals.tolist())
        if ref is not None: ax.axhline(ref,color="0.45",ls="--",lw=1)
        ylim=robust_cell_ylim(display,ref)
        if ylim:
            ax.set_ylim(ylim[0],ylim[1])
            if ylim[2]: ax.text(.98,.02,f"display clips {ylim[2]} outlier(s)",transform=ax.transAxes,ha="right",fontsize=7,color="0.4")
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(metric_label(metric,mode)); ax.set_title(metric_label(metric,mode))
        ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False)
    for ax in axes[len(metrics):]: ax.axis("off")
    mode_text={
        "cells":"individual cells + pooled mean +/- SEM (exploratory display)",
        "mean":"light session mean +/- SD; dark overall mean +/- SEM",
        "session_paired":"paired session mean +/- SD; dark overall mean +/- SEM",
        "session_mean":"paired session mean +/- SD; dark overall mean +/- SEM",
    }[display_mode]
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\n{subset_label}: GREEN vs YELLOW — {mode_text}",fontsize=14)
    fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def _plot_pooled_tuning_profile(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    """Backward-compatible pooled-cell tuning profile (exploratory display)."""
    cols,values,_=response_columns(cell_df,mode)
    if not cols: return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(9.5,5.8)); allm=[]; alls=[]
    for cls in CELL_CLASSES:
        cdf=cell_df[cell_df.cell_class==cls]; means=[]; sems=[]
        for col in cols:
            m,se,_=mean_sem(cdf[col]); means.append(m); sems.append(se)
        allm.extend(means); alls.extend(sems)
        ax.errorbar(x,means,yerr=sems,marker="o",capsize=4,lw=2,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
    ylim=optimized_ylim_from_summary(np.asarray(allm),np.asarray(alls),[0]);
    if ylim: ax.set_ylim(*ylim)
    ax.axhline(0,color="0.45",ls="--",lw=1); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Response (dF/F)")
    apply_log2_tuning_axis(ax,values,mode)
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nPooled cells mean +/- SEM — exploratory — {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.25); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_POOLED_CELL_MEAN_SEM.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profile_session(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    sdf=aggregate_sessions(cell_df,mode) if len(cell_df) else pd.DataFrame()
    cols,values,_=response_columns(cell_df,mode)
    if not cols or len(sdf)==0: return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(10,6.3)); display=[]
    for cls in CELL_CLASSES:
        color=CELL_CLASS_COLORS[cls]; c_sessions=sdf[sdf.cell_class==cls]; profiles=[]
        for _,row in c_sessions.iterrows():
            means=np.asarray([row.get(c,np.nan) for c in cols],float)
            profiles.append(means); ax.plot(x,means,color=color,alpha=.22,lw=1.0,marker="o",ms=2.5,zorder=1)
            display.extend(finite_values(means).tolist())
        if profiles:
            smat=np.vstack(profiles); overall=np.nanmean(smat,axis=0)
            sem=np.asarray([stats.sem(smat[:,i],nan_policy="omit") if np.sum(np.isfinite(smat[:,i]))>1 else np.nan for i in range(len(cols))])
            ax.errorbar(x,overall,yerr=sem,fmt="o-",color=color,lw=2.8,ms=5.5,elinewidth=2.0,capsize=4,label=f"{cls.capitalize()} overall ({len(profiles)} sessions)",zorder=5)
            display.extend(finite_values(overall).tolist()); display.extend(finite_values(np.r_[overall-sem,overall+sem]).tolist())
    # paired Wilcoxon at every tuning value, Holm across values
    tests=[]
    for col,v in zip(cols,values):
        _,y,g=paired_session_vectors(sdf,col); rec=safe_wilcoxon_pairs(y,g); tests.append(rec.get("p",np.nan))
    padj=holm_adjust(tests)
    sig=[f"{log2_tick_labels([v],mode)[0]}: pH={p:.3g}" for v,p in zip(values,padj) if np.isfinite(p) and p<.05]
    ax.axhline(0,color="0.45",ls="--",lw=1); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Session mean response (dF/F)")
    apply_log2_tuning_axis(ax,values,mode)
    ylim=optimized_ylim_from_summary(np.asarray(display),None,[0]);
    if ylim: ax.set_ylim(*ylim)
    subtitle="; ".join(sig) if sig else "no tuning-value GREEN/YELLOW differences survive Holm correction"
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nsession means; dark=overall mean ± SEM — {suffix.replace('_',' ')}\n{subtitle}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.25); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

def plot_tuning_profiles_sessions_top_cells(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    cols,values,_=response_columns(cell_df,mode)
    if not cols or "tuning_lifetime_sparseness" not in cell_df: return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(10,6.2))
    for cls in CELL_CLASSES:
        color=CELL_CLASS_COLORS[cls]; cdf=cell_df[cell_df.cell_class==cls]
        for _,sdf in cdf.groupby("session_key",sort=True):
            mat=sdf[cols].to_numpy(float)
            if len(mat)==0: continue
            ranks=pd.to_numeric(sdf.tuning_lifetime_sparseness,errors="coerce").to_numpy(float)
            valid=np.flatnonzero(np.isfinite(ranks)); valid=valid[np.argsort(ranks[valid])[::-1]][:5]
            for ridx in valid: ax.plot(x,mat[ridx],color=color,alpha=.14,lw=.8,ls="--",zorder=1)
            ax.plot(x,np.nanmean(mat,axis=0),color=color,alpha=.65,lw=1.8,marker="o",ms=3,zorder=3)
    ax.axhline(0,color="0.45",ls="--",lw=1); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Response (dF/F)")
    apply_log2_tuning_axis(ax,values,mode)
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nsolid=session means; dashed=top 5 cells/session by lifetime sparseness — {suffix.replace('_',' ')}")
    ax.legend(handles=[Line2D([0],[0],color=CELL_CLASS_COLORS['green'],lw=2,label='Green session mean'),
                       Line2D([0],[0],color=CELL_CLASS_COLORS['yellow'],lw=2,label='Yellow session mean'),
                       Line2D([0],[0],color='0.35',lw=1,ls='--',alpha=.5,label='High-sparseness cell')],frameon=False)
    ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_MEANS_TOP5_CELLS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_selectivity_rasters(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str,
                             sort_metric: str = "preferred_tuning_value_Hz", stem_extra: str = "") -> None:
    cols,values,labels=response_columns(cell_df,mode)
    if len(cols)<2: return
    fig,axes=plt.subplots(2,1,figsize=(10,7.8),squeeze=False); im=None
    edges=log2_bin_edges(values,mode)
    for row,cls in enumerate(CELL_CLASSES):
        ax=axes[row,0]; cdf=cell_df[cell_df.cell_class==cls].copy()
        if len(cdf)==0:
            ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center",va="center"); ax.set_axis_off(); continue
        mat=cdf[cols].to_numpy(float); denom=np.nanmax(np.abs(mat),axis=1); good=np.isfinite(denom)&(denom>0)
        mat=mat[good]; cdf=cdf.iloc[np.where(good)[0]].copy()
        if len(mat)==0: continue
        norm=mat/denom[good,None]
        rank=pd.to_numeric(cdf.get(sort_metric,np.nan),errors="coerce").to_numpy(float)
        if sort_metric=="tuning_lifetime_sparseness": order=np.argsort(np.nan_to_num(rank,nan=-np.inf))[::-1]
        else: order=np.argsort(np.nan_to_num(rank,nan=np.inf))
        norm=norm[order]
        if edges is not None:
            yedges=np.arange(len(norm)+1,dtype=float)
            im=ax.pcolormesh(edges,yedges,norm,cmap="coolwarm",vmin=-1,vmax=1,shading="flat")
            ax.set_ylim(len(norm),0); apply_log2_tuning_axis(ax,values,mode)
        else:
            im=ax.imshow(norm,aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm")
            ax.set_xticks(np.arange(len(labels)),labels,rotation=45,ha="right")
        ax.set_ylabel(f"{cls.capitalize()} cells"); ax.set_xlabel(mode_axis_label(mode))
        sort_label="lifetime sparseness" if sort_metric=="tuning_lifetime_sparseness" else "preferred tuning value"
        ax.set_title(f"{cls.capitalize()}: n={len(norm)} | sorted by {sort_label}")
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\nGREEN vs YELLOW tuning rasters — {suffix.replace('_',' ')}",y=1.01)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Normalized tuning response",shrink=.75)
    fig.tight_layout(); fig.savefig(outdir/f"selectivity_rasters_{suffix}{stem_extra}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_preferred_distribution(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    vals=np.sort(pd.to_numeric(cell_df.preferred_tuning_value_Hz,errors="coerce").dropna().unique())
    if len(vals)==0: return
    x=xplot(vals,mode); fig,ax=plt.subplots(figsize=(9,5.5))
    # Small additive offsets in octave coordinates preserve GREEN/YELLOW grouping.
    offset_oct=0.055
    for cls,shift in (("green",-offset_oct),("yellow",offset_oct)):
        cdf=cell_df[cell_df.cell_class==cls]; pref=pd.to_numeric(cdf.preferred_tuning_value_Hz,errors="coerce").to_numpy(float)
        total=np.sum(np.isfinite(pref)); pct=[100*np.sum(np.isclose(pref,v,equal_nan=False))/total if total else np.nan for v in vals]
        ax.plot(x+shift,pct,"o",ms=7,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
    apply_log2_tuning_axis(ax,vals,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Cells preferring condition (%)")
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nPreferred tuning distribution — {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.25); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(outdir/f"preferred_tuning_distribution_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_standalone_selectivity_figures(cell_df: pd.DataFrame, session_df: pd.DataFrame, stats_out: dict[str,Any],
                                        area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    rng=np.random.default_rng(9917)
    for metric in SELECTIVITY_METRICS:
        if metric not in cell_df: continue
        label=metric_label(metric,mode); ref=CONTINUOUS_METRICS[metric]["reference"]; stem=metric.replace("tuning_","")
        fig,ax=plt.subplots(figsize=(7,6.3)); display=[]
        for xi,cls in enumerate(CELL_CLASSES):
            vals=finite_values(cell_df.loc[cell_df.cell_class==cls,metric])
            if len(vals):
                ax.scatter(np.full(len(vals),xi)+rng.uniform(-.09,.09,len(vals)),vals,s=22,alpha=.23,color=CELL_CLASS_COLORS[cls],edgecolors="none")
                m,_,se,n=mean_sd_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,elinewidth=2.4,color=CELL_CLASS_COLORS[cls],zorder=5); display.extend(vals.tolist())
        pooled=stats_out.get("continuous",{}).get(metric,{}).get("pooled_cell_exploratory",{}).get("yellow_vs_green_mannwhitney",{}); p=pooled.get("p",np.nan)
        if ref is not None: ax.axhline(ref,color="0.45",ls="--",lw=1)
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel(label); ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\n{label}\nindividual cells; exploratory Mann–Whitney p={p:.3g}" if np.isfinite(p) else label)
        ax.text(.5,-.15,selectivity_equation_footer(mode),transform=ax.transAxes,ha="center",va="top",fontsize=7.5,wrap=True); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
        ylim=robust_cell_ylim(display,ref); 
        if ylim: ax.set_ylim(ylim[0],ylim[1])
        fig.subplots_adjust(bottom=.25); fig.savefig(outdir/f"{stem}_green_yellow_{suffix}_CELL_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

        fig,ax=plt.subplots(figsize=(7,6.3)); _plot_session_metric_panel(ax,session_df,metric,mode,connect_pairs=True)
        primary=stats_out.get("continuous",{}).get(metric,{}).get("session_level_primary_paired",{}).get("yellow_vs_green_wilcoxon",{}); p=primary.get("p",np.nan); ph=primary.get("p_holm_selectivity_family",np.nan); n=primary.get("n_paired_sessions",0)
        ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\n{label}\npaired Wilcoxon p={p:.3g}, Holm p={ph:.3g}, n={n}" if np.isfinite(p) else label)
        ax.text(.5,-.15,selectivity_equation_footer(mode),transform=ax.transAxes,ha="center",va="top",fontsize=7.5,wrap=True)
        fig.subplots_adjust(bottom=.25); fig.savefig(outdir/f"{stem}_green_yellow_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    # Alternate-dF/F sensitivity analyses for the primary selectivity metric only.
    for altcol,tag,label_extra in [
        ("tuning_lifetime_sparseness_session_median_dff","session_median_dff","whole-session median F0"),
        ("tuning_lifetime_sparseness_60s_prestim_median_dff","60s_prestim_median_dff","60-s local prestimulus median F0"),
    ]:
        if altcol not in cell_df.columns: continue
        alt_sdf=aggregate_sessions(cell_df,mode)
        fig,ax=plt.subplots(figsize=(7,6.3)); display=[]
        for xi,cls in enumerate(CELL_CLASSES):
            vals=finite_values(cell_df.loc[cell_df.cell_class==cls,altcol]);
            if len(vals):
                ax.scatter(np.full(len(vals),xi)+rng.uniform(-.09,.09,len(vals)),vals,s=22,alpha=.22,color=CELL_CLASS_COLORS[cls],edgecolors="none"); m,se,n=mean_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,color=CELL_CLASS_COLORS[cls]); display.extend(vals.tolist())
        test=safe_mannwhitney(cell_df.loc[cell_df.cell_class=="yellow",altcol],cell_df.loc[cell_df.cell_class=="green",altcol])
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel("Lifetime sparseness"); ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nLifetime sparseness sensitivity: {label_extra}\nexploratory pooled p={test.get('p',np.nan):.3g}")
        ylim=robust_cell_ylim(display,None); 
        if ylim: ax.set_ylim(ylim[0],ylim[1])
        fig.tight_layout(); fig.savefig(outdir/f"lifetime_sparseness_{tag}_green_yellow_{suffix}_CELL_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)
        fig,ax=plt.subplots(figsize=(7,6.3)); _plot_session_metric_panel(ax,alt_sdf,altcol,mode,True)
        _,y,g=paired_session_vectors(alt_sdf,altcol); test=safe_wilcoxon_pairs(y,g)
        ax.set_ylabel("Lifetime sparseness"); ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nLifetime sparseness sensitivity: {label_extra}\npaired Wilcoxon p={test.get('p',np.nan):.3g}, n={test.get('n_paired_sessions',0)}")
        fig.tight_layout(); fig.savefig(outdir/f"lifetime_sparseness_{tag}_green_yellow_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

def plot_responsiveness(cell_df: pd.DataFrame, session_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path) -> None:
    metrics=[(m,p,l) for m,(p,l) in BINARY_METRICS.items()]
    fig,axes=plt.subplots(1,3,figsize=(14.5,4.9),squeeze=False); axes=axes.ravel(); rawps=[]
    for ax,(_,pct_col,label) in zip(axes,metrics):
        piv=session_df.pivot_table(index="session_key",columns="cell_class",values=pct_col,aggfunc="first") if len(session_df) else pd.DataFrame()
        paired=piv[["green","yellow"]].dropna() if {"green","yellow"}.issubset(piv.columns) else pd.DataFrame(columns=["green","yellow"])
        for _,r in paired.iterrows():
            ax.plot([0,1],[r.green,r.yellow],color=".55",alpha=.45,lw=.9); ax.scatter([0,1],[r.green,r.yellow],s=24,color=[CELL_CLASS_COLORS["green"],CELL_CLASS_COLORS["yellow"]],zorder=3)
        for xpos,cls in enumerate(CELL_CLASSES):
            m,se,n=mean_sem(session_df.loc[session_df.cell_class==cls,pct_col]);
            if np.isfinite(m): ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=5,lw=2,color=CELL_CLASS_COLORS[cls])
        test=safe_wilcoxon_pairs(paired.yellow if len(paired) else [],paired.green if len(paired) else []); rawps.append(test.get("p",np.nan))
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel("Session percentage (%)"); ax.set_title(label.replace("FDR ","")); ax.grid(axis="y",alpha=.25); ax.spines[["top","right"]].set_visible(False)
    adj=holm_adjust(rawps)
    for ax,p,ph in zip(axes,rawps,adj): ax.text(.5,.98,f"Wilcoxon p={p:.3g}; Holm p={ph:.3g}" if np.isfinite(p) else "test unavailable",transform=ax.transAxes,ha="center",va="top",fontsize=8)
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\nPrimary v9 responsiveness (union of tuning-value-specific FDR discoveries)",fontsize=13); fig.tight_layout(rect=[0,0,1,.92]); fig.savefig(outdir/"responsiveness_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    # Tuning-value-specific responsiveness profile.
    cols,values,_=response_columns(cell_df,mode); flagcols=[]
    for v in values:
        tag=f"{float(v):g}".replace(".","p"); c=f"tuning_value_responsive_fdr_{tag}_Hz";
        if c in cell_df.columns: flagcols.append((v,c))
    if not flagcols: return
    x=xplot([v for v,_ in flagcols],mode); fig,ax=plt.subplots(figsize=(9.5,5.8)); pvals=[]; display=[]
    # recompute session percentages directly for each flag
    for cls in CELL_CLASSES:
        profiles=[]
        for sk,sdf in cell_df[cell_df.cell_class==cls].groupby("session_key",sort=True):
            prof=np.asarray([100*float(sdf[c].astype(bool).mean()) if len(sdf) else np.nan for _,c in flagcols]); profiles.append(prof); ax.plot(x,prof,color=CELL_CLASS_COLORS[cls],alpha=.20,lw=1,marker="o",ms=2.5); display.extend(finite_values(prof).tolist())
        if profiles:
            mat=np.vstack(profiles); mean=np.nanmean(mat,axis=0); sem=np.asarray([stats.sem(mat[:,i],nan_policy="omit") if np.sum(np.isfinite(mat[:,i]))>1 else np.nan for i in range(mat.shape[1])]); ax.errorbar(x,mean,yerr=sem,fmt="o-",lw=2.7,capsize=4,color=CELL_CLASS_COLORS[cls],label=cls.capitalize()); display.extend(finite_values(np.r_[mean-sem,mean+sem]).tolist())
    for v,c in flagcols:
        sess=[]
        for (sk,cls),sdf in cell_df.groupby(["session_key","cell_class"]): sess.append({"session_key":sk,"cell_class":cls,"pct":100*float(sdf[c].astype(bool).mean())})
        ss=pd.DataFrame(sess); piv=ss.pivot_table(index="session_key",columns="cell_class",values="pct",aggfunc="first"); paired=piv[["green","yellow"]].dropna() if {"green","yellow"}.issubset(piv.columns) else pd.DataFrame(); rec=safe_wilcoxon_pairs(paired.yellow if len(paired) else [],paired.green if len(paired) else []); pvals.append(rec.get("p",np.nan))
    padj=holm_adjust(pvals); sig=[f"{log2_tick_labels([v],mode)[0]}: pH={p:.3g}" for (v,_),p in zip(flagcols,padj) if np.isfinite(p) and p<.05]
    apply_log2_tuning_axis(ax,[v for v,_ in flagcols],mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Responsive cells per session (%)"); ax.set_ylim(0,100); ax.grid(alpha=.22); ax.legend(frameon=False); ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nTuning-value-specific responsiveness\n"+("; ".join(sig) if sig else "no per-value differences survive Holm correction")); fig.tight_layout(); fig.savefig(outdir/"responsiveness_by_tuning_value_SESSION_PROFILE.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

def _plot_intensity_condition_grid_pooled(cond_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path,
                                           suffix: str, metric: str, label: str, filename: str) -> None:
    if len(cond_df)==0: return
    values=np.sort(pd.to_numeric(cond_df.tuning_value_Hz,errors="coerce").dropna().unique()); intensities=np.sort(pd.to_numeric(cond_df.intensity_dB,errors="coerce").dropna().unique())
    if len(values)==0 or len(intensities)==0: return
    ncols=min(3,len(intensities)); nrows=math.ceil(len(intensities)/ncols); fig,axes=plt.subplots(nrows,ncols,figsize=(5*ncols,4.4*nrows),squeeze=False); axes=axes.ravel(); x=xplot(values,mode)
    for ax,intensity in zip(axes,intensities):
        for cls in CELL_CLASSES:
            means=[]; sems=[]
            for value in values:
                vals=cond_df[(cond_df.cell_class==cls)&np.isclose(cond_df.intensity_dB,intensity)&np.isclose(cond_df.tuning_value_Hz,value)][metric]
                m,se,_=mean_sem(vals); means.append(m); sems.append(se)
            ax.errorbar(x,means,yerr=sems,marker="o",capsize=3,lw=2,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
        ax.axhline(0,color=".45",ls="--",lw=1); apply_log2_tuning_axis(ax,values,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel(label); ax.set_title(f"{intensity:g} dB"); ax.grid(axis="y",alpha=.25); ax.legend(frameon=False)
    for ax in axes[len(intensities):]: ax.axis("off")
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\n{label} — pooled cells mean +/- SEM — {suffix.replace('_',' ')}",fontsize=14); fig.tight_layout(rect=[0,0,1,.94])
    fig.savefig(outdir/f"{filename}_{suffix}_POOLED_CELL_MEAN_SEM.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_intensity_condition_grid(cond_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str,
                                  metric: str, label: str, filename: str) -> None:
    if len(cond_df)==0: return
    values=np.sort(pd.to_numeric(cond_df.tuning_value_Hz,errors="coerce").dropna().unique()); intensities=np.sort(pd.to_numeric(cond_df.intensity_dB,errors="coerce").dropna().unique())
    if len(values)==0 or len(intensities)==0: return
    ncols=min(3,len(intensities)); nrows=math.ceil(len(intensities)/ncols); fig,axes=plt.subplots(nrows,ncols,figsize=(5.3*ncols,4.6*nrows),squeeze=False); axes=axes.ravel(); x=xplot(values,mode)
    grouped=cond_df.groupby(["session_key","cell_class","tuning_value_Hz","intensity_dB"],dropna=False)[metric].mean().reset_index()
    all_display=[]
    for ax,intensity in zip(axes,intensities):
        pvals=[]
        for cls in CELL_CLASSES:
            csub=grouped[(grouped.cell_class==cls)&np.isclose(grouped.intensity_dB,intensity)]; profiles=[]; color=CELL_CLASS_COLORS[cls]
            for sk,sdf in csub.groupby("session_key",sort=True):
                prof=np.asarray([float(sdf[np.isclose(sdf.tuning_value_Hz,v)].iloc[0][metric]) if len(sdf[np.isclose(sdf.tuning_value_Hz,v)]) else np.nan for v in values]); profiles.append(prof); ax.plot(x,prof,color=color,alpha=.20,lw=1,marker="o",ms=2.2); all_display.extend(finite_values(prof).tolist())
            if profiles:
                mat=np.vstack(profiles); mean=np.nanmean(mat,axis=0); sem=np.asarray([stats.sem(mat[:,i],nan_policy="omit") if np.sum(np.isfinite(mat[:,i]))>1 else np.nan for i in range(len(values))]); ax.errorbar(x,mean,yerr=sem,fmt="o-",ms=5,lw=2.6,elinewidth=1.8,capsize=3,color=color,label=cls.capitalize(),zorder=5); all_display.extend(finite_values(np.r_[mean-sem,mean+sem]).tolist())
        # tests at each tuning value for this intensity
        for v in values:
            ss=grouped[np.isclose(grouped.intensity_dB,intensity)&np.isclose(grouped.tuning_value_Hz,v)]; piv=ss.pivot_table(index="session_key",columns="cell_class",values=metric,aggfunc="first"); paired=piv[["green","yellow"]].dropna() if {"green","yellow"}.issubset(piv.columns) else pd.DataFrame(); rec=safe_wilcoxon_pairs(paired.yellow if len(paired) else [],paired.green if len(paired) else []); pvals.append(rec.get("p",np.nan))
        padj=holm_adjust(pvals); sig=[f"{log2_tick_labels([v],mode)[0]}" for v,p in zip(values,padj) if np.isfinite(p) and p<.05]
        ax.axhline(0,color=".45",ls="--",lw=1); apply_log2_tuning_axis(ax,values,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel(label); ax.set_title(f"{intensity:g} dB"+(f" | sig: {', '.join(sig)}" if sig else "")); ax.grid(axis="y",alpha=.25); ax.legend(frameon=False)
    ylim=optimized_ylim_from_summary(np.asarray(all_display),None,[0])
    if ylim:
        for ax in axes[:len(intensities)]: ax.set_ylim(*ylim)
    for ax in axes[len(intensities):]: ax.axis("off")
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\n{label} — session means; overall mean ± SEM — {suffix.replace('_',' ')}",fontsize=14); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(outdir/f"{filename}_{suffix}_SESSION_PROFILE.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

def make_metric_figures(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, responsive_only: bool) -> None:
    suffix="FDR_responsive_only" if responsive_only else "all_cells"
    df=cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
    if len(df)==0: return
    sdf=aggregate_sessions(df,mode); subset_stats=run_statistics(df,sdf,include_binary=False)
    plot_tuning_profile_session(df,area,layer_label,mode,outdir,suffix)
    plot_preferred_distribution(df,area,layer_label,mode,outdir,suffix)
    # One primary raster sorted by lifetime sparseness; preferred-value raster retained as tuning organization view.
    plot_selectivity_rasters(df,area,layer_label,mode,outdir,suffix,"preferred_tuning_value_Hz","_PREFERRED_VALUE")
    plot_selectivity_rasters(df,area,layer_label,mode,outdir,suffix,"tuning_lifetime_sparseness","_LIFETIME_SPARSENESS")
    plot_standalone_selectivity_figures(df,sdf,subset_stats,area,layer_label,mode,outdir,suffix)

# =============================================================================
# REPORTS / SUMMARY TABLES
# =============================================================================

def write_figure_index(outdir: Path) -> None:
    figs=sorted(p.name for p in outdir.glob("*.png"))
    (outdir/"FIGURE_INDEX.txt").write_text("\n".join(figs)+("\n" if figs else ""))


def write_report(path: Path, subject: str, dates: list[str], area: str, layer_key: str, mode: str, cell_df: pd.DataFrame, session_df: pd.DataFrame, stats_all: dict[str, Any], stats_resp: dict[str, Any]) -> None:
    layer_label=LAYERS[layer_key][2]
    lines=[
        "AM_TUNING AREA x LAYER GREEN-vs-YELLOW REPORT (v7-compatible)",
        "="*72,
        f"Subject: {subject}", f"Dates: {', '.join(dates)}", f"Area: {area}", f"Layer: {layer_label}", f"Tuning mode: {mode_title(mode)}",
        f"Cells: {len(cell_df)} | sessions: {cell_df.session_key.nunique() if len(cell_df) else 0}",
        f"Green cells: {sum(cell_df.cell_class=='green')} | Yellow cells: {sum(cell_df.cell_class=='yellow')}",
        "",
        "PRIMARY INFERENCE: paired session-level YELLOW vs GREEN Wilcoxon signed-rank tests.",
        "All paired differences are defined as YELLOW - GREEN.",
        "Pooled-cell tests are exploratory/descriptive only.",
        "Primary tuning selectivity: lifetime sparseness across |mean baseline-corrected tuning response|.",
        "Comparison selectivity metrics: Gini coefficient, tuning-profile Fano factor, and FWHM bandwidth.",
        "FWHM units: octaves for tuningFreq; Hz for tuningAM. Fano is scale-dependent.", "",
    ]
    for subset_name,stats_out in (("ALL CELLS",stats_all),("FDR-RESPONSIVE CELLS ONLY",stats_resp)):
        lines += [subset_name, "-"*len(subset_name)]
        for metric,result in stats_out.get("continuous",{}).items():
            label=result["label"]; lines.append(label)
            for cls in CELL_CLASSES:
                s=result["session_level_primary_paired"]["summary"][cls]
                lines.append(f"  {cls.upper()}: {s['mean']:.4g} ± {s['sem']:.4g} across n={s['n_sessions']} session summaries")
            w=result["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
            lines.append(f"  Paired YELLOW vs GREEN: W={w['W']:.4g}, {p_text(w['p'])}, n_pairs={w['n_paired_sessions']}") if np.isfinite(w["W"]) else lines.append(f"  Paired YELLOW vs GREEN: unavailable (n_pairs={w['n_paired_sessions']})")
            lines.append(f"  Paired difference YELLOW-GREEN: mean={w['mean_difference_yellow_minus_green']:.4g}, SEM={w['sem_difference']:.4g}, median={w['median_difference_yellow_minus_green']:.4g}")
            exp=result["pooled_cell_exploratory"]["yellow_vs_green_mannwhitney"]
            if np.isfinite(exp["U"]): lines.append(f"  Exploratory pooled cells: U={exp['U']:.4g}, {p_text(exp['p'])}, Cliff delta(Y-G)={exp['cliffs_delta_yellow_minus_green']:.3g}")
            lines.append("")
        if subset_name=="ALL CELLS":
            for metric,result in stats_out.get("binary",{}).items():
                lines.append(result["label"])
                for cls in CELL_CLASSES:
                    s=result["session_level_primary_paired"]["summary"][cls]
                    lines.append(f"  {cls.upper()}: {s['mean_percent']:.3g} ± {s['sem_percent']:.3g}% across n={s['n_sessions']} sessions")
                w=result["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
                lines.append(f"  Paired YELLOW vs GREEN: W={w['W']:.4g}, {p_text(w['p'])}, n_pairs={w['n_paired_sessions']}") if np.isfinite(w["W"]) else lines.append(f"  Paired YELLOW vs GREEN: unavailable (n_pairs={w['n_paired_sessions']})")
                f=result["pooled_cell_exploratory"]["yellow_vs_green_fisher"]
                if np.isfinite(f["odds_ratio"]): lines.append(f"  Exploratory pooled-cell Fisher: odds ratio={f['odds_ratio']:.4g}, {p_text(f['p'])}")
                lines.append("")
    path.write_text("\n".join(lines)+"\n")


def master_stats_rows(area: str, layer_key: str, mode: str, subset: str, stats_out: dict[str, Any]) -> list[dict[str, Any]]:
    rows=[]
    for family in ("continuous","binary"):
        for metric,result in stats_out.get(family,{}).items():
            w=result["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
            row={
                "tuning_mode":mode,"area":area,"layer":layer_key,"subset":subset,"metric_family":family,"metric":metric,"label":result["label"],
                "n_paired_sessions":w["n_paired_sessions"],"wilcoxon_W":w["W"],"wilcoxon_p":w["p"],
                "mean_difference_yellow_minus_green":w["mean_difference_yellow_minus_green"],"sem_difference":w["sem_difference"],
                "median_difference_yellow_minus_green":w["median_difference_yellow_minus_green"],
            }
            if family=="continuous":
                exp=result["pooled_cell_exploratory"]["yellow_vs_green_mannwhitney"]
                row.update({"pooled_test":"Mann-Whitney","pooled_statistic":exp["U"],"pooled_p":exp["p"],"pooled_effect":exp["cliffs_delta_yellow_minus_green"]})
            else:
                exp=result["pooled_cell_exploratory"]["yellow_vs_green_fisher"]
                row.update({"pooled_test":"Fisher exact","pooled_statistic":exp["odds_ratio"],"pooled_p":exp["p"],"pooled_effect":exp["odds_ratio"]})
            rows.append(row)
    return rows


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args=parse_args(); subject=str(args.subject); dates=[str(d) for d in args.dates]; areas=list(args.areas)
    modes=list(TUNING_MODES) if args.mode=="both" else [args.mode]
    outroot=output_root(subject,dates)

    print("="*86)
    print("AM_TUNING AREA x LAYER GREEN-vs-YELLOW ANALYSIS (v4; v9 prerequisite)")
    print("="*86)
    print(f"Subject: {subject}")
    print(f"Dates:   {', '.join(dates)}")
    print(f"Areas:   {', '.join(areas)}")
    print(f"Modes:   {', '.join(modes)}")
    print("Layers:  L2/3 = 100 <= depth < 300 um; L4/5 = 300 <= depth <= 600 um")
    print(f"Input root:  {Path(settings.TEMP_OUTPUT_PATH)/'evan'/'am_tuning_area_analysis'}")
    print(f"Output root: {outroot}")
    print("\nExpected inputs:")
    any_missing=False
    for mode in modes:
        print(f"  {mode}:")
        for area in areas:
            cp=expected_area_cell_csv(subject,area,dates,mode); qp=expected_area_condition_csv(subject,area,dates,mode)
            ok=cp.exists() and qp.exists(); any_missing |= not ok
            print(f"    {area}: cells [{'FOUND' if cp.exists() else 'MISSING'}]  conditions [{'FOUND' if qp.exists() else 'MISSING'}]")
            print(f"         {cp}")
            print(f"         {qp}")
    if args.dry_run:
        print("\nDry run complete; no tables were loaded.")
        return

    outroot.mkdir(parents=True,exist_ok=True)
    master_rows=[]; tuning_stats_all=[]; cond_resp_all=[]; cond_sel_all=[]; provenance_all={}

    for mode in modes:
        cells,conds,provenance=load_mode_tables(subject,dates,areas,mode); provenance_all[mode]=provenance
        mode_root=outroot/mode; mode_root.mkdir(parents=True,exist_ok=True)
        cells.to_csv(mode_root/"all_areas_combined_cell_results.csv",index=False); conds.to_csv(mode_root/"all_areas_combined_condition_results.csv",index=False)
        print("\n"+"="*86); print(mode_title(mode).upper()); print("="*86)
        for area in areas:
            acells=cells[cells.canonicalArea==area].copy(); aconds=conds[conds.canonicalArea==area].copy()
            print(f"\n{area}: {len(acells)} cells, {acells.session_key.nunique()} sessions")
            for layer_key,(_,_,layer_label) in LAYERS.items():
                lcells=subset_layer(acells,layer_key); lconds=subset_layer(aconds,layer_key); leaf=mode_root/area/layer_key; leaf.mkdir(parents=True,exist_ok=True)
                print(f"  {layer_label}:")
                for cls in CELL_CLASSES:
                    cdf=lcells[lcells.cell_class==cls]; print(f"    {cls.upper():6s}: {len(cdf)} cells, {cdf.session_key.nunique()} sessions")
                sdf=aggregate_sessions(lcells,mode) if len(lcells) else pd.DataFrame()
                rcells=lcells[lcells.stim_responsive_fdr.astype(bool)].copy(); rsdf=aggregate_sessions(rcells,mode) if len(rcells) else pd.DataFrame(columns=sdf.columns)
                lcells.to_csv(leaf/"cell_results.csv",index=False); lconds.to_csv(leaf/"condition_results.csv",index=False); sdf.to_csv(leaf/"session_summary.csv",index=False); rsdf.to_csv(leaf/"session_summary_FDR_responsive_only.csv",index=False)

                stats_all=run_statistics(lcells,sdf,include_binary=True) if len(lcells) else {"continuous":{},"binary":{}}
                stats_resp=run_statistics(rcells,rsdf,include_binary=False) if len(rcells) else {"continuous":{},"binary":{}}
                save_json(leaf/"statistics.json",{"all_cells":stats_all,"FDR_responsive_only":stats_resp})
                write_report(leaf/"REPORT.txt",subject,dates,area,layer_key,mode,lcells,sdf,stats_all,stats_resp)
                master_rows.extend(master_stats_rows(area,layer_key,mode,"all_cells",stats_all)); master_rows.extend(master_stats_rows(area,layer_key,mode,"FDR_responsive_only",stats_resp))

                tv=pd.concat([tuning_value_statistics(lcells,mode,False),tuning_value_statistics(lcells,mode,True)],ignore_index=True); tv.insert(0,"area",area); tv.insert(1,"layer",layer_key); tv.to_csv(leaf/"tuning_value_statistics.csv",index=False); tuning_stats_all.append(tv)
                cr=pd.concat([condition_statistics(lconds,"condition_response",False),condition_statistics(lconds,"condition_response",True)],ignore_index=True); cr.insert(0,"tuning_mode",mode); cr.insert(0,"layer",layer_key); cr.insert(0,"area",area); cr.to_csv(leaf/"condition_response_statistics.csv",index=False); cond_resp_all.append(cr)
                cs=pd.concat([condition_statistics(lconds,"condition_selectivity_contrast",False),condition_statistics(lconds,"condition_selectivity_contrast",True)],ignore_index=True); cs.insert(0,"tuning_mode",mode); cs.insert(0,"layer",layer_key); cs.insert(0,"area",area); cs.to_csv(leaf/"condition_selectivity_statistics.csv",index=False); cond_sel_all.append(cs)

                plot_responsiveness(lcells,sdf,area,layer_label,mode,leaf)
                make_metric_figures(lcells,area,layer_label,mode,leaf,False); make_metric_figures(lcells,area,layer_label,mode,leaf,True)
                for responsive_only in (False,True):
                    suffix="FDR_responsive_only" if responsive_only else "all_cells"; qdf=lconds[lconds.stim_responsive_fdr.astype(bool)].copy() if responsive_only else lconds.copy()
                    plot_intensity_condition_grid(qdf,area,layer_label,mode,leaf,suffix,"condition_response","Condition response (dF/F)","intensity_resolved_condition_response")
                    plot_intensity_condition_grid(qdf,area,layer_label,mode,leaf,suffix,"condition_selectivity_contrast","Condition selectivity contrast (dF/F)","intensity_resolved_condition_selectivity")
                write_figure_index(leaf)
                n_pairs=0
                if len(sdf) and "stim_response_mean" in sdf.columns:
                    piv,_,_=paired_session_vectors(sdf,"stim_response_mean"); n_pairs=len(piv)
                print(f"    Paired GREEN/YELLOW sessions available: {n_pairs} -> {leaf}")

    master=pd.DataFrame(master_rows); master.to_csv(outroot/"MASTER_STATISTICS.csv",index=False)
    if len(master):
        qcols=["tuning_mode","area","layer","subset","metric_family","metric","n_paired_sessions","wilcoxon_W","wilcoxon_p","mean_difference_yellow_minus_green","median_difference_yellow_minus_green"]
        master[qcols].sort_values(["tuning_mode","layer","area","wilcoxon_p"],na_position="last").to_csv(outroot/"PAIRED_GREEN_YELLOW_RESULTS_QUICKVIEW.csv",index=False)
    if tuning_stats_all: pd.concat(tuning_stats_all,ignore_index=True).to_csv(outroot/"ALL_TUNING_VALUE_STATISTICS.csv",index=False)
    if cond_resp_all: pd.concat(cond_resp_all,ignore_index=True).to_csv(outroot/"ALL_CONDITION_RESPONSE_STATISTICS.csv",index=False)
    if cond_sel_all: pd.concat(cond_sel_all,ignore_index=True).to_csv(outroot/"ALL_CONDITION_SELECTIVITY_STATISTICS.csv",index=False)
    save_json(outroot/"run_manifest.json",{
        "subject":subject,"dates":dates,"areas":areas,"modes":modes,"output_root":str(outroot),"input_files":provenance_all,
        "layers":{"L23_100to300um":"100 <= depth < 300 um","L45_300to600um":"300 <= depth <= 600 um"},
        "primary_inference":"paired session-level YELLOW-vs-GREEN Wilcoxon signed-rank tests",
        "difference_sign":"YELLOW - GREEN","pooled_cell_inference":"exploratory/descriptive only",
        "prerequisite_area_analysis":"am_tuning_area_analysis_v9.py",
        "primary_tuning_selectivity_metric":"tuning_lifetime_sparseness",
        "primary_responsiveness":"BH-FDR separately across cells at each tuning value; union across values",
        "alternate_dff_sensitivity":"whole-session median F0 and 60-s local prestimulus median F0 for lifetime sparseness",
        "selectivity_metrics":["tuning_lifetime_sparseness","tuning_gini_coefficient","tuning_fano_factor","tuning_fwhm"],
        "selectivity_profile_definition":"absolute magnitude of mean baseline-corrected 0-1 s dF/F response at each tuning value",
        "frequency_fwhm_units":"octaves","am_fwhm_units":"Hz",
        "fano_definition":"sample variance / mean across absolute tuning-response magnitudes",
        "numeric_tuning_axes":"base-2 logarithmic for positive frequency and AM-rate values",
    })
    print("\n"+"="*86); print("DONE"); print(f"Outputs saved under: {outroot}"); print("Primary tests are paired session-level YELLOW-vs-GREEN comparisons."); print("="*86)


if __name__ == "__main__":
    main()
