import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

figName = 'figure_inhibitory_inactivation_reaction_times'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, figName)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, figName)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
CORRECTED = 1
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'Fig4_inhib_inactivation_reaction_times_corrected'  # Do not include extension
else:
    figFilename = 'Fig4_inhib_inactivation_reaction_times'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [10,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.001, 0.24, 0.51, 0.76]  # Horiz position for panel labels
labelPosY = [0.97, 0.46]  # Vert position for panel labels

summaryFileName = 'all_reaction_times_inhib_inactivation.npz'
PVExampleFileName = 'band093_reaction_times.npz'
SOMExampleFileName = 'band108_reaction_times.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
controlColour = figparams.colp['control']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4, width_ratios=[1.0, 0.8, 1.0, 0.8])
gs.update(top=0.98, bottom=0.08, left=0.04, right=0.98, wspace=0.6, hspace=0.3)

# --- example histograms of sampling time ---
if PANELS[0]:
    fileNames = [PVExampleFileName, SOMExampleFileName]

    panelLabels = ['A', 'E']
    colours = [PVColour, SOMColour]

    for indType, exampleFileName in enumerate(fileNames):
        exampleDataFullPath = os.path.join(inactDataDir, exampleFileName)
        exampleData = np.load(exampleDataFullPath)

        axHist = plt.subplot(gs[indType, 0])

        controlDecisionTimes = exampleData['controlReactionTimes']
        laserDecisionTimes = exampleData['laserReactionTimes']

        bins = np.linspace(0.0, 0.6, 10)
        n, bins, patches = plt.hist([controlDecisionTimes, laserDecisionTimes], bins=bins, color=[baseColour, 'none'],
                                    density=True)
        plt.setp(patches[0], edgecolor=baseColour)
        plt.setp(patches[1], edgecolor=colours[indType], lw=1.5)

        # axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        # axScatter.set_xticks(xLocs)
        # axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axHist.set_xlabel('Sampling time (s)', fontsize=fontSizeLabels)

        # axScatter.set_ylim(50, 95)
        # axScatter.set_ylabel('Accuracy (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axHist)
        extraplots.set_ticks_fontsize(axHist, fontSizeTicks)

        axHist.annotate(panelLabels[indType], xy=(labelPosX[0], labelPosY[indType]), xycoords='figure fraction',
                        fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in sampling times with inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserReaction = summaryData['PVexpLaserReaction']
    PVcontrolReaction = summaryData['PVexpNoLaserReaction']
    SOMlaserReaction = summaryData['SOMexpLaserReaction']
    SOMcontrolReaction = summaryData['SOMexpNoLaserReaction']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        PVlaserReactionControl = summaryData['PVcontrolLaserReaction']
        PVcontrolReactionControl = summaryData['PVcontrolNoLaserReaction']
        SOMlaserReactionControl = summaryData['SOMcontrolLaserReaction']
        SOMcontrolReactionControl = summaryData['SOMcontrolNoLaserReaction']

        PVlaserReactionCorrected = PVlaserReaction - (PVlaserReactionControl - PVcontrolReactionControl)
        SOMlaserReactionCorrected = SOMlaserReaction - (SOMlaserReactionControl - SOMcontrolReactionControl)

    else:
        PVlaserReactionCorrected = PVlaserReaction
        SOMlaserReactionCorrected = SOMlaserReaction

    laserReactions = [PVlaserReactionCorrected, SOMlaserReactionCorrected]
    controlReactions = [PVcontrolReaction, SOMcontrolReaction]

    panelLabels = ['B', 'F']

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLims = [(0, 0.2), (-0.05, 0.3)]
    xTickLabels = possibleBands
    legendLabels = ['no PV', 'no SOM']
    colours = [PVColour, SOMColour]

    for type in range(len(laserReactions)):
        axScatter = plt.subplot(gs[type, 1])
        laserReaction = laserReactions[type]
        controlReaction = controlReactions[type]
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserReaction.shape[0]):
                plt.plot(thisxLocs, [controlReaction[indMouse, indBand], laserReaction[indMouse, indBand]], '-',
                         color=baseColour)

            l1, = plt.plot(np.tile(thisxLocs[1], laserReaction.shape[0]), laserReaction[:, indBand], 'o',
                           mec=colours[type], mfc='white')
            l2, = plt.plot(np.tile(thisxLocs[0], controlReaction.shape[0]), controlReaction[:, indBand], 'o',
                           mec=baseColour, mfc=baseColour)

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], ['control', legendLabels[type]], loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Sampling time (s)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[1], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- stats!! --
        for band in range(len(possibleBands)):
            pVal = stats.wilcoxon(laserReaction[:,band], controlReaction[:,band])[1]
            if pVal < 0.05:
                extraplots.significance_stars(barLoc + xLocs[band], 0.98 * yLims[type][1], 0.02 * np.diff(yLims[type]), gapFactor=0.3)
            print(f"Change in reaction time at {possibleBands[band]} oct with {legendLabels[type]} pVal: {pVal}")

