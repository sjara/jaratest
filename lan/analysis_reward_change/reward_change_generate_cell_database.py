import os
import subprocess
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import extrafuncs
reload(extrafuncs)
from scipy import stats
import numpy as np
import pandas as pd
reload(celldatabase)
reload(spikesorting)
reload(ephyscore)
import reward_change_behavior_criteria as behavCriteria
import activity_consistency_score_celldb as consistentActivity
import reward_change_cell_in_target_range_celldb as inTargetRangeCheck
import good_cell_duplication_check_celldb as duplicationCheck
import reward_change_evaluate_sound_response as evaluateSoundResp
import reward_change_evaluate_movement_selectivity as evaluateMovementSel

STUDY_NAME = '2018rc'
SAVE_FULL_DB = True
RECALCULATE_TETRODESTATS = False
FIND_TETRODES_WITH_NO_SPIKES = False
dbKey = 'reward_change'

#We need access to ALL of the neurons from all animals that have been recorded from. 
animals = ['adap005','adap012','adap013','adap015','adap017','gosi001','gosi004','gosi008','gosi010','adap067','adap071']
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

CASE = 12

if CASE == 1:
    # -- Cluster and generate database with all clusters -- #
    for animal in animals:
        inforecFn = os.path.join(inforecFolder, '{}_inforec.py'.format(animal))

        #If we need to regenerate the tetrodeStats files
        if RECALCULATE_TETRODESTATS:
            ci = spikesorting.ClusterInforec(inforecFn)
            ci.process_all_experiments(maxClusters=12, maxPossibleClusters=12, recluster=False)

        if FIND_TETRODES_WITH_NO_SPIKES:
            ci = spikesorting.ClusterInforec(inforecFn)
            ci.find_tetrodes_with_no_spikes()
            continue

        fullDb = celldatabase.generate_cell_database(inforecFn)

        fullDbFullPath = os.path.join(dbFolder, '{}_database_all_clusters.h5'.format(animal)) 
        if SAVE_FULL_DB:
            print 'Saving database to {}'.format(fullDbFullPath)
            #fullDb.to_hdf(fullDbFullPath, key=dbKey)
            celldatabase.save_hdf(fullDb, fullDbFullPath)


if CASE == 2:
    # -- check behavior criteria, cell depth is inside target region, consistent firing during behavior(2afc) session, generate a good quality cell db, save only subset of good qual cells on disk -- #
    for animal in animals:
        fullDbFullPath = os.path.join(dbFolder, '{}_database_all_clusters.h5'.format(animal)) 
        #fullDb = pd.read_hdf(fullDbFullPath, key=dbKey) 
        fullDb = celldatabase.load_hdf(fullDbFullPath)    

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
        #goodQualCells.to_hdf(goodDbFullPath, key=dbKey)
        celldatabase.save_hdf(goodQualCells, goodDbFullPath)

if CASE == 3:
    # -- evaluate sound responsiveness; pre-requisite to testing and discarding duplicates -- #
    for animal in animals:
        print 'Checking sound response in {}'.format(animal)
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        #goodDb = pd.read_hdf(goodDbFullPath, key=dbKey) 
        goodDb = celldatabase.load_hdf(goodDbFullPath)

        tuningDict = evaluateSoundResp.evaluate_tuning_sound_response_celldb(goodDb)
        for key in tuningDict:
            print 'Padding arrays to the same length for storage'
            goodDb[key] = extrafuncs.pad_float_list(tuningDict[key])

        behavDict = evaluateSoundResp.evaluate_2afc_sound_response_celldb(goodDb)
        for key in behavDict:
            goodDb[key] = extrafuncs.pad_float_list(behavDict[key])
        
        #goodDb.to_hdf(goodDbFullPath, key=dbKey)
        celldatabase.save_hdf(goodDb, goodDbFullPath)

if CASE == 4:
    # -- duplicate check and keep the one with largest sound Z score -- #
    corrThreshold = 0.92
    for animal in animals:
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        #goodDb = pd.read_hdf(goodDbFullPath, key=dbKey) 
        goodDb = celldatabase.load_hdf(goodDbFullPath)
        print 'Checking within session duplicates'
        excludeDfWithinSess = duplicationCheck.find_within_session_duplicates(goodDb, corrThreshold)
        print 'Checking cross session duplicates'
        excludeDfCrossSess = duplicationCheck.find_cross_session_duplicates(goodDb, corrThreshold)
        goodDb['duplicateSelf'] = excludeDfWithinSess['duplicate_self']
        goodDb['duplicateCross'] = excludeDfCrossSess['duplicate_cross']
        goodDb['duplicateSelfDiscard'] = excludeDfWithinSess['duplicate_self_discard']
        goodDb['duplicateCrossDiscard'] = excludeDfCrossSess['duplicate_cross_discard']
        discardAfterDupTest = excludeDfWithinSess['duplicate_self_discard'].astype(bool) | excludeDfCrossSess['duplicate_cross_discard'].astype(bool)
        keepAfterDupTest = ~discardAfterDupTest
        keepAfterDupTest = keepAfterDupTest.astype(int)
        goodDb['keepAfterDupTest'] = keepAfterDupTest
        print 'Finished checking duplication for good cells, saving database...'
        celldatabase.save_hdf(goodDb, goodDbFullPath)
        #goodDb.to_hdf(goodDbFullPath, key=dbKey)


