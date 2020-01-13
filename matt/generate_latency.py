# We want the latency, but which latency?? We can do lat to first spike for response to a specific type of session
# or to a specific freq/inten combo potentially.

# Try to use the freq/inten combos that have significant responses according to a more strict threshold

# Save the aligned spikes to an NPZ so that we can plot reports

import os
import numpy as np
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import studyparams

d1mice = studyparams.ASTR_D1_CHR2_MICE
# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'{}.h5'.format('_'.join(d1mice)))
db = celldatabase.load_hdf(dbPath)
dataframe = db
thresholdFRA = 0.2
latencyDataList = []

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):

    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)

    try:
        ephysData, bdata = cell.load('tuningCurve')
    except (IndexError, ValueError):  # The cell does not have a tc or the tc session has no spikes
        print("No tc for cell {}".format(indRow))
        dataframe.loc[indRow, 'latency'] = np.nan
        continue

    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    # eventOnsetTimes = ephysData['events']['stimOn']

    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
    spikeTimes = ephysData['spikeTimes']
    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    # FIXME: I need to remove the last event here if there is an extra one
    if len(eventOnsetTimes) == len(freqEachTrial)+1:
        eventOnsetTimes = eventOnsetTimes[:-1]
    elif len(eventOnsetTimes) < len(freqEachTrial):
        print("Wrong number of events, probably caused by the original sound detector problems")
        dataframe.loc[indRow, 'latency'] = np.nan
        continue
    else:
        print("Something else is wrong with the number of events")
        dataframe.loc[indRow, 'latency'] = np.nan
        continue

    trialsEachCondition = behavioranalysis.find_trials_each_combination(intensityEachTrial, possibleIntensity,
                                                                        freqEachTrial, possibleFreq)

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [-0.2, 0.2]

    # Align all spikes to events
    (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                      eventOnsetTimes,
                                                                      alignmentRange)

    # Count spikes in baseline and response ranges
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)

    # Filter and average the response spikes by the condition matrix
    conditionMatShape = np.shape(trialsEachCondition)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(nspkResp.squeeze().repeat(numRepeats), conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
    avgRespArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
        trialsEachCondition, 0).astype('float')

    thresholdResponse = nspkBase.mean() + thresholdFRA*(avgRespArray.max()-nspkBase.mean())

    if not np.any(avgRespArray > thresholdResponse):
        print("Nothing above the threshold")
        dataframe.loc[indRow, 'latency'] = np.nan
        continue

    # Determine trials that come from a I/F pair with a response above the threshold
    fra = avgRespArray > thresholdResponse
    selectedTrials = np.any(trialsEachCondition[:,fra], axis=1)

    # -- Calculate response latency --
    indexLimitsSelectedTrials = indexLimitsEachTrial[:,selectedTrials]
    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsSelectedTrials,
                                                                timeRangeForLatency, threshold=0.5,
                                                                win=signal.hanning(11))
    except IndexError:
        print("Index error for cell {}".format(indRow))  # If there are no spikes in the timeRangeForLatency
        dataframe.loc[indRow, 'latency'] = np.nan
        continue

    dataframe.loc[indRow, 'latency'] = respLatency
    print('Response latency: {:0.1f} ms'.format(1e3*respLatency))


# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
print('Saving database to {}'.format(dbPath))
celldatabase.save_hdf(dataframe, dbPath)

# latencyDataArray = np.array(latencyDataList)
# savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'latency_data.npz')
# np.savez(dataFn, data=latencyDataArray)
