"""
An annotated versio of figure_am for personal review
comments are placed above section of code they refer to
Devin Henderling - 2020-08-22
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from scipy import stats
import figparams
import studyparams

FIGNAME = 'figure_am'
# Devin - Where to put output 
outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# outputDir = '/var/tmp/figuresdata/2019astrpi/output'
# Devin - Setting where to get data from 
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# Devin - sets predictable random numbers (the same each time script run)
np.random.seed(1)

messages = []

# Function for creating random variation in panes E and F
def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

# Devin - Function for black bars on panes C,E,F
def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

# Devin - Turns on or off each panel (2nd/4th panels not used becaue only one example cell now)
PANELS = [1, 1, 1, 1, 1, 1, 1]

# Devin - sets file name and format 
SAVE_FIGURE = 1
# outputDir = '/tmp/'
figFilename = 'figure_am_tuning'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'

# Devin - sets dimensions of figure 
fullPanelWidthInches = 6.9
figSizeFactor = 2
figWidth = fullPanelWidthInches * figSizeFactor
figHeight = figWidth / 1.625
figSize = [figWidth, figHeight]  # In inches


#thalHistColor = '0.4'
#acHistColor = '0.4'

# Devin - Font size adjusted for figure size 
fontSizeLabels = figparams.fontSizeLabels * figSizeFactor
fontSizeTicks = figparams.fontSizeTicks * figSizeFactor
fontSizePanel = figparams.fontSizePanel * figSizeFactor
fontSizeTitles = 12

# Params for extraplots significance stars
fontSizeNS = figparams.fontSizeNS
fontSizeStars = figparams.fontSizeStars
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor
dotEdgeColor = figparams.dotEdgeColor
dataMS = 6

labelPosX = [0.02, 0.35, 0.68, 0.85]   # Horiz position for panel labels
labelPosY = [0.46, 0.96]    # Vert position for panel labels

# Devin - cp is jaratoolbox colorpalette
# Define colors, use figparams
#laserColor = figparams.colp['blueLaser']
#colorD1 = figparams.cp.TangoPalette['SkyBlue2']
#colornD1 = figparams.cp.TangoPalette['ScarletRed1']

laserColor = figparams.colp['blueLaser']
colorD1 = figparams.colp['D1']
colornD1 = figparams.colp['nD1']

# Devin - creates figure object, Clears figure, and sets background color 
fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

# Devin - sets the grid for the panels and the edge spacing  
gs = gridspec.GridSpec(2, 5)  # Reduced from 2x6 to 2x5 after removing one example cell for each cell group
gs.update(left=0.05, right=0.98, top=0.94, bottom=0.10, wspace=0.8, hspace=0.5)

# Load example data
exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath, allow_pickle=True)

# Devin - Sets variables for frequencies and spikes for each trial
exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

# Devin - Places each panel in grid
gsPanelA = gs[0, 0:3]
# gsPanelB = gs[0, 2:4]
gsPanelC = gs[0, 3]
gsPanelD = gs[0, 4]
gsPanelE = gs[1, 0:3]
# gsPanelF = gs[1, 2:4]
gsPanelG = gs[1, 3]
gsPanelH = gs[1, 4]

# Devin - Makes raster plots with firing rate averages on side 
def plot_example_with_rate(subplotSpec, exampleName, color='k'):
    fig = plt.gcf()

    # Devin - Creates a subgrid that is 1 by 4
    sub_gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=subplotSpec, wspace=-0.45, hspace=0.0)
    
    # Devin - Assigns location for raster plot
    specRaster = sub_gs[0:2]
    # Devin = Creates a axis object for raster plot and adds it to figure 
    axRaster = plt.Subplot(fig, specRaster)
    fig.add_subplot(axRaster)

    # Devin = Sets spikes for raster 
    spikeTimes = exampleSpikeTimes[exampleName]
    # Devin NOT SURE YET 
    indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
    # Devin = Sets range of times for raster 
    timeRange = [-0.2, 0.7]
    # Devin - Sets frequency for each trial 
    freqEachTrial = exampleFreqEachTrial[exampleName]
    # Devin - create array of frequencies presented 
    possibleFreq = np.unique(freqEachTrial)
    # Devin - Labels the frequecies 
    freqLabels = ['{0:.0f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)
    pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
                                                   timeRange, trialsEachCondition, labels=freqLabels)
    # Devin - Sets markersize
    plt.setp(pRaster, ms=figparams.rasterMS)
    # Devin - sets y-axis labels for raster
    blankLabels = ['']*11
    for labelPos in [0, 5, 10]:
        blankLabels[labelPos] = freqLabels[labelPos]
    axRaster.set_yticklabels(blankLabels)

    # Devin - Sets x ticks and axis labels 
    ax = plt.gca()
    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from\nsound onset (s)', fontsize=fontSizeLabels, labelpad=-1)
    ax.set_ylabel('AM rate (Hz)', fontsize=fontSizeLabels, labelpad=-5)

    #ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
    #             fontsize=fontSizePanel, fontweight='bold')

    countRange = [0.1, 0.5]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes, indexLimitsEachTrial, countRange)
    numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)
    numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                       axis=0))
    # Devin = Checks if num spikes is longer than number of trials 
    if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
        numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]
    # Devin - finds average firing rate for raster plot     
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
    # Devin - Plots the average chart 
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

# Devin - Creates the first panel (top left) raster/firing rate, labels panel, adds A letter, sets ticks/labels
if PANELS[0]:
    (axDirectCellEx1, axDirectFREx1) = plot_example_with_rate(gsPanelA, 'Direct1', color=colorD1)
    axDirectCellEx1.set_title('Direct pathway example 1', fontsize=fontSizeTitles)
    axDirectFREx1.set_xlim([0, 75])
    axDirectFREx1.set_xticks([0, 75])
    extraplots.set_ticks_fontsize(axDirectFREx1, fontSizeTicks)
    extraplots.set_ticks_fontsize(axDirectCellEx1, fontSizeTicks)
    axDirectCellEx1.annotate('A', xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# Went down to one example cell each for D1/nD1 instead of two, so this is being commented out
# if PANELS[1]:
#     (axDirectCellEx2, axDirectFREx2) = plot_example_with_rate(gsPanelB, 'Direct2', color=colorD1)
#     axDirectCellEx2.set_title('Direct pathway example 2', fontsize=fontSizeTitles)
#     axDirectFREx2.set_xlim([0, 15])
#     axDirectFREx2.set_xticks([0, 15])
#     extraplots.set_ticks_fontsize(axDirectFREx2, fontSizeTicks)
#     extraplots.set_ticks_fontsize(axDirectCellEx2, fontSizeTicks)
#     axDirectCellEx2.annotate('B', xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
#                              fontsize=fontSizePanel, fontweight='bold')

if PANELS[2]:
    (axNonDirectEx1, axNonDirectFREx1) = plot_example_with_rate(gsPanelE, 'nDirect1', color=colornD1)
    axNonDirectEx1.set_title('Non-direct pathway example 1', fontsize=fontSizeTitles)
    axNonDirectFREx1.set_xlim([0, 75])
    axNonDirectFREx1.set_xticks([0, 75])
    extraplots.set_ticks_fontsize(axNonDirectFREx1, fontSizeTicks)
    extraplots.set_ticks_fontsize(axNonDirectEx1, fontSizeTicks)
    axNonDirectEx1.annotate('D', xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
                            fontsize=fontSizePanel, fontweight='bold')
    (axNonDirectEx1, axNonDirectFREx1) = plot_example_with_rate(gsPanelE, 'nDirect1', color=colornD1)
    axNonDirectEx1.set_title('Non-direct pathway example 1', fontsize=fontSizeTitles)
    axNonDirectFREx1.set_xlim([0, 75])
    axNonDirectFREx1.set_xticks([0, 75])
    extraplots.set_ticks_fontsize(axNonDirectFREx1, fontSizeTicks)
    extraplots.set_ticks_fontsize(axNonDirectEx1, fontSizeTicks)
    axNonDirectEx1.annotate('D', xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
                            fontsize=fontSizePanel, fontweight='bold')
# Went down to one example cell each for D1/nD1 instead of two, so this is being commented out
# if PANELS[3]:
#     (axNonDirectEx2, axNonDirectFREx2) = plot_example_with_rate(gsPanelF, 'nDirect2', color=colornD1)
#     axNonDirectEx2.set_title('Non-direct pathway example 2', fontsize=fontSizeTitles)
#     axNonDirectFREx2.set_xlim([0, 25])
#     axNonDirectFREx2.set_xticks([0, 25])
#     extraplots.set_ticks_fontsize(axNonDirectFREx2, fontSizeTicks)
#     extraplots.set_ticks_fontsize(axNonDirectEx2, fontSizeTicks)
#     axNonDirectFREx2.annotate('F', xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
#                               fontsize=fontSizePanel, fontweight='bold')

# ---------------- Highest Sync -------------------

# Devin - Plots top right stuff (pie chart + scatter plot)
if PANELS[4]:
    popStatCol = 'highestSyncCorrected'
    D1PopStat = exampleData["D1_{}".format(popStatCol)]
    nD1PopStat = exampleData["nD1_{}".format(popStatCol)]
    ytickLabels = [4, 8, 16, 32, 64, 128]
    yticks = np.log(ytickLabels)

    # axSummary = plt.subplot(gs[0, 5])
    # Devin - Sets spacing between points on very top right figure (scatter plot) 
    spacing = 0.07
    # plt.sca(axSummary)
    axPanelD = plt.subplot(gsPanelD)
    plt.sca(axPanelD)

    # pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
    # axSummary.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=0.5)
    markers = extraplots.spread_plot(0, D1PopStat, spacing)
    plt.setp(markers, mec=colorD1, mfc='None')
    plt.setp(markers, ms=dataMS)

    medline(np.median(D1PopStat), 0, 0.5)

    # pos = jitter(np.ones(len(acPopStat))*1, 0.20)
    # axSummary.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=0.5)
    # Devin - Places markers 
    markers = extraplots.spread_plot(1, nD1PopStat, spacing)
    plt.setp(markers, mec=colornD1, mfc='None')
    plt.setp(markers, ms=dataMS)

    medline(np.median(nD1PopStat), 1, 0.5)

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
    # Devin - Puts n.s graphic on top of scatter 
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
    # Devin - Adds boxes next to labels for each pie chart section
    rect1 = mpatches.Rectangle(xy=(rectX, rectY[0]), width=rectWidth, height=rectHeight, fc='w', ec='k', clip_on=False,
                               transform=axnD1Pie.transAxes)
    rect2 = mpatches.Rectangle(xy=(rectX, rectY[1]), width=rectWidth, height=rectHeight, fc='k', ec='k', clip_on=False,
                               transform=axnD1Pie.transAxes)

    axnD1Pie.add_patch(rect1)
    axnD1Pie.add_patch(rect2)

    nD1SyncFrac = exampleData['nD1_pieSync']
    nD1NonSyncFrac = exampleData["nD1_pieNonSync"]
    pieWedges = axnD1Pie.pie([nD1NonSyncFrac, nD1SyncFrac], colors=['w', colornD1], shadow=False, startangle=0)
    for wedge in pieWedges[0]:
        wedge.set_edgecolor(colornD1)

    # axACPie.annotate('Non-Sync\n{}%'.format(int(100*acNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
    # axACPie.annotate('Sync\n{}%'.format(int(100*acSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
    fontSizePercent = 12
    axnD1Pie.annotate('{:0.0f}%'.format(np.round(100 * nD1NonSyncFrac)), xy=[0.48, 0.6], rotation=0,
                      fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
    axnD1Pie.annotate('{:0.0f}%'.format(np.round(100 * nD1SyncFrac)), xy=[0.25, 0.25], rotation=0,
                      fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
    axnD1Pie.set_aspect('equal')

    D1SyncFrac = exampleData["D1_pieSync"]
    D1NonSyncFrac = exampleData["D1_pieNonSync"]

    pieWedges = axD1Pie.pie([D1NonSyncFrac, D1SyncFrac], colors=['w', colorD1], shadow=False, startangle=0)
    for wedge in pieWedges[0]:
        wedge.set_edgecolor(colorD1)

    # axThalPie.annotate('Non-Sync\n{}%'.format(int(100*thalNonSyncFrac)), xy=[0.8, 0.8], rotation=0, fontweight='bold', textcoords='axes fraction')
    # axThalPie.annotate('Sync\n{}%'.format(int(100*thalSyncFrac)), xy=[-0.05, -0.05], rotation=0, fontweight='bold', textcoords='axes fraction')
    axD1Pie.annotate('{:0.0f}%'.format(np.round(100 * D1NonSyncFrac)), xy=[0.57, 0.525], rotation=0,
                     fontweight='regular', textcoords='axes fraction', fontsize=fontSizePercent)
    axD1Pie.annotate('{:0.0f}%'.format(np.round(100 * D1SyncFrac)), xy=[0.2, 0.3], rotation=0,
                     fontweight='bold', textcoords='axes fraction', fontsize=fontSizePercent, color='w')
    axD1Pie.set_aspect('equal')

    D1SyncN = exampleData["D1_pieSyncN"]
    D1NonSyncN = exampleData["D1_pieNonSyncN"]
    nD1SyncN = exampleData["nD1_pieSyncN"]
    nD1NonSyncN = exampleData["nD1_pieNonSyncN"]

    oddsratio, pValue = stats.fisher_exact([[nD1SyncN, D1SyncN],
                                            [nD1NonSyncN, D1NonSyncN]])
    print("nD1: {} Nonsync / {} total".format(nD1NonSyncN, nD1SyncN + nD1NonSyncN))
    print("D1: {} Nonsync / {} total".format(D1NonSyncN, D1SyncN + D1NonSyncN))
    print("p-Val for fisher exact test: {}".format(pValue))
    if pValue < 0.05:
        starMarker = '*'
    else:
        starMarker = 'n.s.'
    
    # Devin - Places the pane titles for B-F
    axD1Pie.annotate('B', xy=(labelPosX[2], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axD1Pie.annotate('C', xy=(labelPosX[3], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axD1Pie.annotate('E', xy=(0.64, labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axD1Pie.annotate('F', xy=(labelPosX[3], labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    xBar = -2
    # FarUntagged, CloseUntagged, tagged
    yCircleCenters = [0, 3]
    xTickWidth = 0.2
    yGapWidth = 0.5

# ---------------- Discrimination of Rate ----------------
if PANELS[5]:

    popStatCol = 'rateDiscrimAccuracy'
    D1PopStat = exampleData["D1_{}".format(popStatCol)]
    nD1PopStat = exampleData["nD1_{}".format(popStatCol)]

    # plt.clf()
    # axSummary = plt.subplot(111)
    axPanelG = plt.subplot(gsPanelG)
    plt.sca(axPanelG)
    
    # Devin - Sets randomness of how points are placed on pane E
    jitterFrac = 0.2
    pos = jitter(np.ones(len(D1PopStat)) * 0, jitterFrac)
    axPanelG.plot(pos, D1PopStat, 'o', mec=colorD1, mfc='None', alpha=1, ms=dataMS)
    # Devin - Places median lines on panes C,E,F
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
    # plt.hold(1)


# -------------Discrimination of Phase -------------------
if PANELS[6]:
    D1MeanPerCell = exampleData["D1_phaseDiscrimAccuracy"]
    nD1MeanPerCell = exampleData["nD1_phaseDiscrimAccuracy"]

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
    axPanelH.set_ylim([0.5, 1])
    yticks = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
    axPanelH.set_yticks(yticks)
    ytickLabels = ['50', '', '', '', '', '100']
    axPanelH.set_yticklabels(ytickLabels)
    # axSummary.set_yticklabels(map(str, [50, 60, 70, 80, 90, 100]))
    axPanelH.set_ylabel('Discrimination accuracy\nof AM phase (%)', fontsize=fontSizeLabels, labelpad=-12)


    zstat, pVal = stats.mannwhitneyu(D1MeanPerCell, nD1MeanPerCell)

    messages.append("{} p={}".format("Phase discrimination accuracy", pVal))
    messages.append("{} D1 n={}, nD1 n={}".format("Phase discrimination accuracy", len(D1PopStat), len(nD1PopStat)))

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

print("\nSTATISTICS:\n")
for message in messages:
    print(message)
print("\n")

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
plt.show()
