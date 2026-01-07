OVERVIEW:
---------
This directory contains scripts for analyzing frequency and amplitude modulation
(AM) tuning in auditory cortex neurons under optogenetic manipulation conditions.

There are 3 groups of scripts located in the following folders:
* AC_inhibition_group
* TH_inhibition_group
* control_group
In each of these folders there are subfolders for frequency tuning, AM tuning, and Gaussian fitting.

In addition to this there is:
* raster_plot_scripts - for plotting rasters for recording from each animal
* comparison_scripts - for plotting comparisons between pathways

Scripts follow a naming convention:
  [prefix]_[subject]_[analysis]_[data_type].py

Where:
  - prefix: "archT" (archaerhodopsin inhibition experiments)
  - subject: Animal group (arch018, arch019, arch020, arch022, arch024)
  - analysis: Type of analysis (e.g., calculate, plot, statistics)
  - data_type: "freq" (frequency tuning) or "AM" (amplitude modulation tuning)

EXPERIMENTAL CONDITIONS:
------------------------
1. AC (Auditory Cortex) Inhibition:
   - arch018, arch019, arch020, arch022: Direct AC inhibition
   
2. Th-pStr (Thalamo-striatal) Inhibition:
   - arch024: Thalamic input inhibition to striatum
   
3. Control Sessions:
   - arch024/control_sessions/: Control recordings with the same animals from AC-pStr 
     inhibition group but laser was 'blocked'

TYPICAL WORKFLOW:
-----------------
0. Update the config.py file to define outputs by updating the 'DEFAULT_REPORTS_ROOT' path
1. Run CALCULATION script → generates tuning metrics CSV files
2. (Optional) Edit classification_overrides.csv for manual corrections
3. Run PLOT script → visualize individual cell tuning curves + rasters
4. Run TRENDS script → classify cells by laser effects
5. Run STATISTICS script → population-level statistical analysis
6. Run GAUSSIAN FITTING script → parametric tuning curve analysis
   a. Fits Gaussian models to each cell's tuning curve (OFF and ON)
   b. Extracts parameters (amplitude, center frequency, sigma, baseline)
   c. Calculates goodness of fit (R²) for quality control
   d. Performs paired statistical tests on parameter changes
   e. Generates comparison plots showing parameter shifts
   f. Identifies cells with significant parameter changes (e.g., bandwidth narrowing)
7. Run COMPARISON scripts → compare different experimental groups
   a. Load metrics from multiple groups (e.g., AC vs controls)
   b. Perform unpaired statistical tests between groups
   c. Generate violin plots and effect size comparisons
   d. Can compare either tuning metrics or Gaussian fit parameters


MAIN SCRIPT TYPES:
------------------

1. CALCULATION SCRIPTS - Compute tuning metrics from raw data

   Pure Tones:
   - archT_AC_calculate_frequency_tuning.py
   - archT_AC_controls_calculate_frequency_tuning.py
   - archT_Th_calculate_frequency_tuning.py
   - archT_Th_cntrl_calculate_frequency_tuning.py

   Amplitude Modulation:
   - archT_AC_calculate_AM_tuning.py
   - archT_AC_controls_calculate_AM_tuning.py
   - archT_Th_calculate_AM_tuning.py
   - archT_Th_cntrl_calculate_AM_tuning.py

   Function: Each script will analyse the following for a defined dataset: Calculates selectivity index, sparseness,
             bandwidth, tuning quality for both laser OFF and ON conditions

   Input: spike sorted data 
   
   You will need to update the following inside the script to add/change recording sites:
   SESSIONS = {
       0: SessionConfig('AnimalID', 'RecordingDate', RecordingDepth),
       1: SessionConfig('arch024', '2025-04-10', 3500),  # Example
   }

   Output: 
   - all_sessions_laser_off_tuning_metrics.csv
   - all_sessions_laser_on_tuning_metrics.csv
   - classification_overrides.csv (can be edited to manually override cell classifications)


