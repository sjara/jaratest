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
      #preData = np.asarray(preProcessedPreValues)  
      #postData = np.asarray(preProcessedPostValues)
      return(preData, postData, preValuesIndices, postValuesIndices)
      
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
      
# --- Find the location of the given frequencies as args ---

      findPreFreq1 = np.argwhere(freq1 == preFreqArr) #finds indices for 2kHz values in preFreqs
      findPreFreq1Arr = findPreFreq1.flatten()
      findPreFreq2 = np.argwhere(freq5 == preFreqArr) #finds indices for 32kHz values in preFreqs
      findPreFreq2Arr = findPreFreq2.flatten()
      
# --- Find the post freqs corresponding to their pre freqs ---       
      correspondingValues1 = np.take(postFreqArr, findPreFreq1Arr) #finds all post frequencies values for pre 2kHz
      correspondingValues2 = np.take(postFreqArr, findPreFreq2Arr) #finds all post frequencies values for pre 32kHz
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
       
                
def find_type_freqs_pupil_values(preFreqArr, postFreqArr, signal):
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
     '''
     Creates a plot with traces made up with the mean pupil size along the videos
     Args:
     timeData1...3 (np.array) = array containing the time window to evaluate the pupil size
     plotData1...3 (np.array) = array containing the mean pupil size to plot against time
     
     Returns:
     plt.show() = returns a plot with traces of different colors, representing the mean pupil behavior in each video recorded
     '''
 
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
     Calculates the pupil size with normalized values for pre freqs 2kHz and 32kHz, and plots them
     
     Args:
     normVal1...10e (np.array) =  array containing the normalized pupil size for each frequency type
     frequencies (np.array) = array containing the number of frequencies being tested
     
     Returns:
     plot.show() = plots the normalized pupil size across videos for each frequency type
     '''
     
# --- Creating one array per post freqs values across videos in one array ---
     
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

# --- Calculate mean values for each array created in the past step ---
     
     mean2Khz1 = np.nanmean(values2Khz1)
     mean4Khz1 = np.nanmean(values4Khz1)
     mean8Khz1 = np.nanmean(values8Khz1)
     mean16Khz1 = np.nanmean(values16Khz1)
     mean32Khz1 = np.nanmean(values32Khz1)
     mean2Khz2 = np.nanmean(values2Khz2)
     mean4Khz2 = np.nanmean(values4Khz2)
     mean8Khz2 = np.nanmean(values8Khz2)
     mean16Khz2 = np.nanmean(values16Khz2)
     mean32Khz2 = np.nanmean(values32Khz2)
     meanPre2Khz1 = np.nanmean(pre2Khz1)
     meanPre4Khz1 = np.nanmean(pre4Khz1)
     meanPre8Khz1 = np.nanmean(pre8Khz1)
     meanPre16Khz1 = np.nanmean(pre16Khz1)
     meanPre32Khz1 = np.nanmean(pre32Khz1)
     meanPre2Khz2 = np.nanmean(pre2Khz2)
     meanPre4Khz2 = np.nanmean(pre4Khz2)
     meanPre8Khz2 = np.nanmean(pre8Khz2)
     meanPre16Khz2 = np.nanmean(pre16Khz2)
     meanPre32Khz2 = np.nanmean(pre32Khz2)

# --- Round mean values decimals so it is easier to see in the plot --- 
     
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
     
# --- Calculate the deviation bars for each frequency type --- 

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
     
# --- Create an array with the errors and mean values for freqs type with pre 2kHz and pre 32kHz ---
    
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

          
# --- Plot the results ---
     
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
     plotVal[1,0].plot(preXaxis32, preValPlot32, color ='r', marker ='o', label = secondLegend) # Red dot in plot
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
     plotVal[0,1].set_ylim([-0.01, 0.05])
     plotVal[1,1].set_ylim([-0.01, 0.05])
     plotVal[0,0].legend(prop ={"size":10})
     plotVal[0,1].legend(prop ={"size":10})
     plotVal[1,0].legend(prop ={"size":10})
     plotVal[1,1].legend(prop ={"size":10})
     plt.show() 
     
     return(plt.show())

def calculate_pupil_size_trials(value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,  value1a, value2a, value3a, value4a, value5a, value6a, value7a, value8a, value9a, value10a, value1b, value2b, value3b, value4b, value5b, value6b, value7b, value8b, value9b, value10b, value1c, value2c, value3c, value4c, value5c, value6c, value7c, value8c, value9c, value10c, value1d, value2d, value3d, value4d, value5d, value6d, value7d, value8d, value9d, value10d, value1e, value2e, value3e, value4e, value5e, value6e, value7e, value8e, value9e, value10e, preVal1, preVal2, preVal3, preVal4, preVal5, preVal6, preVal7, preVal8, preVal9, preVal10, preVal1a, preVal2a, preVal3a, preVal4a, preVal5a, preVal6a, preVal7a, preVal8a, preVal9a, preVal10a, preVal1b, preVal2b, preVal3b, preVal4b, preVal5b, preVal6b, preVal7b, preVal8b, preVal9b, preVal10b, preVal1c, preVal2c, preVal3c, preVal4c, preVal5c, preVal6c, preVal7c, preVal8c, preVal9c, preVal10c, preVal1d, preVal2d, preVal3d, preVal4d, preVal5d, preVal6d, preVal7d, preVal8d, preVal9d, preVal10d, preVal1e, preVal2e, preVal3e, preVal4e, preVal5e, preVal6e, preVal7e, preVal8e, preVal9e, preVal10e, index1, index2 ,index3 ,index4, index5, index6, index7 ,index8, index9, index10, index1a, index2a ,index3a, index4a, index5a, index6a, index7a ,index8a, index9a, index10a, index1b, index2b, index3b ,index4b, index5b, index6b, index7b ,index8b, index9b, index10b, index1c, index2c ,index3c ,index4c, index5c, index6c, index7c ,index8c, index9c, index10c, index1d, index2d ,index3d ,index4d, index5d, index6d, index7d ,index8d, index9d, index10d, index1e, index2e ,index3e, index4e, index5e, index6e, index7e, index8e, index9e, index10e, preSignal, postSignal):
     '''
     Returns the pre and post values for each frequency type in their respective trials
     
     Args:
     value1...value10e (np.array) = post values of each frequency type of each video
     preVal1...preValue10e (np.array) = pre valus of each frequency type of each video
     index1...10e (np.array) = index corresponding to each one of the positions of the pre and post freqs for each freq type
     preSignal (np.array) = array containing the values of the pupil size during the pre period
     postSignal (np.array) = array containing the vlaues of the pupils size during the post period
     
     Returns:
     trialsVal2kHz1... 32kHz1 (np.array) = array containing all the pre and post values across videos for the frequency types with a pre period frequency of 2kHz
     trialsVal2kHz2... 32kHz2 (np.array) = array containing all the pre and post values across videos for the frequency types with a pre period frequency of 32kHz
      
     '''
# --- transform into arrays the data input ---     
     arrValue1 = np.array([value1])
     arrValue2 = np.array([value2])
     arrValue3 = np.array([value3])
     arrValue4 = np.array([value4])
     arrValue5 = np.array([value5])
     arrValue6 = np.array([value6])
     arrValue7 = np.array([value7])
     arrValue8 = np.array([value8])
     arrValue9 = np.array([value9])
     arrValue10 = np.array([value10])
     
     arrValue1a = np.array([value1a])
     arrValue2a = np.array([value2a])
     arrValue3a = np.array([value3a])
     arrValue4a = np.array([value4a])
     arrValue5a = np.array([value5a])
     arrValue6a = np.array([value6a])
     arrValue7a = np.array([value7a])
     arrValue8a = np.array([value8a])
     arrValue9a = np.array([value9a])
     arrValue10a = np.array([value10a])
     
     arrValue1b = np.array([value1b])
     arrValue2b = np.array([value2b])
     arrValue3b = np.array([value3b])
     arrValue4b = np.array([value4b])
     arrValue5b = np.array([value5b])
     arrValue6b = np.array([value6b])
     arrValue7b = np.array([value7b])
     arrValue8b = np.array([value8b])
     arrValue9b = np.array([value9b])
     arrValue10b = np.array([value10b]) 
     
     arrValue1c = np.array([value1c])
     arrValue2c = np.array([value2c])
     arrValue3c = np.array([value3c])
     arrValue4c = np.array([value4c])
     arrValue5c = np.array([value5c])
     arrValue6c = np.array([value6c])
     arrValue7c = np.array([value7c])
     arrValue8c = np.array([value8c])
     arrValue9c = np.array([value9c])
     arrValue10c = np.array([value10c])
     
     arrValue1d = np.array([value1d])
     arrValue2d = np.array([value2d])
     arrValue3d = np.array([value3d])
     arrValue4d = np.array([value4d])
     arrValue5d = np.array([value5d])
     arrValue6d = np.array([value6d])
     arrValue7d = np.array([value7d])
     arrValue8d = np.array([value8d])
     arrValue9d = np.array([value9d])
     arrValue10d = np.array([value10d])

     arrValue1e = np.array([value1e])
     arrValue2e = np.array([value2e])
     arrValue3e = np.array([value3e])
     arrValue4e = np.array([value4e])
     arrValue5e = np.array([value5e])
     arrValue6e = np.array([value6e])
     arrValue7e = np.array([value7e])
     arrValue8e = np.array([value8e])
     arrValue9e = np.array([value9e])
     arrValue10e = np.array([value10e])                   
  
     arrPreValue1 = np.array([preVal1])
     arrPreValue2 = np.array([preVal2])
     arrPreValue3 = np.array([preVal3])
     arrPreValue4 = np.array([preVal4])
     arrPreValue5 = np.array([preVal5])
     arrPreValue6 = np.array([preVal6])
     arrPreValue7 = np.array([preVal7])
     arrPreValue8 = np.array([preVal8])
     arrPreValue9 = np.array([preVal9])
     arrPreValue10 = np.array([preVal10])
     
     arrPreValue1a = np.array([preVal1a])
     arrPreValue2a = np.array([preVal2a])
     arrPreValue3a = np.array([preVal3a])
     arrPreValue4a = np.array([preVal4a])
     arrPreValue5a = np.array([preVal5a])
     arrPreValue6a = np.array([preVal6a])
     arrPreValue7a = np.array([preVal7a])
     arrPreValue8a = np.array([preVal8a])
     arrPreValue9a = np.array([preVal9a])
     arrPreValue10a = np.array([preVal10a])     
     
     arrPreValue1b = np.array([preVal1b])
     arrPreValue2b = np.array([preVal2b])
     arrPreValue3b = np.array([preVal3b])
     arrPreValue4b = np.array([preVal4b])
     arrPreValue5b = np.array([preVal5b])
     arrPreValue6b = np.array([preVal6b])
     arrPreValue7b = np.array([preVal7b])
     arrPreValue8b = np.array([preVal8b])
     arrPreValue9b = np.array([preVal9b])
     arrPreValue10b = np.array([preVal10b])
     
     arrPreValue1c = np.array([preVal1c])
     arrPreValue2c = np.array([preVal2c])
     arrPreValue3c = np.array([preVal3c])
     arrPreValue4c = np.array([preVal4c])
     arrPreValue5c = np.array([preVal5c])
     arrPreValue6c = np.array([preVal6c])
     arrPreValue7c = np.array([preVal7c])
     arrPreValue8c = np.array([preVal8c])
     arrPreValue9c = np.array([preVal9c])
     arrPreValue10c = np.array([preVal10c])
     
     arrPreValue1d = np.array([preVal1d])
     arrPreValue2d = np.array([preVal2d])
     arrPreValue3d = np.array([preVal3d])
     arrPreValue4d = np.array([preVal4d])
     arrPreValue5d = np.array([preVal5d])
     arrPreValue6d = np.array([preVal6d])
     arrPreValue7d = np.array([preVal7d])
     arrPreValue8d = np.array([preVal8d])
     arrPreValue9d = np.array([preVal9d])
     arrPreValue10d = np.array([preVal10d])
     
     arrPreValue1e = np.array([preVal1e])
     arrPreValue2e = np.array([preVal2e])
     arrPreValue3e = np.array([preVal3e])
     arrPreValue4e = np.array([preVal4e])
     arrPreValue5e = np.array([preVal5e])
     arrPreValue6e = np.array([preVal6e])
     arrPreValue7e = np.array([preVal7e])
     arrPreValue8e = np.array([preVal8e])
     arrPreValue9e = np.array([preVal9e])
     arrPreValue10e = np.array([preVal10e])                    

# --- Reshape arrays so they contain the corresponding rows and columns from the preIndicesTime and indexType variables ---       

     arrPost2khz1 = np.resize(arrValue1,(postSignal.shape[0], index1.shape[0]))
     arrPost4khz1 = np.resize(arrValue2,(postSignal.shape[0], index2.shape[0]))
     arrPost8khz1 = np.resize(arrValue3,(postSignal.shape[0], index3.shape[0]))
     arrPost16khz1 = np.resize(arrValue4,(postSignal.shape[0], index4.shape[0]))
     arrPost32khz1 = np.resize(arrValue5,(postSignal.shape[0], index5.shape[0]))
     arrPost2khz2 = np.resize(arrValue6,(postSignal.shape[0], index6.shape[0]))
     arrPost4khz2 = np.resize(arrValue7,(postSignal.shape[0], index7.shape[0]))
     arrPost8khz2 = np.resize(arrValue8,(postSignal.shape[0], index8.shape[0]))
     arrPost16khz2 = np.resize(arrValue9,(postSignal.shape[0], index9.shape[0]))
     arrPost32khz2 = np.resize(arrValue10,(postSignal.shape[0], index10.shape[0]))
     
     arrPost2khz1a = np.resize(arrValue1a,(postSignal.shape[0], index1a.shape[0]))
     arrPost4khz1a = np.resize(arrValue2a,(postSignal.shape[0], index2a.shape[0]))
     arrPost8khz1a = np.resize(arrValue3a,(postSignal.shape[0], index3a.shape[0]))
     arrPost16khz1a = np.resize(arrValue4a,(postSignal.shape[0], index4a.shape[0]))
     arrPost32khz1a = np.resize(arrValue5a,(postSignal.shape[0], index5a.shape[0]))
     arrPost2khz2a = np.resize(arrValue6a,(postSignal.shape[0], index6a.shape[0]))
     arrPost4khz2a = np.resize(arrValue7a,(postSignal.shape[0], index7a.shape[0]))
     arrPost8khz2a = np.resize(arrValue8a,(postSignal.shape[0], index8a.shape[0]))
     arrPost16khz2a = np.resize(arrValue9a,(postSignal.shape[0], index9a.shape[0]))
     arrPost32khz2a = np.resize(arrValue10a,(postSignal.shape[0], index10a.shape[0]))
     
     arrPost2khz1b = np.resize(arrValue1b,(postSignal.shape[0], index1b.shape[0]))
     arrPost4khz1b = np.resize(arrValue2b,(postSignal.shape[0], index2b.shape[0]))
     arrPost8khz1b = np.resize(arrValue3b,(postSignal.shape[0], index3b.shape[0]))
     arrPost16khz1b = np.resize(arrValue4b,(postSignal.shape[0], index4b.shape[0]))
     arrPost32khz1b = np.resize(arrValue5b,(postSignal.shape[0], index5b.shape[0]))
     arrPost2khz2b = np.resize(arrValue6b,(postSignal.shape[0], index6b.shape[0]))
     arrPost4khz2b = np.resize(arrValue7b,(postSignal.shape[0], index7b.shape[0]))
     arrPost8khz2b = np.resize(arrValue8b,(postSignal.shape[0], index8b.shape[0]))
     arrPost16khz2b = np.resize(arrValue9b,(postSignal.shape[0], index9b.shape[0]))
     arrPost32khz2b = np.resize(arrValue10b,(postSignal.shape[0], index10b.shape[0]))
     
     arrPost2khz1c = np.resize(arrValue1c,(postSignal.shape[0], index1c.shape[0]))
     arrPost4khz1c = np.resize(arrValue2c,(postSignal.shape[0], index2c.shape[0]))
     arrPost8khz1c = np.resize(arrValue3c,(postSignal.shape[0], index3c.shape[0]))
     arrPost16khz1c = np.resize(arrValue4c,(postSignal.shape[0], index4c.shape[0]))
     arrPost32khz1c = np.resize(arrValue5c,(postSignal.shape[0], index5c.shape[0]))
     arrPost2khz2c = np.resize(arrValue6c,(postSignal.shape[0], index6c.shape[0]))
     arrPost4khz2c = np.resize(arrValue7c,(postSignal.shape[0], index7c.shape[0]))
     arrPost8khz2c = np.resize(arrValue8c,(postSignal.shape[0], index8c.shape[0]))
     arrPost16khz2c = np.resize(arrValue9c,(postSignal.shape[0], index9c.shape[0]))
     arrPost32khz2c = np.resize(arrValue10c,(postSignal.shape[0], index10c.shape[0]))
     
     arrPost2khz1d = np.resize(arrValue1d,(postSignal.shape[0], index1d.shape[0]))
     arrPost4khz1d = np.resize(arrValue2d,(postSignal.shape[0], index2d.shape[0]))
     arrPost8khz1d = np.resize(arrValue3d,(postSignal.shape[0], index3d.shape[0]))
     arrPost16khz1d = np.resize(arrValue4d,(postSignal.shape[0], index4d.shape[0]))
     arrPost32khz1d = np.resize(arrValue5d,(postSignal.shape[0], index5d.shape[0]))
     arrPost2khz2d = np.resize(arrValue6d,(postSignal.shape[0], index6d.shape[0]))
     arrPost4khz2d = np.resize(arrValue7d,(postSignal.shape[0], index7d.shape[0]))
     arrPost8khz2d = np.resize(arrValue8d,(postSignal.shape[0], index8d.shape[0]))
     arrPost16khz2d = np.resize(arrValue9d,(postSignal.shape[0], index9d.shape[0]))
     arrPost32khz2d = np.resize(arrValue10d,(postSignal.shape[0], index10d.shape[0]))           
     
     arrPost2khz1e = np.resize(arrValue1e,(postSignal.shape[0], index1e.shape[0]))
     arrPost4khz1e = np.resize(arrValue2e,(postSignal.shape[0], index2e.shape[0]))
     arrPost8khz1e = np.resize(arrValue3e,(postSignal.shape[0], index3e.shape[0]))
     arrPost16khz1e = np.resize(arrValue4e,(postSignal.shape[0], index4e.shape[0]))
     arrPost32khz1e = np.resize(arrValue5e,(postSignal.shape[0], index5e.shape[0]))
     arrPost2khz2e = np.resize(arrValue6e,(postSignal.shape[0], index6e.shape[0]))
     arrPost4khz2e = np.resize(arrValue7e,(postSignal.shape[0], index7e.shape[0]))
     arrPost8khz2e = np.resize(arrValue8e,(postSignal.shape[0], index8e.shape[0]))
     arrPost16khz2e = np.resize(arrValue9e,(postSignal.shape[0], index9e.shape[0]))
     arrPost32khz2e = np.resize(arrValue10e,(postSignal.shape[0], index10e.shape[0]))

     arrPre2khz1 = np.resize(arrPreValue1,(preSignal.shape[0], index1.shape[0]))
     arrPre4khz1 = np.resize(arrPreValue2,(preSignal.shape[0], index2.shape[0]))
     arrPre8khz1 = np.resize(arrPreValue3,(preSignal.shape[0], index3.shape[0]))
     arrPre16khz1 = np.resize(arrPreValue4,(preSignal.shape[0], index4.shape[0]))
     arrPre32khz1 = np.resize(arrPreValue5,(preSignal.shape[0], index5.shape[0]))
     arrPre2khz2 = np.resize(arrPreValue6,(preSignal.shape[0], index6.shape[0]))
     arrPre4khz2 = np.resize(arrPreValue7,(preSignal.shape[0], index7.shape[0]))
     arrPre8khz2 = np.resize(arrPreValue8,(preSignal.shape[0], index8.shape[0]))
     arrPre16khz2 = np.resize(arrPreValue9,(preSignal.shape[0], index9.shape[0]))
     arrPre32khz2 = np.resize(arrPreValue10,(preSignal.shape[0], index10.shape[0]))
     
     arrPre2khz1a = np.resize(arrPreValue1a,(preSignal.shape[0], index1a.shape[0]))
     arrPre4khz1a = np.resize(arrPreValue2a,(preSignal.shape[0], index2a.shape[0]))
     arrPre8khz1a = np.resize(arrPreValue3a,(preSignal.shape[0], index3a.shape[0]))
     arrPre16khz1a = np.resize(arrPreValue4a,(preSignal.shape[0], index4a.shape[0]))
     arrPre32khz1a = np.resize(arrPreValue5a,(preSignal.shape[0], index5a.shape[0]))
     arrPre2khz2a = np.resize(arrPreValue6a,(preSignal.shape[0], index6a.shape[0]))
     arrPre4khz2a = np.resize(arrPreValue7a,(preSignal.shape[0], index7a.shape[0]))
     arrPre8khz2a = np.resize(arrPreValue8a,(preSignal.shape[0], index8a.shape[0]))
     arrPre16khz2a = np.resize(arrPreValue9a,(preSignal.shape[0], index9a.shape[0]))
     arrPre32khz2a = np.resize(arrPreValue10a,(preSignal.shape[0], index10a.shape[0]))
     
     arrPre2khz1b = np.resize(arrPreValue1b,(preSignal.shape[0], index1b.shape[0]))
     arrPre4khz1b = np.resize(arrPreValue2b,(preSignal.shape[0], index2b.shape[0]))
     arrPre8khz1b = np.resize(arrPreValue3b,(preSignal.shape[0], index3b.shape[0]))
     arrPre16khz1b = np.resize(arrPreValue4b,(preSignal.shape[0], index4b.shape[0]))
     arrPre32khz1b = np.resize(arrPreValue5b,(preSignal.shape[0], index5b.shape[0]))
     arrPre2khz2b = np.resize(arrPreValue6b,(preSignal.shape[0], index6b.shape[0]))
     arrPre4khz2b = np.resize(arrPreValue7b,(preSignal.shape[0], index7b.shape[0]))
     arrPre8khz2b = np.resize(arrPreValue8b,(preSignal.shape[0], index8b.shape[0]))
     arrPre16khz2b = np.resize(arrPreValue9b,(preSignal.shape[0], index9b.shape[0]))
     arrPre32khz2b = np.resize(arrPreValue10b,(preSignal.shape[0], index10b.shape[0]))
     
     arrPre2khz1c = np.resize(arrPreValue1c,(preSignal.shape[0], index1c.shape[0]))
     arrPre4khz1c = np.resize(arrPreValue2c,(preSignal.shape[0], index2c.shape[0]))
     arrPre8khz1c = np.resize(arrPreValue3c,(preSignal.shape[0], index3c.shape[0]))
     arrPre16khz1c = np.resize(arrPreValue4c,(preSignal.shape[0], index4c.shape[0]))
     arrPre32khz1c = np.resize(arrPreValue5c,(preSignal.shape[0], index5c.shape[0]))
     arrPre2khz2c = np.resize(arrPreValue6c,(preSignal.shape[0], index6c.shape[0]))
     arrPre4khz2c = np.resize(arrPreValue7c,(preSignal.shape[0], index7c.shape[0]))
     arrPre8khz2c = np.resize(arrPreValue8c,(preSignal.shape[0], index8c.shape[0]))
     arrPre16khz2c = np.resize(arrPreValue9c,(preSignal.shape[0], index9c.shape[0]))
     arrPre32khz2c = np.resize(arrPreValue10c,(preSignal.shape[0], index10c.shape[0]))
     
     arrPre2khz1d = np.resize(arrPreValue1d,(preSignal.shape[0], index1d.shape[0]))
     arrPre4khz1d = np.resize(arrPreValue2d,(preSignal.shape[0], index2d.shape[0]))
     arrPre8khz1d = np.resize(arrPreValue3d,(preSignal.shape[0], index3d.shape[0]))
     arrPre16khz1d = np.resize(arrPreValue4d,(preSignal.shape[0], index4d.shape[0]))
     arrPre32khz1d = np.resize(arrPreValue5d,(preSignal.shape[0], index5d.shape[0]))
     arrPre2khz2d = np.resize(arrPreValue6d,(preSignal.shape[0], index6d.shape[0]))
     arrPre4khz2d = np.resize(arrPreValue7d,(preSignal.shape[0], index7d.shape[0]))
     arrPre8khz2d = np.resize(arrPreValue8d,(preSignal.shape[0], index8d.shape[0]))
     arrPre16khz2d = np.resize(arrPreValue9d,(preSignal.shape[0], index9d.shape[0]))
     arrPre32khz2d = np.resize(arrPreValue10d,(preSignal.shape[0], index10d.shape[0]))
     
     arrPre2khz1e = np.resize(arrPreValue1e,(preSignal.shape[0], index1e.shape[0]))
     arrPre4khz1e = np.resize(arrPreValue2e,(preSignal.shape[0], index2e.shape[0]))
     arrPre8khz1e = np.resize(arrPreValue3e,(preSignal.shape[0], index3e.shape[0]))
     arrPre16khz1e = np.resize(arrPreValue4e,(preSignal.shape[0], index4e.shape[0]))
     arrPre32khz1e = np.resize(arrPreValue5e,(preSignal.shape[0], index5e.shape[0]))
     arrPre2khz2e = np.resize(arrPreValue6e,(preSignal.shape[0], index6e.shape[0]))
     arrPre4khz2e = np.resize(arrPreValue7e,(preSignal.shape[0], index7e.shape[0]))
     arrPre8khz2e = np.resize(arrPreValue8e,(preSignal.shape[0], index8e.shape[0]))
     arrPre16khz2e = np.resize(arrPreValue9e,(preSignal.shape[0], index9e.shape[0]))
     arrPre32khz2e = np.resize(arrPreValue10e,(preSignal.shape[0], index10e.shape[0]))
     
     
# --- Calculate mean row-wise ---               
     
     meanPost2kz1 = arrPost2khz1.mean(axis = 1)
     meanPost4kz1 = arrPost4khz1.mean(axis = 1)
     meanPost8kz1 = arrPost8khz1.mean(axis = 1)
     meanPost16kz1 = arrPost16khz1.mean(axis = 1)
     meanPost32kz1 = arrPost32khz1.mean(axis = 1)
     meanPost2kz2 = arrPost2khz2.mean(axis = 1)
     meanPost4kz2 = arrPost4khz2.mean(axis = 1)
     meanPost8kz2 = arrPost8khz2.mean(axis = 1)
     meanPost16kz2 = arrPost16khz2.mean(axis = 1)
     meanPost32kz2 = arrPost32khz2.mean(axis = 1)
     
     meanPost2kz1a = arrPost2khz1a.mean(axis = 1)
     meanPost4kz1a = arrPost4khz1a.mean(axis = 1)
     meanPost8kz1a = arrPost8khz1a.mean(axis = 1)
     meanPost16kz1a = arrPost16khz1a.mean(axis = 1)
     meanPost32kz1a = arrPost32khz1a.mean(axis = 1)
     meanPost2kz2a = arrPost2khz2a.mean(axis = 1)
     meanPost4kz2a = arrPost4khz2a.mean(axis = 1)
     meanPost8kz2a = arrPost8khz2a.mean(axis = 1)
     meanPost16kz2a = arrPost16khz2a.mean(axis = 1)
     meanPost32kz2a = arrPost32khz2a.mean(axis = 1)
     
     meanPost2kz1b = arrPost2khz1b.mean(axis = 1)
     meanPost4kz1b = arrPost4khz1b.mean(axis = 1)
     meanPost8kz1b = arrPost8khz1b.mean(axis = 1)
     meanPost16kz1b = arrPost16khz1b.mean(axis = 1)
     meanPost32kz1b = arrPost32khz1b.mean(axis = 1)
     meanPost2kz2b = arrPost2khz2b.mean(axis = 1)
     meanPost4kz2b = arrPost4khz2b.mean(axis = 1)
     meanPost8kz2b = arrPost8khz2b.mean(axis = 1)
     meanPost16kz2b = arrPost16khz2b.mean(axis = 1)
     meanPost32kz2b = arrPost32khz2b.mean(axis = 1)          
     
     meanPost2kz1c = arrPost2khz1c.mean(axis = 1)
     meanPost4kz1c = arrPost4khz1c.mean(axis = 1)
     meanPost8kz1c = arrPost8khz1c.mean(axis = 1)
     meanPost16kz1c = arrPost16khz1c.mean(axis = 1)
     meanPost32kz1c = arrPost32khz1c.mean(axis = 1)
     meanPost2kz2c = arrPost2khz2c.mean(axis = 1)
     meanPost4kz2c = arrPost4khz2c.mean(axis = 1)
     meanPost8kz2c = arrPost8khz2c.mean(axis = 1)
     meanPost16kz2c = arrPost16khz2c.mean(axis = 1)
     meanPost32kz2c = arrPost32khz2c.mean(axis = 1)     
     
     meanPost2kz1d = arrPost2khz1d.mean(axis = 1)
     meanPost4kz1d = arrPost4khz1d.mean(axis = 1)
     meanPost8kz1d = arrPost8khz1d.mean(axis = 1)
     meanPost16kz1d = arrPost16khz1d.mean(axis = 1)
     meanPost32kz1d = arrPost32khz1d.mean(axis = 1)
     meanPost2kz2d = arrPost2khz2d.mean(axis = 1)
     meanPost4kz2d = arrPost4khz2d.mean(axis = 1)
     meanPost8kz2d = arrPost8khz2d.mean(axis = 1)
     meanPost16kz2d = arrPost16khz2d.mean(axis = 1)
     meanPost32kz2d = arrPost32khz2d.mean(axis = 1)     
     
     meanPost2kz1e = arrPost2khz1e.mean(axis = 1)
     meanPost4kz1e = arrPost4khz1e.mean(axis = 1)
     meanPost8kz1e = arrPost8khz1e.mean(axis = 1)
     meanPost16kz1e = arrPost16khz1e.mean(axis = 1)
     meanPost32kz1e = arrPost32khz1e.mean(axis = 1)
     meanPost2kz2e = arrPost2khz2e.mean(axis = 1)
     meanPost4kz2e = arrPost4khz2e.mean(axis = 1)
     meanPost8kz2e = arrPost8khz2e.mean(axis = 1)
     meanPost16kz2e = arrPost16khz2e.mean(axis = 1)
     meanPost32kz2e = arrPost32khz2e.mean(axis = 1)
     
     meanPre2kz1 = arrPre2khz1.mean(axis = 1)
     meanPre4kz1 = arrPre4khz1.mean(axis = 1)     
     meanPre8kz1 = arrPre8khz1.mean(axis = 1)
     meanPre16kz1 = arrPre16khz1.mean(axis = 1)
     meanPre32kz1 = arrPre32khz1.mean(axis = 1)
     meanPre2kz2 = arrPre2khz2.mean(axis = 1)
     meanPre4kz2 = arrPre4khz2.mean(axis = 1)
     meanPre8kz2 = arrPre8khz2.mean(axis = 1)
     meanPre16kz2 = arrPre16khz2.mean(axis = 1)
     meanPre32kz2 = arrPre32khz2.mean(axis = 1)
     
     meanPre2kz1a = arrPre2khz1a.mean(axis = 1)
     meanPre4kz1a = arrPre4khz1a.mean(axis = 1)     
     meanPre8kz1a = arrPre8khz1a.mean(axis = 1)
     meanPre16kz1a = arrPre16khz1a.mean(axis = 1)
     meanPre32kz1a = arrPre32khz1a.mean(axis = 1)
     meanPre2kz2a = arrPre2khz2a.mean(axis = 1)
     meanPre4kz2a = arrPre4khz2a.mean(axis = 1)
     meanPre8kz2a = arrPre8khz2a.mean(axis = 1)
     meanPre16kz2a = arrPre16khz2a.mean(axis = 1)
     meanPre32kz2a = arrPre32khz2a.mean(axis = 1)     
     
     meanPre2kz1b = arrPre2khz1b.mean(axis = 1)
     meanPre4kz1b = arrPre4khz1b.mean(axis = 1)     
     meanPre8kz1b = arrPre8khz1b.mean(axis = 1)
     meanPre16kz1b = arrPre16khz1b.mean(axis = 1)
     meanPre32kz1b = arrPre32khz1b.mean(axis = 1)
     meanPre2kz2b = arrPre2khz2b.mean(axis = 1)
     meanPre4kz2b = arrPre4khz2b.mean(axis = 1)
     meanPre8kz2b = arrPre8khz2b.mean(axis = 1)
     meanPre16kz2b = arrPre16khz2b.mean(axis = 1)
     meanPre32kz2b = arrPre32khz2b.mean(axis = 1)     
     
     meanPre2kz1c = arrPre2khz1c.mean(axis = 1)
     meanPre4kz1c = arrPre4khz1c.mean(axis = 1)     
     meanPre8kz1c = arrPre8khz1c.mean(axis = 1)
     meanPre16kz1c = arrPre16khz1c.mean(axis = 1)
     meanPre32kz1c = arrPre32khz1c.mean(axis = 1)
     meanPre2kz2c = arrPre2khz2c.mean(axis = 1)
     meanPre4kz2c = arrPre4khz2c.mean(axis = 1)
     meanPre8kz2c = arrPre8khz2c.mean(axis = 1)
     meanPre16kz2c = arrPre16khz2c.mean(axis = 1)
     meanPre32kz2c = arrPre32khz2c.mean(axis = 1)
     
     meanPre2kz1d = arrPre2khz1d.mean(axis = 1)
     meanPre4kz1d = arrPre4khz1d.mean(axis = 1)     
     meanPre8kz1d = arrPre8khz1d.mean(axis = 1)
     meanPre16kz1d = arrPre16khz1d.mean(axis = 1)
     meanPre32kz1d = arrPre32khz1d.mean(axis = 1)
     meanPre2kz2d = arrPre2khz2d.mean(axis = 1)
     meanPre4kz2d = arrPre4khz2d.mean(axis = 1)
     meanPre8kz2d = arrPre8khz2d.mean(axis = 1)
     meanPre16kz2d = arrPre16khz2d.mean(axis = 1)
     meanPre32kz2d = arrPre32khz2d.mean(axis = 1)          
     
     meanPre2kz1e = arrPre2khz1e.mean(axis = 1)
     meanPre4kz1e = arrPre4khz1e.mean(axis = 1)     
     meanPre8kz1e = arrPre8khz1e.mean(axis = 1)
     meanPre16kz1e = arrPre16khz1e.mean(axis = 1)
     meanPre32kz1e = arrPre32khz1e.mean(axis = 1)
     meanPre2kz2e = arrPre2khz2e.mean(axis = 1)
     meanPre4kz2e = arrPre4khz2e.mean(axis = 1)
     meanPre8kz2e = arrPre8khz2e.mean(axis = 1)
     meanPre16kz2e = arrPre16khz2e.mean(axis = 1)
     meanPre32kz2e = arrPre32khz2e.mean(axis = 1)
     
          
# --- Create an array per post and pre frequency ---
      
     values2Khz1 = np.concatenate((meanPost2kz1, meanPost2kz1a, meanPost2kz1b, meanPost2kz1c, meanPost2kz1d, meanPost2kz1e), axis = 0)
     values4Khz1 = np.concatenate((meanPost4kz1, meanPost4kz1a, meanPost4kz1b, meanPost4kz1, meanPost4kz1d, meanPost4kz1e), axis = 0)
     values8Khz1 = np.concatenate((meanPost8kz1, meanPost8kz1a, meanPost8kz1b, meanPost8kz1c, meanPost8kz1d, meanPost8kz1e), axis = 0)
     values16Khz1 = np.concatenate((meanPost16kz1, meanPost16kz1a, meanPost16kz1b, meanPost16kz1c, meanPost16kz1d, meanPost16kz1e), axis = 0)
     values32Khz1 = np.concatenate((meanPost32kz1, meanPost32kz1a, meanPost32kz1b, meanPost32kz1c, meanPost32kz1d, meanPost32kz1e), axis = 0)
     values2Khz2 = np.concatenate((meanPost2kz2, meanPost2kz2a, meanPost2kz2b, meanPost2kz2c, meanPost2kz2d, meanPost2kz2e), axis = 0)
     values4Khz2 = np.concatenate((meanPost4kz2, meanPost4kz2a, meanPost4kz2b, meanPost4kz2c, meanPost4kz2d, meanPost4kz2e), axis = 0)
     values8Khz2 = np.concatenate((meanPost8kz2, meanPost8kz2a, meanPost8kz2b, meanPost8kz2c, meanPost8kz2d, meanPost8kz2e), axis = 0)
     values16Khz2 = np.concatenate((meanPost16kz2, meanPost16kz2a, meanPost16kz2b, meanPost16kz2c, meanPost16kz2d, meanPost16kz2e), axis = 0)
     values32Khz2 = np.concatenate((meanPost32kz2, meanPost32kz2a, meanPost32kz2b, meanPost32kz2c, meanPost32kz2d, meanPost32kz2e), axis = 0)
     
     trialsVal2kHz1 = np.concatenate((meanPre2kz1, meanPost2kz1, meanPre2kz1a, meanPost2kz1a, meanPre2kz1b, meanPost2kz1b, meanPre2kz1c, meanPost2kz1c, meanPre2kz1d, meanPost2kz1d, meanPre2kz1e, meanPost2kz1e), axis = 0)
     
     trialsVal4kHz1 = np.concatenate((meanPre4kz1, meanPost4kz1, meanPre4kz1a, meanPost4kz1a, meanPre4kz1b, meanPost4kz1b, meanPre4kz1c, meanPost4kz1c, meanPre4kz1d, meanPost4kz1d, meanPre4kz1e, meanPost4kz1e), axis = 0)
     
     trialsVal8kHz1 = np.concatenate((meanPre8kz1, meanPost8kz1, meanPre8kz1a, meanPost8kz1a, meanPre8kz1b, meanPost8kz1b, meanPre8kz1c, meanPost8kz1c, meanPre8kz1d, meanPost8kz1d, meanPre8kz1e, meanPost8kz1e), axis = 0)
     
     trialsVal16kHz1 = np.concatenate((meanPre16kz1, meanPost16kz1, meanPre16kz1a, meanPost16kz1a, meanPre16kz1b, meanPost16kz1b, meanPre16kz1c, meanPost16kz1c, meanPre16kz1d, meanPost16kz1d, meanPre16kz1e, meanPost16kz1e), axis = 0)
     
     trialsVal32kHz1 = np.concatenate((meanPre32kz1, meanPost32kz1, meanPre32kz1a, meanPost32kz1a, meanPre32kz1b, meanPost32kz1b, meanPre32kz1c, meanPost32kz1c, meanPre32kz1d, meanPost32kz1d, meanPre32kz1e, meanPost32kz1e), axis = 0)
     
     trialsVal2kHz2 = np.concatenate((meanPre2kz2, meanPost2kz2, meanPre2kz2a, meanPost2kz2a, meanPre2kz2b, meanPost2kz2b, meanPre2kz2c, meanPost2kz2c, meanPre2kz2d, meanPost2kz2d, meanPre2kz2e, meanPost2kz2e), axis = 0)
     
     trialsVal4kHz2 = np.concatenate((meanPre4kz2, meanPost4kz2, meanPre4kz2a, meanPost4kz2a, meanPre4kz2b, meanPost4kz2b, meanPre4kz2c, meanPost4kz2c, meanPre4kz2d, meanPost4kz2d, meanPre4kz2e, meanPost4kz2e), axis = 0)
     
     trialsVal8kHz2 = np.concatenate((meanPre8kz2, meanPost8kz2, meanPre8kz2a, meanPost8kz2a, meanPre8kz2b, meanPost8kz2b, meanPre8kz2c, meanPost8kz2c, meanPre8kz2d, meanPost8kz2d, meanPre8kz2e, meanPost8kz2e), axis = 0)
     
     trialsVal16kHz2 = np.concatenate((meanPre16kz2, meanPost16kz2, meanPre16kz2a, meanPost16kz2a, meanPre16kz2b, meanPost16kz2b, meanPre16kz2c, meanPost16kz2c, meanPre16kz2d, meanPost16kz2d, meanPre16kz2e, meanPost16kz2e), axis = 0)
     
     trialsVal32kHz2 = np.concatenate((meanPre32kz2, meanPost32kz2, meanPre32kz2a, meanPost32kz2a, meanPre32kz2b, meanPost32kz2b, meanPre32kz2c, meanPost32kz2c, meanPre32kz2d, meanPost32kz2d, meanPre32kz2e, meanPost32kz2e), axis = 0)
     
     return(trialsVal2kHz1, trialsVal4kHz1, trialsVal8kHz1, trialsVal16kHz1, trialsVal32kHz1, trialsVal2kHz2, trialsVal4kHz2, trialsVal8kHz2, trialsVal16kHz2, trialsVal32kHz2)

   
        


def plot_trials_only(timePlot1, timePlot2, timePlot3, timePlot4, timePlot5, timePlot6, timePlot7, timePlot8, timePlot9, timePlot10,  dataPlot1, dataPlot2, dataPlot3, dataPlot4, dataPlot5, dataPlot6, dataPlot7, dataPlot8, dataPlot9, dataPlot10):
     '''
     Plots the mean pupil behavior for each frequency type across videos
     
     Args:
     timePlot1...10 (np.array) = array containing the time values where each value of each trial takes place during the pre and post period for each frequency type across videos
     dataPlot...10 (np.array) = array containing the pre and post values for each frequency type across videos
     
     Returns:
     plt.show() = plots each frequency type vs time across videos
     '''

# --- Organize the time values but prevailing their indices positions ---

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
     
# --- Organizes the dataPlots variables in new arrays corresponding to their associated time ---
     
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

# --- Plot the results ---
            
     labelSize = 14

     fig, trialPl = plt.subplots(1, 1, constrained_layout = True, sharex= True, sharey = True) 
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

     trialPl[0,0].set_ylim([400, 700])
     trialPl[1,0].set_ylim([400, 700])
     trialPl[2,0].set_ylim([400, 700])
     trialPl[3,0].set_ylim([400, 700])
     trialPl[4,0].set_ylim([400, 700])
     trialPl[0,1].set_ylim([400, 700])
     trialPl[1,1].set_ylim([400, 700])
     trialPl[2,1].set_ylim([400, 700])
     trialPl[3,1].set_ylim([400, 700])
     trialPl[4,1].set_ylim([400, 700])
     '''
     plt.suptitle('Pupil size for each frequency type across videos: pure11_20220415-19(actual pure011)', fontsize = labelSize)

     plt.show()
     
     return(plt.show())    
      

