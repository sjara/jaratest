from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import extrafuncs
from jaratoolbox import extraplots
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import matplotlib.gridspec as gridspec


'''
Lan Guo 2015-11-11
This script updates test006 to plot time of individual trials as dot plot instead of running average for ITI. Plot choice and reaction time using per-block running average. Only plotting leftward and rightward choice trials, not distinguishing between correct and error trials.
'''


def plot_ITI_dynamics(bData, winsize=40, fontsize=12):
    '''
    Plot speed of performance (in intertrial intervals) in time for one session. Plots left- and right- rewardSide trials separately. 
    First argument is an object created by loadbehavior.BehaviorData (or subclasses)
    '''
    lineWidth = 2
    trialStarts = bData['timeTrialStart']
    interTrialIntervals = np.hstack((0,np.diff(trialStarts)))
    leftTrialIndex, = np.nonzero(bData['rewardSide']==bData.labels['rewardSide']['left'])
    #leftTrialIndex = bData['rewardSide'].index(bData.labels['rewardSide']['left'])
    plt.plot(interTrialIntervals, marker='.',linestyle='None',color='r')
    plt.plot(leftTrialIndex, interTrialIntervals[leftTrialIndex], marker='.',linestyle='None',color='g')
    
    '''
    leftTrialITIs=interTrialIntervals.copy()
    leftTrialITIs[~leftTrials]=0
    plt.plot(leftTrialITIs, marker='.',linestyle='None',color='g')
    
    rightTrialITIs = interTrialIntervals.copy() 
    rightTrialITIs[leftTrials]=0
    plt.plot(rightTrialITIs,marker='.',linestyle='None',color='r')
    #plt.hold(1)
    #(line1, line2) = plt.plot(range(0,len(leftTrials)), movAvITI_left, range(0,len(~leftTrials)), movAvITI_right)
    #plt.setp((line1,line2), color=('g','b'), linewidth=2.0)
    #plt.legend([line1, line2], ['Leftward trials', 'Rightward trials'])
    '''
    #plt.ylabel('Intertrial Interval(s)',fontsize=fontsize)
    plt.xlabel('Trial number',fontsize=fontsize)
    #plt.title('Intertrial Interval')
    plt.ylim(0,30)
    ax = plt.gca()
    ax.set_ylabel('Intertrial Interval(s)',fontsize=fontsize,labelpad=1)
    extraplots.set_ticks_fontsize(ax,fontsize)
    #plt.show()


def plot_choicetime_dynamics(bData, winsize=40, fontsize=12):
    '''
    This function plots a running average for the choice time based on trial outcomes or which side the animal actually choosed ('choice'). 
    *Invalid trials does not have choice time since timeSideIn is NaN.
    Choice time is defined as the time it took to get to the side ports to retrieve water from the time of leaving center port.
    '''
    lineWidth = 2

    choiceTime = bData['timeSideIn']-bData['timeCenterOut']
    correctTrials = bData['outcome']==bData.labels['outcome']['correct']
    errorTrials = bData['outcome']==bData.labels['outcome']['error']
#    invalidTrials = bData['outcome']==bData.labels['outcome']['invalid']
#Cannot use rewardSide here since some trials will be invalid and contain NaN 'timeSideIn'
    leftTrials = bData['choice']==bData.labels['choice']['left']
