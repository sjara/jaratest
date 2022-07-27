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

# Load file with pupil, light, groom, & whisk data
proc = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc.npy', allow_pickle=True).item()
pupil = proc['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']
light = proc['blink'][0]
groom = proc['blink'][1]
whisk = proc['running'][0] # outputs the dx, dy offsets between frames by registering frame N to frame
# N-1. If the movement is larger than half the frame size, outputs NaN.
whisking_sum = np.sqrt(np.square(whisk[:,0]) + np.square(whisk[:,1])) # Convert to movement vector

# Load file with run data
proc2 = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc_run.npy', allow_pickle=True).item()
run = proc2['running'][0]
running_sum = np.sqrt(np.square(run[:,0]) + np.square(run[:,1])) # Convert to movement vector

# Load file with sniff data
proc3 = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc_sniff.npy', allow_pickle=True).item()
sniff = proc3['running'][0]
sniffing_sum = np.sqrt(np.square(sniff[:,0]) + np.square(sniff[:,1]))

### PLOTS
## Plot the pupil area
plt.plot(pArea, '.-')
plt.xlabel('Frame')
plt.ylabel('Pupil Size [A.U.]')
plt.title('Pupil Area',fontweight="bold")

## Plot a blink
plt.plot(pArea)
plt.xlabel('Frame')
plt.ylabel('Pupil Size [A.U.]')
plt.title('Pupil Area During a Blink',fontweight="bold")
plt.xlim((14241,14259))

## Plot running
plt.figure()
#plt.subplot(211)
plt.plot(running_sum,'.-')
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('Running',fontweight="bold")
plt.xlim((0,len(running_sum)))
plt.ylim((0,5))
plt.subplot(212)
plt.title('Running - Time-Frequency Domain',fontweight="bold")
samplingFrequency = 12
powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(running_sum, Fs=samplingFrequency)
plt.xlabel('Time Bin')
plt.ylabel('Frequency')
#plt.xlim((0,250)) # USE TO ZOOM IN TO SUBSET OF SPECTROGRAM
plt.ylim((0,5))
plt.tight_layout()
plt.show()

## Plot the synchronization light
plt.figure()
plt.plot(light)
plt.xlabel('Frame')
plt.ylabel('Light')
plt.title('Synchronization Light',fontweight="bold")

## Plot grooming
plt.figure()
plt.plot(groom)
plt.xlabel('Frame')
plt.ylabel("Grooming ROI ('Blink')")
plt.title('Grooming',fontweight="bold")

## Plot whisking
plt.figure()
plt.plot(whisking_sum)
plt.xlabel('Frame')
plt.ylabel('Value')
plt.title('Whisking',fontweight="bold")
#plt.xlim((2400,2900)) GOOD EXAMPLE OF A WHISKING BOUT

## Plot pupil, running, whisking
plt.figure()
ax1 = plt.subplot(3,1,1)
plt.plot(pArea)
ax2 = plt.subplot(3,1,2, sharex=ax1)
plt.plot(running_sum)
ax3 = plt.subplot(3,1,3, sharex=ax1)
plt.plot(groom)
plt.title('Pupil Area (blue), Running (orange), and Whisking (Green)',fontweight="bold")

## Could insert a regression of Pupil Area (y), based on running (x1), whisking (x2)


## Plot sniffing
plt.figure()
plt.plot(sniffing_sum)
plt.xlabel('Frame')
plt.ylabel('Movement')
plt.title('Sniffing',fontweight="bold")

# Plot sniffing and spectrogram
plt.subplot(211)
plt.plot(sniffing_sum)
plt.xlabel('Frame')
plt.ylabel('Movement')
plt.title('Sniffing (Movement at Tip of Nose)',fontweight="bold")
plt.xlim((0,len(sniffing_sum)))
plt.subplot(212)
plt.title('Sniffing - Time-Frequency Domain',fontweight="bold")
samplingFrequency = 12
powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(sniffing_sum, Fs=samplingFrequency)
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.ylim((0,5))
plt.tight_layout()
plt.show()

# Plot a 'sniffing' session, with regular sniffing/breathing patterns.
plt.figure()
plt.plot(sniffing_sum)
plt.xlabel('Frame')
plt.ylabel('Movement')
plt.title('Sniffing (Movement at Tip of Nose)',fontweight="bold")
plt.xlim((4320,4500))
plt.ylim((0,0.01)) # EVEN WHEN YOU ZOOM ALL THE WAY IN, CAN'T DETECT BREATHING

## Show a specific frame
filename = '/data/videos/feat007/feat007_am_tuning_curve_20220321_02.mp4'
frame_no=np.where(light == max(light))[0][0]
import numpy as np
import cv2
cap = cv2.VideoCapture(filename) #video_name is the video being called
cap.set(1,frame_no); # Where frame_no is the frame you want
ret, frame = cap.read() # Read the frame    
plt.imshow(frame)





## Attempting to use jaratoolbox to access video frames:
#import cv2
#from jaratoolbox import videoanalysis
#videoanalysis.Video('/data/videos/feat007/feat007_am_tuning_curve_20220321_02.mp4')
#
## To locate the maximum value of a variable:
#np.where(light == max(light))[0][0]

# To apply ROIs to other files:
#from jaratoolbox import pupilanalysis
#pupilanalysis.copy_facemap_roi('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc_whisk.npy', '/data/videos/feat007/feat007_am_tuning_curve_20220321_01.mp4')

# If you want to apply a moving average:
#def movingaverage(interval, window_size):
#    window= np.ones(int(window_size))/float(window_size)
#    return np.convolve(interval, window, 'same')
