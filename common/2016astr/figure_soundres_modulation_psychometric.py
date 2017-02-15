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
import scipy.stats as stats

FIGNAME = 'soundres_modulation_psychometric'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

removedDuplicates = True

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

colorsDict = {'colorL':figparams.colp['MidFreqL'], 
              'colorR':figparams.colp['MidFreqR']} 

SAVE_FIGURE = 1
outputDir = '/home/languo/tmp/'
if removedDuplicates:
    figFilename = 'figure_choice_modulation_psychometric_remove_dup'
else:
    figFilename = 'figure_choice_modulation_psychometric' # Do not include extension
figFormat = 'png' # 'pdf' or 'svg'
figSize = [18,4]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1

labelPosX = [0.07, 0.35, 0.6]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.85, wspace=0.3, hspace=0.3)

gs00 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,1], hspace=0.1)
gs01 = gridspec.GridSpecFromSubplotSpec(3, 3, subplot_spec=gs[:,2], hspace=0.1)

timeRangeSound = [-0.2, 0.4]
msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

# -- Panel A: schematic of psychometric curve indicating center freq-- #
#ax1 = plt.subplot(gs[0, 0:2])
ax1 = plt.subplot(gs[0, 0])
plt.axis('off')


ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel B: representative sound-evoked raster from psychometric task, Not modulated -- #
#ax2 = plt.subplot(gs[0, 2:4])
ax2 = plt.subplot(gs00[0:2, :])
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
#plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
ax2.axes.xaxis.set_ticklabels([])
plt.ylabel('Trials',fontsize=fontSizeLabels,labelpad=labelDis)
#plt.xlim(timeRangeSound[0],timeRangeSound[1])
ax2.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel B2: representative sound-evoked psth from psychometric task, Not modulated -- #
#ax3 = plt.subplot(gs[1,2:4])
ax3 = plt.subplot(gs00[2, :])
psthFilename = 'example_psycurve_9781Hz_soundaligned_psth_test055_20150313a_T4_c7.npz' 
psthFullPath = os.path.join(dataDir, psthFilename)
psthExample =np.load(psthFullPath)

condLabels = psthExample['condLabels']
trialsEachCond = psthExample['trialsEachCond']
colorEachCond = psthExample['colorEachCond']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.ylim(0,100)
plt.xlim(timeRangeSound[0],timeRangeSound[1])
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels,labelpad=labelDis)

# -- Panel C: representative sound-evoked raster from psychometric task, Modulated-- #
#ax4 = plt.subplot(gs[0, 4:6])
ax4 = plt.subplot(gs01[0:2, :])
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
#plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels) 
ax4.axes.xaxis.set_ticklabels([])
plt.ylabel('Trials',fontsize=fontSizeLabels, labelpad=labelDis)
#plt.xlim(timeRangeSound[0],timeRangeSound[1])
ax4.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


# -- Panel C2: representative sound-evoked psth from psychometric task, Modulated -- #
#ax5 = plt.subplot(gs[1,4:6])
ax5 = plt.subplot(gs01[2, :])
psthFilename = 'example_psycurve_11607Hz_soundaligned_psth_adap017_20160411a_T3_c10.npz' 
psthFullPath = os.path.join(dataDir, psthFilename)
psthExample =np.load(psthFullPath)

condLabels = psthExample['condLabels']
trialsEachCond = psthExample['trialsEachCond']
colorEachCond = psthExample['colorEachCond']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

for ind,line in enumerate(pPSTH):
    plt.setp(line, label=condLabels[ind])
plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeSound[0],timeRangeSound[1])
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels, labelpad=labelDis)

# -- Panel D: summary distribution of psychometric modulation index -- #
ax6 = plt.subplot(gs[1,0])

if removedDuplicates:
    summaryFilename = 'summary_psychometric_sound_modulation_good_cells_responsive_midfreq_remove_dup.npz'
else:
    summaryFilename = 'summary_psychometric_sound_modulation_good_cells_responsive_midfreq.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

sigModulated = summary['modulated']
sigMI = summary['modulationIndex'][sigModulated]
nonsigMI = summary['modulationIndex'][~sigModulated]
plt.hist([sigMI,nonsigMI], bins=25, edgecolor='None', color=['k','darkgrey'], stacked=True)

sig_patch = mpatches.Patch(color='k', label='Modulated')
nonsig_patch = mpatches.Patch(color='darkgrey', label='Not modulated')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)

plt.axvline(x=0, linestyle='--',linewidth=1.5, color='k')
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Modulation index', fontsize=fontSizeLabels)
plt.ylabel('Number of cells', fontsize=fontSizeLabels)

ax6.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


# -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
(T, pVal) = stats.wilcoxon(summary['modulationIndex'])
print 'Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of', pVal
