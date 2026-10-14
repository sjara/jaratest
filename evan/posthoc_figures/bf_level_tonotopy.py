#!/usr/bin/env python3
"""Post-hoc tonotopy figures for the pure-tone level series (sound_tuning_pure_tone_levels_fov_analysis_v1).

Sound level is used to recruit cells: parts of A1 with higher thresholds (e.g. the low-frequency
pole) need louder tones to reveal cells, so the map is built from all levels together.

Per cell (all definitions use the stage-1 per-level columns, so every FOV is handled the same way,
including FOVs recorded at one level only):
    threshold   lowest recorded level with a significant excitatory response (any frequency with
                q < 0.05 and mean response > 0). Censored when it equals the lowest level recorded in
                that FOV (true threshold is at or below it).
    CF          characteristic frequency: the significant excitatory frequency with the largest
                response at the threshold level.
    CF+10/+20   center frequency 10 / 20 dB above threshold: half-max centroid of the tuning curve
                (stage-1 bf_centroid_hz: log2-frequency centroid weighted by response - peak/2) at
                level threshold+10 / +20, if that level was recorded and the cell has a significant
                excitatory response there. The argmax BF at that level is kept in the CSV too.
                With 45-75 dB levels, CF+20 only exists for thresholds of 45 or 55 dB.

Figures (labeled PNG + unlabeled TIFF for the report-style ones):
    recruitment_CF_by_threshold      rows = FOVs; CF counts stacked by threshold level
    threshold_vs_CF                  threshold of each cell vs its CF, per FOV and pooled;
                                     line = lowest threshold among cells with each CF
    tonotopic_map_CF_center10_center20   ROI masks on the FOV mean image, colored by frequency;
                                         linear gradient of log2 frequency over ROI position
    tonotopic_map_BF_by_level        same, BF at each level (BF-eligible cells)
    CF_vs_center_frequency           CF vs CF+10 and CF+20 for the same cells
Tables: tonotopy_cells.csv (one row per cell), tonotopy_statistics.json.

Map orientation is the imaging frame (rows/columns of the Suite2p mean image), not cortical axes.
The gradient is a least-squares fit log2(f) ~ x + y over ROI centers (octaves per 100 pixels; pixel
size depends on magnification) with a permutation p-value (frequencies shuffled across ROIs).

Example:
    python bf_level_tonotopy.py /var/tmp/evan/sound_tuning_pure_tone_levels_fov_analysis/imag041 \
        --date 20261008 --areas A1 --fov-order A1=0,1,2,3,4
"""
import argparse
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

OCTAVE_TICKS_KHZ = [2, 4, 8, 16, 32]
FREQ_CMAP = "viridis"
N_GRADIENT_PERM = 2000


def lp(level):
    return f"pure_{level:g}dB"


def recorded_levels(cells):
    levels = sorted({float(c[len("pure_"):-len("dB_responsive_fdr")]) for c in cells.columns
                     if c.startswith("pure_") and c.endswith("dB_responsive_fdr")})
    if not levels:
        raise SystemExit("No pure_<N>dB_responsive_fdr columns: is this a level-series stage-1 output?")
    return levels


def level_colors(levels):
    cols = plt.cm.magma(np.linspace(0.18, 0.72, max(len(levels), 2)))
    return {lv: cols[i] for i, lv in enumerate(levels)}


def truthy(v):
    return bool(v) if pd.notna(v) else False


def condition_columns(cells, level):
    pat = re.compile(rf"^{lp(level)}_response_([0-9.eE+-]+)_Hz$")
    return sorted((float(m.group(1)), c) for c in cells.columns for m in [pat.match(c)] if m)


