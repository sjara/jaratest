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
from jaratoolbox import extraplots
from importlib import reload
reload(loadneuropix)


RAW_DATA_DIR = os.path.join('/Volumes/CrucialX10','Jaralab','data')
PROCESSED_DATA_DIR = os.path.join('/Volumes/CrucialX10','Jaralab','figures')
# RAW_DATA_DIR = settings.EPHYS_NEUROPIX_PATH
# PROCESSED_DATA_DIR = "C:\\tmpdata"

DEBUG=False
# DEBUG=True
SAVE=True
# -- Load raw data --
subject = 'poni001'
#ephysSession = '2025-03-10_15-30-45'; behavSession = '20250310a' # Shank 1, tones
#ephysSession = '2025-03-10_16-17-01'; behavSession = '20250310e' # Shank 1, AM
# ephysSession = '2025-06-25_15-43-57'; behavSession = '20250310b' # Shank 2, tones
#ephysSession = '2025-03-10_15-55-03'; behavSession = '20250310c' # Shank 3, tones
#ephysSession = '2025-03-10_16-06-35'; behavSession = '20250310d' # Shank 4, tones
# ephysSession = '2025-06-25_16-27-00'; behavSession = '20250625a'
ephysSession = '2025-06-30_14-59-47'; behavSession = '20250630c'
# ephysSession = '2025-07-17_17-20-44'; behavSession = '20250717a'
# ephysSession = '2025-07-17_17-47-55'; behavSession = '20250717b'
# ephysSession = '2025-07-18_15-42-52'; behavSession = '20250718a'
# ephysSession = '2025-07-18_16-17-46'; behavSession = '20250718b'


dataStream = 'Neuropix-PXI-100.ProbeA'


paradigm = 'am_tuning_curve'
# paradigm = 'am_image_tuning'

highpassCutoff = 300  # In HZ
spikeThreshold = -100 #-100  # In uV
refractoryPeriod = 0.001  # In milliseconds
filterOrder = 3
channelToUse = 110 #42  #336

# -- Load raw data --
print('Loading raw data...')
# rawDataPath = os.path.join(settings.EPHYS_NEUROPIX_PATH, subject+'_raw', ephysSession)
rawDataPath = os.path.join(RAW_DATA_DIR,subject, ephysSession)
contData = loadneuropix.Continuous(rawDataPath, dataStream)
rawdata = contData.data
sampleRate = contData.sampleRate
nChannels = contData.nChannels
bitVolts = contData.bitVolts

if 0:
    # -- Test things on a chunk of data from one channel --
    dataSubset = rawdata[:20000,channelToUse]
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
# stimEachTrial = bdata['currentFreq']
stimEachTrial = np.array([f"C{i}R{j}" if i+j>=0 else 'off' for i,j \
                          in zip(bdata['currentStimCol'],bdata['currentStimRow'])])
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
# timeRange = [-0.5,1.0]
timeRange = [-0.2, 0.4]
#timeRange = [-0.1, 0.1]
sampleRange = [int(timeRange[0]*sampleRate), int(timeRange[1]*sampleRate)]
timeVec = np.arange(sampleRange[0], sampleRange[1])/sampleRate
nSamplesToExtract = sampleRange[1] - sampleRange[0]
# eventlockedLFP = np.empty((nTrials, nSamplesToExtract, nChannels), dtype=np.int16)
eventlockedLFP = np.empty((nTrials, nSamplesToExtract), dtype=np.int16)

