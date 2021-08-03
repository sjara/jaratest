Python
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
print(pAreaa.shape)
#print(blink2_a.shape)

framerate = 30 # frame rate of video
total_frames = pAreaa # In this particular case, you can use the total frames to plot, or to be more precise, the number of frames contained within the plotting values (pAreaa & blink2_a)
totalfr_time = pAreaa[0]
time = (totalfr_time * 1)/framerate # Time to reproduce the pAreaa & blink2_a frames. This apply only in this case, because they have the same number of frames.
#print(time)

step_number_array = time/pAreaa # Time required to reproduce each of those 993 frames from pAreaa.
step_number = step_number_array[0]
# time_array = np.arange(0, time + 2.9, step_number) # Time used to plot in the x axis
#print(time_array)
#print(step_number)

print('step_number_array:', step_number_array.shape) #Should contain 993 elements. Time required to reproduce each of those 993 frames from pAreaa
print('step_number:', step_number.shape) #Should contain 1 element from the step_number_array array. Number that will be used to cover the frames from 0 seconds to 35 seconds, which is the length of the video
print('time:', time.shape) #Should contain 993 elements. Provides how many time is required to cover 993 frames, or the time to cover the "total frames"
print('total_frames:',total_frames.shape) #Should have 993 elements. It represents the total frames from the area of interest, which is the pArea (one should be able to do the same with blink2_a as well, but since it's a transposed matrix, results may very. Should try doing that)
print('pArea:',pArea.shape) #Should contain 998 elements. Here we haven't trimmed the 5 last elements that affect the plot. Area to plot from pupil
print('pAreaa:',pAreaa.shape) #Should contain 993 elements. Here we have the trimmed array from "pArea". We shouldn't have the last 5 elements from "pArea". Area to plot from pupil in the range of interest
print('blink:',blink.shape) #Should contain 998 elements. Here  we haven't trimmed the 5 last elements that affect the plot. Area of interest to plot
print('blink2:',blink2.shape) #Should contain same 998 elements as "blink" variable, it's just that is is transposed
print('blink2_a:',blink2_a.shape) #Should contain 993 elements. here we have the trimmed array from "blink". We shouldn't have the last 5 elements from "blink". Area to plot from blink in the range of interest

