'''
Updated to use new celldb.
This script take a cell database for reward-change mice that includes only the good quality cells that passed shape quality, isi, consistent firing, in target area check. The database includes basic information such as subject, date, behavior sessions, ephys sessions, sessiontype, tetrode, cluster, depth, brainarea recorded from, inforecPath etc. Also includes measurements calculated while clustering: 'clusterPeakAmplitudes', 'clusterPeakTimes', 'clusterSpikeSD', 'clusterSpikeShape', 'isiViolations', 'nSpikes'.
Measurements calculated to reflect movement selectivity from this script: 'movementModI' and 'movementModS' for each time period specified.
The script is to be run after the database has been fully generated and good quality cells database saved. 
Lan 2018-01-02
'''
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import settings
reload(settings)
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import os
import pandas as pd
import subprocess
import numpy as np
import importlib
import sys
from scipy import stats

#animal = 'adap005'

#databaseFullPath = os.path.join(settings.DATABASE_PATH, 'new_celldb', '{}_database.h5'.format(animal))
#key = 'reward_change'

timeRange = [-0.5,0.5]
#movementTimeRangeList = [[0.05, 0.15], [0.05, 0.25]] 
#soundTriggerChannel = 0
soundChannelType = 'stim'
ephysDir = settings.EPHYS_PATH_REMOTE
STUDY_NAME = '2018rc'
evlockFileFolder = 'evlock_spktimes'

#cellDb = pd.read_hdf(databaseFullPath, key=key)

def evaluate_movement_selectivity_celldb(cellDb, movementTimeRange, removeSideIn=False):
    '''
    Analyse 2afc data: calculate movement selectivity index and significance;
    movementTimeRange should be a list (in seconds, time from center-out).
    '''
    print 'Calculating movement selectivity index for 2afc session in time range: ' + str(movementTimeRange)

    movementModI = pd.Series(np.zeros(len(cellDb)), index=cellDb.index) #default value 0
    movementModS = pd.Series(np.ones(len(cellDb)), index=cellDb.index) #default value 1

    for indCell, cell in cellDb.iterrows():
        cellObj = ephyscore.Cell(cell)
        sessiontype = 'behavior'  #2afc behavior
        #ephysData, bata = cellObj.load(sessiontype)
        sessionInd = cellObj.get_session_inds(sessiontype)[0]
        bdata = cellObj.load_behavior_by_index(sessionInd)
        possibleFreq = np.unique(bdata['targetFrequency'])
        numFreqs = len(possibleFreq)

        try:
            ephysData = cellObj.load_ephys_by_index(sessionInd)
        except ValueError:
            continue

        eventsDict = ephysData['events']
        spikeTimestamps = ephysData['spikeTimes']

        if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
            continue

        soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]
        soundOnsetTimeBehav = bdata['timeTarget']

        # -- Check to see if ephys and behav recordings have same number of trials, remove missing trials from behav file -- #
        # Find missing trials
        missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimes,soundOnsetTimeBehav)
        # Remove missing trials
        bdata.remove_trials(missingTrials)

        if len(soundOnsetTimes) != len(bdata['timeTarget']): #some error not handled by remove missing trials
            continue

        # -- calculate movement selectivity -- #
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left'] 
       
        diffTimes = bdata['timeCenterOut'] - bdata['timeTarget']
        movementOnsetTimes = soundOnsetTimes + diffTimes

        responseTimesEachTrial = bdata['timeSideIn'] - bdata['timeCenterOut'] 
        responseTimesEachTrial[np.isnan(responseTimesEachTrial)] = 0
        sideInTrials = (responseTimesEachTrial <= movementTimeRange[-1])
        
        if removeSideIn:
            trialsToUseRight = rightward & (~sideInTrials)
            trialsToUseLeft = leftward & (~sideInTrials)
        else:
            trialsToUseRight = rightward 
            trialsToUseLeft = leftward 
        trialsEachCond = [trialsToUseLeft,trialsToUseRight] 
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimestamps,movementOnsetTimes,timeRange)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial, movementTimeRange)

        spikeCountEachTrial = spikeCountMat.flatten()
        spikeAvgLeftward = np.mean(spikeCountEachTrial[leftward])
        spikeAvgRightward = np.mean(spikeCountEachTrial[rightward])

        if ((spikeAvgRightward + spikeAvgLeftward) == 0):
            movementModI[indCell] = 0.0
            movementModS[indCell] = 1.0

        else:
            movementModI[indCell] = ((spikeAvgRightward - spikeAvgLeftward)/(spikeAvgRightward + spikeAvgLeftward))  
            movementModS[indCell] = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,movementTimeRange,trialsEachCond)[1]

    return movementModI, movementModS


    

