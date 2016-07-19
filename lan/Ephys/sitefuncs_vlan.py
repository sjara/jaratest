'''
2015-08-01 Nick Ponvert

This module will contain report plotting methods that act on entire sites

Modulated to include function for plotting ephys data during 2afc behavior - Lan.

LG 20151202 modified to use new features for clustering (peak, valleyFirstHalf)
'''
from jaratoolbox.test.lan.Ephys import clusterManySessions_vlan as cms2 #this version uses new features for clustering
reload(cms2)
from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.lan.Ephys import dataplotter_vlan as dataplotter
reload(dataplotter)
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import spikesanalysis
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import numpy as np
import os


def cluster_site(site, siteName, tetrode, report=True): 
    oneTT = cms2.MultipleSessionsToCluster(site.animalName, site.get_session_ephys_filenames(), tetrode, '{}_{}'.format(site.date, siteName))
    oneTT.load_all_waveforms() #LG 20160329 if don't load waveforms, oneTT.timestamps is empty. need a better way to do this 
    
    #Do the clustering if necessary.
    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    
    if os.path.isfile(clusterFile):
        oneTT.set_clusters_from_file()
        
    else:
        oneTT.load_all_waveforms() #load waveforms only if need to cluster
        oneTT.create_multisession_fet_files()
        oneTT.run_clustering()
        oneTT.set_clusters_from_file()

        oneTT.save_single_session_clu_files()
        #LG 2016-03-21 changed this so that  multisession report only generated once during clustering
        if report:
            plt.clf()
            oneTT.save_multisession_report()

    return oneTT #This is a little bit lazy, it should really spit out some attributes not the whole object 


