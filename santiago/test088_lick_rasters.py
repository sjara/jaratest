"""
Plot histogram of lick times aligned to sound onset and sound change (on change detection task).
"""

import sys
sys.path.append('/home/sjara/src/')  # This is specific to Santiago's computer

import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import spikesanalysis

    
subject = 'chad051'  # 053, 054 051
session = '20201123a'
paradigm = 'detectiontwochoice'  # The paradigm name needs to change!

behavFile = loadbehavior.path_to_behavior_data(subject,paradigm,session)
bdata = loadbehavior.BehaviorData(behavFile)

nTrials = len(bdata['outcome'])
soundOnTime = np.empty(nTrials)

activePortStr = bdata.labels['activePort'][bdata['activePort'][-1]]
activeLickEvent = activePortStr[0].upper() + 'in'  # This create something like 'Lin'
lickEvents = bdata.events['eventCode'] == bdata.stateMatrix['eventsNames'][activeLickEvent]
licksTimes = bdata.events['eventTime'][lickEvents]

fontsizeLabels = 14
plt.clf()

axTop = plt.subplot(2,1,1)
timeRange = [-5,5]
mainEventState = 'playPre'
xLabel = 'Time from first sound onset (s)'
mainEventCode = bdata.stateMatrix['statesNames'][mainEventState]
lastEventThisTrial = 0
for indTrial in range(nTrials):
    lastEventPreviousTrial = lastEventThisTrial
    lastEventThisTrial = bdata.events['indexLastEventEachTrial'][indTrial]
    statesThisTrial = bdata.events['nextState'][lastEventPreviousTrial:lastEventThisTrial]
    eventTimesThisTrial = bdata.events['eventTime'][lastEventPreviousTrial:lastEventThisTrial]
    if mainEventCode in statesThisTrial:
        firstPlayPre = np.flatnonzero(statesThisTrial==mainEventCode)[0]
        soundOnTime[indTrial] = eventTimesThisTrial[firstPlayPre]
    else:
        soundOnTime[indTrial] = np.nan
(lickTimesFromEventOnset,trialIndexForEachLick,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(licksTimes, soundOnTime, timeRange)
plt.plot(lickTimesFromEventOnset, trialIndexForEachLick, '.k')
plt.ylim([-1,nTrials])
plt.ylabel('Trial', fontsize=fontsizeLabels)
plt.xlabel(xLabel, fontsize=fontsizeLabels)
plt.xlim(timeRange)

axBot = plt.subplot(2,1,2)
timeRange = [-4,6]
xLabel = 'Time from potential sound change (s)\n(false alarms included even though there is no change)'
startTrialID = bdata.stateMatrix['statesNames']['startTrial']
startTrialInds = bdata.events['nextState']==startTrialID
startTrialTime = bdata.events['eventTime'][startTrialInds][:-1] # Remove incomplete last trial
postEventTime = startTrialTime + bdata['interTrialInterval'] + bdata['preDuration']
soundOnTime = postEventTime
    
(lickTimesFromEventOnset,trialIndexForEachLick,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(licksTimes, soundOnTime, timeRange)
plt.plot(lickTimesFromEventOnset, trialIndexForEachLick, '.k')
plt.ylim([-1,nTrials])
plt.ylabel('Trial', fontsize=fontsizeLabels)
plt.xlabel(xLabel, fontsize=fontsizeLabels)
plt.xlim(timeRange)

plt.gcf().suptitle('{} - {}'.format(subject,session), fontweight='bold')
plt.show()




'''
selectedTrialsBool = bdata['outcome']==bdata.labels['outcome']['falseAlarm']
selectedTrialsInds = np.flatnonzero(selectedTrialsBool)
selectedLickInds = np.isin(trialIndexForEachLick, selectedTrialsInds) 
'''

'''
plt.clf()
#axTop = plt.subplot(2,1,1)
if 1:
    plt.plot(lickTimesFromEventOnset, trialIndexForEachLick, '.k')
else:
    plt.plot(lickTimesFromEventOnset, trialIndexForEachLick, '.b')
    plt.plot(lickTimesFromEventOnset[selectedLickInds], trialIndexForEachLick[selectedLickInds], '.r')
    plt.legend(['Other trials', 'False alarms'], loc='upper left', framealpha=1)
plt.ylim([-1,nTrials])
plt.ylabel('Trial')
#plt.title('Licks LEFT')
plt.xlabel(xLabel)
plt.xlim(timeRange)
plt.gcf().suptitle('{} - {}'.format(subject,session), fontweight='bold')
plt.show()
#plt.savefig('/tmp/example_lick_raster.png', format='png')

sys.exit()
'''



