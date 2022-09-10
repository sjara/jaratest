'''
This script creates plots of pupil dilation, and is configured for the am_tuning_curve and gonogo
paradigms.  It creates windowed-average plots of pupil data, which are grouped by the various frequency
changes the animal is presented with.  The script outputs n plots, with 'n' determined by the number of
unique frequency changes that appear in the data provided.
'''
# Imports
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

# Reminder: may need to mount jarahubdata.  In terminal:
#sshfs -o ro -o idmap=user jarauser@jarahub:/data/ /mnt/jarahubdata

# Input the session parameters
subject = 'pure014'
date = '2022-09-07'
breakout = 1
runplot = 0
limitrunning = 0

runThreshold = .35
runningThresholdTime = 3
 
# Load data from infovideos file
#infovideosFilename = os.path.join('/home/jarauser/src/jarainfo/infovideos', f'{subject}_infovideos.py') #CHANGE
infovideosFilename = os.path.join(settings.INFOVIDEOS_PATH, f'{subject}_infovideos.py')
infovideos = extrafuncs.read_infofile(infovideosFilename)

# File locations for behavioral data and processed FaceMap data
for session in infovideos.videos.sessions:
    if session.date == date:
        selSession = session
        break
if session.date != date:
    raise ValueError('ERROR - No data with that date in infovideos file.')

filename_behav = selSession.behavFile
fileloc_behav = os.path.join(settings.BEHAVIOR_PATH,subject,filename_behav)
filename_video = selSession.videoFile
filename_fmap = '_'.join([filename_video.split('.')[0],'proc.npy'])
fileloc_fmap = os.path.join(settings.VIDEO_PATH,f'{subject}_processed', filename_fmap)

paradigm = filename_behav[8:-13]
params = selSession.sessionType

# Load the Behavioral Data and FaceMap data
bdata = loadbehavior.BehaviorData(fileloc_behav)
faceMap = fmap.load_data(os.path.join(fileloc_fmap), runchecks=False)

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
#        raise ValueError('Your first window falls outside the recorded data.')
        print('NOTE: Your first window fell outside of the recorded data; the trial has been discarded.')
        eventOnsetTimes = eventOnsetTimes[1::]
    if (eventOnsetTimes[-1] + windowTimeRange[-1]) > timeVec[-1]:
#        raise ValueError('Your last window falls outside the recorded data.')
        print('NOTE: Your last window fell outside of the recorded data; the trial has been discarded.')
        eventOnsetTimes = eventOnsetTimes[0:-1]
    samplingRate = 1/(timeVec[1]-timeVec[0])
    windowSampleRange = samplingRate*np.array(windowTimeRange)  # units: frames
    windowSampleVec = np.arange(*windowSampleRange, dtype=int) # units: frames
    windowTimeVec = windowSampleVec/samplingRate # Units: time
    nSamples = len(windowTimeVec) # time samples / trial
    nTrials = len(eventOnsetTimes) # number of times the sync light went off
    lockedSignal = np.empty((nSamples,nTrials))
    for inde,eventTime in enumerate(eventOnsetTimes):
       eventSample = np.searchsorted(timeVec, eventTime) # eventSample = index at which the sync turns on
       thiswin = windowSampleVec + eventSample # indexes of window
       lockedSignal[:,inde] = signal[thiswin]
    return (windowTimeVec, lockedSignal)

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
   
