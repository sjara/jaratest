'''
This file will contain an example showing how to use EphysExperiment to process data during an experiment
'''

import ephys_experiment_v3 as ee3
reload(ee3)

ex0624 = ee3.EphysExperiment('pinp003', '2015-06-24', experimenter = 'nick')

#ex0624.plot_array_raster('15-27-37', replace = 0, ms = 1, timeRange = [-0.5, 1.5])
#ex0624.plot_session_tc_heatmap('15-31-48', 6, 'a')


#ex0624.plot_sorted_tuning_raster('15-31-48', 6, 'a', ms=4)

import numpy as np
from jaratoolbox import extraplots
from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
import matplotlib
import matplotlib.pyplot as plt

bdata = ex0624.get_session_behav_data('15-31-48','a')
freqEachTrial = bdata['currentFreq']
intensityEachTrial = bdata['currentIntensity']
possibleFreq = np.unique(freqEachTrial)
possibleIntensity = np.unique(intensityEachTrial)
trialsEachCond = behavioranalysis.find_trials_each_combination(intensityEachTrial, possibleIntensity, freqEachTrial, possibleFreq)
trialsEachCondFreq = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)
trialsEachCondInt = behavioranalysis.find_trials_each_type(intensityEachTrial, possibleIntensity)

spikeData = ex0624.get_session_spike_data_one_tetrode('15-31-48', 6)
eventData = ex0624.get_session_event_data('15-31-48')
eventOnsetTimes = ex0624.get_event_onset_times(eventData)

eventOnsetTimes = eventOnsetTimes[:-1] #FIXME: WHY IS THIS NECESSARY????!!

spikeTimestamps=spikeData.timestamps


timeRange = [0, 0.1]

spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                                                                                                eventOnsetTimes,
                                                                                                                timeRange)


def avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCond):

    numSpikesInTimeRangeEachTrial = np.squeeze(np.diff(indexLimitsEachTrial, axis=0))
    conditionMatShape = np.shape(trialsEachCond)
    numRepeats = np.product(conditionMatShape[1:])
    nSpikesMat = np.reshape(numSpikesInTimeRangeEachTrial.repeat(numRepeats), conditionMatShape)
    spikesFilteredByTrialType = nSpikesMat*trialsEachCond
    avgSpikesArray = np.sum(spikesFilteredByTrialType, 0)/np.sum(trialsEachCond, 0).astype('float')
    return avgSpikesArray

def avg_spikes_in_event_locked_timerange_each_cond(spikeTimestamps, trialsEachCond, timeRange):
    spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                                                                                                    eventOnsetTimes,
                                                                                                                    timeRange)
    spikeArray = avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCond)

    return spikeArray

def plot_array_as_heatmap(heatmapArray, xlabels=None, ylabels=None, flipy=True, flipylabels=True, cmap='Blues'):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Intensity (dB SPL)')
    ax.set_xlabel('Frequency (kHz)') #FIXME: This should be outside this function and does not appear to work anyway

    if flipy:
        heatmapArray = np.flipud(heatmapArray)

    cax = ax.imshow(heatmapArray, interpolation='none', aspect='auto', cmap=cmap)
    vmin, vmax = cax.get_clim()
    cbar=plt.colorbar(cax, format = '%.1f')

    if xlabels is not None:
        ax.set_xticks(range(len(xlabels)))
        xticks = ["%.1f" % freq for freq in xlabels/1000.0] #FIXME: This should be outside this function
        ax.set_xticklabels(xticks, rotation = 'vertical')

    ax.set_yticks(range(np.shape(heatmapArray)[0]))


    if ylabels is not None:
        if flipylabels:
            ax.set_yticklabels(ylabels[::-1])
        else:
            ax.set_yticklabels(ylabels)
            
    plt.show()


spikesFI = avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCond)
spikesF = avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCondFreq)
spikesI = avg_locked_spikes_per_condition(indexLimitsEachTrial, trialsEachCondInt)

'''
TODO

DONE Add tetrode labels to the array raster plot
DONE also space in xlabel between time and seconds
DONE sharex between the tetrodes

### Could be solved by using the new code for generating TC heatmap arrays, 
although there would be some additional work needed on the plotting code ###

Pass spikes already aligned to the tc heatmap code, 
using the code to find trials each condition

add parameter for the timerange for the tc heatmap, 
which must also update the labels. 

labels for frequency and intensity, including units

also pass the clim param. 

also possibly a smart scale parameter? That would set the color limits intelligently?
use a diverging colormap with the zero point set at the baseline firing rate? 

###########

DONE Use the other raster plotting code to plot the sorted tuning curve rasters. 
these axes should be shared as well

it would be awesome if we could cluster quickly and tell whether the same unit is really 
responsive to the sound and the laser

move this to the repo as ephysexperiment

find a better name for RecordingDay - this will be the top class and have a method to add new sites
we also need a module name for this. 

The behavFileIdentifier needs to be well documented. Currently it relies on an EphysExperiment object

We need to specify the paradigm in the recording file


Are the event IDs for the laser and the sound the same eventID?


NEXT TIME: How are we going to interface with a database that stores cells for later?


Santiago:
Use rsync to automatically send the behavior data to jarahub when the user saves the data


'''

# def avg_spikes_in_event_locked_timerange_each_combination(spikeTimestamps, trialsEachCond, timeRange):

#     spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
#                                                                                                                  eventOnsetTimes,
#                                                                                                                  timeRange)

#     numSpikesInTimeRangeEachTrial = indexLimitsEachTrial[1,:]-indexLimitsEachTrial[0,:]
#     numInts = np.shape(trialsEachCond)[2]
#     numFreqs = np.shape(trialsEachCond)[1]
#     avgSpikesEachCombination = np.zeros([numInts, numFreqs])

#     for intensity in range(numInts):
#         for frequency in range(numFreqs):
#             trialsThisFreqThisIntensity = trialsEachCond[:,frequency, intensity]
#             spikesEachTrialThisCombination = numSpikesInTimeRangeEachTrial[trialsThisFreqThisIntensity]
#             avgSpikesThisCombination = spikesEachTrialThisCombination.mean()
#             avgSpikesEachCombination[intensity, frequency]=avgSpikesThisCombination

#    return avgSpikesEachCombination

# evokedTR = [0, 0.1]
# evokedHeatmap = avg_spikes_in_event_locked_timerange_each_combination(spikeTimestamps, trialsEachCond, evokedTR)

# baselineTR = [-0.05, 0]
# baselineHeatmap = avg_spikes_in_event_locked_timerange_each_combination(spikeTimestamps, trialsEachCond, baselineTR)

# possibleFreq = np.unique(freqEachTrial)
# possibleIntensity = np.unique(intensityEachTrial)

# tcHeatmap = evokedHeatmap - baselineHeatmap

#plot_array_as_heatmap(evokedHeatmap, cmap='Blues')
#
#plot_array_as_heatmap(heatMap, cmap = 'Blues')

#plot_array_as_heatmap(evokedHeatmap, cmap='bone')
