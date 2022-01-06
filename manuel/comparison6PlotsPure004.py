'''
This script is for the project of pupil dilation. It is intended to obtain pupil data, its mean the desired time windows, create a slope and bar plots
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
     
     label1 = filesDict['config1'],'pval:',sp
     label2 = filesDict['config2'],'pval:',sp1
     label3 = filesDict['config3'],'pval:',sp2
     label4 = filesDict['config4'],'pval:',sp3
     label5 = filesDict['config5'],'pval:',sp4
     label6 = filesDict['config6'],'pval:',sp5
     
     subplt.plot(time, valuesData1, color = 'g', label = label1, linewidth = 4)
     subplt.plot(time, valuesData2, color = 'c', label = label2, linewidth = 4)
     subplt.plot(time, valuesData3, color = 'b', label = label3, linewidth = 4)
     subplt.plot(time, valuesData4, color = 'm', label = label4, linewidth = 4)
     subplt.plot(time, valuesData5, color = 'r', label = label5, linewidth = 4)
     subplt.plot(time, valuesData6, color = 'y', label = label6, linewidth = 4)
     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     subplt.set_title('Pupil behavior in condition 13: pure004_20211207', fontsize = labelsSize)
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
     scatterPlots[0].set_title(filesDict['config1'], fontsize = scatterLabelsSize)
     scatterPlots[0].set_ylabel('Mean Pupil Area', fontsize = scatterLabelsSize)
     scatterPlots[0].tick_params(axis = 'x', labelsize = scatterXlabels)
     scatterPlots[1].plot(xLabelling, dataToPlot2, marker = 'o', linewidth = 1) 
     scatterPlots[1].set_title(filesDict['config2'], fontsize = scatterLabelsSize)
     scatterPlots[1].tick_params(axis = 'x', labelsize = scatterXlabels) 
     scatterPlots[2].plot(xLabelling, dataToPlot3, marker = 'o', linewidth = 1) 
     scatterPlots[2].set_title(filesDict['config3'], fontsize = scatterLabelsSize)
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
     shortPval1 = np.round(pVal1, decimals=3)
     shortPval2 = np.round(pVal2, decimals=2)
     shortPval3 = np.round(pVal3, decimals=3)
     shortPval4 = np.round(pVal4, decimals=3)
     shortPval5 = np.round(pVal5, decimals=16)
     shortPval6 = np.round(pVal6, decimals=3)
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
     barPlots[0].set_title(filesDict['config1'], fontsize = barLabelsFontSize)
     barPlots[0].set_ylabel(scatBarDict['yLabel'], fontsize = barLabelsFontSize)
     barPlots[0].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[0].plot(xlabels, dataPlot1, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[0].legend(prop ={"size":10})
     barPlots[1].bar(xlabels, barMeanValues2, yerr = stdErrors2, color= 'c', label = pValue2) 
     barPlots[1].errorbar(xlabels, barMeanValues2, yerr = stdErrors2, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[1].set_title(filesDict['config2'], fontsize = barLabelsFontSize)
     barPlots[1].set_xlabel(scatBarDict['xLabelTitle'], fontsize = barLabelsFontSize)
     barPlots[1].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[1].plot(xlabels, dataPlot2, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[1].legend(prop ={"size":10})
     barPlots[2].bar(xlabels, barMeanValues3, yerr = stdErrors3, color = 'b', label = pValue3) 
     barPlots[2].errorbar(xlabels, barMeanValues3, yerr = stdErrors3, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[2].set_title(filesDict['config3'], fontsize = barLabelsFontSize)
     barPlots[2].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[2].plot(xlabels, dataPlot3, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[3].bar(xlabels, barMeanValues4, yerr = stdErrors4, color = 'm', label = pValue4)
     barPlots[3].errorbar(xlabels, barMeanValues4, yerr = stdErrors4, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
     barPlots[3].set_title(filesDict['config4'], fontsize = barLabelsFontSize)
     barPlots[3].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[3].plot(xlabels, dataPlot4, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[4].bar(xlabels, barMeanValues5, yerr = stdErrors5, color = 'r', label = pValue5)
     barPlots[4].errorbar(xlabels, barMeanValues5, yerr = stdErrors5, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black')
     barPlots[4].set_title(filesDict['config5'], fontsize = barLabelsFontSize)
     barPlots[4].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[4].plot(xlabels, dataPlot5, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     barPlots[5].bar(xlabels, barMeanValues6, yerr = stdErrors6, color = 'y', label = pValue6)
     barPlots[5].errorbar(xlabels, barMeanValues6, yerr = stdErrors6, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black')
     barPlots[5].set_title(filesDict['config6'], fontsize = barLabelsFontSize)
     barPlots[5].tick_params(axis='x', labelsize=barLabelsFontSize)
     barPlots[5].plot(xlabels, dataPlot6, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
     plt.ylim(100, 800)
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


filesDict = {'file1':'pure004_20211203_syncSound_28_config12_proc.npy', 
	'loadFile1':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211203_syncSound_28_config12_proc.npy', allow_pickle = True).item(),
	'config1':'config12', 'sessionFile1':'28', 'condition':'syncSound', 'sound':'ChordTrain', 'file2':'pure004_20211203_syncSound_29_config12_proc.npy', 
	'loadFile2':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211203_syncSound_29_config12_proc.npy', allow_pickle = True).item(), 
	'config2':'config12', 'sessionFile2':'29', 'file3':'pure004_20211203_syncSound_30_config12_proc.npy', 
	'loadFile3':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211203_syncSound_30_config12_proc.npy', allow_pickle = True).item(), 
	'config3':'config12', 'sessionFile3':'30', 'file4':'pure004_20211203_syncSound_31_config13_proc.npy', 
	'loadFile4':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211203_syncSound_31_config13_proc.npy', allow_pickle = True).item(), 
	'config4':'config13', 'sessionFile4':'31', 'file4':'pure004_20211207_syncSound_42_config14_proc.npy', 
	'loadFile4':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211207_syncSound_42_config14_proc.npy', allow_pickle = True).item(), 
	'config4':'config14', 'sessionFile4':'42', 'file5':'pure004_20211207_syncSound_40_config14_proc.npy', 
	'loadFile5':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211207_syncSound_40_config14_proc.npy', allow_pickle = True).item(), 
	'config5':'config14', 'sessionFile5':'40', 'file6':'pure004_20211207_syncSound_41_config14_proc.npy', 
	'loadFile6':np.load('./project_videos/mp4Files/mp4Outputs/pure004_20211207_syncSound_41_config14_proc.npy', allow_pickle = True).item(), 
	'config6':'config14', 'sessionFile6':'41'}
	
scatBarDict = {'title':'Pupil behavior before and after stimulus: pure004_20211203', 'savedName':'barControlsPure004Plot', 'yLabel':'Mean Pupil Area', 'xLabelTitle':'Conditions'}


proc = filesDict['loadFile1']


#---obtain pupil data---
pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
minNumberBlink = np.amin(blink2)
diffBlink = np.amax(blink2) - minNumberBlink
blink2Bool = np.logical_and(blink2 > minNumberBlink, blink2 < diffBlink) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRangeForPupilDilation = np.array([-6, 6])
pupilDilationTimeWindowVec, pAreaDilated = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRangeForPupilDilation)
pAreaDilatedMean = pAreaDilated.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat, pval = stats.wilcoxon(averagePreSignal, averagePostSignal)
print('Wilcoxon value config12_1', wstat,',',  'P-value config12_1', pval )


















proc1 = filesDict['loadFile2']

#---obtain pupil data---
pupil1 = proc1['pupil'][0] # Dic.
pArea1 = pupil1['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink1a = proc1['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink11 = proc1['blink']   # List.
blink21 = np.array(blink1a).T # Creates transpose matrix of blink. Necessary for plotting.


#---obtain values where sync signal is on---
minNumberBlink1 = np.amin(blink21)
diffBlink1 = np.amax(blink21) - minNumberBlink1
blink2Bool1 = np.logical_and(blink21 > minNumberBlink1, blink21 < diffBlink1) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRangeForPupilDilation1 = np.array([-6, 6])
pupilDilationTimeWindowVec1, pAreaDilated1 = eventlocked_signal(timeVec1, pArea1, timeOfBlink2Event1, timeRangeForPupilDilation1)
pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)

#--- Wilcoxon test to obtain statistics ---
wstat1, pval1 = stats.wilcoxon(averagePreSignal1, averagePostSignal1)
print('Wilcoxon value config12_2', wstat1,',',  'P-value config12_2', pval1 )

















proc2 = filesDict['loadFile3']


#---obtain pupil data---
pupil2 = proc2['pupil'][0] # Dic.
pArea2 = pupil2['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink2a = proc2['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink12 = proc2['blink']   # List.
blink22 = np.array(blink2a).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minNumberBlink2 = np.amin(blink22)
diffBlink2 = np.amax(blink22) - minNumberBlink2
blink2Bool2 = np.logical_and(blink22 > minNumberBlink2, blink22 < diffBlink2) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRangeForPupilDilation2 = np.array([-6, 6])
pupilDilationTimeWindowVec2, pAreaDilated2 = eventlocked_signal(timeVec2, pArea2, timeOfBlink2Event2, timeRangeForPupilDilation2)
pAreaDilatedMean2 = pAreaDilated2.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat2, pval2 = stats.wilcoxon(averagePreSignal2, averagePostSignal2)
print('Wilcoxon value config12_3', wstat2,',',  'P-value config12_3', pval2 )


























proc3 = filesDict['loadFile4']
#---obtain pupil data---
pupil3 = proc3['pupil'][0] # Dic.
pArea3 = pupil3['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink3 = proc3['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink13 = proc3['blink']   # List.
blink23 = np.array(blink3).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minNumberBlink3 = np.amin(blink23)
diffBlink3 = np.amax(blink23) - minNumberBlink3
blink2Bool3 = np.logical_and(blink23 > minNumberBlink3, blink23 < diffBlink3) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRangeForPupilDilation3 = np.array([-6, 6])
pupilDilationTimeWindowVec3, pAreaDilated3 = eventlocked_signal(timeVec3, pArea3, timeOfBlink2Event3, timeRangeForPupilDilation3)
pAreaDilatedMean3 = pAreaDilated3.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat3, pval3 = stats.wilcoxon(averagePreSignal3, averagePostSignal3)
print('Wilcoxon value config12_4', wstat3,',',  'P-value config12_4', pval3 )

                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
proc4 = filesDict['loadFile5']

#---obtain pupil data---
pupil4 = proc4['pupil'][0] # Dic.
pArea4 = pupil4['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink4 = proc4['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink14 = proc4['blink']   # List.
blink24 = np.array(blink4).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minNumberBlink4 = np.amin(blink24)
diffBlink4 = np.amax(blink24) - minNumberBlink4
blink2Bool4 = np.logical_and(blink24 > minNumberBlink4, blink24 < diffBlink4) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRangeForPupilDilation4 = np.array([-6, 6])
pupilDilationTimeWindowVec4, pAreaDilated4 = eventlocked_signal(timeVec4, pArea4, timeOfBlink2Event4, timeRangeForPupilDilation4)
pAreaDilatedMean4 = pAreaDilated4.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat4, pval4 = stats.wilcoxon(averagePreSignal4, averagePostSignal4)
print('Wilcoxon value config12_5', wstat4,',',  'P-value config12_5', pval4)                                                
                                                
                                                
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
                         
proc5 = filesDict['loadFile6']
#---obtain pupil data---
pupil5 = proc5['pupil'][0] # Dic.
pArea5 = pupil5['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink5 = proc5['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink15 = proc5['blink']   # List.
blink25 = np.array(blink5).T # Creates transpose matrix of blink. Necessary for plotting.



#---obtain values where sync signal is on---
minNumberBlink5 = np.amin(blink25)
diffBlink5 = np.amax(blink25) - minNumberBlink5
blink2Bool5 = np.logical_and(blink25 > minNumberBlink5, blink25 < diffBlink5) # Boolean values from the blink2 variable where True values will be within the established range.
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
timeRangeForPupilDilation5 = np.array([-6, 6])
pupilDilationTimeWindowVec5, pAreaDilated5 = eventlocked_signal(timeVec5, pArea5, timeOfBlink2Event5, timeRangeForPupilDilation5)
pAreaDilatedMean5 = pAreaDilated5.mean(axis = 1)


#--- Wilcoxon test to obtain statistics ---
wstat5, pval5 = stats.wilcoxon(averagePreSignal5, averagePostSignal5)
print('Wilcoxon value config12_6', wstat5,',',  'P-value config12_2', pval5)                            
                         
                         
                         
                  
                         
                                                
                                                
                                                
                                                
                                                
                                                                
#--- plot with the three conditions aligned ---
OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean,  pAreaDilatedMean1, pAreaDilatedMean2, pAreaDilatedMean3, pAreaDilatedMean4, pAreaDilatedMean5, pval, pval1, pval2, pval3, pval4, pval5)


#--- Figure with 3 scatter plots ---
#scatterPlots = scatter_plots(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2, averagePreSignal3, averagePostSignal3)

#--- Figure with 3 bar plots and scatter plots ---
scattBar = barScat_plots(averagePreSignal, averagePostSignal, 'pre stimulus onset', 'post stimulus onset', preSignal, postSignal, averagePreSignal1, averagePostSignal1, preSignal1, postSignal2, averagePreSignal2, averagePostSignal2, preSignal2, postSignal2, averagePreSignal3, averagePostSignal3, preSignal3, postSignal3, averagePreSignal4, averagePostSignal4, preSignal4, postSignal4, averagePreSignal5, averagePostSignal5, preSignal5, postSignal5,pval, pval1, pval2, pval3, pval4, pval5)

#--- Pupil Dilation plots --- 
#pupilDilationPlots = pupilDilation_time(pupilDilationTimeWindowVec, pAreaDilatedMean, pupilDilationTimeWindowVec1, pAreaDilatedMean1, pupilDilationTimeWindowVec2, pAreaDilatedMean2)

#--- scatter & bar plots overlapped ---
#scattBar = bar_and_scatter(averagePreSignal, averagePostSignal, averagePreSignal1, averagePostSignal1, averagePreSignal2, averagePostSignal2)
