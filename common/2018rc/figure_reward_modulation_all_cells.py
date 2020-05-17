'''
Show the reward modulation (during sound and movement) for all cells, not just sound-responsive or choice-selective.
'''

import sys, os
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import celldatabase
from matplotlib import pyplot as plt
from jaratoolbox import extraplots
import figparams

PLOT_RESULTS = 0

STUDY_NAME = figparams.STUDY_NAME

alphaLevel = 0.05

databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
celldb = celldatabase.load_hdf(databaseFullPath)
goodCells = celldb.query("keepAfterDupTest==1 and cellInTargetArea==1")# 716 total
#goodCells = celldb.query("missingTrialsBehav==0 and keepAfterDupTest==1 and cellInTargetArea==1")# 700 total
# Note that originally we said 414 AC and 312 pStr, but 16 cells are excluded because missingTrialsBehav==1

soundResponsive = goodCells.behavPval.apply(lambda x: np.min(x[~np.isnan(x)]) < (alphaLevel/2)) # 297 (159+138)
choiceSelective = goodCells['movementModS_[0.0, 0.3]_removedsidein']<alphaLevel # 312 total (169+143)
if 1:
    nonSoundResponsiveCells = goodCells[~soundResponsive]
    nonChoiceSelectiveCells = goodCells[~choiceSelective]
    selectedLabel = '(Non reponsive/selective)'
else:
    nonSoundResponsiveCells = goodCells[soundResponsive]
    nonChoiceSelectiveCells = goodCells[choiceSelective]
    selectedLabel = '(Reponsive/selective)'


brainAreas = ['rightAC','rightAStr']

plt.clf()
for inda,brainArea in enumerate(brainAreas):
    #cellsThisArea = goodCells.query("brainArea=='{}'".format(brainArea))
    cellsThisArea = nonSoundResponsiveCells.query("brainArea=='{}'".format(brainArea))
    nCells = len(cellsThisArea)
    
    # =========== During sound =============
    modSigLowSound = cellsThisArea['modSigLow_0-0.1s_sound']
    modSigHighSound = cellsThisArea['modSigHigh_0-0.1s_sound']
    modIndLowSound = cellsThisArea['modIndLow_0-0.1s_sound']
    modIndHighSound = cellsThisArea['modIndHigh_0-0.1s_sound']
    modDirLowSound = cellsThisArea['modDirLow_0-0.1s_sound']
    modDirHighSound = cellsThisArea['modDirHigh_0-0.1s_sound']

    nSignifLow = np.sum((modSigLowSound<alphaLevel) & modDirLowSound)
    nSignifHigh = np.sum((modSigHighSound<alphaLevel) & modDirHighSound)
    fractionSignifLow = np.mean((modSigLowSound<alphaLevel) & modDirLowSound)
    fractionSignifHigh = np.mean((modSigHighSound<alphaLevel) & modDirHighSound)
    fractionAND = np.mean( ((modSigLowSound<alphaLevel) & modDirLowSound) & ((modSigHighSound<alphaLevel) & modDirHighSound) )
    fractionOR = np.mean( ((modSigLowSound<alphaLevel) & modDirLowSound) | ((modSigHighSound<alphaLevel) & modDirHighSound) )
    
    print('==== {} during SOUND {} ===='.format(brainArea,selectedLabel))
    print('modIndLow: {:0.1%} {}/{}   {} +/- {}'.format(fractionSignifLow, nSignifLow, nCells, np.mean(modIndLowSound), np.std(modIndLowSound)))
    print('modIndHigh: {:0.1%} {}/{}   {} +/- {}'.format(fractionSignifHigh, nSignifHigh, nCells, np.mean(modIndHighSound), np.std(modIndHighSound)))
    print('modInd_AND: {:0.1%}'.format(fractionAND))
    print('modInd_OR: {:0.1%}'.format(fractionOR))
    print('\n')

    if PLOT_RESULTS:
        plt.subplot(2,1,inda+1)
        plt.hist(np.concatenate((modIndLowMove,modIndHighMove)),50)
        plt.xlim([-1,1])
        

    # =========== During movement =============
    cellsThisArea = nonChoiceSelectiveCells.query("brainArea=='{}'".format(brainArea))

    modSigLowMove = cellsThisArea['modSigLow_0-0.3s_center-out_removedsidein']
    modSigHighMove = cellsThisArea['modSigHigh_0-0.3s_center-out_removedsidein']
    modIndLowMove = cellsThisArea['modIndLow_0-0.3s_center-out_removedsidein']
    modIndHighMove = cellsThisArea['modIndHigh_0-0.3s_center-out_removedsidein']
    modDirLowMove = cellsThisArea['modDirLow_0-0.3s_center-out_removedsidein']
    modDirHighMove = cellsThisArea['modDirHigh_0-0.3s_center-out_removedsidein']

    nSignifLow = np.sum((modSigLowMove<alphaLevel) & modDirLowMove)
    nSignifHigh = np.sum((modSigHighMove<alphaLevel) & modDirHighMove)
    fractionSignifLow = np.mean((modSigLowMove<alphaLevel) & modDirLowMove)
    fractionSignifHigh = np.mean((modSigHighMove<alphaLevel) & modDirHighMove)
    fractionAND = np.mean( ((modSigLowMove<alphaLevel) & modDirLowMove) & ((modSigHighMove<alphaLevel) & modDirHighMove) )
    fractionOR = np.mean( ((modSigLowMove<alphaLevel) & modDirLowMove) | ((modSigHighMove<alphaLevel) & modDirHighMove) )
    
    print('==== {} during MOVEMENT {} ===='.format(brainArea,selectedLabel))
    print('modIndLow: {:0.1%} {}/{}   {} +/- {}'.format(fractionSignifLow, nSignifLow, nCells, np.mean(modIndLowMove), np.std(modIndLowMove)))
    print('modIndHigh: {:0.1%} {}/{}   {} +/- {}'.format(fractionSignifHigh, nSignifHigh, nCells, np.mean(modIndHighMove), np.std(modIndHighMove)))
    print('modInd_AND: {:0.1%}'.format(fractionAND))
    print('modInd_OR: {:0.1%}'.format(fractionOR))
    print('\n')

    if PLOT_RESULTS:
        plt.subplot(2,1,inda+1)
        plt.hist(np.concatenate((modIndLowMove,modIndHighMove)),50)
        plt.xlim([-1,1])

