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

FIGNAME = 'figure_ac_inactivation' # data for control figure in same folder
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'SuppFig2_ac_inactivation_controls'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [5,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.58]  # Horiz position for panel labels
labelPosY = [0.97, 0.49]  # Vert position for panel labels

summaryFileName = 'all_behaviour_ac_inactivation_control.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2, width_ratios=[1.0, 0.5])
gs.update(top=0.99, bottom=0.12, left=0.13, right=0.97, wspace=0.5, hspace=0.3)

# --- summary of change in accuracy with laser but without inactivation ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserAccuracy = summaryData['laserAccuracy']
    controlAccuracy = summaryData['controlAccuracy']
    possibleBands = summaryData['possibleBands']

    axScatter = plt.subplot(gs[0,0])
    panelLabel = 'A'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['no laser', 'laser']

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

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserAccuracy[:,band], controlAccuracy[:,band])[1]
        print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

# --- comparison in change in bias with laser but not inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserBias = summaryData['laserBias']
    controlBias = summaryData['controlBias']
    possibleBands = summaryData['possibleBands']

    axScatter = plt.subplot(gs[1, 0])
    panelLabel = 'C'

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['no laser', 'laser']

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

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserBias[:,band], controlBias[:,band])[1]
        print(f"Change in bias at {possibleBands[band]} oct pVal: {pVal}")

# -- comparison of change in accuracy between inactivation and no inactivation conditions --
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    controlChangeAccuracy = summaryData['controlChangeAccuracy']
    inactChangeAccuracy = summaryData['expChangeAccuracy']

    axScatter = plt.subplot(gs[0, 1])
    panelLabel = 'B'

    xLocs = range(2)
    yLims = (-20,1)

    plt.plot(np.tile(xLocs[0], len(controlChangeAccuracy)), controlChangeAccuracy, 'o', color=ExcColour, alpha=0.3)
    plt.plot(np.tile(xLocs[1], len(inactChangeAccuracy)), inactChangeAccuracy, 'o', color=PVColour, alpha=0.3)

    plt.plot([xLocs[0]-0.2, xLocs[0]+0.2], np.tile(np.median(controlChangeAccuracy),2), '-', color='k', lw=3)
    plt.plot([xLocs[1] - 0.2, xLocs[1] + 0.2], np.tile(np.median(inactChangeAccuracy), 2), '-', color='k', lw=3)

    axScatter.set_xlim(-0.5, 1.5)
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(['control', 'inactivation'], rotation=-45)

    axScatter.set_ylim(yLims)
    axScatter.set_ylabel('Change in accuracy (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    pVal = stats.ranksums(controlChangeAccuracy, inactChangeAccuracy)[1]
    print(f"Control vs inactivation change in accuracy p val = {pVal}")
    if pVal < 0.05:
        extraplots.significance_stars(xLocs, 0.98 * yLims[1], 0.03 * np.diff(yLims), gapFactor=0.2)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

# -- comparison of change in bias between inactivation and no inactivation conditions --
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    controlChangeBias = summaryData['controlChangeBias']
    inactChangeBias = summaryData['expChangeBias']

    axScatter = plt.subplot(gs[1, 1])
    panelLabel = 'D'

    xLocs = range(2)
    yLims = (-0.5, 0.1)

    plt.plot(np.tile(xLocs[0], len(controlChangeBias)), controlChangeBias, 'o', color=ExcColour, alpha=0.3)
    plt.plot(np.tile(xLocs[1], len(inactChangeBias)), inactChangeBias, 'o', color=PVColour, alpha=0.3)

    plt.plot([xLocs[0]-0.2, xLocs[0]+0.2], np.tile(np.median(controlChangeBias),2), '-', color='k', lw=3)
    plt.plot([xLocs[1] - 0.2, xLocs[1] + 0.2], np.tile(np.median(inactChangeBias), 2), '-', color='k', lw=3)

    axScatter.set_xlim(-0.5, 1.5)
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(['control', 'inactivation'], rotation=-45)

    axScatter.set_ylim(yLims)
    axScatter.set_ylabel('Change in bias', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    pVal = stats.ranksums(controlChangeBias, inactChangeBias)[1]
    print(f"Control vs inactivation change in bias p val = {pVal}")
    if pVal < 0.05:
        extraplots.significance_stars(xLocs, 0.98 * yLims[1], 0.03 * np.diff(yLims), gapFactor=0.2)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
