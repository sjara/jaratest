
'''
Plot the average firing rate in response to each frequency presented.
'''

from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0
timeRange=[-0.5, 1] #In seconds

ephysRoot = '/home/nick/data/ephys/hm4d002/cno_08-12'
#ephysSession=sort(os.listdir(ephysRoot))[-1]
#ephysSession = '2014-08-12_14-00-18'
ephysSessions=sort(os.listdir(ephysRoot))

behaviorDir='/home/nick/data/behavior/nick/hm4d002/'
#ephysDir = os.path.join(ephysRoot, ephysSession)
#event_filename=os.path.join(ephysDir, 'all_channels.events')

numTetrodes = 4


#behavDataFileName=os.path.join(behaviorDir, 'hm4d002_tuning_curve_20140812_exp01.h5')
for ind, ephysDir in enumerate(ephysSessions):
    event_filename=os.path.join(ephysRoot, ephysDir, 'all_channels.events')

    behavDataFileName=os.path.join(behaviorDir, 'hm4d002_tuning_curve_20140812_exp0{0}.h5'.format(ind+1))

    bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
    freqEachTrial = bdata['currentFreq']
    possibleFreq = np.unique(freqEachTrial)

    # -- The old way of sorting (useful for plotting sorted raster) --
    sortedTrials = []
    for indf,oneFreq in enumerate(possibleFreq):
        indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
        sortedTrials = np.concatenate((sortedTrials,indsThisFreq))
    sortingInds = argsort(sortedTrials)

    # -- Load event data and convert event timestamps to ms --
    ev=loadopenephys.Events(event_filename)
    eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
    evID=np.array(ev.eventID)
    eventOnsetTimes=eventTimes[evID==1]

    eventOnsetTimes=eventOnsetTimes[:-1] #FIXME: Horrible fix

    tetrodeID = 3
    spike_filename=os.path.join(ephysRoot, ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID))
    sp=loadopenephys.DataSpikes(spike_filename)
    spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]


    # -- Calculate tuning --
    responseRange = [0.010,0.020]
    nSpikes = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange)
    meanSpikesEachFrequency = np.empty(len(possibleFreq))

    # -- This part will be replace by something like behavioranalysis.find_trials_each_type --
    trialsEachFreq = []
    for indf,oneFreq in enumerate(possibleFreq):
        trialsEachFreq.append(np.flatnonzero(freqEachTrial==oneFreq))

    # -- Calculate average firing for each freq --
    for indf,oneFreq in enumerate(possibleFreq):
        try:
            meanSpikesEachFrequency[indf] = np.mean(nSpikes[trialsEachFreq[indf]])

        except IndexError:
            print 'Fucked up on {0}, freq {1}'.format(ephysDir, oneFreq)
            pass


    #clf()
    ax2 = plt.subplot2grid((len(ephysSessions),4), (ind, 0), colspan=3)
    plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')
    title(ephysDir+' TT{0}'.format(tetrodeID))
    #xlabel('Time (sec)')
    #ylabel('Sorted trials')

    ax2 = plt.subplot2grid((len(ephysSessions),4), (ind, 3), colspan=1)
    ax2.set_xscale('log')
    plot(possibleFreq,meanSpikesEachFrequency,'o-')
    #ylabel('Avg spikes in window {0}-{1} sec'.format(*responseRange))
xlabel('Frequency')
draw()
show()



