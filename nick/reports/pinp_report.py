import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import extraplots

#We will see if this is necessary
from jaratest.nick.database import dataloader_v3 as dataloader
from jaratest.nick.database import dataplotter
reload(dataplotter)

#Define the gridspec for the report

def plot_pinp_report(cell, saveDir):
    plt.clf()
    gs = gridspec.GridSpec(9, 6)
    gs.update(left=0.15, right=0.95, bottom=0.15, wspace=1, hspace=1)

    #Laser pulse raster
    ax0 = plt.subplot(gs[0:2, 0:3])
    if 'laserpulse' in cell['sessiontype']:
        spikeData, eventData = dataloader.get_session_ephys(cell, 'laserpulse')
        eventOnsetTimes = eventData.get_event_onset_times()

        # timeRange = [-0.5, 1]
        # (spikeTimesFromEventOnset,
        #  trialIndexForEachSpike,
        #  indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
        #                                                                eventOnsetTimes,
        #                                                                timeRange)
        # extraplots.raster_plot(spikeTimesFromEventOnset,
        #                        indexLimitsEachTrial,
        #                        timeRange)
        if spikeData.timestamps is not None:
            dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes)

    #Laser pulse psth
    ax1 = plt.subplot(gs[2:4, 0:3])
    if 'laserpulse' in cell['sessiontype']:
        spikeData, eventData = dataloader.get_session_ephys(cell, 'laserpulse')
        if spikeData.timestamps is not None:
            dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes, plotLegend=0)

    #Laser train raster
    ax2 = plt.subplot(gs[0:2, 3:6])
    spikeData, eventData = dataloader.get_session_ephys(cell, 'lasertrain')
    eventOnsetTimes = eventData.get_event_onset_times()
    eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)
    if spikeData.timestamps is not None:
        dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes)

    #Laser train psth
    ax3 = plt.subplot(gs[2:4, 3:6])
    if spikeData.timestamps is not None:
        dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes, plotLegend=0)

    #Sorted tuning raster
    try:
        ax4 = plt.subplot(gs[4:6, 0:3])
        spikeData, eventData = dataloader.get_session_ephys(cell, 'tc')
        eventOnsetTimes = eventData.get_event_onset_times()
        bdata = dataloader.get_session_bdata(cell, 'tc')
        if spikeData.timestamps is not None:
            dataplotter.plot_raster(spikeData.timestamps, eventOnsetTimes, sortArray=bdata['currentFreq'])

        #TC heatmap
        ax5 = plt.subplot(gs[6:8, 0:3])
        dataplotter.two_axis_heatmap(spikeData.timestamps,
                                    eventOnsetTimes,
                                    firstSortArray = bdata['currentIntensity'],
                                        secondSortArray = bdata['currentFreq'],
                                        flipFirstAxis=False,
                                        firstSortLabels= np.unique(bdata['currentIntensity']),
                                        secondSortLabels = ['{:.3}'.format(freq/1000.) for freq in np.unique(bdata['currentFreq'])])
    except IndexError:
        print "No TC for this cell"

    #Sorted am raster
    try:
        ax6 = plt.subplot(gs[4:6, 3:6])
        spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
        eventOnsetTimes = eventData.get_event_onset_times()
        bdata = dataloader.get_session_bdata(cell, 'am')
        colors = get_colors(len(np.unique(bdata['currentFreq'])))
        if spikeData.timestamps is not None:
            dataplotter.plot_raster(spikeData.timestamps,
                                    eventOnsetTimes,
                                    sortArray=bdata['currentFreq'],
                                    colorEachCond=colors)

        #AM psth
        ax7 = plt.subplot(gs[6:8, 3:6])
        if spikeData.timestamps is not None:
            dataplotter.plot_psth(spikeData.timestamps,
                                eventOnsetTimes,
                                sortArray=bdata['currentFreq'],
                                colorEachCond=colors,
                                plotLegend=0)
    except IndexError:
        print "No AM for this cell"


    (timestamps,
     samples,
     recordingNumber) = load_all_spikedata(cell)

    #ISI loghist
    ax8 = plt.subplot(gs[8, 0:2])
    if timestamps is not None:
        try:
            spikesorting.plot_isi_loghist(timestamps)
        except:
            # raise AttributeError
            print "problem with isi vals"

    #Waveforms
    ax9 = plt.subplot(gs[8, 2:4])
    if timestamps is not None:
        spikesorting.plot_waveforms(samples)

    #Events in time
    ax10 = plt.subplot(gs[8, 4:6])
    if timestamps is not None:
        try:
            spikesorting.plot_events_in_time(timestamps)
        except:
            print "problem with isi vals"

    fig = plt.gcf()
    fig.set_size_inches(8.5, 11)

    figName = 'exp{}site{}_TT{}c{}.png'.format(int(cell['indExperiment']),
                                                   int(cell['indSite']),
                                                   int(cell['tetrode']),
                                                   int(cell['cluster']))

    plt.suptitle(figName[:-4])

    figPath = os.path.join(saveDir, figName)
    plt.savefig(figPath)

def get_colors(ncolors):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colors = cm.viridis(np.linspace(0,1,ncolors))
    return colors





