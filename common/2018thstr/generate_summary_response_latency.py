#We want the latency, but which latency?? We can do lat to first spike for response to a specific type of session
#or to a specific freq/inten combo potentially.

#Try to use the freq/inten combos that have significant responses according to a more strict threshold

#Save the aligned spikes to an NPZ so that we can plot reports

import os
import numpy as np
from numpy import inf
from scipy import optimize
from scipy import stats
from scipy import signal
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
import figparams
import pandas as pd

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')
dataframe = db
threshold = 0.4
latencyDataList = []

for indIter, (indRow, dbRow) in enumerate(dataframe.iterrows()):
    failed=False
    print "Cell {}".format(indRow)
    cell = ephyscore.Cell(dbRow)
    cellData = {}
    try:
        ephysData, bdata = cell.load('tc')
    except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
        failed=True
        print "No tc for cell {}".format(indRow)
        cellData['spikeTimes'] = np.array([])
        cellData['trialInds'] = np.array([])
        dataframe.loc[indRow, 'medianFSLatency'] = np.nan
        latencyDataList.append(cellData)
        #NOTE: If the cell has no TC data we actually don't need to do anything
        #because the arrays are filled with NaN by default
        continue #Move on to the next cell

    # eventOnsetTimes = ephysData['events']['soundDetectorOn']
    # eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.05)
    eventOnsetTimes = ephysData['events']['stimOn']
    spikeTimes = ephysData['spikeTimes']

    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)

    #Init arrays to hold the baseline and response spike counts per condition
    allIntenBase = np.array([])
    allIntenResp = np.empty((len(possibleIntensity), len(possibleFreq)))

    # HARDCODED baseline and response ranges here
    baseRange = [-0.1, 0]
    responseRange = [0, 0.1]
    alignmentRange = [baseRange[0], responseRange[1]]
    #Align all spikes to all events (not sep by freq/inten yet)
    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                alignmentRange)
    #Calculate the number of baseline and response spikes for each trial
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                        indexLimitsEachTrial,
                                                        responseRange)

    #For each f/i pair, find the response spike numbers (we already have all the base spikes)
    for indinten, inten in enumerate(possibleIntensity):
        for indfreq, freq in enumerate(possibleFreq):
            indsThisCombination = np.flatnonzero((freqEachTrial==freq)&(intensityEachTrial==inten))
            respThisCombination = nspkResp[indsThisCombination]
            allIntenResp[indinten, indfreq] = np.mean(respThisCombination)

    thresholdResponse = nspkBase.mean() + threshold*(allIntenResp.max()-nspkBase.mean())

    if not np.any(allIntenResp > thresholdResponse):
        print "Nothing above the threshold"
        cellData['spikeTimes'] = np.array([])
        cellData['trialInds'] = np.array([])
        dataframe.loc[indRow, 'medianFSLatency'] = np.nan
        latencyDataList.append(cellData)
        continue #Move on to the next cell

    fraInds = np.transpose(np.where(allIntenResp > thresholdResponse))

    #Go back and get the actual spiketimes for the combos that pass the threshold
    #Re-align the spikes starting at 0
    alignmentRange = [0, 0.1]
    (spikeTimesFromEventOnset,
    trialIndexForEachSpike,
    indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                eventOnsetTimes,
                                                                alignmentRange)
    spikesAllCombinations = np.array([])
    trialIndsAllCombinations = np.array([])
    latenciesAllCombinations = np.array([])
    for indSet in fraInds:
        thisInten = possibleIntensity[indSet[0]]
        thisFreq = possibleFreq[indSet[1]]
        trialsThisCombination = np.flatnonzero((intensityEachTrial==thisInten) & (freqEachTrial==thisFreq))

        indexLimitsThisCombination = indexLimitsEachTrial[:, trialsThisCombination]

        trialsWithSpikes = np.flatnonzero(indexLimitsThisCombination[1,:]-indexLimitsThisCombination[0,:])

        #Gives the index of the first spike for each of the trials with spikes
        firstSpikeIndThisCombination = indexLimitsThisCombination[0,trialsWithSpikes]

        firstSpikeTimeRelativeToTimeRange = spikeTimesFromEventOnset[firstSpikeIndThisCombination]
        latenciesThisCombination = firstSpikeTimeRelativeToTimeRange - alignmentRange[0]
        latenciesAllCombinations = np.concatenate((latenciesAllCombinations, latenciesThisCombination))

        spikesThisCombination = spikeTimesFromEventOnset[np.in1d(trialIndexForEachSpike, trialsThisCombination)]
        trialIndsThisCombination = trialIndexForEachSpike[np.in1d(trialIndexForEachSpike, trialsThisCombination)]
        spikesAllCombinations = np.concatenate((spikesAllCombinations, spikesThisCombination))
        trialIndsAllCombinations = np.concatenate((trialIndsAllCombinations, trialIndsThisCombination))

    cellData.update({'spikeTimes':spikesAllCombinations})
    cellData.update({'trialInds':trialIndsAllCombinations})

    dataframe.loc[indRow, 'medianFSLatency'] = np.median(latenciesAllCombinations)
    latencyDataList.append(cellData)

latencyDataArray = np.array(latencyDataList)
savePath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'latency_data.npz')
np.savez(dataFn, data=latencyDataArray)