2. PLOT SCRIPTS - Visualize tuning curves with rasters

   Pure Tones:
   - archT_AC_plot_tuning_freq_with_rasters.py
   - archT_AC_controls_plot_tuning_freq_with_rasters.py
   - archT_Th_plot_tuning_freq_with_rasters.py
   - archT_Th_cntrl_plot_tuning_freq_with_rasters.py

   Amplitude Modulation:
   - archT_AC_plot_tuning_AM_with_rasters.py
   - archT_AC_controls_plot_tuning_AM_with_rasters.py
   - archT_Th_plot_tuning_AM_with_rasters.py
   - archT_Th_cntrl_plot_tuning_AM_with_rasters.py

   Function: Creates multi-page PDFs showing tuning curves (top) and raster
             plots (bottom) for individual cells, organized by tuning category

   Input: 
   - all_sessions_laser_off_tuning_metrics.csv (from CALCULATION scripts)
   - all_sessions_laser_on_tuning_metrics.csv (from CALCULATION scripts)
   - classification_overrides.csv (optional manual corrections)
DEFAULT_REPORTS_ROOT
   Output: 
   - [category]_cells_with_rasters_all_sessions.pdf
   - Organized by tuning category (tuned/non-tuned)
   - 3 cells per page in landscape layout


3. TRENDS SCRIPTS - Plot laser effect trends across cells

   Pure Tones:
   - archT_AC_plot_freq_tuning_trends.py
   - archT_AC_controls_plot_freq_tuning_trends.py
   - archT_Th_plot_freq_tuning_trends.py
   - archT_Th_cntrl_plot_freq_tuning_trends.py

   Amplitude Modulation:
   - archT_AC_plot_AM_tuning_trends.py
   - archT_AC_controls_plot_AM_tuning_trends.py
   - archT_Th_plot_AM_tuning_trends.py
   - archT_Th_cntrl_plot_AM_tuning_trends.py

   Function: Classifies cells by laser effect (increase/decrease/no_change in
             tuning quality and firing rate), generates summary plot which shows the distribution

   Input: 
   - all_sessions_laser_off_tuning_metrics.csv (from CALCULATION scripts)
   - all_sessions_laser_on_tuning_metrics.csv (from CALCULATION scripts)
   - classification_overrides.csv (optional manual corrections)

   Classification Categories (6 total):
   - increase_tuning / decrease_tuning / no_change_tuning
   - increase_fr / decrease_fr / no_change_fr

   Output: 
   - [category]_archT_[subject]_tuning.pdf
   - category_distribution_summary.png
   - One PDF per category showing affected cells


4. STATISTICS SCRIPTS - Compare laser OFF vs ON conditions

   Pure Tones:
   - archT_AC_tuning_laser_effect_statistics.py
   - archT_AC_controls_tuning_laser_effect_statistics.py
   - archT_Th_tuning_laser_effect_statistics.py
   - archT_Th_cntrl_tuning_laser_effect_statistics.py

   Amplitude Modulation:
   - archT_AC_AM_tuning_laser_effect_statistics.py
   - archT_AC_controls_AM_tuning_laser_effect_statistics.py
   - archT_Th_AM_tuning_laser_effect_statistics.py
   - archT_Th_cntrl_AM_tuning_laser_effect_statistics.py

   Function: Performs paired statistical tests (Wilcoxon signed-rank),
             generates comparison plots, normalized population tuning curves

   Input: 
   - all_sessions_laser_off_tuning_metrics.csv (from CALCULATION scripts)
   - all_sessions_laser_on_tuning_metrics.csv (from CALCULATION scripts)
   - classification_overrides.csv (optional manual corrections)

   Statistical Tests:
   - Paired Wilcoxon signed-rank test (non-parametric)
   - Cohen's d for effect size
   - Pointwise significance testing on normalized curves

   Output: 
   - laser_on_vs_off_metrics.csv (merged OFF/ON data)
   - statistical_results.csv (test results)
   - laser_on_vs_off_comparison.pdf (scatter & bar plots)
   - selectivity_histogram_distribution.png
   - tuning_quality_histogram_distribution.png
   - normalized_tuning_curves.png
   - normalized_tuning_data.csv


