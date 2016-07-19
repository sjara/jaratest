'''
Plots number of significantly and non-significantly modulated cells from modulation index of -1 to +1. Only using good quality cells (either all_cells file only contain good quality cells or has 'oneCell.quality' indicating whether it's a good cell). 
This plots modulated cells when spikes are aligned to sound onset. -modified 20160303
Generates laserSoundResponsiveCellDB (soundZ score >=3, laserZ score>=3) and modulatedCellDB (mod sig <= 0.05) without considering ISI violations.
Implemented: write to a text file the cell name, cell ID (index in allcells file), frequency modulated, and modulation index (only for the significantly modulated ones). Also write to files sound or laser responsive cells' name, frequency(for sound),and Z score, so can use these files to see which 'center-out' or 'side-in' modulated cells are also sound or laser responsive.
Lan Guo 20160308
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings_2 as settings
from jaratoolbox import ephyscore
import os
import shutil
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
#from jaratoolbox import celldatabase
from jaratoolbox.test.lan.Ephys import celldatabase_quality_vlan as celldatabase
from jaratoolbox.test.lan import test022_plot2afc_given_cell_rew_change as cellplotter
import matplotlib.pyplot as plt
import sys
import importlib

subject = str(sys.argv[1]) #the first argument is the mouse name to tell the script which allcells file to use
allcellsFileName = 'allcells_'+subject
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)

numOfCells = len(allcells.cellDB) #number of cells that were clustered on all sessions clustered

outputDir = '/home/languo/data/ephys/'+subject+'/'

binWidth = 0.020 # Size of each bin in histogram in seconds

clusNum = 12 #Number of clusters that Klustakwik speparated into
numTetrodes = 8 #Number of tetrodes

CellInfo = celldatabase.CellInfo  #This is for creating subdatabase for responsive and modulated cells
soundResponsiveCellDB = celldatabase.CellDatabase()
laserResponsiveCellDB = celldatabase.CellDatabase()
modulatedCellDB = celldatabase.CellDatabase()
modulatedCellDB_laser= celldatabase.CellDatabase()
################################################################################################
##############################-----Minimum Requirements------###################################
################################################################################################
qualityList = [1,6]#[1,4,5,6,7]#range(1,10)
minZVal = 3.0
#maxISIviolation = 0.02
minPValue = 0.05
################################################################################################
################################################################################################

subject = allcells.cellDB[0].animalName
behavSession = ''
processedDir = os.path.join(outputDir,subject+'_stats')
maxZFilename = os.path.join(processedDir,'maxZVal_'+subject+'.txt')
#ISIFilename = os.path.join(processedDir,'ISI_Violations_'+subject+'.txt')
modIFilename = os.path.join(processedDir,'modIndex_alignedToSound_'+subject+'.txt')
modSFilename = os.path.join(processedDir,'modSig_alignedToSound_'+subject+'.txt')
maxZLaserFilename = os.path.join(processedDir,'maxZVal_laser_'+subject+'.txt')

class nestedDict(dict):#This is for maxZDict
    def __getitem__(self, item):
        try:
            return super(nestedDict, self).__getitem__(item)
        except KeyError:
            value = self[item] = type(self)()
            return value


maxZFile = open(maxZFilename, 'r')
#ISIFile = open(ISIFilename, 'r')
modIFile = open(modIFilename, 'r')
modSFile = open(modSFilename, 'r')
maxZLaserFile = open(maxZLaserFilename, 'r')

maxZDict = nestedDict()
behavName = ''
for line in maxZFile:
    behavLine = line.split(':')
    freqLine = line.split()
    if (behavLine[0] == 'Behavior Session'):
        behavName = behavLine[1][:-1]
    else:
        maxZDict[behavName][freqLine[0]] = freqLine[1].split(',')[0:-1]

maxZLaserDict = nestedDict()
behavName = ''
for line in maxZLaserFile:
    behavLine = line.split(':')
    
    if (behavLine[0] == 'Behavior Session'):
        behavName = behavLine[1][:-1]
    else:
        maxZLaserDict[behavName] = line.split(',')[0:-1]

'''
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

modIDict = nestedDict() #stores all the modulation indices
modSigDict = nestedDict() #stores the significance of the modulation of each cell
#modDirectionScoreDict = {} #stores the score of how often the direction of modulation changes
behavName = ''
for line in modIFile:
    behavLine = line.split(':')
    freqLine = line.split()
    if (behavLine[0] == 'Behavior Session'):
        behavName = behavLine[1][:-1]
    else:
        modIDict[behavName][freqLine[0]] = [float(x) for x in freqLine[1].split(',')[0:-1]]

