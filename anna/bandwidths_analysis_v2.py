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

def get_cell_info(cell):
    ephysDirs = [word.strip(string.punctuation) for word in cell['ephys'].split()]
    behavDirs = [word.strip(string.punctuation) for word in cell['behavior'].split()]
    sessType = [word.strip(string.punctuation) for word in cell['sessiontype'].split()]
    
    tetrode = int(cell['tetrode'])
    cluster = int(cell['cluster'])
    bandIndex = [i for i, type in enumerate(sessType) if type == 'bandwidth']
    noiseIndex = [i for i, type in enumerate(sessType) if type == 'noisebursts']
    laserIndex = [i for i, type in enumerate(sessType) if type == 'laserPulse' or type == 'laserPulse2.5']
    laserTrainIndex = [i for i, type in enumerate(sessType) if type == 'laserTrain']
    tuningIndex = [i for i, type in enumerate(sessType) if type == 'tuningCurve']
    amIndex = [i for i, type in enumerate(sessType) if type == 'AM']
    cellInfo = {'ephysDirs': ephysDirs,
                'behavDirs': behavDirs,
                'tetrode': tetrode,
                'cluster': cluster,
                'bandIndex': bandIndex,
                'noiseIndex': noiseIndex,
                'laserIndex': laserIndex,
                'laserTrainIndex': laserTrainIndex,
                'tuningIndex': tuningIndex,
                'amIndex': amIndex,
                'subject': cell['subject'],
                'date': cell['date'],
                'depth': int(cell['depth'])}
    return cellInfo

def plot_bandwidth_report(cell):
    cellInfo = get_cell_info(cell)
    #pdb.set_trace()
    loader = dataloader.DataLoader(cell['subject'])
    
    if len(cellInfo['laserIndex'])>0:
        laser = True
        gs = gridspec.GridSpec(13, 6)
    else:
        laser = False
        gs = gridspec.GridSpec(9, 6)
    offset = 4*laser
    gs.update(left=0.15, right=0.85, top = 0.96, wspace=0.7, hspace=1.0)

    plt.clf() 
    bandIndex = cellInfo['bandIndex']
    
    #plots separate reports for every bandwidth session per site
    for index in bandIndex:      
         # -- plot bandwidth rasters --
        plt.clf()
        eventData = loader.get_session_events(cellInfo['ephysDirs'][index])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][index], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        timeRange = [-0.2, 1.5]
        bandBData = loader.get_session_behavior(cellInfo['behavDirs'][index])  
        bandEachTrial = bandBData['currentBand']
        ampEachTrial = bandBData['currentAmp']
        charfreq = str(np.unique(bandBData['charFreq'])[0]/1000)
        modrate = str(np.unique(bandBData['modRate'])[0])
        numBands = np.unique(bandEachTrial)
        numAmps = np.unique(ampEachTrial)
                
        firstSortLabels = ['{}'.format(band) for band in np.unique(bandEachTrial)]
        secondSortLabels = ['Amplitude: {}'.format(amp) for amp in np.unique(ampEachTrial)]      
        spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels = bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial)
        colours = [np.tile(['#4e9a06','#8ae234'],len(numBands)/2+1), np.tile(['#5c3566','#ad7fa8'],len(numBands)/2+1)]
        for ind, secondArrayVal in enumerate(numAmps):
            plt.subplot(gs[5+2*ind+offset:7+2*ind+offset, 0:3])
            trialsThisSecondVal = trialsEachCond[:, :, ind]
            pRaster, hcond, zline = extraplots.raster_plot(spikeTimesFromEventOnset,
                                                            indexLimitsEachTrial,
                                                            timeRange,
                                                            trialsEachCond=trialsThisSecondVal,
                                                            labels=firstSortLabels,
                                                            colorEachCond = colours[ind])
            plt.setp(pRaster, ms=4)        
            plt.title(secondSortLabels[ind])
            plt.ylabel('bandwidth (octaves)')
            if ind == len(np.unique(ampEachTrial)) - 1:
                plt.xlabel("Time from sound onset (sec)")
        
               
        # -- plot Yashar plots for bandwidth data --
        plt.subplot(gs[5+offset:, 3:])
        spikeArray, errorArray, baseSpikeRate = band_select(spikeTimestamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange = [0.0, 1.0])
        band_select_plot(spikeArray, errorArray, baseSpikeRate, numBands, legend=True)
                
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
                                        flipFirstAxis=True,
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
        colourList = ['b', 'g', 'y', 'orange', 'r']
        numRates = np.unique(rateEachTrial)
        trialsEachCond = behavioranalysis.find_trials_each_type(rateEachTrial, numRates)
        plt.subplot(gs[2+offset:4+offset, 3:])
        dataplotter.plot_psth(spikeTimestamps, eventOnsetTimes, rateEachTrial, timeRange = [-0.2, 0.8], binsize = 25, colorEachCond = colourList)
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
        if laser:
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
    
        plt.suptitle('{0}, {1}, {2}um, Tetrode {3}, Cluster {4}, {5}kHz, {6}Hz modulation'.format(cellInfo['subject'], 
                                                                                                cellInfo['date'], 
                                                                                                cellInfo['depth'], 
                                                                                                cellInfo['tetrode'], 
                                                                                                cellInfo['cluster'], 
                                                                                                charfreq, 
                                                                                                modrate))
        
        fig_path = '/home/jarauser/Pictures'
        if len(bandIndex)>1:
            fig_name = '{0}_{1}_{2}um_TT{3}Cluster{4}Ind{5}.png'.format(cellInfo['subject'], cellInfo['date'], cellInfo['depth'], cellInfo['tetrode'], cellInfo['cluster'], index)
        else:
            fig_name = '{0}_{1}_{2}um_TT{3}Cluster{4}.png'.format(cellInfo['subject'], cellInfo['date'], cellInfo['depth'], cellInfo['tetrode'], cellInfo['cluster'])
        full_fig_path = os.path.join(fig_path, fig_name)
        fig = plt.gcf()
        fig.set_size_inches(20, 25)
        fig.savefig(full_fig_path, format = 'png', bbox_inches='tight')


