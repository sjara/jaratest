#!/usr/bin/env python3
"""
Cross-area analysis of pure-tone, chord, and FM responses from the FOV-aware
sound_tuning multistim pipeline.

Prerequisite: sound_tuning_multistim_fov_analysis_v3.py for A1/AAF/A2.

GREEN and YELLOW are analyzed separately. Primary inference uses one summary per
FOV. Cross-area omnibus tests are Kruskal-Wallis; all A1/AAF/A2 pairwise tests
are two-sided Mann-Whitney U with Holm correction across the three area pairs.
Families of related omnibus tests are also Holm corrected. Pooled-cell outputs,
where present, are explicitly exploratory.

Depth strata:
  all_depths
  L23_100to300um   : 100 <= depth < 300
  L45_300to600um   : 300 <= depth <= 600

A YELLOW trial-reduction robustness branch is included for individually
significant primary cross-area results. It subsamples trials without replacement
within FOV x sound-block x stimulus condition at 100/75/50/25%, recomputes the
condition-specific response/FDR/selectivity results, and re-runs the exact test
identified on each robustness figure. This is an empirical stability analysis,
not prospective power.
"""

from __future__ import annotations
import argparse, json, math, re, hashlib
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
AREA_COLORS={"A1":"tab:blue","AAF":"tab:orange","A2":"tab:purple"}
BLOCKS=("pure_tones","chord_tones","fm_tones")
SHORT={"pure_tones":"pure","chord_tones":"chord","fm_tones":"fm"}
BLOCK_LABEL={"pure_tones":"Pure tones","chord_tones":"3-tone chords","fm_tones":"FM sweeps"}
SELECTIVITY_SPEC={
 "pure_tones":{"metric":"pure_lifetime_sparseness","label":"Pure-tone selectivity (lifetime sparseness)","equation":r"$S_{life}=\frac{1-(\overline{|R|})^2/\overline{|R|^2}}{1-1/n}$","ylim":(-0.05,1.05),"folder":"pure_tones"},
 "chord_tones":{"metric":"chord_harmonic_selectivity","label":"Chord harmonic selectivity","equation":r"$SI_{harm}=\frac{R_{harm}-\overline{R}_{nonharm}}{|R_{harm}|+|\overline{R}_{nonharm}|}$","ylim":(-1.05,1.05),"folder":"chord_tones"},
 "fm_tones":{"metric":"fm_direction_selectivity","label":"FM direction selectivity","equation":r"$SI_{dir}=\frac{\overline{R}_{up}-\overline{R}_{down}}{|\overline{R}_{up}|+|\overline{R}_{down}|}$","ylim":(-1.05,1.05),"folder":"fm_sounds"},
}
DEPTHS={"all_depths":(-np.inf,np.inf,"All depths"),"L23_100to300um":(100.,300.,"L2/3 (100-<300 um)"),"L45_300to600um":(300.,600.000001,"L4/5 (300-600 um)")}
TRIAL_FRACTIONS=(1.0,.75,.50,.25)
METRICS={
 "pure_tones":[("pure_lifetime_sparseness","Lifetime sparseness"),("pure_gini_coefficient","Gini coefficient"),("pure_fano_factor","Tuning-profile Fano factor"),("pure_fwhm_octaves","FWHM bandwidth (octaves)")],
 "chord_tones":[("chord_lifetime_sparseness","Lifetime sparseness"),("chord_gini_coefficient","Gini coefficient"),("chord_fano_factor","Tuning-profile Fano factor"),("chord_harmonic_selectivity","Harmonic selectivity"),("chord_best_middle_distance_from_harmonic_octave","|preferred middle octave - 1|")],
 "fm_tones":[("fm_lifetime_sparseness","Lifetime sparseness"),("fm_gini_coefficient","Gini coefficient"),("fm_fano_factor","Tuning-profile Fano factor"),("fm_direction_selectivity","Direction selectivity"),("fm_speed_lifetime_sparseness","Speed lifetime sparseness")],
}
PREF={"pure_tones":("pure_best_frequency_hz","Best frequency"),"chord_tones":("chord_best_middle_octave","Preferred chord middle octave"),"fm_tones":("fm_best_slope_oct_per_s","Preferred FM slope")}


def parse_args():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("subject"); p.add_argument("--dates",nargs="+",required=True); p.add_argument("--areas",nargs="+",default=list(AREAS_DEFAULT),choices=list(AREAS_DEFAULT))
 p.add_argument("--trial-reduction-resamples",type=int,default=500); p.add_argument("--trial-reduction-response-permutations",type=int,default=512); p.add_argument("--trial-reduction-seed",type=int,default=20260910)
 p.add_argument("--skip-trial-reduction",action="store_true"); p.add_argument("--dry-run",action="store_true"); return p.parse_args()
def tag(d): return "_".join(map(str,d))
def input_csv(subject,area,dates): return Path(settings.TEMP_OUTPUT_PATH)/"evan"/"sound_tuning_multistim_fov_analysis"/subject/area/tag(dates)/"combined"/"combined_cell_results.csv"
def output_root(subject,dates): return Path(settings.TEMP_OUTPUT_PATH)/"evan"/"sound_tuning_multistim_cross_area_cellclass_analysis"/subject/tag(dates)
def jsonable(x):
 if isinstance(x,dict): return {str(k):jsonable(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)): return [jsonable(v) for v in x]
 if isinstance(x,(np.integer,)): return int(x)
 if isinstance(x,(np.floating,)): return None if not np.isfinite(x) else float(x)
 if isinstance(x,np.ndarray): return x.tolist()
 if isinstance(x,Path): return str(x)
 return x
def save_json(p,o): p.write_text(json.dumps(jsonable(o),indent=2),encoding="utf-8")
def finite(v):
 a=np.asarray(list(v) if not isinstance(v,np.ndarray) else v,float).ravel(); return a[np.isfinite(a)]
def mean_sem(v):
 a=finite(v); return (float(np.mean(a)),float(stats.sem(a)) if len(a)>1 else np.nan,len(a)) if len(a) else (np.nan,np.nan,0)
def holm(pv):
 p=np.asarray(list(pv),float); out=np.full_like(p,np.nan); idx=np.flatnonzero(np.isfinite(p))
 if not len(idx): return out
 vals=p[idx]; o=np.argsort(vals); r=vals[o]; a=np.maximum.accumulate((len(r)-np.arange(len(r)))*r); a=np.minimum(a,1); out[idx[o]]=a; return out
def ptxt(p): return "NA" if not np.isfinite(p) else (f"{p:.2e}" if p<1e-3 else f"{p:.4f}")
def cliffs_delta(x,y):
 x=finite(x); y=finite(y)
 if not len(x) or not len(y): return np.nan
 return float((np.sum(x[:,None]>y[None,:])-np.sum(x[:,None]<y[None,:]))/(len(x)*len(y)))
def mw(x,y):
 x=finite(x); y=finite(y)
 if not len(x) or not len(y): return {"n1":len(x),"n2":len(y),"U":np.nan,"p":np.nan,"cliffs_delta":np.nan}
 r=stats.mannwhitneyu(x,y,alternative="two-sided"); return {"n1":len(x),"n2":len(y),"U":float(r.statistic),"p":float(r.pvalue),"cliffs_delta":cliffs_delta(x,y)}
def kw(groups):
 g={k:finite(v) for k,v in groups.items()}; good=[v for v in g.values() if len(v)]
 if len(good)<2: return {"H":np.nan,"p":np.nan,"n_by_area":{k:len(v) for k,v in g.items()}}
 try:
  r=stats.kruskal(*good); H=float(r.statistic); pv=float(r.pvalue)
  if not np.isfinite(H) or not np.isfinite(pv): H,pv=0.0,1.0
 except ValueError:
  H,pv=0.0,1.0
 return {"H":H,"p":pv,"n_by_area":{k:len(v) for k,v in g.items()}}