if CASE == 5:
    # -- evaluate movement selectivity -- #
    movementTimeRangeList = [[0.05, 0.15], [0.05, 0.25]] 
    for animal in animals:
        goodDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        #goodDb = pd.read_hdf(goodDbFullPath, key=dbKey) 
        goodDb = celldatabase.load_hdf(goodDbFullPath)

        for movementTimeRange in movementTimeRangeList:
            movementModI, movementModS = evaluateMovementSel.evaluate_movement_selectivity_celldb(goodDb, movementTimeRange)
            goodDb['movementModI_{}'.format(movementTimeRange)] = movementModI
            goodDb['movementModS_{}'.format(movementTimeRange)] = movementModS
        #goodDb.to_hdf(goodDbFullPath, key=dbKey)
        celldatabase.save_hdf(goodDb, goodDbFullPath)

if CASE == 6:
    # -- calculate reward modulation index and modulation direction -- #
    for animal in animals:
        modIndScriptPath = '/home/languo/src/jaratest/lan/analysis_reward_change/calculate_reward_modulation_celldb.py'
        # -- Call to calculate modulation indices for different windows different alignments -- #
        commandListCalculate = ['python'] + [modIndScriptPath] + ['--CASE', 'calculate'] + ['--MOUSE', animal]
        subprocess.call(commandListCalculate)

        # -- Call to merge newly generated mod indices columns into database -- #
        commandListMerge = ['python'] + [modIndScriptPath] + ['--CASE', 'merge'] + ['--MOUSE', animal]
        subprocess.call(commandListMerge)

if CASE == 7:
    # -- Merge all individual animal databases into one master db -- #
    dfs = []
    for animal in animals:
        animalDbFullPath = os.path.join(dbFolder, '{}_database.h5'.format(animal)) 
        #animalDb = pd.read_hdf(animalDbFullPath, key=dbKey) 
        animalDb = celldatabase.load_hdf(animalDbFullPath)
        dfs.append(animalDb)
    masterDf = pd.concat(dfs, ignore_index=True)
    for onecol in masterDf.columns:
        onevalue = masterDf.iloc[0][onecol]
        if isinstance(onevalue, np.ndarray):
            masterDf[onecol] = extrafuncs.pad_float_list(masterDf[onecol])
    masterDfFullPath = os.path.join(dbFolder, 'rc_database.h5')
    #masterDf.to_hdf(masterDfFullPath, key=dbKey)
    celldatabase.save_hdf(masterDf, masterDfFullPath)

if CASE == 8:
    # -- For the merged database: calculate reward modulation index during movement while removing trials with side-in -- #
    modIndScriptPath = '/home/languo/src/jaratest/lan/analysis_reward_change/calculate_reward_modulation_during_movement_remove_sidein_trials.py'
    # -- Call to calculate modulation indices for different windows different alignments -- #
    commandListCalculate = ['python'] + [modIndScriptPath] + ['--CASE', 'calculate'] + ['--DBNAME', 'rc_database.h5']
    subprocess.call(commandListCalculate)

    # -- Call to merge newly generated mod indices columns into database -- #
    commandListMerge = ['python'] + [modIndScriptPath] + ['--CASE', 'merge'] + ['--DBNAME', 'rc_database.h5']
    subprocess.call(commandListMerge)

if CASE == 9:
    # -- For the merged database: evaluate movement selectivity while removing trials with side-in -- #
    movementTimeRangeList = [[0.0, 0.3]] 
    dbFullPath = os.path.join(dbFolder, 'rc_database.h5') 
    db = celldatabase.load_hdf(dbFullPath)

    for movementTimeRange in movementTimeRangeList:
        movementModI, movementModS = evaluateMovementSel.evaluate_movement_selectivity_celldb(db, movementTimeRange, removeSideIn=True)
        db['movementModI_{}_removedsidein'.format(movementTimeRange)] = movementModI
        db['movementModS_{}_removedsidein'.format(movementTimeRange)] = movementModS
    #goodDb.to_hdf(goodDbFullPath, key=dbKey)
    celldatabase.save_hdf(db, dbFullPath)

