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

    '''
    ASCENDING
    '''

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
    trialsEachCondA = behavioranalysis.find_trials_each_type(frequenciesEachTrialA,arrayOfFrequenciesA)

    plt.figure()
    (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetA,indexLimitsEachTrialA,timeRange,
            trialsEachCondA,labels=labelsForYaxis)
    plt.setp(pRaster,ms=1.2)
    plt.xlabel('Time From Event Onset [s]', fontsize=14)
    plt.ylabel('Frequency [kHz]', fontsize=14)
    plt.title('Ascending')
    
    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_ascraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([8,4])

    '''
    DESCENDING
    '''

    ephysDataD, bdataD = oneCell.load('descending')
    spikeTimesD = ephysDataD['spikeTimes']
    eventOnsetTimesD = ephysDataD['events']['stimOn']
    if len(eventOnsetTimesD)==len(bdataD['currentFreq'])+1:
        eventOnsetTimesD = eventOnsetTimesD[:-1]
    (spikeTimesFromEventOnsetD,trialIndexForEachSpikeD,indexLimitsEachTrialD) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesD, eventOnsetTimesD, timeRange)

    frequenciesEachTrialD = bdataD['currentFreq']
    arrayOfFrequenciesD = np.unique(bdataD['currentFreq'])
    arrayOfFrequenciesDkHz = arrayOfFrequenciesD/1000
    labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesDkHz]
    trialsEachCondD = behavioranalysis.find_trials_each_type(frequenciesEachTrialD,
                arrayOfFrequenciesD)

    plt.figure()
    (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetD,indexLimitsEachTrialD,timeRange,
                trialsEachCondD, labels=labelsForYaxis)
    plt.setp(pRaster,ms=1.2)
    plt.xlabel('Time From Event Onset [s]', fontsize=14)
    plt.ylabel('Frequency [kHz]', fontsize=14)
    plt.title('Descending')

    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_desraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([8,4])
    plt.show()
