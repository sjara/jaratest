import numpy as np
import os
from jaratoolbox import clusteranalysis
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from jaratoolbox import settings
import imp

class ClusterInforec(object):

    def __init__(self, inforecPath):
        '''
        Class for clustering sites from inforec files
        Args:
            inforecPath (str): The path to the inforec file
        '''

        self.filepath = inforecPath
        self.inforec = self.load_inforec()

    def load_inforec(self):
        inforec = imp.load_source('module.name', self.filepath)
        return inforec

    def cluster_tetrode(self, experiment, site, tetrode,
                        saveSingleSessionCluFiles=True,
                        minClusters=3,
                        maxClusters=6,
                        maxPossibleClusters=6,
                        recluster=True):
        '''
        Cluster a single tetrode from a site.
        Args:
            experiment (int): Index of experiment in inforec to use
            site (int): Index of site in experiment to use
            tetrode (int): Tetrode number to cluster (starts from 1)
            saveSingleSessionCluFiles (bool): Whether to save clu files for individual sessions
            minClusters (int): Minimum number of clusters for KK to find
            maxClusters (int): Max clusters for KK to find
            maxPossibleClusters (int): Max clusters for KK to find
            recluster (bool): Whether to recluster the site if clustering has been done already
        '''

            siteObj = self.inforec.experiments[experiment].sites[site]
            idString = 'exp{}site{}'.format(experiment, site)
            oneTT = cluster_many_sessions(siteObj.subject,
                                          siteObj.session_ephys_dirs(),
                                          tetrode,
                                          idString,
                                          saveSingleSessionCluFiles=saveSingleSessionCluFiles,
                                          minClusters=minClusters,
                                          maxClusters=maxClusters,
                                          maxPossibleClusters=maxPossibleClusters,
                                          recluster=recluster)

    def cluster_site(self, experiment, site, **kwargs):
        '''
        For available kwargs, see help(cluster_tetrode)
        '''
        siteObj = self.inforec.experiments[experiment].sites[site]
        for tetrode in siteObj.tetrodes:
            self.cluster_tetrode(experiment, site, tetrode, **kwargs)

    def cluster_all_sites(self, indExperiment, **kwargs):
        '''
        For available kwargs, see help(cluster_tetrode)
        '''
        experiment = self.inforec.experiments[indExperiment]
        for indSite, site in enumerate(experiment.sites):
            self.cluster_site(indExperiment, indSite, **kwargs)

def cluster_many_sessions(subject, sessions,
                          tetrode, idString,
                          saveSingleSessionCluFiles=True,
                          minClusters=10,
                          maxClusters=12,
                          maxPossibleClusters=12,
                          recluster=False):
        '''
        Run clustering for many ephys sessions
        Args:
            subject (str): Name of subject
            sessions (list): List of session directories (e.g. ['2016-01-01_12-12-12', etc.])
            tetrode (int): Tetrode number to cluster (starts from 1)
            idString (str): A unique identifier for the multisession clustering (usually 'expXsiteY')
            saveSingleSessionCluFiles (bool): Whether to save clu files for individual sessions
            minClusters (int): Minimum number of clusters for KK to find
            maxClusters (int): Max clusters for KK to find
            maxPossibleClusters (int): Max clusters for KK to find
            recluster (bool): Whether to recluster the site if clustering has been done already
        '''

    oneTT = spikesorting.MultipleSessionsToCluster(subject,
                                                   sessions,
                                                   tetrode,
                                                   idString)
    oneTT.load_waveforms()

    clusterFile = os.path.join(oneTT.clustersDir,
                            'Tetrode%d.clu.1'%oneTT.tetrode)
    if os.path.isfile(clusterFile) and not recluster:
        oneTT.set_clusters_from_file()
    else:
        oneTT.create_fet_files()
        oneTT.run_clustering(minClusters, maxClusters, maxPossibleClusters)
        oneTT.set_clusters_from_file()
        oneTT.save_report()
    if saveSingleSessionCluFiles:
        oneTT.save_single_session_clu_files()
    return oneTT
