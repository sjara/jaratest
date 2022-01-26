import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

print('Enter which subjects you want to look at: 1 = VOT, 2 = FT, 3 = all, 4 = AM cohort, 5 = PM cohort or enter a specific animal name')
#print('Enter the subject name')
whichSubject = input()
if whichSubject == '1': #VOT cohort
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042'] #VOT animals
elif whichSubject == '2': #FT cohort
    subject = ['bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051'] #FT animals
elif whichSubject == '3': #all
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili039', 'bili040', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047', 'bili048', 'bili049', 'bili050', 'bili051']
elif whichSubject == '4': #AM cohort
    subject = ['bili034', 'bili035', 'bili036', 'bili037', 'bili038', 'bili048', 'bili049', 'bili050', 'bili051']
elif whichSubject == '5': #PM cohort
    subject = ['bili039', 'bili040', 'bili041', 'bili042', 'bili043', 'bili044', 'bili045', 'bili046', 'bili047']
else:
    subject = [whichSubject]

paradigm = '2afc_speech'

# Add the dates
sessions = []
print('input the date of the first session you want to look at (e.g. 20220115):')
firstSession = int(input())
print('input the last date of the sessions you want to look at (e.g. 20220121):')
lastSession = int(input())
dates = np.arange(firstSession,lastSession+1,1)
for nDates in range(len(dates)):
    sessions.append('{}a'.format(dates[nDates]))




for nSub in range(len(subject)): #np.unique(bdata['subjectID']):
    bdata = behavioranalysis.load_many_sessions(subject[nSub], sessions, paradigm)
    leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
    rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
    leftChoice = bdata['choice'] == bdata.labels['choice']['left']
    rightChoice = bdata['choice'] == bdata.labels['choice']['right']
    noChoice = bdata['choice'] == bdata.labels['choice']['none']

    sessionStart = 0
    subjPerformance = np.zeros((len(sessions),3))
    sessionLimits = np.zeros((len(sessions),2))
    for nSess in np.unique(bdata['sessionID']):
        #check if file exists, if it doesn't, set all performance = 0
        behavFile = loadbehavior.path_to_behavior_data(subject[nSub], paradigm, sessions[nSess])
        try:
            loadbehavior.BehaviorData(behavFile)
        except IOError:
            sessionLimits[nSess,:] = [0, 0]
            subjPerformance[nSess,:] = [0, 0, 0]
            endInd = int(sessionLimits[nSess,1])

        sessionEnd = sessionStart + sum(bdata['sessionID'] == nSess) - 1
        #if session is empty (zero trials) then set everything to 0
        if sessionEnd - sessionStart == 0:
            sessionLimits[nSess,:] = [sessionStart, sessionEnd]
            subjPerformance[nSess,:] = [0, 0, 0]
            plt.plot(sessions[nSess], subjPerformance[nSess,0],'ro', mfc ='r')
            plt.plot(sessions[nSess], subjPerformance[nSess,1], 'bo', mfc ='b')
            plt.plot(sessions[nSess], subjPerformance[nSess,2], 'ko', mfc ='k')
        #otherwise, calculate percent correct for Left, right and all trials
        else:
            leftCorrect = leftTrials[sessionStart:sessionEnd] & leftChoice[sessionStart:sessionEnd]
            leftError = leftTrials[sessionStart:sessionEnd] & rightChoice[sessionStart:sessionEnd]
            leftInvalid = leftTrials[sessionStart:sessionEnd] & noChoice[sessionStart:sessionEnd]
            rightCorrect = rightTrials[sessionStart:sessionEnd] & rightChoice[sessionStart:sessionEnd]
            rightError = rightTrials[sessionStart:sessionEnd] & leftChoice[sessionStart:sessionEnd]
            rightInvalid = rightTrials[sessionStart:sessionEnd] & noChoice[sessionStart:sessionEnd]
            rightPercentCorrect = round(sum(rightCorrect)/sum(rightTrials[sessionStart:sessionEnd])*100,2)
            leftPercentCorrect = round(sum(leftCorrect)/sum(leftTrials[sessionStart:sessionEnd])*100,2)
            totalPercentCorrect = round((sum(leftCorrect)+sum(rightCorrect))/(sum(leftTrials[sessionStart:sessionEnd]) + sum(rightTrials[sessionStart:sessionEnd]))*100,2)
            subjPerformance[nSess,:] = [rightPercentCorrect, leftPercentCorrect, totalPercentCorrect]
            sessionLimits[nSess,:] = [sessionStart, sessionEnd]
            sessionStart = sessionEnd + 1


    plt.title(subject[nSub])
    plt.plot(sessions, subjPerformance[:,0],'r')
    plt.plot(sessions, subjPerformance[:,1],'b')
    plt.plot(sessions, subjPerformance[:,2],'k')
    plt.show()
    for nSess in np.unique(bdata['sessionID']):
        endInd = int(sessionLimits[nSess,1])
        if bdata['outcomeMode'][endInd] == bdata.labels['outcomeMode']['only_if_correct']:
            if bdata['antibiasMode'][endInd] == bdata.labels['antibiasMode']['repeat_mistake']:
                plt.plot(sessions[nSess], subjPerformance[nSess,0],'ro', mfc = 'w' )
                plt.plot(sessions[nSess], subjPerformance[nSess,1], 'bo', mfc = 'w')
                plt.plot(sessions[nSess], subjPerformance[nSess,2], 'ko', mfc ='w')
            else:
                plt.plot(sessions[nSess], subjPerformance[nSess,0],'ro', mfc ='r')
                plt.plot(sessions[nSess], subjPerformance[nSess,1], 'bo', mfc ='b')
                plt.plot(sessions[nSess], subjPerformance[nSess,2], 'ko', mfc ='k')

    input('press enter for next subject')
    plt.close()
plt.close()





## Multiple subjects, single day
'''
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
'''
