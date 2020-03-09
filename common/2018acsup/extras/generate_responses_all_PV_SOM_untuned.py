import os
import numpy as np
import copy

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

db = celldatabase.load_hdf('/mnt/jarahubdata/figuresdata/2018acsup/photoidentification_cells.h5')
bestCells = db.query('isiViolations<0.02 or modifiedISI<0.02')
bestCells = bestCells.query('spikeShapeQuality>2.5 and sustainedSoundResponsePVal<0.05')

LASER_RESPONSE_PVAL = 0.001 # want to be EXTRA sure not to include false positives

EXC_LASER_RESPONSE_PVAL = 0.5 # for selecting putative excitatory cells NOT responsive to laser
EXC_SPIKE_WIDTH = 0.0004

PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034','band037','band038','band044','band045','band054','band059','band060']

PV_CELLS = bestCells.query('laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,PV_CHR2_MICE))
SOM_CELLS = bestCells.query('laserPVal<{} and laserUStat>0 and subject=={}'.format(LASER_RESPONSE_PVAL,SOM_CHR2_MICE))
EXC_CELLS = bestCells.query('(laserPVal>{} or laserUStat<0) and spikeWidth>{} and subject=={}'.format(EXC_LASER_RESPONSE_PVAL,EXC_SPIKE_WIDTH,SOM_CHR2_MICE))

freqTunedPV = PV_CELLS.query('tuningFitR2>0.1 and octavesFromPrefFreq<0.3')
freqTunedOffCentrePV = PV_CELLS.query('tuningFitR2>0.1 and octavesFromPrefFreq>0.3')
notFreqTunedPV = PV_CELLS.query('tuningFitR2<0.1')

freqTunedSOM = SOM_CELLS.query('tuningFitR2>0.1 and octavesFromPrefFreq<0.3')
freqTunedOffCentreSOM = SOM_CELLS.query('tuningFitR2>0.1 and octavesFromPrefFreq>0.3')
notFreqTunedSOM = SOM_CELLS.query('tuningFitR2<0.1')

freqTunedExc = EXC_CELLS.query('tuningFitR2>0.1 and octavesFromPrefFreq<0.3')
freqTunedOffCentreExc = EXC_CELLS.query('tuningFitR2>0.1 and octavesFromPrefFreq>0.3')
notFreqTunedExc = EXC_CELLS.query('tuningFitR2<0.1')

cells = [freqTunedPV, freqTunedOffCentrePV, notFreqTunedPV, 
         freqTunedSOM, freqTunedOffCentreSOM, notFreqTunedSOM, 
         freqTunedExc, freqTunedOffCentreExc, notFreqTunedExc]

baselineSpikeRates = [np.zeros(len(freqTunedPV)), np.zeros(len(freqTunedOffCentrePV)), np.zeros(len(notFreqTunedPV)),
                      np.zeros(len(freqTunedSOM)), np.zeros(len(freqTunedOffCentreSOM)), np.zeros(len(notFreqTunedSOM)),
                      np.zeros(len(freqTunedExc)), np.zeros(len(freqTunedOffCentreExc)), np.zeros(len(notFreqTunedExc))]

highBandSustainedSpikeRates = copy.deepcopy(baselineSpikeRates)
highBandOnsetSpikeRates = copy.deepcopy(baselineSpikeRates)

highBands = [5,6] # change in FR and average PSTHs for 4 octaves and white noise (high bandwidths)

onsetTimeRange = [0.0, 0.05]
sustainedTimeRange = [0.2, 1.0]

# -- compute change in firing rate for high bandwidths for all PV and SOM, and Exc. cells
for ind, cellsThisType in enumerate(cells):
    for indCell in range(len(cellsThisType)):
        cell = cellsThisType.iloc[indCell]
        cellObj = ephyscore.Cell(cell, useModifiedClusters=True)
        bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandSession']))
        bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
        if len(bandEventOnsetTimes)==0: # some cells recorded before sound detector installed
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
        
        trialsHighAmp = bandTrialsEachCond[:,:,-1] # only using high amplitude trials (-1 in list of amps)     
        # find high bandwidth trials
        trialsHighBands = None
        for band in highBands:
            if trialsHighBands is None:
                trialsHighBands = trialsHighAmp[:,band]
            else:
                trialsHighBands = trialsHighBands | trialsHighAmp[:,band]
        
        # Average firing rate for high amplitude trials
        highBandOnsetSpikeCounts = onsetSpikeCountMat[trialsHighBands]
        highBandOnsetMean = np.mean(highBandOnsetSpikeCounts)/(onsetTimeRange[1]-onsetTimeRange[0])
         
        highBandOnsetSpikeRates[ind][indCell] = highBandOnsetMean
        
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
        if len(bandEventOnsetTimes)==0: # some cells recorded before sound detector installed
            bandEventOnsetTimes = bandEphysData['events']['stimOn'] + 0.0093 # correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
        bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        bandTimeRange = [-0.5, 1.5]
        binsize = 50 # in milliseconds
        
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
        thisCellTypeAllPSTHs[indCell,:] = thisPSTH
    
    thisCellTypeAllPSTHs = thisCellTypeAllPSTHs[~np.isnan(thisCellTypeAllPSTHs).any(axis=1)] #do not include any cells that for whatever reason had a sound onset firing rate of 0, resulting in NaN during normalisation
    thisCellTypePSTH = np.median(thisCellTypeAllPSTHs, axis=0)
    
    # smooth PSTH
    smoothWinSize = 1
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    thisCellTypePSTH = np.convolve(thisCellTypePSTH,winShape,mode='same')
    
    averagePSTHs.append(thisCellTypePSTH)
    
outputFile = 'all_photoidentified_cells_untuned_stats.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFile,
         PVTunedSustainedResponses = highBandSustainedSpikeRates[0],
         PVTunedOffCentreSustainedResponses = highBandSustainedSpikeRates[1],
         PVUntunedSustainedResponses = highBandSustainedSpikeRates[2],
         SOMTunedSustainedResponses = highBandSustainedSpikeRates[3],
         SOMTunedOffCentreSustainedResponses = highBandSustainedSpikeRates[4],
         SOMUntunedSustainedResponses = highBandSustainedSpikeRates[5],
         ExcTunedSustainedResponses = highBandSustainedSpikeRates[6],
         ExcTunedOffCentreSustainedResponses = highBandSustainedSpikeRates[7],
         ExcUntunedSustainedResponses = highBandSustainedSpikeRates[8],
         
         PVTunedOnsetResponses = highBandOnsetSpikeRates[0],
         PVTunedOffCentreOnsetResponses = highBandOnsetSpikeRates[1],
         PVUntunedOnsetResponses = highBandOnsetSpikeRates[2],
         SOMTunedOnsetResponses = highBandOnsetSpikeRates[3],
         SOMTunedOffCentreOnsetResponses = highBandOnsetSpikeRates[4],
         SOMUntunedOnsetResponses = highBandOnsetSpikeRates[5],
         ExcTunedOnsetResponses = highBandOnsetSpikeRates[6],
         ExcTunedOffCentreOnsetResponses = highBandOnsetSpikeRates[7],
         ExcUntunedOnsetResponses = highBandOnsetSpikeRates[8],
         
         PVtunedBaselines = baselineSpikeRates[0],
         PVtunedOffCentreBaselines = baselineSpikeRates[1],
         PVuntunedBaselines = baselineSpikeRates[2],
         SOMtunedBaselines = baselineSpikeRates[3],
         SOMtunedOffCentreBaselines = baselineSpikeRates[4],
         SOMuntunedBaselines = baselineSpikeRates[5],
         ExcTunedBaselines = baselineSpikeRates[6],
         ExcTunedOffCentreBaselines = baselineSpikeRates[7],
         ExcUntunedBaselines = baselineSpikeRates[8],
         
         PVtunedAveragePSTH = averagePSTHs[0],
         PVtunedOffCentreAveragePSTH = averagePSTHs[1],
         PVuntunedAveragePSTH = averagePSTHs[2],
         SOMtunedAveragePSTH = averagePSTHs[3],
         SOMtunedOffCentreAveragePSTH = averagePSTHs[4],
         SOMuntunedAveragePSTH = averagePSTHs[5],
         ExcTunedAveragePSTH = averagePSTHs[6],
         ExcTunedOffCentreAveragePSTH = averagePSTHs[7],
         ExcUntunedAveragePSTH = averagePSTHs[8],
         
         PSTHbinStartTimes = binEdges[:-1])
print outputFile + " saved"