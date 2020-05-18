"""
--- Frequency-sorted tuning curve ---
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

    ephysDataT, bdataT = oneCell.load('tc')
    ephysDataT, bdataT = oneCell.load('tc')
    spikeTimesT = ephysDataT['spikeTimes']
    eventOnsetTimesT = ephysDataT['events']['stimOn']

    frequenciesEachTrialT = bdataT['currentFreq']
    arrayOfFrequenciesT = np.unique(bdataT['currentFreq'])
    arrayOfFrequenciesTkHz = arrayOfFrequenciesT/1000
    labelsForYaxis = ['%.1f' % f for f in arrayOfFrequenciesTkHz]
    trialsEachCondT = behavioranalysis.find_trials_each_type(frequenciesEachTrialT,arrayOfFrequenciesT)

    (spikeTimesFromEventOnsetT,trialIndexForEachSpikeT,indexLimitsEachTrialT) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesT, eventOnsetTimesT, timeRange)

    (pRaster,hcond,zline) = extraplots.raster_plot(spikeTimesFromEventOnsetT,indexLimitsEachTrialT,timeRange,
                trialsEachCondT,labels=labelsForYaxis)
    #plt.setp(pRaster,ms=1)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Time from event onset [s]', fontsize=18)
    plt.ylabel('Frequency [kHz]', fontsize=18)

    """
    Saving the figure --------------------------------------------------------------
    """
    figFormat = 'png'
    figFilename ='{}_{}_{}um_T{}_c{}_tuning.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    reportFolder = 'reports'
    outputDir = os.path.join(settings.FIGURES_DATA_PATH, studyparams.STUDY_NAME, reportFolder + '/{}'.format(dbRow['subject']))
    figFullpath = os.path.join(outputDir,figFilename)
    plt.tight_layout()
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([7,14])

    plt.show()
