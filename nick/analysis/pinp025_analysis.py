from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
import numpy as np
from numpy import inf
import pandas
from jaratest.nick.reports import pinp_report
from jaratest.nick.database import dataloader_v3 as dataloader
from jaratest.nick.stats import am_funcs
from scipy import stats

inforecFn = '/home/nick/src/jaratest/common/inforecordings/pinp025_inforec.py'
db = celldatabase.generate_cell_database(inforecFn)

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
noiseZscore = np.empty(len(db))
noisePval = np.empty(len(db))
baseRange = [-0.2,0]
responseRange = [0, 0.2]
for indCell, cell in db.iterrows():
    spikeData, eventData = dataloader.get_session_ephys(cell, 'noiseburst')
    if spikeData.timestamps is not None:
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
    else:
        zScore=0
        pVal=0
    noiseZscore[indCell] = zScore
    noisePval[indCell] = pVal
db['noiseZscore'] = noiseZscore
db['noisePval'] = noisePval

amKWstat = np.empty(len(db))
amKWp = np.empty(len(db))

# for indCell, cell in db.iterrows():
#     spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
#     eventOnsetTimes = eventData.get_event_onset_times()
#     bdata = dataloader.get_session_bdata(cell, 'am')

#     rateEachTrial = bdata['currentFreq'] #NOTE: bdata uses 'Freq' but this is AM so I'm calling it rate
#     possibleRate = np.unique(rateEachTrial)
#     timeRange = [0, 0.5]
#     respSpikeArrays = [] #List to hold the arrays of response bin spike counts (not all same number of trials)
#     respSpikeInds = [] #This will hold arrays with the inds for which rate the response spikes came from
#     for indRate, thisRate in enumerate(possibleRate):
#         trialsThisRate = np.flatnonzero(rateEachTrial==thisRate)
#         (spikeTimesFromEventOnset,
#             trialIndexForEachSpike,
#             indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
#                                                                         eventOnsetTimes[trialsThisRate],
#                                                                         timeRange)
#         nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                             indexLimitsEachTrial,
#                                                             timeRange)
#         respSpikeArrays.append(nspkResp.ravel())

#     try:
#         statistic, pval = stats.kruskal(*respSpikeArrays)
#     except ValueError:
#         pval=None
#         statistic=None

#     amKWp[indCell] = pval
#     amKWstat[indCell] = statistic
# db['amKWp'] = amKWp
# db['amKWstat'] = amKWstat

#TODO: investigate this function - is it doing what we want??
# highestSync = np.empty(len(db))
# db['highestSync'] = highestSync
# for indCell, cell in db.iterrows():
#     hs = am_funcs.highest_significant_sync(cell)
#     highestSync[indCell] = hs

#Plotting
# figPath = '/home/nick/data/reports/nick/20170904_pinp025_striatum_cells/'
soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05 and nSpikes>100')
# for indCell, cell in soundResponsive.iterrows():
#     pinp_report.plot_pinp_report(cell, figPath)
