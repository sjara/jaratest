'''
Load in behavior data corresponding to the LFP data.

Create uncollapsed PSTH given a stimulus type of interest. A figure is made illustrating
stimulus onset and 
'''

from jaratoolbox import loadneuropix
from jaratoolbox import loadbehavior, behavioranalysis
from jaratoolbox import settings
import matplotlib.pyplot as plt
import jeremy_psth as jpsth
import numpy as np
import os


subject = 'feat018'
session = '2024-06-14_11-20-22'
dataStream = 'Neuropix-PXI-100.1'
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', session)

events = loadneuropix.RawEvents(rawDataPath, dataStream)
eventOnsetTimes = events.get_onset_times() # Stimulus onset times ... 331 in total

contData = loadneuropix.Continuous(rawDataPath, dataStream)
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

## Load in behavior data corresponding to the LFP data.
subject = 'feat018'
paradigm = 'am_tuning_curve'
session = '20240614a'
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

eventOnsetTimes = jpsth.fix_stimuli_number_mismatch(bdata, 'currentFreq', eventOnsetTimes)

frequencies_each_trial = bdata['currentFreq']
array_of_frequencies = np.unique(bdata['currentFreq'])
trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

time_upper = 0.2
time_lower = 0.2
psth_upper = jpsth.time_to_indices(time_upper, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEYOND stimulus onset
psth_lower = jpsth.time_to_indices(time_lower, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEFORE stimulus onset
print(f"Indices below: {psth_lower}\nIndices above: {psth_upper}")

'''
Single figure
'''
# Grab your trials of interest
trials = trialsEachCond[:,6]

psth_uncollapsed, collection_outcome_list = jpsth.get_psth_uncollapsed(contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower)

print(f"Uncollapsed psth shape: {psth_uncollapsed.shape}")
plt.figure(figsize=(10,5))
plt.imshow(psth_uncollapsed.mean(axis=0).T * bitVolts, aspect='auto',
           extent=[-time_lower, time_upper, 0, nChannels])
plt.colorbar(label='Amplitude (uV)')
plt.axvline(x=1/sampleRate, c='r', label='Stimulus onset')
plt.legend(loc='upper left')
plt.title("Heatmap of average LFP data for a given stimuli.")
plt.xlabel("Time evolution (s)")
plt.ylabel("Channel index")
plt.show()

'''
4 column subplot of all stimuli
'''
num_trials = trialsEachCond.T.shape[0]  # Number of subplots needed
cols = min(num_trials, 4)  # Maximum 4 subplots in a row
rows = int(np.ceil(num_trials / cols))  # Determine rows needed

fig, axes = plt.subplots(rows, cols, figsize=(16, 2 * rows))  # Adjust figure size

# Flatten axes if there's only one row to avoid indexing issues
if rows == 1:
    axes = np.reshape(axes, (1, -1))

for idx, trials in enumerate(trialsEachCond.T):
    psth_uncollapsed, collection_outcome_list = jpsth.get_psth_uncollapsed(
        contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower
    )
    
    row = idx // 4  # Determine row
    col = idx % 4   # Determine column

    im = axes[row, col].imshow(
        psth_uncollapsed.mean(axis=0).T * bitVolts, 
        aspect='auto',
        extent=[-time_lower, time_upper, 0, nChannels]
    )
    
    axes[row, col].axvline(x=1/sampleRate, c='r')
    # axes[row, col].legend(loc='upper left')
    axes[row, col].set_title(f"Stimulus {idx}")
    axes[row, col].set_xlabel("Time evolution (s)")
    axes[row, col].set_ylabel("Channel index")

# Remove unused axes if num_trials is less than total subplots
for idx in range(num_trials, rows * cols):
    fig.delaxes(axes.flatten()[idx])

cbar_ax = fig.add_axes([0.92, 0.2, 0.02, 0.6])  # Position the colorbar correctly
fig.colorbar(im, cax=cbar_ax, label='Amplitude (uV)')  # Apply to all subplots

plt.tight_layout(rect=[0, 0, 0.9, 1])  # Adjust layout to prevent overlap
plt.show()