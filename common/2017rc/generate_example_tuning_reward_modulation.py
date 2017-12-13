'''
Generate and store intermediate data for plots showing tuning curve of astr/ac neurons recorded in reward-change task. Tuning curve used 50dB chords. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, spikeTimesFromEventOnset, trialsEachFreq, as well as meta params.
For psth data, output contains spikeCountMat, timeVec, trialsEachFreq, as well as meta params.

Lan Guo 20171009
'''
import os
import sys
import numpy as np
import pandas as pd
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

STUDY_NAME = '2017rc'

FIGNAME = 'tuning_reward_change'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

colorDict = {'leftMoreLowFreq':'g',
             'rightMoreLowFreq':'m',
             'sameRewardLowFreq':'y',
             'leftMoreHighFreq':'r',
             'rightMoreHighFreq':'b',
             'sameRewardHighFreq':'darkgrey'}

# -- These example cells I picked manually  --#
cellParamsList = []

exampleCell = {'subject':'adap015',
              'date':'2016-03-18',
              'tetrode':3,
               'cluster':9,
               'brainRegion':'astr'} # low freq, sound modulated
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-03',
              'tetrode':6,
               'cluster':3,
               'brainRegion':'ac'} # low freq, sound modulated
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-18',
              'tetrode':6,
               'cluster':10,
               'brainRegion':'ac'} # low freq, sound modulated
cellParamsList.append(exampleCell)

exampleCell = {'subject':'adap012',
              'date':'2016-02-04',
              'tetrode':3,
               'cluster':3,
               'brainRegion':'astr'} # rightward, movement modulated
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-11',
              'tetrode':1,
               'cluster':10,
               'brainRegion':'ac'} # leftward, movement modulated
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-14',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac'} # rightward, movement modulated
cellParamsList.append(exampleCell)

# -- Here we can choose to generate data for a specific cell instead of every cell -- #
if len(sys.argv)>1:
    cellInd = int(sys.argv[1])
    cellsToGenerate = [cellParamsList[cellInd]]
else:
    cellsToGenerate = cellParamsList

####################################################################################
intensityToPlot = 50  # 50dB is the stimulus intensity used in 2afc task
scriptFullPath = os.path.realpath(__file__)
timeRange = [-0.5,1]
binWidth = 0.010
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
###################################################################################

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- Select an example cell from allcells file -- #
for cellParams in cellsToGenerate:
    animal = cellParams['subject']
    date = cellParams['date']
    tetrode = cellParams['tetrode']
    cluster = cellParams['cluster']
    brainRegion = cellParams['brainRegion']
    celldbPath = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    
    ### Using cellDB methode to find this cell in the cellDB ###
    oneCell = celldb.loc[(celldb.subject==animal) & (celldb.date==date) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)]
    sessionsThisCell = oneCell.iloc[0].sessiontype
    tuningInd = sessionsThisCell.index('tc')
    tuningEphysThisCell = oneCell['ephys'].iloc[0][tuningInd]
    tuningBehavThisCell = oneCell['behavior'].iloc[0][tuningInd]

    ## Get behavior data associated with 2afc session ###
    behavFileName = tuningBehavThisCell
    behavFile = os.path.join(BEHAVIOR_PATH,animal,behavFileName)
    bdata = loadbehavior.BehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, animal, tuningEphysThisCell, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    ### Get sound-onset event times ###
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(EPHYS_PATH, animal, tuningEphysThisCell, 'Tetrode{}.spikes'.format(tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH, animal, tuningEphysThisCell)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==cluster]
    spikeData.samples = spikeData.samples[clusters==cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    spikeTimestamps = spikeData.timestamps

    # -- Calculate and store intermediate data for tuning raster -- #
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)
    if len(possibleIntensity) != 1:
        intensity = intensityToPlot  # 50dB is the stimulus intensity used in 2afc task
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        #intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        soundOnsetTimes = soundOnsetTimes[trialsThisIntensity]

    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)

    # -- Save raster intermediate data -- #    
    outputFile = 'example_tuning_raster_{}_{}_T{}_c{}.npz'.format(animal, date, tetrode, cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=soundOnsetTimes, spikeTimesFromEventOnset=spikeTimesFromEventOnset, indexLimitsEachTrial=indexLimitsEachTrial, possibleFreq=possibleFreq, trialsEachFreq=trialsEachFreq, script=scriptFullPath, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, timeRange=timeRange, **cellParams)

    # -- Calculate additional arrays for plotting psth -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    # -- Save psth intermediate data -- #
    outputFile = 'example_tuning_psth_{}_{}_T{}_c{}.npz'.format(animal, date, tetrode, cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    print 'Saving {0} ...'.format(outputFullPath)
    np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, trialsEachFreq=trialsEachFreq, possibleFreq=possibleFreq, timeRange=timeRange, binWidth=binWidth, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, script=scriptFullPath, **cellParams)
