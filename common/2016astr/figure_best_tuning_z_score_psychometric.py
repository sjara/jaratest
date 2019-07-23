'''
Create figure summarizing best tuning frequencies for all good cells in striatum.
'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import figparams
import matplotlib.patches as mpatches

FIGNAME = 'tuning_Z_score_psychometric'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/home/languo/tmp/'
figFilename = 'figure_tuning_z_score_psychometric' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(left=0.15, right=0.85, wspace=0.5, hspace=0.5)

alphaLevel = 0.05
numFreqs = 16
bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs

summaryFilename = 'summary_tuning_best_freq_maxZ_psychometric.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

####################################################################################3
cellSelectorBoolArray = summary['cellSelectorBoolArray']
bestFreqEachCell = summary['bestFreqEachCell'][cellSelectorBoolArray]
#bestFreqEachCell = bestFreqEachCell[bestFreqEachCell!=0]
maxZscoreEachCell = summary['maxZscoreEachCell'][cellSelectorBoolArray]
#maxZscoreEachCell = maxZscoreEachCell[maxZscoreEachCell!=0]
responseIndEachCell = summary['responseIndEachCell'][cellSelectorBoolArray]
freqSelective = (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel)
sigSoundResponse = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= bonferroniCorrectedAlphaLevel)

# -- Panel A: histogram of maximum sound response Z score for all good cells -- #
ax1 = plt.subplot(gs[0,0])
plt.hist((responseIndEachCell[sigSoundResponse],responseIndEachCell[~sigSoundResponse]), color=['k','darkgrey'], bins=20)
plt.xlabel('Maximum sound response index')
plt.ylabel('Number of cells')
sig_patch = mpatches.Patch(color='k', label='sound responsive')
nonsig_patch = mpatches.Patch(color='darkgrey', label='Not sound responsive')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)

# -- Panel B: histogram of most responsive frequency for all good cells -- #
ax2 = plt.subplot(gs[0,1])
plt.hist((bestFreqEachCell[freqSelective],bestFreqEachCell[~freqSelective]), color=['k','darkgrey'], bins=20)
plt.xlabel('Most responsive frequency (Hz)')
plt.ylabel('Number of cells')
sig_patch = mpatches.Patch(color='k', label='frequency selective')
nonsig_patch = mpatches.Patch(color='darkgrey', label='Not frequency selective')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# -- Stats summary-- #
numCells = sum(cellSelectorBoolArray)
numSoundResCells = sum(sigSoundResponse.astype(int))
print 100*float(numSoundResCells)/numCells, '% of cells show significant sound response (after Bonferroni correction)'
numFreqSelectiveCells = sum(freqSelective.astype(int))
print 100*float(numFreqSelectiveCells)/numCells, '% of cells show significant frequency selectivity'


