'''
This script produces 

TO DO:
- Make sure inforec files get reloaded (by celldatabase.py)
'''

from jaratoolbox import settings

import database_generic
reload(database_generic)
import database_photoidentification
reload(database_photoidentification)
import database_inactivation
reload(database_inactivation)
import subjects_info
reload(subjects_info)

 
# # creates and saves a database for photoidentified cells
# chr2mice = subjects_info.PV_CHR2_MICE + subjects_info.SOM_CHR2_MICE
# basicDB = database_generic.generic_database(chr2mice)
# database_photoidentification.photoIDdatabase(basicDB, clusterRescue = True, baseStats = True, computeIndices = True)
# 
# # creates and saves a database for inactivation
# archTmice = subjects_info.PV_ARCHT_MICE + subjects_info.SOM_ARCHT_MICE
# basicDB = database_generic.generic_database(archTmice)
# database_inactivation.inactivation_database(basicDB, baseStats = True, computeIndices = True)

#database_photoidentification.photoIDdatabase('/home/jarauser/data/database/photoidentification_cells.h5', clusterRescue = False, baseStats = False, computeIndices = True)
database_inactivation.inactivation_database('/home/jarauser/data/database/inactivation_cells.h5', baseStats = False, computeIndices = True)

# # test on some extra mice I recorded 
# mice = ['band073']
# basicDB = database_generic.generic_database(mice)
# database_inactivation.inactivation_database(basicDB, baseStats = True, computeIndices = True, filename='band073_cells.h5')
