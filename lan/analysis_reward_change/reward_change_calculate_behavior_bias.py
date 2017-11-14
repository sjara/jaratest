import os
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

animalList = ['adap012', 'adap013', 'adap015', 'adap017', 'gosi001','gosi004', 'gosi008','gosi010']

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
    allRightwardBias = []
    for date in np.unique(celldb.date):
        cellsThisSession = celldb.query('date=="{}"'.format(date))
        rcInd = cellsThisSession['sessiontype'].iloc[0].index('behavior')
        rcBehavior = cellsThisSession['behavior'].iloc[0][rcInd]
        behavFile = os.path.join(BEHAVIOR_PATH,animal,rcBehavior)
        bdata = loadbehavior.FlexCategBehaviorData(behavFile, readmode='full')
        possibleFreqs = np.unique(bdata['targetFrequency'])
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        rightwardBiasByReward = [] #np.zeros(len(possibleFreqs))
        for indf, freq in enumerate(possibleFreqs):
            oneFreqTrials = (bdata['targetFrequency'] == freq) & bdata['valid'].astype('bool') & (bdata['choice'] != bdata.labels['choice']['none'])
            trialsMoreRightReward =  trialsEachType[:,2] & oneFreqTrials
            trialsMoreLeftReward =  trialsEachType[:,1] & oneFreqTrials
            if sum(trialsMoreRightReward) != 0:
                percentRightChoiceMoreRightReward = sum(bdata['choice'][trialsMoreRightReward] == bdata.labels['choice']['right']) / float(sum(trialsMoreRightReward)) * 100
            else:
                percentRightChoiceMoreRightReward = 0
            if sum(trialsMoreLeftReward) != 0:
                percentRightChoiceMoreLeftReward = sum(bdata['choice'][trialsMoreLeftReward] == bdata.labels['choice']['right']) / float(sum(trialsMoreLeftReward)) * 100
            else:
                percentRightChoiceMoreLeftReward = 0
            rightwardBiasThisFreq = percentRightChoiceMoreRightReward - percentRightChoiceMoreLeftReward
            rightwardBiasByReward.append(rightwardBiasThisFreq)
        allRightwardBiasThisSession = [rightwardBiasByReward for cell in range(len(cellsThisSession))]
        allRightwardBias.extend(allRightwardBiasThisSession)
        
    celldb['rightwardBiasByReward'] = allRightwardBias  #np.tile(rightwardBiasByReward, (len(cellsThisSession),1))
    celldb.to_hdf(celldbPath,  key='reward_change')

