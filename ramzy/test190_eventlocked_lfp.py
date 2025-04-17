"""
Load LFP data from Neuropixels 2.0 and align it to stim onset.
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
from importlib import reload
reload(loadneuropix)


# PROCESSED_DATA_DIR = 'C:\\tmpdata'
PROCESSED_DATA_DIR = '/mnt/c/tmpdata'

# -- Load raw data --
subject = 'inpi003'
#ephysSession = '2025-03-10_15-30-45'; behavSession = '20250310a' # Shank 1, tones
#ephysSession = '2025-03-10_16-17-01'; behavSession = '20250310e' # Shank 1, AM
# ephysSession = '2025-03-10_15-43-57'; behavSession = '20250310b' # Shank 2, tones
#ephysSession = '2025-03-10_15-55-03'; behavSession = '20250310c' # Shank 3, tones
#ephysSession = '2025-03-10_16-06-35'; behavSession = '20250310d' # Shank 4, tones
# ephysSession = '2025-04-09_12-27-15'; behavSession = '20250409a' # bank 385-480, tones
ephysSession = '2025-04-09_12-35-59'; behavSession = '20250409b' # bank 385-480, AM
# ephysSession = '2025-04-09_12-43-46'; behavSession = '20250409a' # bank 385-480, naturalSound

dataStream = 'Neuropix-PXI-100.ProbeA'

paradigm = 'am_tuning_curve'

# -- Load raw data --
print('Loading raw data...')
rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject, ephysSession)
contData = loadneuropix.Continuous(rawDataPath, dataStream)
rawdata = contData.data
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

if 0:
    # -- Using only a subset of channels --
    channelsToUse = np.arange(0, 48) + 7*48
    rawdata = rawdata[:, channelsToUse]
    nChannels = len(channelsToUse)
if 0:
    # -- Extract a subset of the data --
    nSamplesToProcess = 4 * int(sampleRate)  # 4 sec
    nChannelsToProcess = 2
    traceToProcess = rawdata[:nSamplesToProcess, :nChannelsToProcess] * bitVolts  # In uV 
    tvec = np.arange(nSamplesToProcess) / sampleRate
if 0:
    # Filter traceToProcess with a digital low-pass filter
    highcut = 300
    bCoeff, aCoeff = signal.iirfilter(4, Wn=highcut, fs=sampleRate, btype="low", ftype="butter")
    filteredTraceToProcess = signal.filtfilt(bCoeff, aCoeff, traceToProcess, axis=0)
    sys.exit()
if 0:
    # -- Plot a subset of the data --
    plt.cla()
    plt.plot(tvec, traceToProcess)
    plt.plot(tvec, filteredTraceToProcess)
    plt.xlim([0, 1])
    plt.show()
    

# -- Load events from ephys data --
print('Loading events data...')
events = loadneuropix.RawEvents(rawDataPath, dataStream)
#pdir = '/data/neuropixels/inpi003_raw/2025-03-10_15-30-45/Record Node 101/experiment1/recording1/'
#events = loadneuropix.Events(pdir, dataStream)
eventOnsetTimes = events.get_onset_times()  # In samples
eventOnsetTimes -= events.firstSample  # Convert to 0-based

# DEBUG: testing what's up with sample_numbers.npy
#x = np.load('/data/neuropixels/inpi003_raw/2025-03-10_15-30-45/Record Node 101/experiment1/recording1/continuous/Neuropix-PXI-100.ProbeA/sample_numbers.npy')
#y = np.load('/data/neuropixels/inpi003_raw/2025-03-10_15-30-45/Record Node 101/experiment1/recording1/events/Neuropix-PXI-100.ProbeA/TTL/sample_numbers.npy')
#w = np.load('/data/neuropixels/feat018_raw/2024-06-14_11-20-22/Record Node 101/experiment1/recording1/continuous/Neuropix-PXI-100.1/timestamps.npy')
#z = np.load('/data/neuropixels/feat018_raw/2024-06-14_11-20-22/Record Node 101/experiment1/recording1/continuous/Neuropix-PXI-100.0/timestamps.npy')
if 0:
    print('WARNING: Hardcoded first sample number for inpi003 2025-03-10_15-30-45')
    firstSample = 94422
    eventOnsetTimes = eventOnsetTimes - firstSample

# -- Load behavior data --
print('Loading behavior data...')
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, behavSession)
bdata = loadbehavior.BehaviorData(behavFile)
stimEachTrial = bdata['currentFreq']
nTrials = len(stimEachTrial)
possibleStim = np.unique(stimEachTrial)
nStim = len(possibleStim)

# FIXME: hack for session '20250310c'. Maybe there was a mistake during recording?
#eventOnsetTimes = eventOnsetTimes[1:]  # Remove first timestamp

# If the ephys data is 1 more than the bdata, delete the last ephys trial.
if len(stimEachTrial) == len(eventOnsetTimes)-1:
    eventOnsetTimes = eventOnsetTimes[:len(stimEachTrial)]
assert len(stimEachTrial) == len(eventOnsetTimes), \
    "Number of trials in behavior and ephys do not match"

trialsEachCond = behavioranalysis.find_trials_each_type(stimEachTrial, possibleStim)

# -- Align LFP to event onset --
timeRange = [-0.2, 0.4]
#timeRange = [-2, 2]
sampleRange = [int(timeRange[0]*sampleRate), int(timeRange[1]*sampleRate)]
timeVec = np.arange(sampleRange[0], sampleRange[1])/sampleRate
nSamplesToExtract = sampleRange[1] - sampleRange[0]
eventlockedLFP = np.empty((nTrials, nSamplesToExtract, nChannels), dtype=np.int16)

# -- Calculate event-locked LFP --
print('Calculating eventlockedLFP...')
for indt, evSample in enumerate(eventOnsetTimes):
    eventlockedLFP[indt, :, :] = rawdata[evSample+sampleRange[0]:evSample+sampleRange[1], :]

# -- Calculate average LFP for each stimulus condition --
print('Calculating average LFP for each stimulus...')
avgLFP = np.empty((nStim, nSamplesToExtract, nChannels))
labelsAvgLFP = ['Stimulus', 'Time', 'Channel']
for indstim, stimFreq in enumerate(possibleStim):
    avgLFP[indstim, :, :] = np.mean(eventlockedLFP[trialsEachCond[:, indstim], :, :], axis=0)
avgLFP *= bitVolts  # Convert to uV

# -- Save the average LFP --
if 1:
    scriptFullPath = os.path.realpath(__file__)
    outputFile = os.path.join(PROCESSED_DATA_DIR, f'{subject}_{behavSession}_avgLFP.npz')
    print(f'Saving avgLFP to {outputFile}')
    np.savez(outputFile, avgLFP=avgLFP, timeVec=timeVec, sampleRate=sampleRate,
             nChannels=nChannels,labelsAvgLFP=labelsAvgLFP,
             possibleStim=possibleStim, trialsEachCond=trialsEachCond,
             subject=subject, ephysSession=ephysSession, behavSession=behavSession,
             script=scriptFullPath)

# -- Plot the average LFP for each stimulus condition --
if 0:
    print('Plotting responses for all stimuli...')
    plt.clf()
    for indStim in range(len(possibleStim)):
        plt.subplot(4, 4, indStim+1)
        plt.imshow(avgLFP[indStim, :, :].T, aspect='auto', origin='lower',
                   extent=[timeVec[0], timeVec[-1], 0, nChannels])
        plt.colorbar()
        plt.title(f'{possibleStim[indStim]} Hz')
    plt.suptitle(f'Average LFP for {subject} {ephysSession}')
    plt.axis('tight')
    plt.show()

collapsedAvgLFP = np.mean(avgLFP, axis=2)  # Average across channels
if 0:
    # -- Filter avgLFP --
    print('Filtering avgLFP...')
    highcut = 300
    bCoeff, aCoeff = signal.iirfilter(4, Wn=highcut, fs=sampleRate, btype="low", ftype="butter")
    collapsedAvgLFP = signal.filtfilt(bCoeff, aCoeff, collapsedAvgLFP, axis=1)

# -- Plot the average LFP for each stimulus condition --
if 1:
    print('Plotting responses for all stimuli...')
    plt.clf()
    for indStim in range(len(possibleStim)):
        plt.subplot(4, 4, indStim+1)
        plt.ylim([-25, 25])
        plt.plot(timeVec, collapsedAvgLFP[indStim, :])
        plt.title(f'{possibleStim[indStim]} Hz')
    plt.suptitle(f'Average LFP for {subject} {ephysSession} (averaged across trials and channels)')
    plt.axis('tight')
    plt.show()



    
'''
# -- Save the eventlocked LFP --
if 0:
    print('Saving eventlockedLFP')

    outputFile = '/tmp/eventlockedLFP.npz'
    np.savez(outputFile, eventlockedLFP=eventlockedLFP, timeVec=timeVec,
             sampleRate=sampleRate, nChannels=nChannels)
sys.exit()
'''


