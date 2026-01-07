"""
Statistical comparison of tuning metrics between laser OFF and laser ON conditions.

This script performs comprehensive statistical analysis comparing frequency tuning metrics
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
- Peak firing rate
- Mean firing rate

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

# Add hylen directory to path
sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


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
    response_window: Tuple[float, float] = (0.005, 0.095)
    tuned_categories: List[str] = None
    min_cells_for_stats: int = 3
    
    def __post_init__(self):
        """Set default tuned categories."""
        if self.tuned_categories is None:
            object.__setattr__(self, 'tuned_categories', ['tuned'])
    
    @property
    def metrics_dir(self) -> str:
        """Get metrics directory from config."""
        return str(get_reports_subdir('tuning_freq_analysis'))
    
    @property
    def override_file(self) -> str:
        """Get override file path from config."""
        # Note: This is a FILE path, not a directory, so we construct it manually
        return os.path.join(self.metrics_dir, 'classification_overrides.csv')


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
    wilcoxon_statistic: float
    wilcoxon_pvalue: float
    cohens_d: float


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
                "Please run calculate_tuning_new.py first!"
            )
        
        if not os.path.exists(csv_on):
            raise FileNotFoundError(
                f"Laser ON metrics not found: {csv_on}\n"
                "Please run calculate_tuning_new.py first!"
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
                    'peak_rate', 'mean_rate', 'selectivity_index', 'sparseness',
                    'tuning_quality', 'bandwidth_octaves']
        df_off_renamed = df_off[cols_off].rename(columns={
            'peak_rate': 'peak_rate_off',
            'mean_rate': 'mean_rate_off',
            'selectivity_index': 'selectivity_off',
            'sparseness': 'sparseness_off',
            'tuning_quality': 'tuning_quality_off',
            'bandwidth_octaves': 'bandwidth_off'
        })
        
        # Select and rename columns from laser ON
        cols_on = ['session_id', 'cell_idx', 'peak_rate', 'mean_rate',
                   'selectivity_index', 'sparseness', 'tuning_quality', 'bandwidth_octaves']
        df_on_renamed = df_on[cols_on].rename(columns={
            'peak_rate': 'peak_rate_on',
            'mean_rate': 'mean_rate_on',
            'selectivity_index': 'selectivity_on',
            'sparseness': 'sparseness_on',
            'tuning_quality': 'tuning_quality_on',
            'bandwidth_octaves': 'bandwidth_on'
        })
        
        # Merge with LEFT join to keep all cells with laser OFF data
        # Cells with complete suppression will have laser ON metrics
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
        missing_on_data = df_merged['peak_rate_on'].isna()
        n_missing = missing_on_data.sum()
        
        if n_missing > 0:
            print(f"\n  ⚠ {n_missing} cell(s) have no laser ON data:")
            for idx in df_merged[missing_on_data].index:
                row = df_merged.loc[idx]
                session_id = int(row['session_id'])
                cell_idx = int(row['cell_idx'])
                print(f"    Session {session_id}, Cell {cell_idx} - treating as complete suppression")
            
            # Fill missing laser ON firing rates with 0 (complete suppression)
            df_merged.loc[missing_on_data, 'peak_rate_on'] = 0.0
            df_merged.loc[missing_on_data, 'mean_rate_on'] = 0.0
            
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
            wilcoxon_statistic=wilcoxon_stat,
            wilcoxon_pvalue=wilcoxon_p,
            cohens_d=cohens_d
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
            ('peak_rate', 'peak_rate_off', 'peak_rate_on'),
            ('mean_rate', 'mean_rate_off', 'mean_rate_on')
        ]
        
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
        
        print(f"  n = {result.n_cells}")
        print(f"  Laser OFF: {result.mean_off:.4f} ± {result.sem_off:.4f} (mean ± SEM)")
        print(f"  Laser ON:  {result.mean_on:.4f} ± {result.sem_on:.4f} (mean ± SEM)")
        print(f"  Difference: {result.mean_diff:.4f}")
        print(f"  Wilcoxon p-value: {p_str}")
        print(f"  Cohen's d: {result.cohens_d:.4f}")
        print(f"  {sig_label}")


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
        ax.set_title(f'{metric_name}\n(Mean ± SEM, n = {stats_result.n_cells} cells)',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add significance bracket
        y_max = max(means) + max(sems) * 1.2
        sig_text = get_significance_label(stats_result.wilcoxon_pvalue)
        
        ax.plot([0, 1], [y_max, y_max], 'k-', linewidth=2)
        ax.text(0.5, y_max * 1.05, sig_text, ha='center',
               fontsize=14, fontweight='bold')
        
        # Add p-value
        p_str = format_pvalue(stats_result.wilcoxon_pvalue)
        ax.text(0.5, -0.15, f'p = {p_str}',
               transform=ax.transAxes, ha='center', fontsize=9)
    
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
            'peak_rate': ('peak_rate_off', 'peak_rate_on'),
            'mean_rate': ('mean_rate_off', 'mean_rate_on')
        }
        
        n_cells = len(df)
        
        with PdfPages(output_path) as pdf:
            # Page 1: Scatter plots
            with figure_context(figsize=(17, 11)) as fig:
                fig.suptitle(
                    f'Laser OFF vs ON Comparison (Scatter Plots)\n'
                    f'Tuned Cells Only (n = {n_cells} cells)',
                    fontsize=16, fontweight='bold'
                )
                
                for idx, result in enumerate(stats_results):
                    ax = fig.add_subplot(2, 3, idx + 1)
                    col_off, col_on = metrics_map[result.metric]
                    
                    self.plot_scatter(
                        ax, df[col_off].values, df[col_on].values,
                        result.metric.replace('_', ' ').title(), result
                    )
                
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig, dpi=150)
            
            # Page 2: Bar plots
            with figure_context(figsize=(17, 11)) as fig:
                fig.suptitle(
                    f'Laser OFF vs ON Comparison (Bar Plots)\n'
                    f'Tuned Cells Only (n = {n_cells} cells)',
                    fontsize=16, fontweight='bold'
                )
                
                for idx, result in enumerate(stats_results):
                    ax = fig.add_subplot(2, 3, idx + 1)
                    self.plot_bar(
                        ax, result,
                        result.metric.replace('_', ' ').title()
                    )
                
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig, dpi=150)
        
        print(f"\nSaved comparison plots: {output_path}")
    
    def create_histogram_distributions(
        self,
        df: pd.DataFrame,
        stats_results: List[StatisticalResult],
        output_dir: str
    ):
        """
        Create histogram distribution plots for selectivity index and tuning quality.
        
        Two separate figures (Option C):
        - Figure 1: Selectivity Index (OFF on left, ON on right)
        - Figure 2: Tuning Quality (OFF on left, ON on right)
        
        Each with separate histograms, all statistics, and 40 bins.
        
        Args:
            df: DataFrame with merged OFF/ON data
            stats_results: List of statistical results
            output_dir: Directory to save plots
        """
        print(f"\n{'='*70}")
        print("GENERATING HISTOGRAM DISTRIBUTION PLOTS")
        print(f"{'='*70}")
        
        # Define metrics to plot
        metrics_to_histogram = {
            'selectivity': 'Selectivity Index',
            'tuning_quality': 'Tuning Quality'
        }
        
        for metric_key, metric_label in metrics_to_histogram.items():
            print(f"\n  Creating histogram for {metric_label}...")
            
            # Find the corresponding stats result
            stats_result = next((r for r in stats_results if r.metric == metric_key), None)
            
            if stats_result is None:
                print(f"    WARNING: No statistics found for {metric_key}, skipping...")
                continue
            
            # Get data
            col_off = f'{metric_key}_off'
            col_on = f'{metric_key}_on'
            
            # Remove NaN values
            data_off = df[col_off].dropna().values
            data_on = df[col_on].dropna().values
            
            if len(data_off) == 0 or len(data_on) == 0:
                print(f"    WARNING: No valid data for {metric_key}, skipping...")
                continue
            
            # Create figure with 2 subplots (side by side)
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # Define common bin range for both histograms
            all_data = np.concatenate([data_off, data_on])
            data_min = np.min(all_data)
            data_max = np.max(all_data)
            bin_edges = np.linspace(data_min, data_max, 41)  # 40 bins
            
            # LEFT PANEL: Laser OFF
            ax_off = axes[0]
            
            # Plot histogram
            n_off, bins_off, patches_off = ax_off.hist(
                data_off, bins=bin_edges, 
                color='#4472C4', alpha=0.7, 
                edgecolor='black', linewidth=1.2
            )
            
            # Add mean line
            mean_off = stats_result.mean_off
            ax_off.axvline(mean_off, color='red', linestyle='--', linewidth=2.5,
                          label=f'Mean = {mean_off:.3f}', zorder=10)
            
            # Add median line
            median_off = stats_result.median_off
            ax_off.axvline(median_off, color='orange', linestyle=':', linewidth=2.5,
                          label=f'Median = {median_off:.3f}', zorder=10)
            
            # Format axes
            ax_off.set_xlabel(metric_label, fontsize=13, fontweight='bold')
            ax_off.set_ylabel('Count (Number of Cells)', fontsize=13, fontweight='bold')
            ax_off.set_title(f'Laser OFF\n(n = {stats_result.n_cells} cells)',
                           fontsize=14, fontweight='bold', pad=15)
            ax_off.grid(True, alpha=0.3, axis='y')
            ax_off.legend(loc='best', fontsize=11, frameon=True, framealpha=0.9)
            
            # Add statistics text box (top-right)
            stats_text_off = (
                f"Mean ± SEM:\n"
                f"{mean_off:.3f} ± {stats_result.sem_off:.3f}\n\n"
                f"Median:\n"
                f"{median_off:.3f}\n\n"
                f"SD:\n"
                f"{stats_result.std_off:.3f}\n\n"
                f"Range:\n"
                f"[{data_min:.3f}, {data_max:.3f}]"
            )
            
            ax_off.text(0.98, 0.98, stats_text_off, transform=ax_off.transAxes,
                       fontsize=10, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                                edgecolor='black', linewidth=1.5, alpha=0.95))
            
            # RIGHT PANEL: Laser ON
            ax_on = axes[1]
            
            # Plot histogram
            n_on, bins_on, patches_on = ax_on.hist(
                data_on, bins=bin_edges,
                color='#ED7D31', alpha=0.7,
                edgecolor='black', linewidth=1.2
            )
            
            # Add mean line
            mean_on = stats_result.mean_on
            ax_on.axvline(mean_on, color='red', linestyle='--', linewidth=2.5,
                         label=f'Mean = {mean_on:.3f}', zorder=10)
            
            # Add median line
            median_on = stats_result.median_on
            ax_on.axvline(median_on, color='orange', linestyle=':', linewidth=2.5,
                         label=f'Median = {median_on:.3f}', zorder=10)
            
            # Format axes
            ax_on.set_xlabel(metric_label, fontsize=13, fontweight='bold')
            ax_on.set_ylabel('Count (Number of Cells)', fontsize=13, fontweight='bold')
            ax_on.set_title(f'Laser ON\n(n = {stats_result.n_cells} cells)',
                          fontsize=14, fontweight='bold', pad=15)
            ax_on.grid(True, alpha=0.3, axis='y')
            ax_on.legend(loc='best', fontsize=11, frameon=True, framealpha=0.9)
            
            # Add statistics text box (top-right)
            stats_text_on = (
                f"Mean ± SEM:\n"
                f"{mean_on:.3f} ± {stats_result.sem_on:.3f}\n\n"
                f"Median:\n"
                f"{median_on:.3f}\n\n"
                f"SD:\n"
                f"{stats_result.std_on:.3f}\n\n"
                f"Δ Mean:\n"
                f"{stats_result.mean_diff:+.3f}"
            )
            
            ax_on.text(0.98, 0.98, stats_text_on, transform=ax_on.transAxes,
                      fontsize=10, verticalalignment='top', horizontalalignment='right',
                      bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                               edgecolor='black', linewidth=1.5, alpha=0.95))
            
            # Make y-axis ranges consistent for comparison
            y_max = max(np.max(n_off), np.max(n_on))
            ax_off.set_ylim([0, y_max * 1.15])
            ax_on.set_ylim([0, y_max * 1.15])
            
            # Overall figure title with statistical test results
            p_str = format_pvalue(stats_result.wilcoxon_pvalue)
            sig_label = get_significance_label(stats_result.wilcoxon_pvalue)
            
            fig.suptitle(
                f'{metric_label} Distribution: Laser OFF vs ON\n'
                f'Paired Wilcoxon Test: p = {p_str} {sig_label}, '
                f"Cohen's d = {stats_result.cohens_d:.3f}",
                fontsize=15, fontweight='bold', y=1.02)
            
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save figure (MOVED INSIDE LOOP)
            histogram_output_path = os.path.join(output_dir, f'{metric_key}_histogram_distribution.png')
            fig.savefig(histogram_output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            print(f"    Saved: {histogram_output_path}")


# =============================================================================
# NORMALIZED TUNING CURVE ANALYSIS MODULE
# =============================================================================

class NormalizedTuningAnalyzer:
    """Analyzes population-average tuning curves normalized to best frequency."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def compute_normalized_curves(
        self,
        df: pd.DataFrame,
        octave_bins: np.ndarray = None
    ):
        """
        Compute population-average tuning curves using metrics from CSV.
        
        Uses summary statistics (peak rate, mean rate, bandwidth) to construct
        synthetic tuning curves without reloading raw data.
        
        Args:
            df: DataFrame with tuning metrics from CSV
            octave_bins: Octave bins relative to best frequency (default: -2 to +2 in 0.25 steps)
        
        Returns:
            NormalizedTuningData with averaged curves for laser OFF and ON
        """
        if octave_bins is None:
            octave_bins = np.arange(-2.0, 2.25, 0.25)
        
        print(f"\n{'='*70}")
        print("COMPUTING NORMALIZED AVERAGE TUNING CURVES")
        print("="*70)
        print(f"  Octave bins: {octave_bins}")
        print(f"  Analyzing {len(df)} tuned cells")
        print(f"  NOTE: Using pre-computed metrics from CSV (no raw data reloading)")
        
        # Initialize accumulators for each octave bin
        n_bins = len(octave_bins)
        rates_off_all = [[] for _ in range(n_bins)]  # Absolute rates
        rates_on_all = [[] for _ in range(n_bins)]
        rates_off_norm_all = [[] for _ in range(n_bins)]  # Normalized to peak
        rates_on_norm_all = [[] for _ in range(n_bins)]
        
        # Process each cell - construct synthetic tuning curves from metrics
        n_cells_processed = 0
        n_cells_skipped = 0
        
        for idx, row in df.iterrows():
            # Extract metrics for laser OFF
            peak_rate_off = row['peak_rate_off']
            mean_rate_off = row['mean_rate_off']
            
            # Extract metrics for laser ON
            peak_rate_on = row['peak_rate_on']
            mean_rate_on = row['mean_rate_on']
            
            # Skip cells with invalid data
            if pd.isna(peak_rate_off) or peak_rate_off <= 0:
                n_cells_skipped += 1
                continue
            
            # Get bandwidth (use default if not available)
            if 'bandwidth_octaves_off' in row and not pd.isna(row['bandwidth_octaves_off']):
                bandwidth_off = row['bandwidth_octaves_off']
            else:
                bandwidth_off = 1.0  # Default bandwidth
            
            if 'bandwidth_octaves_on' in row and not pd.isna(row['bandwidth_octaves_on']):
                bandwidth_on = row['bandwidth_octaves_on']
            else:
                bandwidth_on = bandwidth_off  # Use same as OFF if not available
            
            # Create synthetic Gaussian tuning curves centered at octave 0 (best freq)
            sigma_off = bandwidth_off / 2.355
            sigma_on = bandwidth_on / 2.355
            
            # Tuning curve for laser OFF
            tuning_curve_off = mean_rate_off + (peak_rate_off - mean_rate_off) * \
                              np.exp(-(octave_bins**2) / (2 * sigma_off**2))
            
            # Tuning curve for laser ON
            baseline_on = mean_rate_on if not pd.isna(mean_rate_on) else 0
            peak_on = peak_rate_on if not pd.isna(peak_rate_on) else 0
            tuning_curve_on = baseline_on + (peak_on - baseline_on) * \
                             np.exp(-(octave_bins**2) / (2 * sigma_on**2))
            
            # Normalize to OFF peak
            tuning_curve_off_norm = tuning_curve_off / peak_rate_off
            tuning_curve_on_norm = tuning_curve_on / peak_rate_off
            
            # Add to bins
            for bin_idx in range(n_bins):
                rates_off_all[bin_idx].append(tuning_curve_off[bin_idx])
                rates_on_all[bin_idx].append(tuning_curve_on[bin_idx])
                rates_off_norm_all[bin_idx].append(tuning_curve_off_norm[bin_idx])
                rates_on_norm_all[bin_idx].append(tuning_curve_on_norm[bin_idx])
            
            n_cells_processed += 1
        
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
        
        print(f"  Successfully processed {n_cells_processed} cells")
        print(f"  Skipped {n_cells_skipped} cells (invalid metrics)")
        print(f"  Cells per bin: {n_cells_off[0]} (all bins have same count)")
        
        # Perform pointwise statistical tests
        print(f"\n  Performing pointwise statistical tests...")
        p_values = self._compute_pointwise_statistics(
            rates_off_all, rates_on_all, octave_bins
        )
        
        from collections import namedtuple
        NormalizedTuningData = namedtuple('NormalizedTuningData', [
            'octave_bins', 'mean_rates_off', 'sem_rates_off', 'n_cells_off',
            'mean_rates_on', 'sem_rates_on', 'n_cells_on',
            'mean_rates_off_normalized', 'sem_rates_off_normalized',
            'mean_rates_on_normalized', 'sem_rates_on_normalized',
            'p_values_absolute', 'p_values_normalized'  # NEW!
        ])
        
        # Also compute p-values for normalized data
        p_values_normalized = self._compute_pointwise_statistics(
            rates_off_norm_all, rates_on_norm_all, octave_bins
        )
        
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
            sem_rates_on_normalized=sem_rates_on_norm,
            p_values_absolute=p_values,  # NEW!
            p_values_normalized=p_values_normalized  # NEW!
        )
    
    @staticmethod
    def _compute_pointwise_statistics(
        rates_off_all: List[List[float]],
        rates_on_all: List[List[float]],
        octave_bins: np.ndarray,
        alpha: float = 0.05
    ) -> np.ndarray:
        """
        Perform paired Wilcoxon signed-rank test at each octave bin.
        
        Args:
            rates_off_all: List of lists, one per bin, containing OFF rates
            rates_on_all: List of lists, one per bin, containing ON rates
            octave_bins: Octave bin centers
            alpha: Significance threshold
        
        Returns:
            Array of p-values for each bin
        """
        n_bins = len(octave_bins)
        p_values = np.zeros(n_bins)
        
        for i in range(n_bins):
            rates_off = np.array(rates_off_all[i])
            rates_on = np.array(rates_on_all[i])
            
            if len(rates_off) < 3:  # Need at least 3 cells for test
                p_values[i] = np.nan
                continue
            
            try:
                # Paired Wilcoxon signed-rank test
                stat, p = stats.wilcoxon(rates_off, rates_on, alternative='two-sided')
                p_values[i] = p
            except Exception as e:
                p_values[i] = np.nan
        
        # Report significant bins
        sig_bins = np.where(p_values < alpha)[0]
        if len(sig_bins) > 0:
            print(f"    Significant bins (p < {alpha}): {len(sig_bins)}/{n_bins}")
            for bin_idx in sig_bins:
                print(f"      Octave {octave_bins[bin_idx]:.2f}: p = {p_values[bin_idx]:.4f}")
        else:
            print(f"    No significant bins (p < {alpha})")
        
        return p_values
    
    @staticmethod
    def plot_normalized_curves(norm_data, output_path: str):
        """Plot normalized average tuning curves with pointwise significance and shaded SEM."""
        print(f"\n  Generating normalized tuning curve plots...")
        
        # Define colorblind-friendly colors (matching selected cells script)
        color_off = '#56B4E9'  # Dull cyan - Laser OFF
        color_on = '#9E4784'   # Darker magenta/purple - Laser ON
        
        with figure_context(output_path, figsize=(14, 6)) as fig:
            # Plot 1: Absolute firing rates
            ax1 = fig.add_subplot(1, 2, 1)
            
            # Plot laser OFF with shaded SEM
            valid_off = ~np.isnan(norm_data.mean_rates_off)
            ax1.plot(
                norm_data.octave_bins[valid_off],
                norm_data.mean_rates_off[valid_off],
                marker='o', markersize=8, linewidth=2,
                color=color_off, label='Laser OFF', alpha=0.8, zorder=3
            )
            # Add shaded SEM region for OFF
            ax1.fill_between(
                norm_data.octave_bins[valid_off],
                norm_data.mean_rates_off[valid_off] - norm_data.sem_rates_off[valid_off],
                norm_data.mean_rates_off[valid_off] + norm_data.sem_rates_off[valid_off],
                color=color_off, alpha=0.3, zorder=2
            )
            
            # Plot laser ON with shaded SEM
            valid_on = ~np.isnan(norm_data.mean_rates_on)
            ax1.plot(
                norm_data.octave_bins[valid_on],
                norm_data.mean_rates_on[valid_on],
                marker='s', markersize=8, linewidth=2,
                color=color_on, label='Laser ON', alpha=0.8, zorder=3
            )
            # Add shaded SEM region for ON
            ax1.fill_between(
                norm_data.octave_bins[valid_on],
                norm_data.mean_rates_on[valid_on] - norm_data.sem_rates_on[valid_on],
                norm_data.mean_rates_on[valid_on] + norm_data.sem_rates_on[valid_on],
                color=color_on, alpha=0.3, zorder=2
            )
            
            # Add significance markers at bottom
            sig_bins_abs = norm_data.p_values_absolute < 0.05
            if np.any(sig_bins_abs):
                y_min = ax1.get_ylim()[0]
                ax1.scatter(
                    norm_data.octave_bins[sig_bins_abs],
                    np.ones(np.sum(sig_bins_abs)) * (y_min + 0.05 * np.ptp(ax1.get_ylim())),
                    marker='*', s=150, color='black', zorder=10,
                    label='p < 0.05'
                )
            
            ax1.axvline(0, color='black', linestyle='--', alpha=0.5, linewidth=1.5,
                       label='Best Frequency')
            ax1.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
            ax1.set_title('Population-Average Frequency Tuning\n(Absolute Firing Rates)',
                         fontsize=13, fontweight='bold')
            ax1.legend(loc='best', fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Normalized to peak
            ax2 = fig.add_subplot(1, 2, 2)
            
            # Plot laser OFF with shaded SEM
            ax2.plot(
                norm_data.octave_bins[valid_off],
                norm_data.mean_rates_off_normalized[valid_off],
                marker='o', markersize=8, linewidth=2,
                color=color_off, label='Laser OFF', alpha=0.8, zorder=3
            )
            # Add shaded SEM region for OFF
            ax2.fill_between(
                norm_data.octave_bins[valid_off],
                norm_data.mean_rates_off_normalized[valid_off] - norm_data.sem_rates_off_normalized[valid_off],
                norm_data.mean_rates_off_normalized[valid_off] + norm_data.sem_rates_off_normalized[valid_off],
                color=color_off, alpha=0.3, zorder=2
            )
            
            # Plot laser ON with shaded SEM
            ax2.plot(
                norm_data.octave_bins[valid_on],
                norm_data.mean_rates_on_normalized[valid_on],
                marker='s', markersize=8, linewidth=2,
                color=color_on, label='Laser ON', alpha=0.8, zorder=3
            )
            # Add shaded SEM region for ON
            ax2.fill_between(
                norm_data.octave_bins[valid_on],
                norm_data.mean_rates_on_normalized[valid_on] - norm_data.sem_rates_on_normalized[valid_on],
                norm_data.mean_rates_on_normalized[valid_on] + norm_data.sem_rates_on_normalized[valid_on],
                color=color_on, alpha=0.3, zorder=2
            )
            
            # Add significance markers at bottom
            sig_bins_norm = norm_data.p_values_normalized < 0.05
            if np.any(sig_bins_norm):
                ax2.scatter(
                    norm_data.octave_bins[sig_bins_norm],
                    np.ones(np.sum(sig_bins_norm)) * 0.05,
                    marker='*', s=150, color='black', zorder=10,
                    label='p < 0.05'
                )
            
            ax2.axvline(0, color='black', linestyle='--', alpha=0.5, linewidth=1.5,
                       label='Best Frequency')
            ax2.axhline(1.0, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
            ax2.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Normalized Firing Rate\n(Fraction of Peak)', fontsize=12, fontweight='bold')
            ax2.set_title('Population-Average Frequency Tuning\n(Normalized to Peak)',
                         fontsize=13, fontweight='bold')
            ax2.legend(loc='best', fontsize=10)
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim([0, 1.2])
            
            fig.suptitle('Normalized Frequency Tuning: Laser OFF vs ON\n'
                        f'(Tuned Cells, n = {norm_data.n_cells_off[norm_data.n_cells_off > 0].mean():.0f} cells/bin avg)\n'
                        f'* = significant difference (p < 0.05, paired Wilcoxon)',
                        fontsize=14, fontweight='bold', y=1.02)
            
            fig.tight_layout()
        
        print(f"    Saved: {output_path}")
    
    @staticmethod
    def save_normalized_data(norm_data, output_path: str):
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
            'sem_rate_on_normalized': norm_data.sem_rates_on_normalized,
            'p_value_absolute': norm_data.p_values_absolute,  # NEW!
            'p_value_normalized': norm_data.p_values_normalized,  # NEW!
            'significant_abs': norm_data.p_values_absolute < 0.05,  # NEW!
            'significant_norm': norm_data.p_values_normalized < 0.05  # NEW!
        })
        
        df.to_csv(output_path, index=False)
        print(f"    Saved: {output_path}")


