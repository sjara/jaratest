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

print('Enter which subjects you want to look at: 1 = all or enter a specific animal name')
whichSubject = input()
if whichSubject == '1':
    subject = ['febe007', 'febe008'] #VOT animals
else:
    subject = [whichSubject]

paradigm = 'headfixed_speech'

# Add the dates
#session = '20220113a'
print('input the session name (e.g. 20220113a):')
session = input()
#suffix = "a"
#session = session + suffix


## Multiple subjects, single day
for nSub in range(len(subject)):
    behavFile = loadbehavior.path_to_behavior_data(subject[nSub], paradigm, session)
    bdata = loadbehavior.BehaviorData(behavFile)


    taskMode = bdata.labels['taskMode'][bdata['taskMode'][-1]]
    numLicksL = bdata['nLicksLeft'][-1]
    numLicksR = bdata['nLicksRight'][-1]
    print(subject[nSub])
    numTrials = len(bdata['taskMode'])
    print(taskMode)
    print('# of Trials: {}'.format(numTrials))
    print('# Licks L: {}'.format(numLicksL))
    print('# Licks R: {}'.format(numLicksR))

    if bdata['taskMode'][-1] == bdata.labels['taskMode']['discriminate_stim']:
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
        if len(subject) > 1:
            numSubPlots = int(len(subject)/3)
        else:
            numSubPlots = 1
        subPlotInd = nSub + 1
        fig1 = plt.subplot(3,numSubPlots,subPlotInd)
        plt.title('{0} [{1}]'.format(subject[nSub],session))
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
        plt.xlabel('{0} level (a.u.)'.format(whichFeature) ,fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)
        plt.show()





    if bdata['taskMode'][-1] == bdata.labels['taskMode']['water_after_sound']: #Stage1
        print('Stage1')
        if numLicksL >= 100 and numLicksR >= 100:
            print('move to next stage')
        else:
            print('stay on this stage')
    elif bdata['taskMode'][-1] == bdata.labels['taskMode']['lick_on_stim']: #Stage2
        print('Stage2')
        if bdata['nHitsLeft'][-1] >= 100 and bdata['nHitsRight'][-1] >= 100:
            print('# Hits L: {}'.format(bdata['nHitsLeft'][-1]))
            print('# Hits R: {}'.format(bdata['nHitsRight'][-1]))
            print('move to next stage')
        else:
            print('# Hits L: {}'.format(bdata['nHitsLeft'][-1]))
            print('# Hits R: {}'.format(bdata['nHitsRight'][-1]))
            print('stay on this stage')
    elif bdata['taskMode'][-1] == bdata.labels['taskMode']['discriminate_stim']:
        if bdata['rewardSideMode'][-1] == bdata.labels['rewardSideMode']['repeat_mistake']: #Stage3
            print('Stage3')
            if leftPercentCorrect >= 70 and sum(leftTrials) >=100 and rightPercentCorrect >= 70 and sum(rightTrials) >= 100:
                print('move to next stage')
            else:
                print('stay on this stage')
        elif bdata['rewardSideMode'][-1] == bdata.labels['rewardSideMode']['random']: #Stage4
            print('you are on stage4! Bother Jenny if there is not a stage5 yet')

        '''
        elif bdata['psycurveMode'][-1] != bdata.labels['psycurveMode']['off']:
            print('you are on psycurve mode, woohoo!')
            if bdata['psycurveMode'][1] == bdata.labels['psycurveMode']['uniform']:
                print('psycurveMode = uniform')
            elif bdata['psycurveMode'][1] == bdata.labels['psycurveMode']['extreme80pc']:
                print('psycurveMode = extremes80pct')
        else:
            if rightPercentCorrect < 20 or leftPercentCorrect < 20:
                print('move to bias mode')
            elif rightPercentCorrect >= 70 and leftPercentCorrect >= 70 and numTrials >= 300:
                print('move to psycuve mode')
            else:
                print('stay on this stage')'''
