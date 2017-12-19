import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import ephyscore

# -- Behavior criteria -- #
sessiontype='behavior'
minBlockNum = 3
minTrialNumEndBlock = 50 # Last block has to have at least 50 valid trials to count as a block
performanceThreshold = 70 # Has to do over 70% correct overall
###########################

BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))


def ensure_behav_criteria_celldb(celldb, strict=True, sessiontype=sessiontype, minBlockNum=minBlockNum, minTrialNumEndBlock=minTrialNumEndBlock, performanceThreshold=performanceThreshold):
    '''
    Given a celldb, check all behavior sessions and return whether each cell meets behavior criteria based on the behavior session it is in.
    Returns a pandas series (single column) containing boolean values (True means cell meets behavior criteria).
    '''
    metBehavCriteria = pd.Series(np.repeat(0, len(celldb)), dtype=bool)
    
    for date in np.unique(celldb.date):
        cellsThisSession = celldb.query('date=="{}"'.format(date))
        firstCellThisSession = cellsThisSession.loc[0]
        cellObj = ephyscore.CellDataObj(firstCellThisSession)
        rcInd = cellObj.get_session_inds(sessiontype=sessiontype)
        bdata = cellObj.load_behavior_by_index(rcInd)

        currentBlock = bdata['currentBlock']
        blockChanges = len(np.flatnonzero(np.diff(currentBlock)))
        firstTrialsEachBlock = np.r_[0, 1+np.flatnonzero(np.diff(currentBlock))]
        blockTypeEachBlock = currentBlock[firstTrialsEachBlock]
        numOfMoreLeftBlocks = sum(blockTypeEachBlock == bdata.labels['currentBlock']['more_left'])
        numOfMoreRightBlocks = sum(blockTypeEachBlock == bdata.labels['currentBlock']['more_right'])
        totalBlockNum = blockChanges + 1
        numOfLeftOrRightMoreBlocks = numOfMoreLeftBlocks + numOfMoreRightBlocks
        nValid = bdata['nValid'][-1]
        validTrialsLastBlock = nValid - bdata['nValid'][firstTrialsEachBlock[-1]] 
        nRewarded = bdata['nRewarded'][-1]
        percentCorrect = nRewarded / float(nValid) * 100
        
        if not strict:
            if (totalBlockNum >= minBlockNum) & (percentCorrect >= performanceThreshold):
                metBehavCriteria.loc[cellsThisSession.index] = True
        elif strict:
            # -- Implementing more strict criteria -- #
            # Get rid of last blocks that were too short
            # Only take sessions that has three or more 'more_left' or 'more_right' blocks
            if validTrialsLastBlock < minTrialNumEndBlock:
                lastBlockType = blockTypeEachBlock[-1]
                if (lastBlockType == bdata.labels['currentBlock']['more_right']) | (lastBlockType == bdata.labels['currentBlock']['more_left']):
                    numOfLeftOrRightMoreBlocks -= 1

            if (numOfLeftOrRightMoreBlocks >= minBlockNum) & (percentCorrect >= performanceThreshold):
                metBehavCriteria.loc[cellsThisSession.index] = True
        
        return metBehavCriteria


