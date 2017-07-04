''' Create figure showing bandwidth tuning with and without SOM inactivation'''
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


FIGNAME = 'SOM_inactivation_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

PANELS_TO_PLOT = [1,1,1] # [ExperimentalRaster, ExperimentalTuning, ModelTuning]

filenameTuning = 'example_bandwidth_tuning_band025_2017-04-20_T6_c6.npz'

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'figure_SOM_inactivation_bandwidth_tuning' # Do not include extension
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

gs = gridspec.GridSpec(2,4)
gs.update(top=0.9, left=0.05, bottom=0.15, right=0.98, wspace=0.25, hspace=0.25)

dataFullPath = os.path.join(dataDir,filenameTuning)
data = np.load(dataFullPath)

# --- Raster plots of sound response with and without laser ---
if PANELS_TO_PLOT[0]:
    laserTrials = data['possibleSecondSort']
    for laser in laserTrials:
        plt.subplot(gs[laser,1])
        colourEachCond = np.tile(colours[laser], len(data['possibleBands'])/2+1)
        pRaster, hcond, zline = extraplots.raster_plot(data['spikeTimesFromEventOnset'],
                                                   data['indexLimitsEachTrial'],
                                                   data['timeRange'],
                                                   trialsEachCond=data['trialsEachCond'][:,:,laser],
                                                   labels=data['firstSortLabels'])
        plt.setp(pRaster, ms=3, color=colours[laser][0])
        plt.ylabel('Bandwidth (oct)')
    plt.xlabel('Time (s)')

# --- Plot of bandwidth tuning with and without laser ---
if PANELS_TO_PLOT[1]:
    spikeArray = data['spikeArray']
    errorArray = data['errorArray']
    bands = data['possibleBands']
    axTuning = plt.subplot(gs[0:,2])
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
    #plt.legend(lines,['no laser', 'laser'], bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)
    plt.legend(lines,['No SOM', 'Control'], loc='lower center', frameon=False) #'upper left'
    plt.title('Mouse AC',fontsize=fontSizeLabels,fontweight='bold')


# -- Plot model curves --
modelDataDir = './modeldata'
if PANELS_TO_PLOT[2] & os.path.isdir(modelDataDir):
    import pandas as pd
    modelDataFiles = ['SSNbandwidthTuning_regime1.csv']

    colorEachCond = [noLaserColour[0], laserColour[0]]
    axModel = plt.subplot(gs[0:,3])
    for indm, oneModelFile in enumerate(modelDataFiles):
        modelData = pd.read_csv(os.path.join(modelDataDir,oneModelFile))
        modelBW = modelData['BW(oct)']
        modelRates = [modelData['y_PV'], modelData['y_SOM']]

        for indc,rates in enumerate(modelRates):
            #plt.plot(np.log2(modelBW), rates, 'o', lw=5, color=cellColor[indc], mec=cellColor[indc])
            plt.plot(modelBW, rates, 'o-', lw=5, color=colorEachCond[indc], mec=colorEachCond[indc], clip_on=True)
            #axModel.set_xticklabels(bands)
            plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
            extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
            axModel.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
            extraplots.boxoff(axModel)
    plt.title('Model',fontsize=fontSizeLabels,fontweight='bold')
    
plt.show()

if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
