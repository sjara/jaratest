''' 
Generates inputs to plot median firing rates during bandwidth trials for PV and SOM cells
'''

import os
import pandas as pd
import numpy as np
import scipy.stats

from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams

def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
    """
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbase = pd.read_hdf(dbPath, 'database', index_col=0)

figName = 'figure_PV_SOM_firing_rates'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034','band037','band038','band044','band045']

EXCLUDED_DATES = ['2017-07-27','2017-08-02'] #dates where there were some problems with recording

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = dbase.query('tuningFitR2High>@R2CUTOFF and octavesFromBestHigh<@OCTAVESCUTOFF')
bestCells = bestCells.loc[~bestCells['date'].isin(EXCLUDED_DATES)]
laserResponsiveCells = bestCells.query('laserResponsepVal<0.001 and laserResponseStdFromBase>2.0')
PVCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(PV_CHR2_MICE)]
SOMCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(SOM_CHR2_MICE)]

# -- get cells responsive during sustained portion of response --
sustainedPVCells = PVCells.loc[PVCells['bandSustainedSoundResponsepVal']<SOUND_RESPONSE_PVAL]
sustainedSOMCells = SOMCells.loc[SOMCells['bandSustainedSoundResponsepVal']<SOUND_RESPONSE_PVAL]

# -- get cells responsive during onset portion of response --
onsetPVCells = PVCells.loc[PVCells['bandOnsetSoundResponsepVal']<SOUND_RESPONSE_PVAL]
onsetSOMCells = SOMCells.loc[SOMCells['bandOnsetSoundResponsepVal']<SOUND_RESPONSE_PVAL]

# -- get cells responsive during any part of response --
responsivePVCells = PVCells.loc[PVCells['bandSoundResponsepVal']<SOUND_RESPONSE_PVAL]
responsiveSOMCells = SOMCells.loc[SOMCells['bandSoundResponsepVal']<SOUND_RESPONSE_PVAL]

# -- get proportions of response that happens at onset --
PVonsetProp = onsetPVCells['bandOnsetSpikePropHigh']
SOMonsetProp = onsetSOMCells['bandOnsetSpikePropHigh']

onsetTimeRange = [0.0, 0.05]
sustainedTimeRange = [0.2, 1.0]

PVonsetResponseArrays = None
PVonsetBaseSpikeRates = np.zeros(len(onsetPVCells))

PVsustainedResponseArrays = None
PVsustainedBaseSpikeRates = np.zeros(len(sustainedPVCells))

SOMonsetResponseArrays = None
SOMonsetBaseSpikeRates = np.zeros(len(onsetSOMCells))

SOMsustainedResponseArrays = None
SOMsustainedBaseSpikeRates = np.zeros(len(sustainedSOMCells))

cells = [onsetPVCells, sustainedPVCells, onsetSOMCells, sustainedSOMCells]
responseArrays = [PVonsetResponseArrays, PVsustainedResponseArrays, SOMonsetResponseArrays, SOMsustainedResponseArrays]
baselineSpikeRates = [PVonsetBaseSpikeRates, PVsustainedBaseSpikeRates, SOMonsetBaseSpikeRates, SOMsustainedBaseSpikeRates]
timeRanges = [onsetTimeRange, sustainedTimeRange, onsetTimeRange, sustainedTimeRange]

# -- compute average onset and sustained responses for all PV and SOM cells
for ind, cellsThisType in enumerate(cells):
    for indCell in range(len(cellsThisType)):
        cell = cellsThisType.iloc[indCell]
        cellObj = ephyscore.Cell(cell)
        bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandIndexHigh']))
        bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
        if len(bandEventOnsetTimes)==0: #some cells recorded before sound detector installed
            bandEventOnsetTimes = bandEphysData['events']['stimOn'] + 0.0093 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
        bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
        bandSpikeTimestamps = bandEphysData['spikeTimes']
        
        bandTimeRange = [-0.5, 1.5]
        responseTimeDuration = timeRanges[ind][1] - timeRanges[ind][0]
        
        bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        bandTimeRange)
        
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, timeRanges[ind])
    
        bandEachTrial = bandBData['currentBand']
        ampEachTrial = bandBData['currentAmp']
        numBands = np.unique(bandEachTrial)
        numAmps = np.unique(ampEachTrial)
        
        bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           ampEachTrial, 
                                                                           numAmps)
        
        if responseArrays[ind] is None:
            responseArrays[ind] = np.zeros((len(numBands),len(cellsThisType)))
        
        responseArray = np.zeros(len(numBands))
        
        # Average firing rate for high amplitude trials
        trialsHighAmp = bandTrialsEachCond[:,:,-1] #only using high amplitude trials (-1 in list of amps)
        for band in range(len(numBands)):
            trialsThisBand = trialsHighAmp[:,band]
            if spikeCountMat.shape[0] != len(trialsThisBand): #if number of events greater than behaviour trials because last trial didn't get saved
                spikeCountMat = spikeCountMat[:-1,:]
            if any(trialsThisBand):
                thisBandOnsetCounts = spikeCountMat[trialsThisBand].flatten()
                responseArray[band] = np.mean(thisBandOnsetCounts)/responseTimeDuration
                
        # Baseline firing rate and SEM
        baselineRange = [-1.1, -0.1]
        baselineDuration = baselineRange[1]-baselineRange[0]
        baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                         bandIndexLimitsEachTrial, baselineRange)
        baselineMean = np.mean(baselineSpikeCountMat)/baselineDuration
        
        responseArrays[ind][:,indCell] = responseArray
        baselineSpikeRates[ind][indCell] = baselineMean

# -- compute p values for differenced in PV and SOM firing per bandwidth --
onsetpVals = np.zeros(len(numBands))
sustainedpVals = np.zeros_like(onsetpVals)

for band in range(len(numBands)):
    thisBandPVonsetResponses = responseArrays[0][band,:]
    thisBandPVsustainedResponses = responseArrays[1][band,:]
    thisBandSOMonsetResponses = responseArrays[2][band,:]
    thisBandSOMsustainedResponses = responseArrays[3][band,:]
    
    onsetpVals[band] = scipy.stats.ranksums(thisBandPVonsetResponses,thisBandSOMonsetResponses)[1]
    sustainedpVals[band] = scipy.stats.ranksums(thisBandPVsustainedResponses,thisBandSOMsustainedResponses)[1]

# -- compute average normalised PSTH of PV and SOM cell responses --
cells = [responsivePVCells, responsiveSOMCells]
averagePSTHs = []
MADs = []

for ind, cellsThisType in enumerate(cells):
    thisCellTypeAllPSTHs = None
    for indCell in range(len(cellsThisType)):
        cell = cellsThisType.iloc[indCell]
        cellObj = ephyscore.Cell(cell)
        bandEphysData, bandBData = cellObj.load_by_index(int(cell['bestBandIndexHigh']))
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
        thisPSTH = np.mean(spikeCountMat,axis=0)
        #thisPSTH = thisPSTH/max(thisPSTH)
        thisPSTH = thisPSTH/thisPSTH[np.where(binEdges==0)[0][0]] #normalise so onset is 1
        thisCellTypeAllPSTHs[indCell,:] = thisPSTH
    smoothWinSize = 1
    winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
    winShape = winShape/np.sum(winShape)
    thisCellTypePSTH = np.median(thisCellTypeAllPSTHs, axis=0)
    smoothPSTH = np.convolve(thisCellTypePSTH,winShape,mode='same')
    averagePSTHs.append(smoothPSTH)
    
    MAD = np.zeros(len(smoothPSTH))
    for thisBin in range(len(smoothPSTH)):
        MAD[thisBin] = mad(thisCellTypeAllPSTHs[:,thisBin])
    MADs.append(MAD)
        
    
        
        
# -- save photoidentified suppression scores --
outputFile = 'photoidentified_cells_firing_rates.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVonsetResponses = responseArrays[0],
         PVsustainedResponses = responseArrays[1],
         SOMonsetResponses = responseArrays[2],
         SOMsustainedResponses = responseArrays[3],
         possibleBands = numBands,
         PVonsetBaselines = baselineSpikeRates[0],
         PVsustainedBaselines = baselineSpikeRates[1],
         SOMonsetBaselines = baselineSpikeRates[2],
         SOMsustainedBaselines = baselineSpikeRates[3],
         onsetpVals = onsetpVals,
         sustainedpVals = sustainedpVals,
         PVonsetProp = PVonsetProp,
         SOMonsetProp = SOMonsetProp,
         PVaveragePSTH = averagePSTHs[0],
         SOMaveragePSTH = averagePSTHs[1],
         PVPSTHMAD = MADs[0],
         SOMPSTHMAD = MADs[1],
         PSTHbinStartTimes = binEdges[:-1])
print outputFile + " saved"