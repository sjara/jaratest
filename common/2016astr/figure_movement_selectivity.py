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
import scipy.stats as stats

FIGNAME = 'movement_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

#removedDuplicates = True

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/home/languo/tmp/'
'''
if removedDuplicates:
    figFilename = 'figure_movement_selectivity_remove_dup' # Do not include extension
else:
    figFilename = 'figure_movement_selectivity' # Do not include extension
'''
figFilename = 'figure_movement_selectivity'
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

timeRangeMovement = [-0.2, 0.5]
msRaster = 2
smoothWinSizePsth = 3
lwPsth = 2
downsampleFactorPsth = 1

#colormapMovement =  

labelPosX = [0.07, 0.47]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

MOVEMENTCOLORS = {'left':'red', 'right':'green'}

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.2)


# -- Panel A: representative raster during movement from switching task -- #
ax1 = plt.subplot(gs[0, 0:2])

rasterFilename = 'example_movement_sel_raster_test059_20150629a_T2_c7.npz' 
rasterFullPath = os.path.join(dataDir, rasterFilename)
rasterExample =np.load(rasterFullPath)

trialsEachCond = rasterExample['trialsEachCond']
colorEachCond = rasterExample['colorEachCond']
condLabels = rasterExample['condLabels']
spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
timeRange = rasterExample['timeRange']

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                               indexLimitsEachTrial,
                                               timeRange=timeRangeMovement,
                                               trialsEachCond=trialsEachCond,
                                               colorEachCond=colorEachCond)

plt.setp(pRaster, ms=msRaster)
#plt.xlabel('Time from movement onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Trials', fontsize=fontSizeLabels)
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

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

for ind,line in enumerate(pPSTH):
    plt.setp(line, label=condLabels[ind])
plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeMovement[0],timeRangeMovement[1])
plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate (spk/sec)',fontsize=fontSizeLabels)


# -- Panel B: summary distribution of movement modulation index -- #
ax3 = plt.subplot(gs[0:,2:4])

'''
if removedDuplicates:
    summaryFilename = 'summary_movement_selectivity_all_good_cells_remove_dup.npz'
else:
    summaryFilename = 'summary_movement_selectivity_all_good_cells.npz'
'''
summaryFilename = 'summary_movement_selectivity_psychometric.npz'
#summaryFilename = 'summary_movement_selectivity_switching.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

sigModulated = summary['movementSelective']
sigMI = summary['movementModI'][sigModulated]
nonsigMI = summary['movementModI'][~sigModulated]
plt.hist([sigMI,nonsigMI], bins=50, color=['k','darkgrey'],edgecolor='None',stacked=True)
numSig = len(sigMI)
numSigNeg = sum(sigMI<0)
numSigPos = sum(sigMI>0)
print numSig, ' cells were significantly modulated by movement direction, that is ', np.mean(sigModulated)*100, '% of total good cells recorded in the striatum.'
print 'Out of the movement direction selective cells,', numSigNeg, ' cells were more active when moving to the contralaterral side (left). That is {}%.'.format(100*numSigNeg/float(numSig))

'''
sig_patch = mpatches.Patch(color='k', label='Selective')
nonsig_patch = mpatches.Patch(color='darkgrey', label='Not selective')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper left', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2, ncol=2, columnspacing=0.5)
'''

plt.axvline(x=0, linestyle='--',linewidth=1.5, color='k')
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Modulation index', fontsize=fontSizeLabels)
plt.ylabel('Number of cells', fontsize=fontSizeLabels)

ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
(T, pVal) = stats.wilcoxon(summary['movementModI'])
print 'Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of', pVal
