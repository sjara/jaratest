'''
modIndexCalc.py
Finds modulation idex for all cells for psychometric curve task.
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
allcellsFileName = 'allcells_'+mouseName+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds
countTimeRange = [0,0.1] #time range in which to count spikes for modulation index

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1]#range(1,10)
minZVal = 3.0
maxISIviolation = 0.02

minFileName = 'qualityCluster' #name of the file to put the copied files in
################################################################################################
################################################################################################


timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH
outputDir = '/home/billywalker/Pictures/modIndex/'

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered


subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')
ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')


class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


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


ISIFile.close()
maxZFile.close()
minPerfFile.close()
minTrialFile.close()


modIndexArray = []
for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    

    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    ephysRoot = os.path.join(ephysRootDir,subject)
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
    freqList=[]
    for freq in minTrialDict[behavSession]:
        if ((abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal) & (ISIDict[ephysSession][tetrode-1][cluster-1] <= maxISIviolation)):
            freqList.append(int(freq))

    if (len(freqList) < 1):
        continue


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

    possibleFreq = np.unique(bdata['targetFrequency'])
    numberOfFrequencies = len(possibleFreq)
    numberOfTrials = len(bdata['choice'])
    targetFreqs = bdata['targetFrequency']

    '''
    ##############################################################################################################################checks for bad trials
    if (numberOfTrials>sum(soundOnsetEvents)):
        print 'bad trial behavior session: ',behavSession
        behavTimes = np.empty(numberOfTrials)
        prevTimeCenter = bdata['timeCenterIn'][0]
        for trial,timeCenter in enumerate(bdata['timeCenterIn']):
            behavTimes[trial] = timeCenter - prevTimeCenter
            prevTimeCenter = timeCenter

        ephysTimes = np.empty(np.sum(soundOnsetEvents))
        prevTime = eventOnsetTimes[0]
        for etrial,timeSound in enumerate(eventOnsetTimes):
            ephysTimes[etrial] = timeSound - prevTime
            prevTime = timeSound

        numberToPlot = min(numberOfTrials,np.sum(soundOnsetEvents))
        differenceTimes = np.empty(numberToPlot)
        firstSkipped = True
        badTrial = 0
        for dtrial in range(0,numberToPlot):
            differenceTimes[dtrial] = ephysTimes[dtrial]-behavTimes[dtrial]
            if (differenceTimes[dtrial]>0.2) and firstSkipped:
                badTrial = dtrial
                firstSkipped = False

        if badTrial != 0:
            rightward = np.concatenate((rightward[0:badTrial],rightward[(badTrial+1):]),0)
            leftward = np.concatenate((leftward[0:badTrial],leftward[(badTrial+1):]),0)
            targetFreqs = np.concatenate((targetFreqs[0:badTrial],targetFreqs[(badTrial+1):]),0)
            numberOfTrials = numberOfTrials-1
        ###################################################################################################################################
    '''
    for Freq in freqList:

            #Freq = possibleFreq[Frequency]
            oneFreq = targetFreqs == Freq

            trialsToUseRight = rightward & oneFreq
            trialsToUseLeft = leftward & oneFreq

            print 'behavior ',behavSession,' tetrode ',oneCell.tetrode,' cluster ',cluster,'freq',Freq

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

            spikeCountEachTrial = spikeCountMat.flatten()
            spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
            spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))
            if ((spikeAvgRight + spikeAvgLeft) == 0):
                modIndexArray.append(0)
            else:
                modIndexArray.append((spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft))



modIndBinVec = np.arange(-1,1,binWidth)
binModIndexArray = np.empty(len(modIndBinVec))
for binInd in range(len(modIndBinVec)-1):
    binModIndexArray[binInd] = len(np.where((modIndexArray >= modIndBinVec[binInd]) & (modIndexArray < modIndBinVec[binInd+1]))[0])
binModIndexArray[-1] = len(np.where(modIndexArray >= modIndBinVec[-1])[0])

print 'number of cells: ',len(modIndexArray)


plt.clf() 

modIndBinVec
plt.bar(modIndBinVec,binModIndexArray,width = binWidth)

plt.xlabel('Modulation Index')
plt.ylabel('Number of Cells')

plt.gcf().set_size_inches((8.5,11))
figformat = 'png' #'png' #'pdf' #'svg'
filename = 'modIndex_%s.%s'%(subject,figformat)
fulloutputDir = outputDir+subject +'/'
fullFileName = os.path.join(fulloutputDir,filename)

directory = os.path.dirname(fulloutputDir)
if not os.path.exists(directory):
    os.makedirs(directory)
print 'saving figure to %s'%fullFileName
plt.gcf().savefig(fullFileName,format=figformat)

plt.show()

