"""
AC-pStr Experimental vs Control Comparison Analysis

Compares the effects of optogenetic inhibition of AC-pStr pathway in experimental
animals (ArchT expressing) vs control animals (laser blocked, no pathway inhibition).

Datasets:
- AC-pStr Experimental: arch018, arch019, arch020, arch022 (ArchT expressing, AC-pStr inhibition)
- Control: Control animals (laser blocked, no opsin expression or laser blocked)

Analysis:
1. Load pre-computed Gaussian fit parameters from both groups' CSV files
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
        """Set default paths and metrics based on tuning type."""
        # Set data directories based on tuning type
        if self.tuning_type == 'frequency':
            object.__setattr__(self, 'ac_pstr_dir', 
                str(get_reports_subdir('tuning_freq_gaussian_fits')))
            object.__setattr__(self, 'control_dir',
                str(get_reports_subdir('control_group/tuning_freq_gaussian_fits')))
            object.__setattr__(self, 'output_dir',
                str(get_reports_subdir('AC_vs_Control_gaussian_comparison_freq')))
        elif self.tuning_type == 'am':
            object.__setattr__(self, 'ac_pstr_dir',
                str(get_reports_subdir('tuning_AM_gaussian_fits')))
            object.__setattr__(self, 'control_dir',
                str(get_reports_subdir('control_group/tuning_AM_gaussian_fits')))
            object.__setattr__(self, 'output_dir',
                str(get_reports_subdir('AC_vs_Control_gaussian_comparison_AM')))
        
        # Set default metrics to plot - GAUSSIAN FIT PARAMETERS
        if self.metrics_to_plot is None:
            if self.tuning_type == 'frequency':
                object.__setattr__(self, 'metrics_to_plot', {
                    'amplitude': 'Fitted Amplitude (Hz)',
                    'best_freq_fitted_hz': 'Fitted Best Frequency (Hz)',
                    'sigma': 'Fitted Sigma (octaves)',
                })
            elif self.tuning_type == 'am':
                object.__setattr__(self, 'metrics_to_plot', {
                    'amplitude': 'Fitted Amplitude (Hz)',
                    'preferred_rate': 'Fitted Preferred Rate (Hz)',
                    'sigma': 'Fitted Sigma (log10 units)',
                })
    
    # Note: ac_pstr_dir, control_dir, and output_dir are set dynamically above
    ac_pstr_dir: str = None
    control_dir: str = None
    output_dir: str = None


# =============================================================================
# DATA LOADING
# =============================================================================

class PathwayDataLoader:
    """Loads and organizes data from experimental and control groups."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
    
    def load_both_pathways(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load metrics from both AC-pStr experimental and Control datasets.
        
        Returns:
            Tuple of (ac_pstr_df, control_df) with laser effects calculated
        """
        print("="*70)
        print("LOADING GROUP DATA")
        print("="*70)
        
        # Load AC-pStr data (arch018-022)
        print("\nLoading AC-pStr Experimental data (arch018-022)...")
        ac_df = self._load_pathway_data(
            self.config.ac_pstr_dir,
            pathway_label='AC-pStr'
        )
        
        # Load Control data
        print("\nLoading Control data (laser blocked)...")
        control_df = self._load_pathway_data(
            self.config.control_dir,
            pathway_label='Control'
        )
        
        return ac_df, control_df
    
    def _load_pathway_data(self, metrics_dir: str, pathway_label: str) -> pd.DataFrame:
        """Load and process Gaussian fit data for one pathway."""
        # Load Gaussian fit CSVs (different names for frequency vs AM)
        if self.config.tuning_type == 'frequency':
            csv_off = os.path.join(metrics_dir, 'all_sessions_laser_off_gaussian_fits.csv')
            csv_on = os.path.join(metrics_dir, 'all_sessions_laser_on_gaussian_fits.csv')
        elif self.config.tuning_type == 'am':
            csv_off = os.path.join(metrics_dir, 'all_sessions_laser_off_log_gaussian_fits.csv')
            csv_on = os.path.join(metrics_dir, 'all_sessions_laser_on_log_gaussian_fits.csv')
        
        if not os.path.exists(csv_off) or not os.path.exists(csv_on):
            raise FileNotFoundError(f"Gaussian fit CSV files not found in {metrics_dir}")
        
        df_off = pd.read_csv(csv_off)
        df_on = pd.read_csv(csv_on)
        
        print(f"  Laser OFF: {len(df_off)} cells")
        print(f"  Laser ON:  {len(df_on)} cells")
        
        # Filter to only GOOD fits (fit_quality == 'good')
        df_off_good = df_off[df_off['fit_quality'] == 'good'].copy()
        df_on_good = df_on[df_on['fit_quality'] == 'good'].copy()
        
        print(f"  Good fits OFF: {len(df_off_good)}/{len(df_off)} cells")
        print(f"  Good fits ON:  {len(df_on_good)}/{len(df_on)} cells")
        
        # Merge on session_id and cell_idx
        df_merged = pd.merge(df_off_good, df_on_good, on=['session_id', 'cell_idx'],
                            how='inner', suffixes=('_off', '_on'))  # Use 'inner' to keep only cells with good fits in BOTH
        
        print(f"  After merge (good fits in both conditions): {len(df_merged)} cells")
        
        # Add unique cell identifier
        df_merged['cell_id'] = (
            df_merged['subject_off'] + '_' + 
            df_merged['date_off'] + '_' + 
            df_merged['depth_off'].astype(str) + '_' + 
            df_merged['cell_idx'].astype(str)
        )
        
        # Calculate laser effects (deltas)
        df_merged = self._calculate_laser_effects(df_merged)
        
        # Add pathway label
        df_merged['pathway'] = pathway_label
        
        print(f"  Final cells for analysis: {len(df_merged)} cells with good fits in both OFF and ON")
        
        return df_merged
    
    @staticmethod
    def _calculate_laser_effects(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate laser effect metrics for Gaussian fit parameters."""
        # Amplitude change (fitted parameter)
        if 'amplitude_on' in df.columns and 'amplitude_off' in df.columns:
            df['delta_amplitude'] = df['amplitude_on'] - df['amplitude_off']
            df['percent_amplitude_change'] = ((df['amplitude_on'] - df['amplitude_off']) / 
                                              df['amplitude_off'] * 100)
        
        # Best frequency/rate shift (fitted parameter, in Hz)
        # Frequency data: best_freq_fitted_hz
        if 'best_freq_fitted_hz_on' in df.columns and 'best_freq_fitted_hz_off' in df.columns:
            df['delta_best_freq_hz'] = df['best_freq_fitted_hz_on'] - df['best_freq_fitted_hz_off']
            # Also calculate in octaves
            df['delta_best_freq_octaves'] = np.log2(df['best_freq_fitted_hz_on'] / df['best_freq_fitted_hz_off'])
        
        # AM data: preferred_rate
        if 'preferred_rate_on' in df.columns and 'preferred_rate_off' in df.columns:
            df['delta_preferred_rate'] = df['preferred_rate_on'] - df['preferred_rate_off']
            # Also calculate in log10 units
            df['delta_preferred_rate_log10'] = np.log10(df['preferred_rate_on']) - np.log10(df['preferred_rate_off'])
        
        # Sigma change (fitted parameter)
        if 'sigma_on' in df.columns and 'sigma_off' in df.columns:
            df['delta_sigma'] = df['sigma_on'] - df['sigma_off']
            df['percent_sigma_change'] = ((df['sigma_on'] - df['sigma_off']) / 
                                          df['sigma_off'] * 100)
        
        # Mean octave shift (fitted parameter - only for frequency tuning)
        if 'mean_octave_on' in df.columns and 'mean_octave_off' in df.columns:
            df['delta_mean_octave'] = df['mean_octave_on'] - df['mean_octave_off']
        
        # Baseline change (fixed parameter from fitting)
        if 'baseline_on' in df.columns and 'baseline_off' in df.columns:
            df['delta_baseline'] = df['baseline_on'] - df['baseline_off']
        
        return df


# =============================================================================
# STATISTICAL COMPARISON
# =============================================================================

class PathwayComparator:
    """Performs statistical comparisons between pathways."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
    
    def test_within_pathway_effects(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        metric_name: str
    ) -> Dict:
        """
        Test if laser has significant effect within each group for a given metric.
        
        Args:
            ac_df: AC-pStr experimental data
            control_df: Control data
            metric_name: Name of the metric column (e.g., 'amplitude', 'sigma')
        
        Returns:
            Dictionary with statistics for each group
        """
        results = {}
        
        # Test AC-pStr experimental group
        ac_off_col = f'{metric_name}_off'
        ac_on_col = f'{metric_name}_on'
        
        # Filter to rows where both OFF and ON are not NaN
        ac_valid = ac_df[[ac_off_col, ac_on_col]].dropna()
        ac_off = ac_valid[ac_off_col].values
        ac_on = ac_valid[ac_on_col].values
        
        # Paired test (same cells OFF vs ON)
        if len(ac_off) >= self.config.min_cells_for_stats:
            ac_stat, ac_p = stats.wilcoxon(ac_off, ac_on, alternative='two-sided')
        else:
            ac_p = np.nan
        
        ac_mean_off = np.mean(ac_off)
        ac_mean_on = np.mean(ac_on)
        ac_sem_off = np.std(ac_off) / np.sqrt(len(ac_off))
        ac_sem_on = np.std(ac_on) / np.sqrt(len(ac_on))
        
        results['AC-pStr'] = {
            'n': len(ac_off),
            'mean_off': ac_mean_off,
            'sem_off': ac_sem_off,
            'mean_on': ac_mean_on,
            'sem_on': ac_sem_on,
            'p_value': ac_p,
            'significant': ac_p < self.config.alpha if not np.isnan(ac_p) else False
        }
        
        # Test Control group
        control_off_col = f'{metric_name}_off'
        control_on_col = f'{metric_name}_on'
        
        # Filter to rows where both OFF and ON are not NaN
        control_valid = control_df[[control_off_col, control_on_col]].dropna()
        control_off = control_valid[control_off_col].values
        control_on = control_valid[control_on_col].values
        
        if len(control_off) >= self.config.min_cells_for_stats:
            control_stat, control_p = stats.wilcoxon(control_off, control_on, alternative='two-sided')
        else:
            control_p = np.nan
        
        control_mean_off = np.mean(control_off)
        control_mean_on = np.mean(control_on)
        control_sem_off = np.std(control_off) / np.sqrt(len(control_off))
        control_sem_on = np.std(control_on) / np.sqrt(len(control_on))
        
        results['Control'] = {
            'n': len(control_off),
            'mean_off': control_mean_off,
            'sem_off': control_sem_off,
            'mean_on': control_mean_on,
            'sem_on': control_sem_on,
            'p_value': control_p,
            'significant': control_p < self.config.alpha if not np.isnan(control_p) else False
        }
        
        return results
    
    def test_all_metrics(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
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
            
            results = self.test_within_pathway_effects(ac_df, control_df, metric_name)
            
            # Print AC-pStr results
            ac_stats = results['AC-pStr']
            sig_str = '***' if ac_stats['p_value'] < 0.001 else '**' if ac_stats['p_value'] < 0.01 else '*' if ac_stats['p_value'] < 0.05 else 'ns'
            print(f"  AC-pStr (n={ac_stats['n']}): OFF={ac_stats['mean_off']:.3f}, ON={ac_stats['mean_on']:.3f}, p={ac_stats['p_value']:.2e} {sig_str}")
            
            # Print Control results
            control_stats = results['Control']
            sig_str = '***' if control_stats['p_value'] < 0.001 else '**' if control_stats['p_value'] < 0.01 else '*' if control_stats['p_value'] < 0.05 else 'ns'
            print(f"  Control (n={control_stats['n']}): OFF={control_stats['mean_off']:.3f}, ON={control_stats['mean_on']:.3f}, p={control_stats['p_value']:.2e} {sig_str}")
            
            all_results[metric_name] = results
        
        return all_results


# =============================================================================
# VISUALIZATION
# =============================================================================

class PathwayVisualizer:
    """Creates comparison visualizations."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
    
    def create_basic_comparison_plot(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        within_pathway_stats: Dict,
        metric_label: str,
        output_dir: str,
        filename: str
    ):
        """
        Create a simple bar chart comparing a metric:
        Laser OFF vs ON for AC-pStr and Control groups.
        
        Args:
            ac_df: AC-pStr data
            control_df: Control data
            within_pathway_stats: Statistics for this metric
            metric_label: Label for y-axis (e.g., 'Fitted Amplitude')
            output_dir: Directory to save the plot
            filename: Output filename
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract statistics
        ac_stats = within_pathway_stats['AC-pStr']
        control_stats = within_pathway_stats['Control']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Prepare data
        x_positions = [1, 2, 4, 5]  # Group 1: AC OFF/ON, Group 2: Control OFF/ON
        means = [
            ac_stats['mean_off'],
            ac_stats['mean_on'],
            control_stats['mean_off'],
            control_stats['mean_on']
        ]
        sems = [
            ac_stats['sem_off'],
            ac_stats['sem_on'],
            control_stats['sem_off'],
            control_stats['sem_on']
        ]
        colors = ['#4472C4', '#2E4A7C', '#C55A11', '#8B3F0C']
        
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
        self._add_significance_bracket(ax, 1, 2, means[0:2], sems[0:2], ac_stats)
        self._add_significance_bracket(ax, 4, 5, means[2:4], sems[2:4], control_stats)
        
        # Format axes
        ax.set_ylabel(metric_label, fontsize=13, fontweight='bold')
        ax.set_xticks([1.5, 4.5])
        ax.set_xticklabels(['AC-pStr\n(Experimental)', 'Control\n(Laser blocked)'], 
                          fontsize=12, fontweight='bold')
        ax.set_xlim([0, 6])
        
        # Set y-limit with extra space at top for sample size annotations
        y_max = max(means) + max(sems) + 0.25
        ax.set_ylim([0, y_max])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add legend and sample sizes at fixed top position
        self._add_legend(ax)
        self._add_sample_sizes_top(ax, ac_stats, control_stats, y_max)
        
        # Title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        ax.set_title(f'{metric_label}: Laser OFF vs ON Comparison\nAC-pStr vs Control ({tuning_label} - {gaussian_type})',
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, filename)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_path
    
    def create_all_metric_plots(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        all_stats: Dict[str, Dict],
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create bar charts for all metrics.
        
        Args:
            ac_df: AC-pStr data
            control_df: Th-pStr data
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
                ac_df, control_df,
                all_stats[metric_name],
                metric_label,
                output_dir,
                filename
            )
            print(f"    Saved: {output_path}")
    
    def create_population_tuning_curves(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 4-panel figure showing population-average frequency tuning curves.
        
        Panel layout:
        - Top left: AC-pStr Laser OFF
        - Bottom left: AC-pStr Laser ON
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
        
        # Define conditions
        conditions = [
            (ac_df, 'off', 'AC-pStr Laser OFF', axes[0, 0], '#4472C4'),
            (ac_df, 'on', 'AC-pStr Laser ON', axes[1, 0], '#2E4A7C'),
            (control_df, 'off', 'Control Laser OFF', axes[0, 1], '#C55A11'),
            (control_df, 'on', 'Control Laser ON', axes[1, 1], '#8B3F0C')
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
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        fig.suptitle(f'Population-Average Tuning Curves from {gaussian_type}\nAC-pStr vs Control Groups ({tuning_label})',
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_curves.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Population tuning curves saved: {output_path}")
    
    def create_population_tuning_comparison(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 2-panel figure comparing laser OFF vs ON conditions (absolute firing rates).
        
        Panel layout:
        - Left: AC-pStr (Laser OFF and ON overlaid)
        - Right: Th-pStr (Laser OFF and ON overlaid)
        """
        print("\n" + "="*70)
        print("GENERATING POPULATION TUNING COMPARISON (ON/OFF OVERLAID)")
        print("="*70)
        
        # Create figure with 1x2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Panel 1: AC-pStr (OFF and ON)
        print("\n  Processing AC-pStr...")
        ax = axes[0]
        
        # Calculate tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(ac_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(ac_df, 'on')
        
        # Plot OFF condition
        ax.plot(octaves_off, mean_off, '-o', color='#4472C4', linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})', 
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color='#4472C4', alpha=0.3)
        
        # Plot ON condition
        ax.plot(octaves_on, mean_on, '-o', color='#2E4A7C', linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color='#2E4A7C', alpha=0.3)
        
        # Format AC-pStr panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_title('AC-pStr Pathway\n(AC→pStr inhibition)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Panel 2: Th-pStr (OFF and ON)
        print("\n  Processing Th-pStr...")
        ax = axes[1]
        
        # Calculate tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(control_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(control_df, 'on')
        
        # Plot OFF condition
        ax.plot(octaves_off, mean_off, '-o', color='#C55A11', linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color='#C55A11', alpha=0.3)
        
        # Plot ON condition
        ax.plot(octaves_on, mean_on, '-o', color='#8B3F0C', linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color='#8B3F0C', alpha=0.3)
        
        # Format Th-pStr panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=12, fontweight='bold')
        ax.set_title('Control Group\n(Laser blocked)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Overall title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        fig.suptitle(f'Population Tuning Curves from {gaussian_type}: Laser OFF vs ON Comparison ({tuning_label})',
                    fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_comparison.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Population tuning comparison saved: {output_path}")
    
    def create_population_tuning_curves_normalized(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 4-panel figure showing NORMALIZED population-average tuning curves.
        
        Normalization: Each cell's OFF peak = 1.0, same normalization applied to ON.
        This shows relative changes in tuning shape and amplitude.
        
        Panel layout:
        - Top left: AC-pStr Laser OFF
        - Bottom left: AC-pStr Laser ON
        - Top right: Control Laser OFF
        - Bottom right: Control Laser ON
        """
        print("\n" + "="*70)
        print("GENERATING NORMALIZED POPULATION TUNING CURVES")
        print("="*70)
        
        # Create figure with 2x2 subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Define conditions
        conditions = [
            (ac_df, 'off', 'AC-pStr Laser OFF', axes[0, 0], '#4472C4'),
            (ac_df, 'on', 'AC-pStr Laser ON', axes[1, 0], '#2E4A7C'),
            (control_df, 'off', 'Control Laser OFF', axes[0, 1], '#C55A11'),
            (control_df, 'on', 'Control Laser ON', axes[1, 1], '#8B3F0C')
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
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        fig.suptitle(f'Normalized Population-Average Tuning Curves from {gaussian_type}\nAC-pStr vs Control Groups ({tuning_label})',
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_curves_normalized.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Normalized population tuning curves saved: {output_path}")
    
    def create_population_tuning_comparison_normalized(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        output_dir: str
    ):
        """
        Create 2-panel figure comparing NORMALIZED laser OFF vs ON conditions.
        
        Normalization: Each cell's OFF peak = 1.0, same normalization applied to ON.
        This allows direct comparison of relative amplitude changes.
        
        Panel layout:
        - Left: AC-pStr (Laser OFF and ON overlaid)
        - Right: Th-pStr (Laser OFF and ON overlaid)
        """
        print("\n" + "="*70)
        print("GENERATING NORMALIZED POPULATION TUNING COMPARISON (ON/OFF OVERLAID)")
        print("="*70)
        
        # Create figure with 1x2 subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Panel 1: AC-pStr (OFF and ON)
        print("\n  Processing AC-pStr...")
        ax = axes[0]
        
        # Calculate NORMALIZED tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning_normalized(ac_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning_normalized(ac_df, 'on')
        
        # Plot OFF condition
        ax.plot(octaves_off, mean_off, '-o', color='#4472C4', linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})', 
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color='#4472C4', alpha=0.3)
        
        # Plot ON condition
        ax.plot(octaves_on, mean_on, '-o', color='#2E4A7C', linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color='#2E4A7C', alpha=0.3)
        
        # Format AC-pStr panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Normalized Firing Rate\n(OFF peak = 1.0)', fontsize=12, fontweight='bold')
        ax.set_title('AC-pStr Pathway\n(AC→pStr inhibition)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.axhline(1, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Panel 2: Th-pStr (OFF and ON)
        print("\n  Processing Th-pStr...")
        ax = axes[1]
        
        # Calculate NORMALIZED tuning curves for both conditions
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning_normalized(control_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning_normalized(control_df, 'on')
        
        # Plot OFF condition
        ax.plot(octaves_off, mean_off, '-o', color='#C55A11', linewidth=2.5,
               markersize=6, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color='#C55A11', alpha=0.3)
        
        # Plot ON condition
        ax.plot(octaves_on, mean_on, '-o', color='#8B3F0C', linewidth=2.5,
               markersize=6, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color='#8B3F0C', alpha=0.3)
        
        # Format Th-pStr panel
        ax.set_xlabel('Octaves from Best Frequency', fontsize=12, fontweight='bold')
        ax.set_ylabel('Normalized Firing Rate\n(OFF peak = 1.0)', fontsize=12, fontweight='bold')
        ax.set_title('Control Group\n(Laser blocked)', fontsize=13, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.axhline(1, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
        
        # Overall title
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        fig.suptitle(f'Normalized Population Tuning Curves from {gaussian_type}: Laser OFF vs ON Comparison ({tuning_label})',
                    fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        # Save
        output_path = os.path.join(output_dir, 'population_tuning_comparison_normalized.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\n  Normalized population tuning comparison saved: {output_path}")
    
    def create_scatter_plots(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create scatter plots showing individual cell changes (OFF vs ON) for each metric.
        
        One figure per metric with 2 panels:
        - Left: AC-pStr cells
        - Right: Th-pStr cells
        """
        print("\n" + "="*70)
        print("GENERATING SCATTER PLOTS (Individual Cell Changes)")
        print("="*70)
        
        for metric_name, metric_label in metrics_to_plot.items():
            print(f"\n  Creating scatter plot for {metric_label}...")
            
            # Create figure with 1x2 subplots
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            
            # Panel 1: AC-pStr
            ax = axes[0]
            ac_off_col = f'{metric_name}_off'
            ac_on_col = f'{metric_name}_on'
            ac_valid = ac_df[[ac_off_col, ac_on_col]].dropna()
            
            if len(ac_valid) > 0:
                ac_off = ac_valid[ac_off_col].values
                ac_on = ac_valid[ac_on_col].values
                
                # Scatter plot
                ax.scatter(ac_off, ac_on, alpha=0.6, s=50, 
                          color='#4472C4', edgecolors='black', linewidth=0.5)
                
                # Unity line (no change)
                min_val = min(ac_off.min(), ac_on.min())
                max_val = max(ac_off.max(), ac_on.max())
                ax.plot([min_val, max_val], [min_val, max_val], 
                       'k--', linewidth=2, alpha=0.5, label='No change')
                
                # Format
                ax.set_xlabel(f'{metric_label} (Laser OFF)', fontsize=11, fontweight='bold')
                ax.set_ylabel(f'{metric_label} (Laser ON)', fontsize=11, fontweight='bold')
                ax.set_title(f'AC-pStr (n={len(ac_valid)})', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend(loc='best', fontsize=9)
                ax.set_aspect('equal', adjustable='box')
            
            # Panel 2: Control
            ax = axes[1]
            control_off_col = f'{metric_name}_off'
            control_on_col = f'{metric_name}_on'
            control_valid = control_df[[control_off_col, control_on_col]].dropna()
            
            if len(control_valid) > 0:
                control_off = control_valid[control_off_col].values
                control_on = control_valid[control_on_col].values
                
                # Scatter plot
                ax.scatter(control_off, control_on, alpha=0.6, s=50,
                          color='#C55A11', edgecolors='black', linewidth=0.5)
                
                # Unity line (no change)
                min_val = min(control_off.min(), control_on.min())
                max_val = max(control_off.max(), control_on.max())
                ax.plot([min_val, max_val], [min_val, max_val],
                       'k--', linewidth=2, alpha=0.5, label='No change')
                
                # Format
                ax.set_xlabel(f'{metric_label} (Laser OFF)', fontsize=11, fontweight='bold')
                ax.set_ylabel(f'{metric_label} (Laser ON)', fontsize=11, fontweight='bold')
                ax.set_title(f'Control (n={len(control_valid)})', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend(loc='best', fontsize=9)
                ax.set_aspect('equal', adjustable='box')
            
            # Overall title
            tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
            gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
            fig.suptitle(f'{metric_label}: Individual Cell Changes from {gaussian_type}\n({tuning_label})',
                        fontsize=13, fontweight='bold')
            
            plt.tight_layout()
            
            # Save
            output_path = os.path.join(output_dir, f'{metric_name}_scatter.png')
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            print(f"    Saved: {output_path}")
    
    def create_delta_distribution_plots(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
        metrics_to_plot: Dict[str, str],
        output_dir: str
    ):
        """
        Create distribution plots showing the change (delta = ON - OFF) for each metric.
        
        One figure per metric comparing AC-pStr vs Control distributions.
        """
        print("\n" + "="*70)
        print("GENERATING DELTA DISTRIBUTION PLOTS")
        print("="*70)
        
        for metric_name, metric_label in metrics_to_plot.items():
            print(f"\n  Creating delta distribution for {metric_label}...")
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Calculate deltas
            ac_off_col = f'{metric_name}_off'
            ac_on_col = f'{metric_name}_on'
            ac_valid = ac_df[[ac_off_col, ac_on_col]].dropna()
            ac_delta = (ac_valid[ac_on_col] - ac_valid[ac_off_col]).values
            
            control_off_col = f'{metric_name}_off'
            control_on_col = f'{metric_name}_on'
            control_valid = control_df[[control_off_col, control_on_col]].dropna()
            control_delta = (control_valid[control_on_col] - control_valid[control_off_col]).values
            
            # Create violin plots
            positions = [1, 2]
            parts = ax.violinplot([ac_delta, control_delta], positions=positions,
                                 showmeans=True, showmedians=True, widths=0.7)
            
            # Color the violins
            colors = ['#4472C4', '#C55A11']
            for i, pc in enumerate(parts['bodies']):
                pc.set_facecolor(colors[i])
                pc.set_alpha(0.7)
                pc.set_edgecolor('black')
                pc.set_linewidth(1.5)
            
            # Overlay individual points with jitter
            np.random.seed(42)
            jitter_strength = 0.04
            
            # AC-pStr points
            jitter_ac = np.random.normal(0, jitter_strength, len(ac_delta))
            ax.scatter(1 + jitter_ac, ac_delta, alpha=0.4, s=20,
                      color='#4472C4', edgecolors='black', linewidth=0.3)
            
            # Control points
            jitter_control = np.random.normal(0, jitter_strength, len(control_delta))
            ax.scatter(2 + jitter_control, control_delta, alpha=0.4, s=20,
                      color='#C55A11', edgecolors='black', linewidth=0.3)
            
            # Add zero line (no change)
            ax.axhline(0, color='black', linestyle='--', linewidth=2, alpha=0.5)
            
            # Statistical test: Mann-Whitney U test (independent samples)
            # Tests if the distributions of changes differ between pathways
            if len(ac_delta) >= 3 and len(control_delta) >= 3:
                u_stat, p_value = stats.mannwhitneyu(ac_delta, control_delta, alternative='two-sided')
                sig_label = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
                
                # Add bracket between groups to show comparison
                y_top = ax.get_ylim()[1] * 0.88
                ax.plot([1, 2], [y_top, y_top], '-', linewidth=1.5)
                ax.text(1.5, y_top + (ax.get_ylim()[1] * 0.02), sig_label,
                       ha='center', va='bottom', fontsize=12, fontweight='bold')
                ax.text(1.5, y_top - (ax.get_ylim()[1] * 0.03), f'p={p_value:.2e}',
                       ha='center', va='top', fontsize=9)
            
            # Add mean values as text
            ac_mean = np.mean(ac_delta)
            control_mean = np.mean(control_delta)
            ax.text(1, ax.get_ylim()[1] * 0.72, f'Mean: {ac_mean:.3f}',
                   ha='center', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                            edgecolor='black', alpha=0.8))
            ax.text(2, ax.get_ylim()[1] * 0.72, f'Mean: {control_mean:.3f}',
                   ha='center', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                            edgecolor='black', alpha=0.8))
            
            # Format axes
            ax.set_xticks([1, 2])
            ax.set_xticklabels([f'AC-pStr\n(n={len(ac_delta)})', 
                               f'Control\n(n={len(control_delta)})'],
                              fontsize=11, fontweight='bold')
            ax.set_ylabel(f'Change in {metric_label}\n(Laser ON - Laser OFF)',
                         fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Title
            tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
            gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
            ax.set_title(f'{metric_label}: Distribution of Changes from {gaussian_type}\n({tuning_label})',
                        fontsize=13, fontweight='bold', pad=15)
            
            plt.tight_layout()
            
            # Save
            output_path = os.path.join(output_dir, f'{metric_name}_delta_distribution.png')
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            print(f"    Saved: {output_path}")
    
    def create_pdf_report(
        self,
        ac_df: pd.DataFrame,
        control_df: pd.DataFrame,
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
        pdf_filename = f'AC_vs_Control_comparison_report_{self.config.tuning_type}.pdf'
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
                self._plot_scatter_for_pdf(ax2_left, ax2_right, ac_df, control_df, metric_name, metric_label)
                
                # Row 3: Delta distribution
                ax3 = plt.subplot(3, 1, 3)
                self._plot_delta_distribution_for_pdf(ax3, ac_df, control_df, metric_name, metric_label)
                
                # Overall title for the page
                gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
                fig.suptitle(f'{metric_label} - Pathway Comparison ({gaussian_type})\n({tuning_label})',
                           fontsize=16, fontweight='bold', y=0.995)
                
                plt.tight_layout(rect=[0, 0, 1, 0.985])
                pdf.savefig(fig, dpi=150)
                plt.close(fig)
            
            # Add population tuning curves (4-panel)
            print("\n  Adding 4-panel population tuning curves to PDF...")
            fig = self._create_population_tuning_figure(ac_df, control_df, '4-panel')
            pdf.savefig(fig, dpi=150)
            plt.close(fig)
            
            # Add population tuning comparison (2-panel overlaid)
            print("\n  Adding 2-panel population tuning comparison to PDF...")
            fig = self._create_population_tuning_comparison_figure(ac_df, control_df)
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
            d['Title'] = f'AC-pStr Experimental vs Control Comparison ({tuning_label})'
            d['Author'] = 'Hylen'
            d['Subject'] = 'Optogenetic experimental vs control comparison analysis'
            d['Keywords'] = f'{tuning_label}, AC-pStr, Control, Optogenetics'
        
        print(f"\n  PDF report saved: {pdf_path}")
    
    def _plot_bar_comparison_for_pdf(self, ax, stats, metric_label):
        """Plot bar comparison for PDF (simplified version)."""
        ac_stats = stats['AC-pStr']
        control_stats = stats['Control']
        
        x_positions = [1, 2, 4, 5]
        means = [ac_stats['mean_off'], ac_stats['mean_on'],
                control_stats['mean_off'], control_stats['mean_on']]
        sems = [ac_stats['sem_off'], ac_stats['sem_on'],
               control_stats['sem_off'], control_stats['sem_on']]
        colors = ['#4472C4', '#2E4A7C', '#C55A11', '#8B3F0C']
        
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
        self._add_significance_bracket(ax, 1, 2, means[0:2], sems[0:2], ac_stats)
        self._add_significance_bracket(ax, 4, 5, means[2:4], sems[2:4], control_stats)
        
        ax.set_ylabel(metric_label, fontsize=11, fontweight='bold')
        ax.set_xticks([1.5, 4.5])
        ax.set_xticklabels([f'AC-pStr\n(n={ac_stats["n"]})', f'Control\n(n={control_stats["n"]})'],
                          fontsize=10, fontweight='bold')
        ax.set_xlim([0, 6])
        ax.set_ylim([0, y_max + 0.25])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add legend
        self._add_legend(ax)
        
        ax.set_title('Bar Chart: Laser OFF vs ON', fontsize=11, fontweight='bold', pad=10)
    
    def _plot_scatter_for_pdf(self, ax_left, ax_right, ac_df, control_df, metric_name, metric_label):
        """Plot scatter plots for PDF."""
        # AC-pStr
        ac_off_col = f'{metric_name}_off'
        ac_on_col = f'{metric_name}_on'
        ac_valid = ac_df[[ac_off_col, ac_on_col]].dropna()
        
        if len(ac_valid) > 0:
            ac_off = ac_valid[ac_off_col].values
            ac_on = ac_valid[ac_on_col].values
            
            ax_left.scatter(ac_off, ac_on, alpha=0.6, s=40,
                          color='#4472C4', edgecolors='black', linewidth=0.5)
            min_val = min(ac_off.min(), ac_on.min())
            max_val = max(ac_off.max(), ac_on.max())
            ax_left.plot([min_val, max_val], [min_val, max_val],
                        'k--', linewidth=1.5, alpha=0.5)
            
            ax_left.set_xlabel(f'{metric_label} (OFF)', fontsize=9, fontweight='bold')
            ax_left.set_ylabel(f'{metric_label} (ON)', fontsize=9, fontweight='bold')
            ax_left.set_title(f'AC-pStr (n={len(ac_valid)})', fontsize=10, fontweight='bold')
            ax_left.grid(True, alpha=0.3)
            ax_left.set_aspect('equal', adjustable='box')
        
        # Control
        control_off_col = f'{metric_name}_off'
        control_on_col = f'{metric_name}_on'
        control_valid = control_df[[control_off_col, control_on_col]].dropna()
        
        if len(control_valid) > 0:
            control_off = control_valid[control_off_col].values
            control_on = control_valid[control_on_col].values
            
            ax_right.scatter(control_off, control_on, alpha=0.6, s=40,
                           color='#C55A11', edgecolors='black', linewidth=0.5)
            min_val = min(control_off.min(), control_on.min())
            max_val = max(control_off.max(), control_on.max())
            ax_right.plot([min_val, max_val], [min_val, max_val],
                         'k--', linewidth=1.5, alpha=0.5)
            
            ax_right.set_xlabel(f'{metric_label} (OFF)', fontsize=9, fontweight='bold')
            ax_right.set_ylabel(f'{metric_label} (ON)', fontsize=9, fontweight='bold')
            ax_right.set_title(f'Control (n={len(control_valid)})', fontsize=10, fontweight='bold')
            ax_right.grid(True, alpha=0.3)
            ax_right.set_aspect('equal', adjustable='box')
    
    def _plot_delta_distribution_for_pdf(self, ax, ac_df, control_df, metric_name, metric_label):
        """Plot delta distribution for PDF."""
        # Calculate deltas
        ac_off_col = f'{metric_name}_off'
        ac_on_col = f'{metric_name}_on'
        ac_valid = ac_df[[ac_off_col, ac_on_col]].dropna()
        ac_delta = (ac_valid[ac_on_col] - ac_valid[ac_off_col]).values
        
        control_off_col = f'{metric_name}_off'
        control_on_col = f'{metric_name}_on'
        control_valid = control_df[[control_off_col, control_on_col]].dropna()
        control_delta = (control_valid[control_on_col] - control_valid[control_off_col]).values
        
        # Violin plots
        positions = [1, 2]
        parts = ax.violinplot([ac_delta, control_delta], positions=positions,
                             showmeans=True, showmedians=True, widths=0.7)
        
        colors = ['#4472C4', '#C55A11']
        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(colors[i])
            pc.set_alpha(0.7)
            pc.set_edgecolor('black')
            pc.set_linewidth(1.2)
        
        # Scatter points
        np.random.seed(42)
        jitter_ac = np.random.normal(0, 0.04, len(ac_delta))
        ax.scatter(1 + jitter_ac, ac_delta, alpha=0.3, s=15,
                  color='#4472C4', edgecolors='black', linewidth=0.2)
        
        jitter_control = np.random.normal(0, 0.04, len(control_delta))
        ax.scatter(2 + jitter_control, control_delta, alpha=0.3, s=15,
                  color='#C55A11', edgecolors='black', linewidth=0.2)
        
        ax.axhline(0, color='black', linestyle='--', linewidth=1.5, alpha=0.5)
        
        # Statistical test
        if len(ac_delta) >= 3 and len(control_delta) >= 3:
            u_stat, p_value = stats.mannwhitneyu(ac_delta, control_delta, alternative='two-sided')
            sig_label = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
            
            y_top = ax.get_ylim()[1] * 0.88
            ax.plot([1, 2], [y_top, y_top], 'k-', linewidth=1.2)
            ax.text(1.5, y_top + (ax.get_ylim()[1] * 0.02), sig_label,
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
            ax.text(1.5, y_top - (ax.get_ylim()[1] * 0.03), f'p={p_value:.2e}',
                   ha='center', va='top', fontsize=8)
        
        # Mean values
        ac_mean = np.mean(ac_delta)
        control_mean = np.mean(control_delta)
        ax.text(1, ax.get_ylim()[1] * 0.72, f'Mean: {ac_mean:.3f}',
               ha='center', fontsize=8, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        edgecolor='black', alpha=0.8))
        ax.text(2, ax.get_ylim()[1] * 0.72, f'Mean: {control_mean:.3f}',
               ha='center', fontsize=8, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        edgecolor='black', alpha=0.8))
        
        ax.set_xticks([1, 2])
        ax.set_xticklabels([f'AC-pStr\n(n={len(ac_delta)})', f'Control\n(n={len(control_delta)})'],
                          fontsize=10, fontweight='bold')
        ax.set_ylabel(f'Change in {metric_label}\n(Laser ON - OFF)', fontsize=9, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_title('Delta Distribution', fontsize=11, fontweight='bold', pad=10)
    
    def _create_population_tuning_figure(self, ac_df, control_df, title_suffix):
        """Create 4-panel population tuning curves figure for PDF."""
        fig, axes = plt.subplots(2, 2, figsize=(11, 10))
        
        conditions = [
            (ac_df, 'off', 'AC-pStr Laser OFF', axes[0, 0], '#4472C4'),
            (ac_df, 'on', 'AC-pStr Laser ON', axes[1, 0], '#2E4A7C'),
            (control_df, 'off', 'Control Laser OFF', axes[0, 1], '#C55A11'),
            (control_df, 'on', 'Control Laser ON', axes[1, 1], '#8B3F0C')
        ]
        
        for df, condition, title, ax, color in conditions:
            octaves, mean_rates, sem_rates, n_cells = self._calculate_population_tuning(df, condition)
            
            if len(octaves) > 0:
                ax.plot(octaves, mean_rates, '-o', color=color, linewidth=2,
                       markersize=5, markeredgecolor='black', markeredgewidth=0.5)
                ax.fill_between(octaves, mean_rates - sem_rates, mean_rates + sem_rates,
                               color=color, alpha=0.3)
                
                ax.set_xlabel('Octaves from Best Frequency', fontsize=10, fontweight='bold')
                ax.set_ylabel('Firing Rate (Hz)', fontsize=10, fontweight='bold')
                ax.set_title(f'{title}\n(n={n_cells})', fontsize=11, fontweight='bold')
                ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
                ax.grid(True, alpha=0.3)
        
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        fig.suptitle(f'Population-Average Tuning Curves from {gaussian_type} ({tuning_label})',
                    fontsize=14, fontweight='bold')
        
       
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        return fig
    
    def _create_population_tuning_comparison_figure(self, ac_df, control_df):
        """Create 2-panel population tuning comparison figure for PDF."""
        fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
        
        # AC-pStr
        ax = axes[0]
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(ac_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(ac_df, 'on')
        
        ax.plot(octaves_off, mean_off, '-o', color='#4472C4', linewidth=2,
               markersize=5, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color='#4472C4', alpha=0.3)
        
        ax.plot(octaves_on, mean_on, '-o', color='#2E4A7C', linewidth=2,
               markersize=5, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color='#2E4A7C', alpha=0.3)
        
        ax.set_xlabel('Octaves from Best Frequency', fontsize=11, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=11, fontweight='bold')
        ax.set_title('AC-pStr Pathway', fontsize=12, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)
        
        # Th-pStr
        ax = axes[1]
        octaves_off, mean_off, sem_off, n_off = self._calculate_population_tuning(control_df, 'off')
        octaves_on, mean_on, sem_on, n_on = self._calculate_population_tuning(control_df, 'on')
        
        ax.plot(octaves_off, mean_off, '-o', color='#C55A11', linewidth=2,
               markersize=5, label=f'Laser OFF (n={n_off})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_off, mean_off - sem_off, mean_off + sem_off,
                       color='#C55A11', alpha=0.3)
        
        ax.plot(octaves_on, mean_on, '-o', color='#8B3F0C', linewidth=2,
               markersize=5, label=f'Laser ON (n={n_on})',
               markeredgecolor='black', markeredgewidth=0.5)
        ax.fill_between(octaves_on, mean_on - sem_on, mean_on + sem_on,
                       color='#8B3F0C', alpha=0.3)
        
        ax.set_xlabel('Octaves from Best Frequency', fontsize=11, fontweight='bold')
        ax.set_ylabel('Firing Rate (Hz)', fontsize=11, fontweight='bold')
        ax.set_title('Control Group', fontsize=12, fontweight='bold')
        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)
        
        tuning_label = 'Frequency Tuning' if self.config.tuning_type == 'frequency' else 'AM Tuning'
        gaussian_type = 'Fitted Gaussians' if self.config.tuning_type == 'frequency' else 'Fitted Log-Gaussians'
        fig.suptitle(f'Population Tuning Comparison from {gaussian_type}: OFF vs ON ({tuning_label})',
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
        """Add legend for laser conditions."""
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#4472C4', edgecolor='black', label='Laser OFF', alpha=0.8),
            Patch(facecolor='#2E4A7C', edgecolor='black', label='Laser ON', alpha=0.8),
            Patch(facecolor='#C55A11', edgecolor='black', label='Laser OFF', alpha=0.8),
            Patch(facecolor='#8B3F0C', edgecolor='black', label='Laser ON', alpha=0.8)
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.9)
    
    @staticmethod
    def _add_sample_sizes_top(ax, ac_stats, control_stats, y_max):
        """Add sample size annotations near the bottom, just above x-axis."""
        # Position at 10% of y-axis height (near bottom but above x-axis)
        bottom_position = y_max * 0.10
        
        # Add n annotations at bottom position, centered over each group
        ax.text(1.5, bottom_position, f'n = {ac_stats["n"]}', ha='center', va='center',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                        edgecolor='black', linewidth=1.5, alpha=0.9))
        ax.text(4.5, bottom_position, f'n = {control_stats["n"]}', ha='center', va='center',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                        edgecolor='black', linewidth=1.5, alpha=0.9))


# =============================================================================
# MAIN COORDINATOR
# =============================================================================

class PathwayComparisonCoordinator:
    """Coordinates the experimental vs control comparison analysis."""
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
        self.loader = PathwayDataLoader(config)
        self.comparator = PathwayComparator(config)
        self.visualizer = PathwayVisualizer(config)
    
    def run(self):
        """Execute complete comparison analysis."""
        print("="*70)
        print("AC-pStr EXPERIMENTAL vs CONTROL COMPARISON")
        print("="*70)
        
        # Load data
        ac_df, control_df = self.loader.load_both_pathways()
        
        # Test within-group laser effects for all metrics
        all_stats = self.comparator.test_all_metrics(
            ac_df, control_df, self.config.metrics_to_plot
        )
        
        # Create output directory
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Generate comparison plots for all metrics
        self.visualizer.create_all_metric_plots(
            ac_df, control_df, all_stats, 
            self.config.metrics_to_plot, 
            self.config.output_dir
        )
        
        # Generate population tuning curves (4-panel)
        self.visualizer.create_population_tuning_curves(
            ac_df, control_df, self.config.output_dir
        )
        
        # Generate population tuning curves comparison (2-panel, ON/OFF overlaid)
        self.visualizer.create_population_tuning_comparison(
            ac_df, control_df, self.config.output_dir
        )
        
        # Generate NORMALIZED population tuning curves (cell-specific normalization)
        self.visualizer.create_population_tuning_curves_normalized(
            ac_df, control_df, self.config.output_dir
        )
        
        # Generate NORMALIZED population tuning comparison (2-panel, ON/OFF overlaid)
        self.visualizer.create_population_tuning_comparison_normalized(
            ac_df, control_df, self.config.output_dir
        )
        
        # Generate scatter plots (individual cell changes)
        self.visualizer.create_scatter_plots(
            ac_df, control_df, self.config.metrics_to_plot, self.config.output_dir
        )
        
        # Generate delta distribution plots
        self.visualizer.create_delta_distribution_plots(
            ac_df, control_df, self.config.metrics_to_plot, self.config.output_dir
        )
        
        # Generate comprehensive PDF report
        self.visualizer.create_pdf_report(
            ac_df, control_df, all_stats, self.config.metrics_to_plot, self.config.output_dir
        )
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"AC-pStr cells: {len(ac_df)}")
        print(f"Control cells: {len(control_df)}")
        print(f"Metrics analyzed: {len(self.config.metrics_to_plot)}")
        
        # Count significant effects
        n_sig_ac = sum(1 for stats in all_stats.values() if stats['AC-pStr']['significant'])
        n_sig_control = sum(1 for stats in all_stats.values() if stats['Control']['significant'])
        
        print(f"\nSignificant laser effects (p < {self.config.alpha}):")
        print(f"  AC-pStr: {n_sig_ac}/{len(all_stats)} metrics")
        print(f"  Control: {n_sig_control}/{len(all_stats)} metrics")
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
    freq_coordinator = PathwayComparisonCoordinator(freq_config)
    
    try:
        freq_coordinator.run()
        print("\n" + "="*70)
        print("FREQUENCY TUNING ANALYSIS COMPLETED")
        print("="*70)
    except Exception as e:
        print(f"\nERROR in Frequency Analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # AM tuning analysis - SKIP if data doesn't exist yet
    print("\n\n" + "="*70)
    print("CHECKING FOR AM TUNING DATA...")
    print("="*70 + "\n")
    
    am_config = ComparisonConfig(tuning_type='am')
    
    # Check if AM Gaussian fit data exists (uses log_gaussian_fits for AM!)
    am_ac_csv = os.path.join(am_config.ac_pstr_dir, 'all_sessions_laser_off_log_gaussian_fits.csv')
    if not os.path.exists(am_ac_csv):
        print(f"AM Gaussian fit data not found at: {am_config.ac_pstr_dir}")
        print("Skipping AM analysis - generate AM Gaussian fits first!")
    else:
        print("RUNNING AM TUNING ANALYSIS")
        print("="*70 + "\n")
        
        am_coordinator = PathwayComparisonCoordinator(am_config)
        
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
    if os.path.exists(am_ac_csv):
        print(f"AM tuning results: {am_config.output_dir}")
    else:
        print(f"AM tuning results: SKIPPED (no Gaussian fit data)")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
