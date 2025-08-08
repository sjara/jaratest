'''
This code shows per 1 session, how the change in signal looks like for odd and even trials
'''
import os
import numpy as np
from jaratoolbox import settings
import lizeth_utils as lutils
import matplotlib.pyplot as plt

mouse_name = 'wifi008'
date = '20241219'
session = '161007' 

# mouse_name = 'wifi009'
# date = '20250611'
# session = '114322'

# mouse_name = 'wifi010'
# date = '20250424'
# session = '145415'

# mouse_name = 'wifi011'
# date = '20250424'
# session = '162320'

paradigm = 'am_tuning_curve'

data_dir = os.path.join(settings.WIDEFIELD_PROCESSED, mouse_name)
data_file = os.path.join(data_dir , f'{mouse_name}_{date}_{session}_splitted.npz')


if os.path.exists(data_file):
    wf_data = np.load(data_file, allow_pickle=True)
else:
    wf_data = lutils.process_widefield_odd_even(mouse_name, date, session, save_data=True)

evoked_frames_each_freq = []
plt.clf()
fig = plt.gcf()
axs = fig.subplots(int(wf_data['n_freq']), 6, sharex=True, sharey=True) 
cmap = 'viridis'

#frame_after_onset = np.searchsorted(wf_data['ts_frames'], wf_data['sound_onset'], side='left')

intensity_scale = [[0.0, 0.03], [0.002, 0.06], [0.0, 0.06]] # wifi008
#intensity_scale = [[0.0, 0.008], [0.002, 0.01], [0.0, 0.01]] # wifi009
#intensity_scale = [[0.002, 0.025], [0.002, 0.06], [0.0, 0.005]] # wifi010
#intensity_scale = [[0.002, 0.01], [0.002, 0.02], [0.0, 0.005]] # wifi011


for indf, freq in enumerate(wf_data['possible_freq']):
    # Plotting
    plt.sca(axs[indf, 0])
    plt.imshow(np.rot90(wf_data['avg_evoked_set1'][indf]), cmap=cmap)
    plt.colorbar()
    plt.title('Evoked Set 1')
    plt.ylabel(f'{freq:g} Hz\n({(len(wf_data['set1_indices']))/5} trials)')

    plt.sca(axs[indf, 1])
    plt.imshow(np.rot90(wf_data['avg_baseline_set1'][indf]), cmap=cmap)
    plt.colorbar()
    plt.title('Baseline Set 1')

    plt.sca(axs[indf, 2])
    plt.imshow(np.rot90(wf_data['signal_change_set1'][indf]), cmap=cmap, vmin=intensity_scale[indf][0], vmax=intensity_scale[indf][1])#vmin=intensity_scale[0], vmax=intensity_scale[1]) #vmax=intensity_scale[indf][1])
    plt.colorbar()
    plt.title('Signal change Set 1')

    plt.sca(axs[indf, 3])
    plt.imshow(np.rot90(wf_data['avg_evoked_set2'][indf]), cmap=cmap)
    plt.colorbar()
    plt.title('Evoked Set 2')

    plt.sca(axs[indf, 4])
    plt.imshow(np.rot90(wf_data['avg_baseline_set2'][indf]), cmap=cmap)
    plt.colorbar()
    plt.title('Baseline Set 2')

    plt.sca(axs[indf, 5])
    plt.imshow(np.rot90(wf_data['signal_change_set2'][indf]), cmap=cmap, vmin=intensity_scale[indf][0], vmax=intensity_scale[indf][1])#vmin=intensity_scale[0], vmax=intensity_scale[1])
    plt.colorbar()
    plt.title('Signal change Set 2')

    fig.suptitle(f"{mouse_name} / {date} / {session}", fontsize=13)

plt.show()