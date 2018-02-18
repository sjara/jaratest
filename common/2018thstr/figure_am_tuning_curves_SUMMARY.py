import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from collections import Counter
from scipy import stats
import pandas as pd
import figparams
reload(figparams)

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')

db = pd.read_hdf(dbPath, key='dataframe')
goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')

# popStatColumn = 'd_aMax'
# popStatCol = 'mutualInfoBC'

ac = goodLaser.groupby('brainArea').get_group('rightAC')
thal = goodLaser.groupby('brainArea').get_group('rightThal')

np.random.seed(0)


def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

PANELS=[1,1,1,1,1]

SAVE_FIGURE = 1
# outputDir = '/tmp/'
outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
figFilename = 'plots_am_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [16,8] # In inches

thalHistColor = '0.4'
acHistColor = '0.4'

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

#Params for extraplots significance stars
fontSizeNS = figparams.fontSizeNS
fontSizeStars = figparams.fontSizeStars
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor

dotEdgeColor = figparams.dotEdgeColor

labelPosX = [0.04, 0.32, 0.62]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']
colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 6)
gs.update(left=0.1, right=0.90, top=0.95, bottom=0.1, wspace=.4, hspace=0.4)

#Load example data
exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath)

exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

def plot_example_with_rate(subplotSpec, exampleName, color='k'):
    fig = plt.gcf()

    gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=subplotSpec, wspace=-0.45, hspace=0.0 )

    specRaster = gs[0:2]
    axRaster = plt.Subplot(fig, specRaster)
    fig.add_subplot(axRaster)

    spikeTimes = exampleSpikeTimes[exampleName]
    indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
    timeRange = [-0.2, 0.7]
    freqEachTrial = exampleFreqEachTrial[exampleName]
    possibleFreq = np.unique(freqEachTrial)
    freqLabels = ['{0:.1f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
                                                   timeRange, trialsEachCondition, labels=freqLabels)
    plt.setp(pRaster, ms=2)
    ax = plt.gca()
    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from\nsound onset (s)')
    ax.set_ylabel('AM Rate (Hz)')

    # ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')


    countRange = [0.1, 0.5]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes,indexLimitsEachTrial,countRange)
    numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)

    numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                       axis=0))

    if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
        numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]
    conditionMatShape = np.shape(trialsEachCondition)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
                            conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
    avgSpikesArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
        trialsEachCondition, 0).astype('float')/np.diff(np.array(countRange))
    stdSpikesArray = np.std(spikesFilteredByTrialType, 0)/np.diff(np.array(countRange))

    specRate = gs[3]
    axRate = plt.Subplot(fig, specRate)
    fig.add_subplot(axRate)

    nRates = len(possibleFreq)
    plt.hold(True)
    plt.plot(avgSpikesArray, range(nRates), 'ro-', mec='none', ms=7, lw=3, color=color)
    plt.plot(avgSpikesArray-stdSpikesArray, range(len(possibleFreq)), 'k:')
    plt.plot(avgSpikesArray+stdSpikesArray, range(len(possibleFreq)), 'k:')
    axRate.set_ylim([-0.5, nRates-0.5])
    axRate.set_yticks(range(nRates))
    axRate.set_yticklabels([])
    
    #ax = plt.gca()
    axRate.set_xlabel('Firing rate\n(spk/s)')
    extraplots.boxoff(axRate)
    # extraplots.boxoff(ax, keep='right')
    return (axRaster, axRate)

spec = gs[0, 0:2]
if PANELS[0]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'Thal1', color=colorATh)
    axRaster.set_title('ATh:Str example 1')
    axRate.set_xlim([0,200])
    axRate.set_xticks([0,200])
# ax = plt.gc
axRaster.annotate('A', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

# -- Panel: Thalamus less synchronized --
# axWide = plt.subplot(gs[0, 1])
spec = gs[0, 2:4]
if PANELS[1]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'Thal2', color=colorATh)
    axRaster.set_title('ATh : Str example 2')
    axRate.set_xlim([0,20])
    axRate.set_xticks([0,20])
axRaster.annotate('B', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

spec = gs[1, 0:2]
# axSharp.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'AC1', color=colorAC)
    axRaster.set_title('AC > Str example 1')
    axRate.set_xlim([0, 25])
    axRate.set_xticks([0, 25])

axRaster.annotate('C', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
# -- Panel: Cortex less synchronized --
# axWide = plt.subplot(gs[1, 1])
spec = gs[1, 2:4]
# axWide.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[3]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'AC2', color=colorAC)
    axRaster.set_title('AC>Str example 2')
    axRate.set_xlim([0, 30])
    axRate.set_xticks([0, 30])
axRaster.annotate('D', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')


############## Mutual info AM RATE #######################
popStatCol = 'mutualInfoPerSpikeBits'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

axSummary = plt.subplot(gs[1, 4])

#REMOVE NEGATIVE MI VALUES, REPLACE WITH 0
acPopStat[acPopStat < 0] = 0
thalPopStat[thalPopStat < 0] = 0
pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=0.5)
medline(np.median(thalPopStat), 0, 0.5)
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=0.5)
medline(np.median(acPopStat), 1, 0.5)
plt.ylabel('MI, Spike rate / AM rate (bits/spike)')
tickLabels = ['ATh:Str', 'AC:Str']
axSummary.set_xticks(range(2))
axSummary.set_xticklabels(tickLabels)
axSummary.set_xlim([-0.5, 1.5])
extraplots.boxoff(axSummary)
axSummary.set_ylim([-0.001, 0.25])

zstat, pVal = stats.ranksums(thalPopStat, acPopStat)

print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)

