'''
Calculate reward modulation for first half of trials vs second half of trials

Based on calculate_reward_modulation_celldb.py

NOTES:
- It currently uses re-calculated evlockData (by Santiago, after submission)
- I am using only trials of preferred choice of the cell (not all choices)
  so this gives an underestimate of how many total trials it takes to switch.

It took about 12 seconds (for both areas).
'''


import sys, os
import numpy as np
import pandas as pd
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
SHUFFLE_DATA = 0

#evlockDataPath = os.path.join(settings.EPHYS_PATH, figparams.STUDY_NAME, 'evlock_spktimes')
evlockDataPath = '/var/tmp/processed_data'

STUDY_NAME = figparams.STUDY_NAME
FIGNAME = 'reward_modulation_after_switch'
figDataFile = 'summary_rewardmod_after_switch.npz'
if SHUFFLE_DATA:
    figDataFile = 'summary_rewardmod_after_switch_shuffled.npz'    
figDataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)
if not os.path.exists(figDataDir):
    os.mkdir(figDataDir)
figDataFullPath = os.path.join(figDataDir,figDataFile)
scriptFullPath = os.path.realpath(__file__)

databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
celldb = celldatabase.load_hdf(databaseFullPath)

brainAreas = ['rightAC','rightAStr']
#brainAreas = ['rightAStr']

minBlockSize = 30  # Minimum number of trials in a block to be analyzed
alphaLevel = 0.05
nTrialsAroundTransition = 140

goodCells = celldb.query("missingTrialsBehav==0 and keepAfterDupTest==1 and cellInTargetArea==1")

modDirLow = goodCells['modDirLow_0-0.3s_center-out_removedsidein'].astype(bool)
modDirHigh = goodCells['modDirHigh_0-0.3s_center-out_removedsidein'].astype(bool)
modSigLow = goodCells['modSigLow_0-0.3s_center-out_removedsidein']
modSigHigh = goodCells['modSigHigh_0-0.3s_center-out_removedsidein']



choiceSelectiveCells = goodCells['movementModS_[0.0, 0.3]_removedsidein']<alphaLevel # 312 total
encodeMovement = (goodCells['movementSelective_moredif_Mv'] | goodCells['movementSelective_samedif_MvSd']).astype(bool) # 251
#modulatedCells = (goodCells['modSigLow_0-0.3s_center-out_removedsidein']<(alphaLevel/2)) | \
#                 (goodCells['modSigHigh_0-0.3s_center-out_removedsidein']<(alphaLevel/2)) # 107 total
#modulatedCells = ( (modSigLow<(alphaLevel)) & modDirLow ) | ( (modSigHigh<(alphaLevel)) & modDirHigh )

rightwardPrefer = goodCells['movementModI_[0.0, 0.3]_removedsidein']>0
modulatedCells = ( ~rightwardPrefer & (modSigLow<(alphaLevel)) & modDirLow ) | \
                 ( rightwardPrefer & (modSigHigh<(alphaLevel)) & modDirHigh )

#cellsToAnalyze = goodCells.loc[modulatedCells]
cellsToAnalyze = goodCells.loc[modulatedCells & encodeMovement] # 47 total (when separating by choice preference)

# -- Find choice side with strongest response for each cell (0:Left, 1:Right)--
preferredChoiceRight = cellsToAnalyze['movementAveFrRight_[0.0, 0.3]_removedsidein'] > \
                       cellsToAnalyze['movementAveFrLeft_[0.0, 0.3]_removedsidein']

avgSpikesInTransitionEachCell = {'rightAC':[], 'rightAStr':[]}

