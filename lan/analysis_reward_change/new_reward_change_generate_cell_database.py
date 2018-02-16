import os
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from scipy import stats
import numpy as np
import pandas as pd
reload(celldatabase)
reload(spikesorting)
reload(ephyscore)
import new_reward_change_behavior_criteria as behavCriteria
import new_activity_consistency_score_celldb as consistentActivity
import new_reward_change_cell_in_target_range_celldb as inTargetRangeCheck
import new_good_cell_duplication_check_celldb as duplicationCheck
import new_reward_change_evaluate_sound_response as evaluateSoundResp
import new_reward_change_evaluate_movement_selectivity as evaluateMovementSel

STUDY_NAME = '2017rc'
SAVE_FULL_DB = True
RECALCULATE_TETRODESTATS = False
FIND_TETRODES_WITH_NO_SPIKES = False
dbKey = 'reward_change'

#We need access to ALL of the neurons from all animals that have been recorded from.
animals = ['adap005', 'adap012', 'adap013', 'adap015','adap017','gosi001','gosi004','gosi008','adap067','adap071']  #
#'gosi010' completed 20180213
inforecFolder = settings.INFOREC_PATH

qualityThreshold = 3
ISIcutoff = 0.02
useStrictBehavCriterionWhenSaving = True

# -- params for behavior criteria -- #
minBlockNum = 3
minTrialNumEndBlock = 50 # Last block has to have at least 50 valid trials to count as a block
performanceThreshold = 70 # Has to do over 70% correct overall
#####################################

# -- params for consistent activity check -- #
numBins = 20
sdToMeanRatio=0.5
#############################################
dbFolder = os.path.join(settings.DATABASE_PATH, 'new_celldb')

CASE = 5

if CASE == 1:
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

        fullDbFullPath = os.path.join(dbFolder, '{}_database_all_clusters.h5'.format(animal)) 
        if SAVE_FULL_DB:
            print 'Saving database to {}'.format(fullDbFullPath)
            fullDb.to_hdf(fullDbFullPath, key=dbKey)


if CASE == 2:
    # -- check behavior criteria, cell depth is inside target region, consistent firing during behavior(2afc) session, generate a good quality cell db, save only subset of good qual cells on disk -- #
    for animal in animals:
        fullDbFullPath = os.path.join(dbFolder, '{}_database_all_clusters.h5'.format(animal)) 
        fullDb = pd.read_hdf(fullDbFullPath, key=dbKey) 
        
        # -- check if cell meets behavior criteria -- #
        print 'Checking behavior criteria'
        metBehavCriteria = behavCriteria.ensure_behav_criteria_celldb(fullDb, strict=useStrictBehavCriterionWhenSaving,  sessiontype='behavior', minBlockNum=minBlockNum, minTrialNumEndBlock=minTrialNumEndBlock, performanceThreshold=performanceThreshold)
        fullDb['metBehavCriteria'] = metBehavCriteria

        # -- check if cell depth is inside target region range -- #
        print 'Checking whether cell in target range'
        actualDepthEachCell, inTargetArea = inTargetRangeCheck.celldb_in_target_range_check(fullDb, inforecPath = settings.INFOREC_PATH)
        fullDb['depth_this_cell'] = actualDepthEachCell
        fullDb['inTargetArea'] = inTargetArea

        # calculate behav criteria, and depth in target region (by calling designated functions in a separate module), then save only the good qual cells as a celldb, keeping the noncontinuous indices from the original celldb:
        goodQualCells = fullDb.query('isiViolations<{} and spikeShapeQuality>{} and inTargetArea==True and metBehavCriteria==True'.format(ISIcutoff, qualityThreshold))
        
        print 'Checking consistent firing'
        consistentFiring = pd.Series(index=goodQualCells.index, dtype=bool)
        for indCell, cell in goodQualCells.iterrows():
            cellObj = ephyscore.Cell(cell)
            consistencyThisCell = consistentActivity.score_compare_ave_firing_vs_std(cellObj, sessionToUse='behavior', numBins=numBins, sd2mean=sdToMeanRatio)
            consistentFiring[indCell] = consistencyThisCell
        goodQualCells['consistentFiring'] = consistentFiring
        goodQualCells = goodQualCells.query('consistentFiring==True')

        print 'Saving only cells that met behavior criterion, in target area, and have consistent firing during 2afc into a good quality cell database.'
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        goodQualCells.reset_index(inplace=True)
        goodQualCells.to_hdf(goodDbFullPath, key=dbKey)