# =============================================================================
# OUTPUT MODULE
# =============================================================================

class ResultsSaver:
    """Handles saving of analysis results."""
    
    def __init__(self, metrics_dir: str):
        """Initialize with base metrics directory."""
        self.output_dir = os.path.join(metrics_dir, 'laser_statistics')
        os.makedirs(self.output_dir, exist_ok=True)
    
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
        self.saver = ResultsSaver(config.metrics_dir)
        self.output_dir = self.saver.output_dir
    
    def run(self):
        """Execute the complete analysis pipeline."""
        print("="*70)
        print("STATISTICAL COMPARISON: LASER OFF vs ON (TUNED CELLS ONLY)")
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
        
        # NEW: Generate histogram distribution plots
        self.plotter.create_histogram_distributions(
            df_complete, stats_results, self.output_dir
        )
        
        # 9. Generate normalized average tuning curves
        print(f"\n{'='*70}")
        print("GENERATING NORMALIZED POPULATION TUNING CURVES")
        print(f"{'='*70}")
        
        # Create normalized tuning analyzer
        norm_analyzer = NormalizedTuningAnalyzer(self.config)
        
        # Compute normalized curves using CSV metrics
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
        
        print(f"\n  Additional files:")
        print(f"  - Normalized tuning plot: {norm_plot_path}")
        print(f"  - Normalized tuning data: {norm_csv_path}")
        print(f"  - Selectivity histogram: {os.path.join(self.output_dir, 'selectivity_histogram_distribution.png')}")
        print(f"  - Tuning quality histogram: {os.path.join(self.output_dir, 'tuning_quality_histogram_distribution.png')}")
        
        return df_complete, stats_results


