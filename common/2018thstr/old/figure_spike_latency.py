import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
reload(spikesanalysis)
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
from jaratoolbox import extraplots
from scipy import stats
import figparams
reload(figparams)

STUDY_NAME = '2018thstr'

SAVE_FIGURE = 1
outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
figFilename = 'plots_spike_latency' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12, 5] # In inches

labelPosX = [0.07, 0.68]   # Horiz position for panel labels
labelPosY = 0.90    # Vert position for panel label
fontSizePanel = figparams.fontSizePanel

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.1, right=0.98, top=0.88, bottom=0.10, wspace=0.52, hspace=0)
np.random.seed(0)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

goodLaser = dbase.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
goodStriatum = dbase.groupby('brainArea').get_group('rightAstr').query('isiViolations<0.02 and spikeShapeQuality>2')
goodLaserPlusStriatum = goodLaser.append(goodStriatum, ignore_index=True)
goodFit = goodLaserPlusStriatum.query('rsquaredFit > 0.08')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

dataframe = goodFitToUse


### -- Example plot -- ###

threshold = 0.2

cellDict = {'subject' : 'pinp017',
            'date' : '2017-03-22',
            'depth' : 1143,
            'tetrode' : 2,
            'cluster' : 4}

cellInd, dbRow = celldatabase.find_cell(dbase, **cellDict)
cell = ephyscore.Cell(dbRow)

try:
    ephysData, bdata = cell.load('tc')
except (IndexError, ValueError): #The cell does not have a tc or the tc session has no spikes
    print "No tc for cell {}".format(indRow)
    sys.exit()

eventOnsetTimes = ephysData['events']['soundDetectorOn']
eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, minEventOnsetDiff=0.2)
spikeTimes = ephysData['spikeTimes']
freqEachTrial = bdata['currentFreq']
possibleFreq = np.unique(freqEachTrial)
intensityEachTrial = bdata['currentIntensity']
possibleIntensity = np.unique(intensityEachTrial)

#FIXME: I need to remove the last event here if there is an extra one
if len(eventOnsetTimes) == len(freqEachTrial)+1:
    eventOnsetTimes = eventOnsetTimes[:-1]

trialsEachCondition = behavioranalysis.find_trials_each_combination(intensityEachTrial, possibleIntensity,
                                                                    freqEachTrial, possibleFreq)
baseRange = [-0.1, 0]
responseRange = [0, 0.1]
alignmentRange = [-0.2, 0.2]

#Align all spikes to events
(spikeTimesFromEventOnset,
trialIndexForEachSpike,
indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimes,
                                                            eventOnsetTimes,
                                                            alignmentRange)

#Count spikes in baseline and response ranges
nspkBase = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                    indexLimitsEachTrial,
                                                    baseRange)
nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                    indexLimitsEachTrial,
                                                    responseRange)

#Filter and average the response spikes by the condition matrix
conditionMatShape = np.shape(trialsEachCondition)
numRepeats = np.product(conditionMatShape[1:])
nSpikesMat = np.reshape(nspkResp.squeeze().repeat(numRepeats), conditionMatShape)
spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
avgRespArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
    trialsEachCondition, 0).astype('float')

thresholdResponse = nspkBase.mean() + threshold*(avgRespArray.max()-nspkBase.mean())

if not np.any(avgRespArray > thresholdResponse):
    print "Nothing above the threshold"
    sys.exit()

#Determine trials that come from a I/F pair with a response above the threshold
fra = avgRespArray > thresholdResponse
selectedTrials = np.any(trialsEachCondition[:,fra], axis=1)

# -- Calculate response latency --
indexLimitsSelectedTrials = indexLimitsEachTrial[:,selectedTrials]
timeRangeForLatency = [-0.1,0.1]
(respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                        indexLimitsSelectedTrials,
                                                        timeRangeForLatency, threshold=0.5)


print 'Response latency: {:0.1f} ms'.format(1e3*respLatency)

