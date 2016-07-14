'''
Load sound frequencies from tuning_curve data
'''

from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os


SAMPLING_RATE=30000.0

#behavDataFileName = '/home/jarauser/tmp/test035_tuning_curve_20140708_2.h5'
#event_filename = '/home/jarauser/tmp/2014-07-08_17-54-12/all_channels.events'
#spike_filename = '/home/jarauser/tmp/2014-07-08_17-54-12/Tetrode6.spikes'

'''
dataDir = '/home/jarauser/data/ephys/test030/2014-07-23_15-11-34/'
behavDataFileName = os.path.join(dataDir,'test030_tuning_curve_20140723a.h5')
event_filename = os.path.join(dataDir,'all_channels.events')
spike_filename = os.path.join(dataDir,'Tetrode4.spikes')

dataDir = '/home/jarauser/data/ephys/test030/2014-07-23_15-56-09/'
behavDataFileName = os.path.join(dataDir,'test030_tuning_curve_20140723b.h5')
event_filename = os.path.join(dataDir,'all_channels.events')
spike_filename = os.path.join(dataDir,'Tetrode4.spikes')
'''
'''
dataDir = '/home/jarauser/data/ephys/test030/2014-07-23_16-36-05/'
behavDataFileName = os.path.join(dataDir,'test030_tuning_curve_20140723e.h5')
event_filename = os.path.join(dataDir,'all_channels.events')
spike_filename = os.path.join(dataDir,'Tetrode4.spikes')
'''

ephysDir='/home/nick/data/ephys/pinp003/2014-08-04_17-54-34'
behaviorDir='/home/nick/data/behavior/nick/hm4d002'
behavDataFileName=os.path.join(behaviorDir, 'hm4d002_tuning_curve_20140804a.h5')
event_filename=os.path.join(ephysDir, 'all_channels.events')
spike_filename=os.path.join(ephysDir, 'Tetrode2.spikes')


# -- Load behavior data -
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


# -- Load ephys data --

ev=loadopenephys.Events(event_filename)
sp=loadopenephys.DataSpikes(spike_filename)

spkTimeStamps=np.array(sp.timestamps)/SAMPLING_RATE
eventTimes=np.array(ev.timestamps)/SAMPLING_RATE
evID=np.array(ev.eventID)
eventOnsetTimes=eventTimes[evID==1]

# -- Remove last started (but not finished) trial --
eventOnsetTimes = eventOnsetTimes[:-1]

timeRange=[-0.5, 1]
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]

###plot(spikeTimesFromEventOnset, trialIndexForEachSpike, '.')
if 1:
    plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.')
else:
    stimOnsetInds = bdata.events['nextState']==2
    stimOnsetBehavTime = bdata.events['eventTime'][stimOnsetInds]

    plot(stimOnsetBehavTime-stimOnsetBehavTime[0],'.')
    hold(1)
    plot(eventOnsetTimes-eventOnsetTimes[0],'x',color='g')
    hold(0)
    ylabel('Time of event (s)')
    xlabel('Event number')

draw()
show()
