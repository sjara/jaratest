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
reload(extraplots)

import figparams
reload(figparams)


FIGNAME = 'figure_PV_SOM_suppression'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'PV_SOM_suppression' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [9,8] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.32, 0.65]   # Horiz position for panel labels
labelPosY = [0.96, 0.65, 0.36]    # Vert position for panel labels

#PVFileName = 'band026_2017-04-27_1350um_T4_c2.npz'
PVFileName = 'band026_2017-04-27_1410um_T4_c6.npz'

#SOMFileName = 'band028_2017-05-21_1450um_T2_c4.npz'
SOMFileName = 'band028_2017-05-21_1625um_T6_c6.npz'
#SOMFileName = 'band031_2017-06-29_1280um_T1_c4.npz'

summaryFileName = 'photoidentified_cells_suppression_scores.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3,3,width_ratios=[1,1.3,1.3],height_ratios=[1,1,1.5])
gs.update(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.4, hspace=0.6)

# gs0 = gridspec.GridSpec(2,3,width_ratios=[1, 1.3, 1.3])
# gs0.update(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.4, hspace=0.3)

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
    
    axRaster.set_xticklabels('')
    axRaster.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    extraplots.boxoff(axRaster)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.title('PV')

    
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
    axRaster.annotate('D', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    plt.setp(pRaster, ms=3, color='k')
    extraplots.boxoff(axRaster)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    plt.title('SOM')

# -- Plots of onset and sustained bandwidth tuning --
if PANELS[1]:
    # PV response
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVonsetResponseArray = PVData['onsetResponseArray']
    PVonsetSTD = PVData['onsetSTD']
    PVsustainedResponseArray = PVData['sustainedResponseArray']
    PVsustainedSTD = PVData['sustainedSTD']
    PVbaseline = PVData['baselineMean']
    
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMonsetResponseArray = SOMData['onsetResponseArray']
    SOMonsetSTD = SOMData['onsetSTD']
    SOMsustainedResponseArray = SOMData['sustainedResponseArray']
    SOMsustainedSTD = SOMData['sustainedSTD']
    SOMbaseline = SOMData['baselineMean']

    bands = PVData['possibleBands']
    
    onsetResponses = [PVonsetResponseArray, SOMonsetResponseArray]
    onsetSTDs = [PVonsetSTD, SOMonsetSTD]
    
    sustainedResponses = [PVsustainedResponseArray, SOMsustainedResponseArray]
    sustainedSTDs = [PVsustainedSTD, SOMsustainedSTD]
    
    responses = [onsetResponses, sustainedResponses]
    SEMs = [onsetSTDs, sustainedSTDs]
    baselineRates = [PVbaseline, SOMbaseline]
    
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor]
    panelLabels = [['B', 'E'], ['C', 'F']]
    
    for ind, responseType in enumerate(responses):
        for ind2, responseByCell in enumerate(responseType):
            plt.hold(1)
            axCurve = plt.subplot(gs[ind2,ind+1])
            plt.plot(range(len(bands)), responseByCell, '-o', ms=7, lw=3,
                     color=cellTypeColours[ind2], mec=cellTypeColours[ind2], clip_on=False)
            plt.fill_between(range(len(bands)), responseByCell - SEMs[ind][ind2], 
                             responseByCell + SEMs[ind][ind2], alpha=0.2, color=cellTypeColours[ind2], edgecolor='none')
            plt.plot(range(len(bands)), np.tile(baselineRates[ind2], len(bands)), '--', color='0.4', lw=2)
            axCurve.annotate(panelLabels[ind][ind2], xy=(labelPosX[ind+1],labelPosY[ind2]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
            axCurve.set_xticklabels('')
            axCurve.set_ylim(bottom=0)
            yLims = np.array(plt.ylim())
            axCurve.set_ylim(top=yLims[1]*1.3)
            extraplots.boxoff(axCurve)
            extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
            if not (ind | ind2):
                plt.title('Onset responses',fontsize=fontSizeLabels,fontweight='normal')
            if ind and not ind2:
                plt.title('Sustained responses',fontsize=fontSizeLabels,fontweight='normal')
            if ind2:
                axCurve.set_xticklabels(bands)
                plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
            if not ind:
                plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
                

# gs1 = gridspec.GridSpec(1,2)
# gs1.update(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.4, hspace=0.3)

# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for onset and sustained responses --    
if PANELS[2]:
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
    
    categoryLabels = ['PV', 'SOM', 'Ex.']
    
    panelLabels = ['G', 'H']
    
    yLabels = ['Onset Suppression Index', 'Sustained Suppression Index']
    
    for ind, vals in enumerate(suppressionVals):
        axScatter = plt.subplot(gs[2,ind+1])
        plt.hold(1)
        for category in range(len(vals)):
            edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
            xval = (category+1)*np.ones(len(vals[category]))
            
            jitterAmt = np.random.random(len(xval))
            xval = xval + (0.4 * jitterAmt) - 0.2
            
            plt.plot(xval, vals[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
            median = np.median(vals[category])
            #sem = stats.sem(vals[category])
            plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
            plt.ylabel(yLabels[ind],fontsize=fontSizeLabels)
        axScatter.annotate(panelLabels[ind], xy=(labelPosX[ind+1],labelPosY[2]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        plt.xlim(0,len(vals)+1)
        plt.ylim(0,1)
        axScatter.set_xticks(range(1,len(vals)+1))
        axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
        extraplots.boxoff(axScatter)
        yLims = np.array(plt.ylim())
        if ind==0:
            extraplots.new_significance_stars([1,2], yLims[1]*1.1, yLims[1]*0.04, starMarker='p=0.40', gapFactor=0.4, color='0.5')
            extraplots.new_significance_stars([2,3], yLims[1]*1.1, yLims[1]*0.04, starMarker='p=0.82', gapFactor=0.4, color='0.5')
            extraplots.new_significance_stars([1,3], yLims[1]*1.18, yLims[1]*0.04, starMarker='p=0.06', gapFactor=0.2, color='0.5')
        if ind==1:
            extraplots.new_significance_stars([1,2], yLims[1]*1.1, yLims[1]*0.04, starMarker='p=0.82', gapFactor=0.4, color='0.5')
            extraplots.new_significance_stars([2,3], yLims[1]*1.1, yLims[1]*0.04, starMarker='p=0.09', gapFactor=0.4, color='0.5')
            extraplots.new_significance_stars([1,3], yLims[1]*1.18, yLims[1]*0.04, starMarker='p=0.03', gapFactor=0.2, color='0.5')
        plt.hold(0)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)