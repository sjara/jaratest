'''
modIndexCalc.py
Finds modulation idex for all cells for psychometric curve task.
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

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
#binWidth = 0.010 # Size of each bin in histogram in seconds
countTimeRange = [0,0.1] #time range in which to count spikes for modulation index
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
stimulusRange = [0.0,0.1] # The time range that the stimulus is being played

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

ephysRootDir = settings.EPHYS_PATH
outputDir = ephysRootDir#'/home/billywalker/data/ephys/'

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered


subject = allcells.cellDB[0].animalName
behavSession = ''
#processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')

nameOfFile = 'modIndex'
finalOutputDir = outputDir+subject+'_processed'


class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value

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
maxMI = 0.0
modIDict = nestedDict() #stores all the modulation indices
modSigDict = nestedDict() #stores the significance of the modulation of each cell


print 'modulation check'
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
            behaviorFilename = loadbehavior.path_to_behavior_data(subject=subject,paradigm=paradigm,sessionstr=behavSession)
            bdata = loadbehavior.BehaviorData(behaviorFilename)

            # -- Load event data and convert event timestamps to ms --
            ephysDir = os.path.join(ephysRoot, ephysSession)
            eventFilename=os.path.join(ephysDir, 'all_channels.events')
            events = loadopenephys.Events(eventFilename) # Load events data
            eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

            soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

            eventOnsetTimes = eventTimes[soundOnsetEvents]
            soundOnsetTimeBehav = bdata['timeTarget']

            # Find missing trials
            missingTrials = behavioranalysis.find_missing_trials(eventOnsetTimes,soundOnsetTimeBehav)
            # Remove missing trials
            bdata.remove_trials(missingTrials)

            rightward = bdata['choice']==bdata.labels['choice']['right']
            leftward = bdata['choice']==bdata.labels['choice']['left']

            possibleFreq = np.unique(bdata['targetFrequency'])
            numberOfFrequencies = len(possibleFreq)
            numberOfTrials = len(bdata['choice'])
            targetFreqs = bdata['targetFrequency']

            for possFreq in possibleFreq:
                modIDict[behavSession][str(possFreq)] = np.empty([clusNum*numTetrodes])
                modSigDict[behavSession][str(possFreq)] = np.empty([clusNum*numTetrodes])

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



        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterNumber = (tetrode-1)*clusNum+(cluster-1)

        # -- Load Spike Data From Certain Cluster --
        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)
        spikeCountEachTrial = spikeCountMat.flatten()

        for Freq in possibleFreq:

                oneFreq = targetFreqs == Freq

                trialsToUseRight = rightward & oneFreq
                trialsToUseLeft = leftward & oneFreq
                trialsEachCond = [trialsToUseRight,trialsToUseLeft]

                if ((sum(trialsToUseRight)==0) or (sum(trialsToUseLeft)==0)): #If there are no trials on one side
                    modIDict[behavSession][str(Freq)][clusterNumber] = 0.0
                    modSigDict[behavSession][str(Freq)][clusterNumber] = 1.0
                    continue
                spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
                spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))
                if ((spikeAvgRight + spikeAvgLeft) == 0):
                    modIDict[behavSession][str(Freq)][clusterNumber] = 0
                    modSigDict[behavSession][str(Freq)][clusterNumber] = 1.0
                else:
                    mod_sig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,stimulusRange,trialsEachCond)
                    modIDict[behavSession][str(Freq)][clusterNumber] =((spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft))
                    modSigDict[behavSession][str(Freq)][clusterNumber] = mod_sig[1]


    except:
        if (oneCell.behavSession not in badSessionList):
            badSessionList.append(oneCell.behavSession)


'''
modIndBinVec = np.arange(-1,1,binWidth)
binModIndexArray = np.empty(len(modIndBinVec))
for binInd in range(len(modIndBinVec)-1):
    binModIndexArray[binInd] = len(np.where((modIndexArray >= modIndBinVec[binInd]) & (modIndexArray < modIndBinVec[binInd+1]))[0])
binModIndexArray[-1] = len(np.where(modIndexArray >= modIndBinVec[-1])[0])

print 'number of cells: ',len(modIndexArray)
'''
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

    #modI_file.write("modI:\n")
    for Freq in modIDict[bSession]:
        modI_file.write("modI:%s:" % Freq)
        for modIInd in modIDict[bSession][Freq]:
            modI_file.write("%s," % modIInd)
        modI_file.write("\n")

    #modI_file.write("modSig:\n")
    for Freq in modSigDict[bSession]:
        modI_file.write("modSig:%s:" % Freq)
        for modSigInd in modSigDict[bSession][Freq]:
            modI_file.write("%s," % modSigInd)
        modI_file.write("\n")

modI_file.close()

#########################################################################################


print 'error with sessions: '
for badSes in badSessionList:
    print badSes
print 'finished modI value check'

'''
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
'''
