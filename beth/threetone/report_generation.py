"""
Generate a report for each cell, showing ...

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

figFormat = 'png'
outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME,'reports/{}'.format(studyparams.MICE_LIST[0]))

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
# -- chad013 (269:466); chad015(20:428) --
for indRow,dbRow in celldb[428:].iterrows():
    oneCell = ephyscore.Cell(dbRow)

    plt.clf()
    ax = plt.subplot2grid((4,6), (0,0)) # Subplots


    """
    Parameters
    """
    ax0 = plt.subplot2grid((4,6), (0,0))
    ax0.axis('off')
    plt.text(0.0, 0.5, '{}_{}_{:.0f}um_T{}_c{}'.format(dbRow['subject'], dbRow['date'],
            dbRow['depth'], dbRow['tetrode'], dbRow['cluster']), fontsize=9)


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
    ax1 = plt.subplot2grid((4,6), (1,0))
    extraplots.raster_plot(spikeTimesFromEventOnsetN,indexLimitsEachTrialN,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=9)
    plt.ylabel('Trial', fontsize=9)
    plt.title('Noiseburst', fontsize=9)


    """
    --- Noiseburst waveform ---
    """
    ax2 = plt.subplot2grid((4,6), (2,0))
    try:
        spikesorting.plot_waveforms(ephysDataN['samples'])
        ax2.set_title('Cell Waveform From Noiseburst', fontsize=9)
    except ValueError as verror:
        print(verror)
        continue


    """
    Tuning Curve
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
        ax4 = plt.subplot2grid((4,6), (0,1), rowspan=3)
        (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetT,indexLimitsEachTrialT,timeRange,
                trialsEachCondT,labels=labelsForYaxis)
        plt.setp(pRaster,ms=1)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Frequency [kHz]', fontsize=9)
        plt.title('Tuning Curve', fontsize=9)


        """
        --- Tuning Curve ISI ---
        """
        ax5 = plt.subplot2grid((4,6), (3,1))
        spikesorting.plot_isi_loghist(spikeTimesT)
    else:
        ax4 = plt.subplot2grid((4,6), (0,1), rowspan=3)
        ax5 = plt.subplot2grid((4,6), (3,1))


    """
    Three tone - Ascending
    """
    ax20 = plt.subplot2grid((4,6), (0,2))
    ax20.axis('off')
    plt.text(0.35, 0.5, 'Ascending', fontsize=9)

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

        oddballsA = np.flatnonzero(bdataA['stimCondition'])


        """
        --- Oddball Trials Raster (first and second) ---
        """
        # -- Will need to change this if we ever change the way tones are presented. --
        firstOddballA = np.array(oddballsA[::2])
        secondOddballA = np.array(oddballsA[1::2])
        standardForFirstOddballA = firstOddballA - 2
        standardForSecondOddballA = secondOddballA - 4

        firstOddballIndexLimitsA = indexLimitsEachTrialA[:,firstOddballA]
        secondOddballIndexLimitsA = indexLimitsEachTrialA[:, secondOddballA]
        #secondOddballIndexLimitsA = indexLimitsEachTrialA[:,bdataA['currentFreq']==22000]

        ax7 = plt.subplot2grid((4,6), (1,2))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,firstOddballIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Oddball', fontsize=9)

        ax10 = plt.subplot2grid((4,6), (1,3))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,secondOddballIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Oddball', fontsize=9)


        """
        --- Standard Trials Raster (first and second) ---
        """
        firstStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForFirstOddballA]
        secondStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForSecondOddballA]

        ax8 = plt.subplot2grid((4,6), (2,2))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,firstStandardIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Standard', fontsize=9)

        ax11 = plt.subplot2grid((4,6), (2,3))
        extraplots.raster_plot(spikeTimesFromEventOnsetA,secondStandardIndexLimitsA,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Standard', fontsize=9)


        """
        --- Frequency-sorted raster ---
        """
        frequenciesEachTrialA = bdataA['currentFreq']
        arrayOfFrequenciesA = np.unique(bdataA['currentFreq'])
        arrayOfFrequenciesAkHz = arrayOfFrequenciesA/1000
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesAkHz]

        trialsEachCondA = behavioranalysis.find_trials_each_type(frequenciesEachTrialA,arrayOfFrequenciesA)

        ax6 = plt.subplot2grid((4,6), (0,3))
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
        spikeCountMatFirstStdA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                firstStandardIndexLimitsA,timeVec)
        spikeCountMatSecondStdA = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetA,
                secondStandardIndexLimitsA,timeVec)

        ax9 = plt.subplot2grid((4,6), (3,2))
        extraplots.plot_psth(spikeCountMatFirstOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatFirstStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesAkHz[2]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

        ax12 = plt.subplot2grid((4,6), (3,3))
        extraplots.plot_psth(spikeCountMatSecondOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatSecondStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesAkHz[1]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)
    else:
        ax7 = plt.subplot2grid((4,6), (1,2))
        ax10 = plt.subplot2grid((4,6), (1,3))
        ax8 = plt.subplot2grid((4,6), (2,2))
        ax11 = plt.subplot2grid((4,6), (2,3))
        ax6 = plt.subplot2grid((4,6), (0,3))
        ax9 = plt.subplot2grid((4,6), (3,2))
        ax12 = plt.subplot2grid((4,6), (3,3))


    """
    Three tone - Descending
    """
    ax21 = plt.subplot2grid((4,6), (0,4))
    ax21.axis('off')
    plt.text(0.33, 0.5, 'Descending', fontsize=9)

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

        oddballsD = np.flatnonzero(bdataD['stimCondition'])

        firstOddballD = np.array(oddballsD[::2])
        secondOddballD = np.array(oddballsD[1::2])
        firstStandardD = firstOddballD - 2
        secondStandardD = secondOddballD - 4


        """
        --- Oddball Trials Raster (first and second) ---
        """
        firstOddballIndexLimitsD = indexLimitsEachTrialD[:,firstOddballD]
        secondOddballIndexLimitsD = indexLimitsEachTrialD[:, secondOddballD]

        ax14 = plt.subplot2grid((4,6), (1,4))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,firstOddballIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Oddball', fontsize=9)

        ax17 = plt.subplot2grid((4,6), (1,5))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,secondOddballIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Oddball', fontsize=9)


        """
        --- Standard Trials Raster (first and second) ---
        """
        firstStandardIndexLimitsD = indexLimitsEachTrialD[:, firstStandardD]
        secondStandardIndexLimitsD = indexLimitsEachTrialD[:, secondStandardD]

        ax15 = plt.subplot2grid((4,6), (2,4))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,firstStandardIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('First Standard', fontsize=9)

        ax18 = plt.subplot2grid((4,6), (2,5))
        extraplots.raster_plot(spikeTimesFromEventOnsetD,secondStandardIndexLimitsD,timeRange)
        plt.xlabel('Time From Event Onset [s]', fontsize=9)
        plt.ylabel('Trial', fontsize=9)
        plt.title('Second Standard', fontsize=9)


        """
        --- Frequency-sorted raster ---
        """
        frequenciesEachTrialD = bdataD['currentFreq']
        arrayOfFrequenciesD = np.unique(bdataD['currentFreq'])
        arrayOfFrequenciesDkHz = arrayOfFrequenciesD/1000
        labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesDkHz]

        trialsEachCondD = behavioranalysis.find_trials_each_type(frequenciesEachTrialD,
                arrayOfFrequenciesD)

        ax13 = plt.subplot2grid((4,6), (0,5))
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
        spikeCountMatFirstStdD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                firstStandardIndexLimitsD,timeVec)
        spikeCountMatSecondStdD = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetD,
                secondStandardIndexLimitsD,timeVec)

        ax16 = plt.subplot2grid((4,6), (3,4))
        extraplots.plot_psth(spikeCountMatFirstOddballD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatFirstStdD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesDkHz[0]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)

        ax19 = plt.subplot2grid((4,6), (3,5))
        extraplots.plot_psth(spikeCountMatSecondOddballD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        extraplots.plot_psth(spikeCountMatSecondStdD/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
        plt.xlabel('Time from event onset [s]', fontsize=9)
        plt.ylabel('Firing Rate [Hz]', fontsize=9)
        plt.title('{} kHz Sound'.format(arrayOfFrequenciesDkHz[1]), fontsize=9)
        plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)


        """
        --- Last descending waveform ---
        """
        ax3 = plt.subplot2grid((4,6), (3,0))
        try:
            spikesorting.plot_waveforms(ephysDataD['samples'])
            ax3.set_title('Cell Waveform From Last Session', fontsize=9)
        except ValueError as verror:
            print(verror)
            continue

    else:
        ax14 = plt.subplot2grid((4,6), (1,4))
        ax17 = plt.subplot2grid((4,6), (1,5))
        ax15 = plt.subplot2grid((4,6), (2,4))
        ax18 = plt.subplot2grid((4,6), (2,5))
        ax13 = plt.subplot2grid((4,6), (0,5))
        ax16 = plt.subplot2grid((4,6), (3,4))
        ax19 = plt.subplot2grid((4,6), (3,5))


    """
    Saving the figure --------------------------------------------------------------
    """
    figFilename ='{}_{}_{}um_T{}_c{}.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([18,10])

    plt.tight_layout()
    plt.show()

    print('{}/{} - Finished report for {}'.format(indRow, number_of_clusters, figFilename))
