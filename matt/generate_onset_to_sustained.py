import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
import studyparams

d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '_'.join(d1mice) + '.h5'
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)

PLOT = 0
SAVE = 1
# Compute onsetivity using CF trials with top 5 intensities.
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    try:
        ephysData, bdata = cell.load('tuningCurve')
    except (IndexError, ValueError):  # The cell does not have a tc or the tc session has no spikes
        print("No TC for cell {}".format(indRow))

    else:
        eventOnsetTimes = ephysData['events']['soundDetectorOn']
        # eventOnsetTimes = ephysData['events']['stimOn']
        spikeTimes = ephysData['spikeTimes']
        freqEachTrial = bdata['currentFreq']
        if len(eventOnsetTimes) != len(freqEachTrial):
            eventOnsetTimes = eventOnsetTimes[:-1]
            if len(eventOnsetTimes) != len(freqEachTrial):
                print("BAD number of trials! Skipping")
                continue

        # Get the trials for the CF
        possibleFreq = np.unique(freqEachTrial)
        intensityEachTrial = bdata['currentIntensity']
        cfTrials = freqEachTrial == dbRow['cf']
        eventsThisFreq = eventOnsetTimes[cfTrials]
        intenThisFreq = intensityEachTrial[cfTrials]

        # Get only the trials with the CF and the top 5 intensities
        possibleIntensity = np.unique(intenThisFreq)
        if len(possibleIntensity) > 4:
            intenToUse = possibleIntensity[-5:]
        else:
            intenToUse = possibleIntensity

        # Boolean of which trials from this frequency were high intensity
        highIntenTrials = np.in1d(intenThisFreq, intenToUse)

        # Filter the events this frequency to just take the ones from high intensity
        eventsThisFreqHighIntensity = eventsThisFreq[highIntenTrials]

        cellLatency = dbRow['latency']
        if not cellLatency > 0:
            print("Negative latency!! Skipping")
            continue

        baseRange = [-0.1, -0.05]
        # responseRange = [0, 0.05, 0.1]
        responseRange = [cellLatency, cellLatency + 0.05, 0.1+cellLatency]
        # if dbRow['brainArea']=='rightAC':
        #     # responseRange = [0.02, 0.07, 0.12]
        #     responseRange = [0.02, 0.07, 0.1]
        # elif dbRow['brainArea']=='rightThal':
        #     # responseRange = [0.005, 0.015, 0.105]
        #     responseRange = [0.005, 0.015, 0.1]

        alignmentRange = [baseRange[0], responseRange[-1]]

        # Align spikes just to the selected event onset times
        (spikeTimesFromEventOnset,
         trialIndexForEachSpike,
         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                       eventsThisFreqHighIntensity,
                                                                       alignmentRange)

        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)

        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            responseRange)

        avgResponse = nspkResp.mean(axis=0)
        onsetSpikes = avgResponse[0]
        sustainedSpikes = avgResponse[1]
        onsetRate = onsetSpikes / (responseRange[1] - responseRange[0])
        sustainedRate = sustainedSpikes / (responseRange[2] - responseRange[1])

        baseSpikes = nspkBase.mean()
        baseRate = baseSpikes / (baseRange[1] - baseRange[0])

        onsetBaseSubtracted = onsetRate - baseRate
        sustainedBaseSubtracted = sustainedRate - baseRate

        # baseSub = avgResponse - avgBase
        # normResponse = baseSub / baseSub[0]
        db.at[indRow, 'onsetRateCF'] = onsetRate
        db.at[indRow, 'sustainedRateCF'] = sustainedRate
        db.at[indRow, 'baselineRateCF'] = baseRate

db['cfOnsetivityIndex'] = (db['onsetRateCF'] - db['sustainedRateCF']) / (
                db['sustainedRateCF'] + db['onsetRateCF'])

if SAVE:
    celldatabase.save_hdf(db, pathtoDB)