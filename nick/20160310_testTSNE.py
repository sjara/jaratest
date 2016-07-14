


fetFilename='/home/nick/data/ephys/pinp009/multisession_2016-01-27_site1_cortex/Tetrode6.fet.1'
fetFile = open(fetFilename, 'r')

numFetclusters = fetFile.readline()
fetList = fetFile.read().split('\n')

for indF,fet in enumerate(fetList):
    fetList[indF] = fet.split()

fetList = np.asarray(fetList[:-1])

fetSmall = fetList[0:5000, :]
plot(fetSmall[:,0], fetSmall[:,1], '.')

#No t-sne??
from sklearn.manifold import TSNE

model = TSNE(n_components=2, method='barnes_hut', verbose=20, n_iter=1000)

Y = model.fit_transform(fetSmall)

clf()
plot(Y[:,0], Y[:,1], '.')

from sklearn.cluster import DBSCAN

db = DBSCAN(eps=0.3, min_samples=10).fit(Y)

#PLot the clusters in the embedded space
clf()
for label in unique(db.labels_):
    indsThisLabel = np.flatnonzero(db.labels_==label)
    plot(Y[indsThisLabel, 0], Y[indsThisLabel, 1], '.')

#PLot the clusters in feature-space
clf()
for label in unique(db.labels_):
    indsThisLabel = np.flatnonzero(db.labels_==label)
    plot(fetSmall[indsThisLabel, 1], fetSmall[indsThisLabel, 4], '.')


#I wish i could plot the waveforms


