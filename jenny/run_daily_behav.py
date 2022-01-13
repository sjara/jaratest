import os
import sys
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import behavioranalysis

##ToDo##
# Build pandas structure with stuff I want
# nRewarded
# nValid
# relevantFeature
# rewardSide
# targetPercentage
# valid
# sessionID
# subjectID


# Add the subject(s)
## VOT animals
#subject = 'bili034'
#subject = 'bili035'
#subject = 'bili036'
#subject = 'bili037'
#subject = 'bili038'
#subject = 'bili039'
#subject = 'bili040'
#subject = 'bili041'
#subject = 'bili042'
#subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042']

## FT animals
#subject = 'bili043'
#subject = 'bili044'
#subject = 'bili045'
#subject = 'bili046'
#subject = 'bili047'
#subject = 'bili048'
#subject = 'bili049'
#subject = 'bili050'
#subject = 'bili051'
subject = ['bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']

paradigm = '2afc_speech'

# Add the dates
sessions = ['20220112a']

'''
## Single session/subject
bdata = behavioranalysis.load_many_sessions(subject, sessions, paradigm)
sessionID = bdata['sessionID']
uniqueSessionID = np.unique(sessionID)
outcomeMode = bdata['outcomeMode']
sidesDirect = bdata['outcomeMode'] == bdata.labels['outcomeMode']['sides_direct']
automationMode = np.any(bdata['automationMode'])
direct = bdata['outcomeMode'] == bdata.labels['outcomeMode']['direct']

if automationMode == 1:
    maxDelay = np.max(bdata['delayToTarget'])
    print(maxDelay)
else:

print(subject)
numTrls = len(bdata['sessionID'])
print(numTrls)
print(np.unique(outcomeMode))

'''

## Multiple subjects, single day
for nSub in range(len(subject)):
    bdata = behavioranalysis.load_many_sessions(subject[nSub], sessions, paradigm)

    sessionID = bdata['sessionID']
    uniqueSessionID = np.unique(sessionID)
    outcomeMode = bdata['outcomeMode']
    sidesDirect = bdata['outcomeMode'] == bdata.labels['outcomeMode']['sides_direct']
    direct = bdata['outcomeMode'] == bdata.labels['outcomeMode']['direct']
    automationMode = np.any(bdata['automationMode'])
    mode = bdata.labels['outcomeMode'][bdata['outcomeMode'][0]]

    print(subject[nSub])
    numTrls = len(bdata['sessionID'])
    print(mode)
    print('numTrls')
    print(numTrls)


    if automationMode == 1:
        maxDelay = np.max(bdata['delayToTarget'])
        print(maxDelay)


# testing
