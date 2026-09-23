# Two-photon auditory analysis scripts

Scripts by Evan Vickers for two-photon auditory cortex analyses in `jaratest/evan`.

This directory contains:

- single-session command-line tools for sound tuning and green/red visualization;
- batch analyses that combine multiple imaging sessions from one auditory cortical area;
- GREEN-versus-YELLOW comparisons within area and cortical layer;
- cross-area comparisons across A1, AAF, and A2;
- FOV-aware analysis of matched pure-tone, 3-tone-chord, and FM-sweep blocks;
- natural-sound response, repeat-variability, and repeat-number stability analyses;
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
| Multistim FOV analysis (stage 1) | `sound_tuning_multistim_fov_analysis_v3.py` | Analyze matched pure-tone, chord, and FM blocks from the same FOV |
| Multistim GREEN vs YELLOW by layer (stage 2) | `sound_tuning_multistim_area_layer_green_yellow_analysis_v4.py` | Compare GREEN/YELLOW cells within area and layer using FOV-level inference |
| Multistim cross-area analysis (stage 3) | `sound_tuning_multistim_cross_area_cellclass_analysis_v4.py` | Compare A1/AAF/A2 separately within GREEN and YELLOW cells |
| Natural-sound response analysis | `natural_sound_response_analysis_v2.py` | Analyze natural-sound responsiveness and same-condition repeat variability |
| Natural-sound repeat stability | `natural_sound_repeat_stability_v2.py` | Estimate how stable mean and variance estimates are as repeat count changes |

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

For the original `sound_tuning` and `am_tuning` GREEN-versus-YELLOW and cross-area analyses, the imaging **session** is treated as the primary biological replicate. For the newer multistim workflow, the shared imaging **FOV** is the primary replicate.

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

# 3. FOV-aware multistim `sound_tuning` workflow

This workflow analyzes the newer `sound_tuning` blocks:

- `pure_tones` / `pure_tone`;
- `chord_tones` / `chord_3t`;
- `fm_tones` / `fm_sounds` / `fm`.

It is designed for blocks acquired without moving the two-photon field of view and processed from one concatenated Suite2p binary. After the concatenated result is split into per-session folders, Suite2p ROI index `i` must refer to the same cell in every block assigned to that FOV.

### Current pipeline

| Stage | Script |
|---|---|
| 1. FOV analysis (run once per area) | `sound_tuning_multistim_fov_analysis_v3.py` |
| 2. GREEN vs YELLOW within area and layer | `sound_tuning_multistim_area_layer_green_yellow_analysis_v4.py` |
| 3. Cross-area comparison | `sound_tuning_multistim_cross_area_cellclass_analysis_v4.py` |

Example run for two areas:

```bash
python sound_tuning_multistim_fov_analysis_v3.py imag039 --area A1 --dates 20260910
python sound_tuning_multistim_fov_analysis_v3.py imag039 --area AAF --dates 20260910
python sound_tuning_multistim_area_layer_green_yellow_analysis_v4.py imag039 --dates 20260910 --areas A1 AAF
python sound_tuning_multistim_cross_area_cellclass_analysis_v4.py imag039 --dates 20260910 --areas A1 AAF
```

Stages 2 and 3 read the stage 1 outputs, so run stage 1 with v3 for every area of interest before running the v4 scripts. Stage 1 writes to the same output folder regardless of version, so a v3 run overwrites earlier v1/v2 stage 1 outputs for the same subject, area, and dates. The v4 downstream scripts are v3 plus the v2b fixes for FOVs that lack a sound block: cells with no data for a block are excluded from that block's plots, rasters, and statistics.

### Required `info2p` FOV metadata

`FOV#` is the authoritative grouping field and is an integer starting at 0. FOV numbers may be reused on different dates because the unique key is subject + date + `FOV#`.

Example session metadata:

