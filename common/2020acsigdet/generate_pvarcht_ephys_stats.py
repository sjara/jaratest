import os
import sys
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis

#from jaratest.anna.analysis import band_plots

import studyparams
import figparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'band075_cells.h5')
# dbFilename = os.path.join(settings.FIGURES_DATA_PATH, 'band075_cells.h5')
db = celldatabase.load_hdf(dbFilename)

bestCells = db.query('isiViolations<0.02 and spikeShapeQuality>2.5 and soundFR>1')
print(f'Number of cells: {len(bestCells)}')

basepVals = bestCells['baselinepVal']
print(f'Cells with baseline change (p<0.05): {np.sum(basepVals<0.05)}')

soundpVals = bestCells['soundpVal']
soundTestStatistic = bestCells['soundTestStatistic']
soundpVals = soundpVals[soundTestStatistic<0]
print(f'Cells with sound-evoked change (p<0.05): {np.sum(soundpVals<0.05)}')

soundFR = bestCells['soundFR']
soundLaserFR = bestCells['soundLaserFR']
pVal = stats.wilcoxon(soundFR, soundLaserFR)[1]
print(f'Laser on vs off sound-evoked FR pVal: {pVal}')

changeFR = soundLaserFR - soundFR

increaseAndSignif = (changeFR>0) & (soundpVals<0.05)
print(f'Signif cells with increased sound-evoked (p<0.05): {np.sum(increaseAndSignif)}')
decreaseAndSignif = (changeFR<0) & (soundpVals<0.05)
print(f'Signif cells with increased sound-evoked (p<0.05): {np.sum(decreaseAndSignif)}')

percentChange = 100*soundLaserFR/soundFR
print(f'Mean percent change: {np.mean(percentChange)}')

plt.clf()
bins = np.linspace(-1, 4, 25)
plt.subplot(2,1,1)
plt.hist(changeFR, bins)
plt.xlabel('Change in firing rate (spks/sec)')
plt.subplot(2,1,2)
plt.hist(percentChange,25)
plt.xlabel('Change in firing rate (%)')
plt.show()

# for indCell, cell in bestCells.iterrows():
#     band_plots.plot_laser_bandwidth_summary(cell, 5)
