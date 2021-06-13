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
#inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig3_ac_inactivation_reaction_times'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [3.34,4]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.001, 0.5]  # Horiz position for panel labels
labelPosY = [0.96, 0.42]  # Vert position for panel labels

summaryFileName = 'all_reaction_times_ac_inactivation.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
connectLineColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2, wspace=0.3, hspace=0.4, height_ratios=[1,0.7])
gs.update(top=0.98, bottom=0.1, left=0.16, right=0.98, wspace=0.6, hspace=0.2)

# --- summary of reaction times ---
if PANELS[0]:
    dataFullPath = os.path.join(inactDataDir, summaryFileName)
    data = np.load(dataFullPath)

    laserReaction = 1000*data['expLaserReactionAllBand'] # convert to ms
    controlReaction = 1000*data['expNoLaserReactionAllBand']

    axScatter = plt.subplot(gs[0, 0])
    panelLabel = 'A'

    yLim = [0, 150]
    xTickLabels = ['baseline', 'no AC']

    bf.plot_laser_comparison(axScatter, [controlReaction, laserReaction], PVColour, PVColour, yLim, xTickLabels)

    axScatter.set_ylabel('Sampling time (ms)', fontsize=fontSizeLabels)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

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
    expChange = 1000 * (laserReaction - controlReaction)
    controlChange = 1000 * (laserReactionControl - controlReactionControl)

    yLim = [-5, 34]
    xLim = [-5, 34]

    bf.plot_exp_vs_control_scatter(axScatter, controlChange, expChange, PVColour, xLim, yLim, PVColour)

    axScatter.set_xlabel('Control \n' r'$\Delta$ sampling time (ms)', fontsize=fontSizeLabels, labelpad=2, linespacing=0.9)
    axScatter.set_ylabel('No AC \n' r'$\Delta$ sampling time (ms)', fontsize=fontSizeLabels, labelpad=1, linespacing=0.9)

    axScatter.annotate(panelLabel, xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out sampling time change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

# -- sommary of change in decision times with and without laser inactivation --
if PANELS[2]:
    dataFullPath = os.path.join(inactDataDir, summaryFileName)
    data = np.load(dataFullPath)

    laserDecision = 1000*data['expLaserDecisionAllBand']
    controlDecision = 1000*data['expNoLaserDecisionAllBand']

    axScatter = plt.subplot(gs[0, 1])
    panelLabel = 'B'
    yLim = [300, 450]
    xTickLabels = ['baseline', 'no AC']

    bf.plot_laser_comparison(axScatter, [controlDecision, laserDecision], PVColour, PVColour, yLim, xTickLabels)

    axScatter.set_ylabel('Time to reward (ms)', fontsize=fontSizeLabels)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

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
    expChange = 1000 * (laserDecision - controlDecision)
    controlChange = 1000 * (laserDecisionControl - controlDecisionControl)

    yLim = [-10, 20]
    xLim = [-10, 20]

    bf.plot_exp_vs_control_scatter(axScatter, controlChange, expChange, PVColour, xLim, yLim, PVColour)

    axScatter.set_xlabel(r'Control $\Delta$' ' time\n to reward (ms)', fontsize=fontSizeLabels, labelpad=2, linespacing=0.9)
    axScatter.set_ylabel(r'No AC $\Delta$' ' time\n to reward (ms)', fontsize=fontSizeLabels, labelpad=-3, linespacing=0.9)

    axScatter.annotate(panelLabel, xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- linear regression --
    slope, intercept, rVal, pVal, stdErr = stats.linregress(controlChange, expChange)

    print(f'Laser in vs. out decision time change: \ncorrelation coefficient: {rVal} \np Val: {pVal}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
