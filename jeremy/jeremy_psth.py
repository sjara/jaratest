"""
Some utility functions for making a PSTH
"""

import numpy as np

def fix_stimuli_number_mismatch(bdata, my_key, neuropixels_event_onset_times):
    """
    Ensures that the lengths of behavioral data and zeroed event onset times match.

    If there is a mismatch where the neuropixels_event_onset_times list has one extra element
    compared to the behavioral data, it trims the excess element from neuropixels_event_onset_times.
    Then it asserts that the lengths are equal, raising an error if they still do not match.

    Parameters:
        bdata (dict): A dictionary containing behavioral data.
        my_key (str): The key of interest in `bdata`.
        neuropixels_event_onset_times (list): A list of zeroed event onset times.

    Returns:
        list: The corrected `neuropixels_event_onset_times` list, ensuring lengths match.

    Raises:
        AssertionError: If the lengths of the behavioral data and onset times do not match.
    """
    if len(bdata[my_key]) == len(neuropixels_event_onset_times) - 1:
        neuropixels_event_onset_times = neuropixels_event_onset_times[:len(bdata[my_key])]
    
    assert len(bdata[my_key]) == len(neuropixels_event_onset_times), (
        'Number of trials in behavior and ephys do not match'
    )

    return neuropixels_event_onset_times

def collect_psth_events(bdata, modality, stims_of_interest):
    '''
    Collects indices of all listed stims for a specific modality within bdata.
    
    Parameters:
        bdata (dict): A dictionary containing behavioral data.
        modality (str): The key in `bdata` corresponding to the modality of interest.
        stims_of_interest (list): A list of stimulus types within a specified modality.
    
    Returns:
        list: A sorted numpy array of bdata[modality] indices corresponding to our stims of interest
    '''

    ## Start pulling available stimuli irrespective of our previous results
    chosen_events = np.sort(np.hstack([np.argwhere(bdata[modality]==soi).T[0] for soi in stims_of_interest]))
    return chosen_events

def collect_window(my_data, chosen_index, lower, higher):
    '''
    Collects a window of data around a specified timestamp from the input dataset.
    Also returns a dictionary with information on whether the extracted window is of valid length.

    Parameters:
        my_data (ndarray): A 2D array containing the data to extract the window from.
        chosen_index (int): The central index around which the data window is collected.
        lower (int): The number of data points to include before the chosen_index.
        higher (int): The number of data points to include after the chosen_index.

    Returns:
        tuple:
            - collected_window (ndarray): A slice of the data around the chosen timestamp,
              with a range of indices from (chosen_index - lower) to (chosen_index + higher).
            - outcome (dict): A dictionary containing:
                - "valid_length" (bool): Indicates whether the collected window has the expected length
                  of lower + higher + 1.
                - "chosen_index" (int): The input chosen timestamp for reference.
                - "lower" (int): The lower offset used.
                - "higher" (int): The higher offset used.
    '''
    collected_window = (my_data)[max(chosen_index-lower,0):chosen_index+higher+1,:]

    valid_length = True
    if len(collected_window)!=lower+higher+1:
        valid_length = False

    outcome = {"valid_length": valid_length, "chosen_index": chosen_index, "lower": lower, "higher": higher, "length": len(my_data)}

    return collected_window, outcome

def fill_invalid_window(my_window, collection_outcome, fill_value=np.nan):
    """
    Extends a window with specified fill values (e.g., np.nan) at the upper and lower ends
    based on the given collection outcome.

    Parameters:
    - my_window: The original window data, which may be smaller in size than intended.
    - collection_outcome: A dictionary containing the outcome and additional information.
        Keys:
            - "outcome" (bool): Whether the window size was invalid.
            - "chosen_timestamp" (int): A specific timestamp chosen.
            - "lower" (int): Lower bound on the window.
            - "higher" (int): Upper bound on the window.
            - "length" (int): The number of timepoints in the dataset.
    - fill_value: The value to use for filling the upper and lower extensions. Default is np.nan.

    Returns:
    - my_window: The extended window with fill values added to the upper and lower ends.
    """
    
    if not collection_outcome["valid_length"]:
        chosen_timestamp = collection_outcome["chosen_index"]
        lower = collection_outcome["lower"]
        higher = collection_outcome["higher"]
        length = collection_outcome["length"]

        print(f"Fixing window at timestamp [{chosen_timestamp}]")

        # Calculate the number of elements to add to the lower and upper parts
        add_to_lower = max(lower - chosen_timestamp, 0)
        add_to_upper = max(higher + chosen_timestamp - length + 1, 0) ## Todo: Double check that I should be adding 1 here

        lower_fill = np.full((add_to_lower,) + my_window.shape[1:], fill_value)
        upper_fill = np.full((add_to_upper,) + my_window.shape[1:], fill_value)

        my_window = np.concatenate((lower_fill, my_window, upper_fill))

    return my_window

def get_psth_uncollapsed(my_data, dataTimeStamps, eventOnsetTimes, trials, psth_upper, psth_lower, fill_overextended_windows=True):
    '''
    Collects windows of specified size given 
    
    Parameters:
        data (numpy array): array of any size. First dimension must have length=len(dataTimeStamps).
        dataTimeStamps (numpy array): array of timestamps corresponding to data. Used here to relate back to eventOnsetTimes.
        eventOnsetTimes (numpy array): a 1d array of all stimuli incident timings aligned with dataTimeStamps.
        trials (array): an array of boolean values (# trials) indicating whether to extract a window at the corresponding index within eventOnsetTimes
        psth_upper (int): Collect 100 datapoints BEYOND stimulus onset
        psth_lower (int): Collect 100 datapoints BEFORE stimulus onset
        fill_overextended_windows (bool): Option to fill window(s) with np.nan if psth_upper or psth_lower extend beyond available data relative to a chosen event.
    
    Returns:
        numpy array: an array of shape (N, )
    '''
    
    psth_uncollapsed = []
    collection_outcome_list = []

    # Select indices that correspond to events of interest.
    ChosenIndex_list = eventOnsetTimes[np.argwhere(trials==True)]-dataTimeStamps[0]

    # Cycle through the indices and grab windows of chosen size.
    for grab_index in ChosenIndex_list:
        collected_window, collection_outcome = collect_window(my_data, grab_index[0], psth_lower, psth_upper)

        if fill_overextended_windows:
            collected_window = fill_invalid_window(collected_window, collection_outcome, fill_value=np.nan)

        collection_outcome_list.append(collection_outcome)
        psth_uncollapsed.append(collected_window)

    psth_uncollapsed = np.array(psth_uncollapsed)
    
    return psth_uncollapsed, collection_outcome_list

def time_to_indices(time_difference, sampleRate, time_difference_units='s'):
    '''
    Parameters:
        time_difference (float): Time elapsed to convert to samples elapsed.
        sample_rate (int): Sampling rate (hz).
        time_difference_units (str): Assumed input time units. Can be 's', 'ms', 'us'.

    Returns:
        int: Nearest number of samples encompassing the requested time difference.
    '''

    unit_conversion = {'s': 1, 'ms': 1e-3, 'us': 1e-6}
    
    if time_difference_units not in unit_conversion:
        raise ValueError("time_difference_units must be 's', 'ms', or 'us'.")

    time_in_seconds = time_difference * unit_conversion[time_difference_units]
    sample_count = round(time_in_seconds * sampleRate)

    return sample_count