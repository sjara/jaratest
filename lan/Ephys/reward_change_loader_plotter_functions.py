'''
This script contains functions for loading and plotting various plots for cells recroded in the reward change frequency discrimination task.
The unit of plotting is a 'site' as defined in inforec files and nick's celldatabase class.
Lan Guo 2017-02-15
'''
import os
import numpy as np
from jaratoolbox import settings
from jaratoolbox import behavioranalysis
from jaratoolbox import spikeanalysis
from jaratoolbox import extraplots
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.nick.database import dataplotter

EPHYS_PATH = settings.EPHYS_PATH
BEHAVIOR_PATH = settings.BEHAVIOR_PATH

colorDictRC = {'leftMoreLowFreq':'g',
               'rightMoreLowFreq':'m',
               'sameRewardLowFreq':'y',
               'leftMoreHighfreq':'r',
               'rightMoreHighfreq':'b',
               'sameRewardHighfreq':'darkgrey'}

soundTriggerChannel = 1


def set_clusters_from_file(animal, session, tetrode):
    '''
    Get an array containing the cluster assignment of each spike detected in the tetrode for that ephys session.
    :param arg1: A string of the name of the ephys session. 
    :param arg2: An int in range(1,9) for tetrode number.
    :return: Array containing the cluster number of each spike.       
    '''
    clustersDir = os.path.join(EPHYS_PATH, animal, session, '_kk')
    if not os.path.exists(clustersDir):
        print 'This session has not been clustered! Please cluster it first.'
        return None
    else:
        clusterFile = os.path.join(clustersDir,'Tetrode%d.clu.1'%tetrode)
        clusters = np.fromfile(clusterFile,dtype='int32',sep=' ')[1:]
        return clusters


def load_n_plot_tuning_raster(ephysSession, behavSession, tetrode, cluster, intensity=50, timeRange = [-0.5,1]):
    '''
    Function to load the ephys, behavior data and plot a tuning raster. 
    :param arg1: A string of the file name of the tuning curve ephys session.
    :param arg2: A string of the file name of the tuning curve behavior session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :param arg5: An int for the intensity in (dB) to plot, default is 50(dB), which is the stimulus intensity used in 2afc task.
    :param arg6: A list of floats for the start and the end of the time period around sound-onset to plot raster.
    '''
    bData = loader.get_session_behavior(behavSession)
    eventData = loader.get_session_events(ephysSession)
    spikeData = loader.get_session_spikes(ephysSession, tetrode, cluster)
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimestamps = spikeData.timestamps

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
    plt.title(plotTitle)
    

def load_n_remove_missing_trials_2afc_behav(behavSession, ephysSession, tetrode, cluster):
    '''
    Loads a 2afc behavior session, compare the number of trials recorded to the corresponding ephys session and removes trials that were not recorded in the ephys session.
    :param arg1: A string of the file name of the 2afc curve behavior session.
    :param arg2: A string of the file name of the 2afc curve ephys session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :return: bData object with missing trials removed in all fields
    '''
    bData = loader.get_session_behavior(behavSession)
    eventData = loader.get_session_events(ephysSession)
    soundOnsetTimeEphys = loader.get_event_onset_times(eventData)
    soundOnsetTimeBehav = bdata['timeTarget']
    
    # Find missing trials
    missingTrials = behavioranalysis.find_missing_trials(soundOnsetTimeEphys,soundOnsetTimeBehav)
    # Remove missing trials
    bData.remove_trials(missingTrials)

    return bData


