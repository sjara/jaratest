import tifffile
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import traceback
from scipy.signal import detrend
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis


mouse_name = 'wifi008'
date = '20241219'#First session
session = '161007' #First session

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
if os.path.exists(evoked_file) and os.path.exists(baseline_file) and os.path.exists(signal_change_file) and os.path.exists(possible_freq_file) and os.path.exists(n_freq_file ):
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
    mean_interest = []

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

    np.save(evoked_file, avg_evoked_each_freq)
    np.save(baseline_file, avg_baseline_each_freq)
    np.save(signal_change_file, signal_change_each_freq)
    np.save(n_freq_file, n_freq)
    np.save(possible_freq_file, possible_freq)
    print("Processing complete. Results saved.")

    # ---- Plot the same graph using the loaded or computed data ----

plt.clf()
n_freq = int(n_freq) #When I save the images, I also save this variable.
fig = plt.gcf()
axs = fig.subplots(n_freq, 3, sharex=True, sharey=True) 
cmap = 'viridis'
p=0

for indf, freq in enumerate(possible_freq):
    if p==0:
        INTENSITY_SCALE = [-0.01, 0.011] #[-0.01, 0.05] [-0.01, 0.075]] [-0.01, 0.01]
    elif p==1:
        INTENSITY_SCALE = [-0.01, 0.028]
    elif p==2:
        INTENSITY_SCALE = [-0.01, 0.013]
    elif p==3:
        INTENSITY_SCALE = [-0.01, 0.05]
    elif p==4:
        INTENSITY_SCALE = [-0.01, 0.008]

    plt.sca(axs[indf, 0])
    plt.imshow(avg_evoked_each_freq[indf], cmap=cmap) 
    plt.colorbar()
    plt.title(f'Evoked')
    plt.ylabel(f'{freq:g} Hz')

    plt.sca(axs[indf, 1])
    plt.imshow(avg_baseline_each_freq[indf], cmap=cmap) 
    plt.colorbar()
    plt.title('Baseline')

    plt.sca(axs[indf, 2])
    plt.imshow(signal_change_each_freq[indf], cmap=cmap, vmin=INTENSITY_SCALE[0], vmax=INTENSITY_SCALE[1]) #signal_change_each_freq
    plt.colorbar()
    plt.title('Signal change: (E-B)/B')

    fig.suptitle(f"{mouse_name} / {date} / {session}", fontsize=13)
    p += 1

plt.show()