# =============================================================================
# FILTERED ANALYSIS COORDINATOR (NEW!)
# =============================================================================

class FilteredAnalysisCoordinator:
    """
    Coordinates filtered analysis for cells with meaningful selectivity changes.
    
    Filters to cells where |ΔSI| ≥ threshold (default 0.05).
    Runs same analysis pipeline as main coordinator but saves to separate directory.
    """
    
    def __init__(self, config: AnalysisConfig, si_threshold: float = 0.05):
        self.config = config
        self.si_threshold = si_threshold
        self.metrics_loader = MetricsLoader(config)
        self.analyzer = StatisticalAnalyzer(config)
        self.plotter = ComparisonPlotter()
        
        # Create separate output directory for filtered analysis
        filtered_output_dir = os.path.join(config.metrics_dir, 'laser_statistics_SI_filtered')
        self.saver = ResultsSaver(filtered_output_dir)
        self.output_dir = self.saver.output_dir
    
    def run(self, df_complete: pd.DataFrame):
        """
        Execute filtered analysis pipeline.
        
        Args:
            df_complete: Complete dataset from main analysis (to avoid re-loading)
        """
        print("\n" + "="*70)
        print("FILTERED ANALYSIS: CELLS WITH MEANINGFUL SI CHANGES")
        print(f"Filter: |ΔSI| ≥ {self.si_threshold}")
        print("="*70)
        
        # Filter to cells with meaningful SI changes
        df_filtered, filter_report = self._filter_by_si_change(df_complete)
        
        if len(df_filtered) < self.config.min_cells_for_stats:
            print(f"\n✗ Insufficient cells after filtering ({len(df_filtered)} < {self.config.min_cells_for_stats})")
            print("  Skipping filtered analysis.")
            return None, None
        
        # Print filtering results
        self._print_filter_report(filter_report)
        
        # Save filtered merged data
        csv_comparison = self.saver.save_merged_data(df_filtered)
        
        # Perform statistical analysis on filtered data
        stats_results = self.analyzer.analyze_all_metrics(df_filtered)
        
        # Save statistical results
        csv_stats = self.saver.save_statistical_results(stats_results)
        
        # Generate plots
        print(f"\n{'='*70}")
        print("GENERATING COMPARISON PLOTS (FILTERED)")
        print(f"{'='*70}")
        
        pdf_path = os.path.join(self.output_dir, 'laser_on_vs_off_comparison_SI_filtered.pdf')
        self.plotter.create_comparison_pdf(df_filtered, stats_results, pdf_path)
        
        # Generate histogram distribution plots
        self.plotter.create_histogram_distributions(
            df_filtered, stats_results, self.output_dir
        )
        
        # Generate normalized average tuning curves
        print(f"\n{'='*70}")
        print("GENERATING NORMALIZED POPULATION TUNING CURVES (FILTERED)")
        print(f"{'='*70}")
        
        norm_analyzer = NormalizedTuningAnalyzer(self.config)
        norm_data = norm_analyzer.compute_normalized_curves(df_filtered)
        
        norm_plot_path = os.path.join(self.output_dir, 'normalized_tuning_curves_SI_filtered.png')
        norm_analyzer.plot_normalized_curves(norm_data, norm_plot_path)
        
        norm_csv_path = os.path.join(self.output_dir, 'normalized_tuning_data_SI_filtered.csv')
        norm_analyzer.save_normalized_data(norm_data, norm_csv_path)
        
        # Print summary
        self.saver.print_summary(
            df_filtered, stats_results,
            csv_comparison, csv_stats, pdf_path
        )
        
        print(f"\n  Additional filtered analysis files:")
        print(f"  - Normalized tuning plot: {norm_plot_path}")
        print(f"  - Normalized tuning data: {norm_csv_path}")
        print(f"  - Selectivity histogram: {os.path.join(self.output_dir, 'selectivity_histogram_distribution.png')}")
        print(f"  - Tuning quality histogram: {os.path.join(self.output_dir, 'tuning_quality_histogram_distribution.png')}")
        
        return df_filtered, stats_results
    
    def _filter_by_si_change(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Filter to cells with |ΔSI| ≥ threshold.
        
        Args:
            df: Complete dataset
        
        Returns:
            Tuple of (filtered_df, filter_report_dict)
        """
        # Calculate ΔSI for each cell
        df['delta_SI'] = df['selectivity_on'] - df['selectivity_off']
        df['abs_delta_SI'] = np.abs(df['delta_SI'])
        
        # Apply filter
        n_before = len(df)
        df_filtered = df[df['abs_delta_SI'] >= self.si_threshold].copy()
        n_after = len(df_filtered)
        n_excluded = n_before - n_after
        
        # Count cells that increased vs decreased
        n_increased = np.sum(df_filtered['delta_SI'] > 0)
        n_decreased = np.sum(df_filtered['delta_SI'] < 0)
        
        # Distribution of ΔSI values
        delta_si_mean = np.mean(df_filtered['delta_SI'])
        delta_si_median = np.median(df_filtered['delta_SI'])
        delta_si_std = np.std(df_filtered['delta_SI'])
        
        filter_report = {
            'n_before': n_before,
            'n_after': n_after,
            'n_excluded': n_excluded,
            'percent_passed': (n_after / n_before * 100) if n_before > 0 else 0,
            'n_increased': n_increased,
            'n_decreased': n_decreased,
            'delta_si_mean': delta_si_mean,
            'delta_si_median': delta_si_median,
            'delta_si_std': delta_si_std,
            'threshold': self.si_threshold
        }
        
        return df_filtered, filter_report
    
    @staticmethod
    def _print_filter_report(report: Dict):
        """Print detailed filtering report."""
        print(f"\n{'='*70}")
        print("FILTERING RESULTS")
        print(f"{'='*70}")
        print(f"  SI Change Threshold: ±{report['threshold']}")
        print(f"\n  Before filtering: {report['n_before']} cells")
        print(f"  After filtering:  {report['n_after']} cells ({report['percent_passed']:.1f}% passed)")
        print(f"  Excluded:         {report['n_excluded']} cells ({100 - report['percent_passed']:.1f}%)")
        
        print(f"\n  Direction of SI changes:")
        print(f"    Increased SI (ΔSI > 0): {report['n_increased']} cells")
        print(f"    Decreased SI (ΔSI < 0): {report['n_decreased']} cells")
        
        print(f"\n  ΔSI Distribution (filtered cells):")
        print(f"    Mean:   {report['delta_si_mean']:+.4f}")
        print(f"    Median: {report['delta_si_median']:+.4f}")
        print(f"    Std:    {report['delta_si_std']:.4f}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main execution: Perform statistical analysis of laser effects."""
    config = AnalysisConfig()
    
    # =========================================================================
    # MAIN ANALYSIS (ALL TUNED CELLS)
    # =========================================================================
    print("="*70)
    print("MAIN ANALYSIS: ALL TUNED CELLS")
    print("="*70)
    
    coordinator = StatisticalAnalysisCoordinator(config)
    
    try:
        df_results, stats_results = coordinator.run()
        print("\n✓ Main analysis completed successfully!")
        
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
    
    # =========================================================================
    # FILTERED ANALYSIS (CELLS WITH MEANINGFUL SI CHANGES)
    # =========================================================================
    print("\n\n" + "="*70)
    print("FILTERED ANALYSIS: CELLS WITH MEANINGFUL SI CHANGES")
    print("="*70)
    
    filtered_coordinator = FilteredAnalysisCoordinator(config, si_threshold=0.05)
    
    try:
        df_filtered, stats_filtered = filtered_coordinator.run(df_results)
        
        if df_filtered is not None:
            print("\n✓ Filtered analysis completed successfully!")
        
    except Exception as e:
        print(f"\n✗ ERROR in filtered analysis: {e}")
        import traceback
        traceback.print_exc()
        print("  Main analysis results are still valid.")
    
    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n\n" + "="*70)
    print("ALL ANALYSES COMPLETE")
    print("="*70)
    print(f"\nMain analysis (all tuned cells):")
    print(f"  - {len(df_results)} cells analyzed")
    print(f"  - Output: {coordinator.output_dir}")
    
    if df_filtered is not None:
        print(f"\nFiltered analysis (|ΔSI| ≥ 0.05):")
        print(f"  - {len(df_filtered)} cells analyzed")
        print(f"  - Output: {filtered_coordinator.output_dir}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
