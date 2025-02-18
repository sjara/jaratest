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
import jeremy_utils as jutils
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

psth_mean_list = []
collection_outcome_list = []
for idx, trials in enumerate(trialsEachCond.T):
    psth_uncollapsed, collection_outcomes = jpsth.get_psth_uncollapsed(
        contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower
    )
    psth_mean_list.append(psth_uncollapsed.mean(axis=0).T * bitVolts)
    collection_outcome_list.append(collection_outcomes)

jutils.make_4xN_subplots(psth_mean_list, time_lower, time_upper, nChannels, sampleRate, amplitude_units = 'μV')