import os
import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots

# Change to cellDB 
filename = 'c:/Users/mdhor/Documents/updatedAcid006.h5'
celldb = celldatabase.load_hdf(filename)


fig, axes = plt.subplots(figsize = (10,10))
gsMain = gs.GridSpec(1, 3, figure = fig)
plt.subplots_adjust(wspace=1)
barLoc = np.array([-0.75, 0.75])



baseAvgFiringRateSalineColumn= celldb['baselineFiringRatePureTonesSaline']
baseAvgFiringRateDOIColumn= celldb['baselineFiringRatePureTonesDOI']

stimAvgFiringRateSalineColumn= celldb['stimFiringRatePureTonesSaline']
stimAvgFiringRateDOIColumn= celldb['stimFiringRatePureTonesDOI']

stimMaxFiringRatePureTonesSaline= celldb['stimMaxFiringRatePureTonesSaline']
stimMaxFiringRatePureTonesDOI= celldb['stimMaxFiringRatePureTonesDOI']



responseMagnitude = (celldb['stimFiringRatePureTonesSaline'] - celldb['baselineFiringRatePureTonesSaline'])

selectedCells = ((stimAvgFiringRateSalineColumn > 5) | (stimAvgFiringRateDOIColumn > 5)) & (responseMagnitude > 0)

stimAvgFiringRateSaline = stimAvgFiringRateSalineColumn[selectedCells].to_numpy()
stimAvgFiringRateDOI = stimAvgFiringRateDOIColumn[selectedCells].to_numpy()
baseAvgFiringRateSaline = baseAvgFiringRateSalineColumn[selectedCells].to_numpy()
baseAvgFiringRateDOI = baseAvgFiringRateDOIColumn[selectedCells].to_numpy()
stimMaxFiringRateSaline = stimMaxFiringRatePureTonesSaline[selectedCells].to_numpy()
stimMaxFiringRateDOI = stimMaxFiringRatePureTonesDOI[selectedCells].to_numpy()


ax1 = plt.subplot(gsMain[0])
for cellInd in range(len(stimAvgFiringRateSaline)):
    plt.plot(barLoc, [stimAvgFiringRateSaline[cellInd], stimAvgFiringRateDOI[cellInd]], '-', color = 'black')

plt.plot(np.tile(barLoc[0], len(stimAvgFiringRateSaline)), stimAvgFiringRateDOI, 'o', color = 'blue')
plt.plot(np.tile(barLoc[1], len(stimAvgFiringRateSaline)), stimAvgFiringRateDOI, 'o', color = 'red')

ax1.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
ax1.set_xticks(barLoc)
ax1.set_xticklabels(['saline', 'DOI'])
ax1.set_ylabel("Firing rate (spk/s)", fontsize = 21)
#axes.set_ylim(5,40)
plt.title("Average Stim Firing Rate by Drug Condition")
#extraplots.boxoff(ax1)
extraplots.set_ticks_fontsize(ax1, 20)

ax2 = plt.subplot(gsMain[1])
for cellInd in range(len(baseAvgFiringRateSaline)):
    plt.plot(barLoc, [baseAvgFiringRateSaline[cellInd], baseAvgFiringRateDOI[cellInd]], '-', color = 'black')

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

ax3 = plt.subplot(gsMain[2])
for cellInd in range(len(stimMaxFiringRateSaline)):
    plt.plot(barLoc, [stimMaxFiringRateSaline[cellInd], stimMaxFiringRatePureTonesDOI[cellInd]], '-', color = 'black')

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

plt.show

stimStat, stimP = scipy.stats.wilcoxon(stimAvgFiringRateSaline, stimAvgFiringRateDOI)
print(scipy.stats.wilcoxon(stimAvgFiringRateSaline, stimAvgFiringRateDOI))
print(np.median(stimAvgFiringRateSaline))
print(np.median(stimAvgFiringRateDOI))

baseStat, baseP = scipy.stats.wilcoxon(baseAvgFiringRateSaline, baseAvgFiringRateDOI)
print(scipy.stats.wilcoxon(baseAvgFiringRateSaline, baseAvgFiringRateDOI))
print(np.median(baseAvgFiringRateSaline))
print(np.median(baseAvgFiringRateDOI))

maxStat, maxP = scipy.stats.wilcoxon(stimMaxFiringRateSaline, stimMaxFiringRateDOI)
print(scipy.stats.wilcoxon(stimMaxFiringRateSaline, stimMaxFiringRateDOI))
print(np.median(stimMaxFiringRateSaline))
print(np.median(stimMaxFiringRateDOI))
