#Just functions that load data when given a 'cell' from the celldatabase

from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import settings
import numpy as np
import sys
import os

def get_session_inds(cell, sessiontype):
    '''
    Get the index of a particular sessiontype for a cell.
    Args:
        cell (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
                              This function requires the 'sessiontype' field, which must contain a list of strings.
        sessiontype (str): The type of session

    Returns:
        sessionInds (list): A list of indices where cell['sessiontype'] and the sessiontype arg match.
    '''
    sessionInds = [i for i, st in enumerate(cell['sessiontype']) if st==sessiontype]
    return sessionInds

def get_session_bdata(cell, sessiontype):
    '''
    Load the behavior data from a cell for a single session.
    Args:
        cell (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
                              This function requires the 'sessiontype' field, which must contain a list of strings.
        sessiontype (str): The type of session

    Returns:
        bdata (jaratoolbox.loadbehavior.BehaviorData): The behavior data for the session
    '''
    sessionInds = get_session_inds(cell, sessiontype)
    sessionInd = sessionInds[0] #FIXME: Just takes the first one for now
    behavFile = cell['behavior'][sessionInd]
    behavDataFilePath=os.path.join(settings.BEHAVIOR_PATH, cell['subject'], behavFile)
    bdata = loadbehavior.BehaviorData(behavDataFilePath,readmode='full')
    return bdata

def convert_openephys(dataObj):
    '''
    Converts samples to millivolts and timestamps to seconds.
    Args:
        dataObj (jaratoolbox.loadopenephys data object): Can be a DataSpikes, DataCont, or Events object.
    Returns:
        dataObj: Returns the same dataObj with samples and timestamps converted.
    '''
    if hasattr(dataObj, 'samples'):
        dataObj.samples = dataObj.samples.astype(float)-2**15
        dataObj.samples = (1000.0/dataObj.gain[0,0]) * dataObj.samples
    if hasattr(dataObj, 'timestamps'):
        dataObj.timestamps = dataObj.timestamps/dataObj.samplingRate
    return dataObj

def get_session_ephys(cell, sessiontype):
    '''
    Load the spikes and events from a cell for a single session.
    Args:
        cell (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
        sessiontype (str): The type of session
    Returns:
        spikeData (jaratoolbox.loadopenephys.DataSpikes): The spike data for the session
        eventData (jaratoolbox.loadopenephys.Events): The event data for the session
    '''
    sessionInds = get_session_inds(cell, sessiontype)
    sessionInd = sessionInds[0] #FIXME: Just takes the first one for now
    ephysSession = cell['ephys'][sessionInd]
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, cell['subject'])
    tetrode=int(cell['tetrode'])
    eventFilename=os.path.join(ephysBaseDir,
                               ephysSession,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                ephysSession,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    if spikeData.timestamps is not None:
        clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(ephysSession))
        clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
        spikeData.set_clusters(clustersFile)
        spikeData.samples=spikeData.samples[spikeData.clusters==cell['cluster']]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cell['cluster']]
        spikeData = convert_openephys(spikeData)
    eventData = convert_openephys(eventData)
    return spikeData, eventData

def load_all_spikedata(cell):
    '''
    Load the spike data for all recorded sessions into a set of arrays.
    Args:
        cell (pandas.Series): One row from a pandas cell database created using generate_cell_database or by
                              manually constructing a pandas.Series object that contains the required fields.
    Returns:
        timestamps (np.array): The timestamps for all spikes across all sessions
        samples (np.array): The samples for all spikes across all sessions
        recordingNumber (np.array): The index of the session where the spike was recorded
    '''

    samples=np.array([])
    timestamps=np.array([])
    recordingNumber=np.array([])

    for ind, sessionType in enumerate(cell['sessiontype']):
        dataSpkObj, dataEvents = get_session_ephys(cell, sessionType)
        if (dataSpkObj.timestamps is None) or (len(dataSpkObj.timestamps)==0):
            continue

        numSpikes = len(dataSpkObj.timestamps)
        sessionVector = np.zeros(numSpikes)+ind

        if len(samples)==0:
            samples = dataSpkObj.samples
            timestamps = dataSpkObj.timestamps
            recordingNumber = sessionVector
        else:
            samples = np.concatenate([samples, dataSpkObj.samples])
            # Check to see if next session ts[0] is lower than self.timestamps[-1]
            # If so, add self.timestamps[-1] to all new timestamps before concat
            if dataSpkObj.timestamps[0]<timestamps[-1]:
                dataSpkObj.timestamps = dataSpkObj.timestamps + timestamps[-1]
            timestamps = np.concatenate([timestamps, dataSpkObj.timestamps])
            recordingNumber = np.concatenate([recordingNumber, sessionVector])

    return timestamps, samples, recordingNumber