# ------------ From here down is for plotting -------------
selectedTrialsInds = np.flatnonzero(selectedTrials)
# selectedSpikesInds = np.isin(trialIndexForEachSpike,selectedTrialsInds)#NOTE: Requires newer numpy
selectedSpikesInds = np.in1d(trialIndexForEachSpike,selectedTrialsInds)
tempTIFES = trialIndexForEachSpike[selectedSpikesInds]
newSpikeTimes = spikeTimesFromEventOnset[selectedSpikesInds]

# The next thing is slow, but I don't have time to optimize
newTrialInds = np.empty(tempTIFES.shape, dtype=int)
for ind,trialInd in enumerate(np.unique(tempTIFES)):
    newTrialInds[tempTIFES==trialInd] = ind


axRaster = plt.subplot(gs[0, 0:2])
# plt.title(cellInd)
plt.plot(newSpikeTimes, newTrialInds, '.k')
#plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.k') # Plot all trials
# plt.xlim(timeRangeForLatency)
plt.xlim([-0.05, 0.1])
plt.hold(1)
plt.axvline(respLatency,color='r')
plt.axis('off')

axRaster.annotate('A', xy=(labelPosX[0], labelPosY), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')


axPSTH = plt.subplot(gs[1, 0:2])
# plt.plot(interim['timeVec'], interim['avgCount'],'.-k')
plt.hold(1)
maxFR = np.max(interim['psth'])
plt.axvline(respLatency,color='r')
plt.axhline(interim['threshold']/maxFR,ls='--',color='0.75')
plt.axhline(interim['baseline']/maxFR,ls=':',color='0.75')
plt.axhline(interim['maxResponse']/maxFR,ls=':',color='0.75')
plt.plot(interim['timeVec'],interim['psth']/maxFR,'r-',mec='none',lw=3)
# plt.xlim(timeRangeForLatency)
ax = plt.gca()
ax.set_yticks([0, 0.5, 1.0])
plt.ylim([0, 1.1])
plt.xlim([-0.05, 0.1])
ax.set_xticks([0, 0.1])
plt.ylabel('Normalized spike rate')
plt.xlabel('Time from sound onset (s)')
extraplots.boxoff(axPSTH)
plt.show()


### -- Summary plot -- ###
areas = ['rightThal', 'rightAC'] # Should match 'tickLabels'
tickLabels = ['ATh->Str', 'AC->AStr']       # Should match 'order'
groups = dataframe.groupby('brainArea')
boxColor = "0.2"
linewidth = 2

dataList = []
for area in areas:
    dbThisArea = groups.get_group(area)
    dataThisArea = dbThisArea['latency'][pd.notnull(dbThisArea['latency'])]*1000
    dataList.append(dataThisArea)

axHist = plt.subplot(gs[0:2, 2])

# for position, groupName in enumerate(order):
#     data = groups.get_group(groupName)[column].values*1000
#     dataList.append(data)
#     pos = jitter(np.ones(len(data))*position, 0.20)
#     axHist.plot(pos, data, 'o', mec = 'k', mfc = 'None')
#     medline(np.nanmedian(data), position, 0.5)
#     order_n.append(len(data))

bp = axHist.boxplot(dataList, widths=0.5)

# axHist.set_xticks(range(2))
axHist.set_xticklabels(tickLabels)
# axHist.set_xlim([-0.5, 1.5])
# axHist.set_ylim([0, 65])
plt.ylabel('Response latency (ms)')
extraplots.boxoff(axHist)
# plt.title('ATh -> Str N: {}\nAC -> Str N: {}'.format(order_n[0], order_n[1]))
plt.setp(bp['boxes'], color=boxColor, lw=linewidth)
plt.setp(bp['whiskers'], color=boxColor, lw=linewidth)
plt.setp(bp['fliers'], color=boxColor, marker='+')
plt.setp(bp['medians'], color=boxColor, lw=linewidth)
plt.setp(bp['caps'], color=boxColor)

axHist.annotate('B', xy=(labelPosX[1], labelPosY), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

zVal, pVal = stats.ranksums(*dataList)
plt.title('p={:.3f}'.format(pVal))

plt.show()
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
