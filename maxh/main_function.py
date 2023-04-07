'''
These functions are used for analysis of oddball sequence data in max's acid mice.
'''



import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis




def main_function(oneCell, session_type, timeRange):
    if oneCell.get_session_inds(session_type) != []: #and oneCell.get_session_inds('lowFreq') != []:
        ephysData, bdata = oneCell.load(session_type)  
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        #eventOnsetTimes = eventOnsetTimes[:-1]

        frequencies_each_trial = bdata['currentStartFreq']

        if (len(frequencies_each_trial) > len(eventOnsetTimes)) or (len(frequencies_each_trial) < len(eventOnsetTimes)-1):
            print(f'Warning! BevahTrials ({len(frequencies_each_trial)}) and ' + f'EphysTrials ({len(eventOnsetTimes)})')
            sys.exit()

        if len(frequencies_each_trial) == len(eventOnsetTimes)-1:
            eventOnsetTimes = eventOnsetTimes[:len(frequencies_each_trial)]

        (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        array_of_frequencies = np.unique(frequencies_each_trial)
        trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)


        # Extract column and reshape array for raster_plot function
        trialsEachFreqColumn1 = trialsEachCond[:,0].reshape(-1,1) 
        trialsEachFreqColumn2 = trialsEachCond[:,1].reshape(-1,1)

        return (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial, trialsEachFreqColumn1, trialsEachFreqColumn2)

def trials_before_oddball(oddballTrials):
        """
        Create a boolean array of the trials before the oddball as TRUE

        Args:
            1D array of oddballTrials 
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
        ilet = np.hstack((indexLimitsEachTrial1, indexLimitsEachTrial2 +len(spikeTimesFromEventOnset1)))

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

        return (tec)



def prepare_plots(oneCell, timeRange, sessionType1, sessionType2, timeVec):
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