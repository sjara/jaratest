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
      
def find_freqs_indices(preFreqArr, postFreqArr, freq1, freq2, freq3, freq4, freq5):
      '''
      find the indices of each post frequency
      Args:
      preFreqArr (np.array): array containing the frequencies corresponding to the pre period
      postFreqArr (np.array): array containing the frequencies corresponding to the post period
      freq1 (np.array): lowest frequency tested, it must be the minimum value in the frequency range tested
      freq 2..4 (np.array): frequencies tested between the frequencies range
      freq 5 (np.array): highest frequency tested, it must be the maximum value in the frequency range tested
      
      returns:
      findPostFreq1..5Arr = arrays containing the indices values for each freq that correspond to the postValues used as an input
      '''
      findPreFreq1 = np.argwhere(freq1 == preFreqArr) #finds indices for 2kHz values in preFreqs
      findPreFreq1Arr = findPreFreq1.flatten()
      findPreFreq2 = np.argwhere(freq5 == preFreqArr) #finds indices for 32kHz values in preFreqs
      findPreFreq2Arr = findPreFreq2.flatten()
      correspondingValues1 = np.take(postFreqArr, findPreFreq1Arr) #finds all post frequencies values for pre 2kHz
      correspondingValues2 = np.take(postFreqArr, findPreFreq2Arr) #finds all post frequencies values for pre 32kHz
      #print(findPreFreq1Arr)
      #print(correspondingValues1)
      findPostFreq1 = np.argwhere(freq1 == correspondingValues1) #finds the 2kHz post values indices with 2kHz as pre value
      
      findPostFreq1a = np.argwhere(freq1 == correspondingValues2) #finds the 2kHz post values indices with 32kHz as pre value.. so forth
      findPostFreq2 = np.argwhere(freq2 == correspondingValues1)
      findPostFreq2a = np.argwhere(freq2 == correspondingValues2)
      findPostFreq3 = np.argwhere(freq3 == correspondingValues1)
      findPostFreq3a = np.argwhere(freq3 == correspondingValues2)
      findPostFreq4 = np.argwhere(freq4 == correspondingValues1)
      findPostFreq4a = np.argwhere(freq4 == correspondingValues2)
      findPostFreq5 = np.argwhere(freq5 == correspondingValues1)
      findPostFreq5a = np.argwhere(freq5 == correspondingValues2)
      findPostFreq1Arr = findPostFreq1.flatten()
      findPostFreq1aArr = findPostFreq1a.flatten()
      findPostFreq2Arr = findPostFreq2.flatten()
      findPostFreq2aArr = findPostFreq2a.flatten()
      findPostFreq3Arr = findPostFreq3.flatten()
      findPostFreq3aArr = findPostFreq3a.flatten()
      findPostFreq4Arr = findPostFreq4.flatten()
      findPostFreq4aArr = findPostFreq4a.flatten()
      findPostFreq5Arr = findPostFreq5.flatten()
      findPostFreq5aArr = findPostFreq5a.flatten()
      #print(findPostFreq1Arr)
      
      return(findPostFreq1Arr, findPostFreq1aArr, findPostFreq2Arr, findPostFreq2aArr, findPostFreq3Arr, findPostFreq3aArr, findPostFreq4Arr, findPostFreq4aArr, findPostFreq5Arr, findPostFreq5aArr, findPreFreq1Arr, findPreFreq2Arr)


def find_prepost_freqs_values(preValues, postValues, indices1, indices1a, indices2, indices2a, indices3, indices3a, indices4, indices4a, indices5, indices5a, indicesPre2kz, indicesPre32kz):
      '''
      Provides the pupil size values in the pre period and post period for given indices
      args:
      preValues (np.array) = array containing the pupil size in the pre period
      postValues (np.array) = array containing the pupil size in the post period
      indices1..5 (np.array) = array containing the indices of each frequency that matches the lowest frequency tested
      indices1a..5a (np.array) = array containing the indices of each frequency that matches the highest frequency tested
      indicesPre2kz (np.array) = array containig the indices of the lowest frequency tested in the pre period
      indicesPre32kz (np.array) = array containig the indices of the highest frequency tested in the pre period.
      
      returns:
      postValues2Kz1..5 (np.array) = array containing the pupil values for each frequency in the post period for the lowest frequency tested
      postValues32Kz1a..5a (np.array) = array containing the pupil values for each frequency in the post period forthe highest frequency tested.
      flatPre2Kz (np.array) = flattened array with the pupil values during the pre period for the lowest frequency tested.
      flatPre32Kz (np.array) = flattened array with the pupil values during the pre period for the highest frequency tested
      
      '''

      preValues2Kz = np.take(preValues, indicesPre2kz) #finds pupil pre values of 2kHz in preSignal
      preValues32Kz = np.take(preValues, indicesPre32kz) #finds pupil pre values of 32kHz in preSignal
      flatPre2Kz = preValues2Kz.flatten()
      flatPre32Kz = preValues32Kz.flatten()
    
      postValues2Kz1 = np.take(postValues, indices1)
      postValues2Kz2 = np.take(postValues, indices2)
      postValues2Kz3 = np.take(postValues, indices3)
      postValues2Kz4 = np.take(postValues, indices4)
      postValues2Kz5 = np.take(postValues, indices5)

      postValues32Kz1a = np.take(postValues, indices1a)
      postValues32Kz2a = np.take(postValues, indices2a)
      postValues32Kz3a = np.take(postValues, indices3a)
      postValues32Kz4a = np.take(postValues, indices4a)
      postValues32Kz5a = np.take(postValues, indices5a)
            
      return(postValues2Kz1, postValues2Kz2, postValues2Kz3, postValues2Kz4, postValues2Kz5, postValues32Kz1a, postValues32Kz2a, postValues32Kz3a, postValues32Kz4a, postValues32Kz5a, flatPre2Kz, flatPre32Kz)
       
     
      
      
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
 
      
def normalize_data_videos(pupilArea, pupilArea1, pupilArea2, pupilArea3, pupilArea4, pupilArea5, valuesToNormalize):
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
     minVal4 = np.nanmin(pupilArea3)
     minVal5 = np.nanmin(pupilArea4)
     minVal6 = np.nanmin(pupilArea5)
     minArray = np.array([minVal1, minVal2, minVal3, minVal4, minVal5, minVal6])
     minValue = np.amin(minArray)
     maxVal1 = np.nanmax(pupilArea)
     maxVal2 = np.nanmax(pupilArea1)
     maxVal3 = np.nanmax(pupilArea2)
     maxVal4 = np.nanmax(pupilArea3)
     maxVal5 = np.nanmax(pupilArea4)
     maxVal6 = np.nanmax(pupilArea5)
     maxArray = np.array([maxVal1, maxVal2, maxVal3, maxVal4, maxVal5, maxVal6])
     maxValue = np.amin(maxArray) 
     rangeValues = maxValue - minValue 
     listData = [] 
     for i in valuesToNormalize: 
         substractMin = i - minValue 
         newData = substractMin/rangeValues 
         listData.append(newData) 
         normalizedData = np.asarray(listData) 
     return(normalizedData)

def indices_values_each_freq(meanPrePupilSize, meanPostPupilSize, indices1, indices2, indices3, indices4, indices5, indices6, indices7, indices8, indices9, indices10):
     
     preValues2kz1 = np.take(meanPrePupilSize, indices1)
     preValues4kz1 = np.take(meanPrePupilSize, indices2)
     preValues8kz1 = np.take(meanPrePupilSize, indices3)
     preValues16kz1 = np.take(meanPrePupilSize, indices4)
     preValues32kz1 = np.take(meanPrePupilSize, indices5)
     postValues2kz1 = np.take(meanPostPupilSize, indices1)
     postValues4kz1 = np.take(meanPostPupilSize, indices2)
     postValues8kz1 = np.take(meanPostPupilSize, indices3)
     postValues16kz1 = np.take(meanPostPupilSize, indices4)
     postValues32kz1 = np.take(meanPostPupilSize, indices5)
     
     preValues2kz2 = np.take(meanPrePupilSize, indices6)
     preValues4kz2 = np.take(meanPrePupilSize, indices7)
     preValues8kz2 = np.take(meanPrePupilSize, indices8)
     preValues16kz2 = np.take(meanPrePupilSize, indices9)
     preValues32kz2 = np.take(meanPrePupilSize, indices10)
     postValues2kz2 = np.take(meanPostPupilSize, indices6)
     postValues4kz2 = np.take(meanPostPupilSize, indices7)
     postValues8kz2 = np.take(meanPostPupilSize, indices8)
     postValues16kz2 = np.take(meanPostPupilSize, indices9)
     postValues32kz2 = np.take(meanPostPupilSize, indices10)     
     
     return(preValues2kz1, preValues4kz1, preValues8kz1, preValues16kz1, preValues32kz1, postValues2kz1, postValues4kz1, postValues8kz1, postValues16kz1, postValues32kz1, preValues2kz2, preValues4kz2, preValues8kz2, preValues16kz2, preValues32kz2, postValues2kz2, postValues4kz2, postValues8kz2, postValues16kz2, postValues32kz2)
     
     
     
     

     

