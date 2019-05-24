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
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

PANELS = [1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig2_gaussian_frequency_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [8,8] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.47]   # Horiz position for panel labels
labelPosY = [0.96, 0.51]    # Vert position for panel labels

ExampleFileName = 'band016_2016-12-11_950um_T6_c6.npz'
#ExampleFileName = 'band029_2017-05-25_1240um_T2_c2.npz'
#ExampleFileName = 'band031_2017-06-29_1140um_T1_c3.npz'
#ExampleFileName = 'band044_2018-01-16_975um_T7_c4.npz'
#ExampleFileName = 'band060_2018-04-02_1275um_T4_c2.npz'

statsFileName = 'all_photoidentified_cells_stats_by_best_freq.npz'

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,2,height_ratios=[0.8,1], width_ratios=[0.8,1])
gs.update(top=0.96, bottom=0.08, left=0.1, right=0.96, wspace=0.3, hspace=0.3)

# --- Raster of frequency tuning ---
if PANELS[0]:
    ExampleFile = 'example_frequency_tuning_'+ExampleFileName
    ExampleDataFullPath = os.path.join(dataDir,ExampleFile)
    ExampleData = np.load(ExampleDataFullPath)
    
    panelLabel = 'a'
    
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
    axRaster.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    plt.locator_params(axis='x', nbins=5)
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
    
    cellColour = figparams.colp['excitatoryCell']
    fitColour = figparams.colp['excitatoryCell']
    
    panelLabel = 'b'
    
    plt.hold(True)
    axCurve = plt.subplot(gs[0,1])
    l1,=plt.plot(np.log2(possibleFreqs), responseArray, 'o', ms=5,
             color=cellColour, mec=cellColour, clip_on=False, zorder=4)
    plt.errorbar(np.log2(possibleFreqs), responseArray, yerr = [SEM, SEM], 
                 fmt='none', ecolor=cellColour, zorder=3)

    l3,=plt.plot([fitFreqs[0],fitFreqs[-1]], np.tile(baselineSpikeRate, 2), '--', color='0.5', lw=1.5, zorder=1)
    l2,=plt.plot(fitFreqs, fitResponse, '-', lw=1.5, color=fitColour, zorder=2)
    axCurve.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    labels = ['%.1f' % f for f in possibleFreqs/1000]
    labels[1::3] = ['']*len(labels[1::3])
    labels[2::3] = ['']*len(labels[2::3])
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
    
    xValsPointer = [np.log2(prefFreq)-0.5,np.log2(prefFreq)-0.5,
                    np.log2(prefFreq)+0.5,np.log2(prefFreq)+0.5]
    yValsPointer = [yLims[1]*0.92, yLims[1]*0.96, yLims[1]*0.96, yLims[1]*0.92]
    axCurve.plot(xValsPointer,yValsPointer,color='k')
    
#     rect = patches.Rectangle((np.log2(prefFreq)-0.5,yLims[1]*0.93),1,yLims[1]*0.05,linewidth=1,edgecolor='0.5',facecolor='0.5',clip_on=False)
#     axCurve.add_patch(rect)
    axCurve.annotate('1 octave', xy=(np.log2(prefFreq)-0.5,yLims[1]*0.98), xycoords='data',
                     fontsize=fontSizeLabels)
    
#     rect2 = patches.Rectangle((np.log2(prefFreq)-2,yLims[1]),4,yLims[1]*0.05,linewidth=1,edgecolor='0.5',facecolor='0.5',clip_on=False)
#     axCurve.add_patch(rect2)
#     axCurve.annotate('4 octaves', xy=(np.log2(prefFreq)-0.5,yLims[1]*1.01), xycoords='data',
#                      fontsize=fontSizeLabels, clip_on=False)

