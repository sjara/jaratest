'''
This script runs everything needed to create the two databases required for this study (photoidentified and inactivated cells).

Can specify which database to generate with user input (0: photoID database, 1: inactivation database).
No user input will result in both being generated.
'''
import os
import sys
import numpy as np

from jaratoolbox import celldatabase
from jaratoolbox import settings

import cluster_ephys_data
import database_photoidentification
reload(database_photoidentification)
import database_inactivation
reload(database_inactivation)
import studyparams
import figparams

# -- select which database to generate --
args = sys.argv[1:]
if len(args):
    dbsToGenerate = np.zeros(2)
    indsToGenerate = [int(x) for x in args]
    dbsToGenerate[indsToGenerate] = 1
else:
    print("Please select a database to generate (0: photoID, 1: inactivation)")

if dbsToGenerate[0]: 
    # cluster your data
    chr2mice = studyparams.PV_CHR2_MICE + studyparams.SOM_CHR2_MICE
    cluster_ephys_data.cluster_spike_data(chr2mice)
    
    # creates a basic database and performs cluster rescue
    basicDB = celldatabase.generate_cell_database_from_subjects(chr2mice)
    basicDB = cluster_ephys_data.cluster_rescue(basicDB, isiThreshold=studyparams.ISI_THRESHOLD)
    
    # creates and saves a database for photoidentified cells, computing first the base stats and then the indices
    photoDBFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME,'photoidentification_cells.h5')
    photoIDDB = database_photoidentification.photoID_base_stats(basicDB, filename = photoDBFilename)
    photoIDDB = database_photoidentification.photoID_indices(basicDB, filename = photoDBFilename)
 
if dbsToGenerate[1]:
    # cluster your data
    archTmice = studyparams.PV_ARCHT_MICE + studyparams.SOM_ARCHT_MICE
    cluster_ephys_data.cluster_spike_data(archTmice)
    
    # creates and saves a database for inactivation
    inactivationDBFilename = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME,'inactivation_cells.h5')
    basicDB = celldatabase.generate_cell_database_from_subjects(archTmice)
    inactivationDB = database_inactivation.inactivation_database(basicDB, baseStats = True, computeIndices = True, filename = inactivationDBFilename)
