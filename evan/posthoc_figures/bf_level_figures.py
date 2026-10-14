#!/usr/bin/env python3
"""Post-hoc report figures for the pure-tone level series (sound_tuning_pure_tone_levels_fov_analysis_v1).

Level-aware versions of bf_histogram_stack.py and bf_example_cells_grid.py, one set per area:

1. BF histograms: rows = FOVs, columns = levels. GREEN/YELLOW counts per tested frequency.
   --cells responsive (default; same counting as bf_histogram_stack.py) or bf_eligible
   (responsive, response at BF > 0, q < 0.05 at BF). Levels an FOV was not recorded at are
   left blank.
2. Example cells: rows = FOVs, columns = low / medium / high BF, chosen at --pick-level
   (default: highest level) with the bf_example_cells_grid.py rule (excited, q < 0.05 at BF,
   strongest cell at the lowest / median-inner / highest BF; no cell used twice). Each panel
   overlays that cell's tuning curve (mean +/- SEM) at every level recorded in its FOV, with
   a dotted line at each level's BF where the cell is BF-eligible.

FOV order (top -> bottom): --fov-order AREA=0,1,2,3, or by median BF at --pick-level.
Each figure is written as a labeled PNG and an unlabeled TIFF (no text). Use make_wiki_pngs.py for wiki copies.

Example:
    python bf_level_figures.py \
        /path/to/sound_tuning_pure_tone_levels_fov_analysis/imag041 --date 20261008 --areas A1 \
        --fov-order A1=0,1,2,3,4
"""
import argparse
import glob
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

CLASS_COLORS = {"green": "tab:green", "yellow": "goldenrod"}
CLASS_ORDER = ["green", "yellow"]
OCTAVE_TICKS_KHZ = [2, 4, 8, 16, 32]
COLUMNS = ["low", "medium", "high"]


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


def as_bool(s):
    return s.fillna(False).astype(bool)


def selected_cells(cells, level, mode):
    p = lp(level)
    bf = pd.to_numeric(cells[f"{p}_best_frequency_hz"], errors="coerce")
    flag = as_bool(cells[f"{p}_bf_eligible" if mode == "bf_eligible" else f"{p}_responsive_fdr"])
    return cells[flag & bf.notna()]


def load_archives(area_dir, fov_uid):
    out = {}
    for path in sorted(glob.glob(str(area_dir / "fov_outputs" / fov_uid / "*_pure_tones_*dB_trial_response_archive_levels_v1.npz"))):
        with np.load(path, allow_pickle=False) as z:
            out[float(z["level_db"])] = {k: z[k] for k in ["suite2p_roi_index", "trial_response", "trial_condition_value",
                                                          "valid_trial_mask", "condition_values"]}
    if not out:
        raise FileNotFoundError(f"No level archives for {fov_uid} under {area_dir}")
    return out


def tested_frequencies(archives):
    return np.asarray(next(iter(archives.values()))["condition_values"], float)


def fov_order(cells, pick_level, fov_nums):
    stats_ = (cells.groupby("fov_uid").agg(fov_num=("FOV#", "first"), brain_area=("brainArea", "first")))
    ref = selected_cells(cells, pick_level, "responsive")
    stats_["median_bf"] = ref.groupby("fov_uid")[f"{lp(pick_level)}_best_frequency_hz"].median()
    if fov_nums is None:
        return stats_.sort_values(["median_bf", "fov_num"])
    by_num = stats_.reset_index().set_index("fov_num")
    unknown = sorted(set(fov_nums) - set(by_num.index))
    missing = sorted(set(by_num.index) - set(fov_nums))
    if unknown or missing:
        raise SystemExit(f"--fov-order mismatch: unknown {unknown}, not listed {missing}")
    return by_num.loc[fov_nums].reset_index().set_index("fov_uid")


def style(ax, labelsize=15):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_linewidth(1.5)
    ax.tick_params(width=1.5, length=6, labelsize=labelsize)


