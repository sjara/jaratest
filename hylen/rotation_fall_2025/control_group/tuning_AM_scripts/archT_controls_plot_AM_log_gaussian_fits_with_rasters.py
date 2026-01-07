"""
Log-Gaussian Fit AM Tuning Curves with Raster Plots

This script creates comprehensive PDFs showing Log-Gaussian fitted AM tuning curves
with their corresponding raster plots for detailed analysis.

Layout (Landscape, 3 cells per page):
- Top: Metrics boxes (R², baseline, amplitude, preferred rate, sigma)
- Middle: Log-Gaussian fit tuning curves (OFF vs ON)
- Bottom: Raster plots organized by AM rate

Features:
- Reads fitted Log-Gaussian parameters from CSV files
- Loads raw data for raster plotting
- 4 category-based PDFs (good fits, poor fits, failed fits, all tuned)
- Uses jaratoolbox for raster generation
- Adapted for AM rate tuning (not frequency tuning)

Author: Hylen
Date: 2025
"""

import os
import sys
from typing import Tuple, Dict, List, NamedTuple
from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec

from jaratoolbox import settings, celldatabase, ephyscore, behavioranalysis, extraplots

sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class SessionConfig:
    """Recording session configuration."""
    subject: str
    date: str
    depth: int


@dataclass(frozen=True)
class PlotConfig:
    """Configuration for visualization."""
    time_range: Tuple[float, float] = (-0.5, 1.0)
    response_window: Tuple[float, float] = (0.005, 0.495)  # AM uses longer window
    cells_per_page: int = 3  # 3 cells per page (landscape)
    fig_width: float = 17  # Landscape (full page width)
    fig_height: float = 13  # Increased height for better space utilization
    
    # Experimental group identification
    experiment_name: str = 'control (blocked laser) AM'

    @property
    def gaussian_fits_dir(self) -> str:
        result = str(get_reports_subdir('control_group/tuning_AM_gaussian_fits'))
        print(f"DEBUG PlotConfig.gaussian_fits_dir: {result}")
        return result

    @property
    def output_dir(self) -> str:
        result = str(get_reports_subdir('control_group/tuning_AM_gaussian_fits'))
        print(f"DEBUG PlotConfig.output_dir: {result}")
        return result
    
    @property
    def metrics_dir(self) -> str:
        result = str(get_reports_subdir('control_group/tuning_AM_analysis'))
        print(f"DEBUG PlotConfig.metrics_dir: {result}")
        return result


# All available sessions
SESSIONS = {
    0: SessionConfig('arch018', '2024-12-16', 3780),
    1: SessionConfig('arch018', '2024-12-16', 4500),
    2: SessionConfig('arch018', '2025-01-12', 3780),
    3: SessionConfig('arch018', '2025-01-12', 4500),
    4: SessionConfig('arch019', '2024-12-04', 3780),
    5: SessionConfig('arch019', '2024-12-04', 4500), #missing multisession_info.csv file, cannot be split
    6: SessionConfig('arch019', '2024-12-06', 3780),
    7: SessionConfig('arch019', '2024-12-06', 4500),
    8: SessionConfig('arch020', '2025-03-27', 2780),
    9: SessionConfig('arch020', '2025-03-27', 3500),
    10: SessionConfig('arch020', '2025-04-02', 2780),
    11: SessionConfig('arch020', '2025-04-02', 3500),
    12: SessionConfig('arch022', '2025-03-17', 2780),
    13: SessionConfig('arch022', '2025-03-17', 3500),
}


# =============================================================================
# DATA LOADING
# =============================================================================

