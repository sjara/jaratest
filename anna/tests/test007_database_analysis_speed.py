from jaratoolbox import ephyscore
from jaratoolbox import celldatabase


db = celldatabase.load_hdf('/home/jarauser/data/database/inactivation_cells2.h5')
import time

ticTime = time.time()
for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    try:
        laserEphysData, noBehav = cellObj.load('laserPulse')
    except IndexError:
        pass
    try:
        bandEphysData, bandBehavData = cellObj.load('bandwidth')
    except IndexError:
        pass
        
print 'Elapsed Time: ' + str(time.time()-ticTime)

ticTime = time.time()

for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    try:
        laserEphysData, noBehav = cellObj.load('laserPulse')
    except IndexError:
        pass
        
for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    try:
        bandEphysData, bandBehavData = cellObj.load('bandwidth')
    except IndexError:
        pass

print 'Elapsed Time: ' + str(time.time()-ticTime)
