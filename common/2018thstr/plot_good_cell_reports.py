import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratest.nick.reports import pinp_report
from collections import Counter
from scipy import stats
from scipy import signal
import pandas as pd
import figparams
reload(figparams)
reload(pinp_report)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')

db = pd.read_hdf(dbPath, key='dataframe')
# db = db.query("subject=='pinp015'")
# goodLaser = db.query('pulsePval<0.05 and pulseZscore>0 and trainRatio>0.8')
# goodLaser = db[db['taggedCond']==0]
goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2 and nSpikes>2000')
goodLaser = goodShape.query('autoTagged==1')

goodLaserAM = goodLaser[~pd.isnull(goodLaser['highestSyncCorrected'])]
### PLOT REPORTS FOR CELLS IN AM DATASET
reportDirAM = '/tmp/20180421_AM_CELLS'
if not os.path.exists(reportDirAM):
    os.mkdir(reportDirAM)

# for indRow, dbRow in goodLaserAM.iterrows():

#     subject = dbRow['subject']
#     date = dbRow['date']
#     depth = dbRow['depth']
#     tetrode = dbRow['tetrode']
#     cluster = int(dbRow['cluster'])
#     brainArea = dbRow['brainArea']
#     cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)
#     print "Plotting report for {}".format(cellName)

#     plt.clf()
#     pinp_report.plot_pinp_report(dbRow, useModifiedClusters=True)
#     figsize = (9, 11)
#     plt.gcf().set_size_inches(figsize)
#     fullDir = os.path.join(reportDirAM, brainArea)
#     if not os.path.exists(fullDir):
#         os.mkdir(fullDir)
#     fullName = os.path.join(fullDir, cellName)
#     plt.savefig(fullName,format='png')


### PLOT REPORTS FOR CELLS IN FREQ DATASET
reportDirFreq = '/tmp/20180421_FREQ_CELLS_noRsquared'
if not os.path.exists(reportDirFreq):
    os.mkdir(reportDirFreq)
goodFit = goodLaser.query('rsquaredFit > 0.0')
# #Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

for indRow, dbRow in goodFitToUse.iterrows():

    subject = dbRow['subject']
    date = dbRow['date']
    depth = dbRow['depth']
    tetrode = dbRow['tetrode']
    cluster = int(dbRow['cluster'])
    brainArea = dbRow['brainArea']
    cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)
    print "Plotting report for {}".format(cellName)

    plt.clf()
    pinp_report.plot_pinp_report(dbRow, useModifiedClusters=True)
    figsize = (9, 11)
    plt.gcf().set_size_inches(figsize)
    fullDir = os.path.join(reportDirFreq, brainArea)
    if not os.path.exists(fullDir):
        os.mkdir(fullDir)
    fullName = os.path.join(fullDir, cellName)
    plt.savefig(fullName,format='png')


### LATENCY PLOTS
# reportDirLatency = '/tmp/20180421_LATENCY_CELLS'
# if not os.path.exists(reportDirLatency):
#     os.mkdir(reportDirLatency)
# threshold = 0.2
# for indRow, dbRow in goodFitToUse.iterrows():

#     # cellInd, dbRow = celldatabase.find_cell(dataframe, **cellDict)
#     cell = ephyscore.Cell(dbRow, useModifiedClusters=True)

#     try:
#         ephysData, bdata = cell.load('tc')
#     except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
#         print "No tc for cell {}".format(indRow)
#         sys.exit()

#     # eventOnsetTimes = ephysData['events']['soundDetectorOn']
#     eventOnsetTimes = ephysData['events']['stimOn']

#     eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
#     spikeTimes = ephysData['spikeTimes']
#     freqEachTrial = bdata['currentFreq']
#     possibleFreq = np.unique(freqEachTrial)
#     intensityEachTrial = bdata['currentIntensity']
#     possibleIntensity = np.unique(intensityEachTrial)

#     #FIXME: I need to remove the last event here if there is an extra one
#     if len(eventOnsetTimes) == len(freqEachTrial)+1:
#         eventOnsetTimes = eventOnsetTimes[:-1]
#     elif len(eventOnsetTimes) < len(freqEachTrial):
#         print "Wrong number of events, probably caused by the original sound detector problems"
#         # dataframe.loc[indRow, 'latency'] = np.nan
#         continue
#     else:
#         print "Something else wrong with the events"
#         continue

