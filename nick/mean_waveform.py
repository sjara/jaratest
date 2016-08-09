from jaratoolbox import loadopenephys
from jaratoolbox import settings
from jaratoolbox import spikesorting
import numpy as np

subject = 'test098'
date = '2016-07-26'
time = '12-18-39'
tetrode = 1
cluster = 2

session = '{}_{}'.format(date, time)
ephysDir = os.path.join(settings.EPHYS_PATH, subject, session)
clusterDir = os.path.join(settings.EPHYS_PATH, subject, '{}_kk'.format(session))

ephysFn = os.path.join(ephysDir, 'Tetrode{}.spikes'.format(tetrode))
clusterFn = os.path.join(clusterDir, 'Tetrode{}.clu.1'.format(tetrode))

#Load the samples
dataSpikes = loadopenephys.DataSpikes(spikesFn)
dataSpikes.samples = dataSpikes.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
dataSpikes.samples = (1000.0/dataSpikes.gain[0,0]) * dataSpikes.samples

#Set the clusters
dataSpikes.set_clusters(clusterFn)

#Select which cluster to use
spikesThisCluster = dataSpikes.clusters == cluster
dataSpikes.samples = dataSpikes.samples[spikesThisCluster, :, :]
dataSpikes.timestamps = dataSpikes.timestamps[spikesThisCluster]

#Align the waveforms
alignedWaves = spikesorting.align_waveforms(dataSpikes.samples)

#calculate and return mean
meanWaveform = np.mean(alignedWaves,axis=0)

figure()
clf()
plot(meanWaveform[0,:])

