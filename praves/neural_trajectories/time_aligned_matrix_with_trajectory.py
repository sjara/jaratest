"""
This file builds upon the `time_aligned_matrix.py` file to plot the neural trajectory of 2 cells.
 
"""


## load modules
import os 
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

## define the path to the jaratoolbox directory
jara_src = '/Users/praveslamichhane/src/jaratoolbox' 
## append the path to the sys.path
sys.path.append(jara_src)

from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

## create a database of cells
inforecFile = os.path.join(settings.INFOREC_PATH, 'feat015_inforec.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)
INSTANCE_ID = 19

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

## create a boolean 2D array representing the sound category of each trial
currentStim = bdata["soundID"]
possibleStims = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStims)
nTrialsEachCond = trialsEachCond.sum(axis=0)

## sort trials by stimulus type and extract the type into each stimulus type
condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)

## extract trial category 0
category_ind_0 = np.where(condEachSortedTrial == INSTANCE_ID)
trials_category_0 = sortedTrials[category_ind_0]

## extract spikes for each cell for each trial in category 0
spikes_category_0 = []
print(len(indexLimitsEachTrialAll))
for cell_num in range(len(indexLimitsEachTrialAll)):
    total_spikes = []
    spikes_curr_cell = spikeTimesFromEventOnsetAll[cell_num]
    indices_curr_cell = indexLimitsEachTrialAll[cell_num]
    indices_to_select = indices_curr_cell[:, trials_category_0]
    for index in indices_to_select.T: ## this is where the problem is 
        total_spikes.append(spikes_curr_cell[index[0]:index[1] + 1])
    spikes_category_0.append(total_spikes)


## bin spikes for each cell
spikes_binned_all_cells = []
binEdges = np.arange(timeRange[0], timeRange[1], bin_size)
for cell_num in range(len(spikes_category_0)):
    curr_cell = spikes_category_0[cell_num]
    spikes_binned_curr_cell = []
    for trial in curr_cell:
        spike_counts, _ = np.histogram(trial, binEdges)
        spikes_binned_curr_cell.append(spike_counts)
        # print(len(spike_counts))
    spikes_binned_all_cells.append(spikes_binned_curr_cell)


## total spike counts for each cell in category 0 for each bin
total_spikes_all_cells = []
for cell_num in range(len(spikes_binned_all_cells)):
    curr_cell = spikes_binned_all_cells[cell_num]
    total_spikes_curr_cell = np.sum(curr_cell, axis=0)
    total_spikes_all_cells.append(total_spikes_curr_cell)

## use various print statements to check the dimensions of the average spikes
print("Number of cells: ", len(total_spikes_all_cells))
print("Total number of time bins: ", len(total_spikes_all_cells[0]))

## create a 2D numpy array for the sum of spikes for each cell in each bin
total_spikes_all_cells = np.array(total_spikes_all_cells)
print("Shape of spike array: ", total_spikes_all_cells.shape)
print("Max num of spike in a bin: ", np.max(total_spikes_all_cells))
print("Min num of spike in a bin: ", np.min(total_spikes_all_cells))

# plt.imshow(total_spikes_all_cells, aspect="auto", interpolation="nearest")
# plt.show()

## select 2 cells for plotting
## cell num = 6, 13 (indexed 0)

CELL_1 = 6
CELL_2 = 13
CELLS = [CELL_1, CELL_2]
new_mat = total_spikes_all_cells[CELLS, :]

## plot the trajectory
plt.clf()
plt.plot(new_mat[0, :], new_mat[1, :], '.-')
## plot only the first point as a circle
plt.plot(new_mat[0, 0], new_mat[1, 0], 'ko')
plt.xlabel(f"CELL {CELL_1}")
plt.ylabel(f"CELL {CELL_2}")
plt.title(f"Trajectory of cells from time {timeRange[0]} s to {timeRange[1]} s of the stimulus onset")
plt.show()

