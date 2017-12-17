import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from collections import Counter
import pandas as pd
import figparams
reload(figparams)

FIGNAME = 'figure_am'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'celldatabase.h5')

PANELS = [1, 1, 1, 1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'plots_figure_name' # Do not include extension
figFormat = 'svg' # 'pdf' or 'svg'
figSize = [7,5] # In inches

thalHistColor = '0.4'
acHistColor = '0.4'

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.07, 0.36, 0.7]   # Horiz position for panel labels
labelPosY = [0.9, 0.48, 0.19]    # Vert position for panel labels

# Define colors, use figparams
laserColor = figparams.colp['blueLaser']
colorATh = figparams.cp.TangoPalette['SkyBlue2']
colorAC = figparams.cp.TangoPalette['ScarletRed1']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2)
gs.update(left=0.1, right=0.90, top=0.95, bottom=0.1, wspace=.2, hspace=0.3)

#Load example data
exampleDataPath = os.path.join(dataDir, 'data_am_examples.npz')
exampleData = np.load(exampleDataPath)

exampleFreqEachTrial = exampleData['exampleFreqEachTrial'].item()
exampleSpikeTimes = exampleData['exampleSpikeTimes'].item()
exampleTrialIndexForEachSpike = exampleData['exampleTrialIndexForEachSpike'].item()
exampleIndexLimitsEachTrial = exampleData['exampleIndexLimitsEachTrial'].item()

def plot_example_with_rate(subplotSpec, exampleName, color='k'):
    fig = plt.gcf()

    gs = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=subplotSpec, wspace=-0.45, hspace=0.0 )

    specRaster = gs[0:2]
    axRaster = plt.Subplot(fig, specRaster)
    fig.add_subplot(axRaster)

    spikeTimes = exampleSpikeTimes[exampleName]
    indexLimitsEachTrial = exampleIndexLimitsEachTrial[exampleName]
    timeRange = [-0.2, 0.7]
    freqEachTrial = exampleFreqEachTrial[exampleName]
    possibleFreq = np.unique(freqEachTrial)
    freqLabels = ['{0:.1f}'.format(freq) for freq in possibleFreq]
    trialsEachCondition = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    pRaster, hCond, zline = extraplots.raster_plot(spikeTimes, indexLimitsEachTrial,
                                                   timeRange, trialsEachCondition, labels=freqLabels)
    plt.setp(pRaster, ms=2)
    ax = plt.gca()
    ax.set_xticks([0, 0.5])
    ax.set_xlabel('Time from sound onset (s)')
    ax.set_ylabel('AM Rate (Hz)')


    countRange = [0.1, 0.5]
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimes,indexLimitsEachTrial,countRange)
    numSpikesInTimeRangeEachTrial = np.squeeze(spikeCountMat)

    numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial,
                                                       axis=0))

    if len(numSpikesInTimeRangeEachTrial) == len(freqEachTrial)+1:
        numSpikesInTimeRangeEachTrial = numSpikesInTimeRangeEachTrial[:-1]
    conditionMatShape = np.shape(trialsEachCondition)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats),
                            conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat * trialsEachCondition
    avgSpikesArray = np.sum(spikesFilteredByTrialType, 0) / np.sum(
        trialsEachCondition, 0).astype('float')/np.diff(np.array(countRange))
    stdSpikesArray = np.std(spikesFilteredByTrialType, 0)/np.diff(np.array(countRange))

    specRate = gs[3]
    axRate = plt.Subplot(fig, specRate)
    fig.add_subplot(axRate)

    nRates = len(possibleFreq)
    plt.hold(True)
    plt.plot(avgSpikesArray, range(nRates), 'ro-', mec='none', ms=7, lw=3, color=color)
    plt.plot(avgSpikesArray-stdSpikesArray, range(len(possibleFreq)), 'k:')
    plt.plot(avgSpikesArray+stdSpikesArray, range(len(possibleFreq)), 'k:')
    axRate.set_ylim([-0.5, nRates-0.5])
    axRate.set_yticks(range(nRates))
    axRate.set_yticklabels([])
    
    #ax = plt.gca()
    axRate.set_xlabel('Firing rate (spk/s)')
    extraplots.boxoff(axRate)
    # extraplots.boxoff(ax, keep='right')
    return (axRaster, axRate)

spec = gs[0, 0]

if PANELS[0]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'Thal1', color=colorATh)
    axRaster.set_title('ATh -> Str Example 1')
    axRate.set_xlim([0,200])
# ax = plt.gc
# ax.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')

# -- Panel: Thalamus less synchronized --
# axWide = plt.subplot(gs[0, 1])
spec = gs[0, 1]
# axWide.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[1]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'Thal2', color=colorATh)
    axRaster.set_title('ATh -> Str Example 2')
    axRate.set_xlim([0,20])

spec = gs[1, 0]
# axSharp.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[2]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'AC1', color=colorAC)
    axRaster.set_title('AC -> Str Example 1')
# -- Panel: Cortex less synchronized --
# axWide = plt.subplot(gs[1, 1])
spec = gs[1, 1]
# axWide.annotate('E', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
#              fontsize=fontSizePanel, fontweight='bold')
if PANELS[3]:
    (axRaster, axRate) = plot_example_with_rate(spec, 'AC2', color=colorAC)
    axRaster.set_title('AC -> Str Example 2')
