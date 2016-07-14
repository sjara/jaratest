#Testing the SOMPY library:
#https://github.com/sevamoo/SOMPY


#The module is pretty badly documented but seems to have some nice functions implemented already...
#http://nbviewer.jupyter.org/gist/sevamoo/ec0eb28229304f4575085397138ba5b1


import pandas as pd
import time as time
import numpy as np
from matplotlib import pyplot as plt
import sys
import SOMPY


#The critical factor which increases the computational time, but mostly the memory problem is the size of SOM (i.e. msz0,msz1),
#other wise the training data will be parallelized


#This is your selected map size
msz0 = 30
msz1 = 30

#This is a random data set, but in general it is assumed that you have your own data set as a numpy ndarray
data = np.random.rand(10*1000,20)
print 'Data size: ', data.shape


sm = SOMPY.sompy.SOM(data, neighborhood=SOMPY.neighborhood.GaussianNeighborhood(), normalizer=SOMPY.normalization.VarianceNormalizator(), mapsize = [msz0, msz1], initialization='pca', name='sm', )
sm.train(n_job = 1, shared_memory = 'no')


h = sompylib.hitmap.HitMapView(10, 10, 'hitmap', text_size=8, show_text=True)
h.show(sm)



###Testing on spike data
from jaratoolbox import loadopenephys
from jaratoolbox import spikesorting
from jaratoolbox.test.nick import clustercutting
from matplotlib import pyplot as plt
import os
animalName='pinp013'
ephysLoc = '/home/nick/data/ephys/'
ephysPath = os.path.join(ephysLoc, animalName)
ephysFn='2016-05-27_14-13-26'
tetrode=3
spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode{}.spikes'.format(tetrode))


dataSpikes = loadopenephys.DataSpikes(spikesFn)

GAIN = 5000.0
SAMPLING_RATE=30000.0
dataSpikes.samples = ((dataSpikes.samples - 32768.0) / GAIN) * 1000.0
dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE

(numSpikes, numChans, numSamples) = shape(dataSpikes.samples)

allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

#Testing larger data sizes
### Looks like even with 3 times the spikes the algo is still fast
# allWaves = vstack((allWaves, allWaves, allWaves))

msz0 = 30
msz1 = 30

sm = sompylib.sompy.SOM(allWaves, neighborhood=SOMPY.neighborhood.GaussianNeighborhood(), normalizer=SOMPY.normalization.VarianceNormalizator(), mapsize = [msz0, msz1], initialization='pca', name='sm')
sm.train(n_job = 1, shared_memory = 'yes')

h = sompylib.hitmap.HitMapView(10, 10, 'hitmap', text_size=8, show_text=True)
h.show(sm)



#Code for showing u-matrix
u = sompylib.umatrix.UMatrixView(50, 50, 'umatrix', show_axis=True, text_size=8, show_text=True)
#This is the Umat value
UMAT  = u.build_u_matrix(sm, distance=1, row_normalized=False)
#Here you have Umatrix plus its render
UMAT = u.show(sm, distance2=1, row_normalized=False, show_data=True, contooor=True, blob=False)


### Try to plot a report
# dataSpikes.samples
# dataSpikes.timestamps
dataSpikes.clusters = sm.cluster()[sm.project_data(allWaves)]

figure()
plot_cluster_waves(allWaves, dataSpikes.clusters)


cr = spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename='somcluster_shared_{}{}{}.png'.format(animalName, ephysFn,'Tetrode{}'.format(tetrode) ))



codebookVecs = sm.codebook.matrix

from sklearn.manifold import TSNE

import timeit
start_time = timeit.default_timer()

model = TSNE(n_components=2, method='barnes_hut', verbose=20, n_iter=1000)
Y = model.fit_transform(codebookVecs)

elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)
#########################################


figure()
clf()
plot(Y[:,0], Y[:,1], '.')


from sklearn.cluster import DBSCAN

start_time = timeit.default_timer()
db = DBSCAN(eps=1.8, min_samples=10).fit(Y)
elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)

labels = db.labels_
uniqueLabels = np.unique(labels)

colors = plt.cm.Paired(np.linspace(0, 1, len(uniqueLabels)))

#PLot the clusters in the embedded space
# figure()
# figure()
clf()
for indLabel, label in enumerate(unique(db.labels_)):
    hold(1)
    indsThisLabel = np.flatnonzero(db.labels_==label)
    plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel])

labels = db.labels_


dataClusters = labels[sm.project_data(allWaves)]


plot_cluster_waves(allWaves, dataClusters)


mapview = SOMPY.mapview.MapView(sm)

import hdbscan

clus = hdbscan.HDBSCAN(min_cluster_size=10)
cluster_labels = clus.fit_predict(Y)

figure()
for indLabel, label in enumerate(unique(cluster_labels)):
    hold(1)
    indsThisLabel = np.flatnonzero(cluster_labels==label)
    plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel])
