import sys; sys.path.append('/home/nick/data')
sys.path.append('/home/nick/src')

from inforecordings import test098_inforec as inforec
from jaratoolbox import loadopenephys
from jaratoolbox import settings
from jaratoolbox import spikesorting
from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms
from jaratoolbox import celldatabase

from matplotlib import pyplot as plt
import numpy as np
import os

#Load the inforec file and use the InfoRec object inside to access the experiments

#Print the experiments and number of sessions for an inforec object
print inforec.test098

session=inforec.test098.experiments[0].sites[0].sessions[0]
site=inforec.test098.experiments[0].sites[0]

tetrode=6

oneTT = cluster_session(session, tetrode)
cluster_site(site, tetrode, 'cluster_test')

def cluster_session(session, tetrode, features=['peak', 'valleyFirstHalf']):
    #TODO: the oneTT obj here has dataTT attribute, the cms one does not
    oneTT = spikesorting.TetrodeToCluster(session.subject,
                                        session.ephys_dir(),
                                        tetrode,
                                        features)
    oneTT.load_waveforms()
    clusterFile = os.path.join(oneTT.clustersDir,
                            'Tetrode%d.clu.1'%oneTT.tetrode)
    if os.path.isfile(clusterFile):
        oneTT.dataTT.set_clusters(clusterFile)
    else:
        oneTT.create_fet_files()
        oneTT.run_clustering()
        oneTT.save_report()
    return oneTT

def cluster_site(site, tetrode, idString,
                 features=['peak', 'valleyFirstHalf'],
                 saveSingleSessionCluFiles=False):
    oneTT = cms.MultipleSessionsToCluster(site.subject,
                                          site.session_ephys_dirs(),
                                          tetrode,
                                          idString)
    oneTT.load_all_waveforms()

    clusterFile = os.path.join(oneTT.clustersDir,
                            'Tetrode%d.clu.1'%oneTT.tetrode)
    if os.path.isfile(clusterFile):
        oneTT.set_clusters_from_file()
    else:
        oneTT.create_multisession_fet_files()
        oneTT.run_clustering()
        oneTT.save_multisession_report()
    if saveSingleSessionCluFiles:
        oneTT.save_single_session_clu_files()
    return oneTT


def add_to_database(dbObj,
                    oneTTobj,
                    infoObj,
                    clusters='all'):
    '''
    TODO: work in progress, needs to be cleaner to use
    Adds clusters to a database. Can be used with either a Site object or a Session object

    Args:
        dbObj (pandas.DataFrame): The database to append the clusters to
        oneTTobj (jaratoolbox.spikesorting.TetrodeToCluster): The clustering object
        infoObj (jaratest.celldatabase.Session or Site): The site or session object for the cluster


    '''
    if clusters=='all':
        for cluster in np.unique(oneTTobj.clusters):
            clusterDict = infoObj.cluster_info()
            clusterDict.update({'tetrode':oneTTobj.tetrode,
                             'cluster':cluster})
            db.append(clusterDict, ignore_index=True)



