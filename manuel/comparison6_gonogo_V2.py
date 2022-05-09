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
       
                
def find_type_freqs_pupil_values(preFreqArr, postFreqArr):
     '''
     Function will provide indices for each type of frequency
     Args:
     preFreqArr (np.array): array with the indices where the first pre frequency values are
     postFreqArr (np.array): array containing all of the post period frequencies
     
     returns:
     freqsType1...5 (np.array): arrays containing the indices where each pre and post period frequency match
     '''
     arr1 = [] 
     arr2 = [] 
     arr3 = [] 
     arr4 = [] 
     arr5 = [] 
     for i in preFreqArr: 
         if postFreqArr[i] == 2000: 
             arr1.append(i) 
             freqsType1 = np.asarray(arr1) 
         if postFreqArr[i] == 4000: 
             arr2.append(i) 
             freqsType2 = np.asarray(arr2) 
         if postFreqArr[i] == 8000: 
             arr3.append(i) 
             freqsType3 = np.asarray(arr3) 
         if postFreqArr[i] == 16000: 
             arr4.append(i) 
             freqsType4 = np.asarray(arr4) 
         if postFreqArr[i] == 32000: 
             arr5.append(i) 
             freqsType5 = np.asarray(arr5) 
     return(freqsType1, freqsType2, freqsType3, freqsType4, freqsType5)


def find_pupil_values(prePupilSize, postPupilSize, index1, index2, index3, index4, index5):
     '''
     Finds the corresponding pupil values for each type of frequency
     Args:
     prePupilSize (np.array): array containing the pupil size during the pre period
     postPupilSize (np.array): array containing the pupil size during the post period
     index1..5 (np.array): arrays containing the indices of each frequency type.
     
     returns:
     preValues2.. preValues32kz (np.array): arrays containing the pupil size during the pre period for each frequency type
     postvalues2.. postValues32kz (np.arrray): arrays containing the pupil size during the post period for each frequency type
     '''
     preValues2kz = np.take(prePupilSize, index1)
     preValues4kz = np.take(prePupilSize, index2)
     preValues8kz = np.take(prePupilSize, index3)
     preValues16kz = np.take(prePupilSize, index4)
     preValues32kz = np.take(prePupilSize, index5)
     
     postValues2kz = np.take(postPupilSize, index1)
     postValues4kz = np.take(postPupilSize, index2)
     postValues8kz = np.take(postPupilSize, index3)
     postValues16kz = np.take(postPupilSize, index4)
     postValues32kz = np.take(postPupilSize, index5)
     
     return(preValues2kz, preValues4kz, preValues8kz, preValues16kz, preValues32kz, postValues2kz, postValues4kz, postValues8kz, postValues16kz, postValues32kz)




def normalize_data_videos(pupilArea, pupilArea1, pupilArea2, pupilArea3, pupilArea4, pupilArea5, valuesToNormalize):
     ''' 
     Allows to normalize the average pupil area for each video
     Args:
     pupilArea1...5 (np.array) = array containing the raw data of the pupil area
     valuesToNormalize (np.array) = array containing the values of the pupil area to normalize
     returns:
     normalizedData (np.array) = variable containing an array with normalized values
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



def comparison_plot(time, valuesData1, valuesData2, valuesData3, valuesData4, valuesData5, valuesData6, pVal, pVal1, pVal2, pVal3, pVal4, pVal5): 
     ''' 
     Creates 1 figure with 3 plots 
     Args: 
     time = vector values for x axis 
     valuesData1 (np.array) = vector values for y axis of the first plot 
     valuesData2 (np.array)= vector values for y axis of the second plot
     valuesData3 (np.array)= vector values for y axis of the third plot
     returns: 
     plt.show() = 1 figure with 3 traces using the input data 
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

def calculate_pupil_size_and_plot(normValue1, normValue2, normValue3, normValue4, normValue5, normValue6, normValue7, normValue8, normValue9, normValue10,  normValue1a, normValue2a, normValue3a, normValue4a, normValue5a, normValue6a, normValue7a, normValue8a, normValue9a, normValue10a, normValue1b, normValue2b, normValue3b, normValue4b, normValue5b, normValue6b, normValue7b, normValue8b, normValue9b, normValue10b, normValue1c, normValue2c, normValue3c, normValue4c, normValue5c, normValue6c, normValue7c, normValue8c, normValue9c, normValue10c,  normValue1d, normValue2d, normValue3d, normValue4d, normValue5d, normValue6d, normValue7d, normValue8d, normValue9d, normValue10d, normValue1e, normValue2e, normValue3e, normValue4e, normValue5e, normValue6e, normValue7e, normValue8e, normValue9e, normValue10e, normPreVal1, normPreVal2, normPreVal3, normPreVal4, normPreVal5, normPreVal6, normPreVal7, normPreVal8, normPreVal9, normPreVal10, normPreVal1a, normPreVal2a, normPreVal3a, normPreVal4a, normPreVal5a, normPreVal6a, normPreVal7a, normPreVal8a, normPreVal9a, normPreVal10a, normPreVal1b, normPreVal2b, normPreVal3b, normPreVal4b, normPreVal5b, normPreVal6b, normPreVal7b, normPreVal8b, normPreVal9b, normPreVal10b, normPreVal1c, normPreVal2c, normPreVal3c, normPreVal4c, normPreVal5c, normPreVal6c, normPreVal7c, normPreVal8c, normPreVal9c, normPreVal10c, normPreVal1d, normPreVal2d, normPreVal3d, normPreVal4d, normPreVal5d, normPreVal6d, normPreVal7d, normPreVal8d, normPreVal9d, normPreVal10d, normPreVal1e, normPreVal2e, normPreVal3e, normPreVal4e, normPreVal5e, normPreVal6e, normPreVal7e, normPreVal8e, normPreVal9e, normPreVal10e, frequencies):
     '''
     Calculates the pupil size with normalized values  and plots it
     
     args:
     normVal1...10e (np.array) =  array containing the normalized pupil size for each frequency type
     frequencies (np.array) = array containing the number of frequencies being tested
     returns:
     plot.show() = plots the normalized pupil size across videos for each frequency type
     '''
     
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
     pre2Khz1 = np.concatenate((normPreVal1, normPreVal1a, normPreVal1b, normPreVal1c, normPreVal1d, normPreVal1e), axis = 0)
     pre4Khz1 = np.concatenate((normPreVal2, normPreVal2a, normPreVal2b, normPreVal2c, normPreVal2d, normPreVal2e), axis = 0)
     pre8Khz1 = np.concatenate((normPreVal3, normPreVal3a, normPreVal3b, normPreVal3c, normPreVal3d, normPreVal3e), axis = 0)
     pre16Khz1 = np.concatenate((normPreVal4, normPreVal1a, normPreVal4b, normPreVal4c, normPreVal4d, normPreVal4e), axis = 0)
     pre32Khz1 = np.concatenate((normPreVal5, normPreVal5a, normPreVal5b, normPreVal5c, normPreVal5d, normPreVal5e), axis = 0)
     pre2Khz2 = np.concatenate((normPreVal6, normPreVal6a, normPreVal6b, normPreVal6c, normPreVal6d, normPreVal6e), axis = 0)
     pre4Khz2 = np.concatenate((normPreVal7, normPreVal7a, normPreVal7b, normPreVal7c, normPreVal7d, normPreVal7e), axis = 0)
     pre8Khz2 = np.concatenate((normPreVal8, normPreVal8a, normPreVal8b, normPreVal8c, normPreVal8d, normPreVal8e), axis = 0)
     pre16Khz2 = np.concatenate((normPreVal9, normPreVal9a, normPreVal9b, normPreVal9c, normPreVal9d, normPreVal9e), axis = 0)
     pre32Khz2 = np.concatenate((normPreVal10, normPreVal10a, normPreVal10b, normPreVal10c, normPreVal10d, normPreVal10e), axis = 0)
     
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
     meanPre2Khz1 = np.average(pre2Khz1)
     meanPre4Khz1 = np.average(pre4Khz1)
     meanPre8Khz1 = np.average(pre8Khz1)
     meanPre16Khz1 = np.average(pre16Khz1)
     meanPre32Khz1 = np.average(pre32Khz1)
     meanPre2Khz2 = np.average(pre2Khz2)
     meanPre4Khz2 = np.average(pre4Khz2)
     meanPre8Khz2 = np.average(pre8Khz2)
     meanPre16Khz2 = np.average(pre16Khz2)
     meanPre32Khz2 = np.average(pre32Khz2)
     
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
     roundPre2Khz1 = np.round(meanPre2Khz1, decimals = 3)
     roundPre4Khz1 = np.round(meanPre4Khz1, decimals = 3)
     roundPre8Khz1 = np.round(meanPre8Khz1, decimals = 3)
     roundPre16Khz1 = np.round(meanPre16Khz1, decimals = 3)
     roundPre32Khz1 = np.round(meanPre32Khz1, decimals = 3)
     roundPre2Khz2 = np.round(meanPre2Khz2, decimals = 3)
     roundPre4Khz2 = np.round(meanPre4Khz2, decimals = 3)
     roundPre8Khz2 = np.round(meanPre8Khz2, decimals = 3)
     roundPre16Khz2 = np.round(meanPre16Khz2, decimals = 3)
     roundPre32Khz2 = np.round(meanPre32Khz2, decimals = 3)
     
     
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
     errPre2Khz1 = np.std(pre2Khz1)
     errPre4Khz1 = np.std(pre4Khz1)
     errPre8Khz1 = np.std(pre8Khz1)
     errPre16Khz1 = np.std(pre16Khz1)
     errPre32Khz1 = np.std(pre32Khz1)
     errPre2Khz2 = np.std(pre2Khz2)
     errPre4Khz2 = np.std(pre4Khz2)
     errPre8Khz2 = np.std(pre8Khz2)
     errPre16Khz2 = np.std(pre16Khz2)
     errPre32Khz2 = np.std(pre32Khz2)
     
     
     totalErr1 = [err2Khz1, err4Khz1, err8Khz1, err16Khz1, err32Khz1]
     totalErr2 = [err2Khz2, err4Khz2, err8Khz2, err16Khz2, err32Khz2]
     totalMean1 = [round2Khz1, round4Khz1, round8Khz1, round16Khz1, round32Khz1]
     totalPreMean1 = [roundPre2Khz1, roundPre4Khz1, roundPre8Khz1, roundPre16Khz1, roundPre32Khz1]
     totalMean2 = [round2Khz2, round4Khz2, round8Khz2, round16Khz2, round32Khz2]
     totalPreMean2 = [roundPre2Khz2, roundPre4Khz2, roundPre8Khz2, roundPre16Khz2, roundPre32Khz2]
     
