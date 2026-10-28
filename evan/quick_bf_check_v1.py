#!/usr/bin/env python3
"""
Quick best-frequency check for ONE pure-tone session, to set the next blocks' frequencies (v1).

Run it during the experiment, right after a pure-tone session of an FOV and a single-session
Suite2p run of it (standard location: TWOPHOTON_PATH/<subject>_processed/<date>/<session>/
suite2p/plane<plane>, with the Scanbox .mat next to it). It writes figures to check by eye and
prints suggested settings for the FOV's other sound types:

If the BF distribution has two clear peaks, the targets are the two modes instead of the median
(one set of settings per mode; see find_bf_modes and --mode-* options). Otherwise the target is
the median BF:

    noise pair   noisepair_center_freq = median BF (band A centered on the FOV's cells)
    band noise   bandnoise_center_freq = median BF, and the widest bandwidth that stays in 2-40 kHz
    chords       chord3t_F0 = median BF, so the lowest tone sits at the BF (the chord spans
                 F0 .. 4 x F0 = BF .. 4 x BF, which stays within 40 kHz only for BF <= 10 kHz)
    FM range     fixed 2-40 kHz sweep (center 8944 Hz, 4.32 octaves) for every FOV; the script
                 only checks that the median BF lies inside it

Every suggestion is checked for clipping at the planned level, using this session's own
calibrated amplitudes (current_amp_L: the rig has only a left speaker; find_amplitude scales
them by 10^(dB/20)) and, for
noise, --noise-amp-at-60db (the noise calibration is not stored in a pure-tone file). Peaks of
filtered noise are simulated the way taskontrol generates them.

Same conventions as the multistim / level-series pipelines (helpers imported from
sound_tuning_multistim_fov_analysis_v6.py): dF/F (jaratoolbox dff=True), response =
mean(0-1 s) - mean(-1-0 s), per-frequency sign-flip test with BH-FDR across cells.
BF = argmax of the mean tuning curve. BF-eligible = responsive, response at BF > 0, and q < 0.05
at the BF (the level-series definition). Median BF and its 95% CI (bootstrap over cells) use
BF-eligible cells. ROI indices are those of this single-session Suite2p run, not of a later
concatenated run, so use this only to choose stimuli, not as the final analysis.

Example
-------
python quick_bf_check_v1.py imag041 20261022 001
python quick_bf_check_v1.py imag041 20261022 001 --target-level 70 --tone-levels 70 75

Output: <TEMP_OUTPUT_PATH>/evan/quick_bf_check_<session>/<subject>/<date>_<session>/
    quick_bf_summary.png         BF histograms with median/CI, responsiveness by frequency,
                                 normalized tuning raster sorted by BF, ROI map colored by BF,
                                 suggested settings + QC
    cell_tuning_pages/page_*.png every BF-eligible cell's tuning curve (mean +/- SEM, significant
                                 frequencies filled, BF marked), sorted by BF
    example_traces.png           mean trace at BF vs a far frequency for cells across the BF range
    bf_histogram_labeled.png / bf_histogram_unlabeled.tif
                                 BF histogram in the posthoc_figures report style (300-dpi PNG,
                                 600-dpi LZW TIFF without text); --hist-cells picks the cells
    quick_bf_cells.csv, quick_bf_summary.json, suggested_settings.txt
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from jaratoolbox import settings
from jaratoolbox import twophotonanalysis

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("_multistim_v6", HERE / "sound_tuning_multistim_fov_analysis_v6.py")
ms = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ms)

SAFE_RANGE_HZ = (2000.0, 40000.0)      # tested / calibrated pure-tone range
FM_FIXED = {"center_hz": 8944.0, "octave_range": 4.32}
NOISEPAIR_A_BW = 0.25
BANDNOISE_BWS = (0.25, 0.5, 1.0, 2.0, 4.0)
CHORD_MIDDLE_OCT = (0.382, 0.764, 1.0, 1.236, 1.618)   # 5 middle tones, irrational scheme


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject"); p.add_argument("date"); p.add_argument("session")
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--n-permutations", type=int, default=4096)
    p.add_argument("--seed", type=int, default=20261022)
    p.add_argument("--target-level", type=float, default=70.0, help="planned level of chords / FM / band noise (dB SPL)")
    p.add_argument("--noisepair-level", type=float, default=60.0, help="planned noise-pair level (dB SPL)")
    p.add_argument("--tone-levels", type=float, nargs="+", default=[70.0, 75.0], help="pure-tone levels to check for clipping")
    p.add_argument("--noise-amp-at-60db", type=float, default=0.3955,
                   help="left-channel white-noise amplitude at 60 dB from the noise calibration (0.3955 on 20261015)")
    p.add_argument("--sampling-rate", type=float, default=192000.0, help="sound card rate, for the noise peak simulation")
    p.add_argument("--cells-per-page", type=int, default=20)
    p.add_argument("--hist-cells", choices=["bf_eligible", "responsive"], default="bf_eligible",
                   help="cells counted in the report-style histogram (posthoc_figures default: responsive)")
    p.add_argument("--mode-min-separation", type=float, default=1.0, help="octaves between the two peaks to call it bimodal")
    p.add_argument("--mode-min-fraction", type=float, default=0.2,
                   help="each peak must hold this fraction of BF-eligible cells within +/-0.5 octave")
    p.add_argument("--mode-max-dip", type=float, default=0.6,
                   help="lowest density between the peaks must be below this fraction of the smaller peak")
    p.add_argument("--out-dir", type=Path, default=None)
    return p.parse_args()


def halfmax_centroid_log2(curves: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Copied from sound_tuning_pure_tone_levels_fov_analysis_v2.py (same definition)."""
    c = np.asarray(curves, float)
    peak = np.max(np.where(np.isfinite(c), c, -np.inf), axis=-1, keepdims=True)
    w = np.clip(np.nan_to_num(c - peak / 2.0, nan=0.0, neginf=0.0, posinf=0.0), 0.0, None)
    s = w.sum(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = (w * np.asarray(x, float)).sum(axis=-1) / s
    return np.where((peak[..., 0] > 0) & (s > 0), out, np.nan)


def find_bf_modes(lb: np.ndarray, freqs: np.ndarray, args, bw_oct: float = 0.3) -> dict:
    """Peaks of the log2-BF distribution (Gaussian kernel density, bandwidth bw_oct octaves).

    Bimodal when the two highest peaks are >= --mode-min-separation octaves apart, each holds
    >= --mode-min-fraction of the cells within +/-0.5 octave, and the density between them falls
    below --mode-max-dip x the smaller peak. Each mode is reported as the density peak and as the
    tested frequency with the most cells within +/-0.3 octave of it.
    """
    from scipy.signal import find_peaks
    grid = np.linspace(np.log2(freqs[0]) - .5, np.log2(freqs[-1]) + .5, 600)
    dens = np.exp(-0.5 * ((grid[:, None] - lb[None, :]) / bw_oct) ** 2).sum(1)
    dens /= dens.sum() * (grid[1] - grid[0])
    pk, _ = find_peaks(dens, prominence=0.05 * dens.max())
    peaks = []
    for i in pk:
        near = freqs[np.abs(np.log2(freqs) - grid[i]) <= 0.3]
        cnt = [np.sum(np.isclose(lb, np.log2(f))) for f in near]
        peaks.append({"density_peak_hz": float(2 ** grid[i]), "height": float(dens[i]),
                      "tested_freq_hz": float(near[int(np.argmax(cnt))]) if len(near) else float(2 ** grid[i]),
                      "fraction_within_half_octave": float(np.mean(np.abs(lb - grid[i]) <= 0.5))})
    peaks.sort(key=lambda d: -d["height"])
    res = {"grid_log2": grid, "density": dens, "peaks": peaks, "bimodal": False, "reason": ""}
    if len(peaks) < 2:
        res["reason"] = "one peak"; return res
    a, b = sorted(peaks[:2], key=lambda d: d["density_peak_hz"])
    sep = abs(np.log2(b["density_peak_hz"] / a["density_peak_hz"]))
    between = (grid > np.log2(a["density_peak_hz"])) & (grid < np.log2(b["density_peak_hz"]))
    dip = float(dens[between].min() / min(a["height"], b["height"])) if between.any() else 1.0
    ok = (sep >= args.mode_min_separation, min(a["fraction_within_half_octave"], b["fraction_within_half_octave"]) >= args.mode_min_fraction,
          dip <= args.mode_max_dip)
    res.update({"separation_oct": float(sep), "dip_ratio": dip, "modes": [a, b], "bimodal": bool(all(ok)),
                "reason": "; ".join(t for t, good in zip((f"separation {sep:.2f} oct", f"smaller peak holds {min(a['fraction_within_half_octave'], b['fraction_within_half_octave']):.0%}",
                                                          f"dip {dip:.2f} of smaller peak"), ok) if not good) or "two clear peaks"})
    return res


OCTAVE_TICKS_KHZ = [2, 4, 8, 16, 32]


def draw_report_histogram(bf_hz: np.ndarray, freqs_hz: np.ndarray, title: str, legend: str,
                          targets: list, labeled: bool, out_path: Path) -> None:
    """One-panel BF histogram in the style of posthoc_figures/bf_histogram_stack.py."""
    x = np.log2(freqs_hz / 1000.0); step = np.min(np.diff(x))
    counts = np.array([np.sum(np.isclose(bf_hz, v)) for v in freqs_hz])
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(x, counts, width=0.84 * step, color="tab:green", label=legend)
    for f in targets:
        ax.axvline(np.log2(f / 1000.0), color="black", lw=2, ls="--")
    ax.set_ylim(0, max(1, counts.max()) * 1.12)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=3, integer=True))
    ax.spines[["top", "right"]].set_visible(False); ax.spines[["left", "bottom"]].set_linewidth(1.5)
    ax.tick_params(width=1.5, length=6, labelsize=18)
    ax.set_xlim(x[0] - step, x[-1] + step); ax.set_xticks(np.log2(OCTAVE_TICKS_KHZ)); ax.set_xticks(x, minor=True)
    ax.tick_params(which="minor", length=3, width=1)
    if labeled:
        ax.set_xticklabels([str(k) for k in OCTAVE_TICKS_KHZ]); ax.set_xlabel("Best frequency (kHz)", fontsize=20)
        ax.set_ylabel("Cells (count)", fontsize=20); ax.set_title(title, fontsize=16, loc="left", pad=6)
        ax.legend(frameon=False, fontsize=13, loc="upper right", handlelength=1.2)
        fig.tight_layout(); fig.savefig(out_path, dpi=300)
    else:
        ax.tick_params(labelleft=False, labelbottom=False)
        fig.tight_layout(); fig.savefig(out_path, dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)


