'''
This script contains functions for plotting various plots for cells recroded in the reward change frequency discrimination task.
UPDATED TO USE NEW CELLDB LOADING CAPABILITITES 
Lan Guo 2018-02-15
'''
import os
import numpy as np
import pdb
import matplotlib.pyplot as plt
from jaratoolbox import settings
from jaratoolbox import ephyscore
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import extraplots
import matplotlib.patches as mpatches

EPHYS_PATH = settings.EPHYS_PATH_REMOTE
BEHAVIOR_PATH = settings.BEHAVIOR_PATH

colorDictRC = {'leftMoreLowFreq':'g',
               'rightMoreLowFreq':'m',
               #'sameRewardLowFreq':'y',
               'leftMoreHighFreq':'r',
               'rightMoreHighFreq':'b',
               #'sameRewardHighFreq':'darkgrey'
}


colorDictMovement = {'left':'g',
                     'right':'r'}

soundChannelType = 'stim'

minBlockSize = 20 # Last blocks with valid trial number smaller than this is not plotted

def plot_waveform_each_cluster(cellObj, sessionType='tc'):
    '''Function to plot average and individual waveforms for one isolated cluster. 
    :param arg1: Cell object from ephyscore.
    :param arg2: A string of the type of the ephys session to use. 
    '''
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData = cellObj.load_ephys_by_index(sessionInd) 
    wavesThisCluster = ephysData['samples']
    spikesorting.plot_waveforms(wavesThisCluster)


def plot_projections_each_cluster(cellObj, sessionType='tc'):
    '''Function to plot the projection cloud of a given cluster.
    :param arg1: Cell object from ephyscore.
    :param arg2: A string of the type of the ephys session to use. 
    '''
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData = cellObj.load_ephys_by_index(sessionInd) 
    wavesThisCluster = ephysData['samples']
    spikesorting.plot_projections(wavesThisCluster)


def plot_events_in_time_each_cluster(cellObj, sessionType='tc'):
    '''Function to plot the average firing rate over time for a cluster in a recording session.
    :param arg1: Cell object from ephyscore.
    :param arg2: A string of the type of the ephys session to use. 
    '''
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData = cellObj.load_ephys_by_index(sessionInd) 
    spikeTimestamps = ephysData['spikeTimes']
    
    spikesorting.plot_events_in_time(spikeTimestamps)


def plot_isi_loghist_each_cluster(cellObj, sessionType='tc'):
    '''Function to plot the ISI of a given cluster.
    :param arg1: Cell object from ephyscore.
    :param arg2: A string of the type of the ephys session to use.
    '''
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData = cellObj.load_ephys_by_index(sessionInd) 
    spikeTimestamps = ephysData['spikeTimes']
    
    spikesorting.plot_isi_loghist(spikeTimestamps)


def plot_tuning_raster(cellObj, sessionType='tc', intensity=50, timeRange = [-0.5,1]):
    '''
    Function to plot a tuning raster sorted by frequency. 
    :param arg1: Cell object from ephyscore.
    :param arg2: A string for the session type, for tuning it should be 'tc'.
    :param arg3: An int for the intensity in (dB) to plot, default is 50(dB), which is the stimulus intensity used in 2afc task.
    :param arg4: A list of floats for the start and the end of the time period around sound-onset to plot raster.
    '''
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    bdata = cellObj.load_behavior_by_index(sessionInd)
    ephysData = cellObj.load_ephys_by_index(sessionInd) 
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]
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
        soundOnsetTimes = soundOnsetTimes[trialsThisIntensity]
    
    #print len(intensityEachTrial),len(eventOnsetTimes),len(spikeTimestamps)

    freqLabels = ['{0:.1f}'.format(freq/1000.0) for freq in possibleFreq]
    #intensityLabels = ['{:.0f} dB'.format(intensity) for intensity in possibleIntensity]        
    
    ### FIXME: this is a bad hack for when ephys is one trial more than behavior file ###
    if len(soundOnsetTimes)==len(freqEachTrial)+1:
        soundOnsetTimes=soundOnsetTimes[:-1]
        print('Tuning behavior is one trial less than ephys!')
        ### FIXME: this is a bad hack for when behavior is one trial more than ephys file ###
    if len(soundOnsetTimes)==len(freqEachTrial)-1:
        freqEachTrial=freqEachTrial[:-1]
        print('Tuning behavior is one trial more than ephys!')
    #print len(freqEachTrial),len(eventOnsetTimes),len(spikeTimestamps)
    
    trialsEachFreq = behavioranalysis.find_trials_each_type(freqEachTrial,possibleFreq)
    
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimestamps,soundOnsetTimes,timeRange)
    
    pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                   indexLimitsEachTrial,
                                                   timeRange,
                                                   trialsEachCond=trialsEachFreq,
                                                   labels=freqLabels)
    plt.xlabel('Time from sound onset')
    plt.xlim(timeRange[0]+0.1,timeRange[1])
    plotTitle = 'tuning with 50dB chords'  
    plt.title(plotTitle,fontsize=10)

    

