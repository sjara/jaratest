''' 
Generates inputs to plot mean/median responses for all recorded PV/SOM/putative pyramidal cells according to the AM rate chosen for each cell

Inputs generated:
* AM rate used (for sorting)
* suppression indices for all cells
* preferred bandwidth for all cells
* "onsetivity"
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
dbFilename = os.path.join(settings.DATABASE_PATH,'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_characterisation_of_responses_by_AM_rate'

#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_CHR2_MICE = subjects_info.PV_CHR2_MICE
SOM_CHR2_MICE = subjects_info.SOM_CHR2_MICE

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = db.query("isiViolations<0.02 or modifiedISI<0.02")
bestCells = bestCells.query('spikeShapeQuality>2.5 and tuningFitR2>@R2CUTOFF and octavesFromPrefFreq<@OCTAVESCUTOFF')

# -- find cells responsive to laser pulse or train --
laserResponsiveCells = bestCells.query("laserPVal<0.001 and laserUStat>0")
PVCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(PV_CHR2_MICE)]
SOMCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(SOM_CHR2_MICE)]

# -- find cells unresponsive to laser (putative pyramidal) --
ExCells = bestCells.query("laserPVal>0.05 and laserTrainPVal>0.05")
ExCells = ExCells.loc[ExCells['subject'].isin(SOM_CHR2_MICE)]

# -- PV, SOM, Ex cells sound responsive during sustained portion of bw trials --
sustPVCells = PVCells.loc[PVCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]
sustSOMCells = SOMCells.loc[SOMCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]
sustExCells = ExCells.loc[ExCells['sustainedSoundResponsePVal']<SOUND_RESPONSE_PVAL]

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustPVCells['sustainedSuppressionIndex']
SOMsustainedSuppression = sustSOMCells['sustainedSuppressionIndex']
ExsustainedSuppression = sustExCells['sustainedSuppressionIndex']

fitPVsustainedSuppression = sustPVCells['fitSustainedSuppressionIndex']
fitSOMsustainedSuppression = sustSOMCells['fitSustainedSuppressionIndex']
fitExsustainedSuppression = sustExCells['fitSustainedSuppressionIndex']

# -- get preferred bandwidths for all cells responsive during sustained portion of response --
PVsustainedPrefBW = sustPVCells['sustainedPrefBandwidth']
SOMsustainedPrefBW = sustSOMCells['sustainedPrefBandwidth']
ExsustainedPrefBW = sustExCells['sustainedPrefBandwidth']

fitPVsustainedPrefBW = sustPVCells['fitSustainedPrefBandwidth']
fitSOMsustainedPrefBW = sustSOMCells['fitSustainedPrefBandwidth']
fitExsustainedPrefBW = sustExCells['fitSustainedPrefBandwidth']

# -- get proportions of response that happens at onset --
PVonsetProp = sustPVCells['proportionSpikesOnset']
SOMonsetProp = sustSOMCells['proportionSpikesOnset']
ExonsetProp = sustExCells['proportionSpikesOnset']
PVSOMonsetProppVal = scipy.stats.ranksums(PVonsetProp,SOMonsetProp)[1]
PVExonsetProppVal = scipy.stats.ranksums(PVonsetProp,ExonsetProp)[1]
ExSOMonsetProppVal = scipy.stats.ranksums(ExonsetProp,SOMonsetProp)[1]

# -- get AM rates used for all cells --
ExAMrate = sustExCells['AMRate']
PVAMrate = sustPVCells['AMRate']
SOMAMrate = sustSOMCells['AMRate']

# -- save photoidentified suppression scores --
outputFile = 'all_photoidentified_cells_stats_by_AM_rate.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVonsetProp = PVonsetProp,
         SOMonsetProp = SOMonsetProp,
         ExcOnsetProp = ExonsetProp,
         PVSOMonsetProppVal = PVSOMonsetProppVal,
         PVExconsetProppVal = PVExonsetProppVal,
         ExcSOMonsetProppVal = ExSOMonsetProppVal,
         rawPVsustainedSuppressionInd = PVsustainedSuppression,
         rawSOMsustainedSuppressionInd = SOMsustainedSuppression,
         rawExcSustainedSuppressionInd = ExsustainedSuppression,
         fitPVsustainedSuppressionInd = fitPVsustainedSuppression,
         fitSOMsustainedSuppressionInd = fitSOMsustainedSuppression,
         fitExcSustainedSuppressionInd = fitExsustainedSuppression,
         rawPVsustainedPrefBW = PVsustainedPrefBW,
         rawSOMsustainedPrefBW = SOMsustainedPrefBW,
         rawExcSustainedPrefBW = ExsustainedPrefBW,
         fitPVsustainedPrefBW = fitPVsustainedPrefBW,
         fitSOMsustainedPrefBW = fitSOMsustainedPrefBW,
         fitExcSustainedPrefBW = fitExsustainedPrefBW,
         ExAMrate = ExAMrate,
         PVAMrate = PVAMrate,
         SOMAMrate = SOMAMrate)
print outputFile + " saved"