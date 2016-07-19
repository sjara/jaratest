'''
Lan Guo 20160111
Modified from Billy's modIndexCalcSwitching.py
New version, now takes cellDB whose individual cells contain the property 'quality' to mark whether it's a good cell or not.
Finds modulation index for all good cells (based on oneCell.quality, score of 1 or 6) for reward_change task. Comparing response to one frequency under less or more reward conditions using only correct trials.
NEW: can choose different alignment options (sound, center-out, side-in) and calculate Mod Index for different time windows with aligned spikes. 
Implemented: using santiago's methods to remove missing trials from behavior when ephys has skipped trials. -LG20160307
Implemented 'trialLimit' constraint to exclude blocks with few trials at the end of a behav session. -LG 20160324
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import sys
import importlib

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
#from jaratoolbox.test.lan.Allcells import allcellsFileName as allcells
reload(allcells)

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.020 # Size of each bin in histogram in seconds
#Frequency = 1 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
#countTimeRange = [0,0.1] #time range in which to count spikes for modulation index and modulation significance tests
#stimulusRange = [0.0,0.1] # The time range that the stimulus is being played, used in statistic test for modulation significance

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

subject = allcells.cellDB[0].animalName
ephysRootDir = settings.EPHYS_PATH
outputDir = '/home/languo/data/ephys/'+mouseName

###################Choose alignment and time window to calculate mod Index#######################
alignment = 'center-out'  #put here alignment choice!!choices are 'sound', 'center-out', 'side-in'.
countTimeRange = [0,0.1]
window = str(countTimeRange[0])+'to'+str(countTimeRange[1])+'sec_window_'
nameOfmodSFile = 'modSig_'+alignment+'_'+window+mouseName
nameOfmodIFile = 'modIndex_'+alignment+'_'+window+mouseName
#############################################################################

finalOutputDir = outputDir+'/'+subject+'_stats'

#experimenter = 'lan'
experimenter = 'billy'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered
print numOfCells

behavSession = ''
#processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')

###############FOR USING MODIDICT WITH ALL FREQS############################################
class nestedDict(dict):
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value
#############################################################################################


modIList = []#List of behavior sessions that already have modI values calculated
try:
    modI_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodIFile), 'r+') #open a text file to read and write in
    behavName = ''
    for line in modI_file:
        behavLine = line.split(':')
        if (behavLine[0] == 'Behavior Session'):
            behavName = behavLine[1][:-1]
            modIList.append(behavName)
    
except:
    modI_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodIFile), 'w') #when file dosenot exit then create it, but will truncate the existing file


#No need to initialize modIList again since all behav sessions in modI file should be the same as the ones in modSig file.
try:
    modSig_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodSFile), 'r+') #open a text file to read and write in
   
except:
    modSig_file = open('%s/%s.txt' % (finalOutputDir,nameOfmodSFile), 'w') #when file dosenot exit then create it, but will truncate the existing file


badSessionList = [] #Makes sure sessions that crash don't get modI values printed
behavSession = ''
modIndexArray = []
modIDict = nestedDict() #stores all the modulation indices
modSigDict = nestedDict()
cellNum=0
modCellNum=0
modCellList=[]
minPValue=0.05

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    print behavSession
    if oneCell.quality==1 or oneCell.quality==6:
        cellNum+=1
        if (oneCell.behavSession == behavSession): #checks to make sure the modI value is not rec
            continue
        else:
            print oneCell
    behavSession =oneCell.behavSession
print cellNum, behavSession




            
