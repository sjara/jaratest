"""
Generalized raster plot generator for neural recordings with multiple stimulus paradigms.

This refactored version separates concerns into modular, reusable components:
- Configuration management
- Data loading and processing
- Plotting functions
- Main execution logic

Supports:
- AM tuning, Frequency tuning, Natural sound categories/instances
- Laser ON/OFF comparison
- Color-coded stimulus visualization
- Configurable category mappings
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings, celldatabase, ephyscore, behavioranalysis, loadneuropix, extraplots
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any

# Turn off interactive plotting
plt.ioff()

# =============================================================================
# CONFIGURATION CLASSES
# =============================================================================

@dataclass
class CategoryConfig:
    """Configuration for stimulus category visualization."""
    names: List[str]
    base_colors: List[str]
    instances_per_category: int = 4
    brightness_factors: List[float] = field(default_factory=lambda: [0.5, 0.7, 0.85, 1.0])
    
    def get_category_info(self, stimulus_id: int) -> Tuple[str, int, str, int]:
        """
        Get category name, instance number, color, and index for a stimulus ID.
        
        Args:
            stimulus_id: The stimulus identifier
            
        Returns:
            Tuple of (category_name, instance_num, color_hex, category_index)
        """
        category_idx = int(stimulus_id) // self.instances_per_category
        instance_num = int(stimulus_id) % self.instances_per_category
        
        if category_idx < len(self.names):
            category_name = self.names[category_idx]
            base_color = self.base_colors[category_idx]
            
            # Apply brightness factor for this instance
            factor = self.brightness_factors[instance_num]
            rgb = tuple(int(base_color[i:i+2], 16) for i in (1, 3, 5))
            adjusted_rgb = tuple(int(c * factor) for c in rgb)
            color = '#{:02x}{:02x}{:02x}'.format(*adjusted_rgb)
            
            return category_name, instance_num, color, category_idx
        else:
            return 'Unknown', instance_num, '#000000', -1


@dataclass
class PlotConfig:
    """Configuration for plot layout and appearance."""
    n_rows: int = 3
    n_cols: int = 5
    fig_size: List[float] = field(default_factory=lambda: [25, 18])
    shank_mapping: List[int] = field(default_factory=lambda: [0, 0, 1, 1, 2, 2, 3, 3])
    spike_marker_size: float = 1
    laser_line_width: float = 2.5
    laser_line_style: str = '--'
    laser_line_color: str = 'red'
    laser_line_alpha: float = 0.8
    shading_alpha_tuning: float = 0.4
    shading_alpha_natural: float = 0.2
    save_dpi: int = 200
    # Shank filtering: [0,1,2,3] = process each shank separately (DEFAULT)
    # Set to None to plot all shanks together (original behavior)
    # Or specify subset like [0,2] to only process shanks 0 and 2
    shank_filter: Optional[List[int]] = None #field(default_factory=lambda: [0, 1, 2, 3])


@dataclass
class SessionConfig:
    """Configuration for a single recording session."""
    subject: str
    date: str
    depth: int


@dataclass
class CaseConfig:
    """Configuration for a stimulus paradigm case."""
    name: str
    session: str
    stim_key: str
    time_range: List[float]
    is_frequency_based: bool = False
    is_natural_sounds: bool = False


# =============================================================================
# DEFAULT CONFIGURATIONS
# =============================================================================

# Natural sound categories for arch018 dataset
DEFAULT_CATEGORY_CONFIG = CategoryConfig(
    names=['Croaking', 'Insect', 'Streamside', 'Bubbling', 'Bees'],
    base_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
)

# Session configurations
SESSIONS = {
    0: SessionConfig('arch022', '2025-03-13', 2780),
    1: SessionConfig('arch022', '2025-03-13', 3500),
    2: SessionConfig('arch022', '2025-03-14', 2780),
    3: SessionConfig('arch022', '2025-03-14', 3500),
    4: SessionConfig('arch022', '2025-03-17', 2780),
    5: SessionConfig('arch022', '2025-03-17', 3500),
}

# Paradigm configurations
CASES = {
    0: CaseConfig('optoTuningAM', 'optoTuningAM', 'currentFreq', [-0.5, 1], is_frequency_based=True),
    1: CaseConfig('optoTuningFreq', 'optoTuningFreq', 'currentFreq', [-0.5, 1], is_frequency_based=True),
    2: CaseConfig('optoNatCateg', 'optoNaturalCategories', 'soundID', [-2, 6], is_natural_sounds=True),
    3: CaseConfig('optoNatIns', 'optoNaturalInstances', 'soundID', [-2, 6], is_natural_sounds=True),
}

PLOT_CONFIG = PlotConfig()

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_session_data(session: SessionConfig, case: CaseConfig) -> Tuple[Any, Any, Any, Any]:
    """
    Load cell database and behavioral data for a session/case combination.
    
    Args:
        session: Session configuration
        case: Case configuration
        
    Returns:
        Tuple of (celldb_subset, ephys_data, behavioral_data, ensemble)
    """
    inforec_file = os.path.join(settings.INFOREC_PATH, f'{session.subject}_inforec.py')
    celldb = celldatabase.generate_cell_database(inforec_file, ignoreMissing=True)
    celldb_subset = celldb[(celldb.date == session.date) & (celldb.pdepth == session.depth)]
    
    if len(celldb_subset) == 0:
        raise ValueError(f"No cells found for {session.subject} {session.date} {session.depth}um")
    
    # Add shank classification
    celldb_subset = add_shank_classification(celldb_subset, session)
    
    # Load ephys and behavioral data
    ensemble = ephyscore.CellEnsemble(celldb_subset)
    ephys_data, bdata = ensemble.load(case.session)
    
    return celldb_subset, ephys_data, bdata, ensemble


def add_shank_classification(celldb: Any, session: SessionConfig) -> Any:
    """Add shank number to each cell based on probe geometry."""
    sessions_root = os.path.join(settings.EPHYS_NEUROPIX_PATH, session.subject)
    multisession_dir = os.path.join(sessions_root, f'multisession_{session.date}_{session.depth}um_processed')
    
    one_cell = celldb.iloc[0]
    ephys_times = one_cell.ephysTime
    session_name = f'{one_cell.date}_{ephys_times[0]}'
    xml_path = os.path.join(multisession_dir, session_name, 'info', 'settings.xml')
    
    pmap = loadneuropix.ProbeMap(xml_path)
    possible_xpos = np.unique(pmap.xpos)
    
    shank_list = []
    for idx, cell in celldb.iterrows():
        ch = cell.bestChannel
        xpos = pmap.xpos[int(ch)]
        ind_possible_xpos = np.where(possible_xpos == xpos)[0][0]
        shank_list.append(PLOT_CONFIG.shank_mapping[ind_possible_xpos])
    
    celldb = celldb.copy()
    celldb['shank'] = shank_list
    return celldb


def prepare_spike_data(ensemble: Any, ephys_data: Any, bdata: Any, case: CaseConfig) -> Dict[str, Any]:
    """
    Prepare spike times and trial information.
    
    Returns:
        Dictionary with spike times, trial indices, stimulus info, etc.
    """
    current_stim = bdata[case.stim_key]
    n_trials = len(current_stim)
    event_onset_times = ephys_data['events']['stimOn']
    
    if len(current_stim) == len(event_onset_times) - 1:
        event_onset_times = event_onset_times[:n_trials]
    
    spike_times_all, trial_index_all, index_limits_all = ensemble.eventlocked_spiketimes(
        event_onset_times, case.time_range)
    
    possible_stim = np.unique(current_stim)
    trials_each_cond = behavioranalysis.find_trials_each_type(current_stim, possible_stim)
    cond_each_sorted_trial, sorted_trials = np.nonzero(trials_each_cond.T)
    sorting_inds = np.argsort(sorted_trials)
    
    return {
        'spike_times_all': spike_times_all,
        'trial_index_all': trial_index_all,
        'index_limits_all': index_limits_all,  # Add this for extraplots.raster_plot
        'current_stim': current_stim,
        'possible_stim': possible_stim,
        'trials_each_cond': trials_each_cond,
        'sorting_inds': sorting_inds,
        'n_trials': n_trials
    }


# =============================================================================
# TRIAL ORDERING FUNCTIONS
# =============================================================================

def prepare_laser_trial_order(current_stim: np.ndarray, possible_stim: np.ndarray, 
                              laser_trials: np.ndarray) -> Tuple[np.ndarray, Dict[int, int], np.ndarray, np.ndarray]:
    """
    Create trial ordering that groups by stimulus within each laser condition.
    
    Args:
        current_stim: Stimulus ID for each trial
        possible_stim: Unique stimulus IDs
        laser_trials: Boolean array indicating laser ON trials
        
    Returns:
        Tuple of (trial_order, trial_map, off_trials, on_trials)
    """
    # More efficient: use boolean indexing instead of np.where + list comprehension
    off_trials = np.flatnonzero(laser_trials == 0)
    on_trials = np.flatnonzero(laser_trials == 1)
    
    # Sort trials by stimulus within each laser condition
    off_trials_by_stim = []
    on_trials_by_stim = []
    
    for stim in possible_stim:
        stim_mask = (current_stim == stim)
        off_trials_by_stim.extend(off_trials[stim_mask[off_trials]])
        on_trials_by_stim.extend(on_trials[stim_mask[on_trials]])
    
    trial_order = np.concatenate([off_trials_by_stim, on_trials_by_stim])
    trial_map = {trial: i for i, trial in enumerate(trial_order)}
    
    return trial_order, trial_map, off_trials, on_trials


# =============================================================================
# PLOTTING HELPER FUNCTIONS
# =============================================================================

def plot_colored_spikes(ax: plt.Axes, spike_times: np.ndarray, trial_inds: np.ndarray, 
                       sorted_trial_inds: np.ndarray, current_stim: np.ndarray, 
                       possible_stim: np.ndarray, category_config: CategoryConfig):
    """Plot spikes with colors based on stimulus category."""
    for stim_id in possible_stim:
        _, _, color, _ = category_config.get_category_info(stim_id)
        trials_this_stim = np.where(current_stim == stim_id)[0]
        spikes_this_stim = np.isin(trial_inds, trials_this_stim)
        
        if spikes_this_stim.sum() > 0:
            ax.plot(spike_times[spikes_this_stim], sorted_trial_inds[spikes_this_stim], 
                   '.', ms=PLOT_CONFIG.spike_marker_size, color=color)


def add_background_shading(ax: plt.Axes, possible_stim: np.ndarray, trials_each_cond: np.ndarray,
                          trial_mapping: np.ndarray, is_natural_sounds: bool,
                          category_config: Optional[CategoryConfig] = None):
    """Add alternating background shading to distinguish stimulus groups."""
    alpha = PLOT_CONFIG.shading_alpha_natural if is_natural_sounds else PLOT_CONFIG.shading_alpha_tuning
    
    for i, stim in enumerate(possible_stim):
        # Determine shading pattern
        if is_natural_sounds and category_config:
            _, _, _, category_idx = category_config.get_category_info(stim)
            should_shade = (category_idx % 2 == 1)
        else:
            should_shade = (i % 2 == 1)
        
        if should_shade:
            trials_this_cond = trials_each_cond[:, i] if trials_each_cond.ndim > 1 else trials_each_cond
            if trials_this_cond.sum() > 0:
                cond_trial_inds = np.where(trials_this_cond)[0]
                sorted_inds = trial_mapping[cond_trial_inds]
                
                if len(sorted_inds) > 0:
                    ymin = np.min(sorted_inds) - 0.5
                    ymax = np.max(sorted_inds) + 0.5
                    ax.axhspan(ymin, ymax, facecolor='lightgray', alpha=alpha, zorder=-10)


def get_ytick_locations_simple(trials_each_cond: np.ndarray, sorting_inds: np.ndarray, 
                               possible_stim: np.ndarray) -> List[float]:
    """Calculate y-tick locations for simple (non-laser) plots."""
    ytick_locs = []
    for i in range(len(possible_stim)):
        trials_this_cond = trials_each_cond[:, i]
        if trials_this_cond.sum() > 0:
            cond_trial_inds = np.where(trials_this_cond)[0]
            sorted_cond_inds = sorting_inds[cond_trial_inds]
            ytick_locs.append(np.median(sorted_cond_inds))
    return ytick_locs


def get_ytick_locations_laser(current_stim: np.ndarray, possible_stim: np.ndarray,
                              trial_map: Dict[int, int], off_trials: np.ndarray, 
                              on_trials: np.ndarray) -> Tuple[List[Optional[float]], List[Optional[float]]]:
    """Calculate separate y-tick locations for laser OFF and ON conditions."""
    yticks_off = []
    yticks_on = []
    
    for stim in possible_stim:
        stim_trials = np.where(current_stim == stim)[0]
        
        # OFF trials
        stim_off_trials = [t for t in stim_trials if t in off_trials]
        if len(stim_off_trials) > 0:
            mapped_inds = [trial_map[t] for t in stim_off_trials if t in trial_map]
            yticks_off.append(np.median(mapped_inds) if len(mapped_inds) > 0 else None)
        else:
            yticks_off.append(None)
        
        # ON trials
        stim_on_trials = [t for t in stim_trials if t in on_trials]
        if len(stim_on_trials) > 0:
            mapped_inds = [trial_map[t] for t in stim_on_trials if t in trial_map]
            yticks_on.append(np.median(mapped_inds) if len(mapped_inds) > 0 else None)
        else:
            yticks_on.append(None)
    
    return yticks_off, yticks_on


# =============================================================================
# AXIS LABELING FUNCTIONS
# =============================================================================

def hide_alternating_labels(ax: plt.Axes, start_index: int = 1) -> None:
    """
    Hide every other y-tick label to reduce clutter.
    
    Args:
        ax: Matplotlib axes object
        start_index: Index to start hiding (default=1 hides odd indices)
    """
    for i, label in enumerate(ax.get_yticklabels()):
        if i % 2 == start_index:
            label.set_visible(False)


def format_stimulus_labels(case_id: int, possible_stim: np.ndarray, 
                          category_config: CategoryConfig) -> Tuple[List[str], List[str]]:
    """
    Generate labels and colors for y-axis based on stimulus type.
    
    Returns:
        Tuple of (labels, colors)
    """
    if case_id == 0:  # AM tuning
        labels = [f'{int(r)}' for r in possible_stim]
        colors = ['black'] * len(labels)
    elif case_id == 1:  # Frequency tuning
        freqs_khz = np.round(possible_stim / 1000, 2)
        labels = [f'{fk}' for fk in freqs_khz]
        colors = ['black'] * len(labels)
    elif case_id == 2:  # Natural categories
        labels = [category_config.get_category_info(sid)[0] for sid in possible_stim]
        colors = [category_config.base_colors[int(sid) // category_config.instances_per_category] 
                 for sid in possible_stim]
    else:  # case_id == 3: Natural instances
        labels = []
        colors = []
        for sid in possible_stim:
            cat_name, inst_num, color, _ = category_config.get_category_info(sid)
            labels.append(f'{cat_name} {inst_num}')
            colors.append(color)
    
    return labels, colors


def apply_yaxis_labels_simple(ax: plt.Axes, case_id: int, ytick_locs: List[float],
                              possible_stim: np.ndarray, category_config: CategoryConfig):
    """Apply y-axis labels for non-laser plots."""
    labels, colors = format_stimulus_labels(case_id, possible_stim, category_config)
    
    if len(ytick_locs) > 0:
        ax.set_yticks(ytick_locs, labels, minor=False)
        
        # Color labels if needed
        if case_id in [2, 3]:
            for tick, color in zip(ax.get_yticklabels(), colors):
                tick.set_color(color)
                tick.set_fontweight('bold')
        
        fontsize = 6 if case_id == 3 else 7
        ax.tick_params(axis='y', labelsize=fontsize)


def apply_yaxis_labels_laser(ax: plt.Axes, case_id: int, yticks_off: List[Optional[float]],
                            yticks_on: List[Optional[float]], possible_stim: np.ndarray,
                            category_config: CategoryConfig):
    """Apply separate y-axis labels for laser OFF and ON conditions."""
    labels, colors = format_stimulus_labels(case_id, possible_stim, category_config)
    
    # Place OFF labels
    for ytick, label, color in zip(yticks_off, labels, colors):
        if ytick is not None:
            fontsize = 6 if case_id == 3 else 7
            fontweight = 'bold' if case_id in [2, 3] else 'normal'
            ax.text(-0.15, ytick, label, transform=ax.get_yaxis_transform(),
                   ha='right', va='center', fontsize=fontsize, color=color, fontweight=fontweight)
    
    # Place ON labels (smaller font for AM/Freq tuning)
    for ytick, label, color in zip(yticks_on, labels, colors):
        if ytick is not None:
            # Smaller font for ON labels in AM and Freq tuning cases
            if case_id == 0 or case_id == 1:
                fontsize = 3  # Smaller for AM/Freq above laser line
            else:
                fontsize = 6 if case_id == 3 else 7
            fontweight = 'bold' if case_id in [2, 3] else 'normal'
            ax.text(-0.15, ytick, label, transform=ax.get_yaxis_transform(),
                   ha='right', va='center', fontsize=fontsize, color=color, fontweight=fontweight)
    
    ax.set_yticks([])  # Hide default ticks


def get_ylabel(case_id: int) -> str:
    """Get appropriate y-axis label for case."""
    ylabel_map = {
        0: 'AM rate (Hz)',
        1: 'Tone Frequency (kHz)',
        2: 'Sound Category',
        3: 'Sound (Category Instance)'
    }
    return ylabel_map.get(case_id, 'Stimulus')


# =============================================================================
# MAIN PLOTTING FUNCTION
# =============================================================================

def plot_single_cell_raster(ax: plt.Axes, cell_idx: int, spike_data: Dict[str, Any],
                           case: CaseConfig, case_id: int, bdata: Any, shank_num: Any,
                           category_config: CategoryConfig = DEFAULT_CATEGORY_CONFIG):
    """
    Plot raster for a single cell.
    
    Args:
        ax: Matplotlib axes object
        cell_idx: Index of cell to plot
        spike_data: Dictionary with spike times and trial info
        case: Case configuration
        case_id: Case identifier (0-3)
        bdata: Behavioral data
        shank_num: Shank number for this cell
        category_config: Category configuration for natural sounds
    """
    spike_times = spike_data['spike_times_all'][cell_idx]
    trial_inds = spike_data['trial_index_all'][cell_idx]
    index_limits = spike_data['index_limits_all'][cell_idx]
    current_stim = spike_data['current_stim']
    possible_stim = spike_data['possible_stim']
    trials_each_cond = spike_data['trials_each_cond']
    sorting_inds = spike_data['sorting_inds']
    
    # Check for laser trials
    has_laser = 'laserTrial' in bdata
    
    if has_laser:
        laser_trials = bdata['laserTrial']
        
        # For frequency-based plots, use extraplots.raster_plot with laser grouping
        if case.is_frequency_based:
            # Prepare trials grouped by laser condition (OFF first, then ON)
            off_trials = np.flatnonzero(laser_trials == 0)
            on_trials = np.flatnonzero(laser_trials == 1)
            
            # Build trialsEachCond with laser grouping: [stim1_OFF, stim2_OFF, ..., stim1_ON, stim2_ON, ...]
            trials_each_cond_laser = []
            
            # More efficient: process OFF and ON in one loop
            for stim_idx in range(len(possible_stim)):
                stim_trials = trials_each_cond[:, stim_idx]
                
                # OFF trials for this stimulus
                off_mask = stim_trials.copy()
                off_mask[on_trials] = False
                trials_each_cond_laser.append(off_mask)
            
            for stim_idx in range(len(possible_stim)):
                stim_trials = trials_each_cond[:, stim_idx]
                
                # ON trials for this stimulus
                on_mask = stim_trials.copy()
                on_mask[off_trials] = False
                trials_each_cond_laser.append(on_mask)
            
            trials_each_cond_laser = np.column_stack(trials_each_cond_laser)
            
            # Generate alternating colors
            n_cond = len(possible_stim)
            color_each_cond = (['0.5', '0.75'] * int(np.ceil(n_cond / 2.0)))[:n_cond]
            # Repeat for laser ON conditions
            color_each_cond = color_each_cond + color_each_cond
            
            # Format labels (OFF conditions, then ON conditions)
            labels, _ = format_stimulus_labels(case_id, possible_stim, category_config)
            labels_laser = labels + labels  # Duplicate for OFF and ON
            
            # Use jaratoolbox's raster_plot
            pRaster, hcond, zline = extraplots.raster_plot(
                spike_times, index_limits, case.time_range,
                trialsEachCond=trials_each_cond_laser, colorEachCond=color_each_cond, labels=labels_laser)
            plt.setp(pRaster, ms=PLOT_CONFIG.spike_marker_size)
            
            # Hide every other label to reduce clutter
            hide_alternating_labels(ax)
            
            # Add laser separator line
            n_off = len(off_trials)
            n_on = len(on_trials)
            # Find the boundary between OFF and ON conditions
            cumsum_trials = np.cumsum([trials_each_cond_laser[:, i].sum() for i in range(n_cond)])
            laser_boundary = cumsum_trials[-1] - 0.5
            
            ax.axhline(laser_boundary, color=PLOT_CONFIG.laser_line_color, 
                      linewidth=PLOT_CONFIG.laser_line_width, 
                      linestyle=PLOT_CONFIG.laser_line_style,
                      alpha=PLOT_CONFIG.laser_line_alpha, zorder=10)
            
            # Minor ticks for laser labels
            total_trials = trials_each_cond_laser.sum()
            yticks_minor = [laser_boundary/2, laser_boundary + (total_trials - laser_boundary)/2]
            ax.set_yticks(yticks_minor, ['laser OFF', 'laser ON'], minor=True)
            ax.tick_params(axis='y', which='minor', left=False, right=True, 
                          labelleft=False, labelright=True, labelsize=8, pad=2)
        
        else:
            # Natural sounds with laser - use original colored spike plotting
            trial_order, trial_map, off_trials, on_trials = prepare_laser_trial_order(
                current_stim, possible_stim, laser_trials)
            
            sorted_trial_inds = np.array([trial_map[t] for t in trial_inds])
            
            plot_colored_spikes(ax, spike_times, trial_inds, sorted_trial_inds, 
                              current_stim, possible_stim, category_config)
            
            n_off = len(off_trials)
            n_on = len(on_trials)
            ax.set_ylim([-2, n_off + n_on + 1])
            
            # Background shading
            add_background_shading(ax, possible_stim, trials_each_cond, 
                                  np.array([trial_map.get(i, -1) for i in range(len(current_stim))]),
                                  case.is_natural_sounds, category_config)
            
            # Laser separator line
            ax.axhline(n_off - 0.5, color=PLOT_CONFIG.laser_line_color, 
                      linewidth=PLOT_CONFIG.laser_line_width, 
                      linestyle=PLOT_CONFIG.laser_line_style,
                      alpha=PLOT_CONFIG.laser_line_alpha, zorder=10)
            
            # Y-axis labels
            yticks_off, yticks_on = get_ytick_locations_laser(current_stim, possible_stim, 
                                                              trial_map, off_trials, on_trials)
            apply_yaxis_labels_laser(ax, case_id, yticks_off, yticks_on, possible_stim, category_config)
            
            # Minor ticks for laser labels
            yticks_minor = [max(n_off/2-1, 0), n_off + max(n_on/2-1, 0)]
            ax.set_yticks(yticks_minor, ['laser OFF', 'laser ON'], minor=True)
            ax.tick_params(axis='y', which='minor', left=False, right=True, 
                          labelleft=False, labelright=True, labelsize=8, pad=2)
    
    else:
        # Non-laser plotting  
        # Use extraplots.raster_plot for AM/Freq tuning (better alternating colors)
        if case.is_frequency_based:
            # Generate alternating colors for AM/Freq tuning
            n_cond = len(possible_stim)
            color_each_cond = ['0.5', '0.75'] * int(np.ceil(n_cond / 2.0))
            
            # Format labels
            labels, _ = format_stimulus_labels(case_id, possible_stim, category_config)
            
            # Use jaratoolbox's raster_plot for clean alternating colors
            pRaster, hcond, zline = extraplots.raster_plot(
                spike_times, index_limits, case.time_range,
                trialsEachCond=trials_each_cond, colorEachCond=color_each_cond, labels=labels)
            plt.setp(pRaster, ms=PLOT_CONFIG.spike_marker_size)
            
            # Show every other label to reduce clutter
            hide_alternating_labels(ax)
            
        elif case.is_natural_sounds:
            sorted_trial_inds = sorting_inds[trial_inds]
            plot_colored_spikes(ax, spike_times, trial_inds, sorted_trial_inds,
                              current_stim, possible_stim, category_config)
            ax.set_ylim([-1, np.max(sorted_trial_inds) + 1])
            
            # Background shading for natural sounds
            add_background_shading(ax, possible_stim, trials_each_cond, sorting_inds,
                                  case.is_natural_sounds, category_config)
            
            # Y-axis labels for natural sounds
            ytick_locs = get_ytick_locations_simple(trials_each_cond, sorting_inds, possible_stim)
            apply_yaxis_labels_simple(ax, case_id, ytick_locs, possible_stim, category_config)
    
    # Common elements
    ax.set_xlabel('Time (s)', fontsize=8, labelpad=8)
    ax.set_ylabel(get_ylabel(case_id), fontsize=8)
    ax.set_title(f'Cell {cell_idx} (Shank {shank_num})', fontsize=9, pad=10)
    ax.set_xlim(case.time_range)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def process_session_case(session_id: int, case_id: int, output_dir: str, 
                        save_figs: bool = True, shank_filter: Optional[List[int]] = None) -> Optional[str]:
    """
    Process a single session/case combination and generate plots.
    
    Args:
        session_id: Session identifier
        case_id: Case identifier
        output_dir: Directory to save figures
        save_figs: Whether to save figures to disk
        shank_filter: Optional list of shanks to include. None = all shanks. 
                     If specified, creates separate output folders per shank.
        
    Returns:
        Error message if failed, None if successful
    """
    try:
        session = SESSIONS[session_id]
        case = CASES[case_id]
        
        # Load data
        celldb_subset, ephys_data, bdata, ensemble = load_session_data(session, case)
        
        # Prepare spike data
        spike_data = prepare_spike_data(ensemble, ephys_data, bdata, case)
        
        # Determine shanks to process
        if shank_filter is None:
            # Process all cells together (original behavior)
            shanks_to_process = [None]  # None means "all shanks"
        else:
            # Process each shank separately
            shanks_to_process = shank_filter
        
        # Process each shank
        for shank_num in shanks_to_process:
            # Filter cells by shank if specified
            if shank_num is None:
                # All shanks
                cells_to_plot = list(range(len(celldb_subset)))
                shank_label = ""
                shank_output_dir = output_dir
            else:
                # Specific shank
                cells_to_plot = [i for i in range(len(celldb_subset)) 
                               if celldb_subset.iloc[i].get('shank', -1) == shank_num]
                shank_label = f"_shank{shank_num}"
                shank_output_dir = os.path.join(output_dir, f'shank{shank_num}')
                
                # Create shank-specific directory if it doesn't exist
                if save_figs and not os.path.exists(shank_output_dir):
                    os.makedirs(shank_output_dir)
                
                # Skip if no cells on this shank
                if len(cells_to_plot) == 0:
                    print(f"  No cells found on shank {shank_num}, skipping...")
                    continue
            
            # Plot in pages
            n_cells = len(cells_to_plot)
            n_pages = int(np.ceil(n_cells / (PLOT_CONFIG.n_rows * PLOT_CONFIG.n_cols)))
            
            for page_idx in range(n_pages):
                fig = plt.figure(figsize=PLOT_CONFIG.fig_size)
                plt.clf()
                
                cells_this_page_idx = np.arange(PLOT_CONFIG.n_rows * PLOT_CONFIG.n_cols) + \
                                page_idx * PLOT_CONFIG.n_rows * PLOT_CONFIG.n_cols
                
                for plot_idx, cell_list_idx in enumerate(cells_this_page_idx):
                    if cell_list_idx >= n_cells:
                        break
                    
                    cell_idx = cells_to_plot[cell_list_idx]
                    shank_num_cell = celldb_subset.iloc[cell_idx].get('shank', 'N/A')
                    ax = plt.subplot(PLOT_CONFIG.n_rows, PLOT_CONFIG.n_cols, plot_idx + 1)
                    
                    plot_single_cell_raster(ax, cell_idx, spike_data, case, case_id, 
                                          bdata, shank_num_cell, DEFAULT_CATEGORY_CONFIG)
                
                # Figure title and layout
                title = f'{session.subject} {session.date} {session.depth}um {case.name}'
                if shank_num is not None:
                    title += f' (Shank {shank_num})'
                title += f' ({page_idx+1}/{n_pages})'
                plt.suptitle(title, fontweight='bold', y=1.02)
                plt.tight_layout(rect=[0, 0.04, 1, 0.97], pad=2.0)
                
                if save_figs:
                    fig_filename = f'{session.subject}_{case.name}_{session.date}_{session.depth}um{shank_label}_{page_idx+1:02d}'
                    extraplots.save_figure(fig_filename, 'png', PLOT_CONFIG.fig_size, 
                                         outputDir=shank_output_dir, facecolor='w', dpi=PLOT_CONFIG.save_dpi)
                    plt.close(fig)
        
        return None  # Success
        
    except Exception as e:
        return str(e)


def main():
    """Main execution function."""
    output_dir = '/data/reports/arch022_rasters/'
    save_figs = True
    
    # NOTE: By default, plots are generated separately for each shank (shanks 0,1,2,3)
    # To plot all shanks together (original behavior), uncomment the line below:
    # PLOT_CONFIG.shank_filter = None
    
    session_ids = list(SESSIONS.keys())
    case_ids = list(CASES.keys())
    
    failures = []
    
    for session_id in session_ids:
        for case_id in case_ids:
            session = SESSIONS[session_id]
            case = CASES[case_id]
            
            print(f"Processing {session.subject} {session.date} {session.depth}um {case.name}...")
            
            error = process_session_case(session_id, case_id, output_dir, save_figs, 
                                        shank_filter=PLOT_CONFIG.shank_filter)
            
            if error:
                if "No cells found" in error:
                    print(f"SKIP: {error}")
                    failures.append((session_id, case_id, 'not spike sorted'))
                else:
                    print(f"FAIL: {error}")
                    failures.append((session_id, case_id, error))
    
    print("\n" + "="*80)
    print("SUMMARY OF FAILURES:")
    print("="*80)
    for session_id, case_id, error in failures:
        session = SESSIONS[session_id]
        case = CASES[case_id]
        print(f"{session.subject} {session.date} {session.depth}um {case.name}: {error}")


if __name__ == '__main__':
    main()
