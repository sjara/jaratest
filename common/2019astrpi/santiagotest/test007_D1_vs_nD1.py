"""
Check that our selection of D1 and nD1 is appropriate.

To check:
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
TEMPDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,
                      'tempdb_subset_good.h5')

toExclude = np.loadtxt(os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,
                                    'cell_indices_manually_removed.txt'), dtype=int)

columnsToLoad = ['index', 'spikeShape', 'laserpulse_pVal', 'laserpulse_SpikeCountChange',
                 'laserpulse_responseSpikeCount']
cellDB = celldatabase.load_hdf(TEMPDB,  columns=columnsToLoad)
#print(len(cellDB))
cellDB.drop(toExclude, inplace=True, errors='ignore')
#print(len(cellDB))
cellIndices = cellDB.index

#sys.exit()

spikeShape = np.array(list(cellDB['spikeShape']))

peakRange = slice(0,20)
peakEachSpike = -np.min(spikeShape[:,peakRange], axis=1)
normedSpikeShape = spikeShape/peakEachSpike[:, np.newaxis]

cellDB['normedSpikeShape'] = list(normedSpikeShape)



laserpulse_pVal_threshold = 0.05  # 0.001 if want to be extra sure not to include false positives
laserpulse_responseCount_threshold = 0.5
D1_CELLS = 'laserpulse_pVal<{} and laserpulse_SpikeCountChange>0 and laserpulse_responseSpikeCount>{}'.format(laserpulse_pVal_threshold, laserpulse_responseCount_threshold)
nD1_CELLS = 'not (laserpulse_pVal<{} and laserpulse_SpikeCountChange>0)'.format(laserpulse_pVal_threshold)
dbD1 = cellDB.query(D1_CELLS)
dbnD1 = cellDB.query(nD1_CELLS)
#dbD1 = cellDB.query(studyparams.D1_CELLS)
#dbnD1 = cellDB.query(studyparams.nD1_CELLS)


spikeShapeD1 = np.array(list(dbD1['normedSpikeShape']))
spikeShapeNonD1 = np.array(list(dbnD1['normedSpikeShape']))

SAMPLERATE = 30000
nSamples = spikeShape.shape[1]
timeVec = (np.arange(nSamples)-8)/SAMPLERATE

if 1:
    plt.clf()
    for counter, indc in enumerate(cellIndices):
        plt.plot(1e6*timeVec, normedSpikeShape[counter,:])
        plt.title(indc)
        plt.waitforbuttonpress()
        #plt.draw()

# -- Plot all --
# plot(spikeShapeNonD1.T)  
# plot(spikeShapeD1.T)

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

