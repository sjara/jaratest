# -*- coding: utf-8 -*-
"""
This script creates a basic database from an inforec file using the 
"generate_cell_database_from_subjects" method found in the "celldatabase" module.

The database generated with this script is filtered by:
1. ISI violations less than 0.05
2. Spike shape quality greater than 2

Created on Jan 17, 2021
Author: Devin Henderling
"""

import os
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings

# ========================== Run Mode ==========================

ONE_SUBJECT = 1 # Set to 1 to generate database for one animal for faster testing

if ONE_SUBJECT:
    d1mice = studyparams.SINGLE_MOUSE
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   '{}_clusters.h5'.format(d1mice[0]))
else:
    d1mice = studyparams.ASTR_D1_CHR2_MICE 
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME,
                                   'all_clusters.h5')
 
# ========================== Basic Database Creation ==========================
        
# Generates basic database, minimally selected for SSQ and ISI
db = celldatabase.generate_cell_database_from_subjects(d1mice)   

# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("\n SAVED DATAFRAME TO: \n {}".format(outputDirectory))