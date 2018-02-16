'''
Generate and store intermediate data for plot showing movement-aligned firing activity of astr neurons recorded in psychometric/switching task. Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.
Trials from all frequencies that have either a valid left or right choice are plotted
Lan Guo20161223
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
FIGNAME = 'movement_selectivity'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, STUDY_NAME, FIGNAME)

if not os.path.exists(outputDir):
    os.mkdir(outputDir)

scriptFullPath = os.path.realpath(__file__)
timeRange = [-0.5,1]
binWidth = 0.010
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0

colorsDict = {'left':'r', 'right':'g'} 

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- These example cells we picked manually  --#
cellParamsList = []
exampleCell = {'subject':'gosi004',
              'date':'2017-02-13',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-11',
              'tetrode':4,
               'cluster':5,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-15',
              'tetrode':4,
               'cluster':8,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-18',
              'tetrode':4,
               'cluster':10,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi004',
              'date':'2017-03-25',
              'tetrode':8,
               'cluster':3,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-07',
              'tetrode':1,
               'cluster':4,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-10',
              'tetrode':1,
               'cluster':10,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-14',
              'tetrode':7,
               'cluster':8,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi008',
              'date':'2017-03-20',
              'tetrode':4,
               'cluster':12,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

exampleCell = {'subject':'gosi010',
              'date':'2017-05-02',
              'tetrode':4,
               'cluster':12,
               'brainRegion':'ac'} 
cellParamsList.append(exampleCell)

# -- Here we can choose to generate data for a specific cell instead of every cell -- #
if len(sys.argv) > 1:
    cellIndToGenerate = int(sys.argv[1])
    cellParamsList = [cellParamsList[cellIndToGenerate]]

for cellParams in cellParamsList:
    animal = cellParams['subject']
    date = cellParams['date']
    tetrode = cellParams['tetrode']
    cluster = cellParams['cluster']
    brainRegion = cellParams['brainRegion']
    celldbPath = os.path.join(settings.DATABASE_PATH, '{}_database.h5'.format(animal))
    celldb = pd.read_hdf(celldbPath, key='reward_change')
    
    ### Using cellDB methode to find this cell in the cellDB ###
    oneCell = celldb.loc[(celldb.subject==animal) & (celldb.date==date) & (celldb.tetrode==tetrode) & (celldb.cluster==cluster)]
    sessionsThisCell = oneCell.iloc[0].sessiontype
    rcInd = sessionsThisCell.index('behavior')
    rcEphysThisCell = oneCell['ephys'].iloc[0][rcInd]
    rcBehavThisCell = oneCell['behavior'].iloc[0][rcInd]

    ## Get behavior data associated with 2afc session ###
    behavFileName = rcBehavThisCell
    behavFile = os.path.join(BEHAVIOR_PATH,animal,behavFileName)
    bdata = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(EPHYS_PATH, animal, rcEphysThisCell, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    ##### Get event onset times #####
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!

    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(EPHYS_PATH, animal, rcEphysThisCell, 'Tetrode{}.spikes'.format(tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH, animal, rcEphysThisCell)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==cluster]
    spikeData.samples = spikeData.samples[clusters==cluster, :, :]
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

    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)

    # -- Select trials to plot from behavior file -- #
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']

    trialsToUseRight = rightward
    trialsToUseLeft = leftward
    condLabels = ['go left', 'go right']
    trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight] 
    colorEachCond = [colorsDict['left'],colorsDict['right']]

    # -- Calculate eventOnsetTimes aligned to movement onset (CenterOut events) -- #
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]
    diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
    movementOnsetTimes = soundOnsetTimes+diffTimes

    # -- Calculate arrays for plotting raster -- #
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,movementOnsetTimes,timeRange)


    # -- Save raster intermediate data -- #    
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_movement_sel_raster_{}_{}_T{}_c{}.npz'.format(animal, date, tetrode, cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=movementOnsetTimes, spikeTimesFromEventOnset=spikeTimesFromEventOnset, indexLimitsEachTrial=indexLimitsEachTrial, condLabels=condLabels, trialsEachCond=trialsEachCond, colorEachCond=colorEachCond, script=scriptFullPath, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, timeRange=timeRange, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], **cellParams) 


    # -- Calculate additional arrays for plotting psth -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    # -- Save psth intermediate data -- #
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_movement_sel_psth_{}_{}_T{}_c{}.npz'.format(animal, date, tetrode, cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, condLabels=condLabels, trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,timeRange=timeRange, binWidth=binWidth, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], script=scriptFullPath, **cellParams) 
