import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from jaratoolbox import loadopenephys
from jaratoolbox import settings
import bandwidths_analysis_v2 as bandan

SAMPLING_RATE=30000.0
subjects = ['band002', 'band003', 'band004', 'band005']
db = pd.DataFrame()

for subject in subjects:
    db = db.append(pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/'+subject+'_celldb.csv',index_col=0),ignore_index=True)

cells = db[db['isiViolations']<2.0]
cells = cells[db['nSpikes']>2000]

for indCell, cell in cells.iterrows():
    bandan.suppression_stats(cell)

cells.to_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv')