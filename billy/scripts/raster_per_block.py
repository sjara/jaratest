'''
Show a raster for each condition
and maybe a PSTH?
'''


from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import sys
import importlib
import re

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

outputDir = '/home/billywalker/Pictures/raster_block/'
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
middleFreq = 1 #This is the middle freq in list of possible frequencies
ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

minBlockSize = 40 #This is so that if the last block is small, it wont be plotted


'''
clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
qualityList = [1]
minZVal = 3.0
maxISIviolation = 0.02
'''

behavSession = ''

badSessionList = []#prints bad sessions at end
print "raster_per_block"
for cellID in range(0,numOfCells): 
    oneCell = allcells.cellDB[cellID]
    subject = oneCell.animalName
    try:

        if (behavSession != oneCell.behavSession):

            behavSession = oneCell.behavSession
            ephysSession = oneCell.ephysSession
            ephysRoot = os.path.join(ephysRootDir,subject)

            print behavSession

            # -- Load Behavior Data --
            behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
            bdata = loadbehavior.FlexCategBehaviorData(behaviorFilename)

            # -- Load event data and convert event timestamps to ms --
            ephysDir = os.path.join(ephysRoot, ephysSession)
            eventFilename=os.path.join(ephysDir, 'all_channels.events')
            events = loadopenephys.Events(eventFilename) # Load events data
            eventTimes=np.array(events.timestamps)/SAMPLING_RATE 

            soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

            eventOnsetTimes = eventTimes[soundOnsetEvents]
            soundOnsetTimeBehav = bdata['timeTarget']

            # Find missing trials
            missingTrials = behavioranalysis.find_missing_trials(eventOnsetTimes,soundOnsetTimeBehav)
            # Remove missing trials
            bdata.remove_trials(missingTrials)

            bdata.find_trials_each_block()

            correct = bdata['outcome']==bdata.labels['outcome']['correct']

            possibleFreq = np.unique(bdata['targetFrequency'])
            oneFreq = bdata['targetFrequency'] == possibleFreq[middleFreq]

            correctOneFreq = oneFreq & correct
            trialsEachBlock = bdata.blocks['trialsEachBlock']
            correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
            correctBlockSizes = sum(correctTrialsEachBlock)
            if (correctBlockSizes[-1] < minBlockSize): #Just a check to see if last block is too small to plot
                blockSizes = sum(trialsEachBlock)
                numBlocks = len(trialsEachBlock[0])
                sumBlocks = sum(blockSizes)
                newTrialsLastBlock = np.zeros((blockSizes[-1],numBlocks), dtype=np.bool)
                trialsEachBlock[(sumBlocks-blockSizes[-1]):] = newTrialsLastBlock #if the last block is too small, make the condition for the last trial all false
                correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]

            #trialsEachCond = np.c_[invalid,leftward,rightward]; colorEachCond = ['0.75','g','r']
            #trialsEachCond = np.c_[leftward,rightward]; colorEachCond = ['0.5','0.7','0']
            trialsEachCond = correctTrialsEachBlock;

            if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
                colorEachBlock = 4*['g','r']
            else:
                colorEachBlock = 4*['r','g']

        # -- Load Spike Data From Certain Cluster --
        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)


        plt.clf()
        ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
        plt.setp(ax1.get_xticklabels(), visible=False)
        extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=correctTrialsEachBlock,
                               colorEachCond=colorEachBlock,fillWidth=None,labels=None)
        #plt.yticks([0,trialsEachCond.sum()])
        #ax1.set_xticklabels([])
        plt.ylabel('Trials')

        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

        smoothWinSize = 3
        ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)

        extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=correctTrialsEachBlock,
                             colorEachCond=colorEachBlock,linestyle=None,linewidth=3,downsamplefactor=1)

        plt.xlabel('Time from sound onset (s)')
        plt.ylabel('Firing rate (spk/sec)')

        #plt.show()

        nameFreq = str(possibleFreq[middleFreq])
        tetrodeClusterName = 'T'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)
        plt.gcf().set_size_inches((8.5,11))
        figformat = 'png' #'png' #'pdf' #'svg'
        filename = 'block_%s_%s_%s_%s.%s'%(subject,behavSession,nameFreq,tetrodeClusterName,figformat)
        fulloutputDir = outputDir+subject +'/'
        fullFileName = os.path.join(fulloutputDir,filename)

        directory = os.path.dirname(fulloutputDir)
        if not os.path.exists(directory):
            os.makedirs(directory)
        #print 'saving figure to %s'%fullFileName
        plt.gcf().savefig(fullFileName,format=figformat)


    except:
    #print "error with session "+oneCell.behavSession
        if (oneCell.behavSession not in badSessionList):
            badSessionList.append(oneCell.behavSession)

print 'error with sessions: '
for badSes in badSessionList:
    print badSes
