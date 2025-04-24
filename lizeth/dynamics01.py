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
    
mouse_name = 'wifi008'
#date = '20250311'
#session = '111936' #Good calcium
#session = '114832' #Good calcium + anesthesia
#session = '120701' #Intrinsic
#session = '121856' #Intrinsic
#session = '131605' #Intrinsic
#session = '133151' #Intrinsic
#session = '142707' #Intrinsic

date = '20241219'#First session
session = '161007' #First session

#date = '20250317'
#session = '185100' #Calcium
#session = '192011' #Calcium anesthesia
#session = '193843' #IOI
#session = '195505' #IOI 3s
#session = '201040'

frames_filename = '/data/widefield/' + mouse_name + '/' + date + '/' + mouse_name + '_' + date + '_' + session + '_LG.tif'
n_frames_files = 1
timestamps_filename = '/data/widefield/' + mouse_name + '/' + date + '/' + mouse_name + '_timestamps_' + date + '_' + session + '.npz'
stimulus_filename = '/mnt/jarahubdata/behavior/wifi008/wifi008_am_tuning_curve_' + date + '_' + session + '.h5'
#stimulus_filename = '/data/widefield/' + mouse_name + '/' + mouse_name + '_am_tuning_curve_' + date + '_' + session + '.h5'
#

INTENSITY_SCALE = [-0.01, 0.05]

# Define directory for cached results
save_dir = f"/data/widefield/dynamics_data/{mouse_name}/{date}/{session}"
os.makedirs(save_dir, exist_ok=True)

# Filenames for cached data
evoked_file = os.path.join(save_dir, "evoked.npy")
baseline_file = os.path.join(save_dir, "baseline.npy")
signal_change_file = os.path.join(save_dir, "signal_change.npy")
possible_freq_file = os.path.join(save_dir, "possible_freq.npy")
n_freq_file = os.path.join(save_dir, "n_freq.npy")
mean_interest_file = os.path.join(save_dir, "mean_interest.npy")
dynamics = os.path.join(save_dir, "dynamics.npy")

# Check if data is already processed
if 0:#os.path.exists(evoked_file) and os.path.exists(baseline_file) and os.path.exists(signal_change_file) and os.path.exists(possible_freq_file) and os.path.exists(n_freq_file ) and os.path.exists(mean_interest_file):
    avg_evoked_each_freq = np.load(evoked_file)
    avg_baseline_each_freq = np.load(baseline_file)
    signal_change_each_freq = np.load(signal_change_file)
    possible_freq = np.load(possible_freq_file)
    n_freq = np.load(n_freq_file)
    mean_interest = np.load(mean_interest_file)
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
    
    evoked_frames_each_freq = []
    avg_evoked_each_freq = []
    avg_baseline_each_freq = []
    signal_change_each_freq = []
    mean_interest = []


plt.figure(figsize=(8, 5))

time_before = 1  # Seconds before sound onset 
time_after = 5  # Seconds after sound onset 

frame_rate = 20# 1 / np.mean(np.diff(ts_frames))  # Calculate frame rate
frames_before = int(time_before * frame_rate)
frames_after = int(time_after * frame_rate)

for i, freq in enumerate(possible_freq):
    frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, i]]
    
    aligned_signal = []
    time_vector = np.linspace(-time_before, time_after, frames_before + frames_after)

    for trial in frame_after_onset_this_freq: #Every trial of each frequency
        # Select frames before and after sound onset 
        selected_frames = np.arange(trial - frames_before, trial + frames_after)
        if selected_frames[-1] >= len(frames):
            continue  # Skip if exceeding the number of frames
        
        # Extract and normalize signal
        signal = np.mean(frames[selected_frames, 258:270, 255:270], axis=(1, 2)) #258:270, 255:270
        #baseline = np.mean(frames[selected_frames[:frames_before], 260:320, 240:320], axis=(1, 2))
        baseline = np.mean(signal[:frames_before])  # Average before sound onset
        signal_change = (signal - baseline) / baseline
        aligned_signal.append(signal_change)

    # Compute mean across trials
    aligned_signal = np.array(aligned_signal)
    mean_signal = np.mean(aligned_signal, axis=0)
    std_signal = np.std(aligned_signal, axis=0) / np.sqrt(len(aligned_signal))  # SEM


     # Convert lists to arrays and save them
    avg_evoked_each_freq = np.array(avg_evoked_each_freq)
    avg_baseline_each_freq = np.array(avg_baseline_each_freq)
    signal_change_each_freq = np.array(signal_change_each_freq)
    n_freq = np.array(n_freq)
    possible_freq = np.array(possible_freq)
    mean_signal = np.array(mean_signal)

    np.save(evoked_file, avg_evoked_each_freq)
    np.save(baseline_file, avg_baseline_each_freq)
    np.save(signal_change_file, signal_change_each_freq)
    np.save(n_freq_file, n_freq)
    np.save(possible_freq_file, possible_freq)
    np.save(mean_interest_file,mean_signal)
    print("Processing complete. Results saved.")
    

    # Plot
    plt.plot(time_vector, mean_signal, label=f"{freq} Hz", linewidth=2)
    plt.fill_between(time_vector, mean_signal - std_signal, mean_signal + std_signal, alpha=0.2)

plt.axvline(0, color='k', linestyle='--', label="Sound Onset")  # Mark sound onset
plt.xlabel("Time (s)")
plt.ylabel("ΔF/F (Signal Change)")
plt.title("Change in activity before and after sound presentation: " f"{mouse_name} / {date} / {session}",fontsize=14)
plt.legend()
plt.grid()
plt.show()