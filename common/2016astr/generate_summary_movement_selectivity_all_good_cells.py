'''
Generate and store intermediate data for plot showing movement-selectivity of astr neurons recorded in the psychometric curve and switching tasks. 
Output npz file contains animalName, selective(boolean vector indicating whether each cell was significantly modulated by movement), and movementModI(modulation index for each cell).
Lan Guo20161222
'''
# TO DO
# Include in the database information about what script creates it


import os
import numpy as np
import pandas as pd
from jaratoolbox import settings

# -- Read in databases storing all measurements from psycurve and switching mice -- #
allcells_switching = pd.read_hdf('/home/languo/data/ephys/switching_summary_stats/all_cells_all_measures_extra_mod_waveform_switching.h5',key='switching')

allcells_psychometric = pd.read_hdf('/home/languo/data/ephys/psychometric_summary_stats/all_cells_all_measures_psychometric.h5',key='psychometric')

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
np.savez(outputFullPath, **dataToPlot)
