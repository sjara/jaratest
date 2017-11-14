import pandas
from jaratoolbox import celldatabase
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from jaratoolbox.colorpalette import TangoPalette
from jaratoolbox import extraplots
import os

STUDY_NAME = '2018thstr'

dbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, 'celldatabase.h5')
db = pandas.read_hdf(dbPath, 'dataframe')

def first_spike_latency_each_trial(spikeTimestamps, eventOnsetTimes, timeRange):
    (spikeTimesFromEventOnset,
     trialIndexForEachSpike,
     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                   eventOnsetTimes,
                                                                   timeRange)
    #This gives the indices of the trials that actually had spikes
    trialsWithSpikes = np.flatnonzero(indexLimitsEachTrial[1,:]-indexLimitsEachTrial[0,:])

    #Gives the index of the first spike for each of the trials with spikes
    firstSpikeIndEachTrial = indexLimitsEachTrial[0,trialsWithSpikes]

    firstSpikeTimeRelativeToTimeRange = spikeTimesFromEventOnset[firstSpikeIndEachTrial]
    latency = firstSpikeTimeRelativeToTimeRange - timeRange[0]
    return latency

medianLatencies = np.full(len(db), np.nan)

for indCell, cell in db.iterrows():
    if 'noiseburst' in cell['sessiontype']:
        spikeData, eventData = celldatabase.get_session_ephys(cell, 'noiseburst')
        if spikeData.timestamps is not None:
            eventOnsetTimes = eventData.get_event_onset_times(eventChannel=5)
            eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)

            preRange = [-0.1, 0]
            preLatency = first_spike_latency_each_trial(spikeData.timestamps, eventOnsetTimes, preRange)

            postRange = [0, 0.1]
            postLatency = first_spike_latency_each_trial(spikeData.timestamps, eventOnsetTimes, postRange)

            timeRange = [-0.2, 0.2]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        timeRange)

            #TODO: Use this for plotting examples
            # if PLOT==1:
            #     plt.clf()
            #     ax1 = plt.subplot(211)
            #     plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=4)
            #     ax1.add_patch(patches.Rectangle((preRange[0], 0),
            #                                     preRange[1]-preRange[0],
            #                                     trialIndexForEachSpike[-1]+1,
            #                                     color='0.5',
            #                                     alpha=0.5))
            #     ax1.add_patch(patches.Rectangle((postRange[0], 0),
            #                                     postRange[1]-postRange[0],
            #                                     trialIndexForEachSpike[-1]+1,
            #                                     color='r',
            #                                     alpha=0.5))

            #     plt.axvline(preRange[0]+np.median(preLatency), color='k')
            #     plt.axvline(postRange[0]+np.median(postLatency), color='r')
            #     ax1.set_xlim(timeRange)
            #     ax1.set_ylim([0, trialIndexForEachSpike[-1]])
            #     ax1.set_title('{}\nZ-score: {}'.format(cell['brainarea'],cell['noiseZscore']))

            #     # plt.axvline(preRange[0], color='0.5')
            #     # plt.axvline(postRange[0], color='r')

            #     plt.subplot(212)
            #     plt.hist(preLatency, histtype='step', color='0.5')
            #     plt.hold(1)
            #     plt.hist(postLatency, histtype='step', color='r')
            #     plt.xlim([0, 0.1])

            #     figName = '{}_{}_{}_TT{}c{}.png'.format(cell['subject'],
            #                                             cell['date'],
            #                                             int(cell['depth']),
            #                                             int(cell['tetrode']),
            #                                             int(cell['cluster']))
            #     saveDir = '/home/nick/data/reports/nick/20170607_spike_latency/'
            #     if cell['brainarea']=='rightThal':
            #         fullFn = os.path.join(saveDir, 'thal', figName)
            #     elif cell['brainarea']=='rightAC':
            #         fullFn = os.path.join(saveDir, 'ac', figName)
            #     elif cell['brainarea']=='rightAstr':
            #         fullFn = os.path.join(saveDir, 'astr', figName)
            #     else:
            #         raise
            #     plt.savefig(fullFn)

            medianLatencies[indCell]= np.median(postLatency)
        else:
            medianLatencies[indCell]= np.nan
    else:
        medianLatencies[indCell]= np.nan

db['medianFSLatency'] = medianLatencies

db.to_hdf(dbPath, key='dataframe')