def nick_lan_daily_report(site, siteName, mainRasterInds, mainTCind, mainSTRind):
    '''

    '''

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=np.unique(oneTT.clusters)


        #Iterate through the clusters, making a new figure for each cluster.
        #for indClust, cluster in enumerate([3]):
        for indClust, cluster in enumerate(possibleClusters):
            if mainRasterInds:
                mainRasterEphysFilenames = [site.get_mouse_relative_ephys_filenames()[i] for i in mainRasterInds]
                mainRasterTypes = [site.get_session_types()[i] for i in mainRasterInds]
                mainRasterbehavFilenames = [site.get_mouse_relative_behav_filenames()[i] for i in mainRasterInds]

            if mainTCind or mainTCind==0:
                try:
                    mainTCsession = site.get_mouse_relative_ephys_filenames()[mainTCind]
                    mainTCbehavFilename = site.get_mouse_relative_behav_filenames()[mainTCind]
                    mainTCtype = site.get_session_types()[mainTCind]
                except:
                    mainTCsession=None
            else:
                mainTCsession=None
            
            if mainSTRind:
                mainSTRsession = site.get_mouse_relative_ephys_filenames()[mainSTRind]
                mainSTRbehavFilename = site.get_mouse_relative_behav_filenames()[mainSTRind]
                mainSTRtype = site.get_session_types()[mainSTRind]
            else:
                mainSTRsession=None

            # plt.figure() #The main report for this cluster/tetrode/session
            plt.clf()

            #####0917LG modified to add code specific to plotting sorted the mixed laser&sound rasters (lasersounds paradigm)
            if mainRasterInds:
                for indRaster, rasterSession in enumerate(mainRasterEphysFilenames):
                    plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)
                    rasterSpikes = loader.get_session_spikes(rasterSession, tetrode)
                    spikeTimestamps = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]

                    rasterEvents = loader.get_session_events(rasterSession)
                    eventOnsetTimes = loader.get_event_onset_times(rasterEvents)
                    if mainRasterTypes[indRaster]== 'lasersounds':  
                        laserSoundsbehavFilename=mainRasterbehavFilenames[indRaster]
                        bdata = loader.get_session_behavior(laserSoundsbehavFilename)              
                        laserTrial = bdata['laserTrial']
                        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=laserTrial, timeRange=[-0.5, 1], ms=4, labels=['with laser', 'without laser'])
                    else:
                        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=4)

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

                dataplotter.two_axis_heatmap(spikeTimestamps,
                                            eventOnsetTimes,
                                            intensityEachTrial,
                                            freqEachTrial,
                                            intenLabels,
                                            freqLabels,
                                            xlabel,
                                            ylabel,
                                            plotTitle,
                                            flipFirstAxis=True,
                                            flipSecondAxis=False,
                                            timeRange=[0, 0.1])

                plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)
                #plt.show()
            
            nSpikes = len(oneTT.timestamps)
            nClusters = len(possibleClusters)

            tsThisCluster = oneTT.timestamps[oneTT.clusters==cluster]
            wavesThisCluster = oneTT.samples[oneTT.clusters==cluster]
            # -- Plot ISI histogram --
            plt.subplot2grid((6,6), (4,0), rowspan=1, colspan=3)
            try:
                spikesorting.plot_isi_loghist(tsThisCluster)
                plt.ylabel('c%d'%cluster,rotation=0,va='center',ha='center')
                plt.xlabel('')
            except:
                continue
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
            plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')
            #plt.show()
            # plt.close()

            if mainSTRsession: 
                mainSTRtype = site.get_session_types()[mainSTRind]

                bdata = loader.get_session_behavior(mainSTRbehavFilename)
                plotTitle = loader.get_session_filename(mainSTRsession)
                eventData = loader.get_session_events(mainSTRsession)
                spikeData = loader.get_session_spikes(mainSTRsession, tetrode)

                spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

                eventOnsetTimes = loader.get_event_onset_times(eventData)

                if mainSTRtype == 'tuningCurve':
                    freqEachTrial = bdata['currentFreq']
                    intensityEachTrial = bdata['currentIntensity']

                    possibleFreq = np.unique(freqEachTrial)
                    possibleIntensity = np.unique(intensityEachTrial)

                    xlabel='Time relative to event onset (s)'
                    #ylabel='Intensity (dB SPL)'

                    #freqLabels = ["%.1f" % freq for freq in possibleFreq]#this is amplitude modulation freq for santiago's more sounds paradigm
                    freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0] #freq of sine/chord presented
                    intenLabels = ["%.1f" % inten for inten in possibleIntensity]
                               
                    plt.figure()
                    dataplotter.two_axis_sorted_raster(spikeTimestamps,
                                                eventOnsetTimes,
                                                intensityEachTrial,
                                                freqEachTrial,
                                                intenLabels,
                                                freqLabels,
                                                xlabel,
                                                plotTitle, 
                                                flipFirstAxis=True,
                                                flipSecondAxis=False,
                                                timeRange=[-0.5,1])
                    plt.title("{0}\n{1}".format(mainSTRsession, mainSTRbehavFilename), fontsize = 10)
                    #plt.show()
                    plt.subplots_adjust(wspace = 0.7)
                    fig_path = oneTT.clustersDir
                    fig_name = 'TT{0}Cluster{1}{2}.png'.format(tetrode, cluster, 'sorted_raster_more_sounds')
                    full_fig_path = os.path.join(fig_path, fig_name)
                    print full_fig_path
                    #plt.tight_layout()
                    plt.gcf().set_size_inches((8.5,11))
                    plt.savefig(full_fig_path, format = 'png')

    '''
         if mainSTRtype == 'lasersounds':
                            laserTrial = bdata['laserTrial']
                            plt.figure()
                            dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=laserTrial, timeRange=[-0.5, 1], ms=4, labels=['with laser', 'without laser'])
                            plt.title("{0}\n{1}".format(mainSTRsession, mainSTRbehavFilename), fontsize = 10)
                            #plt.show()
                            plt.subplots_adjust(wspace = 0.7)
                            fig_path = oneTT.clustersDir
                            fig_name = 'TT{0}Cluster{1}{2}.png'.format(tetrode, cluster, 'mixed_laser_sound')
                            full_fig_path = os.path.join(fig_path, fig_name)
                            print full_fig_path
                            #plt.tight_layout()
                            plt.gcf().set_size_inches((8.5,11))
                            plt.savefig(full_fig_path, format='png')
    '''


def am_mod_report(site, siteName, amSessionInd):
    '''

    '''
    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
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


def nick_lan_daily_report_short(site, siteName, mainRasterInds):
    '''

    '''

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=np.unique(oneTT.clusters)


        #Iterate through the clusters, making a new figure for each cluster.
        #for indClust, cluster in enumerate([3]):
        for indClust, cluster in enumerate(possibleClusters):


            mainRasterEphysFilenames = [site.get_mouse_relative_ephys_filenames()[i] for i in mainRasterInds]
            mainRasterTypes = [site.get_session_types()[i] for i in mainRasterInds]
            
            plt.clf()

            for indRaster, rasterSession in enumerate(mainRasterEphysFilenames):
                plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 6)

                rasterSpikes = loader.get_session_spikes(rasterSession, tetrode)
                spikeTimestamps = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]

                rasterEvents = loader.get_session_events(rasterSession)
                eventOnsetTimes = loader.get_event_onset_times(rasterEvents)

                dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=1)

                plt.ylabel('{}\n{}'.format(mainRasterTypes[indRaster], rasterSession.split('_')[1]), fontsize = 10)
                ax=plt.gca()
                extraplots.set_ticks_fontsize(ax,6) #Should this go in dataplotter? 

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
            plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')
            #plt.show()
            # plt.close()




