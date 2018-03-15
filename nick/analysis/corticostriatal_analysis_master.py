import pandas
from matplotlib import pyplot as plt
from collections import Counter
from jaratest.nick.stats import am_funcs
reload(am_funcs)
import numpy as np
from jaratoolbox import colorpalette
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from scipy import stats

#Its just functions that load data when given a 'cell' from the celldatabase
from jaratest.nick.database import dataloader_v3 as dataloader

from jaratest.nick.stats import tuningfuncs
from jaratest.nick.reports import pinp_report
reload(pinp_report)
dbFolderFormat = '/home/nick/data/database/{}/{}_database.h5' #(mouse, mouse)
inforecFolderFormat = '/home/nick/src/jaratest/nick/inforecordings/{}/{}_inforec.py' #(mouse, mouse)

mice = ['pinp016', 'pinp017', 'pinp018']

RECALCULATE_DB=1
dbs = []
for mouse in mice:
    if RECALCULATE_DB==1:
        db = celldatabase.generate_cell_database(inforecFolderFormat.format(mouse, mouse))

        #Calculate shape quality
        allShapeQuality = np.empty(len(db))
        for indCell, cell in db.iterrows():
            peakAmplitudes = cell['clusterPeakAmplitudes']
            spikeShapeSD = cell['clusterSpikeSD']
            shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
            allShapeQuality[indCell] = shapeQuality
        allShapeQuality[allShapeQuality==inf]=0
        db['shapeQuality'] = allShapeQuality

        #Calculate noiseburst response
        #TODO: Response to things other than noise as well??
        #DONE: Remove eventresponse dependency
        noiseZscore = np.empty(len(db))
        noisePval = np.empty(len(db))
        baseRange = [-0.2,0]
        responseRange = [0, 0.2]
        for indCell, cell in db.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'noiseburst')
            eventOnsetTimes = eventData.get_event_onset_times()
            alignmentRange = [baseRange[0], responseRange[1]]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        alignmentRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)
            [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
            noiseZscore[indCell] = zScore
            noisePval[indCell] = pVal
        db['noiseZscore'] = noiseZscore
        db['noisePval'] = noisePval

        #Laser pulse response
        #NOTE: This does the same thing as the noise burst response, but I am not making a function
        #because things are getting hidden and I want to be more explicit about what I am doing.
        pulseZscore = np.empty(len(db))
        pulsePval = np.empty(len(db))
        baseRange = [-0.1,0]
        responseRange = [0, 0.1]
        for indCell, cell in db.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'laserpulse')
            eventOnsetTimes = eventData.get_event_onset_times()
            alignmentRange = [baseRange[0], responseRange[1]]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        alignmentRange)
            nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                baseRange)
            nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                responseRange)
            [zScore, pVal] = stats.ranksums(nspkResp,nspkBase)
            pulseZscore[indCell] = zScore
            pulsePval[indCell] = pVal
        db['pulseZscore'] = pulseZscore
        db['pulsePval'] = pulsePval

        #Laser train response, ratio of pulse avg spikes
        trainRatio = np.empty(len(db))
        timeRange = [-0.1, 1] #For initial alignment
        baseRange = [0, 0.05]
        responseRange = [0.2, 0.25]
        for indCell, cell in db.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'lasertrain')
            eventOnsetTimes = eventData.get_event_onset_times()
            eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        timeRange)
            avgSpikesBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                     indexLimitsEachTrial,
                                                                     baseRange).mean()
            avgSpikesResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                     indexLimitsEachTrial,
                                                                     responseRange).mean()
            ratio = avgSpikesResp/avgSpikesBase
            trainRatio[indCell] = ratio
        db['trainRatio'] = trainRatio

        #AM stats
        #TODO: Change correlation to ANOVA
        amKWstat = np.empty(len(db))
        amKWp = np.empty(len(db))

        for indCell, cell in db.iterrows():
            spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
            eventOnsetTimes = eventData.get_event_onset_times()
            bdata = dataloader.get_session_bdata(cell, 'am')
            rateEachTrial = bdata['currentFreq'] #NOTE: bdata uses 'Freq' but this is AM so I'm calling it rate
            possibleRate = np.unique(rateEachTrial)
            timeRange = [0, 0.5]
            respSpikeArrays = [] #List to hold the arrays of response bin spike counts (not all same number of trials)
            respSpikeInds = [] #This will hold arrays with the inds for which rate the response spikes came from
            for indRate, thisRate in enumerate(possibleRate):
                trialsThisRate = np.flatnonzero(rateEachTrial==thisRate)
                (spikeTimesFromEventOnset,
                 trialIndexForEachSpike,
                 indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                               eventOnsetTimes[trialsThisRate],
                                                                               timeRange)
                nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                                    indexLimitsEachTrial,
                                                                    timeRange)
                respSpikeArrays.append(nspkResp.ravel())
            try:
                statistic, pval = stats.kruskal(*respSpikeArrays)
            except ValueError:
                pval=None
                statistic=None
            amKWp[indCell] = pval
            amKWstat[indCell] = statistic
        db['amKWp'] = amKWp
        db['amKWstat'] = amKWstat

        #NOTE: I am here
        #Highest significant sync rate
        highestSync = np.empty(len(db))
        db['highestSync'] = highestSync
        for indCell, cell in db.iterrows():
            hs = am_funcs.highest_significant_sync(cell)
            highestSync[indCell] = hs
    else:
        dbFn = dbFolderFormat.format(mouse, mouse)
        db = pandas.read_hdf(dbFn, 'database')
    dbs.append(db)

