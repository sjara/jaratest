import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#README: Lines to change for each video: 11, 35, 61, 111, and 112

proc = np.load('./project_videos/projectOutputs/pure001_20210928_syncVisibleNoSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data---
pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.


#LargeNumbersIndeces = np.where(blink2 == np.amax(blink2))
#newpArea = np.delete(pArea, LargeNumbersIndeces)
#newBlink = np.delete(blink2,LargeNumbersIndeces)

#---obtain values where sync signal is on---
blink2Bool = np.logical_and(blink2>20000, blink2<60000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#newpArea = pArea[blink2 != np.amax(blink2)]
#newBlink = blink2[blink2 != np.amax(blink2)] 
#correctedpArea = pArea[blink2Bool] 
#correctedBlink = blink2[blink2Bool] #Trims weird values from variable ((elim. Largest elements)


#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
#newFrame = frameVec[blink2Bool]
#newFrame = frameVec[blink2 != np.amax(blink2)]
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video.


'''
with np.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(blink)
'''


def onset_values(signalArray): 

     '''
     Helps to find onset start values of the sync singal in any given array: 
     Args: 
     array = array that contains data of the sync signal
     Returns:
     startValuesVec = an array of the indices containing the start onset values of the sync signal.
    ''' 
     firstIndexValue = 0 
     lastIndexValue = len(signalArray)-1 
     stepNumber = 2
     startIndicesValues = range(firstIndexValue, lastIndexValue, stepNumber)
     startIndicesVec = np.array(startIndicesValues)
     onsetStartValues = np.take(signalArray, startIndicesVec)
     return (onsetStartValues)

syncOnsetValues = onset_values(indicesValueSyncSignal)
#syncOnsetIndices = range(0, len(syncOnsetValues),1)
#syncOnsetVec = np.array(syncOnsetIndices)
#timeBlink = timeVec[syncOnsetVec]
timeOfBlink2Event = timeVec[syncOnsetValues] # Provides the time values in which the sync signal is on.

timeRange = np.array([-0.5, 0.5])

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

windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)

maxValuesIndices = np.where(windowed_signal == np.amax(windowed_signal)) #Finds the indices of the max value in the windowed_trials array
correctedWindowedSignal = np.delete(windowed_signal, maxValuesIndices, axis = 1) #Eliminates the max value in each column(trial) in the array provided.


def signalsPlot(xValues,yValues):
    '''
    Plots trials in a given time window
    args:
    xValues(numpy.array): values to be plotted in the x Axis of the plot
    yValues(numpy.array): valus to be plotted in the y Axis of the plot
    returns:
    plt.show(): plot with the trials in a given time window
    ''' 
    plt.plot(xValues,yValues)
    plt.title('Trials signals: Pure001, positive control')
    plt.xlabel('Time Window')
    plt.ylabel('Pupil Area') 
    plt.show()
    return(plt.show()) 

windowedSignalPlot = signalsPlot(windowTimeVec, correctedWindowedSignal)

#---obtain mean trial values pre and post signal, plot slope plot---
preSignal = correctedWindowedSignal[0:15] # Takes the values of the pArea between timeRange within the time window. [0:28] for experimental and [0:18] for controls
postSignal = correctedWindowedSignal[15:30] # Takes the values of the pArea between timeRange within the time window. [28:57] for experimental and [18:36] for controls
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']

def scatter_plotting(preArray, postArray):
     '''
     Shows how to plot 2 conditions regarding a stimulus
     Args:
     preArray = data array before stimulus
     postArray = data array after stimulus
     returns:
     plt.show() = slope plot with both defined conditions and the data corresponding to each condition
     ''' 
     xLabelsToPlot = ['Pre stimulus onset', 'Post stimulus onset'] 
     dataToPlot = [preArray, postArray] 
     fig, trials = plt.subplots(1,1) 
     trials.plot(xLabelsToPlot, dataToPlot, marker = 'o', linewidth=1)
     trials.set_xlabel('Conditions') 
     trials.set(title = 'Average trials signals behavior during session 01: positive control', ylabel = 'Mean Pupil Area')
     #plt.ylim(100, 1500) 
     plt.show() 
     return(plt.show())

prePostSignalpArea = scatter_plotting(averagePreSignal, averagePostSignal)

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
     barPlots.set(title = 'Pupil behavior before and after stimulus: positive control', ylabel = 'Mean Pupil Area')
     plt.ylim(40, 800) 
     plt.show() 
     return(plt.show())

barPlotting = bar_plotting(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal)

timeRangeForPupilDilation = np.array([-2, 2])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)

pAreaDilatedMean = pAreaDilated.mean(axis = 1)

def pupilDilation_time(time, data):
 '''
 Create a time window to identify the pupil's dilation time range
 Args:
 time: time window vector to be used for the plot
 data: mean value vector of the trials
 Returns:
 plt.show(): plot with all of the trials in the selected time window
 '''
 fig, signalsPlots = plt.subplots()
 signalsPlots.plot(time, data)
 signalsPlots.set(title = 'Average trials behavior in time window: positive control', ylabel = 'Pupil area', xlabel = 'Time(s)')
 #plt.ylim(150, 800)
 plt.show()
 return(plt.show())

trialsWindow = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean)

#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value:', wstat,',',  'P-value:', pval )
