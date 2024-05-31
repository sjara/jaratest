"""
Estimate the average evoked signal for each stimulus frequency from widefield data.
This script combines multiple TIFFs recorded by the PCO software.

You need the tifffile package (I use my tiff virtual environment).
"""

import tifffile
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# -- Load the data --
frames_filename = '/data/widefield/20240601/test000-20240507-151825.tif'
n_frames_files = 3
timestamps_filename = '/data/widefield/20240601/test000_timestamps_20240507_151825.npz'

frames_filenames = [frames_filename]
suffix = '_@{0:04g}'
for indf in range(1, n_frames_files):
    new_suffix = suffix.format(indf)
    new_filename = frames_filename.replace('.tif', new_suffix+'.tif')
    frames_filenames.append(new_filename)

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

# -- Simulate having more sound onsets and frames --
sound_period = np.mean(np.diff(sound_onset))
frame_period = np.mean(np.diff(ts_frames))
new_sound_onset = [sound_onset]
new_sound_offset = [sound_offset]
new_ts_frames = [ts_frames]
for indf in range(1, n_frames_files):
    time_offset = (sound_onset[-1]-sound_onset[0]+sound_period)
    frames_offset = (ts_frames[-1]-ts_frames[0]+frame_period)
    new_sound_onset.append(sound_onset + indf*time_offset)
    new_sound_offset.append(sound_offset + indf*time_offset)
    new_ts_frames.append(ts_frames + indf*frames_offset)
sound_onset = np.concatenate(new_sound_onset)
sound_offset = np.concatenate(new_sound_offset)
ts_frames = np.concatenate(new_ts_frames)

if 1:
    # -- Plot timestamps --
    plt.figure(1)
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


#sys.exit()

# -- Estimate average evoked image --
sound_duration = np.mean(sound_offset[:len(sound_onset)]-sound_onset)
frame_rate = 1/np.mean(np.diff(ts_frames))
sound_duration_in_frames = int(round(sound_duration*frame_rate))
# Find frames corresponding to evoked period
frame_after_onset = np.searchsorted(ts_frames, sound_onset, side='left')
evoked_frames = np.tile(frame_after_onset, (sound_duration_in_frames, 1))
evoked_frames += np.arange(sound_duration_in_frames)[:,None]
evoked_frames = np.sort(evoked_frames.ravel())
# Average frames
avg_evoked = np.mean(frames[evoked_frames], axis=0)

# -- Estimate average baseline image --
baseline_frames = evoked_frames - sound_duration_in_frames
avg_baseline = np.mean(frames[baseline_frames], axis=0)

# -- Estimate change in fluorescence --
signal_change = (avg_evoked-avg_baseline)/avg_baseline
    
if 1:
    plt.figure(2)
    plt.clf()
    cmap = 'viridis'
    plt.subplot(1, 3, 1)
    plt.imshow(avg_evoked, cmap=cmap)
    plt.colorbar()
    plt.title('Evoked')
    plt.subplot(1, 3, 2)
    plt.imshow(avg_baseline, cmap=cmap)
    plt.colorbar()
    plt.title('Baseline')
    plt.subplot(1, 3, 3)
    plt.imshow(signal_change, cmap=cmap)
    plt.colorbar()
    plt.title('Signal change: (E-B)/B')
    plt.show()
    


### for frame in frames: imshow(frame); plt.waitforbuttonpress()
### for indf, frame in enumerate(frames): plt.cla(); plt.imshow(frame); plt.title(indf); plt.waitforbuttonpress()

