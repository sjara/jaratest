#!/usr/bin/env python3
"""Post-hoc report figure: example pure-tone tuning curves, one row per FOV, low/medium/high BF columns.

For each FOV, candidate cells are pure-tone FDR-responsive, excited, and significant (q < 0.05) at
their own best frequency (BF = argmax of the tuning curve, as in stage 1). Columns are relative to
that FOV's candidates:
    low    = lowest BF present
    medium = median BF of the candidates whose BF lies strictly between low and high
             (median of all candidates if there are none, e.g. only two distinct BFs)
    high   = highest BF present
and each panel shows the strongest-responding (largest response at BF) candidate at that BF.
A cell is never used twice; if medium coincides with low or high, it takes the next-strongest cell
at that BF, and the panel is left empty if none remains. Tuning curves are mean +/- SEM of the
per-trial response scalar from the stage-1 pure-tone trial archive, coloured by cell class.

Writes a labeled PNG and an unlabeled TIFF (no text) per area, plus a CSV of the chosen cells.

Example:
    python bf_example_cells_grid.py /path/to/sound_tuning_multistim_dualF0_fov_analysis/imag039 \
        --date 20260924 --fov-order A1=0,1,2,3 AAF=8,7,6,5
"""
import argparse
import glob
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

CLASS_COLORS = {"green": "tab:green", "yellow": "goldenrod"}
OCTAVE_TICKS_KHZ = [2, 4, 8, 16, 32]
COLUMNS = ["low", "medium", "high"]


def q_at_bf(row):
    col = f"pure_response_q_{row['pure_best_frequency_hz']:g}_Hz"
    return row.get(col, np.nan)


def candidates(cells):
    bf = pd.to_numeric(cells["pure_best_frequency_hz"], errors="coerce")
    use = cells[cells["pure_responsive_fdr"].fillna(False).astype(bool)
                & cells["pure_excited_fdr"].fillna(False).astype(bool) & bf.notna()].copy()
    use["q_at_bf"] = use.apply(q_at_bf, axis=1)
    return use[use["q_at_bf"] < 0.05]


