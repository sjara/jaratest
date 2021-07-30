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

proc2 = np.load('', allow_pickle = True).item()

pupil1 = proc2['pupil'][0] # Dic
pArea1 = pupil1['area']    # numpy.array
pAreab = pArea1[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink1 = proc2['blink'][0] # numpy.array
blink11 = proc2['blink']   # List
blink21 = np.array(blink1).T # Creates transpose matrix of blink. Necessary for plotting
blink2_b = blink21[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAreab.shape)
print(blink2_b.shape)

framerate2 = 30 # frame rate of video
total_frames2 = 998 # from video
time2 = (total_frames2 * 1)/framerate # Time to reproduce 998 frames
#print(time2)
step_number2 = time2/993
time_array2 = np.arange(0, time2, step_number2) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array2)


fig2, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array2, pAreab)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array2, blink2_b)
blink.grid(b = True)
plt.show()
                                                          
proc3 = np.load('', allow_pickle = True).item()
  
pupil2 = proc3['pupil'][0] # Dic
pArea2 = pupil2['area']    # numpy.array
pAreac = pArea2[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink2 = proc3['blink'][0] # numpy.array
blink12 = proc3['blink']   # List
blink22 = np.array(blink2).T # Creates transpose matrix of blink. Necessary for plotting
blink2_c = blink22[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAreac.shape)
print(blink2_c.shape)

framerate3 = 30 # frame rate of video
total_frames3 = 998 # from video
time3 = (total_frames3 * 1)/framerate # Time to reproduce 998 frames
#print(time3)
step_number3 = time3/993
time_array3 = np.arange(0, time3, step_number3) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array3)

fig3, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array3, pAreac)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array3, blink2_c)
blink.grid(b = True)
plt.show()
                                                                                                                                   
proc4 = np.load('', allow_pickle = True).item()
  
pupil3 = proc4['pupil'][0] # Dic
pArea3 = pupil3['area']    # numpy.array
pAread = pArea3[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink3 = proc4['blink'][0] # numpy.array
blink13 = proc4['blink']   # List
blink23 = np.array(blink3).T # Creates transpose matrix of blink. Necessary for plotting
blink2_d = blink23[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAread.shape)
print(blink2_d.shape)

framerate4 = 30 # frame rate of video
total_frames4 = 998 # from video
time4 = (total_frames4 * 1)/framerate4 # Time to reproduce 998 frames
#print(time4)
step_number4 = time4/993
time_array4 = np.arange(0, time4, step_number4) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array4)


fig4, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots 
pupil.plot(time_array4, pAread)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array4, blink2_d)
blink.grid(b = True)
plt.show()

proc5 = np.load('', allow_pickle = True).item()

pupil4 = proc5['pupil'][0] # Dic
pArea4 = pupil4['area']    # numpy.array
pAreae = pArea4[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink4 = proc5['blink'][0] # numpy.array
blink14 = proc5['blink']   # List
blink24 = np.array(blink4).T # Creates transpose matrix of blink. Necessary for plotting
blink2_e = blink24[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAreae.shape)
print(blink2_e.shape)

framerate5 = 30 # frame rate of video
total_frames5 = 998 # from video
time5 = (total_frames5 * 1)/framerate5 # Time to reproduce 998 frames
#print(time5)
step_number5 = time5/993
time_array5 = np.arange(0, time5, step_number5) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array5)


fig5, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array5, pAreae)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array5, blink2_e)
blink.grid(b = True)
plt.show()

proc6 = np.load('', allow_pickle = True).item()

pupil5 = proc6['pupil'][0] # Dic
pArea5 = pupil5['area']    # numpy.array
pAreaf = pArea5[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink5 = proc6['blink'][0] # numpy.array
blink15 = proc6['blink']   # List
blink25 = np.array(blink5).T # Creates transpose matrix of blink. Necessary for plotting
blink2_f = blink25[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAreaf.shape)
print(blink2_f.shape)

framerate6 = 30 # frame rate of video
total_frames6 = 998 # from video
time6 = (total_frames6 * 1)/framerate6 # Time to reproduce 998 frames
#print(time6)
step_number6 = time6/993
time_array6 = np.arange(0, time6, step_number6) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array6)


fig6, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array6, pAreaf)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array6, blink2_f)
blink.grid(b = True)
plt.show()

proc7 = np.load('', allow_pickle = True).item()

pupil6 = proc7['pupil'][0] # Dic
pArea6 = pupil6['area']    # numpy.array
pAreag = pArea6[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink6 = proc7['blink'][0] # numpy.array
blink16 = proc7['blink']   # List
blink26 = np.array(blink6).T # Creates transpose matrix of blink. Necessary for plotting
blink2_g = blink26[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAreag.shape)
print(blink2_g.shape)

framerate7 = 30 # frame rate of video
total_frames7 = 998 # from video
time7 = (total_frames7 * 1)/framerate7 # Time to reproduce 998 frames
#print(time7)
step_number7 = time7/993
time_array7 = np.arange(0, time7, step_number7) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array7)


fig7, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array7, pAreag)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array7, blink2_g)
blink.grid(b = True)
plt.show()

proc8 = np.load('', allow_pickle = True).item()

pupil7 = proc8['pupil'][0] # Dic
pArea7 = pupil7['area']    # numpy.array
pAreah = pArea7[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (X axis)
blink7 = proc8['blink'][0] # numpy.array
blink17 = proc8['blink']   # List
blink27 = np.array(blink7).T # Creates transpose matrix of blink. Necessary for plotting
blink2_h = blink27[:-5] # Elimination of last 5 elements of array. Fixes infinite line length (Y axis)

print(pAreah.shape)
print(blink2_h.shape)

framerate8 = 30 # frame rate of video
total_frames8 = 998 # from video
time8 = (total_frames8 * 1)/framerate8 # Time to reproduce 998 frames
#print(time8)
step_number8 = time8/993
time_array8 = np.arange(0, time8, step_number8) #step_number shows the required numbers regarding the time, to match the number of rows in the 1D array of pAreaa and blink2_a so it can be plotted.
#print(time_array8)

fig8, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True)
pupil.set(title = 'Animal name and session date', ylabel = 'Pupil Area', xlabel = 'Time(s)')
plt.setp((pupil, blink), xticks = (np.arange(0, 35, 1))) #Set ups number of ticks in both plots
pupil.plot(time_array8, pAreah)
pupil.grid(b = True)
blink.set(title = 'Animal name and session date', ylabel = 'on/off', xlabel = 'Time(s)')
blink.plot(time_array8, blink2_h)
blink.grid(b = True)
plt.show()
