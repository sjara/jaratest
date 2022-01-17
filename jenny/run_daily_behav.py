import os
import sys
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
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
#subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042']

## FT animals
#subject = ['bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']

print('Enter which subjects you want to look at: 1 = VOT, 2 = FT, 3 = all, or enter a specific animal name')
whichSubject = input()
if whichSubject == '1':
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042']
elif whichSubject == '2':
    subject = ['bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']
elif whichSubject == '3':
    #subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']
    subject = ['bili034', 'bili035', 'bili037', 'bili038', 'bili039', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']

else:
    subject = [whichSubject]

paradigm = '2afc_speech'

# Add the dates
#session = '20220113a'
print('input the session name (e.g. 20220113a):')
session = input()


## Multiple subjects, single day
for nSub in range(len(subject)):
    behavFile = loadbehavior.path_to_behavior_data(subject[nSub], paradigm, session)
    bdata = loadbehavior.BehaviorData(behavFile)


    automationMode = bdata['automationMode'][-1] == bdata.labels['automationMode']['increase_delay']
    mode = bdata.labels['outcomeMode'][bdata['outcomeMode'][-1]]
    print()
    print(subject[nSub])
    numTrials = len(bdata['outcomeMode'])
    print(mode)
    print('# of Trials: {}'.format(numTrials))
    #print(numTrials)

    if automationMode == 1:
        maxDelay = np.max(bdata['delayToTarget'])
        print('maxDelay: {}'.format(maxDelay))
        #print(maxDelay)


    if bdata['outcomeMode'][-1] == bdata.labels['outcomeMode']['only_if_correct']:
        leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
        rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
        leftChoice = bdata['choice'] == bdata.labels['choice']['left']
        rightChoice = bdata['choice'] == bdata.labels['choice']['right']
        noChoice = bdata['choice'] == bdata.labels['choice']['none']
        leftCorrect = leftTrials & leftChoice
        leftError = leftTrials & rightChoice
        leftInvalid = leftTrials & noChoice
        rightCorrect = rightTrials & rightChoice
        rightError = rightTrials & leftChoice
        rightInvalid = rightTrials & noChoice
        print('% Right Correct: {}'.format(round(sum(rightCorrect)/sum(rightTrials)*100,2)))
        print('% Left Correct: {}'.format(round(sum(leftCorrect)/sum(leftTrials)*100,2)))
        print('# Right Errors: {}'.format(sum(rightError)))
        print('# Left Errors: {}'.format(sum(leftError)))
        print('# of noChoice: {}'.format(np.sum(noChoice)))
        if bdata['antibiasMode'][-1] == bdata.labels['antibiasMode']['repeat_mistake']:
            print('Bias Correct ON')





# 'soundActionMode' ('high_left' or 'low_left')
# 'rewardSide' ('left','right')
# 'outcome' ('aborted', 'aftererror', 'correct', 'error', 'free', 'invalid', 'nochoice')
# 'choice' ('left', 'right', 'none')
# 'antibiasMode' = 'off', 'repeat_mistake'
