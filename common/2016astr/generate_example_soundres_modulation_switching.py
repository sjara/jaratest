'''
Generate and store intermediate data for plot showing sound-onset-aligned firing activity of astr neurons recorded in switching task, only middle frequency is plotted. Data for raster and psth are saved separately. 
For raster data, output contains spikeTimestamps, eventOnsetTimes, freqEachTrial.
For psth data, output contains spikeCountMat, timeVec, freqEachTrial.

Lan Guo20161227
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
reload(figparams)

FIGNAME = 'soundres_modulation_switching'
dataDir = os.path.join(settings.FIGURES_DATA_PATH, figparams.STUDY_NAME, FIGNAME)

if not os.path.exists(dataDir):
    os.mkdir(dataDir)

colorsDict = {'lowBlock':figparams.colp['MidFreqL'], 
              'highBlock':figparams.colp['MidFreqR']} 


# -- These example cells I picked manually from jarauser@jarahub/data/reports/billy/20160818_billys_lastest_reports/2016_billy_lan_paper/20160615_switching_modulation_examples_figure7/Best_quality_ISI-2_ZVal-3/sound_modulation --#

cellParamsList = [{'firstParam':'test089',
                   'behavSession':'20160124a',
                   'tetrode':4,
                   'cluster':6}, #modulated
                  {'firstParam':'test059',
                   'behavSession':'20150624a',
                   'tetrode':1,
                   'cluster':2}, #modulated, duplicate
                  {'firstParam':'test059',
                   'behavSession':'20150624a',
                   'tetrode':1,
                   'cluster':7}, #modulated, duplicate
                  {'firstParam':'adap020',
                   'behavSession':'20160526a',
                   'tetrode':2,
                   'cluster':9}] #not modulated

'''
# OLD examples removed due to duplicate
{'firstParam':'test059',
   'behavSession':'20150624a',
   'tetrode':1,
   'cluster':2},
  {'firstParam':'test059',
   'behavSession':'20150624a',
   'tetrode':1,
   'cluster':7},
'''
####################################################################################
scriptFullPath = os.path.realpath(__file__)
timeRange = [-0.5,1]
binWidth = 0.010
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
plotByBlock = True #Define whether to make the plots split by block
minBlockSize = 20 #Omit blocks with less than 20 trials

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
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)

    # -- Select trials of middle frequency to plot, determine whether to plot by block -- #
    middleFreq = possibleFreq[numFreqs/2] #selects middle frequency, using int division resulting in int property. MAY FAIL IN THE FUTURE
    #pdb.set_trace()
    oneFreq = bdata['targetFrequency'] == middleFreq #vector for selecing trials presenting this frequency
    correctOneFreq = oneFreq  & correct 
    
    if plotByBlock:
        bdata.find_trials_each_block()
        trialsEachBlock = bdata.blocks['trialsEachBlock']
        correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
        correctBlockSizes = sum(correctTrialsEachBlock)
        if (correctBlockSizes[-1] < minBlockSize): #A check to see if last block is too small to plot
            correctTrialsEachBlock = correctTrialsEachBlock[:,:-1]

        trialsEachCond = correctTrialsEachBlock
        if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
            colorEachCond = 5*[colorsDict['lowBlock'],colorsDict['highBlock']] #assume there are not more than 5 blocks
        elif bdata['currentBlock'][0]==bdata.labels['currentBlock']['high_boundary']:
            colorEachCond = 5*[colorsDict['highBlock'],colorsDict['lowBlock']]

    else:
        currentBlock = bdata['currentBlock']
        blockTypes = [bdata.labels['currentBlock']['low_boundary'],bdata.labels['currentBlock']['high_boundary']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        midFreqCorrectBlockLow = correctOneFreq&trialsEachType[:,0]
        midFreqCorrectBlockHigh = correctOneFreq&trialsEachType[:,1]
        trialsEachCond = np.c_[midFreqCorrectBlockLow,midFreqCorrectBlockHigh]
        colorEachCond = [colorsDict['lowBlock'],colorsDict['highBlock']]


    # -- Calculate eventOnsetTimes aligned to sound onset -- #
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimes = eventOnsetTimes[soundOnsetEvents]

    # -- Calculate arrays for plotting raster -- #
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)


    # -- Save raster intermediate data -- #    
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_switching_midfreq_soundaligned_raster_{}_{}_T{}_c{}.npz'.format(oneCell.animalName, oneCell.behavSession, oneCell.tetrode,oneCell.cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, spikeTimestamps=spikeTimestamps, eventOnsetTimes=soundOnsetTimes, indexLimitsEachTrial=indexLimitsEachTrial,spikeTimesFromEventOnset=spikeTimesFromEventOnset, trialsEachCond=trialsEachCond, colorEachCond=colorEachCond, script=scriptFullPath, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, plotByBlock=plotByBlock, minBlockSize=minBlockSize, timeRange=timeRange, colorMidFreqL=colorsDict['lowBlock'], colorMidFreqR=colorsDict['highBlock'], frequencyPloted=middleFreq, **cellParams)


    # -- Calculate additional arrays for plotting psth -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)

    # -- Save psth intermediate data -- #
    #outputDir = os.path.join(settings.FIGURESDATA, figparams.STUDY_NAME)
    outputFile = 'example_switching_midfreq_soundaligned_psth_{}_{}_T{}_c{}.npz'.format(oneCell.animalName, oneCell.behavSession,oneCell.tetrode,oneCell.cluster)
    outputFullPath = os.path.join(dataDir,outputFile)
    np.savez(outputFullPath, spikeCountMat=spikeCountMat, timeVec=timeVec, trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,timeRange=timeRange, binWidth=binWidth, EPHYS_SAMPLING_RATE=EPHYS_SAMPLING_RATE, soundTriggerChannel=soundTriggerChannel, plotByBlock=plotByBlock, minBlockSize=minBlockSize, script=scriptFullPath, colorMidFreqL=colorsDict['lowBlock'], colorMidFreqR=colorsDict['highBlock'], frequencyPloted=middleFreq, **cellParams)
