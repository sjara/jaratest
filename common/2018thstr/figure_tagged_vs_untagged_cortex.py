import os
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)
from jaratoolbox import colorpalette
from jaratoolbox import celldatabase
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
# colorCloseUntagged = '0.33'
# colorFarUntagged = '0.66'

colorTagged = colorpalette.TangoPalette['ScarletRed2']
colorCloseUntagged = colorpalette.TangoPalette['Orange2']
colorFarUntagged = colorpalette.TangoPalette['Butter3']

labelPosX = [0.04, 0.48]   # Horiz position for panel labels
labelPosY = [0.48, 0.95]    # Vert position for panel labels

# exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuningexamples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_calculated_columns.h5')
dbase = celldatabase.load_hdf(dbPath)
# dbase = pd.read_hdf(dbPath, key='dataframe')

# #Copy over rate decoder columns
# dbRateDecoderPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_am', 'celldatabase_with_am_discrimination_accuracy.h5')
# dbaseRateDecoder = pd.read_hdf(dbRateDecoderPath, key='dataframe')
# dbase['accuracyRate'] = dbaseRateDecoder['accuracy']

# #Copy over phase decoder columns
# dbPhaseDecoderPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_am', 'celldatabase_with_phase_discrimination_accuracy.h5')
# dbasePhaseDecoder = pd.read_hdf(dbPhaseDecoderPath, key='dataframe')
# possibleRateKeys = np.array([4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128])
# for rate in possibleRateKeys:
#     key = 'phaseAccuracy_{}Hz'.format(rate)
#     dbase[key] = dbasePhaseDecoder[key]

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
# dataframe = dbase.query("brainArea == 'rightAC' and nSpikes>2000")
dataframe = dbase.query("brainArea == 'rightThal' and nSpikes>2000")

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
# closeUntaggedCellsFreq = goodFitToUse[goodFitToUse['closeUntagged']==1]
# farUntaggedCellsFreq = goodFitToUse[goodFitToUse['farUntagged']==1]

# taggedCellsAM = dataframe[dataframe['tagged']==1]
# closeUntaggedCellsAM = dataframe[dataframe['closeUntagged']==1]
# farUntaggedCellsAM = dataframe[dataframe['farUntagged']==1]
# farUntaggedCellsAM = farUntaggedCellsAM.query('noiseZscore>0')

taggedBool = ((goodFitToUse['taggedCond']==0) & (goodFitToUse['summaryPulseLatency']<0.01))

taggedCellsFreq = goodFitToUse[taggedBool]
closeUntaggedCellsFreq = goodFitToUse[goodFitToUse['taggedCond']==1]
farUntaggedCellsFreq = goodFitToUse[goodFitToUse['taggedCond']==2]

# farUntaggedCellsFreq = goodFitToUse[(goodFitToUse['taggedCond']==1) | (goodFitToUse['taggedCond']==2)]

# taggedCellsAM = dataframe[dataframe['taggedCond']==0]
# closeUntaggedCellsAM = dataframe[dataframe['taggedCond']==1]
# # farUntaggedCellsAM = dataframe[dataframe['taggedCond']==2]
# farUntaggedCellsAM = dataframe[(dataframe['taggedCond']==1) | (dataframe['taggedCond']==2)]

taggedBool = ((goodShape['taggedCond']==0) & (goodShape['summaryPulseLatency']<0.01))
taggedCellsAM = goodShape[taggedBool]
closeUntaggedCellsAM = goodShape[goodShape['taggedCond']==1]
farUntaggedCellsAM = goodShape[goodShape['taggedCond']==2]
# farUntaggedCellsAM = goodShape[(goodShape['taggedCond']==1) | (goodShape['taggedCond']==2)]

## Layout: Top: BW10, threshold, latency. Bottom: nsync percent, highestSync, MI rate, MI phase
## Layout needs to be 2, 12

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axBW10.hold(1)
axThresh = plt.subplot(gs[0, 7:14])
axThresh.hold(1)
axLatency = plt.subplot(gs[0, 14:21])
axLatency.hold(1)

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axTaggedNSYNC = plt.subplot(gsNSYNC[0, 0])
axTaggedNSYNC.hold(1)
axCloseUntaggedNSYNC = plt.subplot(gsNSYNC[1, 0])
axCloseUntaggedNSYNC.hold(1)
axFarUntaggedNSYNC = plt.subplot(gsNSYNC[2, 0])
axFarUntaggedNSYNC.hold(1)

