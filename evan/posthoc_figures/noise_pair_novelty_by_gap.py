#!/usr/bin/env python3
"""
Noise-pair figure: does the preceding sound change the response to the second sound, at each gap?

Reads only multistim v6 stage-1 noise-pair trial archives. For each FOV (one row):
    * population mean traces (noise-pair responsive cells) of AB, BA, AA, BB at the gaps where the
      second sound is resolvable in time (default 0.4 and 0.8 s), with the sound times marked;
    * the novelty contrast R_diff - R_same = mean(AB, BA) - mean(AA, BB) at every gap, with a 95%
      CI computed across TRIALS: each trial's response is first averaged over the cells, so
      trial-to-trial fluctuations shared by all cells are part of the error (a CI across cells
      would ignore them and be too narrow). Shown in dF/F and as % of the mean pair response.
      The gray band is +/- --equivalence-pct of the mean pair response, a smallest effect of
      interest: a CI entirely inside it supports "no effect larger than that".

The design gives one scalar per trial for both sounds, so the effect of A on B alone is not
identifiable (4 orders, 6 unknowns); the contrast tests whether the second response depends on
the second sound being different from or the same as the first. Under linear summation the
first-sound responses cancel in it.

Example
-------
python posthoc_figures/noise_pair_novelty_by_gap.py \
    /var/tmp/evan/sound_tuning_multistim_fov_analysis/imag041/A1/20261015
"""

from __future__ import annotations

import argparse
import glob
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ORDERS = ("A_then_B", "B_then_A", "A_then_A", "B_then_B")   # code = 10 * index + gap, as in multistim v6
SHORT = {"A_then_B": "AB", "B_then_A": "BA", "A_then_A": "AA", "B_then_B": "BB"}
COLORS = {"A_then_B": "tab:blue", "B_then_A": "tab:orange", "A_then_A": "tab:blue", "B_then_B": "tab:orange"}
STYLES = {"A_then_B": "-", "B_then_A": "-", "A_then_A": "--", "B_then_B": "--"}


def decode(code):
    c = np.round(np.asarray(code, float), 6)
    oi = np.floor(c / 10).astype(int)
    return oi, np.round(c - 10 * oi, 6)


