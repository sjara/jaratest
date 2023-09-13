'''
These functions are used for analysis of oddball sequence data in max's acid mice.
'''



import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import importlib
import datetime
sys.path.append('C:/Users/mdhor/Documents/GitHub/jaratoolbox/')
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis




def load_data(oneCell, session_type, timeRange):

    """
    Loads a session from oneCell accoring to the 'session_type'. Creates variables spikeTimes and eventOnsetTimes and calls the 
    spikesanalysis.eventlocked_spiketimes() function to lock the spikes to the events. Creates the trialsEachCond array according to the frequencies of each trial
    in the bdata. Splits the trialsEachCond variable by its columns to seperate the conditions by standard and oddball. 

    Args:
        oneCell: One cell from your database
        session_type: (str) The session from your inforec you want to load.
        timeRange: (list) The time around the stimulus you want to load. eg: [-0.3, 0.45]
    
    """
    if oneCell.get_session_inds(session_type) != []: #and oneCell.get_session_inds('lowFreq') != []:
        ephysData, bdata = oneCell.load(session_type)  
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']

        frequencies_each_trial = bdata['currentStartFreq']

        # Checks to see if trial count from bdata is the same as trial count from ephys
        if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
            print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
            sys.exit()

        # If the ephys data is 1 more than the bdata, delete the last ephys trial.
        if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
            eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

        (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        array_of_frequencies = np.unique(frequencies_each_trial)
        trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)


        # Extract column and reshape array.
        trialsLowFreq= trialsEachCond[:,0].reshape(-1,1) 
        trialsHighFreq = trialsEachCond[:,1].reshape(-1,1)

        return (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, trialsLowFreq, trialsHighFreq)


def trials_before_oddball(oddballTrials):
        """
        Creates a boolean array of the trials directly before the oddball trials as TRUE

        Args:
            1D boolean array of oddballTrials 
        """
        trialIndexBeforeOddball = np.array(np.flatnonzero(oddballTrials[:,0])) -1
        nTrials = len(oddballTrials)
        trialsBeforeOddball = np.zeros(nTrials, dtype=bool)
        trialsBeforeOddball[trialIndexBeforeOddball]=True
        trialsBeforeOddball = trialsBeforeOddball.reshape(-1,1)

        return (trialsBeforeOddball)

def combine_index_limits(spikeTimesFromEventOnset1, spikeTimesFromEventOnset2, indexLimitsEachTrial1, indexLimitsEachTrial2):
        """
        Combine the spikeTimesFromEventOnset and indexLimitsEachTrial from two sessions.

        Args:
            spikeTimesFromEventOnset1, spikeTimesFromEventOnset2, indexLimitsEachTrial1, indexLimitsEachTrial2
        Returns:
            SpikeTimes, IndexLimits
        """
        stfeo = np.concatenate((spikeTimesFromEventOnset1, spikeTimesFromEventOnset2))
        ilet = np.hstack((indexLimitsEachTrial1, indexLimitsEachTrial2 + len(spikeTimesFromEventOnset1)))

        return (stfeo, ilet)


def combine_trials(trials1, trials2):
        """
        Combine two trial arrays into one 2d array. 

        Args:
            trials1: (np.arry) standard trials before oddball
            trials2: (np.array) oddball trials
        """
        tec1 = np.vstack((trials1, np.zeros(trials2.shape)))
        tec2 = np.vstack((np.zeros(trials1.shape), trials2))
        tec = np.hstack((tec1, tec2))

        return (tec.astype(bool))