def cell_frequency_table(cells, levels):
    conds = {lv: condition_columns(cells, lv) for lv in levels}
    rows = []
    for uid, g in cells.groupby("fov_uid"):
        here = [lv for lv in levels if g[f"{lp(lv)}_responsive_fdr"].notna().all()]
        for _, r in g.iterrows():
            rec = {"fov_uid": uid, "FOV#": int(r["FOV#"]), "brainArea": r["brainArea"], "depth": r["depth"],
                   "suite2p_roi_index": int(r["suite2p_roi_index"]), "cell_class": r["cell_class"],
                   "levels_recorded_db": "+".join(f"{lv:g}" for lv in here), "lowest_level_db": min(here),
                   "responsive_any_level": any(truthy(r[f"{lp(lv)}_responsive_fdr"]) for lv in here)}
            for lv in here:
                ok = truthy(r[f"{lp(lv)}_bf_eligible"])
                rec[f"bf_{lv:g}dB_hz"] = r[f"{lp(lv)}_best_frequency_hz"] if ok else np.nan
            thr = next((lv for lv in here if truthy(r[f"{lp(lv)}_any_excitatory_condition_fdr"])), np.nan)
            rec["threshold_db"] = thr
            rec["threshold_censored"] = bool(np.isfinite(thr) and thr == min(here))
            rec["cf_hz"] = np.nan
            if np.isfinite(thr):
                freqs = np.array([f for f, _ in conds[thr]])
                resp = np.array([r[c] for _, c in conds[thr]], float)
                q = np.array([r[c.replace("_response_", "_response_q_")] for _, c in conds[thr]], float)
                sig = (q < 0.05) & (resp > 0)
                rec["cf_hz"] = freqs[np.flatnonzero(sig)[np.argmax(resp[sig])]]
            for above in (10, 20):
                lv = thr + above if np.isfinite(thr) else np.nan
                rec[f"center{above}_level_db"] = lv
                rec[f"center{above}_hz"] = rec[f"bf{above}_hz"] = np.nan
                if lv in here:
                    rec[f"center{above}_status"] = "ok" if truthy(r[f"{lp(lv)}_any_excitatory_condition_fdr"]) else "no excitatory response"
                    if rec[f"center{above}_status"] == "ok":
                        rec[f"center{above}_hz"] = r[f"{lp(lv)}_bf_centroid_hz"]
                        rec[f"bf{above}_hz"] = r[f"{lp(lv)}_best_frequency_hz"]
                else:
                    rec[f"center{above}_status"] = "no threshold" if not np.isfinite(thr) else "level not recorded"
            rows.append(rec)
    return pd.DataFrame(rows)


def fov_order(tab, fov_nums):
    info = tab.groupby("fov_uid").agg(fov_num=("FOV#", "first"), brain_area=("brainArea", "first"),
                                      median_cf=("cf_hz", "median"))
    if fov_nums is None:
        return info.sort_values(["median_cf", "fov_num"])
    by_num = info.reset_index().set_index("fov_num")
    unknown = sorted(set(fov_nums) - set(by_num.index)); missing = sorted(set(by_num.index) - set(fov_nums))
    if unknown or missing:
        raise SystemExit(f"--fov-order mismatch: unknown {unknown}, not listed {missing}")
    return by_num.loc[fov_nums].reset_index().set_index("fov_uid")


def style(ax, labelsize=13):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_linewidth(1.3)
    ax.tick_params(width=1.3, length=5, labelsize=labelsize)


def khz_xaxis(ax, freqs, labeled=True):
    x = np.log2(freqs / 1000.0); step = np.min(np.diff(x)) if len(x) > 1 else 1.0
    ax.set_xlim(x[0] - step, x[-1] + step); ax.set_xticks(np.log2(OCTAVE_TICKS_KHZ)); ax.set_xticks(x, minor=True)
    ax.tick_params(which="minor", length=3, width=1)
    ax.set_xticklabels([str(k) for k in OCTAVE_TICKS_KHZ] if labeled else [])


# ----------------------------------------------------------------------------- recruitment

