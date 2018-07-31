import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
import figparams

STUDY_NAME = figparams.STUDY_NAME
FIGNAME = 'reward_change_behavior_times'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)

animalList = np.unique(celldb.subject)

BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

# reward_change_freq_discrim paradigm 'rewardAvailability' is set to 4 sec
rewardAvailability = 4
soundDuration = 0.098  #Due to a precision problem some trials were at 0.099999... ,not 0.1

resultsDict = {}

for inda, animal in enumerate(animalList):
    #celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldbThisAnimal = celldb.query('subject=="{}"'.format(animal))
    reactionTimeLeftChoiceMoreLeftAll = np.array([])
    reactionTimeRightChoiceMoreLeftAll = np.array([])
    reactionTimeLeftChoiceMoreRightAll = np.array([])
    reactionTimeRightChoiceMoreRightAll = np.array([])

    responseTimeLeftChoiceMoreLeftAll = np.array([])
    responseTimeRightChoiceMoreLeftAll = np.array([])
    responseTimeLeftChoiceMoreRightAll = np.array([])
    responseTimeRightChoiceMoreRightAll = np.array([])

    for date in np.unique(celldbThisAnimal.date):
        firstCell = celldbThisAnimal.query('date=="{}"'.format(date)).iloc[0]
        cellObj = ephyscore.Cell(firstCell)
        rcInd = firstCell['sessionType'].index('behavior')
        bdata = cellObj.load_behavior_by_index(rcInd)

        validTrials = bdata['valid'].astype(bool) & (bdata['choice']!=bdata.labels['choice']['none'])
        choiceRightTrials = bdata['choice'] == bdata.labels['choice']['right']
        choiceLeftTrials = bdata['choice'] == bdata.labels['choice']['left']
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        
        reactionTimeAll = bdata['timeSideIn'] - bdata['timeCenterOut'] 
        if np.any(reactionTimeAll[validTrials] > rewardAvailability):
            inds = np.flatnonzero(reactionTimeAll[validTrials] > rewardAvailability)
            print '{} session {}, found valid reaction time larger than the reward availability at trial(s):'.format(animal, date), inds
        else:
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
        
        responseTimeAll = bdata['timeCenterOut'] - bdata['timeTarget'] - soundDuration
        if np.any(responseTimeAll[validTrials] < 0):
            inds = np.flatnonzero(responseTimeAll[validTrials] < 0) 
            print '{} session {}, found valid response time shorter than the sound duration at trial(s):'.format(animal, date), inds
        else:
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
        
    resultsDict.update({animal+'_reactionTimeLeftChoiceMoreLeft': reactionTimeLeftChoiceMoreLeftAll,
        animal+'_reactionTimeLeftChoiceMoreRight': reactionTimeLeftChoiceMoreRightAll,
        animal+'_reactionTimeRightChoiceMoreLeft': reactionTimeRightChoiceMoreLeftAll,
        animal+'_reactionTimeRightChoiceMoreRight': reactionTimeRightChoiceMoreRightAll,
        animal+'_responseTimeLeftChoiceMoreLeft': responseTimeLeftChoiceMoreLeftAll,
        animal+'_responseTimeRightChoiceMoreLeft': responseTimeRightChoiceMoreLeftAll,
        animal+'_responseTimeLeftChoiceMoreRight': responseTimeLeftChoiceMoreRightAll,
        animal+'_responseTimeRightChoiceMoreRight': responseTimeRightChoiceMoreRightAll
        })

outputFile = 'rc_behavior_reaction_and_response_times.npz'
outputFilePath = os.path.join(dataDir, outputFile)
np.savez(outputFilePath, **resultsDict)