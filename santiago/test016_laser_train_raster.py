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

ephysRoot = os.path.join(settings.EPHYS_PATH, subject)
ephysSession = sort(os.listdir(ephysRoot))[sessionInd]
ephysDir = os.path.join(ephysRoot, ephysSession)

tetrodes = [6]#3,4,5,6]
nTetrodes = len(tetrodes)

event_filename=os.path.join(ephysDir, 'all_channels.events')

#Load event data and convert event timestamps to ms
ev=loadopenephys.Events(event_filename)
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
eventOnsetTimes=eventTimes[(ev.eventID==1)&(ev.eventChannel==0)]
clf()

dEv = np.r_[1,np.diff(eventOnsetTimes)]
eventOnsetTimes = eventOnsetTimes[dEv>0.4]


ax = [subplot(nTetrodes,1,1)]
for ind,tetrodeID in enumerate(tetrodes):
    #tetrodeID = ind+1
    spikeFilename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
    sp=loadopenephys.DataSpikes(spikeFilename)

    # -- Load clusters --
    kkDataDir = os.path.dirname(spikeFilename)+'_kk'
    clusterFilename = 'Tetrode{0}.clu.1'.format(tetrodeID)
    fullPath = os.path.join(kkDataDir,clusterFilename)
    clusters = np.fromfile(fullPath,dtype='int32',sep=' ')[1:]
    
    clustersToPlot = [2,3,4,5,6,7]
    for indc,clusterID in enumerate(clustersToPlot):
        try:
            #spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
            spkTimeStamps=np.array(sp.timestamps[clusters==clusterID])/SAMPLING_RATE
            (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

            #ax.append(subplot(nTetrodes,1,ind+1,sharex=ax[0]))
            ax.append(subplot(len(clustersToPlot),1,indc+1,sharex=ax[0]))

            plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.',ms=3)
            axvline(x=0, ymin=0, ymax=1, color='r')
            xlim(timeRange)
            if indc == 0:
                title(ephysDir)
            #title('Channel {0} spikes'.format(ind+1))
            ylabel('T{0}c{1}'.format(tetrodeID,clusterID))
        except AttributeError:  #Spikes files without any spikes will throw an error
            print 'File empty: {0}'.format(spikeFilename)
            pass

xlabel('time(sec)')
#tight_layout()
draw()
show()

