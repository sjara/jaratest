import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt


STUDY_NAME = '2017rc'
brainRegions = ['astr', 'ac']
qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

#outputDir = '/home/languo/data/ephys/reward_change_stats/reports/'
outputDir = '/tmp/'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)

plt.figure()
figFormat = 'svg'
#movementIndGroups = []
#movementSigGroups = []

if len(sys.argv) == 1:
    print 'Please input a number to indicate the brain region to plot, 1=ac, 2=astr'
elif len(sys.argv) > 1:
    brainRegion = brainRegions[int(sys.argv[1])]

    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    movementInd = goodQualCells.movementModI
    movementSig = goodQualCells.movementModS
    #movementIndGroups.append(movementInd)
    #movementSigGroups.append(movementSig)

    '''
    # -- Stats -- #
    T, pVal = stats.ranksums(*movementIndGroups)
    print 'movement selectivity index from both brain regions were compared using the Wilcoxon signed-rank test, p value is: {}'.format(pVal)
    '''
    # -- Plot hist -- #
    plt.clf()
    binsEdges = np.linspace(-1,1,20)
    movIndMean = np.mean(movementInd)
    sigMovementSel = movementSig < alphaLevel
    percentMovementSel = sum(sigMovementSel) / float(len(sigMovementSel)) * 100
    plt.hist([movementInd[sigMovementSel], movementInd[~sigMovementSel]], bins=binsEdges, stacked=True, color=['k','darkgrey'], edgecolor='None', label=['selective','not selective'])
    plt.xlabel('Movement selectivity index')
    plt.ylabel('Number of cells')
    plt.legend()
    plt.title(brainRegion)
    T, pVal =  stats.wilcoxon(movementInd.values)
    plt.text(-0.8, 30, '{} movement selectivity index mean: {:.3f}, p value: {:.3E}\n {:.2f}% of good cells were movement selective'.format(brainRegion, movIndMean, pVal, percentMovementSel))
    figTitle = '{} movement selectivity index'.format(brainRegion)

    figFullPath = os.path.join(outputDir, figTitle)
    print 'Saving {} to {}'.format(figTitle, outputDir)
    plt.savefig(figFullPath,format=figFormat)
