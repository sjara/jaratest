import sys; sys.path.append('/home/jarauser/data')
import os
from jaratest.anna.inforecordings import band005_inforec as inforec
from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms
reload(cms)
import pandas
import numpy as np
import matplotlib.pyplot as plt

tetrodes = range(1,9)

db = pandas.DataFrame()

for experiment in inforec.experiments:
    for i,site in enumerate(experiment.sites):
        for tetrode in site.tetrodes:
            siteName = '{0}_{1}um'.format(site.date,site.depth)
            oneTT = cms.MultipleSessionsToCluster(site.subject, site.session_ephys_dirs(), tetrode, siteName)
            oneTT.load_all_waveforms()
            clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)

            if os.path.isfile(clusterFile):
                oneTT.set_clusters_from_file()
            else:
                if oneTT.nSpikes != 0:
                    oneTT.create_multisession_fet_files()
                    oneTT.run_clustering(MinClusters=3, MaxClusters=6, MaxPossibleClusters=6)
                    oneTT.set_clusters_from_file()
                    oneTT.save_single_session_clu_files() #Don't do this yet because it will overwrite
                plt.clf()
                oneTT.save_multisession_report()
                
            for cluster in np.unique(oneTT.clusters):
                clusterDict=site.cluster_info()
                clusterDict.update({'tetrode':tetrode, 'cluster':cluster})
                isi = np.diff(oneTT.timestamps[oneTT.clusters==cluster])
                isiViolations = sum(isi<0.002)/np.double(len(isi))*100
                clusterDict.update({'isiViolations': isiViolations})
                clusterDict.update({'nSpikes': len(oneTT.timestamps[oneTT.clusters==cluster])})
                db = db.append(clusterDict, ignore_index=True)

db.to_csv('/home/jarauser/src/jaratest/anna/analysis/band005_celldb.csv')