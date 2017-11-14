from jaratest.nick.database import dataplotter
from jaratest.nick.database import dataloader_v2 as dataloader
from jaratest.nick.ephysExperiments import clusterManySessions_v2 as cms2
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
from scipy import stats
import os
import string
import pdb

def get_colours(ncolours):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colours = cm.viridis(np.linspace(0,1,ncolours))
    return colours

def get_cell_info(cell):
    # ephysDirs = [word.strip(string.punctuation) for word in cell['ephys'].split()]
    # behavDirs = [word.strip(string.punctuation) for word in cell['behavior'].split()]
    # sessType = [word.strip(string.punctuation) for word in cell['sessiontype'].split()]

    tetrode = int(cell['tetrode'])
    cluster = int(cell['cluster'])
    noiseIndex = [i for i, type in enumerate(cell['sessiontype']) if type == 'noiseburst']
    laserIndex = [i for i, type in enumerate(cell['sessiontype']) if type == 'laserpulse']
    laserTrainIndex = [i for i, type in enumerate(cell['sessiontype']) if type == 'lasertrain']
    tuningIndex = [i for i, type in enumerate(cell['sessiontype']) if type == 'tc']
    amIndex = [i for i, type in enumerate(cell['sessiontype']) if type == 'am']
    cellInfo = {'ephysDirs': cell['ephys'],
                'behavDirs': cell['behavior'],
                'tetrode': tetrode,
                'cluster': cluster,
                'noiseIndex': noiseIndex,
                'laserIndex': laserIndex,
                'laserTrainIndex': laserTrainIndex,
                'tuningIndex': tuningIndex,
                'amIndex': amIndex,
                'subject': cell['subject'],
                'date': cell['date'],
                'depth': int(cell['depth']),
                'experimentInd':int(cell['indExperiment']),
                'siteInd':int(cell['indSite'])}
    return cellInfo

