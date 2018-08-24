'''
This module contains generic database generation funcitons that may eventually be implemented in jaratoolbox.
'''

import os
import pandas as pd

from jaratoolbox import celldatabase
from jaratoolbox import settings


def generic_database(subjects):
    '''
    This function takes as argument the a list of the animals to process and outputs 
    a generic database containing all clusters
    '''
    fulldb = pd.DataFrame()
    for subject in subjects:
        inforec = os.path.join(settings.INFOREC_PATH,'{0}_inforec.py'.format(subject))
        db = celldatabase.generate_cell_database(inforec)               
        # --- Keep only good cells ---
        db = db[(db['isiViolations'] < 0.05) | (db['spikeShapeQuality'] > 2)]
        fulldb = fulldb.append(db, ignore_index=True)
    return fulldb
