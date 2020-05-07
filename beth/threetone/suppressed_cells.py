
"""
Finding suppression cells from the significantly responsive database of cells.
"""

from __future__ import division
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import celldatabase
import studyparams
reload(studyparams)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'signRespCellsdb_{}.h5'.format(studyparams.STUDY_NAME))
# -- Load the database of responsive cells --
signRespCells = celldatabase.load_hdf(dbFilename)

suppressedCells = []

for indRow, dbRow in signRespCells.iterrows():
    highBaseA = signRespCells['meanBaseHighA'][indRow]
    highEvokedA = signRespCells['meanEvokedHighA'][indRow]
    midBaseA = signRespCells['meanBaseMidA'][indRow]
    midEvokedA = signRespCells['meanEvokedMidA'][indRow]
    lowBaseA = signRespCells['meanBaseLowA'][indRow]
    lowEvokedA = signRespCells['meanEvokedLowA'][indRow]

    if signRespCells['mostRespFreqPValueOddStdA'][indRow] == signRespCells['pValHighFRA'][indRow]:
        if highBaseA > highEvokedA:
            suppressedCells.append(signRespCells.iloc[indRow])
            continue
    elif signRespCells['mostRespFreqPValueOddStdA'][indRow] == signRespCells['pValMidFRA'][indRow]:
        if midBaseA > midEvokedA:
            suppressedCells.append(signRespCells.iloc[indRow])
            continue
    else:
        if lowBaseA > lowEvokedA:
            suppressedCells.append(signRespCells.iloc[indRow])
            continue

    highBaseD = signRespCells['meanBaseHighD'][indRow]
    highEvokedD = signRespCells['meanEvokedHighD'][indRow]
    midBaseD = signRespCells['meanBaseMidD'][indRow]
    midEvokedD = signRespCells['meanEvokedMidD'][indRow]
    lowBaseD = signRespCells['meanBaseLowD'][indRow]
    lowEvokedD = signRespCells['meanEvokedLowD'][indRow]

    if signRespCells['mostRespFreqPValueOddStdD'][indRow] == signRespCells['pValHighFRD'][indRow]:
        if highBaseD > highEvokedD:
            suppressedCells.append(signRespCells.iloc[indRow])
    elif signRespCells['mostRespFreqPValueOddStdD'][indRow] == signRespCells['pValMidFRD'][indRow]:
        if midBaseD > midEvokedD:
            suppressedCells.append(signRespCells.iloc[indRow])
    else:
        if lowBaseD > lowEvokedD:
            suppressedCells.append(signRespCells.iloc[indRow])

suppresseddb = pd.DataFrame(suppressedCells)

# -- Saving the database of suppressed significantly responsive cells. --
dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'suppressedRespCellsdb_{}.h5'.format(studyparams.STUDY_NAME))
celldatabase.save_hdf(suppresseddb, dbFilename)
print('Saved suppressed firing significantly responsive cell database to {}'.format(dbFilename))
