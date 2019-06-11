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

FIGNAME = 'supplement_figure_cells_inactivated_by_archt'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

PANELS = [1,0,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
#outputDir = '/home/jarauser/data/figuresdata/2018acsup/figures'
figFilename = 'SuppFig7_suppression_by_archt' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
#figFormat = 'svg'
figSize = [8,6] # In inches
#figSize = [13,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.02, 0.36, 0.55]   # Horiz position for panel labels
labelPosY = [0.96, 0.46]    # Vert position for panel labels

PVFileName = 'example_PV_inactivated_sound_response_band062_2018-05-25_1450um_T5_c5.npz'
SOMFileName = 'example_SOM_inactivated_sound_response_band073_2018-09-14_1300um_T4_c4.npz'
summaryFileName = 'low_bandwidth_responses_during_inactivation.npz'

ExcColour = figparams.colp['excitatoryCell']
PVColour = figparams.colp['PVcell']
SOMColour = figparams.colp['SOMcell']

laserColour = figparams.colp['greenLaser']
soundColour = figparams.colp['sound']

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(2,2)
gs.update(top=0.95, bottom=0.1, left=0.1, right=0.99, wspace=0.2, hspace=0.4)

# --- suppressed responses of example cells ---
if PANELS[0]:
    exampleCells = [PVFileName, SOMFileName]
    
    cellColours = [PVColour, SOMColour]
    
    panelLabels = ['a', 'c']
    
    PSTHylims = [(-1, 47), (-0.4,16)]
    
    for indCell, cell in enumerate(exampleCells):
        axExample = gs[indCell, 0]
        
        exampleDataFullPath = os.path.join(dataDir,cell)
        exampleData = np.load(exampleDataFullPath)
        
        laserTrials = exampleData['possibleLasers']
        inner = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=axExample, wspace=0.1, hspace=0.4)
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

        axRaster.annotate(panelLabels[indCell], xy=(labelPosX[0],labelPosY[indCell]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')

# --- scatter plots of firing rates with and without laser        
if PANELS[1]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    cellColours = [PVColour, SOMColour]
    
    panelLabels = ['b', 'e']
    
    PVcontrolResponses = summaryData['PVcontrolResponses']
    PVlaserResponses = summaryData['PVlaserResponses']
    
    SOMcontrolResponses = summaryData['SOMcontrolResponses']
    SOMlaserResponses = summaryData['SOMlaserResponses']
    
    PVpVals = summaryData['PVpVals']
    SOMpVals = summaryData['SOMpVals']
    
    PVcontrolLaserOnsets = summaryData['PVcontrolLaserOnset']
    PVlaserOnsets = summaryData['PVlaserOnset']
    PVchangeLaserOnsetResponse = PVlaserOnsets-PVcontrolLaserOnsets
    
    SOMcontrolLaserOnsets = summaryData['SOMcontrolLaserOnset']
    SOMlaserOnsets = summaryData['SOMlaserOnset']
    SOMchangeLaserOnsetResponse = SOMlaserOnsets-SOMcontrolLaserOnsets
    
    PVlaserOnsetpVals = summaryData['PVlaserOnsetpVals']
    SOMlaserOnsetpVals = summaryData['SOMlaserOnsetpVals']
    
    
    responses = [[PVcontrolResponses, PVlaserResponses],[SOMcontrolResponses, SOMlaserResponses]]
    pVals = [PVpVals, SOMpVals]
    onsetChange = [PVchangeLaserOnsetResponse, SOMchangeLaserOnsetResponse]
    laserpVals = [PVlaserOnsetpVals, SOMlaserOnsetpVals]
    
    for indType, cellType in enumerate(responses):
        axScatter = plt.subplot(gs[indType, 2])
        
        plt.hold(True)
        
        sigCells = (pVals[indType]<0.05) & (cellType[0]>cellType[1])
        sigOnsetCells = (laserpVals[indType]<0.05) & (onsetChange[indType]<0)
        
        axisMin = 0.03 #lowest point on log scale
        
        cellType[0][cellType[0]<axisMin] = axisMin #boost up the ones that wouldn't show up on a log scale
        cellType[1][cellType[1]<axisMin] = axisMin
        
        plt.scatter(cellType[0][sigCells],cellType[1][sigCells], edgecolors=cellColours[indType], facecolors='none', s=15)
        plt.scatter(cellType[0][sigOnsetCells],cellType[1][sigOnsetCells], marker='x', color='k', s=15, zorder=10)
        plt.scatter(cellType[0][~sigCells],cellType[1][~sigCells], edgecolors=cellColours[indType], facecolors=cellColours[indType], s=15)
        plt.ylabel('Sound response \nwith laser (spk/s)',fontsize=fontSizeLabels)
        plt.xlabel('Sound response (spk/s)',fontsize=fontSizeLabels)
        axScatter.set_xscale('log', basex=10)
        axScatter.set_yscale('log', basex=10)
        
        plt.plot([-5,100], [-5,100], 'k--')
        plt.xlim(axisMin,100)
        plt.ylim(axisMin,100)
        axScatter.tick_params(top=False, right=False, which='both')
        
        ticks=[0.1,1,10,100]
        
        axScatter.set_xticks(ticks)
        axScatter.set_xticklabels(ticks)
        axScatter.set_yticks(ticks)
        axScatter.set_yticklabels(ticks)
    
        axScatter.annotate(panelLabels[indType], xy=(labelPosX[1],labelPosY[indType]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        extraplots.boxoff(axScatter)
        axScatter.set(adjustable='box-forced', aspect='equal')
        
# --- plots of cells immediately suppressed and their sustained suppression
if PANELS[2]:
    summaryDataFullPath = os.path.join(dataDir,summaryFileName)
    summaryData = np.load(summaryDataFullPath)
    
    cellColours = [PVColour, SOMColour]
    
    panelLabels = ['b', 'd']
    
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
        axScatter = plt.subplot(gs[indType, 1])
        
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
    
        axScatter.annotate(panelLabels[indType], xy=(labelPosX[2],labelPosY[indType]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
        extraplots.boxoff(axScatter)
        axScatter.set(adjustable='box-forced', aspect='equal')
    

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)