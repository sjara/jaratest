import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats


dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, 'dataframe')

currentLaserQuery = 'pulsePval < 0.05 and trainRatio > 0.8'
# newLaserQuery = 'pulsePval < 0.05 and pulseZscore > 0 and trainRatio > 0.3'
# newLaserQuery = 'pulsePval < 0.05 and pulseZscore > 0'

currentDB = db.query(currentLaserQuery)
newDB = db.query(newLaserQuery)
dbToUse = newDB

colNames = ['BW10', 'highestSyncCorrected', 'mutualInfoBCBits', 'mutualInfoPerSpikeBits']
thalDB = dbToUse.groupby('brainArea').get_group('rightThal')
acDB = dbToUse.groupby('brainArea').get_group('rightAC')

plt.close('all')
for indCol, colName in enumerate(colNames):
    # plt.figure()
    # plt.subplot(1, len(colNames), indCol+1)
    dbToUse.boxplot(column=colName, by='brainArea')
    thalData = thalDB[colName][pd.notnull(thalDB[colName])]
    acData = acDB[colName][pd.notnull(acDB[colName])]
    zVal, pVal = stats.mannwhitneyu(thalData, acData)
    print "{}, p={}".format(colName, pVal)
plt.show()