axHighestSync = plt.subplot(gs[1, 3:9])
axHighestSync.hold(1)
axMIRate = plt.subplot(gs[1, 9:15])
axMIRate.hold(1)
axMIPhase = plt.subplot(gs[1, 15:21])
axMIPhase.hold(1)

## -- BW10 -- ##
feature="BW10"
dataTagged = taggedCellsFreq[feature][pd.notnull(taggedCellsFreq[feature])]
dataCloseUntagged = closeUntaggedCellsFreq[feature][pd.notnull(closeUntaggedCellsFreq[feature])]
dataFarUntagged = farUntaggedCellsFreq[feature][pd.notnull(farUntaggedCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
posCloseUntagged = jitter(np.ones(len(dataCloseUntagged))*1, 0.20)
posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)

## Old method to jitter data points
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axBW10, np.median(dataTagged), 0, 0.5)
# ax.plot(posCloseUntagged, dataCloseUntagged, 'o', mec = colorCloseUntagged, mfc = 'None')
# medline(axBW10, np.median(dataCloseUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axBW10, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataCloseUntagged, dataFarUntagged]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorCloseUntagged, colorFarUntagged]
whiskerColors = [colorTagged, colorTagged, colorCloseUntagged,
                 colorCloseUntagged, colorFarUntagged, colorFarUntagged]
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
                    'Close\nUntagged\nN={}'.format(len(dataCloseUntagged)),
                    'Far\nUntagged\nN={}'.format(len(dataFarUntagged))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataTagged, dataCloseUntagged)
