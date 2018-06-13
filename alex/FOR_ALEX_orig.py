from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
reload(loadopenephys)
from jaratoolbox import settings
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy import stats
import os
import pdb

def load_ephys_data(subject, session, tetrode, cluster=None):
    ephysBaseDir = os.path.join(settings.EPHYS_PATH, subject)
    eventFilename=os.path.join(ephysBaseDir,
                               session,
                               'all_channels.events')
    spikesFilename=os.path.join(ephysBaseDir,
                                session,
                                'Tetrode{}.spikes'.format(tetrode))
    eventData=loadopenephys.Events(eventFilename)
    spikeData = loadopenephys.DataSpikes(spikesFilename)
    clustersDir = os.path.join(ephysBaseDir, '{}_kk'.format(session))
    clustersFile = os.path.join(clustersDir,'Tetrode{}.clu.1'.format(tetrode))
    spikeData.set_clusters(clustersFile)
    if cluster is not None:
        spikeData.samples=spikeData.samples[spikeData.clusters==cluster]
        spikeData.timestamps=spikeData.timestamps[spikeData.clusters==cluster]
    
    # convert to seconds and millivolts
    spikeData.samples = spikeData.samples.astype(float)-2**15
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    spikeData.timestamps = spikeData.timestamps/spikeData.samplingRate
    eventData.timestamps = eventData.timestamps/eventData.samplingRate
    return eventData, spikeData
    
def load_behaviour_data(subject, fileName):
    behavFile = os.path.join(settings.BEHAVIOR_PATH,subject,fileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')
    return bdata

# LOAD YOUR SHIT
eventData, spikeData = load_ephys_data(SUBJECT, EPHYSSESSION, tetrode, cluster)
eventOnsetTimes = eventData.get_event_onset_times()
spikeTimeStamps = spikeData.timestamps
tuningBData = load_behaviour_data(SUBJECT, BEHAVIORSESSION)   

freqEachTrial = tuningBData['currentFreq']

trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, np.unique(freqEachTrial))
spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
    spikeTimeStamps, eventOnsetTimes, timeRange)
pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,
                                               trialsEachCond=trialsEachCond, *args, **kwargs)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.setp(pRaster, ms=ms)