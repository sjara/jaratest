'''
This script is for the project of pupil dilation. It is intended to obtain pupil data, its mean the desired time windows, create a slope and bar plots
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from jaratoolbox.jaratoolbox import loadbehavior


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
    
def find_prepost_values(timeArray, dataArray, preLimDown, preLimUp, postLimDown, postLimUp): 
  
      '''  
      Obtain pupil data before and after stimulus  
      Args:  
      timeArray (np.array): array of the time window to evaluate pupil area obtained from even  t_locked  
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
      Creates arrays containing the pupil area for each tested frequency. Am_tuning_curve paradigm
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
      
def freqs_gonogo(freqsArr, indicesArr, freq1, freq2, freq3, freq4, freq5):      
      '''
      Creates arrays containing the pupil area for each tested frequency. Detectiongonogo paradigm
      Args:
      freqsArray (np.array): array containing the tested frequencies
      meanPareaVariable (np.array): array containing the average pupil size
      freq1 and freq2 (int): frequencies tested
      
      returns:
      arrValues1..5 (np.array): one array per frequency tested (freq1..5) that contains the pupil size for the given frequency
      '''
      indicesFreq1 = np.argwhere(freq1 == indicesArr)  
      indicesFreq2 = np.argwhere(freq2 == indicesArr)
      indicesFreq3 = np.argwhere(freq3 == indicesArr)  
      indicesFreq4 = np.argwhere(freq4 == indicesArr)  
      indicesFreq5 = np.argwhere(freq5 == indicesArr)
      arrValues1 = indicesFreq1.flatten()
      arrValues2 = indicesFreq2.flatten()   
      arrValues3 = indicesFreq3.flatten() 
      arrValues4 = indicesFreq4.flatten()   
      arrValues5 = indicesFreq5.flatten()
      newVal1 = np.take(freqsArr, arrValues1)
      newVal2 = np.take(freqsArr, arrValues2)
      newVal3 = np.take(freqsArr, arrValues3)
      newVal4 = np.take(freqsArr, arrValues4)
      newVal5 = np.take(freqsArr, arrValues5)
      
      
      return(newVal1, newVal2, newVal3, newVal4, newVal5)      
 
      
def normalize_data_videos(pupilArea, pupilArea1, pupilArea2, valuesToNormalize):
     ''' 
     Allows to normalize the average pupil area for each video
     Args:
     pupilArea (np.array) = array containing the raw data of the pupil area
     valuesToNormalize (np.array) = array containing the values of the pupil area to normalize
     returns:
     noramlizedData (np.array) = variable containing an array with normalized values
     '''

     minVal1 = np.nanmin(pupilArea)
     minVal2 = np.nanmin(pupilArea1)
     minVal3 = np.nanmin(pupilArea2)
     minArray = np.array([minVal1, minVal2, minVal3])
     minValue = np.amin(minArray)
     maxVal1 = np.nanmax(pupilArea)
     maxVal2 = np.nanmax(pupilArea1)
     maxVal3 = np.nanmax(pupilArea2)
     maxArray = np.array([maxVal1, maxVal2, maxVal3])
     maxValue = np.amin(maxArray) 
     rangeValues = maxValue - minValue 
     listData = [] 
     for i in valuesToNormalize: 
         substractMin = i - minValue 
         newData = substractMin/rangeValues 
         listData.append(newData) 
         normalizedData = np.asarray(listData) 
     return(normalizedData)

