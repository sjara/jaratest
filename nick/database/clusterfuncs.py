from jaratoolbox.test.nick.database import dataloader
from jaratoolbox.test.nick.database import dataplotter
from jaratoolbox.test.nick.database import cellDB
from jaratoolbox import spikesorting
from matplotlib import pyplot as plt
import numpy as np


def plot_cluster_tuning(clusterObj, indTC, experimenter='nick', *args, **kwargs):
    loader = dataloader.DataLoader('offline', experimenter=experimenter)
    spikeData, eventData, behavData = loader.get_cluster_data(clusterObj, indTC)

    spikeTimestamps = spikeData.timestamps
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    freqEachTrial = behavData['currentFreq']
    intensityEachTrial = behavData['currentIntensity']

    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)

    xlabel='Frequency (kHz)'
    ylabel='Intensity (dB SPL)'

    freqLabels = ["%.1f" % freq for freq in possibleFreq/1000.0]
    intenLabels = ["%.1f" % inten for inten in possibleIntensity]

    # plt.clf()
    ax, cax, cbar = dataplotter.two_axis_heatmap(spikeTimestamps,
                                                 eventOnsetTimes,
                                                 firstSortArray=intensityEachTrial,
                                                 secondSortArray=freqEachTrial,
                                                 firstSortLabels=intenLabels,
                                                 secondSortLabels=freqLabels,
                                                 timeRange=[0, 0.1],
                                                 *args,
                                                 **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    return ax, cax, cbar
    # plt.show()
