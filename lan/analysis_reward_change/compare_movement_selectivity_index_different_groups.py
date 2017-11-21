import os
import sys
import itertools
import pandas as pd
import numpy as np
import scipy.stats as stats
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt

STUDY_NAME_1 = '2016astr'
STUDY_NAME_2 = '2017rc'
brainRegions = ['astr', 'ac']
qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05
qualityList = [1,6]

#outputDir = '/home/languo/data/ephys/reward_change_stats/reports/'
outputDir = '/tmp/'

plt.figure()
figFormat = 'svg'

movementIndGroups = []
movementSigGroups = []
groupLabels = ['rcAc','rcAStr','swAStr','pcAStr']

rcAcCelldbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME_2, 'reward_change_ac.h5')
rcAcCelldb = pd.read_hdf(rcAcCelldbPath, key='reward_change')
rcAcGoodQualCells = rcAcCelldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
rcAcMovementInd = rcAcGoodQualCells.movementModI
rcAcMovementSig = rcAcGoodQualCells.movementModS
movementIndGroups.append(rcAcMovementInd)
movementSigGroups.append(rcAcMovementSig)

rcAstrCelldbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME_2, 'reward_change_astr.h5')
rcAstrCelldb = pd.read_hdf(rcAstrCelldbPath, key='reward_change')
rcAstrGoodQualCells = rcAstrCelldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
rcAstrMovementInd = rcAstrGoodQualCells.movementModI
rcAstrMovementSig = rcAstrGoodQualCells.movementModS
movementIndGroups.append(rcAstrMovementInd)
movementSigGroups.append(rcAstrMovementSig)

swAstrCelldbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME_1, 'all_cells_all_measures_extra_mod_waveform_switching.h5')
swAstrCelldb = pd.read_hdf(swAstrCelldbPath, key='switching')
swAstrGoodQualCells = swAstrCelldb.query('ISI<={} and keep_after_dup_test==True and cellInStr==1'.format(ISIcutoff, qualityThreshold))
swAstrGoodQualCells = swAstrGoodQualCells.loc[swAstrGoodQualCells.cellQuality.isin(qualityList)]
swAstrMovementInd = swAstrGoodQualCells.movementModI
swAstrMovementSig = swAstrGoodQualCells.movementModS
movementIndGroups.append(swAstrMovementInd)
movementSigGroups.append(swAstrMovementSig)

pcAstrCelldbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME_1, 'all_cells_all_measures_waveform_psychometric.h5')
pcAstrCelldb = pd.read_hdf(pcAstrCelldbPath, key='psychometric')
pcAstrGoodQualCells = pcAstrCelldb.query('ISI<={} and keep_after_dup_test==True and cellInStr==1'.format(ISIcutoff, qualityThreshold))
pcAstrGoodQualCells = pcAstrGoodQualCells.loc[pcAstrGoodQualCells.cellQuality.isin(qualityList)]
pcAstrMovementInd = pcAstrGoodQualCells.movementModI
pcAstrMovementSig = pcAstrGoodQualCells.movementModS
movementIndGroups.append(pcAstrMovementInd)
movementSigGroups.append(pcAstrMovementSig)

# -- Stats -- #
T, pVal = stats.kruskal(*movementIndGroups)
print 'movement selectivity index from different groups were compared using the Kruskal-Wallis H-test, p value is: {}'.format(pVal)
pairsOfGroups = list(itertools.combinations(movementIndGroups, 2))
pairsLabels = list(itertools.combinations(groupLabels, 2))
for label,pair in zip(pairsLabels, pairsOfGroups):
    T, pVal = stats.ranksums(*pair)
    print 'comparing {} using ranksum test, p = {:.3f}'.format(label, pVal)

'''
# -- Plot hist -- #
for ind, movementInd in enumerate(movementIndGroups):
    plt.clf()
    binsEdges = np.linspace(-1,1,20)
    movIndMean = np.mean(movementInd)
    movementSig = movementSigGroups[ind]
    sigMovementSel = movementSig < alphaLevel
    percentMovementSel = sum(sigMovementSel) / float(len(sigMovementSel)) * 100
    plt.hist([movementInd[sigMovementSel], movementInd[~sigMovementSel]], bins=binsEdges, stacked=True, color=['k','darkgrey'], edgecolor='None', label=['selective','not selective'])
    plt.xlabel('Movement selectivity index')
    plt.ylabel('Number of cells')
    plt.legend()
    plt.title(groupLabels[ind])
    T, pVal =  stats.wilcoxon(movementInd.values)
    plt.text(-0.8, 0.5*plt.ylim()[1], '{} movement selectivity index mean: {:.3f}, p value: {:.3E}\n {:.2f}% of good cells were movement selective'.format(groupLabels[ind], movIndMean, pVal, percentMovementSel))
    figTitle = '{} movement selectivity index'.format(groupLabels[ind])

    figFullPath = os.path.join(outputDir, figTitle)
    print 'Saving {} to {}'.format(figTitle, outputDir)
    plt.savefig(figFullPath,format=figFormat)
    plt.show()

'''
