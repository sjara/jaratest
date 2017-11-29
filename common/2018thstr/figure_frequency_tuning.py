import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
import pandas as pd
import figparams
reload(figparams)

FIGNAME = 'figure_frequency_tuning'
exampleDataPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME, 'data_freq_tuning_examples.npz')
exData = np.load(exampleDataPath)

dbPath = '/home/nick/data/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')
goodLaser = db.query('isiViolations<0.02 and spikeShapeQuality>2 and pulsePval<0.05 and trainRatio>0.8')
#Use the good Laser 
goodStriatum = db.groupby('brainArea').get_group('rightAstr').query('isiViolations<0.02 and spikeShapeQuality>2')
goodLaserPlusStriatum = goodLaser.append(goodStriatum, ignore_index=True)

PANELS = [1, 1, 1, 1, 1, 0, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_frequency_tuning' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,7] # In inches

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

gs = gridspec.GridSpec(6, 3)
gs.update(left=0.15, right=0.98, top=0.95, bottom=0.05, wspace=.4, hspace=0.5)


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
axSharp = plt.subplot(gs[0:2, 0])
axSharp.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[0]:
    # Plot stuff
    plt.imshow(np.flipud(exData['Thal2']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')
# -- Panel: Thalamus wide tuning --
axWide = plt.subplot(gs[0:2, 1])
axWide.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    # Plot stuff
    plt.imshow(np.flipud(exData['Thal1']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')

##### Cortex #####
# -- Panel: Cortex sharp tuning --
axSharp = plt.subplot(gs[2:4, 0])
axSharp.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[3]:
    # Plot stuff
    plt.imshow(np.flipud(exData['AC1']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')
    pass
# -- Panel: Cortex wide tuning --
axWide = plt.subplot(gs[2:4, 1])
axWide.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[4]:
    # Plot stuff
    pass
    plt.imshow(np.flipud(exData['AC2']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')


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
axSharp = plt.subplot(gs[4:6, 0])
axSharp.annotate('G', xy=(labelPosX[0],labelPosY[2]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[6]:
    # Plot stuff
    plt.imshow(np.flipud(exData['Str1']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')
    pass
# -- Panel: Striatum wide tuning --
axWide = plt.subplot(gs[4:6, 1])
axWide.annotate('H', xy=(labelPosX[1],labelPosY[2]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[7]:
    # Plot stuff
    pass
    plt.imshow(np.flipud(exData['Str2']), interpolation='none', cmap='Blues')
    # ax.set_yticks(range(len(possibleIntensity)))
    # ax.set_yticklabels(possibleIntensity[::-1])
    # ax.set_xticks(range(len(possibleFreq)))
    # freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    # ax.set_xticklabels(freqLabels, rotation='vertical')
    # ax.set_xlabel('Frequency (kHz)')
    # plt.ylabel('Intensity (db SPL)')




# -- Panel: Thalamus histogram --
axHist = plt.subplot(gs[0:3, 2])
plt.hold(True)
axHist.annotate('C', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    goodLaserPlusStriatum.boxplot(ax=axHist, column='BW10', by='brainArea')
    plt.ylabel('BW10')
    plt.ylim([0, 4.5])
    pass

# -- Panel: Striatum histogram --
axHist = plt.subplot(gs[3:6, 2])
plt.hold(True)
axHist.annotate('I', xy=(labelPosX[2],labelPosY[2]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')
if PANELS[8]:
    goodLaserPlusStriatum.boxplot(ax=axHist, column='threshold', by='brainArea')
    plt.ylabel('Threshold (dB SPL)')
    plt.ylim([0, 80])

plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
