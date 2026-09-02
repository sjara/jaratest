#!/usr/bin/env python3
"""
Compare YELLOW versus GREEN sound-tuning responses within each AREA x LAYER stratum.

This is a follow-up analysis for sound_tuning_area_analysis_v5.py. It does NOT
rerun Suite2p, Cellpose, or event alignment. Instead, it loads the already-saved
combined_cell_results.csv files for A1, AAF, and A2 and asks questions such as:

    Within A2 L2/3, do YELLOW cells have a larger |fade-in| / |fade-out|
    response ratio than GREEN cells?

The same GREEN-vs-YELLOW comparisons are run independently for each of six
AREA x LAYER combinations:

    A1  x L2/3   100 <= depth < 300 um
    A1  x L4/5   300 <= depth <= 600 um
    AAF x L2/3   100 <= depth < 300 um
    AAF x L4/5   300 <= depth <= 600 um
    A2  x L2/3   100 <= depth < 300 um
    A2  x L4/5   300 <= depth <= 600 um

The 300-um boundary is assigned to L4/5 so no session is counted twice.

IMPORTANT STATISTICAL CONVENTION
--------------------------------
Primary inference is SESSION-LEVEL and PAIRED: within a given area/layer,
YELLOW and GREEN cells are recorded in the same imaging sessions. Each session
therefore contributes one YELLOW summary and one GREEN summary, and the primary
continuous/binary comparisons use paired Wilcoxon signed-rank tests on sessions
that contain both classes. Pooled-cell tests are also saved, but are explicitly
labeled exploratory because cells within a session are not independent
biological replicates.

For continuous response metrics, session summaries use the same aggregation as
sound_tuning_cross_area_cellclass_analysis.py:
    mean   for dF/F-like response metrics
    median for absolute response ratios

Inputs and outputs are resolved from jaratoolbox.settings.TEMP_OUTPUT_PATH.
There is no path prompt and no save flag.

Expected prerequisite output for each area:
    <TEMP_OUTPUT_PATH>/evan/sound_tuning_area_analysis/<subject>/<area>/<dates>/
        combined/combined_cell_results.csv

Example
-------
python sound_tuning_area_layer_green_yellow_analysis.py imag039 \
    --dates 20260717 20260729 20260730

Optional dry run:
python sound_tuning_area_layer_green_yellow_analysis.py imag039 \
    --dates 20260717 20260729 20260730 --dry-run
"""

from __future__ import annotations

import argparse
import json
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
CELL_CLASS_COLORS = {
    "green": "limegreen",
    "yellow": "goldenrod",
}

LAYERS = {
    "L23_100to300um": (100.0, 300.0, "L2/3 (100-<300 um)"),
    "L45_300to600um": (300.0, 600.0, "L4/5 (300-600 um)"),
}

DPI = 180

CONTINUOUS_METRICS = {
    "mean_sound_response": {
        "label": "Mean all-sound response (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "fade_in_response": {
        "label": "Fade-in response (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "fade_out_response": {
        "label": "Fade-out response (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "mean_am_response_across_rates": {
        "label": "Mean AM response across rates (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "best_am_response": {
        "label": "Best-AM response (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "fade_in_over_fade_out_abs_ratio": {
        "label": "|Fade-in| / |Fade-out|",
        "session_agg": "median",
        "reference": 1.0,
    },
    "fade_in_over_best_am_abs_ratio": {
        "label": "|Fade-in| / |Best AM|",
        "session_agg": "median",
        "reference": 1.0,
    },
    "looming_score": {
        "label": "Looming score (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
}

BINARY_METRICS = {
    "sound_responsive_fdr": {
        "label": "FDR sound-responsive cells (%)",
        "session_col": "pct_sound_responsive_fdr",
    },
    "sound_excited_fdr": {
        "label": "FDR excited cells (%)",
        "session_col": "pct_sound_excited_fdr",
    },
    "sound_suppressed_fdr": {
        "label": "FDR suppressed cells (%)",
        "session_col": "pct_sound_suppressed_fdr",
    },
}


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
        "--dates",
        nargs="+",
        required=True,
        help="Dates used for the v5 area analyses, e.g. 20260717 20260729 20260730.",
    )
    parser.add_argument(
        "--areas",
        nargs="+",
        default=list(AREAS),
        choices=list(AREAS),
        help="Areas to analyze. Default: A1 AAF A2.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print expected input/output paths and stop before loading tables.",
    )
    return parser.parse_args()


def date_tag(dates: Iterable[str]) -> str:
    return "_".join(str(d) for d in dates)


def expected_area_csv(subject: str, area: str, dates: list[str]) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH)
        / "evan"
        / "sound_tuning_area_analysis"
        / subject
        / area
        / date_tag(dates)
        / "combined"
        / "combined_cell_results.csv"
    )


def output_root(subject: str, dates: list[str]) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH)
        / "evan"
        / "sound_tuning_area_layer_green_yellow_analysis"
        / subject
        / date_tag(dates)
    )


# =============================================================================
# GENERAL UTILITIES
# =============================================================================

def json_default(obj: Any) -> Any:
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
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
        float(np.median(vals)),
        float(np.percentile(vals, 25)),
        float(np.percentile(vals, 75)),
        len(vals),
    )


