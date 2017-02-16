'''
This script contains functions for loading and plotting various plots for cells recroded in the reward change frequency discrimination task.

Lan Guo 2017-02-15
'''
import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
#from jaratest.nick.database import dataloader_v2 as dataloader
#from jaratest.nick.database import dataplotter
import matplotlib.patches as mpatches

EPHYS_PATH = settings.EPHYS_PATH
BEHAVIOR_PATH = settings.BEHAVIOR_PATH

colorDictRC = {'leftMoreLowFreq':'g',
               'rightMoreLowFreq':'m',
               'sameRewardLowFreq':'y',
               'leftMoreHighFreq':'r',
               'rightMoreHighFreq':'b',
               'sameRewardHighfreq':'darkgrey'}

EPHYS_SAMPLING_RATE = 30000.0
soundTriggerChannel = 0

minBlockSize = 20 # Last blocks with valid trial number smaller than this is not plotted

def set_clusters_from_file(animal, session, tetrode):
    '''
    Get an array containing the cluster assignment of each spike detected in the tetrode for that ephys session.
    :param arg1: A string of the name of the ephys session. 
    :param arg2: An int in range(1,9) for tetrode number.
    :return: Array containing the cluster number of each spike.       
    '''
    clustersDir = os.path.join(EPHYS_PATH, animal, session+'_kk')
    if not os.path.exists(clustersDir):
        print 'This session has not been clustered! Please cluster it first.'
        return None
    else:
        clusterFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
        clusterList = np.fromfile(clusterFile,dtype='int32',sep=' ')[1:]
        return clusterList

def load_event_data(animal, ephysSession):
    fullEventFilename=os.path.join(EPHYS_PATH, animal, ephysSession, 'all_channels.events')
    eventData = loadopenephys.Events(fullEventFilename)
    eventData.timestamps = np.array(eventData.timestamps)/EPHYS_SAMPLING_RATE #hard-coded ephys sampling rate!!
    return eventData
    
def load_spike_data(animal, ephysSession, tetrode, cluster):
    '''
    Function to load spike data of just one isolated cluster. 
    '''
    spikeFilename = os.path.join(EPHYS_PATH,animal,ephysSession, 'Tetrode{}.spikes'.format(tetrode))
    spikeData = loadopenephys.DataSpikes(spikeFilename)
    spikeData.timestamps = spikeData.timestamps/EPHYS_SAMPLING_RATE
    clustersDir = os.path.join(EPHYS_PATH,animal,ephysSession)+'_kk'
    clusterFilename = os.path.join(clustersDir, 'Tetrode{}.clu.1'.format(tetrode))
    clusters = np.fromfile(clusterFilename, dtype='int32', sep=' ')[1:]
    spikeData.timestamps = spikeData.timestamps[clusters==cluster]
    spikeData.samples = spikeData.samples[clusters==cluster, :, :]
    spikeData.samples = spikeData.samples.astype(float)-2**15# FIXME: this is specific to OpenEphys
    # FIXME: This assumes the gain is the same for all channels and records
    spikeData.samples = (1000.0/spikeData.gain[0,0]) * spikeData.samples
    return spikeData

def load_behavior_basic(animal, behavSession):
    '''
    Load behavior using the basic BehaviorData class of loadbehavior module.
    '''
    behavFullPath = os.path.join(BEHAVIOR_PATH, animal, behavSession) 
    bData = loadbehavior.BehaviorData(behavFullPath)
    return bData

def load_behavior_flexcat(animal, behavSession):
    '''
    Load behavior using the FlexCategBehaviorData class of loadbehavior module.
    '''
    behavFullPath = os.path.join(BEHAVIOR_PATH, animal, behavSession) 
    bData = loadbehavior.FlexCategBehaviorData(behavFullPath)
    return bData


