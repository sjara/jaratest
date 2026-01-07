"""
Calculate Amplitude Modulation (AM) tuning quality metrics for neural recordings.

This script analyzes AM rate tuning quality for both laser OFF and laser ON conditions,
computing metrics such as selectivity index, sparseness, and bandwidth for each cell.

Key differences from frequency tuning:
- Analyzes AM rate tuning (modulation depth at different rates)
- Uses longer response window (5-495ms) to capture full modulation cycles
- AM rates typically range from 4-128 Hz

Features:
- Analyzes multiple recording sessions across different subjects, dates, and depths
- Computes metrics for BOTH laser OFF and laser ON trials without reloading data
- Loads cell databases once per subject for efficiency
- Quality control based on minimum firing rate threshold
- Generates comprehensive plots and CSV files for downstream analysis

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
from matplotlib.figure import Figure
from contextlib import contextmanager

from jaratoolbox import settings, celldatabase, ephyscore, spikesanalysis

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
    """Analysis parameters configuration (immutable)."""
    time_range: Tuple[float, float] = (-0.5, 1.0)
    baseline_window: Tuple[float, float] = (-0.495, -0.005)  # Pre-stimulus baseline
    response_window: Tuple[float, float] = (0.005, 0.495)  # Exclude laser artifact
    min_detection_threshold: float = 0.2  # Hz - minimum to detect cell is alive
    min_analysis_threshold: float = 2.0   # Hz - minimum for reliable tuning analysis
    tuning_quality_threshold: float = 0.15  # Minimum tuning quality score (>= 0.15 passes)
    min_modulation_threshold: float = 0.20  # Minimum 20% increase from baseline to be tuned (>= 0.20 passes)
    
    # Use centralized config for directories
    @property
    def output_dir(self) -> str:
        """Get output directory from config."""
        return str(get_reports_subdir('tuning_AM_analysis'))
    
    @property
    def override_file(self) -> str:
        """Get override file path from config."""
        return os.path.join(self.output_dir, 'classification_overrides.csv')
    
    def __post_init__(self):
        """Validate configuration parameters."""
        assert self.time_range[0] < self.time_range[1], "Invalid time_range"
        assert self.baseline_window[0] < self.baseline_window[1], "Invalid baseline_window"
        assert self.response_window[0] < self.response_window[1], "Invalid response_window"
        assert self.baseline_window[1] <= 0, "Baseline window must be before stimulus onset"
        assert self.response_window[0] >= 0, "Response window must be after stimulus onset"
        assert self.min_detection_threshold > 0, "Detection threshold must be positive"
        assert self.min_analysis_threshold >= self.min_detection_threshold, \
            "Analysis threshold must be >= detection threshold"
        assert self.tuning_quality_threshold > 0, "Tuning quality threshold must be positive"
        assert 0 < self.min_modulation_threshold < 5, "Modulation threshold must be between 0 and 5"


class TuningMetrics(NamedTuple):
    """Container for AM tuning curve metrics."""
    best_rate: float  # Best AM rate (Hz)
    peak_response: float  # Peak firing rate (Hz)
    baseline_rate: float  # Baseline firing rate during pre-stimulus window (Hz)
    mean_response: float  # Mean firing rate across all AM rates (Hz)
    dynamic_range: float  # Peak - minimum
    baseline_subtracted_peak: float  # Peak response - baseline rate
    baseline_subtracted_mean: float  # Mean response - baseline rate
    selectivity_index: float
    sparseness: float
    bandwidth_hz: float
    bandwidth_octaves: float
    q_factor: float
    tuning_quality: float
    fano_factor: float  # Trial-to-trial variability (variance/mean of spike counts)


class SessionData(NamedTuple):
    """Container for loaded session data."""
    celldb: pd.DataFrame
    ephys_data: dict
    bdata: dict
    ensemble: ephyscore.CellEnsemble


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
            print(f"  Saved to: {save_path}")
        plt.close(fig)


def safe_divide(numerator: float, denominator: float, default: float = np.nan) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    return numerator / denominator if denominator != 0 else default


def get_unique_subjects(sessions: Dict[int, SessionConfig]) -> List[str]:
    """Extract unique subject names from session configurations."""
    return list(set(session.subject for session in sessions.values()))


# =============================================================================
# CLASSIFICATION OVERRIDE MODULE
# =============================================================================

class ClassificationOverrideManager:
    """
    Manages manual overrides for cell tuning classifications.
    
    Allows researchers to manually override automatic classifications for cells
    that are false positives (auto-classified as tuned but actually non-tuned)
    or false negatives (auto-classified as non-tuned but actually tuned).
    
    Override file format (CSV):
        session_id,cell_idx,override_category,reason,notes
        0,42,tuned,clear_peak,Visual inspection shows clear tuning
        1,15,non_tuned,noise,Too noisy despite passing auto criteria
        2,88,excluded,artifact,Electrode artifact contamination
    
    Valid override_category values:
        - 'tuned': Force classification as tuned
        - 'non_tuned': Force classification as non-tuned
        - 'excluded': Force exclusion (ignore in analysis)
    """
    
    def __init__(self, override_file: str):
        self.override_file = override_file
        self.overrides: Dict[Tuple[int, int], Dict[str, str]] = {}
        self._load_overrides()
    
    def _load_overrides(self):
        """Load overrides from CSV file."""
        if not os.path.exists(self.override_file):
            print(f"\n  No override file found at: {self.override_file}")
            print(f"  To create overrides, create a CSV file with columns:")
            print(f"    session_id,cell_idx,override_category,reason,notes")
            self._create_template()
            return
        
        try:
            df = pd.read_csv(self.override_file)
            
            # Validate required columns
            required_cols = ['session_id', 'cell_idx', 'override_category']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"  WARNING: Override file missing columns: {missing_cols}")
                return
            
            # Load overrides
            for _, row in df.iterrows():
                key = (int(row['session_id']), int(row['cell_idx']))
                self.overrides[key] = {
                    'category': str(row['override_category']).lower(),
                    'reason': str(row.get('reason', '')),
                    'notes': str(row.get('notes', ''))
                }
            
            if len(self.overrides) > 0:
                print(f"\n  ✓ Loaded {len(self.overrides)} classification overrides from:")
                print(f"    {self.override_file}")
                self._print_override_summary()
            
        except Exception as e:
            print(f"  WARNING: Failed to load overrides: {e}")
    
    def _create_template(self):
        """Create a template override file if it doesn't exist."""
        template_data = {
            'session_id': [0, 1],
            'cell_idx': [42, 15],
            'override_category': ['tuned', 'non_tuned'],
            'reason': ['clear_peak_visual_inspection', 'too_noisy'],
            'notes': ['Example: Force tuned despite auto-classification', 
                     'Example: Force non-tuned due to noise']
        }
        
        template_df = pd.DataFrame(template_data)
        template_path = self.override_file.replace('.csv', '_TEMPLATE.csv')
        
        try:
            template_df.to_csv(template_path, index=False)
            print(f"  Created template override file at: {template_path}")
            print(f"  Edit this file and rename to: {os.path.basename(self.override_file)}")
        except Exception as e:
            print(f"  Could not create template: {e}")
    
    def _print_override_summary(self):
        """Print summary of loaded overrides."""
        by_category = {}
        for override_data in self.overrides.values():
            cat = override_data['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print(f"  Override breakdown:")
        for cat, count in sorted(by_category.items()):
            print(f"    - {cat}: {count} cells")
    
    def get_override(self, session_id: int, cell_idx: int) -> Optional[str]:
        """
        Get override category for a specific cell.
        
        Returns:
            Override category ('tuned', 'non_tuned', 'excluded') or None if no override
        """
        key = (session_id, cell_idx)
        if key in self.overrides:
            return self.overrides[key]['category']
        return None
    
    def apply_overrides(
        self,
        df: pd.DataFrame,
        session_id: int,
        laser_condition: str = 'OFF'
    ) -> pd.DataFrame:
        """
        Apply overrides to a DataFrame of cell metrics.
        
        Args:
            df: DataFrame with cell metrics
            session_id: Session identifier
            laser_condition: 'OFF' or 'ON' (only apply overrides to OFF)
        
        Returns:
            Modified DataFrame with overrides applied
        """
        if laser_condition != 'OFF':
            # Only apply overrides to laser OFF condition
            return df
        
        if len(self.overrides) == 0:
            return df
        
        n_overridden = 0
        override_log = []
        
        for idx, row in df.iterrows():
            cell_idx = int(row['cell_idx'])
            override_cat = self.get_override(session_id, cell_idx)
            
            if override_cat is not None:
                original_cat = row['tuning_category']
                
                # Apply override
                df.at[idx, 'tuning_category'] = override_cat
                df.at[idx, 'is_tuned'] = (override_cat == 'tuned')
                
                if override_cat == 'excluded':
                    df.at[idx, 'is_excluded'] = True
                    df.at[idx, 'exclusion_reason'] = 'manual_override'
                else:
                    df.at[idx, 'is_excluded'] = False
                
                # Add override flag and info
                df.at[idx, 'is_overridden'] = True
                df.at[idx, 'override_from'] = original_cat
                df.at[idx, 'override_reason'] = self.overrides[(session_id, cell_idx)]['reason']
                
                n_overridden += 1
                override_log.append({
                    'cell': cell_idx,
                    'from': original_cat,
                    'to': override_cat,
                    'reason': self.overrides[(session_id, cell_idx)]['reason']
                })
        
        # Add override columns if they don't exist
        if 'is_overridden' not in df.columns:
            df['is_overridden'] = False
            df['override_from'] = ''
            df['override_reason'] = ''
        
        if n_overridden > 0:
            print(f"\n  ✓ Applied {n_overridden} classification overrides for session {session_id}:")
            for log in override_log:
                print(f"    Cell {log['cell']}: {log['from']} → {log['to']} ({log['reason']})")
        
        return df
    
    def has_overrides(self) -> bool:
        """Check if any overrides are loaded."""
        return len(self.overrides) > 0


# =============================================================================
# DATA LOADING MODULE
# =============================================================================

class CellDatabaseLoader:
    """Handles loading and caching of cell databases."""
    
    def __init__(self, sessions: Dict[int, SessionConfig]):
        self.sessions = sessions
        self._cache: Dict[str, pd.DataFrame] = {}
    
    def load_all(self) -> Dict[str, pd.DataFrame]:
        """Load cell databases for all unique subjects."""
        if self._cache:
            return self._cache
            
        print("\nLoading cell databases for all subjects...")
        subjects = get_unique_subjects(self.sessions)
        
        for subject in subjects:
            inforec_file = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py')
            print(f"  Loading {subject}...")
            self._cache[subject] = celldatabase.generate_cell_database(
                inforec_file, ignoreMissing=True
            )
        
        print(f"Loaded cell databases for {len(self._cache)} subjects\n")
        return self._cache


class SessionDataLoader:
    """Handles loading of session-specific data."""
    
    @staticmethod
    def load(session: SessionConfig, celldb_full: pd.DataFrame) -> SessionData:
        """Load AM tuning session data using pre-loaded cell database.
    
        """
        print(f"\nLoading: {session.subject} {session.date} depth={session.depth}um")
        
        # Filter to this session
        celldb_subset = celldb_full[
            (celldb_full.date == session.date) & 
            (celldb_full.pdepth == session.depth)
        ]
        
        if len(celldb_subset) == 0:
            raise ValueError(
                f"No cells found for {session.subject} {session.date} {session.depth}um"
            )
        
        print(f"  Found {len(celldb_subset)} cells")
        
        # Create ensemble and load data
        ensemble = ephyscore.CellEnsemble(celldb_subset)
        ephys_data, bdata = ensemble.load('optoTuningAM')
        
        # Find the correct field name for AM rates
        # Different experiments may use different field names
        possible_rate_fields = ['currentAMrate', 'AMrate', 'modRate', 'targetAMrate', 'currentFreq']
        rate_field = None
        
        for field in possible_rate_fields:
            if field in bdata:
                rate_field = field
                print(f"  Found AM rate data in field: '{field}'")
                break
        
        if rate_field is None:
            # Print all available fields for debugging
            print(f"  ERROR: Could not find AM rate field. Trying to list all bdata fields...")
            try:
                all_fields = [key for key in dir(bdata) if not key.startswith('_')]
                print(f"  Available bdata attributes: {all_fields[:20]}")  # Show first 20
            except:
                pass
            raise KeyError(
                f"AM rate field not found. Tried: {possible_rate_fields}. "
                f"Available label keys: {list(bdata.labels.keys()) if hasattr(bdata, 'labels') else 'N/A'}"
            )
        
        # Store the field name for later use
        bdata._am_rate_field = rate_field
        
        return SessionData(celldb_subset, ephys_data, bdata, ensemble)


# =============================================================================
# SPIKE ANALYSIS MODULE
# =============================================================================

class SpikeAnalyzer:
    """Handles spike-related computations."""
    
    @staticmethod
    def extract_event_locked_spikes(
        ensemble: ephyscore.CellEnsemble,
        event_onset_times: np.ndarray,
        time_range: Tuple[float, float]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Extract event-locked spike times for all cells."""
        return ensemble.eventlocked_spiketimes(event_onset_times, time_range)
    
    @staticmethod
    def compute_firing_rates_vectorized(
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        trial_nums: np.ndarray,
        response_window: Tuple[float, float]
    ) -> np.ndarray:
        """
        Compute firing rate (Hz) for specified trials using vectorized operations.
        
        Args:
            spike_times: Spike times relative to event onset
            trial_index: Trial index for each spike
            trial_nums: Which trials to analyze
            response_window: (start, end) time window in seconds
        
        Returns:
            Array of firing rates (Hz) for each trial
        """
        window_duration = response_window[1] - response_window[0]
        in_window = (spike_times >= response_window[0]) & (spike_times < response_window[1])
        
        firing_rates = np.zeros(len(trial_nums))
        for i, trial_num in enumerate(trial_nums):
            trial_mask = (trial_index == trial_num) & in_window
            firing_rates[i] = np.sum(trial_mask) / window_duration
        
        return firing_rates


# =============================================================================
# TUNING CURVE MODULE
# =============================================================================

class TuningCurveAnalyzer:
    """Analyzes AM rate tuning curves."""
    
    def __init__(self, spike_analyzer: SpikeAnalyzer):
        self.spike_analyzer = spike_analyzer
    
    def compute_tuning_curve(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        response_window: Tuple[float, float],
        baseline_window: Tuple[float, float],
        laser_condition: str = 'off'
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
        """
        Compute firing rate as a function of AM rate for one cell.
        
        IMPORTANT: baseline_rate is computed across ALL trials (both OFF and ON)
        for consistent comparison, but firing rates are condition-specific.
        
        Args:
            spike_times: Spike times for one cell
            trial_index: Trial indices for each spike
            bdata: Behavioral data dictionary
            response_window: Time window for counting spikes (stimulus-evoked)
            baseline_window: Time window for baseline firing rate (pre-stimulus)
            laser_condition: 'off' or 'on'
        
        Returns:
            Tuple of (am_rates, mean_rates, sem_rates, baseline_rate, fano_factor)
        """
        # Use the dynamically discovered field name
        rate_field = getattr(bdata, '_am_rate_field', 'currentFreq')
        am_rates = bdata[rate_field]  # AM rates from behavioral data
        laser_mask = self._get_laser_mask(bdata, laser_condition)
        unique_rates = np.unique(am_rates)
        
        mean_rates = np.zeros(len(unique_rates))
        sem_rates = np.zeros(len(unique_rates))
        all_fano_factors = []
        
        # Compute BASELINE firing rate across ALL trials (both OFF and ON combined)
        # This provides a shared baseline for fair comparison
        baseline_duration = baseline_window[1] - baseline_window[0]
        in_baseline = (spike_times >= baseline_window[0]) & (spike_times < baseline_window[1])
        all_trials = np.arange(len(am_rates))  # ALL trials, not filtered by laser
        
        baseline_spike_counts = []
        for trial_num in all_trials:
            trial_baseline_mask = (trial_index == trial_num) & in_baseline
            baseline_spike_counts.append(np.sum(trial_baseline_mask))
        
        baseline_rate = np.mean(baseline_spike_counts) / baseline_duration if len(baseline_spike_counts) > 0 else 0.0
        
        # Precompute response window mask
        window_duration = response_window[1] - response_window[0]
        in_window = (spike_times >= response_window[0]) & (spike_times < response_window[1])
        
        for i, rate in enumerate(unique_rates):
            trial_mask = (am_rates == rate) & laser_mask
            trial_nums = np.where(trial_mask)[0]
            
            if len(trial_nums) == 0:
                mean_rates[i] = np.nan
                sem_rates[i] = np.nan
                continue
            
            # Collect spike counts for each trial
            spike_counts = np.zeros(len(trial_nums))
            for j, trial_num in enumerate(trial_nums):
                trial_spike_mask = (trial_index == trial_num) & in_window
                spike_counts[j] = np.sum(trial_spike_mask)
            
            # Calculate mean firing rate
            rates = spike_counts / window_duration
            mean_rates[i] = np.mean(rates)
            sem_rates[i] = np.std(rates) / np.sqrt(len(rates))
            
            # Calculate Fano Factor for this AM rate (if sufficient trials)
            if len(spike_counts) >= 3:  # Need minimum trials
                mean_count = np.mean(spike_counts)
                var_count = np.var(spike_counts)
                if mean_count > 0:
                    fano = var_count / mean_count
                    all_fano_factors.append(fano)
        
        # Mean Fano Factor across all AM rates
        fano_factor = np.mean(all_fano_factors) if len(all_fano_factors) > 0 else np.nan
        
        return unique_rates, mean_rates, sem_rates, baseline_rate, fano_factor
    
    @staticmethod
    def _get_laser_mask(bdata: dict, laser_condition: str) -> np.ndarray:
        """Get boolean mask for laser condition."""
        # Get the dynamically discovered field name
        rate_field = getattr(bdata, '_am_rate_field', 'currentFreq')
        
        if 'laserTrial' in bdata:
            laser_trials = bdata['laserTrial']
        else:
            laser_trials = np.zeros(len(bdata[rate_field]), dtype=bool)
        
        if laser_condition == 'off':
            return laser_trials == 0
        elif laser_condition == 'on':
            return laser_trials == 1
        else:
            raise ValueError(f"Invalid laser_condition: {laser_condition}")


# =============================================================================
# METRICS CALCULATION MODULE
# =============================================================================

class TuningMetricsCalculator:
    """Calculates tuning quality metrics from tuning curves."""
    
    @staticmethod
    def calculate(am_rates: np.ndarray, firing_rates: np.ndarray, baseline_rate: float, fano_factor: float = np.nan) -> Optional[TuningMetrics]:
        """
        Calculate comprehensive AM tuning metrics.
        
        Args:
            am_rates: Array of AM rates (Hz)
            firing_rates: Array of mean firing rates at each AM rate
            baseline_rate: Baseline firing rate during pre-stimulus window (Hz)
            fano_factor: Trial-to-trial variability (variance/mean of spike counts)
        
        Returns None if insufficient data points (< 3).
        """
        # Remove NaN values
        valid_mask = ~np.isnan(firing_rates)
        if np.sum(valid_mask) < 3:
            return None
        
        rates_valid = am_rates[valid_mask]
        responses_valid = firing_rates[valid_mask]
        
        # Basic statistics
        peak_idx = np.argmax(responses_valid)
        best_rate = rates_valid[peak_idx]
        peak_response = responses_valid[peak_idx]
        min_response = np.min(responses_valid)
        mean_response = np.mean(responses_valid)
        dynamic_range = peak_response - min_response
        
        # Baseline-subtracted metrics
        baseline_subtracted_peak = peak_response - baseline_rate
        baseline_subtracted_mean = mean_response - baseline_rate
        
        # Selectivity Index: (peak - mean) / (peak + mean)
        selectivity = safe_divide(peak_response - mean_response, peak_response + mean_response)
        
        # Sparseness (lifetime): 1 - (mean²/mean(responses²))
        mean_sq = mean_response ** 2
        mean_of_sq = np.mean(responses_valid ** 2)
        sparseness = 1 - safe_divide(mean_sq, mean_of_sq)
        
        # Bandwidth at half-maximum (FWHM)
        bandwidth_hz, bandwidth_octaves = TuningMetricsCalculator._calculate_bandwidth(
            rates_valid, responses_valid, peak_response
        )
        
        # Q-factor: best_rate / bandwidth_hz
        q_factor = safe_divide(best_rate, bandwidth_hz)
        
        # Composite tuning quality score
        if not (np.isnan(selectivity) or np.isnan(sparseness)):
            tuning_quality = (selectivity + sparseness) / 2
        else:
            tuning_quality = np.nan
        
        return TuningMetrics(
            best_rate=best_rate,
            peak_response=peak_response,
            baseline_rate=baseline_rate,
            mean_response=mean_response,
            dynamic_range=dynamic_range,
            baseline_subtracted_peak=baseline_subtracted_peak,
            baseline_subtracted_mean=baseline_subtracted_mean,
            selectivity_index=selectivity,
            sparseness=sparseness,
            bandwidth_hz=bandwidth_hz,
            bandwidth_octaves=bandwidth_octaves,
            q_factor=q_factor,
            tuning_quality=tuning_quality,
            fano_factor=fano_factor
        )
    
    @staticmethod
    def _calculate_bandwidth(
        freqs: np.ndarray,
        rates: np.ndarray,
        peak_rate: float
    ) -> Tuple[float, float]:
        """
        Calculate bandwidth at half-maximum in Hz and octaves.
        
        CRITICAL: Bandwidth should be calculated as half of the AMPLITUDE,
        not half of the peak rate. This accounts for the baseline.
        
        Formula: half_max = baseline + (peak - baseline) / 2
        
        Args:
            freqs: AM rate values
            rates: Firing rates at each AM rate
            peak_rate: Peak firing rate (maximum response)
        
        Returns:
            Tuple of (bandwidth_hz, bandwidth_octaves)
        """
        # Get baseline (minimum response)
        baseline = np.min(rates)
        
        # Calculate amplitude (dynamic range above baseline)
        amplitude = peak_rate - baseline
        
        # Half-maximum is baseline + half the amplitude
        # This ensures we're measuring width at 50% of the response range
        half_max = baseline + amplitude / 2.0
        
        above_half = rates >= half_max
        
        bandwidth_hz = np.nan
        bandwidth_octaves = np.nan
        
        if np.sum(above_half) >= 2:
            crossing_indices = np.where(np.diff(above_half.astype(int)) != 0)[0]
            
            if len(crossing_indices) >= 2:
                idx1, idx2 = crossing_indices[0], crossing_indices[-1]
                lower_freq = freqs[idx1]
                upper_freq = freqs[idx2 + 1] if idx2 < len(freqs) - 1 else freqs[idx2]
                
                bandwidth_hz = upper_freq - lower_freq
                if lower_freq > 0:
                    bandwidth_octaves = np.log2(upper_freq / lower_freq)
        
        return bandwidth_hz, bandwidth_octaves


# =============================================================================
# CELL POPULATION ANALYZER MODULE
# =============================================================================

class CellPopulationAnalyzer:
    """Analyzes populations of cells across laser conditions."""
    
    def __init__(
        self,
        tuning_analyzer: TuningCurveAnalyzer,
        metrics_calculator: TuningMetricsCalculator,
        config: AnalysisConfig
    ):
        self.tuning_analyzer = tuning_analyzer
        self.metrics_calculator = metrics_calculator
        self.config = config
    
    def analyze_all_cells(
        self,
        spike_times_all: np.ndarray,
        trial_index_all: np.ndarray,
        bdata: dict
    ) -> Tuple[pd.DataFrame, pd.DataFrame, int, int]:
        """
        Analyze tuning metrics for all cells for both laser conditions.
        
        Saves ALL cells including excluded ones for QC verification.
        Excluded cells are marked with tuning_category='excluded'.
        
        Returns:
            Tuple of (df_off, df_on, n_excluded, n_total)
        """
        results_off = []
        results_on = []
        n_cells_excluded = 0
        n_cells_total = len(spike_times_all)
        
        for cell_idx in range(n_cells_total):
            spike_times = spike_times_all[cell_idx]
            trial_index = trial_index_all[cell_idx]
            
            # Compute both conditions - now also get AM rates and responses
            metrics_off, rates_off, responses_off = self._compute_cell_metrics(
                spike_times, trial_index, bdata, 'off'
            )
            metrics_on, rates_on, responses_on = self._compute_cell_metrics(
                spike_times, trial_index, bdata, 'on'
            )
            
            # Two-tier quality control
            # Tier 1: Is cell alive? (detection threshold)
            is_dead = (metrics_off is None or 
                      metrics_off.mean_response < self.config.min_detection_threshold)
            
            if is_dead:
                n_cells_excluded += 1
                # Save as excluded_dead for QC verification
                if metrics_off is not None:
                    result = self._metrics_to_dict(cell_idx, spike_times, metrics_off, rates_off, responses_off)
                    result['is_excluded'] = True
                    result['exclusion_reason'] = 'low_fr_dead'
                    results_off.append(result)
                continue
            
            # Tier 2: Does cell have sufficient FR for reliable tuning analysis?
            is_weak = (metrics_off.mean_response < self.config.min_analysis_threshold)
            
            if is_weak:
                n_cells_excluded += 1
                # Save as excluded_weak for QC verification
                result = self._metrics_to_dict(cell_idx, spike_times, metrics_off, rates_off, responses_off)
                result['is_excluded'] = True
                result['exclusion_reason'] = 'low_fr_weak'
                results_off.append(result)
                continue
            
            # Cell passed both QC tiers - analyze it
            result_off = self._metrics_to_dict(cell_idx, spike_times, metrics_off, rates_off, responses_off)
            result_off['is_excluded'] = False  # Mark as included
            results_off.append(result_off)
            
            if metrics_on is not None:
                result_on = self._metrics_to_dict(cell_idx, spike_times, metrics_on, rates_on, responses_on)
                result_on['is_excluded'] = False  # Mark as included
                results_on.append(result_on)
        
        # Print summary
        self._print_qc_summary(n_cells_total, n_cells_excluded, len(results_off) - n_cells_excluded)
        
        # Create and classify DataFrames
        df_off = self._create_classified_dataframe(results_off, 'OFF', n_cells_excluded, n_cells_total)
        df_on = self._create_classified_dataframe(results_on, 'ON')
        
        return df_off, df_on, n_cells_excluded, n_cells_total
    
    def _compute_cell_metrics(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        laser_condition: str
    ) -> Tuple[Optional[TuningMetrics], np.ndarray, np.ndarray]:
        """
        Compute tuning metrics for a single cell.
        
        Returns:
            Tuple of (metrics, am_rates, firing_rates)
        """
        am_rates, firing_rates, _, baseline_rate, fano_factor = self.tuning_analyzer.compute_tuning_curve(
            spike_times, trial_index, bdata,
            self.config.response_window, self.config.baseline_window, laser_condition
        )
        metrics = self.metrics_calculator.calculate(am_rates, firing_rates, baseline_rate, fano_factor)
        return metrics, am_rates, firing_rates
    
    @staticmethod
    def _metrics_to_dict(cell_idx: int, spike_times: np.ndarray, metrics: TuningMetrics,
                        am_rates: np.ndarray, firing_rates: np.ndarray) -> dict:
        """Convert TuningMetrics to dictionary for DataFrame, including tuning curve data."""
        # Convert arrays to comma-separated strings for CSV storage
        rate_str = ','.join([f'{r:.2f}' for r in am_rates])
        response_str = ','.join([f'{fr:.4f}' if not np.isnan(fr) else 'nan' for fr in firing_rates])
        
        return {
            'cell_idx': cell_idx,
            'n_spikes': len(spike_times),
            **metrics._asdict(),
            'tuning_rates_am': rate_str,
            'tuning_responses': response_str
        }
    
    def _print_qc_summary(self, n_total: int, n_excluded: int, n_passed: int):
        """Print quality control summary."""
        print(f"\n  QUALITY CONTROL SUMMARY:")
        print(f"  {'='*50}")
        print(f"  Total cells in session: {n_total}")
        print(f"  Cells passing QC: {n_passed} ({100*n_passed/n_total:.1f}%)")
        print(f"  Cells excluded (low firing rate): {n_excluded} ({100*n_excluded/n_total:.1f}%)")
        print(f"  Detection threshold (alive): {self.config.min_detection_threshold} Hz")
        print(f"  Analysis threshold (reliable tuning): {self.config.min_analysis_threshold} Hz")
    
    def _create_classified_dataframe(
        self,
        results: List[dict],
        laser_label: str,
        n_excluded: int = 0,
        n_total: int = None
    ) -> pd.DataFrame:
        """Create DataFrame and add classification columns."""
        df = pd.DataFrame(results)
        
        if len(df) == 0:
            return df
        
        # Calculate stimulus-evoked change for non-excluded cells
        # stimulus_evoked_change = (peak - baseline) / baseline
        # Use small epsilon (0.1 Hz) for cells with very low baseline to avoid division by zero
        df['stimulus_evoked_change'] = np.nan
        epsilon = 0.1  # Small baseline floor to prevent division by zero
        
        # Calculate for all cells with valid data
        valid_mask = (~np.isnan(df['baseline_rate'])) & (~np.isnan(df['peak_response']))
        df.loc[valid_mask, 'stimulus_evoked_change'] = (
            (df.loc[valid_mask, 'peak_response'] - df.loc[valid_mask, 'baseline_rate']) / 
            np.maximum(df.loc[valid_mask, 'baseline_rate'], epsilon)
        )
        
        # Classify cells based on TWO criteria (AND logic):
        # A cell is tuned if it meets BOTH criteria:
        # 1. Tuning quality >= threshold (0.20) - clear preference for specific AM rates
        # 2. Stimulus-evoked change >= threshold (0.50) - strong response modulation (50% increase)
        has_good_tuning = df['tuning_quality'] >= self.config.tuning_quality_threshold
        has_sufficient_modulation = df['stimulus_evoked_change'] >= self.config.min_modulation_threshold
        
        df['is_tuned'] = has_good_tuning & has_sufficient_modulation  # AND - both required
        df['tuning_category'] = 'non_tuned'  # Default
        
        # Apply classification rules
        df.loc[df['is_excluded'] == True, 'tuning_category'] = 'excluded'
        df.loc[(df['is_excluded'] == False) & (df['is_tuned'] == True), 'tuning_category'] = 'tuned'
        df.loc[(df['is_excluded'] == False) & (df['is_tuned'] == False), 'tuning_category'] = 'non_tuned'
        
        # Print statistics
        self._print_metrics_summary(df, laser_label, n_excluded, n_total)
        
        return df
    
    def _print_metrics_summary(
        self,
        df: pd.DataFrame,
        laser_label: str,
        n_excluded: int,
        n_total: Optional[int]
    ):
        """Print metrics and classification summary."""
        print(f"\n  LASER {laser_label} - TUNING QUALITY METRICS:")
        print(f"  {'='*50}")
        print(f"  Selectivity Index: {df['selectivity_index'].mean():.3f} ± {df['selectivity_index'].std():.3f}")
        print(f"  Sparseness:        {df['sparseness'].mean():.3f} ± {df['sparseness'].std():.3f}")
        
        valid_bw = df['bandwidth_octaves'].dropna()
        if len(valid_bw) > 0:
            print(f"  Bandwidth:         {valid_bw.mean():.2f} ± {valid_bw.std():.2f} octaves")
        
        # Show stimulus-evoked change stats for non-excluded cells
        non_excluded = df[df['is_excluded'] == False]
        if len(non_excluded) > 0:
            valid_change = non_excluded['stimulus_evoked_change'].dropna()
            if len(valid_change) > 0:
                print(f"  Evoked change:     {valid_change.mean()*100:.1f}% ± {valid_change.std()*100:.1f}%")
        
        print(f"\n  LASER {laser_label} - CELL CLASSIFICATION:")
        print(f"  {'='*50}")
        print(f"  Criteria for 'tuned' (BOTH required):")
        print(f"    - Tuning quality >= {self.config.tuning_quality_threshold}")
        print(f"    - Stimulus-evoked change >= {self.config.min_modulation_threshold*100:.0f}% increase from baseline")
        print(f"")
        
        # Print all three categories
        for category in ['excluded', 'non_tuned', 'tuned']:
            n_cells = np.sum(df['tuning_category'] == category)
            if n_cells > 0 or category == 'excluded':  # Always show excluded count
                denominator = n_total if n_total is not None else len(df)
                pct = 100 * n_cells / denominator if denominator > 0 else 0
                category_display = category.replace('_', ' ').title()
                if category == 'excluded':
                    category_display += ' (Low FR)'
                print(f"  {category_display:20s}: {n_cells:3d} cells ({pct:5.1f}%)")
                
                # For tuned cells, show breakdown
                if category == 'tuned' and n_cells > 0:
                    tuned_cells = df[df['tuning_category'] == 'tuned']
                    mean_change = tuned_cells['stimulus_evoked_change'].mean() * 100
                    print(f"    → Mean evoked change: {mean_change:.1f}%")


# =============================================================================
# PLOTTING MODULE
# =============================================================================

class TuningPlotter:
    """Handles all plotting functions."""
    
    @staticmethod
    def plot_session_metrics(
        df: pd.DataFrame,
        session: SessionConfig,
        n_excluded: int,
        n_total: int,
        laser_condition: str = 'OFF',
        save_path: Optional[str] = None
    ) -> Optional[Figure]:
        """Plot summary of tuning quality metrics for one session."""
        if len(df) == 0:
            print("  No cells to plot")
            return None
        
        with figure_context(save_path, figsize=(14, 10)) as fig:
            axes = fig.subplots(2, 2).flatten()
            
            # Plot 1: Selectivity Index
            TuningPlotter._plot_metric_distribution(
                axes[0], df['selectivity_index'], 'Selectivity Index',
                'steelblue', precision=3
            )
            
            # Plot 2: Sparseness
            TuningPlotter._plot_metric_distribution(
                axes[1], df['sparseness'], 'Sparseness',
                'seagreen', precision=3
            )
            
            # Plot 3: Bandwidth
            TuningPlotter._plot_metric_distribution(
                axes[2], df['bandwidth_octaves'], 'Bandwidth (octaves)',
                'purple', precision=2
            )
            
            # Plot 4: Selectivity vs Sparseness scatter
            TuningPlotter._plot_scatter(
                axes[3], df, 'selectivity_index', 'sparseness',
                'Selectivity Index', 'Sparseness'
            )
            
            # Title
            title = TuningPlotter._format_session_title(
                session, laser_condition, len(df), n_excluded, n_total, "Metrics"
            )
            fig.suptitle(title, fontsize=13, fontweight='bold')
            fig.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_all_sessions_summary(
        combined_df: pd.DataFrame,
        sessions: Dict[int, SessionConfig],
        total_excluded: int,
        total_recorded: int,
        laser_condition: str = 'OFF',
        save_path: Optional[str] = None
    ) -> Optional[Figure]:
        """Plot comprehensive summary across all sessions."""
        if len(combined_df) == 0:
            print("  No cells to plot in all-sessions summary")
            return None
        
        # Filter to only analyzed cells (not excluded)
        df_analyzed = combined_df[combined_df['tuning_category'] != 'excluded'].copy()
        n_analyzed = len(df_analyzed)
        
        with figure_context(save_path, figsize=(18, 10)) as fig:
            # Create grid: 2 rows x 3 columns
            gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
            
            # Row 1: Mean metrics by session (bar plots)
            ax1 = fig.add_subplot(gs[0, 0])
            ax2 = fig.add_subplot(gs[0, 1])
            ax3 = fig.add_subplot(gs[0, 2])
            
            # Row 2: Overall distributions
            ax4 = fig.add_subplot(gs[1, 0])  # Scatter
            ax5 = fig.add_subplot(gs[1, 1])  # Pie chart
            ax6 = fig.add_subplot(gs[1, 2])  # Summary text
            
            # Plot 1: Mean Selectivity by Session
            TuningPlotter._plot_metric_by_session(
                ax1, df_analyzed, sessions, 'selectivity_index',
                'Mean Selectivity Index by Session', 'steelblue'
            )
            
            # Plot 2: Mean Sparseness by Session
            TuningPlotter._plot_metric_by_session(
                ax2, df_analyzed, sessions, 'sparseness',
                'Mean Sparseness by Session', 'seagreen'
            )
            
            # Plot 3: Mean Bandwidth by Session
            TuningPlotter._plot_metric_by_session(
                ax3, df_analyzed, sessions, 'bandwidth_octaves',
                'Mean Bandwidth by Session', 'purple'
            )
            
            # Plot 4: Selectivity vs Sparseness scatter
            TuningPlotter._plot_all_sessions_scatter(
                ax4, df_analyzed, 'selectivity_index', 'sparseness'
            )
            
            # Plot 5: Classification pie chart
            TuningPlotter._plot_classification_pie(
                ax5, combined_df, total_recorded
            )
            
            # Plot 6: Summary statistics text
            TuningPlotter._plot_summary_text(
                ax6, combined_df, total_excluded, total_recorded, n_analyzed
            )
            
            # Overall title
            pct_excluded = 100 * total_excluded / total_recorded if total_recorded > 0 else 0
            fig.suptitle(
                f'AM Rate Tuning Quality - All Sessions Summary\n'
                f'Total analyzed: {n_analyzed} cells | '
                f'Excluded: {total_excluded} cells ({pct_excluded:.1f}% filtered by firing rate)',
                fontsize=14, fontweight='bold'
            )
        
        return fig
    
    @staticmethod
    def _plot_metric_by_session(ax, df, sessions, metric_col, title, color):
        """Plot mean ± SEM of a metric across sessions."""
        session_ids = sorted(df['session_id'].unique())
        means = []
        sems = []
        labels = []
        
        for sid in session_ids:
            session_data = df[df['session_id'] == sid][metric_col].dropna()
            if len(session_data) > 0:
                means.append(session_data.mean())
                sems.append(session_data.std() / np.sqrt(len(session_data)))
                labels.append(f'S{sid}')
        
        x_pos = np.arange(len(means))
        ax.bar(x_pos, means, yerr=sems, capsize=5, color=color, alpha=0.7,
              edgecolor='black', linewidth=1)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, rotation=0, fontsize=9)
        ax.set_xlabel('Session', fontsize=10)
        ax.set_ylabel(metric_col.replace('_', ' ').title(), fontsize=10)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    @staticmethod
    def _plot_all_sessions_scatter(ax, df, x_col, y_col):
        """Plot scatter of all cells across sessions."""
        valid_mask = ~(np.isnan(df[x_col]) | np.isnan(df[y_col]))
        df_valid = df[valid_mask]
        
        ax.scatter(df_valid[x_col], df_valid[y_col], alpha=0.5, s=30, c='blue')
        ax.set_xlabel(x_col.replace('_', ' ').title(), fontsize=10)
        ax.set_ylabel(y_col.replace('_', ' ').title(), fontsize=10)
        ax.set_title(f'{x_col.replace("_", " ").title()} vs {y_col.replace("_", " ").title()}\n'
                    f'(all sessions, n={len(df_valid)})',
                    fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    @staticmethod
    def _plot_classification_pie(ax, df, total_recorded):
        """Plot pie chart of cell classification."""
        # Count by category
        counts = df['tuning_category'].value_counts()
        
        # Define colors and labels
        category_order = ['excluded', 'non_tuned', 'tuned']
        colors_map = {'excluded': 'gray', 'non_tuned': 'lightcoral', 'tuned': 'green'}
        labels_map = {'excluded': 'Excluded\n(Low FR)', 'non_tuned': 'Non-Tuned', 'tuned': 'Tuned'}
        
        sizes = []
        colors = []
        labels = []
        
        for cat in category_order:
            if cat in counts.index and counts[cat] > 0:
                sizes.append(counts[cat])
                colors.append(colors_map[cat])
                labels.append(f'{labels_map[cat]}\n{counts[cat]}\n({100*counts[cat]/total_recorded:.1f}%)')
        
        # Create pie chart
        wedges, texts = ax.pie(sizes, colors=colors, startangle=90,
                                counterclock=False, wedgeprops={'edgecolor': 'black', 'linewidth': 2})
        
        # Add legend
        ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
                 fontsize=9, frameon=True)
        
        ax.set_title('Overall Cell Classification\n'
                    f'(Total: {total_recorded} cells across all sessions)',
                    fontsize=11, fontweight='bold')
    
    @staticmethod
    def _plot_summary_text(ax, df, total_excluded, total_recorded, n_analyzed):
        """Plot summary statistics as text."""
        ax.axis('off')
        
        # Count by category
        n_excluded = np.sum(df['tuning_category'] == 'excluded')
        n_non_tuned = np.sum(df['tuning_category'] == 'non_tuned')
        n_tuned = np.sum(df['tuning_category'] == 'tuned')
        
        # Calculate percentages
        pct_excluded = 100 * n_excluded / total_recorded if total_recorded > 0 else 0
        pct_non_tuned = 100 * n_non_tuned / total_recorded if total_recorded > 0 else 0
        pct_tuned = 100 * n_tuned / total_recorded if total_recorded > 0 else 0
        
        # Tuning prevalence (of analyzed cells only)
        tuning_prevalence = 100 * n_tuned / n_analyzed if n_analyzed > 0 else 0
        
        # Build summary text line by line to avoid f-string issues
        lines = [
            "OVERALL SUMMARY",
            "=" * 45,
            "",
            f"Total cells recorded: {total_recorded}",
            "",
            f"Excluded (low FR < 2.0 Hz):",
            f"  {n_excluded} cells ({pct_excluded:.1f}%)",
            "",
            f"Analyzed cells: {n_analyzed}",
            f"  * Non-tuned: {n_non_tuned} ({pct_non_tuned:.1f}%)",
            f"  * Tuned: {n_tuned} ({pct_tuned:.1f}%)",
            "",
            f"Tuning prevalence:",
            f"  {tuning_prevalence:.1f}% of analyzed cells",
            f"  {pct_tuned:.1f}% of all recorded cells"
        ]
        summary_text = "\n".join(lines)
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
               fontsize=11, verticalalignment='top', family='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8,
                        edgecolor='black', linewidth=2))
    
    @staticmethod
    def _plot_metric_distribution(ax, data, title, color, precision=2):
        """Plot histogram with mean and median lines."""
        valid = data.dropna()
        if len(valid) == 0:
            return
        
        ax.hist(valid, bins=20, alpha=0.7, color=color, edgecolor='black')
        ax.axvline(valid.mean(), color='red', linestyle='--', linewidth=2,
                   label=f'Mean={valid.mean():.{precision}f}')
        ax.axvline(valid.median(), color='orange', linestyle='--', linewidth=2,
                   label=f'Median={valid.median():.{precision}f}')
        ax.set_xlabel(title, fontsize=11)
        ax.set_ylabel('Number of Cells', fontsize=11)
        ax.set_title(f'{title} Distribution (n={len(valid)})', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    @staticmethod
    def _plot_scatter(ax, df, x_col, y_col, x_label, y_label):
        """Plot scatter plot of two metrics."""
        valid_mask = ~(np.isnan(df[x_col]) | np.isnan(df[y_col]))
        df_valid = df[valid_mask]
        ax.scatter(df_valid[x_col], df_valid[y_col], alpha=0.6, s=50, c='blue')
        ax.set_xlabel(x_label, fontsize=11)
        ax.set_ylabel(y_label, fontsize=11)
        ax.set_title(f'{x_label} vs {y_label} (n={len(df_valid)})',
                     fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    @staticmethod
    def _format_session_title(session, laser_condition, n_analyzed, n_excluded, n_total, plot_type):
        """Format title for session plots."""
        if n_total > 0:
            return (f'{session.subject} {session.date} - Depth {session.depth}µm\n'
                   f'AM Rate Tuning {plot_type} (Laser {laser_condition} Trials)\n'
                   f'Analyzed: {n_analyzed} cells | Excluded: {n_excluded} cells '
                   f'({100*n_excluded/n_total:.1f}% filtered by firing rate)')
        else:
            return (f'{session.subject} {session.date} - Depth {session.depth}µm\n'
                   f'AM Rate Tuning {plot_type} (Laser {laser_condition} Trials)')


# =============================================================================
# SESSION COORDINATOR MODULE
# =============================================================================

class SessionAnalysisCoordinator:
    """Coordinates the analysis of individual sessions."""
    
    def __init__(
        self,
        config: AnalysisConfig,
        celldb_loader: CellDatabaseLoader,
        population_analyzer: CellPopulationAnalyzer,
        plotter: TuningPlotter,
        override_manager: ClassificationOverrideManager  # New parameter
    ):
        self.config = config
        self.celldb_loader = celldb_loader
        self.population_analyzer = population_analyzer
        self.plotter = plotter
        self.override_manager = override_manager  # Store override manager
    
    def analyze_session(
        self,
        session_id: int,
        session: SessionConfig,
        celldbs: Dict[str, pd.DataFrame]
    ) -> Optional[Tuple]:
        """Analyze one session and return results."""
        try:
            # Load data
            celldb_full = celldbs[session.subject]
            session_data = SessionDataLoader.load(session, celldb_full)
            
            # Prepare spike data
            event_times = self._prepare_event_times(session_data)
            spike_times_all, trial_index_all, _ = SpikeAnalyzer.extract_event_locked_spikes(
                session_data.ensemble, event_times, self.config.time_range
            )
            
            # Analyze cells
            df_off, df_on, n_excluded, n_total = self.population_analyzer.analyze_all_cells(
                spike_times_all, trial_index_all, session_data.bdata
            )
            
            # Apply manual classification overrides (only to laser OFF)
            if self.override_manager.has_overrides():
                df_off = self.override_manager.apply_overrides(df_off, session_id, laser_condition='OFF')
            
            # Add session metadata
            for df in [df_off, df_on]:
                if len(df) > 0:
                    df['session_id'] = session_id
                    df['subject'] = session.subject
                    df['date'] = session.date
                    df['depth'] = session.depth
            
            # Save outputs
            self._save_session_outputs(session_id, session, df_off, df_on, n_excluded, n_total)
            
            return session, df_off, df_on, n_excluded, n_total
            
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def _prepare_event_times(session_data: SessionData) -> np.ndarray:
        """Prepare event onset times, aligning trial counts if needed."""
        event_times = session_data.ephys_data['events']['stimOn']
        
        # Use the dynamically discovered AM rate field name
        rate_field = getattr(session_data.bdata, '_am_rate_field', 'currentFreq')
        n_trials = len(session_data.bdata[rate_field])
        
        if len(event_times) != n_trials and len(event_times) == n_trials + 1:
            event_times = event_times[:n_trials]
        
        return event_times
    
    def _save_session_outputs(
        self,
        session_id: int,
        session: SessionConfig,
        df_off: pd.DataFrame,
        df_on: pd.DataFrame,
        n_excluded: int,
        n_total: int
    ):
        """Save plots and CSVs for a session."""
        for df, laser_label in [(df_off, 'OFF'), (df_on, 'ON')]:
            if len(df) == 0:
                if laser_label == 'OFF':
                    print(f"  No cells passed QC for LASER {laser_label} in session {session_id}")
                continue
            
            suffix = laser_label.lower()
            
            # Plot metrics
            metrics_path = os.path.join(
                self.config.output_dir,
                f'session_{session_id}_laser_{suffix}_tuning_metrics.png'
            )
            self.plotter.plot_session_metrics(
                df, session, n_excluded if laser_label == 'OFF' else 0,
                n_total if laser_label == 'OFF' else len(df),
                laser_label, metrics_path
            )
            
            # Save CSV
            csv_path = os.path.join(
                self.config.output_dir,
                f'session_{session_id}_laser_{suffix}_tuning_metrics.csv'
            )
            df.to_csv(csv_path, index=False)
            print(f"  Saved LASER {laser_label} data to: {csv_path}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution pipeline."""
    print("="*60)
    print("AM RATE TUNING QUALITY METRICS - ALL SESSIONS")
    print("="*60)
    
    # Initialize configuration
    config = AnalysisConfig()
    
    # Create output directory using config property
    os.makedirs(config.output_dir, exist_ok=True)
    print(f"\nOutput directory: {config.output_dir}")
    
    # Initialize override manager
    override_manager = ClassificationOverrideManager(config.override_file)
    
    # Initialize components
    celldb_loader = CellDatabaseLoader(SESSIONS)
    spike_analyzer = SpikeAnalyzer()
    tuning_analyzer = TuningCurveAnalyzer(spike_analyzer)
    metrics_calculator = TuningMetricsCalculator()
    population_analyzer = CellPopulationAnalyzer(tuning_analyzer, metrics_calculator, config)
    plotter = TuningPlotter()
    coordinator = SessionAnalysisCoordinator(
        config, celldb_loader, population_analyzer, plotter, override_manager
    )
    
    # Load cell databases once
    celldbs = celldb_loader.load_all()
    
    # Analyze all sessions
    all_dataframes_off = []
    all_dataframes_on = []
    all_exclusion_stats = []
    
    for session_id in sorted(SESSIONS.keys()):
        print(f"\n{'='*60}")
        print(f"SESSION {session_id}")
        print(f"{'='*60}")
        
        result = coordinator.analyze_session(session_id, SESSIONS[session_id], celldbs)
        if result is not None:
            _, df_off, df_on, n_excluded, n_total = result
            
            if len(df_off) > 0:
                all_dataframes_off.append(df_off)
            if len(df_on) > 0:
                all_dataframes_on.append(df_on)
            
            all_exclusion_stats.append({'n_excluded': n_excluded, 'n_total': n_total})
    
    # Save combined CSVs
    for dfs, laser_label in [(all_dataframes_off, 'off'), (all_dataframes_on, 'on')]:
        if len(dfs) > 0:
            combined_df = pd.concat(dfs, ignore_index=True)
            csv_path = os.path.join(
                config.output_dir,
                f'all_sessions_laser_{laser_label}_tuning_metrics.csv'
            )
            combined_df.to_csv(csv_path, index=False)
            print(f"\nSaved combined LASER {laser_label.upper()} data to: {csv_path}")
    
    # Generate all-sessions summary plot
    print(f"\n{'='*60}")
    print("GENERATING ALL-SESSIONS SUMMARY PLOTS")
    print(f"{'='*60}")
    
    if len(all_dataframes_off) > 0:
        combined_df_off = pd.concat(all_dataframes_off, ignore_index=True)
        total_excluded = sum(stat['n_excluded'] for stat in all_exclusion_stats)
        total_recorded = sum(stat['n_total'] for stat in all_exclusion_stats)
        
        summary_plot_path = os.path.join(
            config.output_dir,
            'all_sessions_summary_laser_off.png'
        )
        
        plotter.plot_all_sessions_summary(
            combined_df_off,
            SESSIONS,
            total_excluded,
            total_recorded,
            laser_condition='OFF',
            save_path=summary_plot_path
        )
        print(f"Generated all-sessions summary plot: {summary_plot_path}")
    
    if len(all_dataframes_on) > 0:
        combined_df_on = pd.concat(all_dataframes_on, ignore_index=True)
        
        summary_plot_path_on = os.path.join(
            config.output_dir,
            'all_sessions_summary_laser_on.png'
        )
        
        plotter.plot_all_sessions_summary(
            combined_df_on,
            SESSIONS,
            0,  # No exclusions for laser ON
            len(combined_df_on),
            laser_condition='ON',
            save_path=summary_plot_path_on
        )
        print(f"Generated all-sessions summary plot: {summary_plot_path_on}")
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    print(f"Analyzed {len(all_exclusion_stats)} sessions")
    print(f"Generated CSVs for both LASER OFF and LASER ON conditions")
    print(f"Generated all-sessions summary plots")
    print(f"Saved to: {config.output_dir}")


if __name__ == '__main__':
    main()
