'''
Load in behavior data corresponding to the LFP data.

Create uncollapsed PSTH given 
'''

from jaratoolbox import loadneuropix
from jaratoolbox import loadbehavior, behavioranalysis
from jaratoolbox import settings
import matplotlib.pyplot as plt
import jeremy_psth as jpsth
import jeremy_utils as jutils
import numpy as np
import os
reload(jpsth)
reload(jutils)


subject = 'feat018'
session = '2024-06-14_11-20-22'
dataStream = 'Neuropix-PXI-100.1'
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', session)

events = loadneuropix.RawEvents(rawDataPath, dataStream)
eventOnsetTimes = events.get_onset_times() # Stimulus onset times ... 331 in total

contData = loadneuropix.Continuous(rawDataPath, dataStream)
sampleRate = contData.sampleRate

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

psth_upper = jpsth.time_to_indices(3, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEYOND stimulus onset
psth_lower = jpsth.time_to_indices(3, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEFORE stimulus onset
print(f"Indices below: {psth_lower}\nIndices above: {psth_upper}")

# Grab your trials of interest
trials = trialsEachCond[:,6]

psth_uncollapsed, collection_outcome_list = jpsth.get_psth_uncollapsed(contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower)

print(f"Uncollapsed psth shape: {psth_uncollapsed.shape}")
plt.figure(figsize=(15,20))
plt.imshow(psth_uncollapsed.mean(axis=0).T)
plt.axvline(x=psth_lower, c='r')
plt.title("Heatmap of average LFP data for a given stimuli. | yellow = high, purple = low, red line = stimulus onset.")
plt.xlabel("Time evolution (left to right)")
plt.ylabel("Unorded channels")
plt.show()