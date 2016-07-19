'''
Plots 2afc rasters aligned to sound-onset, center-out, and side-in for laser responsive cells. *Laser-responsive being Z score of 2 or bigger.* 
Only using good quality cells (either all_cells file only contain good quality cells or has 'oneCell.quality' indicating whether it's a good cell). without considering ISI violations.
-Lan Guo 20160517
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
from jaratoolbox import ephyscore
import os
import shutil
import numpy as np
from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
from jaratoolbox.test.lan import test022_plot2afc_given_cell_rew_change as cellplotter
reload(cellplotter)
import matplotlib.pyplot as plt
import sys
import importlib
import codecs


subject = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+subject
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

outputDir = '/home/languo/data/ephys/'+subject+'/'

#binWidth = 0.020 # Size of each bin in histogram in seconds

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

#CellInfo = celldatabase.CellInfo  
LaserResponsiveCellDB = celldatabase.CellDatabase()


################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]
minZVal = 2.0
#maxISIviolation = 0.02
minPValue = 0.05
################################################################################################
################################################################################################

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(outputDir,subject+'_stats')
maxZLaserFilename = os.path.join(processedDir,'maxZVal_laser_'+subject+'.txt')
#ISIFilename = os.path.join(processedDir,'ISI_Violations_'+subject+'.txt')

class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


maxZLaserFile = open(maxZLaserFilename, 'r')
maxZDictLaser = nestedDict()
behavName = ''
for line in maxZLaserFile:
    if line.startswith(codecs.BOM_UTF8):
            line = line[3:]    
    if (line.split(':')[0] == 'Behavior Session'):
        behavName = line.split(':')[1][:-1]
    else:
        maxZDictLaser[behavName] = line.split(',')[0:-1]


'''
ISIFile = open(ISIFilename, 'r')
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


#ISIFile.close()
maxZLaserFile.close()
laserResponsiveDict={}
########################CHOOSE WHICH CELLS TO PLOT################################################

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]
    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    clusterQuality = oneCell.quality

    if clusterQuality not in qualityList:
        continue
    elif behavSession not in maxZDictLaser:
        continue

    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
       
    if (abs(float(maxZDictLaser[behavSession][clusterNumber]))>= minZVal):
        LaserResponsiveCellDB.append(oneCell)
        cellName=subject+'_'+behavSession+'_'+str(tetrode)+'_'+str(cluster)
        laserResponsiveDict.update({cellName:maxZDictLaser[behavSession][clusterNumber]})
    else:
        continue

    #print len(LaserResponsiveCellDB)


numOfLaserResponsiveCells = len(LaserResponsiveCellDB)
print numOfLaserResponsiveCells


#####make new folder######
dstDir = processedDir+'/laser_responsive_2.5Z/'
if not os.path.exists(dstDir):
    os.makedirs(dstDir)

 
#####Write all laser responsive cells and their Z score to a text file#####
   
laserResponsiveFilename='laser_responsive_2.5Z'
laserResponsive_file = open('%s/%s.txt' % (dstDir,laserResponsiveFilename), 'w')
for (key,value) in sorted(laserResponsiveDict.items()):
    laserResponsive_file.write('%s:' %key)
    laserResponsive_file.write('%s\n' %value)
laserResponsive_file.close()



####Plot 2afc rasters of laser-responsive cells to a new folder inside the stats folder and rename them. Also copy raster plots of laser/sound response to this folder. ####

for cellID in range(0,numOfLaserResponsiveCells):
    oneCell = LaserResponsiveCellDB[cellID]
   
    for alignment in ['sound','center-out','side-in']:

        figname='{0}_{1}_TT{2}_c{3}_{4}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment)
        full_fig_path=os.path.join(dstDir, figname)
        if not os.path.exists(full_fig_path):
            cellplotter.plot_rew_change_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment=alignment)
            plt.savefig(full_fig_path, format = 'png')

        figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,'right')
        full_fig_path=os.path.join(dstDir, figname)
        if not os.path.exists(full_fig_path):
            cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment=alignment,choiceSide='right')
            plt.savefig(full_fig_path, format = 'png')

        figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,'left')
        full_fig_path=os.path.join(dstDir, figname)
        if not os.path.exists(full_fig_path):
            cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=oneCell.trialLimit,alignment=alignment,choiceSide='left')
            plt.savefig(full_fig_path, format = 'png')


    behavSession = oneCell.behavSession
    date = behavSession[0:4]+'-'+behavSession[4:6]+'-'+behavSession[6:8]
    ephysSession = oneCell.ephysSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
  
    oldFileNameCluster = 'TT'+str(tetrode)+'Cluster'+str(cluster)+'.png'
    newFileNameCluster = behavSession+'TT'+str(tetrode)+'C'+str(cluster)+'.png'
    
    srcDir = os.path.join(outputDir, 'multisession_'+date+'_'+'site1')
        
    srcFile = os.path.join(srcDir, oldFileNameCluster)
    shutil.copy(srcFile,dstDir)
    dstFile = os.path.join(dstDir, oldFileNameCluster)
    newDstFileName = os.path.join(dstDir, newFileNameCluster)
    os.rename(dstFile, newDstFileName)

 

