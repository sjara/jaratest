import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from jaratoolbox import loadbehavior
import os
import facemapanalysis as fmap
import sys

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
    if (eventOnsetTimes[0] + windowTimeRange[0]) < timeVec[0]:
        raise ValueError('Your first window falls outside the recorded data.')
    if (eventOnsetTimes[-1] + windowTimeRange[-1]) > timeVec[-1]:
        raise ValueError('Your last window falls outside the recorded data.')
    samplingRate = 1/(timeVec[1]-timeVec[0])
    windowSampleRange = samplingRate*np.array(windowTimeRange)  # units: frames
    windowSampleVec = np.arange(*windowSampleRange, dtype=int) # units: frames
    windowTimeVec = windowSampleVec/samplingRate # Units: time
    nSamples = len(windowTimeVec) # time samples / trial
    nTrials = len(eventOnsetTimes) # number of times the sync light went off
    lockedSignal = np.empty((nSamples,nTrials))
    for inde,eventTime in enumerate(eventOnsetTimes):
       eventSample = np.searchsorted(timeVec, eventTime) # eventSample = index at which the synch turns on
       thiswin = windowSampleVec + eventSample # indexes of window
       lockedSignal[:,inde] = signal[thiswin]
    return (windowTimeVec, lockedSignal)


def find_valid_windows(timeVec, eventOnsetTimes, windowTimeRange):
    """
    Find windows that lie within the timeVec.
    Args:
        timeVec (np.array): time of each sample in the signal.
        eventOnsetTimes (np.array): time of each event.
        windowTimeRange (list or np.array): 2-element array defining range of window to extract.
    Returns: 
        validWindows (np.array): array of booleans that is True if the window falls within.

    """
    return (validWindows)



def eventlocked_signalold(timeVec, signal, eventOnsetTimes, windowTimeRange):
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
    windowSampleRange = samplingRate*np.array(windowTimeRange)  # units: frames
    windowSampleVec = np.arange(*windowSampleRange, dtype=int) # units: frames
    windowTimeVec = windowSampleVec/samplingRate # Units: time
    nSamples = len(windowTimeVec) # time samples / trial
    nTrials = len(eventOnsetTimes) # number of times the sync light went off
    lockedSignal = np.empty((nSamples,nTrials))
    discards = []                                                           #DB ADDED
    for inde,eventTime in enumerate(eventOnsetTimes):
       eventSample = np.searchsorted(timeVec, eventTime) # eventSample = index at which the synch turns on
       thiswin = windowSampleVec + eventSample # indexes of window
       if np.logical_and(np.min(thiswin) > 0, np.max(thiswin) < len(signal)): # DB ADDED
           lockedSignal[:,inde] = signal[thiswin]                           # DB ADDED
       else:                                                                # DB ADDED
           discards.append(inde)                                            # DB ADDED
    lockedSignal_trim = np.delete(lockedSignal,discards,1)                  # DB ADDED
    return (windowTimeVec, lockedSignal_trim)
    
def find_prepost_values(timeArray, dataArray, preLimDown, preLimUp, postLimDown, postLimUp): 
  
      '''  
      Obtain pupil data before and after stimulus  
      Args:  
      timeArray (np.array): array of the time window to evaluate pupil area obtained from event_locked  
      dataArray (np.array): array of the pupil data obtained from event_locked function  
      preLimDown (int or float): first number of the time interval to evaluate before stimulus onset  
      preLimUp (int or float): second number of the time interval to evaluate before stimulus onset
      postLimDown (int or float): first number of the time interval to evaluate after stimulus onset  
      postLimUp (int or float): second number of the time interval to evaluate after stimulus onset 
      Returns: 
      preData (np.array): array with the pupil data before stimulus 
      postData (np.array): array with the pupil data after stimulus    
      '''   
      preBool = np.logical_and(preLimDown <= timeArray, timeArray < preLimUp) 
      postBool = np.logical_and(postLimDown <= timeArray, timeArray < postLimUp) 
      preValuesIndices = np.argwhere(preBool == True)  
      postValuesIndices = np.argwhere(postBool == True)  
      preProcessedPreValues = dataArray[preValuesIndices]  
      preProcessedPostValues = dataArray[postValuesIndices]  
      preData = preProcessedPreValues.reshape(preValuesIndices.shape[0], dataArray.shape[1]) 
      postData = preProcessedPostValues.reshape(postValuesIndices.shape[0], dataArray.shape[1])  
      return(preData, postData)