def prepare_plots(oneCell, timeRange, sessionType1, sessionType2, timeVec):
    """
    Outdated function. Only kept for old scripts that use it.
    """
    if oneCell.get_session_inds(sessionType2) != []:
        # Load session, lock spikes to event, seperate trials into columns.
        (spikeTimesHigh, trialIndexHigh, indexLimitsHigh, LowStd, HighOdd) = load_data(oneCell, sessionType1, timeRange)
        (spikeTimesLow, trialIndexLow, indexLimitsLow, LowOdd, HighStd) = load_data(oneCell, sessionType2, timeRange)
            

        # Get standard trials before oddball trials
        trialsBeforeOddLowStd = trials_before_oddball(HighOdd)       
        trialsBeforeOddHighStd = trials_before_oddball(LowOdd)
        

        # Combine spike times and index limits of standard and oddball trials.
        (combinedSpikeTimesHigh, combinedIndexLimitsHigh) = combine_index_limits(spikeTimesLow, spikeTimesHigh, indexLimitsLow, indexLimitsHigh)
        (combinedSpikeTimesLow, combinedIndexLimitsLow) = combine_index_limits(spikeTimesHigh, spikeTimesLow, indexLimitsHigh, indexLimitsLow)
        
        
        
        # Combine trials of high freq before oddball and high freq oddball.
        combinedTrialsHigh = combine_trials(trialsBeforeOddHighStd, HighOdd)

        # Combine trials of low freq before oddball and low freq oddball.
        combinedTrialsLow = combine_trials(trialsBeforeOddLowStd, LowOdd)

        # Create spikeCountMat for psth
        spikeCountMatHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeVec)
        spikeCountMatLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesLow, combinedIndexLimitsLow, timeVec)

        return (combinedSpikeTimesHigh, combinedSpikeTimesLow, combinedIndexLimitsHigh, combinedIndexLimitsLow, combinedTrialsHigh, combinedTrialsLow, spikeCountMatHigh, spikeCountMatLow)


def combine_sessions(oneCell, timeRange, sessionType1, sessionType2, timeVec):
    '''Prepares and combines data for plotting peri-stimulus time histograms (PSTHs) of spike counts for a single neuron from two different oddball sessions.
        Seperates trials by stimulus frequency from each session and then combines the same frequencies from both sessions together.

    Args:
        oneCell: A cell object representing a single neuron's data.
        
        timeRange (tuple): A tuple specifying the start and end times of the PSTH relative to a stimulus event.
        
        sessionType1 (str): A string specifying the first session.
        
        sessionType2 (str): A string specifying the second session.
        
        timeVec (numpy.ndarray): A 1D array of time values for the PSTH bins.
    '''
    if oneCell.get_session_inds(sessionType2) != []:
        # Load session, lock spikes to event, seperate trials into columns.
        (spikeTimesHigh, trialIndexHigh, indexLimitsHigh, LowStd, HighOdd) = load_data(oneCell, sessionType1, timeRange)
        (spikeTimesLow, trialIndexLow, indexLimitsLow, LowOdd, HighStd) = load_data(oneCell, sessionType2, timeRange)
            

        # Get standard trials before oddball trials
        trialsBeforeOddLowStd = trials_before_oddball(HighOdd)       
        trialsBeforeOddHighStd = trials_before_oddball(LowOdd)
        

        # Combine spike times and index limits of standard and oddball trials.
        (combinedSpikeTimesHigh, combinedIndexLimitsHigh) = combine_index_limits(spikeTimesLow, spikeTimesHigh, indexLimitsLow, indexLimitsHigh)
        (combinedSpikeTimesLow, combinedIndexLimitsLow) = combine_index_limits(spikeTimesHigh, spikeTimesLow, indexLimitsHigh, indexLimitsLow)
        
        
        
        # Combine trials of high freq before oddball and high freq oddball.
        combinedTrialsHigh = combine_trials(trialsBeforeOddHighStd, HighOdd)

        # Combine trials of low freq before oddball and low freq oddball.
        combinedTrialsLow = combine_trials(trialsBeforeOddLowStd, LowOdd)

        # Create spikeCountMat for psth
        spikeCountMatHigh = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesHigh, combinedIndexLimitsHigh, timeVec)
        spikeCountMatLow = spikesanalysis.spiketimes_to_spikecounts(combinedSpikeTimesLow, combinedIndexLimitsLow, timeVec)

        return (combinedSpikeTimesHigh, combinedSpikeTimesLow, combinedIndexLimitsHigh, combinedIndexLimitsLow, combinedTrialsHigh, combinedTrialsLow, spikeCountMatHigh, spikeCountMatLow)


