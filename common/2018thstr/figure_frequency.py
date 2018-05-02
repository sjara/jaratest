import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from scipy import stats
import pandas as pd
import figparams
reload(extraplots)
reload(figparams)

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(ax, yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    ax.plot([start, end], [yval, yval], color=color, lw=linewidth)

FIGNAME = 'figure_frequency_tuning'
titleExampleBW=True
exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_ALLCELLS_MODIFIED_CLU.h5')
db = pd.read_hdf(dbPath, key='dataframe')
exData = np.load(exampleDataPath)
np.random.seed(8)

goodISI = db.query('isiViolations<0.02 or modifiedISI<0.02')
goodShape = goodISI.query('spikeShapeQuality > 2')
goodLaser = goodShape.query("autoTagged==1 and subject != 'pinp018'")

goodFit = goodLaser.query('rsquaredFit > 0.04')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')
goodFitToUseNSpikes = goodFitToUse.query('nSpikes>2000')

#Which dataframe to use
dataframe = goodFitToUseNSpikes

ac = dataframe.groupby('brainArea').get_group('rightAC')
thal = dataframe.groupby('brainArea').get_group('rightThal')

PANELS = [1, 1, 1, 1, 1, 1, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
# outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'figure_frequency_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12, 5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeTitles = figparams.fontSizeTitles

#Params for extraplots significance stars
fontSizeNS = figparams.fontSizeNS
fontSizeStars = figparams.fontSizeStars
starHeightFactor = figparams.starHeightFactor
starGapFactor = figparams.starGapFactor
starYfactor = figparams.starYfactor

dotEdgeColor = figparams.dotEdgeColor
# tcColorMap = 'magma'
# tcColorMap = 'bone'
thalColorMap = 'Blues'
acColorMap = 'Reds'

colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']
markerAlpha = 1

labelPosX = [0.03, 0.24, 0.45, 0.64, 0.835]   # Horiz position for panel labels
labelPosY = [0.92, 0.42]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#Define the layout
gs = gridspec.GridSpec(2, 6)
gs.update(left=-0.2, right=0.98, top=0.88, bottom=0.125, wspace=0.4, hspace=0.5)

# axBlank1 = plt.subplot(gs[0, 0:3])
# axBlank1.axis('off')
# axBlank2 = plt.subplot(gs[1, 0:3])
# axBlank2.axis('off')

axThalamus = plt.subplot(gs[0, 0:3])
axCortex = plt.subplot(gs[1, 0:3])

axBW = plt.subplot(gs[0:2,3])
axThresh = plt.subplot(gs[0:2, 4])
axLatency = plt.subplot(gs[0:2, 5])

# plt.text(0.1, 1.2, 'A', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axBlank1.transAxes)
plt.text(-0.2, 1.2, 'A', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axThalamus.transAxes)
# plt.text(0.1, 1.2, 'C', ha='center', va='center',
#          fontsize=fontSizePanel, fontweight='bold',
#          transform=axBlank2.transAxes)
plt.text(-0.2, 1.2, 'B', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axCortex.transAxes)
plt.text(-0.3, 1.07, 'C', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axBW.transAxes)
plt.text(-0.3, 1.07, 'D', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axThresh.transAxes)
plt.text(-0.3, 1.07, 'E', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axLatency.transAxes)

# axThalamus.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# axThalamus.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')

# axCortex.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# axCortex.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# axBW.annotate('G', xy=(labelPosX[3],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# axBW.annotate('H', xy=(labelPosX[4],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')

messages = []

##### Thalamus #####

lowFreq = 2
highFreq = 40
nFreqLabels = 3

freqTickLocations = np.linspace(0, 15, nFreqLabels)
freqs = np.logspace(np.log10(lowFreq),np.log10(highFreq),nFreqLabels)
freqs = np.round(freqs, decimals=1)

nIntenLabels = 3
intensities = np.linspace(15, 70, nIntenLabels)
intenTickLocations = np.linspace(0, 11, nIntenLabels)

if PANELS[0]:
    exampleKey = 'Thal0'
    exDataFR = exData[exampleKey]/0.1
    # cax = axThalamus.imshow(np.flipud(exDataFR), interpolation='nearest', cmap='Blues')
    cax = axThalamus.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=thalColorMap)
    # cbar = plt.colorbar(cax, ax=axThalamus, format='%.1f')
    cbar = plt.colorbar(cax, ax=axThalamus, format='%d')
    maxFR = np.max(exDataFR.ravel())
    cbar.ax.set_ylabel('Firing rate\n(spk/sec)', fontsize = fontSizeTicks, labelpad=-10)
    extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
    cbar.set_ticks([0, maxFR])
    cax.set_clim([0, maxFR])

    axThalamus.set_yticks(intenTickLocations)
    axThalamus.set_yticklabels(intensities[::-1])
    axThalamus.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # axThalamus.set_xticklabels(freqLabels, rotation='vertical')
    axThalamus.set_xticklabels(freqLabels)
    axThalamus.set_xlabel('Frequency (kHz)')
    axThalamus.set_ylabel('Intensity (dB SPL)')

    # cellDict = examples[exampleKey]
    # # cellInd, cell = celldatabase.find_cell(dataframe, **cellDict)
    # cellInd, cell = celldatabase.find_cell(db, **cellDict)
    # if titleExampleBW:
    #     axThalamus.set_title('ATh->Str, BW10={:.2f}'.format(cell['BW10']), fontsize=fontSizeTitles)
    # else:
    #     axThalamus.set_title('ATh->Str Example', fontsize=fontSizeTitles)


##### Cortex #####
if PANELS[3]:
    exampleKey = 'AC0'

    exDataFR = exData[exampleKey]/0.1
    # cax = axCortex.imshow(np.flipud(exDataFR), interpolation='nearest', cmap='Blues')
    cax = axCortex.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=acColorMap)
    cbar = plt.colorbar(cax, ax=axCortex, format='%d')
    maxFR = np.max(exDataFR.ravel())
    cbar.ax.set_ylabel('Firing rate\n(spk/sec)', fontsize = fontSizeTicks, labelpad=-10)
    extraplots.set_ticks_fontsize(cbar.ax, fontSizeTicks)
    cbar.set_ticks([0, maxFR])
    cax.set_clim([0, maxFR])

    # im = axCortex.imshow(np.flipud(exData[exampleKey]), interpolation='nearest', cmap='Blues')
    # plt.colorbar(im, ax=axCortex)

    axCortex.set_yticks(intenTickLocations)
    axCortex.set_yticklabels(intensities[::-1])
    axCortex.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # axCortex.set_xticklabels(freqLabels, rotation='vertical')
    axCortex.set_xticklabels(freqLabels)
    axCortex.set_xlabel('Frequency (kHz)')
    axCortex.set_ylabel('Intensity (dB SPL)')
    # plt.title('AC->Str Example 1')
    # cellDict = examples[exampleKey]
    # cellInd, cell = celldatabase.find_cell(db, **cellDict)

    # if titleExampleBW:
    #     axCortex.set_title('AC->Str, BW10={:.2f}'.format(cell['BW10']))
    # else:
    #     axCortex.set_title('AC->Str Example', fontsize=fontSizeTitles)

