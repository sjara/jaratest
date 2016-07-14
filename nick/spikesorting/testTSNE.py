from jaratoolbox import loadopenephys
from jaratoolbox import spikesorting
from jaratoolbox.test.nick import clustercutting
from matplotlib import pyplot as plt
import os

# animalName='pinp013'
# animalName='pinp005'
# ephysLoc = '/home/nick/data/ephys/'
# ephysPath = os.path.join(ephysLoc, animalName)

# #Data with really only 1 neuron
# ephysFn='2016-05-27_14-08-54'
# # ephysFn='2016-05-27_14-13-26'
# # ephysFn='2015-08-05_23-36-02'
# tetrode=4
# spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode2.spikes')
# spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode{}.spikes'.format(tetrode))

# #Data with more than one neuron
# ephysFn='2016-05-25_16-02-29'
# spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode8.spikes')

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

from sklearn.manifold import TSNE


#############Timing code #################
import timeit
start_time = timeit.default_timer()

model = TSNE(n_components=2, method='barnes_hut', verbose=20, n_iter=1000)
Y = model.fit_transform(allWaves)

elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)
#########################################


figure()
clf()
plot(Y[:,0], Y[:,1], '.')


#We can cluster the embedded points manually if we want
# cw = clustercutting.ClusterCutter(Y)

# clusterWaves = allWaves[cw.inCluster]
# # clusterWaves = dataSpikes.samples[cw.inCluster, :, :]

# figure()
# for wave in clusterWaves:
#     plot(wave, 'k-', alpha=0.5)
#     hold(1)
# show()



### Use DBSCAN to cluster the embedded points
from sklearn.cluster import DBSCAN

start_time = timeit.default_timer()
db = DBSCAN(eps=0.37, min_samples=10).fit(Y)
elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)

labels = db.labels_
uniqueLabels = np.unique(labels)

colors = plt.cm.Paired(np.linspace(0, 1, len(uniqueLabels)))

#PLot the clusters in the embedded space
# figure()
figure()
clf()
for indLabel, label in enumerate(unique(db.labels_)):
    hold(1)
    indsThisLabel = np.flatnonzero(db.labels_==label)
    plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel])


def find_eps(Y, lower, upper, npoints=50):
    epsRange = linspace(lower, upper, npoints)
    numClusters = np.zeros(len(epsRange))
    for indEps, eps in enumerate(epsRange):
        db = DBSCAN(eps=eps, min_samples=10).fit(Y)
        numClusters[indEps] = len(unique(db.labels_))
    figure()
    plot(epsRange, numClusters)

find_eps(Y, 0.3, 0.4)




## Plot the waveforms for all the identified clusters
figure()
clf()
rav = allWaves.ravel()
# maxv = max(allWaves.ravel())
maxv = percentile(rav, 99.95)
minv = percentile(rav, 0.05)
# minv = min(allWaves.ravel())
for indLabel, label in enumerate(uniqueLabels):
    subplot(len(uniqueLabels), 1, indLabel+1)
    clusterWaves = allWaves[labels==label]

    spikesToPlot = np.random.randint(len(clusterWaves),size=50)

    for wave in clusterWaves[spikesToPlot]:
        plot(wave, '-', alpha=0.5, color=colors[indLabel])
        hold(1)
    plot(clusterWaves.mean(0), 'k', lw=2, zorder=10)
    ylim([minv, maxv])
    axvline(x=40, lw=3, color='k')
    axvline(x=80, lw=3, color='k')
    axvline(x=120, lw=3, color='k')







################### Try to plot report #################

################################################
#####Hack to make sure there are only 12 clusters (For the report)
labels[labels>11]=-1
################################################

dataSpikes.samples = dataSpikes.samples[labels>=0]
dataSpikes.timestamps = dataSpikes.timestamps[labels>=0]
dataSpikes.clusters = labels[labels>=0]


cr = spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename='{}{}{}.png'.format(animalName, ephysFn,'Tetrode{}'.format(tetrode) ))






import hdbscan

clus = hdbscan.HDBSCAN(min_cluster_size=10)
# start_time = timeit.default_timer()
cluster_labels = clus.fit_predict(Y)
# elapsed = timeit.default_timer() - start_time

figure()
uniqueLabels = np.unique(cluster_labels)
colors = plt.cm.Paired(np.linspace(0, 1, len(uniqueLabels)))
for indLabel, label in enumerate(unique(cluster_labels)):
    hold(1)
    indsThisLabel = np.flatnonzero(cluster_labels==label)
    plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel])

labels = cluster_labels

figure()
clf()
rav = allWaves.ravel()
# maxv = max(allWaves.ravel())
maxv = percentile(rav, 99.95)
minv = percentile(rav, 0.05)
# minv = min(allWaves.ravel())
for indLabel, label in enumerate(uniqueLabels):
    subplot(len(uniqueLabels), 1, indLabel+1)
    clusterWaves = allWaves[labels==label]

    spikesToPlot = np.random.randint(len(clusterWaves),size=50)

    for wave in clusterWaves[spikesToPlot]:
        plot(wave, '-', alpha=0.5, color=colors[indLabel])
        hold(1)
    plot(clusterWaves.mean(0), 'k', lw=2, zorder=10)
    ylim([minv, maxv])
    axvline(x=40, lw=3, color='k')
    axvline(x=80, lw=3, color='k')
    axvline(x=120, lw=3, color='k')



#### Test with a bigger dataset


allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

newAllWaves = vstack((allWaves, allWaves, allWaves))

from sklearn.manifold import TSNE


#############Timing code #################
import timeit
start_time = timeit.default_timer()

model = TSNE(n_components=2, method='barnes_hut', verbose=20, n_iter=1000)
Y = model.fit_transform(newAllWaves)

elapsed = timeit.default_timer() - start_time
print 'ELAPSED TIME: {} mins'.format(elapsed/60)
#########################################


figure()
clf()
plot(Y[:,0], Y[:,1], '.')


##We need to test the memory and computation time taken by t-SNE. I will run a small simulation.

numSpikes = np.linspace()
