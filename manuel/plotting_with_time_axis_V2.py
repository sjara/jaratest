"""
Calculating the time(s) for the x axis for FaceMap plots
"""

#Python
import numpy as np
import matplotlib.pyplot as plt
#from jaratoolbox import pupilanalysis

proc = np.load('./to_compare/chad045_030_1_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap

pupil = proc['pupil'][0] # Dic
pArea = pupil['area']    # numpy.array. Contains calculation of the pupil area in each frame of the video
#pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink = proc['blink'][0] # numpy.array
blink1 = proc['blink']   # List
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting
#blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)



nframes_pArea = len(pArea) # Contains length of pArea variable. It has the total number of frames of the pupil area
nframes_blink2 = len(blink) # Contains length of blink2_a variable. It has the total number of frames of the sync signal
frameVec_pArea = np.arange(0, nframes_pArea, 1) # Vector of the total frames from the video with the size of the pupil in each frame
frameVec_blink2 = np.arange(0, nframes_blink2, 1) # Vector of the total frames from the video with the blink
framerate = 30 # frame rate of video
timeVec_pArea = (frameVec_pArea * 1)/framerate # Time Vector to calculate the length of the video 
#print(timeVec)
timeVec_blink2 = (frameVec_blink2 * 1)/framerate # Time Vector to calculate the length of the video 
#print(timeVec)
fig, (pupil_axis, blink_axis) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil_axis.set(title = 'Animal name and session date', ylabel = 'Pupil Area')
plt.setp((pupil_axis, blink_axis), xticks = (np.arange(0, 35, 1))) #Sets up number of ticks in both plots
pupil_axis.plot(timeVec_pArea, pArea)
pupil_axis.set_xlim([0, nframes_pArea-964.7])
pupil_axis.set_ylim([700, 1500])
pupil_axis.grid(b = True)
blink_axis.set(xlabel = 'Time (s)', ylabel = 'on/off')
blink_axis.plot(timeVec_blink2, blink2)
blink_axis.set_xlim([0, nframes_blink2-964.7])
blink_axis.grid(b = True)
plt.show()

#Important for user: the frameVec_pArea and frameVec_blink2 are the same, as well as timeVec_pArea and timeVec_blink2 are the same in this exercise, but it's good to keep in mind that the frames in the pupil area might not be the same as the ones in the sync signal in other videos, so play safe and create a variable for each one of them. In the particular case of the timeVec, one can use either the pArea or blink2 variables to calculate it (therefore, it can be called just "timeVec"). But again, it was done like this to raise awareness regarding the chance of the variables to have different values. 
