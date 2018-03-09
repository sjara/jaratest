'''
This script copies and renames intermediate event-locked spiketime data on jarastation4 for all cells in the reward change cell database. If data for a cell doesn't exist, then calculates and saves the intermediate data.
'''
import os
import shutil
import numpy as np
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import loadbehavior
reload(ephyscore)
import new_reward_change_plotter_functions as rcfuncs



def save_evlock_spktimes_cell(cell, sessiontype, alignment, timeRange, recalculate, oldOutputDir, newOutputDir):
    '''
    :param arg1: Cell object from jaratoolbox.ephyscore.
    :param arg2: A string indicating the type of recording session to process.
    :param arg3: A string indicating the event to align the spike times to, can be 'sound', 'center-out', or 'side-in'.
    :param arg4: A list of floats for the start and the end of the time period around sound-onset to plot raster.
    :param arg5: A boolean value indicating whether to calculate from scratch.
    :param arg6: A string for old output directory.
    :param arg7: A string for new output directory.
    '''
    subject = cell.dbRow['sudbject']
    depth = cell.dbRow['depth']
    oldOutputFile = 'eventlocked_{0}_{1}_T{2}c{3}_{4}.npz'.format(subject, cell.date, cell.tetrode, cell.cluster, alignment)
    oldOutputFullPath = os.path.join(oldOutputDir,oldOutputFile)
    newOutputFile = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(subject, cell.date, depth, cell.tetrode, cell.cluster, alignment)
    newOutputFullPath = os.path.join(newOutputDir,newOutputFile)
    if os.path.isfile(oldOutputFullPath) and not recalculate:
        #copy to new dir with new name
        shutil.copyfile(oldOutputFullPath, newOutputFullPath)
        print 'Copying event-locked data to {0}'.format(newOutputFullPath)
    else:
        spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = rcfuncs.calculate_intermediate_data_for_raster_psth(cell, alignment, timeRange, behavClass=loadbehavior.FlexCategBehaviorData) 
        np.savez(newOutputFullPath, spikeTimesFromEventOnset=spikeTimesFromEventOnset, trialIndexForEachSpike=trialIndexForEachSpike, indexLimitsEachTrial=indexLimitsEachTrial, timeRange=timeRange, alignment=alignment)
        print 'Saved event-locked data to {0}'.format(newOutputFullPath)



sessiontype = 'behavior' #2afc behavior
recalculate = False
timeRange = [-0.5,0.5] # In seconds. Time range for to calculate spikeTimesFromEventOnset, this time window has to span all the possible count time ranges for generating spike count matrix

newOutputDir = '/home/languo/data/ephys/evlock_spktimes'
oldOutputDir = '/var/tmp/processed_data'

dbKey = 'reward_change'
NEW_DATABASE_FOLDER = 'new_celldb'
databaseFullPath = os.path.join(settings.DATABASE_PATH, NEW_DATABASE_FOLDER, 'rc_database.h5')
cellDb = pd.read_hdf(databaseFullPath, key=dbKey)

alignments = ['sound', 'center-out', 'side-in']

for ind,cell in cellDb.iterrows():
    cellObj = ephyscore.Cell(cell)
    for alignment in alignments:
        save_evlock_spktimes_cell(cellObj, sessiontype, alignment, timeRange, recalculate, oldOutputDir, newOutputDir)
