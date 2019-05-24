'''
Generate and store spike count differences for same sound, different movement and same movement different sounds.
Lan Guo 2018-08-03
'''
import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import loadbehavior
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams
reload(figparams)

STUDY_NAME = figparams.STUDY_NAME
FIGNAME = 'movement_selectivity'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

scriptFullPath = os.path.realpath(__file__)

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))

####################################################################################
dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)
sessionType = 'behavior'
behavClass = loadbehavior.FlexCategBehaviorData
evlockFolder = 'evlock_spktimes'
evlockDataPath = os.path.join(EPHYS_PATH, STUDY_NAME, evlockFolder)
soundChannelType = 'stim'
alphaLevel = 0.05
movementSelWindow = [0.0, 0.3]
####################################################################################

#goodQualCells = celldb.query('keepAfterDupTest==1') # only calculate for non-duplicated cells
goodQualCells = celldb.query('keepAfterDupTest==1 and cellInTargetArea==1') 
#if removeSideInTrials:
movementSelective = goodQualCells['movementModS_{}_removedsidein'.format(movementSelWindow)] < alphaLevel
#else:
#movementSelective = goodQualCells['movementModS_{}'.format(movementSelWindow)] < alphaLevel
movementSelInds = goodQualCells.index[movementSelective]
goodMovementSelCells = goodQualCells[movementSelective]
difCountHighSoundLvR = np.zeros(len(goodMovementSelCells))
difCountLowSoundLvR = np.zeros(len(goodMovementSelCells))
difCountLowvHighLeft = np.zeros(len(goodMovementSelCells))
difCountLowvHighRight = np.zeros(len(goodMovementSelCells))
brainArea = goodMovementSelCells['brainArea'].values

for indC, (indr, cell) in enumerate(goodMovementSelCells.iterrows()):
    print('Cell {}'.format(indC))
    animal = cell['subject']
    date = cell['date']
    tetrode = cell['tetrode']
    cluster = cell['cluster']
    
    ### Using cellDB methode to find this cell in the cellDB ###
    cell = celldb.loc[(celldb.subject==animal) & (celldb.date==date) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)].iloc[0]
    cellObj = ephyscore.Cell(cell)
    depth = cellObj.dbRow['depth']
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    #bdata = cellObj.load_behavior_by_index(sessionInd, behavClass=behavClass)
    ephysData, bdata = cellObj.load_by_index(sessionInd, behavClass=behavClass)
    
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
    soundOnsetTimeBehav = bdata['timeTarget']
    
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)

    # -- Select trials to plot from behavior file -- #
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    freqEachTrial = bdata['targetFrequency']
    lowFreq = freqEachTrial == bdata['lowFreq'][0]
    highFreq = freqEachTrial == bdata['highFreq'][0]

    responseTimesEachTrial = bdata['timeSideIn'] - bdata['timeCenterOut'] 
    responseTimesEachTrial[np.isnan(responseTimesEachTrial)] = 0
    sideInTrials = (responseTimesEachTrial <= movementSelWindow[-1])

    trialsLeftCorrect = leftward & lowFreq & (~sideInTrials)
    trialsLeftError = leftward & highFreq & (~sideInTrials)
    trialsRightCorrect = rightward & highFreq & (~sideInTrials)
    trialsRightError = rightward & lowFreq & (~sideInTrials)

    alignment = 'center-out'
    evlockDataFilename = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(animal, date, depth, tetrode, cluster, alignment)
    evlockDataFullpath = os.path.join(evlockDataPath, evlockDataFilename) 
    evlockSpktimes = np.load(evlockDataFullpath)
    spikeTimesFromEventOnset = evlockSpktimes['spikeTimesFromEventOnset']
    indexLimitsEachTrial = evlockSpktimes['indexLimitsEachTrial']
    
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
        indexLimitsEachTrial,movementSelWindow)
    spikeCountEachTrial = spikeCountMat.flatten()

    difCountHighSoundLvR[indC] = np.abs(np.mean(spikeCountEachTrial[trialsRightCorrect]) - np.mean(spikeCountEachTrial[trialsLeftError]))
    difCountLowSoundLvR[indC] = np.abs(np.mean(spikeCountEachTrial[trialsLeftCorrect]) - np.mean(spikeCountEachTrial[trialsRightError]))
    difCountLowvHighLeft[indC] = np.abs(np.mean(spikeCountEachTrial[trialsLeftCorrect]) - np.mean(spikeCountEachTrial[trialsLeftError]))
    difCountLowvHighRight[indC] = np.abs(np.mean(spikeCountEachTrial[trialsRightCorrect]) - np.mean(spikeCountEachTrial[trialsRightError]))

    #aveDifSameSoundLvR = np.mean(difCountHighSoundLvR, difCountLowSoundLvR)
    #aveDifLowvHighSameMovement = np.mean(difCountLowvHighLeft, difCountLowvHighRight)

# -- Save raster intermediate data -- #    
outputFile = 'summary_movement_sel_cells_control_sound_resp.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, script=scriptFullPath, movementSelective=movementSelective,
    brainAreaEachCell=brainArea,
    difCountHighSoundLvR=difCountHighSoundLvR,
    difCountLowSoundLvR=difCountLowSoundLvR,
    difCountLowvHighLeft=difCountLowvHighLeft,
    difCountLowvHighRight=difCountLowvHighRight)


