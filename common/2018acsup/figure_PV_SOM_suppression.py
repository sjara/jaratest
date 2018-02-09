''' 
Create figure showing bandwidth tuning of an example PV and SOM cell as well as a summary of suppression indices,
comparing SOM to PV to excitatory.

Bandwidth tuning: 30 trials each bandwidth, sound 1 sec long, average iti 1.5 seconds
Center frequency determined with shortened tuning curve (16 freq, best frequency as estimated by gaussian fit)
AM rate selected as one eliciting highest sustained spike
'''
import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
reload(figparams)


FIGNAME = 'figure_PV_SOM_suppression'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'PV_SOM_suppression' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [9,5] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.40, 0.72, 0.9]   # Horiz position for panel labels
labelPosY = [0.9, 0.48]    # Vert position for panel labels

PVFileName = 'band026_2017-04-27_1350um_T4_c2.npz'
#PVFileName = 'band026_2017-04-27_1410um_T4_c6.npz'

#SOMFileName = 'band028_2017-05-21_1450um_T2_c4.npz'
#SOMFileName = 'band028_2017-05-21_1625um_T6_c6.npz'
SOMFileName = 'band031_2017-06-29_1280um_T1_c4.npz'

summaryFileName = 'photoidentified_cells_suppression_scores.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


gs = gridspec.GridSpec(2,4,width_ratios=[1, 0.7, 0.7, 1.5])
gs.update(top=0.9, left=0.07, right=0.95, wspace=0.4, hspace=0.2)

# --- Raster plots of example PV and SOM cell ---
if PANELS[0]:
    # PV cell
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    axRaster = plt.subplot(gs[0,0])
    plt.cla()
    bandSpikeTimesFromEventOnset = PVData['spikeTimesFromEventOnset']
    bandIndexLimitsEachTrial = PVData['indexLimitsEachTrial']
    bandTimeRange = PVData['timeRange']
    trialsEachCond = PVData['trialsEachCond']
    possibleBands = PVData['possibleBands']
    bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
    pRaster, hcond, zline = extraplots.raster_plot(bandSpikeTimesFromEventOnset,bandIndexLimitsEachTrial,bandTimeRange,
                                                   trialsEachCond=trialsEachCond,labels=bandLabels)
    
    axRaster.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    extraplots.boxoff(axRaster)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)

    
    # SOM cell
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    axRaster = plt.subplot(gs[1,0])
    plt.cla()
    bandSpikeTimesFromEventOnset = SOMData['spikeTimesFromEventOnset']
    bandIndexLimitsEachTrial = SOMData['indexLimitsEachTrial']
    bandTimeRange = SOMData['timeRange']
    trialsEachCond = SOMData['trialsEachCond']
    possibleBands = SOMData['possibleBands']
    bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
    pRaster, hcond, zline = extraplots.raster_plot(bandSpikeTimesFromEventOnset,bandIndexLimitsEachTrial,bandTimeRange,
                                                   trialsEachCond=trialsEachCond,labels=bandLabels)
    axRaster.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    extraplots.boxoff(axRaster)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.xlabel('Time from laser onset (s)',fontsize=fontSizeLabels)

