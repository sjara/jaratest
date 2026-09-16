#!/usr/bin/env python3
"""
Natural-sound response and repeat-variability analysis for two-photon data.

This script is the natural-sound companion to am_tuning_area_analysis_v9.py.
It intentionally reuses the AM-v9 helper module for the finalized analysis
conventions that should remain identical across paradigms:

* Suite2p functional-cell inclusion threshold
* Cellpose GREEN/YELLOW classification from channel 2
* primary jaratoolbox dff=True traces
* whole-session-median and 60-s prestimulus-median dF/F sensitivity versions
* sign-flip responsiveness tests and Benjamini-Hochberg FDR correction
* image overlays / QC helpers

The natural-sound-specific parts are generalized rather than hard-coded to one
recording day. Sessions are discovered from <subject>_info2p.py by
paradigm == 'natural_sound_detection'. Each session is analyzed independently,
so it is valid for sessions with different sound sets, repeat counts, stimulus
durations, cortical areas, or depths.

Natural-sound trial identity
----------------------------
The preferred behavior key is `soundID`. The script also accepts `currentSound`,
`soundType`, or `stimID` when present. For taskontrol natural_sound_detection
files, soundID is mapped back to filenames using sessionData/soundsList in the
behavior H5 when available.

Condition definition
--------------------
For repeat-to-repeat variability, a "same stimulus condition" must not silently
mix experimental factors that can change the neural response. By default:

* sound identity is always part of the condition;
* sound location is automatically added if >1 location was presented;
* target intensity is automatically added if >1 intensity was presented;
* laser trials are excluded from the primary analysis.

Use --location-mode ignore or --intensity-mode ignore only if you explicitly
want to pool over those dimensions.

Responsiveness
--------------
For each natural-sound condition, trial-level response scalars are tested against
zero with two-sided Monte-Carlo sign flips. BH-FDR is applied separately across
cells within each condition. `natural_responsive_fdr` is the union across
conditions, matching the AM-v9 "condition-specific FDR then union" convention.

Repeat variability
------------------
For each cell x natural-sound condition, this script saves the individual trial
responses plus mean, sample variance, SD, and CV-like SD/|mean|. For each cell it
also estimates a pooled within-condition noise variance by subtracting the mean
response to each condition before pooling residuals. These quantities describe
repeat-to-repeat response variability to the SAME natural sound; they are not
variance across different sound identities.

The saved NPZ trial archive is the input to natural_sound_repeat_stability_v1.py,
which repeatedly subsamples k presentations to quantify how stable the estimated
mean and variance are as a function of repeat count.

Examples
--------
Analyze every natural-sound session for imag039 on one date:

    python natural_sound_response_analysis_v1.py imag039 --dates 20260717

Only selected sessions:

    python natural_sound_response_analysis_v1.py imag039 --dates 20260717 \
        --sessions 004 008

Only A2 sessions:

    python natural_sound_response_analysis_v1.py imag039 --dates 20260717 \
        --areas A2

Inspect session selection without loading imaging data:

    python natural_sound_response_analysis_v1.py imag039 --dates 20260717 --dry-run

Outputs
-------
<TEMP_OUTPUT_PATH>/evan/natural_sound_response_analysis/<subject>/<date>/<session>/
    cell_results.csv
    condition_results.csv
    condition_summary.csv
    natural_sound_trial_responses.npz
    session_summary.json
    alignment_diagnostics.json
    green_yellow_classification.npz
    classification_overlay_chan1.png
    classification_overlay_chan2.png
    repeat_count_by_condition.png
    response_profiles_*.png
    repeat_variance_distribution_*.png
    pooled_within_condition_variance_*.png
    ... QC figures ...

A subject-level manifest is written under:
<TEMP_OUTPUT_PATH>/evan/natural_sound_response_analysis/<subject>/

Dependency
----------
Keep am_tuning_area_analysis_v9.py on PYTHONPATH or in the same directory as
this script. That dependency is deliberate: the natural-sound analysis then
inherits the exact current AM-v9 classification/FDR/dF/F conventions instead of
maintaining a drifting copy.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import importlib.util
import json
import math
import re
import sys
import traceback
from pathlib import Path
from typing import Any, Iterable

import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import torch

from jaratoolbox import loadbehavior, settings, twophotonanalysis
from suite2p.detection.chan2detect import cellpose_overlap


# =============================================================================
# LOAD THE CURRENT AM-v9 CONVENTION MODULE
# =============================================================================


def _load_am_v9_module():
    """Import am_tuning_area_analysis_v9 from normal path or beside this file."""
    try:
        return importlib.import_module("am_tuning_area_analysis_v9")
    except Exception as first_exc:
        candidates = [
            Path(__file__).resolve().with_name("am_tuning_area_analysis_v9.py"),
            Path.cwd() / "am_tuning_area_analysis_v9.py",
        ]
        for candidate in candidates:
            if not candidate.exists():
                continue
            spec = importlib.util.spec_from_file_location("am_tuning_area_analysis_v9", candidate)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        raise ImportError(
            "Could not import am_tuning_area_analysis_v9.py. Put the current v9 "
            "script on PYTHONPATH or in the same directory as this script. "
            f"Original import error: {first_exc}"
        ) from first_exc


amv9 = _load_am_v9_module()


# =============================================================================
# CONSTANTS
# =============================================================================

PARADIGM = "natural_sound_detection"
SESSION_LABEL_HINT = "natsounds"
PLANE_DEFAULT = int(getattr(amv9, "PLANE_DEFAULT", 0))
CELL_PROB_THRESHOLD = float(getattr(amv9, "CELL_PROB_THRESHOLD", 0.001))
IOU_THRESHOLD = float(getattr(amv9, "IOU_THRESHOLD", 0.15))
CELLPOSE_CELLPROB_THRESHOLD = float(getattr(amv9, "CELLPOSE_CELLPROB_THRESHOLD", -0.5))
CELLPOSE_FLOW_THRESHOLD = float(getattr(amv9, "CELLPOSE_FLOW_THRESHOLD", 0.5))
CELLPOSE_DIAMETER = getattr(amv9, "CELLPOSE_DIAMETER", None)
FDR_ALPHA = float(getattr(amv9, "FDR_ALPHA", 0.05))
N_PERMUTATIONS_DEFAULT = int(getattr(amv9, "N_PERMUTATIONS_DEFAULT", 20000))
RANDOM_SEED_DEFAULT = int(getattr(amv9, "RANDOM_SEED_DEFAULT", 20260813))

# Natural-sound event locking is dynamic. We always include this much baseline
# and post-stimulus padding; the stimulus window itself is taken from targetDuration.
BASELINE_WINDOW = (-1.0, 0.0)
POST_STIM_PADDING_S = 1.0

# Alignment settings mirror AM v9, but expected behavioral timing comes from
# actual timeTarget timestamps rather than stimDur+isi.
MAX_INTERNAL_SKIP_PER_STEP = int(getattr(amv9, "MAX_INTERNAL_SKIP_PER_STEP", 3))
MAX_TOTAL_INTERNAL_SKIPS = int(getattr(amv9, "MAX_TOTAL_INTERNAL_SKIPS", 8))
MAX_LEADING_SKIP = int(getattr(amv9, "MAX_LEADING_SKIP", 3))
LEADING_VALIDATION_INTERVALS = int(getattr(amv9, "LEADING_VALIDATION_INTERVALS", 4))
ALIGN_SKIP_PENALTY_S = float(getattr(amv9, "ALIGN_SKIP_PENALTY_S", 0.25))
MIN_ALIGNMENT_COVERAGE = float(getattr(amv9, "MIN_ALIGNMENT_COVERAGE", 0.80))
MAX_MEAN_ABS_ERROR_S = float(getattr(amv9, "MAX_MEAN_ABS_ERROR_S", 0.25))
MAX_ABS_ERROR_S = float(getattr(amv9, "MAX_ABS_ERROR_S", 0.75))

GREEN_COLOR = getattr(amv9, "GREEN_COLOR", "forestgreen")
YELLOW_COLOR = getattr(amv9, "YELLOW_COLOR", "goldenrod")


# =============================================================================
# CLI / SESSION DISCOVERY
# =============================================================================


def normalize_dates(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        for piece in str(value).replace(",", " ").split():
            if len(piece) != 8 or not piece.isdigit():
                raise argparse.ArgumentTypeError(f"Invalid date {piece!r}; use YYYYMMDD.")
            out.append(piece)
    return sorted(set(out))


def normalize_sessions(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    out = []
    for value in values:
        for piece in str(value).replace(",", " ").split():
            if piece.isdigit():
                piece = f"{int(piece):03d}"
            out.append(piece)
    return sorted(set(out))


def normalize_areas(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    out = []
    for value in values:
        v = str(value).upper()
        if v == "AUV":
            v = "A2"
        if v not in {"A1", "AAF", "A2"}:
            raise argparse.ArgumentTypeError(f"Unknown area {value!r}; use A1 AAF A2/AuV.")
        out.append(v)
    return sorted(set(out))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subject")
    p.add_argument("--dates", nargs="+", required=True, help="One or more dates, YYYYMMDD.")
    p.add_argument("--sessions", nargs="+", default=None, help="Optional session subset, e.g. 004 008.")
    p.add_argument("--areas", nargs="+", default=None, help="Optional canonical area subset: A1 AAF A2.")
    p.add_argument("--plane", type=int, default=PLANE_DEFAULT)
    p.add_argument("--n-permutations", type=int, default=N_PERMUTATIONS_DEFAULT)
    p.add_argument("--seed", type=int, default=RANDOM_SEED_DEFAULT)
    p.add_argument("--min-repeats-for-variance", type=int, default=2,
                   help="Minimum same-condition repeats required to report sample variance. Default 2.")
    p.add_argument("--min-repeats-for-test", type=int, default=2,
                   help="Minimum same-condition repeats required for sign-flip responsiveness. Default 2.")
    p.add_argument("--response-start", type=float, default=0.0,
                   help="Response-window start relative to sound onset. Default 0 s.")
    p.add_argument("--response-end", type=float, default=None,
                   help="Optional fixed response-window end. Default: each trial's targetDuration.")
    p.add_argument("--location-mode", choices=["auto", "include", "ignore"], default="auto",
                   help="Whether sound location is part of the repeat condition. Default auto.")
    p.add_argument("--intensity-mode", choices=["auto", "include", "ignore"], default="auto",
                   help="Whether target intensity is part of the repeat condition. Default auto.")
    p.add_argument("--include-laser", action="store_true",
                   help="Include laser trials. Default excludes them.")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    args.dates = normalize_dates(args.dates)
    args.sessions = normalize_sessions(args.sessions)
    args.areas = normalize_areas(args.areas)
    if args.min_repeats_for_variance < 2:
        p.error("--min-repeats-for-variance must be >=2")
    if args.min_repeats_for_test < 2:
        p.error("--min-repeats-for-test must be >=2")
    if args.response_end is not None and args.response_end <= args.response_start:
        p.error("--response-end must be greater than --response-start")
    return args


def load_info2p_sessions(subject: str) -> tuple[Path, list[dict[str, Any]]]:
    return amv9.load_info2p_sessions(subject)


def select_sessions(sessions: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    dates = set(args.dates)
    session_subset = set(args.sessions) if args.sessions else None
    area_subset = set(args.areas) if args.areas else None
    selected: list[dict[str, Any]] = []
    for sess in sessions:
        date = str(sess.get("date", ""))
        session = str(sess.get("session", ""))
        if date not in dates:
            continue
        if session_subset is not None and session not in session_subset:
            continue
        if str(sess.get("paradigm", "")) != PARADIGM:
            continue
        area = amv9.canonical_brain_area(sess.get("brainArea", ""))
        if area_subset is not None and area not in area_subset:
            continue
        item = dict(sess)
        item["canonicalArea"] = area
        selected.append(item)
    selected.sort(key=lambda x: (str(x.get("date", "")), str(x.get("session", ""))))
    return selected


# =============================================================================
# H5 / BEHAVIOR HELPERS
# =============================================================================


def _decode_scalar(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    if isinstance(value, np.bytes_):
        return bytes(value).decode(errors="replace")
    if isinstance(value, np.ndarray) and value.ndim == 0:
        return _decode_scalar(value.item())
    return value


def load_sound_metadata_from_h5(path: Path) -> dict[str, Any]:
    """Read soundID->filename and enum labels directly from a taskontrol H5."""
    out: dict[str, Any] = {"sound_names": [], "enum_labels": {}}
    if not path.exists():
        return out
    with h5py.File(path, "r") as h5:
        if "sessionData/soundsList" in h5:
            raw = _decode_scalar(h5["sessionData/soundsList"][()])
            try:
                parsed = ast.literal_eval(str(raw))
                if isinstance(parsed, (list, tuple)):
                    out["sound_names"] = [str(x) for x in parsed]
            except Exception:
                pass
        if "resultsLabels" in h5:
            for param_name, grp in h5["resultsLabels"].items():
                if not isinstance(grp, h5py.Group):
                    continue
                mapping = {}
                for label, ds in grp.items():
                    try:
                        mapping[int(np.asarray(ds[()]).item())] = str(label)
                    except Exception:
                        continue
                if mapping:
                    out["enum_labels"][str(param_name)] = mapping
    return out


def infer_sound_key(bdata: Any) -> str:
    for key in ("soundID", "currentSound", "soundType", "stimID"):
        try:
            _ = bdata[key]
            return key
        except Exception:
            pass
    raise KeyError("Could not find a natural-sound identity key (soundID/currentSound/soundType/stimID).")


def get_behavior_array(bdata: Any, key: str, n: int | None = None, default: Any = None,
                       dtype: Any | None = None) -> np.ndarray:
    try:
        arr = np.asarray(bdata[key]).ravel()
    except Exception:
        if n is None:
            raise
        arr = np.full(n, default)
    if dtype is not None:
        arr = arr.astype(dtype)
    return arr


def sound_name_from_id(sound_id: Any, sound_names: list[str]) -> str:
    try:
        idx = int(sound_id)
    except Exception:
        return str(sound_id)
    if 0 <= idx < len(sound_names):
        return sound_names[idx]
    return f"sound_{idx}"


# =============================================================================
# NATURAL-SOUND EVENT ALIGNMENT
# =============================================================================


def align_events_to_behavior_times(
    data2p,
    eventlocked: np.ndarray,
    valid_events: np.ndarray,
    behavior_target_times: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    """Monotonic event alignment using actual target-onset times from behavior.

    This is the natural-sound analogue of AM-v9's align_events(). The AM paradigm
    can reconstruct expected onset timing as stimDur+isi; natural_sound_detection
    instead saves `timeTarget`, so we compare the relative target-onset sequence
    directly with the imaging trigger-onset sequence.
    """
    n_imaging = int(eventlocked.shape[1])
    behavior_target_times = np.asarray(behavior_target_times, dtype=float).ravel()
    n_behavior = int(len(behavior_target_times))
    if n_imaging < 1 or n_behavior < 1:
        raise ValueError(f"Cannot align empty streams: imaging={n_imaging}, behavior={n_behavior}")

    valid_events = np.asarray(valid_events, dtype=bool).ravel()
    onset_samples = np.asarray(data2p.event_onset, dtype=float).ravel()
    if len(onset_samples) < n_imaging:
        raise ValueError("data2p.event_onset is shorter than eventlocked imaging-event axis.")
    imaging_time = (onset_samples[:n_imaging] - onset_samples[0]) / float(data2p.srate)

    if not np.all(np.isfinite(behavior_target_times)):
        bad = np.flatnonzero(~np.isfinite(behavior_target_times))
        raise ValueError(f"Non-finite behavior timeTarget values at trials {bad[:20].tolist()}.")
    behavior_time = behavior_target_times - behavior_target_times[0]

    start_i = 0
    start_j = 0
    leading_imaging = np.array([], dtype=int)
    leading_behavior = np.array([], dtype=int)
    start_alignment_mode = "zero_offset"
    start_candidate_records: list[dict[str, Any]] = []

    if n_imaging > 1 and n_behavior > 1:
        first_err = abs((imaging_time[1] - imaging_time[0]) - (behavior_time[1] - behavior_time[0]))
        if first_err > MAX_ABS_ERROR_S:
            candidates: list[tuple[float, float, int, int, int]] = []

            def eval_start(ii: int, jj: int, nskip: int) -> None:
                n_avail = min(LEADING_VALIDATION_INTERVALS, n_imaging - ii - 1, n_behavior - jj - 1)
                if n_avail < 2:
                    return
                obs = np.diff(imaging_time[ii:ii+n_avail+1])
                exp = np.diff(behavior_time[jj:jj+n_avail+1])
                errs = np.abs(obs - exp)
                mae = float(np.mean(errs))
                maxerr = float(np.max(errs))
                passed = bool(maxerr <= MAX_ABS_ERROR_S and mae <= MAX_MEAN_ABS_ERROR_S)
                rec = {
                    "start_imaging_index": int(ii), "start_behavior_index": int(jj),
                    "n_leading_skipped": int(nskip), "validation_mae_s": mae,
                    "validation_max_abs_error_s": maxerr, "passed": passed,
                }
                start_candidate_records.append(rec)
                if passed:
                    candidates.append((mae + ALIGN_SKIP_PENALTY_S*nskip, mae, ii, jj, nskip))

            for k in range(1, MAX_LEADING_SKIP + 1):
                if k < n_imaging:
                    eval_start(k, 0, k)
                if k < n_behavior:
                    eval_start(0, k, k)
            if not candidates:
                raise ValueError(
                    "Natural-sound event alignment failed at the start: zero-offset first "
                    f"interval error={first_err:.4f}s and no leading skip <= {MAX_LEADING_SKIP} passed QC."
                )
            candidates.sort(key=lambda x: (x[0], x[1], x[4]))
            _, _, start_i, start_j, _ = candidates[0]
            start_alignment_mode = "leading_fallback"
            leading_imaging = np.arange(start_i, dtype=int)
            leading_behavior = np.arange(start_j, dtype=int)

    matched_i = [int(start_i)]
    matched_j = [int(start_j)]
    skipped_i: list[int] = []
    skipped_j: list[int] = []
    steps: list[dict[str, Any]] = []
    i, j = int(start_i), int(start_j)

    while i + 1 < n_imaging and j + 1 < n_behavior:
        normal_err = abs((imaging_time[i+1]-imaging_time[i]) - (behavior_time[j+1]-behavior_time[j]))
        if normal_err <= MAX_ABS_ERROR_S:
            ni, nj, si, sj, chosen_err = i+1, j+1, 0, 0, float(normal_err)
        else:
            candidates: list[tuple[float, float, int, int, int, int]] = []
            for k in range(1, MAX_INTERNAL_SKIP_PER_STEP + 1):
                ni, nj = i+1+k, j+1
                if ni < n_imaging:
                    err = abs((imaging_time[ni]-imaging_time[i]) - (behavior_time[nj]-behavior_time[j]))
                    if err <= MAX_ABS_ERROR_S:
                        candidates.append((err + ALIGN_SKIP_PENALTY_S*k, err, ni, nj, k, 0))
                ni, nj = i+1, j+1+k
                if nj < n_behavior:
                    err = abs((imaging_time[ni]-imaging_time[i]) - (behavior_time[nj]-behavior_time[j]))
                    if err <= MAX_ABS_ERROR_S:
                        candidates.append((err + ALIGN_SKIP_PENALTY_S*k, err, ni, nj, 0, k))
            if not candidates:
                raise ValueError(
                    "Natural-sound internal event alignment failed at imaging event "
                    f"{i}, behavior trial {j}; direct interval error={normal_err:.4f}s."
                )
            candidates.sort(key=lambda x: (x[0], x[1], x[4]+x[5]))
            score, raw_err, ni, nj, si, sj = candidates[0]
            if not score < normal_err:
                raise ValueError(
                    "Natural-sound internal alignment ambiguous: "
                    f"direct error={normal_err:.4f}s, best penalized skip score={score:.4f}s."
                )
            chosen_err = float(raw_err)
            if si:
                skipped_i.extend(range(i+1, ni))
            if sj:
                skipped_j.extend(range(j+1, nj))

        matched_i.append(int(ni)); matched_j.append(int(nj))
        steps.append({
            "from_imaging": int(i), "to_imaging": int(ni),
            "from_behavior": int(j), "to_behavior": int(nj),
            "skipped_imaging": int(si), "skipped_behavior": int(sj),
            "timing_error_s": float(chosen_err),
        })
        i, j = int(ni), int(nj)
        if len(skipped_i) + len(skipped_j) > MAX_TOTAL_INTERNAL_SKIPS:
            raise ValueError(
                f"Alignment required {len(skipped_i)+len(skipped_j)} internal skips, "
                f"greater than MAX_TOTAL_INTERNAL_SKIPS={MAX_TOTAL_INTERNAL_SKIPS}."
            )

    matched_i = np.asarray(matched_i, dtype=int)
    matched_j = np.asarray(matched_j, dtype=int)
    trailing_i = np.arange(i+1, n_imaging, dtype=int)
    trailing_j = np.arange(j+1, n_behavior, dtype=int)
    n_matched = len(matched_i)
    coverage = n_matched / float(max(n_imaging, n_behavior))
    if coverage < MIN_ALIGNMENT_COVERAGE:
        raise ValueError(
            f"Alignment retained {n_matched}/{max(n_imaging,n_behavior)} events "
            f"({100*coverage:.1f}%), below required {100*MIN_ALIGNMENT_COVERAGE:.0f}%. "
            "This often indicates the behavior H5 is incomplete relative to the imaging session."
        )

    if n_matched > 1:
        err = np.diff(imaging_time[matched_i]) - np.diff(behavior_time[matched_j])
        mae = float(np.mean(np.abs(err)))
        maxerr = float(np.max(np.abs(err)))
    else:
        mae = maxerr = 0.0
    if mae > MAX_MEAN_ABS_ERROR_S or maxerr > MAX_ABS_ERROR_S:
        raise ValueError(f"Recovered alignment failed QC: MAE={mae:.4f}s, max={maxerr:.4f}s")

    diag = {
        "n_imaging_events": n_imaging,
        "n_behavior_trials": n_behavior,
        "n_matched_trials": int(n_matched),
        "alignment_coverage": float(coverage),
        "matched_imaging_indices": matched_i.tolist(),
        "matched_behavior_indices": matched_j.tolist(),
        "start_alignment_mode": start_alignment_mode,
        "start_imaging_index": int(start_i),
        "start_behavior_index": int(start_j),
        "leading_imaging_indices": leading_imaging.tolist(),
        "leading_behavior_indices": leading_behavior.tolist(),
        "internal_imaging_skipped_indices": [int(x) for x in skipped_i],
        "internal_behavior_skipped_indices": [int(x) for x in skipped_j],
        "trailing_imaging_indices": trailing_i.tolist(),
        "trailing_behavior_indices": trailing_j.tolist(),
        "timing_mae_s": mae,
        "timing_max_abs_error_s": maxerr,
        "start_alignment_candidates": start_candidate_records,
        "alignment_steps_with_skips": [x for x in steps if x["skipped_imaging"] or x["skipped_behavior"]],
    }
    return (
        eventlocked[:, matched_i, :],
        np.asarray(valid_events, dtype=bool).ravel()[matched_i],
        matched_i,
        matched_j,
        diag,
    )


# =============================================================================
# RESPONSE / CONDITION HELPERS
# =============================================================================


def trial_baseline_correct_and_scalar(
    eventlocked_dff: np.ndarray,
    tvec: np.ndarray,
    target_duration: np.ndarray,
    response_start: float,
    response_end: float | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Baseline-correct traces and compute one response scalar per cell x trial.

    If response_end is None, each trial ends at its own targetDuration. This is
    the general default for natural sounds and allows sessions with variable WAV
    durations. Returns the actual response end used for every trial.
    """
    data = np.asarray(eventlocked_dff, dtype=float)
    tvec = np.asarray(tvec, dtype=float)
    target_duration = np.asarray(target_duration, dtype=float).ravel()
    baseline_mask = (tvec >= BASELINE_WINDOW[0]) & (tvec < BASELINE_WINDOW[1])
    if not np.any(baseline_mask):
        raise ValueError("Event-locked time vector does not contain the -1..0 s baseline window.")
    baseline = np.nanmean(data[:, :, baseline_mask], axis=2, keepdims=True)
    bc = data - baseline
    n_cells, n_trials, _ = bc.shape
    response = np.full((n_cells, n_trials), np.nan, dtype=float)
    used_end = np.full(n_trials, np.nan, dtype=float)
    for ti in range(n_trials):
        end = float(response_end) if response_end is not None else float(target_duration[ti])
        if not np.isfinite(end) or end <= response_start:
            continue
        mask = (tvec >= response_start) & (tvec <= end)
        if not np.any(mask):
            continue
        response[:, ti] = np.nanmean(bc[:, ti, :][:, mask], axis=1)
        used_end[ti] = end
    return bc, response, used_end


