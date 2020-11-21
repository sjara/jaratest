import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

FIGNAME = 'figure_inhibitory_inactivation_reaction_times' # data for control figure in same folder
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'SuppFigX_inhib_inactivation_reaction_controls'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [9,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.04, 0.33, 0.51, 0.79]  # Horiz position for panel labels
labelPosY = [0.97, 0.49]  # Vert position for panel labels

summaryFileName = 'all_reaction_times_inhib_inactivation.npz'

baseColour = figparams.colp['baseline']
controlColour = figparams.colp['control']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
connectColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 4, width_ratios=[1.0, 0.5, 1.0, 0.5])
gs.update(top=0.99, bottom=0.10, left=0.10, right=0.99, wspace=0.6, hspace=0.3)

# --- summary of change in accuracy with laser but without inactivation ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserReaction = summaryData['PVcontrolLaserReaction']
    PVcontrolReaction = summaryData['PVcontrolNoLaserReaction']
    SOMlaserReaction = summaryData['SOMcontrolLaserReaction']
    SOMcontrolReaction = summaryData['SOMcontrolNoLaserReaction']
    possibleBands = summaryData['possibleBands']

    laserReactions = [PVlaserReaction, SOMlaserReaction]
    controlReactions = [PVcontrolReaction, SOMcontrolReaction]

    panelLabels = ['A', 'E']

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['no laser', 'laser']
    colours = [PVColour, SOMColour]
    rowTitles = ['PV-ArchT mice', 'SOM-ArchT mice']
    rowTitleX = 0.01
    rowTitleY = [0.9, 0.4]

    for type in range(len(laserReactions)):
        axScatter = plt.subplot(gs[type, 0])

        laserReaction = laserReactions[type]
        controlReaction = controlReactions[type]
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserReaction.shape[0]):
                plt.plot(thisxLocs, [controlReaction[indMouse, indBand], laserReaction[indMouse, indBand]], '-', color=connectColour)

            l1, = plt.plot(np.tile(thisxLocs[1],laserReaction.shape[0]), laserReaction[:,indBand], 'o', color=controlColour)
            l2, = plt.plot(np.tile(thisxLocs[0],controlReaction.shape[0]), controlReaction[:,indBand], 'o', color=baseColour)

            #median = np.median(accuracyData, axis=0)
            #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], legendLabels, loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (oct)', fontsize=fontSizeLabels)

        #axScatter.set_ylim(50, 95)
        axScatter.set_ylabel('Sampling time (s)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[0], labelPosY[type]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axScatter.annotate(rowTitles[type], xy=(rowTitleX, rowTitleY[type]), xycoords='figure fraction',
                          fontsize=fontSizePanel, fontweight='bold', color=colours[type], rotation=90)

        # -- stats!! --
        for band in range(len(possibleBands)):
            pVal = stats.wilcoxon(laserReaction[:,band], controlReaction[:,band])[1]
            print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

# --- comparison in change in bias with laser but not inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserDecision = summaryData['PVcontrolLaserDecision']
    PVcontrolDecision = summaryData['PVcontrolNoLaserDecision']
    SOMlaserDecision = summaryData['SOMcontrolLaserDecision']
    SOMcontrolDecision = summaryData['SOMcontrolNoLaserDecision']
    possibleBands = summaryData['possibleBands']

    laserDecisions = [PVlaserDecision, SOMlaserDecision]
    controlDecisions = [PVcontrolDecision, SOMcontrolDecision]

    panelLabels = ['C', 'G']

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLims = [(-0.55, 0.2), (-0.8, 0.8)]
    xTickLabels = possibleBands
    legendLabels = ['no laser', 'laser']
    colours = [PVColour, SOMColour]

    for type in range(len(laserDecisions)):
        axScatter = plt.subplot(gs[type, 2])
        laserDecision = laserDecisions[type]
        controlDecision = controlDecisions[type]
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserDecision.shape[0]):
                plt.plot(thisxLocs, [controlDecision[indMouse, indBand], laserDecision[indMouse, indBand]], '-',
                         color=connectColour)

            l1, = plt.plot(np.tile(thisxLocs[1], laserDecision.shape[0]), laserDecision[:, indBand], 'o', color=controlColour)
            l2, = plt.plot(np.tile(thisxLocs[0], controlDecision.shape[0]), controlDecision[:, indBand], 'o', color=baseColour)

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], legendLabels, loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (oct)', fontsize=fontSizeLabels)

        #axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Decision time (s)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[2], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- stats!! --
        for band in range(len(possibleBands)):
            pVal = stats.wilcoxon(laserDecision[:,band], controlDecision[:,band])[1]
            print(f"Change in bias at {possibleBands[band]} oct pVal: {pVal}")

