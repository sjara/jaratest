

#!/usr/bin/env python
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0
timeRange=[-0.5, 1] #In seconds

#########################
#ephysDir='/home/jarauser/data/ephys/hm4d002/2014-08-04_17-11-30'
ephysRoot= '/home/nick/data/ephys/hm4d002/cno_08-12'
ephysSessions=sort(os.listdir(ephysRoot))


tetrodeNum= 'Tetrode3.spikes'


#numTetrodes = 4
#########################

for ind, ephysDir in enumerate(ephysSessions):
    event_filename=os.path.join(ephysRoot, ephysDir, 'all_channels.events')

    behaviorDir='/home/nick/data/behavior/nick/hm4d002/'
    behavDataFileName=os.path.join(behaviorDir, 'hm4d002_tuning_curve_20140812_exp0{0}.h5'.format(ind+1))

    bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')

    freqEachTrial = bdata['currentFreq']

    # -- Workaround for bug (as of 2014-07-08) --
    #freqEachTrial = freqEachTrial[1:]
    #freqEachTrial = np.roll(freqEachTrial,-1)

    possibleFreq = np.unique(freqEachTrial)

    sortedTrials = []
    for indf,oneFreq in enumerate(possibleFreq):
        indsThisFreq = np.flatnonzero(freqEachTrial==oneFreq)
        sortedTrials = np.concatenate((sortedTrials,indsThisFreq))
    sortingInds = argsort(sortedTrials)


    #Load event data and convert event timestamps to ms
    ev=loadopenephys.Events(event_filename)
    eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
    evID=np.array(ev.eventID)
    eventOnsetTimes=eventTimes[evID==1]

    eventOnsetTimes=eventOnsetTimes[:-1] #FIXME: Horrible fix

    spike_filename=os.path.join(ephysRoot, ephysDir, tetrodeNum)
    sp=loadopenephys.DataSpikes(spike_filename)
    spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

    sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]

    subplot(len(ephysSessions),1,ind+1)

    #plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')

    
    case =1
    if case ==1:
        plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1)
    

    elif case == 2:
        H, xedges, yedges = histogram2d(spikeTimesFromEventOnset, sortedIndexForEachSpike, bins=(200, 20))
        H=np.rot90(H)
        H=np.flipud(H)
        #Hmasked = np.ma.masked_where(H==0, H)
        #pcolormesh(xedges, yedges, Hmasked)
        pcolormesh(xedges, yedges, H)

    #title(spike_filename)
    axvline(x=0, ymin=0, ymax=1, color='r')

#xlabel('time(sec)')
#tight_layout()
show()
'''
fig=gcf()
import plotly.plotly as py
py.sign_in('nickponvert', '915nslwqbx')
unique_url = py.plot_mpl(fig, strip_style=True)
'''