def choose_condition_dimensions(
    sound_id: np.ndarray,
    sound_location: np.ndarray,
    target_intensity: np.ndarray,
    analysis_trials: np.ndarray,
    location_mode: str,
    intensity_mode: str,
) -> tuple[bool, bool]:
    idx = np.flatnonzero(analysis_trials)
    nloc = len(np.unique(sound_location[idx])) if len(idx) else 0
    nint = len(np.unique(target_intensity[idx])) if len(idx) else 0
    use_location = location_mode == "include" or (location_mode == "auto" and nloc > 1)
    use_intensity = intensity_mode == "include" or (intensity_mode == "auto" and nint > 1)
    return use_location, use_intensity


def build_condition_keys(
    sound_id: np.ndarray,
    sound_location: np.ndarray,
    target_intensity: np.ndarray,
    use_location: bool,
    use_intensity: bool,
) -> list[tuple[Any, ...]]:
    keys: list[tuple[Any, ...]] = []
    for sid, loc, inten in zip(sound_id, sound_location, target_intensity):
        key: list[Any] = [int(sid) if np.issubdtype(np.asarray(sid).dtype, np.number) else sid]
        if use_location:
            key.append(int(loc) if np.issubdtype(np.asarray(loc).dtype, np.number) else loc)
        if use_intensity:
            key.append(float(inten))
        keys.append(tuple(key))
    return keys


