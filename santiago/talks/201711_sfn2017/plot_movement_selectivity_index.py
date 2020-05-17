import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


STUDY_NAME = '2017rc'
brainRegions = ['astr', 'ac']
qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

#outputDir = '/home/languo/data/ephys/reward_change_stats/reports/'
outputDir = '/tmp/'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)


figFormat = 'svg'
#movementIndGroups = []
#movementSigGroups = []
figSize = [5,5]
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')
gs = gridspec.GridSpec(1, 1)
gs.update(left=0.15, right=0.95, top=0.95, bottom=0.13)
ax = plt.subplot(gs[0,0])

if len(sys.argv) == 1:
    print 'Please input a number to indicate the brain region to plot, 0=astr, 1=ac'
elif len(sys.argv) > 1:
    brainRegion = brainRegions[int(sys.argv[1])]

    celldbPath = os.path.join(dataDir,'reward_change_{}.h5'.format(brainRegion))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    movementInd = -goodQualCells.movementModI
    movementSig = goodQualCells.movementModS
    print('I flipped the sign to use Contra-Ipsi')
    #movementIndGroups.append(movementInd)
    #movementSigGroups.append(movementSig)

    '''
    # -- Stats -- #
    T, pVal = stats.ranksums(*movementIndGroups)
    print 'movement selectivity index from both brain regions were compared using the Wilcoxon signed-rank test, p value is: {}'.format(pVal)
    '''
    # -- Plot hist -- #
    binsEdges = np.linspace(-1,1,20)
    movIndMean = np.mean(movementInd)
    sigMovementSel = movementSig < alphaLevel
    percentMovementSel = sum(sigMovementSel) / float(len(sigMovementSel)) * 100
    plt.hist([movementInd[sigMovementSel], movementInd[~sigMovementSel]], bins=binsEdges, stacked=True, color=['k','darkgrey'], edgecolor='None', label=['selective','not selective'])
    plt.xlabel('Index: (C-I)/(C+I)',fontsize=18)
    #plt.xlabel('Movement selectivity index')
    plt.ylabel('Number of cells',fontsize=18)
    #plt.legend()
    #plt.title(brainRegion)
    T, pVal =  stats.wilcoxon(movementInd.values)

    resultString = '{} movement selectivity index mean: {:.3f}, p value: {:.3E}\n {:.2f}% of good cells were movement selective'.format(brainRegion, movIndMean, pVal, percentMovementSel)
    #plt.text(-0.8, 30, resultString)
    print(resultString)
    figTitle = '{}_movement_selectivity_index'.format(brainRegion)

    extraplots.set_ticks_fontsize(ax,16)
    extraplots.boxoff(plt.gca())
    plt.show()

    figFullPath = os.path.join(outputDir, figTitle)
    print 'Saving {} to {}'.format(figTitle, outputDir)
    #plt.savefig(figFullPath,format=figFormat)
    extraplots.save_figure(figTitle, figFormat, figSize, outputDir)
