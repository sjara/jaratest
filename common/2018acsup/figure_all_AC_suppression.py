''' 
Create figure showing bandwidth tuning of an example cell as well as a summary of suppression indices for all cells collected.

Bandwidth tuning: 30 trials each bandwidth, sound 1 sec long, average iti 1.5 seconds
Center frequency determined with shortened tuning curve (16 freq, best frequency as estimated by gaussian fit)
AM rate selected as one eliciting highest sustained spike
'''
import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams


FIGNAME = 'figure_all_AC_suppression'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'all_AC_suppression' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [9,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.40, 0.72]   # Horiz position for panel labels
labelPosY = [0.9, 0.48]    # Vert position for panel labels

cellFileName = 'band031_2017-06-29_1280um_T1_c3.npz'
#cellFileName = 'band044_2018-01-16_975um_T7_c4.npz' # another option for an example cell

summaryFileName = 'all_cells_suppression_scores.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


gs = gridspec.GridSpec(2,3,width_ratios=[3, 2.2, 1.5])
gs.update(top=0.9, left=0.07, right=0.95, wspace=0.4, hspace=0.2)

# --- Raster plot of example cell ---
if PANELS[0]:
    exampleFilename = 'example_AC_bandwidth_tuning_'+cellFileName
    exampleDataFullPath = os.path.join(dataDir,exampleFilename)
    exampleData = np.load(exampleDataFullPath)
    
    axRaster = plt.subplot(gs[0:,0])
    plt.cla()
    bandSpikeTimesFromEventOnset = exampleData['spikeTimesFromEventOnset']
    bandIndexLimitsEachTrial = exampleData['indexLimitsEachTrial']
    bandTimeRange = exampleData['timeRange']
    trialsEachCond = exampleData['trialsEachCond']
    possibleBands = exampleData['possibleBands']
    bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
    pRaster, hcond, zline = extraplots.raster_plot(bandSpikeTimesFromEventOnset,bandIndexLimitsEachTrial,bandTimeRange,
                                                   trialsEachCond=trialsEachCond,labels=bandLabels)
    
    # plot bars indicating time range taken for onset and sustained responses
    yLims = np.array(plt.ylim())
    soundBarBottom = 1.05*yLims[1]
    soundBarTop = soundBarBottom + 0.02*(yLims[1]-yLims[0])
    plt.hold(1)
    onsetTimeRange = exampleData['onsetTimeRange']
    plt.fill([onsetTimeRange[0],onsetTimeRange[1],onsetTimeRange[1],onsetTimeRange[0]],[soundBarBottom,soundBarBottom,soundBarTop,soundBarTop],
             fc='r', ec='none', clip_on=False)
    
    sustainedTimeRange = exampleData['sustainedTimeRange']
    plt.fill([sustainedTimeRange[0],sustainedTimeRange[1],sustainedTimeRange[1],sustainedTimeRange[0]],[soundBarBottom,soundBarBottom,soundBarTop,soundBarTop],
             fc='r', ec='none', clip_on=False)
    plt.hold(0)
    
    axRaster.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    extraplots.boxoff(axRaster)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.xlabel('Time from laser onset (s)',fontsize=fontSizeLabels)

    

# -- Plots of onset and sustained bandwidth tuning --
if PANELS[1]:
    exampleFilename = 'example_AC_bandwidth_tuning_'+cellFileName
    exampleDataFullPath = os.path.join(dataDir,exampleFilename)
    exampleData = np.load(exampleDataFullPath)
    
    onsetResponseArray = exampleData['onsetResponseArray']
    onsetSEM = exampleData['onsetSEM']
    bands = exampleData['possibleBands']
    axCurve = plt.subplot(gs[0,1])
    plt.plot(range(len(bands)), onsetResponseArray, '-o', ms=7, lw=3,
             color='k', mec='k', clip_on=False)
    plt.fill_between(range(len(bands)), onsetResponseArray - onsetSEM, 
                     onsetResponseArray + onsetSEM, alpha=0.2, color='0.5', edgecolor='none')
    axCurve.annotate('B', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axCurve.set_xticklabels('')
    axCurve.set_ylim(bottom=0)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    #plt.title('Onset response',fontsize=fontSizeLabels,fontweight='normal')
    
    sustainedResponseArray = exampleData['sustainedResponseArray']
    sustainedSEM = exampleData['sustainedSEM']
    axCurve = plt.subplot(gs[1,1])
    plt.plot(range(len(bands)), sustainedResponseArray, '-o', ms=7, lw=3,
             color='k', mec='k', clip_on=False)
    plt.fill_between(range(len(bands)), sustainedResponseArray - sustainedSEM, 
                     sustainedResponseArray + sustainedSEM, alpha=0.2, color='0.5', edgecolor='none')
    axCurve.annotate('C', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axCurve.set_xticklabels(bands)
    axCurve.set_ylim(bottom=0)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    axCurve.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    #plt.title('Sustained response',fontsize=fontSizeLabels,fontweight='normal')
    
    xLims = plt.xlim(); yLims = plt.ylim()
    plt.xlim(xLims); plt.ylim(yLims)
    
# -- Summary of suppression scores for all recorded cells --
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    axHist = plt.subplot(gs[0,2])
    onsetSuppressionIndices = summaryData['allOnsetSuppression']
    bins = np.linspace(0, 1, 50)
    plt.hist(onsetSuppressionIndices, bins, alpha=0.7, color='k', lw=3)
    axHist.annotate('D', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axHist)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    axHist.set_xticklabels('')
    #plt.title('Onset suppression',fontsize=fontSizeLabels,fontweight='normal')
    
    axHist = plt.subplot(gs[1,2])
    sustainedSuppressionIndices = summaryData['allSustainedSuppression']
    plt.hist(sustainedSuppressionIndices, bins, alpha=0.7, color='k', lw=3)
    axHist.annotate('E', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axHist)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    axHist.set_xlabel('Suppression Index',fontsize=fontSizeLabels)
    #plt.title('Sustained suppression',fontsize=fontSizeLabels,fontweight='normal')
            
#plt.show()



if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)