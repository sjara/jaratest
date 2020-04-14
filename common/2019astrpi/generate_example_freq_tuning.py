"""
Generate npz file for tuningCurve heatmaps. There are two cells chosen to be the example cells at the beginning based
on manual judgement, not automated. Using these cells, the number of spikes at each intensity of the tuning curve is
calculated and stored in an npz file.
"""
import os
import sys
import numpy as np
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
import studyparams

if sys.version_info[0] < 3:
    inputFunc = raw_input
elif sys.version_info[0] >= 3:
    inputFunc = input

# ===================================parameters=================================
baseRange = [-0.1, 0]
responseRange = [0, 0.1]
alignmentRange = [baseRange[0], responseRange[1]]
msRaster = 2

FIGNAME = 'figure_frequency_tuning'
titleExampleBW = True

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = studyparams.DATABASE_NAME + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
# pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, '{}.h5'.format("['d1pi026', 'd1pi032', 'd1pi033', 'd1pi036', 'd1pi039', 'd1pi040', 'd1pi041', 'd1pi042', 'd1pi043', 'd1pi044']"))
db = celldatabase.load_hdf(pathtoDB)


examples = {}
examples.update({'D1': 'd1pi036_2019-05-29_2900.0_TT5c3'})
examples.update({'nD1': 'd1pi036_2019-05-29_2800.0_TT2c4'})

exampleCell = [val for key, val in examples.items()]
exampleKeys = [key for key, val in examples.items()]

exampleSpikeData = {}
# ===========================Create and save figures=============================
for ind, cellInfo in enumerate(exampleCell):

    (subject, date, depth, tetrodeCluster) = cellInfo.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

    oneCell = ephyscore.Cell(dbRow)

    ephysData, bdata = oneCell.load('tuningCurve')

    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    # eventOnsetTimes = ephysData['events']['stimOn']
# --------------------------Tuning curve------------------------------------------
# Parameters
    currentFreq = bdata['currentFreq']

    uniqFreq = np.unique(currentFreq)

    currentIntensity = bdata['currentIntensity']
    possibleIntensity = np.unique(bdata['currentIntensity'])
    nIntenLabels = len(possibleIntensity)
    lowIntensity = min(possibleIntensity)
    highIntensity = max(possibleIntensity)
    intensities = np.linspace(lowIntensity, highIntensity, nIntenLabels)
    intensities = intensities.astype(np.int)
    intenTickLocations = np.linspace(0, nIntenLabels-1, nIntenLabels)
    allIntenResp = np.empty((len(possibleIntensity), len(uniqFreq)))
    for indinten, inten in enumerate(possibleIntensity):

        for indfreq, freq in enumerate(uniqFreq):
            selectinds = np.flatnonzero((currentFreq == freq) & (currentIntensity == inten))
            # =====================index mismatch=====================================
            while selectinds[-1] >= eventOnsetTimes.shape[0]:
                selectinds = np.delete(selectinds, -1, 0)
            # ------------------------------------------------------------------------------
            selectedOnsetTimes = eventOnsetTimes[selectinds]
            (spikeTimesFromEventOnset,
             trialIndexForEachSpike,
             indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                           selectedOnsetTimes,
                                                                           alignmentRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)
            # The mean number of spike responses is stored for the particular frequency
            allIntenResp[indinten, indfreq] = np.mean(nspkResp)
    # All of the responses for all of the intensities for a specific cell are added to a dictionary
    exampleSpikeData.update({exampleKeys[ind]: allIntenResp})

exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
if os.path.isdir(os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)):
    np.savez(exampleDataPath, **exampleSpikeData)
    print("{} data saved to {}".format(FIGNAME, exampleDataPath))
elif not os.path.isdir(os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)):
    answer = inputFunc(
        "Save folder is not present. Would you like to make the desired directory now? (y/n) ")
    if answer in ['y', 'Y', 'Yes', 'YES']:
        os.mkdir(
            os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME))
        np.savez(exampleDataPath, **exampleSpikeData)
        print("{} data saved to {}".format(FIGNAME, exampleDataPath))
