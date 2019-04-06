''' 
Generates inputs to plot mean/median responses for all recorded PV/SOM/putative pyramidal cells

Inputs generated:
* suppression indices for all cells
* preferred bandwidth for all cells
* median firing rates for all cells
* PSTHs for high bandwidth responses
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

figName = 'supplement_figure_characterisation_of_responses_pure_tone_fit'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected and have sustained response
bestCells = db.query(studyparams.SINGLE_UNITS)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

sustPVCells = bestCells.query(studyparams.PV_CELLS)
sustSOMCells = bestCells.query(studyparams.SOM_CELLS)
sustExCells = bestCells.query(studyparams.EXC_CELLS)

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustPVCells['sustainedSuppressionIndexPureTone']
SOMsustainedSuppression = sustSOMCells['sustainedSuppressionIndexPureTone']
ExsustainedSuppression = sustExCells['sustainedSuppressionIndexPureTone']

fitPVsustainedSuppression = sustPVCells['fitSustainedSuppressionIndexPureTone']
fitSOMsustainedSuppression = sustSOMCells['fitSustainedSuppressionIndexPureTone']
fitExsustainedSuppression = sustExCells['fitSustainedSuppressionIndexPureTone']

# -- get preferred bandwidths for all cells responsive during sustained portion of response --
PVsustainedPrefBW = sustPVCells['sustainedPrefBandwidthPureTone']
SOMsustainedPrefBW = sustSOMCells['sustainedPrefBandwidthPureTone']
ExsustainedPrefBW = sustExCells['sustainedPrefBandwidthPureTone']

fitPVsustainedPrefBW = sustPVCells['fitSustainedPrefBandwidthPureTone']
fitSOMsustainedPrefBW = sustSOMCells['fitSustainedPrefBandwidthPureTone']
fitExsustainedPrefBW = sustExCells['fitSustainedPrefBandwidthPureTone']
             
        
# -- save photoidentified suppression scores --
outputFile = 'all_photoidentified_cells_stats_pure_tone.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         rawPVsustainedSuppressionIndPureTone = PVsustainedSuppression,
         rawSOMsustainedSuppressionIndPureTone = SOMsustainedSuppression,
         rawExcSustainedSuppressionIndPureTone = ExsustainedSuppression,
         fitPVsustainedSuppressionIndPureTone = fitPVsustainedSuppression,
         fitSOMsustainedSuppressionIndPureTone = fitSOMsustainedSuppression,
         fitExcSustainedSuppressionIndPureTone = fitExsustainedSuppression,
         rawPVsustainedPrefBWPureTone = PVsustainedPrefBW,
         rawSOMsustainedPrefBWPureTone = SOMsustainedPrefBW,
         rawExcSustainedPrefBWPureTone = ExsustainedPrefBW,
         fitPVsustainedPrefBWPureTone = fitPVsustainedPrefBW,
         fitSOMsustainedPrefBWPureTone = fitSOMsustainedPrefBW,
         fitExcSustainedPrefBWPureTone = fitExsustainedPrefBW)
print outputFile + " saved"