from jaratest.nick.database import ephysinterface
from jaratest.nick.database import dataplotter
from jaratest.nick.database import sitefuncs
from jaratoolbox import extraplots
reload(extraplots)
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
reload(ephysinterface)
reload(dataplotter)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats
import os


def plot_bandwidth_report(mouse, date, site, siteName):
    sessions = site.get_session_ephys_filenames()
    behavFilename = site.get_session_behav_filenames()
    ei = ephysinterface.EphysInterface(mouse, date, '', 'bandwidth_am')
    bdata = ei.loader.get_session_behavior(behavFilename[3][-4:-3])
    charfreq = str(np.unique(bdata['charFreq'])[0]/1000)
    modrate = str(np.unique(bdata['modRate'])[0])
    ei2 = ephysinterface.EphysInterface(mouse, date, '', 'am_tuning_curve')
    bdata2 = ei2.loader.get_session_behavior(behavFilename[1][-4:-3])  
    bdata3 = ei2.loader.get_session_behavior(behavFilename[2][-4:-3])  
    currentFreq = bdata2['currentFreq']
    currentBand = bdata['currentBand']
    currentAmp = bdata['currentAmp']
    currentInt = bdata2['currentIntensity']
    currentRate = bdata3['currentFreq']
      
    #for tetrode in site.tetrodes:
    for tetrode in [2]:
        oneTT = sitefuncs.cluster_site(site, siteName, tetrode)
        dataSpikes = ei.loader.get_session_spikes(sessions[3], tetrode)
        dataSpikes2 = ei2.loader.get_session_spikes(sessions[1], tetrode)
        #clusters = np.unique(dataSpikes.clusters)
        clusters = [8]
        for cluster in clusters:
            plt.clf()
            
            # -- plot bandwidth rasters --
            eventData = ei.loader.get_session_events(sessions[3])
            spikeData = ei.loader.get_session_spikes(sessions[3], tetrode, cluster=cluster)
            eventOnsetTimes = ei.loader.get_event_onset_times(eventData)
            spikeTimestamps = spikeData.timestamps
            timeRange = [-0.2, 1.5]
            
            numBands = np.unique(currentBand)
            numAmps = np.unique(currentAmp)
            
            firstSortLabels = ['{}'.format(band) for band in np.unique(currentBand)]
            secondSortLabels = ['Amplitude: {}'.format(amp) for amp in np.unique(currentAmp)]
            
            trialsEachCond = behavioranalysis.find_trials_each_combination(currentBand, 
                                                                           numBands, 
                                                                           currentAmp, 
                                                                           numAmps)
            spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange)
            for ind, secondArrayVal in enumerate(numAmps):
                plt.subplot2grid((12, 15), (5*ind, 0), rowspan = 4, colspan = 7)
                trialsThisSecondVal = trialsEachCond[:, :, ind]
                pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRange,
                                                                trialsEachCond=trialsThisSecondVal,
                                                                labels=firstSortLabels)
                plt.setp(pRaster, ms=4)
                
                plt.title(secondSortLabels[ind])
                plt.ylabel('bandwidth (octaves)')
                if ind == len(np.unique(currentAmp)) - 1:
                    plt.xlabel("Time from sound onset (sec)")
            
            # -- plot Yashar plots for bandwidth data --
            plt.subplot2grid((12,15), (10,0), rowspan = 2, colspan = 3)
            band_select_plot(spikeTimestamps, eventOnsetTimes, currentAmp, currentBand, [0.0, 1.0], title='bandwidth selectivity')
            plt.subplot2grid((12,15), (10,3), rowspan = 2, colspan = 3)
            band_select_plot(spikeTimestamps, eventOnsetTimes, currentAmp, currentBand, [0.2, 1.0], title='first 200ms excluded')
            
            # -- plot frequency tuning heat map -- 
            plt.subplot2grid((12, 15), (5, 7), rowspan = 4, colspan = 4)
            
            eventData = ei2.loader.get_session_events(sessions[1])
            spikeData = ei2.loader.get_session_spikes(sessions[1], tetrode, cluster=cluster)
            eventOnsetTimes = ei2.loader.get_event_onset_times(eventData)
            spikeTimestamps = spikeData.timestamps
            
            dataplotter.two_axis_heatmap(spikeTimestamps=spikeTimestamps,
                                            eventOnsetTimes=eventOnsetTimes,
                                            firstSortArray=currentInt,
                                            secondSortArray=currentFreq,
                                            firstSortLabels=["%.1f" % inten for inten in np.unique(currentInt)],
                                            secondSortLabels=["%.1f" % freq for freq in np.unique(currentFreq)/1000.0],
                                            xlabel='Frequency (kHz)',
                                            ylabel='Intensity (dB SPL)',
                                            plotTitle='Frequency Tuning Curve',
                                            flipFirstAxis=True,
                                            flipSecondAxis=False,
                                            timeRange=[0, 0.1])
            plt.ylabel('Intensity (dB SPL)')
            plt.xlabel('Frequency (kHz)')
            plt.title('Frequency Tuning Curve')
            
            # -- plot frequency tuning raster --
            plt.subplot2grid((12,15), (0, 7), rowspan = 4, colspan = 4)
            freqLabels = ["%.1f" % freq for freq in np.unique(currentFreq)/1000.0]
            dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=currentFreq, timeRange=[-0.1, 0.5], labels=freqLabels)
            plt.xlabel('Time from sound onset (sec)')
            plt.ylabel('Frequency (kHz)')
            plt.title('Frequency Tuning Raster')
            
            # -- plot AM PSTH --
            eventData = ei2.loader.get_session_events(sessions[2])
            spikeData = ei2.loader.get_session_spikes(sessions[2], tetrode, cluster=cluster)
            eventOnsetTimes = ei2.loader.get_event_onset_times(eventData)
            spikeTimestamps = spikeData.timestamps
            timeRange = [-0.2, 1.5]
            
            spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange)
            colourList = ['b', 'g', 'y', 'orange', 'r']
            numRates = np.unique(currentRate)
            trialsEachCond = behavioranalysis.find_trials_each_type(currentRate, 
                                                                           numRates)
            binEdges = np.around(np.arange(-0.2, 0.85, 0.05), decimals=2)
            spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, binEdges)
            plt.subplot2grid((12,15), (5, 11), rowspan = 4, colspan = 4)
            pPSTH = extraplots.plot_psth(spikeCountMat/0.05, 1, binEdges[:-1], trialsEachCond, colorEachCond=colourList)
            plt.setp(pPSTH)
            plt.xlabel('Time from sound onset (sec)')
            plt.ylabel('Firing rate (Hz)')
            plt.title('AM PSTH')
            
            # -- plot AM raster --
            plt.subplot2grid((12,15), (0, 11), rowspan = 4, colspan = 4)
            rateLabels = ["%.1f" % rate for rate in np.unique(currentRate)]
            dataplotter.plot_raster(spikeTimestamps, eventOnsetTimes, sortArray=currentRate, timeRange=[-0.2, 0.8], labels=rateLabels, colorEachCond=colourList)
            plt.xlabel('Time from sound onset (sec)')
            plt.ylabel('Modulation Rate (Hz)')
            plt.title('AM Raster')
            
            # -- show cluster analysis --
            tsThisCluster = oneTT.timestamps[oneTT.clusters==cluster]
            wavesThisCluster = oneTT.samples[oneTT.clusters==cluster]
            
            # -- Plot ISI histogram --
            plt.subplot2grid((12,15), (10,6), rowspan=2, colspan=3)
            spikesorting.plot_isi_loghist(tsThisCluster)
            plt.ylabel('c%d'%cluster,rotation=0,va='center',ha='center')
            plt.xlabel('')

            # -- Plot waveforms --
            plt.subplot2grid((12,15), (10,9), rowspan=2, colspan=3)
            spikesorting.plot_waveforms(wavesThisCluster)

            # -- Plot projections --
            plt.subplot2grid((12,15), (10,12), rowspan=1, colspan=3)
            spikesorting.plot_projections(wavesThisCluster)

            # -- Plot events in time --
            plt.subplot2grid((12,15), (11,12), rowspan=1, colspan=3)
            spikesorting.plot_events_in_time(tsThisCluster)

            plt.subplots_adjust(wspace = 1.5)
            plt.suptitle('{0}, {1}, {2}, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(mouse, date, siteName, tetrode, cluster, charfreq, modrate))
            fig_path = oneTT.clustersDir
            fig_name = 'TT{0}Cluster{1}.png'.format(tetrode, cluster)
            full_fig_path = os.path.join(fig_path, fig_name)
            fig = plt.gcf()
            fig.set_size_inches(24, 12)
            fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')
            #fig.show()


def band_select_plot(spikeTimeStamps, eventOnsetTimes, amplitudes, bandwidths, timeRange, fullRange = [0.0, 2.0], title=None):
    numBands = np.unique(bandwidths)
    numAmps = np.unique(amplitudes)
    spikeArray = np.zeros((len(numBands), len(numAmps)))
    errorArray = np.zeros_like(spikeArray)
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandwidths, 
                                                                   numBands, 
                                                                   amplitudes, 
                                                                   numAmps)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseTimeRange = [timeRange[1]+0.5, fullRange[1]]
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    plt.hold(True)
    for amp in range(len(numAmps)):
        trialsThisAmp = trialsEachCond[:,:,amp]
        for band in range(len(numBands)):
            trialsThisBand = trialsThisAmp[:,band]
            if spikeCountMat.shape[0] != len(trialsThisBand):
                spikeCountMat = spikeCountMat[:-1,:]
                print "FIXME: Using bad hack to make event onset times equal number of trials"
            thisBandCounts = spikeCountMat[trialsThisBand].flatten()
            spikeArray[band, amp] = np.mean(thisBandCounts)
            errorArray[band,amp] = stats.sem(thisBandCounts)
    xrange = range(len(numBands))
    plt.plot(xrange, baselineSpikeRate*(timeRange[1]-timeRange[0])*np.ones(len(numBands)), color = '0.75', linewidth = 2)
    plt.plot(xrange, spikeArray[:,0].flatten(), '-o', color = '#4e9a06', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(), alpha=0.2, edgecolor = '#8ae234', facecolor='#8ae234')
    plt.plot(range(len(numBands)), spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                     spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
    ax = plt.gca()
    ax.set_xticklabels(numBands)
    plt.xlabel('bandwidth (octaves)')
    plt.ylabel('Average num spikes')
    #patch1 = mpatches.Patch(color='#5c3566', label='0.8')
    #patch2 = mpatches.Patch(color='#4e9a06', label='0.2')
    #plt.legend(handles=[patch1, patch2], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    if title:
        plt.title(title)
        
def suppression_stats(spikeArray):
    peakLowAmp = max(spikeArray[1])
    peakHighAmp = max(spikeArray[0])
        
    
        