def lan_2afc_ephys_plots(site, siteName, main2afcind, tetrodes):
    '''
    Plot for each cluster in the site, plot a summary for activity during 2afc behavior. spike rasters/psths are algined to sound onset. Data are split into leftward and rightward trials.
    Right now it assumes the behav data is saved under 'lan'(Experiment.experimenter) folder and not 'santiago' folder.
    '''
    SAMPLING_RATE=30000.0
    soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
    binWidth = 0.010 # Size of each bin in histogram in seconds

    #timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
    timeRange = [-0.25,1.0]

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=np.unique(oneTT.clusters)


        #Iterate through the clusters, making a new figure for each cluster.
               
        main2afcsession = site.get_mouse_relative_ephys_filenames()[main2afcind]
        main2afcbehavFilename = site.get_mouse_relative_behav_filenames()[main2afcind]
        #mainTCtype = site.get_session_types()[main2afcind]
            
        bdata = loader.get_session_behavior(main2afcbehavFilename)
        #plotTitle = loader.get_session_filename(main2afcsession)
        eventData = loader.get_session_events(main2afcsession)
        spikeData = loader.get_session_spikes(main2afcsession, tetrode)
        for indClust, cluster in enumerate(possibleClusters):
            spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

            eventOnsetTimes=np.array(eventData.timestamps)  #already divided by SAMPLING_RATE and has seconds as its unit
            #eventOnsetTimes = loader.get_event_onset_times(eventData) #These are already only the sound onset events
            soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
            soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
            
            freqEachTrial = bdata['targetFrequency']
            possibleFreq = np.unique(freqEachTrial)
            
            rightward = bdata['choice']==bdata.labels['choice']['right']
            leftward = bdata['choice']==bdata.labels['choice']['left']
            invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
            correct = bdata['outcome']==bdata.labels['outcome']['correct'] 
            incorrect = bdata['outcome']==bdata.labels['outcome']['error']  

            ######Split left and right trials into correct and  incorrect categories to look at error trials#########
            rightcorrect = rightward&correct
            leftcorrect = leftward&correct
            righterror = rightward&incorrect
            lefterror = leftward&incorrect
            
            # Set this to 1 to plot only correct trials
            #if 1:
                #rightward &= correct
                #leftward &= correct
            
            trialsEachCond = np.c_[invalid,leftcorrect,rightcorrect] 
            colorEachCond = ['0.75','g','r']
            #trialsEachCond = np.c_[invalid,leftcorrect,rightcorrect,lefterror,righterror] 
            #colorEachCond = ['0.75','g','r','b','m'] 

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)

            plt.clf()
            ###########Added more categories of trials to plot, using longer time range#################
            ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
            extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,
                       colorEachCond=colorEachCond,fillWidth=None,labels=None)
            plt.ylabel('Trials')

            #dataplotter.two_axis_sorted_raster(spikeTimestamps, soundOnsetTimes, secondSortArray=trialsEachCond, secondSortLabels=['invalid', 'leftward', 'rightward'], timeRange=timeRange) #this doesn't work because trialsEachCond is a boolean array of shape [nTrials,nConditions]
            

            timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)

            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
            smoothWinSize = 3
            ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)
            extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                     colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

            plt.xlabel('Time from sound onset (s)')
            plt.ylabel('Firing rate (spk/sec)')

            #plt.show()
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}{2}.png'.format(tetrode, cluster, '_2afc plot')
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            #plt.tight_layout()
            #plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')



