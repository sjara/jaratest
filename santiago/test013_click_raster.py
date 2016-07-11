#!/usr/bin/env python
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0
timeRange=[-0.4, 1.6] #In seconds

subject = sys.argv[1]
if len(sys.argv)>2:
    sessionInd = int(sys.argv[2])
else:
    sessionInd=-1

#########################
#ephysDir='/home/jarauser/data/ephys/hm4d002/2014-08-04_17-11-30'
#ephysRoot= '/home/nick/data/ephys/hm4d002/'
#ephysRoot= '/home/jarauser/data/ephys/rata002/'
#ephysRoot= '/home/jarauser/data/ephys/pinp001/'
#subject = 'pinp001'
ephysRoot = os.path.join(settings.EPHYS_PATH, subject)
ephysSession = sort(os.listdir(ephysRoot))[sessionInd]
ephysDir = os.path.join(ephysRoot, ephysSession)

tetrodes = [3,4,5,6]
nTetrodes = len(tetrodes)
#########################

event_filename=os.path.join(ephysDir, 'all_channels.events')

#Load event data and convert event timestamps to ms
ev=loadopenephys.Events(event_filename)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
eventOnsetTimes=eventTimes[evID==1]
clf()

ax = [subplot(nTetrodes,1,1)]
for ind,tetrodeID in enumerate(tetrodes):
    #tetrodeID = ind+1
    spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
    sp=loadopenephys.DataSpikes(spike_filename)
    try:
        spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

        ax.append(subplot(nTetrodes,1,ind+1,sharex=ax[0]))

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