def draw_recruitment(tab, order, levels, freqs, area, labeled, out_path):
    cols = level_colors(levels); x = np.log2(freqs / 1000.0); w = 0.8 * (np.min(np.diff(x)) if len(x) > 1 else 1)
    fig, axes = plt.subplots(len(order), 1, figsize=(11, 2.4 * len(order) + 1.4), sharex=True, squeeze=False)
    for ax, (uid, row) in zip(axes[:, 0], order.iterrows()):
        style(ax); g = tab[(tab.fov_uid == uid) & tab.cf_hz.notna()]
        bottom = np.zeros(len(freqs))
        for lv in levels:
            n = np.array([np.sum(np.isclose(g.loc[g.threshold_db == lv, "cf_hz"], f)) for f in freqs])
            if n.sum():
                ax.bar(x, n, width=w, bottom=bottom, color=cols[lv], label=f"{lv:g} dB (n={int(n.sum())})")
            bottom += n
        ax.set_ylim(0, max(1, bottom.max()) * 1.15)
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=3, integer=True))
        if labeled:
            only = g.levels_recorded_db.iloc[0] if len(g) else ""
            note = f"  ·  levels {only} dB" if "+" not in str(only) else ""
            ax.set_title(f"FOV {int(row.fov_num)}  ·  {row.brain_area}  ·  {len(g)} cells with a CF{note}", fontsize=13, loc="left")
            ax.legend(frameon=False, fontsize=9.5, loc="upper left", bbox_to_anchor=(1.01, 1.0), title="threshold", title_fontsize=9.5)
        else:
            ax.tick_params(labelleft=False)
    khz_xaxis(axes[-1, 0], freqs, labeled)
    if labeled:
        axes[-1, 0].set_xlabel("Characteristic frequency (kHz)", fontsize=15)
        fig.supylabel("Cells (count)", fontsize=15)
        fig.suptitle(f"{area}: CF of each cell, stacked by the level at which it first responds\n"
                     "(threshold at the lowest recorded level means at or below it)", fontsize=14)
        fig.tight_layout(); fig.savefig(out_path, dpi=300)
    else:
        fig.tight_layout(); fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


# ----------------------------------------------------------------------------- threshold vs CF

