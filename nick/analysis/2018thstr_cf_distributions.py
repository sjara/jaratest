import pandas as pd
import os
import numpy as np
from jaratoolbox import settings
from matplotlib import pyplot as plt
from scipy import stats

STUDY_NAME = '2018thstr'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
db = pd.read_hdf(dbPath, key='dataframe')

goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
goodFit = goodLaser.query('rsquaredFit > 0.04')
goodFitToUse = goodFit.query('nSpikes>2000')

dataframe = goodFitToUse
ac = dataframe.groupby('brainArea').get_group('rightAC')
thal = dataframe.groupby('brainArea').get_group('rightThal')

acData = np.log2(ac['cf'][~pd.isnull(ac['cf'])])
thalData = np.log2(thal['cf'][~pd.isnull(thal['cf'])])

nBins = 20
freqBins = np.logspace(np.log2(2000), np.log2(40000), nBins, base=2.0)
binEdges = np.log2(freqBins)
# binEdges = freqBins
freqBinLabels = ['{:0.1f}'.format(freq/1000) for freq in freqBins]

plt.clf()
plt.hist(acData, binEdges, histtype='step', color='r', label="AC:Str")
plt.hist(thalData, binEdges, histtype='step', color='b', label="ATh:Str")
ax = plt.gca()
ax.set_xticks(binEdges)
ax.set_xticklabels(freqBinLabels)
ax.set_xlabel('Frequency of CF (kHz)')
ax.set_ylabel('Number of cells')
plt.legend()
plt.show()

stat, pVal = stats.mannwhitneyu(acData, thalData)
print "p-value for Mann-Whitney test: {}".format(pVal)

plt.savefig('/tmp/cf_distribution.png')

