'''
This script includes functions to load ephys (cluster files) and behavior data for a cell of interest from billy's data folders in jarastore.
Also functions to plot tuning raster and differently-aligned 2afc rasters.

Lan Guo 2016-08-10
'''

import sys
import os
import importlib
import numpy as np
import matplotlib.pyplot as plt
from jaratest.billy.scripts import celldatabase_quality_tuning as cellDB
from jaratest.nick.database import dataplotter 
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots

### ephys and behavior directory to load data from. SPECIFIC TO BILLY'S DATA. THIS REQUIRES MOUNTING THE DATA2016/EPHYS DIRECTORY AS A DRIVE ON MY COMPUTER ###
EPHYSDIR_MOUNTED = '/home/languo/data/jarastorephys'
BEHAVDIR_MOUNTED = '/home/languo/data/mnt/jarahubdata'
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0

def load_remote_tuning_data(oneCell,behavDirMounted,ephysDirMounted):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated tuning ephys and tuning behav data from the mounted jarastore drive. Returns eventOnsetTimes, spikeTimestamps, and bData objects.
    '''
    
    ### Get behavior data associated with tuning curve ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'tuning_curve',oneCell.tuningBehavior)
    behavFile = os.path.join(behavDirMounted,oneCell.animalName,behavFileName)
    bData = loadbehavior.BehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(ephysDirMounted, oneCell.animalName, oneCell.tuningSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)

    ### Get event onset times ###
    eventTimestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    evID=np.array(eventData.eventID)
    eventOnsetTimes=eventTimestamps[(evID==1)]
    
    ### GEt spike data ###
    spikeFilename = os.path.join(ephysDirMounted,oneCell.animalName,oneCell.tuningSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeTimestamps=spikeData.timestamps/EPHYS_SAMPLING_RATE

    return (eventOnsetTimes, spikeTimestamps, bData)

def load_remote_2afc_data(oneCell,behavDirMounted,ephysDirMounted):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated 2afc ephys and 2afc behav data from the mounted jarastore drive. Returns eventOnsetTimes, spikeTimestamps, and bData objects.
    '''
    
    ### Get behavior data associated with tuning curve ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'2afc',oneCell.behavSession)
    behavFile = os.path.join(behavDirMounted,oneCell.animalName,behavFileName)
    bData = loadbehavior.BehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(ephysDirMounted, oneCell.animalName, oneCell.ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)

    ### Get event onset times ###
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    #evID=np.array(eventData.eventID)
    #eventOnsetTimes=eventTimestamps[(evID==1)]
    
    ### GEt spike data ###
    spikeFilename = os.path.join(ephysDirMounted,oneCell.animalName,oneCell.ephysSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeTimestamps=spikeData.timestamps/EPHYS_SAMPLING_RATE

    return (eventData, spikeTimestamps, bData)


def plot_tuning_raster_one_intensity(oneCell, intensity=50):
    #calls load_remote_tuning_data(oneCell) to get the data, then plot raster
    eventOnsetTimes, spikeTimestamps, bdata = load_remote_tuning_data(oneCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)
    if len(possibleIntensity) != 1:
        intensity = 50.0 #50dB is the stimulus intensity used in 2afc task
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]
    
    #print len(intensityEachTrial),len(eventOnsetTimes),len(spikeTimestamps)

    freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    intensityLabels = ['{:.0f} dB'.format(intensity) for intensity in possibleIntensity]        
    xlabel="Time from sound onset (sec)"
    #plotTitle = ephysSession+'tuning with chords'
    plotTitle = 'Tt'+str(oneCell.tetrode)+'c'+str(oneCell.cluster)+' tuning with 50dB chords'
    timeRange = [-0.5,1]
    ### FIXME: this is a bad hack for when ephys is one trial more than behavior file ###
    if len(eventOnsetTimes)==len(intensityEachTrial)+1:
        eventOnsetTimes=eventOnsetTimes[:-1]
    print len(intensityEachTrial),len(eventOnsetTimes),len(spikeTimestamps)
   
    plt.figure()
    dataplotter.plot_raster(spikeTimestamps,
                            eventOnsetTimes,
                            sortArray=freqEachTrial,
                            timeRange=timeRange,
                            ms=3,
                            labels=freqLabels)
    plt.xlabel('Time from sound onset')
    plt.title(plotTitle)
    

