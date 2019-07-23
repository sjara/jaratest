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

FIGNAME = 'figure_tagged_six'
SAVE_FIGURE = 0
# outputDir = '/mnt/jarahubdata/reports/nick/20171218_all_2018thstr_figures'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_tagged_vs_six_am' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches



colorFive = colorpalette.TangoPalette['ScarletRed2']
colorSix = colorpalette.TangoPalette['Orange2']
colorFarSix = colorpalette.TangoPalette['Butter3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

fig = plt.gcf()
plt.clf()
fig.set_facecolor('w')

from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
mcc = MouseConnectivityCache(resolution=25)
rsp = mcc.get_reference_space()
rspAnnotationVolumeRotated = np.rot90(rsp.annotation, 1, axes=(2, 0))
#First have to get the brain area for each cell
for indRow, dbRow in dbase.iterrows():
    try:
        thisCoordID = rspAnnotationVolumeRotated[int(dbRow['cellX']), int(dbRow['cellY']), int(dbRow['cellZ'])]
    except ValueError:
        dbase.at[indRow, 'location'] = 'NaN'
    else:
        structDict = rsp.structure_tree.get_structures_by_id([thisCoordID])[0]
        dbase.at[indRow, 'location'] = structDict['name']


dataframe = dbase.query("brainArea == 'rightAC' and nSpikes>2000 and autoTagged==1")

### GET ONLY CELLS THAT COME FROM SITES WHERE AT LEAST ONE SOUND/LASER CELL WAS RECORDED
# dataframe = dataframe[~pd.isnull(dataframe['cellX'])]

goodISI = dataframe.query('isiViolations<0.02 or modifiedISI<0.02')
# goodISI = dataframe.query('isiViolations<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodFit = goodShape.query('rsquaredFit > 0.04')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

# sixUntaggedCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']>depthCutoff))]
# fiveUntaggedCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']<depthCutoff))]

fiveString = "Primary auditory area, layer 5"
sixString = "Primary auditory area, layer 6a"

fiveCellsFreq = goodFitToUse[goodFitToUse['location']==fiveString]
sixCellsFreq = goodFitToUse[goodFitToUse['location']==sixString]

fiveCellsAM = goodShape[goodShape['location']==fiveString]
sixCellsAM = goodShape[goodShape['location']==sixString]

# fiveCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']<=depthCutoff))]
# sixCellsAM = goodShape[((goodShape['autoTagged']==1) & (goodShape['depth']>=depthCutoff))]

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axThresh = plt.subplot(gs[0, 7:14])
axLatency = plt.subplot(gs[0, 14:21])

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axFiveNSYNC = plt.subplot(gsNSYNC[0, 0])
axSixNSYNC = plt.subplot(gsNSYNC[1, 0])

axHighestSync = plt.subplot(gs[1, 3:9])
axMIRate = plt.subplot(gs[1, 9:15])
axMIPhase = plt.subplot(gs[1, 15:21])

### Copied below from plots where we are looking tagged, , and far six

feature="BW10"
dataFive = fiveCellsFreq[feature][pd.notnull(fiveCellsFreq[feature])]
dataSix = sixCellsFreq[feature][pd.notnull(sixCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posFive = jitter(np.ones(len(dataFive))*0, 0.20)
posSix = jitter(np.ones(len(dataSix))*1, 0.20)
# posFarSix = jitter(np.ones(len(dataFarSix))*2, 0.20)

## Old method to jitter data points
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axBW10, np.median(dataFive), 0, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axBW10, np.median(dataSix), 1, 0.5)
# ax.plot(posFarSix, dataFarSix, 'o', mec = colorFarSix, mfc = 'None')
# medline(axBW10, np.median(dataFarSix), 2, 0.5)

boxData = [dataFive, dataSix]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorFive, colorSix]
whiskerColors = [colorFive, colorFive,
                 colorSix, colorSix]
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
ax.set_xticklabels(['Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

# #1-2
# zVal, pVal = stats.mannwhitneyu(dataSix, dataFarSix)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataFive, dataFarSix)
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
dataFive = fiveCellsFreq[feature][pd.notnull(fiveCellsFreq[feature])]
dataSix = sixCellsFreq[feature][pd.notnull(sixCellsFreq[feature])]
ax = axThresh

# posFive = jitter(np.ones(len(dataFive))*0, 0.20)
# posSix = jitter(np.ones(len(dataSix))*1, 0.20)
# posFarSix = jitter(np.ones(len(dataFarSix))*2, 0.20)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axThresh, np.median(dataFive), 0, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axThresh, np.median(dataSix), 1, 0.5)
# ax.plot(posFarSix, dataFarSix, 'o', mec = colorFarSix, mfc = 'None')
# medline(axThresh, np.median(dataFarSix), 2, 0.5)

boxData = [dataFive, dataSix]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorFive, colorSix]
whiskerColors = [colorFive, colorFive, colorSix, colorSix]
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
ax.set_xticklabels(['Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


# #1-2
# zVal, pVal = stats.mannwhitneyu(dataSix, dataFarSix)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataFive, dataFarSix)
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
fiveCellsLatency = fiveCellsFreq.query(latencyQuery)
sixCellsLatency = sixCellsFreq.query(latencyQuery)

feature="latency"
dataFive = fiveCellsLatency[feature][pd.notnull(fiveCellsLatency[feature])]
dataSix = sixCellsLatency[feature][pd.notnull(sixCellsLatency[feature])]
ax = axLatency

# posFive = jitter(np.ones(len(dataFive))*0, 0.20)
# posSix = jitter(np.ones(len(dataSix))*1, 0.20)
# posFarSix = jitter(np.ones(len(dataFarSix))*2, 0.20)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axLatency, np.median(dataFive), 0, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axLatency, np.median(dataSix), 1, 0.5)
# ax.plot(posFarSix, dataFarSix, 'o', mec = colorFarSix, mfc = 'None')
# medline(axLatency, np.median(dataFarSix), 2, 0.5)

boxData = [dataFive, dataSix]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorFive, colorSix]
whiskerColors = [colorFive, colorFive, colorSix,
                 colorSix]
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
ax.set_xticklabels(['Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


# #1-2
# zVal, pVal = stats.mannwhitneyu(dataSix, dataFarSix)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)

# #0-2
# zVal, pVal = stats.mannwhitneyu(dataFive, dataFarSix)
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
dataFive = fiveCellsAM[feature][pd.notnull(fiveCellsAM[feature])]
dataSix = sixCellsAM[feature][pd.notnull(sixCellsAM[feature])]
dataFarSix = sixCellsAM[feature][pd.notnull(sixCellsAM[feature])]

taggedSyncN = len(dataFive[dataFive > 0])
taggedNonSyncN = len(dataFive[dataFive == 0])
taggedSyncFrac = taggedSyncN/float(taggedSyncN + taggedNonSyncN)
taggedNonSyncFrac = taggedNonSyncN/float(taggedSyncN + taggedNonSyncN)

sixSyncN = len(dataSix[dataSix > 0])
sixNonSyncN = len(dataSix[dataSix == 0])
sixSyncFrac = sixSyncN/float(sixSyncN + sixNonSyncN)
sixNonSyncFrac = sixNonSyncN/float(sixSyncN + sixNonSyncN)

sixSyncN = len(dataFarSix[dataFarSix > 0])
sixNonSyncN = len(dataFarSix[dataFarSix == 0])
sixSyncFrac = sixSyncN/float(sixSyncN + sixNonSyncN)
sixNonSyncFrac = sixNonSyncN/float(sixSyncN + sixNonSyncN)


pieWedges = axFiveNSYNC.pie([taggedNonSyncFrac, taggedSyncFrac], colors=[colorFive, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorFive)
axFiveNSYNC.set_aspect('equal')

pieWedges = axSixNSYNC.pie([sixNonSyncFrac, sixSyncFrac], colors=[colorSix, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorSix)
axSixNSYNC.set_aspect('equal')

# pieWedges = axFarSixNSYNC.pie([sixNonSyncFrac, sixSyncFrac], colors=[colorFarSix, 'w'], shadow=False, startangle=0)
# for wedge in pieWedges[0]:
#     wedge.set_edgecolor(colorFarSix)
# axFarSixNSYNC.set_aspect('equal')


xBars = [-2, -3]
#FarSix, Six, tagged
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


oddsratio, pValue = stats.fisher_exact([[taggedSyncN, sixSyncN],
                                        [taggedNonSyncN, sixNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axSixNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[1]-0.1,
                    yGapWidth, xTickWidth, starMarker=starMarker)

# oddsratio, pValue = stats.fisher_exact([[sixSyncN, taggedSyncN],
#                                         [sixNonSyncN, taggedNonSyncN]])
# if pValue < 0.05:
#     starMarker = '*'
# else:
#     starMarker = 'n.s.'
# plot_y_lines_with_ticks(axFarSixNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
#                         yGapWidth, xTickWidth, starMarker=starMarker)

# oddsratio, pValue = stats.fisher_exact([[sixSyncN, taggedSyncN],
#                                         [sixNonSyncN, taggedNonSyncN]])
# if pValue < 0.05:
#     starMarker = '*'
# else:
#     starMarker = 'n.s.'
# plot_y_lines_with_ticks(axFarSixNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
#                         yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataFive = dataFive[dataFive>0]
dataFive = np.log(dataFive)

dataSix = dataSix[dataSix>0]
dataSix = np.log(dataSix)

dataFarSix = dataFarSix[dataFarSix>0]
dataFarSix = np.log(dataFarSix)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posFive = jitter(np.ones(len(dataFive))*0, 0.20)
# posSix = jitter(np.ones(len(dataSix))*1, 0.20)
# posFarSix = jitter(np.ones(len(dataFarSix))*2, 0.20)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axHighestSync, np.median(dataFive), 0, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axHighestSync, np.median(dataSix), 1, 0.5)
# ax.plot(posFarSix, dataFarSix, 'o', mec = colorFarSix, mfc = 'None')
# medline(axHighestSync, np.median(dataFarSix), 2, 0.5)

boxData = [dataFive, dataSix]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorFive, colorSix, colorFarSix]
whiskerColors = [colorFive, colorFive, colorSix,
                 colorSix]
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
ax.set_xticklabels(['Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])
ax.set_yticks(yticks)
ax.set_yticklabels(ytickLabels)

#0-1
yMin = np.log(3)
yMax = np.log(128)
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
# #1-2
# zVal, pVal = stats.mannwhitneyu(dataSix, dataFarSix)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor,
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
#                                       ax=ax)
# #0-2
# zVal, pVal = stats.mannwhitneyu(dataFive, dataFarSix)
# print "Highest Sync Rate, Five/FarSix zVal:{}, pVal:{}".format(zVal, pVal)
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

dataFive = fiveCellsAM[feature][pd.notnull(fiveCellsAM[feature])]
dataFive[dataFive<0]=0

dataSix = sixCellsAM[feature][pd.notnull(sixCellsAM[feature])]
dataSix[dataSix<0]=0

dataFarSix = sixCellsAM[feature][pd.notnull(sixCellsAM[feature])]
dataFarSix[dataFarSix<0]=0

# posFive = jitter(np.ones(len(dataFive))*0, 0.20)
# posSix = jitter(np.ones(len(dataSix))*1, 0.20)
# posFarSix = jitter(np.ones(len(dataFarSix))*2, 0.20)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axMIRate, np.median(dataFive), 0, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axMIRate, np.median(dataSix), 1, 0.5)
# ax.plot(posFarSix, dataFarSix, 'o', mec = colorFarSix, mfc = 'None')
# medline(axMIRate, np.median(dataFarSix), 2, 0.5)

boxData = [dataFive, dataSix]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1])

colors = [colorFive, colorSix, colorFarSix]
whiskerColors = [colorFive, colorFive, colorSix,
                 colorSix]
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
ax.set_xticklabels(['Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])

#0-1
yMin = 0
yMax = 0.3
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
# #1-2
# zVal, pVal = stats.mannwhitneyu(dataSix, dataFarSix)
# if pVal < 0.05:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[1],
#                                       ax=ax)
# else:
#     extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
#                                       fontSize=fontSizeStars, gapFactor=starGapFactor[1],
#                                       ax=ax)
# #0-2
# zVal, pVal = stats.mannwhitneyu(dataFive, dataFarSix)
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

dataFive = np.full((len(fiveCellsAM), len(possibleFreqKeys)), np.nan)
dataSix = np.full((len(sixCellsAM), len(possibleFreqKeys)), np.nan)
dataFarSix = np.full((len(sixCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(fiveCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFive[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(sixCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataSix[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(sixCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFarSix[externalInd, indKey] = row[key]

dataFive[dataFive<0]=0
dataSix[dataSix<0]=0
dataFarSix[dataFarSix<0]=0

allPval = []
for indCol, freqKey in enumerate(possibleFreqKeys):
    dataFiveThisFreq = dataFive[:,indCol][np.logical_not(np.isnan(dataFive[:,indCol]))]
    dataSixThisFreq = dataSix[:,indCol][np.logical_not(np.isnan(dataSix[:,indCol]))]
    dataFarSixThisFreq = dataFarSix[:,indCol][np.logical_not(np.isnan(dataFarSix[:,indCol]))]
    zStat, pVal = stats.ranksums(dataFiveThisFreq, dataSixThisFreq)
    allPval.append(int(pVal<0.05))
    print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataFive, axis=0)
# taggedMean = np.nanmedian(dataFive, axis=0)
taggedStd = np.nanstd(dataFive, axis=0)

sixMean = np.nanmean(dataSix, axis=0)
sixStd = np.nanstd(dataSix, axis = 0)

# sixMean = np.nanmean(dataFarSix, axis=0)
# sixStd = np.nanstd(dataFarSix, axis = 0)

numFive = sum(np.logical_not(np.isnan(dataFive[:,0])))
numSix = sum(np.logical_not(np.isnan(dataSix[:,0])))
numFarSix = sum(np.logical_not(np.isnan(dataFarSix[:,0])))

ax.plot(taggedMean, '-', color=colorFive, label='Five, n={}'.format(numFive))
plt.hold(1)
ax.plot(sixMean, '--', color=colorSix, label=" Six, n={}".format(numSix))
# ax.plot(sixMean, '-.', color=colorFarSix, label="Far Six, n={}".format(numFarSix))
ax.set_xticks(range(len(possibleFreqKeys))[::2])
ax.set_xticklabels(possibleFreqKeys[::2])
ax.set_xlabel('AM rate (Hz)')

for indRate, significant in enumerate(allPval):
    if significant:
        ax.plot(indRate, np.mean([sixMean[indRate],taggedMean[indRate]]), "k*")

ax.set_ylabel('MI, Spike rate vs. stimulus phase (bits)')
extraplots.boxoff(ax)
# ax.legend()

plt.show()
