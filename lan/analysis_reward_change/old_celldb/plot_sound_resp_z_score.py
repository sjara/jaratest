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
zScoreGroups = []
for indRegion, brainRegion in enumerate(brainRegions):
    celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(brainRegion))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    goodQualCells = celldb.query('isiViolations<{} and shapeQuality>{} and consistentInFiring==True and keep_after_dup_test==True and inTargetArea==True and met_behav_criteria==True'.format(ISIcutoff, qualityThreshold))
    maxSoundZscore = goodQualCells.behavZscore.apply(lambda x: x[np.argmax(np.abs(x))])
    #soundResp = goodQualCells.behavZscore.apply(lambda x: np.max(np.abs(x)) >=  maxZThreshold)
    zScoreGroups.append(maxSoundZscore.values)

# -- Stats -- #
T, pVal = stats.ranksums(*zScoreGroups)
print 'sound response Z scores from both brain regions were compared using the Wilcoxon signed-rank test, p value is: {}'.format(pVal)

# -- Plot hist -- #
plt.clf()
binsEdges = np.linspace(-15,25,50)
plt.hist(zScoreGroups, bins=binsEdges, color=['darkgrey','k'], edgecolor='None', label=brainRegions)
plt.xlabel('Maximal sound Z score')
plt.ylabel('Number of cells')
plt.legend()
figTitle = 'max_sound_response_Zscore_all_good_cells'
T, pVal0 =  stats.wilcoxon(zScoreGroups[0])
plt.text(-8, 35, 'Test if {} Z score centered at 0, p value: {:.3f}'.format(brainRegions[0], pVal0))
T, pVal1 =  stats.wilcoxon(zScoreGroups[1])
plt.text(-8, 30, 'Test if {} Z score centered at 0, p value: {:.3E}'.format(brainRegions[1], pVal1))
plt.title(figTitle)
plt.text(-8, 40, 'Wilcoxon rank-sum test between group difference, p value: {:.3f}'.format(pVal))
figFullPath = os.path.join(outputDir, figTitle)
plt.savefig(figFullPath,format='png')