def comparison_plot(time, valuesData, pVals, freqs_list, nTrials, firstSound): 
 ''' 
 Creates 1 figure with 6 plots 
 Args: 
 time = vector values for x axis 
 valuesData (np.array) = array of mean pupil traces to be plotted
 pVals (np.array) = list of pValues associated with each frequency
 freqs_list (np.array) = list of frequencies included
 nTrials (np.array) = number of trials at each frequency
 firstSound (float) = Frequency value of the first sound presented in each trial.
 returns: 
 plt.show() = 1 figure with 6 plots using the input data 
 ''' 
 labelsSize = 16
 fig, subplt = plt.subplots(1,1)
 fig.set_size_inches(18, 10, forward = True)
 pVals = np.round(pVals, decimals=4)
 
 if paradigm == 'am_tuning_curve':
     legendLabels = []
     for f_ind, freq in enumerate(freqs_list):
        iteration = f'Sound = {freq} Hz'
        legendLabels.append(iteration)
    
     alphas = np.linspace(.4,1,len(freqs_list))
     for inde in range(len(freqs_list)):
         subplt.plot(time, valuesData[inde], alpha = alphas[inde], label = legendLabels[inde], linewidth = 4)
    
     subplt.set_title(f'Pupil behavior in response to a sound turning on, then off.  Sound = {theseTrials} Hz', fontsize = labelsSize)
     plt.suptitle(f'Mouse = {subject}.  Data Collected {date}.  Params: {params}.  # of Trials: {len(freqs)}.', fontsize = labelsSize)
     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     plt.axvline(0, label = 'sound turns off', color = 'red', linestyle='dashed', linewidth = 3)
     plt.grid(b = True)
 
 if paradigm == 'detectiongonogo':
     legendLabels = []
     for f_ind, freq in enumerate(freqs_list):
        iteration = f'Sound change = {firstSound}-->{freq} Hz, nTrials = {nTrials[f_ind]}, pval = {pVals[f_ind]}'
        legendLabels.append(iteration)
     alphas = np.linspace(.4,1,len(freqs_list))
     
     for inde in range(len(freqs_list)):
         subplt.plot(time, valuesData[inde], alpha = alphas[inde], label = legendLabels[inde], linewidth = 4)
    
     subplt.set_xlabel('Time (s)', fontsize = labelsSize)
     subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
     plt.axvline(0, label = 'sound turns on', color = 'red', linestyle='dashed', linewidth = 3)
     subplt.set_title(f'Pupil behavior in response to a sound change (with no gap): {len(freqs_list)} Rates.  Trials beginning with {theseTrials} Hz', fontsize = labelsSize)
     plt.suptitle(f'Mouse = {subject}.  Data Collected {date}.', fontsize = labelsSize)
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

########## IF ERROR IS THROWN BELOW, FIRST INSPECT THE FILE AND THEN MAKE MANUAL CHANGES HERE ######
# More freqs than sync lights?
#freqs=freqs[0:-1]
# -or- # 
# More sync lights than freqs?
#syncOnsetValues=syncOnsetValues[0:-1]
#timeOfSyncOnset=timeOfSyncOnset[0:-1]


#light = np.array([1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,5,5,5,5,5,5,5,5,5,5,7,7,7,7,7,7,7,7,7,7,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,7,7,7,7,7,7,7,7,7,7,7,5,5,5,5,5,5,5,5,5,5,5,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1])
light = np.ones(100)
if session.date == '2022-08-25':
    light=np.ones(80)

if breakout == 1:
    light[0:10] = 3
    light[10:20] = 4
    light[20:30] = 5
    light[30:40] = 6
    light[40:60] = 7
    light[60:70] = 6
    light[70:80] = 5
    light[80:90] = 4
    light[90:100] = 3
 

bdata['currentFreq'] = light


# Build list of unique frequencies
if paradigm == 'am_tuning_curve':
#    if params == 'AM4sec10off':
#        freqs = light
#    else:
    freqs = bdata['currentFreq'] # works with am_tuning_curve paradigm

if paradigm == 'detectiongonogo':
    freqs = bdata['postFreq'] # works with gonogo paradigm 

freqs_list = np.unique(freqs)

# LIMIT ANALYSIS BY 1ST SOUND PRESENTED
for theseTrials in freqs_list:
    
    #--- obtain frequencies data ---
    if paradigm == 'am_tuning_curve':
