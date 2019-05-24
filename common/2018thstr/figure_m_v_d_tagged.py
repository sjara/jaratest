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

# colorMedial = 'k'
# colorVentral = '0.33'
# colorDorsal = '0.66'

colorMedial = colorpalette.TangoPalette['SkyBlue3']
colorVentral = colorpalette.TangoPalette['SkyBlue1']
colorDorsal = colorpalette.TangoPalette['Aluminium3']

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
dataframe = dbase.query("brainArea == 'rightThal' and autoTagged==1")

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
# medialCellsFreq = goodFitToUse[goodFitToUse['tagged']==1]
# ventralCellsFreq = goodFitToUse[goodFitToUse['ventral']==1]
# dorsalCellsFreq = goodFitToUse[goodFitToUse['dorsal']==1]

# medialCellsAM = dataframe[dataframe['tagged']==1]
# ventralCellsAM = dataframe[dataframe['ventral']==1]
# dorsalCellsAM = dataframe[dataframe['dorsal']==1]
# dorsalCellsAM = dorsalCellsAM.query('noiseZscore>0')

medialString = "Medial geniculate complex, medial part"
ventralString = "Medial geniculate complex, ventral part"
# dorsalString = "Medial geniculate complex, dorsal part"
dorsalString = "Suprageniculate nucleus"

medialCellsFreq = goodFitToUse[goodFitToUse['location']==medialString]
ventralCellsFreq = goodFitToUse[goodFitToUse['location']==ventralString]
dorsalCellsFreq = goodFitToUse[goodFitToUse['location']==dorsalString]

# dorsalCellsFreq = goodFitToUse[(goodFitToUse['taggedCond']==1) | (goodFitToUse['taggedCond']==2)]

# medialCellsAM = dataframe[dataframe['taggedCond']==0]
# ventralCellsAM = dataframe[dataframe['taggedCond']==1]
# # dorsalCellsAM = dataframe[dataframe['taggedCond']==2]
# dorsalCellsAM = dataframe[(dataframe['taggedCond']==1) | (dataframe['taggedCond']==2)]
medialCellsAM = goodShape[goodShape['location']==medialString]
ventralCellsAM = goodShape[goodShape['location']==ventralString]
dorsalCellsAM = goodShape[goodShape['location']==dorsalString]

# dorsalCellsAM = goodShape[(goodShape['taggedCond']==1) | (goodShape['taggedCond']==2)]

## Layout: Top: BW10, threshold, latency. Bottom: nsync percent, highestSync, MI rate, MI phase
## Layout needs to be 2, 12

gs = gridspec.GridSpec(2, 21)
gs.update(left=0.12, right=0.98, top=0.88, bottom=0.15, wspace=40, hspace=0.7)

axBW10 = plt.subplot(gs[0, 0:7])
axThresh = plt.subplot(gs[0, 7:14])
axLatency = plt.subplot(gs[0, 14:21])

gsNSYNC = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs[1, 0:3])
axMedialNSYNC = plt.subplot(gsNSYNC[0, 0])
axVentralNSYNC = plt.subplot(gsNSYNC[1, 0])
axDorsalNSYNC = plt.subplot(gsNSYNC[2, 0])

axHighestSync = plt.subplot(gs[1, 3:9])
axMIRate = plt.subplot(gs[1, 9:15])
axMIPhase = plt.subplot(gs[1, 15:21])

## -- BW10 -- ##
feature="BW10"
dataMedial = medialCellsFreq[feature][pd.notnull(medialCellsFreq[feature])]
dataVentral = ventralCellsFreq[feature][pd.notnull(ventralCellsFreq[feature])]
dataDorsal = dorsalCellsFreq[feature][pd.notnull(dorsalCellsFreq[feature])]
ax = axBW10
ax.set_ylabel('BW10')

posMedial = jitter(np.ones(len(dataMedial))*0, 0.20)
posVentral = jitter(np.ones(len(dataVentral))*1, 0.20)
posDorsal = jitter(np.ones(len(dataDorsal))*2, 0.20)

