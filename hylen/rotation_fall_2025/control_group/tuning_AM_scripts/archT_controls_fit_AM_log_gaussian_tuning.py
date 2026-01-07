"""
Fit Log-Gaussian Models to AM Rate Tuning Curves

This script fits Log-Gaussian models to AM rate tuning curves for both laser OFF and ON conditions.

Key differences from frequency tuning:
- Uses LOG-GAUSSIAN model (Gaussian in log-space) instead of regular Gaussian
- Better for AM rate tuning which spans orders of magnitude (4-128 Hz)
- AM rates are logarithmically spaced, so log-Gaussian is more appropriate
- Baseline is FIXED at pre-stimulus baseline (ground truth, not fitted)

Model:
    firing_rate = baseline + amplitude * exp(-0.5 * ((log10(rate) - log10(preferred_rate)) / sigma)^2)

Parameters:
    - baseline: Fixed at pre-stimulus baseline from metrics (Hz) - GROUND TRUTH
    - amplitude: Peak height above baseline (Hz) - FITTED
    - preferred_rate: Best AM rate (Hz) - FITTED  
    - sigma: Tuning width in log10-space - FITTED

Features:
- Fits 3 parameters (baseline fixed from pre-stimulus window, amplitude/preferred_rate/sigma fitted)
- Quality metrics: R², RMSE, goodness of fit
- Classification: good fits, poor fits, failed fits
- Saves fitted parameters and quality metrics to CSV
- Modular design: all parameters easily adjustable in FitConfig class

Author: Hylen
Date: 2025
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Tuple, Dict, List, Optional, NamedTuple
from dataclasses import dataclass
from scipy.optimize import curve_fit

from jaratoolbox import settings, celldatabase, ephyscore, spikesanalysis

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
class FitConfig:
    """
    Log-Gaussian fitting configuration - ADJUST THESE PARAMETERS TO TUNE FITTING.
    
    All fitting behavior is controlled here for easy experimentation.
    Baseline is FIXED at pre-stimulus baseline (ground truth), not fitted.
    """
    # =========================================================================
    # FITTING PARAMETERS - Adjust these to change fitting behavior
    # =========================================================================
    min_points_for_fit: int = 5  # Minimum data points required (< this = auto-fail)
    r_squared_threshold: float = 0.4  # R² cutoff: >= "good", < "poor" (relaxed for AM)
    max_iterations: int = 2000  # Max iterations for curve_fit (increase if fits fail to converge)
    
    # =========================================================================
    # LOG-GAUSSIAN PARAMETER BOUNDS - Adjust to constrain or relax fits
    # =========================================================================
    # Baseline (firing rate floor) - FIXED at pre-stimulus baseline, NOT FITTED
    allow_negative_baseline: bool = False  # Set True to allow baseline < 0 (usually keep False)
    
    # Amplitude (peak height above baseline)
    min_amplitude: float = 0.1  # Hz minimum (prevents flat fits)
    max_amplitude: Optional[float] = None  # Hz maximum (None = unbounded)
    
    # Preferred Rate (best AM rate in Hz)
    # IMPORTANT: Adjust these based on your AM rate range
    # Default assumes AM rates from 4-128 Hz (typical)
    min_preferred_rate: float = 2.0  # Hz (minimum AM rate to consider)
    max_preferred_rate: float = 256.0  # Hz (maximum AM rate to consider)
    
    # Sigma (tuning width in log10-space)
    # IMPORTANT: These control how narrow/broad tuning can be
    # In log10-space: sigma=0.3 means tuning width spans ~2x rate change
    min_sigma: float = 0.1  # log10 units (slightly relaxed from 0.05)
    max_sigma: float = 3.0  # log10 units (relaxed from 2.0 - allows very broad tuning)
    initial_sigma_guess: float = 0.5  # log10 units (broader starting guess)
    
    # =========================================================================
    # INITIAL GUESS STRATEGY - Change these to affect where fitting starts
    # =========================================================================
    use_empirical_peak_for_amplitude: bool = True  # True = use data peak, False = use mean
    use_empirical_best_rate: bool = False  # False = let optimizer find peak freely (better alignment)
    
    # Weighted fitting - emphasize peak region for better alignment
    use_weighted_fitting: bool = True  # True = weight points near peak more heavily
    peak_weight_factor: float = 1.3  # How much more to weight peak region (1.0 = no weighting, reduced from 2.0)
    
    @property
    def metrics_dir(self) -> str:
        return str(get_reports_subdir('control_group/tuning_AM_analysis'))

    @property
    def output_dir(self) -> str:
        return str(get_reports_subdir('control_group/tuning_AM_gaussian_fits'))
    
    def __post_init__(self):
        """Validate configuration."""
        assert self.min_points_for_fit >= 3, "Need at least 3 points to fit Log-Gaussian (3 params + fixed baseline)"
        assert 0 < self.r_squared_threshold <= 1, "R² threshold must be in (0, 1]"
        assert self.min_sigma > 0, "Sigma must be positive"
        assert self.max_sigma > self.min_sigma, "Max sigma must exceed min sigma"
        assert self.min_amplitude > 0, "Min amplitude must be positive"
        if self.max_amplitude is not None:
            assert self.max_amplitude > self.min_amplitude, "Max amplitude must exceed min"
        assert self.min_preferred_rate > 0, "Preferred rate must be positive"
        assert self.max_preferred_rate > self.min_preferred_rate, "Max preferred rate must exceed min"


class LogGaussianFitResult(NamedTuple):
    """Container for Log-Gaussian fit results."""
    # Fitted parameters
    baseline: float  # Floor firing rate (Hz) - FIXED
    amplitude: float  # Height above baseline (Hz)
    preferred_rate: float  # Best AM rate (Hz)
    sigma: float  # Tuning width in log10-space
    
    # Uncertainties (standard errors)
    baseline_stderr: float  # Always 0 (fixed parameter)
    amplitude_stderr: float
    preferred_rate_stderr: float
    sigma_stderr: float
    
    # Derived parameters
    peak_rate_fitted: float  # baseline + amplitude
    
    # Quality metrics
    r_squared: float
    rmse: float
    fit_quality: str  # 'good', 'poor', or 'failed'
    failure_reason: str  # Empty if fit succeeded
    
    # Empirical comparison
    empirical_best_rate: float  # Best rate from data
    empirical_peak_rate: float  # Peak firing rate from data


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
# LOG-GAUSSIAN MODEL
# =============================================================================

def log_gaussian_am_model(am_rates: np.ndarray, baseline: float, amplitude: float,
                          preferred_rate: float, sigma: float) -> np.ndarray:
    """
    Log-Gaussian AM tuning model (Gaussian in log10-space).
    
    Args:
        am_rates: AM rates (Hz)
        baseline: Floor firing rate (Hz) - FIXED
        amplitude: Peak height above baseline (Hz)
        preferred_rate: Best AM rate (Hz)
        sigma: Tuning width in log10-space
    
    Returns:
        Predicted firing rates (Hz)
    """
    log_rates = np.log10(am_rates + 1)  # +1 to handle 0 Hz gracefully
    log_preferred = np.log10(preferred_rate + 1)
    return baseline + amplitude * np.exp(-0.5 * ((log_rates - log_preferred) / sigma)**2)


# =============================================================================
# DATA LOADING MODULE
# =============================================================================

class MetricsDataLoader:
    """Loads tuning metrics CSV files."""
    
    def __init__(self, config: FitConfig):
        self.config = config
    
    def load_session_metrics(self, session_id: int, laser_condition: str) -> pd.DataFrame:
        """Load tuning metrics CSV for a session."""
        suffix = laser_condition.lower()
        csv_path = os.path.join(
            self.config.metrics_dir,
            f'session_{session_id}_laser_{suffix}_tuning_metrics.csv'
        )
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Metrics file not found: {csv_path}")
        
        return pd.read_csv(csv_path)
    
    def load_combined_baseline(self, session_id: int) -> pd.DataFrame:
        """
        Load baseline rates computed across ALL trials (both OFF and ON).
        
        This provides a shared baseline for fair comparison between conditions.
        
        Returns:
            DataFrame with cell_idx and baseline_rate_combined columns
        """
        # Try to load from OFF metrics (should have baseline_rate_prestim)
        metrics_path_off = os.path.join(
            self.config.metrics_dir,
            f'session_{session_id}_laser_off_tuning_metrics.csv'
        )
        
        if os.path.exists(metrics_path_off):
            df_off = pd.read_csv(metrics_path_off)
            # Return cell_idx and baseline (try prestim first, then regular baseline)
            if 'baseline_rate_prestim' in df_off.columns:
                return df_off[['cell_idx', 'baseline_rate_prestim']].rename(
                    columns={'baseline_rate_prestim': 'baseline_rate_combined'}
                )
            elif 'baseline_rate' in df_off.columns:
                return df_off[['cell_idx', 'baseline_rate']].rename(
                    columns={'baseline_rate': 'baseline_rate_combined'}
                )
        
        # Fallback: return empty DataFrame
        return pd.DataFrame(columns=['cell_idx', 'baseline_rate_combined'])
    
    @staticmethod
    def parse_tuning_curve(row: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """
        Parse tuning curve arrays from CSV string format.
        
        Args:
            row: DataFrame row with 'tuning_rates_am' and 'tuning_responses' columns
        
        Returns:
            Tuple of (am_rates, firing_rates) as numpy arrays
        """
        # Check if tuning columns exist
        if 'tuning_rates_am' not in row.index or 'tuning_responses' not in row.index:
            print(f"  WARNING: Tuning curve columns not found. Available columns: {list(row.index)}")
            print(f"  This likely means the metrics CSV needs to be regenerated with tuning curve data.")
            return np.array([]), np.array([])
        
        # Parse AM rates
        rate_str = str(row['tuning_rates_am'])
        if rate_str == '' or rate_str == 'nan':
            return np.array([]), np.array([])
        
        rates = np.array([float(r) for r in rate_str.split(',')])
        
        # Parse firing rates (handle 'nan' strings)
        response_str = str(row['tuning_responses'])
        if response_str == '' or response_str == 'nan':
            return rates, np.full(len(rates), np.nan)
        
        responses = []
        for r in response_str.split(','):
            if r.strip().lower() == 'nan':
                responses.append(np.nan)
            else:
                responses.append(float(r))
        responses = np.array(responses)
        
        return rates, responses


# =============================================================================
# LOG-GAUSSIAN FITTER MODULE
# =============================================================================

class LogGaussianAMFitter:
    """Fits Log-Gaussian models to AM rate tuning curves."""
    
    def __init__(self, config: FitConfig):
        self.config = config
    
    def fit_cell(
        self,
        am_rates: np.ndarray,
        firing_rates: np.ndarray,
        baseline_prestim: float,
        empirical_best_rate: float
    ) -> LogGaussianFitResult:
        """
        Fit Log-Gaussian model to a single cell's AM tuning curve.
        
        Args:
            am_rates: Array of AM rates (Hz)
            firing_rates: Array of mean firing rates (Hz)
            baseline_prestim: Pre-stimulus baseline rate (Hz) - GROUND TRUTH
            empirical_best_rate: Empirically determined best rate (Hz)
        
        Returns:
            LogGaussianFitResult with fitted parameters and quality metrics
        """
        # Remove NaN values
        valid_mask = ~np.isnan(firing_rates)
        rates_valid = am_rates[valid_mask]
        responses_valid = firing_rates[valid_mask]
        
        # Check if we have enough points
        if len(rates_valid) < self.config.min_points_for_fit:
            return self._create_failed_result(
                am_rates, firing_rates, baseline_prestim, empirical_best_rate, "insufficient_data"
            )
        
        # Initial parameter guesses
        peak_response = np.max(responses_valid)
        min_response = np.min(responses_valid)
        
        # Use configuration to determine initial guess strategy
        if self.config.use_empirical_peak_for_amplitude:
            initial_amplitude = max(peak_response - min_response, self.config.min_amplitude)
        else:
            initial_amplitude = max(np.mean(responses_valid) - min_response, self.config.min_amplitude)
        
        # Baseline is FIXED at pre-stimulus baseline (ground truth - like frequency tuning)
        baseline_fixed = max(baseline_prestim, 0.0)
        
        # Initial guess for preferred rate
        if self.config.use_empirical_best_rate:
            initial_preferred_rate = empirical_best_rate
        else:
            # Use rate at peak response
            initial_preferred_rate = rates_valid[np.argmax(responses_valid)]
        
        # Ensure initial guess is within bounds
        initial_preferred_rate = np.clip(
            initial_preferred_rate,
            self.config.min_preferred_rate,
            self.config.max_preferred_rate
        )
        
        # Initial guesses for the 3 parameters we're fitting
        p0 = [
            initial_amplitude,  # amplitude
            initial_preferred_rate,  # preferred_rate
            self.config.initial_sigma_guess  # sigma
        ]
        
        # Parameter bounds - only for the 3 fitted parameters
        amplitude_upper = self.config.max_amplitude if self.config.max_amplitude is not None else np.inf
        
        bounds = (
            [self.config.min_amplitude, self.config.min_preferred_rate, self.config.min_sigma],
            [amplitude_upper, self.config.max_preferred_rate, self.config.max_sigma]
        )
        
        # Calculate weights if weighted fitting is enabled
        if self.config.use_weighted_fitting:
            # Weight points near peak more heavily
            peak_idx = np.argmax(responses_valid)
            weights = np.ones(len(responses_valid))
            
            # Give higher weight to peak and neighboring points
            peak_range = max(1, len(responses_valid) // 4)  # Weight ~25% of points around peak
            start_idx = max(0, peak_idx - peak_range)
            end_idx = min(len(responses_valid), peak_idx + peak_range + 1)
            weights[start_idx:end_idx] = self.config.peak_weight_factor
            
            # Normalize weights
            weights = weights / np.sum(weights) * len(weights)
        else:
            weights = None
        
        # Fit Log-Gaussian with FIXED baseline
        try:
            # Create wrapper function with fixed baseline
            def log_gaussian_fixed_baseline(rates_arr, amplitude, preferred_rate, sigma):
                return log_gaussian_am_model(rates_arr, baseline_fixed, amplitude, preferred_rate, sigma)
            
            params, covariance = curve_fit(
                log_gaussian_fixed_baseline,
                rates_valid,
                responses_valid,
                p0=p0,
                bounds=bounds,
                sigma=weights if weights is not None else None,  # Use weights here
                absolute_sigma=True if weights is not None else False,
                maxfev=self.config.max_iterations
            )
            
            fit_converged = True
            
        except (RuntimeError, ValueError) as e:
            return self._create_failed_result(
                am_rates, firing_rates, baseline_prestim, empirical_best_rate, f"fit_failed: {str(e)}"
            )
        
        # Extract fitted parameters and add back the fixed baseline
        amplitude, preferred_rate, sigma = params
        baseline = baseline_fixed
        
        # Parameter uncertainties (standard errors)
        try:
            param_stderr = np.sqrt(np.diag(covariance))
            amplitude_stderr, preferred_rate_stderr, sigma_stderr = param_stderr
            baseline_stderr = 0.0  # No uncertainty - it's fixed!
        except:
            amplitude_stderr = preferred_rate_stderr = sigma_stderr = np.nan
            baseline_stderr = 0.0
        
        # Calculate derived parameters
        peak_rate_fitted = baseline + amplitude
        
        # Predict firing rates
        rates_predicted = log_gaussian_am_model(rates_valid, baseline_fixed, amplitude, preferred_rate, sigma)
        
        # Calculate quality metrics
        ss_res = np.sum((responses_valid - rates_predicted)**2)
        ss_tot = np.sum((responses_valid - np.mean(responses_valid))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        rmse = np.sqrt(np.mean((responses_valid - rates_predicted)**2))
        
        # Classify fit quality
        if r_squared >= self.config.r_squared_threshold:
            fit_quality = 'good'
        else:
            fit_quality = 'poor'
        
        # Store empirical values for comparison
        empirical_peak_rate = np.max(responses_valid)
        
        return LogGaussianFitResult(
            baseline=baseline,
            amplitude=amplitude,
            preferred_rate=preferred_rate,
            sigma=sigma,
            baseline_stderr=baseline_stderr,
            amplitude_stderr=amplitude_stderr,
            preferred_rate_stderr=preferred_rate_stderr,
            sigma_stderr=sigma_stderr,
            peak_rate_fitted=peak_rate_fitted,
            r_squared=r_squared,
            rmse=rmse,
            fit_quality=fit_quality,
            failure_reason='',
            empirical_best_rate=empirical_best_rate,
            empirical_peak_rate=empirical_peak_rate
        )
    
    def _create_failed_result(
        self,
        am_rates: np.ndarray,
        firing_rates: np.ndarray,
        baseline_prestim: float,
        empirical_best_rate: float,
        reason: str
    ) -> LogGaussianFitResult:
        """Create a failed fit result with NaN values."""
        valid_mask = ~np.isnan(firing_rates)
        empirical_peak = np.max(firing_rates[valid_mask]) if np.any(valid_mask) else np.nan
        
        return LogGaussianFitResult(
            baseline=baseline_prestim,  # Use prestim baseline even for failed fits
            amplitude=np.nan,
            preferred_rate=np.nan,
            sigma=np.nan,
            baseline_stderr=0.0,  # Fixed parameter
            amplitude_stderr=np.nan,
            preferred_rate_stderr=np.nan,
            sigma_stderr=np.nan,
            peak_rate_fitted=np.nan,
            r_squared=np.nan,
            rmse=np.nan,
            fit_quality='failed',
            failure_reason=reason,
            empirical_best_rate=empirical_best_rate,
            empirical_peak_rate=empirical_peak
        )


# =============================================================================
# SESSION FITTING COORDINATOR
# =============================================================================

class SessionFittingCoordinator:
    """Coordinates fitting for all cells in a session."""
    
    def __init__(self, config: FitConfig):
        self.config = config
        self.loader = MetricsDataLoader(config)
        self.fitter = LogGaussianAMFitter(config)
    
    def fit_session(
        self,
        session_id: int,
        session: SessionConfig,
        laser_condition: str
    ) -> pd.DataFrame:
        """
        Fit Log-Gaussian models to all cells in a session.
        
        Args:
            session_id: Session identifier
            session: Session configuration
            laser_condition: 'off' or 'on'
        
        Returns:
            DataFrame with fit results for all cells
        """
        print(f"\n{'='*70}")
        print(f"FITTING SESSION {session_id} - LASER {laser_condition.upper()}")
        print(f"{'='*70}")
        print(f"  {session.subject} {session.date} depth={session.depth}µm")
        
        # Load metrics
        df_metrics = self.loader.load_session_metrics(session_id, laser_condition)
        print(f"  Loaded {len(df_metrics)} cells from metrics file")
        
        # Load COMBINED baseline (same for both OFF and ON)
        baseline_combined_df = self.loader.load_combined_baseline(session_id)
        
        # Merge combined baseline into metrics
        if len(baseline_combined_df) > 0:
            df_metrics = df_metrics.merge(baseline_combined_df, on='cell_idx', how='left')
            print(f"  Using COMBINED baseline across all trials (OFF + ON)")
        else:
            print(f"  WARNING: Could not load combined baseline, using condition-specific baseline")
            df_metrics['baseline_rate_combined'] = df_metrics['baseline_rate']
        
        # Filter to analyzed cells only (exclude low-FR cells)
        df_analyzed = df_metrics[df_metrics['tuning_category'] != 'excluded'].copy()
        n_excluded = len(df_metrics) - len(df_analyzed)
        print(f"  Fitting {len(df_analyzed)} cells (excluded {n_excluded} cells)")
        
        # Fit each cell
        results = []
        
        for idx, row in df_analyzed.iterrows():
            cell_idx = int(row['cell_idx'])
            
            # Parse tuning curve
            am_rates, firing_rates = self.loader.parse_tuning_curve(row)
            
            if len(am_rates) == 0:
                print(f"    Cell {cell_idx}: No tuning curve data available")
                continue
            
            # Get empirical best rate and COMBINED baseline from metrics
            empirical_best_rate = row['best_rate']
            baseline_prestim = row.get('baseline_rate_combined', row['baseline_rate'])
            if np.isnan(baseline_prestim):
                baseline_prestim = row['baseline_rate']  # Fallback
            
            # Fit Log-Gaussian
            fit_result = self.fitter.fit_cell(am_rates, firing_rates, baseline_prestim, empirical_best_rate)
            
            # Convert to dict and add metadata
            result_dict = fit_result._asdict()
            result_dict['session_id'] = session_id
            result_dict['cell_idx'] = cell_idx
            result_dict['subject'] = session.subject
            result_dict['date'] = session.date
            result_dict['depth'] = session.depth
            
            results.append(result_dict)
        
        # Create DataFrame
        df_results = pd.DataFrame(results)
        
        # Print summary
        self._print_fit_summary(df_results)
        
        return df_results
    
    def _print_fit_summary(self, df: pd.DataFrame):
        """Print summary of fit quality."""
        if len(df) == 0:
            print("  No cells fitted")
            return
        
        n_good = np.sum(df['fit_quality'] == 'good')
        n_poor = np.sum(df['fit_quality'] == 'poor')
        n_failed = np.sum(df['fit_quality'] == 'failed')
        
        print(f"\n  FIT QUALITY SUMMARY:")
        print(f"  {'='*50}")
        print(f"  Good fits (R² ≥ {self.config.r_squared_threshold}): {n_good}/{len(df)} ({100*n_good/len(df):.1f}%)")
        print(f"  Poor fits (R² < {self.config.r_squared_threshold}): {n_poor}/{len(df)} ({100*n_poor/len(df):.1f}%)")
        print(f"  Failed fits: {n_failed}/{len(df)} ({100*n_failed/len(df):.1f}%)")
        
        # Show mean R² for successful fits
        successful = df[df['fit_quality'].isin(['good', 'poor'])]
        if len(successful) > 0:
            mean_r2 = successful['r_squared'].mean()
            print(f"  Mean R² (successful fits): {mean_r2:.3f}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution pipeline."""
    print("="*70)
    print("LOG-GAUSSIAN FITTING FOR AM RATE TUNING")
    print("="*70)
    
    # Initialize
    config = FitConfig()
    os.makedirs(config.output_dir, exist_ok=True)
    
    coordinator = SessionFittingCoordinator(config)
    
    # Fit all sessions
    all_results_off = []
    all_results_on = []
    
    for session_id in sorted(SESSIONS.keys()):
        session = SESSIONS[session_id]
        
        try:
            # Fit laser OFF
            df_off = coordinator.fit_session(session_id, session, 'off')
            if len(df_off) > 0:
                all_results_off.append(df_off)
                
                # Save individual session
                csv_path = os.path.join(
                    config.output_dir,
                    f'session_{session_id}_laser_off_log_gaussian_fits.csv'
                )
                df_off.to_csv(csv_path, index=False)
                print(f"  Saved to: {csv_path}")
            
            # Fit laser ON
            df_on = coordinator.fit_session(session_id, session, 'on')
            if len(df_on) > 0:
                all_results_on.append(df_on)
                
                # Save individual session
                csv_path = os.path.join(
                    config.output_dir,
                    f'session_{session_id}_laser_on_log_gaussian_fits.csv'
                )
                df_on.to_csv(csv_path, index=False)
                print(f"  Saved to: {csv_path}")
        
        except Exception as e:
            print(f"\n  ERROR fitting session {session_id}: {e}")
            import traceback
            traceback.print_exc()
    
    # Save combined results
    if len(all_results_off) > 0:
        combined_off = pd.concat(all_results_off, ignore_index=True)
        csv_path = os.path.join(config.output_dir, 'all_sessions_laser_off_log_gaussian_fits.csv')
        combined_off.to_csv(csv_path, index=False)
        print(f"\n  Saved combined OFF results: {csv_path}")
    
    if len(all_results_on) > 0:
        combined_on = pd.concat(all_results_on, ignore_index=True)
        csv_path = os.path.join(config.output_dir, 'all_sessions_laser_on_log_gaussian_fits.csv')
        combined_on.to_csv(csv_path, index=False)
        print(f"\n  Saved combined ON results: {csv_path}")
    
    print("\n" + "="*70)
    print("FITTING COMPLETE!")
    print("="*70)


if __name__ == '__main__':
    main()
