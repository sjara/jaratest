'''
Script to make a scatter plot of sound modulation index (by choice) vs waveform params, for psychometric curve mice and switching mice separately.
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
figFilename = 'supp_sound_mod_waveform_corr' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,7]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1
labelPosX = [0.07, 0.47]   # Horiz position for panel labels
labelPosY = [0.9, 0.5]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,2)
gs.update(left=0.15, right=0.95,top=0.9, bottom=0.15, wspace=0.5, hspace=0.5)
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

spkWidth_psychometric = 1000*(cellsToPlot_psychometric.peakKTime - cellsToPlot_psychometric.peakCapTime).values
NatoKRatio_psychometric = (np.abs(cellsToPlot_psychometric.peakNaAmp) / np.abs(cellsToPlot_psychometric.peakKAmp)).values

#For psychometric curve task, choose the center frequency that a cell is more responsive to and plot the modulation index of that frequency
strongerSoundResMid1 = abs(cellsToPlot_psychometric.maxZSoundMid1) > abs(cellsToPlot_psychometric.maxZSoundMid2)
soundModI_psychometric = np.r_[cellsToPlot_psychometric.modIndexMid1[strongerSoundResMid1].values,cellsToPlot_psychometric.modIndexMid2[~strongerSoundResMid1].values]
soundModSig_psychometric = np.r_[cellsToPlot_psychometric.modSigMid1[strongerSoundResMid1].values,cellsToPlot_psychometric.modSigMid2[~strongerSoundResMid1].values] 

soundModPsychometric = (soundModSig_psychometric <= 0.05)

# -- Get movement and sound modulation index for switching cells -- #
goodcells_switching = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= ISIcutoff)
cellInStr =  (allcells_switching.cellInStr==1)
keepAfterDupTest = allcells_switching.keep_after_dup_test
responsiveMidFreqs = abs(allcells_switching.maxZSoundMid)>=maxZThreshold
#cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest]
cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest & responsiveMidFreqs]

spkWidth_switching = 1000*(cellsToPlot_switching.peakKTime - cellsToPlot_switching.peakCapTime).values
NatoKRatio_switching = (np.abs(cellsToPlot_switching.peakNaAmp) / np.abs(cellsToPlot_switching.peakKAmp)).values

soundModI_switching = cellsToPlot_switching.modIndex.values
soundModSig_switching = cellsToPlot_switching.modSig.values

soundModSwitching = (soundModSig_switching <= 0.05)


# -- Panel A: Plot scatter of movment modulation index vs sound modulation index for psychometric -- #
ax1 = plt.subplot(gs[0,0])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(spkWidth_psychometric, np.abs(soundModI_psychometric), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(spkWidth_psychometric[soundModPsychometric], np.abs(soundModI_psychometric[soundModPsychometric]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Spike width (ms)',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice',fontsize=fontSizeLabels)
plt.title('Psychometric')
#plt.xlim([-1.1,1.1])
plt.ylim([-0.1,0.5])
extraplots.boxoff(plt.gca())

# -- Panel B: Plot scatter of movment modulation index vs sound modulation index for switching -- #
ax2 = plt.subplot(gs[0,1])
ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(NatoKRatio_psychometric, np.abs(soundModI_psychometric), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(NatoKRatio_psychometric[soundModPsychometric], np.abs(soundModI_psychometric[soundModPsychometric]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Na peak to K peak ratio (log)',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice',fontsize=fontSizeLabels)
plt.title('Psychometric')
#plt.xlim([0,])
ax2.set_xscale("log")
#plt.xticks
plt.ylim([-0.1,0.5])
extraplots.boxoff(plt.gca())

# -- Panel C: Plot scatter of movment modulation index vs sound modulation index for psychometric -- #
ax3 = plt.subplot(gs[1,0])
ax3.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(spkWidth_switching, np.abs(soundModI_switching), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(spkWidth_switching[soundModSwitching], np.abs(soundModI_switching[soundModSwitching]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Spike width (ms)',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice',fontsize=fontSizeLabels)
plt.title('Switching')
#plt.xlim([-1.1,1.1])
plt.ylim([-0.1,0.7])
extraplots.boxoff(plt.gca())

# -- Panel D: Plot scatter of movment modulation index vs sound modulation index for switching -- #
ax4 = plt.subplot(gs[1,1])
ax4.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(NatoKRatio_switching, np.abs(soundModI_switching), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(NatoKRatio_switching[soundModSwitching], np.abs(soundModI_switching[soundModSwitching]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Na peak to K peak ratio (log)',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice',fontsize=fontSizeLabels)
plt.title('Switching')
#plt.xlim([-1.1,1.1])
ax4.set_xscale("log")
plt.ylim([-0.1,0.7])
extraplots.boxoff(plt.gca())


plt.show()

# -- Stats -- # 
#numCellsPsy = len(cellsToPlot_psychometric)
#numMovSelPsy = sum(movementSelectivePsychometric)
#numSoundModPsy = sum(soundModPsychometric)
print 'Number of cells for psychometric:', len(cellsToPlot_psychometric)
print 'Number of cells for switching:', len(cellsToPlot_switching)
rPsy1, pValPsy1 = stats.spearmanr(spkWidth_psychometric, np.abs(soundModI_psychometric))
print '\nPsychometric task: Spearman correlation coefficient between sound response index and spike width is:', rPsy1, 'p value is:', pValPsy1
rPsy2, pValPsy2 = stats.spearmanr(NatoKRatio_psychometric, np.abs(soundModI_psychometric))
print '\nPsychometric task: Spearman correlation coefficient between sound response index and Na to K peak ratio is:', rPsy2, 'p value is:', pValPsy2

rSwi, pValSwi = stats.spearmanr(spkWidth_switching, np.abs(soundModI_switching))
print '\nSwitching task: Spearman correlation coefficient between sound response index and spike width is:', rSwi, 'p value is:', pValSwi
rSwi2, pValSwi2 = stats.spearmanr(NatoKRatio_switching, np.abs(soundModI_switching))
print '\nSwitching task: Spearman correlation coefficient between sound response index and Na to K peak ratio is:', rSwi2, 'p value is:', pValSwi2

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

