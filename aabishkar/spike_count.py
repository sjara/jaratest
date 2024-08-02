import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots

# Count the number of spikes for each cell in the time period [0, 0.1] from sound onset for all trials of a given sound instance.

subject = 'feat015'
sessionDate = '2024-03-20'
probeDepth = 2413

# create database from the inforec file
inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
inforecFile = inforecFile.replace('.py','.test.py')
celldb = celldatabase.generate_cell_database(inforecFile)

ensemble = ephyscore.CellEnsemble(celldb)
ephysData, bdata = ensemble.load('naturalSound')

nTrials = len(bdata['soundID'])
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata
timeRange = [0, 0.1]  # In seconds

spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

currentStim = bdata['soundID']
possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim)
nTrialsEachCond = trialsEachCond.sum(axis=0)

'''
Original array:
[[False  True False]
 [ True False False]
 [False False  True]
 [False  True False]
 [ True False False]]

np.nonzero(trialsEachCond.T) result:
(array([0, 0, 1, 1, 2]), array([1, 4, 0, 3, 2]))

condEachSortedTrial: [0 0 1 1 2]
sortedTrials: [1 4 0 3 2]
'''
# Match (sort) trials by stimulus
condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)

# extract trials for a specific stimulus (soundID)
indices_my_sound_id = np.where(condEachSortedTrial == 1)
trials_my_sound_id = sortedTrials[indices_my_sound_id]

# extract spikes for each cell for all trials for a given stimulus
all_spikes_for_my_sound_id = []
print(len(indexLimitsEachTrialAll))
for cell in range(len(indexLimitsEachTrialAll)):
    cell_spikes_for_my_sound_id = []
    spikes_curr_cell = spikeTimesFromEventOnsetAll[cell]
    index_limits_curr_cell = indexLimitsEachTrialAll[cell]
    index_limits_my_sound_id = index_limits_curr_cell[:, trials_my_sound_id]
    # we transpose index_limits_my_sound_id so that
    # we get a 2-D array where each element is a 1-D array with start and end trial index
    '''
    [[0 2]
     [2 3]
     [3 6]
     [0 2]
     [2 3]]
    '''
    for index in index_limits_my_sound_id.T:
        cell_spikes_for_my_sound_id.append(spikes_curr_cell[index[0]:index[1] + 1]) # add 1 to include the end index
    all_spikes_for_my_sound_id.append(cell_spikes_for_my_sound_id)

# all_spikes_for_my_sound_id now has spikes for each cell for X trials where this stimulus was presented

binSize = 0.05
binEdges = np.arange(timeRange[0], timeRange[1], binSize)
spikeCount = ensemble.spiketimes_to_spikecounts(binEdges)
spike_count_for_my_sound = spikeCount[:, trials_my_sound_id, :]

average_spike_count = (np.mean(spike_count_for_my_sound, axis=1))

for ind in range(average_spike_count.shape[0]):
    print(f"Spike count for cell {ind} is {average_spike_count[ind][0]}")