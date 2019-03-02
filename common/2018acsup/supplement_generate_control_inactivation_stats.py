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

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = db.query("isiViolations<0.02")# or modifiedISI<0.02")
bestCells = bestCells.query('spikeShapeQuality>2.5 and controlSession==1') #good cells with increased FR to laser to try to avoid PV and SOM cells
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

meanPVsupNoLaser = np.mean(fitPVsustainedSuppressionNoLaser)
semPVsupNoLaser = scipy.stats.sem(fitPVsustainedSuppressionNoLaser)

meanSOMsupNoLaser = np.mean(fitSOMsustainedSuppressionNoLaser)
semSOMsupNoLaser = scipy.stats.sem(fitSOMsustainedSuppressionNoLaser)

meanPVsupLaser = np.mean(fitPVsustainedSuppressionLaser)
semPVsupLaser = scipy.stats.sem(fitPVsustainedSuppressionLaser)

meanSOMsupLaser = np.mean(fitSOMsustainedSuppressionLaser)
semSOMsupLaser = scipy.stats.sem(fitSOMsustainedSuppressionLaser)

# --- get changes in sound response with and without laser ---

fitPVpeakChangeFR = PVCells['fitPeakChangeFR']
fitPVWNChangeFR = PVCells['fitWNChangeFR']

fitSOMpeakChangeFR = SOMCells['fitPeakChangeFR']
fitSOMWNChangeFR = SOMCells['fitWNChangeFR']

meanPVpeakChange = np.mean(fitPVpeakChangeFR)
semPVpeakChange = scipy.stats.sem(fitPVpeakChangeFR)

meanPVWNChange = np.mean(fitPVWNChangeFR)
semPVWNChange = scipy.stats.sem(fitPVWNChangeFR)

meanSOMpeakChange = np.mean(fitSOMpeakChangeFR)
semSOMpeakChange = scipy.stats.sem(fitSOMpeakChangeFR)

meanSOMWNChange = np.mean(fitSOMWNChangeFR)
semSOMWNChange = scipy.stats.sem(fitSOMWNChangeFR)

# --- get changes in baseline FR with and without laser ---

PVbaselineNoLaser = PVCells['baselineFRnoLaser']
PVbaselineLaser = PVCells['baselineFRLaser']

SOMbaselineNoLaser = SOMCells['baselineFRnoLaser']
SOMbaselineLaser = SOMCells['baselineFRLaser']
        
# -- save photoidentified suppression scores --
outputFile = 'control_inactivated_cells_stats.npz'
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
         meanPVsupLaser = meanPVsupLaser, semPVsupLaser = semPVsupLaser,
         meanPVsupNoLaser = meanPVsupNoLaser, semPVsupNoLaser = semPVsupNoLaser,
         meanSOMsupLaser = meanSOMsupLaser, semSOMsupLaser = semSOMsupLaser,
         meanSOMsupNoLaser = meanSOMsupNoLaser, semSOMsupNoLaser = semSOMsupNoLaser,
         meanPVpeakChange = meanPVpeakChange, semPVpeakChange = semPVpeakChange,
         meanPVWNChange = meanPVWNChange, semPVWNChange = semPVWNChange,
         meanSOMpeakChange = meanSOMpeakChange, semSOMpeakChange = semSOMpeakChange,
         meanSOMWNChange = meanSOMWNChange, semSOMWNChange = semSOMWNChange,
         fitPVpeakChangeFR = fitPVpeakChangeFR,
         fitPVWNChangeFR = fitPVWNChangeFR,
         fitSOMpeakChangeFR = fitSOMpeakChangeFR,
         fitSOMWNChangeFR = fitSOMWNChangeFR,
         PVbaselineNoLaser = PVbaselineNoLaser, PVbaselineLaser = PVbaselineLaser,
         SOMbaselineNoLaser = SOMbaselineNoLaser, SOMbaselineLaser = SOMbaselineLaser)
print outputFile + " saved"