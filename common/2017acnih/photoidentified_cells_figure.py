''' Create figure showing bandwidth tuning of photoidentified cells.'''
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

# -- Define which excitatory cell to use --
excitatoryCells = ['band016_2016-12-11_T6_c6.npz','band002_2016-08-11_T4_c5.npz','band002_2016-08-12_T6_c4.npz','band003_2016-08-18_T6_c6.npz']

args = sys.argv[1:]
if len(args):
    cellToUse = excitatoryCells[int(args[0])]
else:
    cellToUse = excitatoryCells[0]
print cellToUse


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

# copied this right out of Lan's scripts

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'photoidentified_bandwidth_tuning' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = 12
fontSizeTicks = 10
fontSizePanel = 16
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(3,3)
gs.update(left=0.1, right=0.9, wspace=0.5, hspace=0.5)


cell_file_names = ['band004_2016-09-09_T6_c4.npz', 'band015_2016-11-12_T8_c4.npz',cellToUse]
for ind,cell in enumerate(cell_file_names):
    laserFilename = 'example_laser_response_'+cell
    laserDataFullPath = os.path.join(dataDir,laserFilename)
    try:
        laserData = np.load(laserDataFullPath)
    
        # --- raster plot of laser response ---
        plt.subplot(gs[ind,0])
        pRaster, hcond, zline = extraplots.raster_plot(laserData['spikeTimesFromEventOnset'],
                                                   laserData['indexLimitsEachTrial'],
                                                   laserData['timeRange'])
        plt.setp(pRaster,ms=2)
        extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
        plt.ylabel('Trials',fontsize=fontSizeLabels)
        plt.xlabel('Time (sec)',fontsize=fontSizeLabels)
    except:
        pass
    
    bandFilename = 'example_bandwidth_tuning_'+cell
    bandDataFullPath = os.path.join(dataDir,bandFilename)
    bandData = np.load(bandDataFullPath)
    
    # --- raster plot of sound response at different bandwidths ---
    plt.subplot(gs[ind,1])
    pRaster, hcond, zline = extraplots.raster_plot(bandData['spikeTimesFromEventOnset'],
                                                   bandData['indexLimitsEachTrial'],
                                                   bandData['timeRange'],
                                                   trialsEachCond=bandData['trialsEachCond'][:,:,-1],
                                                   labels=bandData['firstSortLabels'])
    plt.setp(pRaster,ms=2)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
    plt.ylabel('Bandwidth (oct)',fontsize=fontSizeLabels)
    plt.xlabel('Time (sec)',fontsize=fontSizeLabels)

    # --- plot of bandwidth tuning ---
    spikeArray = bandData['spikeArray'][:,-1].flatten()
    errorArray = bandData['errorArray'][:,-1].flatten()
    bands = bandData['possibleBands']
    plt.subplot(gs[ind,2])
    plt.plot(range(len(bands)), spikeArray, '-o', lw = 3)
    plt.fill_between(range(len(bands)), spikeArray - errorArray, 
                         spikeArray + errorArray, alpha=0.2)
    ax = plt.gca()
    ax.set_xticklabels(bands)
    plt.xlabel('Bandwidth (octaves)',fontsize=fontSizeLabels)
    plt.ylabel('Average num spikes',fontsize=fontSizeLabels)
    extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.show()


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)
