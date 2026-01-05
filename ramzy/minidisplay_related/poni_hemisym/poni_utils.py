"""
Functions for 2023acid project.
"""

import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import ephyscore
from joblib import Parallel,delayed
from scipy import stats
from scipy import optimize
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
                               sessionType='optoFreq'):
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
    if allreagents:

        # responsive = ( (( (celldb['offToneResponseMinPval'+eventKey] < alpha) |
        #                     (celldb['offToneSelectivityPval'+eventKey] < alpha) ) &
        #                 ((celldb['offToneFiringRateBestFreq'+eventKey] > frThreshold)|
        #                  (celldb['offToneGaussianA'+eventKey] > frThreshold) |
        #                 (celldb['offToneBaselineFiringRate']>frThreshold) |
        #                  (celldb['offToneGaussianMaxChange'+eventKey] > frThreshold) )) |
        #                 ( ( (celldb['onToneResponseMinPval'+eventKey] < alpha) | 
        #                 (celldb['onToneSelectivityPval'+eventKey] < alpha) ) &
        #                 ( (celldb['onToneFiringRateBestFreq'+eventKey] > frThreshold) |
        #                  (celldb['onToneGaussianA'+eventKey] > frThreshold) |
        #                 (celldb['onToneBaselineFiringRate'] > frThreshold) |
        #                  (celldb['onToneGaussianMaxChange'+eventKey] > frThreshold) ) ) )
        
        
        reagents = studyparams.REAGENTS[sessionType]
        sessionPre = studyparams.SESSION_PREFIXES[sessionType]

        sessionParams = sessionType.split('_')
        # tilesPre = sessionType[len(sessionParams[0])+1:] + '_'
        tilesPre=''
        prefixes = [tilesPre+reagent+sessionPre for reagent in reagents]
        # responsive =  ((celldb[prefixes[0]+'ResponseMinPval'+eventKey] < alpha) |
        #                     (celldb[prefixes[0]+'SelectivityPval'+eventKey] < alpha) )
        responsive =  (((celldb[prefixes[0]+'ResponseMinPval'+eventKey] < alpha) |
                            (celldb[prefixes[0]+'SelectivityPval'+eventKey] < alpha)) & 
                            (celldb[prefixes[0]+'FiringRateBestFreq'+eventKey] > frThreshold) )
        for pre in prefixes:
            # responsive &= ((celldb[pre+'ResponseMinPval'+eventKey] < alpha) |
            #             (celldb[pre+'SelectivityPval'+eventKey] < alpha) )
            responsive &= (((celldb[pre+'ResponseMinPval'+eventKey] < alpha)|
                        (celldb[pre+'SelectivityPval'+eventKey] < alpha)) )
        
    else:
        responsive = ( ((celldb['offToneResponseMinPval'+eventKey] < alpha) |
                        (celldb['offToneSelectivityPval'+eventKey] < alpha)) &
                       ((celldb['offToneFiringRateBestFreq'+eventKey] > frThreshold) |
                        (celldb['offToneGaussianA'+eventKey] > frThreshold) |
                         (celldb['offToneGaussianMaxChange'+eventKey] > frThreshold) ) )
    return responsive


def find_steady_cells(celldb, params, maxChangeFactor=1.2,sessionType='optoFreq'):
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
    if 'poni' in sessionType:
        reagents = studyparams.REAGENTS[sessionType]
        sessionPre = studyparams.SESSION_PREFIXES[sessionType]

        sessionParams = sessionType.split('_')
        # tilesPre = sessionType[len(sessionParams[0])+1:] + '_'
        tilesPre=''
        prefixes = [tilesPre+reagent+sessionPre for reagent in reagents]
        
        
        for param in params:
            offParam = celldb[prefixes[0]+param]
            for prefix in prefixes[1:]:
                changeParam = (celldb[prefix+param] / offParam )
                steadyThisParam =  ( (changeParam < maxChangeFactor) & (changeParam > 1/maxChangeFactor) )
                steady = steady & steadyThisParam
                # print(sum(steady))
    else:
        reagents = studyparams.REAGENTS_LASER
        sessionPre = studyparams.SESSION_PREFIXES[sessionType]
        prefixes = [reagent+sessionPre for reagent in reagents]
        for param in params:
            changeParam = (celldb[prefixes[0]+param] / celldb[prefixes[1]+param] )
            steadyThisParam =  ( (changeParam < maxChangeFactor) & (changeParam > 1/maxChangeFactor) )
            steady = steady & steadyThisParam
    return steady

def find_good_dprime(celldb, eventKey = 'Evoked',minDisc=0.2, sessionType='optoFreq'):
    sessionPre = studyparams.SESSION_PREFIXES[sessionType]
    reagents = studyparams.REAGENTS[sessionType]

    prefixes = [reagent+sessionPre for reagent in reagents if 'off' in reagent]

    goodDprime = np.ones(len(celldb),dtype=bool)

    for prefix in prefixes:
        goodDprime &= (celldb[prefix + 'DiscrimBestFreq'+eventKey] > minDisc)

    return goodDprime