def plot_tuning_raster(animal, ephysSession, behavSession, tetrode, cluster, intensity=50, timeRange = [-0.5,1]):
    '''
    Function to plot a tuning raster sorted by frequency. 
    :param arg1: A string of the file name of the tuning curve ephys session.
    :param arg2: A string of the file name of the tuning curve behavior session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :param arg5: An int for the intensity in (dB) to plot, default is 50(dB), which is the stimulus intensity used in 2afc task.
    :param arg6: A list of floats for the start and the end of the time period around sound-onset to plot raster.
    '''
    
    bdata = load_behavior_basic(animal,behavSession)
    
    spikeData = load_spike_data(animal, ephysSession, tetrode, cluster)
    spikeTimestamps = spikeData.timestamps
    eventData = load_event_data(animal, ephysSession)
    eventOnsetTimes = np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    eventOnsetTimes = eventOnsetTimes[soundOnsetEvents]
    
    freqEachTrial = bdata['currentFreq']
    intensityEachTrial = bdata['currentIntensity']
    possibleFreq = np.unique(freqEachTrial)
    possibleIntensity = np.unique(intensityEachTrial)
    if len(possibleIntensity) != 1:
        intensity = intensity 
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
    plotTitle = 'Tt'+str(tetrode)+'c'+str(cluster)+' tuning with 50dB chords'
    ### FIXME: this is a bad hack for when ephys is one trial more than behavior file ###
    if len(eventOnsetTimes)==len(intensityEachTrial)+1:
        eventOnsetTimes=eventOnsetTimes[:-1]
    #print len(intensityEachTrial),len(eventOnsetTimes),len(spikeTimestamps)
   
    #plt.figure()
    dataplotter.plot_raster(spikeTimestamps,
                            eventOnsetTimes,
                            sortArray=freqEachTrial,
                            timeRange=timeRange,
                            ms=1,
                            labels=freqLabels)
    plt.xlabel('Time from sound onset')
    plt.xlim(timeRange[0]+0.1,timeRange[1])
    plt.title(plotTitle,fontsize=10)
    

def load_n_remove_missing_trials_2afc_behav(animal, behavSession, ephysSession, tetrode, cluster):
    '''
    Loads a 2afc behavior session, compare the number of trials recorded to the corresponding ephys session and removes trials that were not recorded in the ephys session.
    :param arg1: A string of the file name of the 2afc curve behavior session.
    :param arg2: A string of the file name of the 2afc curve ephys session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :return: bData object with missing trials removed in all fields
    '''
    bData = load_behavior_flexcat(animal, behavSession) #need extra methods
    
    eventData = load_event_data(animal,ephysSession)
    
    eventOnsetTimes=np.array(eventData.timestamps)
    soundOnsetEvents = (eventData.eventID==1) & (eventData.eventChannel==soundTriggerChannel)
    soundOnsetTimeEphys = eventOnsetTimes[soundOnsetEvents]
    soundOnsetTimeBehav = bData['timeTarget']
    
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bData.remove_trials(missingTrials)

    return bData


