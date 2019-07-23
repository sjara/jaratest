import pandas as pd
import numpy as np
from jaratoolbox import celldatabase
from jaratoolbox import spikesorting
import band_ephys_analysis as bandan
reload(bandan)

CASE=1


if CASE==1:
    #currentdb = pd.read_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5','database',index_col=0)
    currentdb = pd.DataFrame()
    db = pd.DataFrame()
    subjects = ['band002','band003','band004','band005','band015','band016','band022','band023','band025','band026','band027','band028','band029','band030','band031','band033','band034']
    for subject in subjects:
        inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
        db = db.append(celldatabase.generate_cell_database(inforec),ignore_index=True)
    db = db.reindex(columns=np.concatenate((db.columns.values,['clusterQuality','bestFreq','bestBandIndex','laserResponse','nBandSpikes','suppressionIndex','facilitationIndex','preferedBandwidth','gaussFit'])))
    db['suppressionIndex'] = db['suppressionIndex'].astype('object')
    db['facilitationIndex'] = db['facilitationIndex'].astype('object')
    db['preferedBandwidth'] = db['preferedBandwidth'].astype('object')
    db['gaussFit'] = db['gaussFit'].astype('object')
    
    for indCell, cell in db.iterrows():
        peakAmplitudes = cell['clusterPeakAmplitudes']
        spikeShapeSD = cell['clusterSpikeSD']
        shapeQuality = abs(peakAmplitudes[1]/spikeShapeSD.mean())
        db.set_value(indCell, 'clusterQuality', shapeQuality)
        
        laserResponse = bandan.laser_response(cell)
        db.set_value(indCell, 'laserResponse', laserResponse)
        
        bandIndex, bestFreq, gaussFit, Rsquared, octavesFromBest = bandan.best_index(cell, 'bandwidth')
        db.set_value(indCell, 'bestFreq', bestFreq)
        db.set_value(indCell, 'bestBandIndex', bandIndex)
        db.set_value(indCell, 'gaussFit', gaussFit)
        db.set_value(indCell, 'tuningFitR2', Rsquared)
        db.set_value(indCell, 'octavesFromBestFreq', octavesFromBest)
        
        suppressionIndex, facilitationIndex, preferedBandwidth, nBandSpikes = bandan.bandwidth_tuning_stats(cell, bandIndex)
        db.set_value(indCell, 'nBandSpikes', nBandSpikes)
        if suppressionIndex is not None:
            db.set_value(indCell, 'suppressionIndex', suppressionIndex)
            db.set_value(indCell, 'facilitationIndex', facilitationIndex)
            db.set_value(indCell, 'preferedBandwidth', preferedBandwidth)
    
    currentdb = currentdb.append(db)
    currentdb.to_csv('/home/jarauser/src/jaratest/anna/analysis/all_clusters.csv')
    currentdb.to_hdf('/home/jarauser/src/jaratest/anna/analysis/all_clusters.h5', 'database')
    
elif CASE==2:
    subject = 'band034'
    inforec = '/home/jarauser/src/jaratest/common/inforecordings/{0}_inforec.py'.format(subject)
    ci = spikesorting.ClusterInforec(inforec)
    ci.cluster_all_experiments()


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

