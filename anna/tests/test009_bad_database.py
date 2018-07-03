import pandas as pd
import numpy as np

from jaratoolbox import celldatabase



db = pd.DataFrame()
rand = np.random.random(100)

goodColumn = []
stupidColumn = []

for num in rand:
    if num > 0.5:
        goodColumn.append(np.array([0.0,1.0]))
        stupidColumn.append([0.0,1.0])
    else:
        goodColumn.append(np.full(2, np.nan))
        stupidColumn.append([np.nan, np.nan])
        
db['goodColumn'] = goodColumn
db['stupidColumn'] = stupidColumn
        
celldatabase.save_hdf(db, '/tmp/test_db.h5')

loadDB = celldatabase.load_hdf('/tmp/test_db.h5')

