'''
2015-08-01 Nick Ponvert

This module will contain report plotting methods that act on entire sites

'''
from jaratoolbox.test.nick.ephysExperiments import clusterManySessions_v2 as cms2
reload(cms2)
from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
reload(dataplotter)
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
import matplotlib.pyplot as plt
import numpy as np
import os

def cluster_site(site, siteName, tetrode, report=True):
    oneTT = cms2.MultipleSessionsToCluster(site.animalName, site.get_session_ephys_filenames(), tetrode, '{}_{}'.format(site.date, siteName))
    oneTT.load_all_waveforms()

    #Do the clustering if necessary.
    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    if os.path.isfile(clusterFile):
        oneTT.set_clusters_from_file()
    else:
        oneTT.create_multisession_fet_files()
        oneTT.run_clustering()
        oneTT.set_clusters_from_file()
        oneTT.save_single_session_clu_files()

    if report:
        plt.clf()
        oneTT.save_multisession_report()

    return oneTT #This is a little bit lazy, it should really spit out some attributes not the whole object

def cluster_site_PCA(site, siteName, tetrode, report=True, **kwargs):

    from jaratoolbox.test.nick.spikesorting import pcasort

    oneTT = cms2.MultipleSessionsToCluster(site.animalName, site.get_session_ephys_filenames(), tetrode, '{}_{}'.format(site.date, siteName))
    oneTT.load_all_waveforms()

    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    if os.path.isfile(clusterFile):
        oneTT.set_clusters_from_file()

    else:
        (numSpikes, numChans, numSamples) = np.shape(oneTT.samples)
        allWaves = oneTT.samples.reshape(numSpikes, numChans*numSamples)
        sorter = pcasort.PCASpikeSorter(allWaves, **kwargs)
        oneTT.clusters = sorter.clusters
        oneTT.save_single_session_clu_files()

    if report:
        plt.clf()
        oneTT.save_multisession_report()

    return oneTT

def calculate_site_ISI_violations(site, siteName):

    siteClusterISIViolations = {}


    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode, report=False)
        possibleClusters=np.unique(oneTT.clusters)

        for indClust, cluster in enumerate(possibleClusters):

            tsThisCluster = oneTT.timestamps[oneTT.clusters==cluster]
            tetClustName = '{0}T{1}c{2}'.format(siteName, tetrode, cluster)
            isiThisCluster = calculate_isi_violations(tsThisCluster)
            siteClusterISIViolations[tetClustName] = isiThisCluster

    return siteClusterISIViolations


def calculate_site_response(site, siteName, sessionInd, maxZonly=False):

    from jaratoolbox import spikesanalysis

    #Zscore settings from billy

    baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
    binTime = baseRange[1]-baseRange[0]         # Time-bin size
    responseTimeRange = [-0.5,1]       #Time range to calculate z value for (should be divisible by binTime
    responseTime = responseTimeRange[1]-responseTimeRange[0]
    numBins = responseTime/binTime
    binEdges = np.arange(responseTimeRange[0], responseTimeRange[1], binTime)
    timeRange = [-0.5, 1]

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    sessionEphys = site.get_mouse_relative_ephys_filenames()[sessionInd]

    siteClusterMaxZ = {}
    siteClusterPval = {}
    siteClusterZstat = {}

    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode, report=False)
        possibleClusters=np.unique(oneTT.clusters)


        for indClust, cluster in enumerate(possibleClusters):

            rasterSpikes = loader.get_session_spikes(sessionEphys, tetrode)
            spikeTimes = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]
            rasterEvents = loader.get_session_events(sessionEphys)
            eventOnsetTimes = loader.get_event_onset_times(rasterEvents)


            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimes,eventOnsetTimes,timeRange)


            [zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges) #computes z score for each bin. zStat is array of z scores. maxZ is maximum value of z in timeRange

            tetClustName = '{0}T{1}c{2}'.format(siteName, tetrode, cluster)
            siteClusterMaxZ[tetClustName] = maxZ
            siteClusterPval[tetClustName] = pValue
            siteClusterZstat[tetClustName] = zStat


    if maxZonly:
        return siteClusterMaxZ
    else:
      return siteClusterZstat, siteClusterPval, siteClusterMaxZ


