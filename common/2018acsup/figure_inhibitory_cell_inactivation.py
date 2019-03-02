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

PANELS = [1,1,1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'effect_of_inhibitory_inactivation_on_suppression' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [12,7] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.2, 0.4, 0.59, 0.78]   # Horiz position for panel labels
labelPosY = [0.96, 0.48]    # Vert position for panel labels


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(5,5,width_ratios=[1,1,1.3,1,1.3], height_ratios=[1,1,0.4,1,1])
gs.update(top=0.95, left=0.1, right=0.95, wspace=0.6, hspace=0.2)

#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-16_1000um_T2_c4.npz'
#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-16_1400um_T4_c6.npz'
exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-20_1200um_T6_c4.npz'
#exampleNoSOM = 'example_SOM_inactivation_band073_2018-09-14_1200um_T1_c6.npz'

#exampleNoPV = 'example_PV_inactivation_band056_2018-03-23_1300um_T2_c4.npz'
#exampleNoPV = 'example_PV_inactivation_band062_2018-05-24_1300um_T2_c2.npz'
exampleNoPV = 'example_PV_inactivation_band062_2018-05-25_1250um_T4_c2.npz'

summaryFileName = 'all_inactivated_cells_stats.npz'

# --- Raster plots of sound response with and without laser ---
if PANELS[0]:
    exampleCells = [exampleNoPV, exampleNoSOM]
    
    PVcolour = figparams.colp['PVcell']
    PVlite = figparams.colp['PVerror']
    SOMcolour = figparams.colp['SOMcell']
    SOMlite = figparams.colp['SOMerror']
    
    cellColours = [[PVcolour, PVlite],[SOMcolour, SOMlite]]
    
    panelLabels = ['b', 'e']
    
    for indCell, cell in enumerate(exampleCells):
        exampleDataFullPath = os.path.join(dataDir,cell)
        exampleData = np.load(exampleDataFullPath)
        colours = [['k','0.5'], cellColours[indCell]]
        possibleBands = exampleData['possibleBands']
        bandLabels = possibleBands.tolist()
        bandLabels[-1] = 'WN'
        
        laserTrials = exampleData['possibleLasers']
        for laser in laserTrials:
            axRaster = plt.subplot(gs[laser+2*indCell+indCell,1])
            colorEachCond = np.tile(colours[laser], len(possibleBands)/2+1)
            pRaster, hcond, zline = extraplots.raster_plot(exampleData['spikeTimesFromEventOnset'],
                                                       exampleData['indexLimitsEachTrial'],
                                                       exampleData['timeRange'],
                                                       trialsEachCond=exampleData['trialsEachCond'][:,1:,laser],
                                                       labels=bandLabels[1:],
                                                       colorEachCond=colorEachCond)
            plt.setp(pRaster, ms=3)
            plt.ylabel('Bandwidth (oct)', fontsize=fontSizeLabels)
            if not laser:
                axRaster.set_xticklabels('')
            if laser:
                yLims = np.array(plt.ylim())
                rect = patches.Rectangle((-0.1,yLims[1]*1.03),1.3,yLims[1]*0.08,linewidth=1,edgecolor='0.5',facecolor='0.5',clip_on=False)
                axRaster.add_patch(rect)
        plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
        axRaster.annotate(panelLabels[indCell], xy=(labelPosX[1],labelPosY[indCell]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        
    #also do the panel labels for the cartoons in here I guess
    cartoonPanels = ['a', 'd']
    for indPanel, panel in enumerate(cartoonPanels):
        axRaster.annotate(panel, xy=(labelPosX[0],labelPosY[indPanel]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')


# --- Plot of bandwidth tuning with and without laser ---
if PANELS[1]:
    exampleCells = [exampleNoPV, exampleNoSOM]
    figLegends = ['No PV', 'No SOM']
    
    excColour = figparams.colp['excitatoryCell']
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    colours = [[excColour, PVcolour],[excColour, SOMcolour]]
    lineType = ['-', '--']
        
    panelLabels = ['c', 'f']
    
    for indCell, cell in enumerate(exampleCells):
        exampleDataFullPath = os.path.join(dataDir,cell)
        exampleData = np.load(exampleDataFullPath)
        
        sustainedResponseArray = exampleData['sustainedResponseArray']
        sustainedSEM = exampleData['sustainedSEM']
        baseline = sustainedResponseArray[0]
    
        bands = exampleData['possibleBands']
        laserTrials = exampleData['possibleLasers']
        bandLabels = ['{}'.format(band) for band in np.unique(possibleBands)]
        
        fitBands = exampleData['fitBandsNoZero']
        fitResponseNoLaser = exampleData['fitResponseNoZeroNoLaser']
        fitResponseLaser = exampleData['fitResponseNoZeroLaser']
        fits = [fitResponseNoLaser, fitResponseLaser]
        
        lines = []
        SIs = [float(exampleData['suppIndNoZeroNoLaser']), float(exampleData['suppIndNoZeroLaser'])]
        
        plt.hold(1)
        axCurve = plt.subplot(gs[2*indCell+indCell:2*indCell+2+indCell,2])
        axCurve.set_xscale('log', basex=2)
        for laser in laserTrials:
            thisResponse = sustainedResponseArray[:,laser].flatten()
            thisSEM = sustainedSEM[:,laser].flatten()
            plt.plot(bands[1:], thisResponse[1:], 'o', ms=5,
                     color=colours[indCell][laser], mec=colours[indCell][laser], clip_on=False)
            plt.errorbar(bands[1:], thisResponse[1:], yerr = [thisSEM[1:], thisSEM[1:]], 
                         fmt='none', ecolor=colours[indCell][laser])
            line, = plt.plot(fitBands, fits[laser], lineType[laser], lw=1.5, color=colours[indCell][laser])
            lines.append(line)
        #plt.legend([lines[-1],lines[0]],['{}, SI = {:.2f}'.format(figLegends[indCell], SIs[1]),'Control, SI = {:.2f}'.format(SIs[0])], loc='best', frameon=False, fontsize=fontSizeLabels)
        plt.legend([lines[-1],lines[0]],[figLegends[indCell],'Control'], loc='best', frameon=False, fontsize=fontSizeLabels)
        axCurve.annotate(panelLabels[indCell], xy=(labelPosX[2],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axCurve.set_ylim(bottom=0)
        axCurve.set_xticks(bands[1:])
        axCurve.tick_params(top=False, right=False, which='both')
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
#         if not indCell:
#             axCurve.set_xticklabels('')
#         if indCell:
            #axCurve.set_xticks(bands)
        bands = bands.tolist()
        bands[-1] = 'WN'
        #bands[1::2] = ['']*len(bands[1::2]) #remove every other label so x axis less crowded
        axCurve.set_xticklabels(bands[1:])
        #plt.xticks(rotation=-45)
        plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(0.2,7) #expand x axis so you don't have dots on y axis
        
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppressionNoLaser = summaryData['fitPVsustainedSuppressionNoZeroNoLaser']
    PVsustainedSuppressionLaser = summaryData['fitPVsustainedSuppressionNoZeroLaser']
    
    SOMsustainedSuppressionNoLaser = summaryData['fitSOMsustainedSuppressionNoZeroNoLaser']
    SOMsustainedSuppressionLaser = summaryData['fitSOMsustainedSuppressionNoZeroLaser']
    
    noPVsupDiff = PVsustainedSuppressionLaser-PVsustainedSuppressionNoLaser
    noSOMsupDiff = SOMsustainedSuppressionLaser-SOMsustainedSuppressionNoLaser
    
    panelLabel = 'g'
    
    cellLabels = ['no PV', 'no SOM']
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    supDiffs = [noPVsupDiff, noSOMsupDiff]
    
    axBar = plt.subplot(gs[:2,3])
    
    width = 0.7
    ind = np.arange(2)
    SIMeans = [np.mean(noPVsupDiff), np.mean(noSOMsupDiff)]
    SISEMs = [stats.sem(noPVsupDiff), stats.sem(noSOMsupDiff)]
    barPlot = axBar.bar(ind, SIMeans, width, edgecolor=[PVcolour,SOMcolour], color='none', linewidth=3)
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
    yLims = (-0.12, 0.1)
    plt.ylim(yLims)
    extraplots.significance_stars([width/2,1+width/2], yLims[1]*0.92, yLims[1]*0.07, gapFactor=0.2)
    extraplots.boxoff(axBar)
    plt.ylabel('Change in suppression index',fontsize=fontSizeLabels)
    
    axBar.annotate(panelLabel, xy=(labelPosX[3],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')

if PANELS[3]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVpeakChange = summaryData['fitMeanPVpeakChangeNoZero']
    PVWNChange = summaryData['fitMeanPVWNChangeNoZero']
    
    semPVpeakChange = summaryData['fitSemPVpeakChangeNoZero']
    semPVWNChange = summaryData['fitSemPVWNChangeNoZero']
    
    SOMpeakChange = summaryData['fitMeanSOMpeakChangeNoZero']
    SOMWNChange = summaryData['fitMeanSOMWNChangeNoZero']
    
    semSOMpeakChange = summaryData['fitSemSOMpeakChangeNoZero']
    semSOMWNChange = summaryData['fitSemSOMWNChangeNoZero']
    
    cellLabels = ['no PV', 'no SOM']
    cellColours = [PVcolour, SOMcolour]
    
    panelLabel = 'h'
    
    axBar = plt.subplot(gs[3:,3])
    
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
    
    axBar.annotate(panelLabel, xy=(labelPosX[3],labelPosY[1]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')

if PANELS[4]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppressionNoLaser = summaryData['fitPVsustainedSuppressionNoZeroNoLaser']
    PVsustainedSuppressionLaser = summaryData['fitPVsustainedSuppressionNoZeroLaser']
    
    SOMsustainedSuppressionNoLaser = summaryData['fitSOMsustainedSuppressionNoZeroNoLaser']
    SOMsustainedSuppressionLaser = summaryData['fitSOMsustainedSuppressionNoZeroLaser']

    PVsupNoLaser = summaryData['fitMeanPVsupNoZeroNoLaser']
    PVsupLaser = summaryData['fitMeanPVsupNoZeroLaser']
    
    semPVsupNoLaser = summaryData['fitSemPVsupNoZeroNoLaser']
    semPVsupLaser = summaryData['fitSemPVsupNoZeroLaser']
    
    SOMsupNoLaser = summaryData['fitMeanSOMsupNoZeroNoLaser']
    SOMsupLaser = summaryData['fitMeanSOMsupNoZeroLaser']
    
    semSOMsupNoLaser = summaryData['fitSemSOMsupNoZeroNoLaser']
    semSOMsupLaser = summaryData['fitSemSOMsupNoZeroLaser']
    
    panelLabel = 'i'
    
    cellLabels = ['no PV', 'no SOM']
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    axScatter = plt.subplot(gs[:2,4])
    
    plt.hold(True)
    plt.plot([-2,2],[-2,2], 'k--')
    l2, = plt.plot(SOMsustainedSuppressionNoLaser,SOMsustainedSuppressionLaser, 'o', color=SOMcolour, mec='none', ms=4)
    plt.errorbar(SOMsupNoLaser, SOMsupLaser, xerr = [[semSOMsupNoLaser, semSOMsupNoLaser]], yerr = [[semSOMsupLaser, semSOMsupLaser]], fmt='none', ecolor=SOMcolour, capsize=0, lw=2)
    l1, = plt.plot(PVsustainedSuppressionNoLaser,PVsustainedSuppressionLaser, 'o', color=PVcolour, mec='none', ms=4)
    plt.errorbar(PVsupNoLaser, PVsupLaser, xerr = [[semPVsupNoLaser, semPVsupNoLaser]], yerr = [[semPVsupLaser, semPVsupLaser]], fmt='none', ecolor=PVcolour, capsize=0, lw=2)
    plt.ylabel('Suppression Index (laser)',fontsize=fontSizeLabels)
    plt.xlabel('Suppression Index (control)',fontsize=fontSizeLabels)
    plt.xlim(-0.1,1.1)
    plt.ylim(-0.1,1.1)

    plt.legend([l1,l2], ['No PV', 'No SOM'], loc='upper left', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3)

    extraplots.boxoff(axScatter)

    axScatter.annotate(panelLabel, xy=(labelPosX[4],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    
    # compute stats and print in terminal
    noPV = stats.wilcoxon(PVsustainedSuppressionNoLaser,PVsustainedSuppressionLaser)[1]
    noSOM = stats.wilcoxon(SOMsustainedSuppressionNoLaser, SOMsustainedSuppressionLaser)[1]
    print "Change in SI p values:\nno PV: {0}\nno SOM: {1}".format(noPV,noSOM)
    
if PANELS[5]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVpeakChangeFR = summaryData['fitPVpeakChangeFRNoZero']
    PVWNChangeFR = summaryData['fitPVWNChangeFRNoZero']
    
    SOMpeakChangeFR = summaryData['fitSOMpeakChangeFRNoZero']
    SOMWNChangeFR = summaryData['fitSOMWNChangeFRNoZero']
    
    PVpeakChange = summaryData['fitMeanPVpeakChangeNoZero']
    PVWNChange = summaryData['fitMeanPVWNChangeNoZero']
    
    semPVpeakChange = summaryData['fitSemPVpeakChangeNoZero']
    semPVWNChange = summaryData['fitSemPVWNChangeNoZero']
    
    SOMpeakChange = summaryData['fitMeanSOMpeakChangeNoZero']
    SOMWNChange = summaryData['fitMeanSOMWNChangeNoZero']
    
    semSOMpeakChange = summaryData['fitSemSOMpeakChangeNoZero']
    semSOMWNChange = summaryData['fitSemSOMWNChangeNoZero']
    
    panelLabel = 'j'
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    axScatter = plt.subplot(gs[3:,4])
    
    plt.hold(True)
    plt.plot([-20,30],[-20,30], 'k--')
    l2, = plt.plot(SOMpeakChangeFR,SOMWNChangeFR, 'o', color=SOMcolour, mec='none', ms=4)
    plt.errorbar(SOMpeakChange, SOMWNChange, xerr = [[semSOMpeakChange, semSOMpeakChange]], yerr = [[semSOMWNChange, semSOMWNChange]], fmt='none', ecolor=SOMcolour, capsize=0, lw=2, zorder=9)
    l1, = plt.plot(PVpeakChangeFR,PVWNChangeFR, 'o', color=PVcolour, mec='none', ms=4)
    plt.errorbar(PVpeakChange, PVWNChange, xerr = [[semPVpeakChange, semPVpeakChange]], yerr = [[semPVWNChange, semPVWNChange]], fmt='none', ecolor=PVcolour, capsize=0, lw=2, zorder=10)    
    plt.ylabel('Change in response to WN (spk/s)',fontsize=fontSizeLabels)
    plt.xlabel('Change in response to \n preferred bandwidth (spk/s)',fontsize=fontSizeLabels)
    plt.xlim(-5,8)
    plt.ylim(-5,8)
#     plt.xlim(-10,22)
#     plt.ylim(-10,22)
    plt.legend([l1,l2], ['No PV', 'No SOM'], loc='upper left', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3)
    axScatter.annotate(panelLabel, xy=(labelPosX[4],labelPosY[1]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axScatter)
    
    # compute stats and print in terminal
    noPV = stats.wilcoxon(PVpeakChangeFR,PVWNChangeFR)[1]
    noSOM = stats.wilcoxon(SOMpeakChangeFR, SOMWNChangeFR)[1]
    print "Change in peak  vs WN response p values:\nno PV: {0}\nno SOM: {1}".format(noPV,noSOM)
    
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)