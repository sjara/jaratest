'''
Test function for plotting psy-curves of bili mice (speech categorization)
'''
import numpy as np
import sys
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars.
from jaratoolbox import settings
import matplotlib.gridspec as gridspec


print('enter subject name')
subject = input()

if subject == 'febe007':
    sessions = ['20220517a', '20220518a', '20220519a', '20220521a', '20220522a', '20220523a','20220524a'] #extremes80pct '20220516a',  '20220520a',
elif subject == 'febe008':
    sessions = ['20220517a', '2022018a', '20220519a', '20220520a', '20220521a', '20220522a', '20220523a','20220524a'] #uniform
    #sessions = ['20220503a', '20220504a', '20220505a', '20220506a', '20220507a', '20220508a', '20220509a', '20220510a', '20220511a', '20220512a', '20220513a', '20220514a', '20220515a', '20220516a'] #extremes80pct
elif subject == 'febe009':
    sessions = [ '20220520a', '20220521a', '20220522a', '20220523a','20220524a'] #uniform Biased:'20220517a', '2022018a', '20220519a',
        #sessions = ['20220503a', '20220504a', '20220505a', '20220506a', '20220507a', '20220508a', '20220509a', '20220510a', '20220511a', '20220512a', '20220513a', '20220514a', '20220515a', '20220516a'] #extremes80pct
elif subject == 'febe012':
    sessions = ['20220520a', '20220521a', '20220522a', '20220523a','20220524a'] #extremes80pct
else:
    print('subject doesnt have any psycurve sessions indicated')

paradigm = 'headfixed_speech'

plt.clf()
fontsize=12
bdata = behavioranalysis.load_many_sessions(subject, sessions, paradigm)

#get which feature is relevant

'''
whichFeature = bdata.labels['relevantFeature'][bdata['relevantFeature'][-1]]
leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
leftChoice = bdata['choice'] == bdata.labels['choice']['left']
rightChoice = bdata['choice'] == bdata.labels['choice']['right']
noChoice = bdata['choice'] == bdata.labels['choice']['none']
valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
'''

valid = bdata['choice'] != bdata.labels['choice']['none']
leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left'] & valid
rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right'] & valid
leftChoice = bdata['choice'] == bdata.labels['choice']['left']
rightChoice = bdata['choice'] == bdata.labels['choice']['right']
noChoice = bdata['choice'] == bdata.labels['choice']['none']
leftCorrect = leftTrials & leftChoice
leftError = leftTrials & rightChoice
leftInvalid = leftTrials & noChoice
rightCorrect = rightTrials & rightChoice
rightError = rightTrials & leftChoice
rightInvalid = rightTrials & noChoice
#rightPercentCorrect = round(sum(rightCorrect)/sum(rightTrials & valid)*100,2)
#leftPercentCorrect = round(sum(leftCorrect)/sum(leftTrials & valid)*100,2)
whichFeature = bdata.labels['relevantFeature'][bdata['relevantFeature'][-1]]

if whichFeature == 'spectral':
    targetFrequency = bdata['targetFTpercent']
    irrelevantFrequency = bdata['targetVOTpercent']
elif whichFeature == 'temporal':
    targetFrequency = bdata['targetVOTpercent']
    irrelevantFrequency = bdata['targetFTpercent']

if bdata['irrelevantFeatureMode'][-1] == bdata.labels['irrelevantFeatureMode']['random']:
    possibleTargetFreq = np.unique(targetFrequency)
    possibleIrrelevantFreq = np.unique(irrelevantFrequency)
    trialsEachCond = behavioranalysis.find_trials_each_type(irrelevantFrequency,  possibleIrrelevantFreq)
    numSubPlots = len(possibleIrrelevantFreq)
    #plt.clf()
    plt.figure(1)
    plt.suptitle(subject)
    for indIrrelevant, thisIrrelevant in enumerate(possibleIrrelevantFreq):
        valid = trialsEachCond[:, indIrrelevant]
        (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice, targetFrequency, valid)
        plt.subplot(2, 3, indIrrelevant+1)
        plt.title('{0}% irrelevant Feature'.format(possibleIrrelevantFreq[indIrrelevant]))
        (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
        plt.xlabel('{0} feature level (a.u.)'.format(whichFeature) ,fontsize=fontsize)
        plt.ylabel('Rightward trials (%)',fontsize=fontsize)
        extraplots.set_ticks_fontsize(plt.gca(),fontsize)


    # Psychometric Relevant feature, collapse irrelevant
    valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
    nFreq = len(possibleTargetFreq)
    trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency, possibleTargetFreq)
    (possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice, targetFrequency, valid)

    #fig1 = plt.subplot(3,numSubPlots,subPlotInd)
    plt.figure(2)
    plt.suptitle('{0} [{1}] - [{2}]'.format(subject, sessions[0],sessions[-1]))
    plt.subplot(1, 2, 1)
    plt.title('Relevant Feature')
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
    plt.xlabel('Relevant feature level (a.u.)', fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)

    # Psychometric Irelevant feature, collapse relevant
    nFreq = len(possibleIrrelevantFreq)
    trialsEachFreq = behavioranalysis.find_trials_each_type(irrelevantFrequency, possibleIrrelevantFreq)
    (possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice, irrelevantFrequency, valid)

    #fig1 = plt.subplot(3,numSubPlots,subPlotInd)
    plt.subplot(1, 2, 2)
    plt.title('Irrelevant Feature')
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
    plt.xlabel('irrelevant feature level (a.u.)', fontsize=fontsize)
    plt.ylabel('Rightward trials (%)', fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)


else:
    possibleFreq = np.unique(targetFrequency)
    nFreq = len(possibleFreq)
    trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency, possibleFreq)
    (possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice, targetFrequency, valid)

    #fig1 = plt.subplot(3,numSubPlots,subPlotInd)
    plt.title('{0} [{1}] - [{2}]'.format(subject,sessions[0],sessions[-1]))
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
    plt.xlabel('{0} feature level (a.u.)'.format(whichFeature) ,fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
plt.show()

#sys.exit()
