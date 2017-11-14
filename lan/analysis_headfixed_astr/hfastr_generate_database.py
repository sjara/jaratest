'''
This script generates a cells database for mice recorded from the left and right auditory striatum in the reward change paradigm. The database includes basic information such as subject, date, behavior sessions, ephys sessions, sessiontype, tetrode, cluster, depth, brainarea recorded from, inforecPath etc. Also includes measurements calculated while clustering: 'clusterPeakAmplitudes', 'clusterPeakTimes', 'clusterSpikeSD', 'clusterSpikeShape', 'isiViolations', 'nSpikes'.
Measurements calculated to reflect sound responsiveness from this script: 'tuningFreqs', 'tuningZscore', 'tuningPval', 'tuningRespIndex', 'tuningResp'.
The script includes code to cluster inforec file, which can be commented out once inforec has been fully clustered. 
Lan 2017-04-30
'''

from jaratoolbox import celldatabase
from jaratoolbox import settings
reload(settings)
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import os
import pandas as pd
import subprocess
from jaratest.nick.database import dataloader_v2 as dataloader
import numpy as np
from scipy import stats
import imp

animal = 'adap041'
inforecFullPath = os.path.join(settings.INFOREC_PATH, '{}_inforec.py'.format(animal))
CASE = 3

if CASE == 1:
    # -- Cluster inforec and store stats, if have not already done so -- #
    ci = spikesorting.ClusterInforec(inforecFullPath)
    ci.cluster_all_experiments(maxClusters=6, maxPossibleClusters=6, recluster=False)
    ##############################################################

