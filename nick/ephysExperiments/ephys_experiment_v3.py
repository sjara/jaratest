import jaratoolbox
from jaratoolbox import celldatabase
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from collections import defaultdict
from jaratoolbox.spikesorting import align_waveforms, plot_waveforms #FIXME: don't import functions, import the module
import matplotlib.pyplot as plt
import os
import subprocess
import numpy as np

#from jaratoolbox.test.nick.ephysExperiments import recordingday as rd

from jaratoolbox.test.nick.ephysExperiments import clusterManySessions_v2 as cms2
reload(cms2)

class EphysExperiment(object):

    def __init__(self,
                 animalName,
                 date,
                 experimenter='nick',
                 serverUser='jarauser',
                 serverName='jarahub',
                 serverBehavPathBase='/data/behavior',
                 paradigm='laser_tuning_curve'):

        self.SAMPLING_RATE = 30000.0
        self.animalName = animalName
        self.date = date
        self.paradigm=paradigm
        self.serverUser = serverUser
        self.serverName = serverName
        self.serverBehavPathBase = serverBehavPathBase
        self.experimenter = experimenter
        self.serverBehavPath = os.path.join(self.serverBehavPathBase, self.experimenter, self.animalName)
        self.remoteBehavLocation = '{0}@{1}:{2}'.format(self.serverUser, self.serverName, self.serverBehavPath)
        self.localBehavPath = os.path.join(settings.BEHAVIOR_PATH, self.experimenter)
        self.localEphysDir = os.path.join(settings.EPHYS_PATH, self.animalName)
        self.behavFileBaseName = '_'.join([self.animalName, self.paradigm, ''.join(self.date.split('-'))])

    def get_behavior(self):
        transferCommand = ['rsync', '-a', '--progress', self.remoteBehavLocation, self.localBehavPath]
        print ' '.join(transferCommand)
        subprocess.call(transferCommand)

    def get_session_name(self, session, dataType='ephys'):

        if isinstance(session, str):
            if len(session.split('_'))==2: #Has the date already
                ephysSession = session
            elif len(session.split('_'))==1: #Does not have the date already, assume to be the stored date
                ephysSession = '_'.join([self.date, session])
            else:
                print "Unrecognized session format"
                pass

            return ephysSession

        elif isinstance(session, int): #use the passed int as an index to get the session name from the current directory
            filesFromToday = [f for f in os.listdir(self.localEphysDir) if (f.startswith(self.date) & ('_kk' not in f))]
            ephysSession = sorted(filesFromToday)[session]

            return ephysSession

        elif isinstance(session, jaratoolbox.test.nick.ephysExperiments.recordingday.Session):
            ephysSession = session.session
            behavFileIdentifier = session.behavFileIdentifier

            if dataType=='ephys':
                return ephysSession
            elif dataType=='behavior':
                return behavFileIdentifier
            else:
                print "Unrecognized dataType: use 'ephys' or 'behavior'"

        else:
            print "Unrecognized session format"
            pass


    def get_session_event_data(self, session):
        '''
        Gets the event data for a session. Split because there is no need to specify a tetrode for the event data, but
        a tetrode must be specified for the spike data

        The event data is not modified. Timestamps are not converted to seconds at this point

        '''


        ephysSession = self.get_session_name(session)
        ephysDir=os.path.join(self.localEphysDir, ephysSession)
        event_filename=os.path.join(ephysDir, 'all_channels.events')
        eventData=loadopenephys.Events(event_filename)

        return eventData


    def get_session_plot_title(self, session):
        '''
        Constructs the full session path for use as a plot title
        '''

        ephysSession = self.get_session_name(session)
        ephysDir=os.path.join(self.localEphysDir, ephysSession)
        plotTitle = ephysDir

        return plotTitle


    def get_session_spike_data_one_tetrode(self, session, tetrode, convert_to_seconds=True, convert_to_mV=True):
        '''
        Get the spike data for one session, one tetrode.

        Method to retrieve the spike data for a session/tetrode. Automatically loads the
        clusters if clustering has been done for the session. This method converts the spike
        timestamps to seconds by default.

        Args:

        session (str or int): If a string, then must be either the full name of the ephys file (e.g. '2015-06-24_12-24-03')
        or just the timestamp portion of the file ('12-24-03'), in which case self.date will be used to construct the
        full file name. If an int, then the files that were recorded on self.date will be sorted, and the value provided
        will be used to index the sorted list. Therefore, -1 will return the session with the latest timestamp on the recording day.

        tetrode (int): The tetrode number to retrieve

        convert_to_seconds (bool): Whether or not to divide by the value stored in self.SAMPLING_RATE before returning spike
        timestamps

        Returns:

        spikeData (object of type jaratoolbox.loadopenephys.DataSpikes)

        '''

        ephysSession = self.get_session_name(session)
        ephysDir=os.path.join(self.localEphysDir, ephysSession)
        spikeFilename = os.path.join(ephysDir, 'Tetrode{}.spikes'.format(tetrode))
        spikeData = loadopenephys.DataSpikes(spikeFilename)

        if convert_to_mV and hasattr(spikeData, 'samples'):
            spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
            spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
        else: 
            spikeData.samples = np.array([])

        if convert_to_seconds and hasattr(spikeData, 'timestamps'):
            spikeData.timestamps = spikeData.timestamps/self.SAMPLING_RATE
        else:
            spikeData.timestamps = np.array([])

        print "FIXME: getting spike data without converting values will result in no timestamps or samples being returned"

        #If clustering has been done for the tetrode, add the clusters to the spikedata object
        clustersDir = os.path.join(settings.EPHYS_PATH,'%s/%s_kk/'%(self.animalName,ephysSession))
        clustersFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
        if os.path.isfile(clustersFile):
            spikeData.set_clusters(clustersFile)

        return spikeData

    def get_event_onset_times(self, eventData, eventID=1, eventChannel=0, convert_to_seconds=True):
        '''
        Calculate event onset times given an eventData object.

        Accepts a jaratoolbox.loadopenephys.Events object and finds the event onset times.

        '''

        evID=np.array(eventData.eventID)
        evChannel = np.array(eventData.eventChannel)

        if convert_to_seconds:
            eventTimes=np.array(eventData.timestamps)/self.SAMPLING_RATE
        else:
            eventTimes = np.array(eventData.timestamps)
        eventOnsetTimes=eventTimes[(evID==eventID)&(evChannel==eventChannel)]

        #Restrict to events are seperated by more than 0.5 seconds
        print "FIXME: Hardcoded minimum difference between event onset times"
        evdiff = np.r_[1.0, np.diff(eventOnsetTimes)]
        eventOnsetTimes=eventOnsetTimes[evdiff>0.5]

        return eventOnsetTimes


    def get_session_behav_data(self, session, behavFileIdentifier=None):
        if not isinstance(session, str): #FIXME: This is a hack but I think it will work for nto
            behavFileIdentifier=self.get_session_name(session, dataType='behavior')
        else:
            if not behavFileIdentifier:
                print "Either supply a Session object as the session, or supply a valid behav file identifier"

        behaviorDir=os.path.join(self.localBehavPath, self.animalName)
        fullBehavFilename = ''.join([self.behavFileBaseName, behavFileIdentifier, '.h5'])
        behavDataFileName=os.path.join(behaviorDir, fullBehavFilename)

        #Extract the frequency presented each trial from the behavior data
        bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')

        return bdata

    def cluster_session(self, session, tetrode):

        ephysSession = self.get_session_name(session)

        oneTT = spikesorting.TetrodeToCluster(self.animalName,ephysSession,tetrode)

        oneTT.load_waveforms()
        oneTT.create_fet_files()
        oneTT.run_clustering()
        oneTT.save_report()

    def plot_session_raster(self, session, tetrode, cluster = None, sortArray = [], replace=0, ms=4):

        plotTitle = self.get_session_plot_title(session)
        spikeData= self.get_session_spike_data_one_tetrode(session, tetrode)
        eventData = self.get_session_event_data(session)
        eventOnsetTimes = self.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps

        if cluster:
            spikeTimestamps = spikeTimestamps[spikeData.clusters==cluster]

        if replace:
            plt.cla()
        else:
            plt.figure()

        self.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray = sortArray, replace = replace, ms=ms)

    def plot_raster(self, spikeTimestamps, eventOnsetTimes, sortArray = [], replace = 0, timeRange = [-0.5, 1], ms = 4):
        '''
        Plot a raster given spike timestamps and event onset times

        This method will take the spike timestamps directly, convert them so that they are relative to the event onset times,
        and then call the appropriate plotting code. This method should ideally be able to handle making both sortArrayed and unsortArrayed
        rasters.

        sortArray (array): An array of parameter values for each trial. Output will be sorted by the possible values of the parameter

        '''
        if len(sortArray)>0:
            trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))
        else:
            trialsEachCond = []

        spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)

        #if replace:
            #plt.cla()

        pRaster,hcond,zline = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond = trialsEachCond)
        plt.setp(pRaster,ms=ms)

    def plot_array_raster(self, session, replace=0, timeRange = [-0.5, 1], tetrodeIDs=[3,4,5,6], ms=4):
        '''
        This is the much-improved version of a function to plot a raster for each tetrode. All rasters
        will be plotted using standardized plotting code, and we will simply call the functions.
        In this case, we get the event data once, and then loop through the tetrodes, getting the
        spike data and calling the plotting code for each tetrode.
        '''

        numTetrodes = len(tetrodeIDs)
        eventData = self.get_session_event_data(session)
        eventOnsetTimes = self.get_event_onset_times(eventData)
        plotTitle = self.get_session_plot_title(session)

        if replace:
            fig = plt.gcf()
            plt.clf()
        else:
            fig = plt.figure()


        for ind , tetrodeID in enumerate(tetrodeIDs):

            spikeData = self.get_session_spike_data_one_tetrode(session, tetrodeID)
            if ind == 0:
                ax = fig.add_subplot(numTetrodes,1,ind+1)
            else:
                ax = fig.add_subplot(numTetrodes,1,ind+1, sharex = fig.axes[0], sharey = fig.axes[0])
            spikeTimestamps = spikeData.timestamps
            self.plot_raster(spikeTimestamps, eventOnsetTimes, replace = replace, ms=ms, timeRange = timeRange)
            if ind == 0:
                plt.title(plotTitle)
            #title('Channel {0} spikes'.format(ind+1))
            plt.ylabel('TT {}'.format(tetrodeID))

        plt.xlabel('time (sec)')
        #tight_layout()
        plt.draw()
        plt.show()


    def plot_sorted_session_raster(self, session, tetrode, timeRange = [-0.5, 1]):
        '''
        A method that can sort by any vector and plot the sorted vals.
        '''
        pass

    def plot_sorted_tuning_raster(self, session, tetrode, behavFileIdentifier, cluster = None, replace=0, timeRange = [-0.5, 1], ms = 1):
        '''
        '''
        bdata = self.get_session_behav_data(session,behavFileIdentifier)

        freqEachTrial = bdata['currentFreq']
        possibleFreq = np.unique(freqEachTrial)

        intensityEachTrial = bdata['currentIntensity']
        possibleIntensity = np.unique(intensityEachTrial)


        trialsEachCond = behavioranalysis.find_trials_each_combination(freqEachTrial, possibleFreq, intensityEachTrial, possibleIntensity)

        spikeData = self.get_session_spike_data_one_tetrode(session, tetrode)

        eventData = self.get_session_event_data(session)
        eventOnsetTimes = self.get_event_onset_times(eventData)
        spikeTimestamps=spikeData.timestamps


        spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)

        freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
        plotTitle = self.get_session_plot_title(session)

        fig = plt.figure()
        for indIntensity, intensity in enumerate(possibleIntensity[::-1]):

            if indIntensity == 0:
                fig.add_subplot(len(possibleIntensity), 1, indIntensity+1)
                plt.title(plotTitle)
            else:
                fig.add_subplot(len(possibleIntensity), 1, indIntensity+1, sharex=fig.axes[0], sharey=fig.axes[0])

            trialsThisIntensity = trialsEachCond[:, :, len(possibleIntensity)-indIntensity-1] #FIXME: There must be a better way to flip so high intensity is on top

            pRaster,hcond,zline = extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange, trialsEachCond = trialsThisIntensity, labels = freqLabels)
            plt.setp(pRaster,ms=ms)
            plt.ylabel('{:.0f} dB'.format(intensity))

            if indIntensity == len(possibleIntensity)-1:
                plt.xlabel("time (sec)")

        fig.show()


    def plot_tc_psth(self, session, tetrode, behavFileIdentifier, cluster=None):
        # I removed this method because it does not seem like we want to use it.
        # The code is still in my test dir.
        pass

    def plot_session_tc_heatmap(self, session, tetrode, behavFileIdentifier, replace = 0, cluster = None, norm=False, clim = None):

        '''
        Wrapper to plot a TC heatmap for a single session/tetrode

        Extracts the data from a single tetrode in a recording session, and uses the data to call plot_tc_heatmap.
        The session can either be the actual session name as a string, or an integer that will be used the select
        a session from the sorted list of sessions in the ephys directory for this recording day. Also takes the
        unique identifier for the behavior data file. Can select only the spikes belonging to a single cluster
        if clustering has been done on an ephys session.

        Args:
            session (str or int): Either the session name as a string or an int that will be used to select the session from
                                  the sorted list of sessions in the current directory.
            tetrode (int): The number of the tetrode to plot
            behavFileIdentifier (str): The unique portion of the behavior data filename used to identify it.
            cluster (int): Optional, the number of the cluster to plot. Leave unset to analyze the entire site.
            norm (bool): Whether or not to normalize to the maximum spike rate for the color axis

        Examples:

        With a specified session and the behavior file 'animal000_behavior_paradigm_20150624a.h5'

        >>>experiment.plot_session_tc_heatmap('2015-06-24_15-32-16', 6, 'a')

        To use the last recorded ephys session (the -1 index in the sorted list)

        >>>experiment.plot_session_tc_heatmap(-1, 6, 'a')
        '''

        #Get the ephys and event data
        spikeData = self.get_session_spike_data_one_tetrode(session, tetrode)
        eventData = self.get_session_event_data(session)
        plotTitle = self.get_session_plot_title(session)

        #Get the behavior data and extract the freq and intensity each trial
        bdata = self.get_session_behav_data(session, behavFileIdentifier)
        freqEachTrial = bdata['currentFreq']
        possibleFreq = np.unique(freqEachTrial)
        intensityEachTrial = bdata['currentIntensity']
        possibleIntensity = np.unique(intensityEachTrial)

        #Calculate event onset times from the event data
        eventOnsetTimes = self.get_event_onset_times(eventData)

        #Extract the timestamps from the spikeData object, limit to a single cluster if needed
        spikeTimestamps = spikeData.timestamps
        if cluster:
            spikeTimestamps = spikeTimestamps[spikeData.clusters==cluster]

        #Call the plotting code with the data
        #self.plot_tc_heatmap_old(spikeTimestamps, eventOnsetTimes, freqEachTrial, intensityEachTrial, replace = replace, norm = norm, clim=clim)

        print "Ephys events: {}".format(len(eventOnsetTimes))
        print "Behavior trials: {}".format(len(freqEachTrial))

        trialsEachCond = behavioranalysis.find_trials_each_combination(intensityEachTrial, possibleIntensity, freqEachTrial, possibleFreq)

        timeRange = [0, 0.1]
        spikeArray = self.avg_spikes_in_event_locked_timerange_each_cond(spikeTimestamps, trialsEachCond, eventOnsetTimes, timeRange)

        self.plot_TCarray_as_heatmap(spikeArray, possibleFreq, possibleIntensity, timeRange)



    def plot_TCarray_as_heatmap(self, heatmapArray, xlabels=None, ylabels=None, timeRange = None, flipy=True, flipylabels=True, cmap='Blues'):

        #fig = plt.gcf()
        ax = plt.gca()
        #ax = fig.add_subplot(111)
        ax.set_ylabel('Intensity (dB SPL)')
        ax.set_xlabel('Frequency (kHz)') #FIXME: This should be outside this function and does not appear to work anyway

        if flipy:
            heatmapArray = np.flipud(heatmapArray)

        cax = ax.imshow(heatmapArray, interpolation='none', aspect='auto', cmap=cmap)
        vmin, vmax = cax.get_clim()
        cbar=plt.colorbar(cax, format = '%.1f')

        if timeRange is not None:

            cbar.ax.set_ylabel('Avg spikes in time range: {}'.format(timeRange))

        if xlabels is not None:
            ax.set_xticks(range(len(xlabels)))
            xticks = ["%.1f" % freq for freq in xlabels/1000.0] #FIXME: This should be outside this function
            ax.set_xticklabels(xticks, rotation = 'vertical')

        ax.set_yticks(range(np.shape(heatmapArray)[0]))


        if ylabels is not None:
            if flipylabels:
                ax.set_yticklabels(ylabels[::-1])
            else:
                ax.set_yticklabels(ylabels)

        #plt.show()



    def avg_spikes_in_event_locked_timerange_each_cond(self, spikeTimestamps, trialsEachCond, eventOnsetTimes, timeRange):

        if len(eventOnsetTimes)!=np.shape(trialsEachCond)[0]:
            eventOnsetTimes=eventOnsetTimes[:-1]

        spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                                                                                                     eventOnsetTimes,
                                                                                                                     timeRange)
        spikeArray = self.avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCond)

        return spikeArray


    def avg_locked_spikes_per_condition(self, indexLimitsEachTrial, trialsEachCond):

        numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial, axis=0))
        conditionMatShape = np.shape(trialsEachCond)
        numRepeats = np.product(conditionMatShape[1:])
        nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats), conditionMatShape)
        spikesFilteredByTrialType = nSpikesMat*trialsEachCond
        avgSpikesArray = np.sum(spikesFilteredByTrialType, 0)/np.sum(trialsEachCond, 0).astype('float')
        return avgSpikesArray




    def plot_tc_heatmap_old(self, spikeTimestamps, eventOnsetTimes, freqEachTrial, intensityEachTrial, replace = 0, norm=False, clim = None):

        '''
        Plot a tuning curve heatmap.

        Plots a frequency-intensity tuning curve as a 2-D matrix, where color indicates the number of spikes fired
        after the presentation of the frequency-intensity pair. Accepts arrays of data, so it can be called directly
        or with a wrapper like plot_session_tc_heatmap, which will extract the data from recording session files and
        call this method to do the plotting.

        Takes spike timestamps in SECONDS, event onset times in SECONDS

        Args:
            spikeTimestamps (array): A 1D numpy array of all of the spike timestamps in a recording session IN SECONDS
            eventOnsetTimes (array): A 1D numpy array of the event onset times in a recording session IN SECONDS
            freqEachTrial (array): A 1D numpy array of the frequency presented each trial, in Hz. Must have the same length as
                                   eventOnsettimes
            intensityEachTrial: A 1D numpy array of the intensity presentes each trial, in dB SPL. Must have the same length as
                                eventOnsetTimes
            norm (bool): Whether or not to normalize to the maximum spike rate for the color axis
        '''

        SAMPLING_RATE = 30000.0

        #Calculating the avg # spikes in this time range after the stim onset
        PLOTTING_WINDOW = 0.1

        #Find the possible frequencies and intensities
        possibleFreq = np.unique(freqEachTrial)
        possibleIntensity = np.unique(intensityEachTrial)

        #Initialize a matrix to store the TC data in
        allSettingsSpikeCount = np.zeros([len(possibleIntensity), len(possibleFreq)])

        for indFreq, currentFreq in enumerate(possibleFreq):
            for indIntensity, currentIntensity in enumerate(possibleIntensity):

                #Determine which trials this setting was presented on.
                trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))

                numTrialsThisSetting = len(trialsThisSetting)

                #Get the onset timestamp for each of the trials of this setting.
                eventOnsetTimesThisSetting = eventOnsetTimes[trialsThisSetting]

                spikesAfterThisSetting = np.array([])

                #Loop through all of the trials for this setting, extracting the spike timestamps after each presentation
                for indts, eventTimestamp in enumerate(eventOnsetTimesThisSetting):
                    spikes = spikeTimestamps[(spikeTimestamps >= eventTimestamp) & (spikeTimestamps <= eventTimestamp + PLOTTING_WINDOW)]
                    spikesAfterThisSetting = np.concatenate((spikesAfterThisSetting, spikes))

                #The number of spikes fired in the window after all of the stims of this type
                spikeCountThisSetting = len(spikesAfterThisSetting)

                #Average spikes per stim
                spikeAverageThisSetting = spikeCountThisSetting/float(numTrialsThisSetting)

                #Save to the matrix
                allSettingsSpikeCount[indIntensity, indFreq] = spikeAverageThisSetting

        if norm:
            allSettingsSpikeCount = allSettingsSpikeCount/allSettingsSpikeCount.max()

        #fig = figure()
        #ax = fig.add_subplot(111)

        if replace:
            plt.cla()
        else:
            plt.figure()

        ax = plt.gca()
        ax.set_ylabel('Intensity (dB SPL)')
        ax.set_xlabel('Frequency (kHz)')
        cax = ax.imshow(np.flipud(allSettingsSpikeCount), interpolation='none', aspect='auto', cmap='Blues')
        vmin, vmax = cax.get_clim()
        cbar=plt.colorbar(cax, format = '%.1f')

        if clim is not None:
            cbar.set_clim(clim)

        if norm:
            cbar.ax.set_ylabel('Proportion of max firing')
        else:
            cbar.ax.set_ylabel('Average spikes in 0.1sec after stim')
        ax.set_xticks(range(len(possibleFreq)))
        xticks = ["%.1f" % freq for freq in possibleFreq/1000.0]
        ax.set_xticklabels(xticks, rotation = 'vertical')
        ax.set_yticks([0, 1, 2, 3])

        ax.set_yticklabels(possibleIntensity[::-1])