# -----------------------------------------------------------------------------
# Headroom checks
# -----------------------------------------------------------------------------

def tone_amp_fn(freqs: np.ndarray, amps: np.ndarray, level0: float):
    """Amplitude needed for a tone at (f, level), interpolated in log f like find_amplitude."""
    lf = np.log10(freqs)
    return lambda f, level: np.interp(np.log10(f), lf, amps) * 10 ** ((level - level0) / 20.0)


def noise_peak_factor(center: float, bw: float, fs: float, rescale_to_white: bool, am: bool, n: int = 60) -> float:
    """99th-percentile peak / amplitude of taskontrol-style filtered uniform noise."""
    rng = np.random.default_rng(0); dur = 0.1 if rescale_to_white else 0.5; out = []
    for _ in range(n):
        w = rng.uniform(-1, 1, int(dur * fs)); p0 = np.mean(w ** 2)
        S = np.fft.rfft(w); f = np.fft.rfftfreq(len(w), 1 / fs)
        S[(f < center / 2 ** (bw / 2)) | (f > center * 2 ** (bw / 2))] = 0
        x = np.fft.irfft(S, len(w))
        if rescale_to_white: x *= np.sqrt(p0 / np.mean(x ** 2))
        if am: x *= 0.5 + 0.5 * np.sin(2 * np.pi * 8 * np.arange(len(w)) / fs + np.pi / 2)
        out.append(np.max(np.abs(x)))
    return float(np.percentile(out, 99))


