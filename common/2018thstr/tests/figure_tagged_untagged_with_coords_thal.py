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

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

FIGNAME = 'figure_tagged_untagged'
SAVE_FIGURE = 0
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_untagged_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches


colorTagged = colorpalette.TangoPalette['SkyBlue2']
colorUntagged = colorpalette.TangoPalette['Aluminium3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

dataframe = dbase.query("brainArea == 'rightThal' and nSpikes>2000")

### GET ONLY CELLS THAT COME FROM SITES WHERE AT LEAST ONE SOUND/LASER CELL WAS RECORDED
dataframe = dataframe[~pd.isnull(dataframe['cellX'])]

goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
# goodISI = dataframe.query('isiViolations<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodFit = goodShape.query('rsquaredFit > 0.04')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

taggedCellsFreq = goodFitToUse[goodFitToUse['autoTagged']==1]
untaggedCellsFreq = goodFitToUse[goodFitToUse['autoTagged']==0]

taggedCellsAM = goodShape[goodShape['autoTagged']==1]
untaggedCellsAM = goodShape[goodShape['autoTagged']==0]

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axThresh = plt.subplot(gs[0, 7:14])
axLatency = plt.subplot(gs[0, 14:21])

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axTaggedNSYNC = plt.subplot(gsNSYNC[0, 0])
axUntaggedNSYNC = plt.subplot(gsNSYNC[1, 0])

axHighestSync = plt.subplot(gs[1, 3:9])
axMIRate = plt.subplot(gs[1, 9:15])
axMIPhase = plt.subplot(gs[1, 15:21])

### Copied below from plots where we are looking tagged, , and far untagged

feature="BW10"
dataTagged = taggedCellsFreq[feature][pd.notnull(taggedCellsFreq[feature])]
dataUntagged = untaggedCellsFreq[feature][pd.notnull(untaggedCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)

## Old method to jitter data points
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axBW10, np.median(dataTagged), 0, 0.5)
# ax.plot(posUntagged, dataUntagged, 'o', mec = colorUntagged, mfc = 'None')
# medline(axBW10, np.median(dataUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axBW10, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataUntagged]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorTagged, colorUntagged]
whiskerColors = [colorTagged, colorTagged,
                 colorUntagged, colorUntagged]
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

ax.set_xticks([0,1])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Untagged\nN={}'.format(len(dataUntagged))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataTagged, dataUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

# #1-2
# zVal, pVal = stats.mannwhitneyu(dataUntagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)

ax.set_ylim([yMin, yMax])


#Threshold
feature="threshold"
dataTagged = taggedCellsFreq[feature][pd.notnull(taggedCellsFreq[feature])]
dataUntagged = untaggedCellsFreq[feature][pd.notnull(untaggedCellsFreq[feature])]
ax = axThresh

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axThresh, np.median(dataTagged), 0, 0.5)
# ax.plot(posUntagged, dataUntagged, 'o', mec = colorUntagged, mfc = 'None')
# medline(axThresh, np.median(dataUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axThresh, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataUntagged]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorTagged, colorUntagged]
whiskerColors = [colorTagged, colorTagged, colorUntagged, colorUntagged]
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

ax.set_xticks([0,1])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Untagged\nN={}'.format(len(dataUntagged))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


# #1-2
# zVal, pVal = stats.mannwhitneyu(dataUntagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)

ax.set_ylim([yMin, yMax])
ax.set_ylabel('Threshold (dB SPL)')

## -- Latency -- ##

### FIXME: Why is the latency sometimes <0
# latencyQuery = "noiseZscore>1 and latency>0"
latencyQuery = "latency>0"
taggedCellsLatency = taggedCellsFreq.query(latencyQuery)
untaggedCellsLatency = untaggedCellsFreq.query(latencyQuery)

feature="latency"
dataTagged = taggedCellsLatency[feature][pd.notnull(taggedCellsLatency[feature])]
dataUntagged = untaggedCellsLatency[feature][pd.notnull(untaggedCellsLatency[feature])]
ax = axLatency

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axLatency, np.median(dataTagged), 0, 0.5)
# ax.plot(posUntagged, dataUntagged, 'o', mec = colorUntagged, mfc = 'None')
# medline(axLatency, np.median(dataUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axLatency, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataUntagged]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorTagged, colorUntagged]
whiskerColors = [colorTagged, colorTagged, colorUntagged,
                 colorUntagged]
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

ax.set_xticks([0,1])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Untagged\nN={}'.format(len(dataUntagged))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