def mean_freqs(arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5, arrFreq1a, arrFreq2a, arrFreq3a, arrFreq4a, arrFreq5a, arrFreq1b, arrFreq2b, arrFreq3b, arrFreq4b, arrFreq5b, arrFreq1c, arrFreq2c, arrFreq3c, arrFreq4c, arrFreq5c, arrFreq1d, arrFreq2d, arrFreq3d, arrFreq4d, arrFreq5d, arrFreq1e, arrFreq2e, arrFreq3e, arrFreq4e, arrFreq5e):
     
     totalPreFreq2khz = np.concatenate((arrFreq1, arrFreq1a, arrFreq1b), axis = None)
     totalPostFreq2khz = np.concatenate((arrFreq1c, arrFreq1d, arrFreq1e), axis = None)
     totalPreFreq4khz = np.concatenate((arrFreq2, arrFreq2a, arrFreq2b), axis = None)
     totalPostFreq4khz = np.concatenate((arrFreq2c, arrFreq2d, arrFreq2e), axis = None)
     totalPreFreq8khz = np.concatenate((arrFreq3, arrFreq3a, arrFreq3b), axis = None)
     totalPostFreq8khz = np.concatenate((arrFreq3c, arrFreq3d, arrFreq3e), axis = None)
     totalPreFreq16khz = np.concatenate((arrFreq4, arrFreq4a, arrFreq4b), axis = None)
     totalPostFreq16khz = np.concatenate((arrFreq4c, arrFreq4d, arrFreq4e), axis = None)
     totalPreFreq32khz = np.concatenate((arrFreq5, arrFreq5a, arrFreq5b), axis = None)
     totalPostFreq32khz = np.concatenate((arrFreq5c, arrFreq5d, arrFreq5e), axis = None)
     
     meanPreFreq2kHz = np.average(totalPreFreq2khz)
     meanPostFreq2kHz = np.average(totalPostFreq2khz)
     meanPreFreq4khz = np.average(totalPreFreq4khz)
     meanPostFreq4khz = np.average(totalPostFreq4khz)
     meanPreFreq8khz = np.average(totalPreFreq8khz)
     meanPostFreq8khz = np.average(totalPostFreq8khz)
     meanPreFreq16khz = np.average(totalPreFreq16khz)
     meanPostFreq16khz = np.average(totalPostFreq16khz)
     meanPreFreq32khz = np.average(totalPreFreq32khz)
     meanPostFreq32khz = np.average(totalPostFreq32khz)
     
     preData = np.array([meanPreFreq2kHz, meanPreFreq4khz, meanPreFreq8khz, meanPreFreq16khz, meanPreFreq32khz])
     postData = np.array([meanPostFreq2kHz, meanPostFreq4khz, meanPostFreq8khz, meanPostFreq16khz, meanPostFreq32khz])
     
     return(preData, postData)
     

def comparison_plot(time, valuesData1, valuesData2, valuesData3, pVal, pVal1, pVal2): 
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
     sp = np.round(pVal, decimals=9)
     sp1 = np.round(pVal1, decimals=9)
     sp2 = np.round(pVal2, decimals=9)
     label1 = filesDict['name1'],'pval:',sp
     label2 = filesDict['name2'],'pval:',sp1
     label3 = filesDict['name3'],'pval:',sp2

     subplt.plot(time, valuesData1, color = 'g', label = label1, linewidth = 4)
     subplt.plot(time, valuesData2, color = 'c', label = label2, linewidth = 4)
     subplt.plot(time, valuesData3, color = 'b', label = label3, linewidth = 4)

     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     subplt.set_title('Pupil behavior for frequency range 2kHz-32kHz: pure011 20220419', fontsize = labelsSize)
     plt.grid(b = True)
     #plt.ylim([550, 650])
     plt.xticks(fontsize = labelsSize)
     plt.yticks(fontsize = labelsSize)
     plt.legend()
     #plt.legend(prop ={"size":10}, bbox_to_anchor=(1.0, 0.8))
     #plt.savefig('comparisonPure004Plot', format = 'pdf', dpi = 50)
     plt.show() 
     return(plt.show())


