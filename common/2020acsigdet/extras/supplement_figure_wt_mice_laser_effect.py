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
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
BY_BAND = 0 # split data by bandwidth or no?
outputDir = '/tmp/'
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

summaryFileName = 'all_behaviour_inhib_inactivation_v2_wt_mice.npz'

baseColour = figparams.colp['baseline']
controlColour = figparams.colp['control']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
connectColour = figparams.colp['connectLine']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

if BY_BAND:
    figFilename = 'SuppFigX_wt_mice_bands_separated'  # Do not include extension
    figSize = [6, 6]  # In inches

    labelPosX = [0.06, 0.21, 0.37, 0.53, 0.69, 0.83]  # Horiz position for panel labels
    labelPosY = [0.97, 0.49]  # Vert position for panel labels

    gs = gridspec.GridSpec(2, 3)
    gs.update(top=0.99, bottom=0.10, left=0.14, right=0.98, wspace=0.6, hspace=0.3)
else:
    figFilename = 'SuppFigX_wt_mice'  # Do not include extension
    figSize = [5, 6]  # In inches

    labelPosX = [0.04, 0.2, 0.36, 0.51, 0.68, 0.81]  # Horiz position for panel labels
    labelPosY = [0.97, 0.49]  # Vert position for panel labels

    gs = gridspec.GridSpec(2, 3)
    gs.update(top=0.99, bottom=0.05, left=0.16, right=0.99, wspace=0.6, hspace=0.2)