def comparison_plot(time, valuesData1, valuesData2, valuesData3, valuesData4, valuesData5, valuesData6, pVal, pVal1, pVal2, pVal3, pVal4, pVal5): 
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
     
     sp = np.round(pVal, decimals=5)
     sp1 = np.round(pVal1, decimals=5)
     sp2 = np.round(pVal2, decimals=5)
     sp3 = np.round(pVal3, decimals=5)
     sp4 = np.round(pVal4, decimals=5)
     sp5 = np.round(pVal5, decimals=5)
     
     label1 = filesDict['name1'],'pval:',sp
     label2 = filesDict['name2'],'pval:',sp1
     label3 = filesDict['name3'],'pval:',sp2
     label4 = filesDict['name4'],'pval:',sp3
     label5 = filesDict['name5'],'pval:',sp4
     label6 = filesDict['name6'],'pval:',sp5
     
     subplt.plot(time, valuesData1, color = 'g', label = label1, linewidth = 4)
     subplt.plot(time, valuesData2, color = 'c', label = label2, linewidth = 4)
     subplt.plot(time, valuesData3, color = 'b', label = label3, linewidth = 4)
     subplt.plot(time, valuesData4, color = 'm', label = label4, linewidth = 4)
     subplt.plot(time, valuesData5, color = 'r', label = label5, linewidth = 4)
     subplt.plot(time, valuesData6, color = 'y', label = label6, linewidth = 4)
     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     subplt.set_title('Pupil behavior for 6kHz: pure004 20211207', fontsize = labelsSize)
     plt.grid(b = True)
     #plt.ylim([300, 800])
     plt.xticks(fontsize = labelsSize)
     plt.yticks(fontsize = labelsSize)
     plt.legend(prop ={"size":10})#, bbox_to_anchor=(1.0, 0.8))
     #plt.savefig('comparisonControlsPure004Plot', format = 'pdf', dpi = 50)
     plt.show() 
     return(plt.show())

def scatter_plots(preValues1, postValues1, preValues2, postValues2, preValues3, postValues3, preValues4, postValues4):
     '''
     Create 3 scatter plots within one figure
     Args:
     preValues (np.array): trials values before stimulus onset
     postValues (np.array): trials values after stimulus onset
     Returns:
     plt.show(): one figure with 3 scatter plots.
     '''
     scatterLabelsSize = 14
     scatterXlabels = 11.5
     xLabelling = ['Pre stimulus onset', 'Post stimulus onset'] 
     dataToPlot1 = [preValues1, postValues1] 
     dataToPlot2 = [preValues2, postValues2] 
     dataToPlot3 = [preValues3, postValues3]  
     dataToPlot4 = [preValues4, postValues4]
     fig, scatterPlots = plt.subplots(1,4, constrained_layout = True, sharex = True, sharey = True)
     fig.set_size_inches(10.5, 7.5)
     scatterPlots[0].plot(xLabelling, dataToPlot1, marker = 'o', linewidth = 1) 
     scatterPlots[0].set_title(filesDict['name1'], fontsize = scatterLabelsSize)
     scatterPlots[0].set_ylabel('Mean Pupil Area', fontsize = scatterLabelsSize)
     scatterPlots[0].tick_params(axis = 'x', labelsize = scatterXlabels)
     scatterPlots[1].plot(xLabelling, dataToPlot2, marker = 'o', linewidth = 1) 
     scatterPlots[1].set_title(filesDict['name2'], fontsize = scatterLabelsSize)
     scatterPlots[1].tick_params(axis = 'x', labelsize = scatterXlabels) 
     scatterPlots[2].plot(xLabelling, dataToPlot3, marker = 'o', linewidth = 1) 
     scatterPlots[2].set_title(filesDict['name3'], fontsize = scatterLabelsSize)
     scatterPlots[2].tick_params(axis = 'x', labelsize = scatterXlabels)
     plt.suptitle('Average trials signals behavior: pure004_20210928', fontsize = scatterLabelsSize)
     scatterPlots[3].plot(xLabelling, dataToPlot4, marker = 'o', linewidth = 1)
     scatterPlots[3].set_title(filesDict['config4'], fontsize = scatterLabelsSize)
     scatterPlots[3].tick_params(axis = 'x', labelsize = scatterXlabels)
     plt.rc('xtick', labelsize = scatterXlabels)
     plt.rc('ytick', labelsize = scatterLabelsSize)
     plt.savefig('scatterPure004Plot', format = 'pdf', dpi = 50)
     plt.show()
     return(plt.show())

