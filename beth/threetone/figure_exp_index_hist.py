"""
This script generates expectation index histograms for all frequencies in both sessions for either the responsive cells and significant responsive cells or suppression cells and significant suppression cells.

"""
from __future__ import division
from scipy import stats
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
import studyparams
reload(studyparams)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
# -- Loading responsive cell database --
dbFilename = os.path.join(dbPath,'responsivedb_{}.h5'.format(studyparams.STUDY_NAME))
responsivedb = celldatabase.load_hdf(dbFilename)
# -- Loading suppressed cell database --
dbFilename = os.path.join(dbPath,'suppressedRespCellsdb_{}.h5'.format(studyparams.STUDY_NAME))
suppresseddb = celldatabase.load_hdf(dbFilename)

def expectation_index_hist(database, name):

    # -- Ascending --
    highFreqRespCellsA = []
    midFreqRespCellsA = []
    lowFreqRespCellsA = []
    for indRow, dbRow in database.iterrows():
        pValueHighA = database['pValHighResponseA'][indRow]
        pValueMidA = database['pValMidResponseA'][indRow]
        pValueLowA = database['pValLowResponseA'][indRow]
        pValuesA = dict(pValueHA = pValueHighA, pValueMA = pValueMidA, pValueLA = pValueLowA)
        # -- The best frequency is the one with the lowest pValue in sound responsive cells. --
        minimumA = min(pValuesA, key=pValuesA.get)
        # -- Appending to a list the cells that were most responsive to each of the three frequencies. --
        if minimumA == 'pValueHA':
            highFreqRespCellsA.append(database.iloc[indRow])
        elif minimumA == 'pValueMA':
            midFreqRespCellsA.append(database.iloc[indRow])
        else:
            lowFreqRespCellsA.append(database.iloc[indRow])

    respHighA = pd.DataFrame(highFreqRespCellsA) # Database of cells where the high frequency tone in the ascending sequence is the most responsive
    respMidA = pd.DataFrame(midFreqRespCellsA) # Database of cells where the middle frequency tone in the ascending sequence is the most responsive
    respLowA = pd.DataFrame(lowFreqRespCellsA) # Database of cells where the low frequency tone in the ascending sequence is the most responsive

    signRespCellsHighA = respHighA.query('pValHighFRA < 0.05') # Cells that were most responsive for the high frequency sound that also show a significant difference in firing between the high frequency oddball and standard (first oddball/std)
    signRespCellsMidA = respMidA.query('pValMidFRA < 0.05') # Cells that were most responsive for the middle frequency sound that also show a significant difference in firing between the high frequency oddball and standard (first oddball/std)
    signRespCellsLowA = respLowA.query('pValLowFRA < 0.05') # Cells that were most responsive for the low frequency sound that also show a significant difference in firing between the high frequency oddball and standard (first oddball/std)

    # -- Descending --
    highFreqRespCellsD = []
    midFreqRespCellsD = []
    lowFreqRespCellsD = []
    for indRow, dbRow in database.iterrows():
        pValueHighD = database['pValHighResponseD'][indRow]
        pValueMidD = database['pValMidResponseD'][indRow]
        pValueLowD = database['pValLowResponseD'][indRow]
        pValuesD = dict(pValueHD = pValueHighD, pValueMD = pValueMidD, pValueLD = pValueLowD)
        # -- The best frequency is the one with the lowest pValue in sound responsive cells. --
        minimumD = min(pValuesD, key=pValuesD.get)

        if minimumD == 'pValueHD':
            highFreqRespCellsD.append(database.iloc[indRow])
        elif minimumD == 'pValueMD':
            midFreqRespCellsD.append(database.iloc[indRow])
        else:
            lowFreqRespCellsD.append(database.iloc[indRow])

    respHighD = pd.DataFrame(highFreqRespCellsD)
    respMidD = pd.DataFrame(midFreqRespCellsD)
    respLowD = pd.DataFrame(lowFreqRespCellsD)

    signRespCellsHighD = respHighD.query('pValHighFRD < 0.05')
    signRespCellsMidD = respMidD.query('pValMidFRD < 0.05')
    signRespCellsLowD = respLowD.query('pValLowFRD < 0.05')

    bins = 30
    plt.figure(figsize=(10,4.5)).suptitle(name,fontsize=9,y=1.01)
    ax = plt.subplot2grid((2,3), (0,0)) # Subplots

    ax0 = plt.subplot2grid((2,3), (0,0))
    highIndA = respHighA['expIndHighA']
    plt.hist(highIndA[~np.isnan(highIndA)], bins, histtype='step', color='limegreen')
    signCellsHighA = signRespCellsHighA['expIndHighA']
    plt.hist(signCellsHighA[~np.isnan(signCellsHighA)], bins, color='limegreen')
    plt.title('High Frequency - Ascending', fontsize=8)
    plt.xlabel('Expectation Index', fontsize=8)
    plt.ylabel('Num of Cells', fontsize=8)
    plt.xlim(-1, 1)

    ax1 = plt.subplot2grid((2,3), (0,1))
    midIndA = respMidA['expIndMidA']
    plt.hist(midIndA[~np.isnan(midIndA)], bins, histtype='step', color='dodgerblue')
    signCellsMidA = signRespCellsMidA['expIndMidA']
    plt.hist(signCellsMidA[~np.isnan(signCellsMidA)], bins, color='dodgerblue')
    plt.title('Middle Frequency - Ascending', fontsize=8)
    plt.xlabel('Expectation Index', fontsize=8)
    plt.ylabel('Num of Cells', fontsize=8)
    plt.xlim(-1, 1)

    ax2 = plt.subplot2grid((2,3), (0,2))
    lowIndA = respLowA['expIndLowA']
    plt.hist(lowIndA[~np.isnan(lowIndA)], bins, histtype='step', color='darkorchid')
    signCellsLowA = signRespCellsLowA['expIndLowA']
    plt.hist(signCellsLowA[~np.isnan(signCellsLowA)], bins, color='darkorchid')
    plt.title('Low Frequency - Ascending', fontsize=8)
    plt.xlabel('Expectation Index', fontsize=8)
    plt.ylabel('Num of Cells', fontsize=8)
    plt.xlim(-1, 1)

    ax3 = plt.subplot2grid((2,3), (1,0))
    highIndD = respHighD['expIndHighD']
    plt.hist(highIndD[~np.isnan(highIndD)], bins, histtype='step', color='limegreen')
    signCellsHighD = signRespCellsHighD['expIndHighD']
    plt.hist(signCellsHighD[~np.isnan(signCellsHighD)], bins, color='limegreen')
    plt.title('High Frequency - Descending', fontsize=8)
    plt.xlabel('Expectation Index', fontsize=8)
    plt.ylabel('Num of Cells', fontsize=8)
    plt.xlim(-1, 1)

    ax4 = plt.subplot2grid((2,3), (1,1))
    midIndD = respMidD['expIndMidD']
    plt.hist(midIndD[~np.isnan(midIndD)], bins, histtype='step', color='dodgerblue')
    signCellsMidD = signRespCellsMidD['expIndMidD']
    plt.hist(signCellsMidD[~np.isnan(signCellsMidD)], bins, color='dodgerblue')
    plt.title('Middle Frequency - Descending', fontsize=8)
    plt.xlabel('Expectation Index', fontsize=8)
    plt.ylabel('Num of Cells', fontsize=8)
    plt.xlim(-1, 1)

    ax5 = plt.subplot2grid((2,3), (1,2))
    lowIndD = respLowD['expIndLowD']
    plt.hist(lowIndD[~np.isnan(lowIndD)], bins, histtype='step', color='darkorchid')
    signCellsLowD = signRespCellsLowD['expIndLowD']
    plt.hist(signCellsLowD[~np.isnan(signCellsLowD)], bins, color='darkorchid')
    plt.title('Low Frequency - Descending', fontsize=8)
    plt.xlabel('Expectation Index', fontsize=8)
    plt.ylabel('Num of Cells', fontsize=8)
    plt.xlim(-1, 1)

    plt.tight_layout()
    plt.gcf().set_size_inches([10,4.5])
    figFormat = 'png'
    figFilename ='expectation_index_hist_{}.{}'.format(name, figFormat)
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)

    plt.show()

    # -- Statistics --
    ## -- Ascending --
    print('Ascending:')
    ### -- High Frequency --
    highIndA = highIndA[~np.isnan(highIndA)]
    medianHighIndA = np.median(highIndA)
    signCellsHighA = signCellsHighA[~np.isnan(signCellsHighA)]
    medianSignCellsHighA = np.median(signCellsHighA)
    print('Median High Freq Responsive = {}').format(medianHighIndA)
    print('Median High Freq Significant = {}').format(medianSignCellsHighA)

    statHighA, pHighA, medHighA, tblHighA = stats.median_test(highIndA, signCellsHighA)
    print('Median_test = {}').format(medHighA)

    ### -- Middle Frequency --
    midIndA = midIndA[~np.isnan(midIndA)]
    medianMidIndA = np.median(midIndA)
    signCellsMidA = signCellsMidA[~np.isnan(signCellsMidA)]
    medianSignCellsMidA = np.median(signCellsMidA)
    print('Median Mid Freq Responsive = {}').format(medianMidIndA)
    print('Median Mid Freq Significant = {}').format(medianSignCellsMidA)

    statMidA, pMidA, medMidA, tblMidA = stats.median_test(midIndA, signCellsMidA)
    print('Median_test = {}').format(medMidA)

    ### -- Low Frequency --
    lowIndA = lowIndA[~np.isnan(lowIndA)]
    medianLowIndA = np.median(lowIndA)
    signCellsLowA = signCellsLowA[~np.isnan(signCellsLowA)]
    medianSignCellsLowA = np.median(signCellsLowA)
    print('Median Low Freq Responsive = {}').format(medianLowIndA)
    print('Median Low Freq Significant = {}').format(medianSignCellsLowA)

    statLowA, pLowA, medLowA, tblLowA = stats.median_test(lowIndA, signCellsLowA)
    print('Median_test = {}').format(medLowA)

    ## -- Descending --
    print('Descending:')
    ### -- High Frequency --
    highIndD = highIndD[~np.isnan(highIndD)]
    medianHighIndD = np.median(highIndD)
    signCellsHighD = signCellsHighD[~np.isnan(signCellsHighD)]
    medianSignCellsHighD = np.median(signCellsHighD)
    print('Median High Freq Responsive = {}').format(medianHighIndD)
    print('Median High Freq Significant = {}').format(medianSignCellsHighD)

    statHighD, pHighD, medHighD, tblHighD = stats.median_test(highIndD, signCellsHighD)
    print('Median_test = {}').format(medHighD)

    ### -- Middle Frequency --
    midIndD = midIndD[~np.isnan(midIndD)]
    medianMidIndD = np.median(midIndD)
    signCellsMidD = signCellsMidD[~np.isnan(signCellsMidD)]
    medianSignCellsMidD = np.median(signCellsMidD)
    print('Median Mid Freq Responsive = {}').format(medianMidIndD)
    print('Median Mid Freq Significant = {}').format(medianSignCellsMidD)

    statMidD, pMidD, medMidD, tblMidD = stats.median_test(midIndD, signCellsMidD)
    print('Median_test = {}').format(medMidD)

    ### -- Low Frequency --
    lowIndD = lowIndD[~np.isnan(lowIndD)]
    medianLowIndD = np.median(lowIndD)
    signCellsLowD = signCellsLowD[~np.isnan(signCellsLowD)]
    medianSignCellsLowD = np.median(signCellsLowD)
    print('Median Low Freq Responsive = {}').format(medianLowIndD)
    print('Median Low Freq Significant = {}').format(medianSignCellsLowD)

    statLowD, pLowD, medLowD, tblLowD = stats.median_test(lowIndD, signCellsLowD)
    print('Median_test = {}').format(medLowD)

    ### -- Responsive sessions --
    statA, pA, medA, tblA = stats.median_test(highIndA, midIndA, lowIndA)
    statD, pD, medD, tblD = stats.median_test(highIndD, midIndD, lowIndD)
    print('Ascending median test = {}').format(medA)
    print('Descending median test = {}').format(medD)

    ### -- Significantly responsive sessions --
    statSignA, pSignA, medSignA, tblSignA = stats.median_test(signCellsHighA, signCellsMidA, signCellsLowA)
    statSignD, pSignD, medSignD, tblSignD = stats.median_test(signCellsHighD, signCellsMidD, signCellsLowD)
    print('Ascending median test for significantly responsive cells = {}').format(medSignA)
    print('Descending median test for significantly responsive cells = {}').format(medSignD)

    ### -- Additional Stats --
    print(name)
    percentCellsShiftedRightHighA = sum(highIndA > 0.0) / len(respHighA) * 100
    percentSignCellsShiftedRightHighA = sum(signCellsHighA > 0.0) / len(signRespCellsHighA) * 100
    print('High frequency ascending - {:.2f}% of cells have an expectation index shifted to signify an increase in firing from an unexpected sound to an expected one and {:.2f}% of significantly responsive cells show the same shift.'.format(percentCellsShiftedRightHighA, percentSignCellsShiftedRightHighA))

    percentCellsShiftedRightMidA = sum(midIndA > 0.0) / len(respMidA) * 100
    percentSignCellsShiftedRightMidA = sum(signCellsMidA > 0.0) / len(signRespCellsMidA) * 100
    print('Middle frequency ascending - {:.2f}% of cells have an expectation index shifted to signify an increase in firing from an unexpected sound to an expected one and {:.2f}% of significantly responsive cells show the same shift.'.format(percentCellsShiftedRightMidA, percentSignCellsShiftedRightMidA))

    percentCellsShiftedRightLowA = sum(lowIndA > 0.0) / len(respLowA) * 100
    percentSignCellsShiftedRightLowA = sum(signCellsLowA > 0.0) / len(signRespCellsLowA) * 100
    print('Low frequency ascending - {:.2f}% of cells have an expectation index shifted to signify an increase in firing from an unexpected sound to an expected one and {:.2f}% of significantly responsive cells show the same shift.'.format(percentCellsShiftedRightLowA, percentSignCellsShiftedRightLowA))

    percentCellsShiftedRightHighD = sum(highIndD > 0.0) / len(respHighD) * 100
    percentSignCellsShiftedRightHighD = sum(signCellsHighD > 0.0) / len(signRespCellsHighD) * 100
    print('High frequency descending - {:.2f}% of cells have an expectation index shifted to signify an increase in firing from an unexpected sound to an expected one and {:.2f}% of significantly responsive cells show the same shift.'.format(percentCellsShiftedRightHighD, percentCellsShiftedRightHighD))

    percentCellsShiftedRightMidD = sum(midIndD > 0.0) / len(respMidD) * 100
    percentSignCellsShiftedRightMidD = sum(signCellsMidD > 0.0) / len(signRespCellsMidD) * 100
    print('Middle frequency descending - {:.2f}% of cells have an expectation index shifted to signify an increase in firing from an unexpected sound to an expected one and {:.2f}% of significantly responsive cells show the same shift.'.format(percentCellsShiftedRightMidD, percentSignCellsShiftedRightMidD))

    percentCellsShiftedRightLowD = sum(lowIndD > 0.0) / len(respLowD) * 100
    percentSignCellsShiftedRightLowD = sum(signCellsLowD > 0.0) / len(signRespCellsLowD) * 100
    print('Low frequency descending - {:.2f}% of cells have an expectation index shifted to signify an increase in firing from an unexpected sound to an expected one and {:.2f}% of significantly responsive cells show the same shift.'.format(percentCellsShiftedRightLowD, percentSignCellsShiftedRightLowD))


expectation_index_hist(responsivedb, 'responsive_cells')
#expectation_index_hist(suppresseddb, 'suppression_cells')
