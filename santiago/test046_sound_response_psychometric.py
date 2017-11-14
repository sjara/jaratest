'''
Test the sound response of neurons during psychometric task.


adap013,20160223a,3,4
adap017,20160317a,5,3
adap017,20160323a,1,7
adap017,20160401a,4,10
adap017,20160414a,4,9
test053,20150618a,5,6
test053,20150629a,5,11
test055,20150313a,4,7
'''

from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from jaratoolbox import extraplots
import numpy as np
from matplotlib import pyplot as plt
import os


SAMPLING_RATE=30000.0
timeRange=[-0.3, 0.5] #In seconds
responseRange = [0.0,0.100] # range of time to count spikes in after event onset

#subject='adap013'; behavSession='20160223a'; tune='2016-02-23_10-30-57'; task='2016-02-23_10-39-53'; tetrode=3; cluster=4
#subject='adap017'; behavSession='20160317a'; tune='2016-03-17_16-14-16'; task='2016-03-17_16-22-52'; tetrode=5; cluster=3
subject='gosi004'; behavSession='20170303a'; tune='2017-03-03_16-17-38'; task='2017-03-03_16-24-05'; tetrode=4; cluster=7

MODE = 1        # 0:Tuning, 1:Task
MULTIUNIT = 1    # 0:SingleCluster, 1:Multiunit

if MODE==0:
    ephysSession=tune
    paradigm = 'tuning_curve'
    if subject=='gosi004': paradigm = 'laser_tuning_curve'
    freqKeyName = 'currentFreq'
    plt.figure(1)
elif MODE==1:
    ephysSession=task
    paradigm = '2afc'
    freqKeyName = 'targetFrequency'
    plt.figure(2)
    

fullephysDir = os.path.join(settings.EPHYS_PATH,subject, ephysSession)
eventFilename = os.path.join(fullephysDir, 'all_channels.events')

behavDataFileName = loadbehavior.path_to_behavior_data(subject,paradigm,behavSession)

bdata = loadbehavior.BehaviorData(behavDataFileName)
freqEachTrial = bdata[freqKeyName]
nTrials = len(freqEachTrial)

# -- Load event data and convert event timestamps to ms --
ev = loadopenephys.Events(eventFilename)
eventTimes = np.array(ev.timestamps)/SAMPLING_RATE
evID = np.array(ev.eventID)
evCh = np.array(ev.eventChannel)
eventOnsetTimes = eventTimes[(evCh==0) & (evID==1)]

if nTrials != len(eventOnsetTimes):
    print 'Number of behavior trials and ephys trials do not match. The longest will be cut.'
    print 'nTrials={0} events={1}'.format(nTrials,len(eventOnsetTimes))
    minNtrials = min(nTrials,len(eventOnsetTimes))
    nTrials = minNtrials
    freqEachTrial = freqEachTrial[:nTrials]
    eventOnsetTimes = eventOnsetTimes[:nTrials]

possibleFreq = np.unique(freqEachTrial)

#freqEachTrial = freqEachTrial[selectedTrials]
#eventOnsetTimes = eventOnsetTimes[selectedTrials]

if MODE==0: # Tuning
    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
elif MODE==1: # Task
    trialsEachComb = behavioranalysis.find_trials_each_combination(freqEachTrial,possibleFreq,bdata['valid'],[0,1])
    trialsEachFreq = trialsEachComb[:,:,1] # valid
    #trialsEachFreq = trialsEachComb[:,:,0] # invalid
    
#numTrialsEachFreq = trialsEachFreq.sum(axis=0)
#sortedTrials = np.nonzero(trialsEachFreq.T)[1] # The second array contains the sorted indexes
#sortingInds = np.argsort(sortedTrials) # gives array of indices that would sort the sortedTrials

# -- Load ephys --
spikesFilename = os.path.join(fullephysDir, 'Tetrode{0}.spikes'.format(tetrode))
clustersFilename = os.path.join(fullephysDir+'_kk', 'Tetrode{0}.clu.1'.format(tetrode))
dataSpikes = loadopenephys.DataSpikes(spikesFilename)
if MULTIUNIT:
    spkTimeStamps = np.array(dataSpikes.timestamps)/SAMPLING_RATE
else:
    dataSpikes.set_clusters(clustersFilename)
    spkTimeStamps = np.array(dataSpikes.timestamps[dataSpikes.clusters==cluster])/SAMPLING_RATE
    
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
#sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike]


#plt.subplot(1,2,1)
plt.clf()
#plt.plot(spikeTimesFromEventOnset,sortedIndexForEachSpike,'.k',ms=3)
extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachFreq)
plt.show()


