import allcells_test055_quality as allcells
from jaratoolbox import settings
import os

#oldList = os.listdir('/home/billywalker/Pictures/raster_hist/test055/tmpFolder/low_middle_freq')

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

qualityList = [1]
minZVal = 3.0

subject = allcells.cellDB[0].animalName
processedDir = os.path.join(settings.EPHYS_PATH,subject+'_processed')
maxZFilename = os.path.join(processedDir,'maxZVal.txt')
minPerfFilename = os.path.join(processedDir,'minPerformance.txt')
minTrialFilename = os.path.join(processedDir,'minTrial.txt')

maxZFile = open(maxZFilename, 'r')
minPerfFile = open(minPerfFilename, 'r')
minTrialFile = open(minTrialFilename, 'r')


minPerfFile.readline()
minPerfList=minPerfFile.read().split()


minTrialFile.readline()
minTrialFile.readline()
minTrialDict= {}
for lineCount,line in enumerate(minTrialFile):
    minTrialStr = line.split(':')
    trialFreq = minTrialStr[1].split()
    minTrialDict.update({minTrialStr[0][1:]:trialFreq})


maxZFile.readline()
maxZDict = {}
for lineCount,line in enumerate(maxZFile):
    maxZStr = line.split()
    zVal = maxZStr[1].split(',')
    maxZDict.update({maxZStr[0]:zVal})

maxZFile.close()
minPerfFile.close()
minTrialFile.close()

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    

    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
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
    
    print behavSession



'''
for ind,f in enumerate(oldList):
    fileParts = f.split('_')
    freq = fileParts[5].split('.')[0]
    os.system('cp /home/billywalker/Pictures/raster_hist/test055/%s/rast_test055_%s_%s_%s.png /home/billywalker/Pictures/raster_hist/test055/newTmpFolder/low_middle_freq' % (freq,fileParts[2],freq,fileParts[3]))
'''

