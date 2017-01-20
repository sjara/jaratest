'''
Generate and store intermediate data for plot showing soundonset-aligned firing activity of astr neurons recorded in psychometric curve task, only trials of the two middle frequencies are plotted. Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.

Lan Guo20161226
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

# -- These example cells I picked manually from jarauser@jarahub/data/reports/billy/20160818_billys_lastest_reports/2016_billy_lan_paper/20160728_psycurve_centerFreq_soundResponse_modulation_figure/modulation --#
cellParamsList = []

exampleCell = {'firstParam':'adap017',
              'behavSession':'20160411a',
              'tetrode':3,
              'cluster':10}
cellParamsList.append(exampleCell)
exampleCell = {'firstParam':'test053',
              'behavSession':'20150615a',
              'tetrode':5,
               'cluster':7}
cellParamsList.append(exampleCell)
exampleCell = {'firstParam':'test055',
              'behavSession':'20150303a',
              'tetrode':4,
               'cluster':7}
cellParamsList.append(exampleCell)
exampleCell = {'firstParam':'adap017',
              'behavSession':'20160414a',
              'tetrode':4,
               'cluster':9}
cellParamsList.append(exampleCell)
exampleCell = {'firstParam':'test055',
              'behavSession':'20150313a',
              'tetrode':4,
               'cluster':7} #Not modulated
cellParamsList.append(exampleCell)

'''
## OLDER example now removed due to duplicate clusters
exampleCell = {'firstParam':'adap017',
              'behavSession':'20160407a',
              'tetrode':4,
               'cluster':3}
cellParamsList.append(exampleCell)
'''
####################################################################################

scriptFullPath = os.path.realpath(__file__)
timeRange = [-0.5,1]
binWidth = 0.010
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
colorsDict = {'left':'g', 'right':'r'} 

# -- Access mounted behavior and ephys drives for psycurve and switching mice -- #
BEHAVIOR_PATH = settings.BEHAVIOR_PATH_REMOTE
EPHYS_PATH = settings.EPHYS_PATH_REMOTE

if not os.path.ismount(BEHAVIOR_PATH):
    os.system('sshfs -o idmap=user jarauser@jarahub:/data/behavior/ {}'.format(BEHAVIOR_PATH))

if not os.path.ismount(EPHYS_PATH):
    os.system('sshfs -o idmap=user jarauser@jarastore:/data2016/ephys/ {}'.format(EPHYS_PATH))


# -- Select an example cell from allcells file -- #
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

    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)


    # -- Select trials to plot from behavior file -- #
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']

    # -- Select trials of middle frequency to plot -- #
    middleFreqs = [possibleFreq[numFreqs/2-1], possibleFreq[numFreqs/2]] #selects middle frequencies, using int division resulting in int property. MAY FAIL IN THE FUTURE
    #pdb.set_trace()
    for middleFreq in middleFreqs:
        oneFreq = bdata['targetFrequency'] == middleFreq #vector for selecing trials presenting this frequency

        trialsToUseRight = rightward & oneFreq
        trialsToUseLeft = leftward & oneFreq
        condLabels = ['left choice', 'right choice']
        trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight] 
        colorEachCond = [colorsDict['left'],colorsDict['right']]


        # -- Calculate eventOnsetTimes aligned to sound onset -- #
        eventOnsetTimes=np.array(eventData.timestamps)
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

        # -- Calculate arrays for plotting raster -- #
        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)


        # -- Save raster intermediate data -- #    
        outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
        outputFile = 'example_psycurve_{}Hz_soundaligned_raster_{}_{}_T{}_c{}.npz'.format(middleFreq, oneCell.animalName, oneCell.behavSession, oneCell.tetrode,oneCell.cluster)
        outputFullPath = os.path.join(outputDir,outputFile)
        np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=soundOnsetTimes, spikeTimesFromEventOnset=spikeTimesFromEventOnset, indexLimitsEachTrial=indexLimitsEachTrial, condLabels=condLabels, trialsEachCond=trialsEachCond, colorEachCond=colorEachCond, script=scriptFullPath, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, timeRange=timeRange, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], frequencyPloted=middleFreq, **cellParams)


        # -- Calculate additional arrays for plotting psth -- #
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

        # -- Save psth intermediate data -- #
        outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
        outputFile = 'example_psycurve_{}Hz_soundaligned_psth_{}_{}_T{}_c{}.npz'.format( middleFreq, oneCell.animalName, oneCell.behavSession,oneCell.tetrode,oneCell.cluster)
        outputFullPath = os.path.join(outputDir,outputFile)
        np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, condLabels=condLabels, trialsEachCond=trialsEachCond, colorEachCond=colorEachCond,timeRange=timeRange, binWidth=binWidth, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, script=scriptFullPath, colorLeftTrials=colorsDict['left'], colorRightTrials=colorsDict['right'], frequencyPloted=middleFreq, **cellParams)
