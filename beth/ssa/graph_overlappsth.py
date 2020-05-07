'''
Plotting the overlapped PSTHs
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

    '''
    Standard
    '''
    ephysDataStd, bdataStd = oneCell.load('standard')
    spikeTimesStd = ephysDataStd['spikeTimes']
    eventOnsetTimesStd = ephysDataStd['events']['stimOn']
    if len(eventOnsetTimesStd)==len(bdataStd['currentFreq'])+1:
        eventOnsetTimesStd = eventOnsetTimesStd[:-1]
    (spikeTimesFromEventOnsetStd,trialIndexForEachSpikeStd,indexLimitsEachTrialStd) = spikesanalysis.eventlocked_spiketimes(spikeTimesStd, eventOnsetTimesStd, timeRange)

    frequenciesEachTrialStd = bdataStd['currentFreq']
    numberOfTrialsStd = len(frequenciesEachTrialStd)
    arrayOfFrequenciesStd = np.unique(bdataStd['currentFreq'])
    labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesStd]
    trialsEachCondStd = behavioranalysis.find_trials_each_type(frequenciesEachTrialStd,arrayOfFrequenciesStd)

    '''
    ODDBALL
    '''
    ephysDataOdd, bdataOdd = oneCell.load('oddball')
    spikeTimesOdd = ephysDataOdd['spikeTimes']
    eventOnsetTimesOdd = ephysDataOdd['events']['stimOn']
    if len(eventOnsetTimesOdd)==len(bdataOdd['currentFreq'])+1:
        eventOnsetTimesOdd = eventOnsetTimesOdd[:-1]
    (spikeTimesFromEventOnsetOdd,trialIndexForEachSpikeOdd,indexLimitsEachTrialOdd) = spikesanalysis.eventlocked_spiketimes(spikeTimesOdd, eventOnsetTimesOdd, timeRange)

    frequenciesEachTrialOdd = bdataOdd['currentFreq']
    numberOfTrialsOdd = len(frequenciesEachTrialOdd)
    arrayOfFrequenciesOdd = np.unique(bdataOdd['currentFreq'])
    labelsForYaxis = ['%.0f' % f for f in arrayOfFrequenciesOdd]

    trialsEachCondOdd = behavioranalysis.find_trials_each_type(frequenciesEachTrialOdd,arrayOfFrequenciesOdd)

    '''
    PSTH
    '''
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

    plt.figure()
    extraplots.plot_psth(spikeCountMatHighFreqStdInStdPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='c',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatHighFreqOddInOddPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatLowFreqStdInOddPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='g',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    extraplots.plot_psth(spikeCountMatLowFreqOddInStdPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
                colorEachCond='r',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
    plt.xlabel('Time from event onset [s]')
    plt.ylabel('Firing Rate [Hz]')
    # Legend for PSTH
    #highStd = mpatches.Patch(color='c',label='26.8 kHz (Std)')
    #highOdd = mpatches.Patch(color='b',label='26.8 kHz (Odd)')
    #lowStd = mpatches.Patch(color='g',label='2.9 kHz (Std)')
    #lowOdd = mpatches.Patch(color='lime',label='2.9 kHz (Odd)')

    #plt.legend(handles=[highStd, highOdd, lowStd, lowOdd])

    '''
    Saving the figure --------------------------------------------------------------
    '''
    figFilename ='{}_{}_{}um_T{}_c{}_psth.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
    figFullpath = os.path.join(outputDir,figFilename)
    plt.savefig(figFullpath,format=figFormat)
    plt.gcf().set_size_inches([6,4])

    plt.tight_layout()
    plt.show()
