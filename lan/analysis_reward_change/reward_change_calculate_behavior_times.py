import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt

animalList = ['adap012', 'adap013', 'adap015', 'adap017', 'gosi001','gosi004', 'gosi008','gosi010']

outputDir = '/home/languo/data/ephys/reward_change_stats/reports/behav_times'

BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

plt.figure()
for inda, animal in enumerate(animalList):
    #celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldbPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    if 'level_0' in list(celldb):
        celldb.drop('level_0', inplace=True, axis=1)
    else:
        celldb = celldb.reset_index()
        celldb.drop('level_0', inplace=True, axis=1)
    
    reactionTimeLeftChoiceMoreLeftAll = np.array([])
    reactionTimeRightChoiceMoreLeftAll = np.array([])
    reactionTimeLeftChoiceMoreRightAll = np.array([])
    reactionTimeRightChoiceMoreRightAll = np.array([])

    responseTimeLeftChoiceMoreLeftAll = np.array([])
    responseTimeRightChoiceMoreLeftAll = np.array([])
    responseTimeLeftChoiceMoreRightAll = np.array([])
    responseTimeRightChoiceMoreRightAll = np.array([])

    for date in np.unique(celldb.date):
        cellsThisSession = celldb.query('date=="{}"'.format(date))
        rcInd = cellsThisSession['sessiontype'].iloc[0].index('behavior')
        rcBehavior = cellsThisSession['behavior'].iloc[0][rcInd]
        behavFile = os.path.join(BEHAVIOR_PATH,animal,rcBehavior)
        bdata = loadbehavior.FlexCategBehaviorData(behavFile, readmode='full')
        validTrials = bdata['valid'].astype(bool) & (bdata['choice']!=bdata.labels['choice']['none'])
        choiceRightTrials = bdata['choice'] == bdata.labels['choice']['right']
        choiceLeftTrials = bdata['choice'] == bdata.labels['choice']['left']
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        reactionTimeAll = bdata['timeSideIn'] - bdata['timeCenterOut'] 
        reactionTimeLeftChoiceMoreLeft = reactionTimeAll[choiceLeftTrials & trialsEachType[:,1]]
        reactionTimeLeftChoiceMoreRight = reactionTimeAll[choiceLeftTrials & trialsEachType[:,2]]
        reactionTimeRightChoiceMoreRight = reactionTimeAll[choiceRightTrials & trialsEachType[:,2]]
        reactionTimeRightChoiceMoreLeft = reactionTimeAll[choiceRightTrials & trialsEachType[:,1]]
        reactionTimeLeftChoiceMoreLeftAll = np.append(reactionTimeLeftChoiceMoreLeftAll,reactionTimeLeftChoiceMoreLeft) 
        reactionTimeRightChoiceMoreLeftAll = np.append(reactionTimeRightChoiceMoreLeftAll, reactionTimeRightChoiceMoreLeft)
        reactionTimeLeftChoiceMoreRightAll = np.append(reactionTimeLeftChoiceMoreRightAll, reactionTimeLeftChoiceMoreRight)
        reactionTimeRightChoiceMoreRightAll = np.append(reactionTimeRightChoiceMoreRightAll, reactionTimeRightChoiceMoreRight)
        
        responseTimeAll = bdata['timeCenterOut'] - bdata['timeTarget']
        responseTimeLeftChoiceMoreLeft = responseTimeAll[choiceLeftTrials & trialsEachType[:,1]]
        responseTimeLeftChoiceMoreRight = responseTimeAll[choiceLeftTrials & trialsEachType[:,2]]
        responseTimeRightChoiceMoreRight = responseTimeAll[choiceRightTrials & trialsEachType[:,2]]
        responseTimeRightChoiceMoreLeft = responseTimeAll[choiceRightTrials & trialsEachType[:,1]]
        responseTimeLeftChoiceMoreLeftAll = np.append(responseTimeLeftChoiceMoreLeftAll,responseTimeLeftChoiceMoreLeft) 
        responseTimeRightChoiceMoreLeftAll = np.append(responseTimeRightChoiceMoreLeftAll, responseTimeRightChoiceMoreLeft)
        responseTimeLeftChoiceMoreRightAll = np.append(responseTimeLeftChoiceMoreRightAll, responseTimeLeftChoiceMoreRight)
        responseTimeRightChoiceMoreRightAll = np.append(responseTimeRightChoiceMoreRightAll, responseTimeRightChoiceMoreRight)
        
    plt.clf()
    plt.subplot(211)
    plt.hist([reactionTimeLeftChoiceMoreLeftAll, reactionTimeLeftChoiceMoreRightAll, reactionTimeRightChoiceMoreLeftAll, reactionTimeRightChoiceMoreRightAll], 50, edgecolor='None', color=['k','darkgrey','magenta','r'], label=['go_left_more_left', 'go_left_more_right', 'go_right_more_left', 'go_right_more_right'], stacked=False)
    plt.xlim([0.15, 1.0])
    plt.title('Time from center-out to side-in')
    plt.subplot(212)
    plt.hist([responseTimeLeftChoiceMoreLeftAll, responseTimeLeftChoiceMoreRightAll, responseTimeRightChoiceMoreLeftAll, responseTimeRightChoiceMoreRightAll], 30, edgecolor='None', color=['k','darkgrey','magenta','r'], label=['go_left_more_left', 'go_left_more_right', 'go_right_more_left', 'go_right_more_right'], stacked=False)
    plt.title('Time from sound-onset to center-out')
    plt.xlim([0.1, 0.5])
    plt.legend()
    plt.suptitle(animal)
    #plt.show()
    figFullPath = os.path.join(outputDir, animal)
    plt.savefig(figFullPath,format='png')
