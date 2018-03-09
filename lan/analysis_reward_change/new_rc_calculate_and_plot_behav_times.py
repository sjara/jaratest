import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import ephyscore
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.stats.multicomp as mc

animalList = ['adap005','adap012', 'adap013', 'adap015', 'adap017', 'gosi001','gosi004', 'gosi008','gosi010','adap067','adap071']

#outputDir = '/home/languo/data/ephys/reward_change_stats/reports/behav_times'
outputDir = '/home/languo/data/reports/reward_change/behav_times'

BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

# reward_change_freq_discrim paradigm 'rewardAvailability' is set to 4 sec
rewardAvailability = 4
soundDuration = 0.098  #Due to a precision problem some trials were at 0.099999... ,not 0.1

dbFolder = os.path.join(settings.DATABASE_PATH, 'new_celldb')
figFormat = 'png'

celldbPath = os.path.join(dbFolder,'rc_database.h5')
celldb = pd.read_hdf(celldbPath, key='reward_change')

plt.figure()
for inda, animal in enumerate(animalList):
    #celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    cellThisAnimal = celldb.query("subject=='{}' and keepAfterDupTest==True".format(animal))
    
    reactionTimeLeftChoiceMoreLeftAll = np.array([])
    reactionTimeRightChoiceMoreLeftAll = np.array([])
    reactionTimeLeftChoiceMoreRightAll = np.array([])
    reactionTimeRightChoiceMoreRightAll = np.array([])

    responseTimeLeftChoiceMoreLeftAll = np.array([])
    responseTimeRightChoiceMoreLeftAll = np.array([])
    responseTimeLeftChoiceMoreRightAll = np.array([])
    responseTimeRightChoiceMoreRightAll = np.array([])

    for date in np.unique(cellThisAnimal.date):
        cellsThisSession = cellThisAnimal.query('date=="{}"'.format(date))
        oneCellThisSession = cellsThisSession.iloc[0]
        cellObj = ephyscore.Cell(oneCellThisSession)
        sessionType = 'behavior'
        sessionInd = cellObj.get_session_inds(sessionType)[0]
        bdata = cellObj.load_behavior_by_index(sessionInd, behavClass=loadbehavior.FlexCategBehaviorData)
   
        validTrials = bdata['valid'].astype(bool) & (bdata['choice']!=bdata.labels['choice']['none'])
        choiceRightTrials = bdata['choice'] == bdata.labels['choice']['right']
        choiceLeftTrials = bdata['choice'] == bdata.labels['choice']['left']
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        reactionTimeAll = bdata['timeSideIn'] - bdata['timeCenterOut'] 
        '''
        if np.any((reactionTimeAll > rewardAvailability) & validTrials):
            inds = np.flatnonzero((reactionTimeAll > rewardAvailability) & validTrials)
            print '{} session {}, found valid reaction time larger than the reward availability at trial(s):'.format(animal, date), inds        
        else:
        '''
        reactionTimeLeftChoiceMoreLeft = reactionTimeAll[choiceLeftTrials & trialsEachType[:,1]]
        
        reactionTimeLeftChoiceMoreRight = reactionTimeAll[choiceLeftTrials & trialsEachType[:,2]]
        #Z, pVal = stats.ranksums(reactionTimeLeftChoiceMoreLeft, reactionTimeLeftChoiceMoreRight)
        #print '{} {} going left, time from center to side port, more vs less reward (ranksums) p val: {}'.format(animal, date, pVal)
        reactionTimeRightChoiceMoreRight = reactionTimeAll[choiceRightTrials & trialsEachType[:,2]]
        reactionTimeRightChoiceMoreLeft = reactionTimeAll[choiceRightTrials & trialsEachType[:,1]]
        #Z, pVal = stats.ranksums(reactionTimeRightChoiceMoreLeft, reactionTimeRightChoiceMoreRight)
        #print '{} {} going right, time from center to side port, more vs less reward (ranksums) p val: {}'.format(animal, date, pVal)

        reactionTimeLeftChoiceMoreLeftAll = np.append(reactionTimeLeftChoiceMoreLeftAll,reactionTimeLeftChoiceMoreLeft) 
        reactionTimeRightChoiceMoreLeftAll = np.append(reactionTimeRightChoiceMoreLeftAll, reactionTimeRightChoiceMoreLeft)
        reactionTimeLeftChoiceMoreRightAll = np.append(reactionTimeLeftChoiceMoreRightAll, reactionTimeLeftChoiceMoreRight)
        reactionTimeRightChoiceMoreRightAll = np.append(reactionTimeRightChoiceMoreRightAll, reactionTimeRightChoiceMoreRight)

        responseTimeAll = bdata['timeCenterOut'] - bdata['timeTarget']
        '''
        if np.any((responseTimeAll < soundDuration) & validTrials):
            inds = np.flatnonzero((responseTimeAll < soundDuration) & validTrials)
            print '{} session {}, found valid response time shorter than the sound duration at trial(s):'.format(animal, date), inds
        else:
        '''
        responseTimeLeftChoiceMoreLeft = responseTimeAll[choiceLeftTrials & trialsEachType[:,1]]
        responseTimeLeftChoiceMoreRight = responseTimeAll[choiceLeftTrials & trialsEachType[:,2]]
        #Z, pVal = stats.ranksums(responseTimeLeftChoiceMoreLeft, responseTimeLeftChoiceMoreRight)
        #print '{} {} going left, time from sound to center exit, more vs less reward (ranksums) p val: {}'.format(animal, date, pVal)
        responseTimeRightChoiceMoreRight = responseTimeAll[choiceRightTrials & trialsEachType[:,2]]
        responseTimeRightChoiceMoreLeft = responseTimeAll[choiceRightTrials & trialsEachType[:,1]]
        #Z, pVal = stats.ranksums(responseTimeRightChoiceMoreLeft, responseTimeRightChoiceMoreRight)
        #print '{} {} going right, time from sound to center exit, more vs less reward (ranksums) p val: {}'.format(animal, date, pVal)
        responseTimeLeftChoiceMoreLeftAll = np.append(responseTimeLeftChoiceMoreLeftAll,responseTimeLeftChoiceMoreLeft) 
        responseTimeRightChoiceMoreLeftAll = np.append(responseTimeRightChoiceMoreLeftAll, responseTimeRightChoiceMoreLeft)
        responseTimeLeftChoiceMoreRightAll = np.append(responseTimeLeftChoiceMoreRightAll, responseTimeLeftChoiceMoreRight)
        responseTimeRightChoiceMoreRightAll = np.append(responseTimeRightChoiceMoreRightAll, responseTimeRightChoiceMoreRight)

    # -- histogram -- #
    plt.clf()
    plt.subplot(211)
    if np.any(reactionTimeLeftChoiceMoreLeftAll):
        plt.hist([reactionTimeLeftChoiceMoreLeftAll, reactionTimeLeftChoiceMoreRightAll, reactionTimeRightChoiceMoreLeftAll, reactionTimeRightChoiceMoreRightAll], 50, normed=1, edgecolor='None', color=['k','darkgrey','magenta','r'], label=['go_left_more_left', 'go_left_more_right', 'go_right_more_left', 'go_right_more_right'], stacked=False)
        plt.xlim([0.15, 1.0])
        plt.title('Time from center-out to side-in')
        plt.legend()
    else:
        plt.title('All sessions have dubious reaction times')
    plt.subplot(212)
    if np.any(responseTimeLeftChoiceMoreLeftAll):
        plt.hist([responseTimeLeftChoiceMoreLeftAll, responseTimeLeftChoiceMoreRightAll, responseTimeRightChoiceMoreLeftAll, responseTimeRightChoiceMoreRightAll], 30, normed=1, edgecolor='None', color=['k','darkgrey','magenta','r'], label=['go_left_more_left', 'go_left_more_right', 'go_right_more_left', 'go_right_more_right'], stacked=False)
        plt.title('Time from sound-onset to center-out')
        plt.xlim([0.1, 0.5])
        plt.legend()
    else:
        plt.title('All sessions have dubious reaction times')

    plt.suptitle(animal)
    #plt.show()
    figFullPath = os.path.join(outputDir, animal+'_density')
    plt.savefig(figFullPath,format='png')
    
    # -- violin plot -- #
    plt.clf()
    plt.subplot(211)
    if np.any(reactionTimeLeftChoiceMoreLeftAll):
        sns.violinplot(data=[reactionTimeLeftChoiceMoreLeftAll, reactionTimeLeftChoiceMoreRightAll, reactionTimeRightChoiceMoreLeftAll, reactionTimeRightChoiceMoreRightAll])
        # -- stats -- #
        f, pVal = stats.kruskal(reactionTimeLeftChoiceMoreLeftAll, reactionTimeLeftChoiceMoreRightAll, reactionTimeRightChoiceMoreLeftAll, reactionTimeRightChoiceMoreRightAll)
        plt.text(0, 0.5, 'Kruskal-Wallis H-test p value {:.3f} between groups'.format(pVal)) 
        #plt.xticks([0,1,2,3],['LeftChoiceMoreLeft', 'LeftChoiceMoreRight', 'RightChoiceMoreLeft', 'RightChoiceMoreRight'])
        plt.xticks([])
        plt.ylim([0,1])
        plt.title('Time from center-out to side-in')
    else:
        plt.title('All sessions have dubious reaction times')
    plt.subplot(212)
    if np.any(responseTimeLeftChoiceMoreLeftAll):
        sns.violinplot(data=[responseTimeLeftChoiceMoreLeftAll, responseTimeLeftChoiceMoreRightAll, responseTimeRightChoiceMoreLeftAll, responseTimeRightChoiceMoreRightAll])
        # -- stats -- #
        f, pVal = stats.kruskal(responseTimeLeftChoiceMoreLeftAll, responseTimeLeftChoiceMoreRightAll, responseTimeRightChoiceMoreLeftAll, responseTimeRightChoiceMoreRightAll)
        plt.text(0, 0.25, 'Kruskal-Wallis H-test p value {:.3f} between groups'.format(pVal)) 
        plt.title('Time from sound-onset to center-out')
        plt.ylim([0, 0.5])
    else:
        plt.title('All sessions have dubious reaction times')
    plt.xticks([0,1,2,3],['LeftChoiceMoreLeft', 'LeftChoiceMoreRight', 'RightChoiceMoreLeft', 'RightChoiceMoreRight'])
    plt.suptitle(animal+'_violinplot')
    #plt.show()
    figFullPath = os.path.join(outputDir, animal+'_violinplot')
    plt.savefig(figFullPath,format='png')

    
    
