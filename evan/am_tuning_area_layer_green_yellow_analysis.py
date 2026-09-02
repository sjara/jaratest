#!/usr/bin/env python3
"""
Compare YELLOW versus GREEN AM-tuning responses within each AREA x LAYER stratum.

This is the third-stage follow-up analysis for am_tuning_area_analysis_v3.py.
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

PREREQUISITE OUTPUTS
--------------------
For each requested area and tuning mode, this script expects:

<TEMP_OUTPUT_PATH>/evan/am_tuning_area_analysis/<subject>/<area>/<date_tag>/
    <tuning_mode>/combined/combined_cell_results.csv
    <tuning_mode>/combined/combined_condition_results.csv

These are produced by am_tuning_area_analysis_v3.py.

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
import matplotlib.pyplot as plt
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
    "tuning_selectivity_contrast": {
        "label": "Tuning selectivity contrast (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "tuning_selectivity_index": {
        "label": "Tuning selectivity index",
        "session_agg": "mean",
        "reference": 0.0,
    },
}

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
                raise ValueError(f"{path} has no canonicalArea column; expected am_tuning_area_analysis_v3.py output.")
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
        msg += "\nRun am_tuning_area_analysis_v3.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)
    if not cell_frames:
        raise RuntimeError(f"No {mode} area tables were loaded.")

    cells = pd.concat(cell_frames, ignore_index=True, sort=False)
    conds = pd.concat(cond_frames, ignore_index=True, sort=False)

    req_cells = {
        "subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode",
        "stim_responsive_fdr","stim_excited_fdr","stim_suppressed_fdr","stim_response_mean",
        "best_tuning_response","peak_absolute_response","tuning_modulation_depth",
        "tuning_selectivity_contrast","tuning_selectivity_index","preferred_tuning_value_Hz",
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

def response_columns(df: pd.DataFrame, mode: str) -> tuple[list[str], np.ndarray, list[str]]:
    prefix = "response_freq_" if mode == "tuningFreq" else "response_AM_"
    parsed = []
    for c in df.columns:
        if c.startswith(prefix) and c.endswith("_Hz"):
            text = c[len(prefix):-3]
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
    return "Frequency (kHz)" if mode == "tuningFreq" else "AM rate (Hz)"


def mode_title(mode: str) -> str:
    return "Frequency tuning" if mode == "tuningFreq" else "AM-rate tuning"


def aggregate_sessions(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    rows = []
    group_cols = ["subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode"]
    response_cols, _, _ = response_columns(df, mode)
    for keys, sdf in df.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        n = len(sdf)
        row["n_cells"] = int(n)
        row["n_stim_responsive_fdr"] = int(sdf.stim_responsive_fdr.astype(bool).sum())
        row["pct_stim_responsive_fdr"] = 100*float(sdf.stim_responsive_fdr.astype(bool).mean()) if n else np.nan
        row["pct_stim_excited_fdr"] = 100*float(sdf.stim_excited_fdr.astype(bool).mean()) if n else np.nan
        row["pct_stim_suppressed_fdr"] = 100*float(sdf.stim_suppressed_fdr.astype(bool).mean()) if n else np.nan
        for metric, cfg in CONTINUOUS_METRICS.items():
            vals = finite_values(sdf[metric])
            if len(vals) == 0:
                row[metric] = np.nan
            elif cfg["session_agg"] == "median":
                row[metric] = float(np.median(vals))
            else:
                row[metric] = float(np.mean(vals))
        for col in response_cols:
            vals = finite_values(sdf[col])
            row[col] = float(np.mean(vals)) if len(vals) else np.nan
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
        "label":CONTINUOUS_METRICS[metric]["label"],
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
    for metric in CONTINUOUS_METRICS:
        if metric in cell_df.columns:
            out["continuous"][metric] = analyze_continuous_metric(cell_df, session_df, metric)
    if include_binary:
        for metric in BINARY_METRICS:
            if metric in cell_df.columns:
                out["binary"][metric] = analyze_binary_metric(cell_df, session_df, metric)
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

def plot_metric_grid(
    cell_df: pd.DataFrame, session_df: pd.DataFrame,
    area: str, layer_label: str, mode: str,
    output_path: Path, display_mode: str, subset_label: str,
) -> None:
    metrics = [m for m in CONTINUOUS_METRICS if m in cell_df.columns]
    if not metrics:
        return
    ncols = 3
    nrows = math.ceil(len(metrics)/ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(15, 4.8*nrows), squeeze=False)
    axes = axes.ravel()

    for ax, metric in zip(axes, metrics):
        cfg = CONTINUOUS_METRICS[metric]
        ref = cfg["reference"]
        if display_mode == "cells":
            allvals = finite_values(cell_df[metric])
            ylim = robust_cell_ylim(allvals, ref)
            for xpos, cls in enumerate(CELL_CLASSES):
                vals = finite_values(cell_df.loc[cell_df.cell_class == cls, metric])
                if len(vals):
                    jitter = np.linspace(-0.08,0.08,len(vals)) if len(vals)>1 else np.array([0.0])
                    ax.scatter(xpos+jitter, vals, s=16, alpha=0.35, color=CELL_CLASS_COLORS[cls])
                    m,se,n = mean_sem(vals)
                    ax.errorbar(xpos, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=8, capsize=5, lw=2, color=CELL_CLASS_COLORS[cls])
            if ylim:
                ax.set_ylim(ylim[0],ylim[1])
                if ylim[2]:
                    ax.text(.98,.02,f"display clips {ylim[2]} outlier(s)",transform=ax.transAxes,ha="right",va="bottom",fontsize=7,color="0.4")

        elif display_mode == "mean":
            means=[]; sems=[]; ns=[]
            for cls in CELL_CLASSES:
                m,se,n = mean_sem(cell_df.loc[cell_df.cell_class == cls, metric])
                means.append(m); sems.append(se); ns.append(n)
            ylim = optimized_ylim_from_summary(np.array(means),np.array(sems),[ref] if ref is not None else None)
            if ylim: ax.set_ylim(*ylim)
            for xpos,(cls,m,se,n) in enumerate(zip(CELL_CLASSES,means,sems,ns)):
                if np.isfinite(m):
                    ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=6,lw=2.2,color=CELL_CLASS_COLORS[cls])
                    annotate_mean_sem(ax,xpos,m,se,n,CELL_CLASS_COLORS[cls])

        elif display_mode == "session_paired":
            piv,y,g = paired_session_vectors(session_df,metric)
            for _,r in piv.iterrows():
                ax.plot([0,1],[r.green,r.yellow],color="0.6",alpha=.5,lw=.9)
                ax.scatter([0,1],[r.green,r.yellow],s=22,color=[CELL_CLASS_COLORS["green"],CELL_CLASS_COLORS["yellow"]],zorder=3)
            for xpos,cls in enumerate(CELL_CLASSES):
                m,se,n = mean_sem(session_df.loc[session_df.cell_class==cls,metric])
                if np.isfinite(m):
                    ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=6,lw=2.2,color=CELL_CLASS_COLORS[cls])

        elif display_mode == "session_mean":
            means=[]; sems=[]; ns=[]
            for cls in CELL_CLASSES:
                m,se,n=mean_sem(session_df.loc[session_df.cell_class==cls,metric]); means.append(m); sems.append(se); ns.append(n)
            ylim=optimized_ylim_from_summary(np.array(means),np.array(sems),[ref] if ref is not None else None)
            if ylim: ax.set_ylim(*ylim)
            for xpos,(cls,m,se,n) in enumerate(zip(CELL_CLASSES,means,sems,ns)):
                if np.isfinite(m):
                    ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=6,lw=2.2,color=CELL_CLASS_COLORS[cls])
                    annotate_mean_sem(ax,xpos,m,se,n,CELL_CLASS_COLORS[cls])

        if ref is not None:
            ax.axhline(ref,color="0.45",ls="--",lw=1)
        ax.set_xticks([0,1],["Green","Yellow"])
        ax.set_ylabel(cfg["label"])
        ax.set_title(cfg["label"])
        ax.grid(axis="y",alpha=.25)

    for ax in axes[len(metrics):]:
        ax.set_axis_off()
    mode_text = {
        "cells":"pooled cells + mean ± SEM",
        "mean":"pooled-cell mean ± SEM only",
        "session_paired":"paired session summaries",
        "session_mean":"session mean ± SEM only",
    }[display_mode]
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\n{subset_label}: GREEN vs YELLOW — {mode_text}",fontsize=14)
    fig.tight_layout(rect=[0,0,1,.94])
    fig.savefig(output_path,dpi=DPI,bbox_inches="tight")
    plt.close(fig)


def plot_tuning_profile(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    cols, values, labels = response_columns(cell_df,mode)
    if not cols:
        return
    x = np.arange(len(cols))
    fig,ax=plt.subplots(figsize=(9,5.8))
    allm=[]; alls=[]; text=[]
    for cls in CELL_CLASSES:
        cdf=cell_df[cell_df.cell_class==cls]
        means=[]; sems=[]; ns=[]
        for col in cols:
            m,se,n=mean_sem(cdf[col]); means.append(m); sems.append(se); ns.append(n)
        allm.extend(means); alls.extend(sems)
        ax.errorbar(x,means,yerr=sems,marker="o",capsize=4,lw=2,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
        text.append(cls.capitalize()+": "+"; ".join(f"{lab}={m:.3g}±{se:.2g} (n={n})" for lab,m,se,n in zip(labels,means,sems,ns) if np.isfinite(m)))
    ylim=optimized_ylim_from_summary(np.asarray(allm),np.asarray(alls),[0])
    if ylim: ax.set_ylim(*ylim)
    ax.axhline(0,color="0.45",ls="--",lw=1)
    ax.set_xticks(x,labels)
    ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Response (dF/F)")
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nGREEN vs YELLOW tuning profile — {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
    ax.text(.01,.01,"\n".join(text),transform=ax.transAxes,ha="left",va="bottom",fontsize=6.5,bbox=dict(boxstyle="round,pad=.3",facecolor="white",alpha=.72,edgecolor=".8"))
    fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profile_session(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    sdf=aggregate_sessions(cell_df,mode) if len(cell_df) else pd.DataFrame()
    cols,_,labels=response_columns(cell_df,mode)
    if not cols or len(sdf)==0: return
    x=np.arange(len(cols)); fig,ax=plt.subplots(figsize=(9,5.8)); allm=[]; alls=[]
    for cls in CELL_CLASSES:
        means=[]; sems=[]; ns=[]
        for col in cols:
            m,se,n=mean_sem(sdf.loc[sdf.cell_class==cls,col]); means.append(m); sems.append(se); ns.append(n)
        allm.extend(means); alls.extend(sems)
        ax.errorbar(x,means,yerr=sems,marker="o",capsize=4,lw=2,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
    ylim=optimized_ylim_from_summary(np.asarray(allm),np.asarray(alls),[0])
    if ylim: ax.set_ylim(*ylim)
    ax.axhline(0,color="0.45",ls="--",lw=1); ax.set_xticks(x,labels); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Session mean response (dF/F)")
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nGREEN vs YELLOW session tuning profile — {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.25); fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_selectivity_rasters(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    cols,_,labels=response_columns(cell_df,mode)
    if len(cols)<2: return
    fig,axes=plt.subplots(2,1,figsize=(9,7.5),squeeze=False); im=None
    for row,cls in enumerate(CELL_CLASSES):
        ax=axes[row,0]; cdf=cell_df[cell_df.cell_class==cls].copy()
        if len(cdf)==0:
            ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center",va="center"); ax.set_axis_off(); continue
        mat=cdf[cols].to_numpy(float); denom=np.nanmax(np.abs(mat),axis=1); good=np.isfinite(denom)&(denom>0)
        mat=mat[good]; cdf=cdf.iloc[np.where(good)[0]].copy()
        if len(mat)==0: continue
        norm=mat/denom[good,None]
        pref=pd.to_numeric(cdf.preferred_tuning_value_Hz,errors="coerce").to_numpy(float)
        order=np.argsort(np.nan_to_num(pref,nan=np.inf)); norm=norm[order]
        im=ax.imshow(norm,aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm")
        ax.set_xticks(np.arange(len(labels)),labels); ax.set_ylabel(f"{cls.capitalize()} cells")
        ax.set_title(f"{cls.capitalize()}: n={len(norm)} | sorted by preferred tuning value")
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\nGREEN vs YELLOW tuning rasters — {suffix.replace('_',' ')}",y=1.01)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Normalized tuning response",shrink=.75)
    fig.tight_layout(); fig.savefig(outdir/f"selectivity_rasters_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_preferred_distribution(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str) -> None:
    vals=sorted(pd.to_numeric(cell_df.preferred_tuning_value_Hz,errors="coerce").dropna().unique())
    if not vals: return
    x=np.arange(len(vals)); width=.34; fig,ax=plt.subplots(figsize=(9,5.5))
    for cls,shift in (("green",-width/2),("yellow",width/2)):
        cdf=cell_df[cell_df.cell_class==cls]; total=np.isfinite(pd.to_numeric(cdf.preferred_tuning_value_Hz,errors="coerce")).sum()
        pct=[100*np.sum(np.isclose(pd.to_numeric(cdf.preferred_tuning_value_Hz,errors="coerce"),v,equal_nan=False))/total if total else np.nan for v in vals]
        ax.bar(x+shift,pct,width,color=CELL_CLASS_COLORS[cls],alpha=.8,label=cls.capitalize())
    labels=[f"{v/1000:g}" for v in vals] if mode=="tuningFreq" else [f"{v:g}" for v in vals]
    ax.set_xticks(x,labels); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Cells preferring condition (%)")
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nPreferred tuning distribution — {suffix.replace('_',' ')}"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
    fig.tight_layout(); fig.savefig(outdir/f"preferred_tuning_distribution_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_responsiveness(cell_df: pd.DataFrame, session_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path) -> None:
    metrics=[(m,p,l) for m,(p,l) in BINARY_METRICS.items()]
    x=np.arange(len(metrics),dtype=float); offsets={"green":-.16,"yellow":.16}
    fig,ax=plt.subplots(figsize=(8,5.6))
    for cls in CELL_CLASSES:
        cdf=cell_df[cell_df.cell_class==cls]; vals=[100*float(cdf[m].astype(bool).mean()) if len(cdf) else np.nan for m,_,_ in metrics]
        ax.scatter(x+offsets[cls],vals,s=75,color=CELL_CLASS_COLORS[cls],label=cls.capitalize(),zorder=3)
        for xx,v in zip(x+offsets[cls],vals):
            if np.isfinite(v): ax.text(xx,v,f"{v:.1f}%",ha="center",va="bottom",fontsize=8,color=CELL_CLASS_COLORS[cls])
    ax.set_xticks(x,[m[2].replace("FDR ","").replace(" cells (%)","") for m in metrics]); ax.set_ylabel("Pooled cell percentage (%)")
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nGREEN vs YELLOW FDR responsiveness"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
    fig.tight_layout(); fig.savefig(outdir/"responsiveness_pooled_cell_percentages.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    fig,axes=plt.subplots(1,3,figsize=(14.5,4.8))
    for ax,(_,pct_col,label) in zip(axes,metrics):
        piv=session_df.pivot_table(index="session_key",columns="cell_class",values=pct_col,aggfunc="first")
        paired=piv[["green","yellow"]].dropna() if {"green","yellow"}.issubset(piv.columns) else pd.DataFrame(columns=["green","yellow"])
        for _,r in paired.iterrows():
            ax.plot([0,1],[r.green,r.yellow],color=".55",alpha=.5,lw=.9); ax.scatter([0,1],[r.green,r.yellow],s=24,color=[CELL_CLASS_COLORS["green"],CELL_CLASS_COLORS["yellow"]],zorder=3)
        for xpos,cls in enumerate(CELL_CLASSES):
            m,se,n=mean_sem(session_df.loc[session_df.cell_class==cls,pct_col])
            if np.isfinite(m): ax.errorbar(xpos,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=8,capsize=5,lw=2,color=CELL_CLASS_COLORS[cls])
        ax.set_xticks([0,1],["Green","Yellow"]); ax.set_ylabel("Session percentage (%)"); ax.set_title(label.replace("FDR ","")); ax.grid(axis="y",alpha=.25)
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\nPaired session-level responsiveness",fontsize=13); fig.tight_layout(rect=[0,0,1,.93])
    fig.savefig(outdir/"responsiveness_SESSION_PAIRED.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    fig,ax=plt.subplots(figsize=(9,5.8)); width=.26
    for cls,shift in (("green",-width/2),("yellow",width/2)):
        means=[]; sems=[]; ns=[]
        for _,pct_col,_ in metrics:
            m,se,n=mean_sem(session_df.loc[session_df.cell_class==cls,pct_col]); means.append(m); sems.append(se); ns.append(n)
        xx=x+shift; ax.errorbar(xx,means,yerr=sems,fmt="o",ms=8,capsize=5,lw=2,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
        for xpos,m,se,n in zip(xx,means,sems,ns):
            if np.isfinite(m): ax.text(xpos,m,f"{m:.1f}±{se:.1f}\nn={n}" if np.isfinite(se) else f"{m:.1f}\nn={n}",ha="center",va="bottom",fontsize=7,color=CELL_CLASS_COLORS[cls])
    ax.set_xticks(x,[m[2].replace("FDR ","").replace(" cells (%)","") for m in metrics]); ax.set_ylabel("Session percentage (%)")
    ax.set_title(f"{area} — {layer_label} — {mode_title(mode)}\nGREEN vs YELLOW — SESSION mean ± SEM"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
    fig.tight_layout(); fig.savefig(outdir/"responsiveness_SESSION_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_intensity_condition_grid(cond_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, suffix: str, metric: str, label: str, filename: str) -> None:
    if len(cond_df)==0: return
    values=np.sort(pd.to_numeric(cond_df.tuning_value_Hz,errors="coerce").dropna().unique())
    intensities=np.sort(pd.to_numeric(cond_df.intensity_dB,errors="coerce").dropna().unique())
    if len(values)==0 or len(intensities)==0: return
    ncols=min(3,len(intensities)); nrows=math.ceil(len(intensities)/ncols); fig,axes=plt.subplots(nrows,ncols,figsize=(5*ncols,4.4*nrows),squeeze=False); axes=axes.ravel()
    x=np.arange(len(values)); xlabels=[f"{v/1000:g}" for v in values] if mode=="tuningFreq" else [f"{v:g}" for v in values]
    for ax,intensity in zip(axes,intensities):
        allm=[]; alls=[]
        for cls in CELL_CLASSES:
            means=[]; sems=[]
            for value in values:
                vals=cond_df[(cond_df.cell_class==cls)&np.isclose(cond_df.intensity_dB,intensity)&np.isclose(cond_df.tuning_value_Hz,value)][metric]
                m,se,_=mean_sem(vals); means.append(m); sems.append(se)
            allm.extend(means); alls.extend(sems); ax.errorbar(x,means,yerr=sems,marker="o",capsize=3,lw=2,color=CELL_CLASS_COLORS[cls],label=cls.capitalize())
        ylim=optimized_ylim_from_summary(np.asarray(allm),np.asarray(alls),[0])
        if ylim: ax.set_ylim(*ylim)
        ax.axhline(0,color=".45",ls="--",lw=1); ax.set_xticks(x,xlabels); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel(label); ax.set_title(f"{intensity:g} dB"); ax.grid(axis="y",alpha=.25); ax.legend(frameon=False)
    for ax in axes[len(intensities):]: ax.set_axis_off()
    fig.suptitle(f"{area} — {layer_label} — {mode_title(mode)}\n{label} — {suffix.replace('_',' ')}",fontsize=14); fig.tight_layout(rect=[0,0,1,.94])
    fig.savefig(outdir/f"{filename}_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def make_metric_figures(cell_df: pd.DataFrame, area: str, layer_label: str, mode: str, outdir: Path, responsive_only: bool) -> None:
    suffix="FDR_responsive_only" if responsive_only else "all_cells"
    df=cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
    sdf=aggregate_sessions(df,mode) if len(df) else pd.DataFrame()
    if len(df)==0: return
    plot_metric_grid(df,sdf,area,layer_label,mode,outdir/f"green_yellow_response_metrics_{suffix}_with_cells.png","cells",suffix)
    plot_metric_grid(df,sdf,area,layer_label,mode,outdir/f"green_yellow_response_metrics_{suffix}_MEAN_SEM_ONLY.png","mean",suffix)
    plot_metric_grid(df,sdf,area,layer_label,mode,outdir/f"green_yellow_response_metrics_{suffix}_SESSION_PAIRED.png","session_paired",suffix)
    plot_metric_grid(df,sdf,area,layer_label,mode,outdir/f"green_yellow_response_metrics_{suffix}_SESSION_MEAN_SEM_ONLY.png","session_mean",suffix)
    plot_tuning_profile(df,area,layer_label,mode,outdir,suffix)
    plot_tuning_profile_session(df,area,layer_label,mode,outdir,suffix)
    plot_preferred_distribution(df,area,layer_label,mode,outdir,suffix)
    plot_selectivity_rasters(df,area,layer_label,mode,outdir,suffix)


# =============================================================================
# REPORTS / SUMMARY TABLES
# =============================================================================

def write_figure_index(outdir: Path) -> None:
    figs=sorted(p.name for p in outdir.glob("*.png"))
    (outdir/"FIGURE_INDEX.txt").write_text("\n".join(figs)+("\n" if figs else ""))


def write_report(path: Path, subject: str, dates: list[str], area: str, layer_key: str, mode: str, cell_df: pd.DataFrame, session_df: pd.DataFrame, stats_all: dict[str, Any], stats_resp: dict[str, Any]) -> None:
    layer_label=LAYERS[layer_key][2]
    lines=[
        "AM_TUNING AREA x LAYER GREEN-vs-YELLOW REPORT",
        "="*72,
        f"Subject: {subject}", f"Dates: {', '.join(dates)}", f"Area: {area}", f"Layer: {layer_label}", f"Tuning mode: {mode_title(mode)}",
        f"Cells: {len(cell_df)} | sessions: {cell_df.session_key.nunique() if len(cell_df) else 0}",
        f"Green cells: {sum(cell_df.cell_class=='green')} | Yellow cells: {sum(cell_df.cell_class=='yellow')}",
        "",
        "PRIMARY INFERENCE: paired session-level YELLOW vs GREEN Wilcoxon signed-rank tests.",
        "All paired differences are defined as YELLOW - GREEN.",
        "Pooled-cell tests are exploratory/descriptive only.", "",
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
    print("AM_TUNING AREA x LAYER GREEN-vs-YELLOW ANALYSIS")
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
    })
    print("\n"+"="*86); print("DONE"); print(f"Outputs saved under: {outroot}"); print("Primary tests are paired session-level YELLOW-vs-GREEN comparisons."); print("="*86)


if __name__ == "__main__":
    main()
