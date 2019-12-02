''' 
Generates inputs to plot mean/median responses for all recorded putative pyramidal cells during PV/SOM inactivation

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

dbFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'inactivation_cells_full.h5')
#dbFilename = '/tmp/inactivation_cells.h5'
db = celldatabase.load_hdf(dbFilename)

figName = 'figure_inhibitory_cell_inactivation'

dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, figName)


# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = db.query(studyparams.SINGLE_UNITS_INACTIVATION)
bestCells = bestCells.query(studyparams.GOOD_CELLS)

PVCells = bestCells.query(studyparams.PV_INACTIVATED_CELLS)
SOMCells = bestCells.query(studyparams.SOM_INACTIVATED_CELLS)

# -- get suppression indices for all cells responsive during sustained portion of response with and without laser --
rawPVsustainedSuppressionNoLaser = PVCells['sustainedSuppressionIndexNoLaser']
rawSOMsustainedSuppressionNoLaser = SOMCells['sustainedSuppressionIndexNoLaser']

rawPVsustainedSuppressionLaser = PVCells['sustainedSuppressionIndexLaser']
rawSOMsustainedSuppressionLaser = SOMCells['sustainedSuppressionIndexLaser']

rawMeanPVsupNoLaser = np.mean(rawPVsustainedSuppressionNoLaser)
rawSemPVsupNoLaser = scipy.stats.sem(rawPVsustainedSuppressionNoLaser)

rawMeanSOMsupNoLaser = np.mean(rawSOMsustainedSuppressionNoLaser)
rawSemSOMsupNoLaser = scipy.stats.sem(rawSOMsustainedSuppressionNoLaser)

rawMeanPVsupLaser = np.mean(rawPVsustainedSuppressionLaser)
rawSemPVsupLaser = scipy.stats.sem(rawPVsustainedSuppressionLaser)

rawMeanSOMsupLaser = np.mean(rawSOMsustainedSuppressionLaser)
rawSemSOMsupLaser = scipy.stats.sem(rawSOMsustainedSuppressionLaser)

fitPVsustainedSuppressionNoLaser = PVCells['fitSustainedSuppressionIndexNoLaser']
fitSOMsustainedSuppressionNoLaser = SOMCells['fitSustainedSuppressionIndexNoLaser']

fitPVsustainedSuppressionLaser = PVCells['fitSustainedSuppressionIndexLaser']
fitSOMsustainedSuppressionLaser = SOMCells['fitSustainedSuppressionIndexLaser']

fitMeanPVsupNoLaser = np.mean(fitPVsustainedSuppressionNoLaser)
fitSemPVsupNoLaser = scipy.stats.sem(fitPVsustainedSuppressionNoLaser)

fitMeanSOMsupNoLaser = np.mean(fitSOMsustainedSuppressionNoLaser)
fitSemSOMsupNoLaser = scipy.stats.sem(fitSOMsustainedSuppressionNoLaser)

fitMeanPVsupLaser = np.mean(fitPVsustainedSuppressionLaser)
fitSemPVsupLaser = scipy.stats.sem(fitPVsustainedSuppressionLaser)

fitMeanSOMsupLaser = np.mean(fitSOMsustainedSuppressionLaser)
fitSemSOMsupLaser = scipy.stats.sem(fitSOMsustainedSuppressionLaser)

fitPVsustainedSuppressionNoZeroNoLaser = PVCells['fitSustainedSuppressionIndexNoZeroNoLaser']
fitSOMsustainedSuppressionNoZeroNoLaser = SOMCells['fitSustainedSuppressionIndexNoZeroNoLaser']

fitPVsustainedSuppressionNoZeroLaser = PVCells['fitSustainedSuppressionIndexNoZeroLaser']
fitSOMsustainedSuppressionNoZeroLaser = SOMCells['fitSustainedSuppressionIndexNoZeroLaser']

fitMeanPVsupNoZeroNoLaser = np.mean(fitPVsustainedSuppressionNoZeroNoLaser)
fitSemPVsupNoZeroNoLaser = scipy.stats.sem(fitPVsustainedSuppressionNoZeroNoLaser)

fitMeanSOMsupNoZeroNoLaser = np.mean(fitSOMsustainedSuppressionNoZeroNoLaser)
fitSemSOMsupNoZeroNoLaser = scipy.stats.sem(fitSOMsustainedSuppressionNoZeroNoLaser)

fitMeanPVsupNoZeroLaser = np.mean(fitPVsustainedSuppressionNoZeroLaser)
fitSemPVsupNoZeroLaser = scipy.stats.sem(fitPVsustainedSuppressionNoZeroLaser)

fitMeanSOMsupNoZeroLaser = np.mean(fitSOMsustainedSuppressionNoZeroLaser)
fitSemSOMsupNoZeroLaser = scipy.stats.sem(fitSOMsustainedSuppressionNoZeroLaser)

# fitPVsustainedSuppressionPureToneNoLaser = PVCells['fitSustainedSuppressionIndexPureToneNoLaser']
# fitSOMsustainedSuppressionPureToneNoLaser = SOMCells['fitSustainedSuppressionIndexPureToneNoLaser']
# 
# fitPVsustainedSuppressionPureToneLaser = PVCells['fitSustainedSuppressionIndexPureToneLaser']
# fitSOMsustainedSuppressionPureToneLaser = SOMCells['fitSustainedSuppressionIndexPureToneLaser']
# 
# fitMeanPVsupPureToneNoLaser = np.mean(fitPVsustainedSuppressionPureToneNoLaser)
# fitSemPVsupPureToneNoLaser = scipy.stats.sem(fitPVsustainedSuppressionPureToneNoLaser)
# 
# fitMeanSOMsupPureToneNoLaser = np.mean(fitSOMsustainedSuppressionPureToneNoLaser)
# fitSemSOMsupPureToneNoLaser = scipy.stats.sem(fitSOMsustainedSuppressionPureToneNoLaser)
# 
# fitMeanPVsupPureToneLaser = np.mean(fitPVsustainedSuppressionPureToneLaser)
# fitSemPVsupPureToneLaser = scipy.stats.sem(fitPVsustainedSuppressionPureToneLaser)
# 
# fitMeanSOMsupPureToneLaser = np.mean(fitSOMsustainedSuppressionPureToneLaser)
# fitSemSOMsupPureToneLaser = scipy.stats.sem(fitSOMsustainedSuppressionPureToneLaser)

# -- get preferred bandwidths for all cells responsive during sustained portion of response with and without laser--
PVsustainedPrefBWNoLaser = PVCells['sustainedPrefBandwidthNoLaser']
SOMsustainedPrefBWNoLaser = SOMCells['sustainedPrefBandwidthNoLaser']
 
PVsustainedPrefBWLaser = PVCells['sustainedPrefBandwidthLaser']
SOMsustainedPrefBWLaser = SOMCells['sustainedPrefBandwidthLaser']

fitPVsustainedPrefBWNoLaser = PVCells['fitSustainedPrefBandwidthNoLaser']
fitSOMsustainedPrefBWNoLaser = SOMCells['fitSustainedPrefBandwidthNoLaser']

fitPVsustainedPrefBWLaser = PVCells['fitSustainedPrefBandwidthLaser']
fitSOMsustainedPrefBWLaser = SOMCells['fitSustainedPrefBandwidthLaser']

# -- get changes in firing rate for peak and WN
fitPVpeakFRNoLaser = PVCells['fitPeakFRNoLaser']
fitPVpeakFRLaser = PVCells['fitPeakFRLaser']
fitPVpeakChangeFR = PVCells['fitPeakChangeFR']
        
fitPVWNFRNoLaser = PVCells['fitWNFRNoLaser']
fitPVWNFRLaser = PVCells['fitWNFRLaser']
fitPVWNChangeFR = PVCells['fitWNChangeFR']
        
fitSOMpeakFRNoLaser = SOMCells['fitPeakFRNoLaser']
fitSOMpeakFRLaser = SOMCells['fitPeakFRLaser']
fitSOMpeakChangeFR = SOMCells['fitPeakChangeFR']
        
fitSOMWNFRNoLaser = SOMCells['fitWNFRNoLaser']
fitSOMWNFRLaser = SOMCells['fitWNFRLaser']
fitSOMWNChangeFR = SOMCells['fitWNChangeFR']

fitMeanPVpeakChange = np.mean(fitPVpeakChangeFR)
fitSemPVpeakChange = scipy.stats.sem(fitPVpeakChangeFR)

fitMeanPVWNChange = np.mean(fitPVWNChangeFR)
fitSemPVWNChange = scipy.stats.sem(fitPVWNChangeFR)

fitMeanSOMpeakChange = np.mean(fitSOMpeakChangeFR)
fitSemSOMpeakChange = scipy.stats.sem(fitSOMpeakChangeFR)

fitMeanSOMWNChange = np.mean(fitSOMWNChangeFR)
fitSemSOMWNChange = scipy.stats.sem(fitSOMWNChangeFR)

# fitPVpeakChangeFRPureTone = PVCells['fitPeakChangeFRPureTone']
# fitPVWNChangeFRPureTone = PVCells['fitWNChangeFRPureTone']
# 
# fitSOMpeakChangeFRPureTone = SOMCells['fitPeakChangeFRPureTone']
# fitSOMWNChangeFRPureTone = SOMCells['fitWNChangeFRPureTone']
# 
# fitMeanPVpeakChangePureTone = np.mean(fitPVpeakChangeFRPureTone)
# fitSemPVpeakChangePureTone = scipy.stats.sem(fitPVpeakChangeFRPureTone)
# 
# fitMeanPVWNChangePureTone = np.mean(fitPVWNChangeFRPureTone)
# fitSemPVWNChangePureTone = scipy.stats.sem(fitPVWNChangeFRPureTone)
# 
# fitMeanSOMpeakChangePureTone = np.mean(fitSOMpeakChangeFRPureTone)
# fitSemSOMpeakChangePureTone = scipy.stats.sem(fitSOMpeakChangeFRPureTone)
# 
# fitMeanSOMWNChangePureTone = np.mean(fitSOMWNChangeFRPureTone)
# fitSemSOMWNChangePureTone = scipy.stats.sem(fitSOMWNChangeFRPureTone)

fitPVpeakChangeFRNoZero = PVCells['fitPeakChangeFRNoZero']
fitPVWNChangeFRNoZero = PVCells['fitWNChangeFRNoZero']

fitSOMpeakChangeFRNoZero = SOMCells['fitPeakChangeFRNoZero']
fitSOMWNChangeFRNoZero = SOMCells['fitWNChangeFRNoZero']

fitMeanPVpeakChangeNoZero = np.mean(fitPVpeakChangeFRNoZero)
fitSemPVpeakChangeNoZero = scipy.stats.sem(fitPVpeakChangeFRNoZero)

fitMeanPVWNChangeNoZero = np.mean(fitPVWNChangeFRNoZero)
fitSemPVWNChangeNoZero = scipy.stats.sem(fitPVWNChangeFRNoZero)

fitMeanSOMpeakChangeNoZero = np.mean(fitSOMpeakChangeFRNoZero)
fitSemSOMpeakChangeNoZero = scipy.stats.sem(fitSOMpeakChangeFRNoZero)

fitMeanSOMWNChangeNoZero = np.mean(fitSOMWNChangeFRNoZero)
fitSemSOMWNChangeNoZero = scipy.stats.sem(fitSOMWNChangeFRNoZero)

rawPVpeakChangeFR = PVCells['peakChangeFR']
rawPVWNChangeFR = PVCells['WNChangeFR']

rawSOMpeakChangeFR = SOMCells['peakChangeFR']
rawSOMWNChangeFR = SOMCells['WNChangeFR']

rawMeanPVpeakChange = np.mean(rawPVpeakChangeFR)
rawSemPVpeakChange = scipy.stats.sem(rawPVpeakChangeFR)

rawMeanPVWNChange = np.mean(rawPVWNChangeFR)
rawSemPVWNChange = scipy.stats.sem(rawPVWNChangeFR)

rawMeanSOMpeakChange = np.mean(rawSOMpeakChangeFR)
rawSemSOMpeakChange = scipy.stats.sem(rawSOMpeakChangeFR)

rawMeanSOMWNChange = np.mean(rawSOMWNChangeFR)
rawSemSOMWNChange = scipy.stats.sem(rawSOMWNChangeFR)
        
# -- save photoidentified suppression scores --
outputFile = 'all_inactivated_cells_stats_full.npz'
outputFullPath = os.path.join(dataDir,outputFile)
np.savez(outputFullPath,
         rawPVsustainedSuppressionNoLaser = rawPVsustainedSuppressionNoLaser,
         rawSOMsustainedSuppressionNoLaser = rawSOMsustainedSuppressionNoLaser,
         rawPVsustainedSuppressionLaser = rawPVsustainedSuppressionLaser,
         rawSOMsustainedSuppressionLaser = rawSOMsustainedSuppressionLaser,
         rawMeanPVsupLaser = rawMeanPVsupLaser, rawSemPVsupLaser = rawSemPVsupLaser,
         rawMeanPVsupNoLaser = rawMeanPVsupNoLaser, rawSemPVsupNoLaser = rawSemPVsupNoLaser,
         rawMeanSOMsupLaser = rawMeanSOMsupLaser, rawSemSOMsupLaser = rawSemSOMsupLaser,
         rawMeanSOMsupNoLaser = rawMeanSOMsupNoLaser, rawSemSOMsupNoLaser = rawSemSOMsupNoLaser,
         
         fitPVsustainedSuppressionNoLaser = fitPVsustainedSuppressionNoLaser,
         fitSOMsustainedSuppressionNoLaser = fitSOMsustainedSuppressionNoLaser,
         fitPVsustainedSuppressionLaser = fitPVsustainedSuppressionLaser,
         fitSOMsustainedSuppressionLaser = fitSOMsustainedSuppressionLaser,
         fitMeanPVsupLaser = fitMeanPVsupLaser, fitSemPVsupLaser = fitSemPVsupLaser,
         fitMeanPVsupNoLaser = fitMeanPVsupNoLaser, fitSemPVsupNoLaser = fitSemPVsupNoLaser,
         fitMeanSOMsupLaser = fitMeanSOMsupLaser, fitSemSOMsupLaser = fitSemSOMsupLaser,
         fitMeanSOMsupNoLaser = fitMeanSOMsupNoLaser, fitSemSOMsupNoLaser = fitSemSOMsupNoLaser,
         
         fitPVsustainedSuppressionNoZeroNoLaser = fitPVsustainedSuppressionNoZeroNoLaser,
         fitSOMsustainedSuppressionNoZeroNoLaser = fitSOMsustainedSuppressionNoZeroNoLaser,
         fitPVsustainedSuppressionNoZeroLaser = fitPVsustainedSuppressionNoZeroLaser,
         fitSOMsustainedSuppressionNoZeroLaser = fitSOMsustainedSuppressionNoZeroLaser,
         fitMeanPVsupNoZeroLaser = fitMeanPVsupNoZeroLaser, fitSemPVsupNoZeroLaser = fitSemPVsupNoZeroLaser,
         fitMeanPVsupNoZeroNoLaser = fitMeanPVsupNoZeroNoLaser, fitSemPVsupNoZeroNoLaser = fitSemPVsupNoZeroNoLaser,
         fitMeanSOMsupNoZeroLaser = fitMeanSOMsupNoZeroLaser, fitSemSOMsupNoZeroLaser = fitSemSOMsupNoZeroLaser,
         fitMeanSOMsupNoZeroNoLaser = fitMeanSOMsupNoZeroNoLaser, fitSemSOMsupNoZeroNoLaser = fitSemSOMsupNoZeroNoLaser,
         
#          fitPVsustainedSuppressionPureToneNoLaser = fitPVsustainedSuppressionPureToneNoLaser,
#          fitSOMsustainedSuppressionPureToneNoLaser = fitSOMsustainedSuppressionPureToneNoLaser,
#          fitPVsustainedSuppressionPureToneLaser = fitPVsustainedSuppressionPureToneLaser,
#          fitSOMsustainedSuppressionPureToneLaser = fitSOMsustainedSuppressionPureToneLaser,
#          fitMeanPVsupPureToneLaser = fitMeanPVsupPureToneLaser, fitSemPVsupPureToneLaser = fitSemPVsupPureToneLaser,
#          fitMeanPVsupPureToneNoLaser = fitMeanPVsupPureToneNoLaser, fitSemPVsupPureToneNoLaser = fitSemPVsupPureToneNoLaser,
#          fitMeanSOMsupPureToneLaser = fitMeanSOMsupPureToneLaser, fitSemSOMsupPureToneLaser = fitSemSOMsupPureToneLaser,
#          fitMeanSOMsupPureToneNoLaser = fitMeanSOMsupPureToneNoLaser, fitSemSOMsupPureToneNoLaser = fitSemSOMsupPureToneNoLaser,
         
         rawPVsustainedPrefBWNoLaser = PVsustainedPrefBWNoLaser,
         rawSOMsustainedPrefBWNoLaser = SOMsustainedPrefBWNoLaser,
         rawPVsustainedPrefBWLaser = PVsustainedPrefBWLaser,
         rawSOMsustainedPrefBWLaser = SOMsustainedPrefBWLaser,
         
         fitPVsustainedPrefBWNoLaser = fitPVsustainedPrefBWNoLaser,
         fitSOMsustainedPrefBWNoLaser = fitSOMsustainedPrefBWNoLaser,
         fitPVsustainedPrefBWLaser = fitPVsustainedPrefBWLaser,
         fitSOMsustainedPrefBWLaser = fitSOMsustainedPrefBWLaser,
         
         fitPVpeakFRNoLaser = fitPVpeakFRNoLaser, fitPVpeakFRLaser = fitPVpeakFRLaser, fitPVpeakChangeFR = fitPVpeakChangeFR,
         fitPVWNFRNoLaser = fitPVWNFRNoLaser, fitPVWNFRLaser = fitPVWNFRLaser, fitPVWNChangeFR = fitPVWNChangeFR,
        
         fitSOMpeakFRNoLaser = fitSOMpeakFRNoLaser, fitSOMpeakFRLaser = fitSOMpeakFRLaser, fitSOMpeakChangeFR = fitSOMpeakChangeFR,
         fitSOMWNFRNoLaser = fitSOMWNFRNoLaser, fitSOMWNFRLaser = fitSOMWNFRLaser, fitSOMWNChangeFR = fitSOMWNChangeFR,
         
         fitMeanPVpeakChange = fitMeanPVpeakChange, fitSemPVpeakChange = fitSemPVpeakChange,
         fitMeanPVWNChange = fitMeanPVWNChange, fitSemPVWNChange = fitSemPVWNChange,
         fitMeanSOMpeakChange = fitMeanSOMpeakChange, fitSemSOMpeakChange = fitSemSOMpeakChange,
         fitMeanSOMWNChange = fitMeanSOMWNChange, fitSemSOMWNChange = fitSemSOMWNChange,
         
#          fitPVpeakChangeFRPureTone = fitPVpeakChangeFRPureTone,
#          fitPVWNChangeFRPureTone = fitPVWNChangeFRPureTone,
#          fitSOMpeakChangeFRPureTone = fitSOMpeakChangeFRPureTone,
#          fitSOMWNChangeFRPureTone = fitSOMWNChangeFRPureTone,
#          fitMeanPVpeakChangePureTone = fitMeanPVpeakChangePureTone, fitSemPVpeakChangePureTone = fitSemPVpeakChangePureTone,
#          fitMeanPVWNChangePureTone = fitMeanPVWNChangePureTone, fitSemPVWNChangePureTone = fitSemPVWNChangePureTone,
#          fitMeanSOMpeakChangePureTone = fitMeanSOMpeakChangePureTone, fitSemSOMpeakChangePureTone = fitSemSOMpeakChangePureTone,
#          fitMeanSOMWNChangePureTone = fitMeanSOMWNChangePureTone, fitSemSOMWNChangePureTone = fitSemSOMWNChangePureTone,
         
         fitPVpeakChangeFRNoZero = fitPVpeakChangeFRNoZero,
         fitPVWNChangeFRNoZero = fitPVWNChangeFRNoZero,
         fitSOMpeakChangeFRNoZero = fitSOMpeakChangeFRNoZero,
         fitSOMWNChangeFRNoZero = fitSOMWNChangeFRNoZero,
         fitMeanPVpeakChangeNoZero = fitMeanPVpeakChangeNoZero, fitSemPVpeakChangeNoZero = fitSemPVpeakChangeNoZero,
         fitMeanPVWNChangeNoZero = fitMeanPVWNChangeNoZero, fitSemPVWNChangeNoZero = fitSemPVWNChangeNoZero,
         fitMeanSOMpeakChangeNoZero = fitMeanSOMpeakChangeNoZero, fitSemSOMpeakChangeNoZero = fitSemSOMpeakChangeNoZero,
         fitMeanSOMWNChangeNoZero = fitMeanSOMWNChangeNoZero, fitSemSOMWNChangeNoZero = fitSemSOMWNChangeNoZero,
         
         rawPVpeakChangeFR = rawPVpeakChangeFR,
         rawPVWNChangeFR = rawPVWNChangeFR,
         rawSOMpeakChangeFR = rawSOMpeakChangeFR,
         rawSOMWNChangeFR = rawSOMWNChangeFR,
         rawMeanPVpeakChange = rawMeanPVpeakChange, rawSemPVpeakChange = rawSemPVpeakChange,
         rawMeanPVWNChange = rawMeanPVWNChange, rawSemPVWNChange = rawSemPVWNChange,
         rawMeanSOMpeakChange = rawMeanSOMpeakChange, rawSemSOMpeakChange = rawSemSOMpeakChange,
         rawMeanSOMWNChange = rawMeanSOMWNChange, rawSemSOMWNChange = rawSemSOMWNChange,)
print outputFile + " saved"