#!/usr/bin/env python3
"""
Cross-area comparison of sound-tuning responses within GREEN or YELLOW cells.

This is a follow-up analysis for sound_tuning_area_analysis_v10.py. It does NOT
rerun Suite2p, Cellpose, or event alignment. Instead it loads the already-saved
combined_cell_results.csv files for A1, AAF, and A2 and asks questions such as:

    Do YELLOW cells in A2 have a different FI/FO selectivity index or AM-rate
    lifetime sparseness than YELLOW cells in A1?

The exact same cross-area analyses are then run separately for GREEN cells.

Analyses are repeated for three depth strata:
    all_depths : all included sessions
    L23        : 100 <= depth < 300 um
    L45        : 300 <= depth <= 600 um

The 300-um boundary is assigned to L4/5 so no session is counted twice.

IMPORTANT STATISTICAL CONVENTION
--------------------------------
Cells are useful for descriptive distributions, but the script does not treat
pooled cells as independent biological replicates for its primary cross-area
inference. Primary tests use one summary value per imaging session. Pooled-cell
statistics are also saved, but are explicitly labeled exploratory.

Input locations are resolved from jaratoolbox.settings.TEMP_OUTPUT_PATH.
No path prompt or save flag is used.

Expected prerequisite v10 output for each area:
    <TEMP_OUTPUT_PATH>/evan/sound_tuning_area_analysis/<subject>/<area>/<dates>/
        combined/combined_cell_results.csv

Example
-------
python sound_tuning_cross_area_cellclass_analysis_v2.py imag039 \
    --dates 20260729 20260730

Optional dry run:
python sound_tuning_cross_area_cellclass_analysis_v2.py imag039 \
    --dates 20260729 20260730 --dry-run
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
CELL_CLASSES = ("yellow", "green")

DEPTH_STRATA = {
    "all_depths": (None, None),
    "L23_100to300um": (100.0, 300.0),       # [100, 300)
    "L45_300to600um": (300.0, 600.0),       # [300, 600]
}

GREEN_COLOR = "limegreen"
YELLOW_COLOR = "goldenrod"
AREA_COLORS = {
    "A1": "tab:blue",
    "AAF": "tab:orange",
    "A2": "tab:green",
}

FDR_ALPHA = 0.05
DPI = 180

# Continuous metrics that exist in v5 combined_cell_results.csv.
# Aggregation indicates how each session contributes one value to the primary
# session-level analysis.
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
    "fade_in_vs_fade_out_selectivity": {
        "label": "FI/FO selectivity index",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "fade_in_vs_best_am_selectivity": {
        "label": "FI/best-AM selectivity index",
        "session_agg": "mean",
        "reference": 0.0,
    },
    "am_rate_lifetime_sparseness": {
        "label": "AM-rate lifetime sparseness",
        "session_agg": "mean",
        "reference": None,
    },
    "looming_score": {
        "label": "Looming score (dF/F)",
        "session_agg": "mean",
        "reference": 0.0,
    },
}

BINARY_METRICS = {
    "sound_responsive_fdr": "FDR sound-responsive cells (%)",
    "sound_excited_fdr": "FDR excited cells (%)",
    "sound_suppressed_fdr": "FDR suppressed cells (%)",
}


# =============================================================================
# GENERAL UTILITIES
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
        help="Dates used for the v10 area analyses, e.g. 20260729 20260730.",
    )
    parser.add_argument(
        "--areas",
        nargs="+",
        default=list(AREAS),
        choices=list(AREAS),
        help="Areas to compare. Default: A1 AAF A2.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print expected input/output paths and stop before loading tables.",
    )
    return parser.parse_args()


def date_tag(dates: Iterable[str]) -> str:
    return "_".join(str(d) for d in dates)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(obj, f, indent=2, default=json_default)


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
    sem = sd / np.sqrt(n) if n > 1 and np.isfinite(sd) else np.nan
    return mean, sd, sem, n


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


def holm_adjust(p_values: list[float]) -> list[float]:
    """Holm correction, preserving NaNs and original order."""
    p = np.asarray(p_values, dtype=float)
    out = np.full_like(p, np.nan)
    finite_idx = np.where(np.isfinite(p))[0]
    if len(finite_idx) == 0:
        return out.tolist()
    order = finite_idx[np.argsort(p[finite_idx])]
    m = len(order)
    running = 0.0
    for rank, idx in enumerate(order):
        adjusted = min(1.0, (m - rank) * p[idx])
        running = max(running, adjusted)
        out[idx] = running
    return out.tolist()


def cliffs_delta(x: Iterable[Any], y: Iterable[Any]) -> float:
    """Cliff's delta: positive means x tends to be larger than y."""
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return np.nan
    # Efficient enough for the expected session-level sample sizes. For pooled
    # cells use rank formulation to avoid an n_x * n_y temporary matrix.
    ranks = stats.rankdata(np.concatenate([x, y]))
    rx = np.sum(ranks[: len(x)])
    u = rx - len(x) * (len(x) + 1) / 2
    return float((2 * u) / (len(x) * len(y)) - 1)


def safe_mannwhitney(x: Iterable[Any], y: Iterable[Any]) -> dict[str, Any]:
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return {"n1": len(x), "n2": len(y), "U": np.nan, "p": np.nan, "cliffs_delta": np.nan}
    try:
        res = stats.mannwhitneyu(x, y, alternative="two-sided")
        return {
            "n1": len(x),
            "n2": len(y),
            "U": float(res.statistic),
            "p": float(res.pvalue),
            "cliffs_delta": cliffs_delta(x, y),
        }
    except Exception:
        return {"n1": len(x), "n2": len(y), "U": np.nan, "p": np.nan, "cliffs_delta": np.nan}


def safe_kruskal(groups: dict[str, Iterable[Any]]) -> dict[str, Any]:
    clean = {k: finite_values(v) for k, v in groups.items()}
    usable = {k: v for k, v in clean.items() if len(v) > 0}
    if len(usable) < 2:
        return {
            "areas": list(usable),
            "n_by_area": {k: len(v) for k, v in clean.items()},
            "H": np.nan,
            "p": np.nan,
        }
    try:
        res = stats.kruskal(*usable.values(), nan_policy="omit")
        return {
            "areas": list(usable),
            "n_by_area": {k: len(v) for k, v in clean.items()},
            "H": float(res.statistic),
            "p": float(res.pvalue),
        }
    except Exception:
        return {
            "areas": list(usable),
            "n_by_area": {k: len(v) for k, v in clean.items()},
            "H": np.nan,
            "p": np.nan,
        }


def pairwise_area_tests(groups: dict[str, Iterable[Any]], areas: list[str]) -> dict[str, Any]:
    records = []
    for i, a1 in enumerate(areas):
        for a2 in areas[i + 1 :]:
            test = safe_mannwhitney(groups.get(a1, []), groups.get(a2, []))
            records.append({"area1": a1, "area2": a2, **test})
    adjusted = holm_adjust([r["p"] for r in records])
    for rec, p_holm in zip(records, adjusted):
        rec["p_holm"] = p_holm
    return {f"{r['area1']}_vs_{r['area2']}": r for r in records}


def fisher_pairwise_binary(df: pd.DataFrame, binary_col: str, areas: list[str]) -> dict[str, Any]:
    records = []
    for i, a1 in enumerate(areas):
        for a2 in areas[i + 1 :]:
            d1 = df[df["canonicalArea"] == a1]
            d2 = df[df["canonicalArea"] == a2]
            n1 = len(d1)
            n2 = len(d2)
            y1 = int(d1[binary_col].astype(bool).sum()) if n1 else 0
            y2 = int(d2[binary_col].astype(bool).sum()) if n2 else 0
            if n1 == 0 or n2 == 0:
                odds, p = np.nan, np.nan
            else:
                odds, p = stats.fisher_exact([[y1, n1-y1], [y2, n2-y2]])
            records.append({
                "area1": a1, "area2": a2,
                "n1": n1, "positive1": y1,
                "n2": n2, "positive2": y2,
                "odds_ratio": float(odds) if np.isfinite(odds) else np.nan,
                "p": float(p) if np.isfinite(p) else np.nan,
            })
    adjusted = holm_adjust([r["p"] for r in records])
    for rec, p_holm in zip(records, adjusted):
        rec["p_holm"] = p_holm
    return {f"{r['area1']}_vs_{r['area2']}": r for r in records}


