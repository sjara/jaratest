"""
Calculating the time(s) for the x axis for FaceMap plots
"""


#Python
import numpy as np
import matplotlib.pyplot as plt
#from jaratoolbox import pupilanalysis



proc = np.load('./to_compare/chad045_030_1_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.



pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
#pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis).
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.
#blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis).



nframes_pArea = len(pArea) # Contains length of pArea variable.
nframes_blink2 = len(blink) # Contains length of blink2_a variable.
frameVec_pArea = np.arange(0, nframes_pArea, 1) # Vector of the total frames from the video.
frameVec_blink2 = np.arange(0, nframes_blink2, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec_pArea * 1)/framerate # Time Vector to calculate the length of the video 



min_value_timeVec = np.amin(timeVec) # Minimum value of the variable timeVec_pArea. Added for precision
max_value_timeVec = np.amax(timeVec) # Maximum value of the variable timeVec_pArea. Made to prevent the plotting of space without data in the plot
#range_time = np.array([min_value_timeVec, max_value_timeVec]) # Shows starting and ending seconds of the video


blink2_bool = np.logical_and(blink2>1000, blink2<2000) # Boolean values from the blink2 variable where True values will be within the established range
blink2_range_values = np.diff(blink2_bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
start_value_syncSignal = np.flatnonzero(blink2_range_values) # Provides all the numbers as 'True' from the blink2_binary variable
time_of_blink2_event = timeVec[start_value_syncSignal] # Provides the time windows in which the sync signal is on
range_time = np.array([-1, 2]) # Range of time window


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
        lockedSignal (np.array): extracted windows of signal aligned to event. Size: (nSamples,nEvents)
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
        thiswin = windowSampleVec + eventSample
        lockedSignal[:,inde] = signal[thiswin]
    return (windowTimeVec, lockedSignal)

windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, time_of_blink2_event, range_time)

#plt.plot(timeVec, blink2)
#plt.plot(windowed_signal)



