#!/usr/bin/env python3
"""
Do the frequency-centered sound blocks give the same tuning curves in different FOVs / areas?

Reads only multistim stage-1 (v6/v7) outputs of one run folder: each FOV's trial archives,
fov_cell_results.csv and fov_manifest.json. One figure per block (chord_tones, fm_range,
band_noise, noise_pair), each FOV that recorded the block overlaid in its own color:

    A  population tuning curve: mean +/- SEM across the block's responsive cells (FDR, as in
       stage 1) of each cell's mean response (dF/F) per condition;
    B  shape only: each cell's curve divided by its largest |response| first; asterisks mark
       conditions where the FOVs differ (Mann-Whitney U across cells, Holm over conditions);
    C  % of responsive cells preferring each condition (argmax, as stage 1's preferred condition);
    D  the block's selectivity index (stage-1 column) per FOV, median marked; MWU + Cliff's delta;
    E  BF of the BF-eligible cells relative to the block's center frequency / chord F0, at a
       pure-tone level recorded in every FOV of the block (whether the stimulus was centered
       on the cells, which differs between FOVs if the center was chosen per FOV);
    F  stimulus parameters and cell counts per FOV.

Statistics pool cells, so they are exploratory only: the FOV is the replicate and each area /
position has one FOV here.

Example
-------
python posthoc_figures/multistim_tuning_across_fovs.py \
    /var/tmp/evan/sound_tuning_multistim_fov_analysis/imag041/A1/20261022
"""

from __future__ import annotations

import argparse
import glob
import json
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

BLOCKS = ("chord_tones", "fm_range", "band_noise", "noise_pair")
PREFIX = {"chord_tones": "chord", "fm_range": "fmr", "band_noise": "bn", "noise_pair": "np"}
TITLE = {"chord_tones": "Chords (3 tones; middle tone varied)", "fm_range": "FM sweeps, fixed range",
         "band_noise": "Band noise (8-Hz AM)", "noise_pair": "Noise pairs (A = 0.25-oct band noise, B = white noise)"}
XLABEL = {"chord_tones": "middle tone (octaves above F0)", "fm_range": "sweep slope (oct/s):   ← down  |  up →",
          "band_noise": "bandwidth (octaves)", "noise_pair": "order / gap (s)"}
SI = {"chord_tones": ("chord_harmonic_selectivity", "harmonic selectivity  $SI_{harm}$"),
      "fm_range": ("fmr_direction_selectivity", "direction selectivity  $SI_{dir}$ (up − down)"),
      "band_noise": ("bn_bandwidth_selectivity", "bandwidth selectivity  $SI_{bw}$ (wide − narrow)"),
      "noise_pair": ("np_novelty_selectivity", "novelty selectivity  $SI_{nov}$ (diff − same)")}
CENTER_KEY = {"chord_tones": ("F0_hz", "chord F0"), "fm_range": ("center_frequency_hz", "FM center"),
              "band_noise": ("center_frequency_hz", "band center"), "noise_pair": ("A_center_frequency_hz", "A center")}
NP_ORDERS = ("AB", "BA", "AA", "BB")          # code = 10 x order index + gap, as in multistim v6
# fixed per FOV position so a FOV keeps its color in every figure (validated categorical slots 1-3)
FOV_COLORS = ("#2a78d6", "#eb6834", "#1baf7a", "#8a5cd1", "#eda100")
FOV_MARKERS = ("o", "s", "^", "D", "v")

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 11, "axes.titleweight": "bold", "pdf.fonttype": 42})


