from jaratoolbox.test.nick import striatumMuscimolSessions as ms
import numpy as np
from jaratoolbox import beahvioranalysis
from collections import Counter

from __future__ import print_function
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas

#Adap022 saline sessions
subject = ms.subjects[2]
salineSessions = ms.salineSessions[subject]
musSessions = ms.muscimolSessions[subject]

bdataSaline = behavioranalysis.load_many_sessions(subject, salineSessions)
bdataMus = behavioranalysis.load_many_sessions(subject, musSessions)

def choice_after_right_reward(bdata):

    #Trials where the animal went right
    choiceRight = bdata['choice']==bdata.labels['choice']['right']

    #Valid trials
    valid = bdata['valid']

    #Rewarded trials
    reward = bdata['outcome']==bdata.labels['outcome']['correct']
    validReward = (reward & valid)

    #Valid trials where the animal went to the right and was rewarded
    rightReward = (choiceRight & validReward)

    #The inds of these trials
    rightRewardInds = np.flatnonzero(rightReward)

    #The trial after
    trialAfterRightRewardInds = rightRewardInds + 1

    #Inds of all valid trials
    validInds = np.flatnonzero(valid)

    #Boolean of whether the trials after are valid or not
    validTrialAfterRightReward = np.in1d(trialAfterRightRewardInds, validInds)

    #Select only the inds of the trials after that are valid
    validTrialAfterRightRewardInds = trialAfterRightRewardInds[validTrialAfterRightReward]

    #Get the choices on these trials
    choiceAfterRightReward = bdata['choice'][validTrialAfterRightRewardInds]

    #Make into a list of string labels for easy interpretation
    choiceLabels = [bdata.labels['choice'][x] for x in choiceAfterRightReward]

    #Count them and return the counter
    count = Counter(choiceLabels)
    return count

from scipy import stats


table = [[340, 67], [492, 102]]
s = stats.fisher_exact(table)





#1=r, 0=l
# choice = np.array([0, 1, 0, 1, 1, 0, 0, 0, 1, 1])
# reward = np.array([1, 1, 0, 0, 1, 0, 0, 1, 0, 1])


def R(choice, rewarded, nBack):

    ##Remember to drop the initial trials in the choice array if doing nBack
    #+1 if trial was rewarded and right
    #-1 if rewarded and left
    #0 if unrewarded

    #If nBack is 1, then the last entry in the result array will be meaningless and the First entry in the
    #choice array should be dropped when doing the comparison

    rightReward = np.flatnonzero((choice & reward))
    leftReward = np.flatnonzero((np.logical_not(choice) & reward))
    unrewarded = np.flatnonzero(np.logical_not(reward))

    result = zeros(len(reward))

    result[rightReward]=1
    result[leftReward]=-1
    result[unrewarded]=0

    nBackResult = np.roll(result, nBack)

    return nBackResult



def N(choice, rewarded, nBack):

    ##Remember to drop the initial trials in the choice array if doing nBack
    #+1 if unrewarded and right
    #-1 if unrewarded and left
    #0 if rewarded

    unrewarded = np.logical_not(reward)
    rightUnrewarded = np.flatnonzero((choice & unrewarded))
    leftUnrewarded = np.flatnonzero((np.logical_not(choice) & unrewarded))
    rewarded = np.flatnonzero(reward)

    result = zeros(len(reward))

    result[rightUnrewarded]=1
    result[leftUnrewarded]=-1
    result[rewarded]=0

    nBackResult = np.roll(result, nBack)

    return nBackResult

for indSubject, subjectName in enumerate(ms.subjects):

    subject = ms.subjects[indSubject]
    salineSessions = ms.salineSessions[subject]
    musSessions = ms.muscimolSessions[subject]

    bdataSaline = behavioranalysis.load_many_sessions(subject, salineSessions)
    bdataMus = behavioranalysis.load_many_sessions(subject, musSessions)

    for injection in range(2):

        if injection==0:
            bdata = bdataSaline
        elif injection==1:
            bdata = bdataMus

        subplot2grid((2, len(ms.subjects)), (injection, indSubject))

        bdata.remove_trials(np.flatnonzero(np.logical_not(bdata['valid'])))
        bdata.remove_trials(np.flatnonzero(bdata['choice']==2))


        choice = bdata['choice']
        alternate = np.roll(np.logical_not(choice), 1).astype(int)
        reward = bdata['outcome']==bdata.labels['outcome']['correct']
        targetFreq = bdata['targetFrequency']

        d = {'choice': choice,
            'reward': reward,
            'R1': R(choice,reward,1),
            'N1': N(choice, reward, 1),
            'R2': R(choice,reward,2),
            'N2': N(choice, reward, 2),
            'R3': R(choice,reward,3),
            'N3': N(choice, reward, 3),
            'R4': R(choice,reward,4),
            'N4': N(choice, reward, 4),
            'freq': targetFreq
            }
        df = pandas.DataFrame(d)

        #Drop the initial trials that don't have the right nback information (Its rolled so it is actually wrong info)
        df2 = df.ix[4:]

        # formula = 'choice ~ R1 + N1'
        formula = 'choice ~ R1 + R2 + R3 + R4 + N1 + N2 + N3 + N4 + freq + freq:R1'

        model = smf.glm(formula=formula, data=df2, family=sm.families.Binomial()).fit()

        print(model.summary())

        rParams = model.params[1:5]
        nParams = model.params[5:9]

        x = range(4)

        # figure()
        # clf()
        plot(rParams[::-1], 'g-o')
        hold(1)
        plot(nParams[::-1], 'r-o')
        axhline(y=0, color='k')
        xlim([-0.5, 3.5])
        if injection==0:
            injectionName='saline'
        elif injection==1:
            injectionName='mus'
        title('{}, {}'.format(subjectName, injectionName))


