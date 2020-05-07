"""
Test to find how many responsive cells are significant.
"""
from __future__ import division
import os
import importlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
import studyparams
importlib.reload(studyparams)

#dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbPath = settings.FIGURES_DATA_PATH
dbFilename = os.path.join(dbPath,'responsivedb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of responsive cells --
responsivedb = celldatabase.load_hdf(dbFilename)

dbFilenamex = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilenamex)

def comparing_odd_std_significance(responsivedb):
    """
    Counts how many of the responsive cells show a significant difference between oddball and standard firing rates for their most responsive frequency.

    Inputs:
        responsivedb: Cell database that contains only the cells that are sound responsive and that allows for loading of ephys and behavior data and calculated base stats and indices.

    Outputs:
        responsivedb: Cell database with two additional columns including the p-Value corresponding to whichever frequency (high, middle, low) had the lowest p-Value when comparing evoked to baseline spike counts for the ascending and descending sequence.
    """

    significantCellsA = np.tile(np.nan, len(responsivedb))
    significantCellsD = np.tile(np.nan, len(responsivedb))

    for indRow, dbRow in responsivedb.iterrows():
        pValueHighA = responsivedb['pValHighResponseA'][indRow]
        pValueMidA = responsivedb['pValMidResponseA'][indRow]
        pValueLowA = responsivedb['pValLowResponseA'][indRow]
        pValuesA = dict(pValueHA = pValueHighA, pValueMA = pValueMidA, pValueLA = pValueLowA)
        # -- The best frequency is the one with the lowest pValue in sound_responsive_cells. --
        minimumA = min(pValuesA, key=pValuesA.get)

        # -- This adds to a list the pValue corresponding to whichever frequency (high, middle, low) had the lowest pValue when comparing evoked to baseline spike counts for the ascending sequence --
        if minimumA == 'pValueHA':
            significantCellsA[indRow] = responsivedb['pValHighFRA'][indRow]
        elif minimumA == 'pValueMA':
            significantCellsA[indRow] = responsivedb['pValMidFRA'][indRow]
        else:
            significantCellsA[indRow] = responsivedb['pValLowFRA'][indRow]

        pValueHighD = responsivedb['pValHighResponseD'][indRow]
        pValueMidD = responsivedb['pValMidResponseD'][indRow]
        pValueLowD = responsivedb['pValLowResponseD'][indRow]
        pValuesD = dict(pValueHD = pValueHighD, pValueMD = pValueMidD, pValueLD = pValueLowD)
        # -- The best frequency is the one with the lowest pValue in sound_responsive_cells. --
        minimumD = min(pValuesD, key=pValuesD.get)

        # -- This adds to a list the pValue corresponding to whichever frequency (high, middle, low) had the lowest pValue when comparing evoked to baseline spike counts for the descending sequence --
        if minimumD == 'pValueHD':
            significantCellsD[indRow] = responsivedb['pValHighFRD'][indRow]
        elif minimumD == 'pValueMD':
            significantCellsD[indRow] = responsivedb['pValMidFRD'][indRow]
        else:
            significantCellsD[indRow] = responsivedb['pValLowFRD'][indRow]

    # -- Adding a new column to the database using the array we created earlier. --
    responsivedb['mostRespFreqPValueOddStdA'] = significantCellsA
    responsivedb['mostRespFreqPValueOddStdD'] = significantCellsD

    # -- If either of the smallest pValues in the ascending or descending sequence are below the pValue threshold, that cell is significantly responsive. --
    signRespCells = responsivedb.query('mostRespFreqPValueOddStdA < 0.05 | mostRespFreqPValueOddStdD < 0.05')
    cellInfo = signRespCells[['subject', 'date', 'depth', 'tetrode', 'cluster']]
    #print(cellInfo)
    numSignRespCells = len(signRespCells)

    print('Number of cells recorded from: {}'.format(len(celldb)))
    print('Number of responsive cells: {}'.format(len(responsivedb)))
    print('Number of cells that showed a significant difference between expected and unexpected firing rates: {}'.format(numSignRespCells))
    percentSignRespCells = numSignRespCells / len(responsivedb) * 100
    print('Percentage of significantly responsive cells: {:.2f}%'.format(percentSignRespCells))

    return signRespCells

signRespCellsdb = comparing_odd_std_significance(responsivedb)

'''
# -- Saving the responsive database --
celldatabase.save_hdf(responsivedb, dbFilename)
print('Saved responsive database to {}'.format(dbFilename))

# -- Saving the database of significantly responsive cells. --
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'signRespCellsdb_{}.h5'.format(studyparams.STUDY_NAME))
celldatabase.save_hdf(signRespCellsdb, dbFilename)
print('Saved significantly responsive cell database to {}'.format(dbFilename))
'''
