'''
Generate and store intermediate data for plot showing movement-aligned firing activity of astr neurons recorded in psychometric/switching task. Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.
Trials from all frequencies that have either a valid left or right choice are plotted
Lan Guo20161223
'''
import os
import sys
import importlib
import numpy as np
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from jaratoolbox import behavioranalysis
from jaratoolbox import settings
import figparams

FIGNAME = 'movement_selectivity'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

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


# -- Select an example cell from allcells file -- #
cellParamsList = [{'firstParam':'test059',
                   'behavSession':'20150629a',
                   'tetrode':2,
                   'cluster':7}, #more responsive to left
                  {'firstParam':'test055',
                   'behavSession':'20150313a',
                   'tetrode':7,
                   'cluster':6}, #more responsive to right
                  {'firstParam':'adap017',
                   'behavSession':'20160317a',
                   'tetrode':1,
                   'cluster':6}, #more responsive to right, not so much different though
                  {'firstParam':'adap013',
                   'behavSession':'20160406a',
                   'tetrode':8,
                   'cluster':4}, #more responsive to left
                  {'firstParam':'adap017',
                   'behavSession':'20160330a',
                   'tetrode':4,
                   'cluster':11}, #more responsive to left
                  {'firstParam':'adap017',
                   'behavSession':'20160328a',
                   'tetrode':7,
                   'cluster':9}]  #both sound and movement responsive

for cellParams in cellParamsList:
    mouseName = cellParams['firstParam']

    allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)
    allcells = importlib.import_module(allcellsFileName)

    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(**cellParams)
    oneCell = allcells.cellDB[cellIndex]


    ## Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'2afc',oneCell.behavSession)
    behavFile = os.path.join(BEHAVIOR_PATH,oneCell.animalName,behavFileName)
    bdata = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')


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

    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)


    # -- Select trials to plot from behavior file -- #
    #possibleFreq = np.unique(bdata['targetFrequency'])
    #numFreqs = len(possibleFreq)

    # -- Select trials of middle frequency to plot, determine whether to plot by block -- #
    #middleFreq = possibleFreq[numFreqs/2] #selects middle frequency, using int division resulting in int property. MAY FAIL IN THE FUTURE
    #pdb.set_trace()
    #oneFreq = bdata['targetFrequency'] == middleFreq #vector for selecing trials presenting this frequency
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']

    #trialsToUseRight = rightward & oneFreq
    #trialsToUseLeft = leftward & oneFreq
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
    outputFile = 'example_movement_sel_raster_{}_{}_T{}_c{}.npz'.format(oneCell.animalName, oneCell.behavSession, oneCell.tetrode,oneCell.cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=movementOnsetTimes, spikeTimesFromEventOnset=spikeTimesFromEventOnset, indexLimitsEachTrial=indexLimitsEachTrial, condLabels=condLabels, trialsEachCond=trialsEachCond, colorEachCond=colorEachCond, script=scriptFullPath, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, timeRange=timeRange, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], **cellParams) #frequencyPloted=middleFreq,


    # -- Calculate additional arrays for plotting psth -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    # -- Save psth intermediate data -- #
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_movement_sel_psth_{}_{}_T{}_c{}.npz'.format(oneCell.animalName, oneCell.behavSession,oneCell.tetrode,oneCell.cluster)
    outputFullPath = os.path.join(outputDir,outputFile)
    np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, condLabels=condLabels, trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,timeRange=timeRange, binWidth=binWidth, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], script=scriptFullPath, **cellParams) #frequencyPloted=middleFreq,
