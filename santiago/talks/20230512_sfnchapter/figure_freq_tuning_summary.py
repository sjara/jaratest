"""
Plot comparisons between responses during saline vs DOI.
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

SAVE_FIGURE = 1

# Change to cellDB 
filename = '/var/tmp/acid006_celldb.h5'
celldb = celldatabase.load_hdf(filename)

fontsize = 16
figsToPlot = [1, 0, 0]

#fig, axes = plt.subplots(figsize = (10,10), fig=plt.gcf())
fig = plt.gcf()
gsMain = gs.GridSpec(1, np.sum(figsToPlot))
gsMain.update(top=0.95, bottom=0.1, left=0.275, right=0.95, wspace=0.3, hspace=0.075)

#plt.subplots_adjust(wspace=1)
barLoc = np.array([-0.6, 0.6])

colors = {'saline':cp.TangoPalette['SkyBlue2'], 'doi': cp.TangoPalette['ScarletRed1']}


baseAvgFiringRateSalineColumn= celldb['baselineFiringRatePureTonesSaline']
baseAvgFiringRateDOIColumn= celldb['baselineFiringRatePureTonesDOI']

stimAvgFiringRateSalineColumn= celldb['stimFiringRatePureTonesSaline']
stimAvgFiringRateDOIColumn= celldb['stimFiringRatePureTonesDOI']

stimMaxFiringRatePureTonesSaline= celldb['stimMaxFiringRatePureTonesSaline']
stimMaxFiringRatePureTonesDOI= celldb['stimMaxFiringRatePureTonesDOI']



responseMagnitude = (celldb['stimFiringRatePureTonesSaline'] -
                     celldb['baselineFiringRatePureTonesSaline'])

firingThreshold = 5
selectedCells = ((stimAvgFiringRateSalineColumn > firingThreshold) |
                 (stimAvgFiringRateDOIColumn > firingThreshold)) & (responseMagnitude > 0)
#selectedCells = np.ones(len(celldb), dtype=bool)

stimAvgFiringRateSaline = stimAvgFiringRateSalineColumn[selectedCells].to_numpy()
stimAvgFiringRateDOI = stimAvgFiringRateDOIColumn[selectedCells].to_numpy()
baseAvgFiringRateSaline = baseAvgFiringRateSalineColumn[selectedCells].to_numpy()
baseAvgFiringRateDOI = baseAvgFiringRateDOIColumn[selectedCells].to_numpy()
stimMaxFiringRateSaline = stimMaxFiringRatePureTonesSaline[selectedCells].to_numpy()
stimMaxFiringRateDOI = stimMaxFiringRatePureTonesDOI[selectedCells].to_numpy()

nCells = len(stimAvgFiringRateSaline)

if figsToPlot[0]:
    ax1 = plt.subplot(gsMain[0])
    for cellInd in range(len(stimAvgFiringRateSaline)):
        plt.plot(barLoc, [stimAvgFiringRateSaline[cellInd], stimAvgFiringRateDOI[cellInd]],
                 '-', color = '0.5')

    plt.plot(np.tile(barLoc[0], nCells), stimAvgFiringRateSaline, 'o', color=colors['saline'])
    plt.plot(np.tile(barLoc[1], nCells), stimAvgFiringRateDOI, 'o', color = colors['doi'])

    #ax1.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
    ax1.set_xlim([-1,1])
    ax1.set_xticks(barLoc)
    ax1.set_xticklabels(['Saline', 'DOI'])
    ax1.set_ylabel("Firing rate (spk/s)", fontsize = fontsize)
    #axes.set_ylim(5,40)
    #plt.title("Average Stim Firing Rate by Drug Condition")
    #extraplots.boxoff(ax1)
    extraplots.set_ticks_fontsize(ax1, fontsize)
    extraplots.boxoff(ax1)
    extraplots.significance_stars(barLoc, 65, 2, color='0.75', starSize=10, gapFactor=0.1)

if figsToPlot[1]:
    ax2 = plt.subplot(gsMain[1])
    for cellInd in range(len(baseAvgFiringRateSaline)):
        plt.plot(barLoc, [baseAvgFiringRateSaline[cellInd], baseAvgFiringRateDOI[cellInd]],
                 '-', color = 'black')

    plt.plot(np.tile(barLoc[0], len(baseAvgFiringRateSaline)), baseAvgFiringRateDOI, 'o', color = 'blue')
    plt.plot(np.tile(barLoc[1], len(baseAvgFiringRateSaline)), baseAvgFiringRateDOI, 'o', color = 'red')

    ax2.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
    ax2.set_xticks(barLoc)
    ax2.set_xticklabels(['saline', 'DOI'])
    ax2.set_ylabel("Firing rate (spk/s)", fontsize = 21)
    #axes.set_ylim(5,40)
    plt.title("Average Stim Firing Rate by Drug Condition")
    #extraplots.boxoff(ax2)
    extraplots.set_ticks_fontsize(ax2, 20)

if figsToPlot[2]:
    ax3 = plt.subplot(gsMain[2])
    for cellInd in range(len(stimMaxFiringRateSaline)):
        plt.plot(barLoc, [stimMaxFiringRateSaline[cellInd], stimMaxFiringRatePureTonesDOI[cellInd]],
                 '-', color = 'black')

    plt.plot(np.tile(barLoc[0], len(stimMaxFiringRateSaline)), stimMaxFiringRateDOI, 'o', color = 'blue')
    plt.plot(np.tile(barLoc[1], len(stimMaxFiringRateSaline)), stimMaxFiringRateDOI, 'o', color = 'red')

    ax3.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
    ax3.set_xticks(barLoc)
    ax3.set_xticklabels(['saline', 'DOI'])
    ax3.set_ylabel("Firing rate (spk/s)", fontsize = 21)
    #axes.set_ylim(5,40)
    plt.title("Average Stim Firing Rate by Drug Condition")
    #extraplots.boxoff(ax2)
    extraplots.set_ticks_fontsize(ax3, 20)

plt.show()

stimStat, stimP = scipy.stats.wilcoxon(stimAvgFiringRateSaline, stimAvgFiringRateDOI)
print(f'-- Average firing --')
print(np.median(stimAvgFiringRateSaline))
print(np.median(stimAvgFiringRateDOI))
print(f'p = {stimP}\n')

baseStat, baseP = scipy.stats.wilcoxon(baseAvgFiringRateSaline, baseAvgFiringRateDOI)
print(f'-- Baseline firing --')
print(np.median(baseAvgFiringRateSaline))
print(np.median(baseAvgFiringRateDOI))
print(f'p = {baseP}\n')

maxStat, maxP = scipy.stats.wilcoxon(stimMaxFiringRateSaline, stimMaxFiringRateDOI)
print(f'-- Max firing --')
print(np.median(stimMaxFiringRateSaline))
print(np.median(stimMaxFiringRateDOI))
print(f'p = {maxP}\n')

figName = 'acid006_comparison_avg_firing_tuning'
if SAVE_FIGURE:
    extraplots.save_figure(figName, 'png', [2.5, 5], outputDir='/tmp/', facecolor='w')
