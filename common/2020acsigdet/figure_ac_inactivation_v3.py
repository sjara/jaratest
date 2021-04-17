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
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 0
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'Fig2_ac_inactivation_new2_corrected'  # Do not include extension
else:
    figFilename = 'Fig2_ac_inactivation_new2'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6.8,8]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.35, 0.69, 0.36, 0.68]  # Horiz position for panel labels
labelPosY = [0.97, 0.63, 0.25]  # Vert position for panel labels

ACInactExample1 = 'band046_psycurve.npz'
ACInactExample2 = 'band134_psycurve.npz'
summaryFileName = 'all_behaviour_ac_inactivation_v2.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 3, wspace=0.3, hspace=0.4, height_ratios=[0.8,1,0.7])
gs.update(top=0.97, bottom=0.05, left=0.11, right=0.99, wspace=0.5, hspace=0.3)

axCartoons = gs[0, :]
gs2 = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=axCartoons, wspace=0.3, hspace=0.4, width_ratios=[1.0,0.8,0.8])
# --- example psychometric curves ---
if PANELS[0]:
    examplesFileNames = [ACInactExample1, ACInactExample2]
    panelLabels = ['A', 'B', 'C']  # labels for psy curve and cartoons

    for indExample, example in enumerate(examplesFileNames):
        dataFullPath = os.path.join(inactDataDir, example)
        data = np.load(dataFullPath)

        psyCurveControl = data['psyCurveControl']
        upperErrorControl = data['upperErrorControl']
        lowerErrorControl = data['lowerErrorControl']
        possibleSNRs = data['possibleSNRs']

        axCurve = plt.subplot(gs2[0, indExample+1])
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
        if not indExample:
            axCurve.set_ylabel('Trials with rightward choice (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axCurve)
        extraplots.breakaxis(0.5, 0, 0.15, 5, gap=0.5)
        extraplots.set_ticks_fontsize(axCurve, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axCurve.annotate(label, xy=(labelPosX[indLabel], labelPosY[0]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in d' during AC inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserdprime = summaryData['expLaserdprimeAllBands']
    controldprime = summaryData['expNoLaserdprimeAllBandsAllBand']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        laserdprimeControl = summaryData['controlLaserdprimeAllBands']
        controldprimeControl = summaryData['controlNoLaserdprimeAllBands']

        laserdprimeCorrected = laserdprime - (laserdprimeControl - controldprimeControl)

    else:
        laserdprimeCorrected = laserdprime

    axScatter = plt.subplot(gs[1,0])
    panelLabel = 'D'

    barLoc = np.array([-0.24, 0.24])
    yLim = [0, 2.2]
    legendLabels = ['control', 'PV act.']

    for indMouse in range(laserdprimeCorrected.shape[0]):
        plt.plot(barLoc, [controldprime[indMouse], laserdprimeCorrected[indMouse]], '-', color=connectLineColour)

    l1, = plt.plot(np.tile(barLoc[1],laserdprimeCorrected.shape[0]), laserdprimeCorrected, 'o', color=PVColour)
    l2, = plt.plot(np.tile(barLoc[0],controldprime.shape[0]), controldprime, 'o', color=baseColour)

        #median = np.median(accuracyData, axis=0)
        #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    #axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axScatter.set_xticks(barLoc)
    axScatter.set_xticklabels(legendLabels, fontsize=fontSizeLegend, rotation=-45)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('d\'', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    # -- stats for main panel --
    pVal = stats.wilcoxon(laserdprimeCorrected, controldprime)[1]
    print(f"Change in d\' pVal: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

# --- comparison in change in hit rate with AC inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserHits = summaryData['expLaserHitsAllBands']
    controlHits = summaryData['expNoLaserHitsAllBands']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        laserHitsControl = summaryData['controlLaserHitsAllBands']
        controlHitsControl = summaryData['controlNoLaserHitsAllBands']

        laserHitsCorrected = laserHits - (laserHitsControl - controlHitsControl)

    else:
        laserHitsCorrected = laserHits

    axScatter = plt.subplot(gs[1, 1])
    panelLabel = 'E'

    barLoc = np.array([-0.24, 0.24])
    yLim = [0.0,100.0]
    legendLabels = ['control', 'PV act.']

    for indMouse in range(laserHitsCorrected.shape[0]):
        plt.plot(barLoc, [controlHits[indMouse], laserHitsCorrected[indMouse]], '-',
                 color=connectLineColour)

    l1, = plt.plot(np.tile(barLoc[1], laserHitsCorrected.shape[0]), laserHitsCorrected, 'o', color=PVColour)
    l2, = plt.plot(np.tile(barLoc[0], controlHits.shape[0]), controlHits, 'o', color=baseColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    #axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axScatter.set_xticks(barLoc)
    axScatter.set_xticklabels(legendLabels, fontsize=fontSizeLegend, rotation=-45)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('Hit Rate (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[3], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    pVal = stats.wilcoxon(laserHitsCorrected, controlHits)[1]
    print(f"Change in hit rate p val: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

    # --- comparison in change in FA rate with AC inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserFA = summaryData['expLaserFAallBands']
    controlFA = summaryData['expNoLaserFAallBands']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        laserFAControl = summaryData['controlLaserFAallBands']
        controlFAControl = summaryData['controlNoLaserFAallBands']

        laserFACorrected = laserFA - (laserFAControl - controlFAControl)

    else:
        laserFACorrected = laserFA

    axScatter = plt.subplot(gs[1, 2])
    panelLabel = 'F'

    barLoc = np.array([-0.24, 0.24])
    yLim = [0.0, 100.0]
    legendLabels = ['control', 'PV act.']

    for indMouse in range(laserFACorrected.shape[0]):
        plt.plot(barLoc, [controlFA[indMouse], laserFACorrected[indMouse]], '-', color=connectLineColour)

    l1, = plt.plot(np.tile(barLoc[1], laserFACorrected.shape[0]), laserFACorrected, 'o', color=PVColour)
    l2, = plt.plot(np.tile(barLoc[0], controlFA.shape[0]), controlFA, 'o', color=baseColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    # axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axScatter.set_xticks(barLoc)
    axScatter.set_xticklabels(legendLabels, fontsize=fontSizeLegend, rotation=-45)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('False Alarm Rate (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[4], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    pVal = stats.wilcoxon(laserFACorrected, controlFA)[1]
    print(f"Change in false alarm rate pVal: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

# --- laser in vs out correlation of d' ---
if PANELS[4]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserdprime = summaryData['expLaserdprimeAllBands']
    controldprime = summaryData['expNoLaserdprimeAllBandsAllBand']
    laserdprimeControl = summaryData['controlLaserdprimeAllBands']
    controldprimeControl = summaryData['controlNoLaserdprimeAllBands']

    axScatter = plt.subplot(gs[2, 0])
    panelLabel = 'G'

    expChange = laserdprime - controldprime
    controlChange = laserdprimeControl - controldprimeControl
    plt.plot(controlChange, expChange, 'o', color=PVColour)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    yLim = [-1.0, 0.05]
    xLim = [-0.525, 0.525]

    axScatter.set_xlim(xLim)
    axScatter.set_ylim(yLim)

    axScatter.set_xlabel(r'laser-out $\Delta$ d$^\prime$', fontsize=fontSizeLabels)
    axScatter.set_ylabel(r'laser-in $\Delta$ d$^\prime$', fontsize=fontSizeLabels)
    axScatter.set(adjustable='box', aspect='equal')

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[2]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out d\' change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

    # -- laser-in vs laser-out --
    pVal = stats.wilcoxon(controlChange, expChange)[1]
    print(f'Laser in vs. out d\' change direction pVal: {pVal}')

# --- laser in vs out correlation of hit rate ---
if PANELS[5]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserHits = summaryData['expLaserHitsAllBands']
    controlHits = summaryData['expNoLaserHitsAllBands']
    laserHitsControl = summaryData['controlLaserHitsAllBands']
    controlHitsControl = summaryData['controlNoLaserHitsAllBands']

    axScatter = plt.subplot(gs[2, 1])
    panelLabel = 'H'

    expChange = laserHits - controlHits
    controlChange = laserHitsControl - controlHitsControl
    plt.plot(controlChange, expChange, 'o', color=PVColour)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    yLim = [-70, 10]
    xLim = [-40, 40]

    axScatter.set_xlim(xLim)
    axScatter.set_ylim(yLim)

    axScatter.set_xlabel(r'laser-out $\Delta$ hit rate', fontsize=fontSizeLabels)
    axScatter.set_ylabel(r'laser-in $\Delta$ hit rate', fontsize=fontSizeLabels)
    axScatter.set(adjustable='box', aspect='equal')

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[3], labelPosY[2]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out hit rate change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

# --- laser in vs out correlation of FA rate ---
if PANELS[6]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserFA = summaryData['expLaserFAallBands']
    controlFA = summaryData['expNoLaserFAallBands']
    laserFAControl = summaryData['controlLaserFAallBands']
    controlFAControl = summaryData['controlNoLaserFAallBands']

    axScatter = plt.subplot(gs[2, 2])
    panelLabel = 'I'
    expChange = laserFA - controlFA
    controlChange = laserFAControl - controlFAControl
    plt.plot(controlChange, expChange, 'o', color=PVColour)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    # yLim = [-40, 10]
    # xLim = [-25, 25]
    yLim = [-70, 10]
    xLim = [-40, 40]

    axScatter.set_xlim(xLim)
    axScatter.set_ylim(yLim)

    axScatter.set_xlabel(r'laser-out $\Delta$ FA rate', fontsize=fontSizeLabels)
    axScatter.set_ylabel(r'laser-in $\Delta$ FA rate', fontsize=fontSizeLabels)
    axScatter.set(adjustable='box', aspect='equal')

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[4], labelPosY[2]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out FA rate change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