def lan_2afc_ephys_plots_each_type(site, siteName, main2afcind, tetrodes, trialLimit=[]):
    '''
    Plots ephys data during behavior (reward_change_freq_discrim paradigm), data split according to the type of block in behavior (more_left or more_right) and the choice (left or right). only plotting correct trials.
    '''
    
    SAMPLING_RATE=30000.0
    soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
    binWidth = 0.010 # Size of each bin in histogram in seconds

    #timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
    #timeRange = [-0.25,1.0]
    timeRange = [-0.4,1.2]

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=np.unique(oneTT.clusters)


        #Iterate through the clusters, making a new figure for each cluster.
               
        main2afcsession = site.get_mouse_relative_ephys_filenames()[main2afcind]
        main2afcbehavFilename = site.get_mouse_relative_behav_filenames()[main2afcind]
        #mainTCtype = site.get_session_types()[main2afcind]
        behavDir = '/home/languo/data/behavior/lan/'  #this is specific to lan's mice
        behavFullFilePath = os.path.join(behavDir, main2afcbehavFilename)
        loadingClass = loadbehavior.FlexCategBehaviorData  #using this bdata class so we get 'blocks'
        #bdata = loader.get_session_behavior(main2afcbehavFilename)
        bdata = loadingClass(behavFullFilePath,readmode='full')
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        #blockLabels = ['more_left', 'more_right']
        if(not len(trialLimit)):
            validTrials = np.ones(len(currentBlock),dtype=bool)
        else:
            validTrials = np.zeros(len(currentBlock),dtype=bool)
            validTrials[trialLimit[0]:trialLimit[1]] = 1

        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        
        #plotTitle = loader.get_session_filename(main2afcsession)
        eventData = loader.get_session_events(main2afcsession)
        spikeData = loader.get_session_spikes(main2afcsession, tetrode)
        for indClust, cluster in enumerate(possibleClusters):
            spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

            eventOnsetTimes=np.array(eventData.timestamps)  #already divided by SAMPLING_RATE and has seconds as its unit
            #eventOnsetTimes = loader.get_event_onset_times(eventData) #These are already only the sound onset events
            soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
            soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
            
            freqEachTrial = bdata['targetFrequency']
            possibleFreq = np.unique(freqEachTrial)
            
            rightward = bdata['choice']==bdata.labels['choice']['right']
            leftward = bdata['choice']==bdata.labels['choice']['left']
            invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
            correct = bdata['outcome']==bdata.labels['outcome']['correct'] 
            incorrect = bdata['outcome']==bdata.labels['outcome']['error']  

            ######Split left and right trials into correct and  incorrect categories to look at error trials#########
            rightcorrect = rightward&correct&validTrials
            leftcorrect = leftward&correct&validTrials
            #righterror = rightward&incorrect&validTrials
            #lefterror = leftward&incorrect&validTrials
            
            rightcorrectBlockSameReward = rightcorrect&trialsEachType[:,0]
            rightcorrectBlockMoreLeft = rightcorrect&trialsEachType[:,1] 
            rightcorrectBlockMoreRight = rightcorrect&trialsEachType[:,2]
            leftcorrectBlockSameReward = leftcorrect&trialsEachType[:,0]
            leftcorrectBlockMoreLeft = leftcorrect&trialsEachType[:,1]
            leftcorrectBlockMoreRight = leftcorrect&trialsEachType[:,2]
            
            trialsEachCond = np.c_[leftcorrectBlockMoreLeft,rightcorrectBlockMoreLeft,leftcorrectBlockMoreRight,rightcorrectBlockMoreRight,leftcorrectBlockSameReward,rightcorrectBlockSameReward] 
            
            
            colorEachCond = ['g','r','m','b','y','darkgray']
            #trialsEachCond = np.c_[invalid,leftcorrect,rightcorrect,lefterror,righterror] 
            #colorEachCond = ['0.75','g','r','b','m'] 

            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)

            plt.clf()
            ###########Added more categories of trials to plot, using longer time range#################
            ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
            extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,
                       colorEachCond=colorEachCond,fillWidth=None,labels=None)
            plt.ylabel('Trials')

            #dataplotter.two_axis_sorted_raster(spikeTimestamps, soundOnsetTimes, secondSortArray=trialsEachCond, secondSortLabels=['invalid', 'leftward', 'rightward'], timeRange=timeRange) #this doesn't work because trialsEachCond is a boolean array of shape [nTrials,nConditions]
            

            timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)

            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
            smoothWinSize = 3
            ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)
            extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                     colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

            plt.xlabel('Time from sound onset (s)')
            plt.ylabel('Firing rate (spk/sec)')

            #plt.show()
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}{2}.png'.format(tetrode, cluster, '_2afc plot_each_type')
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            #plt.tight_layout()
            #plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')

