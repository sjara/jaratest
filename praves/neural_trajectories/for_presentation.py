"""
This file applies the NumPy PCA algorithm to the 3D array obtained from `time_aligned_matrix_all_instances.py`

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
COLORS_CATEGORIES = ["red", "blue", "green", "cyan", "purple"]

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

# ## get the stimulus start time for the time range and bin size
# def get_stim_start_time(time_range=timeRange, bin_size=bin_size, stim_start=0):
#     print("Number of seconds each bin: ", bin_size)
#     start_time = time_range[0]
#     end_time = start_time + bin_size
#     curr_bin = 0
#     while True:
#         if stim_start < time_range[0] or stim_start > time_range[1]:
#            raise ValueError("Stimulus start time is outside the time range")  
#         else:
#             if start_time <= stim_start and stim_start < end_time:
#                 print("Stimulus start time bin: ", curr_bin)
#                 return curr_bin
#             start_time = end_time
#             end_time = start_time + bin_size
#             curr_bin += 1 

# Function to get stimulus start time in seconds
def get_stim_start_time(time_range=[-1.5, 5.5], bin_size=0.5, stim_start=0):
    num_bins = int((time_range[1] - time_range[0]) / bin_size)
    bin_edges = np.linspace(time_range[0], time_range[1], num_bins + 1)
    return np.argmin(np.abs(bin_edges - stim_start))

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

# fig, axs = plt.subplots(1, 2, figsize=(15, 10))
# axs = axs.flatten()

# ## plot the PCA transformed matrix all instances
# for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
#     curr_color = colors_categories[instance_id // num_instances_each_category]
#     # print(instance_values.shape)
#     ax = axs[0]
#     plot_pca = ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=curr_color)
#     ## plot only the first point as a circle
#     ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='Recording Start')
#     ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='Recording End')
#     ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='Sound ON')
#     print("Stimulus onset bin location: ", get_stim_start_time())

# ax.set_xlabel('Principal Component 1')
# ax.set_ylabel('Principal Component 2')
# ax.title.set_text('2D PCA of Spike Data all instances')



# ## plot the PCA for only 1 category but separately
# for key, values in category_instance_dict.items():
#     cat_select = 3
#     ## initialize legend elements
#     legend_elements = []
#     if key == cat_select:
#         plt.title(f'Neural Trajectories for Category {cat_select}')
#         for instance_id in values:
#             instance_values = pca_matrix_all_instances_original[instance_id]
#             print(instance_values.shape)
#             ax = axs[1]

#             ax.plot(instance_values[0, :], instance_values[1, :], '.-')
#             # plot only the first point as a circle
#             ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='Recording Start')
#             ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='Recording End')
#             ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='Sound ON')
#         ax.set_xlim(-70, 200)
#         ax.set_ylim(-100, 200)
#         ax.set_xlabel('Principal Component 1')
#         ax.set_ylabel('Principal Component 2')
#         ax.title.set_text('Neural trajectory for Category: {}'.format(key))

# fig.legend(loc='upper right')
# plt.tight_layout()
# plt.show()



# Assuming 'category_instance_dict', 'pca_matrix_all_instances_original', 'colors_categories', 'num_instances_each_category', and 'get_stim_start_time' are defined

fig, axs = plt.subplots(1, 2, figsize=(15, 10))
axs = axs.flatten()

# Initialize a list to store legend elements
legend_elements = []

# Plot the PCA transformed matrix for all instances
for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
    curr_color = colors_categories[instance_id // num_instances_each_category]
    ax = axs[0]
    plot_pca = ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=curr_color)
    # Plot only the first point as a circle
    if instance_id == 0:
        legend_elements.append(ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='Recording Start')[0])
        legend_elements.append(ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='Recording End')[0])
        legend_elements.append(ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='Sound ON')[0])
    else:
        ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='_nolegend_')
        ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='_nolegend_')
        ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='_nolegend_')

ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.title.set_text('Neural Trajectories for all Categories')

# Plot the PCA for only one category separately
cat_select = 3
if cat_select in category_instance_dict:
    values = category_instance_dict[cat_select]
    plt.title(f'Neural Trajectories for Category {cat_select}')
    for instance_id in values:
        instance_values = pca_matrix_all_instances_original[instance_id]
        ax = axs[1]
        ax.plot(instance_values[0, :], instance_values[1, :], '.-')
        # Plot only the first point as a circle
        if instance_id == values[0]:
            ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='Recording Start')
            ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='Recording End')
            ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='Sound ON')
        else:
            ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='_nolegend_')
            ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='_nolegend_')
            ax.plot(instance_values[0, get_stim_start_time()], instance_values[1, get_stim_start_time()], 'rx', markersize=10, label='_nolegend_')

    ax.set_xlim(-70, 200)
    ax.set_ylim(-100, 200)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.title.set_text('Neural trajectory for Category: {}'.format(cat_select))
    ax.legend(loc='upper right')

# # Add the legend to the figure
# fig.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.show()



def calculate_distances(time_aligned_matrix_all_instances):
    distance_all_instances = {}
    num_instances = len(time_aligned_matrix_all_instances)
    for instance_id in range(num_instances):
        for other_instance_id in range(instance_id + 1, num_instances):
            instance_value = time_aligned_matrix_all_instances[instance_id]
            other_instance_value = time_aligned_matrix_all_instances[other_instance_id]
            time_array = np.arange(instance_value.shape[1])
            distance_all_time_points = [np.linalg.norm(instance_value[:, time_point] - other_instance_value[:, time_point])
                                        for time_point in time_array]
            distance_all_instances[(instance_id, other_instance_id)] = distance_all_time_points
    return distance_all_instances


def plot_distances(distance_all_instances, category_instance_dict, colors_categories):
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs = axs.flatten()  # Flatten the array of axes for easier indexing
    stim_start = 0
    stim_start_bin = get_stim_start_time(stim_start=stim_start)

    for category_id, instance_ids in category_instance_dict.items():
        if category_id >= len(axs):
            continue  # Skip if category_id is out of bounds

        ax = axs[category_id]  # Get the specific axis for this category
        all_distances = []

        for key, value in distance_all_instances.items():
            if key[0] in instance_ids and key[1] in instance_ids:
                all_distances.append(value)
                time_in_seconds = np.arange(len(value)) * bin_size
                ax.plot(time_in_seconds, value, alpha=0.3, color=colors_categories[category_id])  # Plot individual distances

        if all_distances:
            all_distances = np.array(all_distances)
            mean_distance = np.mean(all_distances, axis=0)
            std_distance = np.std(all_distances, axis=0)
            time_in_seconds = np.arange(len(mean_distance)) * bin_size + timeRange[0]

            # Plot the average distance with standard deviation
            ax.plot(time_in_seconds, mean_distance, label='Average Distance', color='black')
            ax.fill_between(time_in_seconds, mean_distance - std_distance, mean_distance + std_distance, color='gray', alpha=0.5, label='Standard Deviation')

            # Add axline for stimulus start time
            ax.axvline(x=stim_start_bin * bin_size, color='red', linestyle='--', label='Sound ON')

        ax.set_title(f"Distance as a function of time for Category {category_id}")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Distance")
        ax.legend()  # Show legend on the specific subplot

    plt.tight_layout()
    plt.show()  # Display all plots

    plt.tight_layout()
    plt.show()  # Display all plots



def calculate_category_distances(time_aligned_matrix_all_instances, category_instance_dict):
    distance_all_categories = {}
    for category_id, instance_ids in category_instance_dict.items():
        for other_category_id, other_instance_ids in category_instance_dict.items():
            if category_id < other_category_id:
                distance_all_instances = {}
                for instance_id in instance_ids:
                    for other_instance_id in other_instance_ids:
                        if instance_id < other_instance_id:
                            instance_value = time_aligned_matrix_all_instances[instance_id]
                            other_instance_value = time_aligned_matrix_all_instances[other_instance_id]
                            time_array = np.arange(instance_value.shape[1])
                            distance_all_time_points = [np.linalg.norm(instance_value[:, time_point] - other_instance_value[:, time_point])
                                                        for time_point in time_array]
                            distance_all_instances[(instance_id, other_instance_id)] = distance_all_time_points
                distance_all_categories[(category_id, other_category_id)] = distance_all_instances
    
    return distance_all_categories


def plot_category_distances(distance_all_categories):
    stim_start = 0
    stim_start_bin = get_stim_start_time(stim_start=stim_start)
    for categories, instance_dicts in distance_all_categories.items():
        num_plots = len(instance_dicts)
        plot_rows = int(np.sqrt(num_plots))
        plot_cols = int(np.ceil(num_plots / plot_rows))
        fig, axs = plt.subplots(plot_rows, plot_cols, figsize=(15, 10))
        axs = axs.flatten()  # Flatten the array of axes for easier indexing

        average_distance_all_categories = {}
        for key, value in distance_all_categories.items():
            all_distances = []
            for instance_value in value.values():
                all_distances.append(instance_value)
            all_distances = np.array(all_distances)
            average_distance_all_categories[key] = (np.mean(all_distances, axis=0), np.std(all_distances, axis=0))
            time_in_seconds = np.arange(len(average_distance_all_categories)) * bin_size + timeRange[0]

        for i, (instance_pair, distances) in enumerate(instance_dicts.items()):
            ax = axs[i]
            ax.plot(distances, label=f"Pair {instance_pair}")
            avg_distance = average_distance_all_categories[categories][0]
            std_distance = average_distance_all_categories[categories][1]
            ax.plot(time_in_seconds, avg_distance, 'k--', label="Average Distance")  # Plot average distance
            ax.fill_between(range(len(avg_distance)), avg_distance - std_distance, avg_distance + std_distance, color='gray', alpha=0.5)

            # Add axline for stimulus start time
            ax.axvline(x=stim_start_bin * bin_size, color='red', linestyle='--', label='Sound ON')

            ax.set_title(f"Distance for Instances {instance_pair}")
            ax.legend()  # Show legend on the specific subplot
            ax.set_xlabel("Time (bins)")
            ax.set_ylabel("Distance")
    
        fig.suptitle(f"Distance for Categories {categories}")  # Set title for the entire figure 
        plt.tight_layout()
        plt.show()  # Display all plots


# Calculate distances between instances
distance_all_instances = calculate_distances(time_aligned_matrix_all_instances)

# Plot distances
plot_distances(distance_all_instances, category_instance_dict, COLORS_CATEGORIES)

# Calculate category distances
distance_all_categories = calculate_category_distances(time_aligned_matrix_all_instances, category_instance_dict)

# Plot category distances
plot_category_distances(distance_all_categories)

## plot hypotheses
nt.plot_hypotheses()
