import os

import figparams
import matplotlib.colors
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import studyparams
from jaratoolbox import extraplots
from jaratoolbox import settings

FIGNAME = 'figure_characterise_behaviour'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'FigX_behaviour_characterisation_by_strain'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
# figFormat = 'svg'
figSize = [8,4]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]  # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]  # Vert position for panel labels

fileName = 'unimplanted_behaviour.npz'

wtColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']
PVCHR2Colour = figparams.colp['sound']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,3, width_ratios=[1, 1, 1.4])
gs.update(top=0.94, bottom=0.10, left=0.07, right=0.98, wspace=0.3, hspace=0.5)

# --- individual psychometric curve ---
if PANELS[0]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    PVCHR2psyCurves = data['PVCHR2toneDetect']
    PVARCHTpsyCurves = data['PVARCHTtoneDetect']
    SOMARCHTpsyCurves = data['SOMARCHTtoneDetect']
    wtPsyCurves = data['wtToneDetect']

    possibleSNRs = data['possibleSNRs']

    psyCurves = [wtPsyCurves, PVCHR2psyCurves, PVARCHTpsyCurves, SOMARCHTpsyCurves]
    curveColours = [wtColour, PVCHR2Colour, PVColour, SOMColour]
    curveLabels = ['wild-type', 'PV::ChR2', 'PV::ArchT', 'SOM::ArchT']

    for indType, curves in enumerate(psyCurves):
        axCurves = plt.subplot(gs[indType//2,indType%2])

        for indCurve in range(curves.shape[0]):
            plt.plot(range(len(possibleSNRs)), curves[indCurve,:], '-', color=curveColours[indType], alpha=0.3, zorder=0)

        plt.plot(range(len(possibleSNRs)), np.median(curves, axis=0), 'o-', color=curveColours[indType], lw=3, zorder=10)
        #plt.plot(range(len(possibleSNRs)), np.mean(curves, axis=0), 'o-', color=curveColours[indType], lw=3, zorder=10)

        axCurves.set_xlim(-0.2, len(possibleSNRs)-0.8)
        axCurves.set_xticks(range(len(possibleSNRs)))
        axCurves.set_xticklabels(possibleSNRs)
        if indType//2:
            axCurves.set_xlabel('SNR (dB)')

        axCurves.set_ylim(0, 100)
        if indType%2==0:
            axCurves.set_ylabel('% tone reported')

        axCurves.set_title(curveLabels[indType])

        extraplots.boxoff(axCurves)

# -- summaries of accuracy by bandwidth --
if PANELS[1]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    PVCHR2accuracy = data['PVCHR2correctByBand']
    PVARCHTaccuracy = data['PVARCHTcorrectByBand']
    SOMARCHTaccuracy = data['SOMARCHTcorrectByBand']
    wtAccuracy = data['wtCorrectByBand']

    possibleBands = data['possibleBands']
    bandsToUse = [0,-1] # using first and last bands because PV-ChR2 mice had a third intermediate bandwidth

    accuracies = [wtAccuracy, PVCHR2accuracy, PVARCHTaccuracy, SOMARCHTaccuracy]
    colours = [wtColour, PVCHR2Colour, PVColour, SOMColour]
    labels = ['wild-type', 'PV::ChR2', 'PV::ArchT', 'SOM::ArchT']

    axScatter = plt.subplot(gs[0,2])

    barWidth = 0.2
    barLoc = np.array([-0.22, 0.22])
    xLocs = np.arange(4)
    xTicks = []
    xTickLabels = possibleBands[bandsToUse]

    for indType, accuracyData in enumerate(accuracies):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(colours[indType], alpha=0.5)

        thisxLocs = barLoc + xLocs[indType]
        xTicks.extend(thisxLocs)

        for indMouse in range(accuracyData.shape[0]):
            plt.plot(thisxLocs, np.reshape(accuracyData[indMouse,bandsToUse],(2,1)), 'o-', color=colours[indType], alpha=0.3)

        median = np.median(accuracyData, axis=0)
        plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

        # for indBand, band in enumerate(bandsToUse):
        #     xvals = np.repeat(thisxLocs[indBand], accuracyData.shape[0])
        #     jitterAmt = np.random.random(len(xvals))
        #     xvals = xvals + (barWidth * jitterAmt) - barWidth / 2
        #
        #     plt.plot(xvals, accuracyData[:,band], 'o', mec=edgeColour, mfc='none', clip_on=False, markeredgewidth=1.3)
        #     median = np.median(accuracyData[:,band])
        #     plt.plot([thisxLocs[indBand] - barWidth / 2, thisxLocs[indBand] + barWidth / 2], [median, median], '-', color='k', mec=edgeColour, lw=3)

    # ExPatch = patches.Patch(color=ExColor, label='Exc.')
    # PVPatch = patches.Patch(color=PVColor, label=r'PV$^+$')
    # SOMPatch = patches.Patch(color=SOMColor, label=r'SOM$^+$')
    # plt.legend(handles=[ExPatch, PVPatch, SOMPatch], frameon=False, fontsize=fontSizeLabels, loc='best')

    plt.ylim(45,100)
    plt.xlim(xTicks[0] - 0.3, xTicks[-1] + 0.3)
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Masker bandwidth (octaves)')
    axScatter.set_xticks(xTicks)
    axScatter.set_xticklabels(np.tile(xTickLabels,len(xTicks)//2))
    extraplots.boxoff(axScatter)

if PANELS[2]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    PVCHR2bias = data['PVCHR2biasByBand']
    PVARCHTbias = data['PVARCHTbiasByBand']
    SOMARCHTbias = data['SOMARCHTbiasByBand']
    wtBias = data['wtBiasByBand']

    possibleBands = data['possibleBands']
    bandsToUse = [0,-1] # using first and last bands because PV-ChR2 mice had a third intermediate bandwidth

    biases = [wtBias, PVCHR2bias, PVARCHTbias, SOMARCHTbias]
    colours = [wtColour, PVCHR2Colour, PVColour, SOMColour]
    labels = ['wild-type', 'PV::ChR2', 'PV::ArchT', 'SOM::ArchT']

    axScatter = plt.subplot(gs[1,2])

    barWidth = 0.2
    barLoc = np.array([-0.22, 0.22])
    xLocs = np.arange(4)
    xTicks = []
    xTickLabels = possibleBands[bandsToUse]

    for indType, biasData in enumerate(biases):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(colours[indType], alpha=0.5)

        thisxLocs = barLoc + xLocs[indType]
        xTicks.extend(thisxLocs)

        for indMouse in range(biasData.shape[0]):
            plt.plot(thisxLocs, np.reshape(biasData[indMouse,bandsToUse],(2,1)), 'o-', color=colours[indType], alpha=0.3)

        median = np.median(biasData, axis=0)
        plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

    # ExPatch = patches.Patch(color=ExColor, label='Exc.')
    # PVPatch = patches.Patch(color=PVColor, label=r'PV$^+$')
    # SOMPatch = patches.Patch(color=SOMColor, label=r'SOM$^+$')
    # plt.legend(handles=[ExPatch, PVPatch, SOMPatch], frameon=False, fontsize=fontSizeLabels, loc='best')

    plt.ylim(-1,1)
    plt.xlim(xTicks[0] - 0.3, xTicks[-1] + 0.3)
    plt.ylabel('Bias')
    plt.xlabel('Masker bandwidth (octaves)')
    axScatter.set_xticks(xTicks)
    axScatter.set_xticklabels(np.tile(xTickLabels,len(xTicks)//2))
    extraplots.boxoff(axScatter)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

#plt.show()
