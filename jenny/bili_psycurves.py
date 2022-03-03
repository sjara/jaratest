'''
Test function for plotting psy-curves of bili mice (speech categorization)
'''

from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars.
from jaratoolbox import settings
import sys

print('enter subject name')
subject = input()

if subject == 'bili036':
    sessions = ['20220213a', '20220214a', '20220215a', '20220216a', '20220217a', '20220218a', '20220219a', '20220220a', '20220221a', '20220222a', '20220223a', '20220224a', '20220225a', '20220226a', '20220227a', '20220228a', '20220301a', '20220303a' ] #bili036
elif subject == 'bili041':
    sessions = ['20220225a', '20220226a', '20220227a', '20220228a', '20220301a', '20220302a'] #['20220209a', '20220210a', '20220212a', '20220214a', '20220215a', '20220216a', '20220220a', '20220221a', '2022022a', '20220225a', '20220226a', '20220227a', '20220228a', '20220301a', '20220302a'] #bili041
elif subject == 'bili042':
    sessions = ['20220227a', '20220228a', '20220301a'] #['20220221a', '20220222a', '20220224a', '20220227a', '20220228a', '20220301a']
elif subject == 'bili039':
    sessions = ['20220221a', '20220222a', '20220223a', '20220224a', '20220225a', '20220226a', '20220227a', '20220301a'] #['20220221a', '20220222a', '20220223a', '20220224a', '20220225a', '20220226a', '20220227a', '20220228a', '20220301a']
elif subject == 'bili034':
    sessions = ['20220228a', '20220301a', '20220302a', '20220303a'] #['20220227a', '20220228a', '20220301a', '20220302a', '20220303a']
elif subject == 'bili040':
    sessions = ['20220303a']
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
elif whichFeature == 'temporal':
    targetFrequency = bdata['targetVOTpercent']

possibleFreq = np.unique(targetFrequency)
nFreq = len(possibleFreq)
trialsEachFreq = behavioranalysis.find_trials_each_type(targetFrequency,possibleFreq)
(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(rightChoice,targetFrequency,valid)


#fig1 = plt.subplot(3,numSubPlots,subPlotInd)
plt.title('{0} [{1}] - [{2}]'.format(subject,sessions[0],sessions[-1]))
(pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue, ciHitsEachValue,xTickPeriod=1, xscale='linear')
plt.xlabel('{0} feature level (a.u.)'.format(whichFeature) ,fontsize=fontsize)
plt.ylabel('Rightward trials (%)',fontsize=fontsize)
extraplots.set_ticks_fontsize(plt.gca(),fontsize)
plt.show()

#sys.exit()
