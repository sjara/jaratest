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
reload(studyparams)
reload(spikesanalysis)
reload(ephyscore)

sessionType='poniAM'
DEBUG = 0
PLOT = 0
SAVE = 1

subject = sys.argv[1]
# sessionDate = sys.argv[2]
# probeDepth = int(sys.argv[3])
# -- Check if trialSubset should be changed. Options: 'laseroff', or 'laseron' --
if len(sys.argv)==5:
    trialSubset = sys.argv[4]
else:
    trialSubset = ''
if trialSubset not in ['', 'laseroff', 'laseron']:
    raise ValueError("trialSubset must be '', 'laseroff', or 'laseron'")

timeRange = studyparams.TIME_RANGES

eventTimeKeys = studyparams.EVENT_KEYS

timeKeyMetric = studyparams.TIME_KEY_METRIC

             
timeRangeDuration = {k:np.diff(timeRange[k])[0] for k in timeRange.keys()}

dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath, f'celldb_{subject}.h5')
celldb = celldatabase.load_hdf(dbFilename)
if trialSubset == '':
    outputFilename = os.path.join(dbPath, f'celldb_{subject}_AMtuning.h5')
else:
    outputFilename = os.path.join(dbPath, f'celldb_{subject}_AMtuning_{trialSubset}.h5')

# # -- Load laseroff data --
# if trialSubset in ['laseroff','laseron']:
#     laserData = studyutils.load_laser_data()
    
# -- Initialize the dictionaries for new data (with keys like: doiBaselineFiringRate) --
measurements = ['RateBaselineFiringRate', 'RateNtrials', 'RateFiringRateEachFreq',
                'RateResponseMinPval', 
                'RateSelectivityPval', 'RateFiringRateBestFreq', 'RateBestFreq', 
                'RateAvgEvokedFiringRate', 'RateGaussianA', 'RateGaussianX0', 'RateGaussianSigma', 
                'RateGaussianY0', 'RateGaussianRsquare']

columnsDict = {}
for reagent in studyparams.REAGENTS_IMAGE:
    for measurement in measurements[:2]:
        columnsDict[reagent+measurement] = np.full(len(celldb), np.nan)
    for tKey in eventTimeKeys:   
        for measurement in measurements[3:]:
            columnsDict[reagent+measurement+tKey] = np.full(len(celldb), np.nan)
        columnsDict[reagent+'RateFiringRateEachFreq'+tKey] = np.full((len(celldb),studyparams.N_RATE), np.nan)



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

print(len(celldbToUse))

