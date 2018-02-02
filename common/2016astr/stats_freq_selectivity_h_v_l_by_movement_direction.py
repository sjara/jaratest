import os
import random
import numpy as np
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from scipy import stats
import matplotlib
import figparams
import pdb

subsample = False
fraction = 1/3.0
np.random.seed(0)

FIGNAME = 'sound_freq_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

responseEachFreqEachCellLeftChoiceFile = 'response_each_freq_each_cell_psycurve_left_choice.npz'
responseEachFreqEachCellRightChoiceFile = 'response_each_freq_each_cell_psycurve_right_choice.npz'

responseLeftFullPath = os.path.join(dataDir,responseEachFreqEachCellLeftChoiceFile)
responseEachCellEachFreqLeftChoice = np.load(responseLeftFullPath)
responseRightFullPath = os.path.join(dataDir,responseEachFreqEachCellRightChoiceFile)
responseEachCellEachFreqRightChoice = np.load(responseRightFullPath)

numCells = responseEachCellEachFreqLeftChoice.shape[0]
numFreqs = responseEachCellEachFreqLeftChoice.shape[-1]

#pValsBoth = np.array([])

if subsample:
    repeatedSamples = 100
else:
    repeatedSamples = 1
percentFreqSelLeftSamples = np.zeros(repeatedSamples)
percentFreqSelRightSamples = np.zeros(repeatedSamples)

