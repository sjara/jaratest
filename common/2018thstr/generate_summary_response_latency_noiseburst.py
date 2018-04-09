## This file will calculate latencies to noise burst sessions and save them 

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
import pandas as pd

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')
dataframe = db
latencyDataList = []

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):

    cell = ephyscore.Cell(dbRow)

    try:
        ephysData, _ = cell.load('noiseburst')
    except (IndexError, ValueError): #The cell does not have a noiseburst or has no spikes in nb session
        print "No nb for cell {}".format(indRow)
        dataframe.loc[indRow, 'latencyNB'] = np.nan
        continue

    eventOnsetTimes = ephysData['events']['soundDetectorOn']

    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
    spikeTimes = ephysData['spikeTimes']

    #FIXME: I need to remove the last event here if there is an extra one
    # if len(eventOnsetTimes) == len(freqEachTrial)+1:
    #     eventOnsetTimes = eventOnsetTimes[:-1]
    # elif len(eventOnsetTimes) < len(freqEachTrial):
    #     print "Wrong number of events, probably caused by the original sound detector problems"
    #     dataframe.loc[indRow, 'latencyNB'] = np.nan
    #     continue

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

    # -- Calculate response latency --
    timeRangeForLatency = [-0.1,0.1]
    try:
        (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRangeForLatency, threshold=0.5)
    except IndexError:
        print "Index error for cell {}".format(indRow) #If there are no spikes in the timeRangeForLatency
        dataframe.loc[indRow, 'latencyNB'] = np.nan
        continue

    dataframe.loc[indRow, 'latencyNB'] = respLatency
    print 'Response latency for noiseburst session: {:0.1f} ms'.format(1e3*respLatency)

    saveDir = 

    plt.clf()
    plt.title(respLatency)
    plt.subplot(2,1,1)
    plt.plot(spikeTimesFromEventOnset, newTrialInds, '.k')
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


dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_nblat.h5')
print 'Saving database to {}'.format(dbPath)
dataframe.to_hdf(dbPath, 'dataframe')

# latencyDataArray = np.array(latencyDataList)
# savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'latency_data.npz')
# np.savez(dataFn, data=latencyDataArray)
