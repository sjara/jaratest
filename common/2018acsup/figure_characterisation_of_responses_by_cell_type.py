''' 
Create figure showing bandwidth tuning of an example Excitatory, PV and SOM cell as well as a summary of suppression indices,
comparing SOM to PV to excitatory.

Bandwidth tuning: 30 trials each bandwidth, sound 1 sec long, average iti 1.5 seconds
Center frequency determined with shortened tuning curve (16 freq, best frequency as estimated by gaussian fit)
AM rate selected as one eliciting highest sustained spike

Using difference of gaussians fit to determine suppression indices and preferred bandwidth.
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



FIGNAME = 'figure_characterisation_of_responses_by_cell_type'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

PANELS = [1,1,1,1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'characterisation_of_suppression' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.21, 0.4, 0.58, 0.76]   # Horiz position for panel labels
labelPosY = [0.96, 0.65, 0.34, 0.5]    # Vert position for panel labels

PVFileName = 'band026_2017-04-26_1470um_T4_c5.npz'
#PVFileName = 'band026_2017-04-27_1350um_T4_c2.npz'
#PVFileName = 'band032_2017-07-21_1200um_T6_c2.npz'
#PVFileName = 'band033_2017-07-27_1700um_T4_c5.npz'

SOMFileName = 'band015_2016-11-12_1000um_T8_c4.npz'
#SOMFileName = 'band029_2017-05-22_1320um_T4_c2.npz'
#SOMFileName = 'band031_2017-06-29_1280um_T1_c4.npz'
#SOMFileName = 'band060_2018-04-04_1225um_T3_c4.npz'

ExcFileName = 'band016_2016-12-11_950um_T6_c6.npz'
#ExcFileName = 'band029_2017-05-25_1240um_T2_c2.npz'
#ExcFileName = 'band031_2017-06-29_1140um_T1_c3.npz'
#ExcFileName = 'band044_2018-01-16_975um_T7_c4.npz'
#ExcFileName = 'band060_2018-04-02_1275um_T4_c2.npz'

summaryFileName = 'all_photoidentified_cells_stats.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(6,5,width_ratios=[1,1.2,1.2,1.3,1.3])
gs.update(top=0.95, bottom=0.08, left=0.1, right=0.95, wspace=0.6, hspace=0.6)

# gs0 = gridspec.GridSpec(2,3,width_ratios=[1, 1.3, 1.3])
# gs0.update(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.4, hspace=0.3)

# --- Raster plots of example PV and SOM cell ---
if PANELS[0]:
    # Excitatory cell
    ExcFile = 'example_Exc_bandwidth_tuning_'+ExcFileName
    ExcDataFullPath = os.path.join(dataDir,ExcFile)
    ExcData = np.load(ExcDataFullPath)
    
    # PV cell
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    # SOM cell
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    cellData = [ExcData, PVData, SOMData]
    panelLabels = ['D', 'F', 'H']
    panelTitles = ['Excitatory', 'PV', 'SOM']
    
    for indCell, cell in enumerate(cellData):
        axRaster = plt.subplot(gs[2*indCell:2*indCell+2,1])
        plt.cla()
        bandSpikeTimesFromEventOnset = cell['spikeTimesFromEventOnset']
        bandIndexLimitsEachTrial = cell['indexLimitsEachTrial']
        rasterTimeRange = cell['rasterTimeRange']
        trialsEachCond = cell['trialsEachCond']
        trialsEachCond = trialsEachCond[:,1:] #don't include pure tone
        possibleBands = cell['possibleBands']
        possibleBands = possibleBands[1:]
        bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
        pRaster, hcond, zline = extraplots.raster_plot(bandSpikeTimesFromEventOnset,bandIndexLimitsEachTrial,rasterTimeRange,
                                                       trialsEachCond=trialsEachCond,labels=bandLabels)
        axRaster.annotate(panelLabels[indCell], xy=(labelPosX[1],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        plt.setp(pRaster, ms=3, color='k')
        extraplots.boxoff(axRaster)
        if indCell != 2:
            axRaster.set_xticklabels('')
        plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.title(panelTitles[indCell])
    
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)
    
    #also do the panel labels for the cartoons in here I guess
    cartoonPanels = ['A', 'B', 'C']
    for indPanel, panel in enumerate(cartoonPanels):
        axRaster.annotate(panel, xy=(labelPosX[0],labelPosY[indPanel]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')



# -- Plots of onset and sustained bandwidth tuning --
if PANELS[1]:
    
    ExcFile = 'example_Exc_bandwidth_tuning_'+ExcFileName
    ExcDataFullPath = os.path.join(dataDir,ExcFile)
    ExcData = np.load(ExcDataFullPath)
    
    ExcSustainedResponseArray = ExcData['sustainedResponseArray']
    ExcSustainedError = ExcData['sustainedSEM']
    ExcFitCurve = ExcData['fitResponse']
    
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVsustainedResponseArray = PVData['sustainedResponseArray']
    PVsustainedError = PVData['sustainedSEM']
    PVFitCurve = PVData['fitResponse']
    
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMsustainedResponseArray = SOMData['sustainedResponseArray']
    SOMsustainedError = SOMData['sustainedSEM']
    SOMFitCurve = SOMData['fitResponse']

    bands = PVData['possibleBands']
    fitBands = PVData['fitBands']
    
    sustainedResponses = [ExcSustainedResponseArray, PVsustainedResponseArray, SOMsustainedResponseArray]
    sustainedErrors = [ExcSustainedError, PVsustainedError, SOMsustainedError]
    fitResponses = [ExcFitCurve, PVFitCurve, SOMFitCurve]
    
    ExColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [ExColor, PVColor, SOMColor]
    panelLabels = ['E', 'G', 'I']
    
    for indCell, responseByCell in enumerate(sustainedResponses):
        plt.hold(1)
        axCurve = plt.subplot(gs[2*indCell:2*indCell+2,2])
        plt.plot(bands, responseByCell, 'o', ms=5,
                 color=cellTypeColours[indCell], mec=cellTypeColours[indCell], clip_on=False)
        plt.errorbar(bands, responseByCell, yerr = [sustainedErrors[indCell], sustainedErrors[indCell]], 
                     fmt='none', ecolor=cellTypeColours[indCell])
#         plt.fill_between(range(len(bands)), responseByCell - sustainedErrors[indCell], 
#                          responseByCell + sustainedErrors[indCell], alpha=0.2, color=cellTypeColours[indCell], edgecolor='none')
        plt.plot([bands[0],bands[-1]], np.tile(responseByCell[0], 2), '--', color='0.4', lw=2)
        plt.plot(fitBands, fitResponses[indCell], '-', lw=1.5, color=cellTypeColours[indCell])
        axCurve.annotate(panelLabels[indCell], xy=(labelPosX[2],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axCurve.set_xticklabels('')
        axCurve.set_ylim(bottom=0)
        #yLims = np.array(plt.ylim())
        #axCurve.set_ylim(top=yLims[1]*1.3)
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        if not indCell:
            plt.title('Sustained responses',fontsize=fontSizeLabels,fontweight='normal')
        if indCell==2:
            axCurve.set_xticklabels(bands)
            plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(-0.5,6.5) #expand x axis so you don't have dots on y axis
                

# gs1 = gridspec.GridSpec(1,2)
# gs1.update(top=0.95, bottom=0.05, left=0.1, right=0.95, wspace=0.4, hspace=0.3)

# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppression = summaryData['fitPVsustainedSuppressionInd']
    SOMsustainedSuppression = summaryData['fitSOMsustainedSuppressionInd']
    ACsustainedSuppression = summaryData['fitExcSustainedSuppressionInd']
    
    sustainedSuppressionVals = [ACsustainedSuppression, PVsustainedSuppression, SOMsustainedSuppression]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Ex.', 'PV', 'SOM']
    
    panelLabel = 'J'
    
    axScatter = plt.subplot(gs[:3,3])
    plt.hold(1)
    for category in range(len(sustainedSuppressionVals)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(sustainedSuppressionVals[category]))
        
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
        
        plt.hold(True)
#         plt.plot(xval, sustainedSuppressionVals[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
#         median = np.median(sustainedSuppressionVals[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
    parts = plt.violinplot(sustainedSuppressionVals, widths=0.9, points=500, showmedians=True, showextrema=False)
    for ind,pc in enumerate(parts['bodies']):
        pc.set_facecolor(cellTypeColours[ind])
        pc.set_edgecolor(cellTypeColours[ind])
        pc.set_alpha(0.6)
    axScatter.annotate(panelLabel, xy=(labelPosX[3],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedSuppressionVals)+1)
    plt.ylim(-0.05,1.05)
    axScatter.set_xticks(range(1,len(sustainedSuppressionVals)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.10, yLims[1]*0.04, gapFactor=0.25)
    extraplots.significance_stars([1,2], yLims[1]*1.05, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    
# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[3]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedPrefBW = summaryData['fitPVsustainedPrefBW']
    SOMsustainedPrefBW = summaryData['fitSOMsustainedPrefBW']
    ACsustainedPrefBW = summaryData['fitExcSustainedPrefBW']
    
    prefBandwidths = [ACsustainedPrefBW, PVsustainedPrefBW, SOMsustainedPrefBW]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Ex.', 'PV', 'SOM']
    
    panelLabel = 'K'
    
    axScatter = plt.subplot(gs[3:,3])
    plt.hold(1)
    for category in range(len(prefBandwidths)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(prefBandwidths[category]))
        
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
        
        plt.plot(xval, prefBandwidths[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(prefBandwidths[category])
        print median
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels)
    axScatter.annotate(panelLabel, xy=(labelPosX[3],labelPosY[3]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(prefBandwidths)+1)
    plt.ylim(-0.3,6.3)
    axScatter.set_xticks(range(1,len(prefBandwidths)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.05, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)

# Summary plots showing firing rates of Ex, PV, SOM cells that have positive change in firing rate during sustained response    
if PANELS[4]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVaveragePSTH = summaryData['PVaveragePSTH']
    SOMaveragePSTH = summaryData['SOMaveragePSTH']
    
    binStartTimes = summaryData['PSTHbinStartTimes']
    
    categoryLabels = ['PV', 'SOM']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'L'
    
    axPSTH = plt.subplot(gs[:2,4])
    plt.hold(1)
    plt.plot(binStartTimes[1:-1],PVaveragePSTH[1:-1],color=PVColor, lw=2)
    plt.plot(binStartTimes[1:-1],SOMaveragePSTH[1:-1],color=SOMColor, lw=2)
    zline = plt.axvline(0,color='0.75',zorder=-10)
    plt.ylim(0,1.1)
    plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
    plt.ylabel('Normalized firing rate', fontsize=fontSizeLabels)
    axPSTH.annotate(panelLabel, xy=(labelPosX[4],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axPSTH)
    
if PANELS[5]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVonsetProp = summaryData['PVonsetProp']
    SOMonsetProp = summaryData['SOMonsetProp']
    
    cellTypes = [PVonsetProp, SOMonsetProp]
    
    categoryLabels = ['PV', 'SOM']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'M'
    
    axScatter = plt.subplot(gs[2:4,4])
    plt.hold(1)
    for category in range(len(cellTypes)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(cellTypes[category]))
        
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
        
        plt.plot(xval, cellTypes[category]*100.0, 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
        median = np.median(cellTypes[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median*100.0,median*100.0], '-', color='k', mec=cellTypeColours[category], lw=3)
    plt.xlim(0,len(cellTypes)+1)
    plt.ylim(0,60)
    axScatter.set_xticks(range(1,len(cellTypes)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('Spikes in first 50 ms (%)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*0.95, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[4],labelPosY[1]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
if PANELS[6]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVhighBandRate = summaryData['PVsustainedResponses']-summaryData['PVbaselines']
    SOMhighBandRate = summaryData['SOMsustainedResponses']-summaryData['SOMbaselines']
    
    print PVhighBandRate
    
    cellTypes = [PVhighBandRate, SOMhighBandRate]
    
    categoryLabels = ['PV', 'SOM']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'N'
    
    axScatter = plt.subplot(gs[4:,4])
    plt.hold(1)
    for category in range(len(cellTypes)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(cellTypes[category]))
        
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
        
        plt.plot(xval, cellTypes[category], 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
        median = np.median(cellTypes[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
    plt.xlim(0,len(cellTypes)+1)
    #plt.ylim(0,60)
    axScatter.set_xticks(range(1,len(cellTypes)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('Change in Firing Rate (high bandwidths)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*1.05, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[4],labelPosY[2]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)