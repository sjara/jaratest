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

mouseList = ['test089','test059','test017']

outputDir = '/home/billywalker/Pictures/modIndex_100-200ms/'#####################

binWidth = 0.020 # Size of each bin in histogram in seconds

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes


################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]#[1,4,5,6,7]#range(1,10)
minZVal = 3.0
maxISIviolation = 0.02
minModDirectionScore = 1.0
minPValue = 0.05
################################################################################################
################################################################################################


class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value

modIndexArray = []
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
    modIFilename = os.path.join(processedDir,'modIndex_afterSound.txt')


    maxZFile = open(maxZFilename, 'r')
    minPerfFile = open(minPerfFilename, 'r')
    minTrialFile = open(minTrialFilename, 'r')
    ISIFile = open(ISIFilename, 'r')
    modIFile = open(modIFilename, 'r')


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


    modIDict = {} #stores all the modulation indices
    modSigDict = {} #stores the significance of the modulation of each cell
    modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
    behavName = ''
    for line in modIFile:
        splitLine = line.split(':')
        if (splitLine[0] == 'Behavior Session'):
            behavName = splitLine[1][:-1]
        elif (splitLine[0] == 'modI'):
            modIDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
        elif (splitLine[0] == 'modSig'):
            modSigDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
        elif (splitLine[0] == 'modDir'):
            modDirectionScoreDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]




    ISIFile.close()
    maxZFile.close()
    minPerfFile.close()
    minTrialFile.close()
    modIFile.close()

    ########################CHOOSE WHICH CELLS TO PLOT################################################
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        subject = oneCell.animalName
        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
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
        elif behavSession not in modIDict:
            continue
        elif ephysSession not in ISIDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        midFreq = minTrialDict[behavSession][0]
        if ((abs(float(maxZDict[behavSession][midFreq][clusterNumber])) < minZVal) | (ISIDict[ephysSession][tetrode-1][cluster-1] > maxISIviolation)):
            continue

        modIndexArray.append([modIDict[behavSession][clusterNumber],modSigDict[behavSession][clusterNumber],modDirectionScoreDict[behavSession][clusterNumber]])

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
        if ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1]) and (modIndSig[1] <= minPValue) and (modIndSig[2]>= minModDirectionScore)):
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

plt.figtext(.15,.83,'Total Cells: %s'%(len(modIndexArray)),fontsize=15)
plt.figtext(.15,.87,'Total Sig Mod Cells: %s'%totalSig,fontsize=15)
plt.figtext(.15,.91,'Percentage of Sig Mod Cells: %s'%(round((totalSig/float(len(modIndexArray))),3)*100),fontsize=15)

plt.gcf().set_size_inches((8.5,11))
figformat = 'png'
filename = 'modIndex_%s.%s'%('allmice_switching',figformat)
fulloutputDir = outputDir+'allmice'+'/'
fullFileName = os.path.join(fulloutputDir,filename)

directory = os.path.dirname(fulloutputDir)
if not os.path.exists(directory):
    os.makedirs(directory)
print 'saving figure to %s'%fullFileName
plt.gcf().savefig(fullFileName,format=figformat)


plt.show()

