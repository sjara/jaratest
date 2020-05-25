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
dbFilenameA = os.path.join(dbPath,'newresponsivedb_{}_A.h5'.format(studyparams.STUDY_NAME))
dbFilenameD = os.path.join(dbPath,'newresponsivedb_{}_D.h5'.format(studyparams.STUDY_NAME))

# -- Load the database of responsive cells --
responsivedbA = celldatabase.load_hdf(dbFilenameA)
responsivedbD = celldatabase.load_hdf(dbFilenameD)

pValueThreshold = 0.05

def comparing_odd_std_significance_ascending(responsivedb, pValueThreshold):
    """
    Counts how many of the responsive cells show a significant difference between oddball and standard firing rates for their most responsive frequency in the ascending sequence.

    Inputs:
        responsivedb: Cell database that contains only the cells that are sound responsive and that allows for loading of ephys and behavior data and calculated base stats and indices.
        pValueThreshold: Number below which the number of spikes in the evoked time range is significantly different than in the baseline time range.

    Outputs:
        responsivedb: Cell database with two additional columns including the p-Value corresponding to whichever frequency (high, middle, low) had the lowest p-Value when comparing evoked to baseline spike counts for the ascending and descending sequence.
    """

    significantCells = np.tile(np.nan, len(responsivedb))
    expUnexpRatio = np.tile(np.nan, len(responsivedb))

    for indRow, dbRow in responsivedb.iterrows():
        # -- 'pVal{Freq}Response{Session}' refers to the p-value between baseline and evoked for all frequencies for all trials --
        pValueHigh = responsivedb['pValHighResponseA'][indRow]
        pValueMid = responsivedb['pValMidResponseA'][indRow]
        pValueLow = responsivedb['pValLowResponseA'][indRow]
        pValues = dict(pValueHigh = pValueHigh, pValueMid = pValueMid, pValueLow = pValueLow)

        # -- The best frequency is the one with the lowest pValue --
        minimum = min(pValues, key=pValues.get)

        # -- This adds to a list the pValue for expectation (between oddball and standard) corresponding to whichever frequency (high, middle, low) had the lowest pValue when comparing evoked to baseline spike counts for the sequence in question --
        if minimum == 'pValueHigh':
            significantCells[indRow] = responsivedb['pValHighFRA'][indRow]
            expUnexpRatio[indRow] = responsivedb['meanEvokedFirstOddA'][indRow] / responsivedb['meanEvokedFirstStdA'][indRow]
        elif minimum == 'pValueMid':
            significantCells[indRow] = responsivedb['pValMidFRA'][indRow]
            expUnexpRatio[indRow] = responsivedb['meanEvokedSecondOddA'][indRow] / responsivedb['meanEvokedSecondStdA'][indRow]
        else:
            significantCells[indRow] = responsivedb['pValLowFRA'][indRow]
            expUnexpRatio[indRow] = responsivedb['meanEvokedThirdOddA'][indRow] / responsivedb['meanEvokedThirdStdA'][indRow]

    # -- Adding a new column to the database using the array we created earlier. --
    responsivedb['mostRespFreqExpectationPValueA'] = significantCells
    responsivedb['expUnexpRatioMostRespFreqA'] = expUnexpRatio

    # -- If either of the smallest pValues in the sequence are below the pValue threshold and there is increased firing for the oddball, that cell is significantly modulated. --
    #signModulatedCellsA = np.where((responsivedb['mostRespFreqExpectationPValueA'] < pValueThreshold) & (responsivedb['expUnexpRatioMostRespFreqA'] > 1))
    signCells = responsivedb[responsivedb.mostRespFreqExpectationPValueA < pValueThreshold]
    signModulatedCells = signCells[signCells.expUnexpRatioMostRespFreqA > 1]


    print('Number of responsive cells in the ascending session: {}'.format(len(responsivedb)))

    print('Number of cells that showed a significant difference between expected and unexpected firing rates in the ascending session: {}'.format(len(signCells)))

    print('Number of cells that showed a significant difference between expected and unexpected firing rates where there was more firing for the unexpected tone in the ascending session: {}'.format(len(signModulatedCells)))

    return responsivedb

