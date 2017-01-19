import numpy as np
import sys
import importlib
from jaratoolbox import spikesanalysis
from jaratoolbox import settings
from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader


mouseName = 'test017'
allcellsFileName = 'allcells_'+mouseName+'_quality'
sys.path.append(settings.ALLCELLS_PATH)
allcells = importlib.import_module(allcellsFileName)
cell = allcells.cellDB[100]
(eventData, spikeData, bdata) = loader.load_remote_2afc_data(cell)


valid = (bdata['outcome']==bdata.labels['outcome']['correct'])|(bdata['outcome']==bdata.labels['outcome']['error'])
rightward = bdata['choice']==bdata.labels['choice']['right']
leftward = bdata['choice']==bdata.labels['choice']['left']
correct = bdata['outcome']==bdata.labels['outcome']['correct']
possibleFreq = np.unique(bdata['targetFrequency'])
midFreq = bdata['targetFrequency'] == possibleFreq[len(possibleFreq)/2]
correctRightward = rightward & correct
correctLeftward = leftward & correct

CASE = 1

if CASE == 1:
    # -- Exclude first 20 valid trials and last block if too short -- #
    ################# Lan's method ###################################
    # -- Check if a block or trials fit criteria to include in analysis -- #
    trialsToInclude = np.ones(len(bdata['currentBlock']), dtype=bool)
    indFirstTrialEachBlock  = np.flatnonzero(np.diff(bdata['currentBlock']))+1 #index of first trial at each block(excluding the first block)

    # -- Get rid of the last block if it's too short (don't have enough valid trials)-- #
    minLastBlockSize = 50 
    firstTrialsEachBlock = np.r_[0,indFirstTrialEachBlock]
    lastTrialsEachBlock = np.r_[(indFirstTrialEachBlock-1),(len(bdata['currentBlock'])-1)]
    for (start,end) in zip(firstTrialsEachBlock,lastTrialsEachBlock):
        #firstTrialLastBlock = indFirstTrialEachBlock[-1]
        if sum(valid[start:end+1]) < minLastBlockSize:
            trialsToInclude[start:end+1] = False
            if start != 0:
                indFirstTrialEachBlock = np.delete(indFirstTrialEachBlock,np.where(indFirstTrialEachBlock==start)[0])
    # -- Skip first 20 VALID trials of a block when calculating mod index --#
    numTrialsToExclude = 20 # how many trials to exclude at the beginning of each block from modulation index
    indTwentithValidTrialEachBlock = [(ind+np.where(valid[ind:]==1)[0][20]) for ind in indFirstTrialEachBlock]
    indTrialsToExcludeEachBlock = zip(indFirstTrialEachBlock, indTwentithValidTrialEachBlock)
    for (indStart, indEnd) in indTrialsToExcludeEachBlock:
        trialsToInclude[indStart:indEnd] = False
    ##################################################################


    ################## Billy's method #################################
    # -- 20161123 Found 2 bugs in Billy's method for excluding trials/last block -- #
    #This skips first trials of either frequency (middle or other) in each block. Can easily change to skip first trials of middle freq. Include middle freq oneFreq[trialNum] in elif.
    firstTrialsExclude = 20 # how many trials to exclude at the beginning of each block from modulation index
    highBlock = bdata['currentBlock']==bdata.labels['currentBlock']['high_boundary']

    numTrials = len(highBlock)
    currentBlock = highBlock[0] #NOTE20161123 THIS IS A BUG, it should be currentBlock=bdata['currentBlock'][0], this bug resulted in first 20 trials of block 1 sometimes getting excluded

    firstTrialNum = 0
    trialsToInclude2 = np.zeros((numTrials), dtype = bool) #start out as all false
    blockNumber = np.zeros((numTrials))
    curBlockNum = 0
    totalBlocks = 1
    for trialNum,block in enumerate(highBlock):
        if (block != currentBlock): #check if there is a new block
            firstTrialNum = 0
            currentBlock = block
            curBlockNum += 1
            totalBlocks +=1
        blockNumber[trialNum]=curBlockNum
        if (valid[trialNum] & (firstTrialNum >= firstTrialsExclude)): #check if the trial is correct and past excluding trials
            trialsToInclude2[trialNum] = True 
        elif (valid[trialNum]): #skip this trial 
            firstTrialNum += 1


    #This will check how big the last block is
    minLastBlockSize = 50 #This includes the first blocks that will be skipped
    lastBlock = highBlock[-1] #NOTE20161123 THIS IS A BUG, it should be currentBlock=bdata['currentBlock'][0]
    lastBlockCount = 0
    lastTrialNum = -1
    while (highBlock[lastTrialNum]==lastBlock):
        lastTrialNum-=1
        lastBlockCount-=1
    if (sum(valid[lastBlockCount:])<minLastBlockSize):
        trialsToInclude2[lastTrialNum:]=False
        totalBlocks -=1 #dont count the last block if its too small
    ####################################################################################


