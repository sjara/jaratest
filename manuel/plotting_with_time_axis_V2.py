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
pArea = pupil['area']    # numpy.array
pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink = proc['blink'][0] # numpy.array
blink1 = proc['blink']   # List
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting
blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)



nframes_pAreaa = len(pAreaa) # Contains length of pArea variable. It has the calculation of the pupil area for each frame
nframes_blink2_a = len(pAreaa) # Contains length of pArea variable. It has the calculation of the pupil area for each frame
frameVec_pAreaa = np.arange(0, nframes_pAreaa, 1) # Vector of the total frames from the video
frameVec_blink2_a = np.arange(0, nframes_blink2_a, 1) # Vector of the total frames from the video
framerate = 30 # frame rate of video
timeVec = (frameVec_pAreaa * 1)/framerate # Time Vector to calculate the length of the video 
#print(timeVec)
fig, (pupil_axis, blink_axis) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil_axis.set(title = 'Animal name and session date', ylabel = 'Pupil Area')
plt.setp((pupil_axis, blink_axis), xticks = (np.arange(0, 35, 1))) #Sets up number of ticks in both plots
pupil_axis.plot(timeVec_pAreaa, pAreaa)
#pupil_axis.set_xlim([0, nframes_pAreaa])
pupil_axis.grid(b = True)
blink_axis.set(xlabel = 'Time (s)', ylabel = 'on/off')
blink_axis.plot(timeVec_blink2_a, blink2_a)
blink_axis.grid(b = True)
plt.show()
