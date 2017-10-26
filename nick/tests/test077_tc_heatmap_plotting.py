'''
Plotting frequency/intensity heatmaps

sshfs -o idmap=user jarauser@jarahub:/data/jarashare/ /mnt/jarashare
rsync -a --progress --exclude *.continuous jarauser@jarahub:/data/ephys/adap005/2015-12-15_14-02-08 ./
'''

from jaratoolbox import behavioranalysis
from jaratoolbox import spikesanalysis
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from matplotlib import pyplot as plt
import numpy as np

np.random.seed(5)

#--------------- THIS PART JUST SPOOFS THE DATA ---------------
possibleFreq = [0, 1, 2]
possibleIntensity = [0, 1, 2]
eventOnsetTimes = np.arange(0, 1000, 10)
freqEachTrial = []
intensityEachTrial = []
spikeTimestamps = []
# -- The number of spikes is just the freq*intensity
def neural_response_numspikes(freq, intensity):
    return freq*intensity
# -- Add some spikes after each event according to the freq and intensity of that trial
for event in eventOnsetTimes:
    freq = np.random.choice(possibleFreq)
    freqEachTrial.append(freq)
    intensity = np.random.choice(possibleIntensity)
    intensityEachTrial.append(intensity)
    nSpikes = neural_response_numspikes(freq, intensity)
    for spikeInd in range(nSpikes):
        spikeTimestamps.append(event + spikeInd + 1)
spikeTimestamps = np.array(spikeTimestamps)
freqEachTrial = np.array(freqEachTrial)
intensityEachTrial = np.array(intensityEachTrial)
possibleFreq = np.array(possibleFreq)
possibleIntensity = np.array(possibleIntensity)

#--------------- THIS PART PRODUCES THE ARRAY TO PLOT ---------------
timeRange = [0, 6]
(spikeTimesFromEventOnset,
 trialIndexForEachSpike,
 indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,
                                                               eventOnsetTimes,
                                                               timeRange)
CASE=1
if CASE==0: #Freq/intensity
    trialsEachCond = behavioranalysis.find_trials_each_combination(intensityEachTrial,
                                                                possibleIntensity,
                                                                freqEachTrial,
                                                                possibleFreq)
elif CASE==1: #Only a single sorting variable, frequency
    trialsEachCond = behavioranalysis.find_trials_each_type(freqEachTrial, possibleFreq)

avgSpikesArray = spikesanalysis.avg_num_spikes_each_condition(indexLimitsEachTrial, trialsEachCond)

#--------------- THIS PART PLOTS THE ARRAY ---------------
plt.clf()
if CASE==0:
    #for F/I data, the spike array is more understandable if we flip it upside down
    #to make the higher intensities on the top of the plot
    avgSpikesArray = np.flipud(avgSpikesArray)
    plt.imshow(avgSpikesArray, interpolation='none', cmap='Blues')
    ax = plt.gca()
    ax.set_xticks(possibleFreq)
    ax.set_xticklabels(possibleFreq)
    ax.set_xlabel('Freq')
    ax.set_yticks(possibleIntensity)
    ax.set_yticklabels(possibleIntensity[::-1])
    ax.set_ylabel('Intensity')
elif CASE==1:
    plt.plot(avgSpikesArray)
    ax = plt.gca()
    ax.set_xticks(possibleFreq)
    ax.set_xticklabels(possibleFreq)
    ax.set_xlabel('Freq')
    ax.set_ylabel('Average number of spikes')
plt.show()


