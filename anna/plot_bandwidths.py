from jaratest.nick.database import ephysinterface
from jaratest.nick.database import dataplotter
from jaratoolbox import extraplots
from jaratoolbox import spikesanalysis
from jaratoolbox import spikesorting
from jaratoolbox import behavioranalysis
reload(ephysinterface)
reload(dataplotter)
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    mouse = 'band001'
    date = '2016-07-13'
    session = ['2', '17-06-19', '', '17-29-19']
    suffixes = ['d', '', 'e']
    ei = ephysinterface.EphysInterface(mouse, date, '', 'bandwidth_am')
    bdata = ei.loader.get_session_behavior(suffixes[2])
    ei2 = ephysinterface.EphysInterface(mouse, date, '', 'am_tuning_curve')
    bdata2 = ei2.loader.get_session_behavior(suffixes[0])    
    currentFreq = bdata2['currentFreq']
    currentBand = bdata['currentBand']
    currentAmp = bdata['currentAmp']
    currentInt = bdata2['currentIntensity']
      
    for tetrode in range(1, 2):
        dataSpikes = ei.loader.get_session_spikes(session[3], tetrode)
        dataSpikes2 = ei2.loader.get_session_spikes(session[1], tetrode)
        #clusters = np.unique(dataSpikes.clusters)
        clusters = [12]
        for cluster in clusters:
            plt.clf()
            
            # -- plot bandwidth rasters --
            eventData = ei.loader.get_session_events(session[3])
            spikeData = ei.loader.get_session_spikes(session[3], tetrode, cluster=cluster)
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
                plt.subplot2grid((6, 6), (2*ind, 0), rowspan = 2, colspan = 3)
                trialsThisSecondVal = trialsEachCond[:, :, ind]
                pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                                indexLimitsEachTrial,
                                                                timeRange,
                                                                trialsEachCond=trialsThisSecondVal,
                                                                labels=firstSortLabels)
                plt.setp(pRaster)
                plt.title(secondSortLabels[ind])
                plt.ylabel('bandwidth (octaves)')
                if ind == len(np.unique(currentAmp)) - 1:
                    plt.xlabel("Time from sound onset (sec)")
            
            # -- plot frequency tuning heat map -- 
            plt.subplot2grid((6, 6), (0, 3), rowspan = 2, colspan = 3)
            
            eventData = ei2.loader.get_session_events(session[1])
            spikeData = ei2.loader.get_session_spikes(session[1], tetrode, cluster=cluster)
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
            
            # -- show cluster analysis --
            tsThisCluster = oneTT.timestamps[oneTT.clusters==cluster]
            wavesThisCluster = oneTT.samples[oneTT.clusters==cluster]
            
            # -- Plot ISI histogram --
            plt.subplot2grid((6,6), (4,0), rowspan=2, colspan=2)
            spikesorting.plot_isi_loghist(tsThisCluster)
            plt.ylabel('c%d'%cluster,rotation=0,va='center',ha='center')
            plt.xlabel('')

            # -- Plot waveforms --
            plt.subplot2grid((6,6), (4,2), rowspan=2, colspan=2)
            spikesorting.plot_waveforms(wavesThisCluster)

            # -- Plot projections --
            plt.subplot2grid((6,6), (4,4), rowspan=1, colspan=2)
            spikesorting.plot_projections(wavesThisCluster)

            # -- Plot events in time --
            plt.subplot2grid((6,6), (5,4), rowspan=1, colspan=2)
            spikesorting.plot_events_in_time(tsThisCluster)

            plt.subplots_adjust(wspace = 0.7)
            plt.suptitle(mouse+', Session '+session[0]+', Tetrode '+str(tetrode)+', Cluster '+str(cluster))
            plt.show()
            plt.savefig('/home/jarauser/Pictures/'+mouse+'_session'+session[0]+'_tetrode'+str(tetrode)+'_cluster'+str(cluster)+'.png', bbox_inches='tight', format = 'png')



