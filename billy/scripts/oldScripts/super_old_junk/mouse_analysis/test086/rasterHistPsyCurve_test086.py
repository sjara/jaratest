'''
raster and histogram for switching task
Santiago Jaramillo and Billy Walker
'''

import allcells_test086 as allcells
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

outputDir = '/home/billywalker/Pictures/raster_hist/'
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
subject = ''
behavSession = ''
ephysSession = ''
tetrodeID = ''


for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    if (behavSession != oneCell.behavSession):


        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        ephysRoot = os.path.join(ephysRootDir,subject)

        # -- Load Behavior Data --
        behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
        bdata = loadbehavior.BehaviorData(behaviorFilename)
        numberOfTrials = len(bdata['choice'])

        # -- Load event data and convert event timestamps to ms --
        ephysDir = os.path.join(ephysRoot, ephysSession)
        eventFilename=os.path.join(ephysDir, 'all_channels.events')
        events = loadopenephys.Events(eventFilename) # Load events data
        eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

        soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)


        eventOnsetTimes = eventTimes[soundOnsetEvents]

        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left']
        invalid = bdata['outcome']==bdata.labels['outcome']['invalid']

        possibleFreq = np.unique(bdata['targetFrequency'])
        numberOfFrequencies = len(possibleFreq)



    # -- Load Spike Data From Certain Cluster --
    spkData = ephyscore.CellData(oneCell)
    spkTimeStamps = spkData.spikes.timestamps

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

    for Frequency in range(numberOfFrequencies):

        Freq = possibleFreq[Frequency]
        oneFreq = bdata['targetFrequency'] == Freq

        trialsToUseRight = rightward & oneFreq
        trialsToUseLeft = leftward & oneFreq

        trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight]; colorEachCond = ['g','r']

        plt.clf()
        ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
        extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)

        plt.ylabel('Trials')

        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

        smoothWinSize = 3
        ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)

        extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                             colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

        plt.xlabel('Time from sound onset (s)')
        plt.ylabel('Firing rate (spk/sec)')
        
        if ((Frequency == numberOfFrequencies/2) or (Frequency == (numberOfFrequencies/2 - 1))):
                freqFile = 'Center_Frequencies'
        else:
                freqFile = 'Outside_Frequencies'
        tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
        plt.gcf().set_size_inches((8.5,11))
        figformat = 'png' #'png' #'pdf' #'svg'
        filename = 'rast_%s_%s_%s_%s.%s'%(subject,behavSession,Freq,tetrodeClusterName,figformat)
        fulloutputDir = outputDir+subject+'/'+ freqFile +'/'
        fullFileName = os.path.join(fulloutputDir,filename)

        directory = os.path.dirname(fulloutputDir)
        if not os.path.exists(directory):
            os.makedirs(directory)
        print 'saving figure to %s'%fullFileName
        plt.gcf().savefig(fullFileName,format=figformat)


