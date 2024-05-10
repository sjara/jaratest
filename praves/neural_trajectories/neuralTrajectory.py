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