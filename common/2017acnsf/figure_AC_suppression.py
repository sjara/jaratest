# Figure showing example of surround suppression in AC
#
# CURRENTLY, IT DEPENDS ON:
# jaratest.nick.database import dataloader_v2 as dataloader
# jaratest.anna import bandwidths_analysis
# jaratest/anna/analysis/band002_celldb.csv
# and of course, the ephys data.

import numpy as np
import pandas as pd
from jaratest.nick.database import dataloader_v2 as dataloader
#from jaratest.anna import bandwidths_analysis
#reload(bandwidths_analysis)
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
#from jaratoolbox import figparams
import matplotlib.gridspec as gridspec
import matplotlib
import string
import matplotlib.patches as mpatches
import pdb
#from jaratest.nick.database import dataplotter
#reload(dataplotter)


CELL_NUM = 161
outputFile = './example_AC_supression_c{0}.npz'.format(CELL_NUM)


matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['svg.fonttype'] = 'none'

PRINT_FIGURE = 1
outputDir = '/tmp/'

fontSizeLabels = 18
fontSizeTicks = 14
fontSizePanel = 24

labelPosX = [0.05, 0.5]  # Horiz position for panel labels
labelPosY = [0.9, 0.45]    # Vert position for panel labels


sdata = np.load(outputFile)
spikeTimesFromEventOnset = sdata['spikeTimesFromEventOnset']
indexLimitsEachTrial = sdata['indexLimitsEachTrial']
trialsEachCond = sdata['trialsEachCond']
firstSortLabels = list(sdata['firstSortLabels'])
bandEachTrial = sdata['bandEachTrial']
spikeArray = sdata['spikeArray']
errorArray = sdata['errorArray']
baseSpikeRate = sdata['baseSpikeRate']



plt.clf()

gs = gridspec.GridSpec(4, 4)
gs.update(left=0.14, right=0.95, bottom=0.12, wspace=1, hspace=0.25)


ax1 = plt.subplot(gs[0:2, :-2])
trialsThisSecondVal = trialsEachCond[:, :, 1]
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                indexLimitsEachTrial,
                                                timeRange = [-0.3, 1.4],
                                                trialsEachCond=trialsThisSecondVal,
                                                labels=firstSortLabels,
                                                colorEachCond=np.tile(['#5c3566','#ad7fa8'],len(bandEachTrial)/2+1))
plt.setp(pRaster, ms=4)
extraplots.boxoff(plt.gca())
#plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Bandwidth\n(octaves)', fontsize=fontSizeLabels)
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('')
ax1.set_xticks(np.arange(0,1.5,0.5))
ax1.set_xticklabels([])
ax1.annotate('A', xy=(labelPosX[0],labelPosY[0]), xycoords='figure fraction',
             fontsize=fontSizePanel, fontweight='bold')

ax2 = plt.subplot(gs[2:4,:-2])
trialsThisSecondVal = trialsEachCond[:, :, 0]
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                indexLimitsEachTrial,
                                                timeRange = [-0.3, 1.4],
                                                trialsEachCond=trialsThisSecondVal,
                                                labels=firstSortLabels,
                                                colorEachCond=np.tile(['#4e9a06','#8ae234'],len(bandEachTrial)/2+1))
plt.setp(pRaster, ms=4)
extraplots.boxoff(plt.gca())
extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
plt.xlabel('Time from sound onset (s)', fontsize=fontSizeLabels)
plt.ylabel('Bandwidth\n(octaves)', fontsize=fontSizeLabels)
ax2.set_xticks(np.arange(0,1.5,0.5))
ax2.annotate('B', xy=(labelPosX[0],labelPosY[1]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')


ax3 = plt.subplot(gs[0:3, -2:])
#ax3 = plt.axes() # [left, bottom, width, height]
stimDuration = 1.0        ### FIXME: Hardcoded!!!

#spikeArray, errorArray, baseSpikeRate = band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])
#band_select_plot(spikeArray, errorArray, baseSpikeRate, np.unique(bandEachTrial), legend = True, labels = ['54 dB-SPL', '66 dB-SPL'])

#band_select_plot(spikeArray, errorArray, baselineSpikeRate, bands, legend = False, labels = ['50 dB SPL', '70 dB SPL'], timeRange = [0,1], title=None)
bands = np.unique(bandEachTrial)
labels = ['54 dB', '66 dB']  # dB-SPL
timeRange = timeRange = [0,1]
plt.hold(True)
xrange = range(len(bands))
plt.plot(xrange, baseSpikeRate*(timeRange[1]-timeRange[0])*np.ones(len(bands)), color = '0.5', ls='--', linewidth = 1)
plt.plot(xrange, spikeArray[:,0].flatten(), '-o', color = '#4e9a06', linewidth = 3)
plt.fill_between(xrange, spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                 spikeArray[:,0].flatten() + errorArray[:,0].flatten(), alpha=0.2, edgecolor = '#8ae234', facecolor='#8ae234')
plt.plot(range(len(bands)), spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                 spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
ax = plt.gca()
ax.set_xticklabels(bands)
patch1 = mpatches.Patch(color='#5c3566', label=labels[1])
patch2 = mpatches.Patch(color='#4e9a06', label=labels[0])
plt.legend(handles=[patch1, patch2], bbox_to_anchor=(0.95, 0.95), borderaxespad=0, prop={'size':14})

extraplots.set_ticks_fontsize(plt.gca(),fontSizeTicks)
extraplots.boxoff(ax3)
plt.xlabel('Bandwidth (octaves)', fontsize=fontSizeLabels)
plt.ylabel('Evoked response (spk/s)', fontsize=fontSizeLabels)
ax3.annotate('C', xy=(labelPosX[1],labelPosY[0]), xycoords='figure fraction', fontsize=fontSizePanel, fontweight='bold')

plt.show()

figFormat = 'svg'#'pdf' #'svg' 
figFilename = 'testfig' # Do not include extension
if PRINT_FIGURE:
    extraplots.save_figure(figFilename, figFormat, [8,5], outputDir)
    print 'Saved figure to: {0}'.format(figFilename)
    
