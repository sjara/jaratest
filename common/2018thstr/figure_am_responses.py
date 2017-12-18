import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from collections import Counter
import pandas as pd
import figparams
reload(figparams)

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')

PANELS = [1, 1, 1, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'plots_figure_name' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,5] # In inches

thalHistColor = '0.4'
acHistColor = '0.4'

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.36, 0.7]   # Horiz position for panel labels
labelPosY = [0.9, 0.48, 0.19]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.1, wspace=.4, hspace=0.5)

#Load example data
exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath)

exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

#Load database with AM data
db = pd.read_hdf(dbPath, key='dataframe')
goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
#Use the good Laser 
goodStriatum = db.groupby('brainArea').get_group('rightAstr').query('isiViolations<0.02 and spikeShapeQuality>2')
goodLaserPlusStriatum = goodLaser.append(goodStriatum, ignore_index=True)


# def plot_example_with_rate(subplotSpec, exampleName):
#     fig = plt.gcf()

#     gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=subplotSpec, wspace=0.0, hspace=0.0 )

#     specRaster = gs[0:2]
#     axRaster = plt.Subplot(fig, specRaster)
#     fig.add_subplot(axRaster)

#     spikeTimes = exampleSpikeTimes[exampleName]
#     indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
#     timeRange = [-0.2, 0.7]
#     freqEachTrial = exampleFreqEachTrial[exampleName]
#     possibleFreq = np.unique(freqEachTrial)
#     trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
#     pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
#                                                    timeRange, trialsEachCondition)
#     plt.setp(pRaster, ms=2)


#     countRange = [0.1, 0.5]
#     spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes,indexLimitsEachTrial,countRange)
#     numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)

#     numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
#                                                        axis=0))

#     if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
#         numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]
#     conditionMatShape = np.shape(trialsEachCondition)
#     numRepeats = np.product(conditionMatShape[1:])
#     nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
#                             conditionMatShape)
#     spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
#     avgSpikesArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
#         trialsEachCondition, 0).astype('float')
#     stdSpikesArray = np.std(spikesFilteredByTrialType, 0)

#     specRate = gs[3]
#     axRate = plt.Subplot(fig, specRate)
#     fig.add_subplot(axRate)

#     plt.hold(True)
#     plt.plot(avgSpikesArray, range(len(possibleFreq)), 'r-')
#     plt.plot(avgSpikesArray-stdSpikesArray, range(len(possibleFreq)), 'k--')
#     plt.plot(avgSpikesArray+stdSpikesArray, range(len(possibleFreq)), 'k--')


def plot_example(subplotSpec, exampleName):

    # lowFreq = 4
    # highFreq = 128
    # nFreqLabels = 3

    # freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqLabels)
    # freqs = np.round(freqs, decimals=1)

    spikeTimes = exampleSpikeTimes[exampleName]
    indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
    timeRange = [-0.2, 0.7]
    freqEachTrial = exampleFreqEachTrial[exampleName]
    possibleFreq = np.unique(freqEachTrial)
    freqLabels = ['{0:.1f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
                                                   timeRange, trialsEachCondition, labels=freqLabels)
    ax = plt.gca()
    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from sound onset (s)')
    ax.set_ylabel('AM Rate (Hz)')
    # ax.set_yticks(freqs)
    # ax.set_yticklabels(freqs)
    plt.setp(pRaster, ms=2)


def plot_hist(ax, dataArr, color, label):
    lowFreq = 4
    highFreq = 128
    nFreqs = 11
    freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqs)
    freqs = np.round(freqs, decimals=1)
    freqs = np.r_[0, freqs]
    freqLabels = ['{}'.format(freq) for freq in freqs[1:]]
    freqLabels = ['NS', ' '] + freqLabels

    roundData = np.round(dataArr[pd.notnull(dataArr)], decimals=1)
    counts = Counter(roundData)

    freqsToPlot = np.r_[0, 1, freqs[1:]]
    index = np.arange(len(freqsToPlot))

    heights = []
    for freq in freqsToPlot:
        try:
            heights.append(100*counts[freq]/np.double(len(roundData)))
        except KeyError:
            heights.append(0)


    barWidth = 0.8
    rects = plt.bar(index+0.5*barWidth,
                    heights,
                    barWidth,
                    label=label,
                    color=color)
    plt.xticks(index + barWidth, freqs)
    ax.set_xticklabels(freqLabels, rotation='vertical')
    plt.ylabel('% cells')
    plt.title('{}, N={}'.format(label, len(roundData)))
    # ax.set_xlim([1.5,index[-1]+2*barWidth-0.5])
    plt.xlabel('Highest AM rate to which\ncell can synchronize (Hz)')
    extraplots.boxoff(ax)

    height = max(heights)*0.05
    extraplots.breakaxis(1.8, 0, 0.5, height, gap=0.4)
    plt.ylim([0, max(heights)+1])


    return rects

