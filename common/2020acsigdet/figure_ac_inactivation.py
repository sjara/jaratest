import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

FIGNAME = 'figure_ac_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig2_ac_inactivation'  # Do not include extension
# figFormat = 'pdf'  # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [6,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.4, 0.48]  # Horiz position for panel labels
labelPosY = [0.96, 0.48]  # Vert position for panel labels

ACInactExample = 'band046_psycurve.npz'
summaryFileName = 'all_behaviour_ac_inactivation.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2)
gs.update(top=0.97, bottom=0.08, left=0.08, right=0.97, wspace=0.3, hspace=0.3)

axCartoons = gs[0, :]
gs2 = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=axCartoons, wspace=0.3, hspace=0.4, width_ratios=[0.7,1.0])
# --- example psychometric curves ---
if PANELS[0]:
    dataFullPath = os.path.join(inactDataDir, ACInactExample)
    data = np.load(dataFullPath)

    psyCurveControl = data['psyCurveControl']
    upperErrorControl = data['upperErrorControl']
    lowerErrorControl = data['lowerErrorControl']
    possibleSNRs = data['possibleSNRs']

    axCurve = plt.subplot(gs2[0, 1])
    panelLabels = ['A', 'B']  # labels for psy curve and cartoons
    xTickLabels = ['-inf']
    xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])

    l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=ExcColour, lw=3, ms=8)
    plt.errorbar(range(len(possibleSNRs)), psyCurveControl, yerr=[lowerErrorControl, upperErrorControl], fmt='none',
                 color=ExcColour, lw=2, capsize=5, capthick=1)

    psyCurveLaser = data['psyCurveLaser']
    upperErrorLaser = data['upperErrorLaser']
    lowerErrorLaser = data['lowerErrorLaser']

    l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o-', color=PVColour, lw=3,
                   ms=8)
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

    for indLabel, label in enumerate(panelLabels):
        axCurve.annotate(label, xy=(labelPosX[indLabel], labelPosY[0]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in accuracy during AC inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserAccuracy = summaryData['laserAccuracy']
    controlAccuracy = summaryData['controlAccuracy']
    possibleBands = summaryData['possibleBands']

    axScatter = plt.subplot(gs[1,0])
    panelLabel = 'C'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['control', 'PV activated']

    for indBand in range(len(possibleBands)):
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserAccuracy.shape[0]):
            plt.plot(thisxLocs, [controlAccuracy[indMouse, indBand], laserAccuracy[indMouse, indBand]], '-', color=ExcColour)

        l1, = plt.plot(np.tile(thisxLocs[1],laserAccuracy.shape[0]), laserAccuracy[:,indBand], 'o', color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0],controlAccuracy.shape[0]), controlAccuracy[:,indBand], 'o', color=ExcColour)

        #median = np.median(accuracyData, axis=0)
        #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
    axScatter.set_xlabel('Masker bandwidth (oct)', fontsize=fontSizeLabels)

    axScatter.set_ylim(50, 95)
    axScatter.set_ylabel('Accuracy (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserAccuracy[:,band], controlAccuracy[:,band])[1]
        print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

# --- comparison in change in bias with AC inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserBias = summaryData['laserBias']
    controlBias = summaryData['controlBias']
    possibleBands = summaryData['possibleBands']

    axScatter = plt.subplot(gs[1, 1])
    panelLabel = 'D'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['control', 'PV activated']

    for indBand in range(len(possibleBands)):
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserBias.shape[0]):
            plt.plot(thisxLocs, [controlBias[indMouse, indBand], laserBias[indMouse, indBand]], '-',
                     color=ExcColour)

        l1, = plt.plot(np.tile(thisxLocs[1], laserBias.shape[0]), laserBias[:, indBand], 'o', color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0], controlBias.shape[0]), controlBias[:, indBand], 'o', color=ExcColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
    axScatter.set_xlabel('Masker bandwidth (oct)', fontsize=fontSizeLabels)

    axScatter.set_ylim(-0.75,0.4)
    axScatter.set_ylabel('Bias', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[2], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserBias[:,band], controlBias[:,band])[1]
        print(f"Change in bias at {possibleBands[band]} oct pVal: {pVal}")

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()