def draw_histograms(cells, levels, freqs_hz, order, area, mode, labeled, out_path):
    x = np.log2(freqs_hz / 1000.0); step = np.min(np.diff(x)); bar_w = 0.42 * step
    n, m = len(order), len(levels)
    fig, axes = plt.subplots(n, m, figsize=(4.6 * m, 2.3 * n + 1.4), sharex=True, squeeze=False)
    ymax_row = {}
    for r, (uid, row) in enumerate(order.iterrows()):
        g_fov = cells[cells.fov_uid == uid]
        for c, lv in enumerate(levels):
            ax = axes[r, c]; style(ax)
            if g_fov[f"{lp(lv)}_responsive_fdr"].isna().all():
                ax.axis("off")
                if labeled:
                    ax.text(.5, .5, "not recorded", ha="center", va="center", color="0.5", fontsize=13, transform=ax.transAxes)
                continue
            g = selected_cells(g_fov, lv, mode)
            for cls, offset in zip(CLASS_ORDER, (-0.5 * bar_w, 0.5 * bar_w)):
                arr = g.loc[g["cell_class"] == cls, f"{lp(lv)}_best_frequency_hz"].to_numpy(float)
                counts = np.array([np.sum(np.isclose(arr, v)) for v in freqs_hz])
                ymax_row[r] = max(ymax_row.get(r, 0), counts.max())
                ax.bar(x + offset, counts, width=bar_w, color=CLASS_COLORS[cls], label=f"{cls.upper()} n={len(arr)}")
            ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=3, integer=True))
            if labeled:
                ax.legend(frameon=False, fontsize=10, loc="upper right", handlelength=1.0)
            else:
                ax.tick_params(labelleft=False, labelbottom=False)
    for r in range(n):  # same y scale across levels within an FOV, so levels compare directly
        for ax in axes[r]:
            if ax.axison: ax.set_ylim(0, max(1, ymax_row.get(r, 1)) * 1.15)
    for c, lv in enumerate(levels):
        ax = axes[-1, c]
        ax.set_xlim(x[0] - step, x[-1] + step); ax.set_xticks(np.log2(OCTAVE_TICKS_KHZ)); ax.set_xticks(x, minor=True)
        ax.tick_params(which="minor", length=3, width=1)
        if labeled:
            # Tick labels go on the lowest panel drawn in this column (lower FOVs may lack this level).
            shown = [a for a in axes[:, c] if a.axison]
            if shown:
                shown[-1].tick_params(labelbottom=True)
                shown[-1].set_xticklabels([str(k) for k in OCTAVE_TICKS_KHZ])
            axes[0, c].set_title(f"{lv:g} dB SPL", fontsize=18, fontweight="bold")
    if labeled:
        for r, (uid, row) in enumerate(order.iterrows()):
            axes[r, 0].set_ylabel(f"FOV {int(row.fov_num)}\n{row.brain_area}", fontsize=13)
        fig.supxlabel("Best frequency (kHz)", fontsize=18)
        what = "FDR-responsive" if mode == "responsive" else "BF-eligible"
        fig.suptitle(f"{area}: best frequency per FOV and level ({what} cells; counts)", fontsize=20)
        fig.tight_layout(); fig.savefig(out_path, dpi=300)
    else:
        fig.tight_layout(); fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


def candidates(cells, level):
    p = lp(level)
    use = cells[as_bool(cells[f"{p}_responsive_fdr"]) & as_bool(cells[f"{p}_excited_fdr"])
                & pd.to_numeric(cells[f"{p}_best_frequency_hz"], errors="coerce").notna()].copy()
    return use[pd.to_numeric(use[f"{p}_q_at_bf"], errors="coerce") < 0.05]


