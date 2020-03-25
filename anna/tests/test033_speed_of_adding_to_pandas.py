import numpy as np

from jaratoolbox import ephyscore
from jaratoolbox import celldatabase


db = celldatabase.load_hdf('/tmp/inactivation_cells.h5')
import time

ticTime = time.time()
anArray = np.empty(len(db))
for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    
    try:
        laserEphysData, noBehav = cellObj.load('lasernoisebursts')
    except IndexError:
        pass
    
    anArray[indRow] = 0
db['trash'] = anArray
     
print 'Elapsed Time: ' + str(time.time()-ticTime)

ticTime = time.time()

for indRow, (dbIndex, dbRow) in enumerate(db.iterrows()):
    cellObj = ephyscore.Cell(dbRow)
    
    try:
        laserEphysData, noBehav = cellObj.load('lasernoisebursts')
    except IndexError:
        pass
    
    db.at[dbIndex, 'trash2'] = 0

print 'Elapsed Time: ' + str(time.time()-ticTime)