def lan_2afc_ephys_plots_each_block_each_type(site, siteName, main2afcind, tetrodes, trialLimit=[], choiceSide='both'):
    '''
    Plots ephys data during behavior (reward_change_freq_discrim paradigm), data split according to the block in behavior and the choice (left or right). only plotting correct trials.
    'site' is a cellDB recording site object.
    'main2afcind' is the index of the recording corresponding to 2afc behavior in the whole list of recordings in this site.
    'trialLimit' (e.g. [0, 600]) is the indecies of trials wish to be plotted.
    'choiceSide' is a string, either 'left' or 'right', to plot leftward and rightward trials, respectively. If not provided, will plot both sides.
    '''
    
    SAMPLING_RATE=30000.0
    soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
    binWidth = 0.010 # Size of each bin in histogram in seconds

    #timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
    #timeRange = [-0.25,1.0]
    timeRange = [-0.4,1.2]

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    main2afcsession = site.get_mouse_relative_ephys_filenames()[main2afcind]
        
    main2afcbehavFilename = site.get_mouse_relative_behav_filenames()[main2afcind]
        
    #mainTCtype = site.get_session_types()[main2afcind]
    behavDir = '/home/languo/data/behavior/lan/'  #this is specific to lan's mice
    behavFullFilePath = os.path.join(behavDir, main2afcbehavFilename)
    loadingClass = loadbehavior.FlexCategBehaviorData  #using this bdata class so we get 'blocks'
    #bdata = loader.get_session_behavior(main2afcbehavFilename)
    bdata = loadingClass(behavFullFilePath,readmode='full')
    currentBlock = bdata['currentBlock']
    '''
    if currentBlock[0]==bdata.labels['currentBlock']['more_left']:
        #startMoreLeft=True
        startBlock='left'
    elif currentBlock[0]==bdata.labels['currentBlock']['same_reward']:
        startBlock='same'
    else:
        #startMoreLeft=False
        startBlock='right'
    '''
    #blockTypes = [bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
    if(not len(trialLimit)):
        validTrials = np.ones(len(currentBlock),dtype=bool)
    else:
        validTrials = np.zeros(len(currentBlock),dtype=bool)
        validTrials[trialLimit[0]:trialLimit[1]] = 1

    bdata.find_trials_each_block()
    trialsEachBlock = bdata.blocks['trialsEachBlock']
    #print trialsEachBlock
    nBlocks = bdata.blocks['nBlocks']

    #blockLabels = ['more_left', 'more_right']
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct'] 
    incorrect = bdata['outcome']==bdata.labels['outcome']['error'] 
######Split left and right trials into correct and  incorrect categories to look at error trials#########
    rightcorrect = rightward&correct&validTrials
    leftcorrect = leftward&correct&validTrials
    #righterror = rightward&incorrect&validTrials
    #lefterror = leftward&incorrect&validTrials
    colorEachCond=[]
    for block in range(nBlocks):
        rightcorrectThisBlock = rightcorrect&trialsEachBlock[:,block]
        leftcorrectThisBlock = leftcorrect&trialsEachBlock[:,block]
        #trialTypeVec = leftcorrect*1+rightcorrect*2
        #trialTypePossibleValues = [1,2] #1 stands for left correct, 2 stands for right correct
        
        firstIndexThisBlock=np.nonzero(trialsEachBlock[:,block])[0][0]
        if currentBlock[firstIndexThisBlock]==bdata.labels['currentBlock']['more_left']:
            if choiceSide=='right':
                colorThisCond='r'
            elif choiceSide=='left':
                colorThisCond='g'
            elif choiceSide=='both':
                colorThisCond=['g','r']
        if currentBlock[firstIndexThisBlock]==bdata.labels['currentBlock']['more_right']:
            if choiceSide=='right':
                colorThisCond='b'
            elif choiceSide=='left':
                colorThisCond='m'
            elif choiceSide=='both':
                colorThisCond=['m','b']
        if currentBlock[firstIndexThisBlock]==bdata.labels['currentBlock']['same_reward']:
            if choiceSide=='right':
                colorThisCond='darkgray'
            elif choiceSide=='left':
                colorThisCond='y'
            elif choiceSide=='both':
                colorThisCond=['y','darkgray']

        #trialsEachTypeEachBlock = behavioranalysis.find_trials_each_type_each_block(trialTypeVec, trialTypePossibleValues,currentBlock,blockTypes)
        
        if block==0:
            #trialsEachCond=np.c_[leftcorrectThisBlock,rightcorrectThisBlock] 
            if choiceSide=='right':
                trialsEachCond=np.c_[rightcorrectThisBlock]
            elif choiceSide=='left':
                trialsEachCond=np.c_[leftcorrectThisBlock]              
            elif choiceSide=='both':
                trialsEachCond=np.c_[leftcorrectThisBlock,rightcorrectThisBlock]
        else:
            if choiceSide=='right':
                trialsEachCond=np.c_[trialsEachCond,rightcorrectThisBlock]
            elif choiceSide=='left':
                trialsEachCond=np.c_[trialsEachCond,leftcorrectThisBlock]              
            elif choiceSide=='both':
                trialsEachCond=np.c_[trialsEachCond,leftcorrectThisBlock,rightcorrectThisBlock]
        
        colorEachCond.append(colorThisCond)
        #print colorEachCond
        '''
        if choiceSide=='right':
            if startMoreLeft:
                colorEachCond=['r','b','r','b','r','b','r','b']
            else:
                colorEachCond=['b','r','b','r','b','r','b','r']
        elif choiceSide=='left':
            if startMoreLeft:
                colorEachCond=['g','m','g','m','g','m','g','m']
            else:
                colorEachCond=['m','g','m','g','m','g','m','g']
        elif choiceSide=='both':
            if startMoreLeft:
                colorEachCond=['g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b']
            else:
                colorEachCond=['m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r','m','b','g','r']
        '''
    for tetrode in tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=np.unique(oneTT.clusters)

        #Iterate through the clusters, making a new figure for each cluster.
     
        #plotTitle = loader.get_session_filename(main2afcsession)
        eventData = loader.get_session_events(main2afcsession)
        spikeData = loader.get_session_spikes(main2afcsession, tetrode)
        for indClust, cluster in enumerate(possibleClusters):
            spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

            eventOnsetTimes=np.array(eventData.timestamps)  #already divided by SAMPLING_RATE and has seconds as its unit
            #eventOnsetTimes = loader.get_event_onset_times(eventData) #These are already only the sound onset events
            soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
            soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
            
            freqEachTrial = bdata['targetFrequency']
            possibleFreq = np.unique(freqEachTrial)
            
            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)

            plt.clf()
            ###########Added more categories of trials to plot, using longer time range#################
            ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
            pRaster,hcond,zline =extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,
                       colorEachCond=colorEachCond,fillWidth=None,labels=None)
            plt.setp(pRaster, ms=0.8)
            plt.ylabel('Trials')

            #dataplotter.two_axis_sorted_raster(spikeTimestamps, soundOnsetTimes, secondSortArray=trialsEachCond, secondSortLabels=['invalid', 'leftward', 'rightward'], timeRange=timeRange) #this doesn't work because trialsEachCond is a boolean array of shape [nTrials,nConditions]
            

            timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)

            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
            smoothWinSize = 3
            ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)
            extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                     colorEachCond=colorEachCond,linestyle=None,linewidth=1.5,downsamplefactor=1)

            plt.xlabel('Time from sound onset (s)')
            plt.ylabel('Firing rate (spk/sec)')

            #plt.show()
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}{2}{3}.png'.format(tetrode, cluster, '_2afc plot_eachblock_eachtype_',choiceSide)
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            #plt.tight_layout()
            #plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')