def find_typeLocked_values(indices, conditionIndex, pupilValues):

     '''
     Finds pupil values associated with each frequency type
     
     Args:
     indices (np.array) = array containing the indices of the time values corresponding to each of the pupil values in the pre or post period
     conditionIndex (np.array) = array containing the indices corresponding to a specific period for each frequency type
     pupilValues (np.array) = array containing the pupil values after being processed with the eventlocked_signal function
     
     Returns:
     arr (np.array) = array containing the corresponding pupil values for the specified period for each frequency type.    
     '''

# --- Look for pupil values using the rows determined by the indices variable, and columns determined by conditionIndex ---

     arr = []
     for i in indices.flatten():
         for j in conditionIndex:
             arr.append(pupilValues[i][j])
       
     return(arr)
    

     
     
     
   
     
     
     

filesDict = {'loadFile1':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220414_xtremes_192_xconfig1_proc.npy', allow_pickle = True).item(),
	'sessionFile1':'20220414_xtremes_192_xconfig1', 'condition1':'detectiongonogo', 'sound':'ChordTrain', 'name1':'pure011', 
	'loadFile2':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220415_xtremes_193_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config2':'2Sconfig3', 'sessionFile2':'20220415_xtremes_193_xconfig1', 'name2':'config12_2',
	'loadFile3':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220415_xtremes_194_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config3':'2Sconfig3', 'sessionFile3':'20220415_xtremes_194_xconfig1', 'name3':'config12_3',
	'loadFile4':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220419_xtremes_198_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config4':'2Sconfig4', 'sessionFile4':'20220419_xtremes_198_xconfig1', 'name4':'config14_1', 
	'loadFile5':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220419_xtremes_199_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config5':'2Sconfig4', 'sessionFile5':'20220419_xtremes_199_xconfig1', 'name5':'config14_2', 
	'loadFile6':np.load('./project_videos/mp4Files/mp4Outputs/pure011_20220419_xtremes_200_xconfig1_proc.npy', allow_pickle = True).item(), 
	'config6':'2Sconfig4', 'sessionFile6':'20220419_xtremes_200_xconfig1', 'name6':'config14_3'}
	
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
#timeOfBlink2Event = timeOfBlink2Event[1:-1]

