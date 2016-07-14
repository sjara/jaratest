from jaratoolbox import loadopenephys
import os
import numpy as np
from pylab import *

'''
Plots the spikes/sec in five 20-sec bins per session.
'''

SAMPLING_RATE = 30000.0
experiment_dir = '/home/nick/data/ephys/hm4d002/cno_08-18/'
#tetrode = 'Tetrode3.spikes'

sessions = sorted(os.listdir(experiment_dir))
tetrodes_to_plot=[1,2] #Starts from 0
number_of_baselines = 4

#for tetrode_ind in range(4):
for tetrode_ind in tetrodes_to_plot:

    tetrode='Tetrode{0}.spikes'.format(tetrode_ind+1)

    trials=[]
    session_index=[]
    plotting_inds=[]

    for ind, session in enumerate(sessions):
        current_session = session
        current_spikes = loadopenephys.DataSpikes(os.path.join(experiment_dir, current_session, tetrode))
        if current_spikes.filesize > 1024:

            ts = current_spikes.timestamps
            ts = ts-ts[0]
            ts = ts/SAMPLING_RATE

            first = sum(((ts >= 0) & (ts <=20)))
            second = sum((ts > 20) & (ts <=40))
            third = sum((ts > 40) & (ts <=60))
            fourth = sum((ts > 60) & (ts <=80))
            fifth = sum((ts > 80) & (ts <=100))

            trials.append([first, second, third, fourth, fifth])
            session_index.append([ind, ind, ind, ind, ind])
            plotting_inds.append([ind, ind+0.1, ind+0.2, ind+0.3, ind+0.4])

        else:
            pass

    trials = np.array(trials)
    trials = trials/20.
    session_index = np.array(session_index)
    plotting_inds = np.array(plotting_inds)

    averages=[mean(i) for i in trials]
    average_inds=plotting_inds[:,2]

    t=trials.ravel()
    
    s=session_index.ravel()
    pl=plotting_inds.ravel()

    subplot(4,1,tetrode_ind+1)
    plot(pl, t, '.', label = 'Tetrode {0} spikes'.format(tetrode_ind+1))
    plot(average_inds, averages, 'r-', label = 'Tetrode {0} average'.format(tetrode_ind+1))
    ylabel('spikes/sec')
    axvline(x=number_of_baselines+0.75, ymin=0, ymax=1, color='r')


xlabel('Session')
fig = gcf()

draw()
show()
'''
import plotly.plotly as py
py.sign_in('nickponvert', '915nslwqbx')
unique_url = py.plot_mpl(fig, strip_style=True)
'''
