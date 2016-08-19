
from jaratoolbox import settings
import numpy as np
import os
import sys
import importlib


mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

if (str(sys.argv[2]) == "Switching"):
    switchBool = True
else:
    switchBool = False

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

###############################################################################################################
###############################################################################################################
clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes
qualityList = [1,6]
minZVal = 3.0
maxISIviolation = 0.02
###############################################################################################################
###############################################################################################################



class nestedDict(dict):
    def __getitem__(self, item):#This is for maxZDict
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value




subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')
ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')

maxZFile = open(maxZFilename, 'r')
minPerfFile = open(minPerfFilename, 'r')
minTrialFile = open(minTrialFilename, 'r')
ISIFile = open(ISIFilename, 'r')

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


ISIFile.close()
maxZFile.close()
minPerfFile.close()
minTrialFile.close()
  





def main():
    '''
    #Switching
    cellsPerSessionSwitching()
    cellsPerGoodSession()
    cellsAnyFreqPerSessionSwitching()
    
    
    #PsyCurve
    cellsPerSessionPsyCurve()
    cellsPerGoodSession()
    '''
    print "For mouse "+subject+":"
    if switchBool:
        print 'switching'
        cellsPerSessionSwitching()
        responsiveCellsSwitching()
    else:
        print'psyCurve'
        cellsPerSessionPsyCurve()
        responsiveCellsPsyCurve()




'''
def cellsPerSessionSwitching(): #finds the total average number of good cells per session for middle freq. Switching

    cellCount = 0
    sessions = 0
    bSession = ''
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if (bSession != behavSession):
            sessions += 1
            bSession = behavSession

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in maxZDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freqList = []
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        if (abs(float(maxZDict[behavSession][str(freqList[1])][clusterNumber])) >= minZVal):
            cellCount+=1

    print "Average number of good cells per session for middle freq: ",float(cellCount)/sessions
    print "Total number of good cells for middle freq: ",cellCount

def cellsPerSessionPsyCurve(): #finds the total average number of good cells per session for any freq. PsyCurve

    cellCount = 0
    sessions = 0
    bSession = ''
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if (bSession != behavSession):
            sessions += 1
            bSession = behavSession

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in maxZDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        for freq in maxZDict[behavSession]:
            if (abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal):
                cellCount+=1
                continue

    print "Average number of good cells per session for any freq: ",float(cellCount)/sessions
    print "Total number of good cells for any freq: ",cellCount


def cellsPerGoodSession(): #finds the average number of good cells per good session for some freq. Both
    cellCount = 0
    goodSessions = 0
    bSession = ''
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if behavSession not in minPerfList:
            continue
        elif behavSession not in minTrialDict:
            continue

        if (bSession != behavSession):
            goodSessions += 1
            bSession = behavSession

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in maxZDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        for freq in  minTrialDict[behavSession]:
            #print clusterNumber,' ',freq,' ',behavSession
            #print maxZDict[behavSession][freq][clusterNumber]
            if (abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal):
                cellCount+=1
                continue

    print "Average number of good cells per good session: ",float(cellCount)/goodSessions
    print "Total number of good cells in good sessions: ",cellCount



def cellsAnyFreqPerSessionSwitching(): #finds the average number of good cells per frequency per good session. Switching
    highCellCount = 0
    lowCellCount = 0
    midCellCount = 0
    goodSessions = 0
    bSession = ''
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if behavSession not in minPerfList:
            continue
        elif behavSession not in minTrialDict:
            continue

        if (bSession != behavSession):
            goodSessions += 1
            bSession = behavSession

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in maxZDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freqList = []
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        if (abs(float(maxZDict[behavSession][str(freqList[0])][clusterNumber])) >= minZVal):
            lowCellCount+=1
        if (abs(float(maxZDict[behavSession][str(freqList[1])][clusterNumber])) >= minZVal):
            midCellCount+=1
        if (abs(float(maxZDict[behavSession][str(freqList[2])][clusterNumber])) >= minZVal):
            highCellCount+=1

    print "Average number of good cells per session for high freq: ",float(highCellCount)/goodSessions
    print "Average number of good cells per session for middle freq: ",float(midCellCount)/goodSessions
    print "Average number of good cells per session for low freq: ",float(lowCellCount)/goodSessions
'''
def cellsPerSessionPsyCurve(): #finds the total average number of good cells per session for any freq. PsyCurve

    cellCount = 0
    midFreqCellCount = 0
    bSessions = []
    goodBSessions = []
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if (behavSession not in bSessions):
            bSessions.append(behavSession)
            
        if behavSession not in minPerfList:
            continue
        elif behavSession not in minTrialDict:
            continue

        if (behavSession not in goodBSessions):
            goodBSessions.append(behavSession)

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in maxZDict:
            continue
        elif ephysSession not in ISIDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freqList = []
        cellCountBool = False
        midFreqCellCountBool = False
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        for indFreq,frequency in enumerate(freqList):
            if ((abs(float(maxZDict[behavSession][str(frequency)][clusterNumber])) >= minZVal) & (ISIDict[ephysSession][tetrode-1][cluster-1] <= maxISIviolation)):
                cellCountBool = True
                if ((indFreq == (len(freqList)/2)) or (indFreq == ((len(freqList)/2) + 1))):
                    midFreqCellCountBool = True
        if cellCountBool:
            cellCount += 1
        if midFreqCellCountBool:
            midFreqCellCount += 1
                

    print "Total number of good cells for any freq: ",cellCount
    print "Average number of good cells per session for any freq: ",float(cellCount)/len(bSessions)
    print "Average number of good cells per good session for any freq: ",float(cellCount)/len(goodBSessions)
    print "Total number of good cells for the middle freqs: ",midFreqCellCount
    print "Average number of good cells per session for the middle freqs: ",float(midFreqCellCount)/len(bSessions)
    print "Average number of good cells per good session for the middle freqs: ",float(midFreqCellCount)/len(goodBSessions)
    print "Total number of good sessions: ",len(goodBSessions)
    print "Total number of sessions: ",len(bSessions)


