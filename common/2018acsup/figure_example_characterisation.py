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
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches

from jaratoolbox import settings
from jaratoolbox import extraplots
reload(extraplots)

import figparams
reload(figparams)



FIGNAME = 'figure_characterisation_of_responses_by_cell_type'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'Fig2_characterisation_of_suppression' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [10,7] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.01, 0.26, 0.76]   # Horiz position for panel labels
labelPosY = [0.96, 0.64, 0.33, 0.47]    # Vert position for panel labels

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

ExColor = figparams.colp['excitatoryCell']
PVColor = figparams.colp['PVcell']
SOMColor = figparams.colp['SOMcell']

ExLight = matplotlib.colors.colorConverter.to_rgba(ExColor, alpha=0.5)
PVlight = matplotlib.colors.colorConverter.to_rgba(PVColor, alpha=0.5)
SOMlight = matplotlib.colors.colorConverter.to_rgba(SOMColor, alpha=0.5)

soundColor = figparams.colp['sound']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,3,width_ratios=[1,2.3,1])
gs.update(top=0.95, bottom=0.08, left=0.05, right=0.99, wspace=0.5, hspace=0.3)

# --- space for cartoons ---
if PANELS[0]:
    axCartoon = plt.subplot(gs[:,0])
    plt.axis('off')
    
    #also do the panel labels for the rest of the cartoons in here I guess
    cartoonPanels = ['A', 'B']
    for indPanel, panel in enumerate(cartoonPanels):
        axCartoon.annotate(panel, xy=(labelPosX[0],labelPosY[indPanel*3]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')

# separate gridspec for examples to make them really cozy
axExamples = gs[:,1]
gs2 = gridspec.GridSpecFromSubplotSpec(3,2, subplot_spec=axExamples, hspace=0.3, wspace=0.45)

# --- Raster plots of example PV and SOM cell ---        
if PANELS[1]: 
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
    panelLabels = ['C', 'D', 'E']
    
    colours = [[ExColor, ExLight],[PVColor, PVlight],[SOMColor, SOMlight]]
    
    for indCell, cell in enumerate(cellData):
        axRaster = plt.subplot(gs2[indCell,0])
        plt.cla()
        bandSpikeTimesFromEventOnset = cell['spikeTimesFromEventOnset']
        bandIndexLimitsEachTrial = cell['indexLimitsEachTrial']
        rasterTimeRange = cell['rasterTimeRange']
        trialsEachCond = cell['trialsEachCond']
        trialsEachCond = trialsEachCond[:,1:] #don't include pure tone
        trialsEachCond = trialsEachCond[:-70,:] #remove last couple of trials where baseline seems to increase
        possibleBands = cell['possibleBands']
        possibleBands = possibleBands[1:]
        bandLabels = possibleBands.tolist()
        bandLabels[-1] = 'WN'
        colorEachCond = colours[indCell]*(len(possibleBands)/2+1)
        pRaster, hcond, zline = extraplots.raster_plot(bandSpikeTimesFromEventOnset,bandIndexLimitsEachTrial,rasterTimeRange,
                                                       trialsEachCond=trialsEachCond,labels=bandLabels,colorEachCond=colorEachCond)
        axRaster.annotate(panelLabels[indCell], xy=(labelPosX[1],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        plt.setp(pRaster, ms=3, color='k')
        extraplots.boxoff(axRaster)
        if indCell != 2:
            axRaster.set_xticklabels('')
        plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        
        yLims = np.array(plt.ylim())
        rect = patches.Rectangle((0.0,yLims[1]*1.02),1.0,yLims[1]*0.04,linewidth=1,edgecolor=soundColor,facecolor=soundColor,clip_on=False)
        axRaster.add_patch(rect)
        
    
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.xlabel('Time from sound onset (s)',fontsize=fontSizeLabels)



# -- Plots of sustained bandwidth tuning --
if PANELS[2]:
    SIlabelPosX = [0.62, 0.62, 0.58]
    SIlabelPosY = [0.87, 0.45, 0.31]
    calcInd = 2 #which cell to annotate SI calculation on
    
    ExcFile = 'example_Exc_bandwidth_tuning_'+ExcFileName
    ExcDataFullPath = os.path.join(dataDir,ExcFile)
    ExcData = np.load(ExcDataFullPath)
    
    ExcSustainedResponseArray = ExcData['sustainedResponseArray']
    ExcSustainedError = ExcData['sustainedSEM']
    ExcFitCurve = ExcData['fitResponseNoZero']
    ExcSI = ExcData['SINoZero'].tolist()
    
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVsustainedResponseArray = PVData['sustainedResponseArray']
    PVsustainedError = PVData['sustainedSEM']
    PVFitCurve = PVData['fitResponseNoZero']
    PVSI = PVData['SINoZero'].tolist()
    
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMsustainedResponseArray = SOMData['sustainedResponseArray']
    SOMsustainedError = SOMData['sustainedSEM']
    SOMFitCurve = SOMData['fitResponseNoZero']
    SOMSI = SOMData['SINoZero'].tolist()

    bands = PVData['possibleBands'][1:]
    fitBands = PVData['fitBandsNoZero']
    
    sustainedResponses = [ExcSustainedResponseArray, PVsustainedResponseArray, SOMsustainedResponseArray]
    sustainedErrors = [ExcSustainedError, PVsustainedError, SOMsustainedError]
    fitResponses = [ExcFitCurve, PVFitCurve, SOMFitCurve]
    SIs = [ExcSI, PVSI, SOMSI]
    
    cellTypeColours = [ExColor, PVColor, SOMColor]
    
    for indCell, responseByCell in enumerate(sustainedResponses):
        plt.hold(1)
        axCurve = plt.subplot(gs2[indCell,1])
        #axCurve.set_xscale('log', basex=2, nonposx='clip')
        axCurve.set_xscale('log', basex=2)
        plt.plot(bands, responseByCell[1:], 'o', ms=5,
                 color=cellTypeColours[indCell], mec=cellTypeColours[indCell], clip_on=False)
        plt.errorbar(bands, responseByCell[1:], yerr = [sustainedErrors[indCell][1:], sustainedErrors[indCell][1:]], 
                     fmt='none', ecolor=cellTypeColours[indCell], lw=1.5, capsize=5)
#         plt.fill_between(range(len(bands)), responseByCell - sustainedErrors[indCell], 
#                          responseByCell + sustainedErrors[indCell], alpha=0.2, color=cellTypeColours[indCell], edgecolor='none')
        plt.plot([bands[0],bands[-1]], np.tile(responseByCell[0], 2), '--', color='0.4', lw=2)
        plt.plot(fitBands, fitResponses[indCell], '-', lw=1.5, color=cellTypeColours[indCell])
        axCurve.set_xticks(bands)
        axCurve.set_ylim(bottom=0)
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        axCurve.tick_params(top=False, right=False, which='both')
        if indCell == calcInd:
            axCurve.annotate(r'SI = $\frac{a-b}{a}$ = %.2f' % (SIs[indCell],), xy=(SIlabelPosX[indCell],SIlabelPosY[indCell]), xycoords='figure fraction',
                     fontsize=fontSizeLabels, color=cellTypeColours[indCell])
            bandMax = fitBands[np.argmax(fitResponses[indCell])]
            respMax = np.max(fitResponses[indCell])
            bandWN = fitBands[-1]
            respWN = fitResponses[indCell][-1]
            axCurve.annotate("", xy=(bandMax, respMax), xycoords='data',
                             xytext=(bandMax, 0), textcoords='data',
                             arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color='k'))
            axCurve.annotate(r'$a$', xy=(bandMax/1.35, respMax/3), xycoords='data',
                     fontsize=fontSizeLabels, color='k')
            axCurve.annotate("", xy=(bandWN, respWN), xycoords='data',
                             xytext=(bandWN, 0), textcoords='data',
                             arrowprops=dict(arrowstyle="<->",connectionstyle="arc3",color='k'))
            axCurve.annotate(r'$b$', xy=(bandWN/1.35, respWN/3), xycoords='data',
                     fontsize=fontSizeLabels, color='k')
        else:
            axCurve.annotate('SI = %.2f' % (SIs[indCell],), xy=(SIlabelPosX[indCell],SIlabelPosY[indCell]), xycoords='figure fraction',
                     fontsize=fontSizeLabels, color=cellTypeColours[indCell])
        if indCell!=2:
            axCurve.set_xticklabels('')
        else:
            bandLabels = bands.tolist()
            bandLabels[-1] = 'WN'
            bandLabels[1::2] = ['']*len(bands[1::2]) #remove every other label so x axis less crowded
            axCurve.set_xticklabels(bandLabels)
            plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(0.2,7) #expand x axis so you don't have dots on y axis
        #plt.title(panelTitles[indCell],fontsize=fontSizeLabels, y=1.02)

# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[3]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppression = summaryData['fitPVsustainedSuppressionNoZero']
    SOMsustainedSuppression = summaryData['fitSOMsustainedSuppressionNoZero']
    ACsustainedSuppression = summaryData['fitExcsustainedSuppressionNoZero']
    
    sustainedSuppressionVals = [ACsustainedSuppression, PVsustainedSuppression, SOMsustainedSuppression]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Exc.', r'PV$^+$', r'SOM$^+$']
    
    panelLabel = 'F'
    
    axScatter = plt.subplot(gs[0,2])
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
    
    axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedSuppressionVals)+1)
    plt.ylim(-0.05,1.05)
    plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(sustainedSuppressionVals)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels, rotation=-45)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.07, yLims[1]*0.02, gapFactor=0.25)
    extraplots.significance_stars([1,2], yLims[1]*1.03, yLims[1]*0.02, gapFactor=0.25)
    plt.hold(0)
    
    ExcPV = stats.ranksums(ACsustainedSuppression, PVsustainedSuppression)[1]
    ExcSOM = stats.ranksums(ACsustainedSuppression, SOMsustainedSuppression)[1]
    PVSOM = stats.ranksums(PVsustainedSuppression, SOMsustainedSuppression)[1]
    print "Difference in suppression p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)
    
    
    
