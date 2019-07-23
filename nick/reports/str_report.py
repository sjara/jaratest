import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
from jaratoolbox import settings
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import loadopenephys
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extraplots

#We will see if this is necessary
from jaratest.nick.database import dataloader_v3 as dataloader
from jaratest.nick.database import dataplotter
reload(dataplotter)

#Define the gridspec for the report

def plot_str_report(cell, saveDir):
    plt.clf()
    #first 4 rows are not needed
    # gs = gridspec.GridSpec(9, 6)
    gs = gridspec.GridSpec(5, 6)
    gs.update(left=0.15, right=0.95, bottom=0.15, wspace=1, hspace=1)

    # #Laser pulse raster
    # ax0 = plt.subplot(gs[0:2, 0:3])
    # if 'laserpulse' in cell['sessiontype']:
    #     spikeData, eventData = dataloader.get_session_ephys(cell, 'laserpulse')
    #     eventOnsetTimes = eventData.get_event_onset_times()
    #     if spikeData.timestamps is not None:
    #         timeRange = [-0.5, 1]
    #         (spikeTimesFromEventOnset,
    #          trialIndexForEachSpike,
    #          indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
    #                                                                        eventOnsetTimes,
    #                                                                        timeRange)
    #         (pRaster,
    #          hcond,
    #          zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
    #                                          indexLimitsEachTrial,
    #                                          timeRange)

    #         ms = 2
    #         plt.setp(pRaster, ms=ms)

    #     plt.title('Laser Pulse')
    # #Laser pulse psth
    # ax1 = plt.subplot(gs[2:4, 0:3])
    # if 'laserpulse' in cell['sessiontype']:
    #     spikeData, eventData = dataloader.get_session_ephys(cell, 'laserpulse')
    #     if spikeData.timestamps is not None:
    #         # dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes, plotLegend=0)

    #         timeRange = [-0.5, 1]
    #         binsize = 0.02
    #         lw=2

    #         (spikeTimesFromEventOnset,
    #         trialIndexForEachSpike,
    #         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
    #                                                                      eventOnsetTimes,
    #                                                                      [timeRange[0]-binsize,
    #                                                                       timeRange[1]])
    #         binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
    #         spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
    #         pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
    #         plt.setp(pPSTH, lw=lw)
    #         plt.hold(True)
    #         zline = plt.axvline(0,color='0.75',zorder=-10)
    #         plt.xlim(timeRange)

            extraplots.set_ticks_fontsize(ax1, 9)



    # #Laser train raster
    # ax2 = plt.subplot(gs[0:2, 3:6])
    # spikeData, eventData = dataloader.get_session_ephys(cell, 'lasertrain')
    # eventOnsetTimes = eventData.get_event_onset_times()
    # eventOnsetTimes = spikesanalysis.minimum_event_onset_diff(eventOnsetTimes, 0.5)

    # if spikeData.timestamps is not None:
    #     timeRange = [-0.5, 1]
    #     (spikeTimesFromEventOnset,
    #     trialIndexForEachSpike,
    #     indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
    #                                                                 eventOnsetTimes,
    #                                                                 timeRange)
    #     (pRaster,
    #      hcond,
    #      zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
    #                                      indexLimitsEachTrial,
    #                                      timeRange)

    #     ms = 2
    #     plt.setp(pRaster, ms=ms)

    #     plt.title('Laser Train')

    # #Laser train psth
    # ax3 = plt.subplot(gs[2:4, 3:6])
    # if spikeData.timestamps is not None:
    #     # dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes, plotLegend=0)

    #     lw = 2

    #     binsize = 0.02
    #     (spikeTimesFromEventOnset,
    #         trialIndexForEachSpike,
    #         indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
    #                                                                     eventOnsetTimes,
    #                                                                     [timeRange[0]-binsize,
    #                                                                     timeRange[1]])
    #     binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
    #     spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
    #     pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1])
    #     plt.setp(pPSTH, lw=lw)
    #     plt.hold(True)
    #     zline = plt.axvline(0,color='0.75',zorder=-10)
    #     plt.xlim(timeRange)

    #Sorted tuning raster
    try:
        ax4 = plt.subplot(gs[0:2, 0:3])
        spikeData, eventData = dataloader.get_session_ephys(cell, 'tc')
        eventOnsetTimes = eventData.get_event_onset_times()
        bdata = dataloader.get_session_bdata(cell, 'tc')
        #NOTE: We need to make the behav trials and the events the same size before this will work.
        if len(eventOnsetTimes)>len(bdata['currentFreq']):
            eventOnsetTimes = eventOnsetTimes[:len(bdata['currentFreq'])]
        if spikeData.timestamps is not None:
            ms = 1
            timeRange = [-0.5, 1]
            sortArray=bdata['currentFreq']
            labels = ['{:.3}'.format(freq/1000.) for freq in np.unique(bdata['currentFreq'])]
            trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                         eventOnsetTimes,
                                                                         timeRange)
            (pRaster,
            hcond,
            zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                           indexLimitsEachTrial,
                                           timeRange,
                                           trialsEachCond=trialsEachCond,
                                           labels=labels)
            #Set the marker size for better viewing
            plt.setp(pRaster, ms=ms)
            extraplots.set_ticks_fontsize(ax4, 9)

        #TC heatmap
        ax5 = plt.subplot(gs[2:4, 0:3])

        if spikeData.timestamps is not None:
            timeRange = [0, 0.2]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                        eventOnsetTimes,
                                                                        timeRange)
            intensityEachTrial = bdata['currentIntensity']
            possibleIntensity = np.unique(intensityEachTrial)
            freqEachTrial = bdata['currentFreq']
            possibleFreq = np.unique(freqEachTrial)
            trialsEachCond = behavioranalysis.find_trials_each_combination(intensityEachTrial,
                                                                        possibleIntensity,
                                                                        freqEachTrial,
                                                                        possibleFreq)
            avgSpikesArray = spikesanalysis.avg_num_spikes_each_condition(trialsEachCond, indexLimitsEachTrial)

            #Flip so high intensity is on top
            avgSpikesArray = np.flipud(avgSpikesArray)
            cax = plt.imshow(avgSpikesArray, interpolation='none', cmap='Blues')
            cbar = plt.colorbar(cax, format='%.1f')
            cbar.ax.set_ylabel('Avg spikes in\n200msec after stim', fontsize = 9)
            ax5.set_xticks(range(len(possibleFreq)))
            ax5.set_xticklabels(['{:.1f}'.format(freq/1000.) for freq in possibleFreq], rotation='vertical')
            ax5.set_xlabel('Frequency, Hz')
            ax5.set_yticks(range(len(possibleIntensity)))
            ax5.set_yticklabels(possibleIntensity[::-1])
            ax5.set_ylabel('Intensity\ndB (SPL)')
            extraplots.set_ticks_fontsize(ax5, 9)
            plt.title('cf:{:.0f} thresh:{:.0f}\nlower:{:.0f} upper:{:.0f}'.format(cell['cf'], cell['threshold'], cell['lowerFreq'], cell['upperFreq']), fontsize=9)
    except IndexError:
        print "No TC for this cell"

    #Sorted am raster
    try:
        ax6 = plt.subplot(gs[0:2, 3:6])
        spikeData, eventData = dataloader.get_session_ephys(cell, 'am')
        eventOnsetTimes = eventData.get_event_onset_times()
        bdata = dataloader.get_session_bdata(cell, 'am')
        colors = get_colors(len(np.unique(bdata['currentFreq'])))


        if spikeData.timestamps is not None:
            ms = 2
            sortArray=bdata['currentFreq']
            labels = ['{:d}'.format(int(freq)) for freq in np.unique(bdata['currentFreq'])]
            trialsEachCond = behavioranalysis.find_trials_each_type(sortArray, np.unique(sortArray))
            timeRange = [-0.2, 0.9]
            (spikeTimesFromEventOnset,
            trialIndexForEachSpike,
            indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                         eventOnsetTimes,
                                                                         timeRange)
            (pRaster,
             hcond,
             zline) = extraplots.raster_plot(spikeTimesFromEventOnset,
                                             indexLimitsEachTrial,
                                             timeRange,
                                             trialsEachCond=trialsEachCond,
                                             labels=labels,
                                             colorEachCond=colors)
            #Set the marker size for better viewing
            plt.setp(pRaster, ms=ms)

            extraplots.set_ticks_fontsize(ax6, 9)


        #AM psth
        ax7 = plt.subplot(gs[2:4, 3:6])
        # if spikeData.timestamps is not None:
        #     dataplotter.plot_psth(spikeData.timestamps,
        #                         eventOnsetTimes,
        #                         sortArray=bdata['currentFreq'],
        #                         colorEachCond=colors,
        #                         plotLegend=0)

        if spikeData.timestamps is not None:
            #NOTE: I am here.
            # dataplotter.plot_psth(spikeData.timestamps, eventOnsetTimes, plotLegend=0)

            binsize=0.02
            (spikeTimesFromEventOnset,
             trialIndexForEachSpike,
             indexLimitsEachTrial) = spikesanalysis.eventlocked_spiketimes(spikeData.timestamps,
                                                                           eventOnsetTimes,
                                                                           [timeRange[0]-binsize,
                                                                            timeRange[1]])
            binEdges = np.around(np.arange(timeRange[0]-binsize, timeRange[1]+2*binsize, binsize), decimals=2)
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
            pPSTH = extraplots.plot_psth(spikeCountMat/binsize, 1, binEdges[:-1], trialsEachCond, colorEachCond=colors)
            plt.setp(pPSTH, lw=2)
            plt.hold(True)
            zline = plt.axvline(0,color='0.75',zorder=-10)
            plt.xlim(timeRange)
            extraplots.set_ticks_fontsize(ax7, 9)



    except IndexError:
        print "No AM for this cell"

    (timestamps,
     samples,
     recordingNumber) = dataloader.load_all_spikedata(cell)

    #ISI loghist
    ax8 = plt.subplot(gs[4, 0:2])
    if timestamps is not None:
        try:
            spikesorting.plot_isi_loghist(timestamps)
        except:
            # raise AttributeError
            print "problem with isi vals"

    #Waveforms
    ax9 = plt.subplot(gs[4, 2:4])
    if timestamps is not None:
        spikesorting.plot_waveforms(samples)

    #Events in time
    ax10 = plt.subplot(gs[4, 4:6])
    if timestamps is not None:
        try:
            spikesorting.plot_events_in_time(timestamps)
        except:
            print "problem with isi vals"

    fig = plt.gcf()
    fig.set_size_inches(8.5, 11)

    figName = '{}_{}_{}_TT{}c{}.png'.format(cell['subject'],
                                            cell['date'],
                                            int(cell['depth']),
                                            int(cell['tetrode']),
                                            int(cell['cluster']))

    plt.suptitle('{}\n{}'.format(figName[:-4], cell['brainarea']))

    figPath = os.path.join(saveDir, figName)
    plt.savefig(figPath)

def get_colors(ncolors):
    ''' returns n distinct colours for plotting purpouses when you don't want to manually specify colours'''
    from matplotlib.pyplot import cm
    colors = cm.viridis(np.linspace(0,1,ncolors))
    return colors
