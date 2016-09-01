#!/usr/bin/env python
from jaratoolbox import loadopenephys
import numpy as np
from pylab import *
import os
import matplotlib.pyplot as plt

SAMPLING_RATE=30000.0

ephysDir = '/home/nick/data/ephys/hm4d002/2014-08-25_16-33-38/'

spikeFilename = os.path.join(ephysDir, 'Tetrode4.spikes')
spikes=loadopenephys.DataSpikes(spikeFilename)

eventsFilename = os.path.join(ephysDir, 'all_channels.events')
events=loadopenephys.Events(eventsFilename)

def threshold_spikes(lower_threshold_uV, upper_threshold_uV, spike_samples):

    '''Converts a new threshold to unsigned int (the openephys data format
    for spikes) and applies it to a spike array. 

    Arguments:

    threshold_uV: float, new threshold in uV
    spike_samples: array, Spikes in shape (n, 40, 4), where n is the number of spikes, each spike has 40 samples in each of the 4 tetrode channels. 

    Returns:

    pass_inds: bool list with True for spikes that pass the threshold and False for spikes that do not. 
    '''

    lower_threshold_converted=(lower_threshold_uV*5000.0/1000.0)+32768.0
    lower_threshold_converted=int(lower_threshold_converted)
    upper_threshold_converted=(upper_threshold_uV*5000.0/1000.0)+32768.0
    upper_threshold_converted=int(upper_threshold_converted)

    #pass_inds= ((spikes.samples>lower_threshold_converted) & (spikes.samples<upper_threshold_converted)).any((1,2))
    max_channels=spikes.samples[:,:,10:20].max(2)
    pass_inds=((max_channels>lower_threshold_converted) & (max_channels < upper_threshold_converted))
    print sum(pass_inds)
    return pass_inds

    

def plot_raster(spikeTimestamps, eventTimes, eventID, targetID=1,timeRange=[-0.5, 1]):
    from jaratoolbox import spikesanalysis

    '''
    Plots a raster of spikes with respect to a stimulus.

    Arguments:

    spikeTimestamps: array, timestamps of all spikes collected
    eventTimes: array, timestamps of all events collected
    eventID: array, event channel
    targetID: int, event channel to use for aligning spikes
    timeRange: array, lower and upper limit of time axis in seconds

    '''
    eventOnsetTimes=eventTimes[evID==targetID]
    (spikeTimesFromEventOnset,trialIndexForEachSpike,indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeTimestamps,eventOnsetTimes,timeRange)
    plot(spikeTimesFromEventOnset, trialIndexForEachSpike, 'b.', ms=1)
    axvline(x=0, ymin=0, ymax=1, color='r')
    show()



def plot_spike_peak_voltage(spikeSamples, chx=0, chy=1):
    max_samp=spikeSamples.max(2)
    plot(max_samp[:,chx], max_samp[:,chy], 'b.', ms=1)
    xlabel('Channel {0}'.format(chx))
    ylabel('Channel {0}'.format(chy))
    #TODO: Convert to uV
    ylim([32500, 34500])
    xlim([32500, 34500])
    show()




def plot_spike_peak_voltage_hist(spikeSamples, chx=0, chy=1):

    max_samp=spikeSamples.max(2)
    nbins = len(max_samp[:,0])/60
    H, xedges, yedges = np.histogram2d(max_samp[:,chx],max_samp[:,chy],bins=nbins)
    H = np.rot90(H)
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H==0,H)

    fig2 = plt.figure()
    plt.pcolormesh(xedges,yedges,Hmasked)
    plt.xlabel('Channel {0}'.format(chx))
    plt.ylabel('Channel {0}'.format(chy))
    #TODO: Convert to uV
    ylim([32500, 34500])
    xlim([32500, 34500])
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Counts')
    plt.show()
    

def spike_voltage_threshold_summary(spikeSamples, lower_threshold_uV, upper_threshold_uV):

    passing_inds=threshold_spikes(lower_threshold_uV,upper_threshold_uV, spikeSamples)
    for spike in reshape(spikeSamples, (len(spikeSamples), 160))[passing_inds][:200]:
        plot(spike, 'b-', alpha=0.1)

def peak_voltage_cluster(spikeSamples, comps_to_use, plot_clusters=True):
    from sklearn.mixture import GMM
    
    '''
    Accepts an array of spike samples, plots spike peak voltages per channel, and clusters spikes based on peak voltages. 
    '''
    max_samp=spikeSamples.max(2)
    g=GMM(n_components=comps_to_use)
    g.fit(max_samp)
    preds = g.predict(max_samp)
    
    if plot_clusters:
        for i in preds:
            plot(max_samp[:,0][preds==i], max_samp[:,1][preds==i], ms=1)
        show()
        
    return preds

    

case=1
if case==1:
    pass_inds=threshold_spikes(100, 150, spikes.samples)
    pass_spike_timestamps=spikes.timestamps[pass_inds[:,3]]
    eventTimes=np.array(events.timestamps)/SAMPLING_RATE
    pass_spkTimeStamps=np.array(pass_spike_timestamps)/SAMPLING_RATE
    evID=np.array(events.eventID)
    figure()
    plot_raster(pass_spkTimeStamps, eventTimes, evID) 
    
    figure()
    for spike in reshape(spikes.samples, (len(spikes.samples), 160))[pass_inds[:,0]][:500]:
        plot(spike, 'b-', alpha=0.1)
    show()

elif case==2:
    plot_spike_peak_voltage(spikes.samples)
elif case==3:
    plot_spike_peak_voltage_hist(spikes.samples)

