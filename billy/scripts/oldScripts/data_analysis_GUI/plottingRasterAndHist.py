'''
Plots raster and histogram
author: Billy Walker
'''

import discrimination_analysis as discrm
import numpy as np
import os
from pylab import *

#####################################################################################################################################################################
#PARAMETERS
#####################################################################################################################################################################
'''
ephysRoot='/home/billywalker/data/ephys/'
ephysSession = '2014-12-24_17-11-53'
subject = 'test019'
sessionstr = '20141224a'
tetrodeID = 1 #Which tetrode to plot
responseRange = [0.10,0.40] #range of time to count spikes in after event onset
timeRange=[-0.5,1] #In seconds. Time range for rastor plot to plot spikes (around some event onset as 0)
binTime = 0.1 #Size of each bin in histogram in seconds
trialsToUse1 = behaveData.incorrectRightward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
trialsToUse2 = behaveData.correctLeftward #This is an array of 1's and 0's to decide which trials to count spikes in and compare to the other trials
Frequency = 0 #This chooses which frequency to look at, numbered out of possible frequencies starting with the lowest frequency as number 0
'''
eventID = 0 #THIS IS THE CHANNEL THAT YOU CARE ABOUT. for example, channel 0 could be the sound presentation and channel 1 could be the trial period
#####################################################################################################################################################################
#####################################################################################################################################################################



 #plottingAllFreqCompareRaster(subject, ephys session, behavior session, tetrode number, index of frequency to plot, bin size for histogram, start time of when to count spikes in raster, end time of when to count spikes in raster, start time of when to plot spikes in raster, end time of when to plot spikes in raster)


def plottingAllFreqRaster(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange):
    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
    ###################################################################################################################################################################################

    allFreqData = discrm.allFreqData(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange)
    spikeTimesFromEventOnset = allFreqData[0]
    sortedIndexForEachSpike = allFreqData[1]
    numTrialsEachFreq = allFreqData[2]
    possibleFreq = allFreqData[3]
    meanSpikesEachFrequency = allFreqData[4]
    xCoordinatesPlot = allFreqData[5]
    spikeMeanInBin1 = allFreqData[6]
    spikeMeanInBin2 = allFreqData[7]

    responseRange=[startTime,endTime]

    close()
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
    return;


