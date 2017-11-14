'''
Generate and store intermediate data for plot showing movement-selectivity of astr neurons,
 recorded in either the psychometric curve or switching tasks.
Removed duplicated cells. 
Output npz file contains script, path of the source databases, good cell quality, animalName, movementSelective(boolean vector indicating whether each cell was significantly modulated by movement), and movementModI(modulation index for each cell).
Lan Guo 20170207
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
taskToPlot = 'switching' #'switching' or 'psychometric'

if taskToPlot == 'psychometric':
    # -- Read in databases storing all measurements from psycurve and switching mice -- #
    databaseFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    databaseFileName = 'all_cells_all_measures_waveform_psychometric.h5'
    databaseFullPath = os.path.join(databaseFilePath,databaseFileName)
    allcells = pd.read_hdf(databaseFullPath,key='psychometric')
elif taskToPlot == 'switching':
    # -- Read in databases storing all measurements from psycurve and switching mice -- #
    databaseFilePath = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    databaseFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
    databaseFullPath = os.path.join(databaseFilePath,databaseFileName)
    allcells = pd.read_hdf(databaseFullPath,key='switching')

# -- Get intermediate data relevant to this subfigure of movement selectivity -- #
## Pooling all good cells from switcing task and psychometric curve task together ##
dataToPlot = {'movementSelective':[],'movementModI':[],'animalName':[]}

goodcells = (allcells.cellQuality.isin(qualityList)) & (allcells.ISI <= ISIcutoff)
cellInStr =  (allcells.cellInStr==1)
keepAfterDupTest = allcells.keep_after_dup_test
allcells = allcells[goodcells & cellInStr & keepAfterDupTest]

sigMod = np.array((allcells.movementModS<=0.05), dtype=bool)
dataToPlot['movementSelective'].extend(sigMod)
dataToPlot['animalName'].extend(allcells.animalName)
dataToPlot['movementModI'].extend(allcells.movementModI)

### Save data ###
outputFile = 'summary_movement_selectivity_{}.npz'.format(taskToPlot)
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, sourceDatabase=databaseFullPath, goodCellQuality=qualityList, ISIcutoff=ISIcutoff, script=scriptFullPath, **dataToPlot)
