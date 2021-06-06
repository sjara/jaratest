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
CORRECTED = 0
SIG_CONTROL_REMOVED = 1
outputDir = '/tmp/'
if CORRECTED:
    figFilename = 'Fig3_inhib_inactivation_corrected'
else:
    figFilename = 'Fig3_inhib_inactivation'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
#figFormat = 'svg'
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
controlFileName = 'all_behaviour_inhib_inactivation_control.npz'

baseColour = figparams.colp['baseline']
PVColour = figparams.colp['PVmanip']
SOMColour = figparams.colp['SOMmanip']
controlColour = figparams.colp['control']

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

        psyCurveControl = data['psyCurveLaserInControl']
        upperErrorControl = data['upperErrorLaserInControl']
        lowerErrorControl = data['lowerErrorLaserInControl']
        possibleSNRs = data['possibleSNRs']

        xVals = range(len(possibleSNRs))
        plt.plot(xVals[:2], psyCurveControl[:2], 'o--', color=baseColour, lw=3, ms=8, zorder=10)
        l1, = plt.plot(xVals[1:], psyCurveControl[1:], 'o-', color=baseColour, lw=3, ms=8, zorder=10)
        #l1, = plt.plot(range(len(possibleSNRs)), psyCurveControl, 'o-', color=ExcColour, lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveControl, yerr=[lowerErrorControl, upperErrorControl], fmt='none',
                     color=baseColour, lw=2, capsize=5, capthick=1)

        psyCurveLaser = data['psyCurveLaserIn']
        upperErrorLaser = data['upperErrorLaserIn']
        lowerErrorLaser = data['lowerErrorLaserIn']

        plt.plot(xVals[:2], psyCurveLaser[:2], 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8, zorder=10)
        l2, = plt.plot(xVals[1:], psyCurveLaser[1:], 'o-', color=cellTypeColours[indType], mfc='white', lw=3, ms=8, zorder=10)
        #l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveLaser, yerr=[lowerErrorLaser, upperErrorLaser], fmt='none',
                     color=cellTypeColours[indType], lw=2, capsize=5, capthick=1, zorder=-10)

        psyCurveLaserOut = data['psyCurveLaserOut']
        upperErrorLaserOut = data['upperErrorLaserOut']
        lowerErrorLaserOut = data['lowerErrorLaserOut']

        plt.plot(xVals[:2], psyCurveLaserOut[:2], 'o--', color=controlColour, mfc='white', lw=3, ms=8, zorder=10)
        l3, = plt.plot(xVals[1:], psyCurveLaserOut[1:], 'o-', color=controlColour, mfc='white', lw=3, ms=8, zorder=10)
        # l2, = plt.plot(range(len(possibleSNRs)), psyCurveLaser, 'o--', color=cellTypeColours[indType], mfc='white', lw=3, ms=8)
        plt.errorbar(range(len(possibleSNRs)), psyCurveLaserOut, yerr=[lowerErrorLaserOut, upperErrorLaserOut], fmt='none',
                     color=controlColour, lw=2, capsize=5, capthick=1, zorder=-10)

        axCurve.legend([l1, l2, l3], ['no laser', labels[indType], 'laser out'])

        axCurve.set_xlim(-0.2, len(possibleSNRs) - 0.8)
        axCurve.set_xticks(range(len(possibleSNRs)))
        xTickLabels = ['-inf']
        xTickLabels.extend([int(x) for x in possibleSNRs.tolist()[1:]])
        axCurve.set_xticklabels(xTickLabels)
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

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        summaryControlDataFullPath = os.path.join(inactDataDir, controlFileName)
        summaryControlData = np.load(summaryControlDataFullPath)

        PVlaserAccuracyControl = summaryControlData['PVlaserAccuracy']
        PVcontrolAccuracyControl = summaryControlData['PVcontrolAccuracy']
        SOMlaserAccuracyControl = summaryControlData['SOMlaserAccuracy']
        SOMcontrolAccuracyControl = summaryControlData['SOMcontrolAccuracy']

        PVlaserAccuracyCorrected = PVlaserAccuracy - (PVlaserAccuracyControl - PVcontrolAccuracyControl)
        SOMlaserAccuracyCorrected = SOMlaserAccuracy - (SOMlaserAccuracyControl - SOMcontrolAccuracyControl)

        accuracyData = [[PVcontrolAccuracy, PVlaserAccuracyCorrected], [SOMcontrolAccuracy, SOMlaserAccuracyCorrected]]

    else:
        accuracyData = [[PVcontrolAccuracy, PVlaserAccuracy], [SOMcontrolAccuracy, SOMlaserAccuracy]]

    panelLabels = ['B', 'E']
    colours = [PVColour, SOMColour]

    for indType, accuracies in enumerate(accuracyData):
        axScatter = plt.subplot(gs[indType,1])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(accuracies[0].shape[0]):
                plt.plot(thisxLocs, [accuracies[0][indMouse, indBand], accuracies[1][indMouse, indBand]], '-', color=baseColour)

            plt.plot(np.tile(thisxLocs[0],accuracies[0].shape[0]), accuracies[0][:,indBand], 'o', color=baseColour)
            plt.plot(np.tile(thisxLocs[1],accuracies[1].shape[0]), accuracies[1][:,indBand], 'o', mec=colours[indType], mfc='white')

            #median = np.median(accuracyData, axis=0)
            #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

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

    if CORRECTED:
        controlDataFullPath = os.path.join(inactDataDir, controlFileName)
        controlData = np.load(controlDataFullPath)

        controlPVlaserAccuracy = controlData['PVlaserAccuracy']
        controlPVcontrolAccuracy = controlData['PVcontrolAccuracy']
        controlSOMlaserAccuracy = controlData['SOMlaserAccuracy']
        controlSOMcontrolAccuracy = controlData['SOMcontrolAccuracy']

        controlPVchange = controlPVlaserAccuracy - controlPVcontrolAccuracy
        controlSOMchange = controlSOMlaserAccuracy - controlSOMcontrolAccuracy

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changeAccuracy = [correctedPVchange, correctedSOMchange]
        medianChangeAccuracy = [np.median(correctedPVchange, axis=0), np.median(correctedSOMchange, axis=0)]
    else:
        changeAccuracy = [PVchange, SOMchange]
        medianChangeAccuracy = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]

    axBar = plt.subplot(gs[2,1])
    cartoonLabel = 'G'
    panelLabel = 'H'

    cellTypeColours = [PVColour, SOMColour]

    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)
    xTickLabels = possibleBands

    #changeCIs = [bootstrap_median_CI(PVchange), bootstrap_median_CI(SOMchange)]
    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangeAccuracy)):
            jitter = 0.8 * width * (np.random.random(len(changeAccuracy[indType])) - 0.5)
            plt.plot(np.tile(xLocs[indBand] + barLoc[indType], len(changeAccuracy[indType])) + jitter,
                     changeAccuracy[indType][:, indBand], 'o', mec=cellTypeColours[indType], mfc='white')

            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangeAccuracy[indType][indBand], medianChangeAccuracy[indType][indBand]],
                     color='k', linewidth=3, zorder=10)  # medians

            accuracyCI = bootstrap_median_CI(changeAccuracy[indType][:,indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], accuracyCI,
                     color='k', linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [accuracyCI[0], accuracyCI[0]], color='k', linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [accuracyCI[1], accuracyCI[1]], color='k', linewidth=1.5)  # top caps
    plt.plot([-10, 10], [0, 0], '--', color='0.5', zorder=0)  # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(xTickLabels)
    axBar.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    yLims = (-8, 7)
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

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']
    possibleBands = summaryData['possibleBands']

    if CORRECTED:
        summaryControlDataFullPath = os.path.join(inactDataDir, controlFileName)
        summaryControlData = np.load(summaryControlDataFullPath)

        PVlaserBiasControl = summaryControlData['PVlaserBias']
        PVcontrolBiasControl = summaryControlData['PVcontrolBias']
        SOMlaserBiasControl = summaryControlData['SOMlaserBias']
        SOMcontrolBiasControl = summaryControlData['SOMcontrolBias']

        PVlaserBiasCorrected = PVlaserBias - (PVlaserBiasControl - PVcontrolBiasControl)
        SOMlaserBiasCorrected = SOMlaserBias - (SOMlaserBiasControl - SOMcontrolBiasControl)

        biasData = [[PVcontrolBias, PVlaserBiasCorrected], [SOMcontrolBias, SOMlaserBiasCorrected]]

    else:
        biasData = [[PVcontrolBias, PVlaserBias], [SOMcontrolBias, SOMlaserBias]]

    panelLabels = ['C', 'F']
    colours = [PVColour, SOMColour]
    yLims = [(-0.55,0.4),(-0.75,0.75)]
    legendLabels = ['no PV', 'no SOM']

    for indType, biases in enumerate(biasData):
        axScatter = plt.subplot(gs[indType, 2])

        barLoc = np.array([-0.24, 0.24])
        xLocs = np.arange(2)
        xTickLabels = possibleBands

        for indBand in range(len(possibleBands)):
            thisxLocs = barLoc + xLocs[indBand]

            for indMouse in range(biases[0].shape[0]):
                plt.plot(thisxLocs, [biases[0][indMouse, indBand], biases[1][indMouse, indBand]], '-',
                         color=baseColour)

            plt.plot(np.tile(thisxLocs[0], biases[0].shape[0]), biases[0][:, indBand], 'o', color=baseColour)
            plt.plot(np.tile(thisxLocs[1], biases[1].shape[0]), biases[1][:, indBand], 'o',
                     mec=colours[indType], mfc='white')

            # median = np.median(accuracyData, axis=0)
            # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')

            # calculate those stats!
            pVal = stats.wilcoxon(biases[0][:, indBand], biases[1][:, indBand])
            print(f'{legendLabels[indType]} bias change for bw {possibleBands[indBand]} p val: {pVal}')

            if pVal[1] < 0.05:
                extraplots.significance_stars(thisxLocs, yLims[indType][1] * 1.03, yLims[indType][1] * 0.02, gapFactor=0.25)

        axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
        axScatter.set_xticks(xLocs)
        xTickLabels = possibleBands.tolist()
        xTickLabels[-1] = 'WN'
        axScatter.set_xticks(xLocs)
        axScatter.set_xticklabels(xTickLabels)
        axScatter.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

        axScatter.set_ylim(yLims[indType])
        axScatter.set_ylabel('Bias Index', fontsize=fontSizeLabels)

        extraplots.boxoff(axScatter)
        extraplots.set_ticks_fontsize(axScatter, fontSizeTicks)

    for indLabel, label in enumerate(panelLabels):
        axScatter.annotate(label, xy=(labelPosX[2], labelPosY[indLabel]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- summary of change in bias towards one side during PV or SOM inactivation ---
if PANELS[4]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']

    PVchange = PVlaserBias - PVcontrolBias
    SOMchange = SOMlaserBias - SOMcontrolBias

    if CORRECTED:
        controlDataFullPath = os.path.join(inactDataDir, controlFileName)
        controlData = np.load(controlDataFullPath)

        controlPVlaserBias = controlData['PVlaserBias']
        controlPVcontrolBias = controlData['PVcontrolBias']
        controlSOMlaserBias = controlData['SOMlaserBias']
        controlSOMcontrolBias = controlData['SOMcontrolBias']

        controlPVchange = controlPVlaserBias - controlPVcontrolBias
        controlSOMchange = controlSOMlaserBias - controlSOMcontrolBias

        correctedPVchange = PVchange - controlPVchange
        correctedSOMchange = SOMchange - controlSOMchange

        changeBias = [correctedPVchange, correctedSOMchange]
        medianChangeBias = [np.median(correctedPVchange, axis=0), np.median(correctedSOMchange, axis=0)]

    else:
        changeBias = [PVchange, SOMchange]
        medianChangeBias = [np.median(PVchange, axis=0), np.median(SOMchange, axis=0)]

    axBar = plt.subplot(gs[2,2])

    cellTypeColours = [PVColour, SOMColour]
    panelLabel = 'I'
    width = 0.3
    barLoc = np.array([-0.18, 0.18])
    xLocs = np.arange(2)

    for indBand in range(len(possibleBands)):
        for indType in range(len(medianChangeBias)):
            jitter = 0.8*width*(np.random.random(len(changeBias[indType]))-0.5)
            plt.plot(np.tile(xLocs[indBand]+barLoc[indType], len(changeBias[indType]))+jitter, changeBias[indType][:,indBand],
                     'o', mec=cellTypeColours[indType], mfc='white')
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 2, xLocs[indBand] + barLoc[indType] + width / 2],
                     [medianChangeBias[indType][indBand], medianChangeBias[indType][indBand]],
                     color='k', linewidth=3, zorder=10)  # medians

            biasCI = bootstrap_median_CI(changeBias[indType][:, indBand])
            # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
            plt.plot([xLocs[indBand] + barLoc[indType], xLocs[indBand] + barLoc[indType]], biasCI,
                     color='k', linewidth=1.5)  # error bars
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [biasCI[0], biasCI[0]], color='k', linewidth=1.5)  # bottom caps
            plt.plot([xLocs[indBand] + barLoc[indType] - width / 8, xLocs[indBand] + barLoc[indType] + width / 8],
                     [biasCI[1], biasCI[1]], color='k', linewidth=1.5)  # top caps
    plt.plot([-10,10], [0,0], '--', color='0.5', zorder=0) # line at 0 indicating direction of change

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    xTickLabels = possibleBands.tolist()
    xTickLabels[-1] = 'WN'
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(xTickLabels)
    axBar.set_xlabel('Masker bandwidth (oct.)', fontsize=fontSizeLabels)

    yLims = (-0.2, 0.4)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in Bias Index', fontsize=fontSizeLabels)

    extraplots.boxoff(axBar)
    extraplots.set_ticks_fontsize(axBar, fontSizeTicks)

    axBar.annotate(panelLabel, xy=(labelPosX[2], labelPosY[2]), xycoords='figure fraction', fontsize=fontSizePanel,
                   fontweight='bold')

    # calculate those stats!
    for band in range(len(possibleBands)):
        pVal = stats.ranksums(PVchange[:,band], SOMchange[:,band])
        print(f'PV bias change vs SOM bias change for bw {possibleBands[band]} p val: {pVal}')

        if pVal[1] < 0.05:
            extraplots.significance_stars(barLoc + xLocs[band], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

if CORRECTED:
    plt.suptitle('LASER EFFECT CORRECTION')
else:
    plt.suptitle('NO CORRECTION')

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
