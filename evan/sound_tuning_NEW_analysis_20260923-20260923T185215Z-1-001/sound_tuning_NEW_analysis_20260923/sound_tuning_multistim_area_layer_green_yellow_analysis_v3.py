#!/usr/bin/env python3
"""
GREEN-vs-YELLOW analysis across area x cortical layer for the multistim
sound_tuning FOV pipeline.

Prerequisite
------------
sound_tuning_multistim_fov_analysis_v3.py must have been run for each area.

Primary replicate
-----------------
FOV. For continuous cell metrics, cells are first summarized within
FOV x cell_class, then GREEN and YELLOW FOV summaries are paired. Preference
and tuning-profile distributions are likewise reduced to one vector per
FOV x cell_class before inferential statistics.

Layers
------
L2/3: 100 <= depth < 300 um
L4/5: 300 <= depth <= 600 um

All statistical figures print the explicit test, raw p value, correction family,
adjusted p value, and FOV sample size directly on the graph.
"""

from __future__ import annotations
import argparse, json, math, re
from pathlib import Path
from typing import Any, Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from jaratoolbox import settings

AREAS_DEFAULT=("A1","AAF","A2")
CELL_CLASSES=("green","yellow")
CLASS_COLORS={"green":"tab:green","yellow":"goldenrod"}
BLOCKS=("pure_tones","chord_tones","fm_tones")
SHORT={"pure_tones":"pure","chord_tones":"chord","fm_tones":"fm"}
BLOCK_LABEL={"pure_tones":"Pure tones","chord_tones":"3-tone chords","fm_tones":"FM sweeps"}
SELECTIVITY_SPEC={
 "pure_tones":{"metric":"pure_lifetime_sparseness","label":"Pure-tone selectivity (lifetime sparseness)","equation":r"$S_{life}=\frac{1-(\overline{|R|})^2/\overline{|R|^2}}{1-1/n}$","ylim":(-0.05,1.05),"folder":"pure_tones"},
 "chord_tones":{"metric":"chord_harmonic_selectivity","label":"Chord harmonic selectivity","equation":r"$SI_{harm}=\frac{R_{harm}-\overline{R}_{nonharm}}{|R_{harm}|+|\overline{R}_{nonharm}|}$","ylim":(-1.05,1.05),"folder":"chord_tones"},
 "fm_tones":{"metric":"fm_direction_selectivity","label":"FM direction selectivity","equation":r"$SI_{dir}=\frac{\overline{R}_{up}-\overline{R}_{down}}{|\overline{R}_{up}|+|\overline{R}_{down}|}$","ylim":(-1.05,1.05),"folder":"fm_sounds"},
}
LAYERS={"L23":(100.0,300.0,"L2/3 (100-<300 um)"),"L45":(300.0,600.000001,"L4/5 (300-600 um)")}

METRICS={
 "pure_tones":[
   ("pure_lifetime_sparseness","Lifetime sparseness"),("pure_gini_coefficient","Gini coefficient"),
   ("pure_fano_factor","Tuning-profile Fano factor"),("pure_fwhm_octaves","FWHM bandwidth (octaves)")],
 "chord_tones":[
   ("chord_lifetime_sparseness","Lifetime sparseness"),("chord_gini_coefficient","Gini coefficient"),
   ("chord_fano_factor","Tuning-profile Fano factor"),("chord_harmonic_selectivity","Harmonic-vs-nonharmonic selectivity"),
   ("chord_best_middle_distance_from_harmonic_octave","|preferred middle octave - 1|")],
 "fm_tones":[
   ("fm_lifetime_sparseness","Lifetime sparseness"),("fm_gini_coefficient","Gini coefficient"),
   ("fm_fano_factor","Tuning-profile Fano factor"),("fm_direction_selectivity","Direction selectivity (up-down)"),
   ("fm_speed_lifetime_sparseness","Speed lifetime sparseness")],
}
PREFERENCE={
 "pure_tones":("pure_best_frequency_hz","Best frequency","Hz"),
 "chord_tones":("chord_best_middle_octave","Preferred chord middle position","octaves above F0"),
 "fm_tones":("fm_best_slope_oct_per_s","Preferred FM slope","octaves/s"),
}


def parse_args():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("subject"); p.add_argument("--dates",nargs="+",required=True)
    p.add_argument("--areas",nargs="+",default=list(AREAS_DEFAULT),choices=list(AREAS_DEFAULT))
    p.add_argument("--dry-run",action="store_true")
    return p.parse_args()

def date_tag(dates): return "_".join(map(str,dates))

def input_csv(subject,area,dates):
    return Path(settings.TEMP_OUTPUT_PATH)/"evan"/"sound_tuning_multistim_fov_analysis"/subject/area/date_tag(dates)/"combined"/"combined_cell_results.csv"

def output_root(subject,dates):
    return Path(settings.TEMP_OUTPUT_PATH)/"evan"/"sound_tuning_multistim_area_layer_green_yellow_analysis"/subject/date_tag(dates)

def jsonable(x):
    if isinstance(x,dict): return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [jsonable(v) for v in x]
    if isinstance(x,(np.integer,)): return int(x)
    if isinstance(x,(np.floating,)): return None if not np.isfinite(x) else float(x)
    if isinstance(x,np.ndarray): return x.tolist()
    if isinstance(x,Path): return str(x)
    return x

