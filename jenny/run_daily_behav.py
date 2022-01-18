import os
import sys
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis


print('Enter which subjects you want to look at: 1 = VOT, 2 = FT, 3 = all, or enter a specific animal name')
whichSubject = input()
if whichSubject == '1':
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042'] #VOT animals
elif whichSubject == '2':
    subject = ['bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051'] #FT animals
elif whichSubject == '3':
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']

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

    if automationMode == 1:
        maxDelay = np.max(bdata['delayToTarget'])
        print('maxDelay: {}'.format(maxDelay))


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
        rightPercentCorrect = round(sum(rightCorrect)/sum(rightTrials)*100,2)
        leftPercentCorrect = round(sum(leftCorrect)/sum(leftTrials)*100,2)
        print('% Right Correct: {}'.format(rightPercentCorrect))
        print('% Left Correct: {}'.format(leftPercentCorrect))
        print('# Right Errors: {}'.format(sum(rightError)))
        print('# Left Errors: {}'.format(sum(leftError)))
        print('# of noChoice: {}'.format(np.sum(noChoice)))

    if bdata['outcomeMode'][-1] == bdata.labels['outcomeMode']['sides_direct']:
        if numTrials >= 100:
            print('move to next stage')
        else:
            print('stay on this stage')
    elif bdata['outcomeMode'][-1] == bdata.labels['outcomeMode']['direct']:
        if numTrials >= 200:
            print('move to next stage')
        else:
            print('stay on this stage')
    elif bdata['outcomeMode'][-1] == bdata.labels['outcomeMode']['on_next_correct']:
        if numTrials >= 300:
            print('move to next stage')
        else:
            print('stay on this stage')
    elif bdata['outcomeMode'][-1] == bdata.labels['outcomeMode']['only_if_correct']:
        if bdata['antibiasMode'][-1] == bdata.labels['antibiasMode']['repeat_mistake']:
            print('Bias Correct ON')
            if rightPercentCorrect >= 30 and leftPercentCorrect >= 30:
                print('move off of bias mode')
            else:
                print('stay on bias mode')
        elif bdata['psycurveMode'][-1] != bdata.labels['psycurveMode']['off']:
            print('you are on psycurve mode, woohoo!')
        else:
            if rightPercentCorrect < 20 or leftPercentCorrect < 20:
                print('move to bias mode')
            elif rightPercentCorrect >= 70 and leftPercentCorrect >= 70 and numTrials >= 300:
                print('move to psycuve mode')
            else:
                print('stay on this stage')
