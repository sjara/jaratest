#!/usr/bin/env python3
"""
sound_tuning_redcell_cli.py

Clean CLI pipeline converted from the AM/frequency two-photon notebook.

Examples
--------
AM tuning session:
python sound_tuning_redcell_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0 \
  --output-dir /data/twophoton/imag029_processed/20260424/006/analysis_outputs

Frequency tuning session:
python sound_tuning_redcell_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --suite2p-dir /data/twophoton/imag025_processed/20260417/000/suite2p/plane0 \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs

Natural sound session:
python sound_tuning_redcell_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm natural_sounds --sound-type natural --stim-key soundID \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0 \
  --output-dir /data/twophoton/imag029_processed/20260424/006/analysis_outputs

This script:
- Loads a jaratoolbox TwoPhoton object and associated behavior.
- Loads Suite2p plane outputs.
- Filters cells once.
- Matches behavior trials to 2p event onsets.
- Computes event-locked dF/F.
- Computes baseline-corrected stimulus tuning curves.
- Aligns data2p filtered cells to full Suite2p cell labels.
- Splits cells into green-only and tdTomato+/red classes.
- Saves final figures from the notebook workflow.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.ndimage import binary_erosion
from scipy.stats import skew

try:
    from sklearn.mixture import GaussianMixture
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

from jaratoolbox import behavioranalysis, twophotonanalysis


# =============================================================================
# Data containers
# =============================================================================

@dataclass
class Suite2PData:
    suite2p_dir: Path
    ops: dict
    stat: np.ndarray
    iscell_full: np.ndarray
    redcell_full: np.ndarray | None
    mean_green: np.ndarray
    mean_red: np.ndarray | None


@dataclass
class AnalysisData:
    data2p: object
    eventlocked: np.ndarray
    tvec: np.ndarray
    valid_events: np.ndarray
    stim: np.ndarray
    possible_stim: np.ndarray
    trials_each_stim: np.ndarray
    tuning_curves: np.ndarray
    suite2p_indices: np.ndarray
    redcell: np.ndarray
    green_not_red: np.ndarray
    green_and_red: np.ndarray
    red_mean_full: np.ndarray | None
    red_threshold: float | None
    red_method: str


# =============================================================================
# CLI
# =============================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Reproducible two-photon sound-tuning analysis with red-cell split."
    )

    # Session identity
    p.add_argument("--subject", required=True)
    p.add_argument("--date", required=True, help="YYYYMMDD")
    p.add_argument("--session", required=True, help="Session string, e.g. 006")
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--paradigm", default="am_tuning")

    # Paths
    p.add_argument("--suite2p-dir", required=True, type=Path, help="Path to suite2p/planeN")
    p.add_argument("--output-dir", required=True, type=Path)

    # Stimulus selection
    p.add_argument("--sound-type", choices=["AM", "frequency", "natural"], default="AM")
    p.add_argument(
        "--stim-key",
        default=None,
        help=(
            "Behavior key containing stimulus identity. Defaults to currentFreq for AM/frequency. "
            "For natural sounds, tries soundID/currentSound/soundType/stimID unless provided."
        ),
    )

    # Preprocessing / response windows
    p.add_argument("--prob-threshold", type=float, default=0.5)
    p.add_argument("--eventlocked-time-start", type=float, default=-1.0)
    p.add_argument("--eventlocked-time-end", type=float, default=3.0)
    p.add_argument("--tuning-time-start", type=float, default=-1.0)
    p.add_argument("--tuning-time-end", type=float, default=1.0)
    p.add_argument("--response-start", type=float, default=0.0)
    p.add_argument("--response-end", type=float, default=0.5)
    p.add_argument("--min-trials", type=int, default=3)
    p.add_argument("--min-response", type=float, default=0.02)

    # Red-cell classification
    p.add_argument(
        "--red-source",
        choices=["redcell", "gmm", "percentile", "auto"],
        default="auto",
        help="Use Suite2p redcell.npy, GMM from mean red image, percentile from mean red image, or auto.",
    )
    p.add_argument("--red-percentile", type=float, default=95.0)

    # Plot/output controls
    p.add_argument("--dpi", type=int, default=180)
    p.add_argument("--spatial-dpi", type=int, default=140)
    p.add_argument("--random-seed", type=int, default=0)
    p.add_argument("--make-frequency-tonotopy", action="store_true")
    p.add_argument("--no-examples", action="store_true")
    p.add_argument("--verbose", action="store_true")

    return p.parse_args()


# =============================================================================
# Generic utilities
# =============================================================================

def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def ensure_dir(path: Path) -> Path:
    path = path.expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def savefig(fig: plt.Figure, path: Path, dpi: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pil_kwargs={"compress_level": 9})
    plt.close(fig)
    print(f"[saved] {path}")


def robust_norm(img: np.ndarray, low: float = 2, high: float = 98, gamma: float = 1.0) -> np.ndarray:
    lo, hi = np.percentile(img, [low, high])
    if hi <= lo:
        return np.zeros_like(img, dtype=float)
    out = np.clip((img - lo) / (hi - lo), 0, 1)
    return out ** gamma


def get_stim_labels(possible_stim: np.ndarray, sound_type: str) -> tuple[list[str], str]:
    if sound_type == "AM":
        return [f"{x:.0f}" for x in possible_stim], "AM rate (Hz)"
    if sound_type == "frequency":
        return [f"{x / 1000:.1f}" for x in possible_stim], "Frequency (kHz)"
    return [str(x) for x in possible_stim], "Stimulus"


def maybe_log_x(ax: plt.Axes, sound_type: str) -> None:
    if sound_type in {"AM", "frequency"}:
        ax.set_xscale("log")


def sort_and_normalize(tuning: np.ndarray, possible_stim: np.ndarray) -> np.ndarray:
    if tuning.size == 0 or tuning.shape[0] == 0:
        return tuning

    valid = np.isfinite(tuning).any(axis=1)
    tuning = tuning[valid]
    if tuning.shape[0] == 0:
        return tuning

    best_idx = np.nanargmax(tuning, axis=1)
    order = np.argsort(possible_stim[best_idx])
    tuning_sorted = tuning[order]

    denom = np.nanmax(tuning_sorted, axis=1, keepdims=True)
    denom[denom == 0] = np.nan
    return tuning_sorted / denom


# =============================================================================
# Loading
# =============================================================================

def load_suite2p(suite2p_dir: Path) -> Suite2PData:
    suite2p_dir = suite2p_dir.expanduser().resolve()

    for name in ["ops.npy", "stat.npy", "iscell.npy"]:
        require_file(suite2p_dir / name)

    ops = np.load(suite2p_dir / "ops.npy", allow_pickle=True).item()
    stat = np.load(suite2p_dir / "stat.npy", allow_pickle=True)
    iscell_full = np.load(suite2p_dir / "iscell.npy", allow_pickle=True)

    redcell_path = suite2p_dir / "redcell.npy"
    redcell_full = None
    if redcell_path.exists():
        redcell_full = np.load(redcell_path, allow_pickle=True)[:, 0].astype(bool)

    mean_green = ops.get("meanImg", None)
    mean_red = ops.get("meanImg_chan2", None)

    if mean_green is None:
        raise KeyError("ops.npy does not contain meanImg")
    if mean_red is None:
        print("[warn] ops.npy does not contain meanImg_chan2; red-channel figures will be limited.")

    print("[load] Suite2p")
    print(f"       dir          : {suite2p_dir}")
    print(f"       stat shape   : {stat.shape}")
    print(f"       iscell shape : {iscell_full.shape}")
    print(f"       mean green   : {mean_green.shape}")
    print(f"       mean red     : {None if mean_red is None else mean_red.shape}")
    print(f"       redcell.npy  : {redcell_full is not None}")

    return Suite2PData(
        suite2p_dir=suite2p_dir,
        ops=ops,
        stat=stat,
        iscell_full=iscell_full,
        redcell_full=redcell_full,
        mean_green=mean_green,
        mean_red=mean_red,
    )


def load_twophoton(args: argparse.Namespace):
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
    print(f"       bdata keys: {list(data2p.bdata.keys())[:10]} ...")

    data2p.filter_cells(prob_threshold=args.prob_threshold)

    print("[preprocess] filtered cells")
    print(f"       prob threshold : {args.prob_threshold}")
    print(f"       roiF           : {data2p.roiF.shape}")
    print(f"       iscell         : {data2p.iscell.shape}")

    return data2p


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


def match_trial_count(data2p, stim_all: np.ndarray, stim_key: str) -> np.ndarray:
    n_trials_2p = len(data2p.event_onset)
    n_trials_behavior = len(stim_all)

    if n_trials_2p < n_trials_behavior:
        print(f"[warn] truncating behavior trials: {n_trials_behavior} -> {n_trials_2p}")
        stim_all = stim_all[:n_trials_2p]
        data2p.bdata[stim_key] = data2p.bdata[stim_key][:n_trials_2p]
    elif n_trials_2p > n_trials_behavior:
        print(f"[warn] truncating 2p event_onset: {n_trials_2p} -> {n_trials_behavior}")
        data2p.event_onset = data2p.event_onset[:n_trials_behavior]

    return stim_all


# =============================================================================
# Computation
# =============================================================================

def compute_eventlocked(data2p, time_range: tuple[float, float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=list(time_range), dff=True)
    print("[compute] eventlocked")
    print(f"          time range   : {time_range}")
    print(f"          eventlocked  : {eventlocked.shape}")
    print(f"          tvec         : {tvec.shape}")
    print(f"          valid events : {valid_events.sum()} / {len(valid_events)}")
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
    print(f"          stim values : {possible_stim}")
    print(f"          tuning      : {tuning.shape}")
    print(f"          response win: ({response_start}, {response_end})")
    return tuning, possible_stim, trials_each_stim


def align_data2p_to_suite2p(data2p, suite: Suite2PData) -> np.ndarray:
    """Map currently filtered data2p cells to full Suite2p rows using iscell rows."""
    indices = []
    for row in data2p.iscell:
        matches = np.where(
            (suite.iscell_full[:, 0] == row[0])
            & (np.isclose(suite.iscell_full[:, 1], row[1]))
        )[0]
        if len(matches) == 0:
            raise ValueError(
                "Could not match a filtered data2p cell to Suite2p iscell.npy. "
                "This usually means data2p and --suite2p-dir are not from the same run/session."
            )
        indices.append(matches[0])

    indices = np.asarray(indices, dtype=int)
    print("[compute] cell alignment")
    print(f"          aligned cells: {len(indices)}")
    return indices


def red_mean_from_image(suite: Suite2PData) -> np.ndarray | None:
    if suite.mean_red is None:
        return None
    return np.array([
        suite.mean_red[s["ypix"].astype(int), s["xpix"].astype(int)].mean()
        for s in suite.stat
    ])


def classify_red_cells(
    suite: Suite2PData,
    red_source: str,
    percentile: float,
) -> tuple[np.ndarray, np.ndarray | None, float | None, str]:
    """Return red labels for all Suite2p ROIs."""
    red_mean = red_mean_from_image(suite)

    if red_source in {"redcell", "auto"} and suite.redcell_full is not None:
        print("[compute] red classification from redcell.npy")
        return suite.redcell_full.copy(), red_mean, None, "redcell.npy"

    if suite.mean_red is None or red_mean is None:
        raise ValueError("No red mean image available and redcell.npy unavailable.")

    is_cell = suite.iscell_full[:, 0].astype(bool)
    red_values = red_mean[is_cell]

    if red_source in {"gmm", "auto"} and HAS_SKLEARN and len(red_values) >= 10:
        X = red_values.reshape(-1, 1)
        gmm = GaussianMixture(n_components=2, random_state=0).fit(X)
        means = gmm.means_.flatten()
        stds = np.sqrt(gmm.covariances_.flatten())
        weights = gmm.weights_.flatten()

        order = np.argsort(means)
        means = means[order]
        stds = stds[order]
        weights = weights[order]

        x = np.linspace(red_values.min(), red_values.max(), 2000)

        def gaussian(vals, mu, sigma, weight):
            return weight * (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
                -((vals - mu) ** 2) / (2 * sigma**2)
            )

        g1 = gaussian(x, means[0], stds[0], weights[0])
        g2 = gaussian(x, means[1], stds[1], weights[1])
        threshold = float(x[np.argmin(np.abs(g1 - g2))])
        method = "GMM"
    else:
        threshold = float(np.percentile(red_values, percentile))
        method = f"p{percentile:g}"

    red_labels = red_mean > threshold
    print("[compute] red classification")
    print(f"          method       : {method}")
    print(f"          threshold    : {threshold:.4g}")
    print(f"          red-positive : {red_labels.sum()} / {len(red_labels)}")
    return red_labels, red_mean, threshold, method


def build_analysis(args: argparse.Namespace) -> tuple[Suite2PData, AnalysisData]:
    suite = load_suite2p(args.suite2p_dir)
    data2p = load_twophoton(args)

    stim_key = infer_stim_key(data2p, args.sound_type, args.stim_key)
    stim_all = np.asarray(data2p.bdata[stim_key])
    stim_all = match_trial_count(data2p, stim_all, stim_key)

    # Main tuning eventlocked window.
    eventlocked, tvec, valid_events = compute_eventlocked(
        data2p, (args.tuning_time_start, args.tuning_time_end)
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

    suite2p_indices = align_data2p_to_suite2p(data2p, suite)
    redcell_full, red_mean_full, red_threshold, red_method = classify_red_cells(
        suite, args.red_source, args.red_percentile
    )

    redcell = redcell_full[suite2p_indices].astype(bool)
    green_not_red = ~redcell
    green_and_red = redcell

    print("[summary] cell classes")
    print(f"          total filtered cells : {len(redcell)}")
    print(f"          green only           : {green_not_red.sum()}")
    print(f"          green + red          : {green_and_red.sum()}")

    analysis = AnalysisData(
        data2p=data2p,
        eventlocked=eventlocked,
        tvec=tvec,
        valid_events=valid_events,
        stim=stim,
        possible_stim=possible_stim,
        trials_each_stim=trials_each_stim,
        tuning_curves=tuning,
        suite2p_indices=suite2p_indices,
        redcell=redcell,
        green_not_red=green_not_red,
        green_and_red=green_and_red,
        red_mean_full=red_mean_full,
        red_threshold=red_threshold,
        red_method=red_method,
    )
    return suite, analysis


# =============================================================================
# Plotting
# =============================================================================

def plot_eventlocked_average(args, output_dir: Path, data2p) -> None:
    eventlocked, tvec, valid_events = compute_eventlocked(
        data2p, (args.eventlocked_time_start, args.eventlocked_time_end)
    )
    trialavg = np.nanmean(eventlocked, axis=1)
    n_cells = eventlocked.shape[0]

    fig = plt.figure(figsize=(8, 6), constrained_layout=True)
    ax0 = plt.subplot(4, 1, (1, 3))
    im = ax0.imshow(
        trialavg,
        interpolation="nearest",
        extent=[args.eventlocked_time_start, args.eventlocked_time_end, n_cells, 0],
        aspect="auto",
        cmap="viridis",
    )
    fig.colorbar(im, ax=ax0, label="dF/F")
    ax0.axvline(0, color="darkred")
    ax0.set_title(
        f"Event-locked average\n{args.subject} {args.date} {args.session} p{args.plane}"
    )
    ax0.set_ylabel("Neuron")
    plt.setp(ax0.get_xticklabels(), visible=False)

    ax1 = plt.subplot(4, 1, 4, sharex=ax0)
    ax1.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    ax1.axvline(0, color="darkred")
    ax1.set_xlabel("Time from sound onset (s)")
    ax1.set_ylabel("Mean dF/F")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_eventlocked_avg.png", args.dpi)


def plot_all_tuning_curves(args, output_dir: Path, analysis: AnalysisData) -> None:
    labels, xlabel = get_stim_labels(analysis.possible_stim, args.sound_type)
    tuning = analysis.tuning_curves
    n_cells = tuning.shape[0]

    fig, axes = plt.subplots(2, 1, figsize=(8, 7), constrained_layout=True)

    for i in range(n_cells):
        axes[0].plot(analysis.possible_stim, tuning[i], "o-", alpha=0.3, lw=0.5)

    maybe_log_x(axes[0], args.sound_type)
    axes[0].set_xticks(analysis.possible_stim)
    axes[0].set_xticklabels(labels, rotation=45)
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel("ΔF/F")
    axes[0].set_title(f"{args.sound_type} tuning curves - all cells")
    axes[0].grid(True, alpha=0.3)

    mean_tuning = np.nanmean(tuning, axis=0)
    sem_tuning = np.nanstd(tuning, axis=0) / np.sqrt(n_cells)

    axes[1].errorbar(
        analysis.possible_stim,
        mean_tuning,
        yerr=sem_tuning,
        marker="o",
        capsize=5,
        lw=2,
    )
    maybe_log_x(axes[1], args.sound_type)
    axes[1].set_xticks(analysis.possible_stim)
    axes[1].set_xticklabels(labels, rotation=45)
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel("Mean ΔF/F")
    axes[1].set_title(f"Average tuning curve (n={n_cells})")
    axes[1].grid(True, alpha=0.3)

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_tuning_curves.png", args.dpi)


def plot_responsive_tuning_raster(args, output_dir: Path, analysis: AnalysisData) -> None:
    tuning = analysis.tuning_curves
    peak_response = np.nanmax(tuning, axis=1)
    responsive = peak_response > args.min_response
    tuning_resp = tuning[responsive]

    print("[plot] responsive tuning raster")
    print(f"       responsive cells: {responsive.sum()} / {tuning.shape[0]}")

    if tuning_resp.shape[0] == 0:
        print("[warn] no responsive cells; skipping raster")
        return

    best_idx = np.nanargmax(tuning_resp, axis=1)
    best_stim = analysis.possible_stim[best_idx]
    sort_idx = np.argsort(best_stim)
    tuning_sorted = tuning_resp[sort_idx]
    tuning_norm = tuning_sorted / np.nanmax(tuning_sorted, axis=1, keepdims=True)

    labels, xlabel = get_stim_labels(analysis.possible_stim, args.sound_type)

    fig, ax = plt.subplots(figsize=(6, 8), constrained_layout=True)
    im = ax.imshow(tuning_norm, aspect="auto", cmap="viridis", interpolation="nearest")
    fig.colorbar(im, ax=ax, label="Normalized response")
    ax.set_xticks(np.arange(len(analysis.possible_stim)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Neurons sorted by best stimulus")
    ax.set_title(f"{args.sound_type} tuning raster (responsive cells)")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_tuning_raster.png", args.dpi)


def plot_red_split_raster(args, output_dir: Path, analysis: AnalysisData) -> None:
    labels, xlabel = get_stim_labels(analysis.possible_stim, args.sound_type)

    tuning_gnr_norm = sort_and_normalize(
        analysis.tuning_curves[analysis.green_not_red], analysis.possible_stim
    )
    tuning_gr_norm = sort_and_normalize(
        analysis.tuning_curves[analysis.green_and_red], analysis.possible_stim
    )

    fig, ax = plt.subplots(1, 2, figsize=(12, 8), constrained_layout=True)

    if tuning_gnr_norm.shape[0] > 0:
        im0 = ax[0].imshow(tuning_gnr_norm, aspect="auto", cmap="viridis", interpolation="nearest")
    else:
        im0 = None
    ax[0].set_title(f"Green only (n={analysis.green_not_red.sum()})")

    if tuning_gr_norm.shape[0] > 0:
        im1 = ax[1].imshow(tuning_gr_norm, aspect="auto", cmap="viridis", interpolation="nearest")
    else:
        im1 = None
    ax[1].set_title(f"tdTomato+ / green+red (n={analysis.green_and_red.sum()})")

    for a in ax:
        a.set_xticks(np.arange(len(analysis.possible_stim)))
        a.set_xticklabels(labels, rotation=45)
        a.set_xlabel(xlabel)
        a.set_ylabel("Neurons sorted by best stimulus")

    im_for_cbar = im0 if im0 is not None else im1
    if im_for_cbar is not None:
        cbar = fig.colorbar(im_for_cbar, ax=ax)
        cbar.set_label("Normalized response")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_raster_red_split.png", args.dpi)


def plot_mean_image_overlays(args, output_dir: Path, suite: Suite2PData, analysis: AnalysisData) -> None:
    if suite.mean_red is None:
        print("[warn] no meanImg_chan2; skipping mean image red overlays")
        return

    yc = np.array([s["med"][0] for s in suite.stat])
    xc = np.array([s["med"][1] for s in suite.stat])

    yc_data = yc[analysis.suite2p_indices]
    xc_data = xc[analysis.suite2p_indices]

    yc_red = yc_data[analysis.green_and_red]
    xc_red = xc_data[analysis.green_and_red]
    yc_green = yc_data[analysis.green_not_red]
    xc_green = xc_data[analysis.green_not_red]

    vmin_r, vmax_r = np.percentile(suite.mean_red, [1, 99])
    vmin_g, vmax_g = np.percentile(suite.mean_green, [1, 99])

    fig, ax = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

    ax[0].imshow(suite.mean_red, cmap="gray", vmin=vmin_r, vmax=vmax_r)
    ax[1].imshow(suite.mean_green, cmap="gray", vmin=vmin_g, vmax=vmax_g)

    for a in ax:
        a.scatter(
            xc_green,
            yc_green,
            facecolors="none",
            edgecolors="lime",
            s=70,
            linewidths=1.2,
        )
        a.scatter(
            xc_red,
            yc_red,
            facecolors="none",
            edgecolors="yellow",
            s=70,
            linewidths=2,
        )
        a.axis("off")

    ax[0].set_title("Red mean image (yellow = tdTomato+)")
    ax[1].set_title("Green mean image (yellow = tdTomato+)")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_mean_images_roi_overlay.png", args.dpi)


def plot_red_hist_and_thresholds(args, output_dir: Path, suite: Suite2PData, analysis: AnalysisData) -> None:
    if suite.mean_red is None or analysis.red_mean_full is None:
        print("[warn] no red image/intensity; skipping red threshold diagnostics")
        return

    iscell = suite.iscell_full[:, 0].astype(bool)
    red_values = analysis.red_mean_full[iscell]
    threshold = analysis.red_threshold

    if threshold is None:
        # If using redcell.npy, still draw a reference percentile line for visualization.
        threshold = float(np.percentile(red_values, args.red_percentile))
        method = f"visual p{args.red_percentile:g}"
    else:
        method = analysis.red_method

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    counts, bins, _ = axes[0].hist(red_values, bins=60)
    axes[0].axvline(threshold, color="red", linestyle="--", linewidth=2)
    axes[0].set_xlabel("Mean red intensity in ROI")
    axes[0].set_ylabel("Cells")
    axes[0].set_title(f"Red intensity ({method})")

    counts_zoom, _, _ = axes[1].hist(red_values, bins=60)
    axes[1].axvline(threshold, color="red", linestyle="--", linewidth=2)
    if len(counts_zoom) > 1 and counts_zoom[1] > 0:
        axes[1].set_ylim(0, counts_zoom[1] * 1.05)
    axes[1].set_xlabel("Mean red intensity in ROI")
    axes[1].set_ylabel("Cells")
    axes[1].set_title("Zoomed y-axis")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_red_intensity_hist.png", args.dpi)

    # Three threshold panels using all green ROIs and ROI outlines.
    red_disp = robust_norm(suite.mean_red)
    h, w = suite.mean_red.shape

    roi_mask = np.zeros((h, w), dtype=bool)
    for s in suite.stat:
        roi_mask[s["ypix"].astype(int), s["xpix"].astype(int)] = True
    outline_mask = roi_mask & (~binary_erosion(roi_mask))

    thresholds = [threshold, (2 / 3) * threshold, (1 / 3) * threshold]
    titles = [
        f"{method}: {threshold:.3g}",
        f"2/3 threshold: {(2/3) * threshold:.3g}",
        f"1/3 threshold: {(1/3) * threshold:.3g}",
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)

    for ax, thresh, title in zip(axes, thresholds, titles):
        red_mask = np.zeros((h, w), dtype=bool)
        for i, s in enumerate(suite.stat):
            if iscell[i] and analysis.red_mean_full[i] > thresh:
                ypix = s["ypix"].astype(int)
                xpix = s["xpix"].astype(int)
                red_mask[ypix, xpix] = True

        rgb = np.zeros((h, w, 3))
        rgb[..., 0] = 0.2 * red_disp
        rgb[..., 0][red_mask] = 1.0
        rgb[..., 1][outline_mask] = 0.8
        rgb[..., 0][outline_mask] = 0.2

        ax.imshow(rgb)
        ax.set_title(title)
        ax.axis("off")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_red_threshold_panels.png", args.dpi)


def plot_spatial_maps(args, output_dir: Path, suite: Suite2PData, analysis: AnalysisData) -> None:
    if suite.mean_red is None:
        print("[warn] no mean red image; skipping preferred/skewness spatial maps")
        return

    yc = np.array([s["med"][0] for s in suite.stat])
    xc = np.array([s["med"][1] for s in suite.stat])
    yc_data = yc[analysis.suite2p_indices]
    xc_data = xc[analysis.suite2p_indices]

    best_idx = np.nanargmax(analysis.tuning_curves, axis=1)
    pref_stim = analysis.possible_stim[best_idx]

    dff_flat = analysis.eventlocked.reshape(analysis.eventlocked.shape[0], -1)
    skewness = skew(dff_flat, axis=1, nan_policy="omit")
    skew_clipped = np.clip(skewness, -2, 2)

    vmin_r, vmax_r = np.percentile(suite.mean_red, [1, 99])
    vmin_g, vmax_g = np.percentile(suite.mean_green, [1, 99])

    edgecolors = ["yellow" if r else "lime" for r in analysis.green_and_red]
    linewidths = [2 if r else 1.2 for r in analysis.green_and_red]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

    ax[0].imshow(suite.mean_red, cmap="gray", vmin=vmin_r, vmax=vmax_r)
    sc0 = ax[0].scatter(
        xc_data,
        yc_data,
        c=pref_stim,
        cmap="plasma",
        s=60,
        edgecolors=edgecolors,
        linewidths=linewidths,
    )
    ax[0].set_title(f"Preferred {args.sound_type}")
    ax[0].axis("off")

    ax[1].imshow(suite.mean_green, cmap="gray", vmin=vmin_g, vmax=vmax_g)
    sc1 = ax[1].scatter(
        xc_data,
        yc_data,
        c=skew_clipped,
        cmap="coolwarm",
        vmin=-2,
        vmax=2,
        s=60,
        edgecolors=edgecolors,
        linewidths=linewidths,
    )
    ax[1].set_title("dF/F skewness")
    ax[1].axis("off")

    cbar0 = fig.colorbar(sc0, ax=ax[0])
    if args.sound_type == "AM":
        cbar0.set_label("Preferred AM rate (Hz)")
    elif args.sound_type == "frequency":
        cbar0.set_label("Preferred frequency (Hz)")
    else:
        cbar0.set_label("Preferred stimulus")

    cbar1 = fig.colorbar(sc1, ax=ax[1])
    cbar1.set_label("Skewness (clipped ±2)")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_spatial_maps.png", args.spatial_dpi)


def plot_example_cells(args, output_dir: Path, analysis: AnalysisData, kind: str, rng: np.random.Generator) -> None:
    tuning = analysis.tuning_curves
    best_idx = np.nanargmax(tuning, axis=1)
    best_stim = analysis.possible_stim[best_idx]
    peak = np.nanmax(tuning, axis=1)

    if kind == "low":
        thresh = np.percentile(analysis.possible_stim, 30)
        candidates = np.where((best_stim <= thresh) & (peak > args.min_response))[0]
    elif kind == "high":
        thresh = np.percentile(analysis.possible_stim, 70)
        candidates = np.where((best_stim >= thresh) & (peak > args.min_response))[0]
    elif kind == "red":
        candidates = np.where(analysis.green_and_red & (peak > args.min_response))[0]
    else:
        raise ValueError(kind)

    if len(candidates) == 0:
        print(f"[warn] no {kind} example cells found")
        return

    cell_idx = int(rng.choice(candidates))
    cell_data = analysis.eventlocked[cell_idx]

    n_stim = len(analysis.possible_stim)
    stim_response = np.full((n_stim, len(analysis.tvec)), np.nan)
    for k in range(n_stim):
        trials = analysis.trials_each_stim[:, k]
        if trials.sum() > 0:
            stim_response[k] = np.nanmean(cell_data[trials], axis=0)

    labels, ylabel = get_stim_labels(analysis.possible_stim, args.sound_type)

    fig, axes = plt.subplots(2, 1, figsize=(7, 8), constrained_layout=True)

    im = axes[0].imshow(
        stim_response,
        aspect="auto",
        extent=[analysis.tvec[0], analysis.tvec[-1], 0, n_stim],
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
    axes[0].set_ylabel(ylabel)
    axes[0].set_title(f"{kind} example cell {cell_idx} response raster")
    fig.colorbar(im, ax=axes[0], label="dF/F")

    axes[1].plot(analysis.possible_stim, tuning[cell_idx], "o-", lw=2)
    maybe_log_x(axes[1], args.sound_type)
    axes[1].set_xticks(analysis.possible_stim)
    axes[1].set_xticklabels(labels, rotation=45)
    axes[1].set_xlabel(ylabel)
    axes[1].set_ylabel("ΔF/F")
    axes[1].set_title(f"Tuning, best={best_stim[cell_idx]}")
    axes[1].grid(True, alpha=0.3)

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_{kind}_example_cell{cell_idx}.png", args.dpi)


def plot_overlay_traces(args, output_dir: Path, analysis: AnalysisData, rng: np.random.Generator) -> None:
    tuning = analysis.tuning_curves
    peak = np.nanmax(tuning, axis=1)
    candidates = np.where(peak > args.min_response)[0]
    if len(candidates) == 0:
        print("[warn] no cells for overlay trace")
        return

    cell_idx = int(candidates[np.argmax(peak[candidates])])
    best_idx = int(np.nanargmax(tuning[cell_idx]))
    best_stim = analysis.possible_stim[best_idx]

    target_stim = [
        analysis.possible_stim[0],
        analysis.possible_stim[len(analysis.possible_stim) // 2],
        analysis.possible_stim[-1],
        best_stim,
    ]
    target_stim = list(dict.fromkeys(target_stim))

    cell_data = analysis.eventlocked[cell_idx]
    cmap = plt.colormaps["viridis"]
    colors = cmap(np.linspace(0, 1, len(target_stim)))

    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)

    for stim_value, color in zip(target_stim, colors):
        if np.issubdtype(analysis.possible_stim.dtype, np.number):
            k = int(np.argmin(np.abs(analysis.possible_stim - stim_value)))
        else:
            k = int(np.where(analysis.possible_stim == stim_value)[0][0])

        trials = analysis.trials_each_stim[:, k]
        data = cell_data[trials]
        mean_trace = np.nanmean(data, axis=0)
        sem_trace = np.nanstd(data, axis=0) / np.sqrt(max(1, data.shape[0]))

        if args.sound_type == "frequency":
            label = f"{stim_value / 1000:.1f} kHz"
        elif args.sound_type == "AM":
            label = f"{stim_value:.0f} Hz"
        else:
            label = str(stim_value)
        if stim_value == best_stim:
            label += " (best)"

        ax.plot(analysis.tvec, mean_trace, color=color, lw=2.5, label=label)
        ax.fill_between(
            analysis.tvec,
            mean_trace - sem_trace,
            mean_trace + sem_trace,
            color=color,
            alpha=0.25,
        )

    ax.axvline(0, color="red", lw=1)
    ax.axvspan(args.response_start, args.response_end, color="red", alpha=0.08)
    ax.set_xlabel("Time from sound onset (s)")
    ax.set_ylabel("dF/F")
    ax.set_title(f"Cell {cell_idx} response traces")
    ax.legend(frameon=False)

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_trace_overlay_cell{cell_idx}.png", args.dpi)


def plot_tonotopic_map_if_frequency(args, output_dir: Path, suite: Suite2PData, analysis: AnalysisData) -> None:
    if args.sound_type != "frequency":
        return
    if suite.mean_green is None:
        return

    tuning = analysis.tuning_curves
    best_freq = analysis.possible_stim[np.nanargmax(tuning, axis=1)]
    peak = np.nanmax(tuning, axis=1)
    responsive = peak > args.min_response
    inds = np.where(responsive)[0]

    if len(inds) < 3:
        print("[warn] too few responsive cells for tonotopic plane")
        return

    xpos = np.array([np.mean(analysis.data2p.stat[i]["xpix"]) for i in inds])
    ypos = np.array([np.mean(analysis.data2p.stat[i]["ypix"]) for i in inds])
    z = np.log10(best_freq[inds])

    X = np.column_stack([xpos, ypos, np.ones_like(xpos)])
    (a, b, c), *_ = np.linalg.lstsq(X, z, rcond=None)
    grad_vec = np.array([a, b])
    grad_norm = np.linalg.norm(grad_vec)
    if grad_norm == 0:
        print("[warn] zero gradient for tonotopic map")
        return
    grad_dir = grad_vec / grad_norm

    mean_img_disp = robust_norm(suite.mean_green, gamma=0.7)
    h, w = suite.mean_green.shape

    cmap = plt.colormaps["viridis"]
    log_freqs = np.log10(analysis.possible_stim)
    norm = plt.Normalize(log_freqs.min(), log_freqs.max())

    rgb_img = np.stack([mean_img_disp] * 3, axis=-1)
    for i in inds:
        roi = analysis.data2p.stat[i]
        ypix = roi["ypix"].astype(int)
        xpix = roi["xpix"].astype(int)
        color = np.array(cmap(norm(np.log10(best_freq[i])))[:3])
        rgb_img[ypix, xpix] = 0.3 * rgb_img[ypix, xpix] + 0.7 * color

    yy, xx = np.mgrid[0:h, 0:w]
    Z = a * xx + b * yy + c

    fig, ax = plt.subplots(figsize=(7, 7), constrained_layout=True)
    ax.imshow(rgb_img)

    cs = ax.contour(xx, yy, Z, levels=log_freqs, colors="white", linewidths=1)
    fmt = {lvl: f"{10**lvl / 1000:.1f}" for lvl in log_freqs}
    ax.clabel(cs, cs.levels, inline=True, fmt=fmt, fontsize=8, colors="red")

    cx, cy = w / 2, h / 2
    scale = 0.3 * min(h, w)
    dx, dy = grad_dir * scale
    ax.arrow(cx, cy, dx, dy, color="white", width=2, head_width=10)
    ax.text(cx + dx, cy + dy, "High freq", color="red", fontsize=10, fontweight="bold")
    ax.text(cx - dx, cy - dy, "Low freq", color="red", fontsize=10, fontweight="bold")

    ax.set_title("Tonotopic map")
    ax.axis("off")

    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Frequency (kHz, log scale)")

    savefig(fig, output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_tonotopic_map.png", args.dpi)


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    args = parse_args()
    args.suite2p_dir = args.suite2p_dir.expanduser().resolve()
    output_dir = ensure_dir(args.output_dir)

    np.random.seed(args.random_seed)
    rng = np.random.default_rng(args.random_seed)

    print("[start]")
    print(json.dumps({
        "subject": args.subject,
        "date": args.date,
        "session": args.session,
        "plane": args.plane,
        "paradigm": args.paradigm,
        "sound_type": args.sound_type,
        "suite2p_dir": str(args.suite2p_dir),
        "output_dir": str(output_dir),
    }, indent=2))

    suite, analysis = build_analysis(args)

    # Final notebook outputs, de-duplicated.
    plot_eventlocked_average(args, output_dir, analysis.data2p)
    plot_all_tuning_curves(args, output_dir, analysis)
    plot_responsive_tuning_raster(args, output_dir, analysis)
    plot_red_split_raster(args, output_dir, analysis)
    plot_mean_image_overlays(args, output_dir, suite, analysis)
    plot_red_hist_and_thresholds(args, output_dir, suite, analysis)
    plot_spatial_maps(args, output_dir, suite, analysis)

    if not args.no_examples:
        plot_example_cells(args, output_dir, analysis, kind="low", rng=rng)
        plot_example_cells(args, output_dir, analysis, kind="high", rng=rng)
        if analysis.green_and_red.any():
            plot_example_cells(args, output_dir, analysis, kind="red", rng=rng)
        plot_overlay_traces(args, output_dir, analysis, rng=rng)

    if args.make_frequency_tonotopy or args.sound_type == "frequency":
        plot_tonotopic_map_if_frequency(args, output_dir, suite, analysis)

    print("[done]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
