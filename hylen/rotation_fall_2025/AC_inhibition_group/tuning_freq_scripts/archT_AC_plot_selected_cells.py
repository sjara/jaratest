"""
Professional Visualization of Selected Cells of Interest

Creates high-quality, publication-ready PDFs for individually selected cells,
showing comprehensive tuning analysis with 5 key plots:

1. Raster plot (frequency-sorted, laser OFF vs ON)
2. Raw tuning curve (observed data points, laser OFF vs ON)
3. Normalized tuning curve (normalized to OFF peak)
4. Gaussian fitted tuning curve (fitted curves + observed data)
5. Normalized Gaussian fitted tuning curve

Layout: 2 rows × 3 columns (landscape, one cell per page)
Output: Individual PDF per cell for easy inclusion in presentations

Usage:
    Edit CELLS_TO_PLOT list below to specify which cells to visualize.
    Each entry: (session_id, cell_idx, optional_note)

Author: Hylen
Date: 2025
"""

import os
import sys
from typing import Tuple, Dict, List, Optional, NamedTuple
from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from jaratoolbox import settings, celldatabase, ephyscore, behavioranalysis, extraplots

# Add hylen directory to path
sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


# =============================================================================
# CELLS TO PLOT - EDIT THIS LIST!
# =============================================================================

# List of cells to visualize: (session_id, cell_idx, optional_note)
# Add or remove entries as needed
CELLS_TO_PLOT = [
    (4, 108, "Shows an increase in tuning and evoked firing rate with laser on"),# this one to show how tuning increases and firing rate increases
    (4, 57, "Shows an increase in tuning and evoked firing rate with laser on"),  # this one to show how tuning increases but firing rate decreases
    (4, 227, "Increase in tuning by our metric, but has an overall lower firing rate"),  # this one to show how tuning increases but no change in FR
    (8, 5, "Shows no change in selectivity or FR with laser on"),
    (0, 296, " Better example of decrease in FR but increase in tuning"),
    # Add more cells here:
    # (session_id, cell_idx, "Your note here"),
]


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
    
    # Figure dimensions (MUCH LARGER for better visibility)
    fig_width: float = 28  # Increased from 20
    fig_height: float = 16  # Increased from 11
    
    # Directories
    @property
    def tuning_metrics_dir(self) -> str:
        return str(get_reports_subdir('tuning_freq_analysis'))
    
    @property
    def gaussian_fits_dir(self) -> str:
        return str(get_reports_subdir('tuning_freq_gaussian_fits'))
    
    @property
    def output_dir(self) -> str:
        return str(get_reports_subdir('selected_cells_visualization'))


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
# DATA LOADING (unchanged)
# =============================================================================

