# -*- coding: utf-8 -*-
"""
Loads the basic database of clusters created with database_basic_generation.py, selects reliable 
cells that have data for sound reponse comparison, and calculated statistics using laserpulse
session data for D1 vs. nD1 determination.  

The database generated with this script is filtered by:
1. Presence of laserpulse session
2. Presense of either tuning curve or AM session
3. Manual selection
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
import numpy as np
from scipy import stats
import studyparams
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
import database_generation_funcs as funcs

# ========================== Run Mode ==========================

MANUAL_ERROR = 0 # Automatically set to 1 if error in manual selection text document
NO_TAG = 0 # Automatically set to 1 if no tag given

# Determining animals used and file name by arguements given
if __name__ == "__main__":
    if sys.argv[1:] != []: # Checks if there are any arguments after the script name 
        arguments = sys.argv[1:] # Script parameters 
        if arguments[0] == "all":
            d1mice = studyparams.ASTR_D1_CHR2_MICE
            subjects = 'all'
        elif arguments[0].upper() == 'TEST':
            d1mice = studyparams.SINGLE_MOUSE
            subjects = studyparams.SINGLE_MOUSE[0]
        elif isinstance(arguments[0], str):
            d1mice = []
            subjects = arguments[0]
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
    print('Directory exists')
else:
    sys.exit('\n TAG ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory))
    
# ========================== Database Filtering ==========================

print('Loading basic database...')

# Loads basic database
try:
    db = celldatabase.load_hdf(inputDirectory) 
except OSError:
    sys.exit('\n DATABASE ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory))

# Selects cells with a laserpulse session for D1 vs. nD1 determination
db = db[db['sessionType'].apply(lambda s: 'laserpulse' in s)]    

# Selects cells with either tuning curve or AM session for sound comparison
db = db[db['sessionType'].apply(lambda s: ('tuningCurve' in s) or ('am' in s))]

# Empty list to fill with manually-removed cells
indicesRemovedCells = []

# Generates list of clusters from a text document to be removed by manual selection
with open('extras\cell_indices_manually_removed.txt', 'r') as manualSelection:
    for line in manualSelection:
        line = line.rstrip()
        try:
            indicesRemovedCells.append(int(line))
        except ValueError:
            print('\'{}\' not valid cell index'.format(line))
            MANUAL_ERROR = 1

# Removes clusters that were not manually-verfied
db = db.drop(indicesRemovedCells, errors='ignore')

# ========================== Laserpulse Statistics Calculation ==========================

# Iterates through each cell in the database       
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)
    
    # Progress message 
    print("Processing cell {} \n {}, {}, depth = {} tetrode {}, cluster {}".format(indRow, 
          dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
    
    # Loads laserpulse session data for cell
    pulseEphysData, noBData = oneCell.load('laserpulse')
    
    baseRange = [-0.1, 0] # Time used for baseline spike counts.
    
    # Creates arrays of times stimulus presented
    laserEventOnsetTimes = pulseEphysData['events']['laserOn']
    laserSpikeTimes = pulseEphysData['spikeTimes']
    
    # Calculates firing rate during baseline and response periods 
    nspkBaseLaser, nspkRespLaser = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange)
    
    # Calculates mean firing rate for baseline and response periods 
    nspkRespLaserMean = np.mean(nspkRespLaser)
    nspkBaseLaserMean = np.mean(nspkBaseLaser)
    
    # Calculates change in firing rate during laserpulse
    spikeCountChange = nspkRespLaserMean - nspkBaseLaserMean
        
    # Significance calculations for the laserpulse
    try:
        zStats, pVals = stats.mannwhitneyu(nspkRespLaser, nspkBaseLaser, 
                                           alternative='two-sided')
    except ValueError:  # All numbers identical will cause mann-whitney to fail
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats, pVals = [0, 1]
    
    # Adds laserpulse information to database
    db.at[indRow, 'laserpulsePval'] = pVals  # p-value from Mann-Whitney U test
    db.at[indRow, 'laserpulseZstat'] = zStats  # U-statistic from Mann-Whitney U test
    # Difference between base and response firing rate
    db.at[indRow, 'laserpulseSpikeCountChange'] = spikeCountChange
    db.at[indRow, 'laserpulseBaselineSpikeCount'] = nspkBaseLaserMean  # Mean of baseline FR
    db.at[indRow, 'laserpulseResponseSpikeCount'] = nspkRespLaserMean  # Mean of response FR
        
# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("\n SAVED DATAFRAME TO: \n {}".format(outputDirectory))  
if MANUAL_ERROR:
    print('An error occured, database may be incomplete or have erroneous data')   