for inds in range(repeatedSamples):
    selectivityIndsLeft = np.array([])
    pValsLeft = np.array([])
    selectivityIndsRight = np.array([])
    pValsRight = np.array([])
    for cellInd in range(numCells):
        '''
        # -- Not split by movement directions, analyse high vs low selectivity using all trials -- #
        fLow = np.concatenate((responseEachCellEachFreqLeftChoice[cellInd,:,:3].compressed(),responseEachCellEachFreqRightChoice[cellInd,:,:3].compressed())) 
        fHigh = np.concatenate((responseEachCellEachFreqLeftChoice[cellInd,:,3:].compressed(),responseEachCellEachFreqRightChoice[cellInd,:,3:].compressed())) 
        zScore,pVal = stats.ranksums(fLow, fHigh)
        pValsBoth = np.append(pValsBoth,pVal)
        '''
        # -- Split left and right choice to analyse high vs low selectivity fixing each movement direction -- #
        if not subsample:
            fLowLeft = responseEachCellEachFreqLeftChoice[cellInd,:,:3].compressed()
            fHighLeft = responseEachCellEachFreqLeftChoice[cellInd,:,3:].compressed()
        else:
            fLowLeft = np.array([])
            fHighLeft = np.array([])
            fLowTrialNumsLeft = [responseEachCellEachFreqLeftChoice[cellInd,:,indf].compressed().shape[0] for indf in range(numFreqs/2)]
            fHighTrialNumsLeft = [responseEachCellEachFreqLeftChoice[cellInd,:,indf].compressed().shape[0] for indf in range(numFreqs/2,numFreqs)]
            #pdb.set_trace()
            fLowNewTrialNumsLeft = behavioranalysis.equalized_trial_count(np.array(fLowTrialNumsLeft), fraction)
            fHighNewTrialNumsLeft = behavioranalysis.equalized_trial_count(np.array(fHighTrialNumsLeft), fraction)
            for indf in range(numFreqs/2):
                fLowLeftThisFreqAllTrials = responseEachCellEachFreqLeftChoice[cellInd,:,indf].compressed()
                random.shuffle(fLowLeftThisFreqAllTrials)
                fLowLeftThisFreqSampled = fLowLeftThisFreqAllTrials[:fLowNewTrialNumsLeft[indf]] 
                fLowLeft = np.append(fLowLeft, fLowLeftThisFreqSampled)

                fHighLeftThisFreqAllTrials = responseEachCellEachFreqLeftChoice[cellInd,:,indf+numFreqs/2].compressed()
                random.shuffle(fHighLeftThisFreqAllTrials)
                fHighLeftThisFreqSampled = fHighLeftThisFreqAllTrials[:fHighNewTrialNumsLeft[indf]] 
                fHighLeft = np.append(fHighLeft, fHighLeftThisFreqSampled)

        zScoreLeft,pValLeft = stats.ranksums(fLowLeft, fHighLeft)
        pValsLeft = np.append(pValsLeft,pValLeft)
        if (np.mean(fHighLeft)+np.mean(fLowLeft))==0:
            selectivityIndexThisCell = 0
        else:
            selectivityIndexThisCell = (np.mean(fHighLeft)-np.mean(fLowLeft)) / (np.mean(fHighLeft)+np.mean(fLowLeft))
        selectivityIndsLeft = np.append(selectivityIndsLeft, selectivityIndexThisCell)

        if not subsample:
            fLowRight = responseEachCellEachFreqRightChoice[cellInd,:,:3].compressed()
            fHighRight = responseEachCellEachFreqRightChoice[cellInd,:,3:].compressed()

        else:
            fLowRight = np.array([])
            fHighRight = np.array([])
            fLowTrialNumsRight = [responseEachCellEachFreqRightChoice[cellInd,:,indf].compressed().shape[0] for indf in range(numFreqs/2)]
            fHighTrialNumsRight = [responseEachCellEachFreqRightChoice[cellInd,:,indf].compressed().shape[0] for indf in range(numFreqs/2,numFreqs)]
            fLowNewTrialNumsRight = behavioranalysis.equalized_trial_count(np.array(fLowTrialNumsRight), fraction)
            fHighNewTrialNumsRight = behavioranalysis.equalized_trial_count(np.array(fHighTrialNumsRight), fraction)
            for indf in range(numFreqs/2):
                fLowRightThisFreqAllTrials = responseEachCellEachFreqRightChoice[cellInd,:,indf].compressed()
                random.shuffle(fLowRightThisFreqAllTrials)
                fLowRightThisFreqSampled = fLowRightThisFreqAllTrials[:fLowNewTrialNumsRight[indf]] 
                fLowRight = np.append(fLowRight, fLowRightThisFreqSampled)

                fHighRightThisFreqAllTrials = responseEachCellEachFreqRightChoice[cellInd,:,indf+numFreqs/2].compressed()
                random.shuffle(fHighRightThisFreqAllTrials)
                fHighRightThisFreqSampled = fHighRightThisFreqAllTrials[:fHighNewTrialNumsRight[indf]] 
                fHighRight = np.append(fHighRight, fHighRightThisFreqSampled)

        zScoreRight,pValRight = stats.ranksums(fLowRight, fHighRight)
        pValsRight = np.append(pValsRight,pValRight)
        if (np.mean(fHighRight)+np.mean(fLowRight))==0:
            selectivityIndexThisCell = 0
        else:
            selectivityIndexThisCell = (np.mean(fHighRight)-np.mean(fLowRight)) / (np.mean(fHighRight)+np.mean(fLowRight))
        selectivityIndsRight = np.append(selectivityIndsRight, selectivityIndexThisCell)


    #freqSelective = (pValsBoth <= 0.05)
    #numFreqSelCells = sum(freqSelective.astype(int))
    #print 100*float(numFreqSelCells)/numCells, '%', numFreqSelCells, 'out of', numCells, ' cells in 2afc psycurve task show different response to high and low frequencies.'

    nansInData = np.isnan(selectivityIndsLeft)
    if np.any(nansInData):
        print '*** WARNING! *** I found NaN in some elements of selectivity index. I will replace with zero.'
        selectivityIndsLeft[nansInData] = 0
    print('Left choice: high vs low selectivity index is {:.3f} +/- {:.3f}'.format(np.mean(selectivityIndsLeft),np.std(selectivityIndsLeft)))
    # -- There are some modulation index with values of 1 or -1 due to lack of spikes in the trials of either high or low freq -- #
    #selectivityIndsLeft[(selectivityIndsLeft == 1)|(selectivityIndsLeft == -1)] = 0

    freqSelectiveLeftChoice = (pValsLeft <= 0.05)

    nansInData = np.isnan(selectivityIndsRight)
    if np.any(nansInData):
        print '*** WARNING! *** I found NaN in some elements of selectivity index. I will replace with zero.'
        selectivityIndsRight[nansInData] = 0
    print('Right choice: high vs low selectivity index is {:.3f} +/- {:.3f}'.format(np.mean(selectivityIndsRight),np.std(selectivityIndsRight)))
    # -- There are some modulation index with values of 1 or -1 due to lack of spikes in the trials of either high or low freq -- #
    #selectivityIndsRight[(selectivityIndsRight == 1)|(selectivityIndsRight == -1)] = 0

    freqSelectiveRightChoice = (pValsRight <= 0.05)

    # -- Statistic test comparing frequency selectivity vs (premovement) choice selectivity  -- #
    if not subsample:
        FIGNAME = 'premovement_modulation_psychometric'
        choiceModDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
        choiceModsummaryFilename = 'summary_psychometric_premovement_modulation_all_good_cells_remove_dup.npz'
        choiceModsummaryFullPath = os.path.join(choiceModDataDir,choiceModsummaryFilename)
        choiceModsummary = np.load(choiceModsummaryFullPath)
        choiceModI = choiceModsummary['modulationIndex']
        choiceModulated = choiceModsummary['modulated']
    
        if np.any(np.isnan(choiceModI)):
            print 'Detected NaN in modulation index, will replace with 0 for now.'
            choiceModI[np.isnan(choiceModI)] = 0
        # -- There are some modulation index with values of 1 or -1 due to lack of spikes in the trials going one direction (only one center freq trials were included, sometimes very few trials going to one direction) -- #
        #choiceModI[(choiceModI == 1)|(choiceModI == -1)] = 0
        print('Mid freq: left vs right choice modulation index is {:.3f} +/- {:.3f}'.format(np.mean(choiceModI), np.std(choiceModI)))
        Zscore, pValSvC = stats.kruskal(choiceModI, selectivityIndsLeft, selectivityIndsRight)
        ZscoreLvC, pValSvCLeft = stats.ranksums(choiceModI, selectivityIndsLeft)
        ZscoreRvC, pValSvCRight = stats.ranksums(choiceModI, selectivityIndsRight)
        print('Using Kruskal-Wallis H-test to compare choice modulation vs high/low freq selectivity, p = {:.3f}'.format(pValSvC))
        print('Using wilcoxon rank sum test to compare choice modulation vs high/low freq selectivity: for all left-choice trials, p = {:.3f}, for all right-choice trials, p = {:.3f} '.format(pValSvCLeft, pValSvCRight))
    ####################################################3
    numFreqSelCellsLeft = sum(freqSelectiveLeftChoice.astype(int))
    percentFreqSelLeft = 100*float(numFreqSelCellsLeft)/numCells
    if not subsample:
        print 'Using all trials with left choice,', percentFreqSelLeft, '%', numFreqSelCellsLeft, 'out of', numCells, ' cells in 2afc psycurve task show different response to high and low frequencies.'
    else:
       print 'Using {:.3f}% of trials with left choice,'.format(fraction*100), percentFreqSelLeft, '%', numFreqSelCellsLeft, 'out of', numCells, ' cells in 2afc psycurve task show different response to high and low frequencies.' 

    numFreqSelCellsRight = sum(freqSelectiveRightChoice.astype(int))
    percentFreqSelRight = 100*float(numFreqSelCellsRight)/numCells
    if not subsample:
        print 'Using all trials with right choice,', percentFreqSelRight, '%', numFreqSelCellsRight, 'out of', numCells, ' cells in 2afc psycurve task show different response to high and low frequencies.'
    else:
        print 'Using {:.3f}% of trials with right choice,'.format(fraction*100), percentFreqSelRight, '%', numFreqSelCellsRight, 'out of', numCells, ' cells in 2afc psycurve task show different response to high and low frequencies.'
    
    percentFreqSelLeftSamples[inds] = percentFreqSelLeft
    percentFreqSelRightSamples[inds] = percentFreqSelRight