# -- Summary plots comparing preferred bandwidth of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[4]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedPrefBW = summaryData['fitPVsustainedPrefBWNoZero']
    SOMsustainedPrefBW = summaryData['fitSOMsustainedPrefBWNoZero']
    ACsustainedPrefBW = summaryData['fitExcsustainedPrefBWNoZero']
    
    prefBandwidths = [ACsustainedPrefBW, PVsustainedPrefBW, SOMsustainedPrefBW]
    
    possibleBands = summaryData['possibleBands'][1:]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Exc.', r'PV$^+$', r'SOM$^+$']
    
    panelLabel = 'G'
    
    axScatter = plt.subplot(gs[1,2])
    plt.hold(1)
    axScatter.set_yscale('log', basey=2)
    plt.hold(True)
    for category in range(len(prefBandwidths)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(prefBandwidths[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.plot(xval, prefBandwidths[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(prefBandwidths[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
    
#     bplot = plt.boxplot(prefBandwidths, widths=0.6, showfliers=False)
#     
#     for box in range(len(bplot['boxes'])):
#         plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
#         plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
#         plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
#         plt.setp(bplot['medians'][box], color='k', linewidth=2)
#         #plt.setp(bplot['fliers'][box, marker='o', color=cellTypeColours[box]])
# 
#     plt.setp(bplot['medians'], color='k')
    
    axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[3]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(prefBandwidths)+1)
    plt.ylim(0.2,7)
    plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(prefBandwidths)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels, rotation=-45)
    axScatter.set_yticks(possibleBands)
    bandLabels = possibleBands.tolist()
    bandLabels[-1] = 'WN'
    axScatter.set_yticklabels(bandLabels)
    axScatter.tick_params(top=False, right=False, which='both')
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.05, yLims[1]*0.1, gapFactor=0.25)
    plt.hold(0)
    
    ExcPV = stats.ranksums(ACsustainedPrefBW, PVsustainedPrefBW)[1]
    ExcSOM = stats.ranksums(ACsustainedPrefBW, SOMsustainedPrefBW)[1]
    PVSOM = stats.ranksums(PVsustainedPrefBW, SOMsustainedPrefBW)[1]
    print "Difference in pref bandwidth p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)