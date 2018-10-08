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


FIGNAME = 'figure_inhibitory_cell_inactivation'
#dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', FIGNAME)

PANELS = [1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
#outputDir = '/tmp/'
outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'effect_of_inhibitory_inactivation_on_suppression' # Do not include extension
#figFormat = 'pdf' # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [12,7] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.02, 0.24, 0.48, 0.72]   # Horiz position for panel labels
labelPosY = [0.96, 0.47]    # Vert position for panel labels


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(5,4,width_ratios=[1,1,1.3,1.3], height_ratios=[1,1,0.4,1,1])
gs.update(top=0.95, left=0.1, right=0.95, wspace=0.5, hspace=0.2)

#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-16_1000um_T2_c4.npz'
#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-16_1400um_T4_c6.npz'
#exampleNoSOM = 'example_SOM_inactivation_band055_2018-03-20_1200um_T6_c4.npz'
exampleNoSOM = 'example_SOM_inactivation_band073_2018-09-14_1200um_T1_c6.npz'

#exampleNoPV = 'example_PV_inactivation_band056_2018-03-23_1300um_T2_c4.npz'
exampleNoPV = 'example_PV_inactivation_band062_2018-05-24_1300um_T2_c2.npz'
#exampleNoPV = 'example_PV_inactivation_band062_2018-05-25_1250um_T4_c2.npz'

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
        
        fitBands = exampleData['fitBands']
        fitResponseNoLaser = exampleData['fitResponseNoLaser']
        fitResponseLaser = exampleData['fitResponseLaser']
        fits = [fitResponseNoLaser, fitResponseLaser]
        
        lines = []
        SIs = [float(exampleData['suppIndNoLaser']), float(exampleData['suppIndLaser'])]
        print SIs
        
        plt.hold(1)
        axCurve = plt.subplot(gs[2*indCell+indCell:2*indCell+2+indCell,2])
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
        axCurve.annotate(panelLabels[indCell], xy=(labelPosX[2],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        axCurve.set_ylim(bottom=0)
        axCurve.set_xticks(bands)
        axCurve.tick_params(top=False, right=False, which='both')
        extraplots.boxoff(axCurve)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
#         if not indCell:
#             axCurve.set_xticklabels('')
#         if indCell:
            #axCurve.set_xticks(bands)
        bands = bands.tolist()
        bands[-1] = 'WN'
        bands[1::2] = ['']*len(bands[1::2]) #remove every other label so x axis less crowded
        axCurve.set_xticklabels(bands)
        #plt.xticks(rotation=-45)
        plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.xlim(-0.1,7) #expand x axis so you don't have dots on y axis
        
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVsustainedSuppressionNoLaser = summaryData['fitPVsustainedSuppressionNoLaser']
    PVsustainedSuppressionLaser = summaryData['fitPVsustainedSuppressionLaser']
    
    SOMsustainedSuppressionNoLaser = summaryData['fitSOMsustainedSuppressionNoLaser']
    SOMsustainedSuppressionLaser = summaryData['fitSOMsustainedSuppressionLaser']
    
    noPVsupDiff = PVsustainedSuppressionLaser-PVsustainedSuppressionNoLaser
    noSOMsupDiff = SOMsustainedSuppressionLaser-SOMsustainedSuppressionNoLaser
    
    panelLabel = 'g'
    
    cellLabels = ['no PV', 'no SOM']
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    supDiffs = [noPVsupDiff, noSOMsupDiff]
    
    axViolin = plt.subplot(gs[:2,3])
    
    plt.hold(True)
    
    bplot = plt.boxplot(supDiffs, widths=0.6, showfliers=False)
    
    for box in range(len(bplot['boxes'])):
        plt.setp(bplot['boxes'][box], color=cellTypeColours[box])
        plt.setp(bplot['whiskers'][2*box:2*(box+1)], linestyle='-', color=cellTypeColours[box])
        plt.setp(bplot['caps'][2*box:2*(box+1)], color=cellTypeColours[box])
        plt.setp(bplot['medians'][box], color='k', linewidth=2)

    plt.setp(bplot['medians'], color='k')
    
#     for category in range(len(supDiffs)):
#         edgeColour = matplotlib.colors.colorConverter.to_rgba(cellTypeColours[category], alpha=0.5)
#         xval = (category+1)*np.ones(len(supDiffs[category]))
#          
#         jitterAmt = np.random.random(len(xval))
#         xval = xval + (0.4 * jitterAmt) - 0.2
#          
#         plt.hold(True)
#         plt.plot(xval, supDiffs[category], 'o', mec=edgeColour, mfc='none', clip_on=False)
#         median = np.median(supDiffs[category])
#         #sem = stats.sem(vals[category])
#         plt.plot([category+0.7,category+1.3], [median,median], '-', color='k', mec=cellTypeColours[category], lw=3)
#         plt.ylabel('Change in Suppression Index',fontsize=fontSizeLabels)
    
#     parts = plt.violinplot([noPVsupDiff, noSOMsupDiff], widths=0.9, points=500, showextrema=False)
#     PVmedian = np.median(noPVsupDiff)
#     SOMmedian = np.median(noSOMsupDiff)
#     plt.plot([0.7, 1.3], [PVmedian,PVmedian], '-', color='k', lw=2)
#     plt.plot([1.7, 2.3], [SOMmedian,SOMmedian], '-', color='k', lw=2)
#     for ind,pc in enumerate(parts['bodies']):
#         pc.set_facecolor(cellTypeColours[ind])
#         pc.set_edgecolor(cellTypeColours[ind])
#         pc.set_alpha(0.8)
    axViolin.annotate(panelLabel, xy=(labelPosX[3],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    axViolin.set_xticks([1,2])
    axViolin.set_xticklabels(cellLabels)
    yLims = np.array(plt.ylim())
    extraplots.significance_stars([1,2], yLims[1]*1.15, yLims[1]*0.05, gapFactor=0.2)
    extraplots.boxoff(axViolin)
    #plt.ylim(-1.05,1.05)
    plt.ylabel('Change in suppression index',fontsize=fontSizeLabels)
    
if PANELS[3]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    PVpeakChangeFR = summaryData['fitPVpeakChangeFR']
    PVWNChangeFR = summaryData['fitPVWNChangeFR']
    
    SOMpeakChangeFR = summaryData['fitSOMpeakChangeFR']
    SOMWNChangeFR = summaryData['fitSOMWNChangeFR']
    
    panelLabel = 'h'
    
    PVcolour = figparams.colp['PVcell']
    SOMcolour = figparams.colp['SOMcell']
    cellTypeColours = [PVcolour, SOMcolour]
    
    axScatter = plt.subplot(gs[3:,3])
    
    plt.hold(True)
    plt.plot([-20,30],[-20,30], 'k--')
    l2, = plt.plot(SOMpeakChangeFR,SOMWNChangeFR, 'o', color=SOMcolour, mec='none', ms=4)
    l1, = plt.plot(PVpeakChangeFR,PVWNChangeFR, 'o', color=PVcolour, mec='none', ms=4)
    plt.ylabel('Change in response to WN (spk/s)',fontsize=fontSizeLabels)
    plt.xlabel('Change in response to \n preferred bandwidth (spk/s)',fontsize=fontSizeLabels)
    plt.xlim(-5,10)
    plt.ylim(-5,10)
#     plt.xlim(-10,22)
#     plt.ylim(-10,22)
    plt.legend([l1,l2], ['No PV', 'No SOM'], loc='best', fontsize=fontSizeLabels, numpoints=1, handlelength=0.3)
    axScatter.annotate(panelLabel, xy=(labelPosX[3],labelPosY[1]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    extraplots.boxoff(axScatter)

    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)