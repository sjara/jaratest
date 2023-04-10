"""
Load behavior and show the time of each trial.
"""

from jaratoolbox import loadbehavior

subject = 'inpi001'
paradigm = 'oddball_sequence'
session = '20230322asaline'
behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)

startTrialState = bdata.stateMatrix['statesNames']['startTrial']
trialStartEvents = (bdata.events['nextState']==startTrialState)
trialStartTime = bdata.events['eventTime'][trialStartEvents]

print('Time when each trial started')
print(trialStartTime)

runStart = [133, 298] - trialStartTime[0]
runStop = [145, 300 ] - trialStartTime[0]


test = [i for i,v in enumerate(trialStartTime) if v >= runStart[0] and v <= runStop[0]]
test.extend([i for i,v in enumerate(trialStartTime) if v >= runStart[1] and v <= runStop[1]])