def cliffs_delta(x: Iterable[Any], y: Iterable[Any]) -> float:
    """Positive means x tends to be larger than y."""
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return np.nan
    ranks = stats.rankdata(np.concatenate([x, y]))
    rx = np.sum(ranks[: len(x)])
    u = rx - len(x) * (len(x) + 1) / 2
    return float((2 * u) / (len(x) * len(y)) - 1)


def safe_mannwhitney(x: Iterable[Any], y: Iterable[Any]) -> dict[str, Any]:
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return {
            "n1": len(x), "n2": len(y), "U": np.nan, "p": np.nan,
            "cliffs_delta": np.nan,
        }
    try:
        res = stats.mannwhitneyu(x, y, alternative="two-sided")
        return {
            "n1": len(x), "n2": len(y),
            "U": float(res.statistic), "p": float(res.pvalue),
            "cliffs_delta": cliffs_delta(x, y),
        }
    except Exception:
        return {
            "n1": len(x), "n2": len(y), "U": np.nan, "p": np.nan,
            "cliffs_delta": np.nan,
        }


def safe_wilcoxon_pairs(yellow: Iterable[Any], green: Iterable[Any]) -> dict[str, Any]:
    """Paired Wilcoxon. Difference sign is YELLOW - GREEN."""
    y = pd.to_numeric(pd.Series(yellow), errors="coerce").to_numpy(dtype=float)
    g = pd.to_numeric(pd.Series(green), errors="coerce").to_numpy(dtype=float)
    valid = np.isfinite(y) & np.isfinite(g)
    y = y[valid]
    g = g[valid]
    diff = y - g
    n = len(diff)

    if n == 0:
        return {
            "n_paired_sessions": 0, "W": np.nan, "p": np.nan,
            "mean_difference_yellow_minus_green": np.nan,
            "sem_difference": np.nan,
            "median_difference_yellow_minus_green": np.nan,
            "q1_difference": np.nan,
            "q3_difference": np.nan,
        }

    md = float(np.mean(diff))
    sed = float(stats.sem(diff)) if n > 1 else np.nan
    med = float(np.median(diff))
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
        "n_paired_sessions": n,
        "W": W,
        "p": p,
        "mean_difference_yellow_minus_green": md,
        "sem_difference": sed,
        "median_difference_yellow_minus_green": med,
        "q1_difference": float(q1),
        "q3_difference": float(q3),
    }


