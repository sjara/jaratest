'''
finds all behavior sessions in allcells that have more than a minimum percentage correct in performance for all frequencies in the Switching Task. The only argument is the mouse name
Billy Walker
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings
import os
import numpy as np
import sys
import importlib

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


outputDir = '/home/billywalker/data/ephys'
nameOfFile = 'minPerformance'
minPerf = 0.60 #the minimum performance or percentage correct of the end frequencies
minCorrectPerBlock = 50 #the minimum number of correct trials in each block
minNumBlocks = 3 #the minimum number of blocks with at least minCorrectPerBlock number of correct trials

subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''

#nameOfOutputFile = nameOfFile + '_' + subject

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

finalOutputDir = outputDir+'/'+subject+'_processed'

minPerfList = []
try:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "r+") #open a text file to read and write in
    text_file.readline()
    minPerfList=text_file.read().split()
except:
    text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to read and write in
    text_file.write("minimum performance percentage: %s\n" % minPerf)




for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    if (behavSession != oneCell.behavSession):


        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        ephysRoot = os.path.join(ephysRootDir,subject)

        if (behavSession in minPerfList): #if it is already in the list, dont add it again
            continue

        # -- Load Behavior Data --
        behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
        bdata = loadbehavior.BehaviorData(behaviorFilename)
        numberOfTrials = len(bdata['choice'])


        correct = bdata['outcome']==bdata.labels['outcome']['correct']
        incorrect = bdata['outcome']==bdata.labels['outcome']['error']

        possibleFreq = np.unique(bdata['targetFrequency'])
        firstFreq = bdata['targetFrequency'] == possibleFreq[0]
        lastFreq = bdata['targetFrequency'] == possibleFreq[2]

        correctFirst = sum(correct & firstFreq)
        correctLast = sum(correct & lastFreq)
        incorrectFirst = sum(incorrect & firstFreq)
        incorrectLast = sum(incorrect & lastFreq)

        firstPerf = float(correctFirst)/(correctFirst+incorrectFirst)
        lastPerf = float(correctLast)/(correctLast+incorrectLast)

        middleFreq =  bdata['targetFrequency'] == possibleFreq[1]
        highBlock = bdata['currentBlock'] == bdata.labels['currentBlock']['high_boundary']
        lowBlock = bdata['currentBlock'] == bdata.labels['currentBlock']['low_boundary']
        middleFreqHighBlock = middleFreq & highBlock
        middleFreqLowBlock = middleFreq & lowBlock
        correctMidHigh = sum(middleFreqHighBlock & correct)
        incorrectMidHigh = sum(middleFreqHighBlock & incorrect)
        correctMidLow = sum(middleFreqLowBlock & correct)
        incorrectMidLow = sum(middleFreqLowBlock & incorrect)
        highBlPerf = float(correctMidHigh)/(correctMidHigh+incorrectMidHigh)
        lowBlPerf = float(correctMidLow)/(correctMidLow+incorrectMidLow)

        blocks = bdata['currentBlock']
        highBlock = bdata.labels['currentBlock']['high_boundary']
        lowBlock = bdata.labels['currentBlock']['low_boundary']
        goodBlockCount = 0 #Keeps track of the number of good blocks
        badBlockCheck = False #Checks if there in a block in the first 3 blocks that does not pass the requirements
        
        curBlock = blocks[0]
        curTrial = 0
        startTrial = 0
        endTrial = 0
        while (curTrial < (len(blocks)-1)):
            startTrial = curTrial
            while ((curTrial < (len(blocks)-1)) & (blocks[curTrial] == curBlock)):
                curTrial += 1
            endTrial = curTrial #finds the end of the current block
            curBlock = blocks[curTrial]
            if(sum(correct[startTrial:(endTrial+1)]) >= minCorrectPerBlock): #counts all the correct trials in the current block and counts it as good if it has the min num of correct trials
                goodBlockCount += 1
            else:
                if (goodBlockCount < minNumBlocks):
                    badBlockCheck = True
                    break
        

        
        if ((firstPerf >= minPerf) & (lastPerf >= minPerf) & (highBlPerf >= minPerf) & (lowBlPerf >= minPerf) & (goodBlockCount >= minNumBlocks) & (not badBlockCheck)):
            text_file.write("\n%s" % behavSession)        


text_file.close()
print 'finished min behavior performance check'