def p_text(p: float) -> str:
    if not np.isfinite(p):
        return "p=n/a"
    if p < 1e-4:
        return "p<1e-4"
    return f"p={p:.4f}"


# =============================================================================
# INPUT DISCOVERY / VALIDATION
# =============================================================================

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
        / "sound_tuning_cross_area_cellclass_analysis"
        / subject
        / date_tag(dates)
    )


def load_area_tables(subject: str, dates: list[str], areas: list[str]) -> pd.DataFrame:
    frames = []
    missing = []
    for area in areas:
        path = expected_area_csv(subject, area, dates)
        if not path.exists():
            missing.append(path)
            continue
        df = pd.read_csv(path)
        # Be strict about the provenance encoded in the table.
        if "canonicalArea" not in df.columns:
            raise ValueError(f"{path} has no canonicalArea column; expected a v10 output table.")
        bad = set(df["canonicalArea"].dropna().astype(str).unique()) - {area}
        if bad:
            raise ValueError(f"{path} contains unexpected canonicalArea values: {sorted(bad)}")
        frames.append(df)

    if missing:
        msg = "Missing prerequisite v10 output(s):\n" + "\n".join(f"  {p}" for p in missing)
        msg += "\nRun sound_tuning_area_analysis_v10.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)

    if not frames:
        raise RuntimeError("No area tables were loaded.")

    df = pd.concat(frames, ignore_index=True, sort=False)

    required = {
        "subject", "date", "session", "session_key", "canonicalArea", "brainArea",
        "depth", "cell_class", "sound_responsive_fdr", "sound_excited_fdr",
        "sound_suppressed_fdr", "fade_in_response", "fade_out_response",
        "mean_am_response_across_rates", "best_am_response",
        "fade_in_vs_fade_out_selectivity", "fade_in_vs_best_am_selectivity",
        "am_rate_lifetime_sparseness", "looming_score", "mean_sound_response",
    }
    missing_cols = sorted(required - set(df.columns))
    if missing_cols:
        raise ValueError("Combined cell table(s) are missing required columns: " + ", ".join(missing_cols))

    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")
    for col in BINARY_METRICS:
        if df[col].dtype != bool:
            df[col] = df[col].astype(str).str.lower().isin(["true", "1", "yes"])

    return df


def subset_depth(df: pd.DataFrame, stratum: str) -> pd.DataFrame:
    low, high = DEPTH_STRATA[stratum]
    if low is None:
        return df.copy()
    depth = pd.to_numeric(df["depth"], errors="coerce")
    if stratum.startswith("L23"):
        mask = (depth >= low) & (depth < high)
    else:
        mask = (depth >= low) & (depth <= high)
    return df.loc[mask].copy()


# =============================================================================
# SESSION-LEVEL SUMMARIES AND STATISTICS
# =============================================================================