def barScat_plots(firstPlotMeanValues1, firstPlotMeanValues2, xlabel1, xlabel2, firstPlotStdData1, firstPlotStdData2, secondPlotMeanValues1, secondPlotMeanValues2, secondPlotStdData1, secondPlotStdData2, thirdPlotMeanValues1, thirdPlotMeanValues2, thirdPlotStdData1, thirdPlotStdData2, fourthPlotMeanValues1, fourthPlotMeanValues2, fourthPlotStdData1, fourthPlotStdData2, fifthPlotMeanValues1, fifthPlotMeanValues2, fifthPlotStdData1, fifthPlotStdData2, sixthPlotMeanValues1, sixthPlotMeanValues2, sixthPlotStdData1, sixthPlotStdData2, pVal1, pVal2, pVal3, pVal4, pVal5, pVal6):
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
     meanPreSignal2 = secondPlotMeanValues1.mean(axis = 0) 
     meanPostSignal2 = secondPlotMeanValues2.mean(axis = 0) 
     meanPreSignal3 = thirdPlotMeanValues1.mean(axis = 0) 
     meanPostSignal3 = thirdPlotMeanValues2.mean(axis = 0)
     meanPreSignal4 = fourthPlotMeanValues1.mean(axis = 0) 
     meanPostSignal4 = fourthPlotMeanValues2.mean(axis = 0)
     meanPreSignal5 = fifthPlotMeanValues1.mean(axis = 0) 
     meanPostSignal5 = fifthPlotMeanValues2.mean(axis = 0)
     meanPreSignal6 = sixthPlotMeanValues1.mean(axis = 0) 
     meanPostSignal6 = sixthPlotMeanValues2.mean(axis = 0) 
     preSignalStd1 = np.std(firstPlotStdData1) 
     postSignalStd1 = np.std(firstPlotStdData2) 
     preSignalStd2 = np.std(secondPlotStdData1) 
     postSignalStd2 = np.std(secondPlotStdData2) 
     preSignalStd3 = np.std(thirdPlotStdData1) 
     postSignalStd3 = np.std(thirdPlotStdData2)
     preSignalStd4 = np.std(fourthPlotStdData1) 
     postSignalStd4 = np.std(fourthPlotStdData2)
     preSignalStd5 = np.std(fifthPlotStdData1) 
     postSignalStd5 = np.std(fifthPlotStdData2)
     preSignalStd6 = np.std(sixthPlotStdData1) 
     postSignalStd6 = np.std(sixthPlotStdData2) 
     barMeanValues1 = [meanPreSignal1, meanPostSignal1] 
     barMeanValues2 = [meanPreSignal2, meanPostSignal2] 
     barMeanValues3 = [meanPreSignal3, meanPostSignal3]
     barMeanValues4 = [meanPreSignal4, meanPostSignal4]
     barMeanValues5 = [meanPreSignal5, meanPostSignal5]
     barMeanValues6 = [meanPreSignal6, meanPostSignal6]
     stdErrors1 = [preSignalStd1, postSignalStd1] 
     stdErrors2 = [preSignalStd2, postSignalStd2] 
     stdErrors3 = [preSignalStd3, postSignalStd3]
     stdErrors4 = [preSignalStd4, postSignalStd4]
     stdErrors5 = [preSignalStd5, postSignalStd5]
     stdErrors6 = [preSignalStd6, postSignalStd6]
     shortPval1 = np.round(pVal1, decimals=15)
     shortPval2 = np.round(pVal2, decimals=3)
     shortPval3 = np.round(pVal3, decimals=3)
     shortPval4 = np.round(pVal4, decimals=5)
     shortPval5 = np.round(pVal5, decimals=3)
     shortPval6 = np.round(pVal6, decimals=5)
     pValue1 = 'P-value:', shortPval1
     pValue2 = 'P-value:', shortPval2
     pValue3 = 'P-value:', shortPval3
     pValue4 = 'P-value:', shortPval4
     pValue5 = 'P-value:', shortPval5
     pValue6 = 'P-value:', shortPval6
     dataPlot1 = [firstPlotMeanValues1, firstPlotMeanValues2] 
     dataPlot2 = [secondPlotMeanValues1, secondPlotMeanValues2] 
     dataPlot3 = [thirdPlotMeanValues1, thirdPlotMeanValues2]
     dataPlot4 = [fourthPlotMeanValues1, fourthPlotMeanValues2]
     dataPlot5 = [fifthPlotMeanValues1, fifthPlotMeanValues2]
     dataPlot6 = [sixthPlotMeanValues1, sixthPlotMeanValues2]
     
     fig, barPlots = plt.subplots(1,6, constrained_layout = True, sharex = True, sharey = True)
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
     barPlots[1].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[1].plot(xlabels, dataPlot2, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[1].legend(prop ={"size":10})
     barPlots[2].bar(xlabels, barMeanValues3, yerr = stdErrors3, color = 'b', label = pValue3)
     barPlots[2].set_xlabel(scatBarDict['xLabelTitle'], fontsize = barLabelsFontSize)
     barPlots[2].errorbar(xlabels, barMeanValues3, yerr = stdErrors3, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[2].set_title(filesDict['name3'], fontsize = barLabelsFontSize)
     barPlots[2].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[2].plot(xlabels, dataPlot3, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[3].bar(xlabels, barMeanValues4, yerr = stdErrors4, color = 'm', label = pValue4)
     barPlots[3].errorbar(xlabels, barMeanValues4, yerr = stdErrors4, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[3].set_title(filesDict['name4'], fontsize = barLabelsFontSize)
     barPlots[3].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[3].plot(xlabels, dataPlot4, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[4].bar(xlabels, barMeanValues5, yerr = stdErrors5, color = 'r', label = pValue5)
     barPlots[4].errorbar(xlabels, barMeanValues5, yerr = stdErrors5, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black')
     barPlots[4].set_title(filesDict['name5'], fontsize = barLabelsFontSize)
     barPlots[4].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[4].plot(xlabels, dataPlot5, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[5].bar(xlabels, barMeanValues6, yerr = stdErrors6, color = 'y', label = pValue6)
     barPlots[5].errorbar(xlabels, barMeanValues6, yerr = stdErrors6, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black')
     barPlots[5].set_title(filesDict['name6'], fontsize = barLabelsFontSize)
     barPlots[5].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[5].plot(xlabels, dataPlot6, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     #plt.ylim(100, 800)
     plt.suptitle(scatBarDict['title'], fontsize = barLabelsFontSize)
     barPlots[2].legend(prop ={"size":10})
     barPlots[3].legend(prop ={"size":10})
     barPlots[4].legend(prop ={"size":10})
     barPlots[5].legend(prop ={"size":10})
     #plt.xlabel("common X", loc = 'center')
     #plt.savefig(scatBarDict['savedName'], format = 'pdf', dpi =50)
     plt.show() 
     return(plt.show()) 


def  pupilDilation_time(timeData1, plotData1, timeData2, plotData2, timeData3, plotData3): 
     fig, signalsPlots = plt.subplots(1,3, constrained_layout = True, sharey = True, sharex = True) 
     signalsPlots[0].plot(timeData1, plotData1) 
     signalsPlots[0].set(title = 'Positive control') 
     signalsPlots[0].set_ylabel('Pupil Area', fontsize = 13)
     signalsPlots[1].plot(timeData2, plotData2) 
     signalsPlots[1].set(title = 'Negative control')
     signalsPlots[1].set_xlabel('Time(s)', fontsize = 13)
     signalsPlots[2].plot(timeData3, plotData3) 
     signalsPlots[2].set(title = 'chordTrain')
     plt.suptitle('Average trials behavior in time window: pure001_20210928')
     plt.show() 
     return(plt.show())

def calculate_pupil_size_and_plot(normValue1, normValue2, normValue3, normValue4, normValue5, normValue6, normValue7, normValue8, normValue9, normValue10,  normValue1a, normValue2a, normValue3a, normValue4a, normValue5a, normValue6a, normValue7a, normValue8a, normValue9a, normValue10a, normValue1b, normValue2b, normValue3b, normValue4b, normValue5b, normValue6b, normValue7b, normValue8b, normValue9b, normValue10b, normValue1c, normValue2c, normValue3c, normValue4c, normValue5c, normValue6c, normValue7c, normValue8c, normValue9c, normValue10c,  normValue1d, normValue2d, normValue3d, normValue4d, normValue5d, normValue6d, normValue7d, normValue8d, normValue9d, normValue10d, normValue1e, normValue2e, normValue3e, normValue4e, normValue5e, normValue6e, normValue7e, normValue8e, normValue9e, normValue10e, normPreVal1, normPreVal1a, normPreVal1b, normPreVal1c, normPreVal1d, normPreVal1e, normPreVal2, normPreVal2a, normPreVal2b, normPreVal2c, normPreVal2d, normPreVal2e, frequencies):
     
     values2Khz1 = np.concatenate((normValue1, normValue1a, normValue1b, normValue1c, normValue1d, normValue1e), axis = 0)
     values4Khz1 = np.concatenate((normValue2, normValue2a, normValue2b, normValue2c, normValue2d, normValue2e), axis = 0)
     values8Khz1 = np.concatenate((normValue3, normValue3a, normValue3b, normValue3c, normValue3d, normValue3e), axis = 0)
     values16Khz1 = np.concatenate((normValue4, normValue4a, normValue4b, normValue4c, normValue4d, normValue4e), axis = 0)
     values32Khz1 = np.concatenate((normValue5, normValue5a, normValue5b, normValue5c, normValue5d, normValue5e), axis = 0)
     values2Khz2 = np.concatenate((normValue6, normValue6a, normValue6b, normValue6c, normValue6d, normValue6e), axis = 0)
     values4Khz2 = np.concatenate((normValue7, normValue7a, normValue7b, normValue7c, normValue7d, normValue7e), axis = 0)
     values8Khz2 = np.concatenate((normValue8, normValue8a, normValue8b, normValue8c, normValue8d, normValue8e), axis = 0)
     values16Khz2 = np.concatenate((normValue9, normValue9a, normValue9b, normValue9c, normValue9d, normValue9e), axis = 0)
     values32Khz2 = np.concatenate((normValue10, normValue10a, normValue10b, normValue10c, normValue10d, normValue10e), axis = 0)
     pre2Khz = np.concatenate((normPreVal1, normPreVal1a, normPreVal1b, normPreVal1c, normPreVal1d, normPreVal1e), axis = 0)
     pre32Khz = np.concatenate((normPreVal2, normPreVal2a, normPreVal2b, normPreVal2c, normPreVal2d, normPreVal2e), axis = 0)
     
     mean2Khz1 = np.average(values2Khz1)
     mean4Khz1 = np.average(values4Khz1)
     mean8Khz1 = np.average(values8Khz1)
     mean16Khz1 = np.average(values16Khz1)
     mean32Khz1 = np.average(values32Khz1)
     mean2Khz2 = np.average(values2Khz2)
     mean4Khz2 = np.average(values4Khz2)
     mean8Khz2 = np.average(values8Khz2)
     mean16Khz2 = np.average(values16Khz2)
     mean32Khz2 = np.average(values32Khz2)
     meanPre2Khz = np.average(pre2Khz)
     meanPre32Khz = np.average(pre32Khz)
     
     round2Khz1 = np.around(mean2Khz1, decimals = 3)
     round4Khz1 = np.round(mean4Khz1, decimals = 3)
     round8Khz1 = np.round(mean8Khz1, decimals = 3)
     round16Khz1 = np.round(mean16Khz1, decimals = 3)
     round32Khz1 = np.round(mean32Khz1, decimals = 3)
     round2Khz2 = np.round(mean2Khz2, decimals = 3)
     round4Khz2 = np.round(mean4Khz2, decimals = 3)
     round8Khz2 = np.round(mean8Khz2, decimals = 3)
     round16Khz2 = np.round(mean16Khz2, decimals = 3)
     round32Khz2 = np.round(mean32Khz2, decimals = 3)
     roundPre2Khz = np.round(meanPre2Khz, decimals = 3)
     roundPre32Khz = np.round(meanPre32Khz, decimals = 3)
     
     err2Khz1 = np.std(values2Khz1)
     err4Khz1 = np.std(values4Khz1)
     err8Khz1 = np.std(values8Khz1)
     err16Khz1 = np.std(values16Khz1)
     err32Khz1 = np.std(values32Khz1)
     err2Khz2 = np.std(values2Khz2)
     err4Khz2 = np.std(values4Khz2)
     err8Khz2 = np.std(values8Khz2)
     err16Khz2 = np.std(values16Khz2)
     err32Khz2 = np.std(values32Khz2)
     totalErr1 = [err2Khz1, err4Khz1, err8Khz1, err16Khz1, err32Khz1]
     totalErr2 = [err2Khz2, err4Khz2, err8Khz2, err16Khz2, err32Khz2]
     totalMean1 = [round2Khz1, round4Khz1, round8Khz1, round16Khz1, round32Khz1]
     totalMean2 = [round2Khz2, round4Khz2, round8Khz2, round16Khz2, round32Khz2]
     
# --- Delta pupil area ---
     pArea2Khz1 = mean2Khz1 - meanPre2Khz
     pArea4Khz1 = mean4Khz1 - meanPre2Khz
     pArea8Khz1 = mean8Khz1 - meanPre2Khz
     pArea16Khz1 = mean16Khz1 - meanPre2Khz
     pArea32Khz1 = mean32Khz1 - meanPre2Khz
     
     pArea2Khz2 = mean2Khz2 - meanPre32Khz
     pArea4Khz2 = mean4Khz2 - meanPre32Khz
     pArea8Khz2 = mean8Khz2 - meanPre32Khz
     pArea16Khz2 = mean16Khz2 - meanPre32Khz
     pArea32Khz2 = mean32Khz2 - meanPre32Khz
    
     values2Khz = np.array([pArea2Khz1, pArea4Khz1, pArea8Khz1, pArea16Khz1, pArea32Khz1])
     values32Khz = np.array([pArea2Khz2, pArea4Khz2, pArea8Khz2, pArea16Khz2, pArea32Khz2])
     mean2Khz = [mean2Khz1, mean4Khz1, mean8Khz1, mean16Khz1, mean32Khz1]
     mean32Khz = [mean2Khz2, mean4Khz2, mean8Khz2, mean16Khz2, mean32Khz2]
     
     preValPlot2 = [meanPre2Khz]
     preXPlot2 = frequencies[0]
     preValPlot32 = [meanPre32Khz]
     preXplot32 = frequencies[4]
     firstLegend = 'mean pre P. 2kHz Value', roundPre2Khz
     secondLegend = 'mean pre P. 32kHz Value', roundPre32Khz
     ylimArr = [np.nanmin(values2Khz), np.nanmin(values32Khz)]
     ylimInf = np.nanmin(ylimArr)
     ymaxArr = [np.nanmax(values2Khz), np.nanmax(values32Khz)]
     ymaxSup = np.nanmax(ymaxArr)
     
     
     labelSize = 16 
     fig, plotVal = plt.subplots(2,2, constrained_layout = True, sharex= True) 
     fig.set_size_inches(9.5, 7.5, forward = True)
     
     plotVal[0,0].set_title('Pupil behavior for 2kHz', fontsize = labelSize)
     plotVal[0,0].set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
     plotVal[0,0].plot(frequencies, mean2Khz, color = '#000000', marker = '^', markersize = '9')  #add label = firstLegend and comment line 913 for test1.png
     plotVal[0,0].plot(preXPlot2, preValPlot2, color ='r', marker ='o', label = firstLegend)
     plotVal[0,0].errorbar(frequencies, totalMean1, yerr = totalErr1, fmt='none', capsize=3.5, color = '#000000', alpha = 0.5)
     plotVal[0,0].tick_params(axis='y', labelsize=labelSize)
     plotVal[1,0].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1,0].plot(frequencies, mean32Khz, color = '#FFA500', marker = '^', markersize = '9') # add label = secondLegend and comment line 917 for test1.png
     plotVal[1,0].plot(preXplot32, preValPlot32, color ='r', marker ='o', markersize = '9', label = secondLegend)
     plotVal[1,0].errorbar(frequencies, totalMean2, yerr = totalErr2, fmt='none', capsize=3.5, color = '#FFA500', alpha = 0.5) 
     plotVal[1,0].tick_params(axis='x', labelsize=labelSize)
     plotVal[1,0].tick_params(axis='y', labelsize=labelSize)
     plotVal[1,0].set_title('Pupil behavior for 32kHz', fontsize = labelSize)
     plotVal[1,0].title.set_text('Pupil behavior for 32kHz')
     plotVal[0,1].set_title('Pupil behavior for 2kHz', fontsize = labelSize)
     plotVal[0,1].set_ylabel('Δ Mean pupil area (Normalized)', fontsize = labelSize) 
     plotVal[0,1].plot(frequencies, values2Khz, color = '#000000', marker = '^', markersize = '9', label = firstLegend)
     plotVal[0,1].tick_params(axis='y', labelsize=labelSize)
     plotVal[1,1].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1,1].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1,1].plot(frequencies, values32Khz, color = '#FFA500', marker = '^', markersize = '9', label = secondLegend)
     plotVal[1,1].tick_params(axis='x', labelsize=labelSize)
     plotVal[1,1].set_title('Pupil behavior for 32kHz', fontsize = labelSize)
     plotVal[1,1].title.set_text('Pupil behavior for 32kHz')
     
     plotVal[0,0].text(frequencies[0], mean2Khz[0], round2Khz1, horizontalalignment='right')
     plotVal[0,0].text(frequencies[1], mean2Khz[1], round4Khz1)
     plotVal[0,0].text(frequencies[2], mean2Khz[2], round8Khz1)
     plotVal[0,0].text(frequencies[3], mean2Khz[3], round16Khz1)
     plotVal[0,0].text(frequencies[4], mean2Khz[4], round32Khz1)
     plotVal[1,0].text(frequencies[0], mean32Khz[0], round2Khz2)
     plotVal[1,0].text(frequencies[1], mean32Khz[1], round4Khz2)
     plotVal[1,0].text(frequencies[2], mean32Khz[2], round8Khz2)
     plotVal[1,0].text(frequencies[3], mean32Khz[3], round16Khz2)
     plotVal[1,0].text(frequencies[4], mean32Khz[4], round32Khz2)
     plotVal[0,1].text(frequencies[0], values2Khz[0], np.around(pArea2Khz1, decimals =3), horizontalalignment='right')
     plotVal[0,1].text(frequencies[1], values2Khz[1], np.around(pArea4Khz1, decimals =3), horizontalalignment='right')
     plotVal[0,1].text(frequencies[2], values2Khz[2], np.around(pArea8Khz1, decimals =3))
     plotVal[0,1].text(frequencies[3], values2Khz[3], np.around(pArea16Khz1, decimals =3))
     plotVal[0,1].text(frequencies[4], values2Khz[4], np.around(pArea32Khz1, decimals =3))
     plotVal[1,1].text(frequencies[0], values32Khz[0], np.around(pArea2Khz2, decimals =3))
     plotVal[1,1].text(frequencies[1], values32Khz[1], np.around(pArea4Khz2, decimals =3))
     plotVal[1,1].text(frequencies[2], values32Khz[2], np.around(pArea8Khz2, decimals =3))
     plotVal[1,1].text(frequencies[3], values32Khz[3], np.around(pArea16Khz2, decimals =3))
     plotVal[1,1].text(frequencies[4], values32Khz[4], np.around(pArea32Khz2, decimals =3))
     
     
     '''
     plotVal[0].set_title('Pupil behavior for 2kHz', fontsize = labelSize)
     plotVal[0].set_ylabel('Δ Mean pupil area (Normalized)', fontsize = labelSize) 
     plotVal[0].plot(frequencies, values2Khz, color = '#000000', marker = '^', markersize = '5', label = firstLegend)
     plotVal[0].tick_params(axis='y', labelsize=labelSize)
     plotVal[1].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1].plot(frequencies, values32Khz, color = '#FFA500', marker = '^', markersize = '5', label = secondLegend)
     plotVal[1].tick_params(axis='x', labelsize=labelSize)
     plotVal[1].set_title('Pupil behavior for 32kHz', fontsize = labelSize)
     plotVal[1].title.set_text('Pupil behavior for 32kHz')
     
     plotVal[0].text(frequencies[0], values2Khz[0], np.around(pArea2Khz2, decimals =3), horizontalalignment='right')
     plotVal[0].text(frequencies[1], values2Khz[1], np.around(pArea4Khz2, decimals =3), horizontalalignment='right')
     plotVal[0].text(frequencies[2], values2Khz[2], np.around(pArea8Khz2, decimals =3))
     plotVal[0].text(frequencies[3], values2Khz[3], np.around(pArea16Khz2, decimals =3))
     plotVal[0].text(frequencies[4], values2Khz[4], np.around(pArea32Khz2, decimals =3))
     plotVal[1].text(frequencies[0], values32Khz[0], np.around(pArea2Khz32, decimals =3))
     plotVal[1].text(frequencies[1], values32Khz[1], np.around(pArea4Khz32, decimals =3))
     plotVal[1].text(frequencies[2], values32Khz[2], np.around(pArea8Khz32, decimals =3))
     plotVal[1].text(frequencies[3], values32Khz[3], np.around(pArea16Khz32, decimals =3))
     plotVal[1].text(frequencies[4], values32Khz[4], np.around(pArea32Khz32, decimals =3))
     '''
     '''
# --- Create plots such as test1..4.png sent on apr 27 ---
     plotVal[0].set_title('Pupil behavior for 2kHz', fontsize = labelSize)
     plotVal[0].set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
     plotVal[0].plot(frequencies, mean2Khz, color = '#000000', marker = '^', markersize = '5') # add label = firstLegend and comment line 913 for test1.png
     plotVal[0].plot(preXPlot2, preValPlot2, color ='r', marker ='o', label = firstLegend)
     plotVal[0].errorbar(frequencies, totalMean1, yerr = totalErr1, fmt='none', capsize=3.5, color = '#000000', alpha = 0.5)
     plotVal[0].tick_params(axis='y', labelsize=labelSize)
     plotVal[1].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1].plot(frequencies, mean32Khz, color = '#FFA500', marker = '^', markersize = '5') # add label = secondLegend and comment line 917 for test1.png
     plotVal[1].plot(preXplot32, preValPlot32, color ='r', marker ='o', label = secondLegend)
     plotVal[1].errorbar(frequencies, totalMean2, yerr = totalErr2, fmt='none', capsize=3.5, color = '#FFA500', alpha = 0.5) 
     plotVal[1].tick_params(axis='x', labelsize=labelSize)
     plotVal[1].set_title('Pupil behavior for 32kHz', fontsize = labelSize)
     plotVal[1].title.set_text('Pupil behavior for 32kHz')
     
     plotVal[0].text(frequencies[0], mean2Khz[0], round2Khz1, horizontalalignment='right')
     plotVal[0].text(frequencies[1], mean2Khz[1], round4Khz1)
     plotVal[0].text(frequencies[2], mean2Khz[2], round8Khz1)
     plotVal[0].text(frequencies[3], mean2Khz[3], round16Khz1)
     plotVal[0].text(frequencies[4], mean2Khz[4], round32Khz1)
     plotVal[1].text(frequencies[0], mean32Khz[0], round2Khz2)
     plotVal[1].text(frequencies[1], mean32Khz[1], round4Khz2)
     plotVal[1].text(frequencies[2], mean32Khz[2], round8Khz2)
     plotVal[1].text(frequencies[3], mean32Khz[3], round16Khz2)
     plotVal[1].text(frequencies[4], mean32Khz[4], round32Khz2)
     ''' 
     plotVal[0,0].grid(b = True)
     plotVal[0,1].grid(b = True)
     plotVal[1,0].grid(b = True)
     plotVal[1,1].grid(b = True)
     plt.suptitle(scatBarDict['plotFreqName'], fontsize = labelSize)
     plt.xticks(fontsize = labelSize) 
     plt.yticks(fontsize = labelSize)
     plt.yticks(fontsize = labelSize)
     plotVal[0,1].set_ylim([-0.020, 0.010])
     plotVal[1,1].set_ylim([-0.020, 0.010])
     plotVal[0,0].legend(prop ={"size":10})
     plotVal[0,1].legend(prop ={"size":10})
     plotVal[1,0].legend(prop ={"size":10})
     plotVal[1,1].legend(prop ={"size":10})
     plt.show() 
     
     return(plt.show())


filesDict = {'loadFile1':np.load('./project_videos/mp4Files/mp4Outputs/pure010_20220415_xtremes_195_xconfig1_proc.npy', allow_pickle = True).item(),
	'sessionFile1':'20220415_xtremes_195_xconfig1', 'condition1':'detectiongonogo', 'sound':'ChordTrain', 'name1':'pure010', 
	'loadFile2':np.load('./project_videos/mp4Files/mp4Outputs/pure010_20220418_xtremes_196_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config2':'2Sconfig3', 'sessionFile2':'20220418_xtremes_196_xconfig1', 'name2':'config12_2',
	'loadFile3':np.load('./project_videos/mp4Files/mp4Outputs/pure010_20220418_xtremes_197_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config3':'2Sconfig3', 'sessionFile3':'20220418_xtremes_197_xconfig1', 'name3':'config12_3',
	'loadFile4':np.load('./project_videos/mp4Files/mp4Outputs/pure010_20220420_xtremes_201_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config4':'2Sconfig4', 'sessionFile4':'20220420_xtremes_201_xconfig1', 'name4':'config14_1', 
	'loadFile5':np.load('./project_videos/mp4Files/mp4Outputs/pure010_20220421_xtremes_202_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config5':'2Sconfig4', 'sessionFile5':'20220421_xtremes_202_xconfig1', 'name5':'config14_2', 
	'loadFile6':np.load('./project_videos/mp4Files/mp4Outputs/pure010_20220421_xtremes_203_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config6':'2Sconfig4', 'sessionFile6':'20220421_xtremes_203_xconfig1', 'name6':'config14_3'}
	

scatBarDict = {'title':'Pupil behavior before and after sound stimulus: pure011 20220419', 'savedName':'pure0043ScatbarPlot', 'yLabel':'Mean Pupil Area', 'xLabelTitle':'Conditions', 'plotFreqName':'Pupil size for 5 different frequencies: pure010_20220418-21'}

subject = filesDict['name1']
paradigm = filesDict['condition1']
session = filesDict['sessionFile1']

behavFile = loadbehavior.path_to_behavior_data(subject, paradigm, session)
bdata = loadbehavior.BehaviorData(behavFile)
preFreqs = bdata['preFreq'] 
postFreqs = bdata['postFreq'] 


subject2 = filesDict['name1']
paradigm2 = filesDict['condition1']
session2 = filesDict['sessionFile2']

behavFile2 = loadbehavior.path_to_behavior_data(subject2, paradigm2, session2)
bdata2 = loadbehavior.BehaviorData(behavFile2)
preFreqs2 = bdata2['preFreq'] 
postFreqs2 = bdata2['postFreq'] 


subject3 = filesDict['name1']
paradigm3 = filesDict['condition1']
session3 = filesDict['sessionFile3']

behavFile3 = loadbehavior.path_to_behavior_data(subject3, paradigm3, session3)
bdata3 = loadbehavior.BehaviorData(behavFile3)
preFreqs3 = bdata3['preFreq'] 
postFreqs3 = bdata3['postFreq'] 


subject4 = filesDict['name1']
paradigm4 = filesDict['condition1']
session4 = filesDict['sessionFile4']

behavFile4 = loadbehavior.path_to_behavior_data(subject4, paradigm4, session4)
bdata4 = loadbehavior.BehaviorData(behavFile4)
preFreqs4 = bdata4['preFreq'] 
postFreqs4 = bdata4['postFreq'] 


subject5 = filesDict['name1']
paradigm5 = filesDict['condition1']
session5 = filesDict['sessionFile5']

behavFile5 = loadbehavior.path_to_behavior_data(subject5, paradigm5, session5)
bdata5 = loadbehavior.BehaviorData(behavFile5)
preFreqs5 = bdata5['preFreq'] 
postFreqs5 = bdata5['postFreq'] 


subject6 = filesDict['name1']
paradigm6 = filesDict['condition1']
session6 = filesDict['sessionFile6']

behavFile6 = loadbehavior.path_to_behavior_data(subject6, paradigm6, session6)
bdata6 = loadbehavior.BehaviorData(behavFile6)
preFreqs6 = bdata6['preFreq'] #works with modified detectiongonogo paradigm
postFreqs6 = bdata6['postFreq'] #works with modified detectiongonogo paradigm

frequenciesTested = np.array([2, 4, 8, 16, 32])
frequenciesTestedArr = np.array([[2, 2, 4, 4, 8], [8, 16, 16, 32, 32]])




#list(map(tuple, np.where(np.isnan(pAreaDilatedMean4)))) --> finds NaN's within an array
#a = pAreaDilatedMean4[np.isfinite(pAreaDilatedMean4)] --> allows to eliminate NaN's

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
blink2Bool = np.logical_and(blink2 > minBlink, blink2 < maxBlink) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRange = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal, postSignal = find_prepost_values(windowTimeVec, windowed_signal, -0.5, 0, 1.4, 2.0)
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']



#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([-7, 7])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)
pAreaDilatedMean = pAreaDilated.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value config12_1', wstat,',',  'P-value config12_1', pval )

#prefreqValues1, prefreqValues2, prefreqValues3, prefreqValues4, prefreqValues5 = freqs_gonogo(preSignal, postFreqs, 2000, 4000, 8000, 16000, 32000)

#postfreqValues1, postfreqValues2, postfreqValues3, postfreqValues4, postfreqValues5 = freqs_gonogo(postSignal, postFreqs, 2000, 4000, 8000, 16000, 32000) #works with modified detectiongonogo paradigm

freq1Index2Kz, freq1Index32Kz, freq2Index2Kz, freq2Index32Kz, freq3Index2Kz, freq3Index32Kz, freq4Index2Kz, freq4Index32Kz, freq5Index2Kz, freq5Index32Kz, preSignalValues2Kz, preSignalValues32Kz = find_freqs_indices(preFreqs, postFreqs, 2000, 4000, 8000, 16000, 32000)


values2Kz1, values4Kz1, values8Kz1, values16Kz1, values32Kz1, values2Kz2, values4Kz2, values8Kz2, values16Kz2, values32Kz2, pre2KzValues, pre32KzValues = find_prepost_freqs_values(preSignal, postSignal, freq1Index2Kz, freq1Index32Kz, freq2Index2Kz, freq2Index32Kz, freq3Index2Kz, freq3Index32Kz, freq4Index2Kz, freq4Index32Kz, freq5Index2Kz, freq5Index32Kz, preSignalValues2Kz, preSignalValues32Kz)


preFreqVal2kz1, preFreqVal4kz1, preFreqVal8kz1, preFreqVal16kz1, preFreqVal32kz1, postFreqVal2kz1, postFreqVal4kz1, postFreqVal8kz1, postFreqVal16kz1, postFreqVal32kz1,  preFreqVal2kz2, preFreqVal4kz2, preFreqVal8kz2, preFreqVal16kz2, preFreqVal32kz2, postFreqVal2kz2, postFreqVal4kz2, postFreqVal8kz2, postFreqVal16kz2, postFreqVal32kz2 = indices_values_each_freq(averagePreSignal, averagePostSignal, freq1Index2Kz, freq2Index2Kz, freq3Index2Kz, freq4Index2Kz, freq5Index2Kz, freq1Index32Kz, freq2Index32Kz, freq3Index32Kz, freq4Index32Kz, freq5Index32Kz)
















proc1 = filesDict['loadFile2']

#---obtain pupil data---
pupil1 = proc1['pupil'][0] # Dic.
pArea1 = pupil1['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink1a = proc1['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink11 = proc1['blink']   # List.
blink21 = np.array(blink1a).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
minBlink1 = np.amin(blink21)
maxBlink1 = np.amax(blink21) - minBlink1
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
timeOfBlink2Event1 = timeOfBlink2Event1[1:-1]

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
timeRangeForPupilDilation1 = np.array([-7, 7])
pupilDilationTimeWindowVec1, pAreaDilated1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRangeForPupilDilation1)
pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat1, pval1 = stats.wilcoxon(averagePreSignal1, averagePostSignal1)
print('Wilcoxon value config12_2', wstat1,',',  'P-value config12_2', pval1 )

prefreqValues1a, prefreqValues2a, prefreqValues3a, prefreqValues4a, prefreqValues5a = freqs_gonogo(preSignal1, postFreqs2, 2000, 4000, 8000, 16000, 32000) # works with modified detectiongonogo paradigm

postfreqValues1a, postfreqValues2a, postfreqValues3a, postfreqValues4a, postfreqValues5a = freqs_gonogo(postSignal1, postFreqs2, 2000, 4000, 8000, 16000, 32000) #works with modified detectiongonogo paradigm

freq1Index2Kza, freq1Index32Kza, freq2Index2Kza, freq2Index32Kza, freq3Index2Kza, freq3Index32Kza, freq4Index2Kza, freq4Index32Kza, freq5Index2Kza, freq5Index32Kza, preSignalValues2Kza, preSignalValues32Kza = find_freqs_indices(preFreqs2, postFreqs2, 2000, 4000, 8000, 16000, 32000)



values2Kz1a, values4Kz1a, values8Kz1a, values16Kz1a, values32Kz1a, values2Kz2a, values4Kz2a, values8Kz2a, values16Kz2a, values32Kz2a, pre2KzValuesa, pre32KzValuesa = find_prepost_freqs_values(preSignal1, postSignal1, freq1Index2Kza, freq1Index32Kza, freq2Index2Kza, freq2Index32Kza, freq3Index2Kza, freq3Index32Kza, freq4Index2Kza, freq4Index32Kza, freq5Index2Kza, freq5Index32Kza, preSignalValues2Kza, preSignalValues32Kza)

#trials2Kz1a, trials4Kz1a, trials8Kz1a, trials16Kz1a, trials32Kz1a, trials2Kz2a, trials4Kz2a, trials8Kz2a, trials16Kz2a, trials32Kz2a, preTrials2kza, preTrials32Kza = find_averagePupil_values(averagePreSignal1, averagePostSignal1, freq1Index2Kza, freq1Index32Kza, freq2Index2Kza, freq2Index32Kza, freq3Index2Kza, freq3Index32Kza, freq4Index2Kza, freq4Index32Kza, freq5Index2Kza, freq5Index32Kza, preSignalValues2Kza, preSignalValues32Kza)













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
blink2Bool2 = np.logical_and(blink22 > minBlink2, blink22 < maxBlink2) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRange2 = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec2, windowed_signal2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRange2)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal2, postSignal2 = find_prepost_values(windowTimeVec2, windowed_signal2, -0.5, 0, 1.4, 2.0)
averagePreSignal2 = preSignal2.mean(axis = 0)
averagePostSignal2 = postSignal2.mean(axis = 0)
dataToPlot2 = [averagePreSignal2, averagePostSignal2]
xlabels2 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation2 = np.array([-7, 7])
pupilDilationTimeWindowVec2, pAreaDilated2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRangeForPupilDilation2)
pAreaDilatedMean2 = pAreaDilated2.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat2, pval2 = stats.wilcoxon(averagePreSignal2, averagePostSignal2)
print('Wilcoxon value config12_3', wstat2,',',  'P-value config12_3', pval2 )

prefreqValues1b, prefreqValues2b, prefreqValues3b, prefreqValues4b, prefreqValues5b = freqs_gonogo(preSignal2, postFreqs3, 2000, 4000, 8000, 16000, 32000) # works with modified detectiongonogo paradigm

postfreqValues1b, postfreqValues2b, postfreqValues3b, postfreqValues4b, postfreqValues5b = freqs_gonogo(postSignal2, postFreqs3, 2000, 4000, 8000, 16000, 32000) #works with modified detectiongonogo paradigm

freq1Index2Kzb, freq1Index32Kzb, freq2Index2Kzb, freq2Index32Kzb, freq3Index2Kzb, freq3Index32Kzb, freq4Index2Kzb, freq4Index32Kzb, freq5Index2Kzb, freq5Index32Kzb, preSignalValues2Kzb, preSignalValues32Kzb = find_freqs_indices(preFreqs3, postFreqs3, 2000, 4000, 8000, 16000, 32000)


values2Kz1b, values4Kz1b, values8Kz1b, values16Kz1b, values32Kz1b, values2Kz2b, values4Kz2b, values8Kz2b, values16Kz2b, values32Kz2b, pre2KzValuesb, pre32KzValuesb = find_prepost_freqs_values(preSignal2, postSignal2, freq1Index2Kzb, freq1Index32Kzb, freq2Index2Kzb, freq2Index32Kzb, freq3Index2Kzb, freq3Index32Kzb, freq4Index2Kzb, freq4Index32Kzb, freq5Index2Kzb, freq5Index32Kzb, preSignalValues2Kzb, preSignalValues32Kzb)

#trials2Kz1b, trials4Kz1b, trials8Kz1b, trials16Kz1b, trials32Kz1b, trials2Kz2b, trials4Kz2b, trials8Kz2b, trials16Kz2b, trials32Kz2b, preTrials2kzb, preTrials32Kzb = find_averagePupil_values(averagePreSignal2, averagePostSignal2, freq1Index2Kzb, freq1Index32Kzb, freq2Index2Kzb, freq2Index32Kzb, freq3Index2Kzb, freq3Index32Kzb, freq4Index2Kzb, freq4Index32Kzb, freq5Index2Kzb, freq5Index32Kzb, preSignalValues2Kzb, preSignalValues32Kzb)















proc3 = filesDict['loadFile4']
#---obtain pupil data---
pupil3 = proc3['pupil'][0] # Dic.
pArea3 = pupil3['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.

blink3 = proc3['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink13 = proc3['blink']   # List.
blink23 = np.array(blink3).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minBlink3 = np.amin(blink23)
maxBlink3 = np.amax(blink23) - minBlink3
blink2Bool3 = np.logical_and(blink23 > minBlink3, blink23 < maxBlink3)# Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues3 = np.diff(blink2Bool3) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal3 = np.flatnonzero(blink2RangeValues3) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#---calculate number of frames, frame rate, and time vector---
nframes3 = len(pArea3) # Contains length of pArea variable (equivalent to the blink variable).
frameVec3 = np.arange(0, nframes3, 1) # Vector of the total frames from the video.
framerate3 = 30 # frame rate of video
timeVec3 = (frameVec3 * 1)/framerate3 # Time Vector to calculate the length of the video.

#--- obtaining onset sync signal values ---
syncOnsetValues3 = onset_values(indicesValueSyncSignal3)
timeOfBlink2Event3 = timeVec3[syncOnsetValues3] # Provides the time values in which the sync signal is on.
timeOfBlink2Event3 = timeOfBlink2Event3[1:-1]

#--- Align trials to the event ---
timeRange3 = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec3, windowed_signal3 = eventlocked_signal(timeVec3, pArea3, timeOfBlink2Event3, timeRange3)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal3, postSignal3 = find_prepost_values(windowTimeVec3, windowed_signal3, -0.5, 0, 1.4, 2.0)
averagePreSignal3 = preSignal3.mean(axis = 0)
averagePostSignal3 = postSignal3.mean(axis = 0)
dataToPlot3 = [averagePreSignal3, averagePostSignal3]
xlabels3 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation3 = np.array([-7, 7])
pupilDilationTimeWindowVec3, pAreaDilated3 = eventlocked_signal(timeVec3, pArea3, timeOfBlink2Event3, timeRangeForPupilDilation3)
pAreaDilatedMean3 = pAreaDilated3.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat3, pval3 = stats.wilcoxon(averagePreSignal3, averagePostSignal3)
print('Wilcoxon value config12_4', wstat3,',',  'P-value config12_4', pval3 )

                                                
freq1Index2Kzc, freq1Index32Kzc, freq2Index2Kzc, freq2Index32Kzc, freq3Index2Kzc, freq3Index32Kzc, freq4Index2Kzc, freq4Index32Kzc, freq5Index2Kzc, freq5Index32Kzc, preSignalValues2Kzc, preSignalValues32Kzc = find_freqs_indices(preFreqs4, postFreqs4, 2000, 4000, 8000, 16000, 32000)


values2Kz1c, values4Kz1c, values8Kz1c, values16Kz1c, values32Kz1c, values2Kz2c, values4Kz2c, values8Kz2c, values16Kz2c, values32Kz2c, pre2KzValuesc, pre32KzValuesc = find_prepost_freqs_values(preSignal3, postSignal3, freq1Index2Kzc, freq1Index32Kzc, freq2Index2Kzc, freq2Index32Kzc, freq3Index2Kzc, freq3Index32Kzc, freq4Index2Kzc, freq4Index32Kzc, freq5Index2Kzc, freq5Index32Kzc, preSignalValues2Kzc, preSignalValues32Kzc)
                                                
#trials2Kz1c, trials4Kz1c, trials8Kz1c, trials16Kz1c, trials32Kz1c, trials2Kz2c, trials4Kz2c, trials8Kz2c, trials16Kz2c, trials32Kz2c, preTrials32kzc, preTrials2Kzc = find_averagePupil_values(averagePreSignal3, averagePostSignal3, freq1Index2Kzc, freq1Index32Kzc, freq2Index2Kzc, freq2Index32Kzc, freq3Index2Kzc, freq3Index32Kzc, freq4Index2Kzc, freq4Index32Kzc, freq5Index2Kzc, freq5Index32Kzc, preSignalValues32Kzc, preSignalValues2Kzc)                                          
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
proc4 = filesDict['loadFile5']

#---obtain pupil data---
pupil4 = proc4['pupil'][0] # Dic.
pArea4 = pupil4['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink4 = proc4['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink14 = proc4['blink']   # List.
blink24 = np.array(blink4).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minBlink4 = np.amin(blink24)
maxBlink4 = np.amax(blink24) - minBlink4
blink2Bool4 = np.logical_and(blink24 > minBlink4, blink24 < maxBlink4) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues4 = np.diff(blink2Bool4) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal4 = np.flatnonzero(blink2RangeValues4) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#---calculate number of frames, frame rate, and time vector---
nframes4 = len(pArea4) # Contains length of pArea variable (equivalent to the blink variable).
frameVec4 = np.arange(0, nframes4, 1) # Vector of the total frames from the video.
framerate4 = 30 # frame rate of video
timeVec4 = (frameVec4 * 1)/framerate4 # Time Vector to calculate the length of the video.

#--- obtaining onset sync signal values ---
syncOnsetValues4 = onset_values(indicesValueSyncSignal4)
timeOfBlink2Event4 = timeVec4[syncOnsetValues4] # Provides the time values in which the sync signal is on.
timeOfBlink2Event4 = timeOfBlink2Event4[1:-1]

#--- Align trials to the event ---
timeRange4 = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec4, windowed_signal4 = eventlocked_signal(timeVec4, pArea4, timeOfBlink2Event4, timeRange4)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal4, postSignal4 = find_prepost_values(windowTimeVec4, windowed_signal4, -0.5, 0, 1.4, 2.0)
averagePreSignal4 = preSignal4.mean(axis = 0)
averagePostSignal4 = postSignal4.mean(axis = 0)
dataToPlot4 = [averagePreSignal4, averagePostSignal4]
xlabels4 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation4 = np.array([-7, 7])
pupilDilationTimeWindowVec4, pAreaDilated4 = eventlocked_signal(timeVec4, pArea4, timeOfBlink2Event4, timeRangeForPupilDilation4)
pAreaDilatedMean4 = pAreaDilated4.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat4, pval4 = stats.wilcoxon(averagePreSignal4, averagePostSignal4)
print('Wilcoxon value config12_5', wstat4,',',  'P-value config12_5', pval4)                                                
                                                
                                                
freq1Index2Kzd, freq1Index32Kzd, freq2Index2Kzd, freq2Index32Kzd, freq3Index2Kzd, freq3Index32Kzd, freq4Index2Kzd, freq4Index32Kzd, freq5Index2Kzd, freq5Index32Kzd, preSignalValues2Kzd, preSignalValues32Kzd = find_freqs_indices(preFreqs5, postFreqs5, 2000, 4000, 8000, 16000, 32000)


values2Kz1d, values4Kz1d, values8Kz1d, values16Kz1d, values32Kz1d, values2Kz2d, values4Kz2d, values8Kz2d, values16Kz2d, values32Kz2d, pre2KzValuesd, pre32KzValuesd = find_prepost_freqs_values(preSignal4, postSignal4, freq1Index2Kzd, freq1Index32Kzd, freq2Index2Kzd, freq2Index32Kzd, freq3Index2Kzd, freq3Index32Kzd, freq4Index2Kzd, freq4Index32Kzd, freq5Index2Kzd, freq5Index32Kzd, preSignalValues2Kzd, preSignalValues32Kzd)                         
                         
#trials2Kz1d, trials4Kz1d, trials8Kz1d, trials16Kz1d, trials32Kz1d, trials2Kz2d, trials4Kz2d, trials8Kz2d, trials16Kz2d, trials32Kz2d, preTrials32kzd, preTrials2Kzd = find_averagePupil_values(averagePreSignal4, averagePostSignal4, freq1Index2Kzd, freq1Index32Kzd, freq2Index2Kzd, freq2Index32Kzd, freq3Index2Kzd, freq3Index32Kzd, freq4Index2Kz, freq4Index32Kzd, freq5Index2Kzd, freq5Index32Kzd, preSignalValues32Kzd, preSignalValues2Kzd)                   
                         
                         
                         
                         
                         
                         
                         
                         
                         
proc5 = filesDict['loadFile6']
#---obtain pupil data---
pupil5 = proc5['pupil'][0] # Dic.
pArea5 = pupil5['area'] # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink5 = proc5['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink15 = proc5['blink']   # List.
blink25 = np.array(blink5).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minBlink5 = np.amin(blink25)
maxBlink5 = np.amax(blink25) - minBlink5
blink2Bool5 = np.logical_and(blink25 > minBlink5, blink25 < maxBlink5) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues5 = np.diff(blink2Bool5) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal5 = np.flatnonzero(blink2RangeValues5) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

#---calculate number of frames, frame rate, and time vector---
nframes5 = len(pArea5) # Contains length of pArea variable (equivalent to the blink variable).
frameVec5 = np.arange(0, nframes5, 1) # Vector of the total frames from the video.
framerate5 = 30 # frame rate of video
timeVec5 = (frameVec5 * 1)/framerate5 # Time Vector to calculate the length of the video.

#--- obtaining onset sync signal values ---
syncOnsetValues5 = onset_values(indicesValueSyncSignal5)
timeOfBlink2Event5 = timeVec5[syncOnsetValues5] # Provides the time values in which the sync signal is on.
timeOfBlink2Event5 = timeOfBlink2Event5[1:-1]

#--- Align trials to the event ---
timeRange5 = np.array([-0.5, 2.0]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec5, windowed_signal5 = eventlocked_signal(timeVec5, pArea5, timeOfBlink2Event5, timeRange5)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal5, postSignal5 = find_prepost_values(windowTimeVec5, windowed_signal5, -0.5, 0, 1.4, 2.0)
averagePreSignal5 = preSignal5.mean(axis = 0)
averagePostSignal5 = postSignal5.mean(axis = 0)
dataToPlot5 = [averagePreSignal5, averagePostSignal5]
xlabels5 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation5 = np.array([-7, 7])
pupilDilationTimeWindowVec5, pAreaDilated5 = eventlocked_signal(timeVec5, pArea5, timeOfBlink2Event5, timeRangeForPupilDilation5)
pAreaDilatedMean5 = pAreaDilated5.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat5, pval5 = stats.wilcoxon(averagePreSignal5, averagePostSignal5)
print('Wilcoxon value config12_6', wstat5,',',  'P-value config12_2', pval5)                            
                         

freq1Index2Kze, freq1Index32Kze, freq2Index2Kze, freq2Index32Kze, freq3Index2Kze, freq3Index32Kze, freq4Index2Kze, freq4Index32Kze, freq5Index2Kze, freq5Index32Kze, preSignalValues2Kze, preSignalValues32Kze = find_freqs_indices(preFreqs6, postFreqs6, 2000, 4000, 8000, 16000, 32000)


values2Kz1e, values4Kz1e, values8Kz1e, values16Kz1e, values32Kz1e, values2Kz2e, values4Kz2e, values8Kz2e, values16Kz2e, values32Kz2e, pre2KzValuese, pre32KzValuese = find_prepost_freqs_values(preSignal5, postSignal5, freq1Index2Kze, freq1Index32Kze, freq2Index2Kze, freq2Index32Kze, freq3Index2Kze, freq3Index32Kze, freq4Index2Kze, freq4Index32Kze, freq5Index2Kze, freq5Index32Kze, preSignalValues2Kze, preSignalValues32Kze)



                         
        
        
        
        
        
                  

#--- Normalized data ---
normVal1 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz1)
normVal2 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz1)
normVal3 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz1)
normVal4 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz1)
normVal5 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz1)
normVal6 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz2)
normVal7 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz2)
normVal8 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz2)
normVal9 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz2)
normVal10 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz2)

normVal1a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz1a)
normVal2a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz1a)
normVal3a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz1a)
normVal4a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz1a)
normVal5a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz1a)
normVal6a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz2a)
normVal7a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz2a)
normVal8a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz2a)
normVal9a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz2a)
normVal10a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz2a)