def save_json(path,obj): path.write_text(json.dumps(jsonable(obj),indent=2),encoding="utf-8")

def finite(v):
    a=np.asarray(list(v) if not isinstance(v,np.ndarray) else v,float).ravel(); return a[np.isfinite(a)]

def mean_sem(v):
    a=finite(v)
    return (float(np.mean(a)),float(stats.sem(a)) if len(a)>1 else np.nan,len(a)) if len(a) else (np.nan,np.nan,0)

def holm(pv):
    p=np.asarray(list(pv),float); out=np.full_like(p,np.nan); inds=np.flatnonzero(np.isfinite(p))
    if not len(inds): return out
    vals=p[inds]; order=np.argsort(vals); r=vals[order]; a=np.maximum.accumulate((len(r)-np.arange(len(r)))*r); a=np.minimum(a,1)
    out[inds[order]]=a; return out

def ptxt(p):
    if not np.isfinite(p): return "NA"
    return f"{p:.2e}" if p<1e-3 else f"{p:.4f}"

def safe_wilcoxon(tab,a="green",b="yellow"):
    if a not in tab or b not in tab: return {"n_pairs":0,"W":np.nan,"p":np.nan}
    s=tab[[a,b]].dropna(); n=len(s)
    if n<2: return {"n_pairs":n,"W":np.nan,"p":np.nan}
    d=s[a].to_numpy(float)-s[b].to_numpy(float)
    if np.allclose(d,0): return {"n_pairs":n,"W":0.,"p":1.}
    try:
        r=stats.wilcoxon(s[a],s[b],alternative="two-sided",zero_method="wilcox")
        return {"n_pairs":n,"W":float(r.statistic),"p":float(r.pvalue)}
    except Exception: return {"n_pairs":n,"W":np.nan,"p":np.nan}

def load_tables(subject,dates,areas):
    frames=[]
    for a in areas:
        p=input_csv(subject,a,dates)
        if not p.exists():
            print(f"WARNING missing {a}: {p}"); continue
        d=pd.read_csv(p); d["canonicalArea"]=a; frames.append(d)
    if not frames: raise FileNotFoundError("No multistim area outputs found")
    d=pd.concat(frames,ignore_index=True,sort=False)
    for c in d.columns:
        if c.endswith("_responsive_fdr") or c.endswith("_excited_fdr") or c.endswith("_suppressed_fdr"):
            if d[c].dtype==object: d[c]=d[c].astype(str).str.lower().map({"true":True,"false":False})
    return d

def layer_subset(df,key):
    lo,hi,_=LAYERS[key]; x=pd.to_numeric(df.depth,errors="coerce")
    return df[(x>=lo)&(x<hi)].copy()

def fov_class_metric_table(df,metric):
    if metric not in df: return pd.DataFrame(columns=["fov_uid","cell_class","value"])
    x=df[["fov_uid","cell_class",metric]].copy(); x[metric]=pd.to_numeric(x[metric],errors="coerce")
    return x.groupby(["fov_uid","cell_class"],as_index=False)[metric].mean().rename(columns={metric:"value"})

def paired_metric_stat(df,metric):
    t=fov_class_metric_table(df,metric)
    if t.empty: return {"n_pairs":0,"W":np.nan,"p":np.nan}
    piv=t.pivot(index="fov_uid",columns="cell_class",values="value").reset_index()
    r=safe_wilcoxon(piv); r["table"]=piv; return r

def responsiveness_table(df,block):
    col=f"{SHORT[block]}_responsive_fdr"
    if col not in df: return pd.DataFrame(columns=["fov_uid","cell_class","value"])
    x=df[df[col].notna()].copy()
    if x.empty: return pd.DataFrame(columns=["fov_uid","cell_class","value"])
    x[col]=x[col].astype(float)
    t=x.groupby(["fov_uid","cell_class"],as_index=False)[col].mean(); t["value"]=100*t[col]; return t[["fov_uid","cell_class","value"]]

def condition_columns(df,block):
    if block=="pure_tones": pat=re.compile(r"^pure_response_([0-9.eE+-]+)_Hz$")
    elif block=="chord_tones": pat=re.compile(r"^chord_response_middle_oct_([0-9.eE+-]+)$")
    else: pat=re.compile(r"^fm_response_slope_(pos|neg)?([0-9.eE+]+)_oct_per_s$")
    out=[]
    for c in df.columns:
        m=pat.match(c)
        if not m: continue
        if block=="fm_tones": val=(-1 if m.group(1)=="neg" else 1)*float(m.group(2))
        else: val=float(m.group(1))
        out.append((val,c))
    return sorted(out)

def responsive_only(df,block):
    c=f"{SHORT[block]}_responsive_fdr"
    return df[df[c].fillna(False).astype(bool)].copy() if c in df else df.iloc[0:0].copy()


def _fm_log_positions(values):
    values=np.asarray(values,float); out=np.full(values.shape,np.nan,float); finite=np.isfinite(values); mags=np.sort(np.unique(np.abs(values[finite&(values!=0)])))
    if not len(mags): out[finite]=0.; return out
    lm=np.log2(mags); step=float(np.median(np.diff(lm))) if len(lm)>1 else 1.; step=step if np.isfinite(step) and step>0 else 1.
    base=step if np.any(finite&np.isclose(values,0)) else .5*step; nz=finite&(values!=0); out[nz]=np.sign(values[nz])*(base+np.log2(np.abs(values[nz])/mags[0])); out[finite&np.isclose(values,0)]=0.; return out

