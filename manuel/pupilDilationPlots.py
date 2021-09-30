'''
This script is for the project of pupil dilation. It is intended to obtain pupil data, its mean, the desired time windows, create a slope and bar plots
'''

import numpy as np
import matplotlib.pyplot as plt

#Lines to change for each video: 10 and 34

proc = np.load('./project_videos/projectOutputs/pure001_20210928_syncVisibleNoSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data---
pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.


#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video.

'''
with np.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(blink)
'''

#---obtain values where sync signal is on---
blink2Bool = np.logical_and(blink2>45000, blink2<55000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#---plot to find out which time range can be used---
'''
fig, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 75, 0.1))) #Set ups number of ticks in both plots
pupil.plot(timeVec, pArea)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.grid(b = True)
blink.plot(timeVec, blink2)
plt.show()
'''


def onset_values(array, k): 

     '''
     Helps to find onset start values of the sync singal in any given array: 
     Args: 
     array = array that contains data of the sync signal
     k = step number to create the range from 0 to n index of the given array
     Returns:
     startValuesVec = an array of the indices containing the start onset values of the sync signal.
    ''' 
     firstIndexValue = 0 
     lastIndexValue = len(array)-1 
     stepNumber = k
     startIndicesValues = range(firstIndexValue, lastIndexValue, stepNumber)
     startIndicesVec = np.array(startIndicesValues)
     onsetStartValues = np.take(array, startIndicesVec)
     return (onsetStartValues)

syncOnsetValues = onset_values(indicesValueSyncSignal, 2)
timeOfBlink2Event = timeVec[syncOnsetValues] # Provides the time values in which the sync signal is on.


timeRange = np.array([-1, 1]) # Range of time window, one second before the sync signal is on and one second after is on.

samplingRate = 1/(timeVec[1]-timeVec[0])
windowSampleRange = samplingRate*np.array(timeRange) 
windowSampleVec = np.arange(*windowSampleRange, dtype=int)
windowTimeVec = windowSampleVec/samplingRate
nSamples = len(windowTimeVec)
nTrials = len(timeOfBlink2Event)

#---obtain samples for each trial, regarding sync signal onset---
def eventlocked_signal(timeVec, signal, eventOnsetTimes, windowTimeRange):
    '''
    Make array of signal traces locked to an event.
    Args:
        timeVec (np.array): time of each sample in the signal.
       signal (np.array): samples of the signal to process.
        eventOnsetTimes (np.array): time of each event.
        windowTimeRange (list or np.array): 2-element array defining range of window to extract.
    Returns: 
        windowTimeVec (np.array): time of each sample in the window w.r.t. the event.
        lockedSignal (np.array): extracted windows of signal aligned to event. Size (nSamples,nEvents)
    '''
    samplingRate = 1/(timeVec[1]-timeVec[0])
    windowSampleRange = samplingRate*np.array(windowTimeRange) 
    windowSampleVec = np.arange(*windowSampleRange, dtype=int)
    windowTimeVec = windowSampleVec/samplingRate
    nSamples = len(windowTimeVec)
    nTrials = len(eventOnsetTimes)
    lockedSignal = np.empty((nSamples,nTrials))
    for inde,eventTime in enumerate(eventOnsetTimes):
       eventSample = np.searchsorted(timeVec, eventTime)
       #print('eventS:',eventSample)
       thiswin = windowSampleVec + eventSample
       #print('thiswin:',thiswin)
       lockedSignal[:,inde] = signal[thiswin]
    return (windowTimeVec, lockedSignal)

windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)



#--check if the number of samples and trials are correct---
print('this are the total values on/off from signal:',len(indicesValueSyncSignal))
print('you must obtain half of it, due you need only the onset values:',len(syncOnsetValues))
print('to know what are the size of the slices, figure out which index is 0 in windowSampleVec variable:',windowSampleVec)



#---obtain mean trial values pre and post signal, plot slope plot---
preSignal = windowed_signal[0:30] # Takes the values of the pArea between [-3s to 0s) within the time window
postSignal = windowed_signal[30:60] # Takes the values of the pArea between [0s to 3s] within the time window
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']

def scatter_plotting(preArray, postArray):
     '''
     Shows how to plot 2 conditions regarding a stimulus
     Args:
     preArray = data before stimulus
     postArray = data after stimulus
     returns:
     plt.show() = slope plot with both defined conditions and the data corresponding to each condition
     ''' 
     xLabelsToPlot = ['Pre sync ignal', 'Post sync signal'] 
     dataToPlot = [preArray, postArray] 
     fig, trials = plt.subplots(1,1) 
     trials.plot(xLabelsToPlot, dataToPlot, marker = 'o', linewidth=1) 
     trials.set(title = 'Pupil behavior along trials under the Condition: sync + Visible Light + NoSound', ylabel = 'Mean Pupil Area')
     plt.ylim(100, 1500) 
     plt.show() 
     return(plt.show())

prePostSignalpArea = scatter_plotting(averagePreSignal, averagePostSignal)


#---obtain mean pupil area and bar plot vs conditions---

def bar_plotting(meanSignalsValues1, meanSignalsValues2, xlabel1, xlabel2, stdData1, stdData2):
     ''' 
     Creates bar plots for two mean values
     Args: 
     meanSignalsValues1: nump.array type, first data set to plot  
     meanSignalsValues2: nump.array type, second data set to plot 
     xlabel1: str type, first condition to compare 
     xlabel: str type, second condition to compare
     stdData1: first dataset from which the standard deviation will be calculated from
     stdaData1: second dataset from which the standard deviation will be calculated from
     returns: 
     plt.show(): bar plot comparing the average pupil area before and after signal onset 
     ''' 
     
     meanPreSignal = meanSignalsValues1.mean(axis = 0) 
     meanPostSignal = meanSignalsValues2.mean(axis = 0)
     preSignalStd = np.std(stdData1)
     postSignalStd = np.std(stdData2) 
     xlabels = [xlabel1, xlabel2]
     barMeanValues = [meanPreSignal, meanPostSignal]
     stdErrors = [preSignalStd, postSignalStd] 
     fig, barPlots = plt.subplots()
     barPlots.bar(xlabels, barMeanValues, yerr = stdErrors)
     barPlots.errorbar(xlabels, barMeanValues, yerr = stdErrors, capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots.set(title = 'Mean Pupil Area Vs Condition: sync + Visible Light + NoSound', ylabel = 'Pupil Area')
     plt.ylim(40, 800) 
     plt.show() 
     return(plt.show())

barPlotting = bar_plotting(averagePreSignal, averagePostSignal, 'pre sync signal onset', 'post sync signal onset', preSignal, postSignal)

#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([0.01, 2])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)

pAreaDilatedMean = pAreaDilated.mean(axis = 1)

def pupilDilation_time(time, data):
 '''
 Create a time window to identify the pupil's dilation time range
 Args:
 time: time window to be used for the plot
 data: mean value of the trials
 Returns:
 plt.show(): plot with all of the trials in the selected time window
 '''
 fig, signalsPlots = plt.subplots()
 signalsPlots.plot(time, data)
 signalsPlots.set(title = 'Trials in time window', ylabel = 'Pupil area', xlabel = 'Time(s)')
 plt.show()
 return(plt.show())

trialsWindow = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean)

'''
def compared_time_window(signalRange, signalToCompare, signalToCompareTime):
 signalValuesRange = signalRange[1:3]
 signalTimeValues = np.arange(0,2,1)
 fig, (sync,newWindow) = plt.subplots(2,1, constrained_layout = 'True')
 newWindow.plot(signalToCompareTime, signalToCompare)
 newWindow.set(xlabel = 'Time(s)', ylabel = 'pupil area')
 sync.plot(signalTimeValues, signalValuesRange)
 sync.set(title = 'sync signal of stimulus', ylabel = 'on/off')
 plt.show()
 return(plt.show())

a = compared_time_window(indicesValueSyncSignal, signalsAveragedRange, relaxingTimeWindowVec)
'''
 
