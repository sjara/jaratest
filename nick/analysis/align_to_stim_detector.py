from matplotlib import pyplot as plt
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import extraplots
from jaratest.nick.database import dataplotter
import os

# exp0.add_session('15-57-52', 'i', 'am', 'am_tuning_curve')

def convert_openephys(dataObj):
    '''
    Converts to seconds and milivolts
    '''
    if hasattr(dataObj, 'samples'):
        dataObj.samples = dataObj.samples.astype(float)-2**15
        dataObj.samples = (1000.0/dataObj.gain[0,0]) * dataObj.samples
    if hasattr(dataObj, 'timestamps'):
        dataObj.timestamps = dataObj.timestamps/dataObj.samplingRate
    return dataObj

subject = 'pinp015'
session = '2017-01-26_15-57-52'

spikesFn = os.path.join(settings.EPHYS_PATH, subject, session, 'Tetrode1.spikes')
eventsFn = os.path.join(settings.EPHYS_PATH, subject, session, 'all_channels.events')

dataSpikes = loadopenephys.DataSpikes(spikesFn)
dataEvents = loadopenephys.Events(eventsFn)

dataSpikes = convert_openephys(dataSpikes)
dataEvents = convert_openephys(dataEvents)

behavFn = os.path.join(settings.BEHAVIOR_PATH, subject,'{}_am_tuning_curve_20170126i.h5'.format(subject))
bdata = loadbehavior.BehaviorData(behavFn)

stimSync = dataEvents.get_event_onset_times(eventID=1, eventChannel=0)
stimDetect = dataEvents.get_event_onset_times(eventID=1, eventChannel=5)

# dataplotter.plot_raster(stimDetect, stimSync, sortArray=bdata['currentFreq'], ms=0.5)


sortArray = bdata['currentFreq']
trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))

timeRange = [0, 0.5]
(spikeTimesFromEventOnset,
trialIndexForEachSpike,
indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(stimDetect,
                                                             stimSync,
                                                             timeRange)



pRaster, hcond, zline = extraplots.raster_plot(
    spikeTimesFromEventOnset,
    indexLimitsEachTrial,
    timeRange,
    trialsEachCond=trialsEachCond)
#Set the marker size for better viewing
ms = 1
plt.setp(pRaster, ms=ms)

ax = plt.gca()
ax.hold(True)

# A vector of the possible frequencies presented
freqEachTrial = bdata['currentFreq']
possibleFreq = np.unique(freqEachTrial)

# Sort the trials by looping through the possible frequencies
# and concatenating to the end of a list all of the trials where this 
# frequency was presented
sortedTrials = []
for indf,oneFreq in enumerate(possibleFreq):
    indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
    sortedTrials = np.concatenate((sortedTrials,indsThisFreq))
sortingInds = argsort(sortedTrials)



# Make a new vector of trial indices sorted according to the new order
trialIndexFirstEvents = trialIndexForEachSpike[indexLimitsEachTrial[0,:]]
sortedIndexForEachSpike = sortingInds[trialIndexFirstEvents[:-1]]
firstEvents = spikeTimesFromEventOnset[indexLimitsEachTrial[0,:][:-1]]

#Plot the sorted raster
plot(firstEvents, sortedIndexForEachSpike, 'r.')