if subsample:
    avePercentFreqSelLeft = np.mean(percentFreqSelLeftSamples)
    avePercentFreqSelRight = np.mean(percentFreqSelRightSamples)
    print('After {} samplings, on average {:.3f}% of cells were significantly frequency selective using {:.3f}% of trials with left choice; on average {:.3f}% of cells were significantly frequency selective using {:.3f}% of trials with right choice.'.format(repeatedSamples, avePercentFreqSelLeft, 100*fraction, avePercentFreqSelRight, 100*fraction))


if not subsample:  
    binsEdges = np.linspace(-1,1,20)
    plt.clf()
    plt.subplot(1,3,1)
    plt.hist([selectivityIndsLeft[freqSelectiveLeftChoice],selectivityIndsLeft[~freqSelectiveLeftChoice]], color=['k','darkgrey'], edgecolor='None', stacked=True, bins=binsEdges)
    plt.xlabel('High vs low frequency selectivity')
    plt.ylabel('Number of cells')
    if not subsample:
        plt.title('All trials with left choice')
    else:
        plt.title('{:.3f}% of trials with left choice'.format(fraction*100))

    plt.subplot(1,3,2)
    plt.hist([selectivityIndsRight[freqSelectiveRightChoice],selectivityIndsRight[~freqSelectiveRightChoice]], color=['k','darkgrey'], edgecolor='None', stacked=True, bins=binsEdges)
    plt.xlabel('High vs low frequency selectivity')
    plt.ylabel('Number of cells')
    if not subsample:
        plt.title('All trials with right choice')
    else:
        plt.title('{:.3f}% of trials with right choice'.format(fraction*100))
    
    plt.subplot(1,3,3)
    plt.hist([choiceModI[choiceModulated],choiceModI[~choiceModulated]], color=['k','darkgrey'], edgecolor='None', stacked=True, bins=binsEdges)
    plt.xlabel('choice modulation')
    plt.ylabel('Number of cells')
    plt.title('All trials with mid freq')
    
    plt.show()

