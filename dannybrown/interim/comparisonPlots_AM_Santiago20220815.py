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
subject = 'pure012'
date = '2022-08-11'

# Load data from infovideos file
#infovideosFilename = os.path.join('/home/jarauser/src/jarainfo/infovideos', f'{subject}_infovideos.py') #CHANGE
infovideosFilename = os.path.join(settings.INFOVIDEOS_PATH, f'{subject}_infovideos.py')
infovideos = extrafuncs.read_infofile(infovideosFilename)

# File locations for behavioral data and processed FaceMap data
for session in infovideos.videos.sessions:
    if session.date == date:
        selSession = session
        break

filename_behav = selSession.behavFile
fileloc_behav = os.path.join(settings.BEHAVIOR_PATH,subject,filename_behav)
filename_video = selSession.videoFile
filename_fmap = '_'.join([filename_video.split('.')[0],'proc.npy'])
fileloc_fmap = os.path.join(settings.VIDEO_PATH,f'{subject}_processed', filename_fmap)

# Load the Behavioral Data and FaceMap data
bdata = loadbehavior.BehaviorData(fileloc_behav)
faceMap = fmap.load_data(os.path.join(fileloc_fmap), runchecks=False)

##--- obtain values where sync signal turns on ---
#_, syncOnsetValues, _, _ = fmap.extract_sync(faceMap)
#timeOfSyncOnset = timeVec[syncOnsetValues] # Provides the time values in which the sync signal turns on.

########## IF ERROR IS THROWN BELOW, FIRST INSPECT THE FILE AND THEN MAKE MANUAL CHANGES HERE ######
# More freqs than sync lights?
#freqs=freqs[0:-1]
# -or- # 
# More sync lights than freqs?
#syncOnsetValues=syncOnsetValues[0:-1]
#timeOfSyncOnset=timeOfSyncOnset[0:-1]


# LIMIT ANALYSIS BY 1ST SOUND PRESENTED
#syncOnsetValues_4hz=syncOnsetValues[bdata['preFreq']==4]
#syncOnsetValues_7hz=syncOnsetValues[bdata['preFreq']==7]
#syncOnsetValues_12hz=syncOnsetValues[bdata['preFreq']==12]
#timeOfSyncOnset_4hz=timeOfSyncOnset[bdata['preFreq']==4]
#timeOfSyncOnset_7hz=timeOfSyncOnset[bdata['preFreq']==7]
#timeOfSyncOnset_12hz=timeOfSyncOnset[bdata['preFreq']==12]

if selSession.sessionType == 'random6chord':
    freqs = bdata['currentFreq'] # works with am_tuning_curve paradigm
else:
    freqs = bdata['postFreq'] # works with gonogo paradigm 
freqs_list = np.unique(freqs)

for theseTrials in [4]: #freqs_list:
    #--- obtain frequencies data ---
    if selSession.sessionType == 'random6chord':
        freqs = bdata['currentFreq'] # works with am_tuning_curve paradigm
    else:
        freqs = bdata['postFreq'] # works with gonogo paradigm 
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
    syncOnsetValues = syncOnsetValues[bdata['preFreq']==theseTrials]
    timeOfSyncOnset=timeOfSyncOnset[bdata['preFreq']==theseTrials]
    freqs=freqs[bdata['preFreq']==theseTrials]

###########################################################################

    if len(freqs) != syncOnsetValues.shape[0]: # Throw an error if there wasn't a sync light for every sound
        print('ERROR: # of sync light signals does not match number of sounds played:')
        print(f'freqs = {len(freqs)}, sync lights = {syncOnsetValues.shape[0]}.')
        print('See code line 63 for troubleshooting options.')
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
    
    #--- For p-values: Align trials to events ---
    # create signal locked to sync light, for each condition
    timeRange = np.array([-0.5, 2.0]) # Create range for time window
    windowed_signal=[]
    for inde,freq in enumerate(freqs_list):
        windowTimeVec, signals = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freq], timeRange)
        windowed_signal.append(signals)
    
    
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
    
    pAreaDilated = []
    for inde,freq in enumerate(freqs_list):
        pupilDilationTimeWindowVec, thispArea = eventlocked_signal(timeVec, pArea, timeOfSyncOnset[freqs==freq], timeRangeForPupilDilation)
        pAreaDilated.append(thispArea)
        
    meanpAreaDilated = []
    stdpAreaDilated = []
    for inde in range(len(freqs_list)):
        thismean = pAreaDilated[inde].mean(axis = 1)
        thisstd = pAreaDilated[inde].std(axis = 1)        
        meanpAreaDilated.append(thismean)
        stdpAreaDilated.append(thisstd)
        
    nTrials = []
    for inde in range(len(freqs_list)):
        thisN = pAreaDilated[inde].shape[1]
        nTrials.append(thisN)
    
    def comparison_plot(time, valuesData, valuesStd, pVals, freqs_list, nTrials, firstSound): 
         ''' 
         Creates 1 figure with 6 plots 
         Args: 
         time = vector values for x axis 
         valuesData (np.array) = array of mean pupil traces to be plotted
         valuesStd (np.array) = array of std dev of pupil traces to be plotted
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
         
         legendLabels = []
         for f_ind, freq in enumerate(freqs_list):
            iteration = f'Sound change = {firstSound}-->{freq} Hz, nTrials = {nTrials[f_ind]}, pval = {pVals[f_ind]}'
            legendLabels.append(iteration)
    
         alphas = np.linspace(.4,1,len(freqs_list))
         colors = ['red','blue','orange']
         for inde in range(len(freqs_list)):
             subplt.plot(time, valuesData[inde], alpha = alphas[inde], label = legendLabels[inde], linewidth = 4, color = colors[inde])
             subplt.plot(time, valuesData[inde]+valuesStd[inde], alpha = alphas[inde], linewidth = 1, color = colors[inde])
             subplt.plot(time, valuesData[inde]-valuesStd[inde], alpha = alphas[inde], linewidth = 1, color = colors[inde])
             # This is nearly done; just need to know how to make the stds the same color as its corresponding mean plot.
    
         subplt.set_xlabel('Time (s)', fontsize = labelsSize)
         subplt.set_ylabel('Pupil Area', fontsize = labelsSize)
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
    
    
    if np.logical_or(selSession.sessionType == 'lowestfirst3chord', selSession.sessionType == 'lowestfirst6chord'):
        firstSound = np.min(freqs_list)
    if selSession.sessionType == 'highestfirst6chord':
        firstSound = np.max(freqs_list)
    if selSession.sessionType == 'random6chord':
        firstSound='(only one sound)'
    if selSession.sessionType == 'AMrandom3rate':
        firstSound = theseTrials
    
    
    #--- plot for all included frequencies ---
    OverLapPlots = comparison_plot(pupilDilationTimeWindowVec, meanpAreaDilated, stdpAreaDilated, pvals, freqs_list=freqs_list,
                                   nTrials = nTrials, firstSound=firstSound)