def cellsPerSessionSwitching(): #finds the total average number of good cells per session for any freq. PsyCurve

    cellCount = 0
    midFreqCellCount = 0
    bSessions = []
    goodBSessions = []
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if (behavSession not in bSessions):
            bSessions.append(behavSession)
            print behavSession
            
        if behavSession not in minPerfList:
            continue
        elif behavSession not in minTrialDict:
            continue

        if (behavSession not in goodBSessions):
            goodBSessions.append(behavSession)
            print "good"

        if clusterQuality not in qualityList:
            continue
        elif behavSession not in maxZDict:
            continue
        elif ephysSession not in ISIDict:
            continue

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freqList = []
        cellCountBool = False
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        for indFreq,frequency in enumerate(freqList):
            if ((abs(float(maxZDict[behavSession][str(frequency)][clusterNumber])) >= minZVal) & (ISIDict[ephysSession][tetrode-1][cluster-1] <= maxISIviolation)):
                cellCountBool = True
                if (indFreq == 1):
                    midFreqCellCount += 1
        if cellCountBool:
            cellCount += 1
                
    print "Total number of good cells for any freq: ",cellCount
    print "Average number of good cells per session for any freq: ",float(cellCount)/len(bSessions)
    print "Average number of good cells per good session for any freq: ",float(cellCount)/len(goodBSessions)
    print "Total number of good cells for the middle freq: ",midFreqCellCount
    print "Average number of good cells per session for the middle freq: ",float(midFreqCellCount)/len(bSessions)
    print "Average number of good cells per good session for the middle freq: ",float(midFreqCellCount)/len(goodBSessions)
    print "Total number of good sessions: ",len(goodBSessions)
    print "Total number of sessions: ",len(bSessions)

def responsiveCellsPsyCurve(): #finds the total average number of good cells per session for any freq. PsyCurve

    responsiveCellCount = 0
    midFreqResponsiveCellCount = 0
    qualityCellCount = 0
    qualityAndISICellCount = 0
    bSessions = []
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if (behavSession not in bSessions):
            bSessions.append(behavSession)

        if behavSession not in maxZDict:
            continue
        elif ephysSession not in ISIDict:
            continue
        if clusterQuality in qualityList:
            qualityCellCount += 1

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freqList = []
        responsiveCellCountBool = False
        midFreqResponsiveCellCountBool  = False
        qualityAndISICellCountBool = False
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        for indFreq,frequency in enumerate(freqList):
            if (abs(float(maxZDict[behavSession][str(frequency)][clusterNumber])) >= minZVal):
                responsiveCellCountBool = True
                if ((indFreq == (len(freqList)/2)) or (indFreq == ((len(freqList)/2) + 1))):
                    midFreqResponsiveCellCountBool  = True
            if ((ISIDict[ephysSession][tetrode-1][cluster-1] <= maxISIviolation) and (clusterQuality in qualityList)):
                qualityAndISICellCountBool = True
        
        if qualityAndISICellCountBool:
            qualityAndISICellCount += 1
        if midFreqResponsiveCellCountBool:
            midFreqResponsiveCellCount += 1
        if responsiveCellCountBool:
            responsiveCellCount += 1
                

    print "Total number of responsive cells for any freq (any session): ",responsiveCellCount
    print "Total number of responsive cells for middle freqs (any session): ",midFreqResponsiveCellCount
    print "Total number of good quality cells not including ISI (any session): ", qualityCellCount
    print "Total number of good quality cells including ISI (any session): ", qualityAndISICellCount

def responsiveCellsSwitching(): #finds the total average number of good cells per session for any freq. PsyCurve

    responsiveCellCount = 0
    midFreqResponsiveCellCount = 0
    qualityCellCount = 0
    qualityAndISICellCount = 0
    bSessions = []
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]

        behavSession = oneCell.behavSession
        ephysSession = oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]

        if (behavSession not in bSessions):
            bSessions.append(behavSession)

        if behavSession not in maxZDict:
            continue
        elif ephysSession not in ISIDict:
            continue
        if clusterQuality in qualityList:
            qualityCellCount += 1

        clusterNumber = (tetrode-1)*clusNum+(cluster-1)
        freqList = []
        responsiveCellCountBool = False
        midFreqResponsiveCellCountBool  = False
        qualityAndISICellCountBool = False
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        for indFreq,frequency in enumerate(freqList):
            if (abs(float(maxZDict[behavSession][str(frequency)][clusterNumber])) >= minZVal):
                responsiveCellCountBool = True
                if (indFreq == 1):
                    midFreqResponsiveCellCountBool  = True
            if ((ISIDict[ephysSession][tetrode-1][cluster-1] <= maxISIviolation) and (clusterQuality in qualityList)):
                qualityAndISICellCountBool = True
        
        if qualityAndISICellCountBool:
            qualityAndISICellCount += 1
        if midFreqResponsiveCellCountBool:
            midFreqResponsiveCellCount += 1
        if responsiveCellCountBool:
            responsiveCellCount += 1
                

    print "Total number of responsive cells for any freq (any session): ",responsiveCellCount
    print "Total number of responsive cells for middle freqs (any session): ",midFreqResponsiveCellCount
    print "Total number of good quality cells not including ISI (any session): ", qualityCellCount
    print "Total number of good quality cells including ISI (any session): ", qualityAndISICellCount
    

main()
