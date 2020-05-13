import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams

FIGNAME = 'figure_inhibitory_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 1, 1, 1]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig3_inhib_inactivation'  # Do not include extension
#figFormat = 'pdf'  # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [9,9]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.003, 0.39, 0.675]  # Horiz position for panel labels
labelPosY = [0.98, 0.64, 0.3]  # Vert position for panel labels

PVInactExample = 'band081_psycurve.npz'
SOMInactExample = 'band065_psycurve.npz'
summaryFileName = 'all_behaviour_inhib_inactivation.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 3, width_ratios=[1.5, 1, 1])
gs.update(top=0.98, bottom=0.05, left=0.07, right=0.94, wspace=0.5, hspace=0.4)

def bootstrap_median_CI(data, reps=1000, interval=95):
    medians = np.zeros(reps)
    for ind in range(reps):
        samples = np.random.choice(data, len(data), replace=True)
        medians[ind] = np.median(samples)
    low = np.percentile(medians,(100-interval)/2.0)
    high = np.percentile(medians,interval+(100-interval)/2.0)
    return [low, high]

# --- example psychometric curves ---
if PANELS[0]:
    examples = [PVInactExample, SOMInactExample]
    cellTypeColours = [PVColour, SOMColour]
    labels = ['no PV', 'no SOM']
    panelLabels = ['A', 'D']

    for indType, exampleFileName in enumerate(examples):
        dataFullPath = os.path.join(inactDataDir, exampleFileName)
        data = np.load(dataFullPath)

        axCurve = plt.subplot(gs[indType, 0])

        psyCurveControl = data['psyCurveControl']
        upperErrorControl = data['upperErrorControl']
        lowerErrorControl = data['lowerErrorControl']
        possibleSNRs = data['possibleSNRs']

        l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=ExcColour, lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveControl, yerr=[lowerErrorControl, upperErrorControl], fmt='none',
                     color=ExcColour, lw=2, capsize=5, capthick=1)

        psyCurveLaser = data['psyCurveLaser']
        upperErrorLaser = data['upperErrorLaser']
        lowerErrorLaser = data['lowerErrorLaser']

        l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveLaser, yerr=[lowerErrorLaser, upperErrorLaser], fmt='none',
                     color=cellTypeColours[indType], lw=2, capsize=5, capthick=1, zorder=-10)

        axCurve.legend([l1, l2], ['control', labels[indType]])

        axCurve.set_xlim(-0.2, len(possibleSNRs) - 0.8)
        axCurve.set_xticks(range(len(possibleSNRs)))
        axCurve.set_xticklabels(possibleSNRs)
        axCurve.set_xlabel('SNR (dB)', fontsize=fontSizeLabels)

        axCurve.set_ylim(0, 100)
        axCurve.set_ylabel('Trials with tone reported (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axCurve)
        extraplots.breakaxis(0.5, 0, 0.15, 5, gap=0.5)
        extraplots.set_ticks_fontsize(axCurve, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axCurve.annotate(label, xy=(labelPosX[0], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in accuracy during PV or SOM inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    panelLabels = ['B', 'E']

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']
    possibleBands = summaryData['possibleBands']

    colours = [PVColour, SOMColour]
    accuracyData = [[PVcontrolAccuracy, PVlaserAccuracy], [SOMcontrolAccuracy, SOMlaserAccuracy]]

    for indType, accuracies in enumerate(accuracyData):
        axScatter = plt.subplot(gs[indType,1])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(accuracies[0].shape[0]):
                plt.plot(thisxLocs, [accuracies[0][indMouse, indBand], accuracies[1][indMouse, indBand]], '-', color=ExcColour)

            plt.plot(np.tile(thisxLocs[0],accuracies[0].shape[0]), accuracies[0][:,indBand], 'o', color=ExcColour)
            plt.plot(np.tile(thisxLocs[1],accuracies[1].shape[0]), accuracies[1][:,indBand], 'o', mec=colours[indType], mfc='white')

            #median = np.median(accuracyData, axis=0)
            #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (octaves)', fontsize=fontSizeLabels)

        axScatter.set_ylim(50, 80)
        axScatter.set_ylabel('Accuracy (%)', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[1], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- comparison in change in accuracy with PV and SOM inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']
    possibleBands = summaryData['possibleBands']

    PVchange = PVlaserAccuracy - PVcontrolAccuracy
    SOMchange = SOMlaserAccuracy - SOMcontrolAccuracy

    axBar = plt.subplot(gs[2,1])
    cartoonLabel = 'G'
    panelLabel = 'H'

    cellTypeColours = [PVColour, SOMColour]

    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)
    xTickLabels = possibleBands

    changeAccuracy = [PVchange, SOMchange]
    medianChangeAccuracy = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]
    #changeCIs = [bootstrap_median_CI(PVchange), bootstrap_median_CI(SOMchange)]
    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangeAccuracy)):
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangeAccuracy[indType][indBand], medianChangeAccuracy[indType][indBand]],
                     color=cellTypeColours[indType], linewidth=3)  # medians

            accuracyCI = bootstrap_median_CI(changeAccuracy[indType][:,indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], accuracyCI,
                     color=cellTypeColours[indType], linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [accuracyCI[0], accuracyCI[0]], color=cellTypeColours[indType], linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [accuracyCI[1], accuracyCI[1]], color=cellTypeColours[indType], linewidth=1.5)  # top caps
    plt.plot([-10, 10], [0, 0], '--', color='0.5')  # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(possibleBands)
    axBar.set_xlabel('Masker bandwidth (octaves)', fontsize=fontSizeLabels)

    yLims = (-12, 2)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in accuracy (%)', fontsize=fontSizeLabels)

    extraplots.boxoff(axBar)
    extraplots.set_ticks_fontsize(axBar, fontSizeTicks)

    for band in range(len(possibleBands)):
        pVal = stats.ranksums(PVchange[:, band], SOMchange[:, band])
        print(f'PV accuracy change vs SOM accuracy change for bw {possibleBands[band]} p val: {pVal}')

    # extraplots.significance_stars(barLoc + xLocs[0], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)
    # extraplots.significance_stars(barLoc + xLocs[1], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

    axBar.annotate(panelLabel, xy=(labelPosX[1], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                     fontweight='bold')
    axBar.annotate(cartoonLabel, xy=(labelPosX[0], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

# --- comparison in change in bias with PV and SOM inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    panelLabels = ['C', 'F']

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']
    possibleBands = summaryData['possibleBands']

    colours = [PVColour, SOMColour]
    biasData = [[PVcontrolBias, PVlaserBias], [SOMcontrolBias, SOMlaserBias]]

    for indType, biases in enumerate(biasData):
        axScatter = plt.subplot(gs[indType, 2])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(biases[0].shape[0]):
                plt.plot(thisxLocs, [biases[0][indMouse, indBand], biases[1][indMouse, indBand]], '-',
                         color=ExcColour)

            plt.plot(np.tile(thisxLocs[0], biases[0].shape[0]), biases[0][:, indBand], 'o', color=ExcColour)
            plt.plot(np.tile(thisxLocs[1], biases[1].shape[0]), biases[1][:, indBand], 'o',
                     mec=colours[indType], mfc='white')

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
        axScatter.set_xlabel('Masker bandwidth (octaves)', fontsize=fontSizeLabels)

        axScatter.set_ylim(-0.75,0.4)
        axScatter.set_ylabel('Bias', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in bias towards one side during PV or SOM inactivation ---
if PANELS[4]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    panelLabel = 'I'

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']

    PVchange = PVlaserBias - PVcontrolBias
    SOMchange = SOMlaserBias - SOMcontrolBias

    axBar = plt.subplot(gs[2,2])

    cellTypeColours = [PVColour, SOMColour]

    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)
    xTickLabels = possibleBands

    changeBias = [PVchange, SOMchange]
    medianChangeBias = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]
    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangeBias)):
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangeBias[indType][indBand], medianChangeBias[indType][indBand]],
                     color=cellTypeColours[indType], linewidth=3)  # medians

            biasCI = bootstrap_median_CI(changeBias[indType][:, indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], biasCI,
                     color=cellTypeColours[indType], linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [biasCI[0], biasCI[0]], color=cellTypeColours[indType], linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [biasCI[1], biasCI[1]], color=cellTypeColours[indType], linewidth=1.5)  # top caps
    plt.plot([-10,10], [0,0], '--', color='0.5') # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(possibleBands)
    axBar.set_xlabel('Masker bandwidth (octaves)', fontsize=fontSizeLabels)

    yLims = (-0.5, 0.3)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in bias', fontsize=fontSizeLabels)

    extraplots.boxoff(axBar)
    extraplots.set_ticks_fontsize(axBar, fontSizeTicks)

    axBar.annotate(panelLabel, xy=(labelPosX[2], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

    # calculate those stats!
    for band in range(len(possibleBands)):
        pVal = stats.ranksums(PVchange[:,band], SOMchange[:,band])
        print(f'PV bias change vs SOM bias change for bw {possibleBands[band]} p val: {pVal}')

    extraplots.significance_stars(barLoc + xLocs[0], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)
    extraplots.significance_stars(barLoc + xLocs[1], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
