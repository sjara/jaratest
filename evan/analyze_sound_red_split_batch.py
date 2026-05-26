#!/usr/bin/env python3
"""
analyze_sound_red_split_batch.py

Batch CLI for two-photon sound tuning + red-cell split analysis.

Required CSV columns:
subject,date,session,plane,paradigm,sound_type,suite2p_dir,output_dir

Example:
python analyze_sound_red_split_batch.py --batch-csv batch_sessions.csv
"""

import argparse
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import skew
from scipy.ndimage import binary_erosion

try:
    from sklearn.mixture import GaussianMixture
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

from jaratoolbox import twophotonanalysis, behavioranalysis


# ============================================================
# CLI
# ============================================================

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--batch-csv", required=True)
    p.add_argument("--prob-threshold", type=float, default=0.5)
    p.add_argument("--time-start", type=float, default=-1.0)
    p.add_argument("--time-end", type=float, default=1.5)
    p.add_argument("--resp-start", type=float, default=0.0)
    p.add_argument("--resp-end", type=float, default=0.5)
    p.add_argument("--min-response", type=float, default=0.03)
    p.add_argument("--min-trials", type=int, default=3)
    p.add_argument("--dpi", type=int, default=150)
    return p.parse_args()


# ============================================================
# Helpers
# ============================================================

def savefig(fig, output_dir, name, dpi):
    path = output_dir / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pil_kwargs={"compress_level": 9})
    plt.close(fig)
    print(f"Saved: {path}")


def norm_img(img, p=(2, 98), gamma=1.0):
    lo, hi = np.percentile(img, p)
    return np.clip((img - lo) / (hi - lo), 0, 1) ** gamma


def get_sound_vector(data2p, sound_type):
    if sound_type in ["frequency", "AM"]:
        key = "currentFreq"
    else:
        for candidate in ["soundID", "currentSound", "soundType", "stimID"]:
            if candidate in data2p.bdata:
                key = candidate
                break
        else:
            raise KeyError("Natural-sound key not found.")
    return np.asarray(data2p.bdata[key]), key


def xlabels_for_stim(possible, sound_type):
    if sound_type == "frequency":
        return [f"{x/1000:.1f}" for x in possible], "Frequency (kHz)"
    if sound_type == "AM":
        return [f"{x:.0f}" for x in possible], "AM rate (Hz)"
    return [str(x) for x in possible], "Natural sound"


def match_trials(data2p, stim_all, stim_key):
    n_trials_2p = len(data2p.event_onset)
    n_trials_behavior = len(stim_all)

    if n_trials_2p < n_trials_behavior:
        stim_all = stim_all[:n_trials_2p]
        data2p.bdata[stim_key] = data2p.bdata[stim_key][:n_trials_2p]
    elif n_trials_2p > n_trials_behavior:
        data2p.event_onset = data2p.event_onset[:n_trials_behavior]

    return stim_all


def compute_tuning(eventlocked, tvec, stim, resp_start, resp_end, min_trials):
    possible = np.unique(stim)
    trials_each = behavioranalysis.find_trials_each_type(stim, possible)

    n_cells = eventlocked.shape[0]
    n_stim = len(possible)
    tuning = np.full((n_cells, n_stim), np.nan)

    bwin = tvec < 0
    rwin = (tvec > resp_start) & (tvec < resp_end)

    for k in range(n_stim):
        trials = trials_each[:, k]
        if trials.sum() < min_trials:
            continue

        data_f = eventlocked[:, trials, :]
        baseline = np.nanmean(data_f[:, :, bwin], axis=(1, 2))
        response = np.nanmean(data_f[:, :, rwin], axis=(1, 2))
        tuning[:, k] = response - baseline

    return tuning, possible, trials_each


def sort_norm(tuning, possible):
    if tuning.shape[0] == 0:
        return tuning

    best_idx = np.nanargmax(tuning, axis=1)
    order = np.argsort(possible[best_idx])
    t = tuning[order]

    denom = np.nanmax(t, axis=1, keepdims=True)
    denom[denom == 0] = np.nan

    return t / denom


