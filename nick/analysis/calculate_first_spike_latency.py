import pandas
from jaratest.nick.database import dataloader_v3 as dataloader
from jaratoolbox import spikesanalysis
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from jaratoolbox.colorpalette import TangoPalette
from jaratoolbox import extraplots
import os
import ipdb

dbFn = '/home/nick/data/database/corticostriatal_master_2017-06-01_13-00-07.h5'
db = pandas.read_hdf(dbFn, 'database')

dbStrFn = '/home/nick/data/database/corticostriatal_striatumcells_2017-05-30_13-27-08.h5'
dbStr = pandas.read_hdf(dbStrFn, 'database')

db = db.append(dbStr, ignore_index=True)

soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05')

PLOT=1

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

for indCell, cell in soundResponsive.iterrows():
    spikeData, eventData = dataloader.get_session_ephys(cell, 'noiseburst')
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


    if PLOT==1:
        plt.clf()
        ax1 = plt.subplot(211)
        plt.plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'k.', ms=4)
        ax1.add_patch(patches.Rectangle((preRange[0], 0),
                                        preRange[1]-preRange[0],
                                        trialIndexForEachSpike[-1]+1,
                                        color='0.5',
                                        alpha=0.5))
        ax1.add_patch(patches.Rectangle((postRange[0], 0),
                                        postRange[1]-postRange[0],
                                        trialIndexForEachSpike[-1]+1,
                                        color='r',
                                        alpha=0.5))

        plt.axvline(preRange[0]+np.median(preLatency), color='k')
        plt.axvline(postRange[0]+np.median(postLatency), color='r')
        ax1.set_xlim(timeRange)
        ax1.set_ylim([0, trialIndexForEachSpike[-1]])
        ax1.set_title('{}\nZ-score: {}'.format(cell['brainarea'],cell['noiseZscore']))

        # plt.axvline(preRange[0], color='0.5')
        # plt.axvline(postRange[0], color='r')

        plt.subplot(212)
        plt.hist(preLatency, histtype='step', color='0.5')
        plt.hold(1)
        plt.hist(postLatency, histtype='step', color='r')
        plt.xlim([0, 0.1])

        figName = '{}_{}_{}_TT{}c{}.png'.format(cell['subject'],
                                                cell['date'],
                                                int(cell['depth']),
                                                int(cell['tetrode']),
                                                int(cell['cluster']))
        saveDir = '/home/nick/data/reports/nick/20170607_spike_latency/'
        if cell['brainarea']=='rightThal':
            fullFn = os.path.join(saveDir, 'thal', figName)
        elif cell['brainarea']=='rightAC':
            fullFn = os.path.join(saveDir, 'ac', figName)
        elif cell['brainarea']=='rightAstr':
            fullFn = os.path.join(saveDir, 'astr', figName)
        else:
            raise
        plt.savefig(fullFn)

    medianLatencies[indCell]= np.median(postLatency)

db['medianFSLatency'] = medianLatencies

#For the hists, take only the cells that were excited by sound
soundResponsive = db.query('isiViolations<0.02 and shapeQuality>2 and noisePval<0.05 and noiseZscore>0')

thal = soundResponsive.groupby('brainarea').get_group('rightThal')
ac = soundResponsive.groupby('brainarea').get_group('rightAC')
astr = soundResponsive.groupby('brainarea').get_group('rightAstr')

tlat = thal['medianFSLatency'][pandas.notnull(thal['medianFSLatency'])]
aclat = ac['medianFSLatency'][pandas.notnull(ac['medianFSLatency'])]
astrlat = astr['medianFSLatency'][pandas.notnull(astr['medianFSLatency'])]

plt.clf()

# plt.hist(tlat, histtype='step', color='g', normed=1)
# plt.hold(1)
# plt.hist(aclat, histtype='step', color='r', normed=1)
# plt.hist(astrlat, histtype='step', color='b', normed=1)
bins=10
thalcolor = TangoPalette['Chameleon3']
accolor = TangoPalette['ScarletRed2']
astrcolor = TangoPalette['SkyBlue2']
fontsize=15

ax = plt.subplot(311)
plt.hist(tlat, histtype='stepfilled', bins=bins, color=thalcolor, weights=np.zeros_like(tlat) + 1. / tlat.size, lw=2)
ax.set_ylim([0, 0.25])
plt.xlim([0, 0.1])
ax.set_xticklabels([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([0, 25])
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, fontsize)

ax = plt.subplot(312)
plt.hist(aclat, histtype='stepfilled', bins=bins, color=accolor, weights=np.zeros_like(aclat) + 1. / aclat.size, lw=2)
ax.set_ylim([0, 0.25])
plt.xlim([0, 0.1])
ax.set_xticklabels([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([0, 25])
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, fontsize)

ax = plt.subplot(313)
plt.hist(astrlat, histtype='stepfilled', bins=bins, color=astrcolor, weights=np.zeros_like(astrlat) + 1. / astrlat.size, lw=2)
ax.set_ylim([0, 0.25])
plt.xlim([0, 0.1])
ax.set_xticklabels([0, 20, 40, 60, 80, 100])
ax.set_yticks([0, 0.25])
ax.set_yticklabels([0, 25])
extraplots.boxoff(ax)
extraplots.set_ticks_fontsize(ax, fontsize)

plt.show()