def threshold_vs_cf(tab, order, levels, freqs, area, out_path):
    multi = [uid for uid in order.index if "+" in str(tab.loc[tab.fov_uid == uid, "levels_recorded_db"].iloc[0])]
    panels = multi + ["pooled"]
    fig, axes = plt.subplots(1, len(panels), figsize=(4.3 * len(panels), 4.8), sharey=True, squeeze=False)
    rng = np.random.default_rng(3); out = {"note": "Spearman rho between CF (log2) and threshold; censored thresholds "
                                                   "kept at the lowest level (ties)"}
    for ax, uid in zip(axes[0], panels):
        style(ax, 11)
        g = tab[tab.cf_hz.notna() & (tab.fov_uid.isin(multi) if uid == "pooled" else (tab.fov_uid == uid))]
        lx = np.log2(g.cf_hz.to_numpy(float) / 1000); ty = g.threshold_db.to_numpy(float); cen = g.threshold_censored.to_numpy(bool)
        jx = lx + rng.uniform(-.06, .06, len(g)); jy = ty + rng.uniform(-1.6, 1.6, len(g))
        ax.scatter(jx[~cen], jy[~cen], s=16, color="0.25", alpha=.6, edgecolors="none", label="threshold")
        ax.scatter(jx[cen], jy[cen], s=16, facecolors="none", edgecolors="0.35", alpha=.7, lw=.8, label="at or below lowest level")
        mins = [(np.log2(f / 1000), g.loc[np.isclose(g.cf_hz, f), "threshold_db"].min()) for f in freqs if np.any(np.isclose(g.cf_hz, f))]
        if mins:
            ax.step([m[0] for m in mins], [m[1] for m in mins], where="mid", color="tab:red", lw=1.8, label="lowest threshold at each CF")
        rho, p = (stats.spearmanr(lx, ty) if len(g) > 2 and np.ptp(ty) > 0 else (np.nan, np.nan))
        out[uid] = {"n_cells": int(len(g)), "spearman_rho": float(rho), "p": float(p),
                    "unit": "cells (pooled across FOVs; exploratory)" if uid == "pooled" else "cells within this FOV"}
        lab = "pooled FOVs" if uid == "pooled" else f"FOV {int(order.loc[uid, 'fov_num'])} · {order.loc[uid, 'brain_area']}"
        ax.set_title(f"{lab}\nrho={rho:.2f}, p={p:.3g}, n={len(g)}", fontsize=11)
        khz_xaxis(ax, freqs); ax.set_xlabel("CF (kHz)")
    axes[0, 0].set_yticks(levels); axes[0, 0].set_ylabel("Threshold (dB SPL)")
    axes[0, 0].set_ylim(min(levels) - 5, max(levels) + 5); axes[0, 0].legend(frameon=False, fontsize=8, loc="upper right")
    fig.suptitle(f"{area}: response threshold vs characteristic frequency (FOVs with more than one level)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, .93]); fig.savefig(out_path, dpi=250); plt.close(fig)
    return out


# ----------------------------------------------------------------------------- maps

def load_fov_geometry(area_dir, uid):
    man = json.loads((area_dir / "fov_outputs" / uid / "fov_manifest.json").read_text())
    sdir = Path(man["suite2p_reference_dir"])
    ops = np.load(sdir / "ops.npy", allow_pickle=True).item()
    stat = np.load(sdir / "stat.npy", allow_pickle=True)
    return np.asarray(ops["meanImg"], float), stat


def gradient_fit(xy, logf, rng):
    """Least-squares log2 f ~ a + b x + c y; permutation p for R^2 (frequencies shuffled across ROIs)."""
    if len(logf) < 6:
        return None
    X = np.column_stack([np.ones(len(logf)), xy])
    coef, *_ = np.linalg.lstsq(X, logf, rcond=None)
    def r2(y):
        c, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ c
        return 1 - res.var() / y.var() if y.var() > 0 else np.nan
    obs = r2(logf)
    null = np.array([r2(rng.permutation(logf)) for _ in range(N_GRADIENT_PERM)])
    p = (1 + np.sum(null >= obs)) / (N_GRADIENT_PERM + 1)
    gx, gy = coef[1], coef[2]
    return {"n": int(len(logf)), "r2": float(obs), "perm_p": float(p),
            "oct_per_100px": float(100 * np.hypot(gx, gy)), "direction_deg_image": float(np.degrees(np.arctan2(gy, gx))),
            "gx": float(gx), "gy": float(gy)}


def draw_map(ax, img, stat, g, col, vmin, vmax, labeled, rng, show_gradient):
    lo, hi = np.nanpercentile(img, [1, 99.5])
    ax.imshow(img, cmap="gray", vmin=lo, vmax=hi)
    over = np.zeros(img.shape + (4,))
    cmap = plt.get_cmap(FREQ_CMAP); norm = matplotlib.colors.Normalize(vmin, vmax)
    xy, lf = [], []
    for _, r in g.iterrows():
        st = stat[int(r.suite2p_roi_index)]; yp = np.asarray(st["ypix"], int); xp = np.asarray(st["xpix"], int)
        v = r[col]
        if np.isfinite(v):
            over[yp, xp] = cmap(norm(np.log2(v / 1000)))
            over[yp, xp, 3] = .9
            xy.append([st["med"][1], st["med"][0]]); lf.append(np.log2(v / 1000))
        else:
            over[yp, xp] = (1, 1, 1, .28)
    ax.imshow(over); ax.set_xticks([]); ax.set_yticks([])
    fit = gradient_fit(np.asarray(xy, float), np.asarray(lf, float), rng) if show_gradient else None
    if fit and labeled:
        cy, cx = img.shape[0] / 2, img.shape[1] / 2; L = .3 * min(img.shape)
        u = np.array([fit["gx"], fit["gy"]]); u = u / (np.hypot(*u) or 1)
        ax.annotate("", xy=(cx + L * u[0], cy + L * u[1]), xytext=(cx - L * u[0], cy - L * u[1]),
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=2.2))
        ax.text(.02, .02, f"{fit['oct_per_100px']:.2f} oct/100 px\nR²={fit['r2']:.2f}, p={fit['perm_p']:.3g}, n={fit['n']}",
                transform=ax.transAxes, color="white", fontsize=8.5, va="bottom",
                bbox=dict(facecolor="black", alpha=.45, lw=0, pad=2))
    elif labeled:
        n = int(np.isfinite(g[col]).sum())
        ax.text(.02, .02, f"n={n}", transform=ax.transAxes, color="white", fontsize=8.5, va="bottom",
                bbox=dict(facecolor="black", alpha=.45, lw=0, pad=2))
    return fit


