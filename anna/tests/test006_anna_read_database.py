import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import celldatabase

from jaratest.anna.analysis import band_plots
from scipy import stats

import subjects_info
reload(subjects_info)

db = celldatabase.load_hdf('/home/jarauser/data/database/inactivation_cells2.h5')

bestCells = db[db['sustainedSuppressionIndexLaser'].notnull()]
noPV = bestCells.loc[bestCells['subject'].isin(subjects_info.PV_ARCHT_MICE)]
noSOM = bestCells.loc[bestCells['subject'].isin(subjects_info.SOM_ARCHT_MICE)]

for indCell, cell in bestCells.iterrows():
    band_plots.plot_laser_bandwidth_summary(cell, bandIndex=int(cell['bestBandSession']))

PVsuppression = noPV['onsetSuppressionIndexNoLaser']
SOMsuppression = noSOM['onsetSuppressionIndexNoLaser']

PVsuppressionlaser = noPV['onsetSuppressionIndexLaser']
SOMsuppressionlaser = noSOM['onsetSuppressionIndexLaser']

plt.figure()
band_plots.plot_paired_scatter_with_median([PVsuppression,PVsuppressionlaser], ['No laser','Laser'], ylabel='Suppression Index', title='PV inactivation: onset')

plt.figure()
band_plots.plot_paired_scatter_with_median([SOMsuppression,SOMsuppressionlaser], ['No laser','Laser'], ylabel='Suppression Index', title='SOM inactivation: onset')

print stats.wilcoxon(PVsuppression, PVsuppressionlaser)
print stats.wilcoxon(SOMsuppression, SOMsuppressionlaser)

PVsuppression = noPV['sustainedSuppressionIndexNoLaser']
SOMsuppression = noSOM['sustainedSuppressionIndexNoLaser']

PVsuppressionlaser = noPV['sustainedSuppressionIndexLaser']
SOMsuppressionlaser = noSOM['sustainedSuppressionIndexLaser']

plt.figure()
band_plots.plot_paired_scatter_with_median([PVsuppression,PVsuppressionlaser], ['No laser','Laser'], ylabel='Suppression Index', title='PV inactivation: sustained')

plt.figure()
band_plots.plot_paired_scatter_with_median([SOMsuppression,SOMsuppressionlaser], ['No laser','Laser'], ylabel='Suppression Index', title='SOM inactivation: sustained')

print stats.wilcoxon(PVsuppression, PVsuppressionlaser)
print stats.wilcoxon(SOMsuppression, SOMsuppressionlaser)