def barScat_plots(firstPlotMeanValues1, firstPlotMeanValues2, xlabel1, xlabel2, firstPlotStdData1, firstPlotStdData2, secondPlotMeanValues1, secondPlotMeanValues2, secondPlotStdData1, secondPlotStdData2, thirdPlotMeanValues1, thirdPlotMeanValues2, thirdPlotStdData1, thirdPlotStdData2, pVal1, pVal2, pVal3):
     '''
     Plot bar plots
     Args:
     *MeanValues1 (np.array): array containing the average size of the pupil area pre stimulus
     *MeanValues2 (np.array): array containing the average size of the pupil area post stimulus
     *StdData1 (np.array): array containing the pupil area pre and stimulus
     *StdData2 (np.array): array containing the pupil area post and stimulus
     xlabel1 (string): name of the first condition to compare
     xlabel2 (string): name of the second condition to compare
     pVal1..3 (float or int): p-value for each one of the animals
     Returns:
     plt.show(): three bar plots within one figure
     '''
     barLabelsFontSize = 14
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
     shortPval1 = np.round(pVal1, decimals=9)
     shortPval2 = np.round(pVal2, decimals=9)
     shortPval3 = np.round(pVal3, decimals=9)
     pValue1 = 'P-value:', shortPval1
     pValue2 = 'P-value:', shortPval2
     pValue3 = 'P-value:', shortPval3
     dataPlot1 = [firstPlotMeanValues1, firstPlotMeanValues2] 
     dataPlot2 = [secondPlotMeanValues1, secondPlotMeanValues2] 
     dataPlot3 = [thirdPlotMeanValues1, thirdPlotMeanValues2]
     
     fig, barPlots = plt.subplots(1,3, constrained_layout = True, sharex = True, sharey = True)
     fig.set_size_inches(9.5, 7.5) 
     barPlots[0].bar(xlabels, barMeanValues1, yerr = stdErrors1, color = 'g', label = pValue1) 
     barPlots[0].errorbar(xlabels, barMeanValues1, yerr = stdErrors1, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[0].set_title(filesDict['name1'], fontsize = barLabelsFontSize)
     barPlots[0].set_ylabel(scatBarDict['yLabel'], fontsize = barLabelsFontSize)
     barPlots[0].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[0].plot(xlabels, dataPlot1, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[0].legend(prop ={"size":10})
     barPlots[1].bar(xlabels, barMeanValues2, yerr = stdErrors2, color= 'c', label = pValue2) 
     barPlots[1].errorbar(xlabels, barMeanValues2, yerr = stdErrors2, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[1].set_title(filesDict['name2'], fontsize = barLabelsFontSize)
     barPlots[1].set_xlabel(scatBarDict['xLabelTitle'], fontsize = barLabelsFontSize)
     barPlots[1].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[1].plot(xlabels, dataPlot2, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[1].legend(prop ={"size":10})
     barPlots[2].bar(xlabels, barMeanValues3, yerr = stdErrors3, color = 'b', label = pValue3) 
     barPlots[2].errorbar(xlabels, barMeanValues3, yerr = stdErrors3, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[2].set_title(filesDict['name3'], fontsize = barLabelsFontSize)
     barPlots[2].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[2].plot(xlabels, dataPlot3, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     
     #plt.ylim(250, 800)
     plt.suptitle(scatBarDict['title'], fontsize = barLabelsFontSize)
     barPlots[2].legend(prop ={"size":10})
     #plt.xlabel("common X", loc = 'center')
     #plt.savefig(scatBarDict['savedName'], format = 'pdf', dpi =50)
     plt.show() 
     return(plt.show()) 


def  pupilDilation_time(timeData1, plotData1, timeData2, plotData2, timeData3, plotData3): 
     fig, signalsPlots = plt.subplots(1,3, constrained_layout = True, sharey = True, sharex = True) 
     signalsPlots[0].plot(timeData1, plotData1) 
     signalsPlots[0].set(title = 'Video 1') 
     signalsPlots[0].set_ylabel('Pupil Area', fontsize = 13)
     signalsPlots[1].plot(timeData2, plotData2) 
     signalsPlots[1].set(title = 'Video 2')
     signalsPlots[1].set_xlabel('Time(s)', fontsize = 13)
     signalsPlots[2].plot(timeData3, plotData3) 
     signalsPlots[2].set(title = 'Video 3')
     plt.suptitle('Average trials behavior in time window: pure011 20220322')
     plt.show() 
     return(plt.show())


     
def two_traces_pupilkHz_plot(freqsArray, arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5, arrFreq1a, arrFreq2a, arrFreq3a, arrFreq4a, arrFreq5a, arrFreq1b, arrFreq2b, arrFreq3b, arrFreq4b, arrFreq5b, arrFreq1c, arrFreq2c, arrFreq3c, arrFreq4c, arrFreq5c, arrFreq1d, arrFreq2d, arrFreq3d, arrFreq4d, arrFreq5d, arrFreq1e, arrFreq2e, arrFreq3e, arrFreq4e, arrFreq5e):
     '''
     Plots average value of pupil size for a given set of frequencies
     Args:
     freqsArray (np.array): array containing the frequencies tested in the experiment
     arrFreq1..5(np.array): several arrays of the first dataset containing the corresponding post stimulus pupil area for each frequency in freqsArray
     arrFreq1a..5a(np.array): several arrays of the second dataset containing the corresponding post stimulus pupil area for each frequency in freqsArray
     arrFreq1b..5b(np.array): several arrays of the third dataset containing the corresponding post stimulus pupil area for each frequency in freqsArray
     arrFreq1c..5c(np.array): several arrays of the first dataset containing the corresponding pre stimulus pupil area for each frequency in freqsArray
     arrFreq1d..5d(np.array): several arrays of the second dataset containing the corresponding pre stimulus pupil area for each frequency in freqsArray
     arrFreq1e..5e(np.array): several arrays of the third dataset containing the corresponding pre stimulus pupil area for each frequency in freqsArray
     returns:
     plt.show(): plot traces comparing mean pupil size pre and post stimulus Vs frequencies
     '''

     labelsSize = 16
     fig, freqplt = plt.subplots(1,1, constrained_layout = True, sharex = True, sharey = True)
     fig.set_size_inches(9.5, 7.5, forward = True)
     label1 = filesDict['name1']
     label2 = filesDict['name2']
     label3 = filesDict['name3']
     labela = 'pre stim size, green'
     labelb = 'pre stim size, L. blue'
     labelc = 'pre stim size, D. blue'
     
     meanPoint1 = arrFreq1.mean(axis = 0)
     meanPoint2 = arrFreq2.mean(axis = 0)     
     meanPoint3 = arrFreq3.mean(axis = 0)     
     meanPoint4 = arrFreq4.mean(axis = 0)     
     meanPoint5 = arrFreq5.mean(axis = 0)      
     meanPoint1a = arrFreq1a.mean(axis = 0)
     meanPoint2a = arrFreq2a.mean(axis = 0)     
     meanPoint3a = arrFreq3a.mean(axis = 0)     
     meanPoint4a = arrFreq4a.mean(axis = 0)     
     meanPoint5a = arrFreq5a.mean(axis = 0)     
     meanPoint1b = arrFreq1b.mean(axis = 0)
     meanPoint2b = arrFreq2b.mean(axis = 0)     
     meanPoint3b = arrFreq3b.mean(axis = 0)     
     meanPoint4b = arrFreq4b.mean(axis = 0)     
     meanPoint5b = arrFreq5b.mean(axis = 0)
     premeanPoint1c = arrFreq1c.mean(axis = 0)
     premeanPoint2c = arrFreq2c.mean(axis = 0)     
     premeanPoint3c = arrFreq3c.mean(axis = 0)     
     premeanPoint4c = arrFreq4c.mean(axis = 0)     
     premeanPoint5c = arrFreq5c.mean(axis = 0)     
     premeanPoint1d = arrFreq1d.mean(axis = 0)
     premeanPoint2d = arrFreq2d.mean(axis = 0)     
     premeanPoint3d = arrFreq3d.mean(axis = 0)     
     premeanPoint4d = arrFreq4d.mean(axis = 0)     
     premeanPoint5d = arrFreq5d.mean(axis = 0)          
     premeanPoint1e = arrFreq1e.mean(axis = 0)
     premeanPoint2e = arrFreq2e.mean(axis = 0)     
     premeanPoint3e = arrFreq3e.mean(axis = 0)     
     premeanPoint4e = arrFreq4e.mean(axis = 0)     
     premeanPoint5e = arrFreq5e.mean(axis = 0)
     
     valPlot = [meanPoint1, meanPoint2, meanPoint3, meanPoint4, meanPoint5]
     valPlota = [meanPoint1a, meanPoint2a, meanPoint3a, meanPoint4a, meanPoint5a]     
     valPlotb = [meanPoint1b, meanPoint2b, meanPoint3b, meanPoint4b, meanPoint5b]
     valPlotc = [premeanPoint1c, premeanPoint2c, premeanPoint3c, premeanPoint4c, premeanPoint5c]
     valPlotd = [premeanPoint1d, premeanPoint2d, premeanPoint3d, premeanPoint4d, premeanPoint5d]     
     valPlote = [premeanPoint1e, premeanPoint2e, premeanPoint3e, premeanPoint4e, premeanPoint5e]

     freqplt.set_title(filesDict['nameCondition3'], fontsize = labelsSize)
     freqplt.set_ylabel('Mean pupil Area', fontsize = labelsSize)
     freqplt.set_xlabel('Frequencies (kHz)', fontsize = labelsSize)
     freqplt.tick_params(axis='both', labelsize = labelsSize)
     freqplt.plot(freqsArray, valPlot, color = 'g', marker = 'o')
     freqplt.plot(freqsArray, valPlota, color = 'c', marker = 'o')
     freqplt.plot(freqsArray, valPlotb, color = 'b', marker = 'o')   
     freqplt.plot(freqsArray, valPlotc, color = 'g', marker = 'o', label = labela, alpha = 0.3)
     freqplt.plot(freqsArray, valPlotd, color = 'c', marker = 'o', label = labelb, alpha = 0.3)
     freqplt.plot(freqsArray, valPlote, color = 'b', marker = 'o', label = labelc, alpha = 0.3)

     freqplt.grid(b = True)
     freqplt.legend(prop ={"size":10})
     plt.xticks(fontsize = labelsSize)
     plt.yticks(fontsize = labelsSize)
     plt.suptitle(scatBarDict['plotFreqName'], fontsize = labelsSize)
     plt.show() 
     return(plt.show())

def plot_normalized_data(frequencies, preValues, postValues):
     '''
     Plots the total pre and post values for each frequency with the mean normalized data
     '''
     labela = 'pre stimulus size'
     labelb = 'post stimulus size'
      
     labelSize = 16 
     fig, normTotal = plt.subplots(constrained_layout = True, sharex= True, sharey = True) 
     fig.set_size_inches(9.5, 7.5, forward = True)
     normTotal.set_title(scatBarDict['plotFreqName'], fontsize = labelSize)
     normTotal.set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
     normTotal.set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     normTotal.plot(frequencies, preValues, color = '#9ACD32', marker = 'o', label = labela)
     normTotal.plot(frequencies, postValues, color = '#FFA500', marker = 'o', label = labelb)
     plt.grid(b = True) 
     plt.xticks(fontsize = labelSize) 
     plt.yticks(fontsize = labelSize)
     plt.legend(prop ={"size":10}) 
     plt.show() 
     return(plt.show())
     
     
def plot_norm_errbar(frequencies, preValues, postValues, arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5, arrFreq1a, arrFreq2a, arrFreq3a, arrFreq4a, arrFreq5a, arrFreq1b, arrFreq2b, arrFreq3b, arrFreq4b, arrFreq5b, arrFreq1c, arrFreq2c, arrFreq3c, arrFreq4c, arrFreq5c, arrFreq1d, arrFreq2d, arrFreq3d, arrFreq4d, arrFreq5d, arrFreq1e, arrFreq2e, arrFreq3e, arrFreq4e, arrFreq5e, freqArr):
     '''
     Plots the total pre and post values for each frequency with the mean normalized data
     Note: the total* arrays were created differently compared to how it is compared in the comparison3Plots.py script because each of these arrays have a different size, the other ones
     did not have a different size
     
     '''
     totalPreFreq2khz = np.concatenate((arrFreq1, arrFreq1a, arrFreq1b), axis = None)
     totalPostFreq2khz = np.concatenate((arrFreq1c, arrFreq1d, arrFreq1e), axis = None)
     totalPreFreq4khz = np.concatenate((arrFreq2, arrFreq2a, arrFreq2b), axis = None)
     totalPostFreq4khz = np.concatenate((arrFreq2c, arrFreq2d, arrFreq2e), axis = None)
     totalPreFreq8khz = np.concatenate((arrFreq3, arrFreq3a, arrFreq3), axis = None)
     totalPostFreq8khz = np.concatenate((arrFreq3c, arrFreq3d, arrFreq3e), axis = None)
     totalPreFreq16khz = np.concatenate((arrFreq4, arrFreq4a, arrFreq4b), axis = None)
     totalPostFreq16khz = np.concatenate((arrFreq4c, arrFreq4d, arrFreq4e), axis = None)
     totalPreFreq32khz = np.concatenate((arrFreq5, arrFreq5a, arrFreq5b), axis = None)
     totalPostFreq32khz = np.concatenate((arrFreq5c, arrFreq5d, arrFreq5e), axis = None)
     meanPreFreq2kHz = np.average(totalPreFreq2khz)
     meanPostFreq2kHz = np.average(totalPostFreq2khz)
     meanPreFreq4khz = np.average(totalPreFreq4khz)
     meanPostFreq4khz = np.average(totalPostFreq4khz)
     meanPreFreq8khz = np.average(totalPreFreq8khz)
     meanPostFreq8khz = np.average(totalPostFreq8khz)
     meanPreFreq16khz = np.average(totalPreFreq16khz)
     meanPostFreq16khz = np.average(totalPostFreq16khz)
     meanPreFreq32khz = np.average(totalPreFreq32khz)
     meanPostFreq32khz = np.average(totalPostFreq32khz)
     errPre2khz = np.std(totalPreFreq2khz)
     errPost2khz = np.std(totalPostFreq2khz)
     errPre4khz = np.std(totalPreFreq4khz)
     errPost4khz = np.std(totalPostFreq4khz)
     errPre8khz = np.std(totalPreFreq8khz)
     errPost8khz = np.std(totalPostFreq8khz)
     errPre16khz = np.std(totalPreFreq16khz)
     errPost16khz = np.std(totalPostFreq16khz)
     errPre32khz = np.std(totalPreFreq32khz)
     errPost32khz = np.std(totalPostFreq32khz) 
     labela = 'pre stimulus size'
     labelb = 'post stimulus size'
  
     labelSize = 16 
     fig, normTotal = plt.subplots(1,1, constrained_layout = True, sharex= True, sharey = True) 
     fig.set_size_inches(9.5, 7.5, forward = True)
     normTotal.set_title(scatBarDict['plotFreqName'], fontsize = labelSize)
     normTotal.set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
     normTotal.set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     normTotal.plot(frequencies, preValues, color = '#000000', marker = 'o', markersize = '5', label = labela)
     normTotal.plot(frequencies, postValues, color = '#FFA500', marker = 'o', markersize = '5', label = labelb)
     normTotal.errorbar(frequencies[0], preValues[0], yerr = errPre2khz, fmt='none', capsize=3.5, color = '#000000')
     normTotal.errorbar(frequencies[1], preValues[1], yerr = errPre4khz, fmt='none', capsize=3.5, color = '#000000')
     normTotal.errorbar(frequencies[2], preValues[2], yerr = errPre8khz, fmt='none', capsize=3.5, color = '#000000')
     normTotal.errorbar(frequencies[3], preValues[3], yerr = errPre16khz, fmt='none', capsize=3.5, color = '#000000')
     normTotal.errorbar(frequencies[4], preValues[4], yerr = errPre32khz, fmt='none', capsize=3.5, color = '#000000')
     normTotal.errorbar(frequencies[0], postValues[0], yerr = errPost2khz, fmt='none', capsize=3.5, color = '#FFA500')
     normTotal.errorbar(frequencies[1], postValues[1], yerr = errPost4khz, fmt='none', capsize=3.5, color = '#FFA500')
     normTotal.errorbar(frequencies[2], postValues[2], yerr = errPost8khz, fmt='none', capsize=3.5, color = '#FFA500')
     normTotal.errorbar(frequencies[3], postValues[3], yerr = errPost16khz, fmt='none', capsize=3.5, color = '#FFA500')
     normTotal.errorbar(frequencies[4], postValues[4], yerr = errPost32khz, fmt='none', capsize=3.5, color = '#FFA500')

     plt.grid(b = True) 
     plt.xticks(fontsize = labelSize) 
     plt.yticks(fontsize = labelSize)
     plt.legend(prop ={"size":10}) 
     plt.show() 
     return(plt.show())


 

filesDict = {'loadFile1':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220419_xtremes_198_xconfig1_proc.npy', allow_pickle = True).item(),
	'config1':'2Sconfig3', 'sessionFile1':'20220419_xtremes_198_xconfig1', 'condition1':'detectiongonogo', 'sound':'ChordTrain', 'name1':'pure011', 'plotName1':'pure011 session01',
	'loadFile2':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220419_xtremes_199_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config2':'2Sconfig3', 'name2':'pure011', 'plotName2':'pure011 session02', 'sessionFile2':'20220419_xtremes_199_xconfig1',
	'loadFile3':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220419_xtremes_200_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config3':'2Sconfig3', 'sessionFile3':'20220419_xtremes_200_xconfig1', 'name3':'pure010', 'nameCondition1':'pre stimulus' ,'nameCondition2':'post stimulus', 'nameCondition3':'pre & post stimulus onset', 'plotName3':'pure010 session03'}

scatBarDict = {'title':'Pupil behavior before and after sound stimulus: pure011 20220419', 'savedName':'pure0043ScatbarPlot', 'yLabel':'Mean Pupil Area', 'xLabelTitle':'Conditions', 'plotFreqName':'Pupil size for 5 different frequencies: pure011_20220419'}


subject = filesDict['name1']
paradigm = filesDict['condition1']
session = filesDict['sessionFile1']

behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)
preFreqs = bdata['preFreq'] #works with modified detectiongonogo paradigm
postFreqs = bdata['postFreq'] #works with modified detectiongonogo paradigm


subject2 = filesDict['name1']
paradigm2 = filesDict['condition1']
session2 = filesDict['sessionFile2']

behavFile2 = loadbehavior.path_to_behavior_data(subject2, paradigm2, session2)
bdata2 = loadbehavior.BehaviorData(behavFile2)
preFreqs2 = bdata2['preFreq'] #works with modified detectiongonogo paradigm
postFreqs2 = bdata2['postFreq'] #works with modified detectiongonogo paradigm


subject3 = filesDict['name1']
paradigm3 = filesDict['condition1']
session3 = filesDict['sessionFile3']

behavFile3 = loadbehavior.path_to_behavior_data(subject3, paradigm3, session3)
bdata3 = loadbehavior.BehaviorData(behavFile3)
preFreqs3 = bdata3['preFreq'] #works with modified detectiongonogo paradigm
postFreqs3 = bdata3['postFreq'] #works with modified detectiongonogo paradigm

frequenciesTested = np.array([2, 4, 8, 16, 32])
frequenciesTestedArr = np.array([[2, 2, 4, 4, 8], [8, 16, 16, 32, 32]])

#list(map(tuple, np.where(np.isnan(pArea))))






proc = filesDict['loadFile1']

#---obtain pupil data---
pupil = proc['pupil'][0] # Dic.
pArea = pupil['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
minBlink = np.amin(blink2)
maxBlink = np.amax(blink2) - minBlink
blink2Bool = np.logical_and(blink2 >= minBlink, blink2 < maxBlink) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.


#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
#newFrame = frameVec[blink2Bool]
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video.


#--- obtaining onset sync signal values ---
syncOnsetValues = onset_values(indicesValueSyncSignal) #--> if the terminal complains around here, check the blink2Bool variable.
timeOfBlink2Event = timeVec[syncOnsetValues] # Provides the time values in which the sync signal is on.
timeOfBlink2Event = timeOfBlink2Event[0:-1]

#--- Align trials to the event ---
timeRange = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal, postSignal = find_prepost_values(windowTimeVec, windowed_signal, -0.5, 0, 1.4, 2.0)
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']



#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([-15, 15])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)
pAreaDilatedMean = pAreaDilated.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value', wstat,',',  'P-value', pval )

prefreqValues1, prefreqValues2, prefreqValues3, prefreqValues4, prefreqValues5 = freqs_gonogo(preSignal, postFreqs, 2000, 4000, 8000, 16000, 32000)

postfreqValues1, postfreqValues2, postfreqValues3, postfreqValues4, postfreqValues5 = freqs_gonogo(postSignal, postFreqs, 2000, 4000, 8000, 16000, 32000) #works with modified detectiongonogo paradigm














proc1 = filesDict['loadFile2']


#---obtain pupil data---
pupil1 = proc1['pupil'][0] # Dic.
pArea1 = pupil1['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink1a = proc1['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink11 = proc1['blink']   # List.
blink21 = np.array(blink1a).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
minBlink1 = np.amin(blink21)
maxBlink1 = np.amax(blink21) - minBlink1 #500
blink2Bool1 = np.logical_and(blink21 > minBlink1, blink21 < maxBlink1) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeOfBlink2Event1 = timeOfBlink2Event1[0:-1]

#--- Align trials to the event ---
timeRange1 = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec1, windowed_signal1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRange1)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal1, postSignal1 = find_prepost_values(windowTimeVec1, windowed_signal1, -0.5, 0, 1.4, 2.0)
averagePreSignal1 = preSignal1.mean(axis = 0)
averagePostSignal1 = postSignal1.mean(axis = 0)
dataToPlot1 = [averagePreSignal1, averagePostSignal1]
xlabels1 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation1 = np.array([-15, 15])
pupilDilationTimeWindowVec1, pAreaDilated1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRangeForPupilDilation1)
pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat1, pval1 = stats.wilcoxon(averagePreSignal1, averagePostSignal1)
print('Wilcoxon value', wstat1,',',  'P-value', pval1 )



prefreqValues1a, prefreqValues2a, prefreqValues3a, prefreqValues4a, prefreqValues5a = freqs_gonogo(preSignal1, postFreqs2, 2000, 4000, 8000, 16000, 32000) # works with modified detectiongonogo paradigm

postfreqValues1a, postfreqValues2a, postfreqValues3a, postfreqValues4a, postfreqValues5a = freqs_gonogo(postSignal1, postFreqs2, 2000, 4000, 8000, 16000, 32000) #works with modified detectiongonogo paradigm








proc2 = filesDict['loadFile3']


#---obtain pupil data---
pupil2 = proc2['pupil'][0] # Dic.
pArea2 = pupil2['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink2a = proc2['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink12 = proc2['blink']   # List.
blink22 = np.array(blink2a).T # Creates transpose matrix of blink. Necessary for plotting.





#---obtain values where sync signal is on---
minBlink2 = np.amin(blink22)
maxBlink2 = np.amax(blink22) - minBlink2 
blink2Bool2 = np.logical_and(blink22 > minBlink2, blink22 < maxBlink2 ) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeOfBlink2Event2 = timeOfBlink2Event2[0:-1]

#--- Align trials to the event ---
timeRange2 = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec2, windowed_signal2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRange2)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal2, postSignal2 = find_prepost_values(windowTimeVec2, windowed_signal2, -0.5, 0, 1.4, 2.0)
averagePreSignal2 = preSignal2.mean(axis = 0)
averagePostSignal2 = postSignal2.mean(axis = 0)
dataToPlot2 = [averagePreSignal2, averagePostSignal2]
xlabels2 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation2 = np.array([-15, 15])
pupilDilationTimeWindowVec2, pAreaDilated2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRangeForPupilDilation2)
pAreaDilatedMean2 = pAreaDilated2.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat2, pval2 = stats.wilcoxon(averagePreSignal2, averagePostSignal2)
print('Wilcoxon value', wstat2,',',  'P-value', pval2 )


prefreqValues1b, prefreqValues2b, prefreqValues3b, prefreqValues4b, prefreqValues5b = freqs_gonogo(preSignal2, postFreqs3, 2000, 4000, 8000, 16000, 32000) # works with modified detectiongonogo paradigm

postfreqValues1b, postfreqValues2b, postfreqValues3b, postfreqValues4b, postfreqValues5b = freqs_gonogo(postSignal2, postFreqs3, 2000, 4000, 8000, 16000, 32000) #works with modified detectiongonogo paradigm


#--- Normalized data for plotting ---
normPreVal1 = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues1)
normPreVal2 = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues2)
normPreVal3 = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues3)
normPreVal4 = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues4)
normPreVal5 = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues5)