def aggregate_sessions(df: pd.DataFrame) -> pd.DataFrame:
    """One row per imaging session/area/class, retaining within-session SD."""
    rows = []
    group_cols = ["subject", "date", "session", "session_key", "canonicalArea", "brainArea", "depth", "cell_class"]

    for keys, sdf in df.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        row["n_cells"] = int(len(sdf))
        for binary_col, pct_col in [
            ("sound_responsive_fdr", "pct_sound_responsive_fdr"),
            ("sound_excited_fdr", "pct_sound_excited_fdr"),
            ("sound_suppressed_fdr", "pct_sound_suppressed_fdr"),
        ]:
            vals = sdf[binary_col].astype(float).to_numpy()
            row["n_" + binary_col] = int(np.sum(vals > 0.5))
            row[pct_col] = 100.0 * float(np.mean(vals)) if len(vals) else np.nan
            row["sd_" + pct_col] = 100.0 * float(np.std(vals, ddof=1)) if len(vals) > 1 else np.nan

        for metric, cfg in CONTINUOUS_METRICS.items():
            vals = finite_values(sdf[metric]) if metric in sdf else np.array([])
            if len(vals) == 0:
                value = np.nan
            elif cfg["session_agg"] == "median":
                value = float(np.median(vals))
            else:
                value = float(np.mean(vals))
            row[metric] = value
            row[f"sd_{metric}"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else np.nan

        for col in sorted(c for c in sdf.columns if c.startswith("am_response_") and c.endswith("Hz")):
            vals = finite_values(sdf[col])
            row[col] = float(np.mean(vals)) if len(vals) else np.nan
            row[f"sd_{col}"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else np.nan

        rows.append(row)
    return pd.DataFrame(rows)


def analyze_continuous_metric(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    metric: str,
    areas: list[str],
) -> dict[str, Any]:
    pooled_groups = {
        area: cell_df.loc[cell_df["canonicalArea"] == area, metric]
        for area in areas
    }
    session_groups = {
        area: session_df.loc[session_df["canonicalArea"] == area, metric]
        for area in areas
    }

    pooled_summary = {}
    session_summary = {}
    for area in areas:
        med, q1, q3, n = median_iqr(pooled_groups[area])
        mean, sem, n_mean = mean_sem(pooled_groups[area])
        pooled_summary[area] = {
            "n_cells": n,
            "mean": mean,
            "sem": sem,
            "median": med,
            "q1": q1,
            "q3": q3,
        }
        sm, se, ns = mean_sem(session_groups[area])
        smed, sq1, sq3, _ = median_iqr(session_groups[area])
        session_summary[area] = {
            "n_sessions": ns,
            "mean": sm,
            "sem": se,
            "median": smed,
            "q1": sq1,
            "q3": sq3,
        }

    return {
        "label": CONTINUOUS_METRICS[metric]["label"],
        "session_aggregation": CONTINUOUS_METRICS[metric]["session_agg"],
        "pooled_cell_exploratory": {
            "summary": pooled_summary,
            "omnibus_kruskal": safe_kruskal(pooled_groups),
            "pairwise_mannwhitney_holm": pairwise_area_tests(pooled_groups, areas),
        },
        "session_level_primary": {
            "summary": session_summary,
            "omnibus_kruskal": safe_kruskal(session_groups),
            "pairwise_mannwhitney_holm": pairwise_area_tests(session_groups, areas),
        },
    }


def analyze_binary_metric(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    metric: str,
    areas: list[str],
) -> dict[str, Any]:
    pct_col = {
        "sound_responsive_fdr": "pct_sound_responsive_fdr",
        "sound_excited_fdr": "pct_sound_excited_fdr",
        "sound_suppressed_fdr": "pct_sound_suppressed_fdr",
    }[metric]

    pooled_summary = {}
    session_summary = {}
    session_groups = {}
    for area in areas:
        cdf = cell_df[cell_df["canonicalArea"] == area]
        n = len(cdf)
        positive = int(cdf[metric].astype(bool).sum()) if n else 0
        pooled_summary[area] = {
            "n_cells": n,
            "positive": positive,
            "percent": 100.0 * positive / n if n else np.nan,
        }
        vals = session_df.loc[session_df["canonicalArea"] == area, pct_col]
        session_groups[area] = vals
        mean, sem, ns = mean_sem(vals)
        session_summary[area] = {"n_sessions": ns, "mean_percent": mean, "sem_percent": sem}

    return {
        "label": BINARY_METRICS[metric],
        "pooled_cell_exploratory": {
            "summary": pooled_summary,
            "pairwise_fisher_holm": fisher_pairwise_binary(cell_df, metric, areas),
        },
        "session_level_primary": {
            "summary": session_summary,
            "omnibus_kruskal": safe_kruskal(session_groups),
            "pairwise_mannwhitney_holm": pairwise_area_tests(session_groups, areas),
        },
    }


def run_statistics(cell_df: pd.DataFrame, session_df: pd.DataFrame, areas: list[str]) -> dict[str, Any]:
    out = {"continuous": {}, "binary": {}}
    for metric in CONTINUOUS_METRICS:
        if metric in cell_df.columns:
            out["continuous"][metric] = analyze_continuous_metric(cell_df, session_df, metric, areas)
    for metric in BINARY_METRICS:
        if metric in cell_df.columns:
            out["binary"][metric] = analyze_binary_metric(cell_df, session_df, metric, areas)
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


def annotate_mean_sem(ax: plt.Axes, x: float, mean: float, sem: float, n: int, color: str, y_top: float | None = None) -> None:
    if not np.isfinite(mean):
        return
    sem_txt = f"{sem:.4g}" if np.isfinite(sem) else "n/a"
    txt = f"{mean:.4g} ± {sem_txt}\nn={n}"
    if y_top is None:
        ax.text(x, mean, txt, ha="center", va="bottom", fontsize=8, color=color)
    else:
        ax.text(x, y_top, txt, ha="center", va="top", fontsize=8, color=color)


def plot_area_distribution(
    df: pd.DataFrame,
    metric: str,
    areas: list[str],
    title: str,
    output_path: Path,
    reference: float | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    positions = np.arange(len(areas))
    all_vals = []
    rng = np.random.default_rng(0)

    for x, area in zip(positions, areas):
        vals = finite_values(df.loc[df["canonicalArea"] == area, metric])
        all_vals.extend(vals.tolist())
        if len(vals):
            jitter = rng.normal(0, 0.055, size=len(vals))
            ax.scatter(
                np.full(len(vals), x) + jitter,
                vals,
                s=14,
                alpha=0.24,
                color=AREA_COLORS[area],
                edgecolors="none",
            )
            mean, sem, _ = mean_sem(vals)
            ax.errorbar(x, mean, yerr=sem if np.isfinite(sem) else None,
                        fmt="o", ms=8, capsize=5, lw=2.0, color=AREA_COLORS[area])

    if reference is not None:
        ax.axhline(reference, ls="--", lw=1, color="0.45")

    ax.set_xticks(positions, areas)
    ax.set_ylabel(CONTINUOUS_METRICS.get(metric, {}).get("label", metric))
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.25)

    # Robust display only; statistics retain all values.
    vals = finite_values(all_vals)
    if len(vals) >= 4:
        q1, q3 = np.percentile(vals, [25, 75])
        iqr = q3 - q1
        if np.isfinite(iqr) and iqr > 0:
            lo_fence, hi_fence = q1 - 3*iqr, q3 + 3*iqr
            inliers = vals[(vals >= lo_fence) & (vals <= hi_fence)]
            if len(inliers):
                lo, hi = float(np.min(inliers)), float(np.max(inliers))
                if reference is not None:
                    lo, hi = min(lo, reference), max(hi, reference)
                span = hi - lo if hi > lo else max(abs(lo), 1.0) * 0.25
                ax.set_ylim(lo - 0.10*span, hi + 0.16*span)
                n_clip = int(np.sum((vals < ax.get_ylim()[0]) | (vals > ax.get_ylim()[1])))
                if n_clip:
                    ax.text(0.99, 0.01, f"display clips {n_clip} extreme cell(s)",
                            transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color="0.35")

    fig.tight_layout()
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_area_mean_sem(
    df: pd.DataFrame,
    metric: str,
    areas: list[str],
    title: str,
    output_path: Path,
    reference: float | None = None,
) -> None:
    means, sems, ns = [], [], []
    for area in areas:
        m, se, n = mean_sem(df.loc[df["canonicalArea"] == area, metric])
        means.append(m); sems.append(se); ns.append(n)
    means = np.asarray(means, float)
    sems = np.asarray(sems, float)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    x = np.arange(len(areas))
    for xi, area, m, se in zip(x, areas, means, sems):
        if np.isfinite(m):
            ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None,
                        fmt="o", ms=10, capsize=6, lw=2.2, color=AREA_COLORS[area])
    if reference is not None:
        ax.axhline(reference, ls="--", lw=1, color="0.45")

    refs = [reference] if reference is not None else None
    ylim = optimized_ylim_from_summary(means, sems, refs)
    if ylim:
        ax.set_ylim(*ylim)
    y_top = ax.get_ylim()[1] - 0.03 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    for xi, area, m, se, n in zip(x, areas, means, sems, ns):
        annotate_mean_sem(ax, xi, m, se, n, AREA_COLORS[area], y_top=y_top)

    ax.set_xticks(x, areas)
    ax.set_ylabel(CONTINUOUS_METRICS.get(metric, {}).get("label", metric))
    ax.set_title(title + "\nmean ± SEM; individual cells not shown")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_session_mean_sem(
    session_df: pd.DataFrame,
    metric: str,
    areas: list[str],
    title: str,
    output_path: Path,
    reference: float | None = None,
) -> None:
    means, sems, ns = [], [], []
    for area in areas:
        m, se, n = mean_sem(session_df.loc[session_df["canonicalArea"] == area, metric])
        means.append(m); sems.append(se); ns.append(n)
    means = np.asarray(means, float); sems = np.asarray(sems, float)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    x = np.arange(len(areas))
    for xi, area, m, se in zip(x, areas, means, sems):
        if np.isfinite(m):
            ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None,
                        fmt="o", ms=10, capsize=6, lw=2.2, color=AREA_COLORS[area])
    if reference is not None:
        ax.axhline(reference, ls="--", lw=1, color="0.45")
    ylim = optimized_ylim_from_summary(means, sems, [reference] if reference is not None else None)
    if ylim:
        ax.set_ylim(*ylim)
    y_top = ax.get_ylim()[1] - 0.03*(ax.get_ylim()[1]-ax.get_ylim()[0])
    for xi, area, m, se, n in zip(x, areas, means, sems, ns):
        annotate_mean_sem(ax, xi, m, se, n, AREA_COLORS[area], y_top=y_top)
    ax.set_xticks(x, areas)
    ax.set_ylabel(CONTINUOUS_METRICS.get(metric, {}).get("label", metric))
    ax.set_title(title + "\nSESSION-LEVEL mean ± SEM")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def plot_responsiveness(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    areas: list[str],
    cell_class: str,
    depth_label: str,
    output_dir: Path,
) -> None:
    metrics = [
        ("sound_responsive_fdr", "pct_sound_responsive_fdr", "Responsive"),
        ("sound_excited_fdr", "pct_sound_excited_fdr", "Excited"),
        ("sound_suppressed_fdr", "pct_sound_suppressed_fdr", "Suppressed"),
    ]
    # Existing pooled-cell descriptive percentages retained.
    fig, ax = plt.subplots(figsize=(9, 5.5)); width=0.22; x=np.arange(len(metrics))
    for ai,area in enumerate(areas):
        vals=[]
        for cell_col,_,_ in metrics:
            adf=cell_df[cell_df["canonicalArea"]==area]; vals.append(100.0*adf[cell_col].astype(bool).mean() if len(adf) else np.nan)
        xx=x+(ai-(len(areas)-1)/2)*width
        ax.bar(xx,vals,width=width,color=AREA_COLORS[area],alpha=0.82,label=area)
        for xxx,yy in zip(xx,vals):
            if np.isfinite(yy): ax.text(xxx,yy,f"{yy:.1f}%",ha="center",va="bottom",fontsize=8,rotation=90)
    ax.set_xticks(x,[m[2] for m in metrics]); ax.set_ylabel("Cells (%)"); ax.set_ylim(0,max(5,min(100,ax.get_ylim()[1]*1.15)))
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\npooled-cell descriptive percentages"); ax.legend(frameon=False); ax.grid(axis="y",alpha=0.25)
    fig.tight_layout(); fig.savefig(output_dir/"responsiveness_pooled_cell_percentages.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    # Existing session filename retained, now following the new session-aware convention.
    fig,axes=plt.subplots(1,3,figsize=(14.8,5.4),squeeze=False); axes=axes.ravel()
    for ax,(_,pct_col,label) in zip(axes,metrics):
        for xi,area in enumerate(areas):
            sdf=session_df[session_df["canonicalArea"]==area]; offsets=np.linspace(-0.07,0.07,max(len(sdf),1))
            for off,(_,row) in zip(offsets,sdf.iterrows()):
                m=float(row.get(pct_col,np.nan)); sd=float(row.get(f"sd_{pct_col}",np.nan))
                if np.isfinite(m):
                    ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=3.5,elinewidth=0.7,capsize=2,
                                color=AREA_COLORS[area],alpha=0.28,zorder=2)
            vals=finite_values(sdf[pct_col]) if pct_col in sdf else np.array([]); m,_,se,n=mean_sd_sem(vals)
            if np.isfinite(m):
                ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,elinewidth=2.5,capsize=6,color=AREA_COLORS[area],zorder=5)
                ax.annotate(f"{m:.1f} +/- {se:.1f}\nn={n}" if np.isfinite(se) else f"{m:.1f}\nn={n}",(xi,m),xytext=(0,10),textcoords="offset points",ha="center",fontsize=7,color=AREA_COLORS[area])
        ax.set_xticks(np.arange(len(areas)),areas); ax.set_ylabel("Session percentage (%)"); ax.set_title(label); ax.grid(axis="y",alpha=0.25); ax.spines[["top","right"]].set_visible(False)
    fig.suptitle(f"{cell_class.upper()} cells across areas — {depth_label}\nlight=session mean +/- SD; dark=overall mean +/- SEM",fontsize=13)
    fig.tight_layout(rect=[0,0,1,0.92]); fig.savefig(output_dir/"responsiveness_session_mean_sem_only.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


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


def plot_condition_profiles(
    cell_df: pd.DataFrame,
    areas: list[str],
    cell_class: str,
    depth_label: str,
    output_dir: Path,
    suffix: str = "all_cells",
) -> None:
    """Condition profile using light session mean +/- SD and dark overall +/- SEM."""
    cols, labels = condition_columns(cell_df)
    if not cols or len(cell_df)==0:
        return
    session_df=aggregate_sessions(cell_df)
    fig, ax = plt.subplots(figsize=(9.8, 6.2))
    x=np.arange(len(cols),dtype=float)
    for area in areas:
        sdf=session_df[session_df["canonicalArea"]==area]
        # Individual sessions: light/thin mean profile with within-session SD.
        for _,row in sdf.iterrows():
            means=np.asarray([float(row.get(c,np.nan)) for c in cols],float)
            sds=np.asarray([float(row.get(f"sd_{c}",np.nan)) for c in cols],float)
            ax.plot(x,means,color=AREA_COLORS[area],alpha=0.20,lw=0.9,marker="o",ms=2.5,zorder=1)
            ax.errorbar(x,means,yerr=sds,fmt="none",elinewidth=0.55,capsize=1.5,color=AREA_COLORS[area],alpha=0.13,zorder=1)
        # Overall: mean of session means +/- SEM across sessions.
        if len(sdf):
            mat=np.column_stack([pd.to_numeric(sdf[c],errors="coerce") for c in cols])
            means=np.nanmean(mat,axis=0)
            counts=np.sum(np.isfinite(mat),axis=0)
            sems=np.full(len(cols),np.nan)
            for j in range(len(cols)):
                vals=mat[:,j]; vals=vals[np.isfinite(vals)]
                if len(vals)>1: sems[j]=float(np.std(vals,ddof=1)/np.sqrt(len(vals)))
            ax.plot(x,means,color=AREA_COLORS[area],alpha=1.0,lw=3.0,marker="o",ms=5,label=f"{area} overall",zorder=5)
            ax.errorbar(x,means,yerr=sems,fmt="none",elinewidth=2.0,capsize=4,color=AREA_COLORS[area],zorder=4)
    ax.axhline(0,ls="--",lw=1,color="0.45")
    ax.set_xticks(x,labels,rotation=30,ha="right"); ax.set_ylabel("Response (dF/F)")
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\n{suffix.replace('_',' ')}: light=session mean +/- SD; dark=overall mean +/- SEM")
    ax.legend(frameon=False,ncol=min(3,len(areas))); ax.grid(axis="y",alpha=0.25); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(output_dir/f"condition_response_profile_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_selectivity_rasters(
    cell_df: pd.DataFrame,
    areas: list[str],
    cell_class: str,
    depth_label: str,
    output_dir: Path,
    suffix: str,
) -> None:
    cols, labels = condition_columns(cell_df)
    if len(cols) < 2:
        return
    fig, axes = plt.subplots(nrows=len(areas), ncols=1, figsize=(9, 3.5*len(areas)), squeeze=False)
    im = None
    for row, area in enumerate(areas):
        ax = axes[row, 0]
        adf = cell_df[cell_df["canonicalArea"] == area].copy()
        if len(adf) == 0:
            ax.text(0.5, 0.5, "No cells", transform=ax.transAxes, ha="center", va="center")
            ax.set_axis_off()
            continue
        matrix = adf[cols].to_numpy(dtype=float)
        denom = np.nanmax(np.abs(matrix), axis=1)
        good = np.isfinite(denom) & (denom > 0)
        matrix = matrix[good]
        adf = adf.iloc[np.where(good)[0]].copy()
        if len(matrix) == 0:
            ax.text(0.5, 0.5, "No finite responses", transform=ax.transAxes, ha="center", va="center")
            continue
        norm = matrix / denom[good, None]
        order = np.argsort(adf["looming_score"].to_numpy(dtype=float))[::-1]
        norm = norm[order]
        im = ax.imshow(norm, aspect="auto", interpolation="nearest", vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(np.arange(len(labels)), labels, rotation=30, ha="right")
        ax.set_ylabel(f"{area} cells")
        ax.set_title(f"{area}: n={len(norm)} | sorted by looming score")
    fig.suptitle(f"{cell_class.upper()} selectivity across areas — {depth_label}\n{suffix.replace('_',' ')}", y=1.01)
    if im is not None:
        fig.colorbar(im, ax=axes.ravel().tolist(), label="Normalized condition response", shrink=0.75)
    fig.tight_layout()
    fig.savefig(output_dir / f"selectivity_rasters_{suffix}.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def _robust_cell_ylim(values, reference=None):
    vals=finite_values(values)
    if len(vals)==0: return None
    if len(vals)>=4:
        q1,q3=np.percentile(vals,[25,75]); iqr=q3-q1
        if np.isfinite(iqr) and iqr>0:
            vals=vals[(vals>=q1-3*iqr)&(vals<=q3+3*iqr)]
    if len(vals)==0: return None
    lo,hi=float(np.min(vals)),float(np.max(vals))
    if reference is not None:
        lo=min(lo,reference); hi=max(hi,reference)
    span=hi-lo if hi>lo else max(abs(lo),abs(hi),1.0)*0.25
    return lo-0.10*span,hi+0.16*span


def _selectivity_equation(metric: str) -> str:
    if metric == "fade_in_vs_fade_out_selectivity":
        return r"$SI_{FI/FO}=(R_{FI}-R_{FO})/(R_{FI}+R_{FO})$"
    if metric == "fade_in_vs_best_am_selectivity":
        return r"$SI_{FI/AM}=(R_{FI}-R_{bestAM})/(R_{FI}+R_{bestAM})$"
    if metric == "am_rate_lifetime_sparseness":
        return r"$S_{life}=\frac{1-(\sum R_i/N)^2/(\sum R_i^2/N)}{1-1/N}$"
    return metric


def plot_metric_grid(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    areas: list[str],
    cell_class: str,
    depth_label: str,
    output_path: Path,
    mode: str,
    subset_label: str,
) -> None:
    """Core cross-area response comparisons with cell or session displays."""
    metrics = list(CONTINUOUS_METRICS.keys())
    ncols=3; nrows=int(np.ceil(len(metrics)/ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(16.5, 4.7*nrows))
    axes=np.atleast_1d(axes).ravel()
    rng=np.random.default_rng(0)

    for ax,metric in zip(axes,metrics):
        cfg=CONTINUOUS_METRICS[metric]; ref=cfg["reference"]; x=np.arange(len(areas),dtype=float)
        if mode=="with_cells":
            display=[]
            for xi,area in enumerate(areas):
                vals=finite_values(cell_df.loc[cell_df["canonicalArea"]==area,metric])
                if len(vals):
                    ax.scatter(np.full(len(vals),xi)+rng.uniform(-0.08,0.08,len(vals)),vals,s=12,alpha=0.20,
                               color=AREA_COLORS[area],edgecolors="none",zorder=1)
                    m,_,se,n=mean_sd_sem(vals)
                    ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=8,capsize=5,elinewidth=2.0,
                                color=AREA_COLORS[area],zorder=4)
                    display.extend(vals.tolist())
            ylim=_robust_cell_ylim(display,ref)
            if ylim: ax.set_ylim(*ylim)
            subtitle="individual cells; dark = pooled mean +/- SEM (exploratory)"
        else:
            # New convention: light individual session mean +/- within-session SD;
            # dark overall mean +/- SEM across session means.
            all_for_ylim=[]
            for xi,area in enumerate(areas):
                sdf=session_df[session_df["canonicalArea"]==area]
                vals=finite_values(sdf[metric]) if metric in sdf else np.array([])
                if len(sdf):
                    offsets=np.linspace(-0.07,0.07,max(len(sdf),1))
                    for off,(_,row) in zip(offsets,sdf.iterrows()):
                        m=float(row.get(metric,np.nan)); sd=float(row.get(f"sd_{metric}",np.nan))
                        if np.isfinite(m):
                            ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=3.6,
                                        elinewidth=0.75,capsize=2,color=AREA_COLORS[area],alpha=0.28,zorder=2)
                            all_for_ylim.append(m)
                            if np.isfinite(sd): all_for_ylim.extend([m-sd,m+sd])
                m,_,se,n=mean_sd_sem(vals)
                if np.isfinite(m):
                    ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,elinewidth=2.6,
                                color=AREA_COLORS[area],zorder=6)
                    ax.annotate(f"{m:.3g} +/- {se:.2g}\nn={n} sessions" if np.isfinite(se) else f"{m:.3g}\nn={n} sessions",
                                (xi,m),xytext=(0,11),textcoords="offset points",ha="center",fontsize=7,color=AREA_COLORS[area])
                    all_for_ylim.extend([m]);
                    if np.isfinite(se): all_for_ylim.extend([m-se,m+se])
            ylim=_robust_cell_ylim(all_for_ylim,ref)
            if ylim: ax.set_ylim(*ylim)
            subtitle="light = session mean +/- SD; dark = overall mean +/- SEM"
        if ref is not None: ax.axhline(ref,ls="--",lw=0.9,color="0.45")
        ax.set_xticks(x,areas); ax.set_title(cfg["label"],fontsize=10); ax.grid(axis="y",alpha=0.22)
        if metric in {"fade_in_vs_fade_out_selectivity","fade_in_vs_best_am_selectivity","am_rate_lifetime_sparseness"}:
            ax.text(0.5,-0.20,_selectivity_equation(metric),transform=ax.transAxes,ha="center",va="top",fontsize=8)

    for ax in axes[len(metrics):]: ax.axis("off")
    fig.suptitle(f"{cell_class.upper()} cells across A1 / AAF / A2 — {depth_label}\n{subset_label}: {subtitle}",fontsize=14)
    fig.tight_layout(rect=[0,0.02,1,0.95])
    fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_standalone_selectivity_across_areas(cell_df, session_df, areas, cell_class, depth_label, output_dir, suffix, stats_out):
    """Standalone FI/FO and AM-sparseness figures in cell-point and session-point forms."""
    specs=[
        ("fade_in_vs_fade_out_selectivity","Fade-in vs fade-out selectivity","fade_in_vs_fade_out_selectivity"),
        ("am_rate_lifetime_sparseness","AM-rate selectivity (lifetime sparseness)","am_rate_lifetime_sparseness"),
    ]
    rng=np.random.default_rng(20260819)
    for metric,title,stem in specs:
        if metric not in cell_df: continue
        ref=CONTINUOUS_METRICS[metric]["reference"]
        # Cell points.
        fig,ax=plt.subplots(figsize=(7.4,6.2)); display=[]
        for xi,area in enumerate(areas):
            vals=finite_values(cell_df.loc[cell_df["canonicalArea"]==area,metric])
            if len(vals):
                ax.scatter(np.full(len(vals),xi)+rng.uniform(-0.09,0.09,len(vals)),vals,s=20,alpha=0.22,
                           color=AREA_COLORS[area],edgecolors="none")
                m,_,se,n=mean_sd_sem(vals)
                ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,elinewidth=2.4,
                            color=AREA_COLORS[area],zorder=5)
                display.extend(vals.tolist())
        if ref is not None: ax.axhline(ref,ls="--",lw=1,color="0.45")
        pooled=stats_out.get("continuous",{}).get(metric,{}).get("pooled_cell_exploratory",{}).get("omnibus_kruskal",{})
        p=pooled.get("p",np.nan)
        ax.set_xticks(np.arange(len(areas)),areas); ax.set_ylabel(CONTINUOUS_METRICS[metric]["label"])
        ax.set_title(f"{cell_class.upper()} — {depth_label}\n{title}\nindividual cells; exploratory omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} — {depth_label}\n{title}\nindividual cells")
        ax.text(0.5,-0.15,_selectivity_equation(metric),transform=ax.transAxes,ha="center",va="top",fontsize=10)
        ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
        ylim=_robust_cell_ylim(display,ref)
        if ylim: ax.set_ylim(*ylim)
        fig.subplots_adjust(bottom=0.22); fig.savefig(output_dir/f"{stem}_across_areas_{suffix}_CELL_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

        # Session points with within-session SD and overall SEM.
        fig,ax=plt.subplots(figsize=(7.4,6.2)); display=[]
        for xi,area in enumerate(areas):
            sdf=session_df[session_df["canonicalArea"]==area]
            offsets=np.linspace(-0.07,0.07,max(len(sdf),1))
            for off,(_,row) in zip(offsets,sdf.iterrows()):
                m=float(row.get(metric,np.nan)); sd=float(row.get(f"sd_{metric}",np.nan))
                if not np.isfinite(m): continue
                ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=4,elinewidth=0.8,capsize=2,
                            color=AREA_COLORS[area],alpha=0.30,zorder=2)
                display.append(m)
                if np.isfinite(sd): display.extend([m-sd,m+sd])
            vals=finite_values(sdf[metric]) if metric in sdf else np.array([])
            m,_,se,n=mean_sd_sem(vals)
            if np.isfinite(m):
                ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=11,elinewidth=2.8,capsize=7,
                            color=AREA_COLORS[area],zorder=6)
                ax.annotate(f"{m:.3g} +/- {se:.2g}\nn={n} sessions" if np.isfinite(se) else f"{m:.3g}\nn={n} sessions",
                            (xi,m),xytext=(0,12),textcoords="offset points",ha="center",fontsize=8,color=AREA_COLORS[area])
        if ref is not None: ax.axhline(ref,ls="--",lw=1,color="0.45")
        primary=stats_out.get("continuous",{}).get(metric,{}).get("session_level_primary",{}).get("omnibus_kruskal",{})
        p=primary.get("p",np.nan)
        ax.set_xticks(np.arange(len(areas)),areas); ax.set_ylabel(CONTINUOUS_METRICS[metric]["label"])
        ax.set_title(f"{cell_class.upper()} — {depth_label}\n{title}\nlight=session mean +/- SD; dark=overall mean +/- SEM\nsession-level omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} — {depth_label}\n{title}\nsession points")
        ax.text(0.5,-0.15,_selectivity_equation(metric),transform=ax.transAxes,ha="center",va="top",fontsize=10)
        ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
        ylim=_robust_cell_ylim(display,ref)
        if ylim: ax.set_ylim(*ylim)
        fig.subplots_adjust(bottom=0.22); fig.savefig(output_dir/f"{stem}_across_areas_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_am_rate_profiles_sessions_top_cells(cell_df, areas, cell_class, depth_label, output_dir, suffix):
    am_cols=[]; am_rates=[]
    for c in cell_df.columns:
        if c.startswith("am_response_") and c.endswith("Hz"):
            try: rate=float(c[len("am_response_"):-2])
            except Exception: continue
            am_cols.append(c); am_rates.append(rate)
    if not am_cols: return
    order=np.argsort(am_rates); am_cols=[am_cols[i] for i in order]; am_rates=[am_rates[i] for i in order]
    x=np.arange(len(am_rates),dtype=float); fig,ax=plt.subplots(figsize=(9.8,6.2))
    for area in areas:
        adf=cell_df[cell_df["canonicalArea"]==area]
        for sk,sdf in adf.groupby("session_key",sort=True):
            matrix=sdf[am_cols].to_numpy(float)
            if matrix.size==0: continue
            sparse=pd.to_numeric(sdf["am_rate_lifetime_sparseness"],errors="coerce").to_numpy(float)
            valid=np.flatnonzero(np.isfinite(sparse)); valid=valid[np.argsort(sparse[valid])[::-1]][:5]
            for idx in valid:
                ax.plot(x,matrix[idx],color=AREA_COLORS[area],alpha=0.12,lw=0.8,ls="--",zorder=1)
            mean=np.nanmean(matrix,axis=0); sd=np.nanstd(matrix,axis=0,ddof=1) if len(matrix)>1 else np.full(len(am_cols),np.nan)
            ax.plot(x,mean,color=AREA_COLORS[area],alpha=0.48,lw=1.5,marker="o",ms=3,zorder=2)
            ax.errorbar(x,mean,yerr=sd,fmt="none",elinewidth=0.55,capsize=1.5,color=AREA_COLORS[area],alpha=0.14,zorder=1)
        # Overall mean of session means, emphasized.
        sess=aggregate_sessions(adf)
        if len(sess):
            sm=np.column_stack([pd.to_numeric(sess[c],errors="coerce") for c in am_cols])
            overall=np.nanmean(sm,axis=0)
            sem=np.nanstd(sm,axis=0,ddof=1)/np.sqrt(np.sum(np.isfinite(sm),axis=0)) if len(sm)>1 else np.full(len(am_cols),np.nan)
            ax.plot(x,overall,color=AREA_COLORS[area],alpha=1,lw=3.0,marker="o",ms=5,label=f"{area} overall session mean",zorder=5)
            ax.errorbar(x,overall,yerr=sem,fmt="none",elinewidth=2.0,capsize=4,color=AREA_COLORS[area],zorder=4)
    ax.axhline(0,color="black",ls=":",lw=0.9); ax.set_xticks(x,[f"{r:g}" for r in am_rates])
    ax.set_xlabel("AM rate (Hz)"); ax.set_ylabel("Baseline-subtracted dF/F")
    ax.set_title(f"{cell_class.upper()} — {depth_label}\nAM-rate response profiles — {suffix.replace('_',' ')}\nlight solid=session means; dim dashed=top 5 cells/session; dark=overall mean +/- SEM")
    ax.legend(frameon=False,fontsize=8,ncol=min(3,len(areas))); ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(output_dir/f"am_rate_profiles_{suffix}_SESSION_MEANS_TOP5_CELLS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_additional_selectivity_rasters(cell_df,areas,cell_class,depth_label,output_dir,suffix):
    cols,labels=condition_columns(cell_df)
    if len(cols)<2 or len(cell_df)==0: return
    fig,axes=plt.subplots(len(areas),2,figsize=(13,3.6*len(areas)),squeeze=False); im=None
    for r,area in enumerate(areas):
        adf=cell_df[cell_df["canonicalArea"]==area].copy(); matrix=adf[cols].to_numpy(float) if len(adf) else np.empty((0,len(cols)))
        if matrix.size==0:
            for ax in axes[r]: ax.text(0.5,0.5,"No cells",transform=ax.transAxes,ha="center"); ax.set_axis_off()
            continue
        denom=np.nanmax(np.abs(matrix),axis=1); good=np.isfinite(denom)&(denom>0); matrix=matrix[good]; adf=adf.iloc[np.where(good)[0]].copy(); norm=matrix/denom[good,None]
        rank_fi=np.abs(pd.to_numeric(adf["fade_in_vs_fade_out_selectivity"],errors="coerce").to_numpy(float)); rank_am=pd.to_numeric(adf["am_rate_lifetime_sparseness"],errors="coerce").to_numpy(float)
        orders=[np.argsort(np.nan_to_num(rank_fi,nan=-np.inf))[::-1],np.argsort(np.nan_to_num(rank_am,nan=-np.inf))[::-1]]
        for c,(ordr,ttl) in enumerate(zip(orders,["sorted by |FI/FO selectivity|","sorted by AM lifetime sparseness"])):
            im=axes[r,c].imshow(norm[ordr],aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm")
            axes[r,c].set_xticks(np.arange(len(labels)),labels,rotation=30,ha="right"); axes[r,c].set_ylabel(f"{area} {cell_class} cells"); axes[r,c].set_title(ttl)
    fig.suptitle(f"{cell_class.upper()} condition-response rasters — {depth_label}\n{suffix.replace('_',' ')}",y=1.01)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Normalized condition response",shrink=0.75)
    fig.tight_layout(); fig.savefig(output_dir/f"selectivity_rasters_{suffix}_FI_FO_AND_AM_SELECTIVITY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def make_metric_figures(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    areas: list[str],
    cell_class: str,
    depth_label: str,
    output_dir: Path,
    responsive_only: bool,
    stats_out: dict[str,Any] | None = None,
) -> None:
    suffix = "FDR_responsive_only" if responsive_only else "all_cells"
    subset_label = "FDR sound-responsive cells only" if responsive_only else "All classified cells"
    cdf = cell_df[cell_df["sound_responsive_fdr"].astype(bool)].copy() if responsive_only else cell_df.copy()
    sdf = aggregate_sessions(cdf) if len(cdf) else pd.DataFrame(columns=session_df.columns)
    current_stats = run_statistics(cdf,sdf,areas) if len(cdf) else {"continuous":{},"binary":{}}

    plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,
        output_dir/f"cross_area_response_metrics_{suffix}_with_cells.png",mode="with_cells",subset_label=subset_label)
    # Existing MEAN_SEM_ONLY name retained, now using the session-aware convention.
    plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,
        output_dir/f"cross_area_response_metrics_{suffix}_MEAN_SEM_ONLY.png",mode="session_mean",subset_label=subset_label)
    if len(sdf):
        plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,
            output_dir/f"cross_area_response_metrics_{suffix}_SESSION_MEAN_SEM_ONLY.png",mode="session_mean",subset_label=subset_label)

    plot_condition_profiles(cdf,areas,cell_class,depth_label,output_dir,suffix=suffix)
    plot_selectivity_rasters(cdf,areas,cell_class,depth_label,output_dir,suffix=suffix)
    plot_standalone_selectivity_across_areas(cdf,sdf,areas,cell_class,depth_label,output_dir,suffix,current_stats)
    plot_am_rate_profiles_sessions_top_cells(cdf,areas,cell_class,depth_label,output_dir,suffix)
    plot_additional_selectivity_rasters(cdf,areas,cell_class,depth_label,output_dir,suffix)