def create_running_boolean(runStart, runStop, oneCell, sessionType):
    '''
    Returns a boolean that is length of ephys trials that are TRUE when the mouse is running according to arguments runStart and Runstop.
    '''
    ephysData, bdata = oneCell.load(sessionType)

    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']


    # Creates an list of indexs of the trials where the mouse is running.
    selectedTrials = [] #Boolean array of size event
    for start, stop in zip(runStart, runStop):
        selectedTrials.extend([j for j,v in enumerate(eventOnsetTimes) if start <= v <= stop])


        frequencies_each_trial = bdata['currentStartFreq']

    if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
        print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
        sys.exit()

    if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
        eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]


    # Creates a boolean of all the trials where running is TRUE
    ntrials = len(eventOnsetTimes)
    runningBoolean = np.zeros(ntrials, dtype=bool)
    runningBoolean[selectedTrials] = True

    return runningBoolean

def seperate_running_trials(combinedTrialsHigh, combinedRunning):
    '''
    Compares two booleans and creates a new array that returns when both are TRUE. Also inverts the second boolean argument and makes the same comparison and return.

    Args: Two arrays. First array values are kept if second array is TRUE.

    '''

    runningOddball = np.zeros_like(combinedTrialsHigh, dtype=bool)
    runningOddball = np.logical_and(combinedTrialsHigh, combinedRunning)
    nonRunningBoolean = ~combinedRunning
    nonRunningOddball = np.logical_and(combinedTrialsHigh, nonRunningBoolean)            


    return runningOddball, nonRunningOddball

def read_videotimes(videotimesFile):
    '''
    Loads a python module to access its dictionaries and values.

    Arg: path to python module file.

    '''
    spec = importlib.util.spec_from_file_location('videotimes', videotimesFile)
    videotimes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(videotimes)

    return videotimes



def convert_videotimes(videotimes, sessionType):
    '''
    Takes a videotimes dictionary and uses the keys 'runStart' and 'runStop' of 'sessionType' to convert the timestamp strings into seconds.

    Args: loaded python module of the video times, the sessionType you want to convert

    Returns: Two arrays of the startTime and stopTime converted into seconds.
    '''
    start_str = videotimes.__dict__[sessionType]["runStart"]
    stop_str = videotimes.__dict__[sessionType]["runStop"]

    start_sec_arr = []
    for time_str in start_str:
        try:
            start_time = datetime.datetime.strptime(time_str, "%M:%S")
            start_sec = start_time.minute * 60 + start_time.second
            start_sec_arr.append(start_sec)
        except ValueError:
            print("Could not convert the time string into seconds. Check your videoTimes file.")
            exit()

    stop_sec_arr = []
    for time_str in stop_str:
        try:
            stop_time = datetime.datetime.strptime(time_str, "%M:%S")
            stop_sec = stop_time.minute * 60 + stop_time.second
            stop_sec_arr.append(stop_sec)
        except ValueError:
            print("Could not convert the time string into seconds. Check your videoTimes file.")
            exit()

    return (start_sec_arr, stop_sec_arr)


def create_labels(trialsEachCond):
    '''
    Takes a boolean of trials of each condition and counts the length of TRUE trials for each of the conditions.
    Used to make labels for standard vs oddball PSTH plots.

    Args: 2D boolean array

    Returns: String of text with trial count
    '''
    standardTrials= trialsEachCond[:,0].sum()
    oddballTrials= trialsEachCond[:,1].sum()
    labels = (f'Standard ({standardTrials})', f"Oddball ({oddballTrials})")

    return labels





    time_obj = datetime.datetime.strptime(time_str, '%M:%S')  # convert to datetime object
    seconds = (time_obj - datetime.datetime(1900, 1, 1)).total_seconds()  # convert to total seconds
    print(seconds)  # output: 75.0


def compare_trial_count(trials1, trials2):
    """
    Compares and matches the length of two trial arrays.
    """

    trials1Matched = trials1
    trials2Matched = trials2
    
    if len(trials1) > len(trials2):
        #diff = abs(len(trials1) - len(trials2))
        trials1Matched = trials1[:len(trials2)]
    if len(trials2) > len(trials1):
        #diff = abs(len(trials2) - len(trials1))
        trials2Matched = trials2[:len(trials1)]

    return trials1Matched, trials2Matched


