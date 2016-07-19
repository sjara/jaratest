import os
from jaratoolbox import spikesorting
from jaratoolbox.test.nick.ephysExperiments import clusterManySessions_v2 as cms2
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v2 as ee2
import matplotlib.pyplot as plt
plt.ioff() #Turn off interactive plottting, save figs to png instead
import numpy as np
reload(cms2)
reload(ee2)

def laser_tc_analysis(site, sitenum):

    '''
    Data analysis function for laser/tuning curve experiments

    This function will take a RecordingSite object, do multisession clustering on it, and save all of the clusters 
    back to the original session cluster directories. We can then use an EphysExperiment object (version 2) 
    to load each session, select clusters, plot the appropriate plots, etc. This code is being removed from 
    the EphysExperiment object because that object should be general and apply to any kind of recording 
    experiment. This function does the data analysis for one specific kind of experiment. 
    
    Args:

        site (RecordingSite object): An instance of the RecordingSite class from the ephys_experiment_v2 module
        sitenum (int): The site number for the site, used for constructing directory names
    
    Example:
    
        from jaratoolbox.test.nick.ephysExperiments import laserTCanalysis
        for indSite, site in enumerate(today.siteList):
            laserTCanalysis.laser_tc_analysis(site, indSite+1)
    '''
    #This is where I should incorporate Lan's sorting function
    #Construct a multiple session clustering object with the session list. 
    for tetrode in site.goodTetrodes:

        oneTT = cms2.MultipleSessionsToCluster(site.animalName, site.get_session_filenames(), tetrode, '{}site{}'.format(site.date, sitenum))
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
        '''
        0710: Ran into problems while saving single session clu file:
        ipdb> can't invoke "event" command: application has been destroyed
        while executing
        "event generate $w <<ThemeChanged>>"
        (procedure "ttk::ThemeChanged" line 6)
        invoked from within
        "ttk::ThemeChanged"
        Fixed by commenting out this line. 
        0712: This seemed to be a warning instead of actual error, still generated reports and save        ed files.
        0712: if not saving single session clu files, ran into another problem when ploting single         cluster raster plots. so have to save them and fix the
        ValueError:too many boolean indices
        > /home/languo/src/jaratoolbox/test/nick/ephysExperiments/clusterManySessions_v2.py(119)sav        e_single_session_clu_files()
        118 
        --> 119             clusterNumsThisSession = self.clusters[self.recordingNumber == indSessi        on]
        120             print "Writing .clu.1 file for session {}".format(session)
        This is fixed: old clu files from last clustering is messing me up, making self.clusters an        d self.RecordingNumber be different size.
        '''

        possibleClusters = np.unique(oneTT.clusters)

        #We also need to initialize an EphysExperiment object to get the sessions
        exp2 = ee2.EphysExperiment(site.animalName, site.date, experimenter = site.experimenter)

        #Iterate through the clusters, making a new figure for each cluster. 
        for indClust, cluster in enumerate(possibleClusters): #Using possibleClusters[1:] was a hack to omit cluster 1 which usually contains noise and sometimes don't have spikes in the range for raster plot to run properlyl
            plt.figure(figsize = (8.5,11))

            #The first noise burst raster plot
            plt.subplot2grid((5, 6), (0, 0), rowspan = 1, colspan = 3)
            nbIndex = site.get_session_types().index('noiseBurst')
            nbSession = site.get_session_filenames()[nbIndex]
            
            exp2.plot_session_raster(nbSession, tetrode, cluster = cluster, replace = 1)
            
            plt.ylabel('Noise Bursts')
            plt.title(nbSession, fontsize = 10)

            #The laser pulse raster plot
            plt.subplot2grid((5, 6), (1, 0), rowspan = 1, colspan = 3)
            lpIndex = site.get_session_types().index('laserPulse')
            lpSession = site.get_session_filenames()[lpIndex]
            exp2.plot_session_raster(lpSession, tetrode, cluster = cluster, replace = 1)
            plt.ylabel('Laser Pulses')
            plt.title(lpSession, fontsize = 10)

            #The laser train raster plot
            plt.subplot2grid((5, 6), (2, 0), rowspan = 1, colspan = 3)
            try:  
                ltIndex = site.get_session_types().index('laserTrain')
                ltSession = site.get_session_filenames()[ltIndex]
                exp2.plot_session_raster(ltSession, tetrode, cluster = cluster, replace = 1)
                plt.ylabel('Laser Trains')
                plt.title(ltSession, fontsize = 10)
            except ValueError:
                print 'This session doesnot exist.'

            #The tuning curve
            plt.subplot2grid((5, 6), (0, 3), rowspan = 3, colspan = 3)
            tcIndex = site.get_session_types().index('tuningCurve')
            tcSession = site.get_session_filenames()[tcIndex]
            tcBehavID = site.get_session_behavIDs()[tcIndex]
            exp2.plot_session_tc_heatmap(tcSession, tetrode, tcBehavID, replace = 1, cluster = cluster)
            plt.title("{0}\nBehavFileID = '{1}'".format(tcSession, tcBehavID), fontsize = 10)

            '''
            The best freq presentation, if a session is not initialized, a Value            Error is raised  when indexing the list returned by the get_ methods            of ee2.RecordingSite. Could use Try Except ValueError?
            '''
           #plt.subplot2grid((6, 6), (3, 0), rowspan=1, colspan=3)
           #bfIndex = site.get_session_types().index('bestFreq')
           #bfSession = site.get_session_filenames()[bfIndex]
           #exp2.plot_session_raster(bfSession, tetrode, cluster = cluster, replace = 1)
           #plt.ylabel('Best Frequency')
           #plt.title(bfSession, fontsize = 10)

           #FIXME: Omitting the laser pulses at different intensities for now

            '''LG0710: Added reports (ISI, waveform, events in time, projections) for each cluster to its sessions summary graph. The MultiSessionClusterReport class initializer calls plot_report automatically... it's hard to get around doing repeated work (i.e. getting bits and pieces of necessary functionality out of this class manually) here without rewriting this class'''

            nSpikes = len(oneTT.timestamps) 
            nClusters = len(possibleClusters)
            spikesEachCluster = np.empty((nClusters, nSpikes),dtype = bool)
            if oneTT.clusters == None:
                oneTT.set_clusters_from_file()
            for indc, clusterID in enumerate (possibleClusters):
                spikesEachCluster[indc, :] = (oneTT.clusters==clusterID)
            
            tsThisCluster = oneTT.timestamps[spikesEachCluster[indClust,:]]
            wavesThisCluster = oneTT.samples[spikesEachCluster[indClust,:],:,:]
            # -- Plot ISI histogram --
            plt.subplot2grid((5,6), (3,0), rowspan=1, colspan=3)
            spikesorting.plot_isi_loghist(tsThisCluster)
            plt.ylabel('c%d'%clusterID,rotation=0,va='center',ha='center')

            # -- Plot waveforms --
            plt.subplot2grid((5,6), (4,0), rowspan=1, colspan=3)
            spikesorting.plot_waveforms(wavesThisCluster)

            # -- Plot projections --
            plt.subplot2grid((5,6), (3,3), rowspan=1, colspan=3)
            spikesorting.plot_projections(wavesThisCluster)  
            
            # -- Plot events in time --
            plt.subplot2grid((5,6), (4,3), rowspan=1, colspan=3)
            spikesorting.plot_events_in_time(tsThisCluster)
            
            #Save the figure in the multisession clustering folder so that it is easy to find
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster)
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            plt.tight_layout()
            plt.savefig(full_fig_path, format = 'png')
            #plt.show()
            plt.close()

        plt.figure()
        oneTT.save_multisession_report()
        plt.close()

