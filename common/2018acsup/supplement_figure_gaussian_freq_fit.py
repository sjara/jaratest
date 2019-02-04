''' 
Create figure showing frequency tuning of example surround suppressed excitatory cell, as well as demonstrating
how the characteristic frequency is estimated.
'''
import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)



FIGNAME = 'supplement_figure_gaussian_frequency_tuning_fit'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

PANELS = [1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
#outputDir = '/tmp/'
outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'gaussian_frequency_tuning' # Do not include extension
#figFormat = 'pdf' # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [8,4] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.52]   # Horiz position for panel labels
labelPosY = [0.94]    # Vert position for panel labels

ExampleFileName = 'band016_2016-12-11_950um_T6_c6.npz'
#ExampleFileName = 'band029_2017-05-25_1240um_T2_c2.npz'
#ExampleFileName = 'band031_2017-06-29_1140um_T1_c3.npz'
#ExampleFileName = 'band044_2018-01-16_975um_T7_c4.npz'
#ExampleFileName = 'band060_2018-04-02_1275um_T4_c2.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2,width_ratios=[1,1])
gs.update(top=0.95, bottom=0.12, left=0.1, right=0.98, wspace=0.25, hspace=0.2)

# --- Raster of frequency tuning ---
if PANELS[0]:
    ExampleFile = 'example_frequency_tuning_'+ExampleFileName
    ExampleDataFullPath = os.path.join(dataDir,ExampleFile)
    ExampleData = np.load(ExampleDataFullPath)
    
    axRaster = plt.subplot(gs[0,0])
    plt.cla()
    spikeTimesFromEventOnset = ExampleData['spikeTimesFromEventOnset']
    indexLimitsEachTrial = ExampleData['indexLimitsEachTrial']
    rasterTimeRange = ExampleData['rasterTimeRange']
    trialsEachCond = ExampleData['trialsEachCond']
    possibleFreqs = ExampleData['possibleFreqs']
    labels = ['%.1f' % f for f in possibleFreqs/1000]
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,rasterTimeRange,
                                                   trialsEachCond=trialsEachCond,labels=labels)
    axRaster.annotate('a', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    extraplots.boxoff(axRaster)
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels) 
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)

# --- gaussian fit tuning curve with different bandwidths indicated ---        
if PANELS[1]:
    ExampleFile = 'example_frequency_tuning_'+ExampleFileName
    ExampleDataFullPath = os.path.join(dataDir,ExampleFile)
    ExampleData = np.load(ExampleDataFullPath)
    
    responseArray = ExampleData['responseArray']
    SEM = ExampleData['SEM']
    possibleFreqs = ExampleData['possibleFreqs']
    baselineSpikeRate = ExampleData['baselineSpikeRate']
    
    fitFreqs = ExampleData['fitXVals']
    fitResponse = ExampleData['fitResponse']
    
    prefFreq = ExampleData['prefFreq']
    
    cellColour = 'k'
    fitColour = figparams.colp['SOMcell']
    
    plt.hold(True)
    axCurve = plt.subplot(gs[0,1])
    l1,=plt.plot(np.log2(possibleFreqs), responseArray, 'o', ms=5,
             color=cellColour, mec=cellColour, clip_on=False, zorder=4)
    plt.errorbar(np.log2(possibleFreqs), responseArray, yerr = [SEM, SEM], 
                 fmt='none', ecolor=cellColour, zorder=3)

    l3,=plt.plot([fitFreqs[0],fitFreqs[-1]], np.tile(baselineSpikeRate, 2), '--', color='0.5', lw=1.5, zorder=1)
    l2,=plt.plot(fitFreqs, fitResponse, '-', lw=1.5, color=fitColour, zorder=2)
    axCurve.annotate('b', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    labels = ['%.1f' % f for f in possibleFreqs/1000]
    labels[1::2] = ['']*len(labels[1::2])
    #plt.legend([l1,l2,l3], ['data','gaussian fit', 'baseline'], loc='best', fontsize=fontSizeLabels, numpoints=1, handlelength=1)
    axCurve.set_xticks(np.log2(possibleFreqs))
    axCurve.set_xticklabels(labels)
    axCurve.set_ylim(bottom=0)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels) 
    plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)
    plt.xlim(fitFreqs[0]-0.2, fitFreqs[-1]+0.1)
    
    #draw patches indicating some example stimuli
    yLims = np.array(plt.ylim())
    
    rect = patches.Rectangle((np.log2(prefFreq)-0.5,yLims[1]*0.93),1,yLims[1]*0.05,linewidth=1,edgecolor='0.5',facecolor='0.5',clip_on=False)
    axCurve.add_patch(rect)
    axCurve.annotate('1 octave', xy=(np.log2(prefFreq)-0.5,yLims[1]*0.94), xycoords='data',
                     fontsize=fontSizeLabels)
    
    rect2 = patches.Rectangle((np.log2(prefFreq)-2,yLims[1]),4,yLims[1]*0.05,linewidth=1,edgecolor='0.5',facecolor='0.5',clip_on=False)
    axCurve.add_patch(rect2)
    axCurve.annotate('4 octaves', xy=(np.log2(prefFreq)-0.5,yLims[1]*1.01), xycoords='data',
                     fontsize=fontSizeLabels, clip_on=False)


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)