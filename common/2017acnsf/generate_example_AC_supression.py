# Generate data for example of surround suppression in AC
#
# CURRENTLY, IT DEPENDS ON:
# jaratest.nick.database import dataloader_v2 as dataloader
# jaratest.anna import bandwidths_analysis
# jaratest/anna/analysis/band002_celldb.csv
# and of course, the ephys data.

import numpy as np
import pandas as pd
from jaratest.nick.database import dataloader_v2 as dataloader
#from jaratest.anna import bandwidths_analysis
#reload(bandwidths_analysis)
from matplotlib import pyplot as plt
from jaratoolbox import colorpalette as cp
from jaratoolbox import extraplots
#from jaratoolbox import figparams
import matplotlib.gridspec as gridspec
import matplotlib
import string
import pdb
#from jaratest.nick.database import dataplotter
#reload(dataplotter)

SAMPLING_RATE=30000.0
#band002, 2016-08-12, 1380um, T6c4
CELL_NUM = 161

outputFile = './example_AC_supression_c{0}.npz'.format(CELL_NUM)

#db = pd.read_csv('/home/jarauser/src/jaratest/anna/analysis/band002_celldb.csv')
db = pd.read_csv('./band002_celldb.csv')
cell = db.loc[CELL_NUM]
ephysDirs = [word.strip(string.punctuation) for word in cell['ephys'].split()]
behavDirs = [word.strip(string.punctuation) for word in cell['behavior'].split()]
sessType = [word.strip(string.punctuation) for word in cell['sessiontype'].split()]
bandIndex = sessType.index('bandwidth')

def bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial, timeRange = [-0.5, 1.5]):          
    from jaratoolbox import behavioranalysis
    from jaratoolbox import spikesanalysis
    numBands = np.unique(bandEachTrial)
    numAmps = np.unique(ampEachTrial)
            
    firstSortLabels = ['{}'.format(band) for band in numBands]
            
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           ampEachTrial, 
                                                                           numAmps)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange) 

    return spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels

def band_select(spikeTimeStamps, eventOnsetTimes, amplitudes, bandwidths, timeRange, fullRange = [0.0, 2.0]):
    from jaratoolbox import behavioranalysis
    from jaratoolbox import spikesanalysis
    from scipy import stats
    numBands = np.unique(bandwidths)
    numAmps = np.unique(amplitudes)
    spikeArray = np.zeros((len(numBands), len(numAmps)))
    errorArray = np.zeros_like(spikeArray)
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandwidths, 
                                                                   numBands, 
                                                                   amplitudes, 
                                                                   numAmps)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseTimeRange = [timeRange[1]+0.5, fullRange[1]]
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    plt.hold(True)
    for amp in range(len(numAmps)):
        trialsThisAmp = trialsEachCond[:,:,amp]
        for band in range(len(numBands)):
            trialsThisBand = trialsThisAmp[:,band]
            if spikeCountMat.shape[0] != len(trialsThisBand):
                spikeCountMat = spikeCountMat[:-1,:]
                print "FIXME: Using bad hack to make event onset times equal number of trials"
            thisBandCounts = spikeCountMat[trialsThisBand].flatten()
            spikeArray[band, amp] = np.mean(thisBandCounts)
            errorArray[band,amp] = stats.sem(thisBandCounts)
    return spikeArray, errorArray, baselineSpikeRate



loader = dataloader.DataLoader(cell['subject'])

eventData = loader.get_session_events(ephysDirs[bandIndex])
spikeData = loader.get_session_spikes(ephysDirs[bandIndex], int(cell['tetrode']), cluster=int(cell['cluster']))
eventOnsetTimes = loader.get_event_onset_times(eventData)
spikeTimestamps = spikeData.timestamps
bdata = loader.get_session_behavior(behavDirs[bandIndex])
bandEachTrial = bdata['currentBand']
ampEachTrial = bdata['currentAmp']
spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)

spikeArray, errorArray, baseSpikeRate = band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0,1])


np.savez(outputFile, spikeTimesFromEventOnset=spikeTimesFromEventOnset, indexLimitsEachTrial=indexLimitsEachTrial,
         trialsEachCond=trialsEachCond, firstSortLabels=firstSortLabels, bandEachTrial=bandEachTrial,
         spikeArray=spikeArray, errorArray=errorArray, baseSpikeRate=baseSpikeRate)
print 'Saved data to: {0}'.format(outputFile)