def lan_2afc_ephys_plots_debug(site, siteName, main2afcind, tetrodes):
    SAMPLING_RATE=30000.0
    soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
    binWidth = 0.010 # Size of each bin in histogram in seconds

    timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    tetrode=tetrodes  #should make this a list

    for tetrode in enumerate(tetrodes):
        oneTT = cluster_site(site, siteName, tetrode)
        #possibleClusters=np.unique(oneTT.clusters)
        cluster=5

        #Iterate through the clusters, making a new figure for each cluster.

        main2afcsession = site.get_mouse_relative_ephys_filenames()[main2afcind]
        main2afcbehavFilename = site.get_mouse_relative_behav_filenames()[main2afcind]
        #mainTCtype = site.get_session_types()[main2afcind]

        bdata = loader.get_session_behavior(main2afcbehavFilename)
        #plotTitle = loader.get_session_filename(main2afcsession)
        eventData = loader.get_session_events(main2afcsession)
        spikeData = loader.get_session_spikes(main2afcsession, tetrode)
        #for indClust, cluster in enumerate(possibleClusters[3]):

        spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

        #eventOnsetTimes=np.array(eventData.timestamps)/SAMPLING_RATE caused error since divided by sampling rate twice.
        eventOnsetTimes=np.array(eventData.timestamps)
        #eventOnsetTimes = loader.get_event_onset_times(eventData) #These are already only the sound onset events
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

        freqEachTrial = bdata['targetFrequency']
        possibleFreq = np.unique(freqEachTrial)

        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left']
        invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
        correct = bdata['outcome']==bdata.labels['outcome']['correct']
        incorrect = bdata['outcome']==bdata.labels['outcome']['error']  

        ######Split left and right trials into correct and  incorrect categories to look at error trials#########
        rightcorrect = rightward&correct
        leftcorrect = leftward&correct
        righterror = rightward&incorrect
        lefterror = leftward&incorrect

        trialsEachCond = np.c_[invalid,leftcorrect,rightcorrect,lefterror,righterror] 
        colorEachCond = ['0.75','g','r','b','m'] 

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
                                                                                 spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)

        plt.clf()

        ax1 =  plt.subplot2grid((3,1), (0, 0), rowspan=2)
        extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,
                   colorEachCond=colorEachCond,fillWidth=None,labels=None)
        plt.ylabel('Trials')
        #plt.ylabel('Trials/n G-leftcorrect, R-rightcorrect, B-lefterror, M-righterror')

        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)

        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
        smoothWinSize = 3
        ax2 = plt.subplot2grid((3,1), (2, 0), sharex=ax1)
        extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,
                 colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

        plt.xlabel('Time from sound onset (s)')
        plt.ylabel('Firing rate (spk/sec)')


        fig_path = oneTT.clustersDir
        fig_name = 'TT{0}Cluster{1}{2}.png'.format(tetrode, cluster, '_2afc plot')
        full_fig_path = os.path.join(fig_path, fig_name)
        print full_fig_path
        #plt.tight_layout()
        plt.gcf().set_size_inches((8.5,11))
        plt.savefig(full_fig_path, format = 'png')
        plt.show()



