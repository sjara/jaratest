# -*- coding: utf-8 -*-
"""
Loads the basic database of clusters created with database_basic_generation.py, selects reliable 
cells that have data for sound reponse comparison, and calculates statistics using laserpulse
session data for D1 vs. nD1 determination.  

The database generated with this script is filtered by:
1. Presence of a laserpulse session
2. Presense of either a tuning curve or AM session
3. Manual selection (specified in `cell_indices_manually_removed.txt`, found in `extras`.)
4. ISI violations (threshold specified in studyparams.py)
5. Spike shape quality (threshold specified in studyparams.py)

This script calculates statistics used for:
1. D1 vs. nD1 selection

When run without arguments, this script will use all animals and store in a default database. This 
script can also be run using arguments to specify a specfic basic database that has been generated. 
The two arguments are "SUBJECT" and "TAG".

Run as (if not using tag)
`database_select_reliable_cells.py` or `database_select_reliable_cells.py SUBJECT`

Run as (if using tag)
`database_select_reliable_cells.py SUBJECT TAG`

The file `studyparams.py` contains a list of animals as well as statistical parameters for the 
database calculations. Database scripts use functions from the moddule 
`database_generation_funcs.py`.
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
        elif arguments[0].upper() == 'TEST':
            subjects = studyparams.SINGLE_MOUSE[0]
        elif isinstance(arguments[0], str):
            subjects = arguments[0]
            if subjects not in studyparams.ASTR_D1_CHR2_MICE:
                sys.exit('\n SUBJECT ERROR, DATAFRAME COULD NOT BE LOADED')
    else:
        subjects = 'all'
        print('No arguments given, default database with all animals will be used')
else:
    subjects = 'all'
    print("database_select_reliable_cells.py being ran as module, default database with all animals will be used")

if TAG == 1:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                  'astrpi_{}_clusters_{}.h5'.format(subjects, tag))
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                   'astrpi_{}_cells_{}.h5'.format(subjects, tag))
else:
    inputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                  'astrpi_{}_clusters.h5'.format(subjects)) 
    outputDirectory = os.path.join(settings.DATABASE_PATH, studyparams.STUDY_NAME, 
                                   'astrpi_{}_cells.h5'.format(subjects)) 
    
dir = os.path.dirname(outputDirectory)

# Checks if file path exists
if os.path.isdir(dir):
    print('Directory Exists')
else:
    sys.exit('\n DIRECTORY ERROR, DATAFRAME COULD NOT BE SAVED TO: \n {}'.format(outputDirectory)) 
    
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

MANUAL_ERROR = 0 # Automatically set to 1 if error in manual selection text document

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
db = db.query(studyparams.CELL_FILTER)

# ========================== Laserpulse Statistics Calculation ==========================

# Iterates through each cell in the database       
for indIter, (indRow, dbRow) in enumerate(db.iterrows()):
    oneCell = ephyscore.Cell(dbRow, useModifiedClusters=False)
    
    # Progress message 
    print("Processing cell {} \n {}, {}, depth = {} tetrode {}, cluster {}".format(indRow, 
          dbRow['subject'], dbRow['date'], dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))
    
    # Loads laserpulse session data for cell
    pulseEphysData, noBData = oneCell.load('laserpulse')
    
    baseRange100 = [-0.1, 0] # Time used for baseline spike counts.
    baseRange50 = [-0.05, 0]
    baseRange200 = [-0.2,0]
    
    # Creates arrays of times stimulus presented
    laserEventOnsetTimes = pulseEphysData['events']['laserOn']
    laserSpikeTimes = pulseEphysData['spikeTimes']
    
    # Calculates firing rate during baseline and response periods of various periods
    nspkBaseLaser100, nspkRespLaser100 = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange100)
       
    nspkBaseLaser50, nspkRespLaser50 = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange50)
        
    nspkBaseLaser200, nspkRespLaser200 = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange200)
    
    # Calculates mean firing rate for baseline and response periods 
    nspkRespLaserMean100 = np.mean(nspkRespLaser100)
    nspkBaseLaserMean100 = np.mean(nspkBaseLaser100)
    
    nspkRespLaserMean50 = np.mean(nspkRespLaser50)
    nspkBaseLaserMean50 = np.mean(nspkBaseLaser50)
    
    nspkRespLaserMean200 = np.mean(nspkRespLaser200)
    nspkBaseLaserMean200 = np.mean(nspkBaseLaser200)
    
    # Calculates change in firing rate during laserpulse
    frChange100 = nspkRespLaserMean100 - nspkBaseLaserMean100
    
    frChange50 = nspkRespLaserMean50 - nspkBaseLaserMean50
    
    frChange200 = nspkRespLaserMean200 - nspkBaseLaserMean200
        
    # Significance calculations for the laserpulse
    try:
        zStats100, pVals100 = stats.mannwhitneyu(nspkRespLaser100, nspkBaseLaser100, 
                                           alternative='two-sided')
    except ValueError:  # If all numbers are identical, mann-whitney test will fail
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats100, pVals100 = [0, 1]
    
    try:
        zStats50, pVals50 = stats.mannwhitneyu(nspkRespLaser50, nspkBaseLaser50, 
                                           alternative='two-sided')
    except ValueError:
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats50, pVals50 = [0, 1]
        
    try:
        zStats200, pVals200 = stats.mannwhitneyu(nspkRespLaser200, nspkBaseLaser200, 
                                           alternative='two-sided')
    except ValueError:
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats200, pVals200 = [0, 1]
    
    # Adds laserpulse columns to database
    db.at[indRow, 'laserpulseBaselineSpikeCount100'] = nspkBaseLaserMean100
    db.at[indRow, 'laserpulseResponseSpikeCount100'] = nspkRespLaserMean100 
    db.at[indRow, 'laserpulseSpikeCountChange100'] = frChange100
    db.at[indRow, 'laserpulsePval100'] = pVals100  # p-value from Mann-Whitney U test
    db.at[indRow, 'laserpulseZstat100'] = zStats100  # U-statistic from Mann-Whitney U test
    
    db.at[indRow, 'laserpulseBaselineSpikeCount50'] = nspkBaseLaserMean50  
    db.at[indRow, 'laserpulseResponseSpikeCount50'] = nspkRespLaserMean50
    db.at[indRow, 'laserpulseSpikeCountChange50'] = frChange50
    db.at[indRow, 'laserpulsePval50'] = pVals50
    db.at[indRow, 'laserpulseZstat50'] = zStats50
    
    db.at[indRow, 'laserpulseBaselineSpikeCount200'] = nspkBaseLaserMean200
    db.at[indRow, 'laserpulseResponseSpikeCount200'] = nspkRespLaserMean200
    db.at[indRow, 'laserpulseSpikeCountChange200'] = frChange200
    db.at[indRow, 'laserpulsePval200'] = pVals200
    db.at[indRow, 'laserpulseZstat200'] = zStats200
          
# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("\n SAVED DATAFRAME TO: \n {}".format(outputDirectory))  
if MANUAL_ERROR:
    print('An error occured, database may be incomplete or have erroneous data')   