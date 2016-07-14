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


ephysDir='/home/nick/data/ephys/test075/'
ephysRoot = '/home/nick/data/ephys/test075'
#ephysSession=sort(os.listdir(ephysRoot))[-1]
ephysSession = '2014-11-06_17-27-43'
ephysDir = os.path.join(ephysRoot, ephysSession)
event_filename=os.path.join(ephysDir, 'all_channels.events')

numTetrodes = 4


behaviorDir='/home/nick/data/behavior/nick/test075/'
behavDataFileName=os.path.join(behaviorDir, 'test075_tuning_curve_20141106a.h5')

bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
freqEachTrial = bdata['currentFreq']
possibleFreq = np.unique(freqEachTrial)

# -- The old way of sorting (useful for plotting sorted raster) --
sortedTrials = []
numTrialsEachFreq = []  #Used to plot lines after each group of sorted trials
for indf,oneFreq in enumerate(possibleFreq):
    indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
    sortedTrials = np.concatenate((sortedTrials,indsThisFreq))
    numTrialsEachFreq.append(len(indsThisFreq))
sortingInds = argsort(sortedTrials)

# -- Load event data and convert event timestamps to ms --
ev=loadopenephys.Events(event_filename)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
eventOnsetTimes=eventTimes[evID==1]

tetrodeID = 3
spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
sp=loadopenephys.DataSpikes(spike_filename)
spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]


# -- Calculate tuning --
responseRange = [0.010,0.020]
nSpikes = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
meanSpikesEachFrequency = np.empty(len(possibleFreq))

# -- This part will be replace by something like behavioranalysis.find_trials_each_type --
trialsEachFreq = []
for indf,oneFreq in enumerate(possibleFreq):
    trialsEachFreq.append(np.flatnonzero(freqEachTrial==oneFreq))

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
title(ephysDir+' TT{0}'.format(tetrodeID))
xlabel('Time (sec)')


ax2 = plt.subplot2grid((1,4), (0, 3), colspan=1)
ax2.set_xscale('log')
plot(possibleFreq,meanSpikesEachFrequency,'o-')
ylabel('Avg spikes in window {0}-{1} sec'.format(*responseRange))
xlabel('Frequency')

show()



