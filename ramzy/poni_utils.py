"""
Functions for 2023acid project.
"""

import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import poni_params as studyparams


# def find_oddball_responsive_cells(celldb, frThreshold=10):
#     """
#     Find cells that are responsive to any of the 4 stimuli.

#     Args:
#         celldb (pandas.DataFrame): The celldb dataframe.
#         frThreshold (float): The minimum firing rate to consider a cell responsive.
#     Returns:
#         responsiveDict (dict): Each item (for keys: high, low, up, down) is a boolean array.
#     """
#     alpha = 0.05/4  # Bonferroni correction for 4 comparisons
#     stimList = ['low','high','up','down']
#     responsiveDict = {}
#     for inds, stim in enumerate(stimList):
#         cstim = stim.capitalize()
#         responsiveDict[stim] = ( (celldb['pre'+cstim+'OddballPval']<alpha) |
#                                  (celldb['pre'+cstim+'StandardPval']<alpha) )
#         firingAboveThreshold = ( (celldb['pre'+cstim+'OddballEvokedFiringRate']>frThreshold) |
#                                  (celldb['pre'+cstim+'StandardEvokedFiringRate']>frThreshold) )
#         allEvokedAboveZero = ( (celldb['saline'+cstim+'OddballEvokedFiringRate']>0) &
#                                (celldb['saline'+cstim+'StandardEvokedFiringRate']>0) &
#                                (celldb['doi'+cstim+'OddballEvokedFiringRate']>0) &
#                                (celldb['doi'+cstim+'StandardEvokedFiringRate']>0) )
#         responsiveDict[stim] = responsiveDict[stim] & firingAboveThreshold & allEvokedAboveZero
#     return responsiveDict


def find_tone_responsive_cells(celldb, eventKey='Evoked',frThreshold=10, allreagents=True):
    """
    Find cells that are responsive to at least one of the pure tones tested during tuning.

    Args:
        celldb (pandas.DataFrame): The celldb dataframe.
        frThreshold (float): The minimum firing rate to consider a cell responsive.
        allreagents (bool): If True, the cell must be responsive under all reagent conditions.
    Returns:
        responsive (np.array): Each item is a boolean.
    """
    N_FREQ = 16	
    # Apply bonferroni correction
    alpha = 0.05#/N_FREQ
    if allreagents:
        responsive = ( (( (celldb['offToneResponseMinPval'+eventKey] < alpha) |
                            (celldb['offToneSelectivityPval'+eventKey] < alpha) ) &
                        ((celldb['offToneFiringRateBestFreq'+eventKey] > frThreshold)|
                         (celldb['offToneGaussianA'+eventKey] > frThreshold) |
                        (celldb['offToneBaselineFiringRate']>frThreshold) |
                         (celldb['offToneGaussianMaxChange'+eventKey] > frThreshold) )) |
                        ( ( (celldb['onToneResponseMinPval'+eventKey] < alpha) | 
                        (celldb['onToneSelectivityPval'+eventKey] < alpha) ) &
                        ( (celldb['onToneFiringRateBestFreq'+eventKey] > frThreshold) |
                         (celldb['onToneGaussianA'+eventKey] > frThreshold) |
                        (celldb['onToneBaselineFiringRate'] > frThreshold) |
                         (celldb['onToneGaussianMaxChange'+eventKey] > frThreshold) ) ) )
    else:
        responsive = ( ((celldb['offToneResponseMinPval'+eventKey] < alpha) |
                        (celldb['offToneSelectivityPval'+eventKey] < alpha)) &
                       ((celldb['offToneFiringRateBestFreq'+eventKey] > frThreshold) |
                        (celldb['offToneGaussianA'+eventKey] > frThreshold) |
                         (celldb['offToneGaussianMaxChange'+eventKey] > frThreshold) ) )
    return responsive