class LogGaussianFitDataLoader:
    """Loads Log-Gaussian fit results and raw session data."""
    
    def __init__(self, config: PlotConfig):
        self.config = config
    
    def load_log_gaussian_fits(self, session_id: int, laser_condition: str) -> pd.DataFrame:
        """Load Log-Gaussian fit results from CSV."""
        suffix = laser_condition.lower()
        csv_path = os.path.join(
            self.config.gaussian_fits_dir,
            f'session_{session_id}_laser_{suffix}_log_gaussian_fits.csv'
        )
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Log-Gaussian fits not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        # Also load the original metrics CSV to get tuning curve data
        metrics_path = os.path.join(
            self.config.metrics_dir,
            f'session_{session_id}_laser_{suffix}_tuning_metrics.csv'
        )
        
        # DEBUG: Print the exact path being checked
        print(f"  DEBUG: Looking for metrics at: {metrics_path}")
        print(f"  DEBUG: File exists: {os.path.exists(metrics_path)}")
        
        if os.path.exists(metrics_path):
            metrics_df = pd.read_csv(metrics_path)
            # Merge tuning curve data into fits dataframe
            df = df.merge(
                metrics_df[['cell_idx', 'tuning_rates_am', 'tuning_responses']],
                on='cell_idx',
                how='left'
            )
            print(f"  Loaded tuning curve data from: {metrics_path}")
        else:
            print(f"  WARNING: Metrics file not found: {metrics_path}")
            print(f"  Observed data will not be plotted!")
        
        return df

    def _load_session_data(
        self,
        session: SessionConfig,
        celldbs: Dict[str, pd.DataFrame]
    ) -> dict:
        """Load session ephys data (adapted for AM tuning)."""
        celldb_full = celldbs[session.subject]
        celldb_subset = celldb_full[
            (celldb_full.date == session.date) &
            (celldb_full.pdepth == session.depth)
        ]
        
        ensemble = ephyscore.CellEnsemble(celldb_subset)
        ephys_data, bdata = ensemble.load('optoTuningAM')  # AM, not Freq!
        
        # Get spike data
        event_onset_times = ephys_data['events']['stimOn']
        
        # Find AM rate field dynamically (same as AM plotting script)
        possible_rate_fields = ['currentAMrate', 'AMrate', 'modRate', 'targetAMrate', 'currentFreq']
        rate_field = None
        
        for field in possible_rate_fields:
            if field in bdata:
                rate_field = field
                break
        
        if rate_field is None:
            raise KeyError(f"AM rate field not found. Tried: {possible_rate_fields}")
        
        # Store the field name for later use
        bdata._am_rate_field = rate_field
        
        n_trials = len(bdata[rate_field])
        
        if len(event_onset_times) == n_trials + 1:
            event_onset_times = event_onset_times[:n_trials]
        
        spike_times_all, trial_index_all, index_limits_all = ensemble.eventlocked_spiketimes(
            event_onset_times, self.config.time_range
        )
        
        return {
            'ephys_data': ephys_data,
            'bdata': bdata,
            'event_onset_times': event_onset_times,
            'spike_times_all': spike_times_all,
            'trial_index_all': trial_index_all,
            'index_limits_all': index_limits_all
        }


# =============================================================================
# PLOTTING MODULE
# =============================================================================

