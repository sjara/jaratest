"""
This file contains the pipeline for the neural trajectory analysis. The pipeline consists of the following steps:
1. time aligned matrix 2D
2. time aligned matrix 3D -> Incorporates the time aligned matrix 2D
3. pca -> Incorporates the time aligned matrix 3D
4. plot pca -> Incorporates the pca
5. get category instance dictionary
6. get distance between categories -> Incorporates the get category instance dictionary
7. get distance between instances of the same category -> Incorporates the get category instance dictionary

"""


## load modules
import os 
import sys
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import neuralTrajectory as nt

## define the path to the jaratoolbox directory since we cannot install
JARATOOL_PATH = '/Users/praveslamichhane/src/jaratoolbox' 
## append the path to the sys.path
sys.path.append(JARATOOL_PATH)

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

## this is firstly for just one session. If multiple sessions, loop through the inforecFiles 
## global variables
TOTAL_CATEGORIES = 5 ## total number of categories of natural sounds used in the experiment

## create a database of cells
# inforecFiles = []

## create cell database for all experiments from inforecFiles
inforecFile = os.path.join(settings.INFOREC_PATH, 'feat015_inforec.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)

## ceate a CellEnsemble class
ensemble = ephyscore.CellEnsemble(celldb)

## load the ephys data and behavioral data for the cell ensemble. We only load the "naturalSound" session data
ephysData, bdata = ensemble.load("naturalSound")

## align all cells to the stimulus onset
## define parameters and variables for the analysis
nTrials = len(bdata["soundID"])
eventOnsetTimes = ephysData["events"]["stimOn"][:nTrials]
timeRange = [-1.5, 5.5]
binSize = 0.5

## get spiketimes, trial index for each spike and index limits for each trial for each cell in the ensemble
## NOTE: eventlocked_spiketimes method returns a list of arrays for each cell in the ensemble
spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

## create a boolean 2D array representing the sound instance of each trial
currentStim = bdata["soundID"]
possibleStims = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStims)
nTrialsEachCond = trialsEachCond.sum(axis=0)

## sort trials by stimulus type and extract the type into each stimulus type
condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)

## create a 3D-array of time_aligned_matrix for all instances
## the dimensions of the array are: (num_instances, num_cells, num_bins)

time_aligned_matrix_all_instances = []
for uniq_stim, instance_id in enumerate(possibleStims):
    
    current_instance = np.where(condEachSortedTrial == instance_id)
    trials_current_instance = sortedTrials[current_instance]

    ## extract spikes for each cell for each trial in instance 0
    spikes_curr_instance = []
    # print(len(indexLimitsEachTrialAll))
    for cell_num in range(len(indexLimitsEachTrialAll)):
        total_spikes = []
        spikes_curr_cell = spikeTimesFromEventOnsetAll[cell_num]
        indices_curr_cell = indexLimitsEachTrialAll[cell_num]
        indices_to_select = indices_curr_cell[:, trials_current_instance]
        for index in indices_to_select.T: ## this is where the problem is 
            total_spikes.append(spikes_curr_cell[index[0]:index[1] + 1])
        spikes_curr_instance.append(total_spikes)


    ## bin spikes for each cell
    spikes_binned_all_cells = []
    binEdges = np.arange(timeRange[0], timeRange[1], binSize)
    for cell_num in range(len(spikes_curr_instance)):
        curr_cell = spikes_curr_instance[cell_num]
        spikes_binned_curr_cell = []
        for trial in curr_cell:
            spike_counts, _ = np.histogram(trial, binEdges)
            spikes_binned_curr_cell.append(spike_counts)
            # print(len(spike_counts))
        spikes_binned_all_cells.append(spikes_binned_curr_cell)


    ## total spike counts for each cell in instance 0 for each bin
    total_spikes_all_cells = []
    for cell_num in range(len(spikes_binned_all_cells)):
        curr_cell = spikes_binned_all_cells[cell_num]
        total_spikes_curr_cell = np.sum(curr_cell, axis=0)
        total_spikes_all_cells.append(total_spikes_curr_cell)

    ## create a 2D numpy array for the sum of spikes for each cell in each bin
    total_spikes_all_cells = np.array(total_spikes_all_cells)

    ## append the total_spikes_all_cells to the time_aligned_matrix_all_instances
    time_aligned_matrix_all_instances.append(total_spikes_all_cells)

## get the dimensions of the time_aligned_matrix_all_instances
time_aligned_matrix_all_instances = np.array(time_aligned_matrix_all_instances)
print("Shape of time aligned matrix: ", time_aligned_matrix_all_instances.shape)
