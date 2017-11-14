'''
Generate and store intermediate data for plot showing response to same stimulus being modulated under different contingency in the switching tasks. 
Output npz file contains animalName, modulated(boolean vector indicating whether each cell was significantly modulated), and modulationIndex(modulation index for each cell).
Lan Guo20161228
'''
# TO DO
# Include in the database information about what script creates it
# Save cell databases on jarahub

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
import figparams

scriptFullPath = os.path.realpath(__file__)
qualityList = [1,6]
maxZThreshold = 3
ISIcutoff = 0.02

# -- Read in databases storing all measurements from switching mice -- #
switchingFilePath = os.path.join(settings.FIGURESDATA,figparams.STUDY_NAME)
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

# -- Get intermediate data relevant to this subfigure of sound modulation -- #
## Plot all good cells from switcing task ##
goodcells = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= 0.02)
allcells = allcells_switching[goodcells & (allcells_switching.cellInStr==1)] #just look at the good cells THAT ARE IN STR 
sigMod = np.array((allcells.modSig<=0.05), dtype=bool)
dataToPlot = {'modulated':sigMod,'modulationIndex':allcells.modIndex,'animalName':allcells.animalName}

### Save data ###
outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_switching_sound_modulation_all_good_cells.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, sourceSwitching=switchingFilePath, goodCellQuality=qualityList, script=scriptFullPath, **dataToPlot)


## Plot only the good cells responsive to middle freq from switcing task ##
responsiveMidFreqs = abs(allcells_switching.maxZSoundMid)>=maxZThreshold
allcellsResponsive = allcells_switching[goodcells & responsiveMidFreqs & (allcells_switching.cellInStr==1)] # good cells IN STR sound responsive to middle frequency
sigMod = np.array((allcellsResponsive.modSig<=0.05) & (allcellsResponsive.modDir>=1), dtype=bool) 
dataToPlot = {'modulated':sigMod,'modulationIndex':allcellsResponsive.modIndex,'animalName':allcellsResponsive.animalName}

### Save data ###
outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
outputFile = 'summary_switching_sound_modulation_good_cells_responsive_midfreq.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, sourceSwitching=switchingFilePath, maxZThreshold=maxZThreshold, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, script=scriptFullPath, **dataToPlot)
