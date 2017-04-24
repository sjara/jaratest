import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import celldatabase
from jaratoolbox import spikesorting
reload(celldatabase)
import bandwidths_analysis_v2 as bandan
reload(bandan)


#subjects = ['band022','band023']
currentdb = db = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
db = pd.DataFrame()
subjects = ['band025']
for subject in subjects:
    inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
    ci = spikesorting.ClusterInforec(inforec)
    ci.cluster_all_experiments()
    db = db.append(celldatabase.generate_cell_database(inforec),ignore_index=True)
#db = db[db['isiViolations']<2.0]
db = db.reindex(columns=np.concatenate((db.columns.values,['clusterQuality','atBestFreq','bestFreq'])))

for indCell, cell in db.iterrows():
    peakAmplitudes = cell['clusterPeakAmplitudes']
    spikeShapeSD = cell['clusterSpikeSD']
    shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
    db.set_value(indCell, 'clusterQuality', shapeQuality)
    bestBand, atBestFreq, bestFreq = bandan.best_band_index(cell)
    db.set_value(indCell, 'atBestFreq', atBestFreq)
    if atBestFreq:
        db.set_value(indCell, 'bestFreq', bestFreq)
        suppressionStats, laserResponse = bandan.suppression_stats(cell, bestBand)
        if suppressionStats is not None:
            db.set_value(indCell, 'laserResponse', laserResponse)
            db.set_value(indCell, 'HighAmpSS', suppressionStats[1])
            db.set_value(indCell, 'HighPeakLoc', suppressionStats[3])
            db.set_value(indCell, 'HighPeakSR', suppressionStats[5])
            if suppressionStats[0] is not None:
                db.set_value(indCell, 'LowAmpSS', suppressionStats[0])
                db.set_value(indCell, 'LowPeakLoc', suppressionStats[2])
                db.set_value(indCell, 'LowPeakSR', suppressionStats[4])
#db.to_csv('/home/jarauser/src/jaratest/anna/analysis/all_clusters.csv')
currentdb = currentdb.append(db)
currentdb.to_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5', 'database')


#manual assignment of cluster quality
'''for indCell, cell in alldata.iterrows():
    if pd.isnull(cell['clusterQuality']):
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
        alldata.set_value(indCell, 'clusterQuality', int(quality))
        alldata.to_csv('/home/jarauser/src/jaratest/anna/analysis/all_good_cells_v2.csv')'''