#     trialsEachCondition = behavioranalysis.find_trials_each_combination(intensityEachTrial, possibleIntensity,
#                                                                         freqEachTrial, possibleFreq)

#     baseRange = [-0.1, 0]
#     responseRange = [0, 0.1]
#     alignmentRange = [-0.2, 0.2]

#     #Align all spikes to events
#     (spikeTimesFromEventOnset,
#     trialIndexForEachSpike,
#     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
#                                                                 eventOnsetTimes,
#                                                                 alignmentRange)

#     #Count spikes in baseline and response ranges
#     nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         baseRange)
#     nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
#                                                         indexLimitsEachTrial,
#                                                         responseRange)

#     #Filter and average the response spikes by the condition matrix
#     conditionMatShape = np.shape(trialsEachCondition)
#     numRepeats = np.product(conditionMatShape[1:])
#     nSpikesMat = np.reshape(nspkResp.squeeze().repeat(numRepeats), conditionMatShape)
#     spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
#     avgRespArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
#         trialsEachCondition, 0).astype('float')

#     thresholdResponse = nspkBase.mean() + threshold*(avgRespArray.max()-nspkBase.mean())

#     if not np.any(avgRespArray > thresholdResponse):
#         print "Nothing above the threshold"
#         sys.exit()

#     #Determine trials that come from a I/F pair with a response above the threshold
#     fra = avgRespArray > thresholdResponse
#     selectedTrials = np.any(trialsEachCondition[:,fra], axis=1)

#     # -- Calculate response latency --
#     indexLimitsSelectedTrials = indexLimitsEachTrial[:,selectedTrials]
#     timeRangeForLatency = [-0.1,0.2]
#     (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
#                                                             indexLimitsSelectedTrials,
#                                                             timeRangeForLatency, threshold=0.5,
#                                                             win=signal.hanning(11))


#     print 'Response latency: {:0.1f} ms'.format(1e3*respLatency)

#     # ------------ From here down is for plotting -------------
#     selectedTrialsInds = np.flatnonzero(selectedTrials)
#     # selectedSpikesInds = np.isin(trialIndexForEachSpike,selectedTrialsInds)#NOTE: Requires newer numpy
#     selectedSpikesInds = np.in1d(trialIndexForEachSpike,selectedTrialsInds)
#     tempTIFES = trialIndexForEachSpike[selectedSpikesInds]
#     newSpikeTimes = spikeTimesFromEventOnset[selectedSpikesInds]

#     # The next thing is slow, but I don't have time to optimize
#     newTrialInds = np.empty(tempTIFES.shape, dtype=int)
#     for ind,trialInd in enumerate(np.unique(tempTIFES)):
#         newTrialInds[tempTIFES==trialInd] = ind

#     plt.clf()
#     plt.title(respLatency)
#     plt.subplot(2,1,1)
#     plt.plot(newSpikeTimes, newTrialInds, '.k')
#     #plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k') # Plot all trials
#     plt.xlim(timeRangeForLatency)
#     plt.hold(1)
#     plt.title('{}'.format(indRow))
#     plt.axvline(respLatency,color='r')

#     plt.subplot(2,1,2)
#     plt.plot(interim['timeVec'], interim['avgCount'],'.-k')
#     plt.hold(1)
#     plt.axvline(respLatency,color='r')
#     plt.axhline(interim['threshold'],ls='--',color='0.75')
#     plt.axhline(interim['baseline'],ls=':',color='0.75')
#     plt.axhline(interim['maxResponse'],ls=':',color='0.75')
#     plt.plot(interim['timeVec'],interim['psth'],'r-',mec='none',lw=3)
#     plt.xlim(timeRangeForLatency)
#     # plt.show()
#     subject = dbRow['subject']
#     date = dbRow['date']
#     depth = dbRow['depth']
#     tetrode = dbRow['tetrode']
#     cluster = int(dbRow['cluster'])
#     brainArea = dbRow['brainArea']
#     cellName = "{}_{}_{}_TT{}c{}".format(subject, date, depth, tetrode, cluster)

#     figsize = (5, 5)
#     plt.gcf().set_size_inches(figsize)
#     fullDir = os.path.join(reportDirLatency, brainArea)
#     if not os.path.exists(fullDir):
#         os.mkdir(fullDir)
#     fullName = os.path.join(fullDir, cellName)
#     plt.savefig(fullName,format='png')
    # plt.waitforbuttonpress()
