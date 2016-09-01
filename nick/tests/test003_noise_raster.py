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
#ephysDir='/home/nick/data/ephys/pinp003/2015-06-22_19-43-42'
ephysRoot= '/home/jarauser/data/ephys/pinp003/'
ephysSession=sort(os.listdir(ephysRoot))[-1]
ephysDir=os.path.join(ephysRoot, ephysSession)

numTetrodes = 4
tetrodeIDs = [3, 4, 5, 6]
#########################

event_filename=os.path.join(ephysDir, 'all_channels.events')

#Load event data and convert event timestamps to ms
ev=loadopenephys.Events(event_filename)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
evChannel = np.array(ev.eventChannel)
eventOnsetTimes=eventTimes[(evID==1)&(evChannel==0)]

evdiff = np.r_[1.0, np.diff(eventOnsetTimes)]
eventOnsetTimes=eventOnsetTimes[evdiff>0.5]

clf()


for ind , tetrodeID in enumerate(tetrodeIDs):
    spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
    sp=loadopenephys.DataSpikes(spike_filename)
    try:
        spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        subplot(numTetrodes,1,ind+1)

        plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.', ms=1)
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