def add_layer_columns(df: pd.DataFrame) -> pd.DataFrame:
    out=df.copy(); depth=pd.to_numeric(out["depth"],errors="coerce")
    out["layer_key"]=np.where((depth>=100)&(depth<300),"L23",np.where((depth>=300)&(depth<=600),"L45",None))
    out["layer_label"]=out["layer_key"].map({"L23":"L2/3","L45":"L4/5"})
    out["area_layer"]=np.where(out["layer_key"].notna(),out["canonicalArea"].astype(str)+"-"+out["layer_label"].astype(str),None)
    return out


def area_layer_order(areas: list[str]) -> list[str]:
    return [f"{a}-L2/3" for a in areas]+[f"{a}-L4/5" for a in areas]


def run_area_layer_statistics(cell_df: pd.DataFrame, session_df: pd.DataFrame, categories: list[str]) -> dict[str,Any]:
    out={"continuous":{},"binary":{}}
    for metric,cfg in CONTINUOUS_METRICS.items():
        if metric not in cell_df: continue
        pooled={c:cell_df.loc[cell_df["area_layer"]==c,metric] for c in categories}
        sess={c:session_df.loc[session_df["area_layer"]==c,metric] for c in categories}
        out["continuous"][metric]={
            "label":cfg["label"],
            "pooled_cell_exploratory":{"omnibus_kruskal":safe_kruskal(pooled),"pairwise_mannwhitney_holm":pairwise_area_tests(pooled,categories)},
            "session_level_primary":{"omnibus_kruskal":safe_kruskal(sess),"pairwise_mannwhitney_holm":pairwise_area_tests(sess,categories)},
        }
    return out


