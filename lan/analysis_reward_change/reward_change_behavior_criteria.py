import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior

animalList = ['adap071', 'adap067'] #['adap005','adap012', 'adap013', 'adap015', 'adap017', 'gosi001','gosi004', 'gosi008','gosi010']

# -- Behavior criteria -- #
minBlockNum = 3
performanceThreshold = 70 # Has to do over 70% correct
###########################

BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))


for animal in animalList:
    #celldbPath = os.path.join(settings.DATABASE_PATH,'reward_change_{}.h5'.format(label))
    celldbPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    if 'level_0' in list(celldb):
        celldb.drop('level_0', inplace=True, axis=1)
    else:
        celldb = celldb.reset_index()
        celldb.drop('level_0', inplace=True, axis=1)
    
    celldb['met_behav_criteria'] = False
    
    for date in np.unique(celldb.date):
        cellsThisSession = celldb.query('date=="{}"'.format(date))
        rcInd = cellsThisSession['sessiontype'].iloc[0].index('behavior')
        rcBehavior = cellsThisSession['behavior'].iloc[0][rcInd]
        behavFile = os.path.join(BEHAVIOR_PATH,animal,rcBehavior)
        bdata = loadbehavior.FlexCategBehaviorData(behavFile, readmode='full')
        currentBlock = bdata['currentBlock']
        blockChanges = len(np.flatnonzero(np.diff(currentBlock)))
        blockNum = blockChanges + 1
        nValid = bdata['nValid'][-1]
        nRewarded = bdata['nRewarded'][-1]
        percentCorrect = nRewarded / float(nValid) * 100
        if (blockNum >= minBlockNum) & (percentCorrect >= performanceThreshold):
            celldb['met_behav_criteria'].loc[cellsThisSession.index] = True
        
    celldb.to_hdf(celldbPath, key='reward_change')        
