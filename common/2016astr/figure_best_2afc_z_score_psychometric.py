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

FIGNAME = '2afc_Z_score_psychometric'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

#dataDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)

SAVE_FIGURE = 1
outputDir = '/home/languo/tmp/'
figFilename = 'figure_2afc_z_score_psychometric' # Do not include extension
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
numFreqs = 6
bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs

summaryFilename = 'summary_2afc_best_freq_maxZ_psychometric.npz'
summaryFullPath = os.path.join(dataDir,summaryFilename)
summary = np.load(summaryFullPath)

# -- This file stores which frequencies were used in each behav session -- #
sessionFreqsFilename = 'psycurve_animal_2afc_freqs_each_session.h5'
sessionFreqsFullPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, sessionFreqsFilename)
sessionFreqs = pd.read_hdf(sessionFreqsFullPath, key='psychometric')

# -- This file stores all cells all measures, including behav session name of each cell recorded -- #
psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

####################################################################################3
cellSelectorBoolArray = summary['cellSelectorBoolArray']
bestFreqEachCell = summary['bestFreqEachCell'][cellSelectorBoolArray]
#bestFreqEachCell = bestFreqEachCell[bestFreqEachCell!=0]
maxZscoreEachCell = summary['maxZscoreEachCell'][cellSelectorBoolArray]
#maxZscoreEachCell = maxZscoreEachCell[maxZscoreEachCell!=0]
responseIndEachCell = summary['responseIndEachCell'][cellSelectorBoolArray]

# -- summary stats about sound responsiveness (rank sum test significant) and frequency selectivity (ANOVA test significant) -- #
sigSoundResponse = (summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= bonferroniCorrectedAlphaLevel)
# Only consider whether frequency selective if sigSoundResponsive!
freqSelective =(summary['pValSoundResponseEachCell'][cellSelectorBoolArray] <= bonferroniCorrectedAlphaLevel) & (summary['freqSelectivityEachCell'][cellSelectorBoolArray] <= alphaLevel)

# -- Panel A: histogram of maximum sound response Z score for all good cells -- #
ax1 = plt.subplot(gs[0,0])
plt.hist((responseIndEachCell[sigSoundResponse],responseIndEachCell[~sigSoundResponse]), color=['k','None'], bins=20)
plt.xlabel('Maximum sound response index')
plt.ylabel('Number of cells')
sig_patch = mpatches.Patch(color='k', label='Sound responsive')
nonsig_patch = mpatches.Patch(facecolor='None', edgecolor='k', label='Not sound responsive')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)

# -- Panel B: histogram of most responsive frequency for all good cells -- #
ax2 = plt.subplot(gs[0,1])

freqSelectiveCells = allcells_psychometric[cellSelectorBoolArray][freqSelective]        
freqSelectiveCells['bestFreq'] = bestFreqEachCell[freqSelective]
numResponsiveContra = 0
numResponsiveIpsi = 0
freqInd = np.array([], dtype=int)

for ind,cell in freqSelectiveCells.iterrows():
    animalName = cell['animalName']
    behavSession = cell['behavSession']
    thisSession = sessionFreqs.loc[(sessionFreqs['animalName']==animalName) & (sessionFreqs['behavSession']==behavSession)]
    freqsThisSession = thisSession.loc[:,'freq1':'freq6'].transpose().values
    numFreqs = len(freqsThisSession)
    boundaryThisSession = np.logspace(np.log2(float(freqsThisSession[numFreqs/2-1])), np.log2(float(freqsThisSession[numFreqs/2])), base=2, num=3)[1]
    if cell['bestFreq'] <= boundaryThisSession:
        numResponsiveContra += 1
    elif cell['bestFreq'] > boundaryThisSession:
        numResponsiveIpsi += 1
    freqInd = np.append(freqInd, (np.flatnonzero(freqsThisSession == cell['bestFreq'])+1))

plt.hist(freqInd)
plt.xlim([0,7])
plt.xticks(range(1,7), ['1','2','3','4','5','6'])
plt.xlabel('Index of most responsive frequency (Hz) in psychometric curve')
plt.ylabel('Number of cells')
plt.show()
'''
# -- Plots the most responsive frequency in 2afc task for each cell, but did not contain info about whether this frequency is 'low' or 'high' for a given session -- # 
plt.hist((bestFreqEachCell[freqSelective],bestFreqEachCell[~freqSelective]), color=['k','None'], bins=20)
plt.xlabel('Most responsive frequency (Hz)')
plt.ylabel('Number of cells')
sig_patch = mpatches.Patch(color='k', label='Frequency selective')
nonsig_patch = mpatches.Patch(facecolor='None', edgecolor='k',label='Not frequency selective')
plt.legend(handles=[sig_patch,nonsig_patch], loc='upper center', fontsize=fontSizeTicks, frameon=False, labelspacing=0.1, handlelength=0.2)
plt.show()
'''

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# -- Stats summary-- #
numCells = sum(cellSelectorBoolArray)
print 'total number of good cells:', numCells
numSoundResCells = sum(sigSoundResponse.astype(int))
print 100*float(numSoundResCells)/numCells, '% of cells show significant sound response (after Bonferroni correction)'
numFreqSelectiveCells = sum(freqSelective.astype(int))
print 100*float(numFreqSelectiveCells)/numCells, '% of cells show significant frequency selectivity'
print numResponsiveContra, 'cells were selective for frequencies associated with contralateral reward port, while', numResponsiveIpsi, 'cells were selective for frequencies associated with ipsilateral reward port.'


