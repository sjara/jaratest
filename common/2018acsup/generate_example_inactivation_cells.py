''' 
Generates inputs to plot a raster and tuning curves (for onset and sustained responses) for individual cells from PV or SOM inactivated animals.
Inputs for each cell are saved as npz's.

TODO: add more options for inactivated cells of each type
'''

import os
import sys
import numpy as np
from scipy import stats

from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import database_bandwidth_tuning_fit_funcs as fitfuncs
import figparams

#dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'inactivation_cells.h5')
dbPath = os.path.join(settings.DATABASE_PATH,'inactivation_cells.h5')
dbase = celldatabase.load_hdf(dbPath)

figName = 'figure_inhibitory_cell_inactivation'

#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

# -- Example SOM cell showing difference in suppression -- #
cellList = [{'subject' : 'band055',
             'date' : '2018-03-20',
             'depth' : 1200,
             'tetrode' : 6,
             'cluster' : 4},
            
            {'subject' : 'band062',
             'date' : '2018-05-24',
             'depth' : 1300,
             'tetrode' : 2,
             'cluster' : 2}]

cellTypes = ['SOM', 'PV']

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
    onsetSEM = np.zeros_like(onsetResponseArray)
    onsetpVals = np.zeros(len(numBands))
    
    sustainedResponseArray = np.zeros_like(onsetResponseArray)
    sustainedSEM = np.zeros_like(onsetResponseArray)
    sustainedpVals = np.zeros(len(numBands))
    
    # Average firing rate for laser and non-laser trials and SEMev
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
                
                onsetSEM[band,thisSecVal] = stats.sem(thisLaserOnsetCounts)/onsetDuration
                sustainedSEM[band,thisSecVal] = stats.sem(thisLaserSustainedCounts)/sustainedDuration # Error is standard error of the mean
                
                if noLaserOnsetCounts is None:
                    noLaserOnsetCounts = thisLaserOnsetCounts
                    noLaserSustainedCounts = thisLaserSustainedCounts
                
        onsetpVals[band] = stats.ranksums(noLaserOnsetCounts, thisLaserOnsetCounts)[1]
        sustainedpVals[band] = stats.ranksums(noLaserSustainedCounts, thisLaserSustainedCounts)[1]
    
    # Baseline firing rates
    noLaserBaseline = dbRow['baselineFRnoLaser']
    laserBaseline = dbRow['baselineFRLaser']
    noLaserSEM = dbRow['baselineFRnoLaserSEM']
    laserSEM = dbRow['baselineFRLaserSEM']
    
    # replace pure tone with baselines
    onsetResponseArray[0,0] = noLaserBaseline
    sustainedResponseArray[0,0] = noLaserBaseline
    onsetResponseArray[0,1] = laserBaseline
    sustainedResponseArray[0,1] = laserBaseline
    
    onsetSEM[0,0] = noLaserSEM
    sustainedSEM[0,0] = noLaserSEM
    onsetSEM[0,1] = laserSEM
    sustainedSEM[0,1] = laserSEM
    
    numBands[-1] = 6 #white noise is 6 octaves
    
    # --- produce difference of gaussian curve for sustained response of each cell ---
    testBands = np.linspace(numBands[0],numBands[-1],50)
    testRespsNoLaser = fitfuncs.diff_gauss_form(testBands, dbRow['mnoLaser'], dbRow['R0noLaser'], dbRow['sigmaDnoLaser'], dbRow['sigmaSnoLaser'], dbRow['RDnoLaser'], dbRow['RSnoLaser'])
    testRespsLaser = fitfuncs.diff_gauss_form(testBands, dbRow['mlaser'], dbRow['R0laser'], dbRow['sigmaDlaser'], dbRow['sigmaSlaser'], dbRow['RDlaser'], dbRow['RSlaser'])
    
    
    
    outputFile = 'example_{}_inactivation_{}_{}_{}um_T{}_c{}.npz'.format(cellTypes[indCell], dbRow['subject'], dbRow['date'],
                                                                             int(dbRow['depth']),dbRow['tetrode'],dbRow['cluster'])
            
    
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath,
             onsetResponseArray=onsetResponseArray, onsetSEM=onsetSEM,
             sustainedResponseArray=sustainedResponseArray, sustainedSEM=sustainedSEM,
             possibleBands=numBands, possibleLasers=numSec,
             spikeTimesFromEventOnset=bandSpikeTimesFromEventOnset,
             indexLimitsEachTrial=bandIndexLimitsEachTrial, timeRange=bandTimeRange,
             trialsEachCond=bandTrialsEachCond,
             onsetTimeRange=onsetTimeRange, sustainedTimeRange=sustainedTimeRange,
             onsetpVals=onsetpVals, sustainedpVals=sustainedpVals,
             fitBands = testBands, fitResponseNoLaser = testRespsNoLaser, firResponseLaser = testRespsLaser)
    print outputFile + " saved"