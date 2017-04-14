from jaratoolbox import celldatabase
from jaratoolbox import settings
import pandas
import subprocess
from jaratest.nick.database import dataloader_v2 as dataloader
#from jaratest.nick.analysis import pinp_report
#reload(pinp_report)
#from jaratest.nick.analysis.pinp_report import *
from numpy import inf
#from jaratest.nick.stats import eventresponse
#from jaratest.nick.stats import am_funcs

animal = 'gosi008'
inforecFullPath = os.path.join(settings.INFOREC_PATH, '{}_inforec.py'.format(animal))
gosi008db = celldatabase.generate_cell_database(inforecFullPath)

#Waveform analysis
allShapeQuality = np.empty(len(gosi008db))
for indCell, cell in gosi008db.iterrows():
    peakAmplitudes = cell['clusterPeakAmplitudes']
    spikeShapeSD = cell['clusterSpikeSD']
    shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    allShapeQuality[indCell] = shapeQuality
allShapeQuality[allShapeQuality==inf]=0
gosi008db['shapeQuality'] = allShapeQuality

# -- Aalyse tuning curve and 2afc data -- #
tuningFreqs = np.empty(len(gosi008db))
tuningZscore = np.empty(len(gosi008db))
tuningPval = np.empty(len(gosi008db))
tuningRespIndex = np.empty(len(gosi008db))
tuningResp = np.empty(len(gosi008db))

2afcFreqs = np.empty(len(gosi008db))
2afcZscore = np.empty(len(gosi008db))
2afcPval = np.empty(len(gosi008db))
2afcRespIndex = np.empty(len(gosi008db))
2afcResp = np.empty(len(gosi008db))
2afcRewModInd = np.empty(len(gosi008db))
2afcRewModSig = np.empty(len(gosi008db))
2afcMovementModInd = np.empty(len(gosi008db))
2afcMovementModSig = np.empty(len(gosi008db))

baseRange = [0, 0.1] #Range of baseline period, in sec
respRange = [0, 0.1] #Range of sound response period, in sec

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
        return (0, 0)
    bData = loader.get_session_behavior(behavFile)
    
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
            tuningFreqs[indCell] = possibleFreq
            tuningZscore[indCell] = np.zeros(numFreqs)
            tuningPval[indCell] = np.ones(numFreqs)
            tuningRespIndex[indCell] = np.zeros(numFreqs)
            tuningResp[indCell] = np.zeros(numFreqs)
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
    tuningFreqs[indCell] = possibleFreq
    tuningZscore[indCell] = zScores
    tuningPval[indCell] = pVals
    tuningRespIndex[indCell] = responseInds
    tuningResp[indCell] = responseEachFreq

gosi008db['tuningFreqs'] = tuningFreqs
gosi008db['tuningZscore'] = tuningZscore
gosi008db['tuningPval'] = tuningPval
gosi008db['tuningRespIndex'] = tuningRespIndex
gosi008db['tuningResp'] = tuningResp


# -- Analyse 2afc data: calculate sound response Z score for each freq, store frequencies presented and corresponding Z scores; calculate reward modulation index; calculate movement direction modulation index -- #
for indCell, cell in gosi008db.iterrows():
    loader = dataloader.DataLoader(cell['subject'])
    sessiontype = '2afc'  #tuningcurve
    session = cell['ephys'][cell['sessiontype'].index(sessiontype)]
    behavFile = cell['behavior'][cell['sessiontype'].index(sessiontype)]
    eventData = loader.get_session_events(session)
    try:
        spikeData = loader.get_session_spikes(session, int(cell['tetrode']), cluster=int(cell['cluster']))
    except AttributeError:
        return (0, 0)
    bData = loader.get_session_behavior(behavFile)

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
        2afcFreqs[indCell] = possibleFreq 
        2afcZscore[indCell] = np.zeros(numFreqs) 
        2afcPval[indCell] = np.ones(numFreqs)
        2afcRespIndex[indCell] = np.zeros(numFreqs) 
        2afcResp[indCell] = np.zeros(numFreqs)  
        2afcRewModInd[indCell] = np.zeros(numFreqs) 
        2afcRewModSig[indCell] = np.ones(numFreqs) 
        2afcMovementModInd[indCell] = np.zeros(numFreqs) 
        2afcMovementModSig[indCell] = np.ones(numFreqs)
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
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
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

    2afcFreqs[indCell] = possibleFreq
    2afcZscore[indCell] = zScores
    2afcPval[indCell] = pVals
    2afcRespIndex[indCell] = responseInds
    2afcResp[indCell] = responseEachFreq










    
#Tuning curve analysis
noiseZscore = np.empty(len(gosi008db))
noisePval = np.empty(len(gosi008db))
baseRange = [-0.2,0]
responseRange = [0, 0.2]
for indCell, cell in gosi008db.iterrows():
    zScore, pVal = eventresponse.event_response_score(cell, 'noiseburst',
                                                      responseRange=responseRange,
                                                      baseRange=baseRange)
    noiseZscore[indCell] = zScore
    noisePval[indCell] = pVal
