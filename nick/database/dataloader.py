'''
2015-07-31 Nick Ponvert

Classes and methods for getting electrophysiology and behavior data
'''

import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior

class DataLoader(object):

    def __init__(self,
                 mode='offline',
                 animalName='',
                 date='',
                 experimenter='',
                 paradigm=''):

        '''
        I know you won't like the fact that we are including the paradigm here, but it allows us to
        interactively work with data by just giving the behavior suffix which is really nice

        If mode == 'online', we will set the local ephys path and behav path using the experimenter and animalName.
        If mode == 'offline', we will assume that paths relative to settings.EPHYS_PATH and settings.BEHAVIOR_PATH are passed

        Args: 
            mode (str): Must be either 'online' or 'offline'
            animalName (str): Name of the animal
            date (str): Date of the experiment in the format "2015-06-24"
            experimenter (str): Name of the experimenter for the behavior files
            paradigm (str): Paradigm with which the data was collected
        '''

        print "FIXME: Hardcoded ephys sampling rate in DataLoader __init__"
        self.EPHYS_SAMPLING_RATE = 30000.0

        self.mode=mode

        if self.mode=='offline':
            self.experimenter = experimenter #This will go away in the future

        if self.mode=='online':
            self.animalName = animalName
            self.date = date
            self.experimenter = experimenter
            self.paradigm=paradigm
            self.behavFileBaseName = '_'.join([self.animalName, self.paradigm, ''.join(self.date.split('-'))])
            self.onlineBehavPath = os.path.join(settings.BEHAVIOR_PATH, self.experimenter)
            self.onlineEphysPath = os.path.join(settings.EPHYS_PATH, self.animalName)


    def get_session_filename(self, session):

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
            filesFromToday = [f for f in os.listdir(self.onlineEphysPath) if (f.startswith(self.date) & ('_kk' not in f))]
            ephysSession = sorted(filesFromToday)[session]

            return ephysSession

    def get_session_events(self, session):
        '''
        Gets the event data for a session.
        The event data is not modified. Timestamps are not converted to seconds at this point

        '''

        if self.mode=='online':
            ephysSession = self.get_session_filename(session) #The ephys session will not be relaive to the mouse
            fullEventFilename=os.path.join(self.onlineEphysPath, ephysSession, 'all_channels.events')

        elif self.mode=='offline': #The path should already be relative to the mouse
            fullEventFilename = os.path.join(settings.EPHYS_PATH, session, 'all_channels.events')

        eventData=loadopenephys.Events(fullEventFilename)

        #Convert the timestamps to seconds
        eventData.timestamps = np.array(eventData.timestamps)/self.EPHYS_SAMPLING_RATE

        return eventData


    @staticmethod
    def get_event_onset_times(eventData, eventID=1, eventChannel=0, minEventOnsetDiff=0.5):
        '''
        Calculate event onset times given an eventData object.
        Accepts a jaratoolbox.loadopenephys.Events object and finds the event onset times.

        '''

        evID=np.array(eventData.eventID)
        evChannel = np.array(eventData.eventChannel)

        eventTimes = np.array(eventData.timestamps)
        eventOnsetTimes=eventTimes[(evID==eventID)&(evChannel==eventChannel)]

        #Restrict to events are seperated by more than the minimum event onset time
        evdiff = np.r_[1.0, np.diff(eventOnsetTimes)]
        eventOnsetTimes=eventOnsetTimes[evdiff>minEventOnsetDiff]

        return eventOnsetTimes

    def get_session_spikes(self, session, tetrode, cluster=None, electrodeName='Tetrode'):
        '''
        Get the spike data for one session, one tetrode.

        Method to retrieve the spike data for a session/tetrode. Automatically loads the
        clusters if clustering has been done for the session. This method converts the spike
        timestamps to seconds by default.

        Args:
            session (str or int): If a string, then must be either the full name of the ephys file (e.g. '2015-06-24_12-24-03') or just the timestamp portion of the file ('12-24-03'), in which case self.date will be used to construct the full file name. If an int, then the files that were recorded on self.date will be sorted, and the value provided will be used to index the sorted list. Therefore, -1 will return the session with the latest timestamp on the recording day.

            tetrode (int): The tetrode number to retrieve

            electrodeName (str): The name preceeding the electrode number, saved by openephys eg 'Tetrode6.spikes' needs 'Tetrode'

        Returns:
            spikeData (object of type jaratoolbox.loadopenephys.DataSpikes)
        '''
        if self.mode=='online':
            ephysSession = self.get_session_filename(session)
            spikeFilename = os.path.join(self.onlineEphysPath, ephysSession, '{0}{1}.spikes'.format(electrodeName, tetrode))

        elif self.mode=='offline': #The session should already be relative to the mouse
            spikeFilename = os.path.join(settings.EPHYS_PATH, session, '{0}{1}.spikes'.format(electrodeName, tetrode))

        spikeData = loadopenephys.DataSpikes(spikeFilename)

        #Make samples an empty array if there are no spikes
        if not hasattr(spikeData, 'samples'):
            spikeData.samples = np.array([])

        #Convert the spike samples to mV
        spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
        spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples

        #Make timestamps an empty array if it does not exist
        if not hasattr(spikeData, 'timestamps'):
            spikeData.timestamps = np.array([])

        #Convert the timestamps to seconds
        spikeData.timestamps = spikeData.timestamps/self.EPHYS_SAMPLING_RATE

        #If clustering has been done for the tetrode, add the clusters to the spikedata object
        if self.mode=='online':
            clustersDir = os.path.join(settings.EPHYS_PATH,'%s/%s_kk/'%(self.animalName,ephysSession)) #FIXME: Change to python 3 compatible format
            clustersFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
        elif self.mode=='offline':
            clustersFile = os.path.join(settings.EPHYS_PATH, '{}_kk/'.format(session), 'Tetrode{}.clu.1'.format(tetrode))

        if os.path.isfile(clustersFile):
            spikeData.set_clusters(clustersFile)

        if cluster:
            spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
            spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]
            
        return spikeData

    def get_session_behavior(self, behavFileName):

        if self.mode=='online':
            behaviorDir=os.path.join(self.onlineBehavPath, self.animalName)
            fullBehavFilename = ''.join([self.behavFileBaseName, behavFileName, '.h5'])
            behavDataFilePath=os.path.join(behaviorDir, fullBehavFilename)

        elif self.mode=='offline': #The path should already be relative to the mouse
            print "Fixme: Stop dividing the behavior by experimenter and change this method"
            behavDataFilePath = os.path.join(settings.BEHAVIOR_PATH, self.experimenter, behavFileName)

        bdata = loadbehavior.BehaviorData(behavDataFilePath,readmode='full')
        return bdata

    # def get_full_session_path(self, session):
    #     '''
    #     Constructs the full session path for use as a plot title
    #     '''
    #     ephysSession = self.get_session_filename(session)
    #     fullPath = os.path.join(self.localEphysDir, ephysSession)
    #     return fullPath

    def get_cluster_data(self, clusterObj, sessionType=None):
        '''
        A method that will take a cluster object and return data objects. 
        '''
        ephysFn, behavFn = clusterObj.get_data_filenames(sessionType)

        spikeData = self.get_session_spikes(ephysFn, clusterObj.tetrode, clusterObj.cluster)
        eventData = self.get_session_events(ephysFn)

        behavData = None

        if behavFn:
            behavData = self.get_session_behavior(behavFn)

        return spikeData, eventData, behavData

        