if not DEBUG:
    binSize = 0.01
    binEdges = np.arange(timeRange[0],timeRange[1]+binSize,binSize)
    nBins = len(binEdges)-1
    spikeTimesFromEventOnsetAll = []
    trialIndexForEachSpikeAll = []
    spikeCountMatAll = []
    sortedSpikeCountsAll = []
    PSTHs = np.zeros((nStim,nChannels,nBins))
    condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
    sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

    # -- Extract spikes for each channel --
    for chan in range(nChannels):
        if not chan%10:
            print(f"Processing channel {chan}/{nChannels}")
        # -- Do things for a single channel --
        rawdataOneChan = rawdata[:, chan]

        # -- Calculate event-locked LFP --
        # print('Calculating eventlockedLFP...')
        for indt, evSample in enumerate(eventOnsetTimes):
            # eventlockedLFP[indt, :, :] = rawdata[evSample+sampleRange[0]:evSample+sampleRange[1], :]
            eventlockedLFP[indt, :] = rawdataOneChan[evSample+sampleRange[0]:evSample+sampleRange[1]]


        # print(eventlockedLFP.shape)
        # -- High-pass filter --
        # print('Filtering eventlocked data...')
        nyquist = 0.5 * sampleRate
        b, a = signal.butter(filterOrder, highpassCutoff / nyquist, btype='high')
        eventlockedFiltered = signal.filtfilt(b, a, eventlockedLFP, axis=1)

        # print(eventlockedFiltered.shape)
        # -- Use data for only one frequency --
        #eventlockedFiltered = eventlockedFiltered[trialsEachCond[:,7]]
        # eventlockedFiltered = eventlockedFiltered[np.any(trialsEachCond[:,7:9], axis=1)]

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
            if len(spikeSamplesRepeated):
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



    # deltaSpikes[cell,:,:] = sortedSpikeCount[cell,:,:] #- np.mean(sortedSpikeCount[cell,:,0:100])

        if 0:
            plt.clf()
            plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
            # plt.plot(spikeTimesFromEventOnset, np.tile(0, len(spikeTimesFromEventOnset)), '.')
            plt.show()


        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)

        sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]
        sortedSpikeCount = spikeCountMat[sortingInds,:]

        spikeTimesFromEventOnsetAll.append(spikeTimesFromEventOnset)
        trialIndexForEachSpikeAll.append(trialIndexForEachSpike)
        spikeCountMatAll.append(spikeCountMat)
        sortedSpikeCountsAll.append(sortedSpikeCount)
        PSTHThisChan = [spikeCountMat[trialsThisCond,:].mean(axis=0) for trialsThisCond in trialsEachCond.T]
        PSTHs[:,chan,:] = PSTHThisChan

    sortedSpikeCountsAll = np.array(sortedSpikeCountsAll)
    spikeCountMatAll = np.array(spikeCountMatAll)

    # -- Load probe map --
    if os.path.exists(rawDataPath):
        xmlfile = os.path.join(rawDataPath, 'Record Node 101', 'settings.xml')

    else:
        print('Please make sure there is a settings.xml file in your neuropixels ephys data directory.')
        exit(1)

    probeMap = loadneuropix.ProbeMap(xmlfile)

    chanOrder = np.argsort(probeMap.channelID)          # conversion between LFP and probeMap

    sortedChannels = sorted(list(np.arange(0,nChannels)),
                        key = lambda x: probeMap.ypos[chanOrder[x]]*(100**probeMap.channelShank[chanOrder[x]]))

    if 1:
        sortedStims = sorted(list(possibleStim),
            key = lambda x: int(x[3])*10 + int(x[1]) if x!='off' else 0)

        plt.clf()
        dims = (16,16)
        plt.figure(figsize=dims)
        chanBins = max(nChannels//nBins,1)
        chanSortedPSTHs = PSTHs[:,sortedChannels,:]
        for indstim,stim in enumerate(sortedStims):
            chanAvgPSTHs = np.array([chanSortedPSTHs[:,i:i+chanBins,:].mean(axis=1) for i in range(0,nChannels,chanBins)])
            plt.subplot(4,4,indstim+1)
            ax = plt.gca()
            # plt.imshow(chanAvgPSTHs[:,indstim,:])
            plt.imshow(chanAvgPSTHs[:,indstim,:],
                vmin = np.percentile(PSTHs[indstim,:,:],1),
                vmax = np.percentile(PSTHs[indstim,:,:],99))
            # plt.imshow(PSTHs[indstim,sortedChannels,:],
            #     vmin = np.percentile(PSTHs[indstim,:,:],10),
            #     vmax=np.percentile(PSTHs[indstim,:,:],90))

            plt.colorbar()
            if indstim//4==3:
                plt.xlabel("time (sec)")
            if indstim%4 == 0:
                plt.ylabel(f"Channel Depth ({r"$\mu$m"})")

            zeroPoint = int(timeRange[0]*nBins/(timeRange[0]-timeRange[1]))


            ax.set_xticks(np.arange(0,len(binEdges),zeroPoint//2)-0.5,np.round(binEdges[::zeroPoint//2],2))
            ax.set_yticks(np.arange(0,nChannels,nChannels//4)//chanBins,probeMap.ypos[chanOrder[sortedChannels][0:nChannels:nChannels//4]])
            plt.axvline(zeroPoint - 0.5,color='r',alpha=0.5)
            plt.title(stim)
        plt.tight_layout()
        plt.suptitle(f"{subject}_{ephysSession}_MUA_PSTHs")

        if SAVE:
            figFilename = f"{subject}_{ephysSession}_MUA_PSTHs"
            figOutDir = os.path.join(PROCESSED_DATA_DIR,"MUA_plots")
            extraplots.save_figure(figFilename,'png',dims,outputDir=figOutDir,facecolor='w')

        plt.show()
        plt.close()


    if 0:
        plt.clf()
        plt.plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.')
        # plt.plot(spikeTimesFromEventOnset, np.tile(0, len(spikeTimesFromEventOnset)), '.')
        plt.axvline(0,color='m')
        plt.show()



### ----- For doing one channel
else:
    # -- Do things for a single channel --

    rawdataOneChan = rawdata[:, channelToUse]

    # -- Calculate event-locked LFP --
    print('Calculating eventlockedLFP...')
    for indt, evSample in enumerate(eventOnsetTimes):
        # eventlockedLFP[indt, :, :] = rawdata[evSample+sampleRange[0]:evSample+sampleRange[1], :]
        eventlockedLFP[indt, :] = rawdataOneChan[evSample+sampleRange[0]:evSample+sampleRange[1]]


    print(eventlockedLFP.shape)
    # -- High-pass filter --
    print('Filtering eventlocked data...')
    nyquist = 0.5 * sampleRate
    b, a = signal.butter(filterOrder, highpassCutoff / nyquist, btype='high')
    eventlockedFiltered = signal.filtfilt(b, a, eventlockedLFP, axis=1)

    print(eventlockedFiltered.shape)
    # -- Use data for only one frequency --
    #eventlockedFiltered = eventlockedFiltered[trialsEachCond[:,7]]
    # eventlockedFiltered = eventlockedFiltered[np.any(trialsEachCond[:,7:9], axis=1)]

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
        if len(spikeSamplesRepeated):
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

    if 0:
        plt.clf()
        plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
        # plt.plot(spikeTimesFromEventOnset, np.tile(0, len(spikeTimesFromEventOnset)), '.')
        plt.show()

    binEdges = np.array([-0.2, -0.1, 0.0, 0.1, 0.2])
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)

    condEachSortedTrial, sortedTrials = np.nonzero(trialsEachCond.T)
    sortingInds = np.argsort(sortedTrials)  # This will be used to sort trialIndexForEachSpike

    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]
if 0:
    plt.clf()
    plt.plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.')
    # plt.plot(spikeTimesFromEventOnset, np.tile(0, len(spikeTimesFromEventOnset)), '.')
    plt.axvline(0,color='m')
    plt.show()
