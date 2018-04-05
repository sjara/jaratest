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
from matplotlib import pyplot as plt
from scipy import signal
import pandas as pd
reload(spikesanalysis)

STUDY_NAME = '2018thstr'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS.h5')
db = pd.read_hdf(dbPath, key='dataframe')

# Examples of bad cells
# pinp017_2017-03-23_1604.0_TT2c6

# cellDict = {
#     'subject':'pinp017',
#     'date':'2017-03-23',
#     'depth':1604,
#     'tetrode':2,
#     'cluster':6
# }

cellsToTest = [
    'pinp017_2017-03-22_1338.0_TT3c4',
    'pinp017_2017-03-23_1604.0_TT2c6',
    'pinp017_2017-03-23_1518.0_TT8c2',
    'pinp016_2017-03-16_3707.0_TT2c6',
    'pinp015_2017-02-15_2902.0_TT8c4',
    'pinp016_2017-03-15_3797.0_TT1c3',
    'pinp026_2017-11-16_3256.0_TT6c3'
]

for cellName in cellsToTest:
    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    indRow, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)

    # indRow, dbRow = celldatabase.find_cell(db, **cellDict)
    cell = ephyscore.Cell(dbRow)

    ephysData, bdata = cell.load('tc')

    # eventOnsetTimes = ephysData['events']['soundDetectorOn']
    eventOnsetTimes = ephysData['events']['stimOn']

    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
    spikeTimes = ephysData['spikeTimes']
    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    #FIXME: I need to remove the last event here if there is an extra one
    if len(eventOnsetTimes) == len(freqEachTrial)+1:
        eventOnsetTimes = eventOnsetTimes[:-1]

    trialsEachCondition = behavioranalysis.find_trials_each_combination(intensityEachTrial, possibleIntensity,
                                                                        freqEachTrial, possibleFreq)

    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [-0.2, 0.2]

    #Align all spikes to events
    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                alignmentRange)

    #Count spikes in baseline and response ranges
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)

    #Filter and average the response spikes by the condition matrix
    conditionMatShape = np.shape(trialsEachCondition)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(nspkResp.squeeze().repeat(numRepeats), conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
    avgRespArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
        trialsEachCondition, 0).astype('float')

    thresholdFRA=0.2
    thresholdResponse = nspkBase.mean() + thresholdFRA*(avgRespArray.max()-nspkBase.mean())

    if not np.any(avgRespArray > thresholdResponse):
        print "Nothing above the threshold"

    #Determine trials that come from a I/F pair with a response above the threshold
    fra = avgRespArray > thresholdResponse
    selectedTrials = np.any(trialsEachCondition[:,fra], axis=1)

    # -- Calculate response latency --
    indexLimitsSelectedTrials = indexLimitsEachTrial[:,selectedTrials]
    timeRangeForLatency = [-0.1,0.1]
    (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                            indexLimitsSelectedTrials,
                                                            timeRangeForLatency, threshold=0.5,
                                                            win=signal.hanning(11))


    selectedTrialsInds = np.flatnonzero(selectedTrials)
    # selectedSpikesInds = np.isin(trialIndexForEachSpike,selectedTrialsInds)#NOTE: Requires newer numpy
    selectedSpikesInds = np.in1d(trialIndexForEachSpike,selectedTrialsInds)
    tempTIFES = trialIndexForEachSpike[selectedSpikesInds]
    newSpikeTimes = spikeTimesFromEventOnset[selectedSpikesInds]

    # The next thing is slow, but I don't have time to optimize
    newTrialInds = np.empty(tempTIFES.shape, dtype=int)
    for ind,trialInd in enumerate(np.unique(tempTIFES)):
        newTrialInds[tempTIFES==trialInd] = ind

    plt.clf()
    plt.title(respLatency)
    plt.subplot(2,1,1)
    plt.plot(newSpikeTimes, newTrialInds, '.k')
    #plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k') # Plot all trials
    plt.xlim(timeRangeForLatency)
    plt.hold(1)
    plt.title('{}'.format(indRow))
    plt.axvline(respLatency,color='r')

    plt.subplot(2,1,2)
    plt.plot(interim['timeVec'], interim['avgCount'],'.-k')
    plt.hold(1)
    plt.axvline(respLatency,color='r')
    plt.axhline(interim['threshold'],ls='--',color='0.75')
    plt.axhline(interim['baseline'],ls=':',color='0.75')
    plt.axhline(interim['maxResponse'],ls=':',color='0.75')
    plt.plot(interim['timeVec'],interim['psth'],'r-',mec='none',lw=3)
    plt.xlim(timeRangeForLatency)
    plt.show()
    plt.waitforbuttonpress()
