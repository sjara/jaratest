'''
Create figure summarizing best frequencies and frequency-selectivity during psychometric 2afc for all good cells in striatum.
'''
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import figparams
import matplotlib.patches as mpatches
import scipy.stats as stats

FIGNAME = 'sound_movement_selectivity_corr_psychometric'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)
soundDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'sound_freq_selectivity')
movementDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'movement_selectivity')
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
#PANELS = [1,1] # Which panels to plot

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'supp_sound_movement_selectivity_corr_psychometric' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [10,3]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
#labelDis = 0.1
labelPosX = [0.07, 0.4, 0.67]   # Horiz position for panel labels
labelPosY = [0.9]    # Vert position for panel labels
MOVEMENTCOLORS = [figparams.colp['MidFreqL'],figparams.colp['MidFreqR']]
colormapTuning = matplotlib.cm.winter 
timeRangeSound = [-0.2, 0.4]
timeRangeMovement = [-0.2, 0.4]
msRaster = 2
smoothWinSizePsth = 2
lwPsth = 2
downsampleFactorPsth = 1

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,3)
gs.update(left=0.15, right=0.95,top=0.95, bottom=0.15, wspace=0.4, hspace=0.1)
gs00 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,0], hspace=0.1)
gs01 = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=gs[:,1], hspace=0.1)

# -- Panel A: example of sound-evoked raster and psth from 2afc task -- #
ax1 = plt.subplot(gs00[0:3,:])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

rasterFilename = 'example_freq_tuning_2afc_raster_adap017_20160328a_T7_c9.npz' 
rasterFullPath = os.path.join(soundDir, rasterFilename)
rasterExample =np.load(rasterFullPath)

possibleFreq = rasterExample['possibleFreq']
trialsEachCond = rasterExample['trialsEachFreq']
spikeTimesFromEventOnset = rasterExample['spikeTimesFromEventOnset']
indexLimitsEachTrial = rasterExample['indexLimitsEachTrial']
#timeRange = rasterExample['timeRange']
labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

colorEachFreq = [colormapTuning(x) for x in np.linspace(1.0, 0.2, len(possibleFreq))] 

pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                               indexLimitsEachTrial,
                                               timeRangeSound,
                                               trialsEachCond=trialsEachCond,
                                               colorEachCond=colorEachFreq,
                                               labels=labels)
plt.setp(pRaster, ms=msRaster)
plt.setp(hcond,zorder=3)
#plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels, labelpad=labelDis)
plt.gca().set_xticklabels('')
plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels) #, labelpad=labelDis)
plt.xlim(timeRangeSound[0],timeRangeSound[1])

ax2 = plt.subplot(gs00[3,:])

psthFilename = 'example_freq_tuning_2afc_psth_adap017_20160328a_T7_c9.npz' 
psthFullPath = os.path.join(soundDir, psthFilename)
psthExample =np.load(psthFullPath)

trialsEachCond = psthExample['trialsEachFreq']
spikeCountMat = psthExample['spikeCountMat']
timeVec = psthExample['timeVec']
binWidth = psthExample['binWidth']
timeRange = psthExample['timeRange']
possibleFreq = psthExample['possibleFreq']
numFreqs = len(possibleFreq)
labels = ['%.1f' % f for f in np.unique(possibleFreq)/1000.0]

#smoothWinSizePsth = 1

pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSizePsth,timeVec,
                             trialsEachCond=trialsEachCond,colorEachCond=colorEachFreq,
                             linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
for ind,line in enumerate(pPSTH):
    plt.setp(line, label=labels[ind])
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.axvline(x=0,linewidth=1, color='darkgrey')
plt.xlim(timeRangeSound)
plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels) #, labelpad=labelDis
plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels) #, labelpad=labelDis
plt.ylim([0,80])
plt.yticks([0,80])
extraplots.boxoff(plt.gca())
#plt.legend(loc='upper right', fontsize=fontSizeTicks, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)


# -- Panel B: same cell during movement  -- #
ax3 = plt.subplot(gs01[0:3,:])
ax3.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

rasterFilename = 'example_movement_sel_raster_adap017_20160328a_T7_c9.npz' #adap013_20160406a_T8_c4  #test059_20150629a_T2_c7
rasterFullPath = os.path.join(movementDir, rasterFilename)
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
plt.ylabel('Trials grouped\nby choice', fontsize=fontSizeLabels)
ax3.set_yticklabels([])
ax3.set_xticklabels([])
#plt.xlim(timeRangeMovement[0],timeRangeMovement[1])


