'''
Generate and store summary data for movement selectivity index for astr or ac in reward-change task. 

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

FIGNAME = 'movement_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

####################################################################################
scriptFullPath = os.path.realpath(__file__)
brainAreas = ['rightAC','rightAStr']
maxZThreshold = 3
alphaLevel = 0.05
numFreqs = 2
movementWindow = [0.0, 0.3] #[0.05, 0.15] # in seconds
removeSideIn = True
###################################################################################
#dbKey = 'reward_change'
dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)

for brainArea in brainAreas:
    goodQualCells = celldb.query("keepAfterDupTest==1 and brainArea=='{}'".format(brainArea))

    movementModI = goodQualCells['movementModI_{}_removedsidein'.format(movementWindow)]
    movementModS = goodQualCells['movementModS_{}_removedsidein'.format(movementWindow)]
    encodeMv = (goodQualCells['movementSelective_moredif_Mv'] + goodQualCells['movementSelective_samedif_MvSd']).astype(bool)
    # encodeSd =  goodQualCells['movementSelective_moredif_Sd'].astype(bool) 
    # zScoreRight = goodQualCells['movementZscoreRight_{}_removedsidein'.format(movementWindow)]
    # zScoreLeft = goodQualCells['movementZscoreLeft_{}_removedsidein'.format(movementWindow)]

    sigMovSel = (movementModS < alphaLevel) #& encodeMv
    # sigModI = movementModI[sigMovSel]
    # nonsigModI = movementModI[~sigMovSel]

    soundResp = goodQualCells.behavPval.apply(lambda x: np.min(x[~np.isnan(x)]) < alphaLevel / numFreqs) # Bonforroni correction for multiple comparison # The smallest of the p value is less than 0.025
    # moreRespLowFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[~np.isnan(x)][0]) > abs(x[~np.isnan(x)][-1]))
    # moreRespHighFreq = soundResp & goodQualCells.behavZscore.apply(lambda x: abs(x[~np.isnan(x)][-1]) > abs(x[~np.isnan(x)][0]))
    
    soundRespNMvSel = soundResp & sigMovSel
    numSoundRespNMvSel = sum(soundRespNMvSel)
    numSoundResp = sum(soundResp)
    numMvSel = sum(sigMovSel)

    print('{}: {} out of {} ({:.2f}%) sound responsive cells are also movement direction selective.\n'
        .format(brainArea, numSoundRespNMvSel, numSoundResp, 100*numSoundRespNMvSel/float(numSoundResp)))
    print('{}: {} out of {} ({:.2f}%)movement direction selective cells are also sound responsive.\n'
        .format(brainArea, numSoundRespNMvSel, numMvSel, 100*numSoundRespNMvSel/float(numMvSel)))

    