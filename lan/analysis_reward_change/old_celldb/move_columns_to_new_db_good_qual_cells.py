import os
import pandas as pd
import numpy as np
from jaratoolbox import settings

animalList = ['adap071'] #'adap012', 'adap013', 'adap015', 'adap017','gosi001','gosi004', 'gosi008','gosi010','adap067',


oldDbFolder = os.path.join(settings.DATABASE_PATH)
newDbFolder = os.path.join(settings.DATABASE_PATH, 'new_celldb')

dbKey = 'reward_change'

qualityThreshold = 3 
maxZThreshold = 3
ISIcutoff = 0.02


for animal in animalList:
    oldDb = pd.read_hdf(os.path.join(oldDbFolder, '{}_database.h5'.format(animal)), key=dbKey)
    newDb = pd.read_hdf(os.path.join(newDbFolder, '{}_database.h5'.format(animal)), key=dbKey) #new db only contain 'good qual' cells (before consistency check and duplicate check)

    oldGoodQualCells = oldDb.query('isiViolations<{} and shapeQuality>{} and inTargetArea==True and met_behav_criteria_strict==True'.format(ISIcutoff, qualityThreshold))
    
    assert np.all(oldGoodQualCells.index == newDb.index)
    consistencyCheck = oldGoodQualCells['consistentInFiring']
    newDb['consistentFiring'] = consistencyCheck
    duplicateCheck = oldGoodQualCells['keep_after_dup_test']
    newDb['keepAfterDupTest'] = duplicateCheck

    rewardModColumnNames = [col for col in oldGoodQualCells.columns if ('modInd' in col) or ('modSig' in col)] 
    for colName in rewardModColumnNames:
        newDb[colName] = oldGoodQualCells[colName]
        
    # -- Save just the cells that met all good quality criteria -- # 
    newGoodDb = newDb.query('isiViolations<{} and spikeShapeQuality>{} and inTargetArea==True and metBehavCriteria==True and consistentFiring==True and keepAfterDupTest==True'.format(ISIcutoff, qualityThreshold))
    newGoodDb.to_hdf(os.path.join(newDbFolder, '{}_database.h5'.format(animal)), key=dbKey)