def x_positions(block: str, cond: np.ndarray) -> tuple[np.ndarray, list[str], list[tuple[float, str]]]:
    """Plot positions, tick labels and group labels (noise-pair order) for a block's conditions."""
    if block == "fm_range":         # equal spacing, a gap at 0 between down and up sweeps
        k = np.arange(len(cond)) + 0.6 * (cond > 0)
        return k, [f"{c:+g}" for c in cond], []
    if block == "band_noise":
        return np.log2(cond), [f"{c:g}" for c in cond], []
    if block == "noise_pair":
        oi = np.floor(np.round(cond, 6) / 10).astype(int)
        gap = np.round(cond - 10 * oi, 6)
        pos = np.empty(len(cond))
        groups = []
        for o in np.unique(oi):
            m = oi == o
            pos[m] = o * 5 + np.argsort(np.argsort(gap[m]))
            groups.append((pos[m].mean(), NP_ORDERS[o]))
        return pos, [f"{g:g}" for g in gap], groups
    return cond.astype(float), [f"{c:.3g}" for c in cond], []


def segments(block: str, cond: np.ndarray) -> list[np.ndarray]:
    """Condition indices drawn as one connected line (down/up sweeps and noise-pair orders separate)."""
    if block == "fm_range":
        return [np.flatnonzero(cond < 0), np.flatnonzero(cond > 0)]
    if block == "noise_pair":
        oi = np.floor(np.round(cond, 6) / 10).astype(int)
        return [np.flatnonzero(oi == o) for o in np.unique(oi)]
    return [np.arange(len(cond))]


def cliffs_delta(a, b) -> float:
    a, b = np.asarray(a), np.asarray(b)
    return float((np.sign(a[:, None] - b[None, :])).mean())


