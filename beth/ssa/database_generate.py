'''
CLUSTER FIRST!!!

Generate and save database with calculated stats and parameters that will be used in analysis
'''
import os
import sys
import pandas as pd
import numpy as np
import time
import studyparams
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
#import database_generation_funcs as funcs
#reload(funcs)
reload(settings)
reload(studyparams)

'''
MODIFY THIS CODE to fit your study.
'''

def calculate_base_stats(db):
    return db

def calculate_indices(db):
    return db

def calculate_cell_locations(db): # to be filled after complete collecting histology data
    pass


if __name__ == "__main__":

    SAVE = 1  # 1: Save database

    # -- Cluster your data --
    CLUSTER_DATA = 0  # We don't generally run this code. We kept this for documentation
    miceList = studyparams.MICE_LIST
    if CLUSTER_DATA: #SPIKE SORTING
        inforecFile = os.path.join(settings.INFOREC_PATH,'{}_inforec.py'.format(d1mice))
        clusteringObj = spikesorting.ClusterInforec(inforecFile)
        clusteringObj.process_all_experiments()
        pass

    # -- Generate_cell_database_filters cells with the followings: isi < 0.05, spike quality > 2 --
    basicDB = celldatabase.generate_cell_database_from_subjects(miceList)

    # Computing first the base stats and then the indices
    firstDB = calculate_base_stats(basicDB)

    if SAVE:
        dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
        dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))
        if os.path.isdir(dbPath):
            celldatabase.save_hdf(firstDB, dbFilename)
            print('Saved database to {}'.format(dbFilename))
        else:
            print('{} does not exist. Please create this folder.'.format(dbPath))
