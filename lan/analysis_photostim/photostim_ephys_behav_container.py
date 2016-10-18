#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Objects and methods for keeping information about recording sites in photostim experiments, including tuning info and behavior (psychometric curve). PhotostimSession object now inherits from cellDB.Experiment object.
Lan Guo 20160803
'''

import numpy as np
import os
import pandas as pd
import pdb
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratest.nick.database import dataloader as loader
from jaratest.nick.database import dataplotter as dataplotter
from jaratest.nick.database import cellDB
from jaratest.lan import test047_group_photostim_psycurve_by_trialtype as photostimPlotter
reload(photostimPlotter)
from jaratest.lan.Ephys import clusterManySessions_vlan as cms2
reload(cms2)


class PhotostimSession(cellDB.Experiment):
    '''
    Object that contains information for a photostim experiment and has methods for plotting data. 
    animalName should be a string.
    date should be a string with format 'year-month-day'.
    ephysSession should be a string containing the timestamp part (can omit the date part of the file name).
    tuningSurffix is the surffix of the behavior session associated with tuning curve, should be a string.
    behavSurffix is the surffix of the photostim_freq_discrim behavior session, should be a string.
    '''
    
    def __init__(self,animalName, date, experimenter='', defaultParadigm='tuning_curve'):
        # -- Basic info --
        self.animalName = animalName
        self.date = date
        self.experimenter = experimenter
        self.defaultParadigm = defaultParadigm
        self.siteList = []

    def add_site(self, depth, tetrodes, stimHemi):
        site = PhotostimSite(animalName=self.animalName,
                             date=self.date,
                             experimenter=self.experimenter,
                             defaultParadigm=self.defaultParadigm,
                             tetrodes=tetrodes,
                             depth=depth,
                             stimHemi=stimHemi)

        self.siteList.append(site)
        return site
            

class PhotostimSite (cellDB.Site):
    '''
    Oject that contain information for a recording site in the photostim experiment. Has methods to cluster 
    '''

    def __init__(self, animalName, date, experimenter, defaultParadigm, tetrodes, stimHemi, depth=0):
        self.depth = depth
        self.stimHemi = stimHemi
        self.tetrodes = tetrodes
        self.animalName = animalName #Provided by Experiment
        self.date = date #Provided by Experiment
        self.experimenter = experimenter #Provided by Experiment
        self.defaultParadigm = defaultParadigm #Provided by Experiment
        self.sessionList = []
        self.clusterDict = [] #Dictionary of good clusters in format: {tetrode:[clusterNumbers]}
        ####I decided not to repeat low-level data loading and plotting methods since they already exist. Instead, in the plotting methods I'm using methods in nick's dataloader and dataplotter #####
        self.loader = loader.DataLoader(mode='offline', animalName=animalName, experimenter='', date=date, paradigm='laser_tuning_curve') #loader's default paradigm is for loading the behav data corresponding to tuning curve 


    def add_session(self, session, behavFileSuffix, sessionType, paradigm=None):
        if not paradigm:
            paradigm = self.defaultParadigm

        if behavFileSuffix:
            # if len(behavFileSuffix)==1: #This is just the suffix - need to add the date
            datestr = ''.join(self.date.split('-'))
            behavFileNameBaseName = '_'.join([self.animalName, paradigm, datestr])
            fullBehavFileName = '{}{}.h5'.format(behavFileNameBaseName, behavFileSuffix)
            # elif len(behavFileSuffix)==9: #Has the date but no paradigm - add the rest ##EDIT: I dont think we need this any more
            #     behavFileNameBaseName = '_'.join([self.animalName, paradigm])
            #     fullBehavFileName = '{}_{}.h5'.format(behavFileNameBaseName, behavFileSuffix)
        else:
            fullBehavFileName=None

        #If we need to record past midnight, just include the date in the session timestamp
        if session == None: #This is changed so that ephysSession can be None.
            ephysSession = None
        elif len(session.split('_'))==2: #Has the date already
            ephysSession = session

        elif len(session.split('_'))==1: #Does not have the date already, assume to be the stored date
            ephysSession = '_'.join([self.date, session])
        

        session = cellDB.Session(ephysSession, fullBehavFileName, sessionType)
        self.sessionList.append(session)
        return session


    def add_clusters(self, clusterDict):
        '''
        Add clusters from many tetrodes at once by passing a dictionary.

        Args:
            clusterDict (dict): A dictionary in the form: {tetrodeNumber: [clusterNumbers]}
        '''
        
        self.clusterDict = clusterDict


    def cluster_photostim_session(self):
        '''
        Method to cluster all ephys sessions for all the tetrodes in a photostim session, now placed in the PhotostimSite object instead of sitefuncs.
        '''
        for tetrode in self.tetrodes:
            oneTT = cms2.MultipleSessionsToCluster(self.animalName, self.get_session_ephys_filenames(), tetrode, self.date) #last argument is used to create cluster report folder

            oneTT.load_all_waveforms()
        
            clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)

            if os.path.isfile(clusterFile):
                oneTT.set_clusters_from_file()

            else:
                #oneTT.load_all_waveforms() #load waveforms only if need to cluster
                oneTT.create_multisession_fet_files()
                oneTT.run_clustering()
                oneTT.set_clusters_from_file()

                oneTT.save_single_session_clu_files()
                #if report:
                    #plt.clf()
                oneTT.save_multisession_report()
    def get_mouse_relative_ephys_filenames(self):
        '''
        This method is modified from Site methods, returns None if session does not have ephys recording.
        '''
        return [os.path.join(self.animalName, fn) if fn else None for fn in self.get_session_ephys_filenames()]


    def raster_reports_all_clusters(self, mainRasterInds, mainTCind):
        '''
        This is method nick_lan_daily_reports_v2 migrated from sitefuncs_vlan

        '''
        for tetrode in self.tetrodes:
            oneTT = cms2.MultipleSessionsToCluster(self.animalName, self.get_session_ephys_filenames(), tetrode, self.date) #last argument is used to create cluster report folder'
            oneTT.set_clusters_from_file()
            possibleClusters=np.unique(oneTT.clusters)

            for indClust, cluster in enumerate(possibleClusters):
                fig_path = oneTT.clustersDir
                fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster)
                full_fig_path = os.path.join(fig_path, fig_name)
                if os.path.exists(full_fig_path):
                    print 'Plot already exists for tetrode %s cluster %s'%(tetrode,cluster)
                    continue  #Do not replot when plot already exists

                if mainRasterInds:
                    mainRasterEphysFilenames = [self.get_mouse_relative_ephys_filenames()[i] for i in mainRasterInds]
                    mainRasterTypes = [self.get_session_types()[i] for i in mainRasterInds]
                    mainRasterbehavFilenames = [self.get_mouse_relative_behav_filenames()[i] for i in mainRasterInds]

                if mainTCind or mainTCind==0:
                    mainTCsession = self.get_mouse_relative_ephys_filenames()[mainTCind]
                    mainTCbehavFilename = self.get_mouse_relative_behav_filenames()[mainTCind]
                    mainTCtype = self.get_session_types()[mainTCind]
                    #except:
                        #mainTCsession=None
                else:
                    mainTCsession=None
                # plt.figure() #The main report for this cluster/tetrode/session
                plt.clf()

                #####0917LG modified to add code specific to plotting sorted the mixed laser&sound rasters (lasersounds paradigm)
                if mainRasterInds:
                    for indRaster, rasterSession in enumerate(mainRasterEphysFilenames):
                        plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)
                        rasterSpikes = self.loader.get_session_spikes(rasterSession, tetrode)
                        spikeTimestamps = rasterSpikes.timestamps[rasterSpikes.clusters==cluster]

                        rasterEvents = self.loader.get_session_events(rasterSession)
                        eventOnsetTimes = self.loader.get_event_onset_times(rasterEvents)
                        if mainRasterTypes[indRaster]== 'lasersounds':  
                            laserSoundsbehavFilename=mainRasterbehavFilenames[indRaster]
                            bdata = self.loader.get_session_behavior(laserSoundsbehavFilename)              
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


                    bdata = self.loader.get_session_behavior(mainTCbehavFilename)
                    plotTitle = self.loader.get_session_filename(mainTCsession)
                    eventData = self.loader.get_session_events(mainTCsession)
                    spikeData = self.loader.get_session_spikes(mainTCsession, tetrode)

                    spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]

                    eventOnsetTimes = self.loader.get_event_onset_times(eventData)

                    freqEachTrial = bdata['currentFreq']
                    intensityEachTrial = bdata['currentIntensity']
                    #If presented more than one intensity, just use the one used in task(should be 50dB in tuning with Chords)
                    if len(np.unique(intensityEachTrial))>1:
                        intensity = 50.0
                    else:
                        intensity = np.unique(intensityEachTrial)
                    ###Just select the trials with a given intensity###
                    trialsThisIntensity = [intensityEachTrial==intensity]
                    freqEachTrial = freqEachTrial[trialsThisIntensity]
                    intensityEachTrial = intensityEachTrial[trialsThisIntensity]
                    eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

                    possibleFreq = np.unique(freqEachTrial)
                    #possibleIntensity = np.unique(intensityEachTrial)
                    #print numt
                    xlabel='Time relative to event onset (s)'
                    #ylabel='Intensity (dB SPL)'

                    freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
                    #intenLabels = ["%.1f" % inten for inten in possibleIntensity]

                    ####This will fail with multiple intensities??
                    dataplotter.plot_raster(spikeTimestamps,
                                            eventOnsetTimes,
                                            sortArray=freqEachTrial,
                                            timeRange=[-0.5, 1],
                                            ms=4,
                                            labels=freqLabels)
                    plt.title("{0}\n{1}".format(mainTCsession, mainTCbehavFilename), fontsize = 10)


                oneTT.load_all_waveforms()
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
                #fig_path = oneTT.clustersDir
                #fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster)
                #full_fig_path = os.path.join(fig_path, fig_name)
               
                #plt.tight_layout()
                plt.gcf().set_size_inches((8.5,11))
                plt.savefig(full_fig_path, format = 'png')
                #plt.show()
                # plt.close()
                print 'saving to %s'%full_fig_path



    def get_tuning_spiketimes_good_clusters(self,tetrode,mainTCind):
        '''
        Get spikeTimestamps for a tetrode, if added good clusters in the site(self) then only include spikes from those clusters. 
        '''
        ephysSession = os.path.join(self.animalName, self.get_session_ephys_filenames()[mainTCind])
        spikeData = self.loader.get_session_spikes(ephysSession,tetrode)
        
        # -- If selected good clusters for this tetrode, only include spikes from these clusters -- #
        try: 
            goodClusterNumbers = self.clusterDict[tetrode]
            spikeTimestamps=spikeData.timestamps
            spikeMask = np.zeros(len(spikeTimestamps),dtype=bool)
            for goodClusterNum in goodClusterNumbers:
                spikeMask = spikeMask | (spikeData.clusters==goodClusterNum)
            spikeTimestamps = spikeTimestamps[spikeMask]
        except KeyError:
            print 'There are no clusters selected!'
            goodClusterNumbers = '[all]'
            spikeTimestamps=spikeData.timestamps
        
        return (spikeTimestamps,goodClusterNumbers)

    def plot_tuning_raster_one_intensity_good_clusters(self,tetrode,mainTCind,intensity=50.0):
        '''
        Method for plotting tuning raster for only selected clusters at one site. Just plotting one frequency since plotting several intensity requires subplot inside subplots, the code breaks. Plotting tetrodes that are in the same hemi as the hemi receiving photostim during behavior if given the corresponding tetrodes when initiating PhotostimSession object.
        Args:
        tetrode is a integer giving the tetrode number.
        mainTCind is a integer giving the index of the tuning session in Site.sessionList.
        intensity is a float giving the tuning intensity(in dB) to plot.
         
        '''
        #ephysSession = self.loader.get_session_filename(self.ephysSession)
        #numTetrodes = len(self.tetrodes)
        ephysSession = os.path.join(self.animalName, self.get_session_ephys_filenames()[mainTCind])
        behavSession = self.get_mouse_relative_behav_filenames()[mainTCind]
        TCtype = self.get_session_types()[mainTCind]
        
        ### Get behavior data associated with tuning curve ###
        #bdata = self.loader.get_session_behavior(self.tuningSession)
        bdata = self.loader.get_session_behavior(behavSession)
        ### Get events data ###
        eventData = self.loader.get_session_events(ephysSession)
        ### Get event onset times ###
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        ### Get spike data for each tetrode and plot tuning
        #for indt, tetrode in enumerate(self.tetrodes):
        #plt.subplot2grid((numTetrodes,1),(indt,0),colspan=1)
            
        (spikeTimestamps,goodClusterNumbers)=self.get_tuning_spiketimes_good_clusters(tetrode,mainTCind)

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)
        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        intensityLabels = ['{:.0f} dB'.format(intensity) for intensity in possibleIntensity]        
        xlabel="Time from sound onset (sec)"
        #plotTitle = ephysSession+'tuning with chords'
        plotTitle = 'Tt'+str(tetrode)+'c'+str(goodClusterNumbers)+' tuning with chords'
        timeRange = [-0.5,1]
        
        dataplotter.plot_raster(spikeTimestamps,
                                eventOnsetTimes,
                                sortArray=freqEachTrial,
                                timeRange=timeRange,
                                ms=3,
                                labels=freqLabels)
        plt.title(plotTitle)
        #plt.show()     


    def plot_photostim_psycurve(self,main2afcind): 
        '''
        Method for plotting psychometric curve for 2afc paradigm. 
        Plots separate curves for trials with and without laser/photo stim. Can plot average psy curve if given more than one behavior sessions.
        Args:
            main2afcind is an integer indicating the index of the 2afc session in site.sessionList.
        '''
        behavSession = self.get_session_behav_filenames()[main2afcind]
        session = [behavSession.split('_')[2].strip('.h5')]
        
        #print session
        photostimPlotter.plot_ave_photostim_psycurve_by_trialtype(self.animalName, session)

   
    def fit_psycuve(self):
        '''
        Fit psycometric curve with pypsignifit BootstrapInference class (using 'ab' core and 'logistic' sigmoid function.
        Using constraints silently inside (not ideal): list of four distributions (can be 'unconstrained') for alpha, beta, lapse, guess, respectively; used in fitting to constrain the position of the curve.
        '''
        import pypsignifit as psi        
        main2afcind = self.get_session_types().index('2afc')
        behavSession = self.get_session_behav_filenames()[main2afcind]
        session = [behavSession.split('_')[2].strip('.h5')]
        bdata = behavioranalysis.load_many_sessions(self.animalName,session)
        targetFrequency=bdata['targetFrequency']
        choice=bdata['choice']
        valid=bdata['valid'] & (choice!=bdata.labels['choice']['none'])
        choiceRight = choice==bdata.labels['choice']['right']

        trialType = bdata['trialType']
        stimTypes = [bdata.labels['trialType']['no_laser'],bdata.labels['trialType']['laser_left'],bdata.labels['trialType']['laser_right']]
        stimLabels = ['no_laser','laser_left','laser_right']
        trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
        nStimTypes = len(stimTypes)
        curveParamDf = pd.DataFrame()
        for stimType in range(nStimTypes):
            if np.any(trialsEachType[:,stimType]):
                targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
                validThisBlock = valid[trialsEachType[:,stimType]]
                choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]
                # -- Calculate and plot psychometric points --
                (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
            behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)

                logPossibleValues = np.log2(possibleValues)

            # -- Calculate and plot psychometric fit --
                constraints = ['Uniform({},{})'.format(logPossibleValues[0],logPossibleValues[-1]), 'unconstrained' ,'unconstrained', 'unconstrained']
                # -- Fit psy curve with psi.BoostrapInference object -- #
                data = np.c_[logPossibleValues,nHitsEachValue,nTrialsEachValue]
                # linear core 'ab': (x-a)/b; logistic sigmoid: 1/(1+np.exp(-(xval-alpha)/beta))
                psyCurveInference = psi.BootstrapInference(data,sample=False, sigmoid='logistic', core='ab',priors=constraints, nafc=1)
                curveParams = psyCurveInference.estimate
                deviance = psyCurveInference.deviance
                predicted = psyCurveInference.predicted
                (alpha, beta, lapse, guess) = list(curveParams)
                curveParamDf = curveParamDf.append({'animal':self.animalName,'session':self.date,'photostim':stimLabels[stimType],'bias':alpha,'slope':beta,'upper':(1-lapse)*100,'lower':100*guess},ignore_index=True)
         
        return curveParamDf       
    

    def plot_tuning_heatmap_one_tetrode(self,tetrode,mainTCind):
        '''
        Method for plotting heatmap for multiunit tuning at one site. 
        Plotting tetrodes that are in the same hemi as the hemi receiving photostim during behavior if given the corresponding tetrodes when initiating PhotostimSession object. 
        '''
        #ephysSession = self.loader.get_session_filename(self.ephysSession)
        #numTetrodes = len(self.tetrodes)
        #gs = gridspec.GridSpec(1,numTetrodes)
       
        ephysSession = os.path.join(self.animalName, self.get_session_ephys_filenames()[mainTCind])
        behavSession = self.get_mouse_relative_behav_filenames()[mainTCind]
        TCtype = self.get_session_types()[mainTCind]
        
        ### Get behavior data associated with tuning curve ###
        #bdata = self.loader.get_session_behavior(self.tuningSession)
        bdata = self.loader.get_session_behavior(behavSession)
        
        ### Get events data ###
        eventData = self.loader.get_session_events(ephysSession)
        ### Get event onset times ###
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        ### Get spike data for each tetrode and plot tuning
        #for indt, tetrode in enumerate(self.tetrodes):
        #plt.subplot2grid((numTetrodes,1),(indt,0),colspan=1)
            
        spikeData = self.loader.get_session_spikes(ephysSession,tetrode)
        spikeTimestamps=spikeData.timestamps
        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)
        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        intensityLabels = ['{:.0f} dB'.format(intensity) for intensity in possibleIntensity]
        #xLabel="Time from sound onset (sec)"
        xlabel='Frequency (kHz)'
        ylabel='Intensity (dB SPL)'
        #plotTitle = ephysSession+'tuning with chords'
        plotTitle = 'Tt'+str(tetrode)+' tuning with chords'
        timeRange = [0,0.1]

        dataplotter.two_axis_heatmap(spikeTimestamps,
                                     eventOnsetTimes,
                                     firstSortArray=intensityEachTrial,
                                     secondSortArray=freqEachTrial,
                                     firstSortLabels=intensityLabels,
                                     secondSortLabels=freqLabels,
                                     xlabel=xlabel,
                                     ylabel=ylabel,
                                     plotTitle=plotTitle,
                                     flipFirstAxis=True,
                                     flipSecondAxis=False,
                                     timeRange=timeRange)


    def plot_tuning_raster_one_intensity_tetrode(self,tetrode,intensity,mainTCind):
        '''
        Method for plotting raster for multiunit tuning at one site. Just plotting one frequency since plotting several intensity requires subplot inside subplots, the code breaks. 
        Takes an argument giving the tuning intensity(in dB) to plot, this should be a float.
        Plotting tetrodes that are in the same hemi as the hemi receiving photostim during behavior if given the corresponding tetrodes when initiating PhotostimSession object. 
        '''
      
        #ephysSession = self.loader.get_session_filename(self.ephysSession)
        #numTetrodes = len(self.tetrodes)
        
        ephysSession = os.path.join(self.animalName, self.get_session_ephys_filenames()[mainTCind])
        behavSession = self.get_mouse_relative_behav_filenames()[mainTCind]
        TCtype = self.get_session_types()[mainTCind]
        
        ### Get behavior data associated with tuning curve ###
        #bdata = self.loader.get_session_behavior(self.tuningSession)
        bdata = self.loader.get_session_behavior(behavSession)

        ### Get events data ###
        eventData = self.loader.get_session_events(ephysSession)
        ### Get event onset times ###
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        ### Get spike data for each tetrode and plot tuning
        #for indt, tetrode in enumerate(self.tetrodes):
        #plt.subplot2grid((numTetrodes,1),(indt,0),colspan=1)
            
        spikeData = self.loader.get_session_spikes(ephysSession,tetrode)
        spikeTimestamps=spikeData.timestamps

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)
        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        intensityLabels = ['{:.0f} dB'.format(intensity) for intensity in possibleIntensity]        
        xlabel="Time from sound onset (sec)"
        #plotTitle = ephysSession+'tuning with chords'
        plotTitle = 'Tt'+str(tetrode)+' tuning with chords'
        timeRange = [-0.5,1]
        '''
        dataplotter.two_axis_sorted_raster(spikeTimestamps,
                                           eventOnsetTimes,
                                           firstSortArray=freqEachTrial,
                                           secondSortArray=intensityEachTrial,
                                           firstSortLabels=freqLabels,
                                           secondSortLabels=intensityLabels,
                                           xLabel=xlabel,
                                           yLabel=ylabel,
                                           plotTitle=plotTitle,
                                           flipFirstAxis=False,
                                           flipSecondAxis=True,
                                           timeRange=timeRange,
                                           ms=2)
        '''
        dataplotter.plot_raster(spikeTimestamps,
                                eventOnsetTimes,
                                sortArray=freqEachTrial,
                                timeRange=timeRange,
                                ms=3,
                                labels=freqLabels)
        plt.title(plotTitle)
        #plt.show()
   
    def daily_report(self, mainTCind, main2afcind):
        '''
        Daily report produced after clustering and selecting good clusters. Includes tuning raster for only the tetrodes with good clusters in the site and 2afc psy curve by condition.
        '''
        plt.subplots(figsize=(20, 8))
        plt.clf()
        #plt.title('%s %s %s hemi depth=%d' %(self.animalName, self.date, self.stimHemi, self.depth))
        tetrodes = self.clusterDict.keys()
        numberTetrodes=len(tetrodes) 
        for ind,tetrode in enumerate(tetrodes):
            plt.subplot2grid((3,3*(numberTetrodes+1)+1),(0,ind*3),colspan=3,rowspan=2)
            self.plot_tuning_raster_one_intensity_good_clusters(tetrode,mainTCind,intensity=50.0)
            plt.ylabel('Freqs (kHz)')
            plt.subplot2grid((3,3*(numberTetrodes+1)+1),(2,ind*3),colspan=3,rowspan=1)
            self.plot_tuning_response_stats(mainTCind,tetrode,intensity=50.0,baseRange=[-0.050,-0.025],binEdges=[0,0.025,0.05,0.075,0.1],maxZthreshold=2,aveTimeRange=[0,0.125])
            plt.title('Average response and maxZ during sound')
        plt.hold(True)
        plt.subplot2grid((3,3*(numberTetrodes+1)+1),(0,3*numberTetrodes),colspan=4,rowspan=3)
        self.plot_photostim_psycurve(main2afcind)
        plt.tight_layout()
        #plt.subplots_adjust(hspace=0.25, wspace=0.6)
        plt.subplots_adjust(top=0.88)    
        plt.suptitle('%s %s %s hemi depth=%d' %(self.animalName, self.date, self.stimHemi, self.depth),fontsize=15)

        outputDir=os.path.join('/home/languo/data/behavior_reports',self.animalName+'select_clusters') 
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        filename = 'tuning_behavior_summary_%s_%s_selectClusters.%s'%(self.animalName,self.date,'png')
        fullFileName = os.path.join(outputDir,filename)
        print 'saving figure to %s'%fullFileName
        plt.gcf().savefig(fullFileName)
        plt.close()


    def ave_std_event_locked_spike_per_cond(self,spikeTimestamps, eventOnsetTimesThisCond, aveTimeRange=[0,0.125]):
        '''
        Calculates average number of spikes in a time range for a given condition.
        Args:
        spikeTimeStamps: (np.array) the time of each spike.
        eventOnsetTimes: (np.array) the time of each instance of the event to lock to, in the condition of interest.
        timeRange:(list or np.array) two-element array specifying time-range to extract spikes around event. usually [0,0.1] for sound presentation.
        
        '''
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimesThisCond,aveTimeRange)
        numSpikesEachTrialThisCond = np.diff(indexLimitsEachTrial, axis=0)
        aveSpikesThisCond = np.mean(numSpikesEachTrialThisCond,dtype=float)
        sdSpikesThisCond = np.std(numSpikesEachTrialThisCond,dtype=float)
        return (aveSpikesThisCond, sdSpikesThisCond)
        

    def estimate_responsive_freq_range_tuning(self,mainTCind,tetrode,intensity=50.0,baseRange=[-0.050,-0.025],binEdges=[0,0.025,0.05,0.075,0.1],aveTimeRange=[0,0.125],maxZthreshold=2):
        '''
        Method for estimating the most responsive frequency range presented in tuning session based on response Z score (calculated with baseline=[-0.05,-0.025] and timeRange=[0,0.1] in 4 bins). 
        Returns (as a dictionary) frequency, maxZ, pvalue, and average spikes in sound-presentation window for each frequency. Also returns the frequencies that passed maxZ threshold (as specified in maxZthreshold argument).
        '''
        ephysSession = os.path.join(self.animalName, self.get_session_ephys_filenames()[mainTCind])
        behavSession = self.get_mouse_relative_behav_filenames()[mainTCind]
       
        ### Get behavior data associated with tuning curve ###
        bdata = self.loader.get_session_behavior(behavSession)
        ### Get events data ###
        eventData = self.loader.get_session_events(ephysSession)
        ### Get event onset times ###
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)
        ### Get spike data for each tetrode and plot tuning
        # -- WATCH OUT: get_tuning_spiketimes_good_clusters returns spikeTimestamps and goodClusterNumbers  
        (spikeTimestamps, goodClusterNumbers)=self.get_tuning_spiketimes_good_clusters(tetrode,mainTCind)
        
        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        # -- check to see if ephys and behavior have the same number of trials -- #
        if len(eventOnsetTimes) == (len(freqEachTrial)+1):
            eventOnsetTimes = eventOnsetTimes[:-1]
            print 'Warning: ephys and behavior donot have same number of trials! Using bad hack to remove last trial in ephys'
        
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        #intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

        possibleFreq = np.unique(freqEachTrial)
        numberOfFrequencies = len(possibleFreq)
        
        #responseDict = {'Freq':np.array([]),'GoodClusters':np.array([]),'Ave_spikes':np.array([]),'Std_spikes':np.array([]),'maxZ':np.array([]),'pValue':np.array([])}
        response_df = pd.DataFrame(columns=['tetrode','good_clusters','freq','maxZ','ave_spike','std_spike'])
        
        for Frequency in range(numberOfFrequencies):
            Freq = possibleFreq[Frequency]
            oneFreqTrials = freqEachTrial == Freq
            oneFreqEventOnsetTimes = eventOnsetTimes[oneFreqTrials] #Choose only the trials with this frequency
            #soundWindow = aveTimeRange #Made sound window bigger to include offset response
            # - Calculate average number of spikes in time-presentation window for this frequency - #
            (aveSpikes,stdSpikes) = self.ave_std_event_locked_spike_per_cond(spikeTimestamps, oneFreqEventOnsetTimes, aveTimeRange)
            #print aveSpikes,stdSpikes

            # - Calculate Z score and stats for this frequency - #
            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,oneFreqEventOnsetTimes,timeRange=[-0.3,0.7])
            (zStats,pValue,maxZValue) = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange=baseRange, binEdges=binEdges)

            response_df = response_df.append({'tetrode':tetrode,'good_clusters':goodClusterNumbers,'freq':Freq,'maxZ':maxZValue,'ave_spike':aveSpikes,'std_spike':stdSpikes}, ignore_index=True)
            #print num
        
        highestAveSpikesFreq = response_df['freq'][np.argmax(response_df['ave_spike'])]
        responsive = (np.abs(response_df['maxZ']) >= maxZthreshold)
        if np.any(responsive):
            responsiveFreqs = response_df['freq'][responsive]   
        else:
            responsiveFreqs = None
        return (response_df, responsiveFreqs, highestAveSpikesFreq)


    def plot_tuning_response_stats(self,mainTCind,tetrode,intensity=50.0,baseRange=[-0.050,-0.025],binEdges=[0,0.025,0.05,0.075,0.1],aveTimeRange=[0,0.125],maxZthreshold=2):
        (response_df, responsiveFreqs, highestAveSpikesFreq) = self.estimate_responsive_freq_range_tuning(mainTCind,tetrode,intensity,baseRange,binEdges,aveTimeRange,maxZthreshold)
        freqs, aveSpikes, stdSpikes, maxZ = np.split(response_df.ix[:,['freq','ave_spike','std_spike','maxZ']].values,4,1)
         
        #plot mean and std of spike number during sound, freqs on log scale
        plt.errorbar(freqs.flatten(), aveSpikes.flatten(), yerr=stdSpikes.flatten(), fmt='-o',linewidth=2)
        plt.ylabel('Ave spikes (%s to %ssec)'%(aveTimeRange[0],aveTimeRange[-1]),color='blue')
        #Set x axis (frequency on log scale base 2)
        plt.xscale('log',base=2)
        #on a different y axis plot maxZ score
        ax2 = plt.twinx()
        plt.plot(freqs, maxZ, color='gray',linewidth=2) 
        plt.ylabel('maxZ score during sound',color='gray')
        #ax = plt.gca()
        plt.xticks(freqs.flatten(),['%.1f'%(freq/1000) for freq in freqs.flatten()], rotation=90)
        plt.tick_params(axis='x',labelsize='small')
        plt.xlabel('Freq (kHz)')
        plt.subplots_adjust(bottom=0.25)
        plt.axhline(y=2, linestyle='dashed', linewidth=0.7, color='black')
        #xmin,xmax,ymin,ymax = plt.axis()
        #if np.any(responsiveFreqs):
        #    plt.text(0.5*(xmin+xmax), 0.5*(ymin+ymax),('responsive freqs:\n'+str(['%s'%freq for freq in responsiveFreqs]))+'\n'+str(highestAveSpikesFreq), color='r')
        #plt.show()


    def calculate_percent_correct_each_freq_each_cond(self):
        '''
        Method to calculate percent of correct trials for each frequency presented in the 2afc task in each stimulation conditions.

        '''
        main2afcind = self.get_session_types().index('2afc')
        behavSession = self.get_session_behav_filenames()[main2afcind]
        session = [behavSession.split('_')[2].strip('.h5')]
        allBehavDataThisAnimal = behavioranalysis.load_many_sessions(self.animalName,session)
        targetFrequency = allBehavDataThisAnimal['targetFrequency']
        choice=allBehavDataThisAnimal['choice']
        valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])

        choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
        trialType = allBehavDataThisAnimal['trialType']
        stimTypes = [allBehavDataThisAnimal.labels['trialType']['no_laser'],allBehavDataThisAnimal.labels['trialType']['laser_left'],allBehavDataThisAnimal.labels['trialType']['laser_right']]
        stimLabels = ['no_laser','laser_left','laser_right']

        trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
        #trialsEachType=np.vstack(( ( (trialType==0) | (trialType==2) ),trialType==1, np.zeros(len(trialType),dtype=bool) )).T  ###This is a hack when percentLaserTrials were sum of both sides and just did one side stim
        #print trialsEachType

        nStimeTypes = len(stimTypes)
        percentCorrectEachFreqEachCond = pd.DataFrame()
        import math
        for stimType in range(nStimeTypes):
            if np.any(trialsEachType[:,stimType]):
                targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
                validThisBlock = valid[trialsEachType[:,stimType]]
                choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]

                (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                                                                                                        behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)\
                                                                                                        
                numFreqs = len(possibleValues)
                
                fractionCorrectLeftFreqs = 1-np.array(fractionHitsEachValue[:int(math.floor(0.5*numFreqs))])
                fractionCorrectRightFreqs = np.array(fractionHitsEachValue[int(math.ceil(0.5*numFreqs)):])
                percentCorrectEachFreqEachCond.loc[:,'percentCorrect_%s'%(stimLabels[stimType])]=np.append(fractionCorrectLeftFreqs,fractionCorrectRightFreqs)
        percentCorrectEachFreqEachCond.loc[:,'freqs']=possibleValues

        return percentCorrectEachFreqEachCond
        

    def calculate_percent_rightward_each_freq_each_cond(self):
        '''
        Method to calculate percent of correct trials for each frequency presented in the 2afc task in each stimulation conditions.

        '''
        main2afcind = self.get_session_types().index('2afc')
        behavSession = self.get_session_behav_filenames()[main2afcind]
        session = [behavSession.split('_')[2].strip('.h5')]
        allBehavDataThisAnimal = behavioranalysis.load_many_sessions(self.animalName,session)
        targetFrequency = allBehavDataThisAnimal['targetFrequency']
        choice=allBehavDataThisAnimal['choice']
        valid=allBehavDataThisAnimal['valid']& (choice!=allBehavDataThisAnimal.labels['choice']['none'])

        choiceRight = choice==allBehavDataThisAnimal.labels['choice']['right']
        trialType = allBehavDataThisAnimal['trialType']
        stimTypes = [allBehavDataThisAnimal.labels['trialType']['no_laser'],allBehavDataThisAnimal.labels['trialType']['laser_left'],allBehavDataThisAnimal.labels['trialType']['laser_right']]
        stimLabels = ['no_laser','laser_left','laser_right']

        trialsEachType = behavioranalysis.find_trials_each_type(trialType,stimTypes)
        #trialsEachType=np.vstack(( ( (trialType==0) | (trialType==2) ),trialType==1, np.zeros(len(trialType),dtype=bool) )).T  ###This is a hack when percentLaserTrials were sum of both sides and just did one side stim
        #print trialsEachType

        nStimeTypes = len(stimTypes)
        percentRightwardEachFreqEachCond = pd.DataFrame()
        import math
        for stimType in range(nStimeTypes):
            if np.any(trialsEachType[:,stimType]):
                targetFrequencyThisBlock = targetFrequency[trialsEachType[:,stimType]]    
                validThisBlock = valid[trialsEachType[:,stimType]]
                choiceRightThisBlock = choiceRight[trialsEachType[:,stimType]]

                (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
                                                                                                        behavioranalysis.calculate_psychometric(choiceRightThisBlock,targetFrequencyThisBlock,validThisBlock)\
    
                numFreqs = len(possibleValues)
                
                percentRightwardEachFreqEachCond.loc[:,'percentRightward_%s'%(stimLabels[stimType])]=fractionHitsEachValue
        percentRightwardEachFreqEachCond.loc[:,'freqs']=possibleValues

        return percentRightwardEachFreqEachCond



    def calculate_ave_percent_correct_lhfreqs_each_cond(self):
        '''
        Function that takes a PhotostimSite objects. Calculates the average percent correct for the low and high freqs under no stim and stim conditions.
        '''
        avePercentCorrectByTypeByFreq = pd.DataFrame(columns=['freq_label','stim_type','ave_performance_baseline','ave_performance_stim'])
        import math
        percentCorrectDf = self.calculate_percent_correct_each_freq_each_cond()
        #percentCorrectDf always has three columns with the last one being 'freqs', first two would be 'percentCorrect_no_laser' and 'percentCorrect_laser_left' or 'percentCorrect_laser_right'
        numFreq = len(percentCorrectDf['freqs'])
        noStimPerf = percentCorrectDf['percentCorrect_no_laser']
        avePercentCorrectNoStim = np.append(np.mean(noStimPerf[:int(math.floor(0.5*numFreq))]),np.mean(noStimPerf[int(math.ceil(0.5*numFreq)):]))

        try:
            stimPerf = percentCorrectDf['percentCorrect_laser_right']
            stimType = ['right','right']
        except KeyError:
            stimPerf = percentCorrectDf['percentCorrect_laser_left']
            stimType = ['left','left']

        avePercentCorrectStim = np.append(np.mean(stimPerf[:int(math.floor(0.5*numFreq))]),
                                                      np.mean(stimPerf[int(math.ceil(0.5*numFreq)):]))

        freqLabel = ['low','high']
        avePercentCorrectByTypeByFreq = pd.concat([avePercentCorrectByTypeByFreq, pd.DataFrame({'freq_label':freqLabel,'stim_type':stimType,'ave_performance_baseline':avePercentCorrectNoStim,'ave_performance_stim':avePercentCorrectStim})], ignore_index=True)
        return avePercentCorrectByTypeByFreq
    

    def calculate_ave_percent_rightward_lhfreqs_each_cond(self):
        '''
        Function that takes a PhotostimSite objects. Calculates the average percent correct for the low and high freqs under no stim and stim conditions.
        '''
        avePercentRightwardByTypeByFreq = pd.DataFrame(columns=['freq_label','stim_type','ave_performance_baseline','ave_performance_stim'])
        import math
        percentRightwardDf = self.calculate_percent_rightward_each_freq_each_cond()
        #percentRightwardDf always has three columns with the last one being 'freqs', first two would be 'percentRightward_no_laser' and 'percentRightward_laser_left' or 'percentRightward_laser_right'
        numFreq = len(percentRightwardDf['freqs'])
        noStimPerf = percentRightwardDf['percentRightward_no_laser']
        avePercentRightwardNoStim = np.append(np.mean(noStimPerf[:int(math.floor(0.5*numFreq))]),np.mean(noStimPerf[int(math.ceil(0.5*numFreq)):]))

        try:
            stimPerf = percentRightwardDf['percentRightward_laser_right']
            stimType = ['right','right']
        except KeyError:
            stimPerf = percentRightwardDf['percentRightward_laser_left']
            stimType = ['left','left']

        avePercentRightwardStim = np.append(np.mean(stimPerf[:int(math.floor(0.5*numFreq))]),
                                                      np.mean(stimPerf[int(math.ceil(0.5*numFreq)):]))

        freqLabel = ['low','high']
        avePercentRightwardByTypeByFreq = pd.concat([avePercentRightwardByTypeByFreq, pd.DataFrame({'freq_label':freqLabel,'stim_type':stimType,'ave_performance_baseline':avePercentRightwardNoStim,'ave_performance_stim':avePercentRightwardStim})], ignore_index=True)
        return avePercentRightwardByTypeByFreq



    def task_freq_distance_to_best_freq(self,bestFreq):
        pass
    
    

#######################################################################################################
# -- Multi-site methods -- #
def paired_dot_plot_with_lines(y1,y2,**kwargs):
    '''
    Given two columns in a dataframe with each row containing paired observations, generate dot plot for each category and link the pair of dots by a line segment.
    '''
    ax = plt.gca()
    #nCategories = ndarray.shape[1]
    #nObservations = ndarray.shape[0]
    #nCategories = 2
    nObservations = len(y1)
    xs=[]
    ys=[]
    #for colNum in range(0, nCategories):
    x=np.tile(1, nObservations)
    y=y1.values
    ax.plot(x,y,'o')
    xs.append(x)
    ys.append(y)
    x=np.tile(2, nObservations)
    y=y2.values
    ax.plot(x,y,'o')
    xs.append(x)
    ys.append(y)
    ax.plot(xs,ys,linewidth=1.5,color='k')  
    plt.xlim(0.8,2.2)
    
def paired_dot_plot_with_lines_df(df,**kwargs):
    '''
    Given a dataframe with each row containing paired observations, generate dot plot for each category and link the pair of dots by a line segment.
    '''
    ax = plt.gca()
    ndarray = df.values
    nCategories = ndarray.shape[1]
    nObservations = ndarray.shape[0]
    xs=[]
    ys=[]
    for colNum in range(0, nCategories):
        x=np.tile(colNum+1, nObservations)
        y=ndarray[:,colNum]
        ax.plot(x,y,'o')
        xs.append(x)
        ys.append(y)
    ymask = np.isfinite(ys)
    #pdb.set_trace()
    ax.plot(xs[ymask],ys[ymask],linewidth=1.5,color='k')    
    

def plot_ave_performance_lhfreqs_each_cond(avePercentPerfByTypeByFreq):
    '''
    Takes a dataframe containing 
    '''
    import seaborn as sns
    import matplotlib
    import matplotlib.pyplot as plt
    plt.style.use(['seaborn-white', 'seaborn-talk'])             
    font={'family':"sans-serif",'size':18}
    matplotlib.rc("font", **font)

    #sns.set(font='serif')
    g = sns.FacetGrid(avePercentPerfByTypeByFreq, row="stim_type", col="freq_label", margin_titles=True)
    g=(g.map(paired_dot_plot_with_lines,'ave_performance_baseline','ave_performance_stim').set(xlim=(0.5,2.5),ylim=(-0.05,1.05),xticks=[1,2],xticklabels=['Baseline','Photostim'],xlabel='',ylabel='Average rightward choice (%)'))
    #g.set_axis_labels('','Average rightward choice (%)')
    plt.show()



'''
OLD: PhostostimSession __init__ method before changing this object to a cellDB.Experiment object. 
#def __init__(self, animalName, date, stimHemi, depth, tuningEphysSession, tuningSurffix, behavSurffix, tuningParadigm='laser_tuning_curve', behavParadigm='2afc', tetrodes=[1,2,3,4,5,6,7,8], clusters = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}):
        #self.animalName = animalName
        #self.date = date
        #self.stimHemi = stimHemi #string indicating which hemisphere received photostim during 2afc
        
        #self.tuningEphysSession = tuningEphysSession #ephys session associated with tuning curve
        ##self.tuningSession = animalName+'_'+tuningParadigm+'_'+date+tuningSurffix
        #self.tuningSession = tuningSurffix
        #self.behavSession =  ''.join(date.split('-'))+behavSurffix 
        #self.tuningParadigm ='laser_tuning_curve' 
        #self.behavParadigm ='2afc'
        #self.depth = depth
        #self.tetrodes = tetrodes  #to include all 8 tetrodes??
        #self.clusters = clusters  #just include good clusters?
        #self.tetrode_hemi_map = {} #Dict describing which tetrodes located in which hemi?? 
        ####I decided not to repeat low-level data loading and plotting methods since they already exist. Instead, in the plotting methods I'm using methods in nick's dataloader and dataplotter #####
        #self.loader = loader.DataLoader(mode='online', animalName=animalName, experimenter='', date=date, paradigm=tuningParadigm) #loader's default paradigm is for loading the behav data corresponding to tuning curve 
'''

if __name__ == '__main__':
    CASE = 2

    sessionTypes = {'nb':'noiseBurst',
                    'lp':'laserPulse',
                    'lt':'laserTrain',
                    'tc':'tuningCurve',
                    'bf':'bestFreq',
                    '3p':'3mWpulse',
                    '1p':'1mWpulse',
                    '2afc':'2afc'}


    ##### Mapping tetrodes to hemisphere in each mice ######
    tetrodesDict={'d1pi015_righthemi':[5,6,7,8], 'd1pi015_lefthemi':[1,2,3,4], 'd1pi016_righthemi':[1,2,7,8], 'd1pi016_lefthemi':[3,4,5,6]}
    ########################################################
    session = PhotostimSession(animalName='d1pi016', date ='2016-08-01', experimenter='', defaultParadigm='laser_tuning_curve')
    site1 = session.add_site(depth=2100, tetrodes=tetrodesDict['d1pi016_lefthemi'], stimHemi='left')
    site1.add_session('13-51-14', 'a', sessionTypes['tc'])
    site1.add_session(None, 'a', sessionTypes['2afc'], paradigm='2afc')
    site1.add_clusters(clusterDict = {4:[2,5],5:[9]})

    if CASE == 1:
        response_df,responsiveFreqs=site1.estimate_responsive_freq_range_tuning(mainTCind=0,tetrode=4,intensity=50.0,baseRange=[-0.050,-0.025],binEdges=[0,0.025,0.05,0.075,0.1],maxZthreshold=2)
        '''
        tetrode = 4
        mainTCind = 0
        intensity = 50.0
        
        ephysSession = os.path.join(site1.animalName, site1.get_session_ephys_filenames()[mainTCind])
        behavSession = site1.get_mouse_relative_behav_filenames()[mainTCind]
       
        ### Get behavior data associated with tuning curve ###
        bdata = site1.loader.get_session_behavior(behavSession)
        ### Get events data ###
        eventData = site1.loader.get_session_events(ephysSession)
        ### Get event onset times ###
        eventOnsetTimes = site1.loader.get_event_onset_times(eventData)
        ### Get spike data for each tetrode and plot tuning
        # -- WATCH OUT: get_tuning_spiketimes_good_clusters returns spikeTimestamps and goodClusterNumbers  
        (spikeTimestamps, goodClusterNumbers)=site1.get_tuning_spiketimes_good_clusters(tetrode,mainTCind)
        
        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        # -- check to see if ephys and behavior have the same number of trials -- #
        if len(eventOnsetTimes) == (len(freqEachTrial)+1):
            eventOnsetTimes = eventOnsetTimes[:-1]
            print 'Warning: ephys and behavior donot have same number of trials! Using bad hack to remove last trial in ephys'
        
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        #intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]

        oneFreq = freqEachTrial == 2000.0
        eventOnsetTimesThisCond = eventOnsetTimes[oneFreq] 
        timeRange = [0,0.125]
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimesThisCond,timeRange)

        numSpikesEachTrialThisCond = np.diff(indexLimitsEachTrial, axis=0)
        
        #aveSpikesThisCond = np.sum(numSpikesEachTrialThisCond,dtype=float)/len(eventOnsetTimesThisCond)
        aveSpikesThisCond = np.mean(numSpikesEachTrialThisCond,dtype=float)
        sdSpikesThisCond = np.std(numSpikesEachTrialThisCond,dtype=float)
        '''
    if CASE == 2:
        siteList=[]
        #percentCorrectDf = site1.calculate_percent_correct_each_freq_each_cond(main2afcind=1)
        siteList.append(site1)
        plot_ave_performance_lhfreqs_each_cond(siteList)
