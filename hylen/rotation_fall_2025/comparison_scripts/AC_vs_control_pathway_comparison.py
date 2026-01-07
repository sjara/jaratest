"""
AC-pStr Experimental vs Control Comparison Analysis

Compares the effects of optogenetic inhibition of AC-pStr pathway in experimental
animals (ArchT) vs control animals (no opsin expression) on auditory cortex
frequency tuning properties.

Datasets:
- AC-pStr Experimental: arch018, arch019, arch020, arch022 (ArchT expressing)
- AC-pStr Control: Control animals (laser locked with light)

Analysis:
1. Load pre-computed metrics from both groups' CSV files
2. Compare distributions of laser effects between experimental and control groups
3. Statistical tests (Wilcoxon signed-rank, within-group effects)
4. Visualization of group-specific effects

Author: Hylen
Date: 2025
"""

import os
import sys
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages

# Add hylen directory to path
sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class ComparisonConfig:
    """Configuration for experimental vs control comparison analysis."""
    # Tuning type: 'frequency' or 'am'
    tuning_type: str = 'frequency'
    
    # Analysis parameters
    min_cells_for_stats: int = 3
    alpha: float = 0.01  # Significance threshold
    
    # Metrics to compare (metric_name: ylabel)
    metrics_to_plot: Dict[str, str] = None
    
    def __post_init__(self):
        """Set default metrics based on tuning type."""
        # Set default metrics to plot
        if self.metrics_to_plot is None:
            object.__setattr__(self, 'metrics_to_plot', {
                'tuning_quality': 'Tuning Quality',
                'bandwidth_octaves': 'Bandwidth (octaves)',
                'selectivity_index': 'Selectivity Index',
                'sparseness': 'Sparseness',
                'peak_rate': 'Peak Firing Rate (Hz)',
                'mean_rate': 'Mean Firing Rate (Hz)',
            })
    
    @property
    def experimental_dir(self) -> str:
        """Get Experimental (AC-pStr ArchT) data directory based on tuning type."""
        if self.tuning_type == 'frequency':
            return str(get_reports_subdir('tuning_freq_analysis'))
        elif self.tuning_type == 'am':
            return str(get_reports_subdir('tuning_AM_analysis'))
        else:
            raise ValueError(f"Unknown tuning_type: {self.tuning_type}")
    
    @property
    def control_dir(self) -> str:
        """Get Control group data directory based on tuning type."""
        if self.tuning_type == 'frequency':
            return str(get_reports_subdir('control_group/tuning_freq_analysis'))
        elif self.tuning_type == 'am':
            return str(get_reports_subdir('control_group/tuning_AM_analysis'))
        else:
            raise ValueError(f"Unknown tuning_type: {self.tuning_type}")
    
    @property
    def output_dir(self) -> str:
        """Get output directory based on tuning type."""
        if self.tuning_type == 'frequency':
            return str(get_reports_subdir('archT_AC_control_comparison_freq'))
        elif self.tuning_type == 'am':
            return str(get_reports_subdir('archT_AC_control_comparison_AM'))
        else:
            raise ValueError(f"Unknown tuning_type: {self.tuning_type}")


# =============================================================================
# DATA LOADING
# =============================================================================

