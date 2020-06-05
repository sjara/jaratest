import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase
from scipy import stats
import pandas as pd
import figparams
import studyparams

FIGNAME = 'figure_am'
d1mice = studyparams.ASTR_D1_CHR2_MICE
nameDB = '{}.h5'.format('direct_and_indirect_cells')
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
db = celldatabase.load_hdf(pathtoDB)
zDB = db.query(studyparams.LABELLED_Z)
zDB2 = db[db['z_coord'].isnull()]
zDBt = pd.concat([zDB, zDB2], axis=0, ignore_index=True, sort=False)
db = zDBt.query(studyparams.BRAIN_REGION_QUERY)

D1 = db.query(studyparams.D1_CELLS)
nD1 = db.query(studyparams.nD1_CELLS)
D1 = D1.query(studyparams.AM_FILTER)
nD1 = nD1.query(studyparams.AM_FILTER)

outputDir = '/var/tmp/figuresdata/2019astrpi/output'

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME, 'data_AM_tuning_examples.npz')
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)

np.random.seed(1)

messages = []


def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr


def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)


PANELS = [0, 1, 0, 1, 1, 1, 1]

SAVE_FIGURE = 1
# outputDir = '/tmp/'
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
# outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_am_tuning_symposium'  # Do not include extension
# figFormat = 'svg'  # 'pdf' or 'svg'
figFormat = 'png'  # 'pdf' or 'svg'
# figSize = [13,8] # In inches

fullPanelWidthInches = 6.9
figSizeFactor = 3.5
figWidth = 17.25
figHeight = figWidth / 1.625
figSize = [figWidth, figHeight]  # In inches


thalHistColor = '0.4'
acHistColor = '0.4'

sympSize = 22
fontSizeLabels = sympSize
fontSizeTicks = sympSize
fontSizePanel = sympSize
fontSizeTitles = sympSize

# Params for extraplots significance stars
fontSizeNS = 16
fontSizeStars = 16
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor
dotEdgeColor = figparams.dotEdgeColor
dataMS = 12

labelPosX = [0.02, 0.02, 0.54, 0.80]   # Horiz position for panel labels
labelPosY = [0.46, 0.96]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']
colorD1 = figparams.cp.TangoPalette['SkyBlue2']
colornD1 = figparams.cp.TangoPalette['ScarletRed1']

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.05, right=0.98, top=0.94, bottom=0.10, wspace=0.8, hspace=0.5)

# Load example data
exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath, allow_pickle=True)

exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

gsPanelB = gs[0, 0:2]
gsPanelC = gs[0, 2]
gsPanelD = gs[0, 3]
gsPanelF = gs[1, 0:2]
gsPanelG = gs[1, 2]
gsPanelH = gs[1, 3]


def plot_example_with_rate(subplotSpec, exampleName, color='k'):
    fig = plt.gcf()

    sub_gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=subplotSpec, wspace=-0.45, hspace=0.0)

    specRaster = sub_gs[0:2]
    axRaster = plt.Subplot(fig, specRaster)
    fig.add_subplot(axRaster)

    spikeTimes = exampleSpikeTimes[exampleName]
    indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
    timeRange = [-0.2, 0.7]
    freqEachTrial = exampleFreqEachTrial[exampleName]
    possibleFreq = np.unique(freqEachTrial)
    freqLabels = ['{0:.0f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)
    pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
                                                   timeRange, trialsEachCondition, labels=freqLabels)
    plt.setp(pRaster, ms=3)

    blankLabels = ['']*11
    for labelPos in [0, 5, 10]:
        blankLabels[labelPos] = freqLabels[labelPos]

    axRaster.set_yticklabels(blankLabels)

    ax = plt.gca()
    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from\nsound onset (s)', fontsize=fontSizeLabels, labelpad=-1)
    ax.set_ylabel('AM rate (Hz)', fontsize=fontSizeLabels, labelpad=-15)
    plt.setp(zline, linewidth=4)

    # ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')

    countRange = [0.1, 0.5]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes, indexLimitsEachTrial, countRange)
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

    specRate = sub_gs[3]
    axRate = plt.Subplot(fig, specRate)
    fig.add_subplot(axRate)

    nRates = len(possibleFreq)
    # plt.hold(True)
    plt.plot(avgSpikesArray, range(nRates), 'ro-', mec='none', ms=6, lw=3, color=color)
    plt.plot(avgSpikesArray-stdSpikesArray, range(len(possibleFreq)), 'k:')
    plt.plot(avgSpikesArray+stdSpikesArray, range(len(possibleFreq)), 'k:')
    axRate.set_ylim([-0.5, nRates-0.5])
    axRate.set_yticks(range(nRates))
    axRate.set_yticklabels([])

    # ax = plt.gca()
    axRate.set_xlabel('Firing rate\n(spk/s)', fontsize = fontSizeLabels, labelpad=-1)
    extraplots.boxoff(axRate)
    # extraplots.boxoff(ax, keep='right')
    return axRaster, axRate