def align_cells(data2p, suite2p_dir):
    stat = np.load(suite2p_dir / "stat.npy", allow_pickle=True)
    iscell_full = np.load(suite2p_dir / "iscell.npy", allow_pickle=True)

    iscell_data = data2p.iscell

    inds = []
    for row in iscell_data:
        matches = np.where(
            (iscell_full[:, 0] == row[0]) &
            (np.isclose(iscell_full[:, 1], row[1]))
        )[0]
        if len(matches) == 0:
            raise ValueError("Could not match a cell between data2p and Suite2p.")
        inds.append(matches[0])

    return np.asarray(inds), stat, iscell_full


def classify_red_cells(suite2p_dir, stat, iscell_full):
    ops = np.load(suite2p_dir / "ops.npy", allow_pickle=True).item()
    red_img = ops["meanImg_chan2"]

    red_mean = np.array([
        red_img[s["ypix"].astype(int), s["xpix"].astype(int)].mean()
        for s in stat
    ])

    is_cell = iscell_full[:, 0].astype(bool)
    red_values = red_mean[is_cell]

    if HAS_SKLEARN and len(red_values) >= 10:
        X = red_values.reshape(-1, 1)
        gmm = GaussianMixture(n_components=2, random_state=0).fit(X)

        means = gmm.means_.flatten()
        stds = np.sqrt(gmm.covariances_.flatten())
        weights = gmm.weights_.flatten()

        order = np.argsort(means)
        means, stds, weights = means[order], stds[order], weights[order]

        x = np.linspace(red_values.min(), red_values.max(), 2000)

        def gaussian(x, mu, sd, w):
            return w * (1 / (sd * np.sqrt(2*np.pi))) * np.exp(-(x - mu)**2 / (2 * sd**2))

        g1 = gaussian(x, means[0], stds[0], weights[0])
        g2 = gaussian(x, means[1], stds[1], weights[1])
        thresh = x[np.argmin(np.abs(g1 - g2))]
        method = "GMM"
    else:
        thresh = np.percentile(red_values, 95)
        method = "p95"

    redcell = red_mean > thresh
    return redcell, red_mean, thresh, method


# ============================================================
# Plots
# ============================================================

def plot_eventlocked_qc(eventlocked, tvec, prefix, output_dir, dpi):
    trialavg = np.nanmean(eventlocked, axis=1)

    fig = plt.figure(figsize=(8, 6), constrained_layout=True)

    ax0 = plt.subplot(4, 1, (1, 3))
    im = ax0.imshow(
        trialavg,
        interpolation="nearest",
        extent=[tvec[0], tvec[-1], eventlocked.shape[0], 0],
        aspect="auto"
    )
    plt.colorbar(im, ax=ax0, label="dF/F")
    ax0.axvline(0, color="darkred")
    ax0.set_title("Event-locked average")
    ax0.set_ylabel("Neuron")
    plt.setp(ax0.get_xticklabels(), visible=False)

    ax1 = plt.subplot(4, 1, 4, sharex=ax0)
    ax1.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    ax1.axvline(0, color="darkred")
    ax1.set_xlabel("Time from sound onset (s)")
    ax1.set_ylabel("Mean dF/F")

    savefig(fig, output_dir, f"{prefix}_eventlocked_qc.png", dpi)


