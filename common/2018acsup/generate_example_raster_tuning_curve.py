''' 
Generates inputs to plot a raster and tuning curves (for onset and sustained responses) for individual cells.
Inputs for each cell are saved as npz's

Can select which cells from the list to generate by index.
Not specifying which cells to generate will generate all of them.

To run:
run generate_example_raster_tuning_curve.py 0 2 (generate the first and third cell)
'''

import os
import sys
import pandas as pd
import numpy as np
from scipy import stats

from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbase = pd.read_hdf(dbPath, 'database',index_col=0)

allACFigName = 'figure_all_AC_suppression'
photoFigName = 'figure_PV_SOM_suppression'

allACDataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', allACFigName)
photoDataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', photoFigName)

# -- Example cells -- #
cellList = [{'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1280,
            'tetrode' : 1,
            'cluster' : 3}, #example AC cell
            
            {'subject' : 'band044',
            'date' : '2018-01-16',
            'depth' : 975,
            'tetrode' : 7,
            'cluster' : 4}, #another AC cell
            
            {'subject' : 'band026',
            'date' : '2017-04-27',
            'depth' : 1350,
            'tetrode' : 4,
            'cluster' : 2}, #PV cell
            
            {'subject' : 'band026',
            'date' : '2017-04-27',
            'depth' : 1410,
            'tetrode' : 4,
            'cluster' : 6}, #PV cell
            
            {'subject' : 'band028',
            'date' : '2017-05-21',
            'depth' : 1450,
            'tetrode' : 2,
            'cluster' : 4}, #SOM cell
            
            {'subject' : 'band028',
            'date' : '2017-05-21',
            'depth' : 1625,
            'tetrode' : 6,
            'cluster' : 6}, #SOM cell
            
            {'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1280,
            'tetrode' : 1,
            'cluster' : 4}] #SOM cell

cellTypes = ['AC', 'AC', 'PV', 'PV', 'SOM', 'SOM', 'SOM']

# -- select which cells to generate --
args = sys.argv[1:]
if len(args):
    cellsToGenerate = [int(x) for x in args]
else:
    cellsToGenerate = range(len(cellList))
print cellsToGenerate


for indCell in cellsToGenerate:
    # -- find the cell we want based on dictionary --
    cellInd, dbRow = celldatabase.find_cell(dbase, **cellList[indCell])
    cell = ephyscore.Cell(dbRow)
    
    # --- loads spike and event data for bandwidth ephys sessions ---
    bandEphysData, bandBData = cell.load_by_index(int(dbRow['bestBandIndexHigh'])) #make them ints in the first place
    bandEventOnsetTimes = bandEphysData['events']['soundDetectorOn']
    if len(bandEventOnsetTimes)==0: #some cells recorded before sound detector installed
        bandEventOnsetTimes = bandEphysData['events']['stimOn'] + 0.0093 #correction for bandwidth trials, determined by comparing sound detector onset to stim event onset
    bandEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(bandEventOnsetTimes, minEventOnsetDiff=0.2)
    bandSpikeTimestamps = bandEphysData['spikeTimes']
    
    # -- Define sorting parameters for behaviour --
    bandEachTrial = bandBData['currentBand']
    numBands = np.unique(bandEachTrial)
    
    secondSort = bandBData['currentAmp']
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
    
    
    
    # --- produce input for bandwidth tuning curve (onset and sustained responses) ---
    soundDuration = bandBData['stimDur'][-1]
    print('Sound duration from behavior data: {0} sec'.format(soundDuration))
    onsetTimeRange = [0.0, 0.05]
    onsetDuration = onsetTimeRange[1]-onsetTimeRange[0]
    sustainedTimeRange = [0.2, soundDuration]
    sustainedDuration = sustainedTimeRange[1]-sustainedTimeRange[0]
    
    onsetSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, onsetTimeRange)
    sustainedSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset, bandIndexLimitsEachTrial, sustainedTimeRange)
    
    onsetResponseArray = np.zeros(len(numBands))
    onsetSTD = np.zeros_like(onsetResponseArray)
    sustainedResponseArray = np.zeros_like(onsetResponseArray)
    sustainedSTD = np.zeros_like(onsetResponseArray)
    
    # Average firing rate for high amplitude trials and stdev
    trialsHighAmp = bandTrialsEachCond[:,:,-1] #only using high amplitude trials (-1 in list of amps)
    for band in range(len(numBands)):
        trialsThisBand = trialsHighAmp[:,band]
        if onsetSpikeCountMat.shape[0] != len(trialsThisBand): #if number of events greater than behaviour trials because last trial didn't get saved
            onsetSpikeCountMat = onsetSpikeCountMat[:-1,:]
            sustainedSpikeCountMat = sustainedSpikeCountMat[:-1,:]
        if any(trialsThisBand):
            thisBandOnsetCounts = onsetSpikeCountMat[trialsThisBand].flatten()
            thisBandSustainedCounts = sustainedSpikeCountMat[trialsThisBand].flatten()
            
            onsetResponseArray[band] = np.mean(thisBandOnsetCounts)/onsetDuration
            sustainedResponseArray[band] = np.mean(thisBandSustainedCounts)/sustainedDuration
            
            onsetSTD[band] = np.std(thisBandOnsetCounts)/onsetDuration
            sustainedSTD[band] = np.std(thisBandSustainedCounts)/sustainedDuration # Error is standard error of the mean

    # Baseline firing rate and stdev
    baselineRange = [-1.1, -0.1]
    baselineDuration = baselineRange[1]-baselineRange[0]
    baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                     bandIndexLimitsEachTrial, baselineRange)
    baselineMean = baselineSpikeCountMat.mean()/baselineDuration
    baselineSTD = np.std(baselineSpikeCountMat)/baselineDuration
    
    ### Save bandwidth data ###    
    outputFile = 'example_{}_bandwidth_tuning_{}_{}_{}um_T{}_c{}.npz'.format(cellTypes[indCell],dbRow['subject'], dbRow['date'],
                                                                         int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])
        
    dirDict = {'AC':allACDataDir,
               'PV':photoDataDir,
               'SOM':photoDataDir}

    outputFullPath = os.path.join(dirDict[cellTypes[indCell]],outputFile)
    np.savez(outputFullPath,
             onsetResponseArray=onsetResponseArray, onsetSTD=onsetSTD,
             sustainedResponseArray=sustainedResponseArray, sustainedSTD=sustainedSTD,
             possibleBands=numBands,
             spikeTimesFromEventOnset=bandSpikeTimesFromEventOnset,
             indexLimitsEachTrial=bandIndexLimitsEachTrial, timeRange=bandTimeRange,
             baselineRange=baselineRange, baselineMean=baselineMean, baselineSTD=baselineSTD,
             trialsEachCond=trialsHighAmp,
             onsetTimeRange=onsetTimeRange, sustainedTimeRange=sustainedTimeRange)
    print outputFile + " saved"

