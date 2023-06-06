"""
Plot  oddball enhancement index for all cells (for saline and DOI).

Based on generate_oddball_comparison_plots.py by Max Horrocks.
"""

import os
import sys
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
from jaratoolbox import colorpalette as cp

SAVE_FIGURE = 0


# Change to cellDB 
filename = '/home/jarauser/Max/Acid007WithBaseline.h5'
celldb = celldatabase.load_hdf(filename)

fontsize = 16
figsToPlot = [1, 0]

#fig, axes = plt.subplots(figsize = (10,10))
fig = plt.gcf()
gsMain = gs.GridSpec(1, np.sum(figsToPlot), figure = fig)
gsMain.update(top=0.95, bottom=0.1, left=0.32, right=0.95, wspace=0.3, hspace=0.075)
plt.subplots_adjust(wspace=1)
barLoc = np.array([-0.6, 0.6])

colors = {'saline':cp.TangoPalette['SkyBlue2'], 'doi': cp.TangoPalette['ScarletRed1']}

upOddballIndexSalineColumn= celldb['upOddballIndexSaline']
upOddballIndexDOIColumn= celldb['upOddballIndexDOI']
upOddSpikesAvgSalineColumn = celldb['upOddSpikesAvgFiringRateSaline']
upOddSpikesAvgDOIColumn = celldb['upOddSpikesAvgFiringRateDOI']

upStandSpikesAvgSalineColumn = celldb['upStandardSpikesAvgFiringRateSaline']
upStandSpikesAvgDOIColumn = celldb['upStandardSpikesAvgFiringRateDOI']

downOddballIndexSalineColumn= celldb['downOddballIndexSaline']
downOddballIndexDOIColumn= celldb['downOddballIndexDOI']
downOddSpikesAvgSalineColumn = celldb['downOddSpikesAvgFiringRateSaline']
downOddSpikesAvgDOIColumn = celldb['downOddSpikesAvgFiringRateDOI']

downStandSpikesAvgSalineColumn = celldb['downStandardSpikesAvgFiringRateSaline']
downStandSpikesAvgDOIColumn = celldb['downStandardSpikesAvgFiringRateDOI']

#baselineDownSaline = celldb['baselineFiringDownSaline']
baselineUpStandardFiringRateSaline = celldb['baselineUpStandardFiringRateSaline']
baselineDownStandardFiringRateSaline = celldb['baselineDownStandardFiringRateSaline']
#baselineUpSaline = celldb['baselineFiringUpSaline']

firingThreshold = 5
selectedCellsUp = ((upOddSpikesAvgSalineColumn > firingThreshold) &
                   (upOddSpikesAvgDOIColumn > firingThreshold) &
                   (baselineUpStandardFiringRateSaline < upStandSpikesAvgSalineColumn)) #& (responseMagnitude > 0)

selectedCellsDown = ((downOddSpikesAvgSalineColumn > firingThreshold) &
                     (downOddSpikesAvgDOIColumn > firingThreshold) &
                     (baselineDownStandardFiringRateSaline < downStandSpikesAvgSalineColumn))

upOddballIndexSaline = upOddballIndexSalineColumn[selectedCellsUp].to_numpy()
upOddballIndexDOI = upOddballIndexDOIColumn[selectedCellsUp].to_numpy()

downOddballIndexSaline = downOddballIndexSalineColumn[selectedCellsDown].to_numpy()
downOddballIndexDOI = downOddballIndexDOIColumn[selectedCellsDown].to_numpy()



if figsToPlot[0]:
    ax1 = plt.subplot(gsMain[0])
    plt.axhline(0, ls=':', color='0.75')
    for i in range(len(upOddballIndexSaline)):
        plt.plot(barLoc, [upOddballIndexSaline[i], upOddballIndexDOI[i]], '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], len(upOddballIndexSaline)), upOddballIndexSaline, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[1], len(upOddballIndexDOI)), upOddballIndexDOI, 'o', color=colors['doi'])

    ax1.set_xlim([-1,1])
    ax1.set_xticks(barLoc)
    ax1.set_xticklabels(['Saline', 'DOI'])
    ax1.set_ylabel('Oddball enhancement index', fontsize = fontsize)
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax1, fontsize)
    extraplots.boxoff(ax1)
    extraplots.significance_stars(barLoc, 0.55, 0.02, color='0.75', starSize=10, gapFactor=0.1)


if figsToPlot[1]:
    ax2 = plt.subplot(gsMain[1])
    for i in range(len(downOddballIndexSaline)):
        plt.plot(barLoc, [downOddballIndexSaline[i], downOddballIndexDOI[i]], '-', color = 'black')

    plt.plot(np.tile(barLoc[0], len(downOddballIndexSaline)), downOddballIndexDOI, 'o', color = 'blue')
    plt.plot(np.tile(barLoc[1], len(downOddballIndexSaline)), downOddballIndexDOI, 'o', color = 'red')

    ax2.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
    ax2.set_xticks(barLoc)
    ax2.set_xticklabels(['saline', 'DOI'])
    ax2.set_ylabel("downOddballIndex")
    #axes.set_ylim(0,5)
    #extraplots.boxoff(axes)
    extraplots.set_ticks_fontsize(ax2, 20)


upStat, upP = scipy.stats.wilcoxon(upOddballIndexSaline, upOddballIndexDOI)
print(f'-- FM up --')
print(np.median(upOddballIndexSaline))
print(np.median(upOddballIndexDOI))
print(f'p = {upP}\n')

downStat, downP = scipy.stats.wilcoxon(downOddballIndexSaline, downOddballIndexDOI)
print(f'-- FM down --')
print(np.median(downOddballIndexSaline))
print(np.median(downOddballIndexDOI))
print(f'p = {downP}\n')

plt.show()

figName = 'acid006_comparison_oddball_index'
if SAVE_FIGURE:
    extraplots.save_figure(figName, 'png', [2.75, 5], outputDir='/tmp/', facecolor='w')
