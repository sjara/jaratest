"""
Frequency tuning curves of neurons recorded with two-photon imaging.
"""

import matplotlib.pyplot as plt
import numpy as np
from jaratoolbox import twophotonanalysis
from jaratoolbox import behavioranalysis

subject = 'imag022'
date = '20260123'
session = '012'
plane = 0

data2p = twophotonanalysis.TwoPhoton(subject, date, session, plane, paradigm='am_tuning_curve')
print(f"Loaded {data2p.roiF.shape[0]} ROIs from {data2p.data_path}")
print(f"Sampling rate: {data2p.srate} Hz")

if 1:
    time_range = [-1, 3.0]  # Time window around event in seconds
    # Filter cells with low probability
    data2p.filter_cells(prob_threshold=0.5)
    signal_type = 'dF/F' #'raw F'
    if signal_type == 'dF/F':
        eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
    else:
        eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=False)
    trialavg = eventlocked[:, valid_events, :].mean(axis=1)

    # -- Plot evoked response (of the mean across cells) --
    fig = plt.figure(1) #gcf()
    fig.clf()
    fig.set_constrained_layout(True)
    ax0 = plt.subplot(4, 1, (1,3))
    plt.imshow(trialavg, interpolation='nearest', extent=[*time_range, eventlocked.shape[0], 0])
    plt.colorbar(label=f'Signal ({signal_type})')
    plt.axvline(0, color='darkred', ls='-')
    plt.title(f'Event-locked average ({subject} {date} {session} p{plane})')
    #plt.xlabel('Time from sound onset (s)')
    plt.ylabel('Neuron')
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax1 = plt.subplot(4, 1, 4, sharex=ax0)
    plt.plot(tvec, np.nanmean(trialavg, axis=0), lw=2)
    plt.axvline(0, color='darkred', ls='-')
    plt.xlabel('Time from sound onset (s)')
    plt.ylabel(f'Avg signal\nacross cells ({signal_type})')
    plt.show()

if 1:
    # -- Create frequency tuning curves for each cell --
    time_range = [0, 1.0]  # Time window for calculating response
    data2p.filter_cells(prob_threshold=0.5)
    
    # Fix number of trials if behavior and 2p data mismatch
    n_trials_2p = len(data2p.event_onset)
    n_trials_behavior = len(data2p.bdata['currentFreq'])
    if n_trials_2p < n_trials_behavior:
        data2p.bdata['currentFreq'] = data2p.bdata['currentFreq'][:n_trials_2p]
        print(f"Warning: Fewer 2p trials ({n_trials_2p}) than behavior trials ({n_trials_behavior})." +
                " Truncating behavior trials.")
    elif n_trials_2p > n_trials_behavior:
        data2p.event_onset = data2p.event_onset[:n_trials_behavior]
        print(f"Warning: More 2p trials ({n_trials_2p}) than behavior trials ({n_trials_behavior})." +
                " Truncating 2p trials.")

    # Get event-locked responses with dF/F
    eventlocked, tvec, valid_events = data2p.event_locked_average(time_range=time_range, dff=True)
    n_cells, n_trials, n_timepoints = eventlocked.shape
    
    # Get unique frequencies and find trials for each frequency
    n_trials_2p = len(data2p.event_onset)

    current_freq = data2p.bdata['currentFreq']
    possible_freq = np.unique(current_freq)
    n_freq = len(possible_freq)
    trials_each_freq = behavioranalysis.find_trials_each_type(current_freq, possible_freq)
    
    # Calculate mean response for each frequency for each cell
    tuning_curves = np.zeros((n_cells, n_freq))
    for ind_freq, this_freq in enumerate(possible_freq):
        trials_this_freq = trials_each_freq[:, ind_freq]
        # Average across trials and time for this frequency
        tuning_curves[:, ind_freq] = eventlocked[:, trials_this_freq, :].mean(axis=(1, 2))
    
    # -- Plot tuning curves for all cells --
    fig = plt.figure(2) #gcf()
    fig.clf()
    fig.set_constrained_layout(True)
    
    # Plot individual tuning curves
    ax1 = plt.subplot(2, 1, 1)
    for ind_cell in range(n_cells):
        plt.plot(possible_freq, tuning_curves[ind_cell, :], 'o-', alpha=0.3, lw=0.5)
    plt.xscale('log')
    ax1.set_xticks(possible_freq)
    ax1.set_xticklabels([f'{freq/1000:.1f}' for freq in possible_freq])
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Mean dF/F')
    plt.title(f'Frequency tuning curves - all cells ({subject} {date} {session} p{plane})')
    plt.grid(True, alpha=0.3)
    
    # Plot average tuning curve across cells
    ax2 = plt.subplot(2, 1, 2)
    mean_tuning = tuning_curves.mean(axis=0)
    sem_tuning = tuning_curves.std(axis=0) / np.sqrt(n_cells)
    plt.errorbar(possible_freq, mean_tuning, yerr=sem_tuning, 
                    marker='o', capsize=5, lw=2)
    plt.xscale('log')
    ax2.set_xticks(possible_freq)
    ax2.set_xticklabels([f'{freq/1000:.1f}' for freq in possible_freq])
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Mean dF/F')
    plt.title(f'Average tuning curve (n={n_cells} cells)')
    plt.grid(True, alpha=0.3)
    
    plt.show()