def evaluate_movement_zScore_celldb(cellDb, baselineAlignment='sound', baselineTimeRange=[-0.1,0], movementAlignment='center-out', movementTimeRange=[0,0.3], removeSideIn=True):
    '''
    Analyse 2afc data: compare spike count during movement and baseline, compute z score and p value.
    baselineTimeRange and movementTimeRange should be lists (in seconds, time from center-out).
    '''
    print 'Calculating movement vs baseline z score and p value in time range: ' + str(movementTimeRange)

    movementZscore = np.zeros((len(cellDb),2)) #default value 0
    movementPval = np.ones((len(cellDb), 2)) #default value 1

    for indCell, cell in cellDb.iterrows():
        cellObj = ephyscore.Cell(cell)
        sessiontype = 'behavior'  #2afc behavior
        subject = cell.subject
        date = cell.date
        depth = cell.depth
        tetrode = cell.tetrode 
        cluster = cell.cluster
        #ephysData, bata = cellObj.load(sessiontype)
        sessionInd = cellObj.get_session_inds(sessiontype)[0]
        bdata = cellObj.load_behavior_by_index(sessionInd)
        possibleFreq = np.unique(bdata['targetFrequency'])
        numFreqs = len(possibleFreq)

        try:
            ephysData = cellObj.load_ephys_by_index(sessionInd)
        except ValueError:
            continue

        eventsDict = ephysData['events']
        spikeTimestamps = ephysData['spikeTimes']

        if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
            continue

        soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]
        soundOnsetTimeBehav = bdata['timeTarget']

        # -- Check to see if ephys and behav recordings have same number of trials, remove missing trials from behav file -- #
        # Find missing trials
        missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimes,soundOnsetTimeBehav)
        # Remove missing trials
        bdata.remove_trials(missingTrials)

        if len(soundOnsetTimes) != len(bdata['timeTarget']): #some error not handled by remove missing trials
            continue

        # -- calculate movement selectivity -- #
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left'] 
       
        diffTimes = bdata['timeCenterOut'] - bdata['timeTarget']
        movementOnsetTimes = soundOnsetTimes + diffTimes

        responseTimesEachTrial = bdata['timeSideIn'] - bdata['timeCenterOut'] 
        responseTimesEachTrial[np.isnan(responseTimesEachTrial)] = 0
        sideInTrials = (responseTimesEachTrial <= movementTimeRange[-1])
        
        if removeSideIn:
            trialsToUseRight = rightward & (~sideInTrials)
            trialsToUseLeft = leftward & (~sideInTrials)
        else:
            trialsToUseRight = rightward 
            trialsToUseLeft = leftward 
        trialsEachCond = [trialsToUseLeft,trialsToUseRight] 
        
        evlockFileCOut = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(subject, date, depth, tetrode, cluster, movementAlignment)
        evlockFileCOutPath = os.path.join(ephysDir, STUDY_NAME, evlockFileFolder, evlockFileCOut)
        evlockDataCOut = np.load(evlockFileCOutPath)
        spikeTimesFromEventOnsetCOut = evlockDataCOut['spikeTimesFromEventOnset']
        trialIndexForEachSpikeCOut = evlockDataCOut['trialIndexForEachSpike']
        indexLimitsEachTrialCOut = evlockDataCOut['indexLimitsEachTrial']
        spikeCountMatMovement = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetCOut,indexLimitsEachTrialCOut, movementTimeRange)
        spikeCountEachTrialMovement = spikeCountMatMovement.flatten()
        spikeCountLeftwardMovement = spikeCountEachTrialMovement[leftward]
        spikeCountRightwardMovement = spikeCountEachTrialMovement[rightward]

        evlockFileSound = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(subject, date, depth, tetrode, cluster, baselineAlignment)
        evlockFileSoundPath = os.path.join(ephysDir, STUDY_NAME, evlockFileFolder, evlockFileSound)
        evlockDataSound = np.load(evlockFileSoundPath)
        spikeTimesFromEventOnsetSound = evlockDataSound['spikeTimesFromEventOnset']
        trialIndexForEachSpikeSound = evlockDataSound['trialIndexForEachSpike']
        indexLimitsEachTrialSound = evlockDataSound['indexLimitsEachTrial']
        spikeCountMatBaseline = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetSound,indexLimitsEachTrialSound, baselineTimeRange)
        spikeCountEachTrialBaseline = spikeCountMatBaseline.flatten()
        spikeCountLeftwardBaseline = spikeCountEachTrialBaseline[leftward]
        spikeCountRightwardBaseline = spikeCountEachTrialBaseline[rightward]

        zScore,pValue = stats.ranksums(spikeCountLeftwardBaseline, spikeCountLeftwardMovement)
        movementZscore[indCell,0] = zScore
        movementPval[indCell,0] = pValue

        zScore,pValue = stats.ranksums(spikeCountRightwardBaseline, spikeCountRightwardMovement)
        movementZscore[indCell,1] = zScore
        movementPval[indCell,1] = pValue

    return movementZscore, movementPval