def pick_cells(fov_cells):
    """Return {column: row or None} for one FOV."""
    bfs = np.sort(fov_cells["pure_best_frequency_hz"].to_numpy(float))
    inner = bfs[(bfs > bfs[0] * 1.001) & (bfs < bfs[-1] * 0.999)]
    mid_pool = inner if len(inner) else bfs
    targets = {"low": bfs[0], "high": bfs[-1], "medium": mid_pool[(len(mid_pool) - 1) // 2]}
    ranked = fov_cells.sort_values("pure_preferred_response", ascending=False)
    picked, used = {}, set()
    for col in ["low", "high", "medium"]:  # extremes first; medium yields on ties
        pool = ranked[np.isclose(ranked["pure_best_frequency_hz"], targets[col])
                      & ~ranked["suite2p_roi_index"].isin(used)]
        picked[col] = None if pool.empty else pool.iloc[0]
        if not pool.empty:
            used.add(pool.iloc[0]["suite2p_roi_index"])
    return picked


def load_archive(area_dir, fov_uid):
    hits = sorted(glob.glob(str(area_dir / "fov_outputs" / fov_uid / "*pure_tones*archive*.npz")))
    if not hits:
        raise FileNotFoundError(f"No pure-tone archive for {fov_uid} under {area_dir}")
    with np.load(hits[0], allow_pickle=False) as z:
        return {k: z[k] for k in ["suite2p_roi_index", "trial_response", "trial_condition_value",
                                  "valid_trial_mask", "condition_values"]}


def tuning_curve(arc, roi):
    i = int(np.flatnonzero(np.asarray(arc["suite2p_roi_index"], int) == int(roi))[0])
    vals = np.asarray(arc["condition_values"], float)
    tr = np.asarray(arc["trial_response"], float)[i]
    cond = np.asarray(arc["trial_condition_value"], float)
    valid = np.asarray(arc["valid_trial_mask"], bool)
    means, sems = [], []
    for v in vals:
        z = tr[valid & np.isclose(cond, v, rtol=1e-8, atol=1e-10)]
        z = z[np.isfinite(z)]
        means.append(np.mean(z) if len(z) else np.nan)
        sems.append(stats.sem(z) if len(z) > 1 else np.nan)
    return vals, np.array(means), np.array(sems)


def draw(area, rows, labeled, out_path):
    n = len(rows)
    fig, axes = plt.subplots(n, 3, figsize=(15, 3.2 * n + 1.4), squeeze=False)
    for r, row in enumerate(rows):
        for c, col in enumerate(COLUMNS):
            ax = axes[r, c]
            cell = row["picks"][col]
            ax.spines[["top", "right"]].set_visible(False)
            ax.spines[["left", "bottom"]].set_linewidth(1.5)
            ax.tick_params(width=1.5, length=6, labelsize=15)
            if cell is None:
                ax.axis("off")
                if labeled:
                    ax.text(0.5, 0.5, "no remaining cell", ha="center", va="center",
                            fontsize=15, color="0.4", transform=ax.transAxes)
                continue
            vals, means, sems = tuning_curve(row["archive"], cell["suite2p_roi_index"])
            x = np.log2(vals / 1000.0)
            color = CLASS_COLORS.get(str(cell["cell_class"]), "0.25")
            ax.axhline(0, color="0.6", ls="--", lw=1)
            ax.axvline(np.log2(cell["pure_best_frequency_hz"] / 1000.0), color="0.6", ls=":", lw=1.5)
            ax.errorbar(x, means, yerr=sems, marker="o", ms=5, lw=2.2, capsize=3, color=color)
            ax.set_xlim(x[0] - 0.3, x[-1] + 0.3)
            ax.set_xticks(np.log2(OCTAVE_TICKS_KHZ))
            ax.set_xticks(x, minor=True)
            ax.tick_params(which="minor", length=3, width=1)
            ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=3))
            if labeled:
                ax.set_xticklabels([str(k) for k in OCTAVE_TICKS_KHZ])
                ax.set_title(f"ROI {int(cell['suite2p_roi_index'])} · {str(cell['cell_class']).upper()}"
                             f" · {cell['pure_best_frequency_hz'] / 1000:.3g} kHz", fontsize=14)
            else:
                ax.tick_params(which="both", labelleft=False, labelbottom=False)
        if labeled:
            axes[r, 0].annotate(f"FOV {row['fov_num']}\n{row['brain_area']}", xy=(-0.31, 0.5),
                                xycoords="axes fraction", ha="right", va="center", fontsize=17,
                                fontweight="bold")
    if labeled:
        for c, col in enumerate(COLUMNS):
            axes[0, c].annotate(f"{col.capitalize()} BF", xy=(0.5, 1.32), xycoords="axes fraction",
                                ha="center", va="bottom", fontsize=19, fontweight="bold")
        fig.supxlabel("Frequency (kHz)", fontsize=19)
        fig.supylabel("Mean response (dF/F)", fontsize=19)
        fig.suptitle(f"{area}: example pure-tone tuning by FOV (mean ± SEM; dotted line = BF)", fontsize=21)
        fig.tight_layout(rect=[0.1, 0, 0.99, 0.97])
        fig.savefig(out_path, dpi=300)
    else:
        fig.tight_layout()
        fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subject_dir", type=Path, help="stage-1 output folder for one subject (contains A1/, AAF/, ...)")
    ap.add_argument("--date", required=True)
    ap.add_argument("--fov-order", nargs="+", required=True, metavar="AREA=FOV,FOV,...",
                    help="areas and their top-to-bottom FOV# order, e.g. A1=0,1,2,3 AAF=8,7,6,5")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="default: <run folder>/posthoc_figures/bf_example_cells")
    args = ap.parse_args()
    out_dir = args.out_dir or args.subject_dir.parent.parent / "posthoc_figures" / "bf_example_cells"
    out_dir.mkdir(parents=True, exist_ok=True)

    chosen = []
    for item in args.fov_order:
        area, nums = item.split("=", 1)
        fov_nums = [int(v) for v in nums.split(",")]
        area_dir = args.subject_dir / area / args.date
        cells = pd.read_csv(area_dir / "combined" / "combined_cell_results.csv")
        cand = candidates(cells)
        rows = []
        for num in fov_nums:
            fc = cand[cand["FOV#"] == num]
            if fc.empty:
                raise SystemExit(f"{area} FOV {num}: no candidate cells")
            fov_uid = fc["fov_uid"].iloc[0]
            picks = pick_cells(fc)
            rows.append({"fov_num": num, "brain_area": fc["brainArea"].iloc[0], "picks": picks,
                         "archive": load_archive(area_dir, fov_uid)})
            for col, cell in picks.items():
                chosen.append({"area": area, "FOV#": num, "fov_uid": fov_uid, "column": col,
                               "suite2p_roi_index": None if cell is None else int(cell["suite2p_roi_index"]),
                               "cell_class": None if cell is None else cell["cell_class"],
                               "bf_khz": None if cell is None else cell["pure_best_frequency_hz"] / 1000,
                               "response_at_bf": None if cell is None else cell["pure_preferred_response"],
                               "q_at_bf": None if cell is None else cell["q_at_bf"],
                               "n_candidates_in_fov": len(fc)})
        stem = (f"{cells['subject'].iloc[0]}_{args.date}_{area}_example_tuning_low_med_high_BF"
                f"_FOVorder_{'_'.join(map(str, fov_nums))}")
        draw(area, rows, True, out_dir / f"{stem}_labeled.png")
        draw(area, rows, False, out_dir / f"{stem}_unlabeled.tif")
        print(f"{area}: wrote {stem}")
    pd.DataFrame(chosen).to_csv(out_dir / "chosen_example_cells.csv", index=False)
    print(pd.DataFrame(chosen).to_string(index=False))


if __name__ == "__main__":
    main()
