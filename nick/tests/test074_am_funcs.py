from jaratest.nick.database import dataloader_v3 as dataloader
from jaratoolbox import spikesanalysis
from matplotlib import pyplot as plt
import numpy as np
import pandas
from scipy import stats
import random
import os
from sklearn import metrics

from jaratest.nick.database import dataplotter

def get_bin_edges(data):
    d = np.diff(np.unique(data)).min()
    left_of_first_bin = data.min() - float(d)/2
    right_of_last_bin = data.max() + float(d)/2
    bins = np.arange(left_of_first_bin, right_of_last_bin + d, d)
    return bins

masterdb = pandas.read_hdf('/home/nick/data/database/corticostriatal_master_20170452.h5', 'database')
goodcells = masterdb.query('isiViolations<0.02 and shapeQuality>2')
# cell = masterdb.ix[9] #Not too selective for rate
exampleCell = goodcells.iloc[15] #Selective for rate

# # To find an example cells

figDir = '/home/nick/data/database/amstats/'
# for indCell, cell in masterdb.iterrows():
for indCell, cell in enumerate([exampleCell]):
    spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
    eventOnsetTimes = eventData.get_event_onset_times()
    bdata = dataloader.get_session_bdata(cell, 'am')
    rateEachTrial = bdata['currentFreq'] #NOTE: bdata uses 'Freq' but this is AM so I'm calling it rate

    plt.clf()
    plt.subplot(121)
    dataplotter.plot_raster(spikeData.timestamps,
                            eventOnsetTimes,
                            sortArray=rateEachTrial,
                            timeRange=[-0.3, 0.8])
    plt.ylabel('AM rate (Hz)')
    plt.xlabel('Time from sound onset (sec)')
    plt.show()
    print indCell


    spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
    eventOnsetTimes = eventData.get_event_onset_times()
    bdata = dataloader.get_session_bdata(cell, 'am')

    rateEachTrial = bdata['currentFreq'] #NOTE: bdata uses 'Freq' but this is AM so I'm calling it rate
    possibleRate = np.unique(rateEachTrial)
    timeRange = [0, 0.5]
    respSpikeArrays = [] #List to hold the arrays of response bin spike counts (not all same number of trials)
    respSpikeInds = [] #This will hold arrays with the inds for which rate the response spikes came from
    for indRate, thisRate in enumerate(possibleRate):
        trialsThisRate = np.flatnonzero(rateEachTrial==thisRate)
        (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes[trialsThisRate],
                                                                        timeRange)
        # plt.clf()
        # plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.')
        # plt.show()
        # plt.waitforbuttonpress()
        nspkResp = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            timeRange)
        respSpikeArrays.append(nspkResp.ravel())
        respSpikeInds.append(np.ones(len(nspkResp))*indRate)

    #K-W test (nonparametric anova) to see if response to any rate significantly differs
    try:
        statistic, pval = stats.kruskal(*respSpikeArrays)
    except ValueError:
        pval=None

    #Plotting number of spikes against rate
    #Flatten spikes and inds to be ablet to plot them easily
    flatSpikes = []
    flatInds = []
    for arr in respSpikeArrays:
        for t in arr:
            flatSpikes.append(t)
    for arr in respSpikeInds:
        for t in arr:
            flatInds.append(t)

    plt.subplot(122)
    jitterVals = np.array([random.uniform(-0.2, 0.2) for _ in flatInds])
    jitterVals2 = np.array([random.uniform(-0.05, 0.05) for _ in flatInds])
    plt.plot(flatInds+jitterVals, flatSpikes+jitterVals2, 'ko', alpha=0.2)
    plt.xlim([-0.5, 10.5])
    plt.ylim([-0.5, max(flatSpikes)+0.5])
    plt.ylabel('Number of spikes per trial in range [0, 0.5]')
    plt.xlabel('Rate')
    ax = plt.gca()
    rateLabels = ['{:.01f}'.format(rate) for rate in possibleRate]
    ax.set_xticklabels(rateLabels)
    plt.title('P-val of KW test: {}'.format(pval))
    fig = plt.gcf()
    fig.set_size_inches((11, 6))
    figName = 'cell{}.png'.format(indCell)
    figFullPath = os.path.join(figDir, figName)
    # plt.savefig(figFullPath)

    #Calculate mutual information
    spikesPerTrial = np.concatenate(respSpikeArrays)
    freqIndPerTrial = np.concatenate(respSpikeInds)

    xbins = get_bin_edges(freqIndPerTrial)
    ybins = get_bin_edges(spikesPerTrial)

    # c_xy = np.histogram2d(freqIndPerTrial, spikesPerTrial, [xbins, ybins])[0]
    c_xy = np.histogram2d(freqIndPerTrial, spikesPerTrial)[0]
    mi = metrics.mutual_info_score(None, None, contingency=c_xy)

### testing numpy 2dhist
a = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
b = np.array([1, 1, 2, 0, 1, 2, 3, 3, 3])
aedges = np.array([-0.5, 0.5, 1.5, 2.5])
bedges = np.array([-0.5, 0.5, 1.5, 2.5, 3.5])
c, xe, ye = np.histogram2d(b, a, [bedges, aedges])
imshow(np.flipud(c), interpolation='none')