'''
Old code to plot the waveforms - not sure how we are going to change this analysis, so not implementing yet
        elif indSession == 5: # Laser pulses at 3mW

            if site.sessionList[5]:
                subplot2grid((4, 6), (3, 3), rowspan = 1, colspan = 3)
                hold(True)

                #alignedWaveforms = align_waveforms(clusterSamples)

                #plot_waveforms(alignedWaveforms)
                if shape(clusterSamples)[0]:
                    #pdb.set_trace()

                    clusterSamples = reshape(clusterSamples, [len(clusterSamples), 160])

                    meanSample  = clusterSamples.mean(axis=0)

                    plot(meanSample, 'r')

                    indsToPlot = np.random.randint(len(clusterSamples), size = 20)

                    for indP in indsToPlot:
                        plot(clusterSamples[indP, :], 'r', alpha = 0.1)


        elif indSession == 6: # Laser pulses at 1mW
            if site.sessionList[6]:
                #subplot2grid((4, 6), (3, 3), rowspan = 1, colspan = 3)
                hold(True)

                #alignedWaveforms = align_waveforms(clusterSamples)

                #plot_waveforms(alignedWaveforms)
                if shape(clusterSamples)[0]:
                    #pdb.set_trace()

                    clusterSamples = reshape(clusterSamples, [len(clusterSamples), 160])

                    meanSample  = clusterSamples.mean(axis=0)

                    plot(meanSample, 'b')

                    indsToPlot = np.random.randint(len(clusterSamples), size = 20)

                    for indP in indsToPlot:
                        plot(clusterSamples[indP, :], 'b', alpha = 0.1)


'''
