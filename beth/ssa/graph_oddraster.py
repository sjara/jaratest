'''
Oddball raster plot
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

for indRow,dbRow in celldb[266:267].iterrows():
    oneCell = ephyscore.Cell(dbRow)
    timeRange = [-0.1, 0.4]  # In seconds

    ephysDataOdd, bdataOdd = oneCell.load('oddball')
    spikeTimesOdd = ephysDataOdd['spikeTimes']
    eventOnsetTimesOdd = ephysDataOdd['events']['stimOn']
    (spikeTimesFromEventOnsetOdd,trialIndexForEachSpikeOdd,indexLimitsEachTrialOdd) = \
                spikesanalysis.eventlocked_spiketimes(spikeTimesOdd, eventOnsetTimesOdd, timeRange)

    frequenciesEachTrialOdd = bdataOdd['currentFreq']
    numberOfTrialsOdd = len(frequenciesEachTrialOdd)
    arrayOfFrequenciesOdd = np.unique(bdataOdd['currentFreq'])
    arrayOfFrequenciesOddkHz = arrayOfFrequenciesOdd/1000
    labelsForYaxis = ['%.1f' % f for f in arrayOfFrequenciesOddkHz]

    trialsEachCondOdd = behavioranalysis.find_trials_each_type(frequenciesEachTrialOdd,
                arrayOfFrequenciesOdd)

    extraplots.raster_plot(spikeTimesFromEventOnsetOdd,indexLimitsEachTrialOdd,timeRange,
                trialsEachCondOdd, labels=labelsForYaxis)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Time from event onset [s]', fontsize=18)
    plt.ylabel('Frequency [kHz]', fontsize=18)

    '''
    Saving the figure --------------------------------------------------------------
    '''
    figFilename ='{}_{}_{}um_T{}_c{}_oddraster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([6,4])

    plt.tight_layout()
    plt.show()