def nick_lan_daily_report_v2(site, siteName, mainRasterInds, mainTCind):
    '''

    '''

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=np.unique(oneTT.clusters)


        #Iterate through the clusters, making a new figure for each cluster.
        #for indClust, cluster in enumerate([3]):
        
        for indClust, cluster in enumerate(possibleClusters):
            if mainRasterInds:
                mainRasterEphysFilenames = [site.get_mouse_relative_ephys_filenames()[i] for i in mainRasterInds]
                mainRasterTypes = [site.get_session_types()[i] for i in mainRasterInds]
                mainRasterbehavFilenames = [site.get_mouse_relative_behav_filenames()[i] for i in mainRasterInds]

            if mainTCind or mainTCind==0:
                try:
                    mainTCsession = site.get_mouse_relative_ephys_filenames()[mainTCind]
                    mainTCbehavFilename = site.get_mouse_relative_behav_filenames()[mainTCind]
                    mainTCtype = site.get_session_types()[mainTCind]
                except:
                    mainTCsession=None
            else:
                mainTCsession=None
            # plt.figure() #The main report for this cluster/tetrode/session
            plt.clf()

            #####0917LG modified to add code specific to plotting sorted the mixed laser&sound rasters (lasersounds paradigm)
            if mainRasterInds:
                for indRaster, rasterSession in enumerate(mainRasterEphysFilenames):
                    plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)
                    rasterSpikes = loader.get_session_spikes(rasterSession, tetrode)
                    spikeTimestamps = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]

                    rasterEvents = loader.get_session_events(rasterSession)
                    eventOnsetTimes = loader.get_event_onset_times(rasterEvents)
                    if mainRasterTypes[indRaster]== 'lasersounds':  
                        laserSoundsbehavFilename=mainRasterbehavFilenames[indRaster]
                        bdata = loader.get_session_behavior(laserSoundsbehavFilename)              
                        laserTrial = bdata['laserTrial']
                        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=laserTrial, timeRange=[-0.5, 1], ms=4, labels=['with laser', 'without laser'])
                    else:
                        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=4)

                    plt.ylabel('{}\n{}'.format(mainRasterTypes[indRaster], rasterSession.split('_')[1]), fontsize = 10)
                    ax=plt.gca()
                    extraplots.set_ticks_fontsize(ax,6) #Should this go in dataplotter?

            #This is only for tuning with one intensity (usu. done for implanted mouse with 50dB intensity only).
            if mainTCsession:
                plt.subplot2grid((6, 6), (0, 3), rowspan = 3, colspan = 3)


                bdata = loader.get_session_behavior(mainTCbehavFilename)
                plotTitle = loader.get_session_filename(mainTCsession)
                eventData = loader.get_session_events(mainTCsession)
                spikeData = loader.get_session_spikes(mainTCsession, tetrode)

                spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

                eventOnsetTimes = loader.get_event_onset_times(eventData)

                freqEachTrial = bdata['currentFreq']
                #intensityEachTrial = bdata['currentIntensity']

                possibleFreq = np.unique(freqEachTrial)
                #possibleIntensity = np.unique(intensityEachTrial)

                xlabel='Time relative to event onset (s)'
                #ylabel='Intensity (dB SPL)'
              
                freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
                #intenLabels = ["%.1f" % inten for inten in possibleIntensity]

                dataplotter.plot_raster(spikeTimestamps,
                                        eventOnsetTimes,
                                        sortArray=freqEachTrial,
                                        timeRange=[-0.5, 1],
                                        ms=4,
                                        labels=freqLabels)
                plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)
               
            

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
            plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')
            #plt.show()
            # plt.close()

           

   
