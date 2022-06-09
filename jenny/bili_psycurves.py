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

if subject == 'bili034':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = ['20220308a', '20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a','20220315a', '20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a']  #uniform distribution
    #extremes 80pct: sessions = ['20220228a', '20220301a', '20220302a', '20220303a', '20220304a' ,'2020305a', '20220306a', '20220307a']
elif subject == 'bili035':
    sessions = ['20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a']
    #sessions = [ '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a'] #uniform
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a', '20220411a', '20220412a', '20220413a', '20220414a'] #Log spaced!
    #sessions = [ '20220317a','20220318a', '20220319a', '20220320a', '20220321a' ] #uniform distribution
    #sessions = [  '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #extremes 80pct
elif subject == 'bili036':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = [ '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] # uniform distribution   strange behavior, very biased: '20220307a', '20220304a'
    #sessions = ['20220305a', '20220306a',  '20220308a', '20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a','20220315a', '20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a'] # uniform distribution   strange behavior, very biased: '20220307a', '20220304a'
    #extremes 80pct:['20220213a', '20220214a', '20220215a', '20220216a', '20220217a', '20220218a', '20220219a', '20220220a', '20220221a', '20220222a', '20220223a', '20220224a', '20220225a', '20220226a', '20220227a', '20220228a', '20220301a', '20220303a', '20220304a' ] #bili036
elif subject == 'bili037':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = ['20220315a', '20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #uniform distribution
    #sessions = ['20220304a',  '20220307a', '20220308a', '20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a'] #biased: '20220306a','2020305a',
elif subject == 'bili038':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = [ '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #uniform
    #sessions = ['20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a','20220315a', '20220316a'] #very biased '20220306a'
elif subject == 'bili039':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = [ '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #uniform distribution
    #sessions = ['20220304a','2020305a', '20220306a', '20220307a', '20220308a', '20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a','20220315a','20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a'] #uniform distribution
    #sessions = ['20220221a', '20220222a', '20220223a', '20220224a', '20220225a', '20220226a', '20220227a', '20220301a', '20220303a', '20220304a'] #['20220221a', '20220222a', '20220223a', '20220224a', '20220225a', '20220226a', '20220227a', '20220228a', '20220301a']
elif subject == 'bili040':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = ['20220315a','20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #uniform distribution
    #sessions = ['20220303a', '20220304a','2020305a', '20220306a', '20220307a', '20220308a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a']
elif subject == 'bili041':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = ['20220306a', '20220307a', '20220308a', '20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a','20220315a','20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220321a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #uniform distribution
    #extremes 80 pct: sessions = ['20220225a', '20220226a', '20220227a', '20220228a', '20220301a', '20220302a','20220303a', '20220304a','2020305a'] #['20220209a', '20220210a', '20220212a', '20220214a', '20220215a', '20220216a', '20220220a', '20220221a', '2022022a', '20220225a', '20220226a', '20220227a', '20220228a', '20220301a', '20220302a'] #bili041
elif subject == 'bili042':
    sessions = ['20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #Irrelevant feature = random
    #sessions = ['20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a'] #Log spaced!
    #sessions = ['20220308a', '20220309a', '20220312a', '20220313a','20220315a','20220316a', '20220317a','20220318a', '20220319a', '20220320a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a'] #uniform distribution
    #sessions =  ['20220227a', '20220228a', '20220301a', '20220303a', '20220304a','2020305a', '20220306a', '20220307', '20220311a'] #'20220314a' very biased.#['20220221a', '20220222a', '20220224a', '20220227a', '20220228a', '20220301a']
elif subject == 'bili043':
    sessions = ['20220329a', '20220330a', '20220414a', '20220415a', '20220416a', '20220417a']
elif subject == 'bili044':
    sessions = ['20220504a', '20220505a', '20220506a', '20220507a', '20220508a', '20220509a', '20220510a', '20220512a', '20220513a', '20220514a', '20220515a', '20220516a', '20220517a', '20220518a'] #Irrelevant Feature = random , '20220513a', '20220511a',
    #sessions = ['20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a', '20220331a', '20220401a', '20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a', '20220411a', '20220412a', '20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a' ] #uniform
    #sessions = ['20220308a', '20220309a', '20220310a', '20220311a', '20220312a', '20220313a', '20220314a','20220315a','20220316a', '20220317a','20220318a', '20220320a', '20220321a','20220322a']
elif subject == 'bili045':
    sessions = ['20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a'] #extremes80pct
elif subject == 'bili046':
    sessions = [ '20220503a', '20220504a', '20220506a', '20220508a', '20220509a', '20220510a', '20220511a', '20220512a', '20220513a', '20220514a', '20220515a', '20220516a', '20220517a', '20220518a'] #extremes80pct '20220413a', '20220414a', '20220502a', '20220505a', '20220507a',
elif subject == 'bili047':
    sessions = ['20220504a', '20220505a', '20220506a', '20220507a', '20220508a', '20220509a', '20220510a', '20220511a', '20220512a', '20220513a', '20220514a', '20220515a', '20220516a', '20220517a', '20220518a'] #Irrelevant Feature = random
    #sessions = ['20220320a','20220321a', '20220322a', '20220322a','20220323a','20220324a', '20220325a', '20220326a','20220327a', '20220328a', '20220329a', '20220330a', '20220331a', '20220401a', '20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a', '20220411a', '20220412a', '20220413a' , '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a', '20220503a' ] #uniform
    #sessions = ['20220311a', '20220312a', '20220313a', '20220314a','20220315a','20220316a', '20220317a','20220318a', '20220319a']
elif subject == 'bili048':
    sessions = ['20220413a', '20220414a']
elif subject == 'bili049':
    sessions = ['20220413a', '20220414a', '20220415a', '20220416a', '20220417a', '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a' ]
elif subject == 'bili051':
    sessions = ['20220504a', '20220505a', '20220506a', '20220507a', '20220508a', '20220509a', '20220510a', '20220511a', '20220512a', '20220513a', '20220514a', '20220515a', '20220516a', '20220517a', '20220518a'] #Irrelevant Feature = random
    #sessions = ['20220415a', '20220416a', '2020417a' , '20220418a', '20220419a', '20220420a', '20220421a', '20220422', '20220423a', '20220424a', '20220425a', '20220426a', '20220427a', '20220428a', '20220429a', '20220430a', '20220501a', '20220502a', '20220503a'] #uniform
    #sessions = ['20220324a', '20220329a', '20220330a',  '20220331a', '20220401a', '20220402a', '20220403a', '20220404a', '20220405a', '20220406a', '20220407a', '20220408a', '20220409a', '20220410a', '20220411a', '20220412a', '20220413a' , '20220414a' ] # extreme80pc
else:
    print('subject doesnt have any psycurve sessions indicated')

paradigm = '2afc_speech'

plt.clf()
fontsize=12
bdata = behavioranalysis.load_many_sessions(subject, sessions, paradigm)

#get which feature is relevant


whichFeature = bdata.labels['relevantFeature'][bdata['relevantFeature'][-1]]
leftTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['left']
rightTrials = bdata['rewardSide'] == bdata.labels['rewardSide']['right']
leftChoice = bdata['choice'] == bdata.labels['choice']['left']
rightChoice = bdata['choice'] == bdata.labels['choice']['right']
noChoice = bdata['choice'] == bdata.labels['choice']['none']
valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])

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
