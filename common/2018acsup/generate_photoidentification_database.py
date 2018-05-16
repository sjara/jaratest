import pandas as pd
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis

from scipy import stats


subject = 'band045'

inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
db = celldatabase.generate_cell_database(inforec)

db = db.reindex(columns=np.concatenate((db.columns.values,['gaussFreqFit','bestFreqTuningWindow'])))
db['gaussFreqFit'] = db['gaussFreqFit'].astype(object) 
db['bestFreqTuningWindow'] = db['bestFreqTuningWindow'].astype(object)
        
db = db.drop(db[(db['isiViolations'] > 0.05) | (db['spikeShapeQuality'] < 2)].index).reset_index(drop=True)

# --- determine laser responsiveness of each cell (using laser pulse) ---

laserTestStatistic = np.empty(len(db))
laserPVal = np.empty(len(db))

for indRow, dbRow in db.iterrows():
    
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
        baseRange = [-0.05,-0.04]              # Baseline range (in seconds)
        binTime = baseRange[1]-baseRange[0]         # Time-bin size
        responseRange = [0, 0+binTime]
        fullTimeRange = [baseRange[0], responseRange[1]]
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserSpikeTimestamps, 
                                                                                                                   laserEventOnsetTimes, 
                                                                                                                   fullTimeRange)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
        laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, responseRange)
        [testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    laserTestStatistic[indRow] = testStatistic
    laserPVal[indRow] = pVal
    
db['laserPVal'] = laserPVal
db['laserUStat'] = laserTestStatistic

# --- determine laser responsiveness of each cell (using laser train) ---
# code for this and above step are virtually identical, but copying here for transparency of what's going on

laserTrainTestStatistic = np.empty(len(db))
laserTrainPVal = np.empty(len(db))

for indRow, dbRow in db.iterrows():
    
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
        baseRange = [-0.05,-0.04]              # Baseline range (in seconds)
        binTime = baseRange[1]-baseRange[0]         # Time-bin size
        responseRange = [0, 0+binTime]
        fullTimeRange = [baseRange[0], responseRange[1]]
        spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(laserTrainSpikeTimestamps, 
                                                                                                                   laserTrainEventOnsetTimes, 
                                                                                                                   fullTimeRange)
        baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseRange)
        laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, responseRange)
        [testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    laserTrainTestStatistic[indRow] = testStatistic
    laserTrainPVal[indRow] = pVal
    
db['laserTrainPVal'] = laserTrainPVal
db['laserTrainUStat'] = laserTrainTestStatistic

# --- determine sound frequency tuning (gaussian fit for high amplitude trials) ---

# save db as h5 and csv
db.to_hdf('/home/jarauser/data/database/{0}_test.h5'.format(subject), 'database')
db.to_csv('/home/jarauser/data/database/{0}_test.csv'.format(subject))        