def find_freq_selective(celldb, eventKey='Evoked', minR2=0.05,sessionType='optoFreq'):
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
    sessionParams = sessionType.split('_')
    tilesPre = sessionType[len(sessionParams[0])+1:]
    prefixes = [tilesPre+reagent+sessionPre for reagent in reagents]
    freqSelectiveOff = (celldb[prefixes[0]+'SelectivityPval'+eventKey]<0.05) 
    freqSelectiveOn = (celldb[prefixes[-1]+'SelectivityPval'+eventKey]<0.05)
    goodFitOff = (celldb[prefixes[0]+'GaussianRsquare'+eventKey] > minR2)
    goodFitOn = (celldb[prefixes[-1]+'GaussianRsquare'+eventKey] > minR2)
    return (freqSelectiveOff & goodFitOff) #| (freqSelectiveOn & goodFitOn)
    
    
def find_good_gaussian_fit(celldb,eventKey='Evoked', minR2=0.05,sessionType = 'optoFreq'):
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

    sessionParams = sessionType.split('_')
    tilesPre = sessionType[len(sessionParams[0])+1:] 

    if 'poni' in sessionType:
        prefixes = [tilesPre+reagent+sessionPre for reagent in reagents]
    else:
        prefixes = [reagent+sessionPre for reagent in reagents]
    goodFit = (celldb[prefixes[0]+'GaussianRsquare'+eventKey] > minR2)
    # if 'poni' in sessionType:
    #     for prefix in prefixes:
    #         goodFit &= (celldb[prefix+'GaussianRsquare'+eventKey] > minR2)

    return goodFit 

def find_best_time_keys(celldb,metric,
                        eventKeys=studyparams.EVENT_KEYS,
                        sessionType='optoFreq'):
    if metric in ['Ntrials','BaselineFiringRate','BaselineFiringRate']:
        print('Invalid Metric!')
        return 0
    
    greaterThans = ['GaussianA','GaussianRsquare','GaussianMaxChange','MeanDiscrim','DiscrimBestFreq']
    lessThans = ['ResponseMinPval','GaussianSigma','SelectivityPval','GaussianBandwidth']
    sessionPre = studyparams.SESSION_PREFIXES[sessionType]
    reagents = studyparams.REAGENTS[sessionType]

    sessionParams = sessionType.split('_')
    # tilesPre = sessionType[len(sessionParams[0])+1:] +'_'
    tilesPre = ''

    prefix = tilesPre+reagents[0]+sessionPre
    bestKey = 'Evoked'
    bestKeys = np.zeros(len(celldb),dtype='U15')+bestKey
    cellInd = 0
    
    for indRow,dbRow in celldb.iterrows():
        for tKey in eventKeys:
            metricBestKey = dbRow[prefix+metric+bestKey]*dbRow[prefix+'GaussianRsquare'+bestKey]
            metricThisKey = dbRow[prefix+metric+tKey]*dbRow[prefix+'GaussianRsquare'+tKey]

            if metric in greaterThans and metricThisKey > metricBestKey:
                bestKey = tKey

            elif metric in lessThans and metricThisKey < metricBestKey:
                bestKey = tKey

            elif metric in ['BestFreq'] :
                changeParamThisKey = (np.log2(celldb[prefix+metric+tKey])/np.log2(celldb[prefix+metric+tKey]))
                changeParamBestKey = (np.log2(celldb[prefix+metric+bestKey])/np.log2(celldb[prefix+metric+bestKey]))

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


