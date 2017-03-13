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

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/home/languo/tmp/'
figFilename = 'sound_movement_selectivity_corr_psychometric' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [6,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#gs = gridspec.GridSpec(1,1)
#gs.update(left=0.15, right=0.85, wspace=0.5, hspace=0.5)

alphaLevel = 0.05
numFreqs = 6
bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs

summaryFilename = 'summary_2afc_best_freq_maxZ_psychometric.npz'
summaryFullPath = os.path.join(dataDir,'2afc_Z_score_psychometric', summaryFilename)
summary = np.load(summaryFullPath)

psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(dataDir, psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

#####################################################################################
cellSelectorBoolArray = summary['cellSelectorBoolArray']
bestFreqEachCell = summary['bestFreqEachCell'][cellSelectorBoolArray]
#bestFreqEachCell = bestFreqEachCell[bestFreqEachCell!=0]
maxZscoreEachCell = summary['maxZscoreEachCell'][cellSelectorBoolArray]
#maxZscoreEachCell = maxZscoreEachCell[maxZscoreEachCell!=0]
responseIndEachCell = summary['responseIndEachCell'][cellSelectorBoolArray]

# -- summary stats about sound responsiveness (rank sum test significant) and frequency selectivity (ANOVA test significant) -- #
sigSoundResponse = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= bonferroniCorrectedAlphaLevel)
# Only consider whether frequency selective if sigSoundResponsive!
#freqSelective =(summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= bonferroniCorrectedAlphaLevel) & (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel)
freqSelective = (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel)
# -- Get movement and sound modulation index for psychometric cells -- #
goodcells_psychometric = allcells_psychometric[cellSelectorBoolArray]

movementModIEachCell = goodcells_psychometric.movementModI.values
movementModSigEachCell = goodcells_psychometric.movementModS.values

movementSelectivePsychometric = (movementModSigEachCell <= alphaLevel)

# -- Scatter plot of modulation index vs sound response index -- #
plt.scatter(responseIndEachCell, movementModIEachCell)
plt.xlabel('sound response index')
plt.ylabel('movement direction modulation index')
plt.title('Psychometric task')
plt.show()

# -- Stats -- #
numCells = sum(cellSelectorBoolArray)
numSoundMovementSelective = sum(freqSelective & movementSelectivePsychometric)
print numSoundMovementSelective, 'cells out of', numCells, 'good cells were both selective to sound freq and movement direction during 2afc'
r, pVal = stats.spearmanr(responseIndEachCell, movementModIEachCell)
print '\nSpearman correlation coefficient between sound response index and movement direction modulation index is:', r, 'p value is:', pVal

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
