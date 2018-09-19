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
import subjects_info

#dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'inactivation_cells.h5')
dbFilename = os.path.join(settings.DATABASE_PATH,'inactivation_cells.h5')
db = celldatabase.load_hdf(dbFilename)

figName = 'figure_inhibitory_cell_inactivation'

#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_ARCHT_MICE = subjects_info.PV_ARCHT_MICE
SOM_ARCHT_MICE = subjects_info.SOM_ARCHT_MICE

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = db.query("isiViolations<0.02")# or modifiedISI<0.02")
bestCells = bestCells.query('spikeShapeQuality>2.5 and laserChangeFR>0') #good cells with increased FR to laser to try to avoid PV and SOM cells
bestCells = bestCells.query('tuningFitR2>@R2CUTOFF and octavesFromPrefFreq<@OCTAVESCUTOFF and sustainedSoundResponsePVal<@SOUND_RESPONSE_PVAL')

PVCells = bestCells.loc[bestCells['subject'].isin(PV_ARCHT_MICE)]
SOMCells = bestCells.loc[bestCells['subject'].isin(SOM_ARCHT_MICE)]

# -- get suppression indices for all cells responsive during sustained portion of response with and without laser --
PVsustainedSuppressionNoLaser = PVCells['sustainedSuppressionIndexNoLaser']
SOMsustainedSuppressionNoLaser = SOMCells['sustainedSuppressionIndexNoLaser']

PVsustainedSuppressionLaser = PVCells['sustainedSuppressionIndexNoLaser']
SOMsustainedSuppressionLaser = SOMCells['sustainedSuppressionIndexNoLaser']

fitPVsustainedSuppressionNoLaser = PVCells['fitSustainedSuppressionIndexNoLaser']
fitSOMsustainedSuppressionNoLaser = SOMCells['fitSustainedSuppressionIndexNoLaser']

fitPVsustainedSuppressionLaser = PVCells['fitSustainedSuppressionIndexLaser']
fitSOMsustainedSuppressionLaser = SOMCells['fitSustainedSuppressionIndexLaser']

# -- get preferred bandwidths for all cells responsive during sustained portion of response with and without laser--
# PVsustainedPrefBWNoLaser = PVCells['sustainedPrefBandwidthNoLaser']
# SOMsustainedPrefBWNoLaser = SOMCells['sustainedPrefBandwidthNoLaser']
# 
# PVsustainedPrefBWLaser = PVCells['sustainedPrefBandwidthLaser']
# SOMsustainedPrefBWLaser = SOMCells['sustainedPrefBandwidthLaser']

fitPVsustainedPrefBWNoLaser = PVCells['fitSustainedPrefBandwidthNoLaser']
fitSOMsustainedPrefBWNoLaser = SOMCells['fitSustainedPrefBandwidthNoLaser']

fitPVsustainedPrefBWLaser = PVCells['fitSustainedPrefBandwidthLaser']
fitSOMsustainedPrefBWLaser = SOMCells['fitSustainedPrefBandwidthLaser']
        
# -- save photoidentified suppression scores --
outputFile = 'all_inactivated_cells_stats.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         rawPVsustainedSuppressionNoLaser = PVsustainedSuppressionNoLaser,
         rawSOMsustainedSuppressionNoLaser = SOMsustainedSuppressionNoLaser,
         rawPVsustainedSuppressionLaser = PVsustainedSuppressionLaser,
         rawSOMsustainedSuppressionLaser = SOMsustainedSuppressionLaser,
         fitPVsustainedSuppressionNoLaser = fitPVsustainedSuppressionNoLaser,
         fitSOMsustainedSuppressionNoLaser = fitSOMsustainedSuppressionNoLaser,
         fitPVsustainedSuppressionLaser = fitPVsustainedSuppressionLaser,
         fitSOMsustainedSuppressionLaser = fitSOMsustainedSuppressionLaser,
#          rawPVsustainedPrefBWNoLaser = PVsustainedPrefBWNoLaser,
#          rawSOMsustainedPrefBWNoLaser = SOMsustainedPrefBWNoLaser,
#          rawPVsustainedPrefBWLaser = PVsustainedPrefBWLaser,
#          rawSOMsustainedPrefBWLaser = SOMsustainedPrefBWLaser,
         fitPVsustainedPrefBWNoLaser = fitPVsustainedPrefBWNoLaser,
         fitSOMsustainedPrefBWNoLaser = fitSOMsustainedPrefBWNoLaser,
         fitPVsustainedPrefBWLaser = fitPVsustainedPrefBWLaser,
         fitSOMsustainedPrefBWLaser = fitSOMsustainedPrefBWLaser)
print outputFile + " saved"