# plt.title('p = {}'.format(np.round(pVal, decimals=5)))

axSummary.annotate('E', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')

yDataMax = max([max(acPopStat), max(thalPopStat)])
yStars = yDataMax + yDataMax*starYfactor
yStarHeight = (yDataMax*starYfactor)*starHeightFactor
extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                    fontSize=fontSizeStars, gapFactor=starGapFactor)
plt.hold(1)

################### Mutual info PHASE #####################
# popStatCol = 'mutualInfoPerSpike'
# acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
# thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

axSummary = plt.subplot(gs[1, 5])

# pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
# axSummary.plot(pos, thalPopStat, 'o', mec = 'k', mfc = 'None')
# medline(np.median(thalPopStat), 0, 0.5)
# pos = jitter(np.ones(len(acPopStat))*1, 0.20)
# axSummary.plot(pos, acPopStat, 'o', mec = 'k', mfc = 'None')
# medline(np.median(acPopStat), 1, 0.5)
# plt.ylabel('Mutual information between neuronal spike rate and AM rate (nats/spike)')
# tickLabels = ['ATh->Str', 'AC->AStr']
# axSummary.set_xticks(range(2))
# axSummary.set_xticklabels(tickLabels)
# axSummary.set_xlim([-0.5, 1.5])
# extraplots.boxoff(axSummary)
# axSummary.set_ylim([-0.001, 0.161])

################### Highest Sync #####################
popStatCol = 'highestSyncCorrected'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

acPopStat = acPopStat[acPopStat>0]
thalPopStat = thalPopStat[thalPopStat>0]

possibleFreqLabels = ["{0:.1f}".format(freq) for freq in np.unique(thalPopStat)]

acPopStat = np.log(acPopStat)
thalPopStat = np.log(thalPopStat)

axSummary = plt.subplot(gs[0, 4])

pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=0.5)
medline(np.median(thalPopStat), 0, 0.5)
pos = jitter(np.ones(len(acPopStat))*1, 0.20)
axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=0.5)
medline(np.median(acPopStat), 1, 0.5)


tickLabels = ['ATh\nv\nStr', 'AC\nv\nAStr']
axSummary.set_xticks(range(2))
axSummary.set_xticklabels(tickLabels)
axSummary.set_xlim([-0.5, 1.5])
extraplots.boxoff(axSummary)
axSummary.set_yticks(np.unique(thalPopStat))
axSummary.set_yticklabels(possibleFreqLabels)
# axSummary.set_ylim([-0.001, 0.161])


# yDataMax = max([max(acPopStat), max(thalPopStat)])
# yStars = yDataMax + yDataMax*starYfactor
# yStarHeight = (yDataMax*starYfactor)*starHeightFactor
extraplots.new_significance_stars([0, 1], np.log(170), np.log(1.1), starMarker='*',
                                    fontSize=fontSizeStars, gapFactor=starGapFactor)
axSummary.set_ylim([np.log(3.6), np.log(150)])
axSummary.set_ylabel('Highest AM sync. rate (Hz)', labelpad=-5)
plt.hold(1)

################### Percent non-sync #####################
axSummary = plt.subplot(gs[0, 5])

popStatCol = 'highestSyncCorrected'
acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
acPopStat = acPopStat[pd.notnull(acPopStat)]
thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]
thalPopStat = thalPopStat[pd.notnull(thalPopStat)]

acSyncN = len(acPopStat[acPopStat > 0])
acNonSyncN = len(acPopStat[acPopStat == 0])
acSyncPercent = acSyncN/float(acSyncN + acNonSyncN) * 100
acNonSyncPercent = acNonSyncN/float(acSyncN + acNonSyncN) * 100

thalSyncN = len(thalPopStat[thalPopStat > 0])
thalNonSyncN = len(thalPopStat[thalPopStat == 0])
thalSyncPercent = thalSyncN/float(thalSyncN + thalNonSyncN)*100
thalNonSyncPercent = thalNonSyncN/float(thalSyncN + thalNonSyncN)*100

width = 0.5
plt.hold(1)
loc = [1, 2]
axSummary.bar(loc[0]-width/2, thalNonSyncPercent, width, color=colorATh)
axSummary.bar(loc[0]-width/2, thalSyncPercent, width, bottom=thalNonSyncPercent, color=colorATh, alpha=0.5)
axSummary.bar(loc[1]-width/2, acNonSyncPercent, width, color=colorAC)
axSummary.bar(loc[1]-width/2, acSyncPercent, width, bottom=acNonSyncPercent, color=colorAC, alpha=0.5)
extraplots.boxoff(axSummary)

extraplots.new_significance_stars([1, 2], 105, 2.5, starMarker='*',
                                    fontSize=fontSizeStars, gapFactor=starGapFactor)

axSummary.text(2.65, 30, 'Non-Sync.', rotation=90, fontweight='bold')
axSummary.text(2.65, 75, 'Sync.', rotation=90, fontweight='bold', color='0.5')

axSummary.set_xlim([0.5, 2.6])
# extraplots.boxoff(axSummary)
axSummary.set_ylim([0, 100.5])
axSummary.set_xticks([1, 2])
tickLabels = ['ATh\nv\nStr', 'AC\nv\nAStr']
axSummary.set_xticklabels(tickLabels)
axSummary.set_ylabel('% neurons', labelpad=-5)


##########################################################


plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
