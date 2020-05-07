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
from jaratoolbox import behavioranalysis
# import database_generation_funcs as funcs
from jaratoolbox import ephyscore
import studyparams

reload(studyparams)


dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)

'''
def calculate_pvalues(celldb):

    Generates p-Values between oddball and standard firing rates during sound presentation and between the high frequency sound 100ms before sound presentation and during sound presentation.

    Inputs:
        celldb: Database that allows for loading of ephys and behavior data.

'''

ratioFR = 1.01

timeRange = [-0.1, 0.3]  # seconds
binWidth = 0.01
responseRange = [0,0.1] # sec
baseRange = [-0.1,0] # sec

meanEvokedFRStd = np.tile(np.nan, len(celldb))
meanBaseFROdd = np.tile(np.nan, len(celldb))
meanEvokedFROdd = np.tile(np.nan, len(celldb))
pValueBaselineEvokedOddball = np.tile(np.nan, len(celldb))
pValueEvokedOddballStandard = np.tile(np.nan, len(celldb))

numOfCellsOddballParadigm = 0

for indRow,dbRow in celldb.iterrows():
    if not 'standard' in dbRow['sessionType']:
        #print('This cell does not contain the standard sequence.')
        continue

    oneCell = ephyscore.Cell(dbRow)

    numOfCellsOddballParadigm = numOfCellsOddballParadigm + 1

    if oneCell.get_session_inds('standard') != []:
        try:
            ephysDataStd, bdataStd = oneCell.load('standard')
        except ValueError as verror:
            continue

    spikeTimesStd = ephysDataStd['spikeTimes']
    eventOnsetTimesStd = ephysDataStd['events']['stimOn']
    if len(eventOnsetTimesStd)==len(bdataStd['currentFreq'])+1:
        eventOnsetTimesStd = eventOnsetTimesStd[:-1]
    (spikeTimesFromEventOnsetStd,trialIndexForEachSpikeStd,indexLimitsEachTrialStd) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimesStd, eventOnsetTimesStd, timeRange)
    frequenciesEachTrialStd = bdataStd['currentFreq']
    arrayOfFrequenciesStd = np.unique(bdataStd['currentFreq'])

    trialsEachCondStd = behavioranalysis.find_trials_each_type(frequenciesEachTrialStd,
                arrayOfFrequenciesStd)

    # -- Oddball session --
    if oneCell.get_session_inds('oddball') != []:
        try:
            ephysDataOdd, bdataOdd = oneCell.load('oddball')
        except ValueError as verror:
            continue

    spikeTimesOdd = ephysDataOdd['spikeTimes']
    eventOnsetTimesOdd = ephysDataOdd['events']['stimOn']
    if len(eventOnsetTimesOdd)==len(bdataOdd['currentFreq'])+1:
        eventOnsetTimesOdd = eventOnsetTimesOdd[:-1]
    (spikeTimesFromEventOnsetOdd,trialIndexForEachSpikeOdd,indexLimitsEachTrialOdd) =       spikesanalysis.eventlocked_spiketimes(spikeTimesOdd, eventOnsetTimesOdd, timeRange)
    frequenciesEachTrialOdd = bdataOdd['currentFreq']
    arrayOfFrequenciesOdd = np.unique(bdataOdd['currentFreq'])

    trialsEachCondOdd = behavioranalysis.find_trials_each_type(frequenciesEachTrialOdd, arrayOfFrequenciesOdd)

    # -- Statistics --

    highFreqInOddPara = indexLimitsEachTrialOdd[:,trialsEachCondOdd[:,1]]
    highFreqInStdPara = indexLimitsEachTrialStd[:,trialsEachCondStd[:,1]]

    spikeCountMatHighFreqOddInOddParaBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,
                highFreqInOddPara,baseRange)
    spikeCountMatHighFreqOddInOddParaEvoked = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,
                highFreqInOddPara,responseRange)
    spikeCountMatHighFreqStdInStdParaEvoked = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStd,
                highFreqInStdPara,responseRange)

    evokedSpikeCountOddball = spikeCountMatHighFreqOddInOddParaEvoked.ravel().tolist()
    baseSpikeCountOddball = spikeCountMatHighFreqOddInOddParaBase.ravel().tolist()
    evokedSpikeCountStandard = spikeCountMatHighFreqStdInStdParaEvoked.ravel().tolist()

    # Firing rates
    meanEvokedFROdd[indRow] = np.mean(evokedSpikeCountOddball) / binWidth
    meanBaseFROdd[indRow] = np.mean(baseSpikeCountOddball) / binWidth
    meanEvokedFRStd[indRow] = np.mean(evokedSpikeCountStandard) / binWidth

    # Adding firing rates to the cell database
    celldb['evokedFROdd'] = meanEvokedFROdd
    celldb['baseFROdd'] = meanBaseFROdd
    celldb['evokedFRStd'] = meanEvokedFRStd

    # -- p-Value between responsive (high frequency) oddball for 100ms before sound onset and during sound presentation. --
    if np.sum(evokedSpikeCountOddball) != 0 or np.sum(baseSpikeCountOddball) != 0:
        [testStatistic, pValueBaseEvokedOddball] = stats.mannwhitneyu(evokedSpikeCountOddball, baseSpikeCountOddball)
        pValueBaselineEvokedOddball[indRow] = pValueBaseEvokedOddball

    # -- p-Value between the responsive high frequency tone during sound presentation when the high frequency is the oddball and when it is the standard. --
    if np.sum(evokedSpikeCountOddball) != 0 or np.sum(evokedSpikeCountStandard)!= 0:
        if celldb['evokedFROdd'][indRow] / celldb['evokedFRStd'][indRow] > ratioFR:
            [testStatisticOS, pValueEvokedOddStd] = stats.mannwhitneyu(evokedSpikeCountOddball, evokedSpikeCountStandard)
            pValueEvokedOddballStandard[indRow] = pValueEvokedOddStd

    # -- Adding p-Values to the cell database --
    celldb['pValueOddballResponse'] = pValueBaselineEvokedOddball
    celldb['pValueOddStd'] = pValueEvokedOddballStandard

    signRespCells = celldb.query('pValueOddballResponse < 0.05')
    increasedResponseToOddball = celldb.query('pValueOddStd < 0.05')

cellInfo = increasedResponseToOddball[['subject', 'date', 'depth', 'tetrode', 'cluster']]
print(cellInfo)

print('The total number of cells recorded from while presenting the oddball sequence is {}').format(numOfCellsOddballParadigm)
print('There are {} cells that show significantly increased responses to the oddball stimuli compared to the standard paradigm.').format(len(increasedResponseToOddball))
# print('There are {} cells that were significantly sound responsive.').format(len(signRespCells))


#startTime = time.time()
#calculate_pvalues(celldb)
#totalTime = time.time() - startTime
#print ('The script took {} seconds').format(totalTime)
