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
import new_reward_change_behavior_criteria as behavCriteria
import new_activity_consistency_score_celldb as consistentActivity
import new_reward_change_cell_in_target_range_celldb as inTargetRangeCheck

STUDY_NAME = '2017rc'
SAVE_FULL_DB = 1
RECALCULATE_TETRODESTATS=0
FIND_TETRODES_WITH_NO_SPIKES=0
dbKey = 'reward_change'

#We need access to ALL of the neurons from all animals that have been recorded from.
animals = ['adap005']
inforecFolder = settings.INFOREC_PATH

qualityThreshold = 2.5 # conservative quality threshold 
ISIcutoff = 0.02
useStrictBehavCriterionWhenSaving = True
checkDuplicateBeforeSaving = False

# -- params for behavior criteria -- #
minBlockNum = 3
minTrialNumEndBlock = 50 # Last block has to have at least 50 valid trials to count as a block
performanceThreshold = 70 # Has to do over 70% correct overall
#####################################

# -- params for consistent activity check -- #
numBins = 20
sdToMeanRatio=0.5
#############################################

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

    fullDb = celldatabase.generate_cell_database(inforecFn)
    
    dbFolder = os.path.join(settings.DATABASE_PATH, 'new_celldb')
    fullDbFullPath = os.path.join(dbFolder, '{}_database_all_clusters.h5'.format(animal)) 
    if SAVE_FULL_DB:
        print 'Saving database to {}'.format(dbPath)
        fullDb.to_hdf(fullDbFullPath, key=dbKey)

    # -- check if cell meets behavior criteria -- #
    metBehavCriteria = behavCriteria.ensure_behav_criteria_celldb(fullDb, strict=useStrictBehavCriterionWhenSaving,  sessiontype='behavior', minBlockNum=minBlockNum, minTrialNumEndBlock=minTrialNumEndBlock, performanceThreshold=performanceThreshold)
    
    # -- check firing consistency in 2afc session -- #
    consistentFiring = pd.Series(index=fullDb.index, dtype=bool)
    for indCell, cell in fullDb.iterrows():
        cellObj = ephyscore.Cell(cell)
        consistencyThisCell = consistentActivity.score_compare_ave_firing_vs_std(cellObj, sessionToUse='behavior', numBins=numBins, sd2mean=sdToMeanRatio)
        consistentFiring[indCell] = consistencyThisCell

    # -- check if cell depth is inside target region range -- #
    actualDepthEachCell, inTargetArea = inTargetRangeCheck.celldb_in_target_range_check(fullDb, inforecPath = settings.INFOREC_PATH)
    
    # -- check if cell is duplicated -- #
    keepAfterDupTest = 
    goodQualCells['keep_after_dup_test'] = keepAfterDupTest

    # PLAN: calculate behav criteria, firing consistency, depth in target region (by calling designated functions in a separate module), then save only the good qual cells as a celldb, keeping the noncontinuous indices from the original celldb:
    
    goodQualCells = celldb.query('isiViolations<{} and spikeShapeQuality>{}'.format(ISIcutoff, qualityThreshold))

    goodQualCells = goodQualCells.loc[(consistentFiring==True) & (inTargetArea==True) & (metBehavCriteria==True)]
    
    if checkDuplicateBeforeSaving:
        goodQualCells = goodQualCells.query('keep_after_dup_check==True')
    
    
    


    '''
    #Calculate noiseburst response
    #TODO: Instead of using alternative session types if 'noiseburst' is not available, should we
    #just calculate the onset response to each sound stimulus type and see if any of them are significant?
    noiseZscore = np.empty(len(db))
    noisePval = np.empty(len(db))
    baseRange = [-0.1,0]
    responseRange = [0, 0.1]
    for indRow, dbRow in db.iterrows():

        cell = ephyscore.Cell(dbRow)

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
dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
# dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'

if SAVE:
    print 'Saving database to {}'.format(dbPath)
    masterdb.to_hdf(dbPath, 'dataframe')

'''