#--- Align trials to the event ---
timeRange = np.array([-5, 5]) # Range of time window, 0.5 seconds before the sync signal is on and 2 seconds after is on.
windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal, postSignal, preTimeIndices, postTimeIndices = find_prepost_values(windowTimeVec, windowed_signal, -5, 0, 0, 5)
averagePreSignal = preSignal.mean(axis = 1)
averagePostSignal = postSignal.mean(axis = 1)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre signal', 'Post signal']



#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([-7, 7])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)
pAreaDilatedMean = pAreaDilated.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
#wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal[0:-3])
#print('Wilcoxon value config12_1', wstat,',',  'P-value config12_1', pval )

freq1Index2Kz, freq1Index32Kz, freq2Index2Kz, freq2Index32Kz, freq3Index2Kz, freq3Index32Kz, freq4Index2Kz, freq4Index32Kz, freq5Index2Kz, freq5Index32Kz, preSignalValues2Kz, preSignalValues32Kz = find_freqs_indices(preFreqs, postFreqs, 2000, 4000, 8000, 16000, 32000)

indexType22kz, indexType24kz, indexType28kz, indexType216kz, indexType232kz = find_type_freqs_pupil_values(preSignalValues2Kz, postFreqs, windowed_signal)

indexType322kz, indexType324kz, indexType328kz, indexType3216kz, indexType3232kz = find_type_freqs_pupil_values(preSignalValues32Kz, postFreqs, windowed_signal)

















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
#timeOfBlink2Event1 = timeOfBlink2Event1[1:-1]