def find_steady_cells(celldb, params, maxChangeFactor=1.2):
    """
    Find cells that are steady during the pure tone presentation.

    Args:
        celldb (pandas.DataFrame): The celldb dataframe.
        params (list): List of strings with the names of the parameters to check.
        maxChangeFactor (float): The maximum factor by which the parameter can change
                                 to be considered steady.
    Returns:
        steady (np.array): Each item is a boolean.
    """
    steady = np.ones(len(celldb), dtype=bool)
    for param in params:
        changeParam = (celldb['on'+param] / celldb['off'+param] )
        steadyThisParam =  ( (changeParam < maxChangeFactor) & (changeParam > 1/maxChangeFactor) )
        steady = steady & steadyThisParam
    return steady


def find_freq_selective(celldb, eventKey='Evoked', minR2=0.05):
    """
    Find cells that are frequency selective and have a good fit.

    Args:
        celldb (pandas.DataFrame): The celldb dataframe.
        minR2 (float): The minimum r-square to consider a cell frequency selective.
    Returns:
        freqSelective (np.array): Each item is a boolean.
    """
    freqSelectiveOff = (celldb['offToneSelectivityPval'+eventKey]<0.05) 
    freqSelectiveOn = (celldb['onToneSelectivityPval'+eventKey]<0.05)
    goodFitOff = (celldb['offToneGaussianRsquare'+eventKey] > minR2)
    goodFitOn = (celldb['onToneGaussianRsquare'+eventKey] > minR2)
    return (freqSelectiveOff & goodFitOff) | (freqSelectiveOn & goodFitOn)
    
    
def find_good_gaussian_fit(celldb,eventKey='Evoked', minR2=0.05):
    """
    Find cells that have a good Gaussian fit in both pre and saline conditions.

    Args:
        celldb (pandas.DataFrame): The celldb dataframe.
        minR2 (float): The minimum r-square to consider a cell frequency selective.
    Returns:
        goodFit (np.array): Each item is a boolean.
    """
    goodFitOff = (celldb['offToneGaussianRsquare'+eventKey] > minR2)
    goodFitOn = (celldb['onToneGaussianRsquare'+eventKey] > minR2)
    return goodFitOff #| goodFitOn

def find_best_time_keys(celldb,metric,tranges=studyparams.EVENT_KEYS):
    if metric in ['ToneNtrials','offToneBaselineFiringRate','onToneBaselineFiringRate']:
        print('Invalid Metric!')
        return 0
    
    greaterThans = ['ToneGaussianA','ToneGaussianRsquare','ToneGaussianMaxChange']
    lessThans = ['ToneResponseMinPval','ToneGaussianSigma','ToneSelectivityPval','ToneGaussianBandwidth']
    bestKey = 'Evoked'
    bestKeys = np.zeros(len(celldb),dtype='U15')+bestKey
    cellInd = 0
    
    for indRow,dbRow in celldb.iterrows():
        for tKey in tranges:
            metricBestKey = dbRow['off'+metric+bestKey]
            metricThisKey = dbRow['off'+metric+tKey]

            if metric in greaterThans and metricThisKey > metricBestKey:
                bestKey = tKey

            elif metric in lessThans and metricThisKey < metricBestKey:
                bestKey = tKey

            elif metric in ['ToneBestFreq'] :
                changeParamThisKey = (np.log2(celldb['off'+metric+tKey])/np.log2(celldb['off'+metric+tKey]))
                changeParamBestKey = (np.log2(celldb['off'+metric+bestKey])/np.log2(celldb['off'+metric+bestKey]))

                if changeParamThisKey < changeParamBestKey:
                    bestKey = tKey
            
            bestKeys[cellInd] = bestKey
        cellInd += 1
        
            
    return bestKeys

def modulation_index(vec1, vec2):
    """
    Calculate the modulation index between two vectors.

    Args:
        vec1 (np.array): The first vector.
        vec2 (np.array): The second vector.
    Returns:
        modIndex (float): The modulation index.
    """
    modIndex = (vec1 - vec2) / (vec1 + vec2)
    return modIndex


