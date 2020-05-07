"""
Plotting histogram of number of cells vs expectation index along with which of those are significantly responsive for each of the three frequencies and for both sessions for five auditory regions (primary AC(0-1300um), ventral AC(1300-1800um), TeA(1800-2175um), Ectorhinal(2175-2675um), and Perirhinal(2675-3050um)).
"""

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

def expectation_index_hist_by_region(database, region, title):
    bins = 30
    plt.figure(figsize=(10,4.5)).suptitle(region[0] + ' ' + title, fontsize=9, y=1.01)
    ax = plt.subplot2grid((2,3), (0,0))

    area = database.query(region[1])
    # -- Reindexing the responsive database --
    area = area.reset_index(drop=True)

    # -- Ascending --
    highFreqRespCellsA = []
    midFreqRespCellsA = []
    lowFreqRespCellsA = []
    for indRow, dbRow in area.iterrows():
        pValueHighA = area['pValHighResponseA'][indRow]
        pValueMidA = area['pValMidResponseA'][indRow]
        pValueLowA = area['pValLowResponseA'][indRow]
        pValuesA = dict(pValueHA = pValueHighA, pValueMA = pValueMidA, pValueLA = pValueLowA)
        # -- The best frequency is the one with the lowest pValue in sound responsive cells. --
        minimumA = min(pValuesA, key=pValuesA.get)
        # -- Appending to a list the cells that were most responsive to each of the three frequencies. --
        if minimumA == 'pValueHA':
            highFreqRespCellsA.append(area.iloc[indRow])
        elif minimumA == 'pValueMA':
            midFreqRespCellsA.append(area.iloc[indRow])
        else:
            lowFreqRespCellsA.append(area.iloc[indRow])

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
    for indRow, dbRow in area.iterrows():
        pValueHighD = area['pValHighResponseD'][indRow]
        pValueMidD = area['pValMidResponseD'][indRow]
        pValueLowD = area['pValLowResponseD'][indRow]
        pValuesD = dict(pValueHD = pValueHighD, pValueMD = pValueMidD, pValueLD = pValueLowD)
        # -- The best frequency is the one with the lowest pValue in sound responsive cells. --
        minimumD = min(pValuesD, key=pValuesD.get)

        if minimumD == 'pValueHD':
            highFreqRespCellsD.append(area.iloc[indRow])
        elif minimumD == 'pValueMD':
            midFreqRespCellsD.append(area.iloc[indRow])
        else:
            lowFreqRespCellsD.append(area.iloc[indRow])

    respHighD = pd.DataFrame(highFreqRespCellsD)
    respMidD = pd.DataFrame(midFreqRespCellsD)
    respLowD = pd.DataFrame(lowFreqRespCellsD)

    signRespCellsHighD = respHighD.query('pValHighFRD < 0.05')
    signRespCellsMidD = respMidD.query('pValMidFRD < 0.05')
    signRespCellsLowD = respLowD.query('pValLowFRD < 0.05')

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
    figFilename ='{}_expectation_index_hist.{}'.format(region[0], figFormat)
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.show()


# -- Regions --
primaryAC = ['PrimaryAC', 'depth > 0 & depth < 1300']
ventralAC = ['VentralAC', 'depth > 1300 & depth < 1800']
TeA = ['TeA', 'depth > 1800 & depth < 2175']
ECT = ['ECT', 'depth > 2175 & depth < 2675']
PERI = ['PERI', 'depth > 2675 & depth < 3050']

expectation_index_hist_by_region(responsivedb, primaryAC, 'Responsive')
expectation_index_hist_by_region(responsivedb, ventralAC, 'Responsive')

#expectation_index_hist_by_region(suppresseddb, primaryAC, 'Suppressed')
#expectation_index_hist_by_region(suppresseddb, ventralAC, 'Suppressed')
