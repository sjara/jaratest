"""
Script to formulate single PSTHs for the classical oddball sequence.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from jaratoolbox import celldatabase
from jaratoolbox import ephyscore
from jaratoolbox import spikesanalysis
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis

dbPath = '/mnt/jarahubdata/reports/2019ssa'
studyName = 'ssa'

figFormat = 'png'
imageFolder = 'images'
outputDir = '/tmp/' #os.path.join(dbPath, imageFolder)

dbFilename = os.path.join(dbPath,'celldb_{}.h5'.format(studyName))
celldb = celldatabase.load_hdf(dbFilename)

# -- PSTH variables --
binWidth = 0.010
timeRange = [-0.1, 0.4]
timeVec = np.arange(timeRange[0],timeRange[-1],binWidth)
smoothWinSizePsth = 5
lwPsth = 2
downsampleFactorPsth = 1
# -- Legend for PSTH --
oddball_patch = mpatches.Patch(color='b', label='Oddball')
standard_patch = mpatches.Patch(color='k', label='Standard')

cellDict = {'subject' : 'chad013',
            'date' : '2019-07-02',
            'depth' : 1300,
            'tetrode' : 8,
            'cluster' : 6}

cellInd, dbRow = celldatabase.find_cell(celldb, **cellDict)
oneCell = ephyscore.Cell(dbRow)

# -- Loading standard sequence data --
ephysDataStd, bdataStd = oneCell.load('standard')
spikeTimesStd = ephysDataStd['spikeTimes']
eventOnsetTimesStd = ephysDataStd['events']['stimOn']
if len(eventOnsetTimesStd)==len(bdataStd['currentFreq'])+1:
    eventOnsetTimesStd = eventOnsetTimesStd[:-1]
(spikeTimesFromEventOnsetStd,trialIndexForEachSpikeStd,indexLimitsEachTrialStd) = spikesanalysis.eventlocked_spiketimes(spikeTimesStd, eventOnsetTimesStd, timeRange)

frequenciesEachTrialStd = bdataStd['currentFreq']
arrayOfFrequenciesStd = np.unique(bdataStd['currentFreq'])
arrayOfFrequenciesStdkHz = arrayOfFrequenciesStd/1000
labelsForYaxisStd = ['%.0f' % f for f in arrayOfFrequenciesStd]
trialsEachCondStd = behavioranalysis.find_trials_each_type(frequenciesEachTrialStd,arrayOfFrequenciesStd)

# -- Loading oddball sequence data --
ephysDataOdd, bdataOdd = oneCell.load('oddball')
spikeTimesOdd = ephysDataOdd['spikeTimes']
eventOnsetTimesOdd = ephysDataOdd['events']['stimOn']
if len(eventOnsetTimesOdd)==len(bdataOdd['currentFreq'])+1:
    eventOnsetTimesOdd = eventOnsetTimesOdd[:-1]
(spikeTimesFromEventOnsetOdd,trialIndexForEachSpikeOdd,indexLimitsEachTrialOdd) = spikesanalysis.eventlocked_spiketimes(spikeTimesOdd, eventOnsetTimesOdd, timeRange)

frequenciesEachTrialOdd = bdataOdd['currentFreq']
arrayOfFrequenciesOdd = np.unique(bdataOdd['currentFreq'])
labelsForYaxisOdd = ['%.0f' % f for f in arrayOfFrequenciesOdd]
trialsEachCondOdd = behavioranalysis.find_trials_each_type(frequenciesEachTrialOdd,arrayOfFrequenciesOdd)

# --  --
LowFreqOddInStdPara = indexLimitsEachTrialStd[:,trialsEachCondStd[:,0]]
spikeCountMatLowFreqOddInStdPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStd,LowFreqOddInStdPara,timeVec)

HighFreqStdInStdPara = indexLimitsEachTrialStd[:,trialsEachCondStd[:,1]]
spikeCountMatHighFreqStdInStdPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetStd,HighFreqStdInStdPara,timeVec)

LowFreqStdInOddPara = indexLimitsEachTrialOdd[:,trialsEachCondOdd[:,0]]
spikeCountMatLowFreqStdInOddPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,LowFreqStdInOddPara,timeVec)

HighFreqOddInOddPara = indexLimitsEachTrialOdd[:,trialsEachCondOdd[:,1]]
spikeCountMatHighFreqOddInOddPara = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnsetOdd,HighFreqOddInOddPara,timeVec)

# -- Plotting the PSTH --
plt.figure(1)
plt.clf()
extraplots.plot_psth(spikeCountMatHighFreqOddInOddPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
        colorEachCond='b',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
extraplots.plot_psth(spikeCountMatHighFreqStdInStdPara/binWidth, smoothWinSizePsth,timeVec,trialsEachCond=[],
        colorEachCond='k',linestyle=None,linewidth=lwPsth,downsamplefactor=downsampleFactorPsth)
plt.xlabel('Time from event onset [s]', fontsize=9)
plt.ylabel('Firing Rate [spikes/s]', fontsize=9)
plt.title('{} kHz Sound'.format(arrayOfFrequenciesStdkHz[1]), fontsize=9)
plt.legend(handles=[oddball_patch, standard_patch], fontsize=7)
# -- Saving the PSTH --
figFilename ='{}_{}_{}um_T{}_c{}_PSTH.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
figFullpath = os.path.join(outputDir,figFilename)
plt.savefig(figFullpath,format=figFormat)

# -- Plotting the oddball raster --
plt.figure(2)
plt.clf()
extraplots.raster_plot(spikeTimesFromEventOnsetOdd,indexLimitsEachTrialOdd,timeRange,trialsEachCondOdd,labels=labelsForYaxisOdd)
plt.xlabel('Time from event onset [s]')
plt.ylabel('Frequency [spikes/s]')
plt.title('Oddball Sequence')
# -- Saving the oddball raster --
figFilename ='{}_{}_{}um_T{}_c{}_raster.{}'.format(dbRow['subject'],dbRow['date'],dbRow['depth'],
            dbRow['tetrode'],dbRow['cluster'],figFormat)
figFullpath = os.path.join(outputDir,figFilename)
plt.savefig(figFullpath,format=figFormat)

plt.show()