# #1-2
# zVal, pVal = stats.mannwhitneyu(dataUntagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)

ax.set_ylim([yMin, yMax])
ax.set_ylabel('Latency (s)')




## -- Pie charts -- ##
feature = "highestSyncCorrected"
dataTagged = taggedCellsAM[feature][pd.notnull(taggedCellsAM[feature])]
dataUntagged = untaggedCellsAM[feature][pd.notnull(untaggedCellsAM[feature])]
dataFarUntagged = untaggedCellsAM[feature][pd.notnull(untaggedCellsAM[feature])]

taggedSyncN = len(dataTagged[dataTagged > 0])
taggedNonSyncN = len(dataTagged[dataTagged == 0])
if taggedSyncN>0:
    taggedSyncFrac = taggedSyncN/float(taggedSyncN + taggedNonSyncN)
else:
    taggedSyncFrac = 0
if taggedNonSyncN>0:
    taggedNonSyncFrac = taggedNonSyncN/float(taggedSyncN + taggedNonSyncN)
else:
    taggedNonSyncFrac = 0

# untaggedSyncN = len(dataUntagged[dataUntagged > 0])
# untaggedNonSyncN = len(dataUntagged[dataUntagged == 0])
# untaggedSyncFrac = untaggedSyncN/float(untaggedSyncN + untaggedNonSyncN)
# untaggedNonSyncFrac = untaggedNonSyncN/float(untaggedSyncN + untaggedNonSyncN)

untaggedSyncN = len(dataFarUntagged[dataFarUntagged > 0])
untaggedNonSyncN = len(dataFarUntagged[dataFarUntagged == 0])

if untaggedSyncN>0:
    untaggedSyncFrac = untaggedSyncN/float(untaggedSyncN + untaggedNonSyncN)
else:
    untaggedSyncFrac = 0

if untaggedNonSyncN>0:
    untaggedNonSyncFrac = untaggedNonSyncN/float(untaggedSyncN + untaggedNonSyncN)
else:
    untaggedNonSyncFrac = 0



