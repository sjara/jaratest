import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
from jaratoolbox import colorpalette
from scipy import stats
import copy
import pandas as pd
import figparams
reload(figparams)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

np.random.seed(0)

FIGNAME = 'figure_tagged_untagged'
SAVE_FIGURE = 0
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_untagged_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches

colorThalTagged = colorpalette.TangoPalette['SkyBlue1']
colorThalUntagged = '0.5'
colorACTagged = colorpalette.TangoPalette['ScarletRed2']
colorACUntagged = colorpalette.TangoPalette['Butter3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

dataframe = pd.read_hdf(dbPath, key='dataframe')
goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodNSpikes = goodShape.query('nSpikes>2000')

dataframeToUse = goodNSpikes

taggedCells = dataframeToUse.query('autoTagged==1')
farUntaggedCells = dataframeToUse.query('newFarUntagged==1')

acTagged = taggedCells.groupby('brainArea').get_group('rightAC')
acUntagged = farUntaggedCells.groupby('brainArea').get_group('rightAC')
thalTagged = taggedCells.groupby('brainArea').get_group('rightThal')
thalUntagged = farUntaggedCells.groupby('brainArea').get_group('rightThal')


popStatCol = 'highestSyncCorrected'
acTaggedStat = acTagged[popStatCol][pd.notnull(acTagged[popStatCol])]
acUntaggedStat = acUntagged[popStatCol][pd.notnull(acUntagged[popStatCol])]

thalTaggedStat = thalTagged[popStatCol][pd.notnull(thalTagged[popStatCol])]
thalUntaggedStat = thalUntagged[popStatCol][pd.notnull(thalUntagged[popStatCol])]

acTaggedStat = acTaggedStat[acTaggedStat>0]
acUntaggedStat = acUntaggedStat[acUntaggedStat>0]
thalTaggedStat = thalTaggedStat[thalTaggedStat>0]
thalUntaggedStat = thalUntaggedStat[thalUntaggedStat>0]

ytickLabels = [4, 8, 16, 32, 64, 128]

#Log the values
acTaggedStat = np.log(acTaggedStat)
acUntaggedStat = np.log(acUntaggedStat)
thalTaggedStat = np.log(thalTaggedStat)
thalUntaggedStat = np.log(thalUntaggedStat)

## -- Thalamus plot -- ##

axThalamus = plt.subplot(1, 2, 1)

pos = jitter(np.ones(len(thalTaggedStat))*0, 0.20)
axThalamus.plot(pos, thalTaggedStat, 'o', mec = colorThalTagged, mfc = 'None', alpha=0.5)
# plt.hold(1)
medline(axThalamus, np.median(thalTaggedStat), 0, 0.5)
# plt.hold(1)

pos = jitter(np.ones(len(thalUntaggedStat))*1, 0.20)
axThalamus.plot(pos, thalUntaggedStat, 'o', mec = colorThalUntagged, mfc = 'None', alpha=0.5)
# plt.hold(1)
medline(axThalamus, np.median(thalUntaggedStat), 1, 0.5)
# plt.hold(1)

tickLabels = ['Tagged\nn={}'.format(len(thalTaggedStat)), 'Untagged\nn={}'.format(len(thalUntaggedStat))]
axThalamus.set_xticks(range(2))
axThalamus.set_xticklabels(tickLabels)
axThalamus.set_xlim([-0.5, 1.5])
extraplots.boxoff(axThalamus)
axThalamus.set_yticks(np.log(ytickLabels))
axThalamus.set_yticklabels(ytickLabels)

zStat, pVal = stats.mannwhitneyu(thalTaggedStat, thalUntaggedStat)
print("Thalamus tagged vs. far untagged p-val={}".format(pVal))

## -- Cortex plot -- ##

axCortex = plt.subplot(1, 2, 2)

pos = jitter(np.ones(len(acTaggedStat))*0, 0.20)
axCortex.plot(pos, acTaggedStat, 'o', mec = colorACTagged, mfc = 'None', alpha=0.5)
# plt.hold(1)
medline(axCortex, np.median(acTaggedStat), 0, 0.5)
# plt.hold(1)

pos = jitter(np.ones(len(acUntaggedStat))*1, 0.20)
axCortex.plot(pos, acUntaggedStat, 'o', mec = colorACUntagged, mfc = 'None', alpha=0.5)
# plt.hold(1)
medline(axCortex, np.median(acUntaggedStat), 1, 0.5)
# plt.hold(1)

tickLabels = ['Tagged\nn={}'.format(len(acTaggedStat)), 'Untagged\nn={}'.format(len(acUntaggedStat))]
axCortex.set_xticks(range(2))
axCortex.set_xticklabels(tickLabels)
axCortex.set_xlim([-0.5, 1.5])
extraplots.boxoff(axCortex)
axCortex.set_yticks(np.log(ytickLabels))
axCortex.set_yticklabels(ytickLabels)

zStat, pVal = stats.mannwhitneyu(acTaggedStat, acUntaggedStat)
print("Cortex tagged vs. far untagged p-val={}".format(pVal))

plt.show()
