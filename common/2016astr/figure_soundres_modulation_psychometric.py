'''
Create figure about the activity of astr neurons during sound being modulated by choice in the psychometric curve task.
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

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'fig_choice_modulation_psychometric' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

timeRangeSound = [-0.2, 0.4]
msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

#colormapSound =  

labelPosX = [0.07, 0.35, 0.65]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

#COLORMAP = {'leftTrials':'red', 'rightTrials':'green'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 6)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)


# -- Panel A: representative sound-evoked raster from psychometric task, Modulated-- #
ax1 = plt.subplot(gs[0, 0:2])

rasterFilename = 'example_psycurve_11607Hz_soundaligned_raster_adap017_20160411a_T3_c10.npz' 
rasterFullPath = os.path.join(dataDir, rasterFilename)
rasterExample =np.load(rasterFullPath)

trialsEachCond = rasterExample['trialsEachCond']
colorEachCond = rasterExample['colorEachCond']
spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
timeRange = rasterExample['timeRange']

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                               indexLimitsEachTrial,
                                               timeRange=timeRangeSound,
                                               trialsEachCond=trialsEachCond,
                                               colorEachCond=colorEachCond)

plt.setp(pRaster, ms=msRaster)
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels) 
plt.ylabel('Trials',fontsize=fontSizeLabels)
#plt.xlim(timeRangeSound[0],timeRangeSound[1])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel A2: representative sound-evoked psth from psychometric task, Modulated -- #
ax2 = plt.subplot(gs[1,0:2])

psthFilename = 'example_psycurve_11607Hz_soundaligned_psth_adap017_20160411a_T3_c10.npz' 
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
plt.xlim(timeRangeSound[0],timeRangeSound[1])
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels)


# -- Panel B: representative sound-evoked raster from psychometric task, Not modulated -- #
ax3 = plt.subplot(gs[0, 2:4])

rasterFilename = 'example_psycurve_9781Hz_soundaligned_raster_test055_20150313a_T4_c7.npz' 
rasterFullPath = os.path.join(dataDir, rasterFilename)
rasterExample =np.load(rasterFullPath)

trialsEachCond = rasterExample['trialsEachCond']
colorEachCond = rasterExample['colorEachCond']
spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
timeRange = rasterExample['timeRange']

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                               indexLimitsEachTrial,
                                               timeRange=timeRangeSound,
                                               trialsEachCond=trialsEachCond,
                                               colorEachCond=colorEachCond,
                                               fillWidth=None,labels=None)

plt.setp(pRaster, ms=msRaster)
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Trials',fontsize=fontSizeLabels)
#plt.xlim(timeRangeSound[0],timeRangeSound[1])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel B2: representative sound-evoked psth from psychometric task, Not modulated -- #
ax4 = plt.subplot(gs[1,2:4])

psthFilename = 'example_psycurve_9781Hz_soundaligned_psth_test055_20150313a_T4_c7.npz' 
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
plt.xlim(timeRangeSound[0],timeRangeSound[1])
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels)


# -- Panel C: summary distribution of psychometric modulation index -- #
ax5 = plt.subplot(gs[0:,4:6])

summaryFilename = 'summary__selectivity_all_good_cells.npz'
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

ax5.annotate('C', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')
'''
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

