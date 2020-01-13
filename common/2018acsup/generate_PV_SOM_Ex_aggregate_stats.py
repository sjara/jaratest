''' 
Generates inputs to plot mean/median responses for all recorded PV/SOM/putative pyramidal cells

Inputs generated:
* suppression indices for all cells
* preferred bandwidth for all cells
* median firing rates for all cells
* PSTHs for high bandwidth responses
* onset and sustained responses to high bandwidth stimuli
'''

import os
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams
import studyparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'figure_characterisation_of_responses_by_cell_type'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected and have sustained sound response
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

sustPVCells = bestCells.query(studyparams.PV_CELLS)
sustSOMCells = bestCells.query(studyparams.SOM_CELLS)
sustExCells = bestCells.query(studyparams.EXC_CELLS)

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustPVCells['sustainedSuppressionIndex']
SOMsustainedSuppression = sustSOMCells['sustainedSuppressionIndex']
ExsustainedSuppression = sustExCells['sustainedSuppressionIndex']

fitPVsustainedSuppression = sustPVCells['fitSustainedSuppressionIndex']
fitSOMsustainedSuppression = sustSOMCells['fitSustainedSuppressionIndex']
fitExsustainedSuppression = sustExCells['fitSustainedSuppressionIndex']

fitPVsustainedSuppressionNoZero = sustPVCells['fitSustainedSuppressionIndexNoZeroHighAmp']
fitSOMsustainedSuppressionNoZero = sustSOMCells['fitSustainedSuppressionIndexNoZeroHighAmp']
fitExsustainedSuppressionNoZero = sustExCells['fitSustainedSuppressionIndexNoZeroHighAmp']

# -- get preferred bandwidths for all cells responsive during sustained portion of response --
PVsustainedPrefBW = sustPVCells['sustainedPrefBandwidth']
SOMsustainedPrefBW = sustSOMCells['sustainedPrefBandwidth']
ExsustainedPrefBW = sustExCells['sustainedPrefBandwidth']

fitPVsustainedPrefBW = sustPVCells['fitSustainedPrefBandwidth']
fitSOMsustainedPrefBW = sustSOMCells['fitSustainedPrefBandwidth']
fitExsustainedPrefBW = sustExCells['fitSustainedPrefBandwidth']

fitPVsustainedPrefBWNoZero = sustPVCells['fitSustainedPrefBandwidthNoZeroHighAmp']
fitSOMsustainedPrefBWNoZero = sustSOMCells['fitSustainedPrefBandwidthNoZeroHighAmp']
fitExsustainedPrefBWNoZero = sustExCells['fitSustainedPrefBandwidthNoZeroHighAmp']

# -- get proportions of response that happens at onset and sustained --
PVonsetProp = sustPVCells['proportionSpikesOnset']
SOMonsetProp = sustSOMCells['proportionSpikesOnset']
ExonsetProp = sustExCells['proportionSpikesOnset']

PVsustProp = sustPVCells['proportionSpikesSustained']
SOMsustProp = sustSOMCells['proportionSpikesSustained']
ExsustProp = sustExCells['proportionSpikesSustained']

onsetTimeRange = [0.0, 0.05]
sustainedTimeRange = [0.2, 1.0]


PVBaseSpikeRates = np.zeros(len(sustPVCells))
SOMBaseSpikeRates = np.zeros(len(sustSOMCells))
ExBaseSpikeRates = np.zeros(len(sustExCells))

PVHighBandOnsetSpikeRates = np.zeros(len(sustPVCells))
SOMHighBandOnsetSpikeRates = np.zeros(len(sustSOMCells))
ExHighBandOnsetSpikeRates = np.zeros(len(sustExCells))

PVHighBandSustainedSpikeRates = np.zeros(len(sustPVCells))
SOMHighBandSustainedSpikeRates = np.zeros(len(sustSOMCells))
ExHighBandSustainedSpikeRates = np.zeros(len(sustExCells))

cells = [sustPVCells, sustSOMCells, sustExCells]
highBandOnsetSpikeRates = [PVHighBandOnsetSpikeRates, SOMHighBandOnsetSpikeRates, ExHighBandOnsetSpikeRates]
highBandSustainedSpikeRates = [PVHighBandSustainedSpikeRates, SOMHighBandSustainedSpikeRates, ExHighBandSustainedSpikeRates]
baselineSpikeRates = [PVBaseSpikeRates, SOMBaseSpikeRates, ExBaseSpikeRates]