def _condition_x(block,vals):
    vals=np.asarray(vals,float)
    if block=="pure_tones": return np.log2(vals/1000.0)
    if block=="fm_tones": return _fm_log_positions(vals)
    return vals

def _selectivity_equation_box(ax,block):
    ax.text(.02,.03,SELECTIVITY_SPEC[block]["equation"],transform=ax.transAxes,ha="left",va="bottom",fontsize=9.3,bbox=dict(boxstyle="round,pad=.32",facecolor="white",edgecolor=".75",alpha=.95))

def stats_text(rec,ph,label="paired FOV Wilcoxon"):
    return f"{label}\nW={rec.get('W',np.nan):.3g}; p={ptxt(rec.get('p',np.nan))}\nHolm p={ptxt(ph)}; n={rec.get('n_pairs',0)} pairs"


def plot_responsiveness(df,area,layer_label,out):
    fig,axes=plt.subplots(1,3,figsize=(15,5)); recs=[]
    for ax,b in zip(axes,BLOCKS):
        t=responsiveness_table(df,b); piv=t.pivot(index="fov_uid",columns="cell_class",values="value").reset_index() if len(t) else pd.DataFrame()
        r=safe_wilcoxon(piv); recs.append((ax,b,r,piv))
        if len(piv):
            for _,rr in piv.iterrows():
                if "green" in rr and "yellow" in rr and np.isfinite(rr.get("green",np.nan)) and np.isfinite(rr.get("yellow",np.nan)):
                    ax.plot([0,1],[rr.green,rr.yellow],color=".75",lw=.8)
            for x,cls in enumerate(CELL_CLASSES):
                v=finite(piv[cls]) if cls in piv else np.array([]); ax.scatter(np.full(len(v),x),v,s=28,facecolors=CLASS_COLORS[cls],edgecolors="none")
                mu,se,n=mean_sem(v); ax.errorbar(x,mu,yerr=se,fmt="o",color="black",capsize=4)
        ax.set_xticks([0,1]); ax.set_xticklabels(["GREEN","YELLOW"]); ax.set_ylim(0,100); ax.set_title(BLOCK_LABEL[b]); ax.set_ylabel("Responsive cells (%)")
    adj=holm([r["p"] for _,_,r,_ in recs]); statsout={}
    for (ax,b,r,_),ph in zip(recs,adj):
        r["p_holm_3_blocks"]=ph; statsout[b]=r; ax.text(.02,.98,stats_text(r,ph),transform=ax.transAxes,va="top",fontsize=8)
    fig.suptitle(f"{area} {layer_label}: sound-responsive fraction — GREEN vs YELLOW"); fig.tight_layout(rect=[0,0,1,.93])
    fig.savefig(out/"responsiveness_GREEN_vs_YELLOW_FOV_POINTS.png",dpi=250); plt.close(fig)
    return statsout


def plot_metric_family(df,block,area,layer_label,out,branch):
    use=df if branch=="all_cells" else responsive_only(df,block)
    avail=[(m,l) for m,l in METRICS[block] if m in use and np.any(np.isfinite(pd.to_numeric(use[m],errors="coerce")))]
    if not avail: return {}
    n=len(avail); ncol=min(3,n); nrow=int(math.ceil(n/ncol)); fig,axes=plt.subplots(nrow,ncol,figsize=(5*ncol,4.8*nrow),squeeze=False)
    recs=[]
    for ax,(m,label) in zip(axes.ravel(),avail):
        t=fov_class_metric_table(use,m); piv=t.pivot(index="fov_uid",columns="cell_class",values="value").reset_index(); r=safe_wilcoxon(piv); recs.append((ax,m,label,r,piv))
        for _,rr in piv.iterrows():
            if np.isfinite(rr.get("green",np.nan)) and np.isfinite(rr.get("yellow",np.nan)): ax.plot([0,1],[rr.green,rr.yellow],color=".78",lw=.8)
        for x,cls in enumerate(CELL_CLASSES):
            v=finite(piv[cls]) if cls in piv else np.array([]); ax.scatter(np.full(len(v),x),v,s=25,facecolors=CLASS_COLORS[cls],edgecolors="none"); mu,se,nn=mean_sem(v); ax.errorbar(x,mu,yerr=se,fmt="o",color="black",capsize=3)
        ax.set_xticks([0,1]); ax.set_xticklabels(["GREEN","YELLOW"]); ax.set_ylabel(label); ax.set_title(label)
        if "selectivity" in m: ax.axhline(0,color=".5",ls="--",lw=1)
    for ax in axes.ravel()[len(avail):]: ax.axis("off")
    adj=holm([r["p"] for _,_,_,r,_ in recs]); outstats={}
    for (ax,m,label,r,piv),ph in zip(recs,adj):
        r["p_holm_metric_family"]=ph; outstats[m]=r; ax.text(.02,.98,stats_text(r,ph,f"paired FOV Wilcoxon; Holm({len(avail)})"),transform=ax.transAxes,va="top",fontsize=7.5)
    fig.suptitle(f"{area} {layer_label}: {BLOCK_LABEL[block]} selectivity — {branch.replace('_',' ')}"); fig.tight_layout(rect=[0,0,1,.95])
    fig.savefig(out/f"{block}_selectivity_{branch}_GREEN_YELLOW_SESSION_POINTS.png",dpi=250); plt.close(fig)
    return outstats