#--- Align trials to the event ---
timeRange1 = np.array([-5, 5]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec1, windowed_signal1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRange1)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal1, postSignal1, preTimeIndices1, postTimeIndices1 = find_prepost_values(windowTimeVec1, windowed_signal1, -5, 0, 0, 5)
averagePreSignal1 = preSignal1.mean(axis = 1)
averagePostSignal1 = postSignal1.mean(axis = 1)
dataToPlot1 = [averagePreSignal1, averagePostSignal1]
xlabels1 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation1 = np.array([-7, 7])
pupilDilationTimeWindowVec1, pAreaDilated1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRangeForPupilDilation1)
pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
#wstat1, pval1 = stats.wilcoxon(averagePreSignal1, averagePostSignal1[0:-3])
#print('Wilcoxon value config12_2', wstat1,',',  'P-value config12_2', pval1 )



freq1Index2Kza, freq1Index32Kza, freq2Index2Kza, freq2Index32Kza, freq3Index2Kza, freq3Index32Kza, freq4Index2Kza, freq4Index32Kza, freq5Index2Kza, freq5Index32Kza, preSignalValues2Kza, preSignalValues32Kza = find_freqs_indices(preFreqs2, postFreqs2, 2000, 4000, 8000, 16000, 32000)


indexType22kza, indexType24kza, indexType28kza, indexType216kza, indexType232kza = find_type_freqs_pupil_values(preSignalValues2Kza, postFreqs2, windowed_signal1)

