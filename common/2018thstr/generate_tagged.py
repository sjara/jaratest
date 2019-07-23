import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from scipy import stats
import copy
import pandas as pd
import figparams
reload(figparams)

STUDY_NAME = '2018thstr'
SAVE = True

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbPath = '/tmp/celldatabase_new_20180830.h5'
dataframe = pd.read_hdf(dbPath, key='dataframe')

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):

    cell = ephyscore.Cell(dbRow, useModifiedClusters=True)

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
    responseRange = [0, 0+binTime]
    alignmentRange = [baseRange[0], responseRange[1]]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                   eventOnsetTimes,
                                                                   alignmentRange)
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,responseRange)

    try:
        zStat, pVal = stats.mannwhitneyu(nspkResp, nspkBase)
    except ValueError: #All numbers identical will cause mann whitney to fail
        zStat, pVal = [0, 1]

    # if pVal<0.05 and zStat>0: #This does not work because MW still gives positive Z if response goes down
    if (pVal<0.05) and (nspkResp.ravel().mean() > nspkBase.ravel().mean()):
        passPulse = True
    else:
        passPulse = False


    #Lasertrain analysis
    #There should be a significant response to all of the pulses
    spikeTimes = trainData['spikeTimes']
    trainPulseOnsetTimes = trainData['events']['stimOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(trainPulseOnsetTimes, 0.5)
    baseRange = [-0.050,-0.04]              # Baseline range (in seconds)
    pulseTimes = [0, 0.2, 0.4, 0.6, 0.8]
    # baseRange = [-0.05, -0.03]
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
            zStats[indPulse], pVals[indPulse] = [0, 1]
    numSignificant = sum( pVals<0.05 )
    dataframe.loc[indRow, 'numSignificantTrainResponses'] = numSignificant

    # if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and all(zStats>0):
    if (pVals[0] < 0.05) and (sum(pVals[1:]<0.05) >= 3) and (all(respSpikeMean > nspkBase.ravel().mean())):
        passTrain = True
    else:
        passTrain = False

    if passPulse and passTrain:
        print "PASS"
        dataframe.loc[indRow, 'autoTagged'] = 1
    else:
        print "FAIL"
        dataframe.loc[indRow, 'autoTagged'] = 0

if SAVE:
    # savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
    dataframe.to_hdf(dbPath, 'dataframe')
    print "SAVED DATAFRAME to {}".format(dbPath)
