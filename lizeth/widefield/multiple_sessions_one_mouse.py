"""
Shows signal change for multiple sessions of one mouse in one day
"""

import os
import numpy as np
from jaratoolbox import settings
import lizeth_utils as lutils
import matplotlib.pyplot as plt

# mouse_name = 'wifi008'
# date = '20241219' 
# sessions = ['161007','164500']

#Anesthesia sessions

# mouse_name = 'wifi008'
# date = '20250310' 
# sessions = ['165755','170613','172924']
#session = '165755' #Calcium
#session = '170613' #anesthesia Example 
#session = '172924' #anesthesia Example 

# mouse_name = 'wifi008'
# date = '20250311'
# sessions = ['111936','114832']
#session = '111936' #Good calcium #Example 
#session = '114832' #Anesthesia #Example 

# mouse_name = 'wifi008'
# date = '20250317' #----------------------------
# sessions = ['185100','192011']
#session = '185100' #Calcium
#session = '192011' #Calcium anesthesia #Good for report with anesthesia Example 

mouse_name = 'wifi009'
date = '20250411'
sessions = ['122755','154307']
# session = '122755' #Example
# session = '154307' #Example




# mouse_name = 'wifi009'
# date = '20250411'
# sessions = ['122755','155748']

# mouse_name = 'wifi010'
# date = '20250424'
# sessions = ['135900','143307','144540', '145415', '150446', '151937']

# mouse_name = 'wifi010'
# date = '20250611'
# sessions = ['121624','123330']


#sound_intensity = [60,70,75] If I was testing different sound intensities, I would need to add the parameters here so
#they can appear in the final plot

data_dir = os.path.join(settings.WIDEFIELD_PROCESSED, mouse_name)

# Prepare for plotting
n_frequencies = 3
fig, axs = plt.subplots(len(sessions), n_frequencies, sharex=True, sharey=True)
cmap = 'viridis'

for inds, session in enumerate(sessions):

    data_file = os.path.join(data_dir , f'{mouse_name}_{date}_{session}_processed.npz')

    if os.path.exists(data_file):
        wf_data = np.load(data_file)
    else:
        wf_data = lutils.process_widefield(mouse_name, date, session, save_data=True)

    for indf, freq in enumerate(wf_data['possible_freq']):
        if len(wf_data['signal_change_each_freq']) > indf:
            plt.sca(axs[inds, indf % 3])
            plt.imshow(wf_data['signal_change_each_freq'][indf], cmap=cmap, vmin=-0.003, vmax=0.02)
            plt.colorbar()
            plt.title(f'Session {session} - {freq} Hz')
        else:
            print(f"Warning: No data for frequency {freq} in session {session}")

fig.suptitle(f'Activity change across sessions for {mouse_name}')
plt.show()

