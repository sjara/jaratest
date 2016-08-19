'''
Does main computation for comparing raster plots and histograms of outcomes of behavior
author: Billy Walker
'''

from jaratoolbox import spikesanalysis
import numpy as np
from pylab import * #I SHOULD CHANGE THIS. EFFECTS ARGSORT
import os
import loadEphysData
import loadBehaviorData
import decision_discrimination_rasterplot as behaveData

###########################
#ASSUMPTIONS
#There is a sound onset in every trial
###########################

#####################################################################################################################################################################
#PARAMETERS
#####################################################################################################################################################################
'''
ephysRoot='/home/billywalker/data/ephys/test019/'
ephysSession = '2014-12-24_17-11-53'

tetrodeID = 3 #Which tetrode to plot
responseRange = [0.10,0.40] #range of time to count spikes in after event onset
timeRange=[-0.5,1] #In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
binTime = 0.1 #Size of each bin in histogram in seconds
Frequency = 0 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
'''
trialsToUse1 = behaveData.incorrectRightward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
trialsToUse2 = behaveData.correctLeftward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
eventID = 0 #THIS IS THE CHANNEL THAT YOU CARE ABOUT. for example, channel 0 could be the sound presentation and channel 1 could be the trial period
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


def allFreqData(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange):

    timeRange = [startTime, endTime]
    responseRange = [startRange, endRange]

    # -- Load event and spike data --
    ephysData = loadEphysData.loadEphys(subject, ephysSession, tetrodeID)
    eventTimes = ephysData[0]
    multipleEventOnset = ephysData[1]
    eventChannel = ephysData[2]
    spkTimeStamps = ephysData[3]

    # -- Load behavior data --
    

    # -- Number of trials in Behavior data --
    #The number of trials that will be used will be that from the behavior data. The ephys data may contain the same number of trials or one more
    numberOfTrials = behaveData.numberOfTrials


    # -- Only use event onset times of one event --
    oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
    eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want
    #This makes sure that the behavior and ephys data have the same number of trials
    while (numberOfTrials < np.sum(eventOnset)):
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


    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE HISTOGRAM#####################################################################################################
    ###################################################################################################################################################################################


    # -- Pick which trials you care about in counting spikes --
    spikeMeanInBin1 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse1
    spikeMeanInBin2 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse2
    for indBin, spikeCounts in enumerate(spikeNumberInBinPerTrial):
        spikeMeanInBin1[indBin] = np.mean(np.append(spikeCounts[trialsToUse1==1],0))  #The append 0 is just for the edge case that there are no trials to use so np.mean does not give a nan.
        spikeMeanInBin2[indBin] = np.mean(np.append(spikeCounts[trialsToUse2==1],0))



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

    return [spikeTimesFromEventOnset, sortedIndexForEachSpike, numTrialsEachFreq, possibleFreq, meanSpikesEachFrequency, xCoordinatesPlot, spikeMeanInBin1, spikeMeanInBin2]






