def headroom_checks(bf: float, amp_at, args) -> list[dict]:
    rows = []
    def add(sound, setting, level, peak):
        rows.append({"sound": sound, "setting": setting, "level_db": level, "peak": float(peak),
                     "ok": bool(peak <= 1.0), "clean_max_db": float(level - 20 * np.log10(peak)) if peak > 0 else np.nan})
    tested = np.geomspace(2000, 40000, 16)
    for lv in args.tone_levels:
        pk = np.max([amp_at(f, lv) for f in tested]); add("pure tones 2-40 kHz", "16 log-spaced tones", lv, pk)
    f0 = bf
    comps = [f0 * 2 ** o for o in (0.0, 2.0)] + [f0 * 2 ** o for o in CHORD_MIDDLE_OCT]
    a = {f: amp_at(f, args.target_level) for f in comps}
    worst = max((a[f0] + a[f0 * 2 ** o] + a[f0 * 4]) / np.sqrt(3) for o in CHORD_MIDDLE_OCT)
    add("chord (3 tones)", f"F0 {f0:.0f} Hz", args.target_level, worst)
    add("FM fixed range", f"center {FM_FIXED['center_hz']:.0f} Hz", args.target_level, amp_at(FM_FIXED["center_hz"], args.target_level))
    namp = lambda lv: args.noise_amp_at_60db * 10 ** ((lv - 60) / 20)
    for bw in BANDNOISE_BWS:
        add("band noise", f"center {bf:.0f} Hz, {bw:g} oct", args.target_level,
            namp(args.target_level) * noise_peak_factor(bf, bw, args.sampling_rate, False, True))
    add("noise pair A", f"center {bf:.0f} Hz, {NOISEPAIR_A_BW:g} oct", args.noisepair_level,
        namp(args.noisepair_level) * noise_peak_factor(bf, NOISEPAIR_A_BW, args.sampling_rate, True, False))
    add("noise pair B", "white noise", args.noisepair_level, namp(args.noisepair_level))
    return rows


