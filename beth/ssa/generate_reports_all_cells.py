'''
Generate a report for each cell, showing white noise (noiseburst) cell response and cell waveform,
noiseburst ISI, tuning curve, oddball & standard paradigm response, PSTH comparing the high(low)
frequency standard to the high(low) frequency oddball, and the oddball waveform. A list of oddball
paradigm parameters is also included.
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

figFormat = 'png'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'reports')

# -- Load the database of cells --
celldb = celldatabase.load_hdf(dbFilename)
number_of_clusters = len(celldb) - 1

# -- Loop through cells and generate reports --
#for indRow,dbRow in celldb.iterrows():
for indRow,dbRow in celldb[260:261].iterrows():
    ax = plt.subplot2grid((3,4), (0,0)) # Subplots
    #plt.suptitle('{}_{}_{:.0f}um_T{}_c{}'.format(dbRow['subject'], dbRow['date'],
            #dbRow['depth'], dbRow['tetrode'], dbRow['cluster']), ha='right') # Report title

    ax0 = plt.subplot2grid((3, 4), (0, 3))
    ax0.axis('off')
    plt.text(0.02, 0.8, '{}_{}_{:.0f}um_T{}_c{}'.format(dbRow['subject'], dbRow['date'],
            dbRow['depth'], dbRow['tetrode'], dbRow['cluster']), fontsize=12)

    '''
    White noise raster plot --------------------------------------------------------
    '''
    oneCell = ephyscore.Cell(dbRow)
    try:
        ephysData, bdata = oneCell.load('noiseburst') # Loads the spikes, events, and behavior
                # data for a single session. Loads the LAST recorded session of the type that
                # was recorded from the cell.
    except ValueError as verror:
        print(verror)
        continue
    # Aligning spikes to an event
    spikeTimes = ephysData['spikeTimes']
    eventOnsetTimes = ephysData['events']['stimOn']
    timeRange = [-0.3, 0.8]  # In seconds
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimes, eventOnsetTimes, timeRange)

    ax1 = plt.subplot2grid((3, 4), (0, 0))
    extraplots.raster_plot(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    plt.xlabel('Time from event onset [s]')
    plt.ylabel('Trials')
    plt.title('Noiseburst')

    '''
    Noiseburst waveform ------------------------------------------------------------
    '''
    ax2 = plt.subplot2grid((3, 4), (1, 0))
    try:
        spikesorting.plot_waveforms(ephysData['samples'])
        ax2.set_title('Noiseburst')
    except ValueError as verror:
        print(verror)
        continue

    '''
    ISI ----------------------------------------------------------------------------
    '''
    ax3 = plt.subplot2grid((3, 4), (2, 0))
    spikesorting.plot_isi_loghist(spikeTimes)

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

        ax4 = plt.subplot2grid((3, 4), (0, 1), rowspan=3)
        extraplots.raster_plot(spikeTimesFromEventOnsetTuning,indexLimitsEachTrialTuning,
                timeRange,trialsEachCondTuning,labels=labelsForYaxis)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Tuning Curve ({} Trials)'.format(numberOfTrialsTuning))
    else:
        ax4 = plt.subplot2grid((3, 4), (0, 1), rowspan=3)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Tuning Curve')

    '''
    Standard raster plot -----------------------------------------------------------
    '''
    if oneCell.get_session_inds('standard') != []:
        try:
            ephysDataStd, bdataStd = oneCell.load('standard')
        except ValueError as verror:
            print(verror)
            continue
        #ephysData, bdata = oneCell.load('standard')
        spikeTimesStd = ephysDataStd['spikeTimes']
        eventOnsetTimesStd = ephysDataStd['events']['stimOn']
        if len(eventOnsetTimesStd)==len(bdataStd['currentFreq'])+1:
            print('Removing last trial from standard ephys data.')
            eventOnsetTimesStd = eventOnsetTimesStd[:-1]
        (spikeTimesFromEventOnsetStd,trialIndexForEachSpikeStd,indexLimitsEachTrialStd) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesStd, eventOnsetTimesStd, timeRange)

        frequenciesEachTrialStd = bdataStd['currentFreq']
        numberOfTrialsStd = len(frequenciesEachTrialStd)
        arrayOfFrequenciesStd = np.unique(bdataStd['currentFreq'])
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesStd]

        trialsEachCondStd = behavioranalysis.find_trials_each_type(frequenciesEachTrialStd,
                arrayOfFrequenciesStd)

        ax5 = plt.subplot2grid((3, 4), (2, 2))
        extraplots.raster_plot(spikeTimesFromEventOnsetStd,indexLimitsEachTrialStd,
                timeRange, trialsEachCondStd, labels=labelsForYaxis)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Standard Sequence ({} Trials)'.format(numberOfTrialsStd))

        '''
        Standard waveform ---------------------------------------------------------------
        '''
        ax7 = plt.subplot2grid((3, 4), (0, 2))
        try:
            spikesorting.plot_waveforms(ephysDataStd['samples'])
            ax7.set_title('Standard')
        except ValueError as verror:
            print(verror)
            continue

    else:
        ax5 = plt.subplot2grid((3, 4), (2, 2))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Standard Sequence')

        ax7 = plt.subplot2grid((3, 4), (0, 2))

    '''
    Oddball --------------------------------------------------------------------
    '''
    if oneCell.get_session_inds('oddball') != []:
        try:
            ephysDataOdd, bdataOdd = oneCell.load('oddball')
        except ValueError as verror:
            print(verror)
            continue

        # Parameters in the title block
        ax0.text(0.02, 0.6, 'Oddball Parameters:', fontsize=12)
        ax0.text(0.02, 0.5, 'Sound Duration: {} s'.format(bdataOdd['stimDuration'][1]))
        ax0.text(0.02, 0.4, 'Sound Intensity: {} dB'.format(bdataOdd['soundIntensity'][1]))
        ax0.text(0.02, 0.3, 'Oddball Probability: {}'.format(bdataOdd['oddballProb'][1]))
        ax0.text(0.02, 0.2, 'Sound Interval: {} +/- {} s'.format(bdataOdd['isiMean'][1],
                bdataOdd['isiHalfRange'][1]))

        '''
        Oddball raster plot ------------------------------------------------------------
        '''
        spikeTimesOdd = ephysDataOdd['spikeTimes']
        eventOnsetTimesOdd = ephysDataOdd['events']['stimOn']
        if len(eventOnsetTimesOdd)==len(bdataOdd['currentFreq'])+1:
            print('Removing last trial from oddball ephys data.')
            eventOnsetTimesOdd = eventOnsetTimesOdd[:-1]
        (spikeTimesFromEventOnsetOdd,trialIndexForEachSpikeOdd,indexLimitsEachTrialOdd) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesOdd, eventOnsetTimesOdd, timeRange)

        frequenciesEachTrialOdd = bdataOdd['currentFreq']
        numberOfTrialsOdd = len(frequenciesEachTrialOdd)
        arrayOfFrequenciesOdd = np.unique(bdataOdd['currentFreq'])
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesOdd]

        trialsEachCondOdd = behavioranalysis.find_trials_each_type(frequenciesEachTrialOdd,
                arrayOfFrequenciesOdd)

        ax6 = plt.subplot2grid((3, 4), (1, 2))
        extraplots.raster_plot(spikeTimesFromEventOnsetOdd,indexLimitsEachTrialOdd,timeRange,
                trialsEachCondOdd, labels=labelsForYaxis)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Oddball Sequence ({} Trials)'.format(numberOfTrialsOdd))
    else:
        ax6 = plt.subplot2grid((3, 4), (1, 2))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Frequency [Hz]')
        plt.title('Oddball Sequence')

    '''
    Plotting the overlapped PSTH ---------------------------------------------------
    '''
    if oneCell.get_session_inds('oddball') != [] and oneCell.get_session_inds('standard') != []:
        # Parameters
        binWidth = 0.010 # seconds
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        smoothWinSizePsth = 5
        lwPsth = 2
        downsampleFactorPsth = 1

        iletLowFreqOddInStdPara = indexLimitsEachTrialStd[:,trialsEachCondStd[:,0]]
        spikeCountMatLowFreqOddInStdPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStd,
                iletLowFreqOddInStdPara,timeVec)

        iletHighFreqStdInStdPara = indexLimitsEachTrialStd[:,trialsEachCondStd[:,1]]
        spikeCountMatHighFreqStdInStdPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStd,
                iletHighFreqStdInStdPara,timeVec)

        iletLowFreqStdInOddPara = indexLimitsEachTrialOdd[:,trialsEachCondOdd[:,0]]
        spikeCountMatLowFreqStdInOddPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,
                iletLowFreqStdInOddPara,timeVec)

        iletHighFreqOddInOddPara = indexLimitsEachTrialOdd[:,trialsEachCondOdd[:,1]]
        spikeCountMatHighFreqOddInOddPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,
                iletHighFreqOddInOddPara,timeVec)

        ax8 = plt.subplot2grid((3, 4), (1, 3))
        extraplots.plot_psth(spikeCountMatHighFreqStdInStdPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatHighFreqOddInOddPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Firing Rate [Hz]')
        plt.title('{} Hz Sound'.format(arrayOfFrequenciesOdd[1]))
        # Legend for PSTH
        oddball_patch = mpatches.Patch(color='b',label='Oddball')
        standard_patch = mpatches.Patch(color='k',label='Standard')
        plt.legend(handles=[oddball_patch, standard_patch])

        ax9 = plt.subplot2grid((3, 4), (2, 3))
        extraplots.plot_psth(spikeCountMatLowFreqStdInOddPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatLowFreqOddInStdPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Firing Rate [Hz]')
        plt.title('{} Hz Sound'.format(arrayOfFrequenciesOdd[0]))
        plt.legend(handles=[oddball_patch, standard_patch])

    elif oneCell.get_session_inds('standard') == [] and oneCell.get_session_inds('oddball') != []:
        binWidth = 0.010
        timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
        smoothWinSizePsth = 2
        lwPsth = 2
        downsampleFactorPsth = 1

        spikeCountMatOdd = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,
                indexLimitsEachTrialOdd,timeVec)

        ax8 = plt.subplot2grid((3, 4), (2, 3))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Firing Rate [Hz]')

        ax9 = plt.subplot2grid((3, 4), (1, 3))
        extraplots.plot_psth(spikeCountMatOdd/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Firing Rate [Hz]')
        plt.title('Oddball Event')
    else:
        ax8 = plt.subplot2grid((3, 4), (2, 3))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Firing Rate [Hz]')

        ax9 = plt.subplot2grid((3, 4), (1, 3))
        plt.xlabel('Time from event onset [s]')
        plt.ylabel('Firing Rate [Hz]')

    '''
    Saving the figure --------------------------------------------------------------
    '''
    figFilename ='{}_{}_{}um_T{}_c{}.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([18,10])

    plt.tight_layout()
    plt.show()
    print('{}/{} - Finished report for {}'.format(indRow, number_of_clusters, figFilename))
