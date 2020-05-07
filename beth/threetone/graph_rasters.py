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

for indRow,dbRow in celldb[97:98].iterrows():
    oneCell = ephyscore.Cell(dbRow)

    ephysDataA, bdataA = oneCell.load('ascending')
    spikeTimesA = ephysDataA['spikeTimes']
    eventOnsetTimesA = ephysDataA['events']['stimOn']
    if len(eventOnsetTimesA)==len(bdataA['currentFreq'])+1:
        eventOnsetTimesA = eventOnsetTimesA[:-1]
    (spikeTimesFromEventOnsetA,trialIndexForEachSpikeA,indexLimitsEachTrialA) = \
            spikesanalysis.eventlocked_spiketimes(spikeTimesA, eventOnsetTimesA, timeRange)

    stimConditionA = bdataA['stimCondition']
    if stimConditionA[-1] == 1:
        stimConditionA = stimConditionA[:-1]

    oddballsA = np.flatnonzero(stimConditionA)

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

    plt.figure()
    extraplots.raster_plot(spikeTimesFromEventOnsetA,firstOddballIndexLimitsA,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=14)
    plt.ylabel('Trial', fontsize=14)
    plt.title('First Oddball', fontsize=14)
    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_firoddraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([3,2])


    plt.figure()
    extraplots.raster_plot(spikeTimesFromEventOnsetA,secondOddballIndexLimitsA,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=14)
    plt.ylabel('Trial', fontsize=14)
    plt.title('Second Oddball', fontsize=14)
    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_secoddraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([3,2])


    """
    --- Standard Trials Raster (first and second) ---
    """
    firstStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForFirstOddballA]
    secondStandardIndexLimitsA = indexLimitsEachTrialA[:, standardForSecondOddballA]


    plt.figure()
    extraplots.raster_plot(spikeTimesFromEventOnsetA,firstStandardIndexLimitsA,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=14)
    plt.ylabel('Trial', fontsize=14)
    plt.title('First Standard', fontsize=14)
    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_firstdraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([3,2])


    plt.figure()
    extraplots.raster_plot(spikeTimesFromEventOnsetA,secondStandardIndexLimitsA,timeRange)
    plt.xlabel('Time From Event Onset [s]', fontsize=14)
    plt.ylabel('Trial', fontsize=14)
    plt.title('Second Standard', fontsize=14)
    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_secstdraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([3,2])

    plt.show()
