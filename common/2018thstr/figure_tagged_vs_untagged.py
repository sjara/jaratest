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
outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
figFilename = 'plots_tagged_vs_untagged' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches


labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

thalColor = colorpalette.TangoPalette['SkyBlue2']
acColor = colorpalette.TangoPalette['ScarletRed2']

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

goodFit = dbase.query('rsquaredFit > 0.08')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

# dataframe = goodFitToUse.query("brainArea == 'rightThal'")

# for feature in features:
#     zval, pval = stats.ranksums(dataTagged, dataUntagged)
#     print "p-val for feature: {} is {}".format(feature, pval)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

def plot_hist(ax, dataArr, color, label):
    lowFreq = 4
    highFreq = 128
    nFreqs = 11
    freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqs)
    freqs = np.round(freqs, decimals=1)
    freqs = np.r_[0, freqs]
    freqLabels = ['{}'.format(freq) for freq in freqs[1:]]
    freqLabels = ['NS', ' '] + freqLabels

    roundData = np.round(dataArr[pd.notnull(dataArr)], decimals=1)
    counts = Counter(roundData)

    freqsToPlot = np.r_[0, 1, freqs[1:]]
    index = np.arange(len(freqsToPlot))

    heights = []
    for freq in freqsToPlot:
        try:
            heights.append(100*counts[freq]/np.double(len(roundData)))
        except KeyError:
            heights.append(0)

    barWidth = 0.8
    rects = plt.bar(index+0.5*barWidth,
                    heights,
                    barWidth,
                    label=label,
                    color=color)
    plt.xticks(index + barWidth, freqs)
    ax.set_xticklabels(freqLabels, rotation='vertical')
    plt.ylabel('% cells')
    # ax.set_xlim([1.5,index[-1]+2*barWidth-0.5])
    # plt.xlabel('Highest AM rate to which\ncell can synchronize (Hz)')
    extraplots.boxoff(ax)

    height = max(heights)*0.05
    extraplots.breakaxis(1.8, 0, 0.3, height, gap=0.4)
    ax.tick_params(axis='x', length=0)
    plt.ylim([0, max(heights)+1])
    labelText = '{}, N={}'.format(label, len(roundData))
    ax.annotate(labelText, xy=(0.1, 0.9), xycoords='axes fraction',
                fontsize=9, fontweight='bold')
    return rects

plt.clf()

gs = gridspec.GridSpec(4, 3)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=0.52, hspace=1)




#boxplot features
features = ['BW10', 'threshold']
yLabels = ['BW10', 'Threshold (dB SPL)', 'Response latency (s)']

## -- Thal cells -- ##
dataframe = goodFitToUse.query("brainArea == 'rightThal'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

rowX = 0
for indFeature, feature in enumerate(features):
    dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
    dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]
    ax = plt.subplot(gs[rowX:rowX+2, indFeature])

    posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
    posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)

    ax.plot(posTagged, dataTagged, 'o', mec = 'k', mfc = 'None')
    medline(np.median(dataTagged), 0, 0.5)
    ax.plot(posUntagged, dataUntagged, 'o', mec = 'k', mfc = 'None')
    medline(np.median(dataUntagged), 1, 0.5)
    ax.set_xticks([0,1])
    ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                        'Untagged\nN={}'.format(len(dataUntagged))])
    ax.set_ylabel(yLabels[indFeature])
    extraplots.boxoff(ax)
    if indFeature==1:
        ax.set_ylim([12, 62])
    elif indFeature==2:
        ax.set_ylim([0, 0.06])
    zVal, pVal = stats.ranksums(dataTagged, dataUntagged)
    plt.title('p={:.3f}'.format(pVal))

# -- Highest Sync plots -- #
hsFeature = 'highestSyncCorrected'