class SelectedCellsLoader:
    """Loads data for selected cells."""
    
    def __init__(self, config: PlotConfig):
        self.config = config
    
    def load_cell_data(
        self,
        session_id: int,
        cell_idx: int
    ) -> dict:
        """Load all data for one cell."""
        session = SESSIONS[session_id]
        
        # Load tuning metrics (OFF and ON)
        metrics_off = self._load_metrics(session_id, cell_idx, 'off')
        metrics_on = self._load_metrics(session_id, cell_idx, 'on')
        
        # Load Gaussian fits (OFF and ON)
        fits_off = self._load_gaussian_fits(session_id, cell_idx, 'off')
        fits_on = self._load_gaussian_fits(session_id, cell_idx, 'on')
        
        # Load raw session data (for rasters and tuning curves)
        session_data = self._load_session_data(session)
        
        return {
            'session': session,
            'session_id': session_id,
            'cell_idx': cell_idx,
            'metrics_off': metrics_off,
            'metrics_on': metrics_on,
            'fits_off': fits_off,
            'fits_on': fits_on,
            'session_data': session_data
        }
    
    def _load_metrics(self, session_id: int, cell_idx: int, laser: str) -> pd.Series:
        """Load tuning metrics for one cell."""
        csv_path = os.path.join(
            self.config.tuning_metrics_dir,
            f'session_{session_id}_laser_{laser}_tuning_metrics.csv'
        )
        
        df = pd.read_csv(csv_path)
        cell_data = df[df['cell_idx'] == cell_idx]
        
        if len(cell_data) == 0:
            raise ValueError(f"Cell {cell_idx} not found in session {session_id} laser {laser}")
        
        return cell_data.iloc[0]
    
    def _load_gaussian_fits(self, session_id: int, cell_idx: int, laser: str) -> Optional[pd.Series]:
        """Load Gaussian fits for one cell."""
        csv_path = os.path.join(
            self.config.gaussian_fits_dir,
            f'session_{session_id}_laser_{laser}_gaussian_fits.csv'
        )
        
        if not os.path.exists(csv_path):
            return None
        
        df = pd.read_csv(csv_path)
        cell_data = df[df['cell_idx'] == cell_idx]
        
        if len(cell_data) == 0:
            return None
        
        return cell_data.iloc[0]
    
    def _load_session_data(self, session: SessionConfig) -> dict:
        """Load session ephys data (copy from tuning_with_rasters)."""
        # Load cell database
        inforec_file = os.path.join(settings.INFOREC_PATH, f'{session.subject}_inforec.py')
        celldb = celldatabase.generate_cell_database(inforec_file, ignoreMissing=True)
        
        celldb_subset = celldb[
            (celldb.date == session.date) &
            (celldb.pdepth == session.depth)
        ]
        
        ensemble = ephyscore.CellEnsemble(celldb_subset)
        ephys_data, bdata = ensemble.load('optoTuningFreq')
        
        # Get spike data
        event_onset_times = ephys_data['events']['stimOn']
        n_trials = len(bdata['currentFreq'])
        
        if len(event_onset_times) == n_trials + 1:
            event_onset_times = event_onset_times[:n_trials]
        
        spike_times_all, trial_index_all, index_limits_all = ensemble.eventlocked_spiketimes(
            event_onset_times, (-0.5, 1.0)
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
# PLOTTING MODULE (FIXED)
# =============================================================================

class ProfessionalCellPlotter:
    """Creates publication-quality plots for individual cells."""
    
    def __init__(self, config: PlotConfig):
        self.config = config
        # Use desaturated/dull cyan and darker magenta (colorblind-friendly)
        self.color_off = '#56B4E9'  # Dull cyan - Laser OFF (unchanged)
        self.color_on = '#9E4784'   # Darker magenta/purple - Laser ON
    
    def plot_cell_5panel(self, cell_data: dict, output_dir: str):
        """
        Create 5 individual PNG files for one cell.
        
        Layout: Each plot saved separately as PNG in cell-specific subfolder
        """
        session = cell_data['session']
        cell_idx = cell_data['cell_idx']
        session_id = cell_data['session_id']
        
        category = cell_data['metrics_off'].get('tuning_category', 'unknown')
        category_display = category.replace('_', ' ').title()
        
        # Create individual plots
        print(f"  Creating raster plot...")
        self._save_raster(cell_data, output_dir)
        
        print(f"  Creating raw tuning curve...")
        self._save_raw_tuning(cell_data, output_dir)
        
        print(f"  Creating normalized tuning curve...")
        self._save_normalized_tuning(cell_data, output_dir)
        
        print(f"  Creating Gaussian fit...")
        self._save_gaussian_fit(cell_data, output_dir, normalized=False)
        
        print(f"  Creating normalized Gaussian fit...")
        self._save_gaussian_fit(cell_data, output_dir, normalized=True)
        
        print(f"  ✓ Saved all plots to: {output_dir}")
    
    def _save_raster(self, cell_data: dict, output_dir: str):
        """Save raster plot as PNG."""
        fig, ax = plt.subplots(figsize=(12, 10))
        self._plot_raster(ax, cell_data)
        
        session = cell_data['session']
        cell_idx = cell_data['cell_idx']
        session_id = cell_data['session_id']
        
        ax.set_title(
            f"Cell {cell_idx} | Session {session_id} | {session.subject} {session.date} {session.depth}µm\nRaster Plot",
            fontsize=14, fontweight='bold', pad=15
        )
        
        output_path = os.path.join(output_dir, '1_raster.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    
    def _save_raw_tuning(self, cell_data: dict, output_dir: str):
        """Save raw tuning curve as PNG."""
        fig, ax = plt.subplots(figsize=(10, 8))
        self._plot_raw_tuning(ax, cell_data)
        
        session = cell_data['session']
        cell_idx = cell_data['cell_idx']
        session_id = cell_data['session_id']
        
        ax.set_title(
            f"Cell {cell_idx} | Session {session_id} | {session.subject} {session.date} {session.depth}µm\nRaw Tuning Curve",
            fontsize=14, fontweight='bold', pad=15
        )
        
        output_path = os.path.join(output_dir, '2_raw_tuning.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    
    def _save_normalized_tuning(self, cell_data: dict, output_dir: str):
        """Save normalized tuning curve as PNG."""
        fig, ax = plt.subplots(figsize=(10, 8))
        self._plot_normalized_tuning(ax, cell_data)
        
        session = cell_data['session']
        cell_idx = cell_data['cell_idx']
        session_id = cell_data['session_id']
        
        ax.set_title(
            f"Cell {cell_idx} | Session {session_id} | {session.subject} {session.date} {session.depth}µm\nNormalized Tuning Curve",
            fontsize=14, fontweight='bold', pad=15
        )
        
        output_path = os.path.join(output_dir, '3_normalized_tuning.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    
    def _save_gaussian_fit(self, cell_data: dict, output_dir: str, normalized: bool):
        """Save Gaussian fit as PNG."""
        fig, ax = plt.subplots(figsize=(12, 8))
        self._plot_gaussian_fit(ax, cell_data, normalized=normalized)
        
        session = cell_data['session']
        cell_idx = cell_data['cell_idx']
        session_id = cell_data['session_id']
        
        title_suffix = "Normalized Gaussian Fit" if normalized else "Gaussian Fit"
        filename = '5_normalized_gaussian.png' if normalized else '4_gaussian_fit.png'
        
        ax.set_title(
            f"Cell {cell_idx} | Session {session_id} | {session.subject} {session.date} {session.depth}µm\n{title_suffix}",
            fontsize=14, fontweight='bold', pad=15
        )
        
        output_path = os.path.join(output_dir, filename)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    
    def _plot_raster(self, ax: Axes, cell_data: dict):
        """Plot raster - EXACT COPY from tuning_with_rasters script."""
        cell_idx = cell_data['cell_idx']
        session_data = cell_data['session_data']
        
        spike_times = session_data['spike_times_all'][cell_idx]
        trial_index = session_data['trial_index_all'][cell_idx]
        index_limits = session_data['index_limits_all'][cell_idx]
        bdata = session_data['bdata']
        
        frequencies = np.asarray(bdata['currentFreq']).flatten()
        unique_freqs = np.unique(frequencies)
        
        if 'laserTrial' in bdata:
            laser_trials = np.asarray(bdata['laserTrial']).flatten().astype(bool)
        else:
            laser_trials = np.zeros(len(frequencies), dtype=bool)
        
        # Build trial organization - EXACT from working script
        trials_each_freq = behavioranalysis.find_trials_each_type(frequencies, unique_freqs)
        
        off_trials = np.flatnonzero(laser_trials == 0)
        on_trials = np.flatnonzero(laser_trials == 1)
        
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
        
        # Colors
        n_freqs = len(unique_freqs)
        color_each_cond = (['0.5', '0.75'] * int(np.ceil(n_freqs / 2.0)))[:n_freqs]
        color_each_cond = color_each_cond + color_each_cond
        
        # Labels
        freqs_khz = np.round(unique_freqs / 1000, 2)
        labels = [f'{fk}' for fk in freqs_khz]
        labels = labels + labels
        
        # Plot raster - EXACT from working script
        pRaster, hcond, zline = extraplots.raster_plot(
            spike_times, index_limits, self.config.time_range,
            trialsEachCond=trials_each_cond,
            colorEachCond=color_each_cond,
            labels=labels
        )
        plt.setp(pRaster, ms=3)  # Slightly larger markers for individual plots
        
        # Add analysis window indicator (gray filled box with 50% opacity)
        total_trials = trials_each_cond.sum()
        ax.axvspan(self.config.response_window[0], self.config.response_window[1],
                  ymin=0, ymax=1, color='gray', alpha=0.5, zorder=0)
        
        # Hide every other label
        for i, label in enumerate(ax.get_yticklabels()):
            if i % 2 == 1:
                label.set_visible(False)
        
        # Laser boundary
        cumsum_trials = np.cumsum([trials_each_cond[:, i].sum() for i in range(n_freqs)])
        laser_boundary = cumsum_trials[-1] - 0.5
        ax.axhline(laser_boundary, color='red', linewidth=4, linestyle='--', alpha=0.8, zorder=10)
        
        # Laser labels
        yticks_minor = [laser_boundary/2, laser_boundary + (total_trials - laser_boundary)/2]
        ax.set_yticks(yticks_minor, ['Laser OFF', 'Laser ON'], minor=True)
        ax.tick_params(axis='y', which='minor', left=False, right=True,
                      labelleft=False, labelright=True, labelsize=14, pad=5, labelcolor='red')
        
        # Format - keep original time range to preserve alternating background boxes
        ax.set_xlabel('Time from sound onset (s)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Frequency (kHz)', fontsize=14, fontweight='bold')
        ax.set_xlim(self.config.time_range)  # Keep full range to preserve background boxes
        ax.tick_params(axis='both', which='major', labelsize=13)
    
    def _plot_raw_tuning(self, ax: Axes, cell_data: dict):
        """Plot raw tuning curve (observed data points) with SEM shaded regions."""
        metrics_off = cell_data['metrics_off']
        metrics_on = cell_data['metrics_on']
        
        # Parse tuning curves from CSV strings
        freqs_str = str(metrics_off.get('tuning_freqs', ''))
        rates_off_str = str(metrics_off.get('tuning_rates', ''))
        rates_on_str = str(metrics_on.get('tuning_rates', ''))
        
        # Parse SEM values
        sems_off_str = str(metrics_off.get('tuning_sems', ''))
        sems_on_str = str(metrics_on.get('tuning_sems', ''))
        
        if not freqs_str or freqs_str == 'nan':
            ax.text(0.5, 0.5, 'No tuning data', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return
        
        # Parse frequencies
        freqs = np.array([float(f) for f in freqs_str.split(',') if f.strip()])
        freqs_khz = freqs / 1000.0
        x_pos = np.arange(len(freqs_khz))
        
        # Parse rates
        rates_off = self._parse_rates_string(rates_off_str, len(freqs))
        rates_on = self._parse_rates_string(rates_on_str, len(freqs))
        
        # Parse SEMs
        sems_off = self._parse_rates_string(sems_off_str, len(freqs))
        sems_on = self._parse_rates_string(sems_on_str, len(freqs))
        
        # Plot OFF with shaded SEM
        valid_off = ~np.isnan(rates_off)
        ax.plot(x_pos[valid_off], rates_off[valid_off],
                'o-', color=self.color_off, linewidth=4, markersize=12,
                markerfacecolor=self.color_off, markeredgecolor='black', markeredgewidth=2,
                label='Laser OFF', alpha=0.8, zorder=3)
        
        # Add shaded SEM region for OFF
        ax.fill_between(x_pos[valid_off],
                        rates_off[valid_off] - sems_off[valid_off],
                        rates_off[valid_off] + sems_off[valid_off],
                        color=self.color_off, alpha=0.3, zorder=2)
        
        # Plot ON with shaded SEM
        valid_on = ~np.isnan(rates_on)
        if np.any(valid_on):
            ax.plot(x_pos[valid_on], rates_on[valid_on],
                    's--', color=self.color_on, linewidth=4, markersize=12,
                    markerfacecolor=self.color_on, markeredgecolor='black', markeredgewidth=2,
                    label='Laser ON', alpha=0.8, zorder=3)
            
            # Add shaded SEM region for ON
            ax.fill_between(x_pos[valid_on],
                            rates_on[valid_on] - sems_on[valid_on],
                            rates_on[valid_on] + sems_on[valid_on],
                            color=self.color_on, alpha=0.3, zorder=2)
        
        # Mark best frequencies
        if np.any(valid_off):
            bf_idx_off = np.argmax(rates_off[valid_off])
            bf_x = x_pos[valid_off][bf_idx_off]
            bf_y = rates_off[valid_off][bf_idx_off]
            ax.plot(bf_x, bf_y, '*', markersize=24, color=self.color_off,
                   markeredgecolor='black', markeredgewidth=2, zorder=10)
        
        if np.any(valid_on):
            bf_idx_on = np.argmax(rates_on[valid_on])
            bf_x = x_pos[valid_on][bf_idx_on]
            bf_y = rates_on[valid_on][bf_idx_on]
            ax.plot(bf_x, bf_y, '*', markersize=24, color=self.color_on,
                   markeredgecolor='black', markeredgewidth=2, zorder=10)
        
        # Format
        ax.set_ylabel('Firing Rate (Hz)', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'{f:.1f}' for f in freqs_khz], rotation=45, ha='right', fontsize=12)
        ax.set_xlim([-0.5, len(freqs_khz) - 0.5])
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(loc='upper right', fontsize=12, frameon=True, framealpha=0.9)
        ax.tick_params(axis='both', which='major', labelsize=13)
    
    def _plot_normalized_tuning(self, ax: Axes, cell_data: dict):
        """Plot normalized tuning curve (normalized to OFF peak) with SEM shaded regions."""
        metrics_off = cell_data['metrics_off']
        metrics_on = cell_data['metrics_on']
        
        # Parse tuning curves
        freqs_str = str(metrics_off.get('tuning_freqs', ''))
        rates_off_str = str(metrics_off.get('tuning_rates', ''))
        rates_on_str = str(metrics_on.get('tuning_rates', ''))
        
        # Parse SEM values
        sems_off_str = str(metrics_off.get('tuning_sems', ''))
        sems_on_str = str(metrics_on.get('tuning_sems', ''))
        
        if not freqs_str or freqs_str == 'nan':
            ax.text(0.5, 0.5, 'No tuning data', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return
        
        freqs = np.array([float(f) for f in freqs_str.split(',') if f.strip()])
        rates_off = self._parse_rates_string(rates_off_str, len(freqs))
        rates_on = self._parse_rates_string(rates_on_str, len(freqs))
        
        # Parse SEMs
        sems_off = self._parse_rates_string(sems_off_str, len(freqs))
        sems_on = self._parse_rates_string(sems_on_str, len(freqs))
        
        # Get best frequency from OFF condition
        best_freq = metrics_off.get('best_freq', np.nan)
        if np.isnan(best_freq) or best_freq == 0:
            ax.text(0.5, 0.5, 'Cannot determine\nbest frequency', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return
        
        # Convert frequencies to octaves from best frequency
        octaves_from_bf = np.log2(freqs / best_freq)
        
        # Normalize by OFF peak
        peak_off = np.nanmax(rates_off)
        if peak_off == 0 or np.isnan(peak_off):
            ax.text(0.5, 0.5, 'Cannot normalize\n(peak = 0)', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return
        
        rates_off_norm = rates_off / peak_off
        rates_on_norm = rates_on / peak_off
        
        # Normalize SEMs by the same factor
        sems_off_norm = sems_off / peak_off
        sems_on_norm = sems_on / peak_off
        
        # Plot OFF with shaded SEM
        valid_off = ~np.isnan(rates_off_norm)
        ax.plot(octaves_from_bf[valid_off], rates_off_norm[valid_off],
                'o-', color=self.color_off, linewidth=4, markersize=12,
                markerfacecolor=self.color_off, markeredgecolor='black', markeredgewidth=2,
                label='Laser OFF', alpha=0.8, zorder=3)
        
        # Add shaded SEM region for OFF
        ax.fill_between(octaves_from_bf[valid_off],
                        rates_off_norm[valid_off] - sems_off_norm[valid_off],
                        rates_off_norm[valid_off] + sems_off_norm[valid_off],
                        color=self.color_off, alpha=0.3, zorder=2)
        
        # Plot ON with shaded SEM
        valid_on = ~np.isnan(rates_on_norm)
        if np.any(valid_on):
            ax.plot(octaves_from_bf[valid_on], rates_on_norm[valid_on],
                    's--', color=self.color_on, linewidth=4, markersize=12,
                    markerfacecolor=self.color_on, markeredgecolor='black', markeredgewidth=2,
                    label='Laser ON', alpha=0.8, zorder=3)
            
            # Add shaded SEM region for ON
            ax.fill_between(octaves_from_bf[valid_on],
                            rates_on_norm[valid_on] - sems_on_norm[valid_on],
                            rates_on_norm[valid_on] + sems_on_norm[valid_on],
                            color=self.color_on, alpha=0.3, zorder=2)
        
        # Reference line at 1.0 (normalized peak)
        ax.axhline(1.0, color='black', linestyle=':', linewidth=3, alpha=0.5, zorder=0)
        
        # Vertical line at BF (0 octaves)
        ax.axvline(0, color=self.color_off, linestyle='--', linewidth=2, alpha=0.6, zorder=0,
                  label=f'BF = {best_freq/1000:.1f} kHz')
        
        # Format
        ax.set_xlabel('Octaves from Best Frequency (OFF)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Normalized Response', fontsize=14, fontweight='bold')
        ax.set_ylim([0, max(1.2, np.nanmax(rates_on_norm) * 1.1) if np.any(valid_on) else 1.2])
        ax.grid(True, alpha=0.3, axis='both')
        ax.legend(loc='upper right', fontsize=12, frameon=True, framealpha=0.9)
        ax.tick_params(axis='both', which='major', labelsize=13)
    
    def _plot_gaussian_fit(self, ax: Axes, cell_data: dict, normalized: bool = False):
        """Plot Gaussian fitted tuning curve with SEM shaded regions on observed data."""
        fits_off = cell_data.get('fits_off')
        fits_on = cell_data.get('fits_on')
        
        if fits_off is None:
            ax.text(0.5, 0.5, 'No Gaussian fit\navailable', ha='center', va='center',
                   transform=ax.transAxes, fontsize=14)
            return
        
        # Get best frequency
        bf = fits_off['empirical_best_freq']
        
        # Parse observed data
        metrics_off = cell_data['metrics_off']
        metrics_on = cell_data['metrics_on']
        
        freqs_str = str(metrics_off.get('tuning_freqs', ''))
        rates_off_str = str(metrics_off.get('tuning_rates', ''))
        rates_on_str = str(metrics_on.get('tuning_rates', ''))
        
        # Parse SEMs
        sems_off_str = str(metrics_off.get('tuning_sems', ''))
        sems_on_str = str(metrics_on.get('tuning_sems', ''))
        
        freqs_obs = np.array([float(f) for f in freqs_str.split(',') if f.strip()])
        rates_off_obs = self._parse_rates_string(rates_off_str, len(freqs_obs))
        rates_on_obs = self._parse_rates_string(rates_on_str, len(freqs_obs))
        
        # Parse SEMs
        sems_off_obs = self._parse_rates_string(sems_off_str, len(freqs_obs))
        sems_on_obs = self._parse_rates_string(sems_on_str, len(freqs_obs))
        
        # Smooth frequencies for Gaussian curve
        freqs_smooth = bf * 2 ** np.linspace(-3, 3, 200)
        
        # Gaussian function
        def gaussian(f, baseline, amplitude, mean_oct, sigma, bf_ref):
            octaves = np.log2(f / bf_ref)
            return baseline + amplitude * np.exp(-0.5 * ((octaves - mean_oct) / sigma)**2)
        
        # Calculate Gaussian curves
        rates_off_smooth = gaussian(freqs_smooth,
                                   fits_off['baseline'], fits_off['amplitude'],
                                   fits_off['mean_octave'], fits_off['sigma'], bf)
        
        rates_on_smooth = gaussian(freqs_smooth,
                                  fits_on['baseline'], fits_on['amplitude'],
                                  fits_on['mean_octave'], fits_on['sigma'], bf) if fits_on is not None else None
        
        # Normalize if requested - use OBSERVED OFF peak, not fitted peak
        if normalized:
            peak_off_obs = np.nanmax(rates_off_obs)
            if peak_off_obs == 0 or np.isnan(peak_off_obs):
                ax.text(0.5, 0.5, 'Cannot normalize\n(peak = 0)', ha='center', va='center',
                       transform=ax.transAxes, fontsize=14)
                return
            
            # Normalize everything by the same observed OFF peak
            rates_off_smooth = rates_off_smooth / peak_off_obs
            if rates_on_smooth is not None:
                rates_on_smooth = rates_on_smooth / peak_off_obs
            rates_off_obs = rates_off_obs / peak_off_obs
            rates_on_obs = rates_on_obs / peak_off_obs
            
            # Normalize SEMs
            sems_off_obs = sems_off_obs / peak_off_obs
            sems_on_obs = sems_on_obs / peak_off_obs
        
        # X-axis positions
        x_smooth = np.linspace(0, 15, 200)
        octaves_obs = np.log2(freqs_obs / bf)
        x_obs = (octaves_obs + 3) * (15 / 6)
        
        # Plot Gaussian curves (solid lines)
        ax.plot(x_smooth, rates_off_smooth, '-', color=self.color_off, linewidth=4,
               label='Fitted OFF', alpha=0.7)
        
        if rates_on_smooth is not None:
            ax.plot(x_smooth, rates_on_smooth, '-', color=self.color_on, linewidth=4,
                   label='Fitted ON', alpha=0.7)
        
        # Plot observed data with shaded SEM (dotted lines)
        valid_off = ~np.isnan(rates_off_obs)
        if np.any(valid_off):
            ax.plot(x_obs[valid_off], rates_off_obs[valid_off],
                    'o:', color=self.color_off, linewidth=4, markersize=10,
                    markerfacecolor=self.color_off, markeredgecolor='black', markeredgewidth=1.5,
                    label='Observed OFF', zorder=4)
            
            # Add shaded SEM region for OFF
            ax.fill_between(x_obs[valid_off],
                            rates_off_obs[valid_off] - sems_off_obs[valid_off],
                            rates_off_obs[valid_off] + sems_off_obs[valid_off],
                            color=self.color_off, alpha=0.3, zorder=3)
        
        valid_on = ~np.isnan(rates_on_obs)
        if np.any(valid_on):
            ax.plot(x_obs[valid_on], rates_on_obs[valid_on],
                    's:', color=self.color_on, linewidth=4, markersize=10,
                    markerfacecolor=self.color_on, markeredgecolor='black', markeredgewidth=1.5,
                    label='Observed ON', zorder=4)
            
            # Add shaded SEM region for ON
            ax.fill_between(x_obs[valid_on],
                            rates_on_obs[valid_on] - sems_on_obs[valid_on],
                            rates_on_obs[valid_on] + sems_on_obs[valid_on],
                            color=self.color_on, alpha=0.3, zorder=3)
        
        # Format
        freqs_ticks = bf * 2 ** np.linspace(-3, 3, 16)
        freqs_khz_ticks = freqs_ticks / 1000.0
        x_ticks = np.linspace(0, 15, 16)
        
        ylabel = 'Normalized Response' if normalized else 'Firing Rate (Hz)'
        ax.set_ylabel(ylabel, fontsize=14, fontweight='bold')
        ax.set_xlabel('Frequency (kHz)', fontsize=14, fontweight='bold')
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f'{f:.1f}' for f in freqs_khz_ticks],
                          rotation=45, ha='right', fontsize=12)
        ax.set_xlim([-0.5, 15.5])
        ax.grid(True, alpha=0.3, axis='y')
        
        if normalized:
            ax.axhline(1.0, color='black', linestyle=':', linewidth=3, alpha=0.5, zorder=0)
        
        ax.legend(loc='upper right', fontsize=11, frameon=True, framealpha=0.9, ncol=2)
        ax.tick_params(axis='both', which='major', labelsize=13)
    
    @staticmethod
    def _parse_rates_string(rates_str: str, n_freqs: int) -> np.ndarray:
        """Parse comma-separated rates string into numpy array."""
        if not rates_str or rates_str == 'nan':
            return np.full(n_freqs, np.nan)
        
        rates = []
        for r in rates_str.split(','):
            if r.strip().lower() == 'nan' or r.strip() == '':
                rates.append(np.nan)
            else:
                rates.append(float(r))
        
        return np.array(rates)


# =============================================================================
# MAIN COORDINATOR
# =============================================================================

class SelectedCellsVisualizer:
    """Coordinates visualization of selected cells."""
    
    def __init__(self, config: PlotConfig, cells_list: List[Tuple]):
        self.config = config
        self.cells_list = cells_list
        self.loader = SelectedCellsLoader(config)
        self.plotter = ProfessionalCellPlotter(config)
    
    def run(self):
        """Execute visualization pipeline."""
        print("="*70)
        print("PROFESSIONAL VISUALIZATION OF SELECTED CELLS")
        print("="*70)
        
        if len(self.cells_list) == 0:
            print("\n✗ No cells specified in CELLS_TO_PLOT list!")
            print("  Edit the script and add cells to the CELLS_TO_PLOT list.")
            return 1
        
        print(f"\n✓ Found {len(self.cells_list)} cells to plot")
        
        # Create output directory
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Process each cell
        n_success = 0
        n_failed = 0
        
        for entry in self.cells_list:
            # Parse entry (handle both 2-tuple and 3-tuple)
            if len(entry) == 2:
                session_id, cell_idx = entry
                notes = ""
            elif len(entry) == 3:
                session_id, cell_idx, notes = entry
            else:
                print(f"\n✗ Invalid entry format: {entry}")
                n_failed += 1
                continue
            
            print(f"\n{'='*70}")
            print(f"Processing Cell {cell_idx} from Session {session_id}")
            if notes:
                print(f"  Notes: {notes}")
            print(f"{'='*70}")
            
            try:
                # Load all data for this cell
                cell_data = self.loader.load_cell_data(session_id, cell_idx)
                
                # Create cell-specific subfolder
                session = cell_data['session']
                cell_folder_name = (
                    f"session{session_id:02d}_{session.subject}_{session.date}_"
                    f"depth{session.depth}_cell{cell_idx:03d}"
                )
                cell_output_dir = os.path.join(self.config.output_dir, cell_folder_name)
                os.makedirs(cell_output_dir, exist_ok=True)
                
                # Generate plots (saves 5 PNGs)
                self.plotter.plot_cell_5panel(cell_data, cell_output_dir)
                
                n_success += 1
                
            except Exception as e:
                print(f"  ✗ ERROR: {e}")
                import traceback
                traceback.print_exc()
                n_failed += 1
        
        # Summary
        print(f"\n{'='*70}")
        print("VISUALIZATION COMPLETE")
        print(f"{'='*70}")
        print(f"Successfully plotted: {n_success} cells")
        print(f"Failed: {n_failed} cells")
        print(f"Output directory: {self.config.output_dir}")
        print(f"\nEach cell has 5 PNGs in its own subfolder:")
        print(f"  1_raster.png")
        print(f"  2_raw_tuning.png")
        print(f"  3_normalized_tuning.png")
        print(f"  4_gaussian_fit.png")
        print(f"  5_normalized_gaussian.png")
        
        return 0 if n_failed == 0 else 1


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main execution."""
    config = PlotConfig()
    visualizer = SelectedCellsVisualizer(config, CELLS_TO_PLOT)
    
    return visualizer.run()


if __name__ == '__main__':
    import sys
    sys.exit(main())
