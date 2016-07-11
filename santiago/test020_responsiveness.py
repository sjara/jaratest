'''
Evaluate sound responsiveness
'''

from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import ephyscore
import os
import numpy as np
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import matplotlib.pyplot as plt

reload(spikesanalysis)


SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial
binWidth = 0.010 # Size of each bin in histogram in seconds

timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)

ephysRootDir = settings.EPHYS_PATH

experimenter = 'santiago'
paradigm = '2afc'

CASE = 2
if CASE==1:
    import allcells_test055 as allcells
    cellID = allcells.cellDB.findcell('test055','20150228a',3,11)
    cellID = allcells.cellDB.findcell('test055','20150228a',3,6)
elif CASE==2:
    import allcells_test017 as allcells
    cellID = allcells.cellDB.findcell('test017','20150309a',6,10)

oneCell = allcells.cellDB[cellID]

subject = oneCell.animalName
behavSession = oneCell.behavSession
ephysSession = oneCell.ephysSession
ephysRoot = os.path.join(ephysRootDir,subject)

# -- Load Behavior Data --
behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
bdata = loadbehavior.BehaviorData(behaviorFilename)

# -- Load event data and convert event timestamps to ms --
ephysDir = os.path.join(ephysRoot, ephysSession)
eventFilename=os.path.join(ephysDir, 'all_channels.events')
events = loadopenephys.Events(eventFilename) # Load events data
eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 

soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)

# -- Load Spike Data From Certain Cluster --
spkData = ephyscore.CellData(oneCell)
spkTimeStamps = spkData.spikes.timestamps

eventOnsetTimes = eventTimes[soundOnsetEvents]

(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)

plt.clf()
ax1=plt.subplot(2,1,1)
plt.plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.')
plt.show()

# -- Calculate sound responsiveness --

baseRange = [-0.050,-0.025]              # Baseline range (in seconds)
rangeLength = np.diff(baseRange)         # Time-bin size
binEdges = np.arange(-8,24)*rangeLength  # Edges of bins to calculate response (in seconds)

#baseRange = [-0.1, 0]              # Baseline range (in seconds)
#binEdges = [-0.1,0, 0.1, 0.2]
[zStat,pValue,maxZ] = spikesanalysis.response_score(spikeTimesFromEventOnset,indexLimitsEachTrial,baseRange,binEdges)

print 'Max absolute z-score: {0}'.format(maxZ)

ax2=plt.subplot(2,1,2,sharex=ax1)
plt.axhline(0,ls='-',color='0.5')
plt.axhline(+3,ls='--',color='0.5')
plt.axhline(-3,ls='--',color='0.5')
plt.step(binEdges[:-1],zStat,where='post',lw=2)
plt.ylabel('z-score')
plt.xlabel('time (sec)')
plt.show()

