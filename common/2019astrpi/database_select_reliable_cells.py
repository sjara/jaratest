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
    baseRange50 = [-0.05, 0]
    baseRange200 = [-0.2,0]
    
    # Creates arrays of times stimulus presented
    laserEventOnsetTimes = pulseEphysData['events']['laserOn']
    laserSpikeTimes = pulseEphysData['spikeTimes']
    
    # Calculates firing rate during baseline and response periods of various periods, specified above
    nspkBaseLaser, nspkRespLaser = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange)
       
    nspkBaseLaser50, nspkRespLaser50 = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange50)
        
    nspkBaseLaser200, nspkRespLaser200 = funcs.calculate_spike_count(laserEventOnsetTimes, 
                                                               laserSpikeTimes, baseRange200)
    
    # Calculates mean firing rate for baseline and response periods 
    nspkRespLaserMean = np.mean(nspkRespLaser)
    nspkBaseLaserMean = np.mean(nspkBaseLaser)
    
    nspkRespLaserMean50 = np.mean(nspkRespLaser50)
    nspkBaseLaserMean50 = np.mean(nspkBaseLaser50)
    
    nspkRespLaserMean200 = np.mean(nspkRespLaser200)
    nspkBaseLaserMean200 = np.mean(nspkBaseLaser200)
    
    # Calculates change in firing rate during laserpulse
    frChange = nspkRespLaserMean - nspkBaseLaserMean
    
    frChange50 = nspkRespLaserMean50 - nspkBaseLaserMean50
    
    frChange200 = nspkRespLaserMean200 - nspkBaseLaserMean200
        
    # Significance calculations for the laserpulse
    try:
        zStats, pVals = stats.mannwhitneyu(nspkRespLaser, nspkBaseLaser, 
                                           alternative='two-sided')
    except ValueError:  # All numbers identical will cause mann-whitney to fail
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats, pVals = [0, 1]
    
    try:
        zStats50, pVals50 = stats.mannwhitneyu(nspkRespLaser50, nspkBaseLaser50, 
                                           alternative='two-sided')
    except ValueError:  # All numbers identical will cause mann-whitney to fail
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats50, pVals50 = [0, 1]
        
    try:
        zStats200, pVals200 = stats.mannwhitneyu(nspkRespLaser200, nspkBaseLaser200, 
                                           alternative='two-sided')
    except ValueError:  # All numbers identical will cause mann-whitney to fail
        print("laserpulse mann-whitney fail for {}".format(oneCell))
        zStats200, pVals200 = [0, 1]
    
    # Adds laserpulse columns to database
    db.at[indRow, 'laserpulseBaselineFR'] = nspkBaseLaserMean
    db.at[indRow, 'laserpulseResponseFR'] = nspkRespLaserMean  
    db.at[indRow, 'laserpulseFRChange'] = frChange
    db.at[indRow, 'laserpulsePval'] = pVals  # p-value from Mann-Whitney U test
    db.at[indRow, 'laserpulseZstat'] = zStats  # U-statistic from Mann-Whitney U test
    
    db.at[indRow, 'laserpulseBaselineFR50'] = nspkBaseLaserMean50  
    db.at[indRow, 'laserpulseResponseFR50'] = nspkRespLaserMean50
    db.at[indRow, 'laserpulseFRChange50'] = frChange50
    db.at[indRow, 'laserpulsePval50'] = pVals50  # p-value from Mann-Whitney U test
    db.at[indRow, 'laserpulseZstat50'] = zStats50  # U-statistic from Mann-Whitney U test
    
    db.at[indRow, 'laserpulseBaselineFR200'] = nspkBaseLaserMean200
    db.at[indRow, 'laserpulseResponseFR200'] = nspkRespLaserMean200
    db.at[indRow, 'laserpulseFRChange200'] = frChange200
    db.at[indRow, 'laserpulsePval200'] = pVals200  # p-value from Mann-Whitney U test
    db.at[indRow, 'laserpulseZstat200'] = zStats200  # U-statistic from Mann-Whitney U test
        
# ========================== Saving ==========================

celldatabase.save_hdf(db, outputDirectory)
print("\n SAVED DATAFRAME TO: \n {}".format(outputDirectory))  
if MANUAL_ERROR:
    print('An error occured, database may be incomplete or have erroneous data')   