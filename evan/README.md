# Two-photon auditory analysis scripts

Scripts by Evan Vickers for two-photon auditory cortex analyses in `jaratest/evan`.

This directory contains:

- single-session command-line tools for sound tuning and green/red visualization;
- batch analyses that combine multiple imaging sessions from one auditory cortical area;
- GREEN-versus-YELLOW comparisons within area and cortical layer;
- cross-area comparisons across A1, AAF, and A2;
- FOV-aware analysis of matched pure-tone, 3-tone-chord, and FM-sweep blocks;
- natural-sound response, repeat-variability, and repeat-number stability analyses;
- an experimental alternate branch for days with two chord F0 blocks per FOV (dual-F0 chord analysis; section 3b);
- a pure-tone level-series branch for tonotopic mapping across sound levels (threshold, CF, BF at each level in the same cells; section 3c);
- an automatic planner that detects which sounds were presented and runs the matching analyses (section 0);
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
| Quick BF check during an experiment | `quick_bf_check_v1.py` | Median BF of one pure-tone session (about 20 s after single-session Suite2p) with suggested centers / chord F0 and clipping checks |
| Automatic planner / runner | `sound_tuning_auto_analysis_v1.py` | Detect the sounds in each FOV and run the level-series and/or multistim analyses |
| Multistim FOV analysis (stage 1) | `sound_tuning_multistim_fov_analysis_v7.py` | Analyze matched pure-tone, chord, FM, FM fixed-range, band-noise, and noise-pair blocks from the same FOV; each single-cell panel notes the cell's BF (every pure-tone level), BF offset from the sound's center, and selectivity index |
| Multistim GREEN vs YELLOW by layer (stage 2) | `sound_tuning_multistim_area_layer_green_yellow_analysis_v6.py` | Compare GREEN/YELLOW cells within area and layer using FOV-level inference |
| Multistim cross-area analysis (stage 3) | `sound_tuning_multistim_cross_area_cellclass_analysis_v6.py` | Compare A1/AAF/A2 separately within GREEN and YELLOW cells |
| Pure-tone level series (stage 1) | `sound_tuning_pure_tone_levels_fov_analysis_v2.py` | BF / threshold / CF across sound levels in the same cells (section 3c) |
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

# 0. Automatic analysis (`sound_tuning_auto_analysis_v1.py`)

For `sound_tuning` days with FOV# in info2p, the planner reads every session's behavior file, works out which sounds were presented in each FOV, and runs the matching analyses:

| What it finds in an FOV | What it runs |
|---|---|
| pure-tone sessions at >= 2 levels | `sound_tuning_pure_tone_levels_fov_analysis_v2.py` on those sessions, then `posthoc_figures/bf_level_figures.py` and `posthoc_figures/bf_level_tonotopy.py` with `--fov-order AREA=<FOV# ascending>` |
| any chord, FM, FM fixed-range, band-noise, or noise-pair session | `sound_tuning_multistim_fov_analysis_v6.py` on those sessions plus the FOV's pure tones (one level per FOV). The planner still runs v6; run v7 directly (section 3) for the per-cell BF / SI notes and the other pure-tone levels |
| two chord F0s in one FOV | the dual-F0 branch (section 3b) |
| a red channel, and multistim blocks | stage 2; stage 3 if >= 2 areas |

Sessions without a behavior file or Suite2p output, with several sound types, or with AM / fading noise (section 1) are listed and left out.

```bash
python sound_tuning_auto_analysis_v1.py imag041 --dates 20261015 --dry-run   # print the plan only
python sound_tuning_auto_analysis_v1.py imag041 --dates 20261015
```

