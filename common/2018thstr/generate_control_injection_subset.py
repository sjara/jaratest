import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import figparams
reload(extraplots)
reload(figparams)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_with_latency.h5')
db = pd.read_hdf(dbPath, key='dataframe')

goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
goodStriatum = db.groupby('brainArea').get_group('rightAstr').query('isiViolations<0.02 and spikeShapeQuality>2')
goodLaserPlusStriatum = goodLaser.append(goodStriatum, ignore_index=True)
goodFit = goodLaserPlusStriatum.query('rsquaredFit > 0.08')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

#Which dataframe to use
# dataframe = goodFit
dataframe = goodFitToUse
groups = dataframe.groupby('brainArea')

goodMice = ['pinp016', 'pinp017']
ath = dataframe.groupby('brainArea').get_group('rightThal')
athSubgroup = ath.query('subject in @goodMice')

ac = dataframe.groupby('brainArea').get_group('rightAC')
acSubgroup = ac.query('subject in @goodMice')

#Figure 2 stats
features = ['BW10', 'threshold', 'latency', 'highestSyncCorrected', 'mutualInfoPerSpike']
for feature in features:
    stat, pVal = stats.ranksums(athSubgroup[feature], acSubgroup[feature])
    print "ranksums test for feature: {}, pval={}".format(feature, pVal)
