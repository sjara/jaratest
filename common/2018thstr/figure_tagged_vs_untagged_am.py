import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import colorpalette
from scipy import stats
import pandas as pd
import figparams
reload(figparams)

np.random.seed(0)

FIGNAME = 'figure_tagged_untagged'
SAVE_FIGURE = 1
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_untagged_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches


labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

thalColor = figparams.colp['thalColor']
acColor = figparams.colp['acColor']

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

plt.clf()

gs = gridspec.GridSpec(2, 3)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=0.52, hspace=1)


#boxplot features
features = ['highestSyncCorrected', 'mutualInfoPerSpikeBits']
yLabels = ['Highest AM sync. rate (Hz)', 'MI (AM Rate, bits)', 'MI (AM Phase, bits)']

## -- Thal cells -- ##
dataframe = dbase.query("brainArea == 'rightThal'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

rowX = 0
for indFeature, feature in enumerate(features):
    ax = plt.subplot(gs[rowX, indFeature])

    if indFeature==0:
        dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
        dataTagged = dataTagged[dataTagged>0]
        dataTagged = np.log(dataTagged)
        dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]
        dataUntagged = dataUntagged[dataUntagged>0]
        dataUntagged = np.log(dataUntagged)

        # ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
        ytickLabels = [4, 8, 16, 32, 64, 128]
        yticks = np.log(ytickLabels)

    elif indFeature==1:
        dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
        dataTagged[dataTagged<0]=0
        dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]
        dataUntagged[dataUntagged<0]=0

    else:
        dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
        dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]

    posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
    posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)

    ax.plot(posTagged, dataTagged, 'o', mec = '0.5', mfc = 'None')
    medline(np.median(dataTagged), 0, 0.5)
    ax.plot(posUntagged, dataUntagged, 'o', mec = '0.5', mfc = 'None')
    medline(np.median(dataUntagged), 1, 0.5)
    ax.set_xticks([0,1])
    ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                        'Untagged\nN={}'.format(len(dataUntagged))])
    ax.set_ylabel(yLabels[indFeature])
    if indFeature==0:
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytickLabels)
    extraplots.boxoff(ax)
    # if indFeature==1:
    #     ax.set_ylim([12, 62])
    # elif indFeature==2:
    #     ax.set_ylim([0, 0.06])
    zVal, pVal = stats.ranksums(dataTagged, dataUntagged)
    plt.title('p={:.3f}'.format(pVal))

# -- Highest Sync plots -- #
# hsFeature = 'highestSyncCorrected'

# dataframe = dbase.query("brainArea == 'rightThal'")
# taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
# taggedCells = dataframe[taggedBool]
# untaggedCells = dataframe[~taggedBool]

# histColor = '0.5'
# axTaggedSync = plt.subplot(gs[rowX, 2])
# dataTagged = taggedCells[hsFeature][pd.notnull(taggedCells[hsFeature])]
# dataTaggedSync = dataTagged[dataTagged>0]
# dataTaggedNonSync = dataTagged[dataTagged==0]
# plot_hist(axTaggedSync, dataTagged, thalColor, 'Tagged')

# axUntaggedSync = plt.subplot(gs[rowX+1, 2])
# dataUntagged = untaggedCells[hsFeature][pd.notnull(untaggedCells[hsFeature])]
# dataUntaggedSync = dataUntagged[dataUntagged>0]
# dataUntaggedNonSync = dataUntagged[dataUntagged==0]
# plot_hist(axUntaggedSync, dataUntagged, thalColor, 'Untagged')
# plt.xlabel('Highest AM rate to which\ncell can synchronize (Hz)')

# zval, pval = stats.ranksums(dataTaggedSync, dataUntaggedSync)
# print "Thalamus, tagged vs. untagged AM sync ranksums test pval: {}".format(pval)

## -- AC cells -- ##
dataframe = dbase.query("brainArea == 'rightAC'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

rowX = 1
for indFeature, feature in enumerate(features):

    if indFeature==0: #Plot in log for highest AM rate
        dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
        dataTagged = dataTagged[dataTagged>0]
        dataTagged = np.log(dataTagged)
        dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]
        dataUntagged = dataUntagged[dataUntagged>0]
        dataUntagged = np.log(dataUntagged)

        # ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
        ytickLabels = [4, 8, 16, 32, 64, 128]
        yticks = np.log(ytickLabels)

    elif indFeature==1: #Lower limit at 0
        dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
        dataTagged[dataTagged<0]=0
        dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]
        dataUntagged[dataUntagged<0]=0

    else:
        dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
        dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]

    ax = plt.subplot(gs[rowX, indFeature])

    posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
    posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)

    ax.plot(posTagged, dataTagged, 'o', mec = '0.5', mfc = 'None')
    plt.hold(1)
    medline(np.median(dataTagged), 0, 0.5)
    ax.plot(posUntagged, dataUntagged, 'o', mec = '0.5', mfc = 'None')
    plt.hold(1)
    medline(np.median(dataUntagged), 1, 0.5)
    ax.set_xticks([0,1])
    ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                        'Untagged\nN={}'.format(len(dataUntagged))])
    ax.set_ylabel(yLabels[indFeature])
    if indFeature==0:
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytickLabels)
    extraplots.boxoff(ax)
    zVal, pVal = stats.ranksums(dataTagged, dataUntagged)
    plt.title('p={:.3f}'.format(pVal))