def draw_map_grid(tab, order, area_dir, cols, col_titles, freqs, area, labeled, out_path, suptitle):
    vmin, vmax = np.log2(freqs[0] / 1000), np.log2(freqs[-1] / 1000)
    fig, axes = plt.subplots(len(order), len(cols), figsize=(3.6 * len(cols) + 1.6, 3.6 * len(order) + 1.0), squeeze=False)
    rng = np.random.default_rng(11); fits = {}
    for r_, (uid, row) in enumerate(order.iterrows()):
        img, stat = load_fov_geometry(area_dir, uid); g = tab[tab.fov_uid == uid]
        for c_, col in enumerate(cols):
            ax = axes[r_, c_]
            m = re.match(r"bf_([0-9.]+)dB_hz$", col)
            if m and m.group(1) not in str(g.levels_recorded_db.iloc[0]).split("+"):   # level not recorded in this FOV
                ax.axis("off")
                if labeled: ax.text(.5, .5, "not recorded", ha="center", va="center", color="0.5", transform=ax.transAxes)
                continue
            fits[f"{uid}|{col}"] = draw_map(ax, img, stat, g, col, vmin, vmax, labeled, rng, show_gradient=True)
            if labeled and r_ == 0: ax.set_title(col_titles[c_], fontsize=13, fontweight="bold")
        if labeled:
            axes[r_, 0].set_ylabel(f"FOV {int(row.fov_num)}\n{row.brain_area}", fontsize=12)
            axes[r_, 0].yaxis.set_visible(True)
    sm = matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin, vmax), cmap=FREQ_CMAP)
    if labeled:
        fig.tight_layout(rect=[0, 0, .9, .95])
        cax = fig.add_axes([.92, .25, .018, .5]); cb = fig.colorbar(sm, cax=cax)
        cb.set_ticks(np.log2(OCTAVE_TICKS_KHZ)); cb.set_ticklabels([str(k) for k in OCTAVE_TICKS_KHZ]); cb.set_label("kHz")
        fig.suptitle(suptitle, fontsize=13); fig.savefig(out_path, dpi=300)
    else:
        fig.tight_layout(); fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
    return fits


# ----------------------------------------------------------------------------- CF vs center

