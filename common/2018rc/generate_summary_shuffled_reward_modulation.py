'''
Estimate reward modulation on shuffled data.

Based on calculate_reward_modulation_celldb.py
and generate_summary_reward_modulation_movement.py

It took 36 seconds for one iteration (for the 251 neurons selected).
It took 45 minutes for 100 iterations.
'''

import sys, os
import numpy as np
import pandas as pd
from scipy import stats
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
import figparams

from matplotlib import pyplot as plt
from jaratoolbox import extraplots


PLOT_EACH_CELL = 0
VERBOSE = 0

#evlockDataPath = os.path.join(settings.EPHYS_PATH, figparams.STUDY_NAME, 'evlock_spktimes')
evlockDataPath = '/var/tmp/processed_data'

FIGNAME = 'reward_modulation_shuffled'
figDataFile = 'rewardmod_shuffled.npz'
figDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
if not os.path.exists(figDataDir):
    os.mkdir(figDataDir)
figDataFullPath = os.path.join(figDataDir,figDataFile)
scriptFullPath = os.path.realpath(__file__)

databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
celldb = celldatabase.load_hdf(databaseFullPath)

brainAreas = ['rightAC','rightAStr']

alphaLevel = 0.05

#conditions = [('sound', [-0.2,0]), ('center-out', [0,0.3])]
conditions = [('center-out', [0,0.3])]


goodCells = celldb.query("missingTrialsBehav==0 and keepAfterDupTest==1 and cellInTargetArea==1")

choiceSelectiveCells = goodCells['movementModS_[0.0, 0.3]_removedsidein']<alphaLevel # 312 total
encodeMovement = (goodCells['movementSelective_moredif_Mv'] | goodCells['movementSelective_samedif_MvSd']).astype(bool) # 251
cellsToAnalyze = goodCells.loc[encodeMovement] # 251 total

#########33cellsToAnalyze = cellsToAnalyze.iloc[:10]  ### Test with a few cells

nIter = 100  # Number of shuffled iterations
shuffledResults = []

