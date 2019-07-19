import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import celldatabase
import pandas as pd
import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
db = celldatabase.load_hdf(dbPath)

#Database of good cells that are id'd as tagged and has short pulse latency.
goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")
goodPulseLatency = goodLaser.query('summaryPulseLatency<0.01')
goodNSpikes = goodPulseLatency.query('nSpikes>2000')

goodSoundResponsiveBool = (~pd.isnull(goodNSpikes['BW10'])) | (~pd.isnull(goodNSpikes['highestSyncCorrected'])) | (goodNSpikes['noiseZscore']<0.05)
goodSoundResponsive = goodNSpikes[goodSoundResponsiveBool]

goodSoundResponsive['fitMidPoint'] = np.sqrt(goodSoundResponsive['upperFreq']*goodSoundResponsive['lowerFreq'])
goodFit = goodSoundResponsive.query('rsquaredFit > 0.04')
goodFitToUse = goodFit.query('fitMidPoint<32000')

print goodSoundResponsive[['date', 'subject', 'autoTagged', 'brainArea', 'BW10', 'highestSync']].groupby(['autoTagged', 'brainArea']).agg(['count'])

print goodFitToUse[['date', 'subject', 'autoTagged', 'brainArea', 'BW10', 'highestSync']].groupby(['autoTagged', 'brainArea']).agg(['count'])



#Lets also look at the examples we use to make sure they are in the updated database.

#Frequency examples
db = goodFitToUse

# examples.update({'Thal0' : 'pinp026_2017-11-16_3256.0_TT6c3'})
#Frequency thalamus example
subject = 'pinp026'
date = '2017-11-16'
depth = 3256.0
tetrode = 6
cluster = 3


indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
print indRow

# examples.update({'AC0':'pinp016_2017-03-09_1904.0_TT6c6'})
#Frequency AC examples
subject = 'pinp016'
date = '2017-03-09'
depth = 1904.0
tetrode = 6
cluster = 6

indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
print indRow


### AM examples

db = goodNSpikes

#AC examples
# examples.update({'AC0' : 'pinp017_2017-03-23_1604.0_TT4c2'})
subject = 'pinp017'
date = '2017-03-23'
depth = 1604.0
tetrode = 4
cluster = 2

indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
print indRow

# examples.update({'AC1' : 'pinp017_2017-03-23_1414.0_TT5c6'})
subject = 'pinp017'
date = '2017-03-23'
depth = 1414.0
tetrode = 5
cluster = 6

indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
print indRow

#ATh
# examples.update({'Thal0' : 'pinp015_2017-02-15_2902.0_TT8c4'})

subject = 'pinp015'
date = '2017-02-15'
depth = 2902.0
tetrode = 8
cluster = 4

# indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
# print indRow

# examples.update({'Thal1' : 'pinp016_2017-03-16_3707.0_TT2c3'})

subject = 'pinp016'
date = '2017-03-16'
depth = 3707.0
tetrode = 2
cluster = 3

indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
print indRow
