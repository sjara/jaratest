'''
Generate npz file for tuningCurve heatmaps
'''
import os
import sys
import numpy as np
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import studyparams
reload(studyparams)

if sys.version_info[0] < 3:
    input_func = raw_input
elif sys.version_info[0] >= 3:
    input_func = input

#===================================parameters=================================
baseRange = [-0.1, 0]
responseRange = [0, 0.1]
alignmentRange = [baseRange[0], responseRange[1]]
msRaster = 2

FIGNAME = 'figure_frequency_tuning'
titleExampleBW=True

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '_'.join(d1mice) + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)


examples = {}
examples.update({'D1':'d1pi032_2019-02-22_3400.0_TT5c4'})
examples.update({'nD1':'d1pi033_2019-04-17_2900.0_TT8c2'})

exampleCell = [val for key, val in examples.items()]
exampleKeys = [key for key, val in examples.items()]

exampleSpikeData = {}
#===========================Create and save figures=============================
for ind, cellInfo in enumerate(exampleCell):

    (subject, date, depth, tetrodeCluster) = cellInfo.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

    oneCell = ephyscore.Cell(dbRow)

    try:
        ephysData, bdata = oneCell.load('tuningCurve')
    except:
        ephysData, bdata = oneCell.load('tuningCurve(tc)')

    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
#--------------------------Tuning curve------------------------------------------
## Parameters
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
            selectinds = np.flatnonzero((currentFreq==freq)&(currentIntensity==inten))
            #=====================index mismatch=====================================
            while selectinds[-1] >= eventOnsetTimes.shape[0]:
                 selectinds = np.delete(selectinds,-1,0)
            #------------------------------------------------------------------------------
            selectedOnsetTimes = eventOnsetTimes[selectinds]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                        selectedOnsetTimes,
                                                                        alignmentRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)
            allIntenResp[indinten, indfreq] = np.mean(nspkResp)
    exampleSpikeData.update({exampleKeys[ind]:allIntenResp})

exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
if os.path.isdir(os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)):
    np.savez(exampleDataPath, **exampleSpikeData)
    print "{} data saved to {}".format(FIGNAME, exampleDataPath)
elif os.path.isdir(os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)) == False:
    answer = input_func(
        "Save folder is not present. Would you like to make the desired directory now? (y/n) ")
    if answer in ['y', 'Y', 'Yes', 'YES']:
        os.mkdir(
            os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME))
        np.savez(exampleDataPath, **exampleSpikeData)
        print "{} data saved to {}".format(FIGNAME, exampleDataPath)
