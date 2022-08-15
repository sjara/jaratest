'''
This script is for the project of pupil dilation. It is intended to obtain pupil data, its mean the desired time windows, create a slope and bar plots
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from jaratoolbox import loadbehavior
from jaratoolbox import settings
from jaratoolbox import extrafuncs
import os
import sys
sys.path.append('/home/jarauser/src/jaratest/dannybrown/')
import facemapanalysis as fmap

# Input session parameters
subject = 'pure012'
date = '20220701'

# Load data from infovideos file
infovideosFilename = os.path.join('/home/jarauser/src/jarainfo_old', f'{subject}_infovideos.py') # Remove 'old' when SJ has fixed Jarainfo
infovideos = extrafuncs.read_infofile(infovideosFilename)

# File locations for behavioral data and processed FaceMap data
#sessionNumber = (FIND THE SESSION NUMBER BY DATE IN INFOVIDEOS) # HOW DO YOU FIND A MATCH FOR THE DATE?
filename_behav = infovideos.videos.sessions[3].behavFile # Hardcoded - sub in 3 for the date match from above.
fileloc_behav = os.path.join(settings.BEHAVIOR_PATH,subject,filename_behav)
filename_video = infovideos.videos.sessions[3].videoFile
filename_fmap = '_'.join([filename_video.split('.')[0],'proc.npy'])
fileloc_fmap = os.path.join('/data/videos',f'{subject}_processed', filename_fmap)

# Load the Behavioral Data and FaceMap data
bdata = loadbehavior.BehaviorData(fileloc_behav)
faceMap = fmap.load_data(os.path.join(fileloc_fmap), runchecks=False)

#--- obtain frequencies data ---
freqs = bdata['currentFreq'] # works with am_tuning_curve paradigm
#freqs = bdata['postFreq'] # works with gonogo paradigm
freqs_list = np.unique(freqs)
#--- obtain pupil data ---
pArea = fmap.extract_pupil(faceMap)

#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Number of frames.
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = frameVec / framerate # Time Vector to calculate the length of the video.

#--- obtain values where sync signal turns on ---
_, syncOnsetValues, _, _ = fmap.extract_sync(faceMap)
timeOfSyncOnset = timeVec[syncOnsetValues] # Provides the time values in which the sync signal turns on.

########## IF ERROR IS THROWN BELOW, YOU CAN MAKE MANUAL CHANGE HERE ######
#freqs=freqs[0:-1]
#timeOfSyncOnset=timeOfSyncOnset[0:-1]
syncOnsetValues=syncOnsetValues[0:-1]
###########################################################################

if len(freqs) != syncOnsetValues.shape[0]: # Throw an error if there wasn't a sync light for every sound
    print('ERROR: # of sync light signals does not match number of sounds played')
    sys.exit()
     
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

#--- For p-values: Align trials to events ---
timeRange = np.array([-0.5, 2.0]) # Create range for time window
# create signal locked to sync light, for each condition
windowTimeVec, _ = eventlocked_signal(timeVec, pArea, timeOfSyncOnset, timeRange) # CAN YOU TAKE THIS OUT?
_, windowed_signal_nochange = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[0]], timeRange)
_, windowed_signal_change1 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[1]], timeRange)
_, windowed_signal_change2 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[2]], timeRange)
_, windowed_signal_change3 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[3]], timeRange)
_, windowed_signal_change4 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[4]], timeRange)
_, windowed_signal_change5 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[5]], timeRange)

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

#--- For p-values: Obtain pupil pre and post stimulus values, and average size ---
preSignal_nochange, postSignal_nochange = find_prepost_values(windowTimeVec, windowed_signal_nochange, -0.5, 0, 1.4, 2.0)
preSignal_change1, postSignal_change1 = find_prepost_values(windowTimeVec, windowed_signal_change1, -0.5, 0, 1.4, 2.0)
preSignal_change2, postSignal_change2 = find_prepost_values(windowTimeVec, windowed_signal_change2, -0.5, 0, 1.4, 2.0)
preSignal_change3, postSignal_change3 = find_prepost_values(windowTimeVec, windowed_signal_change3, -0.5, 0, 1.4, 2.0)
preSignal_change4, postSignal_change4 = find_prepost_values(windowTimeVec, windowed_signal_change4, -0.5, 0, 1.4, 2.0)
preSignal_change5, postSignal_change5 = find_prepost_values(windowTimeVec, windowed_signal_change5, -0.5, 0, 1.4, 2.0)

averagePreSignal_nochange = preSignal_nochange.mean(axis = 0)
averagePreSignal_change1 = preSignal_change1.mean(axis = 0)
averagePreSignal_change2 = preSignal_change2.mean(axis = 0)
averagePreSignal_change3 = preSignal_change3.mean(axis = 0)
averagePreSignal_change4 = preSignal_change4.mean(axis = 0)
averagePreSignal_change5 = preSignal_change5.mean(axis = 0)

averagePostSignal_nochange = postSignal_nochange.mean(axis = 0)
averagePostSignal_change1 = postSignal_change1.mean(axis = 0)
averagePostSignal_change2 = postSignal_change2.mean(axis = 0)
averagePostSignal_change3 = postSignal_change3.mean(axis = 0)
averagePostSignal_change4 = postSignal_change4.mean(axis = 0)
averagePostSignal_change5 = postSignal_change5.mean(axis = 0)



#--- For p-values: Wilcoxon test to obtain statistics ---
wstat0, pval0 = stats.wilcoxon(averagePreSignal_nochange, averagePostSignal_nochange)
wstat1, pval1 = stats.wilcoxon(averagePreSignal_change1, averagePostSignal_change1)
wstat2, pval2 = stats.wilcoxon(averagePreSignal_change2, averagePostSignal_change2)
wstat3, pval3 = stats.wilcoxon(averagePreSignal_change3, averagePostSignal_change3)
wstat4, pval4 = stats.wilcoxon(averagePreSignal_change4, averagePostSignal_change4)
wstat5, pval5 = stats.wilcoxon(averagePreSignal_change5, averagePostSignal_change5)

#--- For Plots: Defining the correct time range for pupil's relaxation (dilation) ---
timeRangeForPupilDilation = np.array([-15, 15])
pupilDilationTimeWindowVec, pAreaDilated0 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[0]], timeRangeForPupilDilation)
_, pAreaDilated1 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[1]], timeRangeForPupilDilation)
_, pAreaDilated2 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[2]], timeRangeForPupilDilation)
_, pAreaDilated3 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[3]], timeRangeForPupilDilation)
_, pAreaDilated4 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[4]], timeRangeForPupilDilation)
_, pAreaDilated5 = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freqs_list[5]], timeRangeForPupilDilation)


pAreaDilatedMean0 = pAreaDilated0.mean(axis = 1)
pAreaDilatedMean1 = pAreaDilated1.mean(axis = 1)
pAreaDilatedMean2 = pAreaDilated2.mean(axis = 1)
pAreaDilatedMean3 = pAreaDilated3.mean(axis = 1)
pAreaDilatedMean4 = pAreaDilated4.mean(axis = 1)
pAreaDilatedMean5 = pAreaDilated5.mean(axis = 1)

def comparison_plot(time, valuesData0, valuesData1, valuesData2, valuesData3, valuesData4, valuesData5, pVal0, pVal1, pVal2, pVal3, pVal4, pVal5, freqs_list): 
     ''' 
     Creates 1 figure with 6 plots 
     Args: 
     time = vector values for x axis 
     valuesData0 (np.array) = vector values for y axis of the first plot 
     valuesData1 (np.array)= vector values for y axis of the second plot
     valuesData2 (np.array)= vector values for y axis of the third plot
     valuesData3 (np.array) = vector values for y axis of the fourth plot 
     valuesData4 (np.array)= vector values for y axis of the fifth plot
     valuesData5 (np.array)= vector values for y axis of the sixth plot
     freqs_list (np.array) = list of frequencies included
     returns: 
     plt.show() = 1 figure with 6 plots using the input data 
     ''' 
     labelsSize = 16
     fig, subplt = plt.subplots(1,1)
     fig.set_size_inches(18, 10, forward = True)
     sp0 = np.round(pVal0, decimals=9)
     sp1 = np.round(pVal1, decimals=9)
     sp2 = np.round(pVal2, decimals=9)
     sp3 = np.round(pVal3, decimals=9)
     sp4 = np.round(pVal4, decimals=9)
     sp5 = np.round(pVal5, decimals=9)
     label0 = 'Change = '+str(freqs_list[-1])+' Hz--> '+str(freqs_list[0])+' Hz: nTrials = '+str(sum(freqs==freqs_list[0]))+', pval='+str(sp0)
     label1 = 'Change = '+str(freqs_list[-1])+' Hz--> '+str(freqs_list[1])+' Hz: nTrials = '+str(sum(freqs==freqs_list[1]))+', pval='+str(sp1)
     label2 = 'Change = '+str(freqs_list[-1])+' Hz--> '+str(freqs_list[2])+' Hz: nTrials = '+str(sum(freqs==freqs_list[2]))+', pval='+str(sp2)
     label3 = 'Change = '+str(freqs_list[-1])+' Hz--> '+str(freqs_list[3])+' Hz: nTrials = '+str(sum(freqs==freqs_list[3]))+', pval='+str(sp3)
     label4 = 'Change = '+str(freqs_list[-1])+' Hz--> '+str(freqs_list[4])+' Hz: nTrials = '+str(sum(freqs==freqs_list[4]))+', pval='+str(sp4)
     label5 = 'Change = '+str(freqs_list[-1])+' Hz--> '+str(freqs_list[5])+' Hz: nTrials = '+str(sum(freqs==freqs_list[5]))+', pval='+str(sp5)
     
     alphas = np.linspace(.4,1,6)
     subplt.plot(time, valuesData0, alpha = alphas[0], label = label0, linewidth = 4)
     subplt.plot(time, valuesData1, alpha = alphas[1], label = label1, linewidth = 4)
     subplt.plot(time, valuesData2, alpha = alphas[2], label = label2, linewidth = 4)
     subplt.plot(time, valuesData3, alpha = alphas[3], label = label3, linewidth = 4)
     subplt.plot(time, valuesData4, alpha = alphas[4], label = label4, linewidth = 4)
     subplt.plot(time, valuesData5, alpha = alphas[5], label = label5, linewidth = 4)

     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     subplt.set_title('Pupil behavior in response to a chord change (with no gap): 6 Frequencies.', fontsize = labelsSize)
     plt.suptitle('Mouse = pure012.  Data Collected 2022-06-28.', fontsize = labelsSize)
     plt.axvline(-7, label='begin fade in', color = 'lightskyblue', linestyle='dashed', linewidth = 3)
     plt.axvline(-5, label='fade in complete', color = 'dodgerblue', linestyle='dashed', linewidth = 3)
     plt.axvline(0, label = 'sound change', color = 'red', linestyle='dashed', linewidth = 3)
     plt.axvline(5, label = 'sound turns off', color = 'pink', linestyle='dashed', linewidth = 3)
     plt.grid(b = True)
     #plt.ylim([550, 650])
     plt.xticks(fontsize = labelsSize)
     plt.yticks(fontsize = labelsSize)
     plt.legend()
     #plt.legend(prop ={"size":10}, bbox_to_anchor=(1.0, 0.8))
     #plt.savefig('comparisonPure004Plot', format = 'pdf', dpi = 50)
     plt.show() 
     return(plt.show())

#--- plot with the three conditions aligned ---
OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, pAreaDilatedMean0, pAreaDilatedMean1,  pAreaDilatedMean2, pAreaDilatedMean3, pAreaDilatedMean4, pAreaDilatedMean5, pval0, pval1, pval2, pval3, pval4,  pval5, freqs_list=freqs_list)
#scattBar1 = barScat_plots(averagePreSignal_nochange, averagePostSignal_nochange, 'pre stimulus onset', 'post stimulus onset', preSignal_nochange, postSignal_nochange,  pval0)
#--- Get the number of trials for each condition ---
print('cond0: ',sum(freqs==freqs_list[0]))
print('cond1: ',sum(freqs==freqs_list[1]))
print('cond2: ',sum(freqs==freqs_list[2]))
print('cond3: ',sum(freqs==freqs_list[3]))
print('cond4: ',sum(freqs==freqs_list[4]))
print('cond5: ',sum(freqs==freqs_list[5]))

#Unneccessary Code
#     
#
#def onset_values(signalArray): 
#
#     '''
#     Helps to find onset start values of the sync singal in any given array: 
#     Args: 
#     SignalArray (np.array) = array that contains data of the sync signal
#     Returns:
#     onsetStartValues (np.array)  = an array of the indices containing the start onset values of the sync signal.
#    ''' 
#     firstIndexValue = 0 
#     lastIndexValue = len(signalArray)-1 
#     stepNumber = 2
#     startIndicesValues = range(firstIndexValue, lastIndexValue, stepNumber)
#     startIndicesVec = np.array(startIndicesValues)
#     onsetStartValues = np.take(signalArray, startIndicesVec)
#     return (onsetStartValues)
#     

      
      
