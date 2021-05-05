import os
import sys
import numpy as np
from scipy import stats

from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import settings
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis

from jaratest.anna.analysis import band_plots

import studyparams
import figparams

#dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'band075_cells.h5')
dbFilename = os.path.join(settings.FIGURES_DATA_PATH, 'band075_cells.h5')
db = celldatabase.load_hdf(dbFilename)

bestCells = db.query('isiViolations<0.02 and spikeShapeQuality>2.5 and soundFR>1')
print(len(bestCells))

basepVals = bestCells['baselinepVal']
print(np.sum(basepVals<0.05))

soundpVals = bestCells['soundpVal']
soundTestStatistic = bestCells['soundTestStatistic']
soundpVals = soundpVals[soundTestStatistic<0]
print(np.sum(soundpVals<0.05))

soundFR = bestCells['soundFR']
soundLaserFR = bestCells['soundLaserFR']
pVal = stats.wilcoxon(soundFR, soundLaserFR)[1]
print(f'Laser on vs off sound-evoked FR pVal: {pVal}')

# for indCell, cell in bestCells.iterrows():
#     band_plots.plot_laser_bandwidth_summary(cell, 5)