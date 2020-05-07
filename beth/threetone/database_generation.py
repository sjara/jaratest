"""
Generate and save database containing basic information, stats, and indices for each cell.
"""
import os
import importlib
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
importlib.reload(studyparams)

"""
Uploading celldb (in order to recalculate base stats)
"""
dbPath = settings.FIGURES_DATA_PATH
dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)


def calculate_base_stats(celldb, frequency, session):
    """
    Creates columns in the generic cell database for evoked and baseline firing rates and p-Values between the two.

    Inputs:
        celldb: Database that allows for loading of ephys and behavior data.
        frequency: Ascending: ['High', 'First']; ['Mid', 'Second']; ['Low', 'Third']
                   Descending: ['High', 'Third']; ['Mid', 'Second']; ['Low', 'First']
        session: ['ascending', 'A']; ['descending', 'D']

    Outputs:
        celldb: Updated cell database that includes eight additional columns for each of the three frequencies for both sequences. The columns include, for example, for the high frequency (first std and odd) in the ascending sequence: pValHighResponseA, meanEvokedHighA, meanBaseHighA, pValHighFRA, meanEvokedFirstStdA, meanBaseFirstStdA, meanEvokedFirstOddA, meanBaseFirstOddA.
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

    for indRow,dbRow in celldb.iterrows():
        if not 'ascending' in dbRow['sessionType']:
            print('This cell does not contain the threetone sequence.')
            continue

        oneCell = ephyscore.Cell(dbRow)

        #FIXME: This is bad way of testing if no spikes because ValueError could happen for a different reason.
        try:
            ephysData, bdata = oneCell.load(session[0])
        except ValueError:
            print('Session "{}" has no spikes for {} {} {:.0f}um T{} c{}'.format(session[0], dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
            continue

        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        if len(eventOnsetTimes)==len(bdata['currentFreq'])+1:
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)
        frequenciesEachTrial = bdata['currentFreq']
        arrayOfFrequencies = np.unique(bdata['currentFreq'])
        stimCondition = bdata['stimCondition']
        if stimCondition[-1] == 1:
            print('Removing last trial from behavioral data. Paradigm ended in the middle of an oddball sequence.')
            stimCondition = stimCondition[:-1]
        oddballs = np.flatnonzero(stimCondition)

        if frequency[0] == 'High':
            Oddball = np.array(oddballs[::2])
            Standard = Oddball - 2
            OddballIndexLimits = indexLimitsEachTrial[:,Oddball]
            StandardIndexLimits = indexLimitsEachTrial[:, Standard]
        elif frequency[0] == 'Mid':
            Oddball = np.array(oddballs[1::2])
            Standard = Oddball - 4
            OddballIndexLimits = indexLimitsEachTrial[:, Oddball]
            StandardIndexLimits = indexLimitsEachTrial[:, Standard]
        else:
            Oddball = np.array(oddballs[1::2]) + 1
            Standard = Oddball - 3
            OddballIndexLimits = indexLimitsEachTrial[:, Oddball]
            StandardIndexLimits = indexLimitsEachTrial[:, Standard]

        # -- Using responseRange and baseRange gives the number of spikes for each trial in the range 100ms. This avoids dealing with bins and also gives us better sets of numbers to compare - if we used bins, the numbers of spikes in those bins would be small and would affect our p-Values. --
        evokedSpikeCountMatOdd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, OddballIndexLimits,responseRange)
        baseSpikeCountMatOdd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, OddballIndexLimits,baseRange)
        evokedSpikeCountMatStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, StandardIndexLimits,responseRange)
        baseSpikeCountMatStd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, StandardIndexLimits,baseRange)

        # -- Saving the calculated value into the array --
        meanEvokedFROdd[indRow] = np.mean(evokedSpikeCountMatOdd) / binWidth
        meanBaseFROdd[indRow] = np.mean(baseSpikeCountMatOdd) / binWidth
        meanEvokedFRStd[indRow] = np.mean(evokedSpikeCountMatStd) / binWidth
        meanBaseFRStd[indRow] = np.mean(baseSpikeCountMatStd) / binWidth

        # -- Because mannwhitneyu needs an array or a list as it's arguments, we're converting the matrix that is evokedSpikeCountMat to a list --
        evokedSpikeCountMatOddList = evokedSpikeCountMatOdd.ravel().tolist()
        evokedSpikeCountMatStdList = evokedSpikeCountMatStd.ravel().tolist()

        # -- mannwhitneyu blows up if both the lists it is comparing are all zeros --
        if np.sum(evokedSpikeCountMatOddList) != 0 or np.sum(evokedSpikeCountMatStdList) != 0:
            [testStatisticUE, pValUE] = stats.mannwhitneyu(evokedSpikeCountMatOddList,evokedSpikeCountMatStdList,alternative='two-sided')
            pValueFR[indRow] = pValUE

        # -- Statistics for frequency-sorted raster --
        if frequency[0] == 'High':
            eventOnsetTimesFreqSort = eventOnsetTimes[frequenciesEachTrial==arrayOfFrequencies[2]]
        elif frequency[0] == 'Mid':
            eventOnsetTimesFreqSort = eventOnsetTimes[frequenciesEachTrial==arrayOfFrequencies[1]]
        else:
            eventOnsetTimesFreqSort = eventOnsetTimes[frequenciesEachTrial==arrayOfFrequencies[0]]

        (spikeTimesFromEventOnsetFreqSort,trialIndexForEachSpikeFreqSort,indexLimitsEachTrialFreqSort) = spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimesFreqSort, timeRange)

        # -- Only calculating if there are spikes --
        if len(spikeTimesFromEventOnsetFreqSort) > 0:
            evokedSpikeCount = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetFreqSort, indexLimitsEachTrialFreqSort,responseRange)
            baseSpikeCount = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetFreqSort, indexLimitsEachTrialFreqSort,baseRange)

            meanEvokedFR[indRow] = np.mean(evokedSpikeCount) / binWidth
            meanBaseFR[indRow] = np.mean(baseSpikeCount) / binWidth

            evokedSpikeCountList = evokedSpikeCount.ravel().tolist()
            baseSpikeCountList = baseSpikeCount.ravel().tolist()
            if np.sum(evokedSpikeCountList) != 0 or np.sum(baseSpikeCountList) != 0:
                [testStatistic, pVal] = stats.wilcoxon(evokedSpikeCountList, baseSpikeCountList, alternative='two-sided')
                pValueResponse[indRow] = pVal

        print('Added statistics for {} {} {:.0f}um T{} c{} {} freq {} to the database'.format(dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster'], frequency[0], session[0]))

    # -- Adding the new column to the database using the array we created earlier --
    celldb['pVal' + frequency[0] + 'Response' + session[1]] = pValueResponse
    celldb['meanEvoked' + frequency[0] + session[1]] = meanEvokedFR
    celldb['meanBase' + frequency[0] + session[1]] = meanBaseFR
    celldb['pVal' + frequency[0] + 'FR' + session[1]] = pValueFR
    celldb['meanEvoked' + frequency[1] + 'Std' + session[1]] = meanEvokedFRStd
    celldb['meanBase' + frequency[1] + 'Std' + session[1]] = meanBaseFRStd
    celldb['meanEvoked' + frequency[1] +'Odd' + session[1]] = meanEvokedFROdd
    celldb['meanBase' + frequency[1] + 'Odd' + session[1]] = meanBaseFROdd


def calculate_indices(celldb, frequency, session):
    """
    Creates columns in the cell database for the expectation index comparing oddball and standard evoked firing rates.

    Inputs:
        celldb: Database that allows for loading of ephys and behavior data.
        frequency: Ascending: ['High', 'First']; ['Mid', 'Second']; ['Low', 'Third']
                   Descending: ['High', 'Third']; ['Mid', 'Second']; ['Low', 'First']
        session: 'A'; 'D'

    Outputs:
        celldb: Updated cell database that includes one additional column for each of the three frequencies for both sequences. The column, for example, for the high frequency (first std and odd) in the ascending sequence: expIndHighA.
    """

    # -- Initializing an empty array to hold the results of the calculations --
    expectationIndex = np.tile(np.nan, len(celldb))

    for indRow,dbRow in celldb.iterrows():
        std = celldb['meanEvoked' + frequency[1] + 'Std' + session][indRow]
        odd = celldb['meanEvoked' + frequency[1] + 'Odd' + session][indRow]
        # -- To avoid the division by zero in the expectation index calculation --
        if std and odd != 0:
            expectationIndex[indRow] = (odd - std) / (odd + std)

        print('Added indices for {} {} {:.0f}um T{} c{} {} freq {} to the database'.format(dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster'], frequency[0], session))

    # -- Adding the new column to the database using the array we created earlier --
    celldb['expInd' + frequency[0] + session] = expectationIndex


def calculate_cell_locations(celldb):
    pass


if __name__ == "__main__":

    # -- Spike sort the data (code is left here for reference) --
    '''
    import os
    from jaratoolbox import spikesorting
    from jaratoolbox import settings

    subject = 'testXXX'
    inforecFile = os.path.join(settings.INFOREC_PATH,'{}_inforec.py'.format(subject))
    clusteringObj = spikesorting.ClusterInforec(inforecFile)
    clusteringObj.process_all_experiments()
    '''
    startTime = time.time()

    """
    # -- Generate cell database (this function excludes clusters with isi>0.05, spikeQuality<2 --
    celldb = celldatabase.generate_cell_database_from_subjects(studyparams.MICE_LIST, removeBadCells=True, isi=0.05, quality=2)
    """
    # -- Compute the base stats for all cells --
    # -- Ascending base stats --
    calculate_base_stats(celldb, ['High', 'First'], ['ascending', 'A'])
    calculate_base_stats(celldb, ['Mid', 'Second'], ['ascending', 'A'])
    calculate_base_stats(celldb, ['Low', 'Third'], ['ascending', 'A'])
    # -- Descending base stats --
    calculate_base_stats(celldb, ['High', 'Third'], ['descending', 'D'])
    calculate_base_stats(celldb, ['Mid', 'Second'], ['descending', 'D'])
    calculate_base_stats(celldb, ['Low', 'First'], ['descending', 'D'])

    # -- Compute indices for all cells --
    # -- Ascending indices --
    calculate_indices(celldb, ['High', 'First'], 'A')
    calculate_indices(celldb, ['Mid', 'Second'], 'A')
    calculate_indices(celldb, ['Low', 'Third'], 'A')
    # -- Descending indices --
    calculate_indices(celldb, ['High', 'First'], 'D')
    calculate_indices(celldb, ['Mid', 'Second'], 'D')
    calculate_indices(celldb, ['Low', 'Third'], 'D')

    # -- Saving the database --
    # dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    dbPath = settings.FIGURES_DATA_PATH
    # -- Database file name for single animal --
    dbFilename = os.path.join(dbPath,'newcelldb_{}_{}.h5'.format(studyparams.STUDY_NAME, studyparams.MICE_LIST[0]))
    # -- Database file name for all animals in study --
    #dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))

    if os.path.isdir(dbPath):
        celldatabase.save_hdf(celldb, dbFilename)
        print('Saved database to {}'.format(dbFilename))
    else:
        print('{} does not exist. Please create this folder.'.format(dbPath))

    totalTime = time.time() - startTime
    totalTimeMins = totalTime / 60
    print ('The script took {:.2f} minutes'.format(totalTimeMins))