Options: `--areas`, `--only levels|multistim`, `--exclude-sessions`, `--pure-tone-level`, `--n-permutations`, `--skip-cell-reports`, `--no-fov-order` (sort FOVs by median BF/CF instead of FOV#), `--plane`. The plan and one log per step go to `<TEMP_OUTPUT_PATH>/evan/sound_tuning_auto_analysis/<subject>/<date_tag>/`. FOV# should follow the physical order along the tonotopic axis, because it sets the order of the level-series figures.

## Quick BF check during an experiment (`quick_bf_check_v1.py`)

Use it after a pure-tone session (70 dB recommended: the planned level of the other sounds and the highest clean tone level with the current calibration) and a single-session Suite2p run, to choose the next blocks' frequencies:

```bash
python quick_bf_check_v1.py imag041 20261022 001
```

It prints and saves (`<TEMP_OUTPUT_PATH>/evan/quick_bf_check_<session>/<subject>/<date>_<session>/`) the median BF of BF-eligible cells with a bootstrap 95% CI, the half-max centroid median, and the center that puts the most cells within ±0.5 octave. It also prints suggested `noisepair_center_freq` / `bandnoise_center_freq` (= median BF), `chord3t_F0` (= median BF; the chord spans BF to 4 × BF), and the fixed 2–40 kHz FM sweep. Each setting gets a clipping check at the planned levels (`--target-level`, `--noisepair-level`, `--tone-levels`), computed from the session's own left-speaker amplitudes and `--noise-amp-at-60db`. Figures: a report-style BF histogram (`bf_histogram_labeled.png` + `bf_histogram_unlabeled.tif`, same style as `posthoc_figures/bf_histogram_stack.py`, BF-eligible cells by default, `--hist-cells responsive` for all FDR-responsive cells, dashed line = target), BF histogram, normalized tuning raster sorted by BF, ROI map colored by BF, one page per 20 BF-eligible cells, and example traces. If the BF distribution has two clear peaks, it reports the two modes instead of the median, with one set of settings and clipping checks per mode. The test smooths the log2 BF values (0.3-octave kernel) and requires the two highest peaks to be at least 1 octave apart (`--mode-min-separation`), each to hold at least 20% of BF-eligible cells within ±0.5 octave (`--mode-min-fraction`), and the density between them to fall below 0.6 of the smaller peak (`--mode-max-dip`). It also warns when a single-peaked distribution is too spread for the median to represent the FOV, and when a target sits at the edge of the tested range. It uses the multistim v6 conventions; on imag041 20261015 it reproduced the level-series median BFs (sessions 004 and 015). ROI indices are those of the single-session Suite2p run.

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
- `fm_tones` / `fm_sounds` / `fm` (fixed-duration FM sweeps);
- `fm_range` (FM sweeps over a fixed frequency range; behavior stim type `FM_fixed_range`), v6 and later;
- `band_noise` (`Band_noise`), v6 and later;
- `noise_pair` (`Noise_pair`), v6 and later.

From v6 the block type comes from the behavior file (`current_stim_type`), not the sessionLabel, so labels such as `fm_sounds_frange_60dB` need no alias.

It is designed for blocks acquired without moving the two-photon field of view and processed from one concatenated Suite2p binary. After the concatenated result is split into per-session folders, Suite2p ROI index `i` must refer to the same cell in every block assigned to that FOV.

### Current pipeline

| Stage | Script |
|---|---|
| 1. FOV analysis (run once per area) | `sound_tuning_multistim_fov_analysis_v7.py` |
| 2. GREEN vs YELLOW within area and layer | `sound_tuning_multistim_area_layer_green_yellow_analysis_v6.py` |
| 3. Cross-area comparison | `sound_tuning_multistim_cross_area_cellclass_analysis_v6.py` |

Example run for two areas:

```bash
python sound_tuning_multistim_fov_analysis_v7.py imag039 --area A1 --dates 20260910
python sound_tuning_multistim_fov_analysis_v7.py imag039 --area AAF --dates 20260910
python sound_tuning_multistim_area_layer_green_yellow_analysis_v6.py imag039 --dates 20260910 --areas A1 AAF
python sound_tuning_multistim_cross_area_cellclass_analysis_v6.py imag039 --dates 20260910 --areas A1 AAF
```

Stages 2 and 3 read the stage 1 outputs, so run stage 1 (v7; v6 or v5 for an earlier result) for every area of interest before running the v6 scripts. v7 keeps the v6 columns and archive schema, so the v6 downstream scripts read it unchanged. Stage 2/3 v6 analyze pure tones, chords, and fixed-duration FM only; the fm_range / band_noise / noise_pair columns are ignored by them. Stage 1 writes to the same output folder regardless of version, so a v5 run overwrites earlier stage 1 outputs for the same subject, area, and dates. The v6 downstream scripts keep the v2b fixes for FOVs that lack a sound block: cells with no data for a block are excluded from that block's plots, rasters, and statistics.

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
python sound_tuning_multistim_fov_analysis_v7.py imag039 \
    --area A1 \
    --dates 20260910

python sound_tuning_multistim_fov_analysis_v7.py imag039 \
    --area AAF \
    --dates 20260910
```

Check grouping without loading imaging data:

```bash
python sound_tuning_multistim_fov_analysis_v7.py imag039 \
    --area A1 \
    --dates 20260910 \
    --dry-run
```

Legacy explicit grouping example:

```bash
python sound_tuning_multistim_fov_analysis_v7.py imag039 \
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
            pure_tones_other_levels/<N>dB/     (v7: FOVs with pure tones at several levels)
            ... per-block figures and trial-response archives ...
    combined/
        combined_cell_results.csv
        combined_fov_summary.csv
        responsiveness_statistics.json
        REPORT.txt
        ... combined figures ...
```

### What is new in stage 1 v7

v7 keeps the v6 statistics, response windows, column names, and trial archives (`schema_version = multistim_v2`). The extra pure-tone levels get their own seeds, so the other blocks' random draws are the same as in v6. New:

- **Per-cell notes on every single-cell panel** (`individual_tuning_pages/<block>/` and each tuning panel of `cell_reports/`):
  - `BF: 70 dB 8.09 kHz · 75 dB 6.63 kHz`: the cell's BF at each pure-tone level of that FOV, the pure_tones block level first. `n.s.` means not BF-eligible at that level.
  - `BF re band center (8 kHz): −0.29 oct`: BF (pure_tones level) relative to the sound's center frequency (FM center, band center, noise-pair A center) or chord F0. Only for BF-eligible cells.
  - the selectivity index (as in v5/v6); noise-pair panels also give the per-cell novelty-test q.
  The tuning pages are drawn after all blocks of the FOV are merged, so they know each cell's BF. The cell-report title gives the BF note and, on its own line, the blocks the cell responds to.
- **Other pure-tone levels are analyzed, not skipped.** The pure_tones block level is chosen as in v6 (`--pure-tone-level`, or by default the level recorded in the most FOVs; ties: closest to the other blocks' level). Each other level in the FOV is analyzed the same way into `fov_outputs/<FOV>/pure_tones_other_levels/<N>dB/` (own archive, raster, tuning pages) and merged as `pure_<N>dB_*` columns. Run FOVs separately (or pass `--pure-tone-level`) when one FOV has only a different level, otherwise the "most FOVs" rule can pick that level for every FOV.
- **BF eligibility** as in the level-series branch and `quick_bf_check_v1.py`: `pure_bf_eligible` = responsive (FDR) & response at BF > 0 & q at BF < 0.05, plus `pure_q_at_bf` (and `pure_<N>dB_bf_eligible`, `pure_<N>dB_q_at_bf`). `pure_tones_level_db` records the pure_tones block level. Existing columns such as `pure_bf_octaves_from_<fmr|bn|np>_center` are unchanged and still use the argmax BF of every cell.
- **Reading the notes.** BF is the argmax of the tuning curve, so broadly tuned cells can show very different BFs at two levels (on 20261022 FOV1, 25% of cells eligible at both levels shifted by > 1 octave). A bounded index is ±1 when its two responses have opposite signs.
- **One output folder per subject, area, and dates.** `fov_outputs/<FOV>/` folders from separate runs coexist, but `combined/`, `fov_manifest.csv`, and `run_manifest.json` describe the last run only (a `--dry-run` also rewrites the two manifests). Copy `combined/` first to keep an earlier run's summaries.

### What is new in stage 1 v6

v6 analyzes pure tones, chords, and fixed-duration FM exactly as v5 does (the FOV grouping on imag039 20260910 is identical). New:

- **FM fixed range** (`fmr_`): condition = signed slope (oct/s). The sound lasts as long as the sweep (octave range / |slope|: 0.075–1.2 s for 6 octaves at 5–80 oct/s). Metrics as for fixed-duration FM: direction selectivity `fmr_direction_selectivity`, best slope, speed sparseness, plus `fmr_best_sweep_duration_s`.
- **Band noise** (`bn_`): condition = bandwidth (octaves) around a fixed center, AM at `bandnoise_mod_rate`. `bn_bandwidth_selectivity` SI_bw = (R_widest − R_narrowest) / (|R_widest| + |R_narrowest|); +1 = prefers broadband. Spectral density is the same for every bandwidth, so wider bands carry more total power.
- **Noise pair** (`np_`): two 0.1-s sounds, A = narrow band noise (`noisepair_center_freq`, `noisepair_bandwidth`), B = white noise, in orders AB, BA, AA, BB at several gaps. Condition code = 10 × order index (AB=0, BA=1, AA=2, BB=3) + gap in s. `np_novelty_selectivity` SI_nov = (R_diff − R_same) / (|R_diff| + |R_same|), with R_diff = mean(AB, BA) and R_same = mean(AA, BB). Both sides start once with A and once with B, so under linear summation the first-sound responses cancel and SI_nov measures the extra response to a second sound that differs from the first (stimulus-specific adaptation). Also per gap (`np_novelty_selectivity_gap_<g>_s`), `np_first_sound_selectivity` (A-first vs B-first; +1 = prefers band noise A), and a per-cell test of R_diff − R_same (`np_novelty_contrast`, `_z`, `_p`, `_q`, `_sig_fdr`; Welch-style z, BH-FDR across cells). The ratio is noisy when responses are small, so use the contrast test for "which cells adapt".
- **Response windows:** 0–1.4 s for fm_range and noise_pair, whose sounds last up to 1.2 s and 1.0 s (with ISI ≥ 1.4 s, the window never reaches the next sound); 0–1 s for every other block. Their indices are also saved for 0–1 s (`*_win0to1`). Baseline stays −1–0 s.
- **Real sound duration in alignment QC.** For fm_range and noise_pair the behavior file's `stim_duration` is the GUI value (0.5 s), not the sound length. v6 uses `current_FMfixedrange_sweep_duration` and 2 × `noisepair_sound_duration` + `current_noisepair_gap`.
- **One pure-tone level per FOV** when an FOV has a level series: `--pure-tone-level`, or by default the level recorded in the most FOVs (ties: closest to the other blocks' level). The other levels are listed as skipped. The level series itself goes to section 3c.
- **No red channel** (`nchannels = 1`): every cell is GREEN (= unclassified), `red_channel_recorded = False`, combined figures show all cells, and each selectivity index is tested against 0 per FOV (`combined/selectivity_plots/<sound>/*_by_FOV.png`, `selectivity_by_FOV_statistics.json`) instead of GREEN vs YELLOW.
- **BF relative to each new block's center frequency** (`pure_bf_octaves_from_<fmr|bn|np>_center`, octaves) with same-cell scatters against the new indices (per FOV). For fixed-range sweeps this is the main confound of direction selectivity: an upward sweep reaches a high-BF cell late, a downward sweep reaches it early.
- `combined/selectivity_plots/noise_pair/noise_pair_gap_dependence.png`: SI_nov and per-order responses against gap.
- `posthoc_figures/noise_pair_novelty_by_gap.py <multistim run folder>` writes `combined/selectivity_plots/noise_pair/noise_pair_novelty_contrast_by_gap.png`: population traces of AB/BA/AA/BB at the 0.4 and 0.8 s gaps, and the novelty contrast mean(AB, BA) − mean(AA, BB) at each gap with a 95% CI **across trials** (trial responses averaged over cells first, so shared trial-to-trial noise is included), plus a ±20% band of the mean response as a smallest effect of interest. Use this figure, not the cell-level p-values, to judge whether the preceding sound matters. The design cannot isolate the effect of A on B by itself (4 orders, 6 unknowns).
- `posthoc_figures/noise_pair_second_sound_by_gap.py <multistim run folder>` answers "does the response to B depend on whether A preceded it, as a function of gap": `noise_pair_B_response_by_preceding_sound_and_gap.png` (+ `.txt`, `.json`) compares, in B-driven cells, B alone (B as the first sound), B after A (AB), and B after B (BB). The first sound's response is removed by subtracting a template: the mean trace of trials starting with the same frozen sound at the longest gap, valid until 0.9 s and extrapolated linearly after that (so the 0.8 s gap is less certain). Each B response is the mean over 0.4 s after B onset. 95% CIs and p-values are bootstrapped over trials. It reloads the noise-pair sessions, because single-trial traces are not in the archive. This assumes the two responses add; at the 0.1–0.2 s gaps the second window overlaps the first response's peak, so sublinear summation after a large first response (B) would look like B-specific adaptation.
- `--sessions`, `--exclude-sessions`, `--skip-cell-reports`. Sessions without a behavior file are skipped. Cell reports show one row per block recorded in that FOV.
- Archives keep `schema_version = multistim_v2` and add `response_window_s`, `trial_sound_duration_s`, and `level_db`.

### What stage 1 (v5) does

- groups matched sessions by FOV and verifies shared Suite2p ROIs;
- performs one shared Cellpose GREEN/YELLOW classification per FOV;
- computes baseline-corrected responses using 0-1 s minus -1-0 s;
- tests each stimulus condition with Monte-Carlo sign flips and BH-FDR across cells;
- defines block responsiveness as the union of significant conditions;
- calculates lifetime sparseness, Gini coefficient, and tuning-profile Fano factor;
- calculates pure-tone BF and FWHM bandwidth, chord harmonic selectivity, and FM direction/speed selectivity;
- creates GREEN/YELLOW profiles, rasters, pure-tone BF summaries, 3 x 2 tuning pages, and one report per responsive cell;
- combines matched cells across sound blocks for cross-sound response-overlap summaries;
- saves trial archives (schema `multistim_v2`, unchanged in v3 to v5) used by the cross-area trial-reduction analysis;
- plots FM-sweep conditions on signed log2-magnitude axes, so adjacent tested FM rates are evenly spaced;
- writes dedicated selectivity figures (pure-tone lifetime sparseness, chord harmonic selectivity, FM direction selectivity) under `combined/selectivity_plots/<sound>/`;
- prints each cell's selectivity index for the matching sound type (pure tones S_life, chords SI_harm, FM SI_dir) on every `individual_tuning_pages` panel and on each sound row of every `cell_reports` image. Missing values print as `NA`.

On every dedicated selectivity figure (stages 1-3), the statistics and the index equation share one side panel, with the equation drawn large directly under the p-values, so neither covers data points. Stage 2 v6 also places FM significance asterisks at the signed-log2 FM axis positions, and kHz tick labels are rounded to 3 significant figures.

An FOV may lack one or more sound blocks. Block-specific plots exclude cells with no data for that block, and cell reports mark unavailable blocks explicitly.

## Step 2: GREEN vs YELLOW within area and layer

After running the FOV analysis for the desired areas:

```bash
python sound_tuning_multistim_area_layer_green_yellow_analysis_v6.py imag039 \
    --dates 20260910 \
    --areas A1 AAF
```

This script compares GREEN and YELLOW populations independently in each area x layer stratum. Primary tests use paired FOV summaries; pooled-cell plots are labeled exploratory. It includes all-cell and responsive-only tuning metrics, profiles, rasters, preference distributions, and pure-tone BF analyses. Dedicated selectivity figures are written under `<area>/<layer>/selectivity_plots/<sound>/`.

## Step 3: cross-area comparison

```bash
python sound_tuning_multistim_cross_area_cellclass_analysis_v6.py imag039 \
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

Always run `sound_tuning_multistim_fov_analysis_v7.py` (or v6/v5) before the v6 downstream scripts. If only v1 outputs exist, they lack the condition-level mean/SEM traces that the `multistim_v2` archive schema added, so stage 1 must be rerun.

---

# 3b. ALTERNATE BRANCH (experimental): dual-F0 chord analysis

**Status:** alternate analysis branch, not yet part of the recommended pipeline. Treat its results as provisional until they have been reviewed. It writes to its own output folders, so it never overwrites the main multistim pipeline.

Use it for days where each FOV has **two `chord_tones` sessions with different chord F0s**, for example imag039 20260924: F0 = 4 kHz and 6.5 kHz, with no FM block. The main stage-1 script stops on these days with "duplicate block types".

| Stage | Script |
|---|---|
| 1. FOV analysis (run once per area) | `sound_tuning_multistim_dualF0_fov_analysis_v1.py` |
| 2. GREEN vs YELLOW within area and layer | `sound_tuning_multistim_dualF0_area_layer_green_yellow_analysis_v1.py` |
| 3. Cross-area comparison | `sound_tuning_multistim_dualF0_cross_area_cellclass_analysis_v1.py` |

```bash
python sound_tuning_multistim_dualF0_fov_analysis_v1.py imag039 --area A1 --dates 20260924
python sound_tuning_multistim_dualF0_fov_analysis_v1.py imag039 --area AAF --dates 20260924
python sound_tuning_multistim_dualF0_area_layer_green_yellow_analysis_v1.py imag039 --dates 20260924 --areas A1 AAF
python sound_tuning_multistim_dualF0_cross_area_cellclass_analysis_v1.py imag039 --dates 20260924 --areas A1 AAF
```

All options are the same as in the main pipeline, including `--dry-run`. The stage-1 dry run also prints which F0 each chord session was assigned.

### What differs from the main pipeline

- **Chord blocks split by F0.** Stage 1 reads `chord3t_F0` from each chord session's behavior file and assigns it to `chord_lowF0` (column prefix `chordlo_`) or `chord_highF0` (`chordhi_`). At most two distinct F0s are allowed per run, and stages 2 and 3 check that each block has one F0 across all areas. Each block keeps the usual within-block metrics, including within-block harmonic selectivity `chordlo_/chordhi_harmonic_selectivity`.
- **Combined harmonic selectivity** uses both chord blocks to control for each neuron's frequency preference:
  - **Primary:** `chord_matched_harmonic_selectivity`, a frequency-matched 2 × 2 index. H is the mean response to the two harmonic chords (middle tone at 2×F0 in each block). N is the mean response to the two non-harmonic chords whose middle tone is closest in absolute frequency to the other block's harmonic tone. For F0 = 4 / 6.5 kHz that pairs 8.00 kHz with 8.47 kHz and 13.0 kHz with 12.28 kHz, 0.08 octave apart each; the maximum allowed gap is 0.15 octave. SI = (H − N)/(|H| + |N|). Each F0 block and each middle-frequency region contributes one harmonic and one non-harmonic term, so a preference for the outer tones or for the middle-tone frequency cancels out.
  - **Sensitivity:** `chord_bfresid_harmonic_selectivity`. Each chord response is predicted as a + b × (sum of the cell's pure-tone responses at the chord's three frequencies, interpolated in log2 frequency). a and b are fit on the eight non-harmonic chords only. The index is the mean residual of the two harmonic chords divided by the cell's mean |chord response|. It is undefined (NaN) when a cell has no usable pure-tone tuning.
  - The two indices are tested separately, not as one Holm family. Figures are under `selectivity_plots/chord_combined_matched/` and `selectivity_plots/chord_combined_bfresid/` at each stage. Stage 3 also includes them in the area × layer tests and the YELLOW trial-reduction robustness branch.
- **Best frequency across all FOVs of an area.** These outputs come from stage 1, in `combined/best_frequency_across_FOVs/`:
  - BF of every pure-tone-responsive cell per FOV, with Kruskal-Wallis across FOVs;
  - pairwise FOV heatmaps (Mann-Whitney U, Holm across pairs);
  - FOV median BF grouped by the brainArea subfield label (for example `lowFreq` vs `highFreq`), with FOV as the replicate.

  The cell-level tests describe BF differences between FOVs, i.e. tonotopic position. They are not GREEN/YELLOW inference.
- **Outputs** go under `<TEMP_OUTPUT_PATH>/evan/sound_tuning_multistim_dualF0_{fov_analysis,area_layer_green_yellow_analysis,cross_area_cellclass_analysis}/`.

---

# 3c. ALTERNATE BRANCH: pure-tone level series (tonotopic mapping across sound levels)

**Status:** v1. The analyses were reviewed on the imag041 20261008 pilot. That day is too sparse for conclusions (see "Pilot data and next recordings" below). The branch writes to its own output folder.

**Why several levels.** Response thresholds differ across A1. For example, cells at the low-frequency pole may need louder tones before they respond, so a map built from one quiet level under-samples parts of the tonotopic axis. Each FOV is therefore imaged at several levels (e.g. 45, 55, 65, 75 dB SPL), and the map is built from all of them: each cell gets a threshold and a characteristic frequency (CF), and we can see at which level each part of the map fills in. Comparing BF across levels in the same cells also shows how far the preferred frequency moves with level, i.e. how safe it is to combine levels.

Use it for days where each FOV has **several `pure_tones` sessions at different sound levels**, processed from one concatenated Suite2p run so the ROIs are the same cells in every level. In info2p, give each session the FOV's `FOV#` and a `sessionLabel` of the form `pure_tones_<N>dB` (for example `pure_tones_45dB`). The level is checked against the behavior file (`tone_intensity` / `current_intensity`) when the session is analyzed, and the script stops if any trial is not a pure tone. A plain `pure_tones` label falls back to the behavior file. An FOV may have any subset of levels: an FOV with a single level (imag041 FOV 4, session 016, 75 dB only) is included in the per-level analyses and skipped by the paired cross-level comparisons.

| Step | Script |
|---|---|
| 1. FOV analysis (run once per area) | `sound_tuning_pure_tone_levels_fov_analysis_v2.py` (v1 + `--sessions` / `--exclude-sessions`; skips sessions without a behavior file; same outputs) |
| Report figures | `posthoc_figures/bf_level_figures.py` (then `posthoc_figures/make_wiki_pngs.py` if needed) |
| Tonotopic map from all levels | `posthoc_figures/bf_level_tonotopy.py`: threshold, CF, center frequency at threshold + 10 / + 20 dB, recruitment by level, threshold vs CF, ROI maps on the mean image with a fitted frequency gradient |

The two posthoc scripts read only stage-1 outputs (plus each FOV's Suite2p `ops.npy` / `stat.npy` for the maps), so they can be rerun with a different FOV order without rerunning stage 1. Pass `--fov-order AREA=...` in physical order along the tonotopic axis (for imag041 20261008: FOV 0 → 4 runs from low to high frequency, `A1=0,1,2,3,4`). Without it, FOVs are sorted by median BF / CF.

```bash
python sound_tuning_pure_tone_levels_fov_analysis_v2.py imag041 --area A1 --dates 20261008 --dry-run
python sound_tuning_pure_tone_levels_fov_analysis_v2.py imag041 --area A1 --dates 20261008
python sound_tuning_pure_tone_levels_fov_analysis_v2.py imag041 --area A1 --dates 20261015 --sessions 001-004 012-015
python posthoc_figures/bf_level_figures.py \
    <TEMP_OUTPUT_PATH>/evan/sound_tuning_pure_tone_levels_fov_analysis/imag041 --date 20261008 --areas A1 \
    --fov-order A1=0,1,2,3,4
python posthoc_figures/bf_level_tonotopy.py \
    <TEMP_OUTPUT_PATH>/evan/sound_tuning_pure_tone_levels_fov_analysis/imag041 --date 20261008 --areas A1 \
    --fov-order A1=0,1,2,3,4
```

On the lab workstation `TEMP_OUTPUT_PATH` is `/var/tmp/`, so outputs land under `/var/tmp/evan/`. Most of the stage-1 run time goes to the per-cell report PNGs (`--skip-cell-reports` turns them off).

**Recordings without a red channel** (PMT1 not recorded, `nchannels = 1` in ops, as for imag041 20261008) are detected automatically. Cellpose is skipped and every cell is labeled GREEN, with `red_channel_recorded = False`, so here GREEN means "not classified", not "tdTomato-negative". If no FOV in the run has a red channel, the GREEN-vs-YELLOW comparisons are skipped and the summary figures show all cells in one column.

Options: `--n-permutations` (responsiveness, default 4096), `--n-shift-permutations` (per-cell BF-shift test, default 2000), `--reference-level` (default: highest level), `--skip-cell-reports` (the per-cell report PNGs are the slowest part), `--plane`, `--seed`, `--dry-run`.

### Definitions

- Responsiveness, response scalar, dF/F, Cellpose GREEN/YELLOW classification, and BF (argmax of the mean tuning curve) are the same as in the multistim pipeline, computed separately at each level.
- **BF-eligible** at a level: FDR-responsive at that level, response at BF > 0, and q < 0.05 at the BF itself. All cross-level BF comparisons use BF-eligible cells. The per-level replicas of earlier BF outputs keep the earlier rule (all FDR-responsive cells).
- **Half-max centroid BF:** mean log2 frequency weighted by (response − peak/2) over the frequencies at or above half the peak. It is less granular than the argmax and is unchanged by a pure gain change.
- **BF shift** for a level pair = log2(BF_high-level / BF_low-level) in octaves, for the same cell. **Slope** = least-squares slope of log2 BF against level, in octaves per 10 dB (cells BF-eligible at ≥ 3 levels).
- **Per-cell shift test:** within each frequency, the trials of the two levels are pooled and the level labels are shuffled; BH-FDR across cells per pair within each FOV. Use the **centroid** version. On synthetic data it detected a 0.9-octave shift in >99% of cells, with no false positives for unshifted cells tuned away from the range edges. The argmax version is very conservative and is kept for reference. Caveat: when tuning broadens with level, a cell whose BF is within ~1.5 octaves of the lowest or highest tested frequency is truncated at the range edge, which really does move its centroid. Check edge cells before calling their shift a BF change.
- **Threshold:** the lowest level with a significant excitatory response (any frequency with q < 0.05 and mean response > 0). A threshold at the lowest level recorded in that FOV is censored: it means "≤ that level". **CF:** the significant excitatory frequency with the largest response at the threshold level. **Pooled BF:** argmax of the tuning curve averaged across levels. Stage 1 computes threshold/CF only for FOVs with ≥ 2 levels; `bf_level_tonotopy.py` recomputes them from the stage-1 columns for every FOV. For a single-level FOV its "CF" is the BF at that level, with a censored threshold.
- **Center frequency at threshold + 10 / + 20 dB** (`bf_level_tonotopy.py`): the half-max centroid at that level, if the level was recorded and the cell has a significant excitatory response there. The argmax BF at that level is also in the CSV. With 45–75 dB in 10 dB steps, + 20 dB exists only for thresholds of 45 or 55 dB. On the pilot data, the + 20 dB center sat a median 0.9 octave below CF, the usual low-frequency broadening at louder levels, so CF and center-frequency maps are not interchangeable.
- **Maps** use the imaging frame (rows/columns of the Suite2p mean image), not cortical axes. The gradient arrow is a least-squares fit of log2 frequency on ROI center position (octaves per 100 pixels; pixel size depends on magnification), with a permutation p-value from shuffling frequencies across ROIs.
- **Statistics:** FOV is the replicate. Across FOVs the script uses Wilcoxon on FOV medians (shift vs 0, Holm across levels), Friedman across levels on FOVs that have every level, and paired FOV Wilcoxon for GREEN vs YELLOW. With 4 FOVs, the smallest possible two-sided Wilcoxon p is 0.125, so within-FOV cell-level tests (which describe that FOV) and pooled-cell tests (labeled exploratory) are also reported.

### Outputs

```text
<TEMP_OUTPUT_PATH>/evan/sound_tuning_pure_tone_levels_fov_analysis/<subject>/<area>/<date_tag>/
    fov_manifest.csv, run_manifest.json, failures.json
    fov_outputs/<date>_FOV###/
        *_pure_tones_<N>dB_trial_response_archive_levels_v1.npz   (schema_version pure_tone_levels_v1, level_db)
        <N>dB/                     profile, raster, BF histogram at that level
        level_tuning_pages/        all cells responsive at any level; tuning curves at every level overlaid
        cell_reports/<class>/      frequency x level response map, tuning curves per level, traces at each level's BF
        fov_cell_results.csv
    combined/
        combined_cell_results.csv           wide: pure_<N>dB_* per level + cross-level columns
                                            (bfshift_/centroidshift_<b>_vs_<a>dB_oct, _perm_p, _perm_q,
                                             bf_/centroid_level_slope_oct_per_10dB, threshold_level_db, cf_hz, pooled_bf_hz)
        combined_cell_level_results.csv     long: one row per cell x level
        responsive_fraction_GREEN_vs_YELLOW_by_level.png
        per_level/<N>dB/best_frequency/ and best_frequency_across_FOVs/   the earlier BF outputs, one folder per level
        best_frequency_across_levels/
            tuning_metrics_by_level.png        % responsive, % BF-eligible, median BF, response at BF, FWHM, sparseness
            BF_distribution_by_level.png       BF distributions per level, pooled and per FOV
            BF_pairwise_level_scatter.png      same cells, BF at level a vs level b, every pair
            BF_shift_vs_reference_level.png    shift re reference level (argmax and centroid), FOV medians
            bf_level_slope_by_FOV.png, centroid_level_slope_by_FOV.png
            BF_across_levels_cell_matrix.png   cells x levels BF map per FOV
            BF_shift_permutation_significance.png
            threshold_and_CF.png
            *.csv, BF_across_levels_statistics.json
        REPORT.txt
<TEMP_OUTPUT_PATH>/evan/posthoc_figures/bf_levels/   (bf_level_figures.py; labeled PNG + unlabeled TIFF)
<TEMP_OUTPUT_PATH>/evan/posthoc_figures/bf_levels_tonotopy/   (bf_level_tonotopy.py)
    <subject>_<date>_<area>_tonotopy_cells.csv          one row per cell: threshold (+ censored flag), CF,
                                                        center frequency and BF at threshold + 10 / + 20 dB, BF per level
    <subject>_<date>_<area>_tonotopy_FOV_summary.csv    cells, responsive, with CF, thresholds per level, median CF
    *_recruitment_CF_by_threshold*                      CF counts per FOV stacked by threshold level
    *_threshold_vs_CF*.png                              per FOV and pooled; Spearman rho (cells within FOV; pooled = exploratory)
    *_tonotopic_map_CF_center10_center20*               ROI masks colored by frequency, gradient arrow
    *_tonotopic_map_BF_by_level*                        same, BF at each level
    *_CF_vs_center_frequency.png
    tonotopy_statistics.json
```

### Pilot data and next recordings

imag041 20261008 (A1; FOVs 0 → 4 from low to high frequency; FOVs 0–3 at 45/55/65/75 dB, FOV 4 = session 016 at 75 dB only; no red channel) ran end to end but cannot answer the tonotopy question:

- The four concatenated Suite2p runs (sessions 000-003, 004-007, 008-011, 012-015) detected only 49 / 20 / 24 / 54 ROIs in total, while the standalone session 016 had 827 ROIs (207 kept as cells), with the same settings. The mean images show many more somata. FOV 0 (low-frequency pole) had only 5 cells with a CF.
- At 75 dB, FOV 4 (nominal high-frequency end) was mostly tuned to 4–6 kHz, so the FOV medians do not follow the nominal order. Several FOVs pile up BFs at 40 kHz, the top of the tested range.

For the next recordings:
- record all four levels in at least 3 FOVs along the tonotopic axis, and number `FOV#` in physical order;
- after Suite2p, compare the concatenated run's ROI count with a single-session run of the same FOV before analyzing;
- consider extending the frequency range if many BFs sit at the top (or bottom) tested frequency;
- record PMT1 if GREEN/YELLOW classification is wanted (without it every cell is labeled GREEN, meaning unclassified).

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

sound_tuning_auto_analysis_v1.py

sound_tuning_multistim_fov_analysis_v7.py
sound_tuning_multistim_area_layer_green_yellow_analysis_v6.py
sound_tuning_multistim_cross_area_cellclass_analysis_v6.py

natural_sound_response_analysis_v2.py
natural_sound_repeat_stability_v2.py
```

Use an older version only when reproducing an analysis that was originally generated with that version.

The `sound_tuning_multistim_dualF0_*_v1.py` scripts are an experimental alternate branch (section 3b), not part of the recommended list above.

`sound_tuning_pure_tone_levels_fov_analysis_v2.py` (section 3c) is a separate branch for pure-tone level-series days. It is the only stage-1 script for that experiment (v1 is kept for the 20261008 pilot); its report figures come from `posthoc_figures/bf_level_figures.py` and `posthoc_figures/bf_level_tonotopy.py`.

When adding a new version, please update this README so the recommended-script list and workflow examples continue to point to the current pipeline.