for indRow, dbRow in celldbToUse.iterrows():
    oneCell = ephyscore.Cell(dbRow)
    ephysData, bdata = oneCell.load(sessionType)
    tileEachTrial = np.array([f'C{i}R{j}' for i,j in zip(bdata['currentStimRow'],bdata['currentStimCol'])])
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

    if PLOT:
        indplot = 0; plt.clf()
        plt.suptitle(f'{oneCell} [{indRow}]', fontweight='bold')
    if indRow%20==0:
        print(f'{indRow}/{len(celldb)} cells analyzed')
    for reagent in studyparams.REAGENTS_IMAGE:
        # print(reagent)
        trialInds = (tileEachTrial==reagent)
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
        columnsDict[reagent+'RateBaselineFiringRate'][indRow] = baselineFiringRate
        columnsDict[reagent+'RateNtrials'][indRow] = nTrials

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
                print("Could not fit gaussian curve to tuning data.")
                fitParams = np.full(4, np.nan)
                Rsquared = 0
            else:
                gaussianResp = spikesanalysis.gaussian(logFreq, *fitParams)
                residuals = firingRateEachTrial - gaussianResp
                ssquared = np.sum(residuals**2)
                ssTotal = np.sum((firingRateEachTrial-np.mean(firingRateEachTrial))**2)
                Rsquared = 1 - (ssquared/ssTotal)
                fullWidthHalfMax = 2.355*fitParams[2] # Sigma is fitParams[2]

            # -- Store results in dictionary --
            
            columnsDict[reagent+'RateResponseMinPval'+tKey][indRow] = pValEvokedMin
            columnsDict[reagent+'RateSelectivityPval'+tKey][indRow] = pValKruskal
            columnsDict[reagent+'RateFiringRateBestFreq'+tKey][indRow] = maxEvokedFiringRate
            columnsDict[reagent+'RateAvgEvokedFiringRate'+tKey][indRow] = avgEvokedFiringRate
            columnsDict[reagent+'RateBestFreq'+tKey][indRow] = possibleFreq[avgFiringRateEachStim.argmax()]
            columnsDict[reagent+'RateGaussianA'+tKey][indRow] = fitParams[0]
            columnsDict[reagent+'RateGaussianX0'+tKey][indRow] = fitParams[1]
            columnsDict[reagent+'RateGaussianSigma'+tKey][indRow] = fitParams[2]
            columnsDict[reagent+'RateGaussianY0'+tKey][indRow] = fitParams[3]
            columnsDict[reagent+'RateGaussianRsquare'+tKey][indRow] = Rsquared
            columnsDict[reagent+'RateFiringRateEachFreq'+tKey][indRow] = avgFiringRateEachStim

        if PLOT:
            plt.clf()
            plt.suptitle(f'[{indRow}]  {oneCell}')
            plt.subplot(1,2,1)
            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                           indexLimitsEachTrial,
                                                           timeRange['Full'], trialsEachCond)
            plt.setp(pRaster, ms=0.5)
            plt.title(f'{reagent} {sessionType}')
            
            plt.subplot(1,2,2)
            pdots = plt.plot(possibleLogFreq, avgFiringRateEachStim, 'o')
            if not np.isnan(fitParams[0]):
                xvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
                yvals = spikesanalysis.gaussian(xvals, *fitParams)
                pfit = plt.plot(xvals, yvals, '-', lw=3)
            plt.ylabel('Firing rate (Hz)')
            plt.xlabel('Frequency (kHz)')
            xTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
            plt.xticks(possibleLogFreq, xTickLabels)
            plt.title(f'R2={Rsquared:0.4f}  s={fitParams[2]:0.4f}')
            plt.show()
            plt.pause(0.5);
            #print(fitParams)
            if reagent=='pre':
                sys.exit()

for reagent in studyparams.REAGENTS_IMAGE:
    for tKey in eventTimeKeys:
        columnsDict[reagent+'RateFiringRateEachFreq'+tKey] = \
            list(columnsDict[reagent+'RateFiringRateEachFreq'+tKey])

celldbWithTuning = celldb.assign(**columnsDict)

for eventKey in eventTimeKeys:
    for indr, reagent in enumerate(studyparams.REAGENTS_IMAGE):
        #celldbWithTuning[reagent+'RateGaussianMax'+eventKey] = ( celldbWithTuning[reagent+'RateGaussianA'+eventKey] +
        #                                      celldbWithTuning[reagent+'RateGaussianY0'+eventKey] )
        negResponseThisReagent = celldbWithTuning[reagent+'RateGaussianA'+eventKey]<0
        thisRateGaussianMax = ( celldbWithTuning[reagent+'RateGaussianA'+eventKey] +
                                celldbWithTuning[reagent+'RateGaussianY0'+eventKey] )
        thisRateGaussianMax[negResponseThisReagent] = celldbWithTuning[reagent+'RateGaussianY0'+eventKey]
        celldbWithTuning[reagent+'RateGaussianMax'+eventKey] = thisRateGaussianMax
        celldbWithTuning[reagent+'RateGaussianBandwidth'+eventKey] = \
            extraplots.gaussian_full_width_half_max(celldbWithTuning[reagent+'RateGaussianSigma'+eventKey])
        baselineFiringRate = celldbWithTuning[reagent+'RateBaselineFiringRate']
        celldbWithTuning[reagent+'RateGaussianMaxChange'+eventKey] = np.abs(thisRateGaussianMax-baselineFiringRate)

# -- Save the updated celldb --
if SAVE:
    celldatabase.save_hdf(celldbWithTuning, outputFilename)

# -- Useful for debugging --    
# for k,v in celldbWithTuning.iloc[46].items(): print(f'{k}:\t {v}')




# cellInds = np.arange(len(celldbToUse))

# ensemble = ephyscore.CellEnsemble(celldbToUse)
# ephysData,bdata = ensemble.load(sessionType)

