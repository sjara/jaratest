import os
import shutil

allThalLaserCellsDir = '/home/nick/data/reports/nick/20180326_ALL_2018thstr_LASER_CELLS/rightThal'
allACLaserCellsDir = '/home/nick/data/reports/nick/20180326_ALL_2018thstr_LASER_CELLS/rightAC'

goodThalCellsDir = '/home/nick/Desktop/2018thstr_goodThalCells_20180326'
goodThalCells = os.listdir(goodThalCellsDir)
goodACCellsDir = '/home/nick/Desktop/2018thstr_goodACcells_20180326'

badThalCellsDir = '/home/nick/Desktop/2018thstr_badThalCells_20180327'
if not os.path.exists(badThalCellsDir):
    os.mkdir(badThalCellsDir)
for report in os.listdir(allThalLaserCellsDir):
    if report not in os.listdir(goodThalCellsDir):
        reportFullFn = os.path.join(allThalLaserCellsDir, report)
        newFn = os.path.join(badThalCellsDir, report)
        shutil.copyfile(reportFullFn, newFn)

badACCellsDir = '/home/nick/Desktop/2018thstr_badACcells_20180327'
if not os.path.exists(badACCellsDir):
    os.mkdir(badACCellsDir)
for report in os.listdir(allACLaserCellsDir):
    if report not in os.listdir(goodACCellsDir):
        reportFullFn = os.path.join(allACLaserCellsDir, report)
        newFn = os.path.join(badACCellsDir, report)
        shutil.copyfile(reportFullFn, newFn)
