
from jaratoolbox import settings
import os
import glob
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
qualityList = [1,6]
minZVal = 0.0
maxISIviolation = 0.02
inStriatumRangeCheck = True #if true, check that the cells are in the striatum
minMovementModulation = 0.1
maxMovementModSig = 0.05
movementModulationWindow = '0.05to0.15sec_window'
minFileName = 'testMove_BEST_quality-1-6_ZVal-0_ISI-02_moveMod-0.0'+'_'+movementModulationWindow
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

#copyToDir = '/home/billywalker/Pictures/quality_clusters/raster_hist/'+subject+'/'+minFileName+'/'
#if not os.path.exists(copyToDir):
    #os.makedirs(copyToDir)
#copyReportsToDir = '/home/billywalker/Pictures/quality_clusters/psyCurve_reports/centerFreq/'+subject+'/'+minFileName+'/'
#if not os.path.exists(copyReportsToDir):
    #os.makedirs(copyReportsToDir)
copyToCenterFreqDir = '/home/billywalker/Pictures/quality_clusters/psyCurve_tuning_centerfreq_sound_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyToCenterFreqDir):
    os.makedirs(copyToCenterFreqDir)
os.chdir(copyToCenterFreqDir)#This deletes the files that already exist in that folder
files=glob.glob('*.png')
for filename in files:
    os.unlink(filename)
copyToAllFreqDir = '/home/billywalker/Pictures/quality_clusters/psyCurve_tuning_allFreq_movement_reports/'+subject+'/'+minFileName+'/'
if not os.path.exists(copyToAllFreqDir):
    os.makedirs(copyToAllFreqDir)
os.chdir(copyToAllFreqDir)#This deletes the files that already exist in that folder
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
    depth = oneCell.depth #FOR DEPTH CLUSTER QUALTIY

    if clusterQuality not in qualityList:
        continue
    elif behavSession not in minPerfList:
        print 'not in minPerfList'
        continue
    elif behavSession not in minTrialDict:
        print 'not in minTrialList'
        continue
    #elif behavSession not in maxZDict:
        #print 'not in maxZ'
        #continue
    elif behavSession not in ISIDict:
        print 'not in ISI'
        continue
    elif behavSession not in movementmodIDict:
        print 'not in movement Dict '+behavSession
        continue
   
    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
    if ((ISIDict[behavSession][clusterNumber] <= maxISIviolation) & (abs(movementmodIDict[behavSession][clusterNumber]) >= minMovementModulation) & (movementmodSigDict[behavSession][clusterNumber] <= maxMovementModSig) & (not(inStriatumRangeCheck) or animalTetDepths.tetDB.isInStriatum(subject,tetrode,depth))):
        for freq in minTrialDict[behavSession]:
        #if ((abs(float(maxZDict[behavSession][freq][clusterNumber])) >= minZVal) & (ISIDict[behavSession][clusterNumber] <= maxISIviolation)):
            #thisRaster = '/home/billywalker/Pictures/raster_hist/'+subject+'/Center_Frequencies/rast_'+subject+'_'+behavSession+'_'+freq+'_T'+str(tetrode)+'c'+str(cluster)+'.png'
            #if (os.path.isfile(thisRaster)):
                #os.system('cp /home/billywalker/Pictures/raster_hist/%s/Center_Frequencies/rast_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_hist/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            #else:
                #os.system('cp /home/billywalker/Pictures/raster_hist/%s/Outside_Frequencies/rast_%s_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/raster_hist/%s/%s/' % (subject,subject,behavSession,freq,str(tetrode),str(cluster),subject,minFileName))
            os.system('cp /home/billywalker/Pictures/psyCurve_tuning_centerfreq_sound_reports/%s/psycurve_report_centerfreq_sound_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/psyCurve_tuning_centerfreq_sound_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
            os.system('cp /home/billywalker/Pictures/psyCurve_tuning_allFreq_movement_reports/%s/psycurve_report_allFreq_movement_%s_%s_T%sc%s.png /home/billywalker/Pictures/quality_clusters/psyCurve_tuning_allFreq_movement_reports/%s/%s/' % (subject,subject,behavSession,str(tetrode),str(cluster),subject,minFileName))
