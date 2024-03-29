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
nframes = len(pArea)     # Contains length of pArea variable. It has the calculation of the pupil area for each frame. Each number represents a frame and defines if pupil is large or small.
frameVec = np.arange(0, nframes, 1) #Vector of the total frames from the video regarding pArea
framerate = 30 # frame rate of video
timeVec = (frameVec * 1)/framerate # Time Vector to calculate the length of the video 


print(timeVec)
print(frameVec)

fig, (pupil_axis, blink_axis) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil_axis.set_xlim([0, nframes])
#pupil_axis.set_ylim([0, 1500])
blink_axis.set_xlabel('Time (s)')
plt.show()

'''
fig, (pupil_axis, blink_axis) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil_axis.plot(timeVec, pArea)
pupil_axis.plot(frameVec, pArea)
pupil_axis.set_xlim([0, nframes-20])
pupil_axis.set_ylim([0, 1500])
blink_axis.set_xlabel('Frame')
plt.show()
'''

"""
pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink = proc['blink'][0] # numpy.array
blink1 = proc['blink']   # List
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting
blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)
#print(pAreaa.shape)
#print(blink2_a.shape)

framerate = 30 # frame rate of video
total_frames = pAreaa # In this particular case, you can use the total frames to plot, or to be more precise, the number of frames contained within the plotting values (pAreaa & blink2_a)
time = (total_frames * 1)/framerate # Time to reproduce the pAreaa & blink2_a frames. This apply only in this case, because they have the same number of frames.
#print(time)

step_number_array = time/pAreaa # Time required to reproduce each of those 993 frames from pAreaa.
step_number = step_number_array[0]
time_array = np.arange(0, time, step_number) # Time used to plot in the x axis
#print(time_array)
#print(step_number)

fig, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Sets up number of ticks in both plots
pupil.plot(plot, pAreaa)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.grid(b = True)
blink.plot(time_array, blink2_a)
plt.show()
"""