# --- distribution of preferred frequencies for recorded cells ---
if PANELS[2]:
    dataFullPath = os.path.join(dataDir,statsFileName)
    data = np.load(dataFullPath)
    
    axHist = gs[1,0]
    
    panelLabel = 'c'

    ExbestFreq = data['ExbestFreq']
    PVbestFreq = data['PVbestFreq']
    SOMbestFreq = data['SOMbestFreq']
    
    ExColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    freqs = [np.log2(ExbestFreq), np.log2(PVbestFreq), np.log2(SOMbestFreq)]
    colours = [ExColor, PVColor, SOMColor]
    bins = np.log2(possibleFreqs)
    
    panelTitles = ['Exc.', 'PV', 'SOM']
    
    cellLabelPosX = 0.13
    cellLabelPosY = [0.46, 0.29, 0.14]
    
    inner = gridspec.GridSpecFromSubplotSpec(len(freqs), 1, subplot_spec=axHist, wspace=0.1, hspace=0.3)
    for ind, thisFreqs in enumerate(freqs):
        thisAx = plt.subplot(inner[ind])
        plt.hist(thisFreqs, bins=bins, color=colours[ind], edgecolor=colours[ind])
        thisAx.set_xticks(bins)
        thisAx.set_xticklabels(labels)
        plt.xlim(bins[0]-0.2, bins[-1]+0.1)
        plt.locator_params(axis='y', nbins=4)
        extraplots.boxoff(thisAx)
        plt.ylabel('Cell count',fontsize=fontSizeLabels) 
        
        if ind != 2:
            thisAx.set_xticklabels('')
            
        thisAx.annotate(panelTitles[ind], xy=(cellLabelPosX,cellLabelPosY[ind]), xycoords='figure fraction',
                         fontsize=fontSizeLabels)
            
    thisAx.annotate(panelLabel, xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    plt.xlabel('Frequency (kHz)',fontsize=fontSizeLabels)
    
# --- suppression indices for cells of different preferred frequencies ---
if PANELS[3]:
    dataFullPath = os.path.join(dataDir,statsFileName)
    data = np.load(dataFullPath)
    
    axScatter = plt.subplot(gs[1,1])
    
    panelLabel = 'd'
    
    ExbestFreq = data['ExbestFreq']
    PVbestFreq = data['PVbestFreq']
    SOMbestFreq = data['SOMbestFreq']
    
    ExSI = data['fitExcSustainedSuppressionInd']
    PVSI = data['fitPVsustainedSuppressionInd']
    SOMSI = data['fitSOMsustainedSuppressionInd']
    
    cellTypeLabels = ['Exc.', 'PV', 'SOM']
    
    cellFreqs = [ExbestFreq, PVbestFreq, SOMbestFreq]
    cellSIs = [ExSI, PVSI, SOMSI]
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    bar_width = 0.15
    bar_spacing = 0.15
    bar_loc = [-1,0,1]
    
    allxvals = []
    
    for cellType in range(len(cellFreqs)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[cellType], alpha=0.6)
        thisCellTypeSIs = cellSIs[cellType]
        thisCellTypePrefFreqs = cellFreqs[cellType]
        
        SIsLowFreq = thisCellTypeSIs[np.where(thisCellTypePrefFreqs<7000)[0]]
        SIsMidFreq = thisCellTypeSIs[np.where(np.logical_and(thisCellTypePrefFreqs>=7000,thisCellTypePrefFreqs<17000))[0]]
        SIsHighFreq = thisCellTypeSIs[np.where(thisCellTypePrefFreqs>=17000)[0]]
        
        print "p val for effect of frequency on {} cell SI: {}".format(cellTypeLabels[cellType],stats.f_oneway(SIsLowFreq, SIsMidFreq, SIsHighFreq)[1])
        
        for indSI, SIs in enumerate([SIsLowFreq, SIsMidFreq, SIsHighFreq]):
            xval = (cellType+1)+(bar_loc[indSI]*(bar_width+bar_spacing))
            allxvals.append(xval)
            xvals = xval*np.ones(len(SIs))
              
            jitterAmt = np.random.random(len(xvals))
            xvals = xvals + (bar_width * jitterAmt) - bar_width/2
              
            plt.hold(True)
            plt.plot(xvals, SIs, 'o', mec=edgeColour, mfc='none', clip_on=False)
            median = np.median(SIs)
            plt.plot([xval-bar_width/2,xval+bar_width/2], [median,median], '-', color='k', mec=edgeColour, lw=3)
            
    ExPatch = patches.Patch(color=ExColor, label='Exc.')
    PVPatch = patches.Patch(color=PVColor, label='PV')
    SOMPatch = patches.Patch(color=SOMColor, label='SOM')
    plt.legend(handles=[ExPatch,PVPatch,SOMPatch],frameon=False, fontsize=fontSizeLabels, loc='best')
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    plt.ylim(-0.1,1.1)
    plt.ylabel('Suppression Index')
    plt.xlabel('Preferred frequency (kHz)')
    axScatter.set_xticks(allxvals)
    axScatter.set_xticklabels(np.tile(['L','M','H'],len(cellFreqs)))
    extraplots.boxoff(axScatter)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)