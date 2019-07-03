''' 
Create figure showing laser response of example PV and SOM cell as well as waveforms of all recorded PV and SOM cells
'''
import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import ndimage

from jaratoolbox import settings
from jaratoolbox import extraplots

import figparams
import studyparams



FIGNAME = 'supplement_figure_photoidentification'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

HISTFIGNAME = 'supplement_figure_histology'
histDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, HISTFIGNAME)


PANELS = [1,1,1,1] # Plot panel i if PANELS[i]==1

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'Fig1_photoidentification_method' # Do not include extension
#figFormat = 'pdf' # 'pdf' or 'svg'
figFormat = 'svg'
figSize = [10,6] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
fontSizeLegend = figparams.fontSizeLegend

labelPosX = [0.005, 0.24, 0.49, 0.76]   # Horiz position for panel labels
labelPosY = [0.96, 0.66, 0.37]    # Vert position for panel labels

ExcFileName = 'band016_2016-12-11_950um_T6_c6.npz'
#ExcFileName = 'band029_2017-05-25_1240um_T2_c2.npz'
#ExcFileName = 'band031_2017-06-29_1140um_T1_c3.npz'
#ExcFileName = 'band044_2018-01-16_975um_T7_c4.npz'
#ExcFileName = 'band060_2018-04-02_1275um_T4_c2.npz'

#PVFileName = 'band026_2017-04-26_1470um_T4_c5.npz'
#PVFileName = 'band026_2017-04-27_1350um_T4_c2.npz'
#PVFileName = 'band032_2017-07-21_1200um_T6_c2.npz'
PVFileName = 'band033_2017-07-27_1700um_T4_c5.npz'

SOMFileName = 'band015_2016-11-12_1000um_T8_c4.npz'
#SOMFileName = 'band029_2017-05-22_1320um_T4_c2.npz'
#SOMFileName = 'band031_2017-06-29_1280um_T1_c4.npz'
#SOMFileName = 'band060_2018-04-04_1225um_T3_c4.npz'

waveformsFileName = 'photoidentified_cells_waveforms.npz'

laserResponsesFileName = 'all_cells_laser_responses.npz'

histFileName = 'band055_outlines.jpg'

ExcColor = figparams.colp['excitatoryCell']
excludedExcColor = figparams.colp['excludedExcitatory']
PVColor = figparams.colp['PVcell']
SOMColor = figparams.colp['SOMcell']

laserColor = figparams.colp['blueLaser']


fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3,4, width_ratios=[1.1,0.9,1,1])
gs.update(top=0.95, bottom=0.14, left=0.02, right=0.99, wspace=0.5, hspace=0.3)

#REALLY DUMB WORKAROUND FOR THE FACT THAT EDGECOLORS ONLY TAKES RGBA INPUTS
def list_colours_to_rgba(colours):
    dumbcolours = np.zeros((len(colours),4))
    for indColour, colour in enumerate(colours):
        thisColour = matplotlib.colors.colorConverter.to_rgba(colour, alpha=1)
        dumbcolours[indColour,:] = thisColour
    return dumbcolours

# --- Plot of histology and making room for cartoons ---
if PANELS[0]:
    panelLabels = ['A', 'D', 'G']
    
    histFullPath = os.path.join(histDataDir, histFileName)
    histImage = ndimage.imread(histFullPath)
    
    imageBounds = [400, 800, 0, 400] #for band055
    #imageBounds = [300, 700, 988, 1388] #for band004
    
    axImage = plt.subplot(gs[2,0])
    plt.imshow(histImage[imageBounds[0]:imageBounds[1],imageBounds[2]:imageBounds[3],:])
    plt.axis('off')
    
    axImage.set_position([0.015,0.07,0.17,0.27]) #position: left, bottom, width, height
    
    for ind, label in enumerate(panelLabels):
        axImage.annotate(label, xy=(labelPosX[0],labelPosY[ind]), xycoords='figure fraction',
                             fontsize=fontSizePanel, fontweight='bold')
    
    axImage.annotate('AUDp', xy=(0.6,0.35), xycoords='axes fraction', fontsize=fontSizeLegend, color='w')
    axImage.annotate('AUDpo', xy=(0.65,0.75), xycoords='axes fraction', fontsize=fontSizeLegend, color='w')
    axImage.annotate('AUDv', xy=(0.45,0.05), xycoords='axes fraction', fontsize=fontSizeLegend, color='w')
    

