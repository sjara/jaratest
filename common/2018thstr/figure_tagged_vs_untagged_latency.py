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
figFilename = 'plots_tagged_vs_untagged_latency' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7, 5] # In inches

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

thalColor = colorpalette.TangoPalette['SkyBlue2']
acColor = colorpalette.TangoPalette['ScarletRed2']
linewidth = 2

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

goodFit = dbase.query('rsquaredFit > 0.08')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

plt.clf()

# gs = gridspec.GridSpec(4, 3)
# gs.update(left=0.12, right=0.98, top=0.88, bottom=0.10, wspace=0.52, hspace=0.5)

#boxplot features
features = ['latency']
yLabels = ['Response latency (ms)']

## -- Thal cells -- ##
dataframe = goodFitToUse.query("brainArea == 'rightThal'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

rowX = 0
for indFeature, feature in enumerate(features):
    dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]*1000
    dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]*1000
    # ax = plt.subplot(gs[rowX:rowX+2, indFeature])
    ax = plt.subplot(121)

    bp = ax.boxplot([dataTagged, dataUntagged], widths=0.5)

    plt.setp(bp['boxes'], color=thalColor, lw=linewidth)
    plt.setp(bp['whiskers'], color=thalColor, lw=linewidth)
    plt.setp(bp['fliers'], color=thalColor, marker='+')
    plt.setp(bp['medians'], color=thalColor, lw=linewidth)
    plt.setp(bp['caps'], color=thalColor)

    # ax.set_xticks([0,1])
    ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                        'Untagged\nN={}'.format(len(dataUntagged))])
    ax.set_ylabel(yLabels[indFeature])
    extraplots.boxoff(ax)
    # if indFeature==1:
    #     ax.set_ylim([12, 62])
    # elif indFeature==2:
    #     ax.set_ylim([0, 0.06])
    zVal, pVal = stats.ranksums(dataTagged, dataUntagged)
    plt.title('p={:.3f}'.format(pVal))
    ax.set_ylim([0, 60])

# -- AC cells --

dataframe = goodFitToUse.query("brainArea == 'rightAC'")
taggedBool = (dataframe['pulsePval']<0.05) & (dataframe['trainRatio']>0.8)
taggedCells = dataframe[taggedBool]
untaggedCells = dataframe[~taggedBool]

rowX = 2
for indFeature, feature in enumerate(features):
    dataTagged = taggedCells[feature][pd.notnull(taggedCells[feature])]*1000
    dataUntagged = untaggedCells[feature][pd.notnull(untaggedCells[feature])]*1000
    # ax = plt.subplot(gs[rowX:rowX+2, indFeature])
    ax = plt.subplot(122)

    posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
    posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)

    bp = ax.boxplot([dataTagged, dataUntagged], widths=0.5)

    plt.setp(bp['boxes'], color=acColor, lw=linewidth)
    plt.setp(bp['whiskers'], color=acColor, lw=linewidth)
    plt.setp(bp['fliers'], color=acColor, marker='+')
    plt.setp(bp['medians'], color=acColor, lw=linewidth)
    plt.setp(bp['caps'], color=acColor)
    # 1/0

    # ax.plot(posTagged, dataTagged, 'o', mec = 'k', mfc = 'None')
    # medline(np.median(dataTagged), 0, 0.5)
    # ax.plot(posUntagged, dataUntagged, 'o', mec = 'k', mfc = 'None')
    # medline(np.median(dataUntagged), 1, 0.5)

    # ax.set_xticks([0,1])
    ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                        'Untagged\nN={}'.format(len(dataUntagged))])
    ax.set_ylabel(yLabels[indFeature])
    extraplots.boxoff(ax)
    zVal, pVal = stats.ranksums(dataTagged, dataUntagged)
    plt.title('p={:.3f}'.format(pVal))
    ax.set_ylim([0, 60])

labelPosX = [0.03, 0.46]   # Horiz position for panel labels
labelPosY = [0.89, 0.94]    # Vert position for panel labels

ax.annotate('ATh', xy=(labelPosX[0], labelPosY[0]), xycoords='figure fraction',
            fontsize=14, fontweight='bold', color=thalColor)
ax.annotate('A', xy=(labelPosX[0], labelPosY[1]), xycoords='figure fraction',
            fontsize=14, fontweight='bold')

ax.annotate('AC', xy=(labelPosX[1], labelPosY[0]), xycoords='figure fraction',
            fontsize=14, fontweight='bold', color=acColor)
ax.annotate('B', xy=(labelPosX[1], labelPosY[1]), xycoords='figure fraction',
            fontsize=14, fontweight='bold')

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
