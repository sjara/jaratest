from jaratest.nick.database import dataloader_v2 as dataloader
import numpy as np
from jaratoolbox import spikesanalysis
from scipy import stats

def event_response_score(cell, sessiontype,
                         responseRange = [0, 0.1],
                         baseRange=[-0.1, 0]):
    loader = dataloader.DataLoader(cell['subject'])
    session = cell['ephys'][cell['sessiontype'].index(sessiontype)]
    eventData = loader.get_session_events(session)
    try:
        spikeData = loader.get_session_spikes(session, int(cell['tetrode']), cluster=int(cell['cluster']))
    except AttributeError:
        return (0, 0)
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
    return zScore, pVal

def train_response_ratio(cell, sessiontype,
                         minEventOnsetDiff=0.1,
                         timeRange = [-0.1, 1],
                         baseRange = [0, 0.05],
                         responseRange = [0.2, 0.25]):
    loader = dataloader.DataLoader(cell['subject'])
    trainSession = cell['ephys'][cell['sessiontype'].index(sessiontype)]
    eventData = loader.get_session_events(trainSession)
    try:
        spikeData = loader.get_session_spikes(trainSession, int(cell['tetrode']), cluster=int(cell['cluster']))
    except AttributeError:
        return 0
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff)
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                   eventOnsetTimes,
                                                                   timeRange)
    avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange).mean()
    avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange).mean()
    ratio = avgSpikesResp/avgSpikesBase





#DEPRECATED, old version used for SFN 2016 poster analysis
# def response_reliability(cell, sessiontype='LaserTrain',
#                          responseRange = [0, 0.04],
#                          baseRange=[-0.04, 0],
#                          pulse=4):
#     '''
#     Percent of trials where response range spikes/sec greater than base range
#     Use for laser train analysis
#     '''
#     #Find the index of the ephys for this session if it exists
#     try:
#         sessiontypeIndex = cell['sessiontype'].index(sessiontype)
#     except ValueError: #The cell does not have this session type
#         return None
#     #Initialize a data loader for this animal
#     loader = dataloader.DataLoader(cell['subject'])
#     ephysDir = cell['ephys'][sessiontypeIndex]
#     clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
#     clusterSpikeTimes = clusterSpikeData.timestamps
#     #Get the events for this session and calculate onset times
#     eventData = loader.get_session_events(ephysDir)
#     eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)
#     if pulse:
#         onsetTimesToUse = np.arange(pulse, len(eventOnsetTimes), 5)
#         eventOnsetTimes = eventOnsetTimes[onsetTimesToUse]
#     # import ipdb; ipdb.set_trace()
#     alignmentRange = [baseRange[0], responseRange[1]]
#     (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
#     spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes,eventOnsetTimes,alignmentRange)
#     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         baseRange)
#     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         responseRange)
#     nspkBase=nspkBase[:,0]
#     nspkResp=nspkResp[:,0]
#     print sum(nspkBase)
#     print sum(nspkResp)
#     reliability = sum(nspkResp>nspkBase)/np.double(len(nspkResp))
#     return reliability


#DEPRECATED, old version used for SFN 2016 poster analysis
# def event_response_score(cell, sessiontype,
#                          responseRange = [0, 0.1],
#                          baseRange=[-0.050, -0.025],
#                          skip=False):
#     '''
#     Used to calculate simple response to noise bursts and laser pulses
#     '''

#     #Find the index of the ephys for this session if it exists
#     try:
#         sessiontypeIndex = cell['sessiontype'].index(sessiontype)
#     except ValueError: #The cell does not have this session type
#         return None, None

#     #Initialize a data loader for this animal
#     loader = dataloader.DataLoader(cell['subject'])

#     ephysDir = cell['ephys'][sessiontypeIndex]
#     clusterSpikeData = loader.get_session_spikes(ephysDir, int(cell['tetrode']), cluster=int(cell['cluster']))
#     clusterSpikeTimes = clusterSpikeData.timestamps

#     #Get the events for this session and calculate onset times
#     eventData = loader.get_session_events(ephysDir)
#     eventOnsetTimes = loader.get_event_onset_times(eventData, minEventOnsetDiff=None)

#     if skip:
#         onsetTimesToUse = np.arange(skip, len(eventOnsetTimes), skip)
#         eventOnsetTimes = eventOnsetTimes[onsetTimesToUse]


#     alignmentRange = [baseRange[0], responseRange[1]]

#     (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
#     spikesanalysis.eventlocked_spiketimes(clusterSpikeTimes,eventOnsetTimes,alignmentRange)

#     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         baseRange)
#     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         responseRange)

#     zStat, pValue = stats.ranksums(nspkResp[:,0], nspkBase[:,0])

#     return zStat, pValue
