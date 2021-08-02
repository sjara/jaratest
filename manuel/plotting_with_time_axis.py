"""
Calculating the time(s) for the x axis for FaceMap plots
"""

#Python
import numpy as np
import matplotlib.pyplot as plt


proc = np.load('chad045_030_1_proc.npy', allow_pickle = True).item()
#Note: the proc.npy is the output file generated from facemap

pupil = proc['pupil'][0] # Dic                                                                                                                                                                             
pArea = pupil['area']    # numpy.array
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
pupil.plot(time_array, pAreaa)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.grid(b = True)
blink.plot(time_array, blink2_a)
plt.show()
