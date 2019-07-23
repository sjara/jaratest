import os
import shutil
import pandas as pd
from jaratoolbox import celldatabase

dbPath = '/mnt/jarahubdata/figuresdata/2018thstr/celldatabase.h5'
db = pd.read_hdf(dbPath, key='dataframe')

allCellsDir = '/home/nick/Desktop/20180328_2018thstr_analysis/20180328_goodCells'
thalDir = '/home/nick/Desktop/20180328_2018thstr_analysis/20180328_thalGoodCells'
acDir = '/home/nick/Desktop/20180328_2018thstr_analysis/20180328_acGoodCells'

os.mkdir(thalDir)
os.mkdir(acDir)

for report in os.listdir(allCellsDir):
    (subject, date, depth, tetrodeCluster) = report.split('_')
    depth = float(depth)
    tetrode = int(tetrodeCluster[2])
    cluster = int(tetrodeCluster[4:])

    index, dbRow = celldatabase.find_cell(db, subject, date, depth, tetrode, cluster)
    sourceFn = os.path.join(allCellsDir, report)
    if dbRow['brainArea']=='rightThal':
        destFn = os.path.join(thalDir, report)
    elif dbRow['brainArea']=='rightAC':
        destFn = os.path.join(acDir, report)
    else:
        raise ValueError("Report {} not AC or Thal??".format(report))
    shutil.copy(sourceFn, destFn)
