
#!/usr/bin/env python
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0
timeRange=[-0.5, 1] #In seconds

#########################
ephysDir='/home/nick/data/ephys/hm4d002/2014-08-04_18-04-45'  #Setting filepath 
ephysRoot= '/home/nick/data/ephys/hm4d002/'
ephysSession=sort(os.listdir(ephysRoot))[-1]
#ephysDir=os.path.join(ephysRoot, ephysSession)

numTetrodes = 4
#########################

event_filename=os.path.join(ephysDir, 'all_channels.events')

behaviorDir='/home/nick/data/behavior/nick/hm4d002/'
behavDataFileName=os.path.join(behaviorDir, 'hm4d002_tuning_curve_20140804a.h5')

bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')

freqEachTrial = bdata['currentFreq'] # Returns an array containing the freq of the
                                     # presented sound each trial

possibleFreq = np.unique(freqEachTrial) 

sortedTrials = []
for indf,oneFreq in enumerate(possibleFreq):
    indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
    sortedTrials = np.concatenate((sortedTrials,indsThisFreq))
sortingInds = argsort(sortedTrials)


#Load event data and convert event timestamps to ms
ev=loadopenephys.Events(event_filename)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
eventOnsetTimes=eventTimes[evID==1]
eventOnsetTimes=eventOnsetTimes[:-1] # The last behavior trial is always started but never finishe
                                     # by the time that we stop the paradigm
clf()

sortedFreqs = sorted(bdata['currentFreq'])

for ind in range(numTetrodes):
    tetrodeID = ind+1
    spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
    sp=loadopenephys.DataSpikes(spike_filename)
    try:
        spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

	sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]

        subplot(numTetrodes,1,ind+1)

        #plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
        scatter(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1, c=sortedFreqs)
        jet()
        axvline(x=0, ymin=0, ymax=1, color='r')
	if ind == 0:
	    title(ephysDir)
        #title('Channel {0} spikes'.format(ind+1))
    except AttributeError:  #Spikes files without any spikes will throw an error
        pass

xlabel('time(sec)')
#tight_layout()
draw()
show()