def cross_stats(groups,areas):
 areas=list(areas)
 g={a:finite(groups.get(a,[])) for a in areas}
 if len(areas)==2:
  a,b=areas
  r=mw(g[a],g[b]); r.update({"area1":a,"area2":b})
  primary={"test":"Mann-Whitney U","U":r["U"],"p":r["p"],"cliffs_delta":r["cliffs_delta"],"n_by_area":{a:r["n1"],b:r["n2"]}}
  # No redundant area-pair Holm correction when there is exactly one comparison.
  return {"omnibus":primary,"pairwise":{},"direct_two_area":r}
 om=kw(g); om["test"]="Kruskal-Wallis"
 prs={}; raw=[]
 for i,a in enumerate(areas):
  for b in areas[i+1:]:
   r=mw(g.get(a,[]),g.get(b,[])); r.update({"area1":a,"area2":b}); prs[f"{a}_vs_{b}"]=r; raw.append(r["p"])
 adj=holm(raw)
 for r,ph in zip(prs.values(),adj): r["p_holm_pairs"]=ph
 return {"omnibus":om,"pairwise":prs}

def load_tables(subject,dates,areas):
 frames=[]
 for a in areas:
  p=input_csv(subject,a,dates)
  if not p.exists(): print("WARNING missing",a,p); continue
  d=pd.read_csv(p); d["canonicalArea"]=a; frames.append(d)
 if not frames: raise FileNotFoundError("No area inputs found")
 d=pd.concat(frames,ignore_index=True,sort=False)
 for c in d.columns:
  if c.endswith("_responsive_fdr") or c.endswith("_excited_fdr") or c.endswith("_suppressed_fdr"):
   if d[c].dtype==object: d[c]=d[c].astype(str).str.lower().map({"true":True,"false":False})
 return d
def subset_depth(df,key):
 lo,hi,_=DEPTHS[key]; x=pd.to_numeric(df.depth,errors="coerce"); return df[(x>=lo)&(x<hi)].copy()
def responsive(df,b):
 c=f"{SHORT[b]}_responsive_fdr"; return df[df[c].fillna(False).astype(bool)].copy() if c in df else df.iloc[0:0].copy()
def fov_metric(df,metric):
 if metric not in df: return pd.DataFrame(columns=["fov_uid","canonicalArea","value"])
 x=df[["fov_uid","canonicalArea",metric]].copy(); x[metric]=pd.to_numeric(x[metric],errors="coerce"); return x.groupby(["fov_uid","canonicalArea"],as_index=False)[metric].mean().rename(columns={metric:"value"})
def fov_percent(df,col):
 if col not in df: return pd.DataFrame(columns=["fov_uid","canonicalArea","value"])
 x=df[df[col].notna()][["fov_uid","canonicalArea",col]].copy(); x[col]=x[col].astype(float); t=x.groupby(["fov_uid","canonicalArea"],as_index=False)[col].mean(); t["value"]=100*t[col]; return t[["fov_uid","canonicalArea","value"]]
def stat_from_table(t,areas): return cross_stats({a:t.loc[t.canonicalArea==a,"value"] for a in areas},areas)
def condition_cols(df,b):
 if b=="pure_tones": pat=re.compile(r"^pure_response_([0-9.eE+-]+)_Hz$")
 elif b=="chord_tones": pat=re.compile(r"^chord_response_middle_oct_([0-9.eE+-]+)$")
 else: pat=re.compile(r"^fm_response_slope_(pos|neg)?([0-9.eE+]+)_oct_per_s$")
 out=[]
 for c in df.columns:
  m=pat.match(c)
  if not m: continue
  v=(-1 if b=="fm_tones" and m.group(1)=="neg" else 1)*float(m.group(2) if b=="fm_tones" else m.group(1)); out.append((v,c))
 return sorted(out)
def fov_profile(df,cols):
 rows=[]
 for (u,a),g in df.groupby(["fov_uid","canonicalArea"]):
  r={"fov_uid":u,"canonicalArea":a}
  for v,c in cols:
   z=pd.to_numeric(g[c],errors="coerce"); r[c]=float(np.nanmean(z)) if np.any(np.isfinite(z)) else np.nan
  rows.append(r)
 return pd.DataFrame(rows)
def preference_table(df,b,resp_only=True):
 m,_=PREF[b]
 if m not in df: return pd.DataFrame(),[]
 use=responsive(df,b) if resp_only else df[df[m].notna()].copy()
 if use.empty: return pd.DataFrame(),[]
 vals=np.sort(pd.to_numeric(use[m],errors="coerce").dropna().unique()); rows=[]
 for (u,a),g in use.groupby(["fov_uid","canonicalArea"]):
  x=pd.to_numeric(g[m],errors="coerce").to_numpy(float); x=x[np.isfinite(x)]
  for v in vals: rows.append({"fov_uid":u,"canonicalArea":a,"condition":v,"value":100*np.mean(np.isclose(x,v)) if len(x) else np.nan})
 return pd.DataFrame(rows),vals.tolist()

def stat_lines(rec,scope="FOV-level primary"):
 o=rec["omnibus"]; lines=[scope]
 if o.get("test")=="Mann-Whitney U":
  areas=list(o.get("n_by_area",{})); pair=f"{areas[0]} vs {areas[1]}" if len(areas)==2 else "2-area comparison"
  line=f"{pair}: Mann-Whitney U={o.get('U',np.nan):.3g}, p={ptxt(o.get('p',np.nan))}, d={o.get('cliffs_delta',np.nan):.2f}"
  if "p_holm_family" in o: line+=f", family-Holm={ptxt(o['p_holm_family'])}"
  if len(areas)==2: line+=f", n={o['n_by_area'][areas[0]]}/{o['n_by_area'][areas[1]]}"
  lines.append(line)
 else:
  line=f"Kruskal-Wallis: H={o.get('H',np.nan):.3g}, p={ptxt(o.get('p',np.nan))}"
  if "p_holm_family" in o: line+=f", family-Holm={ptxt(o['p_holm_family'])}"
  lines.append(line)
  for r in rec["pairwise"].values(): lines.append(f"{r['area1']} vs {r['area2']}: U={r['U']:.3g}, p={ptxt(r['p'])}, Holm={ptxt(r['p_holm_pairs'])}, d={r['cliffs_delta']:.2f}, n={r['n1']}/{r['n2']}")
 return lines
def draw_stats(ax,lines): ax.axis("off"); ax.text(.01,.99,"\n".join(lines),va="top",ha="left",fontsize=8.2,family="monospace")



def _readable_ticks(ax,x,labels,dense_threshold=10):
 x=np.asarray(x,float); labels=list(labels); ax.set_xticks(x)
 if len(labels)>=dense_threshold: ax.set_xticklabels([lab if i%2==0 else "" for i,lab in enumerate(labels)],rotation=60,ha="right",rotation_mode="anchor")
 else: ax.set_xticklabels(labels,rotation=45 if len(labels)>6 else 0,ha="right" if len(labels)>6 else "center")

def _fm_log_positions(values):
 values=np.asarray(values,float); out=np.full(values.shape,np.nan,float); finite=np.isfinite(values); mags=np.sort(np.unique(np.abs(values[finite&(values!=0)])))
 if not len(mags): out[finite]=0.; return out
 lm=np.log2(mags); step=float(np.median(np.diff(lm))) if len(lm)>1 else 1.; step=step if np.isfinite(step) and step>0 else 1.; base=step if np.any(finite&np.isclose(values,0)) else .5*step; nz=finite&(values!=0); out[nz]=np.sign(values[nz])*(base+np.log2(np.abs(values[nz])/mags[0])); out[finite&np.isclose(values,0)]=0.; return out

