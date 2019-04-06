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
import subjects_info

#dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbFilename = '/home/jarauser/data/database/photoidentification_cells.h5'
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_intensity_tuning'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_CHR2_MICE = subjects_info.PV_CHR2_MICE
SOM_CHR2_MICE = subjects_info.SOM_CHR2_MICE

# -- find all cells with a noise "suppression" calculated --
bestCells = db[db['noiseSustainedSI'].notnull()]
bestCells = bestCells[bestCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]

# -- find cells responsive to laser pulse or train --
laserResponsiveCells = bestCells.query("laserPVal<0.001 and laserUStat>0")
PVCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(PV_CHR2_MICE)]
SOMCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(SOM_CHR2_MICE)]

# -- find cells unresponsive to laser (putative pyramidal) --
#ExCells = bestCells.query("laserPVal>0.05 and laserTrainPVal>0.05")
ExCells = bestCells.query("laserUStat<0")
ExCells = ExCells.loc[ExCells['subject'].isin(SOM_CHR2_MICE)]

# -- PV, SOM, Ex cells sound responsive during sustained portion of bw trials --
sustPVCells = PVCells.loc[PVCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]
sustSOMCells = SOMCells.loc[SOMCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]
sustExCells = ExCells.loc[ExCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustPVCells['sustainedSuppressionIndex']
SOMsustainedSuppression = sustSOMCells['sustainedSuppressionIndex']
ExsustainedSuppression = sustExCells['sustainedSuppressionIndex']

PVsustainedSuppressionPVal = sustPVCells['sustainedSuppressionpVal']
SOMsustainedSuppressionPVal = sustSOMCells['sustainedSuppressionpVal']
ExsustainedSuppressionPVal = sustExCells['sustainedSuppressionpVal']

fitPVsustainedSuppression = sustPVCells['fitSustainedSuppressionIndex']
fitSOMsustainedSuppression = sustSOMCells['fitSustainedSuppressionIndex']
fitExsustainedSuppression = sustExCells['fitSustainedSuppressionIndex']

fitPVsustainedSuppressionNoZero = sustPVCells['fitSustainedSuppressionIndexnoZero']
fitSOMsustainedSuppressionNoZero = sustSOMCells['fitSustainedSuppressionIndexnoZero']
fitExsustainedSuppressionNoZero = sustExCells['fitSustainedSuppressionIndexnoZero']

PVsustainedNoiseSuppression = sustPVCells['noiseSustainedSI']
SOMsustainedNoiseSuppression = sustSOMCells['noiseSustainedSI']
ExsustainedNoiseSuppression = sustExCells['noiseSustainedSI']

# -- get difference/sum for different bandwidths --
PVhighSpikeArray = sustPVCells['bandwidthSustainedSpikeArrayHighAmp']
PVlowSpikeArray = sustPVCells['bandwidthSustainedSpikeArrayLowAmp']
PVdiffSum = (PVhighSpikeArray-PVlowSpikeArray)/(PVhighSpikeArray+PVlowSpikeArray)
PVprefBW = sustPVCells['fitSustainedPrefBandwidthnoZero']

SOMhighSpikeArray = sustSOMCells['bandwidthSustainedSpikeArrayHighAmp']
SOMlowSpikeArray = sustSOMCells['bandwidthSustainedSpikeArrayLowAmp']
SOMdiffSum = (SOMhighSpikeArray-SOMlowSpikeArray)/(SOMhighSpikeArray+SOMlowSpikeArray)
SOMprefBW = sustSOMCells['fitSustainedPrefBandwidthnoZero']

ExhighSpikeArray = sustExCells['bandwidthSustainedSpikeArrayHighAmp']
ExlowSpikeArray = sustExCells['bandwidthSustainedSpikeArrayLowAmp']
ExdiffSum = (ExhighSpikeArray-ExlowSpikeArray)/(ExhighSpikeArray+ExlowSpikeArray)
ExprefBW = sustExCells['fitSustainedPrefBandwidthnoZero']


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