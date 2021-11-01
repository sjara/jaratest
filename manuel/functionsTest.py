'''
This script is to test functions for the project
'''

#Python
import numpy as np
import matplotlib.pyplot as plt
#from jaratoolbox import pupilanalysis


proc = np.load('./fromFullVideos/chad050_020-5_proc.npy', allow_pickle = True).item()
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

blink2Bool = np.logical_and(blink2>103000, blink2<143000) # Boolean values from the blink2 variable where True values will be within the established range.
blink2RangeValues = np.diff(blink2Bool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(blink2RangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable.

'''
with np.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(arr)
'''

def onset_values(array, k): 

     '''
     Helps to find onset start values of the sync singal in any given array: 
     Args: 
     array = array that contains data of the sync signal
     k = step number to create the range from 0 to n index of the given array
     Returns:
     startValuesVec = an array of the indices containing the start onset values of the sync signal.
     '''
     firstIndexValue = 0 
     lastIndexValue = len(array)-1 
     stepNumber = k
     startIndicesValues = range(firstIndexValue, lastIndexValue, stepNumber)
     startIndicesVec = np.array(startIndicesValues)
     onsetStartValues = np.take(array, startIndicesVec)
     return (onsetStartValues)

syncOnsetValues = onset_values(indicesValueSyncSignal, 2)
timeOfBlink2Event = timeVec[syncOnsetValues] # Provides the time values in which the sync signal is on.
timeRange = np.array([-1, 2]) # Range of time window, one second before the sync signal is on and two seconds after is on.

samplingRate = 1/(timeVec[1]-timeVec[0])
windowSampleRange = samplingRate*np.array(timeRange) 
windowSampleVec = np.arange(*windowSampleRange, dtype=int)
windowTimeVec = windowSampleVec/samplingRate
nSamples = len(windowTimeVec)
nTrials = len(timeOfBlink2Event)



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
        thiswin = windowSampleVec + eventSample
        lockedSignal[:,inde] = signal[thiswin]
        #print('this is eventsample:',eventSample)
        #print('this is thiswin:;',thiswin)
        #print(thiswin.shape)
    return (windowTimeVec, lockedSignal)

windowTimeVec, windowed_signal = eventlocked_signal(timeVec, pArea, timeOfBlink2Event, timeRange)


preSignal = windowed_signal[0:30] # Takes the values of the pArea between [-1s to 0s) within the time window
postSignal = windowed_signal[30:90] # Takes the values of the pArea between [0s to 2s] within the time window
averagePreSignal = preSignal.mean(axis = 0)
averagePostSignal = postSignal.mean(axis = 0)
dataToPlot = [averagePreSignal, averagePostSignal]
xlabels = ['Pre Signal', 'Post Signal']


def conditions_Plotting(preArray, postArray): 
     xLabelsToPlot = ['Pre Signal', 'Post Signal'] 
     dataToPlot = [preArray, postArray] 
     fig, trials = plt.subplots(1,1) 
     trials.plot(xLabelsToPlot, dataToPlot, marker = 'o', linewidth=1) 
     trials.set(title = 'Average Pupil Area Vs Pre and Post-signal onset', ylabel = 'Mean Pupil Area') 
     plt.show() 
     return(plt.show())

PrePostSignalpArea = conditions_Plotting(averagePreSignal, averagePostSignal)
 
'''
def conditions_Plotting(preArray, postArray, k): 
    ...:     for i in range(k): 
    ...:         verts = [(preArray[i], postArray[i])] 
    ...:         for i in verts: 
    ...:             codes = [Path.MOVETO, Path.LINETO,  Path.CLOSEPOLY] 
    ...:             pathToPlot = Path(verts, codes) 
    ...:             fig, ax = plt.subplots() 
    ...:             patch = patches.PathPatch(path, facecolor='orange', lw=2) 
    ...:             ax.add_patch(patch) 
    ...:             plt.show() 
    ...:     return(plt.show())
'''    