def holm(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    adj = np.minimum(1, np.maximum.accumulate((n - np.arange(n)) * p[o]))
    out = np.empty(n); out[o] = adj
    return out


def load_fovs(run_dir: Path) -> list[dict]:
    fovs = []
    for k, man in enumerate(sorted(glob.glob(str(run_dir / "fov_outputs" / "*" / "fov_manifest.json")))):
        d = Path(man).parent
        m = json.loads(Path(man).read_text())
        cells = pd.read_csv(d / "fov_cell_results.csv")
        fovs.append({"uid": m["fov_uid"], "fov": int(m["FOV#"]), "dir": d, "manifest": m, "cells": cells,
                     "area": str(cells["brainArea"].iloc[0]), "color": FOV_COLORS[k % len(FOV_COLORS)],
                     "marker": FOV_MARKERS[k % len(FOV_MARKERS)]})
    if not fovs:
        raise FileNotFoundError(f"No fov_manifest.json under {run_dir}/fov_outputs")
    return fovs


def bf_columns(fov: dict, level: float) -> tuple[str, str]:
    """(BF column, eligibility column) for a pure-tone level of this FOV."""
    main = float(fov["cells"]["pure_tones_level_db"].iloc[0])
    p = "pure_" if np.isclose(level, main) else f"pure_{level:g}dB_"
    return p + "best_frequency_hz", p + "bf_eligible"


def fov_levels(fov: dict) -> list[float]:
    m = fov["manifest"]
    lv = [m["block_metadata"]["pure_tones"]["level_db"]] if "pure_tones" in m["block_metadata"] else []
    return lv + [v["level_db"] for v in m.get("other_pure_tone_levels", {}).values()]


def block_data(fov: dict, block: str) -> dict | None:
    meta = fov["manifest"]["block_metadata"].get(block)
    if meta is None:
        return None
    arc = np.load(meta["trial_archive"], allow_pickle=True)
    cond = np.asarray(arc["condition_values"], float)
    resp = np.asarray(arc["any_condition_responsive_fdr"], bool)
    R = np.asarray(arc["condition_mean_response"], float)[resp]
    peak = np.nanmax(np.abs(R), axis=1, keepdims=True)
    cells = fov["cells"].set_index("suite2p_roi_index").loc[np.asarray(arc["suite2p_roi_index"])[resp]]
    return {"meta": meta, "cond": cond, "R": R, "Rn": R / np.where(peak > 0, peak, np.nan),
            "n_cells": int(len(resp)), "n_resp": int(resp.sum()), "cells": cells,
            "si": cells[SI[block][0]].to_numpy(float), "session": meta["session"]}


def line(ax, x, y, segs, color, marker, label, se=None, lw=2):
    for k, i in enumerate(segs):
        if se is not None:
            ax.fill_between(x[i], y[i] - se[i], y[i] + se[i], color=color, alpha=0.22, lw=0)
        ax.plot(x[i], y[i], color=color, lw=lw, marker=marker, ms=6, mec="white", mew=1,
                label=label if k == 0 else None)


def band(ax, x, Y, segs, color, marker, label):
    mu = np.nanmean(Y, axis=0)
    se = np.nanstd(Y, axis=0, ddof=1) / np.sqrt(np.sum(np.isfinite(Y), axis=0))
    line(ax, x, mu, segs, color, marker, label, se)
    return mu


def style_x(ax, block, pos, ticks, groups):
    if block == "noise_pair":
        ax.set_xticks(pos); ax.set_xticklabels(ticks, fontsize=8)
        for xc, name in groups:
            ax.text(xc, -0.10, name, transform=ax.get_xaxis_transform(), ha="center", va="top",
                    fontsize=10, weight="bold")
            ax.axvspan(xc - 2, xc + 2, color="0.5", alpha=0.05 if NP_ORDERS.index(name) % 2 else 0, lw=0)
        ax.set_xlabel(XLABEL[block], labelpad=20)
    else:
        ax.set_xticks(pos); ax.set_xticklabels(ticks, fontsize=9 if block == "fm_range" else 10)
        ax.set_xlabel(XLABEL[block])
    if block == "fm_range":
        ax.axvline(np.mean(pos[[4, 5]]), color="0.75", lw=1, ls=":")
    if block == "chord_tones":
        ax.axvline(1.0, color="0.75", lw=1, ls=":")
        ax.text(1.0, 0.98, " harmonic (2·F0)", transform=ax.get_xaxis_transform(), ha="left", va="top",
                color="0.45", fontsize=9)


def make_figure(block: str, fovs: list[dict], out: Path) -> dict | None:
    data = [(f, block_data(f, block)) for f in fovs]
    data = [(f, b) for f, b in data if b is not None]
    if not data:
        return None
    cond = data[0][1]["cond"]
    assert all(np.allclose(b["cond"], cond) for _, b in data), f"{block}: conditions differ between FOVs"
    pos, ticks, groups = x_positions(block, cond)
    segs = segments(block, cond)
    lab = lambda f, b: f"FOV{f['fov']} · {f['area']} (n={b['n_resp']})"
    summary = {"block": block, "fovs": {}, "comparisons": {}}

    fig = plt.figure(figsize=(16, 9.6))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], hspace=0.45, wspace=0.28,
                          left=0.06, right=0.98, top=0.88, bottom=0.08)
    axA, axB, axC = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])
    axD, axE, axF = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1]), fig.add_subplot(gs[1, 2])

    # A, B, C: curves
    curves = {}
    for f, b in data:
        band(axA, pos, b["R"], segs, f["color"], f["marker"], lab(f, b))
        curves[f["uid"]] = band(axB, pos, b["Rn"], segs, f["color"], f["marker"], lab(f, b))
        pref = np.nanargmax(b["R"], axis=1)
        pct = 100 * np.bincount(pref, minlength=len(cond)) / len(pref)
        line(axC, pos, pct, segs, f["color"], f["marker"], lab(f, b))
        summary["fovs"][f["uid"]] = {"FOV#": f["fov"], "brainArea": f["area"], "session": b["session"],
                                     "n_cells": b["n_cells"], "n_responsive": b["n_resp"],
                                     "mean_curve": np.nanmean(b["R"], 0).round(5).tolist(),
                                     "mean_normalized_curve": np.nanmean(b["Rn"], 0).round(4).tolist(),
                                     "pct_preferring": pct.round(2).tolist(),
                                     "si_median": float(np.nanmedian(b["si"]))}
    for ax in (axA, axB, axC):
        ax.axhline(0, color="0.6", lw=0.8)
        style_x(ax, block, pos, ticks, groups)
    axA.set_title("A  Population tuning curve"); axA.set_ylabel("response (ΔF/F), mean ± SEM")
    axB.set_title("B  Shape (each cell ÷ its peak |response|)"); axB.set_ylabel("normalized response, mean ± SEM")
    axC.set_title("C  Preferred condition"); axC.set_ylabel("% of responsive cells"); axC.set_ylim(bottom=0)
    axA.legend(frameon=False, fontsize=9, loc="lower center" if block == "chord_tones" else "best")

    # B: per-condition FOV differences, shape correlation
    note = []
    if len(data) >= 2:
        for (fa, ba), (fb, bb) in combinations(data, 2):
            p = np.array([stats.mannwhitneyu(*(x[np.isfinite(x)] for x in (ba["Rn"][:, j], bb["Rn"][:, j])))[1]
                          for j in range(len(cond))])
            q = holm(p)
            r = float(np.corrcoef(curves[fa["uid"]], curves[fb["uid"]])[0, 1])
            key = f"FOV{fa['fov']}_vs_FOV{fb['fov']}"
            summary["comparisons"][key] = {"normalized_curve_pearson_r": r, "per_condition_mwu_holm_q": q.round(5).tolist()}
            note.append(f"FOV{fa['fov']} vs FOV{fb['fov']}: shape r = {r:.2f}; "
                        f"{int((q < 0.05).sum())}/{len(q)} conditions differ (q<0.05)")
            if len(data) == 2:
                lo, hi = axB.get_ylim()
                axB.set_ylim(lo, hi + 0.12 * (hi - lo))
                for j in np.flatnonzero(q < 0.05):
                    axB.text(pos[j], 0.985, "*", transform=axB.get_xaxis_transform(), ha="center",
                             va="top", fontsize=14)
        note.append("B: * q < 0.05 (MWU across cells, Holm over conditions)")

    # D: selectivity index
    sis = []
    for k, (f, b) in enumerate(data):
        s = b["si"][np.isfinite(b["si"])]; sis.append(s)
        jit = np.random.default_rng(0).uniform(-0.18, 0.18, len(s))
        axD.scatter(k + jit, s, s=9, color=f["color"], alpha=0.45, lw=0, marker=f["marker"])
        med = np.median(s)
        axD.plot([k - 0.3, k + 0.3], [med, med], color="black", lw=2.5)
        axD.text(k + 0.33, med, f"{med:+.2f}", va="center", fontsize=9)
    axD.set_xticks(range(len(data))); axD.set_xticklabels([f"FOV{f['fov']}\n{f['area']}" for f, _ in data])
    axD.axhline(0, color="0.6", lw=0.8); axD.set_ylim(-1.08, 1.15); axD.set_xlim(-0.6, len(data) - 0.2)
    axD.set_ylabel(SI[block][1]); axD.set_title("D  Selectivity index (responsive cells; bar = median)")
    if len(data) == 2:
        u = stats.mannwhitneyu(*sis)
        d = cliffs_delta(*sis)
        summary["comparisons"]["si_mwu"] = {"U": float(u.statistic), "p": float(u.pvalue), "cliffs_delta": d}
        axD.text(0.5, 1.0, f"MWU p = {u.pvalue:.2g}, Cliff's δ = {d:+.2f}", transform=axD.transAxes,
                 ha="center", va="top", fontsize=9, color="0.25")

    # E: BF relative to the block's center frequency at a pure-tone level common to all FOVs
    ckey, cname = CENTER_KEY[block]
    levels = [set(fov_levels(f)) for f, _ in data]
    common = sorted(set.intersection(*levels))
    main = [f["manifest"]["block_metadata"].get("pure_tones", {}).get("level_db") for f, _ in data]
    level = next((lv for lv in main if lv in common), common[0] if common else None)
    if level is not None:
        bins = np.arange(-4.125, 4.25, 0.25)
        for f, b in data:
            bfc, elc = bf_columns(f, level)
            c = f["cells"]
            ok = c[elc].astype(bool).to_numpy()
            off = np.log2(c[bfc].to_numpy(float)[ok] / float(b["meta"][ckey]))
            h = 100 * np.histogram(off, bins)[0] / max(len(off), 1)
            axE.stairs(h, bins, color=f["color"], lw=2,
                       label=f"FOV{f['fov']}: {cname} {b['meta'][ckey]/1000:g} kHz, median {np.median(off):+.2f} oct (n={ok.sum()})")
            summary["fovs"][f["uid"]].update({"bf_level_db": level, "center_hz": float(b["meta"][ckey]),
                                              "bf_minus_center_median_oct": float(np.median(off)),
                                              "n_bf_eligible": int(ok.sum())})
        axE.axvline(0, color="black", lw=1, ls="--")
        axE.set_xlabel(f"BF − {cname} (octaves); {level:g}-dB tones, BF-eligible cells (all, not only {PREFIX[block]}-responsive)")
        axE.set_ylabel("% of BF-eligible cells"); axE.legend(frameon=False, fontsize=8.5, loc="upper left")
        axE.set_ylim(top=axE.get_ylim()[1] * 1.35)
    axE.set_title("E  Was the stimulus centered on the cells' BFs?")

    # F: parameters
    axF.axis("off"); axF.set_title("F  Sessions and stimulus", loc="left")
    lines = []
    for f, b in data:
        m = b["meta"]
        extra = (f"{cname} {m[ckey]/1000:g} kHz" + (f", {m['octave_range']:g} oct range" if "octave_range" in m else ""))
        lines.append(f"FOV{f['fov']}  {f['area']}  session {b['session']}  {m['level_db']:g} dB\n"
                     f"    {extra};  window {m['response_window_s'][0]:g}–{m['response_window_s'][1]:g} s\n"
                     f"    {b['n_resp']} of {b['n_cells']} cells responsive (FDR); SI median {np.nanmedian(b['si']):+.2f}")
    absent = [f"FOV{f['fov']}" for f in fovs if block not in f["manifest"]["block_metadata"]]
    if absent:
        lines.append(f"Not recorded in {', '.join(absent)}.")
    lines += ["\n".join(note)] if note else []
    lines.append("Statistics pool cells within FOV: exploratory\n(one FOV per area/position; the FOV is the replicate).")
    if level is not None and level >= 75:
        lines.append(f"Panel E uses {level:g}-dB tones (only level common to these FOVs);\n"
                     "75-dB tones may be clipped — BF peaks at harmonics possible.")
    axF.text(0, 0.95, "\n\n".join(lines), transform=axF.transAxes, va="top", fontsize=9.5, family="DejaVu Sans")

    f0 = data[0][0]["manifest"]
    fig.suptitle(f"{TITLE[block]} — tuning across FOVs", fontsize=15, weight="bold", x=0.06, ha="left", y=0.975)
    fig.text(0.06, 0.93, f"{data[0][0]['cells']['subject'].iloc[0]} · {f0['date']} · responsive cells of each FOV "
             f"(any condition, BH-FDR) · color = FOV", fontsize=10.5, color="0.3")
    out.mkdir(parents=True, exist_ok=True)
    stem = out / f"{block}_tuning_across_FOVs"
    fig.savefig(stem.with_suffix(".png"), dpi=200); fig.savefig(stem.with_suffix(".pdf"))
    plt.close(fig)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path, help="multistim stage-1 folder <subject>/<area>/<date_tag>")
    ap.add_argument("--blocks", nargs="+", default=list(BLOCKS), choices=BLOCKS)
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <run_dir>/across_FOV_tuning")
    args = ap.parse_args()
    fovs = load_fovs(args.run_dir)
    out = args.out_dir or args.run_dir / "across_FOV_tuning"
    summaries = {}
    for block in args.blocks:
        s = make_figure(block, fovs, out)
        if s is None:
            print(f"{block}: not recorded in any FOV, skipped")
            continue
        summaries[block] = s
        counts = ", ".join("FOV%d n=%d" % (v["FOV#"], v["n_responsive"]) for v in s["fovs"].values())
        print(f"{block}: {counts} -> {out / (block + '_tuning_across_FOVs.png')}")
    (out / "tuning_across_FOVs_summary.json").write_text(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
