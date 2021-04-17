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

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig3_ac_inactivation_reaction_times'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [3.3,4]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.49]  # Horiz position for panel labels
labelPosY = [0.97, 0.47]  # Vert position for panel labels

summaryFileName = 'all_reaction_times_ac_inactivation.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2, wspace=0.3, hspace=0.4, height_ratios=[1,0.7])
gs.update(top=0.97, bottom=0.1, left=0.2, right=0.99, wspace=0.5, hspace=0.3)

# --- summary of reaction times ---
if PANELS[0]:
    dataFullPath = os.path.join(inactDataDir, summaryFileName)
    data = np.load(dataFullPath)

    laserReaction = data['expLaserReactionAllBand']
    controlReaction = data['expNoLaserReactionAllBand']

    axScatter = plt.subplot(gs[0, 0])
    panelLabel = 'A'

    barLoc = np.array([-0.24, 0.24])
    yLim = [0, 0.15]
    legendLabels = ['control', 'PV act.']

    for indMouse in range(len(laserReaction)):
        plt.plot(barLoc, [controlReaction[indMouse], laserReaction[indMouse]], '-', color=connectLineColour)

    l1, = plt.plot(np.tile(barLoc[1], laserReaction.shape[0]), laserReaction, 'o', color=PVColour)
    l2, = plt.plot(np.tile(barLoc[0], controlReaction.shape[0]), controlReaction, 'o', color=baseColour)

    # median = np.median(accuracyData, axis=0)
    # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    # axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axScatter.set_xticks(barLoc)
    axScatter.set_xticklabels(legendLabels, fontsize=fontSizeLegend, rotation=-45)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('Sampling time (s)', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats for main panel --
    pVal = stats.wilcoxon(laserReaction, controlReaction)[1]
    print(f"Change in sampling time pVal: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

# --- laser in vs out reaction times ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserReaction = summaryData['expLaserReactionAllBand']
    controlReaction = summaryData['expNoLaserReactionAllBand']
    laserReactionControl = summaryData['controlLaserReactionAllBand']
    controlReactionControl = summaryData['controlNoLaserReactionAllBand']

    axScatter = plt.subplot(gs[1, 0])
    panelLabel = 'C'
    expChange = laserReaction - controlReaction
    controlChange = laserReactionControl - controlReactionControl
    plt.plot(controlChange, expChange, 'o', color=PVColour)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    yLim = [-0.005, 0.034]
    xLim = [-0.005, 0.034]

    axScatter.set_xlim(xLim)
    axScatter.set_ylim(yLim)

    axScatter.set_xlabel(r'laser-out $\Delta$ sampling time', fontsize=fontSizeLabels)
    axScatter.set_ylabel(r'laser-in $\Delta$ sampling time', fontsize=fontSizeLabels)
    axScatter.set(adjustable='box', aspect='equal')

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out sampling time change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

# -- sommary of change in decision times with and without laser inactivation --
if PANELS[2]:
    dataFullPath = os.path.join(inactDataDir, summaryFileName)
    data = np.load(dataFullPath)

    laserDecision = data['expLaserDecisionAllBand']
    controlDecision = data['expNoLaserDecisionAllBand']

    axScatter = plt.subplot(gs[0, 1])
    panelLabel = 'B'

    barLoc = np.array([-0.24, 0.24])
    yLim = [0.3, 0.45]
    legendLabels = ['control', 'PV act.']

    for indMouse in range(len(laserDecision)):
        plt.plot(barLoc, [controlDecision[indMouse], laserDecision[indMouse]], '-', color=connectLineColour)

    l1, = plt.plot(np.tile(barLoc[1], laserDecision.shape[0]), laserDecision, 'o', color=PVColour)
    l2, = plt.plot(np.tile(barLoc[0], controlDecision.shape[0]), controlDecision, 'o', color=baseColour)

    # median = np.median(accuracyData, axis=0)
    # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    # axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
    axScatter.set_xticks(barLoc)
    axScatter.set_xticklabels(legendLabels, fontsize=fontSizeLegend, rotation=-45)

    axScatter.set_ylim(yLim)
    axScatter.set_ylabel('Time to reward (s)', fontsize=fontSizeLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats for main panel --
    pVal = stats.wilcoxon(laserDecision, controlDecision)[1]
    print(f"Change in decision time pVal: {pVal}")

    if pVal < 0.05:
        extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

# --- laser in vs out reaction times ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserDecision = summaryData['expLaserDecisionAllBand']
    controlDecision = summaryData['expNoLaserDecisionAllBand']
    laserDecisionControl = summaryData['controlLaserDecisionAllBand']
    controlDecisionControl = summaryData['controlNoLaserDecisionAllBand']

    axScatter = plt.subplot(gs[1, 1])
    panelLabel = 'D'
    expChange = laserDecision - controlDecision
    controlChange = laserDecisionControl - controlDecisionControl
    plt.plot(controlChange, expChange, 'o', color=PVColour)

    plt.plot([-100, 100], [0, 0], ':', c='0.5', zorder=-10)
    plt.plot([0, 0], [-100, 100], ':', c='0.5', zorder=-10)
    plt.plot([-100, 100], [-100, 100], ':', c='0.5', zorder=-10)

    yLim = [-0.01, 0.02]
    xLim = [-0.01, 0.02]

    axScatter.set_xlim(xLim)
    axScatter.set_ylim(yLim)

    axScatter.set_xlabel(r'laser-out $\Delta$ time to reward', fontsize=fontSizeLabels)
    axScatter.set_ylabel(r'laser-in $\Delta$ time to reward', fontsize=fontSizeLabels)
    axScatter.set(adjustable='box', aspect='equal')

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out decision time change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
