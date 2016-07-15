'''
finds all behavior sessions in allcells that have more than a minimum percentage correct in performance for all frequencies in the Switching Task. Also checks that there are 3 blocks with at least 50 correct trials in each block.
Billy Walker
'''

#import allcells_test059 as allcells
from jaratoolbox import loadbehavior
from jaratoolbox import settings
#from jaratoolbox import ephyscore
import os
import numpy as np
#from jaratoolbox import loadopenephys
#from jaratoolbox import spikesanalysis
#from jaratoolbox import extraplots
#import matplotlib.pyplot as plt
import sys
import importlib

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)


outputDir = '/home/billywalker/data/ephys'
nameOfFile = 'minPerformance'
minPerf = 0.50 #the minimum performance or percentage correct of the end frequencies
minCorrectPerBlock = 50 #the minimum number of correct trials in each block
minNumBlocks = 3 #the minimum number of blocks with at least minCorrectPerBlock number of correct trials

subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''

nameOfOutputFile = nameOfFile + '_' + subject

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

finalOutputDir = outputDir+'/'+subject+'_processed'
text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to write in


text_file.write("minimum performance percentage: %s\n" % minPerf)

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
        print behavSession+' curTrial '+str(curBlock)
        curTrial = 0
        startTrial = 0
        endTrial = 0
        while (curTrial < (len(blocks)-1)):
            print curBlock
            startTrial = curTrial
            while ((curTrial < (len(blocks)-1)) & (blocks[curTrial] == curBlock)):
                #print curTrial
                curTrial += 1
            endTrial = curTrial
            curBlock = blocks[curTrial]
            print 'sum correct is '+ str(sum(correct[startTrial:(endTrial+1)]))
            if(sum(correct[startTrial:(endTrial+1)]) >= minCorrectPerBlock):
                goodBlockCount += 1
            else:
                if (goodBlockCount < minNumBlocks):
                    badBlockCheck = True
                    break
        

        
        if ((firstPerf >= minPerf) & (lastPerf >= minPerf) & (highBlPerf >= minPerf) & (lowBlPerf >= minPerf) & (goodBlockCount >= minNumBlocks) & (not badBlockCheck)):
            text_file.write("\n%s" % behavSession)
        
        #print behavSession,': ','low ',firstPerf,' middleLow ',lowBlPerf,' middleHigh ',highBlPerf,' high ',lastPerf 
        #raw_input("Press Enter to continue...")


text_file.close()