def pick_cells(fov_cells, level):
    """Same rule as bf_example_cells_grid.py, at one level."""
    bfcol, rcol = f"{lp(level)}_best_frequency_hz", f"{lp(level)}_preferred_response"
    bfs = np.sort(fov_cells[bfcol].to_numpy(float))
    inner = bfs[(bfs > bfs[0] * 1.001) & (bfs < bfs[-1] * 0.999)]
    mid_pool = inner if len(inner) else bfs
    targets = {"low": bfs[0], "high": bfs[-1], "medium": mid_pool[(len(mid_pool) - 1) // 2]}
    ranked = fov_cells.sort_values(rcol, ascending=False)
    picked, used = {}, set()
    for col in ["low", "high", "medium"]:
        pool = ranked[np.isclose(ranked[bfcol], targets[col]) & ~ranked["suite2p_roi_index"].isin(used)]
        picked[col] = None if pool.empty else pool.iloc[0]
        if not pool.empty:
            used.add(pool.iloc[0]["suite2p_roi_index"])
    return picked


def tuning_curve(arc, roi):
    i = int(np.flatnonzero(np.asarray(arc["suite2p_roi_index"], int) == int(roi))[0])
    vals = np.asarray(arc["condition_values"], float)
    tr = np.asarray(arc["trial_response"], float)[i]
    cond = np.asarray(arc["trial_condition_value"], float); valid = np.asarray(arc["valid_trial_mask"], bool)
    means, sems = [], []
    for v in vals:
        z = tr[valid & np.isclose(cond, v, rtol=1e-8, atol=1e-10)]; z = z[np.isfinite(z)]
        means.append(np.mean(z) if len(z) else np.nan); sems.append(stats.sem(z) if len(z) > 1 else np.nan)
    return vals, np.array(means), np.array(sems)


def draw_examples(area, rows, levels, pick_level, labeled, out_path):
    cols = level_colors(levels)
    n = len(rows)
    fig, axes = plt.subplots(n, 3, figsize=(15, 3.2 * n + 1.6), squeeze=False)
    for r, row in enumerate(rows):
        for c, col in enumerate(COLUMNS):
            ax = axes[r, c]; style(ax)
            cell = row["picks"][col]
            if cell is None:
                ax.axis("off")
                if labeled:
                    ax.text(.5, .5, "no remaining cell", ha="center", va="center", fontsize=15, color="0.4", transform=ax.transAxes)
                continue
            ax.axhline(0, color="0.6", ls="--", lw=1)
            for lv in sorted(row["archives"]):
                vals, means, sems = tuning_curve(row["archives"][lv], cell["suite2p_roi_index"])
                x = np.log2(vals / 1000.0)
                ax.errorbar(x, means, yerr=sems, marker="o", ms=4, lw=2, capsize=2, color=cols[lv], label=f"{lv:g} dB")
                if bool(cell.get(f"{lp(lv)}_bf_eligible", False)) and pd.notna(cell.get(f"{lp(lv)}_bf_eligible")):
                    ax.axvline(np.log2(cell[f"{lp(lv)}_best_frequency_hz"] / 1000.0), color=cols[lv], ls=":", lw=1.5)
            ax.set_xlim(x[0] - 0.3, x[-1] + 0.3); ax.set_xticks(np.log2(OCTAVE_TICKS_KHZ)); ax.set_xticks(x, minor=True)
            ax.tick_params(which="minor", length=3, width=1); ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=3))
            if labeled:
                ax.set_xticklabels([str(k) for k in OCTAVE_TICKS_KHZ])
                ax.set_title(f"ROI {int(cell['suite2p_roi_index'])} · {str(cell['cell_class']).upper()}"
                             f" · BF@{pick_level:g} dB {cell[f'{lp(pick_level)}_best_frequency_hz'] / 1000:.3g} kHz", fontsize=11.5)
            else:
                ax.tick_params(which="both", labelleft=False, labelbottom=False)
        if labeled:
            axes[r, 0].annotate(f"FOV {row['fov_num']}\n{row['brain_area']}", xy=(-0.31, 0.5), xycoords="axes fraction",
                                ha="right", va="center", fontsize=17, fontweight="bold")
    if labeled:
        for c, col in enumerate(COLUMNS):
            axes[0, c].annotate(f"{col.capitalize()} BF", xy=(0.5, 1.32), xycoords="axes fraction",
                                ha="center", va="bottom", fontsize=19, fontweight="bold")
        handles = [matplotlib.lines.Line2D([], [], color=cols[lv], marker="o", lw=2, label=f"{lv:g} dB") for lv in levels]
        fig.supxlabel("Frequency (kHz)", fontsize=19); fig.supylabel("Mean response (dF/F)", fontsize=19)
        fig.suptitle(f"{area}: example tuning across levels (cells picked at {pick_level:g} dB; dotted = BF at each level)", fontsize=18)
        fig.tight_layout(rect=[0.1, 0, 0.98, 0.93])
        fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.55, 0.955), ncol=len(levels), frameon=False, fontsize=13)
        fig.savefig(out_path, dpi=300)
    else:
        fig.tight_layout(); fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subject_dir", type=Path, help="level-series stage-1 output folder for one subject (contains A1/, ...)")
    ap.add_argument("--date", required=True, help="date tag folder, e.g. 20261008")
    ap.add_argument("--areas", nargs="+", default=["A1"])
    ap.add_argument("--fov-order", nargs="+", default=[], metavar="AREA=FOV,FOV,...")
    ap.add_argument("--pick-level", type=float, default=None, help="level used to pick example cells and default FOV order")
    ap.add_argument("--cells", choices=["responsive", "bf_eligible"], default="responsive", help="cells counted in the histograms")
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <run folder>/posthoc_figures/bf_levels")
    args = ap.parse_args()
    fov_orders = {k: [int(v) for v in vals.split(",")] for k, vals in (item.split("=", 1) for item in args.fov_order)}
    out_dir = args.out_dir or args.subject_dir.parent.parent / "posthoc_figures" / "bf_levels"
    out_dir.mkdir(parents=True, exist_ok=True)

    chosen = []; provenance = {"subject_dir": str(args.subject_dir), "date": args.date, "cells": args.cells, "areas": {}}
    for area in args.areas:
        area_dir = args.subject_dir / area / args.date
        cells = pd.read_csv(area_dir / "combined" / "combined_cell_results.csv")
        levels = recorded_levels(cells)
        pick = args.pick_level if args.pick_level is not None else levels[-1]
        if pick not in levels:
            raise SystemExit(f"--pick-level {pick:g} not in recorded levels {levels}")
        nums = fov_orders.get(area)
        order = fov_order(cells, pick, nums)
        subject = cells["subject"].iloc[0]
        suffix = "" if nums is None else "_FOVorder_" + "_".join(map(str, nums))
        archives = {uid: load_archives(area_dir, uid) for uid in order.index}
        freqs = tested_frequencies(next(iter(archives.values())))

        stem = f"{subject}_{args.date}_{area}_BF_histograms_by_FOV_and_level_{args.cells}{suffix}"
        draw_histograms(cells, levels, freqs, order, area, args.cells, True, out_dir / f"{stem}_labeled.png")
        draw_histograms(cells, levels, freqs, order, area, args.cells, False, out_dir / f"{stem}_unlabeled.tif")

        cand = candidates(cells, pick); rows = []
        for uid, orow in order.iterrows():
            fc = cand[cand.fov_uid == uid]
            picks = pick_cells(fc, pick) if len(fc) else {c: None for c in COLUMNS}
            rows.append({"fov_num": int(orow.fov_num), "brain_area": orow.brain_area, "picks": picks, "archives": archives[uid]})
            for col, cell in picks.items():
                rec = {"area": area, "FOV#": int(orow.fov_num), "fov_uid": uid, "column": col, "pick_level_db": pick,
                       "suite2p_roi_index": None if cell is None else int(cell["suite2p_roi_index"]),
                       "cell_class": None if cell is None else cell["cell_class"], "n_candidates_in_fov": len(fc)}
                for lv in levels:
                    ok = cell is not None and pd.notna(cell.get(f"{lp(lv)}_bf_eligible")) and bool(cell.get(f"{lp(lv)}_bf_eligible"))
                    rec[f"bf_khz_{lv:g}dB"] = cell[f"{lp(lv)}_best_frequency_hz"] / 1000 if ok else None
                rec["bf_level_slope_oct_per_10dB"] = None if cell is None else cell.get("bf_level_slope_oct_per_10dB")
                chosen.append(rec)
        stem2 = f"{subject}_{args.date}_{area}_example_tuning_across_levels_low_med_high_BF_at{pick:g}dB{suffix}"
        draw_examples(area, rows, levels, pick, True, out_dir / f"{stem2}_labeled.png")
        draw_examples(area, rows, levels, pick, False, out_dir / f"{stem2}_unlabeled.tif")
        provenance["areas"][area] = {"levels_db": levels, "pick_level_db": pick,
                                     "fov_order_top_to_bottom": [int(r.fov_num) for _, r in order.iterrows()],
                                     "files": [stem, stem2]}
        print(f"{area}: FOV order top -> bottom = {provenance['areas'][area]['fov_order_top_to_bottom']}")
    pd.DataFrame(chosen).to_csv(out_dir / "chosen_example_cells.csv", index=False)
    (out_dir / "figure_provenance.json").write_text(json.dumps(provenance, indent=2))
    print(pd.DataFrame(chosen).to_string(index=False))
    print(f"Wrote figures to {out_dir}")


if __name__ == "__main__":
    main()
