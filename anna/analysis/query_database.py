import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import spikesorting
reload(spikesorting)
reload(celldatabase)
import bandwidths_analysis_v2 as bandan
reload(bandan)

#CELL LOCS:
# 20: suppressed cell
# 131: first contextual mod cell
# 141: second contextual mod cell

db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
bestCells = db.query("isiViolations<0.02 and clusterQuality>2 and atBestFreq==1 and subject=='band025'")
cell = bestCells.loc[141]
bestBand, atBestFreq, bestFreq = bandan.best_band_index(cell)
bandan.plot_laser_bandwidth_summary(cell, bestBand)