def plot_pinp_report(cell, fig_path):
    cellInfo = get_cell_info(cell)
    #pdb.set_trace()
    loader = dataloader.DataLoader(cell['subject'])

    if len(cellInfo['laserTrainIndex'])>0:
        laser = True
        gs = gridspec.GridSpec(13, 6)
    else:
        laser = False
        gs = gridspec.GridSpec(9, 6)
    offset = 4*laser
    gs.update(left=0.15, right=0.85, top = 0.96, wspace=0.7, hspace=1.0)

    plt.clf()

    # -- plot frequency tuning heat map --
    tuningBData = loader.get_session_behavior(cellInfo['behavDirs'][cellInfo['tuningIndex'][-1]])
    freqEachTrial = tuningBData['currentFreq']
    intEachTrial =  tuningBData['currentIntensity']

    eventData = loader.get_session_events(cellInfo['ephysDirs'][cellInfo['tuningIndex'][-1]])
    spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][cellInfo['tuningIndex'][-1]], cellInfo['tetrode'], cluster=cellInfo['cluster'])
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimestamps = spikeData.timestamps

    plt.subplot(gs[2+offset:4+offset, 0:3])
    dataplotter.two_axis_heatmap(spikeTimestamps=spikeTimestamps,
                                    eventOnsetTimes=eventOnsetTimes,
                                    firstSortArray=intEachTrial,
                                    secondSortArray=freqEachTrial,
                                    firstSortLabels=["%.0f" % inten for inten in np.unique(intEachTrial)],
                                    secondSortLabels=["%.1f" % freq for freq in np.unique(freqEachTrial)/1000.0],
                                    xlabel='Frequency (kHz)',
                                    ylabel='Intensity (dB SPL)',
                                    plotTitle='Frequency Tuning Curve',
                                    flipFirstAxis=False,
                                    flipSecondAxis=False,
                                    timeRange=[0, 0.1])
    plt.ylabel('Intensity (dB SPL)')
    plt.xlabel('Frequency (kHz)')
    plt.title('Frequency Tuning Curve')

    # -- plot frequency tuning raster --
    plt.subplot(gs[0+offset:2+offset, 0:3])
    freqLabels = ["%.1f" % freq for freq in np.unique(freqEachTrial)/1000.0]
    dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=freqEachTrial, timeRange=[-0.1, 0.5], labels=freqLabels)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Frequency (kHz)')
    plt.title('Frequency Tuning Raster')

    # -- plot AM PSTH --
    amBData = loader.get_session_behavior(cellInfo['behavDirs'][cellInfo['amIndex'][-1]])
    rateEachTrial = amBData['currentFreq']

    eventData = loader.get_session_events(cellInfo['ephysDirs'][cellInfo['amIndex'][-1]])
    spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][cellInfo['amIndex'][-1]], cellInfo['tetrode'], cluster=cellInfo['cluster'])
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimestamps = spikeData.timestamps
    timeRange = [-0.2, 1.5]

    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                spikeTimestamps, eventOnsetTimes, timeRange)


    numRates = np.unique(rateEachTrial)

    colourList = get_colours(len(numRates))
    trialsEachCond = behavioranalysis.find_trials_each_type(rateEachTrial, numRates)
    plt.subplot(gs[2+offset:4+offset, 3:])
    dataplotter.plot_psth(spikeTimestamps, eventOnsetTimes, rateEachTrial, timeRange = [-0.2, 0.8], binsize = 25, colorEachCond = colourList, plotLegend=0)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Firing rate (Hz)')
    plt.title('AM PSTH')

    # -- plot AM raster --
    plt.subplot(gs[0+offset:2+offset, 3:])
    rateLabels = ["%.0f" % rate for rate in np.unique(rateEachTrial)]
    dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=rateEachTrial, timeRange=[-0.2, 0.8], labels=rateLabels, colorEachCond=colourList)
    plt.xlabel('Time from sound onset (sec)')
    plt.ylabel('Modulation Rate (Hz)')
    plt.title('AM Raster')

    # -- plot laser pulse and laser train data (if available) --
    # -- didn't record laser trains for some earlier sessions --
    if len(cellInfo['laserIndex']) > 0:

        # -- plot laser pulse raster --
        plt.subplot(gs[0:2, 0:3])
        eventData = loader.get_session_events(cellInfo['ephysDirs'][cellInfo['laserIndex'][-1]])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][cellInfo['laserIndex'][-1]], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        timeRange = [-0.1, 0.4]
        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, timeRange=timeRange)
        plt.xlabel('Time from sound onset (sec)')
        plt.title('Laser Pulse Raster')

        # -- plot laser pulse psth --
        plt.subplot(gs[2:4, 0:3])
        dataplotter.plot_psth(spikeTimestamps, eventOnsetTimes, timeRange = timeRange, binsize = 10)
        plt.xlabel('Time from sound onset (sec)')
        plt.ylabel('Firing Rate (Hz)')
        plt.title('Laser Pulse PSTH')

    # -- didn't record laser trains for some earlier sessions --
    if len(cellInfo['laserTrainIndex']) > 0:
        # -- plot laser train raster --
        plt.subplot(gs[0:2, 3:])
        eventData = loader.get_session_events(cellInfo['ephysDirs'][cellInfo['laserTrainIndex'][-1]])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][cellInfo['laserTrainIndex'][-1]], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        timeRange = [-0.2, 1.0]
        dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, timeRange=timeRange)
        plt.xlabel('Time from sound onset (sec)')
        plt.title('Laser Train Raster')

        # -- plot laser train psth --
        plt.subplot(gs[2:4, 3:])
        dataplotter.plot_psth(spikeTimestamps, eventOnsetTimes, timeRange = timeRange, binsize = 10)
        plt.xlabel('Time from sound onset (sec)')
        plt.ylabel('Firing Rate (Hz)')
        plt.title('Laser Train PSTH')

    # -- show cluster analysis --
    tsThisCluster, wavesThisCluster = load_cluster_waveforms(cellInfo)

    # -- Plot ISI histogram --
    plt.subplot(gs[4+offset, 0:2])
    spikesorting.plot_isi_loghist(tsThisCluster)
    plt.ylabel('c%d'%cellInfo['cluster'],rotation=0,va='center',ha='center')
    plt.xlabel('')

    # -- Plot waveforms --
    plt.subplot(gs[4+offset, 2:4])
    spikesorting.plot_waveforms(wavesThisCluster)

    # -- Plot events in time --
    plt.subplot(gs[4+offset, 4:6])
    spikesorting.plot_events_in_time(tsThisCluster)

    cellArgs = [cellInfo['subject'],
                cellInfo['date'],
                cellInfo['experimentInd'],
                cellInfo['siteInd'],
                cellInfo['tetrode'],
                cellInfo['cluster']]

    plt.suptitle('{0}, {1}, Experiment {2}, site {3}, Tetrode {4}, Cluster {5}'.format(*cellArgs))

    fig_name = '{0}_{1}_exp{2}site{3}_TT{4}Cluster{5}.png'.format(*cellArgs)
    full_fig_path = os.path.join(fig_path, fig_name)
    fig = plt.gcf()
    fig.set_size_inches(20, 25)
    fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')

def load_cluster_waveforms(cellInfo):
    idString = 'exp{}site{}'.format(cellInfo['experimentInd'],cellInfo['siteInd'])
    oneTT = cms2.MultipleSessionsToCluster(cellInfo['subject'], cellInfo['ephysDirs'], cellInfo['tetrode'], idString)
    oneTT.load_all_waveforms()
    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    oneTT.set_clusters_from_file()
    tsThisCluster = oneTT.timestamps[oneTT.clusters==cellInfo['cluster']]
    wavesThisCluster = oneTT.samples[oneTT.clusters==cellInfo['cluster']]
    return tsThisCluster, wavesThisCluster