column = 'highestSync'
groups = goodLaserPlusStriatum.groupby('brainArea')
##### Thalamus #####
# -- Panel: Thalamus more synchronized --
# axSharp = plt.subplot(gs[0, 0])
spec = gs[0, 0]
if PANELS[0]:
    plt.subplot(spec)
    plot_example(spec, 'Thal1')
    plt.title('ATh -> Str Example 1')
# ax = plt.gc
# ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')

# -- Panel: Thalamus less synchronized --
# axWide = plt.subplot(gs[0, 1])
spec = gs[0, 1]
# axWide.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    plt.subplot(spec)
    plot_example(spec, 'Thal2')
    plt.title('ATh -> Str Example 2')
# -- Panel: Thalamus histogram --
axHist = plt.subplot(gs[0, 2])
# axHist.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    groupName = 'rightThal'
    data = groups.get_group(groupName)[column]
    plot_hist(axHist, data, thalHistColor, 'ATh')

##### Cortex #####
# -- Panel: Cortex more synchronized --
# axSharp = plt.subplot(gs[1, 0])
spec = gs[1, 0]
# axSharp.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[3]:
    plt.subplot(spec)
    plot_example(spec, 'AC1')
    plt.title('AC -> Str Example 1')
# -- Panel: Cortex less synchronized --
# axWide = plt.subplot(gs[1, 1])
spec = gs[1, 1]
# axWide.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[4]:
    plt.subplot(spec)
    plot_example(spec, 'AC2')
    plt.title('AC -> Str Example 2')
# -- Panel: Cortex histogram --
axHist = plt.subplot(gs[1, 2])
# axHist.annotate('F', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[5]:
    groupName = 'rightAC'
    data = groups.get_group(groupName)[column]
    plot_hist(axHist, data, acHistColor, 'AC')


##### Striatum #####
# -- Panel: Striatum more synchronized --
# axSharp = plt.subplot(gs[2, 0])
# spec = gs[2, 0]
# axSharp.annotate('G', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# if PANELS[6]:
#     plt.subplot(spec)
#     plot_example(spec, 'Str1')
# -- Panel: Striatum less synchronized --
# axWide = plt.subplot(gs[2, 1])
# axWide.annotate('H', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# if PANELS[7]:
    # Plot stuff
    # pass
# -- Panel: Striatum histogram --
# axHist = plt.subplot(gs[2, 2])
# # axHist.annotate('I', xy=(labelPosX[2],labelPosY[2]), xycoords='figure fraction',
# #              fontsize=fontSizePanel, fontweight='bold')
# if PANELS[8]:
#     groupName = 'rightAstr'
#     data = groups.get_group(groupName)[column]
#     plot_hist(axHist, data, 'b', 'Striatum')


plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


# thal = goodLaserPlusStriatum.groupby('brainArea').get_group('rightThal')
# thalBW = thal['BW10'][pd.notnull(thal['BW10'])]
# thalThresh = thal['threshold'][pd.notnull(thal['threshold'])]
# thalLatency = thal['medianFSLatency'][pd.notnull(thal['medianFSLatency'])]

# ac = goodLaserPlusStriatum.groupby('brainArea').get_group('rightAC')
# acBW = ac['BW10'][pd.notnull(ac['BW10'])]
# acThresh = ac['threshold'][pd.notnull(ac['threshold'])]
# acLatency = ac['medianFSLatency'][pd.notnull(ac['medianFSLatency'])]