if CASE == 2:
    # -- Check if a block or trials fit criteria to include in analysis -- #
    trialsToInclude = np.ones(len(bdata['currentBlock']), dtype=bool)
    indFirstTrialEachBlock  = np.flatnonzero(np.diff(bdata['currentBlock']))+1 #index of first trial at each block(excluding the first block)

    # -- Get rid of the last block if it's too short (don't have enough valid trials)-- #
    minLastBlockSize = 50 
    firstTrialLastBlock = indFirstTrialEachBlock[-1]
    if sum(valid[firstTrialLastBlock:]) < minLastBlockSize:
        trialsToInclude[firstTrialLastBlock:] = False
        indFirstTrialEachBlock = indFirstTrialEachBlock[:-1]

    # -- Skip first 20 VALID trials of a block when calculating mod index --#
    numTrialsToExclude = 20 # how many trials to exclude at the beginning of each block from modulation index
    indTwentithValidTrialEachBlock = [(ind+np.where(valid[ind:]==1)[0][20]) for ind in indFirstTrialEachBlock]
    indTrialsToExcludeEachBlock = zip(indFirstTrialEachBlock, indTwentithValidTrialEachBlock)
    for (indStart, indEnd) in indTrialsToExcludeEachBlock:
        trialsToInclude[indStart:indEnd] = False

    # -- Calculate modulation index using only correct trials, trials not skipped, and only middle frequency
    trialsToUse = trialsToInclude & midFreq 
    trialsToUseRight = correctRightward & trialsToUse
    trialsToUseLeft = correctLeftward & trialsToUse
    trialsEachCond = [trialsToUseRight,trialsToUseLeft]
    eventTimes = eventData.timestamps
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==0)
    EventOnsetTimes = eventTimes[soundOnsetEvents]
    countTimeRange = [0,0.1]

    spkTimeStamps = spikeData.timestamps
    timeRange = [-0.2,0.8] # In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spkTimeStamps,EventOnsetTimes,timeRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)  #spike counts in the window of interest for modulation
    spikeCountEachTrial = spikeCountMat.flatten() #spikeCountMat contains num of spikes in countTimeRange, each column is each trial, only one row because only given one time bin(countTimeRange)
    # -- Calculate modulation index and significance p value -- #
    spikeAvgRight = sum(spikeCountEachTrial[trialsToUseRight])/float(sum(trialsToUseRight))
    spikeAvgLeft = sum(spikeCountEachTrial[trialsToUseLeft])/float(sum(trialsToUseLeft))
    if ((spikeAvgRight + spikeAvgLeft) == 0):
        modIndex = 0.0
        modSig = 1.0
    else:
        modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)
        modIndex = (spikeAvgRight - spikeAvgLeft)/(spikeAvgRight + spikeAvgLeft)

    # -- Calculate modulation direction score -- #
    aveSpikesEachBlock = []
    blockVec = np.zeros(len(bdata['currentBlock']))
    firstTrialsEachBlock = np.r_[0,indFirstTrialEachBlock]
    lastTrialsEachBlock = np.r_[(indFirstTrialEachBlock-1),(len(bdata['currentBlock'])-1)]
    for (start,end) in zip(firstTrialsEachBlock,lastTrialsEachBlock):
        trialsThisBlock = np.zeros(len(bdata['currentBlock']), dtype=bool)
        trialsThisBlock[start:end] = True
        aveSpikesEachBlock.append(np.average(spikeCountEachTrial[trialsToUse&trialsThisBlock]))
    rateChangeOverBlocks = np.diff(np.array(AveSpikesEachBlock))
    if np.all(rateChangeOverBlocks>0) or np.all(rateChangeOverBlocks<0) or np.all(rateChangeOverBlocks==0): #consistently go up or down, or unchanged the whole session
        modDir = 0
    elif len(np.flatnonzero(rateChangeOverBlocks))==1: #no change the whole session except one block either goes up or down
        modDir = 0
    else:
        modDir = 1

