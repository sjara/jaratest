import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
import pandas as pd
import figparams #TODO: Remove this once we move plotting code to a figure file
import matplotlib.pyplot as plt
from scipy import stats


dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_calculated_columns.h5'
database = celldatabase.load_hdf(dbPath)


goodISI = database.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")

goodFit = goodLaser.query('rsquaredFit > 0.04')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')
goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')
# goodPulseLatency = goodFitToUseNSpikes.query('summaryPulseLatency<0.014')
goodPulseLatency = goodFitToUseNSpikes.query('summaryPulseLatency<0.01')

dbToUse = goodPulseLatency

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

plt.clf()
ax = plt.subplot(111)
colorATh = 'b'
colorAC = 'r'

ac = dbToUse.groupby('brainArea').get_group('rightAC')
thal = dbToUse.groupby('brainArea').get_group('rightThal')

popStatCol = 'monotonicityIndex'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
ax.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None')
# medline(axBW, np.median(thalPopStat), 0, 0.5)
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
ax.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None')
ax.set_ylabel('Monotonicity index')
ax.set_xticks([0, 1])
ax.set_xticklabels(['ATh:Str', 'AC:Str'])

zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)
print pVal