def plot_all_cell_tuning(tuning, possible, sound_type, prefix, output_dir, dpi):
    labels, xlabel = xlabels_for_stim(possible, sound_type)
    n_cells = tuning.shape[0]

    fig, ax = plt.subplots(2, 1, figsize=(8, 7), constrained_layout=True)

    for i in range(n_cells):
        ax[0].plot(possible, tuning[i], "o-", alpha=0.25, lw=0.5)

    if sound_type in ["frequency", "AM"]:
        ax[0].set_xscale("log")
    ax[0].set_xticks(possible)
    ax[0].set_xticklabels(labels, rotation=45)
    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel("ΔF/F")
    ax[0].set_title("Tuning curves — all cells")
    ax[0].grid(alpha=0.3)

    mean = np.nanmean(tuning, axis=0)
    sem = np.nanstd(tuning, axis=0) / np.sqrt(n_cells)

    ax[1].errorbar(possible, mean, yerr=sem, marker="o", capsize=4, lw=2)
    if sound_type in ["frequency", "AM"]:
        ax[1].set_xscale("log")
    ax[1].set_xticks(possible)
    ax[1].set_xticklabels(labels, rotation=45)
    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("Mean ΔF/F")
    ax[1].set_title(f"Average tuning (n={n_cells})")
    ax[1].grid(alpha=0.3)

    savefig(fig, output_dir, f"{prefix}_all_cell_tuning.png", dpi)