## Old method to jitter data points
# ax.plot(posMedial, dataMedial, 'o', mec = colorMedial, mfc = 'None')
# medline(axBW10, np.median(dataMedial), 0, 0.5)
# ax.plot(posVentral, dataVentral, 'o', mec = colorVentral, mfc = 'None')
# medline(axBW10, np.median(dataVentral), 1, 0.5)
# ax.plot(posDorsal, dataDorsal, 'o', mec = colorDorsal, mfc = 'None')
# medline(axBW10, np.median(dataDorsal), 2, 0.5)

boxData = [dataMedial, dataVentral, dataDorsal]
bp = axBW10.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorMedial, colorVentral, colorDorsal]
whiskerColors = [colorMedial, colorMedial, colorVentral,
                 colorVentral, colorDorsal, colorDorsal]
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
ax.set_xticklabels(['Medial\nN={}'.format(len(dataMedial)),
                    'Ventral\nN={}'.format(len(dataVentral)),
                    'Dorsal\nN={}'.format(len(dataDorsal))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 2
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9
zVal, pVal = stats.mannwhitneyu(dataMedial, dataVentral)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)

#1-2
zVal, pVal = stats.mannwhitneyu(dataVentral, dataDorsal)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataMedial, dataDorsal)
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
dataMedial = medialCellsFreq[feature][pd.notnull(medialCellsFreq[feature])]
dataVentral = ventralCellsFreq[feature][pd.notnull(ventralCellsFreq[feature])]
dataDorsal = dorsalCellsFreq[feature][pd.notnull(dorsalCellsFreq[feature])]
ax = axThresh

# posMedial = jitter(np.ones(len(dataMedial))*0, 0.20)
# posVentral = jitter(np.ones(len(dataVentral))*1, 0.20)
# posDorsal = jitter(np.ones(len(dataDorsal))*2, 0.20)
# ax.plot(posMedial, dataMedial, 'o', mec = colorMedial, mfc = 'None')
# medline(axThresh, np.median(dataMedial), 0, 0.5)
# ax.plot(posVentral, dataVentral, 'o', mec = colorVentral, mfc = 'None')
# medline(axThresh, np.median(dataVentral), 1, 0.5)
# ax.plot(posDorsal, dataDorsal, 'o', mec = colorDorsal, mfc = 'None')
# medline(axThresh, np.median(dataDorsal), 2, 0.5)

boxData = [dataMedial, dataVentral, dataDorsal]
bp = axThresh.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorMedial, colorVentral, colorDorsal]
whiskerColors = [colorMedial, colorMedial, colorVentral,
                 colorVentral, colorDorsal, colorDorsal]
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
ax.set_xticklabels(['Medial\nN={}'.format(len(dataMedial)),
                    'Ventral\nN={}'.format(len(dataVentral)),
                    'Dorsal\nN={}'.format(len(dataDorsal))])

extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 65
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataMedial, dataVentral)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataVentral, dataDorsal)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataMedial, dataDorsal)
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
medialCellsLatency = medialCellsFreq.query(latencyQuery)
ventralCellsLatency = ventralCellsFreq.query(latencyQuery)
dorsalCellsLatency = dorsalCellsFreq.query(latencyQuery)

feature="latency"
dataMedial = medialCellsLatency[feature][pd.notnull(medialCellsLatency[feature])]
dataVentral = ventralCellsLatency[feature][pd.notnull(ventralCellsLatency[feature])]
dataDorsal = dorsalCellsLatency[feature][pd.notnull(dorsalCellsLatency[feature])]
ax = axLatency