#def freqs_and_meanParea(freqsArray, meanPareaVariable, freq1, freq2, freq3, freq4, freq5):      
#      '''
#      Creates arrays containing the pupil area for each tested frequency. Am_tuning_curve paradigm
#      Args:
#      freqsArray (np.array): array containing the tested frequencies
#      meanPareaVariable (np.array): array containing the average pupil size
#      freq1..5 (int): frequencies tested
#      
#      returns:
#      arrValues1..5 (np.array): one array per frequency tested (freq1..5) that contains the pupil size for the given frequency
#      '''
#      
#      indicesFreq1 = np.argwhere(freq1 == freqsArray)  
#      indicesFreq2 = np.argwhere(freq2 == freqsArray)
#      indicesFreq3 = np.argwhere(freq3 == freqsArray)  
#      indicesFreq4 = np.argwhere(freq4 == freqsArray)  
#      indicesFreq5 = np.argwhere(freq5 == freqsArray)  
#      newIndexArr1 = np.take(meanPareaVariable, indicesFreq1)  
#      newIndexArr2 = np.take(meanPareaVariable, indicesFreq2)  
#      newIndexArr3 = np.take(meanPareaVariable, indicesFreq3)  
#      newIndexArr4 = np.take(meanPareaVariable, indicesFreq4)  
#      newIndexArr5 = np.take(meanPareaVariable, indicesFreq5)
#      arrValues1 = newIndexArr1.flatten()
#      arrValues2 = newIndexArr2.flatten()   
#      arrValues3 = newIndexArr3.flatten() 
#      arrValues4 = newIndexArr4.flatten()   
#      arrValues5 = newIndexArr5.flatten()
#      
#      return(arrValues1, arrValues2, arrValues3, arrValues4, arrValues5)
#      
#
#      
#def normalize_data_videos(pupilArea, pupilArea1, pupilArea2, valuesToNormalize):
#     ''' 
#     Allows to normalize the average pupil area for each video
#     Args:
#     pupilArea (np.array) = array containing the raw data of the pupil area
#     valuesToNormalize (np.array) = array containing the values of the pupil area to normalize
#     returns:
#     noramlizedData (np.array) = variable containing an array with normalized values
#     '''
#     minVal = np.nanmin(pupilArea) 
#     maxVal = np.nanmax(pupilArea)
#     minVal1 = np.nanmin(pupilArea)
#     minVal2 = np.nanmin(pupilArea1)
#     minVal3 = np.nanmin(pupilArea2)
#     minArray = np.array([minVal1, minVal2, minVal3])
#     minValue = np.amin(minArray)
#     maxVal1 = np.nanmax(pupilArea)
#     maxVal2 = np.nanmax(pupilArea1)
#     maxVal3 = np.nanmax(pupilArea2)
#     maxArray = np.array([maxVal1, maxVal2, maxVal3])
#     maxValue = np.amin(maxArray) 
#     rangeValues = maxValue - minValue 
#     listData = [] 
#     for i in valuesToNormalize: 
#         substractMin = i - minValue 
#         newData = substractMin/rangeValues 
#         listData.append(newData) 
#         normalizedData = np.asarray(listData) 
#     return(normalizedData)
#
#def mean_freqs(arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5, arrFreq1a, arrFreq2a, arrFreq3a, arrFreq4a, arrFreq5a, arrFreq1b, arrFreq2b, arrFreq3b, arrFreq4b, arrFreq5b, arrFreq1c, arrFreq2c, arrFreq3c, arrFreq4c, arrFreq5c, arrFreq1d, arrFreq2d, arrFreq3d, arrFreq4d, arrFreq5d, arrFreq1e, arrFreq2e, arrFreq3e, arrFreq4e, arrFreq5e):
#     
#     totalPreFreq2khz = np.array([arrFreq1, arrFreq1a, arrFreq1b])
#     totalPostFreq2khz = np.array([arrFreq1c, arrFreq1d, arrFreq1e])
#     totalPreFreq4khz = np.array([arrFreq2, arrFreq2a, arrFreq2b])
#     totalPostFreq4khz = np.array([arrFreq2c, arrFreq2d, arrFreq2e])
#     totalPreFreq8khz = np.array([arrFreq3, arrFreq3a, arrFreq3b])
#     totalPostFreq8khz = np.array([arrFreq3c, arrFreq3d, arrFreq3e])
#     totalPreFreq16khz = np.array([arrFreq4, arrFreq4a, arrFreq4b])
#     totalPostFreq16khz = np.array([arrFreq4c, arrFreq4d, arrFreq4e])
#     totalPreFreq32khz = np.array([arrFreq5, arrFreq5a, arrFreq5b])
#     totalPostFreq32khz = np.array([arrFreq5c, arrFreq5d, arrFreq5e])
#     
#     meanPreFreq2kHz = np.average(totalPreFreq2khz)
#     meanPostFreq2kHz = np.average(totalPostFreq2khz)
#     meanPreFreq4khz = np.average(totalPreFreq4khz)
#     meanPostFreq4khz = np.average(totalPostFreq4khz)
#     meanPreFreq8khz = np.average(totalPreFreq8khz)
#     meanPostFreq8khz = np.average(totalPostFreq8khz)
#     meanPreFreq16khz = np.average(totalPreFreq16khz)
#     meanPostFreq16khz = np.average(totalPostFreq16khz)
#     meanPreFreq32khz = np.average(totalPreFreq32khz)
#     meanPostFreq32khz = np.average(totalPostFreq32khz)
#     
#     preData = np.array([meanPreFreq2kHz, meanPreFreq4khz, meanPreFreq8khz, meanPreFreq16khz, meanPreFreq32khz])
#     postData = np.array([meanPostFreq2kHz, meanPostFreq4khz, meanPostFreq8khz, meanPostFreq16khz, meanPostFreq32khz])
#     
#     return(preData, postData)
#
#
#def barScat_plots(firstPlotMeanValues1, firstPlotMeanValues2, xlabel1, xlabel2, firstPlotStdData1, firstPlotStdData2, secondPlotMeanValues1, secondPlotMeanValues2, secondPlotStdData1, secondPlotStdData2, thirdPlotMeanValues1, thirdPlotMeanValues2, thirdPlotStdData1, thirdPlotStdData2, pVal1, pVal2, pVal3):
#     '''
#     Plot bar plots
#     Args:
#     *MeanValues1 (np.array): array containing the average size of the pupil area pre stimulus
#     *MeanValues2 (np.array): array containing the average size of the pupil area post stimulus
#     *StdData1 (np.array): array containing the pupil area pre and stimulus
#     *StdData2 (np.array): array containing the pupil area post and stimulus
#     xlabel1 (string): name of the first condition to compare
#     xlabel2 (string): name of the second condition to compare
#     pVal1..3 (float or int): p-value for each one of the animals
#     Returns:
#     plt.show(): three bar plots within one figure
#     '''
#     barLabelsFontSize = 14
#     meanPreSignal1 = firstPlotMeanValues1.mean(axis = 0) 
#     meanPostSignal1 = firstPlotMeanValues2.mean(axis = 0) 
#     meanPreSignal2 = secondPlotMeanValues1.mean(axis = 0) 
#     meanPostSignal2 = secondPlotMeanValues2.mean(axis = 0) 
#     meanPreSignal3 = thirdPlotMeanValues1.mean(axis = 0) 
#     meanPostSignal3 = thirdPlotMeanValues2.mean(axis = 0)
#     preSignalStd1 = np.std(firstPlotStdData1) 
#     postSignalStd1 = np.std(firstPlotStdData2) 
#     preSignalStd2 = np.std(secondPlotStdData1) 
#     postSignalStd2 = np.std(secondPlotStdData2) 
#     preSignalStd3 = np.std(thirdPlotStdData1) 
#     postSignalStd3 = np.std(thirdPlotStdData2)
#     barMeanValues1 = [meanPreSignal1, meanPostSignal1] 
#     barMeanValues2 = [meanPreSignal2, meanPostSignal2] 
#     barMeanValues3 = [meanPreSignal3, meanPostSignal3]
#     stdErrors1 = [preSignalStd1, postSignalStd1] 
#     stdErrors2 = [preSignalStd2, postSignalStd2] 
#     stdErrors3 = [preSignalStd3, postSignalStd3]
#     shortPval1 = np.round(pVal1, decimals=9)
#     shortPval2 = np.round(pVal2, decimals=9)
#     shortPval3 = np.round(pVal3, decimals=9)
#     pValue1 = 'P-value:', shortPval1
#     pValue2 = 'P-value:', shortPval2
#     pValue3 = 'P-value:', shortPval3
#     dataPlot1 = [firstPlotMeanValues1, firstPlotMeanValues2] 
#     dataPlot2 = [secondPlotMeanValues1, secondPlotMeanValues2] 
#     dataPlot3 = [thirdPlotMeanValues1, thirdPlotMeanValues2]
#     
#     fig, barPlots = plt.subplots(1,3, constrained_layout = True, sharex = True, sharey = True)
#     fig.set_size_inches(9.5, 7.5) 
#     barPlots[0].bar(xlabels, barMeanValues1, yerr = stdErrors1, color = 'g', label = pValue1) 
#     barPlots[0].errorbar(xlabels, barMeanValues1, yerr = stdErrors1, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
#     barPlots[0].set_title(filesDict['name1'], fontsize = barLabelsFontSize)
#     barPlots[0].set_ylabel(scatBarDict['yLabel'], fontsize = barLabelsFontSize)
#     barPlots[0].tick_params(axis='x', labelsize=barLabelsFontSize)
#     barPlots[0].plot(xlabels, dataPlot1, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
#     barPlots[0].legend(prop ={"size":10})
#     barPlots[1].bar(xlabels, barMeanValues2, yerr = stdErrors2, color= 'c', label = pValue2) 
#     barPlots[1].errorbar(xlabels, barMeanValues2, yerr = stdErrors2, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
#     barPlots[1].set_title(filesDict['name2'], fontsize = barLabelsFontSize)
#     barPlots[1].set_xlabel(scatBarDict['xLabelTitle'], fontsize = barLabelsFontSize)
#     barPlots[1].tick_params(axis='x', labelsize=barLabelsFontSize)
#     barPlots[1].plot(xlabels, dataPlot2, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
#     barPlots[1].legend(prop ={"size":10})
#     barPlots[2].bar(xlabels, barMeanValues3, yerr = stdErrors3, color = 'b', label = pValue3) 
#     barPlots[2].errorbar(xlabels, barMeanValues3, yerr = stdErrors3, fmt='none', capsize=5,  alpha=0.5, ecolor = 'black') 
#     barPlots[2].set_title(filesDict['name3'], fontsize = barLabelsFontSize)
#     barPlots[2].tick_params(axis='x', labelsize=barLabelsFontSize)
#     barPlots[2].plot(xlabels, dataPlot3, marker = 'o', color = 'k', alpha = 0.3, linewidth = 1)
#     
#     #plt.ylim(250, 800)
#     plt.suptitle(scatBarDict['title'], fontsize = barLabelsFontSize)
#     barPlots[2].legend(prop ={"size":10})
#     #plt.xlabel("common X", loc = 'center')
#     #plt.savefig(scatBarDict['savedName'], format = 'pdf', dpi =50)
#     plt.show() 
#     return(plt.show()) 
#
#
#def  pupilDilation_time(timeData1, plotData1, timeData2, plotData2, timeData3, plotData3): 
#     fig, signalsPlots = plt.subplots(1,3, constrained_layout = True, sharey = True, sharex = True) 
#     signalsPlots[0].plot(timeData1, plotData1) 
#     signalsPlots[0].set(title = 'Video 1') 
#     signalsPlots[0].set_ylabel('Pupil Area', fontsize = 13)
#     signalsPlots[1].plot(timeData2, plotData2) 
#     signalsPlots[1].set(title = 'Video 2')
#     signalsPlots[1].set_xlabel('Time(s)', fontsize = 13)
#     signalsPlots[2].plot(timeData3, plotData3) 
#     signalsPlots[2].set(title = 'Video 3')
#     plt.suptitle('Average trials behavior in time window: pure011 20220322')
#     plt.show() 
#     return(plt.show())
#
#
#     
#def two_traces_pupilkHz_plot(freqsArray, arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5, arrFreq1a, arrFreq2a, arrFreq3a, arrFreq4a, arrFreq5a, arrFreq1b, arrFreq2b, arrFreq3b, arrFreq4b, arrFreq5b, arrFreq1c, arrFreq2c, arrFreq3c, arrFreq4c, arrFreq5c, arrFreq1d, arrFreq2d, arrFreq3d, arrFreq4d, arrFreq5d, arrFreq1e, arrFreq2e, arrFreq3e, arrFreq4e, arrFreq5e):
#     '''
#     Plots average value of pupil size for a given set of frequencies
#     Args:
#     freqsArray (np.array): array containing the frequencies tested in the experiment
#     arrFreq1..5(np.array): several arrays of the first dataset containing the corresponding post stimulus pupil area for each frequency in freqsArray
#     arrFreq1a..5a(np.array): several arrays of the second dataset containing the corresponding post stimulus pupil area for each frequency in freqsArray
#     arrFreq1b..5b(np.array): several arrays of the third dataset containing the corresponding post stimulus pupil area for each frequency in freqsArray
#     arrFreq1c..5c(np.array): several arrays of the first dataset containing the corresponding pre stimulus pupil area for each frequency in freqsArray
#     arrFreq1d..5d(np.array): several arrays of the second dataset containing the corresponding pre stimulus pupil area for each frequency in freqsArray
#     arrFreq1e..5e(np.array): several arrays of the third dataset containing the corresponding pre stimulus pupil area for each frequency in freqsArray
#     returns:
#     plt.show(): plot traces comparing mean pupil size pre and post stimulus Vs frequencies
#     '''
#
#     labelsSize = 16
#     fig, freqplt = plt.subplots(1,1, constrained_layout = True, sharex = True, sharey = True)
#     fig.set_size_inches(9.5, 7.5, forward = True)
#     label1 = filesDict['name1']
#     label2 = filesDict['name2']
#     label3 = filesDict['name3']
#     labela = 'pre stim size, green'
#     labelb = 'pre stim size, L. blue'
#     labelc = 'pre stim size, D. blue'
#     
#     meanPoint1 = arrFreq1.mean(axis = 0)
#     meanPoint2 = arrFreq2.mean(axis = 0)     
#     meanPoint3 = arrFreq3.mean(axis = 0)     
#     meanPoint4 = arrFreq4.mean(axis = 0)     
#     meanPoint5 = arrFreq5.mean(axis = 0)      
#     meanPoint1a = arrFreq1a.mean(axis = 0)
#     meanPoint2a = arrFreq2a.mean(axis = 0)     
#     meanPoint3a = arrFreq3a.mean(axis = 0)     
#     meanPoint4a = arrFreq4a.mean(axis = 0)     
#     meanPoint5a = arrFreq5a.mean(axis = 0)     
#     meanPoint1b = arrFreq1b.mean(axis = 0)
#     meanPoint2b = arrFreq2b.mean(axis = 0)     
#     meanPoint3b = arrFreq3b.mean(axis = 0)     
#     meanPoint4b = arrFreq4b.mean(axis = 0)     
#     meanPoint5b = arrFreq5b.mean(axis = 0)
#     premeanPoint1c = arrFreq1c.mean(axis = 0)
#     premeanPoint2c = arrFreq2c.mean(axis = 0)     
#     premeanPoint3c = arrFreq3c.mean(axis = 0)     
#     premeanPoint4c = arrFreq4c.mean(axis = 0)     
#     premeanPoint5c = arrFreq5c.mean(axis = 0)     
#     premeanPoint1d = arrFreq1d.mean(axis = 0)
#     premeanPoint2d = arrFreq2d.mean(axis = 0)     
#     premeanPoint3d = arrFreq3d.mean(axis = 0)     
#     premeanPoint4d = arrFreq4d.mean(axis = 0)     
#     premeanPoint5d = arrFreq5d.mean(axis = 0)          
#     premeanPoint1e = arrFreq1e.mean(axis = 0)
#     premeanPoint2e = arrFreq2e.mean(axis = 0)     
#     premeanPoint3e = arrFreq3e.mean(axis = 0)     
#     premeanPoint4e = arrFreq4e.mean(axis = 0)     
#     premeanPoint5e = arrFreq5e.mean(axis = 0)
#     
#     valPlot = [meanPoint1, meanPoint2, meanPoint3, meanPoint4, meanPoint5]
#     valPlota = [meanPoint1a, meanPoint2a, meanPoint3a, meanPoint4a, meanPoint5a]     
#     valPlotb = [meanPoint1b, meanPoint2b, meanPoint3b, meanPoint4b, meanPoint5b]
#     valPlotc = [premeanPoint1c, premeanPoint2c, premeanPoint3c, premeanPoint4c, premeanPoint5c]
#     valPlotd = [premeanPoint1d, premeanPoint2d, premeanPoint3d, premeanPoint4d, premeanPoint5d]     
#     valPlote = [premeanPoint1e, premeanPoint2e, premeanPoint3e, premeanPoint4e, premeanPoint5e]
#
#     freqplt.set_title(filesDict['nameCondition3'], fontsize = labelsSize)
#     freqplt.set_ylabel('Mean pupil Area', fontsize = labelsSize)
#     freqplt.set_xlabel('Frequencies (kHz)', fontsize = labelsSize)
#     freqplt.tick_params(axis='both', labelsize = labelsSize)
#     freqplt.plot(freqsArray, valPlot, color = 'g', marker = 'o')
#     freqplt.plot(freqsArray, valPlota, color = 'c', marker = 'o')
#     freqplt.plot(freqsArray, valPlotb, color = 'b', marker = 'o')   
#     freqplt.plot(freqsArray, valPlotc, color = 'g', marker = 'o', label = labela, alpha = 0.3)
#     freqplt.plot(freqsArray, valPlotd, color = 'c', marker = 'o', label = labelb, alpha = 0.3)
#     freqplt.plot(freqsArray, valPlote, color = 'b', marker = 'o', label = labelc, alpha = 0.3)
#
#     freqplt.grid(b = True)
#     freqplt.legend(prop ={"size":10})
#     plt.xticks(fontsize = labelsSize)
#     plt.yticks(fontsize = labelsSize)
#     plt.suptitle(scatBarDict['plotFreqName'], fontsize = labelsSize)
#     plt.show() 
#     return(plt.show())
#
#def plot_normalized_data(frequencies, preValues, postValues):
#     '''
#     Plots the total pre and post values for each frequency with the mean normalized data
#     '''
#     labela = 'pre stimulus size'
#     labelb = 'post stimulus size'
#      
#     labelSize = 16 
#     fig, normTotal = plt.subplots(constrained_layout = True, sharex= True, sharey = True) 
#     fig.set_size_inches(9.5, 7.5, forward = True)
#     normTotal.set_title(scatBarDict['plotFreqName'], fontsize = labelSize)
#     normTotal.set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
#     normTotal.set_xlabel('Frequencies (kHz)', fontsize = labelSize)
#     normTotal.plot(frequencies, preValues, color = 'y', marker = 'o', label = labela)
#     normTotal.plot(frequencies, postValues, color = 'r', marker = 'o', label = labelb)
#     plt.grid(b = True) 
#     plt.xticks(fontsize = labelSize) 
#     plt.yticks(fontsize = labelSize)
#     plt.legend(prop ={"size":10}) 
#     plt.show() 
#     return(plt.show())
#     
#     
#def plot_norm_errbar(frequencies, preValues, postValues, arrFreq1, arrFreq2, arrFreq3, arrFreq4, arrFreq5, arrFreq1a, arrFreq2a, arrFreq3a, arrFreq4a, arrFreq5a, arrFreq1b, arrFreq2b, arrFreq3b, arrFreq4b, arrFreq5b, arrFreq1c, arrFreq2c, arrFreq3c, arrFreq4c, arrFreq5c, arrFreq1d, arrFreq2d, arrFreq3d, arrFreq4d, arrFreq5d, arrFreq1e, arrFreq2e, arrFreq3e, arrFreq4e, arrFreq5e, freqArr):
#     '''
#     Plots the total pre and post values for each frequency with the mean normalized data
#     '''
#     totalPreFreq2khz = np.array([arrFreq1, arrFreq1a, arrFreq1b])
#     totalPostFreq2khz = np.array([arrFreq1c, arrFreq1d, arrFreq1e])
#     totalPreFreq4khz = np.array([arrFreq2, arrFreq2a, arrFreq2b])
#     totalPostFreq4khz = np.array([arrFreq2c, arrFreq2d, arrFreq2e])
#     totalPreFreq8khz = np.array([arrFreq3, arrFreq3a, arrFreq3b])
#     totalPostFreq8khz = np.array([arrFreq3c, arrFreq3d, arrFreq3e])
#     totalPreFreq16khz = np.array([arrFreq4, arrFreq4a, arrFreq4b])
#     totalPostFreq16khz = np.array([arrFreq4c, arrFreq4d, arrFreq4e])
#     totalPreFreq32khz = np.array([arrFreq5, arrFreq5a, arrFreq5b])
#     totalPostFreq32khz = np.array([arrFreq5c, arrFreq5d, arrFreq5e])
#     meanPreFreq2kHz = np.average(totalPreFreq2khz)
#     meanPostFreq2kHz = np.average(totalPostFreq2khz)
#     meanPreFreq4khz = np.average(totalPreFreq4khz)
#     meanPostFreq4khz = np.average(totalPostFreq4khz)
#     meanPreFreq8khz = np.average(totalPreFreq8khz)
#     meanPostFreq8khz = np.average(totalPostFreq8khz)
#     meanPreFreq16khz = np.average(totalPreFreq16khz)
#     meanPostFreq16khz = np.average(totalPostFreq16khz)
#     meanPreFreq32khz = np.average(totalPreFreq32khz)
#     meanPostFreq32khz = np.average(totalPostFreq32khz)
#     errPre2khz = np.std(totalPreFreq2khz)
#     errPost2khz = np.std(totalPostFreq2khz)
#     errPre4khz = np.std(totalPreFreq4khz)
#     errPost4khz = np.std(totalPostFreq4khz)
#     errPre8khz = np.std(totalPreFreq8khz)
#     errPost8khz = np.std(totalPostFreq8khz)
#     errPre16khz = np.std(totalPreFreq16khz)
#     errPost16khz = np.std(totalPostFreq16khz)
#     errPre32khz = np.std(totalPreFreq32khz)
#     errPost32khz = np.std(totalPostFreq32khz)
#     
#     twokhzErr = np.concatenate((errPre2khz, errPost2khz), axis = None)
#     fourkhzErr = np.concatenate((errPre4khz, errPost4khz), axis = None)
#     eightkhzErr = np.concatenate((errPre8khz, errPost8khz), axis = None)
#     sixkhzErr = np.concatenate((errPre16khz, errPost16khz), axis = None)
#     threetwokhzErr = np.concatenate((errPre32khz, errPost32khz), axis = None)
#    
#     
#     errStdPre = np.concatenate((errPre2khz, errPre4khz, errPre8khz, errPre16khz, errPre32khz), axis = None)
#     errStdPost = np.concatenate((errPost2khz, errPost4khz, errPost8khz, errPost16khz, errPost32khz), axis = None)
#    
#     errStd = np.concatenate((twokhzErr, fourkhzErr, eightkhzErr, sixkhzErr, threetwokhzErr), axis = None)
#
#     preAverage = np.array([meanPreFreq2kHz, meanPostFreq2kHz, meanPreFreq4khz, meanPostFreq4khz, meanPreFreq8khz])
#     postAverage = np.array([meanPostFreq8khz, meanPreFreq16khz, meanPostFreq16khz, meanPreFreq32khz, meanPostFreq32khz])
#     meanArray = np.concatenate((preAverage, postAverage), axis = None)
#     meanArr = np.asarray(meanArray)
#     xVal = freqArr.flatten()
#     labela = 'pre stimulus size'
#     labelb = 'post stimulus size'
#      
#     labelSize = 16 
#     fig, normTotal = plt.subplots(1,1, constrained_layout = True, sharex= True, sharey = True) 
#     fig.set_size_inches(9.5, 7.5, forward = True)
#     normTotal.set_title(scatBarDict['plotFreqName'], fontsize = labelSize)
#     normTotal.set_ylabel('Mean normalized pupil area', fontsize = labelSize) 
#     normTotal.set_xlabel('Frequencies (kHz)', fontsize = labelSize)
#     normTotal.plot(frequencies, preValues, color = '#000000', marker = 'o', label = labela)
#     normTotal.plot(frequencies, postValues, color = '#FFA500', marker = 'o', label = labelb)
#     #normTotal.errorbar(xVal, meanArr , yerr = errStd, fmt='none', capsize=5,  alpha=0.4, ecolor = 'black' )
#     normTotal.errorbar(frequencies, preAverage , yerr = errStdPre, fmt='none', capsize=5,  alpha=0.6, ecolor = '#000000' )
#     normTotal.errorbar(frequencies, postAverage , yerr = errStdPost, fmt='none', capsize=5,  alpha=0.6, ecolor = '#FFA500' )
#
#     plt.grid(b = True) 
#     plt.xticks(fontsize = labelSize) 
#     plt.yticks(fontsize = labelSize)
#     plt.legend(prop ={"size":10}) 
#     plt.show() 
#     return(plt.show())