# -- Plots of onset bandwidth tuning --
if PANELS[1]:
    # PV response
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVonsetResponseArray = PVData['onsetResponseArray']
    PVonsetSEM = PVData['onsetSEM']
    bands = PVData['possibleBands']
    axCurve = plt.subplot(gs[0,1])
    plt.plot(range(len(bands)), PVonsetResponseArray, '-o', ms=7, lw=3,
             color='k', mec='k', clip_on=False)
    plt.fill_between(range(len(bands)), PVonsetResponseArray - PVonsetSEM, 
                     PVonsetResponseArray + PVonsetSEM, alpha=0.2, color='0.5', edgecolor='none')
    axCurve.annotate('C', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axCurve.set_xticklabels('')
    axCurve.set_ylim(bottom=0)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.title('Onset responses',fontsize=fontSizeLabels,fontweight='normal')
    
    # SOM response
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMonsetResponseArray = SOMData['onsetResponseArray']
    SOMonsetSEM = SOMData['onsetSEM']
    bands = SOMData['possibleBands']
    axCurve = plt.subplot(gs[1,1])
    plt.plot(range(len(bands)), SOMonsetResponseArray, '-o', ms=7, lw=3,
             color='k', mec='k', clip_on=False)
    plt.fill_between(range(len(bands)), SOMonsetResponseArray - SOMonsetSEM, 
                     SOMonsetResponseArray + SOMonsetSEM, alpha=0.2, color='0.5', edgecolor='none')
    axCurve.annotate('D', xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axCurve.set_xticklabels(bands)
    axCurve.set_ylim(bottom=0)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    axCurve.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    
# -- Plots of sustained bandwidth tuning --
if PANELS[2]:
    # PV response
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVsustainedResponseArray = PVData['sustainedResponseArray']
    PVsustainedSEM = PVData['sustainedSEM']
    bands = PVData['possibleBands']
    axCurve = plt.subplot(gs[0,2])
    plt.plot(range(len(bands)), PVsustainedResponseArray, '-o', ms=7, lw=3,
             color='k', mec='k', clip_on=False)
    plt.fill_between(range(len(bands)), PVsustainedResponseArray - PVsustainedSEM, 
                     PVsustainedResponseArray + PVsustainedSEM, alpha=0.2, color='0.5', edgecolor='none')
    axCurve.annotate('E', xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axCurve.set_xticklabels('')
    axCurve.set_ylim(bottom=0)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.title('Sustained responses',fontsize=fontSizeLabels,fontweight='normal')
    
    # SOM response
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMsustainedResponseArray = SOMData['sustainedResponseArray']
    SOMsustainedSEM = SOMData['sustainedSEM']
    bands = SOMData['possibleBands']
    axCurve = plt.subplot(gs[1,2])
    plt.plot(range(len(bands)), SOMsustainedResponseArray, '-o', ms=7, lw=3,
             color='k', mec='k', clip_on=False)
    plt.fill_between(range(len(bands)), SOMsustainedResponseArray - SOMsustainedSEM, 
                     SOMsustainedResponseArray + SOMsustainedSEM, alpha=0.2, color='0.5', edgecolor='none')
    axCurve.annotate('F', xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    axCurve.set_xticklabels(bands)
    axCurve.set_ylim(bottom=0)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    axCurve.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    extraplots.boxoff(axCurve)

# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for onset and sustained responses --    
if PANELS[3]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVonsetSuppression = summaryData['PVonsetSuppression']
    SOMonsetSuppression = summaryData['SOMonsetSuppression']
    AConsetSuppression = summaryData['nonSOMonsetSuppression']
    
    onsetSuppressionVals = [PVonsetSuppression, SOMonsetSuppression, AConsetSuppression]
    
    PVsustainedSuppression = summaryData['PVsustainedSuppression']
    SOMsustainedSuppression = summaryData['SOMsustainedSuppression']
    ACsustainedSuppression = summaryData['nonSOMsustainedSuppression']
    
    sustainedSuppressionVals = [PVsustainedSuppression, SOMsustainedSuppression, ACsustainedSuppression]
    
    suppressionVals = [onsetSuppressionVals, sustainedSuppressionVals]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor, excitatoryColor]
    
    categoryLabels = ['PV', 'SOM', 'excitatory']
    
    for ind, vals in enumerate(suppressionVals):
        axScatter = plt.subplot(gs[ind,3])
        plt.hold(1)
        for category in range(len(vals)):
            edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
            xval = (category+1)*np.ones(len(vals[category]))
            
            jitterAmt = np.random.random(len(xval))
            xval = xval + (0.3 * jitterAmt) - 0.15
            
            plt.plot(xval, vals[category], 'o', mec=edgeColour, mfc='none')
            median = np.median(vals[category])
            #sem = stats.sem(vals[category])
            plt.plot([category+0.85,category+1.15], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
    
        plt.xlim(0,len(vals)+1)
        plt.ylim(0,1)
        ax = plt.gca()
        ax.set_xticks(range(1,len(vals)+1))
        ax.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
        plt.hold(0)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)