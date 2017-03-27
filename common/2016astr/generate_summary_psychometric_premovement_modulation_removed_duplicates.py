'''
Generate and store intermediate data for plot showing activity before center-out exit for trials with same stimulus (mid freq) being modulated under different contingency in the psychometric tasks. 
Output npz file contains animalName, modulated(boolean vector indicating whether each cell was significantly modulated), and modulationIndex(modulation index for each cell).
DONE AFTER REMOVING DUPLICATES
Use the modulation index and significance of the mid freq eliciting a stronger sound response (based on max Z).
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

FIGNAME = 'premovement_modulation_psychometric'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(dataDir):
    os.mkdir(dataDir)

# -- Read in databases storing all measurements from psychometric mice -- #
psychometricFilePath = os.path.join(settings.FIGURESDATA,figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_extra_mod_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

# -- Get intermediate data relevant to this subfigure of sound modulation -- #
## Plot all good cells from switcing task ##
goodcells = (allcells_psychometric.cellQuality.isin(qualityList)) & (allcells_psychometric.ISI <= ISIcutoff)
cellsInStr = allcells_psychometric.cellInStr==1
keepAfterDupTest = allcells_psychometric.keep_after_dup_test
allcells = allcells_psychometric[goodcells & cellsInStr & keepAfterDupTest] #just look at the good cells THAT ARE IN STR 
strongerSoundResMid1 = abs(allcells.maxZSoundMid1) > abs(allcells.maxZSoundMid2)
modIStrongerSoundRes = np.r_[allcells['modIndMid1_-0.1-0s_center-out'][strongerSoundResMid1].values,allcells['modIndMid2_-0.1-0s_center-out'][~strongerSoundResMid1].values]
modSigStrongerSoundRes = np.r_[allcells['modSigMid1_-0.1-0s_center-out'][strongerSoundResMid1].values,allcells['modSigMid2_-0.1-0s_center-out'][~strongerSoundResMid1].values] 
#sigMod = np.array(((allcells.modSigMid1<=0.05)|(allcells.modSigMid2<=0.05)), dtype=bool)
sigMod = np.array((modSigStrongerSoundRes <= 0.05), dtype=bool)

dataToPlot = {'modulated':sigMod,'modulationIndex':modIStrongerSoundRes,'animalName':allcells.animalName}

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_psychometric_premovement_modulation_all_good_cells_remove_dup.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath, sourcePsychometric=psychometricFilePath, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, removedDuplicates=removedDuplicates, script=scriptFullPath, **dataToPlot)


## Plot only the good cells responsive to middle freq from psychometric task ##
responsiveMidFreqs = (abs(allcells_psychometric.maxZSoundMid1)>=maxZThreshold) | (abs(allcells_psychometric.maxZSoundMid2)>=maxZThreshold)
allcellsResponsive = allcells_psychometric[goodcells & cellsInStr & keepAfterDupTest & responsiveMidFreqs] # good cells IN STR sound responsive to middle frequency
strongerSoundResMid1 = abs(allcellsResponsive.maxZSoundMid1) > abs(allcellsResponsive.maxZSoundMid2)
modIStrongerSoundRes = np.r_[allcellsResponsive['modIndMid1_-0.1-0s_center-out'][strongerSoundResMid1].values,allcellsResponsive['modIndMid2_-0.1-0s_center-out'][~strongerSoundResMid1].values]
modSigStrongerSoundRes = np.r_[allcellsResponsive['modSigMid1_-0.1-0s_center-out'][strongerSoundResMid1].values,allcellsResponsive['modSigMid2_-0.1-0s_center-out'][~strongerSoundResMid1].values]
sigMod = np.array((modSigStrongerSoundRes <= 0.05), dtype=bool)

dataToPlot = {'modulated':sigMod,'modulationIndex':modIStrongerSoundRes,'animalName':allcellsResponsive.animalName}

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_psychometric_premovement_modulation_good_cells_responsive_midfreqs_remove_dup.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath, sourcePsychometric=psychometricFilePath, maxZThreshold=maxZThreshold, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, removedDuplicates=removedDuplicates, script=scriptFullPath, **dataToPlot)

'''
## Plot only the good cells selective to movement direction ##
movementSelective = allcells_psychometric.movementModS<=0.05
allcellsMovementSel = allcells_psychometric[goodcells & cellsInStr & keepAfterDupTest & movementSelective] # good cells IN STR selective to movement direction
strongerSoundResMid1 = abs(allcellsMovementSel.maxZSoundMid1) > abs(allcellsMovementSel.maxZSoundMid2)
modIStrongerSoundRes = np.r_[allcellsMovementSel['modIndMid1_-0.1-0s_center-out'][strongerSoundResMid1].values,allcellsMovementSel['modIndMid2_-0.1-0s_center-out'][~strongerSoundResMid1].values]
modSigStrongerSoundRes = np.r_[allcellsMovementSel['modSigMid1_-0.1-0s_center-out'][strongerSoundResMid1].values,allcellsMovementSel['modSigMid2_-0.1-0s_center-out'][~strongerSoundResMid1].values] 
sigMod = np.array((modSigStrongerSoundRes <= 0.05), dtype=bool)

dataToPlot = {'modulated':sigMod,'modulationIndex':modIStrongerSoundRes,'animalName':allcellsMovementSel.animalName}

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_psychometric_premovement_modulation_good_cells_movement_selective_remove_dup.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath, sourcePsychometric=psychometricFilePath, maxZThreshold=maxZThreshold, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, removedDuplicates=removedDuplicates, script=scriptFullPath, **dataToPlot)
'''
