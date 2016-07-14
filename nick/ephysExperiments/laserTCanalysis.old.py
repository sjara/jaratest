import os
from jaratoolbox.test.nick.ephysExperiments import clusterManySessions_v2 as cms2
reload(cms2)
from jaratoolbox.test.nick.ephysExperiments import ephys_experiment_v2 as ee2
reload(ee2)
import matplotlib.pyplot as plt
plt.ioff() #Turn off interactive plottting, save figs to png instead
import numpy as np

def laser_tc_analysis(site, sitenum):

    '''
    Data analysis function for laser/tuning curve experiments

    This function will take a RecordingSite object, do multisession clustering on it, and save all of the clusters 
    back to the original session cluster directories. We can then use an EphysExperiment object (version 2) 
    to load each session, select clusters, plot the appropriate plots, etc. This code is being removed from 
    the EphysExperiment object because that object should be general and apply to any kind of recording 
    experiment. This function does the data analysis for one specific kind of experiment. 
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
        possibleClusters = np.unique(oneTT.clusters)

        #We also need to initialize an EphysExperiment object to get the sessions
        exp2 = ee2.EphysExperiment(site.animalName, site.date, experimenter = site.experimenter)

        #Iterate through the clusters, making a new figure for each cluster. 
        for indClust, cluster in enumerate(possibleClusters):

            plt.figure()

            #The first noise burst raster plot
            plt.subplot2grid((4, 6), (0, 0), rowspan = 1, colspan = 3)
            nbIndex = site.get_session_types().index('noiseBurst')
            nbSession = site.get_session_filenames()[nbIndex]
            exp2.plot_session_raster(nbSession, tetrode, cluster = cluster, replace = 1)
            plt.ylabel('Noise Bursts')
            plt.title(nbSession, fontsize = 10)

            #The laser pulse raster plot
            plt.subplot2grid((4, 6), (1, 0), rowspan = 1, colspan = 3)
            lpIndex = site.get_session_types().index('laserPulse')
            lpSession = site.get_session_filenames()[lpIndex]
            exp2.plot_session_raster(lpSession, tetrode, cluster = cluster, replace = 1)
            plt.ylabel('Laser Pulses')
            plt.title(lpSession, fontsize = 10)

            #The laser train raster plot
            plt.subplot2grid((4, 6), (2, 0), rowspan = 1, colspan = 3)
            ltIndex = site.get_session_types().index('laserTrain')
            ltSession = site.get_session_filenames()[ltIndex]
            exp2.plot_session_raster(ltSession, tetrode, cluster = cluster, replace = 1)
            plt.ylabel('Laser Trains')
            plt.title(ltSession, fontsize = 10)

            #The tuning curve
            plt.subplot2grid((4, 6), (0, 3), rowspan = 3, colspan = 3)
            tcIndex = site.get_session_types().index('tuningCurve')
            tcSession = site.get_session_filenames()[tcIndex]
            tcBehavID = site.get_session_behavIDs()[tcIndex]
            exp2.plot_session_tc_heatmap(tcSession, tetrode, tcBehavID, replace = 1, cluster = cluster)
            plt.title('Tetrode {0} Cluster {1}'.format(tetrode, cluster))

            #The best freq presentation
            plt.subplot2grid((4, 6), (3, 0), rowspan=1, colspan=3)
            bfIndex = site.get_session_types().index('bestFreq')
            bfSession = site.get_session_filenames()[bfIndex]
            exp2.plot_session_raster(bfSession, tetrode, cluster = cluster, replace = 1)
            plt.ylabel('Best Frequency')
            plt.title(bfSession, fontsize = 10)

            #FIXME: Omitting the laser pulses at different intensities for now

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
