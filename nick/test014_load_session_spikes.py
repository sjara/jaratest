from jaratoolbox import loadopenephys

import os
import numpy as np

'''
Load spikes from all sessions in an experiment database into an object. 
'''


ephys_path = '/home/nick/data/ephys/hm4d002/cno_08-14/'
ephys_sessions=sorted(os.listdir(ephys_path))
tetrode = 3


case=2

if case == 1:
    all_session_samples=[]
    all_session_timestamps=[]
    for session in ephys_sessions:
        ephys_file = os.path.join(ephys_path, session, 'Tetrode{0}.spikes'.format(tetrode))
        spikes = loadopenephys.DataSpikes(ephys_file)
        all_session_samples.append(spikes.samples)
        all_session_timestamps.append(spikes.timestamps)

elif case == 2:
    session_inds=[]
    conc_samples=[]
    t0_each_session=[]
    timestamps_each_session=[]
    
    for session_ind, session in enumerate(ephys_sessions):
        ephys_file = os.path.join(ephys_path, session, 'Tetrode{0}.spikes'.format(tetrode))
        spikes=loadopenephys.DataSpikes(ephys_file)
        t0_each_session.append(spikes.timestamps[0])

        for sample_ind, channels in enumerate(spikes.samples):
            conc_samples.append(np.concatenate(channels))  #For each spike, save the concatenated channels
            session_inds.append(session_ind)  #For each spike, save the index of the session it came from 
            timestamps_each_session.append(spikes.timestamps[sample_ind])


    conc_samples=np.array(conc_samples)
    session_inds=np.array(session_inds)
    t0_each_session=np.array(t0_each_session)
    timestamps_each_session=np.array(timestamps_each_session)

 
