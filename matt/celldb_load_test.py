from jaratoolbox import celldatabase
import pandas as pd
import numpy as np

dbPath = '/var/tmp/test_db_load_new3.h5'
load = 1
save = 0
regions = np.array(['leftAC', 'rightAC'])
behavior1 = ['a', None, 'b']
behavior2 = ['a', 'b', None]
b1Arr = np.array(behavior1)
b2Arr = np.array(behavior2)
if save:
    data = {'Names': ['band001', 'd1pi033'],
            'Depths': [100.0, 3201.0],
            'regions': regions,
            'behaviors': [behavior1, behavior2],
            }

    db = pd.DataFrame(data)
    celldatabase.save_hdf(db, dbPath)
    print('saved db')

if load:
    db = celldatabase.load_hdf(dbPath)
    print('loaded db')