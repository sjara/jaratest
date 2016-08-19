
from jaratoolbox import settings
from jaratoolbox import extraplots
import indiv_SwitchingReport as indiv
import numpy as np
import os
import sys
import importlib
import glob


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
tmpFileName = 'tmp_numCells'
excludedTmpFileName = 'tmp_excluded_numCells'
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
  

copyToDir = '/home/billywalker/Pictures/'+tmpFileName+'/'+mouseName+'/'
copyToExcludedDir = '/home/billywalker/Pictures/'+tmpFileName+'/'+mouseName+'/'+excludedTmpFileName+'/'
if not os.path.exists(copyToDir):
    os.makedirs(copyToDir)
if not os.path.exists(copyToExcludedDir):
    os.makedirs(copyToExcludedDir)

files = glob.glob(copyToDir+'*.png')
for f in files:
    os.remove(f)
files = glob.glob(copyToExcludedDir+'*')
for f in files:
    os.remove(f)


ClusterDict = {}
excludedClusterDict = {}
behavEphysDict = {}

def main():
    global myft
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
        totalClusterNum()
        clustersInGoodSessions()
        responsiveCellsMiddleFreqSwitching()
        qualityCell()
        ISIcheck()
        #middleFreqSwitching()
        #myft = showClusters()
        plotClusters()
        #raw_input("Press Enter to continue...")
    else:
        print'psyCurve'
        cellsPerSessionPsyCurve()
        responsiveCellsPsyCurve()


def totalClusterNum():
    global behavEphysDict
    behavSession = ''
    for cellID in range(0,numOfCells):
        oneCell = allcells.cellDB[cellID]
        if (behavSession != oneCell.behavSession):
            behavSession = oneCell.behavSession
            ClusterDict[behavSession] = list()
            behavEphysDict[behavSession]= oneCell.ephysSession
        tetrode = oneCell.tetrode
        cluster = oneCell.cluster
        clusterQuality = oneCell.quality[cluster-1]
        ClusterDict[behavSession].append((tetrode,cluster,clusterQuality))

def showClusters():
    currentCellList = []
    for behavSession,tetClusList in ClusterDict.iteritems():
        for tetClus in tetClusList:
            #print 'session: ',behavSession,', tetrode: ',tetClus[0],', cluster: ',tetClus[1]
            currentCellList.append((mouseName,behavSession,tetClus[0],tetClus[1]))
    #print currentCellList
    ft = extraplots.FlipThrough(indiv.switch_report,currentCellList)#############################################################
    return ft

def plotClusters():
    currentCellList = []
    totalCellCount = 0
    for behavSession,tetClusList in ClusterDict.iteritems():
        for tetClus in tetClusList:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            #print mouseName, ' ',behavSession,' ',tetrode,' ',cluster
            os.system('cp /home/billywalker/Pictures/switching_reports/%s/report_%s_%s_T%sc%s.png /home/billywalker/Pictures/%s/%s/' % (mouseName,mouseName,behavSession,str(tetrode),str(cluster),tmpFileName,mouseName))
            totalCellCount+=1
    for behavSession,tetClusList in excludedClusterDict.iteritems():
        for tetClus in tetClusList:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            #print mouseName, ' ',behavSession,' ',tetrode,' ',cluster
            os.system('cp /home/billywalker/Pictures/switching_reports/%s/report_%s_%s_T%sc%s.png %s' % (mouseName,mouseName,behavSession,str(tetrode),str(cluster),copyToExcludedDir))
    print 'Total Number Of Cells: ',totalCellCount

def clustersInGoodSessions():
    badSession = list()
    for behavSession in ClusterDict:
        if ((behavSession not in minPerfList) or (behavSession not in minTrialDict)):
            badSession.append(behavSession)
    for badSess in badSession:
        del ClusterDict[badSess]
    #print badSession

def responsiveCellsMiddleFreqSwitching():
    global excludedClusterDict
    excludedClusterDict = {}
    badSession = list()
    middleFreq = 1
    for behavSession,tetClusList in ClusterDict.iteritems():
        badTetClus = list()
        if behavSession not in maxZDict:
            if behavSession not in badSession:
                badSession.append(behavSession)
            continue
        freqList = list()
        for freq in maxZDict[behavSession]:
            freqList.append(int(freq))
        freqList.sort()
        frequency = freqList[middleFreq]
        for tetClus in tetClusList:
            clusterNumber = (tetClus[0]-1)*clusNum+(tetClus[1]-1)
            if (abs(float(maxZDict[behavSession][str(frequency)][clusterNumber])) < minZVal):
                badTetClus.append(tetClus)
        excludedClusterDict[behavSession] = list()
        for tetClus in badTetClus:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            clusterQuality = tetClus[2]
            excludedClusterDict[behavSession].append((tetrode,cluster,clusterQuality))
            ClusterDict[behavSession].remove(tetClus)
    for badSess in badSession:
        del ClusterDict[badSess]
        

def qualityCell():
    global excludedClusterDict
    excludedClusterDict = {}
    for behavSession,tetClusList in ClusterDict.iteritems():
        badTetClus = list()
        for tetClus in tetClusList:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            clusterQuality = tetClus[2]
            if clusterQuality not in qualityList:
                badTetClus.append(tetClus)
        excludedClusterDict[behavSession] = list()
        for tetClus in badTetClus:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            clusterQuality = tetClus[2]
            excludedClusterDict[behavSession].append((tetrode,cluster,clusterQuality))
            ClusterDict[behavSession].remove(tetClus)

def ISIcheck():
    global excludedClusterDict
    excludedClusterDict = {}
    badSession = list()
    for behavSession,tetClusList in ClusterDict.iteritems():
        ephysSession = behavEphysDict[behavSession]
        if ephysSession not in ISIDict:
            if behavSession not in badSession:
                badSession.append(behavSession)
            continue
        badTetClus = list()
        for tetClus in tetClusList:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            clusterQuality = tetClus[2]
            if (ISIDict[ephysSession][tetrode-1][cluster-1] > maxISIviolation):
                badTetClus.append(tetClus)
        excludedClusterDict[behavSession] = list()
        for tetClus in badTetClus:
            tetrode = tetClus[0]
            cluster = tetClus[1]
            clusterQuality = tetClus[2]
            excludedClusterDict[behavSession].append((tetrode,cluster,clusterQuality))
            ClusterDict[behavSession].remove(tetClus)
    for badSess in badSession:
        del ClusterDict[badSess]

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