# -- Panel A2: representative psth during movement  -- #
#ax2 = plt.subplot(gs[3,0], sharex=ax1)
#ax2 = plt.subplot(gs[3,0])
ax4 = plt.subplot(gs01[3,:])

psthFilename = 'example_movement_sel_psth_adap017_20160328a_T7_c9.npz' #adap013_20160406a_T8_c4  #test059_20150629a_T2_c7 
psthFullPath = os.path.join(movementDir, psthFilename)
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
plt.ylabel('Firing rate\n(spk/s)',fontsize=fontSizeLabels)
yLims = [0,35]
plt.ylim(yLims)
plt.yticks(yLims)
plt.xticks(np.arange(-0.2,0.6,0.2))
extraplots.boxoff(plt.gca())

# -- Panel C: correlation between sound freq selectivity and movement selectivity -- #
ax5 = plt.subplot(gs[:,2])
ax3.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

alphaLevel = 0.05
#numFreqs = 6
#bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs

summaryFilename = 'summary_2afc_best_freq_maxZ_psychometric.npz'
summaryFullPath = os.path.join(dataDir,'sound_freq_selectivity', summaryFilename)
summary = np.load(summaryFullPath)

psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(dataDir, psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

#####################################################################################
cellSelectorBoolArray = summary['cellSelectorBoolArray']
#bestFreqEachCell = summary['bestFreqEachCell'][cellSelectorBoolArray]
#maxZscoreEachCell = summary['maxZscoreEachCell'][cellSelectorBoolArray]
responseIndEachCell = summary['responseIndEachCell'][cellSelectorBoolArray]

# -- summary stats about sound responsiveness (rank sum test significant) and frequency selectivity (ANOVA test significant) -- #
#sigSoundResponse = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= bonferroniCorrectedAlphaLevel)
freqSelective = (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel) #freqSelectivityEachCell contain the p value of the ANOVA test comparing evoked responses from all frequencies for each cell
# -- Get movement and sound modulation index for psychometric cells -- #
goodcells_psychometric = allcells_psychometric[cellSelectorBoolArray]

movementModIEachCell = goodcells_psychometric.movementModI.values
movementModSigEachCell = goodcells_psychometric.movementModS.values

movementSelectivePsychometric = (movementModSigEachCell <= alphaLevel)

# -- Scatter plot of modulation index vs sound response index -- #
#plt.plot(responseIndEachCell, movementModIEachCell, marker='o', linestyle='none', mec='grey', mfc='none')
plt.plot(np.abs(responseIndEachCell), np.abs(movementModIEachCell), marker='o', linestyle='none', mec='grey', mfc='none')
plt.xlabel('Sound response index')
plt.ylabel('Movement selectivity index')
plt.xlim([-1.1,1.1])
plt.ylim([-1.1,1.1])
#plt.title('Psychometric task')
extraplots.boxoff(plt.gca())

plt.show()

nanCells = np.isnan(responseIndEachCell)|np.isnan(movementModIEachCell)

print '****** WARNING ***** found {} cells with NaN response/movement index. They are removed from stats.'.format(np.sum(nanCells))
responseIndEachCell = responseIndEachCell[~nanCells]
movementModIEachCell = movementModIEachCell[~nanCells]

# -- Stats -- #
numCells = sum(cellSelectorBoolArray)
numSoundMovementSelective = sum(freqSelective & movementSelectivePsychometric)
print numSoundMovementSelective, 'cells out of', numCells, 'good cells were both selective to sound freq and movement direction during 2afc'
r, pVal = stats.spearmanr(responseIndEachCell, movementModIEachCell)
print '\nSpearman correlation coefficient between sound response index and movement direction modulation index is:', r, 'p value is:', pVal

r, pVal = stats.spearmanr(np.abs(responseIndEachCell), np.abs(movementModIEachCell))
print '\nSpearman correlation coefficient between ABS(sound response index) and ABS(movement direction modulation index) is:', r, 'p value is:', pVal

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


'''
# Test whether we get correlation from noise when using abs()
# It looks like using abs() does not increase correlation

nSamples = 1000
x=np.random.randn(nSamples)
y=np.random.randn(nSamples)
stats.spearmanr(x,y)
stats.spearmanr(np.abs(x),np.abs(y))

plot(x,y,'o',mfc='none')
plot(np.abs(x),np.abs(y),'o',mfc='none')
'''
