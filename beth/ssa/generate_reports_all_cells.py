'''
Generate a report for each cell, showing...
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from jaratoolbox import settings
from jaratoolbox import celldatabase
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import ephyscore
from jaratoolbox import spikesorting
import studyparams

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyparams.STUDY_NAME))

# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)
number_of_clusters = len(celldb) - 1

# -- Loop through cells and generate reports --
#for indRow,dbRow in celldb.iterrows():
for indRow,dbRow in celldb[:50].iterrows():
    ax = plt.subplot2grid((3,3), (0,0))
    plt.suptitle('{}_{}_{}um_T{}_c{}'.format(dbRow['subject'], dbRow['date'],
            dbRow['depth'], dbRow['tetrode'], dbRow['cluster']))

    '''
    White noise raster plot --------------------------------------------------------
    '''
    oneCell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = oneCell.load('noiseburst')
    except ValueError as verror:
        print(verror)
        continue
    # Aligning spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3, 0.8]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    ax1 = plt.subplot2grid((3, 3), (0, 0))
    extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    plt.xlabel('Time from event onset [s]')
    plt.ylabel('Trials')
    plt.title('Noiseburst')

    '''
    Frequency tuning raster plot ---------------------------------------------------
    '''
    if oneCell.get_session_inds('tc') != []:
        ephysDataTuning, bdataTuning = oneCell.load('tc')
        spikeTimes = ephysDataTuning['spikeTimes']
        eventOnsetTimes = ephysDataTuning['events']['stimOn']
        (spikeTimesFromEventOnsetTuning,trialIndexForEachSpikeTuning,indexLimitsEachTrialTuning) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        frequenciesEachTrialTuning = bdataTuning['currentFreq']
        numberOfTrialsTuning = len(frequenciesEachTrialTuning)
        arrayOfFrequenciesTuning = np.unique(bdataTuning['currentFreq'])
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesTuning] # Generating a label of the
                # behavior data for the y-axis

        trialsEachCondTuning = behavioranalysis.find_trials_each_type(frequenciesEachTrialTuning,
                arrayOfFrequenciesTuning)

        ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2)
        extraplots.raster_plot(spikeTimesFromEventOnsetTuning,indexLimitsEachTrialTuning,
                timeRange,trialsEachCondTuning,labels=labelsForYaxis)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Tuning Curve (# of Trials = {})'.format(numberOfTrialsTuning))
    else:
        ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Tuning Curve (# of Trials = {})'.format(numberOfTrialsTuning))

    '''
    Standard raster plot -----------------------------------------------------------
    '''
    if oneCell.get_session_inds('standard') != []:
        try:
            ephysData, bdata = oneCell.load('standard')
        except ValueError as verror:
            print(verror)
            continue
        #ephysData, bdata = oneCell.load('standard')
        spikeTimes = ephysData['spikeTimes']
        eventOnsetTimes = ephysData['events']['stimOn']
        if len(eventOnsetTimes)==len(bdata['currentFreq'])+1:
            print('Removing last trial from standard ephys data.')
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnsetStandard,trialIndexForEachSpikeStandard,indexLimitsEachTrialStandard) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        frequenciesEachTrialStandard = bdata['currentFreq']
        numberOfTrialsStandard = len(frequenciesEachTrialStandard)
        arrayOfFrequenciesStandard = np.unique(bdata['currentFreq'])
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesStandard]

        trialsEachCondStandard = \
                behavioranalysis.find_trials_each_type(frequenciesEachTrialStandard,arrayOfFrequenciesStandard)

        ax3 = plt.subplot2grid((3, 3), (1, 1))
        extraplots.raster_plot(spikeTimesFromEventOnsetStandard,indexLimitsEachTrialStandard,
                timeRange, trialsEachCondStandard, labels=labelsForYaxis)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Standard Sequence (# of Trials = {})'.format(numberOfTrialsStandard))
    else:
        ax3 = plt.subplot2grid((3, 3), (1, 1))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Standard Sequence (# of Trials = {})'.format(numberOfTrialsStandard))

    '''
    Oddball raster plot ------------------------------------------------------------
    '''
    if oneCell.get_session_inds('oddball') != []:
        try:
            ephysDataOddball, bdataOddball = oneCell.load('oddball')
        except ValueError as verror:
            print(verror)
            continue
        #ephysDataOddball, bdataOddball = oneCell.load('oddball')
        spikeTimes = ephysDataOddball['spikeTimes']
        eventOnsetTimes = ephysDataOddball['events']['stimOn']
        if len(eventOnsetTimes)==len(bdataOddball['currentFreq'])+1:
            print('Removing last trial from oddball ephys data.')
            eventOnsetTimes = eventOnsetTimes[:-1]
        (spikeTimesFromEventOnsetOddball,trialIndexForEachSpikeOddball,indexLimitsEachTrialOddball) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

        frequenciesEachTrialOddball = bdataOddball['currentFreq']
        numberOfTrialsOddball = len(frequenciesEachTrialOddball)
        arrayOfFrequenciesOddball = np.unique(bdataOddball['currentFreq'])
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesOddball]

        trialsEachCondOddball = behavioranalysis.find_trials_each_type(frequenciesEachTrialOddball,
                arrayOfFrequenciesOddball)

        ax4 = plt.subplot2grid((3, 3), (2, 1))
        extraplots.raster_plot(spikeTimesFromEventOnsetOddball,indexLimitsEachTrialOddball,timeRange,
                trialsEachCondOddball, labels=labelsForYaxis)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Oddball Sequence (# of Trials = {})'.format(numberOfTrialsOddball))
    else:
        ax4 = plt.subplot2grid((3, 3), (2, 1))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Oddball Sequence (# of Trials = {})'.format(numberOfTrialsOddball))

    '''
    Waveform plot ------------------------------------------------------------------
    '''
    ax5 = plt.subplot2grid((3, 3), (0, 2))
    spikesorting.plot_waveforms(ephysDataOddball['samples'])

    '''
    Plotting the overlapped PSTH ---------------------------------------------------
    '''
    # Parameters
    binWidth = 0.010
    timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
    smoothWinSizePsth = 5
    lwPsth = 2
    downsampleFactorPsth = 1

    # For standard sequence
    iletLowFreqStandard = indexLimitsEachTrialStandard[:,trialsEachCondStandard[:,0]]
    spikeCountMatLowStandard = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStandard,
            iletLowFreqStandard,timeVec)

    iletHighFreqStandard = indexLimitsEachTrialStandard[:,trialsEachCondStandard[:,1]]
    spikeCountMatHighStandard = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStandard,
            iletHighFreqStandard,timeVec)

    # For oddball sequence
    iletLowFreqOddball = indexLimitsEachTrialOddball[:,trialsEachCondOddball[:,0]]
    spikeCountMatLowOddball = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOddball,
            iletLowFreqOddball,timeVec)

    iletHighFreqOddball = indexLimitsEachTrialOddball[:,trialsEachCondOddball[:,1]]
    spikeCountMatHighOddball = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOddball,
            iletHighFreqOddball,timeVec)

    ax6 = plt.subplot2grid((3, 3), (1, 2))
    extraplots.plot_psth(spikeCountMatLowOddball/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
            colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatLowStandard/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
            colorEachCond='c',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time from event onset [s]')
    plt.ylabel('Number of spikes')
    plt.title('Low Frequency Event')

    # Legend for PSTH
    oddball_patch = mpatches.Patch(color='b',label='Oddball')
    standard_patch = mpatches.Patch(color='c',label='Standard')
    plt.legend(handles=[oddball_patch, standard_patch])

    ax7 = plt.subplot2grid((3, 3), (2, 2))
    extraplots.plot_psth(spikeCountMatHighOddball/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
            colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatHighStandard/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
            colorEachCond='c',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time from event onset [s]')
    plt.ylabel('Number of spikes')
    plt.title('High Frequency Event')
    plt.legend(handles=[oddball_patch, standard_patch])

    '''
    Saving the figure --------------------------------------------------------------
    '''
    figFormat = 'png'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'reports')
    figFilename ='{}_{}_{}um_T{}_c{}.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([9,5])

    plt.tight_layout()
    plt.show()

    print('{}/{} - Finished report for {}'.format(indRow, number_of_clusters, figFilename))