normPostVal1 = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues1)
normPostVal2 = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues2)
normPostVal3 = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues3)
normPostVal4 = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues4)
normPostVal5 = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues5)

normPreVal1a = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues1a)
normPreVal2a = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues2a)
normPreVal3a = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues3a)
normPreVal4a = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues4a)
normPreVal5a = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues5a)

normPostVal1a = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues1a)
normPostVal2a = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues2a)
normPostVal3a = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues3a)
normPostVal4a = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues4a)
normPostVal5a = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues5a)

normPreVal1b = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues1b)
normPreVal2b = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues2b)
normPreVal3b = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues3b)
normPreVal4b = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues4b)
normPreVal5b = normalize_data_videos(pArea, pArea1, pArea2, prefreqValues5b)

normPostVal1b = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues1b)
normPostVal2b = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues2b)
normPostVal3b = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues3b)
normPostVal4b = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues4b)
normPostVal5b = normalize_data_videos(pArea, pArea1, pArea2, postfreqValues5b)



#--- Calculation of the mean normalized data for pre and post total values only---
preStimValues, postStimValues = mean_freqs(normPreVal1, normPostVal1, normPreVal2, normPostVal2, normPreVal3, normPostVal3, normPreVal4, normPostVal4, normPreVal5, normPostVal5, normPreVal1a,  normPostVal1a, normPreVal2a, normPostVal2a, normPreVal3a, normPostVal3a, normPreVal4a, normPostVal4a, normPreVal5a, normPostVal5a, normPreVal1b, normPostVal1b, normPreVal2b, normPostVal2b, normPreVal3b, normPostVal3b, normPreVal4b, normPostVal4b, normPreVal5b, normPostVal5b) #preStim represents the total mean normalized values of each freq (2,4,8, etc.), postStim is the same but for the post Data


