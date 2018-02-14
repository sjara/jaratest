import os
import pandas as pd
import numpy as np
from scipy import stats

from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'inactivation_cells.h5')
dbase = pd.read_hdf(dbPath, 'database',index_col=0)

figName = 'figure_SOM_inactivation'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)

# -- Example SOM cell showing difference in suppression -- #
cell = {'subject' : 'band025',
        'date' : '2017-04-20',
        'depth' : 1400,
        'tetrode' : 6,
        'cluster' : 6}

# -- find the cell we want based on dictionary --
cellInd, dbRow = celldatabase.find_cell(dbase, **cell)
cell = ephyscore.Cell(dbRow)

# --- loads spike and event data for bandwidth ephys sessions ---
bandEphysData, bandBData = cell.load('laserBandwidth') #make them ints in the first place
bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
if len(bandEventOnsetTimes)==0: #some cells recorded before sound detector installed
    bandEventOnsetTimes = bandEphysData['events']['stimOn'] + 0.0093 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
bandSpikeTimestamps = bandEphysData['spikeTimes']

# -- Define sorting parameters for behaviour --
bandEachTrial = bandBData['currentBand']
numBands = np.unique(bandEachTrial)

secondSort = bandBData['laserTrial']
numSec = np.unique(secondSort)
    
bandTimeRange = [-0.5, 1.5]
bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                       numBands, 
                                                                       secondSort, 
                                                                       numSec)
bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                    bandSpikeTimestamps, 
                                                                                                    bandEventOnsetTimes,
                                                                                                    bandTimeRange)



# --- produce input for laser bandwidth tuning curve (onset and sustained responses) ---
soundDuration = bandBData['stimDur'][-1]
print('Sound duration from behavior data: {0} sec'.format(soundDuration))
onsetTimeRange = [0.0, 0.05]
onsetDuration = onsetTimeRange[1]-onsetTimeRange[0]
sustainedTimeRange = [0.2, soundDuration]
sustainedDuration = sustainedTimeRange[1]-sustainedTimeRange[0]

onsetSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, onsetTimeRange)
sustainedSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, sustainedTimeRange)

onsetResponseArray = np.zeros((len(numBands),len(numSec)))
onsetSTD = np.zeros_like(onsetResponseArray)
onsetpVals = np.zeros(len(numBands))

sustainedResponseArray = np.zeros_like(onsetResponseArray)
sustainedSTD = np.zeros_like(onsetResponseArray)
sustainedpVals = np.zeros(len(numBands))

# Average firing rate for laser and non-laser trials and stdev
for band in range(len(numBands)):
    trialsThisBand = bandTrialsEachCond[:,band,:]
    noLaserOnsetCounts = None
    noLaserSustainedCounts = None
    for thisSecVal in range(len(numSec)):
        trialsThisLaser = trialsThisBand[:,thisSecVal]
        if onsetSpikeCountMat.shape[0] != len(trialsThisLaser): #if number of events greater than behaviour trials because last trial didn't get saved
            onsetSpikeCountMat = onsetSpikeCountMat[:-1,:]
            sustainedSpikeCountMat = sustainedSpikeCountMat[:-1,:]
        if any(trialsThisLaser):
            thisLaserOnsetCounts = onsetSpikeCountMat[trialsThisLaser].flatten()
            thisLaserSustainedCounts = sustainedSpikeCountMat[trialsThisLaser].flatten()
            
            onsetResponseArray[band,thisSecVal] = np.mean(thisLaserOnsetCounts)/onsetDuration
            sustainedResponseArray[band,thisSecVal] = np.mean(thisLaserSustainedCounts)/sustainedDuration
            
            onsetSTD[band,thisSecVal] = np.std(thisLaserOnsetCounts)/onsetDuration
            sustainedSTD[band,thisSecVal] = np.std(thisLaserSustainedCounts)/sustainedDuration # Error is standard error of the mean
            
            if noLaserOnsetCounts is None:
                noLaserOnsetCounts = thisLaserOnsetCounts
                noLaserSustainedCounts = thisLaserSustainedCounts
            
    onsetpVals[band] = stats.ranksums(noLaserOnsetCounts, thisLaserOnsetCounts)[1]
    sustainedpVals[band] = stats.ranksums(noLaserSustainedCounts, thisLaserSustainedCounts)[1]

# Baseline firing rate and stdev
baselineRange = [-1.1, -0.1]
baselineDuration = baselineRange[1]-baselineRange[0]
baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                 bandIndexLimitsEachTrial, baselineRange)
baselineMean = baselineSpikeCountMat.mean()/baselineDuration
baselineSTD = np.std(baselineSpikeCountMat)/baselineDuration

outputFile = 'example_SOM_inactivation_{}_{}_{}um_T{}_c{}.npz'.format(dbRow['subject'], dbRow['date'],
                                                                         int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])
        

outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         onsetResponseArray=onsetResponseArray, onsetSTD=onsetSTD,
         sustainedResponseArray=sustainedResponseArray, sustainedSTD=sustainedSTD,
         possibleBands=numBands, possibleLasers=numSec,
         spikeTimesFromEventOnset=bandSpikeTimesFromEventOnset,
         indexLimitsEachTrial=bandIndexLimitsEachTrial, timeRange=bandTimeRange,
         baselineRange=baselineRange, baselineMean=baselineMean, baselineSTD=baselineSTD,
         trialsEachCond=bandTrialsEachCond,
         onsetTimeRange=onsetTimeRange, sustainedTimeRange=sustainedTimeRange,
         onsetpVals=onsetpVals, sustainedpVals=sustainedpVals)
print outputFile + " saved"