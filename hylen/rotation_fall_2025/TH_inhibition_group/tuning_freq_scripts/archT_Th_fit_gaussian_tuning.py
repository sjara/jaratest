"""
Fit Gaussian Models to Frequency Tuning Curves

This script fits Gaussian functions to frequency tuning curves and extracts
4 key parameters that describe the tuning properties:
1. Baseline: Floor firing rate (from pre-stimulus period)
2. Amplitude: Height above baseline (dynamic range)
3. Mean: Best frequency (center of tuning in octaves)
4. Sigma: Tuning width (standard deviation in octaves)

Features:
- Fits both laser OFF and laser ON conditions
- Uses pre-stimulus baseline as Gaussian floor
- Calculates fit quality (R², RMSE, chi-squared)
- Flags and separately plots failed fits (R² < 0.5)
- Compares fitted metrics to empirical metrics
- Generates comprehensive visualizations and CSV outputs

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
from scipy.optimize import curve_fit, differential_evolution
from contextlib import contextmanager
from matplotlib.gridspec import GridSpec

from jaratoolbox import settings, celldatabase, ephyscore, behavioranalysis, extraplots, spikesanalysis

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
    Gaussian fitting configuration - ADJUST THESE PARAMETERS TO TUNE FITTING.
    
    All fitting behavior is controlled here for easy experimentation.
    """
    # =========================================================================
    # FITTING PARAMETERS - Adjust these to change fitting behavior
    # =========================================================================
    min_points_for_fit: int = 5  # Minimum data points required (< this = auto-fail)
    r_squared_threshold: float = 0.5  # R² cutoff: >= "good", < "poor"
    max_iterations: int = 5000  # Max iterations for curve_fit (increased for better convergence)
    
    # =========================================================================
    # GAUSSIAN PARAMETER BOUNDS - Adjust to constrain or relax fits
    # =========================================================================
    # Baseline (firing rate floor)
    allow_negative_baseline: bool = False  # Set True to allow baseline < 0
    
    # Amplitude (peak height above baseline)
    min_amplitude: float = 0.1  # Hz minimum (prevents flat fits)
    max_amplitude: Optional[float] = None  # Hz maximum (None = unbounded)
    
    # Mean (best frequency offset in octaves)
    max_mean_offset: float = 1.5  # octaves from empirical BF (tight constraint for alignment)
    
    # Sigma (tuning width in octaves)
    min_sigma: float = 0.05  # octaves (narrowest allowed tuning) - reduced from 0.1
    max_sigma: float = 3.0  # octaves (broadest allowed tuning) - increased from 2.25
    initial_sigma_guess: float = 1.0  # octaves (starting guess for optimization)
    
    # =========================================================================
    # INITIAL GUESS STRATEGY
    # =========================================================================
    use_empirical_peak_for_amplitude: bool = True  # True = use data peak, False = use mean
    center_mean_at_empirical_bf: bool = True  # True = start at BF, False = start at 0
    
    # Weighted fitting - emphasize peak region for better alignment
    use_weighted_fitting: bool = True # True = weight points near peak more heavily
    peak_weight_factor: float = 3.0  # How much more to weight peak region (1.0 = no weighting)
    
    # Multi-start optimization - try multiple initial guesses for better alignment
    use_multi_start: bool = False  # True = try multiple starting points, pick best fit
    n_initial_guesses: int = 5  # Number of different starting points to try (reduced from 10 for speed)

    @property
    def metrics_dir(self) -> str:
        return str(get_reports_subdir('arch024/tuning_freq_analysis'))

    @property
    def output_dir(self) -> str:
        return str(get_reports_subdir('arch024/tuning_freq_gaussian_fits'))
    
    def __post_init__(self):
        """Validate configuration."""
        assert self.min_points_for_fit >= 3, "Need at least 3 points to fit Gaussian (4 params)"
        assert 0 < self.r_squared_threshold <= 1, "R² threshold must be in (0, 1]"
        assert self.min_sigma > 0, "Sigma must be positive"
        assert self.max_sigma > self.min_sigma, "Max sigma must exceed min sigma"
        assert self.min_amplitude > 0, "Min amplitude must be positive"
        if self.max_amplitude is not None:
            assert self.max_amplitude > self.min_amplitude, "Max amplitude must exceed min"


