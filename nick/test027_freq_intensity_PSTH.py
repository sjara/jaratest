from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
from collections import defaultdict
import numpy as np
from pylab import *
import os

SAMPLING_RATE = 30000.0
PLOTTING_WINDOW = 0.1 #Window to plot, in seconds

ephysDir='/home/jarauser/data/ephys/pinp003/2015-06-24_18-55-40'
event_filename=os.path.join(ephysDir, 'all_channels.events')

behaviorDir='/home/jarauser/data/behavior/nick/pinp003'
behavDataFileName=os.path.join(behaviorDir, 'pinp003_laser_tuning_curve_20150624i.h5')

#Extract the frequency presented each trial from the behavior data
bdata = loadbehavior.BehaviorData(behavDataFileName,readmode='full')
freqEachTrial = bdata['currentFreq']
intensityEachTrial = bdata['currentIntensity']

possibleFreq = np.unique(freqEachTrial) 
possibleIntensity = np.unique(intensityEachTrial)

#Get the event timestamps from openEphys
ev=loadopenephys.Events(event_filename)
evID=np.array(ev.eventID)
eventOnsetTimes=ev.timestamps[evID==1] #The timestamps of all of the stimulus onsets

tetrode = 6 #The tetrode to plot
spikeFilename = os.path.join(ephysDir, 'Tetrode{}.spikes'.format(tetrode))
spikeData = loadopenephys.DataSpikes(spikeFilename)

spikeTimestamps = spikeData.timestamps

allSettingsSpikes = defaultdict(dict) #2D dictionary to hold the spiketimes arrays organized by frequency and intensity

for indFreq, currentFreq in enumerate(possibleFreq):
    for indIntensity, currentIntensity in enumerate(possibleIntensity):

        #Determine which trials this setting was presented on. 
        trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))

        #Get the onset timestamp for each of the trials of this setting. 
        timestampsThisSetting = eventOnsetTimes[trialsThisSetting]
        
        spikesAfterThisSetting = np.array([])
        #Loop through all of the trials for this setting, extracting the trace after each presentation
        for indts, eventTimestamp in enumerate(timestampsThisSetting):
            spikes = spikeTimestamps[(spikeTimestamps >= eventTimestamp) & (spikeTimestamps <= eventTimestamp + SAMPLING_RATE * PLOTTING_WINDOW)]
            spikes = spikes - eventTimestamp
            spikes = spikes / 30 #Spikes in ms after the stimulus
            
            spikesAfterThisSetting = np.concatenate((spikesAfterThisSetting, spikes))
        allSettingsSpikes[indFreq][indIntensity] = spikesAfterThisSetting #Put the spikes into the 2d dict

maxBinCount = []
for indI, intensity in enumerate(possibleIntensity):
    for indF, frequency in enumerate(possibleFreq):
        h, bin_edges = histogram(allSettingsSpikes[indF][indI]) #Dict is ordered by freq and then by Int.
        maxBinCount.append(max(h))

maxNumSpikesperBin = max(maxBinCount)

for intensity in range(len(possibleIntensity)):
    #Subplot2grid plots from top to bottom, but we need to plot from bottom to top
    #on the intensity scale. So we make an array of reversed intensity indices.
    intensPlottingInds = range(len(possibleIntensity))[::-1]
    for frequency in range(len(possibleFreq)):
        if (intensity == len(possibleIntensity) - 1) & (frequency == len(possibleFreq) -1):
            ax2 = subplot2grid((len(possibleIntensity), len(possibleFreq)), (intensPlottingInds[intensity], frequency))
            ax2.hist(allSettingsSpikes[frequency][intensity])
            ax2.set_ylim([0, maxNumSpikesperBin])
            ax2.get_xaxis().set_ticks([])
        else:
            ax = subplot2grid((len(possibleIntensity), len(possibleFreq)), (intensPlottingInds[intensity], frequency))
            ax.hist(allSettingsSpikes[frequency][intensity])
            ax.set_ylim([0, maxNumSpikesperBin])
            ax.set_axis_off()

def getXlabelpoints(n):
    rawArray = array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
    diffFromCenter = rawArray - 0.6
    partialDiffFromCenter = diffFromCenter * 0.175 #Percent change has to be determined empirically
    finalArray = rawArray - partialDiffFromCenter
    return finalArray

#Not sure yet if similar modification to the locations will be necessary. 
def getYlabelpoints(n):
    rawArray = array(range(1, n+1))/float(n+1) #The positions in a perfect (0,1) world
    return rawArray

freqLabelPositions = getXlabelpoints(len(possibleFreq))
for indp, position in enumerate(freqLabelPositions):
    figtext(position, 0.065, "%.1f"% (possibleFreq[indp]/1000), ha = 'center')

intensLabelPositions = getYlabelpoints(len(possibleIntensity))
for indp, position in enumerate(intensLabelPositions):
    figtext(0.075, position, "%d"% possibleIntensity[indp])

figtext(0.525, 0.025, "Frequency (kHz)", ha = 'center')
figtext(0.025, 0.5, "Intensity (dB SPL)", va = 'center', rotation = 'vertical')
show()

#if #Has some spikes            
#    hist(spikesAfterThisSetting)
