#!/usr/bin/env python3
"""
sound_tuning_redcell_spatial_maps_cli.py

Spatial-map-only CLI for two-photon sound tuning with red-cell classification.

Outputs exactly one PNG whose filename ends with "spatial_maps.png".
The left panel shows preferred AM rate or preferred frequency.
The right panel shows dF/F skewness.

Default output directory is /home/jarauser/tmp, but this can be overridden
with --output-dir.

Examples
--------
AM tuning:
python twophoton_green_red_colocalization_cli.py \
  --subject imag029 --date 20260424 --session 006 --plane 0 \
  --paradigm am_tuning --sound-type AM \
  --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0

Frequency tuning:
python twophoton_green_red_colocalization_cli.py \
  --subject imag025 --date 20260417 --session 000 --plane 0 \
  --paradigm tuning_curve --sound-type frequency \
  --suite2p-dir /data/twophoton/imag025_processed/20260417/000/suite2p/plane0 \
  --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import skew

try:
    from sklearn.mixture import GaussianMixture
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

from jaratoolbox import behavioranalysis, twophotonanalysis


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Create preferred-stimulus/skewness spatial maps from 2p sound tuning data."
    )

    p.add_argument("--subject", required=True)
    p.add_argument("--date", required=True, help="YYYYMMDD")
    p.add_argument("--session", required=True, help="Session string, e.g. 006")
    p.add_argument("--plane", type=int, default=0)
    p.add_argument("--paradigm", default="am_tuning")

    p.add_argument("--suite2p-dir", required=True, type=Path, help="Path to suite2p/planeN")
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/home/jarauser/tmp"),
        help="Output directory. Default: /home/jarauser/tmp",
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
    p.add_argument("--time-start", type=float, default=-1.0)
    p.add_argument("--time-end", type=float, default=1.0)
    p.add_argument("--response-start", type=float, default=0.0)
    p.add_argument("--response-end", type=float, default=0.5)
    p.add_argument("--min-trials", type=int, default=3)

    p.add_argument(
        "--red-source",
        choices=["redcell", "gmm", "percentile", "auto"],
        default="auto",
        help="Red-cell classification source. auto uses redcell.npy if present, otherwise GMM/percentile.",
    )
    p.add_argument("--red-percentile", type=float, default=95.0)

    p.add_argument("--dpi", type=int, default=140)
    p.add_argument("--marker-size", type=float, default=60.0)

    return p.parse_args()


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")


def robust_percentile_limits(img: np.ndarray, low: float = 1, high: float = 99) -> tuple[float, float]:
    vmin, vmax = np.percentile(img, [low, high])
    if vmax <= vmin:
        vmax = vmin + 1e-9
    return float(vmin), float(vmax)


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


def match_trial_count(data2p, stim_all: np.ndarray, stim_key: str) -> None:
    n_trials_2p = len(data2p.event_onset)
    n_trials_behavior = len(stim_all)

    if n_trials_2p < n_trials_behavior:
        print(f"[warn] truncating behavior trials: {n_trials_behavior} -> {n_trials_2p}")
        data2p.bdata[stim_key] = data2p.bdata[stim_key][:n_trials_2p]
    elif n_trials_2p > n_trials_behavior:
        print(f"[warn] truncating 2p event_onset: {n_trials_2p} -> {n_trials_behavior}")
        data2p.event_onset = data2p.event_onset[:n_trials_behavior]


def get_colorbar_label(sound_type: str) -> str:
    if sound_type == "AM":
        return "Preferred AM rate (Hz)"
    if sound_type == "frequency":
        return "Preferred frequency (Hz)"
    return "Preferred stimulus"


def get_panel_title(sound_type: str) -> str:
    if sound_type == "AM":
        return "Preferred AM rate"
    if sound_type == "frequency":
        return "Preferred frequency"
    return "Preferred stimulus"


# -----------------------------------------------------------------------------
# Loading and computation
# -----------------------------------------------------------------------------

def load_suite2p(suite2p_dir: Path) -> dict:
    suite2p_dir = suite2p_dir.expanduser().resolve()
    for name in ["ops.npy", "stat.npy", "iscell.npy"]:
        require_file(suite2p_dir / name)

    ops = np.load(suite2p_dir / "ops.npy", allow_pickle=True).item()
    stat = np.load(suite2p_dir / "stat.npy", allow_pickle=True)
    iscell_full = np.load(suite2p_dir / "iscell.npy", allow_pickle=True)

    mean_green = ops.get("meanImg", None)
    mean_red = ops.get("meanImg_chan2", None)
    if mean_green is None:
        raise KeyError("ops.npy does not contain meanImg")
    if mean_red is None:
        raise KeyError("ops.npy does not contain meanImg_chan2")

    redcell_path = suite2p_dir / "redcell.npy"
    redcell_full = None
    if redcell_path.exists():
        redcell_full = np.load(redcell_path, allow_pickle=True)[:, 0].astype(bool)

    print("[load] Suite2p")
    print(f"       dir          : {suite2p_dir}")
    print(f"       stat shape   : {stat.shape}")
    print(f"       iscell shape : {iscell_full.shape}")
    print(f"       mean green   : {mean_green.shape}")
    print(f"       mean red     : {mean_red.shape}")
    print(f"       redcell.npy  : {redcell_full is not None}")

    return {
        "suite2p_dir": suite2p_dir,
        "ops": ops,
        "stat": stat,
        "iscell_full": iscell_full,
        "redcell_full": redcell_full,
        "mean_green": mean_green,
        "mean_red": mean_red,
    }


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

    data2p.filter_cells(prob_threshold=args.prob_threshold)
    print("[preprocess] filtered cells")
    print(f"       prob threshold : {args.prob_threshold}")
    print(f"       roiF           : {data2p.roiF.shape}")
    print(f"       iscell         : {data2p.iscell.shape}")

    return data2p


def compute_eventlocked_and_stim(data2p, args: argparse.Namespace):
    stim_key = infer_stim_key(data2p, args.sound_type, args.stim_key)
    stim_all = np.asarray(data2p.bdata[stim_key])
    match_trial_count(data2p, stim_all, stim_key)

    eventlocked, tvec, valid_events = data2p.event_locked_average(
        time_range=[args.time_start, args.time_end],
        dff=True,
    )
    stim = np.asarray(data2p.bdata[stim_key])[valid_events]

    print("[compute] eventlocked")
    print(f"          stim key     : {stim_key}")
    print(f"          eventlocked  : {eventlocked.shape}")
    print(f"          tvec         : {tvec.shape}")
    print(f"          valid events : {valid_events.sum()} / {len(valid_events)}")

    return eventlocked, tvec, valid_events, stim, stim_key


def compute_tuning_curves(eventlocked, tvec, stim, args: argparse.Namespace):
    possible_stim = np.unique(stim)
    trials_each_stim = behavioranalysis.find_trials_each_type(stim, possible_stim)

    n_cells = eventlocked.shape[0]
    n_stim = len(possible_stim)
    tuning = np.full((n_cells, n_stim), np.nan)

    baseline_mask = tvec < 0
    response_mask = (tvec > args.response_start) & (tvec < args.response_end)

    for k in range(n_stim):
        trials = trials_each_stim[:, k]
        if trials.sum() < args.min_trials:
            continue
        data_f = eventlocked[:, trials, :]
        baseline = np.nanmean(data_f[:, :, baseline_mask], axis=(1, 2))
        response = np.nanmean(data_f[:, :, response_mask], axis=(1, 2))
        tuning[:, k] = response - baseline

    print("[compute] tuning")
    print(f"          stim values : {possible_stim}")
    print(f"          tuning      : {tuning.shape}")
    print(f"          response win: ({args.response_start}, {args.response_end})")

    return tuning, possible_stim


def align_data2p_to_suite2p(data2p, iscell_full: np.ndarray) -> np.ndarray:
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

    indices = np.asarray(indices, dtype=int)
    print("[compute] cell alignment")
    print(f"          aligned cells: {len(indices)}")
    return indices


def red_mean_from_image(mean_red: np.ndarray, stat: np.ndarray) -> np.ndarray:
    return np.array([
        mean_red[s["ypix"].astype(int), s["xpix"].astype(int)].mean()
        for s in stat
    ])


def classify_red_cells(suite: dict, args: argparse.Namespace) -> tuple[np.ndarray, str, float | None]:
    redcell_full = suite["redcell_full"]
    iscell_full = suite["iscell_full"]
    mean_red = suite["mean_red"]
    stat = suite["stat"]

    if args.red_source in {"redcell", "auto"} and redcell_full is not None:
        print("[compute] red classification from redcell.npy")
        return redcell_full.copy(), "redcell.npy", None

    red_mean = red_mean_from_image(mean_red, stat)
    is_cell = iscell_full[:, 0].astype(bool)
    red_values = red_mean[is_cell]

    if args.red_source in {"gmm", "auto"} and HAS_SKLEARN and len(red_values) >= 10:
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
        threshold = float(np.percentile(red_values, args.red_percentile))
        method = f"p{args.red_percentile:g}"

    red_labels = red_mean > threshold
    print("[compute] red classification")
    print(f"          method       : {method}")
    print(f"          threshold    : {threshold:.4g}")
    print(f"          red-positive : {red_labels.sum()} / {len(red_labels)}")
    return red_labels, method, threshold


# -----------------------------------------------------------------------------
# Plot
# -----------------------------------------------------------------------------

def plot_spatial_maps(
    args: argparse.Namespace,
    output_dir: Path,
    suite: dict,
    eventlocked: np.ndarray,
    tuning_curves: np.ndarray,
    possible_stim: np.ndarray,
    suite2p_indices: np.ndarray,
    redcell_aligned: np.ndarray,
) -> Path:
    stat = suite["stat"]
    mean_red = suite["mean_red"]
    mean_green = suite["mean_green"]

    yc = np.array([s["med"][0] for s in stat])
    xc = np.array([s["med"][1] for s in stat])
    yc_data = yc[suite2p_indices]
    xc_data = xc[suite2p_indices]

    best_idx = np.nanargmax(tuning_curves, axis=1)
    pref_stim = possible_stim[best_idx]

    dff_flat = eventlocked.reshape(eventlocked.shape[0], -1)
    skewness = skew(dff_flat, axis=1, nan_policy="omit")
    skew_clipped = np.clip(skewness, -2, 2)

    vmin_r, vmax_r = robust_percentile_limits(mean_red, 1, 99)
    vmin_g, vmax_g = robust_percentile_limits(mean_green, 1, 99)

    edgecolors = ["yellow" if r else "lime" for r in redcell_aligned]
    linewidths = [2 if r else 1.2 for r in redcell_aligned]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

    ax[0].imshow(mean_red, cmap="gray", vmin=vmin_r, vmax=vmax_r)
    sc0 = ax[0].scatter(
        xc_data,
        yc_data,
        c=pref_stim,
        cmap="plasma",
        s=args.marker_size,
        edgecolors=edgecolors,
        linewidths=linewidths,
    )
    ax[0].set_title(get_panel_title(args.sound_type))
    ax[0].axis("off")

    ax[1].imshow(mean_green, cmap="gray", vmin=vmin_g, vmax=vmax_g)
    sc1 = ax[1].scatter(
        xc_data,
        yc_data,
        c=skew_clipped,
        cmap="coolwarm",
        vmin=-2,
        vmax=2,
        s=args.marker_size,
        edgecolors=edgecolors,
        linewidths=linewidths,
    )
    ax[1].set_title("dF/F skewness")
    ax[1].axis("off")

    cbar0 = fig.colorbar(sc0, ax=ax[0])
    cbar0.set_label(get_colorbar_label(args.sound_type))

    cbar1 = fig.colorbar(sc1, ax=ax[1])
    cbar1.set_label("Skewness (clipped ±2)")

    out_path = output_dir / f"{args.subject}_{args.date}_{args.session}_p{args.plane}_spatial_maps.png"
    fig.savefig(out_path, dpi=args.dpi, bbox_inches="tight", pil_kwargs={"compress_level": 9})
    plt.close(fig)
    print(f"[saved] {out_path}")
    return out_path


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    args = parse_args()
    args.suite2p_dir = args.suite2p_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("[start]")
    print(f"       subject     : {args.subject}")
    print(f"       date        : {args.date}")
    print(f"       session     : {args.session}")
    print(f"       plane       : {args.plane}")
    print(f"       paradigm    : {args.paradigm}")
    print(f"       sound type  : {args.sound_type}")
    print(f"       suite2p dir : {args.suite2p_dir}")
    print(f"       output dir  : {output_dir}")

    suite = load_suite2p(args.suite2p_dir)
    data2p = load_twophoton(args)

    eventlocked, tvec, valid_events, stim, stim_key = compute_eventlocked_and_stim(data2p, args)
    tuning_curves, possible_stim = compute_tuning_curves(eventlocked, tvec, stim, args)

    suite2p_indices = align_data2p_to_suite2p(data2p, suite["iscell_full"])
    redcell_full, red_method, red_threshold = classify_red_cells(suite, args)
    redcell_aligned = redcell_full[suite2p_indices].astype(bool)

    print("[summary]")
    print(f"       red method       : {red_method}")
    if red_threshold is not None:
        print(f"       red threshold    : {red_threshold:.4g}")
    print(f"       filtered cells   : {len(redcell_aligned)}")
    print(f"       green only       : {(~redcell_aligned).sum()}")
    print(f"       green + red      : {redcell_aligned.sum()}")

    plot_spatial_maps(
        args=args,
        output_dir=output_dir,
        suite=suite,
        eventlocked=eventlocked,
        tuning_curves=tuning_curves,
        possible_stim=possible_stim,
        suite2p_indices=suite2p_indices,
        redcell_aligned=redcell_aligned,
    )

    print("[done]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
