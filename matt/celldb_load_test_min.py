from jaratoolbox import celldatabase
import pandas as pd

dbPath = '/var/tmp/test_db_load.h5'
load = 1
save = 0

if save:
    data = {'Names': ['band001', 'd1pi033'],
            }

    db = pd.DataFrame(data)
    celldatabase.save_hdf(db, dbPath)
    print('saved db')

if load:
    db = celldatabase.load_hdf(dbPath)
    print('loaded db')
