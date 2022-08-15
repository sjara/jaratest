#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to load and visualize pupil size

Created on Mon Mar 21 11:53:29 2022

@author: dannybrown
"""

## Import data
import numpy as np
import matplotlib.pyplot as plt

# Load file with pupil data
proc = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc.npy', allow_pickle=True).item()
pupil = proc['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']
light = proc['blink'][0]
run = proc['running'][0] # outputs the dx, dy offsets between frames by registering frame N to frame
# N-1. If the movement is larger than half the frame size, outputs NaN.
running_sum = np.absolute(run[:,0]) + np.absolute(run[:,1]) # CHANGE THIS TO BE VECTOR

# Load file with whisker data
proc2 = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc_whisk.npy', allow_pickle=True).item()
whisk = proc2['running'][0]
whisking_sum = np.absolute(whisk[:,0]) + np.absolute(whisk[:,1]) # CHANGE THIS TO BE VECTOR
whisking_sum2 = np.sqrt(np.square(whisk[:,0]) + np.square(whisk[:,1]))
groom = proc2['blink'][1]
light2 = proc2['blink'][0]


## Plot the pupil area
plt.plot(pArea)
plt.xlabel('Frame')
plt.ylabel('Pupil Size [A.U.]')
plt.title('Pupil Area',fontweight="bold")

plt.figure()
plt.plot(running_sum)
plt.xlabel('Frame')
plt.ylabel('Abs Offset (Dx+Dy) btwn Frames')
plt.title('Running',fontweight="bold")


plt.figure()
plt.plot(light)
plt.xlabel('Frame')
plt.ylabel('Light')
plt.title('Synchronization Light',fontweight="bold")

plt.figure()
plt.plot(groom)
plt.xlabel('Frame')
plt.ylabel('Light')
plt.title('Grooming',fontweight="bold")

plt.figure()
plt.plot(whisking_sum)
plt.xlabel('Frame')
plt.ylabel('Light')
plt.title('Whisking',fontweight="bold")

plt.figure()
plt.plot(pArea)
plt.plot(running_sum)
plt.plot(whisking_sum)
plt.title('Pupil Area (blue), Running (orange), and Whisking (Green)',fontweight="bold")

plt.figure()
plt.plot(whisking_sum)
plt.plot(whisking_sum2)



