dataframe = dbase.query("brainArea == 'rightThal'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

histColor = '0.5'
axTaggedSync = plt.subplot(gs[rowX, 2])
dataTagged = taggedCells[hsFeature][pd.notnull(taggedCells[hsFeature])]
dataTaggedSync = dataTagged[dataTagged>0]
dataTaggedNonSync = dataTagged[dataTagged==0]
plot_hist(axTaggedSync, dataTagged, thalColor, 'Tagged')

axUntaggedSync = plt.subplot(gs[rowX+1, 2])
dataUntagged = untaggedCells[hsFeature][pd.notnull(untaggedCells[hsFeature])]
dataUntaggedSync = dataUntagged[dataUntagged>0]
dataUntaggedNonSync = dataUntagged[dataUntagged==0]
plot_hist(axUntaggedSync, dataUntagged, thalColor, 'Untagged')
# plt.xlabel('Highest AM rate to which\ncell can synchronize (Hz)')

zval, pval = stats.ranksums(dataTaggedSync, dataUntaggedSync)
print "Thalamus, tagged vs. untagged AM sync ranksums test pval: {}".format(pval)

## -- AC cells -- ##
dataframe = goodFitToUse.query("brainArea == 'rightAC'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

rowX = 2
for indFeature, feature in enumerate(features):
    dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]
    dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]
    ax = plt.subplot(gs[rowX:rowX+2, indFeature])

    posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
    posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)

    ax.plot(posTagged, dataTagged, 'o', mec = 'k', mfc = 'None')
    medline(np.median(dataTagged), 0, 0.5)
    ax.plot(posUntagged, dataUntagged, 'o', mec = 'k', mfc = 'None')
    medline(np.median(dataUntagged), 1, 0.5)
    ax.set_xticks([0,1])
    ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                        'Untagged\nN={}'.format(len(dataUntagged))])
    ax.set_ylabel(yLabels[indFeature])
    extraplots.boxoff(ax)
    if indFeature==1:
        ax.set_ylim([12, 62])
    elif indFeature==2:
        ax.set_ylim([0, 0.06])
    zVal, pVal = stats.ranksums(dataTagged, dataUntagged)
    plt.title('p={:.3f}'.format(pVal))

# -- Highest Sync plots -- #

dataframe = dbase.query("brainArea == 'rightAC'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

axTaggedSync = plt.subplot(gs[rowX, 2])
dataTagged = taggedCells[hsFeature][pd.notnull(taggedCells[hsFeature])]
plot_hist(axTaggedSync, dataTagged, acColor, 'Tagged')
dataTaggedSync = dataTagged[dataTagged>0]
dataTaggedNonSync = dataTagged[dataTagged==0]

axUntaggedSync = plt.subplot(gs[rowX+1, 2])
dataUntagged = untaggedCells[hsFeature][pd.notnull(untaggedCells[hsFeature])]
dataUntaggedSync = dataUntagged[dataUntagged>0]
dataUntaggedNonSync = dataUntagged[dataUntagged==0]
plot_hist(axUntaggedSync, dataUntagged, acColor, 'Untagged')
plt.xlabel('Highest AM rate to which\ncell can synchronize (Hz)')

zval, pval = stats.ranksums(dataTaggedSync, dataUntaggedSync)
print "AC, tagged vs. untagged AM sync ranksums test pval: {}".format(pval)

ax.annotate('ATh', xy=(0.04, 0.875), xycoords='figure fraction',
            fontsize=14, fontweight='bold', color=thalColor)

ax.annotate('AC', xy=(0.04, 0.45), xycoords='figure fraction',
            fontsize=14, fontweight='bold', color=acColor)

labelPosX = [0.04, 0.4, 0.7]   # Horiz position for panel labels
labelPosY = [0.25, 0.49, 0.70, 0.92]    # Vert position for panel labels
fontSizePanel = figparams.fontSizePanel

ax.annotate('A', xy=(labelPosX[0],labelPosY[3]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('B', xy=(labelPosX[1],labelPosY[3]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('C', xy=(labelPosX[2],labelPosY[3]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('D', xy=(labelPosX[2],labelPosY[2]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('E', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('F', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('G', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')
ax.annotate('H', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
            fontsize=fontSizePanel, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
