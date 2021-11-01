'''
This script is for the project of pupil dilation. It is intended to obtain pupil data, its mean, the desired time windows, create a slope and bar plots
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def onset_values(signalArray): 

     '''
     Helps to find onset start values of the sync singal in any given array: 
     Args: 
     SignalArray (np.array) = array that contains data of the sync signal
     Returns:
     onsetStartValues (np.array)  = an array of the indices containing the start onset values of the sync signal.
    ''' 
     firstIndexValue = 0 
     lastIndexValue = len(signalArray)-1 
     stepNumber = 2
     startIndicesValues = range(firstIndexValue, lastIndexValue, stepNumber)
     startIndicesVec = np.array(startIndicesValues)
     onsetStartValues = np.take(signalArray, startIndicesVec)
     return (onsetStartValues)

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
       #print(thiswin.shape, eventSample.shape)
       lockedSignal[:,inde] = signal[thiswin]
    return (windowTimeVec, lockedSignal)

def comparison_plot(time, valuesData1, valuesData2, valuesData3): 
     ''' 
     Creates 1 figure with 3 plots 
     Args: 
     time = vector values for x axis 
     valuesData1 = vector values for y axis of the first plot 
     valuesData2 = vector values for y axis of the second plot
     valuesData3 = vector values for y axis of the third plot
     returns: 
     plt.show() = 1 figure with 3 plots using the input data 
     ''' 
     plt.plot(time, valuesData1, color = 'g', label = 'positive control')
     plt.plot(time, valuesData2, color = 'r', label = 'negative control')
     plt.plot(time, valuesData3, color = 'b', label = 'chordTrain data') 
     plt.xlabel('Time (s)') 
     plt.ylabel('Pupil Area') 
     plt.title('Comparison of pupil behavior in different conditions: pure002_20210928_01')
     plt.grid(b = True)
     plt.ylim([300, 800]) 
     plt.legend()
     plt.show() 
     return(plt.show())

def scatter_plots(preValues1, postValues1, preValues2, postValues2, preValues3, postValues3):
     '''
     Create 3 scatter plots within one figure
     Args:
     preValues (np.array): trials values before stimulus onset
     postValues (np.array): trials values after stimulus onset
     Returns:
     plt.show(): one figure with 3 scatter plots.
     '''
     xLabelling = ['Pre stimulus onset', 'Post stimulus onset'] 
     dataToPlot1 = [preValues1, postValues1] 
     dataToPlot2 = [preValues2, postValues2] 
     dataToPlot3 = [preValues3, postValues3]  
     fig, scatterPlots = plt.subplots(1,3, constrained_layout = True, sharex = True, sharey = True) 
     scatterPlots[0].plot(xLabelling, dataToPlot1, marker = 'o', linewidth = 1) 
     scatterPlots[0].set(title = 'Condition: Positive Control', ylabel = 'Mean Pupil Area') 
     scatterPlots[1].plot(xLabelling, dataToPlot2, marker = 'o', linewidth = 1) 
     scatterPlots[1].set(title = 'Condition: Negative Control') 
     scatterPlots[2].plot(xLabelling, dataToPlot3, marker = 'o', linewidth = 1) 
     scatterPlots[2].set(title = 'Condition: chordTrain')
     plt.suptitle('Average trials signals behavior during session 01: pure002_20210928')
     plt.show() 
     return(plt.show())

def bar_plots(firstPlotMeanValues1, firstPlotMeanValues2, xlabel1, xlabel2, firstPlotStdData1, firstPlotStdData2, secondPlotMeanValues1, secondPlotMeanValues2, secondPlotStdData1, secondPlotStdData2, thirdPlotMeanValues1, thirdPlotMeanValues2, thirdPlotStdData1, thirdPlotStdData2):
     '''
     Plot bar plots
     Args:
     MeanValues (int or float): number representing the average of the data to plot
     xlabel1 (string): name of the first condition to compare
     xlabel2 (string): name of the second condition to compare
     StdData (np.array): values to calculate the standard deviation from
     Returns:
     plt.show(): three bar plots within one figure
     '''
     meanPreSignal1 = firstPlotMeanValues1.mean(axis = 0) 
     meanPostSignal1 = firstPlotMeanValues2.mean(axis = 0) 
     meanPreSignal2 = secondPlotMeanValues1.mean(axis = 0) 
     meanPostSignal2 = secondPlotMeanValues2.mean(axis = 0) 
     meanPreSignal3 = thirdPlotMeanValues1.mean(axis = 0) 
     meanPostSignal3 = thirdPlotMeanValues2.mean(axis = 0) 
     preSignalStd1 = np.std(firstPlotStdData1) 
     postSignalStd1 = np.std(firstPlotStdData2) 
     preSignalStd2 = np.std(secondPlotStdData1) 
     postSignalStd2 = np.std(secondPlotStdData2) 
     preSignalStd3 = np.std(thirdPlotStdData1) 
     postSignalStd3 = np.std(thirdPlotStdData2) 
     barMeanValues1 = [meanPreSignal1, meanPostSignal1] 
     barMeanValues2 = [meanPreSignal2, meanPostSignal2] 
     barMeanValues3 = [meanPreSignal3, meanPostSignal3] 
     stdErrors1 = [preSignalStd1, postSignalStd1] 
     stdErrors2 = [preSignalStd2, postSignalStd2] 
     stdErrors3 = [preSignalStd3, postSignalStd3] 
     fig, barPlots = plt.subplots(1,3, constrained_layout = True, sharex = True, sharey = True) 
     barPlots[0].bar(xlabels, barMeanValues1, yerr = stdErrors1) 
     barPlots[0].errorbar(xlabels, barMeanValues1, yerr = stdErrors1, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[0].set(title = 'Positive control data', ylabel = 'Mean Pupil Area') 
     barPlots[1].bar(xlabels, barMeanValues2, yerr = stdErrors2) 
     barPlots[1].errorbar(xlabels, barMeanValues2, yerr = stdErrors2, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[1].set(title = 'Negative control data')
     barPlots[1].set_xlabel('Conditions')
     barPlots[2].bar(xlabels, barMeanValues3, yerr = stdErrors3) 
     barPlots[2].errorbar(xlabels, barMeanValues3, yerr = stdErrors3, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[2].set(title = 'chordTrain data')  
     plt.ylim(200, 700)
     plt.suptitle('Pupil behavior before and after stimulus: pure002_20210928')
     plt.show() 
     return(plt.show())

def  pupilDilation_time(timeData1, plotData1, timeData2, plotData2, timeData3, plotData3): 
     fig, signalsPlots = plt.subplots(1,3, constrained_layout = True, sharey = True, sharex = True) 
     signalsPlots[0].plot(timeData1, plotData1) 
     signalsPlots[0].set(title = 'Positive control', ylabel = 'Pupil Area',) 
     signalsPlots[1].plot(timeData2, plotData2) 
     signalsPlots[1].set(title = 'Negative control', xlabel = 'Time(s)') 
     signalsPlots[2].plot(timeData3, plotData3) 
     signalsPlots[2].set(title = 'chordTrain')
     plt.suptitle('Average trials behavior in time window: pure002_20210928')
     plt.show() 
     return(plt.show()) 

proc = np.load('./project_videos/mp4Files/mp4Outputs/pure002_20210928_syncVisibleNoSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data---
pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
blink2Bool = np.logical_and(blink2>20000, blink2<60000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.


#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
#newFrame = frameVec[blink2Bool]
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video.

#--- obtaining onset sync signal values ---
syncOnsetValues = onset_values(indicesValueSyncSignal)
timeOfBlink2Event = timeVec[syncOnsetValues] # Provides the time values in which the sync signal is on.
timeOfBlink2Event = timeOfBlink2Event[1:-1]

#--- Align trials to the event ---
timeRange = np.array([-0.8, 0.8]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)
preSignal = windowed_signal[0:24] # Takes the values of the pArea between timeRange within the time window. [0:28] for experimental and [0:18] for controls
postSignal = windowed_signal[24:48] # Takes the values of the pArea between timeRange within the time window. [28:57] for experimental and [18:36] for controls
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']

#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([-6, 6])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)
pAreaDilatedMean = pAreaDilated.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value positive control:', wstat,',',  'P-value positive control:', pval )


















proc1 = np.load('./project_videos/mp4Files/mp4Outputs/pure002_20210928_syncNoSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data---
pupil1 = proc1['pupil'][0] # Dic.
pArea1 = pupil1['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink1 = proc1['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink11 = proc1['blink']   # List.
blink21 = np.array(blink1).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
blink2Bool1 = np.logical_and(blink21>20000, blink21<60000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues1 = np.diff(blink2Bool1) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal1 = np.flatnonzero(blink2RangeValues1) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#---calculate number of frames, frame rate, and time vector---
nframes1 = len(pArea1) # Contains length of pArea variable (equivalent to the blink variable).
frameVec1 = np.arange(0, nframes1, 1) # Vector of the total frames from the video.
framerate1 = 30 # frame rate of video
timeVec1 = (frameVec1 * 1)/framerate1 # Time Vector to calculate the length of the video.

#--- obtaining onset sync signal values ---
syncOnsetValues1 = onset_values(indicesValueSyncSignal1)
timeOfBlink2Event1 = timeVec1[syncOnsetValues1] # Provides the time values in which the sync signal is on.
timeOfBlink2Event1 = timeOfBlink2Event1[1:-1]

#--- Align trials to the event ---
timeRange1 = np.array([-0.25, 0.25]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec1, windowed_signal1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRange1)
preSignal1 = windowed_signal1[0:7] # Takes the values of the pArea between timeRange within the time window. [0:28] for experimental and [0:18] for controls
postSignal1 = windowed_signal1[7:15] # Takes the values of the pArea between timeRange within the time window. [28:57] for experimental and [18:36] for controls
averagePreSignal1 = preSignal1.mean(axis = 0)
averagePostSignal1 = postSignal1.mean(axis = 0)
dataToPlot1 = [averagePreSignal1, averagePostSignal1]
xlabels1 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation1 = np.array([-6, 6])
pupilDilationTimeWindowVec1, pAreaDilated1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRangeForPupilDilation1)
pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat1, pval1 = stats.wilcoxon(averagePreSignal1, averagePostSignal1)
print('Wilcoxon value negative control:', wstat1,',',  'P-value negative control:', pval1 )

















proc2 = np.load('./project_videos/mp4Files/mp4Outputs/pure002_20210928_syncSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data---
pupil2 = proc2['pupil'][0] # Dic.
pArea2 = pupil2['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink2 = proc2['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink12 = proc2['blink']   # List.
blink22 = np.array(blink2).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
blink2Bool2 = np.logical_and(blink22>20000, blink22<60000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues2 = np.diff(blink2Bool2) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal2 = np.flatnonzero(blink2RangeValues2) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#---calculate number of frames, frame rate, and time vector---
nframes2 = len(pArea2) # Contains length of pArea variable (equivalent to the blink variable).
frameVec2 = np.arange(0, nframes2, 1) # Vector of the total frames from the video.
framerate2 = 30 # frame rate of video
timeVec2 = (frameVec2 * 1)/framerate2 # Time Vector to calculate the length of the video.

#--- obtaining onset sync signal values ---
syncOnsetValues2 = onset_values(indicesValueSyncSignal2)
timeOfBlink2Event2 = timeVec2[syncOnsetValues2] # Provides the time values in which the sync signal is on.
timeOfBlink2Event2 = timeOfBlink2Event2[1:-1]

#--- Align trials to the event ---
timeRange2 = np.array([-0.43, 0.43]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec2, windowed_signal2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRange2)
preSignal2 = windowed_signal2[0:12] # Takes the values of the pArea between timeRange within the time window. [0:28] for experimental and [0:18] for controls
postSignal2 = windowed_signal2[12:26] # Takes the values of the pArea between timeRange within the time window. [28:57] for experimental and [18:36] for controls
averagePreSignal2 = preSignal2.mean(axis = 0)
averagePostSignal2 = postSignal2.mean(axis = 0)
dataToPlot2 = [averagePreSignal2, averagePostSignal2]
xlabels2 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation2 = np.array([-6, 6])
pupilDilationTimeWindowVec2, pAreaDilated2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRangeForPupilDilation2)
pAreaDilatedMean2 = pAreaDilated2.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat2, pval2 = stats.wilcoxon(averagePreSignal2, averagePostSignal2)
print('Wilcoxon value chordTrain:', wstat2,',',  'P-value chordTrain:', pval2 )

                                                                
#--- plot with the three conditions aligned ---
OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean,  pAreaDilatedMean1, pAreaDilatedMean2)


#--- Figure with 3 scatter plots ---
scatterPlots = scatter_plots(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2)

#--- Figure with 3 bar plots ---
barPlots = bar_plots(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal, averagePreSignal1, averagePostSignal1, preSignal1, postSignal2, averagePreSignal2, averagePostSignal2, preSignal2, postSignal2)

#--- Pupil Dilation plots ---
pupilDilationPlots = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean, pupilDilationTimeWindowVec1, pAreaDilatedMean1, pupilDilationTimeWindowVec2, pAreaDilatedMean2)
