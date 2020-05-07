"""
Plotting oddball evoked firing rate vs standard evoked firing rate and oddball evoked firing rate vs standard evoked firing rate for only the most responsive frequency.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
import studyparams
reload(studyparams)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'responsivedb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of cells --
responsivedb = celldatabase.load_hdf(dbFilename)


x = np.arange(0, 400)
y = x
plt.figure()
plt.plot(responsivedb['meanEvokedFirstStdA'], responsivedb['meanEvokedFirstOddA'], 'o', markersize=4, color='c', label='High Freq')
plt.plot(responsivedb['meanEvokedSecondStdA'], responsivedb['meanEvokedSecondOddA'], 'x', markersize=4, color='r', label='Middle Freq')
plt.plot(responsivedb['meanEvokedThirdStdA'], responsivedb['meanEvokedThirdOddA'], '*', markersize=4, color='b', label='Low Freq')
plt.plot(x, y, '-', markersize=3, color='k')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Standard Evoked Firing Rate [spikes/s]')
plt.ylabel('Oddball Evoked Firing Rate [spikes/s]')
plt.title('Ascending')
plt.legend()

plt.figure()
plt.plot(responsivedb['meanEvokedFirstStdD'], responsivedb['meanEvokedFirstOddD'], 'o', markersize=4, color='c', label='High Freq')
plt.plot(responsivedb['meanEvokedSecondStdD'], responsivedb['meanEvokedSecondOddD'], 'x', markersize=4, color='r', label='Middle Freq')
plt.plot(responsivedb['meanEvokedThirdStdD'], responsivedb['meanEvokedThirdOddD'], '*', markersize=4, color='b', label='Low Freq')
plt.plot(x, y, '-', markersize=3, color='k')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Standard Evoked Firing Rate [spikes/s]')
plt.ylabel('Oddball Evoked Firing Rate [spikes/s]')
plt.title('Descending')
plt.legend()

#plt.show()

evokedOddA = np.tile(np.nan, len(responsivedb))
evokedStdA = np.tile(np.nan, len(responsivedb))

for indRow, dbRow in responsivedb.iterrows():
    pValueHighA = responsivedb['pValHighResponseA'][indRow]
    pValueMidA = responsivedb['pValMidResponseA'][indRow]
    pValueLowA = responsivedb['pValLowResponseA'][indRow]
    pValuesA = dict(pValueHA = pValueHighA, pValueMA = pValueMidA, pValueLA = pValueLowA)
    # -- The best frequency is the one with the lowest pValue in sound_responsive_cells. --
    minimumA = min(pValuesA, key=pValuesA.get)

    # -- This adds to a list the pValue corresponding to whichever frequency (high, middle, low) had the lowest pValue when comparing evoked to baseline spike counts for the ascending sequence --
    if minimumA == 'pValueHA':
        evokedStdA[indRow] = responsivedb['meanEvokedFirstStdA'][indRow]
        evokedOddA[indRow] = responsivedb['meanEvokedFirstOddA'][indRow]
    elif minimumA == 'pValueMA':
        evokedStdA[indRow] = responsivedb['meanEvokedSecondStdA'][indRow]
        evokedOddA[indRow] = responsivedb['meanEvokedSecondOddA'][indRow]
    else:
        evokedStdA[indRow] = responsivedb['meanEvokedThirdStdA'][indRow]
        evokedOddA[indRow] = responsivedb['meanEvokedThirdOddA'][indRow]

evokedOddD = np.tile(np.nan, len(responsivedb))
evokedStdD = np.tile(np.nan, len(responsivedb))

for indRow, dbRow in responsivedb.iterrows():
    pValueHighD = responsivedb['pValHighResponseD'][indRow]
    pValueMidD = responsivedb['pValMidResponseD'][indRow]
    pValueLowD = responsivedb['pValLowResponseD'][indRow]
    pValuesD = dict(pValueHD = pValueHighD, pValueMD = pValueMidD, pValueLD = pValueLowD)
    # -- The best frequency is the one with the lowest pValue in sound_responsive_cells. --
    minimumD = min(pValuesD, key=pValuesD.get)

    # -- This adds to a list the pValue corresponding to whichever frequency (high, middle, low) had the lowest pValue when comparing evoked to baseline spike counts for the ascending sequence --
    if minimumD == 'pValueHD':
        evokedStdD[indRow] = responsivedb['meanEvokedFirstStdD'][indRow]
        evokedOddD[indRow] = responsivedb['meanEvokedFirstOddD'][indRow]
    elif minimumD == 'pValueMA':
        evokedStdD[indRow] = responsivedb['meanEvokedSecondStdD'][indRow]
        evokedOddD[indRow] = responsivedb['meanEvokedSecondOddD'][indRow]
    else:
        evokedStdD[indRow] = responsivedb['meanEvokedThirdStdD'][indRow]
        evokedOddD[indRow] = responsivedb['meanEvokedThirdOddD'][indRow]

plt.figure()
plt.plot(evokedOddA, evokedStdA, 'o', markersize=4, color='b', label='Ascending')
plt.plot(evokedOddD, evokedStdD, 'o', markersize=4, color='r', label='Descending')
plt.plot(x, y, '-', markersize=2, color='k')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Standard Evoked Firing Rate [spikes/s]')
plt.ylabel('Oddball Evoked Firing Rate [spikes/s]')
plt.title('Most Responsive Frequency')
plt.legend()
plt.show()
