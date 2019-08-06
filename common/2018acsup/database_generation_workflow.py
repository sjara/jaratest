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
from jaratoolbox import spikesorting

import database_photoidentification
import database_inactivation
import database_cell_locations
import studyparams

# -- functions assisting in clustering and cluster rescue --
def cluster_spike_data(subjects):
    for subject in subjects:
        inforecPath = os.path.join(settings.INFOREC_PATH,'{0}_inforec.py'.format(subject))
        ci = spikesorting.ClusterInforec(inforecPath)
        ci.process_all_experiments()
        
def cluster_rescue(db, isiThreshold):
    modifiedDB = spikesorting.rescue_clusters(db, isiThreshold)
    return modifiedDB

# -- select which database to generate --
args = sys.argv[1:]
if len(args):
    dbsToGenerate = np.zeros(2)
    indsToGenerate = [int(x) for x in args]
    dbsToGenerate[indsToGenerate] = 1
else:
    print("Please select a database to generate (0: photoID, 1: inactivation)")

if dbsToGenerate[0]: 
    # -- cluster your data --
    chr2mice = studyparams.PV_CHR2_MICE + studyparams.SOM_CHR2_MICE
    #cluster_spike_data(chr2mice)
    
    # -- creates a basic database and performs cluster rescue --
    basicDB = celldatabase.generate_cell_database_from_subjects(chr2mice)
    basicDB = cluster_rescue(basicDB, isiThreshold=studyparams.ISI_THRESHOLD)
    
    # -- creates and saves a database for photoidentified cells, computing first the base stats and then the indices --
    photoDBFilename = '/tmp/photoidentification_cells.h5' # save database in a temporary place, move it when you're satisfied with it
    photoIDDB = database_photoidentification.photoID_base_stats(basicDB, filename = photoDBFilename)
    photoIDDB = database_photoidentification.photoID_indices(photoIDDB, filename = photoDBFilename)
    
    # -- finds the depths and locations of all cells with indices computed --
    # RUN THIS PART IN A VIRTUAL ENVIRONMENT
    photoIDDB = database_photoidentification.photoDB_cell_locations(photoIDDB, filename = photoDBFilename)
 
if dbsToGenerate[1]:
    # -- cluster your data --
    archTmice = studyparams.PV_ARCHT_MICE + studyparams.SOM_ARCHT_MICE
    #cluster_spike_data(archTmice)
    
    # -- creates and saves a database for inactivation --
    inactivationDBFilename = '/tmp/inactivation_cells.h5' # save database in a temporary place, move it when you're satisfied with it
    basicDB = celldatabase.generate_cell_database_from_subjects(archTmice)
    inactivationDB = database_inactivation.inactivation_base_stats(basicDB)
    inactivationDB = database_inactivation.inactivation_indices(inactivationDB)
    
    # -- locations of cells, RUN IN VIRTUAL ENVIRONMENT --
    inactivationDB = database_cell_locations.cell_locations(inactivationDB)
    
    # -- save the final database --
    celldatabase.save_hdf(inactivationDB, inactivationDBFilename)
    print inactivationDBFilename + " saved"