def contrast_by_gap(arc: dict, cells: np.ndarray) -> list[dict]:
    """Trial-level novelty contrast per gap from the population-mean trial response."""
    valid = arc["valid_trial_mask"].astype(bool)
    pop = np.nanmean(arc["trial_response"][cells], axis=0)           # one value per trial
    oi, gap = decode(arc["trial_condition_value"])
    rows = []
    for g in np.unique(gap[valid]):
        means, var_terms, all_pairs = {}, 0.0, []
        for k, o in enumerate(ORDERS):
            x = pop[valid & (oi == k) & np.isclose(gap, g)]; x = x[np.isfinite(x)]
            means[o] = x.mean(); all_pairs.append(x)
            var_terms += (0.5 ** 2) * x.var(ddof=1) / len(x)            # each side is a mean of 2 orders
        con = 0.5 * (means["A_then_B"] + means["B_then_A"]) - 0.5 * (means["A_then_A"] + means["B_then_B"])
        se = np.sqrt(var_terms); ref = np.mean(np.concatenate(all_pairs))
        rows.append({"gap": float(g), "contrast": con, "ci": 1.96 * se, "mean_pair": ref,
                     "n_trials": int(sum(len(x) for x in all_pairs)), **{SHORT[o]: means[o] for o in ORDERS}})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path, help="multistim stage-1 folder <subject>/<area>/<date_tag>")
    ap.add_argument("--trace-gaps", nargs="+", type=float, default=[0.4, 0.8])
    ap.add_argument("--equivalence-pct", type=float, default=20.0, help="+/- band, %% of the mean pair response")
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <run_dir>/combined/selectivity_plots/noise_pair")
    args = ap.parse_args()
    arcs = sorted(glob.glob(str(args.run_dir / "fov_outputs" / "*" / "*_noise_pair_trial_response_archive_v2.npz")))
    if not arcs:
        raise FileNotFoundError(f"No noise-pair archives under {args.run_dir}/fov_outputs")
    out = args.out_dir or args.run_dir / "combined" / "selectivity_plots" / "noise_pair"
    out.mkdir(parents=True, exist_ok=True)
    ncol = len(args.trace_gaps) + 1
    fig, axes = plt.subplots(len(arcs), ncol, figsize=(4.6 * ncol, 3.6 * len(arcs)), squeeze=False)
    lines = []
    for r, path in enumerate(arcs):
        with np.load(path, allow_pickle=False) as z:
            arc = {k: z[k] for k in z.files}
        fov = Path(path).parent.name
        cells = arc["any_condition_responsive_fdr"].astype(bool)
        t = arc["tvec"].astype(float); vals = arc["condition_values"]; voi, vgap = decode(vals)
        tm = arc["condition_trace_mean"][cells]                          # cells x conditions x time
        # Each sound lasts (pair duration - gap) / 2.
        _, tgap = decode(arc["trial_condition_value"])
        dur = float(np.nanmedian((arc["trial_sound_duration_s"] - tgap) / 2))
        ylim = [np.inf, -np.inf]
        for c, g in enumerate(args.trace_gaps):
            ax = axes[r, c]
            for k, o in enumerate(ORDERS):
                j = np.flatnonzero((voi == k) & np.isclose(vgap, g))
                if not len(j): continue
                y = np.nanmean(tm[:, j[0], :], axis=0)
                ax.plot(t, y, STYLES[o], color=COLORS[o], lw=1.8, label=SHORT[o])
                ylim = [min(ylim[0], np.nanmin(y)), max(ylim[1], np.nanmax(y))]
            for on in (0.0, dur + g):
                ax.axvspan(on, on + dur, color="0.8", alpha=.6, lw=0, zorder=0)
            ax.axhline(0, color="0.6", lw=.7, ls=":")
            ax.set_title(f"{fov} | gap {g:g} s (n={cells.sum()} cells)", fontsize=9)
            ax.set_xlabel("Time from first sound (s)"); ax.set_ylabel("dF/F (baseline-subtracted)")
            ax.spines[["top", "right"]].set_visible(False)
            if r == 0 and c == 0: ax.legend(frameon=False, fontsize=8, title="solid = different, dashed = same", title_fontsize=7)
        for c in range(len(args.trace_gaps)):
            axes[r, c].set_ylim(ylim[0] - .1 * (ylim[1] - ylim[0]), ylim[1] + .1 * (ylim[1] - ylim[0]))
        ax = axes[r, -1]; rows = contrast_by_gap(arc, cells)
        gaps = np.array([x["gap"] for x in rows]); x = np.log2(gaps)
        con = np.array([x_["contrast"] for x_ in rows]); ci = np.array([x_["ci"] for x_ in rows])
        ref = np.mean([x_["mean_pair"] for x_ in rows]); eq = ref * args.equivalence_pct / 100
        ax.axhspan(-eq, eq, color="0.88", lw=0, zorder=0, label=f"±{args.equivalence_pct:g}% of mean response")
        ax.errorbar(x, con, yerr=ci, fmt="o", color="black", capsize=4, zorder=3)
        ax.axhline(0, color="0.5", lw=.8)
        ax.set_xticks(x); ax.set_xticklabels([f"{g:g}" for g in gaps]); ax.set_xlabel("Gap (s)")
        ax.set_ylabel("R_diff − R_same (dF/F)")
        sec = ax.secondary_yaxis("right", functions=(lambda v: 100 * v / ref, lambda p: p * ref / 100))
        sec.set_ylabel("% of mean pair response")
        ax.set_title(f"Novelty contrast, 95% CI across trials\nmean pair response {ref:.3f} dF/F", fontsize=9)
        ax.spines[["top"]].set_visible(False)
        if r == 0: ax.legend(frameon=False, fontsize=7, loc="upper right")
        for x_ in rows:
            lines.append(f"{fov} gap {x_['gap']:g} s: contrast {x_['contrast']:+.4f} ± {x_['ci']:.4f} dF/F "
                         f"({100*x_['contrast']/ref:+.0f}% ± {100*x_['ci']/ref:.0f}% of mean), trials {x_['n_trials']} | "
                         + " ".join(f"{k}={x_[k]:.3f}" for k in ("AB", "BA", "AA", "BB")))
    fig.suptitle("Noise pairs: second sound different (AB, BA) vs same (AA, BB) as the first — responsive cells", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, .97])
    png = out / "noise_pair_novelty_contrast_by_gap.png"
    fig.savefig(png, dpi=220); plt.close(fig)
    (out / "noise_pair_novelty_contrast_by_gap.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print(f"Wrote {png}")


if __name__ == "__main__":
    main()
