''' 
Generates inputs to plot median firing rates during bandwidth trials for PV and SOM cells
'''

import os
import pandas as pd
import numpy as np

from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbase = pd.read_hdf(dbPath, 'dataframe')

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

medianResponses = []
SEMedians = []
medianBaselineRates = []

# -- compute average onset and sustained responses for all PV and SOM cells, then find median response
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
        
        bandTimeRange = [-0.3, 1.5]
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
            responseArrays[ind] = np.zeros((len(cellsThisType),len(numBands)))
        
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
        
        
        responseArrays[ind][indCell,:] = responseArray
        baselineSpikeRates[ind][indCell] = baselineMean
    medianResponses.append(np.median(responseArrays[ind], axis=0))
    medianBaselineRates.append(np.median(baselineSpikeRates[ind]))
    
# -- save photoidentified suppression scores --
outputFile = 'photoidentified_cells_firing_rates.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVonsetMedianResponse = medianResponses[0],
         PVsustainedMedianResponse = medianResponses[1],
         SOMonsetMedianResponse = medianResponses[2],
         SOMsustainedMedianResponse = medianResponses[3],
         possibleBands = numBands,
         PVonsetMedianBaseline = medianBaselineRates[0],
         PVsustainedMedianBaseline = medianBaselineRates[1],
         SOMonsetMedianBaseline = medianBaselineRates[2],
         SOMsustainedMedianBaseline = medianBaselineRates[3],
         PVonsetProp = PVonsetProp,
         SOMonsetProp = SOMonsetProp)
print outputFile + " saved"