def plot_tuning_raster(tuning, possible, sound_type, prefix, output_dir, dpi):
    best_idx = np.nanargmax(tuning, axis=1)
    order = np.argsort(possible[best_idx])
    t = tuning[order]
    t_norm = t / np.nanmax(t, axis=1, keepdims=True)

    labels, xlabel = xlabels_for_stim(possible, sound_type)

    fig, ax = plt.subplots(figsize=(6, 8))
    im = ax.imshow(t_norm, aspect="auto", cmap="viridis")
    fig.colorbar(im, ax=ax, label="Normalized response")
    ax.set_xticks(np.arange(len(possible)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Neurons sorted by preferred stimulus")
    ax.set_title("Tuning raster")

    savefig(fig, output_dir, f"{prefix}_tuning_raster.png", dpi)


def plot_red_diagnostics(suite2p_dir, stat, iscell_full, red_mean, thresh, method, prefix, output_dir, dpi):
    ops = np.load(suite2p_dir / "ops.npy", allow_pickle=True).item()
    red = ops["meanImg_chan2"]

    is_cell = iscell_full[:, 0].astype(bool)
    red_values = red_mean[is_cell]

    fig, ax = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

    counts, bins, _ = ax[0].hist(red_values, bins=60)
    ax[0].axvline(thresh, color="red", ls="--", lw=2)
    ax[0].set_title(f"Red intensity ({method})")
    ax[0].set_xlabel("Mean red intensity")
    ax[0].set_ylabel("Cells")

    counts2, bins2, _ = ax[1].hist(red_values, bins=60)
    ax[1].axvline(thresh, color="red", ls="--", lw=2)
    if len(counts2) > 1:
        ax[1].set_ylim(0, counts2[1] * 1.05)
    ax[1].set_title("Zoomed y-axis")
    ax[1].set_xlabel("Mean red intensity")
    ax[1].set_ylabel("Cells")

    savefig(fig, output_dir, f"{prefix}_red_hist.png", dpi)

    red_disp = norm_img(red)
    h, w = red.shape

    roi_mask = np.zeros((h, w), dtype=bool)
    for s in stat:
        roi_mask[s["ypix"].astype(int), s["xpix"].astype(int)] = True

    outline = roi_mask & (~binary_erosion(roi_mask))

    thresholds = [thresh, (2/3)*thresh, (1/3)*thresh]
    titles = ["threshold", "2/3 threshold", "1/3 threshold"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)

    for ax, th, title in zip(axes, thresholds, titles):
        red_mask = np.zeros((h, w), dtype=bool)

        for i, s in enumerate(stat):
            if is_cell[i] and red_mean[i] > th:
                red_mask[s["ypix"].astype(int), s["xpix"].astype(int)] = True

        rgb = np.zeros((h, w, 3))
        rgb[..., 0] = 0.2 * red_disp
        rgb[..., 0][red_mask] = 1
        rgb[..., 1][outline] = 0.8
        rgb[..., 0][outline] = 0.2

        ax.imshow(rgb)
        ax.set_title(title)
        ax.axis("off")

    savefig(fig, output_dir, f"{prefix}_red_threshold_panels.png", dpi)


def plot_example_cell(tuning, possible, trials_each, eventlocked, tvec, sound_type, resp_start, resp_end,
                      min_response, prefix, output_dir, dpi, kind="low"):
    best_idx = np.nanargmax(tuning, axis=1)
    best = possible[best_idx]
    peak = np.nanmax(tuning, axis=1)

    if kind == "low":
        threshold = np.percentile(possible, 30)
        candidates = np.where((best <= threshold) & (peak > min_response))[0]
    else:
        threshold = np.percentile(possible, 70)
        candidates = np.where((best >= threshold) & (peak > min_response))[0]

    if len(candidates) == 0:
        print(f"No {kind} example cells found.")
        return

    cell_idx = np.random.choice(candidates)
    cell_data = eventlocked[cell_idx]

    n_stim = len(possible)
    freq_response = np.full((n_stim, len(tvec)), np.nan)

    for k in range(n_stim):
        tr = trials_each[:, k]
        if tr.sum() > 0:
            freq_response[k] = np.nanmean(cell_data[tr], axis=0)

    labels, xlabel = xlabels_for_stim(possible, sound_type)

    fig, ax = plt.subplots(2, 1, figsize=(7, 8), constrained_layout=True)

    im = ax[0].imshow(
        freq_response,
        aspect="auto",
        extent=[tvec[0], tvec[-1], 0, n_stim],
        origin="lower",
        cmap="viridis"
    )
    ax[0].axvline(0, color="red", lw=1)

    rect = Rectangle(
        (resp_start, 0),
        resp_end - resp_start,
        n_stim,
        edgecolor="red",
        facecolor="none",
        linestyle="--",
        linewidth=2,
    )
    ax[0].add_patch(rect)

    ax[0].set_yticks(np.arange(n_stim) + 0.5)
    ax[0].set_yticklabels(labels)
    ax[0].set_ylabel(xlabel)
    ax[0].set_title(f"{kind} example cell {cell_idx}")
    fig.colorbar(im, ax=ax[0], label="dF/F")

    ax[1].plot(possible, tuning[cell_idx], "o-", lw=2)
    if sound_type in ["frequency", "AM"]:
        ax[1].set_xscale("log")
    ax[1].set_xticks(possible)
    ax[1].set_xticklabels(labels, rotation=45)
    ax[1].set_xlabel(xlabel)
    ax[1].set_ylabel("ΔF/F")
    ax[1].set_title("Tuning")
    ax[1].grid(alpha=0.3)

    savefig(fig, output_dir, f"{prefix}_{kind}_example_cell{cell_idx}.png", dpi)


def plot_trace_overlay(tuning, possible, trials_each, eventlocked, tvec, sound_type, resp_start, resp_end,
                       min_response, prefix, output_dir, dpi):
    best_idx = np.nanargmax(tuning, axis=1)
    peak = np.nanmax(tuning, axis=1)
    candidates = np.where(peak > min_response)[0]

    if len(candidates) == 0:
        return

    cell_idx = candidates[np.argmax(peak[candidates])]
    best_stim = possible[best_idx[cell_idx]]

    target_vals = [possible[0], possible[len(possible)//2], possible[-1], best_stim]
    target_vals = list(dict.fromkeys(target_vals))

    fig, ax = plt.subplots(figsize=(7, 5))
    cmap = plt.colormaps["viridis"]
    colors = cmap(np.linspace(0, 1, len(target_vals)))

    cell_data = eventlocked[cell_idx]

    for stim_val, color in zip(target_vals, colors):
        k = np.argmin(np.abs(possible - stim_val)) if np.issubdtype(possible.dtype, np.number) else np.where(possible == stim_val)[0][0]
        trials = trials_each[:, k]
        data = cell_data[trials]

        mean = np.nanmean(data, axis=0)
        sem = np.nanstd(data, axis=0) / np.sqrt(max(1, data.shape[0]))

        label = str(stim_val)
        if sound_type == "frequency":
            label = f"{stim_val/1000:.1f} kHz"
        elif sound_type == "AM":
            label = f"{stim_val:.0f} Hz"
        if stim_val == best_stim:
            label += " (best)"

        ax.plot(tvec, mean, color=color, lw=2.5 if stim_val == best_stim else 2, label=label)
        ax.fill_between(tvec, mean-sem, mean+sem, color=color, alpha=0.25)

    ax.axvline(0, color="red", lw=1)
    ax.axvspan(resp_start, resp_end, color="red", alpha=0.08)
    ax.set_xlabel("Time from sound onset (s)")
    ax.set_ylabel("dF/F")
    ax.set_title(f"Cell {cell_idx} response traces")
    ax.legend(frameon=False)

    savefig(fig, output_dir, f"{prefix}_trace_overlay_cell{cell_idx}.png", dpi)


def plot_red_split_raster(tuning, possible, redcell, sound_type, prefix, output_dir, dpi):
    labels, xlabel = xlabels_for_stim(possible, sound_type)

    t_g = sort_norm(tuning[~redcell], possible)
    t_r = sort_norm(tuning[redcell], possible)

    fig, ax = plt.subplots(1, 2, figsize=(12, 8), constrained_layout=True)

    im0 = ax[0].imshow(t_g, aspect="auto", cmap="viridis") if t_g.size else None
    ax[0].set_title(f"Green only (n={(~redcell).sum()})")

    im1 = ax[1].imshow(t_r, aspect="auto", cmap="viridis") if t_r.size else None
    ax[1].set_title(f"Green + red (n={redcell.sum()})")

    for a in ax:
        a.set_xticks(np.arange(len(possible)))
        a.set_xticklabels(labels, rotation=45)
        a.set_xlabel(xlabel)
        a.set_ylabel("Neurons sorted by preferred stimulus")

    im = im0 if im0 is not None else im1
    if im is not None:
        fig.colorbar(im, ax=ax, label="Normalized response")

    savefig(fig, output_dir, f"{prefix}_red_split_raster.png", dpi)


def plot_spatial_maps(tuning, possible, eventlocked, redcell, inds, stat, suite2p_dir,
                      sound_type, prefix, output_dir, dpi):
    ops = np.load(suite2p_dir / "ops.npy", allow_pickle=True).item()
    mean_red = ops["meanImg_chan2"]
    mean_green = ops["meanImg"]

    yc = np.array([s["med"][0] for s in stat])[inds]
    xc = np.array([s["med"][1] for s in stat])[inds]

    best_idx = np.nanargmax(tuning, axis=1)
    pref = possible[best_idx]

    dff_flat = eventlocked.reshape(eventlocked.shape[0], -1)
    skewness = np.clip(skew(dff_flat, axis=1, nan_policy="omit"), -2, 2)

    vmin_r, vmax_r = np.percentile(mean_red, [1, 99])
    vmin_g, vmax_g = np.percentile(mean_green, [1, 99])

    edgecolors = ["yellow" if r else "lime" for r in redcell]
    linewidths = [2 if r else 1.2 for r in redcell]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

    ax[0].imshow(mean_red, cmap="gray", vmin=vmin_r, vmax=vmax_r)
    sc0 = ax[0].scatter(xc, yc, c=pref, cmap="plasma", s=60, edgecolors=edgecolors, linewidths=linewidths)
    ax[0].set_title(f"Preferred {sound_type}")
    ax[0].axis("off")

    ax[1].imshow(mean_green, cmap="gray", vmin=vmin_g, vmax=vmax_g)
    sc1 = ax[1].scatter(xc, yc, c=skewness, cmap="coolwarm", vmin=-2, vmax=2, s=60,
                        edgecolors=edgecolors, linewidths=linewidths)
    ax[1].set_title("dF/F skewness")
    ax[1].axis("off")

    fig.colorbar(sc0, ax=ax[0], label=f"Preferred {sound_type}")
    fig.colorbar(sc1, ax=ax[1], label="Skewness clipped ±2")

    savefig(fig, output_dir, f"{prefix}_spatial_maps.png", dpi)


# ============================================================
# Per-session runner
# ============================================================

def run_one_session(row, args):
    subject = str(row["subject"])
    date = str(row["date"])
    session = str(row["session"]).zfill(3)
    plane = int(row["plane"])
    paradigm = str(row["paradigm"])
    sound_type = str(row["sound_type"])
    suite2p_dir = Path(row["suite2p_dir"]).expanduser().resolve()
    output_dir = Path(row["output_dir"]).expanduser().resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    prefix = f"{subject}_{date}_{session}_p{plane}"

    print("\n" + "=" * 70)
    print(f"Running {prefix} | {paradigm} | {sound_type}")
    print("=" * 70)

    data2p = twophotonanalysis.TwoPhoton(
        subject, date, session, plane, paradigm=paradigm
    )
    data2p.filter_cells(prob_threshold=args.prob_threshold)

    stim_all, stim_key = get_sound_vector(data2p, sound_type)
    match_trials(data2p, stim_all, stim_key)

    eventlocked, tvec, valid_events = data2p.event_locked_average(
        time_range=[args.time_start, args.time_end],
        dff=True
    )

    stim = np.asarray(data2p.bdata[stim_key])[valid_events]

    inds, stat, iscell_full = align_cells(data2p, suite2p_dir)
    redcell_full, red_mean, thresh, method = classify_red_cells(suite2p_dir, stat, iscell_full)
    redcell = redcell_full[inds]

    print(f"Red classification: {method}, threshold={thresh:.3f}")
    print(f"Cells: {eventlocked.shape[0]}")
    print(f"Green only: {(~redcell).sum()}")
    print(f"Green + red: {redcell.sum()}")

    tuning, possible, trials_each = compute_tuning(
        eventlocked, tvec, stim,
        args.resp_start, args.resp_end,
        args.min_trials
    )

    plot_eventlocked_qc(eventlocked, tvec, prefix, output_dir, args.dpi)
    plot_all_cell_tuning(tuning, possible, sound_type, prefix, output_dir, args.dpi)
    plot_tuning_raster(tuning, possible, sound_type, prefix, output_dir, args.dpi)
    plot_red_diagnostics(suite2p_dir, stat, iscell_full, red_mean, thresh, method, prefix, output_dir, args.dpi)
    plot_example_cell(tuning, possible, trials_each, eventlocked, tvec, sound_type,
                      args.resp_start, args.resp_end, args.min_response,
                      prefix, output_dir, args.dpi, kind="low")
    plot_example_cell(tuning, possible, trials_each, eventlocked, tvec, sound_type,
                      args.resp_start, args.resp_end, args.min_response,
                      prefix, output_dir, args.dpi, kind="high")
    plot_trace_overlay(tuning, possible, trials_each, eventlocked, tvec, sound_type,
                       args.resp_start, args.resp_end, args.min_response,
                       prefix, output_dir, args.dpi)
    plot_red_split_raster(tuning, possible, redcell, sound_type, prefix, output_dir, args.dpi)
    plot_spatial_maps(tuning, possible, eventlocked, redcell, inds, stat, suite2p_dir,
                      sound_type, prefix, output_dir, args.dpi)

    print(f"Finished {prefix}")


def main():
    args = parse_args()

    batch_csv = Path(args.batch_csv).expanduser().resolve()
    df = pd.read_csv(batch_csv, dtype={"date": str, "session": str})

    required = {
        "subject", "date", "session", "plane",
        "paradigm", "sound_type", "suite2p_dir", "output_dir"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Batch CSV missing columns: {missing}")

    results = []

    for idx, row in df.iterrows():
        try:
            run_one_session(row, args)
            results.append({"row": idx, "status": "ok", "error": ""})
        except Exception as e:
            print(f"\nFAILED row {idx}: {e}")
            traceback.print_exc()
            results.append({"row": idx, "status": "failed", "error": str(e)})

    summary = pd.DataFrame(results)
    summary_path = batch_csv.with_name(batch_csv.stem + "_run_summary.csv")
    summary.to_csv(summary_path, index=False)
    print(f"\nSaved run summary: {summary_path}")


if __name__ == "__main__":
    main()