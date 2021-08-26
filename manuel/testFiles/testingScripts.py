"""
Test script to try draft processes
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



nframes = len(pArea) # Contains length of pArea variable.
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video 

min_value_timeVec = np.amin(timeVec) # Minimum value of the variable timeVec_pArea. Added for precision
max_value_timeVec = np.amax(timeVec) # Maximum value of the variable timeVec_pArea. Made to prevent the plotting of space without data in the plot
#min_value_timeVec_blink2 = np.amin(timeVec_blink2) # Minimum value of the variable timeVec_blink2. Added for precision for plotting and prevent using plot labels without data
#max_value_timeVec_blink2 = np.amax(timeVec_blink2) # Maximum value of the variable timeVec_blink2. Made to prevent the plotting of space without data in the plot
inferior_limit_y_axis = np.amin(pArea) # Defines the min value for the y axis
superior_limit_y_axis = pArea[nframes - 6] # Defines max value for the y axis. The 6 corresponds to the last 6 elements of the array. Still trying to find a way to not hard-code it.

'''
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
"""

# Note: the last 6 elements in pArea allowed for the plot to create an "infinite" line in the y axis. Thus, it doesn't allow the user to properly analyze the pupil data.  



fig, (pupil_axis, blink_axis) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil_axis.set(title = 'Chad045, 2020-10-30', ylabel = 'Pupil Area')
plt.setp((pupil_axis, blink_axis), xticks = (np.arange(0, 35, 1))) #Sets up number of ticks in both plots
pupil_axis.plot(timeVec_pArea, pArea)
pupil_axis.set_xlim([min_value_timeVec_pArea, max_value_timeVec_pArea])
pupil_axis.set_ylim([inferior_limit_y_axis, superior_limit_y_axis])
pupil_axis.grid(b = True)
blink_axis.set(xlabel = 'Time (s)', ylabel = 'on/off')
blink_axis.plot(timeVec_blink2, blink2)
blink_axis.set_xlim([min_value_timeVec_blink2, max_value_timeVec_blink2])
blink_axis.grid(b = True)
plt.show()
"""
'''
