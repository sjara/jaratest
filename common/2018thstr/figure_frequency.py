import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import celldatabase
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
titleExampleBW=False
exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_with_latency.h5')
db = pd.read_hdf(dbPath, key='dataframe')
db = db.query("subject=='pinp015'")
exData = np.load(exampleDataPath)
np.random.seed(8)

goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
# goodStriatum = db.groupby('brainArea').get_group('rightAstr').query('isiViolations<0.02 and spikeShapeQuality>2')
# goodLaserPlusStriatum = goodLaser.append(goodStriatum, ignore_index=True)
goodFit = goodLaser.query('rsquaredFit > 0.08')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

#Which dataframe to use
# dataframe = goodFit
dataframe = goodFitToUse

PANELS = [0, 0, 0, 0, 0, 0, 0, 0, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
# outputDir = '/tmp/'
outputDir = figparams.FIGURE_OUTPUT_DIR
figFilename = 'plots_frequency_tuning' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
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
tcColorMap = 'bone'
colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']

labelPosX = [0.03, 0.24, 0.45, 0.64, 0.835]   # Horiz position for panel labels
labelPosY = [0.92, 0.42]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

examples = {}
examples.update({'AC1' : {'subject':'pinp016', 'date':'2017-03-09', 'depth':1904, 'tetrode':6, 'cluster':6}})
examples.update({'AC2' :{'subject':'pinp017', 'date':'2017-03-22', 'depth':1143, 'tetrode':6, 'cluster':5}})

#Thalamus
examples.update({'Thal1' :{'subject':'pinp015', 'date':'2017-02-15', 'depth':3110, 'tetrode':7, 'cluster':3}})
examples.update({'Thal2' :{'subject':'pinp016', 'date':'2017-03-16', 'depth':3800, 'tetrode':3, 'cluster':6}})


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#Define the layout
gs = gridspec.GridSpec(2, 9)
gs.update(left=-0.01, right=0.98, top=0.88, bottom=0.125, wspace=0.8, hspace=0.5)

axBlank1 = plt.subplot(gs[0, 0:3])
axBlank1.axis('off')
axBlank2 = plt.subplot(gs[1, 0:3])
axBlank2.axis('off')

axThalamus = plt.subplot(gs[0, 3:6])
axCortex = plt.subplot(gs[1, 3:6])

axBW = plt.subplot(gs[0:2, 6])
axThresh = plt.subplot(gs[0:2, 7])
axLatency = plt.subplot(gs[0:2, 8])

plt.text(0.1, 1.2, 'A', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axBlank1.transAxes)
plt.text(-0.2, 1.2, 'B', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axThalamus.transAxes)
plt.text(0.1, 1.2, 'C', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axBlank2.transAxes)
plt.text(-0.2, 1.2, 'D', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axCortex.transAxes)
plt.text(-0.3, 1.07, 'E', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axBW.transAxes)
plt.text(-0.3, 1.07, 'F', ha='center', va='center',
         fontsize=fontSizePanel, fontweight='bold',
         transform=axThresh.transAxes)
plt.text(-0.3, 1.07, 'G', ha='center', va='center',
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


##### Cells to use #####
# Criteria: Want cells where the threshold and flanks are well-captured.
#AC1 - pinp016 2017-03-09 1904 TT6c6: Beautiful cell with wide looking tuning
#AC2 - pinp017 2017-03-22 1143 TT6c5: Sharper looking tuning on this cell

#Thal1 - pinp015 2017-02-15 3110 TT7c3
#Thal2 - pinp016 2017-03-16 3880 TT3c6

#Check these cells later to make sure they are in the striatum...
#Str1 - pinp020 2017-05-10 2682 TT7c3: Good looking tuning but threshold at 15
#Str2 - pinp025 2017-09-01 2111 TT4c3: High threshold but good tuning

##### Thalamus #####
# -- Panel: Thalamus sharp tuning --

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
    # Plot stuff
    exampleKey = 'Thal2'
    exDataFR = exData[exampleKey]/0.1
    # cax = axThalamus.imshow(np.flipud(exDataFR), interpolation='nearest', cmap='Blues')
    cax = axThalamus.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=tcColorMap)
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

    cellDict = examples[exampleKey]
    cellInd, cell = celldatabase.find_cell(dataframe, **cellDict)
    if titleExampleBW:
        axThalamus.set_title('ATh->Str, BW10={:.2f}'.format(cell['BW10']), fontsize=fontSizeTitles)
    else:
        axThalamus.set_title('ATh->Str Example', fontsize=fontSizeTitles)


##### Cortex #####
# -- Panel: Cortex sharp tuning --
if PANELS[3]:
    # Plot stuff
    exampleKey = 'AC2'

    exDataFR = exData[exampleKey]/0.1
    # cax = axCortex.imshow(np.flipud(exDataFR), interpolation='nearest', cmap='Blues')
    cax = axCortex.imshow(np.flipud(exDataFR), interpolation='nearest', cmap=tcColorMap)
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
    cellDict = examples[exampleKey]
    cellInd, cell = celldatabase.find_cell(dataframe, **cellDict)

    if titleExampleBW:
        axCortex.set_title('AC->Str, BW10={:.2f}'.format(cell['BW10']))
    else:
        axCortex.set_title('AC->Str Example', fontsize=fontSizeTitles)

order = ['rightThal', 'rightAC'] # Should match 'tickLabels'
colors = {'rightThal':colorATh, 'rightAC':colorAC}
tickLabels = ['ATh\nv\nAStr', 'AC\nv\nAStr']       # Should match 'order'
groups = dataframe.groupby('brainArea')

plt.hold(True)
if PANELS[8]:
    column = 'BW10'
    order_n = []
    axBW.hold(True)
    dataList = []
    for position, groupName in enumerate(order):
        data = groups.get_group(groupName)[column].values
        pos = jitter(np.ones(len(data))*position, 0.20)
        axBW.plot(pos, data, 'o', mec=colors[groupName], mfc='None', alpha=0.5)
        medline(axBW, np.median(data), position, 0.5)
        order_n.append(len(data))
        dataList.append(data)
    axBW.set_xticks(range(2))
    axBW.set_xticklabels(tickLabels)
    axBW.set_xlim([-0.5, 1.5])

    yDataMax = max([np.nanmax(l) for l in dataList])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    plt.sca(axBW)
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker='ns',
                                      fontSize=fontSizeNS, gapFactor=starGapFactor)
    axBW.set_ylim([0, yStars + yStarHeight])

    axBW.set_ylabel('BW10')
    zVal, pVal = stats.ranksums(*dataList)
    extraplots.boxoff(axBW)
    plt.hold(1)
    # plt.title('ATh -> Str N: {}\nAC -> Str N: {}'.format(order_n[0], order_n[1]))
    # plt.title('p = {:.03f}'.format(pVal), fontsize=fontSizeTitles)

