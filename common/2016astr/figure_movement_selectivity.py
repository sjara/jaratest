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
outputDir = '/tmp/'
'''
if removedDuplicates:
    figFilename = 'figure_movement_selectivity_remove_dup' # Do not include extension
else:
    figFilename = 'figure_movement_selectivity' # Do not include extension
'''
figFilename = 'figure_movement_selectivity'
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,3.5]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

timeRangeMovement = [-0.3, 0.5]
msRaster = 2
smoothWinSizePsth = 2
lwPsth = 2
downsampleFactorPsth = 1

#colormapMovement =  

labelPosX = [0.05, 0.4, 0.7]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels

#MOVEMENTCOLORS = {'left':figparams.colp['MidFreqL'], 'right':figparams.colp['MidFreqR']}
MOVEMENTCOLORS = [figparams.colp['MidFreqL'],figparams.colp['MidFreqR']]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(4, 3)
#gs.update(left=0.15, right=0.85, wspace=1, hspace=0.2)
gs.update(left=0.1, right=0.98, top=0.95, bottom=0.15, wspace=0.4, hspace=0.1)


# -- Panel A: representative raster during movement  -- #
ax1 = plt.subplot(gs[0:3, 0])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

rasterFilename = 'example_movement_sel_raster_adap017_20160330a_T4_c11.npz' #adap013_20160406a_T8_c4  #test059_20150629a_T2_c7
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
                                               colorEachCond=MOVEMENTCOLORS)

plt.setp(pRaster, ms=msRaster)
#plt.xlabel('Time from movement onset (s)', fontsize=fontSizeLabels)
#plt.ylabel('Trials', fontsize=fontSizeLabels)
ax1.set_yticklabels([])
ax1.set_xticklabels([])
#plt.xlim(timeRangeMovement[0],timeRangeMovement[1])


# -- Panel A2: representative psth during movement  -- #
#ax2 = plt.subplot(gs[3,0], sharex=ax1)
ax2 = plt.subplot(gs[3,0])

psthFilename = 'example_movement_sel_psth_adap017_20160330a_T4_c11.npz' #adap013_20160406a_T8_c4  #test059_20150629a_T2_c7 
psthFullPath = os.path.join(dataDir, psthFilename)
psthExample =np.load(psthFullPath)

trialsEachCond = psthExample['trialsEachCond']
colorEachCond = psthExample['colorEachCond']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,
                             colorEachCond=MOVEMENTCOLORS,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

for ind,line in enumerate(pPSTH):
    plt.setp(line, label=condLabels[ind])
plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeMovement[0],timeRangeMovement[1])
plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate\n(spk/sec)',fontsize=fontSizeLabels)
yLims = [0,35]
plt.ylim(yLims)
plt.yticks(yLims)
plt.xticks(np.arange(-0.2,0.6,0.2))
extraplots.boxoff(plt.gca())

# -- Panel B: Another representative raster during movement, more responsive to ipsilateral movement-- #
ax1 = plt.subplot(gs[0:3, 1])
ax1.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

rasterFilename = 'example_movement_sel_raster_test055_20150313a_T7_c6.npz' #test059_20150629a_T2_c7
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
                                               colorEachCond=MOVEMENTCOLORS)

plt.setp(pRaster, ms=msRaster)
#plt.xlabel('Time from movement onset (s)', fontsize=fontSizeLabels)
#plt.ylabel('Trials', fontsize=fontSizeLabels)
ax1.set_yticklabels([])
ax1.set_xticklabels([])
#plt.xlim(timeRangeMovement[0],timeRangeMovement[1])


# -- Panel B2: representative psth during movement  -- #
#ax2 = plt.subplot(gs[3,0], sharex=ax1)
ax2 = plt.subplot(gs[3,1])

psthFilename = 'example_movement_sel_psth_test055_20150313a_T7_c6.npz' #test059_20150629a_T2_c7 
psthFullPath = os.path.join(dataDir, psthFilename)
psthExample =np.load(psthFullPath)

trialsEachCond = psthExample['trialsEachCond']
colorEachCond = psthExample['colorEachCond']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,trialsEachCond=trialsEachCond,
                             colorEachCond=MOVEMENTCOLORS,linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)

for ind,line in enumerate(pPSTH):
    plt.setp(line, label=condLabels[ind])
plt.legend(['Left','Right'], loc='upper right', fontsize=fontSizeTicks, handlelength=0.2,
           frameon=False, handletextpad=0.3, labelspacing=0, borderaxespad=0)

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeMovement[0],timeRangeMovement[1])
plt.xlabel('Time from movement onset (s)',fontsize=fontSizeLabels)
plt.ylabel('Firing rate\n(spk/sec)',fontsize=fontSizeLabels)
yLims = [0,15]
plt.ylim(yLims)
plt.yticks(yLims)
plt.xticks(np.arange(-0.2,0.6,0.2))
extraplots.boxoff(plt.gca())


# -- Panel C: summary distribution of movement modulation index -- #
ax3 = plt.subplot(gs[:,2])
ax3.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

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
binsEdges = np.linspace(-1,1,20)
plt.hist([sigMI,nonsigMI], bins=binsEdges, color=['k','darkgrey'],edgecolor='None',stacked=True)

'''
sig_patch = mpatches.Patch(color='k', label='Selective')
nonsig_patch = mpatches.Patch(color='darkgrey', label='Not selective')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper left', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2, ncol=2, columnspacing=0.5)
'''

plt.axvline(x=0, linestyle='--',linewidth=1.5, color='0.5')
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Movement selectivity index', fontsize=fontSizeLabels)
plt.ylabel('Number of cells', fontsize=fontSizeLabels)
extraplots.boxoff(plt.gca())

plt.show()

# -- Stats: test whether the modulation index distribution for all good cells is centered at zero -- #
numCells = len(sigModulated)
numSig = len(sigMI)
numSigNeg = sum(sigMI<0)
numSigPos = sum(sigMI>0)
print numSig, ' cells were significantly modulated by movement direction, that is ', np.mean(sigModulated)*100, '% of', numCells, 'total good cells recorded in the striatum.'
print 'Out of the movement direction selective cells,', numSigNeg, ' cells were more active when moving to the contralaterral side (left). That is {}% of total cells.'.format(100*numSigNeg/float(numCells))
print 'median of movemewnt modulation index is', np.mean(summary['movementModI'])
(T, pVal) = stats.wilcoxon(summary['movementModI'])
print 'Using the Wilcoxon signed-rank test, comparing the modulation index distribution for all good cells to zero yielded a p value of', pVal



if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