def load_n_remove_missing_trials_2afc_behav(cellObj, behavClass=loadbehavior.FlexCategBehaviorData):
    '''Loads a 2afc behavior session, compare the number of trials recorded to the corresponding ephys session and removes trials that were not recorded in the ephys session.
    :param arg1: Cell object from ephyscore.
    :param arg2: behavClass (jaratoolbox.loadbehavior Class). The loading class to use, each class of behavData will have different methods.
    :return: bData object with missing trials removed in all fields
    '''
    sessionType = 'behavior'
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData, bdata = cellObj.load_by_index(sessionInd, behavClass=behavClass)
   
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimeEphys = eventsDict['{}On'.format(soundChannelType)]
    soundOnsetTimeBehav = bdata['timeTarget']
    
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bdata.remove_trials(missingTrials)

    return bdata


def get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass=loadbehavior.FlexCategBehaviorData):
    '''Function to generate selection vector showing which trials to plot for each behavior conditions and the color to use in the plot label.
    :param arg1: Cell object from ephyscore.
    :param arg2: A string indicating which frequency to plot, value of 'low' or 'high'.
    :param arg3: Boolean indicating whether to split the plot by behavior blocks. 
    :param arg4: A dictionary indicating which color label each behavior condition gets in the final plot.
    :param arg5: behavClass (jaratoolbox.loadbehavior Class). The loading class to use, each class of behavData will have different methods.
    
    :return: bData object, trialsEachCond, colorsEachCond
    '''
    
    bdata = load_n_remove_missing_trials_2afc_behav(cellObj, behavClass=behavClass)

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
        
        colorEachCond = np.empty(numBlocks, dtype=object)
        labelEachCond = np.empty(numBlocks, dtype=object)
        #pdb.set_trace()
        for blockNum in range(numBlocks):
            currentBlockLabel = currentBlock[trialsEachBlock[:,blockNum]][0]
            # Do not plot 'same_reward' blocks
            if currentBlockLabel == bdata.labels['currentBlock']['same_reward']:
                trialsEachCond[:,blockNum] = False 
            if freqToPlot == 'low':
                if currentBlockLabel == bdata.labels['currentBlock']['more_left']:
                    colorEachCond[blockNum] = colorCondDict['leftMoreLowFreq'] 
                    labelEachCond[blockNum] = 'low freq left more'
                elif currentBlockLabel == bdata.labels['currentBlock']['more_right']:   
                    colorEachCond[blockNum] = colorCondDict['rightMoreLowFreq']
                    labelEachCond[blockNum] = 'low freq right more'
            elif freqToPlot == 'high':
                if currentBlockLabel == bdata.labels['currentBlock']['more_left']:
                    colorEachCond[blockNum] = colorCondDict['leftMoreHighFreq'] 
                    labelEachCond[blockNum] = 'high freq left more'
                elif currentBlockLabel == bdata.labels['currentBlock']['more_right']:   
                    colorEachCond[blockNum] = colorCondDict['rightMoreHighFreq']
                    labelEachCond[blockNum] = 'high freq right more'

    else:
        blockTypes = [bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
        trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
        #oneFreqCorrectBlockSameReward = correctOneFreq&trialsEachType[:,0]
        oneFreqCorrectBlockMoreLeft = correctOneFreq&trialsEachType[:,1]
        oneFreqCorrectBlockMoreRight = correctOneFreq&trialsEachType[:,2]
        
        trialsEachCond = np.c_[oneFreqCorrectBlockMoreLeft,oneFreqCorrectBlockMoreRight]
        if freqToPlot == 'low':
            colorEachCond = [colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
            labelEachCond = ['low freq left more', 'low freq right more']
        elif freqToPlot == 'high':
            colorEachCond = [colorCondDict['leftMoreHighFreq'],colorCondDict['rightMoreHighFreq']]
            labelEachCond = ['high freq left more', 'high freq right more']
    return trialsEachCond, colorEachCond, labelEachCond


def get_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass=loadbehavior.FlexCategBehaviorData):
    '''Function to generate the intermediate data needed to plot raster and psth for reward_change_freq_dis task. 
    :param arg1: cell object from ephyscore
    :param arg2: A string indicating the event to align the spike times to, can be 'sound', 'center-out', or 'side-in'.
    :param arg3: A list of floats for the start and the end of the time period around sound-onset to plot raster.
    :param arg4: behavClass (jaratoolbox.loadbehavior Class). The loading class to use, each class of behavData will have different methods.
    :return: spikeTimesFromEventOnset(spike times aligned to event onset of choice), indexLimitsEachTrial(start and end index for spikes in each trial). 
    '''
    bdata = load_n_remove_missing_trials_2afc_behav(cellObj, behavClass=behavClass)
    
    ### Get events data ###
    sessionType = 'behavior'
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData = cellObj.load_ephys_by_index(sessionInd)
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]

    if len(bdata['timeTarget']) != len(soundOnsetTimes):
        print('2afc ephys and behavior donot have same number of trials. And it is NOT handled by remove_missing_trials!')
        spikeTimesFromEventOnset = np.zeros(())
        trialIndexForEachSpike = np.zeros(())
        indexLimitsEachTrial = np.zeros(())
    else:
        # -- determine spike time based on event to align spikes to -- #
        if alignment == 'sound':
            EventOnsetTimes = soundOnsetTimes
        elif alignment == 'center-out':
            diffTimes= bdata['timeCenterOut'] - bdata['timeTarget']
            EventOnsetTimes = soundOnsetTimes + diffTimes
        elif alignment == 'side-in':
            diffTimes= bdata['timeSideIn'] - bdata['timeTarget']
            EventOnsetTimes = soundOnsetTimes + diffTimes

        (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
    spikesanalysis.eventlocked_spiketimes(spikeTimestamps,EventOnsetTimes,timeRange)
       
    return spikeTimesFromEventOnset,indexLimitsEachTrial


def plot_reward_change_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='sound', timeRange=[-0.3,0.4], freqToPlot='low', byBlock=False, colorCondDict=colorDictRC):
    '''
    Function to plot reward change raster.
    '''
    spikeTimesFromEventOnset,indexLimitsEachTrial = get_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass) 
    if np.any(spikeTimesFromEventOnset):
        if freqToPlot == 'low' or freqToPlot=='high':
            trialsEachCond, colorEachCond, labelEachCond = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass) 

        elif freqToPlot == 'both':
            trialsEachCondList = []
            colorEachCond = []
            labelEachCond = []
            for freq in ['low','high']:
                trialsEachCondThisFreq, colorEachCondThisFreq, labelEachCondThisFreq  = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass)
                trialsEachCondList.append(trialsEachCondThisFreq)
                colorEachCond.extend(colorEachCondThisFreq)
                labelEachCond.extend(labelEachCondThisFreq)
            trialsEachCond = np.concatenate(trialsEachCondList, axis=1)

        # -- Plot raster -- #
        extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
        plt.axvline(x=0,linewidth=1, color='darkgrey')
        plt.ylabel('Trials')
        plt.xlim(timeRange[0]+0.1,timeRange[-1])
        plt.title('{0}_{1}freq'.format(alignment,freqToPlot),fontsize=10)
    else:
       pass

