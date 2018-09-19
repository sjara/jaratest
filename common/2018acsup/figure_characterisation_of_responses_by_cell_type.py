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
figFilename = 'characterisation_of_suppression_log' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [12,8] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.21, 0.4, 0.58, 0.76]   # Horiz position for panel labels
labelPosY = [0.96, 0.65, 0.34, 0.5]    # Vert position for panel labels

#PVFileName = 'band026_2017-04-26_1470um_T4_c5.npz'
#PVFileName = 'band026_2017-04-27_1350um_T4_c2.npz'
#PVFileName = 'band032_2017-07-21_1200um_T6_c2.npz'
PVFileName = 'band033_2017-07-27_1700um_T4_c5.npz'

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
    panelLabels = ['b', 'e', 'h']
    panelTitles = ['Excitatory', 'PV', 'SOM']
    
    for indCell, cell in enumerate(cellData):
        axRaster = plt.subplot(gs[2*indCell:2*indCell+2,1])
        plt.cla()
        bandSpikeTimesFromEventOnset = cell['spikeTimesFromEventOnset']
        bandIndexLimitsEachTrial = cell['indexLimitsEachTrial']
        rasterTimeRange = cell['rasterTimeRange']
        trialsEachCond = cell['trialsEachCond']
        trialsEachCond = trialsEachCond[:,1:] #don't include pure tone
        trialsEachCond = trialsEachCond[:-70,:] #remove last couple of trials where baseline seems to increase
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
    cartoonPanels = ['a', 'd', 'g']
    for indPanel, panel in enumerate(cartoonPanels):
        axRaster.annotate(panel, xy=(labelPosX[0],labelPosY[indPanel]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')



# -- Plots of sustained bandwidth tuning --
if PANELS[1]:
    SIlabelPosX = [0.5, 0.5, 0.48]
    SIlabelPosY = [0.87, 0.6, 0.32]
    calcInd = 2 #which cell to annotate SI calculation on
    
    ExcFile = 'example_Exc_bandwidth_tuning_'+ExcFileName
    ExcDataFullPath = os.path.join(dataDir,ExcFile)
    ExcData = np.load(ExcDataFullPath)
    
    ExcSustainedResponseArray = ExcData['sustainedResponseArray']
    ExcSustainedError = ExcData['sustainedSEM']
    ExcFitCurve = ExcData['fitResponse']
    ExcSI = ExcData['SI'].tolist()
    
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVsustainedResponseArray = PVData['sustainedResponseArray']
    PVsustainedError = PVData['sustainedSEM']
    PVFitCurve = PVData['fitResponse']
    PVSI = PVData['SI'].tolist()
    
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMsustainedResponseArray = SOMData['sustainedResponseArray']
    SOMsustainedError = SOMData['sustainedSEM']
    SOMFitCurve = SOMData['fitResponse']
    SOMSI = SOMData['SI'].tolist()

    bands = PVData['possibleBands']
    fitBands = PVData['fitBands']
    
    sustainedResponses = [ExcSustainedResponseArray, PVsustainedResponseArray, SOMsustainedResponseArray]
    sustainedErrors = [ExcSustainedError, PVsustainedError, SOMsustainedError]
    fitResponses = [ExcFitCurve, PVFitCurve, SOMFitCurve]
    SIs = [ExcSI, PVSI, SOMSI]
    
    ExColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [ExColor, PVColor, SOMColor]
    panelLabels = ['c', 'f', 'i']
    
    for indCell, responseByCell in enumerate(sustainedResponses):
        plt.hold(1)
        axCurve = plt.subplot(gs[2*indCell:2*indCell+2,2])
        axCurve.set_xscale('symlog', basex=2, linthreshx=0.25)
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
        axCurve.set_xticks(bands)
        axCurve.set_ylim(bottom=0)
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        if not indCell:
            plt.title('Sustained responses',fontsize=fontSizeLabels,fontweight='normal')
        if indCell == calcInd:
            axCurve.annotate(r'SI = $\frac{a-b}{a}$ = %.2f' % (SIs[indCell],), xy=(SIlabelPosX[indCell],SIlabelPosY[indCell]), xycoords='figure fraction',
                     fontsize=fontSizeLabels, color=cellTypeColours[indCell])
            bandMax = fitBands[np.argmax(fitResponses[indCell])]
            respMax = np.max(fitResponses[indCell])
            bandWN = fitBands[-1]
            respWN = fitResponses[indCell][-1]
            axCurve.annotate("", xy=(bandMax, respMax), xycoords='data',
                             xytext=(bandMax, 0), textcoords='data',
                             arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color=cellTypeColours[indCell]))
            axCurve.annotate(r'$a$', xy=(bandMax-0.8, respMax/2), xycoords='data',
                     fontsize=fontSizeLabels, color=cellTypeColours[indCell])
            axCurve.annotate("", xy=(bandWN, respWN), xycoords='data',
                             xytext=(bandWN, 0), textcoords='data',
                             arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color=cellTypeColours[indCell]))
            axCurve.annotate(r'$b$', xy=(bandWN-0.8, respWN/2), xycoords='data',
                     fontsize=fontSizeLabels, color=cellTypeColours[indCell])
        else:
            axCurve.annotate('SI = %.2f' % (SIs[indCell],), xy=(SIlabelPosX[indCell],SIlabelPosY[indCell]), xycoords='figure fraction',
                     fontsize=fontSizeLabels, color=cellTypeColours[indCell])
        if indCell!=2:
            axCurve.set_xticklabels('')
        else:
            axCurve.set_xticklabels(bands)
            plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(-0.01,7) #expand x axis so you don't have dots on y axis
                

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
    
    panelLabel = 'j'
    
    axScatter = plt.subplot(gs[:3,3])
    plt.hold(1)
    
    for category in range(len(sustainedSuppressionVals)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(sustainedSuppressionVals[category]))
         
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
         
        plt.hold(True)
        plt.plot(xval, sustainedSuppressionVals[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(sustainedSuppressionVals[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
    
#     parts = plt.violinplot(sustainedSuppressionVals, widths=0.8, points=500, showextrema=False)
#     for category in range(len(sustainedSuppressionVals)):
#         median = np.median(sustainedSuppressionVals[category])
#         plt.plot([category+0.7, category+1.3], [median,median], '-', color='k', lw=2)
#     for ind,pc in enumerate(parts['bodies']):
#         pc.set_facecolor(cellTypeColours[ind])
#         pc.set_edgecolor(cellTypeColours[ind])
#         pc.set_alpha(0.6)
#     plt.ylabel('Suppression Index',fontsize=fontSizeLabels)    
    
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
    
    possibleBands = summaryData['possibleBands']
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Ex.', 'PV', 'SOM']
    
    panelLabel = 'k'
    
    axScatter = plt.subplot(gs[3:,3])
    plt.hold(1)
    axScatter.set_yscale('symlog', basey=2, linthreshy=0.25)
    plt.hold(True)
    for category in range(len(prefBandwidths)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(prefBandwidths[category]))
         
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
         
        plt.plot(xval, prefBandwidths[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(prefBandwidths[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        #plt.semilogy(xval, prefBandwidths[category], 'o', mec=edgeColour, mfc='none', clip_on=False, base=2)
        plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels)
    
#     parts = plt.violinplot(prefBandwidths, widths=0.8, points=500, showextrema=False)
#     for category in range(len(prefBandwidths)):
#         median = np.median(prefBandwidths[category])
#         plt.plot([category+0.7, category+1.3], [median,median], '-', color='k', lw=2)
#     for ind,pc in enumerate(parts['bodies']):
#         pc.set_facecolor(cellTypeColours[ind])
#         pc.set_edgecolor(cellTypeColours[ind])
#         pc.set_alpha(0.6)
#     plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels) 
    
    axScatter.annotate(panelLabel, xy=(labelPosX[3],labelPosY[3]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(prefBandwidths)+1)
    plt.ylim(-0.01,7)
    axScatter.set_xticks(range(1,len(prefBandwidths)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    axScatter.set_yticks(possibleBands)
    axScatter.set_yticklabels(possibleBands)
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
    
    panelLabel = 'l'
    
    axPSTH = plt.subplot(gs[:2,4])
    plt.hold(1)
    plt.plot(binStartTimes[1:-1],PVaveragePSTH[1:-1],color=PVColor, lw=2)
    plt.plot(binStartTimes[1:-1],SOMaveragePSTH[1:-1],color=SOMColor, lw=2)
    zline = plt.axvline(0,color='0.75',zorder=-10)
    plt.ylim(-0.1,1.1)
    plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
    plt.ylabel('Normalized firing rate', fontsize=fontSizeLabels)
    axPSTH.annotate(panelLabel, xy=(labelPosX[4],labelPosY[0]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axPSTH)
    
if PANELS[5]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVonsetProp = summaryData['PVonsetProp']*100.0
    SOMonsetProp = summaryData['SOMonsetProp']*100.0
    
    onsetProps = [PVonsetProp, SOMonsetProp]
    
    categoryLabels = ['PV', 'SOM']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'm'
    
    axScatter = plt.subplot(gs[2:4,4])
    plt.hold(1)
    
#     for category in range(len(onsetProps)):
#         edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
#         xval = (category+1)*np.ones(len(onsetProps[category]))
#           
#         jitterAmt = np.random.random(len(xval))
#         xval = xval + (0.4 * jitterAmt) - 0.2
#           
#         plt.plot(xval, onsetProps[category], 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
#         median = np.median(onsetProps[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
          
    bplot = plt.boxplot(onsetProps, widths=0.6, showfliers=False)
    
    for box in range(len(bplot['boxes'])):
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=2)
        #plt.setp(bplot['fliers'][box, marker='o', color=cellTypeColours[box]])

    plt.setp(bplot['medians'], color='k')
    
#     parts = plt.violinplot(onsetProps, widths=0.8, points=500, showextrema=False)
#     for category in range(len(onsetProps)):
#         median = np.median(onsetProps[category])
#         plt.plot([category+0.7, category+1.3], [median,median], '-', color='k', lw=2)
#     for ind,pc in enumerate(parts['bodies']):
#         pc.set_facecolor(cellTypeColours[ind])
#         pc.set_edgecolor(cellTypeColours[ind])
#         pc.set_alpha(0.6)
    
    plt.xlim(0,len(onsetProps)+1)
    plt.ylim(0,32)
    axScatter.set_xticks(range(1,len(onsetProps)+1))
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
    
    responseRates = [PVhighBandRate, SOMhighBandRate]
    
    categoryLabels = ['PV', 'SOM']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [PVColor, SOMColor]
    
    panelLabel = 'n'
    
    axScatter = plt.subplot(gs[4:,4])
    plt.hold(1)
    
#     for category in range(len(responseRates)):
#         edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
#         xval = (category+1)*np.ones(len(responseRates[category]))
#          
#         jitterAmt = np.random.random(len(xval))
#         xval = xval + (0.4 * jitterAmt) - 0.2
#          
#         plt.plot(xval, responseRates[category], 'o', mec=edgeColour, mfc='none', ms=8, mew = 2, clip_on=False)
#         median = np.median(responseRates[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
        
    bplot = plt.boxplot(responseRates, widths=0.6, showfliers=False)
    
    for box in range(len(bplot['boxes'])):
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=2)

    plt.setp(bplot['medians'], color='k')
    
#     parts = plt.violinplot(responseRates, widths=0.8, points=500, showextrema=False)
#     for category in range(len(responseRates)):
#         median = np.median(responseRates[category])
#         plt.plot([category+0.7, category+1.3], [median,median], '-', color='k', lw=2)
#     for ind,pc in enumerate(parts['bodies']):
#         pc.set_facecolor(cellTypeColours[ind])
#         pc.set_edgecolor(cellTypeColours[ind])
#         pc.set_alpha(0.6)
    
    plt.xlim(0,len(responseRates)+1)
    plt.ylim(top=17)
    axScatter.set_xticks(range(1,len(responseRates)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    plt.ylabel('High bandwidth response (spk/s)', fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*1.05, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    axScatter.annotate(panelLabel, xy=(labelPosX[4],labelPosY[2]), xycoords='figure fraction',
                     fontsize=fontSizePanel, fontweight='bold')
    
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)