class GroupDataLoader:
    """Loads and organizes data from both experimental and control groups."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
    
    def load_both_groups(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load metrics from both experimental and control datasets.
        
        Returns:
            Tuple of (experimental_df, control_df) with laser effects calculated
        """
        print("="*70)
        print("LOADING GROUP DATA")
        print("="*70)
        
        # Load Experimental data (ArchT animals)
        print("\nLoading Experimental group (ArchT)...")
        exp_df = self._load_group_data(
            self.config.experimental_dir,
            group_label='Experimental'
        )
        
        # Load Control data (no opsin)
        print("\nLoading Control group...")
        ctrl_df = self._load_group_data(
            self.config.control_dir,
            group_label='Control'
        )
        
        return exp_df, ctrl_df
    
    def _load_group_data(self, metrics_dir: str, group_label: str) -> pd.DataFrame:
        """Load and process data for one pathway."""
        csv_off = os.path.join(metrics_dir, 'all_sessions_laser_off_tuning_metrics.csv')
        csv_on = os.path.join(metrics_dir, 'all_sessions_laser_on_tuning_metrics.csv')
        
        if not os.path.exists(csv_off) or not os.path.exists(csv_on):
            raise FileNotFoundError(f"CSV files not found in {metrics_dir}")
        
        df_off = pd.read_csv(csv_off)
        df_on = pd.read_csv(csv_on)
        
        print(f"  Laser OFF: {len(df_off)} cells")
        print(f"  Laser ON:  {len(df_on)} cells")
        
        # Merge on session_id and cell_idx
        df_merged = pd.merge(df_off, df_on, on=['session_id', 'cell_idx'],
                            how='left', suffixes=('_off', '_on'))
        
        # Add unique cell identifier (subject_date_depth_cellIdx)
        df_merged['cell_id'] = (
            df_merged['subject_off'] + '_' + 
            df_merged['date_off'] + '_' + 
            df_merged['depth_off'].astype(str) + '_' + 
            df_merged['cell_idx'].astype(str)
        )
        
        # Calculate laser effects
        df_merged = self._calculate_laser_effects(df_merged)
        
        # Filter to tuned cells with valid laser ON data
        # Only require the core metrics that are most reliably calculated
        # Make bandwidth optional since it can be hard to calculate for AM tuning
        mean_rate_off = 'mean_rate_off' if 'mean_rate_off' in df_merged.columns else 'mean_response_off'
        mean_rate_on = 'mean_rate_on' if 'mean_rate_on' in df_merged.columns else 'mean_response_on'
        peak_rate_off = 'peak_rate_off' if 'peak_rate_off' in df_merged.columns else 'peak_response_off'
        peak_rate_on = 'peak_rate_on' if 'peak_rate_on' in df_merged.columns else 'peak_response_on'
        
        # Core metrics that should always be available
        required_cols_off = ['tuning_quality_off', 'selectivity_index_off', 
                            'sparseness_off', peak_rate_off, mean_rate_off]
        required_cols_on = ['tuning_quality_on', 'selectivity_index_on',
                           'sparseness_on', peak_rate_on, mean_rate_on]
        
        # Bandwidth is optional (especially for AM data)
        # We'll still plot it when available, but don't require it for inclusion
        
        df_tuned = df_merged[
            (df_merged['tuning_category_off'] == 'tuned') & 
            (~df_merged['delta_tq'].isna())
        ].copy()
        
        # Count cells before filtering for complete data
        n_before = len(df_tuned)
        
        # Filter to cells with complete data in both conditions (for core metrics)
        df_tuned = df_tuned.dropna(subset=required_cols_off + required_cols_on)
        
        n_after = len(df_tuned)
        
        # Add group label
        df_tuned['group'] = group_label
        
        print(f"  Tuned cells with laser ON data: {n_before}")
        print(f"  Cells with complete OFF and ON data: {n_after}")
        if n_before != n_after:
            print(f"  Note: {n_before - n_after} cells excluded due to missing data in one or both conditions")
        
        # Report how many cells have bandwidth data
        n_with_bandwidth = df_tuned[['bandwidth_octaves_off', 'bandwidth_octaves_on']].dropna().shape[0]
        print(f"  Cells with bandwidth data: {n_with_bandwidth}/{n_after}")
        
        return df_tuned
    
    @staticmethod
    def _calculate_laser_effects(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate laser effect metrics."""
        # Tuning quality change
        if 'tuning_quality_on' in df.columns and 'tuning_quality_off' in df.columns:
            df['delta_tq'] = df['tuning_quality_on'] - df['tuning_quality_off']
        
        # Firing rate changes (check for column names)
        # Frequency tuning uses 'mean_rate', 'peak_rate'
        # AM tuning uses 'mean_response', 'peak_response'
        mean_rate_off_col = 'mean_rate_off' if 'mean_rate_off' in df.columns else 'mean_response_off'
        mean_rate_on_col = 'mean_rate_on' if 'mean_rate_on' in df.columns else 'mean_response_on'
        peak_rate_off_col = 'peak_rate_off' if 'peak_rate_off' in df.columns else 'peak_response_off'
        peak_rate_on_col = 'peak_rate_on' if 'peak_rate_on' in df.columns else 'peak_response_on'
        
        if mean_rate_on_col in df.columns and mean_rate_off_col in df.columns:
            df['percent_fr_change'] = ((df[mean_rate_on_col] - df[mean_rate_off_col]) / 
                                       df[mean_rate_off_col] * 100)
            # Rename for consistency
            if mean_rate_off_col != 'mean_rate_off':
                df['mean_rate_off'] = df[mean_rate_off_col]
                df['mean_rate_on'] = df[mean_rate_on_col]
        
        if peak_rate_on_col in df.columns and peak_rate_off_col in df.columns:
            df['percent_peak_change'] = ((df[peak_rate_on_col] - df[peak_rate_off_col]) / 
                                         df[peak_rate_off_col] * 100)
            # Rename for consistency
            if peak_rate_off_col != 'peak_rate_off':
                df['peak_rate_off'] = df[peak_rate_off_col]
                df['peak_rate_on'] = df[peak_rate_on_col]
        
        # Other metric changes
        if 'selectivity_index_on' in df.columns and 'selectivity_index_off' in df.columns:
            df['delta_selectivity'] = df['selectivity_index_on'] - df['selectivity_index_off']
        
        if 'sparseness_on' in df.columns and 'sparseness_off' in df.columns:
            df['delta_sparseness'] = df['sparseness_on'] - df['sparseness_off']
        
        if 'bandwidth_octaves_on' in df.columns and 'bandwidth_octaves_off' in df.columns:
            df['delta_bandwidth'] = df['bandwidth_octaves_on'] - df['bandwidth_octaves_off']
        
        # Best frequency/rate shift (in octaves)
        # Frequency data: best_freq_on/off
        # AM data: best_rate_on/off
        if 'best_freq_on' in df.columns and 'best_freq_off' in df.columns:
            df['delta_best_freq_octaves'] = np.log2(df['best_freq_on'] / df['best_freq_off'])
        elif 'best_rate_on' in df.columns and 'best_rate_off' in df.columns:
            # For AM, also calculate shift in octaves
            df['delta_best_freq_octaves'] = np.log2(df['best_rate_on'] / df['best_rate_off'])
            # Rename for consistency
            df['best_freq_off'] = df['best_rate_off']
            df['best_freq_on'] = df['best_rate_on']
        
        return df


# =============================================================================
# STATISTICAL COMPARISON
# =============================================================================

class GroupComparator:
    """Performs statistical comparisons between experimental and control groups."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
    
    def test_within_group_effects(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        metric_name: str
    ) -> Dict:
        """
        Test if laser has significant effect within each group for a given metric.
        
        Args:
            exp_df: Experimental group data
            ctrl_df: Control group data
            metric_name: Name of the metric column (e.g., 'tuning_quality', 'bandwidth_octaves')
        
        Returns:
            Dictionary with statistics for each group
        """
        results = {}
        
        # Test Experimental group
        # Get valid paired data (cells with both OFF and ON measurements)
        exp_off_col = f'{metric_name}_off'
        exp_on_col = f'{metric_name}_on'
        
        # Filter to rows where both OFF and ON are not NaN
        exp_valid = exp_df[[exp_off_col, exp_on_col]].dropna()
        exp_off = exp_valid[exp_off_col].values
        exp_on = exp_valid[exp_on_col].values
        
        # Paired test (same cells OFF vs ON)
        if len(exp_off) >= self.config.min_cells_for_stats:
            exp_stat, exp_p = stats.wilcoxon(exp_off, exp_on, alternative='two-sided')
        else:
            exp_p = np.nan
        
        exp_mean_off = np.mean(exp_off)
        exp_mean_on = np.mean(exp_on)
        exp_sem_off = np.std(exp_off) / np.sqrt(len(exp_off))
        exp_sem_on = np.std(exp_on) / np.sqrt(len(exp_on))
        
        results['Experimental'] = {
            'n': len(exp_off),
            'mean_off': exp_mean_off,
            'sem_off': exp_sem_off,
            'mean_on': exp_mean_on,
            'sem_on': exp_sem_on,
            'p_value': exp_p,
            'significant': exp_p < self.config.alpha if not np.isnan(exp_p) else False
        }
        
        # Test Control group
        ctrl_off_col = f'{metric_name}_off'
        ctrl_on_col = f'{metric_name}_on'
        
        # Filter to rows where both OFF and ON are not NaN
        ctrl_valid = ctrl_df[[ctrl_off_col, ctrl_on_col]].dropna()
        ctrl_off = ctrl_valid[ctrl_off_col].values
        ctrl_on = ctrl_valid[ctrl_on_col].values
        
        if len(ctrl_off) >= self.config.min_cells_for_stats:
            ctrl_stat, ctrl_p = stats.wilcoxon(ctrl_off, ctrl_on, alternative='two-sided')
        else:
            ctrl_p = np.nan
        
        ctrl_mean_off = np.mean(ctrl_off)
        ctrl_mean_on = np.mean(ctrl_on)
        ctrl_sem_off = np.std(ctrl_off) / np.sqrt(len(ctrl_off))
        ctrl_sem_on = np.std(ctrl_on) / np.sqrt(len(ctrl_on))
        
        results['Control'] = {
            'n': len(ctrl_off),
            'mean_off': ctrl_mean_off,
            'sem_off': ctrl_sem_off,
            'mean_on': ctrl_mean_on,
            'sem_on': ctrl_sem_on,
            'p_value': ctrl_p,
            'significant': ctrl_p < self.config.alpha if not np.isnan(ctrl_p) else False
        }
        
        return results
    
    def test_all_metrics(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        metrics_to_test: Dict[str, str]
    ) -> Dict[str, Dict]:
        """
        Test all metrics for both groups.
        
        Returns:
            Dictionary mapping metric names to their statistics
        """
        print("\n" + "="*70)
        print("WITHIN-GROUP LASER EFFECTS - ALL METRICS")
        print("="*70)
        
        all_results = {}
        
        for metric_name, metric_label in metrics_to_test.items():
            print(f"\n{metric_label}:")
            print("-" * 50)
            
            results = self.test_within_group_effects(exp_df, ctrl_df, metric_name)
            
            # Print Experimental results
            exp_stats = results['Experimental']
            sig_str = '***' if exp_stats['p_value'] < 0.001 else '**' if exp_stats['p_value'] < 0.01 else '*' if exp_stats['p_value'] < 0.05 else 'ns'
            print(f"  Experimental (n={exp_stats['n']}): OFF={exp_stats['mean_off']:.3f}, ON={exp_stats['mean_on']:.3f}, p={exp_stats['p_value']:.2e} {sig_str}")
            
            # Print Control results
            ctrl_stats = results['Control']
            sig_str = '***' if ctrl_stats['p_value'] < 0.001 else '**' if ctrl_stats['p_value'] < 0.01 else '*' if ctrl_stats['p_value'] < 0.05 else 'ns'
            print(f"  Control (n={ctrl_stats['n']}): OFF={ctrl_stats['mean_off']:.3f}, ON={ctrl_stats['mean_on']:.3f}, p={ctrl_stats['p_value']:.2e} {sig_str}")
            
            all_results[metric_name] = results
        
        return all_results


# =============================================================================
# VISUALIZATION
# =============================================================================

class GroupVisualizer:
    """Creates comparison visualizations."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
        # Define colorblind-friendly colors (matching selected cells and statistics scripts)
        self.color_off = '#56B4E9'  # Dull cyan - Laser OFF
        self.color_on = '#9E4784'   # Darker magenta/purple - Laser ON
    
    def create_basic_comparison_plot(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        within_group_stats: Dict,
        metric_label: str,
        output_dir: str,
        filename: str
    ):
        """
        Create a simple bar chart comparing a metric:
        Laser OFF vs ON for Experimental and Control groups.
        
        Args:
            exp_df: Experimental data
            ctrl_df: Control data
            within_group_stats: Statistics for this metric
            metric_label: Label for y-axis (e.g., 'Tuning Quality')
            output_dir: Directory to save the plot
            filename: Output filename
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract statistics
        exp_stats = within_group_stats['Experimental']
        ctrl_stats = within_group_stats['Control']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Prepare data
        x_positions = [1, 2, 4, 5]  # Group 1: Exp OFF/ON, Group 2: Ctrl OFF/ON
        means = [
            exp_stats['mean_off'],
            exp_stats['mean_on'],
            ctrl_stats['mean_off'],
            ctrl_stats['mean_on']
        ]
        sems = [
            exp_stats['sem_off'],
            exp_stats['sem_on'],
            ctrl_stats['sem_off'],
            ctrl_stats['sem_on']
        ]
        # Updated colors: cyan for OFF, magenta for ON (both groups)
        colors = [self.color_off, self.color_on, self.color_off, self.color_on]
        
        # Create bars
        bars = ax.bar(x_positions, means, yerr=sems, capsize=8,
                     color=colors, edgecolor='black', linewidth=1.5,
                     alpha=0.8, width=0.7)
        
        # Add value labels on bars
        for bar, mean, sem in zip(bars, means, sems):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + sem,
                   f'{mean:.3f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Add significance brackets and p-values
        self._add_significance_bracket(ax, 1, 2, means[0:2], sems[0:2], exp_stats)
        self._add_significance_bracket(ax, 4, 5, means[2:4], sems[2:4], ctrl_stats)
        
        # Format axes
        ax.set_ylabel(metric_label, fontsize=13, fontweight='bold')
        ax.set_xticks([1.5, 4.5])
        ax.set_xticklabels(['Experimental\n(ArchT)', 'Control\n(Laser blocked)'], 
                          fontsize=12, fontweight='bold')
        ax.set_xlim([0, 6])
        
        # Set y-limit with extra space at top for sample size annotations
        y_max = max(means) + max(sems) + 0.25
        ax.set_ylim([0, y_max])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add legend and sample sizes at fixed top position
        self._add_legend(ax)
        self._add_sample_sizes_top(ax, exp_stats, ctrl_stats, y_max)
        
        # Title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        ax.set_title(f'{metric_label}: Laser OFF vs ON Comparison\nExperimental vs Control ({tuning_label})',
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, filename)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
    
    def create_all_metric_plots(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        all_stats: Dict[str, Dict],
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create bar charts for all metrics.
        
        Args:
            exp_df: Experimental data
            ctrl_df: Control data
            all_stats: Dictionary of statistics for all metrics
            metrics_to_plot: Dictionary mapping metric names to labels
            output_dir: Directory to save plots
        """
        print("\n" + "="*70)
        print("GENERATING COMPARISON PLOTS FOR ALL METRICS")
        print("="*70)
        
        for metric_name, metric_label in metrics_to_plot.items():
            print(f"\n  Creating plot for {metric_label}...")
            
            filename = f'{metric_name}_comparison.png'
            output_path = self.create_basic_comparison_plot(
                exp_df, ctrl_df,
                all_stats[metric_name],
                metric_label,
                output_dir,
                filename
            )
            print(f"    Saved: {output_path}")
    
    def create_population_tuning_curves(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 4-panel figure showing population-average frequency tuning curves.
        
        Panel layout:
        - Top left: Experimental Laser OFF
        - Bottom left: Experimental Laser ON
        - Top right: Control Laser OFF
        - Bottom right: Control Laser ON
        
        X-axis: Octaves from best frequency
        Y-axis: Normalized firing rate
        """
        print("\n" + "="*70)
        print("GENERATING POPULATION TUNING CURVES")
        print("="*70)
        
        # Create figure with 2x2 subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Define conditions with updated colors
        conditions = [
            (exp_df, 'off', 'Experimental Laser OFF', axes[0, 0], self.color_off),
            (exp_df, 'on', 'Experimental Laser ON', axes[1, 0], self.color_on),
            (ctrl_df, 'off', 'Control Laser OFF', axes[0, 1], self.color_off),
            (ctrl_df, 'on', 'Control Laser ON', axes[1, 1], self.color_on)
        ]
        
        for df, condition, title, ax, color in conditions:
            print(f"\n  Processing {title}...")
            
            # Calculate population tuning curve
            octaves, mean_rates, sem_rates, n_cells = self._calculate_population_tuning(
                df, condition
            )
            
            # Plot mean with SEM
            ax.plot(octaves, mean_rates, '-o', color=color, linewidth=2.5, 
                   markersize=6, label='Mean', markeredgecolor='black', markeredgewidth=0.5)
            ax.fill_between(octaves, mean_rates - sem_rates, mean_rates + sem_rates,
                           color=color, alpha=0.3, label='SEM')
            
            # Format axes
            ax.set_xlabel('Octaves from Best Frequency', fontsize=11, fontweight='bold')
            ax.set_ylabel('Firing Rate (Hz)', fontsize=11, fontweight='bold')
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Best Freq')
            ax.grid(True, alpha=0.3)
            ax.legend(loc='best', fontsize=9)
            
            # Add n cells annotation
            ax.text(0.02, 0.98, f'n = {n_cells} cells', 
                   transform=ax.transAxes, ha='left', va='top',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                            edgecolor='black', linewidth=1.5, alpha=0.9))
        
        # Overall title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        fig.suptitle(f'Population-Average Tuning Curves\nExperimental vs Control ({tuning_label})',
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_curves.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Population tuning curves saved: {output_path}")
    
    def create_population_tuning_comparison(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 2-panel figure comparing laser OFF vs ON conditions.
        
        Panel layout:
        - Left: Experimental (Laser OFF and ON overlaid)
        - Right: Control (Laser OFF and ON overlaid)
        
        X-axis: Octaves from best frequency
        Y-axis: Firing rate (Hz)
        """
        print("\n" + "="*70)
        print("GENERATING POPULATION TUNING COMPARISON (ON/OFF OVERLAID)")
        print("="*70)
        
        # Create figure with 1x2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Panel 1: Experimental (OFF and ON)
        print("\n  Processing Experimental...")
        ax = axes[0]
        
        # Calculate tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(exp_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(exp_df, 'on')
        
        # Plot OFF condition (cyan)
        ax.plot(octaves_off, mean_off, '-o', color=self.color_off, linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})', 
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color=self.color_off, alpha=0.3)
        
        # Plot ON condition (magenta)
        ax.plot(octaves_on, mean_on, '-o', color=self.color_on, linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color=self.color_on, alpha=0.3)
        
        # Format Experimental panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_title('Experimental Group\n(ArchT)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Panel 2: Control (OFF and ON)
        print("\n  Processing Control...")
        ax = axes[1]
        
        # Calculate tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(ctrl_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(ctrl_df, 'on')
        
        # Plot OFF condition (cyan)
        ax.plot(octaves_off, mean_off, '-o', color=self.color_off, linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color=self.color_off, alpha=0.3)
        
        # Plot ON condition (magenta)
        ax.plot(octaves_on, mean_on, '-o', color=self.color_on, linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color=self.color_on, alpha=0.3)
        
        # Format Control panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_title('Control Group\n(Laser Blocked)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Overall title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        fig.suptitle(f'Population Tuning Curves: Laser OFF vs ON Comparison ({tuning_label})',
                    fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_comparison_overlaid.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Population tuning comparison saved: {output_path}")
    
    @staticmethod
    def _calculate_population_tuning(
        df: pd.DataFrame,
        condition: str
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int]:
        """
        Calculate population-average tuning curve aligned to best frequency.
        
        Args:
            df: DataFrame with tuning data
            condition: 'off' or 'on'
        
        Returns:
            octaves: Array of octave distances from BF
            mean_rates: Mean firing rate at each octave distance
            sem_rates: SEM of firing rate at each octave distance
            n_cells: Number of cells included
        """
        # We need to reconstruct tuning curves from the summary statistics
        # Since we don't have the full tuning curves in the CSV, we'll create
        # a simplified representation using available metrics
        
        # For now, create a representative tuning curve using:
        # - Best frequency (octave 0)
        # - Peak rate at BF
        # - Bandwidth to estimate curve width (if available)
        # - Mean rate for baseline
        
        best_freq_col = f'best_freq_{condition}'
        peak_rate_col = f'peak_rate_{condition}'
        mean_rate_col = f'mean_rate_{condition}'
        bandwidth_col = f'bandwidth_octaves_{condition}'
        
        # IMPORTANT: Filter to cells that have valid data in BOTH conditions
        # This ensures we're comparing the same population of cells
        # But make bandwidth OPTIONAL
        required_cols_off = ['best_freq_off', 'peak_rate_off', 'mean_rate_off']
        required_cols_on = ['best_freq_on', 'peak_rate_on', 'mean_rate_on']
        
        # Only use cells with valid data in both OFF and ON (core metrics only)
        valid_data = df[required_cols_off + required_cols_on].dropna()
        
        if len(valid_data) == 0:
            # Return empty arrays if no valid data
            return np.array([]), np.array([]), np.array([]), 0
        
        # Define octave range (e.g., -3 to +3 octaves from BF)
        octave_range = np.linspace(-3, 3, 13)
        
        # For each cell, create a synthetic tuning curve
        all_tuning_curves = []
        
        for _, row in valid_data.iterrows():
            peak_rate = row[peak_rate_col]
            mean_rate = row[mean_rate_col]
            
            # Check if bandwidth is available for this cell
            if bandwidth_col in row and not pd.isna(row[bandwidth_col]):
                bandwidth = row[bandwidth_col]
            else:
                # If no bandwidth, use a default value (e.g., 1 octave = typical tuning width)
                bandwidth = 1.0
            
            # Create Gaussian-like tuning curve centered at BF (octave 0)
            # Width determined by bandwidth
            sigma = bandwidth / 2.355  # Convert FWHM to sigma (for Gaussian)
            tuning_curve = mean_rate + (peak_rate - mean_rate) * np.exp(-(octave_range**2) / (2 * sigma**2))
            
            all_tuning_curves.append(tuning_curve)
        
        # Calculate population statistics
        all_tuning_curves = np.array(all_tuning_curves)
        mean_rates = np.mean(all_tuning_curves, axis=0)
        sem_rates = np.std(all_tuning_curves, axis=0) / np.sqrt(len(all_tuning_curves))
        n_cells = len(all_tuning_curves)
        
        return octave_range, mean_rates, sem_rates, n_cells
    
    def create_population_tuning_curves_normalized(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 4-panel figure showing NORMALIZED population-average tuning curves.
        
        Normalization: Each cell's OFF peak = 1.0, same normalization applied to ON.
        This shows relative changes in tuning shape and amplitude.
        
        Panel layout:
        - Top left: Experimental Laser OFF
        - Bottom left: Experimental Laser ON
        - Top right: Control Laser OFF
        - Bottom right: Control Laser ON
        """
        print("\n" + "="*70)
        print("GENERATING NORMALIZED POPULATION TUNING CURVES")
        print("="*70)
        
        # Create figure with 2x2 subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Define conditions with updated colors
        conditions = [
            (exp_df, 'off', 'Experimental Laser OFF', axes[0, 0], self.color_off),
            (exp_df, 'on', 'Experimental Laser ON', axes[1, 0], self.color_on),
            (ctrl_df, 'off', 'Control Laser OFF', axes[0, 1], self.color_off),
            (ctrl_df, 'on', 'Control Laser ON', axes[1, 1], self.color_on)
        ]
        
        for df, condition, title, ax, color in conditions:
            print(f"\n  Processing {title}...")
            
            # Calculate NORMALIZED population tuning curve
            octaves, mean_rates, sem_rates, n_cells = self._calculate_population_tuning_normalized(
                df, condition
            )
            
            # Plot mean with SEM
            ax.plot(octaves, mean_rates, '-o', color=color, linewidth=2.5, 
                   markersize=6, label='Mean', markeredgecolor='black', markeredgewidth=0.5)
            ax.fill_between(octaves, mean_rates - sem_rates, mean_rates + sem_rates,
                           color=color, alpha=0.3, label='SEM')
            
            # Format axes
            ax.set_xlabel('Octaves from Best Frequency', fontsize=11, fontweight='bold')
            ax.set_ylabel('Normalized Firing Rate\n(OFF peak = 1.0)', fontsize=11, fontweight='bold')
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5, label='Best Freq')
            ax.axhline(1, color='gray', linestyle=':', linewidth=1, alpha=0.5, label='OFF peak')
            ax.grid(True, alpha=0.3)
            ax.legend(loc='best', fontsize=9)
            
            # Add n cells annotation
            ax.text(0.02, 0.98, f'n = {n_cells} cells', 
                   transform=ax.transAxes, ha='left', va='top',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                            edgecolor='black', linewidth=1.5, alpha=0.9))
        
        # Overall title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        fig.suptitle(f'Normalized Population-Average Tuning Curves\nExperimental vs Control ({tuning_label})',
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_curves_normalized.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Normalized population tuning curves saved: {output_path}")
    
    def create_population_tuning_comparison_normalized(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 2-panel figure comparing NORMALIZED laser OFF vs ON conditions.
        
        Normalization: Each cell's OFF peak = 1.0, same normalization applied to ON.
        This allows direct comparison of relative amplitude changes.
        
        Panel layout:
        - Left: Experimental (Laser OFF and ON overlaid)
        - Right: Control (Laser OFF and ON overlaid)
        """
        print("\n" + "="*70)
        print("GENERATING NORMALIZED POPULATION TUNING COMPARISON (ON/OFF OVERLAID)")
        print("="*70)
        
        # Create figure with 1x2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Panel 1: Experimental (OFF and ON)
        print("\n  Processing Experimental...")
        ax = axes[0]
        
        # Calculate NORMALIZED tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning_normalized(exp_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning_normalized(exp_df, 'on')
        
        # Plot OFF condition (cyan)
        ax.plot(octaves_off, mean_off, '-o', color=self.color_off, linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})', 
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color=self.color_off, alpha=0.3)
        
        # Plot ON condition (magenta)
        ax.plot(octaves_on, mean_on, '-o', color=self.color_on, linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color=self.color_on, alpha=0.3)
        
        # Format Experimental panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Normalized Firing Rate\n(OFF peak = 1.0)', fontsize=12, fontweight='bold')
        ax.set_title('Experimental Group\n(ArchT)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.axhline(1, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Panel 2: Control (OFF and ON)
        print("\n  Processing Control...")
        ax = axes[1]
        
        # Calculate NORMALIZED tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning_normalized(ctrl_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning_normalized(ctrl_df, 'on')
        
        # Plot OFF condition (cyan)
        ax.plot(octaves_off, mean_off, '-o', color=self.color_off, linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color=self.color_off, alpha=0.3)
        
        # Plot ON condition (magenta)
        ax.plot(octaves_on, mean_on, '-o', color=self.color_on, linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color=self.color_on, alpha=0.3)
        
        # Format Control panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Normalized Firing Rate\n(OFF peak = 1.0)', fontsize=12, fontweight='bold')
        ax.set_title('Control Group\n(Laser blocked)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.axhline(1, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Overall title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        fig.suptitle(f'Normalized Population Tuning Curves: Laser OFF vs ON Comparison ({tuning_label})',
                    fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_comparison_normalized.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Normalized population tuning comparison saved: {output_path}")
    
    @staticmethod
    def _calculate_population_tuning_normalized(
        df: pd.DataFrame,
        condition: str
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int]:
        """
        Calculate NORMALIZED population-average tuning curve.
        
        Normalization: Each cell's OFF peak = 1.0, same factor applied to ON.
        This removes absolute firing rate differences and focuses on relative changes.
        
        Args:
            df: DataFrame with tuning data
            condition: 'off' or 'on'
        
        Returns:
            octaves: Array of octave distances from BF
            mean_rates: Mean NORMALIZED firing rate at each octave distance
            sem_rates: SEM of NORMALIZED firing rate
            n_cells: Number of cells included
        """
        # Get column names
        best_freq_col = f'best_freq_{condition}'
        peak_rate_col = f'peak_rate_{condition}'
        mean_rate_col = f'mean_rate_{condition}'
        bandwidth_col = f'bandwidth_octaves_{condition}'
        
        # For normalization, we need BOTH off and on data for each cell
        # This ensures we normalize by the SAME factor (OFF peak) for both conditions
        required_cols_off = ['best_freq_off', 'peak_rate_off', 'mean_rate_off']
        required_cols_on = ['best_freq_on', 'peak_rate_on', 'mean_rate_on']
        
        # Filter to cells with valid data in both conditions
        all_required = []
        for col in required_cols_off + required_cols_on:
            if col in df.columns:
                all_required.append(col)
        
        valid_data = df[all_required].dropna()
        
        if len(valid_data) == 0:
            return np.array([]), np.array([]), np.array([]), 0
        
        # Define octave range
        octave_range = np.linspace(-3, 3, 13)
        
        # For each cell, create normalized tuning curve
        all_tuning_curves_normalized = []
        
        for _, row in valid_data.iterrows():
            # Get OFF peak rate (this is our normalization factor)
            off_peak = row['peak_rate_off']
            
            # Skip cells with very low OFF peak (would cause division issues)
            if off_peak < 0.1:
                continue
            
            # Get current condition's data
            peak_rate = row[peak_rate_col]
            mean_rate = row[mean_rate_col]
            
            # Get baseline if available
            baseline_col = f'baseline_rate_prestim_{condition}'
            if baseline_col in row and not pd.isna(row[baseline_col]):
                baseline = row[baseline_col]
            else:
                baseline = mean_rate
            
            # Get bandwidth if available
            if bandwidth_col in row and not pd.isna(row[bandwidth_col]):
                bandwidth = row[bandwidth_col]
            else:
                bandwidth = 1.0
            
            # Create tuning curve (in absolute firing rates)
            sigma = bandwidth / 2.355
            tuning_curve = baseline + (peak_rate - baseline) * np.exp(-(octave_range**2) / (2 * sigma**2))
            
            # NORMALIZE by OFF peak rate (cell-specific normalization)
            tuning_curve_normalized = tuning_curve / off_peak
            
            all_tuning_curves_normalized.append(tuning_curve_normalized)
        
        # Calculate population statistics
        all_tuning_curves_normalized = np.array(all_tuning_curves_normalized)
        mean_rates = np.mean(all_tuning_curves_normalized, axis=0)
        sem_rates = np.std(all_tuning_curves_normalized, axis=0) / np.sqrt(len(all_tuning_curves_normalized))
        n_cells = len(all_tuning_curves_normalized)
        
        return octave_range, mean_rates, sem_rates, n_cells
    
    def create_scatter_plots(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create scatter plots showing individual cell changes (OFF vs ON) for each metric.
        
        One figure per metric with 2 panels:
        - Left: Experimental cells
        - Right: Control cells
        """
        print("\n" + "="*70)
        print("GENERATING SCATTER PLOTS (Individual Cell Changes)")
        print("="*70)
        
        for metric_name, metric_label in metrics_to_plot.items():
            print(f"\n  Creating scatter plot for {metric_label}...")
            
            # Create figure with 1x2 subplots
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            
            # Panel 1: Experimental
            ax = axes[0]
            exp_off_col = f'{metric_name}_off'
            exp_on_col = f'{metric_name}_on'
            exp_valid = exp_df[[exp_off_col, exp_on_col]].dropna()
            
            if len(exp_valid) > 0:
                exp_off = exp_valid[exp_off_col].values
                exp_on = exp_valid[exp_on_col].values
                
                # Scatter plot (cyan color for consistency with experimental group)
                ax.scatter(exp_off, exp_on, alpha=0.6, s=50, 
                          color=self.color_off, edgecolors='black', linewidth=0.5)
                
                # Unity line (no change)
                min_val = min(exp_off.min(), exp_on.min())
                max_val = max(exp_off.max(), exp_on.max())
                ax.plot([min_val, max_val], [min_val, max_val], 
                       'k--', linewidth=2, alpha=0.5, label='No change')
                
                # Format
                ax.set_xlabel(f'{metric_label} (Laser OFF)', fontsize=11, fontweight='bold')
                ax.set_ylabel(f'{metric_label} (Laser ON)', fontsize=11, fontweight='bold')
                ax.set_title(f'Experimental (n={len(exp_valid)})', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend(loc='best', fontsize=9)
                ax.set_aspect('equal', adjustable='box')
            
            # Panel 2: Control
            ax = axes[1]
            ctrl_off_col = f'{metric_name}_off'
            ctrl_on_col = f'{metric_name}_on'
            ctrl_valid = ctrl_df[[ctrl_off_col, ctrl_on_col]].dropna()
            
            if len(ctrl_valid) > 0:
                ctrl_off = ctrl_valid[ctrl_off_col].values
                ctrl_on = ctrl_valid[ctrl_on_col].values
                
                # Scatter plot (use orange/different color for control to distinguish from experimental)
                ax.scatter(ctrl_off, ctrl_on, alpha=0.6, s=50,
                          color='#CC79A7', edgecolors='black', linewidth=0.5)
                
                # Unity line (no change)
                min_val = min(ctrl_off.min(), ctrl_on.min())
                max_val = max(ctrl_off.max(), ctrl_on.max())
                ax.plot([min_val, max_val], [min_val, max_val],
                       'k--', linewidth=2, alpha=0.5, label='No change')
                
                # Format
                ax.set_xlabel(f'{metric_label} (Laser OFF)', fontsize=11, fontweight='bold')
                ax.set_ylabel(f'{metric_label} (Laser ON)', fontsize=11, fontweight='bold')
                ax.set_title(f'Control (n={len(ctrl_valid)})', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend(loc='best', fontsize=9)
                ax.set_aspect('equal', adjustable='box')
            
            # Overall title
            tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
            fig.suptitle(f'{metric_label}: Individual Cell Changes\n({tuning_label})',
                        fontsize=13, fontweight='bold')
            
            plt.tight_layout()
            
            # Save
            output_path = os.path.join(output_dir, f'{metric_name}_scatter.png')
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            print(f"    Saved: {output_path}")
    
    def create_delta_distribution_plots(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create distribution plots showing the change (delta = ON - OFF) for each metric.
        
        One figure per metric comparing Experimental vs Control distributions.
        """
        print("\n" + "="*70)
        print("GENERATING DELTA DISTRIBUTION PLOTS")
        print("="*70)
        
        for metric_name, metric_label in metrics_to_plot.items():
            print(f"\n  Creating delta distribution for {metric_label}...")
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Calculate deltas
            exp_off_col = f'{metric_name}_off'
            exp_on_col = f'{metric_name}_on'
            exp_valid = exp_df[[exp_off_col, exp_on_col]].dropna()
            exp_delta = (exp_valid[exp_on_col] - exp_valid[exp_off_col]).values
            
            ctrl_off_col = f'{metric_name}_off'
            ctrl_on_col = f'{metric_name}_on'
            ctrl_valid = ctrl_df[[ctrl_off_col, ctrl_on_col]].dropna()
            ctrl_delta = (ctrl_valid[ctrl_on_col] - ctrl_valid[ctrl_off_col]).values
            
            # Create violin plots
            positions = [1, 2]
            parts = ax.violinplot([exp_delta, ctrl_delta], positions=positions,
                                 showmeans=True, showmedians=True, widths=0.7)
            
            # Color the violins (use cyan for experimental, orange for control)
            colors = [self.color_off, '#CC79A7']  # Exp=cyan, Ctrl=orange for group distinction
            for i, pc in enumerate(parts['bodies']):
                pc.set_facecolor(colors[i])
                pc.set_alpha(0.7)
                pc.set_edgecolor('black')
                pc.set_linewidth(1.5)
            
            # Overlay individual points with jitter
            np.random.seed(42)
            jitter_strength = 0.04
            
            # Experimental points (cyan)
            jitter_exp = np.random.normal(0, jitter_strength, len(exp_delta))
            ax.scatter(1 + jitter_exp, exp_delta, alpha=0.4, s=20,
                      color=self.color_off, edgecolors='black', linewidth=0.3)
            
            # Control points (orange)
            jitter_ctrl = np.random.normal(0, jitter_strength, len(ctrl_delta))
            ax.scatter(2 + jitter_ctrl, ctrl_delta, alpha=0.4, s=20,
                      color='#CC79A7', edgecolors='black', linewidth=0.3)
            
            # Add zero line (no change)
            ax.axhline(0, color='black', linestyle='--', linewidth=2, alpha=0.5)
            
            # Statistical test: Mann-Whitney U test (independent samples)
            # Tests if the distributions of changes differ between groups
            if len(exp_delta) >= 3 and len(ctrl_delta) >= 3:
                u_stat, p_value = stats.mannwhitneyu(exp_delta, ctrl_delta, alternative='two-sided')
                sig_label = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
                
                # Add bracket between groups to show comparison
                y_top = ax.get_ylim()[1] * 0.88
                ax.plot([1, 2], [y_top, y_top], 'k-', linewidth=1.5)
                ax.text(1.5, y_top + (ax.get_ylim()[1] * 0.02), sig_label,
                       ha='center', va='bottom', fontsize=12, fontweight='bold')
                ax.text(1.5, y_top - (ax.get_ylim()[1] * 0.03), f'p={p_value:.2e}',
                       ha='center', va='top', fontsize=9)
            
            # Add mean values as text
            exp_mean = np.mean(exp_delta)
            ctrl_mean = np.mean(ctrl_delta)
            ax.text(1, ax.get_ylim()[1] * 0.72, f'Mean: {exp_mean:.3f}',
                   ha='center', fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                            edgecolor='black', alpha=0.8))
            ax.text(2, ax.get_ylim()[1] * 0.72, f'Mean: {ctrl_mean:.3f}',
                   ha='center', fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                            edgecolor='black', alpha=0.8))
            
            # Format axes
            ax.set_xticks([1, 2])
            ax.set_xticklabels([f'Experimental\n(n={len(exp_delta)})', 
                               f'Control\n(n={len(ctrl_delta)})'],
                              fontsize=11, fontweight='bold')
            ax.set_ylabel(f'Change in {metric_label}\n(Laser ON - Laser OFF)',
                         fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Title
            tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
            ax.set_title(f'{metric_label}: Distribution of Changes\n({tuning_label})',
                        fontsize=13, fontweight='bold', pad=15)
            
            plt.tight_layout()
            
            # Save
            output_path = os.path.join(output_dir, f'{metric_name}_delta_distribution.png')
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            print(f"    Saved: {output_path}")
    
    def create_pdf_report(
        self,
        exp_df: pd.DataFrame,
        ctrl_df: pd.DataFrame,
        all_stats: Dict[str, Dict],
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create comprehensive PDF report with all figures.
        
        PDF Structure:
        - Page 1-N: For each metric, show 3 plots:
          1. Bar chart comparison (top)
          2. Scatter plot (middle)
          3. Delta distribution (bottom)
        - Final pages: Population tuning curves (4-panel and 2-panel)
        """
        print("\n" + "="*70)
        print("GENERATING COMPREHENSIVE PDF REPORT")
        print("="*70)
        
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        pdf_filename = f'AC_vs_control_comparison_report_{self.config.tuning_type}.pdf'
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        with PdfPages(pdf_path) as pdf:
            # For each metric, create a page with 3 subplots
            for metric_name, metric_label in metrics_to_plot.items():
                print(f"\n  Adding {metric_label} to PDF...")
                
                # Create figure with 3 rows
                fig = plt.figure(figsize=(11, 14))
                
                # Row 1: Bar chart comparison
                ax1 = plt.subplot(3, 1, 1)
                self._plot_bar_comparison_for_pdf(ax1, all_stats[metric_name], metric_label)
                
                # Row 2: Scatter plots (2 panels side by side)
                ax2_left = plt.subplot(3, 2, 3)
                ax2_right = plt.subplot(3, 2, 4)
                self._plot_scatter_for_pdf(ax2_left, ax2_right, exp_df, ctrl_df, metric_name, metric_label)
                
                # Row 3: Delta distribution
                ax3 = plt.subplot(3, 1, 3)
                self._plot_delta_distribution_for_pdf(ax3, exp_df, ctrl_df, metric_name, metric_label)
                
                # Overall title for the page
                fig.suptitle(f'{metric_label} - Experimental vs Control Comparison\n({tuning_label})',
                           fontsize=16, fontweight='bold', y=0.995)
                
                plt.tight_layout(rect=[0, 0, 1, 0.985])
                pdf.savefig(fig, dpi=150)
                plt.close(fig)
            
            # Add population tuning curves (4-panel)
            print("\n  Adding 4-panel population tuning curves to PDF...")
            fig = self._create_population_tuning_figure(exp_df, ctrl_df, '4-panel')
            pdf.savefig(fig, dpi=150)
            plt.close(fig)
            
            # Add population tuning comparison (2-panel overlaid)
            print("\n  Adding 2-panel population tuning comparison to PDF...")
            fig = self._create_population_tuning_comparison_figure(exp_df, ctrl_df)
            pdf.savefig(fig, dpi=150)
            plt.close(fig)
            
            # Add NORMALIZED population tuning curves (4-panel) - NEW!
            print("\n  Adding 4-panel NORMALIZED population tuning curves to PDF...")
            img_path = os.path.join(output_dir, 'population_tuning_curves_normalized.png')
            if os.path.exists(img_path):
                img = plt.imread(img_path)
                fig = plt.figure(figsize=(14, 10))
                plt.imshow(img)
                plt.axis('off')
                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
            
            # Add NORMALIZED population tuning comparison (2-panel) - NEW!
            print("\n  Adding 2-panel NORMALIZED population tuning comparison to PDF...")
            img_path = os.path.join(output_dir, 'population_tuning_comparison_normalized.png')
            if os.path.exists(img_path):
                img = plt.imread(img_path)
                fig = plt.figure(figsize=(14, 6))
                plt.imshow(img)
                plt.axis('off')
                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
            
            # Set PDF metadata
            d = pdf.infodict()
            d['Title'] = f'AC-pStr vs Control Group Comparison ({tuning_label})'
            d['Author'] = 'Hylen'
            d['Subject'] = 'AC-pStr optogenetic inhibition vs control comparison analysis'
            d['Keywords'] = f'{tuning_label}, AC-pStr, Control, Optogenetics, ArchT'
        
        print(f"\n  PDF report saved: {pdf_path}")
    
    def _plot_bar_comparison_for_pdf(self, ax, stats, metric_label):
        """Plot bar comparison for PDF (simplified version)."""
        exp_stats = stats['Experimental']
        ctrl_stats = stats['Control']
        
        x_positions = [1, 2, 4, 5]
        means = [exp_stats['mean_off'], exp_stats['mean_on'],
                ctrl_stats['mean_off'], ctrl_stats['mean_on']]
        sems = [exp_stats['sem_off'], exp_stats['sem_on'],
               ctrl_stats['sem_off'], ctrl_stats['sem_on']]
        # Updated colors: cyan for OFF, magenta for ON
        colors = [self.color_off, self.color_on, self.color_off, self.color_on]
        
        bars = ax.bar(x_positions, means, yerr=sems, capsize=6,
                     color=colors, edgecolor='black', linewidth=1.2,
                     alpha=0.8, width=0.7)
        
        # Add value labels
        for bar, mean in zip(bars, means):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{mean:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # Add significance
        y_max = max(means) + max(sems)
        self._add_significance_bracket(ax, 1, 2, means[0:2], sems[0:2], exp_stats)
        self._add_significance_bracket(ax, 4, 5, means[2:4], sems[2:4], ctrl_stats)
        
        ax.set_ylabel(metric_label, fontsize=11, fontweight='bold')
        ax.set_xticks([1.5, 4.5])
        ax.set_xticklabels([f'Experimental\n(n={exp_stats["n"]})', f'Control\n(n={ctrl_stats["n"]})'],
                          fontsize=10, fontweight='bold')
        ax.set_xlim([0, 6])
        ax.set_ylim([0, y_max + 0.25])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add legend
        self._add_legend(ax)
        
        ax.set_title('Bar Chart: Laser OFF vs ON', fontsize=11, fontweight='bold', pad=10)
    
    def _plot_scatter_for_pdf(self, ax_left, ax_right, exp_df, ctrl_df, metric_name, metric_label):
        """Plot scatter plots for PDF."""
        # Experimental (cyan)
        exp_off_col = f'{metric_name}_off'
        exp_on_col = f'{metric_name}_on'
        exp_valid = exp_df[[exp_off_col, exp_on_col]].dropna()
        
        if len(exp_valid) > 0:
            exp_off = exp_valid[exp_off_col].values
            exp_on = exp_valid[exp_on_col].values
            
            ax_left.scatter(exp_off, exp_on, alpha=0.6, s=40,
                          color=self.color_off, edgecolors='black', linewidth=0.5)
            min_val = min(exp_off.min(), exp_on.min())
            max_val = max(exp_off.max(), exp_on.max())
            ax_left.plot([min_val, max_val], [min_val, max_val],
                        'k--', linewidth=1.5, alpha=0.5)
            
            ax_left.set_xlabel(f'{metric_label} (OFF)', fontsize=9, fontweight='bold')
            ax_left.set_ylabel(f'{metric_label} (ON)', fontsize=9, fontweight='bold')
            ax_left.set_title(f'Experimental (n={len(exp_valid)})', fontsize=10, fontweight='bold')
            ax_left.grid(True, alpha=0.3)
            ax_left.set_aspect('equal', adjustable='box')
        
        # Control (orange for group distinction)
        ctrl_off_col = f'{metric_name}_off'
        ctrl_on_col = f'{metric_name}_on'
        ctrl_valid = ctrl_df[[ctrl_off_col, ctrl_on_col]].dropna()
        
        if len(ctrl_valid) > 0:
            ctrl_off = ctrl_valid[ctrl_off_col].values
            ctrl_on = ctrl_valid[ctrl_on_col].values
            
            ax_right.scatter(ctrl_off, ctrl_on, alpha=0.6, s=40,
                           color='#CC79A7', edgecolors='black', linewidth=0.5)
            min_val = min(ctrl_off.min(), ctrl_on.min())
            max_val = max(ctrl_off.max(), ctrl_on.max())
            ax_right.plot([min_val, max_val], [min_val, max_val],
                         'k--', linewidth=1.5, alpha=0.5)
            
            ax_right.set_xlabel(f'{metric_label} (OFF)', fontsize=9, fontweight='bold')
            ax_right.set_ylabel(f'{metric_label} (ON)', fontsize=9, fontweight='bold')
            ax_right.set_title(f'Control (n={len(ctrl_valid)})', fontsize=10, fontweight='bold')
            ax_right.grid(True, alpha=0.3)
            ax_right.set_aspect('equal', adjustable='box')
    
    def _plot_delta_distribution_for_pdf(self, ax, exp_df, ctrl_df, metric_name, metric_label):
        """Plot delta distribution for PDF."""
        # Calculate deltas
        exp_off_col = f'{metric_name}_off'
        exp_on_col = f'{metric_name}_on'
        exp_valid = exp_df[[exp_off_col, exp_on_col]].dropna()
        exp_delta = (exp_valid[exp_on_col] - exp_valid[exp_off_col]).values
        
        ctrl_off_col = f'{metric_name}_off'
        ctrl_on_col = f'{metric_name}_on'
        ctrl_valid = ctrl_df[[ctrl_off_col, ctrl_on_col]].dropna()
        ctrl_delta = (ctrl_valid[ctrl_on_col] - ctrl_valid[ctrl_off_col]).values
        
        # Violin plots
        positions = [1, 2]
        parts = ax.violinplot([exp_delta, ctrl_delta], positions=positions,
                             showmeans=True, showmedians=True, widths=0.7)
        
        colors = [self.color_off, '#CC79A7']  # Exp=cyan, Ctrl=orange
        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(colors[i])
            pc.set_alpha(0.7)
            pc.set_edgecolor('black')
            pc.set_linewidth(1.2)
        
        # Scatter points (cyan for exp, orange for control)
        np.random.seed(42)
        jitter_exp = np.random.normal(0, 0.04, len(exp_delta))
        ax.scatter(1 + jitter_exp, exp_delta, alpha=0.3, s=15,
                  color=self.color_off, edgecolors='black', linewidth=0.2)
        
        jitter_ctrl = np.random.normal(0, 0.04, len(ctrl_delta))
        ax.scatter(2 + jitter_ctrl, ctrl_delta, alpha=0.3, s=15,
                  color='#CC79A7', edgecolors='black', linewidth=0.2)
        
        # Add zero line (no change)
        ax.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.5)
        
        # Statistical test
        if len(exp_delta) >= 3 and len(ctrl_delta) >= 3:
            u_stat, p_value = stats.mannwhitneyu(exp_delta, ctrl_delta, alternative='two-sided')
            sig_label = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
            
            y_top = ax.get_ylim()[1] * 0.88
            ax.plot([1, 2], [y_top, y_top], 'k-', linewidth=1.2)
            ax.text(1.5, y_top + (ax.get_ylim()[1] * 0.02), sig_label,
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
            ax.text(1.5, y_top - (ax.get_ylim()[1] * 0.03), f'p={p_value:.2e}',
                   ha='center', va='top', fontsize=8)
        
        # Mean values
        exp_mean = np.mean(exp_delta)
        ctrl_mean = np.mean(ctrl_delta)
        ax.text(1, ax.get_ylim()[1] * 0.72, f'Mean: {exp_mean:.3f}',
               ha='center', fontsize=8, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        edgecolor='black', alpha=0.8))
        ax.text(2, ax.get_ylim()[1] * 0.72, f'Mean: {ctrl_mean:.3f}',
               ha='center', fontsize=8, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        edgecolor='black', alpha=0.8))
        
        ax.set_xticks([1, 2])
        ax.set_xticklabels([f'Experimental\n(n={len(exp_delta)})', f'Control\n(n={len(ctrl_delta)})'],
                          fontsize=10, fontweight='bold')
        ax.set_ylabel(f'Change in {metric_label}\n(Laser ON - Laser OFF)', fontsize=9, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_title('Delta Distribution', fontsize=11, fontweight='bold', pad=10)
    
    def _create_population_tuning_figure(self, exp_df, ctrl_df, title_suffix):
        """Create 4-panel population tuning curves figure for PDF."""
        fig, axes = plt.subplots(2, 2, figsize=(11, 10))
        
        conditions = [
            (exp_df, 'off', 'Experimental Laser OFF', axes[0, 0], self.color_off),
            (exp_df, 'on', 'Experimental Laser ON', axes[1, 0], self.color_on),
            (ctrl_df, 'off', 'Control Laser OFF', axes[0, 1], self.color_off),
            (ctrl_df, 'on', 'Control Laser ON', axes[1, 1], self.color_on)
        ]
        
        for df, condition, title, ax, color in conditions:
            octaves, mean_rates, sem_rates, n_cells = self._calculate_population_tuning(df, condition)
            
            if len(octaves) > 0:
                ax.plot(octaves, mean_rates, '-o', color=color, linewidth=2,
                       markersize=5, label='Mean', markeredgecolor='black', markeredgewidth=0.5)
                ax.fill_between(octaves, mean_rates - sem_rates, mean_rates + sem_rates,
                               color=color, alpha=0.3)
                
                ax.set_xlabel('Octaves from Best Frequency', fontsize=10, fontweight='bold')
                ax.set_ylabel('Firing Rate (Hz)', fontsize=10, fontweight='bold')
                ax.set_title(f'{title}\n(n={n_cells})', fontsize=11, fontweight='bold')
                ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
                ax.grid(True, alpha=0.3)
        
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        fig.suptitle(f'Population-Average Tuning Curves ({tuning_label})',
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        return fig
    
    def _create_population_tuning_comparison_figure(self, exp_df, ctrl_df):
        """Create 2-panel population tuning comparison figure for PDF."""
        fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
        
        # Experimental (cyan OFF, magenta ON)
        ax = axes[0]
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(exp_df, 'off')
       
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(exp_df, 'on')
        
        ax.plot(octaves_off, mean_off, '-o', color=self.color_off, linewidth=2,
               markersize=5, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color=self.color_off, alpha=0.3)
        
        ax.plot(octaves_on, mean_on, '-o', color=self.color_on, linewidth=2,
               markersize=5, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color=self.color_on, alpha=0.3)
        
        # Format Experimental panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=11, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=11, fontweight='bold')
        ax.set_title('Experimental Group', fontsize=12, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)
        
        # Control (cyan OFF, magenta ON)
        ax = axes[1]
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(ctrl_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(ctrl_df, 'on')
        
        ax.plot(octaves_off, mean_off, '-o', color=self.color_off, linewidth=2,
               markersize=5, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color=self.color_off, alpha=0.3)
        
        ax.plot(octaves_on, mean_on, '-o', color=self.color_on, linewidth=2,
               markersize=5, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color=self.color_on, alpha=0.3)
        
        # Format Control panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=11, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=11, fontweight='bold')
        ax.set_title('Control Group', fontsize=12, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)
        
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        fig.suptitle(f'Population Tuning Comparison: OFF vs ON ({tuning_label})',
                    fontsize=13, fontweight='bold')
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        return fig
    
    @staticmethod
    def _add_significance_bracket(ax, x1, x2, means, sems, stats):
        """Add significance bracket and p-value annotation."""
        sig_label = '***' if stats['p_value'] < 0.001 else \
                   '**' if stats['p_value'] < 0.01 else \
                   '*' if stats['p_value'] < 0.05 else 'ns'
        
        y_max = max(means[0] + sems[0], means[1] + sems[1])
        bracket_height = y_max + 0.05
        
        # Draw the bracket
        ax.plot([x1, x2], [bracket_height, bracket_height], '-', linewidth=1.5)
        
        # Add significance stars below the bracket
        ax.text((x1 + x2) / 2, bracket_height - 0.01, sig_label, 
               ha='center', va='top', fontsize=12, fontweight='bold')
        
        # Add p-value above the bracket
        ax.text((x1 + x2) / 2, bracket_height + 0.01, f'p={stats["p_value"]:.2e}', 
               ha='center', va='bottom', fontsize=9)
    
    @staticmethod
    def _add_legend(ax):
        """Add legend for laser conditions with updated colors."""
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#56B4E9', edgecolor='black', label='Laser OFF', alpha=0.8),
            Patch(facecolor='#9E4784', edgecolor='black', label='Laser ON', alpha=0.8)
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.9)
    
    @staticmethod
    def _add_sample_sizes_top(ax, exp_stats, ctrl_stats, y_max):
        """Add sample size annotations near the bottom, just above x-axis."""
        # Position at 10% of y-axis height (near bottom but above x-axis)
        bottom_position = y_max * 0.10
        
        # Add n annotations at bottom position, centered over each group
        ax.text(1.5, bottom_position, f'n = {exp_stats["n"]}', ha='center', va='center',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                        edgecolor='black', linewidth=1.5, alpha=0.9))
        ax.text(4.5, bottom_position, f'n = {ctrl_stats["n"]}', ha='center', va='center',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                        edgecolor='black', linewidth=1.5, alpha=0.9))


# =============================================================================
# MAIN COORDINATOR
# =============================================================================

class GroupComparisonCoordinator:
    """Coordinates the experimental vs control comparison analysis."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
        self.loader = GroupDataLoader(config)
        self.comparator = GroupComparator(config)
        self.visualizer = GroupVisualizer(config)
    
    def run(self):
        """Execute complete comparison analysis."""
        print("="*70)
        print("EXPERIMENTAL VS CONTROL GROUP COMPARISON")
        print(f"Analysis Type: {self.config.tuning_type.upper()} TUNING")
        print("="*70)
        print(f"Experimental directory: {self.config.experimental_dir}")
        print(f"Control directory:      {self.config.control_dir}")
        print(f"Output directory:       {self.config.output_dir}")
        
        # Load data
        exp_df, ctrl_df = self.loader.load_both_groups()
        
        # Test within-group laser effects for all metrics
        all_stats = self.comparator.test_all_metrics(
            exp_df, ctrl_df, self.config.metrics_to_plot
        )
        
        # Create output directory
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Generate comparison plots for all metrics
        self.visualizer.create_all_metric_plots(
            exp_df, ctrl_df, all_stats, 
            self.config.metrics_to_plot, 
            self.config.output_dir
        )
        
        # Generate population tuning curves (4-panel)
        self.visualizer.create_population_tuning_curves(
            exp_df, ctrl_df, self.config.output_dir
        )
        
        # Generate population tuning curves comparison (2-panel, ON/OFF overlaid)
        self.visualizer.create_population_tuning_comparison(
            exp_df, ctrl_df, self.config.output_dir
        )
        
        # Generate NORMALIZED population tuning curves (cell-specific normalization)
        self.visualizer.create_population_tuning_curves_normalized(
            exp_df, ctrl_df, self.config.output_dir
        )
        
        # Generate NORMALIZED population tuning comparison (2-panel, ON/OFF overlaid)
        self.visualizer.create_population_tuning_comparison_normalized(
            exp_df, ctrl_df, self.config.output_dir
        )
        
        # Generate scatter plots (individual cell changes)
        self.visualizer.create_scatter_plots(
            exp_df, ctrl_df, self.config.metrics_to_plot, self.config.output_dir
        )
        
        # Generate delta distribution plots
        self.visualizer.create_delta_distribution_plots(
            exp_df, ctrl_df, self.config.metrics_to_plot, self.config.output_dir
        )
        
        # Generate comprehensive PDF report
        self.visualizer.create_pdf_report(
            exp_df, ctrl_df, all_stats, self.config.metrics_to_plot, self.config.output_dir
        )
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Experimental cells: {len(exp_df)}")
        print(f"Control cells: {len(ctrl_df)}")
        print(f"Metrics analyzed: {len(self.config.metrics_to_plot)}")
        
        # Count significant effects
        n_sig_exp = sum(1 for stats in all_stats.values() if stats['Experimental']['significant'])
        n_sig_ctrl = sum(1 for stats in all_stats.values() if stats['Control']['significant'])
        
        print(f"\nSignificant laser effects (p < {self.config.alpha}):")
        print(f"  Experimental: {n_sig_exp}/{len(all_stats)} metrics")
        print(f"  Control: {n_sig_ctrl}/{len(all_stats)} metrics")
        print(f"\nResults saved to: {self.config.output_dir}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main execution - runs analysis for both frequency and AM tuning."""
    
    # Run frequency tuning analysis
    print("\n" + "="*70)
    print("RUNNING FREQUENCY TUNING ANALYSIS")
    print("="*70 + "\n")
    
    freq_config = ComparisonConfig(tuning_type='frequency')
    freq_coordinator = GroupComparisonCoordinator(freq_config)
    
    try:
        freq_coordinator.run()
        print("\n" + "="*70)
        print("FREQUENCY TUNING ANALYSIS COMPLETED")
        print("="*70)
    except Exception as e:
        print(f"\nERROR in Frequency Analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # Run AM tuning analysis
    print("\n\n" + "="*70)
    print("RUNNING AM TUNING ANALYSIS")
    print("="*70 + "\n")
    
    am_config = ComparisonConfig(tuning_type='am')
    am_coordinator = GroupComparisonCoordinator(am_config)
    
    try:
        am_coordinator.run()
        print("\n" + "="*70)
        print("AM TUNING ANALYSIS COMPLETED")
        print("="*70)
    except Exception as e:
        print(f"\nERROR in AM Analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print("\n\n" + "="*70)
    print("ALL ANALYSES COMPLETED")
    print("="*70)
    print(f"\nFrequency tuning results: {freq_config.output_dir}")
    print(f"AM tuning results: {am_config.output_dir}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
