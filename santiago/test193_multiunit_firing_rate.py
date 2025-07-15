"""
Show plot of multiunit firing rate from Neuropixels data
"""

import sys
import os
import json
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from jaratoolbox import loadneuropix
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from importlib import reload
reload(loadneuropix)


PROCESSED_DATA_DIR = '/var/tmp/'

# -- Load raw data --
subject = 'inpi003'
#ephysSession = '2025-03-10_15-30-45'; behavSession = '20250310a' # Shank 1, tones
#ephysSession = '2025-03-10_16-17-01'; behavSession = '20250310e' # Shank 1, AM
ephysSession = '2025-03-10_15-43-57'; behavSession = '20250310b' # Shank 2, tones
#ephysSession = '2025-03-10_15-55-03'; behavSession = '20250310c' # Shank 3, tones
#ephysSession = '2025-03-10_16-06-35'; behavSession = '20250310d' # Shank 4, tones

dataStream = 'Neuropix-PXI-100.ProbeA'

paradigm = 'am_tuning_curve'

highpassCutoff = 300  # In HZ
spikeThreshold = -100 #-100  # In uV
refractoryPeriod = 0.002  # In milliseconds
filterOrder = 3

# -- Load raw data --
print('Loading raw data...')
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', ephysSession)
contData = loadneuropix.Continuous(rawDataPath, dataStream)
rawdata = contData.data
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

if 0:
    # -- Test things on a chunk of data from one channel --
    dataSubset = rawdata[:20000,100]
    #dataSubset = rawdata[:,100]

    # -- High-pass filter --
    nyquist = 0.5 * sampleRate
    b, a = signal.butter(filterOrder, highpassCutoff / nyquist, btype='high')
    dataFiltered = signal.filtfilt(b, a, dataSubset, axis=-1)

    spikeTimesRepeated = np.flatnonzero(dataFiltered < spikeThreshold)
    refractoryPeriodSamples = int(sampleRate * refractoryPeriod)
    isi = np.diff(spikeTimesRepeated)
    keep = np.insert(isi > refractoryPeriodSamples, 0, True)
    spikeTimes = spikeTimesRepeated[keep]

    #sys.exit()

    # -- Plot --
    plt.clf()
    plt.plot(dataSubset, alpha=0.1)
    plt.plot(dataFiltered)
    plt.axhline(spikeThreshold)
    plt.plot(spikeTimes, np.tile(2*spikeThreshold, len(spikeTimes)), 'o')
    plt.show()
    
# -- Load events from ephys data --
print('Loading events data...')
events = loadneuropix.RawEvents(rawDataPath, dataStream)
eventOnsetTimes = events.get_onset_times()  # In samples
eventOnsetTimes -= events.firstSample  # Convert to 0-based

# -- Load behavior data --
print('Loading behavior data...')
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, behavSession)
bdata = loadbehavior.BehaviorData(behavFile)
stimEachTrial = bdata['currentFreq']
nTrials = len(stimEachTrial)
possibleStim = np.unique(stimEachTrial)
nStim = len(possibleStim)

# If the ephys data is 1 more than the bdata, delete the last ephys trial.
if len(stimEachTrial) == len(eventOnsetTimes)-1:
    eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
assert len(stimEachTrial) == len(eventOnsetTimes), \
    "Number of trials in behavior and ephys do not match"

trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

# -- Align LFP to event onset --
timeRange = [-0.2, 0.2]
#timeRange = [-0.1, 0.1]
sampleRange = [int(timeRange[0]*sampleRate), int(timeRange[1]*sampleRate)]
timeVec = np.arange(sampleRange[0], sampleRange[1])/sampleRate
nSamplesToExtract = sampleRange[1] - sampleRange[0]
#eventlockedLFP = np.empty((nTrials, nSamplesToExtract, nChannels), dtype=np.int16)
eventlockedLFP = np.empty((nTrials, nSamplesToExtract), dtype=np.int16)

# -- Do things for a single channel --
channelToUse = 42  #336
rawdataOneChan = rawdata[:, channelToUse]

# -- Calculate event-locked LFP --
print('Calculating eventlockedLFP...')
for indt, evSample in enumerate(eventOnsetTimes):
    #eventlockedLFP[indt, :, :] = rawdata[evSample+sampleRange[0]:evSample+sampleRange[1], :]
    eventlockedLFP[indt, :] = rawdataOneChan[evSample+sampleRange[0]:evSample+sampleRange[1]]

    
# -- High-pass filter --
print('Filtering eventlocked data...')
nyquist = 0.5 * sampleRate
b, a = signal.butter(filterOrder, highpassCutoff / nyquist, btype='high')
eventlockedFiltered = signal.filtfilt(b, a, eventlockedLFP, axis=-1)

# -- Use data for only one frequency --
#eventlockedFiltered = eventlockedFiltered[trialsEachCond[:,7]]
eventlockedFiltered = eventlockedFiltered[np.any(trialsEachCond[:,7:9], axis=1)]

if 0:
    plt.clf()
    plt.imshow(eventlockedFiltered < spikeThreshold)
    plt.show()

#sys.exit()

# -- Extract spikes from each trial --
spikeSamples = []
trialIndex = []
indexLimits = []
nSpikesSoFar = 0
for indt, dataOneTrial in enumerate(eventlockedFiltered):
    spikeSamplesRepeated = np.flatnonzero(dataOneTrial < spikeThreshold)
    refractoryPeriodSamples = int(sampleRate * refractoryPeriod)
    isi = np.diff(spikeSamplesRepeated, axis=-1)
    keep = np.insert(isi > refractoryPeriodSamples, 0, True)
    spikeSamplesToKeep = spikeSamplesRepeated[keep]
    spikeSamples.append(spikeSamplesToKeep)
    indexLimits.append([nSpikesSoFar, nSpikesSoFar+len(spikeSamplesToKeep)])
    nSpikesSoFar += len(spikeSamplesToKeep)

spikeTimesFromEventOnset = timeVec[np.concatenate(spikeSamples)]
trialIndexForEachSpike = np.concatenate([[indr]*len(row) for indr, row in enumerate(spikeSamples)])
indexLimitsEachTrial = np.array(indexLimits).T

if 1:
    plt.clf()
    #plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
    plt.plot(spikeTimesFromEventOnset, np.tile(0, len(spikeTimesFromEventOnset)), '.')
    plt.show()

binEdges = np.array([-0.2, -0.1, 0.0, 0.1, 0.2])
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