def get_trials_each_cond_reward_change(behavSession, ephysSession, tetrode, cluster, freqToPlot='low', byBlock=True, colorCondDict):
    '''
    Function to generate selection vector showing which trials to plot for each behavior conditions and the color to use in the plot label.
    :param arg1: A string of the file name of the 2afc curve behavior session.
    :param arg2: A string of the file name of the 2afc curve ephys session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :param arg5: A string indicating which frequency to plot, value of 'low' or 'high', or 'both'.
    :param arg6: Boolean indicating whether to split the plot by behavior blocks. NOTE: should set it to false when plotting all frequencies(freqToPlot='both').
    :param arg7: A dictionary indicating which color label each behavior condition gets in the final plot.
    
    :return: bData object, trialsEachCond, colorsEachCond
    '''
    
    bdata = load_n_remove_missing_trials_2afc_behav(behavSession, ephysSession, tetrode, cluster)

    # -- Select trials to plot from behavior file -- #
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    possibleFreq = np.unique(bdata['targetFrequency'])
    numFreqs = len(possibleFreq)
    
    # -- Select trials to plot based on desired frequencies to plot and whether to plot by block -- #
    ### Recordings during reward change usually have 2 frequencies, low freq means go to left, right freq means go to right ###
    if freqToPlot != 'both':
        if freqToPlot == 'low':
            freq = possibleFreq[0] 
            
        elif freqToPlot == 'high':
            freq = possibleFreq[1]
        
        oneFreq = bdata['targetFrequency'] == freq #vector for selecing trials presenting this frequency
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
            
            if bdata['automationMode'][0]==bdata.labels['automationMode']['same_left_right']:
                if freqToPlot == 'low':
                    colorEachCond = 3*[colorCondDict['sameRewardLowFreq'],colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
                if freqToPlot == 'high':
                    colorEachCond = 3*[colorCondDict['sameRewardHighfreq'],colorCondDict['leftMoreHighfreq'],colorCondDict['rightMoreHighfreq']]
            elif bdata['automationMode'][0]==bdata.labels['automationMode']['same_right_left']:
                if freqToPlot == 'low':
                    colorEachCond = 3*[colorCondDict['sameRewardLowFreq'],colorCondDict['rightMoreLowFreq'],colorCondDict['leftMoreLowFreq']]
                if freqToPlot == 'high':
                    colorEachCond = 3*[colorCondDict['sameRewardHighfreq'],colorCondDict['rightMoreHighfreq'],colorCondDict['leftMoreHighfreq']]
            elif bdata['automationMode'][0]==bdata.labels['automationMode']['left_right_left']:
                if freqToPlot == 'low':
                    colorEachCond = 3*[colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
                if freqToPlot == 'high':
                    colorEachCond = 3*[colorCondDict['leftMoreHighfreq'],colorCondDict['rightMoreHighfreq']]
 
        else:
            currentBlock = bdata['currentBlock']
            blockTypes = [bdata.labels['currentBlock']['same_reward'],bdata.labels['currentBlock']['more_left'],bdata.labels['currentBlock']['more_right']]
            trialsEachType = behavioranalysis.find_trials_each_type(currentBlock,blockTypes)
            oneFreqCorrectBlockSameReward = correctOneFreq&trialsEachType[:,0]
            oneFreqCorrectBlockMoreLeft = correctOneFreq&trialsEachType[:,1]
            oneFreqCorrectBlockMoreRight = correctOneFreq&trialsEachType[:,2]
            trialsEachCond = np.c_[oneFreqCorrectBlockSameReward,oneFreqCorrectBlockMoreLeft,oneFreqCorrectBlockMoreRight]
            if freqToPlot == 'low':
                colorEachCond = [colorCondDict['sameRewardLowFreq'],colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq']]
            elif freqToPlot == 'high':
                colorEachCond = [colorCondDict['sameRewardHighfreq'],colorCondDict['leftMoreHighfreq'],colorCondDict['rightMoreHighfreq']]

    # -- When plotting all 3 frequencies will not be plotting by block, just plot by type of block (low_boundary vs high_boundary) -- #
    elif freqToPlot == 'both':
        assert byBlock == False  #when plotting all frequencies will not be plotting by block
        lowFreq = possibleFreq[0]
        highfreq = possibleFreq[1]
        currentBlock = bdata['currentBlock']
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
        colorEachCond = [colorCondDict['sameRewardLowFreq'],colorCondDict['leftMoreLowFreq'],colorCondDict['rightMoreLowFreq'],colorCondDict['sameRewardHighfreq'],colorCondDict['leftMoreHighfreq'],colorCondDict['rightMoreHighfreq']]
    
    return bdata, trialsEachCond, colorEachCond


def plot_rew_change_per_cell_raster_psth(behavSession, ephysSession, tetrode, cluster, freqToPlot='low', byBlock=False, colorCondDict=colorDictRC, alignment='sound', timeRange=[-0.3,0.4], binWidth=0.010):
    '''
    Function to plot raster and psth for reward_change_freq_dis task. 
    :param arg1: A string of the file name of the 2afc curve behavior session.
    :param arg2: A string of the file name of the 2afc curve ephys session.
    :param arg3: An int in range(1,9) for tetrode number.
    :param arg4: An int in range(1,9) for cluster number.
    :param arg5: A string indicating which frequency to plot, value of 'low' or 'high', or 'both'.
    :param arg6: Boolean indicating whether to split the plot by behavior blocks. NOTE: should set it to false when plotting all frequencies(freqToPlot='both').
    :param arg7: A dictionary indicating which color label each behavior condition gets in the final plot.
    :param arg8: A string indicating the event to align the spike times to, can be 'sound', 'center-out', or 'side-in'.
    
    '''

    bdata, trialsEachCond, colorEachCond = get_trials_each_cond_reward_change(behavSession, ephysSession, tetrode, cluster, freqToPlot=freqToPlot, byBlock=byBlock, colorCondDict=colorCondDict)
    
    eventData = loader.get_session_events(ephysSession)
    spikeData = loader.get_session_spikes(ephysSession, tetrode, cluster)
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimestamps = spikeData.timestamps

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
    
    # -- Plot raster -- #
    plt.subplot2grid((3,1), (0, 0), rowspan=2)
    extraplots.raster_plot(spikeTimesFromEventOnset,indexLimitsEachTrial,timeRange,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,fillWidth=None,labels=None)
    plt.ylabel('Trials')
    plt.xlim(timeRange[0]+0.1,timeRange[-1])
    plt.title('{0}_TT{1}_c{2}_{3}'.format(behavSession,tetrode,cluster,alignment))
   
    # -- Plot PSTH -- #
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset,indexLimitsEachTrial,timeVec)
    smoothWinSize = 3
    plt.subplot2grid((3,1), (2, 0))
    extraplots.plot_psth(spikeCountMat/binWidth,smoothWinSize,timeVec,trialsEachCond=trialsEachCond,colorEachCond=colorEachCond,linestyle=None,linewidth=3,downsamplefactor=1)
    plt.xlabel('Time from {0} onset (s)'.format(alignment))
    plt.ylabel('Firing rate (spk/sec)')
    plt.xlim(timeRange[0]+0.1,timeRange[-1])