#        if params == 'AM4sec10off':
#            freqs = light
#        else:
        freqs = bdata['currentFreq'] # works with am_tuning_curve paradigm
    if paradigm == 'detectiongonogo':
        freqs = bdata['postFreq'] # works with gonogo paradigm 
    freqs_list = np.unique(freqs)
    
    
    
    #--- obtain pupil and running data ---
    pArea = fmap.extract_pupil(faceMap)
    running, _ = fmap.extract_whisking(faceMap, window_width = 60)
    
    #--- marker of running behavior ----
    running_binary = np.zeros(len(running))
    running_binary[running<runThreshold] = 1
    
    #---calculate number of frames, frame rate, and time vector---
    nframes = len(pArea) # Number of frames.
    frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
    framerate = 30 # frame rate of video
    timeVec = frameVec / framerate # Time Vector to calculate the length of the video.
    
    #--- obtain values where sync signal turns on ---
    _, syncOnsetValues, _, _ = fmap.extract_sync(faceMap)
    timeOfSyncOnset = timeVec[syncOnsetValues] # Provides the time values in which the sync signal turns on.
    
    if limitrunning == 1:
        freqs = freqs[running_binary[syncOnsetValues - runningThresholdTime*framerate]==0]
        syncOnsetValues = syncOnsetValues[running_binary[syncOnsetValues - runningThresholdTime*framerate]==0]
        timeOfSyncOnset = timeVec[syncOnsetValues]
        
    
    
    #--- Make sure the # of sync lights observed equals the # of sounds played ---    
    if session.date == '2022-08-25':
        syncOnsetValues = syncOnsetValues[:-4] #HARDCODED FOR A VIDEO THAT WAS NOT ENDED ON TIME
        timeOfSyncOnset = timeOfSyncOnset[:-4] #HARDCODED FOR A VIDEO THAT WAS NOT ENDED ON TIME
        
    if len(freqs) != syncOnsetValues.shape[0]:
        if len(freqs) - syncOnsetValues.shape[0] == 1:
            # More freqs than sync lights?
            print('ERROR: # of sync light signals does not match number of sounds played:')
            print(f'freqs = {len(freqs)}, sync lights = {syncOnsetValues.shape[0]}.')
            print('Using solution: last trial was removed.')
            freqs=freqs[0:-1] 
        if len(freqs) - syncOnsetValues.shape[0] == -1:
            # More sync lights than freqs?
            print('ERROR: # of sync light signals does not match number of sounds played:')
            print(f'freqs = {len(freqs)}, sync lights = {syncOnsetValues.shape[0]}.')
            print('Using solution: last trial was removed.')
            syncOnsetValues=syncOnsetValues[0:-1]
            timeOfSyncOnset=timeOfSyncOnset[0:-1]
        else:
            print('ERROR: # of sync light signals does not match number of sounds played and needs to be inspected')
            sys.exit()    
    if limitrunning == 0:
        if paradigm == 'am_tuning_curve':
            syncOnsetValues = syncOnsetValues[bdata['currentFreq']==theseTrials]
            timeOfSyncOnset=timeOfSyncOnset[bdata['currentFreq']==theseTrials]
            freqs=freqs[bdata['currentFreq']==theseTrials] 
        if paradigm == 'detectiongonogo':
            syncOnsetValues = syncOnsetValues[bdata['preFreq']==theseTrials]
            timeOfSyncOnset=timeOfSyncOnset[bdata['preFreq']==theseTrials]
            freqs=freqs[bdata['preFreq']==theseTrials]    
        # skip to the next freq, if this one never appears as a first freq.
        if len(timeOfSyncOnset) == 0:
            continue

###########################################################################
    #--- For p-values: Align trials to events ---
    # create signal locked to sync light, for each condition
    timeRange = np.array([-0.5, 2.0]) # Create range for time window
    windowed_signal=[]
    for inde,freq in enumerate(freqs_list):
        windowTimeVec, signals = eventlocked_signal(timeVec, pArea, timeOfSyncOnset, timeRange)
        windowed_signal.append(signals)
    
    #--- For p-values: Obtain pupil pre and post stimulus values, and average size ---
    preSignal = []
    postSignal = []
    for inde in range(len(freqs_list)):
        thisValuePre, thisValuePost = find_prepost_values(windowTimeVec, windowed_signal[inde], -0.5, 0, 1.4, 2.0)
        preSignal.append(thisValuePre)
        postSignal.append(thisValuePost)
        
    avgPreSignal = []
    avgPostSignal = []
    for inde in range(len(freqs_list)):
        thisfreqPre = preSignal[inde].mean(axis = 0)
        thisfreqPost = postSignal[inde].mean(axis = 0)
        avgPreSignal.append(thisfreqPre)
        avgPostSignal.append(thisfreqPost)
    
    #--- For p-values: Wilcoxon test and Pvalue statistics ---
    wstats = []
    pvals = []
    for inde in range(len(freqs_list)):
        thisW, thisP = stats.wilcoxon(avgPreSignal[inde], avgPostSignal[inde])
        wstats.append(thisW)
        pvals.append(thisP)
    
    #--- For Plots: Defining time range for pupil, extracting the traces, create plotting function ---
    timeRangeForPupilDilation = np.array([-15, 15])
    if np.any([selSession.sessionType == 'pureTone20sec', selSession.sessionType == 'AM20sec', selSession.sessionType == 'AM20secControl']):
        timeRangeForPupilDilation = np.array([-25, 25])
    if np.any([selSession.sessionType == 'AM4sec10off']):
        timeRangeForPupilDilation = np.array([-5, 12])
    
    pAreaDilated = []
    for inde,freq in enumerate(freqs_list):
        pupilDilationTimeWindowVec, thispArea = eventlocked_signal(timeVec, pArea, timeOfSyncOnset, timeRangeForPupilDilation)
        pAreaDilated.append(thispArea)
        
    meanpAreaDilated = []
    for inde in range(len(freqs_list)):
        thismean = pAreaDilated[inde].mean(axis = 1)
        meanpAreaDilated.append(thismean)
        
    nTrials = []
    for inde in range(len(freqs_list)):
        thisN = pAreaDilated[inde].shape[1]
        nTrials.append(thisN)
      
    if np.logical_or(selSession.sessionType == 'lowestfirst3chord', selSession.sessionType == 'lowestfirst6chord'):
        firstSound = np.min(freqs_list)
    if selSession.sessionType == 'highestfirst6chord':
        firstSound = np.max(freqs_list)
    if selSession.sessionType == 'random6chord':
        firstSound='(only one sound)'
    if np.any([selSession.sessionType == 'AMrandom3rate', selSession.sessionType == 'AMpreExtreme3rate', selSession.sessionType == 'pureTone20sec',
              selSession.sessionType == 'AM20sec', selSession.sessionType == 'AM4sec10off']):
        firstSound = theseTrials
       
    #--- plot for all included frequencies ---