order = ['rightThal', 'rightAC'] # Should match 'tickLabels'
colors = {'rightThal':colorATh, 'rightAC':colorAC}
groups = dataframe.groupby('brainArea')

plt.hold(True)
if PANELS[8]:

    popStatCol = 'BW10'
    acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
    thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

    pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
    axBW.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)
    medline(axBW, np.median(thalPopStat), 0, 0.5)
    pos = jitter(np.ones(len(acPopStat))*1, 0.20)
    axBW.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)
    medline(axBW, np.median(acPopStat), 1, 0.5)
    axBW.set_ylabel('BW10')
    # tickLabels = ['ATh:Str', 'AC:Str']
    tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
    axBW.set_xticks(range(2))
    axBW.set_xticklabels(tickLabels)
    axBW.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axBW)
    # axBW.set_ylim([-0.001, 0.25])

    zstat, pVal = stats.ranksums(thalPopStat, acPopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
    messages.append("{} p={}".format(popStatCol, pVal))

    yDataMax = max([max(acPopStat), max(thalPopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    plt.sca(axBW)
    starString = None if pVal<0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars+2, starString=starString,
                                  gapFactor=starGapFactor)
    plt.hold(1)

plt.hold(True)
if PANELS[8]:


    popStatCol = 'threshold'
    acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
    thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

    plt.sca(axThresh)

    spacing = 0.05

    # pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
    # axThresh.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)
    markers = extraplots.spread_plot(0, thalPopStat, spacing)
    # plt.setp(markers, mec = colorATh, mfc = 'None', alpha=markerAlpha)
    plt.setp(markers, mec = colorATh, mfc = 'None')
    medline(axThresh, np.median(thalPopStat), 0, 0.5)

    # pos = jitter(np.ones(len(acPopStat))*1, 0.20)
    # axThresh.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)
    markers = extraplots.spread_plot(1, acPopStat, spacing)
    # plt.setp(markers, mec = colorAC, mfc = 'None', alpha=markerAlpha)
    plt.setp(markers, mec = colorAC, mfc = 'None')

    medline(axThresh, np.median(acPopStat), 1, 0.5)
    axThresh.set_ylabel('Threshold (dB SPL)')
    # tickLabels = ['ATh:Str', 'AC:Str']
    tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
    axThresh.set_xticks(range(2))
    axThresh.set_xticklabels(tickLabels)
    axThresh.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axThresh)
    # axThresh.set_ylim([-0.001, 0.25])

    zstat, pVal = stats.ranksums(thalPopStat, acPopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
    messages.append("{} p={}".format(popStatCol, pVal))

    '''
    if pVal<0.05:
        starMarker='*'
    else:
        starMarker='n.s.'
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker=starMarker,
                                      fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=axThresh)
    '''
    yDataMax = max([max(acPopStat), max(thalPopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    starString = None if pVal<0.05 else 'n.s.'
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)

    plt.hold(1)


if PANELS[8]:

    popStatCol = 'latency'
    acPopStat = ac[popStatCol][pd.notnull(ac[popStatCol])]
    thalPopStat = thal[popStatCol][pd.notnull(thal[popStatCol])]

    pos = jitter(np.ones(len(thalPopStat))*0, 0.20)
    axLatency.plot(pos, thalPopStat, 'o', mec = colorATh, mfc = 'None', alpha=markerAlpha)
    medline(axLatency, np.median(thalPopStat), 0, 0.5)
    pos = jitter(np.ones(len(acPopStat))*1, 0.20)
    axLatency.plot(pos, acPopStat, 'o', mec = colorAC, mfc = 'None', alpha=markerAlpha)
    medline(axLatency, np.median(acPopStat), 1, 0.5)
    axLatency.set_ylabel('Latency (s)')
    # tickLabels = ['ATh:Str', 'AC:Str']
    tickLabels = ['ATh:Str\nn={}'.format(len(thalPopStat)), 'AC:Str\nn={}'.format(len(acPopStat))]
    axLatency.set_xticks(range(2))
    axLatency.set_xticklabels(tickLabels)
    axLatency.set_xlim([-0.5, 1.5])
    extraplots.boxoff(axLatency)
    axLatency.set_ylim([-0.001, 0.07])

    zstat, pVal = stats.ranksums(thalPopStat, acPopStat)

    # print "Ranksums test between thalamus and AC population stat ({}) vals: p={}".format(popStatCol, pVal)
    messages.append("{} p={}".format(popStatCol, pVal))

    '''
    if pVal<0.05:
        starMarker='*'
    else:
        starMarker='n.s.'
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker=starMarker,
                                        fontSize=fontSizeStars, gapFactor=starGapFactor,
                                      ax=axLatency)
    '''
    yDataMax = max([max(acPopStat), max(thalPopStat)])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    starString = None if pVal<0.05 else 'n.s.'
    plt.sca(axLatency)
    extraplots.significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                  starSize=fontSizeStars, starString=starString,
                                  gapFactor=starGapFactor)
    plt.hold(1)


plt.show()

print "\nSTATISTICS:\n"
for message in messages:
    print(message)
print "\n"

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
