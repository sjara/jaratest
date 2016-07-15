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
#binWidth = 0.020 # Size of each bin in histogram in seconds
Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
countTimeRange = [-0.1,0.0] #time range in which to count spikes for modulation index######################

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes


stimulusRange = [-0.1,0.0] # The time range that the mouse is moving after the sound is presented#################
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)#####################################################################################

ephysRootDir = settings.EPHYS_PATH
outputDir = '/home/billywalker/data/ephys'

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

subject = allcells.cellDB[0].animalName
behavSession = ''
#processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')######################################3

nameOfFile = 'modIndex_beforeSound'
finalOutputDir = outputDir+'/'+subject+'_processed'

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
modIDict = {} #stores all the modulation indices
modSigDict = {} #stores the significance of the modulation of each cell
modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
numBlocksDict = {} # stores the number of blocks in the session (not including the last block if its too small

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

            modIDict[behavSession] = np.zeros((clusNum*numTetrodes),dtype = float)
            modSigDict[behavSession] = np.ones((clusNum*numTetrodes),dtype = float)
            modDirectionScoreDict[behavSession] = np.zeros((clusNum*numTetrodes),dtype = float)

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
            oneFreq = bdata['targetFrequency'] == possibleFreq[Frequency]

            ###################################################################################################
            ###################################################################################################
            #This skips first trials of either frequency (middle or other) in each block. Can easily change to skip first trials of middle freq. Include middle freq oneFreq[trialNum] in elif.
            firstTrialsExclude = 20 # how many trials to exclude at the beginning of each block from modulation index
            highBlock = bdata['currentBlock']==bdata.labels['currentBlock']['high_boundary']

            numTrials = len(highBlock)
            currentBlock = highBlock[0]
            firstTrialNum = 0
            trialsToInclude = np.zeros((numTrials), dtype = bool)
            blockNumber = np.zeros((numTrials))
            curBlockNum = 0
            totalBlocks = 1
            for trialNum,block in enumerate(highBlock):
                if (block != currentBlock): #check if there is a new block
                    firstTrialNum = 0
                    currentBlock = block
                    curBlockNum += 1
                    totalBlocks +=1
                blockNumber[trialNum]=curBlockNum
                if (valid[trialNum] & (firstTrialNum >= firstTrialsExclude)): #check if the trial is correct and past excluding trials
                    trialsToInclude[trialNum] = True
                elif (valid[trialNum]): #skip this trial 
                    firstTrialNum += 1


            #This will check how big the last block is
            minLastBlockSize = 50 #This includes the first blocks that will be skipped
            lastBlock = highBlock[-1]
            lastBlockCount = 0
            lastTrialNum = -1
            while (highBlock[lastTrialNum]==lastBlock):
                lastTrialNum-=1
                lastBlockCount-=1
            if (sum(valid[lastBlockCount:])<minLastBlockSize):
                trialsToInclude[lastTrialNum:]=False
                totalBlocks -=1 #dont count the last block if its too small



            correctMiddle = correct & oneFreq #Use only correct tirals and only middle freq
            trialsToUse = trialsToInclude & correctMiddle #Use correctMiddle and only the trials not skipped

            trialsToUseRight = correctRightward & trialsToUse
            trialsToUseLeft = correctLeftward & trialsToUse
            trialsEachCond = [trialsToUseRight,trialsToUseLeft]

            numBlocksDict[behavSession] = totalBlocks
            ###################################################################################################
            ###################################################################################################

        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        #print 'behavior ',behavSession,' tetrode ',oneCell.tetrode,' cluster ',cluster

        # -- Load Spike Data From Certain Cluster --
        spkData = ephyscore.CellData(oneCell)
        spkTimeStamps = spkData.spikes.timestamps

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)

        spikeCountEachTrial = spikeCountMat.flatten()

        curModDirection = ''
        modDirectionScore = 0
        curBlockModI = sum(spikeCountEachTrial[(blockNumber==0) & trialsToUse])/float(sum((blockNumber==0) & trialsToUse))
        for blockNum in range(0,totalBlocks):
            if (sum((blockNumber==blockNum) & trialsToUse) == 0):
                continue
            blockModI = sum(spikeCountEachTrial[(blockNumber==blockNum) & trialsToUse])/float(sum((blockNumber==blockNum) & trialsToUse)) #Count average spikes in this block with the correct trials of middle freq
            if (curBlockModI > blockModI):
                if (curModDirection == 'up'):
                    modDirectionScore +=1
                curModDirection = 'down'
            elif (curBlockModI < blockModI):
                if (curModDirection == 'down'):
                    modDirectionScore +=1
                curModDirection = 'up'
            curBlockModI = blockModI


        spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
        spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))

        if ((spikeAvgRight + spikeAvgLeft) == 0):
            modIDict[behavSession][clusterNumber] = 0.0
            modSigDict[behavSession][clusterNumber] = 1.0
        else:
            mod_sig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,stimulusRange,trialsEachCond)
            currentMI = (spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft)
            modIDict[behavSession][clusterNumber] = currentMI
            modSigDict[behavSession][clusterNumber] = mod_sig[1]

        modDirectionScoreDict[behavSession][clusterNumber] = modDirectionScore

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

    modI_file.write("modI:")
    for modIInd in modIDict[bSession]:
        modI_file.write("%s," % modIInd)
    modI_file.write("\n")

    modI_file.write("modSig:")
    for modSigInd in modSigDict[bSession]:
        modI_file.write("%s," % modSigInd)
    modI_file.write("\n")

    modI_file.write("modDir:")
    for modDirectInd in modDirectionScoreDict[bSession]:
        modI_file.write("%s," % modDirectInd)
    modI_file.write("\n")

modI_file.close()

#########################################################################################

print 'error with sessions: '
for badSes in badSessionList:
    print badSes
print 'finished modI value check'


