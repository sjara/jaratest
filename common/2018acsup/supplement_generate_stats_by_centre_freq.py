''' 
Generates inputs to plot mean/median responses for all recorded PV/SOM/putative pyramidal cells according to the centre frequency for each cell

Inputs generated:
* centre frequency (for sorting)
* R2 values
* suppression indices for all cells
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
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_gaussian_frequency_tuning_fit'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected and have sustained response
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

sustPVCells = bestCells.query(studyparams.PV_CELLS)
sustSOMCells = bestCells.query(studyparams.SOM_CELLS)
sustExCells = bestCells.query(studyparams.EXC_CELLS)

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustPVCells['sustainedSuppressionIndex']
SOMsustainedSuppression = sustSOMCells['sustainedSuppressionIndex']
ExsustainedSuppression = sustExCells['sustainedSuppressionIndex']

fitPVsustainedSuppression = sustPVCells['fitSustainedSuppressionIndex']
fitSOMsustainedSuppression = sustSOMCells['fitSustainedSuppressionIndex']
fitExsustainedSuppression = sustExCells['fitSustainedSuppressionIndex']

# -- get centre frequency for all cells --
ExbestFreq = sustExCells['prefFreq']
PVbestFreq = sustPVCells['prefFreq']
SOMbestFreq = sustSOMCells['prefFreq']

# -- get R2 values for estimation of best frequency --
ExR2 = sustExCells['tuningFitR2']
PVR2 = sustPVCells['tuningFitR2']
SOMR2 = sustSOMCells['tuningFitR2']

# -- save photoidentified suppression scores --
outputFile = 'all_photoidentified_cells_stats_by_best_freq.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         rawPVsustainedSuppressionInd = PVsustainedSuppression,
         rawSOMsustainedSuppressionInd = SOMsustainedSuppression,
         rawExcSustainedSuppressionInd = ExsustainedSuppression,
         fitPVsustainedSuppressionInd = fitPVsustainedSuppression,
         fitSOMsustainedSuppressionInd = fitSOMsustainedSuppression,
         fitExcSustainedSuppressionInd = fitExsustainedSuppression,
         ExbestFreq = ExbestFreq, PVbestFreq = PVbestFreq, SOMbestFreq = SOMbestFreq,
         ExR2 = ExR2, PVR2 = PVR2, SOMR2 = SOMR2)
print outputFile + " saved"