pieWedges = axTaggedNSYNC.pie([taggedNonSyncFrac, taggedSyncFrac], colors=[colorTagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorTagged)
axTaggedNSYNC.set_aspect('equal')

pieWedges = axUntaggedNSYNC.pie([untaggedNonSyncFrac, untaggedSyncFrac], colors=[colorUntagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorUntagged)
axUntaggedNSYNC.set_aspect('equal')

# pieWedges = axFarUntaggedNSYNC.pie([untaggedNonSyncFrac, untaggedSyncFrac], colors=[colorFarUntagged, 'w'], shadow=False, startangle=0)
# for wedge in pieWedges[0]:
#     wedge.set_edgecolor(colorFarUntagged)
# axFarUntaggedNSYNC.set_aspect('equal')


xBars = [-2, -3]
#FarUntagged, Untagged, tagged
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


oddsratio, pValue = stats.fisher_exact([[untaggedSyncN, untaggedSyncN],
                                        [untaggedNonSyncN, untaggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axUntaggedNSYNC, xBars[0], yCircleCenters[0], yCircleCenters[1],
                    yGapWidth, xTickWidth, starMarker=starMarker)

# oddsratio, pValue = stats.fisher_exact([[untaggedSyncN, taggedSyncN],
#                                         [untaggedNonSyncN, taggedNonSyncN]])
# if pValue < 0.05:
#     starMarker = '*'
# else:
#     starMarker = 'n.s.'
# plot_y_lines_with_ticks(axFarUntaggedNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
#                         yGapWidth, xTickWidth, starMarker=starMarker)

# oddsratio, pValue = stats.fisher_exact([[untaggedSyncN, taggedSyncN],
#                                         [untaggedNonSyncN, taggedNonSyncN]])
# if pValue < 0.05:
#     starMarker = '*'
# else:
#     starMarker = 'n.s.'
# plot_y_lines_with_ticks(axFarUntaggedNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
#                         yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataTagged = dataTagged[dataTagged>0]
dataTagged = np.log(dataTagged)

dataUntagged = dataUntagged[dataUntagged>0]
dataUntagged = np.log(dataUntagged)

dataFarUntagged = dataFarUntagged[dataFarUntagged>0]
dataFarUntagged = np.log(dataFarUntagged)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axHighestSync, np.median(dataTagged), 0, 0.5)
# ax.plot(posUntagged, dataUntagged, 'o', mec = colorUntagged, mfc = 'None')
# medline(axHighestSync, np.median(dataUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axHighestSync, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataUntagged]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorTagged, colorUntagged]
whiskerColors = [colorTagged, colorTagged, colorUntagged,
                 colorUntagged]
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

ax.set_xticks([0,1])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Untagged\nN={}'.format(len(dataUntagged))])
ax.set_yticks(yticks)
ax.set_yticklabels(ytickLabels)

#0-1
yMin = np.log(3)
yMax = np.log(128)
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
# #1-2
# zVal, pVal = stats.mannwhitneyu(dataUntagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)
# #0-2
# zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
# print "Highest Sync Rate, Tagged/FarUntagged zVal:{}, pVal:{}".format(zVal, pVal)
# if pVal < 0.05:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
ax.set_ylim([yMin, yMax])
ax.set_ylabel('Highest AM sync. rate')
extraplots.boxoff(ax)

## -- MI (rate) -- ##
ax = axMIRate
feature = "mutualInfoPerSpikeBits"

dataTagged = taggedCellsAM[feature][pd.notnull(taggedCellsAM[feature])]
dataTagged[dataTagged<0]=0

dataUntagged = untaggedCellsAM[feature][pd.notnull(untaggedCellsAM[feature])]
dataUntagged[dataUntagged<0]=0

dataFarUntagged = untaggedCellsAM[feature][pd.notnull(untaggedCellsAM[feature])]
dataFarUntagged[dataFarUntagged<0]=0

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posUntagged = jitter(np.ones(len(dataUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axMIRate, np.median(dataTagged), 0, 0.5)
# ax.plot(posUntagged, dataUntagged, 'o', mec = colorUntagged, mfc = 'None')
# medline(axMIRate, np.median(dataUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axMIRate, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataUntagged]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorTagged, colorUntagged]
whiskerColors = [colorTagged, colorTagged, colorUntagged,
                 colorUntagged]
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

ax.set_xticks([0,1])
ax.set_xticklabels(['Tagged\nN={}'.format(len(dataTagged)),
                    'Untagged\nN={}'.format(len(dataUntagged))])

#0-1
yMin = 0
yMax = 0.05
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
# #1-2
# zVal, pVal = stats.mannwhitneyu(dataUntagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[1],
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[1],
#                                       ax=ax)
# #0-2
# zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
# if pVal < 0.05:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[0],
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[0],
#                                       ax=ax)
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
dataUntagged = np.full((len(untaggedCellsAM), len(possibleFreqKeys)), np.nan)
dataFarUntagged = np.full((len(untaggedCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(taggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataTagged[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(untaggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataUntagged[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(untaggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFarUntagged[externalInd, indKey] = row[key]

dataTagged[dataTagged<0]=0
dataUntagged[dataUntagged<0]=0
dataFarUntagged[dataFarUntagged<0]=0

allPval = []
for indCol, freqKey in enumerate(possibleFreqKeys):
    dataTaggedThisFreq = dataTagged[:,indCol][np.logical_not(np.isnan(dataTagged[:,indCol]))]
    dataUntaggedThisFreq = dataUntagged[:,indCol][np.logical_not(np.isnan(dataUntagged[:,indCol]))]
    dataFarUntaggedThisFreq = dataFarUntagged[:,indCol][np.logical_not(np.isnan(dataFarUntagged[:,indCol]))]
    # zStat, pVal = stats.ranksums(dataTaggedThisFreq, dataUntaggedThisFreq)
    # allPval.append(int(pVal<0.05))
    # print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataTagged, axis=0)
# taggedMean = np.nanmedian(dataTagged, axis=0)
taggedStd = np.nanstd(dataTagged, axis=0)

untaggedMean = np.nanmean(dataUntagged, axis=0)
untaggedStd = np.nanstd(dataUntagged, axis = 0)

# untaggedMean = np.nanmean(dataFarUntagged, axis=0)
# untaggedStd = np.nanstd(dataFarUntagged, axis = 0)

numTagged = sum(np.logical_not(np.isnan(dataTagged[:,0])))
numUntagged = sum(np.logical_not(np.isnan(dataUntagged[:,0])))
numFarUntagged = sum(np.logical_not(np.isnan(dataFarUntagged[:,0])))

ax.plot(taggedMean, '-', color=colorTagged, label='Tagged, n={}'.format(numTagged))
plt.hold(1)
ax.plot(untaggedMean, '--', color=colorUntagged, label=" Untagged, n={}".format(numUntagged))
# ax.plot(untaggedMean, '-.', color=colorFarUntagged, label="Far Untagged, n={}".format(numFarUntagged))
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
