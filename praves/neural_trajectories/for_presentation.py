
"""
Contains the functions used in neural_trajectory_pipeline.py and neural_trajectory_pipeline_multiple_subjects.py

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.decomposition import PCA

def get_stim_start_bin(time_range, bin_size, stim_start=0):
    start_time = time_range[0]
    curr_bin = 0
    while start_time <= time_range[1]:
        end_time = start_time + bin_size
        if start_time <= stim_start < end_time: ## note that this is the bin where the sound is on -> interpret carefully 
            return curr_bin
        start_time = end_time
        curr_bin += 1
    raise ValueError("Stimulus start time is outside the time range")

def extract_spikes_per_cell(cell_num, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, trials_current_instance):
    spikes_curr_cell = spikeTimesFromEventOnsetAll[cell_num]
    indices_curr_cell = indexLimitsEachTrialAll[cell_num]
    indices_to_select = indices_curr_cell[:, trials_current_instance]
    return [spikes_curr_cell[index[0]:index[1] + 1] for index in indices_to_select.T]

def bin_spikes(curr_cell, binEdges):
    return [np.histogram(trial, binEdges)[0] for trial in curr_cell]

# def bin_spikes_with_sliding_window(curr_cell, binEdges, window_size, step_size):
#     binned_spikes = []
#     for trial in curr_cell:
#         trial_binned_spikes = []
#         for start in range(0, len(binEdges) - window_size, step_size):
#             window_bins = binEdges[start:start + window_size + 1]
#             binned_count = np.histogram(trial, bins=window_bins)[0]
#             trial_binned_spikes.append(np.sum(binned_count))
#         binned_spikes.append(trial_binned_spikes)
#     return np.array(binned_spikes)


def process_instance(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE):
    current_instance = np.where(condEachSortedTrial == instance_id)
    trials_current_instance = sortedTrials[current_instance]
    
    spikes_curr_instance = [extract_spikes_per_cell(cell_num, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, trials_current_instance)
                            for cell_num in range(len(indexLimitsEachTrialAll))]
    
    binEdges = np.arange(TIME_RANGE[0], TIME_RANGE[1], BIN_SIZE)
    spikes_binned_all_cells = [bin_spikes(cell, binEdges) for cell in spikes_curr_instance]
    
    total_spikes_all_cells = [np.sum(cell, axis=0) for cell in spikes_binned_all_cells]
    
    return np.array(total_spikes_all_cells)

# def process_instance_with_sliding_bins(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE, WINDOW_SIZE, STEP_SIZE):
#     current_instance = np.where(condEachSortedTrial == instance_id)
#     trials_current_instance = sortedTrials[current_instance]
    
#     spikes_curr_instance = [extract_spikes_per_cell(cell_num, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, trials_current_instance)
#                             for cell_num in range(len(indexLimitsEachTrialAll))]
    
#     binEdges = np.arange(TIME_RANGE[0], TIME_RANGE[1], BIN_SIZE)
#     spikes_binned_all_cells = [bin_spikes_with_sliding_window(cell, binEdges, WINDOW_SIZE, STEP_SIZE) for cell in spikes_curr_instance]
    
#     total_spikes_all_cells = [np.sum(cell, axis=0) for cell in spikes_binned_all_cells]
    
#     return np.array(total_spikes_all_cells)

def create_category_instance_dict(possibleStims, total_categories):
    categories = list(np.arange(0, total_categories, 1))
    num_instances_each_category = len(possibleStims) // total_categories
    category_instance_dict = {}
    for instance_id in range(len(possibleStims)):
        instance_category = categories[instance_id // num_instances_each_category]
        if instance_category in category_instance_dict:
            category_instance_dict[instance_category].append(instance_id)
        else:
            category_instance_dict[instance_category] = [instance_id]
    return category_instance_dict


def get_pca_matrix_all_instances(time_aligned_matrix_all_instances, DIMS=2):
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
    num_trials = time_aligned_matrix_all_instances.shape[0]
    num_cells_pca = DIMS 
    num_bins_per_trial = time_aligned_matrix_all_instances.shape[2] 

    pca_matrix_all_instances_reshaped_original = pca_matrix_all_instances.reshape(num_cells_pca, num_trials, num_bins_per_trial)

    ## transpose the matrix so that the dimension information is preserved
    pca_matrix_all_instances_original = pca_matrix_all_instances_reshaped_original.transpose(1, 0, 2)
    return pca_matrix_all_instances_original


def plot_pca(pca_matrix_all_instances_original, category_instance_dict, colors_categories, TIME_RANGE, BIN_SIZE, soundDuration, num_instances_each_category):
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    axs = axs.flatten()
    pad_value = 20

    legend_elements = []

    def plot_instance(ax, instance_values, color, label_start_end=True):
        ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=color)
        if label_start_end:
            try:
                stim_start_bin = get_stim_start_bin(TIME_RANGE, BIN_SIZE)
                stim_end_bin = stim_start_bin + int(soundDuration / BIN_SIZE)
                print(f"Stimulus start bin: {stim_start_bin}, Stimulus end bin: {stim_end_bin}")
                start_handle = ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='start')[0]
                end_handle = ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='end')[0]

                # Plot points where the stimulus is being presented
                stim_handles = []
                for bin_idx in range(stim_start_bin, stim_end_bin + 1):
                    intensity = 1 - (bin_idx - stim_start_bin) / (stim_end_bin - stim_start_bin)  # Grade the intensity based on how close it is to stim start
                    stim_handle = ax.plot(instance_values[0, bin_idx], instance_values[1, bin_idx], 'o', color=mcolors.to_rgba('red', intensity), label='Stimulus ON')[0]
                    stim_handles.append(stim_handle)

                if not legend_elements:
                    legend_elements.extend([start_handle, end_handle, stim_handles[0]])

            except ValueError as e:
                print(f"Error: {e}")

    min_x = np.min(pca_matrix_all_instances_original[:, 0, :])
    max_x = np.max(pca_matrix_all_instances_original[:, 0, :])
    min_y = np.min(pca_matrix_all_instances_original[:, 1, :])
    max_y = np.max(pca_matrix_all_instances_original[:, 1, :])

    # Plot the PCA transformed matrix for all instances
    for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
        curr_color = colors_categories[instance_id // num_instances_each_category]
        ax = axs[0]
        plot_instance(ax, instance_values, curr_color)

    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.title.set_text('All Categories')
    ax.set_xlim(min_x - pad_value, max_x + pad_value)
    ax.set_ylim(min_y - pad_value, max_y + pad_value)
    count = 0
    # Plot the PCA for each category separately
    for key, values in category_instance_dict.items():
        if key in [2, 3, 4]:
            count += 1
            for instance_id in values:
                instance_values = pca_matrix_all_instances_original[instance_id]
                ax = axs[count]
                plot_instance(ax, instance_values, colors_categories[key])
            ax.set_xlim(min_x - pad_value, max_x + pad_value)
            ax.set_ylim(min_y - pad_value, max_y + pad_value)
            ax.set_xlabel('Principal Component 1')
            ax.set_ylabel('Principal Component 2')
            ax.title.set_text(f'Category: {key}')

    fig.legend(handles=legend_elements, loc='upper right')
    plt.tight_layout()
    plt.show()

def plot_pca_1(pca_matrix_all_instances_original, category_instance_dict, colors_categories, TIME_RANGE, BIN_SIZE, soundDuration, num_instances_each_category):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Adjust figsize to ensure subplots have enough space
    axs = axs.flatten()
    pad_value = 5

    legend_elements = []

    def plot_instance(ax, instance_values, color, label_start_end=True):
        ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=color)
        if label_start_end:
            try:
                stim_start_bin = get_stim_start_bin(TIME_RANGE, BIN_SIZE)
                stim_end_bin = stim_start_bin + int(soundDuration / BIN_SIZE)
                start_handle = ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='start')[0]
                end_handle = ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='end')[0]
                # Plot points where the stimulus is being presented
                stim_handles = []
                for bin_idx in range(stim_start_bin, stim_end_bin + 1):
                    intensity = 1 - (bin_idx - stim_start_bin) / (stim_end_bin - stim_start_bin)
                    stim_handle = ax.plot(instance_values[0, bin_idx], instance_values[1, bin_idx], 'o', color=mcolors.to_rgba('red', intensity), label='Stimulus ON')[0]
                    stim_handles.append(stim_handle)

                if not legend_elements:
                    legend_elements.extend([start_handle, end_handle, stim_handles[0]])

            except ValueError as e:
                print(f"Error: {e}")

    # Set axis limits and labels
    min_x = np.min(pca_matrix_all_instances_original[:, 0, :])
    max_x = np.max(pca_matrix_all_instances_original[:, 0, :])
    min_y = np.min(pca_matrix_all_instances_original[:, 1, :])
    max_y = np.max(pca_matrix_all_instances_original[:, 1, :])

    # Customize subplots
    for ax in axs:
        ax.set_xlim(min_x - pad_value, max_x + pad_value)
        ax.set_ylim(min_y - pad_value, max_y + pad_value)
        ax.set_aspect('equal', adjustable='box')
        ax.tick_params(axis='both', labelsize=12)  # Increase tick label size
        ax.set_xlabel('')  # Remove x-axis labels
        ax.set_ylabel('')  # Remove y-axis labels

    # Plot PCA transformed matrix for all instances
    for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
        curr_color = colors_categories[instance_id // num_instances_each_category]
        ax = axs[0]
        plot_instance(ax, instance_values, curr_color)
    ax.title.set_text('All Categories')

    count = 0
    # Plot PCA for each category separately
    for key, values in category_instance_dict.items():
        if key in [2, 3, 4]:
            count += 1
            for instance_id in values:
                instance_values = pca_matrix_all_instances_original[instance_id]
                ax = axs[count]
                plot_instance(ax, instance_values, colors_categories[key])
            ax.title.set_text(f'Category: {key + 1}')

    fig.legend(handles=legend_elements, loc='upper right')
    # plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=0.1, wspace=0.1)
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


# def plot_distances(distance_all_instances, category_instance_dict, colors_categories, TIME_RANGE, BIN_SIZE, soundDuration, stim_start=0):
#     fig, axs = plt.subplots(2, 3, figsize=(15, 10))
#     axs = axs.flatten()  # Flatten the array of axes for easier indexing

#     stim_start_bin = get_stim_start_bin(TIME_RANGE, BIN_SIZE, stim_start)
#     print(f"Stimulus start bin: {stim_start_bin}")
#     stim_end_bin = stim_start_bin + int(soundDuration / BIN_SIZE)

#     for category_id, instance_ids in category_instance_dict.items():
#         if category_id >= len(axs):
#             continue  # Skip if category_id is out of bounds

#         ax = axs[category_id]  # Get the specific axis for this category
#         all_distances = []

#         for key, value in distance_all_instances.items():
#             if key[0] in instance_ids and key[1] in instance_ids:
#                 all_distances.append(value) ## for later use 
#                 time_in_seconds = np.arange(len(value)) * BIN_SIZE + TIME_RANGE[0]
#                 ax.plot(time_in_seconds, value, alpha=0.3, color=colors_categories[category_id])  # Plot individual distances

#         if all_distances:
#             all_distances = np.array(all_distances)
#             mean_distance = np.mean(all_distances, axis=0)
#             std_distance = np.std(all_distances, axis=0)

#             # Plot the average distance with standard deviation
#             time_in_seconds = np.arange(len(value)) * BIN_SIZE + TIME_RANGE[0]
#             ax.plot(time_in_seconds, mean_distance, label='Average Distance', color='black')
#             ax.fill_between(time_in_seconds, mean_distance - std_distance, mean_distance + std_distance, color='gray', alpha=0.5, label='Standard Deviation')

#             # Add axline for stimulus start time
#             stim_start_time = stim_start_bin * BIN_SIZE + TIME_RANGE[0]
#             ax.axvline(x=stim_start_time, color='red', linestyle='--', label='Sound ON')
#             stim_end_time = stim_end_bin * BIN_SIZE + TIME_RANGE[0]
#             ax.axvline(x=stim_end_time, color='green', linestyle='--', label='Sound OFF')

#         ax.set_title(f"Category {category_id + 1}")
#         # ax.set_xlabel("Time")
#         # ax.set_ylabel("Distance")
#         ax.set_ylim(bottom=0)
#         # Ensure x-ticks are integers
#         start_tick = np.ceil(TIME_RANGE[0] / BIN_SIZE) * BIN_SIZE
#         end_tick = np.floor(TIME_RANGE[1] / BIN_SIZE) * BIN_SIZE
#         ax.set_xticks(np.arange(start_tick, end_tick + BIN_SIZE, BIN_SIZE))
#         # ax.set_xticks(np.arange(TIME_RANGE[0], TIME_RANGE[1], BIN_SIZE))
#         ax.legend()  # Show legend on the specific subplot

#         # Ensure x-ticks are integers
#         start_tick = np.ceil(TIME_RANGE[0] / BIN_SIZE) * BIN_SIZE
#         end_tick = np.floor(TIME_RANGE[1] / BIN_SIZE) * BIN_SIZE
#         ax.set_xticks(np.arange(start_tick, end_tick + BIN_SIZE, BIN_SIZE))

#     plt.tight_layout()
#     plt.show()  # Display all plots



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


def plot_category_distances(distance_all_categories, TIME_RANGE, BIN_SIZE, soundDuration, stim_start=0):
    for categories, instance_dicts in distance_all_categories.items():
        stim_start_bin = get_stim_start_bin(TIME_RANGE, BIN_SIZE, stim_start)
        stim_end_bin = stim_start_bin + int(soundDuration / BIN_SIZE)
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
            time_in_seconds = np.arange(all_distances.shape[1]) * BIN_SIZE + TIME_RANGE[0]

        for i, (instance_pair, distances) in enumerate(instance_dicts.items()):
            ax = axs[i]
            ax.plot(time_in_seconds, distances, label=f"Pair {instance_pair}")
            avg_distance = average_distance_all_categories[categories][0]
            std_distance = average_distance_all_categories[categories][1]
            ax.plot(time_in_seconds, avg_distance, 'k--', label="Average Distance")  # Plot average distance
            ax.fill_between(time_in_seconds, avg_distance - std_distance, avg_distance + std_distance, color='gray', alpha=0.5)

            # Add axline for stimulus start time
            stim_start_time = stim_start_bin * BIN_SIZE + TIME_RANGE[0]
            ax.axvline(x=stim_start_time, color='red', linestyle='--', label='Sound ON')
            stim_end_time = stim_end_bin * BIN_SIZE + TIME_RANGE[0]
            ax.axvline(x=stim_end_time, color='green', linestyle='--', label='Sound OFF')

            ax.set_title(f"Distance for Instances {instance_pair}")
            ax.legend()  # Show legend on the specific subplot
            ax.set_xlabel("Time (bins)")
            ax.set_ylabel("Distance")
            # ax.set_xticks()
            ax.set_ylim(bottom=0)
    
        fig.suptitle(f"Distance for Categories {categories}")  # Set title for the entire figure 
        plt.tight_layout()
        plt.show()  # Display all plots


# Load modules
import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import importlib

# Define the path to the jaratoolbox directory
jara_src = '/Users/praveslamichhane/src/jaratoolbox'
# Append the path to the sys.path
sys.path.append(jara_src)

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

# Constants
TOTAL_CATEGORIES = 5
SESSION_DATE = "2024-03-20"
PROBE_DEPTH = 2413
TIME_RANGE = [-1.5, 5.5]
BIN_SIZE = 0.5
SOUND_TYPE = "naturalSound"
DIMS = 2
COLORS_CATEGORIES = ["red", "blue", "green", "cyan", "purple"]
WINDOW_SIZE = 5  # Window size in bins
STEP_SIZE = 1  # Step size in bins

def main():
    # Generate cell database
    inforecFile = os.path.join(settings.INFOREC_PATH, 'feat015_inforec.test.py')
    celldb = celldatabase.generate_cell_database(inforecFile)

    # Select cells to analyze
    celldbSubset = celldb[(celldb.date == SESSION_DATE) & (celldb.pdepth == PROBE_DEPTH)]

    # Create CellEnsemble class
    ensemble = ephyscore.CellEnsemble(celldbSubset)

    # Load ephys and behavioral data
    ephysData, bdata = ensemble.load(SOUND_TYPE)

    # Align all cells to the stimulus onset
    nTrials = len(bdata["soundID"])
    eventOnsetTimes = ephysData["events"]["stimOn"][:nTrials]
    soundDuration = bdata["targetDuration"][0]

    # Get spiketimes, trial index, and index limits for each trial for each cell
    spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = ensemble.eventlocked_spiketimes(eventOnsetTimes, TIME_RANGE)

    # Create boolean 2D array representing the sound instance of each trial
    currentStim = bdata["soundID"]
    possibleStims = np.unique(currentStim)
    trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStims)
    condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)

    # Process each instance and collect spike counts
    # time_aligned_matrix_all_instances = [nt.process_instance_with_sliding_bins(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE, WINDOW_SIZE, STEP_SIZE)
    #                                      for instance_id in possibleStims]


    time_aligned_matrix_all_instances = [process_instance(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE)
                                         for instance_id in possibleStims]

    # Convert list to numpy array
    time_aligned_matrix_all_instances = np.array(time_aligned_matrix_all_instances)
    print("Shape of time aligned matrix: ", time_aligned_matrix_all_instances.shape)

    # Perform PCA on the time-aligned spike counts
    pca_matrix_all_instances = get_pca_matrix_all_instances(time_aligned_matrix_all_instances, DIMS)

    # Create category-instance dictionary
    category_instance_dict = create_category_instance_dict(possibleStims, TOTAL_CATEGORIES)

    # Calculate number of instances per category
    num_instances_each_category = len(possibleStims) // TOTAL_CATEGORIES

    # # Plot PCA results
    # plot_pca_1(pca_matrix_all_instances, category_instance_dict, COLORS_CATEGORIES, TIME_RANGE, BIN_SIZE, soundDuration, num_instances_each_category)

    # Calculate distances between instances
    distance_all_instances = calculate_distances(time_aligned_matrix_all_instances)

    def plot_distances(distance_all_instances, category_instance_dict, colors_categories, TIME_RANGE, BIN_SIZE, soundDuration, stim_start=0):
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        axs = axs.flatten()

        stim_start_bin = get_stim_start_bin(TIME_RANGE, BIN_SIZE, stim_start)
        stim_end_bin = stim_start_bin + int(soundDuration / BIN_SIZE)

        for category_id, instance_ids in category_instance_dict.items():
            if category_id >= len(axs):
                continue

            ax = axs[category_id]
            all_distances = []

            for key, value in distance_all_instances.items():
                if key[0] in instance_ids and key[1] in instance_ids:
                    all_distances.append(value)
                    time_in_seconds = np.arange(len(value)) * BIN_SIZE + TIME_RANGE[0]
                    ax.plot(time_in_seconds, value, alpha=0.3, color=colors_categories[category_id])

            if all_distances:
                all_distances = np.array(all_distances)
                mean_distance = np.mean(all_distances, axis=0)
                std_distance = np.std(all_distances, axis=0)
                time_in_seconds = np.arange(len(mean_distance)) * BIN_SIZE + TIME_RANGE[0]
                ax.plot(time_in_seconds, mean_distance, label='Average Distance', color='black')
                ax.fill_between(time_in_seconds, mean_distance - std_distance, mean_distance + std_distance, color='gray', alpha=0.5, label='Standard Deviation')

                stim_start_time = stim_start_bin * BIN_SIZE + TIME_RANGE[0]
                ax.axvline(x=stim_start_time, color='red', linestyle='--', label='Sound ON')
                stim_end_time = stim_end_bin * BIN_SIZE + TIME_RANGE[0]
                ax.axvline(x=stim_end_time, color='green', linestyle='--', label='Sound OFF')

            ax.set_title(f"Category {category_id + 1}")
            ax.set_ylim(bottom=0)

            # Correct the x-ticks to be integers only
            start_tick = int(np.floor(TIME_RANGE[0] / BIN_SIZE) * BIN_SIZE)
            end_tick = int(np.ceil(TIME_RANGE[1] / BIN_SIZE) * BIN_SIZE)
            ticks = np.arange(start_tick, end_tick + 1, BIN_SIZE)
            ticks = ticks[np.logical_and(ticks >= TIME_RANGE[0], ticks <= TIME_RANGE[1])]
            ax.set_xticks(ticks)

            ax.legend()

        plt.tight_layout()
        plt.show()

    
    # plot_distances(distance_all_instances, category_instance_dict, COLORS_CATEGORIES, TIME_RANGE, BIN_SIZE, soundDuration)

    # Calculate category distances
    distance_all_categories = calculate_category_distances(time_aligned_matrix_all_instances, category_instance_dict)

    # Plot category distances
    plot_category_distances(distance_all_categories, TIME_RANGE, BIN_SIZE, soundDuration)

if __name__ == "__main__":
    main()