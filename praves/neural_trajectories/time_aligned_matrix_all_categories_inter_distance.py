"""
This script is used to create a time aligned matrix of the spike counts for each cell in the ensemble for all the instances.
"""


## load modules
import os 
import sys
import numpy as np
from matplotlib import pyplot as plt
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


## calculate the distance between the time_aligned_matrix for each instance
## the distance is calculated using the euclidean distance between the time_aligned_matrix for each instance as a function of time
## distance (matrix A, matrix B, time) = |vector A - vector B| for each time point

## create a dictionary to store the distance between the time_aligned_matrix for each instance
distance_all_categories = {} ## key: (category_id_1, category_id_2), value: {(instance a, instance b): [distance array for each time point for two instances]}
for category_id, instance_ids in category_instance_dict.items():
    for other_category_id, other_instance_ids in category_instance_dict.items():
        if category_id < other_category_id:
            distance_all_instances = {} ## key: instance_id_1, instance_id_2, value: [distance array for each time point for two instances]
            for instance_id, instance_value in enumerate(time_aligned_matrix_all_instances):
                for other_instance_id, other_instance_value in enumerate(time_aligned_matrix_all_instances):
                    if (instance_id in instance_ids) and (other_instance_id in other_instance_ids) and (instance_id < other_instance_id):
                        time_array = np.arange(0, instance_value.shape[1], 1)
                        distance_all_time_points = []
                        for time_point in time_array:
                            distance_vector = np.linalg.norm(instance_value[:, time_point] - other_instance_value[:, time_point])
                            distance_all_time_points.append(distance_vector)
                        distance_all_instances[(instance_id, other_instance_id)] = distance_all_time_points
            distance_all_categories[(category_id, other_category_id)] = distance_all_instances


## plot distance between categories 

for categories, instance_dicts in distance_all_categories.items():
    num_plots = len(instance_dicts)
    # print(num_plots)
    plot_rows = int(num_plots // np.sqrt(num_plots))
    plot_cols = int(num_plots // plot_rows)
    fig, axs = plt.subplots(plot_rows, plot_cols)
    axs = axs.flatten()  # Flatten the array of axes for easier indexing

    for i, (key, value) in enumerate(instance_dicts.items()):
        ax = axs[i]
        ax.plot(value, label=str(key))  # Plot on the specific subplot
        ax.set_title(f"Distance for Instances {key}")
        ax.legend()  # Show legend on the specific subplot
        ax.set_xlabel("Time (bins)")
        ax.set_ylabel("Distance")
    
    fig.suptitle(f"Distance for Categories {categories}")  # Set title for the entire figure 
    plt.tight_layout()
    plt.show()  # Display all plots
