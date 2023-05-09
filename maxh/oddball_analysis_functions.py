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




def main_function(oneCell, session_type, timeRange):

    '''
    Loads a session from oneCell accoring to the 'session_type'. Creates variables spikeTimes and eventOnsetTimes and calls the 
    spikesanalysis.eventlocked_spiketimes() function to lock the spikes to the events. Creates the trialsEachCond array according to the frequencies of each trial
    in the bdata. Finally, splits the trialsEachCond variable by its columns to seperate the conditions by standard and oddball. 
    
    '''
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


        # Extract column and reshape array for raster_plot function
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
        Combine two trial arrays into one

        Args:
            trials1: (np.arry) standard trials before oddball
            trials2: (np.array) oddball trials
        """
        tec1 = np.vstack((trials1, np.zeros(trials2.shape)))
        tec2 = np.vstack((np.zeros(trials1.shape), trials2))
        tec = np.hstack((tec1, tec2))

        return (tec.astype(bool))



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
        (spikeTimesHigh, trialIndexHigh, indexLimitsHigh, LowStd, HighOdd) = main_function(oneCell, sessionType1, timeRange)
        (spikeTimesLow, trialIndexLow, indexLimitsLow, LowOdd, HighStd) = main_function(oneCell, sessionType2, timeRange)
            

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
    '''

    runningOddball = np.zeros_like(combinedTrialsHigh, dtype=bool)
    runningOddball = np.logical_and(combinedTrialsHigh, combinedRunning)
    nonRunningBoolean = ~combinedRunning
    nonRunningOddball = np.logical_and(combinedTrialsHigh, nonRunningBoolean)            


    return runningOddball, nonRunningOddball

def read_videotimes(videotimesFile):
    '''
    Loads a python module with videoTimes.
    '''
    spec = importlib.util.spec_from_file_location('videotimes', videotimesFile)
    videotimes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(videotimes)

    return videotimes



def convert_videotimes(videotimes, sessionType):
    '''
    Using the keys runStart and runStop of 'sessionType', converts the timestamp strings into seconds.
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
    '''
    standardTrials= trialsEachCond[:,0].sum()
    oddballTrials= trialsEachCond[:,1].sum()
    labels = (f'Standard ({standardTrials})', f"Oddball ({oddballTrials})")

    return labels





    time_obj = datetime.datetime.strptime(time_str, '%M:%S')  # convert to datetime object
    seconds = (time_obj - datetime.datetime(1900, 1, 1)).total_seconds()  # convert to total seconds
    print(seconds)  # output: 75.0




