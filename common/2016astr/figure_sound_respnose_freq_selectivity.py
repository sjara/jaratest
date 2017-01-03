'''
Create figure about effect of unilateral photo-activation of astr neurons in the 2afc task.
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

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'fig_sound_freq_selective' # Do not include extension
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

colormapTuning = matplotlib.cm.winter 

labelPosX = [0.07, 0.35, 0.65]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

PHOTOSTIMCOLORS = {'no_laser':'k', 'laser_left':'red', 'laser_right':'green'}

SHAPESEACHANIMAL = ['o','s','^']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 6)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)


# -- Panel A: representative sound-evoked raster from tuning task -- #
ax1 = plt.subplot(gs[0, 0:2])

rasterFilename = 'example_freq_tuning_raster_test059_20150624a_T1_c4.npz' 
rasterFullPath = os.path.join(dataDir, rasterFilename)
rasterExample =np.load(rasterFullPath)

possibleFreq = rasterExample['possibleFreq']
trialsEachCond = rasterExample['trialsEachFreq']
spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
timeRange = rasterExample['timeRange']
labels = ['%.1f' % f for f in np.unique(possibleFreq)]

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                               indexLimitsEachTrial,
                                               timeRange,
                                               trialsEachCond=trialsEachCond,
                                               labels=labels)

plt.setp(pRaster, ms=msRaster)
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Frequency (Hz)',fontsize=fontSizeLabels)
plt.xlim(timeRangeSound[0],timeRangeSound[1])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel A2: representative sound-evoked psth from tuning task -- #
ax2 = plt.subplot(gs[1,0:2])

psthFilename = 'example_freq_tuning_psth_test059_20150624a_T1_c4.npz' 
psthFullPath = os.path.join(dataDir, psthFilename)
psthExample =np.load(psthFullPath)

trialsEachCond = psthExample['trialsEachFreq']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']
possibleFreq = psthExample['possibleFreq']
numFreqs = len(possibleFreq)

cm_subsection = np.linspace(0.0, 1.0, numFreqs)
colorEachCond = [colormapTuning(x) for x in cm_subsection] 

extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeSound[0],timeRangeSound[1])
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels)


# -- Panel B:  -- #
ax3 = plt.subplot(gs[0:,2:4])


ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# -- Panel C: summary left vs right hemi best frequency -- #
ax4 = plt.subplot(gs[0:,4:6])

summaryFilename = 'summary_bilateral_best_freq.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

left014 = summary['d1pi014_left']
left015 = summary['d1pi015_left']
left016 = summary['d1pi016_left']
right014 = summary['d1pi014_right']
right015 = summary['d1pi015_right']
right016 = summary['d1pi016_right']

for ind,leftData in enumerate([left014,left015,left016]):
    ax4.plot(np.repeat(1+0.2*(ind-1),len(leftData)), leftData, marker=SHAPESEACHANIMAL[ind], mfc=PHOTOSTIMCOLORS['laser_left'], ls='None')
    
for ind,rightData in enumerate([right014,right015,right016]):
    ax4.plot(np.repeat(2+0.2*(ind-1),len(rightData)), rightData, marker=SHAPESEACHANIMAL[ind], mfc=PHOTOSTIMCOLORS['laser_right'], ls='None')

xlim = [0.3,2.7]
ylim = [-2, 2]
plt.axhline(y=0, linestyle='--',linewidth=1.5, color='k')
plt.xlim(xlim)
plt.ylim(ylim)
xticks = [1,2]
xticklabels = ['left hemi', 'right hemi']
plt.xticks(xticks, xticklabels, fontsize=fontSizeLabels)
plt.ylabel('Log2(most responsive frequency - psychometric boundary)', fontsize=fontSizeLabels)
ax4.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

