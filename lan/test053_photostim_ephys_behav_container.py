#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Objects and methods for keeping information about recording sites in photostim experiments, including tuning info and behavior (psychometric curve).
Lan Guo 20160803
'''


import numpy as np
import os
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratest.nick.database import dataloader as loader
from jaratest.nick.database import dataplotter as dataplotter
from jaratest.lan import test047_group_photostim_psycurve_by_trialtype as photostimPlotter
reload(photostimPlotter)

class PhotostimSession(object):
    '''
    Object that contains information for a photostim experiment and has methods for plotting data. 
    animalName should be a string.
    date should be a string with format 'year-month-day'.
    ephysSession should be a string containing the timestamp part (can omit the date part of the file name).
    tuningSurffix is the surffix of the behavior session associated with tuning curve, should be a string.
    behavSurffix is the surffix of the photostim_freq_discrim behavior session, should be a string.
    '''
    def __init__(self, animalName, date, ephysSession, tuningSurffix, behavSurffix, tuningParadigm='laser_tuning_curve', behavParadigm='2afc', tetrodes=[1,2,3,4,5,6,7,8]):
        # -- Basic info --
        self.animalName = animalName
        self.date=date
        self.ephysSession = ephysSession #ephys session associated with tuning curve
        #self.tuningSession = animalName+'_'+tuningParadigm+'_'+date+tuningSurffix
        self.tuningSession = tuningSurffix
        self.behavSession =  ''.join(date.split('-'))+behavSurffix 
        self.tuningParadigm='laser_tuning_curve' 
        self.behavParadigm='2afc'
        self.tetrodes = tetrodes
        ####I decided not to repeat low-level data loading and plotting methods since they already exist. Instead, in the plotting methods I'm using methods in nick's dataloader and dataplotter #####
        self.loader = loader.DataLoader(mode='online', animalName=animalName, experimenter='', date=date, paradigm=tuningParadigm) #loader's default paradigm is for loading the behav data corresponding to tuning curve 
    
    def plot_tuning_heatmap_one_tetrode(self,tetrode):
        '''
        Method for plotting heatmap for multiunit tuning at one site. 
        Plotting tetrodes that are in the same hemi as the hemi receiving photostim during behavior if given the corresponding tetrodes when initiating PhotostimSession object. 
        '''
        ephysSession = self.loader.get_session_filename(self.ephysSession)
        #numTetrodes = len(self.tetrodes)
        #gs = gridspec.GridSpec(1,numTetrodes)
        
        ### Get behavior data associated with tuning curve ###
        bdata = self.loader.get_session_behavior(self.tuningSession)
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

    def plot_tuning_raster_one_intensity(self,tetrode,intensity):
        '''
        Method for plotting raster for multiunit tuning at one site. Just plotting one frequency since plotting several intensity requires subplot inside subplots, the code breaks. 
        Takes an argument giving the tuning intensity(in dB) to plot, this should be a float.
        Plotting tetrodes that are in the same hemi as the hemi receiving photostim during behavior if given the corresponding tetrodes when initiating PhotostimSession object. 
        '''
        ephysSession = self.loader.get_session_filename(self.ephysSession)
        #numTetrodes = len(self.tetrodes)
        
        ### Get behavior data associated with tuning curve ###
        bdata = self.loader.get_session_behavior(self.tuningSession)
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
        
        

    def plot_photostim_psycurve(self): 
        '''
        Method for plotting psychometric curve for 2afc paradigm. 
        Plots separate curves for trials with and without laser/photo stim. Can plot average psy curve if given more than one behavior sessions.
        '''
        sessions = [self.behavSession]
        print sessions
        photostimPlotter.plot_ave_photostim_psycurve_by_trialtype(self.animalName, sessions)


    def calculate_Z_score_tuning(self,tetrode):
        pass

    def estimate_best_tuning_freq(self,tetrode):
        '''
        Method for estimating the most responsive frequency presented in tuning session based on response Z score (calculated with baseline=[-0.05,-0.025] and timeRange=[0,0.1])
        '''
        pass
        