#--- plot with the three conditions aligned ---
OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean,  pAreaDilatedMean1, pAreaDilatedMean2, pval, pval1, pval2)


#--- Figure with 3 scatter plots ---
#scatterPlots = scatter_plots(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2, averagePreSignal3, averagePostSignal3)

#--- Figure with 3 bar plots and scatter plots ---
#scattBar = barScat_plots(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal, averagePreSignal1, averagePostSignal1, preSignal1, postSignal1, averagePreSignal2, averagePostSignal2, preSignal2, postSignal2, pval, pval1, pval2)

#--- Pupil Dilation plots --- 
#pupilDilationPlots = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean, pupilDilationTimeWindowVec1, pAreaDilatedMean1, pupilDilationTimeWindowVec2, pAreaDilatedMean2)

#--- scatter & bar plots overlapped ---
#scattBar = barScat_plots(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2)

# --- plotting the pupil mean size vs frequency individually ---

prePostTraces = two_traces_pupilkHz_plot(frequenciesTested, postfreqValues1, postfreqValues2, postfreqValues3, postfreqValues4, postfreqValues5, postfreqValues1a, postfreqValues2a, postfreqValues3a, postfreqValues4a, postfreqValues5a, postfreqValues1b, postfreqValues2b, postfreqValues3b, postfreqValues4b, postfreqValues5b, prefreqValues1, prefreqValues2, prefreqValues3, prefreqValues4, prefreqValues5, prefreqValues1a, prefreqValues2a, prefreqValues3a, prefreqValues4a, prefreqValues5a, prefreqValues1b, prefreqValues2b, prefreqValues3b, prefreqValues4b, prefreqValues5b)

# --- plotting normalized pupil data ---
#normalPlot = plot_normalized_data(frequenciesTested, preStimValues, postStimValues)

prePostValuesAcrossVideos = plot_norm_errbar(frequenciesTested, preStimValues, postStimValues, normPreVal1, normPostVal1, normPreVal2, normPostVal2, normPreVal3, normPostVal3, normPreVal4, normPostVal4, normPreVal5, normPostVal5, normPreVal1a,  normPostVal1a, normPreVal2a, normPostVal2a, normPreVal3a, normPostVal3a, normPreVal4a, normPostVal4a, normPreVal5a, normPostVal5a, normPreVal1b, normPostVal1b, normPreVal2b, normPostVal2b, normPreVal3b, normPostVal3b, normPreVal4b, normPostVal4b, normPreVal5b, normPostVal5b, frequenciesTestedArr)