gosi008db['noiseZscore'] = noiseZscore
gosi008db['noisePval'] = noisePval

#Laser pulse response
pulseZscore = np.empty(len(gosi008db))
pulsePval = np.empty(len(gosi008db))
for indCell, cell in gosi008db.iterrows():
    zScore, pVal = eventresponse.event_response_score(cell, 'laserpulse')
    pulseZscore[indCell] = zScore
    pulsePval[indCell] = pVal
gosi008db['pulseZscore'] = pulseZscore
gosi008db['pulsePval'] = pulsePval

#Laser train response
trainRatio = np.empty(len(gosi008db))
for indCell, cell in gosi008db.iterrows():
    ratio = eventresponse.train_response_ratio(cell, 'lasertrain')
    trainRatio[indCell] = ratio
gosi008db['trainRatio'] = trainRatio

#AM stats
amRval = np.empty(len(gosi008db))
highestSync = np.empty(len(gosi008db))
for indCell, cell in gosi008db.iterrows():
    r_val = am_funcs.am_dependence(cell)
    amRval[indCell] = r_val
    hs = am_funcs.highest_significant_sync(cell)
    highestSync[indCell] = hs
gosi008db['amRval'] = amRval
gosi008db['highestSync'] = highestSync

#Save the database
gosi008db.to_hdf('/home/nick/data/database/gosi008/gosi008_database.h5', 'database')

#Query the database and make reports
soundResponsive = gosi008db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')



#Plot reports
# fig_path = '/home/nick/data/database/gosi008/reports_isi_shape_laser_train/'
# for indCell, cell in result.iterrows():
#     plot_pinp_report(cell, fig_path)

#Laser pulse response
# pulseZscore = np.empty(len(gosi008db))
# pulsePval = np.empty(len(gosi008db))
# for indCell, cell in gosi008db.iterrows():
#     loader = dataloader.DataLoader(cell['subject'])
#     pulseSession = cell['ephys'][cell['sessiontype'].index('laserpulse')]
#     eventData = loader.get_session_events(pulseSession)
#     try:
#         spikeData = loader.get_session_spikes(pulseSession, int(cell['tetrode']), cluster=int(cell['cluster']))
#     except AttributeError:
#         pulseZscore[indCell] = 0
#         pulsePval[indCell] = 0
#         continue
#     eventOnsetTimes = loader.get_event_onset_times(eventData)
#     timeRange = [-0.1, 0.1]
#     (spikeTimesFromEventOnset,
#      trialIndexForEachSpike,
#      indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
#                                                                    eventOnsetTimes,
#                                                                    timeRange)
#     baseRange = [-0.1,0]
#     responseRange = [0, 0.1]
#     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange)
#     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
#     [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
#     pulseZscore[indCell] = zScore
#     pulsePval[indCell] = pVal
# gosi008db['pulseZscore'] = pulseZscore
# gosi008db['pulsePval'] = pulsePval

# loader = dataloader.DataLoader(cell['subject'])
# noiseSession = cell['ephys'][cell['sessiontype'].index('noiseburst')]
# eventData = loader.get_session_events(noiseSession)
# try:
#     spikeData = loader.get_session_spikes(noiseSession, int(cell['tetrode']), cluster=int(cell['cluster']))
# except AttributeError:
#     noiseZscore[indCell] = 0
#     noisePval[indCell] = 0
#     continue
# eventOnsetTimes = loader.get_event_onset_times(eventData)
# timeRange = [-0.2, 0.2]
# (spikeTimesFromEventOnset,
#  trialIndexForEachSpike,
#  indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
#                                                                eventOnsetTimes,
#                                                                timeRange)
# baseRange = [-0.2,0]
# responseRange = [0, 0.2]
# nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange)
# nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
# [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
# noiseZscore[indCell] = zScore
# noisePval[indCell] = pVal

#Old laser train response
    # loader = dataloader.DataLoader(cell['subject'])
    # trainSession = cell['ephys'][cell['sessiontype'].index('lasertrain')]
    # eventData = loader.get_session_events(trainSession)
    # try:
    #     spikeData = loader.get_session_spikes(trainSession, int(cell['tetrode']), cluster=int(cell['cluster']))
    # except AttributeError:
    #     trainRatio[indCell] = 0
    #     continue
    # eventOnsetTimes = loader.get_event_onset_times(eventData)
    # eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.1)
    # timeRange = [-0.1, 1]
    # (spikeTimesFromEventOnset,
    #  trialIndexForEachSpike,
    #  indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
    #                                                                eventOnsetTimes,
    #                                                                timeRange)
    # # plt.clf()
    # # plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
    # # plt.show()
    # # plt.waitforbuttonpress()
    # baseRange = [0, 0.05]
    # responseRange = [0.2, 0.25]
    # avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange).mean()
    # avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange).mean()
    # ratio = avgSpikesResp/avgSpikesBase
