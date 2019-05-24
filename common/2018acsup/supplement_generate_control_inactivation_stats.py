''' 
Generates inputs to plot control responses in PV/SOM ArchT mice (laser on, not illuminating cells)

Inputs generated:
* suppression indices with and without laser
* change in firing rate with and without laser
* change in baseline firing with and without laser
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

figName = 'supplement_figure_inhibitory_cell_inactivation_control'

#dataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', figName)
dataDir = os.path.join('/home/jarauser/data/figuresdata/2018acsup', figName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_ARCHT_MICE = subjects_info.PV_ARCHT_MICE
SOM_ARCHT_MICE = subjects_info.SOM_ARCHT_MICE

# -- find PV and SOM-inactivated cells that are sound responsive
bestCells = db.query("isiViolations<0.02")# or modifiedISI<0.02")
bestCells = bestCells.query('spikeShapeQuality>2.5')
bestCells = bestCells.query('onsetSoundResponsePVal<@SOUND_RESPONSE_PVAL or sustainedSoundResponsePVal<@SOUND_RESPONSE_PVAL or soundResponsePVal<@SOUND_RESPONSE_PVAL')

PVCells = bestCells.loc[bestCells['subject'].isin(PV_ARCHT_MICE)]
SOMCells = bestCells.loc[bestCells['subject'].isin(SOM_ARCHT_MICE)]

PVControl = PVCells.loc[PVCells['controlSession']==1]
PVLaser = PVCells.loc[PVCells['controlSession']==0]

SOMControl = SOMCells.loc[SOMCells['controlSession']==1]
SOMLaser = SOMCells.loc[SOMCells['controlSession']==0]

# --- get changes in baseline FR with and without laser ---

PVcontrolBaselineNoLaser = PVControl['baselineFRnoLaser']
PVcontrolBaselineLaser = PVControl['baselineFRLaser']

SOMcontrolBaselineNoLaser = SOMControl['baselineFRnoLaser']
SOMcontrolBaselineLaser = SOMControl['baselineFRLaser']

PVbaselineNoLaser = PVLaser['baselineFRnoLaser']
PVbaselineLaser = PVLaser['baselineFRLaser']

SOMbaselineNoLaser = SOMLaser['baselineFRnoLaser']
SOMbaselineLaser = SOMLaser['baselineFRLaser']
        
# -- save photoidentified suppression scores --
outputFile = 'control_inactivated_cells_stats.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         PVControlNoLaser = PVcontrolBaselineNoLaser, PVControlLaser = PVcontrolBaselineLaser,
         PVNoLaser = PVbaselineNoLaser, PVLaser = PVbaselineLaser,
         SOMControlNoLaser = SOMcontrolBaselineNoLaser, SOMControlLaser = SOMcontrolBaselineLaser,
         SOMNoLaser = SOMbaselineNoLaser, SOMLaser = SOMbaselineLaser)
print outputFile + " saved"