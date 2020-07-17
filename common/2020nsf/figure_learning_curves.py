"""
Plot learning curve for head-fixed animals.
(based on test078_learning_curve_headfixed.py)
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings 
#from importlib import reload


#subject = 'chad029'
#subjects = ['chad028','chad029','chad030','chad032']
subjects = ['chad028','chad029','chad030']

sessionsEachSubject = {
    'chad028': ['20200225a','20200227a','20200228a',
                '20200302a','20200303b','20200304a','20200305a','20200306a',
                '20200309a','20200310a','20200312a','20200313a','20200316a'],
    'chad029': ['20200221a','20200224a','20200225a','20200227a','20200228b',
                '20200302b','20200303a','20200304a','20200305a','20200306a',
                '20200309a','20200310a','20200312a','20200313a','20200316a'],
    'chad030': ['20200221a','20200224a','20200225a','20200227a','20200228b',
                '20200302b','20200303a','20200304a','20200305a','20200306a',
                '20200309a','20200310a','20200312a','20200313a','20200316a'],
    'chad032': ['20200221a','20200224a','20200225a','20200227a','20200228a',
                '20200302b','20200303a','20200304a','20200305a','20200306a',
                '20200309a','20200310a','20200312a','20200313a','20200316a']
    }

#,'20200311a' # Day with no sound (only LED)

fontSizeLabels = 12

fig0 = plt.gcf()
fig0.clf()
gs0 = gridspec.GridSpec(1,3, left=0.075, right=0.98, top=0.9, bottom=0.2, wspace=0.3)

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
    missedTrials = bdata['outcome']==bdata.labels['outcome']['miss']
    falseTrials = bdata['outcome']==bdata.labels['outcome']['falseAlarm']

    nSessions = len(sessions)   #bdata['sessionID'][-1]+!
    correctEachSession = np.empty(nSessions)
    validEachSession = np.empty(nSessions)
    taskModeEachSession = np.empty(nSessions)
    nTrialsEachSession = np.empty(nSessions)
    nStimsEachSession = np.empty(nSessions)
    missedEachSession = np.empty(nSessions)
    falseEachSession = np.empty(nSessions)
    
    for sessionID in range(nSessions):
        trialsThisSession = bdata['sessionID']==sessionID
        correctEachSession[sessionID] = np.sum(hitTrials[trialsThisSession])
        validEachSession[sessionID] = np.sum(validTrials[trialsThisSession])
        taskModeEachSession[sessionID] = bdata['taskMode'][trialsThisSession][-1]
        nTrialsEachSession[sessionID] = np.sum(trialsThisSession)
        missedEachSession[sessionID] = np.sum(missedTrials[trialsThisSession])
        falseEachSession[sessionID] = np.sum(falseTrials[trialsThisSession])

    nStimsEachSession = missedEachSession+validEachSession
    
    fractionCorrect = correctEachSession/validEachSession

    lickAfterStimID = bdata.labels['taskMode']['lick_after_sound']
    lickAfterStimSessions = np.flatnonzero(taskModeEachSession==lickAfterStimID)
    waterOnLickID = bdata.labels['taskMode']['water_on_lick']
    shapingSessions = np.flatnonzero((taskModeEachSession==lickAfterStimID) |
                                     (taskModeEachSession==waterOnLickID))
    
    #plt.subplot(2,2,indsub+1)
    markerSize = 6 #7
    ax0 = fig0.add_subplot(gs0[0,indsub])
    plt.plot(np.arange(1,len(fractionCorrect)+1), 100*fractionCorrect, 'o-', lw=2, mew=2, ms=markerSize)
    #plt.plot(lickAfterStimSessions+1,100*fractionCorrect[lickAfterStimSessions],
    #         'o-', lw=2, mew=2, ms=markerSize, mfc='w')
    plt.plot(shapingSessions+1,100*fractionCorrect[shapingSessions],
             'o-', lw=2, mew=2, ms=markerSize, mfc='w', color='C0')
    plt.ylim([-5,105])
    plt.xlim([-1,15])
    plt.xticks(np.arange(0,20,5))
    if indsub==0:
        plt.ylabel('Correct choices (%)', fontsize=fontSizeLabels)
    plt.xlabel('Day', fontsize=fontSizeLabels)
    plt.grid(True, color='0.9')
    sessionStr = '{} - {}'.format(sessions[0],sessions[-1])
    #plt.title(subject+'\n'+sessionStr, fontsize=fontSizeLabels, fontweight='normal')
    plt.title('Mouse {}'.format(indsub+1), fontsize=fontSizeLabels, fontweight='bold')

    '''
    ax1 = fig0.add_subplot(gs0[1,indsub])
    ax1.plot(falseEachSession/nTrialsEachSession, 'o-', lw=2, mew=2,
             color=[1,0.4,0.4], ms=markerSize)
    ax1.plot(missedEachSession/nStimsEachSession, 'o-', lw=2, mew=2,
             color='0.7', ms=markerSize)
    ax1.set_ylim([-0.05,1.05])
    ax1.set_xlim([-1,15])
    ax1.set_xticks(np.arange(0,20,5))
    ax1.set_ylabel('RED: FalseAlarms / Licks \n GRAY: Missed / Stims', fontsize=fontSizeLabels)
    #ax1.set_ylabel('nMissed/nStim (gray)\n nFalseAlarm/nLicks (red)', fontsize=fontSizeLabels)
    #ax1.set_xlabel('Session', fontsize=fontSizeLabels)
    ax1.grid(True, color='0.9')

    ax2 = fig0.add_subplot(gs0[2,indsub])
    ax2.plot(validEachSession, 'o-', lw=2, mew=2,
             color=[0.4,0.6,0.6], ms=markerSize)
    ax2.set_ylim([0,850])
    ax2.set_xlim([-1,15])
    ax2.set_xticks(np.arange(0,20,5))
    ax2.set_ylabel('N choices \n (correct + error)', fontsize=fontSizeLabels)
    ax2.set_xlabel('Session', fontsize=fontSizeLabels)
    ax2.grid(True, color='0.9')
    #plt.title(subject, fontsize=fontSizeLabels)
    '''
    
    '''
    ax1 = plt.twinx(ax0)
    ax1.set_zorder(zorder=3)
    ax1.plot(missedEachSession/nStimsEachSession, 'o-', lw=2, mew=2,
             color='0.9', ms=markerSize-2, zorder=2)
    '''
    
    plt.pause(0.01)
    plt.show()

    #print(nTrialsEachSession)
    #print(falseEachSession)
    #print(nStimsEachSession)
    #print(validEachSession)
    #print(missedEachSession)
    #print(100*missedEachSession/nStimsEachSession)
    #print('---')

    #break
    
if 1:
    filename = 'headfixed_learning_three_mice'
    extraplots.save_figure(filename, 'png', [8,2.5], '/tmp/', facecolor='w')