#Cannot use ~leftTrials for indexing since will include trials where choice is none and timeSideIn will be NaN
    rightTrials = bData['choice']==bData.labels['choice']['right']

    #choiceTCorrect = np.ma.masked_array(choiceTime[correctTrials])
    #movAvChoiceTime_correct = extrafuncs.moving_average_masked(choiceTCorrect, winsize)
    #choiceTError = np.ma.masked_array(choiceTime[errorTrials])
    #movAvChoiceTime_error = extrafuncs.moving_average_masked(choiceTError, winsize)
    bData.find_trials_each_block()
    trialsEachBlock = bData.blocks['trialsEachBlock']
    nBlocks = bData.blocks['nBlocks']
    choiceTLeft = np.ma.masked_array(choiceTime[leftTrials])
    choiceTRight = np.ma.masked_array(choiceTime[rightTrials])
    for block in range(nBlocks):
        choiceTimeThisBlock = choiceTime[trialsEachBlock[:,block]]
        leftTrialsThisBlock = leftTrials[trialsEachBlock[:,block]]
        rightTrialsThisBlock = rightTrials[trialsEachBlock[:,block]]
        choiceTLeftThisBlock = np.ma.masked_array(choiceTimeThisBlock[leftTrialsThisBlock])
        choiceTRightThisBlock = np.ma.masked_array(choiceTimeThisBlock[rightTrialsThisBlock])
        #choiceTLeftThisBlock = choiceTLeft[trialsEachBlock[:,block]]
        #choiceTRightThisBlock = choiceTRight[trialsEachBlock[:,block]]
        movAvChoiceTime_right = extrafuncs.moving_average_masked(choiceTRightThisBlock, winsize)
        movAvChoiceTime_left = extrafuncs.moving_average_masked(choiceTLeftThisBlock, winsize)
        #plt.plot(movAvChoiceTime_correct,lw=lineWidth,color='m',alpha=1)
        #plt.hold(1)
        #plt.plot(movAvChoiceTime_error,lw=lineWidth,color='b',alpha=1)
        xValues = range(block*150,block*150+len(movAvChoiceTime_left))
        plt.plot(xValues,movAvChoiceTime_left,lw=lineWidth,color='g')
        xValues = range(block*150,block*150+len(movAvChoiceTime_right))
        plt.plot(xValues,movAvChoiceTime_right,lw=lineWidth,color='r')
        #plt.hold(1)
        #plt.ylim([0,2.5])
        #plt.axhline(50,color='0.5',ls='--')
        #plt.ylabel('Choice time(s)',fontsize=fontsize)
    plt.xlabel('Trial number',fontsize=fontsize)
    ax = plt.gca()
    extraplots.set_ticks_fontsize(ax,fontsize)
    ax.set_ylabel('Choice time(s)',fontsize=fontsize,labelpad=1)
    #plt.draw()
    #plt.show()


def plot_reactiontime_dynamics(bData, winsize=40, fontsize=12):
    '''
    This function plots a running average for the reaction time based on trial outcomes or which side the animal actually choosed ('choice'). 
    *Invalid trials does not have choice time since timeSideIn is NaN.
    Reaction time is defined as the time it took from hearing sound stimulus to deciding to act (removing head from center port).
    '''
    lineWidth = 2
    reactionTime = bData['timeCenterOut']-bData['timeTarget']
    correctTrials = bData['outcome']==bData.labels['outcome']['correct']
    errorTrials = bData['outcome']==bData.labels['outcome']['error']
#    invalidTrials = bData['outcome']==bData.labels['outcome']['invalid']
#Cannot use rewardSide here since some trials will be invalid and contain NaN 'timeSideIn'
    leftTrials = bData['choice']==bData.labels['choice']['left']