# -- example histograms of decision times with inactivation --
if PANELS[2]:
    fileNames = [PVExampleFileName, SOMExampleFileName]

    panelLabels = ['C', 'G']
    colours = [PVColour, SOMColour]

    for indType, exampleFileName in enumerate(fileNames):
        exampleDataFullPath = os.path.join(inactDataDir, exampleFileName)
        exampleData = np.load(exampleDataFullPath)

        axHist = plt.subplot(gs[indType, 2])

        controlDecisionTimes = exampleData['controlDecisionTimes']
        laserDecisionTimes = exampleData['laserDecisionTimes']

        bins = np.linspace(0.1, 0.8, 12)
        n, bins, patches = plt.hist([controlDecisionTimes, laserDecisionTimes], bins=bins, color=[baseColour, 'none'],
                                    density=True)
        plt.setp(patches[0], edgecolor=baseColour)
        plt.setp(patches[1], edgecolor=colours[indType], lw=1.5)

        # axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        # axScatter.set_xticks(xLocs)
        # axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axHist.set_xlabel('Time to decision (s)', fontsize=fontSizeLabels)

        # axScatter.set_ylim(50, 95)
        # axScatter.set_ylabel('Accuracy (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axHist)
        extraplots.set_ticks_fontsize(axHist, fontSizeTicks)

        axHist.annotate(panelLabels[indType], xy=(labelPosX[2], labelPosY[indType]), xycoords='figure fraction',
                        fontsize=fontSizePanel, fontweight='bold')

    # --- comparison in change in decision times with inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserDecision = summaryData['PVexpLaserDecision']
    PVcontrolDecision = summaryData['PVexpNoLaserDecision']
    SOMlaserDecision = summaryData['SOMexpLaserDecision']
    SOMcontrolDecision = summaryData['SOMexpNoLaserDecision']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        PVlaserDecisionControl = summaryData['PVcontrolLaserDecision']
        PVcontrolDecisionControl = summaryData['PVcontrolNoLaserDecision']
        SOMlaserDecisionControl = summaryData['SOMcontrolLaserDecision']
        SOMcontrolDecisionControl = summaryData['SOMcontrolNoLaserDecision']

        PVlaserDecisionCorrected = PVlaserDecision - (PVlaserDecisionControl - PVcontrolDecisionControl)
        SOMlaserDecisionCorrected = SOMlaserDecision - (SOMlaserDecisionControl - SOMcontrolDecisionControl)

    else:
        PVlaserDecisionCorrected = PVlaserDecision
        SOMlaserDecisionCorrected = SOMlaserDecision

    laserDecisions = [PVlaserDecisionCorrected, SOMlaserDecisionCorrected]
    controlDecisions = [PVcontrolDecision, SOMcontrolDecision]

    panelLabels = ['D', 'H']

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLims = [(0.3, 0.6), (0.25, 0.55)]
    xTickLabels = possibleBands
    legendLabels = ['no PV', 'no SOM']
    colours = [PVColour, SOMColour]

    for type in range(len(laserDecisions)):
        axScatter = plt.subplot(gs[type, 3])
        laserDecision = laserDecisions[type]
        controlDecision = controlDecisions[type]
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserDecision.shape[0]):
                plt.plot(thisxLocs, [controlDecision[indMouse, indBand], laserDecision[indMouse, indBand]], '-',
                         color=baseColour)

            l1, = plt.plot(np.tile(thisxLocs[1], laserDecision.shape[0]), laserDecision[:, indBand], 'o',
                           mec=colours[type], mfc='white')
            l2, = plt.plot(np.tile(thisxLocs[0], controlDecision.shape[0]), controlDecision[:, indBand], 'o',
                           mec=baseColour, mfc=baseColour)

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], ['control', legendLabels[type]], loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Time to decision (s)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[3], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- stats!! --
        for band in range(len(possibleBands)):
            pVal = stats.wilcoxon(laserDecision[:, band], controlDecision[:, band])[1]
            if pVal < 0.05:
                extraplots.significance_stars(barLoc + xLocs[band], 0.98 * yLims[type][1], 0.02 * np.diff(yLims[type]),
                                              gapFactor=0.3)
            print(f"Change in decision time at {possibleBands[band]} oct with {legendLabels[type]} pVal: {pVal}")

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