for line in modSFile:
    behavLine = line.split(':')
    freqLine = line.split()
    if (behavLine[0] == 'Behavior Session'):
        behavName = behavLine[1][:-1]
    else:
        modSigDict[behavName][freqLine[0]] = [float(x) for x in freqLine[1].split(',')[0:-1]]

'''
for line in modIFile:
    splitLine = line.split(':')
    if (splitLine[0] == 'Behavior Session'):
        behavName = splitLine[1][:-1]
    else:
        line.split
    elif (splitLine[0] == 'modI'):
        modIDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
    elif (splitLine[0] == 'modSig'):
        modSigDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]


    #elif (splitLine[0] == 'modDir'):
        #modDirectionScoreDict[behavName] = [float(x) for x in splitLine[1].split(',')[0:-1]]
'''


sigModIDict={}
sigModIDict_laser={}
soundResponsiveCellDict={}
laserResponsiveCellDict={}

#ISIFile.close()
maxZFile.close()
maxZLaserFile.close()
modIFile.close()
modSFile.close()
########################CHOOSE WHICH CELLS TO PLOT################################################
modIndexArray = []
modIndexArray_sound_laser=[]
modIndexArray_laser=[]

for cellID in range(0,numOfCells):
    oneCell = allcells.cellDB[cellID]

    subject = oneCell.animalName
    behavSession = oneCell.behavSession
    ephysSession = oneCell.ephysSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    clusterQuality = oneCell.quality


    if clusterQuality not in qualityList:
        continue
    
    if behavSession not in maxZDict:
        continue
    elif behavSession not in modIDict:
        continue
    #elif ephysSession not in ISIDict:
        #continue

    clusterNumber = (tetrode-1)*clusNum+(cluster-1)
    #midFreq = minTrialDict[behavSession][0]
    #Here we are using all frequencies tested (usually two freqs per recording session), but one cell will not likely be responsive (Zscore outside 3) for both low and high frequencies.
    
    for freq in maxZDict[behavSession]:
        #if ((abs(float(maxZDict[behavSession][freq][clusterNumber])) < minZVal) | (ISIDict[ephysSession][tetrode-1][cluster-1] > maxISIviolation)):
       
        #####sound responsive cells that are also modulated by reward during sound presentation
        if (abs(float(maxZDict[behavSession][freq][clusterNumber]))>= minZVal):
            modIndexArray.append([modIDict[behavSession][freq][clusterNumber],modSigDict[behavSession][freq][clusterNumber]]) #these are all sound-responsive cells
            oneCell=CellInfo(animalName=subject,
                             ephysSession = ephysSession,
                             tetrode=tetrode,
                             cluster=cluster,
                             behavSession = behavSession,
                             quality=clusterQuality)
            cellName=subject+'_'+behavSession+'_'+str(tetrode)+'_'+str(cluster)
            soundResponsiveCellDB.append(oneCell)
            soundResponsiveCellDict.update({cellName:[freq,maxZDict[behavSession][freq][clusterNumber]]})
            if (modSigDict[behavSession][freq][clusterNumber]<=minPValue):
                modIndexThisCell=modIDict[behavSession][freq][clusterNumber]
                sigModIDict.update({cellName:[cellID,freq,modIndexThisCell]})
                modulatedCellDB.append(oneCell) #significantly modulated cells that are sound responsive
        #####laser responsive cells that are also modulated by reward during sound presentation
        if (abs(float(maxZLaserDict[behavSession][clusterNumber]))>= minZVal):
            modIndexArray_laser.append([modIDict[behavSession][freq][clusterNumber],modSigDict[behavSession][freq][clusterNumber]])
            oneCell=CellInfo(animalName=subject,
                             ephysSession = ephysSession,
                             tetrode=tetrode,
                             cluster=cluster,
                             behavSession = behavSession,
                             quality=clusterQuality)
            cellName=subject+'_'+behavSession+'_'+str(tetrode)+'_'+str(cluster)
            laserResponsiveCellDB.append(oneCell)
            laserResponsiveCellDict.update({cellName:maxZDict[behavSession][freq][clusterNumber]})
            if (modSigDict[behavSession][freq][clusterNumber]<=minPValue):
                modIndexThisCell=modIDict[behavSession][freq][clusterNumber]
                sigModIDict_laser.update({cellName:[cellID,freq,modIndexThisCell]})
                modulatedCellDB_laser.append(oneCell) #significantly modulated cells that are laser responsive

            #####sound and laser responsive cells that are also modulated by reward during sound presentation
        if (abs(float(maxZLaserDict[behavSession][clusterNumber]))>= minZVal)&(abs(float(maxZDict[behavSession][freq][clusterNumber]))>= minZVal):
            modIndexArray_sound_laser.append([modIDict[behavSession][freq][clusterNumber],modSigDict[behavSession][freq][clusterNumber]])

        else:
            continue

        #print 'behavior ',behavSession,' tetrode ',tetrode,' cluster ',cluster
    #print responsiveCellDB, modulatedCellDB, sigModI
