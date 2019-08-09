"""
Generate and save database containing basic information, stats, and indices for each cell.
"""

import os
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import spikesorting
from jaratoolbox import settings
import database_generation_funcs as funcs
import studyparams


def calculate_base_stats(db):
    return db


def calculate_indices(db):
    return db


def calculate_cell_locations(db):
    pass


if __name__ == "__main__":

    # -- Spike sort the data (code is left here for reference) --
    '''
    subject = 'testXXX'
    inforecFile = os.path.join(settings.INFOREC_PATH,'{}_inforec.py'.format(subject))
    clusteringObj = spikesorting.ClusterInforec(inforecFile)
    clusteringObj.process_all_experiments()
    '''
    
    # -- Generate cell database (this function excludes clusters with isi>0.05, spikeQuality<2 --
    celldb = celldatabase.generate_cell_database_from_subjects(studyparams.MICE_LIST)

    # -- Compute the base stats and indices for each cell --
    celldb = calculate_base_stats(celldb)  # Calculated for all cells
    celldb = calculate_indices(celldb)     # Calculated for a selected subset of cells

    dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
    dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
    if os.path.isdir(dbPath):
        celldatabase.save_hdf(celldb, dbFilename)
        print('Saved database to {}'.format(dbFilename))
    else:
        print('{} does not exist. Please create this folder.'.format(dbPath))