def bandwidth_raster_inputs(eventOnsetTimes, spikeTimestamps, bandEachTrial, ampEachTrial, timeRange = [-0.2, 1.5]):          
    numBands = np.unique(bandEachTrial)
    numAmps = np.unique(ampEachTrial)
            
    firstSortLabels = ['{}'.format(band) for band in numBands]
            
    trialsEachCond = behavioranalysis.find_trials_each_combination(bandEachTrial, 
                                                                           numBands, 
                                                                           ampEachTrial, 
                                                                           numAmps)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimestamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        timeRange) 

    return spikeTimesFromEventOnset, indexLimitsEachTrial, trialsEachCond, firstSortLabels

def band_select(spikeTimeStamps, eventOnsetTimes, amplitudes, bandwidths, timeRange, fullRange = [0.0, 2.0]):
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
    return spikeArray, errorArray, baselineSpikeRate

def band_select_plot(spikeArray, errorArray, baselineSpikeRate, bands, legend = False, labels = ['50 dB SPL', '70 dB SPL'], timeRange = [0,1], title=None):
    xrange = range(len(bands))
    plt.plot(xrange, baselineSpikeRate*(timeRange[1]-timeRange[0])*np.ones(len(bands)), color = '0.75', linewidth = 2)
    plt.plot(xrange, spikeArray[:,0].flatten(), '-o', color = '#4e9a06', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,0].flatten() - errorArray[:,0].flatten(), 
                     spikeArray[:,0].flatten() + errorArray[:,0].flatten(), alpha=0.2, edgecolor = '#8ae234', facecolor='#8ae234')
    plt.plot(range(len(bands)), spikeArray[:,1].flatten(), '-o', color = '#5c3566', linewidth = 3)
    plt.fill_between(xrange, spikeArray[:,1].flatten() - errorArray[:,1].flatten(), 
                     spikeArray[:,1].flatten() + errorArray[:,1].flatten(), alpha=0.2, edgecolor = '#ad7fa8', facecolor='#ad7fa8')
    ax = plt.gca()
    ax.set_xticklabels(bands)
    plt.xlabel('bandwidth (octaves)')
    plt.ylabel('Average num spikes')
    if legend: 
        patch1 = mpatches.Patch(color='#5c3566', label=labels[1])
        patch2 = mpatches.Patch(color='#4e9a06', label=labels[0])
        plt.legend(handles=[patch1, patch2], bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)
    if title:
        plt.title(title)
        
def load_cluster_waveforms(cellInfo):
    oneTT = cms2.MultipleSessionsToCluster(cellInfo['subject'], cellInfo['ephysDirs'], cellInfo['tetrode'], '{}_{}um'.format(cellInfo['date'], cellInfo['depth']))
    oneTT.load_all_waveforms()
    clusterFile = os.path.join(oneTT.clustersDir,'Tetrode%d.clu.1'%oneTT.tetrode)
    oneTT.set_clusters_from_file()
    tsThisCluster = oneTT.timestamps[oneTT.clusters==cellInfo['cluster']]
    wavesThisCluster = oneTT.samples[oneTT.clusters==cellInfo['cluster']]
    return tsThisCluster, wavesThisCluster
    
