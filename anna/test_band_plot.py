import pandas as pd
import bandwidths_analysis_v2 as bandan
reload(bandan)
from jaratest.nick.database import dataplotter
reload(dataplotter)

db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv')
cellStats = []
cellStats.append([])
cellStats.append([])
cellStats.append([])
for indCell, cell in db.iterrows():
    print indCell
    suppressionStats, atBestFreq, laserResponse = bandan.suppression_stats(cell)
    if suppressionStats is not None:
        cellStats[0].append(suppressionStats)
        cellStats[1].append(atBestFreq)
        cellStats[2].append(laserResponse)


