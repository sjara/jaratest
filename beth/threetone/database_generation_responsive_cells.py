"""
Creates a database from the full cell database those cells that are responsive based on pValue and firing rate thresholds.
"""

import os
import importlib
import pandas as pd
import matplotlib.pyplot as plt
from numpy import array
from jaratoolbox import settings
from jaratoolbox import celldatabase
import studyparams
importlib.reload(studyparams)

#dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbPath = settings.FIGURES_DATA_PATH
dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)

pValueThreshold = 0.05
firingRateThreshold = 5 #spikes/s
ratioFiringRates = 1.35

def sound_responsive_cells(celldb, pValueThreshold, firingRateThreshold, ratioFiringRates):
    """
    Creates a database of sound responsive cells based on a p-Value threshold, a firing rate threshold between evoked and baseline in the freq. sorted raster, and the ratio between the evoked and baseline firing rates.

    Inputs:
        celldb: Full database that allows for loading of ephys and behavior data and calculated base stats and indices.
        pValueThreshold: Number below which the number of spikes in the evoked time range is significantly different than in the baseline time range.
        firingRateThreshold: Firing rate in spikes per second over which there is good sound response (chosen by hand).
        ratioFiringRates: Ratio between evoked firing rate and baseline firing rate above which there is good sound response (chosen by hand).

    Outputs:
        responsivedb: Cell database that contains only cells from the original database that are sound responsive based on the criteria set forth by the inputs.
    """

    # -- Initialize variables --
    totalCells = 0
    numSoundResponsiveCells = 0
    responsiveCells = []

    for indRow,dbRow in celldb.iterrows():
        if not 'ascending' in dbRow['sessionType']:
            continue
        totalCells = totalCells + 1
        # -- Calculating what percentage of cells are sound responsive to one of the three frequencies in ascending or descending sequence --
        pValueHighFreqA = celldb['pValHighResponseA'][indRow]
        pValueMidFreqA = celldb['pValMidResponseA'][indRow]
        pValueLowFreqA = celldb['pValLowResponseA'][indRow]
        pValueHighFreqD = celldb['pValHighResponseD'][indRow]
        pValueMidFreqD = celldb['pValMidResponseD'][indRow]
        pValueLowFreqD = celldb['pValLowResponseD'][indRow]
        # -- If any of the three frequencies in either the ascending or descending sequence have a p-value (comparison between baseline and evoked time ranges) smaller than the p-value threshold, pass the cells onto the next stage of filtering --
        if (pValueHighFreqA < pValueThreshold) or (pValueMidFreqA < pValueThreshold) or (pValueLowFreqA < pValueThreshold) or (pValueHighFreqD < pValueThreshold) or (pValueMidFreqD < pValueThreshold) or (pValueLowFreqD < pValueThreshold):
            # -- Calculating ratios between evoked firing rates and baseline firing rates --
            highRatioA = celldb['meanEvokedHighA'][indRow] / celldb['meanBaseHighA'][indRow]
            midRatioA = celldb['meanEvokedMidA'][indRow] / celldb['meanBaseMidA'][indRow]
            lowRatioA = celldb['meanEvokedLowA'][indRow] / celldb['meanBaseLowA'][indRow]
            highRatioD = celldb['meanEvokedHighD'][indRow] / celldb['meanBaseHighD'][indRow]
            midRatioD = celldb['meanEvokedMidD'][indRow] / celldb['meanBaseMidD'][indRow]
            lowRatioD = celldb['meanEvokedLowD'][indRow] / celldb['meanBaseLowD'][indRow]
            # -- If the ratio between evoked and baseline firing rates for any of the three frequencies in either the ascending or descending sequence is greater than the ratio threshold, consider the cell responsive. There needs to be a 35% difference in firing rates between the evoked and baseline spike counts. --
            if (highRatioA > ratioFiringRates) or ((1/highRatioA) > ratioFiringRates) or (midRatioA > ratioFiringRates) or ((1/midRatioA) > ratioFiringRates) or (lowRatioA > ratioFiringRates) or ((1/lowRatioA) > ratioFiringRates) or (highRatioD > ratioFiringRates) or ((1/highRatioD) > ratioFiringRates) or (midRatioD > ratioFiringRates) or ((1/midRatioD) > ratioFiringRates) or (lowRatioD > ratioFiringRates) or ((1/lowRatioD) > ratioFiringRates):
                # -- Defining the firing rates of the evoked response for all three frequencies in the ascending and descending sequence --
                highA = celldb['meanEvokedHighA'][indRow]
                midA = celldb['meanEvokedMidA'][indRow]
                lowA = celldb['meanEvokedLowA'][indRow]
                highD = celldb['meanEvokedHighD'][indRow]
                midD = celldb['meanEvokedMidD'][indRow]
                lowD = celldb['meanEvokedLowD'][indRow]
                # -- If any of the three frequencies have an evoked firing rate greater than the firing rate threshold, consider the cell responsive --
                if (highA > firingRateThreshold) or (midA > firingRateThreshold) or (lowA > firingRateThreshold) or (highD > firingRateThreshold) or (midD > firingRateThreshold) or (lowD > firingRateThreshold):
                    numSoundResponsiveCells = numSoundResponsiveCells + 1
                    responsiveCells.append(celldb.iloc[indRow])
                    print('{} {} {} {}um T{} c{} is sound responsive.'.format(indRow, dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))

    print('{} of {} total cells were responsive.'.format(numSoundResponsiveCells, totalCells))

    # -- Creating a database of significantly sound responsive cells --
    responsivedb = pd.DataFrame(responsiveCells)
    return responsivedb

responsivedb = sound_responsive_cells(celldb, pValueThreshold, firingRateThreshold, ratioFiringRates)
# -- Reindexing the responsive database --
responsivedb = responsivedb.reset_index(drop=True)
'''
# -- Saving the database --
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'responsivedb_{}.h5'.format(studyparams.STUDY_NAME))
if os.path.isdir(dbPath):
    celldatabase.save_hdf(responsivedb, dbFilename)
    print('Saved database to {}'.format(dbFilename))
else:
    print('{} does not exist. Please create this folder.'.format(dbPath))
'''