class GaussianFitResult(NamedTuple):
    """Container for Gaussian fit results."""
    # Fitted parameters
    baseline: float  # Floor firing rate (Hz)
    amplitude: float  # Height above baseline (Hz)
    mean_octave: float  # Center of Gaussian (octaves from reference)
    sigma: float  # Tuning width (standard deviation in octaves)
    
    # Uncertainties (standard errors)
    baseline_stderr: float
    amplitude_stderr: float
    mean_stderr: float
    sigma_stderr: float
    
    # Derived parameters
    peak_rate_fitted: float  # baseline + amplitude
    best_freq_fitted_hz: float  # Reference freq * 2^mean_octave
    bandwidth_fitted_octaves: float  # 2.355 * sigma (FWHM)
    
    # Fit quality
    r_squared: float
    rmse: float
    chi_squared_reduced: float
    fit_converged: bool
    fit_quality: str  # 'good', 'poor', or 'failed'
    
    # Raw data for plotting
    frequencies: np.ndarray
    firing_rates_observed: np.ndarray
    firing_rates_predicted: np.ndarray


# All available sessions (same as calculation script)
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
            print(f"  Saved to: {save_path}")
        plt.close(fig)


def safe_divide(numerator: float, denominator: float, default: float = np.nan) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    return numerator / denominator if denominator != 0 else default


# =============================================================================
# GAUSSIAN MODEL
# =============================================================================

def gaussian_tuning_model(octaves: np.ndarray, baseline: float, amplitude: float, 
                         mean_octave: float, sigma: float) -> np.ndarray:
    """
    Gaussian tuning curve model using jaratoolbox implementation.
    
    Uses spikesanalysis.gaussian(x, a, x0, sigma, y0):
        a = amplitude (height of peak)
        x0 = mean_octave (center)
        sigma = sigma (width)
        y0 = baseline (floor)
    
    Args:
        octaves: Frequency in octaves relative to reference
        baseline: Floor firing rate (Hz) - y0
        amplitude: Height of peak (Hz) - a
        mean_octave: Center of tuning (octaves) - x0
        sigma: Tuning width (octaves) - sigma
    
    Returns:
        Predicted firing rates (Hz)
    """
    return spikesanalysis.gaussian(octaves, amplitude, mean_octave, sigma, baseline)


# =============================================================================
# DATA LOADING MODULE
# =============================================================================

