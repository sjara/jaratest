# -*- coding: utf-8 -*-
"""
This script loads the basic database created with basic_database_generation.py and selects reliable 
cells that have data for sound reponse comparison. 

The database generated with this script is filtered by:
1. Laserpulse session ran for cell
2. Either tuning curve or AM session ran for cell
3. Manual verification (Unreasonable cells removed)
4. Parameters specified in basic_database_generation.py

Created on Jan 17, 2021
Author: Devin Henderling
"""

import os
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings

# ========================== Run Mode ==========================

TEST = 0 # Set to 1 to generate database for one animal for faster testing

if TEST:
    d1mice = studyparams.SINGLE_MOUSE 
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   '{}_cells.h5'.format(d1mice[0]))
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   '{}_clusters.h5'.format(d1mice[0]))
else:
    d1mice = studyparams.ASTR_D1_CHR2_MICE
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'all_cells.h5')
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'all_clusters.h5')
 
# ========================== Database Filtering ==========================

print('Loading basic database...')

# Loads basic database
db = celldatabase.load_hdf(inputDirectory)  

# Selects cells with a laserpulse session for D1 vs. nD1 determination
hasLP = db['sessionType'].apply(lambda s: 'laserpulse' in s)
db = db[hasLP]
    
# Selects cells with either tuning curve or AM session for sound comparison
hasTC_AM = db['sessionType'].apply(lambda s: 'tuningCurve' in s or 'am' in s)
db = db[hasTC_AM]

# Removes clusters that were manually selected as non-cells
# TODO: Add this 

# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("\n SAVED DATAFRAME TO: \n {}".format(outputDirectory))