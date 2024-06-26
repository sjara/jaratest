"""
This is a script that plots the raster for each cell for one recording session of natural sound. 
"""

## import modules
import os 
import sys
import numpy as np
import matplotlib.pyplot as plt
jara_src = '/Users/praveslamichhane/src/jaratoolbox' 
sys.path.append(jara_src)
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from jaratoolbox import ephyscore 
from jaratoolbox import spikesorting


## create database of cells
inforecFile = os.path.join(settings.INFOREC_PATH, 'feat016_inforec.py')

# clusteringObj = spikesorting.ClusterInforec(inforecFile)
# clusteringObj.process_all_experiments()

celldbSubset = celldatabase.generate_cell_database(inforecFile)

## load simultaneously recorded cells and create a CellEnsemble class

# ## select session and probe depth
# sessionDate = "2024-04-08"
# probeDepth = 3000
# celldbSubset = celldb[(celldb.date == sessionDate) & (celldb.pdepth == probeDepth)]

## create CellEnsemble class
ensemble = ephyscore.CellEnsemble(celldbSubset)
ephysData, bdata = ensemble.load('naturalSound') 

## align all cells to the stimulus onset 
nTrials = len(bdata['laserDuration'])
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials]
nCells, n_params = ensemble.celldb.shape 
timeRange = [-1, 5] ## in seconds 

## extract spiketimes, trial index, and index limits for each trial for each cell
spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

## create a boolean 2D array representing the sound category of each trial
current_sound_categories = bdata['soundID']
unique_sound_categories = np.unique(current_sound_categories)
trialsEachCategory = behavioranalysis.find_trials_each_type(current_sound_categories, unique_sound_categories)
nTrialsEachCategory = trialsEachCategory.sum(axis=0)

## create a sorting array to be used to plot the raster
condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCategory.T) 

## for now we just need the 1 trial category for each cell
ind_one_trial = np.where(condEachSortedTrial == 0)
trials_category0 = sortedTrials[ind_one_trial]

sortingInds = np.argsort(sortedTrials) ## this returns the indices that would sort the array

## plot the raster for each cell

someCells = np.arange(151, nCells)
fig = plt.figure(figsize=[10, 6])
for count, indcell in enumerate(someCells):
    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
    plt.subplot(10, 5, count+1)
    plt.plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Sorted Trials')

plt.title('Raster plot for each cell')
plt.tight_layout()
plt.show()