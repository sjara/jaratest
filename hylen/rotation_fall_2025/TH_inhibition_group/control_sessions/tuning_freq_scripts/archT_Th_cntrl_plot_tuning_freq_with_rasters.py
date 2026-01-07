"""
Combined Tuning Curve + Raster Plot Visualization

This script creates comprehensive PDFs showing tuning curves with their corresponding
raster plots for detailed analysis of individual cells.

Layout:
- 3 cells per page (landscape orientation)
- Each cell: Tuning curve (top) + Raster plot (bottom)
- Organized by session and tuning category

Features:
- Reads pre-computed metrics from CSV files
- Uses jaratoolbox for all spike/trial processing
- Modular architecture borrowed from raster plot scripts
- Laser OFF vs ON comparison in tuning curves
- Frequency-organized rasters below

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
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.axes import Axes
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
class VisualizationConfig:
    """Configuration for combined visualization."""
    time_range: Tuple[float, float] = (-0.5, 1.0)
    response_window: Tuple[float, float] = (0.005, 0.095)
    artifact_window: float = 0.005
    cells_per_page: int = 3  # 3 cells per page (landscape)
    n_cols: int = 3  # 3 columns
    fig_width: float = 17  # Landscape
    fig_height: float = 11

    @property
    def metrics_dir(self) -> str:
        return str(get_reports_subdir('arch024/control_sessions/tuning_freq_analysis'))

    @property
    def override_file(self) -> str:
        return os.path.join(self.metrics_dir, 'classification_overrides.csv')


class CellMetrics(NamedTuple):
    """Container for cell metrics from CSV."""
    cell_idx: int
    best_freq: float
    peak_rate: float
    mean_rate: float
    selectivity_index: float
    sparseness: float
    tuning_quality: float
    bandwidth_octaves: float
    coefficient_of_variation: float
    tuning_category: str


# All available sessions
SESSIONS = {
    0: SessionConfig('arch024', '2025-04-14', 2780),
    1: SessionConfig('arch024', '2025-04-14', 3500),
    2: SessionConfig('arch024', '2025-04-17', 2780),
    3: SessionConfig('arch024', '2025-04-17', 3500)
}


# =============================================================================
# DATA LOADING
# =============================================================================

class DataLoader:
    """Handles loading of metrics and session data."""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
    
    def load_metrics(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load laser OFF and ON metrics from CSV files."""
        csv_off = os.path.join(self.config.metrics_dir, 'all_sessions_laser_off_tuning_metrics.csv')
        csv_on = os.path.join(self.config.metrics_dir, 'all_sessions_laser_on_tuning_metrics.csv')
        
        df_off = pd.read_csv(csv_off)
        df_on = pd.read_csv(csv_on)
        
        # Apply classification overrides if available
        df_off = self._apply_overrides(df_off)
        
        # Merge on session_id and cell_idx
        df_merged = pd.merge(df_off, df_on, on=['session_id', 'cell_idx'],
                            how='left', suffixes=('_off', '_on'))
        
        return df_merged
    
    def _apply_overrides(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply manual classification overrides from CSV file."""
        if not os.path.exists(self.config.override_file):
            return df
        
        try:
            df_overrides = pd.read_csv(self.config.override_file)
            
            # Validate required columns
            required_cols = ['session_id', 'cell_idx', 'override_category']
            if not all(col in df_overrides.columns for col in required_cols):
                print(f"  WARNING: Override file missing required columns")
                return df
            
            n_overridden = 0
            for _, override_row in df_overrides.iterrows():
                session_id = int(override_row['session_id'])
                cell_idx = int(override_row['cell_idx'])
                new_category = str(override_row['override_category']).lower()
                
                # Find matching cell in dataframe
                mask = (df['session_id'] == session_id) & (df['cell_idx'] == cell_idx)
                
                if mask.any():
                    old_category = df.loc[mask, 'tuning_category'].iloc[0]
                    df.loc[mask, 'tuning_category'] = new_category
                    n_overridden += 1
                    print(f"  Override applied: Session {session_id}, Cell {cell_idx}: "
                          f"{old_category} → {new_category}")
            
            if n_overridden > 0:
                print(f"\n  ✓ Applied {n_overridden} classification overrides")
            
        except Exception as e:
            print(f"  WARNING: Failed to apply overrides: {e}")
        
        return df
    
    @staticmethod
    def load_celldbs(sessions: Dict[int, SessionConfig]) -> Dict[str, pd.DataFrame]:
        """Load cell databases for all unique subjects."""
        subjects = list(set(session.subject for session in sessions.values()))
        celldbs = {}
        
        for subject in subjects:
            inforec_file = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
            celldbs[subject] = celldatabase.generate_cell_database(inforec_file, ignoreMissing=True)
        
        return celldbs
    
    def load_session_data(
        self,
        session: SessionConfig,
        celldb_full: pd.DataFrame
    ) -> Tuple[pd.DataFrame, dict, dict, ephyscore.CellEnsemble]:
        """Load session ephys data using jaratoolbox."""
        celldb_subset = celldb_full[
            (celldb_full.date == session.date) &
            (celldb_full.pdepth == session.depth)
        ]
        
        ensemble = ephyscore.CellEnsemble(celldb_subset)
        ephys_data, bdata = ensemble.load('optoTuningFreq')
        
        return celldb_subset, ephys_data, bdata, ensemble


# =============================================================================
# TUNING CURVE COMPUTATION (using jaratoolbox)
# =============================================================================

class TuningCurveComputer:
    """Computes tuning curves separated by laser condition."""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
    
    def compute_tuning_curves(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        ephys_data: dict,
        event_onset_times: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute tuning curves for laser OFF and ON.
        
        Returns:
            Tuple of (frequencies, rates_off, sem_off, rates_on, sem_on)
        """
        frequencies = bdata['currentFreq']
        laser_trials = bdata.get('laserTrial', np.zeros(len(frequencies), dtype=bool))
        laser_offset_times = ephys_data['events'].get('laserOff', None)
        
        unique_freqs = np.unique(frequencies)
        rates_off, sem_off = [], []
        rates_on, sem_on = [], []
        
        window_duration = self.config.response_window[1] - self.config.response_window[0]
        
        for freq in unique_freqs:
            # Laser OFF
            off_trials = np.where((frequencies == freq) & (laser_trials == 0))[0]
            if len(off_trials) > 0:
                rates = self._compute_rates(spike_times, trial_index, off_trials,
                                            None, None, window_duration)
                rates_off.append(np.mean(rates))
                sem_off.append(np.std(rates) / np.sqrt(len(rates)))
            else:
                rates_off.append(np.nan)
                sem_off.append(np.nan)
            
            # Laser ON
            on_trials = np.where((frequencies == freq) & (laser_trials == 1))[0]
            if len(on_trials) > 0:
                rates = self._compute_rates(spike_times, trial_index, on_trials,
                                            laser_offset_times, event_onset_times, window_duration)
                rates_on.append(np.mean(rates))
                sem_on.append(np.std(rates) / np.sqrt(len(rates)))
            else:
                rates_on.append(np.nan)
                sem_on.append(np.nan)
        
        return unique_freqs, np.array(rates_off), np.array(sem_off), np.array(rates_on), np.array(sem_on)
    
    def _compute_rates(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        trial_nums: np.ndarray,
        laser_offset_times: Optional[np.ndarray],
        event_onset_times: Optional[np.ndarray],
        window_duration: float
    ) -> np.ndarray:
        """Compute firing rates for given trials."""
        rates = []
        
        for trial_num in trial_nums:
            trial_spikes = spike_times[trial_index == trial_num]
            
            # Basic response window
            in_window = (
                (trial_spikes >= self.config.response_window[0]) &
                (trial_spikes < self.config.response_window[1])
            )
            
            # Exclude laser artifact if applicable
            if laser_offset_times is not None and event_onset_times is not None:
                if trial_num < len(laser_offset_times):
                    laser_offset_rel = laser_offset_times[trial_num] - event_onset_times[trial_num]
                    if not np.isnan(laser_offset_rel):
                        artifact_start = laser_offset_rel
                        artifact_end = laser_offset_rel + self.config.artifact_window
                        not_in_artifact = ~(
                            (trial_spikes >= artifact_start) &
                            (trial_spikes < artifact_end)
                        )
                        in_window = in_window & not_in_artifact
            
            spikes_in_window = np.sum(in_window)
            rates.append(spikes_in_window / window_duration)
        
        return np.array(rates)


# =============================================================================
# PLOTTING
# =============================================================================

class CombinedPlotter:
    """Plots tuning curve above raster for each cell."""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
        self.tuning_computer = TuningCurveComputer(config)
    
    def plot_cell_combined(
        self,
        gs: GridSpec,
        col_idx: int,
        cell_data: dict,
        session_data: dict
    ):
        """
        Plot tuning curve + raster for one cell.
        
        Args:
            gs: GridSpec for the page
            col_idx: Which column (0, 1, or 2)
            cell_data: Dict with cell metrics
            session_data: Dict with ephys data, bdata, etc.
        """
        # Create subplots: tuning curve (top) and raster (bottom)
        ax_tuning = plt.subplot(gs[0, col_idx])
        ax_raster = plt.subplot(gs[1, col_idx])
        
        # Plot tuning curve
        self._plot_tuning_curve(ax_tuning, cell_data, session_data)
        
        # Plot raster
        self._plot_raster(ax_raster, cell_data, session_data)
    
    def _plot_tuning_curve(
        self,
        ax: Axes,
        cell_data: dict,
        session_data: dict
    ):
        """Plot tuning curve (laser OFF vs ON)."""
        metrics_off = cell_data['metrics_off']
        metrics_on = cell_data['metrics_on']
        
        # Get spike data for this cell
        cell_idx = metrics_off.cell_idx
        spike_times = session_data['spike_times_all'][cell_idx]
        trial_index = session_data['trial_index_all'][cell_idx]
        
        # Compute tuning curves
        freqs, rates_off, sem_off, rates_on, sem_on = self.tuning_computer.compute_tuning_curves(
            spike_times, trial_index,
            session_data['bdata'],
            session_data['ephys_data'],
            session_data['event_onset_times']
        )
        
        # Plot
        freqs_khz = freqs / 1000.0
        x_pos = np.arange(len(freqs_khz))
        
        # Laser OFF (blue)
        ax.errorbar(x_pos, rates_off, yerr=sem_off,
                   marker='o', markersize=5, linewidth=2, capsize=3,
                   color='blue', markerfacecolor='blue',
                   markeredgecolor='black', markeredgewidth=0.5, alpha=0.8,
                   label='Laser OFF', linestyle='-')
        
        # Laser ON (red)
        valid_on = ~np.isnan(rates_on)
        if np.any(valid_on):
            ax.errorbar(x_pos, rates_on, yerr=sem_on,
                       marker='s', markersize=5, linewidth=2, capsize=3,
                       color='red', markerfacecolor='red',
                       markeredgecolor='black', markeredgewidth=0.5, alpha=0.8,
                       label='Laser ON', linestyle='--')
        
        # Mark best frequencies
        if metrics_off.best_freq in freqs:
            bf_idx = np.where(freqs == metrics_off.best_freq)[0][0]
            ax.plot(x_pos[bf_idx], rates_off[bf_idx],
                   marker='*', markersize=12, color='blue',
                   markeredgecolor='black', markeredgewidth=1, zorder=10)
        
        if metrics_on and metrics_on.best_freq in freqs:
            bf_idx = np.where(freqs == metrics_on.best_freq)[0][0]
            ax.plot(x_pos[bf_idx], rates_on[bf_idx],
                   marker='*', markersize=12, color='red',
                   markeredgecolor='black', markeredgewidth=1, zorder=10)
        
        # Format
        ax.set_ylabel('Firing Rate (Hz)', fontsize=9)
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'{f:.1f}' for f in freqs_khz], rotation=45, ha='right', fontsize=7)
        ax.set_xlim([-0.5, len(freqs_khz) - 0.5])
        ax.grid(True, alpha=0.2, axis='y')
        ax.legend(loc='upper right', fontsize=7, ncol=2)
        
        # Title with cell info and session label
        category = metrics_off.tuning_category.replace('_', ' ').title()
        session_label = cell_data.get('session_label', '')
        if session_label:
            ax.set_title(f"Cell {cell_idx} | {session_label} | {category}",
                        fontsize=8, fontweight='bold', pad=2)
        else:
            ax.set_title(f"Cell {cell_idx} | {category}",
                        fontsize=8, fontweight='bold', pad=2)
        
        # Add metrics text box ABOVE the plot (top-left corner)
        self._add_metrics_text(ax, metrics_off, metrics_on)
    
    @staticmethod
    def _add_metrics_text(
        ax: Axes,
        metrics_off: CellMetrics,
        metrics_on: Optional[CellMetrics]
    ):
        """Add comprehensive metrics text boxes above the plot in horizontal 3-column layout."""
        # Build text for each column separately
        
        # Column 1: LASER OFF
        text_off = (
            f"LASER OFF\n"
            f"Peak: {metrics_off.peak_rate:.1f} Hz\n"
            f"Mean: {metrics_off.mean_rate:.1f} Hz\n"
            f"SI: {metrics_off.selectivity_index:.3f}\n"
            f"Sp: {metrics_off.sparseness:.3f}\n"
            f"TQ: {metrics_off.tuning_quality:.2f}\n"
            f"CV: {metrics_off.coefficient_of_variation:.2f}"
        )
        if not np.isnan(metrics_off.bandwidth_octaves):
            text_off += f"\nBW: {metrics_off.bandwidth_octaves:.1f}oct"
        
        # Column 2: LASER ON
        if metrics_on is not None:
            text_on = (
                f"LASER ON\n"
                f"Peak: {metrics_on.peak_rate:.1f} Hz\n"
                f"Mean: {metrics_on.mean_rate:.1f} Hz\n"
                f"SI: {metrics_on.selectivity_index:.3f}\n"
                f"Sp: {metrics_on.sparseness:.3f}\n"
                f"TQ: {metrics_on.tuning_quality:.2f}\n"
                f"CV: {metrics_on.coefficient_of_variation:.2f}"
            )
            if not np.isnan(metrics_on.bandwidth_octaves):
                text_on += f"\nBW: {metrics_on.bandwidth_octaves:.1f}oct"
        else:
            text_on = "LASER ON\nNo data"
        
        # Column 3: LASER EFFECT
        if metrics_on is not None:
            pct_peak = ((metrics_on.peak_rate - metrics_off.peak_rate) * 100 / 
                       metrics_off.peak_rate) if metrics_off.peak_rate != 0 else 0
            pct_mean = ((metrics_on.mean_rate - metrics_off.mean_rate) * 100 / 
                       metrics_off.mean_rate) if metrics_off.mean_rate != 0 else 0
            
            delta_si = metrics_on.selectivity_index - metrics_off.selectivity_index
            delta_sp = metrics_on.sparseness - metrics_off.sparseness
            delta_tq = metrics_on.tuning_quality - metrics_off.tuning_quality
            delta_cv = metrics_on.coefficient_of_variation - metrics_off.coefficient_of_variation
            
            text_effect = (
                f"EFFECT\n"
                f"Peak: {pct_peak:+.0f}%\n"
                f"Mean: {pct_mean:+.0f}%\n"
                f"ΔSI: {delta_si:+.3f}\n"
                f"ΔSp: {delta_sp:+.3f}\n"
                f"ΔTQ: {delta_tq:+.2f}\n"
                f"ΔCV: {delta_cv:+.2f}"
            )
            
            if not np.isnan(metrics_off.bandwidth_octaves) and not np.isnan(metrics_on.bandwidth_octaves):
                delta_bw = metrics_on.bandwidth_octaves - metrics_off.bandwidth_octaves
                text_effect += f"\nΔBW: {delta_bw:+.1f}oct"
        else:
            text_effect = "EFFECT\nNo data"
        
        # Create 3 separate text boxes positioned horizontally
        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='wheat', 
                         alpha=0.85, edgecolor='black', linewidth=0.8)
        
        # Left box (LASER OFF) - moved down from 1.42 to 1.32
        ax.text(0.02, 1.32, text_off, transform=ax.transAxes,
               fontsize=7, verticalalignment='top', family='monospace',
               bbox=bbox_props, clip_on=False)
        
        # Middle box (LASER ON)
        ax.text(0.35, 1.32, text_on, transform=ax.transAxes,
               fontsize=7, verticalalignment='top', family='monospace',
               bbox=bbox_props, clip_on=False)
        
        # Right box (LASER EFFECT)
        ax.text(0.68, 1.32, text_effect, transform=ax.transAxes,
               fontsize=7, verticalalignment='top', family='monospace',
               bbox=bbox_props, clip_on=False)
    
    def _plot_raster(
        self,
        ax: Axes,
        cell_data: dict,
        session_data: dict
    ):
        """Plot raster sorted by frequency with laser OFF/ON comparison (IDENTICAL to arch018 raster script)."""
        metrics_off = cell_data['metrics_off']
        cell_idx = metrics_off.cell_idx
        
        # Get data
        spike_times = session_data['spike_times_all'][cell_idx]
        trial_index = session_data['trial_index_all'][cell_idx]
        index_limits = session_data['index_limits_all'][cell_idx]
        frequencies = session_data['bdata']['currentFreq']
        laser_trials = session_data['bdata'].get('laserTrial', np.zeros(len(frequencies), dtype=bool))
        
        # Get unique frequencies and trial organization
        unique_freqs = np.unique(frequencies)
        trials_each_freq = behavioranalysis.find_trials_each_type(frequencies, unique_freqs)
        
        # Separate trials by laser condition
        off_trials = np.flatnonzero(laser_trials == 0)
        on_trials = np.flatnonzero(laser_trials == 1)
        
        # Build trialsEachCond with laser grouping: [freq1_OFF, freq2_OFF, ..., freq1_ON, freq2_ON, ...]
        trials_each_cond_laser = []
        
        # OFF trials for each frequency
        for freq_idx in range(len(unique_freqs)):
            freq_trials = trials_each_freq[:, freq_idx]
            off_mask = freq_trials.copy()
            off_mask[on_trials] = False
            trials_each_cond_laser.append(off_mask)
        
        # ON trials for each frequency
        for freq_idx in range(len(unique_freqs)):
            freq_trials = trials_each_freq[:, freq_idx]
            on_mask = freq_trials.copy()
            on_mask[off_trials] = False
            trials_each_cond_laser.append(on_mask)
        
        trials_each_cond_laser = np.column_stack(trials_each_cond_laser)
        
        # Generate alternating colors for frequencies
        n_freqs = len(unique_freqs)
        color_each_cond = (['0.5', '0.75'] * int(np.ceil(n_freqs / 2.0)))[:n_freqs]
        # Repeat for laser ON conditions
        color_each_cond = color_each_cond + color_each_cond
        
        # Format frequency labels (kHz)
        freqs_khz = np.round(unique_freqs / 1000, 2)
        labels = [f'{fk}' for fk in freqs_khz]
        labels_laser = labels + labels  # Duplicate for OFF and ON
        
        # Use jaratoolbox's raster_plot (EXACT same as arch018 script)
        pRaster, hcond, zline = extraplots.raster_plot(
            spike_times, index_limits, self.config.time_range,
            trialsEachCond=trials_each_cond_laser, 
            colorEachCond=color_each_cond, 
            labels=labels_laser
        )
        plt.setp(pRaster, ms=1)  # Small marker size
        
        # Hide every other label to reduce clutter
        for i, label in enumerate(ax.get_yticklabels()):
            if i % 2 == 1:
                label.set_visible(False)
        
        # Add laser separator line (red dashed horizontal line)
        n_off = len(off_trials)
        n_on = len(on_trials)
        cumsum_trials = np.cumsum([trials_each_cond_laser[:, i].sum() for i in range(n_freqs)])
        laser_boundary = cumsum_trials[-1] - 0.5
        
        ax.axhline(laser_boundary, color='red', linewidth=2.5, linestyle='--', alpha=0.8, zorder=10)
        
        # Add laser OFF/ON labels on right side (minor ticks)
        total_trials = trials_each_cond_laser.sum()
        yticks_minor = [laser_boundary/2, laser_boundary + (total_trials - laser_boundary)/2]
        ax.set_yticks(yticks_minor, ['laser OFF', 'laser ON'], minor=True)
        ax.tick_params(axis='y', which='minor', left=False, right=True, 
                      labelleft=False, labelright=True, labelsize=8, pad=2)
        
        # Format axes
        ax.set_xlabel('Time (s)', fontsize=9)
        ax.set_ylabel('Frequency (kHz)', fontsize=9)
        ax.set_xlim(self.config.time_range)


# =============================================================================
# PDF GENERATION
# =============================================================================

class PDFGenerator:
    """Generates multi-page PDFs with combined plots."""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
        self.data_loader = DataLoader(config)
        self.plotter = CombinedPlotter(config)
    
    def create_combined_category_pdf(
        self,
        category: str,
        cells_data: List[dict],
        output_path: str,
        celldbs: Dict[str, pd.DataFrame]
    ):
        """Create PDF for one category with cells from all sessions combined."""
        if len(cells_data) == 0:
            return
        
        # Sort by tuning quality
        cells_data = sorted(cells_data, 
                          key=lambda x: x['metrics_off'].tuning_quality if not np.isnan(x['metrics_off'].tuning_quality) else -1,
                          reverse=True)
        
        n_cells = len(cells_data)
        n_pages = int(np.ceil(n_cells / self.config.cells_per_page))
        
        # Group cells by session to load session data efficiently
        cells_by_session = {}
        for cell_data in cells_data:
            session_id = cell_data['session_id']
            if session_id not in cells_by_session:
                cells_by_session[session_id] = []
            cells_by_session[session_id].append(cell_data)
        
        # Pre-load all session data
        session_data_cache = {}
        for session_id in cells_by_session.keys():
            session = SESSIONS[session_id]
            session_data_cache[session_id] = self._load_session_data(session, celldbs)
        
        with PdfPages(output_path) as pdf:
            for page_idx in range(n_pages):
                self._create_combined_page(pdf, page_idx, n_pages, cells_data, 
                                          session_data_cache, category)
        
        print(f"    Saved: {output_path}")
    
    def _create_combined_page(
        self,
        pdf: PdfPages,
        page_idx: int,
        n_pages: int,
        cells_data: List[dict],
        session_data_cache: Dict[int, dict],
        category: str
    ):
        """Create one page with 3 cells from potentially different sessions."""
        start_idx = page_idx * self.config.cells_per_page
        end_idx = min(start_idx + self.config.cells_per_page, len(cells_data))
        cells_this_page = cells_data[start_idx:end_idx]
        
        # Create figure with GridSpec
        fig = plt.figure(figsize=(self.config.fig_width, self.config.fig_height))
        gs = GridSpec(2, 3, figure=fig, height_ratios=[1, 1.5], 
                     hspace=0.1, wspace=0.3, top=0.88, bottom=0.08)
        
        # Plot each cell (may be from different sessions)
        for col_idx, cell_data in enumerate(cells_this_page):
            session_id = cell_data['session_id']
            session_data = session_data_cache[session_id]
            session = cell_data['session']
            
            # Add session info to cell title
            cell_data_with_session = cell_data.copy()
            cell_data_with_session['session_label'] = f"{session.subject} {session.date} {session.depth}µm"
            
            self.plotter.plot_cell_combined(gs, col_idx, cell_data_with_session, session_data)
        
        # Overall title
        category_display = category.replace('_', ' ').title()
        fig.suptitle(
            f'All Sessions | {category_display} Cells | Page {page_idx + 1}/{n_pages} (Tuning Curves + Rasters)',
            fontsize=12, fontweight='bold', y=1
        )
        
        pdf.savefig(fig, dpi=150, bbox_inches='tight')
        plt.close(fig)
    
    def create_category_pdf(
        self,
        category: str,
        cells_data: List[dict],
        session: SessionConfig,
        output_path: str,
        celldbs: Dict[str, pd.DataFrame]
    ):
        """Create PDF for one category."""
        if len(cells_data) == 0:
            return
        
        # Sort by tuning quality
        cells_data = sorted(cells_data, 
                          key=lambda x: x['metrics_off'].tuning_quality if not np.isnan(x['metrics_off'].tuning_quality) else -1,
                          reverse=True)
        
        n_cells = len(cells_data)
        n_pages = int(np.ceil(n_cells / self.config.cells_per_page))
        
        # Load session data once
        session_data = self._load_session_data(session, celldbs)
        
        with PdfPages(output_path) as pdf:
            for page_idx in range(n_pages):
                self._create_page(pdf, page_idx, n_pages, cells_data, session_data, session, category)
        
        print(f"    Saved: {output_path}")
    
    def _load_session_data(
        self,
        session: SessionConfig,
        celldbs: Dict[str, pd.DataFrame]
    ) -> dict:
        """Load session ephys data."""
        celldb_full = celldbs[session.subject]
        _, ephys_data, bdata, ensemble = self.data_loader.load_session_data(session, celldb_full)
        
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
            'index_limits_all': index_limits_all  # Add this for extraplots.raster_plot
        }
    
    def _create_page(
        self,
        pdf: PdfPages,
        page_idx: int,
        n_pages: int,
        cells_data: List[dict],
        session_data: dict,
        session: SessionConfig,
        category: str
    ):
        """Create one page with 3 cells."""
        start_idx = page_idx * self.config.cells_per_page
        end_idx = min(start_idx + self.config.cells_per_page, len(cells_data))
        cells_this_page = cells_data[start_idx:end_idx]
        
        # Create figure with GridSpec
        fig = plt.figure(figsize=(self.config.fig_width, self.config.fig_height))
        # Reduced hspace to bring plots closer together
        # Increased top margin to make room for title at very top
        gs = GridSpec(2, 3, figure=fig, height_ratios=[1, 1.5], 
                     hspace=0.1, wspace=0.3, top=0.88, bottom=0.08)
        
        # Plot each cell
        for col_idx, cell_data in enumerate(cells_this_page):
            self.plotter.plot_cell_combined(gs, col_idx, cell_data, session_data)
        
        # Overall title at the VERY TOP of the page
        category_display = category.replace('_', ' ').title()
        fig.suptitle(
            f'{session.subject} {session.date} {session.depth}µm | {category_display} Cells | '
            f'Page {page_idx + 1}/{n_pages} (Tuning Curves + Rasters)',
            fontsize=11, fontweight='bold', y=1
        )
        
        pdf.savefig(fig, dpi=150, bbox_inches='tight')
        plt.close(fig)


# =============================================================================
# MAIN COORDINATOR
# =============================================================================

class CombinedVisualizationCoordinator:
    """Coordinates the entire visualization pipeline."""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
        self.data_loader = DataLoader(config)
        self.pdf_generator = PDFGenerator(config)
        self.output_dir = os.path.join(config.metrics_dir, 'tuning_with_rasters')
    
    def run(self):
        """Execute complete visualization pipeline."""
        print("="*70)
        print("COMBINED TUNING CURVE + RASTER VISUALIZATION")
        print("="*70)
        
        # Load data
        df_merged = self.data_loader.load_metrics()
        celldbs = self.data_loader.load_celldbs(SESSIONS)
        
        # Organize cells
        cells_by_session_category = self._organize_cells(df_merged)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate PDFs
        self._generate_pdfs(cells_by_session_category, celldbs)
        
        print(f"\n✓ PDFs saved to: {self.output_dir}")
    
    def _organize_cells(self, df_merged: pd.DataFrame) -> Dict[str, List[dict]]:
        """Organize cells by category only (no session separation)."""
        cells_by_category = {'tuned': [], 'non_tuned': []}
        
        for _, row in df_merged.iterrows():
            session_id = int(row['session_id'])
            category = row['tuning_category_off']
            
            if category not in ['tuned', 'non_tuned']:
                continue
            
            # Get session info for later use
            session = SESSIONS.get(session_id)
            if session is None:
                continue
            
            metrics_off = CellMetrics(
                cell_idx=int(row['cell_idx']),
                best_freq=row['best_freq_off'],
                peak_rate=row['peak_rate_off'],
                mean_rate=row['mean_rate_off'],
                selectivity_index=row['selectivity_index_off'],
                sparseness=row['sparseness_off'],
                tuning_quality=row['tuning_quality_off'],
                bandwidth_octaves=row['bandwidth_octaves_off'],
                coefficient_of_variation=row.get('coefficient_of_variation_off', np.nan),
                tuning_category=category
            )
            
            metrics_on = None
            if not pd.isna(row['peak_rate_on']):
                metrics_on = CellMetrics(
                    cell_idx=int(row['cell_idx']),
                    best_freq=row['best_freq_on'],
                    peak_rate=row['peak_rate_on'],
                    mean_rate=row['mean_rate_on'],
                    selectivity_index=row['selectivity_index_on'],
                    sparseness=row['sparseness_on'],
                    tuning_quality=row['tuning_quality_on'],
                    bandwidth_octaves=row['bandwidth_octaves_on'],
                    coefficient_of_variation=row.get('coefficient_of_variation_on', np.nan),
                    tuning_category=''
                )
            
            cells_by_category[category].append({
                'metrics_off': metrics_off,
                'metrics_on': metrics_on,
                'session_id': session_id,
                'session': session
            })
        
        return cells_by_category
    
    def _generate_pdfs(
        self,
        cells_by_category: Dict[str, List[dict]],
        celldbs: Dict[str, pd.DataFrame]
    ):
        """Generate PDFs for each category (all sessions combined)."""
        for category in ['tuned', 'non_tuned']:
            cells_data = cells_by_category[category]
            
            if len(cells_data) == 0:
                print(f"\n{category.replace('_', ' ').title()}: No cells found")
                continue
            
            print(f"\n{category.replace('_', ' ').title()}: {len(cells_data)} cells across all sessions")
            
            output_path = os.path.join(self.output_dir, f'{category}_cells_with_rasters_all_sessions.pdf')
            self.pdf_generator.create_combined_category_pdf(
                category, cells_data, output_path, celldbs
            )


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main execution."""
    config = VisualizationConfig()
    coordinator = CombinedVisualizationCoordinator(config)
    
    try:
        coordinator.run()
        return 0
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
