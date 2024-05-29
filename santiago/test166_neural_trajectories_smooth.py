"""
Based on jaratest/praves/neural_trajectories/time_aligned_matrix_all_instances_with_pca.py

See also test165...

In this script we use overlapping bins to estimate smooth neural trajectories.
"""


## load modules
import os 
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

## define the path to the jaratoolbox directory
#jara_src = '/Users/praveslamichhane/src/jaratoolbox' 
## append the path to the sys.path
#sys.path.append(jara_src)

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

## global variables
TOTAL_CATEGORIES = 5

## create a database of cells
SESSIONID = 1
if SESSIONID == 0:
    subject = 'feat015'
    sessionDate = "2024-03-20"
    probeDepth = 2413
if SESSIONID == 1:
    subject = 'feat016'
    sessionDate = "2024-04-08"
    probeDepth = 3000
if SESSIONID == 2:
    subject = 'feat017'
    sessionDate = "2024-03-26"
    probeDepth = 3000
    
inforecFile = os.path.join(settings.INFOREC_PATH, f'{subject}_inforec.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)

## load simultaneously recorded cells and create a CellEnsemble class
celldbSubset = celldb[(celldb.date == sessionDate) & (celldb.pdepth == probeDepth)]

## ceate a CellEnsemble class
ensemble = ephyscore.CellEnsemble(celldbSubset)

## load the ephys data and behavioral data for the cell ensemble. We only load the "naturalSound" session data
ephysData, bdata = ensemble.load("naturalSound")

## align all cells to the stimulus onset
## define parameters for the analysis
nTrials = len(bdata["soundID"])
eventOnsetTimes = ephysData["events"]["stimOn"][:nTrials]
#timeRange = [-1.5, 5.5]
timeRange = [-1.5, 5.5]
bin_size = 0.05

## get the stimulus start time for the time range and bin size
def get_stim_start_time(time_range=timeRange, bin_size=bin_size, stim_start=0):
    #print("Number of seconds each bin: ", bin_size)
    start_time = time_range[0]
    end_time = start_time + bin_size
    curr_bin = 0
    while True:
        if stim_start < time_range[0] or stim_start > time_range[1]:
           raise ValueError("Stimulus start time is outside the time range")  
        else:
            if start_time <= stim_start and stim_start <= end_time:
                return curr_bin
            start_time = end_time
            end_time = start_time + bin_size
            curr_bin += 1 


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

#colors_categories = ["red", "blue", "green", "cyan", "purple"]
colors_categories = ["red", "cyan", "green", "blue", "purple"]
#possibleStims = np.array([8, 9, 10, 11])
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


# -- Smooth out the spike counts --
if 1:
    print('Smoothing out the spike counts...')
    smoothWinSize = 10  # 10
    winShape = np.concatenate((np.zeros(smoothWinSize), np.ones(smoothWinSize)))  # Square (causal)
    #winShape = np.ones(smoothWinSize)   # non-causal
    winShape = winShape/np.sum(winShape)
    nInstances, nCells, nBins = time_aligned_matrix_all_instances.shape
    for indi in range(nInstances):
        for indc in range(nCells):
            time_aligned_matrix_all_instances[indi, indc, :] = \
                np.convolve(time_aligned_matrix_all_instances[indi, indc, :], winShape, mode='same')


## use PCA to reduce dimensionality of the time_aligned_matrix_all_instances
DIMS = 3
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

## create a category instance dictionary to store instances for each category
category_instance_dict = {} ## key: category_id, value: [instance_ids]
categories = list((np.arange(0, TOTAL_CATEGORIES, 1)))
print(categories)
num_instances_each_category = len(possibleStims) // TOTAL_CATEGORIES
for instance_id, instance_value in enumerate(time_aligned_matrix_all_instances):
    instance_category = categories[instance_id // num_instances_each_category]
    if instance_category in category_instance_dict:
        category_instance_dict[instance_category].append(instance_id)
    else:
        category_instance_dict[instance_category] = [instance_id]

print(category_instance_dict)


## PCA plots
## plot the PCA transformed matrix

#fig, axs = plt.subplots(2, 3, figsize=(15, 10), sharex=True, sharey=True)
#axs = axs.flatten()
plt.clf()
fig = plt.gcf()

ax = fig.add_subplot(111, projection='3d')

if 1:
    # -- Plot subset 3D --
    #instances_to_plot = 4*num_instances_each_category + np.arange(4)
    instances_to_plot = 3*num_instances_each_category + np.arange(8)
    #instances_to_plot = 3*num_instances_each_category + np.array([0]) # Plot only one
    for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
        if instance_id in instances_to_plot:
            curr_color = colors_categories[instance_id // num_instances_each_category]
            ax = plt.gca()
            plot_pca = ax.plot(instance_values[0, :],
                               instance_values[1, :],
                               instance_values[2, :], '.-', color=curr_color)
            if 1:
                ax.plot(instance_values[0, 0], instance_values[1, 0], instance_values[2, 0],
                        'ko', markersize=10, label='start')
                ax.plot(instance_values[0, -1], instance_values[1, -1], instance_values[2, -1],
                        'yo', markersize=10, label='end')
                ax.plot(instance_values[0, get_stim_start_time()],
                        instance_values[1, get_stim_start_time()],
                        instance_values[2, get_stim_start_time()],
                        'ro', markersize=10, label='Stimulus ON')
    ax.set_xlabel('PC 1')
    ax.set_ylabel('PC 2')
    ax.set_zlabel('PC 3')
    ax.view_init(elev=31, azim=150)

plt.show()



sys.exit()


# ------------------------------------------------------------

## plot the PCA transformed matrix all instances
if 0:
    # -- Plot 3D --
    for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
        curr_color = colors_categories[instance_id // num_instances_each_category]
        # print(instance_values.shape)
        #ax = axs[0]
        ax = plt.gca()
        #ax.set_projection('3d')
        #plot_pca = ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=curr_color)
        plot_pca = ax.plot(instance_values[0, :],
                           instance_values[1, :],
                           instance_values[2, :], '.-', color=curr_color)
        ## plot only the first point as a circle
        if 0:
            #ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='start')
            #ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='end')
            ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'ro', markersize=10, label='Stimulus ON')
    #print("Stimulus onset bin location: ", get_stim_start_time())
    ax.set_xlabel('PC 1')
    ax.set_ylabel('PC 2')
    ax.set_zlabel('PC 3')
    #ax.title.set_text('2D PCA of Spike Data all instances')
else:
    # -- Plot 2D --
    for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
        curr_color = colors_categories[instance_id // num_instances_each_category]
        # print(instance_values.shape)
        #ax = axs[0]
        ax = plt.gca()
        #plot_pca = ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=curr_color)
        plot_pca = ax.plot(instance_values[2, :], instance_values[3, :], '.-', color=curr_color)
        ## plot only the first point as a circle
        if 0:
            ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='start')
            ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='end')
            ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='Stimulus ON')
    print("Stimulus onset bin location: ", get_stim_start_time())

    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.title.set_text('2D PCA of Spike Data all instances')
    

if 0:

    ## plot the PCA for each category separately
    for key, values in category_instance_dict.items():
        plt.title('2D PCA of Spike Data per category')
        for instance_id in values:
            instance_values = pca_matrix_all_instances_original[instance_id]
            print(instance_values.shape)
            ax = axs[(instance_id // num_instances_each_category) + 1]
            ax.plot(instance_values[0, :], instance_values[1, :], '.-')
            # plot only the first point as a circle
            ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='start')
            ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='end')
            ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='Stimulus ON')
        #ax.set_xlim(-70, 200)
        #ax.set_ylim(-100, 200)
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.title.set_text('Category: {}'.format(key))

#fig.legend(loc='upper right')
plt.tight_layout()
plt.show()
