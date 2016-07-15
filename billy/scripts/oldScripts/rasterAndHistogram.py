'''
loadEphysData.py
Load ephys events
author: Billy Walker
'''

from jaratoolbox import loadopenephys
from jaratoolbox import spikesanalysis
import numpy as np
from pylab import * #I SHOULD CHANGE THIS. EFFECTS ARGSORT
import os
import decision_discrimination_rasterplot as behaveData

###########################
#ASSUMPTIONS
#There is a sound onset in every trial
###########################

#####################################################################################################################################################################
#PARAMETERS
#####################################################################################################################################################################

ephysRoot='/home/billywalker/data/ephys/test019/psyCurve/'
ephysSession = '2014-12-20_22-37-24'

tetrodeID = 1 #Which tetrode to plot
responseRange = [0.10,0.40] #range of time to count spikes in after event onset
timeRange=[-0.5,1] #In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
binTime = 0.1 #Size of each bin in histogram in seconds
trialsToUse1 = behaveData.incorrectRightward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
trialsToUse2 = behaveData.correctLeftward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
Frequency = 0 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
#numberOfBins = 4 #number of bins to separate spikes into in the timeRange
#####################################################################################################################################################################
#####################################################################################################################################################################

#####################################################################
#FROM BEHAVIOR DATA
possibleFreq = behaveData.possibleFreq #sorted array of all frequencies presented in this behavior
targetFreqs = behaveData.targetFrequencies #array of which frequency was presented for each trial
#####################################################################

# -- Global variables --
SAMPLING_RATE=30000.0


# -- Load event data and convert event timestamps to ms --
ephysDir = os.path.join(ephysRoot, ephysSession)
eventFilename=os.path.join(ephysDir, 'all_channels.events')
events = loadopenephys.Events(eventFilename) # Load events data
eventTimes=np.array(events.timestamps)/SAMPLING_RATE #get array of timestamps for each event and convert to seconds by dividing by sampling rate (Hz). matches with eventID and 
multipleEventOnset=np.array(events.eventID)  #loads the onset times of all events (matches up with eventID to say if event 1 went on (1) or off (0)
eventChannel = np.array(events.eventChannel) #loads the ID of the channel of the event. For example, 0 is sound event, 1 is trial event, 2 ...

# -- Load spike data and convert spike timestamps to ms --
spike_filename=os.path.join(ephysDir, 'Tetrode{0}.spikes'.format(tetrodeID)) #make a path to ephys spike data of specified tetrode tetrodeID
spikeData=loadopenephys.DataSpikes(spike_filename) #load spike data from specified tetrode tetrodeID
spkTimeStamps=np.array(spikeData.timestamps)/SAMPLING_RATE #array of timestamps for each spike in seconds (thats why you divide by sampling rate)


# -- Number of trials in Behavior data --
#The number of trials that will be used will be that from the behavior data. The ephys data may contain the same number of trials or one more
numberOfTrials = behaveData.numberOfTrials


# -- Only use event onset times of one event --
eventID = 0 #THIS IS THE CHANNEL THAT YOU CARE ABOUT. for example, channel 0 could be the sound presentation and channel 1 could be the trial period
oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want
while (numberOfTrials != np.sum(eventOnset)):
        eventOnset = eventOnset[:-1]
eventOnsetTimes = eventTimes[eventOnset == 1] #This gives only the times of the onset of the channel you want