```python
{
    "subject": "imag039",
    "date": "20260910",
    "session": "000",
    "paradigm": "sound_tuning",
    "sessionLabel": "pure_tones",
    "brainArea": "A1",
    "depth": 250,
    "FOV#": 0,
}
```

For older `info2p` files without `FOV#`, the script can infer provisional groups from acquisition order, brain area, depth, and block labels. Inspect `fov_manifest.csv`; use `--fov-groups` when a legacy day is ambiguous.

## Step 1: analyze each area

Run the FOV analysis once per area:

```bash
python sound_tuning_multistim_fov_analysis_v3.py imag039 \
    --area A1 \
    --dates 20260910

python sound_tuning_multistim_fov_analysis_v3.py imag039 \
    --area AAF \
    --dates 20260910
```

Check grouping without loading imaging data:

```bash
python sound_tuning_multistim_fov_analysis_v3.py imag039 \
    --area A1 \
    --dates 20260910 \
    --dry-run
```

Legacy explicit grouping example:

```bash
python sound_tuning_multistim_fov_analysis_v3.py imag039 \
    --area A1 \
    --dates 20260910 \
    --fov-groups 20260910:000-001-002 20260910:006-007
```

Important optional arguments:

```text
--plane N
--n-permutations N
--seed N
--fov-groups DATE:SESSION-SESSION-...
--dry-run
```

Default response-test permutations: `4096`.

### Main output structure

```text
<TEMP_OUTPUT_PATH>/evan/sound_tuning_multistim_fov_analysis/<subject>/<area>/<date_tag>/
    fov_manifest.csv
    run_manifest.json
    failures.json
    fov_outputs/
        <date>_FOV###/
            fov_cell_results.csv
            shared_FOV_green_yellow_classification.png
            individual_tuning_pages/
            cell_reports/
                green/
                yellow/
            ... per-block figures and trial-response archives ...
    combined/
        combined_cell_results.csv
        combined_fov_summary.csv
        responsiveness_statistics.json
        REPORT.txt
        ... combined figures ...
```

### What stage 1 (v3) does

- groups matched sessions by FOV and verifies shared Suite2p ROIs;
- performs one shared Cellpose GREEN/YELLOW classification per FOV;
- computes baseline-corrected responses using 0-1 s minus -1-0 s;
- tests each stimulus condition with Monte-Carlo sign flips and BH-FDR across cells;
- defines block responsiveness as the union of significant conditions;
- calculates lifetime sparseness, Gini coefficient, and tuning-profile Fano factor;
- calculates pure-tone BF and FWHM bandwidth, chord harmonic selectivity, and FM direction/speed selectivity;
- creates GREEN/YELLOW profiles, rasters, pure-tone BF summaries, 3 x 2 tuning pages, and one report per responsive cell;
- combines matched cells across sound blocks for cross-sound response-overlap summaries;
- saves trial archives (schema `multistim_v2`, unchanged in v3) used by the cross-area trial-reduction analysis;
- plots FM-sweep conditions on signed log2-magnitude axes, so adjacent tested FM rates are evenly spaced;
- writes dedicated selectivity figures (pure-tone lifetime sparseness, chord harmonic selectivity, FM direction selectivity) under `combined/selectivity_plots/<sound>/`, with the equation printed on each plot.

An FOV may lack one or more sound blocks. Block-specific plots exclude cells with no data for that block, and cell reports mark unavailable blocks explicitly.

## Step 2: GREEN vs YELLOW within area and layer

After running the FOV analysis for the desired areas:

```bash
python sound_tuning_multistim_area_layer_green_yellow_analysis_v4.py imag039 \
    --dates 20260910 \
    --areas A1 AAF
```

This script compares GREEN and YELLOW populations independently in each area x layer stratum. Primary tests use paired FOV summaries; pooled-cell plots are labeled exploratory. It includes all-cell and responsive-only tuning metrics, profiles, rasters, preference distributions, and pure-tone BF analyses. Dedicated selectivity figures are written under `<area>/<layer>/selectivity_plots/<sound>/`.

