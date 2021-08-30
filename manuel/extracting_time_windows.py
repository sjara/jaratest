"""
Calculating the time(s) for the x axis for FaceMap plots
"""


#Python
import numpy as np
import matplotlib.pyplot as plt
#from jaratoolbox import pupilanalysis.



proc = np.load('./to_compare/chad045_030_1_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.



pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
#pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis).
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.
#blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis).



nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video .



minValueTimeVec = np.amin(timeVec) # Minimum value of the variable timeVec_pArea. Added for precision.
maxValueTimeVec = np.amax(timeVec) # Maximum value of the variable timeVec_pArea. Made to prevent the plotting of space without data in the plot.
#range_time = np.array([min_value_timeVec, max_value_timeVec]) # Shows starting and ending seconds of the video.


blink2Bool = np.logical_and(blink2>1000, blink2<2000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.
indicesSyncSignal = [0, 2, 4, 6, 8, 10] # Obtains all indices corresponding to the start values from the sync signal. --> trying to define with a FUNCTIONN!!!
startValuesSyncSignalVec = np.take(indicesValueSyncSignal, indicesSyncSignal) # Takes the established indices in indicesSyncSignal and looks for the corresponding numbers within the variable indicesValueSyncSignal
timeOfBlink2Event = timeVec[startValuesSyncSignalVec] # Provides the time windows in which the sync signal is on.
rangeTime = np.array([-1, 2]) # Range of time window, one second before the sync signal is on and two seconds after is on.



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
        print('Diese ist trial:',eventSample)
        thiswin = windowSampleVec + eventSample
        print('Diese ist samples:',thiswin)
        lockedSignal[:,inde] = signal[thiswin]
    return (windowTimeVec, lockedSignal)

samplingRate = 1/(timeVec[1]-timeVec[0])
windowSampleRange = samplingRate*np.array(rangeTime) 
windowSampleVec = np.arange(*windowSampleRange, dtype=int)
windowTimeVec = windowSampleVec/samplingRate
nSamples = len(windowTimeVec)
nTrials = len(timeOfBlink2Event)

windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, rangeTime)

plt.plot(windowTimeVec, windowed_signal)
plt.title('Trials Vs Time window (s)')
plt.xlabel('Time window (s)')
plt.ylabel('Trials')
plt.show()

'''
fig, (signalWindow, comparePlot) = plt.subplots(2, 1, sharex = False, sharey = False, constrained_layout = True)
signalWindow.plot(windowTimeVec, windowed_signal)
signalWindow.set(title = 'Trials Vs Time window (s)' , xlabel = 'Time window (s)', ylabel = 'Trials')
signalWindow.grid(b = True)
comparePlot.plot(timeVec, blink2)
comparePlot.set(title = 'Sync signal Vs Time (s)', xlabel = 'Time (s)', ylabel = 'on/off')
comparePlot.grid(b = True)
plt.show()
'''
