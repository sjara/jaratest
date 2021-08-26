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



nframes = len(pArea) # Contains length of pArea variable.
frameVec = np.arange(0, nframes, 1) # Vector of the total frames from the video.
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video 




min_value_timeVec = np.amin(timeVec) # Minimum value of the variable timeVec_pArea. Added for precision
max_value_timeVec = np.amax(timeVec) # Maximum value of the variable timeVec_pArea. Made to prevent the plotting of space without data in the plot
inferior_limit_y_axis = np.amin(pArea) # Defines the min value for the y axis
superior_limit_y_axis = pArea[nframes - 6] # Defines max value for the y axis. The 6 corresponds to the last 6 elements of the array. Still trying to find a way to not hard-code it.

# Note: the last 6 elements in pArea allowed for the plot to create an "infinite" line in the y axis. Thus, it doesn't allow the user to properly analyze the pupil data.  



fig, (pupil_axis, blink_axis) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil_axis.set(title = 'Chad045, 2020-10-30', ylabel = 'Pupil Area')
plt.setp((pupil_axis, blink_axis), xticks = (np.arange(0, 35, 1))) #Sets up number of ticks in both plots
pupil_axis.plot(timeVec, pArea)
pupil_axis.set_xlim([min_value_timeVec, max_value_timeVec])
pupil_axis.set_ylim([inferior_limit_y_axis, superior_limit_y_axis])
pupil_axis.grid(b = True)
blink_axis.set(xlabel = 'Time (s)', ylabel = 'on/off')
blink_axis.plot(timeVec, blink2)
blink_axis.set_xlim([min_value_timeVec, max_value_timeVec])
blink_axis.grid(b = True)
plt.show()



#Important for user: in case that you have different amount of frames or time or anything between the pupil and the sync signal, make sure to create a variable for each one of them
