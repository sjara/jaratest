'''
Test the relation between factors:  sound, movement, reward on neural activity during movement.

70 seconds
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

from statsmodels.formula.api import ols
from statsmodels.graphics.api import interaction_plot, abline_plot
from statsmodels.stats.anova import anova_lm

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

movementTimeRange = [0,0.3]

minBlockSize = 30  # Minimum number of trials in a block to be analyzed
alphaLevel = 0.05
nTrialsAroundTransition = 140

goodCells = celldb.query("missingTrialsBehav==0 and keepAfterDupTest==1 and cellInTargetArea==1")

anovaAll = [[],[]]

for inda,brainArea in enumerate(brainAreas):

    ###cellsThisArea = celldb.query("brainArea=='{}'".format(brainArea)) # It reorders things in a weird way

    for indc,cellrow in goodCells.iterrows():

        # -- This is not the best way, but doing a query seems to give problems with indexes --
        if cellrow['brainArea']!=brainArea:
            continue
        
        # -- Test just one cell ---
        #indc,cellrow = celldatabase.find_cell(celldb, 'adap012', '2016-02-04', 2340.0, 3, 3)  # Reward mod
        #indc,cellrow = celldatabase.find_cell(celldb, 'adap017', '2016-04-06', 3160.0, 7, 12) # Not reward mod
        #indc,cellrow = celldatabase.find_cell(celldb, 'adap017', '2016-04-21', 3360.0, 1, 7)  # Choice-selective

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
        valid = bdata['valid'].astype(bool)
        possibleFreq = np.unique(bdata['targetFrequency'])
        numFreqs = len(possibleFreq)
        if numFreqs!=2:
            print('WARNING: more than 2 frequencies in this session')
        oneBlockType = bdata.labels['currentBlock']['more_right']

        soundFreq = (bdata['targetFrequency']==possibleFreq[-1])[valid]
        rewardContingency = (bdata['currentBlock']==oneBlockType)[valid]
        rightwardChoice = (bdata['choice']==bdata.labels['choice']['right'])[valid]

        # -- Estimate number of spikes on each trial --
        spkMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,movementTimeRange)
        spikesEachTrial = spkMat.flatten()[valid]


        tableDict = {'spikes':spikesEachTrial,'sound':soundFreq,'reward':rewardContingency,'choice':rightwardChoice}
        kt = pd.DataFrame(tableDict)

        linearModel = ols('spikes ~ C(sound) * C(choice) * C(reward)', data=kt).fit()

        anovaResults = anova_lm(linearModel)
        anovaAll[inda].append(anovaResults)

        #print(anovaResults)
        #raw_input('Press ENTER to continue...')

        # TEST PLOT
        #plt.plot(spikeTimesFromEventOnset,trialIndexForEachSpike,'.')
            
        #sys.exit()

        
#---
'''
plt.figure(figsize=(8,6))
fig = interaction_plot(kt['sound'], kt['choice'], kt['spikes'],
        colors=['red', 'blue'], markers=['D','^'], ms=10, ax=plt.gca())
plt.figure(figsize=(8,6))
fig = interaction_plot(kt['choice'], kt['sound'], kt['spikes'],
        colors=['red', 'blue'], markers=['D','^'], ms=10, ax=plt.gca())
plt.figure(figsize=(8,6))
fig = interaction_plot(kt['choice'], kt['reward'], kt['spikes'],
        colors=['red', 'blue'], markers=['D','^'], ms=10, ax=plt.gca())
plt.show()
'''

#linearModel = ols('np.log(Days+1) ~ C(Duration) * C(Weight)', data=kt).fit()


sys.exit()

anovaAll[0][0]  # [area][cell]
pSoundAC = np.array([anovaAll[0][ind]['PR(>F)'][0] for ind in range(len(anovaAll[0]))])
pChoiceAC = np.array([anovaAll[0][ind]['PR(>F)'][1] for ind in range(len(anovaAll[0]))])
pRewardAC = np.array([anovaAll[0][ind]['PR(>F)'][2] for ind in range(len(anovaAll[0]))])
pSCxAC = np.array([anovaAll[0][ind]['PR(>F)'][3] for ind in range(len(anovaAll[0]))])
pSRxAC = np.array([anovaAll[0][ind]['PR(>F)'][4] for ind in range(len(anovaAll[0]))])
pCRxAC = np.array([anovaAll[0][ind]['PR(>F)'][5] for ind in range(len(anovaAll[0]))])
pSCRxAC = np.array([anovaAll[0][ind]['PR(>F)'][6] for ind in range(len(anovaAll[0]))])

pSoundAStr = np.array([anovaAll[1][ind]['PR(>F)'][0] for ind in range(len(anovaAll[1]))])
pChoiceAStr = np.array([anovaAll[1][ind]['PR(>F)'][1] for ind in range(len(anovaAll[1]))])
pRewardAStr = np.array([anovaAll[1][ind]['PR(>F)'][2] for ind in range(len(anovaAll[1]))])
pSCxAStr = np.array([anovaAll[1][ind]['PR(>F)'][3] for ind in range(len(anovaAll[1]))])
pSRxAStr = np.array([anovaAll[1][ind]['PR(>F)'][4] for ind in range(len(anovaAll[1]))])
pCRxAStr = np.array([anovaAll[1][ind]['PR(>F)'][5] for ind in range(len(anovaAll[1]))])
pSCRxAStr = np.array([anovaAll[1][ind]['PR(>F)'][6] for ind in range(len(anovaAll[1]))])


print('AC\t  S:{:0.1%}  C:{:0.1%}  R:{:0.1%}'.format(np.mean(pSoundAC<0.05),np.mean(pChoiceAC<0.05),np.mean(pRewardAC<0.05)))
print('AStr\t  S:{:0.1%}  C:{:0.1%}  R:{:0.1%}'.format(np.mean(pSoundAStr<0.05),np.mean(pChoiceAStr<0.05),np.mean(pRewardAStr<0.05)))

print('AC\t  SC:{:0.1%}  SR:{:0.1%}  CR:{:0.1%}  SCR:{:0.1%}'.format(np.mean(pSCxAC<0.05),np.mean(pSRxAC<0.05),
                                                                     np.mean(pCRxAC<0.05),np.mean(pSCRxAC<0.05)))
print('AStr\t  SC:{:0.1%}  SR:{:0.1%}  CR:{:0.1%}  SCR:{:0.1%}'.format(np.mean(pSCxAStr<0.05),np.mean(pSRxAStr<0.05),
                                                                       np.mean(pCRxAStr<0.05),np.mean(pSCRxAStr<0.05)))

