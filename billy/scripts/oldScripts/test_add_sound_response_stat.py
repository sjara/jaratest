'''
raster and histogram for switching task
Santiago Jaramillo and Billy Walker
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
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)



SAMPLING_RATE=30000.0

outputDir = '/home/billywalker/data/ephys'
nameOfFile = 'maxZVal'
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.3,0.7] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''
tetrodeID = ''

################################################################################################
baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
responseTimeRange = [-0.1,0.1]       #Time range to calculate z value for (should be divisible by binTime
responseTime = responseTimeRange[1]-responseTimeRange[0]
binEdges = np.arange(0,5)*binTime  # Edges of bins to calculate response (in seconds)
################################################################################################


finalOutputDir = outputDir+'/'+subject+'_processed'


class nestedDict(dict):#This is to create maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


maxZDict = nestedDict()
maxZList = [] #List of behavior sessions that already have maxZ values calculated

try:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "r+") #open a text file to read and write in
    text_file.readline()
    behavName = ''
    for line in text_file:
        behavLine = line.split(':')
        freqLine = line.split()
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            maxZList.append(behavName)
            

except:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to read and write in

##############################################################################################
allcellsFileName = 'allcells_'+'test017'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
###############################################################################################
for cellID in range(0,1):#numOfCells):
    cellNUM=allcells.cellDB.findcell('test017','20150303a',2,9)
    oneCell = allcells.cellDB[cellNUM]
    #oneCell = allcells.cellDB[cellID]
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    if (behavSession != oneCell.behavSession):

        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        ephysRoot = os.path.join(ephysRootDir,subject)

        print oneCell.behavSession

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

        possibleFreq = np.unique(bdata['targetFrequency'])
        numberOfFrequencies = len(possibleFreq)
        for possFreq in possibleFreq:
            maxZDict[behavSession][possFreq] = np.empty([clusNum*numTetrodes])
        #maxZArray = np.empty([clusNum*numTetrodes])

        
    # -- Load Spike Data From Certain Cluster --
    for Frequency in range(1):
        Freq = possibleFreq[1]
        oneFreqTrials = bdata['targetFrequency'] == Freq    

        oneFreqEventOnsetTimes = eventOnsetTimes[oneFreqTrials] #Choose only the trials with this frequency


        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps
        #print oneFreqEventOnsetTimes
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spkTimeStamps,oneFreqEventOnsetTimes,timeRange)

        [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange
        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        #maxZArray[clusterNumber].append(maxZ)
        maxZDict[behavSession][Freq][clusterNumber] = maxZ
 
'''
bSessionList = []
for bSession in maxZDict:
    bSessionList.append(bSession)

bSessionList.sort()
for bSession in bSessionList:
    text_file.write("\nBehavior Session:%s" % bSession)
    for freq in maxZDict[bSession]:
        text_file.write("\n%s " % freq)
        for ZVal in maxZDict[bSession][freq]:
            text_file.write("%s," % ZVal)
'''
text_file.close()
print 'finished max Z value check'
