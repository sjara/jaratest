''' Create figure showing bandwidth tuning with noise and harmonically organised tones'''
import os
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'


FIGNAME = 'harmonics_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

PANELS_TO_PLOT = [1,1] # [ExperimentalRaster, ExperimentalTuning]

filenameTuning = 'example_bandwidth_tuning_band033_2017-08-02_T8_c5.npz'

SAVE_FIGURE = 0
outputDir = '/tmp/'
figFilename = 'figure_harmonics_bandwidth_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [14,4]

fontSizeLabels = 14
fontSizeTicks = 12
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

laserColour = ['#4e9a06','#8ae234']
noLaserColour = ['0.25', '0.75']
colours = [noLaserColour, laserColour]

gs = gridspec.GridSpec(2,2)
gs.update(top=0.9, left=0.05, bottom=0.15, right=0.98, wspace=0.25, hspace=0.25)

dataFullPath = os.path.join(dataDir,filenameTuning)
data = np.load(dataFullPath)

# --- Raster plots of sound response with and without laser ---
if PANELS_TO_PLOT[0]:
    harmoTrials = data['possibleSecondSort']
    trialsEachCond = data['trialsEachCond']
    for harmo in harmoTrials:
        plt.subplot(gs[harmo,0])
        colourEachCond = np.tile(colours[harmo], len(data['possibleBands'])/2+1)
        trialsThisSecondVal = trialsEachCond[:, :, harmo]
        
        # a dumb workaround that dulpicates the tone trials to put in both rasters
        for ind2, band in enumerate(data['possibleBands']):
            if not any(trialsThisSecondVal[:,ind2]):
                trialsThisSecondVal[:,ind2]=trialsEachCond[:,ind2,harmo+1]
        
        pRaster, hcond, zline = extraplots.raster_plot(data['spikeTimesFromEventOnset'],
                                                   data['indexLimitsEachTrial'],
                                                   data['timeRange'],
                                                   trialsEachCond=trialsEachCond[:,:,harmo],
                                                   labels=data['firstSortLabels'])
        plt.setp(pRaster, ms=3, color=colours[harmo][0])
        plt.ylabel('Bandwidth (oct)')
    plt.xlabel('Time (s)')

# --- Plot of bandwidth tuning with and without laser ---
if PANELS_TO_PLOT[1]:
    spikeArray = data['spikeArray']
    errorArray = data['errorArray']
    
    #duplicate tone data for both curves
    spikeArray[0,0]=spikeArray[0,1]
    errorArray[0,0]=errorArray[0,1]
    
    bands = data['possibleBands']
    axTuning = plt.subplot(gs[0:,1:])
    lines = []
    plt.hold(True)
    l2,=plt.plot(range(len(bands)), spikeArray[:,1].flatten(), '-o', clip_on=False,
                 color = laserColour[0], mec = laserColour[0], linewidth = 3)
    lines.append(l2)
    plt.fill_between(range(len(bands)), spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                     spikeArray[:,1].flatten() + errorArray[:,1].flatten(),
                     alpha=0.2, edgecolor = laserColour[1], facecolor=laserColour[1])
    l1,=plt.plot(range(len(bands)), spikeArray[:,0].flatten(), '-o', clip_on=False,
                 color = noLaserColour[0], mec = noLaserColour[0], linewidth = 3)
    lines.append(l1)
    plt.fill_between(range(len(bands)), spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(),
                     alpha=0.2, edgecolor = noLaserColour[1], facecolor=noLaserColour[1])
    axTuning.set_xticklabels(bands)
    plt.xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    extraplots.boxoff(axTuning)
    plt.legend(lines,['Harmonics', 'Noise'], loc='lower center', frameon=False) #'upper left'
    plt.title('Just a graph lol',fontsize=fontSizeLabels,fontweight='bold')
   
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
