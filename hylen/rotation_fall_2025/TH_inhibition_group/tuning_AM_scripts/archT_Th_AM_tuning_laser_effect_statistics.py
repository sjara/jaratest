"""
Statistical comparison of AM tuning metrics between laser OFF and laser ON conditions.

This script performs comprehensive statistical analysis comparing AM rate tuning metrics
between laser OFF and laser ON conditions for tuned cells only.

Features:
- Reads pre-computed metrics from CSV files (no recomputation needed)
- Uses complete cases for selectivity and sparseness (bandwidth can be NaN)
- Performs paired Wilcoxon signed-rank tests
- Generates comprehensive comparison plots and statistical summaries
- Loads cell databases only once per subject (for example tuning curves)

Metrics Compared:
- Selectivity Index
- Sparseness
- Bandwidth (octaves)
- Tuning Quality
- Peak response (firing rate at best AM rate)
- Mean response (mean firing rate across all AM rates)

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
from matplotlib.figure import Figure
from scipy import stats
from contextlib import contextmanager

from jaratoolbox import settings, celldatabase, ephyscore

sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


# =============================================================================
# DATA STRUCTURES
# =============================================================================

class TuningCurveData(NamedTuple):
    """Container for single-cell tuning curve data."""
    frequencies: np.ndarray
    mean_rates: np.ndarray
    sem_rates: np.ndarray
    best_freq: float


class NormalizedTuningData(NamedTuple):
    """Container for population-normalized tuning curve data."""
    octave_bins: np.ndarray
    mean_rates_off: np.ndarray
    sem_rates_off: np.ndarray
    n_cells_off: np.ndarray
    mean_rates_on: np.ndarray
    sem_rates_on: np.ndarray
    n_cells_on: np.ndarray
    mean_rates_off_normalized: np.ndarray
    sem_rates_off_normalized: np.ndarray
    mean_rates_on_normalized: np.ndarray
    sem_rates_on_normalized: np.ndarray


# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

@dataclass(frozen=True)
class SessionConfig:
    """Recording session configuration (immutable)."""
    subject: str
    date: str
    depth: int


@dataclass(frozen=True)
class AnalysisConfig:
    """Statistical analysis configuration (immutable)."""
    time_range: Tuple[float, float] = (-0.5, 1.0)
    response_window: Tuple[float, float] = (0.005, 0.495)  # Longer window for AM analysis
    tuned_categories: List[str] = None
    min_cells_for_stats: int = 3
    
    # Effect size thresholds for biological significance
    min_effect_size_cohens_d: float = 0.3  # Small-to-medium effect (Cohen's d >= 0.3)
    min_percent_change: float = 10.0  # Minimum 10% change from baseline
    
    @property
    def metrics_dir(self) -> str:
        return str(get_reports_subdir('arch024/tuning_AM_analysis'))

    @property
    def override_file(self) -> str:
        return os.path.join(self.metrics_dir, 'classification_overrides.csv')
    
    def __post_init__(self):
        """Set default tuned categories."""
        if self.tuned_categories is None:
            object.__setattr__(self, 'tuned_categories', ['tuned'])


class StatisticalResult(NamedTuple):
    """Container for statistical test results."""
    metric: str
    n_cells: int
    mean_off: float
    median_off: float
    std_off: float
    sem_off: float
    mean_on: float
    median_on: float
    std_on: float
    sem_on: float
    mean_diff: float
    median_diff: float
    percent_change: float  # Percent change from OFF to ON
    wilcoxon_statistic: float
    wilcoxon_pvalue: float
    cohens_d: float
    is_biologically_significant: bool  # True if meets effect size criteria


# All available sessions
SESSIONS = {
    0: SessionConfig('arch024', '2025-04-10', 2780),
    1: SessionConfig('arch024', '2025-04-10', 3500),
    2: SessionConfig('arch024', '2025-04-15', 2780),
    3: SessionConfig('arch024', '2025-04-15', 3500),
    4: SessionConfig('arch024', '2025-04-16', 2780),
    5: SessionConfig('arch024', '2025-04-16', 3500),
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

@contextmanager
def figure_context(save_path: Optional[str] = None, **fig_kwargs):
    """Context manager for creating and saving figures with automatic cleanup."""
    fig = plt.figure(**fig_kwargs)
    try:
        yield fig
    finally:
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)


def format_pvalue(p_val: float) -> str:
    """Format p-value with appropriate precision."""
    if p_val < 0.001:
        return f"{p_val:.2e}"
    else:
        return f"{p_val:.4f}"


def get_significance_label(p_val: float) -> str:
    """Get significance label (*, **, ***, or n.s.)."""
    if p_val < 0.001:
        return '***'
    elif p_val < 0.01:
        return '**'
    elif p_val < 0.05:
        return '*'
    else:
        return 'n.s.'


def get_significance_color(p_val: float) -> str:
    """Get color based on significance level."""
    if p_val < 0.001:
        return 'red'
    elif p_val < 0.01:
        return 'orange'
    elif p_val < 0.05:
        return 'yellow'
    else:
        return 'lightgray'


# =============================================================================
# DATA LOADING MODULE
# =============================================================================

class MetricsLoader:
    """Handles loading of pre-computed tuning metrics from CSV files."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def load_metrics(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load laser OFF and laser ON metrics from CSV files.
        
        Returns:
            Tuple of (df_off, df_on)
        
        Raises:
            FileNotFoundError: If CSV files are missing
        """
        csv_off = os.path.join(
            self.config.metrics_dir,
            'all_sessions_laser_off_tuning_metrics.csv'
        )
        csv_on = os.path.join(
            self.config.metrics_dir,
            'all_sessions_laser_on_tuning_metrics.csv'
        )
        
        if not os.path.exists(csv_off):
            raise FileNotFoundError(
                f"Laser OFF metrics not found: {csv_off}\n"
                "Please run calculate_AM_tuning.py first!"
            )
        
        if not os.path.exists(csv_on):
            raise FileNotFoundError(
                f"Laser ON metrics not found: {csv_on}\n"
                "Please run calculate_AM_tuning.py first!"
            )
        
        print(f"\nLoading laser OFF metrics from:\n  {csv_off}")
        df_off = pd.read_csv(csv_off)
        
        print(f"Loading laser ON metrics from:\n  {csv_on}")
        df_on = pd.read_csv(csv_on)
        
        # Apply classification overrides
        df_off = self._apply_overrides(df_off)
        
        return df_off, df_on
    
    def _apply_overrides(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply manual classification overrides from CSV file."""
        if not os.path.exists(self.config.override_file):
            return df
        
        try:
            df_overrides = pd.read_csv(self.config.override_file, comment='#')
            
            # Skip if file is empty or only has headers
            if len(df_overrides) == 0:
                return df
            
            # Validate required columns
            required_cols = ['session_id', 'cell_idx', 'override_category']
            if not all(col in df_overrides.columns for col in required_cols):
                print(f"  WARNING: Override file missing required columns")
                return df
            
            n_overridden = 0
            for _, override_row in df_overrides.iterrows():
                try:
                    session_id = int(override_row['session_id'])
                    cell_idx = int(override_row['cell_idx'])
                    new_category = str(override_row['override_category']).strip().lower()
                    
                    # Find matching cell in dataframe
                    mask = (df['session_id'] == session_id) & (df['cell_idx'] == cell_idx)
                    
                    if mask.any():
                        old_category = df.loc[mask, 'tuning_category'].iloc[0]
                        df.loc[mask, 'tuning_category'] = new_category
                        n_overridden += 1
                        print(f"  Override applied: Session {session_id}, Cell {cell_idx}: "
                              f"{old_category} → {new_category}")
                except (ValueError, KeyError) as e:
                    # Skip rows that can't be parsed (e.g., example rows)
                    continue
            
            if n_overridden > 0:
                print(f"\n  ✓ Applied {n_overridden} classification overrides to laser OFF data")
            
        except Exception as e:
            print(f"  WARNING: Failed to apply overrides: {e}")
        
        return df
    
    def filter_tuned_cells(self, df_off: pd.DataFrame) -> pd.DataFrame:
        """Filter to include only tuned cells based on laser OFF classification."""
        df_tuned = df_off[df_off['tuning_category'].isin(self.config.tuned_categories)]
        
        print(f"\nLaser OFF - Total analyzed cells: {len(df_off)}")
        print(f"Laser OFF - Tuned cells: {len(df_tuned)}")
        
        if len(df_tuned) == 0:
            raise ValueError("No tuned cells found in laser OFF data!")
        
        return df_tuned


