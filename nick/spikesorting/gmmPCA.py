
from jaratoolbox import loadopenephys
from jaratoolbox import spikesorting
from jaratoolbox.test.nick import clustercutting
from matplotlib import pyplot as plt
import os
import numpy as np

import sklearn
import sklearn.manifold
import sklearn.neighbors
import sklearn.mixture





animalname='adap020'
ephysloc = '/home/nick/data/ephys/'
ephyspath = os.path.join(ephysloc, animalname)
ephysfn='2016-05-25_16-33-09'
tetrode=2
spikesFn = os.path.join(ephyspath, ephysfn, 'Tetrode{}.spikes'.format(tetrode))
dataSpikes = loadopenephys.DataSpikes(spikesFn)

(numSpikes, numChans, numSamples) = np.shape(dataSpikes.samples)
allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

import timeit
start_time = timeit.default_timer()

U, s, Vt = np.linalg.svd(allWaves, full_matrices=False)

elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)







import timeit
start_time = timeit.default_timer()

X_pc = sklearn.decomposition.RandomizedPCA(n_components=50).fit_transform(allWaves)

elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)

wavesToUse = random.randint(len(X_pc), size=10000)
pcWavesToUse = X_pc[wavesToUse, :]

model = sklearn.mixture.GMM(n_components=12)


start_time = timeit.default_timer()
model.fit(pcWavesToUse)
elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)


start_time = timeit.default_timer()
clusters = model.predict(X_pc)
elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)


GAIN = 5000.0
SAMPLING_RATE=30000.0
dataSpikes.samples = ((dataSpikes.samples - 32768.0) / GAIN) * 1000.0
dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE

dataSpikes.clusters = clusters
spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename = 'test50PC_GMM.png')
