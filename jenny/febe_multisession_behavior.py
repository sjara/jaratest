import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

print('Enter which subjects you want to look at: 1 = VOT, 2 = FT (original cohort only), 3 = FT animals + febe007, febe012, or enter a specific animal name')
#print('Enter the subject name')
whichSubject = input()
if whichSubject == '1': #VOT cohort
    subject = ['febe007', 'febe008', 'febe009', 'febe012'] #VOT animals
elif whichSubject == '2': #FT cohort
    subject = ['febe013', 'febe019', 'febe020', 'febe021'] #FT animals
elif whichSubject == '3':
    subject = ['febe007', 'febe012', 'febe013', 'febe019', 'febe020', 'febe021'] #FT cohort +VOT animals that switched to FT
else:
    subject = [whichSubject]

paradigm = 'headfixed_speech'

# Add the dates
sessions = []
print('input the date of the first session you want to look at (e.g. 20220115):')
firstSession = str(input())
#firstSession = str(20220111)
print('input the last date of the sessions you want to look at (e.g. 20220121):')
lastSession = str(input())
dates = pd.date_range(firstSession, lastSession)
dates = dates.strftime("%Y%m%d")
for nDates in range(len(dates)):
    sessions.append('{}a'.format(dates[nDates]))

#bdata = behavioranalysis.load_many_sessions(subject, sessions, paradigm)

fig2, ax2 = plt.subplots(figsize=(5,4),dpi=200)
plt.xlabel('Session Number')
plt.ylabel('Percent Correct')
#plt.title('All subjects in group')
plt.title('Group Performance')
for nSub in range(len(subject)): #np.unique(bdata['subjectID']):
    fig, ax = plt.subplots(figsize=(5,4),dpi=200)
    bdata = behavioranalysis.load_many_sessions(subject[nSub], sessions, paradigm)
    valid = bdata['choice'] != bdata.labels['choice']['none']
    leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left'] & valid
    rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right'] & valid
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

            '''
            ### Deal with psychometric###
            if any(bdata['psycurveMode'][sessionStart:sessionEnd]):
                if bdata['relevantFeature'][-1] == bdata.labels['relevantFeature']['spectral']:
                    targetFrequency = bdata['targetFTpercent'][sessionStart:sessionEnd]
                elif bdata['relevantFeature'][-1] == bdata.labels['relevantFeature']['temporal']:
                    targetFrequency = bdata['targetVOTpercent'][sessionStart:sessionEnd]

                valid=bdata['valid']& (choice!=bdata.labels['choice']['none'])
                possibleFreq = np.unique(targetFrequency)
                sessionRightChoice = rightChoice[sessionStart:sessionEnd]
                nFreq = len(possibleFreq)
                trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)
                (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(sessionRightChoice,targetFrequency,valid)
                (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,ciHitsEachValue,xTickPeriod=1)
                plt.xlabel('Frequency (kHz)',fontsize=fontsize)
                plt.ylabel('Rightward trials (%)',fontsize=fontsize)
                extraplots.set_ticks_fontsize(plt.gca(),fontsize)
                    #    return (pline, pcaps, pbars, pdots)
                '''





    plt.title(subject[nSub])
    numDays = np.arange(0,nSess+1,1)
    line1, = ax.plot(numDays, subjPerformance[:,0],'r', label = "Right Trials")
    line2, = ax.plot(numDays, subjPerformance[:,1],'b', label = "Left Trials")
    line3, = ax.plot(numDays, subjPerformance[:,2],'k', label = "All Trials")
    ax.plot([50] * len(numDays), '0.5' ,linestyle = '--')
    ax2.plot([50] * len(numDays), '0.5' ,linestyle = '--')
    ax.plot([70] * len(numDays), '0.7' ,linestyle = '--')
    ax2.plot([70] * len(numDays), '0.7' ,linestyle = '--')
    line4, = ax2.plot(numDays, subjPerformance[:,2])

    for nSess in np.unique(bdata['sessionID']):
        endInd = int(sessionLimits[nSess,1])
        if bdata['taskMode'][endInd] == bdata.labels['taskMode']['discriminate_stim']:
            if bdata['rewardSideMode'][endInd] == bdata.labels['rewardSideMode']['repeat_mistake']:
                ax.plot(numDays[nSess], subjPerformance[nSess,0],'ro', mfc = 'w' )
                ax.plot(numDays[nSess], subjPerformance[nSess,1], 'bo', mfc = 'w')
                dots1, = ax.plot(numDays[nSess], subjPerformance[nSess,2], 'ko', mfc ='w', label = "Antibiasmode ON")
                dots3, = ax2.plot(numDays[nSess], subjPerformance[nSess,2], 'ko', mfc ='w', label = "Antibiasmode ON")
            elif bdata['psycurveMode'][endInd] != bdata.labels['psycurveMode']['off']:
                ax.plot(numDays[nSess], subjPerformance[nSess,0],'r*', mfc ='r')
                ax.plot(numDays[nSess], subjPerformance[nSess,1], 'b*', mfc ='b')
                dots5, = ax.plot(numDays[nSess], subjPerformance[nSess,2], 'k*', mfc ='k', label = "Psycurve Mode")
                dots6, = ax2.plot(numDays[nSess], subjPerformance[nSess,2], 'k*', mfc ='k', label = "Psycurve Mode")
            else:
                ax.plot(numDays[nSess], subjPerformance[nSess,0],'ro', mfc ='r')
                ax.plot(numDays[nSess], subjPerformance[nSess,1], 'bo', mfc ='b')
                dots2, = ax.plot(numDays[nSess], subjPerformance[nSess,2], 'ko', mfc ='k', label = "Antibiasmode OFF")
                dots4, = ax2.plot(numDays[nSess], subjPerformance[nSess,2], 'ko', mfc ='k', label = "Antibiasmode OFF")


    plt.xlabel('Session Number')
    plt.ylabel('Percent Correct')

#    ax.legend([line1, line2])#,["rightTrials", "leftTrials"])
    if bdata['psycurveMode'][endInd] > 0:
        labels = ['Right Trials', 'Left Trials', 'All Trials', 'Antibiasmode ON', 'Antibiasmode OFF', 'Psycurve Mode']
        ax.legend([line1, line2, line3, dots1, dots2, dots5], labels, loc = 'upper left')
    else:
        labels = ['Right Trials', 'Left Trials', 'All Trials', 'Antibiasmode ON', 'Antibiasmode OFF']
        ax.legend([line1, line2, line3, dots1, dots2], labels, loc = 'upper left')
    #labels2 = ['Antibiasmode ON', 'Antibiasmode OFF']
    #ax2.legend([dots1, dots2, d], labels2, loc = 'upper left')
    plt.show()
#    input('press enter for next subject')
#    plt.close()
#plt.close()
