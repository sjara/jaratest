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
FIGNAME = 'dif_fr_sorted_{}'.format(alignment)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

evlockFileFolder = 'evlock_spktimes'
blockLabels = ['more_left', 'more_right']
movementDirections = ['left', 'right']
sessionType = 'behavior'
soundChannelType = 'stim'
timeRange = [-0.2, 0.5]
binWidth = 0.010 #0.025 #10 msec
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
alphaLevel = 0.05
movementSelWindow = [0.05, 0.15]

dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)
goodQualCells = celldb.query('keepAfterDupTest==1 and missingTrialsBehav==0') # only calculate for non-duplicated cells
movementSelective = goodQualCells['movementModS_{}'.format(movementSelWindow)] < alphaLevel
goodMovementSelCells = goodQualCells[movementSelective]
moreRespMoveLeft = movementSelective & (goodQualCells['movementModI_{}'.format(movementSelWindow)] < 0)
moreRespMoveRight = movementSelective & (goodQualCells['movementModI_{}'.format(movementSelWindow)] > 0)
goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
goodRightMovementSelCells = goodQualCells[moreRespMoveRight]
movementSelInds = goodQualCells.index[movementSelective]

print '{} cells were movement selective for both areas'.format(sum(movementSelective))

aveFrByDirByRwAllCells = np.zeros((len(movementDirections), len(blockLabels), len(timeVec)-1, len(celldb)))
brainAreaEachCell = np.chararray(len(celldb), itemsize=9)

print('Caculating for all movement selective cells per movement direction and reward contingency')
for indC, cell in goodMovementSelCells.iterrows():
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
    rightwardTrials = choiceEachTrial==bdata.labels['choice']['right'] 
    trialsEachDir = np.column_stack((leftwardTrials, rightwardTrials))
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    for indD, direction in enumerate(movementDirections):
        for indB, block in enumerate(blockLabels):
            trialsThisCond = trialsEachBlock[:, indB] & trialsEachDir[:, indD]
            spikeCountThisCond = spikeCountMat[trialsThisCond, :]
            aveSpikeCountThisCond = np.mean(spikeCountThisCond, axis=0)
            aveFrByDirByRwAllCells[indD, indB, :, indC] = aveSpikeCountThisCond

aveFrLeftwardLeftMoreAllCells = aveFrByDirByRwAllCells[0, 0, :, movementSelInds]
aveFrLeftwardRightMoreAllCells = aveFrByDirByRwAllCells[0, 1, :, movementSelInds]
aveFrRightwardLeftMoreAllCells = aveFrByDirByRwAllCells[1, 0, :, movementSelInds]
aveFrRightwardRightMoreAllCells = aveFrByDirByRwAllCells[1, 1, :, movementSelInds]
brainAreaEachCell = brainAreaEachCell[movementSelInds]
outputFilename = 'average_spike_count_by_rc_cond_by_direction_{}ms_bin.npz'.format(int(binWidth*1000))
outputFilePath = os.path.join(dataDir, outputFilename)
np.savez(outputFilePath, movementSelInds=movementSelInds, 
    timeVec=timeVec, binWidth=binWidth, brainAreaEachCell=np.array(brainAreaEachCell), 
    aveFrLeftwardLeftMoreAllCells=aveFrLeftwardLeftMoreAllCells,
    aveFrLeftwardRightMoreAllCells=aveFrLeftwardRightMoreAllCells,
    aveFrRightwardLeftMoreAllCells=aveFrRightwardLeftMoreAllCells,
    aveFrRightwardRightMoreAllCells=aveFrRightwardRightMoreAllCells)