def process_cell(sessionType, sessionPre, reagents, dbRow, timeRange, 
                 timeRangeDuration, eventTimeKeys, measurements, studyparams, 
                 PLOT=False, DEBUG=False):
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
    tileEachTrial = np.array([f'C{i}R{j}' if i+j >= 0 else 'off' \
                              for i,j in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
    
    possibleTile = np.unique(tileEachTrial)

    spikeTimesAll = ephysData['spikeTimes']
    eventOnsetTimesAll = ephysData['events']['stimOn']

    stimEachTrialAll = bdata['currentFreq']
    nTrialsAll = len(stimEachTrialAll)

    # If the ephys data is 1 more than the bdata, delete the last ephys trial.
    if len(stimEachTrialAll) == len(eventOnsetTimesAll)-1:
        eventOnsetTimesAll = eventOnsetTimesAll[:nTrialsAll]
    assert len(stimEachTrialAll) == len(eventOnsetTimesAll), \
        "Number of trials in behavior and ephys do not match for {oneCell}"

    # print(nTrialsAll,len(spikeTimesAll),len(eventOnsetTimesAll),len(stimEachTrialAll))

    for tile in reagents:
        reagent = sessionPre+tile
        trialInds = (tileEachTrial==tile)
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

        # -- Store non-Event data in columns dictionary
        columnsDict[reagent+'ToneBaselineFiringRate'] = baselineFiringRate
        columnsDict[reagent+'ToneNtrials'] = nTrials

        for tKey in eventTimeKeys:
            # -- Estimate evoked firing rate for each stim --
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    timeRange[tKey])
            nSpikesEachTrial = spikeCountMat[:,0]  # Flatten it

            # -- Calculate nSpikes for each freq to test selectivity --
            nSpikesEachStim = []
            avgFiringRateEachStim = np.empty(nStim)
            pValEvokedEachStim = np.empty(nStim)
            for indStim, frequency in enumerate(possibleStim):
                nSpikesThisStim = nSpikesEachTrial[trialsEachCond[:,indStim]]
                nSpikesEachStim.append(nSpikesThisStim)
                avgFiringRateEachStim[indStim] = nSpikesThisStim.mean()/timeRangeDuration[tKey]
                # -- Calculate p-value for each stim --
                baselineSpikesThisStim = spikeCountMatBase[trialsEachCond[:,indStim],0]
                try:
                    wStat, pValThisStim = stats.wilcoxon(nSpikesThisStim, baselineSpikesThisStim,)
                except ValueError:
                    pValThisStim = 1
                pValEvokedEachStim[indStim] = pValThisStim
            try:
                nTrialsEachCond = trialsEachCond.sum(axis=0)>0
                nSpks = [nSpikesEachStim[ind] for ind in np.flatnonzero(nTrialsEachCond)]
                kStat, pValKruskal = stats.kruskal(*nSpks)
                #kStat, pValKruskal = stats.kruskal(*nSpikesEachStim)
            except ValueError:
                pValKruskal = 1
            pValEvokedMin = np.min(pValEvokedEachStim)

            # -- Fit Gaussian to tuning data --
            freqEachTrial = stimEachTrial
            possibleFreq = possibleStim
            logFreq = np.log2(freqEachTrial)
            possibleLogFreq = np.log2(possibleFreq)
            maxEvokedFiringRate = np.nanmax(avgFiringRateEachStim)
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
            columnsDict[reagent+'ToneFiringRateBestFreq'+tKey] = maxEvokedFiringRate
            columnsDict[reagent+'ToneAvgEvokedFiringRate'+tKey] = avgEvokedFiringRate
            columnsDict[reagent+'ToneBestFreq'+tKey] = possibleFreq[avgFiringRateEachStim.argmax()]
            columnsDict[reagent+'ToneGaussianA'+tKey] = fitParams[0]
            columnsDict[reagent+'ToneGaussianX0'+tKey] = fitParams[1]
            columnsDict[reagent+'ToneGaussianSigma'+tKey] = fitParams[2]
            columnsDict[reagent+'ToneGaussianY0'+tKey] = fitParams[3]
            columnsDict[reagent+'ToneGaussianRsquare'+tKey] = Rsquared
            columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = avgFiringRateEachStim
    return (indRow, columnsDict)


def process_database_parallel(sessionType, sessionPre, reagents, celldb, timeRange, 
                                timeRangeDuration, eventTimeKeys, measurements, studyparams, 
                                PLOT=False, DEBUG=False):
    columnsDict = {}
    for tile in reagents:
        reagent = sessionPre+tile
        # print(reagent)
        for measurement in measurements[:2]:
            columnsDict[reagent+measurement] = np.full(len(celldb), np.nan)
        for tKey in eventTimeKeys:   
            for measurement in measurements[3:]:
                columnsDict[reagent+measurement+tKey] = np.full(len(celldb), np.nan)
            columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
    if DEBUG:
        indRow = 46  # 46 # 55
        indRow = 53  # Inverted
        #indRow = 176
        indRow = 1533
        indRow = 1318
        indRow = 1501 # Wide going down
        indRow = 1583 # very flat
        #indRow = 67  # Did not fit before fixing p0(A)
        celldbToUse = celldb[(celldb['sessionType'].apply(lambda x: sessionType in x))].iloc[[indRow]]
    else:
        celldbToUse = celldb[(celldb['sessionType'].apply(lambda x: sessionType in x))]

    print(f"--- Processing {sessionType}, {len(celldbToUse)} cells ---")

    # Prepare task list
    tasks = []
    for _, dbRow in celldbToUse.iterrows():
        tasks.append((
            sessionType, sessionPre, reagents, dbRow,
            timeRange, timeRangeDuration, eventTimeKeys,
            measurements, studyparams,PLOT, DEBUG
        ))

    # Configure parallel processing
    n_workers = os.cpu_count() - 1  # Use all but one core
    columnsDictEachRow = Parallel(n_jobs=n_workers, verbose=10)(
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
