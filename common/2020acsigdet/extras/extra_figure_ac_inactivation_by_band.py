import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import behaviour_analysis_funcs as bf
import figparams
import studyparams

FIGNAME = 'figure_ac_inactivation'
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 0, 0, 0, 0]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
SIG_CONTROL_REMOVED = 1
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'Fig2_ac_inactivation_new_corrected'  # Do not include extension
else:
    figFilename = 'Fig2_ac_inactivation_new'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,3]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.33, 0.54, 0.77, 0.25, 0.5, 0.77]  # Horiz position for panel labels
labelPosY = [0.95, 0.47]  # Vert position for panel labels

ACInactExample = 'band046_psycurve.npz'
ACInactReactionExample = 'band046_reaction_times.npz'
summaryFileName = 'all_behaviour_ac_inactivation_v2.npz'
reactionTimesFileName = 'all_reaction_times_ac_inactivation.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 4, wspace=0.3, hspace=0.4, width_ratios=[1.0,0.6,0.6, 0.6])
gs.update(top=0.97, bottom=0.15, left=0.08, right=0.98, wspace=0.5, hspace=0.3)

# --- example psychometric curves ---
if PANELS[0]:
    dataFullPath = os.path.join(inactDataDir, ACInactExample)
    data = np.load(dataFullPath)

    psyCurveControl = data['psyCurveControl']
    upperErrorControl = data['upperErrorControl']
    lowerErrorControl = data['lowerErrorControl']
    possibleSNRs = data['possibleSNRs']

    axCurve = plt.subplot(gs[0, 0])
    panelLabel = 'A'
    xTickLabels = ['-inf']
    xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])

    xVals = range(len(possibleSNRs))
    plt.plot(xVals[:2], psyCurveControl[:2], 'o--', color=baseColour, lw=3, ms=8, zorder=10)
    l1, = plt.plot(xVals[1:], psyCurveControl[1:], 'o-', color=baseColour, lw=3, ms=8, zorder=10)
    #l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=baseColour, lw=3, ms=8)
    plt.errorbar(range(len(possibleSNRs)), psyCurveControl, yerr=[lowerErrorControl, upperErrorControl], fmt='none',
                 color=baseColour, lw=2, capsize=5, capthick=1)

    psyCurveLaser = data['psyCurveLaser']
    upperErrorLaser = data['upperErrorLaser']
    lowerErrorLaser = data['lowerErrorLaser']

    plt.plot(xVals[:2], psyCurveLaser[:2], 'o--', color=PVColour, lw=3, ms=8, zorder=10)
    l2, = plt.plot(xVals[1:], psyCurveLaser[1:], 'o-', color=PVColour, lw=3, ms=8, zorder=10)
    #l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o-', color=PVColour, lw=3, ms=8)
    plt.errorbar(range(len(possibleSNRs)), psyCurveLaser, yerr=[lowerErrorLaser, upperErrorLaser], fmt='none',
                 color=PVColour, lw=2, capsize=5, capthick=1, zorder=-10)

    axCurve.legend([l1, l2], ['control', 'PV activated'])

    axCurve.set_xlim(-0.2, len(possibleSNRs) - 0.8)
    axCurve.set_xticks(range(len(possibleSNRs)))
    axCurve.set_xticklabels(xTickLabels)
    axCurve.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

    axCurve.set_ylim(0, 100)
    axCurve.set_ylabel('Trials with tone reported (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axCurve)
    extraplots.breakaxis(0.5, 0, 0.15, 5, gap=0.5)
    extraplots.set_ticks_fontsize(axCurve, fontSizeTicks)

    axCurve.annotate(panelLabel, xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in accuracy during AC inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserdprime = summaryData['expLaserdprime']
    controldprime = summaryData['expNoLaserdprime']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        laserAccuracyControl = summaryControlData['laserAccuracy']
        controlAccuracyControl = summaryControlData['controlAccuracy']

        laserAccuracyCorrected = laserAccuracy - (laserAccuracyControl - controlAccuracyControl)

    else:
        laserdprimeCorrected = laserdprime

    axScatter = plt.subplot(gs[0,1])
    panelLabel = 'B'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLim = [0, 2.5]
    legendLabels = ['control', 'PV activated']

    for indBand in xLocs:
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserdprimeCorrected.shape[0]):
            plt.plot(thisxLocs, [controldprime[indMouse, indBand], laserdprimeCorrected[indMouse, indBand]], '-', color=connectLineColour)

        l1, = plt.plot(np.tile(thisxLocs[1],laserdprimeCorrected.shape[0]), laserdprimeCorrected[:,indBand], 'o', color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0],controldprime.shape[0]), controldprime[:,indBand], 'o', color=baseColour)

        #median = np.median(accuracyData, axis=0)
        #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    #axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(xTickLabels)
    #axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('d\'', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    # -- stats for main panel --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserdprimeCorrected[:,band], controldprime[:,band])[1]
        print(f"Change in d\' at {possibleBands[band]} oct pVal: {pVal}")

        if pVal < 0.05:
            extraplots.significance_stars(barLoc + xLocs[band], 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

    # inset showing difference in changes between bandwidths
    # axInset = inset_axes(axScatter, width="20%", height="35%", loc=1, bbox_to_anchor=(0.16, 0.02, 1, 1),
    #                      bbox_transform=axScatter.transAxes)
    #
    # width = 0.6
    # loc = np.arange(1, 3)
    #
    # # changeMedians = [100.0 * np.median(noPVsupDiff), 100.0 * np.median(noSOMsupDiff)]
    # # SICIs = [bootstrap_median_CI(100.0 * noPVsupDiff), bootstrap_median_CI(100.0 * noSOMsupDiff)]
    # changeAccuracy = laserAccuracyCorrected - controlAccuracy
    # for indBand, band in enumerate(possibleBands):
    #     median = np.median(changeAccuracy[:,indBand], axis=0)
    #     plt.plot([loc[indBand] - width / 2, loc[indBand] + width / 2], [median, median], color=PVColour, linewidth=3)  # medians
    #
    #     # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
    #     # loc2 = loc+width/2
    #     CIs = bf.bootstrap_median_CI(changeAccuracy[:,indBand])
    #     plt.plot([loc[indBand], loc[indBand]], CIs, color=PVColour, linewidth=1.5)  # error bars
    #     plt.plot([loc[indBand] - width / 8, loc[indBand] + width / 8], [CIs[0], CIs[0]], color=PVColour, linewidth=1.5)  # bottom caps
    #     plt.plot([loc[indBand] - width / 8, loc[indBand] + width / 8], [CIs[1], CIs[1]], color=PVColour, linewidth=1.5)  # top caps
    #
    # yLim = [-20, 5]
    # plt.ylim(yLim)
    # axInset.yaxis.tick_right()
    # axInset.yaxis.set_ticks_position('right')
    # plt.locator_params(axis='y', nbins=5)
    # axInset.spines['left'].set_visible(False)
    # axInset.spines['top'].set_visible(False)
    # plt.ylabel(r'$\Delta$Accuracy (%)', fontsize=fontSizeLegend, rotation=-90, labelpad=15)
    # axInset.yaxis.set_label_position('right')
    # axInset.tick_params(axis='y', labelsize=fontSizeLegend)
    # plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    #
    # # -- stats for inset --
    # pVal = stats.ranksums(changeAccuracy[:,0], changeAccuracy[:,1])[1]
    # print(f"Change in accuracy between bandwidths pVal: {pVal}")
    #
    # if pVal < 0.05:
    #     extraplots.significance_stars(xLocs, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

# --- comparison in change in hit/FR rate with AC inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserHits = summaryData['expLaserHits']
    controlHits = summaryData['expNoLaserHits']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        laserBiasControl = summaryControlData['laserBias']
        controlBiasControl = summaryControlData['controlBias']

        laserBiasCorrected = laserBias - (laserBiasControl - controlBiasControl)

    else:
        laserHitsCorrected = laserHits

    axScatter = plt.subplot(gs[0, 2])
    panelLabel = 'C'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLim = [0.0,100.0]
    legendLabels = ['control', 'PV activated']

    for indBand in xLocs:
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserHitsCorrected.shape[0]):
            plt.plot(thisxLocs, [controlHits[indMouse, indBand], laserHitsCorrected[indMouse, indBand]], '-',
                     color=connectLineColour)

        l1, = plt.plot(np.tile(thisxLocs[1], laserHitsCorrected.shape[0]), laserHitsCorrected[:, indBand], 'o', color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0], controlHits.shape[0]), controlHits[:, indBand], 'o', color=baseColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    #axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(xTickLabels)
    axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('Hit Rate', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[2], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserHitsCorrected[:,band], controlHits[:,band])[1]
        print(f"Change in hit rate at {possibleBands[band]} oct pVal: {pVal}")

        if pVal < 0.05:
            extraplots.significance_stars(barLoc + xLocs[band], 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

    # --- comparison in change in FR rate with AC inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserFA = summaryData['expLaserFA']
    controlFA = summaryData['expNoLaserFA']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        laserBiasControl = summaryControlData['laserBias']
        controlBiasControl = summaryControlData['controlBias']

        laserBiasCorrected = laserBias - (laserBiasControl - controlBiasControl)

    else:
        laserFACorrected = laserFA

    axScatter = plt.subplot(gs[0, 3])
    panelLabel = 'D'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLim = [0.0, 80.0]
    legendLabels = ['control', 'PV activated']

    for indBand in xLocs:
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserFACorrected.shape[0]):
            plt.plot(thisxLocs, [controlFA[indMouse, indBand], laserFACorrected[indMouse, indBand]], '-',
                     color=connectLineColour)

        l1, = plt.plot(np.tile(thisxLocs[1], laserFACorrected.shape[0]), laserFACorrected[:, indBand], 'o',
                       color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0], controlFA.shape[0]), controlFA[:, indBand], 'o', color=baseColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    # axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(xTickLabels)
    #axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('False Alarm Rate', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[3], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserFACorrected[:, band], controlFA[:, band])[1]
        print(f"Change in false alarm rate at {possibleBands[band]} oct pVal: {pVal}")

        if pVal < 0.05:
            extraplots.significance_stars(barLoc + xLocs[band], 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

# if CORRECTED:
#     plt.suptitle('LASER CORRECTED')
# else:
#     plt.suptitle('NO CORRECTION')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
