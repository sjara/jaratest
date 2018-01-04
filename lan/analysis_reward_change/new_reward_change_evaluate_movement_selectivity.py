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

animal = 'adap067'

databaseFullPath = os.path.join(settings.DATABASE_PATH, 'new_celldb', '{}_database.h5'.format(animal))
key = 'reward_change'

timeRange = [-0.5,1]
movementTimeRangeList = [[0.05, 0.15], [0.05, 0.25]] 
#soundTriggerChannel = 0
soundChannelType = 'stim'

gosidb = pd.read_hdf(databaseFullPath, key=key)

# -- Analyse 2afc data: calculate movement selectivity index and significance -- #
for movementTimeRange in movementTimeRangeList:
    if not ('movementModI_{}'.format(movementTimeRange) in gosidb.columns):
        print 'Calculating movement selectivity index for 2afc session in time range: '+movementTimeRange

        movementModI = np.zeros(len(gosidb)) #default value 0
        movementModS = np.ones(len(gosidb)) #default value 1

        for indCell, cell in gosidb.iterrows():
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

            # -- Calculate Z score of sound response for each frequency -- #
            zScores = []
            pVals = []
            responseEachFreq = []
            responseInds = []


            # -- calculate movement selectivity -- #
            rightward = bdata['choice']==bdata.labels['choice']['right']
            leftward = bdata['choice']==bdata.labels['choice']['left'] 
            trialsToUseRight = rightward
            trialsToUseLeft = leftward

            diffTimes = bdata['timeCenterOut'] - bdata['timeTarget']
            movementOnsetTimes = soundOnsetTimes + diffTimes

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


        gosidb['movementModI_{}'.format(movementTimeRange)] = movementModI
        gosidb['movementModS_{}'.format(movementTimeRange)] = movementModS
        gosidb.to_hdf(databaseFullPath, key=key)