if PANELS[1]:
    (axDirectCellEx2, axDirectFREx2) = plot_example_with_rate(gsPanelB, 'Direct2', color=colorD1)
    axDirectCellEx2.set_title('Direct pathway example', fontsize=fontSizeTitles)
    axDirectFREx2.set_xlim([0, 15])
    axDirectFREx2.set_xticks([0, 15])
    extraplots.set_ticks_fontsize(axDirectFREx2, fontSizeTicks)
    extraplots.set_ticks_fontsize(axDirectCellEx2, fontSizeTicks)
    axDirectCellEx2.annotate('A', xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

if PANELS[3]:
    (axNonDirectEx2, axNonDirectFREx2) = plot_example_with_rate(gsPanelF, 'nDirect2', color=colornD1)
    axNonDirectEx2.set_title('Non-direct pathway example', fontsize=fontSizeTitles)
    axNonDirectFREx2.set_xlim([0, 25])
    axNonDirectFREx2.set_xticks([0, 25])
    extraplots.set_ticks_fontsize(axNonDirectFREx2, fontSizeTicks)
    extraplots.set_ticks_fontsize(axNonDirectEx2, fontSizeTicks)
    axNonDirectFREx2.annotate('D', xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
                              fontsize=fontSizePanel, fontweight='bold')

# ---------------- Highest Sync -------------------

if PANELS[4]:
    popStatCol = 'highestSyncCorrected'
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]

    nD1PopStat = nD1PopStat[nD1PopStat > 0]
    D1PopStat = D1PopStat[D1PopStat > 0]

    # possibleFreqLabels = ["{0:.1f}".format(freq) for freq in np.unique(thalPopStat)]
    ytickLabels = [4, 8, 16, 32, 64, 128]
    yticks = np.log(ytickLabels)

    nD1PopStat = np.log(nD1PopStat)
    D1PopStat = np.log(D1PopStat)

    # axSummary = plt.subplot(gs[0, 5])
    spacing = 0.07
    # plt.sca(axSummary)
    axPanelD = plt.subplot(gsPanelD)
    plt.sca(axPanelD)

    # pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
    # axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=0.5)
    # plt.hold(1)
    markers = extraplots.spread_plot(0, D1PopStat, spacing)
    plt.setp(markers, mec=colorD1, mfc='None')
    plt.setp(markers, ms=dataMS)

    # plt.hold(1)
    medline(np.median(D1PopStat), 0, 0.5)
    # plt.hold(1)

    # pos = jitter(np.ones(len(acPopStat))*1, 0.20)
    # axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=0.5)
    markers = extraplots.spread_plot(1, nD1PopStat, spacing)
    plt.setp(markers, mec=colornD1, mfc='None')
    plt.setp(markers, ms=dataMS)

    # plt.hold(1)
    medline(np.median(nD1PopStat), 1, 0.5)
    # plt.hold(1)

    axPanelD.set_yticks(yticks)
    axPanelD.set_yticklabels(ytickLabels)

    # tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
    tickLabels = ['D1\nn={}'.format(len(D1PopStat)), 'nD1\nn={}'.format(len(nD1PopStat))]
    axPanelD.set_xticks(range(2))
    axPanelD.set_xticklabels(tickLabels, rotation=45)
    axPanelD.set_xlim([-0.5, 1.5])
    extraplots.set_ticks_fontsize(axPanelD, fontSizeLabels)
    extraplots.boxoff(axPanelD)
    # axSummary.set_yticks(np.unique(thalPopStat))
    # axSummary.set_yticklabels(possibleFreqLabels)
    # axSummary.set_ylim([-0.001, 0.161])

    yDataMax = max([max(nD1PopStat), max(D1PopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor

    zVal, pVal = stats.mannwhitneyu(D1PopStat, nD1PopStat)
    messages.append("{} p={}".format(popStatCol, pVal))
    # if pVal < 0.05:
    #     extraplots.new_significance_stars([0, 1], np.log(170), np.log(1.1), starMarker='*',
    #                                         fontSize=fontSizeStars, gapFactor=starGapFactor)
    # else:
    #     extraplots.new_significance_stars([0, 1], np.log(170), np.log(1.1), starMarker='n.s.',
    #                                         fontSize=fontSizeStars, gapFactor=starGapFactor)
    starString = None if pVal < 0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)

    axPanelD.set_ylim([np.log(3.6), np.log(150)])
    axPanelD.set_ylabel('Highest AM sync. rate (Hz)', labelpad=-1, fontsize=fontSizeLabels)
   #  plt.hold(1)

    # ---------------- Percent non-sync --------------------
    # axSummary = plt.subplot(gs[0, 5])
    axPanelC = plt.subplot(gsPanelC)
    plt.sca(axPanelC)
    pieChartGS = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gsPanelC)

    axD1Pie = plt.subplot(pieChartGS[0, 0])
    axnD1Pie = plt.subplot(pieChartGS[1, 0])

    annotateX = 0.2
    annotateY = np.array([-0.3, -0.45]) + 0.1
    rectX = annotateX-0.2
    # rectY = [0.5825, 0.55]
    rectY = annotateY
    rectWidth = 0.15
    rectHeight = 0.1

    # TODO: Move these to the axis transform
    axnD1Pie.annotate('Unsynchronized', xy=(annotateX, annotateY[0]), xycoords='axes fraction', fontsize=fontSizeTicks - 2)
    axnD1Pie.annotate('Synchronized', xy=(annotateX, annotateY[1]), xycoords='axes fraction', fontsize=fontSizeTicks - 2)

    fig = plt.gcf()
    rect1 = mpatches.Rectangle(xy=(rectX, rectY[0]), width=rectWidth, height=rectHeight, fc='w', ec='k', clip_on=False,
                               transform=axnD1Pie.transAxes)
    rect2 = mpatches.Rectangle(xy=(rectX, rectY[1]), width=rectWidth, height=rectHeight, fc='k', ec='k', clip_on=False,
                               transform=axnD1Pie.transAxes)

    axnD1Pie.add_patch(rect1)
    axnD1Pie.add_patch(rect2)

    popStatCol = 'highestSyncCorrected'
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
    nD1PopStat = nD1PopStat[pd.notnull(nD1PopStat)]
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]
    D1PopStat = D1PopStat[pd.notnull(D1PopStat)]

    nD1SyncN = len(nD1PopStat[nD1PopStat > 0])
    nD1NonSyncN = len(nD1PopStat[nD1PopStat == 0])
    nD1SyncFrac = nD1SyncN / float(nD1SyncN + nD1NonSyncN)
    nD1NonSyncFrac = nD1NonSyncN / float(nD1SyncN + nD1NonSyncN)

    pieWedges = axnD1Pie.pie([nD1NonSyncFrac, nD1SyncFrac], colors=['w', colornD1], shadow=False, startangle=0)
    for wedge in pieWedges[0]:
        wedge.set_edgecolor(colornD1)

    # axACPie.annotate('Non-Sync\n{}%'.format(int(100*acNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
    # axACPie.annotate('Sync\n{}%'.format(int(100*acSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
    fontSizePercent = 22
    axnD1Pie.annotate('{:0.0f}%'.format(np.round(100 * nD1NonSyncFrac)), xy=[0.4, 0.6], rotation=0,
                      fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
    axnD1Pie.annotate('{:0.0f}%'.format(np.round(100 * nD1SyncFrac)), xy=[0.25, 0.25], rotation=0,
                      fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
    axnD1Pie.set_aspect('equal')

    D1SyncN = len(D1PopStat[D1PopStat > 0])
    D1NonSyncN = len(D1PopStat[D1PopStat == 0])
    D1SyncFrac = D1SyncN / float(D1SyncN + D1NonSyncN)
    D1NonSyncFrac = D1NonSyncN / float(D1SyncN + D1NonSyncN)

    pieWedges = axD1Pie.pie([D1NonSyncFrac, D1SyncFrac], colors=['w', colorD1], shadow=False, startangle=0)
    for wedge in pieWedges[0]:
        wedge.set_edgecolor(colorD1)

    # axThalPie.annotate('Non-Sync\n{}%'.format(int(100*thalNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
    # axThalPie.annotate('Sync\n{}%'.format(int(100*thalSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
    axD1Pie.annotate('{:0.0f}%'.format(np.round(100 * D1NonSyncFrac)), xy=[0.4, 0.55], rotation=0,
                     fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
    axD1Pie.annotate('{:0.0f}%'.format(np.round(100 * D1SyncFrac)), xy=[0.3, 0.25], rotation=0,
                     fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
    axD1Pie.set_aspect('equal')

    oddsratio, pValue = stats.fisher_exact([[nD1SyncN, D1SyncN],
                                            [nD1NonSyncN, D1NonSyncN]])
    print("nD1: {} Nonsync / {} total".format(nD1NonSyncN, nD1SyncN + nD1NonSyncN))
    print("D1: {} Nonsync / {} total".format(D1NonSyncN, D1SyncN + D1NonSyncN))
    print("p-Val for fisher exact test: {}".format(pValue))
    if pValue < 0.05:
        starMarker = '*'
    else:
        starMarker = 'n.s.'

    axD1Pie.annotate('B', xy=(labelPosX[2], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axD1Pie.annotate('C', xy=(labelPosX[3], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    xBar = -2
    # FarUntagged, CloseUntagged, tagged
    yCircleCenters = [0, 3]
    xTickWidth = 0.2
    yGapWidth = 0.5

# ---------------- Discrimination of Rate ----------------
if PANELS[5]:
    # dbPathRate = os.path.join(dataDir, 'celldatabase_with_am_discrimination_accuracy.h5')
    # dbPathRate = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
    # dataframeRate = pd.read_hdf(dbPathRate, key='dataframe')
    # dataframeRate = celldatabase.load_hdf(dbPathRate)

    # -------- Future things I could calculate and filter by similar to what Nick did --------
    # goodISIRate = dataframeRate.query('isiViolations<0.02 or modifiedISI<0.02')
    # goodShapeRate = goodISIRate.query('spikeShapeQuality > 2')
    # goodLaserRate = goodShapeRate.query("autoTagged==1 and subject != 'pinp018'")
    # goodNSpikesRate = goodLaserRate.query('nSpikes>2000')
    # goodPulseLatency = goodNSpikesRate.query('summaryPulseLatency<0.01')
    # dbToUse = goodPulseLatency

    # nD1Rate = nD1.groupby('brainArea').get_group('rightAC')
    # D1Rate = D1.groupby('brainArea').get_group('rightThal')

    popStatCol = 'rateDiscrimAccuracy'
    # popStatCol = 'accuracySustained'
    nD1PopStat = nD1[popStatCol][pd.notnull(nD1[popStatCol])]
    D1PopStat = D1[popStatCol][pd.notnull(D1[popStatCol])]

    # plt.clf()
    # axSummary = plt.subplot(111)
    axPanelG = plt.subplot(gsPanelG)
    plt.sca(axPanelG)

    jitterFrac = 0.2
    pos = jitter(np.ones(len(D1PopStat)) * 0, jitterFrac)
    axPanelG.plot(pos, D1PopStat, 'o', mec=colorD1, mfc='None', alpha=1, ms=dataMS)
    medline(np.median(D1PopStat), 0, 0.5)
    pos = jitter(np.ones(len(nD1PopStat)) * 1, jitterFrac)
    axPanelG.plot(pos, nD1PopStat, 'o', mec=colornD1, mfc='None', alpha=1, ms=dataMS)
    medline(np.median(nD1PopStat), 1, 0.5)
    tickLabels = ['D1\nn={}'.format(len(D1PopStat)), 'nD1\nn={}'.format(len(nD1PopStat))]
    axPanelG.set_xticks(range(2))
    axPanelG.set_xticklabels(tickLabels, rotation=45)
    extraplots.set_ticks_fontsize(axPanelG, fontSizeLabels)
    axPanelG.set_ylim([0.5, 1])
    yticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
    axPanelG.set_yticks(yticks)
    ytickLabels = ['50', '', '', '', '', '100']
    axPanelG.set_yticklabels(ytickLabels)
    axPanelG.set_ylabel('Discrimination accuracy\nof AM rate (%)', fontsize=fontSizeLabels, labelpad=-12)
    # extraplots.set_ticks_fontsize(axSummary, fontSizeLabels)

    zstat, pVal = stats.mannwhitneyu(D1PopStat, nD1PopStat)

    messages.append("{} p={}".format("Rate discrimination accuracy", pVal))
    messages.append("{} D1 n={}, nD1 n={}".format(popStatCol, len(D1PopStat), len(nD1PopStat)))

    # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

    # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')

    # starHeightFactor = 0.2
    # starGapFactor = 0.3
    # starYfactor = 0.1
    yDataMax = max([max(nD1PopStat), max(D1PopStat)]) - 0.025
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor

    starString = None if pVal < 0.05 else 'n.s.'
    # fontSizeStars = 9
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)
    extraplots.boxoff(axPanelG)
    axPanelG.annotate('E', xy=(labelPosX[2], labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    # plt.hold(1)


# -------------Discrimination of Phase -------------------
if PANELS[6]:
    # dbPathPhase = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
    # # dbPhase = pd.read_hdf(dbPathPhase, key='dataframe')
    # dbPhase = celldatabase.load_hdf(dbPathPhase)

    # -------- Filters I could calculate and add if we think it is necessary ------
    # goodISIPhase = dbPhase.query('isiViolations<0.02 or modifiedISI<0.02')
    # goodShapePhase = goodISIPhase.query('spikeShapeQuality > 2')
    # goodLaserPhase = goodShapePhase.query("autoTagged==1 and subject != 'pinp018'")
    # goodNSpikesPhase = goodLaserPhase.query('nSpikes>2000')

    possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
    ratesToUse = possibleRateKeys
    keys = ['phaseDiscrimAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

    nD1Data = np.full((len(nD1), len(ratesToUse)), np.nan)
    D1Data = np.full((len(D1), len(ratesToUse)), np.nan)

    for externalInd, (indRow, row) in enumerate(nD1.iterrows()):
        for indKey, key in enumerate(keys):
            nD1Data[externalInd, indKey] = row[key]

    for externalInd, (indRow, row) in enumerate(D1.iterrows()):
        for indKey, key in enumerate(keys):
            D1Data[externalInd, indKey] = row[key]

    nD1MeanPerCell = np.nanmean(nD1Data, axis=1)
    nD1MeanPerCell = nD1MeanPerCell[~np.isnan(nD1MeanPerCell)]
    D1MeanPerCell = np.nanmean(D1Data, axis=1)
    D1MeanPerCell = D1MeanPerCell[~np.isnan(D1MeanPerCell)]

    # plt.clf()

    # axSummary = plt.subplot(gs[1, 5])
    axPanelH = plt.subplot(gsPanelH)

    jitterFrac = 0.2
    pos = jitter(np.ones(len(D1MeanPerCell)) * 0, jitterFrac)
    axPanelH.plot(pos, D1MeanPerCell, 'o', mec=colorD1, mfc='None', alpha=1, ms=dataMS)
    medline(np.median(D1MeanPerCell), 0, 0.5)
    pos = jitter(np.ones(len(nD1MeanPerCell)) * 1, jitterFrac)
    axPanelH.plot(pos, nD1MeanPerCell, 'o', mec=colornD1, mfc='None', alpha=1, ms=dataMS)
    medline(np.median(nD1MeanPerCell), 1, 0.5)
    tickLabels = ['D1\nn={}'.format(len(D1MeanPerCell)), 'nD1\nn={}'.format(len(nD1MeanPerCell))]
    axPanelH.set_xticks(range(2))
    axPanelH.set_xticklabels(tickLabels, rotation=45)
    extraplots.set_ticks_fontsize(axPanelH, fontSizeLabels)
    axPanelH.set_ylim([0.5, .75])
    yticks = [0.5, 0.55, 0.60, 0.65, 0.7, 0.75]
    axPanelH.set_yticks(yticks)
    ytickLabels = ['50', '', '', '', '', '75']
    axPanelH.set_yticklabels(ytickLabels)
    # axSummary.set_yticklabels(map(str, [50, 60, 70, 80, 90, 100]))
    axPanelH.set_ylabel('Discrimination accuracy\nof AM phase (%)', fontsize=fontSizeLabels, labelpad=-12)


    zstat, pVal = stats.mannwhitneyu(D1MeanPerCell, nD1MeanPerCell)

    messages.append("{} p={}".format("Phase discrimination accuracy", pVal))
    messages.append("{} D1 n={}, nD1 n={}".format("Phase discrimination accuracy", len(D1MeanPerCell), len(nD1MeanPerCell)))

    # plt.title('p = {}'.format(np.round(pVal, decimals=5)))

    # axSummary.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')

    # starHeightFactor = 0.2
    # starGapFactor = 0.3
    # starYfactor = 0.1
    yDataMax = max([max(nD1MeanPerCell), max(D1MeanPerCell)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor

    starString = None if pVal < 0.05 else 'n.s.'
    # fontSizeStars = 9
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)

    extraplots.boxoff(axPanelH)
    axPanelH.annotate('F', xy=(labelPosX[3], labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

print("\nSTATISTICS:\n")
for message in messages:
    print(message)
print("\n")

for axis in [axDirectCellEx2, axDirectFREx2, axNonDirectEx2, axNonDirectFREx2, axPanelC, axPanelD, axPanelH, axPanelG]:
    plt.setp(axis.spines.values(), linewidth=3)
    axis.tick_params(width=3)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir, 'w')
plt.show()