normVal1b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz1b)
normVal2b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz1b)
normVal3b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz1b)
normVal4b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz1b)
normVal5b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz1b)
normVal6b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz2b)
normVal7b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz2b)
normVal8b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz2b)
normVal9b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz2b)
normVal10b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz2b)

normVal1c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz1c)
normVal2c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz1c)
normVal3c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz1c)
normVal4c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz1c)
normVal5c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz1c)
normVal6c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz2c)
normVal7c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz2c)
normVal8c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz2c)
normVal9c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz2c)
normVal10c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz2c)

normVal1d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz1d)
normVal2d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz1d)
normVal3d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz1d)
normVal4d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz1d)
normVal5d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz1d)
normVal6d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz2d)
normVal7d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz2d)
normVal8d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz2d)
normVal9d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz2d)
normVal10d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz2d)

normVal1e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz1e)
normVal2e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz1e)
normVal3e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz1e)
normVal4e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz1e)
normVal5e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz1e)
normVal6e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values2Kz2e)
normVal7e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values4Kz2e)
normVal8e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values8Kz2e)
normVal9e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values16Kz2e)
normVal10e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, values32Kz2e)

normPreVal1 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre2KzValues)
normPreVal1a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre2KzValuesa)
normPreVal1b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre2KzValuesb)
normPreVal1c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre2KzValuesc)
normPreVal1d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre2KzValuesd)
normPreVal1e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre2KzValuese)