## Step 3: cross-area comparison

```bash
python sound_tuning_multistim_cross_area_cellclass_analysis_v4.py imag039 \
    --dates 20260910 \
    --areas A1 AAF
```

GREEN and YELLOW cells are analyzed separately for all depths, L2/3, and L4/5. The primary replicate is FOV. Dedicated selectivity figures are written under `<depth>/<cell_class>/selectivity_plots/<sound>/`, and within-area L2/3 vs L4/5 selectivity comparisons under `area_by_layer/<cell_class>/selectivity_plots/<sound>/`.

- With exactly two areas, the primary test is a two-sided Mann-Whitney U test on FOV-level summaries, with Cliff's delta.
- With three areas, the primary omnibus test is Kruskal-Wallis, followed by pairwise Mann-Whitney U tests.
- Holm correction is applied within the relevant test families.

For individually significant primary YELLOW results, the default robustness branch retains 100%, 75%, 50%, or 25% of trials within each FOV x sound block x stimulus condition and reruns the same analysis. This is an empirical stability analysis, not a prospective power calculation.

Optional controls:

```text
--trial-reduction-resamples 500
--trial-reduction-response-permutations 512
--trial-reduction-seed 20260910
--skip-trial-reduction
--dry-run
```

Always run `sound_tuning_multistim_fov_analysis_v3.py` before the v4 downstream scripts. If only v1 outputs exist, they lack the condition-level mean/SEM traces that the `multistim_v2` archive schema added, so stage 1 must be rerun.

---

# 4. Natural-sound response and repeat-stability workflow

The natural-sound workflow has two stages. First, analyze responses and save individual trial responses. Second, resample those trials to determine how stable response means and repeat-to-repeat variances are at different repeat counts.

## Step 1: natural-sound response analysis

Sessions are discovered from `info2p` using `paradigm == "natural_sound_detection"` and are analyzed independently. Different sessions may contain different sounds, repeat counts, durations, areas, or depths.

Analyze every matching session on a date:

```bash
python natural_sound_response_analysis_v2.py imag039 \
    --dates 20260717
```

Restrict the analysis when needed:

```bash
python natural_sound_response_analysis_v2.py imag039 \
    --dates 20260717 \
    --sessions 004 008 \
    --areas A2
```

Preview session selection:

```bash
python natural_sound_response_analysis_v2.py imag039 \
    --dates 20260717 \
    --dry-run
```

The preferred sound-identity key is `soundID`; `currentSound`, `soundType`, and `stimID` are accepted fallbacks. When possible, `soundID` is mapped to filenames using `sessionData/soundsList` in the behavior H5 file.

By default, a repeated condition always includes sound identity and automatically adds sound location and target intensity when either varies. Laser trials are excluded. Use `--location-mode ignore`, `--intensity-mode ignore`, or `--include-laser` only when that pooling is intentional.

### Responsiveness definitions

The primary `natural_responsive_fdr` label pools all valid natural-sound trials for each cell, applies a two-sided sign-flip test, and then applies BH-FDR once across cells. This is intended to retain power when each individual sound has few repeats.

A stricter secondary analysis tests each condition separately, applies BH-FDR across cells within that condition, and saves the union of condition-responsive labels. It is retained for interpretation but is not the default filter for repeat-stability analysis.

### Main outputs

```text
<TEMP_OUTPUT_PATH>/evan/natural_sound_response_analysis/<subject>/<date>/<session>/
    cell_results.csv
    condition_results.csv
    condition_summary.csv
    class_summary.csv
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
```

The trial archive contains the primary `jaratoolbox` dF/F responses plus whole-session-median and local 60-s prestimulus-median sensitivity versions. `natural_sound_response_analysis_v2.py` deliberately imports `am_tuning_area_analysis_v9.py` so classification, alignment, FDR, and dF/F conventions remain synchronized.

Important optional arguments:

```text
--sessions SESSION [SESSION ...]
--areas A1 AAF A2
--plane N
--n-permutations N
--seed N
--min-repeats-for-variance N
--min-repeats-for-test N
--response-start SECONDS
--response-end SECONDS
--location-mode auto|include|ignore
--intensity-mode auto|include|ignore
--include-laser
--dry-run
```

## Step 2: repeat-number stability analysis

Run the stability analysis only after creating v2 natural-sound trial archives:

```bash
python natural_sound_repeat_stability_v2.py imag039 \
    --dates 20260717
```

Example with selected sessions and more Monte-Carlo resamples:

```bash
python natural_sound_repeat_stability_v2.py imag039 \
    --dates 20260717 \
    --sessions 004 008 \
    --n-resamples 2000
```

The resampling unit is one cell x one natural-sound condition. For each observed sample size `k`, trials are sampled without replacement and the subsampled mean, sample variance, and sample SD are compared with estimates from all available repeats for that same unit.

Reported stability metrics include:

- relative absolute variance error;
- absolute log2 variance ratio;
- Spearman correlation between subsampled and full-repeat variance across units;
- mean error normalized by the full-repeat SD.

Two curves are produced:

- **available case**: every unit with at least `k` repeats contributes at each `k`;
- **fixed cohort**: the same eligible units contribute across the entire plotted range, avoiding composition changes as `k` increases.

The default design markers are `k = 4, 8, 16`. Unobserved values are reported as unobserved and are never extrapolated. The default empirical threshold summary searches for median variance relative error <= 0.25 and Spearman rho >= 0.90; these are transparent design criteria, not universal biological thresholds or formal power calculations.

Important optional arguments:

```text
--response-source primary|session_median|local_60s
--cell-filter responsive|all
--condition-responsive-only
--min-full-repeats N
--max-k N
--n-resamples N
--seed N
--design-k 4 8 16
--fixed-cohort-min-units N
--target-median-variance-relative-error FLOAT
--target-variance-spearman-rho FLOAT
--input-root PATH
--output-root PATH
```

Default inclusion uses cells passing the primary global natural-sound responsiveness test. `--cell-filter all` is intended as a QC/sensitivity analysis. If an archive reports zero responsive cells and uses the older v1 schema, rerun `natural_sound_response_analysis_v2.py` rather than interpreting an empty stability result.

---

# 5. Single-session utilities

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

# 6. Requirements and expected data

These scripts assume a working Jaramillo-lab Python environment with `jaratoolbox` configured for the local data paths.

The current analysis scripts use packages including:

```text
numpy
pandas
matplotlib
scipy
h5py
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

The multistim workflow additionally expects consistent Suite2p ROI indices across blocks assigned to the same FOV. The recommended metadata route is an explicit integer `FOV#` in every matching `info2p` session.

A standalone `requirements.txt` is not currently maintained inside this folder, so the recommended approach is to run these scripts from the existing lab environment in which `jaratoolbox` and Suite2p are already configured.

---

# 7. Versioning

Many older script versions are intentionally retained in this directory.

For current analyses, use:

```text
sound_tuning_area_analysis_v13.py
sound_tuning_area_layer_green_yellow_analysis_v3.py
sound_tuning_cross_area_cellclass_analysis_v4.py

am_tuning_area_analysis_v9.py
am_tuning_area_layer_green_yellow_analysis_v4.py
am_tuning_cross_area_cellclass_analysis_v5.py

sound_tuning_multistim_fov_analysis_v3.py
sound_tuning_multistim_area_layer_green_yellow_analysis_v4.py
sound_tuning_multistim_cross_area_cellclass_analysis_v4.py

natural_sound_response_analysis_v2.py
natural_sound_repeat_stability_v2.py
```

Use an older version only when reproducing an analysis that was originally generated with that version.

When adding a new version, please update this README so the recommended-script list and workflow examples continue to point to the current pipeline.
