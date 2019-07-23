import numpy as np
import pandas as pd
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.anna import bandwidths_analysis
reload(bandwidths_analysis)
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
#from jaratoolbox import figparams
import matplotlib.gridspec as gridspec
import matplotlib
import string
import pdb
from jaratest.nick.database import dataplotter
reload(dataplotter)

SAMPLING_RATE=30000.0
CELL_NUM = 170

db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band002_celldb.csv')
cell = db.loc[CELL_NUM]
ephysDirs = [word.strip(string.punctuation) for word in cell['ephys'].split()]
behavDirs = [word.strip(string.punctuation) for word in cell['behavior'].split()]
sessType = [word.strip(string.punctuation) for word in cell['sessiontype'].split()]
bandIndex = sessType.index('bandwidth')

loader = dataloader.DataLoader(cell['subject'])

matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

PRINT_FIGURE = 0
outputDir = '/tmp/'

fontSizeLabels = 12
fontSizeTicks = 12
fontSizePanel = 16

labelPosX = [0.07, 0.47]  # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels

plt.clf()

gs = gridspec.GridSpec(2, 4)
gs.update(left=0.15, right=0.85, wspace=1, hspace=0.5)

eventData = loader.get_session_events(ephysDirs[bandIndex])
spikeData = loader.get_session_spikes(ephysDirs[bandIndex], int(cell['tetrode']), cluster=int(cell['cluster']))
eventOnsetTimes = loader.get_event_onset_times(eventData)
spikeTimestamps = spikeData.timestamps
bdata = loader.get_session_behavior(behavDirs[bandIndex])
bandEachTrial = bdata['currentBand']
ampEachTrial = bdata['currentAmp']
spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandwidths_analysis.bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)


ax1 = plt.subplot(gs[0, :-2])
trialsThisSecondVal = trialsEachCond[:, :, 0]
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                indexLimitsEachTrial,
                                                timeRange = [-0.2, 1.5],
                                                trialsEachCond=trialsThisSecondVal,
                                                labels=firstSortLabels)
plt.setp(pRaster, ms=4)
extraplots.boxoff(plt.gca())
plt.xlabel('Time from stimulus onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

ax2 = plt.subplot(gs[1,:-2])
trialsThisSecondVal = trialsEachCond[:, :, 1]
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                indexLimitsEachTrial,
                                                timeRange = [-0.2, 1.5],
                                                trialsEachCond=trialsThisSecondVal,
                                                labels=firstSortLabels)
plt.setp(pRaster, ms=4)
extraplots.boxoff(plt.gca())
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time from stimulus onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


ax3 = plt.subplot(gs[0:, -2:])
spikeArray, errorArray, baseSpikeRate = bandwidths_analysis.band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])
bandwidths_analysis.band_select_plot(spikeArray, errorArray, baseSpikeRate, np.unique(bandEachTrial), legend = True, labels = ['54 dB', '66 dB'])
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
plt.ylabel('Average number of spikes during stimulus', fontsize=fontSizeLabels)
ax3.annotate('C', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

figFormat = 'pdf' #'svg' 
figFilename = 'testfig' # Do not include extension
if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, [8,6], outputDir)