def profile_fov_table(df,cols):
    rows=[]
    for (uid,cls),g in df.groupby(["fov_uid","cell_class"]):
        row={"fov_uid":uid,"cell_class":cls}
        for val,col in cols: row[col]=float(np.nanmean(pd.to_numeric(g[col],errors="coerce"))) if np.any(np.isfinite(pd.to_numeric(g[col],errors="coerce"))) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)

def plot_profile(df,block,area,layer_label,out,branch):
    use=df if branch=="all_cells" else responsive_only(df,block); cols=condition_columns(use,block)
    if not cols: return {}
    t=profile_fov_table(use,cols); vals=np.array([v for v,_ in cols]); x=_condition_x(block,vals)
    fig,ax=plt.subplots(figsize=(10.5,6.0)); stats_rows=[]
    for cls in CELL_CLASSES:
        s=t[t.cell_class==cls]; M=s[[c for _,c in cols]].to_numpy(float) if len(s) else np.empty((0,len(cols)))
        if len(M):
            for row in M: ax.plot(x,row,color=CLASS_COLORS[cls],alpha=.16,lw=.8)
            mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy="omit"); ax.plot(x,mu,marker="o",lw=2.2,color=CLASS_COLORS[cls],label=f"{cls.upper()} nFOV={len(M)}"); ax.fill_between(x,mu-se,mu+se,color=CLASS_COLORS[cls],alpha=.15)
    p=[]
    for val,col in cols:
        piv=t.pivot(index="fov_uid",columns="cell_class",values=col).reset_index(); r=safe_wilcoxon(piv); p.append(r["p"]); stats_rows.append((val,r))
    adj=holm(p); statdict={}
    for (val,r),ph in zip(stats_rows,adj): r["p_holm_across_conditions"]=ph; statdict[str(val)]=r
    sig=[(val,ph) for (val,_),ph in zip(stats_rows,adj) if np.isfinite(ph) and ph<.05]
    if sig:
        ymin,ymax=ax.get_ylim(); y=ymax-(ymax-ymin)*.05
        for val,ph in sig:
            xx=np.log2(val/1000) if block=="pure_tones" else val; ax.text(xx,y,"*",ha="center",va="top",fontsize=15)
    lines=[f"Per-condition paired FOV Wilcoxon; Holm across {len(cols)} conditions"]+[f"{v:g}: p={ptxt(r['p'])}, Holm={ptxt(r.get('p_holm_across_conditions',np.nan))}, n={r['n_pairs']}" for v,r in stats_rows]
    ax.text(1.02,.98,"\n".join(lines),transform=ax.transAxes,va="top",fontsize=7.2)
    ax.axhline(0,color=".5",ls="--",lw=1); ax.set_ylabel("Mean cell response per FOV (dF/F)"); ax.legend(frameon=False)
    if block=="pure_tones": _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel("Frequency (kHz; log2 spacing)")
    elif block=="chord_tones": ax.set_xlabel("Middle tone position (octaves above F0)")
    else: _readable_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel("FM slope (octaves/s; signed log2-magnitude spacing)")
    ax.set_title(f"{area} {layer_label}: {BLOCK_LABEL[block]} — {branch.replace('_',' ')}")
    fig.subplots_adjust(right=.72); fig.savefig(out/f"{block}_profile_{branch}_GREEN_YELLOW_FOV_MEANS.png",dpi=250,bbox_inches="tight"); plt.close(fig)
    return statdict


def preference_distribution(df,block,responsive=True):
    metric,_,_=PREFERENCE[block]
    if metric not in df: return pd.DataFrame(),[]
    use=responsive_only(df,block) if responsive else df[df[metric].notna()].copy()
    if use.empty: return pd.DataFrame(),[]
    values=np.sort(use[metric].dropna().unique())
    rows=[]
    for (uid,cls),g in use.groupby(["fov_uid","cell_class"]):
        arr=pd.to_numeric(g[metric],errors="coerce").to_numpy(float); arr=arr[np.isfinite(arr)]
        for v in values:
            rows.append({"fov_uid":uid,"cell_class":cls,"value":v,"percent":100*np.mean(np.isclose(arr,v)) if len(arr) else np.nan})
    return pd.DataFrame(rows),values.tolist()