def plot_paired_data(axis, laserData, controlData, yLim, ylabel, legendLabels, colours, possibleBands=None, plot_medians=False):
    barLoc = np.array([-0.24, 0.24])
    if possibleBands is not None:
        xLocs = np.arange(len(possibleBands))
        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(laserData.shape[0]):
                plt.plot(thisxLocs, [controlData[indMouse, indBand], laserData[indMouse, indBand]], '-',
                         color=connectColour)

            l1, = plt.plot(np.tile(thisxLocs[1], laserData.shape[0]), laserData[:, indBand], 'o', color=colours[1])
            l2, = plt.plot(np.tile(thisxLocs[0], controlData.shape[0]), controlData[:, indBand], 'o', color=colours[0])

            # -- stats!! --
            pVal = stats.wilcoxon(laserData[:, indBand], controlData[:, indBand])[1]
            print(f"Change in {ylabel} at {possibleBands[indBand]} oct pVal: {pVal}")
            if pVal<0.05:
                extraplots.significance_stars(thisxLocs, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

            if plot_medians:
                laserMedian = np.median(laserData[:, indBand], axis=0)
                controlMedian = np.median(controlData[:, indBand], axis=0)

                plt.plot(thisxLocs, [controlMedian, laserMedian], 'o-', color='k')

        axis.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axis.set_xticks(xLocs)
        axis.set_xticklabels(np.tile(possibleBands, len(xLocs)))
        axis.set_xlabel('Masker bandwidth (oct)', fontsize=fontSizeLabels)

    else:
        for indMouse in range(laserData.shape[0]):
            plt.plot(barLoc, [controlData[indMouse], laserData[indMouse]], '-', color=connectColour)

        l1, = plt.plot(np.tile(barLoc[1], laserData.shape[0]), laserData, 'o', color=colours[1])
        l2, = plt.plot(np.tile(barLoc[0], controlData.shape[0]), controlData, 'o', color=colours[0])

        if plot_medians:
            laserMedian = np.median(laserData, axis=0)
            controlMedian = np.median(controlData, axis=0)

            plt.plot(barLoc, [controlMedian, laserMedian], 'o-', color='k')

        # -- stats!! --
        pVal = stats.wilcoxon(laserData, controlData)[1]
        print(f"Change in {ylabel} pVal: {pVal}")
        if pVal < 0.05:
            extraplots.significance_stars(barLoc, 0.98 * yLim[1], 0.02 * np.diff(yLim), gapFactor=0.3)

        axis.set_xlim(barLoc[0] - 0.3, barLoc[1] + 0.3)
        axis.set_xticks([])

    axis.legend([l2, l1], legendLabels, loc='best')

    axis.set_ylim(yLim)
    axis.set_ylabel(ylabel, fontsize=fontSizeLabels)

    extraplots.boxoff(axis)
    extraplots.set_ticks_fontsize(axis, fontSizeTicks)

# -- comparison of change in d' between laser in and laser out conditions --
if PANELS[0]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    if BY_BAND:
        PVlaserdprime = summaryData['PVexpLaserdprime']
        PVcontroldprime = summaryData['PVexpNoLaserdprime']
        SOMlaserdprime = summaryData['SOMexpLaserdprime']
        SOMcontroldprime = summaryData['SOMexpNoLaserdprime']

        controlPVlaserdprime = summaryData['PVcontrolLaserdprime']
        controlPVcontroldprime = summaryData['PVcontrolNoLaserdprime']
        controlSOMlaserdprime = summaryData['SOMcontrolLaserdprime']
        controlSOMcontroldprime = summaryData['SOMcontrolNoLaserdprime']
        possibleBands = summaryData['possibleBands']
    else:
        PVlaserdprime = summaryData['PVexpLaserdprimeAllBands']
        PVcontroldprime = summaryData['PVexpNoLaserdprimeAllBands']
        SOMlaserdprime = summaryData['SOMexpLaserdprimeAllBands']
        SOMcontroldprime = summaryData['SOMexpNoLaserdprimeAllBands']

        controlPVlaserdprime = summaryData['PVcontrolLaserdprimeAllBands']
        controlPVcontroldprime = summaryData['PVcontrolNoLaserdprimeAllBands']
        controlSOMlaserdprime = summaryData['SOMcontrolLaserdprimeAllBands']
        controlSOMcontroldprime = summaryData['SOMcontrolNoLaserdprimeAllBands']
        possibleBands = None

    inactChangesdprime = [PVlaserdprime-PVcontroldprime, SOMlaserdprime-SOMcontroldprime]
    controlChangesdprime = [controlPVlaserdprime-controlPVcontroldprime, controlSOMlaserdprime-controlSOMcontroldprime]

    panelLabels = ['B', 'H']
    colours = [PVColour, SOMColour]
    yLims = [(-0.75, 0.5), (-0.5, 0.5)]
    rowTitles = ['PV-Cre mice', 'SOM-Cre mice']
    rowTitleX = 0.01
    rowTitleY = [0.7, 0.2]

    for type in range(len(inactChangesdprime)):
        axCompare = plt.subplot(gs[type, 0])

        inactChange = inactChangesdprime[type]
        controlChange = controlChangesdprime[type]

        thisLabels = ['laser out', 'laser in']
        thisColours = [controlColour, colours[type]]

        plot_paired_data(axCompare, inactChange, controlChange, yLims[type], 'Change in d\'', thisLabels, thisColours, possibleBands)

        axCompare.annotate(panelLabels[type], xy=(labelPosX[1], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

        axCompare.annotate(rowTitles[type], xy=(rowTitleX, rowTitleY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold', color=colours[type], rotation=90)

# -- comparison of change in hit rate between inactivation and no inactivation conditions --
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    if BY_BAND:
        PVlaserHitRate = summaryData['PVexpLaserHits']
        PVcontrolHitRate = summaryData['PVexpNoLaserHits']
        SOMlaserHitRate = summaryData['SOMexpLaserHits']
        SOMcontrolHitRate = summaryData['SOMexpNoLaserHits']

        controlPVlaserHitRate = summaryData['PVcontrolLaserHits']
        controlPVcontrolHitRate = summaryData['PVcontrolNoLaserHits']
        controlSOMlaserHitRate = summaryData['SOMcontrolLaserHits']
        controlSOMcontrolHitRate = summaryData['SOMcontrolNoLaserHits']
        possibleBands = summaryData['possibleBands']
    else:
        PVlaserHitRate = summaryData['PVexpLaserHitsAllBands']
        PVcontrolHitRate = summaryData['PVexpNoLaserHitsAllBands']
        SOMlaserHitRate = summaryData['SOMexpLaserHitsAllBands']
        SOMcontrolHitRate = summaryData['SOMexpNoLaserHitsAllBands']

        controlPVlaserHitRate = summaryData['PVcontrolLaserHitsAllBands']
        controlPVcontrolHitRate = summaryData['PVcontrolNoLaserHitsAllBands']
        controlSOMlaserHitRate = summaryData['SOMcontrolLaserHitsAllBands']
        controlSOMcontrolHitRate = summaryData['SOMcontrolNoLaserHitsAllBands']
        possibleBands = None

    inactChangesHitRate = [PVlaserHitRate-PVcontrolHitRate, SOMlaserHitRate-SOMcontrolHitRate]
    controlChangesdHitRate = [controlPVlaserHitRate-controlPVcontrolHitRate, controlSOMlaserHitRate-controlSOMcontrolHitRate]

    panelLabels = ['D', 'J']
    colours = [PVColour, SOMColour]
    yLims = [(-30, 10), (-30, 10)]

    for type in range(len(inactChangesdprime)):
        axCompare = plt.subplot(gs[type, 1])

        inactChange = inactChangesHitRate[type]
        controlChange = controlChangesdHitRate[type]

        thisLabels = ['laser out', 'laser in']
        thisColours = [controlColour, colours[type]]

        plot_paired_data(axCompare, inactChange, controlChange, yLims[type], 'Change in Hit Rate (%)', thisLabels, thisColours,
                         possibleBands)

        axCompare.annotate(panelLabels[type], xy=(labelPosX[3], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

# -- comparison of change in FA rate between inactivation and no inactivation conditions --
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    if BY_BAND:
        PVlaserFARate = summaryData['PVexpLaserFA']
        PVcontrolFARate = summaryData['PVexpNoLaserFA']
        SOMlaserFARate = summaryData['SOMexpLaserFA']
        SOMcontrolFARate = summaryData['SOMexpNoLaserFA']

        controlPVlaserFARate = summaryData['PVcontrolLaserFA']
        controlPVcontrolFARate = summaryData['PVcontrolNoLaserFA']
        controlSOMlaserFARate = summaryData['SOMcontrolLaserFA']
        controlSOMcontrolFARate = summaryData['SOMcontrolNoLaserFA']
        possibleBands = summaryData['possibleBands']
    else:
        PVlaserFARate = summaryData['PVexpLaserFAallBands']
        PVcontrolFARate = summaryData['PVexpNoLaserFAallBands']
        SOMlaserFARate = summaryData['SOMexpLaserFAallBands']
        SOMcontrolFARate = summaryData['SOMexpNoLaserFAallBands']

        controlPVlaserFARate = summaryData['PVcontrolLaserFAallBands']
        controlPVcontrolFARate = summaryData['PVcontrolNoLaserFAallBands']
        controlSOMlaserFARate = summaryData['SOMcontrolLaserFAallBands']
        controlSOMcontrolFARate = summaryData['SOMcontrolNoLaserFAallBands']
        possibleBands = None

    inactChangesFARate = [PVlaserFARate-PVcontrolFARate, SOMlaserFARate-SOMcontrolFARate]
    controlChangesFARate = [controlPVlaserFARate-controlPVcontrolFARate, controlSOMlaserFARate-controlSOMcontrolFARate]

    panelLabels = ['F', 'L']
    colours = [PVColour, SOMColour]
    yLims = [(-30, 20), (-30, 20)]

    for type in range(len(inactChangesdprime)):
        axCompare = plt.subplot(gs[type, 2])

        inactChange = inactChangesFARate[type]
        controlChange = controlChangesFARate[type]

        thisLabels = ['laser out', 'laser in']
        thisColours = [controlColour, colours[type]]

        plot_paired_data(axCompare, inactChange, controlChange, yLims[type], 'Change in False Alarm Rate (%)', thisLabels, thisColours,
                         possibleBands)

        axCompare.annotate(panelLabels[type], xy=(labelPosX[5], labelPosY[type]), xycoords='figure fraction',
                           fontsize=fontSizePanel, fontweight='bold')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
