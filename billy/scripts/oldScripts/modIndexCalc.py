'''
modIndexCalc.py
Finds modulation idex for all cells for switching task.
'''

import allcells_MI_test017 as allcells
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds
Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
countTimeRange = [0,0.1] #time range in which to count spikes for modulation index

timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered


modIndexArray = np.empty(numOfCells)
for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]


    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    ephysRoot = os.path.join(ephysRootDir,subject)

    # -- Load Behavior Data --
    behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
    bdata = loadbehavior.BehaviorData(behaviorFilename)

    # -- Load event data and convert event timestamps to ms --
    ephysDir = os.path.join(ephysRoot, ephysSession)
    eventFilename=os.path.join(ephysDir, 'all_channels.events')
    events = loadopenephys.Events(eventFilename) # Load events data
    eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

    soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

    # -- Load Spike Data From Certain Cluster --
    spkData = ephyscore.CellData(oneCell)
    spkTimeStamps = spkData.spikes.timestamps

    eventOnsetTimes = eventTimes[soundOnsetEvents]

    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])
    oneFreq = bdata['targetFrequency'] == possibleFreq[Frequency]

    trialsToUseRight = correctRightward & oneFreq
    trialsToUseLeft = correctLeftward & oneFreq


    trialsEachCond = np.c_[invalid,trialsToUseRight,trialsToUseLeft]; colorEachCond = ['0.75','g','r']


    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

    spikeCountEachTrial = spikeCountMat.flatten()
    spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
    spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))
    if ((spikeAvgRight + spikeAvgLeft) == 0):
        modIndexArray[cellID] = 0
    else:
        modIndexArray[cellID] = (spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft)
    


modIndBinVec = np.arange(-1,1,binWidth)
binModIndexArray = np.empty(len(modIndBinVec))
for binInd in range(len(modIndBinVec)-1):
    binModIndexArray[binInd] = len(np.where((modIndexArray >= modIndBinVec[binInd]) & (modIndexArray < modIndBinVec[binInd+1]))[0])
binModIndexArray[-1] = len(np.where(modIndexArray >= modIndBinVec[-1])[0])


plt.clf() 

modIndBinVec
plt.bar(modIndBinVec,binModIndexArray,width = binWidth)

plt.xlabel('Time from sound onset (s)')
plt.ylabel('Firing rate (spk/sec)')

plt.show()

