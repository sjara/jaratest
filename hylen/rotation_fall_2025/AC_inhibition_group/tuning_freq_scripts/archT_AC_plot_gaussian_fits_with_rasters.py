"""
Gaussian Fit Tuning Curves with Raster Plots

This script creates comprehensive PDFs showing Gaussian fitted tuning curves
with their corresponding raster plots for detailed analysis.

Layout (Landscape, 3 cells per page):
- Top: Metrics boxes (R², baseline, amplitude, mean, SD)
- Middle: Gaussian fit tuning curves (OFF vs ON)
- Bottom: Raster plots organized by frequency

Features:
- Reads fitted Gaussian parameters from CSV files
- Loads raw data for raster plotting
- 4 category-based PDFs (good fits, poor fits, failed fits, all tuned)
- Uses jaratoolbox for raster generation

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

# Add hylen directory to path
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
    response_window: Tuple[float, float] = (0.005, 0.095)
    cells_per_page: int = 3  # 3 cells per page (landscape)
    fig_width: float = 17  # Landscape (full page width)
    fig_height: float = 13  # Increased height for better space utilization
    
    # Experimental group identification
    experiment_name: str = 'AC - pStr inhibition with pure tones'
    
    # Use centralized config for directories
    @property
    def gaussian_fits_dir(self) -> str:
        """Get Gaussian fits directory from config."""
        return str(get_reports_subdir('tuning_freq_gaussian_fits'))
    
    @property
    def output_dir(self) -> str:
        """Get output directory from config."""
        return str(get_reports_subdir('tuning_freq_gaussian_fits'))
    
    @property
    def metrics_dir(self) -> str:
        """Get metrics directory from config."""
        return str(get_reports_subdir('tuning_freq_analysis'))


# All available sessions
SESSIONS = {
    0: SessionConfig('arch019', '2024-11-19', 3780),
    1: SessionConfig('arch019', '2024-11-19', 4500),
    2: SessionConfig('arch019', '2024-11-20', 3780),
    3: SessionConfig('arch019', '2024-11-20', 4500),
    4: SessionConfig('arch019', '2024-11-20', 3781),
    5: SessionConfig('arch019', '2024-11-20', 4501),
    6: SessionConfig('arch020', '2025-03-25', 3500),
    7: SessionConfig('arch020', '2025-03-25', 2780),
    8: SessionConfig('arch020', '2025-04-01', 2780),
    9: SessionConfig('arch020', '2025-04-01', 3500),
    10: SessionConfig('arch022', '2025-03-13', 2780),
    11: SessionConfig('arch022', '2025-03-13', 3500),
    12: SessionConfig('arch018', '2024-12-17', 3780),
    13: SessionConfig('arch018', '2024-12-17', 4500),
}


# =============================================================================
# DATA LOADING
# =============================================================================

class GaussianFitDataLoader:
    """Loads Gaussian fit results and raw session data."""
    
    def __init__(self, config: PlotConfig):
        self.config = config
    
    def load_gaussian_fits(self, session_id: int, laser_condition: str) -> pd.DataFrame:
        """Load Gaussian fit results from CSV."""
        suffix = laser_condition.lower()
        csv_path = os.path.join(
            self.config.gaussian_fits_dir,
            f'session_{session_id}_laser_{suffix}_gaussian_fits.csv'
        )
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Gaussian fits not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        # Also load the original metrics CSV to get tuning curve data
        metrics_path = os.path.join(
            self.config.metrics_dir,
            f'session_{session_id}_laser_{suffix}_tuning_metrics.csv'
        )
        
        if os.path.exists(metrics_path):
            metrics_df = pd.read_csv(metrics_path)
            # Merge tuning curve data into fits dataframe
            df = df.merge(
                metrics_df[['cell_idx', 'tuning_freqs', 'tuning_rates']],
                on='cell_idx',
                how='left'
            )
        
        return df
    
    def _load_session_data(
        self,
        session: SessionConfig,
        celldbs: Dict[str, pd.DataFrame]
    ) -> dict:
        """Load session ephys data (EXACT copy from tuning_with_rasters)."""
        celldb_full = celldbs[session.subject]
        celldb_subset = celldb_full[
            (celldb_full.date == session.date) &
            (celldb_full.pdepth == session.depth)
        ]
        
        ensemble = ephyscore.CellEnsemble(celldb_subset)
        ephys_data, bdata = ensemble.load('optoTuningFreq')
        
        # Get spike data
        event_onset_times = ephys_data['events']['stimOn']
        n_trials = len(bdata['currentFreq'])
        
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

class GaussianFitPlotter:
    """Creates plots of Gaussian fits with rasters."""
    
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
        Plot one cell with 3-panel layout: metrics, Gaussian fit, raster.
        
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
        
        # Plot Gaussian fits
        self._plot_gaussian_fits(ax_gaussian, fit_data_off, fit_data_on)
        
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
        
        # Left: Laser OFF
        text_off = (
            f"LASER OFF\n"
            f"R²: {fit_off['r_squared']:.3f}\n"
            f"Baseline: {fit_off['baseline']:.1f}Hz\n"
            f"Amplitude: {fit_off['amplitude']:.1f}Hz\n"
            f"BF Shift: {fit_off['mean_octave']:.2f}oct\n"
            f"SD(σ): {fit_off['sigma']:.2f}oct"
        )
        
        # Middle: Laser ON
        text_on = (
            f"LASER ON\n"
            f"R²: {fit_on['r_squared']:.3f}\n"
            f"Baseline: {fit_on['baseline']:.1f}Hz\n"
            f"Amplitude: {fit_on['amplitude']:.1f}Hz\n"
            f"BF Shift: {fit_on['mean_octave']:.2f}oct\n"
            f"SD(σ): {fit_on['sigma']:.2f}oct"
        )
        
        # Right: Effect (difference)
        text_effect = (
            f"EFFECT\n"
            f"ΔR²: {fit_on['r_squared'] - fit_off['r_squared']:+.3f}\n"
            f"ΔBaseline: {fit_on['baseline'] - fit_off['baseline']:+.1f}Hz\n"
            f"ΔAmplitude: {fit_on['amplitude'] - fit_off['amplitude']:+.1f}Hz\n"
            f"ΔBF Shift: {fit_on['mean_octave'] - fit_off['mean_octave']:+.2f}oct\n"
            f"ΔSD: {fit_on['sigma'] - fit_off['sigma']:+.2f}oct"
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
    
    def _plot_gaussian_fits(self, ax: plt.Axes, fit_off: pd.Series, fit_on: pd.Series):
        """Plot Gaussian fit tuning curves (OFF vs ON) with REAL observed data points."""
        bf = fit_off['empirical_best_freq']
        
        # Parse REAL observed tuning curves from CSV strings
        tuning_freqs_str = str(fit_off.get('tuning_freqs', ''))
        tuning_rates_off_str = str(fit_off.get('tuning_rates', ''))
        tuning_rates_on_str = str(fit_on.get('tuning_rates', ''))
        
        # Parse frequencies
        if tuning_freqs_str and tuning_freqs_str != 'nan':
            freqs_observed = np.array([float(f) for f in tuning_freqs_str.split(',') if f.strip()])
        else:
            freqs_observed = bf * 2 ** np.linspace(-3, 3, 16)  # Fallback
        
        # Parse observed rates OFF
        if tuning_rates_off_str and tuning_rates_off_str != 'nan':
            rates_off_observed = []
            for r in tuning_rates_off_str.split(','):
                if r.strip().lower() == 'nan' or r.strip() == '':
                    rates_off_observed.append(np.nan)
                else:
                    rates_off_observed.append(float(r))
            rates_off_observed = np.array(rates_off_observed)
        else:
            rates_off_observed = np.full(len(freqs_observed), np.nan)
        
        # Parse observed rates ON
        if tuning_rates_on_str and tuning_rates_on_str != 'nan':
            rates_on_observed = []
            for r in tuning_rates_on_str.split(','):
                if r.strip().lower() == 'nan' or r.strip() == '':
                    rates_on_observed.append(np.nan)
                else:
                    rates_on_observed.append(float(r))
            rates_on_observed = np.array(rates_on_observed)
        else:
            rates_on_observed = np.full(len(freqs_observed), np.nan)
        
        # Use 200 points for smooth Gaussian curve
        freqs_smooth = bf * 2 ** np.linspace(-3, 3, 200)
        
        # Gaussian function
        def gaussian(f, baseline, amplitude, mean_oct, sigma, bf_ref):
            octaves = np.log2(f / bf_ref)
            return baseline + amplitude * np.exp(-0.5 * ((octaves - mean_oct) / sigma)**2)
        
        # Calculate smooth Gaussian curves (fitted functions)
        rates_off_smooth = gaussian(freqs_smooth, fit_off['baseline'], fit_off['amplitude'],
                                   fit_off['mean_octave'], fit_off['sigma'], bf)
        
        rates_on_smooth = gaussian(freqs_smooth, fit_on['baseline'], fit_on['amplitude'],
                                  fit_on['mean_octave'], fit_on['sigma'], bf)
        
        # Create x-axis positions
        x_pos_smooth = np.linspace(0, 15, 200)  # Smooth fitted curve
        
        # Map observed frequencies to x positions
        if len(freqs_observed) > 0:
            # Assuming frequencies span -3 to +3 octaves from bf
            octaves_observed = np.log2(freqs_observed / bf)
            # Map to 0-15 range
            x_pos_observed = (octaves_observed + 3) * (15 / 6)
        else:
            x_pos_observed = np.linspace(0, 15, 16)
        
        # Plot smooth Gaussian curves (fitted functions) - solid lines
        ax.plot(x_pos_smooth, rates_off_smooth, '-', color='blue', linewidth=3, 
               label='Fitted OFF', zorder=2, alpha=0.7)
        
        ax.plot(x_pos_smooth, rates_on_smooth, '-', color='red', linewidth=3,
               label='Fitted ON', zorder=2, alpha=0.7)
        
        # Plot REAL observed data points - dotted lines (like control group script)
        valid_off = ~np.isnan(rates_off_observed)
        if np.any(valid_off):
            ax.plot(x_pos_observed[valid_off], rates_off_observed[valid_off], ':', 
                   color='blue', linewidth=3.5, marker='o', markersize=8,
                   markerfacecolor='blue', markeredgecolor='black', markeredgewidth=1,
                   label='Observed OFF', zorder=4, alpha=1.0)
        
        valid_on = ~np.isnan(rates_on_observed)
        if np.any(valid_on):
            ax.plot(x_pos_observed[valid_on], rates_on_observed[valid_on], ':', 
                   color='red', linewidth=3.5, marker='s', markersize=8,
                   markerfacecolor='red', markeredgecolor='black', markeredgewidth=1,
                   label='Observed ON', zorder=4, alpha=1.0)
        
        # Mark best frequencies with stars - place at ACTUAL peak of smooth curve
        # Don't rely on best_freq_fitted_hz calculation, just find max of the smooth curve
        bf_off_idx = np.argmax(rates_off_smooth)
        bf_on_idx = np.argmax(rates_on_smooth)
        
        # Also get empirical best frequencies for comparison
        bf_empirical_off = fit_off['empirical_best_freq']
        bf_empirical_on = fit_on.get('empirical_best_freq', bf_empirical_off)
        
        # Find positions of EMPIRICAL best frequencies (for reference)
        if len(freqs_observed) > 0:
            emp_off_x = (np.log2(bf_empirical_off / bf) + 3) * (15 / 6)
            emp_on_x = (np.log2(bf_empirical_on / bf) + 3) * (15 / 6)
        
        # Plot FITTED best frequency stars (on the Gaussian curve)
        ax.plot(x_pos_smooth[bf_off_idx], rates_off_smooth[bf_off_idx], '*', 
               markersize=20, color='blue', markeredgecolor='black', 
               markeredgewidth=2, zorder=10, label='Fitted BF OFF')
        
        ax.plot(x_pos_smooth[bf_on_idx], rates_on_smooth[bf_on_idx], '*',
               markersize=20, color='red', markeredgecolor='black',
               markeredgewidth=2, zorder=10, label='Fitted BF ON')
        
        # Plot EMPIRICAL best frequency markers (crosses) for comparison
        if len(freqs_observed) > 0:
            # Find empirical peak rates
            valid_off = ~np.isnan(rates_off_observed)
            valid_on = ~np.isnan(rates_on_observed)
            
            if np.any(valid_off):
                emp_peak_idx_off = np.argmax(rates_off_observed[valid_off])
                emp_peak_rate_off = rates_off_observed[valid_off][emp_peak_idx_off]
                ax.plot(emp_off_x, emp_peak_rate_off, 'x', 
                       markersize=15, color='darkblue', markeredgewidth=3, 
                       zorder=11, label='Empirical BF OFF')
            
            if np.any(valid_on):
                emp_peak_idx_on = np.argmax(rates_on_observed[valid_on])
                emp_peak_rate_on = rates_on_observed[valid_on][emp_peak_idx_on]
                ax.plot(emp_on_x, emp_peak_rate_on, 'x',
                       markersize=15, color='darkred', markeredgewidth=3,
                       zorder=11, label='Empirical BF ON')
        
        # Create tick positions and labels (use 16 evenly spaced ticks)
        freqs_ticks = bf * 2 ** np.linspace(-3, 3, 16)
        freqs_khz_ticks = freqs_ticks / 1000.0
        x_pos_ticks = np.linspace(0, 15, 16)
        
        # Formatting
        ax.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_xticks(x_pos_ticks)
        ax.set_xticklabels([f'{f:.1f}' for f in freqs_khz_ticks], 
                          rotation=45, ha='right', fontsize=9)
        ax.set_xlim([-0.5, 15.5])
        ax.grid(True, alpha=0.2, axis='y')
        
        # Legend positioned above the plot, horizontal layout
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), 
                 fontsize=8, ncol=4, frameon=True, framealpha=0.9,
                 edgecolor='black', fancybox=True)
        
        ax.tick_params(axis='both', which='major', labelsize=10)
    
    def _plot_raster(self, ax: plt.Axes, cell_idx: int, session_data: dict):
        """Plot raster sorted by frequency with laser OFF/ON comparison (EXACT copy from tuning_with_rasters)."""
        spike_times = session_data['spike_times_all'][cell_idx]
        trial_index = session_data['trial_index_all'][cell_idx]
        index_limits = session_data['index_limits_all'][cell_idx]
        bdata = session_data['bdata']
        
        # Get frequencies and laser trials
        frequencies = np.asarray(bdata['currentFreq']).flatten()
        unique_freqs = np.unique(frequencies)
        
        if 'laserTrial' in bdata:
            laser_trials = np.asarray(bdata['laserTrial']).flatten().astype(bool)
        else:
            laser_trials = np.zeros(len(frequencies), dtype=bool)
        
        # Build trial organization
        trials_each_freq = behavioranalysis.find_trials_each_type(frequencies, unique_freqs)
        
        off_trials = np.flatnonzero(laser_trials == 0)
        on_trials = np.flatnonzero(laser_trials == 1)
        
        # Build trialsEachCond: [freq1_OFF, freq2_OFF, ..., freq1_ON, freq2_ON, ...]
        trials_each_cond = []
        
        # OFF trials for each frequency
        for freq_idx in range(len(unique_freqs)):
            freq_trials = trials_each_freq[:, freq_idx]
            off_mask = freq_trials.copy()
            off_mask[on_trials] = False
            trials_each_cond.append(off_mask)
        
        # ON trials for each frequency
        for freq_idx in range(len(unique_freqs)):
            freq_trials = trials_each_freq[:, freq_idx]
            on_mask = freq_trials.copy()
            on_mask[off_trials] = False
            trials_each_cond.append(on_mask)
        
        trials_each_cond = np.column_stack(trials_each_cond)
        
        # Colors (alternating for frequencies)
        n_freqs = len(unique_freqs)
        color_each_cond = (['0.5', '0.75'] * int(np.ceil(n_freqs / 2.0)))[:n_freqs]
        color_each_cond = color_each_cond + color_each_cond  # Duplicate for ON
        
        # Frequency labels
        freqs_khz = np.round(unique_freqs / 1000, 2)
        labels = [f'{fk}' for fk in freqs_khz]
        labels = labels + labels  # Duplicate for ON
        
        # Use jaratoolbox raster plot
        pRaster, hcond, zline = extraplots.raster_plot(
            spike_times, index_limits, self.config.time_range,
            trialsEachCond=trials_each_cond,
            colorEachCond=color_each_cond,
            labels=labels
        )
        plt.setp(pRaster, ms=2)  # Increased marker size
        
        # Add analysis window indicator (gray filled box with 50% opacity)
        ax.axvspan(self.config.response_window[0], self.config.response_window[1],
                  ymin=0, ymax=1, color='gray', alpha=0.5, zorder=0)
        
        # Hide every other label
        for i, label in enumerate(ax.get_yticklabels()):
            if i % 2 == 1:
                label.set_visible(False)
        
        # Add laser boundary line
        cumsum_trials = np.cumsum([trials_each_cond[:, i].sum() for i in range(n_freqs)])
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
        ax.set_ylabel('Frequency (kHz)', fontsize=12, fontweight='bold')
        ax.set_xlim(self.config.time_range)
        ax.tick_params(axis='both', which='major', labelsize=10)


# =============================================================================
# PDF GENERATOR
# =============================================================================

class CategoryPDFGenerator:
    """Generates category-based PDFs."""
    
    def __init__(self, config: PlotConfig, loader: GaussianFitDataLoader, plotter: GaussianFitPlotter):
        self.config = config
        self.loader = loader
        self.plotter = plotter
    
    @staticmethod
    def load_celldbs(sessions: Dict[int, SessionConfig]) -> Dict[str, pd.DataFrame]:
        """Load cell databases for all unique subjects (from tuning_with_rasters)."""
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
        """Load session ephys data (EXACT copy from tuning_with_rasters)."""
        celldb_full = celldbs[session.subject]
        celldb_subset = celldb_full[
            (celldb_full.date == session.date) &
            (celldb_full.pdepth == session.depth)
        ]
        
        ensemble = ephyscore.CellEnsemble(celldb_subset)
        ephys_data, bdata = ensemble.load('optoTuningFreq')
        
        # Get spike data
        event_onset_times = ephys_data['events']['stimOn']
        n_trials = len(bdata['currentFreq'])
        
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
    
    def create_category_pdfs(self):
        """Create 4 category PDFs across all sessions."""
        print("\n" + "="*70)
        print("CREATING GAUSSIAN FIT + RASTER PDFs")
        print("="*70)
        
        # Load cell databases once for all sessions
        print("\nLoading cell databases...")
        celldbs = self.load_celldbs(SESSIONS)
        
        # Collect all cells by category
        good_fits = []
        poor_fits = []
        failed_fits = []
        all_tuned = []
        
        # Load all sessions
        for session_id in sorted(SESSIONS.keys()):
            session = SESSIONS[session_id]
            
            try:
                print(f"\nLoading session {session_id}: {session.subject} {session.date}")
                
                # Load Gaussian fits
                fits_off = self.loader.load_gaussian_fits(session_id, 'off')
                fits_on = self.loader.load_gaussian_fits(session_id, 'on')
                
                # Load raw data (for rasters) - using proven method
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
                    
                    # Categorize
                    if fit_off['fit_quality'] == 'good' and fit_on['fit_quality'] == 'good':
                        good_fits.append(cell_data)
                    elif fit_off['fit_quality'] == 'poor' and fit_on['fit_quality'] == 'poor':
                        poor_fits.append(cell_data)
                    elif fit_off['fit_quality'] == 'failed' or fit_on['fit_quality'] == 'failed':
                        failed_fits.append(cell_data)
                    
                    if fit_off['empirical_is_tuned']:
                        all_tuned.append(cell_data)
                
            except FileNotFoundError as e:
                print(f"  SKIPPING: {e}")
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
        
        # Create PDFs
        self._create_pdf(good_fits, 'good_fits', 'Good Gaussian Fits')
        self._create_pdf(poor_fits, 'poor_fits', 'Poor Gaussian Fits')
        self._create_pdf(failed_fits, 'failed_fits', 'Failed Gaussian Fits')
        self._create_pdf(all_tuned, 'all_empirically_tuned', 'All Empirically Tuned Cells')
    
    def _create_pdf(self, cell_data_list: List, filename_suffix: str, title: str):
        """Create a single PDF for a category."""
        if len(cell_data_list) == 0:
            print(f"\n  No cells for: {title}")
            return
        
        filename = f'gaussian_fits_with_rasters_{filename_suffix}.pdf'
        pdf_path = os.path.join(self.config.output_dir, filename)
        
        print(f"\n  Creating {title} PDF with {len(cell_data_list)} cells...")
        
        with PdfPages(pdf_path) as pdf:
            n_cells_per_page = self.config.cells_per_page
            n_pages = int(np.ceil(len(cell_data_list) / n_cells_per_page))
            
            for page_idx in range(n_pages):
                # Create figure with GridSpec (3 rows x 3 cols)
                # Increased middle row height for better Gaussian plot visibility
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
    print("GAUSSIAN FIT + RASTER VISUALIZATION")
    print("="*70)
    
    config = PlotConfig()
    
    # Create output directory using config property
    os.makedirs(config.output_dir, exist_ok=True)
    
    loader = GaussianFitDataLoader(config)
    plotter = GaussianFitPlotter(config)
    generator = CategoryPDFGenerator(config, loader, plotter)
    
    generator.create_category_pdfs()
    
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)


if __name__ == '__main__':
    main()
