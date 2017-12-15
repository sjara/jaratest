import sys
import os
import pandas as pd
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams

threshold = 0.2

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

cellDict = {'subject' : 'pinp017',
            'date' : '2017-03-22',
            'depth' : 1143,
            'tetrode' : 2,
            'cluster' : 4}

cellInd, dbRow = celldatabase.find_cell(dbase, **cellDict)
cell = ephyscore.Cell(dbRow)

try:
    ephysData, bdata = cell.load('tc')
except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
    print "No tc for cell {}".format(indRow)
    sys.exit()

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

thresholdResponse = nspkBase.mean() + threshold*(avgRespArray.max()-nspkBase.mean())

if not np.any(avgRespArray > thresholdResponse):
    print "Nothing above the threshold"
    sys.exit()

#Determine trials that come from a I/F pair with a response above the threshold
fra = avgRespArray > thresholdResponse
validTrials = np.any(trialsEachCondition[:,fra], axis=1)