# --- Calculate delta pupil area ---
     pArea2Khz1 = mean2Khz1 - meanPre2Khz1
     pArea4Khz1 = mean4Khz1 - meanPre4Khz1
     pArea8Khz1 = mean8Khz1 - meanPre8Khz1
     pArea16Khz1 = mean16Khz1 - meanPre16Khz1
     pArea32Khz1 = mean32Khz1 - meanPre32Khz1
     
     pArea2Khz2 = mean2Khz2 - meanPre2Khz2
     pArea4Khz2 = mean4Khz2 - meanPre4Khz2
     pArea8Khz2 = mean8Khz2 - meanPre8Khz2
     pArea16Khz2 = mean16Khz2 - meanPre16Khz2
     pArea32Khz2 = mean32Khz2 - meanPre32Khz2
    
     values2Khz = np.array([pArea2Khz1, pArea4Khz1, pArea8Khz1, pArea16Khz1, pArea32Khz1])
     values32Khz = np.array([pArea2Khz2, pArea4Khz2, pArea8Khz2, pArea16Khz2, pArea32Khz2])
     mean2Khz = [mean2Khz1, mean4Khz1, mean8Khz1, mean16Khz1, mean32Khz1]
     mean32Khz = [mean2Khz2, mean4Khz2, mean8Khz2, mean16Khz2, mean32Khz2]
     meanPre2Khz = [meanPre2Khz1, meanPre4Khz1, meanPre8Khz1, meanPre16Khz1, meanPre32Khz1]
     meanPre32Khz = [meanPre2Khz2, meanPre4Khz2, meanPre8Khz2, meanPre16Khz2, meanPre32Khz2]
     
     preValPlot2 = [meanPre2Khz1]
     preXaxis2 = frequencies[0]
     preValPlot32 = [meanPre32Khz2]
     preXaxis32 = frequencies[4]
     firstLegend = 'mean pre P. 2kHz Value', roundPre2Khz1
     secondLegend = 'mean pre P. 32kHz Value', roundPre32Khz2
     preLegend1 = 'mean pre Values (2kHz)'
     preLegend2 = 'mean pre Values (32kHz)'
     postLegend = 'mean post freqs values'
     ylimArr = [np.nanmin(values2Khz), np.nanmin(values32Khz)]
     ylimInf = np.nanmin(ylimArr)
     ymaxArr = [np.nanmax(values2Khz), np.nanmax(values32Khz)]
     ymaxSup = np.nanmax(ymaxArr)
# --- Finishing calculating ---     
     
     labelSize = 16 
     fig, plotVal = plt.subplots(2,2, constrained_layout = True, sharex= True) 
     fig.set_size_inches(9.5, 7.5, forward = True)
     
     plotVal[0,0].set_title('Pupil behavior for 2kHz', fontsize = labelSize)
     plotVal[0,0].set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
     plotVal[0,0].plot(frequencies, mean2Khz, color = '#000000', marker = '^', markersize = '9', label = postLegend)
     plotVal[0,0].plot(frequencies, meanPre2Khz, color = '#000000', marker = '^', markersize = '9', alpha = 0.5, label = preLegend1)
     plotVal[0,0].plot(preXaxis2, preValPlot2, color ='r', marker ='o', label = firstLegend) # Red dot in plot
     plotVal[0,0].errorbar(frequencies, mean2Khz, yerr = totalErr1, fmt='none', capsize=3.5, color = '#000000')    
     plotVal[0,0].tick_params(axis='y', labelsize=labelSize)
     plotVal[1,0].set_xlabel('Frequencies (kHz)', fontsize = labelSize)
     plotVal[1,0].plot(frequencies, mean32Khz, color = '#FFA500', marker = '^', markersize = '9', label = postLegend)
     plotVal[1,0].plot(frequencies, meanPre32Khz, color = '#FFA500', marker = '^', markersize = '9', alpha = 0.5, label = preLegend2)
     plotVal[1,0].plot(preXaxis32, preValPlot32, color ='r', marker ='o', markersize = '9', label = secondLegend) # Red dot in plot
     plotVal[1,0].errorbar(frequencies, totalMean2, yerr = totalErr2, fmt='none', capsize=3.5, color = '#FFA500') 
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
     plotVal[0,1].text(frequencies[1], values2Khz[1], np.around(pArea4Khz1, decimals =3))
     plotVal[0,1].text(frequencies[2], values2Khz[2], np.around(pArea8Khz1, decimals =3))
     plotVal[0,1].text(frequencies[3], values2Khz[3], np.around(pArea16Khz1, decimals =3))
     plotVal[0,1].text(frequencies[4], values2Khz[4], np.around(pArea32Khz1, decimals =3))
     plotVal[1,1].text(frequencies[0], values32Khz[0], np.around(pArea2Khz2, decimals =3))
     plotVal[1,1].text(frequencies[1], values32Khz[1], np.around(pArea4Khz2, decimals =3))
     plotVal[1,1].text(frequencies[2], values32Khz[2], np.around(pArea8Khz2, decimals =3))
     plotVal[1,1].text(frequencies[3], values32Khz[3], np.around(pArea16Khz2, decimals =3))
     plotVal[1,1].text(frequencies[4], values32Khz[4], np.around(pArea32Khz2, decimals =3), horizontalalignment='right')
     
     
     plotVal[0,0].grid(b = True)
     plotVal[0,1].grid(b = True)
     plotVal[1,0].grid(b = True)
     plotVal[1,1].grid(b = True)
     plt.suptitle(scatBarDict['plotFreqName'], fontsize = labelSize)
     plt.xticks(fontsize = labelSize) 
     plt.yticks(fontsize = labelSize)
     plt.yticks(fontsize = labelSize)
     plotVal[0,1].set_ylim([-0.01, 0.04])
     plotVal[1,1].set_ylim([-0.01, 0.04])
     plotVal[0,0].legend(prop ={"size":10})
     plotVal[0,1].legend(prop ={"size":10})
     plotVal[1,0].legend(prop ={"size":10})
     plotVal[1,1].legend(prop ={"size":10})
     plt.show() 
     
     return(plt.show())

