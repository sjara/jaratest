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
proc = np.load('/data/videos/feat007/test/feat007_am_tuning_curve_20220321_02_proc_new.npy', allow_pickle=True).item()
pupil = proc['pupil'][0]  # A dict inside a 1-item list, so you need to get the first element
pArea = pupil['area']
light = proc['blink'][0]
groom = proc['blink'][1]
blink = proc['blink'][2]
whisk = proc['running'][0] # outputs the dx, dy offsets between frames by registering frame N to frame
# N-1. If the movement is larger than half the frame size, outputs NaN.
whisking_sum = np.sqrt(np.square(whisk[:,0]) + np.square(whisk[:,1])) # Convert to movement vector
run = proc['running'][1]
running_sum = np.sqrt(np.square(run[:,0]) + np.square(run[:,1])) # Convert to movement vector

# Load file with run data
#proc2 = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc_run.npy', allow_pickle=True).item()
#run = proc2['running'][0]
#running_sum = np.sqrt(np.square(run[:,0]) + np.square(run[:,1])) # Convert to movement vector
#
## Load file with sniff data
#proc3 = np.load('/data/videos/feat007_processed/feat007_am_tuning_curve_20220321_02_proc_sniff.npy', allow_pickle=True).item()
#sniff = proc3['running'][0]
#sniffing_sum = np.sqrt(np.square(sniff[:,0]) + np.square(sniff[:,1]))



### CALCULATIONS AND TRACES

## Grooming (Works well)
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


## Whisking (Works Well)
avgwidth_whisking = 5
whisking_sum_mvgavg = moving_average(whisking_sum,avgwidth_whisking) # Use moving average to combat repeated video frames
# Plot whisking
plt.figure()
plt.plot(whisking_sum, color='0.7', label='Sum of Movement Vector - Raw')
plt.plot(whisking_sum_mvgavg, label='Smoothed via Moving Average')
plt.xlabel('Frame')
plt.ylabel('Offset Vector Between Frames')
plt.title('Whisking',fontweight="bold")
plt.xlim((0,len(whisking_sum)))
plt.ylim((0,np.max(whisking_sum)))
#plt.xlim((24825,25150)) #GOOD EXAMPLE OF A WHISKING BOUT
plt.legend(loc="upper left")
plt.tight_layout()


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
pArea[pArea<5]=np.nan # (REVIEW: this is to take out the repeated low values.  Hardcoded - a bit hacky.)
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


## Plot Running (Works Well)
plt.figure()
plt.plot(running_sum, color='0.7', label='Sum of Movement Vector - Raw')
plt.plot(moving_average(running_sum,5),color='r', label='Smoothed via Moving Average')
plt.legend(loc="upper left")
plt.xlabel('Frame')
plt.ylabel('Offset Vector between Frames')
plt.title('Running',fontweight="bold")
plt.xlim((0,len(running_sum)))


## Plot the synchronization light (Works Well)
plt.figure()
plt.plot(light)
plt.xlabel('Frame')
plt.ylabel('Light')
plt.title('Synchronization Light',fontweight="bold")


## Blinking (May 10th)
plt.figure()
plt.plot(blink)
input = plt.ginput(1)[0][1]


# To apply ROIs to other files:
from jaratoolbox import pupilanalysis
pupilanalysis.copy_facemap_roi('/data/videos/feat007/feat007_am_tuning_curve_20220321_02_proc.npy', '/data/videos/feat007/test.mp4')






#### Play a video from a start point - q to quit, k to skip to next frame
#def play_video(folder,filename,frame_start):
#    # load video capture from file
#    video = cv2.VideoCapture(os.path.join(folder,filename))
#    # window name and size
#    cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
#    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
#    while video.isOpened():
#        # Read video capture
#        ret, frame = cap.read()
#        # Display each frame
#        cv2.imshow("video",frame)
#        # show one frame at a time
#        key = cv2.waitKey(0)
#        while key not in [ord('q'), ord('k')]:
#            key = cv2.waitKey(0)
#        # Quit when 'q' is pressed
#        if key == ord('q'):
#            break
#
#    # Release capture object
#    video.release()
#    # Exit and distroy all windows
#    cv2.destroyAllWindows()
#
#play_video("/data/videos/feat007","feat007_am_tuning_curve_20220321_02.mp4",61)
#
#
#
#
#### Save a series of video frames
#frame_start = 15000
#frame_end = frame_start+5
#filepath_load = "/data/videos/feat007/feat007_am_tuning_curve_20220321_02.mp4"
#filepath_save = "/data/videos/feat007/test"
#os.chdir(filepath_save)
#cap = cv2.VideoCapture(filepath_load)
#i = 0
#cap.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
#while(cap.isOpened()):
#    ret, frame = cap.read()
#    # This condition prevents from infinite looping in case video ends.
#    if ret == False:
#        break
#    if i==frame_end - frame_start:
#        break
#    # Save Frame by Frame into disk using imwrite method
#    cv2.imwrite('Frame'+str(frame_start+i)+'.jpg', frame)
#    i += 1
#cap.release()
#cv2.destroyAllWindows()
#
#
#
### CONTINUous
#
#
### Plot pupil, running, whisking
#plt.figure()
#ax1 = plt.subplot(3,1,1)
#plt.plot(pArea)
#ax2 = plt.subplot(3,1,2, sharex=ax1)
#plt.plot(running_sum)
#ax3 = plt.subplot(3,1,3, sharex=ax1)
#plt.plot(groom)
#plt.title('Pupil Area (blue), Running (orange), and Grooming (Green)',fontweight="bold")
#
### Could insert a regression of Pupil Area (y), based on running (x1), whisking (x2)
#
#
### Show a specific frame
#filename = '/data/videos/feat007/feat007_am_tuning_curve_20220321_02.mp4'
#frame_no=np.where(light == max(light))[0][0]
#import numpy as np
#import cv2
#cap = cv2.VideoCapture(filename) #video_name is the video being called
#cap.set(1,frame_no); # Where frame_no is the frame you want
#ret, frame = cap.read() # Read the frame    
#plt.imshow(frame)



