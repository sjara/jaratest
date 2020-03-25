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
figFilename = 'FigX_inhib_inactivation'  # Do not include extension
figFormat = 'pdf'  # 'pdf' or 'svg'
# figFormat = 'svg'
figSize = [9,9]  # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]  # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]  # Vert position for panel labels

PVInactExample = ''
SOMInactExample = ''
summaryFileName = 'all_behaviour_inhib_inactivation.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3, 3, width_ratios=[1.5, 1, 1])
gs.update(top=0.99, bottom=0.05, left=0.07, right=0.94, wspace=0.5, hspace=0.3)

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

# --- summary of change in accuracy during PV or SOM inactivation ---
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']

    PVdata = np.hstack((np.reshape(PVcontrolAccuracy, (len(PVcontrolAccuracy),1)), np.reshape(PVlaserAccuracy, (len(PVlaserAccuracy),1))))
    SOMdata = np.hstack((np.reshape(SOMcontrolAccuracy, (len(SOMcontrolAccuracy), 1)), np.reshape(SOMlaserAccuracy, (len(SOMlaserAccuracy), 1))))
    accuracyData = [PVdata, SOMdata]

    for ind, data in enumerate(accuracyData):
        axScatter = plt.subplot(gs[ind,1])

        xVals = range(2)
        for indSubj in range(data.shape[0]):
            plt.plot(xVals, data[indSubj,:], 'o-', color=ExcColour)

        axScatter.set_xlim(-0.3, 1.3)
        axScatter.set_xticks(xVals)
        axScatter.set_xticklabels(['control', 'laser'])

        axScatter.set_ylim(50, 80)
        axScatter.set_ylabel('Accuracy (%)')

        extraplots.boxoff(axScatter)

# --- comparison in change in accuracy with PV and SOM inactivation ---
if PANELS[2]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserAccuracy = summaryData['PVlaserAccuracy']
    PVcontrolAccuracy = summaryData['PVcontrolAccuracy']
    SOMlaserAccuracy = summaryData['SOMlaserAccuracy']
    SOMcontrolAccuracy = summaryData['SOMcontrolAccuracy']

    PVchange = PVlaserAccuracy - PVcontrolAccuracy
    SOMchange = SOMlaserAccuracy - SOMcontrolAccuracy

    axBar = plt.subplot(gs[2,1])

    cellTypeColours = [PVColour, SOMColour]

    width = 0.6
    loc = np.arange(1, 3)

    medianChangeAccuracy = [np.median(PVchange), np.median(SOMchange)]
    changeCIs = [bootstrap_median_CI(PVchange), bootstrap_median_CI(SOMchange)]

    for indType in range(len(medianChangeAccuracy)):
        plt.plot([loc[indType] - width / 2, loc[indType] + width / 2], [medianChangeAccuracy[indType], medianChangeAccuracy[indType]],
                 color=cellTypeColours[indType], linewidth=3)  # medians

        # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
        plt.plot([loc[indType], loc[indType]], changeCIs[indType], color=cellTypeColours[indType],
                 linewidth=1.5)  # error bars
        plt.plot([loc[indType] - width / 8, loc[indType] + width / 8], [changeCIs[indType][0], changeCIs[indType][0]],
                 color=cellTypeColours[indType], linewidth=1.5)  # bottom caps
        plt.plot([loc[indType] - width / 8, loc[indType] + width / 8], [changeCIs[indType][1], changeCIs[indType][1]],
                 color=cellTypeColours[indType], linewidth=1.5)  # top caps

    axBar.set_xlim(0.3, 2.7)
    axBar.set_xticks(loc)
    axBar.set_xticklabels(['no PV', 'no SOM'])

    yLims = (-12, 2)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in accuracy (%)')

    extraplots.boxoff(axBar)

    pVal = stats.ranksums(PVchange, SOMchange)[1]
    print('PV accuracy change vs SOM accuracy change p val: {}'.format(pVal))

# --- summary of change in bias towards one side during PV or SOM inactivation ---
if PANELS[3]:
    summaryDataFullPath = os.path.join(inactDataDir, summaryFileName)
    summaryData = np.load(summaryDataFullPath)

    PVlaserBias = summaryData['PVlaserBias']
    PVcontrolBias = summaryData['PVcontrolBias']
    SOMlaserBias = summaryData['SOMlaserBias']
    SOMcontrolBias = summaryData['SOMcontrolBias']

    PVdata = np.hstack((np.reshape(PVcontrolBias, (len(PVcontrolBias),1)), np.reshape(PVlaserBias, (len(PVlaserBias),1))))
    SOMdata = np.hstack((np.reshape(SOMcontrolBias, (len(SOMcontrolBias), 1)), np.reshape(SOMlaserBias, (len(SOMlaserBias), 1))))
    biasData = [PVdata, SOMdata]

    for ind, data in enumerate(biasData):
        axScatter = plt.subplot(gs[ind,2])

        xVals = range(2)
        for indSubj in range(data.shape[0]):
            plt.plot(xVals, data[indSubj,:], 'o-', color=ExcColour)

        axScatter.set_xlim(-0.3, 1.3)
        axScatter.set_xticks(xVals)
        axScatter.set_xticklabels(['control', 'laser'])

        axScatter.set_ylim(-0.7, 0.7)
        axScatter.set_ylabel('Bias')

        extraplots.boxoff(axScatter)

# --- comparison in change in accuracy with PV and SOM inactivation ---
if PANELS[2]:
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

    width = 0.6
    loc = np.arange(1, 3)

    medianChangeBias = [np.median(PVchange), np.median(SOMchange)]
    changeCIs = [bootstrap_median_CI(PVchange), bootstrap_median_CI(SOMchange)]

    for indType in range(len(medianChangeBias)):
        plt.plot([loc[indType] - width / 2, loc[indType] + width / 2], [medianChangeBias[indType], medianChangeBias[indType]],
                 color=cellTypeColours[indType], linewidth=3)  # medians

        # MAKING THE ERROR BARS MANUALLY BECAUSE plt.errorbars WAS TOO MUCH A PAIN IN THE ASS
        plt.plot([loc[indType], loc[indType]], changeCIs[indType], color=cellTypeColours[indType],
                 linewidth=1.5)  # error bars
        plt.plot([loc[indType] - width / 8, loc[indType] + width / 8], [changeCIs[indType][0], changeCIs[indType][0]],
                 color=cellTypeColours[indType], linewidth=1.5)  # bottom caps
        plt.plot([loc[indType] - width / 8, loc[indType] + width / 8], [changeCIs[indType][1], changeCIs[indType][1]],
                 color=cellTypeColours[indType], linewidth=1.5)  # top caps

    axBar.set_xlim(0.3, 2.7)
    axBar.set_xticks(loc)
    axBar.set_xticklabels(['no PV', 'no SOM'])

    yLims = (-0.3, 0.3)
    axBar.set_ylim(yLims)
    axBar.set_ylabel('Change in bias')

    extraplots.boxoff(axBar)
    extraplots.significance_stars([1, 2], yLims[1] * 1.03, yLims[1] * 0.02, gapFactor=0.25)

    pVal = stats.ranksums(PVchange, SOMchange)[1]
    print('PV bias change vs SOM bias change p val: {}'.format(pVal))

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)