def calculate_pupil_size_trials(value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,  value1a, value2a, value3a, value4a, value5a, value6a, value7a, value8a, value9a, value10a, value1b, value2b, value3b, value4b, value5b, value6b, value7b, value8b, value9b, value10b, value1c, value2c, value3c, value4c, value5c, value6c, value7c, value8c, value9c, value10c, value1d, value2d, value3d, value4d, value5d, value6d, value7d, value8d, value9d, value10d, value1e, value2e, value3e, value4e, value5e, value6e, value7e, value8e, value9e, value10e, preVal1, preVal2, preVal3, preVal4, preVal5, preVal6, preVal7, preVal8, preVal9, preVal10, preVal1a, preVal2a, preVal3a, preVal4a, preVal5a, preVal6a, preVal7a, preVal8a, preVal9a, preVal10a, preVal1b, preVal2b, preVal3b, preVal4b, preVal5b, preVal6b, preVal7b, preVal8b, preVal9b, preVal10b, preVal1c, preVal2c, preVal3c, preVal4c, preVal5c, preVal6c, preVal7c, preVal8c, preVal9c, preVal10c, preVal1d, preVal2d, preVal3d, preVal4d, preVal5d, preVal6d, preVal7d, preVal8d, preVal9d, preVal10d, preVal1e, preVal2e, preVal3e, preVal4e, preVal5e, preVal6e, preVal7e, preVal8e, preVal9e, preVal10e):
     '''
     Returns the pre and post values for each frequency type in their respective trials
     
     args:
     value1...value10e (np.array) = post values of each frequency type of each video
     preVal1...preValue10e (np.array) = pre valus of each frequency type of each video
     returns:
     trialsVal2kHz1... 32kHz1 (np.array) = array containing all the pre and post values across videos for the frequency types with a pre period frequency of 2kHz
     trialsVal2kHz2... 32kHz2 (np.array) = array containing all the pre and post values across videos for the frequency types with a pre period frequency of 32kHz
      
     '''
     
     values2Khz1 = np.concatenate((value1, value1a, value1b, value1c, value1d, value1e), axis = 0)
     values4Khz1 = np.concatenate((value2, value2a, value2b, value2c, value2d, value2e), axis = 0)
     values8Khz1 = np.concatenate((value3, value3a, value3b, value3c, value3d, value3e), axis = 0)
     values16Khz1 = np.concatenate((value4, value4a, value4b, value4c, value4d, value4e), axis = 0)
     values32Khz1 = np.concatenate((value5, value5a, value5b, value5c, value5d, value5e), axis = 0)
     values2Khz2 = np.concatenate((value6, value6a, value6b, value6c, value6d, value6e), axis = 0)
     values4Khz2 = np.concatenate((value7, value7a, value7b, value7c, value7d, value7e), axis = 0)
     values8Khz2 = np.concatenate((value8, value8a, value8b, value8c, value8d, value8e), axis = 0)
     values16Khz2 = np.concatenate((value9, value9a, value9b, value9c, value9d, value9e), axis = 0)
     values32Khz2 = np.concatenate((value10, value10a, value10b, value10c,value10d, value10e), axis = 0)
     pre2Khz1 = np.concatenate((preVal1, preVal1a, preVal1b, preVal1c, preVal1d, preVal1e), axis = 0)
     pre4Khz1 = np.concatenate((preVal2, preVal2a, preVal2b, preVal2c, preVal2d, preVal2e), axis = 0)
     pre8Khz1 = np.concatenate((preVal3, preVal3a, preVal3b, preVal3c, preVal3d, preVal3e), axis = 0)
     pre16Khz1 = np.concatenate((preVal4, preVal1a, preVal4b, preVal4c, preVal4d, preVal4e), axis = 0)
     pre32Khz1 = np.concatenate((preVal5, preVal5a, preVal5b, preVal5c, preVal5d, preVal5e), axis = 0)
     pre2Khz2 = np.concatenate((preVal6, preVal6a, preVal6b, preVal6c, preVal6d, preVal6e), axis = 0)
     pre4Khz2 = np.concatenate((preVal7, preVal7a, preVal7b, preVal7c, preVal7d, preVal7e), axis = 0)
     pre8Khz2 = np.concatenate((preVal8, preVal8a, preVal8b, preVal8c, preVal8d, preVal8e), axis = 0)
     pre16Khz2 = np.concatenate((preVal9, preVal9a, preVal9b, preVal9c, preVal9d, preVal9e), axis = 0)
     pre32Khz2 = np.concatenate((preVal10, preVal10a, preVal10b, preVal10c, preVal10d, preVal10e), axis = 0)
     
     trialsVal2kHz1 = np.concatenate((pre2Khz1, values2Khz1), axis = 0)
     trialsVal4kHz1 = np.concatenate((pre4Khz1, values4Khz1), axis = 0)
     trialsVal8kHz1 = np.concatenate((pre8Khz1, values8Khz1), axis = 0)
     trialsVal16kHz1 = np.concatenate((pre16Khz1, values16Khz1), axis = 0)
     trialsVal32kHz1 = np.concatenate((pre32Khz1, values32Khz1), axis = 0)
     trialsVal2kHz2 = np.concatenate((pre2Khz2, values2Khz2), axis = 0)
     trialsVal4kHz2 = np.concatenate((pre4Khz2, values4Khz2), axis = 0)
     trialsVal8kHz2 = np.concatenate((pre8Khz2, values8Khz2), axis = 0)
     trialsVal16kHz2 = np.concatenate((pre16Khz2, values16Khz2), axis = 0)
     trialsVal32kHz2 = np.concatenate((pre32Khz2, values32Khz2), axis = 0)
     
     return(trialsVal2kHz1, trialsVal4kHz1, trialsVal8kHz1, trialsVal16kHz1, trialsVal32kHz1, trialsVal2kHz2, trialsVal4kHz2, trialsVal8kHz2, trialsVal16kHz2, trialsVal32kHz2)