## Plot sniffing
#plt.figure()
#plt.plot(sniffing_sum)
#plt.xlabel('Frame')
#plt.ylabel('Movement')
#plt.title('Sniffing',fontweight="bold")
#
## Plot sniffing and spectrogram
#plt.subplot(211)
#plt.plot(sniffing_sum)
#plt.xlabel('Frame')
#plt.ylabel('Movement')
#plt.title('Sniffing (Movement at Tip of Nose)',fontweight="bold")
#plt.xlim((0,len(sniffing_sum)))
#plt.subplot(212)
#plt.title('Sniffing - Time-Frequency Domain',fontweight="bold")
#samplingFrequency = 12
#powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(sniffing_sum, Fs=samplingFrequency)
#plt.xlabel('Time')
#plt.ylabel('Frequency')
#plt.ylim((0,5))
#plt.tight_layout()
#plt.show()

# Plot a 'sniffing' session, with regular sniffing/breathing patterns.
#plt.figure()
#plt.plot(sniffing_sum)
#plt.xlabel('Frame')
#plt.ylabel('Movement')
#plt.title('Sniffing (Movement at Tip of Nose)',fontweight="bold")
#plt.xlim((4320,4500))
#plt.ylim((0,0.01)) # EVEN WHEN YOU ZOOM ALL THE WAY IN, CAN'T DETECT BREATHING

## Plot Running with Time-Frequency Analysis (Failed)
#plt.figure()
#plt.subplot(211)
#plt.plot(running_sum)
#plt.xlabel('Frame')
#plt.ylabel('Offset Vector between Frames')
#plt.title('Running',fontweight="bold")
#plt.xlim((0,len(running_sum)))
#plt.ylim((0,5))
#plt.subplot(212)
#plt.title('Running - Time-Frequency Domain',fontweight="bold")
#samplingFrequency = 12
#powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(running_sum, Fs=samplingFrequency)
#plt.xlabel('Time Bin')
#plt.ylabel('Frequency')
#plt.xlim((0,250)) # USE TO ZOOM IN TO SUBSET OF SPECTROGRAM
#plt.ylim((0,5))
#plt.tight_layout()
#plt.show()


## Attempting to use jaratoolbox to access video frames:
#import cv2
#from jaratoolbox import videoanalysis
#videoanalysis.Video('/data/videos/feat007/feat007_am_tuning_curve_20220321_02.mp4')
#
## To locate the maximum value of a variable:
#np.where(light == max(light))[0][0]



## First Version of Blinks Output and Boolean
#plt.figure()
#ax1 = plt.subplot(2,1,1)
#plt.title('Blinks',fontweight="bold")
#plt.plot(blink)
#plt.xlabel('Frame')
#plt.ylabel('Blink Trace')
#plt.axhline(y=np.mean(blink), color='b', linestyle='-')
## Define a stddev-based parameter, to define a grooming cutoff.
#blinks_param = -1.2 # This is the number of std deviations from the mean to place the cutoff.
#threshold_blinks = np.mean(blink)+(blinks_param * np.std(blink))
#plt.axhline(y=threshold_blinks, color='r', linestyle='-')
##plt.xlim((21440, 21520))
## Create boolean for blinks
#blinks_bool=(blink<threshold_blinks)
#ax2 = plt.subplot(2,1,2, sharex=ax1)
#plt.plot(blinks_bool)
#
#
### Blinks Revision: Incorporate Moving Average (last values impute the last calucated avg)
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