def comparing_odd_std_significance_descending(responsivedb, pValueThreshold):
    """
    Counts how many of the responsive cells show a significant difference between oddball and standard firing rates for their most responsive frequency in the descending sequence.

    Inputs:
        responsivedb: Cell database that contains only the cells that are sound responsive and that allows for loading of ephys and behavior data and calculated base stats and indices.
        pValueThreshold: Number below which the number of spikes in the evoked time range is significantly different than in the baseline time range.

    Outputs:
        responsivedb: Cell database with two additional columns including the p-Value corresponding to whichever frequency (high, middle, low) had the lowest p-Value when comparing evoked to baseline spike counts for the ascending and descending sequence.
    """

    significantCells = np.tile(np.nan, len(responsivedb))
    expUnexpRatio = np.tile(np.nan, len(responsivedb))

    for indRow, dbRow in responsivedb.iterrows():
        # -- 'pVal{Freq}Response{Session}' refers to the p-value between baseline and evoked for all frequencies for all trials --
        pValueHigh = responsivedb['pValHighResponseD'][indRow]
        pValueMid = responsivedb['pValMidResponseD'][indRow]
        pValueLow = responsivedb['pValLowResponseD'][indRow]
        pValues = dict(pValueHigh = pValueHigh, pValueMid = pValueMid, pValueLow = pValueLow)

        # -- The best frequency is the one with the lowest pValue --
        minimum = min(pValues, key=pValues.get)

        # -- This adds to a list the pValue for expectation (between oddball and standard) corresponding to whichever frequency (high, middle, low) had the lowest pValue when comparing evoked to baseline spike counts for the sequence in question --
        if minimum == 'pValueHigh':
            significantCells[indRow] = responsivedb['pValHighFRD'][indRow]
            expUnexpRatio[indRow] = responsivedb['meanEvokedFirstOddD'][indRow] / responsivedb['meanEvokedFirstStdD'][indRow]
        elif minimum == 'pValueMid':
            significantCells[indRow] = responsivedb['pValMidFRD'][indRow]
            expUnexpRatio[indRow] = responsivedb['meanEvokedSecondOddD'][indRow] / responsivedb['meanEvokedSecondStdD'][indRow]
        else:
            significantCells[indRow] = responsivedb['pValLowFRD'][indRow]
            expUnexpRatio[indRow] = responsivedb['meanEvokedThirdOddD'][indRow] / responsivedb['meanEvokedThirdStdD'][indRow]

    # -- Adding a new column to the database using the array we created earlier. --
    responsivedb['mostRespFreqExpectationPValueD'] = significantCells
    responsivedb['expUnexpRatioMostRespFreqD'] = expUnexpRatio

    # -- If either of the smallest pValues in the sequence are below the pValue threshold and there is increased firing for the oddball, that cell is significantly modulated. --
    #signModulatedCellsA = np.where((responsivedb['mostRespFreqExpectationPValueA'] < pValueThreshold) & (responsivedb['expUnexpRatioMostRespFreqA'] > 1))
    signCells = responsivedb[responsivedb.mostRespFreqExpectationPValueD < pValueThreshold]
    signModulatedCells = signCells[signCells.expUnexpRatioMostRespFreqD > 1]


    print('Number of responsive cells in the descending session: {}'.format(len(responsivedb)))

    print('Number of cells that showed a significant difference between expected and unexpected firing rates in the descending session: {}'.format(len(signCells)))

    print('Number of cells that showed a significant difference between expected and unexpected firing rates where there was more firing for the unexpected tone in the descending session: {}'.format(len(signModulatedCells)))

    return responsivedb

'''
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

    print('Number of responsive cells: {}'.format(len(responsivedb)))
    print('Number of cells that showed a significant difference between expected and unexpected firing rates: {}'.format(numSignRespCells))
    percentSignRespCells = numSignRespCells / len(responsivedb) * 100
    print('Percentage of significantly responsive cells: {:.2f}%'.format(percentSignRespCells))

    return signRespCells
'''

#signRespCellsdb = comparing_odd_std_significance(responsivedb)
signRespCellsdbA = comparing_odd_std_significance_ascending(responsivedbA, pValueThreshold)
signRespCellsdbD = comparing_odd_std_significance_descending(responsivedbD, pValueThreshold)


'''
# -- Saving the responsive database --
celldatabase.save_hdf(responsivedb, dbFilename)
print('Saved responsive database to {}'.format(dbFilename))

# -- Saving the database of significantly responsive cells. --
dbFilename = os.path.join(dbPath,'newsignRespCellsdb_{}.h5'.format(studyparams.STUDY_NAME))
celldatabase.save_hdf(signRespCellsdb, dbFilename)
print('Saved significantly responsive cell database to {}'.format(dbFilename))
'''
