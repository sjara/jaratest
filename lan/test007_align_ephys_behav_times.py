'''
Script to figure out the problem when ephys recording file and behav file don't have the same number of trials.
'''

from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
import numpy as np
import matplotlib.pyplot as plt

EPHYS_SAMPLING_RATE = 30000.0

#ephysfn = '/home/languo/data/ephys/d1pi002/2015-08-14_15-42-36/all_channels.events'   #bData has 999 trials while len(eventOnsetTimes)=996
ephysfn = '/home/languo/data/ephys/d1pi002/2015-08-14_14-55-22/all_channels.events'
eventData=loadopenephys.Events(ephysfn)

#behavfn ='/home/languo/data/behavior/lan/d1pi002/d1pi002_laser_tuning_curve_20150814b.h5'  #bData has 999 trials while len(eventOnsetTimes)=996
behavfn ='/home/languo/data/behavior/lan/d1pi002/d1pi002_laser_tuning_curve_20150814a.h5'
bData = loadbehavior.BehaviorData(behavfn)

eventID=1
eventChannel=0
evID=np.array(eventData.eventID)
evChannel = np.array(eventData.eventChannel)
eventTimes = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE
eventOnsetTimes=eventTimes[(evID==eventID)&(evChannel==eventChannel)]

eventOnsetTimes=eventOnsetTimes-eventOnsetTimes[0]

indexLEET=bData.events['indexLastEventEachTrial']
indexFEET=np.hstack((4,(indexLEET[:-1]+1))) #hard-coded index for start of first trial as 4 

time_FEET=bData.events['eventTime'][indexFEET]
time_FEET=time_FEET-time_FEET[0]

print 'time_FEET first 10 trials={}'.format(time_FEET[0:10])
print 'eventOnsetTimes first 10 trials={}'.format(eventOnsetTimes[0:10])

plt.figure()
plt.plot(time_FEET, 'r.')
plt.hold(1)
plt.plot(eventOnsetTimes, 'g.')
plt.hold(1)

'''
time_FEET2=time_FEET[5:]-time_FEET[5]
print 'time_FEET2 first 10 trials={}'.format(time_FEET2[0:10])
plt.plot(time_FEET2, 'b.')
plt.show()


timedif = np.diff(time_FEET2)
plt.clf()
plt.plot(timedif, '.')
'''