def find_values_time(pupilTime, index1, index2, index3, index4, index5, index6, index7, index8, index9, index10, index1a, index2a, index3a, index4a, index5a, index6a, index7a, index8a, index9a, index10a, index1b, index2b, index3b, index4b, index5b, index6b, index7b, index8b, index9b, index10b, index1c, index2c, index3c, index4c, index5c, index6c, index7c, index8c, index9c, index10c, index1d, index2d, index3d, index4d, index5d, index6d, index7d, index8d, index9d, index10d, index1e, index2e, index3e, index4e, index5e, index6e, index7e, index8e, index9e, index10e, midLim):
     '''
     finds the corresponding time where each trial takes places for each freq type
     '''
     preBool = np.logical_and(pupilTime[0] <= pupilTime, pupilTime < midLim)
     postBool = np.logical_and(midLim <= pupilTime, pupilTime <= len(pupilTime)-1)
     preTime = pupilTime[preBool]
     postTime = pupilTime[postBool]
     pre2kzTime1 = np.take(preTime, index1)
     pre4kzTime1 = np.take(preTime, index2)
     pre8kzTime1 = np.take(preTime, index3)
     pre16kzTime1 = np.take(preTime, index4)
     pre32kzTime1 = np.take(preTime, index5)
     pre2kzTime2 = np.take(preTime, index6)
     pre4kzTime2 = np.take(preTime, index7)
     pre8kzTime2 = np.take(preTime, index8)
     pre16kzTime2 = np.take(preTime, index9)
     pre32kzTime2 = np.take(preTime, index10)
     
     pre2kzTime1a = np.take(preTime, index1a)
     pre4kzTime1a = np.take(preTime, index2a)
     pre8kzTime1a = np.take(preTime, index3a)
     pre16kzTime1a = np.take(preTime, index4a)
     pre32kzTime1a = np.take(preTime, index5a)
     pre2kzTime2a = np.take(preTime, index6a)
     pre4kzTime2a = np.take(preTime, index7a)
     pre8kzTime2a = np.take(preTime, index8a)
     pre16kzTime2a = np.take(preTime, index9a)
     pre32kzTime2a = np.take(preTime, index10a)     
     
     pre2kzTime1b = np.take(preTime, index1b)
     pre4kzTime1b = np.take(preTime, index2b)
     pre8kzTime1b = np.take(preTime, index3b)
     pre16kzTime1b = np.take(preTime, index4b)
     pre32kzTime1b = np.take(preTime, index5b)
     pre2kzTime2b = np.take(preTime, index6b)
     pre4kzTime2b = np.take(preTime, index7b)
     pre8kzTime2b = np.take(preTime, index8b)
     pre16kzTime2b = np.take(preTime, index9b)
     pre32kzTime2b = np.take(preTime, index10b)     
     
     pre2kzTime1c = np.take(preTime, index1c)
     pre4kzTime1c = np.take(preTime, index2c)
     pre8kzTime1c = np.take(preTime, index3c)
     pre16kzTime1c = np.take(preTime, index4c)
     pre32kzTime1c = np.take(preTime, index5c)
     pre2kzTime2c = np.take(preTime, index6c)
     pre4kzTime2c = np.take(preTime, index7c)
     pre8kzTime2c = np.take(preTime, index8c)
     pre16kzTime2c = np.take(preTime, index9c)
     pre32kzTime2c = np.take(preTime, index10c)
     
     pre2kzTime1d = np.take(preTime, index1d)
     pre4kzTime1d = np.take(preTime, index2d)
     pre8kzTime1d = np.take(preTime, index3d)
     pre16kzTime1d = np.take(preTime, index4d)
     pre32kzTime1d = np.take(preTime, index5d)
     pre2kzTime2d = np.take(preTime, index6d)
     pre4kzTime2d = np.take(preTime, index7d)
     pre8kzTime2d = np.take(preTime, index8d)
     pre16kzTime2d = np.take(preTime, index9d)
     pre32kzTime2d = np.take(preTime, index10d)
     
     pre2kzTime1e = np.take(preTime, index1e)
     pre4kzTime1e = np.take(preTime, index2e)
     pre8kzTime1e = np.take(preTime, index3e)
     pre16kzTime1e = np.take(preTime, index4e)
     pre32kzTime1e = np.take(preTime, index5e)
     pre2kzTime2e = np.take(preTime, index6e)
     pre4kzTime2e = np.take(preTime, index7e)
     pre8kzTime2e = np.take(preTime, index8e)
     pre16kzTime2e = np.take(preTime, index9e)
     pre32kzTime2e = np.take(preTime, index10e)         
     
     post2kzTime1 = np.take(postTime, index1)
     post4kzTime1 = np.take(postTime, index2)
     post8kzTime1 = np.take(postTime, index3)
     post16kzTime1 = np.take(postTime, index4)
     post32kzTime1 = np.take(postTime, index5)
     post2kzTime2 = np.take(postTime, index6)
     post4kzTime2 = np.take(postTime, index7)
     post8kzTime2 = np.take(postTime, index8)
     post16kzTime2 = np.take(postTime, index9)
     post32kzTime2 = np.take(postTime, index10)
     
     post2kzTime1a = np.take(postTime, index1a)
     post4kzTime1a = np.take(postTime, index2a)
     post8kzTime1a = np.take(postTime, index3a)
     post16kzTime1a = np.take(postTime, index4a)
     post32kzTime1a = np.take(postTime, index5a)
     post2kzTime2a = np.take(postTime, index6a)
     post4kzTime2a = np.take(postTime, index7a)
     post8kzTime2a = np.take(postTime, index8a)
     post16kzTime2a = np.take(postTime, index9a)
     post32kzTime2a = np.take(postTime, index10a)     
     
     post2kzTime1b = np.take(postTime, index1b)
     post4kzTime1b = np.take(postTime, index2b)
     post8kzTime1b = np.take(postTime, index3b)
     post16kzTime1b = np.take(postTime, index4b)
     post32kzTime1b = np.take(postTime, index5b)
     post2kzTime2b = np.take(postTime, index6b)
     post4kzTime2b = np.take(postTime, index7b)
     post8kzTime2b = np.take(postTime, index8b)
     post16kzTime2b = np.take(postTime, index9b)
     post32kzTime2b = np.take(postTime, index10b)     
     
     post2kzTime1c = np.take(postTime, index1c)
     post4kzTime1c = np.take(postTime, index2c)
     post8kzTime1c = np.take(postTime, index3c)
     post16kzTime1c = np.take(postTime, index4c)
     post32kzTime1c = np.take(postTime, index5c)
     post2kzTime2c = np.take(postTime, index6c)
     post4kzTime2c = np.take(postTime, index7c)
     post8kzTime2c = np.take(postTime, index8c)
     post16kzTime2c = np.take(postTime, index9c)
     post32kzTime2c = np.take(postTime, index10c)
     
     post2kzTime1d = np.take(postTime, index1d)
     post4kzTime1d = np.take(postTime, index2d)
     post8kzTime1d = np.take(postTime, index3d)
     post16kzTime1d = np.take(postTime, index4d)
     post32kzTime1d = np.take(postTime, index5d)
     post2kzTime2d = np.take(postTime, index6d)
     post4kzTime2d = np.take(postTime, index7d)
     post8kzTime2d = np.take(postTime, index8d)
     post16kzTime2d = np.take(postTime, index9d)
     post32kzTime2d = np.take(postTime, index10d)
     
     post2kzTime1e = np.take(postTime, index1e)
     post4kzTime1e = np.take(postTime, index2e)
     post8kzTime1e = np.take(postTime, index3e)
     post16kzTime1e = np.take(postTime, index4e)
     post32kzTime1e = np.take(postTime, index5e)
     post2kzTime2e = np.take(postTime, index6e)
     post4kzTime2e = np.take(postTime, index7e)
     post8kzTime2e = np.take(postTime, index8e)
     post16kzTime2e = np.take(postTime, index9e)
     post32kzTime2e = np.take(postTime, index10e)
     
     preTime2kz1 = np.concatenate((pre2kzTime1, pre2kzTime1a, pre2kzTime1b, pre2kzTime1c, pre2kzTime1d, pre2kzTime1e), axis = 0)
     preTime4kz1 = np.concatenate((pre4kzTime1, pre4kzTime1a, pre4kzTime1b, pre4kzTime1c, pre4kzTime1d, pre4kzTime1e), axis = 0)
     preTime8kz1 = np.concatenate((pre8kzTime1, pre8kzTime1a, pre8kzTime1b, pre8kzTime1c, pre8kzTime1d, pre8kzTime1e), axis = 0)
     preTime16kz1 = np.concatenate((pre16kzTime1, pre16kzTime1a, pre16kzTime1b, pre16kzTime1c, pre16kzTime1d, pre16kzTime1e), axis = 0)
     preTime32kz1 = np.concatenate((pre32kzTime1, pre32kzTime1a, pre32kzTime1b, pre32kzTime1c, pre32kzTime1d, pre32kzTime1e), axis = 0)  
     preTime2kz2 = np.concatenate((pre2kzTime2, pre2kzTime2a, pre2kzTime2b, pre2kzTime2c, pre2kzTime2d, pre2kzTime2e), axis = 0)
     preTime4kz2 = np.concatenate((pre4kzTime2, pre4kzTime2a, pre4kzTime2b, pre4kzTime2c, pre4kzTime2d, pre4kzTime2e), axis = 0)
     preTime8kz2 = np.concatenate((pre8kzTime2, pre8kzTime2a, pre8kzTime2b, pre8kzTime2c, pre8kzTime2d, pre8kzTime2e), axis = 0)
     preTime16kz2 = np.concatenate((pre16kzTime2, pre16kzTime2a, pre16kzTime2b, pre16kzTime2c, pre16kzTime2d, pre16kzTime2e), axis = 0)
     preTime32kz2 = np.concatenate((pre32kzTime2, pre32kzTime2a, pre32kzTime2b, pre32kzTime2c, pre32kzTime2d, pre32kzTime2e), axis = 0)

     postTime2kz1 = np.concatenate((post2kzTime1, post2kzTime1a, post2kzTime1b, post2kzTime1c, post2kzTime1d, post2kzTime1e), axis = 0)
     postTime4kz1 = np.concatenate((post4kzTime1, post4kzTime1a, post4kzTime1b, post4kzTime1c, post4kzTime1d, post4kzTime1e), axis = 0)
     postTime8kz1 = np.concatenate((post8kzTime1, post8kzTime1a, post8kzTime1b, post8kzTime1c, post8kzTime1d, post8kzTime1e), axis = 0)
     postTime16kz1 = np.concatenate((post16kzTime1, post16kzTime1a, post16kzTime1b, post16kzTime1c, post16kzTime1d, post16kzTime1e), axis = 0)
     postTime32kz1 = np.concatenate((post32kzTime1, post32kzTime1a, post32kzTime1b, post32kzTime1c, post32kzTime1d, post32kzTime1e), axis = 0)  
     postTime2kz2 = np.concatenate((post2kzTime2, post2kzTime2a, post2kzTime2b, post2kzTime2c, post2kzTime2d, post2kzTime2e), axis = 0)
     postTime4kz2 = np.concatenate((post4kzTime2, post4kzTime2a, post4kzTime2b, post4kzTime2c, post4kzTime2d, post4kzTime2e), axis = 0)
     postTime8kz2 = np.concatenate((post8kzTime2, post8kzTime2a, post8kzTime2b, post8kzTime2c, post8kzTime2d, post8kzTime2e), axis = 0)
     postTime16kz2 = np.concatenate((post16kzTime2, post16kzTime2a, post16kzTime2b, post16kzTime2c, post16kzTime2d, post16kzTime2e), axis = 0)
     postTime32kz2 = np.concatenate((post32kzTime2, post32kzTime2a, post32kzTime2b, post32kzTime2c, post32kzTime2d, post32kzTime2e), axis = 0)
     
     time2khz1 = np.concatenate((preTime2kz1, postTime2kz1), axis = 0)
     time4khz1 = np.concatenate((preTime4kz1, postTime4kz1), axis = 0)
     time8khz1 = np.concatenate((preTime8kz1, postTime8kz1), axis = 0)
     time16khz1 = np.concatenate((preTime16kz1, postTime16kz1), axis = 0)
     time32khz1 = np.concatenate((preTime32kz1, postTime32kz1), axis = 0)
     time2khz2 = np.concatenate((preTime2kz2, postTime2kz2), axis = 0)
     time4khz2 = np.concatenate((preTime4kz2, postTime4kz2), axis = 0)
     time8khz2 = np.concatenate((preTime8kz2, postTime8kz2), axis = 0)
     time16khz2 = np.concatenate((preTime16kz2, postTime16kz2), axis = 0)
     time32khz2 = np.concatenate((preTime32kz2, postTime32kz2), axis = 0)
     
     return(time2khz1, time4khz1, time8khz1, time16khz1, time32khz1, time2khz2, time4khz2, time8khz2, time16khz2, time32khz2)   
        


