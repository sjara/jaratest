
    def plot_tc_heatmap(self, session, tetrode, behavFileIdentifier, cluster=None):
        
        
        SAMPLING_RATE = 30000.0
        
        PLOTTING_WINDOW = 0.1 #Window to plot, in seconds

        if isinstance(session, str):
            ephysSession = session
        else:
            ephysRoot = self.localEphysDir
            ephysSession = sort(os.listdir(ephysRoot))[session]

        ephysDir=os.path.join(self.localEphysDir, ephysSession)
        event_filename=os.path.join(ephysDir, 'all_channels.events')

        behaviorDir=os.path.join(self.localBehavPath, self.animalName)
        fullBehavFilename = ''.join([self.behavFileBaseName, behavFileIdentifier, '.h5'])
        behavDataFileName=os.path.join(behaviorDir, fullBehavFilename)

        #Extract the frequency presented each trial from the behavior data
        bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']

        possibleFreq = np.unique(freqEachTrial) 
        possibleIntensity = np.unique(intensityEachTrial)

        #Get the event timestamps from openEphys
        ev=loadopenephys.Events(event_filename)
        evID=np.array(ev.eventID)
        eventOnsetTimes=ev.timestamps[evID==1] #The timestamps of all of the stimulus onsets

        tetrode = 6 #The tetrode to plot
        spikeFilename = os.path.join(ephysDir, 'Tetrode{}.spikes'.format(tetrode))
        spikeData = loadopenephys.DataSpikes(spikeFilename)
        
        if cluster:
            clustersDir = os.path.join(settings.EPHYS_PATH,'%s/%s_kk/'%(self.animalName,ephysSession))
            clustersFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
            spikeData.set_clusters(clustersFile)

            spikeTimestamps = spikeData.timestamps[spikeData.clusters==cluster]
        else:
            spikeTimestamps = spikeData.timestamps





        allSettingsSpikeCount = np.zeros([len(possibleIntensity), len(possibleFreq)]) 

        for indFreq, currentFreq in enumerate(possibleFreq):
            for indIntensity, currentIntensity in enumerate(possibleIntensity):

                #Determine which trials this setting was presented on. 
                trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))

                #Get the onset timestamp for each of the trials of this setting. 
                timestampsThisSetting = eventOnsetTimes[trialsThisSetting]

                spikesAfterThisSetting = np.array([])
                #Loop through all of the trials for this setting, extracting the trace after each presentation
                for indts, eventTimestamp in enumerate(timestampsThisSetting):
                    spikes = spikeTimestamps[(spikeTimestamps >= eventTimestamp) & (spikeTimestamps <= eventTimestamp + SAMPLING_RATE * PLOTTING_WINDOW)]
                    spikes = spikes - eventTimestamp
                    spikes = spikes / 30 #Spikes in ms after the stimulus

                    spikesAfterThisSetting = np.concatenate((spikesAfterThisSetting, spikes))
                    spikeCountThisSetting = len(spikesAfterThisSetting)
                allSettingsSpikeCount[indIntensity, indFreq] = spikeCountThisSetting
                
        fig = figure()
        ax = fig.add_subplot(111)
        ax.set_ylabel('Intensity (dB SPL)')
        ax.set_xlabel('Frequency (kHz)')
        cax = ax.imshow(np.flipud(allSettingsSpikeCount), interpolation='none', aspect='auto')
        cbar=colorbar(cax)
        cbar.ax.set_ylabel('Spikes in 0.1sec after stim')
        ax.set_xticks(range(len(possibleFreq)))
        xticks = ["%.1f" % freq for freq in possibleFreq/1000]
        ax.set_xticklabels(xticks)
        ax.set_yticks([0, 1, 2, 3])
        
        ax.set_yticklabels(possibleIntensity)
