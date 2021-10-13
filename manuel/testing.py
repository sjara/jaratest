'''
This script is for the project of pupil dilation. Its purpose is for tests only
'''

import numpy as np
import matplotlib.pyplot as plt

#Lines to change for each video: 10, 29, 43, 67, 113, 114

proc = np.load('./project_videos/projectOutputs/pure001_20210928_syncSound_01_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap.


#---obtain pupil data ---
pupil = proc['pupil'][0] # Dic.
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video.
blink = proc['blink'][0] # numpy.array. Contains calculation of the sync signal in each frame of the video.
blink1 = proc['blink']   # List.
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting.

#---obtain values where sync signal is on---
newBlinkBool = np.logical_and(blink2>0, blink2<80000) # Boolean values from the blink2 variable where True values will be within the established range.
newBlinkRangeValues = np.diff(newBlinkBool) # Determines the start and ending values (as the boolean value True) where the sync signal is on. 
indicesValueSyncSignal = np.flatnonzero(newBlinkRangeValues) # Provides all the indices of numbers assigned as 'True' from the blink2_binary variable


'''
#it plots something weird
if 'False' in newBlinkBool: 
     newArr = np.delete(newBlinkBool, False)
     print(newArr)
'''



with np.printoptions(threshold=np.inf): # Use the following code to show all the elements within a large array
    print(blink)


#---calculate number of frames, frame rate, and time vector---
nframes = len(pArea) # Contains length of pArea variable (equivalent to the blink variable).
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video.


newpArea = pArea[pArea != np.amax(pArea)] #Trims weird values from variable (elim. Largest elements)
newBlink = blink2[blink2 != np.amax(blink2)] #Trims weird values from variable ((elim. Largest elements)
newFrame = frameVec[newBlinkBool]

#---plot to find out which time range can be used---

fig, (pupil, blik) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'pure001_20210928_syncVisibleNoSound_01', ylabel = 'Pupil Area', xlabel = 'frames')
#plt.setp((pupil, blink), xticks = (np.arange(0, 50, 0.1))) #Set ups number of ticks in both plots
pupil.plot(newFrame, newpArea) #before: pupil.plot(frameVec, pArea)
pupil.grid(b = True)
blik.set(ylabel = 'on/off', xlabel = 'frames')
blik.grid(b = True)
blik.plot(newFrame, newBlink) #before: blik.plot(frameVec, blink2)
plt.show()
