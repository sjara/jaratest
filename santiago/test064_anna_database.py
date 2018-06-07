'''
WRITE DESCRIPTION HERE!

This script takes as argument the name of the animal to process.

TO DO:
- Make sure inforec files get reloaded (by celldatabase.py)
'''

import sys
import os
import pandas as pd
import numpy as np

from jaratoolbox import celldatabase
reload(celldatabase)
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
reload(settings)

from scipy import stats


#subject = 'band045'

if len(sys.argv)==2:
    subject = sys.argv[1]
else:
    raise ValueError('Please specify what subject to process (as an argument to this script).')

#inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
inforec = os.path.join(settings.INFOREC_PATH,'{0}_inforec.py'.format(subject))
db = celldatabase.generate_cell_database(inforec)


# NOTE: it seems unnecessary to create empty things at this point
"""
db = db.reindex(columns=np.concatenate((db.columns.values,['gaussFreqFit','bestFreqTuningWindow'])))
db['gaussFreqFit'] = db['gaussFreqFit'].astype(object)
db['bestFreqTuningWindow'] = db['bestFreqTuningWindow'].astype(object)
"""

# NOTE: this way to remove bad cells seems too convoluted
#db = db.drop(db[(db['isiViolations'] > 0.05) | (db['spikeShapeQuality'] < 2)].index).reset_index(drop=True)

# --- Keep only good cells ---
db = db[(db['isiViolations'] < 0.05) | (db['spikeShapeQuality'] > 2)]


# --- Determine laser responsiveness of each cell (using laser pulse) ---
print('Estimating laser responsiveness (laser pulse)')
laserTestStatistic = np.empty(len(db))
laserPVal = np.empty(len(db))

baseRange = [-0.05,-0.04]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]    # Time-bin size
responseRange = [0, 0+binTime]
fullTimeRange = [baseRange[0], responseRange[1]]

for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    try:
        laserEphysData, noBehav = cellObj.load('laserPulse')
    except IndexError:
        print "No laser session for this cell"
        testStatistic = 0
        pVal = 1
    else:
        laserEventOnsetTimes = laserEphysData['events']['laserOn']
        laserSpikeTimestamps = laserEphysData['spikeTimes']
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
            spikesanalysis.eventlocked_spiketimes(laserSpikeTimestamps,
                                                  laserEventOnsetTimes,
                                                  fullTimeRange)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                     indexLimitsEachTrial,
                                                                     baseRange)
        laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                      indexLimitsEachTrial,
                                                                      responseRange)
        [testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    laserTestStatistic[indRow] = testStatistic
    laserPVal[indRow] = pVal


db['laserPVal'] = laserPVal
db['laserUStat'] = laserTestStatistic


# --- Determine laser responsiveness of each cell (using laser train) ---
# code for this and above step are virtually identical, but copying here for transparency of what's going on
print('Estimating laser responsiveness (laser train)')
laserTrainTestStatistic = np.empty(len(db))
laserTrainPVal = np.empty(len(db))

baseRange = [-0.05,-0.04]              # Baseline range (in seconds)
binTime = baseRange[1]-baseRange[0]         # Time-bin size
responseRange = [0, 0+binTime]
fullTimeRange = [baseRange[0], responseRange[1]]

for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    try:
        laserTrainEphysData, noBehav = cellObj.load('laserTrain')
    except IndexError:
        print "No laser session for this cell"
        testStatistic = 0
        pVal = 1
    else:
        laserTrainEventOnsetTimes = laserTrainEphysData['events']['laserOn']
        laserTrainEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(laserTrainEventOnsetTimes, 0.5)
        laserTrainSpikeTimestamps = laserTrainEphysData['spikeTimes']
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
            spikesanalysis.eventlocked_spiketimes(laserTrainSpikeTimestamps,
                                                  laserTrainEventOnsetTimes,
                                                  fullTimeRange)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                     indexLimitsEachTrial,
                                                                     baseRange)
        laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                      indexLimitsEachTrial,
                                                                      responseRange)
        [testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    laserTrainTestStatistic[indRow] = testStatistic
    laserTrainPVal[indRow] = pVal

db['laserTrainPVal'] = laserTrainPVal
db['laserTrainUStat'] = laserTrainTestStatistic


# --- determine sound frequency tuning (gaussian fit for high amplitude trials) ---

# save db as h5 and csv

'''
dbFilename = os.path.join(settings.DATABASE_PATH,'{0}_test.h5'.format(subject))
db.to_hdf(dbFilename, 'database',mode='w')
print('Saved database to: {}'.format(dbFilename))

db.to_csv(dbFilename+'.csv')
print('Saved database to: {}'.format(dbFilename+'.csv'))
'''

dbFilenameNew = os.path.join(settings.DATABASE_PATH,'{0}_new.h5'.format(subject))
celldatabase.save_hdf(db, dbFilenameNew)
print('Saved database to: {}'.format(dbFilenameNew))

# -- To load the HDF5 --
# df = celldatabase.load_hdf('/tmp/band045_new.h5')




#db.to_csv(dbFilename+'.csv')
#db.to_hdf('/home/jarauser/data/database/{0}_test.h5'.format(subject), 'database')
#db.to_csv('/home/jarauser/data/database/{0}_test.csv'.format(subject))

'''
### TEST CODE ###

for col in db.columns: print('{} \t {}'.format(col,type(db[col][0])));

for col in db.columns: print('{} \t {}'.format(col, db[col][0]) );

dd = celldatabase.load_hdf('/tmp/band045_new.h5')
df=pd.DataFrame({'tetrode':dd['tetrode'], 'depth':dd['depth']})
df=pd.DataFrame({'tetrode':dd['tetrode'], 'date':dd['date']})
df=pd.DataFrame({'tetrode':dd['tetrode'], 'spikeShape':dd['spikeShape']}) # FAILS
df=pd.DataFrame({'tetrode':dd['tetrode'], 'ephysTime':dd['ephysTime']})

df = db.loc[:,['cluster','subject', 'isiViolations', 'spikeShapeQuality']]


'''
