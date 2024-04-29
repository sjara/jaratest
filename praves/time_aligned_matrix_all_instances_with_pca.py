"""
This script is used to create a time aligned matrix of the spike counts for each cell in the ensemble for all the instances.
"""


## load modules
import os 
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
# from mpl_toolkits.mplot3d import Axes3D

## define the path to the jaratoolbox directory
jara_src = '/Users/praveslamichhane/src/jaratoolbox' 
## append the path to the sys.path
sys.path.append(jara_src)

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

## global variables
TOTAL_CATEGORIES = 5

## create a database of cells
inforecFile = os.path.join(settings.INFOREC_PATH, 'feat015_inforec.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)

## load simultaneously recorded cells and create a CellEnsemble class

## select the cells that we want to analyze
sessionDate = "2024-03-20"
probeDepth = 2413

celldbSubset = celldb[(celldb.date == sessionDate) & (celldb.pdepth == probeDepth)]

## ceate a CellEnsemble class
ensemble = ephyscore.CellEnsemble(celldbSubset)

## load the ephys data and behavioral data for the cell ensemble. We only load the "naturalSound" session data
ephysData, bdata = ensemble.load("naturalSound")

## align all cells to the stimulus onset
## define parameters for the analysis
nTrials = len(bdata["soundID"])
eventOnsetTimes = ephysData["events"]["stimOn"][:nTrials]
timeRange = [-1.5, 5.5]
bin_size = 0.5

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

colors_categories = ["red", "blue", "green", "cyan", "purple"]
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
    binEdges = np.arange(timeRange[0], timeRange[1], bin_size)
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

## use PCA to reduce dimensionality of the time_aligned_matrix_all_instances
DIMS = 2
num_instances_each_category = len(possibleStims) // TOTAL_CATEGORIES

## reshape the time_aligned_matrix_all_instances to 2D array so that rows = cells and columns = bins from all instances stacked from 0 to 19
time_aligned_matrix_all_instances_transposed = time_aligned_matrix_all_instances.transpose(1, 0, 2)
final_shape = (time_aligned_matrix_all_instances_transposed.shape[0], -1)
time_aligned_matrix_all_instances_reshaped = time_aligned_matrix_all_instances_transposed.reshape(final_shape)

# ## test whether the reshaping is correct - we expect the first 13 columns to be the same as the first instance
# print(time_aligned_matrix_all_instances[0] == time_aligned_matrix_all_instances_reshaped[:, 0:13])
# print(time_aligned_matrix_all_instances[1] == time_aligned_matrix_all_instances_reshaped[:, 13:26])

## perform PCA on the reshaped 2D array 
pca = PCA(n_components=DIMS)
pca_matrix_all_instances = pca.fit_transform(time_aligned_matrix_all_instances_reshaped.T)

pca_matrix_all_instances = pca_matrix_all_instances.T

## now reshape the pca_matrix_all_instances to 3D array reflecting the original matrix 
num_trials = possibleStims.shape[0]
num_cells_pca = DIMS 
num_bins_per_trial = time_aligned_matrix_all_instances.shape[2] 

pca_matrix_all_instances_reshaped_original = pca_matrix_all_instances.reshape(num_cells_pca, num_trials, num_bins_per_trial)

## transpose the matrix so that the dimension information is preserved
pca_matrix_all_instances_original = pca_matrix_all_instances_reshaped_original.transpose(1, 0, 2)

# ## check if the reshaping is correct
# print(pca_matrix_all_instances_original[0] == pca_matrix_all_instances[:, 0:13])


## plot the PCA transformed matrix

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
plt.title('2D PCA of Spike Data')

## plot the PCA transformed matrix
for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
    curr_color = colors_categories[instance_id // num_instances_each_category]
    print(instance_values.shape)
    plot_pca = ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=curr_color)
    ## plot only the first point as a circle
    plt.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10)
    plt.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10)


ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
plt.show()