class RecordingDay(object):

    '''
    Parent class so that we don't have to re-enter this info for each recording site.
    The construction of new recording sites could possible be handled through a
    method of this class in the future. For now, an instance of this class is a
    required argument for the RecordingSite class
    '''
    def __init__(self, animalName, date, experimenter, **kwargs):
        self.animalName = animalName
        self.date = date
        self.experimenter = experimenter
        self.siteList = []
        #An internal instance of the ephys experiment class for easy plotting?
        self.ee2 = EphysExperiment(animalName, date, experimenter = experimenter, **kwargs)


class RecordingSite(object):

    '''
    Class for holding information about a recording site. Will act as a parent for all of the
    RecordingSession objects that hold information about each individual recording session.
    '''

    def __init__(self, parent, depth, goodTetrodes):

        self.animalName = parent.animalName
        self.date = parent.date
        self.experimenter = parent.experimenter
        self.depth = depth
        self.goodTetrodes = goodTetrodes
        self.sessionList = []
        parent.siteList.append(self)


    def add_session(self, sessionID, behavFileIdentifier, sessionType):
        session = RecordingSession(sessionID, behavFileIdentifier, sessionType, self.date)
        self.sessionList.append(session)
        return session

    def get_session_filenames(self):
        return [s.session for s in self.sessionList]

    def get_session_behavIDs(self):
        return [s.behavFileIdentifier for s in self.sessionList]

    def get_session_types(self):
        return [s.sessionType for s in self.sessionList]

    def get_session_inds_one_type(self, plotType, report):
        return [index for index, s in enumerate(self.sessionList) if ((s.plotType==plotType) & (s.report==report))]

    def add_cluster(self, cluster):

        pass

    def push_clusters_to_database(self):

        pass

    def generate_main_report(self, siteName):
        '''
        Generate the reports for all of the sessions in this site. This is where we should interface with
        the multiunit clustering code, since all of the sessions that need to be clustered together have
        been defined at this point.

        FIXME: This method should be able to load some kind of report template perhaps, so that the
        types of reports we can make are not a limited. For instance, what happens when we just have
        rasters for a site and no tuning curve? Implementing this is a lower priority for now.

        Incorporated lan's code for plotting the cluster reports directly on the main report
        '''
        #FIXME: import another piece of code to do this?
        #FIXME: OR, break into two functions: one that will do the multisite clustering, and one that
        #knows the type of report that we want. The first one can probably be a method of MSTC, the other
        #should either live in extraplots or should go in someone's directory

        for tetrode in self.goodTetrodes:
            oneTT = cms2.MultipleSessionsToCluster(self.animalName, self.get_session_filenames(), tetrode, '{}_{}'.format(self.date, siteName))
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

            ee = EphysExperiment(self.animalName, self.date, experimenter = self.experimenter)

            #Iterate through the clusters, making a new figure for each cluster.
            #for indClust, cluster in enumerate([3]):
            for indClust, cluster in enumerate(possibleClusters):


                mainRasterInds = self.get_session_inds_one_type(plotType='raster', report='main')
                mainRasterSessions = [self.get_session_filenames()[i] for i in mainRasterInds]
                mainRasterTypes = [self.get_session_types()[i] for i in mainRasterInds]

                mainTCinds = self.get_session_inds_one_type(plotType='tc_heatmap', report='main')
                mainTCsessions = [self.get_session_filenames()[i] for i in mainTCinds]

                mainTCbehavIDs = [self.get_session_behavIDs()[i] for i in mainTCinds]
                mainTCtypes = [self.get_session_types()[i] for i in mainTCinds]

                plt.figure() #The main report for this cluster/tetrode/session

                for indRaster, rasterSession in enumerate(mainRasterSessions):
                    plt.subplot2grid((6, 6), (indRaster, 0), rowspan = 1, colspan = 3)
                    ee.plot_session_raster(rasterSession, tetrode, cluster = cluster, replace = 1, ms=1)
                    plt.ylabel('{}\n{}'.format(mainRasterTypes[indRaster], rasterSession.split('_')[1]), fontsize = 10)
                    ax=plt.gca()
                    extraplots.set_ticks_fontsize(ax,6)

                #We can only do one main TC for now.
                if len(mainTCsessions)>0:
                    plt.subplot2grid((6, 6), (0, 3), rowspan = 3, colspan = 3)
                    #tcIndex = site.get_session_types().index('tuningCurve')
                    tcSession = mainTCsessions[0]
                    tcBehavID = mainTCbehavIDs[0]
                    ee.plot_session_tc_heatmap(tcSession, tetrode, tcBehavID, replace = 1, cluster = cluster)
                    plt.title("{0}\nBehavFileID = '{1}'".format(tcSession, tcBehavID), fontsize = 10)

                nSpikes = len(oneTT.timestamps)
                nClusters = len(possibleClusters)
                #spikesEachCluster = np.empty((nClusters, nSpikes),dtype = bool)
                #if oneTT.clusters == None:
                    #oneTT.set_clusters_from_file()
                #for indc, clusterID in enumerate (possibleClusters):
                    #spikesEachCluster[indc, :] = (oneTT.clusters==clusterID)

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
                plt.close()


            plt.figure()
            oneTT.save_multisession_report()
            plt.close()


class RecordingSession(object):
    '''
    Class to hold information about a single session.
    Includes the session name, the type of session, and any associated behavior data
    Accepts just the time of the recording (i.e. 11-36-54), and the date, which can
    be passed from the parent when this class is called. This keeps us from
    having to write it over and over again.
    '''
    def __init__(self, sessionID, behavFileIdentifier, sessionType, date):
        self.session = '_'.join([date, sessionID])
        self.behavFileIdentifier = behavFileIdentifier
        self.sessionType = sessionType
        self.plotType=None
        self.report=None

    def set_plot_type(self, plotTypeStr, report = 'main'):
        self.plotType = plotTypeStr
        self.report = report
