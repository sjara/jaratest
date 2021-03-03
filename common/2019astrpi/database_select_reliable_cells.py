# -*- coding: utf-8 -*-
"""
This script loads the basic database of clusters created with database_basic_generation.py and 
selects reliable cells that have data for sound reponse comparison. 

The database generated with this script is filtered by:
1. Presence of laserpulse session
2. Presense of either tuning curve or AM session
3. Mnual selection
4. Further parameters specified in database_basic_generation.py

This script calculates statistics used for:
1. D1 vs. nD1 selection

Run as:
python3 database_select_reliable_cells.py SUBJECT TAG

A database must exist with these parameters or script will fail. If the database has not been 
previously filtered, 'clusters' will change to 'cells' in the filename. 
"""
import os
import sys
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
                print('\n SUBJECT ERROR, DATAFRAME COULD NOT BE SAVED \n')
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
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_clusters.h5'.format(subjects)) 
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_cells.h5'.format(subjects)) 
else:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_clusters_{}.h5'.format(subjects, tag))
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                               'astrpi_{}_cells_{}.h5'.format(subjects, tag)) 

dir = os.path.dirname(outputDirectory)

if os.path.isdir(dir):
    print('Directory Exists')
else:
    print('\n TAG ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory))
    sys.exit()
    
# ========================== Database Filtering ==========================

print('Loading basic database...')

# Loads basic database
if not NO_TAG:
    try:
        db = celldatabase.load_hdf(inputDirectory) 
    except OSError:
        sys.exit('\n DATABASE ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory)) 
else:
    try:
        db = celldatabase.load_hdf(inputDirectory) 
    except OSError:
        sys.exit('\n DATABASE ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory)) 

# Selects cells with a laserpulse session for D1 vs. nD1 determination
hasLP = db['sessionType'].apply(lambda s: 'laserpulse' in s)
db = db[hasLP]
    
# Selects cells with either tuning curve or AM session for sound comparison
hasTC_AM = db['sessionType'].apply(lambda s: ('tuningCurve' in s) or ('am' in s))
db = db[hasTC_AM]

# Empty list to fill with manually-removed cells
indicesRemovedCells = []

# Generates list of cells from a text document to be removed by manual selection
with open('extras\cell_indices_manually_removed.txt', 'r') as manualSelection:
    for line in manualSelection:
        line = line.rstrip()
        try:
            indicesRemovedCells.append(int(line))
        except ValueError:
            print('\'{}\' not valid cell index'.format(line))

# Removes clusters that were not manually-verfied
db = db.drop(indicesRemovedCells, errors='ignore')

# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("\n SAVED DATAFRAME TO: \n {}".format(outputDirectory))     