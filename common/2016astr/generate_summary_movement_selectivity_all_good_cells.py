'''
Generate and store intermediate data for plot showing movement-selectivity of astr neurons recorded in the psychometric curve and switching tasks. 
Output npz file contains script, path of the source databases, good cell quality, animalName, movementSelective(boolean vector indicating whether each cell was significantly modulated by movement), and movementModI(modulation index for each cell).
Lan Guo20161222
'''
# TO DO
# Include in the database information about what script creates it
# Save cell databases on jarahub

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings
import figparams

FIGNAME = 'movement_selectivity'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

scriptFullPath = os.path.realpath(__file__)
qualityList = [1,6]
ISIcutoff = 0.02
removedDuplicates = True

# -- Read in databases storing all measurements from psycurve and switching mice -- #
switchingFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

psychometricFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
psychometricFileName = 'all_cells_all_measures_waveform_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

# -- Get intermediate data relevant to this subfigure of movement selectivity -- #
## Pooling all good cells from switcing task and psychometric curve task together ##
dataToPlot = {'movementSelective':[],'movementModI':[],'animalName':[]}
for ind,allcells in enumerate([allcells_switching,allcells_psychometric]):
    goodcells = (allcells.cellQuality.isin(qualityList)) & (allcells.ISI <= ISIcutoff)
    cellInStr =  (allcells.cellInStr==1)
    keepAfterDupTest = allcells.keep_after_dup_test
    if removedDuplicates:
        allcells = allcells[goodcells & cellInStr & keepAfterDupTest]
    else:
        allcells = allcells[goodcells & cellInStr] #just look at the good cells THAT ARE IN STR
    sigMod = np.array((allcells.movementModS<=0.05), dtype=bool)
    dataToPlot['movementSelective'].extend(sigMod)
    dataToPlot['animalName'].extend(allcells.animalName)
    dataToPlot['movementModI'].extend(allcells.movementModI)

### Save data ###
#outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
if removedDuplicates:
    outputFile = 'summary_movement_selectivity_all_good_cells_remove_dup.npz'
else:
    outputFile = 'summary_movement_selectivity_all_good_cells.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, sourcePsychometric=psychometricFilePath, sourceSwitching=switchingFilePath, goodCellQuality=qualityList, script=scriptFullPath, **dataToPlot)
