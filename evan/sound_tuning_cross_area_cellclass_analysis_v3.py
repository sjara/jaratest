#!/usr/bin/env python3
"""
Cross-area sound-tuning analysis within YELLOW and GREEN cell classes (v3).

Prerequisite
------------
Run sound_tuning_area_analysis_v13.py for A1, AAF, and A2 using the same
subject/date set.  This script consumes each area's combined_cell_results.csv
and, for YELLOW trial-reduction analyses, the per-session v13 trial-response
archives referenced by trial_response_archive_path.

Scientific structure
--------------------
* YELLOW cells are compared across A1/AAF/A2; GREEN cells are analyzed in a
  separate, identical branch.
* Analyses are repeated for all depths, L2/3 (100 <= depth < 300 um), and
  L4/5 (300 <= depth <= 600 um).
* Primary biological replication is the imaging session.  Cross-area primary
  tests are Kruskal-Wallis on one session summary per area, followed by
  Mann-Whitney pairwise tests with Holm correction.
* Pooled-cell tests are retained only for explicitly exploratory cell-point
  figures.
* FI/FO selectivity is the bounded signed index
      (R_FI - R_FO) / (|R_FI| + |R_FO|).
* FI/best-AM selectivity retains the v13 signed (A-B)/(A+B) definition with
  the v13 cancellation guard.
* Responsive-only analyses use condition-specific v13 populations:
      FI/FO metrics: FI-or-FO responsive cells
      FI/best-AM:    FI and/or >=1 AM-rate responsive cells
      AM metrics:    >=1 AM-rate responsive cells
* Whole-session-median-F0 and 60-s-prestimulus-median-F0 FI/FO analyses are
  sensitivity analyses and are not included in the primary selectivity Holm
  family.

YELLOW trial-reduction robustness
---------------------------------
For every statistically significant PRIMARY session-level YELLOW-across-area
finding, an additional Monte-Carlo robustness figure is generated.  Trial
fractions are 100%, 75%, 50%, and 25% by default.  Reduced trials are sampled
without replacement separately within every session x stimulus condition.
For reduced datasets the script recomputes condition means, FI/FO and
FI/best-AM selectivity, AM lifetime sparseness, and (when needed) the v13-style
condition-specific sign-flip/FDR responsiveness classification.  The same
cross-area multiple-comparison corrections are then re-applied.

The robustness figure reports the distribution of corrected p-values and the
fraction of Monte-Carlo resamples that retain p_adj < 0.05.  Raw and summary
CSV files are saved beside each robustness figure.  The 100% point is the
original v13/full-data result, so it is not contaminated by a second layer of
Monte-Carlo randomness.

Example
-------
python sound_tuning_cross_area_cellclass_analysis_v3.py imag039 \\
    --dates 20260729 20260730

Optional controls
-----------------
--trial-reduction-resamples 500
--trial-reduction-response-permutations 512
--trial-reduction-seed 20260826
--skip-trial-reduction
--dry-run
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
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
    "all_depths": (None, None, "All depths"),
    "L23_100to300um": (100.0, 300.0, "L2/3 (100-<300 um)"),
    "L45_300to600um": (300.0, 600.0, "L4/5 (300-600 um)"),
}

AREA_COLORS = {"A1": "tab:blue", "AAF": "tab:orange", "A2": "tab:green"}
CELL_CLASS_COLORS = {"green": "limegreen", "yellow": "goldenrod"}
DPI = 180
FDR_ALPHA = 0.05
TRIAL_REDUCTION_FRACTIONS = (1.0, 0.75, 0.50, 0.25)
TRIAL_REDUCTION_MIN_TRIALS = 3

RESPONSIVENESS = {
    "sound_responsive_fdr": "Any sound responsive",
    "fade_in_responsive_fdr": "Fade-in responsive",
    "fade_out_responsive_fdr": "Fade-out responsive",
    "fi_or_fo_responsive_fdr": "FI or FO responsive",
    "any_am_rate_responsive_fdr": ">=1 AM-rate responsive",
    "sound_excited_fdr": "Excited",
    "sound_suppressed_fdr": "Suppressed",
}

FI_FO_PRIMARY = "fade_in_vs_fade_out_selectivity"
FI_FO_SESSION_MEDIAN = "fade_in_vs_fade_out_selectivity_session_median_dff"
FI_FO_PRESTIM60 = "fade_in_vs_fade_out_selectivity_60s_prestim_median_dff"
FI_BEST_AM = "fade_in_vs_best_am_selectivity"
AM_SPARSE = "am_rate_lifetime_sparseness"

METRIC_LABELS = {
    FI_FO_PRIMARY: "FI/FO selectivity index",
    FI_FO_SESSION_MEDIAN: "FI/FO selectivity index (whole-session median F0)",
    FI_FO_PRESTIM60: "FI/FO selectivity index (60-s prestimulus median F0)",
    FI_BEST_AM: "FI/best-AM selectivity index",
    AM_SPARSE: "AM-rate lifetime sparseness",
}

SUBSET_LABELS = {
    "all_cells": "all classified cells",
    "fi_fo_responsive": "FI-or-FO responsive cells",
    "fi_am_responsive": "FI and/or >=1-AM responsive cells",
    "am_responsive": ">=1-AM-rate responsive cells",
}

SELECTIVITY_ABS_THRESHOLD = 1e-6
SELECTIVITY_REL_THRESHOLD = 0.10


# =============================================================================
# CLI / PATHS
# =============================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject", help="Subject ID, e.g. imag039")
    p.add_argument("--dates", nargs="+", required=True, help="Dates used in the v13 area analyses")
    p.add_argument("--areas", nargs="+", default=list(AREAS), choices=list(AREAS))
    p.add_argument("--trial-reduction-resamples", type=int, default=500,
                   help="Monte-Carlo resamples at each reduced trial fraction. Default: 500")
    p.add_argument("--trial-reduction-response-permutations", type=int, default=512,
                   help="Sign-flip permutations per condition during reduced-trial responsiveness re-estimation. Default: 512")
    p.add_argument("--trial-reduction-seed", type=int, default=20260826)
    p.add_argument("--skip-trial-reduction", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def date_tag(dates: Iterable[str]) -> str:
    return "_".join(str(d) for d in dates)


def expected_area_csv(subject: str, area: str, dates: list[str]) -> Path:
    return (Path(settings.TEMP_OUTPUT_PATH) / "evan" / "sound_tuning_area_analysis" /
            subject / area / date_tag(dates) / "combined" / "combined_cell_results.csv")


def output_root(subject: str, dates: list[str]) -> Path:
    return (Path(settings.TEMP_OUTPUT_PATH) / "evan" /
            "sound_tuning_cross_area_cellclass_analysis" / subject / date_tag(dates))


# =============================================================================
# GENERIC UTILITIES
# =============================================================================

def json_default(obj: Any) -> Any:
    if isinstance(obj, (np.integer,)): return int(obj)
    if isinstance(obj, (np.floating,)): return None if not np.isfinite(obj) else float(obj)
    if isinstance(obj, (np.bool_,)): return bool(obj)
    if isinstance(obj, np.ndarray): return obj.tolist()
    if isinstance(obj, Path): return str(obj)
    raise TypeError(f"Not JSON serializable: {type(obj)}")


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=json_default, allow_nan=False)


def parse_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1", "yes", "y"])


def finite_values(values: Iterable[Any]) -> np.ndarray:
    x = pd.to_numeric(pd.Series(values), errors="coerce").to_numpy(dtype=float)
    return x[np.isfinite(x)]


def mean_sem(values: Iterable[Any]) -> tuple[float, float, int]:
    x = finite_values(values)
    if len(x) == 0: return np.nan, np.nan, 0
    m = float(np.mean(x))
    se = float(np.std(x, ddof=1) / np.sqrt(len(x))) if len(x) > 1 else np.nan
    return m, se, len(x)


def median_iqr(values: Iterable[Any]) -> tuple[float, float, float, int]:
    x = finite_values(values)
    if len(x) == 0: return np.nan, np.nan, np.nan, 0
    return float(np.median(x)), float(np.percentile(x, 25)), float(np.percentile(x, 75)), len(x)


def holm_adjust(pvalues: Iterable[Any]) -> np.ndarray:
    p = np.asarray(list(pvalues), dtype=float)
    out = np.full(p.shape, np.nan, dtype=float)
    good = np.flatnonzero(np.isfinite(p))
    if len(good) == 0: return out
    vals = p[good]
    order = np.argsort(vals)
    ranked = vals[order]
    m = len(ranked)
    adj = np.maximum.accumulate((m - np.arange(m)) * ranked)
    adj = np.minimum(adj, 1.0)
    restored = np.empty(m, dtype=float)
    restored[order] = adj
    out[good] = restored
    return out


def p_text(p: float) -> str:
    if not np.isfinite(p): return "p=n/a"
    if p < 0.001: return "p<0.001"
    return f"p={p:.3g}"


def pair_key(a: str, b: str) -> str:
    return f"{a}__{b}"


def cliffs_delta(x: Iterable[Any], y: Iterable[Any]) -> float:
    a, b = finite_values(x), finite_values(y)
    if len(a) == 0 or len(b) == 0: return np.nan
    # Efficient enough for the modest cell counts here.
    gt = sum(np.sum(v > b) for v in a)
    lt = sum(np.sum(v < b) for v in a)
    return float((gt - lt) / (len(a) * len(b)))


def safe_mannwhitney(x: Iterable[Any], y: Iterable[Any]) -> dict[str, Any]:
    a, b = finite_values(x), finite_values(y)
    if len(a) == 0 or len(b) == 0:
        return {"U": np.nan, "p": np.nan, "n1": len(a), "n2": len(b), "cliffs_delta": np.nan}
    try:
        r = stats.mannwhitneyu(a, b, alternative="two-sided")
        return {"U": float(r.statistic), "p": float(r.pvalue), "n1": len(a), "n2": len(b),
                "cliffs_delta": cliffs_delta(a, b)}
    except ValueError:
        return {"U": np.nan, "p": np.nan, "n1": len(a), "n2": len(b), "cliffs_delta": np.nan}


def safe_kruskal(groups: dict[str, Iterable[Any]]) -> dict[str, Any]:
    clean = {k: finite_values(v) for k, v in groups.items()}
    usable = [v for v in clean.values() if len(v)]
    if len(usable) < 2:
        return {"H": np.nan, "p": np.nan, "group_ns": {k: len(v) for k, v in clean.items()}}
    try:
        r = stats.kruskal(*usable)
        return {"H": float(r.statistic), "p": float(r.pvalue),
                "group_ns": {k: len(v) for k, v in clean.items()}}
    except ValueError:
        return {"H": np.nan, "p": np.nan, "group_ns": {k: len(v) for k, v in clean.items()}}


def pairwise_area_tests(groups: dict[str, Iterable[Any]], areas: list[str]) -> dict[str, Any]:
    recs, ps = [], []
    for a, b in combinations(areas, 2):
        rec = safe_mannwhitney(groups.get(a, []), groups.get(b, []))
        rec.update({"area1": a, "area2": b})
        recs.append(rec); ps.append(rec["p"])
    adj = holm_adjust(ps)
    out = {}
    for rec, pa in zip(recs, adj):
        rec["p_holm"] = float(pa) if np.isfinite(pa) else np.nan
        out[pair_key(rec["area1"], rec["area2"])] = rec
    return out


def robust_ylim(values: Iterable[Any], reference: float | None = None,
                bounded: bool = False, pad_fraction: float = 0.12) -> tuple[float, float] | None:
    vals = finite_values(values)
    if reference is not None and np.isfinite(reference):
        vals = np.r_[vals, float(reference)]
    if len(vals) == 0: return None
    if bounded:
        lo, hi = float(np.min(vals)), float(np.max(vals))
        span = max(hi - lo, 0.15)
        lo, hi = lo - pad_fraction * span, hi + pad_fraction * span
        return max(-1.05, lo), min(1.05, hi)
    qlo, qhi = np.percentile(vals, [1, 99]) if len(vals) >= 10 else (np.min(vals), np.max(vals))
    span = max(float(qhi - qlo), 1e-6)
    lo, hi = float(qlo - pad_fraction * span), float(qhi + pad_fraction * span)
    if reference is not None:
        lo, hi = min(lo, reference - 0.03 * span), max(hi, reference + 0.03 * span)
    return lo, hi


def add_sig_bars(ax: plt.Axes, pairwise: dict[str, Any], xmap: dict[str, float],
                 alpha: float = 0.05) -> None:
    sig = [r for r in pairwise.values() if np.isfinite(r.get("p_holm", np.nan)) and r["p_holm"] < alpha]
    if not sig: return
    y0, y1 = ax.get_ylim(); span = y1 - y0
    base = y1 - 0.06 * span
    step = 0.065 * span
    for i, r in enumerate(sig):
        a, b = r["area1"], r["area2"]
        if a not in xmap or b not in xmap: continue
        y = base - i * step
        x1, x2 = xmap[a], xmap[b]
        ax.plot([x1, x1, x2, x2], [y-step*0.12, y, y, y-step*0.12], color="0.2", lw=1)
        p = r["p_holm"]
        label = "***" if p < 0.001 else "**" if p < 0.01 else "*"
        ax.text((x1+x2)/2, y+0.006*span, f"{label} {p:.3g}", ha="center", va="bottom", fontsize=8)


def fi_fo_equation() -> str:
    return r"$SI_{FI/FO}=(R_{FI}-R_{FO})/(|R_{FI}|+|R_{FO}|)$"


def fi_best_equation() -> str:
    return r"$SI_{FI/bestAM}=(R_{FI}-R_{bestAM})/(R_{FI}+R_{bestAM})$ (v13 cancellation guard)"


def am_sparse_equation() -> str:
    return r"$S_{life}=\frac{1-(\bar{R}^{2}/\overline{R^{2}})}{1-1/N}$"


# =============================================================================
# LOADING / SUBSETS / SESSION SUMMARIES
# =============================================================================

def _am_primary_columns(df: pd.DataFrame) -> list[tuple[float, str]]:
    out = []
    for c in df.columns:
        if not (c.startswith("am_response_") and c.endswith("Hz")): continue
        if c.endswith("_session_median_dff") or c.endswith("_60s_prestim_median_dff"): continue
        token = c[len("am_response_"):-2]
        try: rate = float(token)
        except ValueError: continue
        out.append((rate, c))
    return sorted(out, key=lambda z: z[0])


def load_area_tables(subject: str, dates: list[str], areas: list[str]) -> pd.DataFrame:
    frames, missing = [], []
    for area in areas:
        path = expected_area_csv(subject, area, dates)
        if not path.exists():
            missing.append(path); continue
        df = pd.read_csv(path)
        if "canonicalArea" not in df:
            raise ValueError(f"{path} lacks canonicalArea")
        bad = set(df["canonicalArea"].dropna().astype(str).unique()) - {area}
        if bad: raise ValueError(f"{path} contains unexpected areas: {sorted(bad)}")
        frames.append(df)
    if missing:
        raise FileNotFoundError(
            "Missing prerequisite v13 output(s):\n" + "\n".join(f"  {p}" for p in missing) +
            "\nRun sound_tuning_area_analysis_v13.py for each missing area first."
        )
    if not frames: raise RuntimeError("No area tables loaded")
    df = pd.concat(frames, ignore_index=True, sort=False)
    required = {
        "subject", "date", "session", "session_key", "canonicalArea", "brainArea", "depth",
        "cell_class", "trial_response_archive_path",
        "sound_responsive_fdr", "fade_in_responsive_fdr", "fade_out_responsive_fdr",
        "fi_or_fo_responsive_fdr", "any_am_rate_responsive_fdr", "fi_or_any_am_responsive_fdr",
        "sound_excited_fdr", "sound_suppressed_fdr",
        "fade_in_response", "fade_out_response", FI_FO_PRIMARY, FI_BEST_AM, AM_SPARSE,
        FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60,
    }
    miss = sorted(required - set(df.columns))
    if miss:
        raise ValueError("Combined cell table(s) are missing v13-required columns: " + ", ".join(miss))
    df["depth"] = pd.to_numeric(df["depth"], errors="coerce")
    for c in set(RESPONSIVENESS) | {"fi_or_any_am_responsive_fdr"}:
        df[c] = parse_bool_series(df[c])
    df = df[df["cell_class"].isin(CELL_CLASSES)].copy()
    return df


def subset_depth(df: pd.DataFrame, stratum: str) -> pd.DataFrame:
    low, high, _ = DEPTH_STRATA[stratum]
    if low is None: return df.copy()
    d = pd.to_numeric(df["depth"], errors="coerce")
    if stratum.startswith("L23"):
        return df[(d >= low) & (d < high)].copy()
    return df[(d >= low) & (d <= high)].copy()


def analysis_subset(df: pd.DataFrame, kind: str) -> pd.DataFrame:
    if kind == "all_cells": return df.copy()
    if kind == "fi_fo_responsive": return df[df["fi_or_fo_responsive_fdr"].astype(bool)].copy()
    if kind == "fi_am_responsive": return df[df["fi_or_any_am_responsive_fdr"].astype(bool)].copy()
    if kind == "am_responsive": return df[df["any_am_rate_responsive_fdr"].astype(bool)].copy()
    raise KeyError(kind)


def session_metric_table(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    rows = []
    if "session_key" not in df.columns or "canonicalArea" not in df.columns:
        return pd.DataFrame(columns=["session_key", "canonicalArea", "value", "n_cells"])
    for (sk, area), sdf in df.groupby(["session_key", "canonicalArea"], dropna=False):
        vals = finite_values(sdf[metric]) if metric in sdf else np.array([])
        rows.append({"session_key": str(sk), "canonicalArea": str(area), "value": float(np.mean(vals)) if len(vals) else np.nan,
                     "n_cells": int(len(vals))})
    return pd.DataFrame(rows, columns=["session_key", "canonicalArea", "value", "n_cells"])


def session_percentage_table(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    rows = []
    if "session_key" not in df.columns or "canonicalArea" not in df.columns or metric not in df.columns:
        return pd.DataFrame(columns=["session_key", "canonicalArea", "value", "n_cells"])
    for (sk, area), sdf in df.groupby(["session_key", "canonicalArea"], dropna=False):
        vals = parse_bool_series(sdf[metric]).to_numpy(dtype=float)
        rows.append({"session_key": str(sk), "canonicalArea": str(area),
                     "value": 100.0 * float(np.mean(vals)) if len(vals) else np.nan,
                     "n_cells": int(len(vals))})
    return pd.DataFrame(rows, columns=["session_key", "canonicalArea", "value", "n_cells"])


def aggregate_sessions(df: pd.DataFrame) -> pd.DataFrame:
    numeric = [FI_FO_PRIMARY, FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60, FI_BEST_AM, AM_SPARSE,
               "fade_in_response", "fade_out_response"] + [c for _, c in _am_primary_columns(df)]
    rows = []
    for keys, sdf in df.groupby(["subject", "date", "session", "session_key", "canonicalArea", "brainArea", "depth", "cell_class"], dropna=False):
        row = dict(zip(["subject", "date", "session", "session_key", "canonicalArea", "brainArea", "depth", "cell_class"], keys))
        row["n_cells"] = int(len(sdf))
        for c in numeric:
            vals = finite_values(sdf[c]) if c in sdf else np.array([])
            row[c] = float(np.mean(vals)) if len(vals) else np.nan
        for b in RESPONSIVENESS:
            vals = parse_bool_series(sdf[b]).to_numpy(dtype=float)
            row[f"pct_{b}"] = 100.0 * float(np.mean(vals)) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


# =============================================================================
# PRIMARY SESSION-LEVEL STATISTICS
# =============================================================================

def _session_cross_area_stat(tab: pd.DataFrame, areas: list[str]) -> dict[str, Any]:
    groups = {a: tab.loc[tab["canonicalArea"] == a, "value"] for a in areas}
    summary = {}
    for a in areas:
        m, se, n = mean_sem(groups[a]); med, q1, q3, _ = median_iqr(groups[a])
        summary[a] = {"mean": m, "sem": se, "median": med, "q1": q1, "q3": q3, "n_sessions": n}
    return {"summary": summary, "omnibus": safe_kruskal(groups), "pairwise": pairwise_area_tests(groups, areas)}


def _pooled_cross_area_stat(df: pd.DataFrame, metric: str, areas: list[str]) -> dict[str, Any]:
    groups = {a: df.loc[df["canonicalArea"] == a, metric] for a in areas}
    summary = {}
    for a in areas:
        m, se, n = mean_sem(groups[a]); med, q1, q3, _ = median_iqr(groups[a])
        summary[a] = {"mean": m, "sem": se, "median": med, "q1": q1, "q3": q3, "n_cells": n}
    return {"summary": summary, "omnibus": safe_kruskal(groups), "pairwise": pairwise_area_tests(groups, areas)}


def _apply_family_holm(stats_dict: dict[str, Any]) -> None:
    keys = list(stats_dict)
    p = [stats_dict[k]["session_level_primary"]["omnibus"]["p"] for k in keys]
    adj = holm_adjust(p)
    for k, pa in zip(keys, adj):
        stats_dict[k]["session_level_primary"]["omnibus"]["p_holm_family"] = float(pa) if np.isfinite(pa) else np.nan


def build_primary_stats(cells: pd.DataFrame, areas: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {"responsiveness": {}, "selectivity": {}, "condition_profiles": {}}

    # Responsiveness: seven session-percentage tests; Holm across seven omnibus tests.
    for metric, label in RESPONSIVENESS.items():
        tab = session_percentage_table(cells, metric)
        out["responsiveness"][metric] = {"label": label, "session_level_primary": _session_cross_area_stat(tab, areas)}
    rkeys = list(out["responsiveness"])
    radj = holm_adjust([out["responsiveness"][k]["session_level_primary"]["omnibus"]["p"] for k in rkeys])
    for k, pa in zip(rkeys, radj):
        out["responsiveness"][k]["session_level_primary"]["omnibus"]["p_holm_family"] = float(pa) if np.isfinite(pa) else np.nan

    # Selectivity families. AM sparseness has no primary session-level inference by design.
    for subset_name, subset_kind in [("all_cells", "all_cells"), ("responsive_only", "fi_fo_responsive")]:
        out["selectivity"][subset_name] = {}
        base = analysis_subset(cells, subset_kind)
        # FI/FO primary.
        out["selectivity"][subset_name][FI_FO_PRIMARY] = {
            "label": METRIC_LABELS[FI_FO_PRIMARY],
            "session_level_primary": _session_cross_area_stat(session_metric_table(base, FI_FO_PRIMARY), areas),
        }
        # FI/best-AM uses a different responsive subset for responsive_only.
        fi_am_df = cells if subset_name == "all_cells" else analysis_subset(cells, "fi_am_responsive")
        out["selectivity"][subset_name][FI_BEST_AM] = {
            "label": METRIC_LABELS[FI_BEST_AM],
            "session_level_primary": _session_cross_area_stat(session_metric_table(fi_am_df, FI_BEST_AM), areas),
        }
        _apply_family_holm(out["selectivity"][subset_name])

        # Alternate FI/FO sensitivity analyses, deliberately not in primary family.
        out["selectivity"][subset_name]["sensitivity"] = {}
        for metric in (FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60):
            if metric in base.columns:
                out["selectivity"][subset_name]["sensitivity"][metric] = {
                    "label": METRIC_LABELS[metric],
                    "session_level_sensitivity": _session_cross_area_stat(session_metric_table(base, metric), areas),
                }

    # Condition-profile families.
    am_cols = _am_primary_columns(cells)
    all_conditions = [("Fade-in", "fade_in_response"), ("Fade-out", "fade_out_response")] + [(f"AM {r:g} Hz", c) for r, c in am_cols]
    families = {
        "all_cells": (cells, all_conditions),
        "responsive_fi_fo": (analysis_subset(cells, "fi_fo_responsive"), all_conditions[:2]),
        "responsive_am": (analysis_subset(cells, "am_responsive"), all_conditions[2:]),
    }
    for fam, (df, conds) in families.items():
        out["condition_profiles"][fam] = {}
        for label, col in conds:
            out["condition_profiles"][fam][col] = {
                "label": label,
                "session_level_primary": _session_cross_area_stat(session_metric_table(df, col), areas),
            }
        keys = list(out["condition_profiles"][fam])
        adj = holm_adjust([out["condition_profiles"][fam][k]["session_level_primary"]["omnibus"]["p"] for k in keys])
        for k, pa in zip(keys, adj):
            out["condition_profiles"][fam][k]["session_level_primary"]["omnibus"]["p_holm_family"] = float(pa) if np.isfinite(pa) else np.nan
    return out


def build_full_stats(cells: pd.DataFrame, areas: list[str]) -> dict[str, Any]:
    out = build_primary_stats(cells, areas)
    out["exploratory_pooled"] = {"selectivity": {}}
    specs = [
        ("all_cells", "all_cells", FI_FO_PRIMARY),
        ("all_cells", "all_cells", FI_FO_SESSION_MEDIAN),
        ("all_cells", "all_cells", FI_FO_PRESTIM60),
        ("all_cells", "all_cells", FI_BEST_AM),
        ("all_cells", "all_cells", AM_SPARSE),
        ("responsive_only", "fi_fo_responsive", FI_FO_PRIMARY),
        ("responsive_only", "fi_fo_responsive", FI_FO_SESSION_MEDIAN),
        ("responsive_only", "fi_fo_responsive", FI_FO_PRESTIM60),
        ("responsive_only", "fi_am_responsive", FI_BEST_AM),
        ("responsive_only", "am_responsive", AM_SPARSE),
    ]
    for branch, subset, metric in specs:
        out["exploratory_pooled"]["selectivity"].setdefault(branch, {})[metric] = _pooled_cross_area_stat(analysis_subset(cells, subset), metric, areas)
    return out


# =============================================================================
# PLOTTING
# =============================================================================

def _metric_reference(metric: str) -> float | None:
    return 0.0 if metric in {FI_FO_PRIMARY, FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60, FI_BEST_AM} else None


def _metric_equation(metric: str) -> str:
    if metric in {FI_FO_PRIMARY, FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60}: return fi_fo_equation()
    if metric == FI_BEST_AM: return fi_best_equation()
    if metric == AM_SPARSE: return am_sparse_equation()
    return ""


def plot_cross_area_cell_metric(df: pd.DataFrame, metric: str, areas: list[str], title: str,
                                stats_rec: dict[str, Any], output_path: Path, sensitivity: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(7.6, 6.3)); rng = np.random.default_rng(1827); display = []
    xmap = {a: float(i) for i, a in enumerate(areas)}
    for a in areas:
        vals = finite_values(df.loc[df["canonicalArea"] == a, metric])
        x = xmap[a]
        if len(vals):
            ax.scatter(np.full(len(vals), x) + rng.uniform(-0.09, 0.09, len(vals)), vals,
                       s=20, alpha=0.22, color=AREA_COLORS[a], edgecolors="none")
            m, se, n = mean_sem(vals)
            ax.errorbar(x, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=10,
                        capsize=6, elinewidth=2.3, color=AREA_COLORS[a], zorder=5)
            display.extend(vals.tolist())
    ref = _metric_reference(metric)
    if ref is not None: ax.axhline(ref, ls="--", lw=1, color="0.45")
    bounded = metric in {FI_FO_PRIMARY, FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60}
    ylim = robust_ylim(display, ref, bounded=bounded)
    if ylim: ax.set_ylim(*ylim)
    add_sig_bars(ax, stats_rec.get("pairwise", {}), xmap)
    omni = stats_rec.get("omnibus", {})
    ax.set_xticks(range(len(areas)), areas); ax.set_ylabel(METRIC_LABELS.get(metric, metric))
    tag = "Sensitivity analysis; " if sensitivity else "Exploratory pooled-cell; "
    ax.set_title(title + f"\n{tag}Kruskal-Wallis {p_text(omni.get('p', np.nan))}")
    eq = _metric_equation(metric)
    if eq: ax.text(0.5, -0.16, eq, transform=ax.transAxes, ha="center", va="top", fontsize=9)
    ax.grid(axis="y", alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
    fig.subplots_adjust(bottom=0.22); fig.savefig(output_path, dpi=DPI, bbox_inches="tight"); plt.close(fig)


def plot_cross_area_session_metric(df: pd.DataFrame, metric: str, areas: list[str], title: str,
                                   stats_rec: dict[str, Any], output_path: Path, sensitivity: bool = False) -> None:
    tab = session_metric_table(df, metric)
    fig, ax = plt.subplots(figsize=(7.6, 6.3)); display = []; xmap = {a: float(i) for i, a in enumerate(areas)}
    for a in areas:
        vals = finite_values(tab.loc[tab["canonicalArea"] == a, "value"])
        x = xmap[a]
        offs = np.linspace(-0.065, 0.065, max(len(vals), 1))
        if len(vals):
            ax.scatter(np.full(len(vals), x) + offs, vals, s=30, alpha=0.35, color=AREA_COLORS[a], zorder=2)
            m, se, n = mean_sem(vals)
            ax.errorbar(x, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=11,
                        capsize=7, elinewidth=2.7, color=AREA_COLORS[a], zorder=5)
            ax.annotate(f"n={n}", (x, m), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=8)
            display.extend(vals.tolist())
    ref = _metric_reference(metric)
    if ref is not None: ax.axhline(ref, ls="--", lw=1, color="0.45")
    bounded = metric in {FI_FO_PRIMARY, FI_FO_SESSION_MEDIAN, FI_FO_PRESTIM60}
    ylim = robust_ylim(display, ref, bounded=bounded)
    if ylim: ax.set_ylim(*ylim)
    add_sig_bars(ax, stats_rec.get("pairwise", {}), xmap)
    omni = stats_rec.get("omnibus", {})
    family_p = omni.get("p_holm_family", np.nan)
    if sensitivity:
        stat_line = f"Sensitivity: Kruskal-Wallis {p_text(omni.get('p', np.nan))}"
    else:
        stat_line = f"Session-level Kruskal-Wallis raw {p_text(omni.get('p', np.nan))}; family Holm {p_text(family_p)}"
    ax.set_xticks(range(len(areas)), areas); ax.set_ylabel(METRIC_LABELS.get(metric, metric))
    ax.set_title(title + "\n" + stat_line)
    eq = _metric_equation(metric)
    if eq: ax.text(0.5, -0.16, eq, transform=ax.transAxes, ha="center", va="top", fontsize=9)
    ax.grid(axis="y", alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
    fig.subplots_adjust(bottom=0.22); fig.savefig(output_path, dpi=DPI, bbox_inches="tight"); plt.close(fig)


def plot_responsiveness(cells: pd.DataFrame, stats_out: dict[str, Any], areas: list[str],
                        cell_class: str, depth_label: str, output_dir: Path) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(17, 9.2)); axes = axes.ravel()
    for ax, (metric, label) in zip(axes, RESPONSIVENESS.items()):
        tab = session_percentage_table(cells, metric); display = []; xmap = {a: float(i) for i, a in enumerate(areas)}
        for a in areas:
            vals = finite_values(tab.loc[tab["canonicalArea"] == a, "value"]); x = xmap[a]
            offs = np.linspace(-0.06, 0.06, max(len(vals), 1))
            if len(vals):
                ax.scatter(np.full(len(vals), x)+offs, vals, s=24, alpha=0.30, color=AREA_COLORS[a])
                m, se, n = mean_sem(vals)
                ax.errorbar(x, m, yerr=se if np.isfinite(se) else None, fmt="o", ms=9,
                            capsize=5, elinewidth=2.2, color=AREA_COLORS[a], zorder=5)
                display.extend(vals.tolist())
        rec = stats_out["responsiveness"][metric]["session_level_primary"]
        vals_for_ylim = display + [0.0]
        ylim = robust_ylim(vals_for_ylim, 0.0)
        if ylim:
            ax.set_ylim(max(0.0, ylim[0]), min(100.0, max(ylim[1], 5.0)))
        add_sig_bars(ax, rec["pairwise"], xmap)
        ax.set_xticks(range(len(areas)), areas); ax.set_ylabel("Session percentage (%)")
        ax.set_title(f"{label}\nKW raw {p_text(rec['omnibus']['p'])}; Holm {p_text(rec['omnibus'].get('p_holm_family', np.nan))}", fontsize=9)
        ax.grid(axis="y", alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[len(RESPONSIVENESS):]: ax.axis("off")
    fig.suptitle(f"{cell_class.upper()} responsiveness across areas — {depth_label}\nsmall points=session percentages; large=area mean ± SE", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(output_dir / "responsiveness_cross_area_SESSION_POINTS.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


def _condition_plot_positions(n_am: int) -> tuple[np.ndarray, np.ndarray]:
    fi_fo = np.array([0.0, 1.0])
    am = np.arange(n_am, dtype=float) + 3.0
    return fi_fo, am


def _annotate_condition_stats(ax: plt.Axes, xs: list[float], cond_cols: list[str], fam_stats: dict[str, Any]) -> None:
    y0, y1 = ax.get_ylim(); span = y1-y0
    for x, c in zip(xs, cond_cols):
        rec = fam_stats.get(c, {}).get("session_level_primary", {})
        omni = rec.get("omnibus", {}); ph = omni.get("p_holm_family", np.nan)
        sigpairs = []
        for r in rec.get("pairwise", {}).values():
            if np.isfinite(r.get("p_holm", np.nan)) and r["p_holm"] < 0.05:
                sigpairs.append(f"{r['area1']}-{r['area2']}({r['p_holm']:.2g})")
        txt = ("* " if np.isfinite(ph) and ph < 0.05 else "") + (f"H:{ph:.2g}" if np.isfinite(ph) else "H:n/a")
        if sigpairs: txt += "\n" + ",".join(sigpairs)
        ax.text(x, y1-0.025*span, txt, ha="center", va="top", fontsize=7)


def plot_condition_profile_all(cells: pd.DataFrame, stats_out: dict[str, Any], areas: list[str],
                               cell_class: str, depth_label: str, output_dir: Path) -> None:
    am_cols = _am_primary_columns(cells); fi_x, am_x = _condition_plot_positions(len(am_cols))
    cols = ["fade_in_response", "fade_out_response"] + [c for _, c in am_cols]
    labels = ["Fade-in", "Fade-out"] + [f"{r:g} Hz" for r, _ in am_cols]
    xs = list(fi_x) + list(am_x)
    fig, ax = plt.subplots(figsize=(11.0, 6.5)); display=[]
    # Individual session traces; intentionally do not connect FO to first AM.
    for a in areas:
        area = cells[cells["canonicalArea"] == a]
        sess_rows = []
        for sk, sdf in area.groupby("session_key"):
            sess_rows.append([np.nanmean(pd.to_numeric(sdf[c], errors="coerce")) for c in cols])
        if sess_rows:
            M = np.asarray(sess_rows, float)
            for row in M:
                ax.plot(fi_x, row[:2], color=AREA_COLORS[a], alpha=0.16, lw=0.8)
                if len(am_cols): ax.plot(am_x, row[2:], color=AREA_COLORS[a], alpha=0.16, lw=0.8)
            overall=np.nanmean(M, axis=0); n=np.sum(np.isfinite(M), axis=0)
            sem=np.nanstd(M, axis=0, ddof=1)/np.sqrt(n)
            ax.plot(fi_x, overall[:2], color=AREA_COLORS[a], lw=2.8, marker="o", ms=5, label=a)
            ax.errorbar(fi_x, overall[:2], yerr=sem[:2], fmt="none", color=AREA_COLORS[a], capsize=4, lw=1.8)
            if len(am_cols):
                ax.plot(am_x, overall[2:], color=AREA_COLORS[a], lw=2.8, marker="o", ms=5)
                ax.errorbar(am_x, overall[2:], yerr=sem[2:], fmt="none", color=AREA_COLORS[a], capsize=4, lw=1.8)
            display.extend(M[np.isfinite(M)].tolist())
    ax.axhline(0, color="0.35", ls="--", lw=1)
    ylim=robust_ylim(display, 0.0)
    if ylim: ax.set_ylim(*ylim)
    _annotate_condition_stats(ax, xs, cols, stats_out["condition_profiles"]["all_cells"])
    ax.set_xticks(xs, labels, rotation=25, ha="right"); ax.set_ylabel("Response (dF/F)")
    ax.set_title(f"{cell_class.upper()} across areas — {depth_label}\nAll cells; session means + area mean ± SE; H=Holm-corrected condition-wise omnibus p")
    ax.legend(frameon=False); ax.grid(axis="y", alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(output_dir/"condition_response_profile_all_cells.png", dpi=DPI, bbox_inches="tight"); plt.close(fig)


def _plot_profile_panel(ax: plt.Axes, df: pd.DataFrame, columns: list[tuple[str,str]], areas: list[str],
                        fam_stats: dict[str, Any], title: str) -> None:
    x=np.arange(len(columns), dtype=float); display=[]
    for a in areas:
        adf=df[df["canonicalArea"]==a]; rows=[]
        for sk,sdf in adf.groupby("session_key"):
            rows.append([np.nanmean(pd.to_numeric(sdf[c], errors="coerce")) for _,c in columns])
        if rows:
            M=np.asarray(rows,float)
            for row in M: ax.plot(x,row,color=AREA_COLORS[a],alpha=0.16,lw=0.8)
            overall=np.nanmean(M,axis=0); n=np.sum(np.isfinite(M),axis=0)
            sem=np.nanstd(M,axis=0,ddof=1)/np.sqrt(n)
            ax.plot(x,overall,color=AREA_COLORS[a],lw=2.7,marker="o",ms=5,label=a)
            ax.errorbar(x,overall,yerr=sem,fmt="none",color=AREA_COLORS[a],capsize=4,lw=1.8)
            display.extend(M[np.isfinite(M)].tolist())
    ax.axhline(0,color="0.35",ls="--",lw=1)
    ylim=robust_ylim(display,0.0)
    if ylim: ax.set_ylim(*ylim)
    _annotate_condition_stats(ax,list(x),[c for _,c in columns],fam_stats)
    ax.set_xticks(x,[l for l,_ in columns],rotation=25,ha="right"); ax.set_ylabel("Response (dF/F)"); ax.set_title(title)
    ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)


def plot_condition_profile_responsive(cells: pd.DataFrame, stats_out: dict[str, Any], areas: list[str],
                                      cell_class: str, depth_label: str, output_dir: Path) -> None:
    am_cols=_am_primary_columns(cells)
    fi_df=analysis_subset(cells,"fi_fo_responsive"); am_df=analysis_subset(cells,"am_responsive")
    fig,axes=plt.subplots(1,2,figsize=(14.5,6.3))
    _plot_profile_panel(axes[0],fi_df,[("Fade-in","fade_in_response"),("Fade-out","fade_out_response")],areas,
                        stats_out["condition_profiles"]["responsive_fi_fo"],"FI-or-FO responsive")
    _plot_profile_panel(axes[1],am_df,[(f"{r:g} Hz",c) for r,c in am_cols],areas,
                        stats_out["condition_profiles"]["responsive_am"],">=1-AM-rate responsive")
    axes[1].legend(frameon=False)
    fig.suptitle(f"{cell_class.upper()} condition responses across areas — {depth_label}\ncondition-specific responsive populations; H=Holm-corrected omnibus p",fontsize=13)
    fig.tight_layout(rect=[0,0,1,0.94]); fig.savefig(output_dir/"condition_response_profile_FDR_responsive_only.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def _condition_matrix(df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    am=_am_primary_columns(df); cols=["fade_in_response","fade_out_response"]+[c for _,c in am]
    labels=["FI","FO"]+[f"{r:g}Hz" for r,_ in am]
    return df[cols].apply(pd.to_numeric,errors="coerce").to_numpy(float),labels


def plot_raster(df: pd.DataFrame, sort_metric: str, areas: list[str], title: str, output_path: Path) -> None:
    fig,axes=plt.subplots(len(areas),1,figsize=(9.5,3.5*len(areas)),squeeze=False); im=None
    for ax,a in zip(axes.ravel(),areas):
        adf=df[df["canonicalArea"]==a].copy(); matrix,labels=_condition_matrix(adf)
        if matrix.size==0:
            ax.text(0.5,0.5,"No cells",transform=ax.transAxes,ha="center"); ax.axis("off"); continue
        denom=np.nanmax(np.abs(matrix),axis=1); good=np.isfinite(denom)&(denom>0)
        matrix=matrix[good]; adf=adf.iloc[np.flatnonzero(good)].copy(); norm=matrix/denom[good,None]
        rank=pd.to_numeric(adf[sort_metric],errors="coerce").to_numpy(float)
        order=np.argsort(np.nan_to_num(rank,nan=-np.inf))[::-1]
        im=ax.imshow(norm[order],aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm")
        ax.set_xticks(np.arange(len(labels)),labels,rotation=25,ha="right"); ax.set_ylabel(f"{a} cells")
        ax.set_title(f"{a}: n={len(order)}")
    fig.suptitle(title,y=0.995)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Normalized condition response",shrink=0.75)
    fig.subplots_adjust(top=0.92,bottom=0.08,hspace=0.35,right=0.90)
    fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_selectivity_outputs(cells: pd.DataFrame, stats_out: dict[str, Any], areas: list[str],
                             cell_class: str, depth_label: str, output_dir: Path) -> None:
    # All cells.
    pooled=stats_out["exploratory_pooled"]["selectivity"]["all_cells"]
    sel=stats_out["selectivity"]["all_cells"]
    for metric,stem,sensitivity in [
        (FI_FO_PRIMARY,"fade_in_vs_fade_out_selectivity",False),
        (FI_FO_SESSION_MEDIAN,"fade_in_vs_fade_out_selectivity_session_median_dff",True),
        (FI_FO_PRESTIM60,"fade_in_vs_fade_out_selectivity_60s_prestim_median_dff",True),
        (FI_BEST_AM,"fade_in_vs_best_am_selectivity",False),
        (AM_SPARSE,"am_rate_lifetime_sparseness",False),
    ]:
        plot_cross_area_cell_metric(cells,metric,areas,f"{cell_class.upper()} — {depth_label}\n{METRIC_LABELS[metric]} — all cells",
                                    pooled[metric],output_dir/f"{stem}_across_areas_all_cells_CELL_POINTS.png",sensitivity=sensitivity)
    for metric,stem,sensitivity in [
        (FI_FO_PRIMARY,"fade_in_vs_fade_out_selectivity",False),
        (FI_FO_SESSION_MEDIAN,"fade_in_vs_fade_out_selectivity_session_median_dff",True),
        (FI_FO_PRESTIM60,"fade_in_vs_fade_out_selectivity_60s_prestim_median_dff",True),
        (FI_BEST_AM,"fade_in_vs_best_am_selectivity",False),
    ]:
        rec=(sel["sensitivity"][metric]["session_level_sensitivity"] if sensitivity else sel[metric]["session_level_primary"])
        plot_cross_area_session_metric(cells,metric,areas,f"{cell_class.upper()} — {depth_label}\n{METRIC_LABELS[metric]} — all cells",
                                       rec,output_dir/f"{stem}_across_areas_all_cells_SESSION_POINTS.png",sensitivity=sensitivity)

    plot_raster(cells,FI_FO_PRIMARY,areas,
                f"{cell_class.upper()} — {depth_label} — all cells\nsorted descending by signed FI/FO selectivity",
                output_dir/"selectivity_rasters_all_cells.png")
    plot_raster(cells,AM_SPARSE,areas,
                f"{cell_class.upper()} — {depth_label} — all cells\nsorted descending by AM-rate lifetime sparseness",
                output_dir/"am_selectivity_raster_all_cells.png")

    # Responsive-only targeted subsets.
    pooled_r=stats_out["exploratory_pooled"]["selectivity"]["responsive_only"]
    sel_r=stats_out["selectivity"]["responsive_only"]
    fi_df=analysis_subset(cells,"fi_fo_responsive"); fi_am_df=analysis_subset(cells,"fi_am_responsive"); am_df=analysis_subset(cells,"am_responsive")
    for metric,df,stem,sensitivity in [
        (FI_FO_PRIMARY,fi_df,"fade_in_vs_fade_out_selectivity",False),
        (FI_FO_SESSION_MEDIAN,fi_df,"fade_in_vs_fade_out_selectivity_session_median_dff",True),
        (FI_FO_PRESTIM60,fi_df,"fade_in_vs_fade_out_selectivity_60s_prestim_median_dff",True),
        (FI_BEST_AM,fi_am_df,"fade_in_vs_best_am_selectivity",False),
        (AM_SPARSE,am_df,"am_rate_lifetime_sparseness",False),
    ]:
        plot_cross_area_cell_metric(df,metric,areas,f"{cell_class.upper()} — {depth_label}\n{METRIC_LABELS[metric]} — {SUBSET_LABELS['fi_fo_responsive' if metric in (FI_FO_PRIMARY,FI_FO_SESSION_MEDIAN,FI_FO_PRESTIM60) else 'fi_am_responsive' if metric==FI_BEST_AM else 'am_responsive']}",
                                    pooled_r[metric],output_dir/f"{stem}_across_areas_FDR_responsive_only_CELL_POINTS.png",sensitivity=sensitivity)
    for metric,df,stem,sensitivity in [
        (FI_FO_PRIMARY,fi_df,"fade_in_vs_fade_out_selectivity",False),
        (FI_FO_SESSION_MEDIAN,fi_df,"fade_in_vs_fade_out_selectivity_session_median_dff",True),
        (FI_FO_PRESTIM60,fi_df,"fade_in_vs_fade_out_selectivity_60s_prestim_median_dff",True),
        (FI_BEST_AM,fi_am_df,"fade_in_vs_best_am_selectivity",False),
    ]:
        rec=(sel_r["sensitivity"][metric]["session_level_sensitivity"] if sensitivity else sel_r[metric]["session_level_primary"])
        plot_cross_area_session_metric(df,metric,areas,f"{cell_class.upper()} — {depth_label}\n{METRIC_LABELS[metric]} — responsive-only",
                                       rec,output_dir/f"{stem}_across_areas_FDR_responsive_only_SESSION_POINTS.png",sensitivity=sensitivity)
    plot_raster(fi_df,FI_FO_PRIMARY,areas,
                f"{cell_class.upper()} — {depth_label} — FI-or-FO responsive\nsorted descending by signed FI/FO selectivity",
                output_dir/"selectivity_rasters_FDR_responsive_only.png")
    plot_raster(am_df,AM_SPARSE,areas,
                f"{cell_class.upper()} — {depth_label} — >=1-AM responsive\nsorted descending by AM-rate lifetime sparseness",
                output_dir/"am_selectivity_raster_FDR_responsive_only.png")


# =============================================================================
# AREA x LAYER TARGETED OUTPUTS
# =============================================================================

def add_layer_columns(df: pd.DataFrame) -> pd.DataFrame:
    out=df.copy(); d=pd.to_numeric(out["depth"],errors="coerce")
    out["layer_key"]=np.where((d>=100)&(d<300),"L23",np.where((d>=300)&(d<=600),"L45",None))
    out["layer_label"]=pd.Series(out["layer_key"]).map({"L23":"L2/3","L45":"L4/5"}).to_numpy()
    return out


def _layer_pair_stats(df: pd.DataFrame, metric: str, areas: list[str], session_level: bool) -> dict[str, Any]:
    recs=[]; ps=[]
    for a in areas:
        adf=df[df["canonicalArea"]==a]
        if session_level:
            vals={}
            for lk in ("L23","L45"):
                sub=adf[adf["layer_key"]==lk]
                vals[lk]=session_metric_table(sub,metric)["value"] if len(sub) else []
        else:
            vals={lk:adf.loc[adf["layer_key"]==lk,metric] for lk in ("L23","L45")}
        r=safe_mannwhitney(vals["L23"],vals["L45"]); r["area"]=a; recs.append(r); ps.append(r["p"])
    adj=holm_adjust(ps)
    return {r["area"]:{**r,"p_holm_across_areas":float(pa) if np.isfinite(pa) else np.nan} for r,pa in zip(recs,adj)}


def plot_area_layer_metric(df: pd.DataFrame, metric: str, areas: list[str], title: str,
                           output_path: Path, session_level: bool) -> dict[str, Any]:
    df=add_layer_columns(df); df=df[df["layer_key"].notna()].copy(); stats_rec=_layer_pair_stats(df,metric,areas,session_level)
    fig,ax=plt.subplots(figsize=(10.5,6.5)); display=[]; xticks=[]; xlabels=[]; x=0
    for a in areas:
        for lk,label in [("L23","L2/3"),("L45","L4/5")]:
            sub=df[(df["canonicalArea"]==a)&(df["layer_key"]==lk)]
            vals=(finite_values(session_metric_table(sub,metric)["value"]) if session_level else finite_values(sub[metric]))
            offs=np.linspace(-0.055,0.055,max(len(vals),1))
            if len(vals):
                ax.scatter(np.full(len(vals),x)+offs,vals,s=28 if session_level else 18,alpha=0.35 if session_level else 0.20,color=AREA_COLORS[a])
                m,se,n=mean_sem(vals); ax.errorbar(x,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,lw=2.3,color=AREA_COLORS[a])
                display.extend(vals.tolist())
            xticks.append(x); xlabels.append(f"{a}\n{label}"); x+=1
        x+=0.6
    ref=_metric_reference(metric)
    if ref is not None: ax.axhline(ref,ls="--",lw=1,color="0.45")
    ylim=robust_ylim(display,ref,bounded=metric in {FI_FO_PRIMARY,FI_FO_SESSION_MEDIAN,FI_FO_PRESTIM60})
    if ylim: ax.set_ylim(*ylim)
    y0,y1=ax.get_ylim(); span=y1-y0
    for i,a in enumerate(areas):
        r=stats_rec[a]; ph=r.get("p_holm_across_areas",np.nan)
        if np.isfinite(ph) and ph<0.05:
            x1=i*2.6; x2=x1+1; y=y1-0.06*span
            ax.plot([x1,x1,x2,x2],[y-0.01*span,y,y,y-0.01*span],color="0.2",lw=1)
            ax.text((x1+x2)/2,y+0.005*span,f"Holm p={ph:.3g}",ha="center",fontsize=8)
    ax.set_xticks(xticks,xlabels); ax.set_ylabel(METRIC_LABELS.get(metric,metric)); ax.set_title(title+"\nL2/3 vs L4/5 within each area; Holm across the three area tests")
    eq=_metric_equation(metric)
    if eq: ax.text(0.5,-0.16,eq,transform=ax.transAxes,ha="center",va="top",fontsize=9)
    ax.grid(axis="y",alpha=0.2); ax.spines[["top","right"]].set_visible(False)
    fig.subplots_adjust(bottom=0.22); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)
    return stats_rec


def make_area_layer_outputs(all_cells: pd.DataFrame, areas: list[str], out_root: Path) -> None:
    root=out_root/"area_by_layer"; root.mkdir(parents=True,exist_ok=True)
    for cell_class in CELL_CLASSES:
        cells=all_cells[all_cells["cell_class"]==cell_class].copy(); out=root/cell_class; out.mkdir(parents=True,exist_ok=True)
        stats_all={}
        for branch in ("all_cells","responsive_only"):
            stats_all[branch]={}
            # FI/FO, including both baseline sensitivities: session-level only.
            fi_df=cells if branch=="all_cells" else analysis_subset(cells,"fi_fo_responsive")
            for metric in (FI_FO_PRIMARY,FI_FO_SESSION_MEDIAN,FI_FO_PRESTIM60):
                stem=f"area_layer_{metric}_{branch}_SESSION_POINTS.png"
                stats_all[branch][metric]=plot_area_layer_metric(fi_df,metric,areas,
                    f"{cell_class.upper()} area x layer — {METRIC_LABELS[metric]} — {branch.replace('_',' ')}",
                    out/stem,session_level=True)
            # FI/best-AM session-level.
            fam_df=cells if branch=="all_cells" else analysis_subset(cells,"fi_am_responsive")
            stats_all[branch][FI_BEST_AM]=plot_area_layer_metric(fam_df,FI_BEST_AM,areas,
                f"{cell_class.upper()} area x layer — {METRIC_LABELS[FI_BEST_AM]} — {branch.replace('_',' ')}",
                out/f"area_layer_{FI_BEST_AM}_{branch}_SESSION_POINTS.png",session_level=True)
            # AM lifetime sparseness remains pooled-cell exploratory only.
            am_df=cells if branch=="all_cells" else analysis_subset(cells,"am_responsive")
            stats_all[branch][AM_SPARSE]=plot_area_layer_metric(am_df,AM_SPARSE,areas,
                f"{cell_class.upper()} area x layer — {METRIC_LABELS[AM_SPARSE]} — {branch.replace('_',' ')}; exploratory cells",
                out/f"area_layer_{AM_SPARSE}_{branch}_CELL_POINTS.png",session_level=False)
        save_json(out/"area_layer_statistics.json",stats_all)
        write_figure_index(out)


# =============================================================================
# V13 TRIAL ARCHIVES / REDUCED-TRIAL RECOMPUTATION
# =============================================================================

def bh_fdr(p_values: np.ndarray, valid_mask: np.ndarray) -> np.ndarray:
    p=np.asarray(p_values,float); valid=np.asarray(valid_mask,bool)
    q=np.full(p.shape,np.nan,float); idx=np.flatnonzero(valid & np.isfinite(p))
    if len(idx)==0: return q
    vals=p[idx]; order=np.argsort(vals); ranked=vals[order]; m=len(ranked)
    adj=ranked*m/np.arange(1,m+1); adj=np.minimum.accumulate(adj[::-1])[::-1]; adj=np.clip(adj,0,1)
    restored=np.empty(m,float); restored[order]=adj; q[idx]=restored; return q


def bounded_fi_fo(fi: np.ndarray, fo: np.ndarray) -> np.ndarray:
    fi=np.asarray(fi,float); fo=np.asarray(fo,float); out=np.full(fi.shape,np.nan); den=np.abs(fi)+np.abs(fo)
    good=np.isfinite(fi)&np.isfinite(fo)&(den>0); out[good]=(fi[good]-fo[good])/den[good]; return out


def fi_best_selectivity(fi: np.ndarray, best: np.ndarray) -> np.ndarray:
    fi=np.asarray(fi,float); best=np.asarray(best,float); out=np.full(fi.shape,np.nan); den=fi+best; scale=np.abs(fi)+np.abs(best)
    threshold=np.maximum(SELECTIVITY_ABS_THRESHOLD,SELECTIVITY_REL_THRESHOLD*scale)
    good=np.isfinite(fi)&np.isfinite(best)&np.isfinite(den)&(np.abs(den)>threshold)
    out[good]=(fi[good]-best[good])/den[good]; return out


def lifetime_sparseness(matrix: np.ndarray) -> np.ndarray:
    M=np.asarray(matrix,float); out=np.full(M.shape[0],np.nan)
    for i,row in enumerate(M):
        v=row[np.isfinite(row)]; n=len(v)
        if n<2: continue
        ms=float(np.mean(v**2))
        if not np.isfinite(ms) or ms<=1e-15: continue
        out[i]=(1-(float(np.mean(v))**2)/ms)/(1-1/n)
    return out


class SignCache:
    def __init__(self, n_perm: int, seed: int):
        self.n_perm=int(n_perm); self.rng=np.random.default_rng(seed); self.cache: dict[int,np.ndarray]={}
    def get(self,n: int) -> np.ndarray:
        n=int(n)
        if n not in self.cache:
            self.cache[n]=self.rng.choice(np.array([-1.0,1.0],dtype=np.float32),size=(self.n_perm,n),replace=True)
        return self.cache[n]


def signflip_pvalues_grouped(response_matrix: np.ndarray, tested_mask: np.ndarray, sign_cache: SignCache) -> np.ndarray:
    R=np.asarray(response_matrix,float); tested=np.asarray(tested_mask,bool); out=np.full(R.shape[0],np.nan)
    groups: dict[bytes,list[int]]={}; masks={}
    for i in np.flatnonzero(tested):
        finite=np.isfinite(R[i]); key=np.packbits(finite).tobytes(); groups.setdefault(key,[]).append(int(i)); masks[key]=finite
    for key,indices in groups.items():
        finite=masks[key]; n=int(np.sum(finite))
        if n<TRIAL_REDUCTION_MIN_TRIALS: continue
        idx=np.asarray(indices,int); values=R[idx][:,finite]; obs=np.mean(values,axis=1)
        signs=sign_cache.get(n); null=(signs@values.T)/float(n); ext=np.sum(np.abs(null)>=np.abs(obs)[None,:],axis=0)
        out[idx]=(1+ext)/(sign_cache.n_perm+1)
    return out


def load_trial_archive(path: str | Path, cache: dict[str,dict[str,np.ndarray]]) -> dict[str,np.ndarray]:
    key=str(path)
    if key in cache: return cache[key]
    p=Path(key)
    if not p.exists(): raise FileNotFoundError(f"Missing v13 trial-response archive: {p}")
    with np.load(p,allow_pickle=False) as z:
        d={k:z[k].copy() for k in z.files}
    needed={"trial_response_primary","trial_condition_index","valid_trial_mask","condition_names","possible_am_rates_hz",
            "classified_mask","cell_class","analysis_index","suite2p_roi","canonical_area","session_key"}
    miss=needed-set(d)
    if miss: raise ValueError(f"{p} missing archive fields: {sorted(miss)}")
    cache[key]=d; return d


def _sample_condition_trials(archive: dict[str,np.ndarray], fraction: float, rng: np.random.Generator) -> tuple[list[np.ndarray],list[int]]:
    cond_idx=np.asarray(archive["trial_condition_index"],int); valid=np.asarray(archive["valid_trial_mask"],bool)
    n_cond=len(np.asarray(archive["condition_names"])); chosen=[]; counts=[]
    for ci in range(n_cond):
        avail=np.flatnonzero(valid & (cond_idx==ci)); n=len(avail)
        if fraction>=0.999999:
            take=avail
        else:
            k=min(n,max(TRIAL_REDUCTION_MIN_TRIALS,int(np.floor(fraction*n+0.5)))) if n else 0
            take=np.sort(rng.choice(avail,size=k,replace=False)) if k else np.array([],dtype=int)
        chosen.append(take); counts.append(len(take))
    return chosen,counts


def reduced_yellow_cells(full_yellow_cells: pd.DataFrame, fraction: float, rng: np.random.Generator,
                         archive_cache: dict[str,dict[str,np.ndarray]], sign_cache: SignCache,
                         recompute_responsiveness: bool = True) -> tuple[pd.DataFrame,list[int]]:
    rows=[]; all_counts=[]
    sessions=full_yellow_cells[["session_key","canonicalArea","depth","trial_response_archive_path"]].drop_duplicates("session_key")
    for _,srow in sessions.iterrows():
        arc=load_trial_archive(srow["trial_response_archive_path"],archive_cache)
        chosen,counts=_sample_condition_trials(arc,fraction,rng); all_counts.extend(counts)
        R=np.asarray(arc["trial_response_primary"],float); classified=np.asarray(arc["classified_mask"],bool)
        n_cells=R.shape[0]; n_cond=len(chosen); cond=np.full((n_cells,n_cond),np.nan)
        pvals=np.full_like(cond,np.nan); qvals=np.full_like(cond,np.nan); resp=np.zeros_like(cond,dtype=bool)
        for ci,take in enumerate(chosen):
            if len(take): cond[:,ci]=np.nanmean(R[:,take],axis=1)
            if recompute_responsiveness and len(take)>=TRIAL_REDUCTION_MIN_TRIALS:
                p=signflip_pvalues_grouped(R[:,take],classified,sign_cache); q=bh_fdr(p,classified)
                pvals[:,ci]=p; qvals[:,ci]=q; resp[:,ci]=classified & np.isfinite(q) & (q<FDR_ALPHA)
        fi=cond[:,0] if n_cond>0 else np.full(n_cells,np.nan); fo=cond[:,1] if n_cond>1 else np.full(n_cells,np.nan)
        am=cond[:,2:] if n_cond>2 else np.empty((n_cells,0))
        best=np.full(n_cells,np.nan)
        if am.shape[1]:
            validrow=np.any(np.isfinite(am),axis=1); idx=np.flatnonzero(validrow)
            if len(idx): best[idx]=am[idx,np.nanargmax(am[idx],axis=1)]
        fi_fo=bounded_fi_fo(fi,fo); fi_best=fi_best_selectivity(fi,best); sparse=lifetime_sparseness(am)
        if recompute_responsiveness:
            fi_resp=resp[:,0] if n_cond>0 else np.zeros(n_cells,bool); fo_resp=resp[:,1] if n_cond>1 else np.zeros(n_cells,bool)
            am_resp=np.any(resp[:,2:],axis=1) if n_cond>2 else np.zeros(n_cells,bool)
            sound_resp=np.any(resp,axis=1); excited=np.zeros(n_cells,bool); suppressed=np.zeros(n_cells,bool)
            for i in np.flatnonzero(sound_resp):
                sig=resp[i]&np.isfinite(cond[i]); cand=np.flatnonzero(sig)
                if len(cand):
                    b=cand[int(np.argmax(np.abs(cond[i,cand])))]
                    if cond[i,b]>0: excited[i]=True
                    elif cond[i,b]<0: suppressed[i]=True
        else:
            fi_resp=fo_resp=am_resp=sound_resp=excited=suppressed=np.zeros(n_cells,bool)
        classes=np.asarray(arc["cell_class"]).astype(str); yellow=(classes=="yellow") & classified
        rates=np.asarray(arc["possible_am_rates_hz"],float)
        for i in np.flatnonzero(yellow):
            row={
                "subject":str(full_yellow_cells["subject"].iloc[0]), "date":"", "session":"",
                "session_key":str(np.asarray(arc["session_key"]).item()), "canonicalArea":str(np.asarray(arc["canonical_area"]).item()),
                "brainArea":"", "depth":float(srow["depth"]), "cell_class":"yellow",
                "analysis_index":int(np.asarray(arc["analysis_index"])[i]), "suite2p_roi":int(np.asarray(arc["suite2p_roi"])[i]),
                "fade_in_response":float(fi[i]), "fade_out_response":float(fo[i]),
                FI_FO_PRIMARY:float(fi_fo[i]), FI_BEST_AM:float(fi_best[i]), AM_SPARSE:float(sparse[i]),
                "fade_in_responsive_fdr":bool(fi_resp[i]), "fade_out_responsive_fdr":bool(fo_resp[i]),
                "fi_or_fo_responsive_fdr":bool(fi_resp[i] or fo_resp[i]),
                "any_am_rate_responsive_fdr":bool(am_resp[i]),
                "fi_or_any_am_responsive_fdr":bool(fi_resp[i] or am_resp[i]),
                "sound_responsive_fdr":bool(sound_resp[i]), "sound_excited_fdr":bool(excited[i]), "sound_suppressed_fdr":bool(suppressed[i]),
            }
            for j,rate in enumerate(rates):
                if j<am.shape[1]: row[f"am_response_{rate:g}Hz"]=float(am[i,j])
            rows.append(row)
    return pd.DataFrame(rows),all_counts


# =============================================================================
# TRIAL-REDUCTION TARGETS / MONTE CARLO
# =============================================================================

def significant_trial_reduction_targets(primary_stats: dict[str,Any]) -> dict[str,list[dict[str,Any]]]:
    groups: dict[str,list[dict[str,Any]]]={}
    def add(group,label,family,branch,key,test,p):
        if np.isfinite(p) and p<0.05:
            groups.setdefault(group,[]).append({"id":f"{group}::{label}","label":label,"family":family,"branch":branch,"key":key,"test":test,"original_p":float(p)})
    # Responsiveness.
    for metric,rec in primary_stats["responsiveness"].items():
        s=rec["session_level_primary"]; add("responsiveness",f"{rec['label']} omnibus","responsiveness","",metric,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
        for pk,pr in s["pairwise"].items(): add("responsiveness",f"{rec['label']}: {pr['area1']} vs {pr['area2']}","responsiveness","",metric,f"pair:{pk}",pr.get("p_holm",np.nan))
    # Primary selectivity only (no sensitivity, no AM-sparseness session test).
    for branch in ("all_cells","responsive_only"):
        for metric in (FI_FO_PRIMARY,FI_BEST_AM):
            rec=primary_stats["selectivity"][branch][metric]; s=rec["session_level_primary"]
            grp=f"selectivity_{branch}"
            add(grp,f"{rec['label']} omnibus","selectivity",branch,metric,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
            for pk,pr in s["pairwise"].items(): add(grp,f"{rec['label']}: {pr['area1']} vs {pr['area2']}","selectivity",branch,metric,f"pair:{pk}",pr.get("p_holm",np.nan))
    # Condition profiles.
    for branch,fam in primary_stats["condition_profiles"].items():
        grp=f"condition_{branch}"
        for col,rec in fam.items():
            s=rec["session_level_primary"]
            add(grp,f"{rec['label']} omnibus","condition_profiles",branch,col,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
            for pk,pr in s["pairwise"].items(): add(grp,f"{rec['label']}: {pr['area1']} vs {pr['area2']}","condition_profiles",branch,col,f"pair:{pk}",pr.get("p_holm",np.nan))
    return groups


def extract_target_p(stats_out: dict[str,Any], target: dict[str,Any]) -> float:
    fam=target["family"]; branch=target["branch"]; key=target["key"]; test=target["test"]
    if fam=="responsiveness": rec=stats_out["responsiveness"][key]["session_level_primary"]
    elif fam=="selectivity": rec=stats_out["selectivity"][branch][key]["session_level_primary"]
    elif fam=="condition_profiles": rec=stats_out["condition_profiles"][branch][key]["session_level_primary"]
    else: return np.nan
    if test=="omnibus": return float(rec["omnibus"].get("p_holm_family",np.nan))
    pk=test.split(":",1)[1]; return float(rec["pairwise"].get(pk,{}).get("p_holm",np.nan))


def target_requires_responsiveness(targets: dict[str,list[dict[str,Any]]]) -> bool:
    for group,recs in targets.items():
        if group=="responsiveness" or "responsive_only" in group or group in {"condition_responsive_fi_fo","condition_responsive_am"}:
            if recs: return True
    return False


def plot_trial_reduction_robustness(group: str, targets: list[dict[str,Any]], raw: pd.DataFrame,
                                    count_summary: dict[float,tuple[float,int,int]], depth_label: str,
                                    output_dir: Path) -> None:
    fractions=np.asarray(TRIAL_REDUCTION_FRACTIONS,float); x=100*fractions
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(10.5,8.2),sharex=True,gridspec_kw={"height_ratios":[1.05,1.0]})
    for target in targets:
        label=target["label"]; med=[]; lo=[]; hi=[]; retain=[]
        for f in fractions:
            vals=finite_values(raw.loc[(raw["fraction"]==f)&(raw["target_id"]==target["id"]),"p_adjusted"])
            if len(vals):
                med.append(np.median(vals)); lo.append(np.percentile(vals,10)); hi.append(np.percentile(vals,90)); retain.append(np.mean(vals<0.05))
            else: med.append(np.nan); lo.append(np.nan); hi.append(np.nan); retain.append(np.nan)
        med=np.asarray(med,float); lo=np.asarray(lo,float); hi=np.asarray(hi,float); retain=np.asarray(retain,float)
        line=ax1.plot(x,np.clip(med,1e-6,1),marker="o",label=label)[0]
        ax1.fill_between(x,np.clip(lo,1e-6,1),np.clip(hi,1e-6,1),alpha=0.12,color=line.get_color())
        ax2.plot(x,retain,marker="o",color=line.get_color(),label=label)
    ax1.axhline(0.05,color="0.35",ls="--",lw=1); ax1.set_yscale("log"); ax1.set_ylabel("Adjusted p\nmedian (10th-90th pct)")
    ax1.grid(alpha=0.2); ax1.spines[["top","right"]].set_visible(False)
    ax2.axhline(0.8,color="0.6",ls=":",lw=1); ax2.axhline(0.9,color="0.7",ls=":",lw=1)
    ax2.set_ylim(-0.02,1.02); ax2.set_ylabel("Fraction of resamples\nretaining p_adj < 0.05"); ax2.grid(alpha=0.2); ax2.spines[["top","right"]].set_visible(False)
    labels=[]
    for f in fractions:
        medn,mn,mx=count_summary.get(float(f),(np.nan,0,0))
        ntext=f"median {medn:.0f}" if np.isfinite(medn) else "n/a"
        if mn!=mx: ntext+=f" ({mn}-{mx})"
        labels.append(f"{int(round(100*f))}%\n{ntext} trials/cond")
    ax2.set_xticks(x,labels); ax2.set_xlabel("Fraction of currently available repetitions retained")
    ax1.legend(frameon=False,fontsize=8,loc="best");
    fig.suptitle(f"YELLOW trial-reduction robustness — {depth_label}\n{group.replace('_',' ')}\n100%=original v13 result; reduced levels=resampling without replacement within session x condition",fontsize=12)
    fig.tight_layout(rect=[0,0,1,0.94]); fig.savefig(output_dir/f"trial_reduction_{group}_ROBUSTNESS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def run_trial_reduction_robustness(full_yellow_cells: pd.DataFrame, primary_stats: dict[str,Any], areas: list[str],
                                   depth_label: str, output_dir: Path, n_resamples: int,
                                   response_permutations: int, seed: int) -> dict[str,Any]:
    targets_by_group=significant_trial_reduction_targets(primary_stats)
    targets_by_group={k:v for k,v in targets_by_group.items() if v}
    if not targets_by_group:
        return {"performed":False,"reason":"No significant primary session-level YELLOW-across-area findings"}
    root=output_dir/"trial_reduction_robustness"; root.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(seed); archive_cache={}; sign_cache=SignCache(response_permutations,seed+991)
    all_targets=[t for v in targets_by_group.values() for t in v]
    need_resp=target_requires_responsiveness(targets_by_group)
    raw_rows=[]; count_summary={}
    # Full-data 100% is the original, exactly.
    counts=[]
    for path in full_yellow_cells["trial_response_archive_path"].dropna().astype(str).unique():
        arc=load_trial_archive(path,archive_cache); _,cc=_sample_condition_trials(arc,1.0,rng); counts.extend(cc)
    count_summary[1.0]=(float(np.median(counts)) if counts else np.nan,int(np.min(counts)) if counts else 0,int(np.max(counts)) if counts else 0)
    for t in all_targets:
        raw_rows.append({"fraction":1.0,"resample":0,"target_id":t["id"],"target_label":t["label"],"p_adjusted":t["original_p"]})

    for frac in TRIAL_REDUCTION_FRACTIONS[1:]:
        first_counts=None
        for rep in range(int(n_resamples)):
            reduced,counts=reduced_yellow_cells(full_yellow_cells,float(frac),rng,archive_cache,sign_cache,recompute_responsiveness=need_resp)
            if first_counts is None: first_counts=list(counts)
            s=build_primary_stats(reduced,areas)
            for t in all_targets:
                raw_rows.append({"fraction":float(frac),"resample":int(rep),"target_id":t["id"],"target_label":t["label"],"p_adjusted":extract_target_p(s,t)})
        cc=first_counts or []
        count_summary[float(frac)]=(float(np.median(cc)) if cc else np.nan,int(np.min(cc)) if cc else 0,int(np.max(cc)) if cc else 0)
    raw=pd.DataFrame(raw_rows); raw.to_csv(root/"trial_reduction_all_significant_targets_RAW.csv",index=False)

    summary_rows=[]
    for group,targets in targets_by_group.items():
        for t in targets:
            for frac in TRIAL_REDUCTION_FRACTIONS:
                vals=finite_values(raw.loc[(raw["fraction"]==frac)&(raw["target_id"]==t["id"]),"p_adjusted"])
                medn,mn,mx=count_summary[float(frac)]
                summary_rows.append({"group":group,"target":t["label"],"fraction":frac,"percent_trials":100*frac,
                                     "median_trials_per_condition":medn,"min_trials_per_condition":mn,"max_trials_per_condition":mx,
                                     "n_valid_resamples":len(vals),"median_p_adjusted":float(np.median(vals)) if len(vals) else np.nan,
                                     "p10":float(np.percentile(vals,10)) if len(vals) else np.nan,"p90":float(np.percentile(vals,90)) if len(vals) else np.nan,
                                     "significance_retention":float(np.mean(vals<0.05)) if len(vals) else np.nan})
        graw=raw[raw["target_id"].isin([t["id"] for t in targets])].copy()
        plot_trial_reduction_robustness(group,targets,graw,count_summary,depth_label,root)
        graw.to_csv(root/f"trial_reduction_{group}_RAW.csv",index=False)
    summary=pd.DataFrame(summary_rows); summary.to_csv(root/"trial_reduction_summary.csv",index=False)
    save_json(root/"trial_reduction_manifest.json",{
        "fractions":list(TRIAL_REDUCTION_FRACTIONS),"n_resamples_per_reduced_fraction":int(n_resamples),
        "response_signflip_permutations":int(response_permutations),"seed":int(seed),
        "sampling":"without replacement within session x stimulus condition",
        "100_percent":"original v13/full-data significance; not re-randomized",
        "targets":targets_by_group,"trial_count_summary":{str(k):v for k,v in count_summary.items()},
        "responsiveness_recomputed_for_reduced_data":bool(need_resp),
    })
    return {"performed":True,"groups":list(targets_by_group),"n_targets":len(all_targets),"output_root":str(root)}


# =============================================================================
# REPORTS / INDEX / MASTER TABLE
# =============================================================================

def write_figure_index(output_dir: Path) -> None:
    pngs=sorted(output_dir.glob("*.png")); lines=["FIGURE INDEX","============",""]+[p.name for p in pngs]
    (output_dir/"FIGURE_INDEX.txt").write_text("\n".join(lines)+"\n",encoding="utf-8")


def write_report(path: Path, subject: str, dates: list[str], cell_class: str, depth_label: str,
                 cells: pd.DataFrame, stats_out: dict[str,Any], areas: list[str]) -> None:
    lines=["CROSS-AREA SOUND-TUNING ANALYSIS v3","="*78,f"Subject: {subject}",f"Dates: {', '.join(dates)}",
           f"Cell class: {cell_class.upper()}",f"Depth: {depth_label}","",
           "PRIMARY INFERENCE: one summary per imaging session.",
           "Pooled-cell tests are exploratory. FI/FO alternate-dF/F analyses are sensitivity analyses.",""]
    for a in areas:
        adf=cells[cells["canonicalArea"]==a]; lines.append(f"{a}: {len(adf)} cells, {adf['session_key'].nunique()} sessions")
    lines += ["","RESPONSIVENESS"]
    for metric,rec in stats_out["responsiveness"].items():
        s=rec["session_level_primary"]; lines.append(f"{rec['label']}: KW {p_text(s['omnibus']['p'])}; family Holm {p_text(s['omnibus'].get('p_holm_family',np.nan))}")
        for pr in s["pairwise"].values():
            if np.isfinite(pr.get("p_holm",np.nan)): lines.append(f"  {pr['area1']} vs {pr['area2']}: Holm p={pr['p_holm']:.4g}")
    lines += ["","SELECTIVITY"]
    for branch in ("all_cells","responsive_only"):
        lines.append(branch)
        for metric in (FI_FO_PRIMARY,FI_BEST_AM):
            rec=stats_out["selectivity"][branch][metric]["session_level_primary"]
            lines.append(f"  {METRIC_LABELS[metric]}: KW {p_text(rec['omnibus']['p'])}; family Holm {p_text(rec['omnibus'].get('p_holm_family',np.nan))}")
    lines += ["","CONDITION PROFILES"]
    for branch,fam in stats_out["condition_profiles"].items():
        lines.append(branch)
        for col,rec in fam.items():
            s=rec["session_level_primary"]; lines.append(f"  {rec['label']}: KW {p_text(s['omnibus']['p'])}; family Holm {p_text(s['omnibus'].get('p_holm_family',np.nan))}")
    path.write_text("\n".join(lines)+"\n",encoding="utf-8")


def master_rows(cell_class: str, depth_key: str, stats_out: dict[str,Any]) -> list[dict[str,Any]]:
    rows=[]
    for metric,rec in stats_out["responsiveness"].items():
        s=rec["session_level_primary"]; rows.append({"cell_class":cell_class,"depth":depth_key,"family":"responsiveness","branch":"", "metric":metric,
            "omnibus_H":s["omnibus"]["H"],"omnibus_p":s["omnibus"]["p"],"omnibus_p_holm_family":s["omnibus"].get("p_holm_family",np.nan)})
    for branch in ("all_cells","responsive_only"):
        for metric in (FI_FO_PRIMARY,FI_BEST_AM):
            s=stats_out["selectivity"][branch][metric]["session_level_primary"]; rows.append({"cell_class":cell_class,"depth":depth_key,"family":"selectivity","branch":branch,"metric":metric,
                "omnibus_H":s["omnibus"]["H"],"omnibus_p":s["omnibus"]["p"],"omnibus_p_holm_family":s["omnibus"].get("p_holm_family",np.nan)})
    for branch,fam in stats_out["condition_profiles"].items():
        for col,rec in fam.items():
            s=rec["session_level_primary"]; rows.append({"cell_class":cell_class,"depth":depth_key,"family":"condition_profile","branch":branch,"metric":col,
                "omnibus_H":s["omnibus"]["H"],"omnibus_p":s["omnibus"]["p"],"omnibus_p_holm_family":s["omnibus"].get("p_holm_family",np.nan)})
    return rows


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args=parse_args(); subject=str(args.subject); dates=[str(d) for d in args.dates]; areas=list(args.areas)
    in_paths={a:expected_area_csv(subject,a,dates) for a in areas}; out_root=output_root(subject,dates)
    print("="*82); print("SOUND_TUNING CROSS-AREA CELL-CLASS ANALYSIS v3"); print("="*82)
    print(f"Subject: {subject}"); print(f"Dates: {', '.join(dates)}"); print(f"Areas: {', '.join(areas)}")
    print(f"Output root: {out_root}"); print("Expected v13 inputs:")
    for a,p in in_paths.items(): print(f"  {a}: {p} {'[FOUND]' if p.exists() else '[MISSING]'}")
    if args.dry_run: print("Dry run complete."); return

    out_root.mkdir(parents=True,exist_ok=True); all_cells=load_area_tables(subject,dates,areas)
    all_cells.to_csv(out_root/"all_areas_combined_cell_results.csv",index=False)
    manifest={
        "script_version":"v3","prerequisite":"sound_tuning_area_analysis_v13.py","subject":subject,"dates":dates,"areas":areas,
        "primary_inference":"session-level cross-area Kruskal-Wallis; pairwise Mann-Whitney with Holm correction",
        "pooled_cells":"exploratory only","fi_fo_selectivity":"(FI-FO)/(|FI|+|FO|)",
        "trial_reduction":{"enabled":not args.skip_trial_reduction,"fractions":list(TRIAL_REDUCTION_FRACTIONS),
                           "resamples":args.trial_reduction_resamples,"response_permutations":args.trial_reduction_response_permutations,
                           "seed":args.trial_reduction_seed,"yellow_primary_significant_results_only":True},
    }
    save_json(out_root/"run_manifest.json",manifest)
    master=[]
    for depth_key,(_,_,depth_label) in DEPTH_STRATA.items():
        dcells=subset_depth(all_cells,depth_key)
        print("\n"+"-"*82); print(f"Depth: {depth_label}")
        for cell_class in CELL_CLASSES:
            cells=dcells[dcells["cell_class"]==cell_class].copy(); out=out_root/depth_key/cell_class; out.mkdir(parents=True,exist_ok=True)
            print(f"  {cell_class.upper():6s}: {len(cells)} cells, {cells['session_key'].nunique()} sessions")
            cells.to_csv(out/"cell_results.csv",index=False); aggregate_sessions(cells).to_csv(out/"session_summary.csv",index=False)
            stats_out=build_full_stats(cells,areas); save_json(out/"statistics.json",stats_out)
            plot_responsiveness(cells,stats_out,areas,cell_class,depth_label,out)
            plot_condition_profile_all(cells,stats_out,areas,cell_class,depth_label,out)
            plot_condition_profile_responsive(cells,stats_out,areas,cell_class,depth_label,out)
            plot_selectivity_outputs(cells,stats_out,areas,cell_class,depth_label,out)
            write_report(out/"REPORT.txt",subject,dates,cell_class,depth_label,cells,stats_out,areas)
            master.extend(master_rows(cell_class,depth_key,stats_out))
            if cell_class=="yellow" and not args.skip_trial_reduction:
                tr=run_trial_reduction_robustness(cells,stats_out,areas,depth_label,out,
                    n_resamples=max(1,int(args.trial_reduction_resamples)),
                    response_permutations=max(64,int(args.trial_reduction_response_permutations)),
                    seed=int(args.trial_reduction_seed)+list(DEPTH_STRATA).index(depth_key)*10000)
                save_json(out/"trial_reduction_status.json",tr)
                if tr.get("performed"): print(f"    Trial reduction: {tr['n_targets']} significant primary target(s) -> {tr['output_root']}")
                else: print(f"    Trial reduction: {tr.get('reason','not performed')}")
            write_figure_index(out)

    make_area_layer_outputs(all_cells,areas,out_root)
    pd.DataFrame(master).to_csv(out_root/"MASTER_SESSION_STATISTICS.csv",index=False)
    print("\n"+"="*82); print("DONE"); print(f"Outputs saved under: {out_root}"); print("="*82)


if __name__ == "__main__":
    main()
