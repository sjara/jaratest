'''
Estimate how quick animals change behavior after switch.

7 seconds
'''

import os, sys
import pandas as pd
import numpy as np
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
import figparams

from matplotlib import pyplot as plt
from jaratoolbox import extraplots

PLOT_SESSIONS = 0
SHUFFLE_DATA = 0

minBlockSize = 30
nTrialsAroundTransition = 140

brainAreas = ['rightAC','rightAStr']

STUDY_NAME = figparams.STUDY_NAME
FIGNAME = 'reward_modulation_after_switch'
figDataFile = 'behavior_change_after_switch.npz'
if SHUFFLE_DATA:
    figDataFile = 'behavior_change_after_switch_shuffled.npz'
figDataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)
if not os.path.exists(figDataDir):
    os.mkdir(figDataDir)
figDataFullPath = os.path.join(figDataDir,figDataFile)
scriptFullPath = os.path.realpath(__file__)

databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
celldb = celldatabase.load_hdf(databaseFullPath)

possibleSubjects = np.unique(celldb.subject)

#for inds,subject in enumerate(possibleSubjects):
#    celldbThisSubject = celldb.query('subject=="{}"'.format(subject))
#    for date in np.unique(celldbThisSubject.date):

avgChoiceInTransitionEachSession = {'rightAC_low':[], 'rightAStr_low':[],
                                    'rightAC_high':[], 'rightAStr_high':[]}
freqLabels = ['low','high']
freqInds = [0,-1] # We use -1 in case there are more than two freqs

for brainArea in brainAreas:
    celldbThisArea = celldb.query('brainArea=="{}"'.format(brainArea))
     
    for date in np.unique(celldbThisArea.date):
        firstCell = celldbThisArea.query('date=="{}"'.format(date)).iloc[0]
        cellObj = ephyscore.Cell(firstCell)
        rcInd = firstCell['sessionType'].index('behavior')
        bdata = cellObj.load_behavior_by_index(rcInd, behavClass=loadbehavior.FlexCategBehaviorData)

        print('Loaded {} {}'.format(str(cellObj),firstCell['brainArea']))

        rightward = bdata['choice']==bdata.labels['choice']['right']
        currentBlock = bdata['currentBlock'] # This can be 1 or 2
        possibleFreq = np.unique(bdata['targetFrequency'])

        # Look at responses to one freq, but use a trial index according to all trials (not just those)
        for indf,freqPos in enumerate(freqInds):
            
            validTrialsThisFreq = ((bdata['targetFrequency']==possibleFreq[freqPos]) & bdata['valid']).astype(bool)
            validTrials = bdata['valid'].astype(bool)
            maskedChoices = np.ma.array(rightward,mask=~validTrialsThisFreq)
            
            ###maskedChoices = maskedChoices[validTrialsThisFreq] # If using only this freq trials
            maskedChoices = maskedChoices[validTrials]  # This should have length of valid, but mask one freq
            maskedChoices = maskedChoices - np.mean(maskedChoices)

            # -- Permute (to test whether effect is not random) --
            if SHUFFLE_DATA:
                np.random.seed(2)
                maskedChoices = np.random.permutation(maskedChoices)

            # -- Find trials each block --
            bdata.find_trials_each_block()
            numBlocks = bdata.blocks['nBlocks']
            eachBlockType = bdata.blocks['eachBlockType']
            trialsEachBlock = bdata.blocks['trialsEachBlock']

            ###trialsToAnalyzeEachBlock = trialsEachBlock & validTrialsThisFreq[:,np.newaxis ]# If using only this freq trials
            trialsToAnalyzeEachBlock = trialsEachBlock & validTrials[:,np.newaxis]
            blockSize = sum(trialsToAnalyzeEachBlock)
            if (blockSize[-1] < minBlockSize): # Check whether last block is too small to analyze
                #trialsToAnalyzeEachBlock = trialsToAnalyzeEachBlock[:,:-1]
                numBlocks -= 1
            
            # -- Estimate choices around transitions --
            alignedBlocks = np.ma.masked_array(np.zeros((numBlocks-1, 2*nTrialsAroundTransition)), dtype=float, mask=True)
            firstTrialInd = nTrialsAroundTransition
            #normedSpikesEachTrial = spkMat[relevantTrials,0] - np.mean(spkMat[relevantTrials,0])
            firstTrialEachBlock = np.cumsum(blockSize)[:-1]
            if eachBlockType[0]==bdata.labels['currentBlock']['more_right']:
                mfactor = [1,-1,1,-1,1,-1,1,-1]
            else:
                mfactor = [-1,1,-1,1,-1,1,-1,1]
            for indtr in range(numBlocks-1):
                nTrialsPre = min(nTrialsAroundTransition, blockSize[indtr])
                nTrialsPost = min(nTrialsAroundTransition, len(maskedChoices)-firstTrialEachBlock[indtr])
                trialRange = range(firstTrialEachBlock[indtr]-nTrialsPre, firstTrialEachBlock[indtr]+nTrialsPost)
                samplesToFill = slice(firstTrialInd-nTrialsPre,firstTrialInd+nTrialsPost)
                alignedBlocks.mask[indtr, samplesToFill]=False
                alignedBlocks[indtr, samplesToFill] = mfactor[indtr]*maskedChoices[trialRange]
            avgChoiceInTransition = np.mean(alignedBlocks,axis=0)

            thisCond = '{}_{}'.format(brainArea,freqLabels[indf])
            avgChoiceInTransitionEachSession[thisCond].append(avgChoiceInTransition)

            if PLOT_SESSIONS:
                plt.clf()
                plt.plot(avgChoiceInTransition)
                plt.show()
                plt.waitforbuttonpress()

        #sys.exit()


print('Saving results to {}'.format(figDataFullPath))
np.savez(figDataFullPath, script=scriptFullPath,
         avgChoiceInTransitionAC_low=avgChoiceInTransitionEachSession['rightAC_low'],
         avgChoiceInTransitionAC_high=avgChoiceInTransitionEachSession['rightAC_high'],
         avgChoiceInTransitionAStr_low=avgChoiceInTransitionEachSession['rightAStr_low'],
         avgChoiceInTransitionAStr_high=avgChoiceInTransitionEachSession['rightAStr_high'],
         minBlockSize=minBlockSize, nTrialsAroundTransition=nTrialsAroundTransition)


'''        
# -- Plot results --
plt.clf()
plt.subplot(2,2,1)
plt.plot(np.mean(avgChoiceInTransitionEachSession['rightAC_low'],axis=0),'.-')
plt.xlim([40,100])
plt.title('AC (low freq)')
plt.grid(1)
plt.subplot(2,2,2)
plt.plot(np.mean(avgChoiceInTransitionEachSession['rightAStr_low'],axis=0),'.-')
plt.xlim([40,100])
plt.title('AStr (low freq)')
plt.grid(1)
plt.subplot(2,2,3)
plt.plot(np.mean(avgChoiceInTransitionEachSession['rightAC_high'],axis=0),'.-')
plt.xlim([40,100])
plt.title('AC (high freq)')
plt.grid(1)
plt.subplot(2,2,4)
plt.plot(np.mean(avgChoiceInTransitionEachSession['rightAStr_high'],axis=0),'.-')
plt.xlim([40,100])
plt.title('AStr (high freq)')
plt.grid(1)
plt.show()
'''
