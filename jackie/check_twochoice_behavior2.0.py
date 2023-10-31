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

print('Enter which subjects you want to look at: 1 = test AM depth animals or enter a specific animal name')
whichSubject = input()
if whichSubject == '1':
    subject = ['test133', 'test134']
else:
    subject = [whichSubject]

paradigm = 'twochoice'

# Add the dates
#session = '20220113a'
print('input the session name (e.g. 20230918):')
session = input()
suffix = "a"
session = session + suffix


## Multiple subjects, single day
for nSub in range(len(subject)):
    behavFile = loadbehavior.path_to_behavior_data(subject[nSub], paradigm, session)
    bdata = loadbehavior.BehaviorData(behavFile)


    taskMode = bdata.labels['taskMode'][bdata['taskMode'][-1]]
    numLicksL = bdata['nLicksLeft'][-1]
    numLicksR = bdata['nLicksRight'][-1]
    if 'interrupt' in bdata.labels['outcome']:
        #numInterruptL = bdata['nInterruptsLeft'][-1] 
        numInterruptL = bdata['ninterruptsByLickL'][-1] #new 10/2023
        #numInterruptR = bdata['nInterruptsRight'][-1]
        #numInterruptR = bdata['nInterruptsByLickR'][-1] #new
        numEarlyLicksL = bdata['nEarlyLicksLeft'][-1]
        #numEarlyLicksL = bdata['nEarlyByLicksL'][-1] #new 10/2023
        numEarlyLicksR = bdata['nEarlyLicksRight'][-1]
        #numEarlyLicksR = bdata['nEarlyByLicksR'][-1] #new 10/2023 #still might have issues running/might be in wrong place
        numNoResponseL = bdata['nNoResponsesLeft'][-1]
        numNoResponseR = bdata['nNoResponsesRight'][-1]

    if 'interrupt' in bdata.labels['outcome']: 
        numInterruptL = bdata['nInterruptsLeft'][-1] 
        numInterruptR = bdata['nInterruptsRight'][-1]
        #numEarlyLicksL = bdata['nEarlyLicksLeft'][-1]
        #numEarlyLicksR = bdata['nEarlyLicksRight'][-1]
            
    print()
    print(subject[nSub])
    numTrials = len(bdata['taskMode'])
    print(taskMode)
    print('# of Trials: {}'.format(numTrials))
    #print('# Licks L: {}'.format(numLicksL))
    #print('# Licks R: {}'.format(numLicksR))

    if bdata['taskMode'][-1] == bdata.labels['taskMode']['discriminate_stim']:
        leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
        rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
        leftChoice = bdata['choice'] == bdata.labels['choice']['left']
        rightChoice = bdata['choice'] == bdata.labels['choice']['right']
        valid = bdata['choice'] != bdata.labels['choice']['none']
        noChoice = bdata['choice'] == bdata.labels['choice']['none']
        if 'interrupt' in bdata.labels['outcome']:
            earlyLick = bdata['outcome'] == bdata.labels['outcome']['earlyLick']
            interrupt = bdata['outcome'] == bdata.labels['outcome']['interrupt']
            noChoice = noChoice & ~earlyLick & ~interrupt
        else:
            earlyLick = bdata['outcome'] == bdata.labels['outcome']['falseAlarm']
            noChoice = noChoice & ~earlyLick
        leftCorrect = leftTrials & leftChoice
        leftError = leftTrials & rightChoice
        leftInvalid = leftTrials & noChoice
        rightCorrect = rightTrials & rightChoice
        rightError = rightTrials & leftChoice
        rightInvalid = rightTrials & noChoice
        rightPercentCorrect = round(sum(rightCorrect)/sum(rightTrials & valid)*100,2)
        leftPercentCorrect = round(sum(leftCorrect)/sum(leftTrials & valid)*100,2)
        #whichFeature = bdata.labels['relevantFeature'][bdata['relevantFeature'][-1]]
        print('# Responded Trials: {}'.format(sum(valid)))
        print('% Right Correct: {}'.format(rightPercentCorrect))
        print('% Left Correct: {}'.format(leftPercentCorrect))
        print('# Right Errors: {}'.format(sum(rightError)))
        print('# Left Errors: {}'.format(sum(leftError)))
        print('# of noChoice: {}'.format(np.sum(noChoice)))
        print('# of Early Licks: {}'.format(np.sum(earlyLick)))
        if 'interrupt' in bdata.labels['outcome']:
            print(f'Interrupts L: {numInterruptL}')
            print(f'Interrupts R: {numInterruptR}')
    else:
        print('# Licks L: {}'.format(numLicksL))
        print('# Licks R: {}'.format(numLicksR))



    if bdata['taskMode'][-1] == bdata.labels['taskMode']['water_after_sound']: #Stage1
        print('Stage 1')
        if numLicksL >= 100 and numLicksR >= 100:
            print('move to next stage')
        else:
            print('stay on this stage')
    elif bdata['taskMode'][-1] == bdata.labels['taskMode']['lick_on_stim']: #Stage2
        if bdata['lickBeforeStimOffset'][-1] == bdata.labels['lickBeforeStimOffset']['ignore']:
            print('Stage 2')
            if bdata['nHitsLeft'][-1] >= 100 and bdata['nHitsRight'][-1] >= 100:
                print('# Hits L: {}'.format(bdata['nHitsLeft'][-1]))
                print('# Hits R: {}'.format(bdata['nHitsRight'][-1]))
                print('move to next stage')
            else:
                print('# Hits L: {}'.format(bdata['nHitsLeft'][-1]))
                print('# Hits R: {}'.format(bdata['nHitsRight'][-1]))
                print('stay on this stage')
        elif bdata['lickBeforeStimOffset'][-1] == bdata.labels['lickBeforeStimOffset']['abort']:
            print('Stage 2.5')
            itiStart = bdata['interTrialIntervalMean'][0]
            itiEnd = bdata['interTrialIntervalMean'][-1]
            print(f'Starting ITI = {itiStart}s')
            print(f'Ending ITI = {itiEnd}s')
            if 'interrupt' in bdata.labels['outcome']:
                print(f'Interrupts L: {numInterruptL}')
                print(f'Interrupts L: {nInterruptsByLick}') #new 10/2023
                print(f'Interrupts R: {numInterruptR}')
                print(f'Interrupts R: {nnInterruptsByLick}') #new 10/2023
            if bdata['interTrialIntervalMean'][-1] >= 2.5:
                print('move to next stage')
            else:
                print(f'set new starting ITI to {itiEnd - 0.05}')

    elif bdata['taskMode'][-1] == bdata.labels['taskMode']['discriminate_stim']:
        if bdata['rewardSideMode'][-1] == bdata.labels['rewardSideMode']['repeat_mistake']: #Bias correct
            print('Bias Correct Mode')
            if leftPercentCorrect >= 30 and sum(leftChoice) >=100 and rightPercentCorrect >= 30 and sum(rightChoice) >= 100:
                print('move back to stage 3')
            else:
                print('stay on this stage')
        elif bdata['rewardSideMode'][-1] == bdata.labels['rewardSideMode']['random']: #Stage3 -6
            if bdata['psycurveMode'][-1] == bdata.labels['psycurveMode']['off']: #Stage3
                if leftPercentCorrect >= 70 and rightPercentCorrect >= 70 and (np.sum(rightChoice)+np.sum(leftChoice)) >= 300:
                    print('move to stage 4!')
                elif leftPercentCorrect < 20 or rightPercentCorrect < 20 and (np.sum(rightChoice) + np.sum(leftChoice)) >= 200:
                    print('move to bias correct')
                else:
                    print('stay on stage 3')
            else:
                if bdata['psycurveMode'][-1] == bdata.labels['psycurveMode']['extreme80pc']:
                    print('you are on psycurveMode, extreme80pc')

                elif bdata['psycurveMode'][-1] == bdata.labels['psycurveMode']['uniform']:
                    print('you are on psycurveMode, uniform')
                    '''
                    if bdata['irrelevantFeatureMode'][-1] == bdata.labels['irrelevantFeatureMode']['random']:
                        print('irrelevantFeatureMode is random')
                    elif bdata['irrelevantFeatureMode'][-1] == bdata.labels['irrelevantFeatureMode']['fix_to_min']:
                        print('irrelevantFeatureMode is fix_to_min')
                    '''

                ### calculate psychometric###
                if any(bdata['psycurveMode']):
                    if bdata['soundType'][-1] == bdata.labels['soundType']['AM_depth']:
                        targetFrequency = bdata['targetAMdepth']
                    elif  bdata['soundType'][-1] == bdata.labels['soundType']['AM_rate']:
                        targetFrequency = bdata['targetAMrate']
                    elif  bdata['soundType'][-1] == bdata.labels['soundType']['chords']:
                        targetFrequency = bdata['targetFrequency']
                    elif  bdata['soundType'][-1] == bdata.labels['soundType']['tone_cloud']:
                        targetFrequency = bdata['targetCloudStrength']
                    elif  bdata['soundType'][-1] == bdata.labels['soundType']['FM_direction']:
                        targetFrequency = bdata['targetFMslope']


                    possibleFreq = np.unique(targetFrequency)
                    nFreq = len(possibleFreq)
                    trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)
                    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice,targetFrequency,valid)
                    fontsize = 12
                    if len(subject) > 1:
                        numSubPlots = 4
                    else:
                        numSubPlots = 1
                    subPlotInd = nSub + 1
                    fig1 = plt.subplot(3,numSubPlots,subPlotInd)
                    plt.title('{0} [{1}]'.format(subject[nSub],session))
                    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
                    plt.xlabel(bdata.labels['soundType'][bdata['soundType'][-1]],fontsize=fontsize)
                    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
                    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
                    plt.show()
