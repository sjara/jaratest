# -*- coding: utf-8 -*-
'''
This script creates a basic database from an inforec file using 
celldatabase.generate_cell_database_from_subjects(). Further analysis can be done with other 
database_.py scripts. 

The database generated with this script is filtered by:
1. ISI violations (threshold specified in celldatabase.generate_cell_database_from_subjects)
2. Spike shape quality (threshold specified in celldatabase.generate_cell_database_from_subjects)

When run without arguments, this script will use all animals and store in a default database. This 
script can also be run using arguments. The two arguments are "SUBJECT" and "TAG".

SUBJECT can be a single animal (example - `d1pi043`), `all`, or `test`. `all` will use all of the 
subjects listed in studyparams.py. `test` will use the test subject listed in studyparams.py. If 
nothing is specified, all subjects will be used. 

Optionally you can set a TAG on the database (using filename acceptable characters). You must enter 
a subject parameter before entering a tag. The tag will appear at the end of the database filename.

Run as (if not using tag)
`database_basic_generation.py` or `database_basic_generation.py SUBJECT`

Run as (if using tag)
`database_basic_generation.py SUBJECT TAG`

The file `studyparams.py` contains a list of animals as well as statistical parameters for the 
database calculations. Database scripts use functions from the moddule 
`database_generation_funcs.py`.
'''
import sys
import os
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings

# ========================== Run Mode ==========================

TAG = 0 # Automatically set to 1 if tag given

# Determining animals used and file name by arguments given
if __name__ == '__main__':
    if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
        arguments = sys.argv[1:] # Script parameters 
        if len(arguments) == 2:
                tag = arguments[1]
                TAG = 1
        if arguments[0].upper() in 'ALL':
            subjects = 'all'
            d1mice = studyparams.ASTR_D1_CHR2_MICE
        elif arguments[0].upper() == 'TEST':
            subjects = studyparams.SINGLE_MOUSE[0]
            d1mice = studyparams.SINGLE_MOUSE
        elif isinstance(arguments[0], str):
            subjects = arguments[0]
            d1mice = []
            d1mice.append(subjects)
            if d1mice[0] not in studyparams.ASTR_D1_CHR2_MICE:
                answer = input('Subject could not be found, Would you like to run for all animals?')
                if answer.upper() in ['YES', 'Y', '1']:
                    subjects = 'all'
                    d1mice = studyparams.ASTR_D1_CHR2_MICE
                else:
                    sys.exit('\n No database will be saved')
            else:
                print('Subject found in database')
        else:
            sys.exit('\n SUBJECT ERROR, DATAFRAME COULD NOT BE SAVED')
    else:
        subjects = 'all'
        d1mice = studyparams.ASTR_D1_CHR2_MICE
        print('No arguments given, all animals will be used')
else:
    subjects = 'all'
    d1mice = studyparams.ASTR_D1_CHR2_MICE
    print("database_basic_generation.py being ran as module, all animals will be used")

if TAG == 1:
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                           'astrpi_{}_clusters_{}.h5'.format(subjects, tag)) 
else:
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_clusters.h5'.format(subjects)) 
    
dir = os.path.dirname(outputDirectory)

# Checks if file path exists
if os.path.isdir(dir):
    print('Directory Exists')
else:
    sys.exit('\n DIRECTORY ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory))
                              
# ========================== Basic Database Creation ==========================
        
# Generates basic database, minimally selected for SSQ and ISI
db = celldatabase.generate_cell_database_from_subjects(d1mice)   

# ========================== Saving ==========================

try:
    celldatabase.save_hdf(db, outputDirectory)
except OSError:
    print('\n FILENAME ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory))
else:
    print('\n SAVED DATAFRAME TO: \n {}'.format(outputDirectory))  