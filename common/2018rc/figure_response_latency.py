'''
Calculate response latency of each cell. Compare between AC and AStr.

Inspired by ~/src/jaratest/common/2018thstr/generate_summary_response_latency.py

Running this scripts takes about 6 seconds (when not plotting)
'''

import sys
import os
import numpy as np
from scipy import stats
from scipy import signal
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
import figparams
from matplotlib import pyplot as plt

PLOT_LATENCY = 0

zScoreThreshold = 4

#evlockDataPath = os.path.join(settings.EPHYS_PATH, figparams.STUDY_NAME, 'evlock_spktimes')
evlockDataPath = '/var/tmp/processed_data'

databaseFullPath = os.path.join(settings.DATABASE_PATH, figparams.STUDY_NAME, 'rc_database.h5')
celldb = celldatabase.load_hdf(databaseFullPath)

timeRangeForLatency = [-0.05,0.1]

brainAreas = ['rightAC','rightAStr']
#brainAreas = ['rightAC']
latencyEachCell = {'rightAC':[], 'rightAStr':[]}

for brainArea in brainAreas:
    goodQualCells = celldb.query("missingTrialsBehav==0 and keepAfterDupTest==1 and cellInTargetArea==1 and brainArea=='{}'".format(brainArea))
    alphaLevel = 0.05
    soundResp = goodQualCells.behavPval.apply(lambda x: np.min(x[~np.isnan(x)]) < (alphaLevel/2))

    soundRespCells = goodQualCells.loc[soundResp]
    maxSoundZscore = goodQualCells.behavZscore.apply(lambda x: np.nanmax(x))
    prefFreqInd = soundRespCells.behavZscore.apply(lambda x: np.nanargmax(x))

    if PLOT_LATENCY:
        plt.clf()
        plt.hold(False)
        plt.show()

    for indc,cellrow in soundRespCells.iterrows():

        if maxSoundZscore.loc[indc] < zScoreThreshold:
            print('IGNORED: z-score for sounds response below {}'.format(zScoreThreshold))
            continue

        # -- Load (preprocessed) ephys data --
        alignment = 'sound'
        evlockDataFilename = '{0}_{1}_{2}_T{3}_c{4}_{5}.npz'.format(cellrow.subject, cellrow.date, cellrow.depth,
                                                                    cellrow.tetrode, cellrow.cluster, alignment)
        evlockDataFullpath = os.path.join(evlockDataPath, evlockDataFilename) 
        evlockSpktimes = np.load(evlockDataFullpath)
        spikeTimesFromEventOnset = evlockSpktimes['spikeTimesFromEventOnset']
        indexLimitsEachTrial = evlockSpktimes['indexLimitsEachTrial']
        trialIndexForEachSpike = evlockSpktimes['trialIndexForEachSpike']
        timeRange = evlockSpktimes['timeRange']
        missingTrials = evlockSpktimes['missingTrials']
        
        # -- Load behavior data --
        cellObj = ephyscore.Cell(cellrow)
        sessionInd = cellObj.get_session_inds('behavior')[0]
        bdata = cellObj.load_behavior_by_index(sessionInd)

        # -- Remove missing trials from behav data --
        if len(missingTrials)>0:
            print('Missing trials: {}'.format(str(missingTrials)))
            bdata.remove_trials(missingTrials) # This modifies all fields of bdata in place

        prefFreq = soundRespCells.behavFreqs.loc[indc][prefFreqInd.loc[indc]]
        trialsPrefFreq = bdata['targetFrequency']==prefFreq 
        selectedTrialsBool = (trialsPrefFreq & bdata['valid']).astype(bool)

        # -- Calculate response latency --
        try:
            indexLimitsSelectedTrials = indexLimitsEachTrial[:,selectedTrialsBool]
        except IndexError:
            print('IGNORED: The behavior and ephys sessions for this cell have different number of trials.')
            raise
        try:
            (respLatency,interim) = spikesanalysis.response_latency(spikeTimesFromEventOnset,
                                                                    indexLimitsSelectedTrials,
                                                                    timeRangeForLatency, threshold=0.5,
                                                                    win=signal.hanning(11))
        except IndexError:
            print('Index error for cell {}'.format(indRow)) # If there are no spikes in the timeRangeForLatency 
            dataframe.loc[indRow, 'latency'] = np.nan
            continue

        print('Response latency: {:0.1f} ms'.format(1e3*respLatency))
        if respLatency<=0:
            print('IGNORED: Estimated response latency was less than 0')

        if PLOT_LATENCY:
            plt.cla()
            trialsEachCond = selectedTrialsBool[:,np.newaxis]
            extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,[-0.3,0.4],trialsEachCond=trialsEachCond)
            plt.axvline(0,color='0.5')
            plt.axvline(respLatency,color='r')
            plt.draw()
            plt.waitforbuttonpress()

        ###celldb.loc[indRow, 'latency'] = respLatency
        if respLatency>0:
            latencyEachCell[brainArea].append(respLatency)
            
        print(maxSoundZscore.loc[indc])


for brainArea in brainAreas:
    meanLatency = np.mean(latencyEachCell[brainArea])
    stdLatency = np.std(latencyEachCell[brainArea])
    print('{} latency = {:0.1f} ms +/- {:0.1f} StDev.'.format(brainArea,1e3*meanLatency,1e3*stdLatency))
    soundDelay = 0.007
    print('\t after removal of sound delay: {:0.1f} ms +/- {:0.1f} StDev.'.format(1e3*(meanLatency-soundDelay),1e3*stdLatency))

sval,pVal = stats.ranksums(latencyEachCell['rightAC'],latencyEachCell['rightAStr'])
print('pVal = {}'.format(pVal))
    
plt.clf()
plt.hold(1)
plt.plot(np.tile(0,len(latencyEachCell['rightAC'])),latencyEachCell['rightAC'],'o',mec='k', mfc='none')
plt.plot(np.tile(1,len(latencyEachCell['rightAStr'])),latencyEachCell['rightAStr'],'o',mec='k', mfc='none')
plt.xlim([-1,2])
plt.xticks([0,1],['AC','AStr'])
#plt.ylim([])
plt.show()

'''
# --- To run this script for just one example --
cellParamsList = []
exampleCell = {'subject':'gosi004',
               'date':'2017-03-15',
               'tetrode':6,
               'cluster':4,
               'brainRegion':'ac'} # low freq, not modulated
cellParamsList.append(exampleCell)

for indc, cellParams in enumerate(cellParamsList):
    animal = cellParams['subject']
    date = cellParams['date']
    tetrode = cellParams['tetrode']
    cluster = cellParams['cluster']
    brainRegion = cellParams['brainRegion']
    # -- Find this cell in the database --
    cell = celldb.loc[(celldb.subject==animal) & (celldb.date==date) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)].iloc[0]
    cellObj = ephyscore.Cell(cell)
    depth = cellObj.dbRow['depth']

'''

