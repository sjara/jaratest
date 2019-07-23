import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import figparams
import studyparams
import pandas as pd
reload(spikesanalysis)

d1mice = studyparams.ASTR_D1_CHR2_MICE
# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'{}.h5'.format('_'.join(d1mice)))
db = celldatabase.load_hdf(dbPath)
thresholdFRA = 0.2
mono = []
maxSpikes = []

SAVE = 1

# -- Monotonicity with respect to level -- #
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    print(indRow)
    failed=False
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    try:
        ephysData, bdata = cell.load('tuningCurve')
    except (IndexError, ValueError):  # The cell does not have a tc or the tc session has no spikes
        failed=True
        print("No tc for cell {}".format(indRow))

    else:
        eventOnsetTimes = ephysData['events']['stimOn']
        spikeTimes = ephysData['spikeTimes']
        freqEachTrial = bdata['currentFreq']
        if len(eventOnsetTimes) != len(freqEachTrial):
            eventOnsetTimes = eventOnsetTimes[:-1]
            if len(eventOnsetTimes) != len(freqEachTrial):
                continue

        possibleFreq = np.unique(freqEachTrial)
        intensityEachTrial = bdata['currentIntensity']
        possibleIntensity = np.unique(intensityEachTrial)

        cfTrials = freqEachTrial==dbRow['cf']
        eventsThisFreq = eventOnsetTimes[cfTrials]
        intenThisFreq = intensityEachTrial[cfTrials]

        baseRange = [-0.1, 0]
        responseRange = [0, 0.1]
        alignmentRange = [baseRange[0], responseRange[1]]

        meanSpikesAllInten = np.empty(len(possibleIntensity))
        maxSpikesAllInten = np.empty(len(possibleIntensity))
        baseSpikesAllInten = np.empty(len(possibleIntensity))
        for indInten, inten in enumerate(possibleIntensity):
            # print inten
            trialsThisIntensity = intenThisFreq==inten
            eventsThisCombo = eventsThisFreq[trialsThisIntensity]

            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                        eventsThisCombo,
                                                                        alignmentRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)

            spikesThisInten = nspkResp[:,0]
            baselineThisInten = nspkBase[:,0]
            # print spikesThisInten
            try:
                meanSpikesThisInten = np.mean(spikesThisInten)
                meanBaselineSpikesThisInten = np.mean(baselineThisInten)
                maxSpikesThisInten = np.max(spikesThisInten)
            except ValueError:
                meanSpikesThisInten = 0
                maxSpikesThisInten = 0

            meanSpikesAllInten[indInten] = meanSpikesThisInten
            maxSpikesAllInten[indInten] = maxSpikesThisInten
            baseSpikesAllInten[indInten] = meanBaselineSpikesThisInten

        baseline = np.mean(baseSpikesAllInten)
        monoIndex = (meanSpikesAllInten[-1] - baseline) / (np.max(meanSpikesAllInten)-baseline)

        db.loc[indRow, 'monotonicityIndex'] = monoIndex

        overallMaxSpikes = np.max(maxSpikesAllInten)
        maxSpikes.append(overallMaxSpikes)

if SAVE:
    celldatabase.save_hdf(db, dbPath)