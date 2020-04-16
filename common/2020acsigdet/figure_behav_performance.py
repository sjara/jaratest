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
# dataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'FigX_behaviour_characterisation'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
# figFormat = 'svg'
figSize = [8,6]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]  # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]  # Vert position for panel labels

fileName = 'unimplanted_behaviour.npz'
exampleFileName = 'band068_unimplanted_psycurve.npz'

wtColour = figparams.colp['excitatoryCell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 3, width_ratios=[1,0.5,0.5], height_ratios=[0.7,1])
gs.update(top=0.94, bottom=0.10, left=0.07, right=0.98, wspace=0.4, hspace=0.4)

# --- individual psychometric curve ---
if PANELS[0]:
    dataFullPath = os.path.join(dataDir, exampleFileName)
    data = np.load(dataFullPath)

    psyCurve = data['psyCurve']
    upperError = data['upperError']
    lowerError = data['lowerError']
    possibleSNRs = data['possibleSNRs']

    axCurve = plt.subplot(gs[0,2])

    plt.plot(range(len(possibleSNRs)), psyCurve, 'o-', color=wtColour, lw=2, ms=5)
    plt.errorbar(range(len(possibleSNRs)), psyCurve, yerr=[lowerError, upperError], fmt='none',
                 color=wtColour, lw=2, capsize=5, capthick=1)

    axCurve.set_xlim(-0.2, len(possibleSNRs)-0.8)
    axCurve.set_xticks(range(len(possibleSNRs)))
    axCurve.set_xticklabels(possibleSNRs)
    axCurve.set_xlabel('SNR (dB)')

    axCurve.set_ylim(0, 100)
    axCurve.set_ylabel('% tone reported')

    extraplots.boxoff(axCurve)

# -- all psychometric curves --
if PANELS[1]:
    dataFullPath = os.path.join(dataDir, fileName)
    data = np.load(dataFullPath)

    psyCurves = data['allToneDetect']
    accuracies = data['allPercentCorrect']
    possibleSNRs = data['possibleSNRs']

    axCurves = plt.subplot(gs[1,0])
    indsToIgnore = []

    for indCurve in range(psyCurves.shape[0]):
        if all(accuracies[indCurve,:] > 55):
            plt.plot(range(len(possibleSNRs)), psyCurves[indCurve, :], '-', color=wtColour, alpha=0.1, zorder=0)
        else:
            indsToIgnore.append(indCurve)

    curves = np.delete(psyCurves, indsToIgnore, axis=0)
    plt.plot(range(len(possibleSNRs)), np.median(curves, axis=0), 'o-', color=wtColour, lw=3, ms=9, zorder=10)
    # plt.plot(range(len(possibleSNRs)), np.mean(curves, axis=0), 'o-', color=curveColours[indType], lw=3, zorder=10)

    axCurves.set_xlim(-0.2, len(possibleSNRs) - 0.8)
    axCurves.set_xticks(range(len(possibleSNRs)))
    axCurves.set_xticklabels(possibleSNRs)
    axCurves.set_xlabel('SNR (dB)')

    axCurves.set_ylim(0, 100)
    axCurves.set_ylabel('% tone reported')

    extraplots.boxoff(axCurves)


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
    plt.ylabel('Accuracy (%)')
    plt.xlabel('Masker bandwidth (oct)')
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(np.tile(possibleBands,len(xLocs)//2))
    extraplots.boxoff(axScatter)

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
    plt.ylabel('Bias')
    plt.xlabel('Masker bandwidth (oct)')
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(np.tile(possibleBands,len(xLocs)//2))
    extraplots.boxoff(axScatter)

    # -- stats!! --
    pVal = stats.wilcoxon(bias[:, 0], bias[:, 1])[1]
    print("Change in bias between bandwidths p val: {}".format(pVal))

    extraplots.significance_stars(xLocs, yLims[1] * 0.99, yLims[1] * 0.06, gapFactor=0.25)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

#plt.show()