def find_sync_light_onsets(sync_light, invert=True, fixmissing=False, prepost=False):
    """
    Find the onsets in the array representing the synchronization light.
    This function assumes the onsets are periodic (with randomness within 0.5T and 1.5T).
    The function can also fix missing onsets.

    Args:
        sync_light (np.array): array representing the synchronization light trace.
                               Values when the light is on are usually lower than baseline,
                               so use invert=True to invert the trace if needed.
        invert (bool): if True, the sync_light trace is inverted before processing.
        fixmissing (bool): if True, missing onsets are added to the output.
        prepost (bool): if True, assume there is a pre and post pulse of longer duration,
                        and ignore these in the final list.

    Returns:
        fixed_sync_light_onset (np.array): array of booleans indicating the onsets.
    """
    PRE_POST_DURATION_THRESHOLD = 20  # In units of frames. HARCODED! (should be calculated)

    # -- Find changes in synch light --
    sync_light_diff = np.diff(sync_light, prepend=sync_light[0])
    if invert:
        sync_light_diff = -sync_light_diff

    sync_light_threshold = 0.2*np.abs(sync_light_diff).max()
    sync_light_onset = sync_light_diff > sync_light_threshold
    sync_light_offset = sync_light_diff < -sync_light_threshold
    sync_light_onset_ind = np.where(sync_light_onset)[0]
    sync_light_offset_ind = np.where(sync_light_offset)[0]

    # -- Find period of sync_light_onset --
    sync_light_onset_diff = np.diff(sync_light_onset_ind)  # In units of frames
    expected_onset_period = np.median(sync_light_onset_diff)  # In units of (float) frames

    # -- Remove repeated onsets --
    onset_freq_upper_threshold = int(1.5 * expected_onset_period)
    onset_freq_lower_threshold = int(0.5 * expected_onset_period)
    repeated_onsets = sync_light_onset_diff < onset_freq_lower_threshold
    repeated_onsets_ind = np.where(repeated_onsets)[0]
    fixed_sync_light_onset = sync_light_onset.copy()
    fixed_sync_light_onset[sync_light_onset_ind[repeated_onsets_ind+1]] = False


    fixed_sync_light_onset_ind= np.where(fixed_sync_light_onset)[0]
    


    if prepost:
        sync_light_midpoint = (sync_light.max()+sync_light.min())/2
        if fixed_sync_light_onset_ind[-1] > sync_light_offset_ind[-1]:
            sync_light_offset_ind = np.append(sync_light_offset_ind, len(sync_light)-1)
            nOffsets = len(sync_light_offset_ind)
        first_sync_duration = sync_light_offset_ind[0] - fixed_sync_light_onset_ind[0]
        last_sync_duration = sync_light_offset_ind[-1] - fixed_sync_light_onset_ind[-1]
        if first_sync_duration > PRE_POST_DURATION_THRESHOLD:
            print('Found pre sync pulse. This pulse will be ignore in the final list.')
            fixed_sync_light_onset[fixed_sync_light_onset_ind[0]] = False
            fixed_sync_light_onset_ind = fixed_sync_light_onset_ind[1:]
        else:
            # Raise ValueError exception
            raise ValueError('No pre sync pulse found.')
        if last_sync_duration > PRE_POST_DURATION_THRESHOLD:
            print('Found post sync pulse. This pulse will be ignore in the final list.')
            fixed_sync_light_onset[fixed_sync_light_onset_ind[-1]] = False
            fixed_sync_light_onset_ind = fixed_sync_light_onset_ind[:-1]
        else:
            # Raise ValueError exception
            raise ValueError('No post sync pulse found.')

    fixed_sync_light_onset_diff = np.diff(fixed_sync_light_onset_ind)

    # -- Fix missing onsets --
    if fixmissing:
        missing_next_onsets = fixed_sync_light_onset_diff > onset_freq_upper_threshold
        missing_next_onsets_ind = np.where(missing_next_onsets)[0]
        for indm, missing_onset_ind in enumerate(missing_next_onsets_ind):
            onset_diff = fixed_sync_light_onset_diff[missing_onset_ind]
            n_missing = int(np.round(onset_diff / expected_onset_period))-1
            #print(n_missing)
            last_onset_ind = fixed_sync_light_onset_ind[missing_onset_ind]
            next_onset_ind = fixed_sync_light_onset_ind[missing_onset_ind+1]
            period_missing = (next_onset_ind - last_onset_ind)//(n_missing+1)
            new_onset_inds = last_onset_ind + np.arange(1, n_missing+1)*period_missing
            #print([last_onset_ind, next_onset_ind])
            #print(new_onset_inds)
            fixed_sync_light_onset[new_onset_inds] = True

    return fixed_sync_light_onset