class LogGaussianAMPlotter:
    """Creates plots of Log-Gaussian fits with rasters for AM tuning."""
    
    def __init__(self, config: PlotConfig):
        self.config = config
    
    def plot_cell_3panel(
        self,
        gs: GridSpec,
        col_idx: int,
        fit_data_off: pd.Series,
        fit_data_on: pd.Series,
        session_data: dict,
        session_id: int
    ):
        """
        Plot one cell with 3-panel layout: metrics, Log-Gaussian fit, raster.
        
        Args:
            gs: GridSpec for page
            col_idx: Column index (0, 1, or 2)
            fit_data_off: Fit data for laser OFF
            fit_data_on: Fit data for laser ON
            session_data: Dict with spike data
            session_id: Session ID
        """
        cell_idx = int(fit_data_off['cell_idx'])
        
        # Create 3 subplots vertically
        ax_metrics = plt.subplot(gs[0, col_idx])
        ax_gaussian = plt.subplot(gs[1, col_idx])
        ax_raster = plt.subplot(gs[2, col_idx])
        
        # Plot metrics box
        self._plot_metrics_box(ax_metrics, fit_data_off, fit_data_on, cell_idx, session_id)
        
        # Plot Log-Gaussian fits
        self._plot_log_gaussian_fits(ax_gaussian, fit_data_off, fit_data_on)
        
        # Plot raster
        self._plot_raster(ax_raster, cell_idx, session_data)
    
    def _plot_metrics_box(
        self,
        ax: plt.Axes,
        fit_off: pd.Series,
        fit_on: pd.Series,
        cell_idx: int,
        session_id: int
    ):
        """Plot metrics text boxes."""
        ax.axis('off')
        
        # Title positioned above the metrics boxes
        session = SESSIONS[session_id]
        title = f"Cell {cell_idx} | Session {session_id} | {session.subject} {session.date} {session.depth}µm"
        ax.text(0.5, 0.95, title, transform=ax.transAxes,
               fontsize=10, fontweight='bold', ha='center', va='top')
        
        # Create 3 text boxes side by side
        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='wheat', 
                         alpha=0.85, edgecolor='black', linewidth=0.8)
        
        # Calculate log10 of preferred rates for display
        log_pref_off = np.log10(fit_off['preferred_rate'] + 1)
        log_pref_on = np.log10(fit_on['preferred_rate'] + 1)
        
        # Left: Laser OFF
        text_off = (
            f"LASER OFF\n"
            f"R²: {fit_off['r_squared']:.3f}\n"
            f"Baseline: {fit_off['baseline']:.1f} sp/s\n"
            f"Amplitude: {fit_off['amplitude']:.1f} sp/s\n"
            f"Best Rate: {fit_off['preferred_rate']:.1f}Hz ({log_pref_off:.2f})\n"
            f"Sigma: {fit_off['sigma']:.2f}log₁₀"
        )
        
        # Middle: Laser ON
        text_on = (
            f"LASER ON\n"
            f"R²: {fit_on['r_squared']:.3f}\n"
            f"Baseline: {fit_on['baseline']:.1f} sp/s\n"
            f"Amplitude: {fit_on['amplitude']:.1f} sp/s\n"
            f"Best Rate: {fit_on['preferred_rate']:.1f}Hz ({log_pref_on:.2f})\n"
            f"Sigma: {fit_on['sigma']:.2f}log₁₀"
        )
        
        # Right: Effect (difference)
        delta_log_pref = log_pref_on - log_pref_off
        text_effect = (
            f"EFFECT\n"
            f"ΔR²: {fit_on['r_squared'] - fit_off['r_squared']:+.3f}\n"
            f"ΔBaseline: {fit_on['baseline'] - fit_off['baseline']:+.1f} sp/s\n"
            f"ΔAmplitude: {fit_on['amplitude'] - fit_off['amplitude']:+.1f} sp/s\n"
            f"ΔBest Rate: {fit_on['preferred_rate'] - fit_off['preferred_rate']:+.1f}Hz ({delta_log_pref:+.2f})\n"
            f"ΔSigma: {fit_on['sigma'] - fit_off['sigma']:+.2f}log₁₀"
        )
        
        # Position text boxes (moved down slightly to make room for title)
        ax.text(0.02, 0.45, text_off, transform=ax.transAxes,
               fontsize=9, verticalalignment='center', family='monospace',
               bbox=bbox_props)
        
        ax.text(0.35, 0.45, text_on, transform=ax.transAxes,
               fontsize=9, verticalalignment='center', family='monospace',
               bbox=bbox_props)
        
        ax.text(0.68, 0.45, text_effect, transform=ax.transAxes,
               fontsize=9, verticalalignment='center', family='monospace',
               bbox=bbox_props)
    
    def _plot_log_gaussian_fits(self, ax: plt.Axes, fit_off: pd.Series, fit_on: pd.Series):
        """Plot Log-Gaussian fit tuning curves (OFF vs ON) with REAL observed data points."""
        # Parse REAL observed tuning curves from CSV strings
        tuning_rates_str = str(fit_off.get('tuning_rates_am', ''))
        tuning_responses_off_str = str(fit_off.get('tuning_responses', ''))
        tuning_responses_on_str = str(fit_on.get('tuning_responses', ''))
        
        # Parse AM rates
        if tuning_rates_str and tuning_rates_str != 'nan':
            rates_observed = np.array([float(r) for r in tuning_rates_str.split(',') if r.strip()])
        else:
            rates_observed = np.array([4, 8, 16, 32, 64, 128])  # Typical AM rates fallback
        
        # Parse observed responses OFF
        if tuning_responses_off_str and tuning_responses_off_str != 'nan':
            responses_off_observed = []
            for r in tuning_responses_off_str.split(','):
                if r.strip().lower() == 'nan' or r.strip() == '':
                    responses_off_observed.append(np.nan)
                else:
                    responses_off_observed.append(float(r))
            responses_off_observed = np.array(responses_off_observed)
        else:
            responses_off_observed = np.full(len(rates_observed), np.nan)
        
        # Parse observed responses ON
        if tuning_responses_on_str and tuning_responses_on_str != 'nan':
            responses_on_observed = []
            for r in tuning_responses_on_str.split(','):
                if r.strip().lower() == 'nan' or r.strip() == '':
                    responses_on_observed.append(np.nan)
                else:
                    responses_on_observed.append(float(r))
            responses_on_observed = np.array(responses_on_observed)
        else:
            responses_on_observed = np.full(len(rates_observed), np.nan)
        
        # Create smooth AM rate range for fitted curves
        rate_min = max(2, rates_observed.min()) if len(rates_observed) > 0 else 2
        rate_max = min(256, rates_observed.max()) if len(rates_observed) > 0 else 128
        rates_smooth = np.logspace(np.log10(rate_min), np.log10(rate_max), 200)
        
        # Log-Gaussian function
        def log_gaussian(rates_arr, baseline, amplitude, preferred_rate, sigma):
            log_rates = np.log10(rates_arr + 1)
            log_preferred = np.log10(preferred_rate + 1)
            return baseline + amplitude * np.exp(-0.5 * ((log_rates - log_preferred) / sigma)**2)
        
        # Calculate smooth Log-Gaussian curves (fitted functions)
        responses_off_smooth = log_gaussian(rates_smooth, fit_off['baseline'], fit_off['amplitude'],
                                           fit_off['preferred_rate'], fit_off['sigma'])
        
        responses_on_smooth = log_gaussian(rates_smooth, fit_on['baseline'], fit_on['amplitude'],
                                          fit_on['preferred_rate'], fit_on['sigma'])
        
        # Plot smooth Log-Gaussian curves (fitted functions) - solid lines
        ax.plot(rates_smooth, responses_off_smooth, '-', color='blue', linewidth=3, 
               label='Fitted OFF', zorder=2, alpha=0.7)
        
        ax.plot(rates_smooth, responses_on_smooth, '-', color='red', linewidth=3,
               label='Fitted ON', zorder=2, alpha=0.7)
        
        # Plot REAL observed data points - dotted lines
        valid_off = ~np.isnan(responses_off_observed)
        if np.any(valid_off):
            ax.plot(rates_observed[valid_off], responses_off_observed[valid_off], ':', 
                   color='blue', linewidth=3.5, marker='o', markersize=8,
                   markerfacecolor='blue', markeredgecolor='black', markeredgewidth=1,
                   label='Observed OFF', zorder=4, alpha=1.0)
        
        valid_on = ~np.isnan(responses_on_observed)
        if np.any(valid_on):
            ax.plot(rates_observed[valid_on], responses_on_observed[valid_on], ':', 
                   color='red', linewidth=3.5, marker='s', markersize=8,
                   markerfacecolor='red', markeredgecolor='black', markeredgewidth=1,
                   label='Observed ON', zorder=4, alpha=1.0)
        
        # Mark preferred rates with stars (at peak of smooth curve)
        pref_off_idx = np.argmax(responses_off_smooth)
        pref_on_idx = np.argmax(responses_on_smooth)
        
        ax.plot(rates_smooth[pref_off_idx], responses_off_smooth[pref_off_idx], '*', 
               markersize=20, color='blue', markeredgecolor='black', 
               markeredgewidth=2, zorder=10, label='Fitted Pref Rate OFF')
        
        ax.plot(rates_smooth[pref_on_idx], responses_on_smooth[pref_on_idx], '*',
               markersize=20, color='red', markeredgecolor='black',
               markeredgewidth=2, zorder=10, label='Fitted Pref Rate ON')
        
        # Plot EMPIRICAL preferred rate markers (crosses) for comparison
        if len(rates_observed) > 0:
            # Find empirical peaks
            if np.any(valid_off):
                emp_peak_idx_off = np.argmax(responses_off_observed[valid_off])
                emp_peak_rate_off = responses_off_observed[valid_off][emp_peak_idx_off]
                emp_rate_off = rates_observed[valid_off][emp_peak_idx_off]
                ax.plot(emp_rate_off, emp_peak_rate_off, 'x', 
                       markersize=15, color='darkblue', markeredgewidth=3, 
                       zorder=11, label='Empirical Best OFF')
            
            if np.any(valid_on):
                emp_peak_idx_on = np.argmax(responses_on_observed[valid_on])
                emp_peak_rate_on = responses_on_observed[valid_on][emp_peak_idx_on]
                emp_rate_on = rates_observed[valid_on][emp_peak_idx_on]
                ax.plot(emp_rate_on, emp_peak_rate_on, 'x',
                       markersize=15, color='darkred', markeredgewidth=3,
                       zorder=11, label='Empirical Best ON')
        
        # Formatting
        ax.set_ylabel('Firing Rate (spikes/s)', fontsize=12, fontweight='bold')
        ax.set_xlabel('AM Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_xscale('log')  # Log scale for AM rates
        
        # Set x-axis ticks to show actual AM rates tested
        if len(rates_observed) > 0:
            ax.set_xticks(rates_observed)
            ax.set_xticklabels([f'{int(r)}' for r in rates_observed], fontsize=10)
        else:
            # Fallback to typical AM rates
            typical_rates = [4, 8, 16, 32, 64, 128]
            ax.set_xticks(typical_rates)
            ax.set_xticklabels([f'{int(r)}' for r in typical_rates], fontsize=10)
        
        ax.grid(True, alpha=0.2, which='both')
        
        # Legend positioned above the plot, horizontal layout
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), 
                 fontsize=8, ncol=4, frameon=True, framealpha=0.9,
                 edgecolor='black', fancybox=True)
        
        ax.tick_params(axis='both', which='major', labelsize=10)
    
    def _plot_raster(self, ax: plt.Axes, cell_idx: int, session_data: dict):
        """Plot raster sorted by AM rate with laser OFF/ON comparison (IDENTICAL to AM raster script)."""
        spike_times = session_data['spike_times_all'][cell_idx]
        trial_index = session_data['trial_index_all'][cell_idx]
        index_limits = session_data['index_limits_all'][cell_idx]
        bdata = session_data['bdata']
        
        # Get AM rates and laser trials
        rate_field = getattr(bdata, '_am_rate_field', 'currentFreq')
        am_rates = np.asarray(bdata[rate_field]).flatten()
        unique_rates = np.unique(am_rates)
        
        if 'laserTrial' in bdata:
            laser_trials = np.asarray(bdata['laserTrial']).flatten().astype(bool)
        else:
            laser_trials = np.zeros(len(am_rates), dtype=bool)
        
        # Build trial organization
        trials_each_rate = behavioranalysis.find_trials_each_type(am_rates, unique_rates)
        
        off_trials = np.flatnonzero(laser_trials == 0)
        on_trials = np.flatnonzero(laser_trials == 1)
        
        # Build trialsEachCond: [rate1_OFF, rate2_OFF, ..., rate1_ON, rate2_ON, ...]
        trials_each_cond = []
        
        # OFF trials for each AM rate
        for rate_idx in range(len(unique_rates)):
            rate_trials = trials_each_rate[:, rate_idx]
            off_mask = rate_trials.copy()
            off_mask[on_trials] = False
            trials_each_cond.append(off_mask)
        
        # ON trials for each AM rate
        for rate_idx in range(len(unique_rates)):
            rate_trials = trials_each_rate[:, rate_idx]
            on_mask = rate_trials.copy()
            on_mask[off_trials] = False
            trials_each_cond.append(on_mask)
        
        trials_each_cond = np.column_stack(trials_each_cond)
        
        # Colors (alternating for AM rates)
        n_rates = len(unique_rates)
        color_each_cond = (['0.5', '0.75'] * int(np.ceil(n_rates / 2.0)))[:n_rates]
        color_each_cond = color_each_cond + color_each_cond  # Duplicate for ON
        
        # AM rate labels
        labels = [f'{int(r)}' for r in unique_rates]
        labels = labels + labels  # Duplicate for ON
        
        # Use jaratoolbox raster plot
        pRaster, hcond, zline = extraplots.raster_plot(
            spike_times, index_limits, self.config.time_range,
            trialsEachCond=trials_each_cond,
            colorEachCond=color_each_cond,
            labels=labels
        )
        plt.setp(pRaster, ms=2)  # Increased marker size
        
        # Hide every other label
        for i, label in enumerate(ax.get_yticklabels()):
            if i % 2 == 1:
                label.set_visible(False)
        
        # Add laser boundary line
        cumsum_trials = np.cumsum([trials_each_cond[:, i].sum() for i in range(n_rates)])
        laser_boundary = cumsum_trials[-1] - 0.5
        ax.axhline(laser_boundary, color='red', linewidth=3, linestyle='--', alpha=0.8, zorder=10)
        
        # Add laser labels
        total_trials = trials_each_cond.sum()
        yticks_minor = [laser_boundary/2, laser_boundary + (total_trials - laser_boundary)/2]
        ax.set_yticks(yticks_minor, ['laser OFF', 'laser ON'], minor=True)
        ax.tick_params(axis='y', which='minor', left=False, right=True,
                      labelleft=False, labelright=True, labelsize=10, pad=2)
        
        # Format axes
        ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax.set_ylabel('AM Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_xlim(self.config.time_range)
        ax.tick_params(axis='both', which='major', labelsize=10)
    


# =============================================================================
# PDF GENERATOR
# =============================================================================

class CategoryPDFGenerator:
    """Generates category-based PDFs."""
    
    def __init__(self, config: PlotConfig, loader: LogGaussianFitDataLoader, plotter: LogGaussianAMPlotter):
        self.config = config
        self.loader = loader
        self.plotter = plotter
    
    @staticmethod
    def load_celldbs(sessions: Dict[int, SessionConfig]) -> Dict[str, pd.DataFrame]:
        """Load cell databases for all unique subjects."""
        subjects = list(set(session.subject for session in sessions.values()))
        celldbs = {}
        
        for subject in subjects:
            inforec_file = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
            celldbs[subject] = celldatabase.generate_cell_database(inforec_file, ignoreMissing=True)
        
        return celldbs
    
    def _load_session_data(
        self,
        session: SessionConfig,
        celldbs: Dict[str, pd.DataFrame]
    ) -> dict:
        """Load session ephys data."""
        return self.loader._load_session_data(session, celldbs)
    
    def create_category_pdfs(self):
        """Create 4 category PDFs across all sessions."""
        print("\n" + "="*70)
        print("CREATING LOG-GAUSSIAN AM FIT + RASTER PDFs")
        print("="*70)
        
        # Load cell databases once for all sessions
        print("\nLoading cell databases...")
        celldbs = self.load_celldbs(SESSIONS)
        
        # Collect all cells by category
        good_fits = []
        poor_fits = []
        failed_fits = []
        empirically_tuned = []
        
        # Load all sessions
        for session_id in sorted(SESSIONS.keys()):
            session = SESSIONS[session_id]
            
            try:
                print(f"\nLoading session {session_id}: {session.subject} {session.date}")
                
                # Load Log-Gaussian fits (now includes tuning curves from individual metrics)
                fits_off = self.loader.load_log_gaussian_fits(session_id, 'off')
                fits_on = self.loader.load_log_gaussian_fits(session_id, 'on')
                
                # Load raw data (for rasters)
                try:
                    session_data = self._load_session_data(session, celldbs)
                except KeyError as e:
                    print(f"  SKIPPING: Cannot load raw data for rasters - {e}")
                    continue
                
                # Match cells
                cells_off = {row['cell_idx']: row for _, row in fits_off.iterrows()}
                cells_on = {row['cell_idx']: row for _, row in fits_on.iterrows()}
                common_cells = sorted(set(cells_off.keys()) & set(cells_on.keys()))
                
                print(f"  Found {len(common_cells)} cells with both OFF and ON fits")
                
                for cell_idx in common_cells:
                    fit_off = cells_off[cell_idx]
                    fit_on = cells_on[cell_idx]
                    
                    cell_data = (session_id, session, fit_off, fit_on, session_data)
                    
                    # Categorize by fit quality
                    if fit_off['fit_quality'] == 'good' and fit_on['fit_quality'] == 'good':
                        good_fits.append(cell_data)
                    elif fit_off['fit_quality'] == 'poor' and fit_on['fit_quality'] == 'poor':
                        poor_fits.append(cell_data)
                    elif fit_off['fit_quality'] == 'failed' or fit_on['fit_quality'] == 'failed':
                        failed_fits.append(cell_data)
                    
                    # Check if empirically tuned from loaded fit data
                    if 'empirical_is_tuned' in fit_off:
                        if fit_off['empirical_is_tuned']:
                            empirically_tuned.append(cell_data)
                
            except FileNotFoundError as e:
                print(f"  SKIPPING: {e}")
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
        
        # Create PDFs
        self._create_pdf(good_fits, 'good_fits', 'Good Log-Gaussian Fits')
        self._create_pdf(poor_fits, 'poor_fits', 'Poor Log-Gaussian Fits')
        self._create_pdf(failed_fits, 'failed_fits', 'Failed Log-Gaussian Fits')
        self._create_pdf(empirically_tuned, 'empirically_tuned', 'Empirically Tuned Cells')
    
    def _create_pdf(self, cell_data_list: List, filename_suffix: str, title: str):
        """Create a single PDF for a category."""
        if len(cell_data_list) == 0:
            print(f"\n  No cells for: {title}")
            return
        
        filename = f'log_gaussian_am_fits_with_rasters_{filename_suffix}.pdf'
        pdf_path = os.path.join(self.config.output_dir, filename)
        
        print(f"\n  Creating {title} PDF with {len(cell_data_list)} cells...")
        
        with PdfPages(pdf_path) as pdf:
            n_cells_per_page = self.config.cells_per_page
            n_pages = int(np.ceil(len(cell_data_list) / n_cells_per_page))
            
            for page_idx in range(n_pages):
                # Create figure with GridSpec (3 rows x 3 cols)
                fig = plt.figure(figsize=(self.config.fig_width, self.config.fig_height))
                gs = GridSpec(3, 3, figure=fig, height_ratios=[0.6, 1.8, 1.6],
                             hspace=0.15, wspace=0.25,
                             left=0.05, right=0.98, top=0.94, bottom=0.05)
                
                start_idx = page_idx * n_cells_per_page
                end_idx = min(start_idx + n_cells_per_page, len(cell_data_list))
                
                for col_idx, cell_idx_in_list in enumerate(range(start_idx, end_idx)):
                    session_id, session, fit_off, fit_on, session_data = cell_data_list[cell_idx_in_list]
                    
                    self.plotter.plot_cell_3panel(
                        gs, col_idx, fit_off, fit_on, session_data, session_id
                    )
                
                # Page title
                fig.suptitle(
                    f'{self.config.experiment_name}\n{title} | Page {page_idx + 1}/{n_pages} | Total: {len(cell_data_list)} cells',
                    fontsize=16, fontweight='bold', y=0.98
                )
                
                pdf.savefig(fig, dpi=150)
                plt.close(fig)
        
        print(f"  Saved: {pdf_path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""
    print("="*70)
    print("LOG-GAUSSIAN AM FIT + RASTER VISUALIZATION")
    print("="*70)
    
    config = PlotConfig()
    os.makedirs(config.output_dir, exist_ok=True)
    
    loader = LogGaussianFitDataLoader(config)
    plotter = LogGaussianAMPlotter(config)
    generator = CategoryPDFGenerator(config, loader, plotter)
    
    generator.create_category_pdfs()
    
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)


if __name__ == '__main__':
    main()
