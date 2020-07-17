"""
Generate npz file for tuningCurve heatmaps. There are two cells chosen to be
the example cells at the beginning based on manual judgement, not automated.
Using these cells, the number of spikes at each intensity of the tuning curve is
calculated and stored in an npz file.
"""
import os
import sys
import numpy as np
import pandas as pd
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
# --------------------------Tuning curve------------------------------------------
    # Parameters
    currentFreq = bdata['currentFreq']
    uniqFreq = np.unique(currentFreq)
    currentIntensity = bdata['currentIntensity']
    possibleIntensity = np.unique(bdata['currentIntensity'])
    ######
    nIntenLabels = len(possibleIntensity)
    lowIntensity = min(possibleIntensity)
    highIntensity = max(possibleIntensity)
    intensities = np.linspace(lowIntensity, highIntensity, nIntenLabels)
    intensities = intensities.astype(np.int)
    intenTickLocations = np.linspace(0, nIntenLabels-1, nIntenLabels)
    ##### This block of above code seems uneeded for generating the npz
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

# Filtering DB for appropraite cells to plot
db = db.query(studyparams.TUNING_FILTER)
zDB = db.query(studyparams.LABELLED_Z)
zDB2 = db[db['z_coord'].isnull()]
zDBt = pd.concat([zDB, zDB2], axis=0, ignore_index=True, sort=False)
db = zDBt.query(studyparams.BRAIN_REGION_QUERY)
D1 = db.query(studyparams.D1_CELLS)  # laser activation response
nD1 = db.query(studyparams.nD1_CELLS)  # no laser repsonse or laser inactivation response

popStatCol = 'bw10'
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
exampleSpikeData.update({"D1_bw10": D1PopStat, "nD1_bw10": nD1PopStat})

popStatCol = 'thresholdFRA'
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
exampleSpikeData.update({"D1_thresholdFRA": D1PopStat, "nD1_thresholdFRA": nD1PopStat})

popStatCol = 'latency'
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
D1PopStat = D1PopStat[D1PopStat > 0]
nD1PopStat = nD1PopStat[nD1PopStat > 0]
exampleSpikeData.update({"D1_latency": D1PopStat, "nD1_latency": nD1PopStat})

popStatCol = 'cfOnsetivityIndex'
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
exampleSpikeData.update({"D1_cfOnsetivityIndex": D1PopStat, "nD1_cfOnsetivityIndex": nD1PopStat})

popStatCol = 'monotonicityIndex'
D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
exampleSpikeData.update({"D1_monotonicityIndex": D1PopStat, "nD1_monotonicityIndex": nD1PopStat})

exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')

# Check for if the directory to save to exists, and if not prompt the user to make it
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