for brainArea in brainAreas:

    ###cellsThisArea = celldb.query("brainArea=='{}'".format(brainArea)) # It reorders things in a weird way

    for indc,cellrow in cellsToAnalyze.iterrows():

        # -- This is not the best way, but doing a query seems to give problems with indexes --
        if cellrow['brainArea']!=brainArea:
            continue
        #for indc in [0]:
        # -- Test just one cell ---
        #indc,cellrow = celldatabase.find_cell(celldb, 'adap012', '2016-02-04', 2340.0, 3, 3)

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
            print('Missing trials: {}'.format(str(missingTrials)))
            bdata.remove_trials(missingTrials) # This modifies all fields of bdata in place

        # -- Find correct trials for frequency of interest --
        correct = bdata['outcome']==bdata.labels['outcome']['correct']
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left']
        possibleFreq = np.unique(bdata['targetFrequency'])
        numFreqs = len(possibleFreq)
        currentBlock = bdata['currentBlock']
        #freqIndToAnalyze = 1  # 0:low, 1:high
        #freqIndToAnalyze = int(preferredChoiceRight[indc])  # 0:low, 1:high
        #correctTrialsThisFreq = correct & (bdata['targetFrequency']==possibleFreq[freqIndToAnalyze])
        if preferredChoiceRight[indc]:
            trialsThisChoice = rightward
        else:
            trialsThisChoice = leftward
        relevantTrials = rightward|leftward  # Use all trials with choices
        ###relevantTrials = trialsThisChoice  # Use only trials with preferred choice
         
        # -- Find trials each block --
        bdata.find_trials_each_block()
        numBlocks = bdata.blocks['nBlocks']
        trialsEachBlock = bdata.blocks['trialsEachBlock']
        #trialsToAnalyzeEachBlock = trialsEachBlock & trialsThisChoice[:,np.newaxis]
        trialsToAnalyzeEachBlock = trialsEachBlock & relevantTrials[:,np.newaxis]
        blockSize = sum(trialsToAnalyzeEachBlock)
        if (blockSize[-1] < minBlockSize): # Check whether last block is too small to analyze
            trialsToAnalyzeEachBlock = trialsToAnalyzeEachBlock[:,:-1]
            numBlocks -= 1

        # -- Estimate number of spikes on each trial --
        spkMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,[0,0.3])

        # -- Permute (to test whether effect is not random) --
        if SHUFFLE_DATA:
            np.random.seed(1)
            spkMat = np.random.permutation(spkMat)
        
        # -- Estimate average spikes during each block transition --
        alignedBlocks = np.ma.masked_array(np.zeros((numBlocks-1, 2*nTrialsAroundTransition)), dtype=float, mask=True)
        firstTrialInd = nTrialsAroundTransition
        #normedSpikesEachTrial = spkMat[relevantTrials,0] - np.mean(spkMat[relevantTrials,0])
        normedSpikesEachTrial = np.ma.array(spkMat[:,0] - np.mean(spkMat[:,0]),mask=True)
        normedSpikesEachTrial.mask[trialsThisChoice] = False
        normedSpikesEachTrial = normedSpikesEachTrial[relevantTrials]
        firstTrialEachBlock = np.cumsum(blockSize)[:-1]
        mfactor = [1,-1,1,-1,1,-1,1,-1]
        for indtr in range(numBlocks-1):
            nTrialsPre = min(nTrialsAroundTransition, blockSize[indtr])
            nTrialsPost = min(nTrialsAroundTransition, len(normedSpikesEachTrial)-firstTrialEachBlock[indtr])
            trialRange = range(firstTrialEachBlock[indtr]-nTrialsPre, firstTrialEachBlock[indtr]+nTrialsPost)
            samplesToFill = slice(firstTrialInd-nTrialsPre,firstTrialInd+nTrialsPost)
            alignedBlocks.mask[indtr, samplesToFill]=False
            alignedBlocks[indtr, samplesToFill] = mfactor[indtr]*normedSpikesEachTrial[trialRange]
        avgSpikesInTransition = np.mean(alignedBlocks,axis=0)

        # -- Flip if necesssary, so all cells have transitions in the same direction --
        avgFiringBefore = np.mean(avgSpikesInTransition[:nTrialsAroundTransition]) # At the transition
        avgFiringAfter = np.mean(avgSpikesInTransition[nTrialsAroundTransition:])  # At the transition
        #avgFiringBefore = np.mean(avgSpikesInTransition[:nTrialsAroundTransition-20]) # Far from the transition
        #avgFiringAfter = np.mean(avgSpikesInTransition[20+nTrialsAroundTransition:])  # Far from the transition
        if avgFiringBefore<avgFiringAfter:
            avgSpikesInTransition = -avgSpikesInTransition

        avgSpikesInTransitionEachCell[brainArea].append(avgSpikesInTransition)
        
        if PLOT_EACH_CELL:
            # -- Smooth signal --
            smoothWinSize= 10;
            winShape = np.concatenate((np.zeros(smoothWinSize),np.ones(smoothWinSize))); # Causal
            #winShape = np.ones(smoothWinSize); # Acausal
            winShape = winShape/np.sum(winShape)
            smoothSpkTransition = np.convolve(avgSpikesInTransition,winShape,mode='same')

            # -- Plot results for each cell --
            plt.clf()
            plt.subplot(3,1,1)
            timeRangeToPlot = [-0.2,0.5]
            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                       indexLimitsEachTrial,
                                                       timeRange=timeRangeToPlot,
                                                       trialsEachCond=trialsToAnalyzeEachBlock)
            plt.subplot(3,1,2)
            plt.plot(spkMat[relevantTrials,0],'.-',color='0.8')
            plt.hold(1)
            for bsize in np.cumsum(blockSize)[:-1]:
                plt.axvline(bsize,color='0.5')
            smoothSpkCount = np.convolve(spkMat[relevantTrials,0],winShape,mode='same')
            plt.plot(smoothSpkCount,'-',lw=2,color='r')


            plt.subplot(3,1,3)
            plt.plot(avgSpikesInTransition,'.-',color='0.8')
            plt.hold(1)
            plt.plot(smoothSpkTransition, lw=2)
            plt.axvline(firstTrialInd,color='0.5')
            plt.waitforbuttonpress()
            
        #sys.exit()
        
print('Saving results to {}'.format(figDataFullPath))
np.savez(figDataFullPath, script=scriptFullPath,
         avgSpikesInTransitionAC=avgSpikesInTransitionEachCell['rightAC'],
         avgSpikesInTransitionAStr=avgSpikesInTransitionEachCell['rightAStr'],
         minBlockSize=minBlockSize, nTrialsAroundTransition=nTrialsAroundTransition)

