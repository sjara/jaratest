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

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams



FIGNAME = 'supplement_figure_characterisation_of_responses_pure_tone_fit'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
exampleDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'figure_characterisation_of_responses_by_cell_type') #using same example cells as in figure 1

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig_characterisation_of_suppression_pure_tone_fit' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [7,8] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01, 0.47]   # Horiz position for panel labels
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

summaryFileName = 'all_photoidentified_cells_stats_pure_tone.npz'


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(6,2,width_ratios=[1,1.2])
gs.update(top=0.95, bottom=0.08, left=0.08, right=0.95, wspace=0.4, hspace=0.7)


# -- Plots of sustained bandwidth tuning --
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
    panelLabels = ['a', 'b', 'c']
    
    for indCell, responseByCell in enumerate(sustainedResponses):
        plt.hold(1)
        axCurve = plt.subplot(gs[2*indCell:2*indCell+2,0])
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
        axCurve.annotate(panelLabels[indCell], xy=(labelPosX[0],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
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
            bandLabels[1::2] = ['']*len(bands[1::2]) #remove every other label so x axis less crowded
            axCurve.set_xticklabels(bandLabels)
            plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(-0.1,7) #expand x axis so you don't have dots on y axis

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
    
    panelLabel = 'd'
    
    axScatter = plt.subplot(gs[:3,1])
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
    
#     bplot = plt.boxplot(sustainedSuppressionVals, widths=0.6, showfliers=False)
#     
#     for box in range(len(bplot['boxes'])):
#         plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
#         plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
#         plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
#         plt.setp(bplot['medians'][box], color='k', linewidth=2)
#         #plt.setp(bplot['fliers'][box, marker='o', color=cellTypeColours[box]])
# 
#     plt.setp(bplot['medians'], color='k')   
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(sustainedSuppressionVals)+1)
    plt.ylim(-0.05,1.05)
    plt.ylabel('Suppression Index',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(sustainedSuppressionVals)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
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
if PANELS[2]:
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
    
    panelLabel = 'e'
    
    axScatter = plt.subplot(gs[3:,1])
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
    
    axScatter.annotate(panelLabel, xy=(labelPosX[1],labelPosY[3]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0,len(prefBandwidths)+1)
    plt.ylim(-0.05,7)
    plt.ylabel('Preferred bandwidth (oct)',fontsize=fontSizeLabels)
    axScatter.set_xticks(range(1,len(prefBandwidths)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels)
    axScatter.set_yticks(bands)
#     bandLabels = possibleBands.tolist()
#     bandLabels[-1] = 'WN'
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