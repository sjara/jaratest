"""
Show the changes of widefield signal over time.
"""

import tifffile
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import traceback
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

#SAVE_DATA = 1
#if SAVE_DATA:
    
date = '20250311'
session = '111936'
frames_filename = '/data/widefield/wifi008/' + date + '/wifi008_' + date + '_' + session + '_LG.tif'
n_frames_files = 1
mouse_name = frames_filename[16:23]
timestamps_filename = '/data/widefield/wifi008/' + date + '/wifi008_timestamps_' + date + '_' + session + '.npz'
stimulus_filename = '/data/widefield/wifi008/wifi008_am_tuning_curve_' + date + '_' + session + '.h5'
#

INTENSITY_SCALE = [-0.01, 0.05]

# Define directory for cached results
save_dir = f"/data/widefield/processed_data/{mouse_name}/{date}/{session}"
os.makedirs(save_dir, exist_ok=True)

# Filenames for cached data
evoked_file = os.path.join(save_dir, "evoked.npy")
baseline_file = os.path.join(save_dir, "baseline.npy")
signal_change_file = os.path.join(save_dir, "signal_change.npy")
possible_freq_file = os.path.join(save_dir, "possible_freq.npy")
n_freq_file = os.path.join(save_dir, "n_freq.npy")
dynamics = os.path.join(save_dir, "dynamics.npy")

# Check if data is already processed
if 0: #os.path.exists(evoked_file) and os.path.exists(baseline_file) and os.path.exists(signal_change_file) and os.path.exists(possible_freq_file) and os.path.exists(n_freq_file ):
    avg_evoked_each_freq = np.load(evoked_file)
    avg_baseline_each_freq = np.load(baseline_file)
    signal_change_each_freq = np.load(signal_change_file)
    possible_freq = np.load(possible_freq_file)
    n_freq = np.load(n_freq_file)
    print("Loaded precomputed data.")

else:
    print("Processing data...")

    # -- Create list of TIFF files --
    frames_filenames = [frames_filename]
    suffix = '_@{0:04g}'
    for indf in range(1, n_frames_files):
        new_suffix = suffix.format(indf)
        new_filename = frames_filename.replace('.tif', new_suffix+'.tif')
        frames_filenames.append(new_filename)

    # -- Load TIFF files --    
    frames = None  # A numpy array to store all frames
    for indf, filename in enumerate(frames_filenames):    
        with tifffile.TiffFile(filename) as tif:
            chunk = tif.asarray()
            # image = tif.asarray()[0] #If I want to see a single image 
            axes = tif.series[0].axes
            if frames is None:
                frames = chunk
            else:
                frames = np.concatenate((frames, chunk), axis=0)

    timestamps = np.load(timestamps_filename)
    sound_onset = timestamps['ts_sound_rising']
    sound_offset = timestamps['ts_sound_falling']
    ts_frames = timestamps['ts_trigger_rising']

    # -- Load stimulus data --
    bdata = loadbehavior.BehaviorData(stimulus_filename)
    n_trials = min(len(bdata['currentFreq']), len(sound_onset))
    current_freq = bdata['currentFreq'][:n_trials]
    possible_freq = np.unique(current_freq)
    n_freq = len(possible_freq)
    trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

    # -- Fix the length of sound onsets to be the same as the number of bdata trials --
    sound_onset = sound_onset[:n_trials]

    # -- Load imaging data --
    with tifffile.TiffFile(frames_filename) as tif:
        frames = tif.asarray()
        axes = tif.series[0].axes
        
    # -- Estimate average evoked image --
    sound_duration = np.mean(sound_offset[:len(sound_onset)]-sound_onset)
    frame_rate = 1/np.mean(np.diff(ts_frames))
    sound_duration_in_frames = int(round(sound_duration*frame_rate))
    # Find frames corresponding to evoked period
    frame_after_onset = np.searchsorted(ts_frames, sound_onset, side='left')

    '''
    #Obtaining the indices of images after a particular sound
    interest_trigger = 50   #The one that I'll use to see the images
    onset_time = sound_onset[interest_trigger]   #Find it in the list
    closer_frame = np.searchsorted(ts_frames, onset_time, side='left')  #Find the frame after the onset sound    
    before_onset = 1   #Quantity of images before the sound onset
    after_onset = sound_duration_in_frames #Quantity of images after the sound onset
    image_indices = np.arange(closer_frame - before_onset, closer_frame + after_onset) #Indices of wanted frames
    '''
    
    evoked_frames_each_freq = []
    avg_evoked_each_freq = []
    avg_baseline_each_freq = []
    signal_change_each_freq = []
    
    for indf, freq in enumerate(possible_freq):
        frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, indf]] #Get the frames after the sound onset
        evoked_frames_this_freq = np.tile(frame_after_onset_this_freq, (sound_duration_in_frames, 1)) #Repeat the array N times
        evoked_frames_this_freq += np.arange(sound_duration_in_frames)[:,None] #Finally: the 10 indicesoftheframesforeach sound
        evoked_frames_this_freq = np.sort(evoked_frames_this_freq.ravel()) # Convert to 1 array only ordered
        evoked_frames_each_freq.append(evoked_frames_this_freq)
        
        #If the video is divided into 2 recordings I have to adjust the # of frames
        final_frames = np.searchsorted(evoked_frames_this_freq,len(frames))
        avg_evoked_this_freq = np.mean(frames[evoked_frames_this_freq[0:final_frames]], axis=0) #Frames during the sound 
        
        baseline_frames_this_freq = evoked_frames_this_freq[0:final_frames] - sound_duration_in_frames#Framesbeforethesoundonset10
        avg_baseline_this_freq = np.mean(frames[baseline_frames_this_freq], axis=0)

        # -- Estimate change in fluorescence --
        signal_change = (avg_evoked_this_freq-avg_baseline_this_freq)/avg_baseline_this_freq


        avg_evoked_each_freq.append(avg_evoked_this_freq)
        avg_baseline_each_freq.append(avg_baseline_this_freq)
        signal_change_each_freq.append(signal_change)

    # Convert lists to arrays and save them
    avg_evoked_each_freq = np.array(avg_evoked_each_freq)
    avg_baseline_each_freq = np.array(avg_baseline_each_freq)
    signal_change_each_freq = np.array(signal_change_each_freq)
    n_freq = np.array(n_freq)
    possible_freq = np.array(possible_freq)
