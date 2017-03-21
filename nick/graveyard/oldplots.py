    def flip_cluster_tuning(self, session, behavSuffix, tetrode, rasterRange=[-0.5, 1]):

        from jaratoolbox import extraplots

        sessions = []
        tetrodes = []
        behavSuffixs = []
        clusters = []

        bdata = self.loader.get_session_behavior(behavSuffix)
        currentFreq = bdata['currentFreq']
        currentIntensity = bdata['currentIntensity']

        spikeData = self.loader.get_session_spikes(sessionDir, tetrode, cluster)
        if spikeData.clusters is None:
            self.cluster_session(session, tetrode)
            spikeData = self.loader.get_session_spikes(sessionDir, tetrode, cluster)

        possibleClusters = np.unique(spikeData.clusters)

        for cluster in possibleClusters:
            sessions.append(session)
            tetrodes.append(tetrode)
            behavSuffixs.append(behavSuffix)
            clusters.append(cluster)

        dataList = zip(sessions, tetrodes, behavSuffixs, clusters)
        flipper = extraplots.FlipThrough(self.plot_sorted_tuning_raster, dataList)
        return flipper

    # def _cluster_tuning(self, session, tetrode, behavSuffix, cluster):

    #     #session, tetrode, behavSuffix, cluster = dataTuple
    #     self.plot_sorted_tuning_raster(session, tetrode, behavSuffix, cluster)

    def flip_tetrode_tuning(self, session, behavSuffix, tetrodes=None , rasterRange=[-0.5, 1], tcRange=[0, 0.1]):

        if not tetrodes:
            tetrodes=self.defaultTetrodes

        plotTitle = sessionDir

        spikesList=[]
        eventsList=[]
        freqList=[]
        rasterRangeList=[]
        tcRangeList=[]

        bdata = self.loader.get_session_behavior(behavSuffix)
        freqEachTrial = bdata['currentFreq']
        eventData = self.loader.get_session_events(sessionDir)
        eventOnsetTimes = self.loader.get_event_onset_times(eventData)

        for tetrode in tetrodes:
            spikeData = self.loader.get_session_spikes(sessionDir, tetrode, cluster)
            spikeTimestamps = spikeData.timestamps

            spikesList.append(spikeTimestamps)
            eventsList.append(eventOnsetTimes)
            freqList.append(freqEachTrial)
            rasterRangeList.append(rasterRange)
            tcRangeList.append(tcRange)

        dataList = zip(sessions, tetrodes, behavSuffixs, clusters)
        flipper = extraplots.FlipThrough(self.plot_sorted_tuning_raster, dataList)
        return flipper

    def flip_freq_am_tuning(self, freqsession, amsession, experiment=-1, site=-1, tetrodes=None, freqRange = [-0.1, 0.3], amRange = [-0.2, 0.8], colorEachCond=None):
        freqsessionList=[]
        amsessionList=[]
        experimentList=[]
        siteList=[]
        tetrodeList=[]
        amRangeList=[]
        freqRangeList=[]
        colorList=[]
        
        sessionObj = self.get_session_obj(freqsession, experiment, site)
        if not tetrodes:
            tetrodes=sessionObj.tetrodes

        from jaratoolbox import extraplots

        for tetrode in tetrodes:
            freqsessionList.append(freqsession)
            amsessionList.append(amsession)
            experimentList.append(experiment)
            siteList.append(site)
            tetrodeList.append(tetrode)
            amRangeList.append(amRange)
            freqRangeList.append(freqRange)
            colorList.append(colorEachCond)

        dataList=zip(freqsessionList, amsessionList, tetrodeList, experimentList, siteList, freqRangeList, amRangeList, colorList)
        flipper=extraplots.FlipThrough(self.plot_am_freq_tuning, dataList)
        return flipper

    #DEPRECATED
    # @dataplotter.FlipThroughData
    @staticmethod
    def _tetrode_tuning(dataTuple):

        '''
        The data tuple must be exactly this: (spikeTimestamps, eventOnsetTimes, freqEachTrial, tetrode, rasterRange, tcRange)
        '''

        #Unpack the data tuple (Watch out - make sure things from the above method are in the right order)
        spikeTimestamps, eventOnsetTimes, freqEachTrial, tetrode, rasterRange, tcRange = dataTuple

        possibleFreq=np.unique(freqEachTrial)
        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        fig = plt.gcf()

        ax1=plt.subplot2grid((3, 3), (0, 0), rowspan=3, colspan=2)
        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = freqEachTrial, ms=1, labels=freqLabels, timeRange=rasterRange)
        plt.title("Tetrode {}".format(tetrode))
        ax1.set_ylabel('Freq (kHz)')
        ax1.set_xlabel('Time from sound onset (sec)')

        ax2=plt.subplot2grid((3, 3), (0, 2), rowspan=3, colspan=1)
        dataplotter.one_axis_tc_or_rlf(spikeTimestamps, eventOnsetTimes, freqEachTrial, timeRange=tcRange)

        ax2.set_ylabel("Avg spikes in range {}".format(tcRange))
        ax2.set_xticks(range(len(freqLabels)))
        ax2.set_xticklabels(freqLabels, rotation='vertical')
        ax2.set_xlabel('Freq (kHz)')

    DEPRECATED
    def plot_LFP_tuning(self, session, channel, behavSuffix): #FIXME: Time range??

        bdata = self.loader.get_session_behavior(behavSuffix)
        plotTitle = sessionDir
        eventData = self.loader.get_session_events(sessionDir, convertToSeconds=False)

        contData = self.loader.get_session_cont(session, channel)

        startTimestamp = contData.timestamps[0]

        eventOnsetTimes = self.loader.get_event_onset_times(eventData, diffLimit=False)

        freqEachTrial = bdata['currentFreq']
        intensityEachTrial = bdata['currentIntensity']

        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)

        secondsEachTrace = 0.1
        meanTraceEachSetting = np.empty((len(possibleIntensity), len(possibleFreq), secondsEachTrace*self.loader.EPHYS_SAMPLING_RATE))


        for indFreq, currentFreq in enumerate(possibleFreq):
            for indIntensity, currentIntensity in enumerate(possibleIntensity):

                #Determine which trials this setting was presented on.
                trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))

                #Get the onset timestamp for each of the trials of this setting.
                timestampsThisSetting = eventOnsetTimes[trialsThisSetting]

                #Subtract the starting timestamp value to get the sample number
                sampleNumbersThisSetting = timestampsThisSetting - startTimestamp

                #Preallocate an array to store the traces for each trial on which this setting was presented.
                traces = np.empty((len(sampleNumbersThisSetting), secondsEachTrace*self.loader.EPHYS_SAMPLING_RATE))

                #Loop through all of the trials for this setting, extracting the trace after each presentation
                for indSamp, sampNumber in enumerate(sampleNumbersThisSetting):
                    trace = contData.samples[sampNumber:sampNumber + secondsEachTrace*self.loader.EPHYS_SAMPLING_RATE]
                    trace = trace - trace[0]
                    traces[indSamp, :] = trace

                #Take the mean of all of the samples for this setting, and store it according to the freq and intensity
                mean_trace = np.mean(traces, axis = 0)
                meanTraceEachSetting[indIntensity, indFreq, :] = mean_trace

        maxVoltageAllSettings = np.max(np.max(meanTraceEachSetting, axis = 2))
        minVoltageAllSettings = np.min(np.min(meanTraceEachSetting, axis = 2))

        #Plot all of the mean traces in a grid according to frequency and intensity
        for intensity in range(len(possibleIntensity)):
            #Subplot2grid plots from top to bottom, but we need to plot from bottom to top
            #on the intensity scale. So we make an array of reversed intensity indices.
            intensPlottingInds = range(len(possibleIntensity))[::-1]
            for frequency in range(len(possibleFreq)):
                plt.subplot2grid((len(possibleIntensity), len(possibleFreq)), (intensPlottingInds[intensity], frequency))
                plt.plot(meanTraceEachSetting[intensity, frequency, :], 'k-')
                plt.ylim([minVoltageAllSettings, maxVoltageAllSettings])
                plt.axis('off')

        #This function returns the location of the text labels
        #We have to mess with the ideal locations due to the geometry of the plot
        def getXlabelpoints(n):
            rawArray = np.array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
            diffFromCenter = rawArray - 0.6
            partialDiffFromCenter = diffFromCenter * 0.175 #Percent change has to be determined empirically
            finalArray = rawArray - partialDiffFromCenter
            return finalArray

        #Not sure yet if similar modification to the locations will be necessary.
        def getYlabelpoints(n):
            rawArray = np.array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
            return rawArray

        freqLabelPositions = getXlabelpoints(len(possibleFreq))
        for indp, position in enumerate(freqLabelPositions):
            plt.figtext(position, 0.075, "%.1f"% (possibleFreq[indp]/1000), ha = 'center')

        intensLabelPositions = getYlabelpoints(len(possibleIntensity))
        for indp, position in enumerate(intensLabelPositions):
            plt.figtext(0.075, position, "%d"% possibleIntensity[indp])

        plt.figtext(0.525, 0.025, "Frequency (kHz)", ha = 'center')
        plt.figtext(0.025, 0.5, "Intensity (dB SPL)", va = 'center', rotation = 'vertical')
        plt.show()
