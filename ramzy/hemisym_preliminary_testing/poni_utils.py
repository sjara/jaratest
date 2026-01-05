"""
Functions for 2023acid project.
"""

import os
import numpy as np
from jaratoolbox import settings,spikesanalysis,behavioranalysis,ephyscore,loadneuropix
from joblib import Parallel,delayed
import importlib
from scipy import stats
from scipy import optimize
from scipy.signal import savgol_filter
import poni_params as studyparams
import warnings


warnings.simplefilter('ignore')


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


def find_tone_responsive_cells(celldb, eventKey='Evoked',frThreshold=10, allreagents=True,
                               sessionType='optoTuningFreq'):
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
    alpha = 0.05/N_FREQ
    modRates = studyparams.SESSION_MODRATES[sessionType]
    responsive = np.ones(len(celldb),dtype=bool)
    # for mod in modRates:
    #     responsive &= ((celldb[f'{mod}Hz_offToneResponseMinPval'+eventKey] <= alpha) &
    #                    ((celldb[f'{mod}Hz_offToneFiringRateBestFreq'+eventKey] >= frThreshold) | 
    #                     (celldb[f'{mod}Hz_offToneBaselineFiringRate'] >= frThreshold)))
        
    for mod in modRates:
        responsive &= (((celldb[f'{mod}Hz_offToneResponseMinPval'+eventKey] <= alpha) | \
                       ((celldb[f'{mod}Hz_offToneDiscrimBestFreq'+eventKey] >= studyparams.MIN_DPRIME))) | \
                        ((celldb[f'{mod}Hz_onToneResponseMinPval'+eventKey] <= alpha) |
                       ((celldb[f'{mod}Hz_onToneDiscrimBestFreq'+eventKey] >= studyparams.MIN_DPRIME))))
        
        # responsive &= ((celldb[f'{mod}Hz_onToneResponseMinPval'+eventKey] <= alpha) &
        #                ((celldb[f'{mod}Hz_onToneFiringRateBestFreq'+eventKey] >= frThreshold) | 
        #                 (celldb[f'{mod}Hz_onToneBaselineFiringRate'] >= frThreshold)))
        
    #    responsive &= (celldb[f'{mod}Hz_offToneResponseMinPval'+eventKey] <= alpha)



        # responsive &= (celldb[f'{mod}Hz_offToneResponseMinPval'+eventKey] <= alpha) & \
        #                     (celldb[f'{mod}Hz_onToneResponseMinPval'+eventKey] <= alpha)

    return responsive


def find_steady_cells(celldb, params, maxChangeFactor=1.2,sessionType='optoTuningFreq'):
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
    if 'AMtone' in sessionType:
        reagents = studyparams.REAGENTS[sessionType]
        sessionPre = studyparams.SESSION_PREFIXES[sessionType]

    
        prefixes = [reagent+sessionPre for reagent in reagents]
        modRates = studyparams.SESSION_MODRATES[sessionType]
        
        for param in params:
            if "Laser" in param:
                offString = f'{modRates[0]}Hz_onTone'
                offParam = celldb[offString+param]

                for mod in studyparams.SESSION_MODRATES['optoTuningAMtone']:
                    prefix = f'{mod}Hz_onTone'
                    changeParam = (celldb[prefix+param] / offParam )
                    steadyThisParam =  ( (changeParam < maxChangeFactor) & (changeParam > 1/maxChangeFactor) )
                    steady &= steadyThisParam

            else:
                for mod in modRates:
                    offString = f'{mod}Hz_offTone'
                    offParam = celldb[offString+param]

                    
                    for prefix in prefixes:
                        if prefix[:3] in offString and 'off' not in prefix:
                            changeParam = (celldb[prefix+param] / offParam )
                            steadyThisParam =  ( (changeParam < maxChangeFactor) & (changeParam > 1/maxChangeFactor) )
                            steady &= steadyThisParam
                    # print(sum(steady))
    else:
        reagents = studyparams.REAGENTS[sessionType]
        sessionPre = studyparams.SESSION_PREFIXES[sessionType]
        prefixes = [reagent+sessionPre for reagent in reagents]
        for param in params:
            changeParam = (celldb[prefixes[0]+param] / celldb[prefixes[1]+param] )
            steadyThisParam =  ( (changeParam < maxChangeFactor) & (changeParam > 1/maxChangeFactor) )
            steady = steady & steadyThisParam
    return steady


