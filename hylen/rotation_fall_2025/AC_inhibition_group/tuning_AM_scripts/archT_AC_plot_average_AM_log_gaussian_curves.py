"""
Plot Average AM Tuning Curves: Population-Level Analysis

This script creates averaged AM tuning curves across multiple cells by:
1. Normalizing each cell's tuning curve (peak normalization: 0-1)
2. Aligning each cell to its best AM rate (center at 0 octaves)
3. Averaging across cells at each octave position
4. Plotting with SEM error bars

Outputs:
- PDF: Average tuning curves (OFF vs ON on same plot)
- CSV: Averaged data for future plotting

Two datasets analyzed:
1. Good Fits: Cells with high R² (≥ 0.4)
2. Empirically Tuned: All cells classified as tuned

Author: Hylen
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import interpolate
from dataclasses import dataclass
from typing import Tuple, List, Dict

# Add hylen directory to path
sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class AverageConfig:
    """Configuration for average tuning curve analysis."""
    # Experiment identification
    experiment_name: str = 'AC - pStr Inhibition with AM'
    
    # Analysis parameters
    r_squared_threshold: float = 0.4  # For "good fits" group
    
    # Octave range for aligned curves (relative to best rate)
    octave_range: Tuple[float, float] = (-2.5, 2.5)  # ±2.5 octaves from best
    octave_resolution: float = 0.25  # Sample every 0.25 octaves
    
    # Plotting style
    fig_width: float = 14
    fig_height: float = 10
    line_width: float = 3
    error_alpha: float = 0.2
    
    # Use centralized config for directories
    @property
    def gaussian_fits_dir(self) -> str:
        """Get Gaussian fits directory from config."""
        return str(get_reports_subdir('tuning_AM_gaussian_fits'))
    
    @property
    def metrics_dir(self) -> str:
        """Get metrics directory from config."""
        return str(get_reports_subdir('tuning_AM_analysis'))
    
    @property
    def output_dir(self) -> str:
        """Get output directory from config."""
        return str(get_reports_subdir('tuning_AM_average_curves'))


# =============================================================================
# DATA LOADING
# =============================================================================

class AMTuningDataLoader:
    """Loads and processes AM tuning data for averaging."""
    
    def __init__(self, config: AverageConfig):
        self.config = config
    
    def load_all_sessions(self, laser_condition: str) -> pd.DataFrame:
        """Load all session fits for a laser condition."""
        combined_path = os.path.join(
            self.config.gaussian_fits_dir,
            f'all_sessions_laser_{laser_condition}_log_gaussian_fits.csv'
        )
        
        if not os.path.exists(combined_path):
            raise FileNotFoundError(f"Combined fits not found: {combined_path}")
        
        return pd.read_csv(combined_path)
    
    def load_tuning_curves_for_cell(
        self, 
        session_id: int, 
        cell_idx: int, 
        laser_condition: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Load the actual tuning curve data for a specific cell."""
        metrics_path = os.path.join(
            self.config.metrics_dir,
            f'session_{session_id}_laser_{laser_condition}_tuning_metrics.csv'
        )
        
        if not os.path.exists(metrics_path):
            return np.array([]), np.array([])
        
        df = pd.read_csv(metrics_path)
        cell_row = df[df['cell_idx'] == cell_idx]
        
        if len(cell_row) == 0:
            return np.array([]), np.array([])
        
        row = cell_row.iloc[0]
        
        # Parse tuning curve
        rate_str = str(row.get('tuning_rates_am', ''))
        response_str = str(row.get('tuning_responses', ''))
        
        if rate_str == '' or rate_str == 'nan':
            return np.array([]), np.array([])
        
        rates = np.array([float(r) for r in rate_str.split(',')])
        
        responses = []
        for r in response_str.split(','):
            if r.strip().lower() == 'nan' or r.strip() == '':
                responses.append(np.nan)
            else:
                responses.append(float(r))
        responses = np.array(responses)
        
        return rates, responses


# =============================================================================
# NORMALIZATION & ALIGNMENT
# =============================================================================

class TuningCurveNormalizer:
    """Normalizes and aligns tuning curves to best rate."""
    
    def __init__(self, config: AverageConfig):
        self.config = config
    
    def normalize_and_align(
        self,
        am_rates: np.ndarray,
        firing_rates: np.ndarray,
        best_rate: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Normalize curve (peak = 1, baseline = 0) and align to best rate.
        
        Args:
            am_rates: AM rates in Hz
            firing_rates: Firing rates (spikes/s)
            best_rate: Best AM rate for this cell (Hz)
        
        Returns:
            Tuple of (octaves_from_best, normalized_rates)
        """
        # Remove NaN values
        valid_mask = ~np.isnan(firing_rates)
        rates_valid = am_rates[valid_mask]
        responses_valid = firing_rates[valid_mask]
        
        if len(rates_valid) == 0:
            return np.array([]), np.array([])
        
        # Peak normalization: (response - min) / (max - min)
        min_response = np.min(responses_valid)
        max_response = np.max(responses_valid)
        
        if max_response - min_response < 0.1:  # Avoid division by near-zero
            return np.array([]), np.array([])
        
        normalized = (responses_valid - min_response) / (max_response - min_response)
        
        # Convert to octaves from best rate
        octaves = np.log2(rates_valid / best_rate)
        
        return octaves, normalized
    
    def interpolate_to_grid(
        self,
        octaves: np.ndarray,
        normalized_rates: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Interpolate curve onto common octave grid.
        
        Args:
            octaves: Octaves from best rate
            normalized_rates: Normalized firing rates (0-1)
        
        Returns:
            Tuple of (grid_octaves, interpolated_rates)
        """
        # Create common grid
        grid_octaves = np.arange(
            self.config.octave_range[0],
            self.config.octave_range[1] + self.config.octave_resolution,
            self.config.octave_resolution
        )
        
        # Only interpolate within the data range
        min_octave = np.min(octaves)
        max_octave = np.max(octaves)
        
        # Create interpolator (linear)
        interpolator = interpolate.interp1d(
            octaves, normalized_rates,
            kind='linear',
            bounds_error=False,
            fill_value=np.nan
        )
        
        # Interpolate onto grid
        interpolated = interpolator(grid_octaves)
        
        # Mask values outside data range
        mask = (grid_octaves < min_octave) | (grid_octaves > max_octave)
        interpolated[mask] = np.nan
        
        return grid_octaves, interpolated


# =============================================================================
# AVERAGING & PLOTTING
# =============================================================================

class AverageTuningPlotter:
    """Creates average tuning curve plots."""
    
    def __init__(self, config: AverageConfig):
        self.config = config
        self.loader = AMTuningDataLoader(config)
        self.normalizer = TuningCurveNormalizer(config)
    
    def create_average_curves(
        self,
        group_name: str,
        filter_func
    ):
        """
        Create average tuning curves for a group of cells.
        
        Args:
            group_name: Name of the group (e.g., "Good Fits")
            filter_func: Function to filter cells (e.g., lambda df: df['r_squared'] >= 0.4)
        """
        print(f"\n{'='*70}")
        print(f"CREATING AVERAGE CURVES: {group_name}")
        print(f"{'='*70}")
        
        # Load data
        df_off = self.loader.load_all_sessions('off')
        df_on = self.loader.load_all_sessions('on')
        
        # Filter cells
        df_off_filtered = filter_func(df_off)
        df_on_filtered = filter_func(df_on)
        
        # CRITICAL: Only keep PAIRED cells (cells with both OFF and ON that pass filter)
        # Match by session_id and cell_idx
        df_off_filtered['cell_key'] = df_off_filtered['session_id'].astype(str) + '_' + df_off_filtered['cell_idx'].astype(str)
        df_on_filtered['cell_key'] = df_on_filtered['session_id'].astype(str) + '_' + df_on_filtered['cell_idx'].astype(str)
        
        # Find intersection
        common_cells = set(df_off_filtered['cell_key']) & set(df_on_filtered['cell_key'])
        
        # Keep only common cells
        df_off_paired = df_off_filtered[df_off_filtered['cell_key'].isin(common_cells)].copy()
        df_on_paired = df_on_filtered[df_on_filtered['cell_key'].isin(common_cells)].copy()
        
        print(f"  Before pairing - OFF: {len(df_off_filtered)}, ON: {len(df_on_filtered)}")
        print(f"  After pairing - OFF: {len(df_off_paired)}, ON: {len(df_on_paired)} (MATCHED)")
        
        if len(df_off_paired) == 0:
            print(f"  WARNING: No paired cells found for {group_name}!")
            return
        
        # Process each condition (USE PAIRED DATA ONLY)
        grid_octaves_off, all_curves_off = self._process_condition(df_off_paired, 'off')
        grid_octaves_on, all_curves_on = self._process_condition(df_on_paired, 'on')
        
        # Calculate averages
        mean_off = np.nanmean(all_curves_off, axis=0)
        sem_off = np.nanstd(all_curves_off, axis=0) / np.sqrt(np.sum(~np.isnan(all_curves_off), axis=0))
        
        mean_on = np.nanmean(all_curves_on, axis=0)
        sem_on = np.nanstd(all_curves_on, axis=0) / np.sqrt(np.sum(~np.isnan(all_curves_on), axis=0))
        
        # Create plot (n should be the same for both)
        n_paired = len(df_off_paired)
        self._plot_average_curves(
            grid_octaves_off, mean_off, sem_off,
            grid_octaves_on, mean_on, sem_on,
            group_name, n_paired
        )
        
        # Save CSV
        self._save_csv(grid_octaves_off, mean_off, sem_off, mean_on, sem_on, group_name)
    
    def _process_condition(self, df: pd.DataFrame, laser_condition: str) -> Tuple[np.ndarray, np.ndarray]:
        """Process all cells for one condition."""
        print(f"  Processing {laser_condition.upper()} condition...")
        
        all_curves = []
        grid_octaves = None
        
        for idx, row in df.iterrows():
            session_id = int(row['session_id'])
            cell_idx = int(row['cell_idx'])
            best_rate = row['empirical_best_rate']
            
            # Load tuning curve
            am_rates, firing_rates = self.loader.load_tuning_curves_for_cell(
                session_id, cell_idx, laser_condition
            )
            
            if len(am_rates) == 0:
                continue
            
            # Normalize and align
            octaves, normalized = self.normalizer.normalize_and_align(
                am_rates, firing_rates, best_rate
            )
            
            if len(octaves) == 0:
                continue
            
            # Interpolate onto grid
            grid_oct, interpolated = self.normalizer.interpolate_to_grid(octaves, normalized)
            
            if grid_octaves is None:
                grid_octaves = grid_oct
            
            all_curves.append(interpolated)
        
        # Convert to array
        all_curves_array = np.array(all_curves)
        
        print(f"    Successfully processed {len(all_curves)} cells")
        
        return grid_octaves, all_curves_array
    
    def _plot_average_curves(
        self,
        octaves_off: np.ndarray,
        mean_off: np.ndarray,
        sem_off: np.ndarray,
        octaves_on: np.ndarray,
        mean_on: np.ndarray,
        sem_on: np.ndarray,
        group_name: str,
        n_paired: int
    ):
        """Create the average tuning curve plot."""
        fig, ax = plt.subplots(figsize=(self.config.fig_width, self.config.fig_height))
        
        # Plot OFF
        ax.plot(octaves_off, mean_off, '-', color='blue', linewidth=self.config.line_width,
               label=f'Laser OFF', zorder=3)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                        color='blue', alpha=self.config.error_alpha, zorder=1)
        
        # Plot ON
        ax.plot(octaves_on, mean_on, '-', color='red', linewidth=self.config.line_width,
               label=f'Laser ON', zorder=3)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                        color='red', alpha=self.config.error_alpha, zorder=1)
        
        # Formatting
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Best Rate')
        ax.axhline(0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        ax.axhline(1, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        
        ax.set_xlabel('Octaves from Best AM Rate', fontsize=14, fontweight='bold')
        ax.set_ylabel('Normalized Response (0-1)', fontsize=14, fontweight='bold')
        ax.set_title(f'{self.config.experiment_name}\nAverage AM Tuning Curves: {group_name}\n(n={n_paired} paired cells)',
                    fontsize=16, fontweight='bold')
        
        ax.legend(loc='best', fontsize=12, frameon=True, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([-0.1, 1.1])
        ax.set_xlim([self.config.octave_range[0], self.config.octave_range[1]])
        
        plt.tight_layout()
        
        # Save
        pdf_path = os.path.join(
            self.config.output_dir,
            f'average_AM_tuning_{group_name.replace(" ", "_").lower()}.pdf'
        )
        plt.savefig(pdf_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved plot: {pdf_path}")
    
    def _save_csv(
        self,
        octaves: np.ndarray,
        mean_off: np.ndarray,
        sem_off: np.ndarray,
        mean_on: np.ndarray,
        sem_on: np.ndarray,
        group_name: str
    ):
        """Save averaged data to CSV."""
        df = pd.DataFrame({
            'octaves_from_best': octaves,
            'mean_off': mean_off,
            'sem_off': sem_off,
            'mean_on': mean_on,
            'sem_on': sem_on
        })
        
        csv_path = os.path.join(
            self.config.output_dir,
            f'average_AM_tuning_{group_name.replace(" ", "_").lower()}.csv'
        )
        df.to_csv(csv_path, index=False)
        
        print(f"  Saved CSV: {csv_path}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution."""
    print("="*70)
    print("AVERAGE AM TUNING CURVES")
    print("="*70)
    
    config = AverageConfig()
    
    # Create output directory using config property
    os.makedirs(config.output_dir, exist_ok=True)
    
    plotter = AverageTuningPlotter(config)
    
    # Group 1: Good fits (R² ≥ 0.4)
    plotter.create_average_curves(
        "Good Fits",
        lambda df: df[df['r_squared'] >= config.r_squared_threshold]
    )
    
    # Group 2: Empirically tuned (need to load from metrics)
    # For this, we'll filter based on cells that exist in the fits
    # (assumes all fitted cells were empirically tuned)
    plotter.create_average_curves(
        "Empirically Tuned",
        lambda df: df  # All cells that were fitted
    )
    
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)


if __name__ == '__main__':
    main()
