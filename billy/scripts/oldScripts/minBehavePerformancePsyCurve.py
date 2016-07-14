'''
finds all behavior sessions in allcells that have more than a minimum percentage correct in performance for outer frequencies in PsyCurve
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
minPerf = 0.70 #the minimum performance or percentage correct of the end frequencies

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
        lastFreq = bdata['targetFrequency'] == possibleFreq[-1]

        correctFirst = sum(correct & firstFreq)
        correctLast = sum(correct & lastFreq)
        incorrectFirst = sum(incorrect & firstFreq)
        incorrectLast = sum(incorrect & lastFreq)

        firstPerf = float(correctFirst)/(correctFirst+incorrectFirst)
        lastPerf = float(correctLast)/(correctLast+incorrectLast)
        
        if ((firstPerf >= minPerf) & (lastPerf >= minPerf)):
            text_file.write("\n%s" % behavSession)


text_file.close()
