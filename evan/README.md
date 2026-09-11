# Two-photon auditory analysis scripts

Scripts by Evan Vickers for two-photon auditory cortex analyses in `jaratest/evan`.

This directory contains:

- single-session command-line tools for sound tuning and green/red visualization;
- batch analyses that combine multiple imaging sessions from one auditory cortical area;
- GREEN-versus-YELLOW comparisons within area and cortical layer;
- cross-area comparisons across A1, AAF, and A2;
- older versioned scripts retained for reproducibility.

For new analyses, use the most recent version listed below unless you specifically need to reproduce an older result.

## Recommended current scripts

| Analysis | Current script | Purpose |
|---|---|---|
| Single-session tuning | `twophoton_sound_tuning_cli.py` | Basic tuning/QC figures for one session |
| Single-session spatial maps | `twophoton_green_red_colocalization_cli.py` | Preferred-stimulus and dF/F-skewness spatial maps |
| `sound_tuning` area analysis | `sound_tuning_area_analysis_v13.py` | Batch analysis of one area across sessions |
| `sound_tuning` GREEN vs YELLOW by layer | `sound_tuning_area_layer_green_yellow_analysis_v3.py` | Within-area, within-layer GREEN/YELLOW comparisons |
| `sound_tuning` cross-area analysis | `sound_tuning_cross_area_cellclass_analysis_v4.py` | Compare A1/AAF/A2 within GREEN or YELLOW cells |
| `am_tuning` area analysis | `am_tuning_area_analysis_v9.py` | Batch frequency/AM-rate tuning analysis of one area |
| `am_tuning` GREEN vs YELLOW by layer | `am_tuning_area_layer_green_yellow_analysis_v4.py` | Within-area, within-layer GREEN/YELLOW comparisons |
| `am_tuning` cross-area analysis | `am_tuning_cross_area_cellclass_analysis_v5.py` | Compare A1/AAF/A2 within GREEN or YELLOW cells |

---

## Analysis conventions

### Auditory cortical areas

Area names from `info2p` are canonicalized as:

- `A1`: any `brainArea` containing `A1`
- `AAF`: any `brainArea` containing `AAF`
- `A2`: any `brainArea` containing `A2` or `AuV`

The area-level scripts preserve additional metadata such as depth and low-/high-frequency suffixes, but these are not used to define the canonical area.

### GREEN, YELLOW, and RED cells

The current batch pipelines use channel-2 anatomical overlap rather than the legacy Suite2p `redcell.npy` score to classify functional ROIs:

- **GREEN**: functional GCaMP ROI without sufficient tdTomato overlap
- **YELLOW**: functional GCaMP ROI with sufficient tdTomato overlap
- **RED**: anatomical tdTomato objects segmented from `meanImg_chan2`

Current Cellpose/overlap parameters are:

- IoU threshold: `0.15`
- Cellpose cell-probability threshold: `-0.5`
- Cellpose flow threshold: `0.5`
- Cellpose diameter: median equivalent diameter of the functional Suite2p ROIs

### Cortical layer bins

Layer-stratified analyses use:

- **L2/3**: `100 <= depth < 300 um`
- **L4/5**: `300 <= depth <= 600 um`

The 300-um boundary is assigned to L4/5 so that no session is counted twice.

### Statistical unit

For GREEN-versus-YELLOW and cross-area inference, the imaging **session** is treated as the primary biological replicate.

Pooled-cell statistics are retained where useful for descriptive/exploratory analyses, but cells from the same imaging session are not treated as independent biological replicates for the primary inference.

### Output location

Batch analyses write under:

```text
<jaratoolbox.settings.TEMP_OUTPUT_PATH>/evan/
```

rather than `/tmp` directly.

---

# 1. `sound_tuning` workflow

The `sound_tuning` workflow analyzes sessions containing fade-in, fade-out, and AM-rate stimuli.

## Step 1: run the area-level analysis

Run `sound_tuning_area_analysis_v13.py` separately for each area you want to include.

Example:

```bash
python sound_tuning_area_analysis_v13.py imag039 \
    --area A1 \
    --dates 20260729 20260730
```

Repeat for AAF and A2 when needed:

```bash
python sound_tuning_area_analysis_v13.py imag039 \
    --area AAF \
    --dates 20260729 20260730

python sound_tuning_area_analysis_v13.py imag039 \
    --area A2 \
    --dates 20260729 20260730
```

To inspect which `info2p` sessions will be selected without loading imaging data:

```bash
python sound_tuning_area_analysis_v13.py imag039 \
    --area A1 \
    --dates 20260729 20260730 \
    --dry-run
```

Important optional arguments:

```text
--plane N
--n-permutations N
--seed N
--dry-run
```

Default response-test permutations: `20000`.

### Main output structure

```text
<TEMP_OUTPUT_PATH>/evan/sound_tuning_area_analysis/<subject>/<area>/<date_tag>/
    session_selection.csv
    run_manifest.json
    session_outputs/
        <date>_<session>/
            ...
            <subject>_<date>_<session>_p<plane>_trial_response_archive_v13.npz
    combined/
        ...
```