# -- comparison of change in sampling time between control and experimental conditions --
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserReaction = summaryData['PVexpLaserReaction']
    PVcontrolReaction = summaryData['PVexpNoLaserReaction']
    SOMlaserReaction = summaryData['SOMexpLaserReaction']
    SOMcontrolReaction = summaryData['SOMexpNoLaserReaction']

    controlPVlaserReaction = summaryData['PVcontrolLaserReaction']
    controlPVcontrolReaction = summaryData['PVcontrolNoLaserReaction']
    controlSOMlaserReaction = summaryData['SOMcontrolLaserReaction']
    controlSOMcontrolReaction = summaryData['SOMcontrolNoLaserReaction']

    possibleBands = summaryData['possibleBands']

    controlChangesSampling = [controlPVlaserReaction-controlPVcontrolReaction, controlSOMlaserReaction-controlSOMcontrolReaction]
    inactChangesSampling = [PVlaserReaction-PVcontrolReaction, SOMlaserReaction-SOMcontrolReaction]

    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    legendLabels = ['no PV', 'no SOM']
    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLims = [(-0.02, 0.02), (-0.02, 0.08)]

    for type in range(len(controlChangesSampling)):
        axScatter = plt.subplot(gs[type, 1])
        controlChangeSampling = controlChangesSampling[type]
        inactChangeSampling = inactChangesSampling[type]

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(len(controlChangeSampling)):
                plt.plot(thisxLocs, [controlChangeSampling[indMouse, indBand], inactChangeSampling[indMouse, indBand]], '-', color=connectColour)
            plt.plot(np.tile(thisxLocs[0], controlChangeSampling.shape[0]), controlChangeSampling[:,indBand], 'o', color=controlColour)
            plt.plot(np.tile(thisxLocs[1], inactChangeSampling.shape[0]), inactChangeSampling[:,indBand], 'o', mec=colours[type], mfc='white')

            plt.plot([thisxLocs[0]-0.2, thisxLocs[0]+0.2], np.tile(np.median(controlChangeSampling,axis=0)[indBand],2), '-', color='k', lw=3)
            plt.plot([thisxLocs[1] - 0.2, thisxLocs[1] + 0.2], np.tile(np.median(inactChangeSampling,axis=0)[indBand], 2), '-', color='k', lw=3)

            axScatter.set_xlim(-0.5, 1.5)
            axScatter.set_xticks(xLocs)
            axScatter.set_xticklabels(['control', legendLabels[type]], rotation=-45)

            axScatter.set_ylim(yLims[type])
            axScatter.set_ylabel('Change in sampling time (s)', fontsize=fontSizeLabels)

            extraplots.boxoff(axScatter)
            extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

            pVal = stats.wilcoxon(controlChangeSampling[:,indBand], inactChangeSampling[:,indBand])[1]
            print(f"Control vs inactivation change in accuracy p val = {pVal}")
            if pVal < 0.05:
                extraplots.significance_stars(thisxLocs, 0.98 * yLims[type][1], 0.03 * np.diff(yLims[type]), gapFactor=0.2)

            axScatter.annotate(panelLabels[type], xy=(labelPosX[1], labelPosY[type]), xycoords='figure fraction',
                               fontsize=fontSizePanel, fontweight='bold')

# -- comparison of change in decision time between control and experimental conditions --
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserDecision = summaryData['PVexpLaserDecision']
    PVcontrolDecision = summaryData['PVexpNoLaserDecision']
    SOMlaserDecision = summaryData['SOMexpLaserDecision']
    SOMcontrolDecision = summaryData['SOMexpNoLaserDecision']

    controlPVlaserDecision = summaryData['PVcontrolLaserDecision']
    controlPVcontrolDecision = summaryData['PVcontrolNoLaserDecision']
    controlSOMlaserDecision = summaryData['SOMcontrolLaserDecision']
    controlSOMcontrolDecision = summaryData['SOMcontrolNoLaserDecision']

    possibleBands = summaryData['possibleBands']

    controlChangesDecision = [controlPVlaserDecision-controlPVcontrolDecision, controlSOMlaserDecision-controlSOMcontrolDecision]
    inactChangesDecision = [PVlaserDecision-PVcontrolDecision, SOMlaserDecision-SOMcontrolDecision]

    panelLabels = ['D', 'H']
    colours = [PVColour, SOMColour]
    legendLabels = ['no PV', 'no SOM']
    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLims = [(-0.02, 0.02), (-0.02, 0.08)]

    for type in range(len(controlChangesDecision)):
        axScatter = plt.subplot(gs[type, 3])
        controlChangeDecision = controlChangesDecision[type]
        inactChangeDecision = inactChangesDecision[type]

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(len(controlChangeDecision)):
                plt.plot(thisxLocs, [controlChangeDecision[indMouse, indBand], inactChangeDecision[indMouse, indBand]], '-', color=connectColour)
            plt.plot(np.tile(thisxLocs[0], controlChangeDecision.shape[0]), controlChangeDecision[:,indBand], 'o', color=controlColour)
            plt.plot(np.tile(thisxLocs[1], inactChangeDecision.shape[0]), inactChangeDecision[:,indBand], 'o', mec=colours[type], mfc='white')

            plt.plot([thisxLocs[0]-0.2, thisxLocs[0]+0.2], np.tile(np.median(controlChangeDecision,axis=0)[indBand],2), '-', color='k', lw=3)
            plt.plot([thisxLocs[1] - 0.2, thisxLocs[1] + 0.2], np.tile(np.median(inactChangeDecision,axis=0)[indBand], 2), '-', color='k', lw=3)

            axScatter.set_xlim(-0.5, 1.5)
            axScatter.set_xticks(xLocs)
            axScatter.set_xticklabels(['control', legendLabels[type]], rotation=-45)

            axScatter.set_ylim(yLims[type])
            axScatter.set_ylabel('Change in sampling time (s)', fontsize=fontSizeLabels)

            extraplots.boxoff(axScatter)
            extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

            pVal = stats.wilcoxon(controlChangeDecision[:,indBand], inactChangeDecision[:,indBand])[1]
            print(f"Control vs inactivation change in accuracy p val = {pVal}")
            if pVal < 0.05:
                extraplots.significance_stars(thisxLocs, 0.98 * yLims[type][1], 0.03 * np.diff(yLims[type]), gapFactor=0.2)

            axScatter.annotate(panelLabels[type], xy=(labelPosX[3], labelPosY[type]), xycoords='figure fraction',
                               fontsize=fontSizePanel, fontweight='bold')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