5. GAUSSIAN FITTING SCRIPTS - Fit Gaussian models to tuning curves

   Pure Tones:
   - archT_AC_gaussian_tuning_freq.py
   - archT_AC_controls_gaussian_tuning_freq.py
   - archT_Th_gaussian_tuning_freq.py
   - archT_Th_cntrl_gaussian_tuning_freq.py

   Amplitude Modulation:
   - archT_AC_gaussian_tuning_AM.py
   - archT_AC_controls_gaussian_tuning_AM.py
   - archT_Th_gaussian_tuning_AM.py
   - archT_Th_cntrl_gaussian_tuning_AM.py

   Function: Fits Gaussian functions to individual cell tuning curves,
             extracts parameters (amplitude, center, width, baseline),
             compares laser OFF vs ON conditions

   Input: 
   - all_sessions_laser_off_tuning_metrics.csv (from CALCULATION scripts)
   - all_sessions_laser_on_tuning_metrics.csv (from CALCULATION scripts)
   - classification_overrides.csv (optional manual corrections)

   Gaussian Model:
   y = baseline + amplitude * exp(-((x - center)^2) / (2 * sigma^2))

   Parameters Extracted:
   - Amplitude (peak height above baseline)
   - Center (best frequency/rate in octaves)
   - Sigma (width/selectivity)
   - Baseline (spontaneous firing rate)
   - R² (goodness of fit)

   Output:
   - gaussian_fit_parameters.csv (all fit parameters)
   - gaussian_fit_quality_summary.csv (R² statistics)
   - gaussian_fits_example_cells.pdf (sample fits with residuals)
   - gaussian_parameter_comparison.pdf (OFF vs ON scatter plots)
   - gaussian_parameter_statistics.csv (paired test results)

   Quality Control:
   - Excludes fits with R² < 0.5 (poor fits)
   - Reports convergence failures
   - Handles cells with insufficient data points


