"""
This is a test to share axis for Facemap output data and for plotting
"""
import numpy as np
import matplotlib.pyplot as plt

proc = np.load('your_video_proc.npy', allow_pickle = True).item()

pupil = proc['pupil'][0] # dtype = Dic
pArea = pupil['area']    # dtype = numpy.array
pArea1 = pupil[:-5]    # Eliminates last 5 elements within arrays: fixes infite line length in plot (X axis)
blink = proc['blink'][0] # dtype = numpy.array
blink1 = proc['blink']   # dtype = List
blink2 = np.array(blink).T # Creates transpose matrix of blink. Necessary for plotting
blink2_2 = blink2[:-5]  # Eliminates last 5 elements within arrays: fixes infite line length in plot (Y axis)

fig, (pupil, blink) = plt.subplots(2, 1, sharex = True, sharey = False, constrained_layout = True) #Tried changing it to fig, (pArea, blink1). Didn't work

pupil.set(title = 'Pupil Area Vs Time', ylabel = 'Area', xlabel = 'Time (s)')
pupil.plot(pArea)
blink.set(title = 'Sync Vs Time', ylabel = 'on/off', xlabel = 'Time (s)')
blink.plot(blink2)
plt.show()
