"""
Estimate the average evoked signal for each stimulus frequency from widefield data.

You need the tifffile package (I use my tiff virtual environment).

[4:46 PM] Tim Reizis
The files I am using to test this are:
D:/wifi003/20240530/wifi003_20240530_174509_tr.tif
D:/wifi003/20240530/wifi003_20240530_174509_tr@0001.tif
D:/wifi003/20240530/wifi003_20240530_174509_tr@0002.tif
wifi003_timestamps_20240530_174509.npz
wifi003_am_tuning_curve_20240530_174509a.h5
"""

import tifffile
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

# -- Load the data --
frames_filename = '/data/widefield/20240507/test000-20240507-151825.tif'
n_frames_files = 1
timestamps_filename = '/data/widefield/20240507/test000_timestamps_20240507_151825.npz'

stimulus_filename = '/data/behavior/test000/test000_am_tuning_curve_20240529-151825.h5'

INTENSITY_SCALE = [None, None]  # [-0.05, 0.1]

# -- Create list of TIFF files --
frames_filenames = [frames_filename]
suffix = '@{0:04g}'
for indf in range(1, n_frames_files):
    new_suffix = suffix.format(indf)
    new_filename = frames_filename.replace('.tif', new_suffix+'.tif')
    frames_filenames.append(new_filename)

# -- Load TIFF files --    
frames = None  # A numpy array to store all frames
for indf, filename in enumerate(frames_filenames):    
    with tifffile.TiffFile(filename) as tif:
        chunk = tif.asarray()
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

sound_onset = sound_onset[:n_trials]

if 0:
    # -- Plot timestamps --
    plt.clf()
    ms = 10
    spos = 0.2
    plt.plot(ts_frames, np.zeros(len(ts_frames)), '|', ms=ms)
    plt.plot(sound_onset, spos*np.ones(len(sound_onset)), 'r|', ms=ms)
    plt.plot(sound_offset, spos*np.ones(len(sound_offset)), 'k|', ms=ms)
    plt.yticks([0, spos], ['frame', 'sound'])
    plt.ylim([-spos, 2*spos])
    plt.xlabel('Time (s)')
    plt.legend(['frame', 'sound onset', 'sound offset'])
    plt.show()

# -- Estimate average evoked image --
sound_duration = np.mean(sound_offset[:len(sound_onset)]-sound_onset)
frame_rate = 1/np.mean(np.diff(ts_frames))
sound_duration_in_frames = int(round(sound_duration*frame_rate))
# Find frames corresponding to evoked period
frame_after_onset = np.searchsorted(ts_frames, sound_onset, side='left')

evoked_frames_each_freq = []
plt.clf()
fig = plt.gcf()
axs = fig.subplots(n_freq, 3)
cmap = 'viridis'
for indf, freq in enumerate(possible_freq):
    frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, indf]]
    evoked_frames_this_freq = np.tile(frame_after_onset_this_freq, (sound_duration_in_frames, 1))
    evoked_frames_this_freq += np.arange(sound_duration_in_frames)[:,None]
    evoked_frames_this_freq = np.sort(evoked_frames_this_freq.ravel())
    evoked_frames_each_freq.append(evoked_frames_this_freq)
    
    avg_evoked_this_freq = np.mean(frames[evoked_frames_this_freq], axis=0)
    baseline_frames_this_freq = evoked_frames_this_freq - sound_duration_in_frames
    avg_baseline_this_freq = np.mean(frames[baseline_frames_this_freq], axis=0)

    # -- Estimate change in fluorescence --
    signal_change = (avg_evoked_this_freq-avg_baseline_this_freq)/avg_baseline_this_freq
    
    plt.sca(axs[indf, 0])
    plt.imshow(avg_evoked_this_freq, cmap=cmap)
    plt.colorbar()
    plt.title(f'Evoked')
    plt.ylabel(f'{freq:g} Hz\n({len(frame_after_onset_this_freq)} trials)')
    plt.sca(axs[indf, 1])
    plt.imshow(avg_baseline_this_freq, cmap=cmap)
    plt.colorbar()
    plt.title('Baseline')
    plt.sca(axs[indf, 2])
    plt.imshow(signal_change, cmap=cmap, vmin=INTENSITY_SCALE[0], vmax=INTENSITY_SCALE[1])
    plt.colorbar()
    plt.title('Signal change: (E-B)/B')
    plt.show()
    


### for frame in frames: imshow(frame); plt.waitforbuttonpress()
### for indf, frame in enumerate(frames): plt.cla(); plt.imshow(frame); plt.title(indf); plt.waitforbuttonpress()

