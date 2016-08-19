'''
loadEphysData.py
Load ephys events
author: Billy Walker
'''

from jaratoolbox import loadopenephys
import numpy as np
import os


def loadEphys(subject, ephysSession, tetrodeID):
    #####################################################################################################################################################################
    #PARAMETERS
    #####################################################################################################################################################################

    ephysRoot='/home/billywalker/data/ephys/'
    #ephysSession = '2014-12-24_17-11-53'
    #tetrodeID is which tetrode to plot
    #####################################################################################################################################################################
    #####################################################################################################################################################################


    # -- Global variables --
    SAMPLING_RATE=30000.0
    
    ephysRoot = ephysRoot + subject + '/' + 'psyCurve/'

    # -- Load event data and convert event timestamps to ms --
    ephysDir = os.path.join(ephysRoot, ephysSession)
    eventFilename=os.path.join(ephysDir, 'all_channels.events')
    events = loadopenephys.Events(eventFilename) # Load events data
    eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
    multipleEventOnset=np.array(events.eventID)  #loads the onset times of all events (matches up with eventID to say if event 1 went on (1) or off (0)
    eventChannel = np.array(events.eventChannel) #loads the ID of the channel of the event. For example, 0 is sound event, 1 is trial event, 2 ...

    # -- Load spike data and convert spike timestamps to ms --
    spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID)) #make a path to ephys spike data of specified tetrode tetrodeID
    spikeData=loadopenephys.DataSpikes(spike_filename) #load spike data from specified tetrode tetrodeID
    spkTimeStamps=np.array(spikeData.timestamps)/SAMPLING_RATE #array of timestamps for each spike in seconds (thats why you divide by sampling rate)
    
    
    return [eventTimes,multipleEventOnset,eventChannel,spkTimeStamps];
