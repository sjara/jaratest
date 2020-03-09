import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots


import figparams
reload(figparams)


FIGNAME = 'supplement_figure_characterisation_of_responses_pure_tone_fit'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
exampleDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_characterisation_of_responses_by_cell_type') #using same example cells as in figure 1

PANELS = [1,1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig3_characterisation_of_pure_tone_responses' # Do not include extension
#figFormat = 'pdf' # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [7,6] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.01, 0.33, 0.67]   # Horiz position for panel labels
labelPosY = [0.97, 0.5]    # Vert position for panel labels

ExcColour = figparams.colp['excitatoryCell']
#Exclight = matplotlib.colors.colorConverter.to_rgba(ExcColour, alpha=0.5)
PVcolour = figparams.colp['PVcell']
#PVlight = matplotlib.colors.colorConverter.to_rgba(PVcolour, alpha=0.5)
SOMcolour = figparams.colp['SOMcell']
#SOMlight = matplotlib.colors.colorConverter.to_rgba(SOMcolour, alpha=0.5)

# laserColour = figparams.colp['greenLaser']
# 
# soundColour = figparams.colp['sound']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,3,width_ratios=[1,1,1])
gs.update(top=0.96, left=0.08, right=0.98, bottom=0.09, wspace=0.5, hspace=0.2)

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

summaryFileName = 'all_photoidentified_cells_stats_pure_tone.npz'
facilitationFileName = 'facilitation_stats.npz'

# -- Plots of sustained bandwidth tuning --
axExamples = gs[:,0]
gs2 = gridspec.GridSpecFromSubplotSpec(3,1, subplot_spec=axExamples, wspace=0.5, hspace=0.2)

if PANELS[0]:
    ExcFile = 'example_Exc_bandwidth_tuning_'+ExcFileName
    ExcDataFullPath = os.path.join(exampleDataDir,ExcFile)
    ExcData = np.load(ExcDataFullPath)
    
    ExcSustainedResponseArray = ExcData['sustainedResponseArrayPureTone']
    ExcSustainedError = ExcData['sustainedSEMPureTone']
    ExcFitCurve = ExcData['fitResponsePureTone']
    ExcSI = ExcData['SIPureTone'].tolist()
    ExcBaseline = ExcData['sustainedResponseArray'][0]
    
    PVFile = 'example_PV_bandwidth_tuning_'+PVFileName
    PVDataFullPath = os.path.join(exampleDataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    PVsustainedResponseArray = PVData['sustainedResponseArrayPureTone']
    PVsustainedError = PVData['sustainedSEMPureTone']
    PVFitCurve = PVData['fitResponsePureTone']
    PVSI = PVData['SIPureTone'].tolist()
    PVBaseline = PVData['sustainedResponseArray'][0]
    
    SOMFile = 'example_SOM_bandwidth_tuning_'+SOMFileName
    SOMDataFullPath = os.path.join(exampleDataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    SOMsustainedResponseArray = SOMData['sustainedResponseArrayPureTone']
    SOMsustainedError = SOMData['sustainedSEMPureTone']
    SOMFitCurve = SOMData['fitResponsePureTone']
    SOMSI = SOMData['SIPureTone'].tolist()
    SOMBaseline = SOMData['sustainedResponseArray'][0]

    bands = PVData['possibleBands']
    fitBands = PVData['fitBands']
    
    sustainedResponses = [ExcSustainedResponseArray, PVsustainedResponseArray, SOMsustainedResponseArray]
    sustainedErrors = [ExcSustainedError, PVsustainedError, SOMsustainedError]
    fitResponses = [ExcFitCurve, PVFitCurve, SOMFitCurve]
    SIs = [ExcSI, PVSI, SOMSI]
    baselines = [ExcBaseline, PVBaseline, SOMBaseline]
    
    ExColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [ExColor, PVColor, SOMColor]
    panelLabel = 'A'
    
    for indCell, responseByCell in enumerate(sustainedResponses):
        plt.hold(1)
        axCurve = plt.subplot(gs2[indCell,0])
        #axCurve.set_xscale('log', basex=2, nonposx='clip')
        axCurve.set_xscale('symlog', basex=2, linthreshx=0.25, linscalex=0.5)
        plt.plot(bands, responseByCell, 'o', ms=5,
                 color=cellTypeColours[indCell], mec=cellTypeColours[indCell], clip_on=False)
        plt.errorbar(bands, responseByCell, yerr = [sustainedErrors[indCell], sustainedErrors[indCell]], 
                     fmt='none', ecolor=cellTypeColours[indCell], lw=1.5, capsize=5)
#         plt.fill_between(range(len(bands)), responseByCell - sustainedErrors[indCell], 
#                          responseByCell + sustainedErrors[indCell], alpha=0.2, color=cellTypeColours[indCell], edgecolor='none')
        plt.plot([bands[0],bands[-1]], np.tile(baselines[indCell], 2), '--', color='0.4', lw=2)
        plt.plot(fitBands, fitResponses[indCell], '-', lw=1.5, color=cellTypeColours[indCell])
        axCurve.set_xticks(bands)
        axCurve.set_ylim(bottom=0)
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        axCurve.tick_params(top=False, right=False, which='both')
        if indCell!=2:
            axCurve.set_xticklabels('')
        else:
            bandLabels = bands.tolist()
            bandLabels[-1] = 'WN'
            bandLabels[0] = 'PT'
            bandLabels[1::2] = ['']*len(bands[1::2]) #remove every other label so x axis less crowded
            axCurve.set_xticklabels(bandLabels)
            plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(-0.1,7) #expand x axis so you don't have dots on y axis
        plt.locator_params(axis='y', nbins=5)
        
    axCurve.annotate(panelLabel, xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')

# -- Summary plots comparing suppression indices of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[1]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppression = summaryData['fitPVsustainedSuppressionIndPureTone']
    SOMsustainedSuppression = summaryData['fitSOMsustainedSuppressionIndPureTone']
    ACsustainedSuppression = summaryData['fitExcSustainedSuppressionIndPureTone']
    
    sustainedSuppressionVals = [ACsustainedSuppression, PVsustainedSuppression, SOMsustainedSuppression]
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    
    panelLabel = 'B'
    
    axScatter = plt.subplot(gs[0,1])
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
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedSuppressionVals)+1)
    plt.ylim(-0.05,1.05)
    plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(sustainedSuppressionVals)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.08, yLims[1]*0.02, gapFactor=0.25)
    extraplots.significance_stars([1,2], yLims[1]*1.04, yLims[1]*0.02, gapFactor=0.25)
    plt.hold(0)
    
    ExcPV = stats.ranksums(ACsustainedSuppression, PVsustainedSuppression)[1]
    ExcSOM = stats.ranksums(ACsustainedSuppression, SOMsustainedSuppression)[1]
    PVSOM = stats.ranksums(PVsustainedSuppression, SOMsustainedSuppression)[1]
    print "Difference in suppression p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)
    
# -- plots of "Anna index" --
if PANELS[2]:
    facilitationDataFullPath = os.path.join(dataDir,facilitationFileName)
    facilitationData = np.load(facilitationDataFullPath)
    
    ExfitPTindex = facilitationData['ExfitPTindex']
    PVfitPTindex = facilitationData['PVfitPTindex']
    SOMfitPTindex = facilitationData['SOMfitPTindex']
    
    sustainedPTindex = [ExfitPTindex, PVfitPTindex, SOMfitPTindex]
    
    panelLabel = 'C'
    
    axScatter = plt.subplot(gs[0,2])
    plt.hold(1)
    
    for category in range(len(sustainedPTindex)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(sustainedPTindex[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.hold(True)
        plt.plot(xval, sustainedPTindex[category], 'o', mec=edgeColour, mfc='none', clip_on=True)
        median = np.median(sustainedPTindex[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)  
    
    axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedPTindex)+1)
    plt.ylim(-1.05,1.05)
    #plt.ylim(-5.05, 1.05)
    plt.ylabel('PT vs. WN index')#,fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(sustainedPTindex)+1))
    axScatter.set_xticklabels(categoryLabels)#, fontsize=fontSizeLabels, rotation=-45)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.16, yLims[1]*0.04, gapFactor=0.25)
    extraplots.significance_stars([1,2], yLims[1]*1.08, yLims[1]*0.04, gapFactor=0.25)
    plt.hold(0)
    
    ExcPV = stats.ranksums(ExfitPTindex, PVfitPTindex)[1]
    ExcSOM = stats.ranksums(ExfitPTindex, SOMfitPTindex)[1]
    PVSOM = stats.ranksums(PVfitPTindex, SOMfitPTindex)[1]
    print "Difference in PT p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)
    
# -- Summary plots comparing preferred bandwidth of PV, SOM, and excitatory cells for sustained responses --    
if PANELS[3]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedPrefBW = summaryData['fitPVsustainedPrefBWPureTone']
    SOMsustainedPrefBW = summaryData['fitSOMsustainedPrefBWPureTone']
    ACsustainedPrefBW = summaryData['fitExcSustainedPrefBWPureTone']
    
    prefBandwidths = [ACsustainedPrefBW, PVsustainedPrefBW, SOMsustainedPrefBW]
    
    #possibleBands = summaryData['possibleBands']
    
    excitatoryColor = figparams.colp['excitatoryCell']
    PVColor = figparams.colp['PVcell']
    SOMColor = figparams.colp['SOMcell']
    
    cellTypeColours = [excitatoryColor, PVColor, SOMColor]
    
    categoryLabels = ['Exc.', 'PV', 'SOM']
    
    panelLabel = 'D'
    
    axScatter = plt.subplot(gs[1,1])
    plt.hold(1)
    axScatter.set_yscale('symlog', basey=2, linthreshy=0.25, linscaley=0.5)
    plt.hold(True)
    for category in range(len(prefBandwidths)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(prefBandwidths[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.plot(xval, prefBandwidths[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(prefBandwidths[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(prefBandwidths)+1)
    plt.ylim(-0.05,7)
    plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(prefBandwidths)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    axScatter.set_yticks(bands)
#     bandLabels = possibleBands.tolist()
#     bandLabels[-1] = 'WN'
    bandLabels = bands.tolist()
    bandLabels[-1] = 'WN'
    bandLabels[0] = 'PT'
    axScatter.set_yticklabels(bandLabels)
    axScatter.tick_params(top=False, right=False, which='both')
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,3], yLims[1]*1.08, yLims[1]*0.1, gapFactor=0.25)
    plt.hold(0)
    
    ExcPV = stats.ranksums(ACsustainedPrefBW, PVsustainedPrefBW)[1]
    ExcSOM = stats.ranksums(ACsustainedPrefBW, SOMsustainedPrefBW)[1]
    PVSOM = stats.ranksums(PVsustainedPrefBW, SOMsustainedPrefBW)[1]
    print "Difference in pref bandwidth p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)
    
# -- summary plot showing facilitation indices for all cells --
if PANELS[4]:
    facilitationDataFullPath = os.path.join(dataDir,facilitationFileName)
    facilitationData = np.load(facilitationDataFullPath)
    
    ExfitFacilitation = facilitationData['ExfitFacilitation']
    PVfitFacilitation = facilitationData['PVfitFacilitation']
    SOMfitFacilitation = facilitationData['SOMfitFacilitation']
    
    sustainedFacilitationVals = [ExfitFacilitation, PVfitFacilitation, SOMfitFacilitation]
    
    axScatter = plt.subplot(gs[1,2])
    plt.hold(1)
    
    panelLabel = 'E'
    
    for category in range(len(sustainedFacilitationVals)):
        edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
        xval = (category+1)*np.ones(len(sustainedFacilitationVals[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.4 * jitterAmt) - 0.2
          
        plt.hold(True)
        plt.plot(xval, sustainedFacilitationVals[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
        median = np.median(sustainedFacilitationVals[category])
        #sem = stats.sem(vals[category])
        plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)  
    
    axScatter.annotate(panelLabel, xy=(labelPosX[2],labelPosY[1]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedFacilitationVals)+1)
    plt.ylim(-0.05,1.05)
    plt.ylabel('Facilitation Index')#,fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(sustainedFacilitationVals)+1))
    axScatter.set_xticklabels(categoryLabels)#, fontsize=fontSizeLabels, rotation=-45)
    extraplots.boxoff(axScatter)
    yLims = np.array(plt.ylim())
    #extraplots.significance_stars([1,3], yLims[1]*1.07, yLims[1]*0.02, gapFactor=0.25)
    #extraplots.significance_stars([1,2], yLims[1]*1.03, yLims[1]*0.02, gapFactor=0.25)
    plt.hold(0)
    
    ExcPV = stats.ranksums(ExfitFacilitation, PVfitFacilitation)[1]
    ExcSOM = stats.ranksums(ExfitFacilitation, SOMfitFacilitation)[1]
    PVSOM = stats.ranksums(PVfitFacilitation, SOMfitFacilitation)[1]
    print "Difference in facilitation p vals: \nExc-PV: {0}\nExc-SOM: {1}\nPV-SOM: {2}".format(ExcPV,ExcSOM,PVSOM)
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