def load_laser_data():
    """
    Load the running data for all subjects.
    
    Returns:
        runningData (dict): Each item is a dict with the running data for each subject.
    """
    dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
    laserData = {}
    for subject in studyparams.SUBJECTS:
        laserData[subject] = dict(np.load(os.path.join(dbPath, f'laser_{subject}.npz')))
    return laserData

def combine_trials_each_cond(trials1, trials2):
        """
        Combine two sets of "trialsEachCond" arrays.

        This version assumes the two sets contain the same number of conditions.

        Args:
            trials1 (np.array): array of boolean (nTrials, nCond) indicating trials for each condition.
            trials2 (np.array): same as trials1 but for another set of conditions.
        Return:
            trialsEachCond: combined boolean array of trials for each condition.
        """
        tec1 = np.vstack((trials1, np.zeros(trials2.shape)))
        tec2 = np.vstack((np.zeros(trials1.shape), trials2))
        tec = np.hstack((tec1, tec2))
        return tec.astype(bool)

def combine_index_limits(spikeTimesFromEventOnset1, spikeTimesFromEventOnset2,
                         indexLimitsEachTrial1, indexLimitsEachTrial2):
        """
        Combine the spikeTimesFromEventOnset and indexLimitsEachTrial from two ephys sessions.

        Args:
            spikeTimesFromEventOnset1, spikeTimesFromEventOnset2, indexLimitsEachTrial1, indexLimitsEachTrial2
        Returns:
            (SpikeTimes, IndexLimits)
        """
        stfeo = np.concatenate((spikeTimesFromEventOnset1, spikeTimesFromEventOnset2))
        ilet = np.hstack((indexLimitsEachTrial1, indexLimitsEachTrial2 + len(spikeTimesFromEventOnset1)))
        nTrials1 = indexLimitsEachTrial1.shape[1]
        nTrials2 = indexLimitsEachTrial2.shape[1]
        tec1 = np.vstack((np.ones((nTrials1,1)), np.zeros((nTrials2,1))))
        tec2 = np.vstack((np.zeros((nTrials1,1)), np.ones((nTrials2,1))))
        tec = np.hstack((tec1, tec2))
        return (stfeo, ilet, tec)

'''    
def combine_ephys_session(spikeTimesFromEventOnset1, spikeTimesFromEventOnset2,
                          indexLimitsEachTrial1, indexLimitsEachTrial2):
        """
        Combine the spikeTimesFromEventOnset and indexLimitsEachTrial from two ephys sessions.

        Args:
            spikeTimesFromEventOnset1, spikeTimesFromEventOnset2, indexLimitsEachTrial1, indexLimitsEachTrial2
        Returns:
            (SpikeTimes, IndexLimits)

        TO DO:
        Maybe specify TriaslEachCond, so we can concatenate session with more than 1 cond.
        """
        stfeo = np.concatenate((spikeTimesFromEventOnset1, spikeTimesFromEventOnset2))
        ilet = np.hstack((indexLimitsEachTrial1, indexLimitsEachTrial2 + len(spikeTimesFromEventOnset1)))
        nTrials1 = indexLimitsEachTrial1.shape[1]
        nTrials2 = indexLimitsEachTrial2.shape[1]
        tec1 = np.vstack((np.ones((nTrials1,1)), np.zeros((nTrials2,1))))
        tec2 = np.vstack((np.zeros((nTrials1,1)), np.ones((nTrials2,1))))
        tec = np.hstack((tec1, tec2))
        return (stfeo, ilet, tec)
'''

# def load_oddball_data_one_cell(oneCell, oddballToLoad, reagent, timeRange, nPreOdd=2):
#     """
#     Load the oddball data for one cell. 
#     It return arrays with 'standard' trials first and 'oddball' trials last.
    
#     Args:
#         oneCell (ephyscore.Cell): The cell to load.
#         oddballToLoad (str): Oddball stim for sessions to load (e.g, 'FM_Up' or 'LowFreq').
#                              This should match the names in studyparams.ODDBALL_SESSION_TYPES.
#         reagent (str): The reagent to load.
#         timeRange (np.array): The time range to load.
#         nPreOdd
#     Returns:
#         stfeo: Spike times from event onset. 
#         ilet: index limits for each trial.
#         tec: trials each condition.
#         condLabels: Labels for each condition (e.g., 'standard', 'oddball').
#         bdataList: list of bdata dicts.
#     """

