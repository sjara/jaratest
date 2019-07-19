import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import figparams
reload(figparams)


# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
dbPath = '/tmp/db_with_am_onsetivity.h5'
db = celldatabase.load_hdf(dbPath)

goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
# goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018' and summaryPulseLatency < 0.01")
goodNSpikes = goodLaser.query('nSpikes>2000')
goodPulseLatency = goodNSpikes.query('summaryPulseLatency<0.006')

dbToUse = goodNSpikes

dbToUse['amOnsetivityIndex'] = (dbToUse['onsetRate'] - dbToUse['sustainedRate']) / (dbToUse['sustainedRate'] + dbToUse['onsetRate'])

ac = dbToUse.groupby('brainArea').get_group('rightAC')
thal = dbToUse.groupby('brainArea').get_group('rightThal')

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

plt.clf()
ax = plt.subplot(111)

colorATh = 'b'
colorAC = 'r'
dataMS = 4

popStatCol = 'amOnsetivityIndex'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

jitterFrac = 0.2
pos = jitter(np.ones(len(thalPopStat))*0, jitterFrac)
ax.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=1, ms=dataMS)
medline(np.median(thalPopStat), 0, 0.5)
pos = jitter(np.ones(len(acPopStat))*1, jitterFrac)
ax.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=1, ms=dataMS)
medline(np.median(acPopStat), 1, 0.5)
tickLabels = ['ATh:Str'.format(len(thalPopStat)), 'AC:Str'.format(len(acPopStat))]
ax.set_xticks(range(2))
ax.set_xticklabels(tickLabels)
ax.set_ylabel('AM onsetivity index')

plt.show()

zStat, pVal = stats.mannwhitneyu(thalPopStat, acPopStat)
print pVal