### What v13 does

The area-level workflow includes:

- discovery of matching `sound_tuning` sessions from `info2p`;
- imaging/behavior event-alignment QC;
- Cellpose-based GREEN/YELLOW classification;
- event-locked dF/F responses;
- condition-specific FDR responsiveness;
- fade-in and fade-out response analysis;
- AM-rate response profiles;
- FI/FO and FI/best-AM selectivity;
- AM-rate lifetime sparseness;
- Gini, Fano-factor, and tuning-width summaries where applicable;
- all-cell and FDR-responsive-only figures;
- per-session and combined summaries;
- alternate dF/F sensitivity analyses;
- compact per-session trial-response archives for downstream trial-count/repetition robustness analyses.

The primary responsiveness labels are defined from the standard `jaratoolbox` `dff=True` analysis. Alternate dF/F definitions are retained as sensitivity analyses rather than redefining the primary responsive-cell population.

## Step 2: GREEN vs YELLOW within area and layer

After the area-level outputs have been generated, run:

```bash
python sound_tuning_area_layer_green_yellow_analysis_v3.py imag039 \
    --dates 20260729 20260730
```

By default this looks for A1, AAF, and A2 outputs. A subset can be selected with, for example:

```bash
python sound_tuning_area_layer_green_yellow_analysis_v3.py imag039 \
    --dates 20260729 20260730 \
    --areas A1 A2
```

Use `--dry-run` to print expected input/output paths without loading the tables.

This analysis compares GREEN and YELLOW populations independently in each AREA x LAYER stratum. Primary GREEN-versus-YELLOW tests are paired at the session level.

## Step 3: cross-area comparison

After area-level v13 outputs exist for the areas of interest, run:

```bash
python sound_tuning_cross_area_cellclass_analysis_v4.py imag039 \
    --dates 20260729 20260730
```

This compares:

- YELLOW cells across A1, AAF, and A2;
- GREEN cells across A1, AAF, and A2;

for:

- all depths;
- L2/3;
- L4/5.

Primary cross-area tests use one summary value per imaging session.

### Trial-reduction robustness analysis

For significant YELLOW cross-area findings, v4 can use the v13 trial-response archives to test how robust the result is to reducing the number of trials.

Defaults:

```text
trial fractions: 100%, 75%, 50%, 25%
Monte-Carlo resamples: 500
response permutations during reduced-trial FDR re-estimation: 512
```

Optional controls:

```bash
--trial-reduction-resamples 500
--trial-reduction-response-permutations 512
--trial-reduction-seed 20260826
--skip-trial-reduction
--dry-run
```

---

# 2. `am_tuning` workflow

The `am_tuning` pipeline supports two tuning modes:

- `tuningFreq`: pure-tone frequency tuning (`stimType == Sine`)
- `tuningAM`: amplitude-modulation-rate tuning (`stimType == AM`)

The two modes are analyzed separately and are never pooled together.

## Step 1: run the area-level analysis

Example:

```bash
python am_tuning_area_analysis_v9.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730
```

By default both `tuningFreq` and `tuningAM` are processed when present.

Frequency tuning only:

```bash
python am_tuning_area_analysis_v9.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730 \
    --mode tuningFreq
```

AM-rate tuning only:

```bash
python am_tuning_area_analysis_v9.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730 \
    --mode tuningAM
```

Discovery/QC only:

```bash
python am_tuning_area_analysis_v9.py imag039 \
    --area A1 \
    --dates 20260717 20260729 20260730 \
    --dry-run
```

Important optional arguments:

```text
--mode both|tuningFreq|tuningAM
--plane N
--n-permutations N
--seed N
--dry-run
```

Default response-test permutations: `20000`.

### Main output structure

```text
<TEMP_OUTPUT_PATH>/evan/am_tuning_area_analysis/<subject>/<area>/<date_tag>/
    session_selection.csv
    run_manifest.json
    tuningFreq/
        session_outputs/
        combined/
    tuningAM/
        session_outputs/
        combined/
```

### What v9 does

The area-level AM workflow includes:

- `info2p` session discovery;
- robust imaging/behavior alignment and timing QC;
- Cellpose-based GREEN/YELLOW classification;
- all-cell and FDR-responsive-only tuning curves;
- frequency- or AM-rate-specific FDR responsiveness;
- lifetime-sparseness selectivity as the primary tuning-selectivity metric;
- Gini coefficient, tuning-profile Fano factor, and FWHM bandwidth;
- condition-selectivity contrasts;
- intensity-resolved response profiles;
- session-level GREEN/YELLOW comparisons;
- selective/responsive example cells and combined rasters;
- alternate dF/F sensitivity analyses;
- per-session trial-response archives.

Frequency and AM-rate axes are plotted in explicit base-2 coordinates so equal frequency ratios occupy equal horizontal distances.

## Step 2: GREEN vs YELLOW within area and layer