def _condition_x(b,vals):
 vals=np.asarray(vals,float)
 if b=="pure_tones": return np.log2(vals/1000.)
 if b=="fm_tones": return _fm_log_positions(vals)
 return vals
def _selectivity_equation_box(ax,b):
 ax.text(.02,.03,SELECTIVITY_SPEC[b]["equation"],transform=ax.transAxes,ha="left",va="bottom",fontsize=9.3,bbox=dict(boxstyle="round,pad=.32",facecolor="white",edgecolor=".75",alpha=.95))

def pooled_cell_stats(df,metric,areas):
 groups={a:pd.to_numeric(df.loc[df.canonicalArea==a,metric],errors='coerce').dropna().to_numpy(float) if metric in df else np.array([]) for a in areas}
 return cross_stats(groups,areas)

def plot_metric_cell_points(cells,b,branch,areas,cls,depth,out):
 use=cells if branch=='all_cells' else responsive(cells,b); avail=[(m,l) for m,l in METRICS[b] if m in use and np.any(np.isfinite(pd.to_numeric(use[m],errors='coerce')))]
 if not avail:return
 n=len(avail); fig,axes=plt.subplots(2,n,figsize=(5*n,8),gridspec_kw={'height_ratios':[2,1.35]},squeeze=False); rng=np.random.default_rng(3381)
 for j,(m,label) in enumerate(avail):
  ax=axes[0,j]; rec=pooled_cell_stats(use,m,areas)
  for i,a in enumerate(areas):
   z=pd.to_numeric(use.loc[use.canonicalArea==a,m],errors='coerce').dropna().to_numpy(float)
   if len(z): ax.scatter(np.full(len(z),i)+rng.uniform(-.10,.10,len(z)),z,s=12,alpha=.22,facecolors=AREA_COLORS[a],edgecolors='none')
   mu,se,nn=mean_sem(z); ax.errorbar(i,mu,yerr=se,fmt='o',color='black',capsize=3,zorder=4)
  ax.set_xticks(range(len(areas))); ax.set_xticklabels(areas); ax.set_ylabel(label); ax.set_title(label)
  if 'selectivity' in m: ax.axhline(0,color='.5',ls='--',lw=.8)
  draw_stats(axes[1,j],stat_lines(rec,'EXPLORATORY pooled-cell comparison'))
 fig.suptitle(f"{cls.upper()} across areas — {depth}: {BLOCK_LABEL[b]} — {branch.replace('_',' ')} — individual cells"); fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(out/f"{b}_selectivity_{branch}_CELL_POINTS.png",dpi=250); plt.close(fig)

def plot_profile_cells(cells,b,branch,areas,cls,depth,out):
 use=cells if branch=='all_cells' else responsive(cells,b); cols=condition_cols(use,b)
 if not cols:return
 vals=np.array([v for v,_ in cols]); x=_condition_x(b,vals); fig,ax=plt.subplots(figsize=(10.5,6))
 for a in areas:
  M=use.loc[use.canonicalArea==a,[c for _,c in cols]].apply(pd.to_numeric,errors='coerce').to_numpy(float)
  if len(M):
   for row in M: ax.plot(x,row,color=AREA_COLORS[a],alpha=.045,lw=.5)
   mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy='omit'); ax.plot(x,mu,color=AREA_COLORS[a],marker='o',lw=2,label=f"{a} n={len(M)} cells"); ax.fill_between(x,mu-se,mu+se,color=AREA_COLORS[a],alpha=.15)
 ax.axhline(0,color='.5',ls='--',lw=.8); ax.set_ylabel('Cell response (dF/F)'); ax.legend(frameon=False)
 if b=='pure_tones': _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel('Frequency (kHz; log2 spacing)')
 elif b=='chord_tones': _readable_ticks(ax,x,[f"{v:.3g}" for v in vals]); ax.set_xlabel('Middle tone position (octaves above F0)')
 else: _readable_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel('FM slope (octaves/s; signed log2-magnitude spacing)')
 ax.set_title(f"{cls.upper()} {depth}: {BLOCK_LABEL[b]} — {branch.replace('_',' ')} — pooled individual-cell profiles (descriptive)"); fig.tight_layout(); fig.savefig(out/f"{b}_profile_{branch}_CELL_PROFILES.png",dpi=250); plt.close(fig)

