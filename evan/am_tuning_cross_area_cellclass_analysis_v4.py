#!/usr/bin/env python3
"""
Cross-area comparison of AM-tuning responses within YELLOW or GREEN cells.

This is the second-stage follow-up analysis for am_tuning_area_analysis_v9.py.
It does NOT rerun Suite2p, Cellpose, or event alignment. Instead it loads the
combined outputs already produced separately for A1, AAF, and A2 and compares:

    YELLOW cells across A1 / AAF / A2
    GREEN  cells across A1 / AAF / A2

The analyses are performed independently for:

    tuningFreq
    tuningAM

and independently for three depth strata:

    all_depths       : all included sessions
    L23_100to300um   : 100 <= depth < 300 um
    L45_300to600um   : 300 <= depth <= 600 um

The 300-um boundary is assigned to L4/5, so no session is counted twice.

TUNING SELECTIVITY
------------------
The primary tuning-selectivity metric is lifetime sparseness across the magnitude
of the mean tuning response profile, r_i = |R_i|. Separate cross-area outputs are
also produced for the Gini coefficient, tuning-profile Fano factor, and FWHM
bandwidth. Frequency FWHM is measured in octaves; AM-rate FWHM is measured in Hz.
Legacy best-vs-rest selectivity contrast/index outputs are retained as secondary
descriptive measures. Numeric frequency and AM-rate axes use true base-2 log scaling.

An additional explicit area_by_layer branch compares each cell class across the six
A1/AAF/A2 x L2/3/L4/5 strata, matching the corresponding sound-tuning workflow.

PRIMARY INFERENCE
-----------------
Cells are useful for descriptive distributions, but cells from the same imaging
session are not independent biological replicates. Therefore the primary
cross-area tests use one summary value per imaging session. Pooled-cell tests
are also saved, but are explicitly labeled exploratory/descriptive.

For continuous metrics, primary tests are:
    * Kruskal-Wallis across areas
    * pairwise Mann-Whitney U tests
    * Holm correction across the three pairwise area comparisons
    * Cliff's delta effect size

For FDR responsiveness/excitation/suppression, the primary tests compare the
session percentages across areas. Pooled-cell Fisher exact tests are saved as
exploratory summaries.

PREREQUISITE OUTPUTS
--------------------
For each requested area and tuning mode, this script expects:

<TEMP_OUTPUT_PATH>/evan/am_tuning_area_analysis/<subject>/<area>/<date_tag>/
    <tuning_mode>/combined/combined_cell_results.csv
    <tuning_mode>/combined/combined_condition_results.csv

The prerequisite files are produced by am_tuning_area_analysis_v9.py.

Examples
--------
Run both tuning modes:

python am_tuning_cross_area_cellclass_analysis.py imag039 \\
    --dates 20260717 20260729 20260730

Only frequency tuning:

python am_tuning_cross_area_cellclass_analysis.py imag039 \\
    --dates 20260717 20260729 20260730 --mode tuningFreq

Dry run:

python am_tuning_cross_area_cellclass_analysis.py imag039 \\
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
from scipy import stats

from jaratoolbox import settings


# =============================================================================
# CONSTANTS
# =============================================================================

AREAS = ("A1", "AAF", "A2")
CELL_CLASSES = ("yellow", "green")
TUNING_MODES = ("tuningFreq", "tuningAM")

DEPTH_STRATA = {
    "all_depths": (None, None),
    "L23_100to300um": (100.0, 300.0),       # [100, 300)
    "L45_300to600um": (300.0, 600.0),       # [300, 600]
}

AREA_COLORS = {
    "A1": "tab:blue",
    "AAF": "tab:orange",
    "A2": "tab:green",
}

FDR_ALPHA = 0.05
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
    # Primary + comparison selectivity metrics from am_tuning_area_analysis_v9.py.
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
    # Legacy best-vs-rest metrics retained as secondary descriptive outputs.
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
    "stim_responsive_fdr": "FDR stimulus-responsive cells (%)",
    "stim_excited_fdr": "FDR excited cells (%)",
    "stim_suppressed_fdr": "FDR suppressed cells (%)",
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
        "--dates", nargs="+", required=True,
        help="Dates used for the prerequisite area analyses.",
    )
    parser.add_argument(
        "--areas", nargs="+", default=list(AREAS), choices=list(AREAS),
        help="Areas to compare. Default: A1 AAF A2.",
    )
    parser.add_argument(
        "--mode", choices=["both", *TUNING_MODES], default="both",
        help="Analyze tuningFreq, tuningAM, or both (default).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print expected inputs/outputs and stop before loading tables.",
    )
    return parser.parse_args()


def date_tag(dates: Iterable[str]) -> str:
    return "_".join(str(d) for d in dates)


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(obj, f, indent=2, default=json_default)


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
        float(np.median(vals)),
        float(np.percentile(vals, 25)),
        float(np.percentile(vals, 75)),
        len(vals),
    )


def holm_adjust(p_values: list[float]) -> list[float]:
    p = np.asarray(p_values, dtype=float)
    out = np.full_like(p, np.nan)
    finite_idx = np.where(np.isfinite(p))[0]
    if len(finite_idx) == 0:
        return out.tolist()
    order = finite_idx[np.argsort(p[finite_idx])]
    m = len(order)
    running = 0.0
    for rank, idx in enumerate(order):
        adjusted = min(1.0, (m-rank) * p[idx])
        running = max(running, adjusted)
        out[idx] = running
    return out.tolist()


def cliffs_delta(x: Iterable[Any], y: Iterable[Any]) -> float:
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return np.nan
    ranks = stats.rankdata(np.concatenate([x, y]))
    rx = np.sum(ranks[:len(x)])
    u = rx - len(x)*(len(x)+1)/2
    return float((2*u)/(len(x)*len(y)) - 1)


def safe_mannwhitney(x: Iterable[Any], y: Iterable[Any]) -> dict[str, Any]:
    x = finite_values(x)
    y = finite_values(y)
    if len(x) == 0 or len(y) == 0:
        return {"n1":len(x), "n2":len(y), "U":np.nan, "p":np.nan, "cliffs_delta":np.nan}
    try:
        res = stats.mannwhitneyu(x, y, alternative="two-sided")
        return {
            "n1":len(x), "n2":len(y), "U":float(res.statistic),
            "p":float(res.pvalue), "cliffs_delta":cliffs_delta(x,y),
        }
    except Exception:
        return {"n1":len(x), "n2":len(y), "U":np.nan, "p":np.nan, "cliffs_delta":np.nan}


def safe_kruskal(groups: dict[str, Iterable[Any]]) -> dict[str, Any]:
    clean = {k: finite_values(v) for k,v in groups.items()}
    usable = {k:v for k,v in clean.items() if len(v)>0}
    if len(usable) < 2:
        return {"areas":list(usable), "n_by_area":{k:len(v) for k,v in clean.items()}, "H":np.nan, "p":np.nan}
    # scipy warns/returns NaN when every observation across all groups is identical.
    # In that degenerate case there is no rank difference, so report H=0, p=1.
    concat = np.concatenate(list(usable.values()))
    if len(concat) and np.allclose(concat, concat[0], equal_nan=False):
        return {"areas":list(usable), "n_by_area":{k:len(v) for k,v in clean.items()}, "H":0.0, "p":1.0}
    try:
        res = stats.kruskal(*usable.values(), nan_policy="omit")
        return {"areas":list(usable), "n_by_area":{k:len(v) for k,v in clean.items()}, "H":float(res.statistic), "p":float(res.pvalue)}
    except Exception:
        return {"areas":list(usable), "n_by_area":{k:len(v) for k,v in clean.items()}, "H":np.nan, "p":np.nan}


def pairwise_area_tests(groups: dict[str, Iterable[Any]], areas: list[str]) -> dict[str, Any]:
    records = []
    for i,a1 in enumerate(areas):
        for a2 in areas[i+1:]:
            test = safe_mannwhitney(groups.get(a1,[]), groups.get(a2,[]))
            records.append({"area1":a1, "area2":a2, **test})
    adjusted = holm_adjust([r["p"] for r in records])
    for rec,p_holm in zip(records,adjusted):
        rec["p_holm"] = p_holm
    return {f"{r['area1']}_vs_{r['area2']}":r for r in records}


def fisher_pairwise_binary(df: pd.DataFrame, binary_col: str, areas: list[str]) -> dict[str, Any]:
    records=[]
    for i,a1 in enumerate(areas):
        for a2 in areas[i+1:]:
            d1=df[df.canonicalArea==a1]; d2=df[df.canonicalArea==a2]
            n1=len(d1); n2=len(d2)
            y1=int(d1[binary_col].astype(bool).sum()) if n1 else 0
            y2=int(d2[binary_col].astype(bool).sum()) if n2 else 0
            if n1==0 or n2==0:
                odds,p=np.nan,np.nan
            else:
                odds,p=stats.fisher_exact([[y1,n1-y1],[y2,n2-y2]])
            records.append({
                "area1":a1,"area2":a2,"n1":n1,"positive1":y1,"n2":n2,"positive2":y2,
                "odds_ratio":float(odds) if np.isfinite(odds) else np.nan,
                "p":float(p) if np.isfinite(p) else np.nan,
            })
    adjusted=holm_adjust([r["p"] for r in records])
    for rec,p_holm in zip(records,adjusted): rec["p_holm"]=p_holm
    return {f"{r['area1']}_vs_{r['area2']}":r for r in records}


def p_text(p: float) -> str:
    if not np.isfinite(p): return "p=n/a"
    if p < 1e-4: return "p<1e-4"
    return f"p={p:.4f}"


# =============================================================================
# INPUT DISCOVERY / VALIDATION
# =============================================================================

def area_mode_dir(subject: str, area: str, dates: list[str], mode: str) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH) / "evan" / "am_tuning_area_analysis"
        / subject / area / date_tag(dates) / mode / "combined"
    )


def expected_area_cell_csv(subject: str, area: str, dates: list[str], mode: str) -> Path:
    return area_mode_dir(subject,area,dates,mode) / "combined_cell_results.csv"


def expected_area_condition_csv(subject: str, area: str, dates: list[str], mode: str) -> Path:
    return area_mode_dir(subject,area,dates,mode) / "combined_condition_results.csv"


def output_root(subject: str, dates: list[str]) -> Path:
    return (
        Path(settings.TEMP_OUTPUT_PATH) / "evan" / "am_tuning_cross_area_cellclass_analysis"
        / subject / date_tag(dates)
    )


def _coerce_bool(df: pd.DataFrame, col: str) -> None:
    if col not in df.columns: return
    if df[col].dtype != bool:
        df[col] = df[col].astype(str).str.lower().isin(["true","1","yes"])


def load_mode_tables(
    subject: str, dates: list[str], areas: list[str], mode: str
) -> tuple[pd.DataFrame,pd.DataFrame,dict[str,dict[str,str]]]:
    cell_frames=[]; cond_frames=[]; missing=[]; provenance={}
    for area in areas:
        cp=expected_area_cell_csv(subject,area,dates,mode)
        qp=expected_area_condition_csv(subject,area,dates,mode)
        provenance[area]={"cell":str(cp),"condition":str(qp)}
        if not cp.exists(): missing.append(cp)
        if not qp.exists(): missing.append(qp)
        if not cp.exists() or not qp.exists(): continue
        cdf=pd.read_csv(cp); qdf=pd.read_csv(qp)
        for df,path in ((cdf,cp),(qdf,qp)):
            if "canonicalArea" not in df.columns:
                raise ValueError(f"{path} has no canonicalArea column; expected am_tuning_area_analysis_v9.py output.")
            bad=set(df.canonicalArea.dropna().astype(str).unique())-{area}
            if bad: raise ValueError(f"{path} contains unexpected canonicalArea values: {sorted(bad)}")
            if "tuning_mode" not in df.columns:
                raise ValueError(f"{path} has no tuning_mode column.")
            badmode=set(df.tuning_mode.dropna().astype(str).unique())-{mode}
            if badmode: raise ValueError(f"{path} contains unexpected tuning_mode values: {sorted(badmode)}")
        cell_frames.append(cdf); cond_frames.append(qdf)
    if missing:
        msg="Missing prerequisite AM area-analysis output(s):\n"+"\n".join(f"  {p}" for p in missing)
        msg += "\nRun am_tuning_area_analysis_v9.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)
    if not cell_frames: raise RuntimeError(f"No {mode} area tables were loaded.")
    cells=pd.concat(cell_frames,ignore_index=True,sort=False)
    conds=pd.concat(cond_frames,ignore_index=True,sort=False)
    required_cells={
        "subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode",
        "stim_responsive_fdr","stim_excited_fdr","stim_suppressed_fdr","stim_response_mean",
        "best_tuning_response","peak_absolute_response","tuning_modulation_depth",
        "tuning_lifetime_sparseness","tuning_gini_coefficient","tuning_fano_factor","tuning_fwhm",
        "tuning_selectivity_contrast","tuning_selectivity_index","preferred_tuning_value_Hz",
    }
    miss=sorted(required_cells-set(cells.columns))
    if miss: raise ValueError("Combined AM cell table(s) are missing required columns: "+", ".join(miss))
    required_cond={
        "subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode",
        "stim_responsive_fdr","tuning_value_Hz","intensity_dB","condition_response","condition_selectivity_contrast",
    }
    miss=sorted(required_cond-set(conds.columns))
    if miss: raise ValueError("Combined AM condition table(s) are missing required columns: "+", ".join(miss))
    cells["depth"]=pd.to_numeric(cells.depth,errors="coerce")
    conds["depth"]=pd.to_numeric(conds.depth,errors="coerce")
    for col in BINARY_METRICS: _coerce_bool(cells,col)
    _coerce_bool(conds,"stim_responsive_fdr")
    return cells,conds,provenance


def subset_depth(df: pd.DataFrame, stratum: str) -> pd.DataFrame:
    low,high=DEPTH_STRATA[stratum]
    if low is None: return df.copy()
    depth=pd.to_numeric(df.depth,errors="coerce")
    if stratum.startswith("L23"):
        mask=(depth>=low)&(depth<high)
    else:
        mask=(depth>=low)&(depth<=high)
    return df.loc[mask].copy()


# =============================================================================
# TUNING-COLUMN HELPERS
# =============================================================================

def response_columns(df: pd.DataFrame, mode: str) -> tuple[list[str],np.ndarray,list[str]]:
    prefix="response_freq_" if mode=="tuningFreq" else "response_AM_"
    cols=[c for c in df.columns if c.startswith(prefix) and c.endswith("_Hz")]
    parsed=[]
    for c in cols:
        text=c[len(prefix):-3]
        try: val=float(text)
        except Exception: continue
        parsed.append((val,c))
    parsed.sort(key=lambda x:x[0])
    values=np.array([x[0] for x in parsed],dtype=float)
    cols=[x[1] for x in parsed]
    labels=[f"{v/1000:g}" for v in values] if mode=="tuningFreq" else [f"{v:g}" for v in values]
    return cols,values,labels


def mode_axis_label(mode: str) -> str:
    return "Tone frequency (kHz)" if mode=="tuningFreq" else "AM rate (Hz)"


def mode_title(mode: str) -> str:
    return "Frequency tuning" if mode=="tuningFreq" else "AM-rate tuning"


def xplot(values_hz: Iterable[Any], mode: str) -> np.ndarray:
    """Return explicit octave coordinates for tuning values.

    The plotted x coordinate is log2 of the displayed tuning value
    (kHz for tuningFreq, Hz for tuningAM). This guarantees that every
    doubling occupies the same physical width on the axis.
    """
    values=np.asarray(values_hz,dtype=float)
    display_values=values/1000.0 if mode=="tuningFreq" else values
    coords=np.full(display_values.shape,np.nan,dtype=float)
    valid=np.isfinite(display_values) & (display_values>0)
    coords[valid]=np.log2(display_values[valid])
    return coords


def log2_tick_labels(values_hz: Iterable[Any], mode: str) -> list[str]:
    values=np.asarray(values_hz,dtype=float)
    return [f"{v/1000:g}" for v in values] if mode=="tuningFreq" else [f"{v:g}" for v in values]


def apply_log2_tuning_axis(ax, values_hz: Iterable[Any], mode: str) -> None:
    """Format tuning axes using explicit log2 coordinates."""
    values_hz=np.asarray(values_hz,dtype=float).ravel()
    x=xplot(values_hz,mode); valid=np.isfinite(x)
    if not np.any(valid):
        return
    xv=x[valid]
    labels=np.asarray(log2_tick_labels(values_hz[valid],mode),dtype=object)
    ax.set_xscale("linear")
    ax.set_xticks(xv)
    ax.set_xticklabels(labels)
    lo,hi=float(np.min(xv)),float(np.max(xv))
    margin_oct=.12
    if hi>lo:
        ax.set_xlim(lo-margin_oct,hi+margin_oct)
    else:
        ax.set_xlim(lo-0.5,hi+0.5)


def log2_bin_edges(values_hz: Iterable[Any], mode: str) -> np.ndarray | None:
    values_hz=np.asarray(values_hz,dtype=float).ravel()
    x=xplot(values_hz,mode)
    if len(x)==0 or np.any(~np.isfinite(x)):
        return None
    if len(x)==1:
        return np.asarray([x[0]-0.5,x[0]+0.5],dtype=float)
    mids=.5*(x[:-1]+x[1:])
    edges=np.empty(len(x)+1,float)
    edges[1:-1]=mids
    edges[0]=x[0]-(mids[0]-x[0])
    edges[-1]=x[-1]+(x[-1]-mids[-1])
    return edges


def metric_label(metric: str, mode: str) -> str:
    if metric=="tuning_fwhm":
        return "FWHM bandwidth (octaves)" if mode=="tuningFreq" else "FWHM bandwidth (Hz)"
    return CONTINUOUS_METRICS.get(metric,{}).get("label",metric)


def selectivity_equation_footer(mode: str) -> str:
    fwhm_unit="octaves (log2 frequency)" if mode=="tuningFreq" else "Hz"
    return (
        r"Lifetime sparseness = [1 - (mean(r))$^2$/mean(r$^2$)]/[1 - 1/N];  "
        r"Gini = inequality of r;  Fano = var(r)/mean(r);  "
        f"FWHM = width of |response| at 1/2 max ({fwhm_unit});  r = |mean baseline-corrected dF/F|"
    )


# =============================================================================
# SESSION AGGREGATION / STATISTICS
# =============================================================================

def aggregate_sessions(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    """One row per session x class, retaining within-session SD columns."""
    rows=[]
    group_cols=["subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode"]
    response_cols,_,_=response_columns(df,mode)
    for keys,sdf in df.groupby(group_cols,dropna=False):
        row=dict(zip(group_cols,keys)); n=len(sdf)
        row["n_cells"]=int(n)
        row["n_stim_responsive_fdr"]=int(sdf.stim_responsive_fdr.astype(bool).sum())
        row["pct_stim_responsive_fdr"]=100*float(sdf.stim_responsive_fdr.astype(bool).mean()) if n else np.nan
        row["pct_stim_excited_fdr"]=100*float(sdf.stim_excited_fdr.astype(bool).mean()) if n else np.nan
        row["pct_stim_suppressed_fdr"]=100*float(sdf.stim_suppressed_fdr.astype(bool).mean()) if n else np.nan
        for metric,cfg in CONTINUOUS_METRICS.items():
            if metric not in sdf:
                row[metric]=np.nan; row[f"sd_{metric}"]=np.nan; continue
            vals=finite_values(sdf[metric])
            if len(vals)==0:
                row[metric]=np.nan; row[f"sd_{metric}"]=np.nan
            elif cfg["session_agg"]=="median":
                row[metric]=float(np.median(vals)); row[f"sd_{metric}"]=float(np.std(vals,ddof=1)) if len(vals)>1 else np.nan
            else:
                row[metric]=float(np.mean(vals)); row[f"sd_{metric}"]=float(np.std(vals,ddof=1)) if len(vals)>1 else np.nan
        for col in response_cols:
            vals=finite_values(sdf[col]); row[col]=float(np.mean(vals)) if len(vals) else np.nan
            row[f"sd_{col}"]=float(np.std(vals,ddof=1)) if len(vals)>1 else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def analyze_continuous_metric(cell_df:pd.DataFrame,session_df:pd.DataFrame,metric:str,areas:list[str]) -> dict[str,Any]:
    pooled={a:cell_df.loc[cell_df.canonicalArea==a,metric] for a in areas}
    sess={a:session_df.loc[session_df.canonicalArea==a,metric] for a in areas}
    pooled_summary={}; session_summary={}
    for a in areas:
        m,se,n=mean_sem(pooled[a]); med,q1,q3,_=median_iqr(pooled[a])
        pooled_summary[a]={"n_cells":n,"mean":m,"sem":se,"median":med,"q1":q1,"q3":q3}
        m,se,n=mean_sem(sess[a]); med,q1,q3,_=median_iqr(sess[a])
        session_summary[a]={"n_sessions":n,"mean":m,"sem":se,"median":med,"q1":q1,"q3":q3}
    return {
        "label":CONTINUOUS_METRICS[metric]["label"],
        "session_aggregation":CONTINUOUS_METRICS[metric]["session_agg"],
        "pooled_cell_exploratory":{
            "summary":pooled_summary,"omnibus_kruskal":safe_kruskal(pooled),
            "pairwise_mannwhitney_holm":pairwise_area_tests(pooled,areas),
        },
        "session_level_primary":{
            "summary":session_summary,"omnibus_kruskal":safe_kruskal(sess),
            "pairwise_mannwhitney_holm":pairwise_area_tests(sess,areas),
        },
    }


def analyze_binary_metric(cell_df:pd.DataFrame,session_df:pd.DataFrame,metric:str,areas:list[str]) -> dict[str,Any]:
    pct_col={
        "stim_responsive_fdr":"pct_stim_responsive_fdr",
        "stim_excited_fdr":"pct_stim_excited_fdr",
        "stim_suppressed_fdr":"pct_stim_suppressed_fdr",
    }[metric]
    pooled_summary={}; session_summary={}; session_groups={}
    for a in areas:
        cdf=cell_df[cell_df.canonicalArea==a]; n=len(cdf); pos=int(cdf[metric].astype(bool).sum()) if n else 0
        pooled_summary[a]={"n_cells":n,"positive":pos,"percent":100*pos/n if n else np.nan}
        vals=session_df.loc[session_df.canonicalArea==a,pct_col]; session_groups[a]=vals
        m,se,ns=mean_sem(vals); session_summary[a]={"n_sessions":ns,"mean_percent":m,"sem_percent":se}
    return {
        "label":BINARY_METRICS[metric],
        "pooled_cell_exploratory":{"summary":pooled_summary,"pairwise_fisher_holm":fisher_pairwise_binary(cell_df,metric,areas)},
        "session_level_primary":{
            "summary":session_summary,"omnibus_kruskal":safe_kruskal(session_groups),
            "pairwise_mannwhitney_holm":pairwise_area_tests(session_groups,areas),
        },
    }


def run_statistics(cell_df:pd.DataFrame,session_df:pd.DataFrame,areas:list[str],include_binary:bool=True) -> dict[str,Any]:
    out={"continuous":{},"binary":{}}
    for metric in CONTINUOUS_METRICS:
        if metric in cell_df.columns: out["continuous"][metric]=analyze_continuous_metric(cell_df,session_df,metric,areas)
    if include_binary:
        for metric in BINARY_METRICS:
            if metric in cell_df.columns: out["binary"][metric]=analyze_binary_metric(cell_df,session_df,metric,areas)
    return out


def tuning_value_statistics(cell_df:pd.DataFrame,mode:str,areas:list[str],responsive_only:bool) -> pd.DataFrame:
    df=cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
    sdf=aggregate_sessions(df,mode) if len(df) else pd.DataFrame()
    cols,values,_=response_columns(df,mode)
    rows=[]
    for col,val in zip(cols,values):
        groups={a:sdf.loc[sdf.canonicalArea==a,col] if len(sdf) else [] for a in areas}
        omni=safe_kruskal(groups); pair=pairwise_area_tests(groups,areas)
        for key,rec in pair.items():
            rows.append({
                "subset":"FDR_responsive_only" if responsive_only else "all_cells",
                "tuning_mode":mode,"tuning_value_Hz":val,"response_column":col,
                "omnibus_H":omni["H"],"omnibus_p":omni["p"],
                "area1":rec["area1"],"area2":rec["area2"],"n1_sessions":rec["n1"],"n2_sessions":rec["n2"],
                "U":rec["U"],"p":rec["p"],"p_holm_within_value":rec["p_holm"],"cliffs_delta":rec["cliffs_delta"],
            })
    out=pd.DataFrame(rows)
    if len(out): out["p_holm_global"] = holm_adjust(out.p.tolist())
    return out


def condition_statistics(cond_df:pd.DataFrame,areas:list[str],metric:str,responsive_only:bool) -> pd.DataFrame:
    df=cond_df[cond_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cond_df.copy()
    group_cols=["canonicalArea","session_key","tuning_value_Hz","intensity_dB"]
    session=df.groupby(group_cols,dropna=False)[metric].mean().reset_index() if len(df) else pd.DataFrame(columns=group_cols+[metric])
    rows=[]
    for (value,intensity),sdf in session.groupby(["tuning_value_Hz","intensity_dB"],dropna=False):
        groups={a:sdf.loc[sdf.canonicalArea==a,metric] for a in areas}
        omni=safe_kruskal(groups); pair=pairwise_area_tests(groups,areas)
        for _,rec in pair.items():
            rows.append({
                "subset":"FDR_responsive_only" if responsive_only else "all_cells",
                "metric":metric,"tuning_value_Hz":value,"intensity_dB":intensity,
                "omnibus_H":omni["H"],"omnibus_p":omni["p"],
                "area1":rec["area1"],"area2":rec["area2"],"n1_sessions":rec["n1"],"n2_sessions":rec["n2"],
                "U":rec["U"],"p":rec["p"],"p_holm_within_condition":rec["p_holm"],"cliffs_delta":rec["cliffs_delta"],
            })
    out=pd.DataFrame(rows)
    if len(out): out["p_holm_global"] = holm_adjust(out.p.tolist())
    return out


# =============================================================================
# PLOTTING HELPERS
# =============================================================================

def optimized_ylim_from_summary(means:np.ndarray,errors:np.ndarray|None=None,reference_values:list[float]|None=None,pad_fraction:float=0.18):
    means=np.asarray(means,dtype=float); finite=np.isfinite(means)
    if not np.any(finite): return None
    if errors is None: errors=np.zeros_like(means)
    errors=np.asarray(errors,dtype=float)
    low=means-np.nan_to_num(errors,nan=0.0); high=means+np.nan_to_num(errors,nan=0.0)
    vals=np.r_[low[np.isfinite(low)],high[np.isfinite(high)]]
    if reference_values: vals=np.r_[vals,np.asarray(reference_values,dtype=float)]
    vals=vals[np.isfinite(vals)]
    if len(vals)==0:return None
    lo,hi=float(np.min(vals)),float(np.max(vals)); span=hi-lo
    if span<=0: span=max(abs(lo),abs(hi),1.0)*.25
    return lo-pad_fraction*span,hi+pad_fraction*span


def robust_cell_ylim(values: Iterable[Any], reference: float|None=None):
    vals=finite_values(values)
    if len(vals)==0:return None
    if len(vals)>=4:
        q1,q3=np.percentile(vals,[25,75]); iqr=q3-q1
        if np.isfinite(iqr) and iqr>0:
            keep=vals[(vals>=q1-3*iqr)&(vals<=q3+3*iqr)]
            if len(keep): vals_for_range=keep
            else: vals_for_range=vals
        else: vals_for_range=vals
    else: vals_for_range=vals
    lo,hi=float(np.min(vals_for_range)),float(np.max(vals_for_range))
    if reference is not None and np.isfinite(reference): lo=min(lo,reference); hi=max(hi,reference)
    span=hi-lo
    if span<=0: span=max(abs(lo),abs(hi),1.0)*.25
    return lo-.10*span,hi+.16*span


def annotate_mean_sem(ax,x,mean,sem,n,color,y_top=None):
    if not np.isfinite(mean): return
    semtxt=f"{sem:.4g}" if np.isfinite(sem) else "n/a"; txt=f"{mean:.4g} +/- {semtxt}\nn={n}"
    if y_top is None: ax.annotate(txt,(x,mean),xytext=(0,10),textcoords="offset points",ha="center",va="bottom",fontsize=7.2,color=color)
    else: ax.text(x,y_top,txt,ha="center",va="top",fontsize=7.2,color=color)


def plot_metric_grid(cell_df,session_df,areas,cell_class,depth_label,mode,output_path,display_mode,subset_label):
    metrics=[m for m in CONTINUOUS_METRICS if m in cell_df.columns]
    if not metrics:return
    ncols=3; nrows=math.ceil(len(metrics)/ncols)
    fig,axes=plt.subplots(nrows,ncols,figsize=(16.5,4.8*nrows),squeeze=False); axes=axes.ravel(); rng=np.random.default_rng(0)
    for ax,metric in zip(axes,metrics):
        ref=CONTINUOUS_METRICS[metric]["reference"]; x=np.arange(len(areas),dtype=float); display=[]
        if display_mode=="with_cells":
            for xi,area in enumerate(areas):
                vals=finite_values(cell_df.loc[cell_df.canonicalArea==area,metric])
                if len(vals):
                    ax.scatter(np.full(len(vals),xi)+rng.uniform(-.08,.08,len(vals)),vals,s=12,alpha=.20,color=AREA_COLORS[area],edgecolors="none")
                    m,_,se,n=mean_sd_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=8,capsize=5,elinewidth=2,color=AREA_COLORS[area],zorder=5)
                    display.extend(vals.tolist())
            subtitle="individual cells; dark = pooled mean +/- SEM (exploratory)"
        else:
            for xi,area in enumerate(areas):
                sdf=session_df[session_df.canonicalArea==area]
                offsets=np.linspace(-.07,.07,max(len(sdf),1))
                for off,(_,row) in zip(offsets,sdf.iterrows()):
                    m=float(row.get(metric,np.nan)); sd=float(row.get(f"sd_{metric}",np.nan))
                    if np.isfinite(m):
                        ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=3.5,elinewidth=.75,capsize=2,color=AREA_COLORS[area],alpha=.28,zorder=2)
                        display.append(m)
                        if np.isfinite(sd): display.extend([m-sd,m+sd])
                vals=finite_values(sdf[metric]) if metric in sdf else np.array([]); m,_,se,n=mean_sd_sem(vals)
                if np.isfinite(m):
                    ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,elinewidth=2.6,color=AREA_COLORS[area],zorder=6)
                    annotate_mean_sem(ax,xi,m,se,n,AREA_COLORS[area]); display.append(m)
                    if np.isfinite(se): display.extend([m-se,m+se])
            subtitle="light = session mean +/- SD; dark = overall mean +/- SEM"
        if ref is not None: ax.axhline(ref,ls="--",lw=.9,color=".45")
        ax.set_xticks(x,areas); ax.set_ylabel(metric_label(metric,mode)); ax.set_title(metric_label(metric,mode),fontsize=10); ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False)
        ylim=robust_cell_ylim(display,ref)
        if ylim: ax.set_ylim(*ylim)
    for ax in axes[len(metrics):]: ax.axis("off")
    fig.suptitle(f"{cell_class.upper()} cells across A1 / AAF / A2 — {depth_label}\n{mode_title(mode)} — {subset_label}: {subtitle}",fontsize=14)
    fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_responsiveness(cell_df,session_df,areas,cell_class,depth_label,mode,outdir):
    metrics=[("stim_responsive_fdr","pct_stim_responsive_fdr","Responsive"),("stim_excited_fdr","pct_stim_excited_fdr","Excited"),("stim_suppressed_fdr","pct_stim_suppressed_fdr","Suppressed")]
    fig,axes=plt.subplots(1,3,figsize=(14.5,4.8));
    for ax,(cell_col,pct_col,label) in zip(axes,metrics):
        x=np.arange(len(areas));
        for xi,area in enumerate(areas):
            sdf=session_df[session_df.canonicalArea==area]; vals=finite_values(sdf[pct_col]) if pct_col in sdf else np.array([])
            if len(vals): ax.scatter(np.full(len(vals),xi)+np.linspace(-.05,.05,len(vals)),vals,s=24,alpha=.3,color=AREA_COLORS[area])
            m,_,se,n=mean_sd_sem(vals)
            if np.isfinite(m): ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=5,elinewidth=2.2,color=AREA_COLORS[area]); annotate_mean_sem(ax,xi,m,se,n,AREA_COLORS[area])
        ax.set_xticks(x,areas); ax.set_ylabel("Session percentage (%)"); ax.set_title(label); ax.grid(axis="y",alpha=.25); ax.spines[["top","right"]].set_visible(False)
    fig.suptitle(f"{cell_class.upper()} | {mode_title(mode)} | {depth_label}\nSession-level responsiveness",fontsize=13); fig.tight_layout(rect=[0,0,1,.92]); fig.savefig(outdir/"responsiveness_session_mean_sem_only.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profile_pooled(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    cols,values,_=response_columns(cell_df,mode)
    if not cols:return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(9.5,5.9)); allm=[]; alle=[]
    for area in areas:
        means=[]; sems=[]
        for col in cols:
            m,se,n=mean_sem(cell_df.loc[cell_df.canonicalArea==area,col]); means.append(m); sems.append(se)
        allm.extend(means); alle.extend(sems); ax.errorbar(x,means,yerr=sems,marker="o",capsize=4,lw=2,color=AREA_COLORS[area],label=area)
    ylim=optimized_ylim_from_summary(np.asarray(allm),np.asarray(alle),[0]);
    if ylim: ax.set_ylim(*ylim)
    ax.axhline(0,ls="--",lw=1,color=".45"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Response (dF/F)"); apply_log2_tuning_axis(ax,values,mode)
    ax.set_title(f"{cell_class.upper()} across areas — {depth_label}\n{mode_title(mode)} | pooled cells mean +/- SEM (exploratory) | {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_POOLED_CELL_MEAN_SEM.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profile_session(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    sdf=aggregate_sessions(cell_df,mode) if len(cell_df) else pd.DataFrame(); cols,values,_=response_columns(cell_df,mode)
    if not cols or len(sdf)==0:return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(10,6.3)); display=[]
    for area in areas:
        adf=sdf[sdf.canonicalArea==area]; profiles=[]
        for _,row in adf.iterrows():
            means=np.asarray([row.get(c,np.nan) for c in cols],float); sds=np.asarray([row.get(f"sd_{c}",np.nan) for c in cols],float); profiles.append(means)
            ax.plot(x,means,color=AREA_COLORS[area],alpha=.24,lw=1,marker="o",ms=2.5,zorder=1)
            if np.any(np.isfinite(sds)): ax.fill_between(x,means-sds,means+sds,color=AREA_COLORS[area],alpha=.035,zorder=0)
            display.extend(finite_values(means).tolist()); display.extend(finite_values(np.r_[means-sds,means+sds]).tolist())
        if profiles:
            mat=np.vstack(profiles); overall=np.nanmean(mat,axis=0); sem=np.asarray([stats.sem(mat[:,i],nan_policy="omit") if np.sum(np.isfinite(mat[:,i]))>1 else np.nan for i in range(len(cols))])
            ax.errorbar(x,overall,yerr=sem,fmt="o-",color=AREA_COLORS[area],lw=2.8,ms=5.5,elinewidth=2,capsize=4,label=f"{area} overall ({len(profiles)} sessions)",zorder=5)
    ax.axhline(0,ls="--",lw=1,color=".45"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Session mean response (dF/F)"); apply_log2_tuning_axis(ax,values,mode)
    ax.set_title(f"{cell_class.upper()} across areas — {depth_label}\n{mode_title(mode)} | light=session mean +/- SD; dark=overall mean +/- SEM | {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False); fig.tight_layout()
    fig.savefig(outdir/f"tuning_profile_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profiles_sessions_top_cells(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    cols,values,_=response_columns(cell_df,mode)
    if not cols or "tuning_lifetime_sparseness" not in cell_df:return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(10,6.2))
    for area in areas:
        adf=cell_df[cell_df.canonicalArea==area]
        for _,sdf in adf.groupby("session_key",sort=True):
            mat=sdf[cols].to_numpy(float)
            if len(mat)==0:continue
            rank=pd.to_numeric(sdf.tuning_lifetime_sparseness,errors="coerce").to_numpy(float); valid=np.flatnonzero(np.isfinite(rank)); valid=valid[np.argsort(rank[valid])[::-1]][:5]
            for ridx in valid: ax.plot(x,mat[ridx],color=AREA_COLORS[area],alpha=.12,lw=.8,ls="--",zorder=1)
            ax.plot(x,np.nanmean(mat,axis=0),color=AREA_COLORS[area],alpha=.58,lw=1.7,marker="o",ms=3,zorder=3)
    ax.axhline(0,ls="--",lw=1,color=".45"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Response (dF/F)"); apply_log2_tuning_axis(ax,values,mode)
    ax.set_title(f"{cell_class.upper()} across areas — {depth_label}\nsolid=session means; dashed=top 5 cells/session by lifetime sparseness | {suffix.replace('_',' ')}")
    ax.legend(handles=[plt.Line2D([0],[0],color=AREA_COLORS[a],lw=2,label=f"{a} session mean") for a in areas]+[plt.Line2D([0],[0],color="0.35",lw=1,ls="--",alpha=.5,label="High-sparseness cell")],frameon=False)
    ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_MEANS_TOP5_CELLS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_preferred_distribution(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    vals=np.sort(pd.to_numeric(cell_df.preferred_tuning_value_Hz,errors="coerce").dropna().unique())
    if len(vals)==0:return
    x=xplot(vals,mode); fig,ax=plt.subplots(figsize=(9,5.4))
    for area in areas:
        adf=cell_df[cell_df.canonicalArea==area]; pref=pd.to_numeric(adf.preferred_tuning_value_Hz,errors="coerce").to_numpy(float); total=np.sum(np.isfinite(pref)); pct=np.asarray([100*np.sum(np.isclose(pref,v,equal_nan=False))/total if total else np.nan for v in vals])
        ax.plot(x,pct,marker="o",lw=2,color=AREA_COLORS[area],label=f"{area} (n={len(adf)})")
    apply_log2_tuning_axis(ax,vals,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Cells preferring value (%)"); ax.set_ylim(bottom=0)
    ax.set_title(f"{cell_class.upper()} preferred tuning across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig(outdir/f"preferred_tuning_distribution_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_selectivity_rasters(cell_df,areas,cell_class,depth_label,mode,outdir,suffix,sort_metric="preferred_tuning_value_Hz",stem_extra=""):
    cols,values,labels=response_columns(cell_df,mode)
    if len(cols)<2:return
    fig,axes=plt.subplots(len(areas),1,figsize=(10,3.6*len(areas)),squeeze=False); im=None; edges=log2_bin_edges(values,mode)
    for row,area in enumerate(areas):
        ax=axes[row,0]; adf=cell_df[cell_df.canonicalArea==area].copy()
        if len(adf)==0: ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center",va="center"); ax.set_axis_off(); continue
        mat=adf[cols].to_numpy(float); denom=np.nanmax(np.abs(mat),axis=1); good=np.isfinite(denom)&(denom>0); mat=mat[good]; adf=adf.iloc[np.where(good)[0]].copy()
        if len(mat)==0:continue
        norm=mat/denom[good,None]; rank=pd.to_numeric(adf.get(sort_metric,np.nan),errors="coerce").to_numpy(float)
        order=np.argsort(np.nan_to_num(rank,nan=-np.inf))[::-1] if sort_metric=="tuning_lifetime_sparseness" else np.argsort(np.nan_to_num(rank,nan=np.inf)); norm=norm[order]
        if edges is not None:
            yedges=np.arange(len(norm)+1,dtype=float); im=ax.pcolormesh(edges,yedges,norm,cmap="coolwarm",vmin=-1,vmax=1,shading="flat"); ax.set_ylim(len(norm),0); apply_log2_tuning_axis(ax,values,mode)
        else:
            im=ax.imshow(norm,aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm"); ax.set_xticks(np.arange(len(labels)),labels,rotation=30,ha="right")
        ax.set_ylabel(f"{area} cells"); ax.set_xlabel(mode_axis_label(mode)); ax.set_title(f"{area}: n={len(norm)} | sorted by {'lifetime sparseness' if sort_metric=='tuning_lifetime_sparseness' else 'preferred tuning'}")
    fig.suptitle(f"{cell_class.upper()} tuning rasters across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')}",y=1.01)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Normalized tuning response",shrink=.75)
    fig.subplots_adjust(left=.09,right=.88,bottom=.10,top=.92,hspace=.48); fig.savefig(outdir/f"selectivity_rasters_{suffix}{stem_extra}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_standalone_selectivity_across_areas(cell_df,session_df,areas,cell_class,depth_label,mode,outdir,suffix,stats_out):
    rng=np.random.default_rng(20260819)
    for metric in SELECTIVITY_METRICS:
        if metric not in cell_df:continue
        label=metric_label(metric,mode); stem=metric.replace("tuning_",""); ref=CONTINUOUS_METRICS[metric]["reference"]
        # Individual cells.
        fig,ax=plt.subplots(figsize=(7.6,6.4)); display=[]
        for xi,area in enumerate(areas):
            vals=finite_values(cell_df.loc[cell_df.canonicalArea==area,metric])
            if len(vals):
                ax.scatter(np.full(len(vals),xi)+rng.uniform(-.09,.09,len(vals)),vals,s=20,alpha=.22,color=AREA_COLORS[area],edgecolors="none")
                m,_,se,n=mean_sd_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,elinewidth=2.4,color=AREA_COLORS[area],zorder=5); display.extend(vals.tolist())
        p=stats_out.get("continuous",{}).get(metric,{}).get("pooled_cell_exploratory",{}).get("omnibus_kruskal",{}).get("p",np.nan)
        ax.set_xticks(np.arange(len(areas)),areas); ax.set_ylabel(label); ax.set_title(f"{cell_class.upper()} — {depth_label} — {mode_title(mode)}\n{label}\nindividual cells; exploratory omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} — {depth_label} — {mode_title(mode)}\n{label}\nindividual cells")
        ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False); ylim=robust_cell_ylim(display,ref); 
        if ylim: ax.set_ylim(*ylim)
        fig.text(.5,.015,selectivity_equation_footer(mode),ha="center",va="bottom",fontsize=8.5); fig.subplots_adjust(bottom=.16); fig.savefig(outdir/f"{stem}_across_areas_{suffix}_CELL_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)
        # Session points: light session mean +/- SD, dark overall mean +/- SEM.
        fig,ax=plt.subplots(figsize=(7.6,6.4)); display=[]
        for xi,area in enumerate(areas):
            sdf=session_df[session_df.canonicalArea==area]; offsets=np.linspace(-.07,.07,max(len(sdf),1))
            for off,(_,row) in zip(offsets,sdf.iterrows()):
                m=float(row.get(metric,np.nan)); sd=float(row.get(f"sd_{metric}",np.nan))
                if np.isfinite(m):
                    ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=4,elinewidth=.8,capsize=2,color=AREA_COLORS[area],alpha=.30,zorder=2); display.append(m)
                    if np.isfinite(sd): display.extend([m-sd,m+sd])
            vals=finite_values(sdf[metric]) if metric in sdf else np.array([]); m,_,se,n=mean_sd_sem(vals)
            if np.isfinite(m): ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=11,elinewidth=2.8,capsize=7,color=AREA_COLORS[area],zorder=6); annotate_mean_sem(ax,xi,m,se,n,AREA_COLORS[area])
        p=stats_out.get("continuous",{}).get(metric,{}).get("session_level_primary",{}).get("omnibus_kruskal",{}).get("p",np.nan)
        ax.set_xticks(np.arange(len(areas)),areas); ax.set_ylabel(label); ax.set_title(f"{cell_class.upper()} — {depth_label} — {mode_title(mode)}\n{label}\nlight=session mean +/- SD; dark=overall mean +/- SEM\nsession-level omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} — {depth_label} — {mode_title(mode)}\n{label}\nsession points")
        ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False); ylim=robust_cell_ylim(display,ref)
        if ylim: ax.set_ylim(*ylim)
        fig.text(.5,.015,selectivity_equation_footer(mode),ha="center",va="bottom",fontsize=8.5); fig.subplots_adjust(bottom=.16); fig.savefig(outdir/f"{stem}_across_areas_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_intensity_condition_grid(cond_df,areas,cell_class,depth_label,mode,outdir,suffix,metric,label,filename):
    if len(cond_df)==0:return
    intens=np.sort(pd.to_numeric(cond_df.intensity_dB,errors="coerce").dropna().unique()); values=np.sort(pd.to_numeric(cond_df.tuning_value_Hz,errors="coerce").dropna().unique())
    if len(intens)==0 or len(values)==0:return
    x=xplot(values,mode)
    # Exploratory pooled-cell figure.
    ncols=2; nrows=math.ceil(len(intens)/ncols); fig,axes=plt.subplots(nrows,ncols,figsize=(13,4.5*nrows),squeeze=False); axes=axes.ravel()
    for ax,intensity in zip(axes,intens):
        for area in areas:
            means=[]; sems=[]
            for value in values:
                vals=cond_df.loc[(cond_df.canonicalArea==area)&np.isclose(cond_df.intensity_dB,intensity)&np.isclose(cond_df.tuning_value_Hz,value),metric]; m,se,n=mean_sem(vals); means.append(m); sems.append(se)
            ax.errorbar(x,means,yerr=sems,marker="o",capsize=3,lw=1.8,color=AREA_COLORS[area],label=area)
        ax.axhline(0,ls="--",lw=.8,color=".5"); ax.set_title(f"{intensity:g} dB"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel(label); apply_log2_tuning_axis(ax,values,mode); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
    for ax in axes[len(intens):]:ax.set_axis_off()
    handles,labs=axes[0].get_legend_handles_labels(); fig.legend(handles,labs,frameon=False,loc="upper right"); fig.suptitle(f"{cell_class.upper()} across areas — {depth_label}\n{mode_title(mode)} | pooled cells mean +/- SEM (exploratory) | {suffix.replace('_',' ')}",y=.995); fig.tight_layout(rect=[0,0,.97,.96]); fig.savefig(outdir/f"{filename}_{suffix}_POOLED_CELL_MEAN_SEM.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)
    # Session-aware figure.
    group=["canonicalArea","session_key","tuning_value_Hz","intensity_dB"]
    sess_mean=cond_df.groupby(group,dropna=False)[metric].mean().reset_index(); sess_sd=cond_df.groupby(group,dropna=False)[metric].std(ddof=1).reset_index().rename(columns={metric:"within_sd"}); sess=sess_mean.merge(sess_sd,on=group,how="left")
    fig,axes=plt.subplots(nrows,ncols,figsize=(13,4.7*nrows),squeeze=False); axes=axes.ravel()
    for ax,intensity in zip(axes,intens):
        for area in areas:
            adf=sess[(sess.canonicalArea==area)&np.isclose(sess.intensity_dB,intensity)]; profiles=[]
            for sk,sdf in adf.groupby("session_key",sort=True):
                means=[]; sds=[]
                for value in values:
                    row=sdf[np.isclose(sdf.tuning_value_Hz,value)]
                    means.append(float(row.iloc[0][metric]) if len(row) else np.nan); sds.append(float(row.iloc[0]["within_sd"]) if len(row) else np.nan)
                means=np.asarray(means,float); sds=np.asarray(sds,float); profiles.append(means); ax.plot(x,means,color=AREA_COLORS[area],alpha=.22,lw=.9,marker="o",ms=2.2)
                if np.any(np.isfinite(sds)): ax.fill_between(x,means-sds,means+sds,color=AREA_COLORS[area],alpha=.028)
            if profiles:
                mat=np.vstack(profiles); overall=np.nanmean(mat,axis=0); sem=np.asarray([stats.sem(mat[:,i],nan_policy="omit") if np.sum(np.isfinite(mat[:,i]))>1 else np.nan for i in range(len(values))]); ax.errorbar(x,overall,yerr=sem,fmt="o-",lw=2.5,ms=4.5,elinewidth=1.8,capsize=3,color=AREA_COLORS[area],label=area)
        ax.axhline(0,ls="--",lw=.8,color=".5"); ax.set_title(f"{intensity:g} dB"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel(label); apply_log2_tuning_axis(ax,values,mode); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
    for ax in axes[len(intens):]:ax.set_axis_off()
    handles,labs=axes[0].get_legend_handles_labels(); fig.legend(handles,labs,frameon=False,loc="upper right"); fig.suptitle(f"{cell_class.upper()} across areas — {depth_label}\n{mode_title(mode)} | light=session means +/- SD; dark=overall mean +/- SEM | {suffix.replace('_',' ')}",y=.995); fig.tight_layout(rect=[0,0,.97,.96]); fig.savefig(outdir/f"{filename}_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def make_figures(cell_df,cond_df,areas,cell_class,depth_label,mode,outdir,responsive_only,stats_out=None):
    suffix="FDR_responsive_only" if responsive_only else "all_cells"; subset="FDR stimulus-responsive cells only" if responsive_only else "All classified cells"
    cdf=cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy(); qdf=cond_df[cond_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cond_df.copy(); sdf=aggregate_sessions(cdf,mode) if len(cdf) else pd.DataFrame()
    current_stats=run_statistics(cdf,sdf,areas,include_binary=False) if len(cdf) else {"continuous":{},"binary":{}}
    plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,mode,outdir/f"cross_area_tuning_metrics_{suffix}_with_cells.png","with_cells",subset)
    plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,mode,outdir/f"cross_area_tuning_metrics_{suffix}_MEAN_SEM_ONLY.png","session_mean",subset)
    if len(sdf): plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,mode,outdir/f"cross_area_tuning_metrics_{suffix}_SESSION_MEAN_SEM_ONLY.png","session_mean",subset)
    plot_tuning_profile_pooled(cdf,areas,cell_class,depth_label,mode,outdir,suffix); plot_tuning_profile_session(cdf,areas,cell_class,depth_label,mode,outdir,suffix); plot_tuning_profiles_sessions_top_cells(cdf,areas,cell_class,depth_label,mode,outdir,suffix)
    plot_preferred_distribution(cdf,areas,cell_class,depth_label,mode,outdir,suffix); plot_selectivity_rasters(cdf,areas,cell_class,depth_label,mode,outdir,suffix); plot_selectivity_rasters(cdf,areas,cell_class,depth_label,mode,outdir,suffix,"tuning_lifetime_sparseness","_LIFETIME_SPARSENESS")
    plot_standalone_selectivity_across_areas(cdf,sdf,areas,cell_class,depth_label,mode,outdir,suffix,current_stats)
    plot_intensity_condition_grid(qdf,areas,cell_class,depth_label,mode,outdir,suffix,"condition_response","Condition response (dF/F)","intensity_condition_response_profile"); plot_intensity_condition_grid(qdf,areas,cell_class,depth_label,mode,outdir,suffix,"condition_selectivity_contrast","Condition selectivity contrast (dF/F)","intensity_condition_selectivity_profile")


def add_layer_columns(df: pd.DataFrame) -> pd.DataFrame:
    out=df.copy(); depth=pd.to_numeric(out["depth"],errors="coerce"); out["layer_key"]=np.where((depth>=100)&(depth<300),"L23",np.where((depth>=300)&(depth<=600),"L45",None)); out["layer_label"]=pd.Series(out["layer_key"],index=out.index).map({"L23":"L2/3","L45":"L4/5"}); out["area_layer"]=np.where(pd.notna(out["layer_key"]),out["canonicalArea"].astype(str)+"-"+out["layer_label"].astype(str),None); return out


def area_layer_order(areas:list[str])->list[str]:
    return [f"{a}-L2/3" for a in areas]+[f"{a}-L4/5" for a in areas]


def run_area_layer_statistics(cell_df,session_df,categories):
    out={"continuous":{}}
    for metric,cfg in CONTINUOUS_METRICS.items():
        if metric not in cell_df:continue
        pooled={c:cell_df.loc[cell_df.area_layer==c,metric] for c in categories}; sess={c:session_df.loc[session_df.area_layer==c,metric] for c in categories}
        out["continuous"][metric]={"label":cfg["label"],"pooled_cell_exploratory":{"omnibus_kruskal":safe_kruskal(pooled),"pairwise_mannwhitney_holm":pairwise_area_tests(pooled,categories)},"session_level_primary":{"omnibus_kruskal":safe_kruskal(sess),"pairwise_mannwhitney_holm":pairwise_area_tests(sess,categories)}}
    return out


def plot_area_layer_metric(cell_df,session_df,categories,cell_class,metric,mode,outdir,suffix,stats_out):
    if metric not in cell_df:return
    ref=CONTINUOUS_METRICS[metric]["reference"]; rng=np.random.default_rng(1827); x=np.arange(len(categories),dtype=float); label=metric_label(metric,mode)
    for kind in ("CELL_POINTS","SESSION_POINTS"):
        fig,ax=plt.subplots(figsize=(11,6.4)); display=[]
        for xi,cat in enumerate(categories):
            area=cat.split("-")[0]
            if kind=="CELL_POINTS":
                vals=finite_values(cell_df.loc[cell_df.area_layer==cat,metric])
                if len(vals):
                    ax.scatter(np.full(len(vals),xi)+rng.uniform(-.08,.08,len(vals)),vals,s=16,alpha=.20,color=AREA_COLORS.get(area,".4"),edgecolors="none"); m,_,se,n=mean_sd_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=8,elinewidth=2,capsize=5,color=AREA_COLORS.get(area,".4")); display.extend(vals.tolist())
            else:
                sdf=session_df[session_df.area_layer==cat]; offsets=np.linspace(-.06,.06,max(len(sdf),1))
                for off,(_,row) in zip(offsets,sdf.iterrows()):
                    m=float(row.get(metric,np.nan)); sd=float(row.get(f"sd_{metric}",np.nan))
                    if np.isfinite(m): ax.errorbar(xi+off,m,yerr=sd if np.isfinite(sd) else None,fmt="o",ms=3.8,elinewidth=.7,capsize=2,color=AREA_COLORS.get(area,".4"),alpha=.28); display.append(m); display.extend([m-sd,m+sd] if np.isfinite(sd) else [])
                vals=finite_values(sdf[metric]) if metric in sdf else np.array([]); m,_,se,n=mean_sd_sem(vals)
                if np.isfinite(m): ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,elinewidth=2.6,capsize=6,color=AREA_COLORS.get(area,".4"),zorder=5); annotate_mean_sem(ax,xi,m,se,n,AREA_COLORS.get(area,".4"))
        if ref is not None:ax.axhline(ref,ls="--",lw=1,color=".45")
        branch="pooled_cell_exploratory" if kind=="CELL_POINTS" else "session_level_primary"; p=stats_out.get("continuous",{}).get(metric,{}).get(branch,{}).get("omnibus_kruskal",{}).get("p",np.nan)
        ax.set_xticks(x,categories,rotation=30,ha="right"); ax.set_ylabel(label); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False); ax.set_title(f"{cell_class.upper()} across area x layer — {mode_title(mode)}\n{label} — {suffix.replace('_',' ')}\n{'individual cells; exploratory' if kind=='CELL_POINTS' else 'light=session mean +/- SD; dark=overall mean +/- SEM'}; omnibus p={p:.3g}" if np.isfinite(p) else f"{cell_class.upper()} across area x layer — {mode_title(mode)}\n{label}")
        ylim=robust_cell_ylim(display,ref)
        if ylim:ax.set_ylim(*ylim)
        if metric in SELECTIVITY_METRICS: fig.text(.5,.015,selectivity_equation_footer(mode),ha="center",va="bottom",fontsize=8.2)
        fig.subplots_adjust(bottom=.25); fig.savefig(outdir/f"area_layer_{metric}_{suffix}_{kind}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def make_area_layer_outputs(all_cells,areas,mode,mode_root):
    layered=add_layer_columns(all_cells); layered=layered[layered.layer_key.notna()].copy(); categories=area_layer_order(areas); root=mode_root/"area_by_layer"; root.mkdir(parents=True,exist_ok=True); layered.to_csv(root/"all_area_layer_cells.csv",index=False)
    for cell_class in CELL_CLASSES:
        class_cells=layered[layered.cell_class==cell_class].copy(); class_out=root/cell_class; class_out.mkdir(parents=True,exist_ok=True)
        for responsive_only in (False,True):
            suffix="FDR_responsive_only" if responsive_only else "all_cells"; cdf=class_cells[class_cells.stim_responsive_fdr.astype(bool)].copy() if responsive_only else class_cells.copy(); sdf=aggregate_sessions(cdf,mode) if len(cdf) else pd.DataFrame()
            if len(sdf): sdf=add_layer_columns(sdf)
            stats_out=run_area_layer_statistics(cdf,sdf,categories) if len(cdf) else {"continuous":{}}; save_json(class_out/f"area_layer_statistics_{suffix}.json",stats_out)
            for metric in CONTINUOUS_METRICS: plot_area_layer_metric(cdf,sdf,categories,cell_class,metric,mode,class_out,suffix,stats_out)
        write_figure_index(class_out)


def write_figure_index(outdir:Path):
    pngs=sorted(outdir.glob("*.png")); lines=["FIGURE INDEX","============",""]+[p.name for p in pngs]; (outdir/"FIGURE_INDEX.txt").write_text("\n".join(lines)+"\n")


# =============================================================================
# REPORTING
# =============================================================================

def write_report(path,subject,dates,mode,cell_class,depth_label,cell_df,session_df,areas,stats_all,stats_resp):
    lines=["CROSS-AREA AM-TUNING CELL-CLASS ANALYSIS","="*78,f"Subject: {subject}",f"Dates: {', '.join(dates)}",f"Tuning mode: {mode}",f"Cell class: {cell_class.upper()}",f"Depth stratum: {depth_label}",""]
    lines.append("Counts:")
    for area in areas:
        adf=cell_df[cell_df.canonicalArea==area]; sdf=session_df[session_df.canonicalArea==area]
        lines.append(f"  {area}: {len(adf)} cells from {sdf.session_key.nunique() if len(sdf) else 0} sessions; FDR responsive={int(adf.stim_responsive_fdr.astype(bool).sum())}")
    lines += ["","PRIMARY INFERENCE: one summary value per imaging session.","Exploratory pooled-cell tests describe cell distributions but do not treat cells as independent biological replicates.",""]
    for subset_name,stats_out in (("ALL CLASSIFIED CELLS",stats_all),("FDR STIMULUS-RESPONSIVE CELLS ONLY",stats_resp)):
        lines += [subset_name,"-"*len(subset_name)]
        for metric,result in stats_out.get("continuous",{}).items():
            primary=result["session_level_primary"]; omni=primary["omnibus_kruskal"]; lines.append(result["label"])
            lines.append(f"  Session omnibus Kruskal-Wallis: H={omni['H']:.4g}, {p_text(omni['p'])}" if np.isfinite(omni["H"]) else "  Session omnibus Kruskal-Wallis: unavailable")
            for area in areas:
                s=primary["summary"][area]; lines.append(f"    {area}: mean={s['mean']:.4g}, SEM={s['sem']:.4g}, median={s['median']:.4g}, n_sessions={s['n_sessions']}")
            for _,rec in primary["pairwise_mannwhitney_holm"].items():
                if np.isfinite(rec["U"]): lines.append(f"    {rec['area1']} vs {rec['area2']}: U={rec['U']:.4g}, p={rec['p']:.4g}, Holm p={rec['p_holm']:.4g}, Cliff delta={rec['cliffs_delta']:.3g}")
                else: lines.append(f"    {rec['area1']} vs {rec['area2']}: unavailable")
            lines.append("")
    lines += ["RESPONSIVENESS / EXCITATION / SUPPRESSION","-"*44]
    for metric,result in stats_all.get("binary",{}).items():
        primary=result["session_level_primary"]; omni=primary["omnibus_kruskal"]; lines.append(result["label"])
        lines.append(f"  Session omnibus Kruskal-Wallis: H={omni['H']:.4g}, {p_text(omni['p'])}" if np.isfinite(omni["H"]) else "  Session omnibus Kruskal-Wallis: unavailable")
        for area in areas:
            s=primary["summary"][area]; lines.append(f"    {area}: {s['mean_percent']:.3g} ± {s['sem_percent']:.3g}% across n={s['n_sessions']} sessions")
        lines.append("")
    path.write_text("\n".join(lines)+"\n")


def save_quickview(outroot:Path,records:list[dict[str,Any]]):
    if records: pd.DataFrame(records).to_csv(outroot/"SESSION_LEVEL_PAIRWISE_QUICKVIEW.csv",index=False)


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    args=parse_args(); subject=str(args.subject); dates=[str(d) for d in args.dates]; areas=list(args.areas)
    modes=list(TUNING_MODES) if args.mode=="both" else [args.mode]
    outroot=output_root(subject,dates)
    print("="*78); print("AM_TUNING CROSS-AREA CELL-CLASS ANALYSIS"); print("="*78)
    print(f"Subject: {subject}"); print(f"Dates:   {', '.join(dates)}"); print(f"Areas:   {', '.join(areas)}"); print(f"Modes:   {', '.join(modes)}")
    print(f"Input root:  {Path(settings.TEMP_OUTPUT_PATH)/'evan'/'am_tuning_area_analysis'}"); print(f"Output root: {outroot}")
    print("\nExpected inputs:")
    all_paths={}
    for mode in modes:
        print(f"  {mode}:")
        all_paths[mode]={}
        for area in areas:
            cp=expected_area_cell_csv(subject,area,dates,mode); qp=expected_area_condition_csv(subject,area,dates,mode); all_paths[mode][area]={"cell":str(cp),"condition":str(qp)}
            status="FOUND" if cp.exists() and qp.exists() else "MISSING"
            print(f"    {area}: {cp.parent} [{status}]")
    if args.dry_run:
        print("\nDry run complete; no tables were loaded."); return
    outroot.mkdir(parents=True,exist_ok=True)
    save_json(outroot/"run_manifest.json",{
        "subject":subject,"dates":dates,"areas":areas,"modes":modes,"inputs":all_paths,"output_root":str(outroot),
        "depth_strata":{"all_depths":"all sessions","L23_100to300um":"100 <= depth < 300 um","L45_300to600um":"300 <= depth <= 600 um"},
        "primary_inference":"session-level summaries; unpaired cross-area Kruskal-Wallis and pairwise Mann-Whitney with Holm correction",
        "pooled_cell_inference":"exploratory/descriptive only",
        "prerequisite_area_analysis":"am_tuning_area_analysis_v9.py",
        "primary_tuning_selectivity_metric":"tuning_lifetime_sparseness",
        "selectivity_metrics":["tuning_lifetime_sparseness","tuning_gini_coefficient","tuning_fano_factor","tuning_fwhm"],
        "frequency_fwhm_units":"octaves","am_fwhm_units":"Hz",
        "numeric_tuning_axes":"base-2 logarithmic scale",
        "area_by_layer_outputs":"additional six-stratum A1/AAF/A2 x L2/3/L4/5 comparisons for each cell class",
    })
    quick=[]
    for mode in modes:
        print("\n"+"="*78); print(f"MODE: {mode}"); print("="*78)
        cells,conds,prov=load_mode_tables(subject,dates,areas,mode)
        cells=cells[cells.cell_class.isin(CELL_CLASSES)].copy(); conds=conds[conds.cell_class.isin(CELL_CLASSES)].copy()
        mode_root=outroot/mode; mode_root.mkdir(parents=True,exist_ok=True)
        cells.to_csv(mode_root/"all_areas_combined_cell_results.csv",index=False); conds.to_csv(mode_root/"all_areas_combined_condition_results.csv",index=False)
        print("Loaded:")
        for area in areas:
            adf=cells[cells.canonicalArea==area]; print(f"  {area}: {len(adf)} cells, {adf.session_key.nunique()} sessions")
        for depth_label in DEPTH_STRATA:
            dcells=subset_depth(cells,depth_label); dconds=subset_depth(conds,depth_label)
            print("\n"+"-"*78); print(f"Depth: {depth_label}")
            for area in areas:
                adf=dcells[dcells.canonicalArea==area]; print(f"  {area}: {len(adf)} cells, {adf.session_key.nunique()} sessions")
            for cell_class in CELL_CLASSES:
                cdf=dcells[dcells.cell_class==cell_class].copy(); qdf=dconds[dconds.cell_class==cell_class].copy(); leaf=mode_root/depth_label/cell_class; leaf.mkdir(parents=True,exist_ok=True)
                sdf=aggregate_sessions(cdf,mode); cdf.to_csv(leaf/"cell_results.csv",index=False); qdf.to_csv(leaf/"condition_results.csv",index=False); sdf.to_csv(leaf/"session_summary.csv",index=False)
                stats_all=run_statistics(cdf,sdf,areas,include_binary=True)
                rcdf=cdf[cdf.stim_responsive_fdr.astype(bool)].copy(); rsdf=aggregate_sessions(rcdf,mode) if len(rcdf) else pd.DataFrame(columns=sdf.columns)
                stats_resp=run_statistics(rcdf,rsdf,areas,include_binary=False) if len(rcdf) else {"continuous":{},"binary":{}}
                save_json(leaf/"statistics.json",{"all_cells":stats_all,"FDR_responsive_only":stats_resp})
                tv=pd.concat([tuning_value_statistics(cdf,mode,areas,False),tuning_value_statistics(cdf,mode,areas,True)],ignore_index=True,sort=False); tv.to_csv(leaf/"tuning_value_statistics.csv",index=False)
                cr=pd.concat([condition_statistics(qdf,areas,"condition_response",False),condition_statistics(qdf,areas,"condition_response",True)],ignore_index=True,sort=False); cr.to_csv(leaf/"condition_response_statistics.csv",index=False)
                cs=pd.concat([condition_statistics(qdf,areas,"condition_selectivity_contrast",False),condition_statistics(qdf,areas,"condition_selectivity_contrast",True)],ignore_index=True,sort=False); cs.to_csv(leaf/"condition_selectivity_statistics.csv",index=False)
                write_report(leaf/"REPORT.txt",subject,dates,mode,cell_class,depth_label,cdf,sdf,areas,stats_all,stats_resp)
                plot_responsiveness(cdf,sdf,areas,cell_class,depth_label,mode,leaf)
                make_figures(cdf,qdf,areas,cell_class,depth_label,mode,leaf,False,stats_all); make_figures(cdf,qdf,areas,cell_class,depth_label,mode,leaf,True,stats_resp); write_figure_index(leaf)
                for subset,statsout in (("all_cells",stats_all),("FDR_responsive_only",stats_resp)):
                    for metric,res in statsout.get("continuous",{}).items():
                        for _,rec in res["session_level_primary"]["pairwise_mannwhitney_holm"].items():
                            quick.append({"tuning_mode":mode,"depth_stratum":depth_label,"cell_class":cell_class,"subset":subset,"metric":metric,"area1":rec["area1"],"area2":rec["area2"],"n1_sessions":rec["n1"],"n2_sessions":rec["n2"],"U":rec["U"],"p":rec["p"],"p_holm":rec["p_holm"],"cliffs_delta":rec["cliffs_delta"]})
                print(f"  {cell_class.upper():6s}: {len(cdf)} cells, {sdf.session_key.nunique() if len(sdf) else 0} sessions -> {leaf}")
        # Explicit six-stratum A1/AAF/A2 x L2/3/L4/5 outputs for this tuning mode.
        make_area_layer_outputs(cells,areas,mode,mode_root)
    save_quickview(outroot,quick)
    print("\n"+"="*78); print("DONE"); print(f"Outputs saved under: {outroot}"); print("="*78)


# =============================================================================
# V4 FINALIZED CROSS-AREA WORKFLOW
# =============================================================================
#
# The original v3 helper functions above are retained for backwards-readable
# provenance, but the executed v4 workflow below deliberately uses only the
# targeted figure/statistics families agreed upon for the sound-tuning update.
# Broad metric grids, pooled tuning-profile figures, top-5-cell overlays, and
# legacy condition-selectivity figures are not called by v4.

V4_PRIMARY_SELECTIVITY = (
    "tuning_lifetime_sparseness",
    "tuning_gini_coefficient",
    "tuning_fano_factor",
    "tuning_fwhm",
)
V4_LIFETIME_SESSION_MEDIAN = "tuning_lifetime_sparseness_session_median_dff"
V4_LIFETIME_PRESTIM60 = "tuning_lifetime_sparseness_60s_prestim_median_dff"
V4_SENSITIVITY_METRICS = (V4_LIFETIME_SESSION_MEDIAN, V4_LIFETIME_PRESTIM60)
V4_RESPONSIVENESS = {
    "stim_responsive_fdr": "Stimulus responsive",
    "stim_excited_fdr": "Excited",
    "stim_suppressed_fdr": "Suppressed",
}
TRIAL_REDUCTION_FRACTIONS = (1.0, 0.75, 0.50, 0.25)
TRIAL_REDUCTION_MIN_TRIALS = 2


def parse_args_v4() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-area AM/frequency tuning analysis using v9 area outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("subject", help="Subject ID, e.g. imag039.")
    parser.add_argument("--dates", nargs="+", required=True,
                        help="Dates used for the prerequisite v9 area analyses.")
    parser.add_argument("--areas", nargs="+", default=list(AREAS), choices=list(AREAS),
                        help="Areas to compare. Default: A1 AAF A2.")
    parser.add_argument("--mode", choices=["both", *TUNING_MODES], default="both",
                        help="Analyze tuningFreq, tuningAM, or both (default).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print expected inputs/outputs and stop before loading tables.")
    parser.add_argument("--trial-reduction-resamples", type=int, default=500,
                        help="Monte Carlo resamples per reduced trial fraction (default 500).")
    parser.add_argument("--trial-reduction-response-permutations", type=int, default=512,
                        help="Sign-flip permutations used to re-estimate responsiveness in each reduced dataset.")
    parser.add_argument("--trial-reduction-seed", type=int, default=20260826,
                        help="Random seed for trial-reduction analysis.")
    parser.add_argument("--skip-trial-reduction", action="store_true",
                        help="Skip YELLOW trial-reduction robustness analysis.")
    return parser.parse_args()


def v4_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s.fillna(False)
    return s.astype(str).str.strip().str.lower().isin({"true", "1", "yes"})


def v4_metric_label(metric: str, mode: str) -> str:
    if metric in V4_SENSITIVITY_METRICS:
        return "Lifetime sparseness"
    return metric_label(metric, mode)


def v4_metric_reference(metric: str) -> float | None:
    if metric == "tuning_fwhm":
        return 0.0
    return None


def v4_metric_footer(metric: str, mode: str) -> str:
    if "lifetime_sparseness" in metric:
        return r"$S_{life}=[1-(\bar r^2/\overline{r^2})]/[1-1/N],\; r_i=|R_i|$"
    if metric == "tuning_gini_coefficient":
        return r"Gini coefficient of the nonnegative tuning-magnitude profile $r_i=|R_i|$"
    if metric == "tuning_fano_factor":
        return r"Fano factor $=\mathrm{Var}(r)/\mathrm{Mean}(r)$ across $r_i=|R_i|$"
    if metric == "tuning_fwhm":
        unit = "octaves (log2 frequency)" if mode == "tuningFreq" else "Hz"
        return f"FWHM of |response| around the largest peak; unbracketed widths are NaN; units={unit}"
    return ""


def v4_tuning_value_flag_columns(df: pd.DataFrame, mode: str) -> list[tuple[float, str]]:
    _, values, _ = response_columns(df, mode)
    out = []
    for value in values:
        # v9 uses the literal :g value in the CSV column name (periods are valid in pandas names).
        col = f"tuning_value_responsive_fdr_{float(value):g}_Hz"
        if col in df.columns:
            out.append((float(value), col))
    return out


def load_mode_tables_v4(subject: str, dates: list[str], areas: list[str], mode: str):
    cells, conds, provenance = load_mode_tables(subject, dates, areas, mode)
    required = {
        "trial_response_archive_path", "analysis_cell_index", "suite2p_roi_index",
        V4_LIFETIME_SESSION_MEDIAN, V4_LIFETIME_PRESTIM60,
    }
    miss = sorted(required - set(cells.columns))
    if miss:
        raise ValueError(
            "Combined AM cell table(s) are missing v9-required columns: " + ", ".join(miss) +
            "\nRun am_tuning_area_analysis_v9.py for each area first."
        )
    flags = v4_tuning_value_flag_columns(cells, mode)
    _, values, _ = response_columns(cells, mode)
    if len(flags) != len(values):
        have = {v for v, _ in flags}
        missing_values = [float(v) for v in values if float(v) not in have]
        raise ValueError(
            "v9 tuning-value-specific responsiveness columns are incomplete for values: " +
            ", ".join(f"{v:g}" for v in missing_values)
        )
    for col in list(V4_RESPONSIVENESS) + [c for _, c in flags]:
        if col in cells:
            cells[col] = v4_bool_series(cells[col])
    if "stim_responsive_fdr" in conds:
        conds["stim_responsive_fdr"] = v4_bool_series(conds["stim_responsive_fdr"])
    return cells, conds, provenance


# -----------------------------------------------------------------------------
# Session summaries and cross-area statistics
# -----------------------------------------------------------------------------

def v4_session_metric_table(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    rows = []
    if metric not in df.columns:
        return pd.DataFrame(columns=["session_key", "canonicalArea", "value", "n_cells"])
    for (sk, area), sdf in df.groupby(["session_key", "canonicalArea"], dropna=False):
        vals = finite_values(sdf[metric])
        rows.append({
            "session_key": str(sk), "canonicalArea": str(area),
            "value": float(np.mean(vals)) if len(vals) else np.nan,
            "n_cells": int(len(vals)),
        })
    return pd.DataFrame(rows)


def v4_session_percentage_table(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    rows = []
    if metric not in df.columns:
        return pd.DataFrame(columns=["session_key", "canonicalArea", "value", "n_cells"])
    for (sk, area), sdf in df.groupby(["session_key", "canonicalArea"], dropna=False):
        vals = v4_bool_series(sdf[metric]).to_numpy(dtype=float)
        rows.append({
            "session_key": str(sk), "canonicalArea": str(area),
            "value": 100.0 * float(np.mean(vals)) if len(vals) else np.nan,
            "n_cells": int(len(vals)),
        })
    return pd.DataFrame(rows)


def v4_cross_area_stat(tab: pd.DataFrame, areas: list[str]) -> dict[str, Any]:
    groups = {a: tab.loc[tab.canonicalArea == a, "value"] if len(tab) else [] for a in areas}
    summary = {}
    for area in areas:
        m, se, n = mean_sem(groups[area]); med, q1, q3, _ = median_iqr(groups[area])
        summary[area] = {"mean": m, "sem": se, "median": med, "q1": q1, "q3": q3, "n_sessions": n}
    return {
        "summary": summary,
        "omnibus": safe_kruskal(groups),
        "pairwise": pairwise_area_tests(groups, areas),
    }


def v4_pooled_stat(df: pd.DataFrame, metric: str, areas: list[str]) -> dict[str, Any]:
    groups = {a: df.loc[df.canonicalArea == a, metric] if metric in df else [] for a in areas}
    summary = {}
    for area in areas:
        m, se, n = mean_sem(groups[area]); med, q1, q3, _ = median_iqr(groups[area])
        summary[area] = {"mean": m, "sem": se, "median": med, "q1": q1, "q3": q3, "n_cells": n}
    return {"summary": summary, "omnibus": safe_kruskal(groups), "pairwise": pairwise_area_tests(groups, areas)}


def v4_apply_omnibus_family_holm(records: dict[str, Any]) -> None:
    keys = list(records)
    raw = [records[k]["session_level_primary"]["omnibus"].get("p", np.nan) for k in keys]
    adj = holm_adjust(raw)
    for key, p_adj in zip(keys, adj):
        records[key]["session_level_primary"]["omnibus"]["p_holm_family"] = p_adj


def v4_selectivity_stats(cells: pd.DataFrame, mode: str, areas: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {"all_cells": {}, "responsive_only": {}}
    for branch in ("all_cells", "responsive_only"):
        df = cells if branch == "all_cells" else cells[v4_bool_series(cells.stim_responsive_fdr)].copy()
        for metric in V4_PRIMARY_SELECTIVITY:
            rec = {
                "label": v4_metric_label(metric, mode),
                "session_level_primary": v4_cross_area_stat(v4_session_metric_table(df, metric), areas),
                "pooled_cell_exploratory": v4_pooled_stat(df, metric, areas),
            }
            out[branch][metric] = rec
        v4_apply_omnibus_family_holm(out[branch])
        out[branch]["sensitivity"] = {}
        for metric, label in [
            (V4_LIFETIME_SESSION_MEDIAN, "Lifetime sparseness — whole-session-median F0 sensitivity"),
            (V4_LIFETIME_PRESTIM60, "Lifetime sparseness — 60-s local prestimulus-median F0 sensitivity"),
        ]:
            out[branch]["sensitivity"][metric] = {
                "label": label,
                "session_level_sensitivity": v4_cross_area_stat(v4_session_metric_table(df, metric), areas),
                "pooled_cell_exploratory": v4_pooled_stat(df, metric, areas),
            }
    return out


def v4_responsiveness_stats(cells: pd.DataFrame, mode: str, areas: list[str]) -> dict[str, Any]:
    overall = {}
    for metric, label in V4_RESPONSIVENESS.items():
        overall[metric] = {
            "label": label,
            "session_level_primary": v4_cross_area_stat(v4_session_percentage_table(cells, metric), areas),
            "pooled_cell_exploratory": {
                "pairwise_fisher_holm": fisher_pairwise_binary(cells, metric, areas)
            },
        }
    v4_apply_omnibus_family_holm(overall)

    per_value = {}
    for value, flag in v4_tuning_value_flag_columns(cells, mode):
        per_value[flag] = {
            "label": f"{log2_tick_labels([value], mode)[0]} {'kHz' if mode=='tuningFreq' else 'Hz'} responsive",
            "tuning_value_Hz": float(value),
            "flag_column": flag,
            "session_level_primary": v4_cross_area_stat(v4_session_percentage_table(cells, flag), areas),
        }
    v4_apply_omnibus_family_holm(per_value)
    return {"overall": overall, "by_tuning_value": per_value}


def v4_tuning_profile_stats(cells: pd.DataFrame, mode: str, areas: list[str], responsive_only: bool) -> dict[str, Any]:
    df = cells[v4_bool_series(cells.stim_responsive_fdr)].copy() if responsive_only else cells.copy()
    cols, values, _ = response_columns(df if len(df) else cells, mode)
    out = {}
    for col, value in zip(cols, values):
        out[col] = {
            "label": f"{log2_tick_labels([value], mode)[0]} {'kHz' if mode=='tuningFreq' else 'Hz'}",
            "tuning_value_Hz": float(value),
            "session_level_primary": v4_cross_area_stat(v4_session_metric_table(df, col), areas),
        }
    v4_apply_omnibus_family_holm(out)
    return out


def v4_condition_key(value: float, intensity: float) -> str:
    return f"{float(intensity):g}dB::{float(value):g}Hz"


def v4_condition_stats(cond_df: pd.DataFrame, areas: list[str], responsive_only: bool) -> dict[str, Any]:
    df = cond_df[v4_bool_series(cond_df.stim_responsive_fdr)].copy() if responsive_only else cond_df.copy()
    if len(df) == 0:
        return {}
    sess = (
        df.groupby(["canonicalArea", "session_key", "tuning_value_Hz", "intensity_dB"], dropna=False)
        ["condition_response"].mean().reset_index()
    )
    out = {}
    for (value, intensity), sdf in sess.groupby(["tuning_value_Hz", "intensity_dB"], dropna=False):
        tab = sdf.rename(columns={"condition_response": "value"})[["session_key", "canonicalArea", "value"]]
        key = v4_condition_key(value, intensity)
        out[key] = {
            "label": f"{float(intensity):g} dB, {float(value):g} Hz",
            "tuning_value_Hz": float(value), "intensity_dB": float(intensity),
            "session_level_primary": v4_cross_area_stat(tab, areas),
        }
    v4_apply_omnibus_family_holm(out)
    return out


def build_v4_primary_stats(cells: pd.DataFrame, conds: pd.DataFrame, mode: str, areas: list[str]) -> dict[str, Any]:
    return {
        "responsiveness": v4_responsiveness_stats(cells, mode, areas),
        "selectivity": v4_selectivity_stats(cells, mode, areas),
        "tuning_profiles": {
            "all_cells": v4_tuning_profile_stats(cells, mode, areas, False),
            "responsive_only": v4_tuning_profile_stats(cells, mode, areas, True),
        },
        "intensity_profiles": {
            "all_cells": v4_condition_stats(conds, areas, False),
            "responsive_only": v4_condition_stats(conds, areas, True),
        },
    }


def aggregate_sessions_v4(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    metrics = list(V4_PRIMARY_SELECTIVITY) + list(V4_SENSITIVITY_METRICS)
    cols, _, _ = response_columns(df, mode)
    rows = []
    groups = ["subject", "date", "session", "session_key", "canonicalArea", "brainArea", "depth", "cell_class", "tuning_mode"]
    for keys, sdf in df.groupby(groups, dropna=False):
        row = dict(zip(groups, keys)); row["n_cells"] = int(len(sdf))
        for metric in metrics + cols:
            vals = finite_values(sdf[metric]) if metric in sdf else np.array([])
            row[metric] = float(np.mean(vals)) if len(vals) else np.nan
        for b in V4_RESPONSIVENESS:
            vals = v4_bool_series(sdf[b]).to_numpy(float)
            row[f"pct_{b}"] = 100.0 * float(np.mean(vals)) if len(vals) else np.nan
        for _, flag in v4_tuning_value_flag_columns(sdf, mode):
            vals = v4_bool_series(sdf[flag]).to_numpy(float)
            row[f"pct_{flag}"] = 100.0 * float(np.mean(vals)) if len(vals) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


# -----------------------------------------------------------------------------
# Plot helpers
# -----------------------------------------------------------------------------

def v4_robust_ylim(values: Iterable[Any], reference: float | None = None, pad: float = 0.14):
    vals = finite_values(values)
    if len(vals) == 0:
        return None
    if len(vals) >= 10:
        lo, hi = np.percentile(vals, [1, 99])
    else:
        lo, hi = float(np.min(vals)), float(np.max(vals))
    if reference is not None and np.isfinite(reference):
        lo, hi = min(lo, reference), max(hi, reference)
    span = float(hi - lo)
    if span <= 1e-12:
        span = max(abs(float(lo)), abs(float(hi)), 0.1)
    return float(lo - pad*span), float(hi + pad*span)


def v4_add_sig_bars(ax, pairwise: dict[str, Any], xmap: dict[str, float]) -> None:
    sig = [r for r in pairwise.values() if np.isfinite(r.get("p_holm", np.nan)) and r["p_holm"] < 0.05]
    if not sig:
        return
    y0, y1 = ax.get_ylim(); span = y1-y0
    base = y1 - 0.055*span; step = 0.065*span
    for i, rec in enumerate(sig):
        if rec["area1"] not in xmap or rec["area2"] not in xmap:
            continue
        x1, x2 = xmap[rec["area1"]], xmap[rec["area2"]]; y = base - i*step
        ax.plot([x1,x1,x2,x2], [y-.008*span,y,y,y-.008*span], color="0.2", lw=1)
        p = rec["p_holm"]
        stars = "***" if p < .001 else "**" if p < .01 else "*"
        ax.text((x1+x2)/2, y+.005*span, f"{stars} {p:.3g}", ha="center", va="bottom", fontsize=8)


def v4_cross_area_cell_metric(df: pd.DataFrame, metric: str, areas: list[str], mode: str,
                              title: str, stat_rec: dict[str, Any], output_path: Path,
                              sensitivity: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(7.6, 6.4)); rng=np.random.default_rng(20260826); display=[]
    xmap={a:i for i,a in enumerate(areas)}
    for area in areas:
        xi=xmap[area]; vals=finite_values(df.loc[df.canonicalArea==area, metric]) if metric in df else np.array([])
        if len(vals):
            ax.scatter(np.full(len(vals),xi)+rng.uniform(-.085,.085,len(vals)),vals,s=19,alpha=.22,color=AREA_COLORS[area],edgecolors="none")
            m,se,n=mean_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10,capsize=6,lw=2.3,color=AREA_COLORS[area],zorder=5); display.extend(vals.tolist())
    ref=v4_metric_reference(metric)
    if ref is not None: ax.axhline(ref,color=".45",ls="--",lw=1)
    ylim=v4_robust_ylim(display,ref)
    if ylim: ax.set_ylim(*ylim)
    pair=stat_rec.get("pairwise",{}); v4_add_sig_bars(ax,pair,xmap)
    omni=stat_rec.get("omnibus",{}); p=omni.get("p",np.nan)
    ax.set_xticks(range(len(areas)),areas); ax.set_ylabel(v4_metric_label(metric,mode)); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
    ax.set_title(title+f"\nindividual cells; exploratory Kruskal p={p:.3g}" if np.isfinite(p) else title+"\nindividual cells; exploratory")
    footer=v4_metric_footer(metric,mode)
    if sensitivity: footer += "\nSensitivity analysis; primary v9 responsiveness labels retained."
    if footer: ax.text(.5,-.16,footer,transform=ax.transAxes,ha="center",va="top",fontsize=8.5)
    fig.subplots_adjust(bottom=.23); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def v4_cross_area_session_metric(df: pd.DataFrame, metric: str, areas: list[str], mode: str,
                                 title: str, stat_rec: dict[str, Any], output_path: Path,
                                 sensitivity: bool = False) -> None:
    tab=v4_session_metric_table(df,metric); fig,ax=plt.subplots(figsize=(7.6,6.4)); display=[]; xmap={a:i for i,a in enumerate(areas)}
    for area in areas:
        xi=xmap[area]; vals=finite_values(tab.loc[tab.canonicalArea==area,"value"])
        if len(vals):
            offs=np.linspace(-.06,.06,max(len(vals),1)); ax.scatter(np.full(len(vals),xi)+offs,vals,s=28,alpha=.38,color=AREA_COLORS[area],zorder=2)
            m,se,n=mean_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=11,capsize=7,lw=2.8,color=AREA_COLORS[area],zorder=5); display.extend(vals.tolist())
            ax.annotate(f"n={n}",(xi,m),xytext=(0,10),textcoords="offset points",ha="center",fontsize=8,color=AREA_COLORS[area])
    ref=v4_metric_reference(metric)
    if ref is not None: ax.axhline(ref,color=".45",ls="--",lw=1)
    ylim=v4_robust_ylim(display,ref)
    if ylim: ax.set_ylim(*ylim)
    v4_add_sig_bars(ax,stat_rec.get("pairwise",{}),xmap)
    omni=stat_rec.get("omnibus",{}); p=omni.get("p",np.nan); ph=omni.get("p_holm_family",np.nan)
    stattext=(f"Kruskal p={p:.3g}; family Holm p={ph:.3g}" if np.isfinite(ph) else f"Kruskal p={p:.3g}" if np.isfinite(p) else "test unavailable")
    ax.set_xticks(range(len(areas)),areas); ax.set_ylabel(v4_metric_label(metric,mode)); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False)
    ax.set_title(title+"\nindividual session means + area mean ± SE\n"+stattext)
    footer=v4_metric_footer(metric,mode)
    if sensitivity: footer += "\nSensitivity analysis; excluded from primary selectivity Holm family."
    if footer: ax.text(.5,-.16,footer,transform=ax.transAxes,ha="center",va="top",fontsize=8.5)
    fig.subplots_adjust(bottom=.23); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def v4_plot_responsiveness(cells: pd.DataFrame, stats_out: dict[str, Any], areas: list[str],
                           cell_class: str, depth_label: str, mode: str, outdir: Path) -> None:
    recs=stats_out["responsiveness"]["overall"]; fig,axes=plt.subplots(1,3,figsize=(15,5.3),squeeze=False); axes=axes.ravel()
    for ax,(metric,label) in zip(axes,V4_RESPONSIVENESS.items()):
        tab=v4_session_percentage_table(cells,metric); xmap={a:i for i,a in enumerate(areas)}; display=[]
        for area in areas:
            vals=finite_values(tab.loc[tab.canonicalArea==area,"value"]); xi=xmap[area]
            if len(vals):
                offs=np.linspace(-.055,.055,max(len(vals),1)); ax.scatter(np.full(len(vals),xi)+offs,vals,s=25,alpha=.38,color=AREA_COLORS[area])
                m,se,n=mean_sem(vals); ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=9,capsize=5,lw=2.2,color=AREA_COLORS[area]); display.extend(vals.tolist())
        ax.set_ylim(0,100); v4_add_sig_bars(ax,recs[metric]["session_level_primary"].get("pairwise",{}),xmap)
        omni=recs[metric]["session_level_primary"]["omnibus"]; ax.set_xticks(range(len(areas)),areas); ax.set_ylabel("Session percentage (%)"); ax.set_title(f"{label}\nKruskal p={omni.get('p',np.nan):.3g}; family Holm p={omni.get('p_holm_family',np.nan):.3g}"); ax.grid(axis="y",alpha=.23); ax.spines[["top","right"]].set_visible(False)
    fig.suptitle(f"{cell_class.upper()} — {mode_title(mode)} — {depth_label}\nPrimary v9 responsiveness: union of tuning-value-specific FDR discoveries",fontsize=13)
    fig.tight_layout(rect=[0,0,1,.91]); fig.savefig(outdir/"responsiveness_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    # Per-tuning-value responsiveness profile.
    byv=stats_out["responsiveness"]["by_tuning_value"]
    if not byv: return
    items=sorted(byv.items(),key=lambda kv:kv[1]["tuning_value_Hz"]); values=np.asarray([r["tuning_value_Hz"] for _,r in items],float); x=xplot(values,mode)
    fig,ax=plt.subplots(figsize=(10,6.2))
    for area in areas:
        adf=cells[cells.canonicalArea==area]; rows=[]
        for sk,sdf in adf.groupby("session_key",sort=True):
            prof=np.asarray([100*float(v4_bool_series(sdf[flag]).mean()) for flag,_ in [(k,r) for k,r in items]],float)
            rows.append(prof); ax.plot(x,prof,color=AREA_COLORS[area],alpha=.17,lw=.9,marker="o",ms=2.3)
        if rows:
            M=np.vstack(rows); mean=np.nanmean(M,axis=0); n=np.sum(np.isfinite(M),axis=0); sem=np.nanstd(M,axis=0,ddof=1)/np.sqrt(n)
            ax.errorbar(x,mean,yerr=sem,fmt="o-",lw=2.8,ms=5,capsize=4,color=AREA_COLORS[area],label=area)
    ax.set_ylim(0,100); apply_log2_tuning_axis(ax,values,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Responsive cells per session (%)"); ax.grid(alpha=.22); ax.legend(frameon=False); ax.spines[["top","right"]].set_visible(False)
    ytop=98
    for xx,(flag,rec) in zip(x,items):
        s=rec["session_level_primary"]; ph=s["omnibus"].get("p_holm_family",np.nan); sig=[]
        for pr in s.get("pairwise",{}).values():
            if np.isfinite(pr.get("p_holm",np.nan)) and pr["p_holm"]<.05: sig.append(f"{pr['area1']}-{pr['area2']}:{pr['p_holm']:.2g}")
        txt=("* " if np.isfinite(ph) and ph<.05 else "")+(f"H:{ph:.2g}" if np.isfinite(ph) else "H:n/a")
        if sig: txt += "\n"+",".join(sig)
        ax.text(xx,ytop,txt,ha="center",va="top",fontsize=7)
    ax.set_title(f"{cell_class.upper()} — {mode_title(mode)} — {depth_label}\nTuning-value-specific responsiveness; H = Holm-corrected omnibus p")
    fig.tight_layout(); fig.savefig(outdir/"responsiveness_by_tuning_value_SESSION_PROFILE.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def v4_annotate_profile_stats(ax, values: np.ndarray, stats_by_col: dict[str,Any], cols: list[str], mode: str) -> None:
    y0,y1=ax.get_ylim(); span=y1-y0
    for xx,col in zip(xplot(values,mode),cols):
        rec=stats_by_col.get(col,{}).get("session_level_primary",{}); ph=rec.get("omnibus",{}).get("p_holm_family",np.nan); sig=[]
        for pr in rec.get("pairwise",{}).values():
            if np.isfinite(pr.get("p_holm",np.nan)) and pr["p_holm"]<.05: sig.append(f"{pr['area1']}-{pr['area2']}:{pr['p_holm']:.2g}")
        txt=("* " if np.isfinite(ph) and ph<.05 else "")+(f"H:{ph:.2g}" if np.isfinite(ph) else "H:n/a")
        if sig: txt += "\n"+",".join(sig)
        ax.text(xx,y1-.025*span,txt,ha="center",va="top",fontsize=7)


def v4_plot_tuning_profile(cells: pd.DataFrame, stats_out: dict[str,Any], areas: list[str], cell_class: str,
                           depth_label: str, mode: str, outdir: Path, responsive_only: bool) -> None:
    branch="responsive_only" if responsive_only else "all_cells"; suffix="FDR_responsive_only" if responsive_only else "all_cells"
    df=cells[v4_bool_series(cells.stim_responsive_fdr)].copy() if responsive_only else cells.copy(); cols,values,_=response_columns(df if len(df) else cells,mode)
    if not cols or len(df)==0: return
    x=xplot(values,mode); fig,ax=plt.subplots(figsize=(10.4,6.3)); display=[]
    for area in areas:
        rows=[]
        for _,sdf in df[df.canonicalArea==area].groupby("session_key",sort=True):
            prof=np.asarray([float(np.nanmean(pd.to_numeric(sdf[c],errors="coerce"))) for c in cols],float); rows.append(prof); ax.plot(x,prof,color=AREA_COLORS[area],alpha=.17,lw=.9,marker="o",ms=2.3); display.extend(finite_values(prof).tolist())
        if rows:
            M=np.vstack(rows); mean=np.nanmean(M,axis=0); n=np.sum(np.isfinite(M),axis=0); sem=np.nanstd(M,axis=0,ddof=1)/np.sqrt(n)
            ax.errorbar(x,mean,yerr=sem,fmt="o-",lw=2.8,ms=5,capsize=4,color=AREA_COLORS[area],label=f"{area} ({len(rows)} sessions)"); display.extend(finite_values(np.r_[mean-sem,mean+sem]).tolist())
    ax.axhline(0,color=".4",ls="--",lw=1); ylim=v4_robust_ylim(display,0.0)
    if ylim: ax.set_ylim(*ylim)
    apply_log2_tuning_axis(ax,values,mode); v4_annotate_profile_stats(ax,values,stats_out["tuning_profiles"][branch],cols,mode)
    ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Session mean response (dF/F)"); ax.grid(axis="y",alpha=.22); ax.legend(frameon=False); ax.spines[["top","right"]].set_visible(False)
    ax.set_title(f"{cell_class.upper()} across A1 / AAF / A2 — {depth_label}\n{mode_title(mode)} — {suffix.replace('_',' ')}; session means + area mean ± SE\nH = Holm-corrected tuning-value omnibus p")
    fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_POINTS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def v4_plot_preferred_distribution(cells: pd.DataFrame, areas: list[str], cell_class: str, depth_label: str,
                                   mode: str, outdir: Path, responsive_only: bool) -> None:
    suffix="FDR_responsive_only" if responsive_only else "all_cells"; df=cells[v4_bool_series(cells.stim_responsive_fdr)].copy() if responsive_only else cells.copy()
    vals=np.sort(pd.to_numeric(df.preferred_tuning_value_Hz,errors="coerce").dropna().unique())
    if len(vals)==0: return
    x=xplot(vals,mode); fig,ax=plt.subplots(figsize=(9.4,5.5))
    for area in areas:
        pref=pd.to_numeric(df.loc[df.canonicalArea==area,"preferred_tuning_value_Hz"],errors="coerce").to_numpy(float); total=np.sum(np.isfinite(pref)); pct=np.asarray([100*np.sum(np.isclose(pref,v))/total if total else np.nan for v in vals])
        ax.plot(x,pct,marker="o",lw=2.2,color=AREA_COLORS[area],label=f"{area} (n={total})")
    apply_log2_tuning_axis(ax,vals,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Cells preferring value (%)"); ax.set_ylim(bottom=0); ax.grid(axis="y",alpha=.22); ax.legend(frameon=False); ax.spines[["top","right"]].set_visible(False)
    ax.set_title(f"{cell_class.upper()} preferred tuning across areas — {depth_label}\n{mode_title(mode)} — {suffix.replace('_',' ')} — descriptive")
    fig.tight_layout(); fig.savefig(outdir/f"preferred_tuning_distribution_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def v4_plot_raster(cells: pd.DataFrame, areas: list[str], cell_class: str, depth_label: str, mode: str,
                   outdir: Path, responsive_only: bool, sort_metric: str, stem: str) -> None:
    suffix="FDR_responsive_only" if responsive_only else "all_cells"; df=cells[v4_bool_series(cells.stim_responsive_fdr)].copy() if responsive_only else cells.copy(); cols,values,labels=response_columns(df if len(df) else cells,mode)
    if len(cols)<2 or len(df)==0: return
    edges=log2_bin_edges(values,mode); fig,axes=plt.subplots(len(areas),1,figsize=(10,3.6*len(areas)),squeeze=False); im=None
    for ax,area in zip(axes.ravel(),areas):
        adf=df[df.canonicalArea==area].copy()
        if len(adf)==0: ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center"); ax.axis("off"); continue
        mat=adf[cols].apply(pd.to_numeric,errors="coerce").to_numpy(float); denom=np.nanmax(np.abs(mat),axis=1); good=np.isfinite(denom)&(denom>0); mat=mat[good]; adf=adf.iloc[np.flatnonzero(good)].copy()
        if len(mat)==0: continue
        norm=mat/denom[good,None]; rank=pd.to_numeric(adf[sort_metric],errors="coerce").to_numpy(float)
        order=np.argsort(np.nan_to_num(rank,nan=-np.inf))[::-1] if sort_metric=="tuning_lifetime_sparseness" else np.argsort(np.nan_to_num(rank,nan=np.inf))
        if edges is not None:
            yedges=np.arange(len(norm)+1,dtype=float); im=ax.pcolormesh(edges,yedges,norm[order],cmap="coolwarm",vmin=-1,vmax=1,shading="flat"); ax.set_ylim(len(norm),0); apply_log2_tuning_axis(ax,values,mode)
        else:
            im=ax.imshow(norm[order],aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm"); ax.set_xticks(range(len(labels)),labels,rotation=30,ha="right")
        ax.set_ylabel(f"{area} cells"); ax.set_xlabel(mode_axis_label(mode)); ax.set_title(f"{area}: n={len(order)}")
    sort_text="descending lifetime sparseness" if sort_metric=="tuning_lifetime_sparseness" else "preferred tuning value"
    fig.suptitle(f"{cell_class.upper()} — {depth_label} — {mode_title(mode)} — {suffix.replace('_',' ')}\nnormalized tuning rasters sorted by {sort_text}",y=.995)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Response / max |response| per cell",shrink=.75)
    fig.subplots_adjust(left=.09,right=.88,bottom=.10,top=.91,hspace=.48); fig.savefig(outdir/f"{stem}_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def v4_plot_selectivity(cells: pd.DataFrame, stats_out: dict[str,Any], areas: list[str], cell_class: str,
                        depth_label: str, mode: str, outdir: Path) -> None:
    for branch in ("all_cells","responsive_only"):
        responsive=(branch=="responsive_only"); suffix="FDR_responsive_only" if responsive else "all_cells"; df=cells[v4_bool_series(cells.stim_responsive_fdr)].copy() if responsive else cells.copy()
        for metric in V4_PRIMARY_SELECTIVITY:
            rec=stats_out["selectivity"][branch][metric]; stem=metric.replace("tuning_","")
            title=f"{cell_class.upper()} — {depth_label} — {mode_title(mode)}\n{v4_metric_label(metric,mode)} — {suffix.replace('_',' ')}"
            v4_cross_area_cell_metric(df,metric,areas,mode,title,rec["pooled_cell_exploratory"],outdir/f"{stem}_across_areas_{suffix}_CELL_POINTS.png")
            v4_cross_area_session_metric(df,metric,areas,mode,title,rec["session_level_primary"],outdir/f"{stem}_across_areas_{suffix}_SESSION_POINTS.png")
        for metric,tag in [(V4_LIFETIME_SESSION_MEDIAN,"session_median_dff"),(V4_LIFETIME_PRESTIM60,"60s_prestim_median_dff")]:
            rec=stats_out["selectivity"][branch]["sensitivity"][metric]; title=f"{cell_class.upper()} — {depth_label} — {mode_title(mode)}\n{rec['label']} — {suffix.replace('_',' ')}"
            v4_cross_area_cell_metric(df,metric,areas,mode,title,rec["pooled_cell_exploratory"],outdir/f"lifetime_sparseness_{tag}_across_areas_{suffix}_CELL_POINTS.png",True)
            v4_cross_area_session_metric(df,metric,areas,mode,title,rec["session_level_sensitivity"],outdir/f"lifetime_sparseness_{tag}_across_areas_{suffix}_SESSION_POINTS.png",True)
        v4_plot_raster(cells,areas,cell_class,depth_label,mode,outdir,responsive,"preferred_tuning_value_Hz","selectivity_rasters_PREFERRED_VALUE")
        v4_plot_raster(cells,areas,cell_class,depth_label,mode,outdir,responsive,"tuning_lifetime_sparseness","selectivity_rasters_LIFETIME_SPARSENESS")


def v4_plot_intensity_profiles(conds: pd.DataFrame, stats_out: dict[str,Any], areas: list[str], cell_class: str,
                               depth_label: str, mode: str, outdir: Path, responsive_only: bool) -> None:
    branch="responsive_only" if responsive_only else "all_cells"; suffix="FDR_responsive_only" if responsive_only else "all_cells"; df=conds[v4_bool_series(conds.stim_responsive_fdr)].copy() if responsive_only else conds.copy()
    if len(df)==0: return
    values=np.sort(pd.to_numeric(df.tuning_value_Hz,errors="coerce").dropna().unique()); intens=np.sort(pd.to_numeric(df.intensity_dB,errors="coerce").dropna().unique())
    if len(values)==0 or len(intens)==0:return
    grouped=df.groupby(["canonicalArea","session_key","tuning_value_Hz","intensity_dB"],dropna=False)["condition_response"].mean().reset_index(); x=xplot(values,mode); ncols=min(3,len(intens)); nrows=math.ceil(len(intens)/ncols); fig,axes=plt.subplots(nrows,ncols,figsize=(5.4*ncols,4.9*nrows),squeeze=False); axes=axes.ravel(); all_display=[]
    fam=stats_out["intensity_profiles"][branch]
    for ax,intensity in zip(axes,intens):
        for area in areas:
            rows=[]; adf=grouped[(grouped.canonicalArea==area)&np.isclose(grouped.intensity_dB,intensity)]
            for _,sdf in adf.groupby("session_key",sort=True):
                prof=np.asarray([float(sdf[np.isclose(sdf.tuning_value_Hz,v)].iloc[0].condition_response) if len(sdf[np.isclose(sdf.tuning_value_Hz,v)]) else np.nan for v in values]); rows.append(prof); ax.plot(x,prof,color=AREA_COLORS[area],alpha=.17,lw=.9,marker="o",ms=2.1); all_display.extend(finite_values(prof).tolist())
            if rows:
                M=np.vstack(rows); mean=np.nanmean(M,axis=0); n=np.sum(np.isfinite(M),axis=0); sem=np.nanstd(M,axis=0,ddof=1)/np.sqrt(n); ax.errorbar(x,mean,yerr=sem,fmt="o-",ms=4.5,lw=2.5,capsize=3,color=AREA_COLORS[area],label=area); all_display.extend(finite_values(np.r_[mean-sem,mean+sem]).tolist())
        ax.axhline(0,color=".45",ls="--",lw=1); apply_log2_tuning_axis(ax,values,mode); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Condition response (dF/F)"); ax.grid(axis="y",alpha=.22); ax.spines[["top","right"]].set_visible(False)
        # condition-wise corrected statistics at this intensity
        y0,y1=ax.get_ylim(); span=y1-y0
        for xx,v in zip(x,values):
            rec=fam.get(v4_condition_key(v,intensity),{}).get("session_level_primary",{}); ph=rec.get("omnibus",{}).get("p_holm_family",np.nan); sig=[]
            for pr in rec.get("pairwise",{}).values():
                if np.isfinite(pr.get("p_holm",np.nan)) and pr["p_holm"]<.05: sig.append(f"{pr['area1']}-{pr['area2']}:{pr['p_holm']:.2g}")
            txt=("* " if np.isfinite(ph) and ph<.05 else "")+(f"H:{ph:.2g}" if np.isfinite(ph) else "H:n/a")
            if sig: txt += "\n"+",".join(sig)
            ax.text(xx,y1-.025*span,txt,ha="center",va="top",fontsize=6.8)
        ax.set_title(f"{intensity:g} dB")
    ylim=v4_robust_ylim(all_display,0.0)
    if ylim:
        for ax in axes[:len(intens)]: ax.set_ylim(*ylim)
    for ax in axes[len(intens):]: ax.axis("off")
    handles,labs=axes[0].get_legend_handles_labels(); fig.legend(handles,labs,frameon=False,loc="upper right")
    fig.suptitle(f"{cell_class.upper()} across areas — {depth_label}\n{mode_title(mode)} intensity-resolved responses — {suffix.replace('_',' ')}\nsession means + area mean ± SE; H = Holm-corrected condition omnibus p",fontsize=13)
    fig.tight_layout(rect=[0,0,.97,.94]); fig.savefig(outdir/f"intensity_condition_response_profile_{suffix}_SESSION_PROFILE.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


# -----------------------------------------------------------------------------
# Targeted area x layer branch: L2/3 versus L4/5 within each area
# -----------------------------------------------------------------------------

def v4_layer_pair_stats(df: pd.DataFrame, metric: str, areas: list[str], session_level: bool) -> dict[str,Any]:
    d=add_layer_columns(df); recs=[]; ps=[]
    for area in areas:
        adf=d[d.canonicalArea==area]
        vals={}
        for lk in ("L23","L45"):
            sub=adf[adf.layer_key==lk]
            vals[lk]=v4_session_metric_table(sub,metric)["value"] if session_level else sub[metric]
        r=safe_mannwhitney(vals["L23"],vals["L45"]); r["area"]=area; recs.append(r); ps.append(r["p"])
    adj=holm_adjust(ps)
    return {r["area"]:{**r,"p_holm_across_areas":p} for r,p in zip(recs,adj)}


def v4_plot_area_layer_metric(df: pd.DataFrame, metric: str, areas: list[str], mode: str, title: str,
                              output_path: Path, session_level: bool, sensitivity: bool=False) -> dict[str,Any]:
    d=add_layer_columns(df); d=d[d.layer_key.notna()].copy(); recs=v4_layer_pair_stats(d,metric,areas,session_level); fig,ax=plt.subplots(figsize=(10.5,6.4)); xt=[]; labels=[]; display=[]; xpos={}; x=0.0; rng=np.random.default_rng(811)
    for area in areas:
        xpos[area]={}
        for lk,ll in (("L23","L2/3"),("L45","L4/5")):
            sub=d[(d.canonicalArea==area)&(d.layer_key==lk)]; vals=finite_values(v4_session_metric_table(sub,metric)["value"] if session_level else sub[metric]); xpos[area][lk]=x
            if len(vals):
                offs=np.linspace(-.055,.055,max(len(vals),1)) if session_level else rng.uniform(-.075,.075,len(vals)); ax.scatter(np.full(len(vals),x)+offs,vals,s=28 if session_level else 18,alpha=.38 if session_level else .22,color=AREA_COLORS[area]); m,se,n=mean_sem(vals); ax.errorbar(x,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=10 if session_level else 8,capsize=6,lw=2.2,color=AREA_COLORS[area]); display.extend(vals.tolist())
            xt.append(x); labels.append(f"{area}\n{ll}"); x+=1
        x+=.6
    ref=v4_metric_reference(metric)
    if ref is not None: ax.axhline(ref,color=".45",ls="--",lw=1)
    ylim=v4_robust_ylim(display,ref)
    if ylim: ax.set_ylim(*ylim)
    y0,y1=ax.get_ylim(); span=y1-y0
    for i,area in enumerate(areas):
        ph=recs[area].get("p_holm_across_areas",np.nan)
        if np.isfinite(ph) and ph<.05:
            x1,x2=xpos[area]["L23"],xpos[area]["L45"]; y=y1-(.055+i*.055)*span; ax.plot([x1,x1,x2,x2],[y-.008*span,y,y,y-.008*span],color=".2",lw=1); ax.text((x1+x2)/2,y+.005*span,f"Holm p={ph:.3g}",ha="center",fontsize=8)
    ax.set_xticks(xt,labels); ax.set_ylabel(v4_metric_label(metric,mode)); ax.grid(axis="y",alpha=.2); ax.spines[["top","right"]].set_visible(False); ax.set_title(title+"\nL2/3 vs L4/5 within each area; Holm across A1/AAF/A2 layer tests")
    footer=v4_metric_footer(metric,mode)+("\nSensitivity analysis." if sensitivity else "")
    if footer: ax.text(.5,-.17,footer,transform=ax.transAxes,ha="center",va="top",fontsize=8.5)
    fig.subplots_adjust(bottom=.24); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig); return recs


def make_area_layer_outputs_v4(all_cells: pd.DataFrame, areas: list[str], mode: str, mode_root: Path) -> None:
    root=mode_root/"area_by_layer"; root.mkdir(parents=True,exist_ok=True)
    layered=add_layer_columns(all_cells); layered=layered[layered.layer_key.notna()].copy(); layered.to_csv(root/"all_area_layer_cells.csv",index=False)
    for cell_class in CELL_CLASSES:
        class_cells=layered[layered.cell_class==cell_class].copy(); out=root/cell_class; out.mkdir(parents=True,exist_ok=True); stats_save={}
        for responsive in (False,True):
            branch="responsive_only" if responsive else "all_cells"; suffix="FDR_responsive_only" if responsive else "all_cells"; df=class_cells[v4_bool_series(class_cells.stim_responsive_fdr)].copy() if responsive else class_cells.copy(); stats_save[branch]={}
            for metric in V4_PRIMARY_SELECTIVITY:
                title=f"{cell_class.upper()} — {mode_title(mode)} — {v4_metric_label(metric,mode)} — {suffix.replace('_',' ')}"
                stats_save[branch][metric]={
                    "cell_exploratory":v4_plot_area_layer_metric(df,metric,areas,mode,title,out/f"area_layer_{metric}_{suffix}_CELL_POINTS.png",False),
                    "session_primary":v4_plot_area_layer_metric(df,metric,areas,mode,title,out/f"area_layer_{metric}_{suffix}_SESSION_POINTS.png",True),
                }
            stats_save[branch]["sensitivity"]={}
            for metric,tag in [(V4_LIFETIME_SESSION_MEDIAN,"session_median_dff"),(V4_LIFETIME_PRESTIM60,"60s_prestim_median_dff")]:
                title=f"{cell_class.upper()} — {mode_title(mode)} — lifetime sparseness {tag} — {suffix.replace('_',' ')}"
                stats_save[branch]["sensitivity"][metric]=v4_plot_area_layer_metric(df,metric,areas,mode,title,out/f"area_layer_lifetime_sparseness_{tag}_{suffix}_SESSION_POINTS.png",True,True)
        save_json(out/"area_layer_statistics.json",stats_save); write_figure_index(out)


# -----------------------------------------------------------------------------
# V9 trial archives and reduced-trial recomputation
# -----------------------------------------------------------------------------

def v4_bh_fdr(p_values: np.ndarray) -> np.ndarray:
    p=np.asarray(p_values,float); q=np.full(p.shape,np.nan); idx=np.flatnonzero(np.isfinite(p))
    if len(idx)==0:return q
    vals=p[idx]; order=np.argsort(vals); ranked=vals[order]; m=len(ranked); adj=ranked*m/np.arange(1,m+1); adj=np.minimum.accumulate(adj[::-1])[::-1]; adj=np.clip(adj,0,1); restored=np.empty(m); restored[order]=adj; q[idx]=restored; return q


def v4_lifetime(curve: np.ndarray) -> float:
    x=np.abs(np.asarray(curve,float)); x=x[np.isfinite(x)]
    if len(x)<2:return np.nan
    ms=float(np.mean(x*x))
    if ms<=1e-15:return np.nan
    return float((1-(float(np.mean(x))**2)/ms)/(1-1/len(x)))


def v4_gini(curve: np.ndarray) -> float:
    x=np.abs(np.asarray(curve,float)); x=x[np.isfinite(x)]
    if len(x)<2:return np.nan
    total=float(np.sum(x))
    if total<=1e-15:return np.nan
    x=np.sort(x); n=len(x); r=np.arange(1,n+1,dtype=float)
    return float(2*np.sum(r*x)/(n*total)-(n+1)/n)


def v4_fano(curve: np.ndarray) -> float:
    x=np.abs(np.asarray(curve,float)); x=x[np.isfinite(x)]
    if len(x)<2:return np.nan
    m=float(np.mean(x))
    return float(np.var(x,ddof=1)/m) if m>1e-15 else np.nan


def v4_fwhm(curve: np.ndarray, values_hz: np.ndarray, mode: str) -> float:
    y=np.asarray(curve,float); xh=np.asarray(values_hz,float); valid=np.isfinite(y)&np.isfinite(xh)&(xh>0)
    if np.sum(valid)<3:return np.nan
    y=np.abs(y[valid]); xh=xh[valid]; order=np.argsort(xh); y=y[order]; xh=xh[order]; peak_i=int(np.nanargmax(y)); peak=float(y[peak_i])
    if peak<=1e-15 or peak_i==0 or peak_i==len(y)-1:return np.nan
    half=.5*peak; x=np.log2(xh) if mode=="tuningFreq" else xh.astype(float); left=right=np.nan
    for i in range(peak_i-1,-1,-1):
        if (y[i]-half)*(y[i+1]-half)<=0:
            y0,y1=float(y[i]),float(y[i+1]); left=float(x[i] if y1==y0 else x[i]+(half-y0)*(x[i+1]-x[i])/(y1-y0)); break
    for i in range(peak_i,len(y)-1):
        if (y[i]-half)*(y[i+1]-half)<=0:
            y0,y1=float(y[i]),float(y[i+1]); right=float(x[i+1] if y1==y0 else x[i]+(half-y0)*(x[i+1]-x[i])/(y1-y0)); break
    return float(right-left) if np.isfinite(left) and np.isfinite(right) and right>=left else np.nan


class V4SignCache:
    def __init__(self,n_perm:int,seed:int): self.n_perm=int(n_perm); self.rng=np.random.default_rng(seed); self.cache={}
    def get(self,n:int):
        n=int(n)
        if n not in self.cache:self.cache[n]=self.rng.choice(np.array([-1.,1.],np.float32),size=(self.n_perm,n),replace=True)
        return self.cache[n]


def v4_signflip_pvalues(R: np.ndarray, cache: V4SignCache) -> np.ndarray:
    R=np.asarray(R,float); out=np.full(R.shape[0],np.nan); groups={}; masks={}
    for i in range(R.shape[0]):
        finite=np.isfinite(R[i]); key=np.packbits(finite).tobytes(); groups.setdefault(key,[]).append(i); masks[key]=finite
    for key,inds in groups.items():
        finite=masks[key]; n=int(np.sum(finite))
        if n<TRIAL_REDUCTION_MIN_TRIALS:continue
        idx=np.asarray(inds,int); vals=R[idx][:,finite]; obs=np.mean(vals,axis=1); signs=cache.get(n); null=(signs@vals.T)/float(n); ext=np.sum(np.abs(null)>=np.abs(obs)[None,:],axis=0); out[idx]=(1+ext)/(cache.n_perm+1)
    return out


def v4_load_archive(path: str|Path, cache: dict[str,dict[str,np.ndarray]]) -> dict[str,np.ndarray]:
    key=str(path)
    if key in cache:return cache[key]
    p=Path(key)
    if not p.exists():raise FileNotFoundError(f"Missing v9 trial-response archive: {p}")
    with np.load(p,allow_pickle=False) as z:d={k:z[k].copy() for k in z.files}
    need={"trial_response_primary","trial_condition_index","valid_trial_mask","analysis_trial_mask","condition_names","condition_tuning_value_hz","condition_intensity_db","possible_tuning_values_hz","cell_class","analysis_cell_index","suite2p_roi_index","canonical_area","session_key","tuning_mode"}
    miss=need-set(d)
    if miss:raise ValueError(f"{p} missing v9 archive fields: {sorted(miss)}")
    cache[key]=d; return d


def v4_sample_conditions(arc: dict[str,np.ndarray],fraction:float,rng:np.random.Generator):
    ci=np.asarray(arc["trial_condition_index"],int); valid=np.asarray(arc["valid_trial_mask"],bool)&np.asarray(arc["analysis_trial_mask"],bool); ncond=len(np.asarray(arc["condition_names"])); chosen=[]; counts=[]
    for k in range(ncond):
        avail=np.flatnonzero(valid&(ci==k)); n=len(avail)
        if fraction>=.999999:take=avail
        else:
            kk=min(n,max(1,int(np.floor(fraction*n+.5)))) if n else 0; take=np.sort(rng.choice(avail,size=kk,replace=False)) if kk else np.array([],int)
        chosen.append(take); counts.append(len(take))
    return chosen,counts


def v4_reduced_yellow_data(full_yellow: pd.DataFrame,fraction:float,rng:np.random.Generator,cache:dict[str,dict[str,np.ndarray]],signcache:V4SignCache):
    cell_rows=[]; cond_rows=[]; counts_all=[]; sessions=full_yellow[["session_key","canonicalArea","depth","trial_response_archive_path"]].drop_duplicates("session_key")
    for _,srow in sessions.iterrows():
        arc=v4_load_archive(srow.trial_response_archive_path,cache); chosen,counts=v4_sample_conditions(arc,fraction,rng); counts_all.extend(counts); R=np.asarray(arc["trial_response_primary"],float); n_cells=R.shape[0]; values=np.asarray(arc["possible_tuning_values_hz"],float); cond_values=np.asarray(arc["condition_tuning_value_hz"],float); cond_intens=np.asarray(arc["condition_intensity_db"],float); nval=len(values); ncond=len(chosen)
        condmat=np.full((n_cells,ncond),np.nan)
        for k,take in enumerate(chosen):
            if len(take):condmat[:,k]=np.nanmean(R[:,take],axis=1)
        curves=np.full((n_cells,nval),np.nan); resp=np.zeros((n_cells,nval),bool)
        for vi,v in enumerate(values):
            parts=[chosen[k] for k in range(ncond) if np.isclose(cond_values[k],v) and len(chosen[k])]
            take=np.sort(np.concatenate(parts)) if parts else np.array([],int)
            if len(take):curves[:,vi]=np.nanmean(R[:,take],axis=1)
            if len(take)>=TRIAL_REDUCTION_MIN_TRIALS:
                p=v4_signflip_pvalues(R[:,take],signcache); q=v4_bh_fdr(p); resp[:,vi]=np.isfinite(q)&(q<FDR_ALPHA)
        anyresp=np.any(resp,axis=1); excited=np.zeros(n_cells,bool); suppressed=np.zeros(n_cells,bool)
        for i in np.flatnonzero(anyresp):
            cand=np.flatnonzero(resp[i]&np.isfinite(curves[i]))
            if len(cand):
                b=cand[int(np.argmax(np.abs(curves[i,cand])))]; excited[i]=curves[i,b]>0; suppressed[i]=curves[i,b]<0
        classes=np.asarray(arc["cell_class"]).astype(str); yellow=(classes=="yellow"); mode=str(np.asarray(arc["tuning_mode"]).item()); prefix="response_freq" if mode=="tuningFreq" else "response_AM"
        for i in np.flatnonzero(yellow):
            curve=curves[i]; finite=np.isfinite(curve); pref=np.nan
            if np.any(finite):
                inds=np.flatnonzero(finite); bestidx=int(inds[int(np.nanargmax(curve[finite]))]); pref=float(values[bestidx])
            row={"subject":str(full_yellow.subject.iloc[0]),"date":"","session":"","session_key":str(np.asarray(arc["session_key"]).item()),"canonicalArea":str(np.asarray(arc["canonical_area"]).item()),"brainArea":"","depth":float(srow.depth),"cell_class":"yellow","tuning_mode":mode,"analysis_cell_index":int(np.asarray(arc["analysis_cell_index"])[i]),"suite2p_roi_index":int(np.asarray(arc["suite2p_roi_index"])[i]),"trial_response_archive_path":str(srow.trial_response_archive_path),"stim_responsive_fdr":bool(anyresp[i]),"stim_excited_fdr":bool(excited[i]),"stim_suppressed_fdr":bool(suppressed[i]),"tuning_lifetime_sparseness":v4_lifetime(curve),"tuning_gini_coefficient":v4_gini(curve),"tuning_fano_factor":v4_fano(curve),"tuning_fwhm":v4_fwhm(curve,values,mode),"preferred_tuning_value_Hz":pref}
            for vi,v in enumerate(values):
                row[f"{prefix}_{v:g}_Hz"]=float(curve[vi]); row[f"tuning_value_responsive_fdr_{v:g}_Hz"]=bool(resp[i,vi])
            cell_rows.append(row)
            for k in range(ncond):
                cond_rows.append({"subject":row["subject"],"date":"","session":"","session_key":row["session_key"],"canonicalArea":row["canonicalArea"],"brainArea":"","depth":row["depth"],"cell_class":"yellow","tuning_mode":mode,"stim_responsive_fdr":bool(anyresp[i]),"tuning_value_Hz":float(cond_values[k]),"intensity_dB":float(cond_intens[k]),"condition_response":float(condmat[i,k])})
    return pd.DataFrame(cell_rows),pd.DataFrame(cond_rows),counts_all


# -----------------------------------------------------------------------------
# Significant-YELLOW trial reduction targets
# -----------------------------------------------------------------------------

def v4_add_target(groups:dict[str,list],group:str,label:str,family:str,branch:str,key:str,test:str,p:float,meta:dict|None=None):
    if np.isfinite(p) and p<.05:
        rec={"id":f"{group}::{label}","label":label,"family":family,"branch":branch,"key":key,"test":test,"original_p":float(p)}
        if meta:rec.update(meta)
        groups.setdefault(group,[]).append(rec)


def significant_trial_reduction_targets_v4(stats_out:dict[str,Any],mode:str):
    groups={}
    for metric,rec in stats_out["responsiveness"]["overall"].items():
        s=rec["session_level_primary"]; v4_add_target(groups,"responsiveness",f"{rec['label']} omnibus","responsiveness","overall",metric,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
        for pk,pr in s["pairwise"].items():v4_add_target(groups,"responsiveness",f"{rec['label']}: {pr['area1']} vs {pr['area2']}","responsiveness","overall",metric,f"pair:{pk}",pr.get("p_holm",np.nan))
    for flag,rec in stats_out["responsiveness"]["by_tuning_value"].items():
        s=rec["session_level_primary"]; label=rec["label"]; v4_add_target(groups,"responsiveness_by_tuning_value",f"{label} omnibus","responsiveness","by_tuning_value",flag,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
        for pk,pr in s["pairwise"].items():v4_add_target(groups,"responsiveness_by_tuning_value",f"{label}: {pr['area1']} vs {pr['area2']}","responsiveness","by_tuning_value",flag,f"pair:{pk}",pr.get("p_holm",np.nan))
    for branch in ("all_cells","responsive_only"):
        for metric in V4_PRIMARY_SELECTIVITY:
            rec=stats_out["selectivity"][branch][metric]; s=rec["session_level_primary"]; grp=f"selectivity_{branch}"; v4_add_target(groups,grp,f"{rec['label']} omnibus","selectivity",branch,metric,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
            for pk,pr in s["pairwise"].items():v4_add_target(groups,grp,f"{rec['label']}: {pr['area1']} vs {pr['area2']}","selectivity",branch,metric,f"pair:{pk}",pr.get("p_holm",np.nan))
        for col,rec in stats_out["tuning_profiles"][branch].items():
            s=rec["session_level_primary"]; grp=f"tuning_profile_{branch}"; v4_add_target(groups,grp,f"{rec['label']} response omnibus","tuning_profiles",branch,col,"omnibus",s["omnibus"].get("p_holm_family",np.nan))
            for pk,pr in s["pairwise"].items():v4_add_target(groups,grp,f"{rec['label']} response: {pr['area1']} vs {pr['area2']}","tuning_profiles",branch,col,f"pair:{pk}",pr.get("p_holm",np.nan))
        for key,rec in stats_out["intensity_profiles"][branch].items():
            s=rec["session_level_primary"]; intensity=rec["intensity_dB"]; grp=f"intensity_profile_{branch}_{intensity:g}dB"; label=f"{intensity:g} dB, {log2_tick_labels([rec['tuning_value_Hz']],mode)[0]} {'kHz' if mode=='tuningFreq' else 'Hz'}"
            v4_add_target(groups,grp,f"{label} omnibus","intensity_profiles",branch,key,"omnibus",s["omnibus"].get("p_holm_family",np.nan),{"intensity_dB":intensity})
            for pk,pr in s["pairwise"].items():v4_add_target(groups,grp,f"{label}: {pr['area1']} vs {pr['area2']}","intensity_profiles",branch,key,f"pair:{pk}",pr.get("p_holm",np.nan),{"intensity_dB":intensity})
    return {k:v for k,v in groups.items() if v}


def v4_extract_target_p(stats_out:dict[str,Any],target:dict[str,Any]):
    fam,branch,key,test=target["family"],target["branch"],target["key"],target["test"]
    if fam=="responsiveness":rec=stats_out["responsiveness"][branch][key]["session_level_primary"]
    elif fam=="selectivity":rec=stats_out["selectivity"][branch][key]["session_level_primary"]
    elif fam=="tuning_profiles":rec=stats_out["tuning_profiles"][branch][key]["session_level_primary"]
    elif fam=="intensity_profiles":
        branch_dict=stats_out.get("intensity_profiles",{}).get(branch,{})
        if key not in branch_dict:
            return np.nan
        rec=branch_dict[key]["session_level_primary"]
    else:return np.nan
    if test=="omnibus":return float(rec["omnibus"].get("p_holm_family",np.nan))
    return float(rec["pairwise"].get(test.split(":",1)[1],{}).get("p_holm",np.nan))


def v4_plot_trial_reduction(group:str,targets:list[dict],raw:pd.DataFrame,count_summary:dict[float,tuple],mode:str,depth_label:str,outdir:Path):
    fractions=np.asarray(TRIAL_REDUCTION_FRACTIONS,float); x=100*fractions; fig,(ax1,ax2)=plt.subplots(2,1,figsize=(10.8,8.3),sharex=True,gridspec_kw={"height_ratios":[1.05,1]})
    for t in targets:
        med=[];lo=[];hi=[];retain=[]
        for f in fractions:
            vals=finite_values(raw.loc[(raw.fraction==f)&(raw.target_id==t["id"]),"p_adjusted"])
            if len(vals):med.append(np.median(vals));lo.append(np.percentile(vals,10));hi.append(np.percentile(vals,90));retain.append(np.mean(vals<.05))
            else:med.append(np.nan);lo.append(np.nan);hi.append(np.nan);retain.append(np.nan)
        line=ax1.plot(x,np.clip(med,1e-6,1),marker="o",label=t["label"])[0]; ax1.fill_between(x,np.clip(lo,1e-6,1),np.clip(hi,1e-6,1),alpha=.12,color=line.get_color()); ax2.plot(x,retain,marker="o",color=line.get_color())
    ax1.axhline(.05,color=".35",ls="--",lw=1); ax1.set_yscale("log"); ax1.set_ylabel("Adjusted p\nmedian (10th-90th pct)"); ax1.grid(alpha=.2); ax1.spines[["top","right"]].set_visible(False); ax1.legend(frameon=False,fontsize=7.5)
    ax2.axhline(.8,color=".6",ls=":",lw=1); ax2.axhline(.9,color=".7",ls=":",lw=1); ax2.set_ylim(-.02,1.02); ax2.set_ylabel("Fraction of resamples\nretaining p_adj < 0.05"); ax2.grid(alpha=.2); ax2.spines[["top","right"]].set_visible(False)
    labels=[]
    for f in fractions:
        medn,mn,mx=count_summary.get(float(f),(np.nan,0,0)); txt=f"median {medn:.0f}" if np.isfinite(medn) else "n/a"; txt+=f" ({mn}-{mx})" if mn!=mx else ""; labels.append(f"{int(100*f)}%\n{txt} trials/condition")
    ax2.set_xticks(x,labels); ax2.set_xlabel("Fraction of currently available repetitions retained")
    fig.suptitle(f"YELLOW trial-reduction robustness — {mode_title(mode)} — {depth_label}\n{group.replace('_',' ')}\n100%=original v9 result; reduced levels=resampled without replacement within session × value × intensity",fontsize=11.5); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(outdir/f"trial_reduction_{group}_ROBUSTNESS.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def run_trial_reduction_v4(full_yellow:pd.DataFrame,full_conds:pd.DataFrame,stats_out:dict[str,Any],areas:list[str],mode:str,depth_label:str,outdir:Path,n_resamples:int,response_permutations:int,seed:int):
    targets_by_group=significant_trial_reduction_targets_v4(stats_out,mode)
    if not targets_by_group:return {"performed":False,"reason":"No significant primary session-level YELLOW findings"}
    root=outdir/"trial_reduction_robustness"; root.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(seed); cache={}; signcache=V4SignCache(response_permutations,seed+991); all_targets=[t for v in targets_by_group.values() for t in v]; raw_rows=[]; count_summary={}
    counts=[]
    for path in full_yellow.trial_response_archive_path.dropna().astype(str).unique():
        arc=v4_load_archive(path,cache); _,cc=v4_sample_conditions(arc,1.,rng); counts.extend(cc)
    count_summary[1.]=(float(np.median(counts)) if counts else np.nan,int(np.min(counts)) if counts else 0,int(np.max(counts)) if counts else 0)
    for t in all_targets:raw_rows.append({"fraction":1.,"resample":0,"target_id":t["id"],"target_label":t["label"],"p_adjusted":t["original_p"]})
    for frac in TRIAL_REDUCTION_FRACTIONS[1:]:
        first_counts=None
        for rep in range(int(n_resamples)):
            rc,rq,cc=v4_reduced_yellow_data(full_yellow,float(frac),rng,cache,signcache); first_counts=cc if first_counts is None else first_counts; rs=build_v4_primary_stats(rc,rq,mode,areas)
            for t in all_targets:raw_rows.append({"fraction":float(frac),"resample":rep,"target_id":t["id"],"target_label":t["label"],"p_adjusted":v4_extract_target_p(rs,t)})
        cc=first_counts or []; count_summary[float(frac)]=(float(np.median(cc)) if cc else np.nan,int(np.min(cc)) if cc else 0,int(np.max(cc)) if cc else 0)
    raw=pd.DataFrame(raw_rows); raw.to_csv(root/"trial_reduction_all_significant_targets_RAW.csv",index=False); summary=[]
    for group,targets in targets_by_group.items():
        graw=raw[raw.target_id.isin([t["id"] for t in targets])].copy(); graw.to_csv(root/f"trial_reduction_{group}_RAW.csv",index=False); v4_plot_trial_reduction(group,targets,graw,count_summary,mode,depth_label,root)
        for t in targets:
            for frac in TRIAL_REDUCTION_FRACTIONS:
                vals=finite_values(raw.loc[(raw.fraction==frac)&(raw.target_id==t["id"]),"p_adjusted"]); medn,mn,mx=count_summary[float(frac)]; summary.append({"group":group,"target":t["label"],"fraction":frac,"percent_trials":100*frac,"median_trials_per_condition":medn,"min_trials_per_condition":mn,"max_trials_per_condition":mx,"n_valid_resamples":len(vals),"median_p_adjusted":float(np.median(vals)) if len(vals) else np.nan,"p10":float(np.percentile(vals,10)) if len(vals) else np.nan,"p90":float(np.percentile(vals,90)) if len(vals) else np.nan,"significance_retention":float(np.mean(vals<.05)) if len(vals) else np.nan})
    pd.DataFrame(summary).to_csv(root/"trial_reduction_summary.csv",index=False); save_json(root/"trial_reduction_manifest.json",{"fractions":list(TRIAL_REDUCTION_FRACTIONS),"n_resamples_per_reduced_fraction":int(n_resamples),"response_signflip_permutations":int(response_permutations),"seed":int(seed),"sampling":"without replacement within session x tuning value x intensity condition","100_percent":"original v9/full-data significance; not rerandomized","targets":targets_by_group,"trial_count_summary":{str(k):v for k,v in count_summary.items()},"responsiveness_recomputed_for_reduced_data":True}); return {"performed":True,"groups":list(targets_by_group),"n_targets":len(all_targets),"output_root":str(root)}


# -----------------------------------------------------------------------------
# Reporting / compact tables
# -----------------------------------------------------------------------------

def v4_tuning_value_stats_table(stats_out:dict[str,Any],branch:str)->pd.DataFrame:
    rows=[]
    for col,rec in stats_out["tuning_profiles"][branch].items():
        s=rec["session_level_primary"]
        for pk,pr in s["pairwise"].items():rows.append({"subset":branch,"tuning_value_Hz":rec["tuning_value_Hz"],"response_column":col,"omnibus_H":s["omnibus"].get("H",np.nan),"omnibus_p":s["omnibus"].get("p",np.nan),"omnibus_p_holm_family":s["omnibus"].get("p_holm_family",np.nan),"area1":pr["area1"],"area2":pr["area2"],"U":pr["U"],"p":pr["p"],"p_holm":pr["p_holm"],"cliffs_delta":pr["cliffs_delta"]})
    return pd.DataFrame(rows)


def v4_tuning_value_responsiveness_table(stats_out:dict[str,Any])->pd.DataFrame:
    rows=[]
    for flag,rec in stats_out["responsiveness"]["by_tuning_value"].items():
        s=rec["session_level_primary"]
        for pk,pr in s["pairwise"].items():rows.append({"tuning_value_Hz":rec["tuning_value_Hz"],"flag_column":flag,"omnibus_H":s["omnibus"].get("H",np.nan),"omnibus_p":s["omnibus"].get("p",np.nan),"omnibus_p_holm_family":s["omnibus"].get("p_holm_family",np.nan),"area1":pr["area1"],"area2":pr["area2"],"U":pr["U"],"p":pr["p"],"p_holm":pr["p_holm"],"cliffs_delta":pr["cliffs_delta"]})
    return pd.DataFrame(rows)


def v4_condition_stats_table(stats_out:dict[str,Any],branch:str)->pd.DataFrame:
    rows=[]
    for key,rec in stats_out["intensity_profiles"][branch].items():
        s=rec["session_level_primary"]
        for pk,pr in s["pairwise"].items():rows.append({"subset":branch,"tuning_value_Hz":rec["tuning_value_Hz"],"intensity_dB":rec["intensity_dB"],"omnibus_H":s["omnibus"].get("H",np.nan),"omnibus_p":s["omnibus"].get("p",np.nan),"omnibus_p_holm_family":s["omnibus"].get("p_holm_family",np.nan),"area1":pr["area1"],"area2":pr["area2"],"U":pr["U"],"p":pr["p"],"p_holm":pr["p_holm"],"cliffs_delta":pr["cliffs_delta"]})
    return pd.DataFrame(rows)


def write_report_v4(path:Path,subject:str,dates:list[str],mode:str,cell_class:str,depth_label:str,cells:pd.DataFrame,areas:list[str],stats_out:dict[str,Any],trial_result:dict[str,Any]|None=None):
    lines=["CROSS-AREA AM/FREQUENCY TUNING CELL-CLASS ANALYSIS — v4","="*78,f"Subject: {subject}",f"Dates: {', '.join(dates)}",f"Tuning mode: {mode_title(mode)}",f"Cell class: {cell_class.upper()}",f"Depth stratum: {depth_label}","","PRIMARY INFERENCE: one summary value per imaging session.","Cross-area tests: Kruskal-Wallis; pairwise Mann-Whitney U with Holm across the three area pairs.","Pooled-cell tests are exploratory/descriptive only.","Primary selectivity family: lifetime sparseness, Gini, Fano, and FWHM; Holm across four omnibus tests.","Primary v9 responsiveness: union of tuning-value-specific BH-FDR discoveries.","All numeric frequency/AM-rate axes use x=log2(value).",""]
    lines.append("Counts:")
    for area in areas:
        adf=cells[cells.canonicalArea==area]; lines.append(f"  {area}: {len(adf)} cells from {adf.session_key.nunique()} sessions; responsive={int(v4_bool_series(adf.stim_responsive_fdr).sum())}")
    lines.append("")
    lines.append("RESPONSIVENESS")
    for metric,rec in stats_out["responsiveness"]["overall"].items():
        s=rec["session_level_primary"]; o=s["omnibus"]; lines.append(f"{rec['label']}: H={o.get('H',np.nan):.4g}, p={o.get('p',np.nan):.4g}, Holm-family p={o.get('p_holm_family',np.nan):.4g}")
        for pr in s["pairwise"].values(): lines.append(f"  {pr['area1']} vs {pr['area2']}: p={pr['p']:.4g}, Holm p={pr['p_holm']:.4g}, Cliff delta={pr['cliffs_delta']:.3g}")
    for branch in ("all_cells","responsive_only"):
        lines += ["",f"SELECTIVITY — {branch.replace('_',' ').upper()}"]
        for metric in V4_PRIMARY_SELECTIVITY:
            rec=stats_out["selectivity"][branch][metric]; s=rec["session_level_primary"]; o=s["omnibus"]; lines.append(f"{rec['label']}: H={o.get('H',np.nan):.4g}, p={o.get('p',np.nan):.4g}, Holm-family p={o.get('p_holm_family',np.nan):.4g}")
            for pr in s["pairwise"].values(): lines.append(f"  {pr['area1']} vs {pr['area2']}: p={pr['p']:.4g}, Holm p={pr['p_holm']:.4g}, Cliff delta={pr['cliffs_delta']:.3g}")
    if trial_result is not None: lines += ["","YELLOW TRIAL-REDUCTION ROBUSTNESS",json.dumps(trial_result,default=json_default)]
    path.write_text("\n".join(lines)+"\n")


def v4_quick_rows(mode:str,depth_label:str,cell_class:str,stats_out:dict[str,Any]):
    rows=[]
    for family,branch,items in [
        ("responsiveness","overall",stats_out["responsiveness"]["overall"]),
        ("responsiveness","by_tuning_value",stats_out["responsiveness"]["by_tuning_value"]),
    ]:
        for key,rec in items.items():
            s=rec["session_level_primary"]
            for pr in s["pairwise"].values():rows.append({"tuning_mode":mode,"depth_stratum":depth_label,"cell_class":cell_class,"family":family,"subset":branch,"metric":key,"area1":pr["area1"],"area2":pr["area2"],"p":pr["p"],"p_holm":pr["p_holm"],"cliffs_delta":pr["cliffs_delta"]})
    for branch in ("all_cells","responsive_only"):
        for metric in V4_PRIMARY_SELECTIVITY:
            s=stats_out["selectivity"][branch][metric]["session_level_primary"]
            for pr in s["pairwise"].values():rows.append({"tuning_mode":mode,"depth_stratum":depth_label,"cell_class":cell_class,"family":"selectivity","subset":branch,"metric":metric,"area1":pr["area1"],"area2":pr["area2"],"p":pr["p"],"p_holm":pr["p_holm"],"cliffs_delta":pr["cliffs_delta"]})
    return rows


# -----------------------------------------------------------------------------
# Executed v4 main
# -----------------------------------------------------------------------------

def main_v4() -> None:
    args=parse_args_v4(); subject=str(args.subject); dates=[str(d) for d in args.dates]; areas=list(args.areas); modes=list(TUNING_MODES) if args.mode=="both" else [args.mode]; outroot=output_root(subject,dates)
    print("="*78); print("AM_TUNING CROSS-AREA CELL-CLASS ANALYSIS v4"); print("="*78); print(f"Subject: {subject}"); print(f"Dates:   {', '.join(dates)}"); print(f"Areas:   {', '.join(areas)}"); print(f"Modes:   {', '.join(modes)}"); print(f"Output root: {outroot}")
    expected={}
    for mode in modes:
        expected[mode]={}; print(f"\n{mode} expected inputs:")
        for area in areas:
            cp=expected_area_cell_csv(subject,area,dates,mode); qp=expected_area_condition_csv(subject,area,dates,mode); expected[mode][area]={"cell":str(cp),"condition":str(qp)}; print(f"  {area}: {cp.parent} [{'FOUND' if cp.exists() and qp.exists() else 'MISSING'}]")
    if args.dry_run:return
    outroot.mkdir(parents=True,exist_ok=True); save_json(outroot/"run_manifest.json",{"script_version":"v4","subject":subject,"dates":dates,"areas":areas,"modes":modes,"inputs":expected,"prerequisite":"am_tuning_area_analysis_v9.py","primary_inference":"session-level; Kruskal-Wallis + pairwise Mann-Whitney, pairwise Holm","selectivity_family":list(V4_PRIMARY_SELECTIVITY),"responsiveness":"v9 tuning-value-specific BH-FDR union","alternate_dff_sensitivity":[V4_LIFETIME_SESSION_MEDIAN,V4_LIFETIME_PRESTIM60],"numeric_tuning_axes":"explicit x=log2(value) for frequency and AM rate","trial_reduction":{"fractions":list(TRIAL_REDUCTION_FRACTIONS),"resamples":args.trial_reduction_resamples,"response_permutations":args.trial_reduction_response_permutations,"seed":args.trial_reduction_seed,"enabled":not args.skip_trial_reduction}})
    quick=[]
    for mode in modes:
        print("\n"+"="*78); print(f"MODE: {mode}"); print("="*78); cells,conds,_=load_mode_tables_v4(subject,dates,areas,mode); cells=cells[cells.cell_class.isin(CELL_CLASSES)].copy(); conds=conds[conds.cell_class.isin(CELL_CLASSES)].copy(); mode_root=outroot/mode; mode_root.mkdir(parents=True,exist_ok=True); cells.to_csv(mode_root/"all_areas_combined_cell_results.csv",index=False); conds.to_csv(mode_root/"all_areas_combined_condition_results.csv",index=False)
        for depth_label in DEPTH_STRATA:
            dc=subset_depth(cells,depth_label); dq=subset_depth(conds,depth_label); print(f"\nDepth: {depth_label}")
            for cell_class in CELL_CLASSES:
                cdf=dc[dc.cell_class==cell_class].copy(); qdf=dq[dq.cell_class==cell_class].copy(); leaf=mode_root/depth_label/cell_class; leaf.mkdir(parents=True,exist_ok=True); sdf=aggregate_sessions_v4(cdf,mode); cdf.to_csv(leaf/"cell_results.csv",index=False); qdf.to_csv(leaf/"condition_results.csv",index=False); sdf.to_csv(leaf/"session_summary.csv",index=False); stats_out=build_v4_primary_stats(cdf,qdf,mode,areas); save_json(leaf/"statistics.json",stats_out)
                pd.concat([v4_tuning_value_stats_table(stats_out,"all_cells"),v4_tuning_value_stats_table(stats_out,"responsive_only")],ignore_index=True).to_csv(leaf/"tuning_value_statistics.csv",index=False); v4_tuning_value_responsiveness_table(stats_out).to_csv(leaf/"tuning_value_responsiveness_statistics.csv",index=False); pd.concat([v4_condition_stats_table(stats_out,"all_cells"),v4_condition_stats_table(stats_out,"responsive_only")],ignore_index=True).to_csv(leaf/"condition_response_statistics.csv",index=False)
                v4_plot_responsiveness(cdf,stats_out,areas,cell_class,depth_label,mode,leaf); v4_plot_tuning_profile(cdf,stats_out,areas,cell_class,depth_label,mode,leaf,False); v4_plot_tuning_profile(cdf,stats_out,areas,cell_class,depth_label,mode,leaf,True); v4_plot_preferred_distribution(cdf,areas,cell_class,depth_label,mode,leaf,False); v4_plot_preferred_distribution(cdf,areas,cell_class,depth_label,mode,leaf,True); v4_plot_selectivity(cdf,stats_out,areas,cell_class,depth_label,mode,leaf); v4_plot_intensity_profiles(qdf,stats_out,areas,cell_class,depth_label,mode,leaf,False); v4_plot_intensity_profiles(qdf,stats_out,areas,cell_class,depth_label,mode,leaf,True)
                trial_result=None
                if cell_class=="yellow" and not args.skip_trial_reduction and len(cdf):
                    trial_result=run_trial_reduction_v4(cdf,qdf,stats_out,areas,mode,depth_label,leaf,args.trial_reduction_resamples,args.trial_reduction_response_permutations,args.trial_reduction_seed)
                write_report_v4(leaf/"REPORT.txt",subject,dates,mode,cell_class,depth_label,cdf,areas,stats_out,trial_result); write_figure_index(leaf); quick.extend(v4_quick_rows(mode,depth_label,cell_class,stats_out)); print(f"  {cell_class.upper():6s}: {len(cdf)} cells, {cdf.session_key.nunique() if len(cdf) else 0} sessions -> {leaf}")
        make_area_layer_outputs_v4(cells,areas,mode,mode_root)
    if quick:pd.DataFrame(quick).to_csv(outroot/"SESSION_LEVEL_PAIRWISE_QUICKVIEW.csv",index=False)
    print("\n"+"="*78); print("DONE"); print(f"Outputs saved under: {outroot}"); print("="*78)


if __name__ == "__main__":
    main_v4()
