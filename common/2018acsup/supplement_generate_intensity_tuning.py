''' 
Generates inputs to plot SI vs some measure of suppression by sounds of different intensities

Inputs generated:
* suppression indices for all cells
* suppression index for white noise at different intensities
* difference/sum for all cell's bandwidth and tuning data
'''

import os
import pandas as pd
import numpy as np
import scipy.stats

from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

import figparams
import studyparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
#dbFilename = '/home/jarauser/data/database/photoidentification_cells.h5'
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_intensity_tuning'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)


# # -- find all cells with a noise "suppression" calculated --
# bestCells = db[db['noiseSustainedSI'].notnull()]
# bestCells = bestCells[bestCells['sustainedSoundResponsePVal']<studyparams.SOUND_RESPONSE_PVAL]

# -- find all good cells --
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

# -- find different cell types --
PVCells = bestCells.query(studyparams.PV_CELLS)
SOMCells = bestCells.query(studyparams.SOM_CELLS)
ExCells = bestCells.query(studyparams.EXC_CELLS)

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = PVCells['sustainedSuppressionIndex']
SOMsustainedSuppression = SOMCells['sustainedSuppressionIndex']
ExsustainedSuppression = ExCells['sustainedSuppressionIndex']

PVsustainedSuppressionPVal = PVCells['sustainedSuppressionpVal']
SOMsustainedSuppressionPVal = SOMCells['sustainedSuppressionpVal']
ExsustainedSuppressionPVal = ExCells['sustainedSuppressionpVal']

fitPVsustainedSuppression = PVCells['fitSustainedSuppressionIndex']
fitSOMsustainedSuppression = SOMCells['fitSustainedSuppressionIndex']
fitExsustainedSuppression = ExCells['fitSustainedSuppressionIndex']

fitPVsustainedSuppressionNoZero = PVCells['fitSustainedSuppressionIndexnoZero']
fitSOMsustainedSuppressionNoZero = SOMCells['fitSustainedSuppressionIndexnoZero']
fitExsustainedSuppressionNoZero = ExCells['fitSustainedSuppressionIndexnoZero']

PVsustainedNoiseSuppression = PVCells['noiseSustainedSI']
SOMsustainedNoiseSuppression = SOMCells['noiseSustainedSI']
ExsustainedNoiseSuppression = ExCells['noiseSustainedSI']

# -- get difference/sum for different bandwidths --
PVhighSpikeArray = PVCells['bandwidthSustainedSpikeArrayHighAmp']
PVlowSpikeArray = PVCells['bandwidthSustainedSpikeArrayLowAmp']
PVdiffSum = (PVhighSpikeArray-PVlowSpikeArray)/(PVhighSpikeArray+PVlowSpikeArray)
PVprefBW = PVCells['fitSustainedPrefBandwidthnoZero']

SOMhighSpikeArray = SOMCells['bandwidthSustainedSpikeArrayHighAmp']
SOMlowSpikeArray = SOMCells['bandwidthSustainedSpikeArrayLowAmp']
SOMdiffSum = (SOMhighSpikeArray-SOMlowSpikeArray)/(SOMhighSpikeArray+SOMlowSpikeArray)
SOMprefBW = SOMCells['fitSustainedPrefBandwidthnoZero']

ExhighSpikeArray = ExCells['bandwidthSustainedSpikeArrayHighAmp']
ExlowSpikeArray = ExCells['bandwidthSustainedSpikeArrayLowAmp']
ExdiffSum = (ExhighSpikeArray-ExlowSpikeArray)/(ExhighSpikeArray+ExlowSpikeArray)
ExprefBW = ExCells['fitSustainedPrefBandwidthnoZero']


outputFile = 'all_cells_intensity_tuning.npz'

outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVsustainedSuppression = PVsustainedSuppression, PVsustainedNoiseSuppression = PVsustainedNoiseSuppression, fitPVsustainedSuppression = fitPVsustainedSuppression, fitPVsustainedSuppressionNoZero = fitPVsustainedSuppressionNoZero,
         SOMsustainedSuppression = SOMsustainedSuppression, SOMsustainedNoiseSuppression = SOMsustainedNoiseSuppression, fitSOMsustainedSuppression = fitSOMsustainedSuppression, fitSOMsustainedSuppressionNoZero = fitSOMsustainedSuppressionNoZero,
         ExsustainedSuppression = ExsustainedSuppression, ExsustainedNoiseSuppression = ExsustainedNoiseSuppression, fitExsustainedSuppression = fitExsustainedSuppression, fitExsustainedSuppressionNoZero = fitExsustainedSuppressionNoZero,
         PVsustainedSuppressionPVal = PVsustainedSuppressionPVal, SOMsustainedSuppressionPVal = SOMsustainedSuppressionPVal, ExsustainedSuppressionPVal = ExsustainedSuppressionPVal,
         PVdiffSum = PVdiffSum, SOMdiffSum = SOMdiffSum, ExdiffSum = ExdiffSum,
         PVprefBW = PVprefBW, SOMprefBW = SOMprefBW, ExprefBW = ExprefBW)
print outputFile + " saved"