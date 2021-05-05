'''
This script generates data for ephys recordings from a pv-archt animal showing a change in activity.
'''
import os
import sys
import numpy as np
from scipy import stats

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis

import studyparams


# -- functions assisting in clustering and cluster rescue --
def cluster_spike_data(subjects):
    for subject in subjects:
        inforecPath = os.path.join(settings.INFOREC_PATH, '{0}_inforec.py'.format(subject))
        ci = spikesorting.ClusterInforec(inforecPath)
        ci.process_all_experiments()

# -- function for calculating responses from spike data --
def laser_response(ephysData, baseRange=[-0.05, -0.04], responseRange=[0.0, 0.01]):
    '''Compares firing rate during laser response range and base range.

    Inputs:
        ephysData: full dictionary of ephys data for laser pulse (or train) session
        baseRange: time range (relative to laser onset) to be used as baseline, list of [start time, end time]
        responseRange: time range (relative to laser onset) to be used as response, list of [start time, end time]

    Outputs:
        testStatistic: U test statistic of ranksums test between baseline and response
        pVal: p-value of ranksums test between baseline and response
        laserChangeFR: change in firing rate from baseline to response
    '''
    fullTimeRange = [baseRange[0], responseRange[1]]
    eventOnsetTimes = ephysData['events']['laserOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)
    spikeTimestamps = ephysData['spikeTimes']
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
        spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                              eventOnsetTimes,
                                              fullTimeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                 indexLimitsEachTrial,
                                                                 baseRange)
    laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                  indexLimitsEachTrial,
                                                                  responseRange)
    [testStatistic, pVal] = stats.ranksums(laserSpikeCountMat, baseSpikeCountMat)
    baseFR = np.mean(baseSpikeCountMat) / (baseRange[1] - baseRange[0])
    laserFR = np.mean(laserSpikeCountMat) / (responseRange[1] - responseRange[0])
    return testStatistic, pVal, laserFR, baseFR

# -- sound response from bw sessions: calcualted average firing rate with and without laser stim --
def laser_sound_response(ephysData, behavData, baseRange=[-0.05, -0.04], responseRange=[0.0, 0.01]):
    fullTimeRange = [baseRange[0], responseRange[1]]
    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.5)
    spikeTimestamps = ephysData['spikeTimes']
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = \
        spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                              eventOnsetTimes,
                                              fullTimeRange)
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                 indexLimitsEachTrial,
                                                                 baseRange)
    laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                  indexLimitsEachTrial,
                                                                  responseRange)

    laserEachTrial = behavData['laserTrial']
    numLaser = np.unique(laserEachTrial)
    trialsEachCond = behavioranalysis.find_trials_each_type(laserEachTrial, numLaser)

    firingRates = []
    spikeCounts = []
    baselineCounts = baseSpikeCountMat.flatten()
    firingRates.append(np.mean(baselineCounts))

    for indLaser in range(len(numLaser)):
        trialsThisLaser = trialsEachCond[:, indLaser]
        if laserSpikeCountMat.shape[0] == len(trialsThisLaser)+1:
            laserSpikeCountMat = laserSpikeCountMat[:-1,:]
        thisLaserCounts = laserSpikeCountMat[trialsThisLaser].flatten()
        firingRates.append(np.mean(thisLaserCounts))
        spikeCounts.append(thisLaserCounts)

    [testStatistic, pVal] = stats.ranksums(spikeCounts[0], spikeCounts[1])

    return testStatistic, pVal, firingRates

# -- cluster your data --
mouse = 'band075'
# cluster_spike_data([mouse])

# -- creates and saves a database for inactivation --
dbFilename = '/tmp/band075_cells.h5'  # save database in a temporary place, move it when you're satisfied with it
basicDB = celldatabase.generate_cell_database_from_subjects([mouse])

allBaselineTestStatistic = np.empty(len(basicDB))
allBaselinePVal = np.empty(len(basicDB))
allBaselineLaserFR = np.empty(len(basicDB))
allBaselineFR = np.empty(len(basicDB))

allSoundTestStatistic = np.empty(len(basicDB))
allSoundPVal = np.empty(len(basicDB))
allBandBaselineFR = np.empty(len(basicDB))
allSoundFR = np.empty(len(basicDB))
allSoundLaserFR = np.empty(len(basicDB))

for indRow, (dbIndex, dbRow) in enumerate(basicDB.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    print("Now processing", dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster'])

    # --- Determine laser responsiveness of each cell (using first 100 ms of noise-in-laser trials) ---
    try:
        laserEphysData, noBehav = cellObj.load('lasernoisebursts')
    except IndexError:
        print("No laser pulse session for this cell")
        baselineTestStatistic = np.nan
        baselinepVal = np.nan
        baselineLaserFR = np.nan
        baselineFR = np.nan
    else:
        baselineTestStatistic, baselinepVal, baselineLaserFR, baselineFR = laser_response(laserEphysData, baseRange=[-0.3, -0.2],
                                                             responseRange=[0.0, 0.1])

    try:
        bandEphysData, bandBehavData = cellObj.load('laserBandwidth')
    except IndexError:
        print("No bandwidth session for this cell")
        soundTestStatistic = np.nan
        soundpVal = np.nan
        soundLaserFR = np.nan
        soundFR = np.nan
        bandBaselineFR = np.nan
    else:
        soundTestStatistic, soundpVal, firingRates = laser_sound_response(bandEphysData, bandBehavData,
                                                                    baseRange=[-1.1, -0.1], responseRange=[0.0, 1.0])
        bandBaselineFR = firingRates[0]
        soundFR = firingRates[1]
        soundLaserFR = firingRates[2]

    allBaselineTestStatistic[indRow] = baselineTestStatistic
    allBaselinePVal[indRow] = baselinepVal
    allBaselineLaserFR[indRow] = baselineLaserFR
    allBaselineFR[indRow] = baselineFR

    allSoundTestStatistic[indRow] = soundTestStatistic
    allSoundPVal[indRow] = soundpVal
    allBandBaselineFR[indRow] = bandBaselineFR
    allSoundFR[indRow] = soundFR
    allSoundLaserFR[indRow] = soundLaserFR

basicDB['baselineTestStatistic'] = allBaselineTestStatistic
basicDB['baselinepVal'] = allBaselinePVal
basicDB['baselineLaserFR'] = allBaselineLaserFR
basicDB['baselineFR'] = allBaselineFR

basicDB['soundTestStatistic'] = allSoundTestStatistic
basicDB['soundpVal'] = allSoundPVal
basicDB['bandBaselineFR'] = allBandBaselineFR
basicDB['soundFR'] = allSoundFR
basicDB['soundLaserFR'] = allSoundLaserFR

# -- save the final database --
celldatabase.save_hdf(basicDB, dbFilename)
print(dbFilename + " saved")