for oneIter in range(nIter):
    '''
    modulationDict = {'subject': [],
                      'date': [],
                      'tetrode': [],
                      'cluster': [],
                      'brainArea':[]}
    '''
    modulationDict = {}
    for (alignment, countTimeRange) in conditions:
        windowStr = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment
        modulationDict.update({'modIndLow_'+windowStr: [],
                               'modSigLow_'+windowStr: [],
                               'modDirLow_'+windowStr: [],
                               'modIndHigh_'+windowStr: [],
                               'modSigHigh_'+windowStr: [],
                               'modDirHigh_'+windowStr: []})

    brainAreaEachCell = []
    for indc,cellrow in cellsToAnalyze.iterrows():
        if VERBOSE:
            print('Cell {} [{}] {}'.format(indc,cellrow['index'],cellrow['brainArea']))

        # -- Load (preprocessed) ephys data --
        alignment = 'center-out'
        evlockDataFilename = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(cellrow.subject, cellrow.date, cellrow.depth,
                                                                    cellrow.tetrode, cellrow.cluster, alignment)
        evlockDataFullpath = os.path.join(evlockDataPath, evlockDataFilename)
        try:
            evlockSpktimes = np.load(evlockDataFullpath)
        except:
            print('Data could not be loaded: {}'.format(evlockDataFullpath))
            continue
        spikeTimesFromEventOnset = evlockSpktimes['spikeTimesFromEventOnset']
        indexLimitsEachTrial = evlockSpktimes['indexLimitsEachTrial']
        trialIndexForEachSpike = evlockSpktimes['trialIndexForEachSpike']
        timeRange = evlockSpktimes['timeRange']
        missingTrials = evlockSpktimes['missingTrials']

        # -- Load behavior data --
        cellObj = ephyscore.Cell(cellrow)
        sessionInd = cellObj.get_session_inds('behavior')[0]
        bdata = cellObj.load_behavior_by_index(sessionInd, behavClass=loadbehavior.FlexCategBehaviorData)

        # -- Remove missing trials from behav data --
        if len(missingTrials)>0:
            #print('Missing trials: {}'.format(str(missingTrials)))
            bdata.remove_trials(missingTrials) # This modifies all fields of bdata in place


        ###==== Code from Lan (calculate_reward_modulation_celldb)  starts here ====###

        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['same_reward'],
                      bdata.labels['currentBlock']['more_left'],
                      bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)

        # -- Find trials each type each block to evaluate Modulation Direction -- #
        nTrials = len(bdata['currentBlock'])
        blockBoundaries = np.flatnonzero(np.diff(bdata['currentBlock']))
        lastTrialEachBlock = np.hstack((blockBoundaries,nTrials))
        firstTrialEachBlock = np.hstack((0,lastTrialEachBlock[:-1]+1))
        nRcBlocks = 0 # Number of blocks with unequal reward on left and right port
        blockNumEachTrial = np.zeros(nTrials)
        for indBlock,firstTrial in enumerate(firstTrialEachBlock):
            typeThisBlock = bdata['currentBlock'][firstTrial]
            if (typeThisBlock == bdata.labels['currentBlock']['more_left']) | \
               (typeThisBlock ==bdata.labels['currentBlock']['more_right']):
                nRcBlocks += 1
                lastTrial = lastTrialEachBlock[indBlock]
                blockNumEachTrial[firstTrial:lastTrial] = nRcBlocks # possible values of blockNumEachTrial start at 1

        trialsEachBlockLeftOrRightMore = behavioranalysis.find_trials_each_type(blockNumEachTrial, range(1, nRcBlocks+1))
        # NOTE: trialsEachBlock is an ndarray of dimension nTrials*nRcBlocks where nRcBlocks is the
        #       number of left_more or right_more blocks

        correct = bdata['outcome']==bdata.labels['outcome']['correct']

        if (not sum(trialsEachType[:,1])) or (not sum(trialsEachType[:,2])):
            # -- Theses condition mean there's no change in reward for this session --
            print '************ Session {} has no change in reward. ***************'.format(cell.date)
            continue


        possibleFreq = np.unique(bdata['targetFrequency'])
        numFreqs = len(possibleFreq)
        if numFreqs != 2:
            if VERBOSE:
                print 'Warning: There are more than 2 frequencies used in behavior session. '+\
                    'Modulation index calculated only for the lowest and highest freqs!'
        lowFreq = bdata['targetFrequency'] == possibleFreq[0]
        highFreq = bdata['targetFrequency'] == possibleFreq[-1]

        '''
        modulationDict['subject'].append(cellrow.subject)
        modulationDict['date'].append(cellrow.date)
        modulationDict['tetrode'].append(cellrow.tetrode)
        modulationDict['cluster'].append(cellrow.cluster)
        modulationDict['brainArea'].append(cellrow.brainArea)
        '''
        brainAreaEachCell.append(cellrow.brainArea)
        
        for (alignment, countTimeRange) in conditions:
            # Make names for count time range and alignment for labeling columns in output df
            windowStr = str(countTimeRange[0])+'-'+str(countTimeRange[1])+'s_'+alignment

            # NOTE: this is done by spikesanalysis.evaluate_modulation() below
            #       but it's needed for evaluating direction of modulation across blocks
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange)
            spikeCountEachTrial = spikeCountMat.flatten()

            # -- Permute (to test whether effect is not random) --
            spikeCountEachTrial = np.random.permutation(spikeCountEachTrial)

            freqLabels = ['Low','High']
            for indf,freq in enumerate([lowFreq, highFreq]):
                # The indexes 1 and 2 below are defined "blockTypes" above
                trialsMoreLeft = trialsEachType[:,1] & freq & correct 
                trialsMoreRight = trialsEachType[:,2] & freq & correct 
                trialsEachCond = [trialsMoreRight,trialsMoreLeft]

                # -- Calculate modulation index and significance p value -- #
                [zStat,modSig] = stats.ranksums(spikeCountEachTrial[trialsMoreRight],
                                                spikeCountEachTrial[trialsMoreLeft])
                spikeAvgMoreRight = np.average(spikeCountEachTrial[trialsMoreRight])
                spikeAvgMoreLeft = np.average(spikeCountEachTrial[trialsMoreLeft])
                modIndex = (spikeAvgMoreRight - spikeAvgMoreLeft)/(spikeAvgMoreRight + spikeAvgMoreLeft)

                #### -- Index calculated as (moreRight-moreLeft)/(moreRight+moreLeft)
                ###modIndex = (spikeAvgEachCond[1]-spikeAvgEachCond[0]) / (spikeAvgEachCond[1]+spikeAvgEachCond[0])
                '''
                if ((spikeAvgMoreRight + spikeAvgMoreLeft) == 0):
                    modIndex = 0.0
                    modSig = 1.0
                else:
                    modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,countTimeRange,trialsEachCond)[1]
                    modIndex = (spikeAvgMoreRight - spikeAvgMoreLeft)/(spikeAvgMoreRight + spikeAvgMoreLeft)
                '''
                '''
                # NOTE: we still need to calculate spiketimes_to_spikecounts() anyway,
                #       so using evaluate_modulation() would be redundant.
                spikeAvgEachCond,modSig = spikesanalysis.evaluate_modulation(spikeTimesFromEventOnset,indexLimitsEachTrial,
                                                                             countTimeRange,trialsEachCond)
                '''

                # -- Evaluate modulation direction (across blocks) -- #
                aveSpikeEachBlock = np.zeros(nRcBlocks)
                for block in range(nRcBlocks):
                    trialsThisBlock = trialsEachBlockLeftOrRightMore[:, block] & freq & correct
                    aveSpikeThisBlock = np.average(spikeCountEachTrial[trialsThisBlock])
                    aveSpikeEachBlock[block] = aveSpikeThisBlock
                aveSpikeDiffEachBlock = np.diff(aveSpikeEachBlock)
                if len(np.unique(np.sign(aveSpikeDiffEachBlock))) == 1:
                    # All spike differences of the same sign, which means that
                    # firing rate keeps going up or going down throughout session
                    modDir = 0
                else:
                    # At least one block firing rate changes in opposite direction;
                    # cannot tell if firing rate flip-flops per block 
                    modDir = 1

                modulationDict['modInd{}_'.format(freqLabels[indf])+windowStr].append(modIndex) 
                modulationDict['modSig{}_'.format(freqLabels[indf])+windowStr].append(modSig)
                modulationDict['modDir{}_'.format(freqLabels[indf])+windowStr].append(modDir)

    modIndLow = np.array(modulationDict['modSigLow_0-0.3s_center-out'])
    modIndHigh = np.array(modulationDict['modSigHigh_0-0.3s_center-out'])

    for inda,brainArea in enumerate(brainAreas):
        inThisBrainArea = np.array(brainAreaEachCell)==brainArea
        fractionModLow = np.mean(modIndLow[inThisBrainArea]<alphaLevel)
        fractionModHigh = np.mean(modIndHigh[inThisBrainArea]<alphaLevel)
        print('low={:0.2%} high={:0.2%}  {}'.format(fractionModLow,fractionModHigh,brainArea))

    shuffledResults.append(modulationDict)

print('Saving results to {}'.format(figDataFullPath))
np.savez(figDataFullPath, script=scriptFullPath, nIter=nIter,
         shuffledResults=shuffledResults, brainAreaEachCell=brainAreaEachCell)
    