After running the v9 area analysis for the desired areas:

```bash
python am_tuning_area_layer_green_yellow_analysis_v4.py imag039 \
    --dates 20260717 20260729 20260730
```

Frequency only:

```bash
python am_tuning_area_layer_green_yellow_analysis_v4.py imag039 \
    --dates 20260717 20260729 20260730 \
    --mode tuningFreq
```

AM rate only:

```bash
python am_tuning_area_layer_green_yellow_analysis_v4.py imag039 \
    --dates 20260717 20260729 20260730 \
    --mode tuningAM
```

Optional area subset:

```bash
--areas A1 AAF A2
```

This analysis compares GREEN vs YELLOW independently in each area/layer stratum using paired session-level inference.

## Step 3: cross-area comparison

Run:

```bash
python am_tuning_cross_area_cellclass_analysis_v5.py imag039 \
    --dates 20260717 20260729 20260730
```

Frequency only:

```bash
python am_tuning_cross_area_cellclass_analysis_v5.py imag039 \
    --dates 20260717 20260729 20260730 \
    --mode tuningFreq
```

This compares GREEN and YELLOW populations separately across A1, AAF, and A2, for all depths and for the L2/3 and L4/5 strata. Version 5 also includes dedicated area x layer tests of responsive-cell fractions and best-frequency distributions.

---

# 3. Single-session utilities

These scripts are useful for quick inspection of one session. They are separate from the newer batch/area workflows above.

## `twophoton_sound_tuning_cli.py`

Creates basic single-session sound-tuning outputs including:

1. event-locked average QC;
2. all-cell tuning curves;
3. responsive-cell tuning raster;
4. low-preferred-stimulus example cell;
5. high-preferred-stimulus example cell;
6. response-trace overlay for an example responsive cell;
7. red-vs-non-red tuning raster when red labels are available.

It does **not** generate the Cellpose GREEN/YELLOW spatial colocalization analysis used by the newer batch workflows.

AM example:

```bash
python twophoton_sound_tuning_cli.py \
    --subject imag029 --date 20260424 --session 006 --plane 0 \
    --paradigm am_tuning --sound-type AM
```

Frequency example:

```bash
python twophoton_sound_tuning_cli.py \
    --subject imag025 --date 20260417 --session 000 --plane 0 \
    --paradigm tuning_curve --sound-type frequency \
    --output-dir /data/twophoton/imag025_processed/20260417/000/analysis_outputs
```

Supported `--sound-type` values are:

```text
AM
frequency
natural
```

If `--suite2p-dir` is omitted, the script infers:

```text
settings.TWOPHOTON_PATH/<subject>_processed/<date>/<session>/suite2p/plane<plane>
```

Default output directory: `/tmp`.

## `twophoton_green_red_colocalization_cli.py`

Creates exactly one spatial-map PNG for a single session. The figure shows:

- preferred AM rate / preferred frequency / preferred stimulus;
- dF/F skewness.

Example:

```bash
python twophoton_green_red_colocalization_cli.py \
    --subject imag029 --date 20260424 --session 006 --plane 0 \
    --paradigm am_tuning --sound-type AM \
    --suite2p-dir /data/twophoton/imag029_processed/20260424/006/suite2p/plane0
```

Default output directory: `/tmp`.

Note that this older single-session utility supports several red-classification sources (`redcell`, GMM, percentile, or auto). That behavior is distinct from the finalized Cellpose-overlap GREEN/YELLOW classification used in the area-level pipelines.

---

# 4. Requirements and expected data

These scripts assume a working Jaramillo-lab Python environment with `jaratoolbox` configured for the local data paths.

The current analysis scripts use packages including:

```text
numpy
pandas
matplotlib
scipy
torch
suite2p
jaratoolbox
```

`scikit-learn` is optionally used by the older single-session colocalization CLI for Gaussian-mixture red-cell classification.

The batch workflows expect, as applicable:

- `info2p` metadata for session discovery;
- Suite2p outputs for the selected plane;
- `meanImg_chan2` for anatomical channel-2 segmentation/classification;
- behavioral files readable through `jaratoolbox`;
- imaging sound-trigger/event timing compatible with the alignment/QC routines.

A standalone `requirements.txt` is not currently maintained inside this folder, so the recommended approach is to run these scripts from the existing lab environment in which `jaratoolbox` and Suite2p are already configured.

---

# 5. Versioning

Many older script versions are intentionally retained in this directory.

For current analyses, use:

```text
sound_tuning_area_analysis_v13.py
sound_tuning_area_layer_green_yellow_analysis_v3.py
sound_tuning_cross_area_cellclass_analysis_v4.py

am_tuning_area_analysis_v9.py
am_tuning_area_layer_green_yellow_analysis_v4.py
am_tuning_cross_area_cellclass_analysis_v5.py
```

Use an older version only when reproducing an analysis that was originally generated with that version.

When adding a new version, please update this README so the recommended-script list and workflow examples continue to point to the current pipeline.