def plot_area_layer_metric(cell_df,session_df,categories,cell_class,metric,output_dir,suffix,stats_out):
    if metric not in cell_df: return
    ref=CONTINUOUS_METRICS[metric]["reference"]; rng=np.random.default_rng(1827); x=np.arange(len(categories),dtype=float)
    # Cell points.
    fig,ax=plt.subplots(figsize=(11,6.2)); display=[]
    for xi,cat in enumerate(categories):
        vals=finite_values(cell_df.loc[cell_df["area_layer"]==cat,metric])
        if len(vals):
            area=cat.split('-')[0]; ax.scatter(np.full(len(vals),xi)+rng.uniform(-0.08,0.08,len(vals)),vals,s=16,alpha=0.20,color=AREA_COLORS.get(area,'0.4'),edgecolors='none')
            m,_,se,n=mean_sd_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt='o',ms=8,elinewidth=2,capsize=5,color=AREA_COLORS.get(area,'0.4'))
            display.extend(vals.tolist())
    if ref is not None: ax.axhline(ref,ls='--',lw=1,color='0.45')
    p=stats_out.get('continuous',{}).get(metric,{}).get('pooled_cell_exploratory',{}).get('omnibus_kruskal',{}).get('p',np.nan)
    ax.set_xticks(x,categories,rotation=30,ha='right'); ax.set_ylabel(CONTINUOUS_METRICS[metric]['label']); ax.grid(axis='y',alpha=0.2); ax.spines[['top','right']].set_visible(False)
    ax.set_title(f"{cell_class.upper()} across area x layer\n{CONTINUOUS_METRICS[metric]['label']} — {suffix.replace('_',' ')}\nindividual cells; exploratory omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} across area x layer\n{CONTINUOUS_METRICS[metric]['label']}")
    if metric in {'fade_in_vs_fade_out_selectivity','fade_in_vs_best_am_selectivity','am_rate_lifetime_sparseness'}: ax.text(0.5,-0.22,_selectivity_equation(metric),transform=ax.transAxes,ha='center',va='top',fontsize=9)
    ylim=_robust_cell_ylim(display,ref)
    if ylim: ax.set_ylim(*ylim)
    fig.subplots_adjust(bottom=0.28); fig.savefig(output_dir/f"area_layer_{metric}_{suffix}_CELL_POINTS.png",dpi=DPI,bbox_inches='tight'); plt.close(fig)

    # Session points.
    fig,ax=plt.subplots(figsize=(11,6.2)); display=[]
    for xi,cat in enumerate(categories):
        sdf=session_df[session_df['area_layer']==cat]; area=cat.split('-')[0]; offsets=np.linspace(-0.06,0.06,max(len(sdf),1))
        for off,(_,row) in zip(offsets,sdf.iterrows()):
            m=float(row.get(metric,np.nan)); sd=float(row.get(f'sd_{metric}',np.nan))
            if np.isfinite(m):
                ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt='o',ms=3.8,elinewidth=0.7,capsize=2,color=AREA_COLORS.get(area,'0.4'),alpha=0.28)
                display.append(m); 
                if np.isfinite(sd): display.extend([m-sd,m+sd])
        vals=finite_values(sdf[metric]) if metric in sdf else np.array([]); m,_,se,n=mean_sd_sem(vals)
        if np.isfinite(m):
            ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt='o',ms=10,elinewidth=2.6,capsize=6,color=AREA_COLORS.get(area,'0.4'),zorder=5)
            ax.annotate(f"{m:.3g} +/- {se:.2g}\nn={n}" if np.isfinite(se) else f"{m:.3g}\nn={n}",(xi,m),xytext=(0,10),textcoords='offset points',ha='center',fontsize=7,color=AREA_COLORS.get(area,'0.4'))
    if ref is not None: ax.axhline(ref,ls='--',lw=1,color='0.45')
    p=stats_out.get('continuous',{}).get(metric,{}).get('session_level_primary',{}).get('omnibus_kruskal',{}).get('p',np.nan)
    ax.set_xticks(x,categories,rotation=30,ha='right'); ax.set_ylabel(CONTINUOUS_METRICS[metric]['label']); ax.grid(axis='y',alpha=0.2); ax.spines[['top','right']].set_visible(False)
    ax.set_title(f"{cell_class.upper()} across area x layer\n{CONTINUOUS_METRICS[metric]['label']} — {suffix.replace('_',' ')}\nlight=session mean +/- SD; dark=overall mean +/- SEM; omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} across area x layer\n{CONTINUOUS_METRICS[metric]['label']} — session points")
    if metric in {'fade_in_vs_fade_out_selectivity','fade_in_vs_best_am_selectivity','am_rate_lifetime_sparseness'}: ax.text(0.5,-0.22,_selectivity_equation(metric),transform=ax.transAxes,ha='center',va='top',fontsize=9)
    ylim=_robust_cell_ylim(display,ref)
    if ylim: ax.set_ylim(*ylim)
    fig.subplots_adjust(bottom=0.28); fig.savefig(output_dir/f"area_layer_{metric}_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches='tight'); plt.close(fig)


def make_area_layer_outputs(all_cells,areas,out_root):
    layered=add_layer_columns(all_cells); layered=layered[layered['layer_key'].notna()].copy(); categories=area_layer_order(areas)
    root=out_root/'area_by_layer'; root.mkdir(parents=True,exist_ok=True)
    layered.to_csv(root/'all_area_layer_cells.csv',index=False)
    for cell_class in CELL_CLASSES:
        class_cells=layered[layered['cell_class']==cell_class].copy(); class_out=root/cell_class; class_out.mkdir(parents=True,exist_ok=True)
        session_df=aggregate_sessions(class_cells)
        if len(session_df):
            session_df=add_layer_columns(session_df)
        class_cells.to_csv(class_out/'cell_results.csv',index=False); session_df.to_csv(class_out/'session_summary.csv',index=False)
        for responsive_only in [False,True]:
            suffix='FDR_responsive_only' if responsive_only else 'all_cells'
            cdf=class_cells[class_cells['sound_responsive_fdr'].astype(bool)].copy() if responsive_only else class_cells.copy()
            sdf=aggregate_sessions(cdf) if len(cdf) else pd.DataFrame()
            if len(sdf): sdf=add_layer_columns(sdf)
            stats_out=run_area_layer_statistics(cdf,sdf,categories) if len(cdf) else {'continuous':{},'binary':{}}
            save_json(class_out/f'area_layer_statistics_{suffix}.json',stats_out)
            # Full metric set plus dedicated selectivity metrics.
            for metric in CONTINUOUS_METRICS:
                plot_area_layer_metric(cdf,sdf,categories,cell_class,metric,class_out,suffix,stats_out)
        write_figure_index(class_out)


def write_figure_index(output_dir: Path) -> None:
    pngs = sorted(output_dir.glob("*.png"))
    lines = ["FIGURE INDEX", "============", ""]
    for p in pngs:
        lines.append(p.name)
    (output_dir / "FIGURE_INDEX.txt").write_text("\n".join(lines) + "\n")


def write_report(
    path: Path,
    subject: str,
    dates: list[str],
    cell_class: str,
    depth_label: str,
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    areas: list[str],
    stats_out: dict[str, Any],
) -> None:
    lines = []
    lines.append("CROSS-AREA SOUND-TUNING ANALYSIS")
    lines.append("=" * 78)
    lines.append(f"Subject: {subject}")
    lines.append(f"Dates: {', '.join(dates)}")
    lines.append(f"Cell class: {cell_class.upper()}")
    lines.append(f"Depth stratum: {depth_label}")
    lines.append("")
    lines.append("Counts:")
    for area in areas:
        adf = cell_df[cell_df["canonicalArea"] == area]
        sdf = session_df[session_df["canonicalArea"] == area]
        lines.append(f"  {area}: {len(adf)} cells from {sdf['session_key'].nunique() if len(sdf) else 0} sessions")
    lines.append("")
    lines.append("PRIMARY INFERENCE: one summary value per imaging session")
    lines.append("Pooled-cell tests are exploratory/descriptive because cells within a session are not independent replicates.")
    lines.append("")

    for metric, result in stats_out["continuous"].items():
        lines.append(result["label"])
        lines.append("-" * len(result["label"]))
        primary = result["session_level_primary"]
        omni = primary["omnibus_kruskal"]
        lines.append(f"Session-level omnibus Kruskal-Wallis: H={omni['H']:.4g}  {p_text(omni['p'])}" if np.isfinite(omni["H"]) else "Session-level omnibus Kruskal-Wallis: unavailable")
        for area in areas:
            s = primary["summary"][area]
            lines.append(f"  {area}: mean={s['mean']:.4g}, SEM={s['sem']:.4g}, median={s['median']:.4g}, n_sessions={s['n_sessions']}")
        for key, rec in primary["pairwise_mannwhitney_holm"].items():
            lines.append(
                f"  {rec['area1']} vs {rec['area2']}: U={rec['U']:.4g}, p={rec['p']:.4g}, "
                f"Holm p={rec['p_holm']:.4g}, Cliff delta={rec['cliffs_delta']:.3g}"
                if np.isfinite(rec["U"])
                else f"  {rec['area1']} vs {rec['area2']}: unavailable"
            )
        lines.append("")

    for metric, result in stats_out["binary"].items():
        lines.append(result["label"])
        lines.append("-" * len(result["label"]))
        primary = result["session_level_primary"]
        omni = primary["omnibus_kruskal"]
        lines.append(f"Session-level omnibus Kruskal-Wallis: H={omni['H']:.4g}  {p_text(omni['p'])}" if np.isfinite(omni["H"]) else "Session-level omnibus Kruskal-Wallis: unavailable")
        for area in areas:
            s = primary["summary"][area]
            lines.append(f"  {area}: {s['mean_percent']:.3g} ± {s['sem_percent']:.3g}% across n={s['n_sessions']} sessions")
        lines.append("")

    path.write_text("\n".join(lines) + "\n")


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

    print("=" * 78)
    print("SOUND_TUNING CROSS-AREA CELL-CLASS ANALYSIS")
    print("=" * 78)
    print(f"Subject: {subject}")
    print(f"Dates:   {', '.join(dates)}")
    print(f"Areas:   {', '.join(areas)}")
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

    # Keep only the requested canonical cell classes.
    all_cells = all_cells[all_cells["cell_class"].isin(CELL_CLASSES)].copy()

    manifest = {
        "subject": subject,
        "dates": dates,
        "areas": areas,
        "input_files": {a: str(p) for a, p in in_paths.items()},
        "output_root": str(out_root),
        "depth_strata": {
            "all_depths": "all sessions",
            "L23_100to300um": "100 <= depth < 300 um",
            "L45_300to600um": "300 <= depth <= 600 um",
        },
        "primary_inference": "session-level summaries; unpaired cross-area Kruskal-Wallis and pairwise Mann-Whitney with Holm correction",
        "pooled_cell_inference": "exploratory/descriptive only",
        "area_by_layer_outputs": "additional six-stratum A1/AAF/A2 x L2/3/L4/5 comparisons for each cell class",
    }
    save_json(out_root / "run_manifest.json", manifest)

    # Master combined table makes it easy to inspect provenance later.
    all_cells.to_csv(out_root / "all_areas_combined_cell_results.csv", index=False)

    print("\nLoaded data:")
    for area in areas:
        adf = all_cells[all_cells["canonicalArea"] == area]
        print(f"  {area}: {len(adf)} cells, {adf['session_key'].nunique()} sessions")

    for depth_label in DEPTH_STRATA:
        depth_cells = subset_depth(all_cells, depth_label)
        print("\n" + "-" * 78)
        print(f"Depth stratum: {depth_label}")
        for area in areas:
            adf = depth_cells[depth_cells["canonicalArea"] == area]
            print(f"  {area}: {len(adf)} cells, {adf['session_key'].nunique()} sessions")

        for cell_class in CELL_CLASSES:
            class_cells = depth_cells[depth_cells["cell_class"] == cell_class].copy()
            class_out = out_root / depth_label / cell_class
            class_out.mkdir(parents=True, exist_ok=True)

            session_df = aggregate_sessions(class_cells)
            class_cells.to_csv(class_out / "cell_results.csv", index=False)
            session_df.to_csv(class_out / "session_summary.csv", index=False)

            stats_out = run_statistics(class_cells, session_df, areas)
            save_json(class_out / "statistics.json", stats_out)

            write_report(
                class_out / "REPORT.txt",
                subject, dates, cell_class, depth_label,
                class_cells, session_df, areas, stats_out,
            )

            # Restored responsiveness comparison + mean-only session view.
            plot_responsiveness(class_cells, session_df, areas, cell_class, depth_label, class_out)

            # Full sound-response comparison suite for all cells and FDR-responsive cells only.
            make_metric_figures(
                class_cells, session_df, areas, cell_class, depth_label, class_out,
                responsive_only=False, stats_out=stats_out,
            )
            make_metric_figures(
                class_cells, session_df, areas, cell_class, depth_label, class_out,
                responsive_only=True, stats_out=stats_out,
            )

            write_figure_index(class_out)

            print(
                f"  {cell_class.upper():6s}: {len(class_cells)} cells, "
                f"{session_df['session_key'].nunique() if len(session_df) else 0} sessions -> {class_out}"
            )

    # Additional explicit six-stratum area x layer outputs (A1-L2/3, A1-L4/5, ...),
    # with YELLOW and GREEN analyzed separately.
    make_area_layer_outputs(all_cells, areas, out_root)

    print("\n" + "=" * 78)
    print("DONE")
    print(f"Outputs saved under: {out_root}")
    print("=" * 78)


if __name__ == "__main__":
    main()
