'''
Script to make a scatter plot of sound modulation index (by choice) vs waveform params, for psychometric curve mice and switching mice separately.
20160330 filter out all cells with trough to peak time larger than 0.4 msec since those mostly have mis-identified K peak.
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
from matplotlib.ticker import FormatStrFormatter

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
labelPosX = [0.04, 0.49]   # Horiz position for panel labels
labelPosY = [0.94, 0.5]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,2)
gs.update(left=0.15, right=0.95,top=0.9, bottom=0.15, wspace=0.6, hspace=0.5)
qualityList = [1,6]
ISIcutoff = 0.02
maxZThreshold = 3
maxTroughToPeakTime = 0.4 #msec

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

trough2peak_psychometric = 1000*(cellsToPlot_psychometric.peakKTime - cellsToPlot_psychometric.peakNaTime).values
trough2peakFilter = (trough2peak_psychometric <= maxTroughToPeakTime)
trough2peak_psychometric = trough2peak_psychometric[trough2peakFilter]
trough2peakRatio_psychometric = (np.abs(cellsToPlot_psychometric.peakNaAmp / cellsToPlot_psychometric.peakKAmp)).values
trough2peakRatio_psychometric = trough2peakRatio_psychometric[trough2peakFilter]
#For psychometric curve task, choose the center frequency that a cell is more responsive to and plot the modulation index of that frequency
strongerSoundResMid1 = abs(cellsToPlot_psychometric.maxZSoundMid1) > abs(cellsToPlot_psychometric.maxZSoundMid2)
soundModI_psychometric = np.r_[cellsToPlot_psychometric.modIndexMid1[strongerSoundResMid1].values,cellsToPlot_psychometric.modIndexMid2[~strongerSoundResMid1].values]
soundModI_psychometric = soundModI_psychometric[trough2peakFilter]
soundModSig_psychometric = np.r_[cellsToPlot_psychometric.modSigMid1[strongerSoundResMid1].values,cellsToPlot_psychometric.modSigMid2[~strongerSoundResMid1].values] 
soundModSig_psychometric = soundModSig_psychometric[trough2peakFilter]

soundModPsychometric = (soundModSig_psychometric <= 0.05)

# -- Get movement and sound modulation index for switching cells -- #
goodcells_switching = (allcells_switching.cellQuality.isin(qualityList)) & (allcells_switching.ISI <= ISIcutoff)
cellInStr =  (allcells_switching.cellInStr==1)
keepAfterDupTest = allcells_switching.keep_after_dup_test
responsiveMidFreqs = abs(allcells_switching.maxZSoundMid)>=maxZThreshold
#cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest]
cellsToPlot_switching = allcells_switching[goodcells_switching & cellInStr & keepAfterDupTest & responsiveMidFreqs]

trough2peak_switching = 1000*(cellsToPlot_switching.peakKTime - cellsToPlot_switching.peakNaTime).values
trough2peakFilter = (trough2peak_switching <= maxTroughToPeakTime)
trough2peak_switching = trough2peak_switching[trough2peakFilter]
trough2peakRatio_switching = (np.abs(cellsToPlot_switching.peakNaAmp) / np.abs(cellsToPlot_switching.peakKAmp)).values
trough2peakRatio_switching = trough2peakRatio_switching[trough2peakFilter]
soundModI_switching = cellsToPlot_switching.modIndex.values
soundModI_switching = soundModI_switching[trough2peakFilter]
soundModSig_switching = cellsToPlot_switching.modSig.values
soundModSig_switching = soundModSig_switching[trough2peakFilter]
soundModDir_switching = cellsToPlot_switching.modDir.values
soundModDir_switching = soundModDir_switching[trough2peakFilter]
soundModSwitching = (soundModSig_switching <= 0.05)&(soundModDir_switching>=1)


# -- Panel A: Plot scatter of movment modulation index vs sound modulation index for psychometric -- #
ax1 = plt.subplot(gs[0,0])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(trough2peak_psychometric, np.abs(soundModI_psychometric), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(trough2peak_psychometric[soundModPsychometric], np.abs(soundModI_psychometric[soundModPsychometric]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Trough to peak time (ms)',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice (absolute value)',fontsize=fontSizeLabels)
plt.title('Sound discrimination task')
#plt.xlim([-1.1,1.1])
#locs, labels = plt.xticks()
#plt.xticks(locs, ('%.1f' %float(l) for l in labels))
#ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
plt.xticks([0.1,0.2,0.3,0.4],['0.1','0.2','0.3','0.4'])
plt.ylim([-0.05,0.4])
plt.yticks([0, 0.1,0.2,0.3,0.4],['0','0.1','0.2','0.3','0.4'])
extraplots.boxoff(plt.gca())

# -- Panel B: Plot scatter of movment modulation index vs sound modulation index for switching -- #
ax2 = plt.subplot(gs[0,1])
ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(trough2peakRatio_psychometric, np.abs(soundModI_psychometric), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(trough2peakRatio_psychometric[soundModPsychometric], np.abs(soundModI_psychometric[soundModPsychometric]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Trough to peak ratio',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice (absolute value)',fontsize=fontSizeLabels)
plt.title('Sound discrimination task')
#plt.xlim([0,])
ax2.set_xscale("log")
#plt.xticks
plt.ylim([-0.05,0.4])
plt.yticks([0,0.1,0.2,0.3,0.4],['0','0.1','0.2','0.3','0.4'])
ax2.xaxis.set_ticks_position('bottom')
extraplots.boxoff(plt.gca())

# -- Panel C: Plot scatter of movment modulation index vs sound modulation index for psychometric -- #
ax3 = plt.subplot(gs[1,0])
ax3.annotate('C', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(trough2peak_switching, np.abs(soundModI_switching), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(trough2peak_switching[soundModSwitching], np.abs(soundModI_switching[soundModSwitching]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Trough to peak time (ms)',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice (absolute value)',fontsize=fontSizeLabels)
plt.title('Switching task')
#plt.xlim([-1.1,1.1])
plt.ylim([-0.05,0.4])
plt.yticks([0,0.1,0.2,0.3,0.4],['0','0.1','0.2','0.3','0.4'])
plt.xticks([0.1,0.2,0.3,0.4],['0.1','0.2','0.3','0.4'])
#ax3.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
extraplots.boxoff(plt.gca())

# -- Panel D: Plot scatter of movment modulation index vs sound modulation index for switching -- #
ax4 = plt.subplot(gs[1,1])
ax4.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
plt.plot(trough2peakRatio_switching, np.abs(soundModI_switching), marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(trough2peakRatio_switching[soundModSwitching], np.abs(soundModI_switching[soundModSwitching]), marker='o', linestyle='none', mec='red', mfc='none')
plt.xlabel('Trough to peak ratio',fontsize=fontSizeLabels)
plt.ylabel('Sound modulation \nby choice (absolute value)',fontsize=fontSizeLabels)
plt.title('Switching task')
#plt.xlim([-1.1,1.1])
ax4.set_xscale("log")
plt.ylim([-0.05,0.4])
plt.yticks([0,0.1,0.2,0.3,0.4],['0','0.1','0.2','0.3','0.4'])
ax4.xaxis.set_ticks_position('bottom')
extraplots.boxoff(plt.gca())


plt.show()

# -- Stats -- # 
#numCellsPsy = len(cellsToPlot_psychometric)
#numMovSelPsy = sum(movementSelectivePsychometric)
#numSoundModPsy = sum(soundModPsychometric)
print 'Number of cells for psychometric:', len(cellsToPlot_psychometric), ', out of which {} cells were modulated'.format(sum(soundModPsychometric))

print 'Number of cells for switching:', len(cellsToPlot_switching), ', out of which {} cells were modulated'.format(sum(soundModSwitching))

rPsy1, pValPsy1 = stats.spearmanr(trough2peak_psychometric, np.abs(soundModI_psychometric))
print '\nPsychometric task: Spearman correlation coefficient between sound response index and trough to peak time is:', rPsy1, 'p value is:', pValPsy1
rPsy2, pValPsy2 = stats.spearmanr(trough2peakRatio_psychometric, np.abs(soundModI_psychometric))
print '\nPsychometric task: Spearman correlation coefficient between sound response index and trough to peak ratio is:', rPsy2, 'p value is:', pValPsy2

rSwi, pValSwi = stats.spearmanr(trough2peak_switching, np.abs(soundModI_switching))
print '\nSwitching task: Spearman correlation coefficient between sound response index and trough to peak time is:', rSwi, 'p value is:', pValSwi
rSwi2, pValSwi2 = stats.spearmanr(trough2peakRatio_switching, np.abs(soundModI_switching))
print '\nSwitching task: Spearman correlation coefficient between sound response index and trough to peak ratio is:', rSwi2, 'p value is:', pValSwi2

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

