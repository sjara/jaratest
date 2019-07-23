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

# colorFour = 'k'
# colorFive = '0.33'
# colorSix = '0.66'

colorFour = colorpalette.TangoPalette['ScarletRed2']
colorFive = colorpalette.TangoPalette['Orange2']
colorSix = colorpalette.TangoPalette['Butter3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbase = pd.read_hdf(dbPath, key='dataframe')

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
dataframe = dbase.query("brainArea == 'rightAC' and autoTagged==1")

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
# fourCellsFreq = goodFitToUse[goodFitToUse['tagged']==1]
# fiveCellsFreq = goodFitToUse[goodFitToUse['five']==1]
# sixCellsFreq = goodFitToUse[goodFitToUse['six']==1]

# fourCellsAM = dataframe[dataframe['tagged']==1]
# fiveCellsAM = dataframe[dataframe['five']==1]
# sixCellsAM = dataframe[dataframe['six']==1]
# sixCellsAM = sixCellsAM.query('noiseZscore>0')

fourString = "Primary auditory area, layer 4"
fiveString = "Primary auditory area, layer 5"
sixStringA = "Primary auditory area, layer 6a"
sixStringB = "Primary auditory area, layer 6b"

fourCellsFreq = goodFitToUse[goodFitToUse['location']==fourString]
fiveCellsFreq = goodFitToUse[goodFitToUse['location']==fiveString]
sixCellsFreq = goodFitToUse[((goodFitToUse['location']==sixStringA)|(goodFitToUse['location']==sixStringB))]

# sixCellsFreq = goodFitToUse[(goodFitToUse['taggedCond']==1) | (goodFitToUse['taggedCond']==2)]

# fourCellsAM = dataframe[dataframe['taggedCond']==0]
# fiveCellsAM = dataframe[dataframe['taggedCond']==1]
# # sixCellsAM = dataframe[dataframe['taggedCond']==2]
# sixCellsAM = dataframe[(dataframe['taggedCond']==1) | (dataframe['taggedCond']==2)]
fourCellsAM = goodShape[goodShape['location']==fourString]
fiveCellsAM = goodShape[goodShape['location']==fiveString]
sixCellsAM = goodShape[((goodShape['location']==sixStringA)|(goodShape['location']==sixStringB))]

# sixCellsAM = goodShape[(goodShape['taggedCond']==1) | (goodShape['taggedCond']==2)]

## Layout: Top: BW10, threshold, latency. Bottom: nsync percent, highestSync, MI rate, MI phase
## Layout needs to be 2, 12

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axThresh = plt.subplot(gs[0, 7:14])
axLatency = plt.subplot(gs[0, 14:21])

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axFourNSYNC = plt.subplot(gsNSYNC[0, 0])
axFiveNSYNC = plt.subplot(gsNSYNC[1, 0])
axSixNSYNC = plt.subplot(gsNSYNC[2, 0])

axHighestSync = plt.subplot(gs[1, 3:9])
axMIRate = plt.subplot(gs[1, 9:15])
axMIPhase = plt.subplot(gs[1, 15:21])

## -- BW10 -- ##
feature="BW10"
dataFour = fourCellsFreq[feature][pd.notnull(fourCellsFreq[feature])]
dataFive = fiveCellsFreq[feature][pd.notnull(fiveCellsFreq[feature])]
dataSix = sixCellsFreq[feature][pd.notnull(sixCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posFour = jitter(np.ones(len(dataFour))*0, 0.20)
posFive = jitter(np.ones(len(dataFive))*1, 0.20)
posSix = jitter(np.ones(len(dataSix))*2, 0.20)

## Old method to jitter data points
# ax.plot(posFour, dataFour, 'o', mec = colorFour, mfc = 'None')
# medline(axBW10, np.median(dataFour), 0, 0.5)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axBW10, np.median(dataFive), 1, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axBW10, np.median(dataSix), 2, 0.5)

boxData = [dataFour, dataFive, dataSix]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorFour, colorFive, colorSix]
whiskerColors = [colorFour, colorFour, colorFive,
                 colorFive, colorSix, colorSix]
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
ax.set_xticklabels(['Four\nN={}'.format(len(dataFour)),
                    'Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataFour, dataFive)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

#1-2
zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataFour, dataSix)
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
dataFour = fourCellsFreq[feature][pd.notnull(fourCellsFreq[feature])]
dataFive = fiveCellsFreq[feature][pd.notnull(fiveCellsFreq[feature])]
dataSix = sixCellsFreq[feature][pd.notnull(sixCellsFreq[feature])]
ax = axThresh

# posFour = jitter(np.ones(len(dataFour))*0, 0.20)
# posFive = jitter(np.ones(len(dataFive))*1, 0.20)
# posSix = jitter(np.ones(len(dataSix))*2, 0.20)
# ax.plot(posFour, dataFour, 'o', mec = colorFour, mfc = 'None')
# medline(axThresh, np.median(dataFour), 0, 0.5)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axThresh, np.median(dataFive), 1, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axThresh, np.median(dataSix), 2, 0.5)

boxData = [dataFour, dataFive, dataSix]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorFour, colorFive, colorSix]
whiskerColors = [colorFour, colorFour, colorFive,
                 colorFive, colorSix, colorSix]
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
ax.set_xticklabels(['Four\nN={}'.format(len(dataFour)),
                    'Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFour, dataFive)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataFour, dataSix)
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
fourCellsLatency = fourCellsFreq.query(latencyQuery)
fiveCellsLatency = fiveCellsFreq.query(latencyQuery)
sixCellsLatency = sixCellsFreq.query(latencyQuery)

feature="latency"
dataFour = fourCellsLatency[feature][pd.notnull(fourCellsLatency[feature])]
dataFive = fiveCellsLatency[feature][pd.notnull(fiveCellsLatency[feature])]
dataSix = sixCellsLatency[feature][pd.notnull(sixCellsLatency[feature])]
ax = axLatency

# posFour = jitter(np.ones(len(dataFour))*0, 0.20)
# posFive = jitter(np.ones(len(dataFive))*1, 0.20)
# posSix = jitter(np.ones(len(dataSix))*2, 0.20)
# ax.plot(posFour, dataFour, 'o', mec = colorFour, mfc = 'None')
# medline(axLatency, np.median(dataFour), 0, 0.5)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axLatency, np.median(dataFive), 1, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axLatency, np.median(dataSix), 2, 0.5)

boxData = [dataFour, dataFive, dataSix]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorFour, colorFive, colorSix]
whiskerColors = [colorFour, colorFour, colorFive,
                 colorFive, colorSix, colorSix]
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
ax.set_xticklabels(['Four\nN={}'.format(len(dataFour)),
                    'Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFour, dataFive)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataFour, dataSix)
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
dataFour = fourCellsAM[feature][pd.notnull(fourCellsAM[feature])]
dataFive = fiveCellsAM[feature][pd.notnull(fiveCellsAM[feature])]
dataSix = sixCellsAM[feature][pd.notnull(sixCellsAM[feature])]

fourSyncN = len(dataFour[dataFour > 0])
fourNonSyncN = len(dataFour[dataFour == 0])
fourSyncFrac = fourSyncN/float(fourSyncN + fourNonSyncN)
fourNonSyncFrac = fourNonSyncN/float(fourSyncN + fourNonSyncN)

fiveSyncN = len(dataFive[dataFive > 0])
fiveNonSyncN = len(dataFive[dataFive == 0])
fiveSyncFrac = fiveSyncN/float(fiveSyncN + fiveNonSyncN)
fiveNonSyncFrac = fiveNonSyncN/float(fiveSyncN + fiveNonSyncN)

sixSyncN = len(dataSix[dataSix > 0])
sixNonSyncN = len(dataSix[dataSix == 0])
sixSyncFrac = sixSyncN/float(sixSyncN + sixNonSyncN)
sixNonSyncFrac = sixNonSyncN/float(sixSyncN + sixNonSyncN)


pieWedges = axFourNSYNC.pie([fourNonSyncFrac, fourSyncFrac], colors=[colorFour, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorFour)
axFourNSYNC.set_aspect('equal')

pieWedges = axFiveNSYNC.pie([fiveNonSyncFrac, fiveSyncFrac], colors=[colorFive, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorFive)
axFiveNSYNC.set_aspect('equal')

pieWedges = axSixNSYNC.pie([sixNonSyncFrac, sixSyncFrac], colors=[colorSix, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorSix)
axSixNSYNC.set_aspect('equal')


xBars = [-2, -3]
#Six, Five, tagged
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


oddsratio, pValue = stats.fisher_exact([[sixSyncN, fiveSyncN],
                                        [sixNonSyncN, fiveNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axSixNSYNC, xBars[0], yCircleCenters[0], yCircleCenters[1]-0.1,
                    yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[fiveSyncN, fourSyncN],
                                        [fiveNonSyncN, fourNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axSixNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[sixSyncN, fourSyncN],
                                        [sixNonSyncN, fourNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axSixNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataFour = dataFour[dataFour>0]
dataFour = np.log(dataFour)

dataFive = dataFive[dataFive>0]
dataFive = np.log(dataFive)

dataSix = dataSix[dataSix>0]
dataSix = np.log(dataSix)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posFour = jitter(np.ones(len(dataFour))*0, 0.20)
# posFive = jitter(np.ones(len(dataFive))*1, 0.20)
# posSix = jitter(np.ones(len(dataSix))*2, 0.20)
# ax.plot(posFour, dataFour, 'o', mec = colorFour, mfc = 'None')
# medline(axHighestSync, np.median(dataFour), 0, 0.5)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axHighestSync, np.median(dataFive), 1, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axHighestSync, np.median(dataSix), 2, 0.5)

boxData = [dataFour, dataFive, dataSix]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorFour, colorFive, colorSix]
whiskerColors = [colorFour, colorFour, colorFive,
                 colorFive, colorSix, colorSix]
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
ax.set_xticklabels(['Four\nN={}'.format(len(dataFour)),
                    'Five\nN={}'.format(len(dataFive)),
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

zVal, pVal = stats.mannwhitneyu(dataFour, dataFive)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataFour, dataSix)
print "Highest Sync Rate, Four/Six zVal:{}, pVal:{}".format(zVal, pVal)
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

dataFour = fourCellsAM[feature][pd.notnull(fourCellsAM[feature])]
dataFour[dataFour<0]=0

dataFive = fiveCellsAM[feature][pd.notnull(fiveCellsAM[feature])]
dataFive[dataFive<0]=0

dataSix = sixCellsAM[feature][pd.notnull(sixCellsAM[feature])]
dataSix[dataSix<0]=0

# posFour = jitter(np.ones(len(dataFour))*0, 0.20)
# posFive = jitter(np.ones(len(dataFive))*1, 0.20)
# posSix = jitter(np.ones(len(dataSix))*2, 0.20)
# ax.plot(posFour, dataFour, 'o', mec = colorFour, mfc = 'None')
# medline(axMIRate, np.median(dataFour), 0, 0.5)
# ax.plot(posFive, dataFive, 'o', mec = colorFive, mfc = 'None')
# medline(axMIRate, np.median(dataFive), 1, 0.5)
# ax.plot(posSix, dataSix, 'o', mec = colorSix, mfc = 'None')
# medline(axMIRate, np.median(dataSix), 2, 0.5)

boxData = [dataFour, dataFive, dataSix]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorFour, colorFive, colorSix]
whiskerColors = [colorFour, colorFour, colorFive,
                 colorFive, colorSix, colorSix]
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
ax.set_xticklabels(['Four\nN={}'.format(len(dataFour)),
                    'Five\nN={}'.format(len(dataFive)),
                    'Six\nN={}'.format(len(dataSix))])

#0-1
yMin = 0
yMax = 0.3
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataFour, dataFive)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataFive, dataSix)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataFour, dataSix)
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

dataFour = np.full((len(fourCellsAM), len(possibleFreqKeys)), np.nan)
dataFive = np.full((len(fiveCellsAM), len(possibleFreqKeys)), np.nan)
dataSix = np.full((len(sixCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(fourCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFour[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(fiveCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFive[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(sixCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataSix[externalInd, indKey] = row[key]

dataFour[dataFour<0]=0
dataFive[dataFive<0]=0
dataSix[dataSix<0]=0

allPval = []
for indCol, freqKey in enumerate(possibleFreqKeys):
    dataFourThisFreq = dataFour[:,indCol][np.logical_not(np.isnan(dataFour[:,indCol]))]
    dataFiveThisFreq = dataFive[:,indCol][np.logical_not(np.isnan(dataFive[:,indCol]))]
    dataSixThisFreq = dataSix[:,indCol][np.logical_not(np.isnan(dataSix[:,indCol]))]
    # zStat, pVal = stats.ranksums(dataFourThisFreq, dataUntaggedThisFreq)
    # allPval.append(int(pVal<0.05))
    # print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataFour, axis=0)
# taggedMean = np.nanmedian(dataFour, axis=0)
taggedStd = np.nanstd(dataFour, axis=0)

fiveMean = np.nanmean(dataFive, axis=0)
fiveStd = np.nanstd(dataFive, axis = 0)

sixMean = np.nanmean(dataSix, axis=0)
sixStd = np.nanstd(dataSix, axis = 0)

numFour = sum(np.logical_not(np.isnan(dataFour[:,0])))
numFive = sum(np.logical_not(np.isnan(dataFive[:,0])))
numSix = sum(np.logical_not(np.isnan(dataSix[:,0])))

ax.plot(taggedMean, '-', color=colorFour, label='Four, n={}'.format(numFour))
plt.hold(1)
ax.plot(fiveMean, '--', color=colorFive, label="Five, n={}".format(numFive))
ax.plot(sixMean, '-.', color=colorSix, label="Six, n={}".format(numSix))
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