def freqs_and_meanParea(freqsArray, meanPareaVariable, freq1, freq2, freq3, freq4, freq5):      
      '''
      Creates arrays containing the pupil area for each tested frequency
      Args:
      freqsArray (np.array): array containing the tested frequencies
      meanPareaVariable (np.array): array containing the average pupil size
      freq1..5 (int): frequencies tested
      
      returns:
      arrValues1..5 (np.array): one array per frequency tested (freq1..5) that contains the pupil size for the given frequency
      '''
      
      indicesFreq1 = np.argwhere(freq1 == freqsArray)  
      indicesFreq2 = np.argwhere(freq2 == freqsArray)
      indicesFreq3 = np.argwhere(freq3 == freqsArray)  
      indicesFreq4 = np.argwhere(freq4 == freqsArray)  
      indicesFreq5 = np.argwhere(freq5 == freqsArray)  
      newIndexArr1 = np.take(meanPareaVariable, indicesFreq1)  
      newIndexArr2 = np.take(meanPareaVariable, indicesFreq2)  
      newIndexArr3 = np.take(meanPareaVariable, indicesFreq3)  
      newIndexArr4 = np.take(meanPareaVariable, indicesFreq4)  
      newIndexArr5 = np.take(meanPareaVariable, indicesFreq5)
      arrValues1 = newIndexArr1.flatten()
      arrValues2 = newIndexArr2.flatten()   
      arrValues3 = newIndexArr3.flatten() 
      arrValues4 = newIndexArr4.flatten()   
      arrValues5 = newIndexArr5.flatten()
      return(arrValues1, arrValues2, arrValues3, arrValues4, arrValues5)


def normalize_data(pupilArea, valuesToNormalize): 
     minVal = np.amin(pupilArea) 
     maxVal = np.amax(pupilArea) 
     rangeValues = maxVal - minVal 
     listData = [] 
     for i in valuesToNormalize: 
         substractMin = i - minVal 
         newData = substractMin/rangeValues
         listData.append(newData) 
         normalizedData = np.asarray(listData) 
     return(normalizedData)

     
def comparison_plot(time, valuesData1, pVal): 
     ''' 
     Creates 1 figure with 3 plots 
     Args: 
     time = vector values for x axis 
     valuesData1 (np.array) = vector values for y axis of the first plot 
     valuesData2 (np.array)= vector values for y axis of the second plot
     valuesData3 (np.array)= vector values for y axis of the third plot
     returns: 
     plt.show() = 1 figure with 3 plots using the input data 
     ''' 
     labelsSize = 16
     fig, subplt = plt.subplots(1,1)
     fig.set_size_inches(9.5, 7.5, forward = True)
     sp = np.round(pVal, decimals=17)
     label1 = filename,'pval:',sp
     
     subplt.plot(time, valuesData1, color = 'g', label = label1, linewidth = 4)

     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     subplt.set_title('Pupil behavior: ' + filename, fontsize = labelsSize)
     plt.suptitle('Mouse = pure013.  Data Collected 2022-07-01.', fontsize = labelsSize)
     plt.grid(b = True)
     #plt.ylim([550, 650])
     plt.xticks(fontsize = labelsSize)
     plt.yticks(fontsize = labelsSize)
#     plt.legend()
     #plt.legend(prop ={"size":10}, bbox_to_anchor=(1.0, 0.8))
     #plt.savefig('comparisonPure004Plot', format = 'pdf', dpi = 50)
     plt.show() 
     return(plt.show())
     
