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

import neuralTrajectory as nt
importlib.reload(nt)

# Check if functions are available in nt module
print(dir(nt))

# Constants
TOTAL_CATEGORIES = 5
SESSION_DATE = "2024-03-20"
PROBE_DEPTH = 2413
TIME_RANGE = [-1.5, 5.5]
BIN_SIZE = 0.5
SOUND_TYPE = "naturalSound"
DIMS = 2
COLORS_CATEGORIES = ["red", "blue", "green", "cyan", "purple"]

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

    # Get spiketimes, trial index, and index limits for each trial for each cell
    spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = ensemble.eventlocked_spiketimes(eventOnsetTimes, TIME_RANGE)

    # Create boolean 2D array representing the sound instance of each trial
    currentStim = bdata["soundID"]
    possibleStims = np.unique(currentStim)
    trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStims)
    condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)

    # Process each instance and collect spike counts
    time_aligned_matrix_all_instances = [nt.process_instance(instance_id, condEachSortedTrial, sortedTrials, indexLimitsEachTrialAll, spikeTimesFromEventOnsetAll, TIME_RANGE, BIN_SIZE)
                                         for instance_id in possibleStims]

    # Convert list to numpy array
    time_aligned_matrix_all_instances = np.array(time_aligned_matrix_all_instances)
    print("Shape of time aligned matrix: ", time_aligned_matrix_all_instances.shape)

    # Perform PCA on the time-aligned spike counts
    pca = PCA(n_components=DIMS)
    pca_matrix_all_instances = [pca.fit_transform(instance.T).T for instance in time_aligned_matrix_all_instances]

    # Create category-instance dictionary
    category_instance_dict = nt.create_category_instance_dict(possibleStims, TOTAL_CATEGORIES)

    # Calculate number of instances per category
    num_instances_each_category = len(possibleStims) // TOTAL_CATEGORIES

    # Plot PCA results
    nt.plot_pca(pca_matrix_all_instances, category_instance_dict, COLORS_CATEGORIES, TIME_RANGE, BIN_SIZE, num_instances_each_category)

    # Calculate distances between instances
    distance_all_instances = nt.calculate_distances(time_aligned_matrix_all_instances)

    # Plot distances
    nt.plot_distances(distance_all_instances, category_instance_dict, COLORS_CATEGORIES)

    # Calculate category distances
    distance_all_categories = nt.calculate_category_distances(time_aligned_matrix_all_instances, category_instance_dict)

    # Plot category distances
    nt.plot_category_distances(distance_all_categories)

if __name__ == "__main__":
    main()
