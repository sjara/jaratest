''' 
Generates inputs to plot mean/median responses for all recorded PV/SOM/putative pyramidal cells

Inputs generated:
* suppression indices for all cells
* preferred bandwidth for all cells
* median firing rates for all cells
* PSTHs for high bandwidth responses
* "onsetivity"
'''

import os
import pandas as pd
import numpy as np
import scipy.stats

from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams
import subjects_info

#dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbFilename = os.path.join(settings.DATABASE_PATH,'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'figure_characterisation_of_responses_by_cell_type'

#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_CHR2_MICE = subjects_info.PV_CHR2_MICE
SOM_CHR2_MICE = subjects_info.SOM_CHR2_MICE

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = db.query("isiViolations<0.02 or modifiedISI<0.02")
bestCells = bestCells.query('spikeShapeQuality>2.5 and tuningFitR2>@R2CUTOFF and octavesFromPrefFreq<@OCTAVESCUTOFF')

# -- find cells responsive to laser pulse or train --
laserResponsiveCells = bestCells.query("laserPVal<0.001 and laserUStat>0")
#laserResponsiveCells = bestCells.query("laserTrainPVal<0.001 and laserTrainUStat>0")
#laserResponsiveCells = laserResponsiveCells1.combine_first(laserResponsiveCells2)
# combine_first changes ints to floats for some reason!!!
#laserResponsiveCells['tetrode'] = laserResponsiveCells['tetrode'].astype(int)
PVCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(PV_CHR2_MICE)]
SOMCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(SOM_CHR2_MICE)]

# -- find cells unresponsive to laser (putative pyramidal) --
ExCells = bestCells.query("laserPVal>0.05 and laserTrainPVal>0.05")
ExCells = ExCells.loc[ExCells['subject'].isin(SOM_CHR2_MICE)]

# -- PV, SOM, Ex cells sound responsive during sustained portion of bw trials --
sustPVCells = PVCells.loc[PVCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]
sustSOMCells = SOMCells.loc[SOMCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]
sustExCells = ExCells.loc[ExCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustPVCells['sustainedSuppressionIndex']
SOMsustainedSuppression = sustSOMCells['sustainedSuppressionIndex']
ExsustainedSuppression = sustExCells['sustainedSuppressionIndex']

fitPVsustainedSuppression = sustPVCells['fitSustainedSuppressionIndex']
fitSOMsustainedSuppression = sustSOMCells['fitSustainedSuppressionIndex']
fitExsustainedSuppression = sustExCells['fitSustainedSuppressionIndex']

# -- get preferred bandwidths for all cells responsive during sustained portion of response --
PVsustainedPrefBW = sustPVCells['sustainedPrefBandwidth']
SOMsustainedPrefBW = sustSOMCells['sustainedPrefBandwidth']
ExsustainedPrefBW = sustExCells['sustainedPrefBandwidth']

fitPVsustainedPrefBW = sustPVCells['fitSustainedPrefBandwidth']
fitSOMsustainedPrefBW = sustSOMCells['fitSustainedPrefBandwidth']
fitExsustainedPrefBW = sustExCells['fitSustainedPrefBandwidth']

# -- get proportions of response that happens at onset --
PVonsetProp = sustPVCells['proportionSpikesOnset']
SOMonsetProp = sustSOMCells['proportionSpikesOnset']
ExonsetProp = sustExCells['proportionSpikesOnset']
PVSOMonsetProppVal = scipy.stats.ranksums(PVonsetProp,SOMonsetProp)[1]
PVExonsetProppVal = scipy.stats.ranksums(PVonsetProp,ExonsetProp)[1]
ExSOMonsetProppVal = scipy.stats.ranksums(ExonsetProp,SOMonsetProp)[1]

#onsetTimeRange = [0.0, 0.05]
sustainedTimeRange = [0.2, 1.0]


PVBaseSpikeRates = np.zeros(len(sustPVCells))
SOMBaseSpikeRates = np.zeros(len(sustSOMCells))
ExBaseSpikeRates = np.zeros(len(sustExCells))

PVHighBandSpikeRates = np.zeros(len(sustPVCells))
SOMHighBandSpikeRates = np.zeros(len(sustSOMCells))
ExHighBandSpikeRates = np.zeros(len(sustExCells))

cells = [sustPVCells, sustSOMCells, sustExCells]
highBandSpikeRates = [PVHighBandSpikeRates, SOMHighBandSpikeRates, ExHighBandSpikeRates]
baselineSpikeRates = [PVBaseSpikeRates, SOMBaseSpikeRates, ExBaseSpikeRates]

highBands = [5,6] #change in FR and average PSTHs for 4 octaves and white noise (high bandwidths)

# -- compute change in firing rate for high bandwidths for all PV and SOM cells
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
        responseTimeDuration = sustainedTimeRange[1]-sustainedTimeRange[0]
        
        bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        fullTimeRange)
        
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, sustainedTimeRange)
    
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
        highBandSpikeCounts = spikeCountMat[trialsHighBands]
        highBandMean = np.mean(highBandSpikeCounts)/(sustainedTimeRange[1]-sustainedTimeRange[0])
        
        highBandSpikeRates[ind][indCell] = highBandMean
                
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
        highBandSpikeCounts = spikeCountMat[trialsHighBands]
        
        thisPSTH = np.mean(highBandSpikeCounts,axis=0)
        #thisPSTH = thisPSTH/max(thisPSTH)
        #thisPSTH = thisPSTH/thisPSTH[np.where(binEdges==0)[0][0]] #normalise so onset is 1
        thisPSTH = (thisPSTH-np.mean(thisPSTH[1:np.where(binEdges==-0.05)[0][0]]))/(thisPSTH[np.where(binEdges==0)[0][0]]-np.mean(thisPSTH[1:np.where(binEdges==-0.05)[0][0]])) #normalise so onset is 1 and baseline is 0
        print thisPSTH
        thisCellTypeAllPSTHs[indCell,:] = thisPSTH
    
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
         PVsustainedResponses = highBandSpikeRates[0],
         SOMsustainedResponses = highBandSpikeRates[1],
         ExcSustainedResponses = highBandSpikeRates[2],
         possibleBands = numBands,
         PVbaselines = baselineSpikeRates[0],
         SOMbaselines = baselineSpikeRates[1],
         ExcBaselines = baselineSpikeRates[2],
         PVonsetProp = PVonsetProp,
         SOMonsetProp = SOMonsetProp,
         ExcOnsetProp = ExonsetProp,
         PVSOMonsetProppVal = PVSOMonsetProppVal,
         PVExconsetProppVal = PVExonsetProppVal,
         ExcSOMonsetProppVal = ExSOMonsetProppVal,
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
         rawPVsustainedPrefBW = PVsustainedPrefBW,
         rawSOMsustainedPrefBW = SOMsustainedPrefBW,
         rawExcSustainedPrefBW = ExsustainedPrefBW,
         fitPVsustainedPrefBW = fitPVsustainedPrefBW,
         fitSOMsustainedPrefBW = fitSOMsustainedPrefBW,
         fitExcSustainedPrefBW = fitExsustainedPrefBW)
print outputFile + " saved"