#!/usr/bin/env python3
"""Post-hoc report figure: stacked per-FOV best-frequency histograms, one file per area.

Rebuilds the top (count) panel of stage 1's best_frequency_histogram_counts_and_fraction.png
for every FOV from combined/combined_cell_results.csv (pure-tone FDR-responsive cells only,
same counting as _save_pure_bf_histograms). FOVs are stacked with the lowest median BF on top
and the highest at the bottom (ties broken by mean log2 BF). Writes a labeled PNG and an
unlabeled TIFF (no text) per area. --fov-order AREA=5,6,7,8 sets the top-to-bottom order explicitly
instead (e.g. nominal tonotopic position from info2p); those files get an _FOVorder_<list> suffix.

Example:
    python bf_histogram_stack.py \
        /path/to/sound_tuning_multistim_dualF0_fov_analysis/imag039 --date 20260924
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

CLASS_COLORS = {"green": "tab:green", "yellow": "goldenrod"}
CLASS_ORDER = ["green", "yellow"]
OCTAVE_TICKS_KHZ = [2, 4, 8, 16, 32]


def tested_frequencies_hz(area_dir):
    """Pure-tone condition values from the first stage-1 trial archive of this area."""
    archives = sorted(glob.glob(str(area_dir / "fov_outputs" / "*" / "*pure_tones*archive*.npz")))
    if not archives:
        raise FileNotFoundError(f"No pure-tone trial archive under {area_dir}")
    with np.load(archives[0], allow_pickle=False) as z:
        return np.asarray(z["condition_values"], float)


def ordered_fovs(use):
    """FOVs sorted low -> high by median BF, then mean log2 BF."""
    stats = (use.assign(log2_bf=np.log2(use["pure_best_frequency_hz"]))
                .groupby("fov_uid")
                .agg(median_bf=("pure_best_frequency_hz", "median"), mean_log2=("log2_bf", "mean"),
                     fov_num=("FOV#", "first"), brain_area=("brainArea", "first")))
    return stats.sort_values(["median_bf", "mean_log2"])


def explicit_order(use, fov_nums):
    """FOVs in the given FOV# order (top -> bottom); every FOV with responsive cells must be listed."""
    stats = ordered_fovs(use).reset_index().set_index("fov_num")
    missing = sorted(set(stats.index) - set(fov_nums))
    unknown = sorted(set(fov_nums) - set(stats.index))
    if missing or unknown:
        raise SystemExit(f"--fov-order mismatch: not listed {missing}, no responsive cells/unknown {unknown}")
    return stats.loc[fov_nums].reset_index().set_index("fov_uid")


