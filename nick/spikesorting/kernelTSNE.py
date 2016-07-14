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


class KernelTSNEClassifier(object):

    def __init__(self, X, trainingSetSize=5000):
        self.data = X

        dataToUse = np.random.randint(len(X), size=trainingSetSize)
        self.trainingSet = self.data[dataToUse, :]

        self.euc = sklearn.neighbors.DistanceMetric.get_metric('euclidean')

    def train(self, sigma_scale=0.1, n_clusters=12):

        print("Calculating Pairwise Distances")

        X_dist = self.euc.pairwise(self.trainingSet)

        print("Embedding training set")
        model = sklearn.manifold.TSNE(n_components=2, verbose=10, n_iter=1000, metric='precomputed')
        self.Y_train = model.fit_transform(X_dist)

        print("Calculating Kernel")

        self.A, self.sig_nb = self.kmap_train(X_dist, self.Y_train, sigma_scale)

        print("Fitting GMM")
        self.fit_gmm(n_clusters)

    def plot_training_set_embedding(self):
        plt.clf()
        plt.plot(self.Y_train[:,0], self.Y_train[:,1], '.')

    def plot_test_embedding(self):
        pass


    def predict_full_dataset(self, chunk=5000):

        print("Calculating distance between new data and training data")
        numDataPts = len(self.data)
        self.clusterLabels = np.zeros((numDataPts))
        self.Y_ose = np.zeros((numDataPts, 2))

        for indItem in range(numDataPts):

            oneItem = self.data[indItem, :][np.newaxis, :]

            X_dist_ose = self.euc.pairwise(oneItem, self.trainingSet)
            Y_ose = self.kmap_test(X_dist_ose, self.A, self.sig_nb)
            clusterLabel = self.predict_cluster(Y_ose)

            self.clusterLabels[indItem] = clusterLabel
            self.Y_ose[indItem, :] = Y_ose

            sys.stdout.write('\r')
            progress = (indItem/np.double(numDataPts))
            sys.stdout.write("[%-20s] %d%%" % ('='*np.floor(progress*20), np.floor(progress*100)))
            sys.stdout.flush()

    # def predict(self, newData):

    #     X_dist_ose = self.euc.pairwise(newData, self.trainingSet)
    #     Y_ose = self.kmap_test(X_dist_ose, self.A, self.sig_nb)
    #     clusterLabels = self.predict_cluster(Y_ose)
    #     return clusterLabels

    def fit_gmm(self, n_clusters):
        self.mixture = sklearn.mixture.GMM(n_components=n_clusters)
        self.mixture.fit(self.Y_train)
        self.training_labels = self.mixture.predict(self.Y_train)

    def predict_cluster(self, Y_new):
        clusterLabels = self.mixture.predict(Y_new)
        return clusterLabels

    def kmap_train(self, X_dist, Y, sigma_scale):
        #Ported from KMap Toolbox by Barbara Hammer's group

        k_nb = 10 # Number of neighbors to use
        f_local =1 # 0 for global, 1 for local

        # sig_nb=determine_sigma(X_dist, k_nb, f_local);
        sig_nb = self.determine_sigma_from_X(self.trainingSet, k_nb, sigma_scale)
        sig_nb = sig_nb**2
        sig_nb = sig_nb * sigma_scale #Scale the sigma values

        #Compute the kernel
        kernel = np.exp(-1*(X_dist/sig_nb))

        #Divide each row by the row sum (use newaxis trick to get broadcasting to behave)
        kernel = kernel / np.sum(kernel, 1)[:,np.newaxis]

        A = np.dot(np.linalg.pinv(kernel), Y)

        return A, sig_nb

    @staticmethod
    def kmap_test(X_dist_ose, A, sig_nb):
        kernel_ose = np.exp(-1*(X_dist_ose/sig_nb))

        #Divide each row by the row sum (use newaxis trick to get broadcasting to behave)
        kernel_ose = kernel_ose / np.sum(kernel_ose, 1)[:,np.newaxis]

        Y_ose = np.dot(kernel_ose, A)

        return Y_ose

    @staticmethod
    def determine_sigma_from_X(X, k_nb, local=True):
        #Adapted from KMap Toolbox by Barbara Hammer's group
        #Just needs the raw vectors, not a distance matrix

        k = k_nb + 1 ##### We add 1 to the number of the neighbor to return because the first will always be zero (dist to self)

        nbrs = sklearn.neighbors.NearestNeighbors(n_neighbors=k, algorithm='auto').fit(X)
        distances, indices = nbrs.kneighbors(X)

        if local:
            return distances[:,-1] #Return distances to last (kth)
        else:
            return mean(distances[:,-1]) #Return average distance to the kth neighbor