#Cannot use ~leftTrials for indexing since will include trials where choice is none and timeSideIn will be NaN
    rightTrials = bData['choice']==bData.labels['choice']['right']
    
    bData.find_trials_each_block()
    trialsEachBlock = bData.blocks['trialsEachBlock']
    nBlocks = bData.blocks['nBlocks']

    #reactionTCorrect = np.ma.masked_array(reactionTime[correctTrials])
    #movAvReactionTime_correct = extrafuncs.moving_average_masked(reactionTCorrect, winsize)
    #reactionTError = np.ma.masked_array(reactionTime[errorTrials])
    #movAvReactionTime_error = extrafuncs.moving_average_masked(reactionTError, winsize)
    
    reactionTLeft = np.ma.masked_array(reactionTime[leftTrials])
    reactionTRight = np.ma.masked_array(reactionTime[rightTrials])

    for block in range(nBlocks):
        reactionTimeThisBlock = reactionTime[trialsEachBlock[:,block]]
        leftTrialsThisBlock = leftTrials[trialsEachBlock[:,block]]
        rightTrialsThisBlock = rightTrials[trialsEachBlock[:,block]]
        reactionTLeftThisBlock = np.ma.masked_array(reactionTimeThisBlock[leftTrialsThisBlock])
        reactionTRightThisBlock = np.ma.masked_array(reactionTimeThisBlock[rightTrialsThisBlock])
        movAvReactionTime_left = extrafuncs.moving_average_masked(reactionTLeftThisBlock, winsize)
        movAvReactionTime_right = extrafuncs.moving_average_masked(reactionTRightThisBlock, winsize)
   
        #line1,=plt.plot(movAvReactionTime_correct,lw=lineWidth,color='m',alpha=1,label='correct')
        #line2,=plt.plot(movAvReactionTime_error,lw=lineWidth,color='b',alpha=1,label='error')
        xValues = range(block*150,block*150+len(movAvReactionTime_left))
        line3,=plt.plot(xValues,movAvReactionTime_left,lw=lineWidth,color='g',label='left')
        xValues = range(block*150,block*150+len(movAvReactionTime_right))
        line4,=plt.plot(xValues,movAvReactionTime_right,lw=lineWidth,color='r',label='right')
       
        #plt.ylim([0,2.5])
        
    plt.xlabel('Trial number',fontsize=fontsize)
    plt.legend([line3,line4],['left','right'],loc=1)
    ax = plt.gca()
    ax.set_ylabel('Reaction time(s)',fontsize=fontsize,labelpad=1)
    extraplots.set_ticks_fontsize(ax,fontsize)
 


if len(sys.argv)>1:
    sessions = sys.argv[1:]

subjects = ['adap005', 'adap008']
EXPERIMENTER = 'santiago'
paradigm = '2afc'
loadingClass = loadbehavior.FlexCategBehaviorData
outputDir = '/home/languo/data/behavior_reports'
settings.BEHAVIOR_PATH = '/home/languo/data/mnt/jarahubdata'
nAnimals = len(subjects)    
nSessions = len(sessions)
gs = gridspec.GridSpec(nAnimals*nSessions, 6)
gs.update(hspace=0.2,wspace=0.7)

plt.figure()
for inda, subject in enumerate(subjects):
    for inds, thisSession in enumerate(sessions):
        try:
            behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,thisSession)
            bData = loadingClass(behavFile,readmode='full')
        except IOError:
            print thisSession+' does not exist'
            continue
        print 'Loaded %s %s'%(subject,thisSession)
        
        thisPlotPos = inda*nSessions+inds
        # -- Plot performance speed as intertrial intervals (left or right)--
        ax1=plt.subplot(gs[thisPlotPos,:-4])
        plot_ITI_dynamics(bData, winsize=20, fontsize=12)
        # -- Plot choice time based on trial outcome and actual choice--
        ax2=plt.subplot(gs[thisPlotPos,2:4])
        plot_choicetime_dynamics(bData, winsize=20, fontsize=12)
        # -- Plot reactopm time based on trial outcome and actual choice--
        ax3=plt.subplot(gs[thisPlotPos,-2:])
        plot_reactiontime_dynamics(bData, winsize=20, fontsize=12)
    plt.title('%s_%s'%(subject,thisSession))
        #plt.hold(1)
#plt.tight_layout()        
plt.show()

fig_path = outputDir
if not os.path.exists(fig_path):
    os.makedirs(fig_path)
sessionStr = '-'.join(sessions)
fig_name = '{}_{}_reaction_per_block.png'.format(subject, sessionStr)
full_fig_path = os.path.join(fig_path, fig_name)
plt.gcf().set_size_inches((10,11))
plt.gcf().savefig(full_fig_path)
#plt.close()

