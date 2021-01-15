import sys
sys.path.append('..')
import os
import numpy as np
import pandas as pd
import studyparams
from scipy import stats
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
import database_generation_funcs as funcs


d1mice = studyparams.ASTR_D1_CHR2_MICE
# Where the finished database will be saved 
outputDirectory = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                               '{}_latencyTest.h5'.format(studyparams.DATABASE_NAME))
# File pathyway to basic database to be added to 
pathtoDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, 
                        '{}.h5'.format(studyparams.DATABASE_NAME))

# Loads basic database for testing
db = celldatabase.load_hdf(pathtoDB)  

db = db.query('latency * 0 == 0')

db = db.query('tuningResponseRatio > 0.35')
# db = db.query('tuningResponseRatio < 0.35')

db = db.query('tuningResponseRate > 0.1')
db = db.query('tuningResponseRate < 0.15')

db = db.query('bw10 * 0 == 0')
print(len(db))
celldatabase.save_hdf(db, outputDirectory)
print("SAVED DATAFRAME to {}".format(outputDirectory))