highBands = [5,6] #change in FR and average PSTHs for 4 octaves and white noise (high bandwidths)

# -- compute change in firing rate for high bandwidths for all PV and SOM, and Exc. cells
for ind, cellsThisType in enumerate(cells):
    for indCell in range(len(cellsThisType)):
        cell = cellsThisType.iloc[indCell]
        cellObj = ephyscore.Cell(cell, useModifiedClusters=True)
        bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandSession']))
        bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
        if len(bandEventOnsetTimes)==0: #some cells recorded before sound detector installed
            bandEventOnsetTimes = bandEphysData['events']['stimOn'] + 0.0093 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
        bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        baselineRange = [-1.0, -0.2]
        fullTimeRange = [baselineRange[0], sustainedTimeRange[1]]
        
        onsetResponseDuration = onsetTimeRange[1]-onsetTimeRange[0]
        sustainedResponseTimeDuration = sustainedTimeRange[1]-sustainedTimeRange[0]
        
        bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        fullTimeRange)
        
        onsetSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, onsetTimeRange)
        sustainedSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, sustainedTimeRange)
    
        bandEachTrial = bandBData['currentBand']
        ampEachTrial = bandBData['currentAmp']
        numBands = np.unique(bandEachTrial)
        numAmps = np.unique(ampEachTrial)
        
        bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           ampEachTrial, 
                                                                           numAmps)
        
        trialsHighAmp = bandTrialsEachCond[:,:,-1] #only using high amplitude trials (-1 in list of amps)     
        # find high bandwidth trials
        trialsHighBands = None
        for band in highBands:
            if trialsHighBands is None:
                trialsHighBands = trialsHighAmp[:,band]
            else:
                trialsHighBands = trialsHighBands | trialsHighAmp[:,band]
        
        # Average firing rate for high amplitude trials
        if onsetSpikeCountMat.shape[0] == len(trialsHighBands)+1:
            onsetSpikeCountMat = onsetSpikeCountMat[:-1,:]
        highBandOnsetSpikeCounts = onsetSpikeCountMat[trialsHighBands]
        highBandOnsetMean = np.mean(highBandOnsetSpikeCounts)/(onsetTimeRange[1]-onsetTimeRange[0])
        
        highBandOnsetSpikeRates[ind][indCell] = highBandOnsetMean
        
        if sustainedSpikeCountMat.shape[0] == len(trialsHighBands)+1:
            sustainedSpikeCountMat = sustainedSpikeCountMat[:-1,:]
        highBandSustainedSpikeCounts = sustainedSpikeCountMat[trialsHighBands]
        highBandSustainedMean = np.mean(highBandSustainedSpikeCounts)/(sustainedTimeRange[1]-sustainedTimeRange[0])
        
        highBandSustainedSpikeRates[ind][indCell] = highBandSustainedMean
                
        # Baseline firing rate and SEM
        baselineDuration = baselineRange[1]-baselineRange[0]
        baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                         bandIndexLimitsEachTrial, baselineRange)
        baselineMean = np.mean(baselineSpikeCountMat)/baselineDuration
        
        baselineSpikeRates[ind][indCell] = baselineMean


# -- compute average normalised PSTH of PV, SOM, Ex cell responses --
averagePSTHs = []