class MetricsDataLoader:
    """Loads pre-computed tuning metrics from CSV files."""
    
    def __init__(self, config: FitConfig):
        self.config = config
    
    def load_session_metrics(
        self,
        session_id: int,
        laser_condition: str = 'off'
    ) -> pd.DataFrame:
        """
        Load pre-computed metrics from CSV file.
        
        Returns:
            DataFrame with tuning metrics and tuning curve data
        
        Raises:
            FileNotFoundError: If metrics file doesn't exist
        """
        # Load pre-computed metrics
        suffix = laser_condition.lower()
        metrics_path = os.path.join(
            self.config.metrics_dir,
            f'session_{session_id}_laser_{suffix}_tuning_metrics.csv'
        )
        
        if not os.path.exists(metrics_path):
            raise FileNotFoundError(f"Metrics file not found: {metrics_path}")
        
        metrics_df = pd.read_csv(metrics_path)
        print(f"  Loaded {len(metrics_df)} cells from metrics file")
        
        return metrics_df
    
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
            # Return cell_idx and baseline
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
            row: DataFrame row with 'tuning_freqs' and 'tuning_rates' columns
        
        Returns:
            Tuple of (frequencies, firing_rates) as numpy arrays
        """
        # Parse frequencies
        freq_str = str(row['tuning_freqs'])
        if freq_str == '' or freq_str == 'nan':
            return np.array([]), np.array([])
        
        freqs = np.array([float(f) for f in freq_str.split(',')])
        
        # Parse firing rates (handle 'nan' strings)
        rate_str = str(row['tuning_rates'])
        if rate_str == '' or rate_str == 'nan':
            return freqs, np.full(len(freqs), np.nan)
        
        rates = []
        for r in rate_str.split(','):
            if r.strip().lower() == 'nan':
                rates.append(np.nan)
            else:
                rates.append(float(r))
        rates = np.array(rates)
        
        return freqs, rates


# =============================================================================
# GAUSSIAN FITTER MODULE
# =============================================================================

class GaussianTuningFitter:
    """Fits Gaussian models to frequency tuning curves."""
    
    def __init__(self, config: FitConfig):
        self.config = config
    
    def fit_cell(
        self,
        frequencies: np.ndarray,
        firing_rates: np.ndarray,
        baseline_prestim: float,
        best_freq_empirical: float
    ) -> GaussianFitResult:
        """
        Fit Gaussian model to a single cell's tuning curve.
        
        Args:
            frequencies: Array of stimulus frequencies (Hz)
            firing_rates: Array of mean firing rates (Hz)
            baseline_prestim: Pre-stimulus baseline rate (Hz)
            best_freq_empirical: Empirically determined best frequency (Hz)
        
        Returns:
            GaussianFitResult with fitted parameters and quality metrics
        """
        # Remove NaN values
        valid_mask = ~np.isnan(firing_rates)
        freqs_valid = frequencies[valid_mask]
        rates_valid = firing_rates[valid_mask]
        
        # Check if we have enough points
        if len(freqs_valid) < self.config.min_points_for_fit:
            return self._create_failed_result(
                frequencies, firing_rates, "insufficient_data"
            )
        
        # Convert to octaves relative to empirical best frequency
        octaves = np.log2(freqs_valid / best_freq_empirical)
        
        # Initial parameter guesses
        peak_rate = np.max(rates_valid)
        min_rate = np.min(rates_valid)
        
        # Use configuration to determine initial guess strategy
        if self.config.use_empirical_peak_for_amplitude:
            initial_amplitude = max(peak_rate - min_rate, self.config.min_amplitude)
        else:
            initial_amplitude = max(np.mean(rates_valid) - min_rate, self.config.min_amplitude)
        
        # Use the COMBINED baseline (passed in as parameter) - this is the ground truth
        # DO NOT use min_rate - that's condition-specific!
        baseline_fixed = baseline_prestim  # This is already the combined baseline from all trials
        
        # Find the observed peak location for better initial guess
        peak_idx = np.argmax(rates_valid)
        peak_freq_hz = freqs_valid[peak_idx]
        peak_octave_observed = np.log2(peak_freq_hz / best_freq_empirical)
        
        # Start at the observed peak instead of empirical BF (0.0)
        initial_mean = peak_octave_observed  # Use observed peak location
        
        # Parameter bounds - only for the 3 fitted parameters
        amplitude_upper = self.config.max_amplitude if self.config.max_amplitude is not None else np.inf
        
        # CRITICAL: Use looser constraint when reference is OFF BF (allows detection of true shifts)
        # The observed peak might be far from the reference (OFF BF) if tuning shifted
        if abs(peak_octave_observed) > 0.5:
            # Observed peak is far from reference - allow wide search
            mean_bound = 1.5  # Allow ±1.5 octaves to capture real shifts
        else:
            # Observed peak is near reference - use tighter constraint
            mean_bound = 0.5  # Allow ±0.5 octaves for alignment
        
        bounds = (
            [self.config.min_amplitude, -mean_bound, self.config.min_sigma],
            [amplitude_upper, mean_bound, self.config.max_sigma]
        )
        
        # Calculate weights if weighted fitting is enabled
        if self.config.use_weighted_fitting:
            # Weight points near peak more heavily
            peak_idx = np.argmax(rates_valid)
            weights = np.ones(len(rates_valid))
            
            # Give higher weight to peak and neighboring points
            peak_range = max(1, len(rates_valid) // 4)  # Weight ~25% of points around peak
            start_idx = max(0, peak_idx - peak_range)
            end_idx = min(len(rates_valid), peak_idx + peak_range + 1)
            weights[start_idx:end_idx] = self.config.peak_weight_factor
            
            # Normalize weights
            weights = weights / np.sum(weights) * len(weights)
        else:
            weights = None
        
        # Multi-start optimization: Use differential evolution for global search
        if self.config.use_multi_start:
            # Create wrapper function for optimization
            def gaussian_fixed_baseline(octaves_arr, amplitude, mean_oct, sigma):
                return gaussian_tuning_model(octaves_arr, baseline_fixed, amplitude, mean_oct, sigma)
            
            # Use differential evolution for robust global optimization
            def objective(params):
                amplitude, mean_oct, sigma = params
                rates_pred = gaussian_fixed_baseline(octaves, amplitude, mean_oct, sigma)
                # Minimize negative R² (maximize R²)
                r_sq = self._calculate_r_squared(rates_valid, rates_pred)
                return -r_sq  # Negative because we're minimizing
            
            # Run global optimization
            result = differential_evolution(
                objective,
                bounds=[(bounds[0][0], bounds[1][0]),  # amplitude
                       (bounds[0][1], bounds[1][1]),  # mean_octave
                       (bounds[0][2], bounds[1][2])],  # sigma
                seed=42,
                maxiter=1000,
                atol=1e-4,
                tol=1e-4,
                workers=1
            )
            
            if result.success:
                params = result.x
                fit_converged = True
                
                # Calculate covariance using curve_fit at the found solution
                try:
                    params_refined, covariance = curve_fit(
                        gaussian_fixed_baseline,
                        octaves,
                        rates_valid,
                        p0=params,
                        bounds=bounds,
                        maxfev=1000
                    )
                    params = params_refined  # Use refined parameters
                except:
                    # If refinement fails, use DE result with no covariance
                    covariance = np.diag([np.nan, np.nan, np.nan])
            else:
                return self._create_failed_result(
                    frequencies, firing_rates, "differential_evolution_failed"
                )
        
        else:
            # Single attempt (original behavior)
            p0 = [initial_amplitude, initial_mean, self.config.initial_sigma_guess]
            
            try:
                # Create wrapper function with fixed baseline
                def gaussian_fixed_baseline(octaves_arr, amplitude, mean_oct, sigma):
                    return gaussian_tuning_model(octaves_arr, baseline_fixed, amplitude, mean_oct, sigma)
                
                params, covariance = curve_fit(
                    gaussian_fixed_baseline,
                    octaves,
                    rates_valid,
                    p0=p0,
                    bounds=bounds,
                    sigma=weights if weights is not None else None,
                    absolute_sigma=True if weights is not None else False,
                    maxfev=self.config.max_iterations
                )
                
                fit_converged = True
                
            except (RuntimeError, ValueError) as e:
                return self._create_failed_result(
                    frequencies, firing_rates, f"fit_failed: {str(e)}"
                )
        
        # Extract fitted parameters and add back the fixed baseline
        amplitude, mean_octave, sigma = params
        baseline = baseline_fixed  # Use the fixed ground truth value
        
        # Parameter uncertainties (standard errors) - baseline has no uncertainty since it's fixed
        try:
            param_stderr = np.sqrt(np.diag(covariance))
            amplitude_stderr, mean_stderr, sigma_stderr = param_stderr
            baseline_stderr = 0.0  # No uncertainty - it's fixed!
        except:
            amplitude_stderr = mean_stderr = sigma_stderr = np.nan
            baseline_stderr = 0.0
        
        # Calculate derived parameters
        peak_rate_fitted = baseline + amplitude
        
        # Calculate fitted best frequency: The peak of the Gaussian is at mean_octave
        # relative to the empirical best frequency (which was used as reference)
        best_freq_fitted_hz = best_freq_empirical * (2 ** mean_octave)
        
        # ALTERNATIVE: Find the actual peak by evaluating the Gaussian
        # Create a fine grid of frequencies and find the maximum
        freq_range = freqs_valid.min(), freqs_valid.max()
        freq_grid = np.linspace(freq_range[0], freq_range[1], 1000)
        octave_grid = np.log2(freq_grid / best_freq_empirical)
        rates_grid = gaussian_tuning_model(octave_grid, baseline, amplitude, mean_octave, sigma)
        best_freq_fitted_hz = freq_grid[np.argmax(rates_grid)]
        
        bandwidth_fitted_octaves = 2.355 * sigma  # FWHM = 2.355 * sigma for Gaussian
        
        # Predict firing rates
        rates_predicted = gaussian_tuning_model(octaves, baseline_fixed, amplitude, mean_octave, sigma)
        
        # Calculate fit quality
        r_squared = self._calculate_r_squared(rates_valid, rates_predicted)
        rmse = np.sqrt(np.mean((rates_valid - rates_predicted) ** 2))
        
        # Chi-squared (reduced)
        n_params = 4
        dof = len(rates_valid) - n_params
        if dof > 0:
            residuals = rates_valid - rates_predicted
            chi_squared_reduced = np.sum(residuals ** 2) / dof
        else:
            chi_squared_reduced = np.nan
        
        # Classify fit quality
        if r_squared >= self.config.r_squared_threshold:
            fit_quality = 'good'
        else:
            fit_quality = 'poor'
        
        # Convert back to original frequency space for storage
        freqs_full = frequencies.copy()
        rates_observed_full = firing_rates.copy()
        rates_predicted_full = np.full_like(firing_rates, np.nan)
        rates_predicted_full[valid_mask] = rates_predicted
        
        return GaussianFitResult(
            baseline=baseline,
            amplitude=amplitude,
            mean_octave=mean_octave,
            sigma=sigma,
            baseline_stderr=baseline_stderr,
            amplitude_stderr=amplitude_stderr,
            mean_stderr=mean_stderr,
            sigma_stderr=sigma_stderr,
            peak_rate_fitted=peak_rate_fitted,
            best_freq_fitted_hz=best_freq_fitted_hz,
            bandwidth_fitted_octaves=bandwidth_fitted_octaves,
            r_squared=r_squared,
            rmse=rmse,
            chi_squared_reduced=chi_squared_reduced,
            fit_converged=fit_converged,
            fit_quality=fit_quality,
            frequencies=freqs_full,
            firing_rates_observed=rates_observed_full,
            firing_rates_predicted=rates_predicted_full
        )
    
    @staticmethod
    def _calculate_r_squared(observed: np.ndarray, predicted: np.ndarray) -> float:
        """Calculate coefficient of determination (R²)."""
        ss_res = np.sum((observed - predicted) ** 2)
        ss_tot = np.sum((observed - np.mean(observed)) ** 2)
        if ss_tot == 0:
            return np.nan
        return 1 - (ss_res / ss_tot)
    
    def _create_failed_result(
        self,
        frequencies: np.ndarray,
        firing_rates: np.ndarray,
        reason: str
    ) -> GaussianFitResult:
        """Create a failed fit result with NaN values."""
        return GaussianFitResult(
            baseline=np.nan,
            amplitude=np.nan,
            mean_octave=np.nan,
            sigma=np.nan,
            baseline_stderr=np.nan,
            amplitude_stderr=np.nan,
            mean_stderr=np.nan,
            sigma_stderr=np.nan,
            peak_rate_fitted=np.nan,
            best_freq_fitted_hz=np.nan,
            bandwidth_fitted_octaves=np.nan,
            r_squared=np.nan,
            rmse=np.nan,
            chi_squared_reduced=np.nan,
            fit_converged=False,
            fit_quality='failed',
            frequencies=frequencies,
            firing_rates_observed=firing_rates,
            firing_rates_predicted=np.full_like(firing_rates, np.nan)
        )

# =============================================================================
# SESSION COORDINATOR
# =============================================================================

class SessionFitCoordinator:
    """Coordinates Gaussian fitting for a session."""
    
    def __init__(
        self,
        fit_config: FitConfig,
        loader: MetricsDataLoader,
        fitter: GaussianTuningFitter
    ):
        self.config = fit_config
        self.loader = loader
        self.fitter = fitter
        # Cache fitted results for combined plotting
        self._session_fits_cache = {}
    
    def fit_session(
        self,
        session_id: int,
        session: SessionConfig,
        laser_condition: str = 'off'
    ) -> pd.DataFrame:
        """
        Fit Gaussian models to all cells in a session.
        
        Returns:
            DataFrame with fit results
        """
        print(f"\n{'='*60}")
        print(f"SESSION {session_id}: {session.subject} {session.date} depth={session.depth}um")
        print(f"LASER {laser_condition.upper()}")
        print(f"{'='*60}")
        
        # Load pre-computed metrics from CSV
        metrics_df = self.loader.load_session_metrics(session_id, laser_condition)
        
        # Load COMBINED baseline (same for both OFF and ON)
        baseline_combined_df = self.loader.load_combined_baseline(session_id)
        
        # Merge combined baseline into metrics
        if len(baseline_combined_df) > 0:
            metrics_df = metrics_df.merge(baseline_combined_df, on='cell_idx', how='left')
            print(f"  Using COMBINED baseline across all trials (OFF + ON)")
        else:
            print(f"  WARNING: Could not load combined baseline, using condition-specific baseline")
            metrics_df['baseline_rate_combined'] = metrics_df['baseline_rate_prestim']
        
        # CRITICAL FIX: For laser ON, load OFF best frequencies to use as reference
        # This ensures both OFF and ON fits are aligned to the same coordinate system
        if laser_condition == 'on':
            print(f"  Loading OFF best frequencies for alignment reference...")
            try:
                metrics_off = self.loader.load_session_metrics(session_id, 'off')
                # Extract only cell_idx and best_freq from OFF
                off_bf_df = metrics_off[['cell_idx', 'best_freq']].rename(
                    columns={'best_freq': 'best_freq_off_reference'}
                )
                # Merge into ON metrics
                metrics_df = metrics_df.merge(off_bf_df, on='cell_idx', how='left')
                print(f"  Successfully loaded OFF best frequencies for {len(off_bf_df)} cells")
            except Exception as e:
                print(f"  WARNING: Could not load OFF best frequencies: {e}")
                print(f"  Falling back to ON best frequencies (fits may be misaligned)")
                metrics_df['best_freq_off_reference'] = metrics_df['best_freq']
        else:
            # For OFF condition, use its own best frequency
            metrics_df['best_freq_off_reference'] = metrics_df['best_freq']
        
        # Filter to non-excluded cells
        fitting_df = metrics_df[~metrics_df['is_excluded']].copy()
        
        print(f"  Fitting {len(fitting_df)} cells (excluded {np.sum(metrics_df['is_excluded'])} cells)")
        
        # Fit each cell
        fit_results = []
        fit_results_for_plotting = []
        
        for _, row in fitting_df.iterrows():
            cell_idx = int(row['cell_idx'])
            
            # Parse tuning curve from CSV strings
            frequencies, firing_rates = self.loader.parse_tuning_curve(row)
            
            if len(frequencies) == 0:
                print(f"  WARNING: Cell {cell_idx} has no tuning curve data, skipping")
                continue
            
            # Get COMBINED baseline (same for both OFF and ON)
            baseline_prestim = row.get('baseline_rate_combined', row['baseline_rate_prestim'])
            if np.isnan(baseline_prestim):
                baseline_prestim = row['baseline_rate']  # Fallback to empirical baseline
            
            # CRITICAL: Use OFF best frequency as reference for BOTH conditions
            best_freq_reference = row['best_freq_off_reference']
            
            # Also store the condition-specific empirical BF for comparison
            best_freq_empirical_this_condition = row['best_freq']
            
            # Fit Gaussian using OFF BF as reference
            fit_result = self.fitter.fit_cell(
                frequencies, firing_rates, baseline_prestim, best_freq_reference
            )
            
            # Store for plotting
            fit_results_for_plotting.append((cell_idx, fit_result, best_freq_reference))
            
            # Convert to dict for DataFrame
            fit_dict = {
                'session_id': session_id,
                'cell_idx': cell_idx,
                'subject': session.subject,
                'date': session.date,
                'depth': session.depth,
                **self._fit_result_to_dict(fit_result),
                # Add empirical metrics for comparison
                'empirical_best_freq': best_freq_empirical_this_condition,  # Condition-specific BF
                'best_freq_reference': best_freq_reference,  # OFF BF used for fitting
                'empirical_peak_rate': row['peak_rate'],
                'empirical_bandwidth_octaves': row['bandwidth_octaves'],
                'empirical_tuning_quality': row['tuning_quality'],
                'empirical_is_tuned': row['is_tuned'],
                'empirical_tuning_category': row['tuning_category']
            }
            
            fit_results.append(fit_dict)
        
        # Create DataFrame
        fit_df = pd.DataFrame(fit_results)
        
        # Print summary
        self._print_fit_summary(fit_df)
        
        # Save CSV
        suffix = laser_condition.lower()
        csv_path = os.path.join(
            self.config.output_dir,
            f'session_{session_id}_laser_{suffix}_gaussian_fits.csv'
        )
        fit_df.to_csv(csv_path, index=False)
        print(f"\n  Saved fit results: {csv_path}")
        
        # Store results for combined plotting across all sessions
        cache_key = (session_id, laser_condition)
        self._session_fits_cache[cache_key] = (fit_results_for_plotting, fitting_df)
        
        return fit_df
    
    def create_combined_category_pdfs(self):
        """
        Create 4 PDFs across all sessions organized by tuning category:
        1. Good fits (tuned cells with good Gaussian fit)
        2. Poor fits (not-tuned cells)
        3. Failed fits (cells where fitting failed)
        4. All empirically tuned cells (regardless of fit quality)
        """
        print(f"\n{'='*70}")
        print("CREATING CATEGORY-BASED PDFs ACROSS ALL SESSIONS")
        print(f"{'='*70}")
        
        # Collect all cells from both OFF and ON, organized by category
        good_fits = []  # Good Gaussian fits
        poor_fits = []  # Poor Gaussian fits
        failed_fits = []  # Failed to fit
        all_tuned = []  # All empirically tuned cells (from calculation script)
        
        # Match cells across OFF and ON
        for (session_id, laser_cond), (fit_results, metrics_df) in self._session_fits_cache.items():
            if (session_id, 'on') not in self._session_fits_cache:
                continue
            
            fit_results_on, metrics_df_on = self._session_fits_cache[(session_id, 'on')]
            
            # Create lookup dictionaries
            cells_off = {cell_idx: (fit_res, bf) for cell_idx, fit_res, bf in fit_results}
            cells_on = {cell_idx: (fit_res, bf) for cell_idx, fit_res, bf in fit_results_on}
            metrics_off_dict = {row['cell_idx']: row for _, row in metrics_df.iterrows()}
            metrics_on_dict = {row['cell_idx']: row for _, row in metrics_df_on.iterrows()}
            
            # Find common cells
            common_cells = sorted(set(cells_off.keys()) & set(cells_on.keys()))
            
            session = SESSIONS[session_id]
            
            for cell_idx in common_cells:
                fit_off, bf_off = cells_off[cell_idx]
                fit_on, bf_on = cells_on[cell_idx]
                metrics_off = metrics_off_dict.get(cell_idx)
                metrics_on = metrics_on_dict.get(cell_idx)
                
                if metrics_off is None or metrics_on is None:
                    continue
                
                cell_data = (session_id, session, cell_idx, 
                           fit_off, fit_on, bf_off, bf_on,
                           metrics_off, metrics_on)
                
                # Categorize based on fit quality AND empirical tuning
                empirically_tuned = metrics_off.get('is_tuned', False)
                
                # Category 1: Good fits (well-fit Gaussians)
                if fit_off.fit_quality == 'good' and fit_on.fit_quality == 'good':
                    good_fits.append(cell_data)
                
                # Category 2: Poor fits (both converged but R² < threshold)
                elif (fit_off.fit_quality == 'poor' and fit_on.fit_quality == 'poor'):
                    poor_fits.append(cell_data)
                
                # Category 3: Failed fits (at least one didn't converge)
                elif fit_off.fit_quality == 'failed' or fit_on.fit_quality == 'failed':
                    failed_fits.append(cell_data)
                
                # Also collect for Category 4: All empirically tuned
                if empirically_tuned:
                    all_tuned.append(cell_data)
        
        # Create PDFs for each category
        self._create_category_pdf(good_fits, 'good_fits', 
                                  'Good Gaussian Fits (Tuned Cells)')
        self._create_category_pdf(poor_fits, 'poor_fits',
                                  'Poor Gaussian Fits (Not-Tuned Cells)')
        self._create_category_pdf(failed_fits, 'failed_fits',
                                  'Failed Gaussian Fits (Fitting Problems)')
        self._create_category_pdf(all_tuned, 'all_empirically_tuned',
                                  'All Empirically Tuned Cells (Any Fit Quality)')
    
    def _create_category_pdf(self, cell_data_list, filename_suffix, title):
        """Helper to create a single category PDF."""
        if len(cell_data_list) == 0:
            print(f"  No cells for category: {title}")
            return
        
        filename = f'all_sessions_gaussian_fits_{filename_suffix}.pdf'
        pdf_path = os.path.join(self.config.output_dir, filename)
        
        print(f"\n  Creating {title} PDF with {len(cell_data_list)} cells...")
        
        with PdfPages(pdf_path) as pdf:
            # Plot 4 cells per page
            n_cells_per_page = 4
            n_pages = int(np.ceil(len(cell_data_list) / n_cells_per_page))
            
            for page_idx in range(n_pages):
                fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                axes = axes.flatten()
                
                start_idx = page_idx * n_cells_per_page
                end_idx = min(start_idx + n_cells_per_page, len(cell_data_list))
                
                for plot_idx in range(start_idx, end_idx):
                    session_id, session, cell_idx, fit_off, fit_on, bf_off, bf_on, metrics_off, metrics_on = cell_data_list[plot_idx]
                    
                    self.plotter.plot_combined_fit(
                        axes[plot_idx - start_idx],
                        fit_off, fit_on,
                        cell_idx, bf_off, bf_on,
                        session_id
                    )
                
                # Hide unused subplots
                for plot_idx in range(end_idx - start_idx, n_cells_per_page):
                    axes[plot_idx].axis('off')
                
                # Page title
                fig.suptitle(
                    f'{title}\n'
                    f'Page {page_idx + 1}/{n_pages} | Total Cells: {len(cell_data_list)}',
                    fontsize=13, fontweight='bold'
                )
                
                plt.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig, dpi=150)
                plt.close(fig)
        
        print(f"  Saved: {pdf_path}")
    
    @staticmethod
    def _fit_result_to_dict(fit_result: GaussianFitResult) -> dict:
        """Convert GaussianFitResult to dictionary (exclude raw arrays)."""
        return {
            'baseline': fit_result.baseline,
            'amplitude': fit_result.amplitude,
            'mean_octave': fit_result.mean_octave,
            'sigma': fit_result.sigma,
            'baseline_stderr': fit_result.baseline_stderr,
            'amplitude_stderr': fit_result.amplitude_stderr,
            'mean_stderr': fit_result.mean_stderr,
            'sigma_stderr': fit_result.sigma_stderr,
            'peak_rate_fitted': fit_result.peak_rate_fitted,
            'best_freq_fitted_hz': fit_result.best_freq_fitted_hz,
            'bandwidth_fitted_octaves': fit_result.bandwidth_fitted_octaves,
            'r_squared': fit_result.r_squared,
            'rmse': fit_result.rmse,
            'chi_squared_reduced': fit_result.chi_squared_reduced,
            'fit_converged': fit_result.fit_converged,
            'fit_quality': fit_result.fit_quality
        }
    
    def _print_fit_summary(self, fit_df: pd.DataFrame):
        """Print summary of fit quality."""
        print(f"\n  FIT QUALITY SUMMARY:")
        print(f"  {'='*50}")
        
        n_good = np.sum(fit_df['fit_quality'] == 'good')
        n_poor = np.sum(fit_df['fit_quality'] == 'poor')
        n_failed = np.sum(fit_df['fit_quality'] == 'failed')
        n_total = len(fit_df)
        
        print(f"  Good fits (R² ≥ {self.config.r_squared_threshold}): {n_good}/{n_total} ({100*n_good/n_total:.1f}%)")
        print(f"  Poor fits (R² < {self.config.r_squared_threshold}): {n_poor}/{n_total} ({100*n_poor/n_total:.1f}%)")
        print(f"  Failed fits: {n_failed}/{n_total} ({100*n_failed/n_total:.1f}%)")
        
        # Summary statistics of good fits
        good_fits = fit_df[fit_df['fit_quality'] == 'good']
        if len(good_fits) > 0:
            print(f"\n  GOOD FITS - Parameter Statistics:")
            print(f"  Baseline:  {good_fits['baseline'].mean():.2f} ± {good_fits['baseline'].std():.2f} Hz")
            print(f"  Amplitude: {good_fits['amplitude'].mean():.2f} ± {good_fits['amplitude'].std():.2f} Hz")
            print(f"  Sigma:     {good_fits['sigma'].mean():.2f} ± {good_fits['sigma'].std():.2f} octaves")
            print(f"  R²:        {good_fits['r_squared'].mean():.3f} ± {good_fits['r_squared'].std():.3f}")
            print(f"  RMSE:      {good_fits['rmse'].mean():.2f} ± {good_fits['rmse'].std():.2f} Hz")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution pipeline."""
    print("="*60)
    print("GAUSSIAN TUNING CURVE FITTING - ALL SESSIONS")
    print("="*60)
    
    # Initialize configuration
    fit_config = FitConfig()
    os.makedirs(fit_config.output_dir, exist_ok=True)
    print(f"\nOutput directory: {fit_config.output_dir}")
    print(f"Reading metrics from: {fit_config.metrics_dir}")
    
    # Initialize components
    loader = MetricsDataLoader(fit_config)
    fitter = GaussianTuningFitter(fit_config)
    coordinator = SessionFitCoordinator(fit_config, loader, fitter)
    
    # Fit all sessions for both laser conditions
    all_fits_off = []
    all_fits_on = []
    
    for session_id in sorted(SESSIONS.keys()):
        session = SESSIONS[session_id]
        
        try:
            # Fit laser OFF
            fit_df_off = coordinator.fit_session(session_id, session, 'off')
            all_fits_off.append(fit_df_off)
            
        except FileNotFoundError as e:
            print(f"\n  SKIPPING session {session_id} (laser OFF): Metrics not found")
            print(f"  {e}")
        except Exception as e:
            print(f"\n  ERROR fitting session {session_id} (laser OFF): {e}")
            import traceback
            traceback.print_exc()
        
        try:
            # Fit laser ON
            fit_df_on = coordinator.fit_session(session_id, session, 'on')
            all_fits_on.append(fit_df_on)
            
        except FileNotFoundError as e:
            print(f"\n  SKIPPING session {session_id} (laser ON): Metrics not found")
            print(f"  {e}")
        except Exception as e:
            print(f"\n  ERROR fitting session {session_id} (laser ON): {e}")
            import traceback
            traceback.print_exc()
    
    # Save combined results
    for fits_list, laser_label in [(all_fits_off, 'off'), (all_fits_on, 'on')]:
        if len(fits_list) > 0:
            combined_df = pd.concat(fits_list, ignore_index=True)
            csv_path = os.path.join(
                fit_config.output_dir,
                f'all_sessions_laser_{laser_label}_gaussian_fits.csv'
            )
            combined_df.to_csv(csv_path, index=False)
            print(f"\nSaved combined LASER {laser_label.upper()} fits: {csv_path}")
            
            # Print overall summary
            print(f"\nOVERALL SUMMARY - LASER {laser_label.upper()}:")
            print(f"{'='*60}")
            print(f"Total cells fitted: {len(combined_df)}")
            n_good = np.sum(combined_df['fit_quality'] == 'good')
            n_poor = np.sum(combined_df['fit_quality'] == 'poor')
            n_failed = np.sum(combined_df['fit_quality'] == 'failed')
            print(f"  Good fits: {n_good} ({100*n_good/len(combined_df):.1f}%)")
            print(f"  Poor fits: {n_poor} ({100*n_poor/len(combined_df):.1f}%)")
            print(f"  Failed fits: {n_failed} ({100*n_failed/len(combined_df):.1f}%)")
    
    print(f"\n{'='*60}")
    print("GAUSSIAN FITTING COMPLETE!")
    print(f"{'='*60}")
    print(f"Results saved to: {fit_config.output_dir}")
    print(f"\nNext step: Run archT_AC_plot_gaussian_fits_with_rasters.py to visualize results")


if __name__ == '__main__':
    main()