def plot_preference_distribution(df,block,area,layer_label,out,responsive=True):
    tab,vals=preference_distribution(df,block,responsive); metric,label,unit=PREFERENCE[block]
    if tab.empty: return {}
    x=_condition_x(block,np.asarray(vals,float))
    fig,ax=plt.subplots(figsize=(10.5,6)); statrows=[]
    for cls in CELL_CLASSES:
        means=[]; ses=[]
        for v in vals:
            a=tab[(tab.cell_class==cls)&np.isclose(tab.value,v)].percent; mu,se,n=mean_sem(a); means.append(mu); ses.append(se)
        ax.errorbar(x,means,yerr=ses,marker="o",lw=2,color=CLASS_COLORS[cls],capsize=3,label=cls.upper())
    ps=[]
    for v in vals:
        s=tab[np.isclose(tab.value,v)].pivot(index="fov_uid",columns="cell_class",values="percent").reset_index(); r=safe_wilcoxon(s); ps.append(r["p"]); statrows.append((v,r))
    adj=holm(ps); outstats={}
    for (v,r),ph in zip(statrows,adj): r["p_holm_bins"]=ph; outstats[str(v)]=r
    lines=[f"Each point = % cells/FOV; paired GREEN-YELLOW Wilcoxon; Holm({len(vals)} bins)"]+[f"{v:g}: p={ptxt(r['p'])}, Holm={ptxt(r.get('p_holm_bins',np.nan))}, n={r['n_pairs']}" for v,r in statrows]
    ax.text(1.02,.98,"\n".join(lines),transform=ax.transAxes,va="top",fontsize=7.2); ax.set_ylabel("Cells preferring condition (%)"); ax.legend(frameon=False)
    if block=="pure_tones": _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel("Best frequency (kHz; log2 spacing)")
    elif block=='fm_tones': _readable_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel(f"{label} ({unit}; signed log2-magnitude spacing)")
    else: ax.set_xlabel(f"{label} ({unit})")
    ax.set_title(f"{area} {layer_label}: {label} distribution — {'FDR responsive only' if responsive else 'all cells descriptive'}")
    fig.subplots_adjust(right=.72); fig.savefig(out/f"{block}_preference_distribution_{'responsive' if responsive else 'all_cells'}_GREEN_YELLOW.png",dpi=250,bbox_inches="tight"); plt.close(fig)
    return outstats



def _readable_ticks(ax,x,labels,dense_threshold=10):
    x=np.asarray(x,float); labels=list(labels); ax.set_xticks(x)
    if len(labels)>=dense_threshold:
        ax.set_xticklabels([lab if i%2==0 else "" for i,lab in enumerate(labels)],rotation=60,ha="right",rotation_mode="anchor")
    else:
        ax.set_xticklabels(labels,rotation=45 if len(labels)>6 else 0,ha="right" if len(labels)>6 else "center")

def _mw_green_yellow(df,metric):
    g=pd.to_numeric(df.loc[df.cell_class=="green",metric],errors="coerce").dropna().to_numpy(float) if metric in df else np.array([])
    y=pd.to_numeric(df.loc[df.cell_class=="yellow",metric],errors="coerce").dropna().to_numpy(float) if metric in df else np.array([])
    if not len(g) or not len(y): return {"U":np.nan,"p":np.nan,"n_green":len(g),"n_yellow":len(y)}
    r=stats.mannwhitneyu(g,y,alternative="two-sided"); return {"U":float(r.statistic),"p":float(r.pvalue),"n_green":len(g),"n_yellow":len(y)}

def plot_cell_metric_family(df,block,area,layer_label,out,branch):
    use=df if branch=="all_cells" else responsive_only(df,block)
    avail=[(m,l) for m,l in METRICS[block] if m in use and np.any(np.isfinite(pd.to_numeric(use[m],errors="coerce")))]
    if not avail:return {}
    n=len(avail); nc=min(3,n); nr=int(math.ceil(n/nc)); fig,axes=plt.subplots(nr,nc,figsize=(5*nc,4.8*nr),squeeze=False); recs=[]; rng=np.random.default_rng(8841)
    for ax,(m,label) in zip(axes.ravel(),avail):
        r=_mw_green_yellow(use,m); recs.append((ax,m,r))
        for pos,cls in enumerate(CELL_CLASSES):
            z=pd.to_numeric(use.loc[use.cell_class==cls,m],errors="coerce").dropna().to_numpy(float)
            if len(z): ax.scatter(np.full(len(z),pos)+rng.uniform(-.09,.09,len(z)),z,s=13,alpha=.26,facecolors=CLASS_COLORS[cls],edgecolors="none")
            mu,se,nn=mean_sem(z); ax.errorbar(pos,mu,yerr=se,fmt='o',color='black',capsize=3,zorder=4)
        ax.set_xticks([0,1]); ax.set_xticklabels(['GREEN','YELLOW']); ax.set_ylabel(label); ax.set_title(label)
        if 'selectivity' in m: ax.axhline(0,color='.5',ls='--',lw=.8)
    for ax in axes.ravel()[len(avail):]:ax.axis('off')
    adj=holm([r['p'] for _,_,r in recs]); outstats={}
    for (ax,m,r),ph in zip(recs,adj):
        r['p_holm_metric_family']=ph; outstats[m]=r; ax.text(.02,.98,f"EXPLORATORY pooled cells\nMann-Whitney U={r['U']:.3g}, p={ptxt(r['p'])}\nHolm={ptxt(ph)}; nG/nY={r['n_green']}/{r['n_yellow']}",transform=ax.transAxes,va='top',fontsize=7.2)
    fig.suptitle(f"{area} {layer_label}: {BLOCK_LABEL[block]} — {branch.replace('_',' ')} — individual cells"); fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(out/f"{block}_selectivity_{branch}_GREEN_YELLOW_CELL_POINTS.png",dpi=250); plt.close(fig); return outstats