# -- Highest Sync plots -- #
################### Percent non-sync #####################
# axSummary = plt.subplot(gs[rowX, len(features)])

# feature = 'highestSyncCorrected'
# dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
# dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]

# taggedSyncN = len(dataTagged[dataTagged > 0])
# taggedNonSyncN = len(dataUntagged[dataUntagged == 0])
# acSyncPercent = acSyncN/float(acSyncN + acNonSyncN) * 100
# acNonSyncPercent = acNonSyncN/float(acSyncN + acNonSyncN) * 100

# thalSyncN = len(thalPopStat[thalPopStat > 0])
# thalNonSyncN = len(thalPopStat[thalPopStat == 0])
# thalSyncPercent = thalSyncN/float(thalSyncN + thalNonSyncN)*100
# thalNonSyncPercent = thalNonSyncN/float(thalSyncN + thalNonSyncN)*100

# width = 0.5
# plt.hold(1)
# loc = [1, 2]
# axSummary.bar(loc[0]-width/2, thalNonSyncPercent, width, color=colorATh)
# axSummary.bar(loc[0]-width/2, thalSyncPercent, width, bottom=thalNonSyncPercent, color=colorATh, alpha=0.5)
# axSummary.bar(loc[1]-width/2, acNonSyncPercent, width, color=colorAC)
# axSummary.bar(loc[1]-width/2, acSyncPercent, width, bottom=acNonSyncPercent, color=colorAC, alpha=0.5)
# extraplots.boxoff(axSummary)

# extraplots.new_significance_stars([1, 2], 105, 2.5, starMarker='*',
#                                     fontSize=fontSizeStars, gapFactor=starGapFactor)

# axSummary.text(2.65, 30, 'Non-Sync.', rotation=90, fontweight='bold')
# axSummary.text(2.65, 75, 'Sync.', rotation=90, fontweight='bold', color='0.5')

# axSummary.set_xlim([0.5, 2.6])
# # extraplots.boxoff(axSummary)
# axSummary.set_ylim([0, 100.5])
# axSummary.set_xticks([1, 2])
# tickLabels = ['ATh\nv\nStr', 'AC\nv\nAStr']
# axSummary.set_xticklabels(tickLabels)
# axSummary.set_ylabel('% neurons', labelpad=-5)


##########################################################

# dataframe = dbase.query("brainArea == 'rightAC'")
# taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
# taggedCells = dataframe[taggedBool]
# untaggedCells = dataframe[~taggedBool]

# axTaggedSync = plt.subplot(gs[rowX, 2])
# dataTagged = taggedCells[hsFeature][pd.notnull(taggedCells[hsFeature])]
# plot_hist(axTaggedSync, dataTagged, acColor, 'Tagged')
# dataTaggedSync = dataTagged[dataTagged>0]
# dataTaggedNonSync = dataTagged[dataTagged==0]

# axUntaggedSync = plt.subplot(gs[rowX+1, 2])
# dataUntagged = untaggedCells[hsFeature][pd.notnull(untaggedCells[hsFeature])]
# dataUntaggedSync = dataUntagged[dataUntagged>0]
# dataUntaggedNonSync = dataUntagged[dataUntagged==0]
# plot_hist(axUntaggedSync, dataUntagged, acColor, 'Untagged')
# plt.xlabel('Highest AM rate to which\ncell can synchronize (Hz)')

# zval, pval = stats.ranksums(dataTaggedSync, dataUntaggedSync)
# print "AC, tagged vs. untagged AM sync ranksums test pval: {}".format(pval)

ax.annotate('ATh', xy=(0.04, 0.875), xycoords='figure fraction',
            fontsize=14, fontweight='bold', color=thalColor)

ax.annotate('AC', xy=(0.04, 0.45), xycoords='figure fraction',
            fontsize=14, fontweight='bold', color=acColor)

labelPosX = [0.04, 0.4, 0.7]   # Horiz position for panel labels
labelPosY = [0.49, 0.92]    # Vert position for panel labels
fontSizePanel = figparams.fontSizePanel

ax.annotate('A', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('B', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('C', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('D', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('E', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('F', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
