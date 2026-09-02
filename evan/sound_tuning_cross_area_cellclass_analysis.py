#!/usr/bin/env python3
"""
Cross-area comparison of sound-tuning responses within GREEN or YELLOW cells.

This is a follow-up analysis for sound_tuning_area_analysis_v5.py. It does NOT
rerun Suite2p, Cellpose, or event alignment. Instead it loads the already-saved
combined_cell_results.csv files for A1, AAF, and A2 and asks questions such as:

    Do YELLOW cells in A2 have a larger |fade-in| / |fade-out| response ratio
    than YELLOW cells in A1?

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

Expected prerequisite output for each area:
    <TEMP_OUTPUT_PATH>/evan/sound_tuning_area_analysis/<subject>/<area>/<dates>/
        combined/combined_cell_results.csv

Example
-------
python sound_tuning_cross_area_cellclass_analysis.py imag039 \
    --dates 20260729 20260730

Optional dry run:
python sound_tuning_cross_area_cellclass_analysis.py imag039 \
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
        help="Dates used for the v5 area analyses, e.g. 20260729 20260730.",
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
    rows = []
    group_cols = ["subject", "date", "session", "session_key", "canonicalArea", "brainArea", "depth", "cell_class"]

    for keys, sdf in df.groupby(group_cols, dropna=False):
        row = dict(zip(group_cols, keys))
        row["n_cells"] = int(len(sdf))
        row["n_sound_responsive_fdr"] = int(sdf["sound_responsive_fdr"].astype(bool).sum())
        row["pct_sound_responsive_fdr"] = 100.0 * row["n_sound_responsive_fdr"] / len(sdf) if len(sdf) else np.nan
        row["pct_sound_excited_fdr"] = 100.0 * float(sdf["sound_excited_fdr"].astype(bool).mean()) if len(sdf) else np.nan
        row["pct_sound_suppressed_fdr"] = 100.0 * float(sdf["sound_suppressed_fdr"].astype(bool).mean()) if len(sdf) else np.nan

        for metric, cfg in CONTINUOUS_METRICS.items():
            vals = finite_values(sdf[metric])
            if len(vals) == 0:
                value = np.nan
            elif cfg["session_agg"] == "median":
                value = float(np.median(vals))
            else:
                value = float(np.mean(vals))
            row[metric] = value

        # AM rates are also summarized per session when present.
        for col in sorted(c for c in sdf.columns if c.startswith("am_response_") and c.endswith("Hz")):
            vals = finite_values(sdf[col])
            row[col] = float(np.mean(vals)) if len(vals) else np.nan

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

    # Pooled cell percentages.
    fig, ax = plt.subplots(figsize=(9, 5.5))
    width = 0.22
    x = np.arange(len(metrics))
    for ai, area in enumerate(areas):
        vals = []
        for cell_col, _, _ in metrics:
            adf = cell_df[cell_df["canonicalArea"] == area]
            vals.append(100.0 * adf[cell_col].astype(bool).mean() if len(adf) else np.nan)
        ax.bar(x + (ai-(len(areas)-1)/2)*width, vals, width=width,
               color=AREA_COLORS[area], alpha=0.82, label=area)
        for xx, yy in zip(x + (ai-(len(areas)-1)/2)*width, vals):
            if np.isfinite(yy):
                ax.text(xx, yy, f"{yy:.1f}%", ha="center", va="bottom", fontsize=8, rotation=90)
    ax.set_xticks(x, [m[2] for m in metrics])
    ax.set_ylabel("Cells (%)")
    ax.set_ylim(0, max(5, min(100, ax.get_ylim()[1]*1.15)))
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\npooled-cell descriptive percentages")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "responsiveness_pooled_cell_percentages.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)

    # Session-level mean percentages ± SEM, no points.
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for ai, area in enumerate(areas):
        means, sems, ns = [], [], []
        for _, pct_col, _ in metrics:
            m, se, n = mean_sem(session_df.loc[session_df["canonicalArea"] == area, pct_col])
            means.append(m); sems.append(se); ns.append(n)
        xx = x + (ai-(len(areas)-1)/2)*width
        ax.errorbar(xx, means, yerr=sems, fmt="o", ms=8, capsize=5, lw=2,
                    color=AREA_COLORS[area], label=area)
        for xxx, m, se, n in zip(xx, means, sems, ns):
            if np.isfinite(m):
                se_txt = f"{se:.1f}" if np.isfinite(se) else "n/a"
                ax.text(xxx, m, f"{m:.1f}±{se_txt}\nn={n}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x, [m[2] for m in metrics])
    ax.set_ylabel("Session percentage (%)")
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\nSESSION mean ± SEM")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "responsiveness_session_mean_sem_only.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


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
    cols, labels = condition_columns(cell_df)
    if not cols:
        return

    # Mean ± SEM profile, no individual points.
    fig, ax = plt.subplots(figsize=(9, 5.7))
    x = np.arange(len(cols))
    all_means, all_sems = [], []
    annotations = []
    for area in areas:
        means, sems, ns = [], [], []
        for col in cols:
            m, se, n = mean_sem(cell_df.loc[cell_df["canonicalArea"] == area, col])
            means.append(m); sems.append(se); ns.append(n)
        all_means.extend(means); all_sems.extend(sems)
        ax.errorbar(x, means, yerr=sems, marker="o", capsize=4, lw=2,
                    color=AREA_COLORS[area], label=area)
        annotations.append((area, means, sems, ns))

    ylim = optimized_ylim_from_summary(np.asarray(all_means), np.asarray(all_sems), [0.0])
    if ylim:
        ax.set_ylim(*ylim)
    ax.axhline(0, ls="--", lw=1, color="0.45")
    ax.set_xticks(x, labels, rotation=30, ha="right")
    ax.set_ylabel("Response (dF/F)")
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\n{suffix.replace('_',' ')}: mean ± SEM")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)

    # Compact numeric table-like annotation inside plot.
    text_lines = []
    for area, means, sems, ns in annotations:
        pieces = []
        for lab, m, se, n in zip(labels, means, sems, ns):
            if np.isfinite(m):
                pieces.append(f"{lab} {m:.3g}±{se:.2g} (n={n})" if np.isfinite(se) else f"{lab} {m:.3g} (n={n})")
        text_lines.append(area + ": " + "; ".join(pieces))
    ax.text(0.01, 0.01, "\n".join(text_lines), transform=ax.transAxes,
            ha="left", va="bottom", fontsize=6.8,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.72, edgecolor="0.8"))

    fig.tight_layout()
    fig.savefig(output_dir / f"condition_response_profile_{suffix}_MEAN_SEM_ONLY.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


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
    """Eight core sound-response comparisons in one 2x4 figure."""
    metrics = list(CONTINUOUS_METRICS.keys())
    fig, axes = plt.subplots(2, 4, figsize=(19, 9.5))
    axes = axes.ravel()
    rng = np.random.default_rng(0)

    for ax, metric in zip(axes, metrics):
        cfg = CONTINUOUS_METRICS[metric]
        ref = cfg["reference"]
        x = np.arange(len(areas))

        means, sems, ns = [], [], []
        source = session_df if mode == "session_mean" else cell_df
        for area in areas:
            vals = finite_values(source.loc[source["canonicalArea"] == area, metric])
            m, se, n = mean_sem(vals)
            means.append(m); sems.append(se); ns.append(n)
            xi = areas.index(area)

            if mode == "with_cells" and len(vals):
                jitter = rng.normal(0, 0.055, len(vals))
                ax.scatter(np.full(len(vals), xi)+jitter, vals, s=10, alpha=0.20,
                           color=AREA_COLORS[area], edgecolors="none")

            if np.isfinite(m):
                ax.errorbar(xi, m, yerr=se if np.isfinite(se) else None,
                            fmt="o", ms=7, capsize=4, lw=1.8, color=AREA_COLORS[area])

        means = np.asarray(means, float); sems = np.asarray(sems, float)
        if ref is not None:
            ax.axhline(ref, ls="--", lw=0.9, color="0.45")

        if mode in ("mean_only", "session_mean"):
            ylim = optimized_ylim_from_summary(means, sems, [ref] if ref is not None else None)
            if ylim:
                ax.set_ylim(*ylim)
            ytop = ax.get_ylim()[1] - 0.03*(ax.get_ylim()[1]-ax.get_ylim()[0])
            for xi, area, m, se, n in zip(x, areas, means, sems, ns):
                annotate_mean_sem(ax, xi, m, se, n, AREA_COLORS[area], y_top=ytop)
        else:
            vals_all = finite_values(source[metric])
            if len(vals_all) >= 4:
                q1, q3 = np.percentile(vals_all, [25, 75]); iqr = q3-q1
                if np.isfinite(iqr) and iqr > 0:
                    inliers = vals_all[(vals_all >= q1-3*iqr) & (vals_all <= q3+3*iqr)]
                    if len(inliers):
                        lo, hi = float(np.min(inliers)), float(np.max(inliers))
                        if ref is not None:
                            lo, hi = min(lo, ref), max(hi, ref)
                        span = hi-lo if hi > lo else max(abs(lo),1.0)*0.25
                        ax.set_ylim(lo-.08*span, hi+.14*span)

        ax.set_xticks(x, areas)
        ax.set_title(cfg["label"], fontsize=10)
        ax.grid(axis="y", alpha=0.22)

    mode_title = {
        "with_cells": "cell distributions + mean ± SEM",
        "mean_only": "cell mean ± SEM; individual cells not shown",
        "session_mean": "SESSION mean ± SEM; one summary per imaging session",
    }[mode]
    fig.suptitle(
        f"{cell_class.upper()} cells across A1 / AAF / A2 — {depth_label}\n{subset_label}: {mode_title}",
        fontsize=14,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def make_metric_figures(
    cell_df: pd.DataFrame,
    session_df: pd.DataFrame,
    areas: list[str],
    cell_class: str,
    depth_label: str,
    output_dir: Path,
    responsive_only: bool,
) -> None:
    suffix = "FDR_responsive_only" if responsive_only else "all_cells"
    subset_label = "FDR sound-responsive cells only" if responsive_only else "All classified cells"
    cdf = cell_df[cell_df["sound_responsive_fdr"].astype(bool)].copy() if responsive_only else cell_df.copy()
    sdf = aggregate_sessions(cdf) if len(cdf) else pd.DataFrame(columns=session_df.columns)

    plot_metric_grid(
        cdf, sdf, areas, cell_class, depth_label,
        output_dir / f"cross_area_response_metrics_{suffix}_with_cells.png",
        mode="with_cells", subset_label=subset_label,
    )
    plot_metric_grid(
        cdf, sdf, areas, cell_class, depth_label,
        output_dir / f"cross_area_response_metrics_{suffix}_MEAN_SEM_ONLY.png",
        mode="mean_only", subset_label=subset_label,
    )
    if len(sdf):
        plot_metric_grid(
            cdf, sdf, areas, cell_class, depth_label,
            output_dir / f"cross_area_response_metrics_{suffix}_SESSION_MEAN_SEM_ONLY.png",
            mode="session_mean", subset_label=subset_label,
        )

    plot_condition_profiles(cdf, areas, cell_class, depth_label, output_dir, suffix=suffix)
    plot_selectivity_rasters(cdf, areas, cell_class, depth_label, output_dir, suffix=suffix)

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
                responsive_only=False,
            )
            make_metric_figures(
                class_cells, session_df, areas, cell_class, depth_label, class_out,
                responsive_only=True,
            )

            write_figure_index(class_out)

            print(
                f"  {cell_class.upper():6s}: {len(class_cells)} cells, "
                f"{session_df['session_key'].nunique() if len(session_df) else 0} sessions -> {class_out}"
            )

    print("\n" + "=" * 78)
    print("DONE")
    print(f"Outputs saved under: {out_root}")
    print("=" * 78)


if __name__ == "__main__":
    main()
