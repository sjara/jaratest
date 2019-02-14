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

import database_photoidentification
reload(database_photoidentification)
import database_inactivation
reload(database_inactivation)
import subjects_info
reload(subjects_info)

# -- select which database to generate --
args = sys.argv[1:]
if len(args):
    dbsToGenerate = np.zeros(2)
    indsToGenerate = [int(x) for x in args]
    dbsToGenerate[indsToGenerate] = 1
else:
    dbsToGenerate = np.ones(2)

if dbsToGenerate[0]: 
    # creates and saves a database for photoidentified cells
    chr2mice = subjects_info.PV_CHR2_MICE + subjects_info.SOM_CHR2_MICE
    photoDBFilename = os.path.join(settings.DATABASE_PATH,'photoidentification_cells.py')
    basicDB = celldatabase.generate_cell_database_from_subjects(chr2mice)
    database_photoidentification.photoIDdatabase(basicDB, clusterRescue = True, baseStats = True, computeIndices = True, dbFilename = photoDBFilename)
 
if dbsToGenerate[1]:  
    # creates and saves a database for inactivation
    archTmice = subjects_info.PV_ARCHT_MICE + subjects_info.SOM_ARCHT_MICE
    inactivationDBFilename = os.path.join(settings.DATABASE_PATH,'inactivation_cells.py')
    basicDB = celldatabase.generate_cell_database_from_subjects(archTmice)
    database_inactivation.inactivation_database(basicDB, baseStats = True, computeIndices = True, dbFilename = inactivationDBFilename)
