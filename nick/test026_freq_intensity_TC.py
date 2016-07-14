'''
Author: Nick Ponvert
2014-09-20

This code plots a frequency-intensity tuning curve from LFP data
'''
from jaratoolbox import loadbehavior
from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import *
import os

SAMPLING_RATE=30000.0

#The length of each time window displayed after the stumulus, in seconds. 
secondsEachTrace = 0.1


ephysDir='/home/nick/data/ephys/test075/2014-11-06_17-27-43'
event_filename=os.path.join(ephysDir, 'all_channels.events')

behaviorDir='/home/nick/data/behavior/nick/test075/'
behavDataFileName=os.path.join(behaviorDir, 'test075_tuning_curve_20141106a.h5')

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

#These are the active channels in this recording, sorted by tetrode
tetrodeChannels = np.array([[9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]])

#Get the continuous data
channel = 24 #The channel to plot
reference = 9 #Experimental: plotting without subtracting a reference made all channels look the same. 
cont_filename = os.path.join(ephysDir, '109_CH{0}.continuous'.format(channel))
ref_filename = os.path.join(ephysDir, '109_CH{0}.continuous'.format(reference))
ephysData = loadopenephys.DataCont(cont_filename)
refData = loadopenephys.DataCont(ref_filename)

#Subtract the reference channel (not sure yet if this is a good thing to include.)
#ephysData.samples = ephysData.samples - refData.samples

#The ephys data starts with a positive nonzero timestamp, corresponding to the system time somehow. 
#We need to subtract this from all timestamp values if we want to know what sample number to get. 
startTimestamp = ephysData.timestamps[0]

#Preallocate an array in which to store the values of each mean trace
meanTraceEachSetting = np.empty((len(possibleIntensity), len(possibleFreq), secondsEachTrace*SAMPLING_RATE))

#Loop through the frequencies and intensities in the list of possible settings,
#extracting the trace after the presentation of each possible kind of stimulus.
for indFreq, currentFreq in enumerate(possibleFreq):
    for indIntensity, currentIntensity in enumerate(possibleIntensity):

        #Determine which trials this setting was presented on. 
        trialsThisSetting = np.flatnonzero((freqEachTrial == currentFreq) & (intensityEachTrial == currentIntensity))

        #Get the onset timestamp for each of the trials of this setting. 
        timestampsThisSetting = eventOnsetTimes[trialsThisSetting]
        
        #Subtract the starting timestamp value to get the sample number
        sampleNumbersThisSetting = timestampsThisSetting - startTimestamp

        #Preallocate an array to store the traces for each trial on which this setting was presented. 
        traces = np.empty((len(sampleNumbersThisSetting), secondsEachTrace*SAMPLING_RATE))
        
        #Loop through all of the trials for this setting, extracting the trace after each presentation
        for indSamp, sampNumber in enumerate(sampleNumbersThisSetting):
            trace = ephysData.samples[sampNumber:sampNumber + secondsEachTrace*SAMPLING_RATE]
            trace = trace - trace[0]
            traces[indSamp, :] = trace
            
        #Take the mean of all of the samples for this setting, and store it according to the freq and intensity
        mean_trace = np.mean(traces, axis = 0)
        meanTraceEachSetting[indIntensity, indFreq, :] = mean_trace    
            
#Determine the optimal ylimits based on the greatest minimum and maximum values in the traces. 
maxVoltageAllSettings = np.max(np.max(meanTraceEachSetting, axis = 2))
minVoltageAllSettings = np.min(np.min(meanTraceEachSetting, axis = 2))


#Plot all of the mean traces in a grid according to frequency and intensity
for intensity in range(len(possibleIntensity)):
    #Subplot2grid plots from top to bottom, but we need to plot from bottom to top
    #on the intensity scale. So we make an array of reversed intensity indices.
    intensPlottingInds = range(len(possibleIntensity))[::-1]
    for frequency in range(len(possibleFreq)):
        subplot2grid((len(possibleIntensity), len(possibleFreq)), (intensPlottingInds[intensity], frequency))
        plot(meanTraceEachSetting[intensity, frequency, :])
        ylim([minVoltageAllSettings, maxVoltageAllSettings])
        axis('off')

#This function returns the location of the text labels
#We have to mess with the ideal locations due to the geometry of the plot
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
    figtext(position, 0.075, "%.1f"% (possibleFreq[indp]/1000), ha = 'center')

intensLabelPositions = getYlabelpoints(len(possibleIntensity))
for indp, position in enumerate(intensLabelPositions):
    figtext(0.075, position, "%d"% possibleIntensity[indp])

figtext(0.525, 0.025, "Frequency (kHz)", ha = 'center')
figtext(0.025, 0.5, "Intensity (dB SPL)", va = 'center', rotation = 'vertical')
show()

