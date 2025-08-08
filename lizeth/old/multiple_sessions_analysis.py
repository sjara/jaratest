import tifffile
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import detrend
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

# Mouse and session information
# mouse_name = 'wifi008'
# sessions = ['161007','164500', '165243']  
# date = '20241219'

#mouse_name = 'wifi008'
#date = '20250317'
#sessions = ['185100', '192011', '193843','195505','201040']
# date = '20250410'
# sessions = ['162524','163117', '163832','165549']  
# date = '20250411'
# sessions = ['113130', '114249', '115339','120312','122101','122755']

# mouse_name = 'wifi009'
# date = '20250411'
# sessions = ['113130', '114249', '115339','120312']
# sessions = ['122101','122755','154307','155748']

# mouse_name = 'wifi009'
# date = '20250411'
# sessions = ['113130','122755','155748']

# mouse_name = 'wifi010'
# date = '20250424'
# sessions = ['135900', '143307', '144540']
# sessions = ['145415','150446','151937']


mouse_name = 'wifi011'
# date = '20250417'
# sessions = ['145218']
date = '20250424'
sessions = ['155110', '161103', '162320']



# Directory for cached results
save_dir = f"/data/widefield/dynamics_data/{mouse_name}/{date}"
os.makedirs(save_dir, exist_ok=True)

# Prepare for plotting
fig, axs = plt.subplots(len(sessions), 3, sharex=True, sharey=True)
cmap = 'viridis'

for session_index, session in enumerate(sessions):
    print(f"Processing session: {session}")
    session_dir = os.path.join(save_dir, session)
    os.makedirs(session_dir, exist_ok=True)

    # Filenames
    evoked_file = os.path.join(session_dir, "evoked.npy")
    baseline_file = os.path.join(session_dir, "baseline.npy")
    signal_change_file = os.path.join(session_dir, "signal_change.npy")
    possible_freq_file = os.path.join(session_dir, "possible_freq.npy")
    n_freq_file = os.path.join(session_dir, "n_freq.npy")

    # Correctly construct frames filename
    frames_filename = f"/data/widefield/{mouse_name}/{date}/{mouse_name}_{date}_{session}_LG.tif"
    timestamps_filename = f'/data/widefield/{mouse_name}/{date}/{mouse_name}_timestamps_{date}_{session}.npz'
    #stimulus_filename = f'/mnt/jarahubdata/behavior/{mouse_name}/{mouse_name}_am_tuning_curve_{date}_{session}.h5'
    stimulus_filename = f'/data/widefield/{mouse_name}/{mouse_name}_am_tuning_curve_{date}_{session}.h5'
    #frames_filename = '/data/widefield/' + mouse_name + '/' + date + '/' + mouse_name + '_' + date + '_' + session + '_LG.tif'

    # Check if data is already processed
    if all(os.path.exists(f) for f in [evoked_file, baseline_file, signal_change_file, possible_freq_file, n_freq_file]):
        avg_evoked_each_freq = np.load(evoked_file)
        avg_baseline_each_freq = np.load(baseline_file)
        signal_change_each_freq = np.load(signal_change_file)
        possible_freq = np.load(possible_freq_file)
        n_freq = np.load(n_freq_file)
        print("Loaded precomputed data.")
    else:
        print("Processing data...")

        # -- Load TIFF files --
        with tifffile.TiffFile(frames_filename) as tif:
            frames = tif.asarray()

        timestamps = np.load(timestamps_filename)
        sound_onset = timestamps['ts_sound_rising']
        sound_offset = timestamps['ts_sound_falling']
        ts_frames = timestamps['ts_trigger_rising']

        bdata = loadbehavior.BehaviorData(stimulus_filename)
        n_trials = min(len(bdata['currentFreq']), len(sound_onset))
        current_freq = bdata['currentFreq'][:n_trials]
        possible_freq = np.unique(current_freq)
        n_freq = len(possible_freq)
        trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)

        sound_onset = sound_onset[:n_trials]
        sound_duration = np.mean(sound_offset[:len(sound_onset)] - sound_onset)
        frame_rate = 1 / np.mean(np.diff(ts_frames))
        sound_duration_in_frames = int(round(sound_duration * frame_rate))
        frame_after_onset = np.searchsorted(ts_frames, sound_onset, side='left')

        avg_evoked_each_freq = []
        avg_baseline_each_freq = []
        signal_change_each_freq = []

        for indf, freq in enumerate(possible_freq):
            frame_after_onset_this_freq = frame_after_onset[trials_each_freq[:, indf]]
            evoked_frames_this_freq = np.tile(frame_after_onset_this_freq, (sound_duration_in_frames, 1))
            evoked_frames_this_freq += np.arange(sound_duration_in_frames)[:, None]
            evoked_frames_this_freq = np.sort(evoked_frames_this_freq.ravel())

            final_frames = np.searchsorted(evoked_frames_this_freq, len(frames))
            avg_evoked_this_freq = np.mean(frames[evoked_frames_this_freq[:final_frames]], axis=0)
            baseline_frames_this_freq = evoked_frames_this_freq[:final_frames] - sound_duration_in_frames
            avg_baseline_this_freq = np.mean(frames[baseline_frames_this_freq], axis=0)

            signal_change = (avg_evoked_this_freq - avg_baseline_this_freq) / avg_baseline_this_freq

            avg_evoked_each_freq.append(avg_evoked_this_freq)
            avg_baseline_each_freq.append(avg_baseline_this_freq)
            signal_change_each_freq.append(signal_change)

        avg_evoked_each_freq = np.array(avg_evoked_each_freq)
        avg_baseline_each_freq = np.array(avg_baseline_each_freq)
        signal_change_each_freq = np.array(signal_change_each_freq)
        np.save(evoked_file, avg_evoked_each_freq)
        np.save(baseline_file, avg_baseline_each_freq)
        np.save(signal_change_file, signal_change_each_freq)
        np.save(possible_freq_file, possible_freq)
        np.save(n_freq_file, n_freq)
        print("Processing complete. Results saved.")

    #scales = [(-0.01, 0.006), (-0.02, 0.01), (-0.005, 0.014)]  # Customize per session
    # scales = [
    # [(-0.01, 0.05), (-0.02, 0.06), (-0.005, 0.04)],  # Session 1
    # [(-0.015, 0.045), (-0.02, 0.055), (-0.01, 0.05)], # Session 2
    # [(-0.005, 0.04), (-0.01, 0.05), (-0.02, 0.06)]]    # Session 3


