#!/usr/bin/env python3
"""
GREEN-versus-YELLOW sound-tuning analysis within each AREA x LAYER stratum.

Prerequisite
------------
Run sound_tuning_area_analysis_v12.py for each requested cortical area first.
This script does not rerun Suite2p, event alignment, dF/F generation, or FDR
responsiveness testing. It consumes each area's v12 combined_cell_results.csv.

Area x layer strata
-------------------
    A1  x L2/3   100 <= depth < 300 um
    A1  x L4/5   300 <= depth <= 600 um
    AAF x L2/3   100 <= depth < 300 um
    AAF x L4/5   300 <= depth <= 600 um
    A2  x L2/3   100 <= depth < 300 um
    A2  x L4/5   300 <= depth <= 600 um

The 300-um boundary is assigned to L4/5, so a cell/session is never counted in
both layer bins.

Primary statistical convention
------------------------------
Sessions are the biological replicate for inferential GREEN-vs-YELLOW tests.
Within a session, GREEN and YELLOW summaries are paired and compared with a
2-sided Wilcoxon signed-rank test. Pooled-cell Mann-Whitney or Fisher tests are
saved only as exploratory/descriptive analyses.

The script uses v12's condition-specific responsiveness flags:
    sound_responsive_fdr          : FI or FO or >=1 AM rate responsive
    fade_in_responsive_fdr        : FI responsive
    fade_out_responsive_fdr       : FO responsive
    fi_or_fo_responsive_fdr       : FI or FO responsive
    any_am_rate_responsive_fdr    : >=1 AM rate responsive
    sound_excited_fdr             : excited under v12 primary classification
    sound_suppressed_fdr          : suppressed under v12 primary classification

Selectivity metrics
-------------------
Primary FI/FO selectivity uses v12's bounded signed-response index:

    SI_FI/FO = (R_FI - R_FO) / (|R_FI| + |R_FO|)

with NaN when the denominator is zero. FI/best-AM selectivity retains the v12
upstream definition. AM selectivity is lifetime sparseness.

Responsive-only inclusion rules
--------------------------------
    FI/FO selectivity        : FI-or-FO responsive cells
    FI/best-AM selectivity   : FI OR >=1 AM-rate responsive cells
    AM lifetime sparseness   : >=1 AM-rate responsive cells
    FI/FO response profile   : FI-or-FO responsive cells
    AM response profile      : >=1 AM-rate responsive cells

Alternate dF/F sensitivity analyses
------------------------------------
v12 exports two alternate dF/F versions. These are used for FI/FO selectivity
sensitivity analyses while retaining the PRIMARY v12 FDR responsiveness flags:
    1) whole-session median F0
    2) 60-s local prestimulus-only median F0

The alternate analyses do NOT recompute FDR responsiveness.

Expected prerequisite output for each area
------------------------------------------
<TEMP_OUTPUT_PATH>/evan/sound_tuning_area_analysis/<subject>/<area>/<dates>/
    combined/combined_cell_results.csv

Example
-------
python sound_tuning_area_layer_green_yellow_analysis_v3.py imag039 \
    --dates 20260717 20260729 20260730

Optional dry run
----------------
python sound_tuning_area_layer_green_yellow_analysis_v3.py imag039 \
    --dates 20260717 20260729 20260730 --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from jaratoolbox import settings


# =============================================================================
# CONSTANTS
# =============================================================================

AREAS = ("A1", "AAF", "A2")
CELL_CLASSES = ("green", "yellow")
CELL_CLASS_COLORS = {"green": "limegreen", "yellow": "goldenrod"}

LAYERS = {
    "L23_100to300um": (100.0, 300.0, "L2/3 (100-<300 um)"),
    "L45_300to600um": (300.0, 600.0, "L4/5 (300-600 um)"),
}

DPI = 180

RESPONSIVENESS_METRICS = [
    ("sound_responsive_fdr", "Any sound responsive"),
    ("fade_in_responsive_fdr", "Fade-in responsive"),
    ("fade_out_responsive_fdr", "Fade-out responsive"),
    ("fi_or_fo_responsive_fdr", "FI or FO responsive"),
    ("any_am_rate_responsive_fdr", "AM responsive (>=1 rate)"),
    ("sound_excited_fdr", "Excited"),
    ("sound_suppressed_fdr", "Suppressed"),
]

SELECTIVITY_SPECS = {
    "fade_in_vs_fade_out_selectivity": {
        "label": "FI/FO selectivity index",
        "reference": 0.0,
        "equation": r"$SI_{FI/FO}=(R_{FI}-R_{FO})/(|R_{FI}|+|R_{FO}|)$",
        "bounded": True,
    },
    "fade_in_vs_best_am_selectivity": {
        "label": "FI/best-AM selectivity index",
        "reference": 0.0,
        "equation": r"FI/best-AM selectivity: v12 upstream definition",
        "bounded": False,
    },
    "am_rate_lifetime_sparseness": {
        "label": "AM-rate lifetime sparseness",
        "reference": None,
        "equation": r"$S_{life}=\frac{1-(\sum R_i/N)^2/(\sum R_i^2/N)}{1-1/N}$",
        "bounded": False,
    },
}

ALT_FI_FO = {
    "session_median_dff": {
        "metric": "fade_in_vs_fade_out_selectivity_session_median_dff",
        "label": "whole-session median F0 dF/F",
        "stem": "SESSION_MEDIAN_DFF",
    },
    "60s_prestim_median_dff": {
        "metric": "fade_in_vs_fade_out_selectivity_60s_prestim_median_dff",
        "label": "60-s local prestimulus-only median F0 dF/F",
        "stem": "60S_PRESTIM_MEDIAN_DFF",
    },
}

BOOL_COLUMNS = [m[0] for m in RESPONSIVENESS_METRICS] + [
    "fi_or_any_am_responsive_fdr",
]

PRIMARY_SELECTIVITY_METRICS = [
    "fade_in_vs_fade_out_selectivity",
    "fade_in_vs_best_am_selectivity",
    "am_rate_lifetime_sparseness",
]


# =============================================================================
# COMMAND LINE / PATHS
# =============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("subject", help="Subject ID, e.g. imag039.")
    parser.add_argument(
        "--dates", nargs="+", required=True,
        help="Dates used for the v12 area analyses, e.g. 20260717 20260729 20260730.",
    )
    parser.add_argument(
        "--areas", nargs="+", default=list(AREAS), choices=list(AREAS),
        help="Areas to analyze. Default: A1 AAF A2.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print expected input/output paths and stop before loading tables.",
    )
    return parser.parse_args()


def date_tag(dates: Iterable[str]) -> str:
    return "_".join(str(d) for d in dates)


def expected_area_csv(subject: str, area: str, dates: list[str]) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH) / "evan" / "sound_tuning_area_analysis"
        / subject / area / date_tag(dates) / "combined" / "combined_cell_results.csv"
    )


def output_root(subject: str, dates: list[str]) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH) / "evan"
        / "sound_tuning_area_layer_green_yellow_analysis"
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


def finite_values(values: Iterable[Any]) -> np.ndarray:
    arr = pd.to_numeric(pd.Series(values), errors="coerce").to_numpy(float)
    return arr[np.isfinite(arr)]


def mean_sem(values: Iterable[Any]) -> tuple[float, float, int]:
    vals = finite_values(values)
    if len(vals) == 0:
        return np.nan, np.nan, 0
    return (
        float(np.mean(vals)),
        float(stats.sem(vals)) if len(vals) > 1 else np.nan,
        int(len(vals)),
    )


def median_iqr(values: Iterable[Any]) -> tuple[float, float, float, int]:
    vals = finite_values(values)
    if len(vals) == 0:
        return np.nan, np.nan, np.nan, 0
    return (
        float(np.median(vals)),
        float(np.percentile(vals, 25)),
        float(np.percentile(vals, 75)),
        int(len(vals)),
    )


def parse_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s.fillna(False).astype(bool)
    return s.astype(str).str.lower().isin(["true", "1", "yes", "y", "t"])


def p_text(p: float) -> str:
    if not np.isfinite(p):
        return "p=n/a"
    if p < 1e-4:
        return "p<1e-4"
    return f"p={p:.4f}"


def holm_adjust(pvalues: Iterable[Any]) -> np.ndarray:
    """Holm step-down adjusted p values; NaNs remain NaN."""
    p = np.asarray(list(pvalues), dtype=float)
    out = np.full(len(p), np.nan, dtype=float)
    valid_idx = np.flatnonzero(np.isfinite(p))
    if len(valid_idx) == 0:
        return out
    pv = p[valid_idx]
    order = np.argsort(pv)
    ranked = pv[order]
    m = len(ranked)
    adj_ranked = np.empty(m, dtype=float)
    running = 0.0
    for i, val in enumerate(ranked):
        candidate = (m - i) * val
        running = max(running, candidate)
        adj_ranked[i] = min(1.0, running)
    unsorted = np.empty(m, dtype=float)
    unsorted[order] = adj_ranked
    out[valid_idx] = unsorted
    return out


def cliffs_delta(x: Iterable[Any], y: Iterable[Any]) -> float:
    """Positive means x tends to be larger than y."""
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return np.nan
    ranks = stats.rankdata(np.concatenate([x, y]))
    rx = np.sum(ranks[:len(x)])
    u = rx - len(x) * (len(x) + 1) / 2
    return float((2 * u) / (len(x) * len(y)) - 1)


def safe_mannwhitney(x: Iterable[Any], y: Iterable[Any]) -> dict[str, Any]:
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return {"n1": len(x), "n2": len(y), "U": np.nan, "p": np.nan, "cliffs_delta": np.nan}
    try:
        res = stats.mannwhitneyu(x, y, alternative="two-sided", method="auto")
        return {
            "n1": int(len(x)), "n2": int(len(y)),
            "U": float(res.statistic), "p": float(res.pvalue),
            "cliffs_delta": cliffs_delta(x, y),
        }
    except Exception:
        return {"n1": len(x), "n2": len(y), "U": np.nan, "p": np.nan, "cliffs_delta": np.nan}


def safe_wilcoxon_pairs(yellow: Iterable[Any], green: Iterable[Any]) -> dict[str, Any]:
    """Two-sided paired Wilcoxon. Difference sign is YELLOW - GREEN."""
    y = pd.to_numeric(pd.Series(yellow), errors="coerce").to_numpy(float)
    g = pd.to_numeric(pd.Series(green), errors="coerce").to_numpy(float)
    valid = np.isfinite(y) & np.isfinite(g)
    y = y[valid]
    g = g[valid]
    diff = y - g
    n = len(diff)
    base = {
        "n_paired_sessions": int(n), "W": np.nan, "p": np.nan,
        "mean_difference_yellow_minus_green": float(np.mean(diff)) if n else np.nan,
        "sem_difference": float(stats.sem(diff)) if n > 1 else np.nan,
        "median_difference_yellow_minus_green": float(np.median(diff)) if n else np.nan,
        "q1_difference": float(np.percentile(diff, 25)) if n else np.nan,
        "q3_difference": float(np.percentile(diff, 75)) if n else np.nan,
    }
    if n == 0:
        return base
    if np.allclose(diff, 0, equal_nan=False):
        base.update({"W": 0.0, "p": 1.0})
        return base
    try:
        res = stats.wilcoxon(y, g, alternative="two-sided", zero_method="wilcox", method="auto")
        base.update({"W": float(res.statistic), "p": float(res.pvalue)})
    except Exception:
        pass
    return base


def fisher_green_yellow(df: pd.DataFrame, binary_col: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    counts = {}
    for cls in CELL_CLASSES:
        cdf = df[df["cell_class"] == cls]
        n = len(cdf)
        pos = int(cdf[binary_col].astype(bool).sum()) if n else 0
        counts[cls] = (pos, n)
        out[cls] = {
            "n_cells": int(n), "positive": pos,
            "percent": 100.0 * pos / n if n else np.nan,
        }
    yp, yn = counts["yellow"]
    gp, gn = counts["green"]
    if yn == 0 or gn == 0:
        odds, p = np.nan, np.nan
    else:
        try:
            odds, p = stats.fisher_exact([[yp, yn - yp], [gp, gn - gp]])
        except Exception:
            odds, p = np.nan, np.nan
    out["yellow_vs_green_fisher"] = {
        "odds_ratio": float(odds) if np.isfinite(odds) else np.nan,
        "p": float(p) if np.isfinite(p) else np.nan,
    }
    return out


def robust_ylim(values: Iterable[Any], reference: float | None = None, bounded: bool = False) -> tuple[float, float] | None:
    vals = finite_values(values)
    if bounded:
        return (-1.05, 1.05)
    if reference is not None:
        vals = np.concatenate([vals, [reference]]) if len(vals) else np.array([reference], float)
    if len(vals) == 0:
        return None
    if len(vals) >= 10:
        lo, hi = np.percentile(vals, [1, 99])
    else:
        lo, hi = np.min(vals), np.max(vals)
    if not np.isfinite(lo) or not np.isfinite(hi):
        return None
    if np.isclose(lo, hi):
        pad = max(0.1, abs(lo) * 0.2)
    else:
        pad = 0.12 * (hi - lo)
    return float(lo - pad), float(hi + pad)


# =============================================================================
# LOAD / FILTER DATA
# =============================================================================

def _am_primary_columns(df: pd.DataFrame) -> list[tuple[float, str]]:
    found = []
    pat = re.compile(r"^am_response_([0-9]+(?:\.[0-9]+)?)Hz$")
    for col in df.columns:
        m = pat.match(col)
        if m:
            found.append((float(m.group(1)), col))
    return sorted(found, key=lambda x: x[0])


def load_area_tables(subject: str, dates: list[str], areas: list[str]) -> pd.DataFrame:
    frames = []
    missing_paths = []
    for area in areas:
        path = expected_area_csv(subject, area, dates)
        if not path.exists():
            missing_paths.append(path)
            continue
        df = pd.read_csv(path)
        if "canonicalArea" not in df.columns:
            raise ValueError(f"{path} has no canonicalArea column; expected a v12 output table.")
        unexpected = set(df["canonicalArea"].dropna().astype(str).unique()) - {area}
        if unexpected:
            raise ValueError(f"{path} contains unexpected canonicalArea values: {sorted(unexpected)}")
        frames.append(df)

    if missing_paths:
        msg = "Missing prerequisite v12 output(s):\n" + "\n".join(f"  {p}" for p in missing_paths)
        msg += "\nRun sound_tuning_area_analysis_v12.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)
    if not frames:
        raise RuntimeError("No area tables were loaded.")

    df = pd.concat(frames, ignore_index=True, sort=False)
    required = {
        "subject", "date", "session", "session_key", "canonicalArea", "brainArea",
        "depth", "cell_class",
        "sound_responsive_fdr", "fade_in_responsive_fdr", "fade_out_responsive_fdr",
        "fi_or_fo_responsive_fdr", "any_am_rate_responsive_fdr",
        "sound_excited_fdr", "sound_suppressed_fdr",
        "fade_in_response", "fade_out_response",
        "fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity",
        "am_rate_lifetime_sparseness",
        "fade_in_vs_fade_out_selectivity_session_median_dff",
        "fade_in_vs_fade_out_selectivity_60s_prestim_median_dff",
    }
    missing_cols = sorted(required - set(df.columns))
    if missing_cols:
        raise ValueError(
            "Combined cell table(s) are missing v12-required columns:\n  "
            + "\n  ".join(missing_cols)
        )
    if len(_am_primary_columns(df)) == 0:
        raise ValueError("No primary am_response_<rate>Hz columns were found in the v12 combined tables.")

    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")
    for col in BOOL_COLUMNS:
        if col in df.columns:
            df[col] = parse_bool_series(df[col])
    df = df[df["cell_class"].isin(CELL_CLASSES)].copy()
    return df


def subset_layer(df: pd.DataFrame, layer_key: str) -> pd.DataFrame:
    low, high, _ = LAYERS[layer_key]
    depth = pd.to_numeric(df["depth"], errors="coerce")
    if layer_key.startswith("L23"):
        mask = (depth >= low) & (depth < high)
    else:
        mask = (depth >= low) & (depth <= high)
    return df.loc[mask].copy()


def analysis_subset(df: pd.DataFrame, kind: str) -> pd.DataFrame:
    if kind == "all":
        return df.copy()
    mapping = {
        "fi_fo": "fi_or_fo_responsive_fdr",
        "fi_am": "fi_or_any_am_responsive_fdr",
        "am": "any_am_rate_responsive_fdr",
    }
    col = mapping[kind]
    if col not in df.columns and kind == "fi_am":
        mask = df["fade_in_responsive_fdr"].astype(bool) | df["any_am_rate_responsive_fdr"].astype(bool)
        return df.loc[mask].copy()
    return df.loc[df[col].astype(bool)].copy()


# =============================================================================
# SESSION AGGREGATION
# =============================================================================

def aggregate_sessions(df: pd.DataFrame, numeric_columns: Iterable[str] | None = None) -> pd.DataFrame:
    """One row per session x class; numeric values are means across included cells."""
    if numeric_columns is None:
        numeric_columns = []
    numeric_columns = [c for c in numeric_columns if c in df.columns]
    group_cols = [
        "subject", "date", "session", "session_key", "canonicalArea",
        "brainArea", "cell_class",
    ]
    rows = []
    for keys, sdf in df.groupby(group_cols, dropna=False, sort=True):
        row = dict(zip(group_cols, keys))
        row["n_cells"] = int(len(sdf))
        depth_vals = finite_values(sdf["depth"])
        row["depth"] = float(np.mean(depth_vals)) if len(depth_vals) else np.nan
        for col in numeric_columns:
            vals = finite_values(sdf[col])
            row[col] = float(np.mean(vals)) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def session_percentages(df: pd.DataFrame, binary_col: str) -> pd.DataFrame:
    group_cols = ["subject", "date", "session", "session_key", "canonicalArea", "brainArea", "cell_class"]
    rows = []
    for keys, sdf in df.groupby(group_cols, dropna=False, sort=True):
        row = dict(zip(group_cols, keys))
        vals = sdf[binary_col].astype(bool).to_numpy(float)
        row["n_cells"] = int(len(vals))
        row["n_positive"] = int(np.sum(vals))
        row["percent"] = 100.0 * float(np.mean(vals)) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def paired_session_vectors(session_df: pd.DataFrame, value_col: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    if len(session_df) == 0 or value_col not in session_df.columns:
        empty = pd.DataFrame(columns=["yellow", "green"])
        return empty, np.array([]), np.array([])
    piv = session_df.pivot_table(index="session_key", columns="cell_class", values=value_col, aggfunc="first")
    for cls in ("yellow", "green"):
        if cls not in piv.columns:
            piv[cls] = np.nan
    piv = piv[["yellow", "green"]]
    valid = np.isfinite(pd.to_numeric(piv["yellow"], errors="coerce")) & np.isfinite(pd.to_numeric(piv["green"], errors="coerce"))
    paired = piv.loc[valid].copy()
    return paired, paired["yellow"].to_numpy(float), paired["green"].to_numpy(float)


# =============================================================================
# STATISTICS
# =============================================================================

def pooled_continuous_stats(df: pd.DataFrame, metric: str) -> dict[str, Any]:
    summary = {}
    for cls in CELL_CLASSES:
        vals = df.loc[df["cell_class"] == cls, metric]
        m, se, n = mean_sem(vals)
        med, q1, q3, _ = median_iqr(vals)
        summary[cls] = {"n_cells": n, "mean": m, "sem": se, "median": med, "q1": q1, "q3": q3}
    mw = safe_mannwhitney(
        df.loc[df["cell_class"] == "yellow", metric],
        df.loc[df["cell_class"] == "green", metric],
    )
    return {"summary": summary, "yellow_vs_green_mannwhitney": mw}


def session_continuous_stats(df: pd.DataFrame, metric: str) -> dict[str, Any]:
    sdf = aggregate_sessions(df, [metric])
    summary = {}
    for cls in CELL_CLASSES:
        vals = sdf.loc[sdf["cell_class"] == cls, metric] if len(sdf) else []
        m, se, n = mean_sem(vals)
        med, q1, q3, _ = median_iqr(vals)
        summary[cls] = {"n_sessions": n, "mean": m, "sem": se, "median": med, "q1": q1, "q3": q3}
    paired, y, g = paired_session_vectors(sdf, metric)
    test = safe_wilcoxon_pairs(y, g)
    test["paired_session_keys"] = paired.index.astype(str).tolist()
    return {"summary": summary, "yellow_vs_green_wilcoxon": test, "session_table": sdf}


def responsiveness_statistics(cells: pd.DataFrame) -> dict[str, Any]:
    results = {}
    raw_p = []
    keys = []
    for metric, label in RESPONSIVENESS_METRICS:
        sdf = session_percentages(cells, metric)
        paired, y, g = paired_session_vectors(sdf, "percent")
        w = safe_wilcoxon_pairs(y, g)
        w["paired_session_keys"] = paired.index.astype(str).tolist()
        per_class = {}
        for cls in CELL_CLASSES:
            vals = sdf.loc[sdf["cell_class"] == cls, "percent"] if len(sdf) else []
            m, se, n = mean_sem(vals)
            per_class[cls] = {"mean_percent": m, "sem_percent": se, "n_sessions": n}
        fisher = fisher_green_yellow(cells, metric)
        results[metric] = {
            "label": label,
            "session_level_primary_paired": {"summary": per_class, "yellow_vs_green_wilcoxon": w},
            "pooled_cell_exploratory": fisher,
        }
        keys.append(metric)
        raw_p.append(w["p"])
    adj = holm_adjust(raw_p)
    for key, ap in zip(keys, adj):
        results[key]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]["holm_p_across_7_responsiveness_tests"] = float(ap) if np.isfinite(ap) else np.nan
    return results


def selectivity_statistics(cells: pd.DataFrame) -> dict[str, Any]:
    out: dict[str, Any] = {"all_cells": {}, "responsive_only": {}, "alternate_dff_sensitivity": {}}

    # All-cell pooled exploratory metrics.
    for metric in PRIMARY_SELECTIVITY_METRICS:
        out["all_cells"].setdefault(metric, {})["pooled_cell_exploratory"] = pooled_continuous_stats(cells, metric)

    # Primary session inference: FI/FO and FI/best-AM only; Holm across 2.
    session_metrics = ["fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity"]
    raw = []
    for metric in session_metrics:
        ss = session_continuous_stats(cells, metric)
        out["all_cells"].setdefault(metric, {})["session_level_primary_paired"] = {
            "summary": ss["summary"], "yellow_vs_green_wilcoxon": ss["yellow_vs_green_wilcoxon"]
        }
        raw.append(ss["yellow_vs_green_wilcoxon"]["p"])
    adj = holm_adjust(raw)
    for metric, ap in zip(session_metrics, adj):
        out["all_cells"][metric]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]["holm_p_across_2_primary_selectivity_tests"] = float(ap) if np.isfinite(ap) else np.nan

    # Responsive-only, metric-specific subsets.
    subset_map = {
        "fade_in_vs_fade_out_selectivity": "fi_fo",
        "fade_in_vs_best_am_selectivity": "fi_am",
        "am_rate_lifetime_sparseness": "am",
    }
    for metric, kind in subset_map.items():
        sub = analysis_subset(cells, kind)
        out["responsive_only"].setdefault(metric, {})["subset_rule"] = kind
        out["responsive_only"][metric]["pooled_cell_exploratory"] = pooled_continuous_stats(sub, metric)

    raw = []
    for metric in session_metrics:
        sub = analysis_subset(cells, subset_map[metric])
        ss = session_continuous_stats(sub, metric)
        out["responsive_only"][metric]["session_level_primary_paired"] = {
            "summary": ss["summary"], "yellow_vs_green_wilcoxon": ss["yellow_vs_green_wilcoxon"]
        }
        raw.append(ss["yellow_vs_green_wilcoxon"]["p"])
    adj = holm_adjust(raw)
    for metric, ap in zip(session_metrics, adj):
        out["responsive_only"][metric]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]["holm_p_across_2_primary_selectivity_tests"] = float(ap) if np.isfinite(ap) else np.nan

    # Alternate FI/FO dF/F sensitivity analyses: raw p only, not in primary Holm family.
    for alt_key, cfg in ALT_FI_FO.items():
        metric = cfg["metric"]
        all_s = session_continuous_stats(cells, metric)
        all_pooled = pooled_continuous_stats(cells, metric)
        resp = analysis_subset(cells, "fi_fo")
        resp_s = session_continuous_stats(resp, metric)
        out["alternate_dff_sensitivity"][alt_key] = {
            "label": cfg["label"],
            "metric": metric,
            "all_cells": {
                "pooled_cell_exploratory": all_pooled,
                "session_level_paired_sensitivity": {
                    "summary": all_s["summary"],
                    "yellow_vs_green_wilcoxon": all_s["yellow_vs_green_wilcoxon"],
                },
            },
            "fi_or_fo_responsive_cells": {
                "session_level_paired_sensitivity": {
                    "summary": resp_s["summary"],
                    "yellow_vs_green_wilcoxon": resp_s["yellow_vs_green_wilcoxon"],
                },
            },
            "multiple_comparison_note": "Sensitivity analysis; not included in the primary Holm family.",
        }
    return out


def condition_profile_statistics(cells: pd.DataFrame, am_cols: list[tuple[float, str]]) -> dict[str, Any]:
    primary_cols = [("fade_in_response", "Fade-in"), ("fade_out_response", "Fade-out")] + [(col, f"AM {rate:g} Hz") for rate, col in am_cols]

    def family(df: pd.DataFrame, cols: list[tuple[str, str]], holm_label: str) -> dict[str, Any]:
        results = {}
        raw = []
        for col, label in cols:
            ss = session_continuous_stats(df, col)
            results[col] = {
                "label": label,
                "summary": ss["summary"],
                "yellow_vs_green_wilcoxon": ss["yellow_vs_green_wilcoxon"],
            }
            raw.append(ss["yellow_vs_green_wilcoxon"]["p"])
        adj = holm_adjust(raw)
        for (col, _), ap in zip(cols, adj):
            results[col]["yellow_vs_green_wilcoxon"][holm_label] = float(ap) if np.isfinite(ap) else np.nan
        return results

    all_cells = family(cells, primary_cols, "holm_p_across_all_displayed_conditions")
    fi_fo_cells = analysis_subset(cells, "fi_fo")
    fi_fo = family(fi_fo_cells, primary_cols[:2], "holm_p_across_FI_FO")
    am_cells = analysis_subset(cells, "am")
    am_only_cols = primary_cols[2:]
    am = family(am_cells, am_only_cols, "holm_p_across_AM_rates")

    return {
        "all_cells": all_cells,
        "responsive_only": {
            "fi_or_fo_responsive": fi_fo,
            "any_am_rate_responsive": am,
        },
    }


def run_statistics(cells: pd.DataFrame, am_cols: list[tuple[float, str]]) -> dict[str, Any]:
    return {
        "statistical_convention": {
            "primary_replicate": "session",
            "primary_test": "paired two-sided Wilcoxon signed-rank, YELLOW versus GREEN within session",
            "difference_sign": "YELLOW - GREEN",
            "pooled_cells": "exploratory/descriptive only",
        },
        "responsiveness": responsiveness_statistics(cells),
        "selectivity": selectivity_statistics(cells),
        "condition_profiles": condition_profile_statistics(cells, am_cols),
    }


# =============================================================================
# PLOTTING HELPERS
# =============================================================================

def _add_reference(ax, reference: float | None) -> None:
    if reference is not None:
        ax.axhline(reference, ls="--", lw=0.9, color="0.45", zorder=0)


def _session_point_plot(
    df: pd.DataFrame,
    metric: str,
    ylabel: str,
    title: str,
    output_path: Path,
    test: dict[str, Any],
    equation: str | None = None,
    bounded: bool = False,
    sensitivity: bool = False,
) -> None:
    sdf = aggregate_sessions(df, [metric])
    paired, _, _ = paired_session_vectors(sdf, metric)
    fig, ax = plt.subplots(figsize=(6.8, 6.3))
    session_keys = list(paired.index.astype(str))
    offsets = np.linspace(-0.045, 0.045, max(len(session_keys), 1))

    for i, sk in enumerate(session_keys):
        g = float(paired.loc[sk, "green"])
        y = float(paired.loc[sk, "yellow"])
        ax.plot([0 + offsets[i], 1 + offsets[i]], [g, y], color="0.55", alpha=0.30, lw=0.9, zorder=1)
        ax.scatter(0 + offsets[i], g, s=24, color=CELL_CLASS_COLORS["green"], alpha=0.55, zorder=2)
        ax.scatter(1 + offsets[i], y, s=24, color=CELL_CLASS_COLORS["yellow"], alpha=0.55, zorder=2)

    for xi, cls in enumerate(CELL_CLASSES):
        vals = sdf.loc[sdf["cell_class"] == cls, metric] if len(sdf) else []
        m, se, n = mean_sem(vals)
        if np.isfinite(m):
            ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=10,
                        capsize=6, elinewidth=2.5, color=CELL_CLASS_COLORS[cls], zorder=5)
            ax.annotate(f"{m:.3g} ± {se:.2g}\nn={n} sessions" if np.isfinite(se) else f"{m:.3g}\nn={n} sessions",
                        (xi, m), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=8,
                        color=CELL_CLASS_COLORS[cls])

    _add_reference(ax, 0.0 if "selectivity" in metric else None)
    w = test
    raw = w.get("p", np.nan)
    holm_keys = [k for k in w if k.startswith("holm_p_")]
    stat_line = f"paired Wilcoxon: W={w.get('W', np.nan):.3g}, {p_text(raw)}, n={w.get('n_paired_sessions', 0)}"
    if holm_keys:
        stat_line += f"; Holm p={w[holm_keys[0]]:.4g}" if np.isfinite(w[holm_keys[0]]) else "; Holm p=n/a"
    if sensitivity:
        stat_line += "\nSensitivity analysis; not in primary Holm family"

    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel(ylabel)
    ax.set_title(f"{title}\n{stat_line}", fontsize=10)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    if bounded:
        ax.set_ylim(-1.05, 1.05)
    if equation:
        ax.text(0.5, -0.16, equation, transform=ax.transAxes, ha="center", va="top", fontsize=9)
        fig.subplots_adjust(bottom=0.23)
    else:
        fig.tight_layout()
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def _cell_point_plot(
    df: pd.DataFrame,
    metric: str,
    ylabel: str,
    title: str,
    output_path: Path,
    pooled_stats: dict[str, Any],
    equation: str | None = None,
    bounded: bool = False,
    sensitivity: bool = False,
) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 6.3))
    rng = np.random.default_rng(2026)
    display = []
    for xi, cls in enumerate(CELL_CLASSES):
        vals = finite_values(df.loc[df["cell_class"] == cls, metric])
        if len(vals):
            ax.scatter(np.full(len(vals), xi) + rng.uniform(-0.09, 0.09, len(vals)), vals,
                       s=20, alpha=0.24, color=CELL_CLASS_COLORS[cls], edgecolors="none")
            m, se, n = mean_sem(vals)
            ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=10,
                        capsize=6, elinewidth=2.4, color=CELL_CLASS_COLORS[cls], zorder=5)
            ax.annotate(f"{m:.3g} ± {se:.2g}\nn={n} cells" if np.isfinite(se) else f"{m:.3g}\nn={n} cells",
                        (xi, m), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=8,
                        color=CELL_CLASS_COLORS[cls])
            display.extend(vals.tolist())
    _add_reference(ax, 0.0 if "selectivity" in metric else None)
    mw = pooled_stats["yellow_vs_green_mannwhitney"]
    stat_line = f"exploratory pooled Mann-Whitney: U={mw.get('U', np.nan):.3g}, {p_text(mw.get('p', np.nan))}"
    if sensitivity:
        stat_line += "\nSensitivity analysis"
    ax.set_xticks([0, 1], ["Green", "Yellow"])
    ax.set_ylabel(ylabel)
    ax.set_title(f"{title}\n{stat_line}", fontsize=10)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    lim = robust_ylim(display, 0.0 if "selectivity" in metric else None, bounded=bounded)
    if lim:
        ax.set_ylim(*lim)
    if equation:
        ax.text(0.5, -0.16, equation, transform=ax.transAxes, ha="center", va="top", fontsize=9)
        fig.subplots_adjust(bottom=0.23)
    else:
        fig.tight_layout()
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_responsiveness(cells: pd.DataFrame, stats_out: dict[str, Any], area: str, layer_label: str, output_dir: Path) -> None:
    resp_stats = stats_out["responsiveness"]
    x = np.arange(len(RESPONSIVENESS_METRICS), dtype=float)
    offsets = {"green": -0.15, "yellow": 0.15}

    # Figure 1: session means + overall mean +/- SE for all seven categories.
    fig, ax = plt.subplots(figsize=(13.5, 6.0))
    for cls in CELL_CLASSES:
        for j, (metric, label) in enumerate(RESPONSIVENESS_METRICS):
            sdf = session_percentages(cells, metric)
            vals = finite_values(sdf.loc[sdf["cell_class"] == cls, "percent"] if len(sdf) else [])
            if len(vals):
                jitter = np.linspace(-0.045, 0.045, len(vals)) if len(vals) > 1 else np.array([0.0])
                ax.scatter(np.full(len(vals), x[j] + offsets[cls]) + jitter, vals, s=18,
                           color=CELL_CLASS_COLORS[cls], alpha=0.28, zorder=2)
                m, se, _ = mean_sem(vals)
                ax.errorbar(x[j] + offsets[cls], m, yerr=se if np.isfinite(se) else None,
                            fmt="o", ms=8, capsize=5, elinewidth=2.1,
                            color=CELL_CLASS_COLORS[cls], zorder=5)
    ax.set_xticks(x, [label for _, label in RESPONSIVENESS_METRICS], rotation=22, ha="right")
    ax.set_ylabel("Session percentage (%)")
    ax.set_title(f"{area} — {layer_label}\nV12 condition-specific responsiveness: session means + overall mean ± SE")
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "responsiveness_pooled_cell_percentages.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)

    # Figure 2: paired session figure, 2x4 with one unused panel.
    fig, axes = plt.subplots(2, 4, figsize=(16.5, 9.2), squeeze=False)
    axes = axes.ravel()
    for ax, (metric, label) in zip(axes, RESPONSIVENESS_METRICS):
        sdf = session_percentages(cells, metric)
        paired, _, _ = paired_session_vectors(sdf, "percent")
        offs = np.linspace(-0.035, 0.035, max(len(paired), 1))
        for i, (sk, row) in enumerate(paired.iterrows()):
            g = float(row["green"]); y = float(row["yellow"])
            ax.plot([0 + offs[i], 1 + offs[i]], [g, y], color="0.55", alpha=0.30, lw=0.8)
            ax.scatter(0 + offs[i], g, s=20, color=CELL_CLASS_COLORS["green"], alpha=0.55)
            ax.scatter(1 + offs[i], y, s=20, color=CELL_CLASS_COLORS["yellow"], alpha=0.55)
        for xi, cls in enumerate(CELL_CLASSES):
            vals = sdf.loc[sdf["cell_class"] == cls, "percent"] if len(sdf) else []
            m, se, _ = mean_sem(vals)
            if np.isfinite(m):
                ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=8,
                            capsize=5, elinewidth=2.2, color=CELL_CLASS_COLORS[cls], zorder=5)
        w = resp_stats[metric]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
        hp = w.get("holm_p_across_7_responsiveness_tests", np.nan)
        ax.set_xticks([0, 1], ["Green", "Yellow"])
        ax.set_ylabel("Session percentage (%)")
        ax.set_title(f"{label}\nWilcoxon {p_text(w.get('p', np.nan))}; Holm p={hp:.4g}; n={w.get('n_paired_sessions', 0)}" if np.isfinite(hp)
                     else f"{label}\nWilcoxon {p_text(w.get('p', np.nan))}; Holm p=n/a; n={w.get('n_paired_sessions', 0)}",
                     fontsize=9)
        ax.grid(axis="y", alpha=0.22)
        ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[len(RESPONSIVENESS_METRICS):]:
        ax.axis("off")
    fig.suptitle(f"{area} — {layer_label}\nPaired GREEN-vs-YELLOW session responsiveness; Holm across 7 categories", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_dir / "responsiveness_SESSION_PAIRED.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_selectivity_outputs(cells: pd.DataFrame, stats_out: dict[str, Any], area: str, layer_label: str, output_dir: Path) -> None:
    sel = stats_out["selectivity"]
    base_title = f"{area} — {layer_label}"

    # ALL CELLS: three pooled cell-point figures.
    for metric in PRIMARY_SELECTIVITY_METRICS:
        spec = SELECTIVITY_SPECS[metric]
        _cell_point_plot(
            cells, metric, spec["label"], f"{base_title}\nAll cells — {spec['label']}",
            output_dir / f"{metric}_green_yellow_all_cells_CELL_POINTS.png",
            sel["all_cells"][metric]["pooled_cell_exploratory"],
            equation=spec["equation"], bounded=spec.get("bounded", False),
        )

    # ALL CELLS: session points only for FI/FO and FI/best-AM.
    for metric in ["fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity"]:
        spec = SELECTIVITY_SPECS[metric]
        test = sel["all_cells"][metric]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
        _session_point_plot(
            cells, metric, spec["label"], f"{base_title}\nAll cells — {spec['label']}",
            output_dir / f"{metric}_green_yellow_all_cells_SESSION_POINTS.png",
            test, equation=spec["equation"], bounded=spec.get("bounded", False),
        )

    # ALL CELLS: two alternate-dF/F FI/FO cell + session sensitivity versions.
    fi_spec = SELECTIVITY_SPECS["fade_in_vs_fade_out_selectivity"]
    for alt_key, cfg in ALT_FI_FO.items():
        a = sel["alternate_dff_sensitivity"][alt_key]["all_cells"]
        metric = cfg["metric"]
        _cell_point_plot(
            cells, metric, fi_spec["label"], f"{base_title}\nAll cells — FI/FO selectivity\n{cfg['label']}",
            output_dir / f"fade_in_vs_fade_out_selectivity_green_yellow_all_cells_{cfg['stem']}_CELL_POINTS.png",
            a["pooled_cell_exploratory"], equation=fi_spec["equation"], bounded=True, sensitivity=True,
        )
        _session_point_plot(
            cells, metric, fi_spec["label"], f"{base_title}\nAll cells — FI/FO selectivity\n{cfg['label']}",
            output_dir / f"fade_in_vs_fade_out_selectivity_green_yellow_all_cells_{cfg['stem']}_SESSION_POINTS.png",
            a["session_level_paired_sensitivity"]["yellow_vs_green_wilcoxon"],
            equation=fi_spec["equation"], bounded=True, sensitivity=True,
        )

    # RESPONSIVE ONLY: three pooled cell-point figures with metric-specific subsets.
    subset_map = {
        "fade_in_vs_fade_out_selectivity": ("fi_fo", "FI-or-FO responsive cells"),
        "fade_in_vs_best_am_selectivity": ("fi_am", "FI or >=1-AM-rate responsive cells"),
        "am_rate_lifetime_sparseness": ("am", ">=1-AM-rate responsive cells"),
    }
    for metric in PRIMARY_SELECTIVITY_METRICS:
        spec = SELECTIVITY_SPECS[metric]
        kind, subset_label = subset_map[metric]
        sub = analysis_subset(cells, kind)
        _cell_point_plot(
            sub, metric, spec["label"], f"{base_title}\n{subset_label} — {spec['label']}",
            output_dir / f"{metric}_green_yellow_FDR_responsive_only_CELL_POINTS.png",
            sel["responsive_only"][metric]["pooled_cell_exploratory"],
            equation=spec["equation"], bounded=spec.get("bounded", False),
        )

    # RESPONSIVE ONLY: session points only for FI/FO and FI/best-AM.
    for metric in ["fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity"]:
        spec = SELECTIVITY_SPECS[metric]
        kind, subset_label = subset_map[metric]
        sub = analysis_subset(cells, kind)
        test = sel["responsive_only"][metric]["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
        _session_point_plot(
            sub, metric, spec["label"], f"{base_title}\n{subset_label} — {spec['label']}",
            output_dir / f"{metric}_green_yellow_FDR_responsive_only_SESSION_POINTS.png",
            test, equation=spec["equation"], bounded=spec.get("bounded", False),
        )

    # RESPONSIVE ONLY FI/FO: alternate-dF/F SESSION sensitivity versions only.
    resp_fi = analysis_subset(cells, "fi_fo")
    for alt_key, cfg in ALT_FI_FO.items():
        a = sel["alternate_dff_sensitivity"][alt_key]["fi_or_fo_responsive_cells"]
        _session_point_plot(
            resp_fi, cfg["metric"], fi_spec["label"],
            f"{base_title}\nFI-or-FO responsive cells — FI/FO selectivity\n{cfg['label']}",
            output_dir / f"fade_in_vs_fade_out_selectivity_green_yellow_FDR_responsive_only_{cfg['stem']}_SESSION_POINTS.png",
            a["session_level_paired_sensitivity"]["yellow_vs_green_wilcoxon"],
            equation=fi_spec["equation"], bounded=True, sensitivity=True,
        )


def _plot_profile_family(
    ax: plt.Axes,
    df: pd.DataFrame,
    columns: list[str],
    labels: list[str],
    x: np.ndarray,
    stats_family: dict[str, Any],
    title: str,
    break_after_index: int | None = None,
) -> None:
    sdf = aggregate_sessions(df, columns)
    for cls in CELL_CLASSES:
        color = CELL_CLASS_COLORS[cls]
        cs = sdf[sdf["cell_class"] == cls]
        # Individual session means, no within-session SD bars.
        for _, row in cs.iterrows():
            vals = np.array([row.get(c, np.nan) for c in columns], float)
            if break_after_index is None:
                ax.plot(x, vals, color=color, alpha=0.14, lw=0.9, marker="o", ms=2)
            else:
                ax.plot(x[:break_after_index + 1], vals[:break_after_index + 1], color=color, alpha=0.14, lw=0.9, marker="o", ms=2)
                ax.plot(x[break_after_index + 1:], vals[break_after_index + 1:], color=color, alpha=0.14, lw=0.9, marker="o", ms=2)
        means = []; sems = []
        for c in columns:
            m, se, _ = mean_sem(cs[c] if c in cs else [])
            means.append(m); sems.append(se)
        means = np.asarray(means, float); sems = np.asarray(sems, float)
        # Overall means: split line when requested, but error bars at every condition.
        if break_after_index is None:
            ax.plot(x, means, color=color, lw=2.6, marker="o", ms=5, label=f"{cls.capitalize()} overall mean ± SE")
        else:
            ax.plot(x[:break_after_index + 1], means[:break_after_index + 1], color=color, lw=2.6, marker="o", ms=5,
                    label=f"{cls.capitalize()} overall mean ± SE")
            ax.plot(x[break_after_index + 1:], means[break_after_index + 1:], color=color, lw=2.6, marker="o", ms=5)
        ax.errorbar(x, means, yerr=sems, fmt="none", capsize=3, elinewidth=1.7, color=color, zorder=4)

    ax.axhline(0, ls="--", lw=0.9, color="0.45")
    ax.set_xticks(x, labels, rotation=28, ha="right")
    ax.set_ylabel("Response (dF/F)")
    ax.set_title(title, fontsize=10)
    ax.grid(axis="y", alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8)

    # Compact p-value strip under the axes.
    texts = []
    for c, lab in zip(columns, labels):
        w = stats_family[c]["yellow_vs_green_wilcoxon"]
        hk = [k for k in w if k.startswith("holm_p_")]
        hp = w[hk[0]] if hk else np.nan
        texts.append(f"{lab}: raw {p_text(w.get('p', np.nan))}, Holm={hp:.3g}" if np.isfinite(hp)
                     else f"{lab}: raw {p_text(w.get('p', np.nan))}, Holm=n/a")
    ax.text(0.5, -0.31, " | ".join(texts), transform=ax.transAxes, ha="center", va="top", fontsize=7, wrap=True)


def plot_condition_profiles(cells: pd.DataFrame, am_cols: list[tuple[float, str]], stats_out: dict[str, Any], area: str, layer_label: str, output_dir: Path) -> None:
    all_cols = ["fade_in_response", "fade_out_response"] + [c for _, c in am_cols]
    all_labels = ["Fade-in", "Fade-out"] + [f"{r:g} Hz" for r, _ in am_cols]
    # Gap between FO and first AM rate; and no connecting line across the gap.
    x = np.r_[0.0, 1.0, np.arange(len(am_cols), dtype=float) + 3.0]

    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    _plot_profile_family(
        ax, cells, all_cols, all_labels, x,
        stats_out["condition_profiles"]["all_cells"],
        f"{area} — {layer_label}\nAll cells: session means + overall mean ± SE",
        break_after_index=1,
    )
    fig.subplots_adjust(bottom=0.34)
    fig.savefig(output_dir / "condition_response_profile_all_cells_MEAN_SEM_ONLY.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)

    # Responsive-only two-panel family.
    fi_cells = analysis_subset(cells, "fi_fo")
    am_cells = analysis_subset(cells, "am")
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.7), squeeze=False)
    _plot_profile_family(
        axes[0, 0], fi_cells,
        ["fade_in_response", "fade_out_response"], ["Fade-in", "Fade-out"], np.array([0.0, 1.0]),
        stats_out["condition_profiles"]["responsive_only"]["fi_or_fo_responsive"],
        "FI-or-FO responsive cells",
    )
    _plot_profile_family(
        axes[0, 1], am_cells,
        [c for _, c in am_cols], [f"{r:g} Hz" for r, _ in am_cols], np.arange(len(am_cols), dtype=float),
        stats_out["condition_profiles"]["responsive_only"]["any_am_rate_responsive"],
        ">=1-AM-rate responsive cells",
    )
    fig.suptitle(f"{area} — {layer_label}\nCondition-specific FDR responsive populations", fontsize=13)
    fig.subplots_adjust(bottom=0.36, top=0.88, wspace=0.30)
    fig.savefig(output_dir / "condition_response_profile_FDR_responsive_only.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def _condition_matrix(df: pd.DataFrame, am_cols: list[tuple[float, str]]) -> tuple[np.ndarray, list[str]]:
    cols = ["fade_in_response", "fade_out_response"] + [c for _, c in am_cols]
    labels = ["Fade-in", "Fade-out"] + [f"{r:g} Hz" for r, _ in am_cols]
    return df[cols].to_numpy(float), labels


def _plot_two_class_raster(cells: pd.DataFrame, am_cols: list[tuple[float, str]], sort_metric: str, title: str, output_path: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10.0, 8.3), squeeze=False)
    im = None
    for row, cls in enumerate(CELL_CLASSES):
        ax = axes[row, 0]
        cdf = cells[cells["cell_class"] == cls].copy()
        if len(cdf) == 0:
            ax.text(0.5, 0.5, "No cells", transform=ax.transAxes, ha="center", va="center")
            ax.axis("off")
            continue
        matrix, labels = _condition_matrix(cdf, am_cols)
        denom = np.nanmax(np.abs(matrix), axis=1)
        good = np.isfinite(denom) & (denom > 0) & np.isfinite(pd.to_numeric(cdf[sort_metric], errors="coerce").to_numpy(float))
        matrix = matrix[good]
        cdf = cdf.iloc[np.flatnonzero(good)].copy()
        if len(cdf) == 0:
            ax.text(0.5, 0.5, "No finite responses", transform=ax.transAxes, ha="center", va="center")
            continue
        norm = matrix / denom[good, None]
        sort_vals = pd.to_numeric(cdf[sort_metric], errors="coerce").to_numpy(float)
        order = np.argsort(sort_vals)[::-1]
        im = ax.imshow(norm[order], aspect="auto", interpolation="nearest", vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(np.arange(len(labels)), labels, rotation=30, ha="right")
        ax.set_ylabel(f"{cls.capitalize()} cells")
        ax.set_title(f"{cls.capitalize()}: n={len(order)}")
    fig.suptitle(title, y=0.995, fontsize=12)
    if im is not None:
        fig.colorbar(im, ax=axes.ravel().tolist(), label="Normalized condition response", shrink=0.75)
    fig.subplots_adjust(left=0.10, right=0.88, bottom=0.12, top=0.90, hspace=0.35)
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_rasters(cells: pd.DataFrame, am_cols: list[tuple[float, str]], area: str, layer_label: str, output_dir: Path) -> None:
    # Main signed FI/FO-sorted raster, all cells.
    _plot_two_class_raster(
        cells, am_cols, "fade_in_vs_fade_out_selectivity",
        f"{area} — {layer_label}\nAll cells sorted descending by bounded signed FI/FO selectivity",
        output_dir / "selectivity_rasters_all_cells.png",
    )

    # Main signed FI/FO-sorted raster, FI-or-FO responsive cells.
    fi = analysis_subset(cells, "fi_fo")
    _plot_two_class_raster(
        fi, am_cols, "fade_in_vs_fade_out_selectivity",
        f"{area} — {layer_label}\nFI-or-FO responsive cells sorted by bounded signed FI/FO selectivity",
        output_dir / "selectivity_rasters_FDR_responsive_only.png",
    )

    # Standalone AM lifetime-sparseness rasters.
    _plot_two_class_raster(
        cells, am_cols, "am_rate_lifetime_sparseness",
        f"{area} — {layer_label}\nAll cells sorted descending by AM-rate lifetime sparseness",
        output_dir / "am_selectivity_raster_all_cells_sorted_by_lifetime_sparseness.png",
    )
    am = analysis_subset(cells, "am")
    _plot_two_class_raster(
        am, am_cols, "am_rate_lifetime_sparseness",
        f"{area} — {layer_label}\nAM-responsive cells sorted descending by AM-rate lifetime sparseness",
        output_dir / "am_selectivity_raster_FDR_responsive_only_sorted_by_lifetime_sparseness.png",
    )


# =============================================================================
# REPORT / MASTER TABLES
# =============================================================================

def make_master_stats_rows(area: str, layer_key: str, stats_out: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    # Responsiveness primary tests.
    for metric, result in stats_out["responsiveness"].items():
        w = result["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
        rows.append({
            "area": area, "layer": layer_key,
            "analysis_family": "responsiveness",
            "subset": "all_cells",
            "metric": metric, "label": result["label"],
            "test": "paired Wilcoxon",
            "n_paired_sessions": w["n_paired_sessions"],
            "statistic": w["W"], "raw_p": w["p"],
            "holm_p": w.get("holm_p_across_7_responsiveness_tests", np.nan),
            "mean_difference_yellow_minus_green": w["mean_difference_yellow_minus_green"],
            "median_difference_yellow_minus_green": w["median_difference_yellow_minus_green"],
            "inference_role": "primary_session_level",
        })

    # Selectivity session primary tests.
    for subset in ["all_cells", "responsive_only"]:
        for metric in ["fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity"]:
            block = stats_out["selectivity"][subset][metric]["session_level_primary_paired"]
            w = block["yellow_vs_green_wilcoxon"]
            rows.append({
                "area": area, "layer": layer_key,
                "analysis_family": "selectivity",
                "subset": subset,
                "metric": metric, "label": SELECTIVITY_SPECS[metric]["label"],
                "test": "paired Wilcoxon",
                "n_paired_sessions": w["n_paired_sessions"],
                "statistic": w["W"], "raw_p": w["p"],
                "holm_p": w.get("holm_p_across_2_primary_selectivity_tests", np.nan),
                "mean_difference_yellow_minus_green": w["mean_difference_yellow_minus_green"],
                "median_difference_yellow_minus_green": w["median_difference_yellow_minus_green"],
                "inference_role": "primary_session_level",
            })

    # Condition profiles, primary session tests.
    for subset_name, fam in [
        ("all_cells", stats_out["condition_profiles"]["all_cells"]),
        ("fi_or_fo_responsive", stats_out["condition_profiles"]["responsive_only"]["fi_or_fo_responsive"]),
        ("any_am_rate_responsive", stats_out["condition_profiles"]["responsive_only"]["any_am_rate_responsive"]),
    ]:
        for metric, block in fam.items():
            w = block["yellow_vs_green_wilcoxon"]
            hk = [k for k in w if k.startswith("holm_p_")]
            hp = w[hk[0]] if hk else np.nan
            rows.append({
                "area": area, "layer": layer_key,
                "analysis_family": "condition_profile",
                "subset": subset_name,
                "metric": metric, "label": block["label"],
                "test": "paired Wilcoxon",
                "n_paired_sessions": w["n_paired_sessions"],
                "statistic": w["W"], "raw_p": w["p"], "holm_p": hp,
                "mean_difference_yellow_minus_green": w["mean_difference_yellow_minus_green"],
                "median_difference_yellow_minus_green": w["median_difference_yellow_minus_green"],
                "inference_role": "primary_session_level",
            })

    # Alternate dF/F session sensitivity tests.
    for alt_key, alt in stats_out["selectivity"]["alternate_dff_sensitivity"].items():
        for subset_name, subkey in [("all_cells", "all_cells"), ("fi_or_fo_responsive", "fi_or_fo_responsive_cells")]:
            w = alt[subkey]["session_level_paired_sensitivity"]["yellow_vs_green_wilcoxon"]
            rows.append({
                "area": area, "layer": layer_key,
                "analysis_family": "alternate_dff_fi_fo_sensitivity",
                "subset": subset_name,
                "metric": alt["metric"], "label": alt["label"],
                "test": "paired Wilcoxon",
                "n_paired_sessions": w["n_paired_sessions"],
                "statistic": w["W"], "raw_p": w["p"], "holm_p": np.nan,
                "mean_difference_yellow_minus_green": w["mean_difference_yellow_minus_green"],
                "median_difference_yellow_minus_green": w["median_difference_yellow_minus_green"],
                "inference_role": "sensitivity_not_in_primary_holm_family",
            })
    return rows


def write_report(path: Path, subject: str, dates: list[str], area: str, layer_key: str,
                 cells: pd.DataFrame, stats_out: dict[str, Any]) -> None:
    _, _, layer_label = LAYERS[layer_key]
    lines = [
        "GREEN-vs-YELLOW SOUND-TUNING ANALYSIS WITHIN AREA x LAYER — v12 INPUT",
        "=" * 86,
        f"Subject: {subject}",
        f"Dates: {', '.join(dates)}",
        f"Area: {area}",
        f"Layer: {layer_label}",
        "",
        "PRIMARY INFERENCE",
        "-----------------",
        "Sessions are biological replicates. GREEN and YELLOW session summaries are paired.",
        "Primary tests: two-sided paired Wilcoxon signed-rank; difference sign = YELLOW - GREEN.",
        "Pooled-cell Mann-Whitney/Fisher tests are exploratory/descriptive only.",
        "",
        "RESPONSIVENESS",
        "--------------",
    ]
    for metric, result in stats_out["responsiveness"].items():
        w = result["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
        hp = w.get("holm_p_across_7_responsiveness_tests", np.nan)
        lines.append(
            f"{result['label']}: W={w['W']:.4g}, raw {p_text(w['p'])}, "
            f"Holm p={hp:.4g}, n_pairs={w['n_paired_sessions']}" if np.isfinite(hp)
            else f"{result['label']}: W={w['W']:.4g}, raw {p_text(w['p'])}, Holm p=n/a, n_pairs={w['n_paired_sessions']}"
        )

    lines += ["", "SELECTIVITY", "-----------"]
    for subset in ["all_cells", "responsive_only"]:
        lines.append(f"Subset: {subset}")
        for metric in PRIMARY_SELECTIVITY_METRICS:
            block = stats_out["selectivity"][subset][metric]
            mw = block["pooled_cell_exploratory"]["yellow_vs_green_mannwhitney"]
            lines.append(f"  {SELECTIVITY_SPECS[metric]['label']}: exploratory pooled U={mw['U']:.4g}, {p_text(mw['p'])}")
            if "session_level_primary_paired" in block:
                w = block["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
                hp = w.get("holm_p_across_2_primary_selectivity_tests", np.nan)
                lines.append(
                    f"    session paired: W={w['W']:.4g}, raw {p_text(w['p'])}, "
                    f"Holm p={hp:.4g}, n_pairs={w['n_paired_sessions']}" if np.isfinite(hp)
                    else f"    session paired: W={w['W']:.4g}, raw {p_text(w['p'])}, Holm p=n/a, n_pairs={w['n_paired_sessions']}"
                )

    lines += ["", "ALTERNATE dF/F FI/FO SENSITIVITY", "-------------------------------"]
    for alt_key, alt in stats_out["selectivity"]["alternate_dff_sensitivity"].items():
        lines.append(f"{alt['label']} ({alt['metric']})")
        lines.append("  Not included in primary Holm family.")
        for subset_name, subkey in [("all_cells", "all_cells"), ("FI-or-FO responsive", "fi_or_fo_responsive_cells")]:
            w = alt[subkey]["session_level_paired_sensitivity"]["yellow_vs_green_wilcoxon"]
            lines.append(f"  {subset_name}: W={w['W']:.4g}, {p_text(w['p'])}, n_pairs={w['n_paired_sessions']}")

    lines += ["", "REMOVED FROM FORMAL STATISTICS", "------------------------------",
              "looming_score, mean all-sound response, standalone raw FI response, standalone raw FO response,",
              "mean AM response across rates, and standalone best-AM response.", ""]
    path.write_text("\n".join(lines) + "\n")


def write_figure_index(output_dir: Path) -> None:
    pngs = sorted(output_dir.glob("*.png"))
    lines = ["FIGURE INDEX", "============", ""] + [p.name for p in pngs]
    (output_dir / "FIGURE_INDEX.txt").write_text("\n".join(lines) + "\n")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args = parse_args()
    subject = str(args.subject)
    dates = [str(d) for d in args.dates]
    areas = list(args.areas)

    in_paths = {area: expected_area_csv(subject, area, dates) for area in areas}
    out_root = output_root(subject, dates)

    print("=" * 86)
    print("SOUND_TUNING AREA x LAYER GREEN-vs-YELLOW ANALYSIS — v12 INPUT")
    print("=" * 86)
    print(f"Subject: {subject}")
    print(f"Dates:   {', '.join(dates)}")
    print(f"Areas:   {', '.join(areas)}")
    print("Layers:  L2/3 = 100 <= depth < 300 um; L4/5 = 300 <= depth <= 600 um")
    print(f"Output root: {out_root}")
    print("\nExpected v12 inputs:")
    for area, path in in_paths.items():
        print(f"  {area}: {path} {'[FOUND]' if path.exists() else '[MISSING]'}")

    if args.dry_run:
        print("\nDry run complete; no tables were loaded.")
        return

    out_root.mkdir(parents=True, exist_ok=True)
    all_cells = load_area_tables(subject, dates, areas)
    all_cells.to_csv(out_root / "all_areas_combined_cell_results.csv", index=False)

    am_cols = _am_primary_columns(all_cells)
    manifest = {
        "script": "sound_tuning_area_layer_green_yellow_analysis_v3.py",
        "prerequisite": "sound_tuning_area_analysis_v12.py",
        "subject": subject, "dates": dates, "areas": areas,
        "input_files": {a: str(p) for a, p in in_paths.items()},
        "output_root": str(out_root),
        "layers": {k: v[2] for k, v in LAYERS.items()},
        "primary_inference": "paired session-level GREEN-vs-YELLOW two-sided Wilcoxon signed-rank tests",
        "difference_sign": "YELLOW - GREEN",
        "pooled_cell_inference": "exploratory/descriptive only",
        "fi_fo_selectivity": "(FI-FO)/(|FI|+|FO|), NaN when denominator is zero",
        "responsive_only_rules": {
            "FI_FO": "fi_or_fo_responsive_fdr",
            "FI_bestAM": "fade_in_responsive_fdr OR any_am_rate_responsive_fdr",
            "AM_lifetime_sparseness": "any_am_rate_responsive_fdr",
        },
        "alternate_dff": {
            "session_median_dff": ALT_FI_FO["session_median_dff"]["metric"],
            "60s_prestim_median_dff": ALT_FI_FO["60s_prestim_median_dff"]["metric"],
            "responsiveness_recomputed": False,
            "role": "sensitivity analyses outside primary Holm family",
        },
        "am_rates_hz": [r for r, _ in am_cols],
    }
    save_json(out_root / "run_manifest.json", manifest)

    master_rows: list[dict[str, Any]] = []
    print("\nLoaded data:")
    for area in areas:
        adf = all_cells[all_cells["canonicalArea"] == area]
        print(f"  {area}: {len(adf)} cells, {adf['session_key'].nunique()} sessions")

    for area in areas:
        area_cells = all_cells[all_cells["canonicalArea"] == area].copy()
        area_am_cols = _am_primary_columns(area_cells)
        for layer_key, (_, _, layer_label) in LAYERS.items():
            cells = subset_layer(area_cells, layer_key)
            out_dir = out_root / area / layer_key
            out_dir.mkdir(parents=True, exist_ok=True)

            print("\n" + "-" * 86)
            print(f"{area} — {layer_label}")
            for cls in CELL_CLASSES:
                cdf = cells[cells["cell_class"] == cls]
                print(f"  {cls.upper():6s}: {len(cdf)} cells, {cdf['session_key'].nunique()} sessions")

            # General cell/session CSVs retained for downstream inspection.
            cells.to_csv(out_dir / "cell_results.csv", index=False)
            numeric_for_session = [
                "fade_in_response", "fade_out_response",
                "fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity",
                "am_rate_lifetime_sparseness",
                ALT_FI_FO["session_median_dff"]["metric"],
                ALT_FI_FO["60s_prestim_median_dff"]["metric"],
            ] + [c for _, c in area_am_cols]
            session_df = aggregate_sessions(cells, numeric_for_session)
            session_df.to_csv(out_dir / "session_summary.csv", index=False)

            stats_out = run_statistics(cells, area_am_cols)
            save_json(out_dir / "statistics.json", stats_out)
            write_report(out_dir / "REPORT.txt", subject, dates, area, layer_key, cells, stats_out)
            master_rows.extend(make_master_stats_rows(area, layer_key, stats_out))

            plot_responsiveness(cells, stats_out, area, layer_label, out_dir)
            plot_selectivity_outputs(cells, stats_out, area, layer_label, out_dir)
            plot_condition_profiles(cells, area_am_cols, stats_out, area, layer_label, out_dir)
            plot_rasters(cells, area_am_cols, area, layer_label, out_dir)
            write_figure_index(out_dir)
            print(f"  -> {out_dir}")

    master_df = pd.DataFrame(master_rows)
    master_df.to_csv(out_root / "MASTER_STATISTICS.csv", index=False)
    if len(master_df):
        quick_cols = [
            "area", "layer", "analysis_family", "subset", "metric", "label", "test",
            "n_paired_sessions", "statistic", "raw_p", "holm_p",
            "mean_difference_yellow_minus_green", "median_difference_yellow_minus_green",
            "inference_role",
        ]
        master_df[quick_cols].sort_values(
            ["analysis_family", "subset", "holm_p", "raw_p"], na_position="last"
        ).to_csv(out_root / "PAIRED_GREEN_YELLOW_RESULTS_QUICKVIEW.csv", index=False)

    print("\n" + "=" * 86)
    print("DONE")
    print(f"Outputs saved under: {out_root}")
    print("Primary inference uses paired sessions; pooled-cell tests are exploratory.")
    print("=" * 86)


if __name__ == "__main__":
    main()
