import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots


import figparams
reload(figparams)


FIGNAME = 'figure_inhibitory_cell_inactivation'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig_effect_of_inhibitory_inactivation_on_suppression_pure_tone' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [5,6] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.53]   # Horiz position for panel labels
labelPosY = [0.96, 0.48]    # Vert position for panel labels


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,2,width_ratios=[1,0.7])
gs.update(top=0.95, left=0.1, right=0.95, wspace=0.6, hspace=0.2)

#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-16_1000um_T2_c4.npz'
#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-16_1400um_T4_c6.npz'
exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-20_1200um_T6_c4.npz'
#exampleNoSOM = 'example_SOM_inactivation_band073_2018-09-14_1200um_T1_c6.npz'

#exampleNoPV = 'example_PV_inactivation_band056_2018-03-23_1300um_T2_c4.npz'
#exampleNoPV = 'example_PV_inactivation_band062_2018-05-24_1300um_T2_c2.npz'
exampleNoPV = 'example_PV_inactivation_band062_2018-05-25_1250um_T4_c2.npz'

summaryFileName = 'all_inactivated_cells_stats.npz'

# --- Plot of bandwidth tuning with and without laser ---
if PANELS[0]:
    exampleCells = [exampleNoPV, exampleNoSOM]
    figLegends = ['No PV', 'No SOM']
    
    excColour = figparams.colp['excitatoryCell']
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    colours = [[excColour, PVcolour],[excColour, SOMcolour]]
    lineType = ['-', '--']
        
    panelLabels = ['a', 'b']
    
    for indCell, cell in enumerate(exampleCells):
        exampleDataFullPath = os.path.join(dataDir,cell)
        exampleData = np.load(exampleDataFullPath)
        
        sustainedResponseArray = exampleData['sustainedResponseArray']
        sustainedSEM = exampleData['sustainedSEM']
        baseline = sustainedResponseArray[0]
    
        bands = exampleData['possibleBands']
        laserTrials = exampleData['possibleLasers']
        bandLabels = ['{}'.format(band) for band in np.unique(bands)]
        
        fitBands = exampleData['fitBands']
        fitResponseNoLaser = exampleData['fitResponsePureToneNoLaser']
        fitResponseLaser = exampleData['fitResponsePureToneLaser']
        fits = [fitResponseNoLaser, fitResponseLaser]
        
        lines = []
        SIs = [float(exampleData['suppIndPureToneNoLaser']), float(exampleData['suppIndPureToneLaser'])]
        
        plt.hold(1)
        axCurve = plt.subplot(gs[indCell,0])
        axCurve.set_xscale('symlog', basex=2, linthreshx=0.25, linscalex=0.5)
        for laser in laserTrials:
            thisResponse = sustainedResponseArray[:,laser].flatten()
            thisSEM = sustainedSEM[:,laser].flatten()
            plt.plot(bands, thisResponse, 'o', ms=5,
                     color=colours[indCell][laser], mec=colours[indCell][laser], clip_on=False)
            plt.errorbar(bands, thisResponse, yerr = [thisSEM, thisSEM], 
                         fmt='none', ecolor=colours[indCell][laser])
            line, = plt.plot(fitBands, fits[laser], lineType[laser], lw=1.5, color=colours[indCell][laser])
            lines.append(line)
        #plt.legend([lines[-1],lines[0]],['{}, SI = {:.2f}'.format(figLegends[indCell], SIs[1]),'Control, SI = {:.2f}'.format(SIs[0])], loc='best', frameon=False, fontsize=fontSizeLabels)
        plt.legend([lines[-1],lines[0]],[figLegends[indCell],'Control'], loc='best', frameon=False, fontsize=fontSizeLabels)
        axCurve.annotate(panelLabels[indCell], xy=(labelPosX[0],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axCurve.set_ylim(bottom=0)
        axCurve.set_xticks(bands[1:])
        axCurve.tick_params(top=False, right=False, which='both')
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        if not indCell:
            axCurve.set_xticklabels('')
        if indCell:
            axCurve.set_xticks(bands)
            bands = bands.tolist()
            bands[-1] = 'WN'
            bands[1::2] = ['']*len(bands[1::2]) #remove every other label so x axis less crowded
            axCurve.set_xticklabels(bands)
            plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(-0.1,7) #expand x axis so you don't have dots on y axis
        
if PANELS[1]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppressionNoLaser = summaryData['fitPVsustainedSuppressionPureToneNoLaser']
    PVsustainedSuppressionLaser = summaryData['fitPVsustainedSuppressionPureToneLaser']
    
    SOMsustainedSuppressionNoLaser = summaryData['fitSOMsustainedSuppressionPureToneNoLaser']
    SOMsustainedSuppressionLaser = summaryData['fitSOMsustainedSuppressionPureToneLaser']
    
    noPVsupDiff = PVsustainedSuppressionLaser-PVsustainedSuppressionNoLaser
    noSOMsupDiff = SOMsustainedSuppressionLaser-SOMsustainedSuppressionNoLaser
    
    panelLabel = 'c'
    
    cellLabels = ['no PV', 'no SOM']
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    supDiffs = [noPVsupDiff, noSOMsupDiff]
    
    axBar = plt.subplot(gs[0,1])
    
    width = 0.7
    ind = np.arange(2)
    SIMeans = [np.mean(noPVsupDiff), np.mean(noSOMsupDiff)]
    SISEMs = [stats.sem(noPVsupDiff), stats.sem(noSOMsupDiff)]
    barPlot = axBar.bar(ind, SIMeans, width, edgecolor=[PVcolour,SOMcolour], color='none', linewidth=3)
    plt.plot([-5,5],[0,0],'k-',zorder=-10)
    plt.errorbar(ind+width/2, SIMeans, yerr = [SISEMs, SISEMs], 
                     fmt='none', ecolor=PVcolour, lw=1.5, capsize=5)
    
#     plt.hold(True)
#     bplot = plt.boxplot(supDiffs, widths=0.6, showfliers=False)
#      
#     for box in range(len(bplot['boxes'])):
#         plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
#         plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
#         plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
#         plt.setp(bplot['medians'][box], color='k', linewidth=2)
#  
#     plt.setp(bplot['medians'], color='k')
#     axBox.set_xticks([1,2])
#     axBox.set_xticklabels(cellLabels)

    plt.xlim(-0.2, 1.9)
    axBar.set_xticks(ind + width/2)
    axBar.set_xticklabels(cellLabels)
    yLims = (-0.15, 0.1)
    plt.ylim(yLims)
    extraplots.significance_stars([width/2,1+width/2], yLims[1]*0.92, yLims[1]*0.07, gapFactor=0.2)
    extraplots.boxoff(axBar)
    plt.ylabel('Change in suppression index',fontsize=fontSizeLabels)
    
    axBar.annotate(panelLabel, xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')

if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVpeakChange = summaryData['fitMeanPVpeakChangePureTone']
    PVWNChange = summaryData['fitMeanPVWNChangePureTone']
    
    semPVpeakChange = summaryData['fitSemPVpeakChangePureTone']
    semPVWNChange = summaryData['fitSemPVWNChangePureTone']
    
    SOMpeakChange = summaryData['fitMeanSOMpeakChangePureTone']
    SOMWNChange = summaryData['fitMeanSOMWNChangePureTone']
    
    semSOMpeakChange = summaryData['fitSemSOMpeakChangePureTone']
    semSOMWNChange = summaryData['fitSemSOMWNChangePureTone']
    
    cellLabels = ['no PV', 'no SOM']
    cellColours = [PVcolour, SOMcolour]
    
    panelLabel = 'd'
    
    axBar = plt.subplot(gs[1,1])
    
    plt.hold(True)
    ind = np.arange(2)
    width = 0.4
    peakMeans = [PVpeakChange, SOMpeakChange]
    peakSEMs = [semPVpeakChange, semSOMpeakChange]
    peakPlot = axBar.bar(ind, peakMeans, width, color=cellColours, edgecolor='none')
    plt.errorbar(ind+width/2, peakMeans, yerr = [peakSEMs, peakSEMs], 
                     fmt='none', ecolor=PVcolour, lw=1.5, capsize=5)

    WNMeans = [PVWNChange, SOMWNChange]
    WNSEMs = [semPVWNChange, semSOMWNChange]
    WNPlot = axBar.bar(ind+width, WNMeans, width, edgecolor=cellColours, color='none', linewidth=3)
    plt.errorbar(ind+3*width/2, WNMeans, yerr = [WNSEMs, WNSEMs], 
                     fmt='none', ecolor=PVcolour, lw=1.5, capsize=5)

    axBar.set_xticks(ind + width)
    axBar.set_xticklabels(cellLabels)

    extraplots.boxoff(axBar)
    
    axBar.legend((peakPlot, WNPlot), ('peak', 'WN'), loc='upper left', frameon=False, fontsize=fontSizeLabels, handlelength=0.6) 
    plt.ylabel('Change in firing rate')
    plt.xlim(-0.1,1.9)
    
    yLims = (0,3.5)
    plt.ylim(yLims)
    extraplots.new_significance_stars([width/2,3*width/2], yLims[1]*0.5, yLims[1]*0.03, starMarker='n.s.', fontSize=10, gapFactor=0.3)
    extraplots.significance_stars([1+width/2,1+3*width/2], yLims[1]*0.92, yLims[1]*0.03, gapFactor=0.2)
    
    axBar.annotate(panelLabel, xy=(labelPosX[1],labelPosY[1]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)