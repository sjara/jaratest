import numpy as np
import sklearn.decomposition
import sklearn.mixture
import timeit

class PCASpikeSorter(object):

    def __init__(self, data, nComponents=50, nClusters=12, trainingSamples=10000):

        timer = timeit.default_timer()

        pca = sklearn.decomposition.RandomizedPCA(n_components=nComponents)
        print("Calculating randomized PCA with {} components".format(nComponents))
        self.PCA = pca.fit_transform(data)

        print('Selecting subset with {} samples'.format(trainingSamples))
        spikesToUse = np.random.randint(len(self.PCA), size=trainingSamples)
        self.trainingData = self.PCA[spikesToUse, :]

        print('Fitting gaussian mixture model with {} clusters'.format(nClusters))
        self.GMM = sklearn.mixture.GMM(n_components=nClusters)
        self.GMM.fit(self.trainingData)

        print('Predicting cluster for each sample in full dataset')
        self.clusters = self.GMM.predict(self.PCA)

        elapsed = timeit.default_timer() - timer

        print('Total time elapsed: {} mins'.format(elapsed/60.0))