6. COMPARISON SCRIPTS - Compare metrics across experimental groups

   Between AC Inhibition and Controls (Tuning Metrics):
   - compare_AC_vs_controls_freq.py
   - compare_AC_vs_controls_AM.py

   Between AC and Th-pStr Inhibition (Tuning Metrics):
   - compare_AC_vs_Th_freq.py
   - compare_AC_vs_Th_AM.py

   Between AC Inhibition and Controls (Gaussian Fit Data):
   - compare_AC_vs_controls_gaussian_freq.py
   - compare_AC_vs_controls_gaussian_AM.py

   Between AC and Th-pStr Inhibition (Gaussian Fit Data):
   - compare_AC_vs_Th_gaussian_freq.py
   - compare_AC_vs_Th_gaussian_AM.py

   Function: Compares tuning metrics between different experimental groups,
             performs statistical tests, generates comparative visualizations
             to determine group-level differences in laser effects

   Input: 
   - all_sessions_laser_off_tuning_metrics.csv (from each group's CALCULATION)
   - all_sessions_laser_on_tuning_metrics.csv (from each group's CALCULATION)
   - classification_overrides.csv (from each group, optional)
   
   For Gaussian comparisons, also uses:
   - gaussian_fit_parameters.csv (from each group's GAUSSIAN FITTING)
   - gaussian_fit_quality_summary.csv (from each group's GAUSSIAN FITTING)

   Statistical Tests:
   - Mann-Whitney U test (unpaired, non-parametric)
   - Two-sample Kolmogorov-Smirnov test (distribution comparison)
   - Effect size (Cohen's d) for group differences
   - Bootstrap confidence intervals

   Output:
   - group_comparison_metrics.csv (combined metrics from both groups)
   - group_comparison_statistics.csv (test results)
   - group_comparison_violin_plots.pdf (distribution comparisons)
   - group_comparison_scatter_plots.pdf (OFF vs ON for each group)
   - laser_effect_comparison.pdf (ΔSI, ΔTQ between groups)
   - group_normalized_tuning_curves.png (population averages)
   
   For Gaussian comparisons, also generates:
   - gaussian_parameter_group_comparison.pdf (amplitude, sigma, center comparisons)
   - gaussian_fit_quality_comparison.pdf (R² distributions between groups)

   Metrics Compared:
   - Laser effect magnitude (ΔSI, ΔTQ, ΔFR)
   - Baseline tuning properties (SI, sparseness, bandwidth)
   - Prevalence of tuned cells
   - Distribution of laser effect directions
   
   For Gaussian comparisons:
   - Gaussian parameter changes (Δamplitude, Δsigma, Δcenter)
   - Fit quality differences (R² distributions)
   - Parameter reliability across groups


7. SELECTED CELLS VISUALIZATION (OPTIONAL) - Publication-quality plots 
   (I used this for getting nice looking examples for my rotation talk)

   Pure Tones Only:
   - archT_AC_plot_selected_cells_freq.py

   Function: Creates high-quality publication-ready figures for manually
             selected cells of interest, with detailed tuning curves and
             raster plots showing laser effects

   Input:
   - all_sessions_laser_off_tuning_metrics.csv (from CALCULATION scripts)
   - all_sessions_laser_on_tuning_metrics.csv (from CALCULATION scripts)
   - Manually specified cell list in script (session_id, cell_idx pairs)
         (session ID is defined in the scripts in the SessionConfig)

   Cell Selection (edit in script):
   # Example cell list format:
   SELECTED_CELLS = [
       (0, 25),   # (session_id, cell_idx) 
       (1, 42),
       (3, 17),
   ]

   Output:
   - selected_cells_detailed_visualization.pdf
   - One page per cell with:
     * Tuning curves (OFF vs ON, normalized)
     * Raster plots (sorted by frequency, OFF/ON comparison)
     * Metrics overlay (SI, TQ, bandwidth, peak FR)
     * Statistical annotations (Wilcoxon test results)

   Features:
   - Colorblind-friendly palette
   - Publication-quality fonts and sizes
   - Consistent formatting across cells
   - High-resolution output (300 DPI)

   Use Case: For highlighting specific examples in papers/presentations


DATA ORGANIZATION:
------------------
All outputs are saved to: /data/reports/[subject]/[analysis_type]/

Where analysis_type is:
  - tuning_freq_analysis/ (frequency tuning)
  - tuning_AM_analysis/ (amplitude modulation tuning)

Subdirectories created:
  - tuning_with_rasters/ (PLOT outputs)
  - laser_statistics/ (STATISTICS outputs)
  - laser_statistics_SI_filtered/ (filtered STATISTICS outputs)
  - gaussian_fits/ (GAUSSIAN FITTING outputs)

KEY OUTPUT FILES:
-----------------
From CALCULATION:
- all_sessions_laser_off_tuning_metrics.csv
- all_sessions_laser_on_tuning_metrics.csv
- classification_overrides.csv

From PLOT:
- tuned_cells_with_rasters_all_sessions.pdf
- non_tuned_cells_with_rasters_all_sessions.pdf

From TRENDS:
- [effect_category]_archT_[subject]_tuning.pdf (6 PDFs)
- category_distribution_summary.png

From STATISTICS:
- laser_on_vs_off_metrics.csv
- statistical_results.csv
- laser_on_vs_off_comparison.pdf
- normalized_tuning_curves.png
- histogram distributions (2 PNGs)

From GAUSSIAN FITTING:
- gaussian_fit_parameters.csv
- gaussian_fit_quality_summary.csv
- gaussian_fits_example_cells.pdf
- gaussian_parameter_comparison.pdf

CONFIGURATION:
--------------
All scripts use config.py for standardized path management:
- get_reports_subdir() provides consistent output directories
- Eliminates hardcoded paths across scripts
- Ensures compatibility across different systems

NOTES:
------
- Scripts use jaratoolbox for spike analysis and cell database management
- Analysis windows differ between frequency (5-95ms) and AM (5-495ms) tuning
- Quality control filters cells by minimum firing rate thresholds (2.0 Hz)
- Classification uses tuning quality, selectivity, bandwidth, and CV metrics
- All statistical tests use non-parametric methods (Wilcoxon signed-rank)
- Gaussian fitting is optional and provides parametric analysis alternative

DEPENDENCIES:
-------------
- Python 3.x
- numpy, pandas, scipy, matplotlib
- jaratoolbox (spike analysis, cell databases)
- dataclasses (configuration management)

For questions or issues, contact: Hylen
Last updated: 2025

================================================================================
