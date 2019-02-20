'''
Addressing Rev1-Comment1
Investigate the relation between movement selectivity and reward modulation.
'''

import os
import sys
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import extraplots
import figparams
reload(figparams)

SHUFFLE_DATA = 0


FIGNAME = 'correlation_all_indexes'
# -- Data needed comes from the database --
'''
figDataFile = 'file_containing_data_for_this_fig.npz'
figDataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
figDataFullPath = os.path.join(figDataDir,figDataFile)
'''

SAVE_FIGURE = 1
outputDir = '/tmp/'
figFilename = 'correlation_all_indexes' # Do not include extension
figFormat = 'pdf' # 'pdf' or 'svg'
figSize = [7,9] # In inches

fontSizeLabels = figparams.fontSizeLabels
fontSizeTicks = figparams.fontSizeTicks
fontSizePanel = figparams.fontSizePanel

labelPosX = [0.01]   # Horiz position for panel labels
labelPosY = [0.98, 0.48]    # Vert position for panel labels
areaLabelPosX = [0.01]   # Horiz position for panel labels
areaLabelPosY = [0.79, 0.28]    # Vert position for panel labels
panelLabels = ['A','B']

scriptFullPath = os.path.realpath(__file__)
brainAreas = ['rightAC','rightAStr']
brainAreasStr = ['AC','pStr']
maxZThreshold = 3
alphaLevel = 0.05
movementWindow = [0.0, 0.3]
removeSideIn = True

movementSelWindow = [0.0,0.3]

labelRewModMove = '0-0.3s_center-out_removedsidein'
labelRewModSound = '0-0.1s_sound'
labelRewModSpont = '-0.1-0s_sound'

dbFolder = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)

#moveMod = {}
rCorr = {}
pVal = {}

# -- Plot results --
fig = plt.gcf()
fig.clf()
fig.set_facecolor('w')

#gs = gridspec.GridSpec(2, 6)
#gs.update(left=0.11, right=0.98, top=0.99, bottom=0.07, wspace=1.2, hspace=0.1)
gs = gridspec.GridSpec(2, 1)
gs.update(left=0.15, right=0.98, top=0.99, bottom=0.07, hspace=0.25)
gsInner = []
for indg in range(len(brainAreas)):
    gsInner.append(gridspec.GridSpecFromSubplotSpec(2, 3, subplot_spec=gs[indg], wspace=1, hspace=0.35))

    
pValAll = np.zeros((2,6)) # nBrainAreas, nComparisons
rCorrAll = np.zeros((2,6)) # nBrainAreas, nComparisons
                        
