# -*- coding: utf-8 -*-
"""
This script will try to replicate and improve on some of the functions of celldatabase.py. 
This script can:
1. Create a basic database (minimally selected for SSQ and ISIviolations)
2. select by spike shape quality interspike interval violations (threshold value held in studyparams.py)
3. select cells that have either frequency or AM data

Created on Fri Sep 18 14:19:55 2020
@author: Devin Henderling
"""

import os
import sys
import numpy as np
import pandas as pd
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore

# for testing 
answered = 0
answered2 = 0
select_for = 0
while answered == 0:
    test = input("Are you testing this script? \n")
    if test.upper() in ["YES", "Y", "1"]:
        d1mice = studyparams.SINGLE_MOUSE
        while answered2 == 0:
            select = input("Would you like to test cell selection? n/")
            print("Starting script test...")
            if select.upper() in ["YES", "Y", "1"]:
                dbpath = os.path.join(settings.TEST_PATH, studyparams.STUDY_NAME, '{}_selected_test.h5'.format(d1mice[0]))
                select_for = 1
                answered2 = 1
            elif select.upper() in ["NO", "N", "0"]:
                dbpath = os.path.join(settings.TEST_PATH, studyparams.STUDY_NAME, '{}_test.h5'.format(d1mice[0]))
                answered2 = 1
            else:
                print("Sorry, please respond with yes or no")
        answered = 1
    elif test.upper() in ["NO", "N", "0"]:
        d1mice = studyparams.ASTR_D1_CHR2_MICE
        while answered2 == 0:
            select = input("Would you like to use cell selection? n/")
            print("Beginning database generation...")
            if select.upper() in ["YES", "Y", "1"]:
                dbpath = os.path.join(settings.TEST_PATH, studyparams.STUDY_NAME, '{}_selected.h5'.format(studyparams.DATABASE_NAME))
                select_for = 1
                answered2 = 1
            elif select.upper() in ["NO", "N", "0"]:
                dbpath = os.path.join(settings.TEST_PATH, studyparams.STUDY_NAME, '{}.h5'.format(studyparams.DATABASE_NAME))
                answered2 = 1 
            else:
                print("Sorry, please respond with yes or no")
        answered = 1
    else:
        print("Sorry, please respond with yes or no")

# ==================================================
        
# Generating basic database, minimally selected for SSQ and ISI
basicDB = celldatabase.generate_cell_database_from_subjects(d1mice)

if select_for:
    # selecting for SSQ and ISIviolations specfied in studyparams
    selectedDB = basicDB.query(studyparams.FIRST_FLTRD_CELLS)
    # selecting for those with either AM or tuning data
    hasTC = selectedDB['sessionType'].apply(lambda s: 'tuningCurve' in s)
    hasAM = selectedDB['sessionType'].apply(lambda s: 'am' in s)
    finalDB = selectedDB[hasTC & hasAM]
else:
    finalDB = basicDB
              
# Saving database
celldatabase.save_hdf(finalDB, dbpath)
print("SAVED DATAFRAME to {}".format(dbpath))