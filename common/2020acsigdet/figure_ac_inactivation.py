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

FIGNAME = 'figure_ac_inactivation'
# inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, FIGNAME)
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, FIGNAME)

PANELS = [1, 1, 0, 1, 0]  # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'FigX_ac_inactivation'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
# figFormat = 'svg'
figSize = [8,3]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]  # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]  # Vert position for panel labels

ACInactExample = ''
summaryFileName = 'all_behaviour_ac_inactivation.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1, 3, width_ratios=[1.5, 1, 1])
gs.update(top=0.97, bottom=0.16, left=0.07, right=0.94, wspace=0.5, hspace=0.3)

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
    pass

# --- summary of change in accuracy during AC inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserAccuracy = summaryData['laserAccuracy']
    controlAccuracy = summaryData['controlAccuracy']
    possibleBands = summaryData['possibleBands']

    axScatter = plt.subplot(gs[0,1])

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['control', 'PV activated']

    for indBand in range(len(possibleBands)):
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserAccuracy.shape[0]):
            plt.plot(thisxLocs, [controlAccuracy[indMouse, indBand], laserAccuracy[indMouse, indBand]], '-', color=ExcColour)

        l1, = plt.plot(np.tile(thisxLocs[1],laserAccuracy.shape[0]), laserAccuracy[:,indBand], 'o', color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0],controlAccuracy.shape[0]), controlAccuracy[:,indBand], 'o', color=ExcColour)

        #median = np.median(accuracyData, axis=0)
        #plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
    axScatter.set_xlabel('Masker bandwidth (oct)')

    axScatter.set_ylim(50, 95)
    axScatter.set_ylabel('Accuracy (%)')

    extraplots.boxoff(axScatter)

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserAccuracy[:,band], controlAccuracy[:,band])[1]
        print(f"Change in accuracy at {possibleBands[band]} oct pVal: {pVal}")

# --- comparison in change in accuracy with AC inactivation ---
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

    cellTypeColours = [PVColour, SOMColour]

    width = 0.45
    barLoc = np.array([-0.24, 0.24])
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

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(possibleBands)
    axBar.set_xlabel('Masker bandwidth (octaves)')

    yLims = (-12, 2)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in accuracy (%)')

    extraplots.boxoff(axBar)

    for band in range(len(possibleBands)):
        pVal = stats.ranksums(PVchange[:, band], SOMchange[:, band])
        print(f'PV accuracy change vs SOM accuracy change for bw {possibleBands[band]} p val: {pVal}')

    # extraplots.significance_stars(barLoc + xLocs[0], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)
    # extraplots.significance_stars(barLoc + xLocs[1], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

# --- comparison in change in bias with PV and SOM inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    laserBias = summaryData['laserBias']
    controlBias = summaryData['controlBias']
    possibleBands = summaryData['possibleBands']

    axScatter = plt.subplot(gs[0, 2])

    barLoc = np.array([-0.24, 0.24])
    xLocs = np.arange(len(possibleBands))
    xTickLabels = possibleBands
    legendLabels = ['control', 'PV activated']

    for indBand in range(len(possibleBands)):
        thisxLocs = barLoc + xLocs[indBand]

        for indMouse in range(laserBias.shape[0]):
            plt.plot(thisxLocs, [controlBias[indMouse, indBand], laserBias[indMouse, indBand]], '-',
                     color=ExcColour)

        l1, = plt.plot(np.tile(thisxLocs[1], laserBias.shape[0]), laserBias[:, indBand], 'o', color=PVColour)
        l2, = plt.plot(np.tile(thisxLocs[0], controlBias.shape[0]), controlBias[:, indBand], 'o', color=ExcColour)

        # median = np.median(accuracyData, axis=0)
        # plt.plot(thisxLocs, median[bandsToUse], 'o-', color='k')
    axScatter.legend([l2, l1], legendLabels, loc='best')

    axScatter.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[-1] + barLoc[1] + 0.3)
    axScatter.set_xticks(xLocs)
    axScatter.set_xticklabels(np.tile(xTickLabels, len(xLocs)))
    axScatter.set_xlabel('Masker bandwidth (oct)')

    axScatter.set_ylim(-0.75,0.4)
    axScatter.set_ylabel('Bias')

    extraplots.boxoff(axScatter)

    # -- stats!! --
    for band in range(len(possibleBands)):
        pVal = stats.wilcoxon(laserBias[:,band], controlBias[:,band])[1]
        print(f"Change in bias at {possibleBands[band]} oct pVal: {pVal}")

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

    axBar = plt.subplot(gs[2,2])

    cellTypeColours = [PVColour, SOMColour]

    width = 0.45
    barLoc = np.array([-0.24, 0.24])
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

    axBar.set_xlim(xLocs[0] + barLoc[0] - 0.3, xLocs[1] + barLoc[1] + 0.3)
    axBar.set_xticks(xLocs)
    axBar.set_xticklabels(possibleBands)
    axBar.set_xlabel('Masker bandwidth (oct)')

    yLims = (-0.5, 0.3)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in bias')

    extraplots.boxoff(axBar)

    # calculate those stats!
    for band in range(len(possibleBands)):
        pVal = stats.ranksums(PVchange[:,band], SOMchange[:,band])
        print(f'PV bias change vs SOM bias change for bw {possibleBands[band]} p val: {pVal}')

    extraplots.significance_stars(barLoc + xLocs[0], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)
    extraplots.significance_stars(barLoc + xLocs[1], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)

# plt.show()