if __name__=='__main__':
    animalName='pinp013'
    ephysLoc = '/home/nick/data/ephys/'
    ephysPath = os.path.join(ephysLoc, animalName)
    ephysFn='2016-05-27_14-13-26'
    tetrode=3
    spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode{}.spikes'.format(tetrode))
    dataSpikes = loadopenephys.DataSpikes(spikesFn)

    (numSpikes, numChans, numSamples) = shape(dataSpikes.samples)
    allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

    kernClass = KernelTSNEClassifier(allWaves, trainingSetSize=1000)

    import timeit
    start_time = timeit.default_timer()

    kernClass.train()

    kernClass.predict_full_dataset()

    elapsed = timeit.default_timer() - start_time
    print 'ELAPSED TIME: {} mins'.format(elapsed/60)


    from sklearn.datasets import load_iris

    data = load_iris()

    kernClass = KernelTSNEClassifier(data.data, trainingSetSize=50)
    kernClass.train()
    kernClass.predict_full_dataset()


    X_dist = kernClass.euc.pairwise(data.data)

    model =  sklearn.manifold.TSNE(n_components=2, verbose=10, n_iter=1000, metric='precomputed')

    Y = model.fit_transform(X_dist)

    plot(Y[:,0], Y[:,1], '.')


    GAIN = 5000.0
    SAMPLING_RATE=30000.0
    dataSpikes.samples = ((dataSpikes.samples - 32768.0) / GAIN) * 1000.0
    dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE

    from jaratoolbox import spikesorting

    spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename = 'testKTSNEcluster.png')


    # for i in range(21):
    #     sys.stdout.write('\r')
    #     # the exact output you're looking for:
    #     sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    #     sys.stdout.flush()
    #     sleep(0.25)


    # progress = (9/100.)
    # sys.stdout.write("[%-20s] %d%%" % ('='*np.floor(progress*20), np.floor(progress*100)))



    animalname='adap020'
    ephysloc = '/home/nick/data/ephys/'
    ephyspath = os.path.join(ephysloc, animalname)
    ephysfn='2016-05-25_16-33-09'
    tetrode=2
    spikesFn = os.path.join(ephysPath, ephysFn, 'Tetrode{}.spikes'.format(tetrode))
    dataSpikes = loadopenephys.DataSpikes(spikesFn)

    (numSpikes, numChans, numSamples) = shape(dataSpikes.samples)
    allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

    import timeit
    start_time = timeit.default_timer()
    kernClass = KernelTSNEClassifier(allWaves, trainingSetSize=5000)

    kernClass.train()

    kernClass.predict_full_dataset()
    elapsed = timeit.default_timer() - start_time
    print 'ELAPSED TIME: {} mins'.format(elapsed/60)

    GAIN = 5000.0
    SAMPLING_RATE=30000.0
    dataSpikes.samples = ((dataSpikes.samples - 32768.0) / GAIN) * 1000.0
    dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE
    dataSpikes.clusters = kernClass.clusterLabels

    spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename = 'testKTSNEclusterHUGEset5000.png')


    figure()
    clf()
    plot(kernClass.Y_ose[:,0], kernClass.Y_ose[:,1], '.', alpha=0.01)
    xlim([-15, 15])
    ylim([-15, 15])

    # largegmm = sklearn.mixture.GMM(n_components=12)
    # clusters = largegmm.fit_predict(kernClass.Y_ose)

    trainLabels = kernClass.mixture.predict(kernClass.Y_train)


    figure()
    plot(kernClass.Y_train[:,0], kernClass.Y_train[:,1], '.')

    Y = kernClass.Y_train
    cluster_labels = trainLabels
    figure(figsize=(10, 10))
    uniqueLabels = np.unique(cluster_labels)
    colors = plt.cm.Paired(np.linspace(0, 1, len(uniqueLabels)))
    for indLabel, label in enumerate(unique(cluster_labels)):
        hold(1)
        indsThisLabel = np.flatnonzero(cluster_labels==label)
        plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel])



    testLabels = kernClass.mixture.predict(kernClass.Y_ose)

    Y = kernClass.Y_ose
    cluster_labels = testLabels
    figure(figsize=(10, 10))
    uniqueLabels = np.unique(cluster_labels)
    colors = plt.cm.Paired(np.linspace(0, 1, len(uniqueLabels)))
    for indLabel, label in enumerate(unique(cluster_labels)):
        hold(1)
        indsThisLabel = np.flatnonzero(cluster_labels==label)
        plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel], alpha=0.01)
    xlim([-15, 15])
    ylim([-15, 15])

    figure(figsize=(10, 20))
    labels = cluster_labels
    uniqueLabels = np.unique(cluster_labels)
    rav = allWaves.ravel()
    maxv = percentile(rav, 99.95)
    minv = percentile(rav, 0.05)
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


    #Test using PCA on the input data

    pcWaves = sklearn.decomposition.PCA(n_components = 50).fit_transform(allWaves)

    start_time = timeit.default_timer()
    kernClass = KernelTSNEClassifier(pcWaves, trainingSetSize=1000)

    kernClass.train()

    kernClass.predict_full_dataset()
    elapsed = timeit.default_timer() - start_time

    print 'ELAPSED TIME: {} mins'.format(elapsed/60)

    Y = kernClass.Y_ose
    cluster_labels = kernClass.clusterLabels
    figure(figsize=(10, 10))
    uniqueLabels = np.unique(cluster_labels)
    colors = plt.cm.Paired(np.linspace(0, 1, len(uniqueLabels)))
    for indLabel, label in enumerate(unique(cluster_labels)):
        hold(1)
        indsThisLabel = np.flatnonzero(cluster_labels==label)
        plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.', color=colors[indLabel], alpha=0.01)
    # xlim([-15, 15])
    # ylim([-15, 15])

    spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename = 'testKTSNEclusterHUGEset1000PCA.png')




    #Test just using PCA and a GMM
    spikesToUse = np.random.randint(len(pcWaves), size=1000)
    pcWavesToUse = pcWaves[spikesToUse, :]

    pcGMM = sklearn.mixture.GMM(n_components=12)
    pcGMM.fit(pcWavesToUse)
    labels = pcGMM.predict(pcWaves)

    dataSpikes.clusters = labels
    spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename = 'test50PC_GMM.png')





    start_time = timeit.default_timer()
    pcWaves = sklearn.decomposition.PCA(n_components = 50).fit_transform(allWaves)
    spikesToUse = np.random.randint(len(pcWaves), size=10000)
    pcWavesToUse = pcWaves[spikesToUse, :]

    pcGMM = sklearn.mixture.GMM(n_components=12)
    pcGMM.fit(pcWavesToUse)
    labels = pcGMM.predict(pcWaves)

    dataSpikes.clusters = labels

    elapsed = timeit.default_timer() - start_time
    print 'ELAPSED TIME: {} mins'.format(elapsed/60)

    spikesorting.ClusterReportFromData(dataSpikes, outputDir='/home/nick/Desktop', filename = 'test50PC_GMM.png')


