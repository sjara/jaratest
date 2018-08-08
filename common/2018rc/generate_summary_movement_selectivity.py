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
movementWindow = [0.0, 0.3] #[0.05, 0.15] # in seconds
removeSideIn = True
###################################################################################
#dbKey = 'reward_change'
dbFolder = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME)
celldbPath = os.path.join(dbFolder, 'rc_database.h5')
celldb = celldatabase.load_hdf(celldbPath)

for brainArea in brainAreas:
    goodQualCells = celldb.query("keepAfterDupTest==1 and brainArea=='{}'".format(brainArea))

    if removeSideIn:
        movementModI = goodQualCells['movementModI_{}_removedsidein'.format(movementWindow)]
        movementModS = goodQualCells['movementModS_{}_removedsidein'.format(movementWindow)]
        encodeMv = (goodQualCells['movementSelective_moredif_Mv'] + goodQualCells['movementSelective_samedif_MvSd']).astype(bool)
        encodeSd =  goodQualCells['movementSelective_moredif_Sd'].astype(bool) 
    else:
        movementModI = goodQualCells['movementModI_{}'.format(movementWindow)]
        movementModS = goodQualCells['movementModS_{}'.format(movementWindow)]
    
    sigMovSel = (movementModS < alphaLevel) 
    sigModI = movementModI[sigMovSel]
    nonsigModI = movementModI[~sigMovSel]

    allModIEncodeMv = movementModI[encodeMv]
    sigModIEncodeMv = sigModI[encodeMv]
    nonsigModIEncodeMv = nonsigModI[encodeMv]
   
    allModIEncodeSd = movementModI[encodeSd]
    sigModIEncodeSd = sigModI[encodeSd]
    nonsigModIEncodeSd = nonsigModI[encodeSd]

    # -- Save summary data -- #
    if removeSideIn:
        outputFile = 'summary_rc_movement_selectivity_{}_removed_sidein_trials.npz'.format(brainArea)
    else:    
        outputFile = 'summary_rc_movement_selectivity_{}.npz'.format(brainArea)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, brainArea=brainArea, 
        sigModI=sigModI, nonsigModI=nonsigModI, allModI=movementModI, 
        sigModIEncodeMv=sigModIEncodeMv, nonsigModIEncodeMv=nonsigModIEncodeMv, allModIEncodeMv=allModIEncodeMv, 
        sigModIEncodeSd=sigModIEncodeSd, nonsigModIEncodeSd=nonsigModIEncodeSd, allModIEncodeSd=allModIEncodeSd, 
        script=scriptFullPath)
