import os
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from scipy import stats
import numpy as np
from numpy import inf
import pandas
reload(celldatabase)
reload(spikesorting)
reload(ephyscore)

STUDY_NAME = '2018thstr'
SAVE = 1
RECALCULATE_TETRODESTATS=0
FIND_TETRODES_WITH_NO_SPIKES=0

#We need access to ALL of the neurons from all animals that have been recorded from.
animals = ['pinp0'+s for s in map(str, [15, 16, 17, 18, 19, 20, 21, 25, 26, 29])] #22 not done yet
inforecFolder = '/home/nick/src/jaratest/common/inforecordings'

dbList = []
for animal in animals:
    inforecFn = os.path.join(inforecFolder, '{}_inforec.py'.format(animal))

    #If we need to regenerate the tetrodeStats files
    if RECALCULATE_TETRODESTATS:
        ci = spikesorting.ClusterInforec(inforecFn)
        ci.process_all_experiments(recluster=False)

    if FIND_TETRODES_WITH_NO_SPIKES:
        ci = spikesorting.ClusterInforec(inforecFn)
        ci.find_tetrodes_with_no_spikes()
        continue

    db = celldatabase.generate_cell_database(inforecFn)

    #Calculate noiseburst response
    #TODO: Instead of using alternative session types if 'noiseburst' is not available, should we
    #just calculate the onset response to each sound stimulus type and see if any of them are significant?
    noiseZscore = np.empty(len(db))
    noisePval = np.empty(len(db))
    baseRange = [-0.1,0]
    responseRange = [0, 0.1]
    for indRow, dbRow in db.iterrows():

        cell = ephyscore.Cell(dbRow, useModifiedClusters=True)

        if 'noiseburst' in cell.dbRow['sessionType']:
            sessionType = 'noiseburst'
        elif 'rlf' in cell.dbRow['sessionType']:
            sessionType = 'rlf'
        elif 'am' in cell.dbRow['sessionType']:
            sessionType = 'am'
        # spikeData, eventData = cellData.load_ephys(sessionType)
        try:
            ephysData, bdata = cell.load(sessionType)
        except ValueError: #No spike data for that session type
            zScore=0
            pVal=0
        else:
            spikeTimes = ephysData['spikeTimes']
            eventOnsetTimes = ephysData['events']['stimOn']
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

        noiseZscore[indRow] = zScore
        noisePval[indRow] = pVal
    db['noiseZscore'] = noiseZscore
    db['noisePval'] = noisePval

    # #Laser pulse response
    # #NOTE: This does the same thing as the noise burst response, but I am not making a function
    # #because things are getting hidden and I want to be more explicit about what I am doing.
    pulseZscore = np.empty(len(db))
    pulsePval = np.empty(len(db))
    baseRange = [-0.1,0]
    responseRange = [0, 0.1]
    for indRow, dbRow in db.iterrows():

        #Create ephyscore object to load data
        # cellDict = cell.to_dict()
        # cellData = ephyscore.CellData(**cellDict)
        cell = ephyscore.Cell(dbRow)

        if 'laserpulse' in cell.dbRow['sessionType']:
            sessionType = 'laserpulse'
        elif 'lasertrain' in cell.dbRow['sessionType']:
            sessionType = 'lasertrain'
        try:
            ephysData, bdata = cell.load(sessionType)
        except (ValueError, IndexError): #No spike data for that session type
            zScore=0
            pVal=0
        else:
            spikeTimes = ephysData['spikeTimes']
            eventOnsetTimes = ephysData['events']['stimOn']
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
        pulseZscore[indRow] = zScore
        pulsePval[indRow] = pVal
    db['pulseZscore'] = pulseZscore
    db['pulsePval'] = pulsePval

    #Laser train response, ratio of pulse avg spikes
    trainRatio = np.full(len(db), np.nan)
    timeRange = [-0.1, 1] #For initial alignment
    baseRange = [0, 0.05]
    responseRange = [0.2, 0.25]
    for indRow, dbRow in db.iterrows():
        #Create ephyscore object to load data
        cell = ephyscore.Cell(dbRow)
        try:
            ephysData, bdata = cell.load('lasertrain')
        except (ValueError, IndexError): #No spike data for that session type
            continue #Just skip this cell, it will be nan
        else:
            spikeTimes = ephysData['spikeTimes']
            eventOnsetTimes = ephysData['events']['stimOn']
            eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                                        eventOnsetTimes,
                                                                        timeRange)
            avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial,
                                                                        baseRange).mean()
            avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                        indexLimitsEachTrial,
                                                                        responseRange).mean()
            ratio = avgSpikesResp/avgSpikesBase
        trainRatio[indRow] = ratio
    db['trainRatio'] = trainRatio
    dbList.append(db)

masterdb = pandas.concat(dbList, ignore_index=True)
# goodCells = masterdb.query('isiViolations<0.02 and spikeShapeQuality>2')

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'

if SAVE:
    print 'Saving database to {}'.format(dbPath)
    masterdb.to_hdf(dbPath, 'dataframe')

