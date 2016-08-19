'''
modIndexCalcSwitching_AllMice.py
Finds modulation index for all cells for all mice in switching task.
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

mouseList = ['test089','test059','test017']

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.020 # Size of each bin in histogram in seconds
Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
countTimeRange = [0,0.1] #time range in which to count spikes for modulation index

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]#range(1,10)
minZVal = 3.0
maxISIviolation = 0.02

minFileName = 'qualityCluster' #name of the file to put the copied files in
minPValue = 0.05
################################################################################################
################################################################################################

stimulusRange = [0.0,0.1] # The time range that the stimulus is being played
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH
outputDir = '/home/billywalker/Pictures/modIndex/'

experimenter = 'santiago'
paradigm = '2afc'
'''
totalCellDB = []
#Load up all cells from all animals
for mouseName in mouseList:
    allcellsFileName = 'allcells_'+mouseName+'_quality'
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)
    totalCellDB.append(allcells.cellDB)
'''



class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


modIndexArray = []
maxMI = 0.0
for mouseName in mouseList:
    allcellsFileName = 'allcells_'+mouseName+'_quality'
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)


    numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

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
        midFreq = minTrialDict[behavSession][0]
        if ((abs(float(maxZDict[behavSession][midFreq][clusterNumber])) < minZVal) | (ISIDict[ephysSession][tetrode-1][cluster-1] > maxISIviolation)):
            continue

        print 'subject ',subject,' behavior ',behavSession,' tetrode ',oneCell.tetrode,' cluster ',cluster

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


        trialsEachCond = [trialsToUseRight,trialsToUseLeft]


        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

        spikeCountEachTrial = spikeCountMat.flatten()
        spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
        spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))

        if ((spikeAvgRight + spikeAvgLeft) == 0):
            modIndexArray.append((0.0,1.0))
        else:
            mod_sig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,stimulusRange,trialsEachCond)
            currentMI = (spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft)
            modIndexArray.append((currentMI,mod_sig[1]))
            maxMI = max(maxMI,abs(currentMI))


modIndBinVec = np.arange(-1,1,binWidth)
binModIndexArraySig = np.empty(len(modIndBinVec))
binModIndexArrayNonSig = np.empty(len(modIndBinVec))
for binInd in range(len(modIndBinVec)-1):
    binTotalSig = 0
    binTotalNonSig = 0
    for modIndSig in modIndexArray:
        if ((modIndSig[0] >= modIndBinVec[binInd]) & (modIndSig[0] < modIndBinVec[binInd+1]) & (modIndSig[1] <= minPValue)):
            binTotalSig += 1
        elif ((modIndSig[0] >= modIndBinVec[binInd]) & (modIndSig[0] < modIndBinVec[binInd+1])):
            binTotalNonSig += 1
    binModIndexArraySig[binInd] = binTotalSig
    binModIndexArrayNonSig[binInd] = binTotalNonSig
binModIndexArraySig[-1] = 0# len(np.where(modIndexArray[:,0] >= modIndBinVec[-1])[0])
binModIndexArrayNonSig[-1] = 0

print 'number of cells: ',len(modIndexArray)


plt.clf() 

plt.bar(modIndBinVec,binModIndexArraySig,width = binWidth, color = 'b')
plt.bar(modIndBinVec,binModIndexArrayNonSig,width = binWidth, color = 'g',bottom = binModIndexArraySig)
#plt.spines['left'].set_position('center')

plt.xlim((-(maxMI+binWidth),maxMI+binWidth))

plt.xlabel('Modulation Index')
plt.ylabel('Number of Cells')

plt.gcf().set_size_inches((8.5,11))
figformat = 'png' #'png' #'pdf' #'svg'
filename = 'modIndex_%s.%s'%('allmice_switching',figformat)
fulloutputDir = outputDir+'allmice'+'/'
fullFileName = os.path.join(fulloutputDir,filename)

directory = os.path.dirname(fulloutputDir)
if not os.path.exists(directory):
    os.makedirs(directory)
print 'saving figure to %s'%fullFileName
plt.gcf().savefig(fullFileName,format=figformat)


plt.show()

