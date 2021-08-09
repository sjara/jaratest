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
timeVec_pArea = (frameVec_pArea * 1)/framerate # Time Vector to calculate the length of the video 
timeVec_blink2 = (frameVec_blink2 * 1)/framerate # Time Vector to calculate the length of the video 



min_value_timeVec_pArea = np.amin(timeVec_pArea) # Minimum value of the variable timeVec_pArea. Added for precision
max_value_timeVec_pArea = np.amax(timeVec_pArea) # Maximum value of the variable timeVec_pArea. Made to prevent the plotting of space without data in the plot
min_value_timeVec_blink2 = np.amin(timeVec_blink2) # Minimum value of the variable timeVec_blink2. Added for precision for plotting and prevent using plot labels without data
max_value_timeVec_blink2 = np.amax(timeVec_blink2) # Maximum value of the variable timeVec_blink2. Made to prevent the plotting of space without data in the plot
inferior_limit_y_axis = np.amin(pArea) # Defines the min value for the y axis
superior_limit_y_axis = pArea[nframes_pArea - 6] # Defines max value for the y axis. The 6 corresponds to the last 6 elements of the array. Still trying to find a way to not hard-code it.

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



#Important for user: the frameVec_pArea and frameVec_blink2 are the same, as well as timeVec_pArea and timeVec_blink2 and so on with the other variables with the pArea and blink2 suffixes in this exercise, but it's good to keep in mind that the frames in the pupil area might not be the same as the ones in the sync signal in other videos, so play safe and create a variable for each one of them. In the particular case of the timeVec, one can use either the pArea or blink2 variables to calculate it (therefore, it can be called just "timeVec"). But again, it was done like this to raise awareness regarding the chance of the variables to have different values. Same logic applies to the rest of the variables with the pArea and blink2 suffixes.
