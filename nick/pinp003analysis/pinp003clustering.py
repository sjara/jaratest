from jaratoolbox import settings
from jaratoolbox import spikesorting
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from pylab import *
import numpy as np
reload(spikesorting)
import os
SAMPLING_RATE=30000.0
timeRange=[-0.5, 1]

#This will cluster a single tetrode from a single session. 
#We will need to go beyond this a bit, but this should be interesting
animalName = 'pinp003'
ephysSession = '2015-06-22_18-39-21'
tetrode = 6
'''
oneTT = spikesorting.TetrodeToCluster(animalName,ephysSession,tetrode)

oneTT.load_waveforms()
oneTT.create_fet_files()
oneTT.run_clustering()
oneTT.save_report()
'''
# Now how do we get the cluster number for each spike? 
#At this point the clusters are stored in oneTT.dataTT.clusters
#However, we can load the clusters by having a DataSpikes object and running        

spike_filename=os.path.join(settings.EPHYS_PATH, animalName, ephysSession, 'Tetrode{0}.spikes'.format(tetrode))
sp=loadopenephys.DataSpikes(spike_filename)
clustersDir = os.path.join(settings.EPHYS_PATH,'%s/%s_kk/'%(animalName,ephysSession))
clustersFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
sp.set_clusters(clustersFile)

event_filename=os.path.join(settings.EPHYS_PATH, animalName, ephysSession, 'all_channels.events')
ev=loadopenephys.Events(event_filename)

eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
evChannel = np.array(ev.eventChannel)
eventOnsetTimes=eventTimes[(evID==1)&(evChannel==0)]


evdiff = np.r_[1.0, np.diff(eventOnsetTimes)]
eventOnsetTimes=eventOnsetTimes[evdiff>0.5]

#Already divided by the sampling rate in spikesorting
allSpkTimestamps = np.array(sp.timestamps)/SAMPLING_RATE
#allSpkTimestamps = np.array(oneTT.dataTT.timestamps)
spkClusters = sp.clusters

clustersToPlot = [2, 3, 4, 5, 6, 7]
clf()
for ind, clusterNum in enumerate(clustersToPlot):
    clusterspikes = allSpkTimestamps[spkClusters==clusterNum]

    spkTimeStamps = clusterspikes


    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

    subplot(len(clustersToPlot), 1, ind+1)

    plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.', ms=1)
    title('Cluster {}'.format(clusterNum))
    axvline(x=0, ymin=0, ymax=1, color='r')
    
xlabel('Time (sec)')
#tight_layout()
draw()
show()
