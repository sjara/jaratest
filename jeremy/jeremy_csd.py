'''
[Work in progress]
This is where the aggregated CSD creation .py script will go.
'''

'''
Load in neurpixels LFP data.
'''

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadneuropix
from jaratoolbox import settings
from importlib import reload
reload(loadneuropix)

subject = 'feat018'
session = '2024-06-14_11-20-22'
dataStream = 'Neuropix-PXI-100.1'

rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', session)

info = loadneuropix.read_oebin(rawDataPath, dataStream)
contData = loadneuropix.Continuous(rawDataPath, dataStream)
rawdata = contData.data # Data x Acquisition channels (384 channels in total)
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

## Display a heatmap of a subset of LFP data
plt.figure(figsize=(15,20))
plt.imshow(contData.data[:1000,:].T)
plt.title("Heatmap of the LFP data across all acquisition channels from n=0 to n=1000 | yellow = high, purple = low")
plt.show()

nSamplesToProcess = 1 * sampleRate  # 4 sec
traceToProcess = rawdata[:nSamplesToProcess, :20] * bitVolts  # In uV 
tvec = np.arange(nSamplesToProcess) / sampleRate

events = loadneuropix.RawEvents(rawDataPath, dataStream)
eventOnsetTimes = events.get_onset_times() # Stimulus onset times ... 331 in total

'''
Load in behavior data corresponding to the LFP data.
'''

from jaratoolbox import loadbehavior, behavioranalysis

subject = 'feat018'
paradigm = 'am_tuning_curve'
session = '20240614a'
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

'''
Create uncollapsed PSTH given 
'''

import jeremy_psth as jpsth
import jeremy_utils as jutils
reload(jpsth)
reload(jutils)

eventOnsetTimes = jpsth.fix_stimuli_number_mismatch(bdata, 'currentFreq', eventOnsetTimes)

frequencies_each_trial = bdata['currentFreq']
array_of_frequencies = np.unique(bdata['currentFreq'])
trialsEachCond = behavioranalysis.find_trials_each_type(frequencies_each_trial, array_of_frequencies)

psth_upper = 1000 # Ex: Collect 100 datapoints BEYOND stimulus onset
psth_lower = 100 # Ex: Collect 100 datapoints BEFORE stimulus onset

## Choose via binary operation whichever trials are of interest.
trials = trialsEachCond[:,6] + trialsEachCond[:,7] + trialsEachCond[:,8]

psth_uncollapsed, collection_outcome_list = jpsth.get_psth_uncollapsed(contData.data, contData.timestamps, eventOnsetTimes, trials, psth_upper, psth_lower)

plt.figure(figsize=(15,20))
plt.imshow(psth_uncollapsed.mean(axis=0).T)
plt.axvline(x=psth_lower, c='r')
plt.title("Heatmap of average LFP data for a given stimuli. | yellow = high, purple = low, red line = stimulus onset.")
plt.xlabel("Time evolution (left to right)")
plt.ylabel("Unorded channels")
plt.show()

'''
Estimate CSD
'''

from elephant.current_source_density import estimate_csd
from neo import AnalogSignal
import quantities as pq

coords = [(elem,) for elem in range(psth_uncollapsed[:,:,:].shape[-1])]
neo_lfp_personal = AnalogSignal(psth_uncollapsed[:,:,:].mean(axis=0)*bitVolts, units="uV", sampling_rate = sampleRate*pq.Hz)
neo_lfp_personal.annotate(coordinates = coords * pq.mm)

csd_not_np = estimate_csd(neo_lfp_personal, method="KCSD1D")
csd = np.array(csd_not_np)

plt.figure(figsize=(15,20))
plt.imshow(csd.T)
plt.axvline(x=psth_lower, c='r')
plt.title("Heatmap of estimated CSD for a given stimuli. | yellow = high, purple = low, red line = stimulus onset.")
plt.xlabel("Time evolution.")
plt.ylabel("Unorded channels.")
plt.show()