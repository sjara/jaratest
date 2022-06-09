#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to load and visualize mouse behavior / physiology

Created on Mon Mar 21 11:53:29 2022

@author: dannybrown
"""

### FUNCTIONS, IMPORTS
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

### LOADING THE DATA
# Load file with pupil, light, groom, & whisk data
proc = np.load('/data/videos/feat007/test/feat007_am_tuning_curve_20220310_01_proc.npy', allow_pickle=True).item()
pupil = proc['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']
light = proc['blink'][0]
groom = proc['blink'][1]
blink_test = proc['blink'][2]
run = proc['running'][0]
running_sum = np.sqrt(np.square(run[:,0]) + np.square(run[:,1])) # Convert to movement vector

### CALCULATIONS AND TRACES

## Grooming
# Define a stddev-based parameter to define a grooming cutoff.
grooming_param = -.2 # This is the number of std deviations from the mean to place the cutoff.
threshold_grooming = np.mean(groom)+(grooming_param * np.std(groom))
avgwidth_grooming = 50  # The moving average of 50 produces best resolution for this behavior.
grooming_bool=(moving_average(groom,avgwidth_grooming)<threshold_grooming) # Boolean = 1 when moving average crosses threshold; else 0.
# Plot grooming
plt.figure()
ax1 = plt.subplot(2,1,1)
plt.plot(groom, color='0.7', label='Sum of Movement Vector - Raw')
plt.plot(moving_average(groom,avgwidth_grooming), label='Smoothed via Moving Average')
plt.xlabel('Frame')
plt.ylabel("Grooming ROI ('Blink')")
plt.title('Grooming',fontweight="bold")
plt.xlim((0,len(groom)))
#plt.xlim((9500,12500)) # Area where I determined how to place threshold
plt.axhline(y=np.mean(groom), color='b', linestyle='-', label='mean of groom')
plt.axhline(y=threshold_grooming, color='r', linestyle='-', label = 'boolean threshold')
plt.legend(loc="lower right")
# Create and Plot the boolean operator
ax2 = plt.subplot(2,1,2, sharex=ax1)
plt.plot(grooming_bool)
plt.title('Boolean',fontweight="bold")
plt.tight_layout()


## Whisking
#avgwidth_whisking = 5
#whisking_sum_mvgavg = moving_average(whisking_sum,avgwidth_whisking) # Use moving average to combat repeated video frames
## Plot whisking
#plt.figure()
#plt.plot(whisking_sum, color='0.7', label='Sum of Movement Vector - Raw')
#plt.plot(whisking_sum_mvgavg, label='Smoothed via Moving Average')
#plt.xlabel('Frame')
#plt.ylabel('Offset Vector Between Frames')
#plt.title('Whisking',fontweight="bold")
#plt.xlim((0,len(whisking_sum)))
#plt.ylim((0,np.max(whisking_sum)))
##plt.xlim((24825,25150)) #GOOD EXAMPLE OF A WHISKING BOUT
#plt.legend(loc="upper left")
#plt.tight_layout()


## Blinking and Pupil Size
# Blinks are identified by finding rapid changes in the pupil area:
pArea[np.isnan(pArea)] = 0.0 # Missing values for pupil area are set to 0 (and will trigger a blink).
pArea_diff = np.abs(np.diff(pArea)) # calculate the absolute change in pupil size from frame to frame.
blinks_param = 5.8   # This is the number of std deviations from the mean to place the threshold.
threshold_blinks = np.mean(pArea_diff)+(blinks_param * np.std(pArea_diff))
# Create boolean for blinks:
blinks_bool = (pArea_diff>threshold_blinks)
blinks_bool = np.hstack(((blinks_bool,blinks_bool[len(blinks_bool)-1]))) # duplicate the last value, so the blinks are aligned with video frames.
avgwidth_blinks = 15 # Anything within 15 frames of a tagged blink is also a blink.
blinks_bool = (moving_average(blinks_bool,avgwidth_blinks)>0)
# Plot blinks
plt.figure()
ax1 = plt.subplot(2,1,1)
plt.title('Diff of Pupil Area',fontweight="bold")
plt.plot(pArea_diff)
plt.xlabel('Frame')
plt.ylabel('Change in Pupil Area (absolute value)')
plt.axhline(y=np.mean(pArea_diff), color='b', linestyle='-')
plt.axhline(y=threshold_blinks, color='r', linestyle='-')
plt.xlim((0, len(pArea_diff)))
#plt.xlim((21440, 21520))
ax2 = plt.subplot(2,1,2, sharex=ax1)
plt.title('Blinks Boolean',fontweight="bold")
plt.plot(blinks_bool)
plt.tight_layout()


## Pupil Area (STILL TO DO: Impute the missing values.)
pArea[blinks_bool==True]=np.nan
pArea[pArea==0.0]=np.nan
#pArea[pArea<5]=np.nan # (NOTE: HAVE TO TAKE THIS OUT, BECAUSE SOMETIMES THE PUPIL IS VERY SMALL)
# Plot Pupil Area
plt.figure()
ax1 = plt.subplot(2,1,1)
plt.plot(pArea)
plt.xlabel('Frame')
plt.ylabel('Pupil Size [A.U.]')
plt.title('Pupil Area',fontweight="bold")
plt.xlim((0,len(pArea)))
# Highlight the blinks in the pupil trace.
for i in range(1,len(blinks_bool)):
    if blinks_bool[i]==True:
        plt.axvspan(i-1, i, color='r', alpha=0.4, lw=0)
ax2 = plt.subplot(2,1,2, sharex=ax1)
plt.title('Blinks Boolean',fontweight="bold")
plt.plot(blinks_bool)
#plt.title('Pupil Area During a Blink',fontweight="bold")
#plt.xlim((14200,14300))
plt.tight_layout()


## Plot Running
plt.figure()
plt.plot(running_sum, color='0.7', label='Sum of Movement Vector - Raw')
plt.plot(moving_average(running_sum,5),color='r', label='Smoothed via Moving Average')
plt.legend(loc="upper left")
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('Running',fontweight="bold")
plt.xlim((0,len(running_sum)))


## Plot the synchronization light
plt.figure()
plt.plot(light)
plt.xlabel('Frame')
plt.ylabel('Light')
plt.title('Synchronization Light',fontweight="bold")