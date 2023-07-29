"""
Test functions in facemapanalysis for the processing of the sync light
and estimating running on each trial.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from jaratoolbox import loadbehavior
from jaratoolbox import facemapanalysis
from importlib import reload
reload(facemapanalysis)

proc_dir = '/data/figuresdata/2023acid/'
behav_dir = '/data/behavior/'

VSESSION = 0
if VSESSION==0:
    proc_filename = 'acid006_oddball_sequence_20230530_01doi_proc.npy'
    behav_filename = 'acid006_oddball_sequence_20230530adoi.h5'
elif VSESSION==1:
    # Missing blink
    proc_filename = 'acid006_oddball_sequence_20230322_02saline_proc.npy'
    behav_filename = 'acid006_oddball_sequence_20230322bsaline.h5'
elif VSESSION==2:
    proc_filename = 'acid006_oddball_sequence_20230525_01pre_proc.npy'
    behav_filename = 'acid006_oddball_sequence_20230525apre.h5'
elif VSESSION==3:
    proc_filename = 'acid006_oddball_sequence_20230530_03saline_proc.npy'
    behav_filename = 'acid006_oddball_sequence_20230530csaline.h5'
elif VSESSION==4:
    proc_filename = 'acid006_am_tuning_curve_20230525_01saline_proc.npy'
    behav_filename = 'acid006_am_tuning_curve_20230525asaline.h5'

proc = np.load(os.path.join(proc_dir,proc_filename), allow_pickle=True).item()
pixchange = proc['pixelchange'][0]  # A dict inside a 1-item list, so you need to get the first element
sync_light = proc['blink'][0]  # A dict inside a 1-item list, so you need to get the first element

# -- Find onsets of sync light --
sync_light_onset = facemapanalysis.find_sync_light_onsets(sync_light, fixmissing=True)
#print(np.diff(np.where(sync_light_onset)[0]))  # Print period between onsets (in frames)
n_trials_video = np.sum(sync_light_onset)

# -- Estimate running on each trial --
running_threshold = 3
running_each_trial, running_trace_smooth = facemapanalysis.estimate_running_each_trial(pixchange,
    sync_light_onset, smoothsize=10, presamples=4, threshold=running_threshold)

# -- Load behavior file associated with video above --
subject = behav_filename.split('_')[0]
bdata = loadbehavior.BehaviorData(os.path.join(behav_dir, subject, behav_filename))
n_trials_behavior = len(bdata['stimType'])

print(f'Number of trials in video (after fix): {n_trials_video}')
print(f'Number of trials in behavior: {n_trials_behavior}')

# -- Plot sync light and running on each trial --
plt.clf()
ax1 = plt.subplot(2,1,1)
plt.plot(sync_light, '0.8')
sync_light_onset_onlypos = sync_light_onset.astype(float)
sync_light_onset_onlypos[sync_light_onset_onlypos==0] = np.nan  # Replace zeros with np.nan
plt.plot(sync_light.max()*sync_light_onset_onlypos,'.r')
#plt.xlabel('Frame number')
plt.ylabel('Sync light magnitude')
plt.legend(['sync_light','sync_light_onset'], loc='upper right')
plt.subplot(2,1,2, sharex=ax1)
plt.plot(running_trace_smooth, '0.8')
plt.axhline(running_threshold, color='0.5')
plt.plot(np.where(sync_light_onset)[0], running_each_trial*running_trace_smooth.max(), '.g')
plt.xlabel('Frame number')
plt.ylabel('Running speed (a.u.)')
plt.legend(['running_trace_smooth','running_threshold','running_each_trial'], loc='upper right')
plt.show()

