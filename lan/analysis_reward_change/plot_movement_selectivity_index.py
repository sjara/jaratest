import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from jaratoolbox import settings
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
import pdb


brainRegions = ['astr', 'ac']
qualityThreshold = 3 #2.5 
maxZThreshold = 3
ISIcutoff = 0.02
alphaLevel = 0.05

outputDir = '/home/languo/data/ephys/reward_change_stats/reports/'

plt.figure()
movementIndGroups = []
movementSigGroups = []
for indRegion, brainRegion in enumerate(brainRegions):
    celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(brainRegion))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    movementInd = goodQualCells.movementModI
    movementSig = goodQualCells.movementModS
    movementIndGroups.append(movementInd)
    movementSigGroups.append(movementSig)

# -- Stats -- #
T, pVal = stats.ranksums(*movementIndGroups)
print 'movement selectivity index from both brain regions were compared using the Wilcoxon signed-rank test, p value is: {}'.format(pVal)

# -- Plot hist -- #
plt.clf()
binsEdges = np.linspace(-1,1,20)
plt.subplot(211)
astrInds = movementIndGroups[0]
astrIndMean = np.mean(astrInds)
astrSig = movementSigGroups[0] < alphaLevel
percentMovementSelAStr = sum(astrSig) / float(len(astrSig)) * 100
plt.hist([astrInds[astrSig], astrInds[~astrSig]], bins=binsEdges, color=['k','darkgrey'], edgecolor='None', label=['selective','not selective'])
#plt.xlabel('Movement selectivity index')
plt.ylabel('Number of cells')
plt.legend()
plt.title('AStr')
T, pVal0 =  stats.wilcoxon(movementIndGroups[0].values)
plt.text(-0.8, 30, '{} movement selectivity index mean: {:.3f}, p value: {:.3f}\n {:.2f} percent of good cells were movement selective'.format(brainRegions[0], astrIndMean, pVal0, percentMovementSelAStr))

plt.subplot(212)
acInds = movementIndGroups[1]
acIndMean = np.mean(acInds)
acSig = movementSigGroups[1] < alphaLevel
percentMovementSelAC = sum(acSig) / float(len(acSig)) * 100
plt.hist([acInds[acSig], acInds[~acSig]], bins=binsEdges, color=['k','darkgrey'], edgecolor='None', label=['selective','not selective'])
plt.xlabel('Movement selectivity index')
plt.ylabel('Number of cells')
plt.legend()
plt.title('AC')
T, pVal1 =  stats.wilcoxon(movementIndGroups[1].values)
plt.text(-0.8, 30, '{} movement selectivity index mean: {:.3f}, p value: {:.3E}\n {:.2f} percent of good cells were movement selective'.format(brainRegions[1], acIndMean, pVal1,percentMovementSelAC))
figTitle = 'movement_selectivity_all_good_cells'

plt.suptitle(figTitle + '\nWilcoxon rank-sum test between group difference, p value: {:.3f}'.format(pVal))
plt.tight_layout()
figFullPath = os.path.join(outputDir, figTitle)
plt.savefig(figFullPath,format='png')
