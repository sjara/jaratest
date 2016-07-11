'''
Fixing skipped behavior trials

sshfs -o idmap=user jarauser@jarahub:/data/jarashare/ /mnt/jarashare
rsync -a --progress --exclude *.continuous sjara@jarahub:/data/ephys/adap005/2015-12-15_14-02-08 ./
'''

from jaratoolbox import loadbehavior
reload(loadbehavior)
from jaratoolbox import behavioranalysis
reload(behavioranalysis)
from jaratoolbox import loadopenephys
from jaratoolbox import settings
import os
import numpy as np
from pylab import *

SAMPLING_RATE=30000.0
soundTriggerChannel = 0 # channel 0 is the sound presentation, 1 is the trial

subject = 'adap005'
experimenter = 'lan'
paradigm = '2afc'
behavSession = '20151215a'
ephysSession = '2015-12-15_14-02-08'

# -- Load behavior data --
behavDataFileName = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
#bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
bdata = loadbehavior.FlexCategBehaviorData(behavDataFileName,readmode='full')
#bdata.remove_trials([166, 1216])
bdata.find_trials_each_block()
soundOnsetTimeBehav = bdata['timeTarget']
nTrialsBehav = len(soundOnsetTimeBehav)

# -- Load event data and convert event timestamps to ms --
ephysDir = os.path.join(settings.EPHYS_PATH, subject, ephysSession)
eventFilename = os.path.join(ephysDir, 'all_channels.events')
events = loadopenephys.Events(eventFilename) # Load events data
eventTimes = np.array(events.timestamps)/SAMPLING_RATE # in sec
soundOnsetEvents = (events.eventID==1) & (events.eventChannel==soundTriggerChannel)
eventOnsetTimes = eventTimes[soundOnsetEvents]
nTrialsEphys = len(eventOnsetTimes)
soundOnsetTimeEphys = eventOnsetTimes

print 'N (behav) = {0}'.format(nTrialsBehav)
print 'N (ephys) = {0}'.format(nTrialsEphys)

sOnBehav = soundOnsetTimeBehav-soundOnsetTimeBehav[0]
sOnEphys = soundOnsetTimeEphys-soundOnsetTimeEphys[0]

minNtrials = min(nTrialsEphys,nTrialsBehav)
tRange = np.arange(0,minNtrials-1)

tDiff = sOnBehav[tRange]-sOnEphys[tRange]


'''
while True:
    firstIndex = np.flatnonzero(abs(tDiff)>0.4)  # HARDCODED!
    if len(firstIndex):
        removedTrials.append(firstIndex[0]+len(removedTrials))
        soundOnsetTimeBehav = np.delete(soundOnsetTimeBehav,firstIndex[0])
        nTrialsBehav = len(soundOnsetTimeBehav)
        sOnBehav = soundOnsetTimeBehav-soundOnsetTimeBehav[0]
        minNtrials = min(nTrialsEphys,nTrialsBehav)
        tRange = np.arange(0,minNtrials-1)
        tDiff = sOnBehav[tRange]-sOnEphys[tRange]
        #break
    else:
        break


removedTrials = []
while True:
    firstIndex = np.flatnonzero(abs(tDiff)>0.4)  # HARDCODED!
    if len(firstIndex):
        removedTrials.append(firstIndex[0]+len(removedTrials))
        sOnBehav = np.delete(sOnBehav,firstIndex[0])
        minNtrials = min(nTrialsEphys,len(sOnBehav))
        tRange = np.arange(0,minNtrials-1)
        tDiff = sOnBehav[tRange]-sOnEphys[tRange]
        #break
    else:
        break
print removedTrials
'''

### THIS SHOWS HOW TO USE THE NEW METHODS ###
missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
print missingTrials
'''
'''
 

### FIX: don't use the last ephys trial if it doesn't have a behav trial

clf()

'''
plot(sOnBehav,'.b',ms=8)
hold(1)
plot(sOnEphys,'.r',ms=8)
'''

# plot(sOnBehav[tRange]-sOnEphys[tRange],'.k',ms=8)

plot(tDiff,'.k',ms=8)

show()


'''
if nTrials != len(eventOnsetTimes):
    print 'Number of behavior trials and ephys trials do not match. The longest will be cut.'
    minNtrials = min(nTrials,len(eventOnsetTimes))
    nTrials = minNtrials
    freqEachTrial = freqEachTrial[:nTrials]
    intensityEachTrial = intensityEachTrial[:nTrials]
    eventOnsetTimes = eventOnsetTimes[:nTrials]
'''
