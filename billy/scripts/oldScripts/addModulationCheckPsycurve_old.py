'''
modIndexCalcSwitching.py
Finds modulation index for all cells for switching task.
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

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.020 # Size of each bin in histogram in seconds
Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
countTimeRange = [0,0.1] #time range in which to count spikes for modulation index

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes


stimulusRange = [0.0,0.1] # The time range that the stimulus is being played
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH
outputDir = '/home/billywalker/data/ephys'

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')

nameOfFile = 'modIndex'
finalOutputDir = outputDir+'/'+subject+'_processed'


###############FOR USING MODIDICT WITH ALL FREQS############################################
class nestedDict(dict):#This is to create maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value
#############################################################################################


modIList = []#List of behavior sessions that already have modI values calculated
try:
    modI_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "r+") #open a text file to read and write in
    behavName = ''
    for line in modI_file:
        behavLine = line.split(':')
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            modIList.append(behavName)
    
            

except:
    modI_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to read and write in


badSessionList = []#Makes sure sessions that crash don't get modI values printed
behavSession = ''
modIndexArray = []
modIDict = nestedDict() #stores all the modulation indices

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]

    if (oneCell.behavSession in modIList): #checks to make sure the modI value is not recalculated
        continue
    try:
        if (behavSession != oneCell.behavSession):

            subject = oneCell.animalName
            behavSession = oneCell.behavSession
            ephysSession = oneCell.ephysSession
            ephysRoot = os.path.join(ephysRootDir,subject)

            print behavSession

            # -- Load Behavior Data --
            behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
            bdata = loadbehavior.BehaviorData(behaviorFilename)

            # -- Load event data and convert event timestamps to ms --
            ephysDir = os.path.join(ephysRoot, ephysSession)
            eventFilename=os.path.join(ephysDir, 'all_channels.events')
            events = loadopenephys.Events(eventFilename) # Load events data
            eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

            soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

            eventOnsetTimes = eventTimes[soundOnsetEvents]

            rightward = bdata['choice']==bdata.labels['choice']['right']
            leftward = bdata['choice']==bdata.labels['choice']['left']
            valid = (bdata['outcome']==bdata.labels['outcome']['correct'])|(bdata['outcome']==bdata.labels['outcome']['error'])
            correct = bdata['outcome']==bdata.labels['outcome']['correct']
            correctRightward = rightward & correct
            correctLeftward = leftward & correct

            possibleFreq = np.unique(bdata['targetFrequency'])
            numberOfFrequencies = len(possibleFreq)
            numberOfTrials = len(bdata['choice'])
            targetFreqs = bdata['targetFrequency']

            for possFreq in possibleFreq:
                modIDict[behavSession][possFreq] = np.empty([clusNum*numTetrodes])

        # -- Load Spike Data From Certain Cluster --
        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps


        clusterNumber = (oneCell.tetrode-1)*clusNum+(oneCell.cluster-1)
        for Freq in possibleFreq:
            oneFreq = targetFreqs == Freq

            trialsToUseRight = rightward & oneFreq
            trialsToUseLeft = leftward & oneFreq

            #print 'behavior ',behavSession,' tetrode ',oneCell.tetrode,' cluster ',oneCell.cluster,'freq',Freq

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

            spikeCountEachTrial = spikeCountMat.flatten()
            spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
            spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))


            if ((spikeAvgRight + spikeAvgLeft) == 0):
                modIDict[behavSession][Freq][clusterNumber]=0.0
            else:
                modIDict[behavSession][Freq][clusterNumber]=((spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft))
            #print spikeAvgRight,' ', spikeAvgLeft, ' ',modIDict[behavSession][Freq][clusterNumber]

    except:
        if (oneCell.behavSession not in badSessionList):
            badSessionList.append(oneCell.behavSession)

#########################################################################################
#This is the save all the values in a text file
#########################################################################################
bSessionList = []
for bSession in modIDict:
    if (bSession not in badSessionList):
        bSessionList.append(bSession)

bSessionList.sort()
for bSession in bSessionList:
    modI_file.write("Behavior Session:%s\n" % bSession)

    for freq in modIDict[bSession]:
        modI_file.write("%s:" % str(freq))
        for modIInd in modIDict[bSession][freq]:
            modI_file.write("%s," % modIInd)
        modI_file.write("\n")


modI_file.close()

#########################################################################################

print 'error with sessions: '
for badSes in badSessionList:
    print badSes
print 'finished modI value check'


