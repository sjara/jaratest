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
import pdb
from jaratest.billy.scripts import celldatabase_quality_tuning as cellDB
from jaratest.nick.database import dataplotter 
from jaratoolbox import settings
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import spikesorting
from jaratoolbox import ephyscore

import matplotlib
#matplotlib.rcParams['font.family'] = 'Helvetica'
matplotlib.rcParams['font.family'] = 'FreeSerif' #'Whitney-Medium'
matplotlib.rcParams['svg.fonttype'] = 'none'  # To

### ephys and behavior directory to load data from. SPECIFIC TO BILLY'S DATA. THIS REQUIRES MOUNTING THE DATA2016/EPHYS DIRECTORY AS A DRIVE ON MY COMPUTER ###
EPHYSDIR_MOUNTED = '/home/languo/data/jarastorephys'
BEHAVDIR_MOUNTED = '/home/languo/data/mnt/jarahubdata'
EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0
minBlockSize = 20  #minimal number of trials per block to be plotted

def load_remote_tuning_data(oneCell,behavDir=BEHAVDIR_MOUNTED,ephysDir=EPHYSDIR_MOUNTED):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated tuning ephys and tuning behav data from the mounted jarastore drive. Returns eventOnsetTimes, spikeTimestamps, and bData objects.
    '''
    
    ### Get behavior data associated with tuning curve ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'tuning_curve',oneCell.tuningBehavior)
    behavFile = os.path.join(behavDir,oneCell.animalName,behavFileName)
    bData = loadbehavior.BehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(ephysDir, oneCell.animalName, oneCell.tuningSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)

    ### Get event onset times ###
    eventTimestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    evID=np.array(eventData.eventID)
    eventOnsetTimes=eventTimestamps[(evID==1)]
    
    ### GEt spike data for just this cluster ###
    spikeFilename = os.path.join(ephysDir,oneCell.animalName,oneCell.tuningSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps=spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(ephysDir,oneCell.animalName,oneCell.tuningSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
    spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell)
    #spikeTimestamps=spikeData.spikes.timestamps

    return (eventOnsetTimes, spikeData.timestamps, bData)


def load_remote_2afc_data(oneCell,behavDir=BEHAVDIR_MOUNTED,ephysDir=EPHYSDIR_MOUNTED):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated 2afc ephys and 2afc behav data from the mounted jarastore drive. Returns eventOnsetTimes, spikeTimestamps, and bData objects.
    '''
    
    ### Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'2afc',oneCell.behavSession)
    behavFile = os.path.join(behavDir,oneCell.animalName,behavFileName)
    bData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

    ### Get events data ###
    fullEventFilename=os.path.join(ephysDir, oneCell.animalName, oneCell.ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)

    ### Get event onset times ###
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    #evID=np.array(eventData.eventID)
    #eventOnsetTimes=eventTimestamps[(evID==1)]
    
    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(ephysDir,oneCell.animalName,oneCell.ephysSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(ephysDir,oneCell.animalName,oneCell.ephysSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
    spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    
    return (eventData, spikeData, bData)


def load_remote_2afc_behav(oneCell,behavDir=BEHAVDIR_MOUNTED,ephysDir=EPHYSDIR_MOUNTED):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated 2afc behav data from the mounted jarastore drive. Returns bData object.
    '''
    ### Get behavior data associated with 2afc session ###
    behavFileName = '{0}_{1}_{2}.h5'.format(oneCell.animalName,'2afc',oneCell.behavSession)
    behavFile = os.path.join(behavDir,oneCell.animalName,behavFileName)
    bData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
    return bData


def load_remote_2afc_events(oneCell,behavDir=BEHAVDIR_MOUNTED,ephysDir=EPHYSDIR_MOUNTED):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated 2afc events from the mounted jarastore drive. Returns eventOnsetTimes, spikeTimestamps.
    '''
    ### Get events data ###
    fullEventFilename=os.path.join(ephysDir, oneCell.animalName, oneCell.ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)

    ### Get event onset times ###
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    #evID=np.array(eventData.eventID)
    #eventOnsetTimes=eventTimestamps[(evID==1)]
    return eventData

def load_remote_2afc_spikes(oneCell,behavDir=BEHAVDIR_MOUNTED,ephysDir=EPHYSDIR_MOUNTED):
    '''
    Given a CellInfo object and remote behavior and ephys directories, this function loads the associated 2afc spikes from the mounted jarastore drive. Returns eventOnsetTimes, spikeTimestamps.
    '''
    ### GEt spike data of just this cluster ###
    spikeFilename = os.path.join(ephysDir,oneCell.animalName,oneCell.ephysSession, 'Tetrode{}.spikes'.format(oneCell.tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(ephysDir,oneCell.animalName,oneCell.ephysSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(oneCell.tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==oneCell.cluster]
    spikeData.samples = spikeData.samples[clusters==oneCell.cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    #spikeData = ephyscore.CellData(oneCell) #This defaults to settings ephys path
    return spikeData


def plot_tuning_raster_one_intensity(oneCell, intensity=50.0, timeRange = [-0.5,1]):
    #calls load_remote_tuning_data(oneCell) to get the data, then plot raster
    eventOnsetTimes, spikeTimestamps, bdata = load_remote_tuning_data(oneCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)
    if len(possibleIntensity) != 1:
        intensity = intensity #50dB is the stimulus intensity used in 2afc task
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
    ### FIXME: this is a bad hack for when ephys is one trial more than behavior file ###
    if len(eventOnsetTimes)==len(intensityEachTrial)+1:
        eventOnsetTimes=eventOnsetTimes[:-1]
    print len(intensityEachTrial),len(eventOnsetTimes),len(spikeTimestamps)
   
    #plt.figure()
    dataplotter.plot_raster(spikeTimestamps,
                            eventOnsetTimes,
                            sortArray=freqEachTrial,
                            timeRange=timeRange,
                            ms=1,
                            labels=freqLabels)
    plt.xlabel('Time from sound onset')
    plt.xlim(timeRange[0]+0.1,timeRange[1])
    plt.title(plotTitle)
    


def plot_tuning_PSTH_one_intensity(oneCell,intensity=50.0,timeRange=[-0.5,1],binWidth=0.010,halfFreqs=True):
    #calls load_remote_tuning_data(oneCell) to get the data, then plot raster
    eventOnsetTimes, spikeTimestamps, bdata = load_remote_tuning_data(oneCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    possibleIntensity = np.unique(intensityEachTrial)
    if len(possibleIntensity) != 1:
        intensity = intensity #50dB is the stimulus intensity used in 2afc task
        ###Just select the trials with a given intensity###
        trialsThisIntensity = [intensityEachTrial==intensity]
        freqEachTrial = freqEachTrial[trialsThisIntensity]
        intensityEachTrial = intensityEachTrial[trialsThisIntensity]
        eventOnsetTimes = eventOnsetTimes[trialsThisIntensity]
    possibleFreq = np.unique(freqEachTrial)
    if halfFreqs:
        possibleFreq = possibleFreq[1::3] #slice to get every other frequence presented
    numFreqs = len(possibleFreq)    
    #print len(intensityEachTrial),len(eventOnsetTimes),len(spikeTimestamps)
    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    #pdb.set_trace()  #for debug

    #colormap = plt.cm.gist_ncar
    #colorEachFreq = [colormap(i) for i in np.linspace(0, 0.9, numFreqs)]
    #from jaratoolbox.colorpalette import TangoPalette as Tango
    #colorEachFreq = [Tango['Aluminium3'], Tango['Orange2'],Tango['Chameleon1'],Tango['Plum1'],Tango['Chocolate1'],Tango['SkyBlue2'],Tango['ScarletRed1'],'k']
    #Creat colorEachCond from color map
    from matplotlib import cm
    cm_subsection = np.linspace(0.0, 1.0, numFreqs)
    colorEachFreq = [cm.winter(x) for x in cm_subsection]
    
    #Create legend
    import matplotlib.patches as mpatches
    handles = []
    for (freq, color) in zip(possibleFreq,colorEachFreq):
        patch = mpatches.Patch(color=color, label=str(freq)+' Hz')
        handles.append(patch)

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
        spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    smoothWinSize = 3
    #plt.figure()
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachFreq,colorEachCond=colorEachFreq,linestyle=None,linewidth=2,downsamplefactor=1)
    extraplots.set_ticks_fontsize(ax=plt.gca(),fontSize=14)
    plt.xlim(timeRange[0]+0.1,timeRange[1])
    plt.legend(handles=handles, loc=2)
    plt.xlabel('Time from sound onset (s)',fontsize=18)
    plt.ylabel('Firing rate (spk/sec)',fontsize=18)



def get_trials_each_cond_switching(oneCell, freqToPlot='middle', byBlock=True):
    '''
    Given a cellInfo object, the frequency to plot(string, value of 'middle' or 'all'), whether to plot by block (boolean), gets the trialsEachCond and colorEachCond vectors for raster and PSTH plotting.
    ''' 
    # -- Calls load_remote_2afc_data(oneCell) to get the data, then plot raster -- #
    (eventData, spkData, bdata) = load_remote_2afc_data(oneCell)
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
    # -- Select trials to plot based on desired frequencies to plot and whether to plot by block -- #
    if freqToPlot == 'middle':
        middleFreq = possibleFreq[numFreqs/2] #selects middle frequency, using int division resulting in int property. MAY FAIL IN THE FUTURE
        #pdb.set_trace()
        oneFreq = bdata['targetFrequency'] == middleFreq #vector for selecing trials presenting this frequency
        correctOneFreq = oneFreq  & correct 

        # -- Find trials each block (if plotting mid frequency by block) or find trials each type (e.g. low-boundary, high-boundary; if not plotting by block) -- #
        if byBlock:
            bdata.find_trials_each_block()
            trialsEachBlock = bdata.blocks['trialsEachBlock']
            correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
            correctBlockSizes = sum(correctTrialsEachBlock)
            if (correctBlockSizes[-1] < minBlockSize): #A check to see if last block is too small to plot
                correctTrialsEachBlock = correctTrialsEachBlock[:,:-1]

            trialsEachCond = correctTrialsEachBlock
            if bdata['currentBlock'][0]==bdata.labels['currentBlock']['low_boundary']:
                colorEachCond = 5*['g','r'] #assume there are not more than 5 blocks
            else:
                colorEachCond = 5*['r','g']
               
        else:
            currentBlock = bdata['currentBlock']
            blockTypes = [bdata.labels['currentBlock']['low_boundary'],bdata.labels['currentBlock']['high_boundary']]
            trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
            midFreqCorrectBlockLow = correctOneFreq&trialsEachType[:,0]
            midFreqCorrectBlockHigh = correctOneFreq&trialsEachType[:,1]
            trialsEachCond = np.c_[midFreqCorrectBlockLow,midFreqCorrectBlockHigh]
            colorEachCond = ['g','r']
 
    # -- When plotting all 3 frequencies will not be plotting by block, just plot by type of block (low_boundary vs high_boundary) -- #
    elif freqToPlot == 'all':
        assert byBlock == False  #when plotting all frequencies will not be plotting by block
        lowFreq = possibleFreq[0]
        middleFreq = possibleFreq[1]
        highFreq = possibleFreq[2]
        leftward = bdata['choice']==bdata.labels['choice']['left']
        rightward = bdata['choice']==bdata.labels['choice']['right']
 
        trialsToUseLowFreq = ((bdata['targetFrequency'] == lowFreq) & correct) #low_boundary block
        trialsToUseHighFreq = ((bdata['targetFrequency'] == highFreq) & correct) #high_boundary block
        trialsToUseMidFreqLeft = leftward & (bdata['targetFrequency'] == middleFreq) #mid freq correct trials in high_boundary block
        trialsToUseMidFreqRight = rightward & (bdata['targetFrequency'] == middleFreq)#mid freq correct trials in low_boundary block
        trialsEachCond = np.c_[trialsToUseLowFreq,trialsToUseMidFreqLeft,trialsToUseMidFreqRight,trialsToUseHighFreq]
        colorEachCond = ['y','r','g','b']
    
    return bdata, trialsEachCond, colorEachCond

def plot_switching_raster(oneCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True):
    '''
    Plots raster for 2afc switching task with different alignment at time 0 and different choices for what frequencies to include in the plot.
    Arguments:
        oneCell is a CellInfo object.
        freqToPlot is a string; 'middle' means plotting only the middle frequency, 'all' means plotting all three frequenciens.
        alignment should be a string with possible values: 'sound', 'center-out','side-in'.
        timeRange is a list of two floats, indicating the start and end of plot range.
        byBlock is a boolean, indicates whether to split the plot into behavior blocks.
    '''

    # -- calls load_remote_2afc_data(oneCell) to get the data, then plot raster -- #
    (eventData, spikeData, oldBdata) = load_remote_2afc_data(oneCell)
    spikeTimestamps = spikeData.timestamps
    # -- Get trialsEachCond and colorEachCond for plotting -- #
    (bdata,trialsEachCond, colorEachCond) = get_trials_each_cond_switching(oneCell=oneCell, freqToPlot=freqToPlot, byBlock=byBlock) #bdata generated here removed missing trials

    # -- Calculate eventOnsetTimes based on alignment parameter -- #
    eventOnsetTimes=np.array(eventData.timestamps)
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

    # -- Calculate matrix of spikes per trial for plotting -- #
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)
    
    # -- Plot raster -- #
    #plt.figure()
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    #plt.ylim()
    plt.xlabel('Time from {} (s)'.format(alignment),fontsize=18)
    plt.ylabel('Trials',fontsize=18)
    plt.xlim(timeRange[0]+0.1,timeRange[1])
    plt.title('{0}_{1}_T{2}c{3}_{4}_{5} frequency'.format(oneCell.animalName,oneCell.behavSession,oneCell.tetrode,oneCell.cluster,alignment,freqToPlot)) 
    #plt.fill([0,0.1,0.1,0],[plt.ylim()[0],plt.ylim()[0],plt.ylim()[1],plt.ylim()[1]],color='0.75')
    extraplots.set_ticks_fontsize(plt.gca(),fontSize=16)


def plot_switching_PSTH(oneCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True, binWidth=0.010):
    # -- calls load_remote_2afc_data(oneCell) to get the data, then plot raster -- #
    (eventData, spikeData, oldBdata) = load_remote_2afc_data(oneCell)
    spikeTimestamps = spikeData.timestamps
    # -- Get trialsEachCond and colorEachCond for plotting -- #
    (bdata, trialsEachCond, colorEachCond) = get_trials_each_cond_switching(oneCell=oneCell, freqToPlot=freqToPlot, byBlock=byBlock)

    # -- Calculate eventOnsetTimes based on alignment parameter -- #
    eventOnsetTimes=np.array(eventData.timestamps)
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
    
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    smoothWinSize = 3
    #plt.figure()
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=2,downsamplefactor=1)
    plt.xlabel('Time from {0} (s)'.format(alignment))
    plt.xlim(timeRange[0]+0.1,timeRange[1])
    plt.ylabel('Firing rate (spk/sec)')
    plt.fill([0,0.1,0.1,0],[plt.ylim()[0],plt.ylim()[0],plt.ylim()[1],plt.ylim()[1]],color='0.75')
    extraplots.set_ticks_fontsize(plt.gca(),fontSize=16)

def plot_psy_curve_raster(oneCell, alignment='sound'):
    pass


def plot_summary_per_cell(oneCell):
    '''
    Plots wave-from, ISI, projections
    '''
    pass

def save_report_plot(animal,date,tetrode,cluster,filePath,figFormat,chartType='report'):
    filename = '%s_%s_%s_%s_%s.%s'%(animal,date,tetrode,cluster,chartType,figFormat)
    fullFileName = os.path.join(filePath,filename)
    print 'saving figure to %s'%fullFileName
    plt.gcf().savefig(fullFileName)

def plot_ave_wave_form_w_peak_times(oneCell):
    spkData = load_remote_2afc_spikes(oneCell)
    waveforms = spkData.samples
    samplingRate = spkData.samplingRate
    sampVals = np.arange(0,waveforms.shape[2]/samplingRate,1/samplingRate)
    (peakTimes, peakAmplitudes, avWaveform) = spikesorting.estimate_spike_peaks(waveforms,samplingRate)
    plt.plot(sampVals,avWaveform, 'g-')
    plt.axvline(peakTimes[1],ls='--',color='r')
    plt.axvline(peakTimes[0],ls='--',color='0.75')
    plt.axvline(peakTimes[2],ls='--',color='0.75')
    



if __name__ == '__main__':
    ### Params associated with the cell of interest ###
    cellParams = {'behavSession':'20160124a',
                  'tetrode':4,
                  'cluster':6}

    ### Loading allcells file for a specified mouse ###
    mouseName = 'test089'
    #allcellsFileName = 'allcells_'+mouseName
    allcellsFileName = 'allcells_'+mouseName+'_quality' #This is specific to Billy's final allcells files after adding cluster quality info 
    sys.path.append(settings.ALLCELLS_PATH)

    allcells = importlib.import_module(allcellsFileName)

    ### Using cellDB methode to find the index of this cell in the cellDB ###
    cellIndex = allcells.cellDB.findcell(mouseName,**cellParams)
    #pdb.set_trace()
    # TEST, plotting cells with sig modulation in 20150624a behav session

    thisCell = allcells.cellDB[cellIndex]
    ephysSession = thisCell.ephysSession
    tuningSession = thisCell.tuningSession
    tuningBehavior = thisCell.tuningBehavior

    #(eventOnsetTimes, spikeTimestamps, bData) = load_remote_tuning_data(thisCell,BEHAVDIR_MOUNTED,EPHYSDIR_MOUNTED)
    #plt.style.use(['seaborn-white', 'seaborn-talk']) 
    #plt.figure()
    #plot_tuning_raster_one_intensity(thisCell)
    #plt.figure()
    #plot_tuning_PSTH_one_intensity(thisCell,timeRange=[-0.3,0.4],halfFreqs=True)
    #movement-selectivity plot
    filePath = '/tmp'
    plt.figure()
    plot_switching_raster(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,0.5],byBlock=True)
    save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='raster',figFormat='svg')
    plt.figure()
    plot_switching_PSTH(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,0.5],byBlock=True, binWidth=0.010)
    save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,filePath,chartType='PSTH',figFormat='svg')
    #plt.figure()
    #plot_switching_PSTH(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=False)
    #plt.figure()
    #plot_switching_raster(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=False)

    #plt.xlim
    plt.show()
    #plt.clf()
    '''
    (eventData, spikeData, bData) = load_remote_2afc_data(thisCell)
    spikeTimestamps = spikeData.timestamps
    spikeWaveforms = spikeData.samples

    plt.subplot2grid((8, 8), (0, 0), rowspan = 5, colspan = 4)
    plot_tuning_raster_one_intensity(thisCell)

    plt.subplot2grid((8, 8), (0, 4), rowspan = 5, colspan = 4)
    plot_switching_raster(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True)

    plt.subplot2grid((8, 8), (5, 4), rowspan = 2, colspan = 4)
    plot_switching_PSTH(thisCell, freqToPlot='middle', alignment='sound',timeRange=[-0.5,1],byBlock=True)

    # -- Plot ISI histogram --
    plt.subplot2grid((8, 8), (5,0), rowspan=1, colspan=4)
    spikesorting.plot_isi_loghist(spikeTimestamps)
    plt.ylabel('c%d'%thisCell.cluster,rotation=0,va='center',ha='center')
    plt.xlabel('')

    # -- Plot waveforms --
    plt.subplot2grid((8, 8), (6,0), rowspan=1, colspan=4)
    spikesorting.plot_waveforms(spikeWaveforms)

    # -- Plot projections --
    plt.subplot2grid((8, 8), (7,0), rowspan=1, colspan=4)
    spikesorting.plot_projections(spikeWaveforms)

    # -- Plot events in time --
    plt.subplot2grid((8, 8), (7,4), rowspan=1, colspan=4)
    spikesorting.plot_events_in_time(spikeTimestamps)

    #plt.show()
    outputDir = '/home/languo/data/ephys/'+thisCell.animalName+'/summary_plots/'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    save_report_plot(thisCell.animalName,thisCell.behavSession,thisCell.tetrode,thisCell.cluster,outputDir)
    '''
