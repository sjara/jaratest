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

    def __init__(self, subject, convertSeconds=True):

        '''
        Args:
            subject (str): The subject to load data for
            convertSeconds (bool): Whether to convert timestamps to seconds
        '''
        # print "FIXME: Hardcoded ephys sampling rate in DataLoader __init__"
        self.convertSeconds = convertSeconds
        self.subject = subject
        self.EPHYS_SAMPLING_RATE = 30000.0
        self.behavPath = os.path.join(settings.BEHAVIOR_PATH, subject)
        self.ephysPath = os.path.join(settings.EPHYS_PATH, subject)

    def get_session_events(self, sessionDir):
        '''
        Gets the event data for a session.
        '''

        eventFilename=os.path.join(self.ephysPath, sessionDir, 'all_channels.events')
        eventData=loadopenephys.Events(eventFilename)
        if self.convertSeconds:
            #Convert the timestamps to seconds
            eventData.timestamps = np.array(eventData.timestamps)/self.EPHYS_SAMPLING_RATE
        return eventData

    def get_session_cont(self, sessionDir, channel):

        contFilename = os.path.join(self.ephysPath, sessionDir, '109_CH{}.continuous'.format(channel))
        contData=loadopenephys.DataCont(contFilename) #FIXME: Convert to mV?
        return contData

    @staticmethod
    #TODO:This might be better as a method of the eventData object
    def get_event_onset_times(eventData, eventID=1, eventChannel=0, minEventOnsetDiff=0.5):
        '''
        Calculate event onset times given an eventData object.
        Accepts a jaratoolbox.loadopenephys.Events object and finds the event onset times.
        Looking for the right events: eventChannel==0 are the sound-onset events (use outbit0); eventChannel==2 are the laser-onset events (use outbit2). For now just look for all events with eventID==1.
        '''
        evID=np.array(eventData.eventID)
        evChannel = np.array(eventData.eventChannel)

        eventTimes = np.array(eventData.timestamps)

        if evID is not None:
            eventOnsetTimes=eventTimes[(evID==eventID)&(evChannel==eventChannel)]
        else:
            eventOnsetTimes=eventTimes[evChannel==eventChannel]


        #Restrict to events are seperated by more than the minimum event onset time
        #TODO: Make the default None, not the setting for laser trains
        if minEventOnsetDiff is not None:
            evdiff = np.r_[1.0, np.diff(eventOnsetTimes)]
            eventOnsetTimes=eventOnsetTimes[evdiff>minEventOnsetDiff]

        return eventOnsetTimes

    def get_session_spikes(self, sessionDir, tetrode, cluster=None, electrodeName='Tetrode'):
        '''
        Get the spike data for one session, one tetrode.

        Method to retrieve the spike data for a session/tetrode. Automatically loads the
        clusters if clustering has been done for the session. This method converts the spike
        timestamps to seconds by default.

        Args:
            sessionDir (str): The ephys directory
            tetrode (int): The tetrode number to retrieve
            electrodeName (str): The name preceeding the electrode number, saved by openephys eg 'Tetrode6.spikes' needs 'Tetrode'

        Returns:
            spikeData (object of type jaratoolbox.loadopenephys.DataSpikes)
        '''
        spikeFilename = os.path.join(self.ephysPath, sessionDir, '{}{}.spikes'.format(electrodeName, tetrode))

        spikeData = loadopenephys.DataSpikes(spikeFilename)

        #TODO: Why do we need this?
        #Make samples an empty array if there are no spikes
        if not hasattr(spikeData, 'samples'):
            spikeData.samples = np.array([])

        #TODO: Make this an option
        #Convert the spike samples to mV
        spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
        spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples

        #Make timestamps an empty array if it does not exist
        if not hasattr(spikeData, 'timestamps'):
            spikeData.timestamps = np.array([])

        #Convert the timestamps to seconds
        if self.convertSeconds:
            spikeData.timestamps = spikeData.timestamps/self.EPHYS_SAMPLING_RATE

        #If clustering has been done for the tetrode, add the clusters to the spikedata object
        clustersDir = os.path.join(self.ephysPath, '{}_kk'.format(sessionDir))
        clustersFile = os.path.join(clustersDir,'{}{}.clu.1'.format(electrodeName, tetrode))
        # print clustersFile #NOTE: For debugging
        if os.path.isfile(clustersFile):
            spikeData.set_clusters(clustersFile)

        if cluster:
            spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
            spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]

        return spikeData

    def get_session_behavior(self, behavFileName):

        behavDataFilePath=os.path.join(self.behavPath, behavFileName)
        bdata = loadbehavior.BehaviorData(behavDataFilePath,readmode='full')
        return bdata

if __name__=="__main__":

    loader = DataLoader('adap015')
    sessionDir = '2016-02-05_14-33-42'
    # spikeData = loader.get_session_spikes(sessionDir, 1)
    eventData = loader.get_session_events(sessionDir)
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    behavData = loader.get_session_behavior('adap015_2afc_20160205a.h5')
    contData = loader.get_session_cont(sessionDir, 33)