def condition_label(
    key: tuple[Any, ...],
    sound_names: list[str],
    use_location: bool,
    use_intensity: bool,
    location_labels: dict[int, str],
) -> str:
    sid = key[0]
    parts = [sound_name_from_id(sid, sound_names)]
    pos = 1
    if use_location:
        loc = int(key[pos]); pos += 1
        parts.append(location_labels.get(loc, f"loc={loc}"))
    if use_intensity:
        parts.append(f"{float(key[pos]):g} dB")
    return " | ".join(parts)


def safe_sample_variance(x: np.ndarray, axis: int = -1) -> np.ndarray:
    return np.nanvar(np.asarray(x, dtype=float), axis=axis, ddof=1)


def per_cell_pooled_within_condition_variance(
    trial_response: np.ndarray,
    analysis_trials: np.ndarray,
    condition_keys: list[tuple[Any, ...]],
) -> tuple[np.ndarray, np.ndarray]:
    """Residual variance after subtracting each cell's mean response per condition."""
    tr = np.asarray(trial_response, dtype=float)
    analysis_trials = np.asarray(analysis_trials, dtype=bool)
    unique_keys = list(dict.fromkeys(condition_keys[i] for i in np.flatnonzero(analysis_trials)))
    ss = np.zeros(tr.shape[0], dtype=float)
    df = np.zeros(tr.shape[0], dtype=int)
    for key in unique_keys:
        mask = analysis_trials & np.array([k == key for k in condition_keys], dtype=bool)
        if np.sum(mask) < 2:
            continue
        x = tr[:, mask]
        n = np.sum(np.isfinite(x), axis=1)
        mu = np.nanmean(x, axis=1, keepdims=True)
        resid = x - mu
        ss += np.nansum(resid**2, axis=1)
        df += np.maximum(n - 1, 0)
    out = np.full(tr.shape[0], np.nan)
    ok = df > 0
    out[ok] = ss[ok] / df[ok]
    return out, df