def find_good_clusters(site, siteName, soundInd, laserInd, maxISI=0.02, minSoundZ=2, minLaserZ=2):


    isi = calculate_site_ISI_violations(site,siteName)
    soundMaxZ = calculate_site_response(site,siteName, sessionInd = soundInd, maxZonly=True)
    laserMaxZ = calculate_site_response(site,siteName, sessionInd = laserInd, maxZonly=True)

    goodISI = [cell for cell, val in isi.iteritems() if val<maxISI]
    soundResponsive = [cell for cell, val in soundMaxZ.iteritems() if val>minSoundZ]
    laserResponsive = [cell for cell, val in laserMaxZ.iteritems() if val>minLaserZ]

    return list(set(goodISI) & set(soundResponsive) & set(laserResponsive))


def nick_lan_daily_report(site, siteName, mainRasterInds, mainTCind, pcasort=True):
    '''

    '''

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)


    for tetrode in site.tetrodes:

        #Tetrodes with no spikes will cause an error when clustering
        try:
            if pcasort:
                oneTT = cluster_site_PCA(site, siteName, tetrode)
            else:
                oneTT = cluster_site(site, siteName, tetrode)
        except AttributeError:
            print "There was an attribute error for tetrode {} at {}".format(tetrode, siteName)
            continue

        possibleClusters=np.unique(oneTT.clusters)


        #Iterate through the clusters, making a new figure for each cluster.
        #for indClust, cluster in enumerate([3]):
        for indClust, cluster in enumerate(possibleClusters):


            mainRasterEphysFilenames = [site.get_mouse_relative_ephys_filenames()[i] for i in mainRasterInds]
            mainRasterTypes = [site.get_session_types()[i] for i in mainRasterInds]
            if mainTCind:
                mainTCsession = site.get_mouse_relative_ephys_filenames()[mainTCind]
                mainTCbehavFilename = site.get_mouse_relative_behav_filenames()[mainTCind]
                mainTCtype = site.get_session_types()[mainTCind]
            else:
                mainTCsession=None

            # plt.figure() #The main report for this cluster/tetrode/session
            plt.clf()

            for indRaster, rasterSession in enumerate(mainRasterEphysFilenames):
                plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)

                rasterSpikes = loader.get_session_spikes(rasterSession, tetrode)
                spikeTimestamps = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]

                rasterEvents = loader.get_session_events(rasterSession)
                eventOnsetTimes = loader.get_event_onset_times(rasterEvents)

                dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=1)

                plt.ylabel('{}\n{}'.format(mainRasterTypes[indRaster], rasterSession.split('_')[1]), fontsize = 10)
                ax=plt.gca()
                extraplots.set_ticks_fontsize(ax,6) #Should this go in dataplotter?

            #We can only do one main TC for now.
            if mainTCsession:

                plt.subplot2grid((6, 6), (0, 3), rowspan = 3, colspan = 3)


                bdata = loader.get_session_behavior(mainTCbehavFilename)
                plotTitle = loader.get_session_filename(mainTCsession)
                eventData = loader.get_session_events(mainTCsession)
                spikeData = loader.get_session_spikes(mainTCsession, tetrode)

                spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

                eventOnsetTimes = loader.get_event_onset_times(eventData)

                freqEachTrial = bdata['currentFreq']
                intensityEachTrial = bdata['currentIntensity']

                possibleFreq = np.unique(freqEachTrial)
                possibleIntensity = np.unique(intensityEachTrial)

                xlabel='Frequency (kHz)'
                ylabel='Intensity (dB SPL)'

                # firstSortLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
                # secondSortLabels = ['{}'.format(inten) for inten in possibleIntensity]

                # dataplotter.two_axis_heatmap(spikeTimestamps,
                #                             eventOnsetTimes,
                #                             freqEachTrial,
                #                             intensityEachTrial,
                #                             firstSortLabels,
                #                             secondSortLabels,
                #                             xlabel,
                #                             ylabel,
                #                             plotTitle=plotTitle,
                #                             flipFirstAxis=False,
                #                             flipSecondAxis=True,
                #                             timeRange=[0, 0.1])

                freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
                intenLabels = ["%.1f" % inten for inten in possibleIntensity]

                dataplotter.two_axis_heatmap(spikeTimestamps=spikeTimestamps,
                                            eventOnsetTimes=eventOnsetTimes,
                                            firstSortArray=intensityEachTrial,
                                            secondSortArray=freqEachTrial,
                                            firstSortLabels=intenLabels,
                                            secondSortLabels=freqLabels,
                                            xlabel=xlabel,
                                            ylabel=ylabel,
                                            plotTitle=plotTitle,
                                            flipFirstAxis=True,
                                            flipSecondAxis=False,
                                            timeRange=[0, 0.1])

                plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)
                plt.show()


            nSpikes = len(oneTT.timestamps)
            nClusters = len(possibleClusters)

            tsThisCluster = oneTT.timestamps[oneTT.clusters==cluster]
            wavesThisCluster = oneTT.samples[oneTT.clusters==cluster]


            # -- Plot ISI histogram --
            plt.subplot2grid((6,6), (4,0), rowspan=1, colspan=3)
            spikesorting.plot_isi_loghist(tsThisCluster)
            plt.ylabel('c%d'%cluster,rotation=0,va='center',ha='center')
            plt.xlabel('')

            # -- Plot waveforms --
            plt.subplot2grid((6,6), (5,0), rowspan=1, colspan=3)
            spikesorting.plot_waveforms(wavesThisCluster)

            # -- Plot projections --
            plt.subplot2grid((6,6), (4,3), rowspan=1, colspan=3)
            spikesorting.plot_projections(wavesThisCluster)

            # -- Plot events in time --
            plt.subplot2grid((6,6), (5,3), rowspan=1, colspan=3)
            spikesorting.plot_events_in_time(tsThisCluster)

            plt.subplots_adjust(wspace = 0.7)
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster)
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            #plt.tight_layout()
            plt.savefig(full_fig_path, format = 'png')
            #plt.show()
            # plt.close()


