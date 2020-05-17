'''
Load ephys and save spikes aligned to events of interest (sound, center-out, etc).
This make further analysis much more efficient.

We also save the missingTrials from behavior, so we can remove them during analysis.

Based on calculate_reward_modulation_celldb.py

In Santiago's computer, it took: 1690 sec (28 min) to do the 716 cells that pass criteria.

'''


import time
import numpy as np
import sys, os
import pandas as pd
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import ephyscore
from jaratoolbox import celldatabase
import figparams

recalculate = False

processedDataDir = '/var/tmp/processed_data'
processedDate = time.strftime("%Y-%m-%d")
zeroTime = time.time() # For profiling

soundChannelType = 'stim'

# -- Time range for to calculate spikeTimesFromEventOnset --
timeRange = [-0.5,0.5] # In seconds. It should span all the possible count time ranges for generating spike count matrix.

# -- Conditions for aligning spikes --
#conditions = [('sound', [-0.1,0]), ('sound', [0,0.1]), ('center-out', [0,0.3])]
conditions = ['sound', 'center-out']

# -- Load database --
databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
celldb = celldatabase.load_hdf(databaseFullPath)
cellsToProcess = celldb.query("keepAfterDupTest==1 and cellInTargetArea==1")
nCells = len(cellsToProcess)
    
for indc,cellrow in cellsToProcess.iterrows():

    # -- Test individual cells --
    #indc,cellrow = celldatabase.find_cell(celldb, 'gosi008', '2017-03-17', 940, 1, 4)
    #indc,cellrow = celldatabase.find_cell(celldb, 'adap071', '2017-09-18', 1100, 6, 2)
    
    print('\nCell {0} [{1}] : Elapsed time: {2:0.2f}s'.format(indc,cellrow['index'],time.time()-zeroTime))
    sys.stdout.flush()

    #print('MESSAGE. Elapsed time: {:0.2f}s'.format(time.time()-zeroTime)); sys.stdout.flush()

    # -- Load behavior and ephys data for this cell --
    cellObj = ephyscore.Cell(cellrow)
    sessiontype = 'behavior'
    sessionInd = cellObj.get_session_inds(sessiontype)[0]
    ###assert len(sessionInds)==1  # There should only be one behavior session
    bdata = cellObj.load_behavior_by_index(sessionInd)
    ephysData = cellObj.load_ephys_by_index(sessionInd)

    spikeTimestamps = ephysData['spikeTimes']
    eventsDict = ephysData['events']
    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
    soundOnsetTimeBehav = bdata['timeTarget']
    
    # -- Find missing trials --
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    if len(missingTrials)>0:
        print('Missing trials: {}'.format(str(missingTrials)))
        bdata.remove_trials(missingTrials) # This modifies all fields of bdata in place

    soundOnsetTimeBehavNew = bdata['timeTarget'] # After removing missing trials from bdata
    if len(soundOnsetTimeBehavNew) != len(soundOnsetTimeEphys):
        # If for some reason cannot make behav and ephys have same amount of trials, skip this cell
        print 'Number of trials differs between behav and ephys (even after fix) in session {}'.format(cellrow.date)
        continue

    # -- Align spikes to different events --
    for alignment in conditions:
        if alignment == 'sound':
            EventOnsetTimes = soundOnsetTimeEphys
        elif alignment == 'center-out':
            diffTimes = bdata['timeCenterOut']-bdata['timeTarget']
            EventOnsetTimes = soundOnsetTimeEphys + diffTimes
        elif alignment == 'side-in':
            diffTimes = bdata['timeSideIn']-bdata['timeTarget']
            EventOnsetTimes = soundOnsetTimeEphys + diffTimes
        outputFile = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(cellrow.subject, cellrow.date, cellrow.depth,
                                                            cellrow.tetrode, cellrow.cluster, alignment)
        outputFullPath = os.path.join(processedDataDir,outputFile)

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
             spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)

        #---- Save intermediate results somewhere, next time can just load it ----
        np.savez(outputFullPath, spikeTimesFromEventOnset=spikeTimesFromEventOnset,
                 trialIndexForEachSpike=trialIndexForEachSpike,
                 indexLimitsEachTrial=indexLimitsEachTrial,
                 missingTrials=missingTrials,
                 timeRange=timeRange, alignment=alignment)
        print 'Saved event-locked data to {0}'.format(outputFullPath)


