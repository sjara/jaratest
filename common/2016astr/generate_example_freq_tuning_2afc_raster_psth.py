'''
Generate and store intermediate data for plot showing frequency-selectivity of astr sound-responsive neurons (using 2afc data). Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.

Lan Guo 20170302
'''

### To DO 

# In the filename of the npz should include tetrode and cluster e.g. T6_c2
# save the script name that generates the npz in the npz file, in the field called 'script' (using os.path.realpath(__file__)
# Save the manually set params such as timeRange in npz file

import os
import sys
import importlib
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
#from jaratest.lan import test055_load_n_plot_billy_data_one_cell as loader
import figparams

FIGNAME = 'sound_freq_selectivity'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
timeRange = [-0.5,0.8]
binWidth = 0.010
scriptFullPath = os.path.realpath(__file__)
paradigm = '2afc'

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

# if not os.path.ismount(BEHAVIOR_PATH):
#     os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

# if not os.path.ismount(EPHYS_PATH):
#     os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- Select an example cell from allcells file -- #
cellParamsList = [{'firstParam':'test053',
                   'behavSession':'20150615a',
                   'tetrode':5,
                   'cluster':7}, #strong sharp response to low freqs
                  {'firstParam':'adap017',
                   'behavSession':'20160405a',
                   'tetrode':3,
                   'cluster':7}, #suppressed in tuning&2afc
                  {'firstParam':'test055',
                   'behavSession':'20150307a',
                   'tetrode':4,
                   'cluster':3}, #similar sharp response in tuning&2afc
                  {'firstParam':'adap017',
                   'behavSession':'20160317a',
                   'tetrode':5,
                   'cluster':3},#sustained strong response to mid freqs
                  {'firstParam':'adap015',
                   'behavSession':'20160205a',
                   'tetrode':6,
                   'cluster':5}, #suppressed in tuning&2afc 
                  {'firstParam':'adap017',
                   'behavSession':'20160328a',
                   'tetrode':7,
                   'cluster':9}] #both sound and movement responsive

for cellParams in cellParamsList:
    mouseName = cellParams['firstParam']

    allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(**cellParams)
    oneCell = allcells.cellDB[cellIndex]

    ## Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,paradigm,oneCell.behavSession)
    behavFile = os.path.join(BEHAVIOR_PATH,oneCell.animalName,behavFileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')


    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, oneCell.animalName, oneCell.ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!


    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.ephysSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH,oneCell.animalName,oneCell.ephysSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
    spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    spikeTimestamps = spikeData.timestamps

    # -- Check to see if ephys has skipped trials, if so remove trials from behav data -- #
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimeEphys = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bdata['timeTarget']

    diffTimes = bdata['timeCenterOut'] - bdata['timeTarget']
    #movementOnsetTimeEphys = soundOnsetTimeEphys + diffTimes
    
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)

    # -- Calculate and store intermediate data for tuning raster -- #
    freqEachTrial = bdata['targetFrequency']
    valid = bdata['valid'].astype('bool')
    possibleFreq = np.unique(freqEachTrial)
    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    trialsEachFreq = trialsEachFreq & valid[:,np.newaxis] #Use only valid trials where sound is played in full 

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimeEphys,timeRange)

    ### Save raster data ###    
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_freq_tuning_2afc_raster_{}_{}_T{}_c{}.npz'.format(oneCell.animalName, oneCell.behavSession, oneCell.tetrode,oneCell.cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=eventOnsetTimes, possibleFreq=possibleFreq, spikeTimesFromEventOnset=spikeTimesFromEventOnset, movementTimesFromEventOnset=diffTimes, indexLimitsEachTrial=indexLimitsEachTrial, timeRange=timeRange,trialsEachFreq=trialsEachFreq, script=scriptFullPath, **cellParams)

    # -- Calculate and store intermediate data for tuning psth -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    ### Save psth data ###
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_freq_tuning_2afc_psth_{}_{}_T{}_c{}.npz'.format(oneCell.animalName, oneCell.behavSession,oneCell.tetrode,oneCell.cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, possibleFreq=possibleFreq, spikeCountMat=spikeCountMat, timeVec=timeVec, trialsEachFreq=trialsEachFreq, timeRange=timeRange, binWidth=binWidth, script=scriptFullPath, **cellParams)
