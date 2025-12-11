"""
Estimate frequency tuning responses.

This script adds columns to the database with tuning results for each reagent.

To run for only laseroff or not-laseroff trials, use:
    python database_freq_tuning.py laseroff
    python database_freq_tuning.py laseron

On laptop, it took between <4 min to run.
"""

import os
import sys
import itertools
from joblib import Parallel, delayed
import numpy as np
import pandas as pd
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import poni_params as studyparams
import poni_utils as studyutils
from importlib import reload
import warnings
reload(studyparams)
reload(spikesanalysis)
reload(ephyscore)

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

# sessionTypes=['poniFreq_4x4_C2R3_2x2','poniFreq_4x1'] 
TEST = 1 if studyparams.TEST else 0
PLOT = 0
SAVE = 1

trialSubset=''


# subject = 'poni001'
# sessionTypes=['optoTuningAMtone']


subject = sys.argv[1]
# sessionDate = sys.argv[2]
# probeDepth = int(sys.argv[3])
if len(sys.argv)==3:
    sessionTypes = sys.argv[2].split(',')
else:
    sessionTypes = ['optoTuningAMtone','optoTuningFreq']

# if sessionTypes == ['all']:
#     sessionTypes = ['optoTuningAMtone','optoTuningFreq']

# if trialSubset not in ['', 'laseroff', 'laseron']:
#     raise ValueError("trialSubset must be '', 'laseroff', or 'laseron'")




eventTimeKeys = studyparams.EVENT_KEYS

timeKeyMetric = studyparams.TIME_KEY_METRIC

             


dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath, f'celldb_{subject}.h5')

# if not os.path.exists(dbFilename):
#     celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py'))
#     if not os.path.exists(dbPath):
#         os.mkdir(dbPath)
#     celldatabase.save_hdf(celldb,dbFilename)
# else:
#     celldb = celldatabase.load_hdf(dbFilename)


