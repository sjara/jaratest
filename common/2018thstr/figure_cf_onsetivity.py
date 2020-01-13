import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
import pandas as pd
import figparams
import matplotlib.pyplot as plt
from scipy import stats


db = celldatabase.load_hdf('/tmp/database_with_cf_onsetivity.h5')

db['cfOnsetivityIndex'] = (db['sustainedRateCF'] - db['onsetRateCF']) / (db['sustainedRateCF'] + db['onsetRateCF'])

goodFit = db.query('rsquaredFit > 0.04')

plt.clf()

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')
goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')
goodPulseLatency = goodFitToUseNSpikes.query('summaryPulseLatency<0.01')

#Which dataframe to use
# dataframe = goodFitToUseNSpikes
dataframe = goodPulseLatency

ac = dataframe.groupby('brainArea').get_group('rightAC')
thal = dataframe.groupby('brainArea').get_group('rightThal')
colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']

popStatCol = 'cfOnsetivityIndex'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

markerAlpha = 1
ax = plt.subplot(111)
pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
ax.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)

pos = jitter(np.ones(len(acPopStat))*1, 0.20)
ax.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)

medline(ax, np.nanmedian(thalPopStat), 0, 0.4)
medline(ax, np.nanmedian(acPopStat), 1, 0.4)

ax.set_ylabel('Onsetivity index')
ax.set_xticks([0, 1])
ax.set_xticklabels(['ATh:Str', 'AC:Str'])

# ax.set_ylim([-5, 5])

plt.show()

zstat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)