print "{} Tagged vs. close untagged, p={}".format(feature, pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

#1-2
zVal, pVal = stats.mannwhitneyu(dataCloseUntagged, dataFarUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
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
dataCloseUntagged = closeUntaggedCellsFreq[feature][pd.notnull(closeUntaggedCellsFreq[feature])]
dataFarUntagged = farUntaggedCellsFreq[feature][pd.notnull(farUntaggedCellsFreq[feature])]
ax = axThresh

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posCloseUntagged = jitter(np.ones(len(dataCloseUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axThresh, np.median(dataTagged), 0, 0.5)
# ax.plot(posCloseUntagged, dataCloseUntagged, 'o', mec = colorCloseUntagged, mfc = 'None')
# medline(axThresh, np.median(dataCloseUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axThresh, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataCloseUntagged, dataFarUntagged]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorCloseUntagged, colorFarUntagged]
whiskerColors = [colorTagged, colorTagged, colorCloseUntagged,
                 colorCloseUntagged, colorFarUntagged, colorFarUntagged]
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
                    'Close\nUntagged\nN={}'.format(len(dataCloseUntagged)),
                    'Far\nUntagged\nN={}'.format(len(dataFarUntagged))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataCloseUntagged)
print "{} Tagged vs. close untagged, p={}".format(feature, pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataCloseUntagged, dataFarUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
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
closeUntaggedCellsLatency = closeUntaggedCellsFreq.query(latencyQuery)
farUntaggedCellsLatency = farUntaggedCellsFreq.query(latencyQuery)

feature="latency"
dataTagged = taggedCellsLatency[feature][pd.notnull(taggedCellsLatency[feature])]
dataCloseUntagged = closeUntaggedCellsLatency[feature][pd.notnull(closeUntaggedCellsLatency[feature])]
dataFarUntagged = farUntaggedCellsLatency[feature][pd.notnull(farUntaggedCellsLatency[feature])]
ax = axLatency

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posCloseUntagged = jitter(np.ones(len(dataCloseUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axLatency, np.median(dataTagged), 0, 0.5)
# ax.plot(posCloseUntagged, dataCloseUntagged, 'o', mec = colorCloseUntagged, mfc = 'None')
# medline(axLatency, np.median(dataCloseUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axLatency, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataCloseUntagged, dataFarUntagged]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorCloseUntagged, colorFarUntagged]
whiskerColors = [colorTagged, colorTagged, colorCloseUntagged,
                 colorCloseUntagged, colorFarUntagged, colorFarUntagged]
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
                    'Close\nUntagged\nN={}'.format(len(dataCloseUntagged)),
                    'Far\nUntagged\nN={}'.format(len(dataFarUntagged))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataCloseUntagged)
print "{} Tagged vs. close untagged, p={}".format(feature, pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataCloseUntagged, dataFarUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
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
dataCloseUntagged = closeUntaggedCellsAM[feature][pd.notnull(closeUntaggedCellsAM[feature])]
dataFarUntagged = farUntaggedCellsAM[feature][pd.notnull(farUntaggedCellsAM[feature])]

taggedSyncN = len(dataTagged[dataTagged > 0])
taggedNonSyncN = len(dataTagged[dataTagged == 0])
taggedSyncFrac = taggedSyncN/float(taggedSyncN + taggedNonSyncN)
taggedNonSyncFrac = taggedNonSyncN/float(taggedSyncN + taggedNonSyncN)

closeUntaggedSyncN = len(dataCloseUntagged[dataCloseUntagged > 0])
closeUntaggedNonSyncN = len(dataCloseUntagged[dataCloseUntagged == 0])
closeUntaggedSyncFrac = closeUntaggedSyncN/float(closeUntaggedSyncN + closeUntaggedNonSyncN)
closeUntaggedNonSyncFrac = closeUntaggedNonSyncN/float(closeUntaggedSyncN + closeUntaggedNonSyncN)

farUntaggedSyncN = len(dataFarUntagged[dataFarUntagged > 0])
farUntaggedNonSyncN = len(dataFarUntagged[dataFarUntagged == 0])
farUntaggedSyncFrac = farUntaggedSyncN/float(farUntaggedSyncN + farUntaggedNonSyncN)
farUntaggedNonSyncFrac = farUntaggedNonSyncN/float(farUntaggedSyncN + farUntaggedNonSyncN)


pieWedges = axTaggedNSYNC.pie([taggedNonSyncFrac, taggedSyncFrac], colors=[colorTagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorTagged)
axTaggedNSYNC.set_aspect('equal')

pieWedges = axCloseUntaggedNSYNC.pie([closeUntaggedNonSyncFrac, closeUntaggedSyncFrac], colors=[colorCloseUntagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorCloseUntagged)
axCloseUntaggedNSYNC.set_aspect('equal')

pieWedges = axFarUntaggedNSYNC.pie([farUntaggedNonSyncFrac, farUntaggedSyncFrac], colors=[colorFarUntagged, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorFarUntagged)
axFarUntaggedNSYNC.set_aspect('equal')


xBars = [-2, -3]
#FarUntagged, CloseUntagged, tagged
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


oddsratio, pValue = stats.fisher_exact([[farUntaggedSyncN, closeUntaggedSyncN],
                                        [farUntaggedNonSyncN, closeUntaggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axFarUntaggedNSYNC, xBars[0], yCircleCenters[0], yCircleCenters[1]-0.1,
                    yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[closeUntaggedSyncN, taggedSyncN],
                                        [closeUntaggedNonSyncN, taggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axFarUntaggedNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[farUntaggedSyncN, taggedSyncN],
                                        [farUntaggedNonSyncN, taggedNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axFarUntaggedNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataTagged = dataTagged[dataTagged>0]
dataTagged = np.log(dataTagged)

dataCloseUntagged = dataCloseUntagged[dataCloseUntagged>0]
dataCloseUntagged = np.log(dataCloseUntagged)

dataFarUntagged = dataFarUntagged[dataFarUntagged>0]
dataFarUntagged = np.log(dataFarUntagged)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posCloseUntagged = jitter(np.ones(len(dataCloseUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axHighestSync, np.median(dataTagged), 0, 0.5)
# ax.plot(posCloseUntagged, dataCloseUntagged, 'o', mec = colorCloseUntagged, mfc = 'None')
# medline(axHighestSync, np.median(dataCloseUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axHighestSync, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataCloseUntagged, dataFarUntagged]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorCloseUntagged, colorFarUntagged]
whiskerColors = [colorTagged, colorTagged, colorCloseUntagged,
                 colorCloseUntagged, colorFarUntagged, colorFarUntagged]
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
                    'Close\nUntagged\nN={}'.format(len(dataCloseUntagged)),
                    'Far\nUntagged\nN={}'.format(len(dataFarUntagged))])
ax.set_yticks(yticks)
ax.set_yticklabels(ytickLabels)

#0-1
yMin = np.log(3)
yMax = np.log(128)
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataCloseUntagged)
print "{} Tagged vs. close untagged, p={}".format(feature, pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataCloseUntagged, dataFarUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
print "Highest Sync Rate, Tagged/FarUntagged zVal:{}, pVal:{}".format(zVal, pVal)
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
# feature = "mutualInfoPerSpikeBits"
feature = 'rateDiscrimAccuracy'

dataTagged = taggedCellsAM[feature][pd.notnull(taggedCellsAM[feature])]
dataTagged[dataTagged<0]=0

dataCloseUntagged = closeUntaggedCellsAM[feature][pd.notnull(closeUntaggedCellsAM[feature])]
dataCloseUntagged[dataCloseUntagged<0]=0

dataFarUntagged = farUntaggedCellsAM[feature][pd.notnull(farUntaggedCellsAM[feature])]
dataFarUntagged[dataFarUntagged<0]=0

# posTagged = jitter(np.ones(len(dataTagged))*0, 0.20)
# posCloseUntagged = jitter(np.ones(len(dataCloseUntagged))*1, 0.20)
# posFarUntagged = jitter(np.ones(len(dataFarUntagged))*2, 0.20)
# ax.plot(posTagged, dataTagged, 'o', mec = colorTagged, mfc = 'None')
# medline(axMIRate, np.median(dataTagged), 0, 0.5)
# ax.plot(posCloseUntagged, dataCloseUntagged, 'o', mec = colorCloseUntagged, mfc = 'None')
# medline(axMIRate, np.median(dataCloseUntagged), 1, 0.5)
# ax.plot(posFarUntagged, dataFarUntagged, 'o', mec = colorFarUntagged, mfc = 'None')
# medline(axMIRate, np.median(dataFarUntagged), 2, 0.5)

boxData = [dataTagged, dataCloseUntagged, dataFarUntagged]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorTagged, colorCloseUntagged, colorFarUntagged]
whiskerColors = [colorTagged, colorTagged, colorCloseUntagged,
                 colorCloseUntagged, colorFarUntagged, colorFarUntagged]
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
                    'Close\nUntagged\nN={}'.format(len(dataCloseUntagged)),
                    'Far\nUntagged\nN={}'.format(len(dataFarUntagged))])

#0-1
yMin = 0.5
yMax = 1
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataTagged, dataCloseUntagged)
print "tagged vs. close untagged, {} p={}".format(feature, pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataCloseUntagged, dataFarUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataTagged, dataFarUntagged)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[0],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[0],
                                      ax=ax)
# ax.set_ylabel("MI Rate (bits/spike)")
ax.set_ylabel("Rate discrim accuracy")
ax.set_ylim([yMin, yMax])
extraplots.boxoff(ax)

## -- MI (Phase) -- ##
ax = axMIPhase
possibleFreqKeys = [4, 5, 8, 11, 16, 22, 32, 45, 64, 90, 128]
ratesToUse = possibleFreqKeys

# dataframe = dataframe.query("pulsePval<0.05 and trainRatio>0.8")
# ac = dataframe.groupby('brainArea').get_group('rightAC')
# thal = dataframe.groupby('brainArea').get_group('rightThal')

# keys = ['mutualInfoPhase_{}Hz'.format(rate) for rate in possibleFreqKeys]
keys = ['phaseDiscrimAccuracy_{}Hz'.format(rate) for rate in ratesToUse]

dataTagged = np.full((len(taggedCellsAM), len(possibleFreqKeys)), np.nan)
dataCloseUntagged = np.full((len(closeUntaggedCellsAM), len(possibleFreqKeys)), np.nan)
dataFarUntagged = np.full((len(farUntaggedCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(taggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataTagged[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(closeUntaggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataCloseUntagged[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(farUntaggedCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataFarUntagged[externalInd, indKey] = row[key]

# dataTagged[dataTagged<0]=0
# dataCloseUntagged[dataCloseUntagged<0]=0
# dataFarUntagged[dataFarUntagged<0]=0
# allPval = []


# for indCol, freqKey in enumerate(possibleFreqKeys):
#     dataTaggedThisFreq = dataTagged[:,indCol][np.logical_not(np.isnan(dataTagged[:,indCol]))]
#     dataCloseUntaggedThisFreq = dataCloseUntagged[:,indCol][np.logical_not(np.isnan(dataCloseUntagged[:,indCol]))]
#     dataFarUntaggedThisFreq = dataFarUntagged[:,indCol][np.logical_not(np.isnan(dataFarUntagged[:,indCol]))]
    # zStat, pVal = stats.ranksums(dataTaggedThisFreq, dataUntaggedThisFreq)
    # allPval.append(int(pVal<0.05))
    # print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataTagged, axis=1)
taggedMean = taggedMean[~np.isnan(taggedMean)]
# taggedMean = np.nanmedian(dataTagged, axis=0)
# taggedStd = np.nanstd(dataTagged, axis=0)

closeUntaggedMean = np.nanmean(dataCloseUntagged, axis=1)
closeUntaggedMean = closeUntaggedMean[~np.isnan(closeUntaggedMean)]
# closeUntaggedStd = np.nanstd(dataCloseUntagged, axis = 0)

farUntaggedMean = np.nanmean(dataFarUntagged, axis=1)
farUntaggedMean = farUntaggedMean[~np.isnan(farUntaggedMean)]

# farUntaggedStd = np.nanstd(dataFarUntagged, axis = 0)

numTagged = sum(np.logical_not(np.isnan(dataTagged[:,0])))
numCloseUntagged = sum(np.logical_not(np.isnan(dataCloseUntagged[:,0])))
numFarUntagged = sum(np.logical_not(np.isnan(dataFarUntagged[:,0])))

boxData = [taggedMean, closeUntaggedMean, farUntaggedMean]
bp = axMIPhase.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])
plt.hold(1)

colors = [colorTagged, colorCloseUntagged, colorFarUntagged]
whiskerColors = [colorTagged, colorTagged, colorCloseUntagged,
                 colorCloseUntagged, colorFarUntagged, colorFarUntagged]
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
ax.set_xticklabels(['Tagged\nN={}'.format(numTagged),
                    'Close\nUntagged\nN={}'.format(numCloseUntagged),
                    'Far\nUntagged\nN={}'.format(numFarUntagged)])

#0-1
yMin = 0.5
yMax = 1
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(taggedMean, closeUntaggedMean)
print "tagged vs. close untagged, accuracyPhase p={}".format(pVal)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(closeUntaggedMean, farUntaggedMean)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(taggedMean, farUntaggedMean)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[0],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 2], yStars[1], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[0],
                                      ax=ax)
# ax.set_ylabel("MI Rate (bits/spike)")
ax.set_ylabel("phase discrim accuracy")
ax.set_ylim([yMin, yMax])
extraplots.boxoff(ax)

# ax.plot(taggedMean, '-', color=colorTagged, label='Tagged, n={}'.format(numTagged))
# plt.hold(1)
# ax.plot(closeUntaggedMean, '--', color=colorCloseUntagged, label="Close Untagged, n={}".format(numCloseUntagged))
# ax.plot(farUntaggedMean, '-.', color=colorFarUntagged, label="Far Untagged, n={}".format(numFarUntagged))
# ax.set_xticks(range(len(possibleFreqKeys))[::2])
# ax.set_xticklabels(possibleFreqKeys[::2])
# ax.set_xlabel('AM rate (Hz)')

# for indRate, significant in enumerate(allPval):
#     if significant:
#         ax.plot(indRate, np.mean([untaggedMean[indRate],taggedMean[indRate]]), "k*")

# ax.set_ylabel('MI, Spike rate vs. stimulus phase (bits)')
extraplots.boxoff(ax)
# ax.legend()

plt.show()
