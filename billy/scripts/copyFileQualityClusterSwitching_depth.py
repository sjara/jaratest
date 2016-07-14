
from jaratoolbox import settings
import os
import sys
import importlib
import re
import numpy as np
import animalTetDepths #This is to get the lengths of the tetrodes for each animal

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality'
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
qualityList = [1,6]#[1,4,5,6,7]#range(1,10)
minZVal = 0.0#3.0
maxISIviolation = 0.02
#minDepth = 2.1######################################FOR DEPTH CLUSTER QUALTIY
#maxDepth = 3.8######################################FOR DEPTH CLUSTER QUALITY

minFileName = 'good_quality_in_striatum-1-6_ZVal-0_ISI-2'#'BEST_quality-1-6_ZVal-3_ISI-2' #name of the file to put the copied files in
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
behavName = ''
for line in ISIFile:
    #ehavLine = line.split(':')
    #reqLine = line.split()
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

ISIFile.close()
maxZFile.close()
minPerfFile.close()
minTrialFile.close()

copyToDir = '/home/billywalker/Pictures/quality_clusters/raster_hist/'+subject+'/'+minFileName+'/'
copyBlockToDir = '/home/billywalker/Pictures/quality_clusters/raster_block/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyToDir):
    os.makedirs(copyToDir)
if not os.path.exists(copyBlockToDir):
    os.makedirs(copyBlockToDir)
copyAllFreqToDir = '/home/billywalker/Pictures/quality_clusters/raster_allFreq/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyAllFreqToDir):
    os.makedirs(copyAllFreqToDir)
copyReportsToDir = '/home/billywalker/Pictures/quality_clusters/switching_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyReportsToDir):
    os.makedirs(copyReportsToDir)
copyRastRepToDir = '/home/billywalker/Pictures/quality_clusters/raster_block_reports/'+subject+'/'+minFileName+'/'###################################################################################################3
if not os.path.exists(copyRastRepToDir):#################################################################
    os.makedirs(copyRastRepToDir)#########################################################################33

copyTuningReportsToDir = '/home/billywalker/Pictures/quality_clusters/switching_tuning_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyTuningReportsToDir):
    os.makedirs(copyTuningReportsToDir)

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
    elif behavSession not in ISIDict: #CHANGE THIS TO EPHYSESSION FOR OLD ISI FILE
        continue
    elif not (animalTetDepths.tetDB.isInStriatum(subject,tetrode,depth)):
        continue
    
    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
    midFreq = minTrialDict[behavSession][0]
    if ((abs(float(maxZDict[behavSession][midFreq][clusterNumber])) >= minZVal) & (ISIDict[behavSession][clusterNumber] <= maxISIviolation)):
        for freq in minTrialDict[behavSession]:
            #os.system('cp /home/billywalker/Pictures/raster_hist/%s/%s/rast_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_hist/%s/%s/' % (subject,freq,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/raster_block/%s/block_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_block/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/raster_allFreq/%s/rast_allFreq_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_allFreq/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/switching_reports/%s/report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/raster_block_reports/%s/report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_block_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))#############################################################################
            os.system('cp /home/billywalker/Pictures/switching_tuning_reports/%s/tuning_report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_tuning_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))#############################################################################