for inda,brainArea in enumerate(brainAreas):
    goodQualCells = celldb.query("keepAfterDupTest==1 and cellInTargetArea==1 and brainArea=='{}'".format(brainArea))
    # 404 from AC, 312 from AStr
    
    # -- Identify movement selective cells --
    if 0:
        movementSelective = goodQualCells['movementModS_{}_removedsidein'.format(movementSelWindow)] < alphaLevel
        goodQualCells = goodQualCells[movementSelective]
        print('--- USING ONLY CHOICE SELECTIVE CELLS (N={}) ---'.format(len(goodQualCells)))

    # -- Keep only neurons with some firing --
    if 1:
        avgFiringLeft = goodQualCells['movementAveFrLeft_[0.0, 0.3]_removedsidein']
        avgFiringRight = goodQualCells['movementAveFrRight_[0.0, 0.3]_removedsidein']
        #print('{}  {}'.format(avgFiringLeft,avgFiringRight))
        firingThreshold = 5
        strongFiringCells = (avgFiringLeft>firingThreshold) | (avgFiringRight>firingThreshold)
        goodQualCells = goodQualCells[strongFiringCells]
        print('--- USING STRONGLY FIRING CELLS (N={}) ---'.format(len(goodQualCells)))

    # -- Identify sound responsive cells (with Bonferroni correction) --
    if 0:
        soundResp = goodQualCells.behavPval.apply(lambda x: np.min(x[~np.isnan(x)]) < (alphaLevel/2))
        goodQualCells = goodQualCells[soundResp]
        print('--- USING ONLY SOUND RESPONSIVE CELLS (N={}) ---'.format(len(goodQualCells)))
                                              
    # -- Find choice modulation index (for good cells) --
    # Note that movementModI is calculated as (R-L)/(R+L) so it needs to be flipped to be (Contra-Ipsi)
    movementModI = goodQualCells['movementModI_{}_removedsidein'.format(movementWindow)]
    movementModS = goodQualCells['movementModS_{}_removedsidein'.format(movementWindow)]
    
    # -- Find reward modulation index during movement (for good cells) --
    leftModIndName = 'modIndLow_'+labelRewModMove
    leftModSigName = 'modSigLow_'+labelRewModMove
    leftModDirName = 'modDirLow_'+labelRewModMove
    rightModIndName = 'modIndHigh_'+labelRewModMove
    rightModSigName = 'modSigHigh_'+labelRewModMove
    rightModDirName = 'modDirHigh_'+labelRewModMove
    leftRewardModI = goodQualCells[leftModIndName]
    rightRewardModI = goodQualCells[rightModIndName]
    avgRewardModIndMove = (goodQualCells[leftModIndName]+goodQualCells[rightModIndName])/2.0

    # -- Find reward modulation index during sound (for good cells) --
    leftModIndName = 'modIndLow_'+labelRewModSound
    leftModSigName = 'modSigLow_'+labelRewModSound
    leftModDirName = 'modDirLow_'+labelRewModSound
    rightModIndName = 'modIndHigh_'+labelRewModSound
    rightModSigName = 'modSigHigh_'+labelRewModSound
    rightModDirName = 'modDirHigh_'+labelRewModSound
    leftRewardModI = goodQualCells[leftModIndName]
    rightRewardModI = goodQualCells[rightModIndName]
    avgRewardModIndSound = (goodQualCells[leftModIndName]+goodQualCells[rightModIndName])/2.0

    # -- Find reward modulation index for spont (for good cells) --
    leftModIndName = 'modIndLow_'+labelRewModSpont
    leftModSigName = 'modSigLow_'+labelRewModSpont
    leftModDirName = 'modDirLow_'+labelRewModSpont
    rightModIndName = 'modIndHigh_'+labelRewModSpont
    rightModSigName = 'modSigHigh_'+labelRewModSpont
    rightModDirName = 'modDirHigh_'+labelRewModSpont
    leftRewardModI = goodQualCells[leftModIndName]
    rightRewardModI = goodQualCells[rightModIndName]
    avgRewardModIndSpont = (goodQualCells[leftModIndName]+goodQualCells[rightModIndName])/2.0
    
    if SHUFFLE_DATA:
        #np.random.seed(0)
        movementModI = np.random.permutation(movementModI)
        avgRewardModIndMove = np.random.permutation(avgRewardModIndMove)
        avgRewardModIndSound = np.random.permutation(avgRewardModIndSound)
        avgRewardModIndSpont = np.random.permutation(avgRewardModIndSpont)
 
    allIndexesLabels = ['Choice selectivity\nindex', 'Reward mod index\n(movement)',
                        'Reward mod index\n(sound evoked)', 'Reward mod index\n(spontaneous)']
    allIndexes = [movementModI, avgRewardModIndMove,
                  avgRewardModIndSound, avgRewardModIndSpont]

    possibleComparisons = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    
    for indc, oneComp in enumerate(possibleComparisons):
        
        #rCorr[brainArea], pVal[brainArea] = stats.pearsonr( abs(allIndexes[oneComp[0]]) ,
        #                                                    abs(allIndexes[oneComp[1]]) )
        rCorr[brainArea], pVal[brainArea] = stats.spearmanr( abs(allIndexes[oneComp[0]]) ,
                                                            abs(allIndexes[oneComp[1]]) )
        print('{0} : {1} vs {2}'.format(brainArea,allIndexesLabels[oneComp[0]],allIndexesLabels[oneComp[1]]))
        print('r={:0.3f}  p={:0.5f}'.format(rCorr[brainArea],pVal[brainArea]))
        pValAll[inda,indc] = pVal[brainArea]
        rCorrAll[inda,indc] = rCorr[brainArea]

        ###### MAKE  4 x 3 grid

        thisAx = plt.subplot(gsInner[inda][indc//3,indc%3])
        #thisAx = plt.subplot(gs[inda, indc])
        ###plt.subplot(2,6,(indc+1)+inda*6)
        plt.plot( abs(allIndexes[oneComp[0]]), abs(allIndexes[oneComp[1]]), '.', color='g', alpha=1, ms=3 )
        plt.axis('square')
        plt.axis([-0.1, 0.8, -0.1, 0.8])
        #plt.axis([-0.1, 1, -0.1, 1])
        tickNumbers = np.arange(0,1,0.2)
        tickLabels = [str(tickNumbers[0])]+(len(tickNumbers)-2)*['']+[str(tickNumbers[-1])]
        plt.xticks(tickNumbers,tickLabels)
        plt.yticks(tickNumbers,tickLabels)
        extraplots.boxoff(thisAx)
        #plt.title('r={:0.2f}  p={:0.3f}'.format(rCorr[brainArea],pVal[brainArea]))
        rText = plt.text(0.3,0.5,'r = {:0.2f}\np = {:0.3f}'.format(rCorr[brainArea],pVal[brainArea]),
                         fontsize=fontSizeLabels, ha='left')
        if pVal[brainArea]<0.05:
            plt.setp(rText,fontweight='bold')
        #plt.text(0.3,0.6,'r={:0.2f}\np={:0.3f}'.format(rCorr[brainArea],pVal[brainArea]),
        #         fontsize=fontSizeLabels, ha='left')
        plt.xlabel(allIndexesLabels[oneComp[0]])
        plt.ylabel(allIndexesLabels[oneComp[1]])
    plt.gca().annotate(brainAreasStr[inda], xy=(areaLabelPosX[0],areaLabelPosY[inda]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='normal', rotation=90)
    plt.gca().annotate(panelLabels[inda], xy=(labelPosX[0],labelPosY[inda]), xycoords='figure fraction',
                       fontsize=fontSizePanel, fontweight='bold')
              
    plt.show()
    print('\n')

'''
    plt.subplot(1,2,inda+1)
    plt.plot(abs(movementModI),abs(avgRewardModI),'.')
    plt.axis('square')
    plt.title('{0} (average across sides)'.format(brainArea))
    plt.xlabel('Choice index (absolute value)')
    plt.ylabel('RewardMod index (absolute value)')
    plt.show()
'''
#hist(moveMod['rightAC'],30)
#hist(nonsigModI,30)
#plot(leftRewardModI,'.')


if SAVE_FIGURE:
    extraplots.save_figure(figFilename, figFormat, figSize, outputDir)


'''
### For shuffled
rr = []
pp = []
rr.append(rCorrAll); pp.append(pValAll)

RR = np.vstack(rr)
PP = np.vstack(pp)

np.savez('/tmp/correlations_shuffled.npz',RR=RR,PP=PP)

'''
