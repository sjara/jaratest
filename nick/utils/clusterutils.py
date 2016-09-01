from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms
import os

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

def cluster_many_sessions(subject, sessions, tetrode, idString,
                 saveSingleSessionCluFiles=False):
    oneTT = cms.MultipleSessionsToCluster(subject,
                                          sessions,
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
