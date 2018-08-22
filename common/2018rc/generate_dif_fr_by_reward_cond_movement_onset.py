import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
import figparams
import pdb

ephysDir = settings.EPHYS_PATH_REMOTE
STUDY_NAME = figparams.STUDY_NAME
alignment = 'center-out'
FIGNAME = 'dif_fr_by_reward_sorted_{}'.format(alignment)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

evlockFileFolder = 'evlock_spktimes'
blockLabels = ['more_left','more_right']
sessionType = 'behavior'
soundChannelType = 'stim'
timeRange = [0, 0.31]
removeSideInTrials = True
binWidth = 0.01 #0.05 
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
alphaLevel = 0.05
movementSelWindow = [0.0,0.3]#[0.05, 0.15]

dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)
goodQualCells = celldb.query('keepAfterDupTest==1') # only calculate for non-duplicated cells
encodeMv = (celldb['movementSelective_moredif_Mv'] + celldb['movementSelective_samedif_MvSd']).astype(bool)
encodeSd = celldb['movementSelective_moredif_Sd'].astype(bool)

if removeSideInTrials:
    movementSelective = goodQualCells['movementModS_{}_removedsidein'.format(movementSelWindow)] < alphaLevel
    moreRespMoveLeft = movementSelective & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] < 0)
    moreRespMoveRight = movementSelective & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] > 0)
    # encodeMv = (goodQualCells['movementSelective_moredif_Mv'] + goodQualCells['movementSelective_samedif_MvSd']).astype(bool)
    # encodeSd =  goodQualCells['movementSelective_moredif_Sd'].astype(bool)
    # moreRespMoveLeftEncodeMv = movementSelective & encodeMv & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] < 0)
    # moreRespMoveRightEncodeMv = movementSelective & encodeMv & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] > 0)
    # moreRespMoveLeftEncodeSd = movementSelective & encodeSd & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] < 0)
    # moreRespMoveRightEncodeSd = movementSelective & encodeSd & (goodQualCells['movementModI_{}_removedsidein'.format(movementSelWindow)] > 0)
else:
    movementSelective = goodQualCells['movementModS_{}'.format(movementSelWindow)] < alphaLevel
    moreRespMoveLeft = movementSelective & (goodQualCells['movementModI_{}'.format(movementSelWindow)] < 0)
    moreRespMoveRight = movementSelective & (goodQualCells['movementModI_{}'.format(movementSelWindow)] > 0)

movementSelInds = goodQualCells.index[movementSelective]
goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
goodRightMovementSelCells = goodQualCells[moreRespMoveRight] 
# goodLeftMovementSelCellsEncodeMv = goodQualCells[moreRespMoveLeftEncodeMv]
# goodRightMovementSelCellsEncodeMv = goodQualCells[moreRespMoveRightEncodeMv]
# goodLeftMovementSelCellsEncodeSd = goodQualCells[moreRespMoveLeftEncodeSd]
# goodRightMovementSelCellsEncodeSd = goodQualCells[moreRespMoveRightEncodeSd] 


print '{} cells were movement selective for both areas'.format(sum(movementSelective))

aveSpikeCountByBlockAllCells = np.zeros((2,len(timeVec)-1,len(celldb)))
brainAreaEachCell = np.chararray(len(celldb), itemsize=9)