def plot_bf_comparison(cells,areas,cls,depth,out):
 if 'pure_best_frequency_hz' not in cells or 'pure_responsive_fdr' not in cells:return {}
 use=cells[cells.pure_responsive_fdr.fillna(False).astype(bool)&pd.to_numeric(cells.pure_best_frequency_hz,errors='coerce').notna()].copy()
 if use.empty:return {}
 root=out/'best_frequency'; root.mkdir(exist_ok=True)
 vals=np.sort(pd.to_numeric(use.pure_best_frequency_hz,errors='coerce').dropna().unique()); x=np.log2(vals/1000)
 # descriptive pooled histograms by area
 fig,ax=plt.subplots(figsize=(10.5,5.8))
 for a in areas:
  arr=pd.to_numeric(use.loc[use.canonicalArea==a,'pure_best_frequency_hz'],errors='coerce').dropna().to_numpy(float); frac=np.array([np.mean(np.isclose(arr,v)) if len(arr) else np.nan for v in vals]); ax.plot(x,frac,marker='o',lw=2,color=AREA_COLORS[a],label=f"{a} n={len(arr)}")
 _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel('Best frequency (kHz; log2 spacing)'); ax.set_ylabel('Fraction of pure-tone responsive cells'); ax.legend(frameon=False); ax.set_title(f"{cls.upper()} {depth}: pooled BF distributions (descriptive)"); fig.tight_layout(); fig.savefig(root/'BF_pooled_histogram_by_area.png',dpi=250); plt.close(fig)
 # one normalized histogram + median BF per FOV
 rows=[]
 for (uid,a),g in use.groupby(['fov_uid','canonicalArea']):
  arr=pd.to_numeric(g.pure_best_frequency_hz,errors='coerce').dropna().to_numpy(float)
  if len(arr):
   r={'fov_uid':uid,'canonicalArea':a,'median_log2_bf':float(np.median(np.log2(arr))),'n_cells':len(arr)}
   for v in vals:r[str(v)]=float(np.mean(np.isclose(arr,v)))
   rows.append(r)
 tab=pd.DataFrame(rows); tab.to_csv(root/'BF_FOV_distributions.csv',index=False)
 if tab.empty:return {}
 medstat=cross_stats({a:tab.loc[tab.canonicalArea==a,'median_log2_bf'] for a in areas},areas)
 # per-bin tests, corrected across BF bins
 binstats={}; prim=[]
 for v in vals:
  r=cross_stats({a:tab.loc[tab.canonicalArea==a,str(v)] for a in areas},areas); binstats[str(v)]=r; prim.append(r['omnibus']['p'])
 adj=holm(prim)
 for r,ph in zip(binstats.values(),adj):r['omnibus']['p_holm_family']=ph
 fig,(ax,axs)=plt.subplots(1,2,figsize=(16,6),gridspec_kw={'width_ratios':[1.5,1]})
 for a in areas:
  M=tab.loc[tab.canonicalArea==a,[str(v) for v in vals]].to_numpy(float)
  if len(M):
   for row in M:ax.plot(x,row,color=AREA_COLORS[a],alpha=.15,lw=.7)
   mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy='omit'); ax.errorbar(x,mu,yerr=se,marker='o',lw=2,color=AREA_COLORS[a],capsize=3,label=f"{a} nFOV={len(M)}")
 _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel('Best frequency (kHz; log2 spacing)'); ax.set_ylabel('Fraction of cells per FOV'); ax.legend(frameon=False)
 lines=[('Direct two-area MW per BF bin' if len(areas)==2 else 'KW + pairwise MW per BF bin')+f"; Holm across {len(vals)} BF bins"]
 for v in vals:
  r=binstats[str(v)]; lines+= [f"{v/1000:g} kHz: "+stat_lines(r,'')[1]+f", family={ptxt(r['omnibus'].get('p_holm_family',np.nan))}"]
 draw_stats(axs,lines); fig.suptitle(f"{cls.upper()} {depth}: BF distribution across FOVs"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(root/'BF_FOV_fraction_profiles_with_stats.png',dpi=250); plt.close(fig)
 # median BF comparison
 fig,(ax,axs)=plt.subplots(1,2,figsize=(12,5.2),gridspec_kw={'width_ratios':[1.3,1]}); rng=np.random.default_rng(981)
 for i,a in enumerate(areas):
  z=tab.loc[tab.canonicalArea==a,'median_log2_bf'].to_numpy(float); ns=tab.loc[tab.canonicalArea==a,'n_cells'].to_numpy(float); ax.scatter(np.full(len(z),i)+rng.uniform(-.07,.07,len(z)),z,s=35+6*np.sqrt(ns),facecolors=AREA_COLORS[a],edgecolors='none',alpha=.8); mu,se,n=mean_sem(z); ax.errorbar(i,mu,yerr=se,fmt='o',color='black',capsize=4)
 ax.set_xticks(range(len(areas))); ax.set_xticklabels(areas); ax.set_ylabel('FOV median log2(BF [Hz])'); ax.set_title('Marker size = responsive-cell count'); draw_stats(axs,stat_lines(medstat)); fig.suptitle(f"{cls.upper()} {depth}: FOV-level BF center"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(root/'BF_FOV_median_comparison.png',dpi=250); plt.close(fig)
 return {'median_bf':medstat,'bf_bins':binstats}

def build_stats(cells,areas):
 out={"responsiveness":{},"metrics":{},"profiles":{},"preferences":{}}
 # responsiveness family
 recs=[]
 for b in BLOCKS:
  t=fov_percent(cells,f"{SHORT[b]}_responsive_fdr"); r=stat_from_table(t,areas); out["responsiveness"][b]={"table":t,"stats":r}; recs.append(r)
 adj=holm([r["omnibus"]["p"] for r in recs])
 for r,ph in zip(recs,adj): r["omnibus"]["p_holm_family"]=ph
 for b in BLOCKS:
  out["metrics"][b]={}
  for branch in ("all_cells","responsive_only"):
   use=cells if branch=="all_cells" else responsive(cells,b); fam=[]
   for metric,label in METRICS[b]:
    t=fov_metric(use,metric); r=stat_from_table(t,areas); out["metrics"][b].setdefault(branch,{})[metric]={"label":label,"table":t,"stats":r}; fam.append(r)
   adj=holm([r["omnibus"]["p"] for r in fam])
   for r,ph in zip(fam,adj): r["omnibus"]["p_holm_family"]=ph
   cols=condition_cols(use,b); ft=fov_profile(use,cols); out["profiles"].setdefault(b,{})[branch]={"table":ft,"conditions":cols,"stats":{}}
   rr=[]
   for v,c in cols:
    groups={a:(ft.loc[ft["canonicalArea"]==a,c] if (not ft.empty and "canonicalArea" in ft and c in ft) else np.array([])) for a in areas}
    r=cross_stats(groups,areas); out["profiles"][b][branch]["stats"][str(v)]=r; rr.append(r)
   adj=holm([r["omnibus"]["p"] for r in rr])
   for r,ph in zip(rr,adj): r["omnibus"]["p_holm_family"]=ph
  out["preferences"][b]={}
  for resp_only in (True,False):
   key="responsive_only" if resp_only else "all_cells_descriptive"; tab,vals=preference_table(cells,b,resp_only); fam=[]; sd={}
   for v in vals:
    r=cross_stats({a:tab.loc[(tab.canonicalArea==a)&np.isclose(tab.condition,v),"value"] for a in areas},areas); sd[str(v)]=r; fam.append(r)
   adj=holm([r["omnibus"]["p"] for r in fam])
   for r,ph in zip(fam,adj): r["omnibus"]["p_holm_family"]=ph
   out["preferences"][b][key]={"table":tab,"conditions":vals,"stats":sd}
 return out


def plot_responsiveness(cells,st,areas,cls,depth,out):
 fig,axes=plt.subplots(2,3,figsize=(16,8),gridspec_kw={"height_ratios":[2,1.25]})
 for j,b in enumerate(BLOCKS):
  ax=axes[0,j]; t=st["responsiveness"][b]["table"]
  for i,a in enumerate(areas):
   v=finite(t.loc[t.canonicalArea==a,"value"]); ax.scatter(np.full(len(v),i),v,s=30,facecolors=AREA_COLORS[a],edgecolors="none"); mu,se,n=mean_sem(v); ax.errorbar(i,mu,yerr=se,fmt="o",color="black",capsize=4)
  ax.set_xticks(range(len(areas))); ax.set_xticklabels(areas); ax.set_ylim(0,100); ax.set_ylabel("Responsive cells (%)"); ax.set_title(BLOCK_LABEL[b]); draw_stats(axes[1,j],stat_lines(st["responsiveness"][b]["stats"]))
 fig.suptitle(f"{cls.upper()} across areas — {depth}: sound responsiveness"); fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(out/"responsiveness_across_areas_FOV_POINTS.png",dpi=250); plt.close(fig)

def plot_metric_family(cells,st,b,branch,areas,cls,depth,out):
 recs=st["metrics"][b][branch]; if_avail=[(m,r) for m,r in recs.items() if len(r["table"])]
 if not if_avail: return
 n=len(if_avail); fig,axes=plt.subplots(2,n,figsize=(5*n,8),gridspec_kw={"height_ratios":[2,1.35]},squeeze=False)
 for j,(m,r) in enumerate(if_avail):
  ax=axes[0,j]; t=r["table"]
  for i,a in enumerate(areas):
   v=finite(t.loc[t.canonicalArea==a,"value"]); ax.scatter(np.full(len(v),i),v,s=26,facecolors=AREA_COLORS[a],edgecolors="none"); mu,se,nn=mean_sem(v); ax.errorbar(i,mu,yerr=se,fmt="o",color="black",capsize=3)
  ax.set_xticks(range(len(areas))); ax.set_xticklabels(areas); ax.set_ylabel(r["label"]); ax.set_title(r["label"])
  if "selectivity" in m: ax.axhline(0,color=".5",ls="--",lw=1)
  draw_stats(axes[1,j],stat_lines(r["stats"]))
 fig.suptitle(f"{cls.upper()} across areas — {depth}: {BLOCK_LABEL[b]} — {branch.replace('_',' ')}"); fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(out/f"{b}_selectivity_{branch}_FOV_POINTS.png",dpi=250); plt.close(fig)

def plot_primary_selectivity_cross_area_fov(st,b,branch,areas,cls,depth,out):
 spec=SELECTIVITY_SPEC[b]; metric=spec["metric"]; rec=st["metrics"][b][branch].get(metric)
 if rec is None or rec["table"].empty: return
 root=out/"selectivity_plots"/spec["folder"]; root.mkdir(parents=True,exist_ok=True)
 fig,(ax,axs)=plt.subplots(1,2,figsize=(12,5.6),gridspec_kw={"width_ratios":[1.4,1]}); t=rec["table"]
 for i,a in enumerate(areas):
  z=finite(t.loc[t.canonicalArea==a,"value"]); ax.scatter(np.full(len(z),i),z,s=30,facecolors=AREA_COLORS[a],edgecolors="none"); mu,se,n=mean_sem(z); ax.errorbar(i,mu,yerr=se,fmt="o",color="black",capsize=4)
 ax.set_xticks(range(len(areas))); ax.set_xticklabels(areas); ax.set_ylabel(spec["label"]); ax.set_ylim(*spec["ylim"])
 if spec["ylim"][0]<0: ax.axhline(0,color=".55",ls="--",lw=.8)
 _selectivity_equation_box(ax,b); draw_stats(axs,stat_lines(rec["stats"])); fig.suptitle(f"{cls.upper()} {depth}: {BLOCK_LABEL[b]} — {branch.replace('_',' ')}\nprimary FOV selectivity across areas"); fig.tight_layout(rect=[0,0,1,.93]); fig.savefig(root/f"{branch}_cross_area_FOV_primary_selectivity.png",dpi=250); plt.close(fig)

def plot_primary_selectivity_cross_area_cells(cells,b,branch,areas,cls,depth,out):
 spec=SELECTIVITY_SPEC[b]; metric=spec["metric"]; use=cells if branch=="all_cells" else responsive(cells,b)
 if metric not in use or not np.any(np.isfinite(pd.to_numeric(use[metric],errors="coerce"))): return
 rec=pooled_cell_stats(use,metric,areas); root=out/"selectivity_plots"/spec["folder"]; root.mkdir(parents=True,exist_ok=True)
 fig,(ax,axs)=plt.subplots(1,2,figsize=(12,5.6),gridspec_kw={"width_ratios":[1.4,1]}); rng=np.random.default_rng(7712)
 for i,a in enumerate(areas):
  z=pd.to_numeric(use.loc[use.canonicalArea==a,metric],errors="coerce").dropna().to_numpy(float)
  if len(z): ax.scatter(np.full(len(z),i)+rng.uniform(-.08,.08,len(z)),z,s=13,alpha=.25,facecolors=AREA_COLORS[a],edgecolors="none")
  mu,se,n=mean_sem(z); ax.errorbar(i,mu,yerr=se,fmt="o",color="black",capsize=4,zorder=4)
 ax.set_xticks(range(len(areas))); ax.set_xticklabels(areas); ax.set_ylabel(spec["label"]); ax.set_ylim(*spec["ylim"])
 if spec["ylim"][0]<0: ax.axhline(0,color=".55",ls="--",lw=.8)
 _selectivity_equation_box(ax,b); draw_stats(axs,stat_lines(rec,"EXPLORATORY pooled-cell comparison")); fig.suptitle(f"{cls.upper()} {depth}: {BLOCK_LABEL[b]} — {branch.replace('_',' ')}\ncell-level selectivity across areas"); fig.tight_layout(rect=[0,0,1,.93]); fig.savefig(root/f"{branch}_cross_area_CELL_exploratory_selectivity.png",dpi=250); plt.close(fig)

def plot_profile(st,b,branch,areas,cls,depth,out):
 rec=st["profiles"][b][branch]; t=rec["table"]; cols=rec["conditions"]
 if t.empty or not cols: return
 vals=np.array([v for v,_ in cols]); x=_condition_x(b,vals)
 fig,(ax,axs)=plt.subplots(1,2,figsize=(15,6),gridspec_kw={"width_ratios":[1.6,1]})
 for a in areas:
  M=t.loc[t.canonicalArea==a,[c for _,c in cols]].to_numpy(float)
  if len(M):
   for row in M: ax.plot(x,row,color=AREA_COLORS[a],alpha=.12,lw=.7)
   mu=np.nanmean(M,axis=0); se=stats.sem(M,axis=0,nan_policy="omit"); ax.plot(x,mu,marker="o",lw=2,color=AREA_COLORS[a],label=f"{a} nFOV={len(M)}"); ax.fill_between(x,mu-se,mu+se,color=AREA_COLORS[a],alpha=.12)
 ax.axhline(0,color=".5",ls="--",lw=1); ax.set_ylabel("Mean cell response/FOV (dF/F)"); ax.legend(frameon=False)
 if b=="pure_tones": _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel("Frequency (kHz; log2 spacing)")
 elif b=="chord_tones": ax.set_xlabel("Middle tone octave above F0")
 else: _readable_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel("FM slope (octaves/s; signed log2-magnitude spacing)")
 lines=[f"Per-condition {'direct Mann-Whitney U' if len(areas)==2 else 'Kruskal-Wallis + all pairwise MW'}; Holm across {len(cols)} conditions"]
 for v,_ in cols:
  r=rec["stats"][str(v)]; lines.append(f"{v:g}: primary p={ptxt(r['omnibus']['p'])}, family={ptxt(r['omnibus'].get('p_holm_family',np.nan))}")
  for q in r["pairwise"].values(): lines.append(f"  {q['area1']}-{q['area2']}: Holm={ptxt(q['p_holm_pairs'])}")
 draw_stats(axs,lines); fig.suptitle(f"{cls.upper()} {depth}: {BLOCK_LABEL[b]} profile — {branch.replace('_',' ')}"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(out/f"{b}_profile_{branch}_FOV_MEANS.png",dpi=250); plt.close(fig)

def plot_preference(st,b,key,areas,cls,depth,out):
 rec=st["preferences"][b][key]; t=rec["table"]; vals=rec["conditions"]
 if t.empty or not vals: return
 x=_condition_x(b,np.asarray(vals,float))
 fig,(ax,axs)=plt.subplots(1,2,figsize=(15,6),gridspec_kw={"width_ratios":[1.6,1]})
 for a in areas:
  mu=[]; se=[]
  for v in vals:
   z=t.loc[(t.canonicalArea==a)&np.isclose(t.condition,v),"value"]; m,s,n=mean_sem(z); mu.append(m); se.append(s)
  ax.errorbar(x,mu,yerr=se,marker="o",lw=2,color=AREA_COLORS[a],capsize=3,label=a)
 ax.set_ylabel("Cells preferring condition (%)"); ax.legend(frameon=False)
 if b=="pure_tones": _readable_ticks(ax,x,[f"{v/1000:g}" for v in vals]); ax.set_xlabel("Best frequency (kHz; log2 spacing)")
 elif b=="fm_tones": _readable_ticks(ax,x,[f"{v:g}" for v in vals]); ax.set_xlabel(PREF[b][1]+" (signed log2-magnitude spacing)")
 else: ax.set_xlabel(PREF[b][1])
 lines=[f"Per-bin FOV percentages; {'direct Mann-Whitney U' if len(areas)==2 else 'Kruskal-Wallis + pairwise MW'}; Holm across {len(vals)} bins"]
 for v in vals:
  r=rec["stats"][str(v)]; lines.append(f"{v:g}: primary={ptxt(r['omnibus']['p'])}, family={ptxt(r['omnibus'].get('p_holm_family',np.nan))}")
  for q in r["pairwise"].values(): lines.append(f"  {q['area1']}-{q['area2']}: Holm={ptxt(q['p_holm_pairs'])}")
 draw_stats(axs,lines); fig.suptitle(f"{cls.upper()} {depth}: {PREF[b][1]} distribution — {key.replace('_',' ')}"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(out/f"{b}_preference_distribution_{key}.png",dpi=250); plt.close(fig)

# -----------------------------------------------------------------------------
# Area x layer explicit tests
# -----------------------------------------------------------------------------
def layer_pair_stat(df,metric,areas,percent=False):
 rows={}; raw=[]
 for a in areas:
  ad=df[df.canonicalArea==a]; groups={}
  for lk in ("L23_100to300um","L45_300to600um"):
   sub=subset_depth(ad,lk); t=fov_percent(sub,metric) if percent else fov_metric(sub,metric); groups[lk]=t.value
  r=mw(groups["L23_100to300um"],groups["L45_300to600um"]); rows[a]=r; raw.append(r["p"])
 adj=holm(raw)
 for a,ph in zip(areas,adj): rows[a]["p_holm_across_areas"]=ph
 return rows
def plot_area_layer(cells,areas,cls,root):
 out=root/"area_by_layer"/cls; out.mkdir(parents=True,exist_ok=True); statsout={}
 items=[]
 for b in BLOCKS: items.append((f"{SHORT[b]}_responsive_fdr",f"{BLOCK_LABEL[b]} responsive cells (%)",True,None))
 for b in BLOCKS:
  for m,l in METRICS[b]: items.append((m,f"{BLOCK_LABEL[b]}: {l}",False,b))
 items.append(("pure_best_frequency_log2_hz","Pure-tone BF center (log2 Hz; responsive cells)",False,"pure_tones"))
 for metric,label,ispercent,b in items:
  use=cells if not b else responsive(cells,b)
  if metric not in use: continue
  rec=layer_pair_stat(use,metric,areas,ispercent); statsout[metric]=rec
  fig,(ax,axs)=plt.subplots(1,2,figsize=(12,5.5),gridspec_kw={"width_ratios":[1.5,1]})
  xpos={}; tick=[]; k=0
  for ai,a in enumerate(areas):
   for li,lk in enumerate(("L23_100to300um","L45_300to600um")):
    sub=subset_depth(use[use.canonicalArea==a],lk); t=fov_percent(sub,metric) if ispercent else fov_metric(sub,metric); v=finite(t.value); x=k; xpos[(a,lk)]=x; ax.scatter(np.full(len(v),x),v,s=25,facecolors=AREA_COLORS[a],edgecolors="none",alpha=.75); mu,se,n=mean_sem(v); ax.errorbar(x,mu,yerr=se,fmt="o",color="black",capsize=3); tick.append(f"{a}\n{'L2/3' if li==0 else 'L4/5'}"); k+=1
   k+=.5
  ax.set_xticks(list(xpos.values())); ax.set_xticklabels(tick); ax.set_ylabel(label); ax.set_title("FOV points + mean ± SEM")
  lines=["Within-area L2/3 vs L4/5: MW U; Holm across 3 areas"]
  for a,r in rec.items(): lines.append(f"{a}: U={r['U']:.3g}, p={ptxt(r['p'])}, Holm={ptxt(r['p_holm_across_areas'])}, d={r['cliffs_delta']:.2f}, n={r['n1']}/{r['n2']}")
  draw_stats(axs,lines); fig.suptitle(f"{cls.upper()} area x layer — {label}"); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig(out/f"area_layer_{metric}_FOV_POINTS.png",dpi=250); plt.close(fig)
 save_json(out/"area_layer_statistics.json",statsout)

def plot_area_layer_primary_selectivity(cells,areas,cls,root):
 outbase=root/"area_by_layer"/cls/"selectivity_plots"
 for b in BLOCKS:
  spec=SELECTIVITY_SPEC[b]; metric=spec["metric"]; use=responsive(cells,b)
  if metric not in use or not np.any(np.isfinite(pd.to_numeric(use[metric],errors="coerce"))): continue
  rec=layer_pair_stat(use,metric,areas,False); out=outbase/spec["folder"]; out.mkdir(parents=True,exist_ok=True)
  fig,(ax,axs)=plt.subplots(1,2,figsize=(12,5.6),gridspec_kw={"width_ratios":[1.5,1]}); xpos={}; labels=[]; k=0
  for a in areas:
   for li,lk in enumerate(("L23_100to300um","L45_300to600um")):
    sub=subset_depth(use[use.canonicalArea==a],lk); t=fov_metric(sub,metric); z=finite(t.value); xpos[(a,lk)]=k
    ax.scatter(np.full(len(z),k),z,s=28,facecolors=AREA_COLORS[a],edgecolors="none",alpha=.78); mu,se,n=mean_sem(z); ax.errorbar(k,mu,yerr=se,fmt="o",color="black",capsize=3); labels.append(f"{a}\n{'L2/3' if li==0 else 'L4/5'}"); k+=1
   k+=.5
  ax.set_xticks(list(xpos.values())); ax.set_xticklabels(labels); ax.set_ylabel(spec["label"]); ax.set_ylim(*spec["ylim"])
  if spec["ylim"][0]<0: ax.axhline(0,color=".55",ls="--",lw=.8)
  _selectivity_equation_box(ax,b); lines=["Within-area L2/3 vs L4/5: MW U; Holm across areas"]
  for a,r in rec.items(): lines.append(f"{a}: U={r['U']:.3g}, p={ptxt(r['p'])}, Holm={ptxt(r['p_holm_across_areas'])}, d={r['cliffs_delta']:.2f}, n={r['n1']}/{r['n2']}")
  draw_stats(axs,lines); fig.suptitle(f"{cls.upper()} area x layer: {BLOCK_LABEL[b]} primary selectivity\nresponsive cells; FOV is replicate"); fig.tight_layout(rect=[0,0,1,.93]); fig.savefig(out/"area_layer_FOV_primary_selectivity.png",dpi=250); plt.close(fig)

# -----------------------------------------------------------------------------
# Trial-reduction utilities
# -----------------------------------------------------------------------------
def bh(p):
 p=np.asarray(p,float); q=np.full_like(p,np.nan); idx=np.flatnonzero(np.isfinite(p))
 if not len(idx): return q
 v=p[idx]; o=np.argsort(v); r=v[o]; a=r*len(r)/np.arange(1,len(r)+1); a=np.minimum.accumulate(a[::-1])[::-1]; q[idx[o]]=np.minimum(a,1); return q
def sparse_rows(mat):
 x=np.abs(np.asarray(mat,float)); out=np.full(x.shape[0],np.nan)
 for i,row in enumerate(x):
  v=row[np.isfinite(row)]; n=len(v)
  if n<=1 or np.mean(v*v)<=0: continue
  out[i]=(1-(np.mean(v)**2/np.mean(v*v)))/(1-1/n)
 return out
def gini_rows(mat):
 x=np.abs(np.asarray(mat,float)); out=np.full(x.shape[0],np.nan)
 for i,row in enumerate(x):
  v=np.sort(row[np.isfinite(row)]); n=len(v)
  if not n or np.sum(v)<=0: continue
  out[i]=np.sum((2*np.arange(1,n+1)-n-1)*v)/(n*np.sum(v))
 return out
def fano_rows(mat):
 x=np.abs(np.asarray(mat,float)); out=np.full(x.shape[0],np.nan)
 for i,row in enumerate(x):
  v=row[np.isfinite(row)]
  if len(v)>1 and np.mean(v)>0: out[i]=np.var(v,ddof=1)/np.mean(v)
 return out
def bounded(a,b):
 a=np.asarray(a,float); b=np.asarray(b,float); d=np.abs(a)+np.abs(b); o=np.full_like(a,np.nan); m=np.isfinite(a)&np.isfinite(b)&(d>0); o[m]=(a[m]-b[m])/d[m]; return o


def fwhm_log2_rows(mat,values):
 x=np.asarray(mat,float); values=np.asarray(values,float); out=np.full(x.shape[0],np.nan)
 if len(values)<3 or np.any(values<=0): return out
 o=np.argsort(values); xx=np.log2(values[o]); yy=x[:,o]
 for i,y in enumerate(yy):
  if not np.all(np.isfinite(y)): continue
  pk=int(np.argmax(y)); peak=y[pk]
  if pk==0 or pk==len(y)-1 or peak<=0: continue
  half=peak/2; li=np.flatnonzero(y[:pk]<=half); ri=np.flatnonzero(y[pk+1:]<=half)
  if not len(li) or not len(ri): continue
  l0=li[-1]; l1=l0+1; r1=pk+1+ri[0]; r0=r1-1
  def ip(xa,ya,xb,yb): return np.nan if yb==ya else xa+(half-ya)*(xb-xa)/(yb-ya)
  xl=ip(xx[l0],y[l0],xx[l1],y[l1]); xr=ip(xx[r0],y[r0],xx[r1],y[r1])
  if np.isfinite(xl) and np.isfinite(xr) and xr>=xl: out[i]=xr-xl
 return out

def signflip(vals,nperm,rng):
 vals=np.asarray(vals,float); nc=vals.shape[0]; p=np.full(nc,np.nan)
 for i in range(nc):
  v=vals[i,np.isfinite(vals[i])]
  if len(v)<3: continue
  obs=np.mean(v); signs=rng.choice([-1.,1.],size=(nperm,len(v))); null=np.mean(signs*v[None,:],axis=1); p[i]=(1+np.sum(np.abs(null)>=abs(obs)))/(nperm+1)
 return p

def load_arc(path,cache):
 path=str(path)
 if path not in cache:
  with np.load(path,allow_pickle=False) as z: cache[path]={k:z[k] for k in z.files}
 return cache[path]
def recompute_block_from_archive(arc,fraction,rng,nperm):
 tr=np.asarray(arc["trial_response"],float); cond=np.asarray(arc["trial_condition_value"],float); valid=np.asarray(arc["valid_trial_mask"],bool); vals=np.asarray(arc["condition_values"],float)
 keep=np.zeros(len(cond),bool)
 for v in vals:
  idx=np.flatnonzero(valid & np.isclose(cond,v)); n=max(1,int(np.floor(len(idx)*fraction))) if len(idx) else 0
  if n: keep[rng.choice(idx,size=n,replace=False)]=True
 curve=np.full((tr.shape[0],len(vals)),np.nan); sig=np.zeros_like(curve,bool)
 for j,v in enumerate(vals):
  m=keep & np.isclose(cond,v); curve[:,j]=np.nanmean(tr[:,m],axis=1) if np.any(m) else np.nan
  p=signflip(tr[:,m],nperm,rng) if np.any(m) else np.full(tr.shape[0],np.nan); q=bh(p); sig[:,j]=np.isfinite(q)&(q<.05)
 resp=np.any(sig,axis=1); pref=np.array([vals[np.nanargmax(row)] if np.any(np.isfinite(row)) else np.nan for row in curve])
 return vals,curve,resp,pref

def reduced_yellow(full,fraction,rng,nperm,cache):
 out=full.copy()
 for b in BLOCKS:
  p=SHORT[b]; pathcol=f"{p}_trial_archive_path"
  if pathcol not in out: continue
  for uid,gidx in out.groupby("fov_uid").groups.items():
   idx=np.asarray(list(gidx),int); paths=out.loc[idx,pathcol].dropna().astype(str).unique()
   if not len(paths): continue
   arc=load_arc(paths[0],cache); vals,curve,resp,pref=recompute_block_from_archive(arc,fraction,rng,nperm)
   # archive contains all cell classes; map current yellow ROI rows back by suite2p ROI index
   roi=np.asarray(arc["suite2p_roi_index"],int); mp={int(r):i for i,r in enumerate(roi)}; jj=np.array([mp.get(int(r),-1) for r in out.loc[idx,"suite2p_roi_index"]])
   ok=jj>=0; ix=idx[ok]; aj=jj[ok]
   out.loc[ix,f"{p}_responsive_fdr"]=resp[aj]
   out.loc[ix,f"{p}_preferred_condition"]=pref[aj]
   out.loc[ix,f"{p}_lifetime_sparseness"]=sparse_rows(curve)[aj]; out.loc[ix,f"{p}_gini_coefficient"]=gini_rows(curve)[aj]; out.loc[ix,f"{p}_fano_factor"]=fano_rows(curve)[aj]
   for k,v in enumerate(vals):
    if b=="pure_tones": c=f"pure_response_{v:.6g}_Hz"
    elif b=="chord_tones": c=f"chord_response_middle_oct_{v:.6g}"
    else: c=f"fm_response_slope_{v:+.6g}_oct_per_s".replace("+","pos").replace("-","neg")
    out.loc[ix,c]=curve[aj,k]
   if b=="pure_tones":
    out.loc[ix,"pure_best_frequency_hz"]=pref[aj]
    out.loc[ix,"pure_fwhm_octaves"]=fwhm_log2_rows(curve,vals)[aj]
   elif b=="chord_tones":
    out.loc[ix,"chord_best_middle_octave"]=pref[aj]; out.loc[ix,"chord_best_middle_distance_from_harmonic_octave"]=np.abs(pref[aj]-1)
    if np.any(np.isclose(vals,1)):
     h=int(np.argmin(np.abs(vals-1))); rh=curve[:,h]; ro=np.nanmean(np.delete(curve,h,axis=1),axis=1); out.loc[ix,"chord_harmonic_selectivity"]=bounded(rh,ro)[aj]
   else:
    out.loc[ix,"fm_best_slope_oct_per_s"]=pref[aj]; out.loc[ix,"fm_best_abs_slope_oct_per_s"]=np.abs(pref[aj]); pos=vals>0; neg=vals<0; up=np.nanmean(curve[:,pos],axis=1); dn=np.nanmean(curve[:,neg],axis=1); out.loc[ix,"fm_direction_selectivity"]=bounded(up,dn)[aj]
    mags=np.sort(np.unique(np.abs(vals[np.abs(vals)>0]))); sm=np.full((curve.shape[0],len(mags)),np.nan)
    for kk,mag in enumerate(mags): sm[:,kk]=np.nanmean(curve[:,np.isclose(np.abs(vals),mag)],axis=1)
    out.loc[ix,"fm_speed_lifetime_sparseness"]=sparse_rows(sm)[aj]
 return out

def significant_targets(st):
 targets=[]
 def add(family,b,branch,key,r,label):
  ph=r["omnibus"].get("p_holm_family",r["omnibus"].get("p",np.nan))
  if np.isfinite(ph) and ph<.05: targets.append({"id":f"{family}::{b}::{branch}::{key}::omnibus","family":family,"block":b,"branch":branch,"key":key,"test":"omnibus","label":label,"original_p":ph})
  for pk,q in r["pairwise"].items():
   if np.isfinite(q.get("p_holm_pairs",np.nan)) and q["p_holm_pairs"]<.05: targets.append({"id":f"{family}::{b}::{branch}::{key}::{pk}","family":family,"block":b,"branch":branch,"key":key,"test":"pairwise","pair":pk,"label":label+f" — {q['area1']} vs {q['area2']}","original_p":q["p_holm_pairs"]})
 for b in BLOCKS: add("responsiveness",b,"",f"{SHORT[b]}_responsive_fdr",st["responsiveness"][b]["stats"],f"{BLOCK_LABEL[b]} responsive fraction")
 for b in BLOCKS:
  for branch in ("all_cells","responsive_only"):
   for m,rec in st["metrics"][b][branch].items(): add("metric",b,branch,m,rec["stats"],f"{BLOCK_LABEL[b]} {rec['label']} [{branch}]")
  for branch in ("all_cells","responsive_only"):
   for v,r in st["profiles"][b][branch]["stats"].items(): add("profile",b,branch,v,r,f"{BLOCK_LABEL[b]} response at condition {v} [{branch}]")
  for v,r in st["preferences"][b]["responsive_only"]["stats"].items(): add("preference",b,"responsive_only",v,r,f"{PREF[b][1]} distribution bin {v} [responsive only]")
 return targets

def target_p(st,t):
 try:
  if t["family"]=="responsiveness": r=st["responsiveness"][t["block"]]["stats"]
  elif t["family"]=="metric": r=st["metrics"][t["block"]][t["branch"]][t["key"]]["stats"]
  elif t["family"]=="profile": r=st["profiles"][t["block"]][t["branch"]]["stats"].get(t["key"])
  else: r=st["preferences"][t["block"]]["responsive_only"]["stats"].get(t["key"])
  if r is None: return np.nan
  if t["test"]=="omnibus": return float(r["omnibus"].get("p_holm_family",r["omnibus"].get("p",np.nan)))
  return float(r["pairwise"].get(t["pair"],{}).get("p_holm_pairs",np.nan))
 except (KeyError,TypeError):
  return np.nan
def safe_stem(s):
 clean=re.sub(r"[^A-Za-z0-9._-]+","_",s)
 return clean[:110]+"__"+hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]
def trial_reduction(full_yellow,full_stats,areas,out,nres,nperm,seed):
 targets=significant_targets(full_stats)
 if not targets: return {"performed":False,"reason":"No individually significant primary YELLOW results"}
 root=out/"trial_reduction_robustness"; root.mkdir(parents=True,exist_ok=True); rng=np.random.default_rng(seed); cache={}; rows=[]
 for t in targets: rows.append({"fraction":1.0,"resample":0,"target_id":t["id"],"p_adjusted":t["original_p"]})
 for frac in TRIAL_FRACTIONS[1:]:
  for rep in range(nres):
   red=reduced_yellow(full_yellow,frac,rng,nperm,cache); st=build_stats(red,areas)
   for t in targets: rows.append({"fraction":frac,"resample":rep,"target_id":t["id"],"p_adjusted":target_p(st,t)})
 raw=pd.DataFrame(rows); raw.to_csv(root/"trial_reduction_all_targets.csv",index=False)
 for t in targets:
  d=raw[raw.target_id==t["id"]]; fig,ax=plt.subplots(figsize=(8,5.5)); xs=[]; med=[]; lo=[]; hi=[]; retain=[]
  for f in TRIAL_FRACTIONS:
   v=finite(d.loc[np.isclose(d.fraction,f),"p_adjusted"]); xs.append(100*f); med.append(np.nanmedian(v) if len(v) else np.nan); lo.append(np.nanpercentile(v,10) if len(v) else np.nan); hi.append(np.nanpercentile(v,90) if len(v) else np.nan); retain.append(np.mean(v<.05) if len(v) else np.nan)
  med=np.array(med); lo=np.array(lo); hi=np.array(hi); ax.plot(xs,med,marker="o",label="median adjusted p"); ax.fill_between(xs,lo,hi,alpha=.2,label="10-90 percentile"); ax.axhline(.05,color=".5",ls="--"); ax.set_yscale("log"); ax.set_xlabel("Trials retained within each stimulus condition (%)"); ax.set_ylabel("Adjusted p value")
  desc=(("direct Mann-Whitney U; family-Holm" if len(areas)==2 else "Kruskal-Wallis omnibus; family-Holm") if t["test"]=="omnibus" else f"Mann-Whitney {t['pair']}; Holm across area pairs")
  ax.set_title(t["label"]+"\n"+desc+f" | original adjusted p={t['original_p']:.3g}"); txt="Significance retention (<0.05):\n"+"\n".join(f"{x:.0f}%: {r:.2f}" for x,r in zip(xs,retain)); ax.text(1.02,.98,txt,transform=ax.transAxes,va="top",fontsize=8); ax.legend(frameon=False); fig.subplots_adjust(right=.76); fig.savefig(root/(safe_stem(t["id"])+"__ROBUSTNESS.png"),dpi=250,bbox_inches="tight"); plt.close(fig)
 save_json(root/"targets.json",targets); return {"performed":True,"n_targets":len(targets),"output_root":str(root)}

def stats_for_json(x):
 if isinstance(x,dict): return {k:stats_for_json(v) for k,v in x.items() if k!="table"}
 if isinstance(x,list): return [stats_for_json(v) for v in x]
 return x

def write_index(out): (out/"FIGURE_INDEX.txt").write_text("\n".join(str(p.relative_to(out)) for p in sorted(out.rglob("*.png")))+"\n",encoding="utf-8")

def main():
 args=parse_args(); subject=str(args.subject); dates=[str(d) for d in args.dates]; areas=list(args.areas); root=output_root(subject,dates)
 print("="*82); print("MULTISTIM CROSS-AREA CELL-CLASS ANALYSIS v3"); print("="*82)
 for a in areas: print(a,input_csv(subject,a,dates),"FOUND" if input_csv(subject,a,dates).exists() else "MISSING")
 if args.dry_run: return
 root.mkdir(parents=True,exist_ok=True); allc=load_tables(subject,dates,areas); allc.to_csv(root/"all_areas_combined_cell_results.csv",index=False)
 save_json(root/"run_manifest.json",{"version":"v3","subject":subject,"dates":dates,"areas":areas,"primary_replicate":"FOV","trial_reduction":{"enabled":not args.skip_trial_reduction,"fractions":TRIAL_FRACTIONS,"resamples":args.trial_reduction_resamples,"all_individual_significant_primary_YELLOW_results":True}})
 for dk,(_,_,dlab) in DEPTHS.items():
  d=subset_depth(allc,dk)
  for cls in CELL_CLASSES:
   cells=d[d.cell_class==cls].copy(); out=root/dk/cls; out.mkdir(parents=True,exist_ok=True); cells.to_csv(out/"cell_results.csv",index=False)
   if cells.empty: continue
   st=build_stats(cells,areas); save_json(out/"statistics.json",stats_for_json(st))
   plot_responsiveness(cells,st,areas,cls,dlab,out)
   for b in BLOCKS:
    for branch in ("all_cells","responsive_only"):
     plot_metric_family(cells,st,b,branch,areas,cls,dlab,out); plot_profile(st,b,branch,areas,cls,dlab,out)
     plot_metric_cell_points(cells,b,branch,areas,cls,dlab,out); plot_profile_cells(cells,b,branch,areas,cls,dlab,out)
     plot_primary_selectivity_cross_area_fov(st,b,branch,areas,cls,dlab,out)
     plot_primary_selectivity_cross_area_cells(cells,b,branch,areas,cls,dlab,out)
    plot_preference(st,b,"responsive_only",areas,cls,dlab,out); plot_preference(st,b,"all_cells_descriptive",areas,cls,dlab,out)
   bfstats=plot_bf_comparison(cells,areas,cls,dlab,out); save_json(out/"best_frequency_statistics.json",stats_for_json(bfstats))
   if cls=="yellow" and not args.skip_trial_reduction:
    tr=trial_reduction(cells,st,areas,out,max(1,args.trial_reduction_resamples),max(64,args.trial_reduction_response_permutations),args.trial_reduction_seed+list(DEPTHS).index(dk)*10000); save_json(out/"trial_reduction_status.json",tr)
   write_index(out)
 if "pure_best_frequency_hz" in allc:
  bf=pd.to_numeric(allc["pure_best_frequency_hz"],errors="coerce")
  mask=allc.get("pure_responsive_fdr",pd.Series(False,index=allc.index)).fillna(False).astype(bool)&(bf>0)
  allc["pure_best_frequency_log2_hz"]=np.where(mask,np.log2(bf),np.nan)
 for cls in CELL_CLASSES:
  cc=allc[allc.cell_class==cls].copy(); plot_area_layer(cc,areas,cls,root); plot_area_layer_primary_selectivity(cc,areas,cls,root)
 print("DONE:",root)

if __name__=="__main__": main()