indexType322kza, indexType324kza, indexType328kza, indexType3216kza, indexType3232kza = find_type_freqs_pupil_values(preSignalValues32Kza, postFreqs2, windowed_signal1)












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
#timeOfBlink2Event2 = timeOfBlink2Event2[1:-1]

#--- Align trials to the event ---
timeRange2 = np.array([-5, 5]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec2, windowed_signal2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRange2)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal2, postSignal2, preTimeIndices2, postTimeIndices2 = find_prepost_values(windowTimeVec2, windowed_signal2, -5, 0, 0, 5)
averagePreSignal2 = preSignal2.mean(axis = 1)
averagePostSignal2 = postSignal2.mean(axis = 1)
dataToPlot2 = [averagePreSignal2, averagePostSignal2]
xlabels2 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation2 = np.array([-7, 7])
pupilDilationTimeWindowVec2, pAreaDilated2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRangeForPupilDilation2)
pAreaDilatedMean2 = pAreaDilated2.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
#wstat2, pval2 = stats.wilcoxon(averagePreSignal2, averagePostSignal2[0:-3])
#print('Wilcoxon value config12_3', wstat2,',',  'P-value config12_3', pval2 )


freq1Index2Kzb, freq1Index32Kzb, freq2Index2Kzb, freq2Index32Kzb, freq3Index2Kzb, freq3Index32Kzb, freq4Index2Kzb, freq4Index32Kzb, freq5Index2Kzb, freq5Index32Kzb, preSignalValues2Kzb, preSignalValues32Kzb = find_freqs_indices(preFreqs3, postFreqs3, 2000, 4000, 8000, 16000, 32000)

indexType22kzb, indexType24kzb, indexType28kzb, indexType216kzb, indexType232kzb = find_type_freqs_pupil_values(preSignalValues2Kzb, postFreqs3, windowed_signal2)

indexType322kzb, indexType324kzb, indexType328kzb, indexType3216kzb, indexType3232kzb = find_type_freqs_pupil_values(preSignalValues32Kzb, postFreqs3, windowed_signal2)













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
#timeOfBlink2Event3 = timeOfBlink2Event3[1:-1]