print('Caculating for all movement selective cells using only trials with preferred direction.')
for indC, cell in goodLeftMovementSelCells.iterrows():
    cellObj = ephyscore.Cell(cell)
    print 'Calculating ave spike count by block for cell {}'.format(indC)
    subject = cell.subject
    date = cell.date
    depth = cell.depth
    brainArea = cell.brainArea
    brainAreaEachCell[indC] = brainArea
    evlockFile = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(subject, date, depth, cell.tetrode, cell.cluster, alignment)
    evlockFilePath = os.path.join(ephysDir, STUDY_NAME, evlockFileFolder, evlockFile)
    evlockData = np.load(evlockFilePath)
    spikeTimesFromEventOnset = evlockData['spikeTimesFromEventOnset']
    trialIndexForEachSpike = evlockData['trialIndexForEachSpike']
    indexLimitsEachTrial = evlockData['indexLimitsEachTrial']
    
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData, bdata = cellObj.load_by_index(sessionInd)
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
    soundOnsetTimeBehav = bdata['timeTarget']
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)
    currentBlock = bdata['currentBlock']
    blockTypes = [bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']] 
    trialsEachBlock = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    choiceEachTrial = bdata['choice']
    leftwardTrials = choiceEachTrial==bdata.labels['choice']['left'] 
    responseTimesEachTrial = bdata['timeSideIn'] - bdata['timeCenterOut'] 
    responseTimesEachTrial[np.isnan(responseTimesEachTrial)] = 0
    sideInTrials = (responseTimesEachTrial <= timeVec[-1])

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    aveSpikeCountByBlock = np.zeros((2,len(timeVec)-1))
    for indB, block in enumerate(blockLabels):
        if removeSideInTrials:
            trialsThisBlock = trialsEachBlock[:, indB] & leftwardTrials & (~sideInTrials)
        else:
            trialsThisBlock = trialsEachBlock[:, indB] & leftwardTrials
        spikeCountThisBlock = spikeCountMat[trialsThisBlock, :]
        aveSpikeCountThisBlock = np.mean(spikeCountThisBlock, axis=0)
        aveSpikeCountByBlock[indB, :] = aveSpikeCountThisBlock
    aveSpikeCountByBlockAllCells[:, :, indC] = aveSpikeCountByBlock
    print 'ave spike count by block for cell {}'.format(indC), aveSpikeCountByBlock

for indC, cell in goodRightMovementSelCells.iterrows():
    cellObj = ephyscore.Cell(cell)
    print 'Calculating ave spike count by block for cell {}'.format(indC)
    subject = cell.subject
    date = cell.date
    depth = cell.depth
    brainArea = cell.brainArea
    brainAreaEachCell[indC] = brainArea
    evlockFile = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(subject, date, depth, cell.tetrode, cell.cluster, alignment)
    evlockFilePath = os.path.join(ephysDir, STUDY_NAME, evlockFileFolder, evlockFile)
    evlockData = np.load(evlockFilePath)
    spikeTimesFromEventOnset = evlockData['spikeTimesFromEventOnset']
    trialIndexForEachSpike = evlockData['trialIndexForEachSpike']
    indexLimitsEachTrial = evlockData['indexLimitsEachTrial']
    
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData, bdata = cellObj.load_by_index(sessionInd)
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
    soundOnsetTimeBehav = bdata['timeTarget']
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)
    currentBlock = bdata['currentBlock']
    blockTypes = [bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']] 
    trialsEachBlock = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    choiceEachTrial = bdata['choice']
    rightwardTrials = choiceEachTrial==bdata.labels['choice']['right']
    responseTimesEachTrial = bdata['timeSideIn'] - bdata['timeCenterOut'] 
    responseTimesEachTrial[np.isnan(responseTimesEachTrial)] = 0
    sideInTrials = (responseTimesEachTrial <= timeVec[-1])

    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    aveSpikeCountByBlock = np.zeros((2,len(timeVec)-1))
    for indB, block in enumerate(blockLabels):
        if removeSideInTrials:
            trialsThisBlock = trialsEachBlock[:, indB] & rightwardTrials & (~sideInTrials)
        else:
            trialsThisBlock = trialsEachBlock[:, indB] & rightwardTrials
        spikeCountThisBlock = spikeCountMat[trialsThisBlock, :]
        aveSpikeCountThisBlock = np.mean(spikeCountThisBlock, axis=0)
        aveSpikeCountByBlock[indB, :] = aveSpikeCountThisBlock
    aveSpikeCountByBlockAllCells[:, :, indC] = aveSpikeCountByBlock
    print 'ave spike count by block for cell {}'.format(indC), aveSpikeCountByBlock

aveSpikeCountByBlockMSCells = aveSpikeCountByBlockAllCells[:,:,movementSelInds]
brainAreaEachCell = brainAreaEachCell[movementSelInds]
encodeMv = encodeMv[movementSelInds]
encodeSd = encodeSd[movementSelInds]

if removeSideInTrials:
    outputFilename = 'average_spike_count_by_rc_cond_preferred_direction_{}ms_bin_{}_win_removed_sidein_trials.npz'.format(int(binWidth*1000), movementSelWindow)
else:
    outputFilename = 'average_spike_count_by_rc_cond_preferred_direction_{}ms_bin_{}_win.npz'.format(int(binWidth*1000), movementSelWindow)

outputFilePath = os.path.join(dataDir, outputFilename)
np.savez(outputFilePath, rightMovementSelInds=goodRightMovementSelCells.index, leftMovementSelInds=goodLeftMovementSelCells.index, 
    timeVec=timeVec, binWidth=binWidth, brainAreaEachCell=np.array(brainAreaEachCell), 
    encodeMv=encodeMv, encodeSd=encodeSd,
    aveSpikeCountByBlock=aveSpikeCountByBlockMSCells)

