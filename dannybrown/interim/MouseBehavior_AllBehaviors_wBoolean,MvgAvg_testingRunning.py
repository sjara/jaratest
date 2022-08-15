#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to load and visualize mouse behavior / physiology
This version was used to look at two Running ROIs placed in the same place.

Created on Mon Mar 21 11:53:29 2022

@author: dannybrown
"""


### DATA LOADING
## Import data
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

def moving_average(data, width):
    """
    Creates a moving average.

    Args:
        data (np.array): Data to calculate the moving average of.
        width (int): Width of window to use.

    Returns:
        np.array: Array of same size as data, with a moving average. 
    """
    return np.convolve(data, np.ones(width), 'same') / width
#    z = np.ones(width-1)*y[len(y)-1]
#    y = np.concatenate((y,z))


# Load file with pupil, light, groom, & whisk data
# NOTE: THIS FILE DOESN'T EXIST ANYMORE, YOU'LL HAVE TO RE-RUN IF NEEDED.
#proc = np.load('/data/videos/feat007/feat007_am_tuning_curve_20220321_02_proc.npy', allow_pickle=True).item()

#Loading two running ROIs placed in the same place.
run1 = proc['running'][0]
run2 = proc['running'][1] # outputs the dx, dy offsets between frames by registering frame N to frame
# N-1. If the movement is larger than half the frame size, outputs NaN.

running_sum1 = np.sqrt(np.square(run1[:,0]) + np.square(run1[:,1]))
running_sum2 = np.sqrt(np.square(run2[:,0]) + np.square(run2[:,1])) 


## Plot Magnitude of the movement vector
plt.figure()
ax1=plt.subplot(2,1,1)
plt.plot(running_sum1)
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('runningsum1',fontweight="bold")
plt.xlim((0,len(running_sum1)))
plt.ylim((0,np.max(running_sum1)))
ax2=plt.subplot(2,1,2, sharex=ax1, sharey=ax1)
plt.plot(running_sum2)
plt.title('runningsum2',fontweight="bold")
plt.xlim((0,len(running_sum1)))
plt.ylim((0,np.max(running_sum1)))

# Plot individual x and y components
plt.figure()
ax1=plt.subplot(2,2,1)
plt.plot(run1[:,0])
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('run1[0]',fontweight="bold")
plt.xlim((0,len(run1)))
ax2=plt.subplot(2,2,2, sharex=ax1)
plt.plot(run1[:,1])
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('run1[1]',fontweight="bold")
plt.xlim((0,len(run1)))
ax3=plt.subplot(2,2,3, sharex=ax1)
plt.plot(run2[:,0])
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('run2[0]',fontweight="bold")
plt.xlim((0,len(run1)))
ax4=plt.subplot(2,2,4, sharex=ax1)
plt.plot(run2[:,1])
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('run2[1]',fontweight="bold")
plt.xlim((0,len(run1)))

np.corrcoef(run1[:,0],run2[:,0])
np.corrcoef(run1[:,1],run2[:,1])

np.corrcoef(run1[:,0],run1[:,1])
np.corrcoef(run2[:,0],run2[:,1])

np.corrcoef(running_sum1, running_sum2)


