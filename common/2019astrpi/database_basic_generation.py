# -*- coding: utf-8 -*-
"""
This script creates a basic database from an inforec file using 
celldatabase.generate_cell_database_from_subjects()

The database generated with this script is filtered by:
1. ISI violations less than 0.05
2. Spike shape quality greater than 2

If run normally, it will use all animals and store in a default database. The two arguements 
'SUBJECT' and 'TAG' can also be used. 

SUBJECT can be a singular subject, 'all', or 'test'. 'all' will use all of the subjects listed in 
studyparams.py. 'test' will use the test subject listed in studyparams.py. If nothing is 
specified, all subjects will be ran. 

Optionally you can set a TAG on the database (using file name acceptable characters). You must enter 
a subject parameter before entering a tag. Aditionally, these two must be the first two parameters 
entered, any subsequent will not be used. If 'AM' or 'TC' are in the tag, 'AM' or 'TC' will not be 
added when each respective statistics script is run.

Run as:
database_.py SUBJECT TAG 
"""
import sys
import os
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings

# ========================== Run Mode ==========================

NO_TAG = 0 # Set to 1 if no tag 

# Determing run mode by arguments
if __name__ == "__main__":
    if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
        arguments = sys.argv[1:] # Script parameters 
        if arguments[0] == "all":
            d1mice = studyparams.ASTR_D1_CHR2_MICE
            subjects = 'all'
        if isinstance(arguments[0], str):
            d1mice = []
            subjects = str(arguments[0]) 
            d1mice.append(subjects)
            if d1mice[0] not in studyparams.ASTR_D1_CHR2_MICE:
                answer = input('Subject could not be found, Would you like to run for all animals?')
                if answer.upper() in ['YES', 'Y', '1']:
                    d1mice = studyparams.ASTR_D1_CHR2_MICE
                else:
                    sys.exit()
            else:
                print('Subject found in database')
        else:
            # If no mice are specified, default to using all mice in the studyparams
            d1mice = studyparams.ASTR_D1_CHR2_MICE
            subjects = 'all'
        if len(arguments) == 2:
            tag = arguments[1]
        else:
            NO_TAG = 1
    else:
        d1mice = studyparams.ASTR_D1_CHR2_MICE
        subjects = 'all'
        NO_TAG = 1

if NO_TAG == 1:
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_clusters.h5'.format(subjects)) 
else:
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_clusters_{}.h5'.format(subjects, tag)) 

dir = os.path.dirname(outputDirectory)

if os.path.isdir(dir):
    print('Directory Exists')
else:
    print('\n FILENAME ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory))
    sys.exit()
                              
# ========================== Basic Database Creation ==========================
        
# Generates basic database, minimally selected for SSQ and ISI
db = celldatabase.generate_cell_database_from_subjects(d1mice)   

# ========================== Saving ==========================

try:
    celldatabase.save_hdf(db, outputDirectory)
except OSError:
    print("\n FILENAME ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}".format(outputDirectory))
else:
    print('\n SAVED DATAFRAME TO: \n {}'.format(outputDirectory))  