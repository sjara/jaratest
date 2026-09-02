#!/usr/bin/env python3
"""
Cross-area comparison of AM-tuning responses within YELLOW or GREEN cells.

This is the second-stage follow-up analysis for am_tuning_area_analysis_v3.py.
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

The prerequisite files are produced by am_tuning_area_analysis_v3.py.

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
                raise ValueError(f"{path} has no canonicalArea column; expected am_tuning_area_analysis_v3.py output.")
            bad=set(df.canonicalArea.dropna().astype(str).unique())-{area}
            if bad: raise ValueError(f"{path} contains unexpected canonicalArea values: {sorted(bad)}")
            if "tuning_mode" not in df.columns:
                raise ValueError(f"{path} has no tuning_mode column.")
            badmode=set(df.tuning_mode.dropna().astype(str).unique())-{mode}
            if badmode: raise ValueError(f"{path} contains unexpected tuning_mode values: {sorted(badmode)}")
        cell_frames.append(cdf); cond_frames.append(qdf)
    if missing:
        msg="Missing prerequisite AM area-analysis output(s):\n"+"\n".join(f"  {p}" for p in missing)
        msg += "\nRun am_tuning_area_analysis_v3.py for each missing area using the same dates first."
        raise FileNotFoundError(msg)
    if not cell_frames: raise RuntimeError(f"No {mode} area tables were loaded.")
    cells=pd.concat(cell_frames,ignore_index=True,sort=False)
    conds=pd.concat(cond_frames,ignore_index=True,sort=False)
    required_cells={
        "subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode",
        "stim_responsive_fdr","stim_excited_fdr","stim_suppressed_fdr","stim_response_mean",
        "best_tuning_response","peak_absolute_response","tuning_modulation_depth",
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
    if mode=="tuningFreq": labels=[f"{v/1000:g}" for v in values]
    else: labels=[f"{v:g}" for v in values]
    return cols,values,labels


def mode_axis_label(mode: str) -> str:
    return "Frequency (kHz)" if mode=="tuningFreq" else "AM rate (Hz)"


def mode_title(mode: str) -> str:
    return "Frequency tuning" if mode=="tuningFreq" else "AM-rate tuning"


# =============================================================================
# SESSION AGGREGATION / STATISTICS
# =============================================================================

def aggregate_sessions(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    rows=[]
    group_cols=["subject","date","session","session_key","canonicalArea","brainArea","depth","cell_class","tuning_mode"]
    response_cols,_,_=response_columns(df,mode)
    for keys,sdf in df.groupby(group_cols,dropna=False):
        row=dict(zip(group_cols,keys)); n=len(sdf)
        row["n_cells"]=int(n)
        row["n_stim_responsive_fdr"]=int(sdf.stim_responsive_fdr.astype(bool).sum())
        row["pct_stim_responsive_fdr"]=100*row["n_stim_responsive_fdr"]/n if n else np.nan
        row["pct_stim_excited_fdr"]=100*float(sdf.stim_excited_fdr.astype(bool).mean()) if n else np.nan
        row["pct_stim_suppressed_fdr"]=100*float(sdf.stim_suppressed_fdr.astype(bool).mean()) if n else np.nan
        for metric,cfg in CONTINUOUS_METRICS.items():
            vals=finite_values(sdf[metric])
            if len(vals)==0: value=np.nan
            elif cfg["session_agg"]=="median": value=float(np.median(vals))
            else: value=float(np.mean(vals))
            row[metric]=value
        for col in response_cols:
            vals=finite_values(sdf[col]); row[col]=float(np.mean(vals)) if len(vals) else np.nan
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
    vals=list(means[finite])
    if errors is not None:
        errors=np.asarray(errors,dtype=float)
        for m,e in zip(means,errors):
            if np.isfinite(m) and np.isfinite(e): vals.extend([m-e,m+e])
    if reference_values: vals.extend([x for x in reference_values if np.isfinite(x)])
    lo=float(np.min(vals)); hi=float(np.max(vals)); span=hi-lo
    if not np.isfinite(span) or span==0: span=max(abs(lo),abs(hi),1.0)*0.25
    return lo-pad_fraction*span,hi+pad_fraction*span


def annotate_mean_sem(ax,x,mean,sem,n,color,y_top=None):
    if not np.isfinite(mean): return
    semtxt=f"{sem:.4g}" if np.isfinite(sem) else "n/a"
    txt=f"{mean:.4g} ± {semtxt}\nn={n}"
    if y_top is None: ax.text(x,mean,txt,ha="center",va="bottom",fontsize=7.5,color=color)
    else: ax.text(x,y_top,txt,ha="center",va="top",fontsize=7.5,color=color)


def plot_metric_grid(cell_df,session_df,areas,cell_class,depth_label,mode,output_path,display_mode,subset_label):
    metrics=list(CONTINUOUS_METRICS.keys())
    fig,axes=plt.subplots(2,3,figsize=(16.5,9.5)); axes=axes.ravel(); rng=np.random.default_rng(0)
    source=session_df if display_mode=="session_mean" else cell_df
    for ax,metric in zip(axes,metrics):
        cfg=CONTINUOUS_METRICS[metric]; ref=cfg["reference"]; x=np.arange(len(areas)); means=[]; sems=[]; ns=[]
        for xi,area in enumerate(areas):
            vals=finite_values(source.loc[source.canonicalArea==area,metric])
            m,se,n=mean_sem(vals); means.append(m); sems.append(se); ns.append(n)
            if display_mode=="with_cells" and len(vals):
                jitter=rng.normal(0,0.055,len(vals)); ax.scatter(np.full(len(vals),xi)+jitter,vals,s=10,alpha=.22,color=AREA_COLORS[area],edgecolors="none")
            if np.isfinite(m): ax.errorbar(xi,m,yerr=se if np.isfinite(se) else None,fmt="o",ms=7,capsize=4,lw=1.8,color=AREA_COLORS[area])
        means=np.asarray(means,float); sems=np.asarray(sems,float)
        if ref is not None: ax.axhline(ref,ls="--",lw=.9,color=".45")
        if display_mode in ("mean_only","session_mean"):
            ylim=optimized_ylim_from_summary(means,sems,[ref] if ref is not None else None)
            if ylim: ax.set_ylim(*ylim)
            ytop=ax.get_ylim()[1]-.03*(ax.get_ylim()[1]-ax.get_ylim()[0])
            for xi,area,m,se,n in zip(x,areas,means,sems,ns): annotate_mean_sem(ax,xi,m,se,n,AREA_COLORS[area],ytop)
        else:
            vals_all=finite_values(source[metric])
            if len(vals_all)>=4:
                q1,q3=np.percentile(vals_all,[25,75]); iqr=q3-q1
                if np.isfinite(iqr) and iqr>0:
                    inl=vals_all[(vals_all>=q1-3*iqr)&(vals_all<=q3+3*iqr)]
                    if len(inl):
                        lo,hi=float(np.min(inl)),float(np.max(inl));
                        if ref is not None: lo,hi=min(lo,ref),max(hi,ref)
                        span=hi-lo if hi>lo else max(abs(lo),1)*.25; ax.set_ylim(lo-.08*span,hi+.14*span)
        ax.set_xticks(x,areas); ax.set_title(cfg["label"],fontsize=10); ax.grid(axis="y",alpha=.22)
    display_title={"with_cells":"cell distributions + mean ± SEM","mean_only":"cell mean ± SEM; individual cells not shown","session_mean":"SESSION mean ± SEM; one summary per imaging session"}[display_mode]
    fig.suptitle(f"{cell_class.upper()} cells across A1 / AAF / A2 — {depth_label}\n{mode_title(mode)} | {subset_label}: {display_title}",fontsize=13)
    fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(output_path,dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_responsiveness(cell_df,session_df,areas,cell_class,depth_label,mode,outdir):
    metrics=[("stim_responsive_fdr","pct_stim_responsive_fdr","Responsive"),("stim_excited_fdr","pct_stim_excited_fdr","Excited"),("stim_suppressed_fdr","pct_stim_suppressed_fdr","Suppressed")]
    x=np.arange(len(metrics)); width=.22
    fig,ax=plt.subplots(figsize=(9,5.5))
    for ai,area in enumerate(areas):
        vals=[]
        for cellcol,_,_ in metrics:
            adf=cell_df[cell_df.canonicalArea==area]; vals.append(100*adf[cellcol].astype(bool).mean() if len(adf) else np.nan)
        xx=x+(ai-(len(areas)-1)/2)*width; ax.bar(xx,vals,width=width,color=AREA_COLORS[area],alpha=.82,label=area)
        for xxx,yy in zip(xx,vals):
            if np.isfinite(yy): ax.text(xxx,yy,f"{yy:.1f}%",ha="center",va="bottom",fontsize=7,rotation=90)
    ax.set_xticks(x,[m[2] for m in metrics]); ax.set_ylabel("Cells (%)"); ax.set_ylim(0,max(5,min(100,ax.get_ylim()[1]*1.15)))
    ax.set_title(f"{cell_class.upper()} | {mode_title(mode)} | {depth_label}\npooled-cell descriptive percentages"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
    fig.tight_layout(); fig.savefig(outdir/"responsiveness_pooled_cell_percentages.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)

    fig,ax=plt.subplots(figsize=(9,5.5))
    for ai,area in enumerate(areas):
        means=[]; sems=[]; ns=[]
        for _,pctcol,_ in metrics:
            m,se,n=mean_sem(session_df.loc[session_df.canonicalArea==area,pctcol]); means.append(m); sems.append(se); ns.append(n)
        xx=x+(ai-(len(areas)-1)/2)*width; ax.errorbar(xx,means,yerr=sems,fmt="o",ms=8,capsize=5,lw=2,color=AREA_COLORS[area],label=area)
        for xxx,m,se,n in zip(xx,means,sems,ns):
            if np.isfinite(m): ax.text(xxx,m,f"{m:.1f}±{se:.1f}\nn={n}" if np.isfinite(se) else f"{m:.1f}\nn={n}",ha="center",va="bottom",fontsize=7)
    ax.set_xticks(x,[m[2] for m in metrics]); ax.set_ylabel("Session percentage (%)")
    ax.set_title(f"{cell_class.upper()} | {mode_title(mode)} | {depth_label}\nSESSION mean ± SEM"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25)
    fig.tight_layout(); fig.savefig(outdir/"responsiveness_session_mean_sem_only.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profile(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    cols,values,labels=response_columns(cell_df,mode)
    if not cols: return
    x=values/1000 if mode=="tuningFreq" else values
    fig,ax=plt.subplots(figsize=(9,5.8)); allmeans=[]; allsems=[]; text=[]
    for area in areas:
        means=[]; sems=[]; ns=[]
        for col in cols:
            m,se,n=mean_sem(cell_df.loc[cell_df.canonicalArea==area,col]); means.append(m); sems.append(se); ns.append(n)
        allmeans.extend(means); allsems.extend(sems)
        ax.errorbar(x,means,yerr=sems,marker="o",capsize=4,lw=2,color=AREA_COLORS[area],label=area)
        text.append(f"{area}: n={max(ns) if ns else 0}")
    ylim=optimized_ylim_from_summary(np.asarray(allmeans),np.asarray(allsems),[0])
    if ylim: ax.set_ylim(*ylim)
    ax.axhline(0,ls="--",lw=1,color=".45"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Response (dF/F)")
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')} | mean ± SEM")
    ax.legend(frameon=False); ax.grid(alpha=.22); ax.text(.01,.01,"; ".join(text),transform=ax.transAxes,ha="left",va="bottom",fontsize=7)
    fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_tuning_profile_session(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    sdf=aggregate_sessions(cell_df,mode) if len(cell_df) else pd.DataFrame()
    cols,values,labels=response_columns(cell_df,mode)
    if not cols or len(sdf)==0: return
    x=values/1000 if mode=="tuningFreq" else values
    fig,ax=plt.subplots(figsize=(9,5.8)); allmeans=[]; allsems=[]
    for area in areas:
        means=[]; sems=[]
        for col in cols:
            m,se,n=mean_sem(sdf.loc[sdf.canonicalArea==area,col]); means.append(m); sems.append(se)
        allmeans.extend(means); allsems.extend(sems); ax.errorbar(x,means,yerr=sems,marker="o",capsize=4,lw=2,color=AREA_COLORS[area],label=area)
    ylim=optimized_ylim_from_summary(np.asarray(allmeans),np.asarray(allsems),[0]);
    if ylim: ax.set_ylim(*ylim)
    ax.axhline(0,ls="--",lw=1,color=".45"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Session mean response (dF/F)")
    ax.set_title(f"{cell_class.upper()} cells across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')} | SESSION mean ± SEM")
    ax.legend(frameon=False); ax.grid(alpha=.22); fig.tight_layout(); fig.savefig(outdir/f"tuning_profile_{suffix}_SESSION_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_preferred_distribution(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    vals=np.sort(pd.to_numeric(cell_df.preferred_tuning_value_Hz,errors="coerce").dropna().unique())
    if len(vals)==0: return
    x=vals/1000 if mode=="tuningFreq" else vals
    fig,ax=plt.subplots(figsize=(9,5.4))
    for area in areas:
        adf=cell_df[cell_df.canonicalArea==area]; pref=pd.to_numeric(adf.preferred_tuning_value_Hz,errors="coerce")
        pct=np.array([100*np.mean(np.isclose(pref,v,equal_nan=False)) if len(pref) else np.nan for v in vals])
        ax.plot(x,pct,marker="o",lw=2,color=AREA_COLORS[area],label=f"{area} (n={len(adf)})")
    ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel("Cells preferring value (%)"); ax.set_ylim(bottom=0)
    ax.set_title(f"{cell_class.upper()} preferred tuning across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')}")
    ax.legend(frameon=False); ax.grid(alpha=.22); fig.tight_layout(); fig.savefig(outdir/f"preferred_tuning_distribution_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_selectivity_rasters(cell_df,areas,cell_class,depth_label,mode,outdir,suffix):
    cols,values,labels=response_columns(cell_df,mode)
    if len(cols)<2: return
    fig,axes=plt.subplots(len(areas),1,figsize=(9,3.5*len(areas)),squeeze=False); im=None
    for row,area in enumerate(areas):
        ax=axes[row,0]; adf=cell_df[cell_df.canonicalArea==area].copy()
        if len(adf)==0: ax.text(.5,.5,"No cells",transform=ax.transAxes,ha="center",va="center"); ax.set_axis_off(); continue
        mat=adf[cols].to_numpy(float); denom=np.nanmax(np.abs(mat),axis=1); good=np.isfinite(denom)&(denom>0); mat=mat[good]; adf=adf.iloc[np.where(good)[0]].copy()
        if len(mat)==0: ax.text(.5,.5,"No finite responses",transform=ax.transAxes,ha="center",va="center"); continue
        norm=mat/denom[good,None]; pref=pd.to_numeric(adf.preferred_tuning_value_Hz,errors="coerce").to_numpy(float); order=np.argsort(np.nan_to_num(pref,nan=np.inf)); norm=norm[order]
        im=ax.imshow(norm,aspect="auto",interpolation="nearest",vmin=-1,vmax=1,cmap="coolwarm"); ax.set_xticks(np.arange(len(labels)),labels,rotation=30,ha="right"); ax.set_ylabel(f"{area} cells"); ax.set_title(f"{area}: n={len(norm)} | sorted by preferred tuning")
    fig.suptitle(f"{cell_class.upper()} tuning selectivity across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')}",y=1.01)
    if im is not None: fig.colorbar(im,ax=axes.ravel().tolist(),label="Normalized tuning response",shrink=.75)
    fig.subplots_adjust(left=0.09, right=0.88, bottom=0.10, top=0.92, hspace=0.45)
    fig.savefig(outdir/f"selectivity_rasters_{suffix}.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def plot_intensity_condition_grid(cond_df,areas,cell_class,depth_label,mode,outdir,suffix,metric,label,filename):
    if len(cond_df)==0: return
    intens=np.sort(pd.to_numeric(cond_df.intensity_dB,errors="coerce").dropna().unique()); values=np.sort(pd.to_numeric(cond_df.tuning_value_Hz,errors="coerce").dropna().unique())
    if len(intens)==0 or len(values)==0: return
    ncols=2; nrows=math.ceil(len(intens)/ncols); fig,axes=plt.subplots(nrows,ncols,figsize=(13,4.4*nrows),squeeze=False); axes=axes.ravel(); x=values/1000 if mode=="tuningFreq" else values
    for ax,intensity in zip(axes,intens):
        allmeans=[]; allsems=[]
        for area in areas:
            means=[]; sems=[]
            for value in values:
                vals=cond_df.loc[(cond_df.canonicalArea==area)&np.isclose(cond_df.intensity_dB,intensity)&np.isclose(cond_df.tuning_value_Hz,value),metric]
                m,se,n=mean_sem(vals); means.append(m); sems.append(se)
            allmeans.extend(means); allsems.extend(sems); ax.errorbar(x,means,yerr=sems,marker="o",capsize=3,lw=1.8,color=AREA_COLORS[area],label=area)
        ylim=optimized_ylim_from_summary(np.asarray(allmeans),np.asarray(allsems),[0]);
        if ylim: ax.set_ylim(*ylim)
        ax.axhline(0,ls="--",lw=.8,color=".5"); ax.set_title(f"{intensity:g} dB"); ax.set_xlabel(mode_axis_label(mode)); ax.set_ylabel(label); ax.grid(alpha=.2)
    for ax in axes[len(intens):]: ax.set_axis_off()
    handles,labels_=axes[0].get_legend_handles_labels(); fig.legend(handles,labels_,frameon=False,loc="upper right")
    fig.suptitle(f"{cell_class.upper()} across areas — {depth_label}\n{mode_title(mode)} | {suffix.replace('_',' ')} | intensity-resolved mean ± SEM",y=.995)
    fig.tight_layout(rect=[0,0,.97,.96]); fig.savefig(outdir/f"{filename}_{suffix}_MEAN_SEM_ONLY.png",dpi=DPI,bbox_inches="tight"); plt.close(fig)


def make_figures(cell_df,cond_df,areas,cell_class,depth_label,mode,outdir,responsive_only):
    suffix="FDR_responsive_only" if responsive_only else "all_cells"; subset="FDR stimulus-responsive cells only" if responsive_only else "All classified cells"
    cdf=cell_df[cell_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cell_df.copy()
    qdf=cond_df[cond_df.stim_responsive_fdr.astype(bool)].copy() if responsive_only else cond_df.copy()
    sdf=aggregate_sessions(cdf,mode) if len(cdf) else pd.DataFrame(columns=["canonicalArea",*CONTINUOUS_METRICS.keys()])
    plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,mode,outdir/f"cross_area_tuning_metrics_{suffix}_with_cells.png","with_cells",subset)
    plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,mode,outdir/f"cross_area_tuning_metrics_{suffix}_MEAN_SEM_ONLY.png","mean_only",subset)
    if len(sdf): plot_metric_grid(cdf,sdf,areas,cell_class,depth_label,mode,outdir/f"cross_area_tuning_metrics_{suffix}_SESSION_MEAN_SEM_ONLY.png","session_mean",subset)
    plot_tuning_profile(cdf,areas,cell_class,depth_label,mode,outdir,suffix)
    plot_tuning_profile_session(cdf,areas,cell_class,depth_label,mode,outdir,suffix)
    plot_preferred_distribution(cdf,areas,cell_class,depth_label,mode,outdir,suffix)
    plot_selectivity_rasters(cdf,areas,cell_class,depth_label,mode,outdir,suffix)
    plot_intensity_condition_grid(qdf,areas,cell_class,depth_label,mode,outdir,suffix,"condition_response","Condition response (dF/F)","intensity_condition_response_profile")
    plot_intensity_condition_grid(qdf,areas,cell_class,depth_label,mode,outdir,suffix,"condition_selectivity_contrast","Condition selectivity contrast (dF/F)","intensity_condition_selectivity_profile")


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
                make_figures(cdf,qdf,areas,cell_class,depth_label,mode,leaf,False); make_figures(cdf,qdf,areas,cell_class,depth_label,mode,leaf,True); write_figure_index(leaf)
                for subset,statsout in (("all_cells",stats_all),("FDR_responsive_only",stats_resp)):
                    for metric,res in statsout.get("continuous",{}).items():
                        for _,rec in res["session_level_primary"]["pairwise_mannwhitney_holm"].items():
                            quick.append({"tuning_mode":mode,"depth_stratum":depth_label,"cell_class":cell_class,"subset":subset,"metric":metric,"area1":rec["area1"],"area2":rec["area2"],"n1_sessions":rec["n1"],"n2_sessions":rec["n2"],"U":rec["U"],"p":rec["p"],"p_holm":rec["p_holm"],"cliffs_delta":rec["cliffs_delta"]})
                print(f"  {cell_class.upper():6s}: {len(cdf)} cells, {sdf.session_key.nunique() if len(sdf) else 0} sessions -> {leaf}")
    save_quickview(outroot,quick)
    print("\n"+"="*78); print("DONE"); print(f"Outputs saved under: {outroot}"); print("="*78)


if __name__ == "__main__":
    main()