for ind, cellsThisType in enumerate(cells):
    thisCellTypeAllPSTHs = None
    for indCell in range(len(cellsThisType)):
        cell = cellsThisType.iloc[indCell]
        cellObj = ephyscore.Cell(cell, useModifiedClusters=True)
        bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandSession']))
        bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
        if len(bandEventOnsetTimes)==0: #some cells recorded before sound detector installed
            bandEventOnsetTimes = bandEphysData['events']['stimOn'] + 0.0093 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
        bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        bandTimeRange = [-0.5, 1.5]
        binsize = 50 #in milliseconds
        
        bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        [bandTimeRange[0]-binsize, bandTimeRange[1]])
        
        binEdges = np.around(np.arange(bandTimeRange[0]-(binsize/1000.0), bandTimeRange[1]+2*(binsize/1000.0), (binsize/1000.0)), decimals=2)
        if thisCellTypeAllPSTHs is None:
            thisCellTypeAllPSTHs = np.zeros((len(cellsThisType),len(binEdges)-1))
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, binEdges)
        
        trialsEachBand = behavioranalysis.find_trials_each_type(bandBData['currentBand'], np.unique(bandBData['currentBand']))
        
        # find high bandwidth trials
        trialsHighBands = None
        for band in highBands:
            if trialsHighBands is None:
                trialsHighBands = trialsEachBand[:,band]
            else:
                trialsHighBands = trialsHighBands | trialsEachBand[:,band]
                
        if spikeCountMat.shape[0] == len(trialsHighBands)+1:
            spikeCountMat = spikeCountMat[:-1,:]
        highBandSpikeCounts = spikeCountMat[trialsHighBands]
        
        thisPSTH = np.mean(highBandSpikeCounts,axis=0)
        #thisPSTH = thisPSTH/max(thisPSTH)
        #thisPSTH = thisPSTH/thisPSTH[np.where(binEdges==0)[0][0]] #normalise so onset is 1
        thisPSTH = (thisPSTH-np.mean(thisPSTH[1:np.where(binEdges==-0.05)[0][0]]))/(thisPSTH[np.where(binEdges==0)[0][0]]-np.mean(thisPSTH[1:np.where(binEdges==-0.05)[0][0]])) #normalise so onset is 1 and baseline is 0
        thisCellTypeAllPSTHs[indCell,:] = thisPSTH
    
    thisCellTypeAllPSTHs = thisCellTypeAllPSTHs[~np.isnan(thisCellTypeAllPSTHs).any(axis=1)] #do not include any cells that for whatever reason had a sound onset firing rate of 0, resulting in NaN during normalisation
    thisCellTypePSTH = np.median(thisCellTypeAllPSTHs, axis=0)
    
    #smooth PSTH
    smoothWinSize = 1
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    thisCellTypePSTH = np.convolve(thisCellTypePSTH,winShape,mode='same')
    
    averagePSTHs.append(thisCellTypePSTH)
    
numBands[-1] = 6
    
        
        
# -- save photoidentified suppression scores --
outputFile = 'all_photoidentified_cells_stats.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVsustainedResponses = highBandSustainedSpikeRates[0],
         SOMsustainedResponses = highBandSustainedSpikeRates[1],
         ExcSustainedResponses = highBandSustainedSpikeRates[2],
         PVonsetResponses = highBandOnsetSpikeRates[0],
         SOMonsetResponses = highBandOnsetSpikeRates[1],
         ExcOnsetResponses = highBandOnsetSpikeRates[2],
         possibleBands = numBands,
         PVbaselines = baselineSpikeRates[0],
         SOMbaselines = baselineSpikeRates[1],
         ExcBaselines = baselineSpikeRates[2],
         PVonsetProp = PVonsetProp,
         SOMonsetProp = SOMonsetProp,
         ExcOnsetProp = ExonsetProp,
         PVsustProp = PVsustProp,
         SOMsustProp = SOMsustProp,
         ExcSustProp = ExsustProp,
         PVaveragePSTH = averagePSTHs[0],
         SOMaveragePSTH = averagePSTHs[1],
         ExcAveragePSTH = averagePSTHs[2],
         PSTHbinStartTimes = binEdges[:-1],
         rawPVsustainedSuppressionInd = PVsustainedSuppression,
         rawSOMsustainedSuppressionInd = SOMsustainedSuppression,
         rawExcSustainedSuppressionInd = ExsustainedSuppression,
         fitPVsustainedSuppressionInd = fitPVsustainedSuppression,
         fitSOMsustainedSuppressionInd = fitSOMsustainedSuppression,
         fitExcSustainedSuppressionInd = fitExsustainedSuppression,
         fitPVsustainedSuppressionNoZero = fitPVsustainedSuppressionNoZero,
         fitSOMsustainedSuppressionNoZero = fitSOMsustainedSuppressionNoZero,
         fitExcsustainedSuppressionNoZero = fitExsustainedSuppressionNoZero,
         rawPVsustainedPrefBW = PVsustainedPrefBW,
         rawSOMsustainedPrefBW = SOMsustainedPrefBW,
         rawExcSustainedPrefBW = ExsustainedPrefBW,
         fitPVsustainedPrefBW = fitPVsustainedPrefBW,
         fitSOMsustainedPrefBW = fitSOMsustainedPrefBW,
         fitExcSustainedPrefBW = fitExsustainedPrefBW,
         fitPVsustainedPrefBWNoZero = fitPVsustainedPrefBWNoZero,
         fitSOMsustainedPrefBWNoZero = fitSOMsustainedPrefBWNoZero,
         fitExcsustainedPrefBWNoZero = fitExsustainedPrefBWNoZero)
print outputFile + " saved"