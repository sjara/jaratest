''' 
Generates inputs to plot histograms/scatter plots of suppression indeces for all cells
'''

import os
import pandas as pd
import numpy as np

from jaratoolbox import settings

import figparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, 'photoidentification_cells.h5')
dbase = pd.read_hdf(dbPath, 'database',index_col=0)

allACFigName = 'figure_all_AC_suppression'
photoFigName = 'figure_PV_SOM_suppression'

allACDataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', allACFigName)
photoDataDir = os.path.join(settings.FIGURES_DATA_PATH, '2018acsup', photoFigName)

R2CUTOFF = 0.1 #minimum R^2 value for a cell to be considered frequency tuned
OCTAVESCUTOFF = 0.3 #maximum octave difference between estimated best frequency and centre frequency presented

SOUND_RESPONSE_PVAL = 0.05

PV_CHR2_MICE = ['band004', 'band026', 'band032', 'band033']
SOM_CHR2_MICE = ['band005', 'band015', 'band016', 'band027', 'band028', 'band029', 'band030', 'band031', 'band034','band037','band038','band044','band045']

EXCLUDED_DATES = ['2017-07-27','2017-08-02'] #dates where there were some problems with recording

# -- find PV, SOM, and non-SOM cells that are tuned to frequency and with a good centre frequency selected
bestCells = dbase.query('tuningFitR2High>@R2CUTOFF and octavesFromBestHigh<@OCTAVESCUTOFF')
bestCells = bestCells.loc[~bestCells['date'].isin(EXCLUDED_DATES)]

laserResponsiveCells = bestCells.query('laserResponsepVal<0.001 and laserResponseStdFromBase>2.0')
PVCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(PV_CHR2_MICE)]
SOMCells = laserResponsiveCells.loc[laserResponsiveCells['subject'].isin(SOM_CHR2_MICE)]

nonSOMCells = bestCells.query('laserResponseStdFromBase<0.5 and subject in @SOM_CHR2_MICE')

# -- get cells responsive during sustained portion of response --
sustainedPVCells = PVCells.loc[PVCells['bandSustainedSoundResponsepVal']<SOUND_RESPONSE_PVAL]
sustainedSOMCells = SOMCells.loc[SOMCells['bandSustainedSoundResponsepVal']<SOUND_RESPONSE_PVAL]
sustainednonSOMCells = nonSOMCells.loc[nonSOMCells['bandSustainedSoundResponsepVal']<SOUND_RESPONSE_PVAL]

# -- get suppression indices for all cells responsive during sustained portion of response --
PVsustainedSuppression = sustainedPVCells['sustainedSuppressionIndexHigh']
SOMsustainedSuppression = sustainedSOMCells['sustainedSuppressionIndexHigh']
nonSOMsustainedSuppression = sustainednonSOMCells['sustainedSuppressionIndexHigh']

# -- get cells responsive during onset portion of response --
onsetPVCells = PVCells.loc[PVCells['bandOnsetSoundResponsepVal']<SOUND_RESPONSE_PVAL]
onsetSOMCells = SOMCells.loc[SOMCells['bandOnsetSoundResponsepVal']<SOUND_RESPONSE_PVAL]
onsetnonSOMCells = nonSOMCells.loc[nonSOMCells['bandOnsetSoundResponsepVal']<SOUND_RESPONSE_PVAL]

# -- get suppression indices for all cells responsive during onset portion of response --
PVonsetSuppression = onsetPVCells['onsetSuppressionIndexHigh']
SOMonsetSuppression = onsetSOMCells['onsetSuppressionIndexHigh']
nonSOMonsetSuppression = onsetnonSOMCells['onsetSuppressionIndexHigh']

# -- get onset and sustained suppression for ALL cells --
allSustainedCells = bestCells.loc[bestCells['bandSustainedSoundResponsepVal']<SOUND_RESPONSE_PVAL]
allSigSupSustainedCells = allSustainedCells.loc[allSustainedCells['sustainedSuppressionpValHigh']<0.05]
allNotSigSustainedCells = allSustainedCells.loc[allSustainedCells['sustainedSuppressionpValHigh']>0.05]

allOnsetCells = bestCells.loc[bestCells['bandOnsetSoundResponsepVal']<SOUND_RESPONSE_PVAL]
allSigSupOnsetCells = allOnsetCells.loc[allOnsetCells['onsetSuppressionpValHigh']<0.05]
allNotSigOnsetCells = allSustainedCells.loc[allSustainedCells['onsetSuppressionpValHigh']>0.05]

allSigSustainedSuppression = allSigSupSustainedCells['sustainedSuppressionIndexHigh']
allNotSigSustainedSuppression = allNotSigSustainedCells['sustainedSuppressionIndexHigh']

allSigOnsetSuppression = allSigSupOnsetCells['onsetSuppressionIndexHigh']
allNotSigOnsetSuppression = allNotSigOnsetCells['onsetSuppressionIndexHigh']

# -- save photoidentified suppression scores --
outputFile = 'photoidentified_cells_suppression_scores.npz'
photoOutputFullPath = os.path.join(photoDataDir,outputFile)
np.savez(photoOutputFullPath,
         PVonsetSuppression = PVonsetSuppression,
         PVsustainedSuppression = PVsustainedSuppression,
         SOMonsetSuppression = SOMonsetSuppression,
         SOMsustainedSuppression = SOMsustainedSuppression,
         nonSOMonsetSuppression = nonSOMonsetSuppression,
         nonSOMsustainedSuppression = nonSOMsustainedSuppression)
print outputFile + " saved"

# -- save all cells suppression scores --
outputFile = 'all_cells_suppression_scores.npz'
allOutputFullPath = os.path.join(allACDataDir,outputFile)
np.savez(allOutputFullPath,
         allSigSustainedSuppression = allSigSustainedSuppression,
         allNotSigSustainedSuppression = allNotSigSustainedSuppression,
         allSigOnsetSuppression = allSigOnsetSuppression,
         allNotSigOnsetSuppression = allNotSigOnsetSuppression)
print outputFile + " saved"