def suggestions(bf: float) -> dict:
    lo, hi = SAFE_RANGE_HZ
    bw_fit = 2 * np.log2(min(hi / bf, bf / lo)) if lo < bf < hi else 0.0
    f0 = bf
    fm_lo = FM_FIXED["center_hz"] / 2 ** (FM_FIXED["octave_range"] / 2); fm_hi = FM_FIXED["center_hz"] * 2 ** (FM_FIXED["octave_range"] / 2)
    notes = []
    if f0 < lo: notes.append(f"chord F0 {f0:.0f} Hz is below {lo:.0f} Hz")
    if 4 * f0 > hi: notes.append(f"chord top tone 4 x F0 = {4*f0:.0f} Hz is above {hi:.0f} Hz; F0 <= {hi/4:.0f} Hz keeps the chord in range")
    if bw_fit < max(BANDNOISE_BWS): notes.append(f"band noise wider than {bw_fit:.2f} oct leaves {lo/1000:g}-{hi/1000:g} kHz at this center")
    if not (fm_lo <= bf <= fm_hi): notes.append("median BF is outside the fixed FM sweep")
    a_lo, a_hi = bf / 2 ** (NOISEPAIR_A_BW / 2), bf * 2 ** (NOISEPAIR_A_BW / 2)
    if a_hi > hi or a_lo < lo: notes.append("noise-pair band A extends beyond the calibrated range")
    return {"noisepair_center_freq": round(bf), "bandnoise_center_freq": round(bf),
            "bandnoise_max_bandwidth_in_range_oct": round(float(bw_fit), 2),
            "chord3t_F0": round(f0), "chord_span_hz": [round(f0), round(4 * f0)],
            "FMfixedrange_center_freq": FM_FIXED["center_hz"], "FMfixedrange_octave_range": FM_FIXED["octave_range"],
            "FM_sweep_hz": [round(fm_lo), round(fm_hi)], "notes": notes}


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    out = args.out_dir or Path(settings.TEMP_OUTPUT_PATH) / "evan" / f"quick_bf_check_{args.session}" / args.subject / f"{args.date}_{args.session}"
    (out / "cell_tuning_pages").mkdir(parents=True, exist_ok=True)
    d = twophotonanalysis.TwoPhoton(args.subject, args.date, args.session, args.plane, paradigm=ms.PARADIGM)
    b = d.bdata
    names = {str(b.labels["current_stim_type"].get(int(c), c)) for c in np.unique(b["current_stim_type"])}
    if names != {"Pure_tone"}:
        raise ValueError(f"Session {args.session} is not a pure-tone session: stim types {names}")
    level = float(np.median(b["current_intensity"]))
    freq_trial = np.asarray(b["current_tone_freq"], float)
    amp_trial = np.asarray(b["current_amp_L"], float)   # left speaker only
    freqs = np.sort(np.unique(freq_trial))
    amp_table = np.array([np.median(amp_trial[freq_trial == f]) for f in freqs])
    clipped_now = freqs[amp_table > 1.0]

    cells = np.flatnonzero((d.iscell[:, 0] == 1) & (d.iscell[:, 1] > ms.CELL_PROB_THRESHOLD))
    ev_all, tvec, valid = d.event_locked_average(time_range=list(ms.TIME_RANGE), dff=True)
    ev, valid, _, align = ms.align_imaging_events_to_behavior(
        np.asarray(ev_all[cells], float), valid, np.asarray(d.event_onset), float(d.srate),
        np.asarray(b["stim_duration"], float), np.asarray(b["ISI"], float), len(freq_trial))
    t = np.asarray(tvec, float); valid = np.asarray(valid, bool)
    base = (t >= ms.BASELINE_RANGE[0]) & (t < ms.BASELINE_RANGE[1])
    ev_bc = ev - np.nanmean(ev[:, :, base], axis=2)[:, :, None]
    tr = ms._trial_response(ev, t); tr[:, ~valid] = np.nan

    rng = np.random.default_rng(args.seed); n = len(cells); nf = len(freqs)
    curve = np.full((n, nf), np.nan); sem = np.full_like(curve, np.nan); q = np.full_like(curve, np.nan)
    for j, f in enumerate(freqs):
        m = valid & (freq_trial == f)
        curve[:, j] = np.nanmean(tr[:, m], 1); sem[:, j] = stats.sem(tr[:, m], axis=1, nan_policy="omit")
        tested = np.sum(np.isfinite(tr[:, m]), 1) >= ms.MIN_FINITE_TRIALS
        q[:, j] = ms.bh_fdr(ms.signflip_pvalues_grouped(tr[:, m], tested, args.n_permutations, rng), tested)
    sig = np.isfinite(q) & (q < 0.05)
    responsive = sig.any(1)
    bfj = np.argmax(np.where(np.isfinite(curve), curve, -np.inf), 1)
    bf = freqs[bfj]; r_bf = curve[np.arange(n), bfj]; q_bf = q[np.arange(n), bfj]
    elig = responsive & (r_bf > 0) & (q_bf < 0.05)
    cen = 2 ** halfmax_centroid_log2(curve, np.log2(freqs))
    lb = np.log2(bf[elig])
    if not len(lb):
        raise RuntimeError("No BF-eligible cells: check the session (Suite2p cells, alignment, level).")
    med = float(2 ** np.median(lb))
    boot = 2 ** np.median(rng.choice(lb, (2000, len(lb))), axis=1); ci = np.percentile(boot, [2.5, 97.5])
    med_cen = float(2 ** np.nanmedian(np.log2(cen[elig])))
    grid = np.log2(np.geomspace(freqs[0], freqs[-1], 200)); cover = np.array([np.mean(np.abs(lb - g) <= 0.5) for g in grid])
    best_cover = float(2 ** grid[np.argmax(cover)]); cover_med = float(np.mean(np.abs(lb - np.log2(med)) <= 0.5))
    counts = np.array([np.sum(bf[elig] == f) for f in freqs])

    modes = find_bf_modes(lb, freqs, args)
    if modes["bimodal"]:
        targets = [(f"low mode {m['tested_freq_hz']/1000:.3g} kHz", m["tested_freq_hz"], m["fraction_within_half_octave"]) for m in modes["modes"]]
        targets[1] = (targets[1][0].replace("low", "high"), targets[1][1], targets[1][2])
    else:
        targets = [("median BF", med, cover_med)]
    amp_at = tone_amp_fn(freqs, amp_table, level)
    plans = [(lab, f, cov, suggestions(f), headroom_checks(f, amp_at, args)) for lab, f, cov in targets]
    sug, head = plans[0][3], plans[0][4]
    warn = []
    if len(clipped_now): warn.append(f"THIS session clipped: amplitude > 1 at {', '.join(f'{f/1000:.3g}' for f in clipped_now)} kHz")
    if not modes["bimodal"] and cover_med < 0.3: warn.append(f"only {cover_med:.0%} of BF-eligible cells lie within +/-0.5 oct of the median "
                                    f"(BF distribution is spread or bimodal); the center covering most cells is {best_cover/1000:.1f} kHz")
    if elig.sum() < 30: warn.append(f"only {elig.sum()} BF-eligible cells: median BF is unreliable")
    if align["timing_mae_s"] > 0.15: warn.append(f"alignment error {align['timing_mae_s']*1000:.0f} ms is high")
    seen = set()
    for _, _, _, _, hd in plans:
        for h in hd:
            key = (h["sound"], h["setting"], h["level_db"])
            if not h["ok"] and key not in seen:
                seen.add(key); warn.append(f"{h['sound']} ({h['setting']}) at {h['level_db']:g} dB CLIPS: peak {h['peak']:.2f}, clean max {h['clean_max_db']:.1f} dB")
    for lab, f, _ in targets:
        if f >= freqs[-1] / 2 ** 0.25 or f <= freqs[0] * 2 ** 0.25:
            warn.append(f"{lab} is at the edge of the tested range: cells may be tuned beyond it")

    # ---- per-cell table ----
    df = pd.DataFrame({"suite2p_roi_index": cells, "responsive_fdr": responsive, "bf_eligible": elig,
                       "best_frequency_hz": bf, "bf_centroid_hz": cen, "response_at_bf": r_bf, "q_at_bf": q_bf,
                       "n_significant_frequencies": sig.sum(1)})
    for j, f in enumerate(freqs):
        df[f"response_{f:.0f}_Hz"] = curve[:, j]; df[f"q_{f:.0f}_Hz"] = q[:, j]
    df.to_csv(out / "quick_bf_cells.csv", index=False)

    # ---- summary figure ----
    x = np.log2(freqs / 1000); klab = [f"{f/1000:.3g}" for f in freqs]
    fig = plt.figure(figsize=(18, 11)); gs = fig.add_gridspec(2, 3, hspace=.38, wspace=.28)
    ax = fig.add_subplot(gs[0, 0])
    ax.bar(x, counts, width=.22, color="tab:blue", alpha=.8, label="argmax BF")
    ax.axvline(np.log2(med / 1000), color="black", lw=2, label=f"median {med/1000:.2f} kHz")
    ax.axvspan(np.log2(ci[0] / 1000), np.log2(ci[1] / 1000), color="0.75", alpha=.5, label=f"95% CI {ci[0]/1000:.2f}-{ci[1]/1000:.2f}")
    ax.axvline(np.log2(med_cen / 1000), color="tab:red", ls="--", lw=1.5, label=f"median centroid {med_cen/1000:.2f} kHz")
    ax.axvspan(np.log2(med / 1000) - .5, np.log2(med / 1000) + .5, color="tab:green", alpha=.08, label=f"±0.5 oct: {cover_med:.0%} of cells")
    ax2 = ax.twinx(); ax2.plot(modes["grid_log2"] - np.log2(1000), modes["density"], color="tab:purple", lw=1.2)
    ax2.set_yticks([]); ax2.set_ylim(0, None)
    for m in modes.get("modes", []) if modes["bimodal"] else []:
        ax.axvline(np.log2(m["tested_freq_hz"] / 1000), color="tab:purple", lw=2.5, ls=":",
                   label=f"mode {m['tested_freq_hz']/1000:.3g} kHz ({m['fraction_within_half_octave']:.0%} within ±0.5 oct)")
    ms._readable_condition_ticks(ax, x, klab); ax.set_xlabel("Best frequency (kHz)"); ax.set_ylabel("BF-eligible cells")
    ax.set_title(f"BF of {elig.sum()} BF-eligible cells (of {n} cells; {responsive.sum()} responsive)"); ax.legend(fontsize=7, frameon=False)
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(x, 100 * sig.mean(0), "o-", label="% cells significant (q<0.05) at frequency")
    ax.plot(x, 100 * np.array([np.mean((curve[:, j] > 0) & sig[:, j]) for j in range(nf)]), "s--", label="% significant and excited")
    ms._readable_condition_ticks(ax, x, klab); ax.set_xlabel("Frequency (kHz)"); ax.set_ylabel("% of cells"); ax.set_ylim(0, None)
    ax.set_title("Responsiveness by frequency"); ax.legend(fontsize=7, frameon=False)
    for f in clipped_now: ax.axvline(np.log2(f / 1000), color="red", alpha=.3, lw=6)
    ax = fig.add_subplot(gs[0, 2])
    order = np.flatnonzero(elig)[np.lexsort((-r_bf[elig], bfj[elig]))]
    norm = curve[order] / np.nanmax(np.abs(curve[order]), axis=1, keepdims=True)
    ax.imshow(norm, aspect="auto", cmap="coolwarm", vmin=-1, vmax=1, interpolation="nearest")
    ms._readable_condition_ticks(ax, np.arange(nf), klab); ax.set_xlabel("Frequency (kHz)")
    ax.set_ylabel("BF-eligible cells, sorted by BF"); ax.set_title("Normalized tuning curves (each row / its max |response|)")
    ax = fig.add_subplot(gs[1, 0])
    mimg = np.asarray(d.ops.get("meanImg"), float); lo_, hi_ = np.nanpercentile(mimg, [1, 99.5])
    ax.imshow(mimg, cmap="gray", vmin=lo_, vmax=hi_)
    cmap = plt.cm.viridis; nrm = matplotlib.colors.Normalize(np.log2(freqs[0]), np.log2(freqs[-1]))
    for k, ci_ in enumerate(cells):
        st = d.stat[ci_]; col = cmap(nrm(np.log2(bf[k]))) if elig[k] else (0.6, 0.6, 0.6, 0.5)
        ax.scatter(st["xpix"], st["ypix"], s=.6, c=[col], alpha=.5 if elig[k] else .25, linewidths=0)
    sm = plt.cm.ScalarMappable(norm=nrm, cmap=cmap); cb = fig.colorbar(sm, ax=ax, fraction=.04)
    cb.set_ticks(np.log2(freqs[::3])); cb.set_ticklabels([f"{f/1000:.3g}" for f in freqs[::3]]); cb.set_label("BF (kHz)")
    ax.set_axis_off(); ax.set_title("ROIs colored by BF (gray = not BF-eligible)")
    ax = fig.add_subplot(gs[1, 1:]); ax.axis("off")
    lines = [f"{args.subject} {args.date} session {args.session} | pure tones at {level:g} dB SPL | {nf} frequencies "
             f"{freqs[0]/1000:.3g}-{freqs[-1]/1000:.3g} kHz | trials/frequency {int(np.min([np.sum(valid & (freq_trial == f)) for f in freqs]))}-"
             f"{int(np.max([np.sum(valid & (freq_trial == f)) for f in freqs]))} | alignment MAE {align['timing_mae_s']*1000:.0f} ms",
             f"MEDIAN BF {med/1000:.2f} kHz (95% CI {ci[0]/1000:.2f}-{ci[1]/1000:.2f}); median centroid {med_cen/1000:.2f} kHz; "
             f"center covering most cells within ±0.5 oct: {best_cover/1000:.2f} kHz ({cover.max():.0%})",
             ("BIMODAL BF distribution: modes " + " and ".join(f"{m['tested_freq_hz']/1000:.3g} kHz ({m['fraction_within_half_octave']:.0%} of cells within ±0.5 oct)" for m in modes["modes"])
              + f"; separation {modes['separation_oct']:.1f} oct, dip {modes['dip_ratio']:.2f}. Settings are given for EACH mode; the median is not used.")
             if modes["bimodal"] else f"Single-peaked by the mode test ({modes['reason']}): target = median BF."]
    for k, (lab, f, cov, sg, hd) in enumerate(plans):
        lines += ["", f"SUGGESTED SETTINGS ({lab}; {cov:.0%} of cells within ±0.5 oct):",
                  f"  noise pair : noisepair_center_freq = {sg['noisepair_center_freq']}  (level {args.noisepair_level:g} dB)",
                  f"  band noise : bandnoise_center_freq = {sg['bandnoise_center_freq']}; widest band in {SAFE_RANGE_HZ[0]/1000:g}-{SAFE_RANGE_HZ[1]/1000:g} kHz = {sg['bandnoise_max_bandwidth_in_range_oct']} oct",
                  f"  chords     : chord3t_F0 = {sg['chord3t_F0']}  (chord spans {sg['chord_span_hz'][0]}-{sg['chord_span_hz'][1]} Hz; lowest tone = BF)"]
        if k == 0:
            lines.append(f"  FM range   : FMfixedrange_center_freq = {sg['FMfixedrange_center_freq']:.0f}, octave_range = {sg['FMfixedrange_octave_range']} ({sg['FM_sweep_hz'][0]}-{sg['FM_sweep_hz'][1]} Hz, same for every FOV)")
        lines += [f"  note: {nt}" for nt in sg["notes"]]
        lines.append("  HEADROOM (peak must be <= 1.0):")
        lines += [f"    {'OK  ' if h['ok'] else 'CLIP'} {h['sound']:20s} {h['setting']:28s} {h['level_db']:4.0f} dB  peak {h['peak']:.2f}  clean max {h['clean_max_db']:.1f} dB"
                  for h in hd if k == 0 or h["sound"] in ("chord (3 tones)", "band noise", "noise pair A")]
    lines += ["", "WARNINGS:"] + ([f"  ! {w}" for w in warn] if warn else ["  none"])
    ax.text(0, 1, "\n".join(lines), va="top", ha="left", family="monospace", fontsize=8.2 if len(plans) == 1 else 7.0, transform=ax.transAxes)
    headline = (" and ".join(f"{f/1000:.3g}" for _, f, _ in targets) + " kHz (two BF modes)") if modes["bimodal"] else f"median BF {med/1000:.2f} kHz"
    fig.suptitle(f"Quick BF check — {args.subject} {args.date} {args.session} — {headline}", fontsize=14)
    fig.savefig(out / "quick_bf_summary.png", dpi=150, bbox_inches="tight"); plt.close(fig)

    # ---- report-style histogram (posthoc_figures style); dashed line(s) = target(s) ----
    hsel = elig if args.hist_cells == "bf_eligible" else responsive
    what = "BF-eligible" if args.hist_cells == "bf_eligible" else "FDR-responsive"
    tdesc = " and ".join(f"{f/1000:.3g}" for _, f, _ in targets) + (" kHz (modes)" if modes["bimodal"] else " kHz (median)")
    for labeled, name in ((True, "bf_histogram_labeled.png"), (False, "bf_histogram_unlabeled.tif")):
        draw_report_histogram(bf[hsel], freqs, f"{args.subject} {args.date} {args.session} · {level:g} dB · target {tdesc}",
                              f"{what} cells (n={int(hsel.sum())})", [f for _, f, _ in targets], labeled, out / name)

    # ---- per-cell tuning pages (all BF-eligible cells, sorted by BF) ----
    per = args.cells_per_page; ncol = 5; nrow = int(np.ceil(per / ncol))
    for pg, s0 in enumerate(range(0, len(order), per), start=1):
        fig, axs = plt.subplots(nrow, ncol, figsize=(3.2 * ncol, 2.5 * nrow), squeeze=False, sharex=True)
        for a_ in axs.ravel(): a_.axis("off")
        for a_, k in zip(axs.ravel(), order[s0:s0 + per]):
            a_.axis("on"); a_.errorbar(x, curve[k], yerr=sem[k], color="0.3", lw=1.2, capsize=1.5)
            a_.scatter(x[sig[k]], curve[k, sig[k]], color="tab:red", s=14, zorder=3)
            a_.axvline(np.log2(bf[k] / 1000), color="tab:blue", lw=1); a_.axhline(0, color="0.7", lw=.6, ls=":")
            a_.set_title(f"ROI {cells[k]} | BF {bf[k]/1000:.3g} kHz | q {q_bf[k]:.1g}", fontsize=7.5)
            a_.tick_params(labelsize=6)
        for a_ in axs[-1]: a_.set_xticks(x[::3]); a_.set_xticklabels(klab[::3], fontsize=6); a_.set_xlabel("kHz", fontsize=7)
        fig.suptitle(f"{args.subject} {args.date} {args.session} {level:g} dB — BF-eligible cells sorted by BF (red = q<0.05) — page {pg}", fontsize=10)
        fig.tight_layout(rect=[0, 0, 1, .96]); fig.savefig(out / "cell_tuning_pages" / f"page_{pg:03d}.png", dpi=110); plt.close(fig)

    # ---- example traces: 12 cells spread over the BF range ----
    pick = order[np.unique(np.linspace(0, len(order) - 1, min(12, len(order))).round().astype(int))]
    fig, axs = plt.subplots(3, 4, figsize=(15, 9), squeeze=False)
    for a_ in axs.ravel(): a_.axis("off")
    for a_, k in zip(axs.ravel(), pick):
        a_.axis("on"); far = int(np.argmax(np.abs(np.log2(freqs) - np.log2(bf[k]))))
        for j, col, lab in ((bfj[k], "tab:blue", f"BF {freqs[bfj[k]]/1000:.3g} kHz"), (far, "0.5", f"far {freqs[far]/1000:.3g} kHz")):
            m = valid & (freq_trial == freqs[j]); y = np.nanmean(ev_bc[k][m], 0); e = stats.sem(ev_bc[k][m], axis=0, nan_policy="omit")
            a_.plot(t, y, color=col, label=lab); a_.fill_between(t, y - e, y + e, color=col, alpha=.2, lw=0)
        a_.axvspan(0, 0.5, color="0.9", zorder=0); a_.axhline(0, color="0.7", lw=.6, ls=":")
        a_.set_title(f"ROI {cells[k]}", fontsize=8); a_.legend(fontsize=6, frameon=False); a_.tick_params(labelsize=7)
    fig.suptitle("Mean ± SEM dF/F at BF vs the farthest tested frequency (gray bar = tone)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, .95]); fig.savefig(out / "example_traces.png", dpi=130); plt.close(fig)

    summary = {"subject": args.subject, "date": args.date, "session": args.session, "level_db": level,
               "n_cells": int(n), "n_responsive": int(responsive.sum()), "n_bf_eligible": int(elig.sum()),
               "median_bf_hz": med, "median_bf_ci95_hz": ci.tolist(), "median_centroid_hz": med_cen,
               "fraction_within_half_octave_of_median": cover_med, "center_covering_most_cells_hz": best_cover,
               "bimodal": modes["bimodal"], "mode_test": {k: v for k, v in modes.items() if k not in ("grid_log2", "density")},
               "targets": [{"label": lab, "frequency_hz": f, "fraction_within_half_octave": cov, "suggested_settings": sg, "headroom": hd}
                           for lab, f, cov, sg, hd in plans],
               "bf_counts": dict(zip([f"{f:.0f}" for f in freqs], counts.tolist())),
               "alignment": align, "suggested_settings": sug, "headroom": head, "warnings": warn,
               "clipped_frequencies_this_session_hz": clipped_now.tolist()}
    (out / "quick_bf_summary.json").write_text(json.dumps(ms.jsonable(summary), indent=2))
    (out / "suggested_settings.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print(f"\nFigures: {out}")


if __name__ == "__main__":
    main()
