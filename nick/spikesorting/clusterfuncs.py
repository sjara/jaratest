from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
import numpy as np

def cluster_dbscan(Y, eps, min_samples=10, *args, **kwargs):
    db = DBSCAN(eps=eps, min_samples=min_samples, *args, **kwargs).fit(Y)
    labels = db.labels_
    return labels

def find_eps(Y, lower, upper, npoints=50):
    '''
    Run DBSCAN clustering with a range of neighborhood sizes and plot the number
    of clusters resulting from each neighborhood. Can be used to help determine
    the optimal neighborhood size.
    '''

    epsRange = linspace(lower, upper, npoints)
    numClusters = np.zeros(len(epsRange))
    for indEps, eps in enumerate(epsRange):
        db = DBSCAN(eps=eps, min_samples=10).fit(Y)
        numClusters[indEps] = len(unique(db.labels_))
    figure()
    plot(epsRange, numClusters)

def cluster_colors(numColors):
    colors = plt.cm.Paired(np.linspace(0, 1, numColors))
    return colors

def plot_cluster_points(Y, labels, colors=None, dim=[0, 1]):
    uniqueLabels = np.unique(labels)

    if not colors:
        colors = cluster_colors(len(uniqueLabels))

    clf()
    for indLabel, label in enumerate(uniqueLabels):
        plt.hold(1)
        indsThisLabel = np.flatnonzero(labels==label)
        plt.plot(Y[indsThisLabel, dim[0]], Y[indsThisLabel, dim[1]], '.', color=colors[indLabel])


def plot_cluster_waves(allWaves, labels, colors=None, nSpikesToPlot=50):

    '''
    Plot some waves from each cluster (Unconstrained number of clusters, unlike the cluster report)

    Args:

    allWaves (array): Array of shape (nSpikes * 160) e.g. all the samples raveled across the 4 channels
    '''

    #Use percentile to determine ylims
    rav = allWaves.ravel()
    maxv = np.percentile(rav, 99.95)
    minv = np.percentile(rav, 0.05)

    uniqueLabels = np.unique(labels)

    if not colors:
        colors=cluster_colors(len(uniqueLabels))

    clf()
    for indLabel, label in enumerate(uniqueLabels):
        plt.subplot(len(uniqueLabels), 1, indLabel+1)
        clusterWaves = allWaves[labels==label]
        spikesToPlot = np.random.randint(len(clusterWaves),size=nSpikesToPlot)

        for wave in clusterWaves[spikesToPlot]:
            plt.plot(wave, '-', alpha=0.5, color=colors[indLabel])
            plt.hold(1)

        plt.plot(clusterWaves.mean(0), 'k', lw=2, zorder=10)
        plt.ylim([minv, maxv])
        plt.axvline(x=40, lw=3, color='k')
        plt.axvline(x=80, lw=3, color='k')
        plt.axvline(x=120, lw=3, color='k')
