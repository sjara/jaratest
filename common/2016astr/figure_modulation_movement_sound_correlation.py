'''
Script to make a scatter plot of movement modulation index vs modulation index of sound response by choice, for psychometric curve mice and switching mice separately.
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
import figparams
import matplotlib.pyplot as plt
import scipy.stats as stats

qualityList = [1,6]
ISIcutoff = 0.02

# -- Read in databases storing all measurements from psycurve and switching mice -- #
switchingFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

# -- Get movement and sound modulation index for psychometric cells -- #
goodcells_psychometric = (allcells_psychometric.cellQuality.isin(qualityList)) & (allcells_psychometric.ISI <= ISIcutoff)
cellInStr =  (allcells_psychometric.cellInStr==1)
keepAfterDupTest = allcells_psychometric.keep_after_dup_test

cellsToPlot_psychometric = allcells_psychometric[goodcells_psychometric & cellInStr & keepAfterDupTest]

movementModI_psychometric = cellsToPlot_psychometric.movementModI.values
movementModSig_psychometric = cellsToPlot_psychometric.movementModS.values

#For psychometric curve task, choose the center frequency that a cell is more responsive to and plot the modulation index of that frequency
strongerSoundResMid1 = abs(cellsToPlot_psychometric.maxZSoundMid1) > abs(cellsToPlot_psychometric.maxZSoundMid2)
soundModI_psychometric = np.r_[cellsToPlot_psychometric.modIndexMid1[strongerSoundResMid1].values,cellsToPlot_psychometric.modIndexMid2[~strongerSoundResMid1].values]
soundModSig_psychometric = np.r_[cellsToPlot_psychometric.modSigMid1[strongerSoundResMid1].values,cellsToPlot_psychometric.modSigMid2[~strongerSoundResMid1].values] 

movementSelectivePsychometric = (movementModSig_psychometric <= 0.05)
soundModPsychometric = (soundModSig_psychometric <= 0.05)

# -- Get movement and sound modulation index for switching cells -- #
goodcells_switching = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= ISIcutoff)
cellInStr =  (allcells_switching.cellInStr==1)
keepAfterDupTest = allcells_switching.keep_after_dup_test

cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest]

movementModI_switching = cellsToPlot_switching.movementModI.values
movementModSig_switching = cellsToPlot_switching.movementModS.values

soundModI_switching = cellsToPlot_switching.modIndex.values
soundModSig_switching = cellsToPlot_switching.modSig.values

movementSelectiveSwitching = (movementModSig_switching <= 0.05)
soundModSwitching = (soundModSig_switching <= 0.05)

# -- Plot scatter of movment modulation index vs sound modulation index for either task -- #
plt.scatter(movementModI_psychometric, soundModI_psychometric)
plt.xlabel('movment modulation index')
plt.ylabel('modulation index of sound response by choice')
plt.title('Psychometric task')

plt.scatter(movementModI_switching, soundModI_switching)
plt.xlabel('movment modulation index')
plt.ylabel('modulation index of sound response by choice')
plt.title('Switching task')

plt.show()

# -- Stats -- # 
#numCellsPsy = len(cellsToPlot_psychometric)
#numMovSelPsy = sum(movementSelectivePsychometric)
#numSoundModPsy = sum(soundModPsychometric)
rPsy, pValPsy = stats.spearmanr(movementModI_psychometric, soundModI_psychometric)
print '\nPsychometric task: Spearman correlation coefficient between sound response index and movement direction modulation index is:', rPsy, 'p value is:', pValPsy
rSwi, pValSwi = stats.spearmanr(movementModI_switching, soundModI_switching)
print '\nSwitching task: Spearman correlation coefficient between sound response index and movement direction modulation index is:', rSwi, 'p value is:', pValSwi