def plottingAllFreqCompareRaster(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange):
    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
    ###################################################################################################################################################################################

    allFreqCompareData = discrm.allFreqCompareData(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange)
    spikeTimesFromEventOnsetTrials1 = allFreqCompareData[0]
    spikeTimesFromEventOnsetTrials2 = allFreqCompareData[1]
    sortedIndexForEachSpikeTrials1 = allFreqCompareData[2]
    sortedIndexForEachSpikeTrials2 = allFreqCompareData[3]
    tickPossibleFreq1 = allFreqCompareData[4]
    tickNumTrialsTrials1 = allFreqCompareData[5]
    tickNumTrialsEachFreqTrials1 = allFreqCompareData[6]
    tickPossibleFreq2 = allFreqCompareData[7]
    tickNumTrialsTrials2 = allFreqCompareData[8]
    tickNumTrialsEachFreqTrials2 = allFreqCompareData[9]
    xCoordinatesPlot = allFreqCompareData[10]
    spikeMeanInBin1 = allFreqCompareData[11]
    spikeMeanInBin2 = allFreqCompareData[12]


    close()
    rastorFreq1 = plt.subplot2grid((3,4), (0, 0), colspan=2, rowspan=2)
    plot(spikeTimesFromEventOnsetTrials1, sortedIndexForEachSpikeTrials1, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')


    #Plot the lines across the figure in between each group of sorted trials
    for indf, num in enumerate(tickNumTrialsTrials1):
        rastorFreq1.axhline(y = num, xmin = 0, xmax = 1, color = '0.90', zorder = 0)

    tickPositions1 = tickNumTrialsTrials1 - mean(tickNumTrialsEachFreqTrials1)/2
    tickLabels1 = ["%0.2f" % (tickPossibleFreq1[indf]/1000.0) for indf in range(len(tickPossibleFreq1))]
    rastorFreq1.set_yticks(tickPositions1)
    rastorFreq1.set_yticklabels(tickLabels1)
    ylabel('Frequency Presented (kHz), {} total trials'.format(tickNumTrialsTrials1[-1]))
    title(ephysSession+' TT{0}'.format(tetrodeID))
    xlabel('Time from sound Onset (sec)')

    rastorFreq2 = plt.subplot2grid((3,4), (0, 2), colspan=2, rowspan=2)
    plot(spikeTimesFromEventOnsetTrials2, sortedIndexForEachSpikeTrials2, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')


    #Plot the lines across the figure in between each group of sorted trials
    for indf, num in enumerate(tickNumTrialsTrials2):
        rastorFreq2.axhline(y = num, xmin = 0, xmax = 1, color = '0.90', zorder = 0)

    tickPositions2 = tickNumTrialsTrials2 - mean(tickNumTrialsEachFreqTrials2)/2
    tickLabels2 = ["%0.2f" % (tickPossibleFreq2[indf]/1000.0) for indf in range(len(tickPossibleFreq2))]
    rastorFreq2.set_yticks(tickPositions2)
    rastorFreq2.set_yticklabels(tickLabels2)
    ylabel('Frequency Presented (kHz), {} total trials'.format(tickNumTrialsTrials2[-1]))
    title(ephysSession+' TT{0}'.format(tetrodeID))
    xlabel('Time from sound Onset (sec)')



    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE HISTOGRAM#####################################################################################################
    ###################################################################################################################################################################################

    histogram3 = plt.subplot2grid((3,4), (2, 0), colspan=2)
    bar(xCoordinatesPlot,spikeMeanInBin1, width=binTime)
    ylabel('trialsToUse1, Number of spikes in bin size {} sec'.format(binTime))
    xlabel('Time from sound Onset (sec)')

    histogram4 = plt.subplot2grid((3,4), (2, 2), colspan=2)
    bar(xCoordinatesPlot,spikeMeanInBin2, width=binTime)
    ylabel('trialsToUse2, Number of spikes in bin size {} sec'.format(binTime))
    xlabel('Time from sound Onset (sec)')

    show()
    return;


def plottingOneFreqCompareRaster(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange):
    ###################################################################################################################################################################################
    #####################################################THIS IS FOR THE RASTOR PLOT###################################################################################################
    ###################################################################################################################################################################################


    oneFreqCompareData = discrm.oneFreqCompareData(subject, ephysSession, behaviorSession, tetrodeID, FreqInd, binTime, startTime, endTime, startRange, endRange)
    spikeTimesFromEventOnsetTrials1 = allFreqData[0]
    spikeTimesFromEventOnsetTrials2 = allFreqData[1]
    sortedIndexForEachSpikeTrials1 = allFreqData[2]
    sortedIndexForEachSpikeTrials2 = allFreqData[3]
    xCoordinatesPlot = allFreqData[8]
    spikeMeanInBin1 = allFreqData[9]
    spikeMeanInBin2 = allFreqData[10]

    close()
    rastorFreq1 = plt.subplot2grid((3,4), (0, 0), colspan=2, rowspan=2)
    plot(spikeTimesFromEventOnsetOneFreqTrials1, sortedIndexForEachSpikeOneFreqTrials1, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')

    ylabel1('Frequency Presented (kHz), {} total trials'.format(numTrials1[-1]))
    title1(ephysSession+' TT{0}'.format(tetrodeID))
    xlabel1('Time (sec)')

    rastorFreq2 = plt.subplot2grid((3,4), (0, 0), colspan=2, rowspan=2)
    plot(spikeTimesFromEventOnsetOneFreqTrials2, sortedIndexForEachSpikeOneFreqTrials2, '.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')

    ylabel2('Frequency Presented (kHz), {} total trials'.format(numTrials2[-1]))
    title2(ephysSession+' TT{0}'.format(tetrodeID))
    xlabel2('Time (sec)')



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
    return;
