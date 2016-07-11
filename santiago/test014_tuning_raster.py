'''
Plot the average firing rate in response to each frequency presented.
'''

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
import numpy as np
from pylab import *
import os


SAMPLING_RATE=30000.0
timeRange=[-0.5, 1] #In seconds
responseRange = [0.0,0.100] # range of time to count spikes in after event onset

selectedIntensity = None #70

subject = 'pinp001'
#behavSession = '20150322a'; ephysSession = '2015-03-22_00-12-18'
#behavSession = '20150322b'; ephysSession = '2015-03-22_17-13-54'
behavSession = '20150322c'; ephysSession = '2015-03-22_17-40-55'
behavSession = '20150323b'; ephysSession = '2015-03-23_22-46-13'
tetrodes = [3,6]

nTetrodes = len(tetrodes)

#ephysSession=sort(os.listdir(fullephysRoot))[-1]
fullephysDir = os.path.join(settings.EPHYS_PATH,subject, ephysSession)
event_filename = os.path.join(fullephysDir, 'all_channels.events')

experimenter = settings.DEFAULT_EXPERIMENTER
paradigm = 'laser_tuning_curve'
behavDataFileName = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)

bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
freqEachTrial = bdata['currentFreq']
intensityEachTrial = bdata['currentIntensity']
nTrials = len(freqEachTrial)

# -- Load event data and convert event timestamps to ms --
ev = loadopenephys.Events(event_filename) # load ephys data (like bdata structure)
eventTimes = np.array(ev.timestamps)/SAMPLING_RATE # convert to seconds by dividing by sampling rate (Hz)
evID = np.array(ev.eventID)  # loads the onset times of events (matches up with eventID to say if event 1 went on (1) or off (0)
eventOnsetTimes = eventTimes[evID==1] # array that is a time stamp for when the chosen event happens.

if nTrials != len(eventOnsetTimes):
    print 'Number of behavior trials and ephys trials do not match. The longest will be cut.'
    minNtrials = min(nTrials,len(eventOnsetTimes))
    nTrials = minNtrials
    freqEachTrial = freqEachTrial[:nTrials]
    intensityEachTrial = intensityEachTrial[:nTrials]
    eventOnsetTimes = eventOnsetTimes[:nTrials]


possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)

# -- Find trials for each frequency and sort them --
if selectedIntensity is None:
    selectedTrials = np.ones(nTrials,dtype=bool)
else:
    selectedTrials = (intensityEachTrial==selectedIntensity)

freqEachTrial = freqEachTrial[selectedTrials]
trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
###trialsEachFreq &= selectedTrials[:,np.newaxis]
numTrialsEachFreq = trialsEachFreq.sum(axis=0)
sortedTrials = np.nonzero(trialsEachFreq.T)[1] # The second array contains the sorted indexes
sortingInds = np.argsort(sortedTrials) # gives array of indices that would sort the sortedTrials

eventOnsetTimes = eventOnsetTimes[selectedTrials]


for indt,tetrodeID in enumerate(tetrodes):

    spikesFilename = os.path.join(fullephysDir, 'Tetrode{0}.spikes'.format(tetrodeID)) # make a path to ephys spike data of specified tetrode tetrodeID
    sp = loadopenephys.DataSpikes(spikesFilename) # load spike data from specified tetrode tetrodeID
    spkTimeStamps = np.array(sp.timestamps)/SAMPLING_RATE # array of timestamps for each spike in seconds (thats why you divide by sampling rate)
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]

    # -- Calculate tuning --
    nSpikes = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
    meanSpikesEachFrequency = np.empty(len(possibleFreq)) # make empty array of same size as possibleFreq

    # -- Calculate average firing for each freq --
    for indf,oneFreq in enumerate(possibleFreq):
        meanSpikesEachFrequency[indf] = np.mean(nSpikes[trialsEachFreq[:,indf]])

    clf()
    ax2 = plt.subplot2grid((1,4), (0, 0), colspan=3)
    plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')

    #The cumulative sum of the list of specific frequency presentations, 
    #used below for plotting the lines across the figure. 
    cumTrials = cumsum(numTrialsEachFreq)

    #Plot the lines across the figure in between each group of sorted trials
    for indf, num in enumerate(cumTrials):
        ax2.axhline(y = num, xmin = 0, xmax = 1, color = '0.90', zorder = 0)
        #ax2.text(timeRange[0]-0.075, cumTrials - mean(numTrialsEachFreq)/2, "%0.2f" % (possibleFreq[indf]/1000), color = 'grey', va = 'center')

    tickPositions = cumTrials - mean(numTrialsEachFreq)/2
    tickLabels = ["%0.2f" % (possibleFreq[indf]/1000) for indf in range(len(possibleFreq))]
    ax2.set_yticks(tickPositions)
    ax2.set_yticklabels(tickLabels)
    ylabel('Frequency Presented (kHz), {} total trials'.format(cumTrials[-1]))
    title(fullephysDir+' TT{0}'.format(tetrodeID))
    xlabel('Time (sec)')


    ax2 = plt.subplot2grid((1,4), (0, 3), colspan=1)
    ax2.set_xscale('log')
    plot(possibleFreq,meanSpikesEachFrequency,'o-')
    ylabel('Avg spikes in window {0}-{1} sec'.format(*responseRange))
    xlabel('Frequency')

    show()

    waitforbuttonpress()
    #raw_input("Press Enter to continue...")

