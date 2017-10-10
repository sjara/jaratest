import os
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from scipy import stats
import numpy as np
from numpy import inf
import pandas

STUDY_NAME = '2018thstr'

#We need access to ALL of the neurons from all animals that have been recorded from.
animals = ['pinp0'+s for s in map(str, [15, 16, 17, 18, 19, 20, 21, 25])] #22 not done yet
inforecFolder = '/home/nick/src/jaratest/common/inforecordings'

dbList = []
for animal in animals:
    inforecFn = os.path.join(inforecFolder, '{}_inforec.py'.format(animal))
    db = celldatabase.generate_cell_database(inforecFn)

    #Calculate shape quality
    allShapeQuality = np.empty(len(db))
    for indCell, cell in db.iterrows():
        peakAmplitudes = cell['clusterPeakAmplitudes']
        spikeShapeSD = cell['clusterSpikeSD']
        shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
        allShapeQuality[indCell] = shapeQuality
    allShapeQuality[allShapeQuality==inf]=0
    db['shapeQuality'] = allShapeQuality

    #Calculate noiseburst response
    #TODO: Instead of using alternative session types if 'noiseburst' is not available, should we
    #just calculate the onset response to each sound stimulus type and see if any of them are significant?
    noiseZscore = np.empty(len(db))
    noisePval = np.empty(len(db))
    baseRange = [-0.2,0]
    responseRange = [0, 0.2]
    for indCell, cell in db.iterrows():
        if 'noiseburst' in cell['sessiontype']:
            sessiontype = 'noiseburst'
        elif 'rlf' in cell['sessiontype']:
            sessiontype = 'rlf'
        elif 'am' in cell['sessiontype']:
            sessiontype = 'am'
        spikeData, eventData = celldatabase.get_session_ephys(cell, sessiontype)
        if spikeData.timestamps is not None:
            eventOnsetTimes = eventData.get_event_onset_times()
            alignmentRange = [baseRange[0], responseRange[1]]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        alignmentRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)
            [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        else:
            zScore=0
            pVal=0
        noiseZscore[indCell] = zScore
        noisePval[indCell] = pVal
    db['noiseZscore'] = noiseZscore
    db['noisePval'] = noisePval

    #Laser pulse response
    #NOTE: This does the same thing as the noise burst response, but I am not making a function
    #because things are getting hidden and I want to be more explicit about what I am doing.
    pulseZscore = np.empty(len(db))
    pulsePval = np.empty(len(db))
    baseRange = [-0.1,0]
    responseRange = [0, 0.1]
    for indCell, cell in db.iterrows():
        if 'laserpulse' in cell['sessiontype']:
            sessiontype = 'laserpulse'
        elif 'lasertrain' in cell['sessiontype']:
            sessiontype = 'lasertrain'
        spikeData, eventData = celldatabase.get_session_ephys(cell, sessiontype)
        if spikeData.timestamps is not None:
            eventOnsetTimes = eventData.get_event_onset_times()
            alignmentRange = [baseRange[0], responseRange[1]]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        alignmentRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)
            [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
        else:
            zScore=0
            pVal=0
        pulseZscore[indCell] = zScore
        pulsePval[indCell] = pVal
    db['pulseZscore'] = pulseZscore
    db['pulsePval'] = pulsePval

    #Laser train response, ratio of pulse avg spikes
    trainRatio = np.empty(len(db))
    timeRange = [-0.1, 1] #For initial alignment
    baseRange = [0, 0.05]
    responseRange = [0.2, 0.25]
    for indCell, cell in db.iterrows():
        if 'laserpulse' in cell['sessiontype']:
            spikeData, eventData = celldatabase.get_session_ephys(cell, 'lasertrain')
            if spikeData.timestamps is not None:
                eventOnsetTimes = eventData.get_event_onset_times()
                eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
                (spikeTimesFromEventOnset,
                trialIndexForEachSpike,
                indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                            eventOnsetTimes,
                                                                            timeRange)
                avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                            indexLimitsEachTrial,
                                                                            baseRange).mean()
                avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                            indexLimitsEachTrial,
                                                                            responseRange).mean()
                ratio = avgSpikesResp/avgSpikesBase
            else:
                ratio = 0
        else:
            ratio = 0
        trainRatio[indCell] = ratio
    db['trainRatio'] = trainRatio

    dbList.append(db)

masterdb = pandas.concat(dbList, ignore_index=True)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'

masterdb.to_hdf(dbPath, 'dataframe')