def plot_trials_only(timePlot1, timePlot2, timePlot3, timePlot4, timePlot5, timePlot6, timePlot7, timePlot8, timePlot9, timePlot10, dataPlot1, dataPlot2, dataPlot3, dataPlot4, dataPlot5, dataPlot6, dataPlot7, dataPlot8, dataPlot9, dataPlot10):
     '''
     Plots the behavior for each frequency type across videos
     args:
     timePlot1...10 (np.array) = array containing the time values where each value of each trial takes place during the pre and post period for each frequency type across videos
     dataPlot...10 (np.array) = array containing the pre and post values for each frequency type across videos
     returns:
     plt.show() = plots each frequency type vs time across videos
     '''
     sortTime1 = np.argsort(timePlot1)
     sortTime2 = np.argsort(timePlot2)
     sortTime3 = np.argsort(timePlot3)
     sortTime4 = np.argsort(timePlot4)
     sortTime5 = np.argsort(timePlot5)
     sortTime6 = np.argsort(timePlot6)
     sortTime7 = np.argsort(timePlot7)
     sortTime8 = np.argsort(timePlot8)
     sortTime9 = np.argsort(timePlot9)
     sortTime10 = np.argsort(timePlot10)
     
     valArr1 = []
     timeSort1 = []
     valArr2 = []
     timeSort2 = []
     valArr3 = []
     timeSort3 = []
     valArr4 = []
     timeSort4 = []
     valArr5 = []
     timeSort5 = []
     valArr6 = []
     timeSort6 = []
     valArr7 = []
     timeSort7 = []
     valArr8 = []
     timeSort8 = []
     valArr9 = []
     timeSort9 = []
     valArr10 = []
     timeSort10 = []
     
     for i in sortTime1:
         timeSort1.append(timePlot1[i])
         valArr1.append(dataPlot1[i])
     for j in sortTime2:
         timeSort2.append(timePlot2[j])
         valArr2.append(dataPlot2[j])
     for k in sortTime3:
         timeSort3.append(timePlot3[k])
         valArr3.append(dataPlot3[k])         
     for l in sortTime4:
         timeSort4.append(timePlot4[l])
         valArr4.append(dataPlot4[l])
     for m in sortTime5:
         timeSort5.append(timePlot5[m])
         valArr5.append(dataPlot5[m])
     for n in sortTime6:
         timeSort6.append(timePlot6[n])
         valArr6.append(dataPlot6[n])
     for o in sortTime7:
         timeSort7.append(timePlot7[o])
         valArr7.append(dataPlot7[o])
     for p in sortTime8:
         timeSort8.append(timePlot8[p])
         valArr8.append(dataPlot8[p])
     for x in sortTime9:
         timeSort9.append(timePlot9[x])
         valArr9.append(dataPlot9[x])
     for z in sortTime10:
         timeSort10.append(timePlot10[z])
         valArr10.append(dataPlot10[z])
             
     labelSize = 14 
     fig, trialPl = plt.subplots(5, 2, constrained_layout = True, sharex= True, sharey = True) 
     fig.set_size_inches(9.5, 7.5, forward = True)
     
     trialPl[0,0].plot(timeSort1, valArr1, color = '#04D8B2')
     trialPl[0,0].set_title('Type 2kHz-2kHz', fontsize = labelSize)
     trialPl[0,0].tick_params(axis='y', labelsize=labelSize)
     trialPl[1,0].plot(timeSort2, valArr2, color = '#D2691E')
     trialPl[1,0].set_title('Type 2kHz-4kHz', fontsize = labelSize)
     trialPl[1,0].tick_params(axis='y', labelsize=labelSize)
     trialPl[2,0].plot(timeSort3, valArr3, color = '#054907')
     trialPl[2,0].set_title('Type 2kHz-8kHz', fontsize = labelSize)
     trialPl[2,0].set_ylabel('Mean pupil area', fontsize = labelSize) 
     trialPl[2,0].tick_params(axis='y', labelsize=labelSize) 
     trialPl[3,0].plot(timeSort4, valArr4, color = 'r')
     trialPl[3,0].set_title('Type 2kHz-16kHz', fontsize = labelSize)
     trialPl[3,0].tick_params(axis='y', labelsize=labelSize) 
     trialPl[4,0].plot(timeSort5, valArr5, color = '#808080')
     trialPl[4,0].set_title('Type 2kHz-32kHz', fontsize = labelSize)
     trialPl[4,0].set_xlabel('Time (s)', fontsize = labelSize)
     trialPl[4,0].tick_params(axis='y', labelsize=labelSize)
     trialPl[4,0].tick_params(axis='x', labelsize=labelSize)
     trialPl[0,1].plot(timeSort6, valArr6, color = '#04D8B2')
     trialPl[0,1].set_title('Type 32kHz-2kHz', fontsize = labelSize)
     trialPl[0,1].tick_params(axis='y', labelsize=labelSize) 
     trialPl[1,1].plot(timeSort7, valArr7, color = '#D2691E')
     trialPl[1,1].set_title('Type 32kHz-4kHz', fontsize = labelSize)
     trialPl[1,1].tick_params(axis='y', labelsize=labelSize)
     trialPl[2,1].plot(timeSort8, valArr8, color = '#054907')
     trialPl[2,1].set_title('Type 32kHz-8kHz', fontsize = labelSize)
     trialPl[2,1].tick_params(axis='y', labelsize=labelSize) 
     trialPl[3,1].plot(timeSort9, valArr9, color = 'r')
     trialPl[3,1].set_title('Type 32kHz-16kHz', fontsize = labelSize)
     trialPl[3,1].tick_params(axis='y', labelsize=labelSize)
     trialPl[4,1].plot(timeSort10, valArr10, color = '#808080')
     trialPl[4,1].set_title('Type 32kHz-32kHz', fontsize = labelSize)
     trialPl[4,1].set_xlabel('Time (s)', fontsize = labelSize)
     trialPl[4,1].tick_params(axis='x', labelsize=labelSize)
     trialPl[4,1].tick_params(axis='y', labelsize=labelSize)  
     plt.suptitle('Pupil size for each frequency type across videos: pure10_20220418-21', fontsize = labelSize)
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
	
scatBarDict = {'title':'Pupil behavior before and after sound stimulus: pure011 20220419', 'savedName':'pure0043ScatbarPlot', 'yLabel':'Mean Pupil Area', 'xLabelTitle':'Conditions', 'plotFreqName':'Pupil size for 5 different frequencies: pure011_20220415-19'}

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

freq1Index2Kz, freq1Index32Kz, freq2Index2Kz, freq2Index32Kz, freq3Index2Kz, freq3Index32Kz, freq4Index2Kz, freq4Index32Kz, freq5Index2Kz, freq5Index32Kz, preSignalValues2Kz, preSignalValues32Kz = find_freqs_indices(preFreqs, postFreqs, 2000, 4000, 8000, 16000, 32000)


indexType22kz, indexType24kz, indexType28kz, indexType216kz, indexType232kz = find_type_freqs_pupil_values(preSignalValues2Kz, postFreqs)

indexType322kz, indexType324kz, indexType328kz, indexType3216kz, indexType3232kz = find_type_freqs_pupil_values(preSignalValues32Kz, postFreqs)

preValType22kz, preValType24kz, preValType28kz, preValType216kz, preValType232kz, postValType22kz, postValType24kz, postValType28kz, postValType216kz, postValType232kz = find_pupil_values(preSignal, postSignal, indexType22kz, indexType24kz, indexType28kz, indexType216kz, indexType232kz)

preValType322kz, preValType324kz, preValType328kz, preValType3216kz, preValType3232kz, postValType322kz, postValType324kz, postValType328kz, postValType3216kz, postValType3232kz = find_pupil_values(preSignal, postSignal, indexType322kz, indexType324kz, indexType328kz, indexType3216kz, indexType3232kz)















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



freq1Index2Kza, freq1Index32Kza, freq2Index2Kza, freq2Index32Kza, freq3Index2Kza, freq3Index32Kza, freq4Index2Kza, freq4Index32Kza, freq5Index2Kza, freq5Index32Kza, preSignalValues2Kza, preSignalValues32Kza = find_freqs_indices(preFreqs2, postFreqs2, 2000, 4000, 8000, 16000, 32000)


indexType22kza, indexType24kza, indexType28kza, indexType216kza, indexType232kza = find_type_freqs_pupil_values(preSignalValues2Kza, postFreqs2)

