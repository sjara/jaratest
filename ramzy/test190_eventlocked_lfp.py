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


PROCESSED_DATA_DIR = 'C:\\tmpdata'
# PROCESSED_DATA_DIR = os.path.join(settings.EPHYS_NEUROPIX_PATH,'inpi003_lfp')

# -- Load raw data --
subject = 'poni001'
#ephysSession = '2025-03-10_15-30-45'; behavSession = '20250310a' # Shank 1a, tones
#ephysSession = '2025-03-10_16-17-01'; behavSession = '20250310e' # Shank 1a, AM
# ephysSession = '2025-03-10_15-43-57'; behavSession = '20250310b' # Shank 2a, tones
#ephysSession = '2025-03-10_15-55-03'; behavSession = '20250310c' # Shank 3a, tones
#ephysSession = '2025-03-10_16-06-35'; behavSession = '20250310d' # Shank 4a, tones
# ephysSession = '2025-04-09_12-27-15'; behavSession = '20250409a' # bank 385-480, tones
# ephysSession = '2025-04-09_12-35-59'; behavSession = '20250409b' # bank 385-480, AM
# ephysSession = '2025-04-09_12-43-46'; behavSession = '20250409a' # bank 385-480, naturalSound

# ephysSession = '2025-04-28_15-25-36'; behavSession = '20250428a' # shank1b extref, tones
# ephysSession = '2025-04-28_15-33-55'; behavSession = '20250428b' # shank1b extref, AM
# ephysSession = '2025-04-28_15-42-06'; behavSession = '20250428c' # shank1b, tones
# ephysSession = '2025-04-28_15-50-41'; behavSession = '20250428d' # shank1b, AM
# ephysSession = '2025-04-28_15-58-13'; behavSession = '20250428a' # shank1b, naturalSound

# ephysSession = '2025-06-02_11-09-19'; behavSession = '20250602a' # bank 385-480, soundLocalization
# ephysSession = '2025-06-02_11-41-31'; behavSession = '20250602a' # bank 385-480, tones
# ephysSession = '2025-06-06_15-06-39'; behavSession = '20250606a' # bank 385-480, tones left
# ephysSession = '2025-06-06_15-15-30'; behavSession = '20250606b' # bank 385-480, tones binaural
# ephysSession = '2025-06-06_15-32-30'; behavSession = '20250606c' # bank 385-480, AM left
# ephysSession = '2025-06-06_15-41-24'; behavSession = '20250606d' # bank 385-480, AM binaural
# ephysSession = '2025-06-06_15-49-33'; behavSession = '20250606a' # bank 385-480, nats left
# ephysSession = '2025-06-06_16-16-12'; behavSession = '20250606b' # bank 385-480, nats binaural

# ephysSession = '2025-06-07_14-07-32'; behavSession = '20250607a' # tones, shank1a
# ephysSession = '2025-06-07_14-16-23'; behavSession = '20250607b' # tones, shank2a
# ephysSession = '2025-06-07_14-25-37'; behavSession = '20250607c' # tones, shank3a
# ephysSession = '2025-06-07_14-36-14'; behavSession = '20250607d' # tones, shank4a
# ephysSession = '2025-06-07_14-45-38'; behavSession = '20250607e' # AM, shank1a
# ephysSession = '2025-06-07_14-55-28'; behavSession = '20250607f' # AM, shank2a
# ephysSession = '2025-06-07_15-03-36'; behavSession = '20250607g' # AM, shank3a
# ephysSession = '2025-06-07_15-11-28'; behavSession = '20250607h' # AM, shank4a
# ephysSession = '2025-06-07_15-22-13'; behavSession = '20250607i' # tones, bank 385-480
# ephysSession = '2025-06-07_15-30-29'; behavSession = '20250607j' # AM, bank 385-480
# ephysSession = '2025-06-10_16-07-57'; behavSession = '20250610b' # soundloc, 3-4_1-192
# ephysSession = '2025-06-10_17-20-19'; behavSession = '20250610a' # optoFreq, 3-4_1-192
ephysSession = '2025-06-10_17-39-32'; behavSession = '20250610b' # optoAM,3-4_1-192

dataStream = 'Neuropix-PXI-100.ProbeA'
LASER_SESSSION = True

paradigm = 'am_tuning_curve'
currentStim = 'currentFreq'


# paradigm = 'natural_sound_detection'
# currentStim = 'soundID'

# paradigm = 'sound_localization'
# currentStim = 'soundLocation'

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
stimEachTrial = bdata[currentStim]
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

if LASER_SESSSION:
    laserEachTrial = bdata['laserTrial']
    possibleLaser = np.unique(laserEachTrial)
    nLaser = len(possibleLaser)
    trialsEachCond = behavioranalysis.find_trials_each_combination(stimEachTrial, possibleStim,laserEachTrial,possibleLaser)

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
    avgLFP = np.empty((nStim, nSamplesToExtract, nChannels, nLaser))
    labelsAvgLFP = ['Stimulus', 'Time', 'Channel','Laser']

    for indLaser in range(nLaser):
        for indStim, stimFreq in enumerate(possibleStim):
            avgLFP[indStim, :, :,indLaser] = np.mean(eventlockedLFP[trialsEachCond[:, indStim,indLaser], :, :], axis=0)
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
        for indLaser in range(nLaser):
            for indStim in range(nStim):
                plt.subplot(4, 4*nLaser, indStim+indLaser+1)
                plt.imshow(avgLFP[indStim, :, :,indLaser].T, aspect='auto', origin='lower',
                           extent=[timeVec[0], timeVec[-1], 0, nChannels])
                plt.colorbar()
                plt.title(f'{possibleStim[indStim]} Hz, Laser {possibleLaser[indLaser]}')
            plt.suptitle(f'Average LFP for {subject} {ephysSession}')
            plt.axis('tight')
            plt.show()

    collapsedAvgLFP = [np.mean(avgLFP[:,:,:,indLaser], axis=2) for indLaser in range(nLaser)]  # Average across channels

    if 0:
        # -- Filter avgLFP --
        print('Filtering avgLFP...')
        highcut = 300
        bCoeff, aCoeff = signal.iirfilter(4, Wn=highcut, fs=sampleRate, btype="low", ftype="butter")
        collapsedAvgLFP = [signal.filtfilt(bCoeff, aCoeff, collapsedAvgLFP[indLaser], axis=1) for indLaser in range(nLaser)]

    # -- Plot the average LFP for each stimulus condition --
    if 1:
        print('Plotting responses for all stimuli...')
        plt.clf()
        for indLaser in range(nLaser):
            for indStim in range(nStim):
                plt.subplot(4, 4, indStim+1)
                plt.ylim([-25, 25])
                plt.plot(timeVec, collapsedAvgLFP[indLaser][indStim, :],label=f'Laser_{possibleLaser[indLaser]}')
                plt.title(f'{possibleStim[indStim]}')
        plt.suptitle(f'Average LFP for {subject} {ephysSession} (averaged across trials and channels)')
        plt.axis('tight')
        plt.legend()
        plt.show()



else:
    trialsEachCond = behavioranalysis.find_trials_each_combination(stimEachTrial, possibleStim)

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
    avgLFP = [np.empty((nStim, nSamplesToExtract, nChannels)),np.empty((nStim, nSamplesToExtract, nChannels))]
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
