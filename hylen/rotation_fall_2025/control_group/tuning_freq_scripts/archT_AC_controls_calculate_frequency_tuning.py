"""
Calculate frequency tuning quality metrics for neural recordings.

This script analyzes frequency tuning quality for both laser OFF and laser ON conditions,
computing metrics such as selectivity index, sparseness, and bandwidth for each cell.

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
    baseline_window: Tuple[float, float] = (-0.095, -0.005)
    response_window: Tuple[float, float] = (0.005, 0.095)
    min_detection_threshold: float = 0.2
    min_analysis_threshold: float = 2.0
    tuning_quality_threshold: float = 0.2
    min_cv_threshold: float = 0.425
    max_bandwidth_threshold: float = 3.0

    @property
    def output_dir(self) -> str:
        return str(get_reports_subdir('control_group/tuning_freq_analysis'))

    @property
    def override_file(self) -> str:
        return os.path.join(self.output_dir, 'classification_overrides.csv')
    
    def __post_init__(self):
        """Validate configuration parameters."""
        assert self.time_range[0] < self.time_range[1], "Invalid time_range"
        assert self.baseline_window[0] < self.baseline_window[1], "Invalid baseline_window"
        assert self.response_window[0] < self.response_window[1], "Invalid response_window"
        assert self.min_detection_threshold > 0, "Detection threshold must be positive"
        assert self.min_analysis_threshold >= self.min_detection_threshold, \
            "Analysis threshold must be >= detection threshold"
        assert self.tuning_quality_threshold > 0, "Tuning quality threshold must be positive"
        assert self.min_cv_threshold > 0, "CV threshold must be positive"
        assert self.max_bandwidth_threshold > 0, "Max bandwidth threshold must be positive"


class TuningMetrics(NamedTuple):
    """Container for tuning curve metrics."""
    best_freq: float
    peak_rate: float
    baseline_rate: float
    mean_rate: float
    dynamic_range: float
    selectivity_index: float
    sparseness: float
    bandwidth_hz: float
    bandwidth_octaves: float
    q_factor: float
    tuning_quality: float
    coefficient_of_variation: float  # CV = std / mean, detect flat curves


class BaselineMetrics(NamedTuple):
    """Container for baseline firing rate metrics (pre-stimulus period)."""
    baseline_rate: float  # Mean firing rate in baseline window (Hz)
    baseline_std: float   # Std dev of firing rates across trials (Hz)
    n_trials_baseline: int  # Number of trials used for baseline calculation


class SessionData(NamedTuple):
    """Container for loaded session data."""
    celldb: pd.DataFrame
    ephys_data: dict
    bdata: dict
    ensemble: ephyscore.CellEnsemble


# All available sessions
SESSIONS = {
    0: SessionConfig('arch018', '2024-12-16', 3780),
    1: SessionConfig('arch018', '2024-12-16', 4500),
    2: SessionConfig('arch018', '2025-01-12', 3780),
    3: SessionConfig('arch018', '2025-01-12', 4500),
    4: SessionConfig('arch019', '2024-12-04', 3780),
    5: SessionConfig('arch019', '2024-12-04', 4500),
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
        """Load frequency tuning session data using pre-loaded cell database."""
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
        ephys_data, bdata = ensemble.load('optoTuningFreq')
        
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
    def compute_baseline_rate(
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        baseline_window: Tuple[float, float],
        laser_condition: str = 'off'
    ) -> BaselineMetrics:
        """
        Compute baseline firing rate from pre-stimulus window.
        
        IMPORTANT: Computes baseline across ALL trials (both OFF and ON combined)
        for consistent comparison between conditions. This is the same baseline
        used by the Gaussian fitting.
        
        Args:
            spike_times: Spike times for one cell (relative to event onset)
            trial_index: Trial indices for each spike
            bdata: Behavioral data dictionary
            baseline_window: (start, end) time window for baseline (e.g., (-0.095, -0.005))
            laser_condition: 'off' or 'on' (not used for baseline calculation, kept for compatibility)
        
        Returns:
            BaselineMetrics with mean rate, std, and trial count
        """
        # Calculate baseline across ALL trials (both OFF and ON)
        # This ensures both conditions use the same ground truth baseline
        all_trial_nums = np.arange(len(bdata['currentFreq']))
        
        if len(all_trial_nums) == 0:
            return BaselineMetrics(
                baseline_rate=np.nan,
                baseline_std=np.nan,
                n_trials_baseline=0
            )
        
        # Extract spikes in baseline window
        window_duration = baseline_window[1] - baseline_window[0]
        in_baseline = (spike_times >= baseline_window[0]) & (spike_times < baseline_window[1])
        
        # Compute firing rate for each trial (ALL trials, not filtered by laser)
        trial_rates = np.zeros(len(all_trial_nums))
        for i, trial_num in enumerate(all_trial_nums):
            trial_spike_mask = (trial_index == trial_num) & in_baseline
            trial_rates[i] = np.sum(trial_spike_mask) / window_duration
        
        # Compute statistics across ALL trials
        baseline_rate = np.mean(trial_rates)
        baseline_std = np.std(trial_rates)
        
        return BaselineMetrics(
            baseline_rate=baseline_rate,
            baseline_std=baseline_std,
            n_trials_baseline=len(all_trial_nums)
        )
    
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
    """Analyzes frequency tuning curves."""
    
    def __init__(self, spike_analyzer: SpikeAnalyzer):
        self.spike_analyzer = spike_analyzer
    
    def compute_tuning_curve(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        response_window: Tuple[float, float],
        laser_condition: str = 'off',
        cell_idx: int = -1  # For debugging
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute firing rate as a function of frequency for one cell.
        
        CRITICAL: trial_index from eventlocked_spiketimes is 0-indexed relative
        to the event_times array, which corresponds directly to bdata indices.
        
        Args:
            spike_times: Spike times for one cell
            trial_index: Trial indices for each spike (0-indexed, matches bdata)
            bdata: Behavioral data dictionary
            response_window: Time window for counting spikes
            laser_condition: 'off' or 'on'
            cell_idx: Cell index for debugging
        
        Returns:
            Tuple of (frequencies, mean_rates, sem_rates)
        """
        frequencies = np.asarray(bdata['currentFreq']).flatten()
        laser_mask = self._get_laser_mask(bdata, laser_condition)
        unique_freqs = np.unique(frequencies)
        
        mean_rates = np.zeros(len(unique_freqs))
        sem_rates = np.zeros(len(unique_freqs))
        
        # Precompute window mask
        window_duration = response_window[1] - response_window[0]
        in_window = (spike_times >= response_window[0]) & (spike_times < response_window[1])
        
        for i, freq in enumerate(unique_freqs):
            # Get trial indices where this frequency was presented with correct laser condition
            freq_laser_mask = (frequencies == freq) & laser_mask
            trial_nums = np.where(freq_laser_mask)[0]  # These are bdata indices (0-indexed)
            
            if len(trial_nums) == 0:
                mean_rates[i] = np.nan
                sem_rates[i] = np.nan
                continue
            
            # Count spikes for each trial
            # CRITICAL: trial_index values match the bdata indices directly
            rates = np.zeros(len(trial_nums))
            for j, trial_num in enumerate(trial_nums):
                trial_spike_mask = (trial_index == trial_num) & in_window
                rates[j] = np.sum(trial_spike_mask) / window_duration
            
            mean_rates[i] = np.mean(rates)
            sem_rates[i] = np.std(rates) / np.sqrt(len(rates))
        
        return unique_freqs, mean_rates, sem_rates
    
    @staticmethod
    def _get_laser_mask(bdata: dict, laser_condition: str) -> np.ndarray:
        """Get boolean mask for laser condition."""
        if 'laserTrial' in bdata:
            laser_trials = bdata['laserTrial']
            
            # Handle different possible formats of laserTrial array
            # It might be nested arrays, so flatten if needed
            if hasattr(laser_trials, 'ndim') and laser_trials.ndim > 1:
                laser_trials = laser_trials.flatten()
            
            # Convert to numpy array and ensure correct type
            laser_trials = np.asarray(laser_trials).flatten().astype(int)
            
            # CRITICAL: Ensure alignment with currentFreq
            n_trials = len(bdata['currentFreq'])
            if len(laser_trials) != n_trials:
                print(f"    WARNING: laserTrial length ({len(laser_trials)}) != currentFreq length ({n_trials})")
                # Truncate or pad to match
                if len(laser_trials) > n_trials:
                    laser_trials = laser_trials[:n_trials]
                else:
                    # Pad with zeros (assume OFF trials)
                    laser_trials = np.pad(laser_trials, (0, n_trials - len(laser_trials)), constant_values=0)
        else:
            laser_trials = np.zeros(len(bdata['currentFreq']), dtype=int)
        
        if laser_condition == 'off':
            mask = (laser_trials == 0)
        elif laser_condition == 'on':
            mask = (laser_trials == 1)
        else:
            raise ValueError(f"Invalid laser_condition: {laser_condition}")
        
        return mask


