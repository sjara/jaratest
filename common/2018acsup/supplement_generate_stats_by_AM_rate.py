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
import studyparams

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'supplement_figure_characterisation_of_responses_by_AM_rate'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)


# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
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