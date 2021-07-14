"""
Show psychometric for head-fixed mice.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import behavioranalysis
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots
from jaratoolbox import settings 

#subject = 'test000'; sessions = ['20201231c']

#subject = 'chad056'
subjects = ['brin001']
sessions = ['20210426a']
sessions = ['20210427a','20210428a']
sessions = ['20210427a','20210428a','20210429a','20210430a',
            '20210501a','20210502a','20210503a','20210504a']
#sessions = ['20210427a','20210428a','20210429a','20210430a']
#sessions = ['20210511a']
#sessions = ['20210427a']

paradigm = 'twochoice'


fontSizeLabels = 12

for subject in subjects:
    fig0 = plt.gcf()
    fig0.clf()
    gs0 = gridspec.GridSpec(1,1, left=0.15, right=0.98, bottom=0.15, wspace=0.25)

    try:
        bdata = behavioranalysis.load_many_sessions(subject,paradigm='twochoice',sessions=sessions)
    except UnboundLocalError:
        continue
    
    nSessions = bdata['sessionID'][-1]

    hitTrials = bdata['outcome']==bdata.labels['outcome']['hit']
    #hitLabel = -1 # Before 2020-03-15 we had a bug that saved hits as 'none'
    #hitTrialsBugHack = bdata['outcome']==hitLabel
    #hitTrials = hitTrials | hitTrialsBugHack

    errorTrials = bdata['outcome']==bdata.labels['outcome']['error']
    validTrials = hitTrials|errorTrials
    missedTrials = bdata['outcome']==bdata.labels['outcome']['miss']

    rewardSideRight = bdata['rewardSide']==bdata.labels['rewardSide']['right']

    nSessions = len(sessions)   #bdata['sessionID'][-1]+!
    #correctEachSession = np.empty(nSessions)
    #validEachSession = np.empty(nSessions)

    #targetFrequency = bdata['targetFrequency'] # I used name 'frequency' initially
    targetCloudStrength = bdata['targetCloudStrength']
    choiceRight = (hitTrials & rewardSideRight) | (errorTrials & ~rewardSideRight)

    nMissed = np.sum(missedTrials)
    nValid = np.sum(validTrials)
    nStim = nMissed + nValid
    print('Stimuli: {}'.format(nStim))
    print('Choices: {} ({:0.1%})'.format(nValid, nValid/nStim))
    print('Misses: {} ({:0.1%})'.format(nMissed, nMissed/nStim))
    #print(''.format())

    # Use a different scale for stim strength
    if 0:
        targetCloudStrength = np.sign(targetCloudStrength)*(np.abs(targetCloudStrength)**2)

    (possibleValues, fractionHitsEachValue, ciHitsEachValue, nTrialsEachValue, nHitsEachValue)=\
        behavioranalysis.calculate_psychometric(choiceRight, targetCloudStrength, validTrials)


    #plt.subplot(1,3,indsub+1)
    plotColor = '#1f77b4'  #[0.2,0.2,1]
    ax0 = fig0.add_subplot(gs0[0,0])
    xTicks = np.arange(-100, 120, 40)
    (pline, pcaps, pbars, pdots) = \
        extraplots.plot_psychometric(possibleValues,fractionHitsEachValue,
                                     ciHitsEachValue, xTicks=xTicks, xscale='linear')
    plt.setp([pline, pcaps, pbars, pdots], color=plotColor)
    plt.setp(pdots,mfc=plotColor)
    plt.axhline(y=50, color='0.85', ls='--')
    #plt.minorticks_off()
    plt.ylim([-5,105])
    plt.ylabel('Licked right (%)', fontsize=fontSizeLabels)
    plt.xlabel('Stim coherence', fontsize=fontSizeLabels)
    sessionStr = '{} - {}'.format(sessions[0],sessions[-1])
    titleStr = f'{subject}: {sessionStr}'
    plt.title(titleStr, fontsize=fontSizeLabels, fontweight='bold')
    extraplots.boxoff(ax0)
    plt.pause(0.01)
    plt.show()
    #plt.waitforbuttonpress()
    #sys.exit()

if 0:
    format = 'png'
    filename = 'headfixed_{}_{}'.format(subject,sessions[0])
    extraplots.save_figure(filename, format, [6,5], '/tmp/', facecolor='w')

if 0:
    import pandas as pd
    import os
    behavFrame = pd.DataFrame({'choice':bdata['choice'],
                               'outcome':bdata['outcome'],
                               'targetCloudStrength':bdata['targetCloudStrength'],
                               'rewardSide':bdata['rewardSide']})
    filename = 'headfixed_{}_{}.pkl'.format(subject,sessions[0])
    outputPath = os.path.join('/tmp/',filename)
    behavFrame.to_pickle(outputPath)
    print(f'Saved pickled dataframe to {outputPath}')
