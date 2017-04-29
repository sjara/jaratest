''' Create figure showing bandwidth tuning of photoidentified cells.'''
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

FIGNAME = 'photoidentified_cells_bandwidth_tuning'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2017acnih', FIGNAME)


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

# copied this right out of Lan's scripts
'''
SAVE_FIGURE = 1
outputDir = '/home/jarauser/tmp/'
figFilename = 'figure_tuning_z_score_psychometric' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [8,6]

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel
labelDis = 0.1
labelPosX = [0.07, 0.45]   # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

gs = gridspec.GridSpec(1,2)
gs.update(left=0.15, right=0.85, wspace=0.5, hspace=0.5)

alphaLevel = 0.05
numFreqs = 16
bonferroniCorrectedAlphaLevel = alphaLevel/numFreqs
'''

# --- so far only plots first cell: PV cell ---
laserFilename = 'example_laser_response_band004_2016-09-09_T6_c4.npz'
laserDataFullPath = os.path.join(dataDir,laserFilename)
laserData = np.load(laserDataFullPath)

plt.figure()
pRaster, hcond, zline = extraplots.raster_plot(laserData['spikeTimesFromEventOnset'],
                                               laserData['indexLimitsEachTrial'],
                                               laserData['timeRange'])
plt.show()

bandFilename = 'example_bandwidth_tuning_band004_2016-09-09_T6_c4.npz'
bandDataFullPath = os.path.join(dataDir,bandFilename)
bandData = np.load(bandDataFullPath)
plt.figure()
pRaster, hcond, zline = extraplots.raster_plot(bandData['spikeTimesFromEventOnset'],
                                               bandData['indexLimitsEachTrial'],
                                               bandData['timeRange'],
                                               trialsEachCond=bandData['trialsEachCond'][:,:,-1],
                                               labels=[bandData['firstSortLabels']])
plt.show()

