import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import spikesorting
import bandwidths_analysis_v2 as bandan

'''
subjects = ['band002', 'band003', 'band004', 'band005', 'band015', 'band016']
db = pd.DataFrame()
for subject in subjects:
    db = db.append(pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/'+subject+'_celldb.csv',index_col=0),ignore_index=True)
cells = db[db['isiViolations']<2.0]
cells = cells.reindex(columns=np.concatenate((cells.columns.values,['clusterQuality'])))
cells.to_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv')'''

cells = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv',index_col=0)
plt.figure()

for indCell, cell in cells.iterrows():
    if (cell['clusterQuality']==3):
        fig = plt.gcf()
        plt.clf()
        cellInfo = bandan.get_cell_info(cell)
        tsThisCluster, wavesThisCluster = bandan.load_cluster_waveforms(cellInfo)
        spikesorting.plot_waveforms(wavesThisCluster)
        plt.show()
        plt.pause(0.0001)
        try:
            quality = input('Cluster '+ str(indCell)+' quality: ')
        except (SyntaxError):
            quality = input('Try again idiot: ')
        cells.set_value(indCell, 'clusterQuality', int(quality))
        cells.to_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells.csv')

