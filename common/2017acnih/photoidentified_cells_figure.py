''' 
Create figure showing bandwidth tuning of photoidentified cells.

Laser trials: at least 100 trials of 100ms laser, average iti 0.8 seconds
Bandwidth tuning: 30 trials each bandwidth, sound 1 sec long, average iti 1.5 seconds
Center frequency determined with shortened tuning curve (16 freq, two intensities, best frequency one that elicits most spikes)
AM rate selected as one eliciting highest spike rate and most consistent response
'''
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
reload(extraplots)
from jaratoolbox import settings
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

FIGNAME = 'photoidentified_cells_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)

PANELS_TO_PLOT = [1,1,1]

# -- Define which excitatory cell to use --
excitatoryCells = ['band016_2016-12-11_T6_c6.npz','band002_2016-08-11_T4_c5.npz','band002_2016-08-12_T6_c4.npz','band003_2016-08-18_T6_c6.npz']

args = sys.argv[1:]
if len(args):
    cellToUse = excitatoryCells[int(args[0])]
else:
    cellToUse = excitatoryCells[0]
print cellToUse

cellFileNames = ['band004_2016-09-09_T6_c4.npz', 'band015_2016-11-12_T8_c4.npz', cellToUse]


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

# copied this right out of Lan's scripts

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'photoidentified_bandwidth_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [14,6]

fontSizeLabels = 14 #12
fontSizeTicks = 12 #10
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels
cellColor = [cp.TangoPalette['Chameleon3'], cp.TangoPalette['ScarletRed1'], cp.TangoPalette['SkyBlue2']]

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')


# -- Load laser example --
gs0 = gridspec.GridSpec(6,3)
gs0.update(top=0.9, left=0.05, right=0.7, wspace=0.6, hspace=0.1)

# --- Raster plot of laser response ---
if PANELS_TO_PLOT[0]:
    indc = 0
    laserFilename = 'example_laser_response_'+cellFileNames[indc]
    laserDataFullPath = os.path.join(dataDir,laserFilename)
    laserData = np.load(laserDataFullPath)

    axLaser = plt.subplot(gs0[0,0])
    nTrials = 30
    laserIndexLimitsEachTrial = laserData['indexLimitsEachTrial'][:,:nTrials]
    laserTimeRange = [-0.1,0.3]
    pRaster, hcond, zline = extraplots.raster_plot(laserData['spikeTimesFromEventOnset'],
                                                   laserIndexLimitsEachTrial,
                                                   laserTimeRange)
    axLaser.set_xticks([-0.1, 0, 0.1, 0.2, 0.3])
    axLaser.set_yticks([0,nTrials])
    plt.setp(pRaster, ms=3, color=cellColor[indc])
    plt.setp(hcond, visible=False)
    plt.setp(zline, visible=False)
    extraplots.boxoff(axLaser)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Trials',fontsize=fontSizeLabels)
    plt.xlabel('Time from laser onset (s)',fontsize=fontSizeLabels)


gs1 = gridspec.GridSpec(3,4)
gs1.update(top=0.95, left=0.05, right=0.98, wspace=0.35, hspace=0.2)

    
# -- Plots for each cell type --
if PANELS_TO_PLOT[1]:
    for indc,cell in enumerate(cellFileNames):

        bandFilename = 'example_bandwidth_tuning_'+cell
        bandDataFullPath = os.path.join(dataDir,bandFilename)
        bandData = np.load(bandDataFullPath)


        # --- Raster plot of sound response at different bandwidths ---
        axRaster = plt.subplot(gs1[indc,1])
        timeRange = [-0.2,1.3]
        pRaster, hcond, zline = extraplots.raster_plot(bandData['spikeTimesFromEventOnset'],
                                                       bandData['indexLimitsEachTrial'],
                                                       timeRange,
                                                       trialsEachCond=bandData['trialsEachCond'][:,:,-1],
                                                       labels=bandData['firstSortLabels'])
        plt.setp(pRaster, ms=2, color=cellColor[indc])
        axRaster.set_xticks([0,0.5,1])
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        if indc==2:
            axRaster.set_xlabel('Time (sec)',fontsize=fontSizeLabels)
        else:
            axRaster.set_xticklabels('')


        # --- Plot of bandwidth tuning ---
        spikeArray = bandData['spikeArray'][:,-1].flatten()
        errorArray = bandData['errorArray'][:,-1].flatten()
        bands = bandData['possibleBands']
        plt.subplot(gs1[indc,2])
        plt.plot(range(len(bands)), spikeArray, '-o', ms=7, lw=3, color=cellColor[indc], mec=cellColor[indc])
        plt.fill_between(range(len(bands)), spikeArray - errorArray, 
                             spikeArray + errorArray, alpha=0.2, color='0.5')
        axCurve = plt.gca()
        axCurve.set_xticklabels(bands)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        if indc==2:
            axCurve.set_xlabel('Bandwidth (oct)',fontsize=fontSizeLabels)
        else:
            axCurve.set_xticklabels('')


# -- Plot model curves --
if PANELS_TO_PLOT[2]:
    modelDataDir = './modeldata'
    modelBW = np.loadtxt(os.path.join(modelDataDir,'bandwidths.dat'), delimiter=',')[:-1]
    modelRatesE = np.loadtxt(os.path.join(modelDataDir,'rates_E.dat'), delimiter=',')[:-1]
    modelRatesPV = np.loadtxt(os.path.join(modelDataDir,'rates_PV.dat'), delimiter=',')[:-1]
    modelRatesSOM = np.loadtxt(os.path.join(modelDataDir,'rates_SOM.dat'), delimiter=',')[:-1]
    modelRates = [modelRatesPV, modelRatesSOM, modelRatesE]

    for indc,rates in enumerate(modelRates):
        axModel = plt.subplot(gs1[indc,3])
        #plt.plot(np.log2(modelBW), rates, 'o', lw=5, color=cellColor[indc], mec=cellColor[indc])
        plt.plot(modelBW, rates, 'o', lw=5, color=cellColor[indc], mec=cellColor[indc])
        #axModel.set_xticklabels(bands)
        plt.ylabel('Firing rate (spk/s)',fontsize=fontSizeLabels)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        if indc==2:
            axModel.set_xlabel('Bandwidth (oct???)',fontsize=fontSizeLabels)
        else:
            axModel.set_xticklabels('')

plt.show()



if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