# =============================================================================
# FIGURES
# =============================================================================


def _short_labels(labels: list[str], maxlen: int = 24) -> list[str]:
    out = []
    for x in labels:
        stem = Path(str(x).split(" | ")[0]).stem
        suffix = " | ".join(str(x).split(" | ")[1:])
        s = stem if not suffix else f"{stem} | {suffix}"
        out.append(s if len(s) <= maxlen else s[:maxlen-1] + "…")
    return out


def plot_repeat_counts(condition_summary: pd.DataFrame, out: Path, title: str) -> None:
    if condition_summary.empty:
        return
    x = np.arange(len(condition_summary))
    fig, ax = plt.subplots(figsize=(max(10, 0.45*len(x)), 5.5))
    ax.bar(x, condition_summary["n_analysis_trials"].to_numpy(float))
    ax.set_xticks(x)
    ax.set_xticklabels(_short_labels(condition_summary["condition_label"].tolist()), rotation=60, ha="right")
    ax.set_ylabel("Matched valid repeats")
    ax.set_title(f"{title}\nRepeat count per natural-sound condition")
    ax.grid(axis="y", alpha=.2)
    fig.tight_layout()
    fig.savefig(out, dpi=250)
    plt.close(fig)


def plot_response_profiles(cell_df: pd.DataFrame, condition_cols: list[str], labels: list[str], outdir: Path, title: str) -> None:
    if not condition_cols:
        return
    x = np.arange(len(condition_cols))
    for responsive_only, tag in ((False, "all_cells"), (True, "natural_responsive_cells")):
        use = cell_df.copy()
        if responsive_only:
            use = use[use["natural_responsive_fdr"].astype(bool)]
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
        for ax, cls, color in zip(axes, ("green", "yellow"), (GREEN_COLOR, YELLOW_COLOR)):
            sub = use[use.cell_class == cls]
            mat = sub[condition_cols].to_numpy(float) if len(sub) else np.empty((0, len(condition_cols)))
            if len(mat):
                for row in mat:
                    ax.plot(x, row, color=color, alpha=.07, lw=.6)
                mu = np.nanmean(mat, axis=0)
                se = stats.sem(mat, axis=0, nan_policy="omit") if len(mat) > 1 else np.full(len(x), np.nan)
                ax.plot(x, mu, color=color, marker="o", lw=2)
                ax.fill_between(x, mu-se, mu+se, color=color, alpha=.18)
            ax.axhline(0, color="0.4", ls="--", lw=.9)
            ax.set_title(f"{cls.upper()} (n={len(sub)})")
            ax.set_xticks(x)
            ax.set_xticklabels(_short_labels(labels), rotation=60, ha="right", fontsize=7)
            ax.set_xlabel("Natural-sound condition")
        axes[0].set_ylabel("Mean baseline-corrected dF/F")
        fig.suptitle(f"{title}\nNatural-sound response profiles — {tag.replace('_',' ')}")
        fig.tight_layout(rect=[0,0,1,.94])
        fig.savefig(outdir / f"response_profiles_{tag}.png", dpi=250)
        plt.close(fig)


