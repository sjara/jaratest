"""
Calculating the time(s) for the x axis for FaceMap plots
"""

#Checking the frame rate of video in the terminal/command line
ffmpeg -i <your_video.mkv> # Look up for the number of "tbr". That's the frame rate

#Python
import numpy as np
import matplotlib.pyplot as plt



proc = np.load('yourvideo_proc.npy', allow_pickle = True).item()

pupil = proc['pupil'][0] # Dic                                                                                                                                                                             
pArea = pupil['area']    # numpy.array
pAreaa = pArea[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink = proc['blink'][0] # numpy.array
blink1 = proc['blink']   # List
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting
blink2_a = blink[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)
print(pAreaa.shape)
print(blink2_a.shape)

framerate = 30 # frame rate of video
total_frames = 998 # from video
time = (total_frames * 1)/framerate # Time to reproduce 998 frames
#print(time)
step_number = time/993
time_array = np.arange(0, time, step_number) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array)

fig, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array, pAreaa)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.grid(b = True)
blink.plot(time_array, blink2_a)
plt.show()
