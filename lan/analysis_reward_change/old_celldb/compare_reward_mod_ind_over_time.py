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

useStrictBehavCriterion = True
cellSelCriterion = 'either_period_modulated' #'side_in_mod'  #'movement_selective' 'center_out_mod'

for indRegion, brainRegion in enumerate(brainRegions):
    plt.clf()
#for animal in animalList:
    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    #celldbPath = os.path.join(dataDir, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')

    # -- For mod index in different windows aligned to side-in for movement-selective cells, take the preferred direction -- #
    if useStrictBehavCriterion:
        goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria_strict==True'.format(ISIcutoff, qualityThreshold))
    else:
        goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    
    print '{}, {} good quality cells'.format(brainRegion, len(goodQualCells))

    movementSel = goodQualCells.movementModS < alphaLevel
    print '{}, {} movement selective cells'.format(brainRegion, sum(movementSel))
    leftPreferred = (goodQualCells.movementModI < 0) & movementSel
    rightPreferred = (goodQualCells.movementModI > 0) & movementSel
    leftPreferredCells = goodQualCells[leftPreferred]
    rightPreferredCells = goodQualCells[rightPreferred]
    
    centerOutModLow = goodQualCells['modSigLow_0.05-0.35s_center-out'] < alphaLevel
    centerOutModLowCells = goodQualCells[centerOutModLow]
    centerOutModHigh = goodQualCells['modSigHigh_0.05-0.35s_center-out'] < alphaLevel
    centerOutModHighCells = goodQualCells[centerOutModHigh]
    print '{}, {} center-out modulated cells'.format(brainRegion, sum(centerOutModLow)+sum(centerOutModHigh))
    
    sideInModLow = goodQualCells['modSigLow_-0.3-0s_side-in'] < alphaLevel
    sideInModLowCells = goodQualCells[sideInModLow]
    sideInModHigh = goodQualCells['modSigHigh_-0.3-0s_side-in'] < alphaLevel
    sideInModHighCells = goodQualCells[sideInModHigh]
    print '{}, {} side-in modulated cells'.format(brainRegion, sum(sideInModLow)+sum(sideInModHigh)) 
    
    eitherPeriodModLow = centerOutModLow | sideInModLow
    eitherPeriodModHigh = centerOutModHigh | sideInModHigh
    eitherPeriodModLowCells =  goodQualCells[eitherPeriodModLow]
    eitherPeriodModHighCells =  goodQualCells[eitherPeriodModHigh]
    print '{}, {} cells modulated either during center-out and side-in'.format(brainRegion, sum(eitherPeriodModLow)+sum(eitherPeriodModHigh)) 

    if cellSelCriterion == 'center_out_mod':
        allModInds = np.empty([sum(centerOutModLow)+sum(centerOutModHigh), len(windowsToCompare)])
    elif cellSelCriterion == 'movement_selective':
        allModInds = np.empty([sum(movementSel), len(windowsToCompare)])
    elif cellSelCriterion == 'side_in_mod':
        allModInds = np.empty([sum(sideInModLow)+sum(sideInModHigh), len(windowsToCompare)])
    elif cellSelCriterion == 'either_period_modulated':
        allModInds = np.empty([sum(eitherPeriodModLow)+sum(eitherPeriodModHigh), len(windowsToCompare)])
        
    for ind,(alignment, modWindow) in enumerate(windowsToCompare):
        lowFreqModIndName = 'modIndLow_{}_{}'.format(modWindow, alignment)
        highFreqModIndName = 'modIndHigh_{}_{}'.format(modWindow, alignment)
        if cellSelCriterion == 'center_out_mod':
            thisWinModInd = np.r_[centerOutModLowCells[lowFreqModIndName], centerOutModHighCells[highFreqModIndName]]
        elif cellSelCriterion == 'movement_selective':
            thisWinModInd = np.r_[leftPreferredCells[lowFreqModIndName], rightPreferredCells[highFreqModIndName]]
        elif cellSelCriterion == 'side_in_mod':
            thisWinModInd = np.r_[sideInModLowCells[lowFreqModIndName], sideInModHighCells[highFreqModIndName]]
        elif cellSelCriterion == 'either_period_modulated':
            thisWinModInd = np.r_[eitherPeriodModLowCells[lowFreqModIndName], eitherPeriodModHighCells[highFreqModIndName]]
        thisWinModInd = np.abs(thisWinModInd)
        allModInds[:,ind] = thisWinModInd
        
    increasedPairCount = 0
    decreasedPairCount = 0
    for row in range(allModInds.shape[0]):
        xVal = [0, 1]
        yVal = [allModInds[row, 0],allModInds[row, 1]]
        plt.plot(xVal, yVal, 'o-', mec='grey', mfc='None', color='grey')
        if yVal[1] > yVal[0]:
            increasedPairCount += 1
        elif yVal[1] < yVal[0]:
            decreasedPairCount += 1

    plt.errorbar(0, np.mean(allModInds[:,0]), yerr=np.std(allModInds[:,0]), marker='s', mfc='red', mec='green', ms=20, ecolor='red', elinewidth=3, barsabove=True)
    plt.errorbar(1, np.mean(allModInds[:,1]), yerr=np.std(allModInds[:,1]), marker='s', mfc='red', mec='green', ms=20, ecolor='red', elinewidth=3, barsabove=True)
    xtickLabels = ['_'.join(win) for win in windowsToCompare]
    plt.xticks(xVal, xtickLabels)
    plt.xlim([-0.5, 1.5])
    #plt.ylim([-0.05, 0.5])
    figTitle = '{}_{}_{}'.format(brainRegion, cellSelCriterion, '_'.join(xtickLabels))
    plt.title(figTitle)
    # -- Stats -- #
    tStat, pVal = stats.ttest_rel(allModInds[:, 0],allModInds[:, 1])
    print 'For {}, using paired t-test to compare absolute modulation index from {}, the t statistic is {}, p value is {}. {} cell increased modulation index overtime, {} cell decreased modulation index overtime.'.format(brainRegion, ' vs '.join(xtickLabels), tStat, pVal, increasedPairCount, decreasedPairCount)
    plt.text(0, plt.ylim()[1]-0.05,'paired t p value: {}'.format(pVal))
    figFullPath = os.path.join(outputDir, figTitle)
    plt.savefig(figFullPath,format=figFormat)

    #plt.show()
    
