import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

FIGNAME = 'figure_inhibitory_inactivation' # data for control figure in same folder
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'SuppFig3_inhib_inactivation_controls'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [9,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.04, 0.33, 0.51, 0.79]  # Horiz position for panel labels
labelPosY = [0.97, 0.49]  # Vert position for panel labels

summaryFileName = 'all_behaviour_inhib_inactivation_control.npz'

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

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']
    possibleBands = summaryData['possibleBands']

    laserAccuracies = [PVlaserAccuracy, SOMlaserAccuracy]
    controlAccuracies = [PVcontrolAccuracy, SOMcontrolAccuracy]

    panelLabels = ['A', 'E']

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['no laser', 'laser']
    colours = [PVColour, SOMColour]
    rowTitles = ['PV-ArchT mice', 'SOM-ArchT mice']
    rowTitleX = 0.01
    rowTitleY = [0.9, 0.4]

    for type in range(len(laserAccuracies)):
        axScatter = plt.subplot(gs[type, 0])

        laserAccuracy = laserAccuracies[type]
        controlAccuracy = controlAccuracies[type]
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserAccuracy.shape[0]):
                plt.plot(thisxLocs, [controlAccuracy[indMouse, indBand], laserAccuracy[indMouse, indBand]], '-', color=connectColour)

            l1, = plt.plot(np.tile(thisxLocs[1],laserAccuracy.shape[0]), laserAccuracy[:,indBand], 'o', color=controlColour)
            l2, = plt.plot(np.tile(thisxLocs[0],controlAccuracy.shape[0]), controlAccuracy[:,indBand], 'o', color=baseColour)

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

        axScatter.annotate(panelLabels[type], xy=(labelPosX[0], labelPosY[type]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axScatter.annotate(rowTitles[type], xy=(rowTitleX, rowTitleY[type]), xycoords='figure fraction',
                          fontsize=fontSizePanel, fontweight='bold', color=colours[type], rotation=90)

        # -- stats!! --
        for band in range(len(possibleBands)):
            pVal = stats.wilcoxon(laserAccuracy[:,band], controlAccuracy[:,band])[1]
            print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

# --- comparison in change in bias with laser but not inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']
    possibleBands = summaryData['possibleBands']

    laserBiases = [PVlaserBias, SOMlaserBias]
    controlBiases = [PVcontrolBias, SOMcontrolBias]

    panelLabels = ['C', 'G']

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    yLims = [(-0.55, 0.2), (-0.8, 0.8)]
    xTickLabels = possibleBands
    legendLabels = ['no laser', 'laser']
    colours = [PVColour, SOMColour]

    for type in range(len(laserBiases)):
        axScatter = plt.subplot(gs[type, 2])
        laserBias = laserBiases[type]
        controlBias = controlBiases[type]
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserBias.shape[0]):
                plt.plot(thisxLocs, [controlBias[indMouse, indBand], laserBias[indMouse, indBand]], '-',
                         color=connectColour)

            l1, = plt.plot(np.tile(thisxLocs[1], laserBias.shape[0]), laserBias[:, indBand], 'o', color=controlColour)
            l2, = plt.plot(np.tile(thisxLocs[0], controlBias.shape[0]), controlBias[:, indBand], 'o', color=baseColour)

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        axScatter.legend([l2, l1], legendLabels, loc='best')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (oct)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Bias', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[2], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        # -- stats!! --
        for band in range(len(possibleBands)):
            pVal = stats.wilcoxon(laserBias[:,band], controlBias[:,band])[1]
            print(f"Change in bias at {possibleBands[band]} oct pVal: {pVal}")

# -- comparison of change in accuracy between inactivation and no inactivation conditions --
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVcontrolChangeAccuracy = summaryData['PVcontrolChangeAccuracy']
    PVinactChangeAccuracy = summaryData['PVexpChangeAccuracy']
    SOMcontrolChangeAccuracy = summaryData['SOMcontrolChangeAccuracy']
    SOMinactChangeAccuracy = summaryData['SOMexpChangeAccuracy']

    controlChangesAccuracy = [PVcontrolChangeAccuracy, SOMcontrolChangeAccuracy]
    inactChangesAccuracy = [PVinactChangeAccuracy, SOMinactChangeAccuracy]

    panelLabels = ['B', 'F']
    colours = [PVColour, SOMColour]
    legendLabels = ['no PV', 'no SOM']
    xLocs = range(2)
    yLims = [(-8, 1), (-10, 5)]

    for type in range(len(controlChangesAccuracy)):
        axScatter = plt.subplot(gs[type, 1])
        controlChangeAccuracy = controlChangesAccuracy[type]
        inactChangeAccuracy = inactChangesAccuracy[type]

        for indMouse in range(len(controlChangeAccuracy)):
            plt.plot(xLocs, [controlChangeAccuracy[indMouse], inactChangeAccuracy[indMouse]], '-', color=connectColour)
        plt.plot(np.tile(xLocs[0], len(controlChangeAccuracy)), controlChangeAccuracy, 'o', color=controlColour)
        plt.plot(np.tile(xLocs[1], len(inactChangeAccuracy)), inactChangeAccuracy, 'o', mec=colours[type], mfc='white')

        plt.plot([xLocs[0]-0.2, xLocs[0]+0.2], np.tile(np.median(controlChangeAccuracy),2), '-', color='k', lw=3)
        plt.plot([xLocs[1] - 0.2, xLocs[1] + 0.2], np.tile(np.median(inactChangeAccuracy), 2), '-', color='k', lw=3)

        axScatter.set_xlim(-0.5, 1.5)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(['control', legendLabels[type]], rotation=-45)

        axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Change in accuracy (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        pVal = stats.ranksums(controlChangeAccuracy, inactChangeAccuracy)[1]
        print(f"Control vs inactivation change in accuracy p val = {pVal}")
        if pVal < 0.05:
            extraplots.significance_stars(xLocs, 0.98 * yLims[type][1], 0.03 * np.diff(yLims[type]), gapFactor=0.2)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[1], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# -- comparison of change in bias between inactivation and no inactivation conditions --
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVcontrolChangeBias = summaryData['PVcontrolChangeBias']
    PVinactChangeBias = summaryData['PVexpChangeBias']
    SOMcontrolChangeBias = summaryData['SOMcontrolChangeBias']
    SOMinactChangeBias = summaryData['SOMexpChangeBias']

    controlChangesBias = [PVcontrolChangeBias, SOMcontrolChangeBias]
    inactChangesBias = [PVinactChangeBias, SOMinactChangeBias]

    panelLabels = ['D', 'H']
    colours = [PVColour, SOMColour]
    legendLabels = ['no PV', 'no SOM']
    xLocs = range(2)
    yLims = [(-0.2, 0.15), (-0.3, 0.2)]

    for type in range(len(controlChangesBias)):
        axScatter = plt.subplot(gs[type, 3])
        controlChangeBias = controlChangesBias[type]
        inactChangeBias = inactChangesBias[type]

        for indMouse in range(len(controlChangeBias)):
            plt.plot(xLocs, [controlChangeBias[indMouse], inactChangeBias[indMouse]], '-', color=connectColour)
        plt.plot(np.tile(xLocs[0], len(controlChangeBias)), controlChangeBias, 'o', color=controlColour)
        plt.plot(np.tile(xLocs[1], len(inactChangeBias)), inactChangeBias, 'o', mec=colours[type], mfc='white')

        plt.plot([xLocs[0]-0.2, xLocs[0]+0.2], np.tile(np.median(controlChangeBias),2), '-', color='k', lw=3)
        plt.plot([xLocs[1] - 0.2, xLocs[1] + 0.2], np.tile(np.median(inactChangeBias), 2), '-', color='k', lw=3)

        axScatter.set_xlim(-0.5, 1.5)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(['control', legendLabels[type]], rotation=-45)

        axScatter.set_ylim(yLims[type])
        axScatter.set_ylabel('Change in bias', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

        pVal = stats.ranksums(controlChangeBias, inactChangeBias)[1]
        print(f"Control vs inactivation change in bias p val = {pVal}")
        if pVal<0.05:
            extraplots.significance_stars(xLocs, 0.98*yLims[type][1], 0.03*np.diff(yLims[type]), gapFactor=0.2)

        axScatter.annotate(panelLabels[type], xy=(labelPosX[3], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