# =============================================================================
# METRICS CALCULATION MODULE
# =============================================================================

class TuningMetricsCalculator:
    """Calculates tuning quality metrics from tuning curves."""
    
    @staticmethod
    def calculate(frequencies: np.ndarray, firing_rates: np.ndarray) -> Optional[TuningMetrics]:
        """
        Calculate comprehensive tuning metrics.
        
        Returns None if insufficient data points (< 3).
        """
        # Remove NaN values
        valid_mask = ~np.isnan(firing_rates)
        if np.sum(valid_mask) < 3:
            return None
        
        freqs_valid = frequencies[valid_mask]
        rates_valid = firing_rates[valid_mask]
        
        # Basic statistics
        peak_idx = np.argmax(rates_valid)
        best_freq = freqs_valid[peak_idx]
        peak_rate = rates_valid[peak_idx]
        baseline_rate = np.min(rates_valid)
        mean_rate = np.mean(rates_valid)
        dynamic_range = peak_rate - baseline_rate
        
        # Selectivity Index: (peak - mean) / (peak + mean)
        selectivity = safe_divide(peak_rate - mean_rate, peak_rate + mean_rate)
        
        # Sparseness (lifetime): 1 - (mean²/mean(rates²))
        mean_sq = mean_rate ** 2
        mean_of_sq = np.mean(rates_valid ** 2)
        sparseness = 1 - safe_divide(mean_sq, mean_of_sq)
        
        # Bandwidth at half-maximum (FWHM)
        bandwidth_hz, bandwidth_octaves = TuningMetricsCalculator._calculate_bandwidth(
            freqs_valid, rates_valid, peak_rate
        )
        
        # Q-factor: best_freq / bandwidth_hz
        q_factor = safe_divide(best_freq, bandwidth_hz)
        
        # Coefficient of Variation: std / mean (detects flat curves)
        # Low CV = flat curve (all frequencies similar), High CV = tuned (peak stands out)
        cv = safe_divide(np.std(rates_valid), mean_rate)
        
        # Composite tuning quality score
        if not (np.isnan(selectivity) or np.isnan(sparseness)):
            tuning_quality = (selectivity + sparseness) / 2
        else:
            tuning_quality = np.nan
        
        return TuningMetrics(
            best_freq=best_freq,
            peak_rate=peak_rate,
            baseline_rate=baseline_rate,
            mean_rate=mean_rate,
            dynamic_range=dynamic_range,
            selectivity_index=selectivity,
            sparseness=sparseness,
            bandwidth_hz=bandwidth_hz,
            bandwidth_octaves=bandwidth_octaves,
            q_factor=q_factor,
            tuning_quality=tuning_quality,
            coefficient_of_variation=cv
        )
    
    @staticmethod
    def _calculate_bandwidth(
        freqs: np.ndarray,
        rates: np.ndarray,
        peak_rate: float
    ) -> Tuple[float, float]:
        """Calculate bandwidth at half-maximum in Hz and octaves."""
        half_max = peak_rate / 2.0
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
        
        QC is based ONLY on laser OFF condition. Cells passing laser OFF QC
        are analyzed for BOTH laser OFF and laser ON, even if laser ON has
        low firing rate (which is biologically meaningful - laser suppression).
        
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
            
            # Compute tuning metrics for both conditions
            metrics_off = self._compute_cell_metrics(
                spike_times, trial_index, bdata, 'off', cell_idx
            )
            metrics_on = self._compute_cell_metrics(
                spike_times, trial_index, bdata, 'on', cell_idx
            )
            
            # Compute baseline metrics for both conditions (for Gaussian fitting later)
            baseline_off = SpikeAnalyzer.compute_baseline_rate(
                spike_times, trial_index, bdata, self.config.baseline_window, 'off'
            )
            baseline_on = SpikeAnalyzer.compute_baseline_rate(
                spike_times, trial_index, bdata, self.config.baseline_window, 'on'
            )
            
            # Two-tier quality control BASED ON LASER OFF ONLY
            # Tier 1: Is cell alive? (detection threshold)
            is_dead = (metrics_off is None or 
                      metrics_off.mean_rate < self.config.min_detection_threshold)
            
            if is_dead:
                n_cells_excluded += 1
                # Save as excluded_dead for QC verification
                if metrics_off is not None:
                    result = self._metrics_to_dict(cell_idx, spike_times, trial_index, 
                                                   bdata, metrics_off, baseline_off, 'off')
                    result['is_excluded'] = True
                    result['exclusion_reason'] = 'low_fr_dead'
                    results_off.append(result)
                continue
            
            # Tier 2: Does cell have sufficient FR for reliable tuning analysis?
            is_weak = (metrics_off.mean_rate < self.config.min_analysis_threshold)
            
            if is_weak:
                n_cells_excluded += 1
                # Save as excluded_weak for QC verification
                result = self._metrics_to_dict(cell_idx, spike_times, trial_index,
                                               bdata, metrics_off, baseline_off, 'off')
                result['is_excluded'] = True
                result['exclusion_reason'] = 'low_fr_weak'
                results_off.append(result)
                continue
            
            # Cell passed QC tiers - analyze for BOTH laser OFF and laser ON
            # Note: Flat curves are NOT excluded, they're just classified as non-tuned
            result_off = self._metrics_to_dict(cell_idx, spike_times, trial_index,
                                               bdata, metrics_off, baseline_off, 'off')
            result_off['is_excluded'] = False
            results_off.append(result_off)
            
            # ALWAYS analyze laser ON for cells that passed laser OFF QC
            # Even if laser ON has low firing rate (that's the point!)
            if metrics_on is not None:
                result_on = self._metrics_to_dict(cell_idx, spike_times, trial_index,
                                                  bdata, metrics_on, baseline_on, 'on')
                result_on['is_excluded'] = False
                results_on.append(result_on)
            else:
                # Still create entry with NaN values if metrics_on is None
                result_on = {
                    'cell_idx': cell_idx,
                    'n_spikes': len(spike_times),
                    'best_freq': np.nan,
                    'peak_rate': np.nan,
                    'baseline_rate': np.nan,
                    'mean_rate': np.nan,
                    'dynamic_range': np.nan,
                    'selectivity_index': np.nan,
                    'sparseness': np.nan,
                    'bandwidth_hz': np.nan,
                    'bandwidth_octaves': np.nan,
                    'q_factor': np.nan,
                    'tuning_quality': np.nan,
                    'coefficient_of_variation': np.nan,
                    'baseline_rate_prestim': np.nan,
                    'baseline_std_prestim': np.nan,
                    'n_trials_baseline': 0,
                    'tuning_freqs': '',
                    'tuning_rates': '',
                    'tuning_sems': '',
                    'is_excluded': False
                }
                results_on.append(result_on)
        
        # Print summary
        self._print_qc_summary(n_cells_total, n_cells_excluded, len(results_off))
        
        # Create and classify DataFrames
        df_off = self._create_classified_dataframe(results_off, 'OFF', n_cells_excluded, n_cells_total)
        df_on = self._create_classified_dataframe(results_on, 'ON')
        
        return df_off, df_on, n_cells_excluded, n_cells_total
    
    def _compute_cell_metrics(
        self,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        laser_condition: str,
        cell_idx: int = -1
    ) -> Optional[TuningMetrics]:
        """Compute tuning metrics for a single cell."""
        freqs, rates, _ = self.tuning_analyzer.compute_tuning_curve(
            spike_times, trial_index, bdata,
            self.config.response_window, laser_condition, cell_idx
        )
        return self.metrics_calculator.calculate(freqs, rates)
    
    def _metrics_to_dict(
        self,
        cell_idx: int,
        spike_times: np.ndarray,
        trial_index: np.ndarray,
        bdata: dict,
        metrics: TuningMetrics,
        baseline: BaselineMetrics,
        laser_condition: str
    ) -> dict:
        """Convert TuningMetrics and BaselineMetrics to dictionary for DataFrame."""
        # Reconstruct tuning curve to save with metrics
        freqs, rates, sems = self.tuning_analyzer.compute_tuning_curve(
            spike_times, trial_index, bdata,
            self.config.response_window, laser_condition, cell_idx
        )
        
        # Convert arrays to comma-separated strings for CSV storage
        freqs_str = ','.join([f'{f:.2f}' for f in freqs])
        rates_str = ','.join([f'{r:.4f}' if not np.isnan(r) else 'nan' for r in rates])
        sems_str = ','.join([f'{s:.4f}' if not np.isnan(s) else 'nan' for s in sems])
        
        return {
            'cell_idx': cell_idx,
            'n_spikes': len(spike_times),
            **metrics._asdict(),
            'baseline_rate_prestim': baseline.baseline_rate,
            'baseline_std_prestim': baseline.baseline_std,
            'n_trials_baseline': baseline.n_trials_baseline,
            # NEW: Save tuning curve data for Gaussian fitting
            'tuning_freqs': freqs_str,
            'tuning_rates': rates_str,
            'tuning_sems': sems_str
        }
    
    def _print_qc_summary(self, n_total: int, n_excluded: int, n_passed: int):
        """Print quality control summary."""
        print(f"\n  QUALITY CONTROL SUMMARY:")
        print(f"  {'='*50}")
        print(f"  Total cells in session: {n_total}")
        print(f"  Cells passing QC: {n_passed} ({100*n_passed/n_total:.1f}%)")
        print(f"  Cells excluded: {n_excluded} ({100*n_excluded/n_total:.1f}%)")
        print(f"    - Detection threshold (alive): {self.config.min_detection_threshold} Hz")
        print(f"    - Analysis threshold (reliable tuning): {self.config.min_analysis_threshold} Hz")
        print(f"\n  Classification criteria (for non-excluded cells):")
        print(f"    - Tuning quality threshold: {self.config.tuning_quality_threshold}")
        print(f"    - CV threshold (flat curve filter): {self.config.min_cv_threshold}")
        print(f"    - Max bandwidth (broad tuning filter): {self.config.max_bandwidth_threshold} octaves")
    
    def _create_classified_dataframe(
        self,
        results: List[dict],
        laser_label: str,
        n_excluded: int = 0,
        n_total: int = None
    ) -> pd.DataFrame:
        """Create DataFrame and add classification columns using tuning quality threshold."""
        df = pd.DataFrame(results)
        
        if len(df) == 0:
            return df
        
        # Simple classification based on tuning quality threshold AND coefficient of variation AND bandwidth
        df['is_tuned'] = False
        df['tuning_category'] = 'excluded'  # Default for excluded cells
        
        for idx, row in df.iterrows():
            if row['is_excluded']:
                # Excluded cells stay as 'excluded' category
                continue
            
            # Classify as non-tuned if:
            # 1. Tuning quality below threshold, OR
            # 2. Coefficient of variation below threshold (flat curve), OR
            # 3. Bandwidth calculable AND too broad (> max_bandwidth_threshold octaves)
            has_good_tq = (not pd.isna(row['tuning_quality'])) and \
                         (row['tuning_quality'] >= self.config.tuning_quality_threshold)
            
            has_good_cv = (not pd.isna(row['coefficient_of_variation'])) and \
                         (row['coefficient_of_variation'] >= self.config.min_cv_threshold)
            
            # Bandwidth criterion: PASS if NaN (not calculable) OR narrow enough
            # FAIL only if bandwidth is calculable AND too broad
            has_acceptable_bw = pd.isna(row['bandwidth_octaves']) or \
                               (row['bandwidth_octaves'] <= self.config.max_bandwidth_threshold)
            
            # Must pass ALL three criteria to be classified as tuned
            is_tuned = has_good_tq and has_good_cv and has_acceptable_bw
            
            df.at[idx, 'is_tuned'] = is_tuned
            df.at[idx, 'tuning_category'] = 'tuned' if is_tuned else 'non_tuned'
        
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
        
        print(f"\n  LASER {laser_label} - CELL CLASSIFICATION:")
        print(f"  {'='*50}")
        
        # Count exclusion reasons (only for excluded cells)
        if n_excluded > 0:
            print(f"  Excluded cells breakdown:")
            for reason in ['low_fr_dead', 'low_fr_weak']:
                if 'exclusion_reason' in df.columns:
                    n_reason = np.sum(df['exclusion_reason'] == reason)
                    if n_reason > 0:
                        reason_display = reason.replace('_', ' ').title()
                        print(f"    - {reason_display}: {n_reason} cells")
        
        # Count non-tuned cells by reason (flat curves and broad bandwidth are in non-tuned)
        non_tuned_df = df[df['tuning_category'] == 'non_tuned']
        if len(non_tuned_df) > 0:
            # Count different types of non-tuned cells
            n_flat = np.sum(
                (non_tuned_df['coefficient_of_variation'] < self.config.min_cv_threshold) |
                pd.isna(non_tuned_df['coefficient_of_variation'])
            )
            n_broad = np.sum(
                (~pd.isna(non_tuned_df['bandwidth_octaves'])) &
                (non_tuned_df['bandwidth_octaves'] > self.config.max_bandwidth_threshold)
            )
            n_low_tq = len(non_tuned_df) - n_flat - n_broad
            
            if n_flat > 0 or n_broad > 0 or n_low_tq > 0:
                print(f"  Non-tuned cells breakdown:")
                if n_flat > 0:
                    print(f"    - Flat tuning curves (CV < {self.config.min_cv_threshold}): {n_flat} cells")
                if n_broad > 0:
                    print(f"    - Broad tuning (BW > {self.config.max_bandwidth_threshold} oct): {n_broad} cells")
                if n_low_tq > 0:
                    print(f"    - Low tuning quality (TQ < {self.config.tuning_quality_threshold}): {n_low_tq} cells")
        
        # Print all three categories
        for category in ['excluded', 'non_tuned', 'tuned']:
            n_cells = np.sum(df['tuning_category'] == category)
            if n_cells > 0 or category == 'excluded':  # Always show excluded count
                denominator = n_total if n_total is not None else len(df)
                pct = 100 * n_cells / denominator if denominator > 0 else 0
                category_display = category.replace('_', ' ').title()
                if category == 'excluded':
                    category_display += ' (Low FR)'
                print(f"  {category_display:25s}: {n_cells:3d} cells ({pct:5.1f}%)")


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
                f'Frequency Tuning Quality - All Sessions Summary\n'
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
        
        # Build summary text line by line
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
    def _plot_metric_distribution(ax, data, metric_name, color, precision=2):
        """Plot histogram distribution of a metric."""
        valid_data = data.dropna()
        
        if len(valid_data) == 0:
            ax.text(0.5, 0.5, 'No valid data', ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title(metric_name, fontsize=11, fontweight='bold')
            return
        
        ax.hist(valid_data, bins=30, color=color, alpha=0.7, edgecolor='black')
        ax.axvline(valid_data.mean(), color='red', linestyle='--', linewidth=2,
                  label=f'Mean = {valid_data.mean():.{precision}f}')
        ax.axvline(valid_data.median(), color='orange', linestyle='--', linewidth=2,
                  label=f'Median = {valid_data.median():.{precision}f}')
        
        ax.set_xlabel(metric_name, fontsize=10)
        ax.set_ylabel('Count', fontsize=10)
        ax.set_title(f'{metric_name} Distribution', fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')
    
    @staticmethod
    def _plot_scatter(ax, df, x_col, y_col, x_label, y_label):
        """Plot scatter of two metrics."""
        # Remove NaN values
        valid_mask = ~(np.isnan(df[x_col]) | np.isnan(df[y_col]))
        df_valid = df[valid_mask]
        
        if len(df_valid) == 0:
            ax.text(0.5, 0.5, 'No valid data', ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title(f'{x_label} vs {y_label}', fontsize=11, fontweight='bold')
            return
        
        ax.scatter(df_valid[x_col], df_valid[y_col], alpha=0.6, s=50, c='blue', edgecolor='black')
        ax.set_xlabel(x_label, fontsize=10)
        ax.set_ylabel(y_label, fontsize=10)
        ax.set_title(f'{x_label} vs {y_label}', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    @staticmethod
    def _format_session_title(session, laser_condition, n_cells, n_excluded, n_total, suffix):
        """Format session title string."""
        pct_excluded = 100 * n_excluded / n_total if n_total > 0 else 0
        pct_analyzed = 100 * n_cells / n_total if n_total > 0 else 0
        
        return (
            f"Frequency Tuning {suffix} - LASER {laser_condition}\n"
            f"{session.subject} {session.date} depth={session.depth}µm | "
            f"Analyzed: {n_cells}/{n_total} cells ({pct_analyzed:.1f}%) | "
            f"Excluded: {n_excluded} ({pct_excluded:.1f}%)"
        )


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
        n_trials = len(session_data.bdata['currentFreq'])
        
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
    print("FREQUENCY TUNING QUALITY METRICS - ALL SESSIONS")
    print("="*60)
    
    # Initialize configuration
    config = AnalysisConfig()
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
    
    # Generate all-sessions summary plots
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