def get_trials_each_cond_reward_change(animal, behavSession, ephysSession, tetrode, cluster, freqToPlot, byBlock, colorCondDict):
    '''
    Function to generate selection vector showing which trials to plot for each behavior conditions and the color to use in the plot label.
    :param arg1: A string of the file name of the 2afc curve behavior session.
    :param arg2: A string of the file name of the 2afc curve ephys session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :param arg5: A string indicating which frequency to plot, value of 'low' or 'high'.
    :param arg6: Boolean indicating whether to split the plot by behavior blocks. 
    :param arg7: A dictionary indicating which color label each behavior condition gets in the final plot.
    
    :return: bData object, trialsEachCond, colorsEachCond
    '''
    
    bdata = load_n_remove_missing_trials_2afc_behav(animal, behavSession, ephysSession, tetrode, cluster)

    # -- Select trials to plot from behavior file -- #
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)
    currentBlock = bdata['currentBlock']
    # -- Select trials to plot based on desired frequencies to plot and whether to plot by block -- #
    ### Recordings during reward change usually have 2 frequencies, low freq means go to left, right freq means go to right ###
    if freqToPlot == 'low':
        freq = possibleFreq[0] 

    elif freqToPlot == 'high':
        freq = possibleFreq[1]

    oneFreq = bdata['targetFrequency'] == freq #vector for selecing trials presenting this frequency
    correctOneFreq = oneFreq  & correct 

    # -- Find trials each block (if plotting mid frequency by block) or find trials each type (e.g. low-boundary, high-boundary; if not plotting by block) -- #
    if byBlock:
        bdata.find_trials_each_block()
        numBlocks = bdata.blocks['nBlocks']
        trialsEachBlock = bdata.blocks['trialsEachBlock']
        correctTrialsEachBlock = trialsEachBlock & correctOneFreq[:,np.newaxis]
        correctBlockSizes = sum(correctTrialsEachBlock)
        if (correctBlockSizes[-1] < minBlockSize): #A check to see if last block is too small to plot
            correctTrialsEachBlock = correctTrialsEachBlock[:,:-1]
            numBlocks -= 1
        trialsEachCond = correctTrialsEachBlock
        currentBlockLabelEachBlock = trialsEachBlock & currentBlock[:,np.newaxis]
        colorEachCond = np.empty(numBlocks)
        for blockNum in numBlocks:
            currentBlockLabel = currentBlockLabelEachBlock[:,blockNum][0]
            if freqToPlot == 'low':
                if currentBlockLabel == bdata.labels['currentBlock']['same_reward']:
                    colorEachCond[blockNum] = colorCondDict['sameRewardLowFreq']
                elif currentBlockLabel == bdata.labels['currentBlock']['more_left']:
                    colorEachCond[blockNum] = colorCondDict['leftMoreLowFreq'] 
                elif currentBlockLabel == bdata.labels['currentBlock']['more_right']:   
                    colorEachCond[blockNum] = colorCondDict['rightMoreLowFreq']
            elif freqToPlot == 'high':
                if currentBlockLabel == bdata.labels['currentBlock']['same_reward']:
                    colorEachCond[blockNum] = colorCondDict['sameRewardHighFreq']
                elif currentBlockLabel == bdata.labels['currentBlock']['more_left']:
                    colorEachCond[blockNum] = colorCondDict['leftMoreHighFreq'] 
                elif currentBlockLabel == bdata.labels['currentBlock']['more_right']:   
                    colorEachCond[blockNum] = colorCondDict['rightMoreHighFreq']

    else:
        blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        oneFreqCorrectBlockSameReward = correctOneFreq&trialsEachType[:,0]
        oneFreqCorrectBlockMoreLeft = correctOneFreq&trialsEachType[:,1]
        oneFreqCorrectBlockMoreRight = correctOneFreq&trialsEachType[:,2]
        
        trialsEachCond = np.c_[oneFreqCorrectBlockSameReward,oneFreqCorrectBlockMoreLeft,oneFreqCorrectBlockMoreRight]
        if freqToPlot == 'low':
            colorEachCond = [colorCondDict['sameRewardLowFreq'],colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
        elif freqToPlot == 'high':
            colorEachCond = [colorCondDict['sameRewardHighfreq'],colorCondDict['leftMoreHighFreq'],colorCondDict['rightMoreHighFreq']]

    return trialsEachCond, colorEachCond

'''  

        if bdata['automationMode'][0]==bdata.labels['automationMode']['same_left_right']:
            if freqToPlot == 'low':
                colorEachCond = numBlocks*[colorCondDict['sameRewardLowFreq'],colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
            if freqToPlot == 'high':
                colorEachCond = numBlocks*[colorCondDict['sameRewardHighfreq'],colorCondDict['leftMoreHighFreq'],colorCondDict['rightMoreHighFreq']]
        elif bdata['automationMode'][0]==bdata.labels['automationMode']['same_right_left']:
            if freqToPlot == 'low':
                colorEachCond = numBlocks*[colorCondDict['sameRewardLowFreq'],colorCondDict['rightMoreLowFreq'],colorCondDict['leftMoreLowFreq']]
            if freqToPlot == 'high':
                colorEachCond = numBlocks*[colorCondDict['sameRewardHighfreq'],colorCondDict['rightMoreHighFreq'],colorCondDict['leftMoreHighFreq']]
        elif bdata['automationMode'][0]==bdata.labels['automationMode']['left_right_left']:
            if freqToPlot == 'low':
                colorEachCond = numBlocks*[colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
            if freqToPlot == 'high':
                colorEachCond = numBlocks*[colorCondDict['leftMoreHighFreq'],colorCondDict['rightMoreHighFreq']]
     
# -- When plotting all 3 frequencies will not be plotting by block, just plot by type of block (low_boundary vs high_boundary) -- #
    elif freqToPlot == 'both':
        lowFreq = possibleFreq[0]
        highfreq = possibleFreq[1]
    
        if byBlock == False:  
            blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
            trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)

            correctLowFreq = lowFreq & correct
            correctHighfreq = highfreq & correct
            trialsToUseLowFreqSameReward = correctLowFreq&trialsEachType[:,0]
            trialsToUseLowFreqLeftMore = correctLowFreq&trialsEachType[:,1]
            trialsToUseLowFreqRightMore = correctLowFreq&trialsEachType[:,2]
            trialsToUseHighfreqSameReward = correctHighfreq&trialsEachType[:,0]
            trialsToUseHighfreqLeftMore = correctHighfreq&trialsEachType[:,1]
            trialsToUseHighfreqRightMore = correctHighfreq&trialsEachType[:,2]

            trialsEachCond = np.c_[trialsToUseLowFreqSameReward,trialsToUseLowFreqLeftMore,trialsToUseLowFreqRightMore,trialsToUseHighfreqSameReward,trialsToUseHighfreqLeftMore,trialsToUseHighfreqRightMore]
            colorEachCond = [colorCondDict['sameRewardLowFreq'],colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq'],colorCondDict['sameRewardHighfreq'],colorCondDict['leftMoreHighFreq'],colorCondDict['rightMoreHighFreq']]
        elif byBlock == True:
            bdata.find_trials_each_block()
            trialsEachBlock = bdata.blocks['trialsEachBlock']
            correctTrialsEachBlock = trialsEachBlock & correct[:,np.newaxis]
            correctBlockSizes = sum(correctTrialsEachBlock)
            if (correctBlockSizes[-1] < minBlockSize): #A check to see if last block is too small to plot
                correctTrialsEachBlock = correctTrialsEachBlock[:,:-1]

            trialsEachCond = correctTrialsEachBlock

'''


def get_intermediate_data_for_raster_psth(animal, behavSession, ephysSession, tetrode, cluster, alignment, timeRange, binWidth):
    '''
    Function to generate the intermediate data needed to plot raster and psth for reward_change_freq_dis task. 
    :param arg1: A string of the file name of the 2afc curve behavior session.
    :param arg2: A string of the file name of the 2afc curve ephys session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :param arg5: A string indicating which frequency to plot, value of 'low' or 'high', or 'both'.
    :param arg6: Boolean indicating whether to split the plot by behavior blocks. NOTE: should set it to false when plotting all frequencies(freqToPlot='both').
    :param arg7: A dictionary indicating which color label each behavior condition gets in the final plot.
    :param arg8: A string indicating the event to align the spike times to, can be 'sound', 'center-out', or 'side-in'.
    :return:
    
    '''
    bdata = load_n_remove_missing_trials_2afc_behav(animal, behavSession, ephysSession, tetrode, cluster)
    
    ### Get events data ###
    eventData = load_event_data(animal, ephysSession)
    
    spikeData = load_spike_data(animal, ephysSession, tetrode, cluster)
    spikeTimestamps = spikeData.timestamps

    eventOnsetTimes = np.array(eventData.timestamps)

    # -- determine spike time based on event to align spikes to -- #
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
       
    return spikeTimesFromEventOnset,indexLimitsEachTrial


def plot_reward_change_raster(animal, behavSession, ephysSession, tetrode, cluster, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010, freqToPlot='low', byBlock=False, colorCondDict=colorDictRC):
    '''
    Function to plot reward change raster.
    '''
    spikeTimesFromEventOnset,indexLimitsEachTrial = get_intermediate_data_for_raster_psth(animal, behavSession, ephysSession, tetrode, cluster, alignment, timeRange, binWidth)

    if freqToPlot == 'low' or freqToPlot=='high':
        trialsEachCond, colorEachCond = get_trials_each_cond_reward_change(animal, behavSession, ephysSession, tetrode, cluster, freqToPlot=freqToPlot, byBlock=byBlock, colorCondDict=colorCondDict)
    elif freqToPlot == 'both':
        trialsEachCondList = []
        colorEachCond = []
        for freq in ['low','high']:
            trialsEachCondThisFreq, colorEachCondThisFreq = get_trials_each_cond_reward_change(animal, behavSession, ephysSession, tetrode, cluster, freqToPlot=freq, byBlock=byBlock, colorCondDict=colorCondDict)
            trialsEachCondList.append(trialsEachCondThisFreq)
            colorEachCond.extend(colorEachCondThisFreq)
        trialsEachCond = np.concatenate(trialsEachCondList, axis=1)
    
    # -- Plot raster -- #
    #plt.subplot2grid((3,1), (0, 0), rowspan=2)
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.ylabel('Trials')
    plt.xlim(timeRange[0]+0.1,timeRange[-1])
    plt.title('{0}_TT{1}_c{2}_{3}'.format(behavSession,tetrode,cluster,alignment),fontsize=10)
   

def plot_reward_change_psth(animal, behavSession, ephysSession, tetrode, cluster, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010, freqToPlot='low', byBlock=False, colorCondDict=colorDictRC, smoothWinSize=3):
    '''
    Function to plot reward change psth.
    '''
    spikeTimesFromEventOnset,indexLimitsEachTrial = get_intermediate_data_for_raster_psth(animal, behavSession, ephysSession, tetrode, cluster, alignment, timeRange, binWidth)
    
    if freqToPlot == 'low' or freqToPlot=='high':
        trialsEachCond, colorEachCond = get_trials_each_cond_reward_change(animal, behavSession, ephysSession, tetrode, cluster, freqToPlot=freqToPlot, byBlock=byBlock, colorCondDict=colorCondDict)
    elif freqToPlot == 'both':
        trialsEachCondList = []
        colorEachCond = []
        for freq in ['low','high']:
            trialsEachCondThisFreq, colorEachCondThisFreq = get_trials_each_cond_reward_change(animal, behavSession, ephysSession, tetrode, cluster, freqToPlot=freq, byBlock=byBlock, colorCondDict=colorCondDict)
            trialsEachCondList.append(trialsEachCondThisFreq)
            colorEachCond.extend(colorEachCondThisFreq)
        trialsEachCond = np.concatenate(trialsEachCondList, axis=1)
    
    # -- Plot PSTH -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    smoothWinSize = smoothWinSize
    #plt.subplot2grid((3,1), (2, 0))
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)
    # -- Add legend -- #
    low_leftmore_patch = mpatches.Patch(color=colorDictRC['leftMoreLowFreq'], label='low leftmore')
    low_rightmore_patch = mpatches.Patch(color=colorDictRC['rightMoreLowFreq'], label='low rightmore')
    high_leftmore_patch = mpatches.Patch(color=colorDictRC['leftMoreHighFreq'], label='high leftmore')
    high_rightmore_patch = mpatches.Patch(color=colorDictRC['rightMoreHighFreq'], label='high rightmore')
    plt.legend(handles=[low_leftmore_patch,low_rightmore_patch, high_leftmore_patch,high_rightmore_patch], loc='upper center', fontsize=10, frameon=False, labelspacing=0.1, handlelength=0.2)
    plt.axvline(x=0,linewidth=1, color='darkgrey')
    plt.xlabel('Time from {0} onset (s)'.format(alignment))
    plt.ylabel('Firing rate (spk/sec)')
    plt.xlim(timeRange[0]+0.1,timeRange[-1])
