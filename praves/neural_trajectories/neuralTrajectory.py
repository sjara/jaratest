
"""
Contains the functions used in neural_trajectory_pipeline.py and neural_trajectory_pipeline_multiple_subjects.py

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def get_stim_start_time(time_range, bin_size, stim_start=0):
    start_time = time_range[0]
    curr_bin = 0
    while start_time <= time_range[1]:
        end_time = start_time + bin_size
        if start_time <= stim_start <= end_time:
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

def bin_spikes_with_sliding_window(curr_cell, binEdges, window_size, step_size):
    binned_spikes = []
    for trial in curr_cell:
        trial_binned_spikes = []
        for start in range(0, len(binEdges) - window_size, step_size):
            window_bins = binEdges[start:start + window_size + 1]
            binned_count = np.histogram(trial, bins=window_bins)[0]
            trial_binned_spikes.append(np.sum(binned_count))
        binned_spikes.append(trial_binned_spikes)
    return np.array(binned_spikes)


def process_instance(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE):
    current_instance = np.where(condEachSortedTrial == instance_id)
    trials_current_instance = sortedTrials[current_instance]
    
    spikes_curr_instance = [extract_spikes_per_cell(cell_num, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, trials_current_instance)
                            for cell_num in range(len(indexLimitsEachTrialAll))]
    
    binEdges = np.arange(TIME_RANGE[0], TIME_RANGE[1], BIN_SIZE)
    spikes_binned_all_cells = [bin_spikes(cell, binEdges) for cell in spikes_curr_instance]
    
    total_spikes_all_cells = [np.sum(cell, axis=0) for cell in spikes_binned_all_cells]
    
    return np.array(total_spikes_all_cells)

def process_instance_with_sliding_bins(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE, WINDOW_SIZE, STEP_SIZE):
    current_instance = np.where(condEachSortedTrial == instance_id)
    trials_current_instance = sortedTrials[current_instance]
    
    spikes_curr_instance = [extract_spikes_per_cell(cell_num, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, trials_current_instance)
                            for cell_num in range(len(indexLimitsEachTrialAll))]
    
    binEdges = np.arange(TIME_RANGE[0], TIME_RANGE[1], BIN_SIZE)
    spikes_binned_all_cells = [bin_spikes_with_sliding_window(cell, binEdges, WINDOW_SIZE, STEP_SIZE) for cell in spikes_curr_instance]
    
    total_spikes_all_cells = [np.sum(cell, axis=0) for cell in spikes_binned_all_cells]
    
    return np.array(total_spikes_all_cells)

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


def plot_pca(pca_matrix_all_instances_original, category_instance_dict, colors_categories, TIME_RANGE, BIN_SIZE, num_instances_each_category):
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    axs = axs.flatten()

    def plot_instance(ax, instance_values, color, label_start_end=True):
        ax.plot(instance_values[0, :], instance_values[1, :], '.-', color=color)
        if label_start_end:
            try:
                stim_start_bin = get_stim_start_time(TIME_RANGE, BIN_SIZE)
                ax.plot(instance_values[0, 0], instance_values[1, 0], 'ko', markersize=10, label='start')
                ax.plot(instance_values[0, -1], instance_values[1, -1], 'yo', markersize=10, label='end')
                ax.plot(instance_values[0, stim_start_bin], instance_values[1, stim_start_bin], 'rx', markersize=10, label='Stimulus ON')
            except ValueError as e:
                print(f"Error: {e}")

    # Plot the PCA transformed matrix for all instances
    for instance_id, instance_values in enumerate(pca_matrix_all_instances_original):
        curr_color = colors_categories[instance_id // num_instances_each_category]
        ax = axs[0]
        plot_instance(ax, instance_values, curr_color)

    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.title.set_text('2D PCA of Spike Data all instances')

    # Plot the PCA for each category separately
    for key, values in category_instance_dict.items():
        for instance_id in values:
            instance_values = pca_matrix_all_instances_original[instance_id]
            ax = axs[(instance_id // num_instances_each_category) + 1]
            plot_instance(ax, instance_values, colors_categories[key])
        ax.set_xlim(-150, 400)
        ax.set_ylim(-150, 350)
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.title.set_text(f'Category: {key}')

    fig.legend(loc='upper right')
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
    fig, axs = plt.subplots(2, 3)
    axs = axs.flatten()  # Flatten the array of axes for easier indexing

    for category_id, instance_ids in category_instance_dict.items():
        ax = axs[category_id]  # Get the specific axis for this category
        for key, value in distance_all_instances.items():
            if key[0] in instance_ids and key[1] in instance_ids:
                ax.plot(value, label=str(key), color=colors_categories[category_id])  # Plot on the specific subplot
        ax.set_title(f"Distance as a function of time for Category {category_id}")
        ax.legend()  # Show legend on the specific subplot

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

# def plot_category_distances(distance_all_categories):
#     for categories, instance_dicts in distance_all_categories.items():
#         num_plots = len(instance_dicts)
#         plot_rows = int(num_plots // np.sqrt(num_plots))
#         plot_cols = int(np.ceil(num_plots / plot_rows))
#         fig, axs = plt.subplots(plot_rows, plot_cols)
#         axs = axs.flatten()  # Flatten the array of axes for easier indexing

#         average_distance_all_categories = {}
#         for key, value in distance_all_categories.items():
#             all_distances = []
#             for instance_key, instance_value in value.items():
#                 all_distances.append(instance_value)
#             all_distances = np.array(all_distances)
#             average_distance_all_categories[key] = (np.mean(all_distances, axis=0), np.std(all_distances, axis=0))

#         for i, (key, value) in enumerate(instance_dicts.items()):
#             ax = axs[i]
#             ax.plot(value, label=str(key))  # Plot on the specific subplot
#             ax.set_title(f"Distance for Instances {key}")
#             ax.legend()  # Show legend on the specific subplot
#             ax.set_xlabel("Time (bins)")
#             ax.set_ylabel("Distance")
    
#         fig.suptitle(f"Distance for Categories {categories}")  # Set title for the entire figure 
#         plt.tight_layout()
#         plt.show()  # Display all plots


def plot_category_distances(distance_all_categories):
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

        for i, (instance_pair, distances) in enumerate(instance_dicts.items()):
            ax = axs[i]
            ax.plot(distances, label=f"Pair {instance_pair}")
            avg_distance = average_distance_all_categories[categories][0]
            std_distance = average_distance_all_categories[categories][1]
            ax.plot(avg_distance, 'k--', label="Average Distance")  # Plot average distance
            ax.fill_between(range(len(avg_distance)), avg_distance - std_distance, avg_distance + std_distance, color='gray', alpha=0.5)
            ax.set_title(f"Distance for Instances {instance_pair}")
            ax.legend()  # Show legend on the specific subplot
            ax.set_xlabel("Time (bins)")
            ax.set_ylabel("Distance")
    
        fig.suptitle(f"Distance for Categories {categories}")  # Set title for the entire figure 
        plt.tight_layout()
        plt.show()  # Display all plots