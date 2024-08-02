import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis

subject = 'feat017'
sessionDate = '2024-04-08'
probeDepth = 3000

# a. Generate database using feat017’s inforec file
inforecFile = os.path.join(settings.INFOREC_PATH,f'{subject}_inforec.py')
inforecFile = inforecFile.replace('.py','.test.py') # b.Create a cellensemble for a specific session - exp9
celldb = celldatabase.generate_cell_database(inforecFile)

# c. Load ephys,bdata for naturalSound for that ensemble
ensemble = ephyscore.CellEnsemble(celldb)
ephysData, bdata = ensemble.load('naturalSound')

nTrials = len(bdata['soundID'])
eventOnsetTimes = ephysData['events']['stimOn'][:nTrials] # Ignore trials not in bdata
timeRange = [-0.5, 6]  # In seconds

# d. Call ensemble.eventlocked_spiketimes function
spikeTimesFromEventOnsetAll, trialIndexForEachSpikeAll, indexLimitsEachTrialAll = \
    ensemble.eventlocked_spiketimes(eventOnsetTimes, timeRange)

currentStim = bdata['soundID']
possibleStim = np.unique(currentStim)
trialsEachCond = behavioranalysis.find_trials_each_type(currentStim, possibleStim) # shape: (209, 20). 209 trials
nTrialsEachCond = trialsEachCond.sum(axis=0) # Total trials each stimulus was presented.

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

sound_id = 15
# extract trials for a specific stimulus (soundID)
indices_my_sound_id = np.where(condEachSortedTrial == sound_id)
trials_my_sound_id = sortedTrials[indices_my_sound_id]

sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

binSize = 0.1
binEdges = np.arange(timeRange[0], timeRange[1], binSize)
spikeCount = ensemble.spiketimes_to_spikecounts(binEdges)
spike_count_for_my_sound = spikeCount[:, trials_my_sound_id, :]

average_spike_count = (np.mean(spike_count_for_my_sound, axis=1))
firing_rate = average_spike_count/binSize

# for ind in range(average_spike_count.shape[0]):
#     print(f"Spike count for cell {ind} is {average_spike_count[ind][0]}")

cell_ind_to_compare = [134, 161] # Indices of the cells to compare. First value for x-axis and second for y-axis

plt.clf()
fig = plt.gcf()
# Create a figure with a grid of subplots (1 row for rasters side by side, 1 row for firing rate)
axs = fig.subplots(2, 2, gridspec_kw={'height_ratios': [1, 2]})

axs[1, 0].remove()
axs[1, 1].remove()

# Plot rasters for each neuron using a loop
for idx, indcell in enumerate(cell_ind_to_compare):
    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpikeAll[indcell]]
    axs[0, idx].plot(spikeTimesFromEventOnsetAll[indcell], sortedIndexForEachSpike, '.k', ms=1)
    axs[0, idx].set_xlabel('Time (s)')
    axs[0, idx].set_ylabel(f'[{indcell}] Sorted trials')
    axs[0, idx].set_title(f'Raster Plot for Neuron {indcell}')
    trial_index_sum = np.cumsum(nTrialsEachCond)
    axs[0, idx].set_ylim(trial_index_sum[sound_id], trial_index_sum[sound_id + 1])


# Merge the bottom two subplots for the firing rate plot
firing_rate_ax = plt.subplot2grid((2, 2), (1, 0), colspan=2, fig=fig)

x_data = firing_rate[cell_ind_to_compare[0]]
y_data = firing_rate[cell_ind_to_compare[1]]

firing_rate_ax.plot(x_data, y_data, 'ok-', alpha=0.5, linewidth=1)

# Add arrows to the line to indicate direction
for ind in range(len(x_data) - 1):
    plt.annotate("",
                 xy=(x_data[ind+1], y_data[ind+1]),
                 xytext=(x_data[ind], y_data[ind]),
                 arrowprops=dict(arrowstyle="->", color="b", lw=1),
                 annotation_clip=False)

# Add labels and title to the firing rate plot
plt.xlabel(f'Firing Rate for Neuron {cell_ind_to_compare[0]} (Hz)', fontsize=12)
plt.ylabel(f'Firing Rate for Neuron {cell_ind_to_compare[1]} (Hz)', fontsize=12)
plt.title(f'Neuron Firing Rate: Neuron {cell_ind_to_compare[0]} vs Neuron {cell_ind_to_compare[1]} (Window Duration: {binSize} s)', fontsize=14)
plt.legend()

# Calculate padding for axes
x_padding = (max(x_data) - min(x_data)) * 0.1
y_padding = (max(y_data) - min(y_data)) * 0.1

# Adjust axes limits with proportional padding
firing_rate_ax.set_xlim([min(x_data) - x_padding, max(x_data) + x_padding])
firing_rate_ax.set_ylim([min(y_data) - y_padding, max(y_data) + y_padding])

# Ensure both axes have correct tick marks and limits
firing_rate_ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))
firing_rate_ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}'))

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()