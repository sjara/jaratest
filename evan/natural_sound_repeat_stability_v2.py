#!/usr/bin/env python3
"""
Repeat-number stability analysis for natural-sound two-photon responses.

This script consumes `natural_sound_trial_responses.npz` archives produced by
natural_sound_response_analysis_v2.py and asks the design question:

    How many repeated exemplars/presentations are needed before estimates of the
    response mean and, especially, the repeat-to-repeat response variance become
    reasonably stable?

It is deliberately session-generic. It can combine any number of natural-sound
sessions, with different cells, sound sets, and repeat counts. No repeat count is
hard-coded. The available k range is inferred from the archives.

Primary resampling unit
-----------------------
A unit is one cell x one natural-sound CONDITION. Conditions are already defined
upstream so that, by default, sound location and target intensity are separated
when they vary. Thus the variance here is repeat-to-repeat variance to the same
stimulus condition, not variance caused by mixing sounds, locations, or levels.

By default the analysis includes every condition from cells classified as
`natural_responsive_fdr` upstream. In response-analysis v2 this is the GLOBAL
natural-sound responsiveness test (one sign-flip test per cell using all valid
natural-sound trials, followed by BH-FDR across cells). Use
--condition-responsive-only if you additionally want to restrict to cell x
condition pairs that were individually FDR-responsive. Use --cell-filter all
only as an explicit sensitivity/QC analysis that ignores the responsive-cell
filter.

For each unit with n repeats, and for every k=2..min(n,max_k), the script draws
k trials WITHOUT replacement many times. For each draw it calculates:

* mean response
* sample variance
* sample SD

and compares those estimates with the estimate obtained from all repeats for that
same cell x condition.

Stability metrics
-----------------
Variance stability:
* relative absolute error: |V_k - V_full| / max(V_full, variance_floor)
* absolute log2 variance ratio: |log2((V_k+floor)/(V_full+floor))|
* Spearman correlation across units between the median subsampled variance and
  the full-repeat variance

Mean stability:
* |mean_k - mean_full| / max(SD_full, sd_floor)

The script first summarizes resampling errors WITHIN each cell x condition and
then aggregates across units. This avoids storing millions of individual
resamples and prevents units with more Monte-Carlo draws from receiving more
weight.

Available-case versus fixed-cohort curves
-----------------------------------------
When sessions have different repeat counts, a naive k curve changes composition:
high k values automatically exclude low-repeat units. Therefore two versions are
reported:

1. available_case: at each k, use every unit with at least k repeats.
2. fixed_cohort: choose the largest K for which at least --fixed-cohort-min-units
   units have >=K repeats, then use that same cohort for every k<=K.

The fixed-cohort curve is preferable for judging how stability changes with k;
the available-case curve shows all usable data.

Design markers
--------------
--design-k defaults to 4 8 16. These are drawn as vertical lines when within the
observed range. A marker beyond the observed range is explicitly reported as
UNOBSERVED; the script never extrapolates performance to k values not supported
by the recordings.

A threshold summary can also identify the first OBSERVED k meeting user-defined
empirical criteria. Defaults are median variance relative error <=0.25 and
Spearman rho >=0.90. These are transparent engineering criteria, not statistical
power calculations and not universal biological thresholds.

Examples
--------
All natural-sound archives for imag039 on one date:

    python natural_sound_repeat_stability_v2.py imag039 --dates 20260717

Only sessions 004 and 008:

    python natural_sound_repeat_stability_v2.py imag039 --dates 20260717 \
        --sessions 004 008

Use the alternate whole-session-median dF/F sensitivity archive:

    python natural_sound_repeat_stability_v2.py imag039 --dates 20260717 \
        --response-source session_median

Increase Monte-Carlo resamples:

    python natural_sound_repeat_stability_v2.py imag039 --dates 20260717 \
        --n-resamples 2000

Outputs
-------
<TEMP_OUTPUT_PATH>/evan/natural_sound_repeat_stability/<subject>/<date_tag>/
    included_archives.csv
    unit_full_repeat_statistics.csv
    per_unit_k_stability.csv
    stability_summary_available_case.csv
    stability_summary_fixed_cohort.csv
    design_k_summary.csv
    threshold_crossings.json
    variance_stability_available_case.png
    variance_stability_fixed_cohort.png
    mean_stability_available_case.png
    mean_stability_fixed_cohort.png
    variance_recovery_scatter_k*.png
    run_manifest.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from jaratoolbox import settings


# =============================================================================
# CLI
# =============================================================================

RESPONSE_KEYS = {
    "primary": "trial_response_primary",
    "session_median": "trial_response_session_median",
    "local_60s": "trial_response_local_60s_prestim",
}


def normalize_dates(values: list[str]) -> list[str]:
    out=[]
    for value in values:
        for piece in str(value).replace(","," ").split():
            if len(piece)!=8 or not piece.isdigit():
                raise argparse.ArgumentTypeError(f"Invalid date {piece!r}; use YYYYMMDD")
            out.append(piece)
    return sorted(set(out))


def normalize_sessions(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    out=[]
    for value in values:
        for piece in str(value).replace(","," ").split():
            if piece.isdigit(): piece=f"{int(piece):03d}"
            out.append(piece)
    return sorted(set(out))


def normalize_areas(values: list[str] | None) -> list[str] | None:
    if not values: return None
    out=[]
    for value in values:
        v=str(value).upper()
        if v=="AUV": v="A2"
        if v not in {"A1","AAF","A2"}:
            raise argparse.ArgumentTypeError(f"Unknown area {value!r}")
        out.append(v)
    return sorted(set(out))


def parse_args() -> argparse.Namespace:
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject")
    p.add_argument("--dates",nargs="+",required=True)
    p.add_argument("--sessions",nargs="+",default=None)
    p.add_argument("--areas",nargs="+",default=None)
    p.add_argument("--response-source",choices=list(RESPONSE_KEYS),default="primary")
    p.add_argument("--cell-filter",choices=["responsive","all"],default="responsive",
                   help="Cell inclusion: primary natural-responsive cells (default) or all cells for QC/sensitivity.")
    p.add_argument("--condition-responsive-only",action="store_true",
                   help="Additionally use only individually FDR-responsive cell x condition pairs.")
    p.add_argument("--min-full-repeats",type=int,default=3,
                   help="Minimum full repeats for a unit to enter analysis. Default 3.")
    p.add_argument("--max-k",type=int,default=0,
                   help="Maximum k to test; 0 = use largest observed repeat count.")
    p.add_argument("--n-resamples",type=int,default=500)
    p.add_argument("--seed",type=int,default=20260916)
    p.add_argument("--design-k",nargs="+",type=int,default=[4,8,16])
    p.add_argument("--fixed-cohort-min-units",type=int,default=50,
                   help="Minimum units required when choosing fixed-cohort Kmax. Default 50.")
    p.add_argument("--target-median-variance-relative-error",type=float,default=0.25)
    p.add_argument("--target-variance-spearman-rho",type=float,default=0.90)
    p.add_argument("--input-root",type=Path,default=None,
                   help="Override natural_sound_response_analysis root.")
    p.add_argument("--output-root",type=Path,default=None)
    args=p.parse_args()
    args.dates=normalize_dates(args.dates)
    args.sessions=normalize_sessions(args.sessions)
    args.areas=normalize_areas(args.areas)
    if args.min_full_repeats<2: p.error("--min-full-repeats must be >=2")
    if args.n_resamples<1: p.error("--n-resamples must be >=1")
    if args.max_k<0: p.error("--max-k must be >=0")
    args.design_k=sorted(set(k for k in args.design_k if k>=2))
    return args


# =============================================================================
# LOAD ARCHIVES
# =============================================================================


def scalar_string(x: np.ndarray) -> str:
    a=np.asarray(x)
    return str(a.item()) if a.ndim==0 else str(a.ravel()[0])


def scalar_float(x: np.ndarray) -> float:
    a=np.asarray(x)
    return float(a.item()) if a.ndim==0 else float(a.ravel()[0])


def discover_archives(args: argparse.Namespace) -> list[Path]:
    root=args.input_root
    if root is None:
        root=Path(settings.TEMP_OUTPUT_PATH)/"evan"/"natural_sound_response_analysis"/args.subject
    if not root.exists():
        raise FileNotFoundError(f"Input root does not exist: {root}")
    candidates=sorted(root.glob("*/*/natural_sound_trial_responses.npz"))
    selected=[]
    dates=set(args.dates); sessions=set(args.sessions) if args.sessions else None
    areas=set(args.areas) if args.areas else None
    for path in candidates:
        try:
            with np.load(path,allow_pickle=False) as z:
                subject=scalar_string(z["subject"]); date=scalar_string(z["date"]); session=scalar_string(z["session"])
                area=scalar_string(z["canonical_area"])
        except Exception as exc:
            print(f"[skip] cannot read {path}: {exc}")
            continue
        if subject!=args.subject or date not in dates: continue
        if sessions is not None and session not in sessions: continue
        if areas is not None and area not in areas: continue
        selected.append(path)
    return selected


def load_units_from_archive(path: Path,args: argparse.Namespace) -> tuple[list[dict[str,Any]],dict[str,Any]]:
    response_key=RESPONSE_KEYS[args.response_source]
    with np.load(path,allow_pickle=False) as z:
        schema=scalar_string(z["schema"]) if "schema" in z else "unknown"
        if schema not in {"natural_sound_response_v1","natural_sound_response_v2"}:
            raise ValueError(f"Unsupported archive schema {schema!r} in {path}")
        if schema=="natural_sound_response_v1" and args.cell_filter=="responsive":
            print(f"[warning] {path} is a v1 archive: its responsive-cell label used the old condition-specific-union definition. "
                  "Rerun natural_sound_response_analysis_v2.py for the new global responsiveness definition.")
        subject=scalar_string(z["subject"]); date=scalar_string(z["date"]); session=scalar_string(z["session"])
        area=scalar_string(z["canonical_area"]); brain=scalar_string(z["brain_area"])
        depth=scalar_float(z["depth"])
        if response_key not in z:
            raise KeyError(f"Archive {path} lacks response array {response_key}")
        tr=np.asarray(z[response_key],dtype=float)
        analysis_trials=np.asarray(z["analysis_trials"],dtype=bool)
        cond_idx=np.asarray(z["condition_index_per_trial"],dtype=int)
        labels=np.asarray(z["condition_labels"]).astype(str)
        classes=np.asarray(z["cell_class"]).astype(str)
        cell_resp=np.asarray(z["cell_natural_responsive_fdr"],dtype=bool)
        roi=np.asarray(z["suite2p_roi_index"],dtype=int)
        cell_index=np.asarray(z["analysis_cell_index"],dtype=int)
        if tr.shape[0]!=len(classes) or tr.shape[1]!=len(analysis_trials):
            raise ValueError(f"Archive shape mismatch in {path}: responses={tr.shape}")

        # condition-responsive q-values are not stored in the NPZ. If requested,
        # read the sibling CSV generated by script 1.
        condition_responsive_map: dict[tuple[int,int],bool]={}
        if args.condition_responsive_only:
            csv=path.with_name("condition_results.csv")
            if not csv.exists():
                raise FileNotFoundError(f"--condition-responsive-only requires {csv}")
            cdf=pd.read_csv(csv)
            for row in cdf.itertuples(index=False):
                condition_responsive_map[(int(row.analysis_cell_index),int(row.condition_index))]=bool(row.condition_responsive_fdr)

        units=[]
        unique_conditions=sorted(c for c in np.unique(cond_idx[analysis_trials]) if c>=0)
        n_units_before_cell_filter=0
        for ci in range(tr.shape[0]):
            # Count units that have enough repeats even if the cell is later filtered.
            for cond in unique_conditions:
                pre_mask=analysis_trials & (cond_idx==cond) & np.isfinite(tr[ci])
                if int(np.sum(pre_mask))>=args.min_full_repeats:
                    n_units_before_cell_filter += 1
            if args.cell_filter=="responsive" and not cell_resp[ci]:
                continue
            for cond in unique_conditions:
                if args.condition_responsive_only and not condition_responsive_map.get((int(cell_index[ci]),int(cond)),False):
                    continue
                mask=analysis_trials & (cond_idx==cond) & np.isfinite(tr[ci])
                vals=np.asarray(tr[ci,mask],dtype=float)
                if len(vals)<args.min_full_repeats:
                    continue
                full_mean=float(np.mean(vals))
                full_var=float(np.var(vals,ddof=1)) if len(vals)>=2 else np.nan
                full_sd=float(np.sqrt(full_var)) if np.isfinite(full_var) and full_var>=0 else np.nan
                units.append({
                    "subject":subject,"date":date,"session":session,"session_key":f"{date}_{session}",
                    "canonical_area":area,"brain_area":brain,"depth":depth,
                    "analysis_cell_index":int(cell_index[ci]),"suite2p_roi_index":int(roi[ci]),"cell_class":classes[ci],
                    "condition_index":int(cond),"condition_label":labels[cond] if cond<len(labels) else f"condition_{cond}",
                    "n_full_repeats":int(len(vals)),"full_mean":full_mean,"full_variance":full_var,"full_sd":full_sd,
                    "values":vals,
                })
        repeat_counts=[]
        for cond in unique_conditions:
            repeat_counts.append(int(np.sum(analysis_trials & (cond_idx==cond))))
        meta={"path":str(path),"schema":schema,"subject":subject,"date":date,"session":session,"canonical_area":area,
              "brain_area":brain,"depth":depth,"n_units":len(units),"n_units_before_cell_filter":int(n_units_before_cell_filter),
              "n_cells":len(classes),"n_responsive_cells":int(np.sum(cell_resp)),"n_trials":int(np.sum(analysis_trials)),
              "n_conditions":len(unique_conditions),
              "min_condition_repeats":int(min(repeat_counts)) if repeat_counts else 0,
              "max_condition_repeats":int(max(repeat_counts)) if repeat_counts else 0}
    return units,meta


# =============================================================================
# RESAMPLING
# =============================================================================


def floors_from_units(units:list[dict[str,Any]]) -> tuple[float,float]:
    vars_=np.array([u["full_variance"] for u in units],float)
    sds=np.array([u["full_sd"] for u in units],float)
    posv=vars_[np.isfinite(vars_)&(vars_>0)]
    poss=sds[np.isfinite(sds)&(sds>0)]
    vf=max(1e-10,float(np.percentile(posv,1))*0.1) if len(posv) else 1e-10
    sf=max(1e-6,float(np.percentile(poss,1))*0.1) if len(poss) else 1e-6
    return vf,sf


def resample_one_unit(unit:dict[str,Any],k:int,n_resamples:int,rng:np.random.Generator,
                      variance_floor:float,sd_floor:float) -> dict[str,Any]:
    vals=np.asarray(unit["values"],float)
    n=len(vals)
    if k>n or k<2:
        raise ValueError("invalid k")
    submeans=np.empty(n_resamples,float)
    subvars=np.empty(n_resamples,float)
    for r in range(n_resamples):
        inds=rng.choice(n,size=k,replace=False)
        x=vals[inds]
        submeans[r]=np.mean(x)
        subvars[r]=np.var(x,ddof=1)
    fv=max(float(unit["full_variance"]),variance_floor)
    fs=max(float(unit["full_sd"]),sd_floor)
    rel_var_err=np.abs(subvars-unit["full_variance"])/fv
    abs_log2=np.abs(np.log2((subvars+variance_floor)/(unit["full_variance"]+variance_floor)))
    mean_std_err=np.abs(submeans-unit["full_mean"])/fs
    return {
        "k":int(k),"median_subsample_mean":float(np.median(submeans)),
        "median_subsample_variance":float(np.median(subvars)),
        "mean_subsample_variance":float(np.mean(subvars)),
        "median_variance_relative_abs_error":float(np.median(rel_var_err)),
        "p90_variance_relative_abs_error":float(np.percentile(rel_var_err,90)),
        "median_abs_log2_variance_ratio":float(np.median(abs_log2)),
        "p90_abs_log2_variance_ratio":float(np.percentile(abs_log2,90)),
        "median_mean_error_in_full_sd":float(np.median(mean_std_err)),
        "p90_mean_error_in_full_sd":float(np.percentile(mean_std_err,90)),
        "variance_ratio_median":float(np.median((subvars+variance_floor)/(unit["full_variance"]+variance_floor))),
    }


def make_per_unit_k_table(units:list[dict[str,Any]],args:argparse.Namespace,
                          variance_floor:float,sd_floor:float,max_k:int) -> pd.DataFrame:
    rows=[]
    for ui,u in enumerate(units):
        rng=np.random.default_rng(args.seed + 1000003*ui)
        this_max=min(max_k,int(u["n_full_repeats"]))
        for k in range(2,this_max+1):
            rec={kk:vv for kk,vv in u.items() if kk!="values"}
            rec.update(resample_one_unit(u,k,args.n_resamples,rng,variance_floor,sd_floor))
            rows.append(rec)
        if (ui+1)%500==0:
            print(f"  resampled {ui+1}/{len(units)} units")
    return pd.DataFrame(rows)


def safe_spearman(x:Iterable[float],y:Iterable[float]) -> tuple[float,float,int]:
    a=np.asarray(list(x),float); b=np.asarray(list(y),float)
    ok=np.isfinite(a)&np.isfinite(b)
    a=a[ok]; b=b[ok]
    if len(a)<3 or np.allclose(a,a[0]) or np.allclose(b,b[0]):
        return np.nan,np.nan,len(a)
    r,p=stats.spearmanr(a,b)
    return float(r),float(p),len(a)


def summarize_curve(per_unit:pd.DataFrame,cohort_units:set[tuple]|None=None) -> pd.DataFrame:
    df=per_unit.copy()
    keycols=["date","session","analysis_cell_index","condition_index"]
    df["unit_key"]=list(zip(*(df[c] for c in keycols)))
    if cohort_units is not None:
        df=df[df.unit_key.isin(cohort_units)]
    rows=[]
    for k,g in df.groupby("k",sort=True):
        rho,p,nrho=safe_spearman(g["median_subsample_variance"],g["full_variance"])
        # Pearson on log variance is also useful when variance spans orders of magnitude.
        vf=np.asarray(g.full_variance,float); sv=np.asarray(g.median_subsample_variance,float)
        pos=(vf>0)&(sv>0)&np.isfinite(vf)&np.isfinite(sv)
        if np.sum(pos)>=3:
            lr,lp=stats.pearsonr(np.log10(vf[pos]),np.log10(sv[pos]))
        else:
            lr,lp=np.nan,np.nan
        rows.append({
            "k":int(k),"n_units":int(g.unit_key.nunique()),"n_sessions":int(g.session_key.nunique()),
            "median_variance_relative_abs_error":float(np.nanmedian(g.median_variance_relative_abs_error)),
            "p90_variance_relative_abs_error":float(np.nanpercentile(g.median_variance_relative_abs_error,90)),
            "median_abs_log2_variance_ratio":float(np.nanmedian(g.median_abs_log2_variance_ratio)),
            "p90_abs_log2_variance_ratio":float(np.nanpercentile(g.median_abs_log2_variance_ratio,90)),
            "median_mean_error_in_full_sd":float(np.nanmedian(g.median_mean_error_in_full_sd)),
            "p90_mean_error_in_full_sd":float(np.nanpercentile(g.median_mean_error_in_full_sd,90)),
            "variance_spearman_rho":rho,"variance_spearman_p":p,"variance_spearman_n":nrho,
            "log10_variance_pearson_r":float(lr) if np.isfinite(lr) else np.nan,
            "log10_variance_pearson_p":float(lp) if np.isfinite(lp) else np.nan,
        })
    return pd.DataFrame(rows)


def choose_fixed_cohort(units:list[dict[str,Any]],max_k:int,min_units:int) -> tuple[int,set[tuple]]:
    def key(u): return (u["date"],u["session"],u["analysis_cell_index"],u["condition_index"])
    chosen=2
    for k in range(2,max_k+1):
        n=sum(int(u["n_full_repeats"])>=k for u in units)
        if n>=min_units:
            chosen=k
        else:
            break
    cohort={key(u) for u in units if int(u["n_full_repeats"])>=chosen}
    return chosen,cohort


# =============================================================================
# FIGURES / DESIGN SUMMARIES
# =============================================================================


def add_design_lines(ax,design_k:list[int],observed_max:int) -> None:
    ymax=ax.get_ylim()[1]
    for k in design_k:
        if k<=observed_max:
            ax.axvline(k,ls="--",lw=1,alpha=.5)
            ax.text(k,ymax,f" k={k}",rotation=90,va="top",ha="left",fontsize=8)


def plot_variance_stability(summary:pd.DataFrame,out:Path,title:str,design_k:list[int]) -> None:
    if summary.empty:return
    fig,ax=plt.subplots(figsize=(8.5,5.8))
    ax.plot(summary.k,summary.median_variance_relative_abs_error,marker="o",label="Median relative |variance error|")
    ax.plot(summary.k,summary.p90_variance_relative_abs_error,marker="o",ls="--",label="90th percentile")
    ax.set_xlabel("k repeated presentations used")
    ax.set_ylabel("|V_k - V_full| / V_full (floored)")
    ax.set_title(title)
    ax.grid(alpha=.25);ax.legend(frameon=False)
    add_design_lines(ax,design_k,int(summary.k.max()))
    fig.tight_layout();fig.savefig(out,dpi=250);plt.close(fig)

    fig,ax=plt.subplots(figsize=(8.5,5.8))
    ax.plot(summary.k,summary.variance_spearman_rho,marker="o")
    ax.axhline(.9,ls=":",lw=1)
    ax.set_ylim(-.05,1.05);ax.set_xlabel("k repeated presentations used");ax.set_ylabel("Spearman rho: V_k vs V_full")
    ax.set_title(title+"\nVariance rank-order recovery")
    ax.grid(alpha=.25);add_design_lines(ax,design_k,int(summary.k.max()))
    fig.tight_layout();fig.savefig(out.with_name(out.stem+"_spearman.png"),dpi=250);plt.close(fig)

    fig,ax1=plt.subplots(figsize=(8.5,5.8))
    ax1.plot(summary.k,summary.n_units,marker="o")
    ax1.set_xlabel("k repeated presentations used");ax1.set_ylabel("Number of cell x condition units")
    ax1.set_title(title+"\nAvailable sample size")
    ax1.grid(alpha=.25);add_design_lines(ax1,design_k,int(summary.k.max()))
    fig.tight_layout();fig.savefig(out.with_name(out.stem+"_n_units.png"),dpi=250);plt.close(fig)


def plot_mean_stability(summary:pd.DataFrame,out:Path,title:str,design_k:list[int]) -> None:
    if summary.empty:return
    fig,ax=plt.subplots(figsize=(8.5,5.8))
    ax.plot(summary.k,summary.median_mean_error_in_full_sd,marker="o",label="Median")
    ax.plot(summary.k,summary.p90_mean_error_in_full_sd,marker="o",ls="--",label="90th percentile")
    ax.set_xlabel("k repeated presentations used")
    ax.set_ylabel("|mean_k - mean_full| / SD_full (floored)")
    ax.set_title(title);ax.grid(alpha=.25);ax.legend(frameon=False)
    add_design_lines(ax,design_k,int(summary.k.max()))
    fig.tight_layout();fig.savefig(out,dpi=250);plt.close(fig)


def plot_recovery_scatter(per_unit:pd.DataFrame,k:int,out:Path,title:str) -> None:
    g=per_unit[per_unit.k==k]
    if len(g)<3:return
    x=np.asarray(g.full_variance,float);y=np.asarray(g.median_subsample_variance,float)
    ok=np.isfinite(x)&np.isfinite(y)&(x>0)&(y>0)
    if np.sum(ok)<3:return
    rho,p,_=safe_spearman(x[ok],y[ok])
    fig,ax=plt.subplots(figsize=(6.5,6))
    ax.scatter(x[ok],y[ok],s=13,alpha=.3)
    lo=min(np.min(x[ok]),np.min(y[ok]));hi=max(np.max(x[ok]),np.max(y[ok]))
    ax.plot([lo,hi],[lo,hi],ls="--",lw=1,color="black")
    ax.set_xscale("log");ax.set_yscale("log")
    ax.set_xlabel("Full-repeat variance");ax.set_ylabel(f"Median variance from k={k} subsamples")
    ax.set_title(f"{title}\nk={k}; Spearman rho={rho:.3f}, p={p:.3g}, n={np.sum(ok)}")
    ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out,dpi=250);plt.close(fig)


def design_summary(available:pd.DataFrame,fixed:pd.DataFrame,args:argparse.Namespace,observed_max:int) -> pd.DataFrame:
    rows=[]
    for k in args.design_k:
        for curve_name,curve in (("available_case",available),("fixed_cohort",fixed)):
            hit=curve[curve.k==k]
            row={"design_k":k,"curve":curve_name,"observed":bool(k<=observed_max and len(hit)>0)}
            if len(hit):
                r=hit.iloc[0]
                for col in ["n_units","n_sessions","median_variance_relative_abs_error","p90_variance_relative_abs_error",
                            "median_abs_log2_variance_ratio","variance_spearman_rho","median_mean_error_in_full_sd"]:
                    row[col]=r[col]
            rows.append(row)
    return pd.DataFrame(rows)


def threshold_crossing(curve:pd.DataFrame,args:argparse.Namespace) -> dict[str,Any]:
    ok=curve[(curve.median_variance_relative_abs_error<=args.target_median_variance_relative_error)&
             (curve.variance_spearman_rho>=args.target_variance_spearman_rho)]
    return {
        "target_median_variance_relative_error":args.target_median_variance_relative_error,
        "target_variance_spearman_rho":args.target_variance_spearman_rho,
        "first_observed_k_meeting_both":int(ok.k.min()) if len(ok) else None,
        "note":"Empirical stability criterion against the full-repeat estimate; not prospective power and not extrapolated beyond observed k."
    }


# =============================================================================
# MAIN
# =============================================================================


def main()->None:
    args=parse_args()
    archives=discover_archives(args)
    if not archives:
        raise RuntimeError("No matching natural_sound_trial_responses.npz archives were found. Run natural_sound_response_analysis_v2.py first.")
    print("="*80);print("NATURAL-SOUND REPEAT-NUMBER STABILITY v2");print("="*80)
    print(f"Archives: {len(archives)}")
    all_units=[];archive_meta=[]
    for path in archives:
        units,meta=load_units_from_archive(path,args)
        all_units.extend(units);archive_meta.append(meta)
        print(
            f"  {meta['date']} {meta['session']} {meta['canonical_area']}: "
            f"cells={meta['n_cells']}, responsive={meta['n_responsive_cells']}, "
            f"conditions={meta['n_conditions']}, repeats={meta['min_condition_repeats']}..{meta['max_condition_repeats']}, "
            f"units before cell filter={meta['n_units_before_cell_filter']}, eligible={meta['n_units']} "
            f"(schema={meta['schema']})"
        )
    if not all_units:
        nresp=sum(int(m.get("n_responsive_cells",0)) for m in archive_meta)
        if args.cell_filter=="responsive" and nresp==0:
            raise RuntimeError(
                "No eligible units because the input archives contain 0 natural-responsive cells. "
                "If these are v1 archives, rerun natural_sound_response_analysis_v2.py first; v2 uses the new global "
                "natural-sound responsiveness test. For QC only, you can run this script with --cell-filter all."
            )
        raise RuntimeError(
            "No eligible cell x condition units after filters. Check --min-full-repeats, "
            "--condition-responsive-only, and the per-session diagnostics printed above."
        )

    outroot=args.output_root
    if outroot is None:
        outroot=Path(settings.TEMP_OUTPUT_PATH)/"evan"/"natural_sound_repeat_stability"/args.subject/"_".join(args.dates)
    outroot.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(archive_meta).to_csv(outroot/"included_archives.csv",index=False)

    full_df=pd.DataFrame([{k:v for k,v in u.items() if k!="values"} for u in all_units])
    full_df.to_csv(outroot/"unit_full_repeat_statistics.csv",index=False)
    observed_max=int(full_df.n_full_repeats.max())
    max_k=observed_max if args.max_k==0 else min(observed_max,args.max_k)
    if max_k<2: raise RuntimeError("No unit has at least 2 repeats.")
    variance_floor,sd_floor=floors_from_units(all_units)
    print(f"Eligible units: {len(all_units)}; observed repeat range {full_df.n_full_repeats.min()}..{observed_max}; testing k=2..{max_k}")
    print(f"Variance floor={variance_floor:.3g}; SD floor={sd_floor:.3g}")

    per_unit=make_per_unit_k_table(all_units,args,variance_floor,sd_floor,max_k)
    per_unit.to_csv(outroot/"per_unit_k_stability.csv",index=False)
    available=summarize_curve(per_unit)
    available.to_csv(outroot/"stability_summary_available_case.csv",index=False)

    fixed_k,cohort=choose_fixed_cohort(all_units,max_k,args.fixed_cohort_min_units)
    fixed=summarize_curve(per_unit,cohort)
    fixed=fixed[fixed.k<=fixed_k].copy()
    fixed.to_csv(outroot/"stability_summary_fixed_cohort.csv",index=False)
    print(f"Fixed cohort: {len(cohort)} units with >= {fixed_k} repeats; curve k=2..{fixed_k}")

    plot_variance_stability(available,outroot/"variance_stability_available_case.png",
                            f"Available-case variance stability ({args.response_source})",args.design_k)
    plot_mean_stability(available,outroot/"mean_stability_available_case.png",
                        f"Available-case mean stability ({args.response_source})",args.design_k)
    plot_variance_stability(fixed,outroot/"variance_stability_fixed_cohort.png",
                            f"Fixed-cohort variance stability: same {len(cohort)} units, n_full >= {fixed_k}",args.design_k)
    plot_mean_stability(fixed,outroot/"mean_stability_fixed_cohort.png",
                        f"Fixed-cohort mean stability: same {len(cohort)} units, n_full >= {fixed_k}",args.design_k)

    for k in args.design_k:
        if k<=max_k:
            plot_recovery_scatter(per_unit,k,outroot/f"variance_recovery_scatter_k{k}.png","Natural-sound repeat variance recovery")

    ds=design_summary(available,fixed,args,observed_max)
    ds.to_csv(outroot/"design_k_summary.csv",index=False)
    crossings={"available_case":threshold_crossing(available,args),"fixed_cohort":threshold_crossing(fixed,args)}
    with (outroot/"threshold_crossings.json").open("w") as f:json.dump(crossings,f,indent=2)

    # Also produce class-specific curves. They are descriptive and useful for
    # checking whether GREEN/YELLOW variability gives the same design conclusion.
    class_summaries={}
    for cls in ("green","yellow"):
        sub=per_unit[per_unit.cell_class==cls].copy()
        if sub.empty:continue
        summ=summarize_curve(sub)
        summ.to_csv(outroot/f"stability_summary_available_case_{cls}.csv",index=False)
        plot_variance_stability(summ,outroot/f"variance_stability_available_case_{cls}.png",
                                f"{cls.upper()} variance stability ({args.response_source})",args.design_k)
        class_summaries[cls]={"n_units":int(sub[["date","session","analysis_cell_index","condition_index"]].drop_duplicates().shape[0])}

    manifest={
        "subject":args.subject,"dates":args.dates,"sessions_filter":args.sessions,"areas_filter":args.areas,
        "response_source":args.response_source,"cell_filter":args.cell_filter,
        "condition_responsive_only":args.condition_responsive_only,
        "n_archives":len(archives),"n_units":len(all_units),"observed_max_repeats":observed_max,"tested_max_k":max_k,
        "n_resamples":args.n_resamples,"seed":args.seed,"variance_floor":variance_floor,"sd_floor":sd_floor,
        "fixed_cohort_kmax":fixed_k,"fixed_cohort_n_units":len(cohort),"design_k":args.design_k,
        "unobserved_design_k":[k for k in args.design_k if k>observed_max],
        "threshold_crossings":crossings,"class_summaries":class_summaries,
        "interpretation_note":"Subsample estimates are compared with the estimate from all available repeats for the same cell x condition. This measures empirical stability, not error relative to an unknown ground-truth variance.",
    }
    with (outroot/"run_manifest.json").open("w") as f:json.dump(manifest,f,indent=2)

    print("\nDesign-k summary:")
    print(ds.to_string(index=False))
    if any(k>observed_max for k in args.design_k):
        print("UNOBSERVED design k values (no extrapolation performed):",[k for k in args.design_k if k>observed_max])
    print("Threshold crossings:",crossings)
    print(f"Output: {outroot}")


if __name__=="__main__":
    main()