# stimEachTrial = bdata['currentFreq']
# possibleStim = np.unique(stimEachTrial)
# nStim = len(possibleStim)
# nTrials = len(stimEachTrial)

# laserEachTrial = bdata['laserTrial']
# onTrials = np.nonzero(laserEachTrial)[0]
# offTrials = np.nonzero(1-laserEachTrial)[0]

# laserCondInds = {
#     'on':onTrials,
#     'off':offTrials
# }

# spikeTimesAll = ephysData['spikeTimes']
# eventOnsetTimesAll = ephysData['events']['stimOn'][:nTrials]
    
# for reagent in studyparams.REAGENTS:
#     print(f'Analyzing {reagent} trials')
#     trialInds = laserCondInds[reagent]
    
#     spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
#         ensemble.eventlocked_spiketimes(eventOnsetTimesAll[trialInds], timeRange['Full'])

#     trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial[trialInds], possibleStim)

#     for count, indRow in enumerate(cellInds):
#         if count%20==0:
#             print(f'{count}/{len(cellInds)} cells analyzed')
#         spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
#             spikeTimesFromEventOnsetAll[indRow], trialIndexForEachSpikeAll[indRow], indexLimitsEachTrialAll[indRow]
        
#         # -- Estimate baseline firing rate --
#         spikeCountMatBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                                     indexLimitsEachTrial,
#                                                                     timeRange['Baseline'])
#         baselineFiringRate = spikeCountMatBase.mean()/timeRangeDuration['Baseline']

#         # -- Estimate evoked firing rate for each stim --
#         spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                                     indexLimitsEachTrial,
#                                                                     timeRange['Evoked'])
#         nSpikesEachTrial = spikeCountMat[:,0]  # Flatten it

#         # -- Calculate nSpikes for each freq to test selectivity --
#         nSpikesEachStim = []
#         avgFiringRateEachStim = np.empty(nStim)
#         pValEvokedEachStim = np.empty(nStim)
#         for indStim, frequency in enumerate(possibleStim):
#             nSpikesThisStim = nSpikesEachTrial[trialsEachCond[:,indStim]]
#             nSpikesEachStim.append(nSpikesThisStim)
#             avgFiringRateEachStim[indStim] = nSpikesThisStim.mean()/timeRangeDuration['Evoked']
#             # -- Calculate p-value for each stim --
#             baselineSpikesThisStim = spikeCountMatBase[trialsEachCond[:,indStim],0]
#             try:
#                 wStat, pValThisStim = stats.wilcoxon(nSpikesThisStim, baselineSpikesThisStim)
#             except ValueError:
#                 pValThisStim = 1
#             pValEvokedEachStim[indStim] = pValThisStim
#         try:
#             nTrialsEachCond = trialsEachCond.sum(axis=0)>0
#             nSpks = [nSpikesEachStim[ind] for ind in np.flatnonzero(nTrialsEachCond)]
#             kStat, pValKruskal = stats.kruskal(*nSpks)
#             #kStat, pValKruskal = stats.kruskal(*nSpikesEachStim)
#         except ValueError:
#             pValKruskal = 1
#         pValEvokedMin = np.min(pValEvokedEachStim)

#         # -- Fit Gaussian to tuning data --
#         freqEachTrial = stimEachTrial[trialInds]
#         possibleFreq = possibleStim
#         logFreq = np.log2(freqEachTrial)
#         possibleLogFreq = np.log2(possibleFreq)
#         maxEvokedFiringRate = np.nanmax(avgFiringRateEachStim)
#         changeFromBaseline = avgFiringRateEachStim - baselineFiringRate
#         maxChangeFromBaseline = changeFromBaseline[np.nanargmax(np.abs(changeFromBaseline))]
#         avgEvokedFiringRate = np.nanmean(avgFiringRateEachStim)
        
