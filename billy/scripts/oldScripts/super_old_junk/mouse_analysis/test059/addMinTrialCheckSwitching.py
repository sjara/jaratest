'''
finds all behavior sessions in allcells that have more than a minimum number of trials in each direction
Billy Walker
'''

import allcells_test059_quality as allcells
from jaratoolbox import loadbehavior
from jaratoolbox import settings
#from jaratoolbox import ephyscore
import os
import numpy as np
#from jaratoolbox import loadopenephys
#from jaratoolbox import spikesanalysis
#from jaratoolbox import extraplots
#import matplotlib.pyplot as plt


outputDir = '/home/billywalker/data/ephys'
nameOfFile = 'minTrial'
minTrialNumber = 30 #the minimum number of trials in each direction to be found

subject = allcells.cellDB[0].animalName
behavSession = ''
ephysSession = ''


numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

Frequency = 1

finalOutputDir = outputDir+'/'+subject+'_processed'
text_file = open("%s/%s.txt" % (finalOutputDir,nameOfFile), "w") #open a text file to write in

text_file.write("minimum number of trials: %s\n" % minTrialNumber)

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


        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left']
        invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
        correct = bdata['outcome']==bdata.labels['outcome']['correct']
        correctRightward = rightward & correct
        correctLeftward = leftward & correct

        possibleFreq = np.unique(bdata['targetFrequency'])
        numberOfFrequencies = len(possibleFreq)


        text_file.write("\n %s: " % behavSession)



        Freq = possibleFreq[Frequency]
        FreqName = str(Freq)
        oneFreq = bdata['targetFrequency'] == Freq

        trialsToUseRight = correctRightward & oneFreq
        trialsToUseLeft = correctLeftward & oneFreq

        if ((sum(trialsToUseRight) >= minTrialNumber) & (sum(trialsToUseLeft) >= minTrialNumber)):
            text_file.write(" %s" % FreqName)


text_file.close()
