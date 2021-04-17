"""
Make a database that contains only "good" cells.
That is, those that:
- Have good ISI and spike quality.
- Have a laser session.
- Have either frequency-tuning session or amplitude-modulated session.
"""

import os
import sys
from jaratoolbox import celldatabase
from jaratoolbox import settings
sys.path.append('..')
import studyparams

origDB = 'tempdb_full_original.h5'
outputDB = 'tempdb_subset_good.h5'

pathToDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, origDB)
print(f'Loading {pathToDB}...')
cellDB = celldatabase.load_hdf(pathToDB)
print('Done')

cellDB = cellDB.query(studyparams.FIRST_FLTRD_CELLS)

hasLaser = cellDB['sessionType'].apply(lambda s: 'laserpulse' in s)
hasTC = cellDB['sessionType'].apply(lambda s: 'tuningCurve' in s)
hasAM = cellDB['sessionType'].apply(lambda s: 'am' in s)

# -- Show a dataframe containing only cells that have both TC and AM sessions
cellDB = cellDB[hasLaser & (hasTC | hasAM)]

pathToNewDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, outputDB)
print(f'Saving {pathToNewDB}')
celldatabase.save_hdf(cellDB, pathToNewDB)
