import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from scipy import stats

from jaratoolbox import settings
from jaratoolbox import extraplots


import figparams

INACTFIGNAME = 'supplement_figure_cells_inactivated_by_archt'
inactDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, INACTFIGNAME)

CONTROLFIGNAME = 'supplement_figure_inhibitory_cell_inactivation_control'
controlDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, CONTROLFIGNAME)

PANELS = [1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'Fig6_inactivation_controls' # Do not include extension
#figFormat = 'pdf' # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [10,10] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.36, 0.66, 0.42]   # Horiz position for panel labels
labelPosY = [0.98, 0.78, 0.48, 0.28]    # Vert position for panel labels

PVFileName = 'example_PV_inactivated_sound_response_band062_2018-05-25_1450um_T5_c5.npz'
SOMFileName = 'example_SOM_inactivated_sound_response_band073_2018-09-14_1300um_T4_c4.npz'
summaryFileName = 'low_bandwidth_responses_during_inactivation.npz'
controlFileName = 'control_inactivated_cells_stats.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

laserColour = figparams.colp['greenLaser']
soundColour = figparams.colp['sound']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(4,3, width_ratios=[1.2,1,1], height_ratios=[0.7,1,0.7,1])
gs.update(top=0.99, bottom=0.05, left=0.07, right=0.94, wspace=0.5, hspace=0.3)

# --- suppressed responses of example cells ---
if PANELS[0]:
    exampleCells = [PVFileName, SOMFileName]
    
    cellColours = [PVColour, SOMColour]
    
    panelLabels = ['C', 'H']
    
    PSTHylims = [(-1, 47), (-0.4,16)]
    
    for indCell, cell in enumerate(exampleCells):
        axExample = gs[2*indCell+1, 0]
        
        exampleDataFullPath = os.path.join(inactDataDir,cell)
        exampleData = np.load(exampleDataFullPath)
        
        laserTrials = exampleData['possibleLasers']
        inner = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=axExample, wspace=0.1, hspace=0.34)
        for laser in laserTrials:
            axRaster = plt.subplot(inner[laser,0])
            trialsEachCond = exampleData['trialsEachCond'][:,laser]
            trialsEachCond = np.reshape(trialsEachCond, (len(trialsEachCond),1)) #for this to be a 2d array even though there's only one trial type
            pRaster, hcond, zline = extraplots.raster_plot(exampleData['spikeTimesFromEventOnset'],
                                                       exampleData['indexLimitsEachTrial'],
                                                       exampleData['rasterTimeRange'],
                                                       trialsEachCond=trialsEachCond)
            plt.setp(pRaster, ms=3)
            plt.locator_params(axis='y', nbins=4)
            
            axRaster.set_xticklabels('')
            
            while len(hcond)>0:
                bar=hcond.pop(0)
                bar.remove()
            
            yLims = np.array(plt.ylim())
            rect = patches.Rectangle((0.0,yLims[1]*1.06),1.0,yLims[1]*0.05,linewidth=1,edgecolor=soundColour,facecolor=soundColour,clip_on=False)
            axRaster.add_patch(rect)
            
            if laser:
                yLims = np.array(plt.ylim())
                rect = patches.Rectangle((-0.1,yLims[1]*1.16),1.3,yLims[1]*0.05,linewidth=1,edgecolor=laserColour,facecolor=laserColour,clip_on=False)
                axRaster.add_patch(rect)