#--- Align trials to the event ---
timeRange3 = np.array([-5, 5]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec3, windowed_signal3 = eventlocked_signal(timeVec3, pArea3, timeOfBlink2Event3, timeRange3)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal3, postSignal3, preTimeIndices3, postTimeIndices3 = find_prepost_values(windowTimeVec3, windowed_signal3, -5, 0, 0, 5)
averagePreSignal3 = preSignal3.mean(axis = 1)
averagePostSignal3 = postSignal3.mean(axis = 1)
dataToPlot3 = [averagePreSignal3, averagePostSignal3]
xlabels3 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation3 = np.array([-5, 5])
pupilDilationTimeWindowVec3, pAreaDilated3 = eventlocked_signal(timeVec3, pArea3, timeOfBlink2Event3, timeRangeForPupilDilation3)
pAreaDilatedMean3 = pAreaDilated3.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
#wstat3, pval3 = stats.wilcoxon(averagePreSignal3, averagePostSignal3[0:-3])
#print('Wilcoxon value config12_4', wstat3,',',  'P-value config12_4', pval3 )

                                                
freq1Index2Kzc, freq1Index32Kzc, freq2Index2Kzc, freq2Index32Kzc, freq3Index2Kzc, freq3Index32Kzc, freq4Index2Kzc, freq4Index32Kzc, freq5Index2Kzc, freq5Index32Kzc, preSignalValues2Kzc, preSignalValues32Kzc = find_freqs_indices(preFreqs4, postFreqs4, 2000, 4000, 8000, 16000, 32000)

indexType22kzc, indexType24kzc, indexType28kzc, indexType216kzc, indexType232kzc = find_type_freqs_pupil_values(preSignalValues2Kzc, postFreqs4, windowed_signal3)

indexType322kzc, indexType324kzc, indexType328kzc, indexType3216kzc, indexType3232kzc = find_type_freqs_pupil_values(preSignalValues32Kzc, postFreqs4, windowed_signal3)               
                                                
                                           
                                                                                             
 
                                                
                 
                                                
                                                
                                                
                                                
                                                
                                                
                                                
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
#timeOfBlink2Event4 = timeOfBlink2Event4[1:-1]

#--- Align trials to the event ---
timeRange4 = np.array([-5, 5]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec4, windowed_signal4 = eventlocked_signal(timeVec4, pArea4, timeOfBlink2Event4, timeRange4)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal4, postSignal4, preTimeIndices4, postTimeIndices4 = find_prepost_values(windowTimeVec4, windowed_signal4, -5, 0, 0, 5)
averagePreSignal4 = preSignal4.mean(axis = 1)
averagePostSignal4 = postSignal4.mean(axis = 1)
dataToPlot4 = [averagePreSignal4, averagePostSignal4]
xlabels4 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation4 = np.array([-7, 7])
pupilDilationTimeWindowVec4, pAreaDilated4 = eventlocked_signal(timeVec4, pArea4, timeOfBlink2Event4, timeRangeForPupilDilation4)
pAreaDilatedMean4 = pAreaDilated4.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
#wstat4, pval4 = stats.wilcoxon(averagePreSignal4, averagePostSignal4[0:-3])
#print('Wilcoxon value config12_5', wstat4,',',  'P-value config12_5', pval4)                                                
                                                
                                                
freq1Index2Kzd, freq1Index32Kzd, freq2Index2Kzd, freq2Index32Kzd, freq3Index2Kzd, freq3Index32Kzd, freq4Index2Kzd, freq4Index32Kzd, freq5Index2Kzd, freq5Index32Kzd, preSignalValues2Kzd, preSignalValues32Kzd = find_freqs_indices(preFreqs5, postFreqs5, 2000, 4000, 8000, 16000, 32000)

indexType22kzd, indexType24kzd, indexType28kzd, indexType216kzd, indexType232kzd = find_type_freqs_pupil_values(preSignalValues2Kzd, postFreqs5, windowed_signal4)

indexType322kzd, indexType324kzd, indexType328kzd, indexType3216kzd, indexType3232kzd = find_type_freqs_pupil_values(preSignalValues32Kzd, postFreqs5, windowed_signal4) 
         
 
  
           
                         
                         
                         
                         
                         
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
#timeOfBlink2Event5 = timeOfBlink2Event5[1:-1]

#--- Align trials to the event ---
timeRange5 = np.array([-5, 5]) # Range of time window, one second before the sync signal is on and one second after is on. For syncSound [-0.95,0.95] and for controls [-0.6,0.6]
windowTimeVec5, windowed_signal5 = eventlocked_signal(timeVec5, pArea5, timeOfBlink2Event5, timeRange5)

#--- Obtain pupil pre and post stimulus values, and average size ---
preSignal5, postSignal5, preTimeIndices5, postTimeIndices5 = find_prepost_values(windowTimeVec5, windowed_signal5, -5, 0, 0, 5)
averagePreSignal5 = preSignal5.mean(axis = 1)
averagePostSignal5 = postSignal5.mean(axis = 1)
dataToPlot5 = [averagePreSignal5, averagePostSignal5]
xlabels5 = ['Pre signal', 'Post signal']


#--- Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation5 = np.array([-7, 7])
pupilDilationTimeWindowVec5, pAreaDilated5 = eventlocked_signal(timeVec5, pArea5, timeOfBlink2Event5, timeRangeForPupilDilation5)
pAreaDilatedMean5 = pAreaDilated5.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
#wstat5, pval5 = stats.wilcoxon(averagePreSignal5, averagePostSignal5[0:-3])
#print('Wilcoxon value config12_6', wstat5,',',  'P-value config12_2', pval5)                            
                         

freq1Index2Kze, freq1Index32Kze, freq2Index2Kze, freq2Index32Kze, freq3Index2Kze, freq3Index32Kze, freq4Index2Kze, freq4Index32Kze, freq5Index2Kze, freq5Index32Kze, preSignalValues2Kze, preSignalValues32Kze = find_freqs_indices(preFreqs6, postFreqs6, 2000, 4000, 8000, 16000, 32000)

# --- Find the indices for each frequency type ---

indexType22kze, indexType24kze, indexType28kze, indexType216kze, indexType232kze = find_type_freqs_pupil_values(preSignalValues2Kze, postFreqs6, windowed_signal5)
indexType322kze, indexType324kze, indexType328kze, indexType3216kze, indexType3232kze = find_type_freqs_pupil_values(preSignalValues32Kze, postFreqs6, windowed_signal5)

                         

# --- Finding pupil area for each freq type (may 11) ---
 
preVal22Type = find_typeLocked_values(preTimeIndices, indexType22kz, windowed_signal)
preVal24Type = find_typeLocked_values(preTimeIndices, indexType24kz, windowed_signal)
preVal28Type = find_typeLocked_values(preTimeIndices, indexType28kz, windowed_signal)
preVal216Type = find_typeLocked_values(preTimeIndices, indexType216kz, windowed_signal)
preVal232Type = find_typeLocked_values(preTimeIndices, indexType232kz, windowed_signal)
postVal22Type = find_typeLocked_values(postTimeIndices, indexType22kz, windowed_signal)
postVal24Type = find_typeLocked_values(postTimeIndices, indexType24kz, windowed_signal)
postVal28Type = find_typeLocked_values(postTimeIndices, indexType28kz, windowed_signal)      
postVal216Type = find_typeLocked_values(postTimeIndices, indexType216kz, windowed_signal)
postVal232Type = find_typeLocked_values(postTimeIndices, indexType232kz, windowed_signal)

preVal322Type = find_typeLocked_values(preTimeIndices, indexType322kz, windowed_signal)
preVal324Type = find_typeLocked_values(preTimeIndices, indexType324kz, windowed_signal)
preVal328Type = find_typeLocked_values(preTimeIndices, indexType328kz, windowed_signal)
preVal3216Type = find_typeLocked_values(preTimeIndices, indexType3216kz, windowed_signal)
preVal3232Type = find_typeLocked_values(preTimeIndices, indexType3232kz, windowed_signal)
postVal322Type = find_typeLocked_values(postTimeIndices, indexType322kz, windowed_signal)
postVal324Type = find_typeLocked_values(postTimeIndices, indexType324kz, windowed_signal)
postVal328Type = find_typeLocked_values(postTimeIndices, indexType328kz, windowed_signal)      
postVal3216Type = find_typeLocked_values(postTimeIndices, indexType3216kz, windowed_signal)
postVal3232Type = find_typeLocked_values(postTimeIndices, indexType3232kz, windowed_signal)     



preVal22Typea = find_typeLocked_values(preTimeIndices1, indexType22kza, windowed_signal1)
preVal24Typea = find_typeLocked_values(preTimeIndices1, indexType24kza, windowed_signal1)
preVal28Typea = find_typeLocked_values(preTimeIndices1, indexType28kza, windowed_signal1)
preVal216Typea = find_typeLocked_values(preTimeIndices1, indexType216kza, windowed_signal1)
preVal232Typea = find_typeLocked_values(preTimeIndices1, indexType232kza, windowed_signal1)
postVal22Typea = find_typeLocked_values(postTimeIndices1, indexType22kza, windowed_signal1)
postVal24Typea = find_typeLocked_values(postTimeIndices1, indexType24kza, windowed_signal1)
postVal28Typea = find_typeLocked_values(postTimeIndices1, indexType28kz, windowed_signal1)      
postVal216Typea = find_typeLocked_values(postTimeIndices1, indexType216kza, windowed_signal1)
postVal232Typea = find_typeLocked_values(postTimeIndices1, indexType232kza, windowed_signal1)

preVal322Typea = find_typeLocked_values(preTimeIndices1, indexType322kza, windowed_signal1)
preVal324Typea = find_typeLocked_values(preTimeIndices1, indexType324kza, windowed_signal1)
preVal328Typea = find_typeLocked_values(preTimeIndices1, indexType328kza, windowed_signal1)
preVal3216Typea = find_typeLocked_values(preTimeIndices1, indexType3216kza, windowed_signal1)
preVal3232Typea = find_typeLocked_values(preTimeIndices1, indexType3232kza, windowed_signal1)
postVal322Typea = find_typeLocked_values(postTimeIndices1, indexType322kza, windowed_signal1)
postVal324Typea = find_typeLocked_values(postTimeIndices1, indexType324kza, windowed_signal1)
postVal328Typea = find_typeLocked_values(postTimeIndices1, indexType328kza, windowed_signal1)    
postVal3216Typea = find_typeLocked_values(postTimeIndices1, indexType3216kza, windowed_signal1)
postVal3232Typea = find_typeLocked_values(postTimeIndices1, indexType3232kza, windowed_signal1)




preVal22Typeb = find_typeLocked_values(preTimeIndices2, indexType22kzb, windowed_signal2)
preVal24Typeb = find_typeLocked_values(preTimeIndices2, indexType24kzb, windowed_signal2)
preVal28Typeb = find_typeLocked_values(preTimeIndices2, indexType28kzb, windowed_signal2)
preVal216Typeb = find_typeLocked_values(preTimeIndices2, indexType216kzb, windowed_signal2)
preVal232Typeb = find_typeLocked_values(preTimeIndices2, indexType232kzb, windowed_signal2)
postVal22Typeb = find_typeLocked_values(postTimeIndices2, indexType22kzb, windowed_signal2)
postVal24Typeb = find_typeLocked_values(postTimeIndices2, indexType24kzb, windowed_signal2)
postVal28Typeb = find_typeLocked_values(postTimeIndices2, indexType28kzb, windowed_signal2)      
postVal216Typeb = find_typeLocked_values(postTimeIndices2, indexType216kzb, windowed_signal2)
postVal232Typeb = find_typeLocked_values(postTimeIndices2, indexType232kzb, windowed_signal2)

preVal322Typeb = find_typeLocked_values(preTimeIndices2, indexType322kzb, windowed_signal2)
preVal324Typeb = find_typeLocked_values(preTimeIndices2, indexType324kzb, windowed_signal2)
preVal328Typeb = find_typeLocked_values(preTimeIndices2, indexType328kzb, windowed_signal2)
preVal3216Typeb = find_typeLocked_values(preTimeIndices2, indexType3216kzb, windowed_signal2)
preVal3232Typeb = find_typeLocked_values(preTimeIndices2, indexType3232kzb, windowed_signal2)
postVal322Typeb = find_typeLocked_values(postTimeIndices2, indexType322kzb, windowed_signal2)
postVal324Typeb = find_typeLocked_values(postTimeIndices2, indexType324kzb, windowed_signal2)
postVal328Typeb = find_typeLocked_values(postTimeIndices2, indexType328kz, windowed_signal2)
postVal3216Typeb = find_typeLocked_values(postTimeIndices2, indexType3216kzb, windowed_signal2)
postVal3232Typeb = find_typeLocked_values(postTimeIndices2, indexType3232kzb, windowed_signal2)



preVal22Typec = find_typeLocked_values(preTimeIndices3, indexType22kzc, windowed_signal3)
preVal24Typec = find_typeLocked_values(preTimeIndices3, indexType24kzc, windowed_signal3)
preVal28Typec = find_typeLocked_values(preTimeIndices3, indexType28kzc, windowed_signal3)
preVal216Typec = find_typeLocked_values(preTimeIndices3, indexType216kzc, windowed_signal3)
preVal232Typec = find_typeLocked_values(preTimeIndices3, indexType232kzc, windowed_signal3)
postVal22Typec = find_typeLocked_values(postTimeIndices3, indexType22kzc, windowed_signal3)
postVal24Typec = find_typeLocked_values(postTimeIndices3, indexType24kzc, windowed_signal3)
postVal28Typec = find_typeLocked_values(postTimeIndices3, indexType28kzc, windowed_signal3)     
postVal216Typec = find_typeLocked_values(postTimeIndices3, indexType216kzc, windowed_signal3)
postVal232Typec = find_typeLocked_values(postTimeIndices3, indexType232kzc, windowed_signal3)

preVal322Typec = find_typeLocked_values(preTimeIndices3, indexType322kzc, windowed_signal3)
preVal324Typec = find_typeLocked_values(preTimeIndices3, indexType324kzc, windowed_signal3)
preVal328Typec = find_typeLocked_values(preTimeIndices3, indexType328kzc, windowed_signal3)
preVal3216Typec = find_typeLocked_values(preTimeIndices3, indexType3216kzc, windowed_signal3)
preVal3232Typec = find_typeLocked_values(preTimeIndices3, indexType3232kzc, windowed_signal3)
postVal322Typec = find_typeLocked_values(postTimeIndices3, indexType322kzc, windowed_signal3)
postVal324Typec = find_typeLocked_values(postTimeIndices3, indexType324kzc, windowed_signal3)
postVal328Typec = find_typeLocked_values(postTimeIndices3, indexType328kzc, windowed_signal3)   
postVal3216Typec = find_typeLocked_values(postTimeIndices3, indexType3216kzc, windowed_signal3)
postVal3232Typec = find_typeLocked_values(postTimeIndices3, indexType3232kzc, windowed_signal3)




preVal22Typed = find_typeLocked_values(preTimeIndices4, indexType22kzd, windowed_signal4)
preVal24Typed = find_typeLocked_values(preTimeIndices4, indexType24kzd, windowed_signal4)
preVal28Typed = find_typeLocked_values(preTimeIndices4, indexType28kzd, windowed_signal4)
preVal216Typed = find_typeLocked_values(preTimeIndices4, indexType216kzd, windowed_signal4)
preVal232Typed = find_typeLocked_values(preTimeIndices4, indexType232kzd, windowed_signal4)
postVal22Typed = find_typeLocked_values(postTimeIndices4, indexType22kzd, windowed_signal4)
postVal24Typed = find_typeLocked_values(postTimeIndices4, indexType24kzd, windowed_signal4) 
postVal28Typed = find_typeLocked_values(postTimeIndices4, indexType28kzd, windowed_signal4)     
postVal216Typed = find_typeLocked_values(postTimeIndices4, indexType216kzd, windowed_signal4)
postVal232Typed = find_typeLocked_values(postTimeIndices4, indexType232kzd, windowed_signal4)

preVal322Typed = find_typeLocked_values(preTimeIndices4, indexType322kzd, windowed_signal4)
preVal324Typed = find_typeLocked_values(preTimeIndices4, indexType324kzd, windowed_signal4)
preVal328Typed = find_typeLocked_values(preTimeIndices4, indexType328kzd, windowed_signal4)
preVal3216Typed = find_typeLocked_values(preTimeIndices4, indexType3216kzd, windowed_signal4)
preVal3232Typed = find_typeLocked_values(preTimeIndices4, indexType3232kzd, windowed_signal4)
postVal322Typed = find_typeLocked_values(postTimeIndices4, indexType322kzd, windowed_signal4)
postVal324Typed = find_typeLocked_values(postTimeIndices4, indexType324kzd, windowed_signal4)
postVal328Typed = find_typeLocked_values(postTimeIndices4, indexType328kz, windowed_signal4)
postVal3216Typed = find_typeLocked_values(postTimeIndices4, indexType3216kzd, windowed_signal4)
postVal3232Typed = find_typeLocked_values(postTimeIndices4, indexType3232kzd, windowed_signal4)



preVal22Typee = find_typeLocked_values(preTimeIndices5, indexType22kze, windowed_signal5)
preVal24Typee = find_typeLocked_values(preTimeIndices5, indexType24kze, windowed_signal5)
preVal28Typee = find_typeLocked_values(preTimeIndices5, indexType28kze, windowed_signal5)
preVal216Typee = find_typeLocked_values(preTimeIndices5, indexType216kze, windowed_signal5)
preVal232Typee = find_typeLocked_values(preTimeIndices5, indexType232kze, windowed_signal5)
postVal22Typee = find_typeLocked_values(postTimeIndices5, indexType22kze, windowed_signal5)
postVal24Typee = find_typeLocked_values(postTimeIndices5, indexType24kze, windowed_signal5)
postVal28Typee = find_typeLocked_values(postTimeIndices5, indexType28kze, windowed_signal5)  
postVal216Typee = find_typeLocked_values(postTimeIndices5, indexType216kze, windowed_signal5)
postVal232Typee = find_typeLocked_values(postTimeIndices5, indexType232kze, windowed_signal5)

preVal322Typee = find_typeLocked_values(preTimeIndices5, indexType322kze, windowed_signal5)
preVal324Typee = find_typeLocked_values(preTimeIndices5, indexType324kze, windowed_signal5)
preVal328Typee = find_typeLocked_values(preTimeIndices5, indexType328kze, windowed_signal5)
preVal3216Typee = find_typeLocked_values(preTimeIndices5, indexType3216kze, windowed_signal5)
preVal3232Typee = find_typeLocked_values(preTimeIndices5, indexType3232kze, windowed_signal5)
postVal322Typee = find_typeLocked_values(postTimeIndices5, indexType322kze, windowed_signal5)
postVal324Typee = find_typeLocked_values(postTimeIndices5, indexType324kze, windowed_signal5)
postVal328Typee = find_typeLocked_values(postTimeIndices5, indexType328kze, windowed_signal5)
postVal3216Typee = find_typeLocked_values(postTimeIndices5, indexType3216kze, windowed_signal5)
postVal3232Typee = find_typeLocked_values(postTimeIndices5, indexType3232kze, windowed_signal5)  
        
                  
                  
                  

#--- Normalized data ---
normVal1 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal22Type)
normVal2 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal24Type)
normVal3 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal28Type)
normVal4 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal216Type)
normVal5 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal232Type)
normVal6 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal322Type)
normVal7 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal324Type)
normVal8 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal328Type)
normVal9 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3216Type)
normVal10 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3232Type)