def plot_report_only_good_clusters(site, siteName, mainRasterInds, mainTCind):
    '''
    Cluster site if not clustered. Plots raster for noiseburst, laserpulase, lasertrain,and tuning for only select clusters that has been added to site.clusterList
    '''

    loader = dataloader.DataLoader('offline', experimenter=site.experimenter)

    for tetrode in site.tetrodes:
        oneTT = cluster_site(site, siteName, tetrode)
        possibleClusters=site.clusterList

        #Iterate through the clusters, making a new figure for each cluster.
        #for indClust, cluster in enumerate([3]):
        
        for indClust, cluster in enumerate(possibleClusters):
            if mainRasterInds:
                mainRasterEphysFilenames = [site.get_mouse_relative_ephys_filenames()[i] for i in mainRasterInds]
                mainRasterTypes = [site.get_session_types()[i] for i in mainRasterInds]
                mainRasterbehavFilenames = [site.get_mouse_relative_behav_filenames()[i] for i in mainRasterInds]

            if mainTCind or mainTCind==0:
                try:
                    mainTCsession = site.get_mouse_relative_ephys_filenames()[mainTCind]
                    mainTCbehavFilename = site.get_mouse_relative_behav_filenames()[mainTCind]
                    mainTCtype = site.get_session_types()[mainTCind]
                except:
                    mainTCsession=None
            
            # plt.figure() #The main report for this cluster/tetrode/session
            plt.clf()

            #####0917LG modified to add code specific to plotting sorted the mixed laser&sound rasters (lasersounds paradigm)
            if mainRasterInds:
                for indRaster, rasterSession in enumerate(mainRasterEphysFilenames):
                    plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)
                    rasterSpikes = loader.get_session_spikes(rasterSession, tetrode)
                    spikeTimestamps = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]

                    rasterEvents = loader.get_session_events(rasterSession)
                    eventOnsetTimes = loader.get_event_onset_times(rasterEvents)
                    if mainRasterTypes[indRaster]== 'lasersounds':  
                        laserSoundsbehavFilename=mainRasterbehavFilenames[indRaster]
                        bdata = loader.get_session_behavior(laserSoundsbehavFilename)              
                        laserTrial = bdata['laserTrial']
                        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=laserTrial, timeRange=[-0.5, 1], ms=4, labels=['with laser', 'without laser'])
                    else:
                        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, ms=4)

                    plt.ylabel('{}\n{}'.format(mainRasterTypes[indRaster], rasterSession.split('_')[1]), fontsize = 10)
                    ax=plt.gca()
                    extraplots.set_ticks_fontsize(ax,6) #Should this go in dataplotter?

            #This is only for tuning with one intensity (usu. done for implanted mouse with 50dB intensity only).
            if mainTCsession:
                plt.subplot2grid((6, 6), (0, 3), rowspan = 3, colspan = 3)


                bdata = loader.get_session_behavior(mainTCbehavFilename)
                plotTitle = loader.get_session_filename(mainTCsession)
                eventData = loader.get_session_events(mainTCsession)
                spikeData = loader.get_session_spikes(mainTCsession, tetrode)

                spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

                eventOnsetTimes = loader.get_event_onset_times(eventData)

                freqEachTrial = bdata['currentFreq']
                #intensityEachTrial = bdata['currentIntensity']

                possibleFreq = np.unique(freqEachTrial)
                #possibleIntensity = np.unique(intensityEachTrial)

                xlabel='Time relative to event onset (s)'
                #ylabel='Intensity (dB SPL)'
              
                freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
                #intenLabels = ["%.1f" % inten for inten in possibleIntensity]

                dataplotter.plot_raster(spikeTimestamps,
                                        eventOnsetTimes,
                                        sortArray=freqEachTrial,
                                        timeRange=[-0.5, 1],
                                        ms=4,
                                        labels=freqLabels)
                plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)
               
            

            nSpikes = len(oneTT.timestamps)
            nClusters = len(possibleClusters)

            tsThisCluster = oneTT.timestamps[oneTT.clusters==cluster]
            wavesThisCluster = oneTT.samples[oneTT.clusters==cluster]
            # -- Plot ISI histogram --
            plt.subplot2grid((6,6), (4,0), rowspan=1, colspan=3)
            spikesorting.plot_isi_loghist(tsThisCluster)
            plt.ylabel('c%d'%cluster.cluster,rotation=0,va='center',ha='center')
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
            fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster.cluster)
            full_fig_path = os.path.join(fig_path, fig_name)
            print full_fig_path
            #plt.tight_layout()
            plt.gcf().set_size_inches((8.5,11))
            plt.savefig(full_fig_path, format = 'png')
            #plt.show()
            # plt.close()
