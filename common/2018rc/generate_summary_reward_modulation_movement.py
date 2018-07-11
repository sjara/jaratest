'''
Generate and store summary data for reward modulation index during movement for astr or ac in reward-change task. 

Lan Guo 20180221
'''
import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import celldatabase
import figparams
reload(figparams)

STUDY_NAME = figparams.STUDY_NAME

FIGNAME = 'reward_modulation_movement'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

####################################################################################
scriptFullPath = os.path.realpath(__file__)
brainAreas = ['rightAC','rightAStr']
#maxZThreshold = 3
alphaLevel = 0.05
movementSelWindow = [0.05, 0.15] #[0.05, 0.25]
modWindow = '0.05-0.25s' #'0.05-0.15s'
###################################################################################
#dbKey = 'reward_change'
dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)

for brainArea in brainAreas:
    goodQualCells = celldb.query("keepAfterDupTest==1 and brainArea=='{}'".format(brainArea))

    movementSelective = goodQualCells['movementModS_{}'.format(movementSelWindow)] < alphaLevel
    moreRespMoveLeft = movementSelective & (goodQualCells['movementModI_{}'.format(movementSelWindow)] < 0)
    moreRespMoveRight = movementSelective & (goodQualCells['movementModI_{}'.format(movementSelWindow)] > 0)
    goodLeftMovementSelCells = goodQualCells[moreRespMoveLeft]
    goodRightMovementSelCells = goodQualCells[moreRespMoveRight]

    leftModIndName = 'modIndLow_'+modWindow+'_'+'center-out'
    leftModSigName = 'modSigLow_'+modWindow+'_'+'center-out'
    leftModDirName = 'modDirLow_'+modWindow+'_'+'center-out'
    rightModIndName = 'modIndHigh_'+modWindow+'_'+'center-out'
    rightModSigName = 'modSigHigh_'+modWindow+'_'+'center-out'
    rightModDirName = 'modDirHigh_'+modWindow+'_'+'center-out'
     
    goodMovementSelCells = goodQualCells[movementSelective]
    sigModEitherDirection = (goodMovementSelCells[leftModSigName] < alphaLevel) | (goodMovementSelCells[rightModSigName] < alphaLevel)  
    print 'Out of {} movement-selective cells, {} were modulated by reward either going left or going right'.format(len(goodMovementSelCells), sum(sigModEitherDirection))
    goodLeftMovementSelModInd = (-1) * goodLeftMovementSelCells[leftModIndName]
    goodLeftMovementSelModSig = goodLeftMovementSelCells[leftModSigName]
    goodLeftMovementSelModDir = goodLeftMovementSelCells[leftModDirName]
    goodRightMovementSelModInd = goodRightMovementSelCells[rightModIndName]
    goodRightMovementSelModSig = goodRightMovementSelCells[rightModSigName]
    goodRightMovementSelModDir = goodRightMovementSelCells[rightModDirName]
    
    sigModulatedLeft = (goodLeftMovementSelModSig < alphaLevel) & (goodLeftMovementSelModDir > 0)
    sigModulatedRight = (goodRightMovementSelModSig < alphaLevel) & (goodRightMovementSelModDir > 0)
    sigModI = np.concatenate((goodLeftMovementSelModInd[sigModulatedLeft].values,
                                      goodRightMovementSelModInd[sigModulatedRight].values))
    nonsigModI = np.concatenate((goodLeftMovementSelModInd[~sigModulatedLeft].values,
                                         goodRightMovementSelModInd[~sigModulatedRight].values))
    allModI = np.concatenate((goodLeftMovementSelModInd.values, goodRightMovementSelModInd.values))
    
    # -- Save summary data -- #    
    outputFile = 'summary_reward_modulation_movement_{}.npz'.format(brainArea)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, brainArea=brainArea, movementSelective=movementSelective, goodLeftMovementSelCells=goodLeftMovementSelCells, goodRightMovementSelCells=goodRightMovementSelCells, sigModulatedLeft=sigModulatedLeft, sigModulatedRight=sigModulatedRight, sigModI=sigModI, nonsigModI=nonsigModI, allModI=allModI, script=scriptFullPath)