def fisher_green_yellow(df: pd.DataFrame, binary_col: str) -> dict[str, Any]:
    out = {}
    counts = {}
    for cls in CELL_CLASSES:
        cdf = df[df["cell_class"] == cls]
        n = len(cdf)
        positive = int(cdf[binary_col].astype(bool).sum()) if n else 0
        counts[cls] = (positive, n)
        out[cls] = {
            "n_cells": n,
            "positive": positive,
            "percent": 100.0 * positive / n if n else np.nan,
        }
    yg, ng = counts["yellow"]
    gg, n_green = counts["green"]
    if ng == 0 or n_green == 0:
        odds, p = np.nan, np.nan
    else:
        odds, p = stats.fisher_exact([[yg, ng-yg], [gg, n_green-gg]])
    out["yellow_vs_green_fisher"] = {
        "odds_ratio": float(odds) if np.isfinite(odds) else np.nan,
        "p": float(p) if np.isfinite(p) else np.nan,
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

def load_area_tables(subject: str, dates: list[str], areas: list[str]) -> pd.DataFrame:
    frames = []
    missing = []
    for area in areas:
        path = expected_area_csv(subject, area, dates)
        if not path.exists():
            missing.append(path)
            continue
        df = pd.read_csv(path)
        if "canonicalArea" not in df.columns:
            raise ValueError(f"{path} has no canonicalArea column; expected a v5 output table.")
        bad = set(df["canonicalArea"].dropna().astype(str).unique()) - {area}
        if bad:
            raise ValueError(f"{path} contains unexpected canonicalArea values: {sorted(bad)}")
        frames.append(df)

    if missing:
        msg = "Missing prerequisite v5 output(s):\n" + "\n".join(f"  {p}" for p in missing)
        msg += "\nRun sound_tuning_area_analysis_v5.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)
    if not frames:
        raise RuntimeError("No area tables were loaded.")

    df = pd.concat(frames, ignore_index=True, sort=False)
    required = {
        "subject", "date", "session", "session_key", "canonicalArea", "brainArea",
        "depth", "cell_class", "sound_responsive_fdr", "sound_excited_fdr",
        "sound_suppressed_fdr", "fade_in_response", "fade_out_response",
        "mean_am_response_across_rates", "best_am_response",
        "fade_in_over_fade_out_abs_ratio", "fade_in_over_best_am_abs_ratio",
        "looming_score", "mean_sound_response",
    }
    missing_cols = sorted(required - set(df.columns))
    if missing_cols:
        raise ValueError("Combined cell table(s) are missing required columns: " + ", ".join(missing_cols))

    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")
    for col in BINARY_METRICS:
        if df[col].dtype != bool:
            df[col] = df[col].astype(str).str.lower().isin(["true", "1", "yes"])
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


# =============================================================================
# SESSION SUMMARIES / STATS
# =============================================================================

def aggregate_sessions(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_cols = [
        "subject", "date", "session", "session_key", "canonicalArea",
        "brainArea", "depth", "cell_class",
    ]
    am_cols = sorted(c for c in df.columns if c.startswith("am_response_") and c.endswith("Hz"))

    for keys, sdf in df.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        row["n_cells"] = int(len(sdf))
        row["n_sound_responsive_fdr"] = int(sdf["sound_responsive_fdr"].astype(bool).sum())
        row["pct_sound_responsive_fdr"] = 100.0 * float(sdf["sound_responsive_fdr"].astype(bool).mean()) if len(sdf) else np.nan
        row["pct_sound_excited_fdr"] = 100.0 * float(sdf["sound_excited_fdr"].astype(bool).mean()) if len(sdf) else np.nan
        row["pct_sound_suppressed_fdr"] = 100.0 * float(sdf["sound_suppressed_fdr"].astype(bool).mean()) if len(sdf) else np.nan

        for metric, cfg in CONTINUOUS_METRICS.items():
            vals = finite_values(sdf[metric])
            if len(vals) == 0:
                row[metric] = np.nan
            elif cfg["session_agg"] == "median":
                row[metric] = float(np.median(vals))
            else:
                row[metric] = float(np.mean(vals))

        for col in am_cols:
            vals = finite_values(sdf[col])
            row[col] = float(np.mean(vals)) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def paired_session_vectors(session_df: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    piv = session_df.pivot_table(
        index="session_key",
        columns="cell_class",
        values=metric,
        aggfunc="first",
    )
    if "yellow" not in piv.columns:
        piv["yellow"] = np.nan
    if "green" not in piv.columns:
        piv["green"] = np.nan
    piv = piv[["yellow", "green"]].copy()
    valid = np.isfinite(pd.to_numeric(piv["yellow"], errors="coerce")) & np.isfinite(pd.to_numeric(piv["green"], errors="coerce"))
    paired = piv.loc[valid].copy()
    return (
        paired,
        paired["yellow"].to_numpy(dtype=float),
        paired["green"].to_numpy(dtype=float),
    )


def analyze_continuous_metric(cell_df: pd.DataFrame, session_df: pd.DataFrame, metric: str) -> dict[str, Any]:
    pooled = {}
    for cls in CELL_CLASSES:
        vals = cell_df.loc[cell_df["cell_class"] == cls, metric]
        mean, sem, n = mean_sem(vals)
        med, q1, q3, _ = median_iqr(vals)
        pooled[cls] = {
            "n_cells": n,
            "mean": mean,
            "sem": sem,
            "median": med,
            "q1": q1,
            "q3": q3,
        }

    pooled_test = safe_mannwhitney(
        cell_df.loc[cell_df["cell_class"] == "yellow", metric],
        cell_df.loc[cell_df["cell_class"] == "green", metric],
    )

    sess_summary = {}
    for cls in CELL_CLASSES:
        vals = session_df.loc[session_df["cell_class"] == cls, metric]
        mean, sem, n = mean_sem(vals)
        med, q1, q3, _ = median_iqr(vals)
        sess_summary[cls] = {
            "n_sessions": n,
            "mean": mean,
            "sem": sem,
            "median": med,
            "q1": q1,
            "q3": q3,
        }

    paired_df, y, g = paired_session_vectors(session_df, metric)
    paired_test = safe_wilcoxon_pairs(y, g)
    paired_test["paired_session_keys"] = paired_df.index.astype(str).tolist()

    return {
        "label": CONTINUOUS_METRICS[metric]["label"],
        "session_aggregation": CONTINUOUS_METRICS[metric]["session_agg"],
        "pooled_cell_exploratory": {
            "summary": pooled,
            "yellow_vs_green_mannwhitney": pooled_test,
        },
        "session_level_primary_paired": {
            "summary": sess_summary,
            "yellow_vs_green_wilcoxon": paired_test,
        },
    }


def analyze_binary_metric(cell_df: pd.DataFrame, session_df: pd.DataFrame, metric: str) -> dict[str, Any]:
    pct_col = BINARY_METRICS[metric]["session_col"]
    pooled = fisher_green_yellow(cell_df, metric)

    sess_summary = {}
    for cls in CELL_CLASSES:
        vals = session_df.loc[session_df["cell_class"] == cls, pct_col]
        mean, sem, n = mean_sem(vals)
        sess_summary[cls] = {
            "n_sessions": n,
            "mean_percent": mean,
            "sem_percent": sem,
        }

    paired_df, y, g = paired_session_vectors(session_df, pct_col)
    paired_test = safe_wilcoxon_pairs(y, g)
    paired_test["paired_session_keys"] = paired_df.index.astype(str).tolist()

    return {
        "label": BINARY_METRICS[metric]["label"],
        "pooled_cell_exploratory": pooled,
        "session_level_primary_paired": {
            "summary": sess_summary,
            "yellow_vs_green_wilcoxon": paired_test,
        },
    }


def run_statistics(cell_df: pd.DataFrame, session_df: pd.DataFrame) -> dict[str, Any]:
    out = {"continuous": {}, "binary": {}}
    for metric in CONTINUOUS_METRICS:
        if metric in cell_df.columns:
            out["continuous"][metric] = analyze_continuous_metric(cell_df, session_df, metric)
    for metric in BINARY_METRICS:
        if metric in cell_df.columns:
            out["binary"][metric] = analyze_binary_metric(cell_df, session_df, metric)
    return out


# =============================================================================
# PLOTTING HELPERS
# =============================================================================

def optimized_ylim_from_summary(
    means: np.ndarray,
    errors: np.ndarray | None = None,
    reference_values: list[float] | None = None,
    pad_fraction: float = 0.18,
) -> tuple[float, float] | None:
    means = np.asarray(means, dtype=float)
    finite = np.isfinite(means)
    if not np.any(finite):
        return None
    vals = list(means[finite])
    if errors is not None:
        errors = np.asarray(errors, dtype=float)
        for m, e in zip(means, errors):
            if np.isfinite(m) and np.isfinite(e):
                vals.extend([m-e, m+e])
    if reference_values:
        vals.extend([x for x in reference_values if np.isfinite(x)])
    lo = float(np.min(vals))
    hi = float(np.max(vals))
    span = hi - lo
    if not np.isfinite(span) or span == 0:
        span = max(abs(lo), abs(hi), 1.0) * 0.25
    return lo - pad_fraction * span, hi + pad_fraction * span


def robust_cell_ylim(values: Iterable[Any], reference: float | None = None) -> tuple[float, float, int] | None:
    vals = finite_values(values)
    if len(vals) == 0:
        return None
    if len(vals) < 4:
        lo, hi = float(np.min(vals)), float(np.max(vals))
    else:
        q1, q3 = np.percentile(vals, [25, 75])
        iqr = q3-q1
        if np.isfinite(iqr) and iqr > 0:
            inliers = vals[(vals >= q1-3*iqr) & (vals <= q3+3*iqr)]
            if len(inliers):
                lo, hi = float(np.min(inliers)), float(np.max(inliers))
            else:
                lo, hi = float(np.min(vals)), float(np.max(vals))
        else:
            lo, hi = float(np.min(vals)), float(np.max(vals))
    if reference is not None and np.isfinite(reference):
        lo, hi = min(lo, reference), max(hi, reference)
    span = hi-lo if hi > lo else max(abs(lo), abs(hi), 1.0)*0.25
    y0, y1 = lo-0.08*span, hi+0.14*span
    nclip = int(np.sum((vals < y0) | (vals > y1)))
    return y0, y1, nclip


def condition_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    am_cols = [c for c in df.columns if c.startswith("am_response_") and c.endswith("Hz")]
    def rate(c: str) -> float:
        try:
            return float(c[len("am_response_"):-2])
        except Exception:
            return np.inf
    am_cols = sorted(am_cols, key=rate)
    cols = ["fade_in_response", "fade_out_response"] + am_cols
    labels = ["Fade-in", "Fade-out"] + [c[len("am_response_"):] for c in am_cols]
    return cols, labels


def plot_metric_grid(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    area: str,
    layer_label: str,
    output_path: Path,
    mode: str,
    subset_label: str,
) -> None:
    metrics = list(CONTINUOUS_METRICS.keys())
    fig, axes = plt.subplots(2, 4, figsize=(19, 9.5))
    axes = axes.ravel()
    rng = np.random.default_rng(0)
    x = np.array([0, 1], dtype=float)
    xlabels = ["Green", "Yellow"]

    for ax, metric in zip(axes, metrics):
        cfg = CONTINUOUS_METRICS[metric]
        ref = cfg["reference"]
        source = session_df if mode in ("session_paired", "session_mean") else cell_df

        means, sems, ns = [], [], []
        for xi, cls in zip(x, CELL_CLASSES):
            vals = finite_values(source.loc[source["cell_class"] == cls, metric])
            m, se, n = mean_sem(vals)
            means.append(m); sems.append(se); ns.append(n)
            if mode == "with_cells" and len(vals):
                jitter = rng.normal(0, 0.055, len(vals))
                ax.scatter(np.full(len(vals), xi)+jitter, vals, s=10, alpha=0.22,
                           color=CELL_CLASS_COLORS[cls], edgecolors="none")
            if np.isfinite(m):
                ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None,
                            fmt="o", ms=7, capsize=4, lw=1.8,
                            color=CELL_CLASS_COLORS[cls])

        if mode == "session_paired":
            piv = source.pivot_table(index="session_key", columns="cell_class", values=metric, aggfunc="first")
            if {"green", "yellow"}.issubset(piv.columns):
                for _, row in piv[["green", "yellow"]].dropna().iterrows():
                    ax.plot(x, [row["green"], row["yellow"]], color="0.55", alpha=0.45, lw=0.8, zorder=0)
                    ax.scatter(x, [row["green"], row["yellow"]], s=15,
                               color=[CELL_CLASS_COLORS["green"], CELL_CLASS_COLORS["yellow"]],
                               alpha=0.75, zorder=1)

        means = np.asarray(means, float)
        sems = np.asarray(sems, float)
        if ref is not None:
            ax.axhline(ref, ls="--", lw=0.9, color="0.45")

        if mode in ("mean_only", "session_mean"):
            ylim = optimized_ylim_from_summary(means, sems, [ref] if ref is not None else None)
            if ylim:
                ax.set_ylim(*ylim)
            ytop = ax.get_ylim()[1] - 0.03*(ax.get_ylim()[1]-ax.get_ylim()[0])
            for xi, cls, m, se, n in zip(x, CELL_CLASSES, means, sems, ns):
                if not np.isfinite(m):
                    continue
                se_txt = f"{se:.4g}" if np.isfinite(se) else "n/a"
                ax.text(xi, ytop, f"{m:.4g} ± {se_txt}\nn={n}", ha="center", va="top",
                        fontsize=8, color=CELL_CLASS_COLORS[cls])
        elif mode == "with_cells":
            ylim = robust_cell_ylim(source[metric], ref)
            if ylim:
                y0, y1, nclip = ylim
                ax.set_ylim(y0, y1)
                if nclip:
                    ax.text(0.99, 0.01, f"display clips {nclip} extreme cell(s)",
                            transform=ax.transAxes, ha="right", va="bottom", fontsize=7, color="0.35")

        ax.set_xticks(x, xlabels)
        ax.set_title(cfg["label"], fontsize=10)
        ax.grid(axis="y", alpha=0.22)

    mode_title = {
        "with_cells": "cell distributions + mean ± SEM",
        "mean_only": "cell mean ± SEM; individual cells not shown",
        "session_paired": "paired session summaries; lines connect same session",
        "session_mean": "SESSION mean ± SEM; one class summary per session",
    }[mode]
    fig.suptitle(
        f"{area} — {layer_label}\n{subset_label}: GREEN vs YELLOW — {mode_title}",
        fontsize=14,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_condition_profile(
    cell_df: pd.DataFrame,
    area: str,
    layer_label: str,
    output_dir: Path,
    suffix: str,
) -> None:
    cols, labels = condition_columns(cell_df)
    if not cols:
        return
    fig, ax = plt.subplots(figsize=(9, 5.8))
    x = np.arange(len(cols))
    all_means, all_sems = [], []
    text_lines = []
    for cls in CELL_CLASSES:
        means, sems, ns = [], [], []
        cdf = cell_df[cell_df["cell_class"] == cls]
        for col in cols:
            m, se, n = mean_sem(cdf[col])
            means.append(m); sems.append(se); ns.append(n)
        all_means.extend(means); all_sems.extend(sems)
        ax.errorbar(x, means, yerr=sems, marker="o", capsize=4, lw=2,
                    color=CELL_CLASS_COLORS[cls], label=cls.capitalize())
        pieces = []
        for lab, m, se, n in zip(labels, means, sems, ns):
            if np.isfinite(m):
                pieces.append(f"{lab} {m:.3g}±{se:.2g} (n={n})" if np.isfinite(se)
                              else f"{lab} {m:.3g} (n={n})")
        text_lines.append(cls.capitalize() + ": " + "; ".join(pieces))

    ylim = optimized_ylim_from_summary(np.asarray(all_means), np.asarray(all_sems), [0.0])
    if ylim:
        ax.set_ylim(*ylim)
    ax.axhline(0, ls="--", lw=1, color="0.45")
    ax.set_xticks(x, labels, rotation=30, ha="right")
    ax.set_ylabel("Response (dF/F)")
    ax.set_title(f"{area} — {layer_label}\nGREEN vs YELLOW — {suffix.replace('_',' ')}: mean ± SEM")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    ax.text(0.01, 0.01, "\n".join(text_lines), transform=ax.transAxes,
            ha="left", va="bottom", fontsize=6.8,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.72, edgecolor="0.8"))
    fig.tight_layout()
    fig.savefig(output_dir / f"condition_response_profile_{suffix}_MEAN_SEM_ONLY.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_selectivity_rasters(
    cell_df: pd.DataFrame,
    area: str,
    layer_label: str,
    output_dir: Path,
    suffix: str,
) -> None:
    cols, labels = condition_columns(cell_df)
    if len(cols) < 2:
        return
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 7.5), squeeze=False)
    im = None
    for row, cls in enumerate(CELL_CLASSES):
        ax = axes[row, 0]
        cdf = cell_df[cell_df["cell_class"] == cls].copy()
        if len(cdf) == 0:
            ax.text(0.5, 0.5, "No cells", transform=ax.transAxes, ha="center", va="center")
            ax.set_axis_off()
            continue
        matrix = cdf[cols].to_numpy(dtype=float)
        denom = np.nanmax(np.abs(matrix), axis=1)
        good = np.isfinite(denom) & (denom > 0)
        matrix = matrix[good]
        cdf = cdf.iloc[np.where(good)[0]].copy()
        if len(matrix) == 0:
            ax.text(0.5, 0.5, "No finite responses", transform=ax.transAxes, ha="center", va="center")
            continue
        norm = matrix / denom[good, None]
        order = np.argsort(cdf["looming_score"].to_numpy(dtype=float))[::-1]
        norm = norm[order]
        im = ax.imshow(norm, aspect="auto", interpolation="nearest", vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(np.arange(len(labels)), labels, rotation=30, ha="right")
        ax.set_ylabel(f"{cls.capitalize()} cells")
        ax.set_title(f"{cls.capitalize()}: n={len(norm)} | sorted by looming score")
    fig.suptitle(f"{area} — {layer_label}\nGREEN vs YELLOW selectivity — {suffix.replace('_',' ')}", y=1.01)
    if im is not None:
        fig.colorbar(im, ax=axes.ravel().tolist(), label="Normalized condition response", shrink=0.75)
    fig.tight_layout()
    fig.savefig(output_dir / f"selectivity_rasters_{suffix}.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_responsiveness(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    area: str,
    layer_label: str,
    output_dir: Path,
) -> None:
    metrics = [
        ("sound_responsive_fdr", "pct_sound_responsive_fdr", "Responsive"),
        ("sound_excited_fdr", "pct_sound_excited_fdr", "Excited"),
        ("sound_suppressed_fdr", "pct_sound_suppressed_fdr", "Suppressed"),
    ]

    # Pooled cell percentages.
    fig, ax = plt.subplots(figsize=(8, 5.6))
    x = np.arange(len(metrics), dtype=float)
    offsets = {"green": -0.16, "yellow": 0.16}
    for cls in CELL_CLASSES:
        vals = []
        for cell_col, _, _ in metrics:
            cdf = cell_df[cell_df["cell_class"] == cls]
            vals.append(100.0 * float(cdf[cell_col].astype(bool).mean()) if len(cdf) else np.nan)
        ax.scatter(x + offsets[cls], vals, s=75, color=CELL_CLASS_COLORS[cls], label=cls.capitalize(), zorder=3)
        for xx, v in zip(x + offsets[cls], vals):
            if np.isfinite(v):
                ax.text(xx, v, f"{v:.1f}%", ha="center", va="bottom", fontsize=8,
                        color=CELL_CLASS_COLORS[cls])
    ax.set_xticks(x, [m[2] for m in metrics])
    ax.set_ylabel("Pooled cell percentage (%)")
    ax.set_title(f"{area} — {layer_label}\nGREEN vs YELLOW FDR responsiveness")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "responsiveness_pooled_cell_percentages.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)

    # Session paired percentages.
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.8))
    for ax, (_, session_col, label) in zip(axes, metrics):
        piv = session_df.pivot_table(index="session_key", columns="cell_class", values=session_col, aggfunc="first")
        if {"green", "yellow"}.issubset(piv.columns):
            paired = piv[["green", "yellow"]].dropna()
        else:
            paired = pd.DataFrame(columns=["green", "yellow"])
        for _, row in paired.iterrows():
            ax.plot([0, 1], [row["green"], row["yellow"]], color="0.55", alpha=0.5, lw=0.9)
            ax.scatter([0, 1], [row["green"], row["yellow"]], s=24,
                       color=[CELL_CLASS_COLORS["green"], CELL_CLASS_COLORS["yellow"]], zorder=3)
        means, sems, ns = [], [], []
        for cls in CELL_CLASSES:
            m, se, n = mean_sem(session_df.loc[session_df["cell_class"] == cls, session_col])
            means.append(m); sems.append(se); ns.append(n)
            if np.isfinite(m):
                ax.errorbar(CELL_CLASSES.index(cls), m, yerr=se if np.isfinite(se) else None,
                            fmt="o", ms=8, capsize=5, lw=2.0, color=CELL_CLASS_COLORS[cls])
        ax.set_xticks([0, 1], ["Green", "Yellow"])
        ax.set_ylabel("Session percentage (%)")
        ax.set_title(label)
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle(f"{area} — {layer_label}\nPaired session-level responsiveness", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(output_dir / "responsiveness_SESSION_PAIRED.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)

    # Session mean ± SEM only.
    fig, ax = plt.subplots(figsize=(9, 5.8))
    width = 0.26
    for cls, shift in [("green", -width/2), ("yellow", width/2)]:
        means, sems, ns = [], [], []
        for _, session_col, _ in metrics:
            m, se, n = mean_sem(session_df.loc[session_df["cell_class"] == cls, session_col])
            means.append(m); sems.append(se); ns.append(n)
        xx = x + shift
        ax.errorbar(xx, means, yerr=sems, fmt="o", ms=8, capsize=5, lw=2,
                    color=CELL_CLASS_COLORS[cls], label=cls.capitalize())
        for xpos, m, se, n in zip(xx, means, sems, ns):
            if np.isfinite(m):
                se_txt = f"{se:.1f}" if np.isfinite(se) else "n/a"
                ax.text(xpos, m, f"{m:.1f}±{se_txt}\nn={n}", ha="center", va="bottom", fontsize=7,
                        color=CELL_CLASS_COLORS[cls])
    ax.set_xticks(x, [m[2] for m in metrics])
    ax.set_ylabel("Session percentage (%)")
    ax.set_title(f"{area} — {layer_label}\nGREEN vs YELLOW — SESSION mean ± SEM")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "responsiveness_SESSION_MEAN_SEM_ONLY.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def make_metric_figures(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    area: str,
    layer_label: str,
    output_dir: Path,
    responsive_only: bool,
) -> None:
    suffix = "FDR_responsive_only" if responsive_only else "all_cells"
    subset_label = "FDR sound-responsive cells only" if responsive_only else "All classified cells"
    cdf = cell_df[cell_df["sound_responsive_fdr"].astype(bool)].copy() if responsive_only else cell_df.copy()
    sdf = aggregate_sessions(cdf) if len(cdf) else pd.DataFrame(columns=session_df.columns)

    plot_metric_grid(
        cdf, sdf, area, layer_label,
        output_dir / f"green_yellow_response_metrics_{suffix}_with_cells.png",
        mode="with_cells", subset_label=subset_label,
    )
    plot_metric_grid(
        cdf, sdf, area, layer_label,
        output_dir / f"green_yellow_response_metrics_{suffix}_MEAN_SEM_ONLY.png",
        mode="mean_only", subset_label=subset_label,
    )
    if len(sdf):
        plot_metric_grid(
            cdf, sdf, area, layer_label,
            output_dir / f"green_yellow_response_metrics_{suffix}_SESSION_PAIRED.png",
            mode="session_paired", subset_label=subset_label,
        )
        plot_metric_grid(
            cdf, sdf, area, layer_label,
            output_dir / f"green_yellow_response_metrics_{suffix}_SESSION_MEAN_SEM_ONLY.png",
            mode="session_mean", subset_label=subset_label,
        )

    plot_condition_profile(cdf, area, layer_label, output_dir, suffix)
    plot_selectivity_rasters(cdf, area, layer_label, output_dir, suffix)


def write_figure_index(output_dir: Path) -> None:
    pngs = sorted(output_dir.glob("*.png"))
    lines = ["FIGURE INDEX", "============", ""]
    lines.extend(p.name for p in pngs)
    (output_dir / "FIGURE_INDEX.txt").write_text("\n".join(lines) + "\n")


# =============================================================================
# REPORT / MASTER SUMMARY
# =============================================================================

def write_report(
    path: Path,
    subject: str,
    dates: list[str],
    area: str,
    layer_key: str,
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    stats_out: dict[str, Any],
) -> None:
    _, _, layer_label = LAYERS[layer_key]
    lines = []
    lines.append("GREEN-vs-YELLOW SOUND-TUNING ANALYSIS WITHIN AREA x LAYER")
    lines.append("=" * 82)
    lines.append(f"Subject: {subject}")
    lines.append(f"Dates: {', '.join(dates)}")
    lines.append(f"Area: {area}")
    lines.append(f"Layer: {layer_label}")
    lines.append("")
    lines.append("Counts:")
    for cls in CELL_CLASSES:
        cdf = cell_df[cell_df["cell_class"] == cls]
        sdf = session_df[session_df["cell_class"] == cls]
        lines.append(f"  {cls.upper()}: {len(cdf)} cells from {sdf['session_key'].nunique() if len(sdf) else 0} sessions")
    lines.append("")
    lines.append("PRIMARY INFERENCE")
    lines.append("  Paired session-level GREEN-vs-YELLOW comparisons using Wilcoxon signed-rank tests.")
    lines.append("  Only sessions containing finite summaries for BOTH classes contribute to each paired test.")
    lines.append("  Difference sign throughout is YELLOW - GREEN.")
    lines.append("  Pooled-cell tests are exploratory/descriptive because cells within a session are not independent replicates.")
    lines.append("")

    for metric, result in stats_out["continuous"].items():
        label = result["label"]
        lines.append(label)
        lines.append("-" * len(label))
        primary = result["session_level_primary_paired"]
        for cls in CELL_CLASSES:
            s = primary["summary"][cls]
            lines.append(
                f"  {cls.upper()}: mean={s['mean']:.4g}, SEM={s['sem']:.4g}, "
                f"median={s['median']:.4g}, n_sessions={s['n_sessions']}"
            )
        w = primary["yellow_vs_green_wilcoxon"]
        if np.isfinite(w["W"]):
            lines.append(
                f"  Paired YELLOW vs GREEN: W={w['W']:.4g}, {p_text(w['p'])}, "
                f"n_pairs={w['n_paired_sessions']}"
            )
        else:
            lines.append(f"  Paired YELLOW vs GREEN: unavailable (n_pairs={w['n_paired_sessions']})")
        lines.append(
            f"  Paired difference YELLOW-GREEN: mean={w['mean_difference_yellow_minus_green']:.4g}, "
            f"SEM={w['sem_difference']:.4g}, median={w['median_difference_yellow_minus_green']:.4g}"
        )
        exp = result["pooled_cell_exploratory"]["yellow_vs_green_mannwhitney"]
        if np.isfinite(exp["U"]):
            lines.append(
                f"  Exploratory pooled cells: U={exp['U']:.4g}, {p_text(exp['p'])}, "
                f"Cliff delta(Y-G)={exp['cliffs_delta']:.3g}"
            )
        lines.append("")

    for metric, result in stats_out["binary"].items():
        label = result["label"]
        lines.append(label)
        lines.append("-" * len(label))
        primary = result["session_level_primary_paired"]
        for cls in CELL_CLASSES:
            s = primary["summary"][cls]
            lines.append(
                f"  {cls.upper()}: {s['mean_percent']:.3g} ± {s['sem_percent']:.3g}% "
                f"across n={s['n_sessions']} sessions"
            )
        w = primary["yellow_vs_green_wilcoxon"]
        if np.isfinite(w["W"]):
            lines.append(
                f"  Paired YELLOW vs GREEN: W={w['W']:.4g}, {p_text(w['p'])}, "
                f"n_pairs={w['n_paired_sessions']}"
            )
        else:
            lines.append(f"  Paired YELLOW vs GREEN: unavailable (n_pairs={w['n_paired_sessions']})")
        fisher = result["pooled_cell_exploratory"]["yellow_vs_green_fisher"]
        lines.append(
            f"  Exploratory pooled-cell Fisher: odds ratio={fisher['odds_ratio']:.4g}, {p_text(fisher['p'])}"
            if np.isfinite(fisher["odds_ratio"])
            else "  Exploratory pooled-cell Fisher: unavailable"
        )
        lines.append("")

    path.write_text("\n".join(lines) + "\n")


def make_master_stats_rows(area: str, layer_key: str, stats_out: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for family in ("continuous", "binary"):
        for metric, result in stats_out[family].items():
            w = result["session_level_primary_paired"]["yellow_vs_green_wilcoxon"]
            row = {
                "area": area,
                "layer": layer_key,
                "metric_family": family,
                "metric": metric,
                "label": result["label"],
                "n_paired_sessions": w["n_paired_sessions"],
                "wilcoxon_W": w["W"],
                "wilcoxon_p": w["p"],
                "mean_difference_yellow_minus_green": w["mean_difference_yellow_minus_green"],
                "sem_difference": w["sem_difference"],
                "median_difference_yellow_minus_green": w["median_difference_yellow_minus_green"],
            }
            if family == "continuous":
                exp = result["pooled_cell_exploratory"]["yellow_vs_green_mannwhitney"]
                row.update({
                    "pooled_test": "Mann-Whitney",
                    "pooled_statistic": exp["U"],
                    "pooled_p": exp["p"],
                    "pooled_effect": exp["cliffs_delta"],
                })
            else:
                exp = result["pooled_cell_exploratory"]["yellow_vs_green_fisher"]
                row.update({
                    "pooled_test": "Fisher exact",
                    "pooled_statistic": exp["odds_ratio"],
                    "pooled_p": exp["p"],
                    "pooled_effect": exp["odds_ratio"],
                })
            rows.append(row)
    return rows


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

    print("=" * 82)
    print("SOUND_TUNING AREA x LAYER GREEN-vs-YELLOW ANALYSIS")
    print("=" * 82)
    print(f"Subject: {subject}")
    print(f"Dates:   {', '.join(dates)}")
    print(f"Areas:   {', '.join(areas)}")
    print("Layers:  L2/3 = 100 <= depth < 300 um; L4/5 = 300 <= depth <= 600 um")
    print(f"Input root:  {Path(settings.TEMP_OUTPUT_PATH) / 'evan' / 'sound_tuning_area_analysis'}")
    print(f"Output root: {out_root}")
    print("\nExpected inputs:")
    for area, path in in_paths.items():
        print(f"  {area}: {path} {'[FOUND]' if path.exists() else '[MISSING]'}")

    if args.dry_run:
        print("\nDry run complete; no tables were loaded.")
        return

    out_root.mkdir(parents=True, exist_ok=True)
    all_cells = load_area_tables(subject, dates, areas)
    all_cells.to_csv(out_root / "all_areas_combined_cell_results.csv", index=False)

    manifest = {
        "subject": subject,
        "dates": dates,
        "areas": areas,
        "input_files": {a: str(p) for a, p in in_paths.items()},
        "output_root": str(out_root),
        "layers": {
            "L23_100to300um": "100 <= depth < 300 um",
            "L45_300to600um": "300 <= depth <= 600 um",
        },
        "primary_inference": "paired session-level GREEN-vs-YELLOW Wilcoxon signed-rank tests",
        "difference_sign": "YELLOW - GREEN",
        "pooled_cell_inference": "exploratory/descriptive only",
    }
    save_json(out_root / "run_manifest.json", manifest)

    print("\nLoaded data:")
    for area in areas:
        adf = all_cells[all_cells["canonicalArea"] == area]
        print(f"  {area}: {len(adf)} cells, {adf['session_key'].nunique()} sessions")

    master_rows: list[dict[str, Any]] = []

    for area in areas:
        area_cells = all_cells[all_cells["canonicalArea"] == area].copy()
        for layer_key, (_, _, layer_label) in LAYERS.items():
            cells = subset_layer(area_cells, layer_key)
            out_dir = out_root / area / layer_key
            out_dir.mkdir(parents=True, exist_ok=True)

            print("\n" + "-" * 82)
            print(f"{area} — {layer_label}")
            for cls in CELL_CLASSES:
                cdf = cells[cells["cell_class"] == cls]
                print(f"  {cls.upper():6s}: {len(cdf)} cells, {cdf['session_key'].nunique()} sessions")

            session_df = aggregate_sessions(cells)
            cells.to_csv(out_dir / "cell_results.csv", index=False)
            session_df.to_csv(out_dir / "session_summary.csv", index=False)

            stats_out = run_statistics(cells, session_df)
            save_json(out_dir / "statistics.json", stats_out)
            write_report(
                out_dir / "REPORT.txt",
                subject, dates, area, layer_key,
                cells, session_df, stats_out,
            )
            master_rows.extend(make_master_stats_rows(area, layer_key, stats_out))

            plot_responsiveness(cells, session_df, area, layer_label, out_dir)
            make_metric_figures(cells, session_df, area, layer_label, out_dir, responsive_only=False)
            make_metric_figures(cells, session_df, area, layer_label, out_dir, responsive_only=True)
            write_figure_index(out_dir)

            # Helpful warning when there are no paired class summaries.
            n_paired_example = 0
            if len(session_df) and "fade_in_response" in session_df.columns:
                paired, _, _ = paired_session_vectors(session_df, "fade_in_response")
                n_paired_example = len(paired)
            print(f"  Paired sessions available (fade-in example): {n_paired_example}")
            print(f"  -> {out_dir}")

    master_df = pd.DataFrame(master_rows)
    master_df.to_csv(out_root / "MASTER_STATISTICS.csv", index=False)

    # Compact significance-oriented table for quick browsing.
    if len(master_df):
        quick_cols = [
            "area", "layer", "metric_family", "metric", "n_paired_sessions",
            "wilcoxon_W", "wilcoxon_p", "mean_difference_yellow_minus_green",
            "median_difference_yellow_minus_green",
        ]
        master_df[quick_cols].sort_values(["layer", "area", "wilcoxon_p"], na_position="last").to_csv(
            out_root / "PAIRED_GREEN_YELLOW_RESULTS_QUICKVIEW.csv", index=False
        )

    print("\n" + "=" * 82)
    print("DONE")
    print(f"Outputs saved under: {out_root}")
    print("Primary tests are paired session-level YELLOW-vs-GREEN comparisons.")
    print("=" * 82)


if __name__ == "__main__":
    main()
