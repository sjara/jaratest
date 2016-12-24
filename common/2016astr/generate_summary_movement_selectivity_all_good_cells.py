'''
Generate and store intermediate data for plot showing movement-selectivity of astr neurons recorded in the psychometric curve and switching tasks. 
Output npz file contains animalName, selective(boolean vector indicating whether each cell was significantly modulated by movement), and movementModI(modulation index for each cell).
Lan Guo20161222
'''
# TO DO
# Include in the database information about what script creates it
# Save cell databases on jarahub

import os
import numpy as np
import pandas as pd
from jaratoolbox import settings

scriptFullPath = os.path.realpath(__file__)

# -- Read in databases storing all measurements from psycurve and switching mice -- #
switchingFilePath = settings.FIGURESDATA
switchingFileName = 'all_cells_all_measures_extra_mod_waveform_switching.h5'
switchingFullPath = os.path.join(switchingFilePath,switchingFileName)
allcells_switching = pd.read_hdf(switchingFullPath,key='switching')

psychometricFilePath = settings.FIGURESDATA
psychometricFileName = 'all_cells_all_measures_psychometric.h5'
psychometricFullPath = os.path.join(psychometricFilePath,psychometricFileName)
allcells_psychometric = pd.read_hdf(psychometricFullPath,key='psychometric')

# -- Get intermediate data relevant to this subfigure of movement selectivity -- #
## Pooling all good cells from switcing task and psychometric curve task together ##
dataToPlot = {'selective':[],'movementModI':[],'animalName':[]}
for ind,allcells in enumerate([allcells_switching,allcells_psychometric]):
    allcells = allcells[allcells.cellQuality.isin([1,6])] #just look at the good cells
    sigMod = np.array((allcells.movementModS<=0.05), dtype=bool)
    dataToPlot['selective'].extend(sigMod)
    dataToPlot['animalName'].extend(allcells.animalName)
    dataToPlot['movementModI'].extend(allcells.movementModI)

### Save data ###
outputDir = '/home/languo/data/mnt/figuresdata'
outputFile = 'summary_movement_selectivity_all_good_cells.npz'
outputFullPath = os.path.join(outputDir,outputFile)
np.savez(outputFullPath, script=scriptFullPath, **dataToPlot)
