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
import animalTetDepths #This is to get the lengths of the tetrodes for each animal

subject = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+subject+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

outputDir = '/home/billywalker/Pictures/modIndex/'

binWidth = 0.020 # Size of each bin in histogram in seconds

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes


################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]#[1,4,5,6,7]#range(1,10) the quality of the cells that should be included. See [[Report 2015-06-29: Numbering System of Cluster Quality]]
minZVal = 0.0 #the minimum Z value for the sound response of the cells includedThis should be zero since the movement modulation does not depend on the sound response
maxISIviolation = 0.02 #maximum ISI violation fraction below 2ums . 
minPValue = 0.05 #the max p value in order for a cell to be considered significant
inStriatumRangeCheck = True #if true, check that the cells are in the striatum
movementModulationWindow = '0.05to0.15sec_window' #which window of movement to look at for the modulation (this window must already be calculated in test038_write_maxZ_movement_response_stat.py) aligned to center out as 0sec
modIndFileName = 'test_inStriatum_modIndex_movement'+'_'+movementModulationWindow #the name of the file to save to
################################################################################################
################################################################################################

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')
ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')
modIFilename = os.path.join(processedDir,'modIndex.txt')
nameOfmovementmodSFile = 'modSig_'+'LvsR_movement_'+movementModulationWindow+'_'+subject+'.txt'
nameOfmovementmodIFile = 'modIndex_'+'LvsR_movement_'+movementModulationWindow+'_'+subject+'.txt'
movementmodIFilename = os.path.join(processedDir,nameOfmovementmodIFile)
movementmodSFilename = os.path.join(processedDir,nameOfmovementmodSFile)



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
modIFile = open(modIFilename, 'r')
movementmodIFile=open(movementmodIFilename, 'r')
movementmodSFile=open(movementmodSFilename, 'r')


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
behavName = ''
for line in ISIFile:
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1]
    else:
        ISIDict[behavName] = [float(x) for x in line.split(',')[0:-1]]
'''
#OLD WAY TO READ ISI FILE
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
'''
'''
modIDict = nestedDict() #stores all the modulation indices
modSigDict = nestedDict() #stores the significance of the modulation of each cell
behavName = ''
for line in modIFile:
    splitLine = line.split(':')
    if (splitLine[0] == 'Behavior Session'):
        behavName = splitLine[1][:-1]
    elif (splitLine[0] == 'modI'):
        modIDict[behavName][splitLine[1]] = [float(x) for x in splitLine[2].split(',')[0:-1]]
    elif (splitLine[0] == 'modSig'):
        modSigDict[behavName][splitLine[1]] = [float(x) for x in splitLine[2].split(',')[0:-1]]
'''
movementmodIDict = {}
movementmodSigDict = {}
behavName = ''

for line in movementmodIFile:
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1]  
    else:
        movementmodIDict[behavName] = [float(x) for x in line.split(',')[0:-1]]

for line in movementmodSFile:
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1] 
    else:
        movementmodSigDict[behavName] = [float(x) for x in line.split(',')[0:-1]]


ISIFile.close()
maxZFile.close()
minPerfFile.close()
minTrialFile.close()
modIFile.close()
movementmodIFile.close()
movementmodSFile.close()

########################CHOOSE WHICH CELLS TO PLOT################################################
modIndexArray = []
for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]

    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    depth = oneCell.depth #FOR DEPTH CLUSTER QUALTIY


    clusterQuality = oneCell.quality[cluster-1]

    
    if clusterQuality not in qualityList:
        #print 'no qualityList'
        continue
    elif behavSession not in minPerfList:
        print 'no minPerfList'
        continue
    elif behavSession not in minTrialDict:
        print 'no minTrialDict'
        continue
    elif behavSession not in movementmodIDict:
        print 'no movementmodIDict ',behavSession
        continue
    elif behavSession not in movementmodSigDict:
        print 'no movementmodSigDict ',behavSession
        continue
    elif behavSession not in ISIDict: #CHANGE THIS TO EPHYSESSION FOR OLD ISI FILE
        print 'no ISIDict'
        continue

    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
    #for freq in minTrialDict[behavSession]: #(abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal)
    if (len(minTrialDict[behavSession]) >= 1):
        if inStriatumRangeCheck:
            if ((ISIDict[behavSession][clusterNumber] <= maxISIviolation) and (animalTetDepths.tetDB.isInStriatum(subject,tetrode,depth))):
                modIndexArray.append([movementmodIDict[behavSession][clusterNumber],movementmodSigDict[behavSession][clusterNumber]])
                #if movementmodSigDict[behavSession][clusterNumber] < 0.05:
                print 'behavior ',behavSession,' tetrode ',tetrode,' cluster ',cluster
        else:
            if ((ISIDict[behavSession][clusterNumber] <= maxISIviolation)):
                modIndexArray.append([movementmodIDict[behavSession][clusterNumber],movementmodSigDict[behavSession][clusterNumber]])
                print 'behavior ',behavSession,' tetrode ',tetrode,' cluster ',cluster

##########################THIS IS TO PLOT HISTOGRAM################################################
modIndBinVec = np.arange(-1,1,binWidth)
binModIndexArraySig = np.empty(len(modIndBinVec))
binModIndexArrayNonSig = np.empty(len(modIndBinVec))
maxMI=0
totalSig = 0
for binInd in range(len(modIndBinVec)-1):
    binTotalSig = 0
    binTotalNonSig = 0
    for modIndSig in modIndexArray:
        if ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1]) and (modIndSig[1] <= minPValue)):
            binTotalSig += 1
            totalSig += 1
        elif ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1])):
            binTotalNonSig += 1
        maxMI = max(maxMI,abs(modIndSig[0]))
    binModIndexArraySig[binInd] = binTotalSig
    binModIndexArrayNonSig[binInd] = binTotalNonSig
binModIndexArraySig[-1] = 0
binModIndexArrayNonSig[-1] = 0

print 'number of cells: ',len(modIndexArray)
print 'number of significantly modulated cells: ',totalSig

plt.clf() 

plt.bar(modIndBinVec,binModIndexArraySig,width = binWidth, color = 'b')
plt.bar(modIndBinVec,binModIndexArrayNonSig,width = binWidth, color = 'g',bottom = binModIndexArraySig)

plt.xlim((-(maxMI+binWidth),maxMI+binWidth))

plt.xlabel('Modulation Index')
plt.ylabel('Number of Cells')


plt.figtext(.2,.87,'Total Number of Cells: %s'%(len(modIndexArray)),fontsize=15)
plt.figtext(.2,.91,'Total Number of Significantly Modulated Cells: %s'%totalSig,fontsize=15)

plt.gcf().set_size_inches((8.5,11))
figformat = 'png'
filename = '%s_%s.%s'%(modIndFileName,subject,figformat)
fulloutputDir = outputDir+subject +'/'
fullFileName = os.path.join(fulloutputDir,filename)

directory = os.path.dirname(fulloutputDir)
if not os.path.exists(directory):
    os.makedirs(directory)
print 'saving figure to %s'%fullFileName
plt.gcf().savefig(fullFileName,format=figformat)


#plt.show()