# posMedial = jitter(np.ones(len(dataMedial))*0, 0.20)
# posVentral = jitter(np.ones(len(dataVentral))*1, 0.20)
# posDorsal = jitter(np.ones(len(dataDorsal))*2, 0.20)
# ax.plot(posMedial, dataMedial, 'o', mec = colorMedial, mfc = 'None')
# medline(axLatency, np.median(dataMedial), 0, 0.5)
# ax.plot(posVentral, dataVentral, 'o', mec = colorVentral, mfc = 'None')
# medline(axLatency, np.median(dataVentral), 1, 0.5)
# ax.plot(posDorsal, dataDorsal, 'o', mec = colorDorsal, mfc = 'None')
# medline(axLatency, np.median(dataDorsal), 2, 0.5)

boxData = [dataMedial, dataVentral, dataDorsal]
bp = axLatency.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorMedial, colorVentral, colorDorsal]
whiskerColors = [colorMedial, colorMedial, colorVentral,
                 colorVentral, colorDorsal, colorDorsal]
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
ax.set_xticklabels(['Medial\nN={}'.format(len(dataMedial)),
                    'Ventral\nN={}'.format(len(dataVentral)),
                    'Dorsal\nN={}'.format(len(dataDorsal))])
extraplots.boxoff(ax)

#0-1
yMin = 0
yMax = 0.04
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataMedial, dataVentral)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)


#1-2
zVal, pVal = stats.mannwhitneyu(dataVentral, dataDorsal)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)

#0-2
zVal, pVal = stats.mannwhitneyu(dataMedial, dataDorsal)
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
dataMedial = medialCellsAM[feature][pd.notnull(medialCellsAM[feature])]
dataVentral = ventralCellsAM[feature][pd.notnull(ventralCellsAM[feature])]
dataDorsal = dorsalCellsAM[feature][pd.notnull(dorsalCellsAM[feature])]

medialSyncN = len(dataMedial[dataMedial > 0])
medialNonSyncN = len(dataMedial[dataMedial == 0])
medialSyncFrac = medialSyncN/float(medialSyncN + medialNonSyncN)
medialNonSyncFrac = medialNonSyncN/float(medialSyncN + medialNonSyncN)

ventralSyncN = len(dataVentral[dataVentral > 0])
ventralNonSyncN = len(dataVentral[dataVentral == 0])
ventralSyncFrac = ventralSyncN/float(ventralSyncN + ventralNonSyncN)
ventralNonSyncFrac = ventralNonSyncN/float(ventralSyncN + ventralNonSyncN)

dorsalSyncN = len(dataDorsal[dataDorsal > 0])
dorsalNonSyncN = len(dataDorsal[dataDorsal == 0])
dorsalSyncFrac = dorsalSyncN/float(dorsalSyncN + dorsalNonSyncN)
dorsalNonSyncFrac = dorsalNonSyncN/float(dorsalSyncN + dorsalNonSyncN)


