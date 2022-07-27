#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to load and visualize mouse behavior / physiology

Created on Mon Mar 21 11:53:29 2022

@author: dannybrown
"""


### DATA LOADING
## Import data
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import math 

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


# Load file with pupil, light, groom, & whisk data
# NOTE: THIS FILE DOESN'T EXIST ANYMORE - YOU'LL HAVE TO MAKE A NEW ONE IF YOU WANT TO RETRY
proc = np.load('/data/videos/feat007/test/feat007_am_tuning_curve_20220321_02_proc.npy', allow_pickle=True).item()
blink1 = proc['blink'][0]
blink2 = proc['blink'][1]
blink3 = proc['blink'][2]

proc2 = np.load('/data/videos/feat007/feat007_am_tuning_curve_20220321_02_proc.npy', allow_pickle=True).item()
pupil = proc2['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']



### CALCULATIONS AND TRACES

## First Version of Blinks Output and Boolean
plt.figure()
ax1 = plt.subplot(2,4,1)
plt.title('Blinks - ROI Inside Eye Edge',fontweight="bold")
plt.plot(blink1)
plt.xlabel('Frame')
plt.ylabel('Blink Trace')
plt.axhline(y=np.mean(blink1), color='b', linestyle='-')
# Define a stddev-based parameter, to define a grooming cutoff.
blinks_param1 = -1.4 # This is the number of std deviations from the mean to place the cutoff.
threshold_blinks1 = np.mean(blink1)+(blinks_param1 * np.std(blink1))
plt.axhline(y=threshold_blinks1, color='r', linestyle='-')
#plt.xlim((21440, 21520))
# Create boolean for blinks
blinks_bool1=(blink1<threshold_blinks1)
ax2 = plt.subplot(2,4,5, sharex=ax1)
plt.plot(blinks_bool1)

## Second Version of Blinks Output and Boolean
ax3 = plt.subplot(2,4,2, sharex=ax1)
plt.title('Blinks - ROI Outside Eye Edge',fontweight="bold")
plt.plot(blink2)
plt.xlabel('Frame')
plt.ylabel('Blink Trace')
plt.axhline(y=np.mean(blink2), color='b', linestyle='-')
# Define a stddev-based parameter, to define a grooming cutoff.
blinks_param2 = -1.4 # This is the number of std deviations from the mean to place the cutoff.
threshold_blinks2 = np.mean(blink2)+(blinks_param2 * np.std(blink2))
plt.axhline(y=threshold_blinks2, color='r', linestyle='-')
#plt.xlim((21440, 21520))
# Create boolean for blinks
blinks_bool2=(blink2<threshold_blinks2)
ax2 = plt.subplot(2,4,6, sharex=ax1)
plt.plot(blinks_bool2)

## Third Version of Blinks Output and Boolean
ax3 = plt.subplot(2,4,3, sharex=ax1)
plt.title('Blinks - ROI Within Eye',fontweight="bold")
plt.plot(blink3)
plt.xlabel('Frame')
plt.ylabel('Blink Trace')
plt.axhline(y=np.mean(blink3), color='b', linestyle='-')
# Define a stddev-based parameter, to define a grooming cutoff.
blinks_param3 = -1.4 # This is the number of std deviations from the mean to place the cutoff.
threshold_blinks3 = np.mean(blink3)+(blinks_param3 * np.std(blink3))
plt.axhline(y=threshold_blinks3, color='r', linestyle='-')
#plt.xlim((21440, 21520))
# Create boolean for blinks
blinks_bool3=(blink3<threshold_blinks3)
ax2 = plt.subplot(2,4,7, sharex=ax1)
plt.plot(blinks_bool3)


## Using Pupil trace, and Boolean
ax3 = plt.subplot(2,4,4, sharex=ax1)
pArea_diff = np.abs(np.diff(pArea)) # calculate the absolute change from frame to frame.
pArea_diff[np.isnan(pArea_diff)]=np.sort(np.unique(pArea_diff))[0] # NaNs are treated like the largest blink.
#plt.figure()
#ax1 = plt.subplot(2,1,1)
plt.title('Diff of Pupil Area',fontweight="bold")
plt.plot(pArea_diff)
plt.xlabel('Frame')
plt.ylabel('Pupil Trace')
plt.axhline(y=np.mean(pArea_diff), color='b', linestyle='-')
# Define a stddev-based parameter, to define a grooming cutoff.
blinks_param4 = 5.8 # This is the number of std deviations from the mean to place the cutoff.
threshold_blinks4 = np.mean(pArea_diff)+(blinks_param4 * np.std(pArea_diff))
plt.axhline(y=threshold_blinks4, color='r', linestyle='-')
plt.xlim((0, len(pArea_diff)))
#plt.xlim((21440, 21520))
# Create boolean for blinks
blinks_bool4 = (pArea_diff>threshold_blinks4)
blinks_bool4 = np.hstack(((blinks_bool4,blinks_bool4[len(blinks_bool4)-1]))) # duplicate the first value, so the blinks are aligned with video frames.
blinks_bool4_smooth = (moving_average(blinks_bool4,7)>0) # Anything within 6 frames of a tagged blink is also a blink.
#ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2 = plt.subplot(2,4,8, sharex=ax1)
plt.plot(blinks_bool4_smooth)






### Revision: Incorporate Moving Average (last values impute the last calucated avg)
#plt.figure()
#ax1 = plt.subplot(2,1,1)
#plt.title('Blinks',fontweight="bold")
#plt.plot(blink)
#plt.xlabel('Frame')
#plt.ylabel('Blink Trace')
##plt.axhline(y=np.mean(blink), color='b', linestyle='-')
##plt.plot(moving_average(blink,100))
#width = 100
#blink_avg = moving_average(blink,width)
## Define a stddev-based parameter, to define a grooming cutoff.
#blinks_param = -0.8 # This is the number of std deviations from the mean to place the cutoff.
#threshold_blinks = blink_avg + (blinks_param * np.std(blink))
#plt.plot(threshold_blinks)
##plt.xlim((21440, 21520))
#blinks_bool=(blink<threshold_blinks)
#ax2 = plt.subplot(2,1,2, sharex=ax1)
##plt.plot(blink_avg-blink)
#plt.plot(blinks_bool)