if CASE == 10:
    # -- For the merged database: evaluate movement compared to baseline zScore and pVal while removing trials with side-in -- #
    baselineAlignment = 'sound'
    baselineTimeRange = [-0.1, 0]
    movementAlignment = 'center-out'
    movementTimeRange = [0.0, 0.3]
    removeSideIn = True
    dbFullPath = os.path.join(dbFolder, 'rc_database.h5') 
    db = celldatabase.load_hdf(dbFullPath)

    movementZscore, movementPval, baselineAveFr, movementAveFr = evaluateMovementSel.evaluate_movement_zScore_celldb(db, baselineAlignment=baselineAlignment, 
        baselineTimeRange=baselineTimeRange, movementAlignment=movementAlignment, movementTimeRange=movementTimeRange, 
        removeSideIn=removeSideIn)
    movementZscoreLeft = movementZscore[:,0]
    movementZscoreRight = movementZscore[:,1]
    movementPvalLeft = movementPval[:,0]
    movementPvalRight = movementPval[:,1]
    aveFrLeftwardBaseline = baselineAveFr[:,0] 
    aveFrRightwardBaseline = baselineAveFr[:,1] 
    aveFrLeftwardMovement = movementAveFr[:,0]  
    aveFrRightwardMovement = movementAveFr[:,1]

    if removeSideIn:
        db['movementZscoreLeft_{}_removedsidein'.format(movementTimeRange)] = movementZscoreLeft
        db['movementPvalLeft_{}_removedsidein'.format(movementTimeRange)] = movementPvalLeft
        db['movementZscoreRight_{}_removedsidein'.format(movementTimeRange)] = movementZscoreRight
        db['movementPvalRight_{}_removedsidein'.format(movementTimeRange)] = movementPvalRight
        db['movementAveFrLeft_{}_removedsidein'.format(movementTimeRange)] = aveFrLeftwardMovement
        db['movementAveFrRight_{}_removedsidein'.format(movementTimeRange)] = aveFrRightwardMovement
        db['movementBaselineAveFrLeft_removedsidein'] = aveFrLeftwardBaseline
        db['movementBaselineAveFrRight_removedsidein'] = aveFrRightwardBaseline
        
    else:
        db['movementZscoreLeft_{}'.format(movementTimeRange)] = movementZscoreLeft
        db['movementPvalLeft_{}'.format(movementTimeRange)] = movementPvalLeft
        db['movementZscoreRight_{}'.format(movementTimeRange)] = movementZscoreRight
        db['movementPvalRight_{}'.format(movementTimeRange)] = movementPvalRight
    
    celldatabase.save_hdf(db, dbFullPath)

if CASE == 11:
    # -- For movement-selective cells, mark whether activity is more different based on sound or movement direction -- #
    summaryDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'movement_selectivity')
    summaryFileName = 'summary_movement_sel_cells_control_sound_resp.npz'
    summaryFullPath = os.path.join(summaryDir, summaryFileName)
    summary = np.load(summaryFullPath)

    dbFullPath = os.path.join(dbFolder, 'rc_database.h5') 
    celldb = celldatabase.load_hdf(dbFullPath)

    brainAreaEachCell = summary['brainAreaEachCell']
    difCountHighSoundLvR = summary['difCountHighSoundLvR']
    difCountLowSoundLvR = summary['difCountLowSoundLvR']
    difCountLowvHighLeft = summary['difCountLowvHighLeft']
    difCountLowvHighRight = summary['difCountLowvHighRight']
    aveDifSameSoundLvR = np.mean(np.c_[difCountHighSoundLvR, difCountLowSoundLvR], axis=1)
    aveDifLowvHighSameMovement = np.mean(np.c_[difCountLowvHighLeft, difCountLowvHighRight], axis=1)

    careMoreAboutMv = (aveDifSameSoundLvR > aveDifLowvHighSameMovement)
    careMoreAboutSound = (aveDifSameSoundLvR < aveDifLowvHighSameMovement)
    careEquallyAboutMvAndSound = (aveDifSameSoundLvR == aveDifLowvHighSameMovement)
    
    movementSelWindow = [0.0, 0.3]
    alphaLevel = 0.05
    goodQualCells = celldb.query('keepAfterDupTest==1') # only calculate for non-duplicated cells
    movementSelective = goodQualCells['movementModS_{}_removedsidein'.format(movementSelWindow)] < alphaLevel
    movementSelInds = goodQualCells.index[movementSelective]

    celldb['movementSelective_moredif_Mv'] = np.zeros(len(celldb), dtype=int)
    celldb['movementSelective_moredif_Sd'] = np.zeros(len(celldb), dtype=int)
    celldb['movementSelective_samedif_MvSd'] = np.zeros(len(celldb), dtype=int)

    celldb.loc[movementSelInds, 'movementSelective_moredif_Mv'] = careMoreAboutMv.astype(int)
    celldb.loc[movementSelInds, 'movementSelective_moredif_Sd'] = careMoreAboutSound.astype(int)
    celldb.loc[movementSelInds, 'movementSelective_samedif_MvSd'] = careEquallyAboutMvAndSound.astype(int)

    celldatabase.save_hdf(celldb, dbFullPath)

if CASE == 12:
    # -- For the merged database: evaluate sound frequency selectivity in 2afc task -- #
    dbFullPath = os.path.join(dbFolder, 'rc_database.h5') 
    db = celldatabase.load_hdf(dbFullPath)

    soundFreqSelPval = evaluateSoundResp.evaluate_2afc_sound_selectivity_celldb(db)
    db['soundFreqSelectivityPval'] = soundFreqSelPval
    
    celldatabase.save_hdf(db, dbFullPath)