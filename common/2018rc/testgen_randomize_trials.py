'''
Estimate modulation after randomizing trials.
'''


import sys
import os
import numpy as np
#from scipy import stats
#from scipy import signal
from jaratoolbox import settings
from jaratoolbox import celldatabase
reload(celldatabase)
from jaratoolbox import ephyscore
#reload(ephyscore)
#from jaratoolbox import spikesanalysis
#from jaratoolbox import extraplots
import figparams
#from matplotlib import pyplot as plt


evlockDataPath = '/var/tmp/processed_data/'
#evlockDataPath = os.path.join(settings.EPHYS_PATH, figparams.STUDY_NAME, 'evlock_spktimes')

databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
#celldb = celldatabase.load_hdf(databaseFullPath)
celldb = celldatabase.load_hdf_subset(databaseFullPath,ignore=['behavSuffix','ephysTime','paradigm','sessionType'])

sys.exit()


brainAreas = ['rightAC','rightAStr']

for brainArea in brainAreas:
    goodQualCells = celldb.query("keepAfterDupTest==1 and cellInTargetArea==1 and brainArea=='{}'".format(brainArea))
    cellsToProcess = goodQualCells

    for indc,cellrow in cellsToProcess.iterrows():

        # -- Load behavior data --
        cellObj = ephyscore.Cell(cellrow)
        print('{}: {}'.format(indc,cellObj))
        sessionInds = cellObj.get_session_inds('behavior')
        assert len(sessionInds)==1  # There should only be one behavior session
        bdata = cellObj.load_behavior_by_index(sessionInds[0])
     
        # -- Load (preprocessed) ephys data --
        alignment = 'center-out'
        #evlockDataFilename = 'eventlocked_{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(cellrow.subject, cellrow.date, cellrow.depth,
        #                                                                        cellrow.tetrode, cellrow.cluster, alignment)
        evlockDataFilename = 'eventlocked_{}_{}_T{}c{}_{}.npz'.format(cellrow.subject, cellrow.date, 
                                                                       cellrow.tetrode, cellrow.cluster, alignment)
        evlockDataFullpath = os.path.join(evlockDataPath, evlockDataFilename)
        try:
            evlockSpktimes = np.load(evlockDataFullpath)
        except IOError:
            print('-- File not found: '.format(evlockDataFullpath))
            continue
        spikeTimesFromEventOnset = evlockSpktimes['spikeTimesFromEventOnset']
        indexLimitsEachTrial = evlockSpktimes['indexLimitsEachTrial']
        trialIndexForEachSpike = evlockSpktimes['trialIndexForEachSpike']
        timeRange = evlockSpktimes['timeRange']
        missingTrials = evlockSpktimes['missingTrials']