def find_freq_selective(celldb, eventKey='Evoked', 
                        minR2=studyparams.MIN_PVAL,
                        minD=studyparams.MIN_DPRIME,
                        minFano=studyparams.MIN_FANO,
                        sessionType='optoTuningFreq'):
    """
    Find cells that are frequency selective and have a good fit.

    Args:
        celldb (pandas.DataFrame): The celldb dataframe.
        minR2 (float): The minimum r-square to consider a cell frequency selective.
    Returns:
        freqSelective (np.array): Each item is a boolean.
    """
    sessionPre = studyparams.SESSION_PREFIXES[sessionType]
    reagents = studyparams.REAGENTS[sessionType]
    prefixes = [reagent+sessionPre for reagent in reagents if 'off' in reagent]
    freqSelectiveOff = (celldb[prefixes[0]+'SelectivityPval'+eventKey] <= minR2) 
    goodDoff = (celldb[prefixes[0]+'DiscrimBestFreq'+eventKey]>=minD)
    goodFano = (celldb[prefixes[0]+'FanoFactor'+eventKey] >= minFano)
    goodFI = (celldb[prefixes[0]+'FanoIndex'+eventKey] >= minFano)
    # goodZ = (celldb[prefixes[0]+'ZscoreBestFreq'+eventKey] >= minFano)
    goodSI = (celldb[prefixes[0]+'SelectivityIndex'+eventKey] >= minFano)
    highFiring = (celldb[prefixes[0]+'FiringRateBestFreq'+eventKey] >= studyparams.FR_THRESHOLD)
    for prefix in prefixes[1:]:
        goodFano |= (celldb[prefix+'FanoFactor'+eventKey] >= minFano)
        goodFI &= (celldb[prefix+'FanoIndex'+eventKey] >= minFano)
        # goodZ |= (celldb[prefix+'ZscoreBestFreq'+eventKey] >= minFano)
        goodSI &= (celldb[prefix+'SelectivityIndex'+eventKey] >= minFano)
        freqSelectiveOff &= (celldb[prefix+'SelectivityPval'+eventKey] <= minR2)
        goodDoff &= (celldb[prefix+'DiscrimBestFreq'+eventKey] >= minD)
        highFiring &= (celldb[prefix+'FiringRateBestFreq'+eventKey] >= studyparams.FR_THRESHOLD)
    
    # freqSelectiveOn = (celldb[prefixes[1]+'SelectivityPval'+eventKey]<0.05)
    # goodFitOff = (celldb[prefixes[0]+'GaussianRsquare'+eventKey] > minR2)
    # goodFitOn = (celldb[prefixes[-1]+'GaussianRsquare'+eventKey] > minR2)
    return goodFano #freqSelectiveOff #| goodZ  #| goodFano #& highFiring #& goodDoff #(freqSelectiveOff & goodFitOff) #| (freqSelectiveOn & goodFitOn)
    
    
def find_good_gaussian_fit(celldb,eventKey='Evoked', minR2=0.05,sessionType = 'optoTuningFreq'):
    """
    Find cells that have a good Gaussian fit in both pre and saline conditions.

    Args:
        celldb (pandas.DataFrame): The celldb dataframe.
        minR2 (float): The minimum r-square to consider a cell frequency selective.
    Returns:
        goodFit (np.array): Each item is a boolean.
    """

    sessionPre = studyparams.SESSION_PREFIXES[sessionType]
    reagents = studyparams.REAGENTS[sessionType]


    if 'poni' in sessionType:
        prefixes = [reagent+sessionPre for reagent in reagents]
    else:
        prefixes = [reagent+sessionPre for reagent in reagents]

    goodFit = (celldb[prefixes[0]+'GaussianRsquare'+eventKey] > minR2)

    if 'optoTuningAMtone' in sessionType:
        goodFit = ((celldb['4Hz_offTone'+'GaussianRsquare'+eventKey] >= minR2) | \
                    (celldb['64Hz_offTone'+'GaussianRsquare'+eventKey] >= minR2)) 

    # if 'poni' in sessionType:
    #     for prefix in prefixes:
    #         goodFit &= (celldb[prefix+'GaussianRsquare'+eventKey] > minR2)

    return goodFit 