if CASE == 2:
    databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    key = 'head_fixed'

    baseRange = [-0.1, 0] #Range of baseline period, in sec
    respRange = [0, 0.1] #Range of sound response period, in sec
    timeRange = [-0.5,1]
    movementTimeRange = [0.05, 0.15] 
    soundTriggerChannel = 0


    celldb = celldatabase.generate_cell_database(inforecFullPath)
    celldb['animalName'] = animal
    celldb.to_hdf(databaseFullPath, key=key)


    celldb = pd.read_hdf(databaseFullPath, key=key)

    if not ('shapeQaulity' in celldb.columns):
        #Waveform analysis
        allShapeQuality = np.empty(len(celldb))
        for indCell, cell in celldb.iterrows():
            peakAmplitudes = cell['clusterPeakAmplitudes']
            spikeShapeSD = cell['clusterSpikeSD']
            shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
            allShapeQuality[indCell] = shapeQuality
        allShapeQuality[allShapeQuality==np.inf]=0
        celldb['shapeQuality'] = allShapeQuality
        celldb.to_hdf(databaseFullPath, key=key)

    # -- Calculate rank_sum test Z score and p Val at maximum intensity of sound for all frequencies -- #
    #if not ('tuningZscore' in celldb.columns):
    tuningDict = {'tuningFreqs':[],
                  'ZscoreEachIntensity':[],
                  'PvalEachIntensity':[],
                  'tuningZscoreEachIntEachFreq':[],
                  'tuningPvalEachIntEachFreq':[],
                  'tuningRespIndex':[],
                  'tuningResp':[],
                  'tuningWeightedBFEachIntensity':[]}

    for indCell, cell in celldb.iterrows():
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
            tuningDict['ZscoreEachIntensity'].append(np.zeros(numIntensities))
            tuningDict['PvalEachIntensity'].append(np.ones(numIntensities))
            tuningDict['tuningFreqs'].append(possibleFreq) 
            tuningDict['tuningZscoreEachIntEachFreq'].append(np.zeros((numIntensities, numFreqs)))
            tuningDict['tuningPvalEachIntEachFreq'].append(np.ones((numIntensities, numFreqs)))
            tuningDict['tuningRespIndex'].append(np.zeros((numIntensities, numFreqs)))
            tuningDict['tuningResp'].append(np.zeros((numIntensities, numFreqs)))
            tuningDict['tuningWeightedBFEachIntensity'].append(np.repeat(np.nan, numIntensities))
            continue

        spikeTimestamps = spikeData.timestamps
        if spikeTimestamps.ndim == 0: #There is only one spike, ! spikesanalysis.eventlocked_spiketimes cannot handle only one spike !
            tuningDict['ZscoreEachIntensity'].append(np.zeros(numIntensities))
            tuningDict['PvalEachIntensity'].append(np.ones(numIntensities))
            tuningDict['tuningFreqs'].append(possibleFreq) 
            tuningDict['tuningZscoreEachIntEachFreq'].append(np.zeros((numIntensities, numFreqs)))
            tuningDict['tuningPvalEachIntEachFreq'].append(np.ones((numIntensities, numFreqs)))
            tuningDict['tuningRespIndex'].append(np.zeros((numIntensities, numFreqs)))
            tuningDict['tuningResp'].append(np.zeros((numIntensities, numFreqs)))
            tuningDict['tuningWeightedBFEachIntensity'].append(np.repeat(np.nan, numIntensities))
            continue

        bdata = loader.get_session_behavior(behavFile)

        possibleFreq = np.unique(bdata['currentFreq'])
        numFreqs = len(possibleFreq)

        possibleIntensity = np.unique(bdata['currentIntensity'])
        #maxIntensity = np.max(possibleIntensity)
        numIntensities = len(possibleIntensity)

        eventOnsetTimes=np.array(eventData.timestamps)
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
        if len(soundOnsetTimes) != len(bdata['currentFreq']):
            # This is a hack for when ephys is one trial longer than behavior
            if len(soundOnsetTimes) == len(bdata['currentFreq'])+1:
                soundOnsetTimes = soundOnsetTimes[:-1]
            else:
                tuningDict['ZscoreEachIntensity'].append(np.zeros(numIntensities))
                tuningDict['PvalEachIntensity'].append(np.ones(numIntensities))
                tuningDict['tuningFreqs'].append(possibleFreq) 
                tuningDict['tuningZscoreEachIntEachFreq'].append(np.zeros((numIntensities, numFreqs)))
                tuningDict['tuningPvalEachIntEachFreq'].append(np.ones((numIntensities, numFreqs)))
                tuningDict['tuningRespIndex'].append(np.zeros((numIntensities, numFreqs)))
                tuningDict['tuningResp'].append(np.zeros((numIntensities, numFreqs)))

                tuningDict['tuningWeightedBFEachIntensity'].append(np.repeat(np.nan, numIntensities))
                continue #skip all subsequent analysis if the two files did not recorded same number of trials

        # -- Calculate normalized response for each frequency at max intensity

        # -- TO DO Evaluate response of different freqs at each intensity -- #
        zStatAllFreqEachIntensity = []
        pValueAllFreqEachIntensity = []
        weightedBestFreqEachIntensity = []
        responseEachFreqEachIntensity = np.empty((numIntensities, numFreqs))
        responseIndEachFreqEachIntensity = np.empty((numIntensities, numFreqs))
        zScoreEachFreqEachIntensity = np.empty((numIntensities, numFreqs))
        pValEachFreqEachIntensity = np.empty((numIntensities, numFreqs))
        for ind,intensity in enumerate(possibleIntensity):
            responseEachFreq = []
            responseIndEachFreq = []
            ZscoreEachFreq = []
            pValEachFreq = []
            # -- Calculate Z score of sound response for all frequencies at each intensity -- #
            thisIntensityTrials = bdata['currentIntensity'] == intensity
            thisIntensitySoundOnsetTimes = soundOnsetTimes[thisIntensityTrials]
            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,thisIntensitySoundOnsetTimes,timeRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange) 
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,respRange)
            # Calculate statistic using ranksums test
            [zStatAllFreq,pValueAllFreq] = stats.ranksums(nspkResp,nspkBase)
            zStatAllFreqEachIntensity.append(zStatAllFreq)
            pValueAllFreqEachIntensity.append(pValueAllFreq)

            for freq in possibleFreq:
                oneFreqTrials = (bdata['currentFreq'] == freq) & thisIntensityTrials
                oneFreqSoundOnsetTimes = soundOnsetTimes[oneFreqTrials]
                (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,oneFreqSoundOnsetTimes,timeRange)
                # Generate the spkCountMatrix where each row is one trial, each column is a time bin to count spikes in, in this case only one time bin
                nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange) 
                nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,respRange)
                [zStat,pValue] = stats.ranksums(nspkResp,nspkBase)
                #print nspkBase.shape, nspkResp.shape
                ZscoreEachFreq.append(zStat)
                pValEachFreq.append(pValue)

                # Calculate response index (S-B)/(S+B) where S and B are ave response during the sound window and baseline window, respectively
                responseIndex = (np.mean(nspkResp) - np.mean(nspkBase))/(np.mean(nspkResp) + np.mean(nspkBase))
                responseIndEachFreq.append(responseIndex)
                responseEachFreq.append(np.mean(nspkResp)) #Store mean response to each stim frequency as a list
                print 'ave firing rate for baseline and sound periods are', np.mean(nspkBase), np.mean(nspkResp), 'response index is', responseIndex

            responseEachFreqEachIntensity[ind,:] = responseEachFreq
            responseIndEachFreqEachIntensity[ind,:] = responseIndEachFreq
            zScoreEachFreqEachIntensity[ind,:] = ZscoreEachFreq
            pValEachFreqEachIntensity[ind,:] = pValEachFreq

            # -- Calculate response weighted 'best frequency' for each intensity-- #
            # Normalize response to each frequency by the maximum response
            responseEachFreq = np.array(responseEachFreq, dtype=float)
            maxResp = np.max(responseEachFreq).astype(float)
            normRespEachFreq = responseEachFreq / maxResp
            base2Freq = np.array(np.log2(possibleFreq)) #convert to log scale
            sumNormRespByFreq = np.sum(normRespEachFreq * base2Freq) #sum of normalized response at each frequency times that frequency
            weightedBestFreqExponent = sumNormRespByFreq / np.sum(normRespEachFreq)
            weightedBestFreq = 2 ** weightedBestFreqExponent #convert back to linear scale
            weightedBestFreqEachIntensity.append(weightedBestFreq)
            print 'weighted best freq is', weightedBestFreq

        # -- Store results -- #
        tuningDict['ZscoreEachIntensity'].append(np.array(zStatAllFreqEachIntensity))
        tuningDict['PvalEachIntensity'].append(np.array(pValueAllFreqEachIntensity))
        tuningDict['tuningZscoreEachIntEachFreq'].append(np.array(zScoreEachFreqEachIntensity))
        tuningDict['tuningPvalEachIntEachFreq'].append(np.array(pValEachFreqEachIntensity))
        tuningDict['tuningRespIndex'].append(np.array(responseIndEachFreqEachIntensity))
        tuningDict['tuningResp'].append(np.array(responseEachFreqEachIntensity))
        tuningDict['tuningWeightedBFEachIntensity'].append(np.array(weightedBestFreqEachIntensity))
        tuningDict['tuningFreqs'].append(np.array(possibleFreq))

    celldb['ZscoreEachIntensity'] = tuningDict['ZscoreEachIntensity']
    celldb['PvalEachIntensity'] = tuningDict['PvalEachIntensity']
    celldb['tuningFreqs'] = tuningDict['tuningFreqs']
    celldb['tuningZscoreEachIntEachFreq'] = tuningDict['tuningZscoreEachIntEachFreq'] #tuningZscore by frequency and intensity
    celldb['tuningPvalEachIntEachFreq'] = tuningDict['tuningPvalEachIntEachFreq'] #tuningPval
    celldb['tuningRespIndex'] = tuningDict['tuningRespIndex'] #tuningRespIndex
    celldb['tuningResp'] = tuningDict['tuningResp'] #tuningResp
    celldb['tuningWeightedBFEachIntensity'] = tuningDict['tuningWeightedBFEachIntensity']
    celldb.to_hdf(databaseFullPath, key=key)

