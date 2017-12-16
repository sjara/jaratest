import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from scipy import stats
import pandas as pd
import figparams
reload(figparams)

FIGNAME = 'figure_frequency_tuning'
exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
# dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase_with_latency.h5')
db = pd.read_hdf(dbPath, key='dataframe')
exData = np.load(exampleDataPath)
np.random.seed(0)

goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
goodStriatum = db.groupby('brainArea').get_group('rightAstr').query('isiViolations<0.02 and spikeShapeQuality>2')
goodLaserPlusStriatum = goodLaser.append(goodStriatum, ignore_index=True)
goodFit = goodLaserPlusStriatum.query('rsquaredFit > 0.08')

#Calculate the midpoint of the gaussian fit
goodFit['fitMidPoint'] = np.sqrt(goodFit['upperFreq']*goodFit['lowerFreq'])
goodFitToUse = goodFit.query('fitMidPoint<32000')

#Which dataframe to use
# dataframe = goodFit
dataframe = goodFitToUse

PANELS = [1, 1, 1, 1, 1, 0, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'plots_frequency_tuning' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [20, 5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.39, 0.69]   # Horiz position for panel labels
labelPosY = [0.92, 0.60, 0.28]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 6)
gs.update(left=0.1, right=0.98, top=0.88, bottom=0.10, wspace=0.5, hspace=0.5)

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
axSharp = plt.subplot(gs[0, 1])
# axSharp.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')

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
    ax = axSharp
    plt.imshow(np.flipud(exData['Thal2']), interpolation='none', cmap='Blues')
    ax.set_yticks(intenTickLocations)
    ax.set_yticklabels(intensities[::-1])
    ax.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    ax.set_xticklabels(freqLabels)
    ax.set_xlabel('Frequency (kHz)')
    plt.ylabel('Intensity (db SPL)')
    plt.title('ATh -> Str Example 1')

# -- Panel: Thalamus wide tuning --
axWide = plt.subplot(gs[0, 2])
# axWide.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    # Plot stuff
    ax = axWide
    plt.imshow(np.flipud(exData['Thal1']), interpolation='none', cmap='Blues')
    ax.set_yticks(intenTickLocations)
    ax.set_yticklabels(intensities[::-1])
    ax.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    ax.set_xticklabels(freqLabels)
    ax.set_xlabel('Frequency (kHz)')
    plt.ylabel('Intensity (db SPL)')
    plt.title('ATh -> Str Example 2')

##### Cortex #####
# -- Panel: Cortex sharp tuning --
axSharp = plt.subplot(gs[1, 1])
# axSharp.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[3]:
    # Plot stuff
    ax = axSharp
    plt.imshow(np.flipud(exData['AC1']), interpolation='none', cmap='Blues')
    ax.set_yticks(intenTickLocations)
    ax.set_yticklabels(intensities[::-1])
    ax.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    ax.set_xticklabels(freqLabels)
    ax.set_xlabel('Frequency (kHz)')
    plt.ylabel('Intensity (db SPL)')
    plt.title('AC -> Str Example 1')

# -- Panel: Cortex wide tuning --
axWide = plt.subplot(gs[1, 2])
# axWide.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[4]:
    # Plot stuff
    ax = axWide
    plt.imshow(np.flipud(exData['AC2']), interpolation='none', cmap='Blues')
    ax.set_yticks(intenTickLocations)
    ax.set_yticklabels(intensities[::-1])
    ax.set_xticks(freqTickLocations)
    freqLabels = ['{0:.1f}'.format(freq) for freq in freqs]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    ax.set_xticklabels(freqLabels)
    ax.set_xlabel('Frequency (kHz)')
    plt.ylabel('Intensity (db SPL)')
    plt.title('AC -> Str Example 2')

# -- Panel: Cortex histogram --
# axHist = plt.subplot(gs[1, 2])
# axHist.annotate('F', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# axHist.set_xlabel('BW10')
# axHist.set_ylabel('% Neurons')
# if PANELS[5]:
#     # Plot stuff
#     pass

##### Striatum #####
# -- Panel: Striatum sharp tuning --
# axSharp = plt.subplot(gs[4:6, 0])
# axSharp.annotate('G', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# if PANELS[6]:
    # Plot stuff
    # plt.imshow(np.flipud(exData['Str1']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')

# -- Panel: Striatum wide tuning --
# axWide = plt.subplot(gs[4:6, 1])
# axWide.annotate('H', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
# if PANELS[7]:
    # Plot stuff
    # plt.imshow(np.flipud(exData['Str2']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')

# -- Panel: Thalamus histogram --

def jitter(arr, frac):
    jitter = (np.random.random(len(arr))-0.5)*2*frac
    jitteredArr = arr + jitter
    return jitteredArr

def medline(yval, midline, width, color='k', linewidth=3):
    start = midline-(width/2)
    end = midline+(width/2)
    plt.plot([start, end], [yval, yval], color=color, lw=linewidth)

order = ['rightThal', 'rightAC']
groups = dataframe.groupby('brainArea')

axHist = plt.subplot(gs[0:2, 3])
plt.hold(True)
# axHist.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    column = 'BW10'
    order_n = []
    axHist.hold(True)
    for position, groupName in enumerate(order):
        data = groups.get_group(groupName)[column].values
        pos = jitter(np.ones(len(data))*position, 0.20)
        axHist.plot(pos, data, 'o', mec = 'k', mfc = 'None')
        medline(np.median(data), position, 0.5)
        order_n.append(len(data))
    axHist.set_xticks(range(2))
    axHist.set_xticklabels(order)
    axHist.set_xlim([-0.5, 1.5])
    plt.ylabel('BW10')
    # plt.ylim([0, 4.5])
    extraplots.boxoff(axHist)
    # plt.title('ATh -> Str N: {}\nAC -> Str N: {}'.format(order_n[0], order_n[1]))

axHist = plt.subplot(gs[0:2, 4])
plt.hold(True)
# axHist.annotate('I', xy=(labelPosX[2],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[8]:
    column='threshold'
    order_n = []
    for position, groupName in enumerate(order):
        data = groups.get_group(groupName)[column].values
        pos = jitter(np.ones(len(data))*position, 0.20)
        axHist.plot(pos, data, 'o', mec = 'k', mfc = 'None')
        medline(np.median(data), position, 0.5)
        order_n.append(len(data))
    axHist.set_xticks(range(2))
    axHist.set_xticklabels(order)
    axHist.set_xlim([-0.5, 1.5])
    plt.ylabel('Threshold (dB SPL)')
    plt.ylim([0, 80])
    extraplots.boxoff(axHist)
    plt.title('ATh -> Str N: {}\nAC -> Str N: {}'.format(order_n[0], order_n[1]))

axHist = plt.subplot(gs[0:2, 5])
plt.hold(True)
# axHist.annotate('I', xy=(labelPosX[2],labelPosY[2]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[8]:
    column='latency'
    order_n = []
    for position, groupName in enumerate(order):
        data = groups.get_group(groupName)[column].values*1000
        pos = jitter(np.ones(len(data))*position, 0.20)
        axHist.plot(pos, data, 'o', mec = 'k', mfc = 'None')
        medline(np.median(data), position, 0.5)
        order_n.append(len(data))
    axHist.set_xticks(range(2))
    axHist.set_xticklabels(order)
    axHist.set_xlim([-0.5, 1.5])
    # axHist.set_ylim([0, 65])
    plt.ylabel('Median latency to first spike (ms)')
    extraplots.boxoff(axHist)
    # plt.title('ATh -> Str N: {}\nAC -> Str N: {}'.format(order_n[0], order_n[1]))

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
