"""

Now processing  d1pi041 2019-08-25 2700.0 4 1 4
/data/behavior/d1pi041/d1pi041_am_tuning_curve_20190825    .h5 

"""

import os
import sys
import numpy as np
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from matplotlib import pyplot as plt

sys.path.append('..')
import studyparams
import database_generation_funcs as funcs


'''
subject = 'd1pi041'
date = '2019-08-25'
depth = 2700
tetrode = 4
cluster = 6
'''

CASE = 0
if CASE==0:
    cellToUse = ('d1pi041','2019-08-31',3500,8,6) # Latency=7ms
elif CASE==1:
    cellToUse = ('d1pi041','2019-08-25',3400,7,6) # Latency=14.8ms

subject = cellToUse[0]
dbPath = '/data/figuresdata/2019astrpi/test{}.h5'.format(subject)
basicDB = celldatabase.load_hdf(dbPath)

    
subject, date, depth, tetrode, cluster = cellToUse
(indRow, dbRow) = celldatabase.find_cell(basicDB, subject, date, depth, tetrode, cluster)
oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)

session = 'tuningCurve'
tuningEphysData, tuningBehavData = oneCell.load(session)


baseRange = [-0.1, 0]

# Extracting information from ephys and behavior data to do calculations later with
currentFreq = tuningBehavData['currentFreq']
currentIntensity = tuningBehavData['currentIntensity']
uniqFreq = np.unique(currentFreq)
uniqueIntensity = np.unique(currentIntensity)
tuningTrialsEachCond = behavioranalysis.find_trials_each_combination(currentFreq, uniqFreq, currentIntensity, uniqueIntensity)

allIntenBase = np.array([])
respSpikeMean = np.empty((len(uniqueIntensity), len(uniqFreq)))  # same as allIntenResp
allIntenRespMedian = np.empty((len(uniqueIntensity), len(uniqFreq)))
Rsquareds = []
popts = []
tuningSpikeTimes = tuningEphysData['spikeTimes']
tuningEventOnsetTimesOrig = tuningEphysData['events']['soundDetectorOn']
tuningEventOnsetTimes = spikesanalysis.minimum_event_onset_diff(tuningEventOnsetTimesOrig, minEventOnsetDiff=0.2)

if len(tuningEventOnsetTimes) == (len(currentFreq) + 1):
    tuningEventOnsetTimes = tuningEventOnsetTimes[0:-1]
    print("Removing incomplete trials at the end of ephys data.")
    toCalculate = True
elif len(tuningEventOnsetTimes) == len(currentFreq):
    print("Data is already the same length")
    toCalculate = True
else:
    print("Something is wrong with the length of these data")
    toCalculate = False


spikeTimes = tuningSpikeTimes
eventOnsetTimes = tuningEventOnsetTimes
alignmentRange = [-0.2, 0.2]
(spikeTimesFromEventOnset,
 trialIndexForEachSpike,
 indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                               eventOnsetTimes,
                                                               alignmentRange)

binEdges = np.arange(*alignmentRange,0.002)
spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,binEdges)
sumSpikes = np.sum(spikeCountMat,axis=0)

plt.clf()
ax0 = plt.subplot(2,1,1)
plt.plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.')
ax1 = plt.subplot(2,1,2, sharex=ax0)
plt.step(binEdges[:-1],sumSpikes, where='post')
plt.show()

sys.exit()


