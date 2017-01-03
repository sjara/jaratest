'''
Create figure about the activity of astr neurons during movement being selective to the side of movement in the 2afc task.
'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import figparams
import matplotlib.patches as mpatches

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'fig_movement_selective' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

timeRangeMovement = [-0.2, 0.5]
msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

#colormapMovement =  

labelPosX = [0.07, 0.5]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

MOVEMENTCOLORS = {'left':'red', 'right':'green'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)


# -- Panel A: representative raster during movement from switching task -- #
ax1 = plt.subplot(gs[0, 0:2])

rasterFilename = 'example_movement_sel_raster_test059_20150629a_T2_c7.npz' 
rasterFullPath = os.path.join(dataDir, rasterFilename)
rasterExample =np.load(rasterFullPath)

trialsEachCond = rasterExample['trialsEachCond']
colorEachCond = rasterExample['colorEachCond']
spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
timeRange = rasterExample['timeRange']

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                               indexLimitsEachTrial,
                                               timeRange=timeRangeMovement,
                                               trialsEachCond=trialsEachCond,
                                               colorEachCond=colorEachCond)

plt.setp(pRaster, ms=msRaster)
plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
#plt.xlim(timeRangeMovement[0],timeRangeMovement[1])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel A2: representative psth during movement from switching task -- #
ax2 = plt.subplot(gs[1,0:2])

psthFilename = 'example_movement_sel_psth_test059_20150629a_T2_c7.npz' 
psthFullPath = os.path.join(dataDir, psthFilename)
psthExample =np.load(psthFullPath)

trialsEachCond = psthExample['trialsEachCond']
colorEachCond = psthExample['colorEachCond']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']

extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeMovement[0],timeRangeMovement[1])
plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels)


# -- Panel B: summary distribution of movement modulation index -- #
ax3 = plt.subplot(gs[0:,2:4])

summaryFilename = 'summary_movement_selectivity_all_good_cells.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

sigModulated = summary['movementSelective']
sigMI = summary['movementModI'][sigModulated]
nonsigMI = summary['movementModI'][~sigModulated]
plt.hist([sigMI,nonsigMI], bins=50, color=['k','darkgrey'], stacked=True)

sig_patch = mpatches.Patch(color='k', label='Selective')
nonsig_patch = mpatches.Patch(color='darkgrey', label='Not selective')
plt.legend(handles=[sig_patch,nonsig_patch])

plt.axvline(x=0, linestyle='--',linewidth=1.5, color='k')
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Modulation index', fontsize=fontSizeLabels)
plt.ylabel('Number of cells', fontsize=fontSizeLabels)

ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

