from jaratest.nick.database import dataloader_v2 as dataloader
import pandas
import numpy as np
from numpy import nan
from jaratoolbox import spikesanalysis
from scipy import stats
import matplotlib.pyplot as plt

dbFn = '/home/nick/data/database/pinp016/pinp016_database_shapeQual.h5'
pinp016db = pandas.read_hdf(dbFn, key='database')


#Pulse response is a z-score for the response in the 100msec after the
#onset of the laser pulse
pulseZscore = np.empty(len(pinp016db))
pulsePval = np.empty(len(pinp016db))

for indCell, cell in pinp016db.iterrows():
    loader = dataloader.DataLoader(cell['subject'])
    pulseSession = cell['ephys'][cell['sessiontype'].index('laserpulse')]
    eventData = loader.get_session_events(pulseSession)
    try:
        spikeData = loader.get_session_spikes(pulseSession, int(cell['tetrode']), cluster=int(cell['cluster']))
    except AttributeError:
        pulseZscore[indCell] = 0
        pulsePval[indCell] = 0
        continue

    eventOnsetTimes = loader.get_event_onset_times(eventData)

    timeRange = [-0.1, 0.1]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                   eventOnsetTimes,
                                                                   timeRange)
    baseRange = [-0.1,0]
    responseRange = [0, 0.1]
    nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange)
    nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)

    [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)

    pulseZscore[indCell] = zScore
    pulsePval[indCell] = pVal


#Laser train ratio of pulse 2 to pulse 1
trainRatio = np.empty(len(pinp016db))

for indCell, cell in pinp016db.iterrows():
    loader = dataloader.DataLoader(cell['subject'])
    trainSession = cell['ephys'][cell['sessiontype'].index('lasertrain')]
    eventData = loader.get_session_events(trainSession)
    try:
        spikeData = loader.get_session_spikes(trainSession, int(cell['tetrode']), cluster=int(cell['cluster']))
    except AttributeError:
        trainRatio[indCell] = 0
        continue

    eventOnsetTimes = loader.get_event_onset_times(eventData)
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.1)

    timeRange = [-0.1, 1]
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                   eventOnsetTimes,
                                                                   timeRange)
    # plt.clf()
    # plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
    # plt.show()
    # plt.waitforbuttonpress()

    baseRange = [0, 0.01]
    responseRange = [0.2, 0.21]
    avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange).mean()
    avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange).mean()

    ratio = avgSpikesResp/avgSpikesBase
    trainRatio[indCell] = ratio

pinp016db['pulseZscore'] = pulseZscore
pinp016db['pulsePval'] = pulsePval
pinp016db['trainRatio'] = trainRatio

dbFn = '/home/nick/data/database/pinp016/pinp016_database_shape_laser.h5'
pinp016db.to_hdf(dbFn, 'database')