def plot_primary_selectivity_fov(df,block,area,layer_label,out,branch,statrec=None):
    spec=SELECTIVITY_SPEC[block]; metric=spec["metric"]; use=df if branch=="all_cells" else responsive_only(df,block)
    if metric not in use or not np.any(np.isfinite(pd.to_numeric(use[metric],errors="coerce"))): return
    t=fov_class_metric_table(use,metric); piv=t.pivot(index="fov_uid",columns="cell_class",values="value").reset_index() if len(t) else pd.DataFrame()
    r=statrec if statrec is not None else safe_wilcoxon(piv); root=out/"selectivity_plots"/spec["folder"]; root.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(6.6,5.8))
    if len(piv):
        for _,rr in piv.iterrows():
            if np.isfinite(rr.get("green",np.nan)) and np.isfinite(rr.get("yellow",np.nan)): ax.plot([0,1],[rr.green,rr.yellow],color=".78",lw=.85)
        for pos,cls in enumerate(CELL_CLASSES):
            z=finite(piv[cls]) if cls in piv else np.array([]); ax.scatter(np.full(len(z),pos),z,s=30,facecolors=CLASS_COLORS[cls],edgecolors="none"); mu,se,n=mean_sem(z); ax.errorbar(pos,mu,yerr=se,fmt="o",color="black",capsize=4)
    ax.set_xticks([0,1]); ax.set_xticklabels(["GREEN","YELLOW"]); ax.set_ylabel(spec["label"]); ax.set_ylim(*spec["ylim"]);
    if spec["ylim"][0]<0: ax.axhline(0,color=".55",ls="--",lw=.8)
    ph=r.get("p_holm_metric_family",np.nan); ax.text(.98,.98,f"paired FOV Wilcoxon\nW={r.get('W',np.nan):.3g}, p={ptxt(r.get('p',np.nan))}\nmetric-family Holm={ptxt(ph)}\nn={r.get('n_pairs',0)} pairs",transform=ax.transAxes,ha="right",va="top",fontsize=8.3)
    _selectivity_equation_box(ax,block); ax.set_title(f"{area} {layer_label}: {BLOCK_LABEL[block]}\n{branch.replace('_',' ')} — primary FOV selectivity"); fig.tight_layout(); fig.savefig(root/f"{branch}_GREEN_YELLOW_FOV_primary_selectivity.png",dpi=250); plt.close(fig)

def plot_primary_selectivity_cells(df,block,area,layer_label,out,branch,statrec=None):
    spec=SELECTIVITY_SPEC[block]; metric=spec["metric"]; use=df if branch=="all_cells" else responsive_only(df,block)
    if metric not in use or not np.any(np.isfinite(pd.to_numeric(use[metric],errors="coerce"))): return
    r=statrec if statrec is not None else _mw_green_yellow(use,metric); root=out/"selectivity_plots"/spec["folder"]; root.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(9017)
    fig,ax=plt.subplots(figsize=(6.6,5.8))
    for pos,cls in enumerate(CELL_CLASSES):
        z=pd.to_numeric(use.loc[use.cell_class==cls,metric],errors="coerce").dropna().to_numpy(float)
        if len(z): ax.scatter(np.full(len(z),pos)+rng.uniform(-.08,.08,len(z)),z,s=14,alpha=.28,facecolors=CLASS_COLORS[cls],edgecolors="none")
        mu,se,n=mean_sem(z); ax.errorbar(pos,mu,yerr=se,fmt="o",color="black",capsize=4,zorder=4)
    ax.set_xticks([0,1]); ax.set_xticklabels(["GREEN","YELLOW"]); ax.set_ylabel(spec["label"]); ax.set_ylim(*spec["ylim"]);
    if spec["ylim"][0]<0: ax.axhline(0,color=".55",ls="--",lw=.8)
    ph=r.get("p_holm_metric_family",np.nan); ax.text(.98,.98,f"EXPLORATORY pooled cells\nMann-Whitney U={r.get('U',np.nan):.3g}, p={ptxt(r.get('p',np.nan))}\nmetric-family Holm={ptxt(ph)}\nnG/nY={r.get('n_green',0)}/{r.get('n_yellow',0)}",transform=ax.transAxes,ha="right",va="top",fontsize=8.3)
    _selectivity_equation_box(ax,block); ax.set_title(f"{area} {layer_label}: {BLOCK_LABEL[block]}\n{branch.replace('_',' ')} — cell-level selectivity"); fig.tight_layout(); fig.savefig(root/f"{branch}_GREEN_YELLOW_CELL_exploratory_selectivity.png",dpi=250); plt.close(fig)

