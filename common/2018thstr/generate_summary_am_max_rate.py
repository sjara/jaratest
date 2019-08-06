import pandas as pd
from scipy import signal
from scipy import stats
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import ephyscore
import figparams
from matplotlib import pyplot as plt
import os


dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_calculated_columns.h5'
dataframe = celldatabase.load_hdf(dbPath)

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    if not 'am' in dbRow['sessionType']:
        # dataframe.loc[indRow, 'highestSync'] = np.nan
        print 'BREAKING, AM'
        continue
    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)
    # spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
    try:
        ephysData, bdata = cell.load('am')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No am session for cell {}".format(indRow)
        # dataframe.loc[indRow, 'highestSync'] = np.nan
        continue

    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']

    if len(spikeTimes)<100:
        # dataframe.loc[indRow, 'highestSync'] = np.nan
        print "BREAKING, Spikenum"
        continue

    rateEachTrial = bdata['currentFreq']
    possibleRate = np.unique(rateEachTrial)

    if len(rateEachTrial) != len(eventOnsetTimes):
        eventOnsetTimes = eventOnsetTimes[:-1]
        if len(rateEachTrial) != len(eventOnsetTimes):
            raise ValueError('Removing one does not align events and behavior')

    # numFreq = len(np.unique(bdata['currentFreq']))

    ### --- Test to see if there is a response to the AM session --- ###
    baseRange = [-0.5, -0.1]
    responseRange = [0.1, 0.5]
    alignmentRange = [baseRange[0], responseRange[1]]
    (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventOnsetTimes,
                                                                    alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)
    [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
    if pVal > 0.05: #No response
        # dataframe.loc[indRow, 'highestSync'] = np.nan
        print "Breaking, no significant response"
        continue


    # timeRange = [0.1, 0.5] #DONE: Use this to cut out onset responses
    # onsetRange = [0, 0.05]
    # sustainedRange = [0.05, 0.5]

    baseRange = [-0.1, -0.05]
    responseRange = [0, 0.5]
    # responseRange = [cellLatency, cellLatency + 0.05, 0.1+cellLatency]


    alignmentRange = [baseRange[0], responseRange[-1]]


    evokedFREachRate = np.zeros(len(possibleRate))
    baselineFREachRate = np.zeros(len(possibleRate))

    for indRate, thisRate in enumerate(possibleRate):

        eventsThisRate = eventOnsetTimes[rateEachTrial==thisRate]

        (spikeTimesFromEventOnset,
        trialIndexForEachSpike,
        indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                    eventsThisRate,
                                                                    alignmentRange)

        nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            baseRange)

        nspkResponse = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)

        avgResponse = nspkResponse.mean(axis=0)
        timeRangeResponse = responseRange[1] - responseRange[0]
        responseRate = avgResponse / timeRangeResponse

        avgBase = nspkBase.mean(axis=0)
        timeRangeBase = baseRange[1] - baseRange[0]
        baseRate = avgBase / timeRangeBase

        evokedFREachRate[indRate] = responseRate
        baselineFREachRate[indRate] = baseRate


    dataframe.loc[indRow, 'maxRateAM'] = np.max(evokedFREachRate)
    dataframe.loc[indRow, 'baseRateAM'] = np.mean(baselineFREachRate)

