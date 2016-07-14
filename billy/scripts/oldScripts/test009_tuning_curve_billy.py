'''
Plot the average firing rate in response to each frequency presented.
'''

from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0
timeRange=[-0.5, 1] #In seconds

subject = 'test019'
day = '20141224a'


#ephysDir='/home/billywalker/data/ephys/'
#fullephysDir = ephysDir+subject+'/'
ephysRoot = '/home/billywalker/data/ephys/'
fullephysRoot = ephysRoot+subject+'/'
#ephysSession=sort(os.listdir(fullephysRoot))[-1]
ephysSession = '2014-12-24_18-27-46'
fullephysDir = os.path.join(fullephysRoot, ephysSession)
event_filename=os.path.join(fullephysDir, 'all_channels.events')

numTetrodes = 8
behaviorDir='/home/billywalker/data/behavior/santiago/'
fullbehaviorDir = behaviorDir+subject+'/'
behavName = subject+'_tuning_curve_'+day+'.h5'
behavDataFileName=os.path.join(fullbehaviorDir, behavName)

bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
freqEachTrial = bdata['currentFreq']
possibleFreq = np.unique(freqEachTrial)
numberOfTrials = len(freqEachTrial)

# -- The old way of sorting (useful for plotting sorted raster) --
sortedTrials = []
numTrialsEachFreq = []  #Used to plot lines after each group of sorted trials
for indf,oneFreq in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
    indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq) #this gives indices of this frequency
    sortedTrials = np.concatenate((sortedTrials,indsThisFreq)) #adds all indices to a list called sortedTrials
    numTrialsEachFreq.append(len(indsThisFreq)) #finds number of trials each frequency has
sortingInds = argsort(sortedTrials) #gives array of indices that would sort the sortedTrials

# -- Load event data and convert event timestamps to ms --
ev=loadopenephys.Events(event_filename) #load ephys data (like bdata structure)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
evID=np.array(ev.eventID)  #loads the onset times of events (matches up with eventID to say if event 1 went on (1) or off (0)
eventOnsetTimes=eventTimes[evID==1] #array that is a time stamp for when the chosen event happens.
#ev.eventChannel woul load array of events like trial start and sound start and finish times (sound event is 0 and trial start is 1 for example). There is only one event though and its sound start
while (numberOfTrials < len(eventOnsetTimes)):
    eventOnsetTimes = eventOnsetTimes[:-1]


for tetrodeID in range(1,numTetrodes+1):

    raw_input("Press Enter to continue...")
    spike_filename=os.path.join(fullephysDir, 'Tetrode{0}.spikes'.format(tetrodeID)) #make a path to ephys spike data of specified tetrode tetrodeID
    sp=loadopenephys.DataSpikes(spike_filename) #load spike data from specified tetrode tetrodeID
    spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE #array of timestamps for each spike in seconds (thats why you divide by sampling rate)
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
    '''
        Create a vector with the spike timestamps w.r.t. events onset.

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = 
            eventlocked_spiketimes(timeStamps,eventOnsetTimes,timeRange)

        timeStamps: (np.array) the time of each spike.
        eventOnsetTimes: (np.array) the time of each instance of the event to lock to.
        timeRange: (list or np.array) two-element array specifying time-range to extract around event.

        spikeTimesFromEventOnset: 1D array with time of spikes locked to event.
    o    trialIndexForEachSpike: 1D array with the trial corresponding to each spike.
           The first spike index is 0.
        indexLimitsEachTrial: [2,nTrials] range of spikes for each trial. Note that
           the range is from firstSpike to lastSpike+1 (like in python slices)
        spikeIndices
    '''

    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike


    # -- Calculate tuning --
    responseRange = [0.010,0.020] #range of time to count spikes in after event onset
    nSpikes = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange) #array of the number of spikes in range for each trial
    '''Count number of spikes on each trial in a given time range.

           spikeTimesFromEventOnset: vector of spikes timestamps with respect
             to the onset of the event.
           indexLimitsEachTrial: each column contains [firstInd,lastInd+1] of the spikes on a trial.
           timeRange: time range to evaluate. Spike times exactly at the limits are not counted.

           returns nSpikes
    '''
    meanSpikesEachFrequency = np.empty(len(possibleFreq)) #make empty array of same size as possibleFreq

    # -- This part will be replace by something like behavioranalysis.find_trials_each_type --
    trialsEachFreq = []
    for indf,oneFreq in enumerate(possibleFreq):
        trialsEachFreq.append(np.flatnonzero(freqEachTrial==oneFreq)) #finds indices of each frequency. Appends them to get an array of indices of trials sorted by freq

    # -- Calculate average firing for each freq --
    for indf,oneFreq in enumerate(possibleFreq):
        meanSpikesEachFrequency[indf] = np.mean(nSpikes[trialsEachFreq[indf]])

    clf()
    ax2 = plt.subplot2grid((1,4), (0, 0), colspan=3)
    plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')

    #The cumulative sum of the list of specific frequency presentations, 
    #used below for plotting the lines across the figure. 
    numTrials = cumsum(numTrialsEachFreq)

    #Plot the lines across the figure in between each group of sorted trials
    for indf, num in enumerate(numTrials):
        ax2.axhline(y = num, xmin = 0, xmax = 1, color = '0.90', zorder = 0)
        #ax2.text(timeRange[0]-0.075, numTrials - mean(numTrialsEachFreq)/2, "%0.2f" % (possibleFreq[indf]/1000), color = 'grey', va = 'center')

    tickPositions = numTrials - mean(numTrialsEachFreq)/2
    tickLabels = ["%0.2f" % (possibleFreq[indf]/1000) for indf in range(len(possibleFreq))]
    ax2.set_yticks(tickPositions)
    ax2.set_yticklabels(tickLabels)
    ylabel('Frequency Presented (kHz), {} total trials'.format(numTrials[-1]))
    title(fullephysDir+' TT{0}'.format(tetrodeID))
    xlabel('Time (sec)')


    ax2 = plt.subplot2grid((1,4), (0, 3), colspan=1)
    ax2.set_xscale('log')
    plot(possibleFreq,meanSpikesEachFrequency,'o-')
    ylabel('Avg spikes in window {0}-{1} sec'.format(*responseRange))
    xlabel('Frequency')

    show()