def allFreqCompareData(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange):

    timeRange = [startTime, endTime]
    responseRange = [startRange, endRange]

    # -- Load event and spike data --
    ephysData = loadEphysData.loadEphys(subject, ephysSession, tetrodeID)
    eventTimes = ephysData[0]
    multipleEventOnset = ephysData[1]
    eventChannel = ephysData[2]
    spkTimeStamps = ephysData[3]

    # -- Load behavior data --
    
    # -- Number of trials in Behavior data --
    #The number of trials that will be used will be that from the behavior data. The ephys data may contain the same number of trials or one more
    numberOfTrials = behaveData.numberOfTrials


    # -- Only use event onset times of one event --
    oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
    eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want
    #This makes sure that the behavior and ephys data have the same number of trials
    while (numberOfTrials < np.sum(eventOnset)):
        eventOnset = eventOnset[:-1]
    eventOnsetTimes = eventTimes[eventOnset == 1] #This gives only the times of the onset of the channel you want


    eventOnsetTimesTrials1 = eventOnsetTimes[trialsToUse1==1]
    eventOnsetTimesTrials2 = eventOnsetTimes[trialsToUse2==1]



    # -- Convert spike data into np.array's --
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
    (spikeTimesFromEventOnsetTrials1,trialIndexForEachSpikeTrials1,indexLimitsEachTrialTrials1) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesTrials1,timeRange)
    (spikeTimesFromEventOnsetTrials2,trialIndexForEachSpikeTrials2,indexLimitsEachTrialTrials2) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesTrials2,timeRange)
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

    ######################################################################################################################
    #THIS IS FOR ALL FREQUENCIES
    # -- Pick which trials you care about in counting spikes --
    spikeMeanInBin1 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse1
    spikeMeanInBin2 = np.empty(numberOfBins) #This will hold the mean number of spikes in each bin or time range for the trialsToUse2
    for indBin, spikeCounts in enumerate(spikeNumberInBinPerTrial):
        spikeMeanInBin1[indBin] = np.mean(np.append(spikeCounts[trialsToUse1==1],0))  #The append 0 is just for the edge case that there are no trials to use so np.mean does not give a nan.
        spikeMeanInBin2[indBin] = np.mean(np.append(spikeCounts[trialsToUse2==1],0))
    ######################################################################################################################



    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
    ###################################################################################################################################################################################

    targetFreqsTrials1 = targetFreqs[trialsToUse1==1]
    targetFreqsTrials2 = targetFreqs[trialsToUse2==1]


    sortedTrials1 = [] #array that sorts trials for different frequencies
    numTrialsEachFreq1 = []  #Used to plot lines after each group of sorted trials
    for indf1,oneFreq1 in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
        indsThisFreq1 = np.flatnonzero(targetFreqsTrials1==oneFreq1) #this gives indices of this frequency
        sortedTrials1 = np.concatenate((sortedTrials1,indsThisFreq1)) #adds all indices to a list called sortedTrials
        numTrialsEachFreq1.append(len(indsThisFreq1)) #finds number of trials each frequency has
    sortingIndsTrials1 = argsort(sortedTrials1) #gives array of indices that would sort the sortedTrials

    sortedIndexForEachSpikeTrials1 = sortingIndsTrials1[trialIndexForEachSpikeTrials1] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike

    sortedTrials2 = [] #array that sorts trials for different frequencies
    numTrialsEachFreq2 = []  #Used to plot lines after each group of sorted trials
    for indf2,oneFreq2 in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
        indsThisFreq2 = np.flatnonzero(targetFreqsTrials2==oneFreq2) #this gives indices of this frequency
        sortedTrials2 = np.concatenate((sortedTrials2,indsThisFreq2)) #adds all indices to a list called sortedTrials
        numTrialsEachFreq2.append(len(indsThisFreq2)) #finds number of trials each frequency has
    sortingIndsTrials2 = argsort(sortedTrials2) #gives array of indices that would sort the sortedTrials

    sortedIndexForEachSpikeTrials2 = sortingIndsTrials2[trialIndexForEachSpikeTrials2] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike

    #The cumulative sum of the list of specific frequency presentations, used below for plotting the lines across the figure. 
    numTrialsTrials1 = cumsum(numTrialsEachFreq1)
    numTrialsTrials2 = cumsum(numTrialsEachFreq2)


    #This is used to plot frequency tick marks on side of raster plot.
    tickPossibleFreq1 = np.empty(0)
    tickNumTrialsTrials1 = np.empty(0)
    tickNumTrialsEachFreq1 = np.empty(0)
    for indf in range(len(possibleFreq)):
        if (numTrialsEachFreq1[indf]!=0):
            tickPossibleFreq1 = np.append(tickPossibleFreq1,possibleFreq[indf])
            tickNumTrialsTrials1 = np.append(tickNumTrialsTrials1,numTrialsTrials1[indf])
            tickNumTrialsEachFreq1 = np.append(tickNumTrialsEachFreq1,numTrialsEachFreq1[indf])
    tickPossibleFreq2 = np.empty(0)
    tickNumTrialsTrials2 = np.empty(0)
    tickNumTrialsEachFreq2 = np.empty(0)
    for indf in range(len(possibleFreq)):
        if (numTrialsEachFreq2[indf]!=0):
            tickPossibleFreq2 = np.append(tickPossibleFreq2,possibleFreq[indf])
            tickNumTrialsTrials2 = np.append(tickNumTrialsTrials2,numTrialsTrials2[indf])
            tickNumTrialsEachFreq2 = np.append(tickNumTrialsEachFreq2,numTrialsEachFreq2[indf])


    return [spikeTimesFromEventOnsetTrials1, spikeTimesFromEventOnsetTrials2,sortedIndexForEachSpikeTrials1,sortedIndexForEachSpikeTrials2,tickPossibleFreq1,tickNumTrialsTrials1,tickNumTrialsEachFreq1,tickPossibleFreq2,tickNumTrialsTrials2,tickNumTrialsEachFreq2,xCoordinatesPlot, spikeMeanInBin1, spikeMeanInBin2]





























