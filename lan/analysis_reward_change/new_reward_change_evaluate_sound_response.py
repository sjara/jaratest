'''
Updated to use new celldb.
This script take a cell database for reward-change mice that includes only the good quality cells that passed shape quality, isi, consistent firing, in target area check. The database includes basic information such as subject, date, behavior sessions, ephys sessions, sessiontype, tetrode, cluster, depth, brainarea recorded from, inforecPath etc. Also includes measurements calculated while clustering: 'clusterPeakAmplitudes', 'clusterPeakTimes', 'clusterSpikeSD', 'clusterSpikeShape', 'isiViolations', 'nSpikes'.
Measurements calculated to reflect sound responsiveness from this script: 'tuningFreqs', 'tuningZscore', 'tuningPval', 'tuningRespIndex', 'tuningResp', 'behavFreqs', 'behavZscore', 'behavPval', 'behavRespIndex', 'behavResp'.
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

baseRange = [-0.1, 0] #Range of baseline period, in sec
respRange = [0, 0.1] #Range of sound response period, in sec
timeRange = [-0.5,1]
movementTimeRange = [0.05, 0.15] 
#soundTriggerChannel = 0
soundChannelType = 'stim'

gosidb = pd.read_hdf(databaseFullPath, key=key)

# -- Analyse tuning curve data: calculate sound response Z score for each freq, store frequencies presented and corresponding Z scores -- #
if not ('tuningZscore' in gosidb.columns):
    print 'Calculating sound response Z scores for tuning curve'
    # -- Aalyse tuning curve and 2afc data -- #
    tuningDict = {'tuningFreqs':[],
                  'tuningZscore':[],
                  'tuningPval':[],
                  'tuningRespIndex':[],
                  'tuningResp':[]}

    for indCell, cell in gosidb.iterrows():
        cellObj = ephyscore.Cell(cell)
        sessiontype = 'tc'  #tuningcurve
        #ephysData, bata = cellObj.load(sessiontype)
        sessionInd = cellObj.get_session_inds(sessiontype)[0]
        bdata = cellObj.load_behavior_by_index(sessionInd)
        possibleFreq = np.unique(bdata['currentFreq'])
        numFreqs = len(possibleFreq)

        try:
            ephysData = cellObj.load_ephys_by_index(sessionInd)
        except ValueError:
            spikeData = (0, 0)
            tuningDict['tuningFreqs'].append(possibleFreq)
            tuningDict['tuningZscore'].append(np.zeros(numFreqs))
            tuningDict['tuningPval'].append(np.ones(numFreqs))
            tuningDict['tuningRespIndex'].append(np.zeros(numFreqs))
            tuningDict['tuningResp'].append(np.zeros(numFreqs))
            continue
            
        eventsDict = ephysData['events']
        spikeTimestamps = ephysData['spikeTimes']

        if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
            tuningDict['tuningFreqs'].append(possibleFreq)
            tuningDict['tuningZscore'].append(np.zeros(numFreqs))
            tuningDict['tuningPval'].append(np.ones(numFreqs))
            tuningDict['tuningRespIndex'].append(np.zeros(numFreqs))
            tuningDict['tuningResp'].append(np.zeros(numFreqs))
            continue
        
        soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]
        
        if len(soundOnsetTimes) != len(bdata['currentFreq']):
            # This is a hack for when ephys is one trial longer than behavior
            if len(soundOnsetTimes) == len(bdata['currentFreq'])+1:
                soundOnsetTimes = soundOnsetTimes[:-1]
            else:
                tuningDict['tuningFreqs'].append(possibleFreq)
                tuningDict['tuningZscore'].append(np.zeros(numFreqs))
                tuningDict['tuningPval'].append(np.ones(numFreqs))
                tuningDict['tuningRespIndex'].append(np.zeros(numFreqs))
                tuningDict['tuningResp'].append(np.zeros(numFreqs))

                continue #skip all subsequent analysis if the two files did not recorded same number of trials

        # -- Calculate Z score of sound response for each frequency -- #
        zScores = []
        pVals = []
        responseEachFreq = []
        responseInds = []
        for freq in possibleFreq:
            oneFreqTrials = bdata['currentFreq'] == freq
            oneFreqSoundOnsetTimes = soundOnsetTimes[oneFreqTrials]
            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimestamps,oneFreqSoundOnsetTimes,timeRange)
            # Generate the spkCountMatrix where each row is one trial, each column is a time bin to count spikes in, in this case only one time bin
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange) 
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,respRange)
            print nspkBase.shape, nspkResp.shape

            # Calculate response index (S-B)/(S+B) where S and B are ave response during the sound window and baseline window, respectively
            responseIndex = (np.mean(nspkResp) - np.mean(nspkBase))/(np.mean(nspkResp) + np.mean(nspkBase))
            responseInds.append(responseIndex)
            responseEachFreq.append(nspkResp) #Store response to each stim frequency (all trials) as a list of lists
            print 'ave firing rate for baseline and sound periods are', np.mean(nspkBase), np.mean(nspkResp), 'response index is', responseIndex

            # Calculate statistic using ranksums test
            [zStat,pValue] = stats.ranksums(nspkResp,nspkBase)
            zScores.append(zStat)
            pVals.append(pValue)


        tuningDict['tuningFreqs'].append(possibleFreq)
        tuningDict['tuningZscore'].append(zScores)
        tuningDict['tuningPval'].append(pVals)
        tuningDict['tuningRespIndex'].append(responseInds)
        tuningDict['tuningResp'].append(responseEachFreq)

    gosidb['tuningFreqs'] = tuningDict['tuningFreqs']
    gosidb['tuningZscore'] = tuningDict['tuningZscore'] #tuningZscore
    gosidb['tuningPval'] = tuningDict['tuningPval'] #tuningPval
    gosidb['tuningRespIndex'] = tuningDict['tuningRespIndex'] #tuningRespIndex
    gosidb['tuningResp'] = tuningDict['tuningResp'] #tuningResp
    gosidb.to_hdf(databaseFullPath, key=key)

# -- Analyse 2afc data: calculate sound response Z score for each freq, store frequencies presented and corresponding Z scores -- #
if not ('behavZscore' in gosidb.columns):
    print 'Calculating sound response Z scores for 2afc session'
    
    behavDict = {'behavFreqs':[], 
                 'behavZscore':[],
                 'behavPval':[],
                 'behavRespIndex':[],
                 'behavResp':[]}
    #movementModI = np.zeros(len(gosidb)) #default value 0
    #movementModS = np.ones(len(gosidb)) #default value 1

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
            spikeData = (0, 0)
            behavDict['behavFreqs'].append(possibleFreq)
            behavDict['behavZscore'].append(np.zeros(numFreqs))
            behavDict['behavPval'].append(np.ones(numFreqs))
            behavDict['behavRespIndex'].append(np.zeros(numFreqs))
            behavDict['behavResp'].append(np.zeros(numFreqs))
            continue
            
        eventsDict = ephysData['events']
        spikeTimestamps = ephysData['spikeTimes']

        if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
            behavDict['behavFreqs'].append(possibleFreq)
            behavDict['behavZscore'].append(np.zeros(numFreqs))
            behavDict['behavPval'].append(np.ones(numFreqs))
            behavDict['behavRespIndex'].append(np.zeros(numFreqs))
            behavDict['behavResp'].append(np.zeros(numFreqs))
            continue

        soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]
        soundOnsetTimeBehav = bdata['timeTarget']

        # -- Check to see if ephys and behav recordings have same number of trials, remove missing trials from behav file -- #
        # Find missing trials
        missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimes,soundOnsetTimeBehav)
        # Remove missing trials
        bdata.remove_trials(missingTrials)

        if len(soundOnsetTimes) != len(bdata['timeTarget']): #some error not handled by remove missing trials
            behavDict['behavFreqs'].append(possibleFreq)
            behavDict['behavZscore'].append(np.zeros(numFreqs))
            behavDict['behavPval'].append(np.ones(numFreqs))
            behavDict['behavRespIndex'].append(np.zeros(numFreqs))
            behavDict['behavResp'].append(np.zeros(numFreqs))
            continue

        # -- Calculate Z score of sound response for each frequency -- #
        zScores = []
        pVals = []
        responseEachFreq = []
        responseInds = []

        for freq in possibleFreq:
            # -- Only use valid trials of one frequency to estimate response index -- #
            oneFreqTrials = (bdata['targetFrequency'] == freq) & bdata['valid'].astype('bool')
            oneFreqSoundOnsetTimes = soundOnsetTimes[oneFreqTrials]
            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimestamps,oneFreqSoundOnsetTimes,timeRange)
            # Generate the spkCountMatrix where each row is one trial, each column is a time bin to count spikes in, in this case one time bin for baseline and one time bin for sound period
            #pdb.set_trace()
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange) 
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,respRange)
            print nspkBase.shape, nspkResp.shape

            # Calculate response index (S-B)/(S+B) where S and B are ave response during the sound window and baseline window, respectively
            responseIndex = (np.mean(nspkResp) - np.mean(nspkBase))/(np.mean(nspkResp) + np.mean(nspkBase))
            responseInds.append(responseIndex)
            responseEachFreq.append(nspkResp) #Store response to each stim frequency (all trials) in a list
            print 'ave firing rate for baseline and sound periods are', np.mean(nspkBase), np.mean(nspkResp), 'response index is', responseIndex

            # Calculate statistic using ranksums test 
            zStat,pValue = stats.ranksums(nspkResp, nspkBase)
            print zStat, pValue
            zScores.append(zStat)
            pVals.append(pValue)

        behavDict['behavFreqs'].append(possibleFreq)
        behavDict['behavZscore'].append(zScores)
        behavDict['behavPval'].append(pVals)
        behavDict['behavRespIndex'].append(responseInds)
        behavDict['behavResp'].append(responseEachFreq)

        '''
        # -- calculate movement selectivity -- #
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left'] 
        trialsToUseRight = rightward
        trialsToUseLeft = leftward

        diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
        movementOnsetTimes = soundOnsetTimes+diffTimes

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
        '''

    gosidb['behavFreqs'] =  behavDict['behavFreqs']
    gosidb['behavZscore'] = behavDict['behavZscore']
    gosidb['behavPval'] = behavDict['behavPval']
    gosidb['behavRespIndex'] = behavDict['behavRespIndex']
    gosidb['behavResp'] = behavDict['behavResp']
    
    #gosidb['movementModI'] = movementModI
    #gosidb['movementModS'] = movementModS
    gosidb.to_hdf(databaseFullPath, key=key)




