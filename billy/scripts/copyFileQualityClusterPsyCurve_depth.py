
from jaratoolbox import settings
import os
import sys
import importlib
import re
import numpy as np

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality_depth'############################FOR DEPTH CLUSTER QUALITY
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]
minZVal = 3.0
maxISIviolation = 0.02
minDepth = 0#2.1######################################FOR DEPTH CLUSTER QUALTIY
maxDepth = 30#3.0######################################FOR DEPTH CLUSTER QUALITY

minFileName = 'BEST_quality-1-6_ZVal-3_ISI-2' #name of the file to put the copied files in
################################################################################################
################################################################################################

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')
ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')


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

copyToDir = '/home/billywalker/Pictures/quality_clusters/raster_hist/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyToDir):
    os.makedirs(copyToDir)
copyReportsToDir = '/home/billywalker/Pictures/quality_clusters/psyCurve_reports/centerFreq/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyReportsToDir):
    os.makedirs(copyReportsToDir)



for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    
    if (behavSession != oneCell.behavSession):
        print oneCell.behavSession
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    clusterQuality = oneCell.quality[cluster-1]
    depth = oneCell.depth#################################FOR DEPTH CLUSTER QUALTIY

    if clusterQuality not in qualityList:
        continue
    elif behavSession not in minPerfList:
        continue
    elif behavSession not in minTrialDict:
        continue
    elif behavSession not in maxZDict:
        continue
    elif ephysSession not in ISIDict:
        continue
    elif ((depth < minDepth) or (depth > maxDepth)):#################################FOR DEPTH CLUSTER QUALTIY
        continue
    
    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
    for freq in minTrialDict[behavSession]:
        if ((abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal) & (ISIDict[ephysSession][tetrode-1][cluster-1] <= maxISIviolation)):
            thisRaster = '/home/billywalker/Pictures/raster_hist/'+subject+'/Center_Frequencies/rast_'+subject+'_'+behavSession+'_'+freq+'_T'+str(tetrode)+'c'+str(cluster)+'.png'
            if (os.path.isfile(thisRaster)):
                os.system('cp /home/billywalker/Pictures/raster_hist/%s/Center_Frequencies/rast_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_hist/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            else:
                os.system('cp /home/billywalker/Pictures/raster_hist/%s/Outside_Frequencies/rast_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_hist/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            os.system('cp /home/billywalker/Pictures/psyCurve_reports/centerFreq/%s/report_centerFreq_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/psyCurve_reports/centerFreq/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
