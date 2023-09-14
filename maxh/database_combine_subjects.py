"""
Combines the databases of all subjects into one database. You must choose which type of databases you're combining:
all trials, nonrunning trials, or running trials.
"""

import os
import pandas as pd
from jaratoolbox import celldatabase
import settings
import studyparams

"""
Choose which type of databases you're combining.
1 = databases with all trials.
2 = databases with only nonrunning trials.
3 = databases with only running trials.
"""

database = 1

databasePath = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME)
arrayOfDatabases = []

#subjects = ['acid010']
subjects = studyparams.SUBJECTS

for subject in subjects:
    if database == 1:
        filename = os.path.join(databasePath, f'{subject}_puretone_and_oddball_calcs_all.h5')
    if database == 2:
        filename = os.path.join(databasePath, f'{subject}_puretone_and_oddball_calcs_nonRunning.h5')
    if database == 3:
        filename = os.path.join(databasePath, f'{subject}_puretone_and_oddball_calcs_running.h5')
    
    celldb = celldatabase.load_hdf(filename)
    arrayOfDatabases.append(celldb)


combinedDBs = pd.concat(arrayOfDatabases)

if database == 1:
    newFilename = os.path.join(databasePath, f'allMice_puretone_and_oddball_calcs_all.h5')
if database == 2:
    newFilename = os.path.join(databasePath, f'allMice_puretone_and_oddball_calcs_nonRunning.h5')
if database == 3:
    newFilename = os.path.join(databasePath, f'allMice_puretone_and_oddball_calcs_running.h5')

celldatabase.save_hdf(combinedDBs, newFilename)