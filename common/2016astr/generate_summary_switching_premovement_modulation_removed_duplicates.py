'''
Generate and store intermediate data for plot showing activity before center-out exit for trials with same stimulus (mid freq) being modulated under different contingency in the switching tasks. 
Output npz file contains animalName, modulated(boolean vector indicating whether each cell was significantly modulated), and modulationIndex(modulation index for each cell).
DONE AFTER REMOVING DUPLICATES
Lan Guo 20170323
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
import figparams

scriptFullPath = os.path.realpath(__file__)
qualityList = [1,6]
maxZThreshold = 3
ISIcutoff = 0.02
removedDuplicates = True

FIGNAME = 'premovement_modulation_switching'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(dataDir):
    os.mkdir(dataDir)

# -- Read in databases storing all measurements from switching mice -- #
switchingFilePath = os.path.join(settings.FIGURESDATA,figparams.STUDY_NAME)
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

# -- Get intermediate data relevant to this subfigure of sound modulation -- #
## Plot all good cells from switcing task ##
goodcells = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= ISIcutoff)
cellsInStr = allcells_switching.cellInStr==1
keepAfterDupTest = allcells_switching.keep_after_dup_test
allcells = allcells_switching[goodcells & cellsInStr & keepAfterDupTest] #just look at the good cells THAT ARE IN STR 
sigMod = np.array((allcells['modSig_-0.1-0s_center-out']<=0.05) & (allcells['modDir_-0.1-0s_center-out']>=1), dtype=bool) 
dataToPlot = {'modulated':sigMod,'modulationIndex':allcells.modIndex,'animalName':allcells.animalName}

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_switching_premovement_modulation_all_good_cells_remove_dup.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath, sourceSwitching=switchingFilePath, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, removedDuplicates=removedDuplicates, script=scriptFullPath, **dataToPlot)


## Plot only the good cells responsive to middle freq from switcing task ##
responsiveMidFreqs = abs(allcells_switching.maxZSoundMid)>=maxZThreshold
allcellsResponsive = allcells_switching[goodcells & cellsInStr & keepAfterDupTest & responsiveMidFreqs] # good cells IN STR sound responsive to middle frequency
sigMod = np.array((allcellsResponsive['modSig_-0.1-0s_center-out']<=0.05) & (allcellsResponsive['modDir_-0.1-0s_center-out']>=1), dtype=bool) 
dataToPlot = {'modulated':sigMod,'modulationIndex':allcellsResponsive.modIndex,'animalName':allcellsResponsive.animalName}

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_switching_premovement_modulation_good_cells_responsive_midfreq_remove_dup.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath, sourceSwitching=switchingFilePath, maxZThreshold=maxZThreshold, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, removedDuplicates=removedDuplicates, script=scriptFullPath, **dataToPlot)


## Plot only the good cells selective to movement direction ##
movementSelective = allcells_switching.movementModS<=0.05
allcellsMovementSel = allcells_switching[goodcells & cellsInStr & keepAfterDupTest & movementSelective] # good cells IN STR selective to movement direction
sigMod = np.array((allcellsMovementSel['modSig_-0.1-0s_center-out']<=0.05) & (allcellsMovementSel['modDir_-0.1-0s_center-out']>=1), dtype=bool) 
dataToPlot = {'modulated':sigMod,'modulationIndex':allcellsMovementSel.modIndex,'animalName':allcellsMovementSel.animalName}

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_switching_premovement_modulation_good_cells_movement_selective_remove_dup.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath, sourceSwitching=switchingFilePath, maxZThreshold=maxZThreshold, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, removedDuplicates=removedDuplicates, script=scriptFullPath, **dataToPlot)
