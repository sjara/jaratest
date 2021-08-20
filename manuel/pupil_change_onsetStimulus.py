"""
Calculating the time(s) for the x axis for FaceMap plots
"""


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
indicesSyncSignal = [0, 2, 4, 6, 8, 10] # Obtains all indices corresponding to the start values from the sync signal.
startValuesSyncSignalVec = np.take(indicesValueSyncSignal, indicesSyncSignal) # Takes the established indices in indicesSyncSignal and looks for the corresponding numbers within the variable indicesValueSyncSignal
timeOfBlink2Event = timeVec[startValuesSyncSignalVec] # Provides the time windows in which the sync signal is on.
rangeTime = np.array([-1, 2]) # Range of time window, one second before the sync signal is on and two seconds after is on.

'''
with numpy.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(arr)
'''

def onset_value(array, ni, k): 

     ''' 
     Helps to find start values of the sync singal in any given array: 
     Args: 
     firstValue = receives the first value of the desired array 
     lastValue = receives the last value of the desired array 
     number = defines the step number to iterate 
     returns: onset values for the several sync signals  
     ''' 

     firstValue = array[0] 
     lastValue = array[ni] 
     stepNumber = k 
     for i in range(firstValue, lastValue, stepNumber): 
         print (i)