if CASE == 3:
    # -- Updated celldb 'info' param of each site to indicate the medial-lateral location of each tetrode -- #
    databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    key = 'head_fixed'
    celldb = pd.read_hdf(databaseFullPath, key=key)
    # Load inforec to read the updated 'info'
    inforec = imp.load_source('module.name', inforecFullPath)
    # Update celldb info column
    for experiment in inforec.experiments:
        for site in experiment.sites:
            infoDictThisSite = site.cluster_info()
            cellsThisSite = (celldb['date'] == infoDictThisSite['date'])&(celldb['depth'] == infoDictThisSite['depth'])
            celldb.loc[cellsThisSite, 'info'] =  [infoDictThisSite['info']]*sum(cellsThisSite)
    
    # Parse info column to generate a 'astrRegion' param for each cell based on the tetrode they're on
    medialTTs = celldb['info'].apply(lambda x: [string.split(':')[1]  for string in x if string.startswith('medial:')][0])
    lateralTTs = celldb['info'].apply(lambda x: [string.split(':')[1] for string in x if string.startswith('lateral:')][0])
    astrRegion = np.empty(len(celldb),dtype = 'object')
    for ind, cell in celldb.iterrows():
        if str(int(cell.tetrode)) in medialTTs.iloc[ind]:
            astrRegion[ind] = 'medial'
        elif str(int(cell.tetrode)) in lateralTTs.iloc[ind]:
            astrRegion[ind] = 'lateral'
        else:
            astrRegion[ind] = 'undetermined'
    celldb['astrRegion'] = astrRegion
    celldb.to_hdf(databaseFullPath, key=key)
