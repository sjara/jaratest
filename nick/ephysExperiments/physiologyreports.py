from jaratoolbox.test.nick.ephysExperiments import clusterManySessions_v2 as cms2
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v3 as ee3
import matplotlib.pyplot as plt
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
import os
import numpy as np

def nick_lan_main_report(siteObj, show=False, save=True, saveClusterReport=True):
    for tetrode in siteObj.goodTetrodes:
        oneTT = cms2.MultipleSessionsToCluster(
            siteObj.animalName,
            siteObj.get_session_filenames(),
            tetrode,
            '{}at{}um'.format(
                siteObj.date,
                siteObj.depth))
        oneTT.load_all_waveforms()

        # Do the clustering if necessary.
        clusterFile = os.path.join(
            oneTT.clustersDir,
            'Tetrode%d.clu.1' %
            oneTT.tetrode)
        if os.path.isfile(clusterFile):
            oneTT.set_clusters_from_file()
        else:
            oneTT.create_multisession_fet_files()
            oneTT.run_clustering()
            oneTT.set_clusters_from_file()

        oneTT.save_single_session_clu_files()
        possibleClusters = np.unique(oneTT.clusters)

        ee = ee3.EphysExperiment(
            siteObj.animalName,
            siteObj.date,
            experimenter=siteObj.experimenter)

        # Iterate through the clusters, making a new figure for each cluster.
        # for indClust, cluster in enumerate([3]):
        for indClust, cluster in enumerate(possibleClusters):

            mainRasterInds = siteObj.get_session_inds_one_type(
                plotType='raster',
                report='main')
            mainRasterSessions = [
                siteObj.get_session_filenames()[i] for i in mainRasterInds]
            mainRasterTypes = [
                siteObj.get_session_types()[i] for i in mainRasterInds]

            mainTCinds = siteObj.get_session_inds_one_type(
                plotType='tc_heatmap',
                report='main')
            mainTCsessions = [
                siteObj.get_session_filenames()[i] for i in mainTCinds]

            mainTCbehavIDs = [
                siteObj.get_session_behavIDs()[i] for i in mainTCinds]
            mainTCtypes = [siteObj.get_session_types()[i] for i in mainTCinds]

            # The main report for this cluster/tetrode/session
            plt.figure()

            for indRaster, rasterSession in enumerate(mainRasterSessions):
                plt.subplot2grid(
                    (6, 6), (indRaster, 0), rowspan=1, colspan=3)
                ee.plot_session_raster(
                    rasterSession,
                    tetrode,
                    cluster=cluster,
                    replace=1,
                    ms=1)
                plt.ylabel(
                    '{}\n{}'.format(
                        mainRasterTypes[indRaster],
                        rasterSession.split('_')[1]),
                    fontsize=10)
                ax = plt.gca()
                extraplots.set_ticks_fontsize(ax, 6)

            # We can only do one main TC for now.
            plt.subplot2grid((6, 6), (0, 3), rowspan=3, colspan=3)
            tcSession = mainTCsessions[0]
            tcBehavID = mainTCbehavIDs[0]
            ee.plot_session_tc_heatmap(
                tcSession,
                tetrode,
                tcBehavID,
                replace=1,
                cluster=cluster)
            plt.title(
                "{0}\nBehavFileID = '{1}'".format(
                    tcSession,
                    tcBehavID),
                fontsize=10)

            nSpikes = len(oneTT.timestamps)
            nClusters = len(possibleClusters)
            #spikesEachCluster = np.empty((nClusters, nSpikes),dtype = bool)
            # if oneTT.clusters == None:
            # oneTT.set_clusters_from_file()
            # for indc, clusterID in enumerate (possibleClusters):
            #spikesEachCluster[indc, :] = (oneTT.clusters==clusterID)

            tsThisCluster = oneTT.timestamps[oneTT.clusters == cluster]
            wavesThisCluster = oneTT.samples[oneTT.clusters == cluster]
            # -- Plot ISI histogram --
            plt.subplot2grid((6, 6), (4, 0), rowspan=1, colspan=3)
            spikesorting.plot_isi_loghist(tsThisCluster)
            plt.ylabel(
                'c%d' %
                cluster,
                rotation=0,
                va='center',
                ha='center')
            plt.xlabel('')

            # -- Plot waveforms --
            plt.subplot2grid((6, 6), (5, 0), rowspan=1, colspan=3)
            spikesorting.plot_waveforms(wavesThisCluster)

            # -- Plot projections --
            plt.subplot2grid((6, 6), (4, 3), rowspan=1, colspan=3)
            spikesorting.plot_projections(wavesThisCluster)

            # -- Plot events in time --
            plt.subplot2grid((6, 6), (5, 3), rowspan=1, colspan=3)
            spikesorting.plot_events_in_time(tsThisCluster)

            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster)
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            # plt.tight_layout()

            if save: 
                plt.savefig(full_fig_path, format='png')
            if show:
                plt.show()
            if not show:
                plt.close()

        if saveClusterReport:
            plt.figure()
            oneTT.save_multisession_report()
            plt.close()