def plot_reward_change_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010, freqToPlot='low', byBlock=False, colorCondDict=colorDictRC, smoothWinSize=3):
    '''
    Function to plot reward change psth.
    '''
    spikeTimesFromEventOnset,indexLimitsEachTrial = get_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass)
    if np.any(spikeTimesFromEventOnset):
        if freqToPlot == 'low' or freqToPlot=='high':
            trialsEachCond, colorEachCond, labelEachCond = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass)
        elif freqToPlot == 'both':
            trialsEachCondList = []
            colorEachCond = []
            labelEachCond = []
            for freq in ['low','high']:
                trialsEachCondThisFreq, colorEachCondThisFreq, labelEachCondThisFreq = get_trials_each_cond_reward_change(cellObj, freqToPlot, byBlock, colorCondDict, behavClass)
                trialsEachCondList.append(trialsEachCondThisFreq)
                colorEachCond.extend(colorEachCondThisFreq)
                labelEachCond.extend(labelEachCondThisFreq)
            trialsEachCond = np.concatenate(trialsEachCondList, axis=1)

        # -- Plot PSTH -- #
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
        smoothWinSize = smoothWinSize
        #plt.subplot2grid((3,1), (2, 0))
        pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)

        # -- Add legend -- #
        for ind,line in enumerate(pPSTH):
            plt.setp(line, label=labelEachCond[ind])
            plt.legend(loc='upper right', fontsize=10, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)

        plt.axvline(x=0,linewidth=1, color='darkgrey')
        plt.xlabel('Time from {0} onset (s)'.format(alignment))
        plt.ylabel('Firing rate (spk/sec)')
        plt.xlim(timeRange[0]+0.1,timeRange[-1])
    else:
        pass