#             else:
#                 axRaster.set_xticklabels('')
        
        axPSTH = plt.subplot(inner[2,0])
         
        binStartTimes = exampleData['PSTHbins']
        controlPSTH = exampleData['controlPSTH']
        laserPSTH = exampleData['laserPSTH']
  
        #smooth PSTH
        smoothWinSize = 2
        winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))) # Square (causal)
        winShape = winShape/np.sum(winShape)
        controlPSTHSmooth = np.convolve(controlPSTH,winShape,mode='same')
        laserPSTHSmooth = np.convolve(laserPSTH,winShape,mode='same')
        
        controlPSTHSmooth[:smoothWinSize] = controlPSTH[:smoothWinSize]
        laserPSTHSmooth[:smoothWinSize] = laserPSTH[:smoothWinSize]
         
        plt.hold(1)
        l1, = plt.plot(binStartTimes,controlPSTHSmooth,color=ExcColour, lw=2)
        l2, = plt.plot(binStartTimes,laserPSTHSmooth,color=cellColours[indCell], lw=2)
        plt.legend([l1,l2],['control', 'laser'], bbox_to_anchor=(1.0, 1.35), frameon=False, fontsize=fontSizeLegend, ncol=2)
        zline = plt.axvline(0,color='0.75',zorder=-10)
        plt.ylim(PSTHylims[indCell])
        plt.locator_params(axis='y', nbins=4)
        plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
        plt.ylabel('Firing rate \n(spk/s)', fontsize=fontSizeLabels)
        extraplots.boxoff(axPSTH)
         
        # set common y label for two rasters
        plt.gcf().add_subplot(inner[:-1,0], frameon=False)
        plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
        plt.ylabel("Trial", fontsize=fontSizeLabels)

        axRaster.annotate(panelLabels[indCell], xy=(labelPosX[0],labelPosY[2*indCell+1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        
        # make panel labels for histology
        cartoonLabels = ['A', 'F']
        for ind, label in enumerate(cartoonLabels):
            axRaster.annotate(label, xy=(labelPosX[0],labelPosY[2*ind]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
            
        cartoonLabels = ['B', 'G']
        for ind, label in enumerate(cartoonLabels):
            axRaster.annotate(label, xy=(labelPosX[3],labelPosY[2*ind]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        
# --- plots of cells immediately suppressed and their sustained suppression
if PANELS[1]:
    summaryDataFullPath = os.path.join(inactDataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    cellColours = [PVColour, SOMColour]
    
    panelLabels = ['D', 'I']
    
    PVcontrolResponses = summaryData['PVcontrolResponses']
    PVlaserResponses = summaryData['PVlaserResponses']
    PVchangeSoundResponse = PVlaserResponses-PVcontrolResponses
    
    SOMcontrolResponses = summaryData['SOMcontrolResponses']
    SOMlaserResponses = summaryData['SOMlaserResponses']
    SOMchangeSoundResponse = SOMlaserResponses-SOMcontrolResponses
    
    PVcontrolLaserOnsets = summaryData['PVcontrolLaserOnset']
    PVlaserOnsets = summaryData['PVlaserOnset']
    PVchangeLaserOnsetResponse = PVlaserOnsets-PVcontrolLaserOnsets
    
    SOMcontrolLaserOnsets = summaryData['SOMcontrolLaserOnset']
    SOMlaserOnsets = summaryData['SOMlaserOnset']
    SOMchangeLaserOnsetResponse = SOMlaserOnsets-SOMcontrolLaserOnsets
    
    PVpVals = summaryData['PVpVals']
    SOMpVals = summaryData['SOMpVals']
    
    PVlaserOnsetpVals = summaryData['PVlaserOnsetpVals']
    SOMlaserOnsetpVals = summaryData['SOMlaserOnsetpVals']
    
    responses = [[PVchangeLaserOnsetResponse, PVchangeSoundResponse],[SOMchangeLaserOnsetResponse, SOMchangeSoundResponse]]
    #pVals = [PVpVals, SOMpVals]
    pVals = [PVlaserOnsetpVals, SOMlaserOnsetpVals]
    
    xRanges = [[-30,40],[-20,30]]
    yRanges = [[-40,30],[-20,30]]

#     xRanges = [[-40,0],[-20,0]]
#     yRanges = [[-40,0],[-20,0]]
    
    for indType, cellType in enumerate(responses):
        axScatter = plt.subplot(gs[2*indType+1, 1])
        
        plt.hold(True)
        
        sigCells = (pVals[indType]<0.05) & (cellType[0]<0)
        #sigCells = (pVals[indType]<0.05) & (cellType[1]<0)
        
        print np.sum(sigCells)
        
        plt.scatter(cellType[0][sigCells],cellType[1][sigCells], edgecolors=cellColours[indType], facecolors='none', s=15)
        #plt.scatter(cellType[0][sigCells],cellType[1][sigCells], marker='x', color='k', s=15, zorder=10)
        plt.scatter(cellType[0][~sigCells],cellType[1][~sigCells], edgecolors=cellColours[indType], facecolors=cellColours[indType], s=15)
        plt.ylabel('Laser sustained \n' r'response ($\Delta$spk/s)',fontsize=fontSizeLabels)
        plt.xlabel(r'Laser onset response ($\Delta$spk/s)',fontsize=fontSizeLabels)
        #axScatter.set_xscale('log', basex=10)
        #axScatter.set_yscale('log', basex=10)
        
        plt.plot([0,0],yRanges[indType], 'k--')
        plt.plot(xRanges[indType], [0,0], 'k--')
        
        plt.xlim(xRanges[indType])
        plt.ylim(yRanges[indType])
    
        axScatter.annotate(panelLabels[indType], xy=(labelPosX[1],labelPosY[2*indType+1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        extraplots.boxoff(axScatter)
        axScatter.set(adjustable='box-forced', aspect='equal')
        
if PANELS[2]:
    panelLabels = ['E', 'J']
    cellLabels = [r'no PV$^+$', r'no SOM$^+$']
    
    dataFullPath = os.path.join(controlDataDir,controlFileName)
    data = np.load(dataFullPath)
    
    PVNoLaser = data['PVNoLaser']
    PVLaser = data['PVLaser']
    noPVChange = 100.0*(PVLaser-PVNoLaser)/PVNoLaser
    
    # normalisation fails in some cases due to control firing rate being 0
    notNanInds = np.where(np.isfinite(noPVChange))
    noPVChange = noPVChange[notNanInds]
    
    controlPVNoLaser = data['PVControlNoLaser']
    controlPVLaser = data['PVControlLaser']
    controlPVChange = 100.0*(controlPVLaser-controlPVNoLaser)/controlPVNoLaser
    
    # normalisation fails in some cases due to control firing rate being 0
    notNanInds = np.where(np.isfinite(controlPVChange))
    controlPVChange = controlPVChange[notNanInds]
    
    SOMNoLaser = data['SOMNoLaser']
    SOMLaser = data['SOMLaser']
    noSOMChange = 100.0*(SOMLaser-SOMNoLaser)/SOMNoLaser
    
    # normalisation fails in some cases due to control firing rate being 0
    notNanInds = np.where(np.isfinite(noSOMChange))
    noSOMChange = noSOMChange[notNanInds]
    
    controlSOMNoLaser = data['SOMControlNoLaser']
    controlSOMLaser = data['SOMControlLaser']
    controlSOMChange = 100.0*(controlSOMLaser-controlSOMNoLaser)/controlSOMNoLaser
    
    # normalisation fails in some cases due to control firing rate being 0
    notNanInds = np.where(np.isfinite(controlSOMChange))
    controlSOMChange = controlSOMChange[notNanInds]
    
    noPVpVal = stats.ranksums((PVLaser-PVNoLaser), (controlPVLaser-controlPVNoLaser))[1]
    noSOMpVal = stats.ranksums((SOMLaser-SOMNoLaser), (controlSOMLaser-controlSOMNoLaser))[1]
    print "Laser vs. control change in FR p values:\nno PV: {0}\nno SOM: {1}".format(noPVpVal, noSOMpVal)
    
    
    cellTypeData = [[PVNoLaser, PVLaser], [SOMNoLaser, SOMLaser]]
    controlCellTypeData = [[controlPVNoLaser, controlPVLaser], [controlSOMNoLaser, controlSOMLaser]]
    cellTypeChangeData = [[noPVChange, controlPVChange],[noSOMChange, controlSOMChange]]
    cellTypeColours = [PVColour, SOMColour]
    
    yRanges = [[0,170],[-20,110]]
    for indType in range(2):
        axScatter = plt.subplot(gs[2*indType+1,2])
        
        laserData = cellTypeData[indType]
        controlData = controlCellTypeData[indType]
        changeData = cellTypeChangeData[indType]
        
        plt.hold(True)
        plt.scatter(laserData[0],laserData[1], edgecolors=cellTypeColours[indType], facecolors='none', s=15, label=cellLabels[indType])
        plt.scatter(controlData[0],controlData[1], edgecolors=ExcColour, facecolors=ExcColour, s=15, label='control')
        
        plt.xlabel('Spontaneous firing rate (spk/s)',fontsize=fontSizeLabels)
        plt.ylabel('Laser-evoked firing rate (spk/s)',fontsize=fontSizeLabels)
    
        plt.legend(scatterpoints=1, loc='upper left', fontsize=fontSizeLegend, numpoints=1, handlelength=0.3, markerscale=1.5)
#         plt.plot([-20,100],[-20,100], 'k--')
#         plt.xlim(-2,45)
#         plt.ylim(-2,55)

        axScatter.set_xscale('log', basex=10)
        axScatter.set_yscale('log', basey=10)
        
        plt.plot([-5,100], [-5,100], 'k--')
        plt.xlim(0.05,100)
        plt.ylim(0.05,100)
        axScatter.tick_params(top=False, right=False, which='both')
        
        ticks=[0.1,1,10,100]
        
        axScatter.set_xticks(ticks)
        axScatter.set_xticklabels(ticks)
        axScatter.set_yticks(ticks)
        axScatter.set_yticklabels(ticks)
     
        extraplots.boxoff(axScatter)
        axScatter.set(adjustable='box-forced', aspect='equal')
        
        axScatter.annotate(panelLabels[indType], xy=(labelPosX[2],labelPosY[2*indType+1]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        
        pControl = stats.wilcoxon(controlData[0],controlData[1])[1]
        pLaser = stats.wilcoxon(laserData[0],laserData[1])[1]
    
        print "Change in FR for {0} p values:\ncontrol: {1}\nlaser: {2}".format(cellLabels[indType],pControl,pLaser)
        
        axInset = inset_axes(axScatter, width="20%", height="30%", loc=4, bbox_to_anchor=(0.12, 0.02, 1, 1), bbox_transform=axScatter.transAxes)
        
        barWidth = 0.9
        xVals = np.arange(2)
        means = [np.mean(changeData[0]), np.mean(changeData[1])]
        SEMs = [stats.sem(changeData[0]), stats.sem(changeData[1])]
        axInset.bar(xVals, means, barWidth, color='none', edgecolor=[cellTypeColours[indType],ExcColour],linewidth=2)
        plt.errorbar(xVals[0]+barWidth/2, means[0], yerr = SEMs[0], fmt='none', ecolor=cellTypeColours[indType], lw=1, capsize=3)
        plt.errorbar(xVals[1]+barWidth/2, means[1], yerr = SEMs[1], fmt='none', ecolor=ExcColour, lw=1, capsize=3)
 
        axInset.set_xticks([])
#         axBar.set_xticklabels(cellLabels)#, rotation=-45)
        axInset.tick_params(axis='y', labelsize=fontSizeLegend)
        
        plt.xlim(-0.2,2.2)
        plt.ylim(yRanges[indType])

#         laserDiff = np.log2(laserData[0])-np.log2(laserData[1])
#         controlDiff = np.log2(controlData[0])-np.log2(controlData[1])
# 
#         laserDensity = stats.gaussian_kde(laserDiff[np.isfinite(laserDiff)])
#         controlDensity = stats.gaussian_kde(controlDiff[np.isfinite(controlDiff)])
#         xs = np.linspace(-5,5,200)
#         
# #         laserDensity.covariance_factor = lambda : .25
# #         laserDensity._compute_covariance()
# #         controlDensity.covariance_factor = lambda : .25
# #         controlDensity._compute_covariance()
#          
#         plt.plot(xs,laserDensity(xs),color=cellTypeColours[indType])
#         plt.plot(xs,controlDensity(xs),color=ExcColour)
    
        #extraplots.boxoff(axInset, keep='right')
        axInset.yaxis.tick_right()
        axInset.yaxis.set_ticks_position('right')
        plt.locator_params(axis='y', nbins=4)
        axInset.spines['left'].set_visible(False)
        axInset.spines['top'].set_visible(False)
        plt.ylabel(r'$\Delta$FR (%)', fontsize=fontSizeLegend, rotation=-90, labelpad=12)
        axInset.yaxis.set_label_position('right')
        
        yLims = np.array(plt.ylim())
        extraplots.significance_stars([barWidth/2,1+barWidth/2], yLims[1]*1.09, yLims[1]*0.04, gapFactor=0.35, starSize=6)
    

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)