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

time_upper = 0.4
time_lower = 0.2
psth_upper = jpsth.time_to_indices(time_upper, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEYOND stimulus onset
psth_lower = jpsth.time_to_indices(time_lower, sampleRate, 's') # Ex: Collect 3 seconds of datapoints BEFORE stimulus onset
print(f"Indices below: {psth_lower}\nIndices above: {psth_upper}")

''' Separate by probe columns '''

xmlfile = os.path.join(rawDataPath, r'Record Node 101/settings.xml')

probeMap, probeName = jutils.get_probemap(xmlfile)
columnInfo = jutils.grab_probe_columns(probeMap)

''' 4 column subplot of all stimuli '''
psth_mean_list = []
collection_outcome_list = []
for idx, trials in enumerate(trialsEachCond.T):
    psth_uncollapsed, collection_outcomes = jpsth.get_psth_uncollapsed(
        contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower
    )
    psth_mean_list.append(psth_uncollapsed.mean(axis=0).T * bitVolts)
    collection_outcome_list.append(collection_outcomes)
psth_mean_list = np.array(psth_mean_list)

''' Separate by column and perform any necessary preprocessing operations'''
psth_mean_dict = {}
for grab_column in columnInfo.keys():
    column_indices = columnInfo[grab_column]['indices']
    psth_mean_col = []
    psth_baseline_corrected_col = []
    
    for grab_psth_mean in psth_mean_list:
        # Grab raw psth
        raw_psth = grab_psth_mean[column_indices]

        # Create a baseline-corrected version
        baseline = np.mean(raw_psth[..., :psth_lower], axis=-1, keepdims=True)
        baseline_corrected_psth = raw_psth - baseline

        psth_mean_col.append(raw_psth)
        psth_baseline_corrected_col.append(baseline_corrected_psth)

    psth_mean_dict[grab_column] = {
        "raw": np.array(psth_mean_col),
        "baseline_corrected": np.array(psth_baseline_corrected_col)
    }

''' Calculate the average response '''
freq_titles = [f"{round(freq / 1000, 1)} kHz" for freq in array_of_frequencies]

select_column = 0 # 0 counting corresponds to xpos of ['11', '27', '43', '59'] um (microns)
xpos = ['11', '27', '43', '59']

'''Show PSTA LFP response across stim types for select column'''
plt.figure(1)
suptitle = f'Single-column LFP PSTA per stimulus type (x = {xpos[select_column]} um)'
chosen_data = psth_mean_dict[xpos[select_column]]['raw']
jutils.make_4xN_subplots(
    chosen_data, time_lower, time_upper, chosen_data.shape[1], sampleRate, suptitle, titles=freq_titles, amplitude_units = 'μV'
    )

''' Baseline subtracted LFP PSTA per stimulus type in chosen column '''
plt.figure(2)
suptitle = f'Baseline subtracted single-column LFP PSTA per stimulus type (x = {xpos[select_column]} um)'
chosen_data = psth_mean_dict[xpos[select_column]]['baseline_corrected']
jutils.make_4xN_subplots(
    chosen_data, time_lower, time_upper, chosen_data.shape[1], sampleRate, suptitle, titles=freq_titles, amplitude_units = 'μV'
    )

'''Show average LFP response across stim types'''
plt.figure(3)
for grab_psth in psth_mean_dict[xpos[select_column]]['baseline_corrected']:
    plt.plot(np.mean(grab_psth*bitVolts, axis=1))

plt.title(f"Average LFP response across stimulus types for col x = {xpos[select_column]} um")
plt.xlabel("Channels")
plt.ylabel("Amplitude (uV)")
plt.legend(freq_titles, loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()

'''Show variance of LFP response across stim types'''
plt.figure(4)
for grab_psth in psth_mean_dict[xpos[select_column]]['baseline_corrected']:
    plt.plot(np.std(grab_psth*bitVolts, axis=1))

plt.title(f"Std of LFP response across stimulus types for col x = {xpos[select_column]} um")
plt.xlabel("Channels")
plt.ylabel("Amplitude (uV)")
plt.legend(freq_titles, loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()

plt.show()