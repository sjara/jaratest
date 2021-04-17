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

PANELS = [1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig1_behaviour_characterisation'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6.92,2.2]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.27, 0.45, 0.72]  # Horiz position for panel labels
labelPosY = [0.92]  # Vert position for panel labels

fileName = 'unimplanted_behaviour_v2.npz'
exampleFileName = 'band068_unimplanted_psycurve.npz'

wtColour = figparams.colp['baseline']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3, width_ratios=[1.2,0.5,0.5])
gs.update(top=0.86, bottom=0.2, left=0.08, right=0.97, wspace=0.6, hspace=0.2)

# --- individual psychometric curve ---
if PANELS[0]:
    dataFullPath = os.path.join(dataDir, exampleFileName)
    data = np.load(dataFullPath)

    psyCurve = data['psyCurve']
    upperError = data['upperError']
    lowerError = data['lowerError']
    possibleSNRs = data['possibleSNRs']

    axCurve = plt.subplot(gs[0,1])
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

    axCurves = plt.subplot(gs[0,2])
    indsToIgnore = []

    panelLabel = 'D'
    xTickLabels = ['-inf']
    xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])

    for indCurve in range(psyCurves.shape[0]):
        if all(accuracies[indCurve,:] > 60):
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

    axCurves.annotate(panelLabel, xy=(labelPosX[3], labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')

    # -- print out stats to include in paper --
    dprimes = data['alldprimes']
    hitRates = data['allHitRate']
    FARates = data['allFArate']

    bands = ['0.25', 'inf']

    for band in range(2):
        print(f'Median d\' for {bands[band]} octaves: {np.median(dprimes[:,band])}')
        print(f'Median hit rate for {bands[band]} octaves: {np.median(hitRates[:, band])}')
        print(f'Median FA rate for {bands[band]} octaves: {np.median(FARates[:, band])}')

    print(f'd\' by band pVal: {stats.wilcoxon(dprimes[:,0], dprimes[:,1])}')
    print(f'Hit rate by band pVal: {stats.wilcoxon(hitRates[:, 0], hitRates[:, 1])}')
    print(f'FA rate by band pVal: {stats.wilcoxon(FARates[:, 0], FARates[:, 1])}')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

#plt.show()
