#!/usr/bin/env python3
"""
twophoton_sound_tuning_cli.py

CLI pipeline for two-photon sound tuning analysis.

This script generates sound-tuning outputs only:
  1. Event-locked average QC plot
  2. All-cell tuning curves
  3. Responsive-cell tuning raster
  4. Random low-preferred-stimulus example cell
  5. Random high-preferred-stimulus example cell
  6. Overlayed response traces for an example responsive cell
  7. Red-split tuning raster if red labels are available. If --suite2p-dir is omitted, it is inferred from settings.TWOPHOTON_PATH.

It does NOT generate green/red/yellow spatial maps or ROI colocalization overlays.

Default output directory:
  /tmp

Example calls
-------------

AM tuning:
python twophoton_sound_tuning_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM

Frequency tuning:
python twophoton_sound_tuning_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs

AM tuning with explicit Suite2p dir:
python twophoton_sound_tuning_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from jaratoolbox import behavioranalysis, twophotonanalysis, settings


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Create sound-tuning plots from two-photon sound-response data."
    )

    p.add_argument("--subject", required=True)
    p.add_argument("--date", required=True, help="YYYYMMDD")
    p.add_argument("--session", required=True, help="Session string, e.g. 006")
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--paradigm", default="am_tuning")

    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/tmp"),
        help="Output directory. Default: /tmp",
    )

    p.add_argument(
        "--suite2p-dir",
        type=Path,
        default=None,
        help=(
            "Optional path to suite2p/planeN. If omitted, defaults to "
            "settings.TWOPHOTON_PATH / '<subject>_processed' / date / session / "
            "'suite2p' / f'plane{plane}'. Used for the red-vs-non-red tuning raster. "
            "No spatial maps are produced."
        ),
    )

    p.add_argument("--sound-type", choices=["AM", "frequency", "natural"], default="AM")
    p.add_argument(
        "--stim-key",
        default=None,
        help=(
            "Behavior key containing stimulus identity. Defaults to currentFreq "
            "for AM/frequency. For natural sounds, tries soundID/currentSound/"
            "soundType/stimID unless provided."
        ),
    )

    p.add_argument("--prob-threshold", type=float, default=0.5)
    p.add_argument("--qc-prob-threshold", type=float, default=0.001)

    p.add_argument("--qc-time-start", type=float, default=-1.0)
    p.add_argument("--qc-time-end", type=float, default=3.0)

    p.add_argument("--time-start", type=float, default=-1.0)
    p.add_argument("--time-end", type=float, default=1.5)
    p.add_argument("--response-start", type=float, default=0.0)
    p.add_argument("--response-end", type=float, default=0.5)

    p.add_argument("--min-response", type=float, default=0.03)
    p.add_argument("--raster-min-response", type=float, default=0.02)
    p.add_argument("--min-trials", type=int, default=3)

    p.add_argument("--dpi", type=int, default=180)
    p.add_argument("--random-seed", type=int, default=None)

    return p.parse_args()


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def savefig(fig: plt.Figure, output_dir: Path, filename: str, dpi: int) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight", pil_kwargs={"compress_level": 9})
    plt.close(fig)
    print(f"[saved] {out_path}")
    return out_path


def infer_stim_key(data2p, sound_type: str, stim_key: str | None) -> str:
    if stim_key is not None:
        if stim_key not in data2p.bdata:
            raise KeyError(f"Requested --stim-key {stim_key!r} not found in behavior data.")
        return stim_key

    if sound_type in {"AM", "frequency"}:
        if "currentFreq" not in data2p.bdata:
            raise KeyError("Behavior data missing currentFreq; provide --stim-key.")
        return "currentFreq"

    for candidate in ["soundID", "currentSound", "soundType", "stimID"]:
        if candidate in data2p.bdata:
            return candidate

    raise KeyError("Could not infer natural-sound key; provide --stim-key.")


def match_trial_count(data2p, stim_key: str) -> None:
    stim_all = np.asarray(data2p.bdata[stim_key])
    n_trials_2p = len(data2p.event_onset)
    n_trials_behavior = len(stim_all)

    if n_trials_2p < n_trials_behavior:
        print(f"[warn] truncating behavior trials: {n_trials_behavior} -> {n_trials_2p}")
        data2p.bdata[stim_key] = data2p.bdata[stim_key][:n_trials_2p]
    elif n_trials_2p > n_trials_behavior:
        print(f"[warn] truncating 2p event_onset: {n_trials_2p} -> {n_trials_behavior}")
        data2p.event_onset = data2p.event_onset[:n_trials_behavior]


def stim_axis_labels(possible_stim: np.ndarray, sound_type: str) -> tuple[list[str], str]:
    if sound_type == "frequency":
        return [f"{x/1000:.1f}" for x in possible_stim], "Frequency (kHz)"
    if sound_type == "AM":
        return [f"{x:.0f}" for x in possible_stim], "AM rate (Hz)"
    return [str(x) for x in possible_stim], "Sound identity"


def maybe_set_log_x(ax, possible_stim: np.ndarray, sound_type: str) -> None:
    if sound_type in {"AM", "frequency"} and np.all(np.asarray(possible_stim, dtype=float) > 0):
        ax.set_xscale("log")


# -----------------------------------------------------------------------------
# Loading and core computation
# -----------------------------------------------------------------------------

def load_data(args: argparse.Namespace):
    data2p = twophotonanalysis.TwoPhoton(
        args.subject,
        args.date,
        args.session,
        args.plane,
        paradigm=args.paradigm,
    )

    print("[load] TwoPhoton")
    print(f"       data path : {data2p.data_path}")
    print(f"       roiF      : {data2p.roiF.shape}")
    print(f"       srate     : {data2p.srate}")

    return data2p


def compute_eventlocked(data2p, time_range: list[float], dff: bool = True, keep_valid_only: bool = True):
    eventlocked, tvec, valid_events = data2p.event_locked_average(
        time_range=time_range,
        dff=dff,
    )

    print("[compute] eventlocked")
    print(f"          time range   : {time_range}")
    print(f"          eventlocked raw : {eventlocked.shape}")
    print(f"          tvec            : {tvec.shape}")
    print(f"          valid events    : {valid_events.sum()} / {len(valid_events)}")

    if keep_valid_only:
        eventlocked = eventlocked[:, valid_events, :]
        print(f"          eventlocked valid-only: {eventlocked.shape}")

    return eventlocked, tvec, valid_events


def compute_tuning_curves(
    eventlocked: np.ndarray,
    tvec: np.ndarray,
    stim: np.ndarray,
    response_start: float,
    response_end: float,
    min_trials: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    possible_stim = np.unique(stim)
    trials_each_stim = behavioranalysis.find_trials_each_type(stim, possible_stim)

    n_cells = eventlocked.shape[0]
    n_stim = len(possible_stim)
    tuning = np.full((n_cells, n_stim), np.nan)

    baseline_mask = tvec < 0
    response_mask = (tvec > response_start) & (tvec < response_end)

    for k in range(n_stim):
        trials = trials_each_stim[:, k]
        if trials.sum() < min_trials:
            continue

        data_f = eventlocked[:, trials, :]
        baseline = np.nanmean(data_f[:, :, baseline_mask], axis=(1, 2))
        response = np.nanmean(data_f[:, :, response_mask], axis=(1, 2))
        tuning[:, k] = response - baseline

    print("[compute] tuning")
    print(f"          possible stim: {possible_stim}")
    print(f"          tuning       : {tuning.shape}")
    print(f"          response win : ({response_start}, {response_end})")
    return tuning, possible_stim, trials_each_stim


def normalize_rows(arr: np.ndarray) -> np.ndarray:
    denom = np.nanmax(arr, axis=1, keepdims=True)
    denom[denom == 0] = np.nan
    return arr / denom


def sort_and_normalize_by_best(tuning: np.ndarray, possible_stim: np.ndarray) -> np.ndarray:
    if tuning.shape[0] == 0:
        return tuning

    best_idx = np.nanargmax(tuning, axis=1)
    best_stim = possible_stim[best_idx]
    sort_idx = np.argsort(best_stim)
    return normalize_rows(tuning[sort_idx])


# -----------------------------------------------------------------------------
# Suite2p path resolution
# -----------------------------------------------------------------------------

def resolve_suite2p_dir(args: argparse.Namespace) -> Path | None:
    """Resolve Suite2p path.

    If --suite2p-dir is not supplied, infer it exactly like TwoPhoton:
    settings.TWOPHOTON_PATH / f"{subject}_processed" / date / session / "suite2p" / f"plane{plane}".
    """
    if args.suite2p_dir is not None:
        suite2p_dir = args.suite2p_dir.expanduser().resolve()
        source = "explicit"
    else:
        suite2p_dir = (
            Path(settings.TWOPHOTON_PATH)
            / f"{args.subject}_processed"
            / args.date
            / args.session
            / "suite2p"
            / f"plane{args.plane}"
        ).expanduser().resolve()
        source = "default"

    print("[suite2p]")
    print(f"       source : {source}")
    print(f"       dir    : {suite2p_dir}")

    if not suite2p_dir.exists():
        print("[warn] Suite2p directory not found; skipping red-split raster.")
        return None

    return suite2p_dir


# -----------------------------------------------------------------------------
# Optional red split
# -----------------------------------------------------------------------------

def align_filtered_cells_to_suite2p(data2p, iscell_full: np.ndarray) -> np.ndarray:
    indices = []
    for row in data2p.iscell:
        matches = np.where(
            (iscell_full[:, 0] == row[0])
            & (np.isclose(iscell_full[:, 1], row[1]))
        )[0]
        if len(matches) == 0:
            raise ValueError(
                "Could not match a filtered data2p cell to Suite2p iscell.npy. "
                "Check that --suite2p-dir belongs to the same session/run."
            )
        indices.append(matches[0])

    return np.asarray(indices, dtype=int)


def load_aligned_red_labels(data2p, suite2p_dir: Path) -> np.ndarray | None:
    suite2p_dir = suite2p_dir.expanduser().resolve()

    iscell_path = suite2p_dir / "iscell.npy"
    redcell_path = suite2p_dir / "redcell.npy"

    if not iscell_path.exists() or not redcell_path.exists():
        print("[warn] suite2p-dir supplied but iscell.npy/redcell.npy missing; skipping red-split raster.")
        return None

    iscell_full = np.load(iscell_path, allow_pickle=True)
    redcell_full = np.load(redcell_path, allow_pickle=True)[:, 0].astype(bool)

    inds = align_filtered_cells_to_suite2p(data2p, iscell_full)
    redcell = redcell_full[inds]

    print("[load] red labels")
    print(f"       suite2p dir      : {suite2p_dir}")
    print(f"       aligned cells    : {len(redcell)}")
    print(f"       green only       : {(~redcell).sum()}")
    print(f"       green + red      : {redcell.sum()}")

    return redcell


# -----------------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------------

def plot_eventlocked_qc(args, output_dir: Path, eventlocked: np.ndarray, tvec: np.ndarray) -> None:
    trialavg = np.nanmean(eventlocked, axis=1)
    n_cells = eventlocked.shape[0]

    fig = plt.figure(figsize=(8, 6), constrained_layout=True)

    ax0 = plt.subplot(4, 1, (1, 3))
    im = ax0.imshow(
        trialavg,
        interpolation="nearest",
        extent=[tvec[0], tvec[-1], n_cells, 0],
        aspect="auto",
        cmap="viridis",
    )
    plt.colorbar(im, ax=ax0, label="dF/F")
    ax0.axvline(0, color="darkred")
    ax0.set_title(f"Event-locked average\n{args.subject} {args.date} {args.session} p{args.plane}")
    ax0.set_ylabel("Neuron")
    plt.setp(ax0.get_xticklabels(), visible=False)

    ax1 = plt.subplot(4, 1, 4, sharex=ax0)
    ax1.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    ax1.axvline(0, color="darkred")
    ax1.set_xlabel("Time from sound onset (s)")
    ax1.set_ylabel("Mean dF/F")

    savefig(fig, output_dir, f"{args.subject}_{args.date}_{args.session}_p{args.plane}_eventlocked_avg.png", args.dpi)


def plot_all_cell_tuning(args, output_dir: Path, tuning: np.ndarray, possible_stim: np.ndarray) -> None:
    labels, xlabel = stim_axis_labels(possible_stim, args.sound_type)
    n_cells = tuning.shape[0]

    fig, axes = plt.subplots(2, 1, figsize=(8, 7), constrained_layout=True)

    for i in range(n_cells):
        axes[0].plot(possible_stim, tuning[i], "o-", alpha=0.3, lw=0.5)

    maybe_set_log_x(axes[0], possible_stim, args.sound_type)
    axes[0].set_xticks(possible_stim)
    axes[0].set_xticklabels(labels, rotation=45)
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel("ΔF/F")
    axes[0].set_title("Tuning curves - all cells")
    axes[0].grid(True, alpha=0.3)

    mean_tuning = np.nanmean(tuning, axis=0)
    sem_tuning = np.nanstd(tuning, axis=0) / np.sqrt(n_cells)

    axes[1].errorbar(
        possible_stim,
        mean_tuning,
        yerr=sem_tuning,
        marker="o",
        capsize=5,
        lw=2,
    )

    maybe_set_log_x(axes[1], possible_stim, args.sound_type)
    axes[1].set_xticks(possible_stim)
    axes[1].set_xticklabels(labels, rotation=45)
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel("Mean ΔF/F")
    axes[1].set_title(f"Average tuning curve (n={n_cells} cells)")
    axes[1].grid(True, alpha=0.3)

    suffix = "AM_tuning_curves" if args.sound_type == "AM" else f"{args.sound_type}_tuning_curves"
    savefig(fig, output_dir, f"{args.subject}_{args.date}_{args.session}_p{args.plane}_{suffix}.png", args.dpi)


def plot_responsive_tuning_raster(args, output_dir: Path, tuning: np.ndarray, possible_stim: np.ndarray) -> None:
    labels, xlabel = stim_axis_labels(possible_stim, args.sound_type)

    peak_response = np.nanmax(tuning, axis=1)
    responsive = peak_response > args.raster_min_response
    tuning_resp = tuning[responsive]

    print("[plot] responsive raster")
    print(f"       responsive : {responsive.sum()} / {len(responsive)}")

    if tuning_resp.shape[0] == 0:
        print("[warn] no responsive cells for tuning raster; skipping.")
        return

    tuning_norm = sort_and_normalize_by_best(tuning_resp, possible_stim)

    fig, ax = plt.subplots(figsize=(6, 8))
    im = ax.imshow(tuning_norm, aspect="auto", cmap="viridis", interpolation="nearest")
    fig.colorbar(im, ax=ax, label="Normalized response")

    ax.set_xticks(np.arange(len(possible_stim)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Neurons sorted by preferred stimulus")
    ax.set_title("Tuning raster (responsive cells)")

    savefig(fig, output_dir, f"{args.subject}_{args.date}_{args.session}_p{args.plane}_tuning_raster.png", args.dpi)


def plot_red_split_tuning_raster(
    args,
    output_dir: Path,
    tuning: np.ndarray,
    possible_stim: np.ndarray,
    redcell: np.ndarray | None,
) -> None:
    if redcell is None:
        return

    labels, xlabel = stim_axis_labels(possible_stim, args.sound_type)

    peak_response = np.nanmax(tuning, axis=1)
    responsive = peak_response > args.raster_min_response

    idx_resp = np.where(responsive)[0]
    idx_green_only = idx_resp[~redcell[idx_resp]]
    idx_green_red = idx_resp[redcell[idx_resp]]

    tuning_g = sort_and_normalize_by_best(tuning[idx_green_only], possible_stim)
    tuning_r = sort_and_normalize_by_best(tuning[idx_green_red], possible_stim)

    fig, axes = plt.subplots(1, 2, figsize=(12, 8), constrained_layout=True)

    im0 = None
    im1 = None

    if tuning_g.shape[0] > 0:
        im0 = axes[0].imshow(tuning_g, aspect="auto", cmap="viridis", interpolation="nearest")
        axes[0].set_title(f"Green only (n={tuning_g.shape[0]})")
    else:
        axes[0].set_title("Green only (none)")

    if tuning_r.shape[0] > 0:
        im1 = axes[1].imshow(tuning_r, aspect="auto", cmap="viridis", interpolation="nearest")
        axes[1].set_title(f"Green + red (n={tuning_r.shape[0]})")
    else:
        axes[1].set_title("Green + red (none)")

    for ax in axes:
        ax.set_xticks(np.arange(len(possible_stim)))
        ax.set_xticklabels(labels, rotation=45)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Neurons sorted by preferred stimulus")

    im_for_cbar = im0 if im0 is not None else im1
    if im_for_cbar is not None:
        fig.colorbar(im_for_cbar, ax=axes, label="Normalized response")

    savefig(fig, output_dir, f"{args.subject}_{args.date}_{args.session}_p{args.plane}_tuning_raster_split_red.png", args.dpi)


def plot_example_cell(
    args,
    output_dir: Path,
    tuning: np.ndarray,
    possible_stim: np.ndarray,
    trials_each_stim: np.ndarray,
    eventlocked: np.ndarray,
    tvec: np.ndarray,
    kind: str,
    rng: np.random.Generator,
) -> None:
    labels, xlabel = stim_axis_labels(possible_stim, args.sound_type)

    best_idx = np.nanargmax(tuning, axis=1)
    best_stim = possible_stim[best_idx]
    peak = np.nanmax(tuning, axis=1)

    if not np.issubdtype(possible_stim.dtype, np.number):
        print(f"[warn] {kind} example not meaningful for nonnumeric stimuli; skipping.")
        return

    if kind == "low":
        stim_thresh = np.percentile(possible_stim.astype(float), 30)
        candidates = np.where((best_stim <= stim_thresh) & (peak > args.min_response))[0]
    elif kind == "high":
        stim_thresh = np.percentile(possible_stim.astype(float), 70)
        candidates = np.where((best_stim >= stim_thresh) & (peak > args.min_response))[0]
    else:
        raise ValueError(kind)

    if len(candidates) == 0:
        print(f"[warn] no {kind} example cells found; skipping.")
        return

    cell_idx = int(rng.choice(candidates))
    print(f"[plot] {kind} example cell: {cell_idx}, best={best_stim[cell_idx]}")

    cell_data = eventlocked[cell_idx]
    n_stim = len(possible_stim)
    stim_response = np.full((n_stim, len(tvec)), np.nan)

    for k in range(n_stim):
        trials = trials_each_stim[:, k]
        if trials.sum() > 0:
            stim_response[k] = np.nanmean(cell_data[trials], axis=0)

    fig, axes = plt.subplots(2, 1, figsize=(7, 8), constrained_layout=True)

    im = axes[0].imshow(
        stim_response,
        aspect="auto",
        extent=[tvec[0], tvec[-1], 0, n_stim],
        cmap="viridis",
        interpolation="nearest",
        origin="lower",
    )

    axes[0].axvline(0, color="red", lw=1)

    rect = Rectangle(
        (args.response_start, 0),
        args.response_end - args.response_start,
        n_stim,
        linewidth=2,
        edgecolor="red",
        facecolor="none",
        linestyle="--",
    )
    axes[0].add_patch(rect)

    axes[0].set_yticks(np.arange(n_stim) + 0.5)
    axes[0].set_yticklabels(labels)
    axes[0].set_ylabel(xlabel)
    axes[0].set_title(f"{kind.title()} example cell {cell_idx}")
    fig.colorbar(im, ax=axes[0], label="dF/F")

    axes[1].plot(possible_stim, tuning[cell_idx], "o-", lw=2)
    maybe_set_log_x(axes[1], possible_stim, args.sound_type)
    axes[1].set_xticks(possible_stim)
    axes[1].set_xticklabels(labels, rotation=45)
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel("ΔF/F")
    axes[1].set_title("Tuning")
    axes[1].grid(True, alpha=0.3)

    savefig(fig, output_dir, f"{args.subject}_{args.date}_{args.session}_p{args.plane}_{kind}_example_cell{cell_idx}.png", args.dpi)


def plot_trace_overlay(
    args,
    output_dir: Path,
    tuning: np.ndarray,
    possible_stim: np.ndarray,
    trials_each_stim: np.ndarray,
    eventlocked: np.ndarray,
    tvec: np.ndarray,
) -> None:
    peak = np.nanmax(tuning, axis=1)
    candidates = np.where(peak > args.min_response)[0]

    if len(candidates) == 0:
        print("[warn] no responsive cells for trace overlay; skipping.")
        return

    cell_idx = int(candidates[np.nanargmax(peak[candidates])])
    best_idx = int(np.nanargmax(tuning[cell_idx]))
    best_stim = possible_stim[best_idx]

    if len(possible_stim) >= 3:
        target_vals = [possible_stim[0], possible_stim[len(possible_stim)//2], possible_stim[-1], best_stim]
    else:
        target_vals = list(possible_stim) + [best_stim]

    # remove duplicates while preserving order
    unique_targets = []
    for val in target_vals:
        if not any(val == seen for seen in unique_targets):
            unique_targets.append(val)

    cmap = plt.colormaps["viridis"]
    colors = cmap(np.linspace(0, 1, len(unique_targets)))

    cell_data = eventlocked[cell_idx]
    fig, ax = plt.subplots(figsize=(7, 5))

    for stim_val, color in zip(unique_targets, colors):
        k = np.where(possible_stim == stim_val)[0][0]
        trials = trials_each_stim[:, k]
        data = cell_data[trials]

        if data.shape[0] == 0:
            continue

        mean_trace = np.nanmean(data, axis=0)
        sem_trace = np.nanstd(data, axis=0) / np.sqrt(data.shape[0])

        if args.sound_type == "frequency":
            label = f"{stim_val/1000:.1f} kHz"
        elif args.sound_type == "AM":
            label = f"{stim_val:.0f} Hz"
        else:
            label = str(stim_val)

        if stim_val == best_stim:
            label += " (best)"
            lw = 3
        else:
            lw = 2

        ax.plot(tvec, mean_trace, color=color, lw=lw, label=label)
        ax.fill_between(tvec, mean_trace - sem_trace, mean_trace + sem_trace, color=color, alpha=0.25)

    ax.axvline(0, color="red", lw=1)
    ax.axvspan(args.response_start, args.response_end, color="red", alpha=0.08)
    ax.set_xlabel("Time from sound onset (s)")
    ax.set_ylabel("dF/F")
    ax.set_title(f"Cell {cell_idx} response traces")
    ax.legend(frameon=False)

    savefig(fig, output_dir, f"{args.subject}_{args.date}_{args.session}_p{args.plane}_cell{cell_idx}_trace_overlay.png", args.dpi)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.random_seed)

    print("[start]")
    print(f"       subject     : {args.subject}")
    print(f"       date        : {args.date}")
    print(f"       session     : {args.session}")
    print(f"       plane       : {args.plane}")
    print(f"       paradigm    : {args.paradigm}")
    print(f"       sound type  : {args.sound_type}")
    print(f"       output dir  : {output_dir}")

    suite2p_dir = resolve_suite2p_dir(args)

    data2p = load_data(args)

    # QC plot uses the low threshold from the notebook.
    data2p.filter_cells(prob_threshold=args.qc_prob_threshold)
    stim_key_qc = infer_stim_key(data2p, args.sound_type, args.stim_key)
    match_trial_count(data2p, stim_key_qc)
    eventlocked_qc, tvec_qc, _ = compute_eventlocked(
        data2p,
        [args.qc_time_start, args.qc_time_end],
        dff=True,
    )
    plot_eventlocked_qc(args, output_dir, eventlocked_qc, tvec_qc)

    # Main tuning analysis reloads data to avoid hidden state from the QC filter.
    data2p = load_data(args)
    data2p.filter_cells(prob_threshold=args.prob_threshold)

    stim_key = infer_stim_key(data2p, args.sound_type, args.stim_key)
    print(f"[preprocess] stim key: {stim_key}")
    match_trial_count(data2p, stim_key)

    eventlocked, tvec, valid_events = compute_eventlocked(
        data2p,
        [args.time_start, args.time_end],
        dff=True,
    )
    stim = np.asarray(data2p.bdata[stim_key])[valid_events]

    tuning, possible_stim, trials_each_stim = compute_tuning_curves(
        eventlocked,
        tvec,
        stim,
        args.response_start,
        args.response_end,
        args.min_trials,
    )

    print("[summary]")
    print(f"       cells        : {eventlocked.shape[0]}")
    print(f"       trials       : {eventlocked.shape[1]}")
    print(f"       stim values  : {possible_stim}")

    plot_all_cell_tuning(args, output_dir, tuning, possible_stim)
    plot_responsive_tuning_raster(args, output_dir, tuning, possible_stim)
    plot_example_cell(args, output_dir, tuning, possible_stim, trials_each_stim, eventlocked, tvec, "low", rng)
    plot_example_cell(args, output_dir, tuning, possible_stim, trials_each_stim, eventlocked, tvec, "high", rng)
    plot_trace_overlay(args, output_dir, tuning, possible_stim, trials_each_stim, eventlocked, tvec)

    redcell = None
    if suite2p_dir is not None:
        redcell = load_aligned_red_labels(data2p, suite2p_dir)
        plot_red_split_tuning_raster(args, output_dir, tuning, possible_stim, redcell)

    print("[done]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