def cf_vs_center(tab, freqs, area, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))
    rng = np.random.default_rng(5); out = {}
    lo, hi = np.log2(freqs[0] / 1000) - .3, np.log2(freqs[-1] / 1000) + .3
    fovs = sorted(tab.fov_uid.unique()); cmap = plt.get_cmap("tab10")
    for ax, above in zip(axes, (10, 20)):
        style(ax, 11); g = tab[tab.cf_hz.notna() & tab[f"center{above}_hz"].notna()]
        for k, uid in enumerate(fovs):
            s = g[g.fov_uid == uid]
            if len(s):
                ax.scatter(np.log2(s.cf_hz / 1000) + rng.uniform(-.06, .06, len(s)), np.log2(s[f"center{above}_hz"] / 1000),
                           s=16, alpha=.7, color=cmap(k % 10), edgecolors="none", label=f"FOV {int(s['FOV#'].iloc[0])} (n={len(s)})")
        ax.plot([lo, hi], [lo, hi], color="0.6", ls="--", lw=1); ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
        for setter in (ax.set_xticks, ax.set_yticks): setter(np.log2(OCTAVE_TICKS_KHZ))
        ax.set_xticklabels(OCTAVE_TICKS_KHZ); ax.set_yticklabels(OCTAVE_TICKS_KHZ)
        d = np.log2(g[f"center{above}_hz"] / g.cf_hz)
        r = stats.wilcoxon(d) if len(d) > 1 and np.any(d != 0) else None
        out[f"center{above}_minus_cf_oct"] = {"n": int(len(d)), "median": float(np.median(d)) if len(d) else np.nan,
                                             "pooled_wilcoxon_p_exploratory": float(r.pvalue) if r else np.nan}
        ax.set_title(f"{above} dB above threshold\nmedian (center − CF) = {out[f'center{above}_minus_cf_oct']['median']:+.2f} oct, n={len(d)}", fontsize=11)
        ax.set_xlabel("CF (kHz)"); ax.set_ylabel(f"Center frequency at threshold + {above} dB (kHz)")
        ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle(f"{area}: CF vs center frequency above threshold (same cells)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, .94]); fig.savefig(out_path, dpi=250); plt.close(fig)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subject_dir", type=Path, help="level-series stage-1 output folder for one subject (contains A1/, ...)")
    ap.add_argument("--date", required=True)
    ap.add_argument("--areas", nargs="+", default=["A1"])
    ap.add_argument("--fov-order", nargs="+", default=[], metavar="AREA=FOV,FOV,...")
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <run folder>/posthoc_figures/bf_levels_tonotopy")
    args = ap.parse_args()
    fov_orders = {k: [int(v) for v in vals.split(",")] for k, vals in (item.split("=", 1) for item in args.fov_order)}
    out_dir = args.out_dir or args.subject_dir.parent.parent / "posthoc_figures" / "bf_levels_tonotopy"
    out_dir.mkdir(parents=True, exist_ok=True)
    all_stats = {}
    for area in args.areas:
        area_dir = args.subject_dir / area / args.date
        cells = pd.read_csv(area_dir / "combined" / "combined_cell_results.csv")
        levels = recorded_levels(cells)
        freqs = np.array(sorted({f for lv in levels for f, _ in condition_columns(cells, lv)}))
        tab = cell_frequency_table(cells, levels)
        subject = cells["subject"].iloc[0]; nums = fov_orders.get(area)
        order = fov_order(tab, nums)
        stem = f"{subject}_{args.date}_{area}"; suffix = "" if nums is None else "_FOVorder_" + "_".join(map(str, nums))
        tab.to_csv(out_dir / f"{stem}_tonotopy_cells.csv", index=False)

        summary = []
        for uid, g in tab.groupby("fov_uid"):
            summary.append({"fov_uid": uid, "FOV#": int(g["FOV#"].iloc[0]), "levels": g.levels_recorded_db.iloc[0],
                            "n_cells": len(g), "n_responsive_any_level": int(g.responsive_any_level.sum()),
                            "n_with_CF": int(g.cf_hz.notna().sum()), "n_with_center10": int(g.center10_hz.notna().sum()),
                            "n_with_center20": int(g.center20_hz.notna().sum()),
                            **{f"n_threshold_{lv:g}dB": int((g.threshold_db == lv).sum()) for lv in levels},
                            "median_CF_khz": float(g.cf_hz.median() / 1000) if g.cf_hz.notna().any() else np.nan})
        summary = pd.DataFrame(summary); summary.to_csv(out_dir / f"{stem}_tonotopy_FOV_summary.csv", index=False)
        print(summary.to_string(index=False))

        for labeled, ext in ((True, "_labeled.png"), (False, "_unlabeled.tif")):
            draw_recruitment(tab, order, levels, freqs, area, labeled, out_dir / f"{stem}_recruitment_CF_by_threshold{suffix}{ext}")
        st = {"levels_db": levels, "fov_order_top_to_bottom": [int(r.fov_num) for _, r in order.iterrows()]}
        st["threshold_vs_CF"] = threshold_vs_cf(tab, order, levels, freqs, area, out_dir / f"{stem}_threshold_vs_CF{suffix}.png")
        cols = ["cf_hz", "center10_hz", "center20_hz"]
        titles = ["CF (at threshold)", "Center freq., threshold + 10 dB", "Center freq., threshold + 20 dB"]
        for labeled, ext in ((True, "_labeled.png"), (False, "_unlabeled.tif")):
            fits = draw_map_grid(tab, order, area_dir, cols, titles, freqs, area, labeled,
                                 out_dir / f"{stem}_tonotopic_map_CF_center10_center20{suffix}{ext}",
                                 f"{area}: tonotopic map per FOV (gray = cells without a value; arrow = direction of increasing frequency)")
        st["gradients_CF_center"] = fits
        lcols = [f"bf_{lv:g}dB_hz" for lv in levels]
        for c in lcols:
            if c not in tab: tab[c] = np.nan
        for labeled, ext in ((True, "_labeled.png"), (False, "_unlabeled.tif")):
            fits = draw_map_grid(tab, order, area_dir, lcols, [f"BF at {lv:g} dB" for lv in levels], freqs, area, labeled,
                                 out_dir / f"{stem}_tonotopic_map_BF_by_level{suffix}{ext}",
                                 f"{area}: BF at each level (BF-eligible cells; gray = not BF-eligible or not recorded)")
        st["gradients_BF_by_level"] = fits
        st["CF_vs_center"] = cf_vs_center(tab, freqs, area, out_dir / f"{stem}_CF_vs_center_frequency.png")
        all_stats[area] = st
    (out_dir / "tonotopy_statistics.json").write_text(json.dumps(all_stats, indent=2, default=lambda o: None if o is None else str(o)))
    print(f"Wrote figures to {out_dir}")


if __name__ == "__main__":
    main()
