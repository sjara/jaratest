import tifffile
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback
from scipy.signal import detrend
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis


# mouse_name = 'wifi008'
# date = '20241219'#First session
# session = '161007' #First session

# date = '20250227'
# session = '163358'

# mouse_name = 'wifi009'
# date = '20250411'
# session = '122755' 

# mouse_name = 'wifi010'
# date = '20250424'
# session = '144540' 

mouse_name = 'wifi009'
date = '20250611'
session = '114322'

frames_filename = '/data/widefield/' + mouse_name + '/' + date + '/' + mouse_name + '_' + date + '_' + session + '_LG.tif'
n_frames_files = 1
timestamps_filename = '/data/widefield/' + mouse_name + '/' + date + '/' + mouse_name + '_timestamps_' + date + '_' + session + '.npz'
stimulus_filename = '/mnt/jarahubdata/behavior/' + mouse_name + '/' + mouse_name + '_am_tuning_curve_' + date + '_' + session + '.h5'

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
if 0:#os.path.exists(evoked_file) and os.path.exists(baseline_file) and os.path.exists(signal_change_file) and os.path.exists(possible_freq_file) and os.path.exists(n_freq_file ):
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
    
    evoked_frames_each_freq = []
    avg_evoked_each_freq = []
    avg_baseline_each_freq = []
    signal_change_each_freq = []

    #plt.clf()
    #fig = plt.gcf()
    #axs = fig.subplots(n_freq, 3, sharex=True, sharey=True) 
    #cmap = 'viridis'
    #p=0
    
    evoked_images_all_trials = []
    baseline_images_all_trials = []
    z_score_maps = []

    for indf, freq in enumerate(possible_freq):
        trial_indices = np.where(trials_each_freq[:, indf])[0]
        evoked_trials = []
        baseline_trials = []

        for idx in trial_indices:
            start_frame = frame_after_onset[idx]
            end_frame = start_frame + sound_duration_in_frames

            if end_frame >= len(frames):
                continue

            # Evoked and baseline windows


            evoked = np.mean(frames[start_frame:end_frame], axis=0)
            baseline = np.mean(frames[start_frame - sound_duration_in_frames:start_frame], axis=0)

            evoked_trials.append(evoked)
            baseline_trials.append(baseline)

        evoked_trials = np.stack(evoked_trials, axis=0)  # shape: (n_trials, h, w)
        baseline_trials = np.stack(baseline_trials, axis=0)

        mu_baseline = np.mean(baseline_trials, axis=0)
        std_baseline = np.std(baseline_trials, axis=0)

        mean_evoked = np.mean(evoked_trials, axis=0)

        # Z-score map
        z_map = (mean_evoked - mu_baseline) / std_baseline
        z_score_maps.append(z_map)

        # Save averages for other plots if needed
        avg_evoked_each_freq.append(mean_evoked)
        avg_baseline_each_freq.append(mu_baseline)
        signal_change_each_freq.append((mean_evoked - mu_baseline) / mu_baseline)

    z_score_maps = np.array(z_score_maps)

    # print(f"\n=== Frequency {freq} Hz ===")
    # print(f"Total trials: {len(trial_indices)}")
    # valid_count = 0

    # for idx in trial_indices:
    #     start_frame = frame_after_onset[idx]
    #     end_frame = start_frame + sound_duration_in_frames

    #     if start_frame - sound_duration_in_frames < 0:
    #         print(f"Trial {idx}: Skipped (not enough baseline frames)")
    #         continue
    #     if end_frame >= len(frames):
    #         print(f"Trial {idx}: Skipped (end frame {end_frame} exceeds total frames {len(frames)})")
    #         continue

    #     valid_count += 1

    # print(f"Valid trials used: {valid_count}")

# Plot only Z-score maps (1 column x n_freq rows)
fig, axs = plt.subplots(n_freq, 1, figsize=(5, 3 * n_freq), sharex=True, sharey=True)  
if n_freq == 1:
    axs = [axs]  # Ensure axs is iterable when n_freq = 1

for indf, freq in enumerate(possible_freq):
    ax = axs[indf]
    im = ax.imshow(z_score_maps[indf], cmap='jet', vmin=0.1, vmax=0.8)
    ax.set_title(f'{freq:.0f} Hz — Z-score')
    ax.axis('off')
    fig.colorbar(im, ax=ax, orientation='vertical', label='Z-score')

plt.tight_layout()
plt.show()