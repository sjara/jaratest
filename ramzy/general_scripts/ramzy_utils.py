"""
Functions for 2023acid project.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import spikesanalysis,behavioranalysis,ephyscore,extraplots
from joblib import Parallel,delayed
from scipy import stats
from scipy import optimize
import warnings
import figparams


warnings.simplefilter('ignore')


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

def find_RS_cells(celldb,samplingRate=30000,nt=61,threshold=300):
    timeDiffEachCell = peak_trough_time(celldb,samplingRate=samplingRate,nt=nt)
    
    return((timeDiffEachCell > threshold))


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

        # -- Store non-Event data in columns dictionary
        columnsDict[reagent+'ToneBaselineFiringRate'] = baselineFiringRate
        columnsDict[reagent+'ToneBaselineSigma'] = baselineSigma
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
            sigmaEachStim = np.empty(nStim)
            dprimeEachFreq = np.empty(nStim)
            pValEvokedEachStim = np.empty(nStim)
            

            for indStim, frequency in enumerate(possibleStim):
                nSpikesThisStim = nSpikesEachTrial[trialsEachCond[:,indStim]]
                nSpikesEachStim.append(nSpikesThisStim)
                avgFiringRateEachStim[indStim] = nSpikesThisStim.mean()/timeRangeDuration[tKey]
                sigmaEachStim[indStim] =np.std(nSpikesThisStim/timeRangeDuration[tKey])

                dprimeEachFreq[indStim] = \
                    (avgFiringRateEachStim[indStim]-baselineFiringRate)/baselineSigma

                

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
                kStat = 0
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
            columnsDict[reagent+'ToneSigmaEachFreq'+tKey] = sigmaEachStim
            columnsDict[reagent+'ToneDiscrimEachFreq'+tKey] = dprimeEachFreq
            columnsDict[reagent+'ToneMeanDiscrim'+tKey] = np.mean(dprimeEachFreq)
            columnsDict[reagent+'ToneDiscrimBestFreq'+tKey] = np.nanmax(abs(dprimeEachFreq))
            columnsDict[reagent+'ToneSigmaAvgFR'+tKey] = np.std(avgFiringRateEachStim)
            columnsDict[reagent+'ToneFanoFactor'+tKey] = (np.std(avgFiringRateEachStim)**2)/avgEvokedFiringRate
            columnsDict[reagent+'ToneVariabilityIndex'+tKey] = (np.std(avgFiringRateEachStim)**2)/maxEvokedFiringRate
            
            
            normResponseEachOctave = np.full(2*nStim-1,np.nan)
            avgFiringRateEachStimOff = columnsDict[reagentOff+'ToneFiringRateEachFreq'+tKey]
            bestFreqInd = np.nanargmax(avgFiringRateEachStim)
            centeringInd = nStim-1-bestFreqInd
            bestFreq = possibleStim[bestFreqInd]

            normResponseEachOctave[centeringInd:centeringInd+nStim] = avgFiringRateEachStim/max(avgFiringRateEachStimOff)
            
            columnsDict[reagent+'ToneNormResponseEachOctave'+tKey] = normResponseEachOctave



    return (indRow, columnsDict)


def process_database_parallel(sessionType, sessionPre, reagents, celldb, timeRange, 
                                timeRangeDuration, eventTimeKeys, measurements, studyparams, 
                                PLOT=False, DEBUG=False):
    columnsDict = {}
    for mod in reagents:
        reagent = sessionPre+str(mod)
        # print(reagent)
        for measurement in measurements[0]:
            columnsDict[reagent+measurement] = np.full(len(celldb), np.nan)
        for tKey in eventTimeKeys:   
            for measurement in measurements[1]:
                columnsDict[reagent+measurement+tKey] = np.full(len(celldb), np.nan)
            columnsDict[reagent+'ToneFiringRateEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneSigmaEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneDiscrimEachFreq'+tKey] = np.full((len(celldb),studyparams.N_FREQ), np.nan)
            columnsDict[reagent+'ToneNormResponseEachOctave'+tKey] = np.full((len(celldb),2*studyparams.N_FREQ - 1), np.nan)

    if DEBUG:
        indRow = 46  
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
    n_workers = -2  # Use all but one core
    columnsDictEachRow = Parallel(n_jobs=n_workers,verbose=10)(
        delayed(process_cell)(*task) for task in tasks
    )

    
    for row in columnsDictEachRow:
        indRow, columnsDictThisRow = row
        for key in columnsDictThisRow:
            columnsDict[key][indRow] = columnsDictThisRow[key]

    return columnsDict
    
def plot_stim(yLims, stimDuration, stimLineWidth=6, stimColor=figparams.colorStim,yposOffset=0,xposOffset=0):
    yPos = (1.02+stimDuration*0.04*yposOffset)*yLims[-1] + 0.075*(yLims[-1]-yLims[0])*2*stimDuration
    pstim = plt.plot([xposOffset, stimDuration], 2*[yPos], lw=stimLineWidth, color=stimColor,
                     clip_on=False, solid_capstyle='butt')
    return pstim[0]

def get_shared_ax(gsSubFig,keep='none',yaxis=False):
    sharedAx = plt.subplot(gsSubFig)
    extraplots.boxoff(sharedAx,keep=keep,yaxis=yaxis)
    sharedAx.tick_params('both',labelcolor='#0000')

    return sharedAx

def gs_shared_xylabs(gsSubFig,xlab='',ylab='',xpad=5,ypad=10,fontsize=16):
    sharedAx = get_shared_ax(gsSubFig)
    sharedAx.set_xlabel(xlab,labelpad=xpad,size=fontsize)
    sharedAx.set_ylabel(ylab,labelpad=ypad,size=fontsize)

def gs_panel_label(gsSubFig,label='A',fontSize=24,hpad=0,vpad=0):
    sharedAx = get_shared_ax(gsSubFig)
    sharedAx.text(-0.25+hpad, 1.05+vpad, label, transform=sharedAx.transAxes, 
                    fontsize=fontSize, fontweight='bold')
    
def subplot_panel_label(sharedAx,label='A',fontSize=24,hpad=0,vpad=0):
    sharedAx.text(-0.25+hpad, 1.05+vpad, label, transform=sharedAx.transAxes, 
                    fontsize=fontSize, fontweight='bold')