# -- Convert spike data into np.array's --
(spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
''' spikesanalysis.eventlocked_spiketimes
    Create a vector with the spike timestamps w.r.t. events onset.

    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = 
        eventlocked_spiketimes(timeStamps,eventOnsetTimes,timeRange)

    timeStamps: (np.array) the time of each spike.
    eventOnsetTimes: (np.array) the time of each instance of the event to lock to.
    timeRange: (list or np.array) two-element array specifying time-range to extract around event.

    spikeTimesFromEventOnset: 1D array with time of spikes locked to event.
    trialIndexForEachSpike: 1D array with the trial corresponding to each spike.
       The first spike index is 0.
    indexLimitsEachTrial: [2,nTrials] range of spikes for each trial. Note that
       the range is from firstSpike to lastSpike+1 (like in python slices)
    spikeIndices
'''


# -- Make np.array of time ranges for bins
startTime = float(timeRange[0]) #makes sure that these are floats so division works as expected
endTime = float(timeRange[1])
fullTime = endTime - startTime
numberOfBins = int((fullTime//binTime)+1)
binTimeRanges = np.empty([numberOfBins,2]) #Gives np.array of time ranges for each bin
xCoordinatesPlot = np.empty(numberOfBins)
for indBin in range(0,numberOfBins):
    xCoordinatesPlot[indBin]=startTime+indBin*binTime
    binTimeRanges[indBin]=np.array([(startTime+indBin*binTime),(startTime+(indBin+1)*binTime)])


'''
# -- Make np.array of time ranges for bins
startTime = float(timeRange[0]) #makes sure that these are floats so division works as expected
endTime = float(timeRange[1])
fullTime = endTime - startTime
binTime = fullTime/numberOfBins
binTimeRanges = np.empty([numberOfBins,2]) #Gives np.array of time ranges for each bin
xCoordinatesPlot = np.empty(numberOfBins)
for indBin in range(0,numberOfBins):
    xCoordinatesPlot[indBin]=startTime+indBin*binTime
    binTimeRanges[indBin]=np.array([(startTime+indBin*binTime),(startTime+(indBin+1)*binTime)])
'''


# -- Find the number of spikes in each bin --
spikeNumberInBinPerTrial = np.empty([numberOfBins,numberOfTrials])
for i,binRange in enumerate(binTimeRanges):
    spikeNumberInBinPerTrial[i] = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,binRange) #array of the number of spikes in range for each trial
''' spikesanalysis.count_spikes_in_range
    Count number of spikes on each trial in a given time range.

       spikeTimesFromEventOnset: vector of spikes timestamps with respect
         to the onset of the event.
       indexLimitsEachTrial: each column contains [firstInd,lastInd+1] of the spikes on a trial.
       timeRange: time range to evaluate. Spike times exactly at the limits are not counted.

       returns nSpikes
'''

##############################
#THIS COULD BE A SEPARATE MODULE
##############################

######################################################################################################################
#THIS IS FOR ALL FREQUENCIES
# -- Pick which trials you care about in counting spikes --
spikeMeanInBin1 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse1
spikeMeanInBin2 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse2
for indBin, spikeCounts in enumerate(spikeNumberInBinPerTrial):
    spikeMeanInBin1[indBin] = np.mean(np.append(spikeCounts[trialsToUse1==1],0))  #The append 0 is just for the edge case that there are no trials to use so np.mean does not give a nan.
    spikeMeanInBin2[indBin] = np.mean(np.append(spikeCounts[trialsToUse2==1],0))
######################################################################################################################
'''
######################################################################################################################
#THIS IS FOR ALL ONE FREQUENCY
# -- Pick which trials you care about in counting spikes --
trialsOfFreq = targetFreqs==possibleFreq[Frequency] #array of booleans that is true if the frequency chosen was played in that trial
trialToUseWithFreq1 = trialsToUse1*trialsOfFreq  #array with 1 is this is a trial to use and of the frequency chosen and 0 if not
trialToUseWithFreq2 = trialsToUse2*trialsOfFreq  #array with 1 is this is a trial to use and of the frequency chosen and 0 if not
spikeMeanInBin1 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse1 for the frequency chosen
spikeMeanInBin2 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse2 for the frequency chosen
for indBin, spikeCounts in enumerate(spikeNumberInBinPerTrial):
    spikeMeanInBin1[indBin] = np.mean(np.append(spikeCounts[trialToUseWithFreq1==1],0)) #The append 0 is just for the edge case that there are no trials to use with this frequency so np.mean does not give a nan.
    spikeMeanInBin2[indBin] = np.mean(np.append(spikeCounts[trialToUseWithFreq2==1],0))
######################################################################################################################
'''






###################################################################################################################################################################################
#####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
###################################################################################################################################################################################


sortedTrials = [] #array that sorts trials for different frequencies
numTrialsEachFreq = []  #Used to plot lines after each group of sorted trials
for indf,oneFreq in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
    indsThisFreq = np.flatnonzero(targetFreqs==oneFreq) #this gives indices of this frequency
    sortedTrials = np.concatenate((sortedTrials,indsThisFreq)) #adds all indices to a list called sortedTrials
    numTrialsEachFreq.append(len(indsThisFreq)) #finds number of trials each frequency has
sortingInds = argsort(sortedTrials) #gives array of indices that would sort the sortedTrials

sortedIndexForEachSpike = sortingInds[trialIndexForEachSpike] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike


nSpikes = spikesanalysis.count_spikes_in_range(spikeTimesFromEventOnset,indexLimitsEachTrial,responseRange) #array of the number of spikes in range for each trial
'''Count number of spikes on each trial in a given time range.

       spikeTimesFromEventOnset: vector of spikes timestamps with respect
         to the onset of the event.
       indexLimitsEachTrial: each column contains [firstInd,lastInd+1] of the spikes on a trial.
       timeRange: time range to evaluate. Spike times exactly at the limits are not counted.

       returns nSpikes
'''
# -- Calculate average firing for each freq --
meanSpikesEachFrequency = np.empty(len(possibleFreq))
for indf,oneFreq in enumerate(possibleFreq):
    meanSpikesEachFrequency[indf] = np.mean(nSpikes[indf])




clf()
rastorFreq1 = plt.subplot2grid((3,4), (0, 0), colspan=3, rowspan=2)
plot(spikeTimesFromEventOnset, sortedIndexForEachSpike, '.', ms=1)
axvline(x=0, ymin=0, ymax=1, color='r')

#The cumulative sum of the list of specific frequency presentations, 
#used below for plotting the lines across the figure. 
numTrials = cumsum(numTrialsEachFreq)

#Plot the lines across the figure in between each group of sorted trials
for indf, num in enumerate(numTrials):
    rastorFreq1.axhline(y = num, xmin = 0, xmax = 1, color = '0.90', zorder = 0)

tickPositions = numTrials - mean(numTrialsEachFreq)/2
tickLabels = ["%0.2f" % (possibleFreq[indf]/1000.0) for indf in range(len(possibleFreq))]
rastorFreq1.set_yticks(tickPositions)
rastorFreq1.set_yticklabels(tickLabels)
ylabel('Frequency Presented (kHz), {} total trials'.format(numTrials[-1]))
title(ephysSession+' TT{0}'.format(tetrodeID))
xlabel('Time (sec)')


rastorFreq2 = plt.subplot2grid((3,4), (0, 3), colspan=1, rowspan=2)
rastorFreq2.set_xscale('log')
plot(possibleFreq,meanSpikesEachFrequency,'o-')
ylabel('Avg spikes in window {0}-{1} sec'.format(*responseRange))
xlabel('Frequency')



###################################################################################################################################################################################
#####################################################THIS IS FOR THE HISTOGRAM#####################################################################################################
###################################################################################################################################################################################

histogram3 = plt.subplot2grid((3,4), (2, 0), colspan=2)
bar(xCoordinatesPlot,spikeMeanInBin1, width=binTime)
ylabel('trialsToUse1, Number of spikes in bin size {} sec'.format(binTime))
xlabel('Time (sec)')

histogram4 = plt.subplot2grid((3,4), (2, 2), colspan=2)
bar(xCoordinatesPlot,spikeMeanInBin2, width=binTime)
ylabel('trialsToUse2, Number of spikes in bin size {} sec'.format(binTime))
xlabel('Time (sec)')

show()