def _plot_distribution_pair(values_by_class: dict[str, np.ndarray], xlabel: str, title: str, out: Path, log_x: bool=False) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    allvals = []
    for cls in ("green", "yellow"):
        v = np.asarray(values_by_class.get(cls, []), dtype=float)
        v = v[np.isfinite(v)]
        if log_x:
            v = v[v > 0]
        if len(v):
            allvals.append(v)
    if not allvals:
        plt.close(fig); return
    pooled = np.concatenate(allvals)
    if log_x:
        lo, hi = np.nanpercentile(pooled, [1,99])
        lo = max(lo, np.nanmin(pooled[pooled>0]))
        bins = np.geomspace(lo, max(hi, lo*1.01), 35)
    else:
        lo, hi = np.nanpercentile(pooled, [0.5,99.5])
        bins = np.linspace(lo, hi if hi>lo else lo+1, 35)
    for cls, color in (("green", GREEN_COLOR), ("yellow", YELLOW_COLOR)):
        v = np.asarray(values_by_class.get(cls, []), dtype=float)
        v = v[np.isfinite(v)]
        if log_x:
            v = v[v>0]
        if not len(v):
            continue
        axes[0].hist(v, bins=bins, density=True, histtype="step", lw=2, color=color, label=f"{cls} n={len(v)}")
        s = np.sort(v)
        axes[1].plot(s, np.arange(1,len(s)+1)/len(s), color=color, lw=2, label=f"{cls} n={len(v)}")
    if log_x:
        axes[0].set_xscale("log"); axes[1].set_xscale("log")
    axes[0].set_xlabel(xlabel); axes[0].set_ylabel("Density")
    axes[1].set_xlabel(xlabel); axes[1].set_ylabel("Empirical CDF")
    for ax in axes:
        ax.legend(frameon=False); ax.grid(alpha=.2)
    fig.suptitle(title)
    fig.tight_layout(rect=[0,0,1,.93])
    fig.savefig(out, dpi=250)
    plt.close(fig)


def plot_variance_distributions(condition_df: pd.DataFrame, cell_df: pd.DataFrame, outdir: Path, title: str) -> None:
    # condition-level variances: only cells that are responsive to at least one natural sound
    cond = condition_df[condition_df["cell_natural_responsive_fdr"].astype(bool)].copy()
    vals = {cls: cond.loc[cond.cell_class==cls, "trial_response_variance"].to_numpy(float) for cls in ("green","yellow")}
    _plot_distribution_pair(vals, "Within-sound repeat variance (dF/F)^2",
                            f"{title}\nCell x sound repeat variance; natural-responsive cells",
                            outdir/"repeat_variance_distribution_linear.png", False)
    _plot_distribution_pair(vals, "Within-sound repeat variance (dF/F)^2",
                            f"{title}\nCell x sound repeat variance; natural-responsive cells",
                            outdir/"repeat_variance_distribution_logx.png", True)

    pooled = {cls: cell_df.loc[(cell_df.cell_class==cls)&cell_df.natural_responsive_fdr.astype(bool),
                               "pooled_within_condition_noise_variance"].to_numpy(float)
              for cls in ("green","yellow")}
    _plot_distribution_pair(pooled, "Pooled within-condition noise variance (dF/F)^2",
                            f"{title}\nPer-cell repeat-to-repeat noise variance",
                            outdir/"pooled_within_condition_variance_linear.png", False)
    _plot_distribution_pair(pooled, "Pooled within-condition noise variance (dF/F)^2",
                            f"{title}\nPer-cell repeat-to-repeat noise variance",
                            outdir/"pooled_within_condition_variance_logx.png", True)


# =============================================================================
# SESSION ANALYSIS
# =============================================================================


def load_natural_twophoton(subject: str, date: str, session: str, plane: int):
    behavior_path = Path(loadbehavior.path_to_behavior_data(subject, PARADIGM, f"{date}_{session}"))
    if not behavior_path.exists():
        raise FileNotFoundError(f"Behavior file not found: {behavior_path}")
    data2p = twophotonanalysis.TwoPhoton(subject, date, session, plane, paradigm=PARADIGM)
    return data2p, behavior_path


