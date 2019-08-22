"""
Generate a report for each cell, showing white noise (noiseburst) cell response and cell waveform,
tuning curve, tuning curve ISI, and the ascending & descending paradigm response, including frequency-
sorted rasters, rasters of first(second) oddball and first(second) standard responses, PSTHs comparing
the first & second oddballs to their standards, and the last descending waveform.

N = Noiseburst
T = Tuning curve
A = Ascending
D = Descending
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numpy import array
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

# -- Variables --
timeRange = [-0.1, 0.4]  # In seconds
binWidth = 0.010
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 2
lwPsth = 2
downsampleFactorPsth = 1
# -- Legend for PSTH --
oddball_patch = mpatches.Patch(color='b',label='Oddball')
standard_patch = mpatches.Patch(color='k',label='Standard')

#for indRow,dbRow in celldb.iterrows():
for indRow,dbRow in celldb[500:].iterrows():
    if not 'ascending' in dbRow['sessionType']:
        print('This cell does not contain the threetone sequence.')
        continue

    oneCell = ephyscore.Cell(dbRow)

    plt.clf()
    ax = plt.subplot2grid((4,8), (0,0)) # Subplots


    """
    Parameters
    """
    ax0 = plt.subplot2grid((4,8), (0,0))
    ax0.axis('off')
    plt.text(0.0, 0.5, '{}_{}'.format(dbRow['subject'], dbRow['date']), fontsize=9)
    plt.text(0.0, 0.4, '{:.0f}um_T{}_c{}'.format(dbRow['depth'], dbRow['tetrode'], dbRow['cluster']), fontsize=9)


    """
    Noiseburst
    """
    ephysDataN, bdataN = oneCell.load('noiseburst')
    spikeTimesN = ephysDataN['spikeTimes']
    eventOnsetTimesN = ephysDataN['events']['stimOn']

    (spikeTimesFromEventOnsetN,trialIndexForEachSpikeN,indexLimitsEachTrialN) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimesN, eventOnsetTimesN, timeRange)


    """
    --- Noiseburst raster ---
    """
    ax1 = plt.subplot2grid((4,8), (1,0))
    extraplots.raster_plot(spikeTimesFromEventOnsetN,indexLimitsEachTrialN,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=9)
    plt.ylabel('Trial', fontsize=9)
    plt.title('Noiseburst', fontsize=9)


    """
    --- Noiseburst waveform ---
    """
    ax2 = plt.subplot2grid((4,8), (2,0))
    try:
        spikesorting.plot_waveforms(ephysDataN['samples'])
        ax2.set_title('Cell Waveform From Noiseburst', fontsize=9)
    except ValueError as verror:
        print(verror)
        continue


    """
    Tuning curve
    """
    if oneCell.get_session_inds('tc') != []:
        try:
            ephysDataT, bdataT = oneCell.load('tc')
        except ValueError as verror:
            print(verror)
            continue
        ephysDataT, bdataT = oneCell.load('tc')
        spikeTimesT = ephysDataT['spikeTimes']
        eventOnsetTimesT = ephysDataT['events']['stimOn']

        frequenciesEachTrialT = bdataT['currentFreq']
        arrayOfFrequenciesT = np.unique(bdataT['currentFreq'])
        arrayOfFrequenciesTkHz = arrayOfFrequenciesT/1000
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesTkHz]
        trialsEachCondT = behavioranalysis.find_trials_each_type(frequenciesEachTrialT,arrayOfFrequenciesT)

        (spikeTimesFromEventOnsetT,trialIndexForEachSpikeT,indexLimitsEachTrialT) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesT, eventOnsetTimesT, timeRange)


        """
        --- Frequency-sorted tuning curve ---
        """
        ax4 = plt.subplot2grid((4,8), (0,1), rowspan=3)
        (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetT,indexLimitsEachTrialT,timeRange,
                trialsEachCondT,labels=labelsForYaxis)
        plt.setp(pRaster,ms=1)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Frequency [kHz]', fontsize=9)
        plt.title('Tuning Curve', fontsize=9)


        """
        --- Tuning curve ISI ---
        """
        ax5 = plt.subplot2grid((4,8), (3,1))
        spikesorting.plot_isi_loghist(spikeTimesT)
    else:
        ax4 = plt.subplot2grid((4,8), (0,1), rowspan=3)
        ax5 = plt.subplot2grid((4,8), (3,1))


    """
    Three tone - Ascending
    """
    ax6 = plt.subplot2grid((4,8), (0,2))
    ax6.axis('off')
    plt.text(0.25, 0.5, 'Ascending', fontsize=9)

    if oneCell.get_session_inds('ascending') != []:
        try:
            ephysDataA, bdataA = oneCell.load('ascending')
        except ValueError as verror:
            print(verror)
            continue
        #ephysDataA, bdataA = oneCell.load('ascending')
        spikeTimesA = ephysDataA['spikeTimes']
        eventOnsetTimesA = ephysDataA['events']['stimOn']
        if len(eventOnsetTimesA)==len(bdataA['currentFreq'])+1:
            print('Removing last trial from ascending ephys data.')
            eventOnsetTimesA = eventOnsetTimesA[:-1]
        (spikeTimesFromEventOnsetA,trialIndexForEachSpikeA,indexLimitsEachTrialA) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesA, eventOnsetTimesA, timeRange)

        stimConditionA = bdataA['stimCondition']
        if stimConditionA[-1] == 1:
            print('Removing last trial from ascending behavioral data. Paradigm ended in the \
                    middle of an oddball sequence.')
            stimConditionA = stimConditionA[:-1]

        oddballsA = np.flatnonzero(stimConditionA)

        """
        --- Oddball Trials Raster (first and second) ---
        """
        # -- Will need to change this if we ever change the way tones are presented. --
        firstOddballA = np.array(oddballsA[::2])
        secondOddballA = np.array(oddballsA[1::2])
        thirdOddballA = secondOddballA + 1
        standardForFirstOddballA = firstOddballA - 2
        standardForSecondOddballA = secondOddballA - 4
        standardForThirdOddballA = thirdOddballA - 3

        firstOddballIndexLimitsA = indexLimitsEachTrialA[:,firstOddballA]
        secondOddballIndexLimitsA = indexLimitsEachTrialA[:, secondOddballA]
        thirdOddballIndexLimitsA = indexLimitsEachTrialA[:, thirdOddballA]
        #secondOddballIndexLimitsA = indexLimitsEachTrialA[:,bdataA['currentFreq']==22000]

        ax7 = plt.subplot2grid((4,8), (1,2))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,firstOddballIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Oddball', fontsize=9)

        ax11 = plt.subplot2grid((4,8), (1,3))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,secondOddballIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Oddball', fontsize=9)

        ax15 = plt.subplot2grid((4,8), (1,4))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,thirdOddballIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Third Oddball', fontsize=9)


        """
        --- Standard Trials Raster (first and second) ---
        """
        firstStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForFirstOddballA]
        secondStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForSecondOddballA]
        thirdStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForThirdOddballA]

        ax8 = plt.subplot2grid((4,8), (2,2))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,firstStandardIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Standard', fontsize=9)

        ax12 = plt.subplot2grid((4,8), (2,3))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,secondStandardIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Standard', fontsize=9)

        ax16 = plt.subplot2grid((4,8), (2,4))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,thirdStandardIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Third Standard', fontsize=9)


        """
        --- Frequency-sorted raster ---
        """
        frequenciesEachTrialA = bdataA['currentFreq']
        arrayOfFrequenciesA = np.unique(bdataA['currentFreq'])
        arrayOfFrequenciesAkHz = arrayOfFrequenciesA/1000
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesAkHz]

        trialsEachCondA = behavioranalysis.find_trials_each_type(frequenciesEachTrialA,arrayOfFrequenciesA)

        ax14 = plt.subplot2grid((4,8), (0,3), colspan=2)
        (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetA,indexLimitsEachTrialA,timeRange,
                trialsEachCondA,labels=labelsForYaxis)
        plt.setp(pRaster,ms=1)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Frequency [kHz]', fontsize=9)


        """
        --- PSTH ---
        """
        spikeCountMatFirstOddballA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                firstOddballIndexLimitsA,timeVec)
        spikeCountMatSecondOddballA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                secondOddballIndexLimitsA,timeVec)
        spikeCountMatThirdOddballA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                thirdOddballIndexLimitsA, timeVec)
        spikeCountMatFirstStdA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                firstStandardIndexLimitsA,timeVec)
        spikeCountMatSecondStdA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                secondStandardIndexLimitsA,timeVec)
        spikeCountMatThirdStdA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                thirdStandardIndexLimitsA, timeVec)

        ax9 = plt.subplot2grid((4,8), (3,2))
        extraplots.plot_psth(spikeCountMatFirstOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatFirstStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesAkHz[2]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

        ax13 = plt.subplot2grid((4,8), (3,3))
        extraplots.plot_psth(spikeCountMatSecondOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatSecondStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesAkHz[1]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

        ax17 = plt.subplot2grid((4,8), (3,4))
        extraplots.plot_psth(spikeCountMatThirdOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatThirdStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesAkHz[0]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

    else:
        ax7 = plt.subplot2grid((4,8), (1,2))
        ax11 = plt.subplot2grid((4,8), (1,3))
        ax15 = plt.subplot2grid((4,8), (1,4))
        ax8 = plt.subplot2grid((4,8), (2,2))
        ax12 = plt.subplot2grid((4,8), (2,3))
        ax16 = plt.subplot2grid((4,8), (2,4))
        ax14 = plt.subplot2grid((4,8), (0,3), colspan=2)
        ax9 = plt.subplot2grid((4,8), (3,2))
        ax13 = plt.subplot2grid((4,8), (3,3))
        ax17 = plt.subplot2grid((4,8), (3,4))


    """
    Three tone - Descending
    """
    ax18 = plt.subplot2grid((4,8), (0,5))
    ax18.axis('off')
    plt.text(0.23, 0.5, 'Descending', fontsize=9)

    if oneCell.get_session_inds('descending') != []:
        try:
            ephysDataD, bdataD = oneCell.load('descending')
        except ValueError as verror:
            print(verror)
            continue
        #ephysDataD, bdataD = oneCell.load('descending')
        spikeTimesD = ephysDataD['spikeTimes']
        eventOnsetTimesD = ephysDataD['events']['stimOn']
        if len(eventOnsetTimesD)==len(bdataD['currentFreq'])+1:
            print('Removing last trial from descending ephys data.')
            eventOnsetTimesD = eventOnsetTimesD[:-1]

        (spikeTimesFromEventOnsetD,trialIndexForEachSpikeD,indexLimitsEachTrialD) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesD, eventOnsetTimesD, timeRange)

        stimConditionD = bdataD['stimCondition']
        if stimConditionD[-1] == 1:
            print('Removing last trial from descending behavioral data. Paradigm ended in the \
                    middle of an oddball sequence.')
            stimConditionD = stimConditionD[:-1]

        oddballsD = np.flatnonzero(stimConditionD)

        firstOddballD = np.array(oddballsD[::2])
        secondOddballD = np.array(oddballsD[1::2])
        thirdOddballD = secondOddballD + 1
        firstStandardD = firstOddballD - 2
        secondStandardD = secondOddballD - 4
        thirdStandardD = thirdOddballD - 3


        """
        --- Oddball Trials Raster (first and second) ---
        """
        firstOddballIndexLimitsD = indexLimitsEachTrialD[:,firstOddballD]
        secondOddballIndexLimitsD = indexLimitsEachTrialD[:, secondOddballD]
        thirdOddballIndexLimitsD = indexLimitsEachTrialD[:, thirdOddballD]

        ax19 = plt.subplot2grid((4,8), (1,5))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,firstOddballIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Oddball', fontsize=9)

        ax23 = plt.subplot2grid((4,8), (1,6))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,secondOddballIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Oddball', fontsize=9)

        ax27 = plt.subplot2grid((4,8), (1,7))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,thirdOddballIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Third Oddball', fontsize=9)


        """
        --- Standard Trials Raster (first and second) ---
        """
        firstStandardIndexLimitsD = indexLimitsEachTrialD[:, firstStandardD]
        secondStandardIndexLimitsD = indexLimitsEachTrialD[:, secondStandardD]
        thirdStandardIndexLimitsD = indexLimitsEachTrialD[:, thirdStandardD]

        ax20 = plt.subplot2grid((4,8), (2,5))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,firstStandardIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Standard', fontsize=9)

        ax24 = plt.subplot2grid((4,8), (2,6))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,secondStandardIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Standard', fontsize=9)

        ax28 = plt.subplot2grid((4,8), (2,7))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,thirdStandardIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Third Standard', fontsize=9)


        """
        --- Frequency-sorted raster ---
        """
        frequenciesEachTrialD = bdataD['currentFreq']
        arrayOfFrequenciesD = np.unique(bdataD['currentFreq'])
        arrayOfFrequenciesDkHz = arrayOfFrequenciesD/1000
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesDkHz]

        trialsEachCondD = behavioranalysis.find_trials_each_type(frequenciesEachTrialD,
                arrayOfFrequenciesD)

        ax26 = plt.subplot2grid((4,8), (0,6), colspan=2)
        (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetD,indexLimitsEachTrialD,timeRange,
                trialsEachCondD, labels=labelsForYaxis)
        plt.setp(pRaster,ms=1)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Frequency [kHz]', fontsize=9)


        """
        --- PSTH ---
        """
        spikeCountMatFirstOddballD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                firstOddballIndexLimitsD,timeVec)
        spikeCountMatSecondOddballD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                secondOddballIndexLimitsD,timeVec)
        spikeCountMatThirdOddballD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                thirdOddballIndexLimitsD, timeVec)
        spikeCountMatFirstStdD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                firstStandardIndexLimitsD,timeVec)
        spikeCountMatSecondStdD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                secondStandardIndexLimitsD,timeVec)
        spikeCountMatThirdStdD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                thirdStandardIndexLimitsD, timeVec)

        ax21 = plt.subplot2grid((4,8), (3,5))
        extraplots.plot_psth(spikeCountMatFirstOddballD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatFirstStdD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesDkHz[0]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

        ax25 = plt.subplot2grid((4,8), (3,6))
        extraplots.plot_psth(spikeCountMatSecondOddballD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatSecondStdD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesDkHz[1]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

        ax29 = plt.subplot2grid((4,8), (3,7))
        extraplots.plot_psth(spikeCountMatThirdOddballD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatThirdStdD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesDkHz[2]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)


        """
        --- Last descending waveform ---
        """
        ax3 = plt.subplot2grid((4,8), (3,0))
        try:
            spikesorting.plot_waveforms(ephysDataD['samples'])
            ax3.set_title('Cell Waveform From Last Session', fontsize=9)
        except ValueError as verror:
            print(verror)
            continue

    else:
        ax22 = plt.subplot2grid((4,8), (0,6))
        ax19 = plt.subplot2grid((4,8), (1,5))
        ax23 = plt.subplot2grid((4,8), (1,6))
        ax27 = plt.subplot2grid((4,8), (1,7))
        ax20 = plt.subplot2grid((4,8), (2,5))
        ax24 = plt.subplot2grid((4,8), (2,6))
        ax28 = plt.subplot2grid((4,8), (2,7))
        ax26 = plt.subplot2grid((4,8), (0,6), colspan=2)
        ax21 = plt.subplot2grid((4,8), (3,5))
        ax25 = plt.subplot2grid((4,8), (3,6))
        ax29 = plt.subplot2grid((4,8), (3,7))
        ax3 = plt.subplot2grid((4,8), (3,0))


    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'reports/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([22,12])

    plt.show()

    print('{}/{} - Finished report for {}'.format(indRow, number_of_clusters, figFilename))
