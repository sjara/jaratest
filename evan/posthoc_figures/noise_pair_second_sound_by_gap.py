#!/usr/bin/env python3
"""
Noise pairs: does the response to B depend on whether it was preceded by A, as a function of gap?

For each FOV this compares three B responses, in the same B-driven cells:
    B alone   B as the FIRST sound (BA and BB trials; the previous sound ended >= 1.4 s earlier):
              mean over [0, W) after B onset. Reference: B not preceded by a sound.
    B | A     the second sound of AB at gap g: mean over [t2, t2 + W) of (trial trace - A1 template)
    B | B     the second sound of BB at gap g: mean over [t2, t2 + W) of (trial trace - B1 template)
t2 = sound duration + gap is the second sound's onset, W = --window (default 0.4 s).

The first-sound template (A1 or B1) is the mean trace of all trials that start with that sound at
the longest gap, where nothing else is played until t2 = 0.9 s (sounds are frozen, so the first
sound is the same waveform on every trial). Subtracting it removes the first sound's response and
its decay (assumes the two responses add). The template is valid until the longest-gap second
sound starts (--template-valid-until, default 0.9 s); later samples, needed only at the longest
gap, are extrapolated linearly from the template's last 0.4 s and are marked in the figure.

Cells: noise-pair FDR-responsive cells whose B-alone response is positive and significant
(one-sample t-test across B-first trials, p < 0.05). Each trial's traces are averaged over those
cells before any statistics, and 95% CIs are bootstrapped over TRIALS (condition trials and
template trials resampled together), so trial-to-trial noise shared by the cells is included.

Reads the multistim v6 noise-pair archives (cell list) and reloads each noise-pair session's
imaging and behavior (single-trial traces are not in the archive). Uses multistim v6's alignment
and condition helpers so the trials match stage 1 exactly.

Example
-------
python posthoc_figures/noise_pair_second_sound_by_gap.py \
    /var/tmp/evan/sound_tuning_multistim_fov_analysis/imag041/A1/20261015
"""

from __future__ import annotations

import argparse
import glob
import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from jaratoolbox import twophotonanalysis

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("_multistim_v6", HERE.parent / "sound_tuning_multistim_fov_analysis_v6.py")
ms = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ms)

AB, BA, AA, BB = (ms.NOISEPAIR_ORDERS.index(o) for o in ("A_then_B", "B_then_A", "A_then_A", "B_then_B"))


