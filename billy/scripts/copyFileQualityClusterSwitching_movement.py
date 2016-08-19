
from jaratoolbox import settings
import os
import glob
import sys
import importlib
import re
import numpy as np

mouseName = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+mouseName+'_quality'#_separated_tuning'############!!!!!!!!!!!!!!!!!!!!!!!!!
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
qualityList = [1,6]#[11,61,13,63,14,64,15,65]#[1,4,5,6,7]#range(1,10)
minZVal = 0.0
maxISIviolation = 0.02
minMovementModulation = 0.1
maxMovementModSig = 0.05
movementModulationWindow = '0to0.2sec_window'
minFileName = 'testMove_BEST_quality-1-6_ZVal-0_ISI-100_moveMod-0.25'+'_'+movementModulationWindow#'test_separated_tuning_BEST_quality-11-61_13_63_14_64_15_65_ZVal-3_ISI-2' #name of the file to put the copied files in 'ONLY_SHAPE_quality-1-6_ZVal-0_ISI-100''good_shape-1-6_ZVAL-0_ISI-100'
################################################################################################
################################################################################################

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')
ISIFilename = os.path.join(processedDir,'ISI_Violations.txt')
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
movementmodIFile.close()
movementmodSFile.close()
'''
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
'''
copyTuningReportsToDir = '/home/billywalker/Pictures/quality_clusters/switching_tuning_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyTuningReportsToDir):
    os.makedirs(copyTuningReportsToDir)
os.chdir(copyTuningReportsToDir)#This deletes the files that already exist in that folder
files=glob.glob('*.png')
for filename in files:
    os.unlink(filename)
copyTuningSideinReportsToDir = '/home/billywalker/Pictures/quality_clusters/switching_tuning_sidein_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyTuningSideinReportsToDir):
    os.makedirs(copyTuningSideinReportsToDir)
os.chdir(copyTuningSideinReportsToDir)#This deletes the files that already exist in that folder
files=glob.glob('*.png')
for filename in files:
    os.unlink(filename)
copyTuningAllfreqReportsToDir = '/home/billywalker/Pictures/quality_clusters/switching_tuning_allfreq_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyTuningAllfreqReportsToDir):
    os.makedirs(copyTuningAllfreqReportsToDir)
os.chdir(copyTuningAllfreqReportsToDir)#This deletes the files that already exist in that folder
files=glob.glob('*.png')
for filename in files:
    os.unlink(filename)


for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]

    if (behavSession != oneCell.behavSession):
        print oneCell.behavSession
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
    elif behavSession not in ISIDict: #CHANGE THIS TO EPHYSESSION FOR OLD ISI FILE
        continue
    elif behavSession not in movementmodIDict:
        print 'not in movement Dict '+behavSession
        continue

    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
    midFreq = minTrialDict[behavSession][0]
    #if ((abs(float(maxZDict[behavSession][midFreq][clusterNumber])) >= minZVal) & (ISIDict[behavSession][clusterNumber] <= maxISIviolation)):#
    if ((ISIDict[behavSession][clusterNumber] <= maxISIviolation) & (abs(movementmodIDict[behavSession][clusterNumber]) >= minMovementModulation) & (movementmodSigDict[behavSession][clusterNumber] <= maxMovementModSig)):
        for freq in minTrialDict[behavSession]:
            #os.system('cp /home/billywalker/Pictures/raster_hist/%s/%s/rast_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_hist/%s/%s/' % (subject,freq,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/raster_block/%s/block_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_block/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/raster_allFreq/%s/rast_allFreq_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_allFreq/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/switching_reports/%s/report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
            #os.system('cp /home/billywalker/Pictures/raster_block_reports/%s/report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_block_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))#############################################################################
            os.system('cp /home/billywalker/Pictures/switching_tuning_reports/%s/tuning_report_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_tuning_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
            os.system('cp /home/billywalker/Pictures/switching_tuning_sidein_reports/%s/switch_report_sidein_movement_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_tuning_sidein_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
            os.system('cp /home/billywalker/Pictures/switching_tuning_allfreq_reports/%s/switch_report_allFreq_movement_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/switching_tuning_allfreq_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))


#OLD WAY OF READING ISI FILE
#ISIDict[ephysSession][tetrode-1][cluster-1]