def barScat_plots(firstPlotMeanValues1, firstPlotMeanValues2, xlabel1, xlabel2, firstPlotStdData1, firstPlotStdData2, pVal):
     '''
     Plot bar plots
     Args:
     MeanValues (int or float): number representing the average of the data to plot
     xlabel1 (string): name of the first condition to compare
     xlabel2 (string): name of the second condition to compare
     StdData (np.array): values to calculate the standard deviation from
     pVal (float or int): p-value for each one of the animals
     Returns:
     plt.show(): three bar plots within one figure
     '''
     barLabelsFontSize = 14
     meanPreSignal1 = firstPlotMeanValues1.mean(axis = 0) 
     meanPostSignal1 = firstPlotMeanValues2.mean(axis = 0)
     preSignalStd1 = np.std(firstPlotStdData1) 
     postSignalStd1 = np.std(firstPlotStdData2) 
     barMeanValues1 = [meanPreSignal1, meanPostSignal1] 
     stdErrors1 = [preSignalStd1, postSignalStd1] 
     shortPval1 = np.round(pVal, decimals=3)
     pValue1 = 'P-value:', shortPval1
     dataPlot1 = [firstPlotMeanValues1, firstPlotMeanValues2] 
    
     fig, barPlots = plt.subplots(1,1, constrained_layout = True, sharex = True, sharey = True)
     fig.set_size_inches(9.5, 7.5) 
     barPlots.bar(xlabels, barMeanValues1, yerr = stdErrors1, color = 'g', label = pValue1) 
     barPlots.errorbar(xlabels, barMeanValues1, yerr = stdErrors1, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots.set_title(filename, fontsize = barLabelsFontSize)
     barPlots.set_ylabel('Pupil area', fontsize = barLabelsFontSize)
     barPlots.tick_params(axis='x', labelsize=barLabelsFontSize)
     #plotcolors = firstPlotMeanValues1 - firstPlotMeanValues2
     barPlots.plot(xlabels, dataPlot1, marker = 'o', c = 'k', alpha = 0.3, linewidth = 1)
     barPlots.legend(prop ={"size":10})
     
     #plt.ylim(250, 800)
     plt.suptitle('pupil behavior across trials', fontsize = barLabelsFontSize)
     #plt.xlabel("common X", loc = 'center')
     #plt.savefig(scatBarDict['savedName'], format = 'pdf', dpi =50)
     plt.show() 
     return(plt.show())
      
def pupilDilation_time(timeData1, plotData1, pvalue):
     shortPval = np.round(pvalue, decimals = 6)
     lab = 'p-value', shortPval 
     plt.plot(timeData1,plotData1, label = lab)
     plt.title('pure004_20220110_2Sounds: average pupil behavior') 
     plt.ylabel('Pupil Area', fontsize = 13)
     plt.xlabel('Time(s)', fontsize = 13)
     plt.legend()
     plt.show() 
     return(plt.show())

def PDR_kHz_plot(freqsArray, arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5):
     labelsSize = 16
     fig, freqplt = plt.subplots(1, 1)
     fig.set_size_inches(9.5, 7.5, forward = True)
     label1 = filename
     
     meanPoint1 = arrFreq1.mean(axis = 0)
     meanPoint2 = arrFreq2.mean(axis = 0)     
     meanPoint3 = arrFreq3.mean(axis = 0)     
     meanPoint4 = arrFreq4.mean(axis = 0)     
     meanPoint5 = arrFreq5.mean(axis = 0)     
     valuesPlot = [meanPoint1, meanPoint2, meanPoint3, meanPoint4, meanPoint5]
     
     freqplt.plot(freqsArray, valuesPlot, marker = 'o')
     freqplt.set_title('Pupil size for 5 different frequencies: pure011_20220331', fontsize = labelsSize)
     freqplt.set_ylabel('Mean pupil Area', fontsize = labelsSize)
     freqplt.set_xlabel('Frequencies (kHz)', fontsize = labelsSize)
     plt.grid(b = True)
     plt.xticks(fontsize = labelsSize)
     plt.yticks(fontsize = labelsSize)
     plt.show() 
     return(plt.show())
# ---------------------------------------------------------------------------------------------------------------
     
   
     
#--- loading data ---
fileloc = '/home/jarauser/Desktop/danny_datacollection/dbtest3_pure013_2022-07-01'
filename = 'pure013_detectiongonogo_20220701a_dbtest3_proc.npy'
proc = fmap.load_data(os.path.join(fileloc, filename), runchecks=False)

#--- obtain pupil data ---
pArea = fmap.extract_pupil(proc)

#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Number of frames.
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = frameVec / framerate # Time Vector to calculate the length of the video.

#--- obtain values where sync signal turns on ---
_, syncOnsetValues, _, _ = fmap.extract_sync(proc)
timeOfSyncOnset = timeVec[syncOnsetValues] # Provides the time values in which the sync signal turns on.

#--- Align trials to the event ---
timeRange = np.array([-0.5, 2.0]) # Range of time window
# run function you're creating, to restrict trials to valid trials: timeofSyncOnset[bool] 
windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfSyncOnset, timeRange)


# TO SHOW SANTIAGO:
print('time of last sync light:')
print(timeOfSyncOnset[-1])
print('total time of recording:')
print(np.max(timeVec))
print('total number of sounds played (times sync light blinked):')
print(syncOnsetValues.shape)
print('total number of trials included in the analysis:')
print(windowed_signal.shape[1])


#sys.exit()  

#--- Obtain pupil pre and post stimulus values, and average size ---
#find_prepost_values(timeArray, dataArray, preLimDown, preLimUp, postLimDown, postLimUp)
preSignal, postSignal = find_prepost_values(windowTimeVec, windowed_signal, -0.5, 0, 1.4, 2.0)
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']

#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value config14_1', wstat,',',  'P-value config14_1', pval)

#--- Defining the correct time range for pupil's relaxation (dilation) ---  DB: SEEMS TO BE FOR PLOTTING, MAYBE WE SHOULD RENAME.
timeRangeForPupilDilation = np.array([-12, 12])
#def eventlocked_signal(timeVec, signal, eventOnsetTimes, windowTimeRange)
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfSyncOnset, timeRangeForPupilDilation)
pAreaDilatedMean = pAreaDilated.mean(axis = 1)

#--- Plotting the results ---
OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean, pval)
scattBar = barScat_plots(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal,  pval)

#--- Finding and plotting pupil area corresponding to each tested frequency ---
#freqValues1, freqValues2, freqValues3, freqValues4, freqValues5 = freqs_and_meanParea(freqs, averagePostSignal, 2000, 4000, 8000, 16000, 32000) 
#pAreaFreqPlot = PDR_kHz_plot(frequenciesTested, freqValues1, freqValues2, freqValues3, freqValues4, freqValues5)

print('Data averaged over ', pAreaDilated.shape[1], ' trials')




