import SOMPY
from sklearn.manifold import TSNE

#Data should be preprocessed to convert to microvolts
# GAIN = 5000.0
# SAMPLING_RATE=30000.0
# dataSpikes.samples = ((dataSpikes.samples - 32768.0) / GAIN) * 1000.0
# dataSpikes.timestamps = dataSpikes.timestamps/SAMPLING_RATE


def sortTSNE(dataSpikes):
    (numSpikes, numChans, numSamples) = shape(dataSpikes.samples)
    allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)

    model = TSNE(n_components=2, method='barnes_hut', verbose=20, n_iter=1000)
    Y = model.fit_transform(allWaves)



def sortSOM(dataSpikes):

    (numSpikes, numChans, numSamples) = shape(tetrodeToCluster.samples)
    allWaves = dataSpikes.samples.reshape(numSpikes, numChans*numSamples)


    msz0 = 30
    msz1 = 30

    sm = SOMPY.sompy.SOM(allWaves, neighborhood=SOMPY.neighborhood.GaussianNeighborhood(), normalizer=SOMPY.normalization.VarianceNormalizator(), mapsize = [msz0, msz1], initialization='pca', name='sm')
    sm.train(n_job = 1, shared_memory = 'yes')

    #Project the waves back onto the SOM (find the bmu for each) and get the clusters
    clusters = sm.cluster()[sm.project_data(allWaves)]

    return clusters

 
