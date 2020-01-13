''' 
Create figure showing frequency tuning of example surround suppressed excitatory cell, as well as demonstrating
how the characteristic frequency is estimated. Also shows effect of preferred frequency on suppression.
'''
import os
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams



FIGNAME = 'supplement_figure_gaussian_frequency_tuning_fit'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig3_frequency_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [6,6] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

ExColor = figparams.colp['excitatoryCell']
PVColor = figparams.colp['PVcell']
SOMColor = figparams.colp['SOMcell']

soundColor = figparams.colp['sound']

labelPosX = [0.01, 0.55]   # Horiz position for panel labels
labelPosY = [0.97, 0.44]    # Vert position for panel labels

ExampleFileName = 'band016_2016-12-11_950um_T6_c6.npz'
#ExampleFileName = 'band029_2017-05-25_1240um_T2_c2.npz'
#ExampleFileName = 'band031_2017-06-29_1140um_T1_c3.npz'
#ExampleFileName = 'band044_2018-01-16_975um_T7_c4.npz'
#ExampleFileName = 'band060_2018-04-02_1275um_T4_c2.npz'

toneSupFileName = 'pure_tone_suppression_stats.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2, 2, height_ratios=[1.0, 0.8], width_ratios=[1.0,0.8])
gs.update(top=0.97, bottom=0.11, left=0.11, right=0.98, wspace=0.4, hspace=0.4)

# --- Raster of frequency tuning ---
if PANELS[0]:
    ExampleFile = 'example_frequency_tuning_'+ExampleFileName
    ExampleDataFullPath = os.path.join(dataDir,ExampleFile)
    ExampleData = np.load(ExampleDataFullPath)
    
    panelLabel = 'A'
    
    axRaster = plt.subplot(gs[0,0])
    plt.cla()
    spikeTimesFromEventOnset = ExampleData['spikeTimesFromEventOnset']
    indexLimitsEachTrial = ExampleData['indexLimitsEachTrial']
    rasterTimeRange = ExampleData['rasterTimeRange']
    trialsEachCond = ExampleData['trialsEachCond']
    possibleFreqs = ExampleData['possibleFreqs']
    labels = ['%.1f' % f for f in possibleFreqs/1000]
    labels[1::2] = ['']*len(labels[1::2])
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,rasterTimeRange,
                                                   trialsEachCond=trialsEachCond,labels=labels)
    axRaster.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    plt.locator_params(axis='x', nbins=5)
    extraplots.boxoff(axRaster)
    plt.ylabel('Frequency (kHz)',fontsize=fontSizeLabels) 
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    
    yLims = np.array(plt.ylim())
    rect = patches.Rectangle((0,yLims[1]*1.02),0.1,yLims[1]*0.03,linewidth=1,edgecolor=soundColor,facecolor=soundColor,clip_on=False)
    axRaster.add_patch(rect)

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
    
    cellColour = figparams.colp['excitatoryCell']
    fitColour = figparams.colp['excitatoryCell']
    
    panelLabel = 'B'
    
    plt.hold(True)
    axCurve = plt.subplot(gs[1,0])
    l1,=plt.plot(np.log2(possibleFreqs), responseArray, 'o', ms=5,
             color=cellColour, mec=cellColour, clip_on=False, zorder=4)
    plt.errorbar(np.log2(possibleFreqs), responseArray, yerr = [SEM, SEM], 
                 fmt='none', ecolor=cellColour, zorder=3)

    l3,=plt.plot([fitFreqs[0],fitFreqs[-1]], np.tile(baselineSpikeRate, 2), '--', color='0.5', lw=1.5, zorder=1)
    l2,=plt.plot(fitFreqs, fitResponse, '-', lw=1.5, color=fitColour, zorder=2)
    axCurve.annotate(panelLabel, xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    labels = ['%.1f' % f for f in possibleFreqs/1000]
    labels[1::3] = ['']*len(labels[1::3])
    labels[2::3] = ['']*len(labels[2::3])
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
    
    xValsPointer = [np.log2(prefFreq)-0.5,np.log2(prefFreq)-0.5,
                    np.log2(prefFreq)+0.5,np.log2(prefFreq)+0.5]
    yValsPointer = [yLims[1]*0.92, yLims[1]*0.96, yLims[1]*0.96, yLims[1]*0.92]
    axCurve.plot(xValsPointer,yValsPointer,color='k')

    axCurve.annotate('1 octave', xy=(np.log2(prefFreq)-0.6,yLims[1]*0.98), xycoords='data', fontsize=fontSizeLabels)
    
# --- suppression indices for cells of different preferred frequencies ---
if PANELS[2]:
    dataFullPath = os.path.join(dataDir,toneSupFileName)
    data = np.load(dataFullPath)
    
    axScatter = plt.subplot(gs[:,1])
    
    SIs = data['ExcCellSIs']
    pVals = data['toneSuppPVal']
    
    panelLabel = 'C'
    sigSIs = SIs[pVals<0.05]
    notSigSIs = SIs[pVals>=0.05]

    for ind, category in enumerate([sigSIs, notSigSIs]):
        xval = (ind+1)*np.ones(len(category))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.hold(True)
        plt.plot(xval, category, 'o', mfc='none', clip_on=False)
        median = np.median(category)
        #sem = stats.sem(vals[category])
        plt.plot([ind+0.7,ind+1.3], [median,median], '-', color='k', lw=3)

    plt.xlim(0,3)
    plt.ylim(-0.05,1.05)
    plt.ylabel('Suppression Index')
    axScatter.set_xticks(range(1,3))
    axScatter.set_xticklabels([r'$<$0.05', r'$\geq$0.05'])
    plt.xlabel('Suppression by pure \ntone (p value)')
    extraplots.boxoff(axScatter)
    
    axCurve.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    pVal = stats.ranksums(sigSIs, notSigSIs)[1]
    print "tone suppressed vs not suppressed SI p val: {}".format(pVal)
    
    pVal = stats.ranksums(SIs, notSigSIs)[1]
    print "not suppressed vs all SI p val: {}".format(pVal)
    

    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)