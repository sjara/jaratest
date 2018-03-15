import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
reload(spikesanalysis)
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')
strCells = dbase.groupby('brainArea').get_group('rightAstr')
# strCellsToPlot = strCells[pd.notnull(strCells['BW10'])]

for indRow, dbRow in strCells.iterrows():
    cell = ephyscore.Cell(dbRow)

    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        print "No tc for cell {}".format(indRow)
        continue

    eventOnsetTimes = ephysData['events']['soundDetectorOn']

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

    plt.clf()
    ax = plt.subplot(111)
    plt.imshow(np.flipud(avgRespArray), interpolation='none', cmap='Blues')
    ax.set_yticks(range(len(possibleIntensity)))
    ax.set_yticklabels(possibleIntensity[::-1])
    ax.set_xticks(range(len(possibleFreq)))
    freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    ax.set_xticklabels(freqLabels, rotation='vertical')
    ax.set_xlabel('Frequency (kHz)')
    plt.ylabel('Intensity (db SPL)')

    figName = '{name}_{date}_{depth}um_TT{tetrode}c{cluster}.png'.format(name = cell.subject,
                                                                        date = cell.dbRow['date'],
                                                                        depth = cell.dbRow['depth'],
                                                                        tetrode = cell.tetrode,
                                                                        cluster = cell.cluster)
    savePath = os.path.join('/home/nick/data/reports/nick/20171218_striatum_freq', figName)
    plt.savefig(savePath)
