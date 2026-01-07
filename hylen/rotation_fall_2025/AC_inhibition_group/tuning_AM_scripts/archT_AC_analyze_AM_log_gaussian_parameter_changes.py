"""
Analyze Log-Gaussian AM Parameter Changes: Laser OFF vs ON

This script analyzes how Log-Gaussian AM tuning parameters change with laser stimulation:
- Baseline (spontaneous firing floor)
- Amplitude (dynamic range)
- Preferred Rate (best AM rate shift)
- Sigma (tuning width/selectivity in log10-space)

Focuses on two groups:
1. Good fits: Cells with high-quality Log-Gaussian fits (R² ≥ threshold)
2. Empirically tuned: Cells classified as 'tuned' by empirical AM metrics

Author: Hylen
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from scipy import stats
from dataclasses import dataclass
from typing import Tuple, Dict, List

# Add hylen directory to path
sys.path.insert(0, '/home/jarauser/src/jaratest/hylen')
from config import get_reports_subdir


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class AnalysisConfig:
    """Configuration for parameter change analysis."""
    # Experiment identification
    experiment_name: str = 'AC - pStr Inhibition with AM'
    
    # Analysis parameters
    r_squared_threshold: float = 0.4  # For "good fits" group (matches fitting script)
    
    # Plotting style
    fig_width: float = 16
    fig_height: float = 10
    point_alpha: float = 0.6
    point_size: float = 50
    
    # Use centralized config for directories
    @property
    def gaussian_fits_dir(self) -> str:
        """Get Gaussian fits directory from config."""
        return str(get_reports_subdir('tuning_AM_gaussian_fits'))
    
    @property
    def output_dir(self) -> str:
        """Get output directory from config."""
        return str(get_reports_subdir('tuning_AM_gaussian_parameter_analysis'))
    
    @property
    def metrics_dir(self) -> str:
        """Get metrics directory from config."""
        return str(get_reports_subdir('tuning_AM_analysis'))


# =============================================================================
# DATA LOADING
# =============================================================================

class LogGaussianFitLoader:
    """Loads and pairs Log-Gaussian fit data for OFF vs ON comparison."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
    
    def load_paired_data(self) -> pd.DataFrame:
        """
        Load Log-Gaussian fits for laser OFF and ON, pair them by cell.
        
        Returns:
            DataFrame with columns for both OFF and ON parameters
        """
        # Load combined OFF and ON data
        off_path = os.path.join(self.config.gaussian_fits_dir, 'all_sessions_laser_off_log_gaussian_fits.csv')
        on_path = os.path.join(self.config.gaussian_fits_dir, 'all_sessions_laser_on_log_gaussian_fits.csv')
        
        df_off = pd.read_csv(off_path)
        df_on = pd.read_csv(on_path)
        
        print(f"Loaded {len(df_off)} OFF cells, {len(df_on)} ON cells")
        
        # Merge on session_id and cell_idx
        df_paired = df_off.merge(
            df_on,
            on=['session_id', 'cell_idx', 'subject', 'date', 'depth'],
            suffixes=('_off', '_on'),
            how='inner'
        )
        
        print(f"Paired {len(df_paired)} cells with both OFF and ON data")
        
        # Calculate change metrics (absolute differences)
        df_paired['delta_baseline'] = df_paired['baseline_on'] - df_paired['baseline_off']
        df_paired['delta_amplitude'] = df_paired['amplitude_on'] - df_paired['amplitude_off']
        df_paired['delta_preferred_rate'] = df_paired['preferred_rate_on'] - df_paired['preferred_rate_off']
        df_paired['delta_sigma'] = df_paired['sigma_on'] - df_paired['sigma_off']
        
        # Percent changes
        df_paired['pct_change_baseline'] = 100 * df_paired['delta_baseline'] / (df_paired['baseline_off'] + 0.1)
        df_paired['pct_change_amplitude'] = 100 * df_paired['delta_amplitude'] / (df_paired['amplitude_off'] + 0.1)
        df_paired['pct_change_preferred_rate'] = 100 * df_paired['delta_preferred_rate'] / (df_paired['preferred_rate_off'] + 0.1)
        df_paired['pct_change_sigma'] = 100 * df_paired['delta_sigma'] / (df_paired['sigma_off'] + 0.01)
        
        return df_paired
    
    def filter_good_fits(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to cells with good fits in BOTH conditions."""
        good_mask = (
            (df['fit_quality_off'] == 'good') &
            (df['fit_quality_on'] == 'good')
        )
        return df[good_mask].copy()
    
    def filter_empirically_tuned(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter to empirically tuned cells from AM metrics classification."""
        # Use config property for metrics directory
        metrics_dir = self.config.metrics_dir
        
        # Collect tuned cells from all sessions
        tuned_cells = set()
        
        for session_id in df['session_id'].unique():
            metrics_path = os.path.join(metrics_dir, f'session_{int(session_id)}_laser_off_tuning_metrics.csv')
            
            if os.path.exists(metrics_path):
                metrics_df = pd.read_csv(metrics_path)
                
                # Check if tuning_category column exists
                if 'tuning_category' in metrics_df.columns:
                    # Get cells classified as 'tuned'
                    tuned_in_session = metrics_df[metrics_df['tuning_category'] == 'tuned']['cell_idx'].values
                    
                    # Add to set as (session_id, cell_idx) tuples
                    for cell_idx in tuned_in_session:
                        tuned_cells.add((int(session_id), int(cell_idx)))
        
        # Filter dataframe to only tuned cells
        if len(tuned_cells) > 0:
            tuned_mask = df.apply(
                lambda row: (int(row['session_id']), int(row['cell_idx'])) in tuned_cells,
                axis=1
            )
            print(f"  Found {tuned_mask.sum()} empirically tuned cells (from tuning_category=='tuned')")
            return df[tuned_mask].copy()
        else:
            print("  WARNING: No cells found with tuning_category=='tuned'")
            print("  Falling back to all cells with successful fits")
            # Fallback: return cells with successful fits
            return df[
                (df['fit_quality_off'] != 'failed') &
                (df['fit_quality_on'] != 'failed')
            ].copy()


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

class ParameterChangeAnalyzer:
    """Statistical analysis of parameter changes."""
    
    @staticmethod
    def paired_t_test(off_values: np.ndarray, on_values: np.ndarray) -> Tuple[float, float]:
        """Perform paired t-test."""
        # Remove NaN values
        valid_mask = ~(np.isnan(off_values) | np.isnan(on_values))
        off_clean = off_values[valid_mask]
        on_clean = on_values[valid_mask]
        
        if len(off_clean) < 3:
            return np.nan, np.nan
        
        t_stat, p_value = stats.ttest_rel(off_clean, on_clean)
        return t_stat, p_value
    
    @staticmethod
    def wilcoxon_test(off_values: np.ndarray, on_values: np.ndarray) -> Tuple[float, float]:
        """Perform Wilcoxon signed-rank test (non-parametric)."""
        valid_mask = ~(np.isnan(off_values) | np.isnan(on_values))
        off_clean = off_values[valid_mask]
        on_clean = on_values[valid_mask]
        
        if len(off_clean) < 3:
            return np.nan, np.nan
        
        try:
            stat, p_value = stats.wilcoxon(off_clean, on_clean)
            return stat, p_value
        except:
            return np.nan, np.nan
    
    def summarize_changes(self, df: pd.DataFrame, group_name: str) -> pd.DataFrame:
        """Create summary statistics for parameter changes."""
        params = ['baseline', 'amplitude', 'preferred_rate', 'sigma']
        
        summary_data = []
        
        for param in params:
            off_col = f'{param}_off'
            on_col = f'{param}_on'
            delta_col = f'delta_{param}'
            
            off_vals = df[off_col].values
            on_vals = df[on_col].values
            delta_vals = df[delta_col].values
            
            # Remove NaNs
            valid_mask = ~(np.isnan(off_vals) | np.isnan(on_vals))
            off_clean = off_vals[valid_mask]
            on_clean = on_vals[valid_mask]
            delta_clean = delta_vals[valid_mask]
            
            if len(off_clean) == 0:
                continue
            
            # Statistics
            t_stat, p_paired = self.paired_t_test(off_vals, on_vals)
            w_stat, p_wilcoxon = self.wilcoxon_test(off_vals, on_vals)
            
            summary_data.append({
                'group': group_name,
                'parameter': param,
                'n_cells': len(off_clean),
                'off_mean': np.mean(off_clean),
                'off_std': np.std(off_clean),
                'off_median': np.median(off_clean),
                'on_mean': np.mean(on_clean),
                'on_std': np.std(on_clean),
                'on_median': np.median(on_clean),
                'delta_mean': np.mean(delta_clean),
                'delta_std': np.std(delta_clean),
                'delta_median': np.median(delta_clean),
                't_statistic': t_stat,
                'p_value_paired_t': p_paired,
                'wilcoxon_stat': w_stat,
                'p_value_wilcoxon': p_wilcoxon,
                'n_increased': np.sum(delta_clean > 0),
                'n_decreased': np.sum(delta_clean < 0),
                'n_unchanged': np.sum(delta_clean == 0)
            })
        
        return pd.DataFrame(summary_data)


# =============================================================================
# VISUALIZATION
# =============================================================================

class ParameterChangePlotter:
    """Create visualizations of parameter changes."""
    
    def __init__(self, config: AnalysisConfig):
        self.config = config
        sns.set_style("whitegrid")
    
    def plot_scatter_comparison(self, df: pd.DataFrame, param: str, ax: plt.Axes, title: str):
        """Scatter plot: OFF vs ON for a single parameter."""
        off_col = f'{param}_off'
        on_col = f'{param}_on'
        
        # Remove NaNs
        valid_mask = ~(np.isnan(df[off_col]) | np.isnan(df[on_col]))
        off_vals = df.loc[valid_mask, off_col]
        on_vals = df.loc[valid_mask, on_col]
        
        # Scatter plot
        ax.scatter(off_vals, on_vals, alpha=self.config.point_alpha, 
                  s=self.config.point_size, edgecolors='black', linewidth=0.5)
        
        # Unity line
        min_val = min(off_vals.min(), on_vals.min())
        max_val = max(off_vals.max(), on_vals.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, linewidth=2, label='Unity')
        
        # Statistics
        mean_off = off_vals.mean()
        mean_on = on_vals.mean()
        
        ax.axvline(mean_off, color='blue', linestyle=':', linewidth=2, alpha=0.7, label=f'Mean OFF = {mean_off:.2f}')
        ax.axhline(mean_on, color='red', linestyle=':', linewidth=2, alpha=0.7, label=f'Mean ON = {mean_on:.2f}')
        
        ax.set_xlabel(f'{param.replace("_", " ").title()} - Laser OFF', fontsize=11, fontweight='bold')
        ax.set_ylabel(f'{param.replace("_", " ").title()} - Laser ON', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3)
    
    def plot_delta_distribution(self, df: pd.DataFrame, param: str, ax: plt.Axes, title: str):
        """Histogram of parameter changes (delta values)."""
        delta_col = f'delta_{param}'
        delta_vals = df[delta_col].dropna()
        
        # Histogram
        ax.hist(delta_vals, bins=30, alpha=0.7, edgecolor='black', linewidth=1.2)
        
        # Statistics
        mean_delta = delta_vals.mean()
        median_delta = delta_vals.median()
        
        ax.axvline(0, color='black', linestyle='--', linewidth=2, label='No change')
        ax.axvline(mean_delta, color='red', linestyle='-', linewidth=2, 
                  label=f'Mean Δ = {mean_delta:.3f}')
        ax.axvline(median_delta, color='blue', linestyle=':', linewidth=2,
                  label=f'Median Δ = {median_delta:.3f}')
        
        ax.set_xlabel(f'Δ {param.replace("_", " ").title()} (ON - OFF)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
    
    def create_summary_figure(self, df: pd.DataFrame, group_name: str, output_path: str):
        """Create comprehensive 4x2 grid: scatter + histogram for each parameter."""
        params = ['baseline', 'amplitude', 'preferred_rate', 'sigma']
        param_labels = ['Baseline (spikes/s)', 'Amplitude (spikes/s)', 'Best AM Rate (Hz)', 'Sigma (log₁₀)']
        
        fig, axes = plt.subplots(4, 2, figsize=(self.config.fig_width, self.config.fig_height))
        
        for i, (param, label) in enumerate(zip(params, param_labels)):
            # Left column: Scatter (OFF vs ON)
            self.plot_scatter_comparison(df, param, axes[i, 0], f'{label}: OFF vs ON')
            
            # Right column: Delta distribution
            self.plot_delta_distribution(df, param, axes[i, 1], f'{label}: Change Distribution')
        
        fig.suptitle(f'{self.config.experiment_name}\nLog-Gaussian AM Parameter Changes: {group_name}\nn={len(df)} cells',
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout(rect=[0, 0, 1, 0.99])
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {output_path}")
    
    def create_bar_chart_summary(self, df_good: pd.DataFrame, df_tuned: pd.DataFrame, output_path: str):
        """Create bar charts comparing OFF vs ON values for each parameter and group."""
        params = ['baseline', 'amplitude', 'preferred_rate', 'sigma']
        param_labels = ['Baseline (spikes/s)', 'Amplitude (spikes/s)', 'Best AM Rate (Hz)', 'Sigma (log₁₀)']
        
        # Create figure with 2 rows (one per group) x 4 columns (one per parameter)
        fig, axes = plt.subplots(2, 4, figsize=(18, 10))
        
        for row_idx, (df, group_name) in enumerate([(df_good, 'Good Fits'), 
                                                     (df_tuned, 'Empirically Tuned Cells')]):
            for col_idx, (param, label) in enumerate(zip(params, param_labels)):
                ax = axes[row_idx, col_idx]
                
                off_col = f'{param}_off'
                on_col = f'{param}_on'
                
                # Get clean data
                valid_mask = ~(np.isnan(df[off_col]) | np.isnan(df[on_col]))
                off_vals = df.loc[valid_mask, off_col].values
                on_vals = df.loc[valid_mask, on_col].values
                
                if len(off_vals) == 0:
                    ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    continue
                
                # Calculate means and SEMs
                mean_off = np.mean(off_vals)
                sem_off = stats.sem(off_vals)
                mean_on = np.mean(on_vals)
                sem_on = stats.sem(on_vals)
                
                # Create bar chart
                x_pos = [0, 1]
                means = [mean_off, mean_on]
                sems = [sem_off, sem_on]
                colors = ['blue', 'red']
                labels_bar = ['OFF', 'ON']
                
                bars = ax.bar(x_pos, means, yerr=sems, capsize=8, alpha=0.7,
                             color=colors, edgecolor='black', linewidth=1.5,
                             error_kw={'linewidth': 2, 'ecolor': 'black'})
                
                # Perform paired tests
                _, p_val_ttest = stats.ttest_rel(off_vals, on_vals)
                try:
                    _, p_val_wilcoxon = stats.wilcoxon(off_vals, on_vals)
                except:
                    p_val_wilcoxon = np.nan
                
                # Use more conservative p-value
                p_val = max(p_val_ttest, p_val_wilcoxon) if not np.isnan(p_val_wilcoxon) else p_val_ttest
                
                # Add significance stars
                if p_val < 0.001:
                    sig_text = '***'
                elif p_val < 0.01:
                    sig_text = '**'
                elif p_val < 0.05:
                    sig_text = '*'
                else:
                    sig_text = 'n.s.'
                
                # Draw line connecting bars with significance
                y_max = max(mean_off + sem_off, mean_on + sem_on)
                y_line = y_max + 0.1 * np.abs(ax.get_ylim()[1] - ax.get_ylim()[0])
                ax.plot([0, 1], [y_line, y_line], 'k-', linewidth=2)
                ax.text(0.5, y_line, sig_text, ha='center', va='bottom',
                       fontsize=12, fontweight='bold')
                
                # Labels and formatting
                ax.set_ylabel(label, fontsize=11, fontweight='bold')
                ax.set_xticks(x_pos)
                ax.set_xticklabels(labels_bar, fontsize=11, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='y')
                
                # Add title with n and p-values on first row
                if row_idx == 0:
                    ax.set_title(f'{label}\n', fontsize=12, fontweight='bold')
                
                # Add group name and n on y-axis
                if col_idx == 0:
                    ax.text(-0.35, 0.5, f'{group_name}\n(n={len(off_vals)})', 
                           transform=ax.transAxes, rotation=90,
                           ha='center', va='center', fontsize=12, fontweight='bold')
                
                # Add p-values as small text
                p_text = f't: {p_val_ttest:.4f}\nW: {p_val_wilcoxon:.4f}'
                ax.text(0.5, -0.15, p_text, transform=ax.transAxes,
                       ha='center', va='top', fontsize=8, style='italic')
        
        fig.suptitle(f'{self.config.experiment_name}\nLog-Gaussian AM Parameters: Laser OFF vs ON Comparison\n(Error bars = SEM; *p<0.05, **p<0.01, ***p<0.001, n.s.=not significant)',
                    fontsize=14, fontweight='bold', y=0.98)
        
        plt.tight_layout(rect=[0.02, 0.02, 1, 0.96])
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {output_path}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main analysis pipeline."""
    print("="*70)
    print("LOG-GAUSSIAN AM PARAMETER CHANGE ANALYSIS")
    print("="*70)
    
    # Initialize
    config = AnalysisConfig()
    os.makedirs(config.output_dir, exist_ok=True)
    
    loader = LogGaussianFitLoader(config)
    analyzer = ParameterChangeAnalyzer()
    plotter = ParameterChangePlotter(config)
    
    # Load paired data
    print("\nLoading paired OFF/ON data...")
    df_all = loader.load_paired_data()
    
    # Filter groups
    print("\nFiltering groups...")
    df_good_fits = loader.filter_good_fits(df_all)
    df_tuned = loader.filter_empirically_tuned(df_all)
    
    print(f"  Good fits (both OFF and ON): {len(df_good_fits)} cells")
    print(f"  Empirically tuned cells: {len(df_tuned)} cells")
    
    # Statistical analysis
    print("\nPerforming statistical analysis...")
    summary_good = analyzer.summarize_changes(df_good_fits, 'Good Fits')
    summary_tuned = analyzer.summarize_changes(df_tuned, 'Empirically Tuned Cells')
    
    summary_combined = pd.concat([summary_good, summary_tuned], ignore_index=True)
    
    # Save summary statistics
    summary_path = os.path.join(config.output_dir, 'am_parameter_change_summary_statistics.csv')
    summary_combined.to_csv(summary_path, index=False)
    print(f"\nSaved summary statistics: {summary_path}")
    
    # Print summary to console
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    print(summary_combined.to_string(index=False))
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # Good fits
    good_fits_path = os.path.join(config.output_dir, 'am_parameter_changes_good_fits.png')
    plotter.create_summary_figure(df_good_fits, 'Good Fits', good_fits_path)
    
    # Empirically tuned
    tuned_path = os.path.join(config.output_dir, 'am_parameter_changes_empirically_tuned.png')
    plotter.create_summary_figure(df_tuned, 'Empirically Tuned Cells', tuned_path)
    
    # Bar chart summary comparing both groups
    bar_chart_path = os.path.join(config.output_dir, 'am_parameter_changes_bar_chart_summary.png')
    plotter.create_bar_chart_summary(df_good_fits, df_tuned, bar_chart_path)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print(f"Results saved to: {config.output_dir}")


if __name__ == '__main__':
    main()
