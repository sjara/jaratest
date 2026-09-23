# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Evan Vickers' two-photon auditory cortex analysis scripts, a subdirectory of the Jaramillo-lab `jaratest` repo (the git root is `..`). There is no package, build, linter, or test suite. Each `.py` file is a standalone argparse CLI script run from the lab Python environment, where `jaratoolbox`, `suite2p` (Cellpose), and `torch` are already set up. There is no `requirements.txt`.

`README.md` is the authoritative user guide: it has the current-script table, full CLI examples, output layouts, and analysis conventions. Read it before changing a workflow. When you add a new script version, update the README's "Recommended current scripts" table and its "Versioning" section.

## Running and checking

```bash
# Every batch script supports --dry-run (session discovery only; no imaging data is loaded)
python sound_tuning_area_analysis_v13.py imag039 --area A1 --dates 20260729 20260730 --dry-run

# The only automated check used here is syntax compilation (the change notes say so)
python -m py_compile <script>.py
```

Real runs need the lab data mounts (`settings.INFO2P_PATH`, `settings.TWOPHOTON_PATH`, behavior files), and they are slow: response tests default to 20000 permutations (4096 for multistim). When validating a change, prefer `--dry-run`, `--n-permutations`, or `--skip-trial-reduction`, or smoke-test the helper functions on synthetic data. That is how earlier changes were validated.

## Versioning model (important)

- Scripts are **copied to a new `_vN` file** rather than edited in place. Old versions are kept so past results can be reproduced. Don't modify an old version unless you're asked to; make changes in the current version, or in a new version if the user wants one. The current versions are listed in `README.md`.
- Each version is **self-contained**. Helpers (info2p loading, Cellpose GREEN/YELLOW classification, FDR, dF/F, plotting) are duplicated across scripts instead of shared. A fix in one script usually needs to be applied by hand to its siblings. The one exception: `natural_sound_response_analysis_v2.py` imports `am_tuning_area_analysis_v9.py` as a module, on purpose, so that the classification, alignment, FDR, and dF/F conventions stay in sync. Renaming or breaking v9 breaks it.
- Output directories are **not versioned** (for example `<TEMP_OUTPUT_PATH>/evan/sound_tuning_multistim_fov_analysis/<subject>/<area>/<date_tag>/`). Running a different version overwrites the previous outputs in the same place. Trial-archive filenames and the `schema_version` field (for example `multistim_v2`, `_trial_response_archive_v13.npz`) are what downstream scripts check for compatibility.
- `*_changes.txt` / `CHANGES_v*.txt` files record what changed per version. Newer drafts sometimes arrive as downloaded zip folders, such as `sound_tuning_NEW_analysis_2026*/` (the original multistim v3 drop) and `sound_chunks_examples_*/` (stimulus-generation scripts and WAV examples). Before using a script from one of these folders, copy it to the top level and add it to the README.

## Current multistim pipeline (v3 / v4 / v4)

1. `sound_tuning_multistim_fov_analysis_v3.py`: run once per area. This is a byte-for-byte copy of the downloaded v3.
2. `sound_tuning_multistim_area_layer_green_yellow_analysis_v4.py`
3. `sound_tuning_multistim_cross_area_cellclass_analysis_v4.py`

The stage 2 and 3 v4 scripts are the v3 scripts plus the v2b fixes. The downloaded v3 downstream scripts were built from v2 and had lost them. The fixes are:
- The `block_data_cells()` filter. Cells from FOVs that never recorded a sound block have all-NaN columns for it, and the filter excludes them from that block's `all_cells` plots, rasters, statistics and responsive-cell subsets.
- The cross-area pandas fragmentation fix (`allc.copy()` / `allc.assign(...)`).

Don't use the downloaded v3 stage 2/3 scripts or the v2/v2b multistim scripts for new analyses. When making a v5, start from v4 and keep `block_data_cells`, including in any new `all_cells` branch.

## Architecture: three-stage pipelines

Every workflow (`sound_tuning`, `am_tuning`, multistim `sound_tuning`, natural sound) follows the same pattern:

1. **Per-area / per-session stage** (`*_area_analysis_vN`, `*_multistim_fov_analysis_vN`, `natural_sound_response_analysis_vN`): loads `settings.INFO2P_PATH/<subject>_info2p.py` dynamically via `importlib` and filters its `sessions` list by paradigm, area, and date. It then loads Suite2p output and behavior, checks imaging/behavior event alignment, classifies ROIs as GREEN/YELLOW with `suite2p.detection.chan2detect.cellpose_overlap` against `meanImg_chan2`, and computes responses and FDR responsiveness. It writes per-session outputs, `combined/` CSVs, `run_manifest.json`, and `.npz` trial-response archives under `settings.TEMP_OUTPUT_PATH/evan/<script_family>/...`.
2. **GREEN vs YELLOW within area × layer** (`*_area_layer_green_yellow_analysis_vN`): reads the stage-1 CSVs from those hard-coded TEMP_OUTPUT_PATH locations. It does not recompute anything from raw data.
3. **Cross-area** (`*_cross_area_cellclass_analysis_vN`): compares A1/AAF/A2 within each cell class. For significant YELLOW results, it reloads the stage-1 trial archives (paths are stored in the CSVs, for example `trial_response_archive_path`) and runs trial-reduction robustness at 100/75/50/25% of trials.

The stage 2 and 3 scripts depend on the exact stage-1 output paths, column names, and archive schema. If you change any of these in stage 1, update the downstream scripts (and bump versions consistently). After a stage-1 schema change, stage 1 must be rerun before stages 2 and 3.

`twophoton_sound_tuning_cli.py` and `twophoton_green_red_colocalization_cli.py` are older single-session tools. They default to writing in `/tmp` and use a different red-cell classification (`redcell.npy`/GMM/percentile), not the Cellpose-overlap GREEN/YELLOW classification.

## Analysis conventions to preserve

(Full details are in the README.)
- Canonical area: `brainArea` containing `A1` → A1; `AAF` → AAF; `A2` or `AuV` → A2.
- Layers: L2/3 = 100 ≤ depth < 300 µm; L4/5 = 300 ≤ depth ≤ 600 µm.
- Cellpose/overlap parameters: IoU 0.15, cellprob −0.5, flow 0.5, diameter = median functional ROI diameter.
- The statistical replicate is the **session** (sound_tuning/am_tuning) or the **FOV** (multistim, where the unique key is subject + date + integer `FOV#` from info2p). Pooled-cell statistics are labeled exploratory only.
- Multistim cross-area with exactly two areas uses Mann-Whitney U with Cliff's delta, not Kruskal-Wallis. With three or more areas it uses KW, then pairwise MWU with Holm correction.
- Primary responsiveness uses `jaratoolbox` `dff=True`. Alternate dF/F definitions are sensitivity analyses only. The response scalar is mean(0–1 s) − mean(−1–0 s).
- `am_tuning` modes `tuningFreq` and `tuningAM` are never pooled. Frequency, AM-rate, and FM axes use log2 spacing.
- Outputs go under `settings.TEMP_OUTPUT_PATH/evan/`, not directly in `/tmp`.