normVal1a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal22Typea)
normVal2a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal24Typea)
normVal3a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal28Typea)
normVal4a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal216Typea)
normVal5a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal232Typea)
normVal6a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal322Typea)
normVal7a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal324Typea)
normVal8a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal328Typea)
normVal9a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3216Typea)
normVal10a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3232Typea)

normVal1b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal22Typeb)
normVal2b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal24Typeb)
normVal3b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal28Typeb)
normVal4b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal216Typeb)
normVal5b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal232Typeb)
normVal6b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal322Typeb)
normVal7b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal324Typeb)
normVal8b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal328Typeb)
normVal9b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3216Typeb)
normVal10b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3232Typeb)

normVal1c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal22Typec)
normVal2c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal24Typec)
normVal3c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal28Typec)
normVal4c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal216Typec)
normVal5c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal232Typec)
normVal6c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal322Typec)
normVal7c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal324Typec)
normVal8c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal328Typec)
normVal9c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3216Typec)
normVal10c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3232Typec)

normVal1d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal22Typed)
normVal2d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal24Typed)
normVal3d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal28Typed)
normVal4d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal216Typed)
normVal5d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal232Typed)
normVal6d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal322Typed)
normVal7d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal324Typed)
normVal8d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal328Typed)
normVal9d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3216Typed)
normVal10d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3232Typed)

