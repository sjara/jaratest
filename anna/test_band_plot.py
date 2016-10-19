import pandas as pd
from jaratest.anna import bandwidths_analysis
reload(bandwidths_analysis)
from jaratest.nick.database import dataplotter
reload(dataplotter)

SAMPLING_RATE=30000.0
COND = 0

if COND==0:
    CELL_NUM = 807
    db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band004_celldb.csv')
elif COND==1:
    CELL_NUM = 270
    db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band002_celldb.csv')
elif COND==2:
    CELL_NUM = 348
    db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band003_celldb.csv')
cell = db.loc[CELL_NUM]
bandwidths_analysis.plot_bandwidth_report(cell)