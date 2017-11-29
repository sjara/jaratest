import os
import numpy as np
import pandas as pd
from jaratoolbox import settings

brainRegions = ['ac', 'astr']
mouseNameList = [['gosi001','gosi004','gosi008','gosi010','adap071','adap067'],['adap005','adap012','adap013','adap015','adap017']]
for region,mouseNameList in zip(brainRegions,mouseNameList):
    allMiceDfs = []
    for mouseName in mouseNameList:
        databaseFullPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(mouseName))
        dfThisMouse = pd.read_hdf(databaseFullPath,key='reward_change')
        '''
        outFilePath = '/var/tmp/{}_reward_change_modulation_2.h5'.format(mouseName)
        dfModThisMouse = pd.read_hdf(outFilePath, key='reward_change')
        if set(list(dfModThisMouse)).issubset(list(dfThisMouse)):
            allMiceDfs.append(dfThisMouse)
            continue
        else:
            dfs = [dfThisMouse,dfModThisMouse]
            dfAllThisMouse = reduce(lambda left,right: pd.merge(left,right,on=['subject','date','tetrode','cluster'],how='inner'), dfs)
            #dfAllThisMouse.drop('level_0', 1, inplace=True)
            dfAllThisMouse.to_hdf(databaseFullPath, key='reward_change')
            allMiceDfs.append(dfAllThisMouse)
        '''
        allMiceDfs.append(dfThisMouse)
    dfAllReward_ChangeMouse = pd.concat(allMiceDfs, ignore_index=True)
    dfAllReward_ChangeMouse.drop('level_0', 1, inplace=True)
    # To make sure there are not duplicates
    dfAllReward_ChangeMouse.drop_duplicates(['subject','date','tetrode','cluster','indSite','indExperiment'], inplace=True)
    dfAllReward_ChangeMouse.reset_index(inplace=True)
    dfAllReward_ChangeMouse.to_hdf(os.path.join(settings.DATABASE_PATH, 'reward_change_{}.h5'.format(region)), key='reward_change')
    #when saving to hdf, using (format='table',data_columns=True) is slower but enable on disk queries
