"""
Show scatter plot of spontaneous firing rate vs spike width to help identify different cell classes.
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


laserPeriod = '200'
laserPval = 'laserpulsePval' + laserPeriod
laserBaseline = 'laserpulseBaselineSpikeCount' + laserPeriod
laserResponse = 'laserpulseResponseSpikeCount' + laserPeriod
laserChange = 'laserpulseSpikeCountChange' + laserPeriod

dbName = 'astrpi_all_cells_20210514.h5'
#dbName = 'astrpi_all_cells_tuning_20200304.h5'
#dbName = 'tempdb_subset_good.h5'
#TEMPDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 'tempdb.h5')
TEMPDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, dbName)

toExclude = np.loadtxt(os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,
                                    'cell_indices_manually_removed.txt'), dtype=int)

#columnsToLoad = ['index', 'spikeShape', 'laserpulse_pVal', 'laserpulse_SpikeCountChange',
#                 'laserpulse_responseSpikeCount', 'laserpulse_baselineSpikeCount']
columnsToLoad = ['index', 'spikeShape', laserPval, laserChange, laserBaseline, laserResponse]
'''
columnsToLoad = ['index', 'spikeShape',
                 'laserpulsePval', 'laserpulseFRChange',
                 'laserpulseResponseFR', 'laserpulseBaselineFR',
                 'laserpulsePval50', 'laserpulseFRChange50',
                 'laserpulseResponseFR50', 'laserpulseBaselineFR50',
                 'laserpulsePval200', 'laserpulseFRChange200',
                 'laserpulseResponseFR200', 'laserpulseBaselineFR200']
'''

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

SAMPLERATE = 30000
nSamples = spikeShape.shape[1]
timeVec = (np.arange(nSamples)-8)/SAMPLERATE

# hist(cellDB['laserpulse_baselineSpikeCount'],arange(0,1,0.02))

# -- Calculate spike width --
mainPeakIndex = np.argmin(normedSpikeShape, axis=1) # Sodium peak
reboundPeakIndex = np.argmax(normedSpikeShape[:,8:], axis=1)+8 # Potassium peak
spikeWidth = (reboundPeakIndex-mainPeakIndex)/SAMPLERATE # In seconds
cellDB['spikeWidth'] = spikeWidth

# -- Laser modulation index --
#laserModIndex = (cellDB['laserpulse_responseSpikeCount']-cellDB['laserpulse_baselineSpikeCount'])/\
#                (cellDB['laserpulse_responseSpikeCount']+cellDB['laserpulse_baselineSpikeCount'])
laserModIndex = (cellDB[laserResponse]-cellDB[laserBaseline])/\
                (cellDB[laserResponse]+cellDB[laserBaseline])
cellDB['laserModIndex'] = laserModIndex

# CAREFUL: temporary fix
#cellDB['laserModIndex'] = cellDB['laserModIndex'].fillna(0)
cellDB.dropna(axis=0, inplace=True)


laserpulse_pVal_threshold = 0.05  # 0.001 if want to be extra sure not to include false positives
laserpulse_responseCount_threshold = 0.5
#D1_CELLS = 'laserpulse_pVal<{} and laserpulse_SpikeCountChange>0 and laserpulse_responseSpikeCount>{}'.format(laserpulse_pVal_threshold, laserpulse_responseCount_threshold)
#nD1_CELLS = 'not (laserpulse_pVal<{} and laserpulse_SpikeCountChange>0)'.format(laserpulse_pVal_threshold)
#D1_CELLS = f'{laserPval}<{} and {laserChange}>0 and {laserResponse}>{}'.format(laserpulse_pVal_threshold, laserpulse_responseCount_threshold)
#nD1_CELLS = f'not ({laserPval}<{} and {laserChange}>0)'.format(laserpulse_pVal_threshold)
D1_CELLS = f'{laserPval}<{laserpulse_pVal_threshold} and {laserChange}>0 and {laserResponse}>{laserpulse_responseCount_threshold}'
nD1_CELLS = f'not ({laserPval}<{laserpulse_pVal_threshold} and {laserChange}>0)'
dbD1 = cellDB.query(D1_CELLS)
dbnD1 = cellDB.query(nD1_CELLS)
'''
#dbD1 = cellDB.query(studyparams.D1_CELLS)
#dbnD1 = cellDB.query(studyparams.nD1_CELLS)
spikeShapeD1 = np.array(list(dbD1['normedSpikeShape']))
spikeShapeNonD1 = np.array(list(dbnD1['normedSpikeShape']))
'''

# plt.hist2d(1e3*cellDB['spikeWidth'], cellDB['laserModIndex'],20)
#randOffset = 0.01 #0.4*(1/SAMPLERATE) * (2*np.random.rand(len(cellDB))-1)
randOffsetAll = 0.1*(2*np.random.rand(len(cellDB['spikeWidth']))-1)
randOffsetD1 = 0.1*(2*np.random.rand(len(dbD1['spikeWidth']))-1)

if 1:
    plt.clf()
    #plt.plot(1e6*spikeWidth, laserModIndex, 'ok', mfc='none')
    plt.plot(1e3*cellDB['spikeWidth']+randOffsetAll, cellDB['laserModIndex'], '.', color='0.75')
    plt.plot(1e3*dbD1['spikeWidth']+randOffsetD1, dbD1['laserModIndex'], 'or', mfc='none')
    #plt.plot(1e3*dbnD1['spikeWidth'], dbnD1['laserModIndex'], 'ob', mfc='none')
    plt.xlabel('Spike width (ms)')
    plt.ylabel('Laser Mod Index')
    plt.show()
    
if 0:
    plt.clf()
    plt.plot(spikeWidth, cellDB['laserpulse_baselineSpikeCount'], 'ok', mfc='none')
    plt.show()
    
#plt.clf(); plt.plot(1e6*timeVec, normedSpikeShape.T); plt.show()
    
if 0:
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