indexType322kza, indexType324kza, indexType328kza, indexType3216kza, indexType3232kza = find_type_freqs_pupil_values(preSignalValues32Kza, postFreqs2)

preValType22kza, preValType24kza, preValType28kza, preValType216kza, preValType232kza, postValType22kza, postValType24kza, postValType28kza, postValType216kza, postValType232kza = find_pupil_values(preSignal1, postSignal1, indexType22kza, indexType24kza, indexType28kza, indexType216kza, indexType232kza)

preValType322kza, preValType324kza, preValType328kza, preValType3216kza, preValType3232kza, postValType322kza, postValType324kza, postValType328kza, postValType3216kza, postValType3232kza = find_pupil_values(preSignal1, postSignal1, indexType322kza, indexType324kza, indexType328kza, indexType3216kza, indexType3232kza)











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


freq1Index2Kzb, freq1Index32Kzb, freq2Index2Kzb, freq2Index32Kzb, freq3Index2Kzb, freq3Index32Kzb, freq4Index2Kzb, freq4Index32Kzb, freq5Index2Kzb, freq5Index32Kzb, preSignalValues2Kzb, preSignalValues32Kzb = find_freqs_indices(preFreqs3, postFreqs3, 2000, 4000, 8000, 16000, 32000)

indexType22kzb, indexType24kzb, indexType28kzb, indexType216kzb, indexType232kzb = find_type_freqs_pupil_values(preSignalValues2Kzb, postFreqs3)

indexType322kzb, indexType324kzb, indexType328kzb, indexType3216kzb, indexType3232kzb = find_type_freqs_pupil_values(preSignalValues32Kzb, postFreqs3)

preValType22kzb, preValType24kzb, preValType28kzb, preValType216kzb, preValType232kzb, postValType22kzb, postValType24kzb, postValType28kzb, postValType216kzb, postValType232kzb = find_pupil_values(preSignal2, postSignal2, indexType22kzb, indexType24kzb, indexType28kzb, indexType216kzb, indexType232kzb)

preValType322kzb, preValType324kzb, preValType328kzb, preValType3216kzb, preValType3232kzb, postValType322kzb, postValType324kzb, postValType328kzb, postValType3216kzb, postValType3232kzb = find_pupil_values(preSignal2, postSignal2, indexType322kzb, indexType324kzb, indexType328kzb, indexType3216kzb, indexType3232kzb)












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

indexType22kzc, indexType24kzc, indexType28kzc, indexType216kzc, indexType232kzc = find_type_freqs_pupil_values(preSignalValues2Kzc, postFreqs4)

indexType322kzc, indexType324kzc, indexType328kzc, indexType3216kzc, indexType3232kzc = find_type_freqs_pupil_values(preSignalValues32Kzc, postFreqs4)               
                                                
preValType22kzc, preValType24kzc, preValType28kzc, preValType216kzc, preValType232kzc, postValType22kzc, postValType24kzc, postValType28kzc, postValType216kzc, postValType232kzc = find_pupil_values(preSignal3, postSignal3, indexType22kzc, indexType24kzc, indexType28kzc, indexType216kzc, indexType232kzc)

preValType322kzc, preValType324kzc, preValType328kzc, preValType3216kzc, preValType3232kzc, postValType322kzc, postValType324kzc, postValType328kzc, postValType3216kzc, postValType3232kzc = find_pupil_values(preSignal3, postSignal3, indexType322kzc, indexType324kzc, indexType328kzc, indexType3216kzc, indexType3232kzc)                                                
                                                
                                                
 
                                                
                 
                                                
                                                
                                                
                                                
                                                
                                                
                                                
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

indexType22kzd, indexType24kzd, indexType28kzd, indexType216kzd, indexType232kzd = find_type_freqs_pupil_values(preSignalValues2Kzd, postFreqs5)

indexType322kzd, indexType324kzd, indexType328kzd, indexType3216kzd, indexType3232kzd = find_type_freqs_pupil_values(preSignalValues32Kzd, postFreqs5) 
         
preValType22kzd, preValType24kzd, preValType28kzd, preValType216kzd, preValType232kzd, postValType22kzd, postValType24kzd, postValType28kzd, postValType216kzd, postValType232kzd = find_pupil_values(preSignal4, postSignal4, indexType22kzd, indexType24kzd, indexType28kzd, indexType216kzd, indexType232kzd)

preValType322kzd, preValType324kzd, preValType328kzd, preValType3216kzd, preValType3232kzd, postValType322kzd, postValType324kzd, postValType328kzd, postValType3216kzd, postValType3232kzd = find_pupil_values(preSignal4, postSignal4, indexType322kzd, indexType324kzd, indexType328kzd, indexType3216kzd, indexType3232kzd)                         
                         
                         
 
  
           
                         
                         
                         
                         
                         
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


indexType22kze, indexType24kze, indexType28kze, indexType216kze, indexType232kze = find_type_freqs_pupil_values(preSignalValues2Kze, postFreqs6)

indexType322kze, indexType324kze, indexType328kze, indexType3216kze, indexType3232kze = find_type_freqs_pupil_values(preSignalValues32Kze, postFreqs6)

preValType22kze, preValType24kze, preValType28kze, preValType216kze, preValType232kze, postValType22kze, postValType24kze, postValType28kze, postValType216kze, postValType232kze = find_pupil_values(preSignal5, postSignal5, indexType22kze, indexType24kze, indexType28kze, indexType216kze, indexType232kze)

preValType322kze, preValType324kze, preValType328kze, preValType3216kze, preValType3232kze, postValType322kze, postValType324kze, postValType328kze, postValType3216kze, postValType3232kze = find_pupil_values(preSignal5, postSignal5, indexType322kze, indexType324kze, indexType328kze, indexType3216kze, indexType3232kze)
                         

      
     
        
        
        
                  

#--- Normalized data ---
normVal1 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType22kz)
normVal2 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType24kz)
normVal3 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType28kz)
normVal4 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType216kz)
normVal5 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType232kz)
normVal6 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType322kz)
normVal7 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType324kz)
normVal8 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType328kz)
normVal9 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3216kz)
normVal10 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3232kz)

normVal1a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType22kza)
normVal2a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType24kza)
normVal3a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType28kza)
normVal4a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType216kza)
normVal5a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType232kza)
normVal6a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType322kza)
normVal7a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType324kz)
normVal8a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType328kza)
normVal9a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3216kza)
normVal10a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3232kza)

normVal1b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType22kzb)
normVal2b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType24kzb)
normVal3b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType28kzb)
normVal4b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType216kzb)
normVal5b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType232kzb)
normVal6b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType322kzb)
normVal7b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType324kzb)
normVal8b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType328kzb)
normVal9b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3216kzb)
normVal10b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3232kzb)

normVal1c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType22kzc)
normVal2c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType24kzc)
normVal3c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType28kzc)
normVal4c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType216kzc)
normVal5c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType232kzc)
normVal6c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType322kzc)
normVal7c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType324kzc)
normVal8c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType328kzc)
normVal9c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3216kzc)
normVal10c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3232kzc)

normVal1d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType22kzd)
normVal2d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType24kzd)
normVal3d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType28kzd)
normVal4d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType216kzd)
normVal5d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType232kzd)
normVal6d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType322kzd)
normVal7d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType324kzd)
normVal8d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType328kzd)
normVal9d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3216kzd)
normVal10d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3232kzd)

normVal1e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType22kze)
normVal2e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType24kze)
normVal3e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType28kze)
normVal4e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType216kze)
normVal5e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType232kze)
normVal6e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType322kze)
normVal7e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType324kze)
normVal8e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType328kze)
normVal9e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3216kze)
normVal10e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postValType3232kze)

normPreVal1 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType22kz)
normPreVal2 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType24kz)
normPreVal3 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType28kz)
normPreVal4 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType216kz)
normPreVal5 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType232kz)
normPreVal6 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType322kz)
normPreVal7 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType324kz)
normPreVal8 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType328kz)
normPreVal9 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3216kz)
normPreVal10 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3232kz)

normPreVal1a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType22kza)
normPreVal2a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType24kza)
normPreVal3a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType28kza)
normPreVal4a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType216kza)
normPreVal5a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType232kza)
normPreVal6a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType322kza)
normPreVal7a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType324kza)
normPreVal8a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType328kza)
normPreVal9a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3216kza)
normPreVal10a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3232kza)

normPreVal1b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType22kzb)
normPreVal2b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType24kzb)
normPreVal3b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType28kzb)
normPreVal4b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType216kzb)
normPreVal5b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType232kzb)
normPreVal6b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType322kzb)
normPreVal7b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType324kzb)
normPreVal8b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType328kzb)
normPreVal9b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3216kzb)
normPreVal10b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3232kzb)

