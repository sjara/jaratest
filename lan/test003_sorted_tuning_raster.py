

'''
This is a function to plot rasters sorted by frequency for each intensity of the tuning curve data. This should go into Nick's ephys_experiment.py module.
Alternatively this could be stand alone, but have to import and change all 'self' to 'ephys_experiment'
import jaratoolbox.test.nick.ephysExperiments.ephys_experiment
'''

    def sorted_tuning_raster(self, session, tetrode, behavFileIdentifier, cluster = None, replace=0, timeRange = [-0.5, 1]):
        '''
        '''
   
        #Calling method to get the ephys and event data
        spikeData, eventData, plotTitle = self.get_session_ephys_data(session, tetrode)
        
        #Calling method to get the behavior data and extract the freq and intensity each trial
        bdata = self.get_session_behav_data(session, behavFileIdentifier)
        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']
        
        #Caling method to calculate event onset times from the event data
        eventOnsetTimes = self.get_event_onset_times(eventData)
        
        #Extract the timestamps from the spikeData object, limit to a single cluster if needed
        spikeTimestamps = spikeData.timestamps  #This is already in seconds
        if cluster:
            spikeTimestamps = spikeTimestamps[spikeData.clusters==cluster]
            
        #Get all possible frequencies and intensities presented
        possibleFreq = np.unique(freqEachTrial) 
        possibleIntensity = np.unique(intensityEachTrial)

        #Interate through all possible intensities and frequencies, get trial numbers selected  by specific frequency and intensity

        for indIntensity, currentIntensity in enumerate(possibleIntensity):
            spikeTimesFromEventOnset_thisIntensity = np.array([])
            trialIndexForEachSpike_thisIntensity = np.array([])
            nTrialsThisCondition = 0
            for indFrequency, currentFreq in enumerate(possibleFreq):
                #Determine which trials this setting was presented on. 
                trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))
                eventOnsetTimesThisSetting = eventOnsetTimes[trialsThisSetting]

                #Loop through all of the trials for this setting, extracting the spike timestamps after each presentation
                # for indts, eventTimestamp in enumerate(eventOnsetTimesThisSetting):
                (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimesThisSetting,timeRange)#??

                spikeTimesFromEventOnset_thisIntensity = np.concatenate((spikeTimesFromEventOnset_thisIntensity, spikeTimesFromEventOnset))
                trialIndexForEachSpike_thisIntensity = np.concatenate((trialIndexForEachSpike_thisIntensity, trialIndexForEachSpike+nTrialsThisCondition))
                nTrialsThisCondition += len(eventOnsetTimesThisSetting)

            #Each intensity gets a subplot of all frequencies presented in this intensity
            subplot(len(possibleIntensity),1,indIntensity+1)

            plot(spikeTimesFromEventOnset_thisIntensity, trialIndexForEachSpike_thisIntensity, '.', ms=1)  #here plotting trialIndexForEachSpike on y-axis may be less informative, can substitute with frequency?
            axvline(x=0, ymin=0, ymax=1, color='r')
            if indIntensity == 0:
                title(plotTitle)
            #return(spikeTimesFromEventOnset_thisIntensity, trialIndexForEachSpike_thisIntensity)
            #return(spikeTimesFromEventOnset, trialIndexForEachSpike)

