'''
ephysBehaveDataAlignmentCheck.py
Checks if the Behavior data and Ephys data is aligned
author: Billy Walker
'''


#from jaratoolbox import ephyscore
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
#from jaratoolbox import spikesanalysis
#from jaratoolbox import extraplots
import numpy as np
import matplotlib.pyplot as plt
#from pylab import * #I SHOULD CHANGE THIS. EFFECTS ARGSORT
import os



subject = 'test089'
behavSession = '20160125a'
ephysSession = '2016-01-25_15-03-55'




SAMPLING_RATE=30000.0
ephysRootDir='/home/billywalker/data/ephys/'
experimenter = 'santiago'
paradigm = '2afc'
ephysRoot = ephysRootDir+subject+'/'
eventID = 0

# -- Load Behavior Data --
behaviorFilename = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,behavSession)
bdata = loadbehavior.BehaviorData(behaviorFilename)
numberOfTrials = len(bdata['choice'])

# -- Load event data and convert event timestamps to ms --
ephysDir = os.path.join(ephysRoot, ephysSession)
eventFilename=os.path.join(ephysDir, 'all_channels.events')
events = loadopenephys.Events(eventFilename) # Load events data
eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
multipleEventOnset=np.array(events.eventID)  #loads the onset times of all events (matches up with eventID to say if event 1 went on (1) or off (0)
eventChannel = np.array(events.eventChannel) #loads the ID of the channel of the event. For example, 0 is sound event, 1 is trial event, 2 ...


# -- Only use event onset times of one event --
oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want
eventOnsetTimes = eventTimes[eventOnset == 1] #This gives only the times of the onset of the channel you want

behavTimes = np.empty(numberOfTrials)
prevTimeCenter = bdata['timeCenterIn'][0]
for trial,timeCenter in enumerate(bdata['timeCenterIn']):
    behavTimes[trial] = timeCenter - prevTimeCenter
    prevTimeCenter = timeCenter

ephysTimes = np.empty(np.sum(eventOnset))
prevTime = eventOnsetTimes[0]
for etrial,timeSound in enumerate(eventOnsetTimes):
    ephysTimes[etrial] = timeSound - prevTime
    prevTime = timeSound

numberToPlot = min(numberOfTrials,np.sum(eventOnset))
differenceTimes = np.empty(numberToPlot)
firstSkipped = True
badTrial = 0
for dtrial in range(0,numberToPlot):
    differenceTimes[dtrial] = ephysTimes[dtrial]-behavTimes[dtrial]
    if (abs(differenceTimes[dtrial])>0.2) and firstSkipped:
        badTrial = dtrial
        firstSkipped = False

differenceTimesSkipped = np.empty(numberToPlot)
for dstrial in range(0,badTrial):
    differenceTimesSkipped[dstrial] = ephysTimes[dstrial]-behavTimes[dstrial]
for dstrial in range(badTrial,numberToPlot):
    differenceTimesSkipped[dstrial] = ephysTimes[dstrial]-behavTimes[dstrial+1]

plt.clf()
differencePlt = plt.subplot2grid((1,2), (0, 0), colspan=1)
plt.plot(differenceTimes)
differenceSkippedPlt = plt.subplot2grid((1,2), (0, 1), colspan=1)
plt.plot(differenceTimesSkipped)
plt.show()




print 'the number of behavior trials is {}'.format(numberOfTrials)
print 'the number of ephys events trials is {}'.format(np.sum(eventOnset))
print 'the skipped trial is {}'.format(badTrial)