# --- Raster plots of example Exc., PV, and SOM cell ---
if PANELS[1]:
    # Exc. cell
    ExcFile = 'example_AC_laser_response_'+ExcFileName
    ExcDataFullPath = os.path.join(dataDir,ExcFile)
    ExcData = np.load(ExcDataFullPath)
    
    # PV cell
    PVFile = 'example_PV_laser_response_'+PVFileName
    PVDataFullPath = os.path.join(dataDir,PVFile)
    PVData = np.load(PVDataFullPath)
    
    # SOM cell
    SOMFile = 'example_SOM_laser_response_'+SOMFileName
    SOMDataFullPath = os.path.join(dataDir,SOMFile)
    SOMData = np.load(SOMDataFullPath)
    
    cellData = [PVData, SOMData, ExcData]
    panelLabels = ['B', 'E', 'H']
    panelTitles = [r'PV$^+$', r'SOM$^+$', 'Excitatory']
    
    colours = [PVColor, SOMColor, ExcColor]
    
    cellLabelPosX = 0.22
    cellLabelPosY = [0.87, 0.595, 0.31]
    
    for indCell, cell in enumerate(cellData):
        axRaster = plt.subplot(gs[indCell:indCell+1,1])
        plt.cla()
        bandSpikeTimesFromEventOnset = cell['spikeTimesFromEventOnset']
        bandIndexLimitsEachTrial = cell['indexLimitsEachTrial']
        rasterTimeRange = cell['rasterTimeRange']
        pRaster, hcond, zline = extraplots.raster_plot(bandSpikeTimesFromEventOnset,bandIndexLimitsEachTrial,rasterTimeRange)
        axRaster.annotate(panelLabels[indCell], xy=(labelPosX[1],labelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        
        axRaster.annotate(panelTitles[indCell], xy=(cellLabelPosX,cellLabelPosY[indCell]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold', color=colours[indCell], rotation=90)
        plt.setp(pRaster, ms=3, color='k')
        
        # is there a better way to remove these things??
        while len(hcond)>0:
            bar=hcond.pop(0)
            bar.remove()
            
        extraplots.boxoff(axRaster)
        xticks = np.arange(rasterTimeRange[0], rasterTimeRange[1]+0.1, 0.1)
        axRaster.set_xticks(xticks)
        if indCell != 2:
            axRaster.set_xticklabels('')
        else:
            plt.xlabel('Time from laser onset (s)',fontsize=fontSizeLabels)
        plt.ylabel('Trial',fontsize=fontSizeLabels, labelpad=-2)
        
        yLims = np.array(plt.ylim())
        rect = patches.Rectangle((0,yLims[1]*1.03),0.1,yLims[1]*0.04,linewidth=1,edgecolor=laserColor,facecolor=laserColor,clip_on=False)
        axRaster.add_patch(rect)
    
    extraplots.set_ticks_fontsize(axRaster,fontSizeTicks)

# --- histograms of spike widths as well as waveforms for all recorded Exc., PV, SOM cells    
if PANELS[2]:
    # all waveforms
    waveformsDataFullPath = os.path.join(dataDir,waveformsFileName)
    spikeShapeData = np.load(waveformsDataFullPath)
    ExcSpikeShapes = spikeShapeData['ExcNormSpikeShapes']
    ExcMedianSpikeShape = spikeShapeData['ExcMedianSpikeShape']
    PVspikeShapes = spikeShapeData['PVnormSpikeShapes']
    PVmedianSpikeShape = spikeShapeData['PVmedianSpikeShape']
    SOMspikeShapes = spikeShapeData['SOMnormSpikeShapes']
    SOMmedianSpikeShape = spikeShapeData['SOMmedianSpikeShape']
    
    ExcSpikeWidths = spikeShapeData['ExcSpikeWidths']
    PVspikeWidths = spikeShapeData['PVspikeWidths']
    SOMspikeWidths = spikeShapeData['SOMspikeWidths']
    
    spikeWidthData = [PVspikeWidths, SOMspikeWidths, ExcSpikeWidths]
    waveformData = [PVspikeShapes, SOMspikeShapes, ExcSpikeShapes]
    medianWaveforms = [PVmedianSpikeShape, SOMmedianSpikeShape, ExcMedianSpikeShape]
    panelLabels = ['C', 'F', 'I']
    
    # plot excitatory waveforms excluded for being too narrow a different colour
    ExcColors = np.where(ExcSpikeWidths>studyparams.EXC_SPIKE_WIDTH, ExcColor, excludedExcColor)
    
    histColours = [PVColor, SOMColor, ExcColor]
    colours = [[PVColor], [SOMColor], ExcColors]
    
    insetLocs = [1, 1, 2]
    insetAnchors = [(0, 0, 1, 1),(0, 0, 1, 1),(.05, 0, 1, 1)]
    
    bins = np.linspace(0, 1, 16)
    
    plt.hold(True)
    for indType, cellTypeData in enumerate(spikeWidthData):
        axHist = plt.subplot(gs[indType:indType+1,2])
        plt.hist(cellTypeData*1000.0, bins=bins, color=histColours[indType], edgecolor=histColours[indType], linewidth=0.3) #plot in ms
        plt.ylabel('Cell count')
        plt.locator_params(axis='y', nbins=5)
        if indType<2:
            axHist.set_xticklabels('')
        else:
            plt.hist(cellTypeData[ExcSpikeWidths<studyparams.EXC_SPIKE_WIDTH]*1000.0, bins=bins, color=excludedExcColor, edgecolor=excludedExcColor, linewidth=0.3)
            axHist.set_xticklabels([0,'',0.4,'',0.8,''])
            plt.xlabel('Peak to trough time (ms)')
        
        axInset = inset_axes(axHist, width="35%", height="35%", loc=insetLocs[indType], bbox_to_anchor=insetAnchors[indType], bbox_transform=axHist.transAxes,)
        for indCell in range(waveformData[indType].shape[0]):
            if len(colours[indType])>1:
                colour = colours[indType][indCell]
            else:
                colour = colours[indType][0]
            plt.plot(waveformData[indType][indCell,:], color=colour, alpha=0.1)
            plt.xticks([])
            plt.yticks([])
        #plt.plot(medianWaveforms[indType], color=medColours[indType])
        axHist.annotate(panelLabels[indType], xy=(labelPosX[2],labelPosY[indType]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
        extraplots.boxoff(axHist)
        
# --- indicate which cells from all "good" ones were identified as PV or SOM ---
if PANELS[3]:
    # laser responses of all good cells
    laserDataFullPath = os.path.join(dataDir,laserResponsesFileName)
    laserResponseData = np.load(laserDataFullPath)
    
    PVanimalsChangeFR = laserResponseData['laserChangePVmice']
    PVanimalsLaserPVal = laserResponseData['laserPValPVmice']
    
    SOManimalsChangeFR = laserResponseData['laserChangeSOMmice']
    SOManimalsLaserPVal = laserResponseData['laserPValSOMmice']
    SOManimalsLaserUStat = laserResponseData['laserUStatSOMmice']
    SOManimalsSpikeWidth = laserResponseData['spikeWidthSOMmice']
    
    #split cells from SOM animals into putative excitatory and other
    putExcCells = ((SOManimalsLaserUStat<0) | (SOManimalsLaserPVal>studyparams.EXC_LASER_RESPONSE_PVAL)) & (SOManimalsSpikeWidth>studyparams.EXC_SPIKE_WIDTH)
    
    putExcCellResponses = SOManimalsChangeFR[putExcCells]
    otherCellResponses = SOManimalsChangeFR[~putExcCells]
    otherCellpVals = SOManimalsLaserPVal[~putExcCells]
    
    changesFR = [PVanimalsChangeFR, otherCellResponses]
    pVals = [PVanimalsLaserPVal, otherCellpVals]

    colours = [PVColor, SOMColor]
    categoryLabels = ['PV::ChR2', 'SOM::ChR2']
    panelLabel = 'J'
    
    axScatter = plt.subplot(gs[:,3])
    
    plt.hold(True)
    for category in range(len(changesFR)):
        xval = (category+1)*np.ones(len(changesFR[category]))
          
        jitterAmt = np.random.random(len(xval))
        xval = xval + (0.6 * jitterAmt) - 0.3
        mfc = np.where(pVals[category]<0.001,colours[category],'none')
        mec = list_colours_to_rgba(np.where(pVals[category]<0.001,colours[category],'0.75'))
            
        plt.scatter(xval, changesFR[category], facecolors=mfc, edgecolors=mec, clip_on=False, s=10, linewidths=0.5)
    
    #plot the putative excitatory ones last to make sure they're on top
    xval = (category+1)*np.ones(len(putExcCellResponses))
    jitterAmt = np.random.random(len(xval))
    xval = xval + (0.6 * jitterAmt) - 0.3
    plt.scatter(xval, putExcCellResponses, facecolors=ExcColor, edgecolors=ExcColor, clip_on=False, s=10, linewidths=0.5, zorder=10)
    
    axScatter.annotate(panelLabel, xy=(labelPosX[3],labelPosY[0]), xycoords='figure fraction',
                         fontsize=fontSizePanel, fontweight='bold')
    plt.xlim(0.3,len(changesFR)+0.7)
    axScatter.set_xticks(range(1,len(changesFR)+1))
    axScatter.set_xticklabels(categoryLabels, fontsize=fontSizeLabels, rotation=-45)#, ha='left')
    plt.ylim(-20,125)
    plt.ylabel('Response to first 10ms of laser (spk/s)')
    extraplots.boxoff(axScatter)
        
    
if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)