def draw_area(use, freqs_hz, area, labeled, out_path, fov_nums=None):
    order = ordered_fovs(use) if fov_nums is None else explicit_order(use, fov_nums)
    n = len(order)
    x = np.log2(freqs_hz / 1000.0)
    step = np.min(np.diff(x))
    bar_w = 0.42 * step
    fig, axes = plt.subplots(n, 1, figsize=(8, 2.3 * n + 1.2), sharex=True, squeeze=False)
    axes = axes[:, 0]
    for ax, (fov_uid, row) in zip(axes, order.iterrows()):
        g = use[use["fov_uid"] == fov_uid]
        ymax = 0
        for cls, offset in zip(CLASS_ORDER, (-0.5 * bar_w, 0.5 * bar_w)):
            arr = g.loc[g["cell_class"] == cls, "pure_best_frequency_hz"].to_numpy(float)
            counts = np.array([np.sum(np.isclose(arr, v)) for v in freqs_hz])
            ymax = max(ymax, counts.max())
            ax.bar(x + offset, counts, width=bar_w, color=CLASS_COLORS[cls],
                   label=f"{cls.upper()} (n={len(arr)})")
        ax.set_ylim(0, max(1, ymax) * 1.12)
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=3, integer=True))
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_linewidth(1.5)
        ax.tick_params(width=1.5, length=6, labelsize=18)
        if labeled:
            subfield = "" if fov_nums is None else f"  ·  {row.brain_area}"
            ax.set_title(f"FOV {int(row.fov_num)}{subfield}  ·  median BF {row.median_bf / 1000:.3g} kHz",
                         fontsize=18, loc="left", pad=6)
            ax.legend(frameon=False, fontsize=15, loc="upper right", handlelength=1.2)
        else:
            ax.tick_params(labelleft=False, labelbottom=False)
    axes[-1].set_xlim(x[0] - step, x[-1] + step)
    axes[-1].set_xticks(np.log2(OCTAVE_TICKS_KHZ))
    axes[-1].set_xticks(x, minor=True)
    axes[-1].tick_params(which="minor", length=3, width=1)
    if labeled:
        axes[-1].set_xticklabels([str(k) for k in OCTAVE_TICKS_KHZ])
        axes[-1].set_xlabel("Best frequency (kHz)", fontsize=20)
        fig.supylabel("Responsive cells (count)", fontsize=20)
        order_note = "(low → high)" if fov_nums is None else "(FOV order " + ", ".join(map(str, fov_nums)) + ")"
        fig.suptitle(f"{area}: best frequency per FOV {order_note}", fontsize=22)
        fig.tight_layout()
        fig.savefig(out_path, dpi=300)
    else:
        fig.tight_layout()
        fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
    return order


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subject_dir", type=Path, help="stage-1 output folder for one subject (contains A1/, AAF/, ...)")
    ap.add_argument("--date", required=True, help="date tag folder, e.g. 20260924")
    ap.add_argument("--areas", nargs="+", default=["A1", "AAF"])
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="default: <run folder>/posthoc_figures/best_frequency_stacks")
    ap.add_argument("--fov-order", nargs="+", default=[], metavar="AREA=FOV,FOV,...",
                    help="explicit top-to-bottom FOV# order for an area, e.g. AAF=5,6,7,8")
    args = ap.parse_args()
    fov_orders = {k: [int(v) for v in vals.split(",")]
                  for k, vals in (item.split("=", 1) for item in args.fov_order)}

    out_dir = args.out_dir or args.subject_dir.parent.parent / "posthoc_figures" / "best_frequency_stacks"
    out_dir.mkdir(parents=True, exist_ok=True)
    provenance = {"subject_dir": str(args.subject_dir), "date": args.date, "areas": {}}
    for area in args.areas:
        area_dir = args.subject_dir / area / args.date
        cells = pd.read_csv(area_dir / "combined" / "combined_cell_results.csv")
        bf = pd.to_numeric(cells["pure_best_frequency_hz"], errors="coerce")
        use = cells[cells["pure_responsive_fdr"].fillna(False).astype(bool) & bf.notna()].copy()
        use["pure_best_frequency_hz"] = bf[use.index]
        freqs = tested_frequencies_hz(area_dir)
        fov_nums = fov_orders.get(area)
        stem = f"{cells['subject'].iloc[0]}_{args.date}_{area}_BF_histograms_by_FOV"
        if fov_nums is not None:
            stem += "_FOVorder_" + "_".join(map(str, fov_nums))
        order = draw_area(use, freqs, area, True, out_dir / f"{stem}_labeled.png", fov_nums)
        draw_area(use, freqs, area, False, out_dir / f"{stem}_unlabeled.tif", fov_nums)
        provenance["areas"][stem] = [
            {"fov_uid": uid, "FOV#": int(r.fov_num), "brainArea": r.brain_area,
             "median_bf_khz": round(r.median_bf / 1000, 4),
             "n_green": int(((use.fov_uid == uid) & (use.cell_class == "green")).sum()),
             "n_yellow": int(((use.fov_uid == uid) & (use.cell_class == "yellow")).sum())}
            for uid, r in order.iterrows()]
        print(f"{area}: top -> bottom = {[int(r.fov_num) for _, r in order.iterrows()]}")
    prov_path = out_dir / "figure_provenance.json"
    if prov_path.exists():  # keep entries from earlier runs (e.g. the default-order files)
        old = json.loads(prov_path.read_text())
        provenance["areas"] = {**old.get("areas", {}), **provenance["areas"]}
    prov_path.write_text(json.dumps(provenance, indent=2))
    print(f"Wrote figures to {out_dir}")


if __name__ == "__main__":
    main()