def suppression_stats(cell):
    cellInfo = get_cell_info(cell)
    loader = dataloader.DataLoader(cell['subject'])
    
    try:
        bandIndex = cellInfo['bandIndex'][0] #only using first for multiple band sessions for now
    except IndexError:
        print "No bandwidth session"
        return None, None
    eventData = loader.get_session_events(cellInfo['ephysDirs'][bandIndex])
    spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][bandIndex], cellInfo['tetrode'], cluster=cellInfo['cluster'])
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimeStamps = spikeData.timestamps
    timeRange = [0.0, 1.0]
    bandBData = loader.get_session_behavior(cellInfo['behavDirs'][bandIndex]) 
    bandEachTrial = bandBData['currentBand']
    ampEachTrial = bandBData['currentAmp']
    charFreq = np.unique(bandBData['charFreq'])[0]
    numBands = np.unique(bandEachTrial)
    numAmps = np.unique(ampEachTrial)
    
    spikeArray, errorArray, baselineSpikeRate = band_select(spikeTimeStamps, eventOnsetTimes, ampEachTrial, bandEachTrial, timeRange)
    suppressionStats = compute_suppression_stats(spikeArray, numBands)
    
    tuningIndex = cellInfo['tuningIndex'][0]
    tuningBData = loader.get_session_behavior(cellInfo['behavDirs'][tuningIndex])
    eventData = loader.get_session_events(cellInfo['ephysDirs'][tuningIndex])
    spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][tuningIndex], cellInfo['tetrode'], cluster=cellInfo['cluster'])
    eventOnsetTimes = loader.get_event_onset_times(eventData)
    spikeTimeStamps = spikeData.timestamps
    freqEachTrial = tuningBData['currentFreq']
    atBestFreq = at_best_freq(spikeTimeStamps, eventOnsetTimes, charFreq, freqEachTrial)
    if len(cellInfo['laserIndex'])>0:
        laserIndex = cellInfo['laserIndex'][-1]
        eventData = loader.get_session_events(cellInfo['ephysDirs'][laserIndex])
        spikeData = loader.get_session_spikes(cellInfo['ephysDirs'][laserIndex], cellInfo['tetrode'], cluster=cellInfo['cluster'])
        eventOnsetTimes = loader.get_event_onset_times(eventData)
        spikeTimestamps = spikeData.timestamps
        laserResponse = laser_response(spikeTimeStamps, eventOnsetTimes)
    else:
        laserResponse = False
    return suppressionStats, atBestFreq, laserResponse

def at_best_freq(spikeTimeStamps, eventOnsetTimes, charFreq, frequencies, timeRange=[0.0,0.1], fullRange = [0.0, 0.7]):
    atBestFreq = False
    numFreqs = np.unique(frequencies)
    spikeArray = np.zeros(len(numFreqs))
    trialsEachCond = behavioranalysis.find_trials_each_type(frequencies, numFreqs)
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullRange)
    spikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    baseTimeRange = [timeRange[1]+0.1, fullRange[1]]
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    baselineSpikeSDev = np.std(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    for freq in range(len(numFreqs)):
        trialsThisFreq = trialsEachCond[:,freq]
        if spikeCountMat.shape[0] != len(trialsThisFreq):
            spikeCountMat = spikeCountMat[:-1,:]
            print "FIXME: Using bad hack to make event onset times equal number of trials"
        thisFreqCounts = spikeCountMat[trialsThisFreq].flatten()
        spikeArray[freq] = np.mean(thisFreqCounts)/(timeRange[1]-timeRange[0])
    bestFreqIndex = np.argmax(spikeArray)
    minIndex = bestFreqIndex-1 if bestFreqIndex>0 else 0
    maxIndex = bestFreqIndex+1 if bestFreqIndex<(len(numFreqs)-1) else len(numFreqs)-1
    bestFreqs = [numFreqs[minIndex], numFreqs[maxIndex]]
    if charFreq >= bestFreqs[0] and charFreq <= bestFreqs[1]:
        if np.max(spikeArray) > (baselineSpikeRate + baselineSpikeSDev):
            atBestFreq = True
    return atBestFreq

def laser_response(spikeTimeStamps, eventOnsetTimes, timeRange=[0.0, 0.1], fullRange=[0.0, 0.7]):
    spikeTimesFromEventOnset, trialIndexForEachSpike, indexLimitsEachTrial = spikesanalysis.eventlocked_spiketimes(
                                                                                                        spikeTimeStamps, 
                                                                                                        eventOnsetTimes,
                                                                                                        fullRange)
    baseTimeRange = [timeRange[1]+0.1, fullRange[1]]
    baseSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, baseTimeRange)
    baselineSpikeRate = np.mean(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    baselineSpikeSDev = np.std(baseSpikeCountMat)/(baseTimeRange[1]-baseTimeRange[0])
    laserSpikeCountMat = spikesanalysis.spiketimes_to_spikecounts(spikeTimesFromEventOnset, indexLimitsEachTrial, timeRange)
    laserSpikeRate = np.mean(laserSpikeCountMat)/(timeRange[1]-timeRange[0])
    return (laserSpikeRate > (baselineSpikeRate + 2*baselineSpikeSDev))
    
def compute_suppression_stats(spikeArray, bands):
    SSLowAmp = (max(spikeArray[:,1])-spikeArray[:,1][-1])/max(spikeArray[:,1])
    peakLocLowAmp = bands[np.argmax(spikeArray[:,1])]
    SSHighAmp = (max(spikeArray[:,0])-spikeArray[:,0][-1])/max(spikeArray[:,0])
    peakLocHighAmp = bands[np.argmax(spikeArray[:,0])]
    return [SSLowAmp, SSHighAmp, peakLocLowAmp, peakLocHighAmp]
        
    
        