def plot_movement_response_raster(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5], colorCondDict=colorDictMovement):
    '''
    Function to plot activity during movement as raster.
    '''
    spikeTimesFromEventOnset,indexLimitsEachTrial = get_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass)
    bdata = load_n_remove_missing_trials_2afc_behav(cellObj, behavClass)
    if np.any(spikeTimesFromEventOnset):
        # -- Select trials to plot from behavior file -- #
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left']

        condLabels = ['go left', 'go right']
        trialsEachCond = np.c_[leftward,rightward] 
        colorEachCond = [colorCondDict['left'],colorCondDict['right']]

        # -- Plot raster -- #
        #plt.subplot2grid((3,1), (0, 0), rowspan=2)
        extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
        plt.axvline(x=0,linewidth=1, color='darkgrey')
        plt.ylabel('Trials')
        plt.xlim(timeRange[0]+0.1,timeRange[-1])
        plt.title('{}_movement_response'.format(alignment),fontsize=10)
    else:
        pass

def plot_movement_response_psth(cellObj, behavClass=loadbehavior.FlexCategBehaviorData, alignment='center-out', timeRange=[-0.3,0.5], binWidth=0.010, colorCondDict=colorDictMovement, smoothWinSize=3):
    '''
    Function to plot activity during movement as psth.
    '''
    spikeTimesFromEventOnset,indexLimitsEachTrial = get_intermediate_data_for_raster_psth(cellObj, alignment, timeRange, behavClass)
    if np.any(spikeTimesFromEventOnset):
        bdata = load_n_remove_missing_trials_2afc_behav(cellObj, behavClass)

        # -- Select trials to plot from behavior file -- #
        rightward = bdata['choice']==bdata.labels['choice']['right']
        leftward = bdata['choice']==bdata.labels['choice']['left']

        condLabels = ['go left', 'go right']
        trialsEachCond = np.c_[leftward,rightward] 
        colorEachCond = [colorCondDict['left'],colorCondDict['right']]

        # -- Plot PSTH -- #
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
        smoothWinSize = smoothWinSize
        #plt.subplot2grid((3,1), (2, 0))
        pPSTH = extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)
        # -- Add legend -- #
        for ind,line in enumerate(pPSTH):
            plt.setp(line, label=condLabels[ind])
            plt.legend(loc='upper right', fontsize=10, handlelength=0.2, frameon=False, labelspacing=0, borderaxespad=0.1)
        plt.axvline(x=0,linewidth=1, color='darkgrey')
        plt.xlabel('Time from {0} onset (s)'.format(alignment))
        plt.ylabel('Firing rate (spk/sec)')
        plt.xlim(timeRange[0]+0.1,timeRange[-1])
    else:
        pass

def plot_noisebursts_response_raster(cellObj, timeRange=[-0.1, 0.3]):
    '''
    Function to plot noisebursts along with waveforms for each cluster to distinguish cell responses and noise.
    '''
    sessionType = 'nb'
    sessionInd = cellObj.get_session_inds(sessionType)[0]
    ephysData, bdata = cellObj.load_by_index(sessionInd, behavClass=behavClass)
   
    eventsDict = ephysData['events']
    spikeTimestamps = ephysData['spikeTimes']
    soundOnsetTimes = eventsDict['{}On'.format(soundChannelType)]
    
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps, soundOnsetTimes, timeRange)
    # -- Plot raster -- #
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=[],fillWidth=None,labels=None)
    plt.ylabel('Trials')
    plt.xlabel('Time from sound onset (s)')
    