# for indf, freq in enumerate(possible_freq):
#     if len(signal_change_each_freq) > indf:
#         plt.sca(axs[session_index, indf % 3])  # Adjust these values as needed
#         # Select the scale for the current session and frequency, or use a default
#         vmin, vmax = scales[session_index][indf] if (session_index < len(scales) and indf < len(scales[session_index])) else (-0.01, 0.05)
#         plt.imshow(signal_change_each_freq[indf], cmap=cmap, vmin=vmin, vmax=vmax)
#         plt.colorbar()
#         plt.title(f'Session {session} - {freq} Hz')
#     else:
#         print(f"Warning: No data for frequency {freq} in session {session}")

# fig.suptitle(f'Activity change across sessions for {mouse_name}')
# plt.show()

# scale_per_session = {
#     '162524': {3000: (-0.01, 0.008),  9798: (-0.01, 0.009), 32000: (-0.01, 0.01)},
#     '163117': {3000: (-0.01, 0.008),  9700: (-0.01, 0.009), 32000: (-0.01, 0.01)},
#     '163832': {3000: (-0.01, 0.008),  9700: (-0.01, 0.009), 32000: (-0.01, 0.01)},
#     '165549': {3000: (-0.01, 0.008),  9700: (-0.01, 0.009), 32000: (-0.01, 0.01)}
# }

# for session_index, session in enumerate(sessions):
#     # … your processing/loading code …

#     for indf, freq in enumerate(possible_freq):
#         if indf < len(signal_change_each_freq):
#             plt.sca(axs[session_index, indf])  # assuming 3 cols and n_freq<=3

#             # Lookup vmin/vmax for this session & frequency, fallback to default
#             vmin, vmax = scale_per_session.get(session, {}).get(freq, (-0.01, 0.009))

#             plt.imshow(signal_change_each_freq[indf],
#                        cmap=cmap, vmin=vmin, vmax=vmax)
#             plt.colorbar()
#             plt.title(f'{freq:.0f} Hz')
#         else:
#             print(f"Warning: No data for frequency {freq} in session {session}")

#     # Label the row with the session name
#     axs[session_index, 0].set_ylabel(f'Session {session}')

# fig.suptitle(f'Activity change across sessions for {mouse_name}')
# plt.tight_layout()
# plt.show()






    for indf, freq in enumerate(possible_freq): #THIS WORKS
        if len(signal_change_each_freq) > indf:
            plt.sca(axs[session_index, indf % 3])
            plt.imshow(np.rot90(signal_change_each_freq[indf]), cmap=cmap, vmin=-0.003, vmax=0.005)
            plt.colorbar()
            plt.title(f'Session {session} - {freq} Hz')
        else:
            print(f"Warning: No data for frequency {freq} in session {session}")

fig.suptitle(f'Activity change across sessions for {mouse_name}')
plt.show()