def analyze_session(meta: dict[str, Any], args: argparse.Namespace, outdir: Path) -> dict[str, Any]:
    subject, date, session = str(meta["subject"]), str(meta["date"]), str(meta["session"])
    outdir.mkdir(parents=True, exist_ok=True)
    print("\n" + "="*80)
    print(f"NATURAL SOUNDS: {subject} {date} {session} | {meta.get('brainArea')} | depth={meta.get('depth')}")
    print("="*80)

    data2p, behavior_path = load_natural_twophoton(subject, date, session, args.plane)
    h5meta = load_sound_metadata_from_h5(behavior_path)
    sound_names = h5meta.get("sound_names", [])
    enum_labels = h5meta.get("enum_labels", {})

    # Behavior arrays are read before event locking so the time window can cover
    # the longest sound in this session.
    sound_key = infer_sound_key(data2p.bdata)
    sound_id = get_behavior_array(data2p.bdata, sound_key)
    n_behavior = len(sound_id)
    target_duration = get_behavior_array(data2p.bdata, "targetDuration", n_behavior, np.nan, float)
    behavior_time_target = get_behavior_array(data2p.bdata, "timeTarget", n_behavior, np.nan, float)
    sound_location = get_behavior_array(data2p.bdata, "soundLocation", n_behavior, 0)
    target_intensity = get_behavior_array(data2p.bdata, "targetIntensity", n_behavior, np.nan, float)
    laser_trial = get_behavior_array(data2p.bdata, "laserTrial", n_behavior, 0).astype(bool)
    valid_behavior = get_behavior_array(data2p.bdata, "valid", n_behavior, 1).astype(bool)

    lengths = {
        sound_key: len(sound_id), "targetDuration": len(target_duration), "timeTarget": len(behavior_time_target),
        "soundLocation": len(sound_location), "targetIntensity": len(target_intensity),
        "laserTrial": len(laser_trial), "valid": len(valid_behavior),
    }
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Behavior arrays have inconsistent lengths: {lengths}")
    finite_dur = target_duration[np.isfinite(target_duration) & (target_duration > 0)]
    max_duration = float(np.max(finite_dur)) if len(finite_dur) else 1.0
    time_range = [BASELINE_WINDOW[0], max_duration + POST_STIM_PADDING_S]

    suite2p_dir = Path(data2p.data_path).expanduser().resolve()
    required = [suite2p_dir/x for x in ("ops.npy","iscell.npy","stat.npy")]
    missing = [str(x) for x in required if not x.exists()]
    if missing:
        raise FileNotFoundError("Missing Suite2p files:\n" + "\n".join(missing))

    iscell = np.asarray(data2p.iscell)
    cell_mask = (iscell[:,0] == 1) & (iscell[:,1] > CELL_PROB_THRESHOLD)
    cell_roi_indices = np.flatnonzero(cell_mask)
    eventlocked_all, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
    eventlocked_raw_all, tvec_raw, valid_events_raw = data2p.event_locked_average(time_range=time_range, dff=False)
    if len(tvec_raw) != len(tvec) or not np.allclose(tvec_raw, tvec, equal_nan=True):
        raise ValueError("dff=True and dff=False time vectors differ.")
    eventlocked = np.asarray(eventlocked_all[cell_mask], dtype=float)
    eventlocked_raw = np.asarray(eventlocked_raw_all[cell_mask], dtype=float)
    valid_events = np.asarray(valid_events, dtype=bool).ravel()
    n_cells = eventlocked.shape[0]
    print(f"Functional analysis cells: {n_cells}/{eventlocked_all.shape[0]}")
    print(f"Behavior trials in H5: {n_behavior}; imaging sound events: {eventlocked.shape[1]}")
    print(f"Natural sounds listed: {len(sound_names)}; longest targetDuration={max_duration:g}s")

    # Cellpose GREEN/YELLOW classification: exactly the current AM-v9 convention.
    ops = np.load(suite2p_dir/"ops.npy", allow_pickle=True).item()
    stat_all = np.load(suite2p_dir/"stat.npy", allow_pickle=True)
    functional_stats = stat_all[np.asarray(cell_roi_indices, dtype=int)]
    if "meanImg_chan2" in ops and ops["meanImg_chan2"] is not None:
        red_image = np.asarray(ops["meanImg_chan2"], dtype=float); red_image_name = "meanImg_chan2"
    elif "meanImg_chan2_corrected" in ops and ops["meanImg_chan2_corrected"] is not None:
        red_image = np.asarray(ops["meanImg_chan2_corrected"], dtype=float); red_image_name = "meanImg_chan2_corrected"
    else:
        raise KeyError("No channel-2 mean image found in ops.npy.")
    equiv = np.asarray([2*np.sqrt(len(s["ypix"])/np.pi) for s in functional_stats if len(s["ypix"])>0], float)
    if not len(equiv):
        raise ValueError("Could not estimate Cellpose diameter.")
    diameter = float(np.nanmedian(equiv)) if CELLPOSE_DIAMETER is None else float(CELLPOSE_DIAMETER)
    cp_settings = {"params":None,"chan2_params":None,"cellprob_threshold":CELLPOSE_CELLPROB_THRESHOLD,
                   "flow_threshold":CELLPOSE_FLOW_THRESHOLD}
    redstats, red_masks = cellpose_overlap(
        functional_stats, red_image, diameter=diameter, chan2_threshold=IOU_THRESHOLD,
        device=torch.device("cpu"), settings=cp_settings,
    )
    red_iou = np.asarray(redstats[:,1], dtype=float)
    yellow_mask = red_iou > IOU_THRESHOLD
    green_mask = ~yellow_mask
    cell_class = np.where(yellow_mask, "yellow", "green")
    print(f"GREEN={np.sum(green_mask)}, YELLOW={np.sum(yellow_mask)}, anatomical RED={int(np.max(red_masks))}")

    title = f"{subject} {date} {session} p{args.plane} | natural sounds"
    amv9.save_classification_overlay(
        red_image, red_image_name, functional_stats, np.asarray(red_masks), green_mask, yellow_mask,
        outdir/"classification_overlay_chan2.png", title,
    )
    if "meanImg" in ops and ops["meanImg"] is not None and np.asarray(ops["meanImg"]).shape == red_image.shape:
        amv9.save_classification_overlay(
            np.asarray(ops["meanImg"],float), "meanImg (chan1)", functional_stats, np.asarray(red_masks),
            green_mask, yellow_mask, outdir/"classification_overlay_chan1.png", title,
        )
    np.savez(outdir/"green_yellow_classification.npz",
             cell_roi_indices=cell_roi_indices, green_only_mask=green_mask, yellow_cell_mask=yellow_mask,
             cellpose_red_iou=red_iou, iou_threshold=IOU_THRESHOLD,
             cellpose_cellprob_threshold=CELLPOSE_CELLPROB_THRESHOLD,
             cellpose_flow_threshold=CELLPOSE_FLOW_THRESHOLD, cellpose_diameter=diameter)

    # Align imaging triggers to actual behavior target-onset timestamps.
    eventlocked_aligned, valid_aligned, imaging_idx, behavior_idx, align_diag = align_events_to_behavior_times(
        data2p, eventlocked, valid_events, behavior_time_target
    )
    eventlocked_raw_aligned = np.asarray(eventlocked_raw[:, imaging_idx, :], dtype=float)
    event_onset_all = np.asarray(data2p.event_onset, dtype=float).ravel()
    event_onset_aligned = event_onset_all[imaging_idx]
    for name, arr in [
        ("sound_id", sound_id), ("target_duration", target_duration), ("sound_location", sound_location),
        ("target_intensity", target_intensity), ("laser_trial", laser_trial), ("valid_behavior", valid_behavior),
        ("behavior_time_target", behavior_time_target),
    ]:
        if len(arr) < np.max(behavior_idx)+1:
            raise ValueError(f"{name} is too short for aligned behavior indices.")
    sound_id = sound_id[behavior_idx]
    target_duration = target_duration[behavior_idx]
    sound_location = sound_location[behavior_idx]
    target_intensity = target_intensity[behavior_idx]
    laser_trial = laser_trial[behavior_idx]
    valid_behavior = valid_behavior[behavior_idx]
    behavior_time_target = behavior_time_target[behavior_idx]

    with (outdir/"alignment_diagnostics.json").open("w") as f:
        json.dump(amv9.jsonable(align_diag), f, indent=2)
    print(f"Alignment matched {len(imaging_idx)} trials; MAE={align_diag['timing_mae_s']:.4f}s; "
          f"coverage={100*align_diag['alignment_coverage']:.1f}%")

    analysis_trials = np.asarray(valid_aligned & valid_behavior, dtype=bool)
    if not args.include_laser:
        analysis_trials &= ~laser_trial
    if not np.any(analysis_trials):
        raise ValueError("No valid analysis trials remain after alignment/QC/laser filtering.")

    # Primary and alternate dF/F trial-response matrices.
    bc_primary, trial_response, response_end_used = trial_baseline_correct_and_scalar(
        eventlocked_aligned, tvec, target_duration, args.response_start, args.response_end
    )
    full_session_raw = np.asarray(data2p.roiF[cell_mask, :], dtype=float)
    session_median_dff = amv9._session_median_dff(eventlocked_raw_aligned, full_session_raw)
    local_prestim_dff = amv9._local_prestim_median_dff(
        eventlocked_raw_aligned, event_onset_aligned, float(data2p.srate), np.asarray(valid_aligned,bool),
        np.asarray(tvec,float), local_window_s=60.0, prestim_window_s=(-0.300,0.0),
    )
    _, trial_response_session_median, _ = trial_baseline_correct_and_scalar(
        session_median_dff, tvec, target_duration, args.response_start, args.response_end
    )
    _, trial_response_local60, _ = trial_baseline_correct_and_scalar(
        local_prestim_dff, tvec, target_duration, args.response_start, args.response_end
    )

    amv9._save_eventlocked_average_figure(eventlocked_aligned, valid_aligned, tvec,
        outdir/"all_stimuli_eventlocked_avg_CURRENT_DFF.png", f"Current jaratoolbox dff=True\n{title}")
    amv9._save_eventlocked_average_figure(session_median_dff, valid_aligned, tvec,
        outdir/"all_stimuli_eventlocked_avg_SESSION_MEDIAN_DFF.png", f"Whole-session median F0 dF/F\n{title}")
    amv9._save_eventlocked_average_figure(local_prestim_dff, valid_aligned, tvec,
        outdir/"all_stimuli_eventlocked_avg_60s_PRESTIM_MEDIAN_DFF.png", f"60-s local prestimulus median F0 dF/F\n{title}")

    use_location, use_intensity = choose_condition_dimensions(
        sound_id, sound_location, target_intensity, analysis_trials, args.location_mode, args.intensity_mode
    )
    keys = build_condition_keys(sound_id, sound_location, target_intensity, use_location, use_intensity)
    unique_keys = list(dict.fromkeys(keys[i] for i in np.flatnonzero(analysis_trials)))
    unique_keys.sort(key=lambda x: tuple(str(v) for v in x))
    loc_labels = h5meta.get("enum_labels", {}).get("soundLocation", {})
    labels = [condition_label(k, sound_names, use_location, use_intensity, loc_labels) for k in unique_keys]
    print(f"Condition definition: soundID + location={use_location} + intensity={use_intensity}")
    print(f"Unique analysis conditions: {len(unique_keys)}")

    rng = np.random.default_rng(args.seed + sum(ord(c) for c in f"{subject}{date}{session}"))
    n_cond = len(unique_keys)
    condition_means = np.full((n_cells,n_cond), np.nan)
    condition_vars = np.full((n_cells,n_cond), np.nan)
    condition_sds = np.full((n_cells,n_cond), np.nan)
    condition_p = np.full((n_cells,n_cond), np.nan)
    condition_q = np.full((n_cells,n_cond), np.nan)
    condition_n = np.zeros(n_cond, dtype=int)
    condition_masks: list[np.ndarray] = []

    for ci, key in enumerate(unique_keys):
        mask = analysis_trials & np.array([x == key for x in keys], dtype=bool)
        condition_masks.append(mask)
        condition_n[ci] = int(np.sum(mask))
        x = trial_response[:,mask]
        condition_means[:,ci] = np.nanmean(x,axis=1) if np.any(mask) else np.nan
        if np.sum(mask) >= args.min_repeats_for_variance:
            condition_vars[:,ci] = np.nanvar(x,axis=1,ddof=1)
            condition_sds[:,ci] = np.sqrt(condition_vars[:,ci])
        if np.sum(mask) >= args.min_repeats_for_test:
            pvals = amv9.signflip_pvalues_grouped(x, args.n_permutations, rng)
            condition_p[:,ci] = pvals
            condition_q[:,ci] = amv9.bh_fdr(pvals)

    condition_resp = condition_q < FDR_ALPHA
    natural_resp = np.any(condition_resp, axis=1)
    condition_exc = condition_resp & (condition_means > 0)
    condition_sup = condition_resp & (condition_means < 0)
    natural_exc = np.any(condition_exc,axis=1)
    natural_sup = np.any(condition_sup,axis=1)

    pooled_noise_var, pooled_noise_df = per_cell_pooled_within_condition_variance(
        trial_response, analysis_trials, keys
    )
    median_cond_var = np.nanmedian(condition_vars, axis=1)
    mean_cond_var = np.nanmean(condition_vars, axis=1)
    profile_mag = np.abs(condition_means)
    lifetime = np.array([amv9.lifetime_sparseness_nonnegative(row[np.isfinite(row)]) for row in profile_mag])
    gini = np.array([amv9.gini_coefficient_nonnegative(row[np.isfinite(row)]) for row in profile_mag])
    fano = np.array([amv9.fano_factor_nonnegative(row[np.isfinite(row)]) for row in profile_mag])

    # Legacy redcell score is metadata only, matching AM-v9.
    legacy_scores = np.full(n_cells, np.nan)
    redcell_path = suite2p_dir/"redcell.npy"
    if redcell_path.exists():
        legacy = np.asarray(np.load(redcell_path,allow_pickle=True))
        if legacy.ndim==2 and legacy.shape[1]>=2 and np.max(cell_roi_indices,initial=-1)<legacy.shape[0]:
            legacy_scores = legacy[cell_roi_indices,1].astype(float)

    cell_rows = []
    for cell in range(n_cells):
        row: dict[str,Any] = {
            "subject":subject,"date":date,"session":session,"session_key":f"{date}_{session}",
            "brainArea":meta.get("brainArea"),"canonicalArea":meta.get("canonicalArea"),"depth":meta.get("depth"),
            "analysis_cell_index":cell,"suite2p_roi_index":int(cell_roi_indices[cell]),"cell_class":cell_class[cell],
            "cellpose_red_iou":float(red_iou[cell]),"legacy_redcell_score":float(legacy_scores[cell]) if np.isfinite(legacy_scores[cell]) else np.nan,
            "natural_responsive_fdr":bool(natural_resp[cell]),"natural_excited_fdr":bool(natural_exc[cell]),
            "natural_suppressed_fdr":bool(natural_sup[cell]),"n_responsive_conditions":int(np.sum(condition_resp[cell])),
            "natural_lifetime_sparseness":float(lifetime[cell]) if np.isfinite(lifetime[cell]) else np.nan,
            "natural_gini_coefficient":float(gini[cell]) if np.isfinite(gini[cell]) else np.nan,
            "natural_profile_fano_factor":float(fano[cell]) if np.isfinite(fano[cell]) else np.nan,
            "mean_within_condition_variance":float(mean_cond_var[cell]) if np.isfinite(mean_cond_var[cell]) else np.nan,
            "median_within_condition_variance":float(median_cond_var[cell]) if np.isfinite(median_cond_var[cell]) else np.nan,
            "pooled_within_condition_noise_variance":float(pooled_noise_var[cell]) if np.isfinite(pooled_noise_var[cell]) else np.nan,
            "pooled_within_condition_noise_df":int(pooled_noise_df[cell]),
        }
        for ci, label in enumerate(labels):
            col = f"condition_{ci:03d}_mean_response"
            row[col] = condition_means[cell,ci]
        cell_rows.append(row)
    cell_df = pd.DataFrame(cell_rows)
    cell_df.to_csv(outdir/"cell_results.csv",index=False)
    condition_cols = [f"condition_{i:03d}_mean_response" for i in range(n_cond)]

    cond_rows = []
    for ci,(key,label) in enumerate(zip(unique_keys,labels)):
        sid = key[0]
        for cell in range(n_cells):
            mu = condition_means[cell,ci]
            sd = condition_sds[cell,ci]
            cv = sd/abs(mu) if np.isfinite(sd) and np.isfinite(mu) and abs(mu)>1e-12 else np.nan
            cond_rows.append({
                "subject":subject,"date":date,"session":session,"session_key":f"{date}_{session}",
                "brainArea":meta.get("brainArea"),"canonicalArea":meta.get("canonicalArea"),"depth":meta.get("depth"),
                "analysis_cell_index":cell,"suite2p_roi_index":int(cell_roi_indices[cell]),"cell_class":cell_class[cell],
                "cell_natural_responsive_fdr":bool(natural_resp[cell]),
                "condition_index":ci,"condition_label":label,"sound_id":sid,
                "sound_name":sound_name_from_id(sid,sound_names),
                "n_repeats":int(condition_n[ci]),"mean_response":mu,"trial_response_variance":condition_vars[cell,ci],
                "trial_response_sd":sd,"trial_response_cv_absmean":cv,
                "response_p_signflip":condition_p[cell,ci],"response_q_bh":condition_q[cell,ci],
                "condition_responsive_fdr":bool(condition_resp[cell,ci]),
                "condition_excited_fdr":bool(condition_exc[cell,ci]),"condition_suppressed_fdr":bool(condition_sup[cell,ci]),
            })
    condition_df = pd.DataFrame(cond_rows)
    condition_df.to_csv(outdir/"condition_results.csv",index=False)

    summary_rows=[]
    for ci,(key,label,mask) in enumerate(zip(unique_keys,labels,condition_masks)):
        sid=key[0]
        summary_rows.append({
            "condition_index":ci,"condition_label":label,"sound_id":sid,"sound_name":sound_name_from_id(sid,sound_names),
            "n_analysis_trials":int(np.sum(mask)),"n_green_responsive":int(np.sum(condition_resp[green_mask,ci])),
            "n_yellow_responsive":int(np.sum(condition_resp[yellow_mask,ci])),
            "pct_green_responsive":100*float(np.mean(condition_resp[green_mask,ci])) if np.any(green_mask) else np.nan,
            "pct_yellow_responsive":100*float(np.mean(condition_resp[yellow_mask,ci])) if np.any(yellow_mask) else np.nan,
        })
    condition_summary = pd.DataFrame(summary_rows)
    condition_summary.to_csv(outdir/"condition_summary.csv",index=False)

    # Trial archive: preserve the exact unit needed for repeat-number resampling.
    np.savez_compressed(
        outdir/"natural_sound_trial_responses.npz",
        schema=np.asarray("natural_sound_response_v1"), subject=np.asarray(subject), date=np.asarray(date), session=np.asarray(session),
        canonical_area=np.asarray(str(meta.get("canonicalArea"))), brain_area=np.asarray(str(meta.get("brainArea"))),
        depth=np.asarray(float(meta.get("depth")) if meta.get("depth") is not None else np.nan),
        analysis_cell_index=np.arange(n_cells,dtype=int), suite2p_roi_index=cell_roi_indices.astype(int),
        cell_class=np.asarray(cell_class,dtype="U16"), cell_natural_responsive_fdr=natural_resp.astype(bool),
        trial_response_primary=trial_response.astype(np.float32),
        trial_response_session_median=trial_response_session_median.astype(np.float32),
        trial_response_local_60s_prestim=trial_response_local60.astype(np.float32),
        analysis_trials=analysis_trials.astype(bool), valid_aligned=np.asarray(valid_aligned,bool),
        sound_id=np.asarray(sound_id), sound_location=np.asarray(sound_location), target_intensity=np.asarray(target_intensity,float),
        target_duration=np.asarray(target_duration,float), response_end_used=np.asarray(response_end_used,float),
        condition_index_per_trial=np.asarray([
            unique_keys.index(keys[i]) if analysis_trials[i] else -1 for i in range(len(keys))
        ],dtype=int),
        condition_labels=np.asarray(labels,dtype="U256"), condition_repeat_counts=condition_n.astype(int),
        sound_names=np.asarray(sound_names,dtype="U256"),
        imaging_trial_indices=imaging_idx.astype(int), behavior_trial_indices=behavior_idx.astype(int),
        tvec=np.asarray(tvec,float),
    )

    plot_repeat_counts(condition_summary,outdir/"repeat_count_by_condition.png",title)
    plot_response_profiles(cell_df,condition_cols,labels,outdir,title)
    plot_variance_distributions(condition_df,cell_df,outdir,title)

    # Compact class summary.
    class_summary=[]
    for cls in ("green","yellow"):
        sub=cell_df[cell_df.cell_class==cls]
        class_summary.append({
            "cell_class":cls,"n_cells":len(sub),"n_natural_responsive":int(sub.natural_responsive_fdr.sum()),
            "pct_natural_responsive":100*float(sub.natural_responsive_fdr.mean()) if len(sub) else np.nan,
            "median_pooled_noise_variance":float(np.nanmedian(sub.pooled_within_condition_noise_variance)) if len(sub) else np.nan,
            "median_within_condition_variance":float(np.nanmedian(sub.median_within_condition_variance)) if len(sub) else np.nan,
        })
    pd.DataFrame(class_summary).to_csv(outdir/"class_summary.csv",index=False)

    summary = {
        "subject":subject,"date":date,"session":session,"brainArea":meta.get("brainArea"),
        "canonicalArea":meta.get("canonicalArea"),"depth":meta.get("depth"),"plane":args.plane,
        "behavior_path":str(behavior_path),"suite2p_dir":str(suite2p_dir),"sound_key":sound_key,
        "n_behavior_trials":int(n_behavior),"n_imaging_events":int(eventlocked.shape[1]),"n_matched_trials":int(len(imaging_idx)),
        "n_analysis_trials":int(np.sum(analysis_trials)),"n_cells":int(n_cells),"n_green":int(np.sum(green_mask)),
        "n_yellow":int(np.sum(yellow_mask)),"n_conditions":int(n_cond),"sound_names":sound_names,
        "condition_labels":labels,"condition_repeat_counts":condition_n.tolist(),
        "condition_uses_location":bool(use_location),"condition_uses_intensity":bool(use_intensity),
        "response_start_s":float(args.response_start),"response_end_fixed_s":args.response_end,
        "response_end_default":"per-trial targetDuration" if args.response_end is None else "fixed",
        "fdr_alpha":FDR_ALPHA,"n_permutations":args.n_permutations,"seed":args.seed,
        "primary_responsiveness":"condition-specific sign-flip; BH-FDR across cells within condition; union across conditions",
        "repeat_variance":"sample variance across repeated presentations of the same condition",
        "pooled_noise_variance":"residual variance after subtracting each condition mean within cell",
        "alignment":align_diag,
        "am_v9_dependency":str(getattr(amv9,"__file__","am_tuning_area_analysis_v9")),
    }
    with (outdir/"session_summary.json").open("w") as f:
        json.dump(amv9.jsonable(summary),f,indent=2)
    return summary


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    args=parse_args()
    info_file,sessions=load_info2p_sessions(args.subject)
    selected=select_sessions(sessions,args)
    root=Path(settings.TEMP_OUTPUT_PATH)/"evan"/"natural_sound_response_analysis"/args.subject
    root.mkdir(parents=True,exist_ok=True)

    selection_rows=[]
    for s in selected:
        selection_rows.append({k:s.get(k) for k in ("subject","date","session","brainArea","canonicalArea","depth","sessionLabel","paradigm","nFrames")})
    pd.DataFrame(selection_rows).to_csv(root/f"session_selection_{'_'.join(args.dates)}.csv",index=False)

    print("="*80)
    print("NATURAL-SOUND RESPONSE / REPEAT-VARIABILITY ANALYSIS v1")
    print("="*80)
    print(f"Subject: {args.subject}")
    print(f"Dates: {', '.join(args.dates)}")
    print(f"Info2p: {info_file}")
    print(f"Selected sessions: {len(selected)}")
    for s in selected:
        print(f"  {s.get('date')} {s.get('session')} {s.get('brainArea')} depth={s.get('depth')} label={s.get('sessionLabel')}")
    if args.dry_run:
        return
    if not selected:
        raise RuntimeError("No natural_sound_detection sessions matched the requested filters.")

    successes=[]; failures=[]
    for meta in selected:
        outdir=root/str(meta["date"])/str(meta["session"])
        try:
            successes.append(analyze_session(meta,args,outdir))
            err=outdir/"ERROR.json"
            if err.exists(): err.unlink()
        except Exception as exc:
            outdir.mkdir(parents=True,exist_ok=True)
            rec={"subject":args.subject,"date":str(meta.get("date")),"session":str(meta.get("session")),
                 "error_type":type(exc).__name__,"error":str(exc),"traceback":traceback.format_exc()}
            with (outdir/"ERROR.json").open("w") as f: json.dump(rec,f,indent=2)
            failures.append(rec)
            print(f"ERROR {meta.get('date')} {meta.get('session')}: {type(exc).__name__}: {exc}")

    manifest={
        "subject":args.subject,"dates":args.dates,"sessions_filter":args.sessions,"areas_filter":args.areas,
        "info2p_file":str(info_file),"output_root":str(root),"n_selected":len(selected),
        "n_success":len(successes),"n_failed":len(failures),"failures":failures,
        "parameters":vars(args),
    }
    with (root/f"run_manifest_{'_'.join(args.dates)}.json").open("w") as f:
        json.dump(amv9.jsonable(manifest),f,indent=2)
    print(f"\nCompleted: {len(successes)} session(s); failed: {len(failures)}")
    print(f"Output root: {root}")


if __name__ == "__main__":
    main()
