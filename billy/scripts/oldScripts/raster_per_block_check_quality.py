'''
Show a raster for each condition
and maybe a PSTH?

For test055
20150228a_T3c11 9781 and 7821 Hz  (OK behavior)

For test017
20150301a_T4c3 reversing freq (but bad behavior, not reversing)


TO CHANGE:
- [DONE] Use settings instead of ephysRootDir, ephysRoot
- Don't import loadopenephys, use ephyscore directly
'''


from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import sys
import importlib
import re

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

#reload(spikesanalysis)
#reload(extraplots)

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

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
qualityList = [1]
minZVal = 3.0
maxISIviolation = 0.02

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')
ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')

maxZFile = open(maxZFilename, 'r')
minPerfFile = open(minPerfFilename, 'r')
minTrialFile = open(minTrialFilename, 'r')
ISIFile = open(ISIFilename, 'r')

minPerfFile.readline()
minPerfList=minPerfFile.read().split()


minTrialFile.readline()
minTrialFile.readline()
minTrialDict= {}
for lineCount,line in enumerate(minTrialFile):
    minTrialStr = line.split(':')
    trialFreq = minTrialStr[1].split()
    minTrialDict.update({minTrialStr[0][1:]:trialFreq})


class nestedDict(dict): #This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


maxZFile.readline()
maxZDict = nestedDict()
behavName = ''
for line in maxZFile:
    behavLine = line.split(':')
    freqLine = line.split()
    if (behavLine[0] == 'Behavior Session'):
        behavName = behavLine[1][:-1]
    else:
        maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]


ISIDict = {}
ephysName = ''
for line in ISIFile:
    ephysLine = line.split(':')
    tetrodeLine = line.split()
    tetrodeName = tetrodeLine[0].split(':')
    if (ephysLine[0] == 'Ephys Session'):
        ephysName = ephysLine[1][:-1]
        ISIDict.update({ephysName:np.full((numTetrodes,clusNum),1.0)})
    else:
        ISIDict[ephysName][int(tetrodeName[1])] = tetrodeLine[1:]


maxZFile.close()
minPerfFile.close()
minTrialFile.close()

def main():
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in minPerfList:
            continue
        elif behavSession not in minTrialDict:
            continue
        elif behavSession not in maxZDict:
            continue
        elif ephysSession not in ISIDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freq = minTrialDict[behavSession][0]
        if ((abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal) & (ISIDict[ephysSession][tetrode-1][cluster-1] >= maxISIviolation)):
            rasterBlock(oneCell)




def rasterBlock(oneCell):
    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    ephysRoot = os.path.join(ephysRootDir,subject)

    # -- Load Behavior Data --
    behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
    bdata = loadbehavior.FlexCategBehaviorData(behaviorFilename)
    bdata.find_trials_each_block()

    # -- Load event data and convert event timestamps to ms --
    ephysDir = os.path.join(ephysRoot, ephysSession)
    eventFilename=os.path.join(ephysDir, 'all_channels.events')
    events = loadopenephys.Events(eventFilename) # Load events data
    eventTimes=np.array(events.timestamps)/SAMPLING_RATE 

    soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

    # -- Load Spike Data From Certain Cluster --
    spkData = ephyscore.CellData(oneCell)
    spkTimeStamps = spkData.spikes.timestamps

    eventOnsetTimes = eventTimes[soundOnsetEvents]

    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    
    possibleFreq = np.unique(bdata['targetFrequency'])
    oneFreq = bdata['targetFrequency'] == possibleFreq[middleFreq]

    correctOneFreq = oneFreq & correct
    correctTrialsEachBlock = bdata.blocks['trialsEachBlock'] & correctOneFreq[:,np.newaxis]

    #trialsEachCond = np.c_[invalid,leftward,rightward]; colorEachCond = ['0.75','g','r']
    #trialsEachCond = np.c_[leftward,rightward]; colorEachCond = ['0.5','0.7','0']
    trialsEachCond = correctTrialsEachBlock; 

    if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
        colorEachBlock = 3*['g','r']
    else:
        colorEachBlock = 3*['r','g']


    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

    #plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.')

    plt.clf()
    ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
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
    filename = 'block_%s_%s_%s_%s.%s'%(subject,behavSession,tetrodeClusterName,nameFreq,figformat)
    fulloutputDir = outputDir+subject +'/'
    fullFileName = os.path.join(fulloutputDir,filename)

    directory = os.path.dirname(fulloutputDir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)

main()