normPreVal1c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType22kzc)
normPreVal2c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType24kzc)
normPreVal3c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType28kzc)
normPreVal4c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType216kzc)
normPreVal5c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType232kzc)
normPreVal6c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType322kzc)
normPreVal7c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType324kzc)
normPreVal8c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType328kzc)
normPreVal9c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3216kzc)
normPreVal10c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3232kzc)

normPreVal1d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType22kzd)
normPreVal2d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType24kzd)
normPreVal3d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType28kzd)
normPreVal4d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType216kzd)
normPreVal5d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType232kzd)
normPreVal6d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType322kzd)
normPreVal7d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType324kzd)
normPreVal8d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType328kzd)
normPreVal9d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3216kzd)
normPreVal10d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3232kzd)

normPreVal1e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType22kze)
normPreVal2e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType24kze)
normPreVal3e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType28kze)
normPreVal4e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType216kze)
normPreVal5e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType232kze)
normPreVal6e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType322kze)
normPreVal7e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType324kze)
normPreVal8e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType328kze)
normPreVal9e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3216kze)
normPreVal10e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preValType3232kze)

                                           

# --- Finding the pupil values (pre/post) of each frequency type across videos ---
trials2kzValues1, trials4kzValues1, trials8kzValues1, trials16kzValues1, trials32kzValues1, trials2kzValues2, trials4kzValues2, trials8kzValues2, trials16kzValues2, trials32kzValues2, = calculate_pupil_size_trials(postValType22kz, postValType24kz, postValType28kz, postValType216kz, postValType232kz, postValType322kz, postValType324kz, postValType328kz, postValType3216kz, postValType3232kz, postValType22kza, postValType24kza, postValType28kza, postValType216kza, postValType232kza, postValType322kza, postValType324kza, postValType328kza, postValType3216kza, postValType3232kza, postValType22kzb, postValType24kzb, postValType28kzb, postValType216kzb, postValType232kzb, postValType322kzb, postValType324kzb, postValType328kzb, postValType3216kzb, postValType3232kzb, postValType22kzc, postValType24kzc, postValType28kzc, postValType216kzc, postValType232kzc, postValType322kzc, postValType324kzc, postValType328kzc, postValType3216kzc, postValType3232kzc, postValType22kzd, postValType24kzd, postValType28kzd, postValType216kzd, postValType232kzd, postValType322kzd, postValType324kzd, postValType328kzd, postValType3216kzd, postValType3232kzd, postValType22kze, postValType24kze, postValType28kze, postValType216kze, postValType232kze, postValType322kze, postValType324kze, postValType328kze, postValType3216kze, postValType3232kze,preValType22kz, preValType24kz, preValType28kz, preValType216kz, preValType232kz, preValType322kz, preValType324kz, preValType328kz, preValType3216kz, preValType3232kz, preValType22kza, preValType24kza, preValType28kza, preValType216kza, preValType232kza, preValType322kza, preValType324kza, preValType328kza, preValType3216kza, preValType3232kza, preValType22kzb, preValType24kzb, preValType28kzb, preValType216kzb, preValType232kzb, preValType322kzb, preValType324kzb, preValType328kzb, preValType3216kzb, preValType3232kzb, preValType22kzc, preValType24kzc, preValType28kzc, preValType216kzc, preValType232kzc, preValType322kzc, preValType324kzc, preValType328kzc, preValType3216kzc, preValType3232kzc, preValType22kzd, preValType24kzd, preValType28kzd, preValType216kzd, preValType232kzd, preValType322kzd, preValType324kzd, preValType328kzd, preValType3216kzd, preValType3232kzd, preValType22kze, preValType24kze, preValType28kze, preValType216kze, preValType232kze, preValType322kze, preValType324kze, preValType328kze, preValType3216kze, preValType3232kze)

# --- Finding the time location for each trial of each frequency type ---
trialsTime2kz1, trialsTime4kz1, trialsTime8kz1, trialsTime16kz1, trialsTime32kz1, trialsTime2kz2, trialsTime4kz2, trialsTime8kz2, trialsTime16kz2, trialsTime32kz2  = find_values_time(pupilDilationTimeWindowVec, indexType22kz, indexType24kz, indexType28kz, indexType216kz, indexType232kz, indexType322kz, indexType324kz, indexType328kz, indexType3216kz-1, indexType3232kz, indexType22kza, indexType24kza, indexType28kza, indexType216kza, indexType232kza, indexType322kza, indexType324kza, indexType328kza, indexType3216kza, indexType3232kza-1, indexType22kzb, indexType24kzb, indexType28kzb, indexType216kzb, indexType232kzb, indexType322kzb, indexType324kzb, indexType328kzb, indexType3216kzb, indexType3232kzb, indexType22kzc, indexType24kzc, indexType28kzc-1, indexType216kzc, indexType232kzc, indexType322kzc, indexType324kzc, indexType328kzc, indexType3216kzc, indexType3232kzc, indexType22kzd, indexType24kzd, indexType28kzd, indexType216kzd, indexType232kzd-1, indexType322kzd, indexType324kzd, indexType328kzd, indexType3216kzd, indexType3232kzd, indexType22kze, indexType24kze, indexType28kze, indexType216kze, indexType232kze, indexType322kze-1, indexType324kze, indexType328kze, indexType3216kze, indexType3232kze, 0)


# --- finding corresponding average pupil values for each type ---
preMeanType22kz = averagePreSignal[indexType22kz] 
preMeanType24kz = averagePreSignal[indexType24kz] 
preMeanType28kz = averagePreSignal[indexType28kz] 
preMeanType216kz = averagePreSignal[indexType216kz] 
preMeanType232kz = averagePreSignal[indexType232kz] 
           
postMeanType22kz = averagePostSignal[indexType22kz] 
postMeanType24kz = averagePostSignal[indexType24kz] 
postMeanType28kz = averagePostSignal[indexType28kz] 
postMeanType216kz = averagePostSignal[indexType216kz] 
postMeanType232kz = averagePostSignal[indexType232kz]

preMeanType322kz = averagePreSignal[indexType322kz] 
preMeanType324kz = averagePreSignal[indexType324kz] 
preMeanType328kz = averagePreSignal[indexType328kz] 
preMeanType3216kz = averagePreSignal[indexType3216kz-1] 
preMeanType3232kz = averagePreSignal[indexType3232kz] 

postMeanType322kz = averagePostSignal[indexType322kz] 
postMeanType324kz = averagePostSignal[indexType324kz] 
postMeanType328kz = averagePostSignal[indexType328kz] 
postMeanType3216kz = averagePostSignal[indexType3216kz-1] 
postMeanType3232kz = averagePostSignal[indexType3232kz]

preMeanType22kza = averagePreSignal1[indexType22kza] 
preMeanType24kza = averagePreSignal1[indexType24kza] 
preMeanType28kza = averagePreSignal1[indexType28kza] 
preMeanType216kza = averagePreSignal1[indexType216kza] 
preMeanType232kza = averagePreSignal1[indexType232kza] 
           
postMeanType22kza = averagePostSignal1[indexType22kza] 
postMeanType24kza = averagePostSignal1[indexType24kza] 
postMeanType28kza = averagePostSignal1[indexType28kza] 
postMeanType216kza = averagePostSignal1[indexType216kza] 
postMeanType232kza = averagePostSignal1[indexType232kza]

preMeanType322kza = averagePreSignal1[indexType322kza] 
preMeanType324kza = averagePreSignal1[indexType324kza] 
preMeanType328kza = averagePreSignal1[indexType328kza] 
preMeanType3216kza = averagePreSignal1[indexType3216kza] 
preMeanType3232kza = averagePreSignal1[indexType3232kza-1] 

postMeanType322kza = averagePostSignal1[indexType322kza] 
postMeanType324kza = averagePostSignal1[indexType324kza] 
postMeanType328kza = averagePostSignal1[indexType328kza] 
postMeanType3216kza = averagePostSignal1[indexType3216kza] 
postMeanType3232kza = averagePostSignal1[indexType3232kza-1]

preMeanType22kzb = averagePreSignal2[indexType22kzb] 
preMeanType24kzb = averagePreSignal2[indexType24kzb] 
preMeanType28kzb = averagePreSignal2[indexType28kzb] 
preMeanType216kzb = averagePreSignal2[indexType216kzb] 
preMeanType232kzb = averagePreSignal2[indexType232kzb] 
           
postMeanType22kzb = averagePostSignal2[indexType22kzb] 
postMeanType24kzb = averagePostSignal2[indexType24kzb] 
postMeanType28kzb = averagePostSignal2[indexType28kzb] 
postMeanType216kzb = averagePostSignal2[indexType216kzb] 
postMeanType232kzb = averagePostSignal2[indexType232kzb]