#     N_PRE_ODDBALL = nPreOdd #2, 8, 4  # Analyze only the last N standard trials before oddball

#     if 'FM' in oddballToLoad:
#         sessionsToLoad = {k: studyparams.ODDBALL_SESSION_TYPES[k] for k in ('FM_Up', 'FM_Down')}
#     elif 'Freq'in oddballToLoad:
#         sessionsToLoad = {k: studyparams.ODDBALL_SESSION_TYPES[k] for k in ('LowFreq', 'HighFreq')}

#     stimConditions = ['oddball', 'standard']
#     stfeoEachSession = {'oddball':[], 'standard':[]}  # Spike times from event onset
#     iletEachSession = {'oddball':[], 'standard':[]} # Index limits for each trial
#     bdataList = []
    
#     for sessionType, sessionInfo in sessionsToLoad.items():
#         ephysData, bdata = oneCell.load(reagent+sessionType)
#         spikeTimes = ephysData['spikeTimes']
#         eventOnsetTimes = ephysData['events']['stimOn']

#         stimEachTrial = bdata['currentStartFreq']
#         nTrials = len(stimEachTrial)
#         bdataList.append(bdata)
        
#         # If the ephys data is 1 more than the bdata, delete the last ephys trial.
#         if len(stimEachTrial) == len(eventOnsetTimes)-1:
#             eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
#         assert len(stimEachTrial) == len(eventOnsetTimes), \
#             "Number of trials in behavior and ephys do not match for {oneCell}"

#         (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
#             spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

#         possibleStim = np.unique(stimEachTrial)
#         trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

#         # -- Get oddball and standard trials (checking things match ODDBALL_SESSION_TYPES) --
#         indOddball = np.argmin(trialsEachCond.sum(axis=0))
#         indEachCond = {'oddball': indOddball, 'standard': 1-indOddball}
#         # -- According to currentStartFreq, this is how the stim are ordered --
#         stimOrder = {'FM': ['FM_up', 'FM_down'],
#                      'Chord': ['low_freq', 'high_freq']}
#         # -- Sanity check --
#         oddballStim = bdata.labels['oddballStim'][bdata['oddballStim'][-1]]
#         stimType = bdata.labels['stimType'][bdata['stimType'][-1]]
#         assert oddballStim == stimOrder[stimType][indOddball], \
#             f"Oddball stim should be {stimOrder[stimType][indOddball]}"

#         # -- Include only the last N standard trials before oddball--
#         oddballInds = np.where(trialsEachCond[:,indOddball])[0]
#         zeroind, pre = np.meshgrid(oddballInds, np.arange(1, N_PRE_ODDBALL+1))
#         lastXinds = np.concatenate(zeroind-pre)
#         trialsEachCond[:, 1-indOddball] = False
#         trialsEachCond[lastXinds, 1-indOddball] = True

#         if sessionType == oddballToLoad:
#             stfeoEachSession['oddball'] = spikeTimesFromEventOnset
#             trialsThisCond = trialsEachCond[:, indEachCond['oddball']]
#             iletEachSession['oddball'] = indexLimitsEachTrial[:, trialsThisCond]
#         else:
#             stfeoEachSession['standard'] = spikeTimesFromEventOnset
#             trialsThisCond = trialsEachCond[:, indEachCond['standard']]
#             iletEachSession['standard'] = indexLimitsEachTrial[:, trialsThisCond]

#     stfeo, ilet, tec = combine_index_limits(stfeoEachSession['standard'],
#                                             stfeoEachSession['oddball'],
#                                             iletEachSession['standard'],
#                                             iletEachSession['oddball'])
#     condLabels = ['standard', 'oddball']
#     return (stfeo, ilet, tec, condLabels, bdataList)