##########################THIS IS TO PLOT HISTOGRAM################################################
modIndexDict={'sound-responsive':modIndexArray,'laser-responsive':modIndexArray_laser,'sound-and-laser-responsive':modIndexArray_sound_laser}

for (key,modIndexArray) in modIndexDict.items():
    modIndBinVec = np.arange(-1,1,binWidth)
    binModIndexArraySig = np.empty(len(modIndBinVec))
    binModIndexArrayNonSig = np.empty(len(modIndBinVec))
    maxMI=0
    for binInd in range(len(modIndBinVec)-1):
        binTotalSig = 0
        binTotalNonSig = 0
        for modIndSig in modIndexArray:
            if ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1]) and (modIndSig[1] <= minPValue)):
                binTotalSig += 1
            elif ((modIndSig[0] >= modIndBinVec[binInd]) and (modIndSig[0] < modIndBinVec[binInd+1])):
                binTotalNonSig += 1
            maxMI = max(maxMI,abs(modIndSig[0]))
        binModIndexArraySig[binInd] = binTotalSig
        binModIndexArrayNonSig[binInd] = binTotalNonSig
    binModIndexArraySig[-1] = 0  #why is this??
    binModIndexArrayNonSig[-1] = 0 #why is this??
    sigNum=int(sum(binModIndexArraySig))
    cellNum=len(modIndexArray)
    print 'number of cells: ',cellNum

    plt.clf() 

    plt.bar(modIndBinVec,binModIndexArraySig,width = binWidth, color = 'b')
    plt.bar(modIndBinVec,binModIndexArrayNonSig,width = binWidth, color = 'g',bottom = binModIndexArraySig)
    plt.xlim((-(maxMI+binWidth),maxMI+binWidth))
    plt.xlabel('Modulation Index')
    plt.ylabel('Number of Cells')
    plt.title('SOUND ONSET %s %s cells, %s cells modulated' %(cellNum,key,sigNum))
    plt.gcf().set_size_inches((8.5,11))
    figformat = 'png'
    filename = 'modIndex_%s_sound_onset_%s.%s'%(subject,key,figformat)
    fulloutputDir = processedDir
    fullFileName = os.path.join(fulloutputDir,filename)
    directory = os.path.dirname(fulloutputDir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName,format=figformat)



####Write all significantly modulated cells and their mod index in a text file###
sigModI_soundresponsive_file = open('%s/%s.txt' % (fulloutputDir,'sigMod_soundOnset_soundresponsive'), 'w')
for (key,value) in sorted(sigModIDict.items()):
    sigModI_soundresponsive_file.write('%s:' %key)
    sigModI_soundresponsive_file.write('%d %s %f\n' %(value[0],value[1],value[2]))
sigModI_soundresponsive_file.close()

sigModI_laserresponsive_file = open('%s/%s.txt' % (fulloutputDir,'sigMod_soundOnset_laserresponsive'), 'w')
for (key,value) in sorted(sigModIDict_laser.items()):
    sigModI_laserresponsive_file.write('%s:' %key)
    sigModI_laserresponsive_file.write('%d %s %f\n' %(value[0],value[1],value[2]))
sigModI_laserresponsive_file.close()

#####Write all sound or laser responsive cells and their Z score to text files#####
soundResponsive_file = open('%s/%s.txt' % (fulloutputDir,'soundResponsive_CellNameFreqZscore'), 'w')
for (key,value) in sorted(soundResponsiveCellDict.items()):
    soundResponsive_file.write('%s:' %key)
    soundResponsive_file.write('%s %s\n' %(value[0],value[1]))
soundResponsive_file.close()

laserResponsive_file = open('%s/%s.txt' % (fulloutputDir,'laserResponsive_CellNameZscore'), 'w')
for (key,value) in sorted(laserResponsiveCellDict.items()):
    laserResponsive_file.write('%s:' %key)
    laserResponsive_file.write('%s\n' %value)
laserResponsive_file.close()

