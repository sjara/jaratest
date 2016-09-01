from jaratoolbox.behavioranalysis import load_many_sessions
from statsmodels.stats.proportion import proportion_confint #Used to compute confidence interval for the error bars. 
from scipy.stats import fisher_exact
import numpy as np
from pylab import *

animalNames = 'hm4d004'
preSessions = ['20140826a']
postSessions =['20140825a']
preInds = range(len(preSessions))
postInds = range(len(preSessions), len(postSessions)+len(preSessions))
sessions = preSessions+postSessions
data = load_many_sessions(animalNames, sessions)
validTrials = data['valid']==1

validEachSession=[]
rewardedEachSession=[]
for session in np.unique(data['sessionID']):
    indsThisSession = data['sessionID']==session
    nValidThisSession = max(data['nValid'][indsThisSession])
    nRewardedThisSession = max(data['nRewarded'][indsThisSession])
    validEachSession.append(nValidThisSession)
    rewardedEachSession.append(nRewardedThisSession)
    
validEachSession = np.array(validEachSession)
rewardedEachSession = np.array(rewardedEachSession)

validEachPre = validEachSession[preInds]
validEachPost = validEachSession[postInds]
rewardedEachPre = rewardedEachSession[preInds]
rewardedEachPost = rewardedEachSession[postInds]

numValidPre = np.sum(validEachPre)
numValidPost = np.sum(validEachPost)
numRewardedPre = np.sum(rewardedEachPre)
numRewardedPost = np.sum(rewardedEachPost)

percentCorrectPre = numRewardedPre/float(numValidPre) *100
percentCorrectPost = numRewardedPost/float(numValidPost) * 100

confintPre = np.array(proportion_confint(numRewardedPre, numValidPre))*100
confintPost = np.array(proportion_confint(numRewardedPost, numValidPost))*100

whiskerlengthsPre = [percentCorrectPre - confintPre[0], confintPre[1] - percentCorrectPre]

whiskerLengthsPost = [percentCorrectPost-confintPost[0], confintPost[1]-percentCorrectPost]

x = [1, 1.4]
width = 0.2
bar(x, [percentCorrectPre, percentCorrectPost], width, yerr = [whiskerlengthsPre , whiskerLengthsPost], ecolor = 'k')

xlim([0.8, 1.8])


###############Calculate stats####################

numWrongPre = numValidPre - numRewardedPre
numWrongPost = numValidPost - numRewardedPost

ctable = [[numRewardedPre, numWrongPre], [numRewardedPost, numWrongPost]]

oddsRatio, pVal = fisher_exact(ctable)
title("p-value = {}".format(pVal))
ylim([0, 100])

show()