masterdb = pandas.concat(dbs, ignore_index=True)

masterdb['BW10'] = 1/masterdb['Q10']

soundResponsive = masterdb.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')

soundResponsive['Identified'] = (soundResponsive.pulsePval<0.05) & (soundResponsive.trainRatio>0.8)

BW10s = []
ixs = []
tcType = 'tc'
dbToProcess = soundResponsive

for index, cell in dbToProcess.iterrows():
    loader = dataloader.DataLoader(cell['subject'])
    try:
        tuningindex = cell['sessiontype'].index(tcType)
    except ValueError:
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
    masterdb.set_value(index, 'BW10', tuner.BW10)
    masterdb.set_value(index, 'bestFreq', tuner.bestFreq)
    masterdb.set_value(index, 'highFreq', tuner.highFreq)
    masterdb.set_value(index, 'lowFreq', tuner.lowFreq)
    masterdb.set_value(index, 'threshold', tuner.threshold)

db.to_hdf('/home/nick/data/database/corticostriatal_master_20170452.h5', 'database')


#Fixing a mistake: the master database should have been set, but I set a diff database instead. 
for index, cell in db.iterrows():
    if pandas.notnull(cell['BW10']):
        masterdb.set_value(index, 'BW10', cell.BW10)
        masterdb.set_value(index, 'bestFreq', cell.bestFreq)
        masterdb.set_value(index, 'highFreq', cell.highFreq)
        masterdb.set_value(index, 'lowFreq', cell.lowFreq)
        masterdb.set_value(index, 'threshold', cell.threshold)

soundResponsive = masterdb.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')
soundLaserResponsive = soundResponsive.query('pulsePval<0.05 and trainRatio>0.8')


# plt.clf()
# stdev = 0.05
# markersize = 8
# linewidth = 2
# thalColor = colorpalette.TangoPalette['Orange2']
# cortColor = colorpalette.TangoPalette['Plum2']


# colors = {'rightThal':thalColor, 'rightAC':cortColor}

# #Hist of highestSync
plt.hold(1)
plt.clf()
plt.hist(soundResponsive.groupby('brainarea').get_group('rightThal')['highestSync'], histtype='step', lw = 2)
plt.hist(soundResponsive.groupby('brainarea').get_group('rightAC')['highestSync'], histtype='step', lw = 2)
plt.show()

# #Hist of amRval
plt.clf()
plt.hold(1)
plt.hist(soundResponsive.groupby('brainarea').get_group('rightThal')['amRval'], histtype='step', lw = 2)
plt.hist(soundResponsive.groupby('brainarea').get_group('rightAC')['amRval'], histtype='step', lw = 2)
plt.xlabel('Correlation R val between AM rate and overall FR during stim', fontsize=14)
plt.show()

#Hist of BW10
# plt.clf()
# plt.hold(1)
# plt.hist(soundResponsive.groupby('brainarea').get_group('rightThal')['BW10'].dropna(), histtype='step', lw = 2)
# plt.hist(soundResponsive.groupby('brainarea').get_group('rightAC')['BW10'].dropna(), histtype='step', lw = 2)
# plt.show()

#Thresholds
#Nurons that had a BW10 have a valid threshold. otherwise, I was clicking to move the program forward
hadBW10 = soundResponsive[pandas.notnull(soundResponsive.BW10)]
plt.clf()
plt.hold(1)
plt.hist(hadBW10.groupby('brainarea').get_group('rightThal')['threshold'].dropna(), histtype='step', lw = 2)
plt.hist(hadBW10.groupby('brainarea').get_group('rightAC')['threshold'].dropna(), histtype='step', lw = 2)
plt.show()

#Plot reports
thalSR = soundResponsive.groupby('brainarea').get_group('rightThal')
fig_path = '/home/nick/data/database/corticostriatal_master_20170425/reports_SR_thal/'
for indCell, cell in thalSR.iterrows():
    pinp_report.plot_pinp_report(cell, fig_path)

cortSR = soundResponsive.groupby('brainarea').get_group('rightAC')
fig_path = '/home/nick/data/database/corticostriatal_master_20170425/reports_SR_ctx/'
for indCell, cell in cortSR.iterrows():
    pinp_report.plot_pinp_report(cell, fig_path)

