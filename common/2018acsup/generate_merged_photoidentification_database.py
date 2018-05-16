import sys
import os
import pandas as pd
import numpy as np

#subjects = ['band002', 'band003','band004','band005','band015','band016','band022','band023','band026','band027','band028','band029','band030','band031','band033','band034','band037','band038','band044','band045','band054','band059','band060']
subjects = ['band045', 'band054']

fulldb = pd.DataFrame()
for subject in subjects:
    db = pd.read_hdf('/home/jarauser/data/database/{}_clusters.h5'.format(subject),'database',index_col=0)
    fulldb = fulldb.append(db, ignore_index=True)
fulldb.to_hdf('/home/jarauser/data/database/photoidentification_cells.h5', 'database')