'''
finds all behavior sessions in allcells that have more than a minimum percentage correct in performance for all frequencies in the Switching Task
Billy Walker
'''

#import allcells_test059 as allcells
from jaratoolbox import loadbehavior
from jaratoolbox import settings
import os
import sys
import numpy as np
import importlib

mouseName = str(sys.argv[1])
allcellsFileName = 'mouse_analysis/'+mouseName+'/allcells_'+mouseName
allcells = importlib.import_module(allcellsFileName)


outputDir = '/home/billywalker/data/ephys'
nameOfFile = 'minPerformance'
minPerf = 0.60 #the minimum performance or percentage correct of the end frequencies

subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''

nameOfOutputFile = nameOfFile + '_' + subject

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
        
        if ((firstPerf >= minPerf) & (lastPerf >= minPerf) & (highBlPerf >= minPerf) & (lowBlPerf >= minPerf)):
            text_file.write("\n%s" % behavSession)
        
        #print behavSession,': ','low ',firstPerf,' middleLow ',lowBlPerf,' middleHigh ',highBlPerf,' high ',lastPerf 
        #raw_input("Press Enter to continue...")


text_file.close()