def oneFreqCompareData(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange):

    timeRange = [startTime, endTime]
    responseRange = [startRange, endRange]

    # -- Load event and spike data --
    ephysData = loadEphysData.loadEphys(subject, ephysSession, tetrodeID)
    eventTimes = ephysData[0]
    multipleEventOnset = ephysData[1]
    eventChannel = ephysData[2]
    spkTimeStamps = ephysData[3]

    # -- Load behavior data --
    
    # -- Number of trials in Behavior data --
    #The number of trials that will be used will be that from the behavior data. The ephys data may contain the same number of trials or one more
    numberOfTrials = behaveData.numberOfTrials

    oneFreqTrials = targetFreq==possibleFreq[FreqInd]
    trailsToUse1 = trialsToUse1*oneFreqTrials
    trialsToUse2 = trialsToUse2*oneFreqTrials

    # -- Only use event onset times of one event --
    oneEvent = eventChannel==eventID #This picks out which channel you care about if there is more that one event
    eventOnset = multipleEventOnset*oneEvent #This keeps the correct size of the array to match eventTimes and picks out the onset of the channel you want
    #This makes sure that the behavior and ephys data have the same number of trials
    while (numberOfTrials < np.sum(eventOnset)):
        eventOnset = eventOnset[:-1]
    eventOnsetTimes = eventTimes[eventOnset == 1] #This gives only the times of the onset of the channel you want


    eventOnsetTimesTrials1 = eventOnsetTimes[trialsToUse1==1]
    eventOnsetTimesTrials2 = eventOnsetTimes[trialsToUse2==1]



    # -- Convert spike data into np.array's --
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimes,timeRange)
    (spikeTimesFromEventOnsetTrials1,trialIndexForEachSpikeTrials1,indexLimitsEachTrialTrials1) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesTrials1,timeRange)
    (spikeTimesFromEventOnsetTrials2,trialIndexForEachSpikeTrials2,indexLimitsEachTrialTrials2) = spikesanalysis.eventlocked_spiketimes(spkTimeStamps,eventOnsetTimesTrials2,timeRange)
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


    ######################################################################################################################
    #THIS IS FOR ONE FREQUENCY
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




    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
    ###################################################################################################################################################################################

    targetFreqsTrials1 = targetFreqs[trialsToUse1==1]
    targetFreqsTrials2 = targetFreqs[trialsToUse2==1]


    sortedTrials1 = [] #array that sorts trials for different frequencies
    numTrialsEachFreq1 = []  #Used to plot lines after each group of sorted trials
    for indf1,oneFreq1 in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
        indsThisFreq1 = np.flatnonzero(targetFreqsTrials1==oneFreq1) #this gives indices of this frequency
        sortedTrials1 = np.concatenate((sortedTrials1,indsThisFreq1)) #adds all indices to a list called sortedTrials
        numTrialsEachFreq1.append(len(indsThisFreq1)) #finds number of trials each frequency has
    sortingIndsTrials1 = argsort(sortedTrials1) #gives array of indices that would sort the sortedTrials

    sortedIndexForEachSpikeTrials1 = sortingIndsTrials1[trialIndexForEachSpikeTrials1] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike

    sortedTrials2 = [] #array that sorts trials for different frequencies
    numTrialsEachFreq2 = []  #Used to plot lines after each group of sorted trials
    for indf2,oneFreq2 in enumerate(possibleFreq): #indf is index of this freq and oneFreq is the frequency
        indsThisFreq2 = np.flatnonzero(targetFreqsTrials2==oneFreq2) #this gives indices of this frequency
        sortedTrials2 = np.concatenate((sortedTrials2,indsThisFreq2)) #adds all indices to a list called sortedTrials
        numTrialsEachFreq2.append(len(indsThisFreq2)) #finds number of trials each frequency has
    sortingIndsTrials2 = argsort(sortedTrials2) #gives array of indices that would sort the sortedTrials

    sortedIndexForEachSpikeTrials2 = sortingIndsTrials2[trialIndexForEachSpikeTrials2] #Takes values of trialIndexForEachSpike and finds value of sortingInds at that index and makes array. This array gives an array with the sorted index of each trial for each spike

    #The cumulative sum of the list of specific frequency presentations, used below for plotting the lines across the figure. 
    numTrialsTrials1 = cumsum(numTrialsEachFreq1)
    numTrialsTrials2 = cumsum(numTrialsEachFreq2)


    #This is used to plot frequency tick marks on side of raster plot.
    tickPossibleFreq1 = np.empty(0)
    tickNumTrialsTrials1 = np.empty(0)
    tickNumTrialsEachFreq1 = np.empty(0)
    for indf in range(len(possibleFreq)):
        if (numTrialsEachFreq1[indf]!=0):
            tickPossibleFreq1 = np.append(tickPossibleFreq1,possibleFreq[indf])
            tickNumTrialsTrials1 = np.append(tickNumTrialsTrials1,numTrialsTrials1[indf])
            tickNumTrialsEachFreq1 = np.append(tickNumTrialsEachFreq1,numTrialsEachFreq1[indf])
    tickPossibleFreq2 = np.empty(0)
    tickNumTrialsTrials2 = np.empty(0)
    tickNumTrialsEachFreq2 = np.empty(0)
    for indf in range(len(possibleFreq)):
        if (numTrialsEachFreq2[indf]!=0):
            tickPossibleFreq2 = np.append(tickPossibleFreq2,possibleFreq[indf])
            tickNumTrialsTrials2 = np.append(tickNumTrialsTrials2,numTrialsTrials2[indf])
            tickNumTrialsEachFreq2 = np.append(tickNumTrialsEachFreq2,numTrialsEachFreq2[indf])


    return [spikeTimesFromEventOnsetTrials1, spikeTimesFromEventOnsetTrials2,sortedIndexForEachSpikeTrials1,sortedIndexForEachSpikeTrials2,tickPossibleFreq1,tickNumTrialsTrials1,tickNumTrialsEachFreq1,tickPossibleFreq2,tickNumTrialsTrials2,tickNumTrialsEachFreq2,xCoordinatesPlot, spikeMeanInBin1, spikeMeanInBin2]