pieWedges = axMedialNSYNC.pie([medialNonSyncFrac, medialSyncFrac], colors=[colorMedial, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorMedial)
axMedialNSYNC.set_aspect('equal')

pieWedges = axVentralNSYNC.pie([ventralNonSyncFrac, ventralSyncFrac], colors=[colorVentral, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorVentral)
axVentralNSYNC.set_aspect('equal')

pieWedges = axDorsalNSYNC.pie([dorsalNonSyncFrac, dorsalSyncFrac], colors=[colorDorsal, 'w'], shadow=False, startangle=0)
for wedge in pieWedges[0]:
    wedge.set_edgecolor(colorDorsal)
axDorsalNSYNC.set_aspect('equal')


xBars = [-2, -3]
#Dorsal, Ventral, tagged
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


oddsratio, pValue = stats.fisher_exact([[dorsalSyncN, ventralSyncN],
                                        [dorsalNonSyncN, ventralNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axDorsalNSYNC, xBars[0], yCircleCenters[0], yCircleCenters[1]-0.1,
                    yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[ventralSyncN, medialSyncN],
                                        [ventralNonSyncN, medialNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axDorsalNSYNC, xBars[0], yCircleCenters[1]+0.1, yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)

oddsratio, pValue = stats.fisher_exact([[dorsalSyncN, medialSyncN],
                                        [dorsalNonSyncN, medialNonSyncN]])
if pValue < 0.05:
    starMarker = '*'
else:
    starMarker = 'n.s.'
plot_y_lines_with_ticks(axDorsalNSYNC, xBars[1], yCircleCenters[0], yCircleCenters[2],
                        yGapWidth, xTickWidth, starMarker=starMarker)


## -- Highest Sync -- ##
ax = axHighestSync
dataMedial = dataMedial[dataMedial>0]
dataMedial = np.log(dataMedial)

dataVentral = dataVentral[dataVentral>0]
dataVentral = np.log(dataVentral)

dataDorsal = dataDorsal[dataDorsal>0]
dataDorsal = np.log(dataDorsal)

# ytickLabels = np.logspace(np.log2(4), np.log2(128), 11, base=2)
ytickLabels = [4, 8, 16, 32, 64, 128]
yticks = np.log(ytickLabels)

# posMedial = jitter(np.ones(len(dataMedial))*0, 0.20)
# posVentral = jitter(np.ones(len(dataVentral))*1, 0.20)
# posDorsal = jitter(np.ones(len(dataDorsal))*2, 0.20)
# ax.plot(posMedial, dataMedial, 'o', mec = colorMedial, mfc = 'None')
# medline(axHighestSync, np.median(dataMedial), 0, 0.5)
# ax.plot(posVentral, dataVentral, 'o', mec = colorVentral, mfc = 'None')
# medline(axHighestSync, np.median(dataVentral), 1, 0.5)
# ax.plot(posDorsal, dataDorsal, 'o', mec = colorDorsal, mfc = 'None')
# medline(axHighestSync, np.median(dataDorsal), 2, 0.5)

boxData = [dataMedial, dataVentral, dataDorsal]
bp = axHighestSync.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorMedial, colorVentral, colorDorsal]
whiskerColors = [colorMedial, colorMedial, colorVentral,
                 colorVentral, colorDorsal, colorDorsal]
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
ax.set_xticklabels(['Medial\nN={}'.format(len(dataMedial)),
                    'Ventral\nN={}'.format(len(dataVentral)),
                    'Dorsal\nN={}'.format(len(dataDorsal))])
ax.set_yticks(yticks)
ax.set_yticklabels(ytickLabels)

#0-1
yMin = np.log(3)
yMax = np.log(128)
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = 0.1
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataMedial, dataVentral)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataVentral, dataDorsal)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor*1.5,
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataMedial, dataDorsal)
print "Highest Sync Rate, Medial/Dorsal zVal:{}, pVal:{}".format(zVal, pVal)
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

dataMedial = medialCellsAM[feature][pd.notnull(medialCellsAM[feature])]
dataMedial[dataMedial<0]=0

dataVentral = ventralCellsAM[feature][pd.notnull(ventralCellsAM[feature])]
dataVentral[dataVentral<0]=0

dataDorsal = dorsalCellsAM[feature][pd.notnull(dorsalCellsAM[feature])]
dataDorsal[dataDorsal<0]=0

# posMedial = jitter(np.ones(len(dataMedial))*0, 0.20)
# posVentral = jitter(np.ones(len(dataVentral))*1, 0.20)
# posDorsal = jitter(np.ones(len(dataDorsal))*2, 0.20)
# ax.plot(posMedial, dataMedial, 'o', mec = colorMedial, mfc = 'None')
# medline(axMIRate, np.median(dataMedial), 0, 0.5)
# ax.plot(posVentral, dataVentral, 'o', mec = colorVentral, mfc = 'None')
# medline(axMIRate, np.median(dataVentral), 1, 0.5)
# ax.plot(posDorsal, dataDorsal, 'o', mec = colorDorsal, mfc = 'None')
# medline(axMIRate, np.median(dataDorsal), 2, 0.5)

boxData = [dataMedial, dataVentral, dataDorsal]
bp = axMIRate.boxplot(boxData, widths=0.5, showfliers=False, positions=[0,1,2])

colors = [colorMedial, colorVentral, colorDorsal]
whiskerColors = [colorMedial, colorMedial, colorVentral,
                 colorVentral, colorDorsal, colorDorsal]
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
ax.set_xticklabels(['Medial\nN={}'.format(len(dataMedial)),
                    'Ventral\nN={}'.format(len(dataVentral)),
                    'Dorsal\nN={}'.format(len(dataDorsal))])

#0-1
yMin = 0
yMax = 0.3
yStars = [yMax*1.1, yMax*1.2]
yStarHeight = (yMax-yMin)*0.05
starGapFactor = [0.1, 0.2]
fontSizeStars = 9

zVal, pVal = stats.mannwhitneyu(dataMedial, dataVentral)
if pVal < 0.05:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([0, 0.9], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#1-2
zVal, pVal = stats.mannwhitneyu(dataVentral, dataDorsal)
if pVal < 0.05:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
else:
    extraplots.new_significance_stars([1.1, 2], yStars[0], yStarHeight, starMarker='n.s.',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor[1],
                                      ax=ax)
#0-2
zVal, pVal = stats.mannwhitneyu(dataMedial, dataDorsal)
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

dataMedial = np.full((len(medialCellsAM), len(possibleFreqKeys)), np.nan)
dataVentral = np.full((len(ventralCellsAM), len(possibleFreqKeys)), np.nan)
dataDorsal = np.full((len(dorsalCellsAM), len(possibleFreqKeys)), np.nan)

for externalInd, (indRow, row) in enumerate(medialCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataMedial[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(ventralCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataVentral[externalInd, indKey] = row[key]

for externalInd, (indRow, row) in enumerate(dorsalCellsAM.iterrows()):
    for indKey, key in enumerate(keys):
        dataDorsal[externalInd, indKey] = row[key]

dataMedial[dataMedial<0]=0
dataVentral[dataVentral<0]=0
dataDorsal[dataDorsal<0]=0

allPval = []
for indCol, freqKey in enumerate(possibleFreqKeys):
    dataMedialThisFreq = dataMedial[:,indCol][np.logical_not(np.isnan(dataMedial[:,indCol]))]
    dataVentralThisFreq = dataVentral[:,indCol][np.logical_not(np.isnan(dataVentral[:,indCol]))]
    dataDorsalThisFreq = dataDorsal[:,indCol][np.logical_not(np.isnan(dataDorsal[:,indCol]))]
    # zStat, pVal = stats.ranksums(dataMedialThisFreq, dataUntaggedThisFreq)
    # allPval.append(int(pVal<0.05))
    # print "{}Hz, p={}".format(freqKey, pVal)

taggedMean = np.nanmean(dataMedial, axis=0)
# taggedMean = np.nanmedian(dataMedial, axis=0)
taggedStd = np.nanstd(dataMedial, axis=0)

ventralMean = np.nanmean(dataVentral, axis=0)
ventralStd = np.nanstd(dataVentral, axis = 0)

dorsalMean = np.nanmean(dataDorsal, axis=0)
dorsalStd = np.nanstd(dataDorsal, axis = 0)

numMedial = sum(np.logical_not(np.isnan(dataMedial[:,0])))
numVentral = sum(np.logical_not(np.isnan(dataVentral[:,0])))
numDorsal = sum(np.logical_not(np.isnan(dataDorsal[:,0])))

ax.plot(taggedMean, '-', color=colorMedial, label='Medial, n={}'.format(numMedial))
plt.hold(1)
ax.plot(ventralMean, '--', color=colorVentral, label="Ventral, n={}".format(numVentral))
ax.plot(dorsalMean, '-.', color=colorDorsal, label="Dorsal, n={}".format(numDorsal))
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
