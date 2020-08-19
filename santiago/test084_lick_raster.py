"""
Plot histogram of lick times aligned to sound change (on change detection task).
"""

import sys
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import spikesanalysis


subject = 'chad046'
session = '20200818a'
paradigm = 'detectiontwochoice'

behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)

nTrials = len(bdata['outcome'])
soundOnTime = np.empty(nTrials)
playPreCode = bdata.stateMatrix['statesNames']['playPre']
lastEventThisTrial = 0
for indTrial in range(nTrials):
    lastEventPreviousTrial = lastEventThisTrial
    lastEventThisTrial = bdata.events['indexLastEventEachTrial'][indTrial]
    statesThisTrial = bdata.events['nextState'][lastEventPreviousTrial:lastEventThisTrial]
    eventTimesThisTrial = bdata.events['eventTime'][lastEventPreviousTrial:lastEventThisTrial]
    if playPreCode in statesThisTrial:
        firstPlayPre = np.flatnonzero(statesThisTrial==playPreCode)[0]
        soundOnTime[indTrial] = eventTimesThisTrial[firstPlayPre]
    else:
        soundOnTime[indTrial] = np.nan

leftLicksTimes = bdata.events['eventTime'][bdata.events['eventCode']==bdata.stateMatrix['eventsNames']['Lin']]
rightLicksTimes = bdata.events['eventTime'][bdata.events['eventCode']==bdata.stateMatrix['eventsNames']['Rin']]

timeRange = [-1,3]
(lickTimesFromEventOnsetL,trialIndexForEachLickL,indexLimitsEachTrialL) = \
    spikesanalysis.eventlocked_spiketimes(leftLicksTimes, soundOnTime, timeRange)
(lickTimesFromEventOnsetR,trialIndexForEachLickR,indexLimitsEachTrialR) = \
    spikesanalysis.eventlocked_spiketimes(rightLicksTimes, soundOnTime, timeRange)


plt.clf()
axTop = plt.subplot(2,1,1)
plt.plot(lickTimesFromEventOnsetL,trialIndexForEachLickL,'.k')
plt.ylim([-1,nTrials])
plt.ylabel('Trial')
plt.title('Licks LEFT')
plt.subplot(2,1,2, sharex=axTop)
plt.plot(lickTimesFromEventOnsetR,trialIndexForEachLickR,'.k')
plt.ylim([-1,nTrials])
plt.xlim(timeRange)
plt.ylabel('Trial')
plt.xlabel('Time from sound onset (s)')
plt.title('Licks RIGHT')

sys.exit()




"""
# --- Older code ---

# Note that trialStartTime will have one more element than nTrials bceause
#      the last trial starts but does not end (and data for it are not saved).
trialStartTime = bdata.events['eventTime'][startTrialState]
waitForLickTime = bdata.events['eventTime'][waitForLickState]

#soundOnState = (bdata.events['nextState']==bdata.stateMatrix['statesNames']['playPre'])
#soundOnTime = bdata.events['eventTime'][soundOnState]
rewardSideLeft = bdata['rewardSide']==bdata.labels['rewardSide']['left']

startTrialState = bdata.events['nextState']==bdata.stateMatrix['statesNames']['startTrial']
waitForLickState = (bdata.events['nextState']==bdata.stateMatrix['statesNames']['waitForLick'])


#eventsThisTrial = bdata.events['eventCode'][lastEventPreviousTrial:lastEventThisTrial]
    if playPreCode in statesThisTrial:
        firstPlayPre = np.flatnonzero(statesThisTrial==playPreCode)[0]
        soundOnTime[indTrial] = eventTimesThisTrial[firstPlayPre]
    else:
        soundOnTime[indTrial] = np.nan

if 0:
    plt.plot(trialStartTime,'.')
    plt.plot(soundOnTime,'.')


    #leftLicksThisTrial = eventsThisTrial==bdata.stateMatrix['eventsNames']['Lin']
    #leftLicksTimesThisTrial = eventTimesThisTrial[leftLicksThisTrial]


#binEdges = np.arange(timeRange[0], timeRange[-1], 0.025)
#spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(lickTimesFromEventOnsetL, indexLimitsEachTrialL, binEdges)

#plt.imshow(spikeCountMat,aspect='auto')

"""
