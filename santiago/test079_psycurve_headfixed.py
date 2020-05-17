"""
Plot learning curve for head-fixed animals.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings 
from importlib import reload



#subject = 'chad029'
subjects = ['chad028','chad029','chad030']

sessionsEachSubject = {
    'chad028': ['20200317a','20200318a','20200319a','20200320a'],
    'chad029': ['20200317a','20200318a','20200319a','20200320a'],
    'chad030': ['20200317a','20200318a','20200319a','20200320a']
}

if 1:
    sessionsEachSubject = {
        'chad028': ['20200318a','20200319a'],
        'chad029': ['20200317a','20200318a','20200319a','20200320a'],
        'chad030': ['20200317a','20200318a','20200320a']
    }

if 0:
    oneDay = '20200320a'
    sessionsEachSubject = {
        'chad028': [oneDay],
        'chad029': [oneDay],
        'chad030': [oneDay]
    }

#,'20200311a' # Day with no sound (only LED)


fontSizeLabels = 12

fig0 = plt.gcf()
fig0.clf()
gs0 = gridspec.GridSpec(1,3, left=0.075, right=0.98, bottom=0.15, wspace=0.25)

for indsub, subject in enumerate(subjects):

    sessions = sessionsEachSubject[subject]
    bdata = behavioranalysis.load_many_sessions(subject,paradigm='twochoice',sessions=sessions)

    nSessions = bdata['sessionID'][-1]

    hitTrials = bdata['outcome']==bdata.labels['outcome']['hit']
    hitLabel = -1 # Before 2020-03-15 we had a bug that saved hits as 'none'
    hitTrialsBugHack = bdata['outcome']==hitLabel
    hitTrials = hitTrials | hitTrialsBugHack

    errorTrials = bdata['outcome']==bdata.labels['outcome']['error']
    validTrials = hitTrials|errorTrials

    rewardSideRight = bdata['rewardSide']==bdata.labels['rewardSide']['right']
    
    nSessions = len(sessions)   #bdata['sessionID'][-1]+!
    correctEachSession = np.empty(nSessions)
    validEachSession = np.empty(nSessions)

    targetFrequency = bdata['targetFrequency'] # I used name 'frequency' initially
    choiceRight = (hitTrials & rewardSideRight) | (errorTrials & ~rewardSideRight)

    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
        behavioranalysis.calculate_psychometric(choiceRight,targetFrequency,validTrials)


    #plt.subplot(1,3,indsub+1)
    ax0 = fig0.add_subplot(gs0[0,indsub])
    xTicks = np.around(1e-3*possibleValues,1)
    (pline, pcaps, pbars, pdots) = \
        extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                     ciHitsEachValue, xTicks=xTicks)
    plt.minorticks_off()
    plt.ylim([-5,105])
    plt.ylabel('Licked right (%)', fontsize=fontSizeLabels)
    plt.xlabel('Frequency (kHz)', fontsize=fontSizeLabels)
    sessionStr = '{} - {}'.format(sessions[0],sessions[-1])
    plt.title(subject+'\n'+sessionStr, fontsize=fontSizeLabels, fontweight='normal')
    plt.pause(0.01)
    plt.show()
    #sys.exit()

if 1:
    filename = 'headfixed_psycurves_all_20200323'
    extraplots.save_figure(filename, 'png', [10,3.5], '/tmp/', facecolor='w')