#         #baselineFiringRate
#         # PARAMS: a, x0, sigma, y0
#         minS = studyparams.MIN_SIGMA
#         maxS = studyparams.MAX_SIGMA
#         if maxChangeFromBaseline >= 0:
#             p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
#             bounds = ([0, possibleLogFreq[0], minS, 0],
#                         [np.inf, possibleLogFreq[-1], maxS, np.inf])
#         else:
#             p0 = [maxChangeFromBaseline, possibleLogFreq[nStim//2], 1, baselineFiringRate]
#             bounds = ([-np.inf, possibleLogFreq[0], minS, 0],
#                         [0, possibleLogFreq[-1], maxS, np.inf])
#         try:
#             firingRateEachTrial = nSpikesEachTrial/timeRangeDuration['Evoked']
#             fitParams, pcov = optimize.curve_fit(spikesanalysis.gaussian, logFreq,
#                                                     firingRateEachTrial, p0=p0, bounds=bounds)
#         except RuntimeError:
#             print("Could not fit gaussian curve to tuning data.")
#             fitParams = np.full(4, np.nan)
#             Rsquared = 0
#         else:
#             gaussianResp = spikesanalysis.gaussian(logFreq, *fitParams)
#             residuals = firingRateEachTrial - gaussianResp
#             ssquared = np.sum(residuals**2)
#             ssTotal = np.sum((firingRateEachTrial-np.mean(firingRateEachTrial))**2)
#             Rsquared = 1 - (ssquared/ssTotal)
#             fullWidthHalfMax = 2.355*fitParams[2] # Sigma is fitParams[2]

#         # -- Store results in dictionary --
#         columnsDict[reagent+'RateBaselineFiringRate'][indRow] = baselineFiringRate
#         columnsDict[reagent+'RateResponseMinPval'][indRow] = pValEvokedMin
#         columnsDict[reagent+'RateSelectivityPval'][indRow] = pValKruskal
#         columnsDict[reagent+'RateFiringRateBestFreq'][indRow] = maxEvokedFiringRate
#         columnsDict[reagent+'RateAvgEvokedFiringRate'][indRow] = avgEvokedFiringRate
#         columnsDict[reagent+'RateBestFreq'][indRow] = possibleFreq[avgFiringRateEachStim.argmax()]
#         columnsDict[reagent+'RateGaussianA'][indRow] = fitParams[0]
#         columnsDict[reagent+'RateGaussianX0'][indRow] = fitParams[1]
#         columnsDict[reagent+'RateGaussianSigma'][indRow] = fitParams[2]
#         columnsDict[reagent+'RateGaussianY0'][indRow] = fitParams[3]
#         columnsDict[reagent+'RateGaussianRsquare'][indRow] = Rsquared
#         columnsDict[reagent+'RateNtrials'][indRow] = nTrials
#         columnsDict[reagent+'RateFiringRateEachFreq'][indRow] = avgFiringRateEachStim

#     if PLOT:
#         plt.clf()
#         plt.figure()
#         plt.suptitle(f'[{indRow}]  {oneCell}')
#         plt.subplot(1,2,1)
#         pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         timeRange['Full'], trialsEachCond)
#         plt.setp(pRaster, ms=0.5)
#         plt.title(f'{reagent} {sessionType}')
        
#         plt.subplot(1,2,2)
#         pdots = plt.plot(possibleLogFreq, avgFiringRateEachStim, 'o')
#         if not np.isnan(fitParams[0]):
#             xvals = np.linspace(possibleLogFreq[0], possibleLogFreq[-1], 60)
#             yvals = spikesanalysis.gaussian(xvals, *fitParams)
#             pfit = plt.plot(xvals, yvals, '-', lw=3)
#         plt.ylabel('Firing rate (Hz)')
#         plt.xlabel('Frequency (kHz)')
#         xTickLabels = [f'{freq/1000:0.0f}' for freq in possibleFreq]
#         plt.xticks(possibleLogFreq, xTickLabels)
#         plt.title(f'R2={Rsquared:0.4f}  s={fitParams[2]:0.4f}')
#         plt.show()
#         plt.pause(0.5);
#         #print(fitParams)
#         if reagent=='pre':
#             sys.exit()

# for reagent in studyparams.REAGENTS:
#     columnsDict[reagent+'RateFiringRateEachFreq'] = list(columnsDict[reagent+'RateFiringRateEachFreq'])
# celldbWithTuning = celldb.assign(**columnsDict)

# # -- Save the updated celldb --
# if SAVE:
#     celldatabase.save_hdf(celldbWithTuning, outputFilename)

# # -- Useful for debugging --    
# # for k,v in celldbWithTuning.iloc[46].items(): print(f'{k}:\t {v}')