#    OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, meanpAreaDilated, pvals, freqs_list=freqs_list,
#                                   nTrials = nTrials, firstSound=firstSound)
#    plt.ylim([650,1850])
    
    runningTraces = []
    for inde,freq in enumerate(freqs_list):
        runTimeWindowVec, thisRunTrace = eventlocked_signal(timeVec, running, timeOfSyncOnset, timeRangeForPupilDilation)
        runningTraces.append(thisRunTrace)
    
    meanRunDilated = []
    for inde in range(len(freqs_list)):
        thismean = runningTraces[inde].mean(axis = 1)
        meanRunDilated.append(thismean)
#    
#    OverLapPlots_running = comparison_plot(runTimeWindowVec, meanRunDilated, pvals, freqs_list=freqs_list, 
#                                           nTrials = nTrials, firstSound=firstSound)
#    plt.title(f'Average running behavior locked to a sound turning on, then off.', fontsize = 16)
#    plt.suptitle(f'Mouse = {subject}.  Data Collected {date}.  Params: {params}.  # of Trials: {len(freqs)}.', fontsize = 16)
#    plt.xlabel('Time (s)', fontsize = 16)
#    plt.ylabel('Running Movement', fontsize = 16)
#    plt.axvline(0, label = 'sound turns off', color = 'red', linestyle='dashed', linewidth = 3)
    if breakout != 1:
        plt.figure()
    if breakout == 1:
        plt.plot(pupilDilationTimeWindowVec, meanpAreaDilated[0], linewidth = 3, label = f'Light = {theseTrials}.  nTrials = {len(freqs)}')
    if breakout != 1:
        plt.plot(pupilDilationTimeWindowVec, meanpAreaDilated[0], linewidth = 3, label = f'nTrials = {len(freqs)}')
    plt.grid(b = True)
    plt.title(f'Pupil trace, all trials.  Mouse: {subject}.  Date: {date}', fontsize=18)
    if limitrunning == 1:
        plt.title(f'Pupil trace restricted to running =< {runThreshold} at {-runningThresholdTime} seconds.  Mouse: {subject}.  Date: {date}', fontsize=18)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Pupil Area', fontsize=14)

plt.axvline(-4, label = 'sound turns on', color = 'red', linestyle='dashed', linewidth = 3)
plt.axvline(0, label = 'sound turns off', color = 'blue', linestyle='dashed', linewidth = 3)
plt.axvline(10, color = 'red', linestyle='dashed', linewidth = 3)
plt.legend(prop={'size':12})  
    
if runplot == 1:
    plt.figure()
    plt.plot(runTimeWindowVec, meanRunDilated[0], linewidth = 3, label = f'nTrials = {len(freqs)}')
    plt.grid(b = True)
    plt.title(f'Running trace.  Mouse: {subject}.  Date: {date}', fontsize=18)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Running', fontsize=14)
    
    plt.axvline(-4, label = 'sound turns on', color = 'red', linestyle='dashed', linewidth = 3)
    plt.axvline(0, label = 'sound turns off', color = 'blue', linestyle='dashed', linewidth = 3)
    plt.axvline(10, color = 'red', linestyle='dashed', linewidth = 3)
    plt.legend(prop={'size':12})            

# Investigating: raw running and pupil traces, with sync light
if breakout != 1:
    plt.figure()
    plt.plot(pArea, label='pupil') # plot pupil
    plt.plot(np.mean(pArea)/np.mean(running)*running, label='running (adjusted)', color = 'purple') # plot running, adjusted to pupil mean
    counter=1
    for x in syncOnsetValues:
        if np.logical_and(counter%10 == 0, limitrunning ==0):
            plt.axvline(x, linestyle='dashed', color = 'orange')
            counter+=1
        else:
            plt.axvline(x, linestyle='dashed', color = 'blue')
            counter+=1
    plt.legend()
    plt.title('Raw Traces - Included trials.')