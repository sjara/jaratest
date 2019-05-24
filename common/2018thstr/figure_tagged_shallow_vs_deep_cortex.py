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

FIGNAME = 'figure_tagged_deep'
SAVE_FIGURE = 0
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_deep_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches


colorShallow = colorpalette.TangoPalette['ScarletRed2']
colorDeep = colorpalette.TangoPalette['Orange2']
colorFarDeep = colorpalette.TangoPalette['Butter3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

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

# deepUntaggedCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']>depthCutoff))]
# shallowUntaggedCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']<depthCutoff))]

depthCutoff = 1300

shallowCellsFreq = goodFitToUse[((goodFitToUse['autoTagged']==1) & (goodFitToUse['depth']<=depthCutoff))]
deepCellsFreq = goodFitToUse[((goodFitToUse['autoTagged']==1) & (goodFitToUse['depth']>=depthCutoff))]

shallowCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']<=depthCutoff))]
deepCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']>=depthCutoff))]

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axThresh = plt.subplot(gs[0, 7:14])
axLatency = plt.subplot(gs[0, 14:21])

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axShallowNSYNC = plt.subplot(gsNSYNC[0, 0])
axDeepNSYNC = plt.subplot(gsNSYNC[1, 0])

axHighestSync = plt.subplot(gs[1, 3:9])
axMIRate = plt.subplot(gs[1, 9:15])
axMIPhase = plt.subplot(gs[1, 15:21])

### Copied below from plots where we are looking tagged, , and far deep

feature="BW10"
dataShallow = shallowCellsFreq[feature][pd.notnull(shallowCellsFreq[feature])]
dataDeep = deepCellsFreq[feature][pd.notnull(deepCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posShallow = jitter(np.ones(len(dataShallow))*0, 0.20)
posDeep = jitter(np.ones(len(dataDeep))*1, 0.20)
# posFarDeep = jitter(np.ones(len(dataFarDeep))*2, 0.20)

## Old method to jitter data points
# ax.plot(posShallow, dataShallow, 'o', mec = colorShallow, mfc = 'None')
# medline(axBW10, np.median(dataShallow), 0, 0.5)
# ax.plot(posDeep, dataDeep, 'o', mec = colorDeep, mfc = 'None')
# medline(axBW10, np.median(dataDeep), 1, 0.5)
# ax.plot(posFarDeep, dataFarDeep, 'o', mec = colorFarDeep, mfc = 'None')
# medline(axBW10, np.median(dataFarDeep), 2, 0.5)

boxData = [dataShallow, dataDeep]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorShallow, colorDeep]
whiskerColors = [colorShallow, colorShallow,
                 colorDeep, colorDeep]
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
ax.set_xticklabels(['Shallow\nN={}'.format(len(dataShallow)),
                    'Deep\nN={}'.format(len(dataDeep))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataShallow, dataDeep)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

# #1-2
# zVal, pVal = stats.mannwhitneyu(dataDeep, dataFarDeep)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataShallow, dataFarDeep)
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
dataShallow = shallowCellsFreq[feature][pd.notnull(shallowCellsFreq[feature])]
dataDeep = deepCellsFreq[feature][pd.notnull(deepCellsFreq[feature])]
ax = axThresh

# posShallow = jitter(np.ones(len(dataShallow))*0, 0.20)
# posDeep = jitter(np.ones(len(dataDeep))*1, 0.20)
# posFarDeep = jitter(np.ones(len(dataFarDeep))*2, 0.20)
# ax.plot(posShallow, dataShallow, 'o', mec = colorShallow, mfc = 'None')
# medline(axThresh, np.median(dataShallow), 0, 0.5)
# ax.plot(posDeep, dataDeep, 'o', mec = colorDeep, mfc = 'None')
# medline(axThresh, np.median(dataDeep), 1, 0.5)
# ax.plot(posFarDeep, dataFarDeep, 'o', mec = colorFarDeep, mfc = 'None')
# medline(axThresh, np.median(dataFarDeep), 2, 0.5)

boxData = [dataShallow, dataDeep]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorShallow, colorDeep]
whiskerColors = [colorShallow, colorShallow, colorDeep, colorDeep]
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
ax.set_xticklabels(['Shallow\nN={}'.format(len(dataShallow)),
                    'Deep\nN={}'.format(len(dataDeep))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataShallow, dataDeep)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


# #1-2
# zVal, pVal = stats.mannwhitneyu(dataDeep, dataFarDeep)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataShallow, dataFarDeep)
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
shallowCellsLatency = shallowCellsFreq.query(latencyQuery)
deepCellsLatency = deepCellsFreq.query(latencyQuery)

feature="latency"
dataShallow = shallowCellsLatency[feature][pd.notnull(shallowCellsLatency[feature])]
dataDeep = deepCellsLatency[feature][pd.notnull(deepCellsLatency[feature])]
ax = axLatency

# posShallow = jitter(np.ones(len(dataShallow))*0, 0.20)
# posDeep = jitter(np.ones(len(dataDeep))*1, 0.20)
# posFarDeep = jitter(np.ones(len(dataFarDeep))*2, 0.20)
# ax.plot(posShallow, dataShallow, 'o', mec = colorShallow, mfc = 'None')
# medline(axLatency, np.median(dataShallow), 0, 0.5)
# ax.plot(posDeep, dataDeep, 'o', mec = colorDeep, mfc = 'None')
# medline(axLatency, np.median(dataDeep), 1, 0.5)
# ax.plot(posFarDeep, dataFarDeep, 'o', mec = colorFarDeep, mfc = 'None')
# medline(axLatency, np.median(dataFarDeep), 2, 0.5)

boxData = [dataShallow, dataDeep]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorShallow, colorDeep]
whiskerColors = [colorShallow, colorShallow, colorDeep,
                 colorDeep]
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
ax.set_xticklabels(['Shallow\nN={}'.format(len(dataShallow)),
                    'Deep\nN={}'.format(len(dataDeep))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataShallow, dataDeep)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


# #1-2
# zVal, pVal = stats.mannwhitneyu(dataDeep, dataFarDeep)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataShallow, dataFarDeep)
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
dataShallow = shallowCellsAM[feature][pd.notnull(shallowCellsAM[feature])]
dataDeep = deepCellsAM[feature][pd.notnull(deepCellsAM[feature])]
dataFarDeep = deepCellsAM[feature][pd.notnull(deepCellsAM[feature])]

taggedSyncN = len(dataShallow[dataShallow > 0])
taggedNonSyncN = len(dataShallow[dataShallow == 0])
taggedSyncFrac = taggedSyncN/float(taggedSyncN + taggedNonSyncN)
taggedNonSyncFrac = taggedNonSyncN/float(taggedSyncN + taggedNonSyncN)

deepSyncN = len(dataDeep[dataDeep > 0])
deepNonSyncN = len(dataDeep[dataDeep == 0])
deepSyncFrac = deepSyncN/float(deepSyncN + deepNonSyncN)
deepNonSyncFrac = deepNonSyncN/float(deepSyncN + deepNonSyncN)

deepSyncN = len(dataFarDeep[dataFarDeep > 0])
deepNonSyncN = len(dataFarDeep[dataFarDeep == 0])
deepSyncFrac = deepSyncN/float(deepSyncN + deepNonSyncN)
deepNonSyncFrac = deepNonSyncN/float(deepSyncN + deepNonSyncN)


pieWedges = axShallowNSYNC.pie([taggedNonSyncFrac, taggedSyncFrac], colors=[colorShallow, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorShallow)
axShallowNSYNC.set_aspect('equal')

pieWedges = axDeepNSYNC.pie([deepNonSyncFrac, deepSyncFrac], colors=[colorDeep, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorDeep)
axDeepNSYNC.set_aspect('equal')

# pieWedges = axFarDeepNSYNC.pie([deepNonSyncFrac, deepSyncFrac], colors=[colorFarDeep, 'w'], shadow=False, startangle=0)
# for wedge in pieWedges[0]:
#     wedge.set_edgecolor(colorFarDeep)
# axFarDeepNSYNC.set_aspect('equal')


xBars = [-2, -3]
#FarDeep, Deep, tagged
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


oddsratio, pValue = stats.fisher_exact([[taggedSyncN, deepSyncN],
                                        [taggedNonSyncN, deepNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axDeepNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[1]-0.1,
                    yGapWidth, xTickWidth, starMarker=starMarker)

# oddsratio, pValue = stats.fisher_exact([[deepSyncN, taggedSyncN],
#                                         [deepNonSyncN, taggedNonSyncN]])
# if pValue < 0.05:
#     starMarker = '*'
# else:
#     starMarker = 'n.s.'
# plot_y_lines_with_ticks(axFarDeepNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
#                         yGapWidth, xTickWidth, starMarker=starMarker)

# oddsratio, pValue = stats.fisher_exact([[deepSyncN, taggedSyncN],
#                                         [deepNonSyncN, taggedNonSyncN]])
# if pValue < 0.05:
#     starMarker = '*'
# else:
#     starMarker = 'n.s.'
# plot_y_lines_with_ticks(axFarDeepNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
#                         yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataShallow = dataShallow[dataShallow>0]
dataShallow = np.log(dataShallow)

dataDeep = dataDeep[dataDeep>0]
dataDeep = np.log(dataDeep)

dataFarDeep = dataFarDeep[dataFarDeep>0]
dataFarDeep = np.log(dataFarDeep)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posShallow = jitter(np.ones(len(dataShallow))*0, 0.20)
# posDeep = jitter(np.ones(len(dataDeep))*1, 0.20)
# posFarDeep = jitter(np.ones(len(dataFarDeep))*2, 0.20)
# ax.plot(posShallow, dataShallow, 'o', mec = colorShallow, mfc = 'None')
# medline(axHighestSync, np.median(dataShallow), 0, 0.5)
# ax.plot(posDeep, dataDeep, 'o', mec = colorDeep, mfc = 'None')
# medline(axHighestSync, np.median(dataDeep), 1, 0.5)
# ax.plot(posFarDeep, dataFarDeep, 'o', mec = colorFarDeep, mfc = 'None')
# medline(axHighestSync, np.median(dataFarDeep), 2, 0.5)

boxData = [dataShallow, dataDeep]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorShallow, colorDeep, colorFarDeep]
whiskerColors = [colorShallow, colorShallow, colorDeep,
                 colorDeep]
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
ax.set_xticklabels(['Shallow\nN={}'.format(len(dataShallow)),
                    'Deep\nN={}'.format(len(dataDeep))])
ax.set_yticks(yticks)
ax.set_yticklabels(ytickLabels)

#0-1
yMin = np.log(3)
yMax = np.log(128)
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataShallow, dataDeep)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
# #1-2
# zVal, pVal = stats.mannwhitneyu(dataDeep, dataFarDeep)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)
# #0-2
# zVal, pVal = stats.mannwhitneyu(dataShallow, dataFarDeep)
# print "Highest Sync Rate, Shallow/FarDeep zVal:{}, pVal:{}".format(zVal, pVal)
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
# feature = "mutualInfoPerSpikeBits"
feature = "mutualInfoBCBits"

dataShallow = shallowCellsAM[feature][pd.notnull(shallowCellsAM[feature])]
dataShallow[dataShallow<0]=0

dataDeep = deepCellsAM[feature][pd.notnull(deepCellsAM[feature])]
dataDeep[dataDeep<0]=0

dataFarDeep = deepCellsAM[feature][pd.notnull(deepCellsAM[feature])]
dataFarDeep[dataFarDeep<0]=0

# posShallow = jitter(np.ones(len(dataShallow))*0, 0.20)
# posDeep = jitter(np.ones(len(dataDeep))*1, 0.20)
# posFarDeep = jitter(np.ones(len(dataFarDeep))*2, 0.20)
# ax.plot(posShallow, dataShallow, 'o', mec = colorShallow, mfc = 'None')
# medline(axMIRate, np.median(dataShallow), 0, 0.5)
# ax.plot(posDeep, dataDeep, 'o', mec = colorDeep, mfc = 'None')
# medline(axMIRate, np.median(dataDeep), 1, 0.5)
# ax.plot(posFarDeep, dataFarDeep, 'o', mec = colorFarDeep, mfc = 'None')
# medline(axMIRate, np.median(dataFarDeep), 2, 0.5)

boxData = [dataShallow, dataDeep]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorShallow, colorDeep, colorFarDeep]
whiskerColors = [colorShallow, colorShallow, colorDeep,
                 colorDeep]
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
ax.set_xticklabels(['Shallow\nN={}'.format(len(dataShallow)),
                    'Deep\nN={}'.format(len(dataDeep))])

#0-1
yMin = 0
yMax = 0.3
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataShallow, dataDeep)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
# #1-2
# zVal, pVal = stats.mannwhitneyu(dataDeep, dataFarDeep)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[1],
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[1],
#                                       ax=ax)
# #0-2
# zVal, pVal = stats.mannwhitneyu(dataShallow, dataFarDeep)
# if pVal < 0.05:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[0],
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[0],
#                                       ax=ax)
ax.set_ylabel("MI Rate")
ax.set_ylim([yMin, yMax])
extraplots.boxoff(ax)

## -- MI (Phase) -- ##
ax = axMIPhase
possibleFreqKeys = [4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128]

# dataframe = dataframe.query("pulsePval<0.05 and trainRatio>0.8")
# ac = dataframe.groupby('brainArea').get_group('rightAC')
# thal = dataframe.groupby('brainArea').get_group('rightThal')

keys = ['mutualInfoPhase_{}Hz'.format(rate) for rate in possibleFreqKeys]

dataShallow = np.full((len(shallowCellsAM), len(possibleFreqKeys)), np.nan)
dataDeep = np.full((len(deepCellsAM), len(possibleFreqKeys)), np.nan)
dataFarDeep = np.full((len(deepCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(shallowCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataShallow[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(deepCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataDeep[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(deepCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFarDeep[externalInd, indKey] = row[key]

dataShallow[dataShallow<0]=0
dataDeep[dataDeep<0]=0
dataFarDeep[dataFarDeep<0]=0

allPval = []
for indCol, freqKey in enumerate(possibleFreqKeys):
    dataShallowThisFreq = dataShallow[:,indCol][np.logical_not(np.isnan(dataShallow[:,indCol]))]
    dataDeepThisFreq = dataDeep[:,indCol][np.logical_not(np.isnan(dataDeep[:,indCol]))]
    dataFarDeepThisFreq = dataFarDeep[:,indCol][np.logical_not(np.isnan(dataFarDeep[:,indCol]))]
    zStat, pVal = stats.ranksums(dataShallowThisFreq, dataDeepThisFreq)
    allPval.append(int(pVal<0.05))
    print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataShallow, axis=0)
# taggedMean = np.nanmedian(dataShallow, axis=0)
taggedStd = np.nanstd(dataShallow, axis=0)

deepMean = np.nanmean(dataDeep, axis=0)
deepStd = np.nanstd(dataDeep, axis = 0)

# deepMean = np.nanmean(dataFarDeep, axis=0)
# deepStd = np.nanstd(dataFarDeep, axis = 0)

numShallow = sum(np.logical_not(np.isnan(dataShallow[:,0])))
numDeep = sum(np.logical_not(np.isnan(dataDeep[:,0])))
numFarDeep = sum(np.logical_not(np.isnan(dataFarDeep[:,0])))

ax.plot(taggedMean, '-', color=colorShallow, label='Shallow, n={}'.format(numShallow))
plt.hold(1)
ax.plot(deepMean, '--', color=colorDeep, label=" Deep, n={}".format(numDeep))
# ax.plot(deepMean, '-.', color=colorFarDeep, label="Far Deep, n={}".format(numFarDeep))
ax.set_xticks(range(len(possibleFreqKeys))[::2])
ax.set_xticklabels(possibleFreqKeys[::2])
ax.set_xlabel('AM rate (Hz)')

for indRate, significant in enumerate(allPval):
    if significant:
        ax.plot(indRate, np.mean([deepMean[indRate],taggedMean[indRate]]), "k*")

ax.set_ylabel('MI, Spike rate vs. stimulus phase (bits)')
extraplots.boxoff(ax)
# ax.legend()

plt.show()
