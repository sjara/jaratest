from jaratoolbox import celldatabase
from jaratoolbox import settings
reload(settings)
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import os
import pandas as pd
import subprocess
from jaratest.nick.database import dataloader_v2 as dataloader
import numpy as np
from scipy import stats

animal = 'gosi008'
inforecFullPath = os.path.join(settings.INFOREC_PATH, '{}_inforec.py'.format(animal))
databaseFullPath = os.path.join(settings.DATABASE_PATH, animal, '{}_database.h5'.format(animal))
key = 'reward_change'

baseRange = [-0.1, 0] #Range of baseline period, in sec
respRange = [0, 0.1] #Range of sound response period, in sec
timeRange = [-0.5,1]
movementTimeRange = [0.05, 0.15] 
soundTriggerChannel = 0


if not os.path.isfile(databaseFullPath):
    gosi008db = celldatabase.generate_cell_database(inforecFullPath)
    gosi008db['animalName'] = animal
    gosi008db.to_hdf(databaseFullPath, key=key)

else:
    gosi008db = pd.read_hdf(databaseFullPath, key=key)

    if not ('shapeQaulity' in gosi008db.columns):
        #Waveform analysis
        allShapeQuality = np.empty(len(gosi008db))
        for indCell, cell in gosi008db.iterrows():
            peakAmplitudes = cell['clusterPeakAmplitudes']
            spikeShapeSD = cell['clusterSpikeSD']
            shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
            allShapeQuality[indCell] = shapeQuality
        allShapeQuality[allShapeQuality==np.inf]=0
        gosi008db['shapeQuality'] = allShapeQuality
        gosi008db.to_hdf(databaseFullPath, key=key)

    if not ('tuningZscore' in gosi008db.columns):
        # -- Aalyse tuning curve and 2afc data -- #
        tuningDict = {'tuningFreqs':[],
                      'tuningZscore':[],
                      'tuningPval':[],
                      'tuningRespIndex':[],
                      'tuningResp':[]}
        '''
        tuningFreqs = np.empty(len(gosi008db))
        tuningZscore = np.empty(len(gosi008db))
        tuningPval = np.empty(len(gosi008db))
        tuningRespIndex = np.empty(len(gosi008db))
        tuningResp = np.empty(len(gosi008db))
        '''
        
        for indCell, cell in gosi008db.iterrows():
            loader = dataloader.DataLoader(cell['subject'])

            # -- Analyse tuning curve data: calculate sound response Z score for each freq, store frequencies presented and corresponding Z scores -- #
            sessiontype = 'tc'  #tuningcurve
            session = cell['ephys'][cell['sessiontype'].index(sessiontype)]
            behavFile = cell['behavior'][cell['sessiontype'].index(sessiontype)]
            eventData = loader.get_session_events(session)
            try:
                spikeData = loader.get_session_spikes(session, int(cell['tetrode']), cluster=int(cell['cluster']))
            except AttributeError:
                spikeData = (0, 0)
                tuningDict['tuningFreqs'].append(possibleFreq)
                tuningDict['tuningZscore'].append(np.zeros(numFreqs))
                tuningDict['tuningPval'].append(np.ones(numFreqs))
                tuningDict['tuningRespIndex'].append(np.zeros(numFreqs))
                tuningDict['tuningResp'].append(np.zeros(numFreqs))
                continue

            spikeTimestamps = spikeData.timestamps
            if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
                tuningDict['tuningFreqs'].append(possibleFreq)
                tuningDict['tuningZscore'].append(np.zeros(numFreqs))
                tuningDict['tuningPval'].append(np.ones(numFreqs))
                tuningDict['tuningRespIndex'].append(np.zeros(numFreqs))
                tuningDict['tuningResp'].append(np.zeros(numFreqs))
                continue

            bdata = loader.get_session_behavior(behavFile)

            possibleFreq = np.unique(bdata['currentFreq'])
            numFreqs = len(possibleFreq)

            eventOnsetTimes=np.array(eventData.timestamps)
            soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
            soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
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
                    '''
                    tuningFreqs[indCell] = possibleFreq
                    tuningZscore[indCell] = np.zeros(numFreqs)
                    tuningPval[indCell] = np.ones(numFreqs)
                    tuningRespIndex[indCell] = np.zeros(numFreqs)
                    tuningResp[indCell] = np.zeros(numFreqs)
                    '''
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

            '''
            tuningFreqs[indCell] = possibleFreq
            tuningZscore[indCell] = zScores
            tuningPval[indCell] = pVals
            tuningRespIndex[indCell] = responseInds
            tuningResp[indCell] = responseEachFreq
            '''
            tuningDict['tuningFreqs'].append(possibleFreq)
            tuningDict['tuningZscore'].append(zScores)
            tuningDict['tuningPval'].append(pVals)
            tuningDict['tuningRespIndex'].append(responseInds)
            tuningDict['tuningResp'].append(responseEachFreq)

        gosi008db['tuningFreqs'] = tuningDict['tuningFreqs']
        gosi008db['tuningZscore'] = tuningDict['tuningZscore'] #tuningZscore
        gosi008db['tuningPval'] = tuningDict['tuningPval'] #tuningPval
        gosi008db['tuningRespIndex'] = tuningDict['tuningRespIndex'] #tuningRespIndex
        gosi008db['tuningResp'] = tuningDict['tuningResp'] #tuningResp
        gosi008db.to_hdf(databaseFullPath, key=key)

    if not ('behavZscore' in gosi008db.columns):
        # -- Analyse 2afc data: calculate sound response Z score for each freq, store frequencies presented and corresponding Z scores -- #
        #gosi008db = pd.read_hdf(databaseFullPath)
        behavDict = {'behavFreqs':[], 
                     'behavZscore':[],
                     'behavPval':[],
                     'behavRespIndex':[],
                     'behavResp':[]}
        movementModI = np.zeros(len(gosi008db)) #default value 0
        movementModS = np.ones(len(gosi008db)) #default value 1
       
        for indCell, cell in gosi008db.iterrows():
            loader = dataloader.DataLoader(cell['subject'])
            sessiontype = 'behavior'  #2afc behavior
            session = cell['ephys'][cell['sessiontype'].index(sessiontype)]
            behavFile = cell['behavior'][cell['sessiontype'].index(sessiontype)]
            eventData = loader.get_session_events(session)
            try:
                spikeData = loader.get_session_spikes(session, int(cell['tetrode']), cluster=int(cell['cluster']))
            except AttributeError:
                spikeData = (0, 0)
                behavDict['behavFreqs'].append(possibleFreq)
                behavDict['behavZscore'].append(np.zeros(numFreqs))
                behavDict['behavPval'].append(np.ones(numFreqs))
                behavDict['behavRespIndex'].append(np.zeros(numFreqs))
                behavDict['behavResp'].append(np.zeros(numFreqs))
                continue

            spikeTimestamps = spikeData.timestamps
            if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
                behavDict['behavFreqs'].append(possibleFreq)
                behavDict['behavZscore'].append(np.zeros(numFreqs))
                behavDict['behavPval'].append(np.ones(numFreqs))
                behavDict['behavRespIndex'].append(np.zeros(numFreqs))
                behavDict['behavResp'].append(np.zeros(numFreqs))
                continue

            bdata = loader.get_session_behavior(behavFile)

            eventOnsetTimes=np.array(eventData.timestamps)
            soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
            soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
            soundOnsetTimeBehav = bdata['timeTarget']

            possibleFreq = np.unique(bdata['targetFrequency'])
            numFreqs = len(possibleFreq)

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
                '''
                rewardModI_sound = np.zeros(numFreqs)
                rewardModS_sound = np.ones(numFreqs)
                rewardModI_movement = np.zeros(numFreqs)
                rewardModS_movement = np.ones(numFreqs) 
                rewardModI_reward = np.zeros(numFreqs)
                rewardModS_reward = np.ones(numFreqs) 
                '''
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

        gosi008db['behavFreqs'] =  behavDict['behavFreqs']
        gosi008db['behavZscore'] = behavDict['behavZscore']
        gosi008db['behavPval'] = behavDict['behavPval']
        gosi008db['behavRespIndex'] = behavDict['behavRespIndex']
        gosi008db['behavResp'] = behavDict['behavResp']
        gosi008db['movementModI'] = movementModI
        gosi008db['movementModS'] = movementModS
        gosi008db.to_hdf(databaseFullPath, key=key)