plt.hold(True)
if PANELS[8]:
    column='threshold'
    order_n = []
    dataList = []
    for position, groupName in enumerate(order):
        data = groups.get_group(groupName)[column].values
        pos = jitter(np.ones(len(data))*position, 0.20)
        axThresh.plot(pos, data, 'o', mec=colors[groupName], mfc='None', alpha=0.5)
        medline(axThresh, np.median(data), position, 0.5)
        order_n.append(len(data))
        dataList.append(data)
    axThresh.set_xticks(range(2))
    axThresh.set_xticklabels(tickLabels)
    axThresh.set_xlim([-0.5, 1.5])
    axThresh.set_ylabel('Threshold (dB SPL)')
    extraplots.boxoff(axThresh)
    zVal, pVal = stats.ranksums(*dataList)
    # plt.title('p = {:.03f}'.format(pVal), fontsize=fontSizeTitles)
    # extraplots.significance_stars([0, 1], 70, 2.5, starMarker='*')

    yDataMax = max([np.nanmax(l) for l in dataList])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    plt.sca(axThresh)
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker='*',
                                      fontSize=fontSizeStars, gapFactor=starGapFactor)
    axThresh.set_ylim([0, yStars + yStarHeight])
    plt.hold(1)

if PANELS[8]:
    column='latency'
    order_n = []
    dataList = []

    for position, groupName in enumerate(order):
        data = groups.get_group(groupName)[column].values * 1000
        pos = jitter(np.ones(len(data))*position, 0.20)
        axLatency.plot(pos, data, 'o', mec=colors[groupName], mfc='None', alpha=0.5)
        medline(axLatency, np.nanmedian(data), position, 0.5)
        order_n.append(len(data))
        dataList.append(data)
        # 1/0

    extraplots.boxoff(axLatency)
    axLatency.set_xticks(range(2))
    axLatency.set_xticklabels(tickLabels)
    axLatency.set_xlim([-0.5, 1.5])
    axLatency.set_ylabel('Latency to first spike (ms)')

    zVal, pVal = stats.ranksums(*dataList)

    yDataMax = max([np.nanmax(l) for l in dataList])
    yStars = yDataMax + yDataMax*starYfactor
    yStarHeight = (yDataMax*starYfactor)*starHeightFactor
    plt.sca(axLatency)
    extraplots.new_significance_stars([0, 1], yStars, yStarHeight, starMarker='ns',
                                      fontSize=fontSizeNS, gapFactor=starGapFactor)
    axLatency.set_ylim([0, yStars + yStarHeight])
    plt.hold(1)

    #TODO: put font size in figparams?
    fontSizeNLabel = 10


#TODO: put font size in figparams?
# fontSizeNLabel = 10
# axThresh.annotate('N = {} ATh->Str \nN = {} AC->Str'.format(order_n[0], order_n[1]),
#                 xy=(0.88, 0.82), xycoords='figure fraction', fontsize=fontSizeNLabel, fontweight='bold')


plt.show()

ath = dataframe.groupby('brainArea').get_group('rightThal')
ac = dataframe.groupby('brainArea').get_group('rightAC')
# thalBW = thal['BW10'][pd.notnull(thal['BW10'])]
# ACBW = AC['BW10'][pd.notnull(thal['BW10'])]
athBW = ath['BW10']
acBW = ac['BW10']
stat, pVal = stats.ranksums(athBW, acBW)
print "p (BW10) = {}".format(pVal)

athThresh = ath['threshold']
acThresh = ac['threshold']
stat, pVal = stats.ranksums(athThresh, acThresh)
print "p (threshold) = {}".format(pVal)

athLatency = ath['latency']
acLatency = ac['latency']
stat, pVal = stats.ranksums(athLatency, acLatency)
print "p (latency) = {}".format(pVal)

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
