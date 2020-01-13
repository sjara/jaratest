"""
Generate and save database containing basic information, stats, and indices for each cell.
"""

import os
import numpy as np
import time
from numpy import array
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import spikesorting # For clustering
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
# import database_generation_funcs as funcs
from jaratoolbox import ephyscore
import studyparams

def calculate_ascending_base_stats(db, frequency, toneIndex):
    """
    db = cell database
    frequency, toneIndex = High, First; Mid, Second; Low, Third
    """

    timeRange = [-0.1, 0.4]  # seconds
    binWidth = 0.01
    responseRange = [0,0.1] # sec
    baseRange = [-0.1,0] # sec

    # -- Initializing an empty array to hold the results of the calculations --
    pValueResponse = np.tile(np.nan, len(celldb))
    meanEvokedFR = np.tile(np.nan, len(celldb))
    meanBaseFR = np.tile(np.nan, len(celldb))
    pValueFR = np.tile(np.nan, len(celldb))
    meanEvokedFRStd = np.tile(np.nan, len(celldb))
    meanBaseFRStd = np.tile(np.nan, len(celldb))
    meanEvokedFROdd = np.tile(np.nan, len(celldb))
    meanBaseFROdd = np.tile(np.nan, len(celldb))
    expectationIndex = np.tile(np.nan, len(celldb))

    for indRow,dbRow in celldb.iterrows():
        if not 'ascending' in dbRow['sessionType']:
            print('This cell does not contain the threetone sequence.')
            continue

        oneCell = ephyscore.Cell(dbRow)

        #FIXME: This is bad way of testing if not spikes because ValueError
        #       could happen for a different reason.
        try:
            ephysData, bdata = oneCell.load('ascending')
        except ValueError:
            print('Session "ascending" has no spikes for {} {} {:.0f}um T{} c{}'.format(dbRow['subject'],dbRow['date'],
                                                                                dbRow['depth'], dbRow['tetrode'],
                                                                                dbRow['cluster']))
            continue

        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        if len(eventOnsetTimes)==len(bdata['currentFreq'])+1:
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)
        frequenciesEachTrial = bdata['currentFreq']
        arrayOfFrequencies = np.unique(bdata['currentFreq'])
        stimCondition = bdata['stimCondition']
        oddballs = np.flatnonzero(stimCondition)

        if frequency == 'High':
            Oddball = np.array(oddballs[::2])
            Standard = Oddball - 2
            OddballIndexLimits = indexLimitsEachTrial[:,Oddball]
            StandardIndexLimits = indexLimitsEachTrial[:, Standard]
        elif frequency == 'Mid':
            Oddball = np.array(oddballs[1::2])
            Standard = Oddball - 4
            OddballIndexLimits = indexLimitsEachTrial[:, Oddball]
            StandardIndexLimits = indexLimitsEachTrial[:, Standard]
        else:
            Oddball = np.array(oddballs[1::2]) + 1
            Standard = Oddball - 3
            OddballIndexLimits = indexLimitsEachTrial[:, Oddball]
            StandardIndexLimits = indexLimitsEachTrial[:, Standard]

        # -- Using responseRange and baseRange gives the number of spikes for each trial in the range 100ms.
        #    This avoids dealing with bins and also gives us better sets of numbers to compare - if we used
        #    bins, the numbers of spikes in those bins would be small and would affect our p-Values. --
        evokedSpikeCountMatOdd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                    OddballIndexLimits,responseRange)
        baseSpikeCountMatOdd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                    OddballIndexLimits,baseRange)
        evokedSpikeCountMatStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                    StandardIndexLimits,responseRange)
        baseSpikeCountMatStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                    StandardIndexLimits,baseRange)

        # -- Saving the calculated value into the array --
        meanEvokedFROdd[indRow] = np.mean(evokedSpikeCountMatOdd) / binWidth
        meanBaseFROdd[indRow] = np.mean(baseSpikeCountMatOdd) / binWidth
        meanEvokedFRStd[indRow] = np.mean(evokedSpikeCountMatStd) / binWidth
        meanBaseFRStd[indRow] = np.mean(baseSpikeCountMatStd) / binWidth

        # -- Because mannwhitneyu needs an array or a list as it's arguments, we're converting the
        #    matrix that is evokedSpikeCountMat to a list --
        evokedSpikeCountMatOddList = evokedSpikeCountMatOdd.ravel().tolist()
        evokedSpikeCountMatStdList = evokedSpikeCountMatStd.ravel().tolist()

        # -- mannwhitneyu blows up if both the lists it is comparing are all zeros --
        if np.sum(evokedSpikeCountMatOddList) != 0 or np.sum(evokedSpikeCountMatStdList) != 0:
            [testStatisticUE, pValUE] = stats.mannwhitneyu(evokedSpikeCountMatOddList,evokedSpikeCountMatStdList)
            pValueFR[indRow] = pValUE

        # -- To avoid the division by zero in the expectation index calculation --
        if meanEvokedFRStd[indRow] and meanEvokedFROdd[indRow] != 0:
            expectationIndex[indRow] = (meanEvokedFROdd[indRow] - meanEvokedFRStd[indRow]) / \
                                                        (meanEvokedFROdd[indRow] + meanEvokedFRStd[indRow])

        # -- Statistics for frequency-sorted raster --
        if frequency == 'High':
            eventOnsetTimesFreqSort = eventOnsetTimes[frequenciesEachTrial==arrayOfFrequencies[2]]
        elif frequency == 'Mid':
            eventOnsetTimesFreqSort = eventOnsetTimes[frequenciesEachTrial==arrayOfFrequencies[1]]
        else:
            eventOnsetTimesFreqSort = eventOnsetTimes[frequenciesEachTrial==arrayOfFrequencies[0]]

        (spikeTimesFromEventOnsetFreqSort,trialIndexForEachSpikeFreqSort,indexLimitsEachTrialFreqSort) = \
                    spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimesFreqSort, timeRange)

        # -- Only calculating if there are spikes --
        if len(spikeTimesFromEventOnsetFreqSort) > 0:
            evokedSpikeCount = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetFreqSort,
                                            indexLimitsEachTrialFreqSort,responseRange)
            baseSpikeCount = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetFreqSort,
                                            indexLimitsEachTrialFreqSort,baseRange)

            meanEvokedFR[indRow] = np.mean(evokedSpikeCount) / binWidth
            meanBaseFR[indRow] = np.mean(baseSpikeCount) / binWidth

            evokedSpikeCountList = evokedSpikeCount.ravel().tolist()
            baseSpikeCountList = baseSpikeCount.ravel().tolist()
            if np.sum(evokedSpikeCountList) != 0 or np.sum(baseSpikeCountList) != 0:
                [testStatistic, pVal] = stats.mannwhitneyu(evokedSpikeCountList, baseSpikeCountList)
                pValueResponse[indRow] = pVal

        print('Added statistics for {} {} {:.0f}um T{} c{} {} freq to the database'.format(dbRow['subject'],dbRow['date'],
                                                                                dbRow['depth'], dbRow['tetrode'],
                                                                                dbRow['cluster'], frequency))

    # -- Adding the new column to the database using the array we created earlier --
    celldb['pVal' + frequency + 'Response'] = pValueResponse
    celldb['meanEvoked' + frequency] = meanEvokedFR
    celldb['meanBase' + frequency] = meanBaseFR
    celldb['pVal' + frequency + 'FR'] = pValueFR
    celldb['meanEvoked' + toneIndex + 'Std'] = meanEvokedFRStd
    celldb['meanBase' + toneIndex + 'Std'] = meanBaseFRStd
    celldb['meanEvoked' + toneIndex +'Odd'] = meanEvokedFROdd
    celldb['meanBase' + toneIndex + 'Odd'] = meanBaseFROdd
    celldb['expInd' + frequency] = expectationIndex

    return db


