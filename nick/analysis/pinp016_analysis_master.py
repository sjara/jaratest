from jaratoolbox import celldatabase
import pandas
import subprocess
from jaratest.nick.analysis import pinp_report
reload(pinp_report)
from jaratest.nick.analysis.pinp_report import *
from numpy import inf
from jaratest.nick.stats import eventresponse
from jaratest.nick.stats import am_funcs

pinp016db = celldatabase.generate_cell_database('/home/nick/src/jaratest/nick/inforecordings/pinp016/pinp016_inforec.py')

#Waveform analysis
allShapeQuality = np.empty(len(pinp016db))
for indCell, cell in pinp016db.iterrows():
    peakAmplitudes = cell['clusterPeakAmplitudes']
    spikeShapeSD = cell['clusterSpikeSD']
    shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    allShapeQuality[indCell] = shapeQuality
allShapeQuality[allShapeQuality==inf]=0
pinp016db['shapeQuality'] = allShapeQuality

#Noise response, new version
noiseZscore = np.empty(len(pinp016db))
noisePval = np.empty(len(pinp016db))
baseRange = [-0.2,0]
responseRange = [0, 0.2]
for indCell, cell in pinp016db.iterrows():
    zScore, pVal = eventresponse.event_response_score(cell, 'noiseburst',
                                                      responseRange=responseRange,
                                                      baseRange=baseRange)
    noiseZscore[indCell] = zScore
    noisePval[indCell] = pVal
pinp016db['noiseZscore'] = noiseZscore
pinp016db['noisePval'] = noisePval

#Laser pulse response
pulseZscore = np.empty(len(pinp016db))
pulsePval = np.empty(len(pinp016db))
for indCell, cell in pinp016db.iterrows():
    zScore, pVal = eventresponse.event_response_score(cell, 'laserpulse')
    pulseZscore[indCell] = zScore
    pulsePval[indCell] = pVal
pinp016db['pulseZscore'] = pulseZscore
pinp016db['pulsePval'] = pulsePval

#Laser train response
trainRatio = np.empty(len(pinp016db))
for indCell, cell in pinp016db.iterrows():
    ratio = eventresponse.train_response_ratio(cell, 'lasertrain')
    trainRatio[indCell] = ratio
pinp016db['trainRatio'] = trainRatio

#AM stats
amRval = np.empty(len(pinp016db))
highestSync = np.empty(len(pinp016db))
for indCell, cell in pinp016db.iterrows():
    r_val = am_funcs.am_dependence(cell)
    amRval[indCell] = r_val
    hs = am_funcs.highest_significant_sync(cell)
    highestSync[indCell] = hs
pinp016db['amRval'] = amRval
pinp016db['highestSync'] = highestSync


#Query the database and make reports
soundResponsive = pinp016db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')



#Plot reports
# fig_path = '/home/nick/data/database/pinp016/reports_isi_shape_laser_train/'
# for indCell, cell in result.iterrows():
#     plot_pinp_report(cell, fig_path)

#Laser pulse response
# pulseZscore = np.empty(len(pinp016db))
# pulsePval = np.empty(len(pinp016db))
# for indCell, cell in pinp016db.iterrows():
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
# pinp016db['pulseZscore'] = pulseZscore
# pinp016db['pulsePval'] = pulsePval

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

q10s = []
ixs = []
tcType = 'tc'
for index, cell in soundResponsive.iterrows():
    loader = dataloader.DataLoader(cell['subject'])
    try:
        tuningindex = cell['sessiontype'].index(tcType)
    except ValueError:
        q10s.append(None)
        continue
    bdata = loader.get_session_behavior(cell['behavior'][tuningindex])
    possibleFreq = np.unique(bdata['currentFreq'])
    possibleInten = np.unique(bdata['currentIntensity'])
    zvalArray = tuningfuncs.tuning_curve_response(cell)
    tuner = tuningfuncs.TuningAnalysis(np.flipud(zvalArray), freqLabs = possibleFreq, intenLabs = possibleInten[::-1])
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    button = True
    while button:
        button = plt.waitforbuttonpress()
    q10 = tuner.Q10
    pinp016db.set_value(index, 'Q10', tuner.Q10)
    pinp016db.set_value(index, 'bestFreq', tuner.bestFreq)
    pinp016db.set_value(index, 'highFreq', tuner.highFreq)
    pinp016db.set_value(index, 'lowFreq', tuner.lowFreq)
    pinp016db.set_value(index, 'threshold', tuner.threshold)


#Save the database
pinp016db.to_hdf('/home/nick/data/database/pinp016/pinp016_database.h5', 'database')
