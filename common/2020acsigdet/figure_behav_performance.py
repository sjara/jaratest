import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

FIGNAME = 'figure_characterise_behaviour'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig1_behaviour_characterisation'  # Do not include extension
#figFormat = 'pdf'  # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [8,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.37, 0.62, 0.45, 0.715]  # Horiz position for panel labels
labelPosY = [0.96, 0.53]  # Vert position for panel labels

fileName = 'unimplanted_behaviour.npz'
exampleFileName = 'band068_unimplanted_psycurve.npz'

wtColour = figparams.colp['baseline']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3, width_ratios=[1,0.5,0.5], height_ratios=[0.7,1])
gs.update(top=0.96, bottom=0.08, left=0.08, right=0.97, wspace=0.4, hspace=0.4)

axCartoons = gs[0, :]
gs2 = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=axCartoons, wspace=0.3, hspace=0.4)

# --- individual psychometric curve ---
if PANELS[0]:
    dataFullPath = os.path.join(dataDir, exampleFileName)
    data = np.load(dataFullPath)

    psyCurve = data['psyCurve']
    upperError = data['upperError']
    lowerError = data['lowerError']
    possibleSNRs = data['possibleSNRs']

    axCurve = plt.subplot(gs2[0,2])
    panelLabels = ['A', 'B', 'C'] # labels for psy curve and cartoons
    xTickLabels = ['-inf']
    xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])

    xVals = range(len(possibleSNRs))
    plt.plot(xVals[:2], psyCurve[:2], 'o--', color=wtColour, lw=2, ms=5)
    plt.plot(xVals[1:], psyCurve[1:], 'o-', color=wtColour, lw=2, ms=5)
    plt.errorbar(range(len(possibleSNRs)), psyCurve, yerr=[lowerError, upperError], fmt='none',
                 color=wtColour, lw=2, capsize=5, capthick=1)

    axCurve.set_xlim(-0.2, len(possibleSNRs)-0.8)
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


# -- all psychometric curves --
if PANELS[1]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    psyCurves = data['allToneDetect']
    accuracies = data['allPercentCorrect']
    possibleSNRs = data['possibleSNRs']

    axCurves = plt.subplot(gs[1,0])
    indsToIgnore = []

    panelLabel = 'D'
    xTickLabels = ['-inf']
    xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])

    for indCurve in range(psyCurves.shape[0]):
        if all(accuracies[indCurve,:] > 55):
            plt.plot(range(len(possibleSNRs)), psyCurves[indCurve, :], '-', color=wtColour, alpha=0.1, zorder=0)
        else:
            indsToIgnore.append(indCurve)

    curves = np.delete(psyCurves, indsToIgnore, axis=0)
    medianCurve = np.median(curves, axis=0)
    xVals = range(len(possibleSNRs))
    plt.plot(xVals[:2], medianCurve[:2], 'o--', color=wtColour, lw=3, ms=9, zorder=10)
    plt.plot(xVals[1:], medianCurve[1:], 'o-', color=wtColour, lw=3, ms=9, zorder=10)

    axCurves.set_xlim(-0.2, len(possibleSNRs) - 0.8)
    axCurves.set_xticks(range(len(possibleSNRs)))
    axCurves.set_xticklabels(xTickLabels)
    axCurves.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

    axCurves.set_ylim(0, 100)
    axCurves.set_ylabel('Trials with tone reported (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axCurves)
    extraplots.breakaxis(0.5, 0, 0.15, 5, gap=0.5)
    extraplots.set_ticks_fontsize(axCurves, fontSizeTicks)

    axCurves.annotate(panelLabel, xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')


# -- summaries of accuracy by bandwidth --
if PANELS[2]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    accuracy = data['allPercentCorrect']
    possibleBands = data['possibleBands']

    axScatter = plt.subplot(gs[1,1])

    barWidth = 0.2
    xLocs = np.arange(len(possibleBands))
    indsToIgnore = []

    edgeColour = matplotlib.colors.colorConverter.to_rgba(wtColour, alpha=0.1)
    panelLabel = 'E'

    for indMouse in range(accuracy.shape[0]):
        if all(accuracy[indMouse, :] > 55):
            plt.plot(xLocs, accuracy[indMouse,:], 'o-', color=edgeColour)
        else:
            indsToIgnore.append(indMouse)

    accuracy = np.delete(accuracy, indsToIgnore, axis=0)
    median = np.median(accuracy, axis=0)
    plt.plot(xLocs, median, 'o-', color='k', lw=3, ms=9)

    yLims = [45, 100]
    plt.ylim(yLims)
    plt.xlim(xLocs[0] - 0.3, xLocs[-1] + 0.3)
    plt.ylabel('Accuracy (%)', fontsize=fontSizeLabels)
    plt.xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(xTickLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[3], labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    pVal = stats.wilcoxon(accuracy[:,0], accuracy[:,1])[1]
    print("Change in accuracy between bandwidths p val: {}".format(pVal))

    extraplots.significance_stars(xLocs, yLims[1] * 0.99, yLims[1] * 0.02, gapFactor=0.25)

if PANELS[3]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    bias = data['allBias']
    accuracy = data['allPercentCorrect']
    possibleBands = data['possibleBands']

    axScatter = plt.subplot(gs[1,2])

    barWidth = 0.2
    xLocs = np.arange(len(possibleBands))
    indsToIgnore = []

    edgeColour = matplotlib.colors.colorConverter.to_rgba(wtColour, alpha=0.1)
    panelLabel = 'F'

    for indMouse in range(bias.shape[0]):
        if all(accuracy[indMouse, :] > 55):
            plt.plot(xLocs, bias[indMouse, :], 'o-', color=edgeColour)
        else:
            indsToIgnore.append(indMouse)

    bias = np.delete(bias, indsToIgnore, axis=0)
    median = np.median(bias, axis=0)
    plt.plot(xLocs, median, 'o-', color='k', lw=3, ms=9)

    yLims = [-0.8, 0.8]
    plt.ylim(yLims)
    plt.xlim(xLocs[0] - 0.3, xLocs[-1] + 0.3)
    plt.ylabel('Bias Index', fontsize=fontSizeLabels)
    plt.xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(xTickLabels)

    extraplots.boxoff(axScatter)
    extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    axScatter.annotate(panelLabel, xy=(labelPosX[4], labelPosY[1]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')

    # -- stats!! --
    pVal = stats.wilcoxon(bias[:, 0], bias[:, 1])[1]
    print("Change in bias between bandwidths p val: {}".format(pVal))

    extraplots.significance_stars(xLocs, yLims[1] * 0.99, yLims[1] * 0.06, gapFactor=0.25)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

#plt.show()
