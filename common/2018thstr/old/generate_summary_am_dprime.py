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
from collections import Counter
import itertools

STUDY_NAME = '2018thstr'

def spiketimes_each_frequency(spikeTimesFromEventOnset, trialIndexForEachSpike, freqEachTrial):
    '''
    Generator func to return the spiketimes/trial indices for trials of each frequency
    '''
    possibleFreq = np.unique(freqEachTrial)
    for freq in possibleFreq:
        trialsThisFreq = np.flatnonzero(freqEachTrial==freq)
        spikeTimesThisFreq = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        trialIndicesThisFreq = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisFreq)]
        yield (freq, spikeTimesThisFreq, trialIndicesThisFreq)


dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
dataframe = pd.read_hdf(dbPath, key='dataframe')

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    if not 'am' in dbRow['sessionType']:
        dataframe.loc[indRow, 'd_aMax'] = np.nan
        print 'BREAKING, AM'
        continue
    cell = ephyscore.Cell(dbRow)
    # spikeData, eventData = celldatabase.get_session_ephys(cell, 'am')
    try:
        ephysData, bdata = cell.load('am')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No am session for cell {}".format(indRow)
        dataframe.loc[indRow, 'd_aMax'] = np.nan
        continue

    spikeTimes = ephysData['spikeTimes']

    if len(spikeTimes)<100:
        dataframe.loc[indRow, 'd_aMax'] = np.nan
        print "BREAKING, Spikenum"
        continue

    numFreq = len(np.unique(bdata['currentFreq']))

    allFreqVS = np.empty(numFreq)
    allFreqRal = np.empty(numFreq)
    allFreqPval = np.empty(numFreq)

    eventOnsetTimes = ephysData['events']['soundDetectorOn']
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.7)

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
        dataframe.loc[indRow, 'd_aMax'] = np.nan
        print "Breaking, no significant response"
        continue


    timeRange = [0.1, 0.5] #DONE: Use this to cut out onset responses
    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                timeRange)

    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    numSpikesEachTrialByFrequency = {}
    for indFreq, (freq, spiketimes, trialInds) in enumerate(spiketimes_each_frequency(spikeTimesFromEventOnset,
                                                                                    trialIndexForEachSpike,
                                                                                    freqEachTrial)):
        numSpikesEachTrialThisFreq = []
        spikesPerTrial = Counter(trialInds)
        trialsThisFreq = np.flatnonzero(freqEachTrial==freq)
        for trial in trialsThisFreq:
            spikesThisTrial = spikesPerTrial[trial]
            numSpikesEachTrialThisFreq.append(spikesThisTrial)
        numSpikesEachTrialThisFreq = np.array(numSpikesEachTrialThisFreq)

        numSpikesEachTrialByFrequency.update({freq:numSpikesEachTrialThisFreq})

    d_aAllFreqs = []
    for freq1, freq2 in itertools.combinations(possibleFreq, r=2):
        numSpikes1 = numSpikesEachTrialByFrequency[freq1]
        numSpikes2 = numSpikesEachTrialByFrequency[freq2]
        d_aThisFreq = np.abs((numSpikes1.mean() - numSpikes2.mean()))/np.sqrt((numSpikes1.std()**2 + numSpikes2.std()**2)/2)
        d_aAllFreqs.append(d_aThisFreq)
        d_aMax = max(d_aAllFreqs)

    dataframe.loc[indRow, 'd_aMax'] = d_aMax


savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dataframe.to_hdf(savePath, 'dataframe')
print "SAVED DATAFRAME to {}".format(savePath)

