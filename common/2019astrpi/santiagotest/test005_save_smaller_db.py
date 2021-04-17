"""
Attempt at working with smaller database (to check that our selection of D1 and nD1 is appropriate).

This to check:
- Are cells with NaN pvalues for laser counted as nD1?
- When is the SPIKE_QUALITY_THRESHOLD use? when creating the database?
"""

import sys
sys.path.append('..')
import os
import figparams
import studyparams
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import extraplots
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

#TEMPDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'tempdb.h5')
TEMPDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'tempdb_laser_and_noise_original.h5')

'''
d1mice = studyparams.ASTR_D1_CHR2_MICE
outputDir = figparams.FIGURE_OUTPUT_DIR 
pathtoDB =  os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                               '{}.h5'.format(studyparams.DATABASE_NAME))
figFilename = 'figure_{}'.format(studyparams.DATABASE_NAME)

# Loads database for plotting 
cellDB = celldatabase.load_hdf(pathtoDB)
goodCellDB = cellDB.query(studyparams.FIRST_FLTRD_CELLS)
keysToKeep = ['behavSuffix', 'brainArea', 'cluster', 'date', 'depth', 'ephysTime',
       'info', 'isiViolations', 'laserpulse_ZStat', 'laserpulse_baselineFR',
       'laserpulse_dFR', 'laserpulse_pVal', 'laserpulse_responseFR', 'latency',
       'maxDepth', 'nSpikes',
       'noiseburst_ZStat', 'noiseburst_baselineFR', 'noiseburst_pVal',
       'noiseburst_responseFR', 'paradigm', 'recordingSiteName', 'recordingTrack',
       'sessionType', 'spikePeakAmplitudes', 'spikePeakTimes',
       'spikeShape', 'spikeShapeQuality', 'spikeShapeSD', 'subject', 'tetrode',
       'x_coord', 'y_coord',
       'z_coord']
goodCellDB = goodCellDB[keysToKeep]

celldatabase.save_hdf(goodCellDB, TEMPDB)
'''

cellDB = celldatabase.load_hdf(TEMPDB)
cellDB = cellDB.query(studyparams.FIRST_FLTRD_CELLS)

spikeShape = np.array(list(cellDB['spikeShape']))

peakRange = slice(0,20)
peakEachSpike = -np.min(spikeShape[:,peakRange], axis=1)
normedSpikeShape = spikeShape/peakEachSpike[:, np.newaxis]

#for indc in range(100): plot(normedSpikeShape[indc,:]); plt.waitforbuttonpress()

'''
dbD1 = cellDB.query(studyparams.D1_CELLS)
spikeShape = np.array(list(dbD1['spikeShape']))
peakEachSpike = -np.min(spikeShape[:,peakRange], axis=1)
normedSpikeShape = spikeShape/peakEachSpike[:, np.newaxis]
'''

'''
FIRST_FLTRD_CELLS = 'isiViolations<{} and spikeShapeQuality>{}'.format(ISI_THRESHOLD, SPIKE_QUALITY_THRESHOLD)
D1_CELLS = 'laserpulse_pVal<{} and laserpulse_SpikeCountChange>0 and laserpulse_responseSpikeCount>{}'.format(laserpulse_pVal_threshold, laserpulse_responseCount_threshold)  # Respond to laser, thus D1-expressing cells
nD1_CELLS = 'not (laserpulse_pVal<{} and laserpulse_SpikeCountChange>0)'.format(laserpulse_pVal_threshold) # Did not respond to laser, thus non-D1-expressing cells
'''

