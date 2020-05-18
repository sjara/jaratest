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

reload(studyparams)

dbPath = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME)
dbFilename = os.path.join(dbPath,'celldb_{}_{}.h5'.format(studyparams.STUDY_NAME, studyparams.MICE_LIST))

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

for indRow,dbRow in celldb[97:98].iterrows():
    oneCell = ephyscore.Cell(dbRow)
    ephysDataA, bdataA = oneCell.load('ascending')

    spikeTimesA = ephysDataA['spikeTimes']
    eventOnsetTimesA = ephysDataA['events']['stimOn']
    if len(eventOnsetTimesA)==len(bdataA['currentFreq'])+1:
        eventOnsetTimesA = eventOnsetTimesA[:-1]
    (spikeTimesFromEventOnsetA,trialIndexForEachSpikeA,indexLimitsEachTrialA) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesA, eventOnsetTimesA, timeRange)

    frequenciesEachTrialA = bdataA['currentFreq']
    arrayOfFrequenciesA = np.unique(bdataA['currentFreq'])
    arrayOfFrequenciesAkHz = arrayOfFrequenciesA/1000
    labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesAkHz]
    stimConditionA = bdataA['stimCondition']
    if stimConditionA[-1] == 1:
        stimConditionA = stimConditionA[:-1]

    oddballsA = np.flatnonzero(stimConditionA)

    firstOddballA = np.array(oddballsA[::2])
    secondOddballA = np.array(oddballsA[1::2])
    standardForFirstOddballA = firstOddballA - 2
    standardForSecondOddballA = secondOddballA - 4

    firstOddballIndexLimitsA = indexLimitsEachTrialA[:,firstOddballA]
    secondOddballIndexLimitsA = indexLimitsEachTrialA[:, secondOddballA]

    firstStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForFirstOddballA]
    secondStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForSecondOddballA]

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

    plt.figure()
    extraplots.plot_psth(spikeCountMatFirstOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
              colorEachCond=[(0.13,0.86,0.27)],linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatFirstStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
              colorEachCond=[(0.13,0.86,0.27)],linestyle=['dotted'],linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Time from event onset [s]', fontsize=18)
    plt.ylabel('Firing Rate [Hz]', fontsize=18)
    plt.legend(['High Freq Odd', 'High Freq Std'])
    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_firpsth.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([6,5])



    plt.figure()
    extraplots.plot_psth(spikeCountMatSecondOddballA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
              colorEachCond=[(1.00,0.49,0.11)],linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatSecondStdA/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
              colorEachCond=[(1.00,0.49,0.11)],linestyle=['dotted'],linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Time from event onset [s]', fontsize=18)
    plt.ylabel('Firing Rate [Hz]', fontsize=18)
    plt.legend(['Mid Freq Odd', 'Mid Freq Std'])

    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_secpsth.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([6,5])
    plt.show()