if CASE == 3:
    # -- evaluate sound responsiveness; pre-requisite to testing and discarding duplicates -- #
    for animal in animals:
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        goodDb = pd.read_hdf(goodDbFullPath, key=dbKey) 
                
        tuningDict = evaluateSoundResp.evaluate_tuning_sound_response_celldb(goodDb)
        behavDict = evaluateSoundResp.evaluate_2afc_sound_response_celldb(goodDb)
        
        for key in tuningDict:
            goodDb[key] = tuningDict[key]
        for key in behavDict:
            goodDb[key] = behavDict[key]
        
        goodDb.to_hdf(goodDbFullPath, key=dbKey)


if CASE == 4:
    # -- duplicate check and keep the one with largest sound Z score -- #
    corrThreshold = 0.92
    for animal in animals:
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        goodDb = pd.read_hdf(goodDbFullPath, key=dbKey) 
        print 'Checking within session duplicates'
        excludeDfWithinSess = duplicationCheck.find_within_session_duplicates(goodDb, corrThreshold)
        print 'Checking cross session duplicates'
        excludeDfCrossSess = duplicationCheck.find_cross_session_duplicates(goodDb, corrThreshold)
        goodDb['duplicateSelf'] = excludeDfWithinSess['duplicate_self']
        goodDb['duplicateCross'] = excludeDfCrossSess['duplicate_cross']
        goodDb['duplicateSelfDiscard'] = excludeDfWithinSess['duplicate_self_discard']
        goodDb['duplicateCrossDiscard'] = excludeDfCrossSess['duplicate_cross_discard']
        discardAfterDupTest = excludeDfWithinSess['duplicate_self_discard'] | excludeDfCrossSess['duplicate_cross_discard']
        keepAfterDupTest = ~discardAfterDupTest.astype('bool')
        goodDb['keepAfterDupTest'] = keepAfterDupTest
        print 'Finished checking duplication for good cells, saving database...'
        
        goodDb.to_hdf(goodDbFullPath, key=dbKey)


if CASE == 5:
    # -- evaluate movement selectivity -- #
    movementTimeRangeList = [[0.05, 0.15], [0.05, 0.25]] 
    for animal in animals:
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        goodDb = pd.read_hdf(goodDbFullPath, key=dbKey) 
    
        for movementTimeRange in movementTimeRangeList:
            movementModI, movementModS = evaluateMovementSel.evaluate_movement_selectivity_celldb(goodDb, movementTimeRange)
            goodDb['movementModI_{}'.format(movementTimeRange)] = movementModI
            goodDb['movementModS_{}'.format(movementTimeRange)] = movementModS
        goodDb.to_hdf(goodDbFullPath, key=dbKey)


if CASE == 6:
    # -- calculate reward modulation index and modulation direction -- #
    for animal in animals:
        modIndScriptPath = '/home/languo/src/jaratest/lan/analysis_reward_change/new_calculate_reward_modulation_celldb.py'
        # -- Call to calculate modulation indices for different windows different alignments -- #
        commandListCalculate = ['python'] + [modIndScriptPath] + ['--CASE', 'calculate'] + ['-MICE'] + animals
        subprocess.call(commandListCalculate)
        #subprocess.call('python /home/languo/src/jaratest/lan/.py --CASE calculate -MICE adap005 adap012 gosi001'.split(' '))
        # -- Call to merge newly generated mod indices columns into database -- #
        commandListMerge = ['python'] + [modIndScriptPath] + ['--CASE', 'merge'] + ['-MICE'] + animals
        subprocess.call(commandListMerge)
