"""
1. Save the important variables that need to be used in other codes to generate plots

"""

import tifffile
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import traceback
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import settings

mouse_name = 'wifi008'
date = '20241219'
session = '161007' 

frames_filename = os.path.join(settings.WIDEFIELD_PATH, mouse_name, date, f'{mouse_name}_{date}_{session}_LG.tif')
n_frames_files = 1
timestamps_filename = os.path.join(settings.WIDEFIELD_PATH, mouse_name, date, f'{mouse_name}_timestamps_{date}_{session}.npz')
paradigm = 'am_tuning_curve'
stimulus_filename = loadbehavior.path_to_behavior_data(mouse_name, paradigm, f'{date}_{session}')

#Directory to save the results
save_dir = os.path.join(settings.WIDEFIELD_PROCESSED, mouse_name)
os.makedirs(save_dir, exist_ok=True)

# # Filenames for cached data
# evoked_file = os.path.join(save_dir, "evoked.npy")
# baseline_file = os.path.join(save_dir, "baseline.npy")
# signal_change_file = os.path.join(save_dir, "signal_change.npy")
# possible_freq_file = os.path.join(save_dir, "possible_freq.npy")
# n_freq_file = os.path.join(save_dir, "n_freq.npy")
# mean_interest_file = os.path.join(save_dir, "mean_interest.npy")
# dynamics = os.path.join(save_dir, "dynamics.npy")

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

evoked_frames_each_freq = []
avg_evoked_each_freq = []
avg_baseline_each_freq = []
signal_change_each_freq = []

plt.clf()
fig = plt.gcf()
axs = fig.subplots(n_freq, 3, sharex=True, sharey=True) 
cmap = 'viridis'
p=0
for indf, freq in enumerate(possible_freq):
    frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, indf]] #Get the frames after the sound onset
    evoked_frames_this_freq = np.tile(frame_after_onset_this_freq, (sound_duration_in_frames, 1))#(sound_duration_in_frames, 1)) #Repeat the array N times
    evoked_frames_this_freq += np.arange(sound_duration_in_frames)[:,None]#np.arange(sound_duration_in_frames)[:,None] #At the end we have the 10 indices of the frames for each sound
    evoked_frames_this_freq = np.sort(evoked_frames_this_freq.ravel()) # Convert to 1 array only ordered
    evoked_frames_each_freq.append(evoked_frames_this_freq)
    
    #If the video is divided into 2 recordings I have to adjust the # of frames
    final_frames = np.searchsorted(evoked_frames_this_freq,len(frames))
    avg_evoked_this_freq = np.mean(frames[evoked_frames_this_freq[0:final_frames]], axis=0) #Frames during the sound 
    
    baseline_frames_this_freq = evoked_frames_this_freq[0:final_frames] - sound_duration_in_frames #Frames before the sound onset (10)
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

# np.save(evoked_file, avg_evoked_each_freq)
# np.save(baseline_file, avg_baseline_each_freq)
# np.save(signal_change_file, signal_change_each_freq)
# np.save(n_freq_file, n_freq)
# np.save(possible_freq_file, possible_freq)

output_file = os.path.join(save_dir , f'{mouse_name}_{date}_{session}.npz')

np.savez(output_file, avg_evoked_each_freq=avg_evoked_each_freq, avg_baseline_each_freq=avg_baseline_each_freq,
         signal_change_each_freq=signal_change_each_freq, n_freq=n_freq, possible_freq=possible_freq)

print(f"Processing complete.  saved.")

'''
processed_data = np.load(output_file)
avg_evoked_each_freq = processed_data['avg_evoked_each_freq']
processed_data['avg_baseline_each_freq']
'''