def trial_traces(arc: dict, plane: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """Baseline-subtracted single-trial traces (cells x trials x time) aligned as in stage 1."""
    subject, date, session = (str(arc[k]) for k in ("subject", "date", "session"))
    d = twophotonanalysis.TwoPhoton(subject, date, session, plane, paradigm=ms.PARADIGM)
    roi = np.asarray(arc["suite2p_roi_index"], int)
    ev_all, tvec, valid = d.event_locked_average(time_range=list(ms.TIME_RANGE), dff=True)
    bdata = d.bdata
    cond, _ = ms._block_condition_values("noise_pair", bdata)
    ev, valid, _, _ = ms.align_imaging_events_to_behavior(
        np.asarray(ev_all[roi], float), valid, np.asarray(d.event_onset), float(d.srate),
        ms._trial_sound_duration("noise_pair", bdata), np.asarray(bdata["ISI"], float), len(cond))
    t = np.asarray(tvec, float)
    base = (t >= ms.BASELINE_RANGE[0]) & (t < ms.BASELINE_RANGE[1])
    ev = ev - np.nanmean(ev[:, :, base], axis=2)[:, :, None]
    ev[:, ~np.asarray(valid, bool), :] = np.nan
    if not np.allclose(cond, arc["trial_condition_value"], equal_nan=True):
        raise ValueError(f"{session}: trial conditions differ from the stage-1 archive")
    sound = float(np.nanmedian(np.asarray(bdata["noisepair_sound_duration"], float)))
    return ev, t, np.asarray(cond, float), {"session": session, "sound_duration": sound}


def window_mask(t: np.ndarray, start: float, width: float) -> np.ndarray:
    # Frame times are frame starts; include frames starting in [start, start + width).
    return (t >= start - 1e-6) & (t < start + width - 1e-6)


def extend_template(tpl: np.ndarray, t: np.ndarray, valid_until: float) -> tuple[np.ndarray, np.ndarray]:
    """Template valid for t < valid_until; later samples extrapolated linearly from the last 0.4 s."""
    out = tpl.copy(); ok = t < valid_until - 1e-6
    fit = ok & (t >= valid_until - 0.4 - 1e-6) & (t >= 0)
    if fit.sum() >= 2:
        k, b = np.polyfit(t[fit], tpl[fit], 1)
        out[~ok] = k * t[~ok] + b
    return out, ~ok


def analyze_fov(pop: np.ndarray, t: np.ndarray, oi: np.ndarray, gap: np.ndarray, info: dict, args, rng) -> dict:
    """pop: trials x time (mean over selected cells)."""
    gaps = np.sort(np.unique(gap[np.isfinite(gap)])); gmax = gaps[-1]; sd = info["sound_duration"]
    ok = np.all(np.isfinite(pop), axis=1)
    idx = {(o, g): np.flatnonzero(ok & (oi == o) & np.isclose(gap, g)) for o in range(4) for g in gaps}
    b_first = np.flatnonzero(ok & np.isin(oi, [BA, BB]))
    tplA_tr = np.r_[idx[(AB, gmax)], idx[(AA, gmax)]]; tplB_tr = np.r_[idx[(BA, gmax)], idx[(BB, gmax)]]
    w0 = window_mask(t, 0.0, args.window)

    def estimates(sel):
        """sel: dict of trial index arrays (possibly resampled). Returns B-alone, B|A(g), B|B(g)."""
        tA, extrap = extend_template(np.nanmean(pop[sel["tplA"]], 0), t, args.template_valid_until)
        tB, _ = extend_template(np.nanmean(pop[sel["tplB"]], 0), t, args.template_valid_until)
        alone = np.nanmean(pop[sel["bfirst"]][:, w0])
        ba, bb = [], []
        for g in gaps:
            w = window_mask(t, sd + g, args.window)
            ba.append(np.nanmean((pop[sel[(AB, g)]] - tA)[:, w]))
            bb.append(np.nanmean((pop[sel[(BB, g)]] - tB)[:, w]))
        return alone, np.array(ba), np.array(bb), extrap

    sel0 = {"tplA": tplA_tr, "tplB": tplB_tr, "bfirst": b_first, **{(o, g): idx[(o, g)] for o in (AB, BB) for g in gaps}}
    alone, ba, bb, extrap = estimates(sel0)
    boots = []
    for _ in range(args.n_boot):
        # Resample each trial set independently. At the longest gap the AB/BB trials also enter the
        # templates, but only through samples before that gap's response window.
        sel = {k: rng.choice(v, len(v), replace=True) for k, v in sel0.items()}
        boots.append(estimates(sel)[:3])
    A_ = np.array([b[0] for b in boots]); BA_ = np.array([b[1] for b in boots]); BB_ = np.array([b[2] for b in boots])
    ci = lambda x: np.percentile(x, [2.5, 97.5], axis=0)
    diff = ba - bb; D_ = BA_ - BB_
    p_diff = np.array([2 * min(np.mean(D_[:, k] <= 0), np.mean(D_[:, k] >= 0)) for k in range(len(gaps))])
    p_vs_alone = np.array([2 * min(np.mean((BA_[:, k] - A_) <= 0), np.mean((BA_[:, k] - A_) >= 0)) for k in range(len(gaps))])
    extrap_gaps = [float(g) for g in gaps if np.any(window_mask(t, sd + g, args.window) & extrap)]
    return {"gaps": gaps, "alone": alone, "alone_ci": ci(A_), "B_after_A": ba, "B_after_A_ci": ci(BA_),
            "B_after_B": bb, "B_after_B_ci": ci(BB_), "diff": diff, "diff_ci": ci(D_), "p_diff": np.minimum(p_diff, 1),
            "p_B_after_A_vs_alone": np.minimum(p_vs_alone, 1),
            "ratio_after_A": ba / alone, "ratio_after_A_ci": ci(BA_ / A_[:, None]),
            "ratio_after_B": bb / alone, "ratio_after_B_ci": ci(BB_ / A_[:, None]),
            "n_trials": {f"{ms.NOISEPAIR_SHORT[ms.NOISEPAIR_ORDERS[o]]}_{g:g}": int(len(idx[(o, g)])) for o in (AB, BB) for g in gaps},
            "extrapolated_template_gaps": extrap_gaps,
            "tplA": extend_template(np.nanmean(pop[tplA_tr], 0), t, args.template_valid_until)[0],
            "tplB": extend_template(np.nanmean(pop[tplB_tr], 0), t, args.template_valid_until)[0]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path, help="multistim stage-1 folder <subject>/<area>/<date_tag>")
    ap.add_argument("--window", type=float, default=0.4, help="response window after each sound onset (s)")
    ap.add_argument("--template-valid-until", type=float, default=0.9,
                    help="first-sound template is measured (not extrapolated) before this time (s)")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--plane", type=int, default=0)
    ap.add_argument("--seed", type=int, default=20261021)
    ap.add_argument("--out-dir", type=Path, default=None, help="default: <run_dir>/combined/selectivity_plots/noise_pair")
    args = ap.parse_args()
    paths = sorted(glob.glob(str(args.run_dir / "fov_outputs" / "*" / "*_noise_pair_trial_response_archive_v2.npz")))
    if not paths:
        raise FileNotFoundError(f"No noise-pair archives under {args.run_dir}/fov_outputs")
    out = args.out_dir or args.run_dir / "combined" / "selectivity_plots" / "noise_pair"; out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    fig, axes = plt.subplots(len(paths), 3, figsize=(15, 3.9 * len(paths)), squeeze=False)
    summary, lines = {}, []
    for r, path in enumerate(paths):
        with np.load(path, allow_pickle=False) as z:
            arc = {k: z[k] for k in z.files}
        fov = Path(path).parent.name
        ev, t, cond, info = trial_traces(arc, args.plane)
        oi, gap = ms.noisepair_decode(cond)
        # B-driven cells: responsive, and significant positive response to B as the first sound.
        bmask = np.isin(oi, [BA, BB]) & np.all(np.isfinite(ev[0]), axis=1)
        b_alone = np.nanmean(ev[:, bmask][:, :, window_mask(t, 0.0, args.window)], axis=2)
        tt = stats.ttest_1samp(b_alone, 0, axis=1, nan_policy="omit")
        cells = arc["any_condition_responsive_fdr"].astype(bool) & (np.nanmean(b_alone, 1) > 0) & (np.asarray(tt.pvalue) < 0.05)
        pop = np.nanmean(ev[cells], axis=0)                              # trials x time
        res = analyze_fov(pop, t, oi, gap, info, args, rng)
        gaps = res["gaps"]; x = np.log2(gaps)
        # (1) B-onset-aligned second-sound responses, first sound removed, vs B alone.
        ax = axes[r, 0]
        okt = np.all(np.isfinite(pop), axis=1)
        alone_tr = np.nanmean(pop[okt & np.isin(oi, [BA, BB])], 0)
        ax.plot(t, alone_tr, color="black", lw=2.2, label="B alone (first sound)")
        cm = plt.cm.viridis(np.linspace(.1, .85, len(gaps)))
        for k, g in enumerate(gaps):
            t2 = info["sound_duration"] + g
            for o, tpl, ls in ((AB, res["tplA"], "-"), (BB, res["tplB"], "--")):
                y = np.nanmean(pop[okt & (oi == o) & np.isclose(gap, g)], 0) - tpl
                m = t >= t2 - 0.2 - 1e-6
                ax.plot(t[m] - t2, y[m], ls, color=cm[k], lw=1.3,
                        label=f"gap {g:g} s: {'B|A' if o == AB else 'B|B'}" if r == 0 else None)
        ax.axvspan(0, args.window, color="0.9", zorder=0); ax.axhline(0, color="0.6", lw=.7, ls=":")
        ax.set_xlim(-0.3, 1.0); ax.set_xlabel("Time from B onset (s)"); ax.set_ylabel("dF/F, first sound subtracted")
        ax.set_title(f"{fov}: B responses (n={cells.sum()} B-driven cells)\nsolid = after A, dashed = after B", fontsize=9)
        if r == 0: ax.legend(fontsize=6, frameon=False, ncol=2, loc="upper right")
        # (2) B|A and B|B relative to B alone, vs gap.
        ax = axes[r, 1]
        for key, lab, col, off in (("after_A", "B preceded by A", "tab:blue", -0.04), ("after_B", "B preceded by B", "tab:orange", 0.04)):
            v = res[f"ratio_{key}"]; c = res[f"ratio_{key}_ci"]
            ax.errorbar(x + off, v, yerr=[v - c[0], c[1] - v], fmt="o-", color=col, capsize=3, label=lab)
        ax.axhline(1, color="black", lw=1, label="B alone"); ax.axhline(0, color="0.6", lw=.7, ls=":")
        for g in res["extrapolated_template_gaps"]:
            ax.annotate("template\nextrapolated", (np.log2(g), ax.get_ylim()[0]), fontsize=6, ha="center", va="bottom", color="0.4")
        ax.set_xticks(x); ax.set_xticklabels([f"{g:g}" for g in gaps]); ax.set_xlabel("Gap (s)")
        ax.set_ylabel("B response / B alone"); ax.set_title("Recovery of the B response (95% CI over trials)", fontsize=9)
        ax.legend(fontsize=7, frameon=False)
        # (3) Direct answer: B|A - B|B per gap.
        ax = axes[r, 2]; d = res["diff"]; c = res["diff_ci"]
        ax.errorbar(x, d, yerr=[d - c[0], c[1] - d], fmt="o", color="black", capsize=4)
        ax.axhline(0, color="0.5", lw=.8)
        for k in range(len(gaps)):
            ax.annotate(f"p={res['p_diff'][k]:.2g}", (x[k], c[1][k]), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=7)
        ax.set_xticks(x); ax.set_xticklabels([f"{g:g}" for g in gaps]); ax.set_xlabel("Gap (s)")
        ax.set_ylabel("B|A − B|B (dF/F)")
        ax.set_title(f"Effect of the preceding sound on B\n(B alone = {res['alone']:.3f} dF/F)", fontsize=9)
        for a in axes[r]: a.spines[["top", "right"]].set_visible(False)
        summary[fov] = {k: v for k, v in res.items() if k not in ("tplA", "tplB")}
        summary[fov]["n_B_driven_cells"] = int(cells.sum()); summary[fov]["session"] = info["session"]
        lines.append(f"{fov} ({info['session']}): {cells.sum()} B-driven cells | B alone {res['alone']:.4f} "
                     f"[{res['alone_ci'][0]:.4f}, {res['alone_ci'][1]:.4f}] dF/F")
        for k, g in enumerate(gaps):
            ex = " (template extrapolated)" if g in res["extrapolated_template_gaps"] else ""
            lines.append(f"   gap {g:g} s: B|A {res['B_after_A'][k]:.4f} ({100*res['ratio_after_A'][k]:.0f}% of alone), "
                         f"B|B {res['B_after_B'][k]:.4f} ({100*res['ratio_after_B'][k]:.0f}%), "
                         f"B|A - B|B {res['diff'][k]:+.4f} [{res['diff_ci'][0][k]:+.4f}, {res['diff_ci'][1][k]:+.4f}] p={res['p_diff'][k]:.2g}; "
                         f"B|A vs alone p={res['p_B_after_A_vs_alone'][k]:.2g}{ex}")
    fig.suptitle("Noise pairs: response to B preceded by A, by B, or by nothing, as a function of gap", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, .97])
    png = out / "noise_pair_B_response_by_preceding_sound_and_gap.png"; fig.savefig(png, dpi=220); plt.close(fig)
    (out / "noise_pair_B_response_by_preceding_sound_and_gap.txt").write_text("\n".join(lines) + "\n")
    (out / "noise_pair_B_response_by_preceding_sound_and_gap.json").write_text(json.dumps(ms.jsonable(summary), indent=2))
    print("\n".join(lines)); print(f"Wrote {png}")


if __name__ == "__main__":
    main()