celldb = celldatabase.generate_cell_database(os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.py'))


outputFilename = os.path.join(dbPath, f'celldb_{subject}_laser_freqtuning.h5')

if studyparams.BLNORM:
    outputFilename  = outputFilename.replace('.h5','_norm.h5')

if studyparams.TEST:
    outputFilename = outputFilename.replace('.h5','_test.h5')

for sessionType in sessionTypes:
    timeRange = studyparams.TIME_RANGES_AM if 'AM' in sessionType else studyparams.TIME_RANGES_FREQ
    timeRangeDuration = {k:np.diff(timeRange[k])[0] for k in timeRange.keys()}
    
    # if trialSubset == '':
    #     outputFilename = os.path.join(dbPath, f'celldb_{subject}_{sessionType}.h5')
    # else:
    #     outputFilename = os.path.join(dbPath, f'celldb_{subject}_{sessionType}_{trialSubset}.h5')

    # # -- Load laseroff data --
    # if trialSubset in ['laseroff','laseron']:
    #     laserData = studyutils.load_laser_data()
        
    # -- Initialize the dictionaries for new data (with keys like: doiBaselineFiringRate) --
    measurements = ['Tone'+i for i in studyparams.METRICS]

    columnsDict = {}
    reagentsAll = {}

    sampleRate = 30000

    for indcell,dbRow in celldb.iterrows():
        spikeShape = dbRow['spikeShape']
        timeStep = len(spikeShape)/sampleRate
        timeVec = np.arange(0,timeStep-timeStep/len(spikeShape),timeStep/len(spikeShape))*1000

        


for sessionType in sessionTypes:
    if 'sham' in sessionType.lower():
        outputFilename  = outputFilename.replace('laser','sham')

    sessionParams = sessionType.split('_')
    # sessionPre = sessionType[len(sessionParams[0])+1:] +'_'
    sessionPre=''
    reagentsAll[sessionType] = studyparams.REAGENTS[sessionType]
    
    columnsDictThisSession = studyutils.process_database_parallel(sessionType, sessionPre, reagentsAll[sessionType], celldb,
                                                                    timeRange, timeRangeDuration, eventTimeKeys,
                                                                    measurements, studyparams, PLOT, TEST)
    columnsDict|=columnsDictThisSession

    for tile in reagentsAll[sessionType]:
        reagent = sessionPre+tile
        for tKey in eventTimeKeys:
            columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = \
                list(columnsDict[reagent+'ToneFiringRateEachFreq'+tKey])
            columnsDict[reagent+'ToneFiringRateEachFreqSmoothed'+tKey] = \
                list(columnsDict[reagent+'ToneFiringRateEachFreqSmoothed'+tKey])
            columnsDict[reagent+'ToneSigmaEachFreq'+tKey] = \
                list(columnsDict[reagent+'ToneSigmaEachFreq'+tKey])
            columnsDict[reagent+'ToneDiscrimEachFreq'+tKey] = \
                list(columnsDict[reagent+'ToneDiscrimEachFreq'+tKey])
            columnsDict[reagent+'ToneNormResponseEachOctave'+tKey] = \
                list(columnsDict[reagent+'ToneNormResponseEachOctave'+tKey])
            columnsDict[reagent+'ToneFiringRateEachOctave'+tKey] = \
                list(columnsDict[reagent+'ToneFiringRateEachOctave'+tKey])


celldbWithTuning = celldb.assign(**columnsDict)
# celldbWithTuning = celldbWithTuning[(celldbWithTuning['sessionType'].apply(lambda x: 'optoAMtone' in x))]

for sessionType in sessionTypes:
    sessionParams = sessionType.split('_')
    # sessionPre = sessionType[len(sessionParams[0])+1:] +'_'
    sessionPre = ''
    for eventKey in eventTimeKeys:
        for indr, tile in enumerate(reagentsAll[sessionType]):
            reagent = sessionPre + tile
            #celldbWithTuning[reagent+'ToneGaussianMax'+eventKey] = ( celldbWithTuning[reagent+'ToneGaussianA'+eventKey] +
            #                                      celldbWithTuning[reagent+'ToneGaussianY0'+eventKey] )
            negResponseThisReagent = celldbWithTuning[reagent+'ToneGaussianA'+eventKey]<0
            thisToneGaussianMax = ( celldbWithTuning[reagent+'ToneGaussianA'+eventKey] +
                                    celldbWithTuning[reagent+'ToneGaussianY0'+eventKey] )
            thisToneGaussianMax[negResponseThisReagent] = celldbWithTuning[reagent+'ToneGaussianY0'+eventKey]
            celldbWithTuning[reagent+'ToneGaussianMax'+eventKey] = thisToneGaussianMax
            celldbWithTuning[reagent+'ToneGaussianBandwidth'+eventKey] = \
                extraplots.gaussian_full_width_half_max(celldbWithTuning[reagent+'ToneGaussianSigma'+eventKey])
            baselineFiringRate = celldbWithTuning[reagent+'ToneBaselineFiringRate']
            celldbWithTuning[reagent+'ToneGaussianMaxChange'+eventKey] = np.abs(thisToneGaussianMax-baselineFiringRate)

celldbWithTuning['celldepth'] = studyutils.get_cell_depths(celldbWithTuning)
# -- Save the updated celldb --
if SAVE:
    celldatabase.save_hdf(celldbWithTuning, outputFilename)



### --- old code, unparallelized ---


# def process_cell(sessionType, sessionPre, reagents, dbRow, timeRange, 
#                  timeRangeDuration, eventTimeKeys, measurements, studyparams, 
#                  PLOT=False, TEST=False):
     
#     """Process a single cell row with proper index handling"""
#     columnsDict = {}
#     indRow = dbRow.name  # Capture the DataFrame index

#     try:
#         oneCell = ephyscore.Cell(dbRow)
#         ephysData, bdata = oneCell.load(sessionType)
#     except Exception as e:
#         print(f"Error processing {indRow}: {str(e)}")
#         return columnsDict

#     oneCell = ephyscore.Cell(dbRow)
#     ephysData, bdata = oneCell.load(sessionType)
#     tileEachTrial = np.array([f'C{i}R{j}' if i+j >= 0 else 'off' for i,j in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
#     possibleTile = np.unique(tileEachTrial)

#     spikeTimesAll = ephysData['spikeTimes']
#     eventOnsetTimesAll = ephysData['events']['stimOn']

#     stimEachTrialAll = bdata['currentFreq']
#     nTrialsAll = len(stimEachTrialAll)

#     # If the ephys data is 1 more than the bdata, delete the last ephys trial.
#     if len(stimEachTrialAll) == len(eventOnsetTimesAll)-1:
#         eventOnsetTimesAll = eventOnsetTimesAll[:nTrialsAll]
#     assert len(stimEachTrialAll) == len(eventOnsetTimesAll), \
#         "Number of trials in behavior and ephys do not match for {oneCell}"

#     # print(nTrialsAll,len(spikeTimesAll),len(eventOnsetTimesAll),len(stimEachTrialAll))

#     if PLOT:
#         indplot = 0; plt.clf()
#         plt.suptitle(f'{oneCell} [{indRow}]', fontweight='bold')
#     if indRow%20==0:
#         print(f'{indRow}/{len(celldb)} cells analyzed')
#     for tile in reagentsAll[sessionType]:
#         reagent = sessionPre+tile
#         trialInds = (tileEachTrial==tile)
#         # print(trialInds)

#         spikeTimes = spikeTimesAll
#         eventOnsetTimes = eventOnsetTimesAll[trialInds]

#         stimEachTrial = stimEachTrialAll[trialInds]
#         nTrials = len(stimEachTrial)
        
#         # print(nTrials,len(spikeTimes),len(eventOnsetTimes))

#         if nTrials == 0:
#             break

#         # -- Doing this before selecting trials by running/notrunning --
#         possibleStim = np.unique(stimEachTrial)
#         nStim = len(possibleStim)
        
#         spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
#             spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange['Full'])

#         trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

#         # -- Estimate baseline firing rate --
#         spikeCountMatBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                                 indexLimitsEachTrial,
#                                                                 timeRange['Baseline'])
#         baselineFiringRate = spikeCountMatBase.mean()/timeRangeDuration['Baseline']

#         # -- Store non-Event data in columns dictionary
#         columnsDict[reagent+'ToneBaselineFiringRate'] = baselineFiringRate
#         columnsDict[reagent+'ToneNtrials'] = nTrials

#         for tKey in eventTimeKeys:
#             # -- Estimate evoked firing rate for each stim --
#             spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                                     indexLimitsEachTrial,
#                                                                     timeRange[tKey])
#             nSpikesEachTrial = spikeCountMat[:,0]  # Flatten it

#             # -- Calculate nSpikes for each freq to test selectivity --
#             nSpikesEachStim = []
#             avgFiringRateEachStim = np.empty(nStim)
#             pValEvokedEachStim = np.empty(nStim)
#             for indStim, frequency in enumerate(possibleStim):
#                 nSpikesThisStim = nSpikesEachTrial[trialsEachCond[:,indStim]]
#                 nSpikesEachStim.append(nSpikesThisStim)
#                 avgFiringRateEachStim[indStim] = nSpikesThisStim.mean()/timeRangeDuration[tKey]
#                 # -- Calculate p-value for each stim --
#                 baselineSpikesThisStim = spikeCountMatBase[trialsEachCond[:,indStim],0]
#                 try:
#                     wStat, pValThisStim = stats.wilcoxon(nSpikesThisStim, baselineSpikesThisStim)
#                 except ValueError:
#                     pValThisStim = 1
#                 pValEvokedEachStim[indStim] = pValThisStim
#             try:
#                 nTrialsEachCond = trialsEachCond.sum(axis=0)>0
#                 nSpks = [nSpikesEachStim[ind] for ind in np.flatnonzero(nTrialsEachCond)]
#                 kStat, pValKruskal = stats.kruskal(*nSpks)
#                 #kStat, pValKruskal = stats.kruskal(*nSpikesEachStim)
#             except ValueError:
#                 pValKruskal = 1
#             pValEvokedMin = np.min(pValEvokedEachStim)

#             # -- Fit Gaussian to tuning data --
#             freqEachTrial = stimEachTrial
#             possibleFreq = possibleStim
#             logFreq = np.log2(freqEachTrial)
#             possibleLogFreq = np.log2(possibleFreq)
#             maxEvokedFiringRate = np.nanmax(avgFiringRateEachStim)
#             changeFromBaseline = avgFiringRateEachStim - baselineFiringRate
#             maxChangeFromBaseline = changeFromBaseline[np.nanargmax(np.abs(changeFromBaseline))]
#             avgEvokedFiringRate = np.nanmean(avgFiringRateEachStim)
            
#             #baselineFiringRate
#             # PARAMS: a, x0, sigma, y0
#             minS = studyparams.MIN_SIGMA
#             maxS = studyparams.MAX_SIGMA
#             if maxChangeFromBaseline >= 0:
#                 p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
#                 bounds = ([0, possibleLogFreq[0], minS, 0],
#                         [np.inf, possibleLogFreq[-1], maxS, np.inf])
#             else:
#                 p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
#                 bounds = ([-np.inf, possibleLogFreq[0], minS, 0],
#                         [0, possibleLogFreq[-1], maxS, np.inf])
#             try:
#                 firingRateEachTrial = nSpikesEachTrial/timeRangeDuration[tKey]
#                 fitParams, pcov = optimize.curve_fit(spikesanalysis.gaussian, logFreq,
#                                                     firingRateEachTrial, p0=p0, bounds=bounds)
#             except RuntimeError:
#                 print("Could not fit gaussian curve to tuning data.")
#                 fitParams = np.full(4, np.nan)
#                 Rsquared = 0
#             else:
#                 gaussianResp = spikesanalysis.gaussian(logFreq, *fitParams)
#                 residuals = firingRateEachTrial - gaussianResp
#                 ssquared = np.sum(residuals**2)
#                 ssTotal = np.sum((firingRateEachTrial-np.mean(firingRateEachTrial))**2)
#                 if ssTotal:
#                     Rsquared = 1 - (ssquared/ssTotal)
#                 else:
#                     print("Divide by zero error...ssTotal is zero")
#                     Rsquared = 0
#                 fullWidthHalfMax = 2.355*fitParams[2] # Sigma is fitParams[2]

#             # -- Store results in dictionary --
            
#             columnsDict[reagent+'ToneResponseMinPval'+tKey] = pValEvokedMin
#             columnsDict[reagent+'ToneSelectivityPval'+tKey] = pValKruskal
#             columnsDict[reagent+'ToneFiringRateBestFreq'+tKey] = maxEvokedFiringRate
#             columnsDict[reagent+'ToneAvgEvokedFiringRate'+tKey] = avgEvokedFiringRate
#             columnsDict[reagent+'ToneBestFreq'+tKey] = possibleFreq[avgFiringRateEachStim.argmax()]
#             columnsDict[reagent+'ToneGaussianA'+tKey] = fitParams[0]
#             columnsDict[reagent+'ToneGaussianX0'+tKey] = fitParams[1]
#             columnsDict[reagent+'ToneGaussianSigma'+tKey] = fitParams[2]
#             columnsDict[reagent+'ToneGaussianY0'+tKey] = fitParams[3]
#             columnsDict[reagent+'ToneGaussianRsquare'+tKey] = Rsquared
#             columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = avgFiringRateEachStim
#     return (indRow, columnsDict)


# for tile in reagentsAll[sessionType]:
    #     reagent = sessionPre+tile
    #     # print(reagent)
    #     for measurement in measurements[:2]:
    #         columnsDict[reagent+measurement] = np.full(len(celldb), np.nan)
    #     for tKey in eventTimeKeys:   
    #         for measurement in measurements[3:]:
    #             columnsDict[reagent+measurement+tKey] = np.full(len(celldb), np.nan)
    #         columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
    # if TEST:
    #     indRow = 46  # 46 # 55
    #     indRow = 53  # Inverted
    #     #indRow = 176
    #     indRow = 1533
    #     indRow = 1318
    #     indRow = 1501 # Wide going down
    #     indRow = 1583 # very flat
    #     #indRow = 67  # Did not fit before fixing p0(A)
    #     celldbToUse = celldb[(celldb['sessionType'].apply(lambda x: sessionType in x))].iloc[[indRow]]
    # else:
    #     celldbToUse = celldb[(celldb['sessionType'].apply(lambda x: sessionType in x))]

    # print(len(celldbToUse))

    # # Prepare task list
    # tasks = []
    # for _, dbRow in celldbToUse.iterrows():
    #     tasks.append((
    #         sessionType, sessionPre, reagentsAll[sessionType], dbRow,
    #         timeRange, timeRangeDuration, eventTimeKeys,
    #         measurements, studyparams,PLOT, TEST
    #     ))
    # # Configure parallel processing
    # n_workers = os.cpu_count() - 1  # Use all but one core
    # columnsDictEachRow = Parallel(n_jobs=n_workers, verbose=10)(
    #     delayed(studyutils.process_cell)(*task) for task in tasks
    # )

    # for row in columnsDictEachRow:
    #     indRow, columnsDictThisRow = row
    #     for key in columnsDictThisRow:
    #         columnsDict[key][indRow] = columnsDictThisRow[key]


    # for indRow, dbRow in celldbToUse.iterrows():
    #     oneCell = ephyscore.Cell(dbRow)
    #     ephysData, bdata = oneCell.load(sessionType)
    #     tileEachTrial = np.array([f'C{i}R{j}' if i+j >= 0 else 'off' for i,j in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
    #     possibleTile = np.unique(tileEachTrial)

    #     spikeTimesAll = ephysData['spikeTimes']
    #     eventOnsetTimesAll = ephysData['events']['stimOn']

    #     stimEachTrialAll = bdata['currentFreq']
    #     nTrialsAll = len(stimEachTrialAll)

    #     # If the ephys data is 1 more than the bdata, delete the last ephys trial.
    #     if len(stimEachTrialAll) == len(eventOnsetTimesAll)-1:
    #         eventOnsetTimesAll = eventOnsetTimesAll[:nTrialsAll]
    #     assert len(stimEachTrialAll) == len(eventOnsetTimesAll), \
    #         "Number of trials in behavior and ephys do not match for {oneCell}"

    #     # print(nTrialsAll,len(spikeTimesAll),len(eventOnsetTimesAll),len(stimEachTrialAll))

    #     if PLOT:
    #         indplot = 0; plt.clf()
    #         plt.suptitle(f'{oneCell} [{indRow}]', fontweight='bold')
    #     if indRow%20==0:
    #         print(f'{indRow}/{len(celldb)} cells analyzed')
    #     for tile in reagentsAll[sessionType]:
    #         reagent = sessionPre+tile
    #         trialInds = (tileEachTrial==tile)
    #         # print(trialInds)

    #         spikeTimes = spikeTimesAll
    #         eventOnsetTimes = eventOnsetTimesAll[trialInds]

    #         stimEachTrial = stimEachTrialAll[trialInds]
    #         nTrials = len(stimEachTrial)
            
    #         # print(nTrials,len(spikeTimes),len(eventOnsetTimes))

    #         if nTrials == 0:
    #             break

    #         # -- Doing this before selecting trials by running/notrunning --
    #         possibleStim = np.unique(stimEachTrial)
    #         nStim = len(possibleStim)
            
    #         spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
    #             spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange['Full'])

    #         trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

    #         # -- Estimate baseline firing rate --
    #         spikeCountMatBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
    #                                                                 indexLimitsEachTrial,
    #                                                                 timeRange['Baseline'])
    #         baselineFiringRate = spikeCountMatBase.mean()/timeRangeDuration['Baseline']

    #         # -- Store non-Event data in columns dictionary
    #         columnsDict[reagent+'ToneBaselineFiringRate'][indRow] = baselineFiringRate
    #         columnsDict[reagent+'ToneNtrials'][indRow] = nTrials

    #         for tKey in eventTimeKeys:
    #             # -- Estimate evoked firing rate for each stim --
    #             spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
    #                                                                     indexLimitsEachTrial,
    #                                                                     timeRange[tKey])
    #             nSpikesEachTrial = spikeCountMat[:,0]  # Flatten it

    #             # -- Calculate nSpikes for each freq to test selectivity --
    #             nSpikesEachStim = []
    #             avgFiringRateEachStim = np.empty(nStim)
    #             pValEvokedEachStim = np.empty(nStim)
    #             for indStim, frequency in enumerate(possibleStim):
    #                 nSpikesThisStim = nSpikesEachTrial[trialsEachCond[:,indStim]]
    #                 nSpikesEachStim.append(nSpikesThisStim)
    #                 avgFiringRateEachStim[indStim] = nSpikesThisStim.mean()/timeRangeDuration[tKey]
    #                 # -- Calculate p-value for each stim --
    #                 baselineSpikesThisStim = spikeCountMatBase[trialsEachCond[:,indStim],0]
    #                 try:
    #                     wStat, pValThisStim = stats.wilcoxon(nSpikesThisStim, baselineSpikesThisStim)
    #                 except ValueError:
    #                     pValThisStim = 1
    #                 pValEvokedEachStim[indStim] = pValThisStim
    #             try:
    #                 nTrialsEachCond = trialsEachCond.sum(axis=0)>0
    #                 nSpks = [nSpikesEachStim[ind] for ind in np.flatnonzero(nTrialsEachCond)]
    #                 kStat, pValKruskal = stats.kruskal(*nSpks)
    #                 #kStat, pValKruskal = stats.kruskal(*nSpikesEachStim)
    #             except ValueError:
    #                 pValKruskal = 1
    #             pValEvokedMin = np.min(pValEvokedEachStim)

    #             # -- Fit Gaussian to tuning data --
    #             freqEachTrial = stimEachTrial
    #             possibleFreq = possibleStim
    #             logFreq = np.log2(freqEachTrial)
    #             possibleLogFreq = np.log2(possibleFreq)
    #             maxEvokedFiringRate = np.nanmax(avgFiringRateEachStim)
    #             changeFromBaseline = avgFiringRateEachStim - baselineFiringRate
    #             maxChangeFromBaseline = changeFromBaseline[np.nanargmax(np.abs(changeFromBaseline))]
    #             avgEvokedFiringRate = np.nanmean(avgFiringRateEachStim)
                
    #             #baselineFiringRate
    #             # PARAMS: a, x0, sigma, y0
    #             minS = studyparams.MIN_SIGMA
    #             maxS = studyparams.MAX_SIGMA
    #             if maxChangeFromBaseline >= 0:
    #                 p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
    #                 bounds = ([0, possibleLogFreq[0], minS, 0],
    #                         [np.inf, possibleLogFreq[-1], maxS, np.inf])
    #             else:
    #                 p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
    #                 bounds = ([-np.inf, possibleLogFreq[0], minS, 0],
    #                         [0, possibleLogFreq[-1], maxS, np.inf])
    #             try:
    #                 firingRateEachTrial = nSpikesEachTrial/timeRangeDuration[tKey]
    #                 fitParams, pcov = optimize.curve_fit(spikesanalysis.gaussian, logFreq,
    #                                                     firingRateEachTrial, p0=p0, bounds=bounds)
    #             except RuntimeError:
    #                 print("Could not fit gaussian curve to tuning data.")
    #                 fitParams = np.full(4, np.nan)
    #                 Rsquared = 0
    #             else:
    #                 gaussianResp = spikesanalysis.gaussian(logFreq, *fitParams)
    #                 residuals = firingRateEachTrial - gaussianResp
    #                 ssquared = np.sum(residuals**2)
    #                 ssTotal = np.sum((firingRateEachTrial-np.mean(firingRateEachTrial))**2)
    #                 if ssTotal:
    #                     Rsquared = 1 - (ssquared/ssTotal)
    #                 else:
    #                     print("Divide by zero error...ssTotal is zero")
    #                     Rsquared = 0
    #                 fullWidthHalfMax = 2.355*fitParams[2] # Sigma is fitParams[2]

    #             # -- Store results in dictionary --
                
    #             columnsDict[reagent+'ToneResponseMinPval'+tKey][indRow] = pValEvokedMin
    #             columnsDict[reagent+'ToneSelectivityPval'+tKey][indRow] = pValKruskal
    #             columnsDict[reagent+'ToneFiringRateBestFreq'+tKey][indRow] = maxEvokedFiringRate
    #             columnsDict[reagent+'ToneAvgEvokedFiringRate'+tKey][indRow] = avgEvokedFiringRate
    #             columnsDict[reagent+'ToneBestFreq'+tKey][indRow] = possibleFreq[avgFiringRateEachStim.argmax()]
    #             columnsDict[reagent+'ToneGaussianA'+tKey][indRow] = fitParams[0]
    #             columnsDict[reagent+'ToneGaussianX0'+tKey][indRow] = fitParams[1]
    #             columnsDict[reagent+'ToneGaussianSigma'+tKey][indRow] = fitParams[2]
    #             columnsDict[reagent+'ToneGaussianY0'+tKey][indRow] = fitParams[3]
    #             columnsDict[reagent+'ToneGaussianRsquare'+tKey][indRow] = Rsquared
    #             columnsDict[reagent+'ToneFiringRateEachFreq'+tKey][indRow] = avgFiringRateEachStim

            # if PLOT:
            #     plt.clf()
            #     plt.suptitle(f'[{indRow}]  {oneCell}')
            #     plt.subplot(1,2,1)
            #     pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
            #                                                 indexLimitsEachTrial,
            #                                                 timeRange['Full'], trialsEachCond)
            #     plt.setp(pRaster, ms=0.5)
            #     plt.title(f'{reagent} {sessionType}')
                
            #     plt.subplot(1,2,2)
            #     pdots = plt.plot(possibleLogFreq, avgFiringRateEachStim, 'o')
            #     if not np.isnan(fitParams[0]):
            #         xvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
            #         yvals = spikesanalysis.gaussian(xvals, *fitParams)
            #         pfit = plt.plot(xvals, yvals, '-', lw=3)
            #     plt.ylabel('Firing rate (Hz)')
            #     plt.xlabel('Frequency (kHz)')
            #     xTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
            #     plt.xticks(possibleLogFreq, xTickLabels)
            #     plt.title(f'R2={Rsquared:0.4f}  s={fitParams[2]:0.4f}')
            #     plt.show()
            #     plt.pause(0.5);
            #     #print(fitParams)
            #     if reagent=='pre':
            #         sys.exit()