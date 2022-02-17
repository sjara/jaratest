import os
import sys
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

print('Enter which subjects you want to look at: 1 = VOT, 2 = FT, 3 = all, 4 = AM cohort, 5 = PM cohort or enter a specific animal name')
whichSubject = input()
if whichSubject == '1':
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042'] #VOT animals
elif whichSubject == '2':
    subject = ['bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051'] #FT animals
elif whichSubject == '3':
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']
elif whichSubject == '4':
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili048', 'bili049', 'bili050', 'bili051']
elif whichSubject == '5':
    subject = ['bili039', 'bili040', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047']
else:
    subject = [whichSubject]

paradigm = '2afc_speech'

# Add the dates
#session = '20220113a'
print('input the session name (e.g. 20220113):')
session = input()
suffix = "a"
session = session + suffix


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
        whichFeature = bdata.labels['relevantFeature'][bdata['relevantFeature'][-1]]

        print('% Right Correct: {}'.format(rightPercentCorrect))
        print('% Left Correct: {}'.format(leftPercentCorrect))
        print('# Right Errors: {}'.format(sum(rightError)))
        print('# Left Errors: {}'.format(sum(leftError)))
        print('# of noChoice: {}'.format(np.sum(noChoice)))
    ### Deal with psychometric###
    if any(bdata['psycurveMode']):
        if bdata['relevantFeature'][-1] == bdata.labels['relevantFeature']['spectral']:
            targetFrequency = bdata['targetFTpercent']
        elif bdata['relevantFeature'][-1] == bdata.labels['relevantFeature']['temporal']:
            targetFrequency = bdata['targetVOTpercent']

        valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
        possibleFreq = np.unique(targetFrequency)
        nFreq = len(possibleFreq)
        trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice,targetFrequency,valid)
        fontsize = 12
        fig1 = plt.subplot(3,len(subject)/3,nSub)
        plt.title('{0} [{1}]'.format(subject[nSub],session))
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
        plt.xlabel('{0} level (a.u.)'.format(whichFeature) ,fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)
        plt.show()





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