def plot_cell_profiles(df,block,area,layer_label,out,branch):
    use=df if branch=='all_cells' else responsive_only(df,block); cols=condition_columns(use,block)
    if not cols:return
    vals=np.array([v for v,_ in cols]); x=_condition_x(block,vals); fig,axes=plt.subplots(1,2,figsize=(13,5.3),sharey=True)
    for ax,cls in zip(axes,CELL_CLASSES):
        M=use.loc[use.cell_class==cls,[c for _,c in cols]].apply(pd.to_numeric,errors='coerce').to_numpy(float)
        if len(M):
            for row in M: ax.plot(x,row,color=CLASS_COLORS[cls],alpha=.08,lw=.55)
            mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy='omit'); ax.plot(x,mu,color=CLASS_COLORS[cls],marker='o',lw=2.2); ax.fill_between(x,mu-se,mu+se,color=CLASS_COLORS[cls],alpha=.18)
        ax.axhline(0,color='.5',ls='--',lw=.8); ax.set_title(f"{cls.upper()} | n={len(M)} cells"); ax.set_ylabel('Cell response (dF/F)')
        if block=='pure_tones': _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel('Frequency (kHz; log2 spacing)')
        elif block=='chord_tones': _readable_ticks(ax,x,[f"{v:.3g}" for v in vals]); ax.set_xlabel('Middle tone position (octaves above F0)')
        else: _readable_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel('FM slope (octaves/s; signed log2-magnitude spacing)')
    fig.suptitle(f"{area} {layer_label}: {BLOCK_LABEL[block]} — {branch.replace('_',' ')} — individual-cell profiles"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(out/f"{block}_profile_{branch}_GREEN_YELLOW_CELL_PROFILES.png",dpi=250); plt.close(fig)

def plot_rasters(df,block,area,layer_label,out):
    cols=condition_columns(df,block)
    if not cols:return
    vals=np.array([v for v,_ in cols]); labels=[f"{v/1000:g}" for v in vals] if block=='pure_tones' else [f"{v:g}" for v in vals]
    for branch in ('all_cells','responsive_only'):
        use=df if branch=='all_cells' else responsive_only(df,block)
        for sort_metric,suffix in ((f"{SHORT[block]}_preferred_condition",'PREFERRED'),(f"{SHORT[block]}_lifetime_sparseness",'SPARSENESS')):
            if sort_metric not in use or use.empty:continue
            fig,axes=plt.subplots(1,2,figsize=(13,6),squeeze=False)
            for ax,cls in zip(axes[0],CELL_CLASSES):
                g=use[use.cell_class==cls].copy(); g['_sort']=pd.to_numeric(g[sort_metric],errors='coerce'); g=g.sort_values('_sort'); M=g[[c for _,c in cols]].apply(pd.to_numeric,errors='coerce').to_numpy(float)
                if len(M):
                    scale=np.nanmax(np.abs(M),axis=1); scale[~np.isfinite(scale)|(scale==0)]=1; N=M/scale[:,None]; im=ax.imshow(N,aspect='auto',interpolation='nearest',cmap='coolwarm',vmin=-1,vmax=1)
                ax.set_title(f"{cls.upper()} n={len(g)}"); ax.set_xlabel('Stimulus condition'); ax.set_ylabel(f"Cells sorted by {suffix.lower()}"); ax.set_xticks(np.arange(len(vals))); ax.set_xticklabels([lab if i%2==0 or len(labels)<10 else '' for i,lab in enumerate(labels)],rotation=60,ha='right')
            fig.suptitle(f"{area} {layer_label}: {BLOCK_LABEL[block]} raster — {branch.replace('_',' ')} — sorted by {suffix.lower()}"); fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(out/f"{block}_raster_{branch}_{suffix}.png",dpi=250); plt.close(fig)

def plot_bf_outputs(df,area,layer_label,out):
    if 'pure_best_frequency_hz' not in df or 'pure_responsive_fdr' not in df:return {}
    use=df[df.pure_responsive_fdr.fillna(False).astype(bool)&pd.to_numeric(df.pure_best_frequency_hz,errors='coerce').notna()].copy()
    if use.empty:return {}
    root=out/'best_frequency'; root.mkdir(exist_ok=True)
    vals=np.sort(pd.to_numeric(use.pure_best_frequency_hz,errors='coerce').dropna().unique()); x=np.log2(vals/1000)
    fig,ax=plt.subplots(figsize=(10,5.5))
    for cls in CELL_CLASSES:
        arr=pd.to_numeric(use.loc[use.cell_class==cls,'pure_best_frequency_hz'],errors='coerce').dropna().to_numpy(float); frac=np.array([np.mean(np.isclose(arr,v)) if len(arr) else np.nan for v in vals]); ax.plot(x,frac,marker='o',lw=2,color=CLASS_COLORS[cls],label=f"{cls.upper()} n={len(arr)}")
    _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel('Best frequency (kHz; log2 spacing)'); ax.set_ylabel('Fraction of responsive cells'); ax.legend(frameon=False); ax.set_title(f"{area} {layer_label}: pooled BF distribution (descriptive)"); fig.tight_layout(); fig.savefig(root/'BF_pooled_fraction_GREEN_YELLOW.png',dpi=250); plt.close(fig)
    # FOV-level BF histograms and paired median BF summary
    rows=[]
    for (uid,cls),g in use.groupby(['fov_uid','cell_class']):
        arr=pd.to_numeric(g.pure_best_frequency_hz,errors='coerce').dropna().to_numpy(float);
        if len(arr):
            rec={'fov_uid':uid,'cell_class':cls,'median_log2_bf':float(np.median(np.log2(arr))),'n_cells':len(arr)}
            for v in vals:rec[str(v)]=float(np.mean(np.isclose(arr,v)))
            rows.append(rec)
    tab=pd.DataFrame(rows); tab.to_csv(root/'BF_FOV_distributions.csv',index=False)
    if not tab.empty:
        fig,axes=plt.subplots(1,2,figsize=(13,5.5)); rng=np.random.default_rng(887)
        piv=tab.pivot(index='fov_uid',columns='cell_class',values='median_log2_bf').reset_index(); r=safe_wilcoxon(piv);
        for _,rr in piv.iterrows():
            if np.isfinite(rr.get('green',np.nan)) and np.isfinite(rr.get('yellow',np.nan)): axes[0].plot([0,1],[rr.green,rr.yellow],color='.78',lw=.8)
        for pos,cls in enumerate(CELL_CLASSES):
            z=finite(piv[cls]) if cls in piv else np.array([]); ns=tab.loc[tab.cell_class==cls,'n_cells'].to_numpy(float); axes[0].scatter(np.full(len(z),pos)+rng.uniform(-.04,.04,len(z)),z,s=35+6*np.sqrt(ns[:len(z)]),facecolors=CLASS_COLORS[cls],edgecolors='none'); mu,se,n=mean_sem(z); axes[0].errorbar(pos,mu,yerr=se,fmt='o',color='black',capsize=3)
        axes[0].set_xticks([0,1]); axes[0].set_xticklabels(['GREEN','YELLOW']); axes[0].set_ylabel('FOV median log2(BF [Hz])'); axes[0].set_title(f"paired FOV Wilcoxon W={r['W']:.3g}, p={ptxt(r['p'])}, n={r['n_pairs']}")
        # heatmap all fov/class rows
        cols=[str(v) for v in vals]; M=tab[cols].to_numpy(float); im=axes[1].imshow(M,aspect='auto',cmap='viridis',vmin=0,vmax=np.nanmax(M) if np.nanmax(M)>0 else 1); axes[1].set_yticks(range(len(tab))); axes[1].set_yticklabels([f"{u} {c}" for u,c in zip(tab.fov_uid,tab.cell_class)]); axes[1].set_xticks(range(len(vals))); axes[1].set_xticklabels([f"{v/1000:g}" if i%2==0 else '' for i,v in enumerate(vals)],rotation=60,ha='right'); axes[1].set_xlabel('BF (kHz)'); axes[1].set_title('Fraction per FOV'); fig.colorbar(im,ax=axes[1],label='Fraction')
        fig.suptitle(f"{area} {layer_label}: pure-tone BF across FOVs"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(root/'BF_FOV_comparison.png',dpi=250); plt.close(fig)
    return {'n_fov_rows':len(tab)}


def write_index(out):
    (out/"FIGURE_INDEX.txt").write_text("\n".join(str(p.relative_to(out)) for p in sorted(out.rglob("*.png")))+"\n",encoding="utf-8")


def main():
    args=parse_args(); subject=str(args.subject); dates=[str(d) for d in args.dates]; areas=list(args.areas)
    root=output_root(subject,dates)
    print("="*80); print("MULTISTIM AREA x LAYER GREEN/YELLOW ANALYSIS v3"); print("="*80)
    for a in areas: print(a,input_csv(subject,a,dates),"FOUND" if input_csv(subject,a,dates).exists() else "MISSING")
    if args.dry_run: return
    root.mkdir(parents=True,exist_ok=True); cells=load_tables(subject,dates,areas); cells.to_csv(root/"all_areas_input_cells.csv",index=False)
    master={}
    for area in areas:
        adf=cells[cells.canonicalArea==area]
        if adf.empty: continue
        for layer_key,(_,_,layer_label) in LAYERS.items():
            df=layer_subset(adf,layer_key); out=root/area/layer_key; out.mkdir(parents=True,exist_ok=True)
            if df.empty: continue
            statsout={"responsiveness":plot_responsiveness(df,area,layer_label,out),"metrics":{},"profiles":{},"preferences":{}}
            for b in BLOCKS:
                statsout["metrics"][b]={}
                for branch in ("all_cells","responsive_only"):
                    statsout["metrics"][b][branch]=plot_metric_family(df,b,area,layer_label,out,branch)
                    statsout["metrics"][b][branch+"_pooled_cells_exploratory"]=plot_cell_metric_family(df,b,area,layer_label,out,branch)
                    smetric=SELECTIVITY_SPEC[b]["metric"]
                    plot_primary_selectivity_fov(df,b,area,layer_label,out,branch,statsout["metrics"][b][branch].get(smetric))
                    plot_primary_selectivity_cells(df,b,area,layer_label,out,branch,statsout["metrics"][b][branch+"_pooled_cells_exploratory"].get(smetric))
                    statsout["profiles"].setdefault(b,{})[branch]=plot_profile(df,b,area,layer_label,out,branch)
                    plot_cell_profiles(df,b,area,layer_label,out,branch)
                plot_rasters(df,b,area,layer_label,out)
                statsout["preferences"][b]={
                    "responsive_only":plot_preference_distribution(df,b,area,layer_label,out,True),
                    "all_cells_descriptive":plot_preference_distribution(df,b,area,layer_label,out,False)}
            statsout["best_frequency"]=plot_bf_outputs(df,area,layer_label,out)
            save_json(out/"statistics.json",statsout); write_index(out); master[f"{area}_{layer_key}"]=statsout
    save_json(root/"MASTER_STATISTICS.json",master)
    print(f"DONE: {root}")

if __name__=="__main__": main()
