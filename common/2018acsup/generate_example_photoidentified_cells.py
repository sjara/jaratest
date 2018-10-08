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

import database_bandwidth_tuning_fit_funcs as fitfuncs
import figparams

dbPath = os.path.join(settings.DATABASE_PATH, 'photoidentification_cells.h5')
dbase = celldatabase.load_hdf(dbPath)

figName = 'figure_characterisation_of_responses_by_cell_type'

#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', allACFigName)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

# -- Example cells -- #
cellList = [{'subject' : 'band016',
            'date' : '2016-12-11',
            'depth' : 950,
            'tetrode' : 6,
            'cluster' : 6}, #example AC cell
            
            {'subject' : 'band029',
            'date' : '2017-05-25',
            'depth' : 1240,
            'tetrode' : 2,
            'cluster' : 2}, #another AC cell
            
            {'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1140,
            'tetrode' : 1,
            'cluster' : 3}, #another AC cell
            
            {'subject' : 'band044',
            'date' : '2018-01-16',
            'depth' : 975,
            'tetrode' : 7,
            'cluster' : 4}, #another AC cell
            
            {'subject' : 'band060',
            'date' : '2018-04-02',
            'depth' : 1275,
            'tetrode' : 4,
            'cluster' : 2}, #another AC cell
            
            {'subject' : 'band026',
            'date' : '2017-04-27',
            'depth' : 1350,
            'tetrode' : 4,
            'cluster' : 2}, #PV cell
            
            {'subject' : 'band026',
            'date' : '2017-04-26',
            'depth' : 1470,
            'tetrode' : 4,
            'cluster' : 5}, #PV cell
            
            {'subject' : 'band032',
            'date' : '2017-07-21',
            'depth' : 1200,
            'tetrode' : 6,
            'cluster' : 2}, #PV cell
            
            {'subject' : 'band033',
            'date' : '2017-07-27',
            'depth' : 1700,
            'tetrode' : 4,
            'cluster' : 5}, #PV cell
            
            {'subject' : 'band015',
            'date' : '2016-11-12',
            'depth' : 1000,
            'tetrode' : 8,
            'cluster' : 4}, #SOM cell
            
            {'subject' : 'band029',
            'date' : '2017-05-22',
            'depth' : 1320,
            'tetrode' : 4,
            'cluster' : 2}, #SOM cell
            
            {'subject' : 'band031',
            'date' : '2017-06-29',
            'depth' : 1280,
            'tetrode' : 1,
            'cluster' : 4}, #SOM cell
            
            {'subject' : 'band060',
            'date' : '2018-04-04',
            'depth' : 1225,
            'tetrode' : 3,
            'cluster' : 4}] #SOM cell

cellTypes = ['Exc', 'Exc', 'Exc', 'Exc', 'Exc', 'PV', 'PV', 'PV', 'PV', 'SOM', 'SOM', 'SOM', 'SOM']

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
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    
    # --- loads spike and event data for bandwidth ephys sessions ---
    bandEphysData, bandBData = cell.load_by_index(int(dbRow['bestBandSession'])) #make them ints in the first place
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
        
    rasterTimeRange = [-0.5, 1.5]
    baselineRange = [-1.0, -0.2]
    fullTimeRange = [baselineRange[0], rasterTimeRange[1]]
    
    bandTrialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           secondSort, 
                                                                           numSec)
    bandSpikeTimesFromEventOnset, trialIndexForEachSpike, bandIndexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        bandSpikeTimestamps, 
                                                                                                        bandEventOnsetTimes,
                                                                                                        fullTimeRange)
    
    
    
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
    onsetSEM = np.zeros_like(onsetResponseArray)
    sustainedResponseArray = np.zeros_like(onsetResponseArray)
    sustainedSEM = np.zeros_like(onsetResponseArray)
    
    # Average firing rate for high amplitude trials and SEM
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
            
            onsetSEM[band] = stats.sem(thisBandOnsetCounts)/onsetDuration
            sustainedSEM[band] = stats.sem(thisBandSustainedCounts)/sustainedDuration # Error is standard error of the mean

    # Baseline firing rate and SEM
    baselineDuration = baselineRange[1]-baselineRange[0]
    baselineSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(bandSpikeTimesFromEventOnset,
                                                                     bandIndexLimitsEachTrial, baselineRange)
    baselineMean = baselineSpikeCountMat.mean()/baselineDuration
    baselineSEM = stats.sem(baselineSpikeCountMat)/baselineDuration
    
    # Replace 0 bandwidth condition with baseline
    onsetResponseArray[0] = baselineMean
    sustainedResponseArray[0] = baselineMean
    
    onsetSEM[0] = baselineSEM
    sustainedSEM[0] = baselineSEM
    
    numBands[-1] = 6 #white noise is 6 octaves
    
    
    # --- produce difference of gaussian curve for sustained response of each cell ---
    testBands = np.linspace(numBands[0],numBands[-1],500)
    testResps = fitfuncs.diff_gauss_form(testBands, dbRow['m'], dbRow['R0'], dbRow['sigmaD'], dbRow['sigmaS'], dbRow['RD'], dbRow['RS'])
    
    # --- get SI for each cell ---
    sustainedSI = dbRow['fitSustainedSuppressionIndex']
    
    ### Save bandwidth data ###    
    outputFile = 'example_{}_bandwidth_tuning_{}_{}_{}um_T{}_c{}.npz'.format(cellTypes[indCell],dbRow['subject'], dbRow['date'],
                                                                         int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])

    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath,
             onsetResponseArray=onsetResponseArray, onsetSEM=onsetSEM,
             sustainedResponseArray=sustainedResponseArray, sustainedSEM=sustainedSEM,
             possibleBands=numBands,
             spikeTimesFromEventOnset=bandSpikeTimesFromEventOnset,
             indexLimitsEachTrial=bandIndexLimitsEachTrial,
             trialsEachCond=trialsHighAmp,
             onsetTimeRange=onsetTimeRange, sustainedTimeRange=sustainedTimeRange, rasterTimeRange=rasterTimeRange,
             fitBands = testBands, fitResponse = testResps, SI = sustainedSI)
    print outputFile + " saved"

