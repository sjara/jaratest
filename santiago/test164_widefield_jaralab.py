"""
Load widefield data, show time stamps, and plot average evoked signal.

You need the tifffile package (I use my tiff virtual environment).
"""

import tifffile
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# -- Load the data --
frames_filename = '/data/widefield/20240507/test000-20240507-151825.tif'
timestamps_filename = '/data/widefield/20240507/test000_timestamps_20240507_151825.npz'

timestamps = np.load(timestamps_filename)
sound_onset = timestamps['ts_sound_rising']
sound_offset = timestamps['ts_sound_falling']
ts_frames = timestamps['ts_trigger_rising']

with tifffile.TiffFile(frames_filename) as tif:
    frames = tif.asarray()
    axes = tif.series[0].axes

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

