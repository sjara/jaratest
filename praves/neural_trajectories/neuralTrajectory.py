# The functions are in the order of dependency

## import external libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import sys 

## import jara toolbox libraries

## define the path to the jaratoolbox directory
JARATOOL_PATH = '/Users/praveslamichhane/src/jaratoolbox' 
## append the path to the sys.path
sys.path.append(JARATOOL_PATH)

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

## internal functions

def load_data(inforecFile):
    """
    This function loads the ephys data and behavioral data for the cell ensemble. We only load the "naturalSound" session data
    """
    celldb = celldatabase.generate_cell_database(inforecFile)
    ensemble = ephyscore.CellEnsemble(celldb)
    ephysData, bdata = ensemble.load("naturalSound")
    return ephysData, bdata

def align_cells_to_stimulus_onset(ephysData, bdata):
    """
    This function aligns all cells to the stimulus onset
    """
    nTrials = len(bdata["soundID"])
    eventOnsetTimes = ephysData["events"]["stimOn"][:nTrials]
    timeRange = [-1.5, 5.5]
    binSize = 0.5
    spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)
    return spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll

def create_boolean_2D_array():
    """
    This function creates a boolean 2D array representing the sound instance of each trial
    """
    currentStim = bdata["soundID"]
    possibleStims = np.unique(currentStim)
    return possibleStims

def get_category_instance_dictionary(total_categories=5, possibleStims, time_aligned_matrix_all_instances):
    """
    This function returns a dictionary with the category as the key and the instance as the value
    """
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

    return category_instance_dict


def get_stim_start_time(time_range=[-1.5, 5.5], bin_size=0.5, stim_start=0):
    print("Number of seconds each bin: ", bin_size)
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

def get_trials_each_instance():
    """
    This function sorts trials by stimulus type and extracts the type into each stimulus type
    """
    trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStims)
    nTrialsEachCond = trialsEachCond.sum(axis=0)
    return nTrialsEachCond


def time_aligned_matrix_2D(instance_id):
    """
    This function creates a 2D array of the number of spike counts for each cell for every time bin. Dimensions = (num of cells x time bins). The values inside the matrix represent the number of spikes for the particular neuron at a particular time bin.
    """
    for cell_num in range(len(indexLimitsEachTrialAll)):
        total_spikes = []
        spikes_curr_cell = spikeTimesFromEventOnsetAll[cell_num]
        indices_curr_cell = indexLimitsEachTrialAll[cell_num]
        indices_to_select = indices_curr_cell[:, trials_category_0]
        for index in indices_to_select.T: ## this is where the problem is 
            total_spikes.append(spikes_curr_cell[index[0]:index[1] + 1])
        spikes_category_0.append(total_spikes)
        return spikes_instance 

def time_aligned_matrix_3D():
    pass

def pca():
    pass

def plot_pca():
    pass

def get_category_instance_dictionary():
    pass

def get_distance_between_categories():
    pass

def get_distance_between_instances_of_the_same_category():
    pass


# 1. time aligned matrix 2D
# 2. time aligned matrix 3D -> Incorporates the time aligned matrix 2D
# 3. pca -> Incorporates the time aligned matrix 3D
# 4. plot pca -> Incorporates the pca
# 5. get category instance dictionary 
# 6. get distance between categories -> Incorporates the get category instance dictionary
# 7. get distance between instances of the same category -> Incorporates the get category instance dictionary

def main():
    pass

if __name__ == "__main__":
    main()