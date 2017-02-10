# Import the inforec

# Visualize cluster quality

# Have option to re-cluster

import numpy as np
import os
from jaratest.nick.spikesorting import clustermanysessions as cms
from jaratoolbox import clusteranalysis
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from jaratoolbox import settings
from jaratoolbox import celldatabase
import pandas

class ClusterInforec(object):

    def __init__(self, inforecPath):

        self.dbPath = dbPath
        self.filepath = filepath
        self.inforec = self.load_inforec()

        # if os.path.isfile(self.dbPath):
        #     self.db = celldatabase.load_dataframe_from_HDF5(self.dbPath)
        # else:
        #     self.db = pandas.DataFrame()

        #Regenerate the database every time, this will avoid a lot of problems with duplicates.
        self.db = pandas.DataFrame()

    def load_inforec(self):
        inforec = imp.load_source('module.name', self.filepath)
        return inforec

    def save_database(self):
        print 'Saving database...'
        celldatabase.save_dataframe_as_HDF5(self.dbPath, self.db)

    def cluster_tetrode(self, experiment, site, tetrode,
                        saveSingleSessionCluFiles=False,
                        minClusters=3,
                        maxClusters=6,
                        maxPossibleClusters=6,
                        recluster=False,
                        addToDB=False):

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

            if addToDB:
                for cluster in np.unique(oneTT.clusters):
                    clusterDict = {'tetrode':tetrode,
                                   'cluster':cluster}
                    clusterDict.update(siteObj.cluster_info())

                    clusterTimestamps = oneTT.timestamps[oneTT.clusters==cluster]

                    nspikes = len(clusterTimestamps)

                    ISI = np.diff(clusterTimestamps)
                    if len(ISI)==0:  # Hack in case there is only one spike
                        ISI = np.array(10)
                    isiViolations = np.mean(ISI<2e-3) # Assumes ISI in usec

                    clusterDict.update({'nspikes':nspikes,
                                        'isiViolations':isiViolations})

                    clusterDict.update({'experimentInd':experiment,
                                        'siteInd':site})

                    self.db = self.db.append(clusterDict, ignore_index=True)

    def cluster_site(self, experiment, site, **kwargs):
        siteObj = self.inforec.experiments[experiment].sites[site]
        for tetrode in siteObj.tetrodes:
            self.cluster_tetrode(experiment, site, tetrode, **kwargs)

    def cluster_all_sites(self, indExperiment, **kwargs):
        experiment = self.inforec.experiments[indExperiment]
        for indSite, site in enumerate(experiment.sites):
            self.cluster_site(indExperiment, indSite, **kwargs)

    def finalize_all_site_clustering(self, indExperiment, **kwargs):
        self.cluster_all_sites(indExperiment,
                               recluster=False,
                               saveSingleSessionCluFiles=True,
                               addToDB=True)

    def site_cluster_correlation(self, experiment, site, tetrode, cmap='jet'):
        #Has to load the waves for each cluster across all the sessions of the site
        ## Waves have to be aligned and flattened

        siteObj = self.inforec.experiments[experiment].sites[site]

        idString = 'exp{}site{}'.format(experiment, site)

        #Use cms to load all the waveforms
        oneTT = cms.MultipleSessionsToCluster(siteObj.subject,
                                              siteObj.session_ephys_dirs(),
                                              tetrode,
                                              idString)

        oneTT.load_all_waveforms()
        oneTT.set_clusters_from_file()

        # import ipdb; ipdb.set_trace()

        reportDir = 'multisession_{}'.format(idString)
        reportFn = '{}.png'.format(tetrode)
        reportFull = os.path.join(settings.EPHYS_PATH, siteObj.subject, reportDir, reportFn)

        reportImage = mpimg.imread(reportFull)

        plt.figure()
        plt.imshow(reportImage)
        plt.show()

        clustersPerTetrode = 12
        wavesize = 160

        allWaveforms = np.empty((clustersPerTetrode, wavesize))

        for indc in range(clustersPerTetrode):
            # print 'Estimating average waveform for {0} T{1}c{2}'.format(ephysSession,tetrode,indc+1)

            # DONE: get waveforms for one cluster
            #Add 1 to the cluster index because clusters start from 1
            waveforms = oneTT.samples[oneTT.clusters==indc+1, :, :]

            alignedWaveforms = spikesorting.align_waveforms(waveforms)
            meanWaveforms = np.mean(alignedWaveforms,axis=0)
            allWaveforms[indc,:] = meanWaveforms.flatten()


        ccSelf = clusteranalysis.row_corrcoeff(allWaveforms, allWaveforms)

        ccSelf = np.tril(ccSelf, k=-1)

        plt.figure()
        plt.imshow(ccSelf,clim=[0,1], cmap=cmap ,interpolation='nearest')
        plt.axis('image')
        plt.colorbar()
        plt.draw()

        return ccSelf



def cluster_many_sessions(subject, sessions,
                          tetrode, idString,
                          saveSingleSessionCluFiles=False,
                          minClusters=10,
                          maxClusters=12,
                          maxPossibleClusters=12,
                          recluster=False):

    oneTT = cms.MultipleSessionsToCluster(subject,
                                          sessions,
                                          tetrode,
                                          idString)
    oneTT.load_all_waveforms()

    clusterFile = os.path.join(oneTT.clustersDir,
                            'Tetrode%d.clu.1'%oneTT.tetrode)
    if os.path.isfile(clusterFile) and not recluster:
        oneTT.set_clusters_from_file()
    else:
        oneTT.create_multisession_fet_files()
        oneTT.run_clustering(minClusters, maxClusters, maxPossibleClusters)
        oneTT.set_clusters_from_file()
        oneTT.save_multisession_report()
    if saveSingleSessionCluFiles:
        oneTT.save_single_session_clu_files()
    return oneTT
