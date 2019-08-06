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

    numFreq = len(np.unique(bdata['currentFreq']))

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

    cellLatency = dbRow['latency']
    if not cellLatency > 0:
        print "Negative latency!! Skipping"
        continue

    baseRange = [-0.1, -0.05]
    # responseRange = [0, 0.05, 0.1]
    # responseRange = [cellLatency, cellLatency + 0.05, 0.1+cellLatency]
    onsetRange = [cellLatency, cellLatency + 0.05]
    sustainedRange = [cellLatency + 0.05, cellLatency + 0.5]


    alignmentRange = [onsetRange[0], sustainedRange[-1]]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)


    nspkOnset = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                         onsetRange)

    nspkSustained = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                             sustainedRange)

    avgOnset = nspkOnset.mean(axis=0)
    timeRangeOnset = onsetRange[1] - onsetRange[0]
    onsetRate = avgOnset / timeRangeOnset

    avgSustained = nspkSustained.mean(axis=0)
    timeRangeSustained = sustainedRange[1] - sustainedRange[0]
    sustainedRate = avgSustained/timeRangeSustained

    dataframe.loc[indRow, 'onsetRate'] = onsetRate
    dataframe.loc[indRow, 'sustainedRate'] = sustainedRate

