"""
This script plots changes in freq tuning from off to on.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import scipy.stats as stats 
import poni_params as studyparams
import poni_utils as studyutils
import ponifig_params as figparams
import importlib
importlib.reload(figparams)
importlib.reload(studyutils)
importlib.reload(studyparams)

pd.set_option('mode.chained_assignment', None)

subject = sys.argv[1]
sessionDate = sys.argv[2]
probeDepth = int(sys.argv[3])
eventKey = sys.argv[4]

if len(sys.argv)==6:
    justCurves = sys.argv[5]
else:
    justCurves = False

SAVE_FIGURE = 1
SAVE=0
studyName = 'patternedOpto'
# BTRmetric = 'ToneResponseMinPval'
# BTRmetric = 'ToneGaussianMaxChange'
BTRmetric = 'ToneGaussianRsquare'
outputDir = os.path.join(settings.FIGURES_DATA_PATH,studyName,subject,sessionDate)
figFilename = f'plots_{eventKey}_AMtuning' # Do not include extension
figFormat = 'pdf' #or 'svg'
figSize = [16, 8] # In inches

cellsToPlot = [61,129,185]
# cellsToPlot=False



# if len(sys.argv)==6:
#     trialSubset = sys.argv[5]
#     figFilename = figFilename + '_' + trialSubset
#     figFormat = 'pdf'
# else:
#     trialSubset = ''
# if trialSubset not in ['', 'laser', 'nonLaser']:
#     raise ValueError("trialSubset must be '', 'laser', 'nonLaser'")

trialSubset = ''

# -- Example cells to plot --
#Cells with decrease: 149, 200, 430, 432, 669, 732, 806, 1145 
# cellsToPlot = [149, 125, 83]   # Best: 149, 200, 1145
#cellsToPlot = [1145, 125, 83]   # Best: 149, 200, 1145
#cellsToPlot = [407, 1320, 1474]  # Give negative estimated max firing rate on on


fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.002, 0.215, 0.43, 0.65, 0.825]   # Horiz position for panel labels
labelPosY = [0.96, 0.47]    # Vert position for panel labels

# -- Assigned colors (defined in figparams) --
colorsRasterDark = figparams.colors
colorsRasterLight = figparams.colorsLight
pColor = '0.5'
#colorsRasterDark = {'off': figparams.colors['off'], 'on': figparams.colors['on']} 
#colorsRasterLight = {'off': figparams.colorsLight['off'], 'on': figparams.colorsLight['on']} 
#Oddball = figparams.colors['oddball']
#colorStandard = figparams.colors['standard']

rasterMarkerSize = 2.0

def plot_stim(yLims, stimDuration, stimLineWidth=6, stimColor=figparams.colorStim):
    yPos = 1.02*yLims[-1] + 0.075*(yLims[-1]-yLims[0])
    pstim = plt.plot([0, stimDuration], 2*[yPos], lw=stimLineWidth, color=stimColor,
                     clip_on=False, solid_capstyle='butt')
    return pstim[0]

# -- Load data --
dbPath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,f'celldb_{subject}_freqtuning.h5')
celldbAll = celldatabase.load_hdf(dbFilename)



if trialSubset == 'laser':
    dbFilename = os.path.join(dbPath,f'celldb_{subject}_freqtuning_laser.h5')
    celldb = celldatabase.load_hdf(dbFilename)
elif trialSubset == 'nonLaser':
    dbFilename = os.path.join(dbPath,f'celldb_{subject}_freqtuning_nonLaser.h5')
    celldb = celldatabase.load_hdf(dbFilename)
else:
    celldb = celldbAll[(celldbAll.date==sessionDate) & (celldbAll.pdepth==probeDepth)]


# -- Find best time range for each cell --
if eventKey == 'BTR':
    # print(f'Finding best time ranges based on {BTRmetric}')
    bestKeys = studyutils.find_best_time_keys(celldb,BTRmetric,['Evoked','Delayed','Sustained','Onset','Offset'])
    # bestKeys = studyutils.find_best_time_keys(celldb,BTRmetric)
    celldb['BestTimeRange']=bestKeys
    measurements = studyparams.METRICS[2:] 
    for indr,reagent in enumerate(studyparams.REAGENTS_IMAGE):
        for metric in studyparams.METRICS[2:]:
            BTRs = []
            for indc,dbRow in celldb.iterrows():
                tKey = dbRow['BestTimeRange']
                BTRs.append(dbRow[reagent+metric+tKey])
            
            celldb[reagent+metric+'BTR'] = BTRs


# -- Process data --
maxChangeFactor = studyparams.MAX_CHANGE_FACTOR


# selective = studyutils.find_freq_selective(celldb, minR2=studyparams.MIN_R_SQUARED)
goodFit = studyutils.find_good_gaussian_fit(celldb, eventKey,minR2=studyparams.MIN_R_SQUARED)
anyFiton = ~np.isnan(celldb['C0R0ToneGaussianA'+eventKey])
anyFitboth = anyFiton
posResponse = ~np.isnan(celldb['C0R0ToneGaussianA'+eventKey])

for indr, reagent in enumerate(studyparams.REAGENTS_IMAGE):
    anyFitboth &= ~np.isnan(celldb[reagent+'ToneGaussianA'+eventKey])
    #celldb[reagent+'ToneGaussianMax'+eventKey] = ( celldb[reagent+'ToneGaussianA'+eventKey] +
    #                                      celldb[reagent+'ToneGaussianY0'+eventKey] )
    negResponseThisReagent = celldb[reagent+'ToneGaussianA'+eventKey]<0
    thisToneGaussianMax = ( celldb[reagent+'ToneGaussianA'+eventKey] +
                            celldb[reagent+'ToneGaussianY0'+eventKey] )
    thisToneGaussianMax[negResponseThisReagent] = celldb[reagent+'ToneGaussianY0'+eventKey]
    celldb[reagent+'ToneGaussianMax'+eventKey] = thisToneGaussianMax
    celldb[reagent+'ToneGaussianBandwidth'+eventKey] = \
        extraplots.gaussian_full_width_half_max(celldb[reagent+'ToneGaussianSigma'+eventKey])
    baselineFiringRate = celldb[reagent+'ToneBaselineFiringRate']
    celldb[reagent+'ToneGaussianMaxChange'+eventKey] = np.abs(thisToneGaussianMax-baselineFiringRate)
    posResponse &= (celldb[reagent+'ToneGaussianA'+eventKey]>0)

# responsive = studyutils.find_tone_responsive_cells(celldb, eventKey, frThreshold=4,allreagents=True)
#posResponse = (celldbAll['preToneGaussianA'+eventKey]>0) #& (celldbAll['offToneGaussianA'+eventKey]>0) #& (celldbAll['onToneGaussianA'+eventKey]>0)
# posResponse = (celldb['offToneGaussianA'+eventKey]>0) & (celldb['onToneGaussianA'+eventKey]>0)
#posResponse = (celldbAll['onToneGaussianA'+eventKey]>0)
#posResponse = (celldb['offToneGaussianMax'+eventKey]>0) & (celldb['onToneGaussianMax'+eventKey]>0)
posResponse &= (celldb['C0R0ToneGaussianA'+eventKey]>3) #& (celldb['offToneFiringRateBestFreq'+eventKey] > 2)
steadyParams = ['ToneBaselineFiringRate'] 
steady = studyutils.find_steady_cells(celldb, steadyParams, maxChangeFactor)


selectedCells = goodFit & posResponse & anyFitboth #& steady 
# selectedCells = goodFit & posResponse & anyFitboth #& responsive
# selectedCells = responsive  & goodFit 
# selectedCells = steady & goodFit & posResponse & anyFitboth
# selectedCells = posResponse & goodFit & anyFitboth
# selectedCells = responsive  & goodFit 

# -- Save the updated celldb --
if SAVE:
    dbFilename = os.path.join(dbPath,f'celldb_{subject}_{sessionDate}_freqtuning.h5')
    celldatabase.save_hdf(celldb, dbFilename)
'''
metrics = ['ToneGaussianX0', 'ToneGaussianBandwidth', 'ToneGaussianMax']
metricsLabel = ['BF', 'Bandwidth', 'Max resp']
metricsUnits = ['kHz', 'oct', 'spk/s']
metricLims = [[np.log2(2000), np.log2(40000)], [0, 10], [0, 120]]
metricTicks = [[2000, 8000, 32000], [0, 5, 10], [0, 60, 120]]
'''


colorsTuning = figparams.colors

reagentsToRaster = []
for indc,dbRow in celldb.iterrows():
    thisGauss = sorted([reagent for reagent in studyparams.REAGENTS_IMAGE], key=lambda x: dbRow[x+'ToneGaussianA'+eventKey])
    reagentsToRaster.append((thisGauss[-1],thisGauss[0]))

# -- Plot examples --
if not justCurves:
    metrics = ['ToneGaussianX0'+eventKey, 'ToneGaussianBandwidth'+eventKey, 'ToneGaussianMaxChange'+eventKey]
    metricsLabel = ['BF', 'Width', 'Max Δ']
    #metricsLabel = ['BF', 'Bandwidth', 'Resp at BF']
    metricsUnits = ['kHz', 'norm.', 'spk/s']
    metricLims = [[np.log2(2000), np.log2(40000)], [0, 6], [0, 10]]
    metricTicks = [[2000, 8000, 32000], [0, 5, 10], [0, 25, 50]]


    # -- Plot results --
    fig = plt.gcf()
    fig.clf()
    fig.set_facecolor('w')

    # -- Main gridspec --
    gsMain = gridspec.GridSpec(1, 4, width_ratios=[0.2, 0.2, 0.2, 0.4])
    gsMain.update(left=0.04, right=0.99, top=0.95, bottom=0.1, wspace=0.35, hspace=0.3)

    # -- Show panel labels --
    for indp, plabel in enumerate(['A','B','C','D','E']):
        plt.figtext(labelPosX[indp], labelPosY[0], plabel, fontsize=fontSizePanel, fontweight='bold')
    for indp, plabel in enumerate(['F','G']):
        plt.figtext(labelPosX[indp+3], labelPosY[1], plabel, fontsize=fontSizePanel, fontweight='bold')

    # -- Raster and PSTH parameters --
    timeRange = [-0.2, 0.4]
    binWidth = 0.010
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 2 
    lwPsth = 2.5
    downsampleFactorPsth = 1

    sessionType = 'poniFreq'
    for indcell, cellInd in enumerate(cellsToPlot):
        gsExample = gsMain[0, indcell].subgridspec(2, 1, hspace=0.35)
        gsRasters = gsExample[0].subgridspec(2, 1, hspace=0.1)
        axTuning = plt.subplot(gsExample[1])
        #cellInd, dbRow = celldatabase.find_cell(celldb, **cellsToPlot[indcell])
        dbRow = celldb.iloc[cellsToPlot[indcell]]
        thisGauss = sorted([reagent for reagent in studyparams.REAGENTS_IMAGE], 
                           key=lambda x: dbRow[x+'ToneGaussianA'+eventKey])
        reagentsToRaster = (thisGauss[-1],thisGauss[0])
        oneCell = ephyscore.Cell(dbRow)
        reagentsToPlot = studyparams.REAGENTS_IMAGE
        reagentLabels = reagentsToPlot
        allFits = []
        ephysData, bdata = oneCell.load(sessionType)  
        tileEachTrial = np.array([f'C{i}R{j}' for i,j in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
        possibleTile = np.unique(tileEachTrial)
        nTrialsAll = len(tileEachTrial)
        eventOnsetTimesAll = ephysData['events']['stimOn'][:nTrialsAll]
        stimEachTrialAll = bdata['currentFreq']

        for indr, reagent in enumerate(studyparams.REAGENTS_IMAGE):
            trialInds = (tileEachTrial == reagent)
            
            spikeTimes = ephysData['spikeTimes']
            
            eventOnsetTimes = eventOnsetTimesAll[trialInds]
            stimEachTrial = stimEachTrialAll[trialInds]

            nTrials = len(stimEachTrial)
            
            # -- onng this before selecting trials by laser/nonLaser --
            possibleStim = np.unique(stimEachTrial)
            nStim = len(possibleStim)
            
            stimDuration = bdata['stimDur'][-1]

            # If the ephys data is 1 more than the bdata, delete the last ephys trial.
            if len(stimEachTrial) == len(eventOnsetTimes)-1:
                eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
            assert len(stimEachTrial) == len(eventOnsetTimes), \
                "Number of trials in behavior and ephys do not match for {oneCell}"

            (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

            trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

            # -- Estimate evoked firing rate for each stim --
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                     indexLimitsEachTrial,
                                                                     timeRange)

            if reagent in reagentsToRaster:
                indrast = 0 if reagent == reagentsToRaster[0] else 1
                # -- Plot Raster --
                axRaster = plt.subplot(gsRasters[indrast])
                possibleStimInKHz = possibleStim/1000
                rasterLabels = ['']*nStim;
                rasterLabels[0] = int(possibleStimInKHz[0])
                rasterLabels[-1] = int(possibleStimInKHz[-1])
                colorEachCond = [colorsRasterDark[reagent], colorsRasterLight[reagent]]*(nStim//2+1)
                (pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial, timeRange,
                                                                trialsEachCond, labels=rasterLabels,
                                                                colorEachCond=colorEachCond,
                                                                rasterized=True)
                
                
                plt.setp(pRasterS, ms=rasterMarkerSize)
                if indrast==1:
                    plt.xlabel('Time (s)', fontsize=fontSizeLabels)
                plt.ylabel('Freq (kHz)', fontsize=fontSizeLabels)
                if eventKey == 'BTR':
                    plt.axvline(studyparams.TIME_RANGES[dbRow['BestTimeRange']][0],color='r',zorder=-10)
                    plt.axvline(studyparams.TIME_RANGES[dbRow['BestTimeRange']][1],color='r',zorder=-10)
                #axRaster.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
                if indrast==0:
                    plot_stim(plt.ylim(), stimDuration)
                    plt.title(f'Cell #{cellInd}',loc='left')
                    axRaster.set_xticklabels([])

            # -- Plot tuning curve --
            plt.sca(axTuning)
            firingRates = dbRow[reagent+'ToneFiringRateEachFreq'+eventKey]
            fitParams = [dbRow[reagent+'ToneGaussianA'+eventKey], dbRow[reagent+'ToneGaussianX0'+eventKey],
                         dbRow[reagent+'ToneGaussianSigma'+eventKey], dbRow[reagent+'ToneGaussianY0'+eventKey]]
            # print(stimEachTrial)
            pdots, pfit = extraplots.plot_tuning_curve(possibleStim, firingRates, fitParams)
            pfit[0].set_color(colorsRasterDark[reagent])
            allFits.append(pfit[0])
            if eventKey == 'BTR':
                plt.title(dbRow['BestTimeRange'])
            pdots[0].set_color(colorsRasterDark[reagent])
            extraplots.boxoff(axTuning)
            xTicks = np.array([2000, 4000, 8000,16000, 32000])
            axTuning.set_xticks(np.log2(xTicks))
            axTuning.set_xticklabels((xTicks/1000).astype(int))
            axTuning.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
            axTuning.set_ylabel('Firing rate (spk/s)', fontsize=fontSizeLabels)
            # axTuning.set_title(f'Cell #{cellInd}',loc='left')
        axTuning.legend(allFits, studyparams.REAGENTS_IMAGE, 
                        loc='upper left', handlelength=1)


    # -- Plot metrics summary --        
    gsMetrics = gsMain[0, 3].subgridspec(2, 2, hspace=0.4, wspace=0.5)
    #for indm, metric in enumerate(['ToneGaussianMax']): #enumerate(metrics):
    for indm, metric in enumerate(metrics):
        print(np.nonzero(selectedCells))
        nCells = np.sum(selectedCells)
        # thisMetricoff = celldb['off'+metric][selectedCells]
        thisMetricEachTile = [celldb[tile+metric][selectedCells] for tile in studyparams.REAGENTS_IMAGE]
        for indt,tileMetric in enumerate(thisMetricEachTile):
            tile = studyparams.REAGENTS_IMAGE[indt]
            thisMetricon = tileMetric
            thisMetricOtherTiles = thisMetricEachTile[0:indt] + thisMetricEachTile[indt+1:]
            thisMetricoff = np.array([np.mean(i) for i in zip(*thisMetricOtherTiles)])
            wstat, pVal = stats.wilcoxon(thisMetricoff, thisMetricon)
            medianoff = np.median(thisMetricoff)
            medianon = np.median(thisMetricon)
            print(f'[N={nCells}]  Median {tile},{metric}: off={medianoff:0.4f}, ' +
                f'on={medianon:0.4f}   p={pVal:0.4f}')
            print(f'\t on>off: {np.mean(thisMetricon>thisMetricoff):0.1%}'+
                f'\t on<off: {np.mean(thisMetricon<thisMetricoff):0.1%}')
            
            thisAx = plt.subplot(gsMetrics[indm+1])
            maxVal = max(thisMetricoff.max(), thisMetricon.max())
            if indm==99:
                plt.loglog(thisMetricoff, thisMetricon, 'o', mfc='none',label=tile,color = colorsTuning[tile])
            else:
                plt.plot(thisMetricoff, thisMetricon, 'o', mfc='none',label=tile,color = colorsTuning[tile])
            plt.plot([0, maxVal], [0, maxVal], 'k-', lw=0.5)
            plt.plot(medianoff, medianon, '+', ms=10, mew=2)
        plt.gca().set_aspect('equal', 'box')
        plt.xlim(metricLims[indm])
        plt.ylim(metricLims[indm])
        if indm==0:
            axTicksLog = np.log2(metricTicks[indm])
            axTickLabels = [f'{int(x/1000)}' for x in metricTicks[indm]]
            plt.xticks(axTicksLog, axTickLabels, fontsize=fontSizeTicks)
            plt.yticks(axTicksLog, axTickLabels, fontsize=fontSizeTicks)
        else:
            plt.xticks(metricTicks[indm], fontsize=fontSizeTicks)
            plt.yticks(metricTicks[indm], fontsize=fontSizeTicks)
        plt.xlabel(f'{metricsLabel[indm]} off ({metricsUnits[indm]})', fontsize=fontSizeLabels)
        plt.ylabel(f'{metricsLabel[indm]} on ({metricsUnits[indm]})', fontsize=fontSizeLabels)
        #plt.gca().tick_params(labelleft=False)
        if indm==99:
            thisAx.set_xscale('log')
            thisAx.set_yscale('log')
        plt.text(0.5, 0.9, f'p = {pVal:0.3f}',
                transform=thisAx.transAxes, ha='center', fontsize=fontSizeTicks)
        if indm==0:
            plt.title(f'N = {nCells} cells', fontsize=fontSizeLabels, fontweight='normal')
        # plt.tight_layout()
        #extraplots.boxoff(thisAx)

    if SAVE_FIGURE:
        cellstring = str(cellsToPlot[0])
        for cell in cellsToPlot[1:]:
            cellstring += f'-{cell:03d}'

        extraplots.save_figure(figFilename+cellstring, figFormat, 
                               figSize, outputDir,transparent=False)

    plt.show()

else:
    labelPosX = [0.002, 0.215, 0.43, 0.65, 0.825]   # Horiz position for panel labels
    labelPosY = [0.96, 0.47] 
    

    # -- Raster and PSTH parameters --
    timeRange = [-0.2, 0.4]
    binWidth = 0.010
    timeVec = np.arange(timeRange[0], timeRange[-1], binWidth)
    smoothWinSizePsth = 2 
    lwPsth = 2.5
    downsampleFactorPsth = 1

    cellIDs = np.arange(len(celldb))[selectedCells]
    celldb = celldb[selectedCells]

    # plotCells = cellsToPlot
    # if cellsToPlot:
    nCells = len(celldb)
    cellInds = [list(range(i,i+5)) for i in range(0,nCells,5)]
    
    
    sessionType = 'poniFreq'
    for pageNum, cellsToPlot in enumerate(cellInds):

        # -- Plot results --
        fig = plt.gcf()
        fig.clf()
        fig.set_facecolor('w')

        # -- Main gridspec --
        gsMain = gridspec.GridSpec(1, 5, width_ratios=[0.2, 0.2, 0.2, 0.2,0.2])
        gsMain.update(left=0.04, right=0.99, top=0.95, bottom=0.1, wspace=0.35, hspace=0.3)

        # -- Show panel labels --
        # for indp, plabel in enumerate(['A','B','C','D','E']):
        #     plt.figtext(labelPosX[indp], labelPosY[0], plabel, fontsize=fontSizePanel, fontweight='bold')



        for indcell,cellInd in enumerate(cellsToPlot):
            if cellInd < nCells:
                gsExample = gsMain[0, indcell].subgridspec(2, 1, hspace=0.35)
                gsRasters = gsExample[0].subgridspec(2, 1, hspace=0.1)
                axTuning = plt.subplot(gsExample[1])
                #cellInd, dbRow = celldatabase.find_cell(celldb, **cellsToPlot[indcell])
                dbRow = celldb.iloc[cellsToPlot[indcell]]
                thisGauss = sorted([reagent for reagent in studyparams.REAGENTS_IMAGE], 
                           key=lambda x: dbRow[x+'ToneGaussianA'+eventKey])
                reagentsToRaster = (thisGauss[-1],thisGauss[0])
                oneCell = ephyscore.Cell(dbRow)
                reagentsToPlot = studyparams.REAGENTS_IMAGE
                reagentLabels = studyparams.REAGENTS_IMAGE
                allFits = []
                ephysData, bdata = oneCell.load(sessionType)  
                tileEachTrial = np.array([f'C{i}R{j}' for i,j in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
                possibleTile = np.unique(tileEachTrial)
                nTrialsAll = len(tileEachTrial)
                eventOnsetTimesAll = ephysData['events']['stimOn'][:nTrialsAll]
                stimEachTrialAll = bdata['currentFreq']
                
                for indr, reagent in enumerate(reagentsToPlot):
                    trialInds = (tileEachTrial == reagent)
                    
                    spikeTimes = ephysData['spikeTimes']
                    eventOnsetTimes = eventOnsetTimesAll[trialInds]

                    stimEachTrial = stimEachTrialAll[trialInds]
                    nTrials = len(stimEachTrial)
                    
                    # -- onng this before selecting trials by laser/nonLaser --
                    possibleStim = np.unique(stimEachTrial)
                    nStim = len(possibleStim)
                    
                    stimDuration = bdata['stimDur'][-1]

                    # If the ephys data is 1 more than the bdata, delete the last ephys trial.
                    if len(stimEachTrial) == len(eventOnsetTimes)-1:
                        eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
                    assert len(stimEachTrial) == len(eventOnsetTimes), \
                        "Number of trials in behavior and ephys do not match for {oneCell}"

                    (spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial) = \
                        spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

                    trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

                    # -- Estimate evoked firing rate for each stim --
                    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                            indexLimitsEachTrial,
                                                                            timeRange)

                    if reagent in reagentsToRaster:
                        indrast = 0 if reagent == reagentsToRaster[0] else 1
                        # -- Plot Raster --
                        axRaster = plt.subplot(gsRasters[indrast])
                        possibleStimInKHz = possibleStim/1000
                        rasterLabels = ['']*nStim;
                        rasterLabels[0] = int(possibleStimInKHz[0])
                        rasterLabels[-1] = int(possibleStimInKHz[-1])
                        colorEachCond = [colorsRasterDark[reagent], colorsRasterLight[reagent]]*(nStim//2+1)
                        (pRasterS,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial, timeRange,
                                                                        trialsEachCond, labels=rasterLabels,
                                                                        colorEachCond=colorEachCond,
                                                                        rasterized=True)
                        
                        
                        plt.setp(pRasterS, ms=rasterMarkerSize)
                        if indrast==1:
                            plt.xlabel('Time (s)', fontsize=fontSizeLabels)
                        plt.ylabel('Freq (kHz)', fontsize=fontSizeLabels)
                        if eventKey == 'BTR':
                            plt.axvline(studyparams.TIME_RANGES[dbRow['BestTimeRange']][0],color='r',zorder=-10)
                            plt.axvline(studyparams.TIME_RANGES[dbRow['BestTimeRange']][1],color='r',zorder=-10)
                        #axRaster.set_yticklabels(['2']+['']*(nFreq-2)+['40'])
                        if indrast==0:
                            plot_stim(plt.ylim(), stimDuration)
                            plt.title(f'Cell #{cellIDs[cellInd]}',loc='left')
                            axRaster.set_xticklabels([])

                    # -- Plot tuning curve --
                    plt.sca(axTuning)
                    firingRates = dbRow[reagent+'ToneFiringRateEachFreq'+eventKey]
                    fitParams = [dbRow[reagent+'ToneGaussianA'+eventKey], dbRow[reagent+'ToneGaussianX0'+eventKey],
                                dbRow[reagent+'ToneGaussianSigma'+eventKey], dbRow[reagent+'ToneGaussianY0'+eventKey]]
                    # print(stimEachTrial)
                    pdots, pfit = extraplots.plot_tuning_curve(possibleStim, firingRates, fitParams)
                    pfit[0].set_color(colorsRasterDark[reagent])
                    allFits.append(pfit[0])
                    if eventKey == 'BTR':
                        plt.title(dbRow['BestTimeRange'])
                    pdots[0].set_color(colorsRasterDark[reagent])
                    extraplots.boxoff(axTuning)
                    xTicks = np.array([2000, 4000, 8000,16000, 32000])
                    axTuning.set_xticks(np.log2(xTicks))
                    axTuning.set_xticklabels((xTicks/1000).astype(int))
                    axTuning.set_xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
                    axTuning.set_ylabel('Firing rate (spk/s)', fontsize=fontSizeLabels)
                    # axTuning.set_title(f'Cell #{cellInd}',loc='left')
                axTuning.legend(allFits, studyparams.REAGENTS_IMAGE, 
                        loc='upper left', handlelength=1)
                
                # plt.tight_layout()

        if SAVE_FIGURE:
            cellstring = str(cellIDs[cellsToPlot[0]])
            for cell in cellsToPlot[1:]:
                if cell < nCells:
                    cellstring += f'-{cellIDs[cell]:03d}'

            outputDirNew = os.path.join(outputDir,'Just_Curves')
            if not os.path.exists(outputDirNew):
                os.mkdir(outputDirNew)
            extraplots.save_figure(figFilename+'_Just_Curves'+cellstring, 
                                   figFormat, figSize, outputDirNew,transparent=False)