class CellDatabaseLoader:
    """Handles loading and caching of cell databases (for example plots only)."""
    
    @staticmethod
    def load_all(sessions: Dict[int, SessionConfig]) -> Dict[str, pd.DataFrame]:
        """Load cell databases for all unique subjects."""
        print("\nLoading cell databases for all subjects...")
        
        subjects = list(set(session.subject for session in sessions.values()))
        celldbs = {}
        
        for subject in subjects:
            inforec_file = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
            print(f"  Loading {subject}...")
            celldbs[subject] = celldatabase.generate_cell_database(
                inforec_file, ignoreMissing=True
            )
        
        print(f"Loaded cell databases for {len(celldbs)} subjects\n")
        return celldbs


# =============================================================================
# DATA PROCESSING MODULE
# =============================================================================

class DataMerger:
    """Handles merging and filtering of laser OFF and ON data."""
    
    @staticmethod
    def merge_conditions(
        df_off: pd.DataFrame,
        df_on: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge laser OFF and ON data on session_id and cell_idx.
        
        Uses LEFT join to include all cells with laser OFF data,
        even if they show complete suppression during laser ON.
        
        Returns:
            Merged DataFrame with renamed columns
        """
        print(f"\n{'='*70}")
        print("MERGING LASER OFF AND ON DATA")
        print(f"{'='*70}")
        
        # Select and rename columns from laser OFF
        cols_off = ['session_id', 'cell_idx', 'tuning_category', 'subject', 'date', 'depth',
                    'peak_response', 'mean_response', 'selectivity_index', 'sparseness',
                    'tuning_quality', 'bandwidth_octaves']
        
        # Add optional columns if they exist
        if 'stimulus_evoked_change' in df_off.columns:
            cols_off.append('stimulus_evoked_change')
        if 'fano_factor' in df_off.columns:
            cols_off.append('fano_factor')
        
        df_off_renamed = df_off[cols_off].rename(columns={
            'peak_response': 'peak_response_off',
            'mean_response': 'mean_response_off',
            'selectivity_index': 'selectivity_off',
            'sparseness': 'sparseness_off',
            'tuning_quality': 'tuning_quality_off',
            'bandwidth_octaves': 'bandwidth_off',
            'stimulus_evoked_change': 'stimulus_evoked_change_off',
            'fano_factor': 'fano_factor_off'
        })
        
        # Select and rename columns from laser ON
        cols_on = ['session_id', 'cell_idx', 'peak_response', 'mean_response',
                   'selectivity_index', 'sparseness', 'tuning_quality', 'bandwidth_octaves']
        
        # Add optional columns if they exist
        if 'stimulus_evoked_change' in df_on.columns:
            cols_on.append('stimulus_evoked_change')
        if 'fano_factor' in df_on.columns:
            cols_on.append('fano_factor')
        
        df_on_renamed = df_on[cols_on].rename(columns={
            'peak_response': 'peak_response_on',
            'mean_response': 'mean_response_on',
            'selectivity_index': 'selectivity_on',
            'sparseness': 'sparseness_on',
            'tuning_quality': 'tuning_quality_on',
            'bandwidth_octaves': 'bandwidth_on',
            'stimulus_evoked_change': 'stimulus_evoked_change_on',
            'fano_factor': 'fano_factor_on'
        })
        
        # Merge with LEFT join to keep all cells with laser OFF data
        df_merged = pd.merge(
            df_off_renamed, df_on_renamed,
            on=['session_id', 'cell_idx'],
            how='left'  # Keep ALL laser OFF cells, even if laser ON has no/NaN metrics
        )
        
        # For cells with missing laser ON data, fill firing rates with 0 (complete suppression)
        # but leave other metrics (SI, sparseness, etc.) as NaN since they're undefined for zero firing
        print(f"\n  Laser OFF cells: {len(df_off)}")
        print(f"  Laser ON cells: {len(df_on)}")
        print(f"  Merged cells: {len(df_merged)}")
        
        # Check for cells missing laser ON data
        missing_on_data = df_merged['peak_response_on'].isna()
        n_missing = missing_on_data.sum()
        
        if n_missing > 0:
            print(f"\n  ⚠ {n_missing} cell(s) have no laser ON data:")
            for idx in df_merged[missing_on_data].index:
                row = df_merged.loc[idx]
                session_id = int(row['session_id'])
                cell_idx = int(row['cell_idx'])
                print(f"    Session {session_id}, Cell {cell_idx} - treating as complete suppression")
            
            # Fill missing laser ON firing rates with 0 (complete suppression)
            df_merged.loc[missing_on_data, 'peak_response_on'] = 0.0
            df_merged.loc[missing_on_data, 'mean_response_on'] = 0.0
            
            # Leave SI, sparseness, TQ, bandwidth as NaN (undefined for zero firing)
            print(f"  → Filled laser ON firing rates with 0 (complete suppression)")
            print(f"  → Left other metrics as NaN (undefined for silent cells)")
        
        print(f"\n  Final merged: {len(df_merged)} cells")
        
        return df_merged
    
    @staticmethod
    def filter_complete_cases(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Filter to complete cases for core metrics.
        
        Core metrics (selectivity, sparseness) must be valid.
        Bandwidth can be NaN (requires clear tuning curve).
        
        Returns:
            Tuple of (filtered_df, stats_dict)
        """
        print(f"\n{'='*70}")
        print("FILTERING TO COMPLETE CASES")
        print(f"{'='*70}")
        
        # Core metrics that must be valid
        core_metrics = [
            'selectivity_off', 'selectivity_on',
            'sparseness_off', 'sparseness_on'
        ]
        
        complete_mask = df[core_metrics].notna().all(axis=1)
        n_before = len(df)
        df_filtered = df[complete_mask].copy()
        n_after = len(df_filtered)
        
        # Count cells with valid bandwidth
        bw_valid = df_filtered[['bandwidth_off', 'bandwidth_on']].notna().all(axis=1)
        n_with_bandwidth = np.sum(bw_valid)
        
        # Print summary
        print(f"  Required valid: selectivity, sparseness")
        print(f"  Optional (can be NaN): bandwidth")
        print(f"  Before filtering: {n_before} cells")
        print(f"  After filtering:  {n_after} cells ({100*n_after/n_before:.1f}%)")
        print(f"  Excluded:         {n_before - n_after} cells")
        print(f"  → Core metrics use n = {n_after}")
        print(f"  → Bandwidth metric uses n = {n_with_bandwidth}")
        
        stats = {
            'n_total': n_before,
            'n_complete': n_after,
            'n_excluded': n_before - n_after,
            'n_with_bandwidth': n_with_bandwidth
        }
        
        return df_filtered, stats


# =============================================================================
# STATISTICAL ANALYSIS MODULE
# =============================================================================

class StatisticalAnalyzer:
    """Performs statistical tests comparing laser conditions."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def compute_paired_statistics(
        self,
        data_off: np.ndarray,
        data_on: np.ndarray,
        metric_name: str
    ) -> Optional[StatisticalResult]:
        """
        Compute paired statistics comparing laser OFF vs ON.
        
        Returns None if insufficient valid data (< min_cells_for_stats).
        """
        # Remove pairs where either value is NaN
        valid_mask = ~(np.isnan(data_off) | np.isnan(data_on))
        data_off_valid = data_off[valid_mask]
        data_on_valid = data_on[valid_mask]
        
        n_cells = len(data_off_valid)
        
        if n_cells < self.config.min_cells_for_stats:
            print(f"  WARNING: Only {n_cells} cells with valid {metric_name} data")
            return None
        
        # Summary statistics
        mean_off = np.mean(data_off_valid)
        median_off = np.median(data_off_valid)
        std_off = np.std(data_off_valid)
        sem_off = std_off / np.sqrt(n_cells)
        
        mean_on = np.mean(data_on_valid)
        median_on = np.median(data_on_valid)
        std_on = np.std(data_on_valid)
        sem_on = std_on / np.sqrt(n_cells)
        
        # Differences
        differences = data_on_valid - data_off_valid
        mean_diff = np.mean(differences)
        median_diff = np.median(differences)
        
        # Wilcoxon signed-rank test (non-parametric paired test)
        try:
            wilcoxon_stat, wilcoxon_p = stats.wilcoxon(data_off_valid, data_on_valid)
        except Exception as e:
            print(f"  WARNING: Wilcoxon test failed for {metric_name}: {e}")
            wilcoxon_stat = np.nan
            wilcoxon_p = np.nan
        
        # Effect size (Cohen's d for paired data)
        std_diff = np.std(differences)
        cohens_d = mean_diff / std_diff if std_diff > 0 else np.nan
        
        # Percent change from baseline
        percent_change = (mean_diff / mean_off * 100) if mean_off != 0 else np.nan
        
        # Determine biological significance based on effect size thresholds
        is_biologically_significant = (
            (abs(cohens_d) >= self.config.min_effect_size_cohens_d) and 
            (abs(percent_change) >= self.config.min_percent_change)
        )
        
        return StatisticalResult(
            metric=metric_name,
            n_cells=n_cells,
            mean_off=mean_off,
            median_off=median_off,
            std_off=std_off,
            sem_off=sem_off,
            mean_on=mean_on,
            median_on=median_on,
            std_on=std_on,
            sem_on=sem_on,
            mean_diff=mean_diff,
            median_diff=median_diff,
            percent_change=percent_change,
            wilcoxon_statistic=wilcoxon_stat,
            wilcoxon_pvalue=wilcoxon_p,
            cohens_d=cohens_d,
            is_biologically_significant=is_biologically_significant
        )
    
    def analyze_all_metrics(
        self,
        df: pd.DataFrame
    ) -> List[StatisticalResult]:
        """Analyze all metrics and return list of results."""
        print(f"\n{'='*70}")
        print("STATISTICAL TESTS")
        print(f"{'='*70}")
        
        metrics_to_test = [
            ('selectivity', 'selectivity_off', 'selectivity_on'),
            ('sparseness', 'sparseness_off', 'sparseness_on'),
            ('bandwidth', 'bandwidth_off', 'bandwidth_on'),
            ('tuning_quality', 'tuning_quality_off', 'tuning_quality_on'),
            ('peak_response', 'peak_response_off', 'peak_response_on'),
            ('mean_response', 'mean_response_off', 'mean_response_on'),
        ]
        
        # Add optional metrics if they exist in the DataFrame
        if 'stimulus_evoked_change_off' in df.columns and 'stimulus_evoked_change_on' in df.columns:
            metrics_to_test.append(('stimulus_evoked_change', 'stimulus_evoked_change_off', 'stimulus_evoked_change_on'))
        
        if 'fano_factor_off' in df.columns and 'fano_factor_on' in df.columns:
            metrics_to_test.append(('fano_factor', 'fano_factor_off', 'fano_factor_on'))
        
        results = []
        
        for metric_name, col_off, col_on in metrics_to_test:
            print(f"\n{metric_name.upper()}:")
            
            data_off = df[col_off].values
            data_on = df[col_on].values
            
            result = self.compute_paired_statistics(data_off, data_on, metric_name)
            
            if result is not None:
                results.append(result)
                self._print_result(result)
        
        return results
    
    @staticmethod
    def _print_result(result: StatisticalResult):
        """Print formatted statistical result."""
        p_str = format_pvalue(result.wilcoxon_pvalue)
        sig_label = get_significance_label(result.wilcoxon_pvalue)
        
        # Determine if change is meaningful
        bio_sig = "✓ BIOLOGICALLY SIGNIFICANT" if result.is_biologically_significant else "✗ Not biologically meaningful"
        
        print(f"  n = {result.n_cells}")
        print(f"  Laser OFF: {result.mean_off:.4f} ± {result.sem_off:.4f} (mean ± SEM)")
        print(f"  Laser ON:  {result.mean_on:.4f} ± {result.sem_on:.4f} (mean ± SEM)")
        print(f"  Difference: {result.mean_diff:+.4f} ({result.percent_change:+.1f}%)")
        print(f"  Wilcoxon p-value: {p_str} {sig_label}")
        print(f"  Cohen's d: {result.cohens_d:.3f}")
        print(f"  Effect: {bio_sig}")


# =============================================================================
# PLOTTING MODULE
# =============================================================================

class ComparisonPlotter:
    """Handles generation of comparison plots."""
    
    @staticmethod
    def plot_scatter(
        ax: plt.Axes,
        data_off: np.ndarray,
        data_on: np.ndarray,
        metric_name: str,
        stats_result: Optional[StatisticalResult]
    ):
        """Create scatter plot comparing laser OFF vs ON."""
        # Remove NaN pairs
        valid_mask = ~(np.isnan(data_off) | np.isnan(data_on))
        data_off_valid = data_off[valid_mask]
        data_on_valid = data_on[valid_mask]
        
        if len(data_off_valid) == 0:
            ax.text(0.5, 0.5, 'No valid data', ha='center', va='center',
                   transform=ax.transAxes)
            return
        
        # Scatter plot
        ax.scatter(data_off_valid, data_on_valid, alpha=0.6, s=50,
                  edgecolors='black', linewidths=0.5)
        
        # Unity line
        min_val = min(np.min(data_off_valid), np.min(data_on_valid))
        max_val = max(np.max(data_off_valid), np.max(data_on_valid))
        ax.plot([min_val, max_val], [min_val, max_val], 'k--',
               alpha=0.5, linewidth=2, label='Unity')
        
        # Labels and title
        ax.set_xlabel(f'{metric_name}\n(Laser OFF)', fontsize=11)
        ax.set_ylabel(f'{metric_name}\n(Laser ON)', fontsize=11)
        ax.set_title(f'{metric_name} Comparison\n(n = {len(data_off_valid)} cells)',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        
        # Add statistics text box
        if stats_result is not None:
            p_str = format_pvalue(stats_result.wilcoxon_pvalue)
            color = get_significance_color(stats_result.wilcoxon_pvalue)
            
            stats_text = (
                f"n = {stats_result.n_cells}\n"
                f"Mean OFF: {stats_result.mean_off:.3f}\n"
                f"Mean ON: {stats_result.mean_on:.3f}\n"
                f"Δ = {stats_result.mean_diff:.3f}\n"
                f"p = {p_str}\n"
                f"d = {stats_result.cohens_d:.3f}"
            )
            
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                   fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
    
    @staticmethod
    def plot_bar(
        ax: plt.Axes,
        stats_result: StatisticalResult,
        metric_name: str
    ):
        """Create bar plot with error bars comparing conditions."""
        x_pos = [0, 1]
        means = [stats_result.mean_off, stats_result.mean_on]
        sems = [stats_result.sem_off, stats_result.sem_on]
        
        ax.bar(x_pos, means, yerr=sems, capsize=10,
              color=['blue', 'red'], alpha=0.7,
              edgecolor='black', linewidth=2)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(['Laser OFF', 'Laser ON'], fontsize=11)
        ax.set_ylabel(metric_name, fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add significance bracket with proper spacing
        y_max = max(means) + max(sems)
        bracket_height = y_max * 1.15  # Position bracket above bars
        sig_text = get_significance_label(stats_result.wilcoxon_pvalue)
        
        # Draw significance bracket
        ax.plot([0, 0, 1, 1], [y_max * 1.08, bracket_height, bracket_height, y_max * 1.08], 
                'k-', linewidth=1.5)
        
        # Add significance label
        ax.text(0.5, bracket_height * 1.02, sig_text, ha='center',
               fontsize=14, fontweight='bold')
        
        # Add p-value below x-axis
        p_str = format_pvalue(stats_result.wilcoxon_pvalue)
        ax.text(0.5, -0.18, f'p = {p_str}',
               transform=ax.transAxes, ha='center', fontsize=9)
        
        # Set title with extra padding to avoid overlap
        ax.set_title(f'{metric_name}\n(Mean ± SEM, n = {stats_result.n_cells})',
                    fontsize=11, fontweight='bold', pad=20)
        
        # Adjust y-axis limit to accommodate bracket
        ax.set_ylim([None, bracket_height * 1.15])
    
    def create_comparison_pdf(
        self,
        df: pd.DataFrame,
        stats_results: List[StatisticalResult],
        output_path: str
    ):
        """Create multi-page PDF with scatter and bar plots."""
        metrics_map = {
            'selectivity': ('selectivity_off', 'selectivity_on'),
            'sparseness': ('sparseness_off', 'sparseness_on'),
            'bandwidth': ('bandwidth_off', 'bandwidth_on'),
            'tuning_quality': ('tuning_quality_off', 'tuning_quality_on'),
            'peak_response': ('peak_response_off', 'peak_response_on'),
            'mean_response': ('mean_response_off', 'mean_response_on'),
            'stimulus_evoked_change': ('stimulus_evoked_change_off', 'stimulus_evoked_change_on'),
            'fano_factor': ('fano_factor_off', 'fano_factor_on')
        }
        
        n_cells = len(df)
        
        with PdfPages(output_path) as pdf:
            # Page 1: Scatter plots (first 6 metrics)
            with figure_context(figsize=(17, 11)) as fig:
                fig.suptitle(
                    f'AM Tuning: Laser OFF vs ON Comparison (Scatter Plots)\n'
                    f'Tuned Cells Only (n = {n_cells} cells)',
                    fontsize=16, fontweight='bold'
                )
                
                for idx, result in enumerate(stats_results[:6]):  # First 6 metrics only
                    ax = fig.add_subplot(2, 3, idx + 1)
                    col_off, col_on = metrics_map[result.metric]
                    
                    self.plot_scatter(
                        ax, df[col_off].values, df[col_on].values,
                        result.metric.replace('_', ' ').title(), result
                    )
                
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig, dpi=150)
            
            # Page 2: Bar plots (first 6 metrics)
            with figure_context(figsize=(17, 11)) as fig:
                fig.suptitle(
                    f'AM Tuning: Laser OFF vs ON Comparison (Bar Plots)\n'
                    f'Tuned Cells Only (n = {n_cells} cells)',
                    fontsize=16, fontweight='bold'
                )
                
                for idx, result in enumerate(stats_results[:6]):  # First 6 metrics only
                    ax = fig.add_subplot(2, 3, idx + 1)
                    self.plot_bar(
                        ax, result,
                        result.metric.replace('_', ' ').title()
                    )
                
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig, dpi=150)
            
            # Page 3: Additional metrics (stimulus-evoked change & fano factor)
            if len(stats_results) > 6:
                with figure_context(figsize=(17, 11)) as fig:
                    fig.suptitle(
                        f'AM Tuning: Laser OFF vs ON - Additional Metrics\n'
                        f'Tuned Cells Only (n = {n_cells} cells)',
                        fontsize=16, fontweight='bold'
                    )
                    
                    # Plot up to 4 additional metrics (2x2 grid)
                    n_additional = min(len(stats_results) - 6, 4)
                    
                    for idx in range(n_additional):
                        result = stats_results[6 + idx]
                        col_off, col_on = metrics_map[result.metric]
                        
                        # Scatter plot (top row)
                        ax_scatter = fig.add_subplot(2, 2, idx + 1)
                        self.plot_scatter(
                            ax_scatter, df[col_off].values, df[col_on].values,
                            result.metric.replace('_', ' ').title(), result
                        )
                    
                    fig.tight_layout(rect=[0, 0, 1, 0.96])
                    pdf.savefig(fig, dpi=150)
                    
            # Page 4: Bar plots for additional metrics
            if len(stats_results) > 6:
                with figure_context(figsize=(17, 11)) as fig:
                    fig.suptitle(
                        f'AM Tuning: Laser OFF vs ON - Additional Metrics (Bar Plots)\n'
                        f'Tuned Cells Only (n = {n_cells} cells)',
                        fontsize=16, fontweight='bold'
                    )
                    
                    n_additional = min(len(stats_results) - 6, 4)
                    
                    for idx in range(n_additional):
                        result = stats_results[6 + idx]
                        
                        # Bar plot
                        ax_bar = fig.add_subplot(2, 2, idx + 1)
                        self.plot_bar(
                            ax_bar, result,
                            result.metric.replace('_', ' ').title()
                        )
                    
                    fig.tight_layout(rect=[0, 0, 1, 0.96])
                    pdf.savefig(fig, dpi=150)
        
        print(f"\nSaved comparison plots: {output_path}")
    
    def create_significance_summary_figure(
        self,
        stats_results: List[StatisticalResult],
        output_path: str
    ):
        """
        Create summary figure showing statistical vs biological significance.
        
        Generates a 2-panel figure:
        1. Effect size (Cohen's d) for each metric with significance thresholds
        2. Classification matrix showing statistical vs biological significance
        """
        print(f"\n  Generating biological significance summary figure...")
        
        with figure_context(output_path, figsize=(16, 6)) as fig:
            # Panel 1: Effect sizes with thresholds
            ax1 = fig.add_subplot(1, 2, 1)
            
            metric_names = [r.metric.replace('_', ' ').title() for r in stats_results]
            cohens_d_values = [r.cohens_d for r in stats_results]
            p_values = [r.wilcoxon_pvalue for r in stats_results]
            bio_sig = [r.is_biologically_significant for r in stats_results]
            
            # Color bars based on significance
            colors = []
            for p, bio in zip(p_values, bio_sig):
                if bio:
                    colors.append('darkgreen')  # Biologically significant
                elif p < 0.05:
                    colors.append('orange')  # Statistically sig but not biologically
                else:
                    colors.append('lightgray')  # Not significant
            
            y_pos = np.arange(len(metric_names))
            bars = ax1.barh(y_pos, cohens_d_values, color=colors, edgecolor='black', linewidth=1.5)
            
            # Add threshold lines
            ax1.axvline(0.3, color='red', linestyle='--', linewidth=2, alpha=0.7, 
                       label='Biological Significance\nThreshold (d = 0.3)')
            ax1.axvline(-0.3, color='red', linestyle='--', linewidth=2, alpha=0.7)
            ax1.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
            
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(metric_names, fontsize=10)
            ax1.set_xlabel("Cohen's d (Effect Size)", fontsize=12, fontweight='bold')
            ax1.set_title("Effect Size of Laser Manipulation\n(AM Tuning Metrics)", 
                         fontsize=13, fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='x')
            ax1.legend(loc='best', fontsize=9)
            
            # Add p-values as text
            for i, (d, p) in enumerate(zip(cohens_d_values, p_values)):
                p_str = format_pvalue(p)
                sig_str = get_significance_label(p)
                x_offset = 0.05 if d >= 0 else -0.05
                ha = 'left' if d >= 0 else 'right'
                ax1.text(d + x_offset, i, f'{sig_str} (p={p_str})', 
                        va='center', ha=ha, fontsize=8)
            
            # Panel 2: Significance classification matrix
            ax2 = fig.add_subplot(1, 2, 2)
            
            # Categorize results
            categories = {
                'Biologically\nSignificant': [],
                'Statistically Sig\nOnly': [],
                'Not\nSignificant': []
            }
            
            for r in stats_results:
                metric_label = r.metric.replace('_', ' ').title()
                if r.is_biologically_significant:
                    categories['Biologically\nSignificant'].append(
                        f"{metric_label}\n(d={r.cohens_d:.2f}, Δ={r.percent_change:+.1f}%)"
                    )
                elif r.wilcoxon_pvalue < 0.05:
                    categories['Statistically Sig\nOnly'].append(
                        f"{metric_label}\n(d={r.cohens_d:.2f}, Δ={r.percent_change:+.1f}%)"
                    )
                else:
                    categories['Not\nSignificant'].append(
                        f"{metric_label}\n(p={format_pvalue(r.wilcoxon_pvalue)})"
                    )
            
            # Count metrics in each category
            counts = [
                len(categories['Biologically\nSignificant']),
                len(categories['Statistically Sig\nOnly']),
                len(categories['Not\nSignificant'])
            ]
            
            # Create stacked bar
            cat_names = list(categories.keys())
            bar_colors = ['darkgreen', 'orange', 'lightgray']
            
            bars = ax2.bar(cat_names, counts, color=bar_colors, 
                          edgecolor='black', linewidth=2, alpha=0.8)
            
            # Add count labels on bars
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height/2,
                        f'n = {count}',
                        ha='center', va='center', fontsize=14, 
                        fontweight='bold', color='white')
            
            ax2.set_ylabel('Number of Metrics', fontsize=12, fontweight='bold')
            ax2.set_title('Classification of Laser Effects\n(Statistical vs Biological Significance)', 
                         fontsize=13, fontweight='bold')
            ax2.set_ylim([0, max(counts) * 1.2])
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Add legend with criteria
            legend_text = (
                'Biologically Significant:\n'
                '  • p < 0.05 AND\n'
                '  • |Cohen\'s d| ≥ 0.3 AND\n'
                '  • |% change| ≥ 10%\n\n'
                'Statistically Sig Only:\n'
                '  • p < 0.05 BUT\n'
                '  • Small effect size\n\n'
                'Not Significant:\n'
                '  • p ≥ 0.05'
            )
            ax2.text(1.15, 0.5, legend_text, transform=ax2.transAxes,
                    fontsize=9, verticalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            # Add metric details below
            details_y = -0.35
            for cat_name, metrics in categories.items():
                if metrics:
                    details_text = f"{cat_name}:\n" + "\n".join(f"  • {m}" for m in metrics)
                    ax2.text(0.5, details_y, details_text, transform=ax2.transAxes,
                            fontsize=8, verticalalignment='top', ha='center',
                            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
                    details_y -= 0.15 * len(metrics)
            
            fig.suptitle('Biological Significance Analysis: Laser Effects on AM Tuning\n'
                        f'(n = {stats_results[0].n_cells} cells)',
                        fontsize=14, fontweight='bold', y=0.98)
            
            fig.tight_layout(rect=[0, 0, 1, 0.96])
        
        print(f"    Saved: {output_path}")


# =============================================================================
# NORMALIZED TUNING CURVE ANALYSIS MODULE
# =============================================================================

class NormalizedTuningAnalyzer:
    """Analyzes population-average tuning curves normalized to best AM rate."""
    
    def __init__(self, config: AnalysisConfig, celldbs: Dict[str, pd.DataFrame]):
        self.config = config
        self.celldbs = celldbs
    
    def compute_normalized_curves(
        self,
        df: pd.DataFrame,
        octave_bins: np.ndarray = None
    ) -> 'NormalizedTuningData':
        """
        Compute population-average tuning curves normalized to best AM rate.
        
        Args:
            df: DataFrame with cell info (session_id, cell_idx, best_rate, etc.)
            octave_bins: Octave bins relative to best rate (default: -2 to +2 in 0.25 steps)
        
        Returns:
            NormalizedTuningData with averaged curves for laser OFF and ON
        """
        if octave_bins is None:
            octave_bins = np.arange(-2.0, 2.25, 0.25)
        
        print(f"\n{'='*70}")
        print("COMPUTING NORMALIZED AVERAGE TUNING CURVES")
        print(f"{'='*70}")
        print(f"  Octave bins: {octave_bins}")
        print(f"  Analyzing {len(df)} tuned cells")
        
        # Initialize accumulators for each octave bin
        n_bins = len(octave_bins)
        rates_off_all = [[] for _ in range(n_bins)]  # Absolute rates
        rates_on_all = [[] for _ in range(n_bins)]
        rates_off_norm_all = [[] for _ in range(n_bins)]  # Normalized to peak
        rates_on_norm_all = [[] for _ in range(n_bins)]
        
        # Process each cell
        for idx, row in df.iterrows():
            session_id = int(row['session_id'])
            cell_idx = int(row['cell_idx'])
            subject = row['subject']
            
            # Load tuning curves for this cell
            tuning_off, tuning_on = self._load_cell_tuning_curves(
                session_id, cell_idx, subject
            )
            
            if tuning_off is None or tuning_on is None:
                continue
            
            # Normalize AM rates to octaves relative to best rate
            best_rate_off = tuning_off.best_freq
            
            if best_rate_off <= 0:
                continue
            
            octaves_off = np.log2(tuning_off.frequencies / best_rate_off)
            
            # Normalize firing rates to peak for this cell
            peak_rate_off = np.max(tuning_off.mean_rates)
            peak_rate_on = np.max(tuning_on.mean_rates)
            
            if peak_rate_off <= 0:
                continue
            
            rates_off_normalized = tuning_off.mean_rates / peak_rate_off
            rates_on_normalized = tuning_on.mean_rates / peak_rate_on if peak_rate_on > 0 else tuning_on.mean_rates
            
            # Bin the data - assign each AM rate to nearest octave bin
            for j, oct in enumerate(octaves_off):
                # Find nearest bin
                bin_idx = np.argmin(np.abs(octave_bins - oct))
                
                # Only include if within 0.15 octaves of bin center (relaxed from 0.125)
                if abs(octave_bins[bin_idx] - oct) < 0.15:
                    rates_off_all[bin_idx].append(tuning_off.mean_rates[j])
                    rates_on_all[bin_idx].append(tuning_on.mean_rates[j])
                    rates_off_norm_all[bin_idx].append(rates_off_normalized[j])
                    rates_on_norm_all[bin_idx].append(rates_on_normalized[j])
        
        # Compute means and SEMs for each bin
        mean_rates_off = np.array([np.mean(rates) if len(rates) > 0 else np.nan 
                                   for rates in rates_off_all])
        sem_rates_off = np.array([np.std(rates) / np.sqrt(len(rates)) if len(rates) > 0 else np.nan
                                 for rates in rates_off_all])
        n_cells_off = np.array([len(rates) for rates in rates_off_all])
        
        mean_rates_on = np.array([np.mean(rates) if len(rates) > 0 else np.nan
                                 for rates in rates_on_all])
        sem_rates_on = np.array([np.std(rates) / np.sqrt(len(rates)) if len(rates) > 0 else np.nan
                                for rates in rates_on_all])
        n_cells_on = np.array([len(rates) for rates in rates_on_all])
        
        # Normalized versions
        mean_rates_off_norm = np.array([np.mean(rates) if len(rates) > 0 else np.nan
                                       for rates in rates_off_norm_all])
        sem_rates_off_norm = np.array([np.std(rates) / np.sqrt(len(rates)) if len(rates) > 0 else np.nan
                                      for rates in rates_off_norm_all])
        
        mean_rates_on_norm = np.array([np.mean(rates) if len(rates) > 0 else np.nan
                                      for rates in rates_on_norm_all])
        sem_rates_on_norm = np.array([np.std(rates) / np.sqrt(len(rates)) if len(rates) > 0 else np.nan
                                     for rates in rates_on_norm_all])
        
        print(f"  Successfully computed normalized curves")
        print(f"  Mean cells per bin: {np.mean(n_cells_off[n_cells_off > 0]):.1f}")
        print(f"  Cells per bin distribution: {n_cells_off}")
        print(f"  Total data points collected: {np.sum(n_cells_off)}")
        
        # Debug: Print sample data
        valid_bins = n_cells_off > 0
        if np.sum(valid_bins) > 0:
            print(f"  Sample valid bins:")
            for i in np.where(valid_bins)[0][:5]:
                print(f"    Bin {octave_bins[i]:.2f} oct: n={n_cells_off[i]}, "
                      f"OFF={mean_rates_off[i]:.2f}Hz, ON={mean_rates_on[i]:.2f}Hz")
        
        return NormalizedTuningData(
            octave_bins=octave_bins,
            mean_rates_off=mean_rates_off,
            sem_rates_off=sem_rates_off,
            n_cells_off=n_cells_off,
            mean_rates_on=mean_rates_on,
            sem_rates_on=sem_rates_on,
            n_cells_on=n_cells_on,
            mean_rates_off_normalized=mean_rates_off_norm,
            sem_rates_off_normalized=sem_rates_off_norm,
            mean_rates_on_normalized=mean_rates_on_norm,
            sem_rates_on_normalized=sem_rates_on_norm
        )
    
    def _load_cell_tuning_curves(
        self,
        session_id: int,
        cell_idx: int,
        subject: str
    ) -> Tuple[Optional['TuningCurveData'], Optional['TuningCurveData']]:
        """Load tuning curves for one cell for both laser conditions."""
        try:
            session = SESSIONS[session_id]
            celldb = self.celldbs[subject]
            
            # Filter to this session
            celldb_session = celldb[
                (celldb.date == session.date) &
                (celldb.pdepth == session.depth)
            ]
            
            if len(celldb_session) == 0:
                return None, None
            
            # Load ephys data
            ensemble = ephyscore.CellEnsemble(celldb_session)
            ephys_data, bdata = ensemble.load('optoTuningAM')
            
            # Extract spike data
            event_times = ephys_data['events']['stimOn']
            n_trials = len(bdata['currentFreq'])
            
            if len(event_times) != n_trials and len(event_times) == n_trials + 1:
                event_times = event_times[:n_trials]
            
            spike_times_all, trial_index_all, _ = ensemble.eventlocked_spiketimes(
                event_times, self.config.time_range
            )
            
            # Get this cell's data
            spike_times = spike_times_all[cell_idx]
            trial_index = trial_index_all[cell_idx]
            
            # Compute tuning curves
            from jaratoolbox import spikesanalysis
            tuning_off = self._compute_single_tuning_curve(
                spike_times, trial_index, bdata, 'off'
            )
            tuning_on = self._compute_single_tuning_curve(
                spike_times, trial_index, bdata, 'on'
            )
            
            return tuning_off, tuning_on
            
        except Exception as e:
            print(f"    Warning: Could not load cell {cell_idx} from session {session_id}: {e}")
            return None, None
    
    def _compute_single_tuning_curve(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        laser_condition: str
    ) -> Optional['TuningCurveData']:
        """Compute tuning curve for one cell and one laser condition."""
        frequencies = np.asarray(bdata['currentFreq']).flatten()
        laser_mask = self._get_laser_mask(bdata, laser_condition)
        unique_freqs = np.unique(frequencies)
        
        mean_rates = np.zeros(len(unique_freqs))
        sem_rates = np.zeros(len(unique_freqs))
        
        window_duration = self.config.response_window[1] - self.config.response_window[0]
        in_window = (spike_times >= self.config.response_window[0]) & \
                   (spike_times < self.config.response_window[1])
        
        for i, freq in enumerate(unique_freqs):
            freq_laser_mask = (frequencies == freq) & laser_mask
            trial_nums = np.where(freq_laser_mask)[0]
            
            if len(trial_nums) == 0:
                mean_rates[i] = 0.0
                sem_rates[i] = 0.0
                continue
            
            rates = np.zeros(len(trial_nums))
            for j, trial_num in enumerate(trial_nums):
                trial_spike_mask = (trial_index == trial_num) & in_window
                rates[j] = np.sum(trial_spike_mask) / window_duration
            
            mean_rates[i] = np.mean(rates)
            sem_rates[i] = np.std(rates) / np.sqrt(len(rates))
        
        # Find best frequency
        best_idx = np.argmax(mean_rates)
        best_freq = unique_freqs[best_idx]
        
        return TuningCurveData(
            frequencies=unique_freqs,
            mean_rates=mean_rates,
            sem_rates=sem_rates,
            best_freq=best_freq
        )
    
    @staticmethod
    def _get_laser_mask(bdata: dict, laser_condition: str) -> np.ndarray:
        """Get boolean mask for laser condition."""
        if 'laserTrial' in bdata:
            laser_trials = bdata['laserTrial']
            if hasattr(laser_trials, 'ndim') and laser_trials.ndim > 1:
                laser_trials = laser_trials.flatten()
            laser_trials = np.asarray(laser_trials).flatten().astype(int)
        else:
            laser_trials = np.zeros(len(bdata['currentFreq']), dtype=int)
        
        if laser_condition == 'off':
            return (laser_trials == 0)
        elif laser_condition == 'on':
            return (laser_trials == 1)
        else:
            raise ValueError(f"Invalid laser_condition: {laser_condition}")
    
    @staticmethod
    def plot_normalized_curves(
        norm_data: 'NormalizedTuningData',
        output_path: str
    ):
        """Plot normalized average tuning curves for laser OFF vs ON."""
        print(f"\n  Generating normalized tuning curve plots...")
        
        with figure_context(output_path, figsize=(14, 6)) as fig:
            # Plot 1: Absolute firing rates
            ax1 = fig.add_subplot(1, 2, 1)
            
            # Plot laser OFF
            valid_off = ~np.isnan(norm_data.mean_rates_off)
            ax1.errorbar(
                norm_data.octave_bins[valid_off],
                norm_data.mean_rates_off[valid_off],
                yerr=norm_data.sem_rates_off[valid_off],
                marker='o', markersize=8, linewidth=2, capsize=5,
                color='blue', label='Laser OFF', alpha=0.8
            )
            
            # Plot laser ON
            valid_on = ~np.isnan(norm_data.mean_rates_on)
            ax1.errorbar(
                norm_data.octave_bins[valid_on],
                norm_data.mean_rates_on[valid_on],
                yerr=norm_data.sem_rates_on[valid_on],
                marker='s', markersize=8, linewidth=2, capsize=5,
                color='red', label='Laser ON', alpha=0.8
            )
            
            ax1.axvline(0, color='black', linestyle='--', alpha=0.5, linewidth=1.5,
                       label='Best AM Rate')
            ax1.set_xlabel('Octaves from Best AM Rate', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
            ax1.set_title('Population-Average AM Tuning\n(Absolute Firing Rates)',
                         fontsize=13, fontweight='bold')
            ax1.legend(loc='best', fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Normalized to peak
            ax2 = fig.add_subplot(1, 2, 2)
            
            ax2.errorbar(
                norm_data.octave_bins[valid_off],
                norm_data.mean_rates_off_normalized[valid_off],
                yerr=norm_data.sem_rates_off_normalized[valid_off],
                marker='o', markersize=8, linewidth=2, capsize=5,
                color='blue', label='Laser OFF', alpha=0.8
            )
            
            ax2.errorbar(
                norm_data.octave_bins[valid_on],
                norm_data.mean_rates_on_normalized[valid_on],
                yerr=norm_data.sem_rates_on_normalized[valid_on],
                marker='s', markersize=8, linewidth=2, capsize=5,
                color='red', label='Laser ON', alpha=0.8
            )
            
            ax2.axvline(0, color='black', linestyle='--', alpha=0.5, linewidth=1.5,
                       label='Best AM Rate')
            ax2.axhline(1.0, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
            ax2.set_xlabel('Octaves from Best AM Rate', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Normalized Firing Rate\n(Fraction of Peak)', fontsize=12, fontweight='bold')
            ax2.set_title('Population-Average AM Tuning\n(Normalized to Peak)',
                         fontsize=13, fontweight='bold')
            ax2.legend(loc='best', fontsize=10)
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim([0, 1.2])
            
            fig.suptitle('Normalized AM Tuning: Laser OFF vs ON\n'
                        f'(Tuned Cells, n = {norm_data.n_cells_off[norm_data.n_cells_off > 0].mean():.0f} cells/bin avg)',
                        fontsize=14, fontweight='bold', y=1.02)
            
            fig.tight_layout()
        
        print(f"    Saved: {output_path}")
    
    @staticmethod
    def save_normalized_data(
        norm_data: 'NormalizedTuningData',
        output_path: str
    ):
        """Save normalized tuning data to CSV."""
        df = pd.DataFrame({
            'octave_bin': norm_data.octave_bins,
            'mean_rate_off_hz': norm_data.mean_rates_off,
            'sem_rate_off_hz': norm_data.sem_rates_off,
            'n_cells_off': norm_data.n_cells_off,
            'mean_rate_on_hz': norm_data.mean_rates_on,
            'sem_rate_on_hz': norm_data.sem_rates_on,
            'n_cells_on': norm_data.n_cells_on,
            'mean_rate_off_normalized': norm_data.mean_rates_off_normalized,
            'sem_rate_off_normalized': norm_data.sem_rates_off_normalized,
            'mean_rate_on_normalized': norm_data.mean_rates_on_normalized,
            'sem_rate_on_normalized': norm_data.sem_rates_on_normalized
        })
        
        df.to_csv(output_path, index=False)
        print(f"    Saved: {output_path}")


# =============================================================================
# OUTPUT MODULE
# =============================================================================

class ResultsSaver:
    """Handles saving of analysis results."""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_merged_data(self, df: pd.DataFrame) -> str:
        """Save merged laser OFF/ON comparison data."""
        csv_path = os.path.join(self.output_dir, 'laser_on_vs_off_metrics.csv')
        df.to_csv(csv_path, index=False)
        print(f"\nSaved merged comparison data: {csv_path}")
        return csv_path
    
    def save_statistical_results(
        self,
        stats_results: List[StatisticalResult]
    ) -> str:
        """Save statistical test results to CSV."""
        # Convert NamedTuples to dicts
        results_dicts = [result._asdict() for result in stats_results]
        df_stats = pd.DataFrame(results_dicts)
        
        csv_path = os.path.join(self.output_dir, 'statistical_results.csv')
        df_stats.to_csv(csv_path, index=False)
        print(f"Saved statistical results: {csv_path}")
        return csv_path
    
    def print_summary(
        self,
        df: pd.DataFrame,
        stats_results: List[StatisticalResult],
        csv_comparison: str,
        csv_stats: str,
        pdf_path: str
    ):
        """Print comprehensive summary of analysis."""
        print(f"\n{'='*70}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*70}")
        print(f"\nOutput directory: {self.output_dir}")
        print(f"\nFiles created:")
        print(f"  1. {csv_comparison}")
        print(f"  2. {csv_stats}")
        print(f"  3. {pdf_path}")
        print(f"\nSummary:")
        print(f"  - Analyzed {len(df)} tuned cells")
        print(f"  - Compared {len(stats_results)} metrics between laser OFF and ON")
        print(f"  - Used Wilcoxon signed-rank test (non-parametric paired test)")
        print(f"\nSignificant effects (p < 0.05):")
        
        for result in stats_results:
            if result.wilcoxon_pvalue < 0.05:
                direction = "increased" if result.mean_diff > 0 else "decreased"
                p_str = format_pvalue(result.wilcoxon_pvalue)
                print(f"  - {result.metric.title()}: {direction} (p = {p_str})")


# =============================================================================
# MAIN EXECUTION COORDINATOR
# =============================================================================

class StatisticalAnalysisCoordinator:
    """Coordinates the entire statistical analysis pipeline."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.metrics_loader = MetricsLoader(config)
        self.analyzer = StatisticalAnalyzer(config)
        self.plotter = ComparisonPlotter()
        self.output_dir = os.path.join(config.metrics_dir, 'laser_statistics')
        self.saver = ResultsSaver(self.output_dir)
    
    def run(self):
        """Execute the complete analysis pipeline."""
        print("="*70)
        print("AM TUNING STATISTICAL COMPARISON: LASER OFF vs ON (TUNED CELLS)")
        print("="*70)
        
        # 1. Load metrics from CSV files
        df_off, df_on = self.metrics_loader.load_metrics()
        
        # 2. Filter to tuned cells
        df_off_tuned = self.metrics_loader.filter_tuned_cells(df_off)
        
        # 3. Merge conditions
        df_merged = DataMerger.merge_conditions(df_off_tuned, df_on)
        
        # 4. Filter to complete cases
        df_complete, filter_stats = DataMerger.filter_complete_cases(df_merged)
        
        # 5. Save merged data
        csv_comparison = self.saver.save_merged_data(df_complete)
        
        # 6. Perform statistical analysis
        stats_results = self.analyzer.analyze_all_metrics(df_complete)
        
        # 7. Save statistical results
        csv_stats = self.saver.save_statistical_results(stats_results)
        
        # 8. Generate plots
        print(f"\n{'='*70}")
        print("GENERATING COMPARISON PLOTS")
        print(f"{'='*70}")
        
        pdf_path = os.path.join(self.output_dir, 'laser_on_vs_off_comparison.pdf')
        self.plotter.create_comparison_pdf(df_complete, stats_results, pdf_path)
        
        # Generate biological significance summary figure
        bio_sig_path = os.path.join(self.output_dir, 'biological_significance_summary.png')
        self.plotter.create_significance_summary_figure(stats_results, bio_sig_path)
        
        # 9. Generate normalized average tuning curves
        print(f"\n{'='*70}")
        print("GENERATING NORMALIZED POPULATION TUNING CURVES")
        print(f"{'='*70}")
        
        # Load cell databases for accessing spike data
        celldbs = CellDatabaseLoader.load_all(SESSIONS)
        
        # Create normalized tuning analyzer
        norm_analyzer = NormalizedTuningAnalyzer(self.config, celldbs)
        
        # Compute normalized curves
        norm_data = norm_analyzer.compute_normalized_curves(df_complete)
        
        # Plot normalized curves
        norm_plot_path = os.path.join(self.output_dir, 'normalized_tuning_curves.png')
        norm_analyzer.plot_normalized_curves(norm_data, norm_plot_path)
        
        # Save normalized data to CSV
        norm_csv_path = os.path.join(self.output_dir, 'normalized_tuning_data.csv')
        norm_analyzer.save_normalized_data(norm_data, norm_csv_path)
        
        # 10. Print summary
        self.saver.print_summary(
            df_complete, stats_results,
            csv_comparison, csv_stats, pdf_path
        )
        
        print(f"\n  Additional normalized tuning curve files:")
        print(f"  - Plot: {norm_plot_path}")
        print(f"  - Data: {norm_csv_path}")
        
        return df_complete, stats_results


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main execution: Perform statistical analysis of laser effects."""
    config = AnalysisConfig()
    coordinator = StatisticalAnalysisCoordinator(config)
    
    try:
        df_results, stats_results = coordinator.run()
        print("\n✓ Analysis completed successfully!")
        
    except FileNotFoundError as e:
        print(f"\n✗ ERROR: {e}")
        return 1
    except ValueError as e:
        print(f"\n✗ ERROR: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
