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
gsMain = gs.GridSpec(1, 2, figure = fig)
plt.subplots_adjust(wspace=1)
barLoc = np.array([-0.75, 0.75])

upOddballIndexSalineColumn= celldb['upOddballIndexSaline']
upOddballIndexDOIColumn= celldb['upOddballIndexDOI']
upOddSpikesAvgSalineColumn = celldb['upOddSpikesAvgFiringRateSaline']
upOddSpikesAvgDOIColumn = celldb['upOddSpikesAvgFiringRateDOI']

downOddballIndexSalineColumn= celldb['downOddballIndexSaline']
downOddballIndexDOIColumn= celldb['downOddballIndexDOI']
downOddSpikesAvgSalineColumn = celldb['downOddSpikesAvgFiringRateSaline']
downOddSpikesAvgDOIColumn = celldb['downOddSpikesAvgFiringRateDOI']


selectedCellsUp = ((upOddSpikesAvgSalineColumn > 5) | (upOddSpikesAvgDOIColumn > 5)) #& (responseMagnitude > 0)
selectedCellsDown = ((downOddSpikesAvgSalineColumn > 5) | (downOddSpikesAvgDOIColumn > 5))

upOddballIndexSaline = upOddballIndexSalineColumn[selectedCellsUp].to_numpy()
upOddballIndexDOI = upOddballIndexDOIColumn[selectedCellsUp].to_numpy()

downOddballIndexSaline = downOddballIndexSalineColumn[selectedCellsDown].to_numpy()
downOddballIndexDOI = downOddballIndexDOIColumn[selectedCellsDown].to_numpy()



ax1 = plt.subplot(gsMain[0])
for i in range(len(upOddballIndexSaline)):
    plt.plot(barLoc, [upOddballIndexSaline[i], upOddballIndexDOI[i]], '-', color = 'black')

plt.plot(np.tile(barLoc[0], len(upOddballIndexSaline)), upOddballIndexSaline, 'o', color = 'blue')
plt.plot(np.tile(barLoc[1], len(upOddballIndexDOI)), upOddballIndexDOI, 'o', color = 'red')

ax1.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
ax1.set_xticks(barLoc)
ax1.set_xticklabels(['saline', 'DOI'])
ax1.set_ylabel("upOddballIndex")
#axes.set_ylim(0,5)
#extraplots.boxoff(axes)
extraplots.set_ticks_fontsize(ax1, 20)


ax2 = plt.subplot(gsMain[1])
for i in range(len(downOddballIndexSaline)):
    plt.plot(barLoc, [downOddballIndexSaline[i], downOddballIndexDOI[i]], '-', color = 'black')

plt.plot(np.tile(barLoc[0], len(downOddballIndexSaline)), downOddballIndexDOI, 'o', color = 'blue')
plt.plot(np.tile(barLoc[1], len(downOddballIndexSaline)), downOddballIndexDOI, 'o', color = 'red')

ax2.set_xlim(barLoc[0] - 0.2, barLoc[1] + 0.2)
ax2.set_xticks(barLoc)
ax2.set_xticklabels(['saline', 'DOI'])
ax2.set_ylabel("upOddballIndex")
#axes.set_ylim(0,5)
#extraplots.boxoff(axes)
extraplots.set_ticks_fontsize(ax2, 20)


upStat, upP = scipy.stats.wilcoxon(upOddballIndexSaline, upOddballIndexDOI)
print(scipy.stats.wilcoxon(upOddballIndexSaline, upOddballIndexDOI))
print(np.median(upOddballIndexSaline))
print(np.median(upOddballIndexDOI))

downStat, downP = scipy.stats.wilcoxon(downOddballIndexSaline, downOddballIndexDOI)
print(scipy.stats.wilcoxon(downOddballIndexSaline, downOddballIndexDOI))
print(np.median(downOddballIndexSaline))
print(np.median(downOddballIndexDOI))

plt.show()