def calculate_indices(db):
    return db


def calculate_cell_locations(db):
    pass


if __name__ == "__main__":

    # -- Spike sort the data (code is left here for reference) --
    '''
    subject = 'testXXX'
    inforecFile = os.path.join(settings.INFOREC_PATH,'{}_inforec.py'.format(subject))
    clusteringObj = spikesorting.ClusterInforec(inforecFile)
    clusteringObj.process_all_experiments()
    '''
    startTime = time.time()

    # -- Generate cell database (this function excludes clusters with isi>0.05, spikeQuality<2 --
    celldb = celldatabase.generate_cell_database_from_subjects(studyparams.MICE_LIST, removeBadCells=True,
                                                                isi=0.05, quality=2)

    # -- Compute the base stats and indices for each cell --
    cellBaseStats = calculate_ascending_base_stats(celldb, 'High', 'First')  # Calculated for all cells
    cellBaseStats = calculate_ascending_base_stats(celldb, 'Mid', 'Second')  # Calculated for all cells
    cellBaseStats = calculate_ascending_base_stats(celldb, 'Low', 'Third')  # Calculated for all cells
    # cellInd = calculate_indices(celldb)     # Calculated for a selected subset of cells

    dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
    if os.path.isdir(dbPath):
        celldatabase.save_hdf(celldb, dbFilename)
        print('Saved database to {}'.format(dbFilename))
    else:
        print('{} does not exist. Please create this folder.'.format(dbPath))

    print ('The script took {0} seconds'.format(time.time() - startTime))