def plot_switching_raster(oneCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True):
    '''
    Plots raster for 2afc switching task with different alignment at time 0 and different choices for what frequencies to include in the plot.
    Arguments:
    oneCell is a CellInfo object.
    freqToPlot is a string; 'middle' means plotting only the middle frequency, 'all' means plotting all three frequenciens.
    alignment should be a string with possible values: 'sound', 'center-out','side-in'.
    timeRange is a list of two floats, indicating the start and end of plot range.
    '''

    #calls load_remote_2afc_data(oneCell) to get the data, then plot raster
    eventData, spikeTimestamps, bdata = load_remote_2afc_data(oneCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
    # -- Check to see if ephys has skipped trials, if so remove trials from behav data -- #
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimeEphys = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bdata['timeTarget']

    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)
    
    # -- Find trials each block (if plotting by block) or find trials each type (e.g. low-boundary, high-boundary; if not plotting by block) -- #
    if byBlock:
        bdata.find_trials_each_block()
        trialsEachBlock = bdata.blocks['trialsEachBlock']
    else:
        #####????What is the dif between this method and the one below????####
        ##trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
    
    
    # -- Calculate eventOnsetTimes based on alignment parameter -- #
    if alignment == 'sound':
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        EventOnsetTimes = eventOnsetTimes[soundOnsetEvents]
    elif alignment == 'center-out':
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        EventOnsetTimes = eventOnsetTimes[soundOnsetEvents]
        diffTimes=bdata['timeCenterOut']-bdata['timeTarget']
        EventOnsetTimes+=diffTimes
    elif alignment == 'side-in':
        soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
        EventOnsetTimes = eventOnsetTimes[soundOnsetEvents]
        diffTimes=bdata['timeSideIn']-bdata['timeTarget']
        EventOnsetTimes+=diffTimes


    # -- Select trials to plot from behavior file -- #
    rightward = bdata['choice']==bdata.labels['choice']['right']
    leftward = bdata['choice']==bdata.labels['choice']['left']
    invalid = bdata['outcome']==bdata.labels['outcome']['invalid']
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    correctRightward = rightward & correct
    correctLeftward = leftward & correct

    possibleFreq = np.unique(bdata['targetFrequency'])
    trialsEachBlock = bdata.blocks['trialsEachBlock']

    # -- Select trials to plot based on desired frequencies to plot -- #
    if freqToPlot == 'middle':
        middleFreq = possibleFreq[1] #selects middle frequency
        oneFreq = bdata['targetFrequency'] == middleFreq #vector for selecing trials presenting this frequency
        trialsToUseRight = rightward & oneFreq #if only plotting middle frequency, then plot both correct and incorrect trials
        trialsToUseLeft = leftward & oneFreq
        trialsEachCond = np.c_[trialsToUseLeft,trialsToUseRight] 
        colorEachCond = ['r','g']   
    elif freqToPlot == 'all':
        lowFreq = possibleFreq[0]
        middleFreq = possibleFreq[1]
        highFreq = possibleFreq[2]
        
        trialsToUseLowFreq = ((bdata['targetFrequency'] == lowFreq) & correct)
        trialsToUseHighFreq = ((bdata['targetFrequency'] == highFreq) & correct)
        trialsToUseMidFreqLeft = leftward & (bdata['targetFrequency'] == middleFreq)
        trialsToUseMidFreqRight = rightward & (bdata['targetFrequency'] == middleFreq)
        trialsEachCond = np.c_[trialsToUseLowFreq,trialsToUseMidFreqLeft,trialsToUseMidFreqRight,trialsToUseHighFreq]
        colorEachCond = ['b','r','g','r']
    
    # -- Calculate matrix of spikes per trial for plotting -- #
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)
    
    # -- Plot raster and PSTH -- #
    plt.figure()
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    
    plt.ylabel('Trials')
    plt.title('{0}_{1}_T{2}c{3}_{4}_{5} frequency'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,freqToPlot)) 


def plot_psy_curve_raster(oneCell, alignment='sound'):
    pass


def plot_summary_per_cell(oneCell):
    #can plot wave-from, ISI, projections...
    pass

if __name__ == '__main__':
    ### Params associated with the cell of interest ###
    cellParams = {'behavSession':'20160420a',
                  'tetrode':3,
                  'cluster':3}

    ### Loading allcells file for a specified mouse ###
    mouseName = 'adap017'
    allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)

    allcells = importlib.import_module(allcellsFileName)

    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)

    thisCell = allcells.cellDB[cellIndex]
    ephysSession = thisCell.ephysSession
    tuningSession = thisCell.tuningSession
    tuningBehavior = thisCell.tuningBehavior

    eventOnsetTimes, spikeTimestamps, bData = load_remote_tuning_data(thisCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
    #plot_tuning_raster_one_intensity(thisCell)
    plot_switching_raster(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1])
    plt.show()