normPreVal2 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5,  pre32KzValues)
normPreVal2a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre32KzValuesa)
normPreVal2b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre32KzValuesb)
normPreVal2c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5,  pre32KzValuesc)
normPreVal2d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre32KzValuesd)
normPreVal2e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, pre32KzValuese)

























                       
                                                
                                                
 #--- Plotting normalized values; differences in pupil pre period and post period         
                                       
#plottingPupilNormalData = calculate_pupil_size_and_plot(normVal1, normVal2, normVal3, normVal4, normVal5, normVal6, normVal7, normVal8, normVal9, normVal10, normVal1a, normVal2a, normVal3a, normVal4a, normVal5a, normVal6a, normVal7a, normVal8a, normVal9a, normVal10a, normVal1b, normVal2b, normVal3b, normVal4b, normVal5b, normVal6b, normVal7b, normVal8b, normVal9b, normVal10b, normVal1c, normVal2c, normVal3c, normVal4c, normVal5c, normVal6c, normVal7c, normVal8c, normVal9c, normVal10c, normVal1d, normVal2d, normVal3d, normVal4d, normVal5d, normVal6d, normVal7d, normVal8d, normVal9d, normVal10d, normVal1e, normVal2e, normVal3e, normVal4e, normVal5e, normVal6e, normVal7e, normVal8e, normVal9e, normVal10e, normPreVal1, normPreVal1a, normPreVal1b, normPreVal1c, normPreVal1d, normPreVal1e, normPreVal2, normPreVal2a, normPreVal2b, normPreVal2c, normPreVal2d, normPreVal2e, frequenciesTested)                                                
                                                
                                                                
#--- plot with the three conditions aligned ---
#OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean,  pAreaDilatedMean1, pAreaDilatedMean2, pAreaDilatedMean3, pAreaDilatedMean4, pAreaDilatedMean5, pval, pval1, pval2, pval3, pval4, pval5)


#--- Figure with 3 scatter plots ---
#scatterPlots = scatter_plots(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2, averagePreSignal3, averagePostSignal3)

#--- Figure with 3 bar plots and scatter plots ---
#scattBar = barScat_plots(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal, averagePreSignal1, averagePostSignal1, preSignal1, postSignal2, averagePreSignal2, averagePostSignal2, preSignal2, postSignal2, averagePreSignal3, averagePostSignal3, preSignal3, postSignal3, averagePreSignal4, averagePostSignal4, preSignal4, postSignal4, averagePreSignal5, averagePostSignal5, preSignal5, postSignal5,pval, pval1, pval2, pval3, pval4, pval5)

#--- Pupil Dilation plots --- 
#pupilDilationPlots = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean, pupilDilationTimeWindowVec1, pAreaDilatedMean1, pupilDilationTimeWindowVec2, pAreaDilatedMean2)

#--- scatter & bar plots overlapped ---
#scattBar = bar_and_scatter(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2)