####Create plots of modulated cells in a new folder inside the stats folder######
numOfModulatedCells = len(modulatedCellDB)
for cellID in range(0,numOfModulatedCells):
    oneCell = modulatedCellDB[cellID]
    
    #####make new plots######
    dstDir = processedDir+'/all_cells_SoundOnset_sig_modulated/'
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    figname='{0}_{1}_TT{2}_c{3}_{4}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,'sound-onset')
    full_fig_path=os.path.join(dstDir, figname)
    if not os.path.exists(full_fig_path):
        cellplotter.plot_rew_change_per_cell(oneCell,trialLimit=[],alignment='sound')
        plt.savefig(full_fig_path, format = 'png')
    
    
    figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,'sound-onset','right')
    full_fig_path=os.path.join(dstDir, figname)

    if not os.path.exists(full_fig_path):
        cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=[],alignment='sound',choiceSide='right')
        plt.savefig(full_fig_path, format = 'png')

   
    figname='{0}_{1}_TT{2}_c{3}_{4}_{5}'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,'sound-onset','left')
    full_fig_path=os.path.join(dstDir, figname)
    if not os.path.exists(full_fig_path):
        cellplotter.plot_rew_change_byblock_per_cell(oneCell,trialLimit=[],alignment='sound',choiceSide='left')
        plt.savefig(full_fig_path, format = 'png')
    


    '''
    behavSession = oneCell.behavSession
    date = behavSession[0:4]+'-'+behavSession[4:6]+'-'+behavSession[6:8]
    ephysSession = oneCell.ephysSession
    tetrode = oneCell.tetrode
    cluster = oneCell.cluster
    #clusterQuality = oneCell.quality[cluster-1]

    oldFileNameCluster = 'TT'+str(tetrode)+'Cluster'+str(cluster)+'.png'
    oldFileName2afcEachType ='TT'+str(tetrode)+'Cluster'+str(cluster)+'_2afc plot_each_type'+'.png'
    oldFileNameTuning = 'TT'+str(tetrode)+'Cluster'+str(cluster)+'sorted_raster_more_sounds'+'.png'
    oldFileNameLeft ='TT'+str(tetrode)+'Cluster'+str(cluster)+'_2afc plot_eachblock_eachtype_left'+'.png'
    oldFileNameRight ='TT'+str(tetrode)+'Cluster'+str(cluster)+'_2afc plot_eachblock_eachtype_right'+'.png'
    newFileNameCluster = subject+'_'+behavSession+'TT'+str(tetrode)+'C'+str(cluster)+'.png'
    newFileName2afcEachType = subject+'_'+behavSession+'TT'+str(tetrode)+'C'+str(cluster)+'_2afc_plot_each_type'+'.png'
    newFileNameTuning = subject+'_'+behavSession+'TT'+str(tetrode)+'C'+str(cluster)+'_sorted_raster_tuning'+'.png'
    newFileNameLeft =subject+'_'+behavSession+'TT'+str(tetrode)+'C'+str(cluster)+'_2afc plot_eachblock_eachtype_left'+'.png'
    newFileNameRight =subject+'_'+behavSession+'TT'+str(tetrode)+'C'+str(cluster)+'_2afc plot_eachblock_eachtype_right'+'.png'

    srcDir = os.path.join(outputDir, 'multisession_'+date+'_'+'site1')
    dstDir = os.path.join(processedDir, 'sound_responsive_modulated')
    if not os.path.exists(dstDir):
        os.mkdir(dstDir)
    
    srcFile = os.path.join(srcDir, oldFileNameCluster)
    shutil.copy(srcFile,dstDir)
    dstFile = os.path.join(dstDir, oldFileNameCluster)
    newDstFileName = os.path.join(dstDir, newFileNameCluster)
    os.rename(dstFile, newDstFileName)

    srcFile = os.path.join(srcDir, oldFileName2afcEachType)
    shutil.copy(srcFile,dstDir)
    dstFile = os.path.join(dstDir, oldFileName2afcEachType)
    newDstFileName = os.path.join(dstDir, newFileName2afcEachType)
    os.rename(dstFile, newDstFileName)

    srcFile = os.path.join(srcDir, oldFileNameTuning)
    shutil.copy(srcFile,dstDir)
    dstFile = os.path.join(dstDir, oldFileNameTuning)
    newDstFileName = os.path.join(dstDir, newFileNameTuning)
    os.rename(dstFile, newDstFileName)
    
    srcFile = os.path.join(srcDir, oldFileNameLeft)
    shutil.copy(srcFile,dstDir)
    dstFile = os.path.join(dstDir, oldFileNameLeft)
    newDstFileName = os.path.join(dstDir, newFileNameLeft)
    os.rename(dstFile, newDstFileName)

    srcFile = os.path.join(srcDir, oldFileNameRight)
    shutil.copy(srcFile,dstDir)
    dstFile = os.path.join(dstDir, oldFileNameRight)
    newDstFileName = os.path.join(dstDir, newFileNameRight)
    os.rename(dstFile, newDstFileName)
    '''
