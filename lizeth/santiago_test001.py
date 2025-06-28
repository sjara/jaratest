"""
Shows the signal change thresholded
"""

import os
import numpy as np
from jaratoolbox import settings
import lizeth_utils as lutils
import matplotlib.pyplot as plt

mouse_name = 'wifi008'
date = '20241219'
session = '161007' 
paradigm = 'am_tuning_curve'

mouse_name = 'wifi009'
date = '20250611'
session = '114322'

data_dir = os.path.join(settings.WIDEFIELD_PROCESSED, mouse_name)
data_file = os.path.join(data_dir , f'{mouse_name}_{date}_{session}.npz')

if os.path.exists(data_file):
    wf_data = np.load(data_file)
else:
    wf_data = lutils.process_widefield(mouse_name, date, session, save_data=True)


plt.clf()
n_freq = int(wf_data['n_freq']) #When I save the images, I also save this variable.
fig = plt.gcf()
axs = fig.subplots(n_freq, 2, sharex=True, sharey=True) 
cmap = 'jet' #'viridis'
#p=0
thresholds = [0.006, 0.008, 0.008]
#thresholds = [0.015, 0.047, 0.0462]
intensity_scale = [[0.002, 0.012], [0.002, 0.011], [0.004, 0.01]] # wifi008

for indf, freq in enumerate(wf_data['possible_freq']):
    # plt.sca(axs[indf, 0])
    # plt.imshow(wf_data['avg_evoked_each_freq'][indf], cmap=cmap) 
    # plt.colorbar()
    # plt.title(f'Evoked')
    # plt.ylabel(f'{freq:g} Hz')

    # plt.sca(axs[indf, 1])
    # plt.imshow(wf_data['avg_baseline_each_freq'][indf], cmap=cmap) 
    # plt.colorbar()
    # plt.title('Baseline')
    if indf == 0: cmap = 'Greens'
    if indf == 1: cmap = 'Oranges'
    if indf == 2: cmap = 'Blues'

    plt.sca(axs[indf, 0])
    plt.imshow(np.rot90(wf_data['signal_change_each_freq'][indf]), cmap=cmap,
               vmin=intensity_scale[indf][0], vmax=intensity_scale[indf][1]) #signal_change_each_freq
    plt.colorbar()
    plt.title('Signal change: (E-B)/B')

    plt.sca(axs[indf, 1])
    plt.imshow(np.rot90(wf_data['signal_change_each_freq'][indf]>thresholds[indf]), cmap=cmap) #signal_change_each_freq
    plt.colorbar()
    plt.title('Signal change thresholded')

    fig.suptitle(f"{mouse_name} / {date} / {session}", fontsize=13)
   

plt.show()

# Plot results
# var1, var2

