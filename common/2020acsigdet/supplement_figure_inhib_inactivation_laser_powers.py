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

PANELS = [1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'SuppFigX_inhib_inactivation_laser_powers'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [9,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.04, 0.33, 0.51, 0.79]  # Horiz position for panel labels
labelPosY = [0.97, 0.49]  # Vert position for panel labels

summaryFileName = 'all_behaviour_inhib_inactivation_different_powers.npz'

baseColour = figparams.colp['baseline']
controlColour = figparams.colp['control']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
connectColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2)
gs.update(top=0.99, bottom=0.10, left=0.10, right=0.99, wspace=0.6, hspace=0.3)

# --- summary of change in accuracy across laser powers ---
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']
    possibleBands = summaryData['possibleBands']

    diffAcuracies = [PVlaserAccuracy-PVcontrolAccuracy, SOMlaserAccuracy-SOMcontrolAccuracy]

    panelLabels = ['A', 'E']

    laserPowers = [5,10,15]
    xLocs = np.arange(len(laserPowers))
    xTickLabels = laserPowers
    legendLabels = ['no laser', 'laser']
    colours = [PVColour, SOMColour]
    rowTitles = ['PV-ArchT mice', 'SOM-ArchT mice']
    rowTitleX = 0.01
    rowTitleY = [0.9, 0.4]

    for indBand, band in enumerate(possibleBands):
        axLine = plt.subplot(gs[0, indBand])

        for indType, accuracies in enumerate(diffAcuracies):
            for indMouse in range(accuracies.shape[0]):
                plt.plot(laserPowers, accuracies[indMouse, :, indBand], 'o-', color=colours[indType])

            # l1, = plt.plot(np.tile(thisxLocs[1],laserAccuracy.shape[0]), laserAccuracy[:,indBand], 'o', color=controlColour)
            # l2, = plt.plot(np.tile(thisxLocs[0],controlAccuracy.shape[0]), controlAccuracy[:,indBand], 'o', color=baseColour)

                #median = np.median(accuracyData, axis=0)
                #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        # axScatter.legend([l2, l1], legendLabels, loc='best')
        #
        # axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axLine.set_xticks(laserPowers)
        axLine.set_xticklabels(laserPowers)
        axLine.set_xlabel('Laser Power (mW)', fontsize=fontSizeLabels)

        # axScatter.set_ylim(50, 95)
        axLine.set_ylabel('Change in accuracy (%)', fontsize=fontSizeLabels)

        axLine.set_title(f'{band} octaves')
        extraplots.boxoff(axLine)
        extraplots.set_ticks_fontsize(axLine, fontSizeTicks)

        # axScatter.annotate(panelLabels[type], xy=(labelPosX[0], labelPosY[type]), xycoords='figure fraction',
        #                      fontsize=fontSizePanel, fontweight='bold')
        # axScatter.annotate(rowTitles[type], xy=(rowTitleX, rowTitleY[type]), xycoords='figure fraction',
        #                       fontsize=fontSizePanel, fontweight='bold', color=colours[type], rotation=90)

        # -- stats!! --
        # for band in range(len(possibleBands)):
        #     pVal = stats.wilcoxon(laserAccuracy[:,band], controlAccuracy[:,band])[1]
        #     print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

# --- comparison in change in bias with laser but not inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']
    possibleBands = summaryData['possibleBands']

    diffBiases = [PVlaserBias - PVcontrolBias, SOMlaserBias - SOMcontrolBias]

    panelLabels = ['A', 'E']

    laserPowers = [5, 10, 15]
    xLocs = np.arange(len(laserPowers))
    xTickLabels = laserPowers
    legendLabels = ['no laser', 'laser']
    colours = [PVColour, SOMColour]
    rowTitles = ['PV-ArchT mice', 'SOM-ArchT mice']
    rowTitleX = 0.01
    rowTitleY = [0.9, 0.4]

    for indBand, band in enumerate(possibleBands):
        axLine = plt.subplot(gs[1, indBand])

        for indType, biases in enumerate(diffBiases):
            for indMouse in range(biases.shape[0]):
                plt.plot(laserPowers, biases[indMouse, :, indBand], 'o-', color=colours[indType])

            # l1, = plt.plot(np.tile(thisxLocs[1],laserAccuracy.shape[0]), laserAccuracy[:,indBand], 'o', color=controlColour)
            # l2, = plt.plot(np.tile(thisxLocs[0],controlAccuracy.shape[0]), controlAccuracy[:,indBand], 'o', color=baseColour)

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
        # axScatter.legend([l2, l1], legendLabels, loc='best')
        #
        # axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axLine.set_xticks(laserPowers)
        axLine.set_xticklabels(laserPowers)
        axLine.set_xlabel('Laser Power (mW)', fontsize=fontSizeLabels)

        # axScatter.set_ylim(50, 95)
        axLine.set_ylabel('Change in bias', fontsize=fontSizeLabels)

        axLine.set_title(f'{band} octaves')
        extraplots.boxoff(axLine)
        extraplots.set_ticks_fontsize(axLine, fontSizeTicks)

        # axScatter.annotate(panelLabels[type], xy=(labelPosX[0], labelPosY[type]), xycoords='figure fraction',
        #                      fontsize=fontSizePanel, fontweight='bold')
        # axScatter.annotate(rowTitles[type], xy=(rowTitleX, rowTitleY[type]), xycoords='figure fraction',
        #                       fontsize=fontSizePanel, fontweight='bold', color=colours[type], rotation=90)

        # -- stats!! --
        # for band in range(len(possibleBands)):
        #     pVal = stats.wilcoxon(laserAccuracy[:,band], controlAccuracy[:,band])[1]
        #     print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
