'''
This script is for the project of pupil dilation. It is intended to obtain pupil data, its mean, the desired time windows, create a slope and bar plots
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#README: Lines to change for each video: 11, 35, 61, 111, and 112

proc = np.load('./project_videos/projectOutputs/pure003_20210928_syncVisibleNoSound_01_proc.npy', allow_pickle = True).item()
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
blink2Bool = np.logical_and(blink2>20000, blink2<55000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

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

timeRange = np.array([-0.68, 0.68]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]

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
print()
print('this are the total values on/off from signal:',len(indicesValueSyncSignal))
print('you must obtain half of it, due you need only the onset values:',len(syncOnsetValues))
print('to know what are the size of the slices, figure out which index is 0 in windowSampleVec variable:',windowSampleVec)
print()



#---obtain mean trial values pre and post signal, plot slope plot---
preSignal = windowed_signal[0:20] # Takes the values of the pArea between timeRange within the time window. [0:28] for experimental and [0:18] for controls
postSignal = windowed_signal[20:41] # Takes the values of the pArea between timeRange within the time window. [28:57] for experimental and [18:36] for controls
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
     trials.set_xlabel('Conditions') 
     trials.set(title = 'Average trials signals', ylabel = 'Mean Pupil Area')
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
     barPlots.set_xlabel('Conditions')
     barPlots.set(title = 'Pupil Area before and after stimulus', ylabel = 'Mean Pupil Area')
     plt.ylim(40, 800) 
     plt.show() 
     return(plt.show())

barPlotting = bar_plotting(averagePreSignal, averagePostSignal, 'pre sync signal onset', 'post sync signal onset', preSignal, postSignal)

#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([-2, 2])
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
 signalsPlots.set(title = 'Averaged trials in time window', ylabel = 'Pupil area', xlabel = 'Time(s)')
 #plt.ylim(150, 800)
 plt.show()
 return(plt.show())

trialsWindow = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean)

#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value:', wstat,',',  'P-value:', pval )

















proc1 = np.load('./project_videos/projectOutputs/pure003_20210928_syncNoSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data---
pupil1 = proc1['pupil'][0] # Dic.
pArea1 = pupil1['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink1 = proc1['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink11 = proc1['blink']   # List.
blink21 = np.array(blink1).T # Creates transpose matrix of blink. Necessary for plotting.


#---calculate number of frames, frame rate, and time vector---
nframes1 = len(pArea1) # Contains length of pArea variable (equivalent to the blink variable).
frameVec1 = np.arange(0, nframes1, 1) # Vector of the total frames from the video.
framerate1 = 30 # frame rate of video
timeVec1 = (frameVec1 * 1)/framerate1 # Time Vector to calculate the length of the video.

'''
with np.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(blink)
'''

#---obtain values where sync signal is on---
blink2Bool1 = np.logical_and(blink21>20000, blink21<55000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues1 = np.diff(blink2Bool1) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal1 = np.flatnonzero(blink2RangeValues1) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

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

syncOnsetValues1 = onset_values(indicesValueSyncSignal1, 2)
timeOfBlink2Event1 = timeVec1[syncOnsetValues1] # Provides the time values in which the sync signal is on.

timeRange1 = np.array([-0.67, 0.67]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]

samplingRate1 = 1/(timeVec[1]-timeVec[0])
windowSampleRange1 = samplingRate*np.array(timeRange1) 
windowSampleVec1 = np.arange(*windowSampleRange1, dtype=int)
windowTimeVec1 = windowSampleVec1/samplingRate1
nSamples1 = len(windowTimeVec1)
nTrials1 = len(timeOfBlink2Event1)

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

windowTimeVec1, windowed_signal1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRange1)



#--check if the number of samples and trials are correct---
print()
print('this are the total values on/off from signal:',len(indicesValueSyncSignal1))
print('you must obtain half of it, due you need only the onset values:',len(syncOnsetValues1))
print('to know what are the size of the slices, figure out which index is 0 in windowSampleVec variable:',windowSampleVec1)
print()



#---obtain mean trial values pre and post signal, plot slope plot---
preSignal1 = windowed_signal1[0:20] # Takes the values of the pArea between timeRange within the time window. [0:28] for experimental and [0:18] for controls
postSignal1 = windowed_signal1[20:41] # Takes the values of the pArea between timeRange within the time window. [28:57] for experimental and [18:36] for controls
averagePreSignal1 = preSignal1.mean(axis = 0)
averagePostSignal1 = postSignal1.mean(axis = 0)
dataToPlot1 = [averagePreSignal1, averagePostSignal1]
xlabels1 = ['Pre signal', 'Post signal']

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
     trials.set_xlabel('Conditions') 
     trials.set(title = 'Average trials signals', ylabel = 'Mean Pupil Area')
     plt.ylim(100, 1500) 
     plt.show() 
     return(plt.show())

prePostSignalpArea1 = scatter_plotting(averagePreSignal1, averagePostSignal1)


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
     barPlots.set_xlabel('Conditions')
     barPlots.set(title = 'Pupil Area before and after stimulus', ylabel = 'Mean Pupil Area')
     plt.ylim(40, 800) 
     plt.show() 
     return(plt.show())

barPlotting1 = bar_plotting(averagePreSignal1, averagePostSignal1, 'pre sync signal onset', 'post sync signal onset', preSignal1, postSignal1)

#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation1 = np.array([-2, 2])
pupilDilationTimeWindowVec1, pAreaDilated1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRangeForPupilDilation1)

pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)

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
 signalsPlots.set(title = 'Averaged trials in time window', ylabel = 'Pupil area', xlabel = 'Time(s)')
 #plt.ylim(150, 800)
 plt.show()
 return(plt.show())

trialsWindow1 = pupilDilation_time(pupilDilationTimeWindowVec1, pAreaDilatedMean1)

#--- Wilcoxon test to obtain statistics ---
wstat1, pval1 = stats.wilcoxon(averagePreSignal1, averagePostSignal1)
print('Wilcoxon value:', wstat1,',',  'P-value:', pval1 )

#--- Plotting Two plots ---
def two_plots(timeData1, valuesData1, timeData2, valuesData2): 
     ''' 
     Create 2 plots in 1 figure. 
     Args: 
     timeData1 = time vector for plotting first plot 
     valuesData1 = data/values vector for plotting first plot 
     timeData2 = time vector for plotting second plot 
     valuesData2 = data/values vector for plotting second plot 
     returns: 
     plt.show() = plots data provided in the aforementioned variables 
     ''' 
     fig, (plotData1, plotData2) = plt.subplots(2, 1, sharey = True, constrained_layout = True) 
     plotData1.plot(timeData1, valuesData1) 
     plotData1.set(title = 'Averaged trials in time window (negative control)', ylabel = 'Pupil area') 
     plotData2.plot(timeData2, valuesData2) 
     plotData2.set(title = 'Averaged trials in time window (positive control)', xlabel = 'Time (s)') 
     plt.show() 
     return(plt.show())
     
#controlsComparison = two_plots(pupilDilationTimeWindowVec1, pAreaDilatedMean1, pupilDilationTimeWindowVec, pAreaDilatedMean)

def two_plots_oneFig(time, valuesData1, valuesData2): 
     ''' 
     Creates 2 plots in 1 figure 
     Args: 
     time = vector values for x axis 
     valuesData1 = vector values for y axis of the first plot 
     valuesData2 = vector values for y axis of the second plot 
     returns: 
     plt.show() = 1 figure with 2 plots using the input data 
     ''' 
     plt.plot(time, valuesData1, color = 'r', label = 'negative control') 
     plt.plot(time, valuesData2, color = 'g', label = 'positive control') 
     plt.xlabel('Time (s)') 
     plt.ylabel('Pupil Area') 
     plt.title('Averaged trials in time window') 
     plt.legend() 
     plt.show() 
     return(plt.show())                                                                                      

overLapPlots = two_plots_oneFig(pupilDilationTimeWindowVec, pAreaDilatedMean1, pAreaDilatedMean)

