import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from jaratoolbox import loadopenephys
from jaratoolbox import settings
import bandwidths_analysis_v2

SAMPLING_RATE=30000.0

db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band016_celldb.csv')


cells = db[db['isiViolations']<2.0]
cells = cells[db['nSpikes']>2000]

for indCell, cell in cells.iterrows():
    bandwidths_analysis_v2.plot_bandwidth_report(cell)