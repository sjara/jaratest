import os
import numpy as np
import pandas as pd
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from scipy import stats
from matplotlib import pyplot as plt

'''
We used to just use the following:
- Significant p value for laser pulse test on [-0.1, 0] and [0, 0.1]
- Response to second train pulse 0.8 of first or greater.

This failed for several reasons.
- The first test could be non-significant if the response went up and then below baseline in the response window
- The first test could pass if the cell was just inhibited by laser
- The second test would let things through even if the latency to each peak was too long to be direct.
'''
dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase_ALLCELLS.h5'
db = pd.read_hdf(dbPath, key='dataframe')

# Need some example data, using a few sets of manually-selected cells
# goodCellsFolder = '/home/nick/Desktop/2018thstr_goodThalCells_20180326'
# badCellsFolder = '/home/nick/Desktop/2018thstr_badThalCells_20180327'
goodCellsFolder = '/home/nick/Desktop/2018thstr_goodACcells_20180326'
badCellsFolder = '/home/nick/Desktop/2018thstr_badACcells_20180327'

goodCells = os.listdir(goodCellsFolder)
badCells = os.listdir(badCellsFolder)

# for cellName in badCells:
# for cellName in goodCells:
for cellName in ['pinp015_2017-02-15_3110.0_TT7c3']:
    (subject, date, depth, tetrodeCluster) = cellName.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])
    index, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
    cell = ephyscore.Cell(dbRow)

    try:
        pulseData, _ = cell.load('laserpulse')
    except (IndexError, ValueError):
        print "Cell has no laserpulse session, loading laser train session for pulse data"
        try:
            pulseData, _ = cell.load('lasertrain') ##FIXME!!! Loading train if we have no pulse. Bad idea??
        except (IndexError, ValueError):
            print "Cell has no laser train session or no spikes. FAIL!"
            dataframe.loc[indRow, 'autoTagged'] = 0
            continue
    try:
        trainData, _ = cell.load('lasertrain')
    except (IndexError, ValueError):
        print "Cell has no laser train session or no spikes. FAIL!"
        dataframe.loc[indRow, 'autoTagged'] = 0
        continue

    #Laser pulse analysis
    spikeTimes = pulseData['spikeTimes']
    eventOnsetTimes = pulseData['events']['stimOn']
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseRange = [0, 0+binTime]       # NOTE: THIS ONLY EVALUATES [0 0.1] BECAUSE OF THE RESPONSE SCORE BINNING BEHAVIOR
    alignmentRange = [baseRange[0], responseRange[1]]
    # responseTime = responseRange[1]-responseRange[0]
    # numBins = responseTime/binTime
    # binEdges = np.arange(responseRange[0], responseRange[1], binTime)
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)

    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,responseRange)

    zStat, pVal = stats.mannwhitneyu(nspkResp, nspkBase)

    # [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,
    #                                                     indexLimitsEachTrial,baseRange,binEdges)
    #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange

    #Latency? what else should we do here?
    # timeRangeForLatency = [-0.1,0.2]
    # (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
    #                                                         indexLimitsEachTrial,
    #                                                         alignmentRange, threshold=0.5)

    if (pVal<0.05) and (nspkResp.ravel().mean() > nspkBase.ravel().mean()):
        print "PASS"
        # print pVal
        # print zStat
        cond1 = 1
    else:
        # print "FAIL"
        cond1 = 0

    plt.clf()
    plt.subplot(311)
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
    plt.hold()
    plt.axvline(x=baseRange[0], color='b')
    plt.axvline(x=baseRange[1], color='b')
    plt.axvline(x=responseRange[0], color='r')
    plt.axvline(x=responseRange[1], color='r')

    #Lasertrain analysis
    #There should be a significant response to all of the pulses
    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    baseRange = [-0.05, -0.03]
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    alignmentRange = [baseRange[0], pulseTimes[-1]+binTime]

    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)


    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)

    zStats = np.empty(len(pulseTimes))
    pVals = np.empty(len(pulseTimes))
    respSpikeMean = np.empty(len(pulseTimes))
    for indPulse, pulse in enumerate(pulseTimes):
        responseRange = [pulse, pulse+binTime]
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                           indexLimitsEachTrial,responseRange)
        respSpikeMean[indPulse] = nspkResp.ravel().mean()
        try:
            zStats[indPulse], pVals[indPulse] = stats.mannwhitneyu(nspkResp, nspkBase)
        except ValueError: #All numbers identical will cause mann whitney to fail
            zStats[indPulse], pVals[indPulse] = [0, 0]

    # if (pVals[0]<0.05) and (sum(pVals<0.05) > 4):
    if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
        print "PASS, zStats={}".format(zStats)
        cond2 = 1
    else:
        print "FAIL, pVals={}\nzStats={}".format(pVals<0.05, zStats)
        cond2 = 0


    if cond1*cond2 == 1:
        print "PASS"
        # cond2 = 1
    else:
        print "FAIL"
        print "Pulse {} train {}".format(cond1, cond2)
        # cond2 = 0


    plt.subplot(312)
    plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
    plt.hold()
    plt.axvline(x=baseRange[0], color='b')
    plt.axvline(x=baseRange[1], color='b')
    for pulseTime in pulseTimes:
        plt.axvline(x=pulseTime, color='r')
        plt.axvline(x=pulseTime+binTime, color='r')

    plt.subplot(313)
    plt.plot(baseRange[0], nspkBase.ravel().mean(), 'b*')
    plt.plot(pulseTimes, respSpikeMean, 'r*')
    # plt.ylim([0, 2])
    plt.waitforbuttonpress()