def find_good_dprime(celldb, eventKey = 'Evoked',minDisc=0.2, sessionType='optoTuningAMtone',
                     frThreshold=studyparams.FR_THRESHOLD):
    sessionPre = studyparams.SESSION_PREFIXES[sessionType]
    reagents = studyparams.REAGENTS[sessionType]

    prefixes = [reagent+sessionPre for reagent in reagents]


    goodDprime = np.zeros(len(celldb),dtype=bool)

    for prefix in prefixes:
        goodDprime |= (celldb[prefix + 'DiscrimBestFreq'+eventKey] >= minDisc) 


    return goodDprime

def moving_average(data, window_size=studyparams.SMOOTHING_WINDOW):
    """
    Calculates the simple moving average of a 1D NumPy array.

    Args:
        data (np.ndarray): The input 1D NumPy array.
        window_size (int): The size of the moving average window.

    Returns:
        np.ndarray: The smoothed array.
    """
    if window_size <= 0:
        raise ValueError("Window size must be a positive integer.")
    if window_size > len(data):
        raise ValueError("Window size cannot be greater than the data length.")

    # Create a kernel of ones for averaging
    kernel = np.ones(window_size) / window_size

    # Convolve the data with the kernel
    # mode='same' to ensure data keeps the same shape, should not be an issue with smaller window sizes
    
    smoothed_data = np.convolve(data, kernel, mode='same')
    # smoothed_data = savgol_filter(data,window_size,2)
    

    return smoothed_data