preMeanType322kzb = averagePreSignal2[indexType322kzb] 
preMeanType324kzb = averagePreSignal2[indexType324kzb] 
preMeanType328kzb = averagePreSignal2[indexType328kzb] 
preMeanType3216kzb = averagePreSignal2[indexType3216kzb] 
preMeanType3232kzb = averagePreSignal2[indexType3232kzb] 
           
postMeanType322kzb = averagePostSignal2[indexType322kzb] 
postMeanType324kzb = averagePostSignal2[indexType324kzb] 
postMeanType328kzb = averagePostSignal2[indexType328kzb] 
postMeanType3216kzb = averagePostSignal2[indexType3216kzb] 
postMeanType3232kzb = averagePostSignal2[indexType3232kzb]

preMeanType22kzc = averagePreSignal3[indexType22kzc] 
preMeanType24kzc = averagePreSignal3[indexType24kzc] 
preMeanType28kzc = averagePreSignal3[indexType28kzc-1] 
preMeanType216kzc = averagePreSignal3[indexType216kzc] 
preMeanType232kzc = averagePreSignal3[indexType232kz] 
           
postMeanType22kzc = averagePostSignal3[indexType22kzc] 
postMeanType24kzc = averagePostSignal3[indexType24kzc] 
postMeanType28kzc = averagePostSignal3[indexType28kzc-1] 
postMeanType216kzc = averagePostSignal3[indexType216kzc] 
postMeanType232kzc = averagePostSignal3[indexType232kzc]

preMeanType322kzc = averagePreSignal3[indexType322kzc] 
preMeanType324kzc = averagePreSignal3[indexType324kzc] 
preMeanType328kzc = averagePreSignal3[indexType328kzc] 
preMeanType3216kzc = averagePreSignal3[indexType3216kzc] 
preMeanType3232kzc = averagePreSignal3[indexType3232kzc] 
           
postMeanType322kzc = averagePostSignal3[indexType322kzc] 
postMeanType324kzc = averagePostSignal3[indexType324kzc] 
postMeanType328kzc = averagePostSignal3[indexType328kzc] 
postMeanType3216kzc = averagePostSignal3[indexType3216kzc] 
postMeanType3232kzc = averagePostSignal3[indexType3232kzc]

preMeanType22kzd = averagePreSignal4[indexType22kzd] 
preMeanType24kzd = averagePreSignal4[indexType24kzd] 
preMeanType28kzd = averagePreSignal4[indexType28kzd] 
preMeanType216kzd = averagePreSignal4[indexType216kzd] 
preMeanType232kzd = averagePreSignal4[indexType232kzd-1] 
           
postMeanType22kzd = averagePostSignal4[indexType22kzd] 
postMeanType24kzd = averagePostSignal4[indexType24kzd] 
postMeanType28kzd = averagePostSignal4[indexType28kzd] 
postMeanType216kzd = averagePostSignal4[indexType216kzd]
postMeanType232kzd = averagePostSignal4[indexType232kzd-1]

preMeanType322kzd = averagePreSignal4[indexType322kzd] 
preMeanType324kzd = averagePreSignal4[indexType324kzd] 
preMeanType328kzd = averagePreSignal4[indexType328kzd] 
preMeanType3216kzd = averagePreSignal4[indexType3216kzd] 
preMeanType3232kzd = averagePreSignal4[indexType3232kzd] 
           
postMeanType322kzd = averagePostSignal4[indexType322kzd] 
postMeanType324kzd = averagePostSignal4[indexType324kzd] 
postMeanType328kzd = averagePostSignal4[indexType328kzd] 
postMeanType3216kzd = averagePostSignal4[indexType3216kzd] 
postMeanType3232kzd = averagePostSignal4[indexType3232kzd]

preMeanType22kze = averagePreSignal5[indexType22kze] 
preMeanType24kze = averagePreSignal5[indexType24kze] 
preMeanType28kze = averagePreSignal5[indexType28kze] 
preMeanType216kze = averagePreSignal5[indexType216kze] 
preMeanType232kze = averagePreSignal5[indexType232kze] 
           
postMeanType22kze = averagePostSignal5[indexType22kze] 
postMeanType24kze = averagePostSignal5[indexType24kze] 
postMeanType28kze = averagePostSignal5[indexType28kze] 
postMeanType216kze = averagePostSignal5[indexType216kze] 
postMeanType232kze = averagePostSignal5[indexType232kze]

preMeanType322kze = averagePreSignal5[indexType322kze-1] 
preMeanType324kze = averagePreSignal5[indexType324kze] 
preMeanType328kze = averagePreSignal5[indexType328kze] 
preMeanType3216kze = averagePreSignal5[indexType3216kze] 
preMeanType3232kze = averagePreSignal5[indexType3232kze] 
           
postMeanType322kze = averagePostSignal5[indexType322kze-1] 
postMeanType324kze = averagePostSignal5[indexType324kze] 
postMeanType328kze = averagePostSignal5[indexType328kze] 
postMeanType3216kze = averagePostSignal5[indexType3216kze] 
postMeanType3232kze = averagePostSignal5[indexType3232kze]


# --- Finding values in the average signals with each freq type indices






# --- calculating the pre and post values for each freq type across videos --- 
trialsMean2kz1, trialsMean4kz1, trialsMean8kz1, trialsMean16kz1, trialsMean32kz1, trialsMean2kz2, trialsMean4kz2, trialsMean8kz2, trialsMean16kz2, trialsMean32kz2, = calculate_pupil_size_trials(postMeanType22kz, postMeanType24kz, postMeanType28kz, postMeanType216kz, postMeanType232kz, postMeanType322kz, postMeanType324kz, postMeanType328kz, postMeanType3216kz, postMeanType3232kz, postMeanType22kza, postMeanType24kza, postMeanType28kza, postMeanType216kza, postMeanType232kza, postMeanType322kza, postMeanType324kza, postMeanType328kza, postMeanType3216kza, postMeanType3232kza, postMeanType22kzb, postMeanType24kzb, postMeanType28kzb, postMeanType216kzb, postMeanType232kzb, postMeanType322kzb, postMeanType324kzb, postMeanType328kzb, postMeanType3216kzb, postMeanType3232kzb, postMeanType22kzc, postMeanType24kzc, postMeanType28kzc, postMeanType216kzc, postMeanType232kzc, postMeanType322kzc, postMeanType324kzc, postMeanType328kzc, postMeanType3216kzc, postMeanType3232kzc, postMeanType22kzd, postMeanType24kzd, postMeanType28kzd, postMeanType216kzd, postMeanType232kzd, postMeanType322kzd, postMeanType324kzd, postMeanType328kzd, postMeanType3216kzd, postMeanType3232kzd, postMeanType22kze, postMeanType24kze, postMeanType28kze, postMeanType216kze, postMeanType232kze, postMeanType322kze, postMeanType324kze, postMeanType328kze, postMeanType3216kze, postMeanType3232kze, preMeanType22kz, preMeanType24kz, preMeanType28kz, preMeanType216kz, preMeanType232kz, preMeanType322kz, preMeanType324kz, preMeanType328kz, preMeanType3216kz, preMeanType3232kz, preMeanType22kza, preMeanType24kza, preMeanType28kza, preMeanType216kza, preMeanType232kza, preMeanType322kza, preMeanType324kza, preMeanType328kza, preMeanType3216kza, preMeanType3232kza, preMeanType22kzb, preMeanType24kzb, preMeanType28kzb, preMeanType216kzb, preMeanType232kzb, preMeanType322kzb, preMeanType324kzb, preMeanType328kzb, preMeanType3216kzb, preMeanType3232kzb, preMeanType22kzc, preMeanType24kzc, preMeanType28kzc, preMeanType216kzc, preMeanType232kzc, preMeanType322kzc, preMeanType324kzc, preMeanType328kzc, preMeanType3216kzc, preMeanType3232kzc, preMeanType22kzd, preMeanType24kzd, preMeanType28kzd, preMeanType216kzd, preMeanType232kzd, preMeanType322kzd, preMeanType324kzd, preMeanType328kzd, preMeanType3216kzd, preMeanType3232kzd, preMeanType22kze, preMeanType24kze, preMeanType28kze, preMeanType216kze, preMeanType232kze, preMeanType322kze, preMeanType324kze, preMeanType328kze, preMeanType3216kze, preMeanType3232kze)

# --- plotting each freq type vs time --- 
onlyTrialsPlots = plot_trials_only(trialsTime2kz1, trialsTime4kz1, trialsTime8kz1, trialsTime16kz1, trialsTime32kz1, trialsTime2kz2, trialsTime4kz2, trialsTime8kz2, trialsTime16kz2, trialsTime32kz2, trialsMean2kz1, trialsMean4kz1, trialsMean8kz1, trialsMean16kz1, trialsMean32kz1, trialsMean2kz2, trialsMean4kz2, trialsMean8kz2, trialsMean16kz2, trialsMean32kz2)

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
