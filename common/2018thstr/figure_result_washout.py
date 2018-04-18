import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from collections import Counter
from scipy import stats
import pandas as pd
import figparams
reload(figparams)

'''
Testing the idea that our results wash out if you include the close untagged cells, or if you only look at the
untagged cells. NOTE: It doesn't seem like the results change when we do this selection.
'''

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')

db = pd.read_hdf(dbPath, key='dataframe')
goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodNSpikes = goodShape.query('nSpikes>2000')

# cellsToUse = goodNSpikes.query('taggedCond==0 or taggedCond==1')
cellsToUse = goodNSpikes.query('taggedCond==0')
# cellsToUse = goodNSpikes.query('taggedCond==2')

ac = cellsToUse.groupby('brainArea').get_group('rightAC')
thal = cellsToUse.groupby('brainArea').get_group('rightThal')

features = ['highestSyncCorrected', 'mutualInfoBCBits']

for indFeature, feature in enumerate(features):
    dataAC = ac[feature][pd.notnull(ac[feature])]
    dataThal = thal[feature][pd.notnull(thal[feature])]

    zStat, pVal = stats.mannwhitneyu(dataAC, dataThal)
    print "{}: p={}".format(feature, pVal)

yLabels = ['Highest AM sync. rate (Hz)', 'MI (AM Rate, bits)', 'MI (AM Phase, bits)']

goodFit = cellsToUse.query('rsquaredFit > 0.08')
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

ac = goodFitToUse.groupby('brainArea').get_group('rightAC')
thal = goodFitToUse.groupby('brainArea').get_group('rightThal')

features = ['BW10', 'threshold', 'latency']

for indFeature, feature in enumerate(features):
    dataAC = ac[feature][pd.notnull(ac[feature])]
    dataThal = thal[feature][pd.notnull(thal[feature])]

    zStat, pVal = stats.mannwhitneyu(dataAC, dataThal)
    print "{}: p={}".format(feature, pVal)