def find_best_time_keys(celldb,metric,
                        eventKeys=studyparams.EVENT_KEYS,
                        sessionType='optoTuningFreq'):
    if metric in ['Ntrials','BaselineFiringRate','BaselineFiringRate']:
        print('Invalid Metric!')
        return 0
    
    greaterThans = ['GaussianA','GaussianRsquare','GaussianMaxChange','DiscrimBestFreq','FanoFactor','SelectivityKstat',
                    'SigmaAvgFR','DiscrimRatio','SelectivityIndex','FanoIndex']
    lessThans = ['ResponseMinPval','GaussianSigma','SelectivityPval','GaussianBandwidth']
    sessionPre = studyparams.SESSION_PREFIXES[sessionType]
    reagents = studyparams.REAGENTS[sessionType]
    bestKeys=[np.zeros(len(celldb),dtype='U15')+'Evoked' for i in range(len(reagents))]

    # for indr in range(len(reagents)):
    #     prefix = str(reagents[indr].replace('on','off').replace('C1','off').replace('C2','off'))+sessionPre
    #     bestKey = 'Evoked'
    #     cellInd = 0
        
    #     for indRow,dbRow in celldb.iterrows():
    #         for tKey in eventKeys:
    #             metricBestKey = dbRow[prefix+metric+bestKey]#*dbRow[prefix+'GaussianRsquare'+bestKey]
    #             metricThisKey = dbRow[prefix+metric+tKey]#*dbRow[prefix+'GaussianRsquare'+tKey]

    #             if metric in greaterThans and metricThisKey > metricBestKey:
    #                 bestKey = tKey

    #             elif metric in lessThans and metricThisKey < metricBestKey:
    #                 bestKey = tKey

    #             elif metric in ['BestFreq'] :
    #                 changeParamThisKey = (np.log2(celldb[prefix+metric+tKey])/np.log2(celldb[prefix+metric+tKey]))
    #                 changeParamBestKey = (np.log2(celldb[prefix+metric+bestKey])/np.log2(celldb[prefix+metric+bestKey]))

    #                 if changeParamThisKey < changeParamBestKey:
    #                     bestKey = tKey
                
    #             bestKeys[indr][cellInd] = bestKey
    #         cellInd += 1

    bestKey = eventKeys[0]
    cellInd = 0
    
    for indRow,dbRow in celldb.iterrows():
        for tKey in eventKeys[1:]:
            if 'Pval' in metric:
                metricBestKey = np.prod(np.concat([[dbRow[f'{mod}Hz_offTone'+metric+bestKey],dbRow[f'{mod}Hz_onTone'+metric+bestKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                metricThisKey = np.prod(np.concat([[dbRow[f'{mod}Hz_offTone'+metric+tKey],dbRow[f'{mod}Hz_onTone'+metric+tKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
            else:
                metricBestKey = np.sum(np.concat([[dbRow[f'{mod}Hz_offTone'+metric+bestKey],dbRow[f'{mod}Hz_onTone'+metric+bestKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                metricThisKey = np.sum(np.concat([[dbRow[f'{mod}Hz_offTone'+metric+tKey],dbRow[f'{mod}Hz_onTone'+metric+tKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
            
            if metric == 'SelectivityPval':
                othermetric = 'DiscrimBestFreq'
                metricBestKey /= np.sum(np.concat([[dbRow[f'{mod}Hz_offTone'+othermetric+bestKey],dbRow[f'{mod}Hz_onTone'+othermetric+bestKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                metricThisKey /= np.sum(np.concat([[dbRow[f'{mod}Hz_offTone'+othermetric+tKey],dbRow[f'{mod}Hz_onTone'+othermetric+tKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))

                # othermetric = 'ResponseMinPval'
                # metricBestKey *= np.prod(np.concat([[dbRow[f'{mod}Hz_offTone'+othermetric+bestKey],dbRow[f'{mod}Hz_onTone'+othermetric+bestKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                # metricThisKey *= np.prod(np.concat([[dbRow[f'{mod}Hz_offToqne'+othermetric+tKey],dbRow[f'{mod}Hz_onTone'+othermetric+tKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
            elif 'FanoFactor' in metric or 'SigmaAvgFR' in metric:
                othermetric = 'DiscrimBestFreq'
                metricBestKey *= np.sum(np.concat([[abs(dbRow[f'{mod}Hz_offTone'+othermetric+bestKey]),abs(dbRow[f'{mod}Hz_onTone'+othermetric+bestKey])] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                metricThisKey *= np.sum(np.concat([[abs(dbRow[f'{mod}Hz_offTone'+othermetric+tKey]),abs(dbRow[f'{mod}Hz_onTone'+othermetric+tKey])] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                
                # othermetric = 'ResponseMinPval'
                # metricBestKey /= np.prod(np.concat([[dbRow[f'{mod}Hz_offTone'+othermetric+bestKey],dbRow[f'{mod}Hz_onTone'+othermetric+bestKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                # metricThisKey /= np.prod(np.concat([[dbRow[f'{mod}Hz_offTone'+othermetric+tKey],dbRow[f'{mod}Hz_onTone'+othermetric+tKey]] for mod in studyparams.SESSION_MODRATES[sessionType]]))

            # elif metric == 'SelectivityKstat':
            #     metricBestKey *= np.sum([np.sum([dbRow[f'{mod}Hz_offToneFiringRateBestFreq'+bestKey],dbRow[f'{mod}Hz_onToneFiringRateBestFreq'+bestKey]]) for mod in studyparams.SESSION_MODRATES[sessionType]])
            #     metricThisKey *= np.sum([np.sum([dbRow[f'{mod}Hz_offToneFiringRateBestFreq'+tKey],dbRow[f'{mod}Hz_onToneFiringRateBestFreq'+tKey]]) for mod in studyparams.SESSION_MODRATES[sessionType]])

            elif 'GaussianA' in metric:
                metricBestKey = np.sum(np.concat([[abs(dbRow[f'{mod}Hz_offTone'+metric+bestKey]),abs(dbRow[f'{mod}Hz_onTone'+metric+bestKey])] for mod in studyparams.SESSION_MODRATES[sessionType]]))
                metricThisKey = np.sum(np.concat([[abs(dbRow[f'{mod}Hz_offTone'+metric+tKey]),abs(dbRow[f'{mod}Hz_onTone'+metric+tKey])] for mod in studyparams.SESSION_MODRATES[sessionType]]))

            if metric in greaterThans and metricThisKey > metricBestKey:
                bestKey = tKey

            elif metric in lessThans and metricThisKey < metricBestKey:
                bestKey = tKey

        for indr in range(len(reagents)):
            bestKeys[indr][cellInd] = bestKey
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

def peak_trough_time(celldb,samplingRate=30000,nt=61):
    nCells = len(celldb)
    timeDiffEachCell = np.empty(nCells)
    spikeShapes = celldb['spikeShape']
    tSteps = 100000*np.arange(nt)/samplingRate
    

    for inds,spikeShape in enumerate(spikeShapes):
        
        peakInd = np.argmin(spikeShape)
        tDiff = np.argmax(spikeShape[peakInd:])
        timeDiffEachCell[inds] = sum(tSteps[:tDiff])

    return timeDiffEachCell

def find_RS_cells(celldb,samplingRate=30000):
    timeDiffEachCell = peak_trough_time(celldb,samplingRate)
    
    return((timeDiffEachCell > 300))


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

def get_cell_depths(celldb):
    cellDepths = []
    pmapEachSite = {}
        

    for indr,dbRow in celldb.iterrows():

        
        subject = dbRow.subject
        pdepth = dbRow.pdepth
        currSite = f'{subject}_{pdepth}'

        ### --- Load Probe Map ---
        if currSite not in pmapEachSite:
            oneSession = f'{dbRow.date}_{dbRow.ephysTime[0]}'
            ephysPath = os.path.join(settings.EPHYS_NEUROPIX_PATH,
                                            subject, f'{oneSession}_processed_multi')
            xmlpath = os.path.join(ephysPath,'info','settings.xml')
            pmapEachSite[currSite] = loadneuropix.ProbeMap(xmlpath)

        pmap = pmapEachSite[currSite]

        ### --- Get Cell Depth ---
        bestChannel = dbRow.bestChannel
        cellDepths.append(pdepth - pmap.ypos[bestChannel])

    return np.array(cellDepths)


def process_cell(sessionType, sessionPre, reagents, dbRow, timeRange, 
                 timeRangeDuration, eventTimeKeys, measurements, studyparams, 
                 PLOT=False, TEST=False):
    '''
    Extracts features from a cell's spiking data. Use with parallelization (e.g., jobslib, multiprocessing)
    so database generation doesn't take forever.

    Returns:
        indRow (int): dataframe index of current cell, important for reincorporating this row's features
                            with the cell database
        columnsDict (dict): dictionary containing extracted features for this cell. 
    '''

    columnsDict = {}
    indRow = dbRow.name 

    try:
        oneCell = ephyscore.Cell(dbRow)
        ephysData, bdata = oneCell.load(sessionType)
    except Exception as e:
        print(f"Error processing {indRow}: {str(e)}")
        return columnsDict

    oneCell = ephyscore.Cell(dbRow)
    ephysData, bdata = oneCell.load(sessionType)

    if 'AMtone' in sessionType:
        modEachTrial = bdata['currentMod']
        possbileMod = np.unique(modEachTrial)
    else:
        modEachTrial = np.zeros(len(bdata['currentFreq']))
        possbileMod = np.unique(modEachTrial)

    if 'opto' in sessionType:
        laserEachTrial = np.array(['on' if i else 'off' for i in bdata['laserTrial']])
        possibleLaser = np.unique(laserEachTrial)
    else:
        laserEachTrial = np.array([f'C{i+1}' if i>=0 else 'off' for i in bdata['currentStimCol']])
        possibleLaser = np.unique(laserEachTrial)
    stimEachTrialAll = bdata['currentFreq']
    nTrialsAll = len(stimEachTrialAll)
    reagentEachTrial = np.array([f'{int(modEachTrial[i])}Hz_{laserEachTrial[i]}' for i in range(nTrialsAll)])
    possibleReagents = np.unique(reagentEachTrial)

    spikeTimesAll = ephysData['spikeTimes']
    eventOnsetTimesAll = ephysData['events']['stimOn']

    

    # If the ephys data is 1 more than the bdata, delete the last ephys trial.
    if len(stimEachTrialAll) == len(eventOnsetTimesAll)-1:
        eventOnsetTimesAll = eventOnsetTimesAll[:nTrialsAll]
    assert len(stimEachTrialAll) == len(eventOnsetTimesAll), \
        "Number of trials in behavior and ephys do not match for {oneCell}"

    # print(nTrialsAll,len(spikeTimesAll),len(eventOnsetTimesAll),len(stimEachTrialAll))

    for mod in reagents:
        reagent = sessionPre+str(mod)
        reagentOff = reagent.replace('on','off')
        trialInds = (reagentEachTrial==mod)
        # print(trialInds)

        spikeTimes = spikeTimesAll
        eventOnsetTimes = eventOnsetTimesAll[trialInds]

        stimEachTrial = stimEachTrialAll[trialInds]
        nTrials = len(stimEachTrial)
        
        # print(nTrials,len(spikeTimes),len(eventOnsetTimes))

        if nTrials == 0:
            break

        # -- Doing this before selecting trials by running/notrunning --
        possibleStim = np.unique(stimEachTrial)
        nStim = len(possibleStim)
        
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
            spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange['Full'])

        trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

        # -- Estimate baseline firing rate --
        spikeCountMatBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRange['Baseline'])
        baselineFiringRate = spikeCountMatBase.mean()/timeRangeDuration['Baseline']
        baselineSigma = np.std(spikeCountMatBase/timeRangeDuration['Baseline'])

        spikeCountMatLaser = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                [-0.25,0])
        laserFiringRate = spikeCountMatLaser.mean()/0.25
        laserSigma = np.std(spikeCountMatLaser/0.25)

        # -- Store non-Event data in columns dictionary
        columnsDict[reagent+'ToneBaselineFiringRate'] = baselineFiringRate
        columnsDict[reagent+'ToneBaselineSigma'] = baselineSigma
        columnsDict[reagent+'ToneNtrials'] = nTrials
        columnsDict[reagent+'ToneLaserFiringRate'] = laserFiringRate
        columnsDict[reagent+'ToneLaserSigma'] = laserSigma
        
        try:
            wStatLaser, pValLaser = stats.wilcoxon(spikeCountMatLaser[:,0], spikeCountMatBase[:,0])
        except ValueError:
            pValLaser = 1
        
        columnsDict[reagent+'ToneLaserPval'] = pValLaser

        for tKey in eventTimeKeys:
            # -- Estimate evoked firing rate for each stim --
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    timeRange[tKey])
            nSpikesEachTrial = spikeCountMat[:,0]  # Flatten it

            # -- Calculate nSpikes for each freq to test selectivity --
            nSpikesEachStim = []
            avgFiringRateEachStim = np.empty(nStim)
            sigmaEachStim = np.empty(nStim)
            dprimeEachFreq = np.empty(nStim)
            pValEvokedEachStim = np.empty(nStim)
            

            for indStim, frequency in enumerate(possibleStim):
                nSpikesThisStim = nSpikesEachTrial[trialsEachCond[:,indStim]]
                nSpikesEachStim.append(nSpikesThisStim)
                avgFiringRateEachStim[indStim] = nSpikesThisStim.mean()/timeRangeDuration[tKey]
                sigmaEachStim[indStim] =np.std(nSpikesThisStim/timeRangeDuration[tKey])

                dprimeEachFreq[indStim] = \
                    abs(avgFiringRateEachStim[indStim]-baselineFiringRate)/np.sqrt(0.5*(sigmaEachStim[indStim]**2 + baselineSigma**2))

                # -- Normalize to Baseline --
                if studyparams.BLNORM:
                    if baselineFiringRate > 0:
                        avgFiringRateEachStim[indStim] /= baselineFiringRate
                        sigmaEachStim[indStim] /= baselineFiringRate
                        baselineFiringRate = 1

                # -- Calculate p-value for each stim --
                baselineSpikesThisStim = spikeCountMatBase[trialsEachCond[:,indStim],0]
                try:
                    wStat, pValThisStim = stats.wilcoxon(nSpikesThisStim, baselineSpikesThisStim)
                except ValueError:
                    pValThisStim = 1
                pValEvokedEachStim[indStim] = pValThisStim
            try:
                nTrialsEachCond = trialsEachCond.sum(axis=0)>0
                nSpks = [nSpikesEachStim[ind] for ind in np.flatnonzero(nTrialsEachCond)]
                kStat, pValKruskal = stats.kruskal(*nSpks)
                #kStat, pValKruskal = stats.kruskal(*nSpikesEachStim)
            except ValueError:
                kStat = 0
                pValKruskal = 1
            pValEvokedMin = np.min(pValEvokedEachStim)

            nSpikesAllStims = np.concat(nSpikesEachStim)
            pooledSigma = np.std(nSpikesAllStims/timeRangeDuration[tKey])

            # -- Fit Gaussian to tuning data --
            freqEachTrial = stimEachTrial
            possibleFreq = possibleStim
            logFreq = np.log2(freqEachTrial)
            possibleLogFreq = np.log2(possibleFreq)
            maxEvokedFiringRate = np.nanmax(avgFiringRateEachStim)
            smoothedFiringRates = moving_average(avgFiringRateEachStim)
            
            changeFromBaseline = avgFiringRateEachStim - baselineFiringRate
            maxChangeFromBaseline = changeFromBaseline[np.nanargmax(np.abs(changeFromBaseline))]
            avgEvokedFiringRate = np.nanmean(avgFiringRateEachStim)

            
            #baselineFiringRate
            # PARAMS: a, x0, sigma, y0
            minS = studyparams.MIN_SIGMA
            maxS = studyparams.MAX_SIGMA
            if maxChangeFromBaseline >= 0:
                p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
                bounds = ([0, possibleLogFreq[0], minS, 0],
                        [np.inf, possibleLogFreq[-1], maxS, np.inf])
            else:
                p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
                bounds = ([-np.inf, possibleLogFreq[0], minS, 0],
                        [0, possibleLogFreq[-1], maxS, np.inf])
            try:
                firingRateEachTrial = nSpikesEachTrial/timeRangeDuration[tKey]
                fitParams, pcov = optimize.curve_fit(spikesanalysis.gaussian, logFreq,
                                                    firingRateEachTrial, p0=p0, bounds=bounds)
            except RuntimeError:
                # print("Could not fit gaussian curve to tuning data.")
                fitParams = np.full(4, np.nan)
                Rsquared = 0
            else:
                gaussianResp = spikesanalysis.gaussian(logFreq, *fitParams)
                residuals = firingRateEachTrial - gaussianResp
                ssquared = np.sum(residuals**2)
                ssTotal = np.sum((firingRateEachTrial-np.mean(firingRateEachTrial))**2)
                if ssTotal:
                    Rsquared = 1 - (ssquared/ssTotal)
                else:
                    # print("Divide by zero error...ssTotal is zero")
                    Rsquared = 0
                fullWidthHalfMax = 2.355*fitParams[2] # Sigma is fitParams[2]

            # -- Store results in dictionary --
            
            columnsDict[reagent+'ToneResponseMinPval'+tKey] = pValEvokedMin
            columnsDict[reagent+'ToneSelectivityPval'+tKey] = pValKruskal
            columnsDict[reagent+'ToneSelectivityKstat'+tKey] = kStat
            columnsDict[reagent+'ToneFiringRateBestFreq'+tKey] = maxEvokedFiringRate
            columnsDict[reagent+'ToneAvgEvokedFiringRate'+tKey] = avgEvokedFiringRate
            columnsDict[reagent+'ToneBestFreq'+tKey] = possibleFreq[avgFiringRateEachStim.argmax()]
            columnsDict[reagent+'ToneGaussianA'+tKey] = fitParams[0]
            columnsDict[reagent+'ToneGaussianX0'+tKey] = fitParams[1]
            columnsDict[reagent+'ToneGaussianSigma'+tKey] = fitParams[2]
            columnsDict[reagent+'ToneGaussianY0'+tKey] = fitParams[3]
            columnsDict[reagent+'ToneGaussianRsquare'+tKey] = Rsquared
            columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = avgFiringRateEachStim
            columnsDict[reagent+'ToneFiringRateEachFreqSmoothed'+tKey] = smoothedFiringRates
            columnsDict[reagent+'ToneSigmaEachFreq'+tKey] = sigmaEachStim
            columnsDict[reagent+'ToneDiscrimEachFreq'+tKey] = dprimeEachFreq
            columnsDict[reagent+'ToneMeanDiscrim'+tKey] = np.mean(abs(dprimeEachFreq))
            columnsDict[reagent+'ToneMeanDiscrimRaw'+tKey] = np.mean(dprimeEachFreq)
            # columnsDict[reagent+'ToneSelectivityIndex'+tKey] = (maxEvokedFiringRate-(sum(avgFiringRateEachStim)-maxEvokedFiringRate)/15)/np.sqrt(np.mean(sigmaEachStim**2))
            columnsDict[reagent+'ToneSelectivityIndex'+tKey] = (maxEvokedFiringRate-avgEvokedFiringRate)/np.sqrt(np.mean(sigmaEachStim**2))
            columnsDict[reagent+'ToneDiscrimBestFreq'+tKey] = np.nanmax(abs(dprimeEachFreq))
            columnsDict[reagent+'ToneSigmaAvgFR'+tKey] = np.std(avgFiringRateEachStim)
            columnsDict[reagent+'ToneFanoFactor'+tKey] = (np.std(avgFiringRateEachStim)**2)/avgEvokedFiringRate
            columnsDict[reagent+'ToneFanoFactorSmoothed'+tKey] = (np.std(smoothedFiringRates)**2)/np.mean(smoothedFiringRates)
            columnsDict[reagent+'ToneFanoIndex'+tKey] = (np.std(avgFiringRateEachStim)**2)/np.sqrt(np.mean(sigmaEachStim**2))
            
            columnsDict[reagent+'ToneVariabilityIndex'+tKey] = (np.std(avgFiringRateEachStim)**2)/maxEvokedFiringRate
            columnsDict[reagent+'TonePooledSigma'+tKey] = pooledSigma
            columnsDict[reagent+'ToneClusteringIndex'+tKey] = pooledSigma/np.sqrt(np.mean(sigmaEachStim**2))

            normResponseEachOctave = np.full(2*nStim-1,np.nan)
            avgFiringRateEachStimOff = columnsDict[reagentOff+'ToneFiringRateEachFreq'+tKey]
            bestFreqInd = np.nanargmax(avgFiringRateEachStim)
            centeringInd = nStim-1-bestFreqInd
            bestFreq = possibleStim[bestFreqInd]

            
            normResponseEachOctave[centeringInd:centeringInd+nStim] = avgFiringRateEachStim/max(avgFiringRateEachStimOff)
            
            columnsDict[reagent+'ToneNormResponseEachOctave'+tKey] = normResponseEachOctave

            if bestFreqInd < nStim//2:
                columnsDict[reagent+'ToneFiringRateEachOctave'+tKey] = avgFiringRateEachStim[bestFreqInd:studyparams.N_FREQ//2+bestFreqInd]
            else:
                columnsDict[reagent+'ToneFiringRateEachOctave'+tKey] = avgFiringRateEachStim[bestFreqInd - studyparams.N_FREQ//2+1: bestFreqInd+1][::-1]

    return (indRow, columnsDict)


def process_database_parallel(sessionType, sessionPre, reagents, celldb, timeRange, 
                                timeRangeDuration, eventTimeKeys, measurements, studyparams, 
                                PLOT=False, TEST=False):
    columnsDict = {}
    for mod in reagents:
        reagent = sessionPre+str(mod)
        # print(reagent)
        for measurement in measurements[:6]:
            columnsDict[reagent+measurement] = np.full(len(celldb), np.nan)
        for tKey in eventTimeKeys:   
            for measurement in measurements[6:]:
                columnsDict[reagent+measurement+tKey] = np.full(len(celldb), np.nan)
            columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneFiringRateEachFreqSmoothed'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneSigmaEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneDiscrimEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneNormResponseEachOctave'+tKey] = np.full((len(celldb),2*studyparams.N_FREQ - 1), np.nan)
            columnsDict[reagent+'ToneFiringRateEachOctave'+tKey] = np.full((len(celldb),studyparams.N_FREQ//2), np.nan)
    
    if TEST:
        celldbToUse = celldb[(celldb['sessionType'].apply(lambda x: sessionType in x)) & \
                             (celldb['date'].apply(lambda x: celldb.iloc[-1]['date'] in x))]
        
    else:
        celldbToUse = celldb[(celldb['sessionType'].apply(lambda x: sessionType in x))]


    print(f"--- Processing {sessionType}, {len(celldbToUse)} cells ---")

    # Prepare task list
    tasks = []
    for indr, dbRow in celldbToUse.iterrows():
        tasks.append((
            sessionType, sessionPre, reagents, dbRow,
            timeRange, timeRangeDuration, eventTimeKeys,
            measurements, studyparams,PLOT, TEST
        ))

    # Configure parallel processing
    n_workers = -2  # Use all but one core
    # n_workers = -1  # Use all cores
    columnsDictEachRow = Parallel(n_jobs=n_workers,verbose=10)(
        delayed(process_cell)(*task) for task in tasks
    )

    
    for row in columnsDictEachRow:
        indRow, columnsDictThisRow = row
        for key in columnsDictThisRow:
            columnsDict[key][indRow] = columnsDictThisRow[key]

    return columnsDict
    

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



    
        