normVal1e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal22Typee)
normVal2e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal24Typee)
normVal3e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal28Typee)
normVal4e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal216Typee)
normVal5e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal232Typee)
normVal6e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal322Typee)
normVal7e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal324Typee)
normVal8e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal328Typee)
normVal9e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3216Typee)
normVal10e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, postVal3232Typee)

normPreVal1 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal22Type)
normPreVal2 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal24Type)
normPreVal3 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal28Type)
normPreVal4 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal216Type)
normPreVal5 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal232Type)
normPreVal6 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal322Type)
normPreVal7 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal324Type)
normPreVal8 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal328Type)
normPreVal9 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3216Type)
normPreVal10 = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3232Type)

normPreVal1a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal22Typea)
normPreVal2a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal24Typea)
normPreVal3a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal28Typea)
normPreVal4a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal216Typea)
normPreVal5a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal232Typea)
normPreVal6a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal322Typea)
normPreVal7a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal324Typea)
normPreVal8a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal328Typea)
normPreVal9a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3216Typea)
normPreVal10a = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3232Typea)

normPreVal1b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal22Typeb)
normPreVal2b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal24Typeb)
normPreVal3b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal28Typeb)
normPreVal4b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal216Typeb)
normPreVal5b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal232Typeb)
normPreVal6b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal322Typeb)
normPreVal7b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal324Typeb)
normPreVal8b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal328Typeb)
normPreVal9b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3216Typeb)
normPreVal10b = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3232Typeb)

normPreVal1c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal22Typec)
normPreVal2c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal24Typec)
normPreVal3c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal28Typec)
normPreVal4c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal216Typec)
normPreVal5c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal232Typec)
normPreVal6c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal322Typec)
normPreVal7c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal324Typec)
normPreVal8c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal328Typec)
normPreVal9c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3216Typec)
normPreVal10c = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3232Typec)

normPreVal1d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal22Typed)
normPreVal2d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal24Typed)
normPreVal3d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal28Typed)
normPreVal4d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal216Typed)
normPreVal5d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal232Typed)
normPreVal6d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal322Typed)
normPreVal7d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal324Typed)
normPreVal8d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal328Typed)
normPreVal9d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3216Typed)
normPreVal10d = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3232Typed)

normPreVal1e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal22Typee)
normPreVal2e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal24Typee)
normPreVal3e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal28Typee)
normPreVal4e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal216Typee)
normPreVal5e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal232Typee)
normPreVal6e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal322Typee)
normPreVal7e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal324Typee)
normPreVal8e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal328Typee)
normPreVal9e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3216Typee)
normPreVal10e = normalize_data_videos(pArea, pArea1, pArea2, pArea3, pArea4, pArea5, preVal3232Typee)

    


 #--- Plotting normalized values; differences in pupil pre period and post period         
                                       
#plottingPupilNormalData = calculate_pupil_size_and_plot(normVal1, normVal2, normVal3, normVal4, normVal5, normVal6, normVal7, normVal8, normVal9, normVal10, normVal1a, normVal2a, normVal3a, normVal4a, normVal5a, normVal6a, normVal7a, normVal8a, normVal9a, normVal10a, normVal1b, normVal2b, normVal3b, normVal4b, normVal5b, normVal6b, normVal7b, normVal8b, normVal9b, normVal10b, normVal1c, normVal2c, normVal3c, normVal4c, normVal5c, normVal6c, normVal7c, normVal8c, normVal9c, normVal10c, normVal1d, normVal2d, normVal3d, normVal4d, normVal5d, normVal6d, normVal7d, normVal8d, normVal9d, normVal10d, normVal1e, normVal2e, normVal3e, normVal4e, normVal5e, normVal6e, normVal7e, normVal8e, normVal9e, normVal10e, normPreVal1, normPreVal2, normPreVal3, normPreVal4, normPreVal5, normPreVal6, normPreVal7, normPreVal8, normPreVal9, normPreVal10, normPreVal1a, normPreVal2a, normPreVal3a, normPreVal4a, normPreVal5a, normPreVal6a, normPreVal7a, normPreVal8a, normPreVal9a, normPreVal10a, normPreVal1b, normPreVal2b, normPreVal3b, normPreVal4b, normPreVal5b, normPreVal6b, normPreVal7b, normPreVal8b, normPreVal9b, normPreVal10b, normPreVal1c, normPreVal2c, normPreVal3c, normPreVal4c, normPreVal5c, normPreVal6c, normPreVal7c, normPreVal8c, normPreVal9c, normPreVal10c, normPreVal1d, normPreVal2d, normPreVal3d, normPreVal4d, normPreVal5d, normPreVal6d, normPreVal7d, normPreVal8d, normPreVal9d, normPreVal10d, normPreVal1e, normPreVal2e, normPreVal3e, normPreVal4e, normPreVal5e, normPreVal6e, normPreVal7e, normPreVal8e, normPreVal9e, normPreVal10e, frequenciesTested)


# --- Calculating mean values for each frequency type --- 
  
trialsMean2kz1, trialsMean4kz1, trialsMean8kz1, trialsMean16kz1, trialsMean32kz1, trialsMean2kz2, trialsMean4kz2, trialsMean8kz2, trialsMean16kz2, trialsMean32kz2 = calculate_pupil_size_trials(postVal22Type, postVal24Type, postVal28Type, postVal216Type, postVal232Type, postVal322Type, postVal324Type, postVal328Type, postVal3216Type, postVal3232Type, postVal22Typea, postVal24Typea, postVal28Typea, postVal216Typea, postVal232Typea, postVal322Typea, postVal324Typea, postVal328Typea, postVal3216Typea, postVal3232Typea, postVal22Typeb, postVal24Typeb, postVal28Typeb, postVal216Typeb, postVal232Typeb, postVal322Typeb, postVal324Typeb, postVal328Typeb, postVal3216Typeb, postVal3232Typeb, postVal22Typec, postVal24Typec, postVal28Typec, postVal216Typec, postVal232Typec, postVal322Typec, postVal324Typec, postVal328Typec, postVal3216Typec, postVal3232Typec, postVal22Typed, postVal24Typed, postVal28Typed, postVal216Typed, postVal232Typed, postVal322Typed, postVal324Typed, postVal328Typed, postVal3216Typed, postVal3232Typed, postVal22Typee, postVal24Typee, postVal28Typee, postVal216Typee, postVal232Typee, postVal322Typee, postVal324Typee, postVal328Typee, postVal3216Typee, postVal3232Typee, preVal22Type, preVal24Type, preVal28Type, preVal216Type, preVal232Type, preVal322Type, preVal324Type, preVal328Type, preVal3216Type, preVal3232Type, preVal22Typea, preVal24Typea, preVal28Typea, preVal216Typea, preVal232Typea, preVal322Typea, preVal324Typea, preVal328Typea, preVal3216Typea, preVal3232Typea, preVal22Typeb, preVal24Typeb, preVal28Typeb, preVal216Typeb, preVal232Typeb, preVal322Typeb, preVal324Typeb, preVal328Typeb, preVal3216Typeb, preVal3232Typeb, preVal22Typec, preVal24Typec, preVal28Typec, preVal216Typec, preVal232Typec, preVal322Typec, preVal324Typec, preVal328Typec, preVal3216Typec, preVal3232Typec, preVal22Typed, preVal24Typed, preVal28Typed, preVal216Typed, preVal232Typed, preVal322Typed, preVal324Typed, preVal328Typed, preVal3216Typed, preVal3232Typed, preVal22Typee, preVal24Typee, preVal28Typee, preVal216Typee, preVal232Typee, preVal322Typee, preVal324Typee, preVal328Typee, preVal3216Typee, preVal3232Typee, indexType22kz, indexType24kz, indexType28kz, indexType216kz, indexType232kz, indexType322kz, indexType324kz, indexType328kz, indexType3216kz, indexType3232kz, indexType22kza, indexType24kza, indexType28kza, indexType216kza, indexType232kza, indexType322kza, indexType324kza, indexType328kza, indexType3216kza, indexType3232kza, indexType22kzb, indexType24kzb, indexType28kzb, indexType216kzb, indexType232kzb, indexType322kzb, indexType324kzb, indexType328kzb, indexType3216kzb, indexType3232kzb, indexType22kzc, indexType24kzc, indexType28kzc, indexType216kzc, indexType232kzc, indexType322kzc, indexType324kzc, indexType328kzc, indexType3216kzc, indexType3232kzc, indexType22kzd, indexType24kzd, indexType28kzd, indexType216kzd, indexType232kzd, indexType322kzd, indexType324kzd, indexType328kzd, indexType3216kzd, indexType3232kzd, indexType22kze, indexType24kze, indexType28kze, indexType216kze, indexType232kze, indexType322kze, indexType324kze, indexType328kze, indexType3216kze, indexType3232kze, preSignal, postSignal)
     
# --- plotting each freq type vs time (second try) having organized pres and posts --- 
onlyTrialPlotsShortTimeWindow = plot_trials_only(windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, windowTimeVec, trialsMean2kz1, trialsMean4kz1, trialsMean8kz1, trialsMean16kz1, trialsMean32kz1, trialsMean2kz2, trialsMean4kz2, trialsMean8kz2, trialsMean16kz2, trialsMean32kz2)

#--- plot with the three conditions aligned ---
#OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean,  pAreaDilatedMean1, pAreaDilatedMean2, pAreaDilatedMean3, pAreaDilatedMean4, pAreaDilatedMean5, pval, pval1, pval2, pval3, pval4, pval5)



#--- Figure with 3 bar plots and scatter plots ---
#scattBar = barScat_plots(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal, averagePreSignal1, averagePostSignal1, preSignal1, postSignal2, averagePreSignal2, averagePostSignal2, preSignal2, postSignal2, averagePreSignal3, averagePostSignal3, preSignal3, postSignal3, averagePreSignal4, averagePostSignal4, preSignal4, postSignal4, averagePreSignal5, averagePostSignal5, preSignal5, postSignal5,pval, pval1, pval2, pval3, pval4, pval5)

#--- Pupil Dilation plots --- 
#pupilDilationPlots = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean, pupilDilationTimeWindowVec1, pAreaDilatedMean1, pupilDilationTimeWindowVec2, pAreaDilatedMean2)
 

