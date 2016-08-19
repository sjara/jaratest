#!/usr/bin/env python
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0
timeRange=[-0.4, 0.5] #In seconds
timeRange=[-0.3, 1] #In seconds

#########################
##ephysDir='/home/jarauser/data/ephys/test089/2015-06-18_14-13-38'
ephysRoot= '/home/jarauser/data/ephys/test087'
ephysSession=sort(os.listdir(ephysRoot))[-1]
ephysDir=os.path.join(ephysRoot, ephysSession)

numTetrodes = 8
#########################

event_filename=os.path.join(ephysDir, 'all_channels.events')

#Load event data and convert event timestamps to ms
ev=loadopenephys.Events(event_filename)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
eventOnsetTimes=eventTimes[evID==1]
clf()


for ind in range(numTetrodes):
    tetrodeID = ind+1
    spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
    sp=loadopenephys.DataSpikes(spike_filename)
    try:
        spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        subplot(numTetrodes,1,ind+1)

        plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.',ms=1)
        axvline(x=0, ymin=0, ymax=1, color='r')
        xlim(timeRange)
	if ind == 0:
	    title(ephysDir)
        #title('Channel {0} spikes'.format(ind+1))
    except AttributeError:  #Spikes files without any spikes will throw an error
        pass

xlabel('time(sec)')
#tight_layout()
draw()
show()

