"""
Create a folder with a subset of reports given a database.
"""

import os
import sys
import shutil
import glob
from jaratoolbox import celldatabase
from jaratoolbox import settings
sys.path.append('..')
import studyparams

import imp
imp.reload(celldatabase)

outputDir = 'tempdb_nD1'
#outputDir = 'tempdb_subset_good'
nameDB = 'tempdb_subset_good.h5'
origDir = '/data/reports/2019astrpi/reports_all_cells_in_db'
#outputPath = '/data/reports/2019astrpi/reports_{}'.format(os.path.splitext(nameDB)[0])
outputPath = f'/data/reports/2019astrpi/reports_{outputDir}'

if not os.path.isdir(outputPath):
    os.mkdir(outputPath)
    print(f'Created {outputPath}')
    
pathToDB = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, nameDB)
columnsToLoad = ['index', 'spikeShape', 'laserpulse_pVal', 'laserpulse_SpikeCountChange',
                 'laserpulse_responseSpikeCount']
print(f'Loading {pathToDB}...')
cellDB = celldatabase.load_hdf(pathToDB, columns=columnsToLoad)
print('Done')

if 1:
    cellDB = cellDB.query(studyparams.nD1_CELLS)

for indc in cellDB.index:
    origFile = glob.glob(os.path.join(origDir,f'cell{indc:04d}_*'))[0]
    print(origFile)
    shutil.copy2(origFile, outputPath)