def calculate_isi_violations(timeStamps,nBins=350):
    '''
    Returns the proportion of ISIs less than 2msec
    '''

    ISI = np.diff(timeStamps)
    if np.any(ISI<0):
        raise 'Times of events are not ordered (or there is at least one repeated).'
    if len(ISI)==0:  # Hack in case there is only one spike
        ISI = np.array(10)
    logISI = np.log10(ISI)
    [ISIhistogram,ISIbinsLog] = np.histogram(logISI,bins=nBins)
    ISIbins = 1000*(10**ISIbinsLog[:-1]) # Conversion to msec
    # fractionViolation = np.mean(ISI<1e-3) # We are not using this one
    fractionViolation2 = np.mean(ISI<2e-3) # Assumes ISI in usec

    return fractionViolation2



def am_mod_report(site, siteName, amSessionInd):
    '''

    '''
    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in site.tetrodes:
        try:
            oneTT = cluster_site(site, siteName, tetrode)
        except AttributeError:
            print "There was an attribute error for tetrode {} at {}".format(tetrode, siteName)
            continue
        possibleClusters=np.unique(oneTT.clusters)

        for indClust, cluster in enumerate(possibleClusters):


            amFilename = site.get_mouse_relative_ephys_filenames()[amSessionInd]
            amBehav = site.get_mouse_relative_behav_filenames()[amSessionInd]

            plt.clf()

            spikeData = loader.get_session_spikes(amFilename, tetrode, cluster=cluster)
            spikeTimes = spikeData.timestamps

            eventData = loader.get_session_events(amFilename)
            eventOnsetTimes = loader.get_event_onset_times(eventData)

            bdata = loader.get_session_behavior(amBehav)

            currentFreq = bdata['currentFreq']

            dataplotter.plot_raster(spikeTimes, eventOnsetTimes, sortArray=currentFreq)
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}_Amp_Mod.png'.format(tetrode, cluster)
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            plt.savefig(full_fig_path, format = 'png')
