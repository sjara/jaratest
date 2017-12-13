import sys
import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.stats as stats

STUDY_NAME = '2017rc'
brainRegions = ['astr', 'ac']

#modulationWindows = {'side-in':['-0.3--0.2s','-0.2--0.1s','-0.1-0s']} 

windowsToCompare = [('center-out','0.05-0.2s'), ('side-in','-0.15-0s')]
#windowsToCompare = [('center-out','0.05-0.25s'), ('side-in','-0.2-0s')]
freqLabels = ['Low','High']
movementDirections = ['Left', 'Right']

qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

plt.figure(figsize=(6,6))
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
dataDir = settings.DATABASE_PATH
outputDir = '/tmp/'
figFormat = 'png'

cellSelCriterion = 'center_out_mod' #'movement_selective'
for indRegion, brainRegion in enumerate(brainRegions):
    plt.clf()
#for animal in animalList:
    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    #celldbPath = os.path.join(dataDir, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- For mod index in different windows aligned to side-in for movement-selective cells, take the preferred direction -- #
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    movementSel = goodQualCells.movementModS < alphaLevel
    leftPreferred = (goodQualCells.movementModI < 0) & movementSel
    rightPreferred = (goodQualCells.movementModI > 0) & movementSel
    leftPreferredCells = goodQualCells[leftPreferred]
    rightPreferredCells = goodQualCells[rightPreferred]
    #allModInds = np.empty([sum(movementSel), len(windowsToCompare)])

    centerOutModLow = goodQualCells['modSigLow_0.05-0.35s_center-out'] < alphaLevel
    centerOutModLowCells = goodQualCells[centerOutModLow]
    centerOutModHigh = goodQualCells['modSigHigh_0.05-0.35s_center-out'] < alphaLevel
    centerOutModHighCells = goodQualCells[centerOutModHigh]
    allModInds = np.empty([sum(centerOutModLow)+sum(centerOutModHigh), len(windowsToCompare)])
    
    for ind,(alignment, modWindow) in enumerate(windowsToCompare):
        lowFreqModIndName = 'modIndLow_{}_{}'.format(modWindow, alignment)
        highFreqModIndName = 'modIndHigh_{}_{}'.format(modWindow, alignment)
        #thisWinModInd = np.r_[leftPreferredCells[lowFreqModIndName], rightPreferredCells[highFreqModIndName]]
        thisWinModInd = np.r_[centerOutModLowCells[lowFreqModIndName], centerOutModHighCells[highFreqModIndName]]
        thisWinModInd = np.abs(thisWinModInd)
        allModInds[:,ind] = thisWinModInd
        
    for row in range(allModInds.shape[0]):
        xVal = [0, 1]
        yVal = [allModInds[row, 0],allModInds[row, 1]]
        plt.plot(xVal, yVal, 'o-', color='grey')

    xtickLabels = ['_'.join(win) for win in windowsToCompare]
    plt.xticks(xVal, xtickLabels)
    plt.xlim([-0.5, 1.5])
    #plt.ylim([-0.05, 0.5])
    figTitle = '{}_{}_{}'.format(brainRegion, cellSelCriterion, '_'.join(xtickLabels))
    plt.title(figTitle)
    # -- Stats -- #
    tStat, pVal = stats.ttest_rel(allModInds[:, 0],allModInds[:, 1])
    print 'For {}, using paired t-test to compare absolute modulation index from {}, the t statistic is {}, p value is {}'.format(brainRegion, ' vs '.join(xtickLabels), tStat, pVal)
    plt.text(0, 0.35,'paired t p value: {}'.format(pVal))
    figFullPath = os.path.join(outputDir, figTitle)
    plt.savefig(figFullPath,format=figFormat)

    #plt.show()
    
