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

np.random.seed(0)

FIGNAME = 'figure_tagged_untagged'
SAVE_FIGURE = 0
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_untagged_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches

# colorTagged = 'k'
# colorDeepUntagged = '0.33'
# colorShallowUntagged = '0.66'

colorTagged = colorpalette.TangoPalette['ScarletRed2']
colorDeepUntagged = colorpalette.TangoPalette['Orange2']
colorShallowUntagged = colorpalette.TangoPalette['Butter3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

features = ['highestSyncCorrected', 'mutualInfoPerSpikeBits']
yLabels = ['Highest AM sync. rate (Hz)', 'MI (AM Rate, bits)', 'MI (AM Phase, bits)']

#Select only the cells from AC
dataframe = dbase.query("brainArea == 'rightAC' and nSpikes>2000")

### GET ONLY CELLS THAT COME FROM SITES WHERE AT LEAST ONE SOUND/LASER CELL WAS RECORDED
# dataframe = dataframe[~pd.isnull(dataframe['cellX'])]

goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
# goodISI = dataframe.query('isiViolations<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodFit = goodShape.query('rsquaredFit > 0.04')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

#Have to use diff sets of cells for freq and AM
# taggedCellsFreq = goodFitToUse[goodFitToUse['tagged']==1]
# deepUntaggedCellsFreq = goodFitToUse[goodFitToUse['deepUntagged']==1]
# shallowUntaggedCellsFreq = goodFitToUse[goodFitToUse['shallowUntagged']==1]

# taggedCellsAM = dataframe[dataframe['tagged']==1]
# deepUntaggedCellsAM = dataframe[dataframe['deepUntagged']==1]
# shallowUntaggedCellsAM = dataframe[dataframe['shallowUntagged']==1]
# shallowUntaggedCellsAM = shallowUntaggedCellsAM.query('noiseZscore>0')

depthCutoff = 1000

taggedCellsFreq = goodFitToUse[goodFitToUse['autoTagged']==1]
deepUntaggedCellsFreq = goodFitToUse[((goodFitToUse['autoTagged']==0) & (goodFitToUse['depth']>depthCutoff))]
shallowUntaggedCellsFreq = goodFitToUse[((goodFitToUse['autoTagged']==0) & (goodFitToUse['depth']<depthCutoff))]

# taggedCellsAM = dataframe[dataframe['taggedCond']==0]
# deepUntaggedCellsAM = dataframe[dataframe['taggedCond']==1]
# # shallowUntaggedCellsAM = dataframe[dataframe['taggedCond']==2]
# shallowUntaggedCellsAM = dataframe[(dataframe['taggedCond']==1) | (dataframe['taggedCond']==2)]
taggedCellsAM = goodShape[goodShape['autoTagged']==1]
deepUntaggedCellsAM = goodShape[((goodShape['autoTagged']==0) & (goodShape['depth']>depthCutoff))]
shallowUntaggedCellsAM = goodShape[((goodShape['autoTagged']==0) & (goodShape['depth']<depthCutoff))]

# shallowUntaggedCellsAM = goodShape[(goodShape['taggedCond']==1) | (goodShape['taggedCond']==2)]

## Layout: Top: BW10, threshold, latency. Bottom: nsync percent, highestSync, MI rate, MI phase
## Layout needs to be 2, 12

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axThresh = plt.subplot(gs[0, 7:14])
axLatency = plt.subplot(gs[0, 14:21])

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axTaggedNSYNC = plt.subplot(gsNSYNC[0, 0])
axDeepUntaggedNSYNC = plt.subplot(gsNSYNC[1, 0])
axShallowUntaggedNSYNC = plt.subplot(gsNSYNC[2, 0])

axHighestSync = plt.subplot(gs[1, 3:9])
axMIRate = plt.subplot(gs[1, 9:15])
axMIPhase = plt.subplot(gs[1, 15:21])

## -- BW10 -- ##
feature="BW10"
dataTagged = taggedCellsFreq[feature][pd.notnull(taggedCellsFreq[feature])]
dataDeepUntagged = deepUntaggedCellsFreq[feature][pd.notnull(deepUntaggedCellsFreq[feature])]
dataShallowUntagged = shallowUntaggedCellsFreq[feature][pd.notnull(shallowUntaggedCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
posDeepUntagged = jitter(np.ones(len(dataDeepUntagged))*1, 0.20)
posShallowUntagged = jitter(np.ones(len(dataShallowUntagged))*2, 0.20)

## Old method to jitter data points
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axBW10, np.median(dataTagged), 0, 0.5)
# ax.plot(posDeepUntagged, dataDeepUntagged, 'o', mec = colorDeepUntagged, mfc = 'None')
# medline(axBW10, np.median(dataDeepUntagged), 1, 0.5)
# ax.plot(posShallowUntagged, dataShallowUntagged, 'o', mec = colorShallowUntagged, mfc = 'None')
# medline(axBW10, np.median(dataShallowUntagged), 2, 0.5)

boxData = [dataTagged, dataDeepUntagged, dataShallowUntagged]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorDeepUntagged, colorShallowUntagged]
whiskerColors = [colorTagged, colorTagged, colorDeepUntagged,
                 colorDeepUntagged, colorShallowUntagged, colorShallowUntagged]
boxColor = 'k'
linewidth=2
for patch, color in zip(bp['boxes'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['whiskers'], whiskerColors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['medians'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
plt.setp(bp['caps'], visible=False)

ax.set_xticks([0,1,2])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Deep\nUntagged\nN={}'.format(len(dataDeepUntagged)),
                    'Shallow\nUntagged\nN={}'.format(len(dataShallowUntagged))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataTagged, dataDeepUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

#1-2
zVal, pVal = stats.mannwhitneyu(dataDeepUntagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

ax.set_ylim([yMin, yMax])


#Threshold
feature="threshold"
dataTagged = taggedCellsFreq[feature][pd.notnull(taggedCellsFreq[feature])]
dataDeepUntagged = deepUntaggedCellsFreq[feature][pd.notnull(deepUntaggedCellsFreq[feature])]
dataShallowUntagged = shallowUntaggedCellsFreq[feature][pd.notnull(shallowUntaggedCellsFreq[feature])]
ax = axThresh

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posDeepUntagged = jitter(np.ones(len(dataDeepUntagged))*1, 0.20)
# posShallowUntagged = jitter(np.ones(len(dataShallowUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axThresh, np.median(dataTagged), 0, 0.5)
# ax.plot(posDeepUntagged, dataDeepUntagged, 'o', mec = colorDeepUntagged, mfc = 'None')
# medline(axThresh, np.median(dataDeepUntagged), 1, 0.5)
# ax.plot(posShallowUntagged, dataShallowUntagged, 'o', mec = colorShallowUntagged, mfc = 'None')
# medline(axThresh, np.median(dataShallowUntagged), 2, 0.5)

boxData = [dataTagged, dataDeepUntagged, dataShallowUntagged]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorDeepUntagged, colorShallowUntagged]
whiskerColors = [colorTagged, colorTagged, colorDeepUntagged,
                 colorDeepUntagged, colorShallowUntagged, colorShallowUntagged]
linewidth=2
for patch, color in zip(bp['boxes'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['whiskers'], whiskerColors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['medians'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
plt.setp(bp['caps'], visible=False)

ax.set_xticks([0,1,2])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Deep\nUntagged\nN={}'.format(len(dataDeepUntagged)),
                    'Shallow\nUntagged\nN={}'.format(len(dataShallowUntagged))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataDeepUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataDeepUntagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

ax.set_ylim([yMin, yMax])
ax.set_ylabel('Threshold (dB SPL)')

## -- Latency -- ##

### FIXME: Why is the latency sometimes <0
# latencyQuery = "noiseZscore>1 and latency>0"
latencyQuery = "latency>0"
taggedCellsLatency = taggedCellsFreq.query(latencyQuery)
deepUntaggedCellsLatency = deepUntaggedCellsFreq.query(latencyQuery)
shallowUntaggedCellsLatency = shallowUntaggedCellsFreq.query(latencyQuery)

feature="latency"
dataTagged = taggedCellsLatency[feature][pd.notnull(taggedCellsLatency[feature])]
dataDeepUntagged = deepUntaggedCellsLatency[feature][pd.notnull(deepUntaggedCellsLatency[feature])]
dataShallowUntagged = shallowUntaggedCellsLatency[feature][pd.notnull(shallowUntaggedCellsLatency[feature])]
ax = axLatency

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posDeepUntagged = jitter(np.ones(len(dataDeepUntagged))*1, 0.20)
# posShallowUntagged = jitter(np.ones(len(dataShallowUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axLatency, np.median(dataTagged), 0, 0.5)
# ax.plot(posDeepUntagged, dataDeepUntagged, 'o', mec = colorDeepUntagged, mfc = 'None')
# medline(axLatency, np.median(dataDeepUntagged), 1, 0.5)
# ax.plot(posShallowUntagged, dataShallowUntagged, 'o', mec = colorShallowUntagged, mfc = 'None')
# medline(axLatency, np.median(dataShallowUntagged), 2, 0.5)

boxData = [dataTagged, dataDeepUntagged, dataShallowUntagged]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorDeepUntagged, colorShallowUntagged]
whiskerColors = [colorTagged, colorTagged, colorDeepUntagged,
                 colorDeepUntagged, colorShallowUntagged, colorShallowUntagged]
linewidth=2
for patch, color in zip(bp['boxes'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['whiskers'], whiskerColors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['medians'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
plt.setp(bp['caps'], visible=False)

ax.set_xticks([0,1,2])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Deep\nUntagged\nN={}'.format(len(dataDeepUntagged)),
                    'Shallow\nUntagged\nN={}'.format(len(dataShallowUntagged))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataDeepUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataDeepUntagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

ax.set_ylim([yMin, yMax])
ax.set_ylabel('Latency (s)')




## -- Pie charts -- ##
feature = "highestSyncCorrected"
dataTagged = taggedCellsAM[feature][pd.notnull(taggedCellsAM[feature])]
dataDeepUntagged = deepUntaggedCellsAM[feature][pd.notnull(deepUntaggedCellsAM[feature])]
dataShallowUntagged = shallowUntaggedCellsAM[feature][pd.notnull(shallowUntaggedCellsAM[feature])]

taggedSyncN = len(dataTagged[dataTagged > 0])
taggedNonSyncN = len(dataTagged[dataTagged == 0])
taggedSyncFrac = taggedSyncN/float(taggedSyncN + taggedNonSyncN)
taggedNonSyncFrac = taggedNonSyncN/float(taggedSyncN + taggedNonSyncN)

deepUntaggedSyncN = len(dataDeepUntagged[dataDeepUntagged > 0])
deepUntaggedNonSyncN = len(dataDeepUntagged[dataDeepUntagged == 0])
deepUntaggedSyncFrac = deepUntaggedSyncN/float(deepUntaggedSyncN + deepUntaggedNonSyncN)
deepUntaggedNonSyncFrac = deepUntaggedNonSyncN/float(deepUntaggedSyncN + deepUntaggedNonSyncN)

shallowUntaggedSyncN = len(dataShallowUntagged[dataShallowUntagged > 0])
shallowUntaggedNonSyncN = len(dataShallowUntagged[dataShallowUntagged == 0])
shallowUntaggedSyncFrac = shallowUntaggedSyncN/float(shallowUntaggedSyncN + shallowUntaggedNonSyncN)
shallowUntaggedNonSyncFrac = shallowUntaggedNonSyncN/float(shallowUntaggedSyncN + shallowUntaggedNonSyncN)


pieWedges = axTaggedNSYNC.pie([taggedNonSyncFrac, taggedSyncFrac], colors=[colorTagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorTagged)
axTaggedNSYNC.set_aspect('equal')

pieWedges = axDeepUntaggedNSYNC.pie([deepUntaggedNonSyncFrac, deepUntaggedSyncFrac], colors=[colorDeepUntagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorDeepUntagged)
axDeepUntaggedNSYNC.set_aspect('equal')

pieWedges = axShallowUntaggedNSYNC.pie([shallowUntaggedNonSyncFrac, shallowUntaggedSyncFrac], colors=[colorShallowUntagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorShallowUntagged)
axShallowUntaggedNSYNC.set_aspect('equal')


xBars = [-2, -3]
#ShallowUntagged, DeepUntagged, tagged
yCircleCenters = [0, 3, 6]
xTickWidth = 0.2
yGapWidth = 1.5

def plot_y_lines_with_ticks(ax, x, y1, y2, gapwidth, tickwidth, color='k', starMarker="*", fontSize=9):
    ax.plot([x, x], [y1, np.mean([y1, y2])-(gapwidth/2)], '-', clip_on=False, color=color)
    ax.hold(1)
    ax.plot([x, x], [np.mean([y1, y2])+(gapwidth/2), y2], '-', clip_on=False, color=color)
    ax.plot([x, x+xTickWidth], [y1, y1], '-', clip_on=False, color=color)
    ax.plot([x, x+xTickWidth], [y2, y2], '-', clip_on=False, color=color)

    ax.text(x, np.mean([y1, y2]), starMarker, fontsize=fontSize, va='center',
            ha='center', clip_on=False, rotation=90)


oddsratio, pValue = stats.fisher_exact([[shallowUntaggedSyncN, deepUntaggedSyncN],
                                        [shallowUntaggedNonSyncN, deepUntaggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axShallowUntaggedNSYNC, xBars[0], yCircleCenters[0], yCircleCenters[1]-0.1,
                    yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[deepUntaggedSyncN, taggedSyncN],
                                        [deepUntaggedNonSyncN, taggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axShallowUntaggedNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[shallowUntaggedSyncN, taggedSyncN],
                                        [shallowUntaggedNonSyncN, taggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axShallowUntaggedNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataTagged = dataTagged[dataTagged>0]
dataTagged = np.log(dataTagged)

dataDeepUntagged = dataDeepUntagged[dataDeepUntagged>0]
dataDeepUntagged = np.log(dataDeepUntagged)

dataShallowUntagged = dataShallowUntagged[dataShallowUntagged>0]
dataShallowUntagged = np.log(dataShallowUntagged)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posDeepUntagged = jitter(np.ones(len(dataDeepUntagged))*1, 0.20)
# posShallowUntagged = jitter(np.ones(len(dataShallowUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axHighestSync, np.median(dataTagged), 0, 0.5)
# ax.plot(posDeepUntagged, dataDeepUntagged, 'o', mec = colorDeepUntagged, mfc = 'None')
# medline(axHighestSync, np.median(dataDeepUntagged), 1, 0.5)
# ax.plot(posShallowUntagged, dataShallowUntagged, 'o', mec = colorShallowUntagged, mfc = 'None')
# medline(axHighestSync, np.median(dataShallowUntagged), 2, 0.5)

boxData = [dataTagged, dataDeepUntagged, dataShallowUntagged]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorDeepUntagged, colorShallowUntagged]
whiskerColors = [colorTagged, colorTagged, colorDeepUntagged,
                 colorDeepUntagged, colorShallowUntagged, colorShallowUntagged]
linewidth=2
for patch, color in zip(bp['boxes'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['whiskers'], whiskerColors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['medians'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
plt.setp(bp['caps'], visible=False)

ax.set_xticks([0,1,2])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Deep\nUntagged\nN={}'.format(len(dataDeepUntagged)),
                    'Shallow\nUntagged\nN={}'.format(len(dataShallowUntagged))])
ax.set_yticks(yticks)
ax.set_yticklabels(ytickLabels)

#0-1
yMin = np.log(3)
yMax = np.log(128)
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataDeepUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataDeepUntagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataShallowUntagged)
print "Highest Sync Rate, Tagged/ShallowUntagged zVal:{}, pVal:{}".format(zVal, pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
ax.set_ylim([yMin, yMax])
ax.set_ylabel('Highest AM sync. rate')
extraplots.boxoff(ax)

## -- MI (rate) -- ##
ax = axMIRate
feature = "mutualInfoPerSpikeBits"

dataTagged = taggedCellsAM[feature][pd.notnull(taggedCellsAM[feature])]
dataTagged[dataTagged<0]=0

dataDeepUntagged = deepUntaggedCellsAM[feature][pd.notnull(deepUntaggedCellsAM[feature])]
dataDeepUntagged[dataDeepUntagged<0]=0

dataShallowUntagged = shallowUntaggedCellsAM[feature][pd.notnull(shallowUntaggedCellsAM[feature])]
dataShallowUntagged[dataShallowUntagged<0]=0

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posDeepUntagged = jitter(np.ones(len(dataDeepUntagged))*1, 0.20)
# posShallowUntagged = jitter(np.ones(len(dataShallowUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axMIRate, np.median(dataTagged), 0, 0.5)
# ax.plot(posDeepUntagged, dataDeepUntagged, 'o', mec = colorDeepUntagged, mfc = 'None')
# medline(axMIRate, np.median(dataDeepUntagged), 1, 0.5)
# ax.plot(posShallowUntagged, dataShallowUntagged, 'o', mec = colorShallowUntagged, mfc = 'None')
# medline(axMIRate, np.median(dataShallowUntagged), 2, 0.5)

boxData = [dataTagged, dataDeepUntagged, dataShallowUntagged]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorDeepUntagged, colorShallowUntagged]
whiskerColors = [colorTagged, colorTagged, colorDeepUntagged,
                 colorDeepUntagged, colorShallowUntagged, colorShallowUntagged]
linewidth=2
for patch, color in zip(bp['boxes'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['whiskers'], whiskerColors):
    patch.set_color(color)
    patch.set_lw(linewidth)
for patch, color in zip(bp['medians'], colors):
    patch.set_color(color)
    patch.set_lw(linewidth)
plt.setp(bp['caps'], visible=False)

ax.set_xticks([0,1,2])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Deep\nUntagged\nN={}'.format(len(dataDeepUntagged)),
                    'Shallow\nUntagged\nN={}'.format(len(dataShallowUntagged))])

#0-1
yMin = 0
yMax = 0.3
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataDeepUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataDeepUntagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataShallowUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[0],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[0],
                                      ax=ax)
ax.set_ylabel("MI Rate (bits/spike)")
ax.set_ylim([yMin, yMax])
extraplots.boxoff(ax)

## -- MI (Phase) -- ##
ax = axMIPhase
possibleFreqKeys = [4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128]

# dataframe = dataframe.query("pulsePval<0.05 and trainRatio>0.8")
# ac = dataframe.groupby('brainArea').get_group('rightAC')
# thal = dataframe.groupby('brainArea').get_group('rightThal')

keys = ['mutualInfoPhase_{}Hz'.format(rate) for rate in possibleFreqKeys]

dataTagged = np.full((len(taggedCellsAM), len(possibleFreqKeys)), np.nan)
dataDeepUntagged = np.full((len(deepUntaggedCellsAM), len(possibleFreqKeys)), np.nan)
dataShallowUntagged = np.full((len(shallowUntaggedCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(taggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataTagged[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(deepUntaggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataDeepUntagged[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(shallowUntaggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataShallowUntagged[externalInd, indKey] = row[key]

dataTagged[dataTagged<0]=0
dataDeepUntagged[dataDeepUntagged<0]=0
dataShallowUntagged[dataShallowUntagged<0]=0

allPval = []
for indCol, freqKey in enumerate(possibleFreqKeys):
    dataTaggedThisFreq = dataTagged[:,indCol][np.logical_not(np.isnan(dataTagged[:,indCol]))]
    dataDeepUntaggedThisFreq = dataDeepUntagged[:,indCol][np.logical_not(np.isnan(dataDeepUntagged[:,indCol]))]
    dataShallowUntaggedThisFreq = dataShallowUntagged[:,indCol][np.logical_not(np.isnan(dataShallowUntagged[:,indCol]))]
    # zStat, pVal = stats.ranksums(dataTaggedThisFreq, dataUntaggedThisFreq)
    # allPval.append(int(pVal<0.05))
    # print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataTagged, axis=0)
# taggedMean = np.nanmedian(dataTagged, axis=0)
taggedStd = np.nanstd(dataTagged, axis=0)

deepUntaggedMean = np.nanmean(dataDeepUntagged, axis=0)
deepUntaggedStd = np.nanstd(dataDeepUntagged, axis = 0)

shallowUntaggedMean = np.nanmean(dataShallowUntagged, axis=0)
shallowUntaggedStd = np.nanstd(dataShallowUntagged, axis = 0)

numTagged = sum(np.logical_not(np.isnan(dataTagged[:,0])))
numDeepUntagged = sum(np.logical_not(np.isnan(dataDeepUntagged[:,0])))
numShallowUntagged = sum(np.logical_not(np.isnan(dataShallowUntagged[:,0])))

ax.plot(taggedMean, '-', color=colorTagged, label='Tagged, n={}'.format(numTagged))
plt.hold(1)
ax.plot(deepUntaggedMean, '--', color=colorDeepUntagged, label="Deep Untagged, n={}".format(numDeepUntagged))
ax.plot(shallowUntaggedMean, '-.', color=colorShallowUntagged, label="Shallow Untagged, n={}".format(numShallowUntagged))
ax.set_xticks(range(len(possibleFreqKeys))[::2])
ax.set_xticklabels(possibleFreqKeys[::2])
ax.set_xlabel('AM rate (Hz)')

# for indRate, significant in enumerate(allPval):
#     if significant:
#         ax.plot(indRate, np.mean([untaggedMean[indRate],taggedMean[indRate]]), "k*")

# ax.set_ylabel('MI, Spike rate vs. stimulus phase (bits)')
extraplots.boxoff(ax)
# ax.legend()

plt.show()
