'''
Script to make a scatter plot of movement modulation index vs modulation index of sound response by choice, for psychometric curve mice and switching mice separately.
'''

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import extraplots
import figparams
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib
import matplotlib.gridspec as gridspec

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'supp_sound_movement_modulation_corr' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,3]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1
labelPosX = [0.07, 0.5]   # Horiz position for panel labels
labelPosY = [0.9]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(left=0.15, right=0.95,top=0.85, bottom=0.2, wspace=0.5, hspace=0.1)
qualityList = [1,6]
ISIcutoff = 0.02
maxZThreshold = 3

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
responsiveMidFreqs = (abs(allcells_psychometric.maxZSoundMid1)>=maxZThreshold) | (abs(allcells_psychometric.maxZSoundMid2)>=maxZThreshold)
#cellsToPlot_psychometric = allcells_psychometric[goodcells_psychometric & cellInStr & keepAfterDupTest]
cellsToPlot_psychometric = allcells_psychometric[goodcells_psychometric & cellInStr & keepAfterDupTest & responsiveMidFreqs]
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
responsiveMidFreqs = abs(allcells_switching.maxZSoundMid)>=maxZThreshold

#cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest]
cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest & responsiveMidFreqs]

movementModI_switching = cellsToPlot_switching.movementModI.values
movementModSig_switching = cellsToPlot_switching.movementModS.values

soundModI_switching = cellsToPlot_switching.modIndex.values
soundModSig_switching = cellsToPlot_switching.modSig.values

movementSelectiveSwitching = (movementModSig_switching <= 0.05)
soundModSwitching = (soundModSig_switching <= 0.05)

# -- Panel A: Plot scatter of movement modulation index vs sound modulation index for psychometric -- #
ax1 = plt.subplot(gs[:,0])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(np.abs(movementModI_psychometric), np.abs(soundModI_psychometric), marker='o', linestyle='none', mec='grey', mfc='none')
plt.xlabel('Movement modulation \nby direction',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice',fontsize=fontSizeLabels)
plt.title('Sound discrimination task')
plt.xlim([-0.1,1.1])
plt.ylim([-0.1,0.7])
extraplots.boxoff(plt.gca())

# -- Panel B: Plot scatter of movement modulation index vs sound modulation index for switching -- #
ax2 = plt.subplot(gs[:,1])
ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(np.abs(movementModI_switching), np.abs(soundModI_switching), marker='o', linestyle='none', mec='grey', mfc='none')
plt.xlabel('Movement modulation \nby direction',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice',fontsize=fontSizeLabels)
plt.title('Switching task')
plt.xlim([-0.1,1.1])
plt.ylim([-0.1,0.7])
extraplots.boxoff(plt.gca())
plt.show()

# -- Stats -- # 
#numCellsPsy = len(cellsToPlot_psychometric)
#numMovSelPsy = sum(movementSelectivePsychometric)
#numSoundModPsy = sum(soundModPsychometric)
print 'Number of cells for psychometric:', len(cellsToPlot_psychometric)
print 'Number of cells for switching:', len(cellsToPlot_switching)
rPsy, pValPsy = stats.spearmanr(np.abs(movementModI_psychometric), np.abs(soundModI_psychometric))
print '\nUSING ABSOLUTE VALUES - Psychometric task: Spearman correlation coefficient between sound response index and movement direction modulation index is:', rPsy, 'p value is:', pValPsy
rPsy, pValPsy = stats.spearmanr(movementModI_psychometric, soundModI_psychometric)
print '\nPsychometric task: Spearman correlation coefficient between sound response index and movement direction modulation index is:', rPsy, 'p value is:', pValPsy

rSwi, pValSwi = stats.spearmanr(np.abs(movementModI_switching), np.abs(soundModI_switching))
print '\nUSING ABSOLUTE VALUES - Switching task: Spearman correlation coefficient between sound response index and movement direction modulation index is:', rSwi, 'p value is:', pValSwi
rSwi, pValSwi = stats.spearmanr(movementModI_switching, soundModI_switching)
print '\nSwitching task: Spearman correlation coefficient between sound response index and movement direction modulation index